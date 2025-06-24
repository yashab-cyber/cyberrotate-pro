# Tor Integration

Comprehensive guide to using Tor network features in CyberRotate Pro for maximum anonymity and privacy.

## 🧅 Tor Network Overview

The Tor network provides strong anonymity by routing your traffic through multiple encrypted layers via volunteer-operated relays worldwide.

### How Tor Works
1. **Entry Guard**: First relay that sees your real IP
2. **Middle Relay**: Intermediate relay for additional encryption layers
3. **Exit Relay**: Final relay that accesses the destination website
4. **Onion Routing**: Multiple encryption layers like an onion

### Tor Benefits
- **Strong Anonymity**: Multiple encryption layers
- **No Logs**: Tor network doesn't log user activity
- **Censorship Resistance**: Difficult to block completely
- **Free to Use**: No subscription fees required
- **Global Network**: Thousands of volunteer relays

### Tor Limitations
- **Slower Speeds**: Multiple hops add latency
- **Exit Node Risks**: Unencrypted traffic visible to exit relay
- **Some Sites Block Tor**: Anti-abuse measures
- **Not Bulletproof**: Advanced attacks possible

## ⚙️ Tor Installation & Setup

### System Requirements
- **Operating System**: Windows, Linux, macOS
- **RAM**: 256MB minimum, 512MB recommended
- **Storage**: 50MB for Tor installation
- **Network**: Unrestricted internet access (or bridge support)

### Method 1: Automatic Installation
```bash
# Install Tor automatically
python ip_rotator.py tor install

# Install with specific version
python ip_rotator.py tor install --version 0.4.8.8

# Install with obfuscation support
python ip_rotator.py tor install --with-bridges
```

### Method 2: Manual Installation

#### Windows Installation
```powershell
# Download and install Tor Browser (includes Tor)
# Or install via Chocolatey
choco install tor

# Verify installation
tor --version
```

#### Linux Installation
```bash
# Ubuntu/Debian
sudo apt update
sudo apt install tor

# CentOS/RHEL
sudo yum install tor

# Fedora
sudo dnf install tor

# Arch Linux
sudo pacman -S tor

# Verify installation
tor --version
```

#### macOS Installation
```bash
# Using Homebrew
brew install tor

# Using MacPorts
sudo port install tor

# Verify installation
tor --version
```

### Method 3: Tor Browser Integration
```bash
# Use existing Tor Browser installation
python ip_rotator.py tor configure --use-tor-browser

# Specify Tor Browser path
python ip_rotator.py tor configure \
  --tor-browser-path "/Applications/Tor Browser.app"

# Extract Tor from Tor Browser
python ip_rotator.py tor extract-from-browser
```

## 🔧 Tor Configuration

### Basic Configuration
```bash
# Initialize Tor configuration
python ip_rotator.py tor init

# Set basic options
python ip_rotator.py config set tor.socks_port 9150
python ip_rotator.py config set tor.control_port 9151
python ip_rotator.py config set tor.data_directory "/var/lib/tor"

# Enable control port authentication
python ip_rotator.py config set tor.control_password "your_password"
python ip_rotator.py config set tor.cookie_authentication true
```

### Advanced Configuration Options

#### Network Settings
```bash
# Configure network timeouts
python ip_rotator.py config set tor.circuit_build_timeout 60
python ip_rotator.py config set tor.new_circuit_timeout 30

# Set bandwidth limits
python ip_rotator.py config set tor.bandwidth_rate "1 MB"
python ip_rotator.py config set tor.bandwidth_burst "2 MB"

# Configure connections
python ip_rotator.py config set tor.max_circuit_dirtiness 600
python ip_rotator.py config set tor.max_streams_per_circuit 10
```

#### Security Settings
```bash
# Enhanced security options
python ip_rotator.py config set tor.enforce_distinct_subnets true
python ip_rotator.py config set tor.strict_nodes true
python ip_rotator.py config set tor.fascist_firewall true

# Disable risky features
python ip_rotator.py config set tor.disable_predicates true
python ip_rotator.py config set tor.disable_network true  # For offline config
```

