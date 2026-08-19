@echo off
TITLE Nexus AI Launcher
echo Starting Nexus AI Backend Server...
start cmd /k "uvicorn app:app --reload"
timeout /t 2 >nul
echo Opening Nexus AI Dashboard in Browser...
start index.html
exit