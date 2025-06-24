# Developer Guide

Comprehensive guide for developers who want to contribute to CyberRotate Pro, extend its functionality, or integrate it into their applications.

## 🚀 Development Overview

CyberRotate Pro is built with modularity and extensibility in mind, making it easy for developers to contribute and customize.

### Architecture Overview
```
CyberRotate Pro
├── core/                 # Core functionality modules
│   ├── proxy_manager.py  # Proxy management and rotation
│   ├── openvpn_manager.py # VPN connection management
│   ├── tor_controller.py # Tor network integration
│   ├── network_monitor.py # Network monitoring and testing
│   └── security_utils.py # Security and privacy features
├── ui/                   # User interface components
│   ├── gui_application.py # Tkinter GUI application
│   ├── cli_interface.py  # Command-line interface
│   └── web_interface.py  # Web-based interface
├── api/                  # REST API server
│   ├── server.py         # Flask/FastAPI server
│   ├── endpoints/        # API endpoint definitions
│   └── middleware/       # Authentication and middleware
├── utils/                # Utility modules
│   ├── logger.py         # Logging functionality
│   ├── config_manager.py # Configuration management
│   └── stats_collector.py # Statistics and analytics
├── plugins/              # Plugin system
│   ├── providers/        # VPN/Proxy provider plugins
│   ├── protocols/        # Protocol implementation plugins
│   └── security/         # Security feature plugins
└── tests/                # Test suite
    ├── unit/             # Unit tests
    ├── integration/      # Integration tests
    └── e2e/              # End-to-end tests
```

### Technology Stack
- **Language**: Python 3.8+
- **GUI Framework**: Tkinter (with optional PyQt5/6)
- **API Framework**: Flask/FastAPI
- **Network Libraries**: requests, urllib3, pycurl
- **VPN Integration**: OpenVPN, WireGuard clients
- **Tor Integration**: stem (Tor controller library)
- **Security**: cryptography, pyOpenSSL
- **Testing**: pytest, unittest
- **Documentation**: Sphinx, MkDocs

## 🔧 Development Environment Setup

### Prerequisites
```bash
# Python 3.8 or higher
python --version

# Git for version control
git --version

# Virtual environment support
python -m venv --help
```

### Environment Setup

#### 1. Clone Repository
```bash
# Clone the repository
git clone https://github.com/ZehraSec/cyberrotate-pro.git
cd cyberrotate-pro

# Create development branch
git checkout -b feature/your-feature-name
```

#### 2. Virtual Environment
```bash
# Create virtual environment
python -m venv cyberrotate-dev
source cyberrotate-dev/bin/activate  # Linux/macOS
cyberrotate-dev\Scripts\activate     # Windows

# Upgrade pip
pip install --upgrade pip setuptools wheel
```

#### 3. Development Dependencies
```bash
# Install development dependencies
pip install -r requirements-dev.txt

# Install in development mode
pip install -e .

# Install pre-commit hooks
pre-commit install
```

#### 4. IDE Configuration

**Visual Studio Code**
```json
{
    "python.defaultInterpreterPath": "./cyberrotate-dev/bin/python",
    "python.linting.enabled": true,
    "python.linting.pylintEnabled": true,
    "python.linting.flake8Enabled": true,
    "python.formatting.provider": "black",
    "python.sortImports.path": "isort",
    "editor.formatOnSave": true
}
```

**PyCharm**
- Set interpreter to virtual environment Python
- Enable code style checks (PEP 8)
- Configure pytest as test runner
- Enable git integration

### Development Tools

#### Code Quality Tools
```bash
# Code formatting
black --line-length 88 .
isort .

# Linting
flake8 .
pylint cyberrotate/

# Type checking
mypy cyberrotate/

# Security scanning
bandit -r cyberrotate/
```

#### Testing Tools
```bash
# Run unit tests
pytest tests/unit/

# Run integration tests
pytest tests/integration/

# Run with coverage
pytest --cov=cyberrotate tests/

# Generate coverage report
coverage html
```

## 📦 Project Structure

### Core Modules

#### proxy_manager.py
```python
"""
Proxy Management Module
Handles proxy configuration, testing, and rotation
"""

class ProxyManager:
    def __init__(self, logger):
        self.logger = logger
        self.proxies = []
        self.current_proxy = None
    
    def add_proxy(self, proxy_config):
        """Add a new proxy to the pool"""
        pass
    
    def test_proxy(self, proxy):
        """Test proxy connectivity and performance"""
        pass
    
    def rotate_proxy(self):
        """Rotate to the next available proxy"""
        pass
    
    def get_working_proxies(self):
        """Return list of working proxies"""
        pass
```

