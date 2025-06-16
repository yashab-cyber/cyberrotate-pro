#!/bin/bash

# CyberRotate Pro GUI Launcher Script
# Compatible with Linux and macOS

echo "CyberRotate Pro - GUI Launcher"
echo "=============================="
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

echo "Using Python: $PYTHON_CMD"
echo

# Change to script directory
cd "$(dirname "$0")"

# Check if virtual environment exists
if [ -d "venv" ]; then
    echo "Activating virtual environment..."
    source venv/bin/activate
fi

# Launch the GUI
echo "Starting CyberRotate Pro GUI..."
$PYTHON_CMD gui_launcher.py "$@"

# Check exit code
if [ $? -ne 0 ]; then
    echo
    echo "An error occurred while starting the GUI."
    echo "Check the error messages above for details."
    echo
    read -p "Press Enter to continue..."
fi
