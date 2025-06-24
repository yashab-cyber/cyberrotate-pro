#!/usr/bin/env python3
"""
Test script to verify CyberRotate Pro GUI functionality
"""

import os
import sys

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_imports():
    """Test all core module imports"""
    print("Testing imports...")
    
    try:
        from core.proxy_manager import ProxyManager
        print("✓ ProxyManager import successful")
    except Exception as e:
        print(f"✗ ProxyManager import failed: {e}")
        return False

    try:
        from core.openvpn_manager import OpenVPNManager
        print("✓ OpenVPNManager import successful")
    except Exception as e:
        print(f"✗ OpenVPNManager import failed: {e}")
        return False

    try:
        from core.tor_controller import TorController
        print("✓ TorController import successful")
    except Exception as e:
        print(f"✗ TorController import failed: {e}")
        return False

    try:
        from core.network_monitor import NetworkMonitor
        print("✓ NetworkMonitor import successful")
    except Exception as e:
        print(f"✗ NetworkMonitor import failed: {e}")
        return False

    try:
        from core.security_utils import SecurityUtils
        print("✓ SecurityUtils import successful")
    except Exception as e:
        print(f"✗ SecurityUtils import failed: {e}")
        return False

    try:
        from utils.logger import Logger
        print("✓ Logger import successful")
    except Exception as e:
        print(f"✗ Logger import failed: {e}")
        return False

    try:
        from utils.stats_collector import StatsCollector
        print("✓ StatsCollector import successful")
    except Exception as e:
        print(f"✗ StatsCollector import failed: {e}")
        return False

    try:
        from ui.gui_application import CyberRotateGUI
        print("✓ GUI Application import successful")
    except Exception as e:
        print(f"✗ GUI Application import failed: {e}")
        return False

    return True

def test_basic_functionality():
    """Test basic functionality without launching GUI"""
    print("\nTesting basic functionality...")
    
    try:
        from utils.logger import Logger
        logger = Logger("test")
        print("✓ Logger creation successful")
    except Exception as e:
        print(f"✗ Logger creation failed: {e}")
        return False

    try:
        from core.proxy_manager import ProxyManager
        proxy_manager = ProxyManager(logger.logger)
        print("✓ ProxyManager creation successful")
    except Exception as e:
        print(f"✗ ProxyManager creation failed: {e}")
        return False

    try:
        from core.network_monitor import NetworkMonitor
        network_monitor = NetworkMonitor(logger.logger)
        print("✓ NetworkMonitor creation successful")
    except Exception as e:
        print(f"✗ NetworkMonitor creation failed: {e}")
        return False

    return True

def main():
    """Main test function"""
    print("CyberRotate Pro - System Test")
    print("=" * 50)
    
    # Test imports
    if not test_imports():
        print("\n❌ Import tests failed!")
        return 1
    
    # Test basic functionality
    if not test_basic_functionality():
        print("\n❌ Basic functionality tests failed!")
        return 1
    
    print("\n✅ All tests passed!")
    print("The system is ready to run.")
    return 0

if __name__ == "__main__":
    exit(main())
