@echo off
title Restore Placeholder

REM Restore index.html back to the template
copy /Y public\index.template.html public\index.html >nul

echo index.html restored to placeholder version.

echo.
echo If Flask or ngrok windows are open, close them manually.
pause
