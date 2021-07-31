@echo off
cd /d %~dp0 
start "" C:\WinPython64-3.8.6.0dot\python-3.8.6.amd64\pythonw.exe "EasyLauncher.py" %*
timeout 1

