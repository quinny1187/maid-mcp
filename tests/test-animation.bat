@echo off
echo Running Animation Test...
echo.
cd /d "%~dp0\.."
node tests\test-animation.js
echo.
pause
