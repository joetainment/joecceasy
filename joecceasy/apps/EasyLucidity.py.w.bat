@echo off
cd /d %~dp0 
start "" pythonw "EasyLucidity.py" %*
timeout 5