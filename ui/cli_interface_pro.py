#!/usr/bin/env python3
"""
CyberRotate Pro - Enhanced CLI Interface
Production-ready command-line interface with enterprise features
"""

import click
import json
import time
import sys
import os
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional
from pathlib import Path
import requests
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.text import Text

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.proxy_manager import ProxyManager
from core.openvpn_manager import OpenVPNManager
from core.tor_controller import TorController
from core.network_monitor import NetworkMonitor
from core.security_utils import SecurityUtils
from core.api_server_enterprise import EnterpriseAPIServer
from utils.logger import Logger
from utils.stats_collector import StatsCollector

console = Console()

class ProCLIInterface:
    """Enhanced CLI interface for CyberRotate Pro"""
    
    def __init__(self):
        self.config_file = "config/config.json"
        self.api_base_url = "http://localhost:8080/api/v1"
        self.api_key = None
        self.logger = Logger("cli")
        
        # Load configuration
        self.config = self.load_config()
        
        # Initialize components
        self.proxy_manager = ProxyManager(self.logger.logger)
        self.vpn_manager = OpenVPNManager(self.logger.logger)
        self.tor_controller = TorController(self.logger.logger)
        self.network_monitor = NetworkMonitor(self.logger.logger)
        self.security_utils = SecurityUtils(self.logger.logger)
        self.stats_collector = StatsCollector(self.logger.logger)
    
    def load_config(self) -> Dict[str, Any]:
        """Load configuration from file"""
        try:
            with open(self.config_file, 'r') as f:
                return json.load(f)
        except Exception as e:
            console.print(f"[red]Failed to load config: {e}[/red]")
            return {}
    
    def load_api_key(self) -> Optional[str]:
        """Load API key from file or environment"""
        # Try environment variable first
        api_key = os.environ.get('CYBERROTATE_API_KEY')
        if api_key:
            return api_key
        
        # Try config file
        api_key_file = Path('data/api_key.txt')
        if api_key_file.exists():
            return api_key_file.read_text().strip()
        
        return None
    
    def make_api_request(self, endpoint: str, method: str = 'GET', data: Dict = None) -> Dict:
        """Make API request to CyberRotate Pro server"""
        if not self.api_key:
            self.api_key = self.load_api_key()
        
        headers = {
            'Content-Type': 'application/json',
            'X-API-Key': self.api_key
        } if self.api_key else {'Content-Type': 'application/json'}
        
        url = f"{self.api_base_url}/{endpoint.lstrip('/')}"
        
        try:
            if method.upper() == 'GET':
                response = requests.get(url, headers=headers)
            elif method.upper() == 'POST':
                response = requests.post(url, headers=headers, json=data or {})
            elif method.upper() == 'PUT':
                response = requests.put(url, headers=headers, json=data or {})
            elif method.upper() == 'DELETE':
                response = requests.delete(url, headers=headers)
            else:
                raise ValueError(f"Unsupported HTTP method: {method}")
            
            response.raise_for_status()
            return response.json()
        except requests.exceptions.ConnectionError:
            console.print("[red]Could not connect to CyberRotate Pro API server[/red]")
            console.print("Make sure the server is running: python core/api_server_enterprise.py")
            sys.exit(1)
        except requests.exceptions.RequestException as e:
            console.print(f"[red]API request failed: {e}[/red]")
            sys.exit(1)

@click.group()
@click.option('--config', default='config/config.json', help='Configuration file path')
@click.option('--api-url', default='http://localhost:8080/api/v1', help='API server URL')
@click.option('--api-key', help='API key for authentication')
@click.pass_context
def cli(ctx, config, api_url, api_key):
    """CyberRotate Pro - Professional IP Rotation & Anonymity Suite"""
    ctx.ensure_object(dict)
    ctx.obj['config_file'] = config
    ctx.obj['api_url'] = api_url
    ctx.obj['api_key'] = api_key
    
    # Create CLI instance
    cli_instance = ProCLIInterface()
    if api_key:
        cli_instance.api_key = api_key
    cli_instance.api_base_url = api_url
    cli_instance.config_file = config
    ctx.obj['cli'] = cli_instance

@cli.command()
@click.pass_context
def version(ctx):
    """Show version information"""
    console.print(Panel.fit(
        "[bold blue]CyberRotate Pro v1.0.0[/bold blue]\n"
        "[cyan]Professional IP Rotation & Anonymity Suite[/cyan]\n"
        "[dim]Created by Yashab Alam - ZehraSec[/dim]",
        title="Version Information"
    ))

