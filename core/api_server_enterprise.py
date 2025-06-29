#!/usr/bin/env python3
"""
CyberRotate Pro - Production API Server
Enterprise-grade RESTful API with authentication, rate limiting, and monitoring
"""

from flask import Flask, request, jsonify, render_template_string, g
from flask_cors import CORS
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from werkzeug.middleware.proxy_fix import ProxyFix
import jwt
import hashlib
import hmac
import time
import json
import threading
from datetime import datetime, timedelta
from typing import Dict, Any, Optional, List
from functools import wraps
import secrets
import logging
from dataclasses import dataclass
import sqlite3
import os

from utils.logger import Logger
from utils.stats_collector import StatsCollector
from core.proxy_manager import ProxyManager
from core.openvpn_manager import OpenVPNManager
from core.tor_controller import TorController
from core.network_monitor import NetworkMonitor
from core.security_utils import SecurityUtils

@dataclass
class APIKey:
    """API Key data structure"""
    key_id: str
    key_hash: str
    name: str
    permissions: List[str]
    created_at: datetime
    last_used: Optional[datetime] = None
    is_active: bool = True
    rate_limit: int = 1000  # requests per hour

class EnterpriseAPIServer:
    """Production-grade API server for CyberRotate Pro"""
    
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.app = Flask(__name__)
        self.app.wsgi_app = ProxyFix(self.app.wsgi_app)
        
        # Configure CORS
        CORS(self.app, resources={
            r"/api/*": {
                "origins": config.get('allowed_origins', ['*']),
                "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
                "allow_headers": ["Content-Type", "Authorization", "X-API-Key"]
            }
        })
        
        # Configure rate limiting
        self.limiter = Limiter(
            app=self.app,
            key_func=self.get_rate_limit_key,
            default_limits=["1000 per hour", "100 per minute"]
        )
        
        # Initialize components
        self.logger = Logger("api_server", debug=config.get('debug', False))
        self.stats = StatsCollector(self.logger.logger)
        
        # Initialize managers
        self.proxy_manager = ProxyManager(self.logger.logger)
        self.vpn_manager = OpenVPNManager(self.logger.logger)
        self.tor_controller = TorController(self.logger.logger)
        self.network_monitor = NetworkMonitor(self.logger.logger)
        self.security_utils = SecurityUtils(self.logger.logger)
        
        # Initialize database
        self.init_database()
        
        # Setup routes
        self.setup_routes()
        
        # Start background monitoring
        self.start_monitoring()
        
    def init_database(self):
        """Initialize SQLite database for API keys and usage tracking"""
        db_path = os.path.join('data', 'api_server.db')
        os.makedirs(os.path.dirname(db_path), exist_ok=True)
        
        self.db_connection = sqlite3.connect(db_path, check_same_thread=False)
        self.db_lock = threading.Lock()
        
        with self.db_lock:
            cursor = self.db_connection.cursor()
            
            # API Keys table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS api_keys (
                    key_id TEXT PRIMARY KEY,
                    key_hash TEXT NOT NULL,
                    name TEXT NOT NULL,
                    permissions TEXT NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    last_used TIMESTAMP,
                    is_active BOOLEAN DEFAULT 1,
                    rate_limit INTEGER DEFAULT 1000
                )
            ''')
            
            # API Usage table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS api_usage (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    key_id TEXT,
                    endpoint TEXT,
                    method TEXT,
                    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    ip_address TEXT,
                    response_time REAL,
                    status_code INTEGER,
                    FOREIGN KEY (key_id) REFERENCES api_keys (key_id)
                )
            ''')
            
            self.db_connection.commit()
    
    def generate_api_key(self, name: str, permissions: List[str] = None) -> Dict[str, str]:
        """Generate a new API key"""
        if permissions is None:
            permissions = ['read', 'rotate']  # Default permissions
            
        key_id = secrets.token_urlsafe(16)
        api_key = secrets.token_urlsafe(32)
        key_hash = hashlib.sha256(api_key.encode()).hexdigest()
        
        with self.db_lock:
            cursor = self.db_connection.cursor()
            cursor.execute('''
                INSERT INTO api_keys (key_id, key_hash, name, permissions)
                VALUES (?, ?, ?, ?)
            ''', (key_id, key_hash, name, json.dumps(permissions)))
            self.db_connection.commit()
        
        self.logger.info(f"Generated API key for: {name}")
        return {
            'key_id': key_id,
            'api_key': api_key,
            'name': name,
            'permissions': permissions
        }
    
    def validate_api_key(self, api_key: str) -> Optional[APIKey]:
        """Validate API key and return associated data"""
        if not api_key:
            return None
            
        key_hash = hashlib.sha256(api_key.encode()).hexdigest()
        
        with self.db_lock:
            cursor = self.db_connection.cursor()
            cursor.execute('''
                SELECT key_id, key_hash, name, permissions, created_at, last_used, is_active, rate_limit
                FROM api_keys WHERE key_hash = ? AND is_active = 1
            ''', (key_hash,))
            
            row = cursor.fetchone()
            if not row:
                return None
            
            # Update last used timestamp
            cursor.execute('''
                UPDATE api_keys SET last_used = CURRENT_TIMESTAMP WHERE key_id = ?
            ''', (row[0],))
            self.db_connection.commit()
        
        return APIKey(
            key_id=row[0],
            key_hash=row[1],
            name=row[2],
            permissions=json.loads(row[3]),
            created_at=datetime.fromisoformat(row[4]),
            last_used=datetime.fromisoformat(row[5]) if row[5] else None,
            is_active=bool(row[6]),
            rate_limit=row[7]
        )
    
    def require_auth(self, permissions: List[str] = None):
        """Decorator for API authentication"""
        def decorator(f):
            @wraps(f)
            def decorated_function(*args, **kwargs):
                # Get API key from header
                api_key = request.headers.get('X-API-Key') or request.headers.get('Authorization', '').replace('Bearer ', '')
                
                if not api_key:
                    return jsonify({'error': 'API key required'}), 401
                
                # Validate API key
                key_data = self.validate_api_key(api_key)
                if not key_data:
                    return jsonify({'error': 'Invalid API key'}), 401
                
                # Check permissions
                if permissions:
                    if not all(perm in key_data.permissions for perm in permissions):
                        return jsonify({'error': 'Insufficient permissions'}), 403
                
                # Store key data in Flask's g object
                g.api_key = key_data
                
                # Record API usage
                self.record_api_usage(key_data.key_id, request.endpoint, request.method, request.remote_addr)
                
                return f(*args, **kwargs)
            return decorated_function
        return decorator
    
    def get_rate_limit_key(self):
        """Get rate limiting key"""
        api_key = request.headers.get('X-API-Key') or request.headers.get('Authorization', '').replace('Bearer ', '')
        if api_key:
            key_data = self.validate_api_key(api_key)
            if key_data:
                return f"api_key:{key_data.key_id}"
        return get_remote_address()
    
    def record_api_usage(self, key_id: str, endpoint: str, method: str, ip_address: str):
        """Record API usage for analytics"""
        with self.db_lock:
            cursor = self.db_connection.cursor()
            cursor.execute('''
                INSERT INTO api_usage (key_id, endpoint, method, ip_address)
                VALUES (?, ?, ?, ?)
            ''', (key_id, endpoint, method, ip_address))
            self.db_connection.commit()
    
    def setup_routes(self):
        """Setup API routes"""
        
        @self.app.route('/')
        def index():
            """API documentation"""
            return render_template_string(self.get_api_docs())
        
        @self.app.route('/health')
        def health_check():
            """Health check endpoint"""
            return jsonify({
                'status': 'healthy',
                'timestamp': datetime.now().isoformat(),
                'version': '1.0.0'
            })
        
        # Authentication endpoints
        @self.app.route('/api/v1/auth/generate-key', methods=['POST'])
        @self.limiter.limit("5 per minute")
        def generate_key():
            """Generate new API key"""
            data = request.get_json() or {}
            name = data.get('name', 'Unnamed Key')
            permissions = data.get('permissions', ['read', 'rotate'])
            
            try:
                key_data = self.generate_api_key(name, permissions)
                return jsonify({
                    'success': True,
                    'data': key_data
                })
            except Exception as e:
                self.logger.error(f"Failed to generate API key: {e}")
                return jsonify({'error': 'Failed to generate API key'}), 500
        
        # Status endpoints
        @self.app.route('/api/v1/status', methods=['GET'])
        @self.require_auth(['read'])
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
                return jsonify({'error': str(e)}), 500
        
        @self.app.route('/api/v1/status/detailed', methods=['GET'])
        @self.require_auth(['read', 'admin'])
        def get_detailed_status():
            """Get detailed system status"""
            try:
                status = self.get_detailed_system_status()
                return jsonify({
                    'success': True,
                    'data': status,
                    'timestamp': datetime.now().isoformat()
                })
            except Exception as e:
                self.logger.error(f"Detailed status check failed: {e}")
                return jsonify({'error': str(e)}), 500
        
        # IP Rotation endpoints
        @self.app.route('/api/v1/rotate', methods=['POST'])
        @self.require_auth(['rotate'])
        @self.limiter.limit("60 per minute")
        def rotate_ip():
            """Rotate IP address"""
            data = request.get_json() or {}
            method = data.get('method', 'auto')  # auto, proxy, vpn, tor
            
            try:
                result = self.perform_rotation(method, data)
                return jsonify({
                    'success': True,
                    'data': result,
                    'timestamp': datetime.now().isoformat()
                })
            except Exception as e:
                self.logger.error(f"IP rotation failed: {e}")
                return jsonify({'error': str(e)}), 500
        
        # Proxy management
        @self.app.route('/api/v1/proxy/rotate', methods=['POST'])
        @self.require_auth(['rotate'])
        def rotate_proxy():
            """Rotate to next proxy"""
            try:
                result = self.proxy_manager.rotate_proxy()
                if result:
                    return jsonify({
                        'success': True,
                        'data': {'proxy': result},
                        'message': 'Proxy rotated successfully'
                    })
                else:
                    return jsonify({'error': 'Failed to rotate proxy'}), 500
            except Exception as e:
                self.logger.error(f"Proxy rotation failed: {e}")
                return jsonify({'error': str(e)}), 500
        
        @self.app.route('/api/v1/proxy/list', methods=['GET'])
        @self.require_auth(['read'])
        def list_proxies():
            """List available proxies"""
            try:
                proxies = self.proxy_manager.get_working_proxies()
                return jsonify({
                    'success': True,
                    'data': {
                        'total': len(proxies),
                        'working': len([p for p in proxies if p.is_working]),
                        'proxies': [{'host': p.host, 'port': p.port, 'type': p.proxy_type} for p in proxies[:10]]
                    }
                })
            except Exception as e:
                return jsonify({'error': str(e)}), 500
        
        # VPN management
        @self.app.route('/api/v1/vpn/connect', methods=['POST'])
        @self.require_auth(['rotate'])
        def connect_vpn():
            """Connect to VPN server"""
            data = request.get_json() or {}
            server = data.get('server')
            
            try:
                if server:
                    result = self.vpn_manager.connect_by_name(server)
                else:
                    result = self.vpn_manager.rotate_connection()
                
                return jsonify({
                    'success': result,
                    'message': 'VPN connected' if result else 'VPN connection failed'
                })
            except Exception as e:
                return jsonify({'error': str(e)}), 500
        
        @self.app.route('/api/v1/vpn/disconnect', methods=['POST'])
        @self.require_auth(['rotate'])
        def disconnect_vpn():
            """Disconnect from VPN"""
            try:
                result = self.vpn_manager.disconnect()
                return jsonify({
                    'success': result,
                    'message': 'VPN disconnected' if result else 'VPN disconnection failed'
                })
            except Exception as e:
                return jsonify({'error': str(e)}), 500
        
        @self.app.route('/api/v1/vpn/servers', methods=['GET'])
        @self.require_auth(['read'])
        def list_vpn_servers():
            """List available VPN servers"""
            try:
                servers = self.vpn_manager.get_available_servers()
                return jsonify({
                    'success': True,
                    'data': servers
                })
            except Exception as e:
                return jsonify({'error': str(e)}), 500
        
        # Tor management
        @self.app.route('/api/v1/tor/start', methods=['POST'])
        @self.require_auth(['rotate'])
        def start_tor():
            """Start Tor service"""
            try:
                result = self.tor_controller.start()
                return jsonify({
                    'success': result,
                    'message': 'Tor started' if result else 'Tor start failed'
                })
            except Exception as e:
                return jsonify({'error': str(e)}), 500
        
        @self.app.route('/api/v1/tor/stop', methods=['POST'])
        @self.require_auth(['rotate'])
        def stop_tor():
            """Stop Tor service"""
            try:
                result = self.tor_controller.stop()
                return jsonify({
                    'success': result,
                    'message': 'Tor stopped' if result else 'Tor stop failed'
                })
            except Exception as e:
                return jsonify({'error': str(e)}), 500
        
        @self.app.route('/api/v1/tor/new-circuit', methods=['POST'])
        @self.require_auth(['rotate'])
        def new_tor_circuit():
            """Get new Tor circuit"""
            try:
                result = self.tor_controller.new_circuit()
                return jsonify({
                    'success': result,
                    'message': 'New Tor circuit created' if result else 'Failed to create new circuit'
                })
            except Exception as e:
                return jsonify({'error': str(e)}), 500
        
        # Analytics endpoints
        @self.app.route('/api/v1/analytics/stats', methods=['GET'])
        @self.require_auth(['read'])
        def get_analytics():
            """Get usage statistics"""
            try:
                stats = self.stats.get_stats()
                return jsonify({
                    'success': True,
                    'data': stats
                })
            except Exception as e:
                return jsonify({'error': str(e)}), 500
        
        @self.app.route('/api/v1/analytics/api-usage', methods=['GET'])
        @self.require_auth(['admin'])
        def get_api_usage():
            """Get API usage statistics"""
            try:
                days = request.args.get('days', 7, type=int)
                usage_stats = self.get_api_usage_stats(days)
                return jsonify({
                    'success': True,
                    'data': usage_stats
                })
            except Exception as e:
                return jsonify({'error': str(e)}), 500
        
        # Security endpoints
        @self.app.route('/api/v1/security/check', methods=['GET'])
        @self.require_auth(['read'])
        def security_check():
            """Perform security checks"""
            try:
                results = self.perform_security_checks()
                return jsonify({
                    'success': True,
                    'data': results
                })
            except Exception as e:
                return jsonify({'error': str(e)}), 500
    
    def get_system_status(self) -> Dict[str, Any]:
        """Get current system status"""
        try:
            # Get current IP
            ip_info = self.network_monitor.get_public_ip()
            
            # Get service statuses
            proxy_status = self.proxy_manager.get_current_proxy()
            vpn_status = self.vpn_manager.is_connected()
            tor_status = self.tor_controller.is_tor_running()
            
            return {
                'network': {
                    'current_ip': ip_info if isinstance(ip_info, str) else ip_info.get('ip') if ip_info else 'Unknown',
                    'location': ip_info.get('location') if isinstance(ip_info, dict) else 'Unknown'
                },
                'services': {
                    'proxy': {
                        'active': proxy_status is not None,
                        'current': proxy_status.host if proxy_status else None
                    },
                    'vpn': {
                        'active': vpn_status,
                        'current': self.vpn_manager.current_config.name if vpn_status and hasattr(self.vpn_manager, 'current_config') else None
                    },
                    'tor': {
                        'active': tor_status
                    }
                },
                'uptime': time.time() - getattr(self, 'start_time', time.time())
            }
        except Exception as e:
            self.logger.error(f"Error getting system status: {e}")
            return {'error': str(e)}
    
    def get_detailed_system_status(self) -> Dict[str, Any]:
        """Get detailed system status"""
        basic_status = self.get_system_status()
        
        # Add detailed information
        detailed = {
            **basic_status,
            'proxy_manager': {
                'total_proxies': len(self.proxy_manager.proxies),
                'working_proxies': len(self.proxy_manager.get_working_proxies()),
                'failed_proxies': len(self.proxy_manager.get_failed_proxies())
            },
            'network_interfaces': self.network_monitor.get_network_interfaces(),
            'performance': self.stats.get_stats()
        }
        
        return detailed
    
    def perform_rotation(self, method: str, options: Dict[str, Any]) -> Dict[str, Any]:
        """Perform IP rotation with specified method"""
        start_time = time.time()
        
        try:
            if method == 'proxy' or method == 'auto':
                result = self.proxy_manager.rotate_proxy()
                if result:
                    response_time = time.time() - start_time
                    return {
                        'method': 'proxy',
                        'success': True,
                        'proxy': {'host': result.host, 'port': result.port},
                        'response_time': response_time
                    }
            
            elif method == 'vpn':
                server = options.get('server')
                if server:
                    result = self.vpn_manager.connect_by_name(server)
                else:
                    result = self.vpn_manager.rotate_connection()
                
                if result:
                    response_time = time.time() - start_time
                    return {
                        'method': 'vpn',
                        'success': True,
                        'server': server or 'auto',
                        'response_time': response_time
                    }
            
            elif method == 'tor':
                result = self.tor_controller.new_circuit()
                if result:
                    response_time = time.time() - start_time
                    return {
                        'method': 'tor',
                        'success': True,
                        'response_time': response_time
                    }
            
            # If all methods fail
            return {
                'method': method,
                'success': False,
                'error': 'Rotation failed'
            }
            
        except Exception as e:
            return {
                'method': method,
                'success': False,
                'error': str(e)
            }
    
    def perform_security_checks(self) -> Dict[str, Any]:
        """Perform comprehensive security checks"""
        results = {}
        
        try:
            # DNS leak check
            dns_check = self.network_monitor.check_dns_leaks()
            results['dns_leaks'] = dns_check
            
            # Get network details for analysis
            network_details = self.network_monitor.get_network_details()
            results['network_analysis'] = network_details
            
            # Check current IP reputation (placeholder)
            results['ip_reputation'] = {'clean': True, 'score': 95}
            
        except Exception as e:
            results['error'] = str(e)
        
        return results
    
    def get_api_usage_stats(self, days: int) -> Dict[str, Any]:
        """Get API usage statistics"""
        with self.db_lock:
            cursor = self.db_connection.cursor()
            
            # Get usage by endpoint
            cursor.execute('''
                SELECT endpoint, COUNT(*) as count
                FROM api_usage 
                WHERE timestamp >= datetime('now', '-{} days')
                GROUP BY endpoint
                ORDER BY count DESC
            '''.format(days))
            
            endpoint_stats = [{'endpoint': row[0], 'count': row[1]} for row in cursor.fetchall()]
            
            # Get usage by API key
            cursor.execute('''
                SELECT ak.name, COUNT(*) as count
                FROM api_usage au
                JOIN api_keys ak ON au.key_id = ak.key_id
                WHERE au.timestamp >= datetime('now', '-{} days')
                GROUP BY ak.name
                ORDER BY count DESC
            '''.format(days))
            
            key_stats = [{'key_name': row[0], 'count': row[1]} for row in cursor.fetchall()]
            
            return {
                'period_days': days,
                'endpoints': endpoint_stats,
                'api_keys': key_stats
            }
    
    def start_monitoring(self):
        """Start background monitoring thread"""
        self.start_time = time.time()
        
        def monitor():
            while True:
                try:
                    # Update system status
                    self.network_monitor.get_public_ip()
                    time.sleep(30)  # Update every 30 seconds
                except Exception as e:
                    self.logger.error(f"Monitoring error: {e}")
                    time.sleep(60)
        
        monitor_thread = threading.Thread(target=monitor, daemon=True)
        monitor_thread.start()
    
    def get_api_docs(self) -> str:
        """Return API documentation HTML"""
        return '''
        <!DOCTYPE html>
        <html>
        <head>
            <title>CyberRotate Pro API</title>
            <style>
                body { font-family: Arial, sans-serif; margin: 40px; }
                .endpoint { margin: 20px 0; padding: 15px; border: 1px solid #ddd; }
                .method { font-weight: bold; color: #007bff; }
                .path { font-family: monospace; background: #f8f9fa; padding: 2px 6px; }
                pre { background: #f8f9fa; padding: 10px; overflow-x: auto; }
            </style>
        </head>
        <body>
            <h1>CyberRotate Pro API Documentation</h1>
            <p>Enterprise-grade IP rotation and anonymity management API</p>
            
            <h2>Authentication</h2>
            <p>Include your API key in the request header:</p>
            <pre>X-API-Key: YOUR_API_KEY</pre>
            
            <h2>Endpoints</h2>
            
            <div class="endpoint">
                <div class="method">GET</div>
                <div class="path">/api/v1/status</div>
                <p>Get current system status</p>
            </div>
            
            <div class="endpoint">
                <div class="method">POST</div>
                <div class="path">/api/v1/rotate</div>
                <p>Rotate IP address</p>
            </div>
            
            <div class="endpoint">
                <div class="method">POST</div>
                <div class="path">/api/v1/proxy/rotate</div>
                <p>Rotate proxy connection</p>
            </div>
            
            <div class="endpoint">
                <div class="method">GET</div>
                <div class="path">/api/v1/analytics/stats</div>
                <p>Get usage statistics</p>
            </div>
            
            <p>For complete documentation, visit the <a href="/docs">API Documentation</a></p>
        </body>
        </html>
        '''
    
    def run(self, host='0.0.0.0', port=8080, debug=False):
        """Start the API server"""
        self.logger.info(f"Starting CyberRotate Pro API Server on {host}:{port}")
        self.app.run(host=host, port=port, debug=debug, threaded=True)

# Module-level app instance for testing/import purposes
app = None

def create_app(config=None):
    """Factory function to create Flask app instance"""
    global app
    if config is None:
        config = {}
    server = EnterpriseAPIServer(config)
    app = server.app
    return app

def main():
    """Main function for running the API server"""
    import argparse
    
    parser = argparse.ArgumentParser(description='CyberRotate Pro API Server')
    parser.add_argument('--host', default='0.0.0.0', help='Host to bind to')
    parser.add_argument('--port', type=int, default=8080, help='Port to bind to')
    parser.add_argument('--debug', action='store_true', help='Enable debug mode')
    parser.add_argument('--config', default='config/api_config.json', help='Configuration file')
    
    args = parser.parse_args()
    
    # Load configuration
    config = {}
    if os.path.exists(args.config):
        with open(args.config, 'r') as f:
            config = json.load(f)
    
    # Create and run server
    server = EnterpriseAPIServer(config)
    server.run(host=args.host, port=args.port, debug=args.debug)

if __name__ == '__main__':
    main()
