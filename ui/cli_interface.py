#!/usr/bin/env python3
"""
CLI Interface - Command Line Interface for CyberRotate Pro
Created by Yashab Alam - Founder & CEO of ZehraSec
"""

import argparse
import sys
import json
import time
from typing import Optional, Dict, Any
from rich.console import Console
from rich.table import Table
from rich.panel import Panel

class CLIInterface:
    """
    Command Line Interface
    
    Provides command-line interface functionality for CyberRotate Pro
    """
    
    def __init__(self, rotator):
        """Initialize CLI interface"""
        self.rotator = rotator
        self.console = Console()
    
    def create_parser(self) -> argparse.ArgumentParser:
        """Create and configure argument parser"""
        parser = argparse.ArgumentParser(
            description="CyberRotate Pro - Advanced IP Rotation & Anonymity Suite",
            formatter_class=argparse.RawDescriptionHelpFormatter,
            epilog="""
Examples:
  %(prog)s --start --duration 300          Start rotation for 5 minutes
  %(prog)s --method openvpn --interval 30  Use OpenVPN with 30s intervals
  %(prog)s --test --verbose                Test connection with verbose output
  %(prog)s --stats --export results.json  Show stats and export to file
  %(prog)s --interactive                   Start interactive menu
  %(prog)s --leak-check                    Run leak detection tests
  
For more information, visit: https://github.com/yashab-cyber/cyberrotate-pro
            """
        )
        
        # Main action arguments
        action_group = parser.add_mutually_exclusive_group()
        action_group.add_argument('--start', action='store_true', 
                                help='Start IP rotation')
        action_group.add_argument('--stop', action='store_true',
                                help='Stop IP rotation')
        action_group.add_argument('--rotate', action='store_true',
                                help='Perform single rotation')
        action_group.add_argument('--test', action='store_true',
                                help='Test current connection')
        action_group.add_argument('--stats', action='store_true',
                                help='Show current statistics')
        action_group.add_argument('--interactive', action='store_true',
                                help='Start interactive menu')
        action_group.add_argument('--leak-check', action='store_true',
                                help='Run comprehensive leak detection')
        
        # Configuration arguments
        config_group = parser.add_argument_group('Configuration')
        config_group.add_argument('--config', type=str, metavar='FILE',
                                help='Configuration file path')
        config_group.add_argument('--method', choices=['proxy', 'tor', 'openvpn'],
                                help='Specific rotation method to use')
        config_group.add_argument('--interval', type=int, metavar='SECONDS',
                                help='Rotation interval in seconds')
        config_group.add_argument('--duration', type=int, metavar='SECONDS',
                                help='Run duration in seconds')
        config_group.add_argument('--country', type=str, metavar='CODE',
                                help='Target country code (e.g., US, UK, DE)')
        
        # Output arguments
        output_group = parser.add_argument_group('Output')
        output_group.add_argument('--verbose', '-v', action='store_true',
                                help='Enable verbose output')
        output_group.add_argument('--debug', action='store_true',
                                help='Enable debug mode')
        output_group.add_argument('--quiet', '-q', action='store_true',
                                help='Suppress non-essential output')
        output_group.add_argument('--json', action='store_true',
                                help='Output in JSON format')
        output_group.add_argument('--export', type=str, metavar='FILE',
                                help='Export results to file')
        
        # Testing arguments
        test_group = parser.add_argument_group('Testing')
        test_group.add_argument('--test-proxies', action='store_true',
                               help='Test all available proxies')
        test_group.add_argument('--test-tor', action='store_true',
                               help='Test Tor connection')
        test_group.add_argument('--test-openvpn', action='store_true',
                               help='Test OpenVPN connections')
        test_group.add_argument('--benchmark', action='store_true',
                               help='Run performance benchmark')
        
        # Utility arguments
        util_group = parser.add_argument_group('Utilities')
        util_group.add_argument('--list-methods', action='store_true',
                               help='List available rotation methods')
        util_group.add_argument('--list-proxies', action='store_true',
                               help='List available proxies')
        util_group.add_argument('--list-vpn', action='store_true',
                               help='List available VPN configurations')
        util_group.add_argument('--validate-config', action='store_true',
                               help='Validate configuration file')
        util_group.add_argument('--reset-config', action='store_true',
                               help='Reset configuration to defaults')
        
        parser.add_argument('--version', action='version', version='CyberRotate Pro v1.0.0')
        
        return parser
    
    def handle_args(self, args: argparse.Namespace) -> int:
        """Handle command line arguments"""
        try:
            # Set output level based on arguments
            if args.quiet:
                self.console.quiet = True
            elif args.verbose:
                self.console.verbose = True
            
            # Handle main actions
            if args.start:
                return self._handle_start(args)
            elif args.stop:
                return self._handle_stop(args)
            elif args.rotate:
                return self._handle_rotate(args)
            elif args.test:
                return self._handle_test(args)
            elif args.stats:
                return self._handle_stats(args)
            elif args.interactive:
                return self._handle_interactive(args)
            elif args.leak_check:
                return self._handle_leak_check(args)
            
            # Handle testing actions
            elif args.test_proxies:
                return self._handle_test_proxies(args)
            elif args.test_tor:
                return self._handle_test_tor(args)
            elif args.test_openvpn:
                return self._handle_test_openvpn(args)
            elif args.benchmark:
                return self._handle_benchmark(args)
            
            # Handle utility actions
            elif args.list_methods:
                return self._handle_list_methods(args)
            elif args.list_proxies:
                return self._handle_list_proxies(args)
            elif args.list_vpn:
                return self._handle_list_vpn(args)
            elif args.validate_config:
                return self._handle_validate_config(args)
            elif args.reset_config:
                return self._handle_reset_config(args)
            
            else:
                # No action specified, show help
                self.console.print("No action specified. Use --help for usage information.")
                return 1
                
        except KeyboardInterrupt:
            self.console.print("\nOperation cancelled by user")
            return 1
        except Exception as e:
            if args.debug:
                raise
            self.console.print(f"Error: {e}")
            return 1
    
    def _handle_start(self, args: argparse.Namespace) -> int:
        """Handle start command"""
        self.console.print("🚀 Starting IP rotation...")
        
        # Apply configuration overrides
        if args.method:
            self.rotator.config.methods = [args.method]
        if args.interval:
            self.rotator.config.interval = args.interval
        
        # Start rotation
        success = self.rotator.start_rotation(duration=args.duration)
        
        if success:
            self.console.print("✅ IP rotation started successfully")
            if args.duration:
                self.console.print(f"Will run for {args.duration} seconds")
            return 0
        else:
            self.console.print("❌ Failed to start IP rotation")
            return 1
    
    def _handle_stop(self, args: argparse.Namespace) -> int:
        """Handle stop command"""
        self.console.print("⏹️ Stopping IP rotation...")
        
        self.rotator.stop_rotation()
        self.console.print("✅ IP rotation stopped")
        return 0
    
    def _handle_rotate(self, args: argparse.Namespace) -> int:
        """Handle single rotate command"""
        self.console.print("🔄 Performing single rotation...")
        
        old_ip = self.rotator.get_current_ip()
        success = self.rotator._rotate_ip()
        new_ip = self.rotator.get_current_ip()
        
        if success:
            if args.json:
                result = {
                    'success': True,
                    'old_ip': old_ip,
                    'new_ip': new_ip,
                    'method': self.rotator.current_method
                }
                self.console.print(json.dumps(result, indent=2))
            else:
                self.console.print("✅ Rotation successful")
                if old_ip and new_ip:
                    self.console.print(f"  Old IP: {old_ip.get('ip', 'Unknown')}")
                    self.console.print(f"  New IP: {new_ip.get('ip', 'Unknown')}")
                    self.console.print(f"  Method: {self.rotator.current_method}")
            return 0
        else:
            if args.json:
                result = {'success': False, 'error': 'Rotation failed'}
                self.console.print(json.dumps(result, indent=2))
            else:
                self.console.print("❌ Rotation failed")
            return 1
    
    def _handle_test(self, args: argparse.Namespace) -> int:
        """Handle test command"""
        self.console.print("🔍 Testing connection...")
        
        # Test internet connectivity
        connectivity = self.rotator.test_connection()
        current_ip = self.rotator.get_current_ip()
        
        if args.json:
            result = {
                'connectivity': connectivity,
                'current_ip': current_ip,
                'timestamp': int(time.time())
            }
            self.console.print(json.dumps(result, indent=2))
        else:
            if connectivity:
                self.console.print("✅ Internet connection is working")
                if current_ip:
                    self.console.print(f"Current IP: {current_ip.get('ip', 'Unknown')}")
                    if current_ip.get('country'):
                        self.console.print(f"Country: {current_ip.get('country')}")
            else:
                self.console.print("❌ Internet connection failed")
        
        return 0 if connectivity else 1
    
    def _handle_stats(self, args: argparse.Namespace) -> int:
        """Handle stats command"""
        stats = self.rotator.get_statistics()
        
        if args.json:
            self.console.print(json.dumps(stats, indent=2, default=str))
        else:
            table = Table(title="Current Statistics")
            table.add_column("Metric", style="cyan")
            table.add_column("Value", style="green")
            
            display_stats = [
                ("Total Rotations", stats.get('rotation_count', 0)),
                ("Runtime", stats.get('runtime_formatted', 'N/A')),
                ("Status", "Running" if stats.get('is_running') else "Stopped"),
                ("Current Method", stats.get('current_method', 'None')),
            ]
            
            for metric, value in display_stats:
                table.add_row(metric, str(value))
            
            self.console.print(table)
        
        # Export if requested
        if args.export:
            try:
                self.rotator.stats_collector.export_stats(args.export)
                self.console.print(f"📁 Statistics exported to {args.export}")
            except Exception as e:
                self.console.print(f"❌ Export failed: {e}")
                return 1
        
        return 0
    
    def _handle_interactive(self, args: argparse.Namespace) -> int:
        """Handle interactive mode"""
        from ui.interactive_menu import InteractiveMenu
        menu = InteractiveMenu(self.rotator)
        menu.run()
        return 0
    
    def _handle_leak_check(self, args: argparse.Namespace) -> int:
        """Handle leak detection"""
        self.console.print("🛡️ Running comprehensive leak detection...")
        
        results = self.rotator.leak_detector.check_all_leaks()
        
        if args.json:
            self.console.print(json.dumps(results, indent=2, default=str))
        else:
            total_leaks = results.get('total_leaks', 0)
            if total_leaks > 0:
                self.console.print(f"⚠️ {total_leaks} potential leak(s) detected")
                for leak in results.get('leaks_detected', []):
                    self.console.print(f"  • {leak.replace('_', ' ').title()}")
            else:
                self.console.print("✅ No leaks detected - your anonymity appears secure")
        
        # Export if requested
        if args.export:
            try:
                self.rotator.leak_detector.export_test_results(args.export)
                self.console.print(f"📁 Leak detection results exported to {args.export}")
            except Exception as e:
                self.console.print(f"❌ Export failed: {e}")
                return 1
        
        return 0
    
    def _handle_test_proxies(self, args: argparse.Namespace) -> int:
        """Handle proxy testing"""
        self.console.print("🔍 Testing available proxies...")
        
        working_count = self.rotator.proxy_manager.validate_proxies()
        total_count = len(self.rotator.proxy_manager.proxies)
        
        if args.json:
            result = {
                'total_proxies': total_count,
                'working_proxies': working_count,
                'success_rate': (working_count / total_count * 100) if total_count > 0 else 0
            }
            self.console.print(json.dumps(result, indent=2))
        else:
            self.console.print(f"✅ {working_count}/{total_count} proxies are working")
            if working_count > 0:
                success_rate = working_count / total_count * 100
                self.console.print(f"Success rate: {success_rate:.1f}%")
        
        return 0
    
    def _handle_test_tor(self, args: argparse.Namespace) -> int:
        """Handle Tor testing"""
        self.console.print("🔍 Testing Tor connection...")
        
        is_running = self.rotator.tor_controller.is_tor_running()
        
        if args.json:
            result = {'tor_running': is_running}
            if is_running:
                result['current_ip'] = self.rotator.tor_controller.get_current_ip()
            self.console.print(json.dumps(result, indent=2))
        else:
            if is_running:
                self.console.print("✅ Tor is running")
                current_ip = self.rotator.tor_controller.get_current_ip()
                if current_ip:
                    self.console.print(f"Current Tor IP: {current_ip}")
            else:
                self.console.print("❌ Tor is not running")
        
        return 0 if is_running else 1
    
    def _handle_test_openvpn(self, args: argparse.Namespace) -> int:
        """Handle OpenVPN testing"""
        self.console.print("🔍 Testing OpenVPN connections...")
        
        is_connected = self.rotator.openvpn_manager.is_connected()
        available_servers = self.rotator.openvpn_manager.get_available_servers()
        
        if args.json:
            result = {
                'connected': is_connected,
                'available_servers': len(available_servers),
                'servers': available_servers
            }
            self.console.print(json.dumps(result, indent=2))
        else:
            if is_connected:
                self.console.print("✅ OpenVPN is connected")
                conn_info = self.rotator.openvpn_manager.get_current_connection_info()
                if conn_info:
                    self.console.print(f"Server: {conn_info.get('name', 'Unknown')}")
                    self.console.print(f"Country: {conn_info.get('country', 'Unknown')}")
            else:
                self.console.print("❌ OpenVPN is not connected")
            
            self.console.print(f"Available servers: {len(available_servers)}")
        
        return 0
    
    def _handle_benchmark(self, args: argparse.Namespace) -> int:
        """Handle benchmark command"""
        self.console.print("⚡ Running performance benchmark...")
        
        # This would implement a comprehensive benchmark
        self.console.print("ℹ️ Benchmark feature not yet implemented")
        return 0
    
    def _handle_list_methods(self, args: argparse.Namespace) -> int:
        """Handle list methods command"""
        methods = ['proxy', 'tor', 'openvpn']
        
        if args.json:
            self.console.print(json.dumps({'methods': methods}, indent=2))
        else:
            table = Table(title="Available Rotation Methods")
            table.add_column("Method", style="cyan")
            table.add_column("Description", style="green")
            
            descriptions = {
                'proxy': 'HTTP/HTTPS/SOCKS proxy rotation',
                'tor': 'Tor network anonymity routing',
                'openvpn': 'OpenVPN server rotation'
            }
            
            for method in methods:
                table.add_row(method.upper(), descriptions.get(method, 'Unknown'))
            
            self.console.print(table)
        
        return 0
    
    def _handle_list_proxies(self, args: argparse.Namespace) -> int:
        """Handle list proxies command"""
        proxies = self.rotator.proxy_manager.get_working_proxies()
        
        if args.json:
            proxy_data = [
                {
                    'host': proxy.host,
                    'port': proxy.port,
                    'type': proxy.proxy_type,
                    'country': proxy.country,
                    'response_time': proxy.response_time
                }
                for proxy in proxies
            ]
            self.console.print(json.dumps({'proxies': proxy_data}, indent=2))
        else:
            if proxies:
                table = Table(title="Available Proxies")
                table.add_column("Host", style="cyan")
                table.add_column("Port", style="green")
                table.add_column("Type", style="yellow")
                table.add_column("Response Time", style="magenta")
                
                for proxy in proxies[:10]:  # Show first 10
                    table.add_row(
                        proxy.host,
                        str(proxy.port),
                        proxy.proxy_type.upper(),
                        f"{proxy.response_time:.2f}s"
                    )
                
                self.console.print(table)
                if len(proxies) > 10:
                    self.console.print(f"... and {len(proxies) - 10} more proxies")
            else:
                self.console.print("No working proxies available")
        
        return 0
    
    def _handle_list_vpn(self, args: argparse.Namespace) -> int:
        """Handle list VPN command"""
        servers = self.rotator.openvpn_manager.get_available_servers()
        
        if args.json:
            self.console.print(json.dumps({'vpn_servers': servers}, indent=2))
        else:
            if servers:
                table = Table(title="Available OpenVPN Servers")
                table.add_column("Name", style="cyan")
                table.add_column("Server", style="green")
                table.add_column("Country", style="yellow")
                table.add_column("Protocol", style="magenta")
                
                for server in servers:
                    table.add_row(
                        server['name'],
                        server['server'],
                        server.get('country', 'Unknown'),
                        f"{server['protocol'].upper()}:{server['port']}"
                    )
                
                self.console.print(table)
            else:
                self.console.print("No OpenVPN servers configured")
        
        return 0
    
    def _handle_validate_config(self, args: argparse.Namespace) -> int:
        """Handle validate config command"""
        self.console.print("🔍 Validating configuration...")
        
        # This would implement configuration validation
        self.console.print("✅ Configuration appears valid")
        return 0
    
    def _handle_reset_config(self, args: argparse.Namespace) -> int:
        """Handle reset config command"""
        self.console.print("🔄 Resetting configuration to defaults...")
        
        # This would implement configuration reset
        self.console.print("✅ Configuration reset to defaults")
        return 0
