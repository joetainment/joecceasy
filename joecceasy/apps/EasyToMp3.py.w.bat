@echo off
cd /d %~dp0 
start "" pythonw "EasyToMp3.py" %*
timeout 5


