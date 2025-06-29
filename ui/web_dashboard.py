"""
CyberRotate Pro - Web Interface Dashboard
Modern React-style web interface for CyberRotate Pro
"""

from flask import Flask, render_template, request, jsonify, session, redirect, url_for, send_from_directory
from flask_socketio import SocketIO, emit
from flask_cors import CORS
import json
import os
import asyncio
from datetime import datetime, timedelta
import threading
import time
from pathlib import Path

# Import CyberRotate modules
from core.api_server_enterprise import app as api_app
from core.database_manager import get_database_manager
from core.license_manager import get_license_manager
from utils.logger import Logger
from utils.stats_collector import StatsCollector

app = Flask(__name__, 
           template_folder='ui/templates',
           static_folder='ui/static')
app.secret_key = os.environ.get('FLASK_SECRET_KEY', 'cyberrotate-pro-secret-key-change-in-production')

# Enable CORS for API integration
CORS(app, origins=['http://localhost:3000', 'http://localhost:8080'])

# Socket.IO for real-time updates
socketio = SocketIO(app, cors_allowed_origins="*")

# Initialize components
logger = Logger()
stats_collector = StatsCollector(logger.logger)
db_manager = get_database_manager()
license_manager = get_license_manager()

# Global state
current_status = {
    'connected': False,
    'service': None,
    'server': None,
    'ip_address': None,
    'country': None,
    'uptime': 0,
    'data_transferred': 0
}

@app.route('/')
def index():
    """Main dashboard page"""
    return render_template('dashboard.html')

@app.route('/dashboard')
def dashboard():
    """Dashboard page"""
    license_status = license_manager.get_license_status()
    return render_template('dashboard.html', license_status=license_status)

@app.route('/analytics')
def analytics():
    """Analytics page"""
    return render_template('analytics.html')

@app.route('/settings')
def settings():
    """Settings page"""
    return render_template('settings.html')

@app.route('/logs')
def logs():
    """Logs viewer page"""
    return render_template('logs.html')

@app.route('/api/status')
def api_status():
    """Get current system status"""
    try:
        # Get real-time stats
        stats = stats_collector.get_current_stats()
        
        # Get license status
        license_status = license_manager.get_license_status()
        
        return jsonify({
            'status': 'success',
            'data': {
                'connection': current_status,
                'stats': stats,
                'license': license_status,
                'timestamp': datetime.now().isoformat()
            }
        })
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500

@app.route('/api/analytics/overview')
def analytics_overview():
    """Get analytics overview"""
    try:
        # Get usage stats from database
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        
        stats_30d = loop.run_until_complete(db_manager.get_usage_stats(days=30))
        stats_7d = loop.run_until_complete(db_manager.get_usage_stats(days=7))
        stats_24h = loop.run_until_complete(db_manager.get_usage_stats(days=1))
        
        loop.close()
        
        return jsonify({
            'status': 'success',
            'data': {
                '30_days': stats_30d,
                '7_days': stats_7d,
                '24_hours': stats_24h,
                'timestamp': datetime.now().isoformat()
            }
        })
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500

@app.route('/api/logs')
def get_logs():
    """Get system logs"""
    try:
        log_level = request.args.get('level', 'INFO')
        limit = int(request.args.get('limit', 100))
        
        # Read logs from file or database
        logs = []
        log_file = Path('data/logs/cyberrotate.log')
        
        if log_file.exists():
            with open(log_file, 'r') as f:
                lines = f.readlines()[-limit:]
                for line in lines:
                    if line.strip():
                        logs.append({
                            'timestamp': datetime.now().isoformat(),
                            'level': log_level,
                            'message': line.strip()
                        })
        
        return jsonify({
            'status': 'success',
            'data': logs
        })
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500

@socketio.on('connect')
def handle_connect():
    """Handle client connection"""
    emit('status_update', current_status)

@socketio.on('request_status')
def handle_status_request():
    """Handle status request from client"""
    emit('status_update', current_status)

def broadcast_status_update():
    """Broadcast status updates to all connected clients"""
    while True:
        try:
            # Update current status
            stats = stats_collector.get_stats()
            current_status.update({
                'timestamp': datetime.now().isoformat(),
                'stats': stats
            })
            
            # Broadcast to all clients
            socketio.emit('status_update', current_status)
            
        except Exception as e:
            logger.error(f"Error broadcasting status: {e}")
        
        time.sleep(5)  # Update every 5 seconds

# Start background status broadcaster (commented out to prevent issues during import/testing)
# status_thread = threading.Thread(target=broadcast_status_update, daemon=True)
# status_thread.start()

class WebDashboard:
    """Web dashboard wrapper class for import compatibility"""
    
    def __init__(self):
        self.app = app
        self.socketio = socketio
        self.logger = logger
        self.stats_collector = stats_collector
    
    def run(self, host='0.0.0.0', port=3000, debug=False):
        """Run the web dashboard"""
        socketio.run(self.app, host=host, port=port, debug=debug)
