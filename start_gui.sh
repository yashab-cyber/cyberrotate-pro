#!/bin/bash

# CyberRotate Pro Enterprise GUI Launcher Script
# Compatible with Linux and macOS
# Supports multiple interface options

echo "CyberRotate Pro Enterprise - Interface Launcher"
echo "==============================================="
echo "Select an interface to launch:"
echo "1. Standard GUI (Traditional Interface)"
echo "2. Web Dashboard (Browser-based)"
echo "3. Analytics Dashboard (Advanced Analytics)"
echo "4. Enhanced CLI (Pro Command Line)"
echo "5. Interactive Mode (Terminal-based)"
echo "6. API Server (Background Service)"
echo ""
read -p "Enter your choice (1-6): " choice
echo

# Check if Python is available
if ! command -v python &> /dev/null && ! command -v python3 &> /dev/null; then
    echo "Error: Python is not installed or not in PATH"
    echo "Please install Python 3.8+ and try again"
    exit 1
fi

# Determine Python command
if command -v python3 &> /dev/null; then
    PYTHON_CMD="python3"
else
    PYTHON_CMD="python"
fi

# Change to script directory
cd "$(dirname "$0")"

# Check if virtual environment exists
if [ -d "venv" ]; then
    echo "Activating virtual environment..."
    source venv/bin/activate
fi

# Launch based on user choice
case $choice in
    1)
        echo "Launching Standard GUI..."
        $PYTHON_CMD ip_rotator.py --gui
        ;;
    2)
        echo "Launching Web Dashboard..."
        $PYTHON_CMD ip_rotator.py --web-dashboard
        ;;
    3)
        echo "Launching Analytics Dashboard..."
        $PYTHON_CMD ip_rotator.py --dashboard
        ;;
    4)
        echo "Launching Enhanced CLI..."
        $PYTHON_CMD ip_rotator.py --cli-pro
        ;;
    5)
        echo "Launching Interactive Mode..."
        $PYTHON_CMD ip_rotator.py --interactive
        ;;
    6)
        echo "Starting API Server..."
        $PYTHON_CMD ip_rotator.py --api-server
        ;;
    *)
        echo "Invalid choice. Launching Standard GUI..."
        $PYTHON_CMD ip_rotator.py --gui
        ;;
esac

# Check exit code
if [ $? -ne 0 ]; then
    echo
    echo "An error occurred while starting the GUI."
    echo "Check the error messages above for details."
    echo
    read -p "Press Enter to continue..."
fi
