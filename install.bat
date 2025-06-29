@echo off
echo Installing maid-mcp dependencies...
echo.

npm install

if %errorlevel% neq 0 (
    echo.
    echo ERROR: npm install failed!
    echo Please make sure Node.js is installed.
    pause
    exit /b 1
)

echo.
echo Installation complete!
echo.
echo Next steps:
echo 1. Test voice: npm test
echo 2. Configure Claude Desktop using CLAUDE_CONFIG.md
echo.
pause
