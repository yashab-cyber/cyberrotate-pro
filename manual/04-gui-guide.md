# GUI User Guide

CyberRotate Pro features an intuitive graphical user interface that makes IP rotation and network privacy management simple and accessible.

## 🖥️ Interface Overview

### Main Window Layout

The CyberRotate Pro GUI is organized into several key sections:

```
┌─────────────────────────────────────────────────────┐
│ File  Tools  VPN  Proxy  Tor  Security  Help       │
├─────────────────────────────────────────────────────┤
│ [Status] [Connect] [Disconnect] [Settings] [Debug] │
├─────────────────────────────────────────────────────┤
│                                                     │
│  Connection Status    │    Current Configuration   │
│  ┌─────────────────┐  │    ┌─────────────────────┐  │
│  │ 🔴 Disconnected │  │    │ VPN: None           │  │
│  │ IP: 192.168.1.x │  │    │ Proxy: Disabled     │  │
│  │ Location: Local │  │    │ Tor: Inactive       │  │
│  └─────────────────┘  │    └─────────────────────┘  │
│                                                     │
│  Rotation Settings    │    Active Connections      │
│  ┌─────────────────┐  │    ┌─────────────────────┐  │
│  │ Auto: ⬜        │  │    │ No active           │  │
│  │ Interval: 5min  │  │    │ connections         │  │
│  │ Method: VPN     │  │    │                     │  │
│  └─────────────────┘  │    └─────────────────────┘  │
│                                                     │
│  Log Output                                         │
│  ┌───────────────────────────────────────────────┐  │
│  │ [INFO] CyberRotate Pro started                │  │
│  │ [INFO] Checking system requirements...        │  │
│  │ [INFO] Ready for connections                  │  │
│  └───────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────┘
```

## 🎛️ Main Controls

### Connection Panel

#### Status Indicators
- **🔴 Red**: Disconnected/No protection
- **🟡 Yellow**: Connecting/Switching
- **🟢 Green**: Connected/Protected

#### Primary Buttons
- **Connect**: Establish VPN/Proxy connection
- **Disconnect**: Terminate all connections
- **Quick Rotate**: Immediately change IP
- **Emergency Stop**: Force disconnect everything

### Configuration Tabs

#### VPN Tab
Configure and manage VPN connections:

1. **Provider Selection**
   - Choose from configured VPN providers
   - Add new VPN configurations
   - Test connection speeds

2. **Server Selection**
   - Browse available servers by country
   - Filter by speed, load, features
   - Add to favorites for quick access

3. **Connection Settings**
   - Protocol selection (OpenVPN, WireGuard)
   - Encryption settings
   - Kill switch options

#### Proxy Tab
Manage proxy configurations:

1. **Proxy Lists**
   - Import proxy lists
   - Test proxy validity
   - Sort by speed/anonymity

2. **Rotation Settings**
   - Random vs sequential rotation
   - Timeout settings
   - Failure handling

3. **Proxy Types**
   - HTTP/HTTPS proxies
   - SOCKS4/5 proxies
   - Residential vs datacenter

#### Tor Tab
Configure Tor network usage:

1. **Tor Settings**
   - Entry/exit node selection
   - Bridge configuration
   - Circuit building preferences

2. **SOCKS Proxy**
   - Local SOCKS proxy settings
   - Application integration
   - DNS over Tor

## 📋 Menu System

### File Menu
- **New Profile**: Create connection profile
- **Load Profile**: Load saved configuration
- **Save Profile**: Save current settings
- **Export Settings**: Backup configuration
- **Exit**: Close application

### Tools Menu
- **IP Checker**: Test current IP address
- **Speed Test**: Measure connection speed
- **DNS Leak Test**: Check for DNS leaks
- **Port Scanner**: Scan for open ports
- **Connection Monitor**: Real-time monitoring

### VPN Menu
- **Connect VPN**: Quick VPN connection
- **Change Server**: Switch VPN server
- **VPN Status**: Detailed connection info
- **Kill Switch**: Emergency disconnect

### Proxy Menu
- **Test Proxies**: Validate proxy list
- **Rotate Now**: Manual IP rotation
- **Proxy Statistics**: Usage analytics
- **Clear Cache**: Reset proxy cache

### Security Menu
- **DNS Settings**: Configure DNS servers
- **Firewall Rules**: Manage traffic rules
- **Leak Protection**: Enable/disable protections
- **Security Scan**: Comprehensive security check

## 🔧 Configuration Dialogs

### VPN Configuration Dialog

