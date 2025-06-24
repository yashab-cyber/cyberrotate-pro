# Troubleshooting Guide

This comprehensive troubleshooting guide helps you resolve common issues with CyberRotate Pro quickly and effectively.

## 🚨 Emergency Quick Fixes

### Connection Lost/Stuck
```bash
# Emergency disconnect all
python ip_rotator.py disconnect --force

# Reset network stack (Windows)
netsh winsock reset
netsh int ip reset

# Reset network (Linux/macOS)
sudo systemctl restart NetworkManager  # Linux
sudo ifconfig en0 down && sudo ifconfig en0 up  # macOS
```

### Application Won't Start
```bash
# Check Python environment
python --version
pip list | grep -E "(requests|psutil|tkinter)"

# Reinstall dependencies
pip install --force-reinstall -r requirements.txt

# Run with verbose logging
python ip_rotator.py --debug --verbose
```

### Kill Switch Activated
```bash
# Disable kill switch emergency
python ip_rotator.py config set security.kill_switch false

# Restore network access
python ip_rotator.py network restore
```

## 🔧 Installation Issues

### Python Environment Problems

#### Issue: ModuleNotFoundError
```bash
# Error: No module named 'requests', 'psutil', etc.

# Solution 1: Install missing modules
pip install requests psutil tkinter

# Solution 2: Virtual environment
python -m venv cyberrotate_env
source cyberrotate_env/bin/activate  # Linux/macOS
cyberrotate_env\Scripts\activate     # Windows
pip install -r requirements.txt

# Solution 3: Check Python path
python -c "import sys; print(sys.path)"
```

#### Issue: Permission Denied
```bash
# Error: Permission denied when installing

# Solution 1: User installation
pip install --user -r requirements.txt

# Solution 2: Use sudo (Linux/macOS)
sudo pip install -r requirements.txt

# Solution 3: Virtual environment (recommended)
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

#### Issue: Python Version Conflicts
```bash
# Check Python version
python --version

# If Python 2.x is default, use Python 3 explicitly
python3 ip_rotator.py
pip3 install -r requirements.txt

# On Windows with multiple Python versions
py -3 ip_rotator.py
```

### System Dependencies

#### Windows Issues
```powershell
# Missing Visual C++ Build Tools
# Download and install Microsoft C++ Build Tools

# WinTun driver issues
# Run as administrator:
python ip_rotator.py install-deps --wintun

# TAP adapter problems
# Reinstall TAP-Windows adapter:
python ip_rotator.py fix-tap-adapter
```

#### Linux Issues
```bash
# Missing system packages
sudo apt update
sudo apt install python3-pip python3-tk openvpn

# NetworkManager conflicts
sudo systemctl stop NetworkManager
sudo systemctl disable NetworkManager
sudo systemctl enable systemd-networkd

# Firewall blocking connections
sudo ufw disable  # Temporary - configure properly
```

#### macOS Issues
```bash
# Homebrew installation
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
brew install python@3.9 openvpn

# Permission issues with /usr/local
sudo chown -R $(whoami) /usr/local

# Code signing issues
xattr -rd com.apple.quarantine /path/to/cyberrotate-pro
```

## 🌐 Connection Problems

### VPN Connection Issues

#### Cannot Connect to VPN
```bash
# Check VPN configuration
python ip_rotator.py vpn test-config

# Test specific server
python ip_rotator.py vpn test-server us-west-1

# Check credentials
python ip_rotator.py config show vpn.credentials

# Reset VPN settings
python ip_rotator.py config reset vpn
```

**Common Causes:**
- Invalid credentials
- Server overloaded/maintenance
- Firewall blocking VPN ports
- ISP blocking VPN traffic
- Outdated VPN configuration

**Solutions:**
1. Verify username/password
2. Try different server
3. Change VPN protocol (OpenVPN ↔ WireGuard)
4. Check firewall settings
5. Contact VPN provider

#### VPN Connects but No Internet
```bash
# Check DNS configuration
nslookup google.com

# Test with different DNS
python ip_rotator.py config set dns.servers "8.8.8.8,1.1.1.1"

