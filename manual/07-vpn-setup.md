# VPN Setup & Management

Comprehensive guide to configuring and managing VPN connections in CyberRotate Pro.

## 🌐 VPN Provider Overview

CyberRotate Pro supports multiple VPN providers and protocols, giving you flexibility and reliability for your privacy needs.

### Supported VPN Providers

#### Commercial Providers
- **NordVPN** - 5000+ servers, 60+ countries
- **ExpressVPN** - 3000+ servers, 94+ countries  
- **Surfshark** - 3200+ servers, 65+ countries
- **CyberGhost** - 7000+ servers, 90+ countries
- **ProtonVPN** - 1700+ servers, 60+ countries
- **Mullvad** - 800+ servers, 38+ countries
- **IVPN** - 150+ servers, 32+ countries

#### Free Providers
- **ProtonVPN Free** - 3 server locations
- **Windscribe Free** - 10 server locations
- **TunnelBear Free** - 20+ server locations

#### Custom Configurations
- **OpenVPN** - Any .ovpn configuration file
- **WireGuard** - Any .conf configuration file
- **IKEv2/IPSec** - Standard IPSec configurations

## ⚙️ Initial VPN Setup

### Method 1: Provider Configuration Wizard

```bash
# Start configuration wizard
python ip_rotator.py vpn setup-wizard

# Follow interactive prompts:
# 1. Select VPN provider
# 2. Enter credentials
# 3. Choose server preferences
# 4. Test connection
```

### Method 2: Manual Provider Setup

#### NordVPN Configuration
```bash
# Add NordVPN provider
python ip_rotator.py vpn add-provider \
  --name "nordvpn" \
  --type commercial \
  --protocol openvpn \
  --server-list-url "https://api.nordvpn.com/v1/servers" \
  --username "your_username" \
  --password "your_password"

# Download server configurations
python ip_rotator.py vpn download-configs nordvpn

# Test connection
python ip_rotator.py vpn test nordvpn
```

#### Custom OpenVPN Setup
```bash
# Import OpenVPN configuration
python ip_rotator.py vpn import-config client.ovpn

# Batch import multiple configs
python ip_rotator.py vpn import-configs /path/to/configs/*.ovpn

# Set authentication
python ip_rotator.py vpn set-auth "your_username" "your_password"
```

### Method 3: Configuration File Setup

Create a provider configuration file:

```json
{
    "provider": "nordvpn",
    "type": "commercial",
    "protocol": "openvpn",
    "authentication": {
        "username": "your_username",
        "password": "your_password"
    },
    "servers": {
        "api_url": "https://api.nordvpn.com/v1/servers",
        "update_interval": 3600
    },
    "preferences": {
        "preferred_countries": ["US", "UK", "DE"],
        "avoid_countries": ["CN", "RU"],
        "protocol_priority": ["wireguard", "openvpn"],
        "features": ["P2P", "streaming"]
    }
}
```

Load the configuration:
```bash
python ip_rotator.py vpn load-config nordvpn-config.json
```

## 🔧 VPN Configuration Options

### Connection Settings

#### Protocol Configuration
```bash
# Set preferred protocol
python ip_rotator.py config set vpn.protocol openvpn

# Protocol-specific settings
python ip_rotator.py config set vpn.openvpn.cipher "AES-256-GCM"
python ip_rotator.py config set vpn.openvpn.auth "SHA256"
python ip_rotator.py config set vpn.wireguard.mtu 1420
```

#### Server Selection
```bash
# Set preferred countries
python ip_rotator.py config set vpn.preferred_countries "US,UK,DE,CA"

# Avoid specific countries
python ip_rotator.py config set vpn.avoid_countries "CN,RU,IR"

# Server features
python ip_rotator.py config set vpn.required_features "P2P,streaming"

# Load balancing
python ip_rotator.py config set vpn.load_balance true
python ip_rotator.py config set vpn.max_load 80
```

