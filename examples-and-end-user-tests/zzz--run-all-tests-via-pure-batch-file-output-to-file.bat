@echo off
cd /d %~dp0
echo Running joecceasy end user tests/examples... > gitignore--test-results-deleteme.txt
echo ############################################## >> gitignore--test-results-deleteme.txt
echo ############################################## >> gitignore--test-results-deleteme.txt
echo: >> gitignore--test-results-deleteme.txt
echo: >> gitignore--test-results-deleteme.txt
REM  unfortunately this would run .py resources as well
for %%f in (test__*.py) do (
    echo ############################ >> gitignore--test-results-deleteme.txt
    echo #### Start test of python file: %%~nf.py >> gitignore--test-results-deleteme.txt
    REM echo #### python start test:  
    python %%~nf.py >> gitignore--test-results-deleteme.txt
    echo #### End of test. >> gitignore--test-results-deleteme.txt
    echo ############################ >> gitignore--test-results-deleteme.txt
    echo: >> gitignore--test-results-deleteme.txt
    echo: >> gitignore--test-results-deleteme.txt
    echo: >> gitignore--test-results-deleteme.txt
    REM process_in "%%~nf.in"
)