# Flush DNS cache
ipconfig /flushdns  # Windows
sudo dscacheutil -flushcache  # macOS
sudo systemctl restart systemd-resolved  # Linux

# Check routing table
route print  # Windows
route -n  # Linux/macOS
```

#### Frequent VPN Disconnections
```bash
# Enable auto-reconnect
python ip_rotator.py config set vpn.auto_reconnect true

# Increase keep-alive interval
python ip_rotator.py config set vpn.keepalive 10

# Check connection stability
python ip_rotator.py vpn monitor --duration 300
```

### Proxy Connection Issues

#### Proxy Authentication Failed
```bash
# Verify proxy credentials
python ip_rotator.py proxy test --host proxy.example.com --port 8080

# Update proxy authentication
python ip_rotator.py proxy update-auth proxy_id --username new_user --password new_pass

# Test without authentication
python ip_rotator.py proxy test --host proxy.example.com --port 8080 --no-auth
```

#### Proxy Too Slow
```bash
# Test proxy speed
python ip_rotator.py proxy speed-test proxy_id

# Set timeout limits
python ip_rotator.py config set proxy.timeout 30

# Remove slow proxies
python ip_rotator.py proxy cleanup --min-speed 1.0
```

#### Proxy List Not Working
```bash
# Validate proxy list
python ip_rotator.py proxy validate-list proxies.txt

# Clean dead proxies
python ip_rotator.py proxy cleanup --remove-dead

# Import fresh proxy list
python ip_rotator.py proxy import fresh-proxies.txt --test-all
```

### Tor Connection Issues

#### Tor Won't Start
```bash
# Check Tor installation
which tor  # Linux/macOS
where tor  # Windows

# Install/update Tor
sudo apt install tor  # Linux
brew install tor      # macOS
# Windows: Download from torproject.org

# Check Tor service
sudo systemctl status tor  # Linux
brew services list | grep tor  # macOS

# Start Tor manually
python ip_rotator.py tor start --verbose
```

#### Tor Connection Timeout
```bash
# Use bridges for censored networks
python ip_rotator.py tor configure-bridges

# Change Tor ports
python ip_rotator.py config set tor.socks_port 9150
python ip_rotator.py config set tor.control_port 9151

# Reset Tor circuits
python ip_rotator.py tor new-circuit --all
```

## 🔒 Security and Privacy Issues

### DNS Leaks

#### Detecting DNS Leaks
```bash
# Run DNS leak test
python ip_rotator.py security dns-leak-test

# Check current DNS servers
python ip_rotator.py info dns-servers

# Test with external service
curl -s https://www.dnsleaktest.com/api/get-result | jq
```

#### Fixing DNS Leaks
```bash
# Enable DNS leak protection
python ip_rotator.py config set security.dns_leak_protection true

# Set custom DNS servers
python ip_rotator.py config set dns.servers "1.1.1.1,1.0.0.1"

# Disable IPv6 (prevents IPv6 leaks)
python ip_rotator.py config set security.disable_ipv6 true

# Force DNS through VPN
python ip_rotator.py config set vpn.force_dns true
```

### WebRTC Leaks

#### Detecting WebRTC Leaks
```bash
# Test for WebRTC leaks
python ip_rotator.py security webrtc-test

# Browser-based test (manual)
# Visit: https://browserleaks.com/webrtc
```

#### Preventing WebRTC Leaks
```bash
# Enable WebRTC protection
python ip_rotator.py config set security.webrtc_protection true

# Block WebRTC in browser (Chrome)
# Install extension: WebRTC Leak Prevent

# Block WebRTC in browser (Firefox)
# about:config -> media.peerconnection.enabled = false
```

### IP Leaks

#### IPv6 Leaks
```bash
# Check IPv6 status
python ip_rotator.py info ipv6

# Disable IPv6 system-wide
# Windows (as admin):
netsh interface ipv6 set global randomizeidentifiers=disabled
netsh interface ipv6 set privacy state=disabled

# Linux:
echo 'net.ipv6.conf.all.disable_ipv6 = 1' | sudo tee -a /etc/sysctl.conf
sudo sysctl -p

