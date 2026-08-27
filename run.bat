@echo off
setlocal
cd /d "%~dp0"

where py >nul 2>nul
if %errorlevel% equ 0 (
  start "Library App" cmd /k py -3 app.py
  timeout /t 3 /nobreak >nul
  start http://127.0.0.1:5000/
  goto :eof
)

where python >nul 2>nul
if %errorlevel% equ 0 (
  start "Library App" cmd /k python app.py
  timeout /t 3 /nobreak >nul
  start http://127.0.0.1:5000/
  goto :eof
)

echo Python was not found on this computer.
echo Install Python 3 and make sure "Add Python to PATH" is enabled.
pause
