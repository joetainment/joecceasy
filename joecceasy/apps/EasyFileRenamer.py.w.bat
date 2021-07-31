@echo off
cd /d %~dp0 
start "" pythonw "EasyFileRenamer.py" %*
timeout 1

