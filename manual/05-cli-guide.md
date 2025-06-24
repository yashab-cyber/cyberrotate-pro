# CLI User Guide

The CyberRotate Pro command-line interface provides powerful automation capabilities and scriptable access to all features.

## 🖥️ Command Line Basics

### Main Command Syntax
```bash
python ip_rotator.py [COMMAND] [OPTIONS] [ARGUMENTS]
```

### Global Options
```bash
--help, -h          Show help message
--version, -v       Show version information
--config, -c FILE   Use specific config file
--verbose, -V       Enable verbose output
--quiet, -q         Suppress output
--debug, -d         Enable debug mode
--log-file FILE     Write logs to file
```

## 🚀 Core Commands

### Connection Management

#### connect
Establish VPN or proxy connection:
```bash
# Connect with default settings
python ip_rotator.py connect

# Connect to specific VPN server
python ip_rotator.py connect --vpn --server "us-west-1"

# Connect using proxy
python ip_rotator.py connect --proxy --proxy-type http

# Connect with Tor
python ip_rotator.py connect --tor
```

**Options:**
- `--vpn`: Use VPN connection
- `--proxy`: Use proxy connection
- `--tor`: Use Tor network
- `--server NAME`: Specific server name
- `--country CODE`: Country code (US, UK, etc.)
- `--protocol PROTO`: Connection protocol
- `--timeout SECONDS`: Connection timeout

#### disconnect
Terminate active connections:
```bash
# Disconnect all
python ip_rotator.py disconnect

# Disconnect specific service
python ip_rotator.py disconnect --vpn
python ip_rotator.py disconnect --proxy
python ip_rotator.py disconnect --tor
```

#### status
Check connection status:
```bash
# Show all status
python ip_rotator.py status

# Show specific service status
python ip_rotator.py status --vpn
python ip_rotator.py status --detailed
```

### IP Rotation

#### rotate
Change IP address:
```bash
# Basic rotation
python ip_rotator.py rotate

# Rotate VPN server
python ip_rotator.py rotate --vpn

# Rotate proxy
python ip_rotator.py rotate --proxy

# Force rotation (ignore timing)
python ip_rotator.py rotate --force
```

#### auto-rotate
Start automatic rotation:
```bash
# Auto-rotate every 5 minutes
python ip_rotator.py auto-rotate --interval 5m

# Auto-rotate with specific method
python ip_rotator.py auto-rotate --method vpn --interval 10m

# Stop auto-rotation
python ip_rotator.py auto-rotate --stop
```

**Interval formats:**
- `30s` - 30 seconds
- `5m` - 5 minutes
- `2h` - 2 hours

### Configuration

#### config
Manage configuration:
```bash
# Show current configuration
python ip_rotator.py config show

# Set configuration value
python ip_rotator.py config set vpn.provider nordvpn
python ip_rotator.py config set proxy.rotation_interval 300

# Reset to defaults
python ip_rotator.py config reset

# Import configuration
python ip_rotator.py config import config.json

# Export configuration
python ip_rotator.py config export backup.json
```

### VPN Management

#### vpn
VPN-specific commands:
```bash
# List available servers
python ip_rotator.py vpn list-servers

# List by country
python ip_rotator.py vpn list-servers --country US

# Test server connection
python ip_rotator.py vpn test-server us-west-1

# Get current VPN info
python ip_rotator.py vpn info

# Import VPN config
python ip_rotator.py vpn import-config config.ovpn
```

### Proxy Management

#### proxy
Proxy-specific commands:
```bash
# List configured proxies
python ip_rotator.py proxy list

# Add new proxy
python ip_rotator.py proxy add --host 1.2.3.4 --port 8080 --type http

# Test proxy
python ip_rotator.py proxy test 1.2.3.4:8080

# Import proxy list
python ip_rotator.py proxy import proxies.txt

# Remove dead proxies
python ip_rotator.py proxy cleanup
```

### Tor Management

