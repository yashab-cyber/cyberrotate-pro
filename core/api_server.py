#!/usr/bin/env python3
"""
CyberRotate Pro API Server
RESTful API for remote control and monitoring of IP rotation
"""

import json
import asyncio
from datetime import datetime
from typing import Dict, Any, Optional, List
from flask import Flask, request, jsonify, render_template_string
from flask_cors import CORS
import threading
import time

from utils.logger import Logger
from utils.stats_collector import StatsCollector
from core.proxy_manager import ProxyManager
from core.openvpn_manager import OpenVPNManager
from core.tor_controller import TorController
from core.network_monitor import NetworkMonitor
from core.security_utils import SecurityUtils

class CyberRotateAPI:
    """RESTful API server for CyberRotate Pro"""
    
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.app = Flask(__name__)
        CORS(self.app)
        
        # Initialize components
        self.logger = Logger("api_server")
        self.stats = StatsCollector()
        
        # Initialize managers
        self.proxy_manager = ProxyManager(config.get('proxy', {}))
        self.vpn_manager = OpenVPNManager(config.get('openvpn', {}))
        self.tor_controller = TorController(config.get('tor', {}))
        self.network_monitor = NetworkMonitor()
        self.security_utils = SecurityUtils()
        
        # API state
        self.is_running = False
        self.current_status = {
            'proxy': {'active': False, 'current': None},
            'vpn': {'active': False, 'current': None},
            'tor': {'active': False, 'current': None},
            'network': {'ip': None, 'location': None, 'dns_leak': False}
        }
        
        self.setup_routes()
        
    def setup_routes(self):
        """Setup API routes"""
        
        @self.app.route('/')
        def index():
            """API documentation"""
            return render_template_string(self.get_api_docs())
        
        @self.app.route('/api/status', methods=['GET'])
        def get_status():
            """Get current system status"""
            try:
                status = self.get_system_status()
                return jsonify({
                    'success': True,
                    'data': status,
                    'timestamp': datetime.now().isoformat()
                })
            except Exception as e:
                self.logger.error(f"Status check failed: {e}")
                return jsonify({
                    'success': False,
                    'error': str(e)
                }), 500
        
        @self.app.route('/api/proxy/rotate', methods=['POST'])
        def rotate_proxy():
            """Rotate to next proxy"""
            try:
                result = self.proxy_manager.rotate_proxy()
                if result:
                    self.current_status['proxy']['active'] = True
                    self.current_status['proxy']['current'] = result
                    return jsonify({
                        'success': True,
                        'data': result,
                        'message': 'Proxy rotated successfully'
                    })
                else:
                    return jsonify({
                        'success': False,
                        'error': 'Failed to rotate proxy'
                    }), 500
            except Exception as e:
                self.logger.error(f"Proxy rotation failed: {e}")
                return jsonify({
                    'success': False,
                    'error': str(e)
                }), 500
        
        @self.app.route('/api/proxy/list', methods=['GET'])
        def list_proxies():
            """List available proxies"""
            try:
                proxies = self.proxy_manager.get_proxy_list()
                return jsonify({
                    'success': True,
                    'data': proxies,
                    'count': len(proxies)
                })
            except Exception as e:
                return jsonify({
                    'success': False,
                    'error': str(e)
                }), 500
        
        @self.app.route('/api/vpn/connect', methods=['POST'])
        def connect_vpn():
            """Connect to VPN server"""
            try:
                data = request.get_json() or {}
                server = data.get('server')
                
                result = self.vpn_manager.connect(server)
                if result:
                    self.current_status['vpn']['active'] = True
                    self.current_status['vpn']['current'] = server
                    return jsonify({
                        'success': True,
                        'message': f'Connected to VPN server: {server}',
                        'server': server
                    })
                else:
                    return jsonify({
                        'success': False,
                        'error': 'Failed to connect to VPN'
                    }), 500
            except Exception as e:
                self.logger.error(f"VPN connection failed: {e}")
                return jsonify({
                    'success': False,
                    'error': str(e)
                }), 500
        
        @self.app.route('/api/vpn/disconnect', methods=['POST'])
        def disconnect_vpn():
            """Disconnect from VPN"""
            try:
                result = self.vpn_manager.disconnect()
                if result:
                    self.current_status['vpn']['active'] = False
                    self.current_status['vpn']['current'] = None
                    return jsonify({
                        'success': True,
                        'message': 'Disconnected from VPN'
                    })
                else:
                    return jsonify({
                        'success': False,
                        'error': 'Failed to disconnect from VPN'
                    }), 500
            except Exception as e:
                return jsonify({
                    'success': False,
                    'error': str(e)
                }), 500
        
        @self.app.route('/api/vpn/servers', methods=['GET'])
        def list_vpn_servers():
            """List available VPN servers"""
            try:
                servers = self.vpn_manager.get_server_list()
                return jsonify({
                    'success': True,
                    'data': servers,
                    'count': len(servers)
                })
            except Exception as e:
                return jsonify({
                    'success': False,
                    'error': str(e)
                }), 500
        
        @self.app.route('/api/tor/start', methods=['POST'])
        def start_tor():
            """Start Tor connection"""
            try:
                result = self.tor_controller.start()
                if result:
                    self.current_status['tor']['active'] = True
                    return jsonify({
                        'success': True,
                        'message': 'Tor started successfully'
                    })
                else:
                    return jsonify({
                        'success': False,
                        'error': 'Failed to start Tor'
                    }), 500
            except Exception as e:
                return jsonify({
                    'success': False,
                    'error': str(e)
                }), 500
        
        @self.app.route('/api/tor/stop', methods=['POST'])
        def stop_tor():
            """Stop Tor connection"""
            try:
                result = self.tor_controller.stop()
                if result:
                    self.current_status['tor']['active'] = False
                    return jsonify({
                        'success': True,
                        'message': 'Tor stopped successfully'
                    })
                else:
                    return jsonify({
                        'success': False,
                        'error': 'Failed to stop Tor'
                    }), 500
            except Exception as e:
                return jsonify({
                    'success': False,
                    'error': str(e)
                }), 500
        
        @self.app.route('/api/tor/new-identity', methods=['POST'])
        def new_tor_identity():
            """Get new Tor identity"""
            try:
                result = self.tor_controller.new_identity()
                if result:
                    return jsonify({
                        'success': True,
                        'message': 'New Tor identity acquired'
                    })
                else:
                    return jsonify({
                        'success': False,
                        'error': 'Failed to get new Tor identity'
                    }), 500
            except Exception as e:
                return jsonify({
                    'success': False,
                    'error': str(e)
                }), 500
        
        @self.app.route('/api/network/check', methods=['GET'])
        def check_network():
            """Check network status and detect leaks"""
            try:
                ip_info = self.network_monitor.get_public_ip()
                dns_check = self.network_monitor.check_dns_leaks()
                
                network_status = {
                    'ip': ip_info.get('ip'),
                    'location': ip_info.get('location'),
                    'isp': ip_info.get('isp'),
                    'dns_leak': not dns_check.get('secure', True),
                    'dns_servers': dns_check.get('servers', [])
                }
                
                self.current_status['network'] = network_status
                
                return jsonify({
                    'success': True,
                    'data': network_status
                })
            except Exception as e:
                return jsonify({
                    'success': False,
                    'error': str(e)
                }), 500
        
        @self.app.route('/api/stats', methods=['GET'])
        def get_stats():
            """Get usage statistics"""
            try:
                stats = self.stats.get_stats()
                return jsonify({
                    'success': True,
                    'data': stats
                })
            except Exception as e:
                return jsonify({
                    'success': False,
                    'error': str(e)
                }), 500
        
        @self.app.route('/api/config', methods=['GET'])
        def get_config():
            """Get current configuration (sanitized)"""
            try:
                # Return sanitized config without sensitive data
                safe_config = {
                    'proxy': {
                        'rotation_interval': self.config.get('proxy', {}).get('rotation_interval'),
                        'max_failures': self.config.get('proxy', {}).get('max_failures')
                    },
                    'openvpn': {
                        'timeout': self.config.get('openvpn', {}).get('timeout'),
                        'retry_attempts': self.config.get('openvpn', {}).get('retry_attempts')
                    },
                    'tor': {
                        'socks_port': self.config.get('tor', {}).get('socks_port'),
                        'control_port': self.config.get('tor', {}).get('control_port')
                    }
                }
                
                return jsonify({
                    'success': True,
                    'data': safe_config
                })
            except Exception as e:
                return jsonify({
                    'success': False,
                    'error': str(e)
                }), 500
    
    def get_system_status(self) -> Dict[str, Any]:
        """Get comprehensive system status"""
        try:
            # Update network status
            ip_info = self.network_monitor.get_public_ip()
            self.current_status['network']['ip'] = ip_info.get('ip')
            self.current_status['network']['location'] = ip_info.get('location')
            
            return {
                'services': self.current_status,
                'uptime': time.time() - self.stats.start_time,
                'stats': self.stats.get_stats(),
                'timestamp': datetime.now().isoformat()
            }
        except Exception as e:
            self.logger.error(f"Failed to get system status: {e}")
            return {'error': str(e)}
    
    def get_api_docs(self) -> str:
        """Generate API documentation HTML"""
        return """
        <!DOCTYPE html>
        <html>
        <head>
            <title>CyberRotate Pro API</title>
            <style>
                body { font-family: Arial, sans-serif; margin: 40px; }
                .endpoint { margin: 20px 0; padding: 15px; border: 1px solid #ddd; }
                .method { font-weight: bold; color: #0066cc; }
                .path { font-family: monospace; background: #f5f5f5; padding: 2px 4px; }
                .description { margin: 10px 0; }
            </style>
        </head>
        <body>
            <h1>CyberRotate Pro RESTful API</h1>
            <p>Advanced IP rotation and anonymity suite API</p>
            
            <div class="endpoint">
                <div class="method">GET</div>
                <div class="path">/api/status</div>
                <div class="description">Get current system status</div>
            </div>
            
            <div class="endpoint">
                <div class="method">POST</div>
                <div class="path">/api/proxy/rotate</div>
                <div class="description">Rotate to next proxy</div>
            </div>
            
            <div class="endpoint">
                <div class="method">GET</div>
                <div class="path">/api/proxy/list</div>
                <div class="description">List available proxies</div>
            </div>
            
            <div class="endpoint">
                <div class="method">POST</div>
                <div class="path">/api/vpn/connect</div>
                <div class="description">Connect to VPN server</div>
            </div>
            
            <div class="endpoint">
                <div class="method">POST</div>
                <div class="path">/api/vpn/disconnect</div>
                <div class="description">Disconnect from VPN</div>
            </div>
            
            <div class="endpoint">
                <div class="method">GET</div>
                <div class="path">/api/vpn/servers</div>
                <div class="description">List available VPN servers</div>
            </div>
            
            <div class="endpoint">
                <div class="method">POST</div>
                <div class="path">/api/tor/start</div>
                <div class="description">Start Tor connection</div>
            </div>
            
            <div class="endpoint">
                <div class="method">POST</div>
                <div class="path">/api/tor/stop</div>
                <div class="description">Stop Tor connection</div>
            </div>
            
            <div class="endpoint">
                <div class="method">POST</div>
                <div class="path">/api/tor/new-identity</div>
                <div class="description">Get new Tor identity</div>
            </div>
            
            <div class="endpoint">
                <div class="method">GET</div>
                <div class="path">/api/network/check</div>
                <div class="description">Check network status and detect leaks</div>
            </div>
            
            <div class="endpoint">
                <div class="method">GET</div>
                <div class="path">/api/stats</div>
                <div class="description">Get usage statistics</div>
            </div>
        </body>
        </html>
        """
    
    def start_server(self, host: str = '127.0.0.1', port: int = 8080, debug: bool = False):
        """Start the API server"""
        try:
            self.is_running = True
            self.logger.info(f"Starting CyberRotate Pro API server on {host}:{port}")
            self.app.run(host=host, port=port, debug=debug, threaded=True)
        except Exception as e:
            self.logger.error(f"Failed to start API server: {e}")
            self.is_running = False
            raise
    
    def stop_server(self):
        """Stop the API server"""
        self.is_running = False
        self.logger.info("API server stopped")

def main():
    """Main function for standalone API server"""
    import argparse
    
    parser = argparse.ArgumentParser(description='CyberRotate Pro API Server')
    parser.add_argument('--host', default='127.0.0.1', help='Host to bind to')
    parser.add_argument('--port', type=int, default=8080, help='Port to bind to')
    parser.add_argument('--debug', action='store_true', help='Enable debug mode')
    parser.add_argument('--config', default='config/config.json', help='Configuration file path')
    
    args = parser.parse_args()
    
    # Load configuration
    try:
        with open(args.config, 'r') as f:
            config = json.load(f)
    except Exception as e:
        print(f"Failed to load configuration: {e}")
        return 1
    
    # Start API server
    api = CyberRotateAPI(config)
    try:
        api.start_server(host=args.host, port=args.port, debug=args.debug)
    except KeyboardInterrupt:
        print("\nShutting down API server...")
        api.stop_server()
    except Exception as e:
        print(f"API server error: {e}")
        return 1
    
    return 0

if __name__ == '__main__':
    exit(main())
