@echo off
title Auto Server + Ngrok Starter

REM --- start Flask server in new window ---
start "Flask Server" cmd /k "python server.py"

REM --- start ngrok in new window ---
start "Ngrok Tunnel" cmd /k "ngrok http 3000"

REM --- wait for ngrok to start ---
timeout /t 3 >nul

REM --- get the ngrok URL ---
for /f %%i in ('python get_ngrok_url.py') do set NGROK_URL=%%i

echo Detected ngrok URL: %NGROK_URL%

REM --- build fresh index.html from the template ---
powershell -Command "(Get-Content public/index.template.html).replace('NGROK_URL_REPLACE', '%NGROK_URL%') | Set-Content public/index.html"

echo Updated index.html with new URL.
pause
