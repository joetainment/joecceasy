@echo off
cd /d %~dp0 
python "test__ArgsParser_01.py" "positional arg a" "positional arg b" "positional arg c" --myStringArg "this is my string!" --myFlagArg --myFloatArg 0.3 --myIntArg 7
timeout 6