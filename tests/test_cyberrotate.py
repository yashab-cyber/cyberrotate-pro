#!/usr/bin/env python3
"""
Test suite for CyberRotate Pro
"""

import unittest
import sys
import os
import json
import tempfile
import shutil
from unittest.mock import Mock, patch, MagicMock

# Add the parent directory to sys.path to import our modules
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.proxy_manager import ProxyManager
from core.openvpn_manager import OpenVPNManager
from core.tor_controller import TorController
from core.network_monitor import NetworkMonitor
from core.security_utils import SecurityUtils
from utils.logger import Logger
from utils.stats_collector import StatsCollector

class TestProxyManager(unittest.TestCase):
    """Test cases for ProxyManager"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.config = {
            'proxy_files': {
                'http': 'test_http_proxies.txt',
                'socks': 'test_socks_proxies.txt'
            },
            'rotation_interval': 300,
            'max_failures': 3,
            'timeout': 30,
            'verify_ssl': False
        }
        
        # Create temporary directory for test files
        self.temp_dir = tempfile.mkdtemp()
        self.config['proxy_files']['http'] = os.path.join(self.temp_dir, 'http_proxies.txt')
        self.config['proxy_files']['socks'] = os.path.join(self.temp_dir, 'socks_proxies.txt')
        
        # Create test proxy files
        with open(self.config['proxy_files']['http'], 'w') as f:
            f.write("127.0.0.1:8080\n")
            f.write("192.168.1.100:3128\n")
        
        with open(self.config['proxy_files']['socks'], 'w') as f:
            f.write("127.0.0.1:1080\n")
            f.write("192.168.1.101:1080\n")
        
        self.proxy_manager = ProxyManager(self.config)
    
    def tearDown(self):
        """Clean up test fixtures"""
        shutil.rmtree(self.temp_dir)
    
    def test_load_proxies(self):
        """Test proxy loading functionality"""
        proxies = self.proxy_manager.load_proxies()
        self.assertGreater(len(proxies), 0)
        self.assertIn('http', proxies)
        self.assertIn('socks', proxies)
    
    def test_get_proxy_list(self):
        """Test getting proxy list"""
        proxy_list = self.proxy_manager.get_proxy_list()
        self.assertIsInstance(proxy_list, list)
        self.assertGreater(len(proxy_list), 0)
    
    def test_format_proxy_string(self):
        """Test proxy string formatting"""
        proxy = {'host': '127.0.0.1', 'port': 8080, 'type': 'http'}
        formatted = self.proxy_manager.format_proxy_string(proxy)
        self.assertEqual(formatted, '127.0.0.1:8080')
    
    @patch('requests.get')
    def test_test_proxy(self, mock_get):
        """Test proxy testing functionality"""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {'ip': '127.0.0.1'}
        mock_get.return_value = mock_response
        
        proxy = {'host': '127.0.0.1', 'port': 8080, 'type': 'http'}
        result = self.proxy_manager.test_proxy(proxy)
        self.assertTrue(result)

class TestOpenVPNManager(unittest.TestCase):
    """Test cases for OpenVPNManager"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.temp_dir = tempfile.mkdtemp()
        self.config = {
            'config_directory': self.temp_dir,
            'servers_file': os.path.join(self.temp_dir, 'servers.json'),
            'timeout': 30,
            'retry_attempts': 3
        }
        
        # Create test servers file
        servers_data = {
            'servers': [
                {
                    'name': 'test-server',
                    'config_file': 'test.ovpn',
                    'country': 'Test Country',
                    'city': 'Test City',
                    'server': 'test.example.com',
                    'port': 1194,
                    'protocol': 'udp'
                }
            ]
        }
        
        with open(self.config['servers_file'], 'w') as f:
            json.dump(servers_data, f)
        
        # Create test OpenVPN config file
        with open(os.path.join(self.temp_dir, 'test.ovpn'), 'w') as f:
            f.write("client\n")
            f.write("dev tun\n")
            f.write("proto udp\n")
            f.write("remote test.example.com 1194\n")
        
        self.vpn_manager = OpenVPNManager(self.config)
    
    def tearDown(self):
        """Clean up test fixtures"""
        shutil.rmtree(self.temp_dir)
    
    def test_load_servers(self):
        """Test server loading functionality"""
        servers = self.vpn_manager.load_servers()
        self.assertGreater(len(servers), 0)
        self.assertEqual(servers[0]['name'], 'test-server')
    
    def test_get_server_list(self):
        """Test getting server list"""
        server_list = self.vpn_manager.get_server_list()
        self.assertIsInstance(server_list, list)
        self.assertGreater(len(server_list), 0)
    
    def test_find_server_by_name(self):
        """Test finding server by name"""
        server = self.vpn_manager.find_server_by_name('test-server')
        self.assertIsNotNone(server)
        self.assertEqual(server['name'], 'test-server')
    
    def test_find_server_by_name_not_found(self):
        """Test finding non-existent server"""
        server = self.vpn_manager.find_server_by_name('non-existent')
        self.assertIsNone(server)

