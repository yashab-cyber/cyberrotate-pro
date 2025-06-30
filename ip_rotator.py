#!/usr/bin/env python3
"""
CyberRotate Pro - Main IP Rotation Engine
Created by Yashab Alam - Founder & CEO of ZehraSec

This is the main entry point for the CyberRotate Pro application.
"""

import sys
import os
import time
import signal
import argparse
import json
from pathlib import Path
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, asdict

# Third-party imports
import requests
import colorama
from colorama import Fore, Back, Style
from rich.console import Console
from rich.table import Table
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.panel import Panel
from rich.text import Text

# Local imports
from core.proxy_manager import ProxyManager
from core.tor_controller import TorController
from core.openvpn_manager import OpenVPNManager
from core.security_utils import SecurityUtils
from core.network_monitor import NetworkMonitor
from utils.logger import setup_logger
from utils.stats_collector import StatsCollector
from utils.leak_detector import LeakDetector
from ui.interactive_menu import InteractiveMenu
from ui.cli_interface import CLIInterface

# Enterprise imports (conditional)
try:
    from core.api_server_enterprise import EnterpriseAPIServer
    from core.license_manager import LicenseManager
    from core.database_manager import DatabaseManager
    from ui.cli_interface_pro import ProCLIInterface
    ENTERPRISE_AVAILABLE = True
except ImportError:
    ENTERPRISE_AVAILABLE = False

# Initialize colorama for cross-platform colored output
colorama.init(autoreset=True)
console = Console()

@dataclass
class RotationConfig:
    """Configuration for IP rotation settings"""
    methods: List[str]
    interval: int
    max_retries: int
    timeout: int
    fail_threshold: int
    geolocation_targeting: bool
    countries: List[str]
    enable_logging: bool
    debug_mode: bool
    # Enterprise features
    api_enabled: bool = False
    api_port: int = 8080
    license_key: str = ""
    enterprise_mode: bool = False
    database_enabled: bool = False
    web_dashboard_enabled: bool = False

