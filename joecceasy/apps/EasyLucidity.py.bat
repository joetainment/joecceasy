@echo off
cd /d %~dp0 
python "EasyLucidity.py" %*
timeout 6