#### Logging Configuration
```bash
# Set logging levels
python ip_rotator.py config set tor.log_level "notice"
python ip_rotator.py config set tor.log_file "/var/log/tor.log"

# Enable specific log categories
python ip_rotator.py config set tor.log_categories "general,circ,conn"

# Disable logging (for privacy)
python ip_rotator.py config set tor.disable_logging true
```

### Configuration File Management
```bash
# Generate torrc file
python ip_rotator.py tor generate-config

# Edit torrc file
python ip_rotator.py tor edit-config

# Validate configuration
python ip_rotator.py tor validate-config

# Backup configuration
python ip_rotator.py tor backup-config
```

## 🌉 Bridge Configuration

Bridges help bypass Tor blocking in censored networks.

### Built-in Bridge Types

#### obfs4 Bridges (Recommended)
```bash
# Enable obfs4 bridges
python ip_rotator.py tor bridges enable --type obfs4

# Use built-in obfs4 bridges
python ip_rotator.py tor bridges use-builtin obfs4

# Request new obfs4 bridges
python ip_rotator.py tor bridges request --type obfs4 --count 3
```

#### Other Bridge Types
```bash
# Enable different bridge types
python ip_rotator.py tor bridges enable --type obfs3
python ip_rotator.py tor bridges enable --type scramblesuit
python ip_rotator.py tor bridges enable --type fte
python ip_rotator.py tor bridges enable --type meek
```

### Custom Bridge Configuration

#### Adding Manual Bridges
```bash
# Add single bridge
python ip_rotator.py tor bridges add \
  "obfs4 203.0.113.1:443 FINGERPRINT cert=CERTIFICATE"

# Import bridges from file
python ip_rotator.py tor bridges import bridges.txt

# Import from BridgeDB email
python ip_rotator.py tor bridges import-email bridges_email.txt
```

#### Bridge Testing
```bash
# Test bridge connectivity
python ip_rotator.py tor bridges test

# Test specific bridge
python ip_rotator.py tor bridges test \
  "obfs4 203.0.113.1:443 FINGERPRINT"

# Remove non-working bridges
python ip_rotator.py tor bridges cleanup
```

### Obtaining Bridges

#### BridgeDB Service
```bash
# Request bridges via email
# Send email to bridges@torproject.org with "get bridges" in body

# Request via website
# Visit https://bridges.torproject.org/

# Import received bridges
python ip_rotator.py tor bridges import-bridgedb response.txt
```

#### Social Media Bridges
```bash
# Telegram bot: @GetBridgesBot
# Twitter: @GetBridges

# Import from social media
python ip_rotator.py tor bridges import-social response.txt
```

## 🚀 Tor Operations

### Starting and Stopping Tor

#### Basic Operations
```bash
# Start Tor service
python ip_rotator.py tor start

# Start with specific configuration
python ip_rotator.py tor start --config custom-torrc

# Start in background/daemon mode
python ip_rotator.py tor start --daemon

# Stop Tor service
python ip_rotator.py tor stop

# Restart Tor service
python ip_rotator.py tor restart

# Check Tor status
python ip_rotator.py tor status
```

#### Advanced Start Options
```bash
# Start with bridges
python ip_rotator.py tor start --use-bridges

# Start with specific entry guards
python ip_rotator.py tor start --entry-guards "US,UK,DE"

# Start with exit node preferences
python ip_rotator.py tor start --exit-nodes "US,UK"

# Start with excluded nodes
python ip_rotator.py tor start --exclude-nodes "CN,RU,IR"
```

### Circuit Management

#### Creating New Circuits
```bash
# Create new circuit (new IP)
python ip_rotator.py tor new-circuit

# Create circuit for specific destination
python ip_rotator.py tor new-circuit --target "example.com"

# Create circuit with country preferences
python ip_rotator.py tor new-circuit --exit-country "US"

# Force new circuit for all streams
python ip_rotator.py tor new-circuit --all-streams
```

