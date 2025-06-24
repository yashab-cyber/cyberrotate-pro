# API Examples and Code Integrations

This guide provides practical examples for integrating with CyberRotate Pro's REST API in various programming languages.

## 📋 Table of Contents

1. [Authentication Examples](#authentication-examples)
2. [Python Integration](#python-integration)
3. [JavaScript/Node.js Examples](#javascriptnodejs-examples)
4. [cURL Examples](#curl-examples)
5. [PHP Integration](#php-integration)
6. [Java Examples](#java-examples)
7. [C# Integration](#c-integration)
8. [PowerShell Scripts](#powershell-scripts)
9. [Common Use Cases](#common-use-cases)
10. [Error Handling](#error-handling)

---

## 🔐 Authentication Examples

### API Key Authentication

```bash
# Set your API key
export CYBERROTATE_API_KEY="your-api-key-here"

# Test authentication
curl -H "Authorization: Bearer $CYBERROTATE_API_KEY" \
     http://localhost:8080/api/v1/status
```

### Session-based Authentication

```bash
# Login and get session token
curl -X POST http://localhost:8080/api/v1/auth/login \
     -H "Content-Type: application/json" \
     -d '{"username":"admin","password":"your-password"}'

# Use session token
curl -H "Authorization: Bearer <session-token>" \
     http://localhost:8080/api/v1/status
```

---

## 🐍 Python Integration

### Basic Client Example

```python
import requests
import time
import json

class CyberRotateClient:
    def __init__(self, base_url="http://localhost:8080", api_key=None):
        self.base_url = base_url
        self.headers = {}
        if api_key:
            self.headers["Authorization"] = f"Bearer {api_key}"
    
    def get_status(self):
        """Get current rotation status"""
        response = requests.get(f"{self.base_url}/api/v1/status", headers=self.headers)
        return response.json()
    
    def start_rotation(self, rotation_type="auto", interval=60):
        """Start IP rotation"""
        data = {
            "type": rotation_type,
            "interval": interval
        }
        response = requests.post(
            f"{self.base_url}/api/v1/rotation/start",
            headers=self.headers,
            json=data
        )
        return response.json()
    
    def stop_rotation(self):
        """Stop IP rotation"""
        response = requests.post(
            f"{self.base_url}/api/v1/rotation/stop",
            headers=self.headers
        )
        return response.json()
    
    def get_current_ip(self):
        """Get current external IP address"""
        response = requests.get(
            f"{self.base_url}/api/v1/ip/current",
            headers=self.headers
        )
        return response.json()
    
    def rotate_now(self):
        """Force immediate rotation"""
        response = requests.post(
            f"{self.base_url}/api/v1/rotation/rotate",
            headers=self.headers
        )
        return response.json()

# Usage example
def main():
    client = CyberRotateClient(api_key="your-api-key")
    
    # Check status
    status = client.get_status()
    print(f"Status: {status}")
    
    # Start rotation
    result = client.start_rotation(rotation_type="vpn", interval=120)
    print(f"Rotation started: {result}")
    
    # Monitor for 5 minutes
    for i in range(5):
        ip_info = client.get_current_ip()
        print(f"Current IP: {ip_info}")
        time.sleep(60)
    
    # Stop rotation
    client.stop_rotation()

if __name__ == "__main__":
    main()
```

### Advanced Python Example with Error Handling

```python
import requests
import logging
from typing import Optional, Dict, Any
from dataclasses import dataclass

@dataclass
class RotationConfig:
    rotation_type: str = "auto"
    interval: int = 60
    vpn_provider: Optional[str] = None
    proxy_type: Optional[str] = None

class CyberRotateAdvanced:
    def __init__(self, base_url: str = "http://localhost:8080", 
                 api_key: Optional[str] = None, timeout: int = 30):
        self.base_url = base_url.rstrip('/')
        self.timeout = timeout
        self.session = requests.Session()
        
        if api_key:
            self.session.headers.update({"Authorization": f"Bearer {api_key}"})
        
        # Setup logging
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)
    
    def _make_request(self, method: str, endpoint: str, **kwargs) -> Dict[Any, Any]:
        """Make HTTP request with error handling"""
        url = f"{self.base_url}{endpoint}"
        
        try:
            response = self.session.request(method, url, timeout=self.timeout, **kwargs)
            response.raise_for_status()
            return response.json()
        
        except requests.exceptions.Timeout:
            self.logger.error(f"Request timeout for {endpoint}")
            raise
        except requests.exceptions.ConnectionError:
            self.logger.error(f"Connection error for {endpoint}")
            raise
        except requests.exceptions.HTTPError as e:
            self.logger.error(f"HTTP error {e.response.status_code} for {endpoint}")
            raise
        except ValueError:
            self.logger.error(f"Invalid JSON response from {endpoint}")
            raise
    
    def configure_rotation(self, config: RotationConfig) -> Dict[Any, Any]:
        """Configure rotation settings"""
        data = {
            "type": config.rotation_type,
            "interval": config.interval
        }
        
        if config.vpn_provider:
            data["vpn_provider"] = config.vpn_provider
        if config.proxy_type:
            data["proxy_type"] = config.proxy_type
        
        return self._make_request("POST", "/api/v1/rotation/configure", json=data)
    
    def get_rotation_history(self, limit: int = 100) -> Dict[Any, Any]:
        """Get rotation history"""
        params = {"limit": limit}
        return self._make_request("GET", "/api/v1/rotation/history", params=params)
    
    def test_connection(self, connection_type: str = "all") -> Dict[Any, Any]:
        """Test connections (VPN, Proxy, Tor)"""
        data = {"type": connection_type}
        return self._make_request("POST", "/api/v1/test/connection", json=data)

# Usage
config = RotationConfig(rotation_type="vpn", interval=300, vpn_provider="nordvpn")
client = CyberRotateAdvanced(api_key="your-key")
client.configure_rotation(config)
```

---

## 🟨 JavaScript/Node.js Examples

### Basic Node.js Client

```javascript
const axios = require('axios');

class CyberRotateAPI {
    constructor(baseURL = 'http://localhost:8080', apiKey = null) {
        this.baseURL = baseURL;
        this.apiKey = apiKey;
        
        this.client = axios.create({
            baseURL: this.baseURL,
            timeout: 30000,
            headers: apiKey ? { 'Authorization': `Bearer ${apiKey}` } : {}
        });
        
        // Add response interceptor for error handling
        this.client.interceptors.response.use(
            response => response,
            error => {
                console.error('API Error:', error.response?.data || error.message);
                return Promise.reject(error);
            }
        );
    }
    
    async getStatus() {
        const response = await this.client.get('/api/v1/status');
        return response.data;
    }
    
    async startRotation(type = 'auto', interval = 60) {
        const response = await this.client.post('/api/v1/rotation/start', {
            type,
            interval
        });
        return response.data;
    }
    
    async getCurrentIP() {
        const response = await this.client.get('/api/v1/ip/current');
        return response.data;
    }
    
    async rotateNow() {
        const response = await this.client.post('/api/v1/rotation/rotate');
        return response.data;
    }
}

// Usage example
async function main() {
    const api = new CyberRotateAPI(process.env.CYBERROTATE_URL, process.env.CYBERROTATE_API_KEY);
    
    try {
        // Check status
        const status = await api.getStatus();
        console.log('Status:', status);
        
        // Start rotation
        await api.startRotation('vpn', 120);
        console.log('Rotation started');
        
        // Monitor IP changes
        let previousIP = null;
        for (let i = 0; i < 5; i++) {
            const ipInfo = await api.getCurrentIP();
            if (ipInfo.ip !== previousIP) {
                console.log(`IP changed to: ${ipInfo.ip} (${ipInfo.country})`);
                previousIP = ipInfo.ip;
            }
            await new Promise(resolve => setTimeout(resolve, 60000));
        }
        
    } catch (error) {
        console.error('Error:', error.message);
    }
}

main();
```

### Browser JavaScript Example

```html
<!DOCTYPE html>
<html>
<head>
    <title>CyberRotate Web Dashboard</title>
</head>
<body>
    <div id="dashboard">
        <h1>CyberRotate Status</h1>
        <div id="status"></div>
        <div id="current-ip"></div>
        <button onclick="toggleRotation()">Toggle Rotation</button>
        <button onclick="rotateNow()">Rotate Now</button>
    </div>

    <script>
        class CyberRotateWeb {
            constructor(baseURL = 'http://localhost:8080', apiKey = null) {
                this.baseURL = baseURL;
                this.apiKey = apiKey;
            }
            
            async request(method, endpoint, data = null) {
                const headers = {
                    'Content-Type': 'application/json'
                };
                
                if (this.apiKey) {
                    headers['Authorization'] = `Bearer ${this.apiKey}`;
                }
                
                const config = {
                    method,
                    headers
                };
                
                if (data) {
                    config.body = JSON.stringify(data);
                }
                
                const response = await fetch(`${this.baseURL}${endpoint}`, config);
                return await response.json();
            }
            
            async getStatus() {
                return await this.request('GET', '/api/v1/status');
            }
            
            async getCurrentIP() {
                return await this.request('GET', '/api/v1/ip/current');
            }
            
            async startRotation() {
                return await this.request('POST', '/api/v1/rotation/start', {
                    type: 'auto',
                    interval: 60
                });
            }
            
            async stopRotation() {
                return await this.request('POST', '/api/v1/rotation/stop');
            }
        }
        
        const api = new CyberRotateWeb();
        let rotationActive = false;
        
        async function updateDashboard() {
            try {
                const status = await api.getStatus();
                const ipInfo = await api.getCurrentIP();
                
                document.getElementById('status').innerHTML = 
                    `<p>Rotation: ${status.rotation_active ? 'Active' : 'Inactive'}</p>`;
                
                document.getElementById('current-ip').innerHTML = 
                    `<p>Current IP: ${ipInfo.ip} (${ipInfo.country})</p>`;
                
                rotationActive = status.rotation_active;
            } catch (error) {
                console.error('Error updating dashboard:', error);
            }
        }
        
        async function toggleRotation() {
            try {
                if (rotationActive) {
                    await api.stopRotation();
                } else {
                    await api.startRotation();
                }
                await updateDashboard();
            } catch (error) {
                alert('Error toggling rotation: ' + error.message);
            }
        }
        
        async function rotateNow() {
            try {
                await api.request('POST', '/api/v1/rotation/rotate');
                setTimeout(updateDashboard, 2000); // Wait for rotation to complete
            } catch (error) {
                alert('Error rotating: ' + error.message);
            }
        }
        
        // Update dashboard every 30 seconds
        setInterval(updateDashboard, 30000);
        updateDashboard(); // Initial load
    </script>
</body>
</html>
```

---

## 🌐 cURL Examples

### Basic Operations

```bash
# Set variables
API_BASE="http://localhost:8080/api/v1"
API_KEY="your-api-key-here"

# Get status
curl -H "Authorization: Bearer $API_KEY" \
     "$API_BASE/status"

# Start rotation
curl -X POST \
     -H "Authorization: Bearer $API_KEY" \
     -H "Content-Type: application/json" \
     -d '{"type":"vpn","interval":120}' \
     "$API_BASE/rotation/start"

# Get current IP
curl -H "Authorization: Bearer $API_KEY" \
     "$API_BASE/ip/current"

# Force rotation
curl -X POST \
     -H "Authorization: Bearer $API_KEY" \
     "$API_BASE/rotation/rotate"

# Stop rotation
curl -X POST \
     -H "Authorization: Bearer $API_KEY" \
     "$API_BASE/rotation/stop"
```

### Batch Operations Script

```bash
#!/bin/bash

API_BASE="http://localhost:8080/api/v1"
API_KEY="your-api-key-here"

# Function to make API calls
api_call() {
    local method=$1
    local endpoint=$2
    local data=$3
    
    if [ -n "$data" ]; then
        curl -s -X "$method" \
             -H "Authorization: Bearer $API_KEY" \
             -H "Content-Type: application/json" \
             -d "$data" \
             "$API_BASE$endpoint"
    else
        curl -s -X "$method" \
             -H "Authorization: Bearer $API_KEY" \
             "$API_BASE$endpoint"
    fi
}

# Test multiple rotation types
echo "Testing VPN rotation..."
api_call "POST" "/rotation/start" '{"type":"vpn","interval":300}'
sleep 5

echo "Current IP with VPN:"
api_call "GET" "/ip/current" | jq '.ip'

echo "Testing Proxy rotation..."
api_call "POST" "/rotation/configure" '{"type":"proxy","interval":180}'
sleep 5

echo "Current IP with Proxy:"
api_call "GET" "/ip/current" | jq '.ip'

echo "Stopping rotation..."
api_call "POST" "/rotation/stop"
```

---

## 🐘 PHP Integration

### Basic PHP Client

```php
<?php

class CyberRotateClient {
    private $baseUrl;
    private $apiKey;
    private $timeout;
    
    public function __construct($baseUrl = 'http://localhost:8080', $apiKey = null, $timeout = 30) {
        $this->baseUrl = rtrim($baseUrl, '/');
        $this->apiKey = $apiKey;
        $this->timeout = $timeout;
    }
    
    private function makeRequest($method, $endpoint, $data = null) {
        $url = $this->baseUrl . $endpoint;
        
        $ch = curl_init();
        curl_setopt_array($ch, [
            CURLOPT_URL => $url,
            CURLOPT_RETURNTRANSFER => true,
            CURLOPT_TIMEOUT => $this->timeout,
            CURLOPT_CUSTOMREQUEST => $method,
            CURLOPT_HTTPHEADER => [
                'Content-Type: application/json',
                'Authorization: Bearer ' . $this->apiKey
            ]
        ]);
        
        if ($data !== null) {
            curl_setopt($ch, CURLOPT_POSTFIELDS, json_encode($data));
        }
        
        $response = curl_exec($ch);
        $httpCode = curl_getinfo($ch, CURLINFO_HTTP_CODE);
        curl_close($ch);
        
        if ($httpCode !== 200) {
            throw new Exception("HTTP Error: $httpCode");
        }
        
        return json_decode($response, true);
    }
    
    public function getStatus() {
        return $this->makeRequest('GET', '/api/v1/status');
    }
    
    public function startRotation($type = 'auto', $interval = 60) {
        return $this->makeRequest('POST', '/api/v1/rotation/start', [
            'type' => $type,
            'interval' => $interval
        ]);
    }
    
    public function getCurrentIP() {
        return $this->makeRequest('GET', '/api/v1/ip/current');
    }
    
    public function rotateNow() {
        return $this->makeRequest('POST', '/api/v1/rotation/rotate');
    }
}

// Usage example
try {
    $client = new CyberRotateClient('http://localhost:8080', 'your-api-key');
    
    // Get status
    $status = $client->getStatus();
    echo "Status: " . json_encode($status) . "\n";
    
    // Start rotation
    $result = $client->startRotation('vpn', 120);
    echo "Rotation started: " . json_encode($result) . "\n";
    
    // Monitor IP for 5 rotations
    for ($i = 0; $i < 5; $i++) {
        $ipInfo = $client->getCurrentIP();
        echo "Current IP: " . $ipInfo['ip'] . " (" . $ipInfo['country'] . ")\n";
        
        // Force rotation
        $client->rotateNow();
        sleep(10); // Wait for rotation to complete
    }
    
} catch (Exception $e) {
    echo "Error: " . $e->getMessage() . "\n";
}
?>
```

---

## ☕ Java Examples

### Java HTTP Client

```java
import java.net.http.HttpClient;
import java.net.http.HttpRequest;
import java.net.http.HttpResponse;
import java.net.URI;
import java.time.Duration;
import com.fasterxml.jackson.databind.ObjectMapper;
import com.fasterxml.jackson.databind.JsonNode;

public class CyberRotateClient {
    private final String baseUrl;
    private final String apiKey;
    private final HttpClient httpClient;
    private final ObjectMapper objectMapper;
    
    public CyberRotateClient(String baseUrl, String apiKey) {
        this.baseUrl = baseUrl.replaceAll("/$", "");
        this.apiKey = apiKey;
        this.httpClient = HttpClient.newBuilder()
            .connectTimeout(Duration.ofSeconds(30))
            .build();
        this.objectMapper = new ObjectMapper();
    }
    
    private JsonNode makeRequest(String method, String endpoint, Object data) throws Exception {
        HttpRequest.Builder requestBuilder = HttpRequest.newBuilder()
            .uri(URI.create(baseUrl + endpoint))
            .timeout(Duration.ofSeconds(30))
            .header("Authorization", "Bearer " + apiKey)
            .header("Content-Type", "application/json");
        
        if ("POST".equals(method) && data != null) {
            String json = objectMapper.writeValueAsString(data);
            requestBuilder.POST(HttpRequest.BodyPublishers.ofString(json));
        } else if ("GET".equals(method)) {
            requestBuilder.GET();
        }
        
        HttpRequest request = requestBuilder.build();
        HttpResponse<String> response = httpClient.send(request, 
            HttpResponse.BodyHandlers.ofString());
        
        if (response.statusCode() != 200) {
            throw new RuntimeException("HTTP Error: " + response.statusCode());
        }
        
        return objectMapper.readTree(response.body());
    }
    
    public JsonNode getStatus() throws Exception {
        return makeRequest("GET", "/api/v1/status", null);
    }
    
    public JsonNode startRotation(String type, int interval) throws Exception {
        Map<String, Object> data = Map.of(
            "type", type,
            "interval", interval
        );
        return makeRequest("POST", "/api/v1/rotation/start", data);
    }
    
    public JsonNode getCurrentIP() throws Exception {
        return makeRequest("GET", "/api/v1/ip/current", null);
    }
    
    // Usage example
    public static void main(String[] args) {
        try {
            CyberRotateClient client = new CyberRotateClient(
                "http://localhost:8080", 
                "your-api-key"
            );
            
            // Check status
            JsonNode status = client.getStatus();
            System.out.println("Status: " + status);
            
            // Start rotation
            JsonNode result = client.startRotation("vpn", 120);
            System.out.println("Rotation started: " + result);
            
            // Monitor IP
            for (int i = 0; i < 3; i++) {
                JsonNode ipInfo = client.getCurrentIP();
                System.out.println("Current IP: " + ipInfo.get("ip").asText());
                Thread.sleep(60000); // Wait 1 minute
            }
            
        } catch (Exception e) {
            e.printStackTrace();
        }
    }
}
```

---

## 🔷 C# Integration

### C# HttpClient Example

```csharp
using System;
using System.Net.Http;
using System.Text;
using System.Threading.Tasks;
using Newtonsoft.Json;
using Newtonsoft.Json.Linq;

public class CyberRotateClient
{
    private readonly HttpClient _httpClient;
    private readonly string _baseUrl;
    private readonly string _apiKey;
    
    public CyberRotateClient(string baseUrl, string apiKey)
    {
        _baseUrl = baseUrl.TrimEnd('/');
        _apiKey = apiKey;
        _httpClient = new HttpClient
        {
            Timeout = TimeSpan.FromSeconds(30)
        };
        _httpClient.DefaultRequestHeaders.Add("Authorization", $"Bearer {apiKey}");
    }
    
    private async Task<JObject> MakeRequestAsync(string method, string endpoint, object data = null)
    {
        var url = $"{_baseUrl}{endpoint}";
        HttpResponseMessage response;
        
        if (method == "GET")
        {
            response = await _httpClient.GetAsync(url);
        }
        else if (method == "POST")
        {
            var json = data != null ? JsonConvert.SerializeObject(data) : "";
            var content = new StringContent(json, Encoding.UTF8, "application/json");
            response = await _httpClient.PostAsync(url, content);
        }
        else
        {
            throw new ArgumentException($"Unsupported method: {method}");
        }
        
        response.EnsureSuccessStatusCode();
        var responseContent = await response.Content.ReadAsStringAsync();
        return JObject.Parse(responseContent);
    }
    
    public async Task<JObject> GetStatusAsync()
    {
        return await MakeRequestAsync("GET", "/api/v1/status");
    }
    
    public async Task<JObject> StartRotationAsync(string type = "auto", int interval = 60)
    {
        var data = new { type, interval };
        return await MakeRequestAsync("POST", "/api/v1/rotation/start", data);
    }
    
    public async Task<JObject> GetCurrentIPAsync()
    {
        return await MakeRequestAsync("GET", "/api/v1/ip/current");
    }
    
    public async Task<JObject> RotateNowAsync()
    {
        return await MakeRequestAsync("POST", "/api/v1/rotation/rotate");
    }
    
    public void Dispose()
    {
        _httpClient?.Dispose();
    }
}

// Usage example
class Program
{
    static async Task Main(string[] args)
    {
        var client = new CyberRotateClient("http://localhost:8080", "your-api-key");
        
        try
        {
            // Check status
            var status = await client.GetStatusAsync();
            Console.WriteLine($"Status: {status}");
            
            // Start rotation
            var result = await client.StartRotationAsync("vpn", 120);
            Console.WriteLine($"Rotation started: {result}");
            
            // Monitor for 5 minutes
            for (int i = 0; i < 5; i++)
            {
                var ipInfo = await client.GetCurrentIPAsync();
                Console.WriteLine($"Current IP: {ipInfo["ip"]} ({ipInfo["country"]})");
                await Task.Delay(60000); // Wait 1 minute
            }
        }
        catch (Exception ex)
        {
            Console.WriteLine($"Error: {ex.Message}");
        }
        finally
        {
            client.Dispose();
        }
    }
}
```

---

## 💻 PowerShell Scripts

### Basic PowerShell Module

```powershell
# CyberRotate PowerShell Module

class CyberRotateAPI {
    [string]$BaseUrl
    [string]$ApiKey
    [int]$Timeout
    
    CyberRotateAPI([string]$BaseUrl, [string]$ApiKey) {
        $this.BaseUrl = $BaseUrl.TrimEnd('/')
        $this.ApiKey = $ApiKey
        $this.Timeout = 30
    }
    
    [hashtable] MakeRequest([string]$Method, [string]$Endpoint, [hashtable]$Data = $null) {
        $Uri = "$($this.BaseUrl)$Endpoint"
        $Headers = @{
            'Authorization' = "Bearer $($this.ApiKey)"
            'Content-Type' = 'application/json'
        }
        
        $Params = @{
            Uri = $Uri
            Method = $Method
            Headers = $Headers
            TimeoutSec = $this.Timeout
        }
        
        if ($Data -and $Method -eq 'POST') {
            $Params.Body = $Data | ConvertTo-Json
        }
        
        try {
            $Response = Invoke-RestMethod @Params
            return $Response
        }
        catch {
            Write-Error "API request failed: $($_.Exception.Message)"
            throw
        }
    }
    
    [hashtable] GetStatus() {
        return $this.MakeRequest('GET', '/api/v1/status')
    }
    
    [hashtable] StartRotation([string]$Type = 'auto', [int]$Interval = 60) {
        $Data = @{
            type = $Type
            interval = $Interval
        }
        return $this.MakeRequest('POST', '/api/v1/rotation/start', $Data)
    }
    
    [hashtable] GetCurrentIP() {
        return $this.MakeRequest('GET', '/api/v1/ip/current')
    }
    
    [hashtable] RotateNow() {
        return $this.MakeRequest('POST', '/api/v1/rotation/rotate')
    }
    
    [hashtable] StopRotation() {
        return $this.MakeRequest('POST', '/api/v1/rotation/stop')
    }
}

# Usage functions
function Connect-CyberRotate {
    param(
        [string]$BaseUrl = 'http://localhost:8080',
        [string]$ApiKey
    )
    
    $Global:CyberRotateClient = [CyberRotateAPI]::new($BaseUrl, $ApiKey)
    Write-Host "Connected to CyberRotate at $BaseUrl"
}

function Get-CyberRotateStatus {
    if (-not $Global:CyberRotateClient) {
        throw "Not connected. Use Connect-CyberRotate first."
    }
    return $Global:CyberRotateClient.GetStatus()
}

function Start-CyberRotateRotation {
    param(
        [string]$Type = 'auto',
        [int]$Interval = 60
    )
    
    if (-not $Global:CyberRotateClient) {
        throw "Not connected. Use Connect-CyberRotate first."
    }
    return $Global:CyberRotateClient.StartRotation($Type, $Interval)
}

function Get-CyberRotateCurrentIP {
    if (-not $Global:CyberRotateClient) {
        throw "Not connected. Use Connect-CyberRotate first."
    }
    return $Global:CyberRotateClient.GetCurrentIP()
}

# Example usage script
function Test-CyberRotate {
    # Connect
    Connect-CyberRotate -ApiKey "your-api-key"
    
    # Check status
    $Status = Get-CyberRotateStatus
    Write-Host "Current Status: $($Status | ConvertTo-Json)"
    
    # Start rotation
    $Result = Start-CyberRotateRotation -Type "vpn" -Interval 120
    Write-Host "Rotation started: $($Result | ConvertTo-Json)"
    
    # Monitor for 3 rotations
    for ($i = 1; $i -le 3; $i++) {
        Write-Host "Check $i..."
        $IPInfo = Get-CyberRotateCurrentIP
        Write-Host "Current IP: $($IPInfo.ip) ($($IPInfo.country))"
        Start-Sleep -Seconds 60
    }
    
    # Stop rotation
    $Global:CyberRotateClient.StopRotation()
    Write-Host "Rotation stopped"
}

# Export functions
Export-ModuleMember -Function Connect-CyberRotate, Get-CyberRotateStatus, 
    Start-CyberRotateRotation, Get-CyberRotateCurrentIP, Test-CyberRotate
```

---

## 🎯 Common Use Cases

### Web Scraping with IP Rotation

```python
import requests
import time
from cyberrotate_client import CyberRotateClient

class RotatingScrap
    def __init__(self, api_key):
        self.cyber_client = CyberRotateClient(api_key=api_key)
        self.session = requests.Session()
    
    def scrape_with_rotation(self, urls, rotation_interval=120):
        """Scrape URLs with automatic IP rotation"""
        
        # Start rotation
        self.cyber_client.start_rotation(rotation_type="proxy", interval=rotation_interval)
        
        results = []
        for i, url in enumerate(urls):
            try:
                # Rotate IP every 10 requests
                if i % 10 == 0:
                    self.cyber_client.rotate_now()
                    time.sleep(5)  # Wait for rotation
                
                # Make request
                response = self.session.get(url, timeout=30)
                results.append({
                    'url': url,
                    'status': response.status_code,
                    'content': response.text,
                    'ip': self.cyber_client.get_current_ip()['ip']
                })
                
                time.sleep(2)  # Rate limiting
                
            except Exception as e:
                print(f"Error scraping {url}: {e}")
                results.append({'url': url, 'error': str(e)})
        
        # Stop rotation
        self.cyber_client.stop_rotation()
        return results

# Usage
scraper = RotatingWebScraper("your-api-key")
urls = ["http://example1.com", "http://example2.com", ...]
results = scraper.scrape_with_rotation(urls)
```

### API Testing with Different IPs

```python
def test_api_from_different_locations():
    """Test API responses from different geographic locations"""
    
    client = CyberRotateClient(api_key="your-key")
    
    # Test with different VPN locations
    locations = ["us", "uk", "jp", "de", "au"]
    results = {}
    
    for location in locations:
        # Configure VPN for specific location
        client.configure_rotation({
            "type": "vpn",
            "vpn_provider": "nordvpn",
            "location": location
        })
        
        time.sleep(10)  # Wait for connection
        
        # Test API
        ip_info = client.get_current_ip()
        api_response = requests.get("https://api.example.com/test")
        
        results[location] = {
            'ip': ip_info['ip'],
            'country': ip_info['country'],
            'api_response': api_response.json(),
            'latency': api_response.elapsed.total_seconds()
        }
    
    return results
```

### Monitoring and Alerting

```python
import smtplib
from email.mime.text import MIMEText

class CyberRotateMonitor:
    def __init__(self, api_key, email_config):
        self.client = CyberRotateClient(api_key=api_key)
        self.email_config = email_config
        self.last_status = None
    
    def check_status(self):
        """Check status and send alerts if needed"""
        try:
            status = self.client.get_status()
            
            # Check for status changes
            if self.last_status and status != self.last_status:
                self.send_alert(f"Status changed: {status}")
            
            # Check for connection issues
            if not status.get('connected'):
                self.send_alert("Connection lost!")
            
            # Check IP leak
            ip_info = self.client.get_current_ip()
            if ip_info.get('is_leaked'):
                self.send_alert(f"IP leak detected: {ip_info}")
            
            self.last_status = status
            
        except Exception as e:
            self.send_alert(f"Monitoring error: {e}")
    
    def send_alert(self, message):
        """Send email alert"""
        msg = MIMEText(message)
        msg['Subject'] = 'CyberRotate Alert'
        msg['From'] = self.email_config['from']
        msg['To'] = self.email_config['to']
        
        with smtplib.SMTP(self.email_config['smtp_server']) as server:
            server.send_message(msg)

# Usage
monitor = CyberRotateMonitor("your-api-key", {
    'smtp_server': 'smtp.gmail.com',
    'from': 'alerts@yourdomain.com',
    'to': 'admin@yourdomain.com'
})

# Run monitoring loop
while True:
    monitor.check_status()
    time.sleep(300)  # Check every 5 minutes
```

---

## ⚠️ Error Handling

### Common Error Responses

```json
{
    "error": "authentication_failed",
    "message": "Invalid API key",
    "code": 401
}

{
    "error": "rotation_failed",
    "message": "No available VPN servers",
    "code": 503
}

{
    "error": "rate_limit_exceeded",
    "message": "Too many requests",
    "code": 429,
    "retry_after": 60
}
```

### Error Handling Best Practices

```python
import time
from typing import Optional

class CyberRotateError(Exception):
    def __init__(self, message: str, code: Optional[int] = None, retry_after: Optional[int] = None):
        self.message = message
        self.code = code
        self.retry_after = retry_after
        super().__init__(message)

def robust_api_call(client, operation, max_retries=3, backoff_factor=2):
    """Make API calls with retry logic and proper error handling"""
    
    for attempt in range(max_retries):
        try:
            if operation == "start_rotation":
                return client.start_rotation()
            elif operation == "get_status":
                return client.get_status()
            elif operation == "rotate_now":
                return client.rotate_now()
            
        except requests.exceptions.HTTPError as e:
            if e.response.status_code == 429:  # Rate limit
                retry_after = int(e.response.headers.get('Retry-After', 60))
                print(f"Rate limited. Waiting {retry_after} seconds...")
                time.sleep(retry_after)
                continue
            
            elif e.response.status_code in [502, 503, 504]:  # Server errors
                wait_time = backoff_factor ** attempt
                print(f"Server error. Retrying in {wait_time} seconds...")
                time.sleep(wait_time)
                continue
            
            else:
                raise CyberRotateError(f"HTTP {e.response.status_code}: {e.response.text}")
        
        except requests.exceptions.ConnectionError:
            wait_time = backoff_factor ** attempt
            print(f"Connection error. Retrying in {wait_time} seconds...")
            time.sleep(wait_time)
            continue
        
        except requests.exceptions.Timeout:
            print(f"Request timeout on attempt {attempt + 1}")
            if attempt == max_retries - 1:
                raise CyberRotateError("Request timed out after all retries")
            continue
    
    raise CyberRotateError(f"Operation failed after {max_retries} attempts")
```

---

## 📖 Additional Resources

- **API Reference**: See [06-api-reference.md](06-api-reference.md) for complete endpoint documentation
- **CLI Guide**: Check [05-cli-guide.md](05-cli-guide.md) for command-line alternatives
- **Troubleshooting**: Visit [14-troubleshooting.md](14-troubleshooting.md) for common API issues
- **Support**: Contact support via [17-support.md](17-support.md) for integration help

---

**Need Help?**

If you need assistance with API integration or have questions about these examples, please:

1. Check the [FAQ](16-faq.md) for common questions
2. Review the [API Reference](06-api-reference.md) for detailed documentation
3. Contact support through our [Support Channels](17-support.md)

---

*This guide is part of the CyberRotate Pro manual. For more information, visit the [main manual page](README.md).*
