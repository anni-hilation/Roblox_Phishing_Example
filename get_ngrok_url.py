import time, json, urllib.request

# wait for ngrok to be fully started
time.sleep(2)

try:
    with urllib.request.urlopen("http://127.0.0.1:4040/api/tunnels") as r:
        data = json.load(r)
        url = data["tunnels"][0]["public_url"]
        print(url)
except:
    print("ERROR")