class IPRotator:
    """
    Main IP Rotation Engine
    
    This class orchestrates all IP rotation activities including:
    - Proxy management and rotation
    - Tor network integration
    - OpenVPN connection management
    - Security monitoring and leak detection
    - Statistics collection and reporting
    """
    
    def __init__(self, config_file: Optional[str] = None):
        """Initialize the IP Rotator with configuration"""
        self.config_file = config_file or "config/config.json"
        self.config = self._load_config()
        self.logger = setup_logger(debug=self.config.debug_mode)
        
        # Initialize enterprise components first
        self.license_manager = None
        self.database_manager = None
        self.api_server = None
        
        if self.config.enterprise_mode and ENTERPRISE_AVAILABLE:
            try:
                # Initialize license manager
                self.license_manager = LicenseManager(self.config.license_key, self.logger)
                
                # Initialize database if enabled
                if self.config.database_enabled:
                    self.database_manager = DatabaseManager(self.logger)
                
                # Initialize API server if enabled
                if self.config.api_enabled:
                    self.api_server = EnterpriseAPIServer(
                        port=self.config.api_port,
                        license_manager=self.license_manager,
                        database_manager=self.database_manager,
                        logger=self.logger
                    )
                    
                self.logger.info("Enterprise features initialized successfully")
            except Exception as e:
                self.logger.error(f"Failed to initialize enterprise features: {e}")
                self.config.enterprise_mode = False
        elif self.config.enterprise_mode and not ENTERPRISE_AVAILABLE:
            self.logger.warning("Enterprise mode requested but enterprise modules not available")
            self.config.enterprise_mode = False
        
        # Initialize core components
        self.proxy_manager = ProxyManager(self.logger)
        self.tor_controller = TorController(self.logger)
        self.openvpn_manager = OpenVPNManager(self.logger)
        self.security_utils = SecurityUtils(self.logger)
        self.network_monitor = NetworkMonitor(self.logger)
        self.stats_collector = StatsCollector(self.logger)
        self.leak_detector = LeakDetector(self.logger)
        
        # Runtime state
        self.is_running = False
        self.current_method = None
        self.rotation_count = 0
        self.start_time = None
        
        # Setup signal handlers
        signal.signal(signal.SIGINT, self._signal_handler)
        signal.signal(signal.SIGTERM, self._signal_handler)
        
        self.logger.info("CyberRotate Pro initialized successfully")
    
    def _load_config(self) -> RotationConfig:
        """Load configuration from file"""
        try:
            if os.path.exists(self.config_file):
                with open(self.config_file, 'r') as f:
                    config_data = json.load(f)
                
                # Extract rotation settings
                rotation_settings = config_data.get('rotation_settings', {})
                security_settings = config_data.get('security_settings', {})
                enterprise_settings = config_data.get('enterprise_settings', {})
                api_settings = config_data.get('api_settings', {})
                
                return RotationConfig(
                    methods=rotation_settings.get('methods', ['proxy', 'openvpn']),
                    interval=rotation_settings.get('interval', 10),
                    max_retries=rotation_settings.get('max_retries', 3),
                    timeout=rotation_settings.get('timeout', 10),
                    fail_threshold=rotation_settings.get('fail_threshold', 5),
                    geolocation_targeting=rotation_settings.get('geolocation_targeting', False),
                    countries=rotation_settings.get('countries', []),
                    enable_logging=config_data.get('monitoring', {}).get('logging_enabled', True),
                    debug_mode=config_data.get('debug_mode', False),
                    # Enterprise settings
                    api_enabled=api_settings.get('enabled', False),
                    api_port=api_settings.get('port', 8080),
                    license_key=enterprise_settings.get('license_key', ''),
                    enterprise_mode=enterprise_settings.get('enabled', False),
                    database_enabled=enterprise_settings.get('database_enabled', False),
                    web_dashboard_enabled=enterprise_settings.get('web_dashboard_enabled', False)
                )
            else:
                # Return default configuration
                return RotationConfig(
                    methods=['proxy', 'openvpn'],
                    interval=10,
                    max_retries=3,
                    timeout=10,
                    fail_threshold=5,
                    geolocation_targeting=False,
                    countries=[],
                    enable_logging=True,
                    debug_mode=False
                )
        except Exception as e:
            print(f"{Fore.RED}Error loading configuration: {e}{Style.RESET_ALL}")
            return RotationConfig(
                methods=['proxy'],
                interval=10,
                max_retries=3,
                timeout=10,
                fail_threshold=5,
                geolocation_targeting=False,
                countries=[],
                enable_logging=True,
                debug_mode=False
            )
    
    def _signal_handler(self, signum, frame):
        """Handle shutdown signals gracefully"""
        console.print(f"\n{Fore.YELLOW}Received shutdown signal. Cleaning up...{Style.RESET_ALL}")
        self.stop_rotation()
        sys.exit(0)
    
    def start_rotation(self, duration: Optional[int] = None) -> bool:
        """
        Start the IP rotation process
        
        Args:
            duration: Optional duration in seconds to run rotation
            
        Returns:
            bool: True if rotation started successfully
        """
        if self.is_running:
            console.print(f"{Fore.YELLOW}IP rotation is already running{Style.RESET_ALL}")
            return False
        
        self.is_running = True
        self.start_time = time.time()
        self.rotation_count = 0
        
        console.print(f"{Fore.GREEN}Starting IP rotation with methods: {', '.join(self.config.methods)}{Style.RESET_ALL}")
        
        try:
            end_time = time.time() + duration if duration else None
            
            while self.is_running:
                if end_time and time.time() >= end_time:
                    break
                
                # Perform rotation
                success = self._rotate_ip()
                if success:
                    self.rotation_count += 1
                    self.stats_collector.record_rotation(
                        method=self.current_method,
                        success=True,
                        response_time=0  # Will be updated with actual response time
                    )
                else:
                    self.stats_collector.record_rotation(
                        method=self.current_method,
                        success=False,
                        response_time=0
                    )
                
                # Wait for next rotation
                if self.is_running:
                    time.sleep(self.config.interval)
            
            return True
            
        except Exception as e:
            self.logger.error(f"Error during rotation: {e}")
            return False
        finally:
            self.is_running = False
    
    def _rotate_ip(self) -> bool:
        """
        Perform a single IP rotation
        
        Returns:
            bool: True if rotation was successful
        """
        for method in self.config.methods:
            try:
                if method == 'proxy':
                    success = self._rotate_proxy()
                elif method == 'tor':
                    success = self._rotate_tor()
                elif method == 'openvpn':
                    success = self._rotate_openvpn()
                else:
                    self.logger.warning(f"Unknown rotation method: {method}")
                    continue
                
                if success:
                    self.current_method = method
                    
                    # Verify new IP
                    new_ip = self.get_current_ip()
                    if new_ip:
                        console.print(f"{Fore.GREEN}✓ Rotated to new IP: {new_ip['ip']} ({new_ip.get('country', 'Unknown')}){Style.RESET_ALL}")
                        
                        # Check for leaks
                        if self.config.enable_logging:
                            self._check_security_leaks()
                        
                        return True
                    else:
                        console.print(f"{Fore.RED}✗ Failed to verify new IP for method: {method}{Style.RESET_ALL}")
                
            except Exception as e:
                self.logger.error(f"Error with rotation method {method}: {e}")
                continue
        
        console.print(f"{Fore.RED}✗ All rotation methods failed{Style.RESET_ALL}")
        return False
    
    def _rotate_proxy(self) -> bool:
        """Rotate to a new proxy"""
        return self.proxy_manager.rotate_proxy()
    
    def _rotate_tor(self) -> bool:
        """Rotate Tor circuit with robust error handling"""
        try:
            # First check if Tor is running
            if not self.tor_controller.is_tor_running():
                self.logger.info("Tor is not running, attempting to start...")
                if not self.tor_controller.start_tor_service():
                    self.logger.error("Failed to start Tor service")
                    console.print(f"{Fore.YELLOW}⚠ Tor service could not be started. Skipping Tor rotation.{Style.RESET_ALL}")
                    return False
                
                # Wait for Tor to fully initialize
                time.sleep(5)
            
            # Ensure Tor controller is connected
            if not self.tor_controller.is_connected:
                self.logger.info("Connecting to Tor controller...")
                if not self.tor_controller.connect_to_controller():
                    self.logger.error("Failed to connect to Tor controller")
                    console.print(f"{Fore.YELLOW}⚠ Could not connect to Tor controller. Check if stem library is installed.{Style.RESET_ALL}")
                    return False
            
            # Perform the circuit rotation
            return self.tor_controller.new_circuit()
            
        except Exception as e:
            self.logger.error(f"Error during Tor rotation: {e}")
            console.print(f"{Fore.YELLOW}⚠ Tor rotation failed: {e}{Style.RESET_ALL}")
            return False
    
    def _rotate_openvpn(self) -> bool:
        """Rotate OpenVPN connection"""
        return self.openvpn_manager.rotate_connection()
    
    def _check_security_leaks(self):
        """Check for various security leaks"""
        try:
            # Check DNS leaks
            dns_leak = self.leak_detector.check_dns_leak()
            if dns_leak:
                console.print(f"{Fore.YELLOW}⚠ DNS leak detected: {dns_leak}{Style.RESET_ALL}")
            
            # Check WebRTC leaks
            webrtc_leak = self.leak_detector.check_webrtc_leak()
            if webrtc_leak:
                console.print(f"{Fore.YELLOW}⚠ WebRTC leak detected: {webrtc_leak}{Style.RESET_ALL}")
            
        except Exception as e:
            self.logger.error(f"Error checking for leaks: {e}")
    
    def stop_rotation(self):
        """Stop the IP rotation process"""
        if self.is_running:
            self.is_running = False
            console.print(f"{Fore.YELLOW}Stopping IP rotation...{Style.RESET_ALL}")
            
            # Cleanup connections
            self.proxy_manager.cleanup()
            self.tor_controller.cleanup()
            self.openvpn_manager.cleanup()
            
            # Show final statistics
            self._show_final_stats()
        else:
            console.print(f"{Fore.YELLOW}IP rotation is not running{Style.RESET_ALL}")
    
    def get_current_ip(self) -> Optional[Dict[str, Any]]:
        """
        Get current public IP information
        
        Returns:
            Dict with IP information or None if failed
        """
        try:
            # Configure proxies based on current method
            proxies = None
            
            if self.current_method == 'tor' and self.tor_controller.is_connected:
                proxies = {
                    'http': 'socks5://127.0.0.1:9050',
                    'https': 'socks5://127.0.0.1:9050'
                }
            elif self.current_method == 'proxy' and self.proxy_manager.current_proxy:
                proxies = self.proxy_manager.get_proxy_dict()
            
            response = requests.get('https://ipapi.co/json/', proxies=proxies, timeout=self.config.timeout, verify=False)
            if response.status_code == 200:
                return response.json()
            else:
                # Fallback to simple IP check
                response = requests.get('https://httpbin.org/ip', proxies=proxies, timeout=self.config.timeout, verify=False)
                if response.status_code == 200:
                    return {'ip': response.json().get('origin')}
        except Exception as e:
            self.logger.error(f"Error getting current IP: {e}")
        
        return None
    
    def get_statistics(self) -> Dict[str, Any]:
        """Get rotation statistics"""
        stats = self.stats_collector.get_stats()
        
        # Add runtime statistics
        if self.start_time:
            runtime = time.time() - self.start_time
            stats['runtime_seconds'] = int(runtime)
            stats['runtime_formatted'] = self._format_duration(runtime)
        
        stats['rotation_count'] = self.rotation_count
        stats['current_method'] = self.current_method
        stats['is_running'] = self.is_running
        
        return stats
    
    def _format_duration(self, seconds: float) -> str:
        """Format duration in human-readable format"""
        hours, remainder = divmod(int(seconds), 3600)
        minutes, seconds = divmod(remainder, 60)
        
        if hours > 0:
            return f"{hours}h {minutes}m {seconds}s"
        elif minutes > 0:
            return f"{minutes}m {seconds}s"
        else:
            return f"{seconds}s"
    
    def _show_final_stats(self):
        """Display final statistics"""
        stats = self.get_statistics()
        
        table = Table(title="Final Rotation Statistics")
        table.add_column("Metric", style="cyan")
        table.add_column("Value", style="green")
        
        table.add_row("Total Rotations", str(stats.get('rotation_count', 0)))
        table.add_row("Runtime", stats.get('runtime_formatted', 'N/A'))
        table.add_row("Success Rate", f"{stats.get('success_rate', 0):.1f}%")
        table.add_row("Average Response Time", f"{stats.get('avg_response_time', 0):.2f}s")
        
        console.print(table)
    
    def test_connection(self) -> bool:
        """Test current internet connection"""
        try:
            response = requests.get('https://httpbin.org/ip', timeout=5)
            return response.status_code == 200
        except:
            return False
    
    def _validate_rotation_methods(self) -> List[str]:
        """Validate and filter rotation methods based on system capabilities"""
        available_methods = []
        
        for method in self.config.methods:
            if method == 'proxy':
                # Proxy should always be available
                available_methods.append(method)
            elif method == 'tor':
                # Check if Tor is available
                if self._check_tor_availability():
                    available_methods.append(method)
                else:
                    self.logger.warning("Tor method requested but Tor is not available")
                    console.print(f"{Fore.YELLOW}⚠ Tor rotation disabled: Tor not available on this system{Style.RESET_ALL}")
            elif method == 'openvpn':
                # Check if OpenVPN configs are available
                if self._check_openvpn_availability():
                    available_methods.append(method)
                else:
                    self.logger.warning("OpenVPN method requested but no VPN configs available")
                    console.print(f"{Fore.YELLOW}⚠ OpenVPN rotation disabled: No VPN configurations found{Style.RESET_ALL}")
        
        if not available_methods:
            # Fallback to proxy if nothing else is available
            self.logger.warning("No rotation methods available, falling back to proxy only")
            available_methods = ['proxy']
        
        return available_methods
    
    def _check_tor_availability(self) -> bool:
        """Check if Tor is available on this system"""
        try:
            # Check if Tor is installed
            if not self.tor_controller._check_tor_installation():
                return False
            
            # Check if stem library is available for control
            try:
                import stem
                return True
            except ImportError:
                self.logger.info("Tor is installed but stem library is missing. Install with: pip install stem")
                return False
                
        except Exception as e:
            self.logger.debug(f"Error checking Tor availability: {e}")
            return False
    
    def _check_openvpn_availability(self) -> bool:
        """Check if OpenVPN configurations are available"""
        try:
            # Check if OpenVPN manager has configurations
            return len(self.openvpn_manager.configs) > 0
        except Exception as e:
            self.logger.debug(f"Error checking OpenVPN availability: {e}")
            return False

