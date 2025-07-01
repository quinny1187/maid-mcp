@echo off
echo ========================================
echo   Stopping All Maid-MCP Systems
echo ========================================
echo.

echo [1/5] Stopping avatar display windows...
taskkill /F /FI "WINDOWTITLE eq Mimi - Maid Avatar*" >nul 2>&1
taskkill /F /FI "WINDOWTITLE eq pygame window*" >nul 2>&1

echo [2/5] Stopping voice input windows...
taskkill /F /FI "WINDOWTITLE eq Voice Input - Maid MCP*" >nul 2>&1
taskkill /F /FI "WINDOWTITLE eq Voice Input*" >nul 2>&1

echo [3/5] Stopping Python processes by command line...
:: Use WMIC to find and kill by command line
wmic process where "CommandLine like '%%avatar_display.py%%' and name='python.exe'" delete >nul 2>&1
wmic process where "CommandLine like '%%avatar_state_server.py%%' and name='python.exe'" delete >nul 2>&1
wmic process where "CommandLine like '%%speechListener.py%%' and name='python.exe'" delete >nul 2>&1

echo [4/5] Killing processes on port 3338...
:: Kill any process listening on port 3338
for /f "tokens=5" %%a in ('netstat -aon ^| find ":3338" ^| find "LISTENING"') do (
    echo   Found process on port 3338 (PID: %%a)
    taskkill /F /PID %%a >nul 2>&1
)

echo [5/5] Final cleanup with PowerShell...
:: PowerShell cleanup for any remaining processes
powershell -Command "Get-Process python -ErrorAction SilentlyContinue | Where-Object {$_.CommandLine -match 'avatar_display|avatar_state_server|speechListener|maid-mcp'} | ForEach-Object { Write-Host '  Stopping process:' $_.Id $_.CommandLine.Substring(0, [Math]::Min(50, $_.CommandLine.Length))...; Stop-Process $_ -Force }" 2>nul

:: Also try to kill any cmd windows that might be running our scripts
taskkill /F /FI "WINDOWTITLE eq Administrator*avatar*" >nul 2>&1
taskkill /F /FI "WINDOWTITLE eq Administrator*speech*" >nul 2>&1

:: Final verification
echo.
echo Verifying all processes are stopped...
timeout /t 1 /nobreak >nul

:: Check if port 3338 is still in use
netstat -an | find ":3338" | find "LISTENING" >nul
if not errorlevel 1 (
    echo WARNING: Port 3338 is still in use!
    echo Attempting forceful cleanup...
    for /f "tokens=5" %%a in ('netstat -aon ^| find ":3338" ^| find "LISTENING"') do (
        taskkill /F /PID %%a >nul 2>&1
        timeout /t 1 /nobreak >nul
    )
)

echo.
echo ✓ All maid-mcp systems stopped.
echo.
pause
