# API Reference

CyberRotate Pro provides a comprehensive REST API for programmatic access to all features. This guide covers all available endpoints, authentication, and integration examples.

## 🔐 Authentication

### API Key Authentication
All API requests require authentication via API key:

```http
Authorization: Bearer YOUR_API_KEY
Content-Type: application/json
```

### Generating API Keys
```bash
# Generate new API key
python ip_rotator.py api generate-key --name "MyApp"

# List existing keys
python ip_rotator.py api list-keys

# Revoke API key
python ip_rotator.py api revoke-key KEY_ID
```

### Base URL
```
Default: http://localhost:8080/api/v1
Custom: http://your-server:port/api/v1
```

## 📡 Core Endpoints

### Connection Management

#### POST /connect
Establish a new connection:

**Request:**
```http
POST /api/v1/connect
Authorization: Bearer YOUR_API_KEY
Content-Type: application/json

{
    "service": "vpn",
    "server": "us-west-1",
    "protocol": "openvpn",
    "options": {
        "kill_switch": true,
        "dns_protection": true
    }
}
```

**Response:**
```json
{
    "success": true,
    "connection_id": "conn_123456",
    "service": "vpn",
    "server": "us-west-1",
    "status": "connecting",
    "estimated_time": 15
}
```

**Parameters:**
- `service` (required): "vpn", "proxy", or "tor"
- `server` (optional): Specific server name
- `country` (optional): Country code
- `protocol` (optional): Connection protocol
- `options` (optional): Additional connection options

#### GET /status
Get current connection status:

**Request:**
```http
GET /api/v1/status
Authorization: Bearer YOUR_API_KEY
```

**Response:**
```json
{
    "status": "connected",
    "service": "vpn",
    "connection_id": "conn_123456",
    "ip_address": "203.0.113.1",
    "location": {
        "country": "United States",
        "country_code": "US",
        "city": "New York",
        "region": "NY",
        "coordinates": {
            "latitude": 40.7128,
            "longitude": -74.0060
        }
    },
    "server": {
        "name": "us-west-1",
        "location": "Los Angeles",
        "load": 45,
        "ping": 25
    },
    "uptime": 3600,
    "data_usage": {
        "bytes_sent": 1048576,
        "bytes_received": 2097152,
        "total": 3145728
    }
}
```

#### POST /disconnect
Terminate connection:

**Request:**
```http
POST /api/v1/disconnect
Authorization: Bearer YOUR_API_KEY
Content-Type: application/json

{
    "service": "all",
    "force": false
}
```

**Response:**
```json
{
    "success": true,
    "message": "All connections terminated",
    "disconnected_services": ["vpn"]
}
```

### IP Rotation

#### POST /rotate
Change IP address:

**Request:**
```http
POST /api/v1/rotate
Authorization: Bearer YOUR_API_KEY
Content-Type: application/json

{
    "method": "vpn",
    "force": false,
    "target_country": "DE"
}
```

**Response:**
```json
{
    "success": true,
    "rotation_id": "rot_789012",
    "old_ip": "203.0.113.1",
    "new_ip": "198.51.100.1",
    "old_location": {
        "country": "United States",
        "city": "New York"
    },
    "new_location": {
        "country": "Germany",
        "city": "Frankfurt"
    },
    "rotation_time": 8.5
}
```

#### POST /auto-rotate
Start/stop automatic rotation:

**Request:**
```http
POST /api/v1/auto-rotate
Authorization: Bearer YOUR_API_KEY
Content-Type: application/json

{
    "action": "start",
    "interval": 300,
    "method": "vpn",
    "countries": ["US", "UK", "DE"]
}
```

**Response:**
```json
{
    "success": true,
    "auto_rotation_id": "auto_345678",
    "status": "active",
    "next_rotation": "2024-01-15T11:05:00Z",
    "settings": {
        "interval": 300,
        "method": "vpn",
        "countries": ["US", "UK", "DE"]
    }
}
```

### VPN Management

#### GET /vpn/servers
List available VPN servers:

**Request:**
```http
GET /api/v1/vpn/servers?country=US&limit=10
Authorization: Bearer YOUR_API_KEY
```

