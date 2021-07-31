@echo off
cd /d %~dp0
python aaall-pytests-run.py > gitignore----aaall-pytests-output.txt 2>&1
timeout 5
