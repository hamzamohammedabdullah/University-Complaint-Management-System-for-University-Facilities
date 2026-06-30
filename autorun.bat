@echo off
setlocal
cd /d "%~dp0"
set "PORT=8000"

where python >nul 2>nul
if errorlevel 1 (
  echo Python 3 was not found on this machine.
  echo Please install Python 3.12 or newer, then run this file again.
  pause
  exit /b 1
)

if not exist ".venv\Scripts\python.exe" (
  echo Creating virtual environment...
  python -m venv .venv
)

call .venv\Scripts\activate

echo Upgrading pip...
python -m pip install --upgrade pip

echo Installing dependencies...
python -m pip install -r requirements.txt

echo Applying database migrations...
python manage.py migrate

echo Running system checks...
python manage.py check
if errorlevel 1 (
  echo System checks failed. Please fix the issues before starting the app.
  pause
  exit /b 1
)

echo Starting the complaint management system...
start "UBIDS Complaint System" http://127.0.0.1:%PORT%
python manage.py runserver 127.0.0.1:%PORT%
