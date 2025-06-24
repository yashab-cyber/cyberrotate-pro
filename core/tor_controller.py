#!/usr/bin/env python3
"""
Tor Controller - Manages Tor network connections and circuit rotation
Created by Yashab Alam - Founder & CEO of ZehraSec
"""

import time
import logging
import socket
import requests
from typing import Dict, Optional, Any, List
import subprocess
import os
import sys

try:
    from stem import Signal
    from stem.control import Controller
    from stem.connection import connect
    import stem.process
    STEM_AVAILABLE = True
except ImportError:
    STEM_AVAILABLE = False

class TorController:
    """
    Tor Network Controller
    
    Manages Tor connections and circuit rotation including:
    - Tor service management
    - Circuit renewal and rotation
    - Connection monitoring
    - Configuration management
    """
    
    def __init__(self, logger: logging.Logger):
        """Initialize Tor controller"""
        self.logger = logger
        self.controller = None
        self.tor_process = None
        self.is_connected = False
        self.circuit_count = 0
        
        # Tor configuration
        self.tor_port = 9050
        self.control_port = 9051
        self.control_password = None
        
        # Connection statistics
        self.connection_attempts = 0
        self.successful_rotations = 0
        self.failed_rotations = 0
        
        if not STEM_AVAILABLE:
            self.logger.warning("Stem library not available. Tor functionality will be limited.")
        
        self.logger.info("Tor Controller initialized")
    
    def is_tor_running(self) -> bool:
        """Check if Tor service is running"""
        try:
            # Try to connect to Tor SOCKS port
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(3)
            result = sock.connect_ex(('127.0.0.1', self.tor_port))
            sock.close()
            return result == 0
        except Exception:
            return False
    
    def start_tor_service(self) -> bool:
        """Start Tor service if not running"""
        if self.is_tor_running():
            self.logger.info("Tor service is already running")
            return True
        
        try:
            # Try to start Tor using stem
            if STEM_AVAILABLE:
                return self._start_tor_with_stem()
            else:
                return self._start_tor_system()
                
        except Exception as e:
            self.logger.error(f"Failed to start Tor service: {e}")
            return False
    
    def _start_tor_with_stem(self) -> bool:
        """Start Tor using stem library"""
        try:
            self.logger.info("Starting Tor process with stem...")
            
            # Configuration for Tor
            tor_config = {
                'SocksPort': str(self.tor_port),
                'ControlPort': str(self.control_port),
                'DataDirectory': self._get_tor_data_directory(),
            }
            
            # Start Tor process
            self.tor_process = stem.process.launch_tor_with_config(
                config=tor_config,
                init_msg_handler=self._tor_init_handler
            )
            
            # Wait for Tor to be ready
            time.sleep(5)
            
            if self.is_tor_running():
                self.logger.info("Tor service started successfully")
                return True
            else:
                self.logger.error("Tor service failed to start")
                return False
                
        except Exception as e:
            self.logger.error(f"Error starting Tor with stem: {e}")
            return False
    
    def _start_tor_system(self) -> bool:
        """Start Tor using system command"""
        tor_commands = [
            'tor',
            '/usr/bin/tor',
            '/usr/sbin/tor',
            'C:\\Program Files\\Tor Browser\\Browser\\TorBrowser\\Tor\\tor.exe',
            'C:\\Program Files (x86)\\Tor Browser\\Browser\\TorBrowser\\Tor\\tor.exe'
        ]
        
        for tor_cmd in tor_commands:
            try:
                self.logger.info(f"Trying to start Tor with command: {tor_cmd}")
                
                # Create Tor configuration
                tor_config = f"""
SocksPort {self.tor_port}
ControlPort {self.control_port}
DataDirectory {self._get_tor_data_directory()}
"""
                
                # Write temporary config file
                config_path = os.path.join(self._get_tor_data_directory(), 'torrc')
                os.makedirs(os.path.dirname(config_path), exist_ok=True)
                
                with open(config_path, 'w') as f:
                    f.write(tor_config)
                
                # Start Tor process
                self.tor_process = subprocess.Popen(
                    [tor_cmd, '-f', config_path],
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    text=True
                )
                
                # Wait for Tor to start
                time.sleep(10)
                
                if self.is_tor_running():
                    self.logger.info("Tor service started successfully")
                    return True
                    
            except Exception as e:
                self.logger.debug(f"Failed to start Tor with {tor_cmd}: {e}")
                continue
        
        self.logger.error("Failed to start Tor service using system commands")
        return False
    
    def _get_tor_data_directory(self) -> str:
        """Get Tor data directory path"""
        if sys.platform == 'win32':
            data_dir = os.path.join(os.environ.get('APPDATA', ''), 'CyberRotate', 'tor')
        else:
            data_dir = os.path.expanduser('~/.cyberrotate/tor')
        
        os.makedirs(data_dir, exist_ok=True)
        return data_dir
    
    def _tor_init_handler(self, line: str):
        """Handle Tor initialization messages"""
        if "Bootstrapped 100%" in line:
            self.logger.info("Tor bootstrap completed")
        elif "Opening Socks listener" in line:
            self.logger.info("Tor SOCKS listener opened")
    
    def connect_to_controller(self) -> bool:
        """Connect to Tor controller"""
        if not STEM_AVAILABLE:
            self.logger.warning("Stem library not available for controller connection")
            return False
        
        try:
            self.connection_attempts += 1
            
            # Try to connect to controller
            self.controller = Controller.from_port(port=self.control_port)
            self.controller.authenticate()
            
            self.is_connected = True
            self.logger.info("Connected to Tor controller")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to connect to Tor controller: {e}")
            self.is_connected = False
            return False
    
    def new_circuit(self) -> bool:
        """Create a new Tor circuit (rotate IP)"""
        if not self.is_connected:
            if not self.connect_to_controller():
                return False
        
        try:
            # Send signal to create new circuit
            self.controller.signal(Signal.NEWNYM)
            self.circuit_count += 1
            self.successful_rotations += 1
            
            # Wait for new circuit to be established
            time.sleep(3)
            
            self.logger.info(f"Created new Tor circuit (#{self.circuit_count})")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to create new Tor circuit: {e}")
            self.failed_rotations += 1
            return False
    
    def get_current_ip(self) -> Optional[str]:
        """Get current IP through Tor"""
        try:
            # Configure requests to use Tor SOCKS proxy
            proxies = {
                'http': f'socks5://127.0.0.1:{self.tor_port}',
                'https': f'socks5://127.0.0.1:{self.tor_port}'
            }
            
            response = requests.get(
                'https://httpbin.org/ip',
                proxies=proxies,
                timeout=10
            )
            
            if response.status_code == 200:
                return response.json().get('origin')
            
        except Exception as e:
            self.logger.error(f"Failed to get current IP through Tor: {e}")
        
        return None
    
    def test_tor_connection(self) -> bool:
        """Test if Tor connection is working"""
        try:
            current_ip = self.get_current_ip()
            if current_ip:
                self.logger.info(f"Tor connection test successful. Current IP: {current_ip}")
                return True
            else:
                self.logger.error("Tor connection test failed")
                return False
                
        except Exception as e:
            self.logger.error(f"Error testing Tor connection: {e}")
            return False
    
    def get_circuit_info(self) -> List[Dict[str, Any]]:
        """Get information about current Tor circuits"""
        if not self.is_connected or not self.controller:
            return []
        
        try:
            circuits = []
            for circuit in self.controller.get_circuits():
                circuit_info = {
                    'id': circuit.id,
                    'status': circuit.status,
                    'purpose': circuit.purpose,
                    'path': []
                }
                
                for hop in circuit.path:
                    circuit_info['path'].append({
                        'fingerprint': hop[0],
                        'nickname': hop[1] if len(hop) > 1 else 'Unknown'
                    })
                
                circuits.append(circuit_info)
            
            return circuits
            
        except Exception as e:
            self.logger.error(f"Error getting circuit info: {e}")
            return []
    
    def get_guard_nodes(self) -> List[str]:
        """Get list of guard nodes being used"""
        if not self.is_connected or not self.controller:
            return []
        
        try:
            entry_guards = self.controller.get_conf('EntryGuards', multiple=True)
            return entry_guards if entry_guards else []
            
        except Exception as e:
            self.logger.error(f"Error getting guard nodes: {e}")
            return []
    
    def get_statistics(self) -> Dict[str, Any]:
        """Get Tor statistics"""
        return {
            'is_connected': self.is_connected,
            'is_tor_running': self.is_tor_running(),
            'circuit_count': self.circuit_count,
            'connection_attempts': self.connection_attempts,
            'successful_rotations': self.successful_rotations,
            'failed_rotations': self.failed_rotations,
            'success_rate': (self.successful_rotations / max(1, self.successful_rotations + self.failed_rotations)) * 100,
            'tor_port': self.tor_port,
            'control_port': self.control_port
        }
    
    def configure_tor(self, config: Dict[str, Any]) -> bool:
        """Configure Tor settings"""
        if not self.is_connected or not self.controller:
            return False
        
        try:
            for key, value in config.items():
                self.controller.set_conf(key, value)
            
            self.logger.info(f"Applied Tor configuration: {config}")
            return True
            
        except Exception as e:
            self.logger.error(f"Error configuring Tor: {e}")
            return False
    
    def stop_tor_service(self):
        """Stop Tor service"""
        try:
            if self.controller:
                self.controller.close()
                self.controller = None
            
            if self.tor_process:
                self.tor_process.terminate()
                self.tor_process.wait(timeout=10)
                self.tor_process = None
            
            self.is_connected = False
            self.logger.info("Tor service stopped")
            
        except Exception as e:
            self.logger.error(f"Error stopping Tor service: {e}")
    
    def cleanup(self):
        """Cleanup Tor connections"""
        self.stop_tor_service()
        self.logger.info("Tor controller cleaned up")
    
    def get_tor_version(self) -> Optional[str]:
        """Get Tor version"""
        if not self.is_connected or not self.controller:
            return None
        
        try:
            version_info = self.controller.get_version()
            return str(version_info)
        except Exception as e:
            self.logger.error(f"Error getting Tor version: {e}")
            return None
    
    def is_hibernating(self) -> bool:
        """Check if Tor is hibernating"""
        if not self.is_connected or not self.controller:
            return False
        
        try:
            return self.controller.is_hibernating()
        except Exception as e:
            self.logger.error(f"Error checking hibernation status: {e}")
            return False

    # GUI wrapper methods for compatibility
    def start(self) -> bool:
        """Start Tor service (wrapper for start_tor_service)"""
        return self.start_tor_service()
    
    def stop(self) -> bool:
        """Stop Tor service (wrapper for stop_tor_service)"""
        try:
            self.stop_tor_service()
            return True
        except Exception as e:
            self.logger.error(f"Error stopping Tor: {e}")
            return False
    
    def new_identity(self) -> bool:
        """Get new Tor identity (wrapper for new_circuit)"""
        return self.new_circuit()
