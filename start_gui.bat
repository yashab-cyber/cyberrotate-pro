@echo off
title CyberRotate Pro - GUI Launcher

echo Starting CyberRotate Pro GUI...
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

REM Launch the GUI
python gui_launcher.py %*

REM Keep window open if there's an error
if errorlevel 1 (
    echo.
    echo An error occurred while starting the GUI.
    echo Check the error messages above for details.
    echo.
    pause
)
