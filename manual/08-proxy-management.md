# Proxy Management

Complete guide to configuring, managing, and optimizing proxy connections in CyberRotate Pro.

## 🌐 Proxy Overview

CyberRotate Pro supports various proxy types and provides advanced management features for reliable IP rotation.

### Supported Proxy Types

#### HTTP/HTTPS Proxies
- **HTTP Proxies**: Basic web traffic proxying
- **HTTPS Proxies**: Encrypted web traffic support
- **Transparent Proxies**: No authentication required
- **Anonymous Proxies**: Hide your IP but identify as proxy
- **Elite Proxies**: Complete anonymity, no proxy detection

#### SOCKS Proxies
- **SOCKS4**: Basic TCP connection proxying
- **SOCKS5**: Advanced features with UDP and authentication
- **SOCKS5 with Auth**: Username/password authentication
- **Residential SOCKS**: Real ISP IP addresses
- **Datacenter SOCKS**: Fast datacenter connections

#### Specialized Proxies
- **Rotating Proxies**: Automatic IP rotation
- **Sticky Proxies**: Session persistence
- **Mobile Proxies**: Mobile network IPs
- **ISP Proxies**: Internet Service Provider IPs

## ⚙️ Proxy Configuration

### Method 1: Interactive Setup Wizard

```bash
# Start proxy setup wizard
python ip_rotator.py proxy setup-wizard

# Follow prompts:
# 1. Choose proxy type
# 2. Enter proxy details
# 3. Set authentication
# 4. Configure rotation settings
# 5. Test connection
```

### Method 2: Manual Proxy Addition

#### Single Proxy Setup
```bash
# Add HTTP proxy
python ip_rotator.py proxy add \
  --host "proxy.example.com" \
  --port 8080 \
  --type http \
  --username "user" \
  --password "pass"

# Add SOCKS5 proxy
python ip_rotator.py proxy add \
  --host "socks.example.com" \
  --port 1080 \
  --type socks5 \
  --username "sockuser" \
  --password "sockpass"

# Add proxy without authentication
python ip_rotator.py proxy add \
  --host "free-proxy.com" \
  --port 3128 \
  --type http
```

#### Bulk Proxy Import
```bash
# Import from text file (IP:PORT format)
python ip_rotator.py proxy import proxies.txt

# Import with authentication (IP:PORT:USER:PASS)
python ip_rotator.py proxy import auth-proxies.txt --format auth

# Import from CSV file
python ip_rotator.py proxy import proxies.csv --format csv

# Import from URL
python ip_rotator.py proxy import --url "http://provider.com/proxies.txt"
```

### Method 3: Configuration File Setup

#### Proxy Configuration Template
```json
{
    "proxies": {
        "providers": [
            {
                "name": "provider1",
                "type": "http",
                "rotation_list": [
                    {
                        "host": "proxy1.example.com",
                        "port": 8080,
                        "username": "user1",
                        "password": "pass1",
                        "country": "US",
                        "region": "west"
                    },
                    {
                        "host": "proxy2.example.com", 
                        "port": 8080,
                        "username": "user2",
                        "password": "pass2",
                        "country": "UK",
                        "region": "london"
                    }
                ]
            }
        ],
        "rotation": {
            "method": "random",
            "interval": 300,
            "max_failures": 3,
            "test_before_use": true
        },
        "authentication": {
            "timeout": 30,
            "retry_attempts": 2
        }
    }
}
```

Load configuration:
```bash
python ip_rotator.py proxy load-config proxy-config.json
```

## 📂 Proxy List Management

### Importing Proxy Lists

#### File Formats

**Basic Format (IP:PORT)**
```
192.168.1.100:8080
203.0.113.1:3128
198.51.100.50:1080
```

**Authentication Format (IP:PORT:USER:PASS)**
```
proxy1.com:8080:username1:password1
proxy2.com:8080:username2:password2
proxy3.com:1080:sockuser:sockpass
```

