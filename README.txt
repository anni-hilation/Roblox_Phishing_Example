Setup needed: 
Python 3.14.0:
pip install pyinstaller
pip install flask
pip install flask-cors
pip install requests

Ngrok:
To set up ngrok, first download it from the official site and unzip it to a folder that’s easy to access. Then, open a command prompt in that folder (or add it to your system PATH) so you can run ngrok from anywhere. Before using it, you need to link ngrok to your account by running ngrok config add-authtoken YOUR_AUTHTOKEN, replacing YOUR_AUTHTOKEN with the key from your ngrok dashboard.

Start Server manually: 
1.navigate to Folder: (cd Desktop, cd RServer)
2.run locally: python server.py
3. open new cmd and run: ngrok http 3000
4. ctrl C to stop (do in both command windows)
(Problems migh happen because the public/index.html is called "template.index.html",and the Server expects "index.html" if starting manually, copy it and rename it "index.html". in line 119, 
enter the url that ngrok gives you 
const response = await fetch("NGROK_URL_REPLACE/senden", {
make sure to leave the /senden in)


Start server using dist/launcher.exe (doesnt rlly work, because it cant properly get the url from ngrok. i made this with chatgpt and i have no idea what im doing or how to fix it)
1.Double tap exe, then press start
2.DONT FORGET TO TURN IT OFF USING THE OFF BUTTON OR EVERYTHING WILL BREAK 
(to fix, go in the template.index.html and fix line 119. should look like this when Server is off:
const response = await fetch("NGROK_URL_REPLACE/senden", { )
3. if editing files that impact the exe, run "pyinstaller --onefile --windowed --hidden-import=requests launcher.py" in cmd. that will replace the exe with a new one, with all your changes. (not needed if editing the website html or server, im not sure abt server but html is def safe)

the "username" and the "password" are both avalible in the json file.
