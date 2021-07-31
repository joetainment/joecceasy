@echo off
cd /d %~dp0 
start "" python "EasyToMp3.py" %*
timeeout 99