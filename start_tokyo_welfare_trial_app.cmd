@echo off
cd /d "%~dp0"
python apps\tokyo_welfare_trial_app.py
if errorlevel 1 pause