#### Connection Behavior
```bash
# Auto-reconnect settings
python ip_rotator.py config set vpn.auto_reconnect true
python ip_rotator.py config set vpn.reconnect_delay 5
python ip_rotator.py config set vpn.max_reconnect_attempts 3

# Connection timeouts
python ip_rotator.py config set vpn.connect_timeout 30
python ip_rotator.py config set vpn.data_timeout 60

# Keep-alive settings
python ip_rotator.py config set vpn.keepalive_interval 10
python ip_rotator.py config set vpn.keepalive_timeout 120
```

### Security Settings

#### Encryption Configuration
```bash
# OpenVPN encryption
python ip_rotator.py config set vpn.openvpn.cipher "AES-256-GCM"
python ip_rotator.py config set vpn.openvpn.auth "SHA512"
python ip_rotator.py config set vpn.openvpn.tls_cipher "TLS-ECDHE-RSA-WITH-AES-256-GCM-SHA384"

# WireGuard settings
python ip_rotator.py config set vpn.wireguard.private_key_file "/path/to/private.key"
python ip_rotator.py config set vpn.wireguard.preshared_key_file "/path/to/psk.key"
```

#### DNS and Leak Protection
```bash
# Force DNS through VPN
python ip_rotator.py config set vpn.force_dns true

# Custom DNS servers
python ip_rotator.py config set vpn.dns_servers "1.1.1.1,1.0.0.1"

# IPv6 protection
python ip_rotator.py config set vpn.disable_ipv6 true

# DNS leak protection
python ip_rotator.py config set vpn.dns_leak_protection true
```

#### Kill Switch Configuration
```bash
# Enable kill switch
python ip_rotator.py config set vpn.kill_switch true

# Kill switch strictness
python ip_rotator.py config set vpn.kill_switch_strict true

# Allow local network
python ip_rotator.py config set vpn.allow_local_network true

# Allowed applications during kill switch
python ip_rotator.py config set vpn.kill_switch_exceptions "firefox.exe,chrome.exe"
```

## 🖥️ VPN Management Commands

### Connection Management

#### Basic Connection
```bash
# Connect to optimal server
python ip_rotator.py vpn connect

# Connect to specific country
python ip_rotator.py vpn connect --country US

# Connect to specific server
python ip_rotator.py vpn connect --server us-west-1

# Connect with specific protocol
python ip_rotator.py vpn connect --protocol wireguard
```

#### Advanced Connection Options
```bash
# Connect with custom settings
python ip_rotator.py vpn connect \
  --country "US" \
  --protocol "openvpn" \
  --features "P2P,streaming" \
  --max-load 70

# Connect with failover
python ip_rotator.py vpn connect \
  --primary "us-west-1" \
  --fallback "us-east-1,uk-london-1"

# Connect with retry logic
python ip_rotator.py vpn connect \
  --retry-attempts 5 \
  --retry-delay 10
```

#### Disconnection
```bash
# Graceful disconnect
python ip_rotator.py vpn disconnect

# Force disconnect
python ip_rotator.py vpn disconnect --force

# Disconnect and clean up
python ip_rotator.py vpn disconnect --cleanup
```

### Server Management

#### Server Discovery
```bash
# List all available servers
python ip_rotator.py vpn list-servers

# Filter servers by country
python ip_rotator.py vpn list-servers --country US

# Filter by features
python ip_rotator.py vpn list-servers --features "P2P,streaming"

# Filter by load
python ip_rotator.py vpn list-servers --max-load 50

# Show detailed server info
python ip_rotator.py vpn server-info us-west-1
```

#### Server Testing
```bash
# Test server connectivity
python ip_rotator.py vpn test-server us-west-1

# Speed test specific server
python ip_rotator.py vpn speed-test us-west-1

# Test multiple servers
python ip_rotator.py vpn test-servers --country US --count 5

# Find fastest servers
python ip_rotator.py vpn find-fastest --country US --count 3
```

#### Server Preferences
```bash
# Add server to favorites
python ip_rotator.py vpn favorite-add us-west-1

# Remove from favorites
python ip_rotator.py vpn favorite-remove us-west-1

# List favorite servers
python ip_rotator.py vpn favorite-list

# Blacklist problematic server
python ip_rotator.py vpn blacklist-add slow-server-1
```

### Status and Monitoring

