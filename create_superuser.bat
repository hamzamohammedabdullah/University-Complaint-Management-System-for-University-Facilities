@echo off
setlocal
cd /d "%~dp0"
if not exist ".venv\Scripts\python.exe" (
  echo Virtual environment not found.
  echo Run autorun.bat first to set up the environment.
  pause
  exit /b 1
)

call .venv\Scripts\activate
python manage.py createsuperuser
pause
