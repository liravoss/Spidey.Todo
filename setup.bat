@echo off
:: ─────────────────────────────────────────────
::  SPIDEY TODO — setup.bat
::  Run this once on Windows to create a virtual
::  environment and install all dependencies.
::
::  Usage:  Double-click setup.bat
::          or run in Command Prompt / PowerShell
:: ─────────────────────────────────────────────

echo.
echo  SPIDEY TODO - Environment Setup
echo  ---------------------------------

:: ── Step 1: Create virtual environment ──
IF EXIST "venv\" (
  echo  [OK] Virtual environment already exists
) ELSE (
  echo  [..] Creating virtual environment...
  python -m venv venv
  echo  [OK] Virtual environment created at venv\
)

:: ── Step 2: Activate ──
echo  [..] Activating virtual environment...
call venv\Scripts\activate.bat

:: ── Step 3: Upgrade pip ──
echo  [..] Upgrading pip...
pip install --upgrade pip --quiet

:: ── Step 4: Install dependencies ──
echo  [..] Installing dependencies...
pip install -r requirements.txt --quiet

echo.
echo  Setup complete!
echo.
echo  ---------------------------------
echo  To activate the environment:
echo    venv\Scripts\activate
echo.
echo  To start the server:
echo    python server.py
echo.
echo  To import a file:
echo    python import.py yourfile.txt
echo.
echo  To deactivate when done:
echo    deactivate
echo  ---------------------------------
echo.
pause
