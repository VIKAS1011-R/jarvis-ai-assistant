@echo off
echo Starting J.A.R.V.I.S...
echo.

REM Check if virtual environment exists
if not exist "jarvis_env" (
    echo Virtual environment not found. Running setup first...
    python setup.py
    echo.
)

REM Activate virtual environment and run J.A.R.V.I.S
echo Activating virtual environment...
call jarvis_env\Scripts\activate
echo Running J.A.R.V.I.S...
python jarvis.py

REM Deactivate when done
deactivate
echo.
echo J.A.R.V.I.S has been shut down.
pause