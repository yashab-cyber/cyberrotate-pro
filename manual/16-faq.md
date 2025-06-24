# Frequently Asked Questions (FAQ)

Common questions and answers about CyberRotate Pro usage, features, and troubleshooting.

## 🚀 Getting Started

### Q: What is CyberRotate Pro?
**A:** CyberRotate Pro is a comprehensive IP rotation and network privacy tool that enables automatic switching between VPN servers, proxy servers, and Tor circuits to enhance online anonymity and bypass geo-restrictions.

### Q: What operating systems are supported?
**A:** CyberRotate Pro supports:
- **Windows**: Windows 10, Windows 11
- **Linux**: Ubuntu 18.04+, Debian 10+, CentOS 7+, Fedora 30+
- **macOS**: macOS 10.14 (Mojave) and later

### Q: Do I need administrator/root privileges?
**A:** Some features require elevated privileges:
- **VPN connections**: Usually require admin/root access
- **Kill switch**: Requires firewall modification permissions
- **Network interface management**: May require elevated privileges
- **GUI and API**: Can run with normal user privileges

### Q: Can I use CyberRotate Pro without a VPN subscription?
**A:** Yes! CyberRotate Pro supports:
- **Free VPN services** (limited servers)
- **Proxy-only mode** (using public or private proxies)
- **Tor-only mode** (completely free)
- **Mixed mode** (combining available services)

## 🔧 Installation & Setup

### Q: How do I install Python dependencies?
**A:** Run the following commands:
```bash
# Install all dependencies
pip install -r requirements.txt

# Or install individually
pip install requests psutil tkinter cryptography
```

### Q: What if I get "module not found" errors?
**A:** This usually indicates missing Python packages:
```bash
# Check Python version (must be 3.8+)
python --version

# Install missing modules
pip install module_name

# Use virtual environment (recommended)
python -m venv cyberrotate_env
source cyberrotate_env/bin/activate  # Linux/macOS
cyberrotate_env\Scripts\activate     # Windows
pip install -r requirements.txt
```

### Q: How do I update CyberRotate Pro?
**A:** Updates depend on your installation method:
```bash
# Git repository
git pull origin main
pip install -r requirements.txt

# Manual download
# Download latest version and replace files

# Check for updates
python ip_rotator.py --check-updates
```

## 🌐 VPN Configuration

### Q: Which VPN providers are supported?
**A:** CyberRotate Pro supports:
- **OpenVPN-compatible providers**: NordVPN, ExpressVPN, Surfshark, CyberGhost
- **WireGuard providers**: Mullvad, IVPN, ProtonVPN
- **Custom configurations**: Any OpenVPN or WireGuard config files
- **Free providers**: ProtonVPN Free, Windscribe Free

### Q: How do I add my VPN provider?
**A:** To add a new VPN provider:
```bash
# Method 1: Import config files
python ip_rotator.py vpn import-config your_config.ovpn

# Method 2: Manual configuration
python ip_rotator.py vpn add-provider \
  --name "MyVPN" \
  --protocol openvpn \
  --server vpn.example.com \
  --username your_user \
  --password your_pass

# Method 3: Edit configuration file
python ip_rotator.py config edit vpn.providers
```

### Q: Can I use multiple VPN providers simultaneously?
**A:** No, you can only connect to one VPN at a time. However, you can:
- **Switch between providers** quickly
- **Configure failover** to alternate providers
- **Rotate between providers** automatically

### Q: Why is my VPN connection slow?
**A:** Several factors affect VPN speed:
```bash
# Try different protocols
python ip_rotator.py config set vpn.protocol wireguard  # Usually faster

# Choose closer servers
python ip_rotator.py vpn find-fastest --country US

# Optimize settings
python ip_rotator.py config set vpn.mtu 1300
python ip_rotator.py config set vpn.compression false

# Check server load
python ip_rotator.py vpn server-status
```

## 🔄 Proxy Management