#### openvpn_manager.py
```python
"""
VPN Management Module
Handles VPN connections using OpenVPN
"""

class OpenVPNManager:
    def __init__(self, logger):
        self.logger = logger
        self.process = None
        self.config = None
    
    def connect(self, config_file):
        """Connect to VPN using config file"""
        pass
    
    def disconnect(self):
        """Disconnect from VPN"""
        pass
    
    def get_status(self):
        """Get current VPN connection status"""
        pass
```

#### security_utils.py
```python
"""
Security Utilities Module
Implements security and privacy features
"""

class SecurityUtils:
    def __init__(self, logger):
        self.logger = logger
    
    def check_dns_leaks(self):
        """Check for DNS leaks"""
        pass
    
    def enable_kill_switch(self):
        """Enable network kill switch"""
        pass
    
    def test_webrtc_leaks(self):
        """Test for WebRTC IP leaks"""
        pass
```

### Configuration Management

#### config_manager.py
```python
"""
Configuration Management
Handles loading, saving, and validating configuration
"""

import json
import os
from typing import Dict, Any

class ConfigManager:
    def __init__(self, config_file: str = "config/config.json"):
        self.config_file = config_file
        self.config = {}
        self.load_config()
    
    def load_config(self) -> Dict[str, Any]:
        """Load configuration from file"""
        try:
            with open(self.config_file, 'r') as f:
                self.config = json.load(f)
        except FileNotFoundError:
            self.config = self.get_default_config()
            self.save_config()
        return self.config
    
    def save_config(self) -> bool:
        """Save configuration to file"""
        try:
            os.makedirs(os.path.dirname(self.config_file), exist_ok=True)
            with open(self.config_file, 'w') as f:
                json.dump(self.config, f, indent=2)
            return True
        except Exception as e:
            self.logger.error(f"Failed to save config: {e}")
            return False
    
    def get(self, key: str, default=None):
        """Get configuration value with dot notation"""
        keys = key.split('.')
        value = self.config
        for k in keys:
            value = value.get(k, {})
        return value if value != {} else default
    
    def set(self, key: str, value: Any) -> bool:
        """Set configuration value with dot notation"""
        keys = key.split('.')
        config = self.config
        for k in keys[:-1]:
            config = config.setdefault(k, {})
        config[keys[-1]] = value
        return self.save_config()
```

## 🔌 Plugin System

### Plugin Architecture

CyberRotate Pro uses a modular plugin system for extending functionality.

#### Plugin Base Classes
```python
"""
Base classes for plugin development
"""

from abc import ABC, abstractmethod
from typing import Dict, Any, List

class ProviderPlugin(ABC):
    """Base class for VPN/Proxy provider plugins"""
    
    @abstractmethod
    def get_name(self) -> str:
        """Return provider name"""
        pass
    
    @abstractmethod
    def get_servers(self) -> List[Dict[str, Any]]:
        """Return list of available servers"""
        pass
    
    @abstractmethod
    def connect(self, server_config: Dict[str, Any]) -> bool:
        """Connect to specified server"""
        pass
    
    @abstractmethod
    def disconnect(self) -> bool:
        """Disconnect from server"""
        pass

class SecurityPlugin(ABC):
    """Base class for security feature plugins"""
    
    @abstractmethod
    def get_name(self) -> str:
        """Return security feature name"""
        pass
    
    @abstractmethod
    def initialize(self, config: Dict[str, Any]) -> bool:
        """Initialize security feature"""
        pass
    
    @abstractmethod
    def check_security(self) -> Dict[str, Any]:
        """Perform security check"""
        pass
```

#### Creating Custom Plugins

