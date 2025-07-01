@echo off
echo ========================================
echo   Maid-MCP Python Launcher
echo ========================================
echo.

:: Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python not found!
    echo Please install Python 3.8 or higher.
    echo.
    pause
    exit /b 1
)

:: Check if psutil is installed
python -c "import psutil" >nul 2>&1
if errorlevel 1 (
    echo ERROR: psutil module not found!
    echo Installing psutil...
    pip install psutil
    if errorlevel 1 (
        echo Failed to install psutil. Please run: pip install psutil
        pause
        exit /b 1
    )
)

:: Run the Python launcher
echo Starting Maid-MCP with proper process management...
echo.
python start_all.py

:: The Python script handles everything including cleanup on exit
