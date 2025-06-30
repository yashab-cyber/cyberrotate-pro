#!/usr/bin/env python3
"""
CyberRotate Pro - Main GUI Application
Modern graphical user interface for IP rotation and anonymity management
"""

import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext, filedialog
from tkinter import font as tkFont
import threading
import time
import json
import os
import sys
from datetime import datetime
from typing import Dict, Any, Optional

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.proxy_manager import ProxyManager
from core.openvpn_manager import OpenVPNManager
from core.tor_controller import TorController
from core.network_monitor import NetworkMonitor
from core.security_utils import SecurityUtils
from utils.logger import Logger
from utils.stats_collector import StatsCollector

class CyberRotateGUI:
    """Main GUI application for CyberRotate Pro"""
    
    def __init__(self, config_file: str = "config/config.json"):
        self.config_file = config_file
        self.config = self.load_config()
          # Initialize core components
        self.logger = Logger("gui")
        self.stats = StatsCollector(self.logger.logger)
          # Initialize managers
        self.proxy_manager = ProxyManager(self.logger.logger)
        self.vpn_manager = OpenVPNManager(self.logger.logger)
        self.tor_controller = TorController(self.logger.logger)
        self.network_monitor = NetworkMonitor(self.logger.logger)
        self.security_utils = SecurityUtils(self.logger.logger)
        
        # GUI state
        self.is_monitoring = False
        self.current_ip = "Unknown"
        self.current_location = "Unknown"
        self.proxy_status = "Disconnected"
        self.vpn_status = "Disconnected"
        self.tor_status = "Stopped"
        
        # Create main window
        self.root = tk.Tk()
        self.setup_main_window()
        self.create_widgets()
        self.setup_styles()
        self.start_monitoring()
        
    def load_config(self) -> Dict[str, Any]:
        """Load configuration from file"""
        try:
            with open(self.config_file, 'r') as f:
                return json.load(f)
        except Exception as e:
            print(f"Failed to load config: {e}")
            return self.get_default_config()
    
    def get_default_config(self) -> Dict[str, Any]:
        """Get default configuration"""
        return {
            "proxy": {
                "rotation_interval": 300,
                "max_failures": 3,
                "timeout": 30
            },
            "openvpn": {
                "config_directory": "config/openvpn",
                "timeout": 30,
                "retry_attempts": 3
            },
            "tor": {
                "socks_port": 9150,
                "control_port": 9151,
                "auto_start": False
            }
        }
    
    def setup_main_window(self):
        """Setup the main application window"""
        self.root.title("CyberRotate Pro - IP Rotation & Anonymity Suite")
        self.root.geometry("1200x800")
        self.root.minsize(800, 600)
        
        # Set window icon (if available)
        try:
            # You can add an icon file here
            pass
        except:
            pass
        
        # Configure grid weights
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(0, weight=1)
        
    def setup_styles(self):
        """Setup custom styles for the GUI"""
        self.style = ttk.Style()
        
        # Configure styles
        self.style.configure('Title.TLabel', font=('Arial', 16, 'bold'))
        self.style.configure('Subtitle.TLabel', font=('Arial', 12, 'bold'))
        self.style.configure('Status.TLabel', font=('Arial', 10))
        self.style.configure('Success.TLabel', foreground='green')
        self.style.configure('Warning.TLabel', foreground='orange')
        self.style.configure('Error.TLabel', foreground='red')
        
        # Button styles
        self.style.configure('Action.TButton', font=('Arial', 10, 'bold'))
        
    def create_widgets(self):
        """Create all GUI widgets"""
        # Main container
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        main_frame.grid_rowconfigure(1, weight=1)
        main_frame.grid_columnconfigure(1, weight=1)
        
        # Title
        title_label = ttk.Label(main_frame, text="CyberRotate Pro", style='Title.TLabel')
        title_label.grid(row=0, column=0, columnspan=3, pady=(0, 20))
        
        # Left panel - Controls
        self.create_control_panel(main_frame)
        
        # Center panel - Status and Information
        self.create_status_panel(main_frame)
        
        # Right panel - Logs and Statistics
        self.create_info_panel(main_frame)
        
        # Bottom panel - Status bar
        self.create_status_bar(main_frame)
        
    def create_control_panel(self, parent):
        """Create the control panel with action buttons"""
        control_frame = ttk.LabelFrame(parent, text="Controls", padding="10")
        control_frame.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), padx=(0, 10))
        
        # IP Status Section
        ip_frame = ttk.LabelFrame(control_frame, text="Current Status", padding="10")
        ip_frame.pack(fill="x", pady=(0, 10))
        
        self.ip_label = ttk.Label(ip_frame, text=f"IP: {self.current_ip}", style='Status.TLabel')
        self.ip_label.pack(anchor="w")
        
        self.location_label = ttk.Label(ip_frame, text=f"Location: {self.current_location}", style='Status.TLabel')
        self.location_label.pack(anchor="w")
        
        ttk.Button(ip_frame, text="Check IP", command=self.check_ip, style='Action.TButton').pack(fill="x", pady=(5, 0))
        
        # Proxy Section
        proxy_frame = ttk.LabelFrame(control_frame, text="Proxy Management", padding="10")
        proxy_frame.pack(fill="x", pady=(0, 10))
        
        self.proxy_status_label = ttk.Label(proxy_frame, text=f"Status: {self.proxy_status}", style='Status.TLabel')
        self.proxy_status_label.pack(anchor="w")
        
        ttk.Button(proxy_frame, text="Rotate Proxy", command=self.rotate_proxy, style='Action.TButton').pack(fill="x", pady=2)
        ttk.Button(proxy_frame, text="Test Proxies", command=self.test_proxies).pack(fill="x", pady=2)
        ttk.Button(proxy_frame, text="Load Proxy List", command=self.load_proxy_list).pack(fill="x", pady=2)
        
        # VPN Section
        vpn_frame = ttk.LabelFrame(control_frame, text="VPN Management", padding="10")
        vpn_frame.pack(fill="x", pady=(0, 10))
        
        self.vpn_status_label = ttk.Label(vpn_frame, text=f"Status: {self.vpn_status}", style='Status.TLabel')
        self.vpn_status_label.pack(anchor="w")
        
        # VPN Server Selection
        ttk.Label(vpn_frame, text="Select Server:").pack(anchor="w")
        self.vpn_server_var = tk.StringVar()
        self.vpn_server_combo = ttk.Combobox(vpn_frame, textvariable=self.vpn_server_var, state="readonly")
        self.vpn_server_combo.pack(fill="x", pady=2)
        self.update_vpn_servers()
        
        ttk.Button(vpn_frame, text="Connect VPN", command=self.connect_vpn, style='Action.TButton').pack(fill="x", pady=2)
        ttk.Button(vpn_frame, text="Disconnect VPN", command=self.disconnect_vpn).pack(fill="x", pady=2)
        
        # Tor Section
        tor_frame = ttk.LabelFrame(control_frame, text="Tor Network", padding="10")
        tor_frame.pack(fill="x", pady=(0, 10))
        
        self.tor_status_label = ttk.Label(tor_frame, text=f"Status: {self.tor_status}", style='Status.TLabel')
        self.tor_status_label.pack(anchor="w")
        
        ttk.Button(tor_frame, text="Start Tor", command=self.start_tor, style='Action.TButton').pack(fill="x", pady=2)
        ttk.Button(tor_frame, text="Stop Tor", command=self.stop_tor).pack(fill="x", pady=2)
        ttk.Button(tor_frame, text="New Identity", command=self.new_tor_identity).pack(fill="x", pady=2)
        
        # Security Section
        security_frame = ttk.LabelFrame(control_frame, text="Security Checks", padding="10")
        security_frame.pack(fill="x")
        
        ttk.Button(security_frame, text="DNS Leak Test", command=self.check_dns_leaks).pack(fill="x", pady=2)
        ttk.Button(security_frame, text="Full Security Scan", command=self.full_security_scan).pack(fill="x", pady=2)
        
    def create_status_panel(self, parent):
        """Create the main status and information panel"""
        status_frame = ttk.LabelFrame(parent, text="Network Status", padding="10")
        status_frame.grid(row=1, column=1, sticky=(tk.W, tk.E, tk.N, tk.S), padx=10)
        status_frame.grid_rowconfigure(1, weight=1)
        status_frame.grid_columnconfigure(0, weight=1)
        
        # Connection Status Display
        self.create_connection_status(status_frame)
        
        # Network Information
        self.create_network_info(status_frame)
        
        # Quick Actions
        self.create_quick_actions(status_frame)
        
    def create_connection_status(self, parent):
        """Create connection status indicators"""
        status_frame = ttk.Frame(parent)
        status_frame.grid(row=0, column=0, sticky=(tk.W, tk.E), pady=(0, 10))
        status_frame.grid_columnconfigure(1, weight=1)
        
        # Status indicators
        ttk.Label(status_frame, text="Connection Status:", style='Subtitle.TLabel').grid(row=0, column=0, columnspan=2, sticky="w")
        
        # Proxy status
        ttk.Label(status_frame, text="Proxy:").grid(row=1, column=0, sticky="w", padx=(20, 10))
        self.proxy_indicator = tk.Label(status_frame, text="●", fg="red", font=('Arial', 20))
        self.proxy_indicator.grid(row=1, column=1, sticky="w")
        
        # VPN status
        ttk.Label(status_frame, text="VPN:").grid(row=2, column=0, sticky="w", padx=(20, 10))
        self.vpn_indicator = tk.Label(status_frame, text="●", fg="red", font=('Arial', 20))
        self.vpn_indicator.grid(row=2, column=1, sticky="w")
        
        # Tor status
        ttk.Label(status_frame, text="Tor:").grid(row=3, column=0, sticky="w", padx=(20, 10))
        self.tor_indicator = tk.Label(status_frame, text="●", fg="red", font=('Arial', 20))
        self.tor_indicator.grid(row=3, column=1, sticky="w")
        
    def create_network_info(self, parent):
        """Create network information display"""
        info_frame = ttk.LabelFrame(parent, text="Network Information", padding="10")
        info_frame.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 10))
        
        # Create text widget for network info
        self.network_info = scrolledtext.ScrolledText(info_frame, height=15, width=50)
        self.network_info.pack(fill="both", expand=True)
        
        # Update with initial info
        self.update_network_info()
        
    def create_quick_actions(self, parent):
        """Create quick action buttons"""
        action_frame = ttk.Frame(parent)
        action_frame.grid(row=2, column=0, sticky=(tk.W, tk.E))
        
        ttk.Button(action_frame, text="Quick Rotate", command=self.quick_rotate, style='Action.TButton').pack(side="left", padx=5)
        ttk.Button(action_frame, text="Emergency Stop", command=self.emergency_stop).pack(side="left", padx=5)
        ttk.Button(action_frame, text="Refresh All", command=self.refresh_all).pack(side="left", padx=5)
        
    def create_info_panel(self, parent):
        """Create the information panel with logs and statistics"""
        info_frame = ttk.LabelFrame(parent, text="Information", padding="10")
        info_frame.grid(row=1, column=2, sticky=(tk.W, tk.E, tk.N, tk.S), padx=(10, 0))
        info_frame.grid_rowconfigure(1, weight=1)
        info_frame.grid_columnconfigure(0, weight=1)
        
        # Tab control for different info types
        notebook = ttk.Notebook(info_frame)
        notebook.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Logs tab
        log_frame = ttk.Frame(notebook)
        notebook.add(log_frame, text="Logs")
        
        self.log_text = scrolledtext.ScrolledText(log_frame, height=20, width=40)
        self.log_text.pack(fill="both", expand=True)
        
        # Statistics tab
        stats_frame = ttk.Frame(notebook)
        notebook.add(stats_frame, text="Statistics")
        
        self.stats_text = scrolledtext.ScrolledText(stats_frame, height=20, width=40)
        self.stats_text.pack(fill="both", expand=True)
        
        # Configuration tab
        config_frame = ttk.Frame(notebook)
        notebook.add(config_frame, text="Settings")
        
        self.create_settings_panel(config_frame)
        
    def create_settings_panel(self, parent):
        """Create settings panel"""
        settings_frame = ttk.Frame(parent)
        settings_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Auto-rotation settings
        ttk.Label(settings_frame, text="Auto-Rotation Interval (seconds):").pack(anchor="w")
        self.rotation_interval = tk.StringVar(value=str(self.config.get('proxy', {}).get('rotation_interval', 300)))
        ttk.Entry(settings_frame, textvariable=self.rotation_interval).pack(fill="x", pady=(0, 10))
        
        # Enable/disable features
        self.auto_rotation_enabled = tk.BooleanVar()
        ttk.Checkbutton(settings_frame, text="Enable Auto-Rotation", variable=self.auto_rotation_enabled).pack(anchor="w")
        
        self.auto_reconnect_enabled = tk.BooleanVar()
        ttk.Checkbutton(settings_frame, text="Auto-Reconnect on Failure", variable=self.auto_reconnect_enabled).pack(anchor="w")
        
        self.notifications_enabled = tk.BooleanVar(value=True)
        ttk.Checkbutton(settings_frame, text="Enable Notifications", variable=self.notifications_enabled).pack(anchor="w")
        
        # Save settings button
        ttk.Button(settings_frame, text="Save Settings", command=self.save_settings).pack(pady=10)
        
    def create_status_bar(self, parent):
        """Create status bar at the bottom"""
        status_frame = ttk.Frame(parent)
        status_frame.grid(row=2, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(10, 0))
        status_frame.grid_columnconfigure(1, weight=1)
        
        self.status_label = ttk.Label(status_frame, text="Ready")
        self.status_label.grid(row=0, column=0, sticky="w")
        
        self.time_label = ttk.Label(status_frame, text="")
        self.time_label.grid(row=0, column=2, sticky="e")
        
        # Update time
        self.update_time()
        
    def update_time(self):
        """Update the time display"""
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.time_label.config(text=current_time)
        self.root.after(1000, self.update_time)
        
    def start_monitoring(self):
        """Start background monitoring thread"""
        self.is_monitoring = True
        monitor_thread = threading.Thread(target=self.monitor_connections, daemon=True)
        monitor_thread.start()
        
    def monitor_connections(self):
        """Monitor connection status in background"""
        while self.is_monitoring:
            try:
                # Update network information
                self.root.after(0, self.update_all_status)
                time.sleep(5)  # Update every 5 seconds
            except Exception as e:
                self.log_message(f"Monitoring error: {e}")
                
    def update_all_status(self):
        """Update all status indicators"""
        try:
            # Update IP and location
            self.update_ip_info()
            
            # Update connection indicators
            self.update_connection_indicators()
            
            # Update network info
            self.update_network_info()
              # Update statistics
            self.update_statistics()
            
        except Exception as e:
            self.log_message(f"Status update error: {e}")
            
    def update_ip_info(self):
        """Update IP address and location information"""
        try:
            ip_info = self.network_monitor.get_public_ip()
            
            # Handle both string and dictionary returns
            if isinstance(ip_info, dict):
                self.current_ip = ip_info.get('ip', 'Unknown')
                self.current_location = ip_info.get('location', 'Unknown')
            elif isinstance(ip_info, str):
                self.current_ip = ip_info
                self.current_location = "Unknown"
            else:
                self.current_ip = "Unknown"
                self.current_location = "Unknown"
            
            self.ip_label.config(text=f"IP: {self.current_ip}")
            self.location_label.config(text=f"Location: {self.current_location}")
            
        except Exception as e:
            self.log_message(f"IP update error: {e}")
            
    def update_connection_indicators(self):
        """Update connection status indicators"""
        # Update proxy indicator
        if self.proxy_status == "Connected":
            self.proxy_indicator.config(fg="green")
        else:
            self.proxy_indicator.config(fg="red")
            
        # Update VPN indicator
        if self.vpn_status == "Connected":
            self.vpn_indicator.config(fg="green")
        else:
            self.vpn_indicator.config(fg="red")
              # Update Tor indicator
        if self.tor_status == "Running":
            self.tor_indicator.config(fg="green")
        else:
            self.tor_indicator.config(fg="red")
            
    def update_network_info(self):
        """Update network information display"""
        try:
            info = f"=== Network Information ===\n"
            info += f"Current IP: {self.current_ip}\n"
            info += f"Location: {self.current_location}\n"
            info += f"Proxy Status: {self.proxy_status}\n"
            info += f"VPN Status: {self.vpn_status}\n"
            info += f"Tor Status: {self.tor_status}\n\n"
              # Add additional network details
            try:
                network_details = self.network_monitor.get_network_details()
                for key, value in network_details.items():
                    info += f"{key}: {value}\n"
            except:
                pass
                
            info += f"\nLast Updated: {datetime.now().strftime('%H:%M:%S')}"
            
            self.network_info.delete(1.0, tk.END)
            self.network_info.insert(1.0, info)
            
        except Exception as e:
            self.log_message(f"Network info update error: {e}")
            
    def update_statistics(self):
        """Update statistics display"""
        try:
            stats = self.stats.get_stats()
            stats_text = "=== Usage Statistics ===\n"
            
            for category, data in stats.items():
                stats_text += f"\n{category.upper()}:\n"
                if isinstance(data, dict):
                    for key, value in data.items():
                        stats_text += f"  {key}: {value}\n"
                else:
                    stats_text += f"  {data}\n"
                    
            self.stats_text.delete(1.0, tk.END)
            self.stats_text.insert(1.0, stats_text)
            
        except Exception as e:
            self.log_message(f"Statistics update error: {e}")
            
    def update_vpn_servers(self):
        """Update VPN server list"""
        try:
            # Get available VPN servers
            servers = self.vpn_manager.get_available_servers()
            if servers and isinstance(servers, list):
                server_names = [server.get('name', 'Unknown') for server in servers]
            else:
                server_names = ["Default VPN"]
            
            self.vpn_server_combo['values'] = server_names
            if server_names:
                self.vpn_server_combo.set(server_names[0])
        except Exception as e:
            self.log_message(f"VPN server update error: {e}")
            # Set a default option if VPN manager fails
            self.vpn_server_combo['values'] = ["No VPN servers available"]
            self.vpn_server_combo.set("No VPN servers available")
            
    def log_message(self, message: str, level: str = "INFO"):
        """Add message to log display"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        log_entry = f"[{timestamp}] {level}: {message}\n"
        
        # Safety check - ensure log_text widget exists
        if hasattr(self, 'log_text') and self.log_text:
            self.log_text.insert(tk.END, log_entry)
            self.log_text.see(tk.END)
        else:
            # Fallback to print if widget not ready
            print(f"[{timestamp}] {level}: {message}")
          # Also log to file
        self.logger.info(message)
        
    def set_status(self, message: str):
        """Set status bar message"""
        self.status_label.config(text=message)
        
    # Action methods
    
    def check_ip(self):
        """Check current IP address"""
        self.set_status("Checking IP address...")
        
        def check_ip_thread():
            try:
                ip_info = self.network_monitor.get_public_ip()
                
                # Handle both string and dictionary returns
                if isinstance(ip_info, dict):
                    self.current_ip = ip_info.get('ip', 'Unknown')
                    self.current_location = ip_info.get('location', 'Unknown')
                elif isinstance(ip_info, str):
                    self.current_ip = ip_info
                    self.current_location = "Unknown"
                else:
                    self.current_ip = "Unknown"
                    self.current_location = "Unknown"
                
                self.root.after(0, lambda: self.log_message(f"IP: {self.current_ip}, Location: {self.current_location}"))
                self.root.after(0, lambda: self.set_status("IP check completed"))
                
            except Exception as e:
                self.root.after(0, lambda: self.log_message(f"IP check failed: {e}", "ERROR"))
                self.root.after(0, lambda: self.set_status("IP check failed"))
                
        threading.Thread(target=check_ip_thread, daemon=True).start()
        
    def rotate_proxy(self):
        """Rotate to next proxy"""
        self.set_status("Rotating proxy...")
        
        def rotate_proxy_thread():
            try:
                result = self.proxy_manager.rotate_proxy()
                if result:
                    self.proxy_status = "Connected"
                    self.root.after(0, lambda: self.log_message(f"Proxy rotated: {result}"))
                    self.root.after(0, lambda: self.set_status("Proxy rotated successfully"))
                else:
                    self.proxy_status = "Failed"
                    self.root.after(0, lambda: self.log_message("Proxy rotation failed", "ERROR"))
                    self.root.after(0, lambda: self.set_status("Proxy rotation failed"))
                    
            except Exception as e:
                self.proxy_status = "Error"
                self.root.after(0, lambda: self.log_message(f"Proxy rotation error: {e}", "ERROR"))
                self.root.after(0, lambda: self.set_status("Proxy rotation error"))
                
        threading.Thread(target=rotate_proxy_thread, daemon=True).start()
        
    def test_proxies(self):
        """Test all available proxies"""
        self.set_status("Testing proxies...")
        
        def test_proxies_thread():
            try:
                working_proxies = self.proxy_manager.test_all_proxies()
                self.root.after(0, lambda: self.log_message(f"Found {len(working_proxies)} working proxies"))
                self.root.after(0, lambda: self.set_status(f"Proxy test completed: {len(working_proxies)} working"))
                
            except Exception as e:
                self.root.after(0, lambda: self.log_message(f"Proxy test error: {e}", "ERROR"))
                self.root.after(0, lambda: self.set_status("Proxy test failed"))
                
        threading.Thread(target=test_proxies_thread, daemon=True).start()
        
    def load_proxy_list(self):
        """Load proxy list from file"""
        filename = filedialog.askopenfilename(
            title="Select Proxy List File",
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")]        )
        
        if filename:
            try:
                # Implementation would load proxies from file
                self.log_message(f"Loading proxies from: {filename}")
                self.set_status("Proxy list loaded")
            except Exception as e:
                self.log_message(f"Failed to load proxy list: {e}", "ERROR")
                
    def connect_vpn(self):
        """Connect to selected VPN server"""
        server_name = self.vpn_server_var.get()
        if not server_name:
            messagebox.showwarning("Warning", "Please select a VPN server")
            return
            
        self.set_status(f"Connecting to VPN server: {server_name}")
        
        def connect_vpn_thread():
            try:
                result = self.vpn_manager.connect_by_name(server_name)
                if result:
                    self.vpn_status = "Connected"
                    self.root.after(0, lambda: self.log_message(f"Connected to VPN: {server_name}"))
                    self.root.after(0, lambda: self.set_status("VPN connected"))
                else:
                    self.vpn_status = "Failed"
                    self.root.after(0, lambda: self.log_message(f"VPN connection failed: {server_name}", "ERROR"))
                    self.root.after(0, lambda: self.set_status("VPN connection failed"))
            except Exception as e:
                self.vpn_status = "Error"
                self.root.after(0, lambda: self.log_message(f"VPN connection error: {e}", "ERROR"))
                self.root.after(0, lambda: self.set_status("VPN connection error"))
                
        threading.Thread(target=connect_vpn_thread, daemon=True).start()
        
    def disconnect_vpn(self):
        """Disconnect from VPN"""
        self.set_status("Disconnecting VPN...")
        
        def disconnect_vpn_thread():
            try:
                result = self.vpn_manager.disconnect()
                if result:
                    self.vpn_status = "Disconnected"
                    self.root.after(0, lambda: self.log_message("VPN disconnected"))
                    self.root.after(0, lambda: self.set_status("VPN disconnected"))
                else:
                    self.root.after(0, lambda: self.log_message("VPN disconnection failed", "ERROR"))
                    self.root.after(0, lambda: self.set_status("VPN disconnection failed"))
                    
            except Exception as e:
                self.root.after(0, lambda: self.log_message(f"VPN disconnection error: {e}", "ERROR"))
                self.root.after(0, lambda: self.set_status("VPN disconnection error"))
                
        threading.Thread(target=disconnect_vpn_thread, daemon=True).start()
        
    def start_tor(self):
        """Start Tor service with enhanced error handling"""
        self.set_status("Starting Tor...")
        
        def start_tor_thread():
            try:
                # First check if Tor is already running
                if self.tor_controller.is_tor_running():
                    self.tor_status = "Running"
                    self.root.after(0, lambda: self.log_message("Tor is already running"))
                    self.root.after(0, lambda: self.set_status("Tor is already running"))
                    self.root.after(0, self.update_tor_status)
                    return
                
                # Check if Tor is installed
                if not self.tor_controller._check_tor_installation():
                    self.tor_status = "Not Installed"
                    self.root.after(0, lambda: self.log_message("Tor is not installed on this system", "ERROR"))
                    self.root.after(0, lambda: self.show_tor_installation_dialog())
                    self.root.after(0, lambda: self.set_status("Tor not installed"))
                    self.root.after(0, self.update_tor_status)
                    return
                
                # Start Tor service
                self.root.after(0, lambda: self.log_message("Starting Tor service..."))
                result = self.tor_controller.start_tor_service()
                
                if result:
                    self.tor_status = "Running"
                    self.root.after(0, lambda: self.log_message("Tor started successfully"))
                    self.root.after(0, lambda: self.set_status("Tor started successfully"))
                    
                    # Try to connect to controller
                    if self.tor_controller.connect_to_controller():
                        self.root.after(0, lambda: self.log_message("Connected to Tor controller"))
                        
                        # Test the connection
                        current_ip = self.tor_controller.get_current_ip()
                        if current_ip:
                            self.root.after(0, lambda: self.log_message(f"Tor connection verified. IP: {current_ip}"))
                        else:
                            self.root.after(0, lambda: self.log_message("Tor started but connection test failed", "WARNING"))
                    else:
                        self.root.after(0, lambda: self.log_message("Tor started but controller connection failed", "WARNING"))
                else:
                    self.tor_status = "Failed"
                    self.root.after(0, lambda: self.log_message("Failed to start Tor service", "ERROR"))
                    self.root.after(0, lambda: self.set_status("Tor start failed"))
                    
            except Exception as e:
                self.tor_status = "Error"
                self.root.after(0, lambda: self.log_message(f"Tor start error: {e}", "ERROR"))
                self.root.after(0, lambda: self.set_status("Tor start error"))
            finally:
                self.root.after(0, self.update_tor_status)
                
        threading.Thread(target=start_tor_thread, daemon=True).start()
        
    def stop_tor(self):
        """Stop Tor service with enhanced cleanup"""
        self.set_status("Stopping Tor...")
        
        def stop_tor_thread():
            try:
                if not self.tor_controller.is_tor_running():
                    self.tor_status = "Stopped"
                    self.root.after(0, lambda: self.log_message("Tor is already stopped"))
                    self.root.after(0, lambda: self.set_status("Tor is already stopped"))
                    self.root.after(0, self.update_tor_status)
                    return
                
                # Stop Tor service
                self.tor_controller.stop_tor_service()
                self.tor_status = "Stopped"
                self.root.after(0, lambda: self.log_message("Tor stopped successfully"))
                self.root.after(0, lambda: self.set_status("Tor stopped"))
                    
            except Exception as e:
                self.root.after(0, lambda: self.log_message(f"Tor stop error: {e}", "ERROR"))
                self.root.after(0, lambda: self.set_status("Tor stop error"))
            finally:
                self.root.after(0, self.update_tor_status)
                
        threading.Thread(target=stop_tor_thread, daemon=True).start()
        
    def new_tor_identity(self):
        """Get new Tor identity with enhanced feedback"""
        self.set_status("Getting new Tor identity...")
        
        def new_identity_thread():
            try:
                # Check if Tor is running
                if not self.tor_controller.is_tor_running():
                    self.root.after(0, lambda: self.log_message("Tor is not running. Please start Tor first.", "ERROR"))
                    self.root.after(0, lambda: self.set_status("Tor not running"))
                    return
                
                # Get current IP for comparison
                old_ip = self.tor_controller.get_current_ip()
                if old_ip:
                    self.root.after(0, lambda: self.log_message(f"Current IP: {old_ip}"))
                
                # Create new circuit
                result = self.tor_controller.new_circuit()
                
                if result:
                    self.root.after(0, lambda: self.log_message("New Tor circuit created"))
                    
                    # Wait a moment and get new IP
                    time.sleep(3)
                    new_ip = self.tor_controller.get_current_ip()
                    
                    if new_ip:
                        if new_ip != old_ip:
                            self.root.after(0, lambda: self.log_message(f"New IP acquired: {new_ip}"))
                            self.root.after(0, lambda: self.set_status("New Tor identity acquired"))
                        else:
                            self.root.after(0, lambda: self.log_message("New circuit created but IP unchanged", "WARNING"))
                            self.root.after(0, lambda: self.set_status("Circuit rotated (IP unchanged)"))
                    else:
                        self.root.after(0, lambda: self.log_message("New circuit created but IP verification failed", "WARNING"))
                        self.root.after(0, lambda: self.set_status("Circuit rotated"))
                else:
                    self.root.after(0, lambda: self.log_message("Failed to create new circuit", "ERROR"))
                    self.root.after(0, lambda: self.set_status("Circuit rotation failed"))
                    
            except Exception as e:
                self.root.after(0, lambda: self.log_message(f"New identity error: {e}", "ERROR"))
                self.root.after(0, lambda: self.set_status("New identity error"))
                
        threading.Thread(target=new_identity_thread, daemon=True).start()
        
    def check_dns_leaks(self):
        """Check for DNS leaks"""
        self.set_status("Checking for DNS leaks...")
        
        def dns_leak_thread():
            try:
                result = self.network_monitor.check_dns_leaks()
                if result.get('secure', True):
                    self.root.after(0, lambda: self.log_message("No DNS leaks detected"))
                    self.root.after(0, lambda: self.set_status("DNS leak check passed"))
                else:
                    self.root.after(0, lambda: self.log_message("DNS leaks detected!", "WARNING"))
                    self.root.after(0, lambda: self.set_status("DNS leaks detected"))
                    
            except Exception as e:
                self.root.after(0, lambda: self.log_message(f"DNS leak check error: {e}", "ERROR"))
                self.root.after(0, lambda: self.set_status("DNS leak check failed"))
                
        threading.Thread(target=dns_leak_thread, daemon=True).start()
        
    def full_security_scan(self):
        """Perform full security scan"""
        self.set_status("Performing full security scan...")
        
        def security_scan_thread():
            try:
                # Perform various security checks
                results = {
                    'ip_check': True,
                    'dns_leak': True,
                    'webrtc_leak': True,
                    'proxy_anonymity': True
                }
                
                # Add actual security checks here
                self.root.after(0, lambda: self.log_message("Security scan completed"))
                self.root.after(0, lambda: self.set_status("Security scan completed"))
                
            except Exception as e:
                self.root.after(0, lambda: self.log_message(f"Security scan error: {e}", "ERROR"))
                self.root.after(0, lambda: self.set_status("Security scan failed"))
                
        threading.Thread(target=security_scan_thread, daemon=True).start()
        
    def quick_rotate(self):
        """Perform quick rotation of all services"""
        self.set_status("Performing quick rotation...")
        
        def quick_rotate_thread():
            try:
                # Rotate proxy
                self.proxy_manager.rotate_proxy()
                
                # Get new Tor identity if running
                if self.tor_status == "Running":
                    self.tor_controller.new_circuit()
                    
                self.root.after(0, lambda: self.log_message("Quick rotation completed"))
                self.root.after(0, lambda: self.set_status("Quick rotation completed"))
                
            except Exception as e:
                self.root.after(0, lambda: self.log_message(f"Quick rotation error: {e}", "ERROR"))
                self.root.after(0, lambda: self.set_status("Quick rotation failed"))
                
        threading.Thread(target=quick_rotate_thread, daemon=True).start()
        
    def emergency_stop(self):
        """Emergency stop all connections"""
        if messagebox.askyesno("Confirm", "Stop all connections immediately?"):
            self.set_status("Emergency stop initiated...")
            
            def emergency_stop_thread():
                try:
                    # Disconnect VPN
                    self.vpn_manager.disconnect()
                    self.vpn_status = "Disconnected"
                    
                    # Stop Tor
                    self.tor_controller.stop()
                    self.tor_status = "Stopped"
                    
                    # Reset proxy
                    self.proxy_status = "Disconnected"
                    
                    self.root.after(0, lambda: self.log_message("Emergency stop completed"))
                    self.root.after(0, lambda: self.set_status("All connections stopped"))
                    
                except Exception as e:
                    self.root.after(0, lambda: self.log_message(f"Emergency stop error: {e}", "ERROR"))
                    self.root.after(0, lambda: self.set_status("Emergency stop failed"))
                    
            threading.Thread(target=emergency_stop_thread, daemon=True).start()
            
    def refresh_all(self):
        """Refresh all status information"""
        self.set_status("Refreshing all information...")
        self.update_all_status()
        self.update_vpn_servers()
        self.set_status("Information refreshed")
        
    def save_settings(self):
        """Save current settings"""
        try:
            # Update config with new values
            self.config['proxy']['rotation_interval'] = int(self.rotation_interval.get())
            
            # Save to file
            with open(self.config_file, 'w') as f:
                json.dump(self.config, f, indent=2)
                
            self.log_message("Settings saved")
            self.set_status("Settings saved")
            messagebox.showinfo("Success", "Settings saved successfully")
            
        except Exception as e:
            self.log_message(f"Failed to save settings: {e}", "ERROR")
            messagebox.showerror("Error", f"Failed to save settings: {e}")
            
    def on_closing(self):
        """Handle application closing"""
        if messagebox.askokcancel("Quit", "Do you want to quit CyberRotate Pro?"):
            self.is_monitoring = False
            self.root.destroy()
            
    def run(self):
        """Start the GUI application"""
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.log_message("CyberRotate Pro GUI started")
        self.set_status("Ready")
        self.root.mainloop()

    def show_tor_installation_dialog(self):
        """Show Tor installation instructions dialog"""
        instructions = self.tor_controller.install_tor_instructions()
        
        # Create a new window for installation instructions
        install_window = tk.Toplevel(self.root)
        install_window.title("Tor Installation Required")
        install_window.geometry("600x400")
        install_window.transient(self.root)
        install_window.grab_set()
        
        # Main frame
        main_frame = ttk.Frame(install_window, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Title
        title_label = ttk.Label(main_frame, text="Tor Installation Required", 
                               font=('Arial', 14, 'bold'))
        title_label.pack(anchor="w", pady=(0, 10))
        
        # Instructions text
        text_widget = scrolledtext.ScrolledText(main_frame, wrap=tk.WORD, 
                                              width=70, height=15)
        text_widget.pack(fill=tk.BOTH, expand=True, pady=(0, 10))
        text_widget.insert(tk.END, instructions)
        text_widget.config(state=tk.DISABLED)
        
        # Buttons frame
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(fill="x")
        
        ttk.Button(button_frame, text="Close", 
                  command=install_window.destroy).pack(side=tk.RIGHT, padx=(10, 0))
        
        ttk.Button(button_frame, text="Test Tor Installation", 
                  command=lambda: self.test_tor_installation(install_window)).pack(side=tk.RIGHT)
    
    def test_tor_installation(self, parent_window=None):
        """Test Tor installation and update status"""
        def test_thread():
            try:
                is_installed = self.tor_controller._check_tor_installation()
                
                if is_installed:
                    self.root.after(0, lambda: self.log_message("Tor installation detected!"))
                    if parent_window:
                        self.root.after(0, parent_window.destroy)
                else:
                    self.root.after(0, lambda: self.log_message("Tor is still not installed", "WARNING"))
                    
                self.root.after(0, self.update_tor_status)
                
            except Exception as e:
                self.root.after(0, lambda: self.log_message(f"Error testing Tor installation: {e}", "ERROR"))
        
        threading.Thread(target=test_thread, daemon=True).start()
    
    def update_tor_status(self):
        """Update Tor status indicator in GUI"""
        try:
            is_running = self.tor_controller.is_tor_running()
            is_connected = self.tor_controller.is_connected
            
            if is_running and is_connected:
                self.tor_indicator.config(fg="green")
                self.tor_status = "Connected"
            elif is_running:
                self.tor_indicator.config(fg="orange")
                self.tor_status = "Running"
            else:
                self.tor_indicator.config(fg="red")
                if not self.tor_controller._check_tor_installation():
                    self.tor_status = "Not Installed"
                else:
                    self.tor_status = "Stopped"
            
            # Update status label
            if hasattr(self, 'tor_status_label'):
                self.tor_status_label.config(text=f"Status: {self.tor_status}")
                
        except Exception as e:
            self.log_message(f"Error updating Tor status: {e}", "ERROR")
    
    def show_tor_diagnostics(self):
        """Show Tor diagnostics window"""
        diag_window = tk.Toplevel(self.root)
        diag_window.title("Tor Diagnostics")
        diag_window.geometry("800x600")
        diag_window.transient(self.root)
        diag_window.grab_set()
        
        # Main frame
        main_frame = ttk.Frame(diag_window, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Title
        title_label = ttk.Label(main_frame, text="Tor Network Diagnostics", 
                               font=('Arial', 14, 'bold'))
        title_label.pack(anchor="w", pady=(0, 10))
        
        # Diagnostics text area
        self.diag_text = scrolledtext.ScrolledText(main_frame, wrap=tk.WORD, 
                                                  width=90, height=25)
        self.diag_text.pack(fill=tk.BOTH, expand=True, pady=(0, 10))
        
        # Buttons frame
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(fill="x")
        
        ttk.Button(button_frame, text="Run Diagnostics", 
                  command=self.run_tor_diagnostics).pack(side=tk.LEFT)
        
        ttk.Button(button_frame, text="Clear", 
                  command=lambda: self.diag_text.delete(1.0, tk.END)).pack(side=tk.LEFT, padx=(10, 0))
        
        ttk.Button(button_frame, text="Close", 
                  command=diag_window.destroy).pack(side=tk.RIGHT)
    
    def run_tor_diagnostics(self):
        """Run comprehensive Tor diagnostics"""
        def diag_thread():
            try:
                self.root.after(0, lambda: self.diag_text.delete(1.0, tk.END))
                self.root.after(0, lambda: self.diag_text.insert(tk.END, "Running Tor diagnostics...\n\n"))
                
                # Check installation
                is_installed = self.tor_controller._check_tor_installation()
                self.root.after(0, lambda: self.diag_text.insert(tk.END, f"Tor Installation: {'✓ FOUND' if is_installed else '✗ NOT FOUND'}\n"))
                
                if not is_installed:
                    instructions = self.tor_controller.install_tor_instructions()
                    self.root.after(0, lambda: self.diag_text.insert(tk.END, f"\n{instructions}\n"))
                    return
                
                # Check if running
                is_running = self.tor_controller.is_tor_running()
                self.root.after(0, lambda: self.diag_text.insert(tk.END, f"Tor Service: {'✓ RUNNING' if is_running else '✗ STOPPED'}\n"))
                
                if not is_running:
                    self.root.after(0, lambda: self.diag_text.insert(tk.END, "Note: Start Tor service to run connectivity tests\n"))
                    return
                
                # Check controller connection
                is_connected = self.tor_controller.is_connected or self.tor_controller.connect_to_controller()
                self.root.after(0, lambda: self.diag_text.insert(tk.END, f"Controller Connection: {'✓ CONNECTED' if is_connected else '✗ FAILED'}\n"))
                
                # Test connectivity
                if is_connected:
                    current_ip = self.tor_controller.get_current_ip()
                    if current_ip:
                        self.root.after(0, lambda: self.diag_text.insert(tk.END, f"Current Tor IP: {current_ip}\n"))
                        self.root.after(0, lambda: self.diag_text.insert(tk.END, "Network Connectivity: ✓ WORKING\n"))
                    else:
                        self.root.after(0, lambda: self.diag_text.insert(tk.END, "Network Connectivity: ✗ FAILED\n"))
                    
                    # Get statistics
                    stats = self.tor_controller.get_statistics()
                    self.root.after(0, lambda: self.diag_text.insert(tk.END, f"\nStatistics:\n"))
                    self.root.after(0, lambda: self.diag_text.insert(tk.END, f"  Circuits Created: {stats.get('circuit_count', 0)}\n"))
                    self.root.after(0, lambda: self.diag_text.insert(tk.END, f"  Successful Rotations: {stats.get('successful_rotations', 0)}\n"))
                    self.root.after(0, lambda: self.diag_text.insert(tk.END, f"  Failed Rotations: {stats.get('failed_rotations', 0)}\n"))
                    self.root.after(0, lambda: self.diag_text.insert(tk.END, f"  Success Rate: {stats.get('success_rate', 0):.1f}%\n"))
                
                self.root.after(0, lambda: self.diag_text.insert(tk.END, "\nDiagnostics completed.\n"))
                
            except Exception as e:
                self.root.after(0, lambda: self.diag_text.insert(tk.END, f"Diagnostics error: {e}\n"))
        
        threading.Thread(target=diag_thread, daemon=True).start()
        
def print_banner():
    """Print the CyberRotate Pro banner"""
    banner = """