**CSV Format**
```csv
host,port,type,username,password,country,speed
proxy1.com,8080,http,user1,pass1,US,high
proxy2.com,1080,socks5,user2,pass2,UK,medium
proxy3.com,3128,http,,,,US,low
```

**JSON Format**
```json
[
    {
        "host": "proxy1.example.com",
        "port": 8080,
        "type": "http",
        "username": "user1",
        "password": "pass1",
        "country": "US",
        "speed": "high",
        "anonymity": "elite"
    }
]
```

#### Import Commands
```bash
# Import with automatic format detection
python ip_rotator.py proxy import proxies.txt --auto-detect

# Import specific format
python ip_rotator.py proxy import proxies.csv --format csv

# Import with testing
python ip_rotator.py proxy import proxies.txt --test-all --remove-dead

# Import with filtering
python ip_rotator.py proxy import proxies.txt --country US --type http

# Import with custom settings
python ip_rotator.py proxy import proxies.txt \
  --timeout 15 \
  --max-response-time 5000 \
  --anonymity-level elite
```

### Proxy List Organization

#### Categories and Tags
```bash
# Create proxy categories
python ip_rotator.py proxy category create "premium" 
python ip_rotator.py proxy category create "datacenter"
python ip_rotator.py proxy category create "residential"

# Add proxies to categories
python ip_rotator.py proxy category add premium proxy1.com:8080
python ip_rotator.py proxy category add datacenter proxy2.com:3128

# Tag proxies for organization
python ip_rotator.py proxy tag add proxy1.com:8080 "fast,reliable,US"
python ip_rotator.py proxy tag add proxy2.com:8080 "streaming,UK"

# List proxies by category
python ip_rotator.py proxy list --category premium
python ip_rotator.py proxy list --tags "fast,reliable"
```

#### Proxy Pools
```bash
# Create proxy pools
python ip_rotator.py proxy pool create "web-scraping" \
  --description "High-speed proxies for web scraping"

# Add proxies to pool
python ip_rotator.py proxy pool add web-scraping \
  --proxies proxy1.com:8080,proxy2.com:3128

# Set pool rotation settings
python ip_rotator.py proxy pool configure web-scraping \
  --rotation-method random \
  --interval 60 \
  --failure-threshold 3

# Use specific pool
python ip_rotator.py proxy connect --pool web-scraping
```

## 🔄 Proxy Rotation

### Manual Rotation
```bash
# Rotate to next proxy
python ip_rotator.py proxy rotate

# Rotate within same country
python ip_rotator.py proxy rotate --same-country

# Rotate to specific country
python ip_rotator.py proxy rotate --country UK

# Rotate with specific type
python ip_rotator.py proxy rotate --type socks5

# Force rotation (ignore timing)
python ip_rotator.py proxy rotate --force
```

### Automatic Rotation
```bash
# Start auto-rotation (every 5 minutes)
python ip_rotator.py proxy auto-rotate --interval 5m

# Auto-rotate with conditions
python ip_rotator.py proxy auto-rotate \
  --interval 10m \
  --on-failure true \
  --max-requests 100 \
  --max-errors 5

# Country-based rotation
python ip_rotator.py proxy auto-rotate \
  --interval 15m \
  --countries "US,UK,DE,CA" \
  --random-order

# Stop auto-rotation
python ip_rotator.py proxy auto-rotate --stop
```

### Advanced Rotation Strategies

#### Smart Rotation
```bash
# Enable intelligent rotation
python ip_rotator.py config set proxy.smart_rotation true

# Configure smart rotation parameters
python ip_rotator.py config set proxy.smart_rotation.failure_threshold 3
python ip_rotator.py config set proxy.smart_rotation.speed_threshold 2000
python ip_rotator.py config set proxy.smart_rotation.success_rate_threshold 90
```

