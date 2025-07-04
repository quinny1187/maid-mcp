@echo off
echo Installing Giphy MCP Server dependencies...
echo.

cd /d "%~dp0"

echo Installing npm packages...
npm install

echo.
echo Installation complete!
echo.
echo IMPORTANT: Before running the server, add your Giphy API key to .env file:
echo   GIPHY_API_KEY=your_actual_api_key_here
echo.
echo To get an API key:
echo   1. Go to https://developers.giphy.com/
echo   2. Create an account or sign in
echo   3. Create a new app
echo   4. Copy the API key
echo.
pause
