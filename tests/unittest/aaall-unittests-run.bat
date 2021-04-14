@echo off
cd /d %~dp0
python aaall-unittests-run.py
timeout 5
