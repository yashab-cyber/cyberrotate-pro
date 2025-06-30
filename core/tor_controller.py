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
            # Check SOCKS port
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(3)
            socks_result = sock.connect_ex(('127.0.0.1', self.tor_port))
            sock.close()
            
            if socks_result == 0:
                # Also check control port if possible
                try:
                    ctrl_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    ctrl_sock.settimeout(3)
                    ctrl_result = ctrl_sock.connect_ex(('127.0.0.1', self.control_port))
                    ctrl_sock.close()
                    
                    if ctrl_result == 0:
                        self.logger.debug("Both Tor SOCKS and control ports are accessible")
                    else:
                        self.logger.debug("Tor SOCKS port accessible but control port is not")
                    
                except Exception:
                    pass
                
                return True
            else:
                return False
                
        except Exception as e:
            self.logger.debug(f"Error checking Tor status: {e}")
            return False
    
    def start_tor_service(self) -> bool:
        """Start Tor service if not running"""
        if self.is_tor_running():
            self.logger.info("Tor service is already running")
            return True
        
        # First check if Tor is installed
        if not self._check_tor_installation():
            self.logger.error("Tor is not installed on this system")
            self.logger.info("Installation instructions:")
            self.logger.info(self.install_tor_instructions())
            return False
        
        try:
            # Try different methods in order of preference
            methods = []
            
            if STEM_AVAILABLE:
                methods.append(("stem", self._start_tor_with_stem))
            
            methods.append(("system", self._start_tor_system))
            
            for method_name, method_func in methods:
                self.logger.info(f"Attempting to start Tor using {method_name} method...")
                
                try:
                    if method_func():
                        self.logger.info(f"Tor started successfully using {method_name} method")
                        return True
                except Exception as e:
                    self.logger.warning(f"Failed to start Tor with {method_name} method: {e}")
                    continue
            
            # If all methods failed, provide helpful guidance
            self.logger.error("Failed to start Tor service using all available methods")
            self.logger.info("Troubleshooting tips:")
            self.logger.info("1. Check if Tor is properly installed")
            self.logger.info("2. Check if ports 9050 and 9051 are available")
            self.logger.info("3. Run with elevated privileges if needed")
            self.logger.info("4. Check firewall settings")
            self.logger.info("5. Try starting Tor manually: 'tor'")
            
            return False
                
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
        # Extended list of possible Tor locations
        tor_commands = [
            'tor',
            '/usr/bin/tor',
            '/usr/sbin/tor',
            '/usr/local/bin/tor',
            '/opt/tor/bin/tor',
            '/snap/bin/tor',
            'C:\\Program Files\\Tor Browser\\Browser\\TorBrowser\\Tor\\tor.exe',
            'C:\\Program Files (x86)\\Tor Browser\\Browser\\TorBrowser\\Tor\\tor.exe',
            'C:\\Users\\' + os.environ.get('USERNAME', '') + '\\Desktop\\Tor Browser\\Browser\\TorBrowser\\Tor\\tor.exe',
            '/Applications/TorBrowser.app/Contents/MacOS/Tor/tor'
        ]
        
        # Check if Tor is available via package manager first
        if not self._check_tor_installation():
            self.logger.warning("Tor may not be installed. Please install Tor using your system package manager.")
            self.logger.info("Installation commands:")
            self.logger.info("Ubuntu/Debian: sudo apt-get install tor")
            self.logger.info("CentOS/RHEL: sudo yum install tor")
            self.logger.info("macOS: brew install tor")
            self.logger.info("Windows: Download from https://www.torproject.org/")
        
        for tor_cmd in tor_commands:
            try:
                # Check if command exists
                if not self._command_exists(tor_cmd):
                    continue
                    
                self.logger.info(f"Trying to start Tor with command: {tor_cmd}")
                
                # Create Tor configuration with better compatibility
                tor_config = f"""
SocksPort {self.tor_port}
ControlPort {self.control_port}
DataDirectory {self._get_tor_data_directory()}
GeoIPFile /usr/share/tor/geoip
GeoIPv6File /usr/share/tor/geoip6
Log notice file {os.path.join(self._get_tor_data_directory(), 'tor.log')}
PidFile {os.path.join(self._get_tor_data_directory(), 'tor.pid')}
RunAsDaemon 0
"""
                
                # Write temporary config file
                config_path = os.path.join(self._get_tor_data_directory(), 'torrc')
                os.makedirs(os.path.dirname(config_path), exist_ok=True)
                
                with open(config_path, 'w') as f:
                    f.write(tor_config)
                
                # Start Tor process with better error handling
                self.tor_process = subprocess.Popen(
                    [tor_cmd, '-f', config_path],
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    text=True,
                    cwd=self._get_tor_data_directory()
                )
                
                # Wait for Tor to start with progress checking
                for i in range(20):  # Wait up to 20 seconds
                    time.sleep(1)
                    if self.is_tor_running():
                        self.logger.info("Tor service started successfully")
                        return True
                    if self.tor_process.poll() is not None:
                        # Process ended, check for errors
                        stdout, stderr = self.tor_process.communicate()
                        self.logger.error(f"Tor process ended early. stderr: {stderr}")
                        break
                    
            except FileNotFoundError:
                self.logger.debug(f"Tor command not found: {tor_cmd}")
                continue
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

    def _check_tor_installation(self) -> bool:
        """Check if Tor is properly installed on the system"""
        tor_paths = [
            '/usr/bin/tor',
            '/usr/sbin/tor',
            '/usr/local/bin/tor',
            '/opt/tor/bin/tor',
            '/snap/bin/tor'
        ]
        
        # Check common installation paths
        for path in tor_paths:
            if os.path.exists(path) and os.access(path, os.X_OK):
                return True
        
        # Check if tor is in PATH
        return self._command_exists('tor')
    
    def _command_exists(self, command: str) -> bool:
        """Check if a command exists and is executable"""
        try:
            if os.path.isfile(command) and os.access(command, os.X_OK):
                return True
            
            # Check if command is in PATH
            if sys.platform == 'win32':
                # Windows - check with 'where'
                result = subprocess.run(['where', command], 
                                      capture_output=True, text=True)
                return result.returncode == 0
            else:
                # Unix-like - check with 'which'
                result = subprocess.run(['which', command], 
                                      capture_output=True, text=True)
                return result.returncode == 0
        except:
            return False
    
    def install_tor_instructions(self) -> str:
        """Get Tor installation instructions for the current platform"""
        instructions = []
        
        if sys.platform.startswith('linux'):
            instructions.append("Linux Installation:")
            instructions.append("  Ubuntu/Debian: sudo apt-get update && sudo apt-get install tor")
            instructions.append("  CentOS/RHEL: sudo yum install tor")
            instructions.append("  Fedora: sudo dnf install tor")
            instructions.append("  Arch: sudo pacman -S tor")
        elif sys.platform == 'darwin':
            instructions.append("macOS Installation:")
            instructions.append("  Homebrew: brew install tor")
            instructions.append("  MacPorts: sudo port install tor")
        elif sys.platform == 'win32':
            instructions.append("Windows Installation:")
            instructions.append("  1. Download Tor Browser from https://www.torproject.org/")
            instructions.append("  2. Or install via Chocolatey: choco install tor")
            instructions.append("  3. Or use Windows Subsystem for Linux (WSL)")
        
        instructions.append("\nAlternatively, you can use CyberRotate Pro without Tor by")
        instructions.append("using only proxy or VPN rotation methods.")
        
        return "\n".join(instructions)

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