```
┌─────────────────────────────────────────────┐
│ VPN Configuration                           │
├─────────────────────────────────────────────┤
│ Provider: [NordVPN        ▼]               │
│ Protocol: [OpenVPN       ▼]               │
│ Server:   [Auto-select   ▼]               │
│                                             │
│ Authentication:                             │
│ Username: [your_username    ]               │
│ Password: [••••••••••••••••]               │
│                                             │
│ Advanced Options:                           │
│ ☑ Enable kill switch                       │
│ ☑ DNS leak protection                      │
│ ☐ Auto-reconnect                           │
│ ☐ Start with Windows                       │
│                                             │
│ [Test Connection] [Save] [Cancel]           │
└─────────────────────────────────────────────┘
```

### Proxy Configuration Dialog

```
┌─────────────────────────────────────────────┐
│ Proxy Configuration                         │
├─────────────────────────────────────────────┤
│ Proxy Type: [HTTP ▼]                       │
│ Host: [proxy.example.com]                   │
│ Port: [8080    ]                           │
│                                             │
│ Authentication (if required):               │
│ Username: [proxy_user     ]                 │
│ Password: [••••••••••••••]                 │
│                                             │
│ Rotation Settings:                          │
│ Interval: [5     ] minutes                  │
│ Method:   [Random ▼]                       │
│                                             │
│ ☑ Test before use                          │
│ ☑ Remove failed proxies                    │
│                                             │
│ [Test Proxy] [Add to List] [Cancel]         │
└─────────────────────────────────────────────┘
```

## 📊 Monitoring and Statistics

### Real-time Monitoring Panel

The monitoring panel provides live updates on:

1. **Connection Status**
   - Current IP address
   - Geographic location
   - Connection uptime
   - Data transferred

2. **Performance Metrics**
   - Connection speed
   - Latency measurements
   - Packet loss statistics
   - Bandwidth usage

3. **Security Status**
   - DNS leak status
   - WebRTC leak detection
   - Firewall status
   - Encryption status

### Statistics Dashboard

Access detailed statistics via `Tools > Statistics`:

- **Usage History**: Daily/weekly/monthly usage
- **Server Performance**: Speed tests and reliability
- **Rotation History**: IP change timeline
- **Security Events**: Leak detection alerts

## 🚨 Status Notifications

### Notification Types

1. **System Tray Notifications**
   - Connection established/lost
   - IP rotation completed
   - Security alerts
   - System errors

2. **In-app Alerts**
   - Configuration warnings
   - Performance issues
   - Update notifications

3. **Sound Alerts** (Optional)
   - Connection success/failure
   - Security breach warnings
   - Critical errors

### Customizing Notifications

Access notification settings via `File > Preferences > Notifications`:

- Enable/disable notification types
- Set sound preferences
- Configure alert thresholds
- Choose notification duration

## 🎯 Quick Tasks

### Connect to VPN
1. Click **VPN** tab
2. Select desired server/country
3. Click **Connect**
4. Wait for green status indicator

### Start Proxy Rotation
1. Click **Proxy** tab
2. Import or configure proxy list
3. Set rotation interval
4. Click **Start Rotation**

### Enable Tor
1. Click **Tor** tab
2. Configure bridge settings (if needed)
3. Click **Connect to Tor**
4. Wait for circuit establishment

### Run Security Check
1. Go to **Tools > Security Scan**
2. Click **Start Comprehensive Scan**
3. Review results in popup dialog
4. Address any identified issues

## 🔍 Troubleshooting GUI Issues

### Common Problems

1. **GUI Won't Start**
   ```bash
   # Check Python GUI libraries
   pip install --upgrade tkinter PyQt5
   
   # Run in debug mode
   python ip_rotator.py --gui --debug
   ```

2. **Missing Menu Items**
   - Update to latest version
   - Check user permissions
   - Reset configuration to defaults

3. **Slow Interface Response**
   - Close unnecessary background processes
   - Reduce log verbosity
   - Clear application cache

4. **Display Issues**
   - Update graphics drivers
   - Adjust display scaling
   - Try different theme options

### Getting Help

- Use **Help > User Manual** for detailed documentation
- Access **Help > Debug Information** for technical details
- Contact support via **Help > Report Issue**

## 🎨 Customization

### Themes and Appearance

1. **Built-in Themes**
   - Light theme (default)
   - Dark theme
   - High contrast theme

2. **Custom Themes**
   - Create custom color schemes
   - Import community themes
   - Export personal themes

### Layout Customization

- Resize panels by dragging borders
- Hide/show panels via View menu
- Save custom layouts as profiles

### Keyboard Shortcuts

| Action | Shortcut |
|--------|----------|
| Connect/Disconnect | Ctrl+C |
| Quick Rotate | Ctrl+R |
| Emergency Stop | Ctrl+Shift+S |
| Settings | Ctrl+, |
| Refresh Status | F5 |
| Show/Hide Log | Ctrl+L |

---

**Next**: [CLI User Guide](05-cli-guide.md) | [Back to Manual](README.md)
