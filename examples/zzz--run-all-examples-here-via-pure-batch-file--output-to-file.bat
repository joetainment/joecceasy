@echo off
cd /d %~dp0
echo Running joecceasy end user examples, outputting to file...
echo Running joecceasy end user examples... > gitignore--test-results-deleteme.txt
echo ############################################## >> gitignore--test-results-deleteme.txt
echo ############################################## >> gitignore--test-results-deleteme.txt
echo: >> gitignore--test-results-deleteme.txt
echo: >> gitignore--test-results-deleteme.txt
REM  unfortunately this would run .py resources as well
for %%f in (example__*.py) do (
    echo ############################ >> gitignore--test-results-deleteme.txt
    echo #### Start test of python file: %%~nf.py
    echo #### Start test of python file: %%~nf.py >> gitignore--test-results-deleteme.txt
    REM echo #### python start test:  
    python %%~nf.py 1>> gitignore--test-results-deleteme.txt 2>&1
    echo #### End of test. >> gitignore--test-results-deleteme.txt
    echo ############################ >> gitignore--test-results-deleteme.txt
    echo: >> gitignore--test-results-deleteme.txt
    echo: >> gitignore--test-results-deleteme.txt
    echo: >> gitignore--test-results-deleteme.txt
    REM process_in "%%~nf.in"
)
echo Examples no longer running, check output file to see info/success/fail
timeout 5