# macOS:
sudo networksetup -setv6off Wi-Fi
sudo networksetup -setv6off Ethernet
```

### Kill Switch Issues

#### Kill Switch Not Working
```bash
# Test kill switch
python ip_rotator.py security test-kill-switch

# Enable kill switch
python ip_rotator.py config set security.kill_switch true

# Configure kill switch rules
python ip_rotator.py security configure-kill-switch
```

#### Kill Switch Blocking Internet
```bash
# Check kill switch status
python ip_rotator.py security kill-switch-status

# Temporarily disable
python ip_rotator.py security kill-switch-disable --temporary

# Restore network access
python ip_rotator.py network restore

# Reconfigure kill switch
python ip_rotator.py security kill-switch-reset
```

## 📱 GUI Issues

### Interface Problems

#### GUI Won't Start
```bash
# Check GUI dependencies
python -c "import tkinter; print('Tkinter OK')"

# Try alternative GUI backend
python ip_rotator.py --gui --backend qt

# Run in terminal mode
python ip_rotator.py --no-gui

# Reinstall GUI libraries
pip install --force-reinstall tkinter PyQt5
```

#### GUI Freezing/Slow
```bash
# Reduce log verbosity
python ip_rotator.py config set logging.level ERROR

# Clear GUI cache
rm -rf ~/.cyberrotate/gui_cache

# Disable animations
python ip_rotator.py config set gui.animations false

# Use lightweight theme
python ip_rotator.py config set gui.theme minimal
```

#### Display Issues
```bash
# Scale interface for high DPI
python ip_rotator.py config set gui.scale_factor 1.5

# Use different theme
python ip_rotator.py config set gui.theme dark

# Reset GUI layout
python ip_rotator.py config reset gui
```

### Control Issues

#### Buttons Not Responding
```bash
# Check for hung processes
ps aux | grep ip_rotator  # Linux/macOS
tasklist | findstr python  # Windows

# Kill hung processes
pkill -f ip_rotator  # Linux/macOS
taskkill /F /IM python.exe  # Windows

# Restart with clean state
python ip_rotator.py --reset-state
```

## 🖥️ CLI Issues

### Command Not Found
```bash
# Check if script is executable
chmod +x ip_rotator.py  # Linux/macOS

# Use full path
python /full/path/to/ip_rotator.py status

# Add to PATH (Linux/macOS)
export PATH=$PATH:/path/to/cyberrotate-pro

# Add to PATH (Windows)
set PATH=%PATH%;C:\path\to\cyberrotate-pro
```

### Command Timeouts
```bash
# Increase timeout
python ip_rotator.py connect --timeout 120

# Use async mode
python ip_rotator.py connect --async

# Check for blocking processes
python ip_rotator.py status --detailed
```

### Output Issues
```bash
# Fix encoding issues (Windows)
chcp 65001
set PYTHONIOENCODING=utf-8

# Redirect output
python ip_rotator.py status > output.txt 2>&1

# Use JSON output for parsing
python ip_rotator.py status --json | jq
```

## 🌍 Network Issues

### ISP Blocking

#### VPN Blocking
```bash
# Try different ports
python ip_rotator.py config set vpn.port 443
python ip_rotator.py config set vpn.port 80

# Use obfuscation
python ip_rotator.py config set vpn.obfuscation true

# Try different protocols
python ip_rotator.py config set vpn.protocol tcp
```

#### Deep Packet Inspection (DPI)
```bash
# Enable traffic obfuscation
python ip_rotator.py config set obfuscation.enabled true

# Use shadowsocks protocol
python ip_rotator.py config set proxy.protocol shadowsocks

# Try different encryption
python ip_rotator.py config set vpn.cipher AES-256-GCM
```

### Firewall Issues

#### Windows Firewall
```powershell
# Allow through Windows Firewall (as admin)
netsh advfirewall firewall add rule name="CyberRotate Pro" dir=in action=allow program="C:\Python\python.exe"