#### Circuit Information
```bash
# List active circuits
python ip_rotator.py tor list-circuits

# Show circuit details
python ip_rotator.py tor circuit-info

# Monitor circuit building
python ip_rotator.py tor monitor-circuits

# Export circuit information
python ip_rotator.py tor export-circuits --format json
```

#### Circuit Control
```bash
# Close specific circuit
python ip_rotator.py tor close-circuit CIRCUIT_ID

# Close all circuits
python ip_rotator.py tor close-all-circuits

# Extend circuit
python ip_rotator.py tor extend-circuit CIRCUIT_ID RELAY_FINGERPRINT
```

### Stream Management
```bash
# List active streams
python ip_rotator.py tor list-streams

# Attach stream to circuit
python ip_rotator.py tor attach-stream STREAM_ID CIRCUIT_ID

# Close stream
python ip_rotator.py tor close-stream STREAM_ID
```

## 🔄 Tor IP Rotation

### Manual Rotation
```bash
# Get new Tor identity (new IP)
python ip_rotator.py tor new-identity

# Force immediate rotation
python ip_rotator.py tor rotate --force

# Rotate with exit country preference
python ip_rotator.py tor rotate --exit-country "UK"

# Rotate avoiding specific countries
python ip_rotator.py tor rotate --avoid-countries "CN,RU"
```

### Automatic Rotation
```bash
# Start automatic rotation (every 10 minutes)
python ip_rotator.py tor auto-rotate --interval 10m

# Rotate on specific conditions
python ip_rotator.py tor auto-rotate \
  --interval 15m \
  --on-new-stream true \
  --max-streams 50

# Country-based automatic rotation
python ip_rotator.py tor auto-rotate \
  --interval 20m \
  --preferred-countries "US,UK,DE,CA,AU" \
  --random-order

# Stop automatic rotation
python ip_rotator.py tor auto-rotate --stop
```

### Scheduled Rotation
```bash
# Schedule rotation at specific times
python ip_rotator.py tor schedule \
  --time "09:00,13:00,17:00,21:00" \
  --action "new-identity"

# Schedule daily rotation
python ip_rotator.py tor schedule \
  --daily "02:00" \
  --action "restart"

# Schedule hourly circuit refresh
python ip_rotator.py tor schedule \
  --hourly \
  --action "new-circuit"
```

## 🛡️ Tor Security Features

### Node Selection

#### Entry Guard Configuration
```bash
# Set number of entry guards
python ip_rotator.py config set tor.num_entry_guards 3

# Set entry guard lifetime
python ip_rotator.py config set tor.guard_lifetime 90

# Prefer specific countries for entry
python ip_rotator.py config set tor.entry_nodes "US,UK,DE"

# Exclude countries from entry
python ip_rotator.py config set tor.exclude_entry_nodes "CN,RU,IR"
```

#### Exit Node Control
```bash
# Set preferred exit nodes
python ip_rotator.py config set tor.exit_nodes "US,UK,DE"

# Exclude exit nodes
python ip_rotator.py config set tor.exclude_exit_nodes "CN,RU,IR"

# Use specific exit node
python ip_rotator.py tor set-exit-node RELAY_FINGERPRINT

# Allow only certain exit ports
python ip_rotator.py config set tor.exit_policy "accept 80,443,993,995"
```

#### Middle Relay Preferences
```bash
# Set middle node preferences
python ip_rotator.py config set tor.middle_nodes "US,UK,DE,CA,AU"

# Exclude middle nodes
python ip_rotator.py config set tor.exclude_middle_nodes "CN,RU,IR"

# Ensure diverse path
python ip_rotator.py config set tor.enforce_distinct_subnets true
```

### Traffic Isolation

#### Stream Isolation
```bash
# Enable stream isolation
python ip_rotator.py config set tor.isolate_streams true

# Isolate by destination port
python ip_rotator.py config set tor.isolate_dest_port true

# Isolate by destination address
python ip_rotator.py config set tor.isolate_dest_addr true

# Isolate by client protocol
python ip_rotator.py config set tor.isolate_socks_auth true
```