**Example: Custom Proxy Provider Plugin**
```python
"""
Custom proxy provider plugin example
"""

from plugins.base import ProviderPlugin
import requests

class CustomProxyProvider(ProviderPlugin):
    def __init__(self, config):
        self.config = config
        self.api_endpoint = config.get('api_endpoint')
        self.api_key = config.get('api_key')
    
    def get_name(self) -> str:
        return "CustomProxy"
    
    def get_servers(self) -> List[Dict[str, Any]]:
        """Fetch proxy list from provider API"""
        try:
            response = requests.get(
                f"{self.api_endpoint}/proxies",
                headers={"Authorization": f"Bearer {self.api_key}"}
            )
            return response.json()['proxies']
        except Exception as e:
            self.logger.error(f"Failed to fetch proxies: {e}")
            return []
    
    def connect(self, server_config: Dict[str, Any]) -> bool:
        """Configure system to use the proxy"""
        try:
            # Implementation specific to your proxy setup
            proxy_url = f"http://{server_config['host']}:{server_config['port']}"
            # Configure proxy settings
            return True
        except Exception as e:
            self.logger.error(f"Failed to connect: {e}")
            return False
    
    def disconnect(self) -> bool:
        """Remove proxy configuration"""
        try:
            # Remove proxy settings
            return True
        except Exception as e:
            self.logger.error(f"Failed to disconnect: {e}")
            return False
```

#### Plugin Registration
```python
"""
Plugin registration system
"""

class PluginManager:
    def __init__(self):
        self.providers = {}
        self.security_plugins = {}
    
    def register_provider(self, plugin_class, config=None):
        """Register a provider plugin"""
        plugin = plugin_class(config or {})
        self.providers[plugin.get_name()] = plugin
    
    def register_security_plugin(self, plugin_class, config=None):
        """Register a security plugin"""
        plugin = plugin_class(config or {})
        self.security_plugins[plugin.get_name()] = plugin
    
    def get_provider(self, name):
        """Get provider plugin by name"""
        return self.providers.get(name)
    
    def list_providers(self):
        """List all registered providers"""
        return list(self.providers.keys())

# Usage
plugin_manager = PluginManager()
plugin_manager.register_provider(CustomProxyProvider, {
    'api_endpoint': 'https://api.customprovider.com',
    'api_key': 'your-api-key'
})
```

## 🧪 Testing Framework

### Test Structure

#### Unit Tests
```python
"""
Example unit test for proxy manager
"""

import unittest
from unittest.mock import Mock, patch
from core.proxy_manager import ProxyManager

class TestProxyManager(unittest.TestCase):
    def setUp(self):
        self.logger = Mock()
        self.proxy_manager = ProxyManager(self.logger)
    
    def test_add_proxy(self):
        """Test adding a proxy to the pool"""
        proxy_config = {
            'host': '192.168.1.100',
            'port': 8080,
            'type': 'http'
        }
        
        result = self.proxy_manager.add_proxy(proxy_config)
        self.assertTrue(result)
        self.assertEqual(len(self.proxy_manager.proxies), 1)
    
    @patch('requests.get')
    def test_test_proxy(self, mock_get):
        """Test proxy connectivity testing"""
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = {'ip': '192.168.1.100'}
        
        proxy = {'host': '192.168.1.100', 'port': 8080}
        result = self.proxy_manager.test_proxy(proxy)
        
        self.assertTrue(result['working'])
        self.assertLess(result['response_time'], 5000)
    
    def test_rotate_proxy(self):
        """Test proxy rotation"""
        # Add test proxies
        self.proxy_manager.add_proxy({'host': '1.1.1.1', 'port': 8080})
        self.proxy_manager.add_proxy({'host': '2.2.2.2', 'port': 8080})
        
        initial_proxy = self.proxy_manager.current_proxy
        self.proxy_manager.rotate_proxy()
        new_proxy = self.proxy_manager.current_proxy
        
        self.assertNotEqual(initial_proxy, new_proxy)

if __name__ == '__main__':
    unittest.main()
```

#### Integration Tests
```python
"""
Integration test example
"""

import pytest
import time
from core.proxy_manager import ProxyManager
from core.network_monitor import NetworkMonitor

class TestProxyIntegration:
    @pytest.fixture
    def setup_managers(self):
        logger = Mock()
        proxy_manager = ProxyManager(logger)
        network_monitor = NetworkMonitor(logger)
        return proxy_manager, network_monitor
    
    def test_proxy_rotation_changes_ip(self, setup_managers):
        """Test that proxy rotation actually changes IP"""
        proxy_manager, network_monitor = setup_managers
        
        # Get initial IP
        initial_ip = network_monitor.get_public_ip()
        
        # Add and connect to proxy
        proxy_manager.add_proxy({
            'host': 'working-proxy.com',
            'port': 8080,
            'type': 'http'
        })
        proxy_manager.rotate_proxy()
        
        # Wait for connection
        time.sleep(5)
        
        # Check if IP changed
        new_ip = network_monitor.get_public_ip()
        assert initial_ip != new_ip
    
    def test_vpn_proxy_chain(self, setup_managers):
        """Test VPN + Proxy chaining"""
        # Implementation for testing VPN + Proxy combination
        pass
```