### Q: What types of proxies are supported?
**A:** CyberRotate Pro supports:
- **HTTP/HTTPS proxies**: Standard web proxies
- **SOCKS4/SOCKS5 proxies**: More versatile, support any protocol
- **Residential proxies**: Real IP addresses from ISPs
- **Datacenter proxies**: Fast but easily detectable
- **Rotating proxies**: Automatically changing IP pools

### Q: How do I import a proxy list?
**A:** Import proxies from various formats:
```bash
# From text file (IP:PORT format)
python ip_rotator.py proxy import proxies.txt

# From CSV file
python ip_rotator.py proxy import proxies.csv --format csv

# From URL
python ip_rotator.py proxy import --url http://example.com/proxies.txt

# Test during import
python ip_rotator.py proxy import proxies.txt --test-all
```

### Q: How often should I rotate proxies?
**A:** Rotation frequency depends on your use case:
- **Web scraping**: Every 1-10 requests
- **General browsing**: Every 5-30 minutes
- **Streaming**: Every 1-2 hours
- **Gaming**: Avoid frequent rotation

```bash
# Set rotation interval
python ip_rotator.py config set proxy.rotation_interval 300  # 5 minutes
```

### Q: Why do my proxies keep failing?
**A:** Common proxy issues:
```bash
# Test proxy validity
python ip_rotator.py proxy test-all

# Remove dead proxies
python ip_rotator.py proxy cleanup --remove-dead

# Check proxy authentication
python ip_rotator.py proxy test --auth proxy.example.com:8080

# Verify proxy type
python ip_rotator.py proxy verify-type proxy.example.com:8080
```

## 🧅 Tor Usage

### Q: Is Tor built into CyberRotate Pro?
**A:** CyberRotate Pro integrates with your system's Tor installation:
- **Uses existing Tor**: If already installed
- **Can install Tor**: Via package managers
- **Manages Tor service**: Starts/stops as needed
- **Creates new circuits**: For IP rotation

### Q: How do I install Tor?
**A:** Installation varies by operating system:
```bash
# Linux (Ubuntu/Debian)
sudo apt update && sudo apt install tor

# Linux (CentOS/RHEL)
sudo yum install tor

# macOS (with Homebrew)
brew install tor

# Windows
# Download from torproject.org or use:
python ip_rotator.py tor install
```

### Q: Can I use Tor bridges?
**A:** Yes, for censored networks:
```bash
# Configure built-in bridges
python ip_rotator.py tor configure-bridges --type obfs4

# Use custom bridges
python ip_rotator.py tor add-bridge "obfs4 IP:PORT FINGERPRINT"

# Import bridge file
python ip_rotator.py tor import-bridges bridges.txt
```

### Q: How do I get a new Tor circuit?
**A:** Force new circuit creation:
```bash
# New circuit for current connection
python ip_rotator.py tor new-circuit

# New circuit for all connections
python ip_rotator.py tor new-circuit --all

# Automatic circuit rotation
python ip_rotator.py config set tor.circuit_rotation 600  # 10 minutes
```

## 🔒 Security & Privacy

### Q: How do I prevent DNS leaks?
**A:** Enable DNS leak protection:
```bash
# Enable built-in protection
python ip_rotator.py config set security.dns_leak_protection true

# Set custom DNS servers
python ip_rotator.py config set dns.servers "1.1.1.1,1.0.0.1"

# Test for DNS leaks
python ip_rotator.py security dns-leak-test

# Force DNS through VPN
python ip_rotator.py config set vpn.force_dns true
```

### Q: What is the kill switch and how does it work?
**A:** The kill switch blocks internet access if the VPN disconnects:
```bash
# Enable kill switch
python ip_rotator.py config set security.kill_switch true

# Test kill switch
python ip_rotator.py security test-kill-switch

# Configure kill switch behavior
python ip_rotator.py config set security.kill_switch_strict true
```

### Q: How can I check for IP leaks?
**A:** Run comprehensive security tests:
```bash
# Full security scan
python ip_rotator.py security scan

# Specific leak tests
python ip_rotator.py security dns-leak-test
python ip_rotator.py security webrtc-test
python ip_rotator.py security ipv6-test

# Continuous monitoring
python ip_rotator.py security monitor --interval 300
```

