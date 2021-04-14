@echo off
cd /d %~dp0
echo Running joecceasy end user examples...
echo ##############################################
echo ##############################################
echo:
echo:
REM  unfortunately this would run .py resources as well
for %%f in (example__*.py) do (
    echo ############################
    echo #### Start test of python file: %%~nf.py 
    REM echo #### python start test:  
    python %%~nf.py
    echo #### End of test.
    echo ############################
    echo:
    echo:
    echo:
    REM process_in "%%~nf.in"
)

timeout 20
