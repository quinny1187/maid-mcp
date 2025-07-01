@echo off
echo ========================================
echo   Voice Input Dependencies Installer
echo ========================================
echo.
echo This will install Python packages needed for speech recognition.
echo.

:: Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python not found!
    echo Please install Python 3.8 or later from python.org
    echo Make sure to check "Add Python to PATH" during installation.
    echo.
    pause
    exit /b 1
)

echo Python found. Installing dependencies...
echo.

:: Install speech recognition requirements
echo Installing speech recognition packages...
cd voice\incoming
pip install -r requirements.txt

if errorlevel 1 (
    echo.
    echo ERROR: Failed to install some packages.
    echo.
    echo Common issues:
    echo - PyAudio may need Visual C++ Build Tools
    echo - Try: pip install pipwin
    echo - Then: pipwin install pyaudio
    echo.
) else (
    echo.
    echo ✓ All dependencies installed successfully!
    echo.
)

cd ..\..

echo.
echo Installation complete!
echo You can now run start_all.bat to launch the complete system.
echo.
pause