def print_banner():
    """Print the application banner"""
    banner = """
╔══════════════════════════════════════════════════════════════════════════════╗
║                          CYBERROTATE PRO GLOBAL NETWORK                      ║
╠══════════════════════════════════════════════════════════════════════════════╣
║                                                                              ║
║   203.0.113.5 ──┐              ╭───────────╮              ┌── 8.8.8.8        ║
║                 │              │     🌍     │             │                 ║
║   1.1.1.1 ──────┼──────────────│   EARTH   │──────────────┼──── 9.9.9.9     ║
║                 │              │  NETWORK  │              │                 ║
║   74.125.224.72 ─┘              ╰───────────╯              └─ 208.67.222.222 ║
║                                                                              ║
║   ┌─── LIVE STATUS ──────────────────────────────────────────────────────┐   ║
║   │ 🔄 Current: 185.199.108.153 ➤ 104.21.14.101 ➤ 151.101.193.140      │   ║
║   │ 🌐 Nodes: 847 servers • 195 countries • 99.97% uptime              │   ║
║   │ 🛡️ Security: Zero logs • Kill switch • DNS leak protection          │   ║
║   └──────────────────────────────────────────────────────────────────────┘   ║
║                                                                              ║
║                    🔒 Professional IP Rotation Suite �                     ║
║                         Created by Yashab Alam - ZehraSec                   ║
║                                                                              ║
╚══════════════════════════════════════════════════════════════════════════════╝    """
    print(banner)

