#!/usr/bin/env python3
"""
Tor Service Test and Diagnostic Tool
Created for CyberRotate Pro

This script tests Tor installation and connectivity across different devices.
"""

import os
import sys
import time
import socket
import subprocess
import logging
from pathlib import Path

# Add the project root to Python path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from core.tor_controller import TorController
from utils.logger import setup_logger

class TorDiagnostics:
    """Comprehensive Tor diagnostics and testing"""
    
    def __init__(self):
        self.logger = setup_logger(debug=True)
        self.tor_controller = TorController(self.logger)
        
    def run_full_diagnostic(self):
        """Run complete Tor diagnostic"""
        print("=" * 60)
        print("CyberRotate Pro - Tor Diagnostic Tool")
        print("=" * 60)
        
        tests = [
            ("System Information", self.test_system_info),
            ("Tor Installation Check", self.test_tor_installation),
            ("Port Availability", self.test_port_availability),
            ("Tor Service Status", self.test_tor_service_status),
            ("Tor Service Start", self.test_tor_service_start),
            ("Controller Connection", self.test_controller_connection),
            ("IP Rotation Test", self.test_ip_rotation),
            ("Network Connectivity", self.test_network_connectivity)
        ]
        
        results = {}
        
        for test_name, test_func in tests:
            print(f"\n--- {test_name} ---")
            try:
                result = test_func()
                results[test_name] = result
                status = "PASS" if result else "FAIL"
                print(f"Result: {status}")
            except Exception as e:
                results[test_name] = False
                print(f"Result: ERROR - {e}")
        
        self.print_summary(results)
        
    def test_system_info(self) -> bool:
        """Test system information"""
        print(f"Operating System: {sys.platform}")
        print(f"Python Version: {sys.version}")
        print(f"Working Directory: {os.getcwd()}")
        
        # Check environment variables
        important_vars = ['PATH', 'HOME', 'USER', 'USERNAME']
        for var in important_vars:
            value = os.environ.get(var, 'Not set')
            print(f"{var}: {value}")
        
        return True
    
    def test_tor_installation(self) -> bool:
        """Test Tor installation"""
        print("Checking Tor installation...")
        
        # Check if Tor is installed
        tor_installed = self.tor_controller._check_tor_installation()
        print(f"Tor installed: {tor_installed}")
        
        if not tor_installed:
            print("Tor installation instructions:")
            print(self.tor_controller.install_tor_instructions())
            return False
        
        # Try to get Tor version
        tor_commands = ['tor', '/usr/bin/tor', '/usr/sbin/tor']
        
        for cmd in tor_commands:
            try:
                if self.tor_controller._command_exists(cmd):
                    result = subprocess.run([cmd, '--version'], 
                                          capture_output=True, text=True, timeout=10)
                    if result.returncode == 0:
                        print(f"Tor version: {result.stdout.strip()}")
                        return True
            except Exception as e:
                print(f"Error checking Tor version with {cmd}: {e}")
        
        return tor_installed
    
    def test_port_availability(self) -> bool:
        """Test if required ports are available"""
        ports = [9050, 9051]  # SOCKS and Control ports
        
        all_available = True
        
        for port in ports:
            try:
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.settimeout(2)
                result = sock.connect_ex(('127.0.0.1', port))
                sock.close()
                
                if result == 0:
                    print(f"Port {port}: IN USE")
                    # Port is in use, check if it's Tor
                    if port == 9050:
                        # Test if it's actually Tor SOCKS
                        is_tor = self.test_socks_proxy(port)
                        print(f"Port {port} appears to be Tor SOCKS: {is_tor}")
                else:
                    print(f"Port {port}: AVAILABLE")
                    
            except Exception as e:
                print(f"Error checking port {port}: {e}")
                all_available = False
        
        return True  # Ports being available or in use by Tor is both OK
    
    def test_socks_proxy(self, port: int) -> bool:
        """Test if a port is running SOCKS proxy"""
        try:
            import socks
            import socket
            
            # Try to create a SOCKS connection
            sock = socks.socksocket()
            sock.set_proxy(socks.SOCKS5, "127.0.0.1", port)
            sock.settimeout(5)
            
            # Try to connect to a test address
            try:
                sock.connect(("httpbin.org", 80))
                sock.close()
                return True
            except:
                sock.close()
                return False
                
        except ImportError:
            # PySocks not available, can't test
            return False
        except Exception:
            return False
    
    def test_tor_service_status(self) -> bool:
        """Test current Tor service status"""
        is_running = self.tor_controller.is_tor_running()
        print(f"Tor service running: {is_running}")
        
        if is_running:
            print("Tor is already running on this system")
        
        return True  # This is informational, not a failure
    
    def test_tor_service_start(self) -> bool:
        """Test starting Tor service"""
        print("Attempting to start Tor service...")
        
        # First check if already running
        if self.tor_controller.is_tor_running():
            print("Tor is already running")
            return True
        
        # Try to start Tor
        success = self.tor_controller.start_tor_service()
        
        if success:
            print("Tor service started successfully")
            
            # Wait a moment and verify
            time.sleep(3)
            if self.tor_controller.is_tor_running():
                print("Tor service verified as running")
                return True
            else:
                print("Tor service started but not responding")
                return False
        else:
            print("Failed to start Tor service")
            return False
    
    def test_controller_connection(self) -> bool:
        """Test Tor controller connection"""
        print("Testing Tor controller connection...")
        
        if not self.tor_controller.is_tor_running():
            print("Tor service is not running")
            return False
        
        success = self.tor_controller.connect_to_controller()
        
        if success:
            print("Successfully connected to Tor controller")
            return True
        else:
            print("Failed to connect to Tor controller")
            return False
    
    def test_ip_rotation(self) -> bool:
        """Test IP rotation functionality"""
        print("Testing IP rotation...")
        
        if not self.tor_controller.is_connected:
            print("Tor controller not connected")
            return False
        
        # Get initial IP
        initial_ip = self.tor_controller.get_current_ip()
        print(f"Initial IP: {initial_ip}")
        
        if not initial_ip:
            print("Could not get initial IP through Tor")
            return False
        
        # Rotate circuit
        print("Rotating Tor circuit...")
        rotation_success = self.tor_controller.new_circuit()
        
        if not rotation_success:
            print("Failed to rotate Tor circuit")
            return False
        
        # Wait and get new IP
        time.sleep(5)
        new_ip = self.tor_controller.get_current_ip()
        print(f"New IP: {new_ip}")
        
        if new_ip and new_ip != initial_ip:
            print("IP rotation successful")
            return True
        else:
            print("IP rotation may have failed (same IP returned)")
            return False
    
    def test_network_connectivity(self) -> bool:
        """Test network connectivity through Tor"""
        print("Testing network connectivity through Tor...")
        
        if not self.tor_controller.is_tor_running():
            print("Tor service is not running")
            return False
        
        try:
            import requests
            
            # Test with Tor proxy
            proxies = {
                'http': 'socks5://127.0.0.1:9050',
                'https': 'socks5://127.0.0.1:9050'
            }
            
            response = requests.get('https://httpbin.org/ip', 
                                  proxies=proxies, 
                                  timeout=15)
            
            if response.status_code == 200:
                data = response.json()
                tor_ip = data.get('origin')
                print(f"Successfully connected through Tor. IP: {tor_ip}")
                
                # Also test without proxy to compare
                direct_response = requests.get('https://httpbin.org/ip', timeout=10)
                if direct_response.status_code == 200:
                    direct_ip = direct_response.json().get('origin')
                    print(f"Direct connection IP: {direct_ip}")
                    
                    if tor_ip != direct_ip:
                        print("Tor is successfully masking your IP")
                        return True
                    else:
                        print("Warning: Tor IP same as direct IP")
                        return False
                else:
                    print("Could not test direct connection")
                    return True  # Tor worked, that's what matters
            else:
                print(f"HTTP request through Tor failed: {response.status_code}")
                return False
                
        except Exception as e:
            print(f"Network connectivity test failed: {e}")
            return False
    
    def print_summary(self, results: dict):
        """Print diagnostic summary"""
        print("\n" + "=" * 60)
        print("DIAGNOSTIC SUMMARY")
        print("=" * 60)
        
        passed = sum(1 for result in results.values() if result)
        total = len(results)
        
        print(f"Tests passed: {passed}/{total}")
        
        if passed == total:
            print("\n✅ All tests passed! Tor should work correctly on this device.")
        else:
            print(f"\n❌ {total - passed} test(s) failed. See details above.")
            
            print("\nRecommendations:")
            if not results.get("Tor Installation Check", True):
                print("- Install Tor using your system package manager")
            if not results.get("Tor Service Start", True):
                print("- Check if you have sufficient permissions")
                print("- Check if ports 9050 and 9051 are available")
                print("- Try running as administrator/root")
            if not results.get("Controller Connection", True):
                print("- Install 'stem' library: pip install stem")
                print("- Check Tor control port configuration")
        
        print("\n" + "=" * 60)
    
    def cleanup(self):
        """Cleanup resources"""
        try:
            self.tor_controller.cleanup()
        except Exception as e:
            print(f"Error during cleanup: {e}")

def main():
    """Main function"""
    diagnostics = TorDiagnostics()
    
    try:
        diagnostics.run_full_diagnostic()
    except KeyboardInterrupt:
        print("\n\nDiagnostic interrupted by user")
    except Exception as e:
        print(f"\nUnexpected error during diagnostic: {e}")
    finally:
        diagnostics.cleanup()

if __name__ == "__main__":
    main()
