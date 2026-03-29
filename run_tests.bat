@echo off
REM Windows batch script for running tests

echo ========================================
echo Condominium Agent - Test Suite
echo ========================================
echo.

REM Check if venv exists
if not exist "venv" (
    echo Creating virtual environment...
    python -m venv venv
)

REM Activate venv
call venv\Scripts\activate.bat

REM Install dependencies
echo Installing dependencies...
pip install -q -r requirements.txt

echo.
echo Running tests...
echo ========================================

REM Run pytest with coverage
pytest tests\ -v --cov=src --cov-report=html --cov-report=term-missing

echo.
echo ========================================
echo Test run complete!
echo Coverage report: htmlcov\index.html
echo ========================================