**Response:**
```json
{
    "servers": [
        {
            "name": "us-west-1",
            "location": "Los Angeles",
            "country": "United States",
            "country_code": "US",
            "load": 45,
            "ping": 25,
            "features": ["P2P", "Streaming"],
            "protocols": ["OpenVPN", "WireGuard"]
        }
    ],
    "total": 156,
    "page": 1,
    "per_page": 10
}
```

#### POST /vpn/test-server
Test VPN server connectivity:

**Request:**
```http
POST /api/v1/vpn/test-server
Authorization: Bearer YOUR_API_KEY
Content-Type: application/json

{
    "server": "us-west-1"
}
```

**Response:**
```json
{
    "success": true,
    "server": "us-west-1",
    "ping": 25,
    "download_speed": 50.2,
    "upload_speed": 25.1,
    "test_duration": 10.5
}
```

### Proxy Management

#### GET /proxy/list
List configured proxies:

**Request:**
```http
GET /api/v1/proxy/list?status=active
Authorization: Bearer YOUR_API_KEY
```

**Response:**
```json
{
    "proxies": [
        {
            "id": "proxy_001",
            "host": "proxy1.example.com",
            "port": 8080,
            "type": "http",
            "country": "US",
            "status": "active",
            "response_time": 150,
            "success_rate": 98.5,
            "last_tested": "2024-01-15T10:30:00Z"
        }
    ],
    "total": 50,
    "active": 45,
    "failed": 5
}
```

#### POST /proxy/add
Add new proxy:

**Request:**
```http
POST /api/v1/proxy/add
Authorization: Bearer YOUR_API_KEY
Content-Type: application/json

{
    "host": "new-proxy.example.com",
    "port": 8080,
    "type": "http",
    "username": "user",
    "password": "pass",
    "test_before_add": true
}
```

**Response:**
```json
{
    "success": true,
    "proxy_id": "proxy_new_001",
    "test_result": {
        "working": true,
        "response_time": 120,
        "ip_changed": true
    }
}
```

#### POST /proxy/test
Test proxy functionality:

**Request:**
```http
POST /api/v1/proxy/test
Authorization: Bearer YOUR_API_KEY
Content-Type: application/json

{
    "proxy_id": "proxy_001"
}
```

**Response:**
```json
{
    "success": true,
    "proxy_id": "proxy_001",
    "working": true,
    "response_time": 145,
    "ip_address": "198.51.100.50",
    "location": {
        "country": "United States",
        "city": "New York"
    }
}
```

### Tor Management

#### POST /tor/start
Start Tor service:

**Request:**
```http
POST /api/v1/tor/start
Authorization: Bearer YOUR_API_KEY
Content-Type: application/json

{
    "use_bridges": false,
    "exit_nodes": ["US", "UK"]
}
```

**Response:**
```json
{
    "success": true,
    "tor_status": "starting",
    "socks_port": 9050,
    "control_port": 9051,
    "estimated_time": 30
}
```

#### POST /tor/new-circuit
Create new Tor circuit:

**Request:**
```http
POST /api/v1/tor/new-circuit
Authorization: Bearer YOUR_API_KEY
```

**Response:**
```json
{
    "success": true,
    "circuit_id": "circuit_456789",
    "path": [
        {
            "nickname": "GuardRelay1",
            "country": "US"
        },
        {
            "nickname": "MiddleRelay1", 
            "country": "DE"
        },
        {
            "nickname": "ExitRelay1",
            "country": "UK"
        }
    ],
    "build_time": 5.2
}
```

## 🔧 Configuration API

#### GET /config
Get current configuration:

**Request:**
```http
GET /api/v1/config
Authorization: Bearer YOUR_API_KEY
```

**Response:**
```json
{
    "vpn": {
        "provider": "nordvpn",
        "protocol": "openvpn",
        "auto_connect": true,
        "kill_switch": true
    },
    "proxy": {
        "rotation_interval": 300,
        "test_before_use": true,
        "max_failures": 3
    },
    "tor": {
        "use_bridges": false,
        "strict_nodes": false
    },
    "security": {
        "dns_leak_protection": true,
        "ipv6_disable": true
    }
}
```

#### PUT /config
Update configuration:

**Request:**
```http
PUT /api/v1/config
Authorization: Bearer YOUR_API_KEY
Content-Type: application/json

{
    "vpn": {
        "kill_switch": true,
        "protocol": "wireguard"
    },
    "proxy": {
        "rotation_interval": 600
    }
}
```