#### Application Isolation
```bash
# Create isolated SOCKS ports for different applications
python ip_rotator.py tor create-isolated-port \
  --port 9152 \
  --name "browser" \
  --isolation-flags "IsolateDestAddr,IsolateDestPort"

python ip_rotator.py tor create-isolated-port \
  --port 9153 \
  --name "email" \
  --isolation-flags "IsolateDestAddr"
```

### Hidden Service Protection
```bash
# Disable hidden service descriptor publishing
python ip_rotator.py config set tor.publish_hid_serv_descriptors false

# Disable hidden service directory requests
python ip_rotator.py config set tor.fetch_hid_serv_descriptors false

# Block .onion domains (if not needed)
python ip_rotator.py config set tor.block_onion_domains true
```

## 🌐 Tor Application Integration

### SOCKS Proxy Configuration

#### Basic SOCKS Setup
```bash
# Configure applications to use Tor SOCKS proxy
# Default: 127.0.0.1:9150 (Tor Browser)
# Default: 127.0.0.1:9050 (Tor service)

# Check SOCKS port
python ip_rotator.py tor info --socks-port

# Test SOCKS proxy
python ip_rotator.py tor test-socks
```

#### Browser Configuration
```bash
# Configure browser proxy settings
# Firefox: about:preferences#general -> Network Settings
# Chrome: --proxy-server="socks5://127.0.0.1:9150"

# Generate browser configuration
python ip_rotator.py tor generate-browser-config --browser firefox
python ip_rotator.py tor generate-browser-config --browser chrome
```

#### Application-specific Configuration
```bash
# Configure curl
curl --socks5 127.0.0.1:9150 http://check.torproject.org/

# Configure wget
wget --socks-5-hostname=127.0.0.1:9150 http://check.torproject.org/

# Configure git
git config --global http.proxy socks5://127.0.0.1:9150
```

### DNS over Tor

#### DNS Configuration
```bash
# Enable DNS port (for DNS over Tor)
python ip_rotator.py config set tor.dns_port 5353

# Configure DNS resolution
python ip_rotator.py config set tor.auto_map_hosts_on_resolve true

# Test DNS over Tor
python ip_rotator.py tor test-dns google.com
```

#### System DNS Configuration
```bash
# Configure system to use Tor DNS (Linux)
echo "nameserver 127.0.0.1:5353" | sudo tee /etc/resolv.conf

# Configure system DNS (Windows)
# Network Settings -> Change adapter settings -> DNS servers: 127.0.0.1
```

## 📊 Tor Monitoring & Analysis

### Real-time Monitoring
```bash
# Monitor Tor connection
python ip_rotator.py tor monitor

# Monitor with specific metrics
python ip_rotator.py tor monitor \
  --metrics "bandwidth,circuits,streams" \
  --interval 30

# Monitor circuit changes
python ip_rotator.py tor monitor-circuits --follow

# Export monitoring data
python ip_rotator.py tor monitor --export monitor.json
```

### Performance Analysis
```bash
# Test Tor performance
python ip_rotator.py tor performance-test

# Speed test through Tor
python ip_rotator.py tor speed-test

# Latency analysis
python ip_rotator.py tor latency-test --samples 10

# Bandwidth usage statistics
python ip_rotator.py tor bandwidth-stats
```

### Network Information
```bash
# Show current Tor circuit
python ip_rotator.py tor current-circuit

# Display exit node information
python ip_rotator.py tor exit-node-info

# Check Tor network status
python ip_rotator.py tor network-status

# Consensus information
python ip_rotator.py tor consensus-info
```

## 🔍 Tor Troubleshooting

### Connection Issues

#### Tor Won't Start
```bash
# Check Tor installation
which tor  # Linux/macOS
where tor  # Windows

# Verify configuration
python ip_rotator.py tor validate-config

# Check port conflicts
python ip_rotator.py tor check-ports

# Debug Tor startup
python ip_rotator.py tor start --debug
```

#### Bootstrap Problems
```bash
# Check bootstrap progress
python ip_rotator.py tor bootstrap-status

# Force bootstrap retry
python ip_rotator.py tor force-bootstrap

# Clear Tor state and restart
python ip_rotator.py tor reset-state

# Use bridges if blocked
python ip_rotator.py tor start --use-bridges
```

