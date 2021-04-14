@echo off
cd /d %~dp0
python aaall-unittests-run.py --output-to-delme-file
REM python -m unittest discover -s . -p "test__*.py"
timeout 5
