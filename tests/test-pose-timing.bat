@echo off
echo New Pose-Based Animation System Test
echo ====================================
echo.
echo This test demonstrates the fixed animation timing:
echo.
echo OLD SYSTEM: Each pose = 1 frame at 4 FPS = 0.25 seconds (TOO FAST!)
echo NEW SYSTEM: Each pose = 2 seconds by default (PERFECT!)
echo.
echo What you'll see:
echo - celebration_v2: 6 poses × 2 seconds = 12 seconds total
echo - quick_tour: 5 poses × 1 second = 5 seconds total
echo.
echo Each pose will be clearly visible for the full duration!
echo.
echo IMPORTANT: You need to restart the avatar display for the new timing!
echo 1. Run stop_all.bat
echo 2. Run start_all.bat
echo 3. Then run this test
echo.
pause

cd /d "%~dp0"
node test-pose-based-animation.js

echo.
echo Test complete! Each pose should have been clearly visible!
pause