#### Circuit Building Issues
```bash
# Debug circuit building
python ip_rotator.py tor debug-circuits

# Test relay connectivity
python ip_rotator.py tor test-relays

# Check relay consensus
python ip_rotator.py tor check-consensus

# Rebuild circuits
python ip_rotator.py tor rebuild-circuits
```

### Performance Issues

#### Slow Connections
```bash
# Optimize circuit selection
python ip_rotator.py tor optimize-circuits

# Test different guard nodes
python ip_rotator.py tor test-guards

# Increase circuit timeout
python ip_rotator.py config set tor.circuit_build_timeout 120

# Enable faster circuit building
python ip_rotator.py config set tor.learn_circuit_build_timeout true
```

#### Frequent Disconnections
```bash
# Increase circuit lifetime
python ip_rotator.py config set tor.max_circuit_dirtiness 1800

# Improve connection stability
python ip_rotator.py config set tor.circuit_stream_timeout 30

# Monitor for network issues
python ip_rotator.py tor network-monitor --duration 3600
```

### Security Diagnostics

#### Check for Leaks
```bash
# Test for IP leaks
python ip_rotator.py tor test-ip-leak

# Check DNS leaks
python ip_rotator.py tor test-dns-leak

# Verify Tor usage
python ip_rotator.py tor verify-connection

# Comprehensive security test
python ip_rotator.py tor security-test
```

#### Verify Anonymity
```bash
# Check current exit node
python ip_rotator.py tor check-exit-node

# Verify circuit path diversity
python ip_rotator.py tor verify-path-diversity

# Test for timing correlation attacks
python ip_rotator.py tor test-timing-correlation
```

## 🔧 Advanced Tor Features

### Custom Tor Builds
```bash
# Compile Tor from source
python ip_rotator.py tor compile-from-source

# Install experimental features
python ip_rotator.py tor install-experimental

# Configure alpha/beta versions
python ip_rotator.py tor use-version --version alpha
```

### Tor Research Features
```bash
# Enable experimental features
python ip_rotator.py config set tor.experimental_features true

# Use research consensus
python ip_rotator.py config set tor.use_research_consensus true

# Enable circuit padding
python ip_rotator.py config set tor.circuit_padding true
```

### Integration with Other Tools
```bash
# Combine with VPN (Tor over VPN)
python ip_rotator.py tor start --over-vpn

# Combine with proxy (Tor over Proxy)
python ip_rotator.py tor start --over-proxy proxy.example.com:8080

# Chain with multiple tools
python ip_rotator.py start-chain --order "vpn,tor,proxy"
```

## 📋 Tor Command Reference

### Essential Tor Commands
| Command | Description | Example |
|---------|-------------|---------|
| `tor start` | Start Tor service | `tor start --use-bridges` |
| `tor stop` | Stop Tor service | `tor stop` |
| `tor status` | Check Tor status | `tor status --detailed` |
| `tor new-identity` | Get new IP | `tor new-identity` |
| `tor new-circuit` | Create new circuit | `tor new-circuit --exit-country US` |
| `tor bridges enable` | Enable bridges | `tor bridges enable --type obfs4` |

### Configuration Commands
| Command | Description | Example |
|---------|-------------|---------|
| `tor init` | Initialize config | `tor init` |
| `tor generate-config` | Create torrc | `tor generate-config` |
| `tor validate-config` | Check config | `tor validate-config` |
| `tor auto-rotate` | Auto rotation | `tor auto-rotate --interval 10m` |

### Monitoring Commands
| Command | Description | Example |
|---------|-------------|---------|
| `tor monitor` | Monitor Tor | `tor monitor --metrics all` |
| `tor list-circuits` | Show circuits | `tor list-circuits` |
| `tor performance-test` | Test performance | `tor performance-test` |
| `tor security-test` | Security check | `tor security-test` |

---

**Next**: [Security Features](10-security.md) | [Back to Manual](README.md)
