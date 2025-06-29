"""
NordVPN Provider Plugin for CyberRotate Pro
Integrates with NordVPN services
"""

import asyncio
import subprocess
import json
import requests
from typing import Dict, List, Any
from plugins import VPNProviderPlugin, PluginInfo

class NordVPNPlugin(VPNProviderPlugin):
    """NordVPN provider implementation"""
    
    def __init__(self, config: Dict[str, Any] = None):
        super().__init__(config)
        self.username = config.get('username', '')
        self.password = config.get('password', '')
        self.current_server = None
        self.connected = False
        
    def get_info(self) -> PluginInfo:
        return PluginInfo(
            name="NordVPN Provider",
            version="1.0.0",
            description="Official NordVPN integration for CyberRotate Pro",
            author="ZehraSec",
            plugin_type="vpn_provider"
        )
    
    def initialize(self) -> bool:
        """Initialize NordVPN plugin"""
        try:
            # Check if NordVPN CLI is installed
            result = subprocess.run(['nordvpn', '--version'], 
                                  capture_output=True, text=True)
            if result.returncode != 0:
                self.logger.error("NordVPN CLI not found")
                return False
            
            # Login if credentials provided
            if self.username and self.password:
                result = subprocess.run(['nordvpn', 'login', '--username', self.username],
                                      input=self.password, text=True, capture_output=True)
                if result.returncode != 0:
                    self.logger.warning("Failed to login to NordVPN")
            
            self.logger.info("NordVPN plugin initialized successfully")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to initialize NordVPN plugin: {e}")
            return False
    
    def cleanup(self):
        """Cleanup NordVPN plugin"""
        try:
            if self.connected:
                asyncio.run(self.disconnect())
        except Exception as e:
            self.logger.error(f"Cleanup error: {e}")
    
    def validate_config(self, config: Dict[str, Any]) -> bool:
        """Validate NordVPN configuration"""
        # Username and password are optional (can use token auth)
        return True
    
    async def connect(self, server: str = None, country: str = None) -> Dict[str, Any]:
        """Connect to NordVPN server"""
        try:
            cmd = ['nordvpn', 'connect']
            
            if server:
                cmd.append(server)
            elif country:
                cmd.append(country)
            
            result = subprocess.run(cmd, capture_output=True, text=True)
            
            if result.returncode == 0:
                self.connected = True
                self.current_server = server or country or "auto"
                
                # Get connection status
                status = await self.get_status()
                
                return {
                    'success': True,
                    'server': self.current_server,
                    'ip': status.get('ip'),
                    'country': status.get('country'),
                    'message': 'Connected successfully'
                }
            else:
                return {
                    'success': False,
                    'message': result.stderr or 'Connection failed'
                }
                
        except Exception as e:
            self.logger.error(f"Connection error: {e}")
            return {
                'success': False,
                'message': str(e)
            }
    
    async def disconnect(self) -> bool:
        """Disconnect from NordVPN"""
        try:
            result = subprocess.run(['nordvpn', 'disconnect'], 
                                  capture_output=True, text=True)
            
            if result.returncode == 0:
                self.connected = False
                self.current_server = None
                return True
            else:
                self.logger.error(f"Disconnect failed: {result.stderr}")
                return False
                
        except Exception as e:
            self.logger.error(f"Disconnect error: {e}")
            return False
    
    async def get_servers(self) -> List[Dict[str, Any]]:
        """Get available NordVPN servers"""
        try:
            # Use NordVPN API to get server list
            response = requests.get('https://api.nordvpn.com/v1/servers/countries')
            
            if response.status_code == 200:
                countries = response.json()
                servers = []
                
                for country in countries:
                    servers.append({
                        'name': country['name'],
                        'code': country['code'],
                        'flag': country['flag'],
                        'cities': len(country.get('cities', []))
                    })
                
                return servers
            else:
                return []
                
        except Exception as e:
            self.logger.error(f"Failed to get servers: {e}")
            return []
    
    async def get_status(self) -> Dict[str, Any]:
        """Get current NordVPN connection status"""
        try:
            result = subprocess.run(['nordvpn', 'status'], 
                                  capture_output=True, text=True)
            
            if result.returncode == 0:
                output = result.stdout.strip()
                
                # Parse status output
                status = {
                    'connected': 'Connected' in output,
                    'server': None,
                    'country': None,
                    'city': None,
                    'ip': None,
                    'protocol': None
                }
                
                lines = output.split('\n')
                for line in lines:
                    if 'Current server:' in line:
                        status['server'] = line.split(':')[1].strip()
                    elif 'Country:' in line:
                        status['country'] = line.split(':')[1].strip()
                    elif 'City:' in line:
                        status['city'] = line.split(':')[1].strip()
                    elif 'Current IP:' in line:
                        status['ip'] = line.split(':')[1].strip()
                    elif 'Current protocol:' in line:
                        status['protocol'] = line.split(':')[1].strip()
                
                return status
            else:
                return {
                    'connected': False,
                    'message': 'Status check failed'
                }
                
        except Exception as e:
            self.logger.error(f"Status check error: {e}")
            return {
                'connected': False,
                'error': str(e)
            }