class TestTorController(unittest.TestCase):
    """Test cases for TorController"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.config = {
            'socks_port': 9050,
            'control_port': 9051,
            'control_password': 'test_password',
            'auto_start': False
        }
        self.tor_controller = TorController(self.config)
    
    def test_initialization(self):
        """Test Tor controller initialization"""
        self.assertEqual(self.tor_controller.socks_port, 9050)
        self.assertEqual(self.tor_controller.control_port, 9051)
        self.assertFalse(self.tor_controller.is_running)
    
    def test_get_socks_proxy(self):
        """Test SOCKS proxy configuration"""
        proxy = self.tor_controller.get_socks_proxy()
        expected = {
            'http': 'socks5://127.0.0.1:9050',
            'https': 'socks5://127.0.0.1:9050'
        }
        self.assertEqual(proxy, expected)

class TestNetworkMonitor(unittest.TestCase):
    """Test cases for NetworkMonitor"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.network_monitor = NetworkMonitor()
    
    @patch('requests.get')
    def test_get_public_ip(self, mock_get):
        """Test public IP retrieval"""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            'ip': '8.8.8.8',
            'country': 'US',
            'city': 'Mountain View'
        }
        mock_get.return_value = mock_response
        
        ip_info = self.network_monitor.get_public_ip()
        self.assertEqual(ip_info['ip'], '8.8.8.8')
        self.assertEqual(ip_info['country'], 'US')
    
    def test_is_valid_ip(self):
        """Test IP address validation"""
        self.assertTrue(self.network_monitor.is_valid_ip('192.168.1.1'))
        self.assertTrue(self.network_monitor.is_valid_ip('8.8.8.8'))
        self.assertFalse(self.network_monitor.is_valid_ip('256.256.256.256'))
        self.assertFalse(self.network_monitor.is_valid_ip('invalid'))

class TestSecurityUtils(unittest.TestCase):
    """Test cases for SecurityUtils"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.security_utils = SecurityUtils()
    
    def test_generate_session_id(self):
        """Test session ID generation"""
        session_id = self.security_utils.generate_session_id()
        self.assertIsInstance(session_id, str)
        self.assertGreater(len(session_id), 0)
    
    def test_hash_password(self):
        """Test password hashing"""
        password = "test_password"
        hashed = self.security_utils.hash_password(password)
        self.assertIsInstance(hashed, str)
        self.assertNotEqual(hashed, password)
    
    def test_verify_password(self):
        """Test password verification"""
        password = "test_password"
        hashed = self.security_utils.hash_password(password)
        self.assertTrue(self.security_utils.verify_password(password, hashed))
        self.assertFalse(self.security_utils.verify_password("wrong_password", hashed))

class TestLogger(unittest.TestCase):
    """Test cases for Logger"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.temp_dir = tempfile.mkdtemp()
        self.log_file = os.path.join(self.temp_dir, 'test.log')
        self.logger = Logger("test_logger", log_file=self.log_file)
    
    def tearDown(self):
        """Clean up test fixtures"""
        shutil.rmtree(self.temp_dir)
    
    def test_log_info(self):
        """Test info logging"""
        self.logger.info("Test info message")
        with open(self.log_file, 'r') as f:
            content = f.read()
            self.assertIn("Test info message", content)
            self.assertIn("INFO", content)
    
    def test_log_error(self):
        """Test error logging"""
        self.logger.error("Test error message")
        with open(self.log_file, 'r') as f:
            content = f.read()
            self.assertIn("Test error message", content)
            self.assertIn("ERROR", content)