#### Connection Status
```bash
# Basic status
python ip_rotator.py vpn status

# Detailed status
python ip_rotator.py vpn status --detailed

# Status in JSON format
python ip_rotator.py vpn status --json

# Status with network info
python ip_rotator.py vpn status --network-info
```

#### Real-time Monitoring
```bash
# Monitor connection continuously
python ip_rotator.py vpn monitor

# Monitor with specific interval
python ip_rotator.py vpn monitor --interval 30

# Monitor and log to file
python ip_rotator.py vpn monitor --log-file vpn-monitor.log

# Monitor with alerts
python ip_rotator.py vpn monitor --alert-on-disconnect
```

#### Traffic Statistics
```bash
# Show traffic statistics
python ip_rotator.py vpn stats

# Reset statistics
python ip_rotator.py vpn stats --reset

# Export statistics
python ip_rotator.py vpn stats --export stats.json

# Real-time traffic monitoring
python ip_rotator.py vpn traffic-monitor
```

## 🔄 VPN Rotation

### Manual Rotation
```bash
# Rotate to random server
python ip_rotator.py vpn rotate

# Rotate within same country
python ip_rotator.py vpn rotate --same-country

# Rotate to specific country
python ip_rotator.py vpn rotate --country UK

# Rotate with server preferences
python ip_rotator.py vpn rotate --features "streaming" --max-load 60
```

### Automatic Rotation
```bash
# Start auto-rotation (every 30 minutes)
python ip_rotator.py vpn auto-rotate --interval 30m

# Auto-rotate with country list
python ip_rotator.py vpn auto-rotate \
  --interval 15m \
  --countries "US,UK,DE,CA" \
  --random-order

# Auto-rotate with conditions
python ip_rotator.py vpn auto-rotate \
  --interval 20m \
  --on-high-load 80 \
  --on-speed-drop 50

# Stop auto-rotation
python ip_rotator.py vpn auto-rotate --stop
```

### Scheduled Rotation
```bash
# Schedule daily rotation
python ip_rotator.py vpn schedule \
  --time "09:00" \
  --action "rotate" \
  --country "random"

# Schedule weekly server change
python ip_rotator.py vpn schedule \
  --weekly "monday" \
  --time "02:00" \
  --action "connect" \
  --server "optimal"

# List scheduled tasks
python ip_rotator.py vpn schedule --list

# Remove scheduled task
python ip_rotator.py vpn schedule --remove task_id
```

## 🛡️ Advanced VPN Features

### Multi-Hop VPN
```bash
# Enable double VPN
python ip_rotator.py vpn multi-hop \
  --entry-country "US" \
  --exit-country "UK"

# Configure VPN chain
python ip_rotator.py vpn chain \
  --servers "us-west-1,uk-london-1,de-frankfurt-1"

# Test multi-hop performance
python ip_rotator.py vpn test-multi-hop
```

### Split Tunneling
```bash
# Enable split tunneling
python ip_rotator.py config set vpn.split_tunnel true

# Add applications to tunnel
python ip_rotator.py vpn split-tunnel add "firefox.exe"
python ip_rotator.py vpn split-tunnel add "torrent-client.exe"

# Exclude applications from tunnel
python ip_rotator.py vpn split-tunnel exclude "gaming-app.exe"

# Configure by IP ranges
python ip_rotator.py vpn split-tunnel add-range "192.168.1.0/24"
```

### Custom Routing
```bash
# Add custom routes
python ip_rotator.py vpn route add 192.168.100.0/24 --gateway vpn

# Route specific domains through VPN
python ip_rotator.py vpn route add-domain "streaming-site.com"

# Bypass VPN for specific IPs
python ip_rotator.py vpn route bypass 8.8.8.8

# Show current routing table
python ip_rotator.py vpn route list
```

## 🔍 VPN Troubleshooting

### Connection Issues

#### Authentication Problems
```bash
# Test authentication
python ip_rotator.py vpn test-auth

# Update credentials
python ip_rotator.py vpn update-credentials \
  --username "new_username" \
  --password "new_password"

# Reset authentication cache
python ip_rotator.py vpn reset-auth-cache
```