#### End-to-End Tests
```python
"""
End-to-end test example
"""

from selenium import webdriver
from selenium.webdriver.common.by import By
import subprocess
import time

class TestE2E:
    def setup_method(self):
        """Setup for each test"""
        # Start CyberRotate Pro
        self.process = subprocess.Popen([
            'python', 'ip_rotator.py', '--api', '--port', '8080'
        ])
        time.sleep(5)  # Wait for startup
        
        # Setup browser with proxy
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument('--proxy-server=socks5://127.0.0.1:9150')
        self.driver = webdriver.Chrome(options=chrome_options)
    
    def teardown_method(self):
        """Cleanup after each test"""
        self.driver.quit()
        self.process.terminate()
    
    def test_ip_rotation_workflow(self):
        """Test complete IP rotation workflow"""
        # Navigate to IP check site
        self.driver.get('http://httpbin.org/ip')
        initial_ip = self.driver.find_element(By.TAG_NAME, 'body').text
        
        # Trigger rotation via API
        import requests
        requests.post('http://localhost:8080/api/v1/rotate')
        time.sleep(10)
        
        # Check new IP
        self.driver.refresh()
        new_ip = self.driver.find_element(By.TAG_NAME, 'body').text
        
        assert initial_ip != new_ip
```

### Test Configuration

#### pytest.ini
```ini
[tool:pytest]
testpaths = tests
python_files = test_*.py
python_functions = test_*
python_classes = Test*
addopts = 
    --verbose
    --tb=short
    --cov=cyberrotate
    --cov-report=html
    --cov-report=term-missing
markers =
    unit: Unit tests
    integration: Integration tests
    e2e: End-to-end tests
    slow: Slow tests that require network access
```

#### Running Tests
```bash
# Run all tests
pytest

# Run specific test types
pytest -m unit
pytest -m integration
pytest -m e2e

# Run with coverage
pytest --cov=cyberrotate --cov-report=html

# Run specific test file
pytest tests/unit/test_proxy_manager.py

# Run specific test
pytest tests/unit/test_proxy_manager.py::TestProxyManager::test_add_proxy

# Run tests in parallel
pytest -n auto
```

## 📝 Documentation

### Code Documentation

#### Docstring Standards
```python
"""
Use Google-style docstrings for consistency
"""

def rotate_proxy(self, country: str = None, proxy_type: str = None) -> bool:
    """Rotate to a new proxy server.
    
    Selects and connects to a new proxy server based on the specified
    criteria. If no criteria are provided, selects randomly from available
    working proxies.
    
    Args:
        country: ISO country code for proxy location (e.g., 'US', 'UK').
        proxy_type: Type of proxy ('http', 'socks4', 'socks5').
    
    Returns:
        True if rotation was successful, False otherwise.
    
    Raises:
        ProxyConnectionError: If unable to connect to any available proxy.
        ConfigurationError: If proxy configuration is invalid.
    
    Example:
        >>> proxy_manager = ProxyManager(logger)
        >>> proxy_manager.rotate_proxy(country='US', proxy_type='http')
        True
    """
    pass
```

#### Type Hints
```python
"""
Use type hints for better code documentation and IDE support
"""

from typing import Dict, List, Optional, Union, Any
from dataclasses import dataclass

@dataclass
class ProxyConfig:
    """Configuration for a proxy server."""
    host: str
    port: int
    type: str
    username: Optional[str] = None
    password: Optional[str] = None
    country: Optional[str] = None

class ProxyManager:
    def __init__(self, logger: logging.Logger) -> None:
        self.proxies: List[ProxyConfig] = []
        self.current_proxy: Optional[ProxyConfig] = None
    
    def add_proxy(self, config: Union[Dict[str, Any], ProxyConfig]) -> bool:
        """Add proxy with type checking."""
        pass
    
    def get_proxies_by_country(self, country: str) -> List[ProxyConfig]:
        """Get proxies filtered by country."""
        pass
```

### API Documentation

