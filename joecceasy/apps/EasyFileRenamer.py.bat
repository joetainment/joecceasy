@echo off
cd /d %~dp0 
python "EasyFileRenamer.py" %*
timeout 6

