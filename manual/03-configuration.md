# Configuration Guide

Complete guide to configuring CyberRotate Pro for your specific needs.

## 📁 Configuration File Locations

### Default Locations
- **Windows**: `%USERPROFILE%\cyberrotate\config\`
- **Linux**: `~/.cyberrotate/config/` or `./config/`
- **macOS**: `~/Library/Application Support/cyberrotate/config/`

### Configuration Files Structure
```
config/
├── config.json           # Main configuration
├── proxies/
│   ├── proxies.txt       # HTTP/HTTPS proxies
│   ├── socks4.txt        # SOCKS4 proxies
│   └── socks5.txt        # SOCKS5 proxies
├── openvpn/
│   ├── client.ovpn       # OpenVPN configs
│   └── auth.txt          # VPN credentials
├── tor/
│   └── torrc             # Tor configuration
└── ssl/
    ├── cert.pem          # SSL certificates
    └── key.pem           # SSL keys
```

## ⚙️ Main Configuration (config.json)

### Complete Configuration Example
```json
{
  "general": {
    "debug_mode": false,
    "log_level": "INFO",
    "log_file": "logs/cyberrotate.log",
    "user_agent": "CyberRotate Pro/1.0",
    "enable_statistics": true,
    "auto_save_stats": true
  },
  "proxy": {
    "rotation_interval": 300,
    "max_failures": 3,
    "timeout": 30,
    "verify_ssl": true,
    "test_url": "http://httpbin.org/ip",
    "concurrent_tests": 5,
    "retry_attempts": 2,
    "enable_geolocation": true,
    "preferred_countries": ["US", "CA", "GB", "DE"],
    "blacklisted_countries": ["CN", "RU"],
    "proxy_types": ["http", "https", "socks4", "socks5"],
    "authentication": {
      "username": "",
      "password": ""
    }
  },
  "openvpn": {
    "config_directory": "config/openvpn",
    "timeout": 30,
    "retry_attempts": 3,
    "auto_reconnect": true,
    "kill_switch": true,
    "dns_servers": ["1.1.1.1", "8.8.8.8"],
    "preferred_protocols": ["udp", "tcp"],
    "preferred_ports": [1194, 443, 80]
  },
  "tor": {
    "socks_port": 9150,
    "control_port": 9151,
    "auto_start": false,
    "new_identity_interval": 600,
    "max_circuits": 3,
    "exit_nodes": [],
    "entry_guards": [],
    "bridges": [],
    "use_bridges": false
  },
  "network": {
    "dns_servers": ["1.1.1.1", "8.8.8.8", "9.9.9.9"],
    "dns_leak_protection": true,
    "ipv6_leak_protection": true,
    "webrtc_leak_protection": true,
    "connection_timeout": 30,
    "read_timeout": 15,
    "max_redirects": 5
  },
  "security": {
    "enable_encryption": true,
    "kill_switch": true,
    "leak_detection": true,
    "auto_leak_test": true,
    "leak_test_interval": 3600,
    "secure_dns": true,
    "block_malware": false,
    "block_ads": false
  },
  "gui": {
    "theme": "dark",
    "auto_start": false,
    "minimize_to_tray": true,
    "start_minimized": false,
    "update_interval": 5,
    "show_notifications": true,
    "advanced_mode": false
  },
  "api": {
    "enabled": false,
    "host": "127.0.0.1",
    "port": 8080,
    "auth_token": "",
    "ssl_enabled": false,
    "cors_enabled": true,
    "rate_limiting": true
  },
  "automation": {
    "auto_rotate": false,
    "rotation_schedule": "*/5 * * * *",
    "health_check_interval": 60,
    "auto_recovery": true,
    "backup_connections": true,
    "failover_timeout": 30
  }
}
```

### Configuration Sections Explained

#### General Settings
```json
{
  "general": {
    "debug_mode": false,          // Enable debug logging
    "log_level": "INFO",          // LOG, DEBUG, INFO, WARNING, ERROR
    "log_file": "logs/app.log",   // Log file location
    "user_agent": "Custom UA",    // HTTP User-Agent string
    "enable_statistics": true,    // Collect usage statistics
    "auto_save_stats": true       // Auto-save statistics
  }
}
```

#### Proxy Configuration
```json
{
  "proxy": {
    "rotation_interval": 300,     // Seconds between rotations
    "max_failures": 3,           // Max failures before marking proxy bad
    "timeout": 30,               // Connection timeout in seconds
    "verify_ssl": true,          // Verify SSL certificates
    "test_url": "http://...",    // URL for testing proxies
    "concurrent_tests": 5,       // How many proxies to test simultaneously
    "retry_attempts": 2,         // Retry attempts for failed connections
    "enable_geolocation": true,  // Get location info for proxies
    "preferred_countries": [...], // Preferred proxy countries
    "blacklisted_countries": [...] // Blocked proxy countries
  }
}
```

## 🌐 Proxy Configuration

### Adding Proxy Lists

#### Format for proxy files:
```
# HTTP/HTTPS Proxies (proxies.txt)
192.168.1.1:8080
192.168.1.1:8080:username:password
http://192.168.1.1:8080
http://username:password@192.168.1.1:8080