#### OpenAPI/Swagger Documentation
```python
"""
API documentation using FastAPI and automatic OpenAPI generation
"""

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional

app = FastAPI(
    title="CyberRotate Pro API",
    description="REST API for IP rotation and network privacy management",
    version="2.1.0"
)

class ConnectionRequest(BaseModel):
    """Request model for connection endpoint."""
    service: str
    server: Optional[str] = None
    country: Optional[str] = None
    
    class Config:
        schema_extra = {
            "example": {
                "service": "vpn",
                "server": "us-west-1",
                "country": "US"
            }
        }

@app.post("/api/v1/connect", response_model=ConnectionResponse)
async def connect(request: ConnectionRequest):
    """
    Establish a new connection.
    
    Connects to the specified service (VPN, proxy, or Tor) with optional
    server and country preferences.
    
    - **service**: Connection service type (vpn, proxy, tor)
    - **server**: Specific server name (optional)
    - **country**: Preferred country code (optional)
    """
    pass
```

### User Documentation

#### Generating Documentation
```bash
# Install documentation tools
pip install sphinx sphinx-rtd-theme

# Initialize Sphinx documentation
sphinx-quickstart docs

# Generate API documentation
sphinx-apidoc -o docs/api cyberrotate

# Build HTML documentation
cd docs
make html

# Build PDF documentation
make latexpdf
```

#### Documentation Structure
```
docs/
├── source/
│   ├── index.rst           # Main documentation index
│   ├── installation.rst    # Installation guide
│   ├── quickstart.rst      # Quick start guide
│   ├── api/                # API documentation
│   │   ├── core.rst        # Core modules
│   │   ├── utils.rst       # Utility modules
│   │   └── plugins.rst     # Plugin system
│   ├── development/        # Development guides
│   │   ├── contributing.rst # Contributing guidelines
│   │   ├── plugins.rst     # Plugin development
│   │   └── testing.rst     # Testing guidelines
│   └── examples/           # Code examples
├── Makefile                # Build configuration
└── conf.py                 # Sphinx configuration
```

## 🤝 Contributing Guidelines

### Getting Started

#### First-time Contributors
1. **Fork the repository** on GitHub
2. **Clone your fork** locally
3. **Create a feature branch** for your changes
4. **Set up development environment** (see above)
5. **Make your changes** following coding standards
6. **Write tests** for new functionality
7. **Update documentation** as needed
8. **Submit a pull request**

#### Development Workflow
```bash
# 1. Create feature branch
git checkout -b feature/proxy-pool-management

# 2. Make changes and commit
git add .
git commit -m "feat: add proxy pool management functionality"

# 3. Push to your fork
git push origin feature/proxy-pool-management

# 4. Create pull request on GitHub
```

### Coding Standards

#### Python Style Guide
- **Follow PEP 8** for code style
- **Use Black** for automatic formatting
- **Use isort** for import sorting
- **Use type hints** for function signatures
- **Write docstrings** for all public functions
- **Keep line length** to 88 characters (Black default)

#### Code Review Checklist
- [ ] Code follows PEP 8 style guidelines
- [ ] All functions have docstrings
- [ ] Type hints are used appropriately
- [ ] Unit tests cover new functionality
- [ ] Integration tests pass
- [ ] Documentation is updated
- [ ] No security vulnerabilities introduced
- [ ] Performance impact is acceptable

### Pull Request Guidelines

#### PR Title Format
```
<type>(<scope>): <description>

Examples:
feat(proxy): add support for SOCKS6 protocol
fix(vpn): resolve connection timeout issue
docs(api): update authentication examples
test(security): add WebRTC leak detection tests
```

#### PR Description Template
```markdown
## Description
Brief description of changes

## Type of Change
- [ ] Bug fix (non-breaking change which fixes an issue)
- [ ] New feature (non-breaking change which adds functionality)
- [ ] Breaking change (fix or feature that would cause existing functionality to not work as expected)
- [ ] Documentation update

## Testing
- [ ] Unit tests pass
- [ ] Integration tests pass
- [ ] Manual testing completed

## Checklist
- [ ] Code follows style guidelines
- [ ] Self-review completed
- [ ] Code is commented where necessary
- [ ] Documentation updated
- [ ] No merge conflicts
```

### Release Process

#### Version Management
```bash
# Update version in setup.py and __init__.py
# Follow semantic versioning (MAJOR.MINOR.PATCH)

# Create release tag
git tag -a v2.1.0 -m "Release version 2.1.0"
git push origin v2.1.0

# Create release on GitHub with changelog
```

