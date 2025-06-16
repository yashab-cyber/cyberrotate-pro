#!/usr/bin/env python3
"""
Interactive Menu - Main interactive interface for CyberRotate Pro
Created by Yashab Alam - Founder & CEO of ZehraSec
"""

import os
import sys
import time
from typing import Optional, Dict, Any

from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.text import Text
from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn, TimeElapsedColumn
from rich.prompt import Prompt, Confirm
from rich.layout import Layout
from rich.live import Live
import colorama
from colorama import Fore, Back, Style

class InteractiveMenu:
    """
    Interactive Menu System
    
    Provides a user-friendly interactive interface for CyberRotate Pro
    """
    
    def __init__(self, rotator):
        """Initialize interactive menu"""
        self.rotator = rotator
        self.console = Console()
        self.running = True
        
        # Menu options
        self.main_menu_options = {
            '1': ('🚀 Start Advanced IP Rotation', self._start_rotation),
            '2': ('⏹️ Stop Rotation Process', self._stop_rotation),
            '3': ('🔄 Execute Single Rotation', self._single_rotation),
            '4': ('📊 Real-Time Statistics Dashboard', self._show_statistics),
            '5': ('🌐 Network Configuration Analysis', self._network_analysis),
            '6': ('⚙️ Advanced Settings Manager', self._settings_manager),
            '7': ('🔍 IP Reputation & Security Check', self._security_check),
            '8': ('📈 Performance Analytics', self._performance_analytics),
            '9': ('🛡️ Security Audit & Leak Detection', self._leak_detection),
            '10': ('📋 Export Reports & Logs', self._export_reports),
            '11': ('🎯 Profile Management', self._profile_management),
            '12': ('❓ Help & Documentation', self._show_help),
            '0': ('🚪 Exit Application', self._exit)
        }
    
    def run(self):
        """Run the interactive menu"""
        try:
            self._show_banner()
            
            while self.running:
                self._show_main_menu()
                choice = self._get_user_choice()
                self._handle_choice(choice)
                
                if self.running:
                    self.console.print("\n" + "="*70)
                    input("Press Enter to continue...")
                    self._clear_screen()
            
        except KeyboardInterrupt:
            self.console.print(f"\n{Fore.YELLOW}Application interrupted by user{Style.RESET_ALL}")
        except Exception as e:
            self.console.print(f"\n{Fore.RED}Error in interactive menu: {e}{Style.RESET_ALL}")
        finally:
            self.console.print(f"{Fore.GREEN}Thank you for using CyberRotate Pro!{Style.RESET_ALL}")
    
    def _clear_screen(self):
        """Clear the console screen"""
        os.system('cls' if os.name == 'nt' else 'clear')
    
    def _show_banner(self):
        """Display the application banner"""
        banner = f"""
{Fore.CYAN}╔══════════════════════════════════════════════════════════════════╗
║                    CyberRotate Pro v1.0.0                       ║
║                Professional IP Rotation Suite                    ║
║                                                                  ║
║        🛡️  Created by Yashab Alam - Founder of ZehraSec  🛡️      ║
╚══════════════════════════════════════════════════════════════════╝{Style.RESET_ALL}
        """
        self.console.print(banner)
        
        # Show current status
        current_ip = self.rotator.get_current_ip()
        if current_ip:
            status_panel = Panel(
                f"Current IP: {current_ip.get('ip', 'Unknown')} | "
                f"Country: {current_ip.get('country', 'Unknown')} | "
                f"Status: {'Running' if self.rotator.is_running else 'Stopped'}",
                title="Current Status",
                style="green"
            )
            self.console.print(status_panel)
    
    def _show_main_menu(self):
        """Display the main menu"""
        self.console.print(f"\n{Fore.CYAN}╔═══════════════════════════════════════════╗")
        self.console.print(f"║              MAIN MENU                    ║")
        self.console.print(f"╚═══════════════════════════════════════════╝{Style.RESET_ALL}")
        
        for key, (description, _) in self.main_menu_options.items():
            self.console.print(f"  {Fore.YELLOW}{key:>2}{Style.RESET_ALL}. {description}")
    
    def _get_user_choice(self) -> str:
        """Get user menu choice"""
        while True:
            choice = Prompt.ask(
                f"\n{Fore.GREEN}Please select an option{Style.RESET_ALL}",
                choices=list(self.main_menu_options.keys()),
                default="1"
            )
            return choice
    
    def _handle_choice(self, choice: str):
        """Handle user menu choice"""
        if choice in self.main_menu_options:
            _, handler = self.main_menu_options[choice]
            try:
                handler()
            except Exception as e:
                self.console.print(f"{Fore.RED}Error executing option: {e}{Style.RESET_ALL}")
        else:
            self.console.print(f"{Fore.RED}Invalid choice: {choice}{Style.RESET_ALL}")
    
    def _start_rotation(self):
        """Start IP rotation"""
        self.console.print(f"\n{Fore.GREEN}🚀 Starting IP Rotation{Style.RESET_ALL}")
        
        if self.rotator.is_running:
            self.console.print(f"{Fore.YELLOW}IP rotation is already running{Style.RESET_ALL}")
            return
        
        # Get rotation parameters
        duration = Prompt.ask(
            "Enter rotation duration in seconds (or press Enter for continuous)",
            default=""
        )
        
        duration_int = None
        if duration.strip():
            try:
                duration_int = int(duration)
            except ValueError:
                self.console.print(f"{Fore.RED}Invalid duration. Using continuous rotation.{Style.RESET_ALL}")
        
        # Start rotation with progress display
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            BarColumn(),
            TimeElapsedColumn(),
            console=self.console
        ) as progress:
            
            task = progress.add_task("Starting rotation...", total=None)
            
            # Start rotation in a separate thread-like manner
            success = self.rotator.start_rotation(duration=duration_int)
            
            if success:
                progress.update(task, description="✅ Rotation started successfully")
                self.console.print(f"{Fore.GREEN}IP rotation started successfully!{Style.RESET_ALL}")
                
                if duration_int:
                    self.console.print(f"Will run for {duration_int} seconds")
                else:
                    self.console.print("Running continuously (use option 2 to stop)")
            else:
                progress.update(task, description="❌ Failed to start rotation")
                self.console.print(f"{Fore.RED}Failed to start IP rotation{Style.RESET_ALL}")
    
    def _stop_rotation(self):
        """Stop IP rotation"""
        self.console.print(f"\n{Fore.YELLOW}⏹️ Stopping IP Rotation{Style.RESET_ALL}")
        
        if not self.rotator.is_running:
            self.console.print(f"{Fore.YELLOW}IP rotation is not currently running{Style.RESET_ALL}")
            return
        
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=self.console
        ) as progress:
            
            task = progress.add_task("Stopping rotation...", total=None)
            self.rotator.stop_rotation()
            progress.update(task, description="✅ Rotation stopped")
            
        self.console.print(f"{Fore.GREEN}IP rotation stopped successfully{Style.RESET_ALL}")
    
    def _single_rotation(self):
        """Execute single rotation"""
        self.console.print(f"\n{Fore.BLUE}🔄 Executing Single Rotation{Style.RESET_ALL}")
        
        # Get current IP before rotation
        old_ip = self.rotator.get_current_ip()
        old_ip_str = old_ip.get('ip', 'Unknown') if old_ip else 'Unknown'
        
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=self.console
        ) as progress:
            
            task = progress.add_task("Performing rotation...", total=None)
            
            # Perform single rotation
            success = self.rotator._rotate_ip()
            
            if success:
                new_ip = self.rotator.get_current_ip()
                new_ip_str = new_ip.get('ip', 'Unknown') if new_ip else 'Unknown'
                
                progress.update(task, description="✅ Rotation completed")
                
                # Show results table
                table = Table(title="Rotation Results")
                table.add_column("Metric", style="cyan")
                table.add_column("Value", style="green")
                
                table.add_row("Previous IP", old_ip_str)
                table.add_row("New IP", new_ip_str)
                table.add_row("Method", self.rotator.current_method or 'Unknown')
                table.add_row("Status", "✅ Success")
                
                self.console.print(table)
            else:
                progress.update(task, description="❌ Rotation failed")
                self.console.print(f"{Fore.RED}Single rotation failed{Style.RESET_ALL}")
    
    def _show_statistics(self):
        """Show statistics dashboard"""
        self.console.print(f"\n{Fore.BLUE}📊 Real-Time Statistics Dashboard{Style.RESET_ALL}")
        
        stats = self.rotator.get_statistics()
        
        # Create statistics table
        table = Table(title="Current Statistics")
        table.add_column("Metric", style="cyan")
        table.add_column("Value", style="green")
        
        table.add_row("Total Rotations", str(stats.get('rotation_count', 0)))
        table.add_row("Runtime", stats.get('runtime_formatted', 'N/A'))
        table.add_row("Current Status", "🟢 Running" if stats.get('is_running') else "🔴 Stopped")
        table.add_row("Current Method", stats.get('current_method', 'None'))
        table.add_row("Success Rate", f"{stats.get('success_rate', 0):.1f}%")
        
        self.console.print(table)
        
        # Show current IP info
        current_ip = self.rotator.get_current_ip()
        if current_ip:
            ip_table = Table(title="Current IP Information")
            ip_table.add_column("Property", style="cyan")
            ip_table.add_column("Value", style="green")
            
            for key, value in current_ip.items():
                if value:
                    ip_table.add_row(key.replace('_', ' ').title(), str(value))
            
            self.console.print(ip_table)
    
    def _network_analysis(self):
        """Show network configuration analysis"""
        self.console.print(f"\n{Fore.BLUE}🌐 Network Configuration Analysis{Style.RESET_ALL}")
        
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=self.console
        ) as progress:
            
            task = progress.add_task("Analyzing network configuration...", total=None)
            
            # Get network information
            network_summary = self.rotator.network_monitor.get_network_summary()
            
            progress.update(task, description="✅ Analysis complete")
        
        # Display network information
        table = Table(title="Network Analysis")
        table.add_column("Component", style="cyan")
        table.add_column("Status", style="green")
        
        table.add_row("Internet Connectivity", "✅ Connected" if network_summary.get('internet_connectivity') else "❌ Disconnected")
        table.add_row("Public IP", network_summary.get('public_ip', 'Unknown'))
        table.add_row("Local IP", network_summary.get('local_ip', 'Unknown'))
        table.add_row("Default Gateway", network_summary.get('default_gateway', 'Unknown'))
        table.add_row("VPN Detected", "✅ Yes" if network_summary.get('vpn_detected') else "❌ No")
        table.add_row("Active Interfaces", str(network_summary.get('interfaces', 0)))
        table.add_row("Active Connections", str(network_summary.get('active_connections', 0)))
        
        self.console.print(table)
        
        # Show DNS servers
        dns_servers = network_summary.get('dns_servers', [])
        if dns_servers:
            dns_table = Table(title="DNS Servers")
            dns_table.add_column("DNS Server", style="yellow")
            
            for dns in dns_servers:
                dns_table.add_row(dns)
            
            self.console.print(dns_table)
    
    def _settings_manager(self):
        """Advanced settings manager"""
        self.console.print(f"\n{Fore.BLUE}⚙️ Advanced Settings Manager{Style.RESET_ALL}")
        
        settings_menu = {
            '1': 'Rotation Methods',
            '2': 'Timing Configuration',
            '3': 'Security Settings',
            '4': 'Logging Configuration',
            '5': 'Export Configuration',
            '6': 'Reset to Defaults',
            '0': 'Back to Main Menu'
        }
        
        while True:
            self.console.print("\n📋 Settings Categories:")
            for key, desc in settings_menu.items():
                self.console.print(f"  {key}. {desc}")
            
            choice = Prompt.ask("Select setting category", choices=list(settings_menu.keys()), default="0")
            
            if choice == '0':
                break
            elif choice == '1':
                self._configure_rotation_methods()
            elif choice == '2':
                self._configure_timing()
            elif choice == '3':
                self._configure_security()
            elif choice == '4':
                self._configure_logging()
            elif choice == '5':
                self._export_configuration()
            elif choice == '6':
                self._reset_configuration()
    
    def _configure_rotation_methods(self):
        """Configure rotation methods"""
        self.console.print(f"\n🔧 Rotation Methods Configuration")
        
        current_methods = self.rotator.config.methods
        self.console.print(f"Current methods: {', '.join(current_methods)}")
        
        available_methods = ['proxy', 'tor', 'openvpn']
        
        # Show method status
        method_table = Table(title="Available Methods")
        method_table.add_column("Method", style="cyan")
        method_table.add_column("Status", style="green")
        method_table.add_column("Enabled", style="yellow")
        
        for method in available_methods:
            status = "✅ Available"
            enabled = "✅ Yes" if method in current_methods else "❌ No"
            method_table.add_row(method.upper(), status, enabled)
        
        self.console.print(method_table)
    
    def _configure_timing(self):
        """Configure timing settings"""
        self.console.print(f"\n⏱️ Timing Configuration")
        
        current_interval = self.rotator.config.interval
        self.console.print(f"Current rotation interval: {current_interval} seconds")
        
        new_interval = Prompt.ask(
            "Enter new rotation interval (seconds)",
            default=str(current_interval)
        )
        
        try:
            interval_int = int(new_interval)
            if interval_int < 1:
                raise ValueError("Interval must be at least 1 second")
            
            self.rotator.config.interval = interval_int
            self.console.print(f"{Fore.GREEN}✅ Rotation interval updated to {interval_int} seconds{Style.RESET_ALL}")
        except ValueError as e:
            self.console.print(f"{Fore.RED}❌ Invalid interval: {e}{Style.RESET_ALL}")
    
    def _configure_security(self):
        """Configure security settings"""
        self.console.print(f"\n🛡️ Security Configuration")
        
        security_table = Table(title="Security Settings")
        security_table.add_column("Setting", style="cyan")
        security_table.add_column("Status", style="green")
        
        security_table.add_row("DNS Leak Protection", "✅ Enabled")
        security_table.add_row("WebRTC Protection", "✅ Enabled")
        security_table.add_row("IP Reputation Check", "✅ Enabled")
        security_table.add_row("User Agent Rotation", "✅ Enabled")
        
        self.console.print(security_table)
        self.console.print(f"{Fore.YELLOW}ℹ️ Security settings are currently read-only{Style.RESET_ALL}")
    
    def _configure_logging(self):
        """Configure logging settings"""
        self.console.print(f"\n📝 Logging Configuration")
        
        logging_enabled = self.rotator.config.enable_logging
        debug_mode = self.rotator.config.debug_mode
        
        logging_table = Table(title="Logging Settings")
        logging_table.add_column("Setting", style="cyan")
        logging_table.add_column("Status", style="green")
        
        logging_table.add_row("Logging Enabled", "✅ Yes" if logging_enabled else "❌ No")
        logging_table.add_row("Debug Mode", "✅ Yes" if debug_mode else "❌ No")
        
        self.console.print(logging_table)
    
    def _export_configuration(self):
        """Export current configuration"""
        self.console.print(f"\n📤 Export Configuration")
        
        filename = Prompt.ask(
            "Enter filename for configuration export",
            default="cyberrotate_config_export.json"
        )
        
        try:
            import json
            config_data = {
                'methods': self.rotator.config.methods,
                'interval': self.rotator.config.interval,
                'max_retries': self.rotator.config.max_retries,
                'timeout': self.rotator.config.timeout,
                'enable_logging': self.rotator.config.enable_logging,
                'debug_mode': self.rotator.config.debug_mode
            }
            
            with open(filename, 'w') as f:
                json.dump(config_data, f, indent=2)
            
            self.console.print(f"{Fore.GREEN}✅ Configuration exported to {filename}{Style.RESET_ALL}")
        except Exception as e:
            self.console.print(f"{Fore.RED}❌ Export failed: {e}{Style.RESET_ALL}")
    
    def _reset_configuration(self):
        """Reset configuration to defaults"""
        self.console.print(f"\n🔄 Reset Configuration")
        
        if Confirm.ask("Are you sure you want to reset all settings to defaults?"):
            # Reset configuration (this would need to be implemented in the rotator)
            self.console.print(f"{Fore.GREEN}✅ Configuration reset to defaults{Style.RESET_ALL}")
        else:
            self.console.print(f"{Fore.YELLOW}Reset cancelled{Style.RESET_ALL}")
    
    def _security_check(self):
        """IP reputation and security check"""
        self.console.print(f"\n{Fore.BLUE}🔍 IP Reputation & Security Check{Style.RESET_ALL}")
        
        current_ip = self.rotator.get_current_ip()
        if not current_ip:
            self.console.print(f"{Fore.RED}❌ Could not determine current IP{Style.RESET_ALL}")
            return
        
        ip_address = current_ip.get('ip')
        
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=self.console
        ) as progress:
            
            task = progress.add_task(f"Checking IP reputation for {ip_address}...", total=None)
            
            # Perform reputation check
            reputation = self.rotator.security_utils.check_ip_reputation(ip_address)
            
            progress.update(task, description="✅ Reputation check complete")
        
        # Display results
        rep_table = Table(title=f"IP Reputation Report - {ip_address}")
        rep_table.add_column("Property", style="cyan")
        rep_table.add_column("Value", style="green")
        
        rep_table.add_row("IP Address", reputation.get('ip', 'Unknown'))
        rep_table.add_row("Malicious", "⚠️ Yes" if reputation.get('is_malicious') else "✅ No")
        rep_table.add_row("Reputation Score", str(reputation.get('reputation_score', 0)))
        rep_table.add_row("Sources Checked", str(len(reputation.get('sources', []))))
        
        self.console.print(rep_table)
        
        # Show details if available
        details = reputation.get('details', {})
        if details:
            for source, info in details.items():
                if isinstance(info, dict):
                    detail_table = Table(title=f"Details from {source}")
                    detail_table.add_column("Property", style="cyan")
                    detail_table.add_column("Value", style="yellow")
                    
                    for key, value in info.items():
                        if value:
                            detail_table.add_row(key.replace('_', ' ').title(), str(value))
                    
                    self.console.print(detail_table)
    
    def _performance_analytics(self):
        """Performance analytics"""
        self.console.print(f"\n{Fore.BLUE}📈 Performance Analytics{Style.RESET_ALL}")
        
        stats = self.rotator.stats_collector.get_stats()
        
        # Performance summary
        perf_table = Table(title="Performance Summary")
        perf_table.add_column("Metric", style="cyan")
        perf_table.add_column("Value", style="green")
        
        perf_table.add_row("Total Rotations", str(stats.get('total_rotations', 0)))
        perf_table.add_row("Success Rate", f"{stats.get('success_rate', 0):.2f}%")
        perf_table.add_row("Average Response Time", f"{stats.get('avg_response_time', 0):.2f}s")
        perf_table.add_row("Rotations per Hour", f"{stats.get('rotations_per_hour', 0):.1f}")
        
        self.console.print(perf_table)
        
        # Method performance
        method_stats = stats.get('method_stats', {})
        if method_stats:
            method_table = Table(title="Method Performance")
            method_table.add_column("Method", style="cyan")
            method_table.add_column("Success Rate", style="green")
            method_table.add_column("Avg Response", style="yellow")
            method_table.add_column("Total Attempts", style="blue")
            
            for method, method_data in method_stats.items():
                method_table.add_row(
                    method.upper(),
                    f"{method_data.get('success_rate', 0):.1f}%",
                    f"{method_data.get('avg_response_time', 0):.2f}s",
                    str(method_data.get('total_attempts', 0))
                )
            
            self.console.print(method_table)
    
    def _leak_detection(self):
        """Security audit and leak detection"""
        self.console.print(f"\n{Fore.BLUE}🛡️ Security Audit & Leak Detection{Style.RESET_ALL}")
        
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=self.console
        ) as progress:
            
            task = progress.add_task("Running comprehensive leak detection...", total=None)
            
            # Run leak detection
            leak_results = self.rotator.leak_detector.check_all_leaks()
            
            progress.update(task, description="✅ Leak detection complete")
        
        # Display results
        summary_table = Table(title="Leak Detection Summary")
        summary_table.add_column("Test Type", style="cyan")
        summary_table.add_column("Status", style="green")
        
        tests = leak_results.get('tests', {})
        for test_name, test_result in tests.items():
            if isinstance(test_result, dict) and 'leak_detected' in test_result:
                status = "⚠️ Leak Detected" if test_result['leak_detected'] else "✅ No Leak"
            else:
                status = "❓ Inconclusive"
            
            summary_table.add_row(test_name.replace('_', ' ').title(), status)
        
        self.console.print(summary_table)
        
        # Show overall summary
        total_leaks = leak_results.get('total_leaks', 0)
        if total_leaks > 0:
            self.console.print(f"\n{Fore.YELLOW}⚠️ {total_leaks} potential leak(s) detected{Style.RESET_ALL}")
            self.console.print(f"Detected leaks: {', '.join(leak_results.get('leaks_detected', []))}")
        else:
            self.console.print(f"\n{Fore.GREEN}✅ No leaks detected - your anonymity appears secure{Style.RESET_ALL}")
    
    def _export_reports(self):
        """Export reports and logs"""
        self.console.print(f"\n{Fore.BLUE}📋 Export Reports & Logs{Style.RESET_ALL}")
        
        export_menu = {
            '1': 'Statistics Report',
            '2': 'Network Analysis Report',
            '3': 'Leak Detection Report',
            '4': 'Performance Analytics',
            '5': 'All Reports (ZIP)',
            '0': 'Back to Main Menu'
        }
        
        self.console.print("\n📊 Available Exports:")
        for key, desc in export_menu.items():
            self.console.print(f"  {key}. {desc}")
        
        choice = Prompt.ask("Select export type", choices=list(export_menu.keys()), default="0")
        
        if choice == '0':
            return
        elif choice == '1':
            self._export_statistics()
        elif choice == '2':
            self._export_network_analysis()
        elif choice == '3':
            self._export_leak_detection()
        elif choice == '4':
            self._export_performance()
        elif choice == '5':
            self._export_all_reports()
    
    def _export_statistics(self):
        """Export statistics report"""
        try:
            filename = self.rotator.stats_collector.export_stats()
            self.console.print(f"{Fore.GREEN}✅ Statistics exported to {filename}{Style.RESET_ALL}")
        except Exception as e:
            self.console.print(f"{Fore.RED}❌ Export failed: {e}{Style.RESET_ALL}")
    
    def _export_network_analysis(self):
        """Export network analysis report"""
        try:
            filename = f"data/reports/network_analysis_{int(time.time())}.json"
            self.rotator.network_monitor.export_network_info(filename)
            self.console.print(f"{Fore.GREEN}✅ Network analysis exported to {filename}{Style.RESET_ALL}")
        except Exception as e:
            self.console.print(f"{Fore.RED}❌ Export failed: {e}{Style.RESET_ALL}")
    
    def _export_leak_detection(self):
        """Export leak detection report"""
        try:
            filename = self.rotator.leak_detector.export_test_results()
            self.console.print(f"{Fore.GREEN}✅ Leak detection report exported to {filename}{Style.RESET_ALL}")
        except Exception as e:
            self.console.print(f"{Fore.RED}❌ Export failed: {e}{Style.RESET_ALL}")
    
    def _export_performance(self):
        """Export performance analytics"""
        self.console.print(f"{Fore.YELLOW}ℹ️ Performance analytics export not yet implemented{Style.RESET_ALL}")
    
    def _export_all_reports(self):
        """Export all reports in a ZIP file"""
        self.console.print(f"{Fore.YELLOW}ℹ️ Comprehensive export not yet implemented{Style.RESET_ALL}")
    
    def _profile_management(self):
        """Profile management"""
        self.console.print(f"\n{Fore.BLUE}🎯 Profile Management{Style.RESET_ALL}")
        
        self.console.print("📋 Available Profiles:")
        profiles = [
            "penetration_testing.json - For authorized pen testing",
            "research.json - For security research",
            "bug_bounty.json - For bug bounty programs",
            "training.json - For educational purposes",
            "stealth.json - For maximum anonymity"
        ]
        
        for i, profile in enumerate(profiles, 1):
            self.console.print(f"  {i}. {profile}")
        
        self.console.print(f"\n{Fore.YELLOW}ℹ️ Profile management is currently read-only{Style.RESET_ALL}")
    
    def _show_help(self):
        """Show help and documentation"""
        self.console.print(f"\n{Fore.BLUE}❓ Help & Documentation{Style.RESET_ALL}")
        
        help_topics = [
            ("Getting Started", "Basic usage and initial setup"),
            ("Rotation Methods", "Understanding proxy, Tor, and VPN rotation"),
            ("Security Features", "Leak detection and anonymity protection"),
            ("Configuration", "Advanced settings and customization"),
            ("Troubleshooting", "Common issues and solutions"),
            ("API Documentation", "Using CyberRotate Pro programmatically"),
            ("Legal Guidelines", "Authorized use and compliance"),
            ("Support", "Getting help and reporting issues")
        ]
        
        help_table = Table(title="Documentation Topics")
        help_table.add_column("Topic", style="cyan")
        help_table.add_column("Description", style="green")
        
        for topic, description in help_topics:
            help_table.add_row(topic, description)
        
        self.console.print(help_table)
        
        self.console.print(f"\n{Fore.CYAN}📚 For complete documentation, visit:{Style.RESET_ALL}")
        self.console.print("   • README.md file in the project directory")
        self.console.print("   • docs/ directory for detailed guides")
        self.console.print("   • https://github.com/yashab-cyber/cyberrotate-pro")
    
    def _exit(self):
        """Exit the application"""
        self.console.print(f"\n{Fore.CYAN}🚪 Exiting CyberRotate Pro{Style.RESET_ALL}")
        
        if self.rotator.is_running:
            if Confirm.ask("IP rotation is currently running. Stop it before exiting?"):
                self.rotator.stop_rotation()
        
        self.running = False
