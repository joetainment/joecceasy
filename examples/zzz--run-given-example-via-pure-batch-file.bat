@echo off
cd /d %~dp0
echo Running given joecceasy end user examples...
echo ##############################################
echo ##############################################
echo:
echo:
REM  unfortunately this would run .py resources as well
for %%f in (%*) do (
    echo ############################
    echo #### Start test of python file: %%f
    REM echo #### python start test:  
    python %%f
    echo #### End of test.
    echo ############################
    echo:
    echo:
    echo:
    REM process_in "%%~nf.in"
)

timeout 20