@cli.command()
@click.pass_context
def status(ctx):
    """Show system status"""
    cli_obj = ctx.obj['cli']
    
    with console.status("[bold green]Checking system status..."):
        try:
            # Try API first
            response = cli_obj.make_api_request('status')
            data = response.get('data', {})
            
            # Create status table
            table = Table(title="CyberRotate Pro System Status", show_header=True)
            table.add_column("Component", style="cyan")
            table.add_column("Status", style="green")
            table.add_column("Details", style="white")
            
            # Network status
            network = data.get('network', {})
            table.add_row(
                "Current IP",
                "✓ Active",
                network.get('current_ip', 'Unknown')
            )
            
            # Services status
            services = data.get('services', {})
            
            proxy_status = services.get('proxy', {})
            proxy_active = "✓ Active" if proxy_status.get('active') else "✗ Inactive"
            proxy_details = proxy_status.get('current') or 'None'
            table.add_row("Proxy Service", proxy_active, proxy_details)
            
            vpn_status = services.get('vpn', {})
            vpn_active = "✓ Connected" if vpn_status.get('active') else "✗ Disconnected"
            vpn_details = vpn_status.get('current') or 'None'
            table.add_row("VPN Service", vpn_active, vpn_details)
            
            tor_status = services.get('tor', {})
            tor_active = "✓ Running" if tor_status.get('active') else "✗ Stopped"
            table.add_row("Tor Service", tor_active, "Ready")
            
            # Uptime
            uptime = data.get('uptime', 0)
            uptime_str = str(timedelta(seconds=int(uptime)))
            table.add_row("System Uptime", "✓ Running", uptime_str)
            
            console.print(table)
            
        except Exception as e:
            # Fallback to direct component check
            console.print(f"[yellow]API unavailable, checking components directly...[/yellow]")
            
            table = Table(title="CyberRotate Pro System Status (Direct Check)")
            table.add_column("Component", style="cyan")
            table.add_column("Status", style="green")
            
            # Check current IP
            try:
                ip_info = cli_obj.network_monitor.get_public_ip()
                current_ip = ip_info if isinstance(ip_info, str) else ip_info.get('ip') if ip_info else 'Unknown'
                table.add_row("Current IP", f"✓ {current_ip}")
            except:
                table.add_row("Current IP", "✗ Error")
            
            # Check services
            try:
                proxy_current = cli_obj.proxy_manager.get_current_proxy()
                proxy_status = "✓ Active" if proxy_current else "✗ Inactive"
                table.add_row("Proxy Service", proxy_status)
            except:
                table.add_row("Proxy Service", "✗ Error")
            
            try:
                vpn_connected = cli_obj.vpn_manager.is_connected()
                vpn_status = "✓ Connected" if vpn_connected else "✗ Disconnected"
                table.add_row("VPN Service", vpn_status)
            except:
                table.add_row("VPN Service", "✗ Error")
            
            try:
                tor_running = cli_obj.tor_controller.is_tor_running()
                tor_status = "✓ Running" if tor_running else "✗ Stopped"
                table.add_row("Tor Service", tor_status)
            except:
                table.add_row("Tor Service", "✗ Error")
            
            console.print(table)

@cli.command()
@click.option('--method', type=click.Choice(['auto', 'proxy', 'vpn', 'tor']), default='auto', help='Rotation method')
@click.option('--server', help='Specific VPN server to connect to')
@click.pass_context
def rotate(ctx, method, server):
    """Rotate IP address"""
    cli_obj = ctx.obj['cli']
    
    with console.status(f"[bold green]Rotating IP using {method} method..."):
        try:
            # Prepare request data
            data = {'method': method}
            if server:
                data['server'] = server
            
            # Make API request
            response = cli_obj.make_api_request('rotate', 'POST', data)
            
            if response.get('success'):
                result_data = response.get('data', {})
                console.print(f"[green]✓ IP rotation successful![/green]")
                console.print(f"Method: {result_data.get('method', method)}")
                if 'response_time' in result_data:
                    console.print(f"Response time: {result_data['response_time']:.2f}s")
            else:
                console.print(f"[red]✗ IP rotation failed: {response.get('error', 'Unknown error')}[/red]")
                
        except Exception as e:
            console.print(f"[red]✗ Rotation error: {e}[/red]")

@cli.group()
def proxy():
    """Proxy management commands"""
    pass

@proxy.command()
@click.pass_context
def list(ctx):
    """List available proxies"""
    cli_obj = ctx.obj['cli']
    
    try:
        response = cli_obj.make_api_request('proxy/list')
        data = response.get('data', {})
        
        table = Table(title="Available Proxies")
        table.add_column("Host", style="cyan")
        table.add_column("Port", style="green")
        table.add_column("Type", style="yellow")
        
        for proxy in data.get('proxies', []):
            table.add_row(
                proxy.get('host', 'Unknown'),
                str(proxy.get('port', 'Unknown')),
                proxy.get('type', 'Unknown')
            )
        
        console.print(table)
        console.print(f"Total proxies: {data.get('total', 0)}")
        console.print(f"Working proxies: {data.get('working', 0)}")
        
    except Exception as e:
        console.print(f"[red]Error listing proxies: {e}[/red]")

