@echo off
setlocal
cd /d "%~dp0"

where py >nul 2>nul
if errorlevel 1 (
  echo Python was not found. Install Python 3.11 or newer from python.org.
  pause
  exit /b 1
)

py -m venv .venv
call .venv\Scripts\activate.bat
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
python -m PyInstaller --noconfirm --clean LeoDesktopBuddy.spec

if errorlevel 1 (
  echo Build failed.
  pause
  exit /b 1
)

echo.
echo Done: dist\LeoDesktopBuddy.exe
pause

