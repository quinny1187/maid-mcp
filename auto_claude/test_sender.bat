@echo off
echo ========================================
echo   Auto-Claude Ultra Fast Sender Test
echo ========================================
echo.
echo This will send a test message to Claude Desktop
echo Make sure Claude Desktop is open!
echo.
echo If you get an error about multiple windows, run debug_windows.bat first
echo.
pause

python ultra_fast_sender.py

echo.
echo Test complete! Check if the message appeared in Claude.
echo.
echo If it failed, try:
echo 1. Close VS Code or other apps with 'Claude' in the title
echo 2. Run debug_windows.bat to see what windows are detected
echo.
pause