@echo off
title Push DealHype Bot to GitHub
cls
echo ===================================================
echo     PUSH DEALHYPE BOT TO GITHUB (FOR 24x7 CLOUD)
echo ===================================================
echo.
git init
git add .
git commit -m "Deploy DealHype 24x7 Automated Bot"
echo.
echo Code committed locally!
echo Agar aapne GitHub par repo banayi hai, to URL paste karein:
set /p REPO_URL="GitHub Repo URL (jaise https://github.com/username/dealhype.git): "
if not "%REPO_URL%"=="" (
    git branch -M main
    git remote remove origin 2>nul
    git remote add origin %REPO_URL%
    git push -u origin main --force
    echo.
    echo ===================================================
    echo Code pushed to GitHub successfully!
    echo Ab GitHub Actions / Render 24x7 automatic chalega!
    echo ===================================================
)
pause
