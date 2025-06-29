@echo off
title CyberRotate Pro Enterprise - Quick Start

echo ================================================================
echo   CyberRotate Pro Enterprise - Quick Start Script
echo   Created by Yashab Alam - Founder of ZehraSec
echo ================================================================
echo.

REM Check if we're in the right directory
if not exist "ip_rotator.py" (
    echo ERROR: Please run this script from the CyberRotate Pro directory
    pause
    exit /b 1
)

echo Choose your deployment mode:
echo 1. Development Mode (Local testing)
echo 2. Production Mode (Full deployment)
echo 3. Enterprise Demo (All features enabled)
echo 4. API Server Only
echo 5. Analytics Dashboard Only
echo.
set /p mode=Enter your choice (1-5): 

if "%mode%"=="1" (
    echo Starting Development Mode...
    echo Features enabled: Core rotation, GUI, basic monitoring
    python ip_rotator.py --interactive
) else if "%mode%"=="2" (
    echo Starting Production Deployment...
    echo For Windows production deployment, please use Docker or manual setup
    echo See PRODUCTION_GUIDE.md for details
    pause
) else if "%mode%"=="3" (
    echo Starting Enterprise Demo...
    echo This will start all enterprise features for demonstration.
    echo.
    echo Starting API server on port 8080...
    start "API Server" python ip_rotator.py --api-server
    
    timeout /t 3 /nobreak >nul
    echo Starting analytics dashboard on port 8050...
    start "Analytics Dashboard" python ip_rotator.py --dashboard
    
    timeout /t 3 /nobreak >nul
    echo Starting web dashboard on port 5000...
    start "Web Dashboard" python ip_rotator.py --web-dashboard
    
    echo.
    echo Enterprise demo started successfully!
    echo Access points:
    echo   - API Server: http://localhost:8080
    echo   - Analytics Dashboard: http://localhost:8050
    echo   - Web Dashboard: http://localhost:5000
    echo   - API Documentation: http://localhost:8080/docs
    echo.
    echo Close the terminal windows to stop the services
    pause
) else if "%mode%"=="4" (
    echo Starting API Server Only...
    python ip_rotator.py --api-server
) else if "%mode%"=="5" (
    echo Starting Analytics Dashboard Only...
    python ip_rotator.py --dashboard
) else (
    echo Invalid choice. Starting interactive mode...
    python ip_rotator.py --interactive
)

pause
