@echo off
echo ========================================
echo   Microphone Calibration Tool
echo ========================================
echo.
echo This will help you find the right sensitivity settings
echo for your microphone and environment.
echo.

cd voice\incoming
python calibrate_microphone.py

cd ..\..
