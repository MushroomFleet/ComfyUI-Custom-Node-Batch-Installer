@echo off
setlocal

echo ComfyUI Custom Nodes Installation Script
echo =======================================
echo.

:: Check if Python is available
where python >nul 2>nul
if %ERRORLEVEL% neq 0 (
    echo Error: Python not found in PATH
    echo Please ensure Python is installed and added to your PATH
    pause
    exit /b 1
)

:: Check if git is available
where git >nul 2>nul
if %ERRORLEVEL% neq 0 (
    echo Error: Git not found in PATH
    echo Please ensure Git is installed and added to your PATH
    pause
    exit /b 1
)

:: Check if we're in the custom_nodes directory
if not exist "clone-custom-nodes.py" (
    echo Error: clone-custom-nodes.py not found
    echo Please ensure this batch file is in the same directory as clone-custom-nodes.py
    pause
    exit /b 1
)

:: Check if comfy-repos.txt exists
if not exist "comfy-repos.txt" (
    echo Error: comfy-repos.txt not found
    echo Please create comfy-repos.txt with your repository URLs
    pause
    exit /b 1
)

echo Starting installation process...
echo.

:: Run the main installation script
python clone-custom-nodes.py

echo.
echo Installation process completed
echo.
pause