# SOCKS4 Proxies (socks4.txt)
192.168.1.1:1080
socks4://192.168.1.1:1080

# SOCKS5 Proxies (socks5.txt)
192.168.1.1:1080
192.168.1.1:1080:username:password
socks5://192.168.1.1:1080
socks5://username:password@192.168.1.1:1080
```

#### Command Line Proxy Management:
```bash
# Add proxies from file
python ip_rotator.py --add-proxies proxies.txt

# Add single proxy
python ip_rotator.py --add-proxy "192.168.1.1:8080"

# Test all proxies
python ip_rotator.py --test-proxies

# Remove dead proxies
python ip_rotator.py --clean-proxies

# Show proxy statistics
python ip_rotator.py --proxy-stats
```

### Proxy Authentication
```json
{
  "proxy": {
    "authentication": {
      "username": "your_username",
      "password": "your_password"
    }
  }
}
```

### Proxy Rotation Strategies
```json
{
  "proxy": {
    "rotation_strategy": "round_robin", // round_robin, random, least_used
    "sticky_session": false,           // Keep same proxy for session
    "session_duration": 3600,          // Session duration in seconds
    "health_check": true,              // Enable proxy health checking
    "health_check_interval": 300       // Health check interval
  }
}
```

## 🔐 VPN Configuration

### OpenVPN Setup

#### Basic OpenVPN Configuration:
```bash
# Create OpenVPN config directory
mkdir -p config/openvpn

# Add your .ovpn files to the directory
cp my-vpn-config.ovpn config/openvpn/

# Add authentication file (if needed)
echo "username" > config/openvpn/auth.txt
echo "password" >> config/openvpn/auth.txt
```

#### OpenVPN Configuration Options:
```json
{
  "openvpn": {
    "config_directory": "config/openvpn",
    "timeout": 30,
    "retry_attempts": 3,
    "auto_reconnect": true,           // Auto-reconnect on disconnect
    "kill_switch": true,              // Block traffic if VPN fails
    "dns_servers": ["1.1.1.1", "8.8.8.8"], // Custom DNS servers
    "preferred_protocols": ["udp"],   // Preferred protocols
    "preferred_ports": [1194, 443],   // Preferred ports
    "verify_certificate": true,       // Verify server certificates
    "compression": "lz4-v2",         // Compression method
    "cipher": "AES-256-GCM"          // Encryption cipher
  }
}
```

### VPN Server Selection:
```bash
# List available VPN servers
python ip_rotator.py --list-vpn-servers

# Connect to specific server
python ip_rotator.py --vpn connect "server-name"

# Rotate VPN servers
python ip_rotator.py --vpn rotate

