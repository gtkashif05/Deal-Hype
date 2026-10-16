@echo off
title Testing Loot Deals Bot
cls
echo ===================================================
echo     AMAZON & FLIPKART LOOT DEALS BOT - TEST MODE
echo ===================================================
echo.
echo Fetching latest live deals and checking affiliate link conversion...
echo.
py bot.py --test
echo.
echo ===================================================
echo Test complete! Press any key to exit.
echo ===================================================
pause >nul