@proxy.command()
@click.pass_context
def rotate(ctx):
    """Rotate to next proxy"""
    cli_obj = ctx.obj['cli']
    
    with console.status("[bold green]Rotating proxy..."):
        try:
            response = cli_obj.make_api_request('proxy/rotate', 'POST')
            
            if response.get('success'):
                console.print("[green]✓ Proxy rotated successfully![/green]")
            else:
                console.print(f"[red]✗ Proxy rotation failed: {response.get('error')}[/red]")
                
        except Exception as e:
            console.print(f"[red]Error rotating proxy: {e}[/red]")

@cli.group()
def vpn():
    """VPN management commands"""
    pass

@vpn.command()
@click.pass_context
def servers(ctx):
    """List available VPN servers"""
    cli_obj = ctx.obj['cli']
    
    try:
        response = cli_obj.make_api_request('vpn/servers')
        servers = response.get('data', [])
        
        table = Table(title="Available VPN Servers")
        table.add_column("Name", style="cyan")
        table.add_column("Country", style="green")
        table.add_column("City", style="yellow")
        table.add_column("Server", style="white")
        
        for server in servers:
            table.add_row(
                server.get('name', 'Unknown'),
                server.get('country', 'Unknown'),
                server.get('city', 'Unknown'),
                server.get('server', 'Unknown')
            )
        
        console.print(table)
        
    except Exception as e:
        console.print(f"[red]Error listing VPN servers: {e}[/red]")

@vpn.command()
@click.argument('server', required=False)
@click.pass_context
def connect(ctx, server):
    """Connect to VPN server"""
    cli_obj = ctx.obj['cli']
    
    with console.status(f"[bold green]Connecting to VPN{' server: ' + server if server else ''}..."):
        try:
            data = {'server': server} if server else {}
            response = cli_obj.make_api_request('vpn/connect', 'POST', data)
            
            if response.get('success'):
                console.print("[green]✓ VPN connected successfully![/green]")
            else:
                console.print(f"[red]✗ VPN connection failed: {response.get('message')}[/red]")
                
        except Exception as e:
            console.print(f"[red]Error connecting to VPN: {e}[/red]")

@vpn.command()
@click.pass_context
def disconnect(ctx):
    """Disconnect from VPN"""
    cli_obj = ctx.obj['cli']
    
    with console.status("[bold green]Disconnecting from VPN..."):
        try:
            response = cli_obj.make_api_request('vpn/disconnect', 'POST')
            
            if response.get('success'):
                console.print("[green]✓ VPN disconnected successfully![/green]")
            else:
                console.print(f"[red]✗ VPN disconnection failed: {response.get('message')}[/red]")
                
        except Exception as e:
            console.print(f"[red]Error disconnecting VPN: {e}[/red]")

@cli.group()
def tor():
    """Tor network commands"""
    pass

@tor.command()
@click.pass_context
def start(ctx):
    """Start Tor service"""
    cli_obj = ctx.obj['cli']
    
    with console.status("[bold green]Starting Tor service..."):
        try:
            response = cli_obj.make_api_request('tor/start', 'POST')
            
            if response.get('success'):
                console.print("[green]✓ Tor service started successfully![/green]")
            else:
                console.print(f"[red]✗ Tor start failed: {response.get('message')}[/red]")
                
        except Exception as e:
            console.print(f"[red]Error starting Tor: {e}[/red]")

@tor.command()
@click.pass_context
def stop(ctx):
    """Stop Tor service"""
    cli_obj = ctx.obj['cli']
    
    with console.status("[bold green]Stopping Tor service..."):
        try:
            response = cli_obj.make_api_request('tor/stop', 'POST')
            
            if response.get('success'):
                console.print("[green]✓ Tor service stopped successfully![/green]")
            else:
                console.print(f"[red]✗ Tor stop failed: {response.get('message')}[/red]")
                
        except Exception as e:
            console.print(f"[red]Error stopping Tor: {e}[/red]")

@tor.command()
@click.pass_context
def circuit(ctx):
    """Create new Tor circuit"""
    cli_obj = ctx.obj['cli']
    
    with console.status("[bold green]Creating new Tor circuit..."):
        try:
            response = cli_obj.make_api_request('tor/new-circuit', 'POST')
            
            if response.get('success'):
                console.print("[green]✓ New Tor circuit created successfully![/green]")
            else:
                console.print(f"[red]✗ Circuit creation failed: {response.get('message')}[/red]")
                
        except Exception as e:
            console.print(f"[red]Error creating new circuit: {e}[/red]")

