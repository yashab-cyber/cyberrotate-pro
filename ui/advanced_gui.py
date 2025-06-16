#!/usr/bin/env python3
"""
CyberRotate Pro - Advanced GUI Components
Additional GUI components and utilities for enhanced user experience
"""

import tkinter as tk
from tkinter import ttk
try:
    import matplotlib.pyplot as plt
    from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
    import numpy as np
    HAS_MATPLOTLIB = True
except ImportError:
    HAS_MATPLOTLIB = False
    print("Warning: matplotlib not available. Advanced charts will be disabled.")

from datetime import datetime, timedelta
import threading
import time

class NetworkSpeedGauge:
    """Network speed gauge widget"""
    
    def __init__(self, parent, title="Network Speed"):
        self.parent = parent
        self.title = title
        self.current_speed = 0
        self.max_speed = 100
        
        self.create_gauge()
          def create_gauge(self):
        """Create the speed gauge"""
        self.frame = ttk.LabelFrame(self.parent, text=self.title, padding="10")
        
        if not HAS_MATPLOTLIB:
            # Fallback to simple text display
            self.speed_label = ttk.Label(self.frame, text="0 Mbps", font=('Arial', 12, 'bold'))
            self.speed_label.pack()
            ttk.Label(self.frame, text="(Install matplotlib for gauge display)").pack()
            return
        
        # Create matplotlib figure
        self.fig, self.ax = plt.subplots(figsize=(4, 3), subplot_kw=dict(projection='polar'))
        self.fig.patch.set_facecolor('white')
        
        # Configure gauge
        self.ax.set_theta_zero_location('N')
        self.ax.set_theta_direction(-1)
        self.ax.set_thetalim(0, np.pi)
        self.ax.set_ylim(0, 100)
        self.ax.set_yticks([20, 40, 60, 80, 100])
        self.ax.set_yticklabels(['20', '40', '60', '80', '100 Mbps'])
        self.ax.grid(True)
        
        # Create needle
        self.needle, = self.ax.plot([0, 0], [0, 80], 'r-', linewidth=3)
        
        # Embed in tkinter
        self.canvas = FigureCanvasTkAgg(self.fig, self.frame)
        self.canvas.get_tk_widget().pack(fill="both", expand=True)
        
        # Speed label
        self.speed_label = ttk.Label(self.frame, text="0 Mbps", font=('Arial', 12, 'bold'))
        self.speed_label.pack()
          def update_speed(self, speed):
        """Update the gauge with new speed value"""
        self.current_speed = speed
        
        if not HAS_MATPLOTLIB:
            # Fallback to simple text display
            self.speed_label.config(text=f"{speed:.1f} Mbps")
            return
        
        # Convert speed to angle (0 to pi)
        angle = (speed / self.max_speed) * np.pi
        
        # Update needle
        self.needle.set_data([angle, angle], [0, 80])
        
        # Update label
        self.speed_label.config(text=f"{speed:.1f} Mbps")
        
        # Refresh canvas
        self.canvas.draw()
        
    def pack(self, **kwargs):
        """Pack the gauge frame"""
        self.frame.pack(**kwargs)

