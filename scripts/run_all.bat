@echo off
setlocal enabledelayedexpansion

REM Get project root (parent of the script directory)
set SCRIPT_DIR=%~dp0
for %%i in ("%SCRIPT_DIR%..") do set PROJECT_ROOT=%%~fi

set INPUT_DIR=%PROJECT_ROOT%\tests\inputs
set SRC_MAIN=%PROJECT_ROOT%\src\main.py

echo Running all test inputs...
echo ----------------------------------

for %%f in ("%INPUT_DIR%\*.txt") do (
    set test_name=%%~nxf

    echo Running !test_name!
    echo ----------------------------------

    python "%SRC_MAIN%" t < "%%f"

    echo.
)

echo Finished running all tests.
pause