### Q: Is my traffic encrypted?
**A:** Encryption depends on the service:
- **VPN**: All traffic encrypted (AES-256, ChaCha20)
- **HTTPS Proxy**: Only HTTPS traffic encrypted
- **HTTP Proxy**: Traffic not encrypted
- **Tor**: Traffic encrypted through network
- **SOCKS Proxy**: Encryption depends on application

## 📱 Interface Usage

### Q: Can I use CyberRotate Pro without the GUI?
**A:** Yes, CyberRotate Pro offers multiple interfaces:
```bash
# Command-line only
python ip_rotator.py connect --vpn --no-gui

# API mode
python ip_rotator.py api start --port 8080

# Configuration file only
python ip_rotator.py --config-file config.json --headless
```

### Q: How do I customize the GUI?
**A:** GUI customization options:
```bash
# Change theme
python ip_rotator.py config set gui.theme dark

# Adjust scale for high DPI
python ip_rotator.py config set gui.scale_factor 1.5

# Hide/show panels
python ip_rotator.py config set gui.panels.logs false

# Custom layout
python ip_rotator.py gui save-layout my_layout
```

### Q: Can I run CyberRotate Pro as a service?
**A:** Yes, for background operation:
```bash
# Linux systemd service
sudo cp cyberrotate.service /etc/systemd/system/
sudo systemctl enable cyberrotate
sudo systemctl start cyberrotate

# Windows service
python ip_rotator.py install-service

# macOS launchd
cp com.cyberrotate.plist ~/Library/LaunchAgents/
launchctl load ~/Library/LaunchAgents/com.cyberrotate.plist
```

## 🔗 API Usage

### Q: How do I enable the API?
**A:** Start the API server:
```bash
# Start API server
python ip_rotator.py api start --port 8080

# Start with authentication
python ip_rotator.py api start --auth --port 8080

# Start in background
python ip_rotator.py api start --daemon --port 8080
```

### Q: How do I generate API keys?
**A:** Create and manage API keys:
```bash
# Generate new API key
python ip_rotator.py api generate-key --name "MyApp"

# List existing keys
python ip_rotator.py api list-keys

# Revoke API key
python ip_rotator.py api revoke-key KEY_ID

# Set key permissions
python ip_rotator.py api set-permissions KEY_ID --read --write
```

### Q: Can I integrate CyberRotate Pro with other applications?
**A:** Yes, through various methods:
- **REST API**: HTTP endpoints for all functions
- **WebSocket**: Real-time updates and control
- **Command line**: Scriptable CLI interface
- **Python module**: Import as Python library
- **Configuration files**: External config management

## 🔄 Automation

### Q: How do I set up automatic rotation?
**A:** Configure automated IP rotation:
```bash
# Start auto-rotation
python ip_rotator.py auto-rotate --interval 10m --method vpn

# Random rotation
python ip_rotator.py auto-rotate --random --interval 5-15m

# Country-specific rotation
python ip_rotator.py auto-rotate --countries "US,UK,DE" --interval 10m

# Stop auto-rotation
python ip_rotator.py auto-rotate --stop
```

### Q: Can I schedule rotations?
**A:** Use system schedulers:
```bash
# Linux cron (every hour)
0 * * * * cd /path/to/cyberrotate && python ip_rotator.py rotate

# Windows Task Scheduler
schtasks /create /tn "CyberRotate" /tr "python C:\cyberrotate\ip_rotator.py rotate" /sc hourly

# Built-in scheduler
python ip_rotator.py schedule add --time "09:00" --action "rotate --method vpn"
```

### Q: How do I create custom automation scripts?
**A:** Write Python scripts using the API:
```python
#!/usr/bin/env python3
import time
from cyberrotate import CyberRotate

cr = CyberRotate()

# Connect to VPN
cr.vpn.connect()

# Rotate every 10 minutes
while True:
    time.sleep(600)  # 10 minutes
    cr.rotate(method='vpn')
    print(f"Rotated to new IP: {cr.get_current_ip()}")
```

