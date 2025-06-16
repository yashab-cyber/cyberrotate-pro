#!/usr/bin/env python3
"""
Security Utils - Security and anonymity utilities
Created by Yashab Alam - Founder & CEO of ZehraSec
"""

import hashlib
import random
import string
import time
import logging
import requests
import json
from typing import Dict, List, Optional, Any
from urllib.parse import urlparse
import os

class SecurityUtils:
    """
    Security and Anonymity Utilities
    
    Provides various security utilities including:
    - User agent randomization
    - IP reputation checking
    - Connection fingerprinting
    - Security headers management
    """
    
    def __init__(self, logger: logging.Logger):
        """Initialize security utilities"""
        self.logger = logger
        self.user_agents = self._load_user_agents()
        self.current_user_agent = None
        
        # Security configuration
        self.ip_reputation_apis = [
            'https://api.abuseipdb.com/api/v2/check',
            'https://ipinfo.io/{ip}/json',
            'https://api.virustotal.com/vtapi/v2/ip-address/report'
        ]
        
        self.logger.info("Security Utils initialized")
    
    def _load_user_agents(self) -> List[str]:
        """Load user agent strings"""
        user_agents = [
            # Chrome on Windows
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36',
            
            # Chrome on macOS
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36',
            
            # Firefox on Windows
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/121.0',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/120.0',
            
            # Firefox on macOS
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:109.0) Gecko/20100101 Firefox/121.0',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:109.0) Gecko/20100101 Firefox/120.0',
            
            # Safari on macOS
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.2 Safari/605.1.15',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.1 Safari/605.1.15',
            
            # Edge on Windows
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36 Edg/120.0.0.0',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36 Edg/119.0.0.0',
            
            # Chrome on Linux
            'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36',
            
            # Firefox on Linux
            'Mozilla/5.0 (X11; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/121.0',
            'Mozilla/5.0 (X11; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/120.0',
        ]
        
        return user_agents
    
    def get_random_user_agent(self) -> str:
        """Get a random user agent string"""
        self.current_user_agent = random.choice(self.user_agents)
        return self.current_user_agent
    
    def get_current_user_agent(self) -> Optional[str]:
        """Get current user agent"""
        return self.current_user_agent
    
    def generate_random_headers(self) -> Dict[str, str]:
        """Generate random HTTP headers"""
        headers = {
            'User-Agent': self.get_random_user_agent(),
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': random.choice([
                'en-US,en;q=0.9',
                'en-GB,en;q=0.9',
                'en-US,en;q=0.8',
                'en-US,en;q=0.5',
                'en-GB,en-US;q=0.9,en;q=0.8'
            ]),
            'Accept-Encoding': 'gzip, deflate, br',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
            'DNT': str(random.choice([0, 1])),
            'Sec-Fetch-Dest': 'document',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'none',
            'Cache-Control': random.choice(['no-cache', 'max-age=0', 'no-store'])
        }
        
        # Randomly add some optional headers
        if random.random() < 0.3:
            headers['Sec-GPC'] = '1'
        
        if random.random() < 0.5:
            headers['Pragma'] = 'no-cache'
        
        return headers
    
    def check_ip_reputation(self, ip_address: str) -> Dict[str, Any]:
        """Check IP address reputation"""
        reputation_info = {
            'ip': ip_address,
            'is_malicious': False,
            'reputation_score': 0,
            'sources': [],
            'details': {}
        }
        
        try:
            # Check with ipinfo.io (free tier)
            response = requests.get(
                f'https://ipinfo.io/{ip_address}/json',
                timeout=10
            )
            
            if response.status_code == 200:
                data = response.json()
                reputation_info['sources'].append('ipinfo.io')
                reputation_info['details']['ipinfo'] = {
                    'country': data.get('country'),
                    'region': data.get('region'),
                    'city': data.get('city'),
                    'org': data.get('org'),
                    'hostname': data.get('hostname')
                }
                
                # Simple reputation scoring based on org
                org = data.get('org', '').lower()
                if any(keyword in org for keyword in ['vpn', 'proxy', 'hosting', 'cloud']):
                    reputation_info['reputation_score'] += 1
                
        except Exception as e:
            self.logger.debug(f"Error checking IP reputation with ipinfo.io: {e}")
        
        # Additional reputation checks could be added here
        # (AbuseIPDB, VirusTotal, etc. - require API keys)
        
        return reputation_info
    
    def generate_connection_fingerprint(self, request_data: Dict[str, Any]) -> str:
        """Generate a connection fingerprint"""
        # Create a unique fingerprint based on connection characteristics
        fingerprint_data = {
            'user_agent': request_data.get('user_agent', ''),
            'headers': sorted(request_data.get('headers', {}).items()),
            'timestamp': int(time.time() / 60),  # Minute-level precision
            'method': request_data.get('method', 'GET'),
            'url_path': urlparse(request_data.get('url', '')).path
        }
        
        # Create hash of fingerprint data
        fingerprint_str = json.dumps(fingerprint_data, sort_keys=True)
        fingerprint_hash = hashlib.sha256(fingerprint_str.encode()).hexdigest()[:16]
        
        return fingerprint_hash
    
    def obfuscate_request_timing(self, min_delay: float = 0.5, max_delay: float = 3.0):
        """Add random delay to obfuscate request timing"""
        delay = random.uniform(min_delay, max_delay)
        time.sleep(delay)
        return delay
    
    def generate_random_session_id(self, length: int = 32) -> str:
        """Generate a random session ID"""
        characters = string.ascii_letters + string.digits
        return ''.join(random.choice(characters) for _ in range(length))
    
    def mask_ip_in_logs(self, ip_address: str) -> str:
        """Mask IP address in logs for privacy"""
        if not ip_address:
            return 'Unknown'
        
        parts = ip_address.split('.')
        if len(parts) == 4:
            # IPv4 - mask last octet
            return f"{parts[0]}.{parts[1]}.{parts[2]}.xxx"
        else:
            # IPv6 or other format - mask last part
            return ip_address[:len(ip_address)//2] + 'x' * (len(ip_address)//2)
    
    def validate_proxy_anonymity(self, proxy_info: Dict[str, Any]) -> Dict[str, Any]:
        """Validate proxy anonymity level"""
        anonymity_check = {
            'anonymity_level': 'unknown',
            'real_ip_leaked': False,
            'proxy_headers_detected': False,
            'details': {}
        }
        
        try:
            # Check for common proxy headers
            proxy_headers = [
                'HTTP_X_FORWARDED_FOR',
                'HTTP_X_REAL_IP',
                'HTTP_X_PROXY_ID',
                'HTTP_VIA',
                'HTTP_FORWARDED',
                'HTTP_CLIENT_IP'
            ]
            
            headers = proxy_info.get('headers', {})
            detected_headers = []
            
            for header in proxy_headers:
                if header.lower().replace('http_', '').replace('_', '-') in headers:
                    detected_headers.append(header)
            
            if detected_headers:
                anonymity_check['proxy_headers_detected'] = True
                anonymity_check['details']['detected_headers'] = detected_headers
                anonymity_check['anonymity_level'] = 'transparent'
            else:
                anonymity_check['anonymity_level'] = 'anonymous'
            
        except Exception as e:
            self.logger.error(f"Error validating proxy anonymity: {e}")
        
        return anonymity_check
    
    def encrypt_sensitive_data(self, data: str, key: Optional[str] = None) -> str:
        """Simple encryption for sensitive data"""
        if not key:
            key = self.generate_random_session_id(16)
        
        # Simple XOR encryption (for demonstration - use proper encryption in production)
        encrypted = []
        for i, char in enumerate(data):
            encrypted.append(chr(ord(char) ^ ord(key[i % len(key)])))
        
        return ''.join(encrypted)
    
    def decrypt_sensitive_data(self, encrypted_data: str, key: str) -> str:
        """Simple decryption for sensitive data"""
        # XOR decryption (same as encryption)
        return self.encrypt_sensitive_data(encrypted_data, key)
    
    def generate_csrf_token(self) -> str:
        """Generate CSRF token"""
        random_data = f"{time.time()}{random.random()}{os.getpid()}"
        return hashlib.sha256(random_data.encode()).hexdigest()[:32]
    
    def validate_url_safety(self, url: str) -> Dict[str, Any]:
        """Validate URL safety"""
        safety_check = {
            'is_safe': True,
            'warnings': [],
            'url': url
        }
        
        try:
            parsed = urlparse(url)
            
            # Check for suspicious TLDs
            suspicious_tlds = ['.tk', '.ml', '.ga', '.cf', '.top', '.xyz']
            if any(parsed.netloc.endswith(tld) for tld in suspicious_tlds):
                safety_check['warnings'].append('Suspicious TLD detected')
            
            # Check for IP addresses instead of domains
            if parsed.netloc.replace('.', '').isdigit():
                safety_check['warnings'].append('IP address used instead of domain')
            
            # Check for non-standard ports
            if parsed.port and parsed.port not in [80, 443, 8080, 8443]:
                safety_check['warnings'].append(f'Non-standard port: {parsed.port}')
            
            # Check for suspicious keywords
            suspicious_keywords = ['admin', 'login', 'password', 'secure', 'bank']
            if any(keyword in url.lower() for keyword in suspicious_keywords):
                safety_check['warnings'].append('Suspicious keywords in URL')
            
            if safety_check['warnings']:
                safety_check['is_safe'] = False
            
        except Exception as e:
            safety_check['is_safe'] = False
            safety_check['warnings'].append(f'URL parsing error: {str(e)}')
        
        return safety_check
    
    def get_security_headers(self) -> Dict[str, str]:
        """Get security-focused HTTP headers"""
        return {
            'X-Content-Type-Options': 'nosniff',
            'X-Frame-Options': 'DENY',
            'X-XSS-Protection': '1; mode=block',
            'Strict-Transport-Security': 'max-age=31536000; includeSubDomains',
            'Content-Security-Policy': "default-src 'self'",
            'Referrer-Policy': 'no-referrer',
            'Permissions-Policy': 'geolocation=(), camera=(), microphone=()'
        }
    
    def generate_noise_data(self, size: int = 1024) -> bytes:
        """Generate random noise data for obfuscation"""
        return os.urandom(size)
    
    def get_system_entropy(self) -> float:
        """Get system entropy for randomness quality"""
        try:
            # Simple entropy estimation
            random_data = os.urandom(1024)
            unique_bytes = len(set(random_data))
            entropy = unique_bytes / 256.0  # Normalized entropy
            return entropy
        except Exception:
            return 0.5  # Default entropy value