class ConnectionHistoryChart:
    """Connection history chart widget"""
    
    def __init__(self, parent, title="Connection History"):
        self.parent = parent
        self.title = title
        self.history_data = {'time': [], 'proxy': [], 'vpn': [], 'tor': []}
        self.max_points = 50
        
        self.create_chart()
        
    def create_chart(self):
        """Create the history chart"""
        self.frame = ttk.LabelFrame(self.parent, text=self.title, padding="10")
        
        # Create matplotlib figure
        self.fig, self.ax = plt.subplots(figsize=(8, 4))
        self.fig.patch.set_facecolor('white')
        
        # Configure chart
        self.ax.set_title('Connection Status Over Time')
        self.ax.set_xlabel('Time')
        self.ax.set_ylabel('Status')
        self.ax.set_ylim(-0.5, 3.5)
        self.ax.set_yticks([0, 1, 2, 3])
        self.ax.set_yticklabels(['Disconnected', 'Proxy', 'VPN', 'Tor'])
        self.ax.grid(True, alpha=0.3)
        
        # Create lines
        self.proxy_line, = self.ax.plot([], [], 'b-', label='Proxy', linewidth=2)
        self.vpn_line, = self.ax.plot([], [], 'g-', label='VPN', linewidth=2)
        self.tor_line, = self.ax.plot([], [], 'r-', label='Tor', linewidth=2)
        
        self.ax.legend()
        
        # Embed in tkinter
        self.canvas = FigureCanvasTkAgg(self.fig, self.frame)
        self.canvas.get_tk_widget().pack(fill="both", expand=True)
        
    def add_data_point(self, proxy_status, vpn_status, tor_status):
        """Add new data point to the chart"""
        current_time = datetime.now()
        
        # Add to history
        self.history_data['time'].append(current_time)
        self.history_data['proxy'].append(1 if proxy_status == "Connected" else 0)
        self.history_data['vpn'].append(2 if vpn_status == "Connected" else 0)
        self.history_data['tor'].append(3 if tor_status == "Running" else 0)
        
        # Limit history size
        if len(self.history_data['time']) > self.max_points:
            for key in self.history_data:
                self.history_data[key].pop(0)
                
        # Update chart
        self.update_chart()
        
    def update_chart(self):
        """Update the chart display"""
        if not self.history_data['time']:
            return
            
        times = self.history_data['time']
        
        # Update lines
        self.proxy_line.set_data(times, self.history_data['proxy'])
        self.vpn_line.set_data(times, self.history_data['vpn'])
        self.tor_line.set_data(times, self.history_data['tor'])
        
        # Update x-axis
        self.ax.set_xlim(times[0], times[-1])
        
        # Format x-axis labels
        self.fig.autofmt_xdate()
        
        # Refresh canvas
        self.canvas.draw()
        
    def pack(self, **kwargs):
        """Pack the chart frame"""
        self.frame.pack(**kwargs)