def main():
    """Main entry point"""
    print_banner()
    
    parser = argparse.ArgumentParser(
        description="CyberRotate Pro - Advanced IP Rotation & Anonymity Suite",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument('--config', type=str, help='Configuration file path')
    parser.add_argument('--start', action='store_true', help='Start rotation immediately')
    parser.add_argument('--duration', type=int, help='Run duration in seconds')
    parser.add_argument('--interactive', action='store_true', help='Start interactive mode')
    parser.add_argument('--gui', action='store_true', help='Launch graphical user interface')
    parser.add_argument('--method', choices=['proxy', 'tor', 'openvpn'], help='Specific rotation method')
    parser.add_argument('--interval', type=int, help='Rotation interval in seconds')
    parser.add_argument('--debug', action='store_true', help='Enable debug mode')
    parser.add_argument('--test', action='store_true', help='Test current connection')
    parser.add_argument('--stats', action='store_true', help='Show current statistics')
    parser.add_argument('--version', action='version', version='CyberRotate Pro v2.1.0')
    
    # Enterprise features
    parser.add_argument('--api-server', action='store_true', help='Start API server')
    parser.add_argument('--api-port', type=int, default=8080, help='API server port')
    parser.add_argument('--dashboard', action='store_true', help='Launch analytics dashboard')
    parser.add_argument('--enterprise', action='store_true', help='Enable enterprise mode')
    parser.add_argument('--license', type=str, help='Enterprise license key')
    parser.add_argument('--cli-pro', action='store_true', help='Launch enhanced CLI interface')
    parser.add_argument('--web-dashboard', action='store_true', help='Launch web dashboard')
    parser.add_argument('--docker-deploy', action='store_true', help='Deploy using Docker')
    parser.add_argument('--production-test', action='store_true', help='Run production tests')
    
    args = parser.parse_args()
    
    try:
        # Initialize rotator
        rotator = IPRotator(config_file=args.config)
        
        # Override config with command line arguments
        if args.method:
            rotator.config.methods = [args.method]
        if args.interval:
            rotator.config.interval = args.interval
        if args.debug:
            rotator.config.debug_mode = True
        if args.enterprise:
            rotator.config.enterprise_mode = True
        if args.license:
            rotator.config.license_key = args.license
        if args.api_server:
            rotator.config.api_enabled = True
            rotator.config.api_port = args.api_port
        
        # Handle different modes
        if args.test:
            console.print("Testing internet connection...")
            if rotator.test_connection():
                console.print(f"{Fore.GREEN}✓ Internet connection is working{Style.RESET_ALL}")
                ip_info = rotator.get_current_ip()
                if ip_info:
                    console.print(f"Current IP: {ip_info.get('ip', 'Unknown')}")
            else:
                console.print(f"{Fore.RED}✗ Internet connection failed{Style.RESET_ALL}")
                return 1
        
        elif args.stats:
            stats = rotator.get_statistics()
            table = Table(title="Current Statistics")
            table.add_column("Metric", style="cyan")
            table.add_column("Value", style="green")
            
            for key, value in stats.items():
                table.add_row(str(key).replace('_', ' ').title(), str(value))
            
            console.print(table)
        elif args.start:
            console.print("Starting IP rotation...")
            rotator.start_rotation(duration=args.duration)
        
        elif args.interactive:
            # Start interactive menu
            menu = InteractiveMenu(rotator)
            menu.run()
        
        elif args.gui:
            # Launch GUI
            try:
                import subprocess
                import sys
                subprocess.run([sys.executable, 'gui_launcher.py'])
            except Exception as e:
                console.print(f"[red]Failed to launch GUI: {e}[/red]")
                console.print("Try running: python gui_launcher.py")
        
        elif args.api_server:
            # Start API server
            if ENTERPRISE_AVAILABLE and rotator.api_server:
                console.print(f"Starting API server on port {rotator.config.api_port}...")
                rotator.api_server.start()
            else:
                console.print("[red]API server not available. Install enterprise dependencies or enable enterprise mode.[/red]")
        
        elif args.dashboard:
            # Launch analytics dashboard
            try:
                import subprocess
                import sys
                subprocess.run([sys.executable, 'ui/analytics_dashboard.py'])
            except Exception as e:
                console.print(f"[red]Failed to launch dashboard: {e}[/red]")
                console.print("Try installing dashboard dependencies: pip install -r requirements-dashboard.txt")
        
        elif args.cli_pro:
            # Launch enhanced CLI
            if ENTERPRISE_AVAILABLE:
                try:
                    pro_cli = ProCLIInterface(api_base_url=f"http://localhost:{rotator.config.api_port}")
                    pro_cli.run()
                except Exception as e:
                    console.print(f"[red]Failed to launch Pro CLI: {e}[/red]")
            else:
                console.print("[red]Pro CLI not available. Install enterprise dependencies.[/red]")
        
        elif args.web_dashboard:
            # Launch web dashboard
            try:
                import subprocess
                import sys
                subprocess.run([sys.executable, 'ui/web_dashboard.py'])
            except Exception as e:
                console.print(f"[red]Failed to launch web dashboard: {e}[/red]")
        
        elif args.docker_deploy:
            # Deploy using Docker
            console.print("Starting Docker deployment...")
            try:
                import subprocess
                subprocess.run(['bash', 'deploy_production.sh', '--docker'])
            except Exception as e:
                console.print(f"[red]Docker deployment failed: {e}[/red]")
        
        elif args.production_test:
            # Run production tests
            console.print("Running production test suite...")
            try:
                import subprocess
                result = subprocess.run([sys.executable, 'test_production.py'], capture_output=True, text=True)
                console.print(result.stdout)
                if result.stderr:
                    console.print(f"[red]{result.stderr}[/red]")
            except Exception as e:
                console.print(f"[red]Production tests failed: {e}[/red]")
        
        else:
            # Default behavior - show help or start interactive mode
            console.print("Welcome to CyberRotate Pro!")
            console.print("Use --help for command line options or --interactive for interactive mode.")
            
            # Ask user what they want to do            
            console.print("\nQuick start options:")
            console.print("1. Start rotation immediately: --start")
            console.print("2. Interactive mode: --interactive")
            console.print("3. Graphical interface: --gui")
            console.print("4. Test connection: --test")
            console.print("5. Show help: --help")
            console.print("\nEnterprise features:")
            console.print("6. Start API server: --api-server")
            console.print("7. Launch analytics dashboard: --dashboard")
            console.print("8. Enhanced CLI interface: --cli-pro")
            console.print("9. Web dashboard: --web-dashboard")
            console.print("10. Production deployment: --docker-deploy")
            console.print("11. Run production tests: --production-test")
        
        return 0
        
    except KeyboardInterrupt:
        console.print(f"\n{Fore.YELLOW}Operation cancelled by user{Style.RESET_ALL}")
        return 1
    except Exception as e:
        console.print(f"{Fore.RED}Error: {e}{Style.RESET_ALL}")
        return 1

if __name__ == "__main__":
    sys.exit(main())
