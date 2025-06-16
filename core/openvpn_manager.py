#!/usr/bin/env python3
"""
OpenVPN Manager - Manages OpenVPN connections for IP rotation
Created by Yashab Alam - Founder & CEO of ZehraSec

This module handles OpenVPN connection management specifically for IP rotation.
"""

import os
import sys
import time
import subprocess
import json
import random
import logging
from typing import Dict, List, Optional, Any, Tuple
from pathlib import Path
import psutil
import netifaces
from dataclasses import dataclass

@dataclass
class OpenVPNConfig:
    """OpenVPN configuration details"""
    name: str
    config_file: str
    country: str
    city: str
    server: str
    port: int
    protocol: str
    auth_file: Optional[str] = None
    ca_file: Optional[str] = None
    cert_file: Optional[str] = None
    key_file: Optional[str] = None

class OpenVPNManager:
    """
    OpenVPN Connection Manager
    
    Manages OpenVPN connections for IP rotation including:
    - Connection establishment and termination
    - Server selection and rotation
    - Connection monitoring and health checks
    - Configuration management
    """
    
    def __init__(self, logger: logging.Logger):
        """Initialize OpenVPN manager"""
        self.logger = logger
        self.current_process = None
        self.current_config = None
        self.available_configs = []
        self.connection_start_time = None
        self.connection_attempts = 0
        self.max_connection_attempts = 3
        
        # OpenVPN paths (will be detected automatically)
        self.openvpn_binary = self._find_openvpn_binary()
        self.config_dir = self._get_config_directory()
        
        # Initialize available configurations
        self._load_available_configs()
        
        self.logger.info("OpenVPN Manager initialized")
    
    def _find_openvpn_binary(self) -> Optional[str]:
        """Find OpenVPN binary on the system"""
        possible_paths = [
            # Windows paths
            r"C:\Program Files\OpenVPN\bin\openvpn.exe",
            r"C:\Program Files (x86)\OpenVPN\bin\openvpn.exe",
            # Linux paths
            "/usr/sbin/openvpn",
            "/usr/bin/openvpn",
            "/sbin/openvpn",
            # macOS paths
            "/usr/local/sbin/openvpn",
            "/usr/local/bin/openvpn",
            "/opt/local/sbin/openvpn",
        ]
        
        # Check if openvpn is in PATH
        try:
            result = subprocess.run(['openvpn', '--version'], 
                                  capture_output=True, 
                                  text=True, 
                                  timeout=5)
            if result.returncode == 0:
                return 'openvpn'
        except:
            pass
        
        # Check specific paths
        for path in possible_paths:
            if os.path.exists(path):
                return path
        
        self.logger.warning("OpenVPN binary not found. Please install OpenVPN.")
        return None
    
    def _get_config_directory(self) -> str:
        """Get the OpenVPN configuration directory"""
        # Create config directory if it doesn't exist
        config_dir = os.path.join(os.path.dirname(__file__), '..', 'config', 'openvpn')
        os.makedirs(config_dir, exist_ok=True)
        return config_dir
    
    def _load_available_configs(self):
        """Load available OpenVPN configurations"""
        if not os.path.exists(self.config_dir):
            self.logger.warning(f"OpenVPN config directory not found: {self.config_dir}")
            return
        
        self.available_configs = []
        
        # Look for .ovpn files
        for file in os.listdir(self.config_dir):
            if file.endswith('.ovpn'):
                config_path = os.path.join(self.config_dir, file)
                config = self._parse_ovpn_file(config_path)
                if config:
                    self.available_configs.append(config)
        
        # Look for configuration JSON files
        config_json_path = os.path.join(self.config_dir, 'servers.json')
        if os.path.exists(config_json_path):
            try:
                with open(config_json_path, 'r') as f:
                    servers_data = json.load(f)
                    for server in servers_data.get('servers', []):
                        config = OpenVPNConfig(
                            name=server.get('name'),
                            config_file=server.get('config_file'),
                            country=server.get('country'),
                            city=server.get('city'),
                            server=server.get('server'),
                            port=server.get('port'),
                            protocol=server.get('protocol'),
                            auth_file=server.get('auth_file'),
                            ca_file=server.get('ca_file'),
                            cert_file=server.get('cert_file'),
                            key_file=server.get('key_file')
                        )
                        self.available_configs.append(config)
            except Exception as e:
                self.logger.error(f"Error loading servers.json: {e}")
        
        if not self.available_configs:
            self.logger.warning("No OpenVPN configurations found")
            self._create_sample_configs()
        else:
            self.logger.info(f"Loaded {len(self.available_configs)} OpenVPN configurations")
    
    def _parse_ovpn_file(self, config_path: str) -> Optional[OpenVPNConfig]:
        """Parse an .ovpn configuration file"""
        try:
            with open(config_path, 'r') as f:
                content = f.read()
            
            # Extract basic information
            name = os.path.basename(config_path).replace('.ovpn', '')
            
            # Parse remote line for server info
            server = None
            port = 1194
            protocol = 'udp'
            
            for line in content.split('\n'):
                line = line.strip()
                if line.startswith('remote '):
                    parts = line.split()
                    if len(parts) >= 2:
                        server = parts[1]
                    if len(parts) >= 3:
                        port = int(parts[2])
                    if len(parts) >= 4:
                        protocol = parts[3]
                elif line.startswith('proto '):
                    protocol = line.split()[1]
                elif line.startswith('port '):
                    port = int(line.split()[1])
            
            if not server:
                return None
            
            return OpenVPNConfig(
                name=name,
                config_file=config_path,
                country='Unknown',
                city='Unknown',
                server=server,
                port=port,
                protocol=protocol
            )
            
        except Exception as e:
            self.logger.error(f"Error parsing .ovpn file {config_path}: {e}")
            return None
    
    def _create_sample_configs(self):
        """Create sample OpenVPN configurations"""
        sample_servers = {
            "servers": [
                {
                    "name": "sample-us-east",
                    "config_file": "sample-us-east.ovpn",
                    "country": "United States",
                    "city": "New York",
                    "server": "us-east.example.com",
                    "port": 1194,
                    "protocol": "udp"
                },
                {
                    "name": "sample-eu-west",
                    "config_file": "sample-eu-west.ovpn",
                    "country": "United Kingdom",
                    "city": "London",
                    "server": "eu-west.example.com",
                    "port": 1194,
                    "protocol": "udp"
                }
            ]
        }
        
        try:
            config_file = os.path.join(self.config_dir, 'servers.json')
            with open(config_file, 'w') as f:
                json.dump(sample_servers, f, indent=2)
            
            # Create sample .ovpn files
            for server in sample_servers['servers']:
                ovpn_content = f"""client
dev tun
proto {server['protocol']}
remote {server['server']} {server['port']}
resolv-retry infinite
nobind
persist-key
persist-tun
ca ca.crt
cert client.crt
key client.key
remote-cert-tls server
cipher AES-256-CBC
verb 3
"""
                ovpn_path = os.path.join(self.config_dir, server['config_file'])
                with open(ovpn_path, 'w') as f:
                    f.write(ovpn_content)
            
            self.logger.info("Created sample OpenVPN configurations")
            
        except Exception as e:
            self.logger.error(f"Error creating sample configs: {e}")
    
    def is_connected(self) -> bool:
        """Check if OpenVPN is currently connected"""
        if not self.current_process:
            return False
        
        try:
            # Check if process is still running
            if self.current_process.poll() is not None:
                return False
            
            # Check for VPN interface
            return self._check_vpn_interface()
            
        except Exception as e:
            self.logger.error(f"Error checking connection status: {e}")
            return False
    
    def _check_vpn_interface(self) -> bool:
        """Check if VPN network interface exists"""
        try:
            interfaces = netifaces.interfaces()
            
            # Look for typical VPN interfaces
            vpn_interfaces = ['tun0', 'tun1', 'tap0', 'tap1', 'ppp0']
            for interface in vpn_interfaces:
                if interface in interfaces:
                    # Check if interface has an IP address
                    try:
                        addrs = netifaces.ifaddresses(interface)
                        if netifaces.AF_INET in addrs:
                            return True
                    except:
                        continue
            
            return False
            
        except Exception as e:
            self.logger.error(f"Error checking VPN interface: {e}")
            return False
    
    def connect(self, config: Optional[OpenVPNConfig] = None) -> bool:
        """
        Connect to OpenVPN server
        
        Args:
            config: Specific configuration to use, or None for random selection
            
        Returns:
            bool: True if connection successful
        """
        if not self.openvpn_binary:
            self.logger.error("OpenVPN binary not found")
            return False
        
        if not self.available_configs:
            self.logger.error("No OpenVPN configurations available")
            return False
        
        # Disconnect existing connection
        if self.is_connected():
            self.disconnect()
        
        # Select configuration
        if not config:
            config = random.choice(self.available_configs)
        
        self.current_config = config
        self.connection_attempts += 1
        
        try:
            # Build OpenVPN command
            cmd = [self.openvpn_binary, '--config', config.config_file]
            
            # Add authentication if specified
            if config.auth_file and os.path.exists(config.auth_file):
                cmd.extend(['--auth-user-pass', config.auth_file])
            
            # Add additional options for better compatibility
            cmd.extend([
                '--verb', '3',
                '--script-security', '2',
                '--up-delay',
                '--down-pre',
                '--pull-filter', 'ignore', 'redirect-gateway',
                '--route-method', 'exe',
                '--route-delay', '2'
            ])
            
            self.logger.info(f"Connecting to OpenVPN server: {config.name}")
            
            # Start OpenVPN process
            self.current_process = subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                creationflags=subprocess.CREATE_NEW_PROCESS_GROUP if sys.platform == 'win32' else 0
            )
            
            self.connection_start_time = time.time()
            
            # Wait for connection to establish
            return self._wait_for_connection()
            
        except Exception as e:
            self.logger.error(f"Error connecting to OpenVPN: {e}")
            return False
    
    def _wait_for_connection(self, timeout: int = 30) -> bool:
        """Wait for OpenVPN connection to establish"""
        start_time = time.time()
        
        while time.time() - start_time < timeout:
            if not self.current_process:
                return False
            
            # Check if process died
            if self.current_process.poll() is not None:
                stderr = self.current_process.stderr.read()
                self.logger.error(f"OpenVPN process terminated: {stderr}")
                return False
            
            # Check if VPN interface is up
            if self._check_vpn_interface():
                self.logger.info(f"OpenVPN connected successfully to {self.current_config.name}")
                return True
            
            time.sleep(1)
        
        self.logger.error("OpenVPN connection timeout")
        self.disconnect()
        return False
    
    def disconnect(self) -> bool:
        """Disconnect from OpenVPN"""
        if not self.current_process:
            return True
        
        try:
            self.logger.info("Disconnecting from OpenVPN")
            
            # Terminate the process
            if sys.platform == 'win32':
                self.current_process.terminate()
            else:
                self.current_process.send_signal(subprocess.signal.SIGTERM)
            
            # Wait for process to terminate
            try:
                self.current_process.wait(timeout=10)
            except subprocess.TimeoutExpired:
                self.logger.warning("OpenVPN process didn't terminate gracefully, killing it")
                self.current_process.kill()
                self.current_process.wait()
            
            self.current_process = None
            self.current_config = None
            self.connection_start_time = None
            
            return True
            
        except Exception as e:
            self.logger.error(f"Error disconnecting from OpenVPN: {e}")
            return False
    
    def rotate_connection(self) -> bool:
        """
        Rotate to a new OpenVPN server
        
        Returns:
            bool: True if rotation successful
        """
        if not self.available_configs:
            self.logger.error("No OpenVPN configurations available for rotation")
            return False
        
        # Get current config to avoid reconnecting to the same server
        current_config = self.current_config
        
        # Get available configs excluding current one
        available_configs = [
            config for config in self.available_configs 
            if config != current_config
        ]
        
        if not available_configs:
            self.logger.warning("No alternative OpenVPN servers available")
            return False
        
        # Select new configuration
        new_config = random.choice(available_configs)
        
        self.logger.info(f"Rotating from {current_config.name if current_config else 'None'} to {new_config.name}")
        
        # Connect to new server
        return self.connect(new_config)
    
    def get_current_connection_info(self) -> Optional[Dict[str, Any]]:
        """Get information about current connection"""
        if not self.is_connected() or not self.current_config:
            return None
        
        connection_time = 0
        if self.connection_start_time:
            connection_time = time.time() - self.connection_start_time
        
        return {
            'name': self.current_config.name,
            'server': self.current_config.server,
            'country': self.current_config.country,
            'city': self.current_config.city,
            'protocol': self.current_config.protocol,
            'port': self.current_config.port,
            'connected_time': connection_time,
            'connection_attempts': self.connection_attempts
        }
    
    def get_available_servers(self) -> List[Dict[str, Any]]:
        """Get list of available OpenVPN servers"""
        return [
            {
                'name': config.name,
                'server': config.server,
                'country': config.country,
                'city': config.city,
                'protocol': config.protocol,
                'port': config.port
            }
            for config in self.available_configs
        ]
    
    def test_connection(self, config: OpenVPNConfig) -> bool:
        """Test connection to a specific OpenVPN server"""
        try:
            # Simple connectivity test
            import socket
            
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(10)
            
            result = sock.connect_ex((config.server, config.port))
            sock.close()
            
            return result == 0
            
        except Exception as e:
            self.logger.error(f"Error testing connection to {config.server}: {e}")
            return False
    
    def cleanup(self):
        """Cleanup OpenVPN connections"""
        if self.is_connected():
            self.disconnect()
        
        self.logger.info("OpenVPN manager cleaned up")
    
    def get_connection_stats(self) -> Dict[str, Any]:
        """Get connection statistics"""
        stats = {
            'is_connected': self.is_connected(),
            'current_server': None,
            'connection_time': 0,
            'total_attempts': self.connection_attempts,
            'available_servers': len(self.available_configs)
        }
        
        if self.current_config:
            stats['current_server'] = self.current_config.name
        
        if self.connection_start_time:
            stats['connection_time'] = time.time() - self.connection_start_time
        
        return stats