@cli.group()
def security():
    """Security and monitoring commands"""
    pass

@security.command()
@click.pass_context
def check(ctx):
    """Perform security checks"""
    cli_obj = ctx.obj['cli']
    
    with console.status("[bold green]Performing security checks..."):
        try:
            response = cli_obj.make_api_request('security/check')
            data = response.get('data', {})
            
            table = Table(title="Security Check Results")
            table.add_column("Check", style="cyan")
            table.add_column("Status", style="green")
            table.add_column("Details", style="white")
            
            # DNS leaks
            dns_leaks = data.get('dns_leaks', {})
            dns_status = "✗ Leak detected" if not dns_leaks.get('secure', True) else "✓ Secure"
            table.add_row("DNS Leaks", dns_status, "DNS queries are secure")
            
            # IP reputation
            ip_rep = data.get('ip_reputation', {})
            ip_status = "✓ Clean" if ip_rep.get('clean', True) else "✗ Flagged"
            ip_score = ip_rep.get('score', 'Unknown')
            table.add_row("IP Reputation", ip_status, f"Score: {ip_score}")
            
            console.print(table)
            
        except Exception as e:
            console.print(f"[red]Error performing security check: {e}[/red]")

@cli.group()
def analytics():
    """Analytics and statistics commands"""
    pass

@analytics.command()
@click.pass_context
def stats(ctx):
    """Show usage statistics"""
    cli_obj = ctx.obj['cli']
    
    try:
        response = cli_obj.make_api_request('analytics/stats')
        stats = response.get('data', {})
        
        # Display statistics
        for category, data in stats.items():
            console.print(f"\n[bold cyan]{category.upper()}[/bold cyan]")
            if isinstance(data, dict):
                for key, value in data.items():
                    console.print(f"  {key}: {value}")
            else:
                console.print(f"  {data}")
                
    except Exception as e:
        console.print(f"[red]Error fetching statistics: {e}[/red]")

@cli.group()
def server():
    """Server management commands"""
    pass

@server.command()
@click.option('--host', default='0.0.0.0', help='Host to bind to')
@click.option('--port', default=8080, help='Port to bind to')
@click.option('--debug', is_flag=True, help='Enable debug mode')
@click.pass_context
def start(ctx, host, port, debug):
    """Start API server"""
    console.print(f"[green]Starting CyberRotate Pro API Server on {host}:{port}[/green]")
    
    try:
        config = {}
        server = EnterpriseAPIServer(config)
        server.run(host=host, port=port, debug=debug)
    except KeyboardInterrupt:
        console.print("\n[yellow]Server stopped by user[/yellow]")
    except Exception as e:
        console.print(f"[red]Server error: {e}[/red]")

@cli.group()
def config():
    """Configuration management commands"""
    pass

@config.command()
@click.pass_context
def show(ctx):
    """Show current configuration"""
    cli_obj = ctx.obj['cli']
    
    try:
        with open(cli_obj.config_file, 'r') as f:
            config_data = json.load(f)
        
        console.print(Panel(
            json.dumps(config_data, indent=2),
            title=f"Configuration: {cli_obj.config_file}",
            expand=False
        ))
    except Exception as e:
        console.print(f"[red]Error reading configuration: {e}[/red]")

@config.command()
@click.argument('key')
@click.argument('value')
@click.pass_context
def set(ctx, key, value):
    """Set configuration value"""
    cli_obj = ctx.obj['cli']
    
    try:
        with open(cli_obj.config_file, 'r') as f:
            config_data = json.load(f)
        
        # Parse nested keys (e.g., "rotation_settings.interval")
        keys = key.split('.')
        current = config_data
        for k in keys[:-1]:
            if k not in current:
                current[k] = {}
            current = current[k]
        
        # Try to parse value as JSON, fallback to string
        try:
            current[keys[-1]] = json.loads(value)
        except json.JSONDecodeError:
            current[keys[-1]] = value
        
        with open(cli_obj.config_file, 'w') as f:
            json.dump(config_data, f, indent=2)
        
        console.print(f"[green]✓ Configuration updated: {key} = {value}[/green]")
        
    except Exception as e:
        console.print(f"[red]Error updating configuration: {e}[/red]")

@cli.command()
@click.pass_context
def dashboard(ctx):
    """Launch analytics dashboard"""
    console.print("[green]Launching CyberRotate Pro Dashboard...[/green]")
    console.print("Dashboard will be available at: http://localhost:8050")
    
    try:
        os.system("python ui/analytics_dashboard.py")
    except KeyboardInterrupt:
        console.print("\n[yellow]Dashboard stopped by user[/yellow]")
    except Exception as e:
        console.print(f"[red]Dashboard error: {e}[/red]")

if __name__ == '__main__':
    cli()