#### Changelog Format
```markdown
# Changelog

## [2.1.0] - 2024-01-15

### Added
- New proxy pool management system
- Support for WireGuard VPN protocol
- Enhanced security monitoring dashboard

### Changed
- Improved proxy rotation algorithm
- Updated API authentication method
- Refactored configuration management

### Fixed
- VPN connection timeout issues
- DNS leak detection accuracy
- Memory leak in proxy testing

### Security
- Enhanced encryption for stored credentials
- Improved WebRTC leak prevention
```

## 🔧 Advanced Development Topics

### Performance Optimization

#### Profiling
```python
"""
Performance profiling example
"""

import cProfile
import pstats
from core.proxy_manager import ProxyManager

def profile_proxy_testing():
    """Profile proxy testing performance"""
    logger = setup_logger()
    proxy_manager = ProxyManager(logger)
    
    # Add many proxies for testing
    for i in range(1000):
        proxy_manager.add_proxy({
            'host': f'proxy{i}.example.com',
            'port': 8080 + (i % 100),
            'type': 'http'
        })
    
    # Test all proxies
    proxy_manager.test_all_proxies()

if __name__ == '__main__':
    # Run profiling
    cProfile.run('profile_proxy_testing()', 'proxy_profile.stats')
    
    # Analyze results
    stats = pstats.Stats('proxy_profile.stats')
    stats.sort_stats('cumulative')
    stats.print_stats(20)
```

#### Async Programming
```python
"""
Async implementation for better performance
"""

import asyncio
import aiohttp
from typing import List, Dict

class AsyncProxyManager:
    def __init__(self, logger):
        self.logger = logger
        self.session = None
    
    async def __aenter__(self):
        self.session = aiohttp.ClientSession()
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.session.close()
    
    async def test_proxy(self, proxy: Dict[str, str]) -> Dict[str, bool]:
        """Test single proxy asynchronously"""
        try:
            proxy_url = f"http://{proxy['host']}:{proxy['port']}"
            async with self.session.get(
                'http://httpbin.org/ip',
                proxy=proxy_url,
                timeout=aiohttp.ClientTimeout(total=30)
            ) as response:
                if response.status == 200:
                    return {'proxy': proxy, 'working': True}
        except Exception as e:
            self.logger.debug(f"Proxy {proxy['host']} failed: {e}")
        
        return {'proxy': proxy, 'working': False}
    
    async def test_proxies_batch(self, proxies: List[Dict[str, str]]) -> List[Dict]:
        """Test multiple proxies concurrently"""
        tasks = [self.test_proxy(proxy) for proxy in proxies]
        return await asyncio.gather(*tasks, return_exceptions=True)

# Usage
async def main():
    proxies = [
        {'host': 'proxy1.com', 'port': '8080'},
        {'host': 'proxy2.com', 'port': '8080'},
        # ... more proxies
    ]
    
    async with AsyncProxyManager(logger) as manager:
        results = await manager.test_proxies_batch(proxies)
        working_proxies = [r['proxy'] for r in results if r.get('working')]
        print(f"Found {len(working_proxies)} working proxies")

if __name__ == '__main__':
    asyncio.run(main())
```

### Security Considerations

