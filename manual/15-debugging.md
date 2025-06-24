# Debugging Guide

Advanced debugging techniques and tools for CyberRotate Pro developers and power users.

## 🔍 Debug Mode Overview

### Enabling Debug Mode
```bash
# Command line debug
python ip_rotator.py --debug

# Debug with verbose output
python ip_rotator.py --debug --verbose

# Debug with file logging
python ip_rotator.py --debug --log-file debug.log

# Debug specific components
python ip_rotator.py --debug --component vpn,proxy
```

### Debug Configuration
```bash
# Set debug level in config
python ip_rotator.py config set debug.level DEBUG
python ip_rotator.py config set debug.components "vpn,proxy,network"
python ip_rotator.py config set debug.file_logging true
python ip_rotator.py config set debug.console_output true
```

## 📊 Logging System

### Log Levels
- **DEBUG**: Detailed diagnostic information
- **INFO**: General application information
- **WARNING**: Warning messages
- **ERROR**: Error conditions
- **CRITICAL**: Critical error conditions

### Log Configuration
```json
{
    "logging": {
        "level": "DEBUG",
        "file_logging": true,
        "console_logging": true,
        "max_file_size": "10MB",
        "backup_count": 5,
        "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        "components": {
            "vpn": "DEBUG",
            "proxy": "INFO",
            "tor": "WARNING",
            "network": "DEBUG",
            "security": "INFO"
        }
    }
}
```

### Log File Locations
```bash
# Default locations
Linux:   ~/.cyberrotate/logs/
macOS:   ~/Library/Logs/CyberRotate/
Windows: %APPDATA%\CyberRotate\logs\

# Find current log location
python ip_rotator.py info log-location

# List all log files
python ip_rotator.py logs list
```

### Log Analysis Tools
```bash
# View recent logs
python ip_rotator.py logs tail --lines 100

# Search logs
python ip_rotator.py logs search "connection failed"

# Filter by component
python ip_rotator.py logs filter --component vpn --level ERROR

# Export logs
python ip_rotator.py logs export --format json --output debug_logs.json
```

## 🕷️ Component-Specific Debugging

### VPN Debugging

#### Enable VPN Debug Logging
```bash
# VPN component debug
python ip_rotator.py --debug --component vpn connect

# OpenVPN debug
python ip_rotator.py config set vpn.openvpn_debug_level 3

# WireGuard debug
python ip_rotator.py config set vpn.wireguard_debug true
```

#### VPN Debug Output Example
```
[DEBUG] VPN: Starting connection to server us-west-1
[DEBUG] VPN: Loading configuration from /path/to/config.ovpn
[DEBUG] VPN: Authenticating with credentials
[DEBUG] VPN: Establishing TLS connection
[DEBUG] VPN: TLS handshake completed
[DEBUG] VPN: Receiving configuration from server
[DEBUG] VPN: Setting up routing table
[DEBUG] VPN: Connection established successfully
[INFO]  VPN: Connected to us-west-1 (203.0.113.1)
```

#### VPN Configuration Debugging
```bash
# Test VPN configuration
python ip_rotator.py vpn debug-config config.ovpn

# Validate VPN credentials
python ip_rotator.py vpn test-auth

# Check VPN routing
python ip_rotator.py vpn debug-routes

# Monitor VPN traffic
python ip_rotator.py vpn monitor-traffic --duration 60
```

### Proxy Debugging

#### Enable Proxy Debug Logging
```bash
# Proxy component debug
python ip_rotator.py --debug --component proxy

# Debug proxy testing
python ip_rotator.py proxy test --debug proxy.example.com:8080

# Debug proxy rotation
python ip_rotator.py --debug rotate --method proxy
```

#### Proxy Debug Output Example
```
[DEBUG] Proxy: Testing proxy 1.2.3.4:8080
[DEBUG] Proxy: Connecting through SOCKS5 proxy
[DEBUG] Proxy: Sending authentication (user/pass)
[DEBUG] Proxy: Authentication successful
[DEBUG] Proxy: Establishing connection to target
[DEBUG] Proxy: Connection established (response time: 150ms)
[DEBUG] Proxy: IP changed from 192.168.1.100 to 1.2.3.4
[INFO]  Proxy: Successfully connected through 1.2.3.4:8080
```