# Disconnect VPN
python ip_rotator.py --vpn disconnect
```

## 🧅 Tor Configuration

### Basic Tor Setup:
```json
{
  "tor": {
    "socks_port": 9150,              // SOCKS proxy port
    "control_port": 9151,            // Control port
    "auto_start": false,             // Auto-start Tor service
    "new_identity_interval": 600,    // Auto new identity interval
    "max_circuits": 3,               // Maximum circuits
    "circuit_timeout": 30,           // Circuit build timeout
    "use_bridges": false,            // Use bridge relays
    "bridges": []                    // Bridge relay addresses
  }
}
```

### Advanced Tor Configuration:
```json
{
  "tor": {
    "exit_nodes": ["US", "CA", "GB"], // Preferred exit countries
    "entry_guards": [],               // Specific entry guards
    "exclude_nodes": ["CN", "RU"],   // Excluded countries
    "use_entry_guards": true,         // Use entry guards
    "num_entry_guards": 3,           // Number of entry guards
    "circuit_build_timeout": 60,     // Circuit build timeout
    "max_client_circuits_pending": 32 // Max pending circuits
  }
}
```

### Tor Bridge Configuration:
```json
{
  "tor": {
    "use_bridges": true,
    "bridges": [
      "bridge 192.0.2.1:443",
      "obfs4 192.0.2.2:80 cert=..."
    ],
    "client_transport_plugin": [
      "obfs4 exec /usr/bin/obfs4proxy"
    ]
  }
}
```

## 🛡️ Security Configuration

### DNS Leak Protection:
```json
{
  "network": {
    "dns_servers": ["1.1.1.1", "8.8.8.8"],
    "dns_leak_protection": true,
    "force_dns_through_proxy": true,
    "block_dns_queries": false,
    "custom_dns_port": 53
  }
}
```

### Security Features:
```json
{
  "security": {
    "enable_encryption": true,        // Enable traffic encryption
    "kill_switch": true,              // Network kill switch
    "leak_detection": true,           // Auto leak detection
    "auto_leak_test": true,          // Automatic leak testing
    "leak_test_interval": 3600,      // Leak test interval
    "secure_dns": true,              // Use secure DNS
    "block_malware": false,          // Block malware domains
    "block_ads": false,              // Block advertising
    "ipv6_leak_protection": true,    // IPv6 leak protection
    "webrtc_leak_protection": true   // WebRTC leak protection
  }
}
```

## 🖥️ GUI Configuration

### GUI Appearance:
```json
{
  "gui": {
    "theme": "dark",                 // dark, light, auto
    "language": "en",                // Interface language
    "auto_start": false,             // Start with system
    "minimize_to_tray": true,        // Minimize to system tray
    "start_minimized": false,        // Start minimized
    "window_size": "1200x800",       // Default window size
    "always_on_top": false,          // Keep window on top
    "transparency": 1.0,             // Window transparency
    "show_splash": true              // Show splash screen
  }
}
```

### GUI Behavior:
```json
{
  "gui": {
    "update_interval": 5,            // Status update interval
    "show_notifications": true,      // Show system notifications
    "advanced_mode": false,          // Enable advanced features
    "confirm_actions": true,         // Confirm destructive actions
    "save_window_state": true,       // Save window position/size
    "auto_refresh": true,            // Auto-refresh data
    "log_level_gui": "INFO"          // GUI log level
  }
}
```

## 🌐 API Configuration

### API Server Settings:
```json
{
  "api": {
    "enabled": false,                // Enable API server
    "host": "127.0.0.1",            // Bind address
    "port": 8080,                    // Port number
    "auth_token": "secret_token",    // Authentication token
    "ssl_enabled": false,            // Enable HTTPS
    "ssl_cert": "ssl/cert.pem",      // SSL certificate
    "ssl_key": "ssl/key.pem",        // SSL private key
    "cors_enabled": true,            // Enable CORS
    "cors_origins": ["*"],           // Allowed origins
    "rate_limiting": true,           // Enable rate limiting
    "rate_limit": "100/hour"         // Rate limit
  }
}
```

## 🤖 Automation Configuration

### Scheduled Rotation:
```json
{
  "automation": {
    "auto_rotate": true,             // Enable auto rotation
    "rotation_schedule": "*/5 * * * *", // Cron schedule
    "rotation_methods": ["proxy", "tor"], // Methods to rotate
    "health_check_interval": 60,     // Health check interval
    "auto_recovery": true,           // Auto-recovery on failure
    "backup_connections": true,      // Maintain backup connections
    "failover_timeout": 30           // Failover timeout
  }
}
```

### Health Monitoring:
```json
{
  "monitoring": {
    "enabled": true,                 // Enable monitoring
    "check_interval": 60,            // Check interval
    "check_timeout": 10,             // Check timeout
    "failure_threshold": 3,          // Failure threshold
    "recovery_threshold": 2,         // Recovery threshold
    "alert_on_failure": true,        // Alert on failure
    "alert_email": "user@example.com" // Alert email
  }
}
```

## 📝 Configuration Management

### Command Line Configuration:
```bash
# View current configuration
python ip_rotator.py --config show

