"""
CyberRotate Pro - Plugin System
Extensible plugin architecture for custom providers and features
"""

import os
import json
import importlib
import importlib.util
from abc import ABC, abstractmethod
from typing import Dict, List, Any, Optional, Type
from pathlib import Path
import logging
from dataclasses import dataclass

@dataclass
class PluginInfo:
    """Plugin information structure"""
    name: str
    version: str
    description: str
    author: str
    plugin_type: str
    enabled: bool = True
    config: Dict[str, Any] = None

class BasePlugin(ABC):
    """Base class for all plugins"""
    
    def __init__(self, config: Dict[str, Any] = None):
        self.config = config or {}
        self.logger = logging.getLogger(f"plugin.{self.__class__.__name__}")
    
    @abstractmethod
    def get_info(self) -> PluginInfo:
        """Return plugin information"""
        pass
    
    @abstractmethod
    def initialize(self) -> bool:
        """Initialize the plugin"""
        pass
    
    @abstractmethod
    def cleanup(self):
        """Cleanup plugin resources"""
        pass
    
    def validate_config(self, config: Dict[str, Any]) -> bool:
        """Validate plugin configuration"""
        return True

class VPNProviderPlugin(BasePlugin):
    """Base class for VPN provider plugins"""
    
    @abstractmethod
    async def connect(self, server: str = None, country: str = None) -> Dict[str, Any]:
        """Connect to VPN server"""
        pass
    
    @abstractmethod
    async def disconnect(self) -> bool:
        """Disconnect from VPN"""
        pass
    
    @abstractmethod
    async def get_servers(self) -> List[Dict[str, Any]]:
        """Get available servers"""
        pass
    
    @abstractmethod
    async def get_status(self) -> Dict[str, Any]:
        """Get current connection status"""
        pass

class ProxyProviderPlugin(BasePlugin):
    """Base class for proxy provider plugins"""
    
    @abstractmethod
    async def get_proxies(self, proxy_type: str = 'http') -> List[Dict[str, Any]]:
        """Get available proxies"""
        pass
    
    @abstractmethod
    async def test_proxy(self, proxy: Dict[str, Any]) -> bool:
        """Test proxy connectivity"""
        pass
    
    @abstractmethod
    async def rotate_proxy(self) -> Dict[str, Any]:
        """Rotate to next proxy"""
        pass

class SecurityPlugin(BasePlugin):
    """Base class for security feature plugins"""
    
    @abstractmethod
    async def check_dns_leak(self) -> Dict[str, Any]:
        """Check for DNS leaks"""
        pass
    
    @abstractmethod
    async def check_ip_leak(self) -> Dict[str, Any]:
        """Check for IP leaks"""
        pass
    
    @abstractmethod
    async def enable_kill_switch(self) -> bool:
        """Enable kill switch protection"""
        pass

