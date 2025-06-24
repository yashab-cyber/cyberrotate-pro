# Installation Guide

This guide covers the installation of CyberRotate Pro on Windows, Linux, and macOS.

## 📋 Prerequisites

### System Requirements
- **Operating System**: Windows 10/11, Linux (Ubuntu 18+), macOS 10.14+
- **Python**: 3.8 or higher (Python 3.9+ recommended)
- **Memory**: 512MB RAM minimum, 1GB recommended
- **Storage**: 100MB free disk space
- **Network**: Active internet connection

### Required Software
- Python 3.8+ with pip
- Git (optional, for development)

## 🚀 Installation Methods

### Method 1: Automated Installation (Recommended)

#### Windows
```powershell
# Download and run the installer
curl -O https://github.com/ZehraSec/cyberrotate-pro/releases/latest/install.ps1
powershell -ExecutionPolicy Bypass -File install.ps1
```

#### Linux/macOS
```bash
# Download and run the installer
curl -sSL https://github.com/ZehraSec/cyberrotate-pro/releases/latest/install.sh | bash
```

### Method 2: Manual Installation

#### Step 1: Download CyberRotate Pro
```bash
# Clone from GitHub
git clone https://github.com/ZehraSec/cyberrotate-pro.git
cd cyberrotate-pro

# Or download ZIP and extract
```

#### Step 2: Install Python Dependencies
```bash
# Install required packages
pip install -r requirements.txt

# Install optional packages for GUI features
pip install -r requirements-optional.txt
```

#### Step 3: Run Initial Setup
```bash
# Run setup script
python setup.py install

# Or for development
python setup.py develop
```

### Method 3: Docker Installation
```bash
# Pull the Docker image
docker pull zehrasec/cyberrotate-pro:latest

# Run the container
docker run -d --name cyberrotate-pro \
  -p 8080:8080 \
  -v $(pwd)/config:/app/config \
  zehrasec/cyberrotate-pro:latest
```

## 🔧 Platform-Specific Instructions

### Windows Installation

#### Prerequisites
1. Install Python 3.9+ from [python.org](https://www.python.org/downloads/)
2. Ensure Python is added to PATH during installation
3. Install Visual C++ Build Tools (for some dependencies)

#### Installation Steps
```powershell
# Open PowerShell as Administrator
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser

# Install Python packages
pip install --upgrade pip
pip install -r requirements.txt

# Install optional GUI dependencies
pip install matplotlib numpy pillow pystray

# Run CyberRotate Pro
python ip_rotator.py --help
```

#### GUI Installation on Windows
```powershell
# Install GUI dependencies
pip install tkinter-tooltip
pip install customtkinter

# Launch GUI
python ip_rotator.py --gui
```

### Linux Installation (Ubuntu/Debian)

#### Prerequisites
```bash
# Update package list
sudo apt update

# Install Python and dependencies
sudo apt install python3 python3-pip python3-venv python3-dev
sudo apt install build-essential libssl-dev libffi-dev

# Install system dependencies for GUI
sudo apt install python3-tk python3-pil python3-pil.imagetk

# Install network tools (optional)
sudo apt install openvpn tor proxychains4
```

#### Installation Steps
```bash
# Create virtual environment (recommended)
python3 -m venv cyberrotate-env
source cyberrotate-env/bin/activate

# Install CyberRotate Pro
pip install --upgrade pip
pip install -r requirements.txt

# Install optional dependencies
pip install -r requirements-optional.txt

# Test installation
python ip_rotator.py --test
```

### macOS Installation

#### Prerequisites
```bash
# Install Homebrew (if not installed)
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Install Python
brew install python@3.9

# Install system dependencies
brew install openvpn tor
```

#### Installation Steps
```bash
# Create virtual environment
python3 -m venv cyberrotate-env
source cyberrotate-env/bin/activate

# Install CyberRotate Pro
pip install --upgrade pip
pip install -r requirements.txt

# Install GUI dependencies
pip install matplotlib numpy pillow

# Test installation
python ip_rotator.py --version
```

## ⚙️ Post-Installation Setup

### 1. Initial Configuration
```bash
# Run initial setup
python ip_rotator.py --setup

# Create sample configuration
python ip_rotator.py --create-config
```

### 2. Verify Installation
```bash
# Test basic functionality
python ip_rotator.py --test

# Check dependencies
python ip_rotator.py --check-deps

# Test network connectivity
python ip_rotator.py --check-connection
```

### 3. Configuration Files
CyberRotate Pro will create these configuration files:
- `config/config.json` - Main configuration
- `config/proxies/` - Proxy lists
- `config/openvpn/` - VPN configurations
- `logs/` - Log files

## 🔌 Optional Dependencies

### GUI Features
```bash
# For advanced GUI features
pip install matplotlib numpy

# For system tray support
pip install pystray pillow

# For modern themes
pip install customtkinter
```

### Network Tools
```bash
# For enhanced network monitoring
pip install netifaces psutil

# For advanced proxy testing
pip install requests[socks] PySocks

# For Tor integration
pip install stem
```

### Development Tools
```bash
# For development and testing
pip install pytest pytest-cov black flake8

# For documentation
pip install sphinx sphinx-rtd-theme
```

## 🚀 Quick Test

After installation, test CyberRotate Pro:

```bash
# Test CLI
python ip_rotator.py --help

# Test GUI (if installed)
python ip_rotator.py --gui

# Test network connection
python ip_rotator.py --test-connection

# Check current IP
python ip_rotator.py --check-ip
```

## 🔧 Troubleshooting Installation

### Common Issues

#### Python Version Issues
```bash
# Check Python version
python --version
python3 --version

# Use specific Python version
python3.9 -m pip install -r requirements.txt
```

#### Permission Issues (Linux/macOS)
```bash
# Use virtual environment (recommended)
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Or install with --user flag
pip install --user -r requirements.txt
```

#### Windows SSL Issues
```powershell
# Upgrade pip and certificates
python -m pip install --upgrade pip certifi

# Install with trusted hosts
pip install --trusted-host pypi.org --trusted-host pypi.python.org -r requirements.txt
```

#### GUI Dependencies Issues
```bash
# Linux: Install tkinter
sudo apt install python3-tk

# macOS: Reinstall Python with tkinter
brew reinstall python-tk

# Windows: Reinstall Python with tkinter option
```

### Getting Help
- Check [Troubleshooting Guide](11-troubleshooting.md)
- View logs in `logs/` directory
- Run with debug mode: `python ip_rotator.py --debug`
- Report issues on GitHub

## 📱 Mobile & Remote Access

### Web Interface
```bash
# Start web interface
python ip_rotator.py --web --port 8080

# Access from browser
# http://localhost:8080
```

### Remote Management
```bash
# Enable API server
python ip_rotator.py --api --host 0.0.0.0 --port 8080

# Secure with authentication
python ip_rotator.py --api --auth-token YOUR_SECRET_TOKEN
```

## 🔄 Updating CyberRotate Pro

### Automatic Update
```bash
# Check for updates
python ip_rotator.py --check-updates

# Update to latest version
python ip_rotator.py --update
```

### Manual Update
```bash
# Git update
git pull origin main
pip install -r requirements.txt

# Or download new version and reinstall
```

## ✅ Installation Complete

Your CyberRotate Pro installation is now complete! 

**Next Steps:**
1. Read the [Quick Start Guide](02-quick-start.md)
2. Configure your settings in [Configuration Guide](03-configuration.md)
3. Start using the [GUI](04-gui-guide.md) or [CLI](05-cli-guide.md)

---

**Need Help?** Check the [FAQ](13-faq.md) or [Support Guide](14-support.md)