#### Load Balancing
```bash
# Enable load balancing
python ip_rotator.py config set proxy.load_balancing true

# Set load balancing method
python ip_rotator.py config set proxy.load_balancing.method "round_robin"
# Options: round_robin, least_connections, weighted, random

# Configure weights for different proxy types
python ip_rotator.py proxy set-weight premium --weight 5
python ip_rotator.py proxy set-weight datacenter --weight 3
python ip_rotator.py proxy set-weight free --weight 1
```

## 🧪 Proxy Testing & Validation

### Individual Proxy Testing
```bash
# Test single proxy
python ip_rotator.py proxy test proxy.example.com:8080

# Test with specific target
python ip_rotator.py proxy test proxy.example.com:8080 \
  --target "http://httpbin.org/ip"

# Test proxy anonymity
python ip_rotator.py proxy test-anonymity proxy.example.com:8080

# Test proxy speed
python ip_rotator.py proxy speed-test proxy.example.com:8080
```

### Bulk Testing
```bash
# Test all proxies
python ip_rotator.py proxy test-all

# Test with threading for speed
python ip_rotator.py proxy test-all --threads 20

# Test and remove dead proxies
python ip_rotator.py proxy test-all --remove-dead

# Test specific category
python ip_rotator.py proxy test-category premium

# Test by country
python ip_rotator.py proxy test-country US
```

### Advanced Testing Options
```bash
# Comprehensive proxy analysis
python ip_rotator.py proxy analyze proxy.example.com:8080

# Test proxy headers and anonymity
python ip_rotator.py proxy test-headers proxy.example.com:8080

# Check for proxy transparency
python ip_rotator.py proxy test-transparency proxy.example.com:8080

# Verify proxy location
python ip_rotator.py proxy verify-location proxy.example.com:8080
```

## 📊 Proxy Performance Monitoring

### Real-time Monitoring
```bash
# Monitor proxy performance
python ip_rotator.py proxy monitor

# Monitor with specific interval
python ip_rotator.py proxy monitor --interval 30

# Monitor specific proxy
python ip_rotator.py proxy monitor proxy.example.com:8080

# Monitor and alert on issues
python ip_rotator.py proxy monitor --alert-threshold 5000ms
```

### Performance Metrics
```bash
# Show proxy statistics
python ip_rotator.py proxy stats

# Detailed performance report
python ip_rotator.py proxy performance-report

# Export metrics to file
python ip_rotator.py proxy stats --export metrics.json

# Compare proxy performance
python ip_rotator.py proxy compare \
  proxy1.com:8080 proxy2.com:3128 proxy3.com:1080
```

### Health Checks
```bash
# Enable automatic health checks
python ip_rotator.py config set proxy.health_checks true

# Configure health check frequency
python ip_rotator.py config set proxy.health_check_interval 300

# Set health check targets
python ip_rotator.py config set proxy.health_check_urls \
  "http://httpbin.org/ip,https://api.ipify.org"

# Manual health check
python ip_rotator.py proxy health-check --all
```

## 🔧 Proxy Authentication

### Authentication Methods

#### Username/Password Authentication
```bash
# Set authentication for proxy
python ip_rotator.py proxy set-auth proxy.example.com:8080 \
  --username "myuser" \
  --password "mypass"

# Bulk authentication update
python ip_rotator.py proxy bulk-auth \
  --file auth-credentials.txt \
  --format "host:port:user:pass"

# Test authentication
python ip_rotator.py proxy test-auth proxy.example.com:8080
```

#### IP Authentication
```bash
# Configure IP-based authentication
python ip_rotator.py proxy set-ip-auth \
  --proxy-provider "provider1" \
  --authorized-ip "203.0.113.1"

# Whitelist current IP
python ip_rotator.py proxy whitelist-current-ip \
  --provider "provider1"

# Check IP authorization status
python ip_rotator.py proxy check-ip-auth
```

#### API Key Authentication
```bash
# Set API key for proxy provider
python ip_rotator.py proxy set-api-key \
  --provider "provider1" \
  --api-key "your-api-key-here"

# Rotate API endpoint authentication
python ip_rotator.py proxy api-auth \
  --endpoint "https://provider1.com/api/rotate" \
  --api-key "your-api-key"
```