class PluginManager:
    """Manages plugin loading, initialization and execution"""
    
    def __init__(self, plugin_dir: str = "plugins"):
        self.plugin_dir = Path(plugin_dir)
        self.plugins: Dict[str, BasePlugin] = {}
        self.plugin_info: Dict[str, PluginInfo] = {}
        self.logger = logging.getLogger(__name__)
        
        # Create plugin directories
        self.plugin_dir.mkdir(exist_ok=True)
        (self.plugin_dir / "providers").mkdir(exist_ok=True)
        (self.plugin_dir / "security").mkdir(exist_ok=True)
        (self.plugin_dir / "protocols").mkdir(exist_ok=True)
        
        # Load plugin configurations
        self.config_file = self.plugin_dir / "config.json"
        self.load_config()
    
    def load_config(self):
        """Load plugin configuration"""
        if self.config_file.exists():
            try:
                with open(self.config_file, 'r') as f:
                    self.config = json.load(f)
            except Exception as e:
                self.logger.error(f"Failed to load plugin config: {e}")
                self.config = {}
        else:
            self.config = {}
    
    def save_config(self):
        """Save plugin configuration"""
        try:
            with open(self.config_file, 'w') as f:
                json.dump(self.config, f, indent=2)
        except Exception as e:
            self.logger.error(f"Failed to save plugin config: {e}")
    
    def discover_plugins(self) -> List[str]:
        """Discover available plugins"""
        plugins = []
        
        for plugin_dir in ['providers', 'security', 'protocols']:
            plugin_path = self.plugin_dir / plugin_dir
            if plugin_path.exists():
                for file_path in plugin_path.glob("*.py"):
                    if file_path.name != "__init__.py":
                        plugin_name = f"{plugin_dir}.{file_path.stem}"
                        plugins.append(plugin_name)
        
        return plugins
    
    def load_plugin(self, plugin_name: str) -> bool:
        """Load a specific plugin"""
        try:
            # Construct module path
            if '.' in plugin_name:
                plugin_dir, plugin_file = plugin_name.split('.', 1)
                module_path = self.plugin_dir / plugin_dir / f"{plugin_file}.py"
            else:
                module_path = self.plugin_dir / f"{plugin_name}.py"
            
            if not module_path.exists():
                self.logger.error(f"Plugin file not found: {module_path}")
                return False
            
            # Load module
            spec = importlib.util.spec_from_file_location(plugin_name, module_path)
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            
            # Find plugin class
            plugin_class = None
            for item_name in dir(module):
                item = getattr(module, item_name)
                if (isinstance(item, type) and 
                    issubclass(item, BasePlugin) and 
                    item != BasePlugin):
                    plugin_class = item
                    break
            
            if not plugin_class:
                self.logger.error(f"No plugin class found in {plugin_name}")
                return False
            
            # Get plugin configuration
            plugin_config = self.config.get(plugin_name, {})
            
            # Initialize plugin
            plugin_instance = plugin_class(plugin_config)
            
            # Validate configuration
            if not plugin_instance.validate_config(plugin_config):
                self.logger.error(f"Invalid configuration for plugin {plugin_name}")
                return False
            
            # Initialize plugin
            if not plugin_instance.initialize():
                self.logger.error(f"Failed to initialize plugin {plugin_name}")
                return False
            
            # Store plugin
            self.plugins[plugin_name] = plugin_instance
            self.plugin_info[plugin_name] = plugin_instance.get_info()
            
            self.logger.info(f"Loaded plugin: {plugin_name}")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to load plugin {plugin_name}: {e}")
            return False
    
    def unload_plugin(self, plugin_name: str) -> bool:
        """Unload a specific plugin"""
        try:
            if plugin_name in self.plugins:
                plugin = self.plugins[plugin_name]
                plugin.cleanup()
                del self.plugins[plugin_name]
                del self.plugin_info[plugin_name]
                self.logger.info(f"Unloaded plugin: {plugin_name}")
                return True
            return False
        except Exception as e:
            self.logger.error(f"Failed to unload plugin {plugin_name}: {e}")
            return False
    
    def reload_plugin(self, plugin_name: str) -> bool:
        """Reload a specific plugin"""
        self.unload_plugin(plugin_name)
        return self.load_plugin(plugin_name)
    
    def load_all_plugins(self):
        """Load all discovered plugins"""
        plugins = self.discover_plugins()
        
        for plugin_name in plugins:
            # Check if plugin is enabled
            plugin_config = self.config.get(plugin_name, {})
            if plugin_config.get('enabled', True):
                self.load_plugin(plugin_name)
    
    def get_plugins_by_type(self, plugin_type: Type[BasePlugin]) -> Dict[str, BasePlugin]:
        """Get all plugins of a specific type"""
        return {
            name: plugin for name, plugin in self.plugins.items()
            if isinstance(plugin, plugin_type)
        }
    
    def get_vpn_providers(self) -> Dict[str, VPNProviderPlugin]:
        """Get all VPN provider plugins"""
        return self.get_plugins_by_type(VPNProviderPlugin)
    
    def get_proxy_providers(self) -> Dict[str, ProxyProviderPlugin]:
        """Get all proxy provider plugins"""
        return self.get_plugins_by_type(ProxyProviderPlugin)
    
    def get_security_plugins(self) -> Dict[str, SecurityPlugin]:
        """Get all security plugins"""
        return self.get_plugins_by_type(SecurityPlugin)
    
    def enable_plugin(self, plugin_name: str) -> bool:
        """Enable a plugin"""
        try:
            if plugin_name not in self.config:
                self.config[plugin_name] = {}
            
            self.config[plugin_name]['enabled'] = True
            self.save_config()
            
            # Load if not already loaded
            if plugin_name not in self.plugins:
                return self.load_plugin(plugin_name)
            
            return True
        except Exception as e:
            self.logger.error(f"Failed to enable plugin {plugin_name}: {e}")
            return False
    
    def disable_plugin(self, plugin_name: str) -> bool:
        """Disable a plugin"""
        try:
            if plugin_name not in self.config:
                self.config[plugin_name] = {}
            
            self.config[plugin_name]['enabled'] = False
            self.save_config()
            
            # Unload if loaded
            if plugin_name in self.plugins:
                return self.unload_plugin(plugin_name)
            
            return True
        except Exception as e:
            self.logger.error(f"Failed to disable plugin {plugin_name}: {e}")
            return False
    
    def get_plugin_info(self, plugin_name: str = None) -> Optional[PluginInfo]:
        """Get plugin information"""
        if plugin_name:
            return self.plugin_info.get(plugin_name)
        else:
            return self.plugin_info
    
    def list_plugins(self) -> Dict[str, Dict[str, Any]]:
        """List all plugins with their status"""
        all_plugins = self.discover_plugins()
        plugin_list = {}
        
        for plugin_name in all_plugins:
            is_loaded = plugin_name in self.plugins
            is_enabled = self.config.get(plugin_name, {}).get('enabled', True)
            
            plugin_list[plugin_name] = {
                'loaded': is_loaded,
                'enabled': is_enabled,
                'info': self.plugin_info.get(plugin_name)
            }
        
        return plugin_list
    
    def cleanup_all(self):
        """Cleanup all loaded plugins"""
        for plugin_name in list(self.plugins.keys()):
            self.unload_plugin(plugin_name)

# Global plugin manager instance
plugin_manager = None

def get_plugin_manager() -> PluginManager:
    """Get global plugin manager instance"""
    global plugin_manager
    if plugin_manager is None:
        plugin_manager = PluginManager()
    return plugin_manager

if __name__ == "__main__":
    # Test plugin manager
    manager = PluginManager()
    
    # Create sample plugin structure
    os.makedirs("plugins/providers", exist_ok=True)
    os.makedirs("plugins/security", exist_ok=True)
    
    print("Plugin Manager initialized")
    print(f"Available plugins: {manager.discover_plugins()}")
    
    # Load all plugins
    manager.load_all_plugins()
    print(f"Loaded plugins: {list(manager.plugins.keys())}")
    
    # List plugin status
    plugin_list = manager.list_plugins()
    for name, status in plugin_list.items():
        print(f"{name}: {status}")
