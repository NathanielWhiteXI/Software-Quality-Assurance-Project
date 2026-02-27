@echo off
setlocal enabledelayedexpansion

REM Paths
set PROJECT_ROOT=%~dp0..
set INPUT_DIR=%PROJECT_ROOT%\tests\inputs
set EXPECTED_DIR=%PROJECT_ROOT%\tests\expected_txt
set SRC_MAIN=%PROJECT_ROOT%\src\main.py
set TEMP_DIR=%PROJECT_ROOT%\tests\temp_outputs

if not exist %TEMP_DIR% mkdir %TEMP_DIR%

set PASS_COUNT=0
set FAIL_COUNT=0

echo Checking all tests...
echo ----------------------------------

for %%f in (%INPUT_DIR%\*.txt) do (
    set TEST_NAME=%%~nxf
    set INPUT_FILE=%%f
    set EXPECTED_FILE=%EXPECTED_DIR%\!TEST_NAME!
    set OUTPUT_FILE=%TEMP_DIR%\!TEST_NAME!

    echo Checking !TEST_NAME!

    python %SRC_MAIN% < "!INPUT_FILE!" > "!OUTPUT_FILE!"

    fc "!OUTPUT_FILE!" "!EXPECTED_FILE!" > nul

    if !errorlevel! == 0 (
        echo PASS
        set /a PASS_COUNT+=1
    ) else (
        echo FAIL
        echo Differences:
        fc "!OUTPUT_FILE!" "!EXPECTED_FILE!"
        set /a FAIL_COUNT+=1
    )

    echo ----------------------------------
)

echo Total Passed: %PASS_COUNT%
echo Total Failed: %FAIL_COUNT%

if %FAIL_COUNT% == 0 (
    echo All tests passed!
) else (
    echo Some tests failed.
)

pause