### Authentication Management
```bash
# Store credentials securely
python ip_rotator.py proxy credentials store \
  --file encrypted-creds.enc \
  --password "master-password"

# Load stored credentials
python ip_rotator.py proxy credentials load \
  --file encrypted-creds.enc \
  --password "master-password"

# Update credentials in bulk
python ip_rotator.py proxy credentials update \
  --provider "provider1" \
  --username "new-user" \
  --password "new-pass"
```

## 🛠️ Proxy Configuration Options

### Connection Settings
```bash
# Set proxy timeout
python ip_rotator.py config set proxy.timeout 30

# Configure retry attempts
python ip_rotator.py config set proxy.retry_attempts 3
python ip_rotator.py config set proxy.retry_delay 5

# Set connection pool size
python ip_rotator.py config set proxy.max_connections 10

# Configure keep-alive
python ip_rotator.py config set proxy.keep_alive true
python ip_rotator.py config set proxy.keep_alive_timeout 60
```

### Traffic Management
```bash
# Set request headers
python ip_rotator.py config set proxy.default_headers '{
  "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
  "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
  "Accept-Language": "en-US,en;q=0.5",
  "Accept-Encoding": "gzip, deflate"
}'

# Configure SSL settings
python ip_rotator.py config set proxy.ssl_verify false
python ip_rotator.py config set proxy.ssl_cert_file "/path/to/cert.pem"

# Set proxy tunneling
python ip_rotator.py config set proxy.tunnel_mode "CONNECT"
```

### Filtering and Selection
```bash
# Set proxy selection criteria
python ip_rotator.py config set proxy.selection.min_speed 1000
python ip_rotator.py config set proxy.selection.max_response_time 5000
python ip_rotator.py config set proxy.selection.min_success_rate 85

# Geographic filtering
python ip_rotator.py config set proxy.geo_filter.allowed_countries "US,UK,DE,CA"
python ip_rotator.py config set proxy.geo_filter.blocked_countries "CN,RU,IR"

# Provider filtering
python ip_rotator.py config set proxy.provider_filter.preferred "provider1,provider2"
python ip_rotator.py config set proxy.provider_filter.blocked "bad-provider"
```

## 🔍 Proxy Troubleshooting

### Connection Issues

#### Authentication Failures
```bash
# Test proxy authentication
python ip_rotator.py proxy test-auth proxy.example.com:8080

# Debug authentication process
python ip_rotator.py proxy debug-auth proxy.example.com:8080 --verbose

# Check credential validity
python ip_rotator.py proxy verify-credentials --provider "provider1"

# Reset authentication cache
python ip_rotator.py proxy reset-auth-cache
```

#### Network Connectivity
```bash
# Test proxy connectivity
python ip_rotator.py proxy ping proxy.example.com:8080

# Test with different protocols
python ip_rotator.py proxy test-protocols proxy.example.com:8080

# Check firewall/ISP blocking
python ip_rotator.py proxy check-blocking proxy.example.com:8080

# Trace connection path
python ip_rotator.py proxy traceroute proxy.example.com:8080
```

#### Performance Issues
```bash
# Diagnose slow proxies
python ip_rotator.py proxy diagnose-slow

# Test proxy bandwidth
python ip_rotator.py proxy bandwidth-test proxy.example.com:8080

# Check for throttling
python ip_rotator.py proxy check-throttling proxy.example.com:8080

# Optimize proxy selection
python ip_rotator.py proxy optimize-selection
```

### Quality Control

#### Dead Proxy Removal
```bash
# Find and remove dead proxies
python ip_rotator.py proxy cleanup --remove-dead

# Remove slow proxies
python ip_rotator.py proxy cleanup --remove-slow --threshold 10000

# Remove unreliable proxies
python ip_rotator.py proxy cleanup --remove-unreliable --success-rate 70

# Comprehensive cleanup
python ip_rotator.py proxy cleanup --comprehensive
```

