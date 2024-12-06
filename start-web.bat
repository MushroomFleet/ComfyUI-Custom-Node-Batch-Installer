@echo off
setlocal

if not exist "venv" (
    echo Virtual environment not found!
    echo Please run install.bat first to set up the environment
    pause
    exit /b 1
)

echo Activating virtual environment...
call venv\Scripts\activate.bat

echo Starting ComfyUI Custom Node Installer...
python gradio_wrapper.py

deactivate
pause