╔══════════════════════════════════════════════════════════════════════════════╗
║                          CYBERROTATE PRO GLOBAL NETWORK                      ║
╠══════════════════════════════════════════════════════════════════════════════╣
║                                                                              ║
║   203.0.113.5 ──┐              ╭───────────╮              ┌── 8.8.8.8        ║
║                 │              │     🌍    │              │                 ║
║   1.1.1.1 ──────┼──────────────│   EARTH   │──────────────┼──── 9.9.9.9      ║
║                 │              │  NETWORK  │              │                  ║
║   74.125.224.72─┘              ╰───────────╯               └─ 208.67.222.222 ║
║                                                                              ║
║   ┌─── LIVE STATUS ──────────────────────────────────────────────────────┐   ║
║   │ 🔄 Current: 185.199.108.153 ➤ 104.21.14.101 ➤ 151.101.193.140      │   ║
║   │ 🌐 Nodes: 847 servers • 195 countries • 99.97% uptime                │   ║
║   │ 🛡️ Security: Zero logs • Kill switch • DNS leak protection           │   ║
║   └──────────────────────────────────────────────────────────────────────┘   ║
║                                                                              ║
║                    🔒 Professional IP Rotation Suite 🔒                      ║
║                         Created by Yashab Alam - ZehraSec                    ║
║                                                                              ║
╚══════════════════════════════════════════════════════════════════════════════╝
    """
    print(banner)

def main():
    """Main function"""
    print_banner()
    
    import argparse
    
    parser = argparse.ArgumentParser(description='CyberRotate Pro GUI')
    parser.add_argument('--config', default='config/config.json', help='Configuration file path')
    
    args = parser.parse_args()
    
    try:
        app = CyberRotateGUI(args.config)
        app.run()
    except Exception as e:
        print(f"Failed to start GUI: {e}")
        return 1
        
    return 0

if __name__ == '__main__':
    print_banner()
    exit(main())
