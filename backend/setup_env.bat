@echo off
echo Setting up project environment...

REM Check if Python is installed
where python >nul 2>nul
if %errorlevel% neq 0 (
    echo Python is not installed. Please install Python 3.10+ first.
    pause
    exit /b
)

REM Create virtual environment
python -m venv venv

REM Activate virtual environment
call venv\Scripts\activate

REM Upgrade pip
python -m pip install --upgrade pip

REM Install requirements
pip install -r requirements.txt

echo.
echo ==============================
echo Setup complete! 
echo To start, activate with:
echo venv\Scripts\activate
echo ==============================
pause
