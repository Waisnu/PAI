@echo off
echo ===============================================
echo   COVID-19 Analysis Project - Auto Setup
echo ===============================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python is not installed or not in PATH
    echo Please install Python 3.8 or later from https://python.org
    pause
    exit /b 1
)

echo [SETUP] Python found - checking version...
python --version

REM Create virtual environment if it doesn't exist
if not exist "venv" (
    echo [SETUP] Creating virtual environment...
    python -m venv venv
    if errorlevel 1 (
        echo [ERROR] Failed to create virtual environment
        pause
        exit /b 1
    )
) else (
    echo [SETUP] Virtual environment already exists
)

REM Activate virtual environment
echo [SETUP] Activating virtual environment...
call venv\Scripts\activate.bat
if errorlevel 1 (
    echo [ERROR] Failed to activate virtual environment
    pause
    exit /b 1
)

REM Install/upgrade dependencies
echo [SETUP] Installing dependencies...
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
if errorlevel 1 (
    echo [ERROR] Failed to install dependencies
    pause
    exit /b 1
)

echo.
echo ===============================================
echo   Setup Complete! Running the project...
echo ===============================================
echo.

REM Run the project
python run.py all

echo.
echo ===============================================
echo   Project execution completed!
echo ===============================================
echo.
echo You can now run individual activities using:
echo   python run.py activity1
echo   python run.py activity2
echo   etc.
echo.
pause 