**Response:**
```json
{
    "success": true,
    "updated_fields": [
        "vpn.kill_switch",
        "vpn.protocol", 
        "proxy.rotation_interval"
    ],
    "restart_required": false
}
```

## 📊 Monitoring API

#### GET /metrics
Get system metrics:

**Request:**
```http
GET /api/v1/metrics
Authorization: Bearer YOUR_API_KEY
```

**Response:**
```json
{
    "system": {
        "cpu_usage": 15.2,
        "memory_usage": 45.8,
        "uptime": 86400
    },
    "network": {
        "connections": {
            "total": 1,
            "vpn": 1,
            "proxy": 0,
            "tor": 0
        },
        "data_usage": {
            "today": 1073741824,
            "this_month": 32212254720
        }
    },
    "security": {
        "dns_leaks": 0,
        "ip_leaks": 0,
        "last_scan": "2024-01-15T10:00:00Z"
    }
}
```

#### GET /logs
Retrieve system logs:

**Request:**
```http
GET /api/v1/logs?level=info&limit=100
Authorization: Bearer YOUR_API_KEY
```

**Response:**
```json
{
    "logs": [
        {
            "timestamp": "2024-01-15T10:30:00Z",
            "level": "INFO",
            "component": "vpn",
            "message": "Connected to server us-west-1"
        }
    ],
    "total": 1500,
    "page": 1,
    "per_page": 100
}
```

## 🧪 Testing API

#### GET /ip-check
Check current IP address:

**Request:**
```http
GET /api/v1/ip-check
Authorization: Bearer YOUR_API_KEY
```

**Response:**
```json
{
    "ip_address": "203.0.113.1",
    "location": {
        "country": "United States",
        "city": "New York",
        "region": "NY",
        "postal_code": "10001",
        "coordinates": {
            "latitude": 40.7128,
            "longitude": -74.0060
        }
    },
    "isp": "Example ISP",
    "organization": "Example Org",
    "timezone": "America/New_York"
}
```

#### POST /speed-test
Run connection speed test:

**Request:**
```http
POST /api/v1/speed-test
Authorization: Bearer YOUR_API_KEY
Content-Type: application/json

{
    "server": "auto",
    "duration": 30
}
```

**Response:**
```json
{
    "success": true,
    "test_id": "speed_123456",
    "server": {
        "name": "Speedtest Server",
        "location": "New York, NY",
        "distance": 25.5
    },
    "results": {
        "download": 50.25,
        "upload": 25.10,
        "ping": 15,
        "jitter": 2.5
    },
    "test_duration": 28.5
}
```

#### POST /security-scan
Run comprehensive security scan:

**Request:**
```http
POST /api/v1/security-scan
Authorization: Bearer YOUR_API_KEY
Content-Type: application/json

{
    "tests": ["dns_leak", "webrtc_leak", "ip_leak"]
}
```

**Response:**
```json
{
    "success": true,
    "scan_id": "scan_789012",
    "results": {
        "dns_leak": {
            "detected": false,
            "servers": ["8.8.8.8", "8.8.4.4"]
        },
        "webrtc_leak": {
            "detected": false
        },
        "ip_leak": {
            "detected": false,
            "ipv4": "203.0.113.1",
            "ipv6": null
        }
    },
    "scan_duration": 12.3,
    "timestamp": "2024-01-15T10:30:00Z"
}
```

## 📋 WebSocket API

### Real-time Events
Connect to WebSocket for real-time updates:

```javascript
const ws = new WebSocket('ws://localhost:8080/api/v1/ws');

ws.onmessage = function(event) {
    const data = JSON.parse(event.data);
    console.log('Event:', data);
};
```

### Event Types

#### Connection Events
```json
{
    "type": "connection_status",
    "data": {
        "status": "connected",
        "service": "vpn",
        "server": "us-west-1"
    }
}
```

#### Rotation Events
```json
{
    "type": "ip_rotation",
    "data": {
        "old_ip": "203.0.113.1",
        "new_ip": "198.51.100.1",
        "rotation_time": 8.5
    }
}
```

