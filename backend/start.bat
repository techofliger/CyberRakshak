@echo off
cd /d "%~dp0"

echo Starting CyberRakshak...
echo.

call "%~dp0venv\Scripts\activate.bat"

python -m uvicorn main:app --reload

pause