#!/usr/bin/env python3
"""
Network Monitor - Monitors network interfaces and connections
Created by Yashab Alam - Founder & CEO of ZehraSec
"""

import time
import logging
import psutil
import netifaces
import socket
from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass
import threading
from collections import defaultdict

@dataclass
class NetworkInterface:
    """Network interface information"""
    name: str
    ip_address: str
    netmask: str
    broadcast: str
    mac_address: str
    is_up: bool
    is_loopback: bool
    bytes_sent: int = 0
    bytes_recv: int = 0
    packets_sent: int = 0
    packets_recv: int = 0

@dataclass
class ConnectionInfo:
    """Network connection information"""
    local_address: str
    local_port: int
    remote_address: str
    remote_port: int
    status: str
    pid: int
    process_name: str

class NetworkMonitor:
    """
    Network Interface Monitor
    
    Monitors network interfaces and connections including:
    - Interface status and statistics
    - Connection tracking
    - Bandwidth monitoring
    - Route table monitoring
    """
    
    def __init__(self, logger: logging.Logger):
        """Initialize network monitor"""
        self.logger = logger
        self.interfaces = {}
        self.connections = []
        self.monitoring = False
        self.monitor_thread = None
        
        # Statistics
        self.stats_history = defaultdict(list)
        self.last_stats_time = time.time()
        
        # Configuration
        self.monitor_interval = 5.0  # seconds
        self.max_history_entries = 100
        
        self.logger.info("Network Monitor initialized")
    
    def get_network_interfaces(self) -> Dict[str, NetworkInterface]:
        """Get all network interfaces"""
        interfaces = {}
        
        try:
            # Get interface names
            interface_names = netifaces.interfaces()
            
            for name in interface_names:
                try:
                    # Get interface addresses
                    addrs = netifaces.ifaddresses(name)
                    
                    # IPv4 information
                    ipv4_info = addrs.get(netifaces.AF_INET, [{}])[0]
                    ip_address = ipv4_info.get('addr', '')
                    netmask = ipv4_info.get('netmask', '')
                    broadcast = ipv4_info.get('broadcast', '')
                    
                    # MAC address
                    mac_info = addrs.get(netifaces.AF_LINK, [{}])[0]
                    mac_address = mac_info.get('addr', '')
                    
                    # Interface status
                    is_up = self._is_interface_up(name)
                    is_loopback = name.startswith('lo') or name == 'Loopback'
                    
                    # Network statistics
                    stats = self._get_interface_stats(name)
                    
                    interface = NetworkInterface(
                        name=name,
                        ip_address=ip_address,
                        netmask=netmask,
                        broadcast=broadcast,
                        mac_address=mac_address,
                        is_up=is_up,
                        is_loopback=is_loopback,
                        bytes_sent=stats.get('bytes_sent', 0),
                        bytes_recv=stats.get('bytes_recv', 0),
                        packets_sent=stats.get('packets_sent', 0),
                        packets_recv=stats.get('packets_recv', 0)
                    )
                    
                    interfaces[name] = interface
                    
                except Exception as e:
                    self.logger.debug(f"Error getting info for interface {name}: {e}")
                    continue
            
            self.interfaces = interfaces
            return interfaces
            
        except Exception as e:
            self.logger.error(f"Error getting network interfaces: {e}")
            return {}
    
    def _is_interface_up(self, interface_name: str) -> bool:
        """Check if network interface is up"""
        try:
            # Try to get interface statistics
            stats = psutil.net_io_counters(pernic=True)
            return interface_name in stats
        except Exception:
            return False
    
    def _get_interface_stats(self, interface_name: str) -> Dict[str, int]:
        """Get interface statistics"""
        try:
            stats = psutil.net_io_counters(pernic=True)
            if interface_name in stats:
                stat = stats[interface_name]
                return {
                    'bytes_sent': stat.bytes_sent,
                    'bytes_recv': stat.bytes_recv,
                    'packets_sent': stat.packets_sent,
                    'packets_recv': stat.packets_recv,
                    'errin': stat.errin,
                    'errout': stat.errout,
                    'dropin': stat.dropin,
                    'dropout': stat.dropout
                }
        except Exception as e:
            self.logger.debug(f"Error getting stats for interface {interface_name}: {e}")
        
        return {}
    
    def get_active_connections(self) -> List[ConnectionInfo]:
        """Get active network connections"""
        connections = []
        
        try:
            # Get all connections
            conns = psutil.net_connections(kind='inet')
            
            for conn in conns:
                try:
                    # Get process information
                    process_name = 'Unknown'
                    if conn.pid:
                        try:
                            process = psutil.Process(conn.pid)
                            process_name = process.name()
                        except (psutil.NoSuchProcess, psutil.AccessDenied):
                            pass
                    
                    # Parse addresses
                    local_addr = conn.laddr.ip if conn.laddr else ''
                    local_port = conn.laddr.port if conn.laddr else 0
                    remote_addr = conn.raddr.ip if conn.raddr else ''
                    remote_port = conn.raddr.port if conn.raddr else 0
                    
                    connection = ConnectionInfo(
                        local_address=local_addr,
                        local_port=local_port,
                        remote_address=remote_addr,
                        remote_port=remote_port,
                        status=conn.status,
                        pid=conn.pid or 0,
                        process_name=process_name
                    )
                    
                    connections.append(connection)
                    
                except Exception as e:
                    self.logger.debug(f"Error processing connection: {e}")
                    continue
            
            self.connections = connections
            return connections
            
        except Exception as e:
            self.logger.error(f"Error getting active connections: {e}")
            return []
    
    def get_default_gateway(self) -> Optional[str]:
        """Get default gateway IP"""
        try:
            gateways = netifaces.gateways()
            default_gateway = gateways.get('default', {})
            
            if netifaces.AF_INET in default_gateway:
                return default_gateway[netifaces.AF_INET][0]
            
        except Exception as e:
            self.logger.error(f"Error getting default gateway: {e}")
        
        return None
    
    def get_dns_servers(self) -> List[str]:
        """Get configured DNS servers"""
        dns_servers = []
        
        try:
            # Try to read from /etc/resolv.conf on Unix systems
            if hasattr(socket, 'AF_UNIX'):
                try:
                    with open('/etc/resolv.conf', 'r') as f:
                        for line in f:
                            if line.startswith('nameserver'):
                                dns_servers.append(line.split()[1])
                except:
                    pass
            
            # Fallback: use common DNS servers
            if not dns_servers:
                dns_servers = ['8.8.8.8', '1.1.1.1', '9.9.9.9']
            
        except Exception as e:
            self.logger.error(f"Error getting DNS servers: {e}")
        
        return dns_servers
    
    def check_internet_connectivity(self) -> bool:
        """Check if internet connectivity is available"""
        try:
            # Try to connect to Google's DNS
            socket.create_connection(('8.8.8.8', 53), timeout=5)
            return True
        except:
            try:
                # Try Cloudflare DNS as backup
                socket.create_connection(('1.1.1.1', 53), timeout=5)
                return True
            except:
                return False
    
    def get_public_ip(self) -> Optional[str]:
        """Get public IP address"""
        try:
            import requests
            response = requests.get('https://httpbin.org/ip', timeout=10)
            if response.status_code == 200:
                return response.json().get('origin')
        except Exception as e:
            self.logger.debug(f"Error getting public IP: {e}")
        
        return None
    
    def get_local_ip(self) -> Optional[str]:
        """Get local IP address"""
        try:
            # Connect to a remote address to determine local IP
            with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
                s.connect(('8.8.8.8', 80))
                return s.getsockname()[0]
        except Exception as e:
            self.logger.debug(f"Error getting local IP: {e}")
        
        return None
    
    def monitor_bandwidth(self, interface_name: str = None) -> Dict[str, float]:
        """Monitor bandwidth usage"""
        try:
            current_time = time.time()
            current_stats = psutil.net_io_counters(pernic=True)
            
            bandwidth_info = {}
            
            if interface_name:
                # Monitor specific interface
                if interface_name in current_stats:
                    stats = current_stats[interface_name]
                    
                    # Calculate bandwidth if we have previous data
                    if interface_name in self.stats_history:
                        prev_stats = self.stats_history[interface_name][-1]
                        time_diff = current_time - prev_stats['timestamp']
                        
                        if time_diff > 0:
                            bytes_sent_diff = stats.bytes_sent - prev_stats['bytes_sent']
                            bytes_recv_diff = stats.bytes_recv - prev_stats['bytes_recv']
                            
                            bandwidth_info = {
                                'upload_speed': bytes_sent_diff / time_diff,  # bytes per second
                                'download_speed': bytes_recv_diff / time_diff,
                                'upload_speed_mbps': (bytes_sent_diff / time_diff) * 8 / 1000000,  # Mbps
                                'download_speed_mbps': (bytes_recv_diff / time_diff) * 8 / 1000000,
                            }
                    
                    # Store current stats
                    self.stats_history[interface_name].append({
                        'timestamp': current_time,
                        'bytes_sent': stats.bytes_sent,
                        'bytes_recv': stats.bytes_recv
                    })
                    
                    # Limit history size
                    if len(self.stats_history[interface_name]) > self.max_history_entries:
                        self.stats_history[interface_name].pop(0)
            
            return bandwidth_info
            
        except Exception as e:
            self.logger.error(f"Error monitoring bandwidth: {e}")
            return {}
    
    def start_monitoring(self):
        """Start continuous network monitoring"""
        if self.monitoring:
            return
        
        self.monitoring = True
        self.monitor_thread = threading.Thread(target=self._monitoring_loop, daemon=True)
        self.monitor_thread.start()
        
        self.logger.info("Network monitoring started")
    
    def stop_monitoring(self):
        """Stop network monitoring"""
        self.monitoring = False
        if self.monitor_thread:
            self.monitor_thread.join(timeout=5)
        
        self.logger.info("Network monitoring stopped")
    
    def _monitoring_loop(self):
        """Main monitoring loop"""
        while self.monitoring:
            try:
                # Update interface information
                self.get_network_interfaces()
                
                # Update connection information
                self.get_active_connections()
                
                # Monitor bandwidth for all interfaces
                for interface_name in self.interfaces:
                    self.monitor_bandwidth(interface_name)
                
                time.sleep(self.monitor_interval)
                
            except Exception as e:
                self.logger.error(f"Error in monitoring loop: {e}")
                time.sleep(self.monitor_interval)
    
    def get_network_summary(self) -> Dict[str, Any]:
        """Get network summary information"""
        summary = {
            'interfaces': len(self.interfaces),
            'active_connections': len(self.connections),
            'internet_connectivity': self.check_internet_connectivity(),
            'public_ip': self.get_public_ip(),
            'local_ip': self.get_local_ip(),
            'default_gateway': self.get_default_gateway(),
            'dns_servers': self.get_dns_servers(),
            'vpn_detected': self._detect_vpn_interface()
        }
        
        return summary
    
    def _detect_vpn_interface(self) -> bool:
        """Detect if VPN interface is active"""
        vpn_interface_names = ['tun', 'tap', 'ppp', 'vpn']
        
        for interface_name in self.interfaces:
            if any(vpn_name in interface_name.lower() for vpn_name in vpn_interface_names):
                if self.interfaces[interface_name].is_up:
                    return True
        
        return False
    
    def get_connection_statistics(self) -> Dict[str, Any]:
        """Get connection statistics"""
        stats = {
            'total_connections': len(self.connections),
            'established_connections': 0,
            'listening_connections': 0,
            'time_wait_connections': 0,
            'unique_remote_ips': set(),
            'top_processes': defaultdict(int)
        }
        
        for conn in self.connections:
            if conn.status == 'ESTABLISHED':
                stats['established_connections'] += 1
            elif conn.status == 'LISTEN':
                stats['listening_connections'] += 1
            elif conn.status == 'TIME_WAIT':
                stats['time_wait_connections'] += 1
            
            if conn.remote_address:
                stats['unique_remote_ips'].add(conn.remote_address)
            
            if conn.process_name:
                stats['top_processes'][conn.process_name] += 1
        
        stats['unique_remote_ips'] = len(stats['unique_remote_ips'])
        stats['top_processes'] = dict(sorted(stats['top_processes'].items(), 
                                           key=lambda x: x[1], reverse=True)[:10])
        
        return stats
    
    def export_network_info(self, filename: str) -> bool:
        """Export network information to file"""
        try:
            import json
            
            network_data = {
                'timestamp': time.time(),
                'interfaces': {name: {
                    'ip_address': interface.ip_address,
                    'mac_address': interface.mac_address,
                    'is_up': interface.is_up,
                    'bytes_sent': interface.bytes_sent,
                    'bytes_recv': interface.bytes_recv
                } for name, interface in self.interfaces.items()},
                'connections': [{
                    'local_address': conn.local_address,
                    'local_port': conn.local_port,
                    'remote_address': conn.remote_address,
                    'remote_port': conn.remote_port,
                    'status': conn.status,
                    'process_name': conn.process_name
                } for conn in self.connections],
                'summary': self.get_network_summary(),
                'statistics': self.get_connection_statistics()
            }
            
            with open(filename, 'w') as f:
                json.dump(network_data, f, indent=2, default=str)
            
            self.logger.info(f"Network information exported to {filename}")
            return True
            
        except Exception as e:
            self.logger.error(f"Error exporting network info: {e}")
            return False