#### Proxy Connection Analysis
```bash
# Analyze proxy performance
python ip_rotator.py proxy analyze-performance

# Debug proxy authentication
python ip_rotator.py proxy debug-auth proxy_id

# Trace proxy connections
python ip_rotator.py proxy trace-connections
```

### Tor Debugging

#### Enable Tor Debug Logging
```bash
# Tor component debug
python ip_rotator.py --debug --component tor

# Tor service debug
python ip_rotator.py tor start --debug

# Monitor Tor circuits
python ip_rotator.py tor monitor-circuits
```

#### Tor Debug Output Example
```
[DEBUG] Tor: Starting Tor service on port 9050
[DEBUG] Tor: Loading Tor configuration
[DEBUG] Tor: Connecting to Tor network
[DEBUG] Tor: Building circuits...
[DEBUG] Tor: Circuit 1: Guard(US) -> Middle(DE) -> Exit(UK)
[DEBUG] Tor: Circuit established successfully
[DEBUG] Tor: SOCKS proxy available on 127.0.0.1:9050
[INFO]  Tor: Connected to Tor network
```

#### Tor Network Analysis
```bash
# Debug Tor circuits
python ip_rotator.py tor debug-circuits

# Analyze Tor performance
python ip_rotator.py tor performance-test

# Check Tor consensus
python ip_rotator.py tor check-consensus
```

### Network Debugging

#### Network Diagnostics
```bash
# Debug network interfaces
python ip_rotator.py network debug-interfaces

# Test DNS resolution
python ip_rotator.py network debug-dns

# Check routing table
python ip_rotator.py network debug-routes

# Monitor network traffic
python ip_rotator.py network monitor --interface all
```

#### Network Debug Output
```
[DEBUG] Network: Available interfaces:
[DEBUG] Network:   eth0: 192.168.1.100/24 (UP)
[DEBUG] Network:   tun0: 10.8.0.1/24 (UP) [VPN]
[DEBUG] Network:   lo: 127.0.0.1/8 (UP)
[DEBUG] Network: Default route via 192.168.1.1
[DEBUG] Network: DNS servers: 8.8.8.8, 1.1.1.1
[DEBUG] Network: VPN traffic routing through tun0
```

## 🔧 Advanced Debugging Tools

### Packet Capture
```bash
# Capture VPN traffic
python ip_rotator.py debug capture --interface tun0 --duration 60

# Capture proxy traffic
python ip_rotator.py debug capture --filter "port 8080" --output proxy.pcap

# Analyze captured packets
python ip_rotator.py debug analyze-capture capture.pcap
```

### Performance Profiling
```bash
# Profile application performance
python ip_rotator.py debug profile --duration 300

# Memory usage analysis
python ip_rotator.py debug memory-profile

# CPU usage monitoring
python ip_rotator.py debug cpu-monitor --interval 5
```

### System Tracing
```bash
# Trace system calls (Linux)
python ip_rotator.py debug strace --output strace.log

# Monitor file operations
python ip_rotator.py debug file-monitor

# Network connection tracing
python ip_rotator.py debug netstat-monitor
```

## 🧪 Testing Framework

### Unit Testing
```bash
# Run all tests
python ip_rotator.py test

# Run specific test modules
python ip_rotator.py test --module vpn
python ip_rotator.py test --module proxy
python ip_rotator.py test --module security

# Run tests with coverage
python ip_rotator.py test --coverage
```

### Integration Testing
```bash
# Test VPN integration
python ip_rotator.py test integration --vpn

# Test proxy integration
python ip_rotator.py test integration --proxy

# Test Tor integration
python ip_rotator.py test integration --tor

# Full integration test
python ip_rotator.py test integration --all
```

