@echo off
echo Starting Maid Avatar System...
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.7+ from python.org
    pause
    exit /b 1
)

REM Install required packages if needed
echo Checking dependencies...
pip show PyQt5 >nul 2>&1
if errorlevel 1 (
    echo Installing PyQt5...
    pip install PyQt5
)

pip show flask >nul 2>&1
if errorlevel 1 (
    echo Installing Flask...
    pip install flask flask-cors
)

pip show requests >nul 2>&1
if errorlevel 1 (
    echo Installing requests...
    pip install requests
)

echo.
echo Starting state server...
start /min cmd /c "python avatar_state_server.py"

REM Wait for server to start
timeout /t 2 /nobreak >nul

echo Starting avatar display...
start python avatar_display.py

echo.
echo Avatar system started!
echo.
echo Controls:
echo - Drag with left mouse button to move
echo - Right-click to close
echo - Double-click to close
echo - Press ESC to close
echo.
echo The avatar will appear in the top-right area of your screen.
pause