# Disable Windows Firewall temporarily
netsh advfirewall set allprofiles state off
```

#### Linux iptables
```bash
# Allow VPN traffic
sudo iptables -A OUTPUT -p udp --dport 1194 -j ACCEPT
sudo iptables -A INPUT -p udp --sport 1194 -j ACCEPT

# Allow HTTP proxy
sudo iptables -A OUTPUT -p tcp --dport 8080 -j ACCEPT

# Save rules
sudo iptables-save > /etc/iptables/rules.v4
```

#### Corporate Firewall
```bash
# Use HTTP proxy mode
python ip_rotator.py config set network.proxy_mode http

# Try port 443 (HTTPS)
python ip_rotator.py config set vpn.port 443

# Use SOCKS over HTTP tunnel
python ip_rotator.py config set proxy.tunnel_mode http
```

## 🔄 Performance Issues

### Slow Connection Speeds

#### Optimize VPN Performance
```bash
# Use fastest protocol
python ip_rotator.py config set vpn.protocol wireguard

# Choose nearest server
python ip_rotator.py vpn find-fastest --country US

# Optimize MTU size
python ip_rotator.py config set vpn.mtu 1300

# Disable compression
python ip_rotator.py config set vpn.compression false
```

#### Optimize Proxy Performance
```bash
# Test proxy speeds
python ip_rotator.py proxy speed-test-all

# Use fastest proxies only
python ip_rotator.py proxy filter --min-speed 5.0

# Increase connection pool
python ip_rotator.py config set proxy.max_connections 10
```

### High CPU/Memory Usage

#### Reduce Resource Usage
```bash
# Lower log level
python ip_rotator.py config set logging.level WARNING

# Disable monitoring
python ip_rotator.py config set monitoring.enabled false

# Reduce GUI updates
python ip_rotator.py config set gui.update_interval 5000

# Use lightweight mode
python ip_rotator.py --lite-mode
```

## 📋 Log Analysis

### Finding Log Files
```bash
# Default log locations
# Linux: ~/.cyberrotate/logs/
# macOS: ~/Library/Logs/CyberRotate/
# Windows: %APPDATA%\CyberRotate\logs\

# Find logs
python ip_rotator.py info log-location

# View recent logs
python ip_rotator.py logs --tail 100
```

### Common Log Patterns

#### Connection Errors
```bash
# Search for connection errors
grep -i "connection.*failed" ~/.cyberrotate/logs/cyberrotate.log

# VPN authentication errors
grep -i "auth.*failed" ~/.cyberrotate/logs/cyberrotate.log

# Proxy errors
grep -i "proxy.*error" ~/.cyberrotate/logs/cyberrotate.log
```

#### Debug Information
```bash
# Enable debug logging
python ip_rotator.py config set logging.level DEBUG

# Capture network traffic
python ip_rotator.py debug capture-traffic --duration 60

# Generate debug report
python ip_rotator.py debug generate-report
```

## 🆘 Getting Additional Help

### Self-Diagnosis
```bash
# Run comprehensive system check
python ip_rotator.py diagnose --full

# Generate support bundle
python ip_rotator.py support generate-bundle

# Test all components
python ip_rotator.py test --all-components
```

### Community Resources
- **GitHub Issues**: Report bugs and get help
- **Community Forum**: Discussion and user support
- **Documentation**: Updated guides and tutorials
- **Discord/Telegram**: Real-time community chat

### Professional Support
- **Priority Support**: Faster response times
- **Remote Assistance**: Screen sharing troubleshooting
- **Custom Configuration**: Tailored setups
- **Training Sessions**: Personal or team training

### Before Contacting Support

1. **Run diagnostics**:
   ```bash
   python ip_rotator.py diagnose --export-report
   ```

2. **Collect system information**:
   ```bash
   python ip_rotator.py info --system --export
   ```

3. **Check recent logs**:
   ```bash
   python ip_rotator.py logs --recent --level ERROR
   ```

4. **Note error messages** and steps to reproduce

5. **Test with minimal configuration**:
   ```bash
   python ip_rotator.py --reset-config connect --vpn
   ```

---

**Next**: [Debugging Guide](15-debugging.md) | [Back to Manual](README.md)
