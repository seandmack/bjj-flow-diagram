@echo off
REM BJJ Flow Diagram Test Setup Script for Windows

echo.
echo BJJ Flow Diagram Test Setup
echo ================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python is not installed. Please install Python 3.8 or higher.
    echo Download from: https://www.python.org/downloads/
    pause
    exit /b 1
)

echo [OK] Python found

REM Create virtual environment
echo.
echo Creating virtual environment...
python -m venv venv

REM Activate virtual environment and install dependencies
echo.
echo Installing dependencies...
call venv\Scripts\activate.bat
python -m pip install --quiet --upgrade pip
pip install --quiet -r requirements.txt

REM Install Playwright browsers
echo.
echo Installing Playwright browsers...
playwright install chromium

REM Create test reports directory
echo.
echo Creating test reports directory...
if not exist test-reports mkdir test-reports
if not exist test-reports\screenshots mkdir test-reports\screenshots

echo.
echo [SUCCESS] Setup complete!
echo.
echo To run tests:
echo   1. Start the local server (in one terminal):
echo      python -m http.server 8000
echo.
echo   2. In another terminal, activate the virtual environment:
echo      venv\Scripts\activate
echo.
echo   3. Run the tests:
echo      pytest                    # Run all tests
echo      pytest -m smoke          # Run smoke tests only
echo      pytest test_counters.py  # Run counter tests only
echo.
echo   4. View the test report:
echo      start test-reports\report.html
echo.
pause