## 🐛 Troubleshooting

### Q: CyberRotate Pro won't start. What should I do?
**A:** Try these troubleshooting steps:
```bash
# Check Python version
python --version  # Must be 3.8+

# Check dependencies
pip list | grep -E "(requests|psutil)"

# Run with debug mode
python ip_rotator.py --debug

# Check for conflicts
python ip_rotator.py diagnose --check-conflicts

# Reset configuration
python ip_rotator.py config reset
```

### Q: Connection keeps dropping. How can I fix this?
**A:** Improve connection stability:
```bash
# Enable auto-reconnect
python ip_rotator.py config set vpn.auto_reconnect true

# Increase keep-alive interval
python ip_rotator.py config set vpn.keepalive 30

# Use more stable protocol
python ip_rotator.py config set vpn.protocol tcp

# Monitor connection
python ip_rotator.py monitor connection --auto-fix
```

### Q: How do I report bugs or get support?
**A:** Multiple support options available:
- **GitHub Issues**: Report bugs with details
- **Debug Report**: `python ip_rotator.py debug generate-report`
- **Community Forum**: User discussions and help
- **Email Support**: For premium users
- **Live Chat**: Available during business hours

### Q: Can I contribute to CyberRotate Pro development?
**A:** Yes! Contributions are welcome:
- **Code contributions**: Submit pull requests
- **Bug reports**: Report issues on GitHub
- **Documentation**: Improve this manual
- **Translations**: Help translate the interface
- **Testing**: Test new features and report feedback

## 💰 Licensing & Commercial Use

### Q: Is CyberRotate Pro free to use?
**A:** CyberRotate Pro offers multiple licensing options:
- **Community Edition**: Free for personal use
- **Professional Edition**: Commercial use, advanced features
- **Enterprise Edition**: Bulk licensing, custom support

### Q: Can I use CyberRotate Pro for commercial purposes?
**A:** Commercial use requires appropriate licensing:
- **Small business**: Professional Edition
- **Large organization**: Enterprise Edition
- **Development/Testing**: Community Edition may be sufficient
- **Redistribution**: Requires special licensing agreement

### Q: What's included in premium support?
**A:** Premium support includes:
- **Priority response**: Faster ticket resolution
- **Phone/video support**: Direct communication
- **Custom configuration**: Tailored setups
- **Training sessions**: Personal or team training
- **Early access**: Beta features and updates

## 🌍 Legal & Compliance

### Q: Is it legal to use IP rotation tools?
**A:** Legality varies by jurisdiction and use case:
- **Generally legal**: For privacy and security
- **May be restricted**: In some countries or networks
- **Terms of service**: Check service provider policies
- **Corporate policies**: Verify workplace compliance
- **Always recommended**: Use responsibly and ethically

### Q: Does CyberRotate Pro log my activity?
**A:** CyberRotate Pro's logging policy:
- **Local logs only**: No data sent to external servers
- **Configurable logging**: You control what gets logged
- **No tracking**: No analytics or telemetry by default
- **User privacy**: Designed with privacy in mind

### Q: Can network administrators detect CyberRotate Pro?
**A:** Detection depends on configuration:
- **VPN traffic**: May be detectable via DPI
- **Proxy usage**: Can be logged by network equipment
- **Tor usage**: Identifiable but not content
- **Stealth options**: Available to reduce detectability

---

## 📞 Still Need Help?

If your question isn't answered here:

1. **Check the full manual**: [Manual Index](README.md)
2. **Search the documentation**: Use Ctrl+F to search
3. **Visit troubleshooting guide**: [Troubleshooting](14-troubleshooting.md)
4. **Generate debug report**: `python ip_rotator.py debug generate-report`
5. **Contact support**: Submit issue with debug information

**Next**: [Support](17-support.md) | [Back to Manual](README.md)
