# CyberRotate Pro - Python 3.13 Installation Guide

## For Python 3.13 Users

Python 3.13 introduced changes that make some older package versions incompatible. Follow this guide for a smooth installation.

### Option 1: Use Python 3.13 Compatible Requirements (Recommended)

```bash
# Install using Python 3.13 compatible requirements
pip install -r requirements-py313.txt
```

### Option 2: Manual Installation (If Option 1 fails)

```bash
# Install core dependencies first
pip install requests>=2.31.0 pysocks>=1.7.1 stem>=1.8.1 colorama>=0.4.6

# Install data processing (Python 3.13 compatible versions)
pip install pandas>=2.2.0 numpy>=1.26.0 matplotlib>=3.8.0

# Install remaining dependencies
pip install beautifulsoup4>=4.12.0 click>=8.1.0 rich>=13.7.0
pip install flask>=3.0.0 flask-cors>=4.0.0
pip install cryptography>=41.0.0 pyopenssl>=23.0.0
pip install pyyaml>=6.0.1 jsonschema>=4.19.0
```

### Option 3: Minimal Installation (Core Features Only)

If you encounter issues with optional dependencies, install only core features:

```bash
pip install -r requirements-minimal.txt
```

### Option 4: Development Environment

For development with all features:

```bash
# Create virtual environment
python -m venv cyberrotate_env

# Activate virtual environment
# Windows:
cyberrotate_env\Scripts\activate
# Linux/macOS:
source cyberrotate_env/bin/activate

# Install Python 3.13 compatible requirements
pip install -r requirements-py313.txt
```

## Troubleshooting Python 3.13 Issues

### Common Error: pandas 2.1.3 compilation failure
**Solution**: Use pandas>=2.2.0 (already specified in requirements-py313.txt)

### Common Error: numpy compatibility issues
**Solution**: Use numpy>=1.26.0 (already specified in requirements-py313.txt)

### Common Error: matplotlib build issues
**Solution**: Use matplotlib>=3.8.0 (already specified in requirements-py313.txt)

## Verification

After installation, verify everything works:

```bash
# Test basic functionality
python ip_rotator.py --help

# Test GUI (if GUI dependencies installed)
python gui_launcher.py
```

## Alternative Python Versions

If you continue to have issues with Python 3.13, consider using:
- Python 3.11 (recommended for stability)
- Python 3.12 (good compatibility)

## Getting Help

If you encounter issues:
1. Check that you're using the correct requirements file for your Python version
2. Ensure you have the latest pip: `pip install --upgrade pip`
3. Try creating a fresh virtual environment
4. Check the error messages for specific package conflicts

## GUI-Specific Notes

The GUI has been designed to work with minimal dependencies:
- **tkinter**: Included with Python (no additional installation needed)
- **matplotlib**: Optional for advanced charts (will degrade gracefully if missing)
- **Pillow**: Optional for system tray icons (will degrade gracefully if missing)
- **pystray**: Optional for system tray functionality (will degrade gracefully if missing)

The GUI will automatically detect available dependencies and enable/disable features accordingly.