#### Secure Coding Practices
```python
"""
Security best practices for CyberRotate Pro development
"""

import hashlib
import secrets
from cryptography.fernet import Fernet
from typing import str

class SecureCredentialManager:
    def __init__(self):
        self.key = self._generate_key()
        self.cipher = Fernet(self.key)
    
    def _generate_key(self) -> bytes:
        """Generate encryption key securely"""
        return Fernet.generate_key()
    
    def encrypt_password(self, password: str) -> str:
        """Encrypt password for storage"""
        return self.cipher.encrypt(password.encode()).decode()
    
    def decrypt_password(self, encrypted_password: str) -> str:
        """Decrypt password for use"""
        return self.cipher.decrypt(encrypted_password.encode()).decode()
    
    def hash_api_key(self, api_key: str) -> str:
        """Hash API key for storage"""
        salt = secrets.token_bytes(32)
        key_hash = hashlib.pbkdf2_hmac('sha256', 
                                       api_key.encode(), 
                                       salt, 
                                       100000)
        return salt.hex() + ':' + key_hash.hex()
    
    def verify_api_key(self, api_key: str, stored_hash: str) -> bool:
        """Verify API key against stored hash"""
        try:
            salt_hex, key_hash_hex = stored_hash.split(':')
            salt = bytes.fromhex(salt_hex)
            stored_key_hash = bytes.fromhex(key_hash_hex)
            
            key_hash = hashlib.pbkdf2_hmac('sha256',
                                          api_key.encode(),
                                          salt,
                                          100000)
            return key_hash == stored_key_hash
        except ValueError:
            return False

# Input validation example
def validate_proxy_config(config: Dict[str, Any]) -> bool:
    """Validate proxy configuration for security"""
    required_fields = ['host', 'port']
    
    # Check required fields
    for field in required_fields:
        if field not in config:
            raise ValueError(f"Missing required field: {field}")
    
    # Validate host (basic IP/domain validation)
    host = config['host']
    if not isinstance(host, str) or len(host) > 253:
        raise ValueError("Invalid host format")
    
    # Validate port
    port = config.get('port')
    if not isinstance(port, int) or not (1 <= port <= 65535):
        raise ValueError("Invalid port number")
    
    # Sanitize optional fields
    if 'username' in config:
        config['username'] = str(config['username'])[:64]  # Limit length
    
    return True
```

### Deployment and Distribution

#### Package Creation
```python
"""
setup.py for package distribution
"""

from setuptools import setup, find_packages
import os

# Read README for long description
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

# Read requirements
with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = [line.strip() for line in fh if line.strip() and not line.startswith("#")]

setup(
    name="cyberrotate-pro",
    version="2.1.0",
    author="Yashab Alam",
    author_email="contact@zehrasec.com",
    description="Professional IP rotation and network privacy management tool",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/ZehraSec/cyberrotate-pro",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "Intended Audience :: System Administrators",
        "Topic :: Internet :: Proxy Servers",
        "Topic :: Security",
        "Topic :: System :: Networking",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
    install_requires=requirements,
    extras_require={
        "dev": [
            "pytest>=6.0",
            "pytest-cov>=2.0",
            "black>=21.0",
            "isort>=5.0",
            "flake8>=3.8",
            "mypy>=0.800",
            "pre-commit>=2.0",
        ],
        "gui": [
            "tkinter",
            "PyQt5>=5.15",
        ],
        "api": [
            "fastapi>=0.70",
            "uvicorn>=0.15",
        ]
    },
    entry_points={
        "console_scripts": [
            "cyberrotate=cyberrotate.cli:main",
            "cyberrotate-gui=cyberrotate.gui:main",
            "cyberrotate-api=cyberrotate.api:main",
        ],
    },
    include_package_data=True,
    package_data={
        "cyberrotate": [
            "config/*.json",
            "templates/*.html",
            "static/*",
        ],
    },
)
```

#### Docker Support
```dockerfile
# Dockerfile for CyberRotate Pro
FROM python:3.9-slim

# Install system dependencies
RUN apt-get update && apt-get install -y \
    openvpn \
    tor \
    iptables \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Create non-root user
RUN useradd -m -s /bin/bash cyberrotate

# Set working directory
WORKDIR /app

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Create necessary directories
RUN mkdir -p /app/config /app/logs && \
    chown -R cyberrotate:cyberrotate /app

# Switch to non-root user
USER cyberrotate

# Expose API port
EXPOSE 8080

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8080/health || exit 1

# Default command
CMD ["python", "ip_rotator.py", "--api", "--host", "0.0.0.0", "--port", "8080"]
```

## 📚 Resources and References

### Development Resources
- **Python Official Documentation**: https://docs.python.org/3/
- **Requests Library**: https://docs.python-requests.org/
- **AsyncIO Documentation**: https://docs.python.org/3/library/asyncio.html
- **FastAPI Documentation**: https://fastapi.tiangolo.com/
- **Pytest Documentation**: https://docs.pytest.org/

### Network Programming
- **RFC 1928** - SOCKS Protocol Version 5
- **RFC 2616** - HTTP/1.1 Protocol
- **OpenVPN Documentation**: https://openvpn.net/community-resources/
- **Tor Specifications**: https://spec.torproject.org/

### Security Resources
- **OWASP Guidelines**: https://owasp.org/
- **Python Security**: https://python-security.readthedocs.io/
- **Cryptography Library**: https://cryptography.io/

---

**Next**: [API Examples](19-api-examples.md) | [Back to Manual](README.md)
