@echo off
echo Running Giphy API test...
echo.

cd /d "%~dp0\.."

node tests/test-giphy.js

echo.
pause
