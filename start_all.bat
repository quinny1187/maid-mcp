@echo off
echo ========================================
echo   Maid-MCP Complete System Launcher
echo ========================================
echo.

:: First run the stop_all script to ensure clean shutdown
echo Ensuring clean shutdown of any existing processes...
call stop_all.bat >nul 2>&1

:: Additional cleanup to be extra sure
echo Performing additional cleanup...

:: Kill by window title
taskkill /F /FI "WINDOWTITLE eq Mimi - Maid Avatar*" >nul 2>&1
taskkill /F /FI "WINDOWTITLE eq pygame window*" >nul 2>&1
taskkill /F /FI "WINDOWTITLE eq Voice Input*" >nul 2>&1

:: Kill Python processes by command line
wmic process where "CommandLine like '%%avatar%%' and name='python.exe'" delete >nul 2>&1
wmic process where "CommandLine like '%%speechListener%%' and name='python.exe'" delete >nul 2>&1

:: Kill by process name patterns
for /f "tokens=2" %%i in ('tasklist /fi "imagename eq python.exe" ^| findstr avatar') do taskkill /pid %%i /f >nul 2>&1
for /f "tokens=2" %%i in ('tasklist /fi "imagename eq python.exe" ^| findstr speech') do taskkill /pid %%i /f >nul 2>&1

:: Kill any process on port 3338
for /f "tokens=5" %%a in ('netstat -aon ^| find ":3338" ^| find "LISTENING"') do (
    echo Killing process on port 3338 (PID: %%a)
    taskkill /F /PID %%a >nul 2>&1
)

:: PowerShell cleanup as final backup
powershell -Command "Get-Process python -ErrorAction SilentlyContinue | Where-Object {$_.CommandLine -match 'avatar|speech'} | Stop-Process -Force" >nul 2>&1

echo Cleanup complete.
echo.

:: Wait longer to ensure processes are fully terminated
echo Waiting for processes to terminate...
timeout /t 3 /nobreak >nul

echo Starting all maid-mcp components...
echo.

:: Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo WARNING: Python not found. Voice input will not work.
    echo Please install Python 3.8+ for speech recognition.
    echo.
    echo For full functionality with process management, run: start_all_python.bat
    echo.
)

:: Start avatar display in background
echo [1/3] Starting avatar display...
cd /d "%~dp0avatar"
start /B "" cmd /c "python avatar_display.py"
cd /d "%~dp0"
timeout /t 2 /nobreak >nul

:: Start avatar state server in background
echo [2/3] Starting avatar state server...
cd /d "%~dp0avatar"
start /B "" cmd /c "python avatar_state_server.py"
cd /d "%~dp0"
timeout /t 2 /nobreak >nul

:: Start voice input listener in new window
echo [3/3] Starting voice input listener...
echo.
start "Voice Input - Maid MCP" cmd /k "cd /d %~dp0voice\incoming && python speechListener.py"

echo.
echo ========================================
echo   All systems started successfully!
echo ========================================
echo.
echo Avatar: Running in background
echo Voice: Check the Voice Input window
echo.
echo To stop all systems:
echo 1. Run stop_all.bat
echo 2. Or close this window and run stop_all.bat
echo 3. Or use start_all_python.bat for better process management
echo.
echo Press any key to continue running...
pause >nul

:: Keep this window open to monitor
echo.
echo Systems are running. Press Ctrl+C to stop all systems.
echo.

:: Wait for user to press Ctrl+C
:wait_loop
timeout /t 10 /nobreak >nul
goto wait_loop

:cleanup
echo.
echo Shutting down all systems...
call stop_all.bat
exit