class AdvancedSettingsDialog:
    """Advanced settings dialog"""
    
    def __init__(self, parent, config):
        self.parent = parent
        self.config = config
        self.result = None
        
        self.create_dialog()
        
    def create_dialog(self):
        """Create the settings dialog"""
        self.dialog = tk.Toplevel(self.parent)
        self.dialog.title("Advanced Settings")
        self.dialog.geometry("500x600")
        self.dialog.transient(self.parent)
        self.dialog.grab_set()
        
        # Center the dialog
        self.center_dialog()
        
        # Create notebook for different setting categories
        notebook = ttk.Notebook(self.dialog)
        notebook.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Proxy settings tab
        proxy_frame = ttk.Frame(notebook)
        notebook.add(proxy_frame, text="Proxy Settings")
        self.create_proxy_settings(proxy_frame)
        
        # VPN settings tab
        vpn_frame = ttk.Frame(notebook)
        notebook.add(vpn_frame, text="VPN Settings")
        self.create_vpn_settings(vpn_frame)
        
        # Tor settings tab
        tor_frame = ttk.Frame(notebook)
        notebook.add(tor_frame, text="Tor Settings")
        self.create_tor_settings(tor_frame)
        
        # Security settings tab
        security_frame = ttk.Frame(notebook)
        notebook.add(security_frame, text="Security")
        self.create_security_settings(security_frame)
        
        # Buttons
        button_frame = ttk.Frame(self.dialog)
        button_frame.pack(fill="x", padx=10, pady=10)
        
        ttk.Button(button_frame, text="Save", command=self.save_settings).pack(side="right", padx=5)
        ttk.Button(button_frame, text="Cancel", command=self.cancel).pack(side="right")
        ttk.Button(button_frame, text="Reset to Defaults", command=self.reset_defaults).pack(side="left")
        
    def center_dialog(self):
        """Center the dialog on parent window"""
        self.dialog.update_idletasks()
        x = (self.parent.winfo_x() + (self.parent.winfo_width() // 2) - 
             (self.dialog.winfo_width() // 2))
        y = (self.parent.winfo_y() + (self.parent.winfo_height() // 2) - 
             (self.dialog.winfo_height() // 2))
        self.dialog.geometry(f"+{x}+{y}")
        
    def create_proxy_settings(self, parent):
        """Create proxy settings"""
        frame = ttk.Frame(parent, padding="10")
        frame.pack(fill="both", expand=True)
        
        # Rotation interval
        ttk.Label(frame, text="Rotation Interval (seconds):").pack(anchor="w")
        self.rotation_interval = tk.StringVar(value=str(self.config.get('proxy', {}).get('rotation_interval', 300)))
        ttk.Entry(frame, textvariable=self.rotation_interval).pack(fill="x", pady=(0, 10))
        
        # Max failures
        ttk.Label(frame, text="Max Failures Before Rotation:").pack(anchor="w")
        self.max_failures = tk.StringVar(value=str(self.config.get('proxy', {}).get('max_failures', 3)))
        ttk.Entry(frame, textvariable=self.max_failures).pack(fill="x", pady=(0, 10))
        
        # Timeout
        ttk.Label(frame, text="Connection Timeout (seconds):").pack(anchor="w")
        self.proxy_timeout = tk.StringVar(value=str(self.config.get('proxy', {}).get('timeout', 30)))
        ttk.Entry(frame, textvariable=self.proxy_timeout).pack(fill="x", pady=(0, 10))
        
        # Verify SSL
        self.verify_ssl = tk.BooleanVar(value=self.config.get('proxy', {}).get('verify_ssl', True))
        ttk.Checkbutton(frame, text="Verify SSL Certificates", variable=self.verify_ssl).pack(anchor="w")
        
        # User agent rotation
        self.rotate_user_agent = tk.BooleanVar(value=self.config.get('proxy', {}).get('rotate_user_agent', False))
        ttk.Checkbutton(frame, text="Rotate User Agent", variable=self.rotate_user_agent).pack(anchor="w")
        
    def create_vpn_settings(self, parent):
        """Create VPN settings"""
        frame = ttk.Frame(parent, padding="10")
        frame.pack(fill="both", expand=True)
        
        # Connection timeout
        ttk.Label(frame, text="Connection Timeout (seconds):").pack(anchor="w")
        self.vpn_timeout = tk.StringVar(value=str(self.config.get('openvpn', {}).get('timeout', 30)))
        ttk.Entry(frame, textvariable=self.vpn_timeout).pack(fill="x", pady=(0, 10))
        
        # Retry attempts
        ttk.Label(frame, text="Retry Attempts:").pack(anchor="w")
        self.retry_attempts = tk.StringVar(value=str(self.config.get('openvpn', {}).get('retry_attempts', 3)))
        ttk.Entry(frame, textvariable=self.retry_attempts).pack(fill="x", pady=(0, 10))
        
        # Auto-reconnect
        self.auto_reconnect = tk.BooleanVar(value=self.config.get('openvpn', {}).get('auto_reconnect', True))
        ttk.Checkbutton(frame, text="Auto-Reconnect on Connection Loss", variable=self.auto_reconnect).pack(anchor="w")
        
        # Kill switch
        self.kill_switch = tk.BooleanVar(value=self.config.get('openvpn', {}).get('kill_switch', True))
        ttk.Checkbutton(frame, text="Enable Kill Switch", variable=self.kill_switch).pack(anchor="w")
        
        # DNS leak protection
        self.dns_protection = tk.BooleanVar(value=self.config.get('openvpn', {}).get('dns_protection', True))
        ttk.Checkbutton(frame, text="DNS Leak Protection", variable=self.dns_protection).pack(anchor="w")
        
    def create_tor_settings(self, parent):
        """Create Tor settings"""
        frame = ttk.Frame(parent, padding="10")
        frame.pack(fill="both", expand=True)
        
        # SOCKS port
        ttk.Label(frame, text="SOCKS Port:").pack(anchor="w")
        self.socks_port = tk.StringVar(value=str(self.config.get('tor', {}).get('socks_port', 9150)))
        ttk.Entry(frame, textvariable=self.socks_port).pack(fill="x", pady=(0, 10))
        
        # Control port
        ttk.Label(frame, text="Control Port:").pack(anchor="w")
        self.control_port = tk.StringVar(value=str(self.config.get('tor', {}).get('control_port', 9151)))
        ttk.Entry(frame, textvariable=self.control_port).pack(fill="x", pady=(0, 10))
        
        # Auto-start
        self.auto_start_tor = tk.BooleanVar(value=self.config.get('tor', {}).get('auto_start', False))
        ttk.Checkbutton(frame, text="Auto-start Tor on Application Launch", variable=self.auto_start_tor).pack(anchor="w")
        
        # Circuit length
        ttk.Label(frame, text="Circuit Length:").pack(anchor="w")
        self.circuit_length = tk.StringVar(value=str(self.config.get('tor', {}).get('circuit_length', 3)))
        ttk.Entry(frame, textvariable=self.circuit_length).pack(fill="x", pady=(0, 10))
        
        # Exclude exit nodes
        ttk.Label(frame, text="Exclude Exit Nodes (comma-separated):").pack(anchor="w")
        self.exclude_exit_nodes = tk.StringVar(value=self.config.get('tor', {}).get('exclude_exit_nodes', ''))
        ttk.Entry(frame, textvariable=self.exclude_exit_nodes).pack(fill="x", pady=(0, 10))
        
    def create_security_settings(self, parent):
        """Create security settings"""
        frame = ttk.Frame(parent, padding="10")
        frame.pack(fill="both", expand=True)
        
        # Leak detection interval
        ttk.Label(frame, text="Leak Detection Interval (seconds):").pack(anchor="w")
        self.leak_detection_interval = tk.StringVar(value=str(self.config.get('security', {}).get('leak_detection_interval', 60)))
        ttk.Entry(frame, textvariable=self.leak_detection_interval).pack(fill="x", pady=(0, 10))
        
        # Enable logging
        self.enable_logging = tk.BooleanVar(value=self.config.get('security', {}).get('enable_logging', True))
        ttk.Checkbutton(frame, text="Enable Detailed Logging", variable=self.enable_logging).pack(anchor="w")
        
        # Log level
        ttk.Label(frame, text="Log Level:").pack(anchor="w")
        self.log_level = tk.StringVar(value=self.config.get('security', {}).get('log_level', 'INFO'))
        log_level_combo = ttk.Combobox(frame, textvariable=self.log_level, values=['DEBUG', 'INFO', 'WARNING', 'ERROR'])
        log_level_combo.pack(fill="x", pady=(0, 10))
        
        # Auto-clear logs
        self.auto_clear_logs = tk.BooleanVar(value=self.config.get('security', {}).get('auto_clear_logs', False))
        ttk.Checkbutton(frame, text="Auto-clear Logs (Weekly)", variable=self.auto_clear_logs).pack(anchor="w")
        
        # Secure delete
        self.secure_delete = tk.BooleanVar(value=self.config.get('security', {}).get('secure_delete', True))
        ttk.Checkbutton(frame, text="Secure Delete Temporary Files", variable=self.secure_delete).pack(anchor="w")
        
    def save_settings(self):
        """Save settings and close dialog"""
        try:
            # Update config with new values
            self.config['proxy'] = self.config.get('proxy', {})
            self.config['proxy']['rotation_interval'] = int(self.rotation_interval.get())
            self.config['proxy']['max_failures'] = int(self.max_failures.get())
            self.config['proxy']['timeout'] = int(self.proxy_timeout.get())
            self.config['proxy']['verify_ssl'] = self.verify_ssl.get()
            self.config['proxy']['rotate_user_agent'] = self.rotate_user_agent.get()
            
            self.config['openvpn'] = self.config.get('openvpn', {})
            self.config['openvpn']['timeout'] = int(self.vpn_timeout.get())
            self.config['openvpn']['retry_attempts'] = int(self.retry_attempts.get())
            self.config['openvpn']['auto_reconnect'] = self.auto_reconnect.get()
            self.config['openvpn']['kill_switch'] = self.kill_switch.get()
            self.config['openvpn']['dns_protection'] = self.dns_protection.get()
            
            self.config['tor'] = self.config.get('tor', {})
            self.config['tor']['socks_port'] = int(self.socks_port.get())
            self.config['tor']['control_port'] = int(self.control_port.get())
            self.config['tor']['auto_start'] = self.auto_start_tor.get()
            self.config['tor']['circuit_length'] = int(self.circuit_length.get())
            self.config['tor']['exclude_exit_nodes'] = self.exclude_exit_nodes.get()
            
            self.config['security'] = self.config.get('security', {})
            self.config['security']['leak_detection_interval'] = int(self.leak_detection_interval.get())
            self.config['security']['enable_logging'] = self.enable_logging.get()
            self.config['security']['log_level'] = self.log_level.get()
            self.config['security']['auto_clear_logs'] = self.auto_clear_logs.get()
            self.config['security']['secure_delete'] = self.secure_delete.get()
            
            self.result = self.config
            self.dialog.destroy()
            
        except ValueError as e:
            tk.messagebox.showerror("Error", f"Invalid input: {e}")
        except Exception as e:
            tk.messagebox.showerror("Error", f"Failed to save settings: {e}")
            
    def cancel(self):
        """Cancel and close dialog"""
        self.result = None
        self.dialog.destroy()
        
    def reset_defaults(self):
        """Reset all settings to defaults"""
        if tk.messagebox.askyesno("Confirm", "Reset all settings to defaults?"):
            # Reset all variables to default values
            self.rotation_interval.set("300")
            self.max_failures.set("3")
            self.proxy_timeout.set("30")
            self.verify_ssl.set(True)
            self.rotate_user_agent.set(False)
            
            self.vpn_timeout.set("30")
            self.retry_attempts.set("3")
            self.auto_reconnect.set(True)
            self.kill_switch.set(True)
            self.dns_protection.set(True)
            
            self.socks_port.set("9150")
            self.control_port.set("9151")
            self.auto_start_tor.set(False)
            self.circuit_length.set("3")
            self.exclude_exit_nodes.set("")
            
            self.leak_detection_interval.set("60")
            self.enable_logging.set(True)
            self.log_level.set("INFO")
            self.auto_clear_logs.set(False)
            self.secure_delete.set(True)

class SystemTrayIcon:
    """System tray icon for minimized operation"""
    
    def __init__(self, parent):
        self.parent = parent
        self.create_tray_icon()
        
    def create_tray_icon(self):
        """Create system tray icon"""
        try:
            import pystray
            from PIL import Image
            
            # Create a simple icon (you can replace with actual icon file)
            image = Image.new('RGB', (64, 64), color='blue')
            
            menu = pystray.Menu(
                pystray.MenuItem("Show", self.show_window),
                pystray.MenuItem("Hide", self.hide_window),
                pystray.MenuItem("Quick Rotate", self.quick_rotate),
                pystray.MenuItem("Exit", self.exit_application)
            )
            
            self.icon = pystray.Icon("CyberRotate Pro", image, menu=menu)
            
        except ImportError:
            print("pystray not available - system tray disabled")
            self.icon = None
            
    def show_window(self, icon=None, item=None):
        """Show the main window"""
        self.parent.root.deiconify()
        self.parent.root.lift()
        
    def hide_window(self, icon=None, item=None):
        """Hide the main window"""
        self.parent.root.withdraw()
        
    def quick_rotate(self, icon=None, item=None):
        """Perform quick rotation from tray"""
        self.parent.quick_rotate()
        
    def exit_application(self, icon=None, item=None):
        """Exit the application"""
        if self.icon:
            self.icon.stop()
        self.parent.on_closing()
        
    def run(self):
        """Run the system tray icon"""
        if self.icon:
            threading.Thread(target=self.icon.run, daemon=True).start()

class ModernTheme:
    """Modern theme manager for the GUI"""
    
    @staticmethod
    def apply_dark_theme(root):
        """Apply dark theme to the application"""
        try:
            # Configure dark theme colors
            bg_color = "#2b2b2b"
            fg_color = "#ffffff"
            select_color = "#404040"
            
            root.configure(bg=bg_color)
            
            style = ttk.Style()
            style.theme_use('clam')
            
            # Configure styles for dark theme
            style.configure('TFrame', background=bg_color)
            style.configure('TLabel', background=bg_color, foreground=fg_color)
            style.configure('TButton', background=select_color, foreground=fg_color)
            style.configure('TEntry', background=select_color, foreground=fg_color)
            style.configure('TCombobox', background=select_color, foreground=fg_color)
            style.configure('TCheckbutton', background=bg_color, foreground=fg_color)
            style.configure('TLabelFrame', background=bg_color, foreground=fg_color)
            style.configure('TNotebook', background=bg_color)
            style.configure('TNotebook.Tab', background=select_color, foreground=fg_color)
            
        except Exception as e:
            print(f"Failed to apply dark theme: {e}")
            
    @staticmethod
    def apply_light_theme(root):
        """Apply light theme to the application"""
        try:
            style = ttk.Style()
            style.theme_use('default')
            
        except Exception as e:
            print(f"Failed to apply light theme: {e}")

# Enhanced GUI launcher
def launch_advanced_gui():
    """Launch the advanced GUI with all features"""
    try:
        from gui_application import CyberRotateGUI
        
        # Create main application
        app = CyberRotateGUI()
        
        # Apply modern theme
        ModernTheme.apply_dark_theme(app.root)
        
        # Add system tray support
        tray = SystemTrayIcon(app)
        tray.run()
        
        # Run the application
        app.run()
        
    except Exception as e:
        print(f"Failed to launch advanced GUI: {e}")
        return 1
        
    return 0

if __name__ == '__main__':
    exit(launch_advanced_gui())