### Performance Testing
```bash
# Connection speed tests
python ip_rotator.py test performance --speed

# Rotation timing tests
python ip_rotator.py test performance --rotation

# Memory leak detection
python ip_rotator.py test performance --memory-leak

# Stress testing
python ip_rotator.py test stress --duration 3600
```

## 🔍 Real-time Monitoring

### Live Monitoring Dashboard
```bash
# Start monitoring dashboard
python ip_rotator.py monitor dashboard

# Monitor specific components
python ip_rotator.py monitor --components vpn,proxy

# Real-time log monitoring
python ip_rotator.py logs monitor --follow
```

### WebSocket Debug Interface
```python
# Connect to debug WebSocket
import websocket
import json

def on_message(ws, message):
    data = json.loads(message)
    print(f"Debug: {data}")

ws = websocket.WebSocketApp(
    "ws://localhost:8080/debug/ws",
    on_message=on_message
)
ws.run_forever()
```

### Metrics Collection
```bash
# Enable metrics collection
python ip_rotator.py config set metrics.enabled true

# Export metrics to file
python ip_rotator.py metrics export --format json

# Send metrics to monitoring system
python ip_rotator.py metrics send --endpoint http://monitoring.local/api
```

## 🐛 Common Debug Scenarios

### Connection Failure Analysis

#### Debugging VPN Connection Failures
```bash
# Step 1: Enable verbose logging
python ip_rotator.py --debug connect --vpn --server us-west-1

# Step 2: Check configuration
python ip_rotator.py vpn debug-config

# Step 3: Test network connectivity
python ip_rotator.py network test-connectivity --host vpn-server.com --port 1194

# Step 4: Analyze authentication
python ip_rotator.py vpn test-auth --verbose

# Step 5: Check firewall rules
python ip_rotator.py security check-firewall --service vpn
```

#### Debug Log Analysis for VPN Issues
```bash
# Search for authentication errors
grep -i "auth.*fail" ~/.cyberrotate/logs/debug.log

# Look for network errors
grep -i "network.*error\|timeout\|unreachable" ~/.cyberrotate/logs/debug.log

# Check TLS/SSL issues
grep -i "tls\|ssl\|certificate" ~/.cyberrotate/logs/debug.log
```

### IP Rotation Issues

#### Debugging Failed Rotations
```bash
# Enable rotation debugging
python ip_rotator.py --debug rotate --method vpn

# Check rotation history
python ip_rotator.py rotation history --debug

# Test rotation mechanisms
python ip_rotator.py rotation test --all-methods

# Analyze rotation failures
python ip_rotator.py rotation analyze-failures
```

### Security Issue Debugging

#### DNS Leak Investigation
```bash
# Debug DNS resolution
python ip_rotator.py --debug security dns-leak-test

# Trace DNS queries
python ip_rotator.py debug dns-trace --duration 60

# Check DNS configuration
python ip_rotator.py network debug-dns --verbose
```

#### Kill Switch Debugging
```bash
# Debug kill switch activation
python ip_rotator.py --debug security test-kill-switch

# Check firewall rules
python ip_rotator.py security debug-firewall-rules

# Monitor kill switch events
python ip_rotator.py security monitor-kill-switch
```

## 📊 Debug Data Export

### Comprehensive Debug Report
```bash
# Generate full debug report
python ip_rotator.py debug generate-report --include-all

# Include system information
python ip_rotator.py debug generate-report --system-info

# Include network configuration
python ip_rotator.py debug generate-report --network-config

# Include recent logs
python ip_rotator.py debug generate-report --logs --days 7
```

### Debug Report Structure
```json
{
    "report_id": "debug_20240115_103000",
    "timestamp": "2024-01-15T10:30:00Z",
    "version": "CyberRotate Pro v2.0.0",
    "system": {
        "os": "Windows 11",
        "python": "3.9.7",
        "architecture": "x64"
    },
    "configuration": {
        "vpn": {...},
        "proxy": {...},
        "security": {...}
    },
    "network": {
        "interfaces": [...],
        "routing": [...],
        "dns": [...]
    },
    "logs": {
        "errors": [...],
        "warnings": [...],
        "debug_entries": [...]
    },
    "performance": {
        "cpu_usage": 15.2,
        "memory_usage": 234.5,
        "network_io": {...}
    }
}
```