#### Proxy Validation
```bash
# Validate proxy list integrity
python ip_rotator.py proxy validate-list

# Check for duplicate proxies
python ip_rotator.py proxy find-duplicates --remove

# Verify proxy locations
python ip_rotator.py proxy verify-locations

# Test anonymity levels
python ip_rotator.py proxy test-anonymity-all
```

## 📋 Proxy Provider Integration

### Popular Proxy Providers

#### Rotating Proxy Services
```bash
# Configure Luminati/Bright Data
python ip_rotator.py proxy add-provider \
  --name "luminati" \
  --type "rotating" \
  --endpoint "session-customer.luminati.io:22225" \
  --username "customer-session" \
  --password "password"

# Configure Oxylabs
python ip_rotator.py proxy add-provider \
  --name "oxylabs" \
  --type "residential" \
  --endpoint "residential.oxylabs.io:10000" \
  --username "customer" \
  --password "password"

# Configure Smartproxy
python ip_rotator.py proxy add-provider \
  --name "smartproxy" \
  --type "residential" \
  --endpoint "gate.smartproxy.com:10000" \
  --username "user" \
  --password "password"
```

#### Free Proxy Sources
```bash
# Import from free proxy APIs
python ip_rotator.py proxy import-api \
  --url "https://www.proxy-list.download/api/v1/get?type=http" \
  --format json

# Import from ProxyNova
python ip_rotator.py proxy import-scrape \
  --source "proxynova" \
  --countries "US,UK,DE"

# Import from FreeProxyList
python ip_rotator.py proxy import-scrape \
  --source "freeproxylist" \
  --anonymity "elite"
```

### Custom Provider Integration
```python
# Custom provider plugin example
class CustomProxyProvider:
    def __init__(self, config):
        self.config = config
        
    def get_proxy_list(self):
        # Implement custom proxy fetching logic
        return proxy_list
        
    def rotate_proxy(self):
        # Implement custom rotation logic
        return new_proxy
        
    def test_proxy(self, proxy):
        # Implement custom testing logic
        return test_result

# Register custom provider
python ip_rotator.py proxy register-provider \
  --plugin CustomProxyProvider \
  --config custom-config.json
```

## 📊 Proxy Analytics & Reporting

### Usage Analytics
```bash
# Generate proxy usage report
python ip_rotator.py proxy report --period "last-week"

# Export detailed analytics
python ip_rotator.py proxy analytics --export analytics.json

# Show proxy efficiency metrics
python ip_rotator.py proxy efficiency-report

# Compare provider performance
python ip_rotator.py proxy compare-providers
```

### Success Rate Tracking
```bash
# Track proxy success rates
python ip_rotator.py proxy track-success --enable

# Show success rate statistics
python ip_rotator.py proxy success-stats

# Alert on low success rates
python ip_rotator.py proxy alert-config \
  --success-rate-threshold 80 \
  --email "admin@example.com"
```

## 🔧 Command Reference Quick Card

### Essential Proxy Commands
| Command | Description | Example |
|---------|-------------|---------|
| `proxy add` | Add single proxy | `proxy add --host 1.2.3.4 --port 8080` |
| `proxy import` | Import proxy list | `proxy import proxies.txt` |
| `proxy test` | Test proxy | `proxy test 1.2.3.4:8080` |
| `proxy rotate` | Rotate proxy | `proxy rotate --country US` |
| `proxy list` | List proxies | `proxy list --working` |
| `proxy cleanup` | Remove dead proxies | `proxy cleanup --remove-dead` |

### Management Commands
| Command | Description | Example |
|---------|-------------|---------|
| `proxy test-all` | Test all proxies | `proxy test-all --threads 10` |
| `proxy auto-rotate` | Start auto-rotation | `proxy auto-rotate --interval 5m` |
| `proxy stats` | Show statistics | `proxy stats --export` |
| `proxy monitor` | Monitor performance | `proxy monitor --interval 30` |

---

**Next**: [Tor Integration](09-tor-integration.md) | [Back to Manual](README.md)
