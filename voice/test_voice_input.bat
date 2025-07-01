@echo off
echo ========================================
echo   Test Speech Recognition
echo ========================================
echo.
echo This will test if your microphone and speech recognition work
echo without sending anything to Claude.
echo.

cd voice\incoming
python test_recognition.py

cd ..\..
