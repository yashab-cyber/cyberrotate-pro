#!/usr/bin/env python3
"""
CyberRotate Pro - GUI Launcher
Main launcher for the graphical user interface
"""

import sys
import os
import tkinter as tk
from tkinter import messagebox
import subprocess

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def check_dependencies():
    """Check if all required GUI dependencies are available"""
    missing_deps = []
    
    # Check tkinter (should be included with Python)
    try:
        import tkinter
        import tkinter.ttk
    except ImportError:
        missing_deps.append("tkinter")
    
    # Check optional dependencies
    optional_deps = {
        'matplotlib': 'Charts and graphs',
        'numpy': 'Numerical operations for charts',
        'PIL': 'System tray icons',
        'pystray': 'System tray functionality'
    }
    
    available_optional = {}
    for dep, description in optional_deps.items():
        try:
            __import__(dep)
            available_optional[dep] = True
        except ImportError:
            available_optional[dep] = False
    
    return missing_deps, available_optional

def install_optional_dependencies():
    """Install optional GUI dependencies"""
    optional_packages = [
        'matplotlib>=3.5.0',
        'numpy>=1.21.0', 
        'Pillow>=8.0.0',
        'pystray>=0.19.0'
    ]
    
    print("Installing optional GUI dependencies...")
    for package in optional_packages:
        try:
            subprocess.check_call([sys.executable, '-m', 'pip', 'install', package])
            print(f"✓ {package} installed successfully")
        except subprocess.CalledProcessError:
            print(f"✗ Failed to install {package}")

def show_dependency_info(missing_deps, available_optional):
    """Show information about dependencies"""
    if missing_deps:
        print("❌ Missing required dependencies:")
        for dep in missing_deps:
            print(f"  - {dep}")
        print("\nPlease install the missing dependencies and try again.")
        return False
    
    print("✅ All required dependencies are available!")
    
    print("\nOptional dependencies status:")
    for dep, available in available_optional.items():
        status = "✓" if available else "✗"
        print(f"  {status} {dep}")
    
    unavailable = [dep for dep, available in available_optional.items() if not available]
    if unavailable:
        print(f"\nNote: {len(unavailable)} optional dependencies are not available.")
        print("Some advanced features may be limited.")
        
        response = input("\nWould you like to install optional dependencies? (y/N): ")
        if response.lower() == 'y':
            install_optional_dependencies()
            return True
    
    return True

def launch_basic_gui():
    """Launch basic GUI without advanced features"""
    try:
        from ui.gui_application import CyberRotateGUI
        
        print("Starting CyberRotate Pro GUI (Basic Mode)...")
        app = CyberRotateGUI()
        app.run()
        
    except Exception as e:
        print(f"Failed to launch basic GUI: {e}")
        return 1
    
    return 0

def launch_advanced_gui():
    """Launch advanced GUI with all features"""
    try:
        from ui.gui_application import CyberRotateGUI
        from ui.advanced_gui import ModernTheme, SystemTrayIcon
        
        print("Starting CyberRotate Pro GUI (Advanced Mode)...")
        
        # Create main application
        app = CyberRotateGUI()
        
        # Apply modern theme
        try:
            ModernTheme.apply_dark_theme(app.root)
            print("✓ Dark theme applied")
        except Exception as e:
            print(f"⚠ Theme application failed: {e}")
        
        # Add system tray support (after GUI is fully initialized)
        tray = None
        try:
            # Ensure the GUI is fully initialized before creating system tray
            app.root.update_idletasks()
            
            # Create system tray
            tray = SystemTrayIcon(app)
            tray.run()
            print("✓ System tray enabled")
        except Exception as e:
            print(f"⚠ System tray failed: {e}")
            # Continue without system tray
        
        # Run the application
        app.run()
        
    except Exception as e:
        print(f"Failed to launch advanced GUI: {e}")
        import traceback
        traceback.print_exc()
        return 1
    
    return 0

