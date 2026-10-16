@echo off
title Verify Telegram Connection
cls
echo ===================================================
echo     VERIFY TELEGRAM BOT CONNECTION
echo ===================================================
echo.
echo Checking your TELEGRAM_BOT_TOKEN from .env file...
echo.
py bot.py --verify
echo.
echo ===================================================
pause
