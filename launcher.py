import subprocess
import threading
import time
import tkinter as tk
import requests
import json
import os
from datetime import datetime

# ----------------------
# GLOBAL VARIABLES
# ----------------------
flask_proc = None
ngrok_proc = None
start_time = None
running = False
total_sessions = 0
current_sessions = 0
dark_mode = False

# ----------------------
# HELPER FUNCTIONS
# ----------------------

root = tk.Tk()
root.title("Auto Server Launcher")
root.geometry("600x550")
root.resizable(False, False)
root.config(bg="#f0f0f0")

log_box = tk.Text(root, height=15, width=70, bg="grey", fg="black", insertbackground="black")
log_box.pack(pady=10)

def log(message):
    """Add a line to the log box."""
    log_box.insert(tk.END, f"{message}\n")
    log_box.see(tk.END)


def read_ngrok_url():
    """Reads the ngrok public URL from the local API."""
    try:
        data = requests.get("http://127.0.0.1:4040/api/tunnels").json()
        return data["tunnels"][0]["public_url"]
    except:
        return None

def wait_for_ngrok(timeout=10):
    """Wait up to `timeout` seconds for ngrok to start and return URL."""
    import time
    for _ in range(timeout * 2):  # check twice per second
        url = read_ngrok_url()
        if url:
            return url
        time.sleep(0.5)
    return None


def update_index_html(url):
    """Builds a fresh index.html from index.template.html."""
    template_path = "public/index.template.html"
    target_path = "public/index.html"

    with open(template_path, "r", encoding="utf-8") as f:
        content = f.read()

    content = content.replace("NGROK_URL_REPLACE", url)

    with open(target_path, "w", encoding="utf-8") as f:
        f.write(content)

def restore_template():
    """Restores the HTML back to the template."""
    os.system("copy /Y public\\index.template.html public\\index.html >nul")

def start_server():
    global flask_proc, ngrok_proc, running, start_time, current_sessions, total_sessions

    if running:
        log("Server is already running!")
        return

    running = True
    start_time = time.time()
    current_sessions = 0
    total_sessions = 0

    # Start Flask server
    flask_proc = subprocess.Popen(
        ["python", "server.py"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )

    # Start ngrok
    ngrok_proc = subprocess.Popen(
        ["ngrok", "http", "3000"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )

    # Wait for ngrok to be ready
    url = wait_for_ngrok(timeout=10)
    if url:
        update_index_html(url)


# Wait for ngrok to be ready
url = wait_for_ngrok(timeout=10)  # poll for up to 10 seconds

if url:
    update_index_html(url)
    log("SERVER STARTED SUCCESSFULLY!")
    log(f"Access your website here: {url}/")
else:
    log("SERVER STARTED, but could not fetch ngrok URL. Check ngrok console.")


def stop_server():
    global flask_proc, ngrok_proc, running, current_sessions, total_sessions

    if not running:
        log("Server is not running!")
        return

    running = False

    if flask_proc:
        flask_proc.kill()

    if ngrok_proc:
        ngrok_proc.kill()

    restore_template()
    log("SERVER STOPPED & HTML RESTORED")

    # Reset session counters
    current_sessions = 0
    total_sessions = 0
    current_label.config(text=f"Current Sessions: {current_sessions}")
    total_label.config(text=f"Total Sessions: {total_sessions}")

def stop_server():
    global flask_proc, ngrok_proc, running

    if not running:
        log("Server is not running!")
        return

    running = False

    if flask_proc:
        flask_proc.kill()

    if ngrok_proc:
        ngrok_proc.kill()

    restore_template()
    log("SERVER STOPPED & HTML RESTORED")

def toggle_dark_mode():
    global dark_mode
    dark_mode = not dark_mode

    if dark_mode:
        root.config(bg="#121212")
        log_box.config(bg="black", fg="#0f0", insertbackground="white")
        uptime_label.config(bg="#121212", fg="white")
        current_label.config(bg="#121212", fg="white")
        total_label.config(bg="#121212", fg="white")
    else:
        root.config(bg="#f0f0f0")
        log_box.config(bg="grey", fg="black", insertbackground="black")
        uptime_label.config(bg="#f0f0f0", fg="black")
        current_label.config(bg="#f0f0f0", fg="black")
        total_label.config(bg="#f0f0f0", fg="black")

def uptime_loop():
    """Updates uptime + stats every 1 second."""
    global total_sessions, current_sessions

    while True:
        if running:
            elapsed = int(time.time() - start_time)
            hours = elapsed // 3600
            minutes = (elapsed % 3600) // 60
            seconds = elapsed % 60

            uptime_label.config(text=f"Uptime: {hours:02}:{minutes:02}:{seconds:02}")

            # Read logs from Flask
            if flask_proc and flask_proc.stdout:
                while True:
                    line = flask_proc.stdout.readline()
                    if not line:
                        break
                    log(line.strip())

                    # Optional: detect GET requests (simple heuristic)
                    if "GET /" in line and "200" in line:
                        current_sessions += 1
                        total_sessions += 1

            current_label.config(text=f"Current Sessions: {current_sessions}")
            total_label.config(text=f"Total Sessions: {total_sessions}")
        time.sleep(1)

# ----------------------
# GUI SETUP
# ----------------------

start_btn = tk.Button(root, text="START SERVER", font=("Arial", 14), command=start_server)
start_btn.pack(pady=10)

stop_btn = tk.Button(root, text="STOP SERVER", font=("Arial", 14), command=stop_server)
stop_btn.pack(pady=10)

dark_mode_btn = tk.Button(root, text="Toggle Dark Mode", font=("Arial", 12), command=toggle_dark_mode)
dark_mode_btn.pack(pady=5)

uptime_label = tk.Label(root, text="Uptime: 00:00:00", font=("Arial", 12), bg="#f0f0f0", fg="black")
uptime_label.pack(pady=5)

current_label = tk.Label(root, text="Current Sessions: 0", font=("Arial", 12), bg="#f0f0f0", fg="black")
current_label.pack(pady=5)

total_label = tk.Label(root, text="Total Sessions: 0", font=("Arial", 12), bg="#f0f0f0", fg="black")
total_label.pack(pady=5)

# Start uptime/log thread
threading.Thread(target=uptime_loop, daemon=True).start()

root.mainloop()
