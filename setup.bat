@echo off
rem One-time setup: make a virtual environment and install the dependencies.
cd /d "%~dp0"
if not exist .venv (
  py -3 -m venv .venv || python -m venv .venv
)
.venv\Scripts\python -m pip install --upgrade pip >nul
.venv\Scripts\python -m pip install -r requirements.txt
echo.
echo Done. Activate with:  .venv\Scripts\activate
pause