#### Network Connectivity
```bash
# Test server reachability
python ip_rotator.py vpn ping-server us-west-1

# Test different ports
python ip_rotator.py vpn test-ports \
  --server us-west-1 \
  --ports "1194,443,80"

# Check firewall issues
python ip_rotator.py vpn check-firewall
```

#### DNS Resolution
```bash
# Test DNS resolution
python ip_rotator.py vpn test-dns

# Flush DNS cache
python ip_rotator.py vpn flush-dns

# Test with different DNS servers
python ip_rotator.py vpn test-dns-servers \
  --servers "8.8.8.8,1.1.1.1,9.9.9.9"
```

### Performance Issues

#### Speed Optimization
```bash
# Run speed test
python ip_rotator.py vpn speed-test

# Find fastest servers
python ip_rotator.py vpn optimize-speed

# Test different protocols
python ip_rotator.py vpn compare-protocols

# Optimize MTU size
python ip_rotator.py vpn optimize-mtu
```

#### Connection Stability
```bash
# Test connection stability
python ip_rotator.py vpn stability-test --duration 3600

# Monitor for disconnections
python ip_rotator.py vpn monitor-stability

# Check for packet loss
python ip_rotator.py vpn packet-loss-test
```

### Diagnostic Tools

#### VPN Diagnostics
```bash
# Comprehensive VPN diagnostics
python ip_rotator.py vpn diagnose

# Generate VPN report
python ip_rotator.py vpn generate-report

# Export logs for analysis
python ip_rotator.py vpn export-logs --days 7

# Check system compatibility
python ip_rotator.py vpn check-compatibility
```

#### Network Analysis
```bash
# Analyze network routes
python ip_rotator.py vpn analyze-routes

# Check for IP leaks
python ip_rotator.py vpn leak-test

# Monitor network interfaces
python ip_rotator.py vpn monitor-interfaces

# Test WebRTC protection
python ip_rotator.py vpn test-webrtc-protection
```

## 📋 VPN Configuration Templates

### High Security Template
```json
{
    "security_profile": "high",
    "protocol": "openvpn",
    "cipher": "AES-256-GCM",
    "auth": "SHA512",
    "kill_switch": true,
    "dns_leak_protection": true,
    "ipv6_disable": true,
    "webrtc_protection": true,
    "auto_connect": true,
    "auto_reconnect": true
}
```

### High Performance Template
```json
{
    "performance_profile": "high",
    "protocol": "wireguard",
    "mtu": 1420,
    "compression": false,
    "tcp_nodelay": true,
    "server_selection": "fastest",
    "load_balance": true,
    "max_load": 70
}
```

### Streaming Template
```json
{
    "streaming_profile": true,
    "required_features": ["streaming"],
    "preferred_countries": ["US", "UK"],
    "smart_location": true,
    "auto_optimize": true,
    "bandwidth_priority": "high"
}
```

### Gaming Template
```json
{
    "gaming_profile": true,
    "low_latency": true,
    "server_selection": "lowest_ping",
    "auto_optimize_latency": true,
    "gaming_acceleration": true,
    "split_tunnel": {
        "enabled": true,
        "gaming_apps_only": true
    }
}
```

## 🔧 Command Reference Quick Card

### Essential VPN Commands
| Command | Description | Example |
|---------|-------------|---------|
| `vpn connect` | Connect to VPN | `vpn connect --country US` |
| `vpn disconnect` | Disconnect VPN | `vpn disconnect` |
| `vpn status` | Show status | `vpn status --detailed` |
| `vpn rotate` | Change server | `vpn rotate --same-country` |
| `vpn list-servers` | List servers | `vpn list-servers --country UK` |
| `vpn speed-test` | Test speed | `vpn speed-test us-west-1` |

### Configuration Commands
| Command | Description | Example |
|---------|-------------|---------|
| `vpn add-provider` | Add provider | `vpn add-provider --name nordvpn` |
| `vpn import-config` | Import config | `vpn import-config client.ovpn` |
| `vpn set-auth` | Set credentials | `vpn set-auth user pass` |
| `vpn auto-rotate` | Auto rotation | `vpn auto-rotate --interval 30m` |

---

**Next**: [Proxy Management](08-proxy-management.md) | [Back to Manual](README.md)
