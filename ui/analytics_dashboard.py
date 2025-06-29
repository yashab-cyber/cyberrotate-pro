#!/usr/bin/env python3
"""
CyberRotate Pro - Production Analytics Dashboard
Real-time monitoring and analytics for enterprise deployments
"""

import dash
from dash import dcc, html, Input, Output, callback_context
import plotly.graph_objs as go
import plotly.express as px
import pandas as pd
import sqlite3
import json
from datetime import datetime, timedelta
import threading
import time
from typing import Dict, List, Any
import os

from utils.logger import Logger
from utils.stats_collector import StatsCollector
from core.network_monitor import NetworkMonitor

class AnalyticsDashboard:
    """Production analytics dashboard for CyberRotate Pro"""
    
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.logger = Logger("dashboard", debug=config.get('debug', False))
        
        # Initialize Dash app
        self.app = dash.Dash(__name__, external_stylesheets=[
            'https://codepen.io/chriddyp/pen/bWLwgP.css',
            'https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css'
        ])
        
        # Initialize components
        self.stats_collector = StatsCollector(self.logger.logger)
        self.network_monitor = NetworkMonitor(self.logger.logger)
        
        # Database connection
        self.db_path = config.get('database_path', 'data/api_server.db')
        
        # Setup layout and callbacks
        self.setup_layout()
        self.setup_callbacks()
        
        # Start background data collection
        self.start_data_collection()
    
    def setup_layout(self):
        """Setup the dashboard layout"""
        self.app.layout = html.Div([
            # Header
            html.Div([
                html.H1([
                    html.I(className="fas fa-shield-alt", style={'margin-right': '10px'}),
                    "CyberRotate Pro - Production Dashboard"
                ], className="dashboard-title"),
                html.P("Real-time monitoring and analytics", className="dashboard-subtitle")
            ], className="header"),
            
            # Top metrics cards
            html.Div([
                html.Div([
                    html.Div([
                        html.I(className="fas fa-globe", style={'font-size': '2em', 'color': '#007bff'}),
                        html.H3(id="current-ip", children="Loading...", style={'margin': '10px 0'}),
                        html.P("Current IP Address", style={'margin': 0, 'color': '#666'})
                    ], className="metric-card")
                ], className="three columns"),
                
                html.Div([
                    html.Div([
                        html.I(className="fas fa-sync-alt", style={'font-size': '2em', 'color': '#28a745'}),
                        html.H3(id="rotation-count", children="0", style={'margin': '10px 0'}),
                        html.P("Total Rotations", style={'margin': 0, 'color': '#666'})
                    ], className="metric-card")
                ], className="three columns"),
                
                html.Div([
                    html.Div([
                        html.I(className="fas fa-chart-line", style={'font-size': '2em', 'color': '#ffc107'}),
                        html.H3(id="success-rate", children="0%", style={'margin': '10px 0'}),
                        html.P("Success Rate", style={'margin': 0, 'color': '#666'})
                    ], className="metric-card")
                ], className="three columns"),
                
                html.Div([
                    html.Div([
                        html.I(className="fas fa-clock", style={'font-size': '2em', 'color': '#dc3545'}),
                        html.H3(id="uptime", children="0h 0m", style={'margin': '10px 0'}),
                        html.P("System Uptime", style={'margin': 0, 'color': '#666'})
                    ], className="metric-card")
                ], className="three columns")
            ], className="row metrics-row"),
            
            # Charts section
            html.Div([
                # Rotation timeline
                html.Div([
                    html.H3("IP Rotation Timeline", className="chart-title"),
                    dcc.Graph(id="rotation-timeline")
                ], className="six columns chart-container"),
                
                # Service status
                html.Div([
                    html.H3("Service Status", className="chart-title"),
                    dcc.Graph(id="service-status")
                ], className="six columns chart-container")
            ], className="row"),
            
            html.Div([
                # Geographic distribution
                html.Div([
                    html.H3("Geographic Distribution", className="chart-title"),
                    dcc.Graph(id="geo-distribution")
                ], className="six columns chart-container"),
                
                # API usage
                html.Div([
                    html.H3("API Usage Statistics", className="chart-title"),
                    dcc.Graph(id="api-usage")
                ], className="six columns chart-container")
            ], className="row"),
            
            # Performance metrics
            html.Div([
                html.Div([
                    html.H3("Performance Metrics", className="chart-title"),
                    dcc.Graph(id="performance-metrics")
                ], className="twelve columns chart-container")
            ], className="row"),
            
            # Live logs section
            html.Div([
                html.H3("Live System Logs", className="chart-title"),
                html.Div(id="live-logs", className="logs-container")
            ], className="logs-section"),
            
            # Auto-refresh component
            dcc.Interval(
                id='interval-component',
                interval=5*1000,  # Update every 5 seconds
                n_intervals=0
            ),
            
            # Store for sharing data between callbacks
            dcc.Store(id='dashboard-data')
        ])
        
        # Custom CSS
        self.app.index_string = '''
        <!DOCTYPE html>
        <html>
            <head>
                {%metas%}
                <title>CyberRotate Pro Dashboard</title>
                {%favicon%}
                {%css%}
                <style>
                    body {
                        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                        margin: 0;
                        background-color: #f5f5f5;
                    }
                    .header {
                        background: linear-gradient(135deg, #007bff, #0056b3);
                        color: white;
                        padding: 20px;
                        text-align: center;
                        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
                    }
                    .dashboard-title {
                        margin: 0;
                        font-size: 2.5em;
                    }
                    .dashboard-subtitle {
                        margin: 10px 0 0 0;
                        opacity: 0.9;
                    }
                    .metrics-row {
                        margin: 20px 0;
                    }
                    .metric-card {
                        background: white;
                        padding: 20px;
                        border-radius: 8px;
                        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
                        text-align: center;
                        margin: 10px;
                    }
                    .chart-container {
                        background: white;
                        padding: 20px;
                        border-radius: 8px;
                        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
                        margin: 10px;
                    }
                    .chart-title {
                        margin-top: 0;
                        color: #333;
                        border-bottom: 2px solid #007bff;
                        padding-bottom: 10px;
                    }
                    .logs-section {
                        background: white;
                        margin: 20px 10px;
                        padding: 20px;
                        border-radius: 8px;
                        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
                    }
                    .logs-container {
                        background: #f8f9fa;
                        padding: 15px;
                        border-radius: 4px;
                        font-family: 'Courier New', monospace;
                        max-height: 300px;
                        overflow-y: auto;
                        border-left: 4px solid #007bff;
                    }
                    .log-entry {
                        margin: 5px 0;
                        padding: 5px;
                    }
                    .log-info { color: #007bff; }
                    .log-warning { color: #ffc107; }
                    .log-error { color: #dc3545; }
                </style>
            </head>
            <body>
                {%app_entry%}
                <footer>
                    {%config%}
                    {%scripts%}
                    {%renderer%}
                </footer>
            </body>
        </html>
        '''
    
    def setup_callbacks(self):
        """Setup dashboard callbacks"""
        
        @self.app.callback(
            [Output('current-ip', 'children'),
             Output('rotation-count', 'children'),
             Output('success-rate', 'children'),
             Output('uptime', 'children'),
             Output('dashboard-data', 'data')],
            [Input('interval-component', 'n_intervals')]
        )
        def update_metrics(n):
            """Update top-level metrics"""
            try:
                # Get current IP
                ip_info = self.network_monitor.get_public_ip()
                current_ip = ip_info if isinstance(ip_info, str) else ip_info.get('ip', 'Unknown') if ip_info else 'Unknown'
                
                # Get statistics
                stats = self.stats_collector.get_stats()
                rotation_stats = stats.get('rotations', {})
                
                rotation_count = rotation_stats.get('total', 0)
                success_rate = f"{rotation_stats.get('success_rate', 0):.1f}%"
                
                # Calculate uptime
                uptime_seconds = getattr(self, 'start_time', time.time())
                uptime_delta = timedelta(seconds=int(time.time() - uptime_seconds))
                uptime = f"{uptime_delta.days}d {uptime_delta.seconds//3600}h {(uptime_delta.seconds//60)%60}m"
                
                # Prepare data for other charts
                dashboard_data = {
                    'current_ip': current_ip,
                    'stats': stats,
                    'timestamp': datetime.now().isoformat()
                }
                
                return current_ip, rotation_count, success_rate, uptime, dashboard_data
                
            except Exception as e:
                self.logger.error(f"Error updating metrics: {e}")
                return "Error", "0", "0%", "0h 0m", {}
        
        @self.app.callback(
            Output('rotation-timeline', 'figure'),
            [Input('dashboard-data', 'data')]
        )
        def update_rotation_timeline(dashboard_data):
            """Update rotation timeline chart"""
            try:
                # Get rotation history from database
                rotation_data = self.get_rotation_history(hours=24)
                
                if not rotation_data:
                    return {
                        'data': [],
                        'layout': {
                            'title': 'No rotation data available',
                            'xaxis': {'title': 'Time'},
                            'yaxis': {'title': 'Rotations'},
                            'template': 'plotly_white'
                        }
                    }
                
                df = pd.DataFrame(rotation_data)
                df['timestamp'] = pd.to_datetime(df['timestamp'])
                
                # Group by hour
                hourly_data = df.groupby(df['timestamp'].dt.floor('H')).agg({
                    'success': ['count', 'sum']
                }).reset_index()
                
                hourly_data.columns = ['timestamp', 'total', 'successful']
                hourly_data['failed'] = hourly_data['total'] - hourly_data['successful']
                
                fig = go.Figure()
                
                fig.add_trace(go.Scatter(
                    x=hourly_data['timestamp'],
                    y=hourly_data['successful'],
                    mode='lines+markers',
                    name='Successful',
                    line=dict(color='#28a745')
                ))
                
                fig.add_trace(go.Scatter(
                    x=hourly_data['timestamp'],
                    y=hourly_data['failed'],
                    mode='lines+markers',
                    name='Failed',
                    line=dict(color='#dc3545')
                ))
                
                fig.update_layout(
                    title='IP Rotations (Last 24 Hours)',
                    xaxis_title='Time',
                    yaxis_title='Number of Rotations',
                    template='plotly_white',
                    hovermode='x unified'
                )
                
                return fig
                
            except Exception as e:
                self.logger.error(f"Error updating rotation timeline: {e}")
                return {'data': [], 'layout': {'title': 'Error loading data'}}
        
        @self.app.callback(
            Output('service-status', 'figure'),
            [Input('dashboard-data', 'data')]
        )
        def update_service_status(dashboard_data):
            """Update service status chart"""
            try:
                # Get service statuses
                services = ['Proxy', 'VPN', 'Tor', 'API Server']
                statuses = ['Active', 'Inactive', 'Active', 'Active']  # Mock data for now
                colors = ['#28a745' if status == 'Active' else '#dc3545' for status in statuses]
                
                fig = go.Figure(data=[go.Bar(
                    x=services,
                    y=[1 if status == 'Active' else 0 for status in statuses],
                    marker_color=colors,
                    text=statuses,
                    textposition='auto'
                )])
                
                fig.update_layout(
                    title='Service Status Overview',
                    xaxis_title='Services',
                    yaxis_title='Status',
                    template='plotly_white',
                    showlegend=False,
                    yaxis=dict(tickvals=[0, 1], ticktext=['Inactive', 'Active'])
                )
                
                return fig
                
            except Exception as e:
                return {'data': [], 'layout': {'title': 'Error loading service status'}}
        
        @self.app.callback(
            Output('geo-distribution', 'figure'),
            [Input('dashboard-data', 'data')]
        )
        def update_geo_distribution(dashboard_data):
            """Update geographic distribution chart"""
            try:
                # Mock geographic data for demonstration
                countries = ['United States', 'United Kingdom', 'Germany', 'Japan', 'Canada']
                usage = [45, 25, 15, 10, 5]
                
                fig = go.Figure(data=[go.Pie(
                    labels=countries,
                    values=usage,
                    hole=0.3,
                    marker_colors=px.colors.qualitative.Set3
                )])
                
                fig.update_layout(
                    title='Geographic Distribution of IP Addresses',
                    template='plotly_white'
                )
                
                return fig
                
            except Exception as e:
                return {'data': [], 'layout': {'title': 'Error loading geographic data'}}
        
        @self.app.callback(
            Output('api-usage', 'figure'),
            [Input('dashboard-data', 'data')]
        )
        def update_api_usage(dashboard_data):
            """Update API usage chart"""
            try:
                # Get API usage data
                api_data = self.get_api_usage_data(hours=24)
                
                if not api_data:
                    return {
                        'data': [],
                        'layout': {
                            'title': 'No API usage data available',
                            'template': 'plotly_white'
                        }
                    }
                
                endpoints = [item['endpoint'] for item in api_data]
                counts = [item['count'] for item in api_data]
                
                fig = go.Figure(data=[go.Bar(
                    x=counts,
                    y=endpoints,
                    orientation='h',
                    marker_color='#007bff'
                )])
                
                fig.update_layout(
                    title='API Endpoint Usage (Last 24 Hours)',
                    xaxis_title='Number of Requests',
                    yaxis_title='Endpoints',
                    template='plotly_white'
                )
                
                return fig
                
            except Exception as e:
                return {'data': [], 'layout': {'title': 'Error loading API usage data'}}
        
        @self.app.callback(
            Output('performance-metrics', 'figure'),
            [Input('dashboard-data', 'data')]
        )
        def update_performance_metrics(dashboard_data):
            """Update performance metrics chart"""
            try:
                # Mock performance data
                times = pd.date_range(start=datetime.now() - timedelta(hours=24), 
                                    end=datetime.now(), freq='H')
                cpu_usage = [20 + 10 * (0.5 - abs(0.5 - ((i/len(times)) % 1))) for i in range(len(times))]
                memory_usage = [30 + 15 * (0.5 - abs(0.5 - (((i+12)/len(times)) % 1))) for i in range(len(times))]
                
                fig = go.Figure()
                
                fig.add_trace(go.Scatter(
                    x=times,
                    y=cpu_usage,
                    mode='lines',
                    name='CPU Usage (%)',
                    line=dict(color='#007bff')
                ))
                
                fig.add_trace(go.Scatter(
                    x=times,
                    y=memory_usage,
                    mode='lines',
                    name='Memory Usage (%)',
                    line=dict(color='#28a745')
                ))
                
                fig.update_layout(
                    title='System Performance Metrics (Last 24 Hours)',
                    xaxis_title='Time',
                    yaxis_title='Usage (%)',
                    template='plotly_white',
                    hovermode='x unified'
                )
                
                return fig
                
            except Exception as e:
                return {'data': [], 'layout': {'title': 'Error loading performance data'}}
        
        @self.app.callback(
            Output('live-logs', 'children'),
            [Input('interval-component', 'n_intervals')]
        )
        def update_live_logs(n):
            """Update live logs display"""
            try:
                logs = self.get_recent_logs(limit=10)
                
                log_elements = []
                for log in logs:
                    level_class = f"log-{log['level'].lower()}"
                    log_elements.append(html.Div([
                        html.Span(f"[{log['timestamp']}] ", style={'color': '#666'}),
                        html.Span(f"{log['level']}: ", className=level_class),
                        html.Span(log['message'])
                    ], className="log-entry"))
                
                return log_elements
                
            except Exception as e:
                return [html.Div(f"Error loading logs: {e}", className="log-entry log-error")]
    
    def get_rotation_history(self, hours: int = 24) -> List[Dict[str, Any]]:
        """Get rotation history from database"""
        try:
            if not os.path.exists(self.db_path):
                return []
            
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                SELECT timestamp, success FROM rotation_history 
                WHERE timestamp >= datetime('now', '-{} hours')
                ORDER BY timestamp
            '''.format(hours))
            
            results = []
            for row in cursor.fetchall():
                results.append({
                    'timestamp': row[0],
                    'success': bool(row[1])
                })
            
            conn.close()
            return results
            
        except Exception as e:
            self.logger.error(f"Error getting rotation history: {e}")
            return []
    
    def get_api_usage_data(self, hours: int = 24) -> List[Dict[str, Any]]:
        """Get API usage data from database"""
        try:
            if not os.path.exists(self.db_path):
                return []
            
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                SELECT endpoint, COUNT(*) as count
                FROM api_usage 
                WHERE timestamp >= datetime('now', '-{} hours')
                GROUP BY endpoint
                ORDER BY count DESC
                LIMIT 10
            '''.format(hours))
            
            results = []
            for row in cursor.fetchall():
                results.append({
                    'endpoint': row[0],
                    'count': row[1]
                })
            
            conn.close()
            return results
            
        except Exception as e:
            self.logger.error(f"Error getting API usage data: {e}")
            return []
    
    def get_recent_logs(self, limit: int = 10) -> List[Dict[str, Any]]:
        """Get recent log entries"""
        try:
            # Read from log file
            log_file = os.path.join('data', 'logs', 'cyberrotate.log')
            if not os.path.exists(log_file):
                return []
            
            logs = []
            with open(log_file, 'r') as f:
                lines = f.readlines()
                for line in lines[-limit:]:
                    if line.strip():
                        parts = line.strip().split(' - ', 2)
                        if len(parts) >= 3:
                            logs.append({
                                'timestamp': parts[0],
                                'level': parts[1],
                                'message': parts[2]
                            })
            
            return logs
            
        except Exception as e:
            return [{'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'), 
                    'level': 'ERROR', 
                    'message': f'Error loading logs: {e}'}]
    
    def start_data_collection(self):
        """Start background data collection"""
        self.start_time = time.time()
        
        def collect_data():
            while True:
                try:
                    # Collect system metrics
                    self.stats_collector.get_stats()
                    time.sleep(30)  # Collect every 30 seconds
                except Exception as e:
                    self.logger.error(f"Data collection error: {e}")
                    time.sleep(60)
        
        collection_thread = threading.Thread(target=collect_data, daemon=True)
        collection_thread.start()
    
    def run(self, host='0.0.0.0', port=8050, debug=False):
        """Run the dashboard server"""
        self.logger.info(f"Starting CyberRotate Pro Dashboard on {host}:{port}")
        self.app.run_server(host=host, port=port, debug=debug)

def main():
    """Main function for running the dashboard"""
    import argparse
    
    parser = argparse.ArgumentParser(description='CyberRotate Pro Analytics Dashboard')
    parser.add_argument('--host', default='0.0.0.0', help='Host to bind to')
    parser.add_argument('--port', type=int, default=8050, help='Port to bind to')
    parser.add_argument('--debug', action='store_true', help='Enable debug mode')
    parser.add_argument('--config', default='config/dashboard_config.json', help='Configuration file')
    
    args = parser.parse_args()
    
    # Load configuration
    config = {'debug': args.debug}
    if os.path.exists(args.config):
        with open(args.config, 'r') as f:
            config.update(json.load(f))
    
    # Create and run dashboard
    dashboard = AnalyticsDashboard(config)
    dashboard.run(host=args.host, port=args.port, debug=args.debug)

if __name__ == '__main__':
    main()