def show_startup_splash():
    """Show startup splash screen"""
    splash = tk.Tk()
    splash.title("CyberRotate Pro")
    splash.geometry("400x300")
    splash.resizable(False, False)
    
    # Center the splash screen
    splash.update_idletasks()
    x = (splash.winfo_screenwidth() // 2) - (splash.winfo_width() // 2)
    y = (splash.winfo_screenheight() // 2) - (splash.winfo_height() // 2)
    splash.geometry(f"+{x}+{y}")
    
    # Remove window decorations
    splash.overrideredirect(True)
    
    # Create splash content
    main_frame = tk.Frame(splash, bg='#2b2b2b', padx=40, pady=40)
    main_frame.pack(fill="both", expand=True)
    
    # Title
    title_label = tk.Label(
        main_frame, 
        text="CyberRotate Pro", 
        font=('Arial', 24, 'bold'),
        fg='#ffffff',
        bg='#2b2b2b'
    )
    title_label.pack(pady=(0, 10))
    
    # Subtitle
    subtitle_label = tk.Label(
        main_frame,
        text="IP Rotation & Anonymity Suite",
        font=('Arial', 12),
        fg='#cccccc',
        bg='#2b2b2b'
    )
    subtitle_label.pack(pady=(0, 20))
    
    # Loading message
    loading_label = tk.Label(
        main_frame,
        text="Loading...",
        font=('Arial', 10),
        fg='#888888',
        bg='#2b2b2b'
    )
    loading_label.pack(pady=(0, 20))
    
    # Progress bar (fake)
    progress_frame = tk.Frame(main_frame, bg='#2b2b2b')
    progress_frame.pack(fill="x")
    
    progress_bg = tk.Frame(progress_frame, bg='#404040', height=4)
    progress_bg.pack(fill="x")
    
    progress_bar = tk.Frame(progress_bg, bg='#0066cc', height=4)
    progress_bar.pack(side="left", fill="y")
      # Animate progress bar
    progress_step = [0]  # Use list to make it mutable in nested function
    
    def animate_progress():
        if progress_step[0] <= 100:
            try:
                # Check if window still exists
                if splash.winfo_exists():
                    progress_bar.config(width=int(300 * progress_step[0] / 100))
                    splash.update_idletasks()
                    progress_step[0] += 2
                    # Schedule next animation step
                    splash.after(40, animate_progress)
            except tk.TclError:
                # Window was destroyed, stop animation
                pass
    
    def close_splash():
        try:
            if splash.winfo_exists():
                splash.destroy()
        except tk.TclError:
            pass
    
    # Start animation and schedule close
    splash.after(100, animate_progress)
    splash.after(2000, close_splash)
    
    splash.mainloop()

def print_banner():
    """Print the CyberRotate Pro banner"""
    banner = """
╔══════════════════════════════════════════════════════════════════════════════╗
║                          CYBERROTATE PRO GLOBAL NETWORK                      ║
╠══════════════════════════════════════════════════════════════════════════════╣
║                                                                              ║
║   203.0.113.5 ──┐              ╭───────────╮              ┌── 8.8.8.8       ║
║                 │              │     🌍     │              │                 ║
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
║                    🔒 Professional IP Rotation Suite 🔒                     ║
║                         Created by Yashab Alam - ZehraSec                   ║
║                                                                              ║
╚══════════════════════════════════════════════════════════════════════════════╝
    """
    print(banner)

def main():
    """Main launcher function"""
    print_banner()
    
    import argparse
    
    parser = argparse.ArgumentParser(description='CyberRotate Pro GUI Launcher')
    parser.add_argument('--mode', choices=['basic', 'advanced', 'auto'], 
                       default='auto', help='GUI mode to launch')
    parser.add_argument('--no-splash', action='store_true', 
                       help='Skip startup splash screen')
    parser.add_argument('--check-deps', action='store_true',
                       help='Check dependencies and exit')
    parser.add_argument('--install-deps', action='store_true',
                       help='Install optional dependencies and exit')
    
    args = parser.parse_args()
    
    # Check dependencies
    missing_deps, available_optional = check_dependencies()
    
    if args.check_deps:
        show_dependency_info(missing_deps, available_optional)
        return 0
    
    if args.install_deps:
        install_optional_dependencies()
        return 0
    
    # Show dependency info
    if not show_dependency_info(missing_deps, available_optional):
        return 1
    
    # Show splash screen
    if not args.no_splash:
        try:
            show_startup_splash()
        except Exception as e:
            print(f"Splash screen failed: {e}")
    
    # Print banner
    print_banner()
    
    # Determine launch mode
    launch_mode = args.mode
    if launch_mode == 'auto':
        # Auto-detect best mode based on available dependencies
        advanced_available = all([
            available_optional.get('matplotlib', False),
            available_optional.get('numpy', False)
        ])
        launch_mode = 'advanced' if advanced_available else 'basic'
    
    print(f"Launching in {launch_mode} mode...")
    
    # Launch appropriate GUI
    if launch_mode == 'advanced':
        return launch_advanced_gui()
    else:
        return launch_basic_gui()

if __name__ == '__main__':
    try:
        exit_code = main()
        sys.exit(exit_code)
    except KeyboardInterrupt:
        print("\nApplication interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"Unexpected error: {e}")
        sys.exit(1)
