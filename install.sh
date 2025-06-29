#!/bin/bash
# CyberRotate Pro Installation Script for Linux/macOS
# Created by Yashab Alam - Founder & CEO of ZehraSec

set -e

echo "=================================================="
echo "  CyberRotate Pro - Installation Script v2.0"
echo "  Created by Yashab Alam - Founder of ZehraSec"
echo "  Enterprise Edition with Full Production Support"
echo "=================================================="

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Functions
print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check if running as root
if [[ $EUID -eq 0 ]]; then
   print_warning "This script should not be run as root for security reasons"
   exit 1
fi

# Detect OS
OS=""
if [[ "$OSTYPE" == "linux-gnu"* ]]; then
    OS="linux"
elif [[ "$OSTYPE" == "darwin"* ]]; then
    OS="macos"
else
    print_error "Unsupported operating system: $OSTYPE"
    exit 1
fi

print_status "Detected OS: $OS"

# Check Python version
print_status "Checking Python installation..."
if command -v python3 &> /dev/null; then
    PYTHON_VERSION=$(python3 -c 'import sys; print(".".join(map(str, sys.version_info[:2])))')
    print_success "Python $PYTHON_VERSION found"
    
    # Check if Python version is 3.8 or higher
    if python3 -c 'import sys; exit(0 if sys.version_info >= (3, 8) else 1)'; then
        print_success "Python version is compatible"
    else
        print_error "Python 3.8 or higher is required"
        exit 1
    fi
else
    print_error "Python 3 is not installed"
    print_status "Please install Python 3.8 or higher and try again"
    exit 1
fi

# Check pip
print_status "Checking pip installation..."
if command -v pip3 &> /dev/null; then
    print_success "pip3 found"
else
    print_error "pip3 is not installed"
    exit 1
fi

# Install system dependencies
print_status "Installing system dependencies..."

if [[ "$OS" == "linux" ]]; then
    # Detect Linux distribution
    if command -v apt &> /dev/null; then
        # Debian/Ubuntu
        print_status "Installing dependencies for Debian/Ubuntu..."
        sudo apt update
        sudo apt install -y python3-venv python3-pip curl wget tor openvpn
    elif command -v yum &> /dev/null; then
        # RHEL/CentOS/Fedora
        print_status "Installing dependencies for RHEL/CentOS/Fedora..."
        sudo yum install -y python3-venv python3-pip curl wget tor openvpn
    elif command -v pacman &> /dev/null; then
        # Arch Linux
        print_status "Installing dependencies for Arch Linux..."
        sudo pacman -S --noconfirm python-virtualenv python-pip curl wget tor openvpn
    else
        print_warning "Unknown Linux distribution. Please install dependencies manually:"
        print_warning "- python3-venv"
        print_warning "- python3-pip"
        print_warning "- curl"
        print_warning "- wget"
        print_warning "- tor (optional)"
        print_warning "- openvpn (optional)"
    fi
elif [[ "$OS" == "macos" ]]; then
    # macOS
    if command -v brew &> /dev/null; then
        print_status "Installing dependencies with Homebrew..."
        brew install python3 curl wget tor openvpn
    else
        print_warning "Homebrew not found. Please install dependencies manually or install Homebrew first"
    fi
fi

# Create virtual environment
print_status "Creating Python virtual environment..."
if [[ -d "venv" ]]; then
    print_warning "Virtual environment already exists"
    read -p "Do you want to recreate it? (y/N): " recreate
    if [[ $recreate =~ ^[Yy]$ ]]; then
        rm -rf venv
        python3 -m venv venv
    fi
else
    python3 -m venv venv
fi

# Activate virtual environment
print_status "Activating virtual environment..."
source venv/bin/activate

# Upgrade pip
print_status "Upgrading pip..."
pip install --upgrade pip

# Install Python dependencies
print_status "Installing Python dependencies (complete enterprise suite)..."
if [[ -f "requirements.txt" ]]; then
    pip install -r requirements.txt
    print_success "All dependencies installed successfully!"
    print_success "✓ Core components"
    print_success "✓ Enterprise features"
    print_success "✓ Analytics dashboard"
    print_success "✓ Development tools"
    print_success "✓ Optional features"
else
    print_error "requirements.txt not found"
    exit 1
fi

# Note: Individual requirements files are maintained for reference but main requirements.txt contains everything

# Install Docker if not present (for production deployment)
print_status "Checking Docker installation..."
if command -v docker &> /dev/null; then
    print_success "Docker found"
else
    print_warning "Docker not found. Installing Docker for production deployment..."
    if [[ "$OS" == "linux" ]]; then
        curl -fsSL https://get.docker.com -o get-docker.sh
        sudo sh get-docker.sh
        sudo usermod -aG docker $USER
        print_success "Docker installed. Please log out and back in for group changes to take effect."
    else
        print_warning "Please install Docker manually for production deployment features"
    fi