# Set configuration value
python ip_rotator.py --config set proxy.timeout 60

# Get configuration value
python ip_rotator.py --config get proxy.timeout

# Reset to defaults
python ip_rotator.py --config reset

# Backup configuration
python ip_rotator.py --config backup

# Restore configuration
python ip_rotator.py --config restore backup.json

# Validate configuration
python ip_rotator.py --config validate
```

### Configuration Profiles:
```bash
# Create profile
python ip_rotator.py --profile create work

# Switch profile
python ip_rotator.py --profile switch work

# List profiles
python ip_rotator.py --profile list

# Delete profile
python ip_rotator.py --profile delete work
```

## 🔧 Environment Variables

### Override Configuration with Environment Variables:
```bash
# General settings
export CYBERROTATE_DEBUG=true
export CYBERROTATE_LOG_LEVEL=DEBUG

# Proxy settings
export CYBERROTATE_PROXY_TIMEOUT=60
export CYBERROTATE_PROXY_ROTATION_INTERVAL=300

# Security settings
export CYBERROTATE_DNS_LEAK_PROTECTION=true
export CYBERROTATE_KILL_SWITCH=true

# API settings
export CYBERROTATE_API_ENABLED=true
export CYBERROTATE_API_TOKEN=your_secret_token
```

## ✅ Configuration Validation

### Validate Your Configuration:
```bash
# Check configuration syntax
python ip_rotator.py --config validate

# Test configuration settings
python ip_rotator.py --test-config

# Show configuration issues
python ip_rotator.py --config lint
```

## 📋 Configuration Templates

### Basic Template (minimal):
```json
{
  "proxy": {
    "rotation_interval": 300,
    "timeout": 30
  },
  "security": {
    "dns_leak_protection": true,
    "kill_switch": true
  }
}
```

### Advanced Template (full features):
```json
{
  "general": {
    "debug_mode": false,
    "log_level": "INFO"
  },
  "proxy": {
    "rotation_interval": 300,
    "max_failures": 3,
    "timeout": 30,
    "preferred_countries": ["US", "CA", "GB"]
  },
  "openvpn": {
    "auto_reconnect": true,
    "kill_switch": true,
    "dns_servers": ["1.1.1.1", "8.8.8.8"]
  },
  "tor": {
    "auto_start": false,
    "new_identity_interval": 600
  },
  "security": {
    "dns_leak_protection": true,
    "kill_switch": true,
    "leak_detection": true
  },
  "automation": {
    "auto_rotate": true,
    "rotation_schedule": "*/5 * * * *"
  }
}
```

## 🆘 Configuration Troubleshooting

### Common Issues:

#### Invalid JSON Syntax:
```bash
# Validate JSON syntax
python ip_rotator.py --config validate

# Use JSON linter
python -m json.tool config/config.json
```

#### Permission Issues:
```bash
# Check file permissions
ls -la config/

# Fix permissions (Linux/macOS)
chmod 644 config/config.json
chmod 755 config/
```

#### Configuration Not Loading:
```bash
# Check configuration search paths
python ip_rotator.py --config paths

# Force specific config file
python ip_rotator.py --config-file /path/to/config.json
```

---

**Next**: Learn about the [GUI Interface](04-gui-guide.md) or [CLI Usage](05-cli-guide.md)
