# CyberRotate Pro User Guide

## Table of Contents
1. [Getting Started](#getting-started)
2. [Basic Usage](#basic-usage)
3. [Interactive Mode](#interactive-mode)
4. [Command Line Interface](#command-line-interface)
5. [Proxy Management](#proxy-management)
6. [VPN Operations](#vpn-operations)
7. [Tor Integration](#tor-integration)
8. [Security Features](#security-features)
9. [Automation](#automation)
10. [Troubleshooting](#troubleshooting)

## Getting Started

### First Launch
After installation, start CyberRotate Pro in interactive mode:

```bash
python ip_rotator.py --interactive
```

This will launch the main menu where you can access all features through a user-friendly interface.

### Quick Start
For immediate IP rotation using the default configuration:

```bash
# Rotate proxy and check new IP
python ip_rotator.py --rotate-proxy --check-ip
```

## Basic Usage

### Checking Your Current IP
```bash
# Basic IP check
python ip_rotator.py --check-ip

# Detailed IP information
python ip_rotator.py --check-ip --verbose
```

### Simple Proxy Rotation
```bash
# Rotate to next proxy
python ip_rotator.py --rotate-proxy

# Rotate and verify
python ip_rotator.py --rotate-proxy --check-ip
```

### Basic VPN Connection
```bash
# List available VPN servers
python ip_rotator.py --list-vpn-servers

# Connect to specific server
python ip_rotator.py --connect-vpn us-east-1

# Disconnect from VPN
python ip_rotator.py --disconnect-vpn
```

## Interactive Mode

The interactive mode provides a menu-driven interface for all features:

```
CyberRotate Pro - Interactive Menu
==================================
1. Check Current IP
2. Proxy Management
3. VPN Management
4. Tor Operations
5. Security Checks
6. Statistics
7. Configuration
8. Exit
```

### Navigation
- Use number keys to select options
- Press Enter to confirm selections
- Use 'q' or 'quit' to exit submenus
- Use 'h' or 'help' for context help

### Menu Sections

#### 1. Check Current IP
- View current public IP address
- Get geolocation information
- Check ISP details
- Verify anonymity status

#### 2. Proxy Management
- Rotate proxies manually
- View current proxy status
- Test proxy connections
- Manage proxy lists

#### 3. VPN Management
- Connect/disconnect VPN
- List available servers
- Check connection status
- Monitor VPN performance

#### 4. Tor Operations
- Start/stop Tor service
- Get new Tor identity
- Configure Tor settings
- Monitor Tor circuits

#### 5. Security Checks
- DNS leak detection
- WebRTC leak testing
- IP consistency verification
- Anonymity assessment

#### 6. Statistics
- View usage statistics
- Connection history
- Performance metrics
- Error logs

#### 7. Configuration
- Edit settings
- Manage profiles
- Update server lists
- Export/import configurations

## Command Line Interface

### Core Commands

#### IP Operations
```bash
# Check current IP with location
python ip_rotator.py --check-ip --location

# Check IP with full details
python ip_rotator.py --check-ip --verbose --json
```

#### Proxy Commands
```bash
# Rotate proxy
python ip_rotator.py --rotate-proxy

# Use specific proxy type
python ip_rotator.py --rotate-proxy --type socks5

# Test proxy connectivity
python ip_rotator.py --test-proxy --proxy 127.0.0.1:8080
```

#### VPN Commands
```bash
# List VPN servers
python ip_rotator.py --list-vpn-servers

# Connect to VPN
python ip_rotator.py --connect-vpn server-name

# Disconnect VPN
python ip_rotator.py --disconnect-vpn

# Auto-select best server
python ip_rotator.py --connect-vpn auto
```

#### Tor Commands
```bash
# Start Tor
python ip_rotator.py --start-tor

# Stop Tor
python ip_rotator.py --stop-tor

# New Tor identity
python ip_rotator.py --new-tor-identity
```

### Advanced Options

#### Configuration
```bash
# Use custom config file
python ip_rotator.py --config /path/to/config.json

# Override specific settings
python ip_rotator.py --proxy-timeout 30 --vpn-timeout 60
```

#### Output Formats
```bash
# JSON output
python ip_rotator.py --check-ip --json

# Quiet mode (minimal output)
python ip_rotator.py --rotate-proxy --quiet

# Verbose mode (detailed output)
python ip_rotator.py --check-ip --verbose
```

#### Automation
```bash
# Continuous rotation (every 5 minutes)
python ip_rotator.py --auto-rotate --interval 300

# Chain operations
python ip_rotator.py --rotate-proxy --connect-vpn auto --check-ip
```

## Proxy Management

### Proxy Types
CyberRotate Pro supports multiple proxy types:
- **HTTP**: Standard web proxies
- **HTTPS**: Encrypted web proxies
- **SOCKS4**: Basic SOCKS proxies
- **SOCKS5**: Advanced SOCKS proxies with authentication

### Adding Proxies
1. Add proxies to appropriate files in `config/proxies/`:
   - `http_proxies.txt`: HTTP/HTTPS proxies
   - `socks_proxies.txt`: SOCKS4/SOCKS5 proxies

2. Format: `ip:port` or `ip:port:username:password`

### Proxy Testing
```bash
# Test all proxies
python ip_rotator.py --test-all-proxies

# Test specific proxy
python ip_rotator.py --test-proxy --proxy 192.168.1.100:8080
```

### Proxy Rotation Strategies
- **Sequential**: Rotate through proxies in order
- **Random**: Select random proxy each time
- **Performance**: Use fastest responding proxies
- **Geographic**: Rotate by geographic location

## VPN Operations

### Server Selection
```bash
# List all servers with details
python ip_rotator.py --list-vpn-servers --detailed

# Show servers by region
python ip_rotator.py --list-vpn-servers --region us
```

### Connection Management
```bash
# Connect with specific protocol
python ip_rotator.py --connect-vpn server --protocol udp

# Connect with custom timeout
python ip_rotator.py --connect-vpn server --timeout 45

# Force reconnection
python ip_rotator.py --reconnect-vpn
```

### Server Health Monitoring
The system automatically monitors VPN server health:
- Ping response times
- Connection success rates
- Bandwidth measurements
- Geographic verification

## Tor Integration

### Basic Tor Operations
```bash
# Start Tor with custom SOCKS port
python ip_rotator.py --start-tor --socks-port 9050

# Check Tor status
python ip_rotator.py --tor-status

# Get circuit information
python ip_rotator.py --tor-circuits
```

### Advanced Tor Features
- **Circuit Management**: Control Tor circuit paths
- **Exit Node Selection**: Choose specific exit countries
- **Bridge Configuration**: Use Tor bridges for censorship circumvention
- **Hidden Service Support**: Connect to .onion services

### Tor Security
- Automatically manages Tor cookies and authentication
- Supports control port authentication
- Implements proper Tor shutdown procedures
- Monitors for Tor vulnerabilities

## Security Features

### Leak Detection

#### DNS Leak Testing
```bash
# Basic DNS leak test
python ip_rotator.py --check-dns-leaks

# Detailed DNS analysis
python ip_rotator.py --check-dns-leaks --verbose
```

#### WebRTC Leak Detection
```bash
# Check for WebRTC leaks
python ip_rotator.py --check-webrtc-leaks
```

#### IP Consistency Verification
```bash
# Verify IP consistency across services
python ip_rotator.py --verify-ip-consistency
```

### Security Profiles
Create security profiles for different use cases:
- **High Anonymity**: Maximum security with Tor + VPN
- **Balanced**: Good security with reasonable performance
- **Performance**: Optimized for speed with basic protection

### Kill Switch
Automatic network kill switch prevents data leaks:
- Monitors active connections
- Blocks traffic on VPN disconnection
- Maintains firewall rules
- Logs security events

## Automation

### Scheduled Rotation
```bash
# Auto-rotate every 10 minutes
python ip_rotator.py --auto-rotate --interval 600

# Rotate on schedule with specific methods
python ip_rotator.py --schedule "proxy:300,vpn:1800,tor:3600"
```

### API Integration
Start the REST API server for remote control:
```bash
# Start API server
python -m core.api_server --host 0.0.0.0 --port 8080
```

### Scripting Examples

#### Basic Rotation Script
```python
#!/usr/bin/env python3
import subprocess
import time

def rotate_ip():
    subprocess.run(['python', 'ip_rotator.py', '--rotate-proxy'])
    subprocess.run(['python', 'ip_rotator.py', '--check-ip'])

# Rotate every 5 minutes
while True:
    rotate_ip()
    time.sleep(300)
```

#### Advanced Automation
```python
#!/usr/bin/env python3
from core.proxy_manager import ProxyManager
from core.openvpn_manager import OpenVPNManager
import json

# Load configuration
with open('config/config.json', 'r') as f:
    config = json.load(f)

# Initialize managers
proxy_mgr = ProxyManager(config['proxy'])
vpn_mgr = OpenVPNManager(config['openvpn'])

# Implement custom rotation logic
def smart_rotate():
    # Check current anonymity level
    # Rotate based on security requirements
    pass
```

## Troubleshooting

### Common Issues

#### "No proxies available"
1. Check proxy list files in `config/proxies/`
2. Verify proxy format is correct
3. Test individual proxies manually
4. Update proxy lists from fresh sources

#### "VPN connection failed"
1. Verify OpenVPN is installed
2. Check configuration files
3. Confirm authentication credentials
4. Test network connectivity

#### "Tor connection timeout"
1. Ensure Tor is properly installed
2. Check firewall settings
3. Verify control port configuration
4. Try different Tor bridges

### Debug Mode
Enable debug mode for detailed troubleshooting:
```bash
python ip_rotator.py --debug --verbose
```

### Log Analysis
Check log files for detailed error information:
```bash
# View recent logs
tail -f logs/cyberrotate.log

# Search for specific errors
grep "ERROR" logs/*.log
```

### Performance Issues
- Reduce rotation frequency
- Use faster proxy sources
- Choose geographically closer servers
- Optimize system resources

## Best Practices

### Security
1. Regularly verify your anonymity
2. Use multiple anonymity layers
3. Monitor for data leaks
4. Keep software updated

### Performance
1. Choose quality proxy sources
2. Monitor connection speeds
3. Use appropriate rotation intervals
4. Implement connection pooling

### Operational
1. Maintain current proxy lists
2. Monitor server availability
3. Backup configurations regularly
4. Document your workflows

## Advanced Tips

### Custom Scripts
Create custom scripts for specific workflows:
- Automated testing routines
- Geographic IP targeting
- Performance benchmarking
- Security auditing

### Integration
Integrate with other tools:
- Web browsers via proxy settings
- Custom applications via SOCKS
- Network analysis tools
- Security scanners

### Monitoring
Set up monitoring for:
- Connection failures
- Performance degradation
- Security breaches
- Resource usage

---

For more advanced configuration options, see the [Advanced Configuration Guide](advanced_config.md).
For API integration, see the [API Reference](api_reference.md).
