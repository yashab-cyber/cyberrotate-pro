@echo off
title CyberRotate Pro Enterprise - Interface Launcher

echo CyberRotate Pro Enterprise - Interface Launcher
echo =================================================
echo Select an interface to launch:
echo 1. Standard GUI (Traditional Interface)
echo 2. Web Dashboard (Browser-based)
echo 3. Analytics Dashboard (Advanced Analytics)
echo 4. Enhanced CLI (Pro Command Line)
echo 5. Interactive Mode (Terminal-based)
echo 6. API Server (Background Service)
echo.
set /p choice=Enter your choice (1-6): 
echo.

REM Check if Python is available
python --version >nul 2>&1
if errorlevel 1 (
    echo Error: Python is not installed or not in PATH
    echo Please install Python 3.8+ from https://python.org
    echo.
    pause
    exit /b 1
)

REM Launch based on user choice
if "%choice%"=="1" (
    echo Launching Standard GUI...
    python ip_rotator.py --gui
) else if "%choice%"=="2" (
    echo Launching Web Dashboard...
    python ip_rotator.py --web-dashboard
) else if "%choice%"=="3" (
    echo Launching Analytics Dashboard...
    python ip_rotator.py --dashboard
) else if "%choice%"=="4" (
    echo Launching Enhanced CLI...
    python ip_rotator.py --cli-pro
) else if "%choice%"=="5" (
    echo Launching Interactive Mode...
    python ip_rotator.py --interactive
) else if "%choice%"=="6" (
    echo Starting API Server...
    python ip_rotator.py --api-server
) else (
    echo Invalid choice. Launching Standard GUI...
    python ip_rotator.py --gui
)

REM Keep window open if there's an error
if errorlevel 1 (
    echo.
    echo An error occurred while starting the interface.
    echo Check the error messages above for details.
    echo.
    pause
)
