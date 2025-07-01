@echo off
echo ========================================
echo   Quick Sensitivity Adjustment
echo ========================================
echo.
echo Current energy_threshold: 8000 (Less sensitive - needs louder voice)
echo.
echo Choose a new sensitivity level:
echo.
echo 1. Very Sensitive (2000) - Picks up whispers
echo 2. Sensitive (4000) - Normal quiet room
echo 3. Moderate (6000) - Average room
echo 4. Less Sensitive (8000) - Current setting
echo 5. Very Insensitive (10000) - Noisy environment
echo 6. Custom value
echo.
set /p choice="Enter your choice (1-6): "

if "%choice%"=="1" set threshold=2000
if "%choice%"=="2" set threshold=4000
if "%choice%"=="3" set threshold=6000
if "%choice%"=="4" set threshold=8000
if "%choice%"=="5" set threshold=10000
if "%choice%"=="6" (
    set /p threshold="Enter custom threshold value: "
)

echo.
echo Setting energy_threshold to %threshold%...

:: Update the config file
cd voice\incoming
python -c "import configparser; c=configparser.ConfigParser(); c.read('voice_config.ini'); c['recognition']['energy_threshold']='%threshold%'; f=open('voice_config.ini','w'); c.write(f); f.close()"
cd ..\..

echo.
echo ✓ Sensitivity updated to %threshold%
echo.
echo Please restart the voice input system for changes to take effect.
echo.
pause
