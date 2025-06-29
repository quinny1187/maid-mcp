@echo off
echo Installing Python dependencies for Maid Avatar...
echo.

pip install PyQt5 flask flask-cors requests

echo.
echo Done! Dependencies installed.
echo.
echo Next steps:
echo 1. Run copy_sprites.bat to copy the sprite images
echo 2. Run start_avatar.bat to start the avatar system
pause