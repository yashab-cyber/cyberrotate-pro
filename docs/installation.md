# CyberRotate Pro Installation Guide

## Overview
This guide will help you install and configure CyberRotate Pro on your system.

## System Requirements

### Minimum Requirements
- Python 3.8 or higher
- 512 MB RAM
- 100 MB free disk space
- Internet connection

### Recommended Requirements
- Python 3.9 or higher
- 2 GB RAM
- 500 MB free disk space
- High-speed internet connection

### Supported Operating Systems
- Windows 10/11
- macOS 10.15 or higher
- Ubuntu 18.04 or higher
- Debian 10 or higher
- CentOS 7/8
- Arch Linux

## Dependencies

### Required Software
1. **Python 3.8+**: Core runtime environment
2. **OpenVPN**: VPN functionality (optional but recommended)
3. **Tor**: Anonymity features (optional)

### Python Dependencies
All Python dependencies are automatically installed via pip. See `requirements.txt` for the complete list.

## Installation Methods

### Method 1: Automated Installation (Recommended)

#### Windows
```powershell
# Run PowerShell as Administrator
.\install.ps1
```

#### Linux/macOS
```bash
# Make the script executable
chmod +x install.sh

# Run the installation script
./install.sh
```

### Method 2: Manual Installation

#### Step 1: Clone or Download
Download the CyberRotate Pro package and extract it to your desired location.

#### Step 2: Install Python Dependencies
```bash
pip install -r requirements.txt
```

#### Step 3: Install System Dependencies

**Ubuntu/Debian:**
```bash
sudo apt update
sudo apt install openvpn tor
```

**CentOS/RHEL:**
```bash
sudo yum install openvpn tor
```

**macOS (with Homebrew):**
```bash
brew install openvpn tor
```

**Windows:**
1. Download and install OpenVPN from https://openvpn.net/
2. Download and install Tor Browser from https://www.torproject.org/

#### Step 4: Configure
```bash
# Copy and edit configuration files
cp config/config.json.example config/config.json
# Edit config/config.json with your settings
```

## Configuration

### Basic Configuration
Edit `config/config.json` to customize your settings:

```json
{
  "proxy": {
    "rotation_interval": 300,
    "max_failures": 3,
    "verify_ssl": true
  },
  "openvpn": {
    "config_dir": "config/openvpn",
    "timeout": 30,
    "retry_attempts": 3
  },
  "tor": {
    "socks_port": 9150,
    "control_port": 9151,
    "auto_start": false
  }
}
```

### Proxy Configuration
1. Add your proxy lists to `config/proxies/`
2. Supported formats: HTTP, HTTPS, SOCKS4, SOCKS5
3. One proxy per line: `ip:port` or `ip:port:username:password`

### VPN Configuration
1. Place your OpenVPN configuration files in `config/openvpn/`
2. Update `config/openvpn/servers.json` with your server details
3. Ensure authentication files are properly configured

### Tor Configuration
1. Install Tor Browser or standalone Tor
2. Configure control port access if needed
3. Set appropriate SOCKS proxy port

## First Run

### Command Line
```bash
# Basic usage
python ip_rotator.py --help

# Interactive mode
python ip_rotator.py --interactive

# Start with specific configuration
python ip_rotator.py --config custom_config.json
```

### Verification
```bash
# Check current IP
python ip_rotator.py --check-ip

# Test proxy rotation
python ip_rotator.py --rotate-proxy --check-ip

# Test VPN connection
python ip_rotator.py --connect-vpn us-east-1 --check-ip
```

## Troubleshooting

### Common Issues

#### Permission Errors
- **Linux/macOS**: Run with `sudo` for system-level network changes
- **Windows**: Run as Administrator

#### OpenVPN Connection Failures
1. Check configuration files in `config/openvpn/`
2. Verify authentication credentials
3. Ensure OpenVPN is installed and in PATH
4. Check firewall settings

#### Tor Connection Issues
1. Verify Tor is installed and running
2. Check control port configuration
3. Ensure SOCKS port is available

#### Proxy Connection Failures
1. Verify proxy lists are up-to-date
2. Check proxy authentication if required
3. Test individual proxies manually

### Log Files
Check log files for detailed error information:
- `logs/cyberrotate.log`: Main application log
- `logs/proxy.log`: Proxy-related logs
- `logs/vpn.log`: VPN connection logs
- `logs/tor.log`: Tor-related logs

### Getting Help
1. Check the FAQ section
2. Review log files for error details
3. Ensure all dependencies are properly installed
4. Verify configuration files are correct

## Security Considerations

### File Permissions
Ensure sensitive files have appropriate permissions:
```bash
# Restrict access to authentication files
chmod 600 config/openvpn/auth.txt
chmod 600 config/openvpn/*.key
```

### Network Security
1. Always verify your new IP after rotation
2. Regularly check for DNS leaks
3. Use HTTPS whenever possible
4. Monitor network traffic for anomalies

### Best Practices
1. Regularly update proxy lists
2. Rotate between different anonymity methods
3. Use strong authentication for VPN services
4. Keep logs secure and rotate them regularly

## Performance Optimization

### System Resources
- Monitor CPU and memory usage
- Adjust rotation intervals based on usage
- Use connection pooling for better performance

### Network Performance
- Choose servers closest to your location
- Use UDP for VPN when possible
- Configure appropriate timeouts

## Updates and Maintenance

### Updating CyberRotate Pro
```bash
# Backup your configuration
cp config/config.json config/config.json.backup

# Update the application
# (Replace with your update method)

# Restore configuration if needed
```

### Regular Maintenance
1. Update proxy lists weekly
2. Check VPN server availability
3. Monitor log file sizes
4. Test anonymity features regularly

## Next Steps
- Review the [User Guide](user_guide.md) for detailed usage instructions
- Check the [API Documentation](api_reference.md) for automation options
- Explore [Advanced Configuration](advanced_config.md) for power users
