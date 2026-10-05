@echo off
echo ==============================================
echo   AEC Attendance Tracker - Setup & APK Build
echo ==============================================
echo.

echo 1. Checking Python installation...
where python >nul 2>nul
if %errorlevel% neq 0 (
    echo Python not found! Please install Python from https://www.python.org/downloads/
    echo Make sure to check "Add Python to PATH" during installation.
    pause
    exit /b
)

echo Python is installed.
echo.
echo 2. Installing required Python packages (Flet, Requests, BeautifulSoup)...
pip install -r requirements.txt
if %errorlevel% neq 0 (
    echo Error installing dependencies.
    pause
    exit /b
)

echo.
echo ==============================================
echo   Select what you want to do:
echo   [1] Run the App locally on PC (Preview)
echo   [2] Build the Android APK (flet build apk)
echo ==============================================
set /p choice="Enter choice (1 or 2): "

if "%choice%"=="1" (
    echo Starting App on PC...
    python main.py
) else if "%choice%"=="2" (
    echo Building Android APK...
    flet build apk
    echo.
    echo If completed, your APK is in build\apk\
) else (
    echo Invalid choice.
)

pause
