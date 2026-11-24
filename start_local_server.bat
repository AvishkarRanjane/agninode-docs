@echo off
title AgniNode Local Document & Video Server
cd /d "%~dp0"
echo ========================================================
echo        Starting AgniNode Local Server on Port 8080
echo ========================================================
echo Any phone connected to your Wi-Fi can scan the QR code!
echo.
python server.py
pause
