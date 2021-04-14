@echo off
cd /d %~dp0 
start "" pythonw "example__qtui__JoeccFileRenamer.py" %*
timeout 6