#### tor
Tor-specific commands:
```bash
# Start Tor service
python ip_rotator.py tor start

# Get new circuit
python ip_rotator.py tor new-circuit

# Check Tor status
python ip_rotator.py tor status

# Configure bridges
python ip_rotator.py tor set-bridges bridge.txt
```

## 🔧 Advanced Usage

### Batch Operations

#### Multiple commands
```bash
# Chain commands with &&
python ip_rotator.py connect --vpn && python ip_rotator.py status

# Use JSON output for scripting
python ip_rotator.py status --json | jq '.ip_address'
```

#### Script integration
```bash
#!/bin/bash
# Auto-rotation script
python ip_rotator.py connect --vpn
python ip_rotator.py auto-rotate --interval 10m
echo "Started auto-rotation"
```

### Configuration Files

#### Custom config files
```bash
# Use specific config
python ip_rotator.py --config ~/my-config.json connect

# Environment-specific configs
python ip_rotator.py --config configs/production.json status
```

#### Config file format (JSON):
```json
{
    "vpn": {
        "provider": "nordvpn",
        "protocol": "openvpn",
        "auto_connect": true,
        "preferred_countries": ["US", "UK", "DE"]
    },
    "proxy": {
        "rotation_interval": 300,
        "test_before_use": true,
        "max_failures": 3
    },
    "security": {
        "dns_leak_protection": true,
        "kill_switch": true,
        "ipv6_disable": true
    }
}
```

### Automation and Scheduling

#### Cron integration (Linux/macOS)
```bash
# Add to crontab for daily rotation
0 9 * * * cd /path/to/cyberrotate && python ip_rotator.py rotate --vpn

# Hourly IP check
0 * * * * cd /path/to/cyberrotate && python ip_rotator.py status --json > /tmp/ip_status.json
```

#### Windows Task Scheduler
```powershell
# Create scheduled task for rotation
schtasks /create /tn "CyberRotate-Daily" /tr "python C:\cyberrotate\ip_rotator.py rotate" /sc daily /st 09:00
```

## 📊 Monitoring and Logging

### Status and Information

#### System information
```bash
# Detailed system info
python ip_rotator.py info --system

# Network diagnostics
python ip_rotator.py info --network

# Security status
python ip_rotator.py info --security
```

#### Logging options
```bash
# Log to file
python ip_rotator.py connect --log-file connection.log

# Different log levels
python ip_rotator.py connect --verbose     # INFO level
python ip_rotator.py connect --debug       # DEBUG level
python ip_rotator.py connect --quiet       # ERROR only
```

### Testing and Diagnostics

#### ip-check
Check current IP and location:
```bash
# Basic IP check
python ip_rotator.py ip-check

# Detailed location info
python ip_rotator.py ip-check --detailed

# Multiple IP check services
python ip_rotator.py ip-check --all-services

# Output formats
python ip_rotator.py ip-check --json
python ip_rotator.py ip-check --csv
```

#### speed-test
Test connection speed:
```bash
# Basic speed test
python ip_rotator.py speed-test

# Test specific server
python ip_rotator.py speed-test --server speedtest.net

# Save results
python ip_rotator.py speed-test --output results.json
```

#### security-scan
Comprehensive security check:
```bash
# Full security scan
python ip_rotator.py security-scan

# Specific tests
python ip_rotator.py security-scan --dns-leak
python ip_rotator.py security-scan --webrtc-leak
python ip_rotator.py security-scan --port-scan
```

## 🔄 Workflow Examples

### Daily IP Rotation Workflow
```bash
#!/bin/bash
# daily-rotation.sh

echo "Starting daily IP rotation..."

# Disconnect any existing connections
python ip_rotator.py disconnect

# Wait a moment
sleep 2

# Connect with new VPN server
python ip_rotator.py connect --vpn --country random

# Verify new IP
NEW_IP=$(python ip_rotator.py ip-check --json | jq -r '.ip')
echo "New IP: $NEW_IP"

# Log the change
echo "$(date): Rotated to $NEW_IP" >> /var/log/cyberrotate.log
```

