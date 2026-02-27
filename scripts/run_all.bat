@echo off
setlocal enabledelayedexpansion

REM Get project root
set "PROJECT_ROOT=%~dp0.."
set "INPUT_DIR=%PROJECT_ROOT%\tests\inputs"
set "SRC_MAIN=%PROJECT_ROOT%\src\main.py"

echo Running all test inputs...
echo ----------------------------------

for %%f in ("%INPUT_DIR%\*.txt") do (
    echo Running %%~nxf
    echo ----------------------------------

    python "!SRC_MAIN!" < "%%f"

    echo.
)

echo Finished running all tests.
pause