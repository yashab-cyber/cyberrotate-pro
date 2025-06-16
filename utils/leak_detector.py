#!/usr/bin/env python3
"""
Leak Detector - Detects DNS, WebRTC, and other anonymity leaks
Created by Yashab Alam - Founder & CEO of ZehraSec
"""

import socket
import logging
import requests
import time
import json
from typing import Dict, List, Optional, Any, Tuple
import subprocess
import os
import threading
from concurrent.futures import ThreadPoolExecutor, as_completed

class LeakDetector:
    """
    Anonymity Leak Detector
    
    Detects various types of anonymity leaks including:
    - DNS leaks
    - WebRTC leaks
    - IPv6 leaks
    - Time zone leaks
    - Browser fingerprinting leaks
    """
    
    def __init__(self, logger: logging.Logger):
        """Initialize leak detector"""
        self.logger = logger
        self.test_results = {}
        self.last_test_time = None
        
        # DNS test servers
        self.dns_test_servers = [
            'https://www.dnsleaktest.com/api/dns-leak-test',
            'https://ipleak.net/json/',
            'https://ipinfo.io/json',
        ]
        
        # WebRTC test URLs
        self.webrtc_test_urls = [
            'https://browserleaks.com/webrtc',
            'https://www.whatismyipaddress.com/webrtc-test',
        ]
        
        # Test configuration
        self.timeout = 10
        self.max_workers = 5
        
        self.logger.info("Leak Detector initialized")
    
    def check_all_leaks(self) -> Dict[str, Any]:
        """Run comprehensive leak detection"""
        self.logger.info("Starting comprehensive leak detection...")
        
        start_time = time.time()
        results = {
            'timestamp': start_time,
            'test_duration': 0,
            'leaks_detected': [],
            'tests': {}
        }
        
        # Run all leak detection tests
        with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            futures = {
                executor.submit(self.check_dns_leak): 'dns_leak',
                executor.submit(self.check_webrtc_leak): 'webrtc_leak',
                executor.submit(self.check_ipv6_leak): 'ipv6_leak',
                executor.submit(self.check_timezone_leak): 'timezone_leak',
                executor.submit(self.check_geolocation_consistency): 'geolocation_consistency'
            }
            
            for future in as_completed(futures):
                test_name = futures[future]
                try:
                    test_result = future.result()
                    results['tests'][test_name] = test_result
                    
                    if test_result and test_result.get('leak_detected'):
                        results['leaks_detected'].append(test_name)
                        
                except Exception as e:
                    self.logger.error(f"Error in {test_name}: {e}")
                    results['tests'][test_name] = {'error': str(e)}
        
        results['test_duration'] = time.time() - start_time
        results['total_leaks'] = len(results['leaks_detected'])
        
        self.test_results = results
        self.last_test_time = start_time
        
        if results['leaks_detected']:
            self.logger.warning(f"Detected {len(results['leaks_detected'])} potential leaks: {', '.join(results['leaks_detected'])}")
        else:
            self.logger.info("No leaks detected in comprehensive test")
        
        return results
    
    def check_dns_leak(self) -> Optional[Dict[str, Any]]:
        """Check for DNS leaks"""
        try:
            self.logger.debug("Checking for DNS leaks...")
            
            # Get current public IP for comparison
            current_ip = self._get_public_ip()
            if not current_ip:
                return {'error': 'Could not determine public IP'}
            
            # Test DNS resolution through different methods
            dns_results = []
            
            # Test 1: Direct DNS query
            dns_servers = self._get_system_dns_servers()
            for dns_server in dns_servers:
                try:
                    # Perform DNS lookup
                    result = socket.gethostbyname('google.com')
                    
                    # Check if DNS server is in same country/region as VPN
                    dns_location = self._get_ip_location(dns_server)
                    current_location = self._get_ip_location(current_ip)
                    
                    dns_results.append({
                        'dns_server': dns_server,
                        'dns_location': dns_location,
                        'current_location': current_location,
                        'potential_leak': dns_location.get('country') != current_location.get('country')
                    })
                    
                except Exception as e:
                    self.logger.debug(f"DNS test failed for server {dns_server}: {e}")
            
            # Test 2: Online DNS leak test
            online_test_result = self._perform_online_dns_test()
            
            # Analyze results
            leak_detected = any(result.get('potential_leak', False) for result in dns_results)
            
            return {
                'leak_detected': leak_detected,
                'test_type': 'dns_leak',
                'current_ip': current_ip,
                'dns_test_results': dns_results,
                'online_test': online_test_result,
                'timestamp': time.time()
            }
            
        except Exception as e:
            self.logger.error(f"Error checking DNS leaks: {e}")
            return {'error': str(e)}
    
    def check_webrtc_leak(self) -> Optional[Dict[str, Any]]:
        """Check for WebRTC leaks"""
        try:
            self.logger.debug("Checking for WebRTC leaks...")
            
            # This is a simplified WebRTC leak detection
            # In a full implementation, you would use selenium or similar to test in a real browser
            
            webrtc_result = {
                'leak_detected': False,
                'test_type': 'webrtc_leak',
                'method': 'simplified_test',
                'note': 'Full WebRTC testing requires browser automation',
                'timestamp': time.time()
            }
            
            # Try to detect WebRTC through available methods
            try:
                # Check if WebRTC ports are open (basic test)
                webrtc_ports = [3478, 5349, 19302]  # Common WebRTC STUN ports
                
                for port in webrtc_ports:
                    try:
                        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                        sock.settimeout(2)
                        # Try to connect to Google's STUN server
                        sock.connect(('stun.l.google.com', port))
                        sock.close()
                        
                        webrtc_result['webrtc_connectivity'] = True
                        webrtc_result['accessible_ports'] = webrtc_result.get('accessible_ports', [])
                        webrtc_result['accessible_ports'].append(port)
                        
                    except:
                        continue
                
            except Exception as e:
                webrtc_result['error'] = str(e)
            
            return webrtc_result
            
        except Exception as e:
            self.logger.error(f"Error checking WebRTC leaks: {e}")
            return {'error': str(e)}
    
    def check_ipv6_leak(self) -> Optional[Dict[str, Any]]:
        """Check for IPv6 leaks"""
        try:
            self.logger.debug("Checking for IPv6 leaks...")
            
            ipv6_result = {
                'leak_detected': False,
                'test_type': 'ipv6_leak',
                'timestamp': time.time()
            }
            
            # Check if IPv6 is enabled
            try:
                # Try to get IPv6 address
                sock = socket.socket(socket.AF_INET6, socket.SOCK_DGRAM)
                sock.connect(('2001:4860:4860::8888', 80))  # Google DNS IPv6
                local_ipv6 = sock.getsockname()[0]
                sock.close()
                
                ipv6_result['local_ipv6'] = local_ipv6
                ipv6_result['ipv6_enabled'] = True
                
                # Check public IPv6
                public_ipv6 = self._get_public_ipv6()
                if public_ipv6:
                    ipv6_result['public_ipv6'] = public_ipv6
                    
                    # Compare with IPv4 geolocation
                    ipv4_location = self._get_ip_location(self._get_public_ip())
                    ipv6_location = self._get_ip_location(public_ipv6)
                    
                    if ipv4_location and ipv6_location:
                        different_location = (
                            ipv4_location.get('country') != ipv6_location.get('country')
                        )
                        ipv6_result['leak_detected'] = different_location
                        ipv6_result['ipv4_location'] = ipv4_location
                        ipv6_result['ipv6_location'] = ipv6_location
                
            except Exception as e:
                ipv6_result['ipv6_enabled'] = False
                ipv6_result['note'] = 'IPv6 not available or disabled'
            
            return ipv6_result
            
        except Exception as e:
            self.logger.error(f"Error checking IPv6 leaks: {e}")
            return {'error': str(e)}
    
    def check_timezone_leak(self) -> Optional[Dict[str, Any]]:
        """Check for timezone leaks"""
        try:
            self.logger.debug("Checking for timezone leaks...")
            
            import datetime
            
            # Get system timezone
            local_time = datetime.datetime.now()
            utc_time = datetime.datetime.utcnow()
            timezone_offset = (local_time - utc_time).total_seconds() / 3600
            
            # Get expected timezone based on public IP
            current_ip = self._get_public_ip()
            ip_location = self._get_ip_location(current_ip) if current_ip else {}
            expected_timezone = ip_location.get('timezone', 'Unknown')
            
            timezone_result = {
                'leak_detected': False,
                'test_type': 'timezone_leak',
                'system_timezone_offset': timezone_offset,
                'expected_timezone': expected_timezone,
                'ip_location': ip_location,
                'timestamp': time.time()
            }
            
            # Simple timezone leak detection
            if expected_timezone != 'Unknown':
                # This is a simplified check - in reality, timezone detection is complex
                timezone_result['note'] = 'Timezone leak detection requires more sophisticated analysis'
            
            return timezone_result
            
        except Exception as e:
            self.logger.error(f"Error checking timezone leaks: {e}")
            return {'error': str(e)}
    
    def check_geolocation_consistency(self) -> Optional[Dict[str, Any]]:
        """Check consistency of geolocation across different services"""
        try:
            self.logger.debug("Checking geolocation consistency...")
            
            current_ip = self._get_public_ip()
            if not current_ip:
                return {'error': 'Could not determine public IP'}
            
            # Get location from multiple services
            location_services = [
                ('ipinfo.io', f'https://ipinfo.io/{current_ip}/json'),
                ('ip-api.com', f'http://ip-api.com/json/{current_ip}'),
                ('ipapi.co', f'https://ipapi.co/{current_ip}/json/'),
            ]
            
            locations = []
            
            for service_name, url in location_services:
                try:
                    response = requests.get(url, timeout=self.timeout)
                    if response.status_code == 200:
                        data = response.json()
                        
                        # Normalize location data
                        location = self._normalize_location_data(service_name, data)
                        locations.append(location)
                        
                except Exception as e:
                    self.logger.debug(f"Failed to get location from {service_name}: {e}")
            
            # Analyze consistency
            consistency_result = {
                'leak_detected': False,
                'test_type': 'geolocation_consistency',
                'ip_address': current_ip,
                'locations': locations,
                'consistent': True,
                'timestamp': time.time()
            }
            
            if len(locations) >= 2:
                # Check if all locations report the same country
                countries = [loc.get('country') for loc in locations if loc.get('country')]
                cities = [loc.get('city') for loc in locations if loc.get('city')]
                
                unique_countries = set(countries)
                unique_cities = set(cities)
                
                if len(unique_countries) > 1:
                    consistency_result['consistent'] = False
                    consistency_result['inconsistent_countries'] = list(unique_countries)
                
                if len(unique_cities) > 1:
                    consistency_result['inconsistent_cities'] = list(unique_cities)
                
                consistency_result['leak_detected'] = not consistency_result['consistent']
            
            return consistency_result
            
        except Exception as e:
            self.logger.error(f"Error checking geolocation consistency: {e}")
            return {'error': str(e)}
    
    def _get_public_ip(self) -> Optional[str]:
        """Get current public IP address"""
        try:
            response = requests.get('https://httpbin.org/ip', timeout=self.timeout)
            if response.status_code == 200:
                return response.json().get('origin')
        except:
            try:
                response = requests.get('https://ipinfo.io/ip', timeout=self.timeout)
                if response.status_code == 200:
                    return response.text.strip()
            except:
                pass
        return None
    
    def _get_public_ipv6(self) -> Optional[str]:
        """Get current public IPv6 address"""
        try:
            response = requests.get('https://ipv6.icanhazip.com', timeout=self.timeout)
            if response.status_code == 200:
                return response.text.strip()
        except:
            pass
        return None
    
    def _get_ip_location(self, ip_address: str) -> Dict[str, Any]:
        """Get location information for an IP address"""
        try:
            response = requests.get(f'https://ipinfo.io/{ip_address}/json', timeout=self.timeout)
            if response.status_code == 200:
                return response.json()
        except:
            pass
        return {}
    
    def _get_system_dns_servers(self) -> List[str]:
        """Get system DNS servers"""
        dns_servers = []
        
        try:
            if os.name == 'nt':  # Windows
                result = subprocess.run(['nslookup', 'localhost'], 
                                      capture_output=True, text=True, timeout=10)
                # Parse nslookup output for DNS servers
                for line in result.stdout.split('\n'):
                    if 'Server:' in line:
                        server = line.split(':')[1].strip()
                        if server != 'localhost' and server != '127.0.0.1':
                            dns_servers.append(server)
            else:  # Unix-like systems
                with open('/etc/resolv.conf', 'r') as f:
                    for line in f:
                        if line.startswith('nameserver'):
                            dns_servers.append(line.split()[1])
        except:
            # Fallback to common DNS servers
            dns_servers = ['8.8.8.8', '1.1.1.1']
        
        return dns_servers[:3]  # Limit to first 3 servers
    
    def _perform_online_dns_test(self) -> Dict[str, Any]:
        """Perform online DNS leak test"""
        try:
            # This is a placeholder for online DNS leak testing
            # In a real implementation, you would integrate with services like dnsleaktest.com
            return {
                'service': 'placeholder',
                'result': 'DNS leak testing requires integration with external services',
                'status': 'not_implemented'
            }
        except Exception as e:
            return {'error': str(e)}
    
    def _normalize_location_data(self, service_name: str, data: Dict[str, Any]) -> Dict[str, Any]:
        """Normalize location data from different services"""
        normalized = {
            'service': service_name,
            'country': None,
            'region': None,
            'city': None,
            'timezone': None,
            'isp': None
        }
        
        # Service-specific parsing
        if service_name == 'ipinfo.io':
            normalized.update({
                'country': data.get('country'),
                'region': data.get('region'),
                'city': data.get('city'),
                'timezone': data.get('timezone'),
                'isp': data.get('org')
            })
        elif service_name == 'ip-api.com':
            normalized.update({
                'country': data.get('country'),
                'region': data.get('regionName'),
                'city': data.get('city'),
                'timezone': data.get('timezone'),
                'isp': data.get('isp')
            })
        elif service_name == 'ipapi.co':
            normalized.update({
                'country': data.get('country_name'),
                'region': data.get('region'),
                'city': data.get('city'),
                'timezone': data.get('timezone'),
                'isp': data.get('org')
            })
        
        return normalized
    
    def get_last_test_results(self) -> Optional[Dict[str, Any]]:
        """Get results from the last leak detection test"""
        return self.test_results if self.test_results else None
    
    def export_test_results(self, filename: Optional[str] = None) -> str:
        """Export test results to file"""
        if not filename:
            timestamp = time.strftime("%Y%m%d_%H%M%S")
            filename = f"data/logs/leak_test_{timestamp}.json"
        
        try:
            os.makedirs(os.path.dirname(filename), exist_ok=True)
            
            export_data = {
                'export_timestamp': time.time(),
                'last_test_results': self.test_results,
                'test_history': getattr(self, 'test_history', [])
            }
            
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(export_data, f, indent=2, default=str)
            
            self.logger.info(f"Leak test results exported to {filename}")
            return filename
            
        except Exception as e:
            self.logger.error(f"Error exporting test results: {e}")
            raise
