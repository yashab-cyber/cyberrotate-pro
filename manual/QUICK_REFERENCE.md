# CyberRotate Pro Manual - Quick Reference Card

## 🚀 Essential Commands & Settings

### Installation (One-liner)
```bash
# Pip install
pip install cyberrotate-pro

# Docker
docker run -d -p 8080:8080 zehrasec/cyberrotate-pro

# Verify installation
cyberrotate --version
```

### Basic CLI Commands
```bash
# Start rotation
cyberrotate start --provider nordvpn --interval 300

# Stop rotation
cyberrotate stop

# Get current IP
cyberrotate ip

# Rotate now
cyberrotate rotate

# Check status
cyberrotate status
```

### API Quick Start
```python
import requests

# Base URL
API_BASE = "http://localhost:8080/api/v1"

# Start rotation
requests.post(f"{API_BASE}/rotation/start", 
              json={"type": "vpn", "interval": 300})

# Get current IP
response = requests.get(f"{API_BASE}/ip/current")
print(response.json()["ip"])
```

## ⚙️ Configuration Quick Setup

### Basic Config File (`~/.cyberrotate/config.yaml`)
```yaml
# Basic configuration
api:
  host: "localhost"
  port: 8080
  key: "your-api-key"

rotation:
  enabled: true
  interval: 300  # 5 minutes
  type: "auto"   # auto, vpn, proxy, tor

providers:
  nordvpn:
    enabled: true
    username: "your-username"
    password: "your-password"
  
security:
  kill_switch: true
  dns_leak_protection: true
  ipv6_blocking: true
```

### VPN Provider Templates
```yaml
# NordVPN
nordvpn:
  type: "openvpn"
  servers_url: "https://downloads.nordcdn.com/configs/archives/servers/ovpn.zip"
  auth_user_pass: true

# ExpressVPN  
expressvpn:
  type: "openvpn"
  config_dir: "/path/to/expressvpn/configs"
  auth_user_pass: true

# Proxy
proxymesh:
  type: "proxy"
  http_proxy: "proxy.example.com:8080"
  auth_required: true
```

## 🔧 Troubleshooting Quick Fixes

### Common Issues
```bash
# Connection failed
cyberrotate test --provider nordvpn
cyberrotate logs --level error --tail 50

# DNS issues
cyberrotate dns --test
cyberrotate dns --set 1.1.1.1,8.8.8.8

# Permission issues (Linux/Mac)
sudo chown -R $USER ~/.cyberrotate
chmod 600 ~/.cyberrotate/config.yaml

# Service not starting
cyberrotate service --restart
systemctl status cyberrotate  # Linux
```

### Log Locations
```bash
# Windows
%APPDATA%\CyberRotate\logs\

# Linux
~/.cyberrotate/logs/
/var/log/cyberrotate/

# macOS
~/Library/Logs/CyberRotate/

# Docker
docker logs cyberrotate-container
```

## 📊 Monitoring & Status

### GUI Access
```
http://localhost:8080/
https://localhost:8443/
```

### Status Endpoints
```bash
# Health check
curl http://localhost:8080/health

# Current status
curl http://localhost:8080/api/v1/status

# Current IP
curl http://localhost:8080/api/v1/ip/current

# Connection history
curl http://localhost:8080/api/v1/connections/history
```

### Performance Metrics
```bash
# Connection speed test
cyberrotate speedtest

# Latency test
cyberrotate ping --count 5

# Provider performance
cyberrotate benchmark --provider all
```

## 🛡️ Security Quick Checks

### Leak Tests
```bash
# DNS leak test
cyberrotate test dns

# WebRTC leak test
cyberrotate test webrtc

# IPv6 leak test
cyberrotate test ipv6

# Full security test
cyberrotate test all
```

### Security URLs
```bash
# Online leak tests
https://dnsleaktest.com/
https://ipleak.net/
https://www.whatismyipaddress.com/
```

## 🤖 Automation Quick Setup

### Cron Examples
```bash
# Rotate every 30 minutes
*/30 * * * * cyberrotate rotate

# Daily provider health check
0 9 * * * cyberrotate test --provider all --email-report

# Weekly cleanup
0 2 * * 0 cyberrotate cleanup --logs --older-than 7d
```

### Systemd Service (Linux)
```bash
# Enable auto-start
sudo systemctl enable cyberrotate
sudo systemctl start cyberrotate

# Check status
systemctl status cyberrotate

# View logs
journalctl -u cyberrotate -f
```

## 📞 Emergency Procedures

### Kill Switch Activation
```bash
# Manual kill switch
cyberrotate kill-switch --enable

# Emergency disconnect
cyberrotate emergency-stop

# Block all traffic except VPN
cyberrotate firewall --lockdown
```

### Recovery Commands
```bash
# Reset configuration
cyberrotate reset --config

# Restore default settings
cyberrotate restore --defaults

# Clear all data
cyberrotate clean --all --force

# Reinstall service
cyberrotate service --reinstall
```

## 🔗 Important Links

### Documentation
- **Manual**: [README.md](README.md)
- **Installation**: [01-installation.md](01-installation.md)
- **Quick Start**: [02-quick-start.md](02-quick-start.md)
- **API Reference**: [06-api-reference.md](06-api-reference.md)
- **Troubleshooting**: [14-troubleshooting.md](14-troubleshooting.md)

### Support
- **Email**: support@zehrasec.com
- **Discord**: https://discord.gg/zehrasec
- **GitHub**: https://github.com/zehrasec/cyberrotate-pro
- **Docs**: https://docs.zehrasec.com/cyberrotate

## 🚨 Emergency Contacts

### Critical Issues
- **Security Emergency**: security@zehrasec.com
- **Enterprise Support**: enterprise@zehrasec.com
- **24/7 Hotline**: +1-800-ZEHRASEC

### Reporting
- **Bug Reports**: bugs@zehrasec.com
- **Feature Requests**: features@zehrasec.com
- **Vulnerability Reports**: security@zehrasec.com

---

## 📋 Version Information

- **Manual Version**: 1.0.0
- **Software Version**: 1.0.0+
- **Last Updated**: June 24, 2025
- **Created by**: Yashab Alam - ZehraSec

---

*Keep this quick reference handy for fast access to essential CyberRotate Pro information. For detailed documentation, visit the [main manual](README.md).*
