@echo off
setlocal enabledelayedexpansion

echo Checking Python installation...
where python >nul 2>nul
if %ERRORLEVEL% neq 0 (
    echo Error: Python not found in PATH
    echo Please ensure Python is installed and added to your PATH
    pause
    exit /b 1
)

echo Creating virtual environment...
python -m venv venv

echo Activating virtual environment...
call venv\Scripts\activate.bat

echo Installing dependencies...
python -m pip install --upgrade pip
pip install -r requirements.txt

echo Installation complete!
echo You can now run start-web.bat to launch the application
pause