#### Error Events
```json
{
    "type": "error",
    "data": {
        "code": "CONNECTION_FAILED",
        "message": "Failed to connect to VPN server",
        "details": {
            "server": "us-west-1",
            "error": "Authentication failed"
        }
    }
}
```

## 🔒 Error Handling

### HTTP Status Codes
- `200` - Success
- `400` - Bad Request
- `401` - Unauthorized  
- `403` - Forbidden
- `404` - Not Found
- `429` - Rate Limited
- `500` - Internal Server Error

### Error Response Format
```json
{
    "success": false,
    "error": {
        "code": "INVALID_SERVER",
        "message": "The specified server is not available",
        "details": {
            "server": "invalid-server",
            "available_servers": ["us-west-1", "us-east-1"]
        }
    }
}
```

### Common Error Codes
- `INVALID_API_KEY` - API key is invalid or expired
- `RATE_LIMITED` - Too many requests
- `CONNECTION_FAILED` - Unable to establish connection
- `INVALID_SERVER` - Server not found or unavailable
- `PROXY_FAILED` - Proxy connection failed
- `TOR_UNAVAILABLE` - Tor service not available
- `CONFIG_ERROR` - Configuration validation failed

## 🚀 SDK Examples

### Python SDK
```python
import requests

class CyberRotateAPI:
    def __init__(self, api_key, base_url='http://localhost:8080/api/v1'):
        self.api_key = api_key
        self.base_url = base_url
        self.headers = {
            'Authorization': f'Bearer {api_key}',
            'Content-Type': 'application/json'
        }
    
    def connect_vpn(self, server=None, country=None):
        data = {}
        if server:
            data['server'] = server
        if country:
            data['country'] = country
        
        response = requests.post(
            f'{self.base_url}/connect',
            json={'service': 'vpn', **data},
            headers=self.headers
        )
        return response.json()
    
    def get_status(self):
        response = requests.get(
            f'{self.base_url}/status',
            headers=self.headers
        )
        return response.json()
    
    def rotate_ip(self, method='vpn'):
        response = requests.post(
            f'{self.base_url}/rotate',
            json={'method': method},
            headers=self.headers
        )
        return response.json()

# Usage
api = CyberRotateAPI('your_api_key_here')
result = api.connect_vpn(country='US')
print(result)
```

### JavaScript SDK
```javascript
class CyberRotateAPI {
    constructor(apiKey, baseUrl = 'http://localhost:8080/api/v1') {
        this.apiKey = apiKey;
        this.baseUrl = baseUrl;
        this.headers = {
            'Authorization': `Bearer ${apiKey}`,
            'Content-Type': 'application/json'
        };
    }
    
    async connectVPN(options = {}) {
        const response = await fetch(`${this.baseUrl}/connect`, {
            method: 'POST',
            headers: this.headers,
            body: JSON.stringify({
                service: 'vpn',
                ...options
            })
        });
        return response.json();
    }
    
    async getStatus() {
        const response = await fetch(`${this.baseUrl}/status`, {
            headers: this.headers
        });
        return response.json();
    }
    
    async rotateIP(method = 'vpn') {
        const response = await fetch(`${this.baseUrl}/rotate`, {
            method: 'POST',
            headers: this.headers,
            body: JSON.stringify({ method })
        });
        return response.json();
    }
}

// Usage
const api = new CyberRotateAPI('your_api_key_here');
api.connectVPN({ country: 'US' }).then(result => {
    console.log(result);
});
```

## 📚 Rate Limiting

### Limits
- **Standard**: 100 requests/minute
- **Premium**: 1000 requests/minute
- **Enterprise**: 10000 requests/minute

### Headers
```http
X-RateLimit-Limit: 100
X-RateLimit-Remaining: 95
X-RateLimit-Reset: 1642248000
```

### Handling Rate Limits
```python
import time
import requests

def api_request_with_retry(url, headers, data=None, max_retries=3):
    for attempt in range(max_retries):
        response = requests.post(url, json=data, headers=headers)
        
        if response.status_code == 429:
            reset_time = int(response.headers.get('X-RateLimit-Reset', 0))
            wait_time = max(reset_time - int(time.time()), 1)
            time.sleep(wait_time)
            continue
            
        return response.json()
    
    raise Exception("Max retries exceeded")
```

---

**Next**: [VPN Setup](07-vpn-setup.md) | [Back to Manual](README.md)
