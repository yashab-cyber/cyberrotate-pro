#!/usr/bin/env python3
"""
Proxy Manager - Handles proxy connections and rotation
Created by Yashab Alam - Founder & CEO of ZehraSec
"""

import random
import time
import logging
import requests
import json
import os
from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass
import threading
from concurrent.futures import ThreadPoolExecutor, as_completed

@dataclass
class ProxyConfig:
    """Proxy configuration details"""
    host: str
    port: int
    username: Optional[str] = None
    password: Optional[str] = None
    proxy_type: str = 'http'  # http, https, socks4, socks5
    country: Optional[str] = None
    is_working: bool = True
    response_time: float = 0.0
    last_tested: Optional[float] = None

class ProxyManager:
    """
    Proxy Connection Manager
    
    Manages proxy connections for IP rotation including:
    - Proxy validation and testing
    - Proxy rotation and selection
    - Performance monitoring
    - Proxy source management
    """
    
    def __init__(self, logger: logging.Logger):
        """Initialize proxy manager"""
        self.logger = logger
        self.proxies = []
        self.current_proxy = None
        self.working_proxies = []
        self.failed_proxies = []
        
        # Configuration
        self.test_timeout = 10
        self.max_retries = 3
        self.rotation_count = 0
        
        # Load proxy sources
        self._load_proxy_sources()
        
        self.logger.info("Proxy Manager initialized")
    
    def _load_proxy_sources(self):
        """Load proxies from various sources"""
        # Load from configuration files
        self._load_from_files()
        
        # Load from free proxy APIs (if configured)
        self._load_from_apis()
        
        if not self.proxies:
            self.logger.warning("No proxies loaded")
            self._create_sample_proxies()
        else:
            self.logger.info(f"Loaded {len(self.proxies)} proxies")
    
    def _load_from_files(self):
        """Load proxies from configuration files"""
        proxy_files = [
            'config/proxies/http_proxies.txt',
            'config/proxies/socks_proxies.txt',
            'config/proxies/custom_proxies.txt'
        ]
        
        for file_path in proxy_files:
            if os.path.exists(file_path):
                try:
                    with open(file_path, 'r') as f:
                        for line in f:
                            line = line.strip()
                            if line and not line.startswith('#'):
                                proxy = self._parse_proxy_line(line)
                                if proxy:
                                    self.proxies.append(proxy)
                except Exception as e:
                    self.logger.error(f"Error loading proxies from {file_path}: {e}")
    
    def _parse_proxy_line(self, line: str) -> Optional[ProxyConfig]:
        """Parse a proxy line from configuration file"""
        try:
            # Format: type://[username:password@]host:port
            # or simple: host:port
            
            if '://' in line:
                parts = line.split('://')
                proxy_type = parts[0].lower()
                connection_string = parts[1]
            else:
                proxy_type = 'http'
                connection_string = line
            
            # Parse authentication
            username = None
            password = None
            
            if '@' in connection_string:
                auth_part, connection_string = connection_string.split('@', 1)
                if ':' in auth_part:
                    username, password = auth_part.split(':', 1)
            
            # Parse host and port
            if ':' in connection_string:
                host, port_str = connection_string.rsplit(':', 1)
                port = int(port_str)
            else:
                self.logger.warning(f"Invalid proxy format: {line}")
                return None
            
            return ProxyConfig(
                host=host,
                port=port,
                username=username,
                password=password,
                proxy_type=proxy_type
            )
            
        except Exception as e:
            self.logger.error(f"Error parsing proxy line '{line}': {e}")
            return None
    
    def _load_from_apis(self):
        """Load proxies from free proxy APIs"""
        # This is a placeholder for loading from proxy APIs
        # In a real implementation, you would integrate with proxy providers
        pass
    
    def _create_sample_proxies(self):
        """Create sample proxy configurations for testing"""
        # Create proxy directory if it doesn't exist
        os.makedirs('config/proxies', exist_ok=True)
        
        sample_proxies = [
            "# HTTP Proxies - Add your own proxies here",
            "# Format: host:port or username:password@host:port",
            "# Example: 192.168.1.100:8080",
            "# Example: user:pass@proxy.example.com:3128",
            "",
            "# SOCKS Proxies",
            "# socks5://127.0.0.1:1080",
        ]
        
        try:
            with open('config/proxies/http_proxies.txt', 'w') as f:
                f.write('\n'.join(sample_proxies))
            
            self.logger.info("Created sample proxy configuration files")
        except Exception as e:
            self.logger.error(f"Error creating sample proxy files: {e}")
    
    def test_proxy(self, proxy: ProxyConfig) -> bool:
        """Test if a proxy is working"""
        try:
            # Create proxy configuration for requests
            proxy_dict = self._get_proxy_dict(proxy)
            
            start_time = time.time()
            
            # Test with a simple HTTP request
            response = requests.get(
                'https://httpbin.org/ip',
                proxies=proxy_dict,
                timeout=self.test_timeout,
                verify=False
            )
            
            response_time = time.time() - start_time
            
            if response.status_code == 200:
                proxy.is_working = True
                proxy.response_time = response_time
                proxy.last_tested = time.time()
                return True
            else:
                proxy.is_working = False
                return False
                
        except Exception as e:
            self.logger.debug(f"Proxy test failed for {proxy.host}:{proxy.port}: {e}")
            proxy.is_working = False
            return False
    
    def _get_proxy_dict(self, proxy: ProxyConfig) -> Dict[str, str]:
        """Convert ProxyConfig to requests proxy dictionary"""
        if proxy.username and proxy.password:
            auth = f"{proxy.username}:{proxy.password}@"
        else:
            auth = ""
        
        proxy_url = f"{proxy.proxy_type}://{auth}{proxy.host}:{proxy.port}"
        
        return {
            'http': proxy_url,
            'https': proxy_url
        }
    
    def validate_proxies(self, max_workers: int = 10) -> int:
        """Validate all loaded proxies"""
        if not self.proxies:
            return 0
        
        self.logger.info(f"Validating {len(self.proxies)} proxies...")
        
        working_count = 0
        self.working_proxies = []
        self.failed_proxies = []
        
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            # Submit all proxy tests
            future_to_proxy = {
                executor.submit(self.test_proxy, proxy): proxy 
                for proxy in self.proxies
            }
            
            # Collect results
            for future in as_completed(future_to_proxy):
                proxy = future_to_proxy[future]
                try:
                    is_working = future.result()
                    if is_working:
                        self.working_proxies.append(proxy)
                        working_count += 1
                    else:
                        self.failed_proxies.append(proxy)
                except Exception as e:
                    self.logger.error(f"Error testing proxy {proxy.host}:{proxy.port}: {e}")
                    self.failed_proxies.append(proxy)
        
        self.logger.info(f"Validation complete: {working_count}/{len(self.proxies)} proxies working")
        return working_count
    
    def rotate_proxy(self) -> bool:
        """Rotate to a new proxy"""
        if not self.working_proxies:
            self.logger.warning("No working proxies available for rotation")
            # Try to validate proxies again
            if self.validate_proxies() == 0:
                return False
        
        # Select a random working proxy
        available_proxies = [p for p in self.working_proxies if p != self.current_proxy]
        
        if not available_proxies:
            if len(self.working_proxies) == 1:
                # Only one proxy available, keep using it
                return True
            else:
                self.logger.warning("No alternative proxies available")
                return False
        
        new_proxy = random.choice(available_proxies)
        
        # Test the new proxy before switching
        if self.test_proxy(new_proxy):
            self.current_proxy = new_proxy
            self.rotation_count += 1
            self.logger.info(f"Rotated to proxy: {new_proxy.host}:{new_proxy.port}")
            return True
        else:
            # Remove failed proxy from working list
            if new_proxy in self.working_proxies:
                self.working_proxies.remove(new_proxy)
                self.failed_proxies.append(new_proxy)
            
            # Try again with another proxy
            return self.rotate_proxy()
    
    def get_current_proxy(self) -> Optional[ProxyConfig]:
        """Get current active proxy"""
        return self.current_proxy
    
    def get_proxy_dict(self) -> Optional[Dict[str, str]]:
        """Get current proxy as requests-compatible dictionary"""
        if self.current_proxy:
            return self._get_proxy_dict(self.current_proxy)
        return None
    
    def get_working_proxies(self) -> List[ProxyConfig]:
        """Get list of working proxies"""
        return self.working_proxies.copy()
    
    def get_failed_proxies(self) -> List[ProxyConfig]:
        """Get list of failed proxies"""
        return self.failed_proxies.copy()
    
    def get_statistics(self) -> Dict[str, Any]:
        """Get proxy statistics"""
        total_proxies = len(self.proxies)
        working_proxies = len(self.working_proxies)
        failed_proxies = len(self.failed_proxies)
        
        avg_response_time = 0
        if self.working_proxies:
            avg_response_time = sum(p.response_time for p in self.working_proxies) / len(self.working_proxies)
        
        return {
            'total_proxies': total_proxies,
            'working_proxies': working_proxies,
            'failed_proxies': failed_proxies,
            'success_rate': (working_proxies / total_proxies * 100) if total_proxies > 0 else 0,
            'rotation_count': self.rotation_count,
            'current_proxy': f"{self.current_proxy.host}:{self.current_proxy.port}" if self.current_proxy else None,
            'avg_response_time': avg_response_time
        }
    
    def add_proxy(self, host: str, port: int, proxy_type: str = 'http', 
                  username: Optional[str] = None, password: Optional[str] = None) -> bool:
        """Add a new proxy"""
        proxy = ProxyConfig(
            host=host,
            port=port,
            proxy_type=proxy_type,
            username=username,
            password=password
        )
        
        # Test the proxy before adding
        if self.test_proxy(proxy):
            self.proxies.append(proxy)
            self.working_proxies.append(proxy)
            self.logger.info(f"Added working proxy: {host}:{port}")
            return True
        else:
            self.logger.warning(f"Failed to add proxy: {host}:{port} (not working)")
            return False
    
    def remove_proxy(self, host: str, port: int) -> bool:
        """Remove a proxy"""
        for proxy_list in [self.proxies, self.working_proxies, self.failed_proxies]:
            for proxy in proxy_list[:]:  # Create a copy to avoid modification during iteration
                if proxy.host == host and proxy.port == port:
                    proxy_list.remove(proxy)
        
        if self.current_proxy and self.current_proxy.host == host and self.current_proxy.port == port:
            self.current_proxy = None
        
        self.logger.info(f"Removed proxy: {host}:{port}")
        return True
    
    def refresh_proxy_list(self):
        """Refresh the proxy list by reloading from sources"""
        self.logger.info("Refreshing proxy list...")
        
        # Clear current lists
        self.proxies = []
        self.working_proxies = []
        self.failed_proxies = []
        self.current_proxy = None
        
        # Reload from sources
        self._load_proxy_sources()
        
        # Validate new proxies
        self.validate_proxies()
    
    def export_working_proxies(self, filename: str) -> bool:
        """Export working proxies to a file"""
        try:
            with open(filename, 'w') as f:
                f.write("# Working Proxies Export\n")
                f.write(f"# Generated: {time.strftime('%Y-%m-%d %H:%M:%S')}\n")
                f.write(f"# Total working proxies: {len(self.working_proxies)}\n\n")
                
                for proxy in self.working_proxies:
                    if proxy.username and proxy.password:
                        line = f"{proxy.proxy_type}://{proxy.username}:{proxy.password}@{proxy.host}:{proxy.port}"
                    else:
                        line = f"{proxy.proxy_type}://{proxy.host}:{proxy.port}"
                    
                    f.write(f"{line} # Response time: {proxy.response_time:.2f}s\n")
            
            self.logger.info(f"Exported {len(self.working_proxies)} working proxies to {filename}")
            return True
            
        except Exception as e:
            self.logger.error(f"Error exporting proxies: {e}")
            return False
    
    def cleanup(self):
        """Cleanup proxy manager"""
        self.current_proxy = None
        self.logger.info("Proxy manager cleaned up")

    def test_all_proxies(self) -> List[ProxyConfig]:
        """Test all proxies and return working ones (wrapper for validate_proxies)"""
        try:
            self.validate_proxies()
            working_proxies = self.get_working_proxies()
            self.logger.info(f"Tested proxies: {len(working_proxies)} working out of {len(self.proxy_list)}")
            return working_proxies
        except Exception as e:
            self.logger.error(f"Error testing proxies: {e}")
            return []