### Proxy Testing and Cleanup
```bash
#!/bin/bash
# proxy-maintenance.sh

echo "Testing proxy list..."

# Test all proxies and remove dead ones
python ip_rotator.py proxy test-all --remove-dead

# Import new proxies if available
if [ -f "new-proxies.txt" ]; then
    python ip_rotator.py proxy import new-proxies.txt
    echo "Imported new proxies"
fi

# Show proxy statistics
python ip_rotator.py proxy stats
```

### Automated Security Monitoring
```bash
#!/bin/bash
# security-monitor.sh

# Run security scan
SCAN_RESULT=$(python ip_rotator.py security-scan --json)

# Check for DNS leaks
DNS_LEAK=$(echo $SCAN_RESULT | jq '.dns_leak')

if [ "$DNS_LEAK" = "true" ]; then
    echo "WARNING: DNS leak detected!"
    # Reconnect to fix potential leak
    python ip_rotator.py disconnect
    sleep 5
    python ip_rotator.py connect --vpn
fi
```

## 📝 Output Formats

### JSON Output
Many commands support `--json` flag for machine-readable output:

```bash
# Status in JSON
python ip_rotator.py status --json
```

```json
{
    "status": "connected",
    "service": "vpn",
    "ip_address": "203.0.113.1",
    "location": {
        "country": "United States",
        "city": "New York",
        "coordinates": [40.7128, -74.0060]
    },
    "uptime": 3600,
    "bytes_sent": 1048576,
    "bytes_received": 2097152
}
```

### CSV Output
Some commands support `--csv` for spreadsheet compatibility:

```bash
# Speed test results in CSV
python ip_rotator.py speed-test --csv
```

```csv
timestamp,server,download_mbps,upload_mbps,ping_ms
2024-01-15T10:30:00Z,us-west-1,50.2,25.1,45
```

## 🐛 CLI Troubleshooting

### Common Issues

1. **Command not found**
   ```bash
   # Ensure you're in the correct directory
   cd /path/to/cyberrotate-pro
   
   # Or use full path
   python /path/to/cyberrotate-pro/ip_rotator.py --help
   ```

2. **Permission errors**
   ```bash
   # Run with sudo (Linux/macOS)
   sudo python ip_rotator.py connect --vpn
   
   # Run as administrator (Windows)
   # Right-click Command Prompt > "Run as administrator"
   ```

3. **Connection timeouts**
   ```bash
   # Increase timeout
   python ip_rotator.py connect --timeout 60
   
   # Use different server
   python ip_rotator.py connect --vpn --server "backup-server"
   ```

4. **Configuration errors**
   ```bash
   # Reset to defaults
   python ip_rotator.py config reset
   
   # Validate configuration
   python ip_rotator.py config validate
   ```

### Debug Mode

Enable debug mode for detailed troubleshooting:

```bash
# Debug mode with file logging
python ip_rotator.py --debug --log-file debug.log connect --vpn

# Verbose output
python ip_rotator.py --verbose status
```

### Getting Help

```bash
# General help
python ip_rotator.py --help

# Command-specific help
python ip_rotator.py connect --help
python ip_rotator.py config --help

# List all commands
python ip_rotator.py commands
```

## 📚 CLI Reference Quick Card

### Essential Commands
| Command | Description | Example |
|---------|-------------|---------|
| `connect` | Establish connection | `connect --vpn` |
| `disconnect` | Terminate connection | `disconnect` |
| `status` | Show status | `status --detailed` |
| `rotate` | Change IP | `rotate --force` |
| `ip-check` | Check current IP | `ip-check --json` |
| `config` | Manage config | `config show` |

### Common Options
| Option | Short | Description |
|--------|-------|-------------|
| `--help` | `-h` | Show help |
| `--verbose` | `-v` | Verbose output |
| `--debug` | `-d` | Debug mode |
| `--json` | | JSON output |
| `--force` | `-f` | Force operation |

---

**Next**: [API Reference](06-api-reference.md) | [Back to Manual](README.md)