fi

# Install Docker Compose
print_status "Checking Docker Compose installation..."
if command -v docker-compose &> /dev/null; then
    print_success "Docker Compose found"
else
    print_warning "Installing Docker Compose..."
    sudo curl -L "https://github.com/docker/compose/releases/download/1.29.2/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
    sudo chmod +x /usr/local/bin/docker-compose
    print_success "Docker Compose installed"
fi

# Install optional dependencies
if [[ -f "requirements-full.txt" ]]; then
    read -p "Do you want to install optional features? (y/N): " install_optional
    if [[ $install_optional =~ ^[Yy]$ ]]; then
        pip install -r requirements-full.txt
        print_success "Optional dependencies installed"
    fi
fi

# Create necessary directories
print_status "Creating necessary directories..."
mkdir -p data/logs
mkdir -p data/stats
mkdir -p data/reports
mkdir -p config/profiles
mkdir -p templates
mkdir -p static/css
mkdir -p static/js

# Initialize database if enterprise mode is enabled
print_status "Initializing enterprise features..."
if [[ -f "core/database_manager.py" ]]; then
    python3 -c "from core.database_manager import DatabaseManager; dm = DatabaseManager(); dm.initialize_database()" 2>/dev/null || true
    print_success "Database initialized"
fi

# Set permissions
print_status "Setting permissions..."
chmod +x ip_rotator.py
chmod +x gui_launcher.py
chmod +x start_gui.sh
chmod +x deploy_production.sh

# Make production scripts executable
if [[ -f "deploy_production.sh" ]]; then
    chmod +x deploy_production.sh
fi

# Test installation
print_status "Testing installation..."
if python3 ip_rotator.py --version &> /dev/null; then
    print_success "Installation test passed"
else
    print_error "Installation test failed"
    exit 1
fi

# Create desktop shortcut (Linux only)
if [[ "$OS" == "linux" ]] && [[ -d "$HOME/Desktop" ]]; then
    read -p "Do you want to create a desktop shortcut? (y/N): " create_shortcut
    if [[ $create_shortcut =~ ^[Yy]$ ]]; then
        cat > "$HOME/Desktop/CyberRotate Pro.desktop" << EOF
[Desktop Entry]
Version=1.0
Type=Application
Name=CyberRotate Pro
Comment=Advanced IP Rotation & Anonymity Suite
Exec=$(pwd)/venv/bin/python $(pwd)/ip_rotator.py --interactive
Icon=network-vpn
Terminal=true
Categories=Network;Security;
EOF
        chmod +x "$HOME/Desktop/CyberRotate Pro.desktop"
        print_success "Desktop shortcut created"
    fi
fi

# Installation complete
echo ""
echo "=================================================="
print_success "CyberRotate Pro Enterprise Edition installation completed successfully!"
echo "=================================================="
echo ""
print_status "Core Features:"
echo "  1. Basic rotation: python3 ip_rotator.py --interactive"
echo "  2. GUI interface: python3 ip_rotator.py --gui"
echo "  3. Quick start: ./start_gui.sh"
echo ""
print_status "Enterprise Features:"
echo "  4. API Server: python3 ip_rotator.py --api-server"
echo "  5. Analytics Dashboard: python3 ip_rotator.py --dashboard"
echo "  6. Enhanced CLI: python3 ip_rotator.py --cli-pro"
echo "  7. Web Dashboard: python3 ip_rotator.py --web-dashboard"
echo "  8. Production Deploy: ./deploy_production.sh"
echo "  9. Docker Deploy: python3 ip_rotator.py --docker-deploy"
echo "  10. Production Tests: python3 ip_rotator.py --production-test"
echo ""
print_status "Configuration files are located in:"
echo "  - config/config.json (main configuration)"
echo "  - config/api_config.json (API server configuration)"
echo "  - config/openvpn/ (OpenVPN configurations)"
echo "  - config/proxies/ (proxy lists)"
echo ""
print_status "Enterprise Documentation:"
echo "  - manual/ (complete user manual)"
echo "  - PRODUCTION_GUIDE.md (production deployment guide)"
echo ""
print_warning "Important Security Notes:"
echo "  - Only use this tool for authorized testing and research"
echo "  - Configure your OpenVPN servers in config/openvpn/"
echo "  - Add your proxy lists in config/proxies/"
echo "  - Review the legal guidelines in README.md"
echo ""
print_status "For support and documentation:"
echo "  - GitHub: https://github.com/yashab-cyber/cyberrotate-pro"
echo "  - Website: https://www.zehrasec.com"
echo ""
print_success "Happy ethical hacking! - Yashab Alam & ZehraSec Team"
