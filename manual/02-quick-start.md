# Quick Start Guide

Get CyberRotate Pro up and running in just 5 minutes!

## 🏁 Prerequisites Check

Before starting, ensure you have:
- ✅ Python 3.8+ installed
- ✅ CyberRotate Pro downloaded/installed
- ✅ Internet connection active

## 🚀 5-Minute Quick Start

### Step 1: First Launch (30 seconds)
```bash
# Navigate to CyberRotate Pro directory
cd cyberrotate-pro

# Check if everything is working
python ip_rotator.py --version
```

Expected output:
```
CyberRotate Pro v1.0.0
Professional IP Rotation & Anonymity Suite
Created by Yashab Alam - ZehraSec
```

### Step 2: Initial Setup (1 minute)
```bash
# Run initial setup - creates default config files
python ip_rotator.py --setup

# Check your current IP (baseline)
python ip_rotator.py --check-ip
```

Expected output:
```
✅ Current IP: 203.0.113.45
📍 Location: New York, US
🌐 ISP: Your Internet Provider
```

### Step 3: Test Basic Functionality (1 minute)
```bash
# Test network connectivity
python ip_rotator.py --test

# Check available rotation methods
python ip_rotator.py --list-methods
```

### Step 4: First IP Rotation (2 minutes)

#### Option A: Use GUI (Easiest)
```bash
# Launch graphical interface
python ip_rotator.py --gui
```

In the GUI:
1. Click "Check IP" to see current IP
2. Click "Rotate Proxy" to change IP
3. Click "Check IP" again to verify change

#### Option B: Use CLI (Quick)
```bash
# Rotate using built-in proxy rotation
python ip_rotator.py --rotate --method proxy

# Check new IP
python ip_rotator.py --check-ip
```

### Step 5: Verify Success (30 seconds)
```bash
# Check rotation history
python ip_rotator.py --status

# View recent logs
python ip_rotator.py --logs --tail 10
```

## 🎯 Common First Tasks

### Task 1: Set Up Automatic Rotation
```bash
# Start automatic rotation every 5 minutes
python ip_rotator.py --auto-rotate --interval 300

# Run in background
python ip_rotator.py --auto-rotate --interval 300 --daemon
```

### Task 2: Add Your Proxy List
```bash
# Add proxies from file
python ip_rotator.py --add-proxies proxies.txt

# Test added proxies
python ip_rotator.py --test-proxies
```

### Task 3: Enable Tor (if available)
```bash
# Start Tor service
python ip_rotator.py --tor start

# Rotate Tor identity
python ip_rotator.py --tor new-identity

# Check Tor IP
python ip_rotator.py --check-ip --method tor
```

## 🖥️ GUI Quick Tour

### Launching the GUI
```bash
# Standard GUI
python ip_rotator.py --gui

# Advanced GUI with all features
python ip_rotator.py --gui --advanced
```

### GUI Main Areas
1. **Control Panel** (Left): IP status, proxy controls, VPN settings
2. **Status Panel** (Center): Current connection status and network info
3. **Information Panel** (Right): Logs, statistics, and settings

### Essential GUI Actions
- **Check Current IP**: Click "Check IP" button
- **Rotate IP**: Click "Rotate Proxy" or "Quick Rotate"
- **Monitor Status**: Watch the colored indicators (🔴/🟢)
- **View Logs**: Switch to "Logs" tab

## 📱 CLI Quick Reference

### Basic Commands
```bash
# Show help
python ip_rotator.py --help

# Check current status
python ip_rotator.py --status

# Start interactive mode
python ip_rotator.py --interactive
```

### IP Operations
```bash
# Check current IP
python ip_rotator.py --check-ip

# Rotate IP using best available method
python ip_rotator.py --rotate

# Rotate using specific method
python ip_rotator.py --rotate --method [proxy|tor|vpn]
```

### Monitoring
```bash
# Show live status
python ip_rotator.py --monitor

# View logs
python ip_rotator.py --logs

# Test connection
python ip_rotator.py --test
```

## 🔧 Configuration Essentials

### Default Configuration Location
- **Windows**: `C:\Users\[Username]\cyberrotate\config\`
- **Linux/macOS**: `~/.cyberrotate/config/` or `./config/`

### Key Configuration Files
- `config.json` - Main settings
- `proxies/proxies.txt` - Proxy list
- `openvpn/` - VPN configurations

### Quick Configuration Changes
```bash
# Set rotation interval to 10 minutes
python ip_rotator.py --config set rotation_interval 600

# Enable DNS leak protection
python ip_rotator.py --config set dns_leak_protection true

# Set default rotation method
python ip_rotator.py --config set default_method proxy
```

## 🛡️ Security Quick Setup

### Enable Basic Security Features
```bash
# Enable all security features
python ip_rotator.py --security enable-all

# Test for DNS leaks
python ip_rotator.py --security dns-leak-test

# Check for IP leaks
python ip_rotator.py --security leak-test
```

### Security Recommendations
1. **Always test**: Run leak tests after setup
2. **Monitor logs**: Check for security warnings
3. **Regular updates**: Keep CyberRotate Pro updated
4. **Backup config**: Save your working configuration

## 🔍 Troubleshooting Quick Fixes

### Common Issues & Solutions

#### "No proxies available"
```bash
# Add sample proxies
python ip_rotator.py --add-sample-proxies

# Or add your own
python ip_rotator.py --add-proxies your-proxy-list.txt
```

#### "Connection failed"
```bash
# Test connectivity
python ip_rotator.py --test --verbose

# Check logs for errors
python ip_rotator.py --logs --level error
```

#### GUI won't start
```bash
# Install GUI dependencies
pip install tkinter matplotlib

# Try basic GUI
python ip_rotator.py --gui --basic
```

#### Permission errors (Linux/macOS)
```bash
# Use virtual environment
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## 📈 Performance Optimization

### Quick Performance Tips
```bash
# Enable fast rotation mode
python ip_rotator.py --config set fast_mode true

# Increase connection timeout
python ip_rotator.py --config set timeout 30

# Enable connection pooling
python ip_rotator.py --config set connection_pooling true
```

## 🎯 Next Steps

Now that you have CyberRotate Pro running:

1. **Explore Features**: Try different rotation methods
2. **Customize Settings**: Read [Configuration Guide](03-configuration.md)
3. **Add Resources**: Set up VPN and proxy lists
4. **Security**: Enable all security features
5. **Automation**: Set up scheduled rotations

### Recommended Reading Order
1. [Configuration Guide](03-configuration.md) - Customize your setup
2. [GUI User Guide](04-gui-guide.md) - Master the interface
3. [Security Features](10-security.md) - Enhance protection
4. [Troubleshooting](11-troubleshooting.md) - Solve issues

## 🆘 Getting Help

If you encounter issues:
1. Check the [FAQ](13-faq.md)
2. Review [Troubleshooting Guide](11-troubleshooting.md)
3. Enable debug mode: `python ip_rotator.py --debug`
4. Check logs: `python ip_rotator.py --logs`
5. Visit [Support](14-support.md) for assistance

## ✅ Quick Start Complete!

Congratulations! You've successfully set up CyberRotate Pro. You should now be able to:
- ✅ Check your current IP address
- ✅ Rotate your IP using available methods
- ✅ Monitor connection status
- ✅ Access both GUI and CLI interfaces

**Happy rotating! 🔄**

---

**Need more help?** The complete manual sections are available in this folder, starting with [Configuration Guide](03-configuration.md).