class TestStatsCollector(unittest.TestCase):
    """Test cases for StatsCollector"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.stats_collector = StatsCollector()
    
    def test_increment_counter(self):
        """Test counter increment"""
        self.stats_collector.increment_counter('test_counter')
        stats = self.stats_collector.get_stats()
        self.assertEqual(stats['counters']['test_counter'], 1)
    
    def test_record_event(self):
        """Test event recording"""
        self.stats_collector.record_event('test_event', {'key': 'value'})
        stats = self.stats_collector.get_stats()
        self.assertIn('test_event', stats['events'])
    
    def test_get_stats(self):
        """Test statistics retrieval"""
        stats = self.stats_collector.get_stats()
        self.assertIsInstance(stats, dict)
        self.assertIn('uptime', stats)
        self.assertIn('counters', stats)
        self.assertIn('events', stats)

class TestIntegration(unittest.TestCase):
    """Integration tests"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.temp_dir = tempfile.mkdtemp()
        self.config = {
            'proxy': {
                'proxy_files': {
                    'http': os.path.join(self.temp_dir, 'http_proxies.txt'),
                    'socks': os.path.join(self.temp_dir, 'socks_proxies.txt')
                },
                'rotation_interval': 300,
                'max_failures': 3,
                'timeout': 30,
                'verify_ssl': False
            },
            'openvpn': {
                'config_directory': self.temp_dir,
                'servers_file': os.path.join(self.temp_dir, 'servers.json'),
                'timeout': 30,
                'retry_attempts': 3
            },
            'tor': {
                'socks_port': 9050,
                'control_port': 9051,
                'auto_start': False
            }
        }
        
        # Create test files
        with open(self.config['proxy']['proxy_files']['http'], 'w') as f:
            f.write("127.0.0.1:8080\n")
        
        with open(self.config['proxy']['proxy_files']['socks'], 'w') as f:
            f.write("127.0.0.1:1080\n")
        
        servers_data = {'servers': []}
        with open(self.config['openvpn']['servers_file'], 'w') as f:
            json.dump(servers_data, f)
    
    def tearDown(self):
        """Clean up test fixtures"""
        shutil.rmtree(self.temp_dir)
    
    def test_component_initialization(self):
        """Test that all components can be initialized"""
        proxy_manager = ProxyManager(self.config['proxy'])
        vpn_manager = OpenVPNManager(self.config['openvpn'])
        tor_controller = TorController(self.config['tor'])
        network_monitor = NetworkMonitor()
        security_utils = SecurityUtils()
        
        self.assertIsNotNone(proxy_manager)
        self.assertIsNotNone(vpn_manager)
        self.assertIsNotNone(tor_controller)
        self.assertIsNotNone(network_monitor)
        self.assertIsNotNone(security_utils)

def run_tests():
    """Run all tests"""
    # Discover and run all tests
    loader = unittest.TestLoader()
    start_dir = os.path.dirname(__file__)
    suite = loader.discover(start_dir, pattern='test_*.py')
    
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    return result.wasSuccessful()

if __name__ == '__main__':
    success = run_tests()
    sys.exit(0 if success else 1)