### Exporting Debug Data
```bash
# Export to JSON
python ip_rotator.py debug export --format json --output debug_data.json

# Export to XML
python ip_rotator.py debug export --format xml --output debug_data.xml

# Export to CSV (metrics only)
python ip_rotator.py debug export --format csv --metrics-only

# Compress debug data
python ip_rotator.py debug export --compress --output debug_bundle.zip
```

## 🔧 Custom Debug Scripts

### Creating Debug Scripts
```python
#!/usr/bin/env python3
# debug_connection.py

import sys
import logging
from ip_rotator import CyberRotate

# Configure debug logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

def debug_vpn_connection():
    """Debug VPN connection process step by step"""
    cr = CyberRotate(debug=True)
    
    print("=== VPN Connection Debug ===")
    
    # Step 1: Check prerequisites
    print("1. Checking prerequisites...")
    if not cr.vpn.check_prerequisites():
        print("❌ Prerequisites not met")
        return False
    print("✅ Prerequisites OK")
    
    # Step 2: Load configuration
    print("2. Loading VPN configuration...")
    try:
        config = cr.vpn.load_config()
        print(f"✅ Config loaded: {config['provider']}")
    except Exception as e:
        print(f"❌ Config error: {e}")
        return False
    
    # Step 3: Test connectivity
    print("3. Testing server connectivity...")
    if cr.vpn.test_connectivity():
        print("✅ Server reachable")
    else:
        print("❌ Server unreachable")
        return False
    
    # Step 4: Attempt connection
    print("4. Attempting connection...")
    try:
        result = cr.vpn.connect()
        if result['success']:
            print(f"✅ Connected: {result['ip']}")
        else:
            print(f"❌ Connection failed: {result['error']}")
    except Exception as e:
        print(f"❌ Exception: {e}")
        return False
    
    return True

if __name__ == "__main__":
    debug_vpn_connection()
```

### Running Custom Debug Scripts
```bash
# Make script executable
chmod +x debug_connection.py

# Run debug script
python debug_connection.py

# Run with additional debugging
python debug_connection.py --verbose

# Redirect output to file
python debug_connection.py > debug_output.log 2>&1
```

## 📱 GUI Debugging

### GUI Debug Mode
```bash
# Start GUI with debug console
python ip_rotator.py --gui --debug-console

# GUI with debug overlay
python ip_rotator.py --gui --debug-overlay

# GUI performance debugging
python ip_rotator.py --gui --debug-performance
```

### GUI Debug Tools
- **Debug Console**: Interactive Python console
- **Widget Inspector**: Inspect GUI elements
- **Event Logger**: Log GUI events
- **Performance Monitor**: Monitor GUI performance

### GUI Debug Output
```
[GUI-DEBUG] MainWindow initialized
[GUI-DEBUG] Connection panel created
[GUI-DEBUG] Status panel created
[GUI-DEBUG] Log panel created
[GUI-DEBUG] Event: connect_button_clicked
[GUI-DEBUG] Calling VPN connect method
[GUI-DEBUG] Updating status display
[GUI-DEBUG] Event: status_updated
```

## 📋 Debug Checklist

### Pre-Debug Checklist
- [ ] Latest version installed
- [ ] Debug mode enabled
- [ ] Log files accessible
- [ ] Network connectivity verified
- [ ] Sufficient disk space for logs
- [ ] Administrative privileges (if needed)

### Debug Process
1. **Reproduce the issue** with debug logging enabled
2. **Collect relevant logs** and system information
3. **Analyze log patterns** for error messages
4. **Test individual components** in isolation
5. **Generate comprehensive report** for analysis
6. **Document findings** and solutions

### Post-Debug Actions
- [ ] Document the solution
- [ ] Update configuration if needed
- [ ] Report bugs to development team
- [ ] Share solution with community
- [ ] Clean up debug files

---

**Next**: [FAQ](16-faq.md) | [Back to Manual](README.md)
