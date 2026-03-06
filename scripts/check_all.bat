@echo off
setlocal enabledelayedexpansion

REM Get project root (parent directory of script)
set SCRIPT_DIR=%~dp0
for %%i in ("%SCRIPT_DIR%..") do set PROJECT_ROOT=%%~fi

set INPUT_DIR=%PROJECT_ROOT%\tests\inputs
set EXPECTED_DIR=%PROJECT_ROOT%\tests\expected_txt
set SRC_MAIN=%PROJECT_ROOT%\src\main.py
set TEMP_DIR=%PROJECT_ROOT%\tests\temp_outputs

if not exist "%TEMP_DIR%" mkdir "%TEMP_DIR%"

set PASS_COUNT=0
set FAIL_COUNT=0

echo Checking all tests...
echo ----------------------------------

for %%f in ("%INPUT_DIR%\*.txt") do (

    set test_name=%%~nxf
    set input_file=%%f
    set expected_file=%EXPECTED_DIR%\!test_name!
    set output_file=%TEMP_DIR%\!test_name!

    echo Checking !test_name!

    python "%SRC_MAIN%" t < "!input_file!" > "!output_file!"

    if exist "!expected_file!" (
        fc "!output_file!" "!expected_file!" > nul

        if !errorlevel! == 0 (
            echo PASS
            set /a PASS_COUNT+=1
        ) else (
            echo FAIL
            echo Differences:
            fc "!output_file!" "!expected_file!"
            set /a FAIL_COUNT+=1
        )
    ) else (
        echo ERROR: Expected file not found: !expected_file!
        set /a FAIL_COUNT+=1
    )

    echo ----------------------------------
)

echo Total Passed: !PASS_COUNT!
echo Total Failed: !FAIL_COUNT!

if !FAIL_COUNT! == 0 (
    echo All tests passed!
) else (
    echo Some tests failed.
)

pause