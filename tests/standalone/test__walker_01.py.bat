@echo off
cd /d %~dp0 
python "test__walker_01.py" %*
timeout 6

