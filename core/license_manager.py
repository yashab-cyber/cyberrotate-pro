"""
CyberRotate Pro - License Management System
Enterprise-grade license validation and management
"""

import json
import datetime
import hashlib
import hmac
import base64
import uuid
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass, asdict
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
import requests
import time
import threading
from pathlib import Path

@dataclass
class LicenseInfo:
    """License information structure"""
    license_key: str
    license_type: str
    organization: str
    max_users: int
    features: List[str]
    issue_date: datetime.datetime
    expiry_date: datetime.datetime
    valid: bool = True
    last_validated: Optional[datetime.datetime] = None

class LicenseManager:
    """Enterprise license management system"""
    
    def __init__(self, license_server_url: str = None, local_cache_path: str = "data/license_cache.json"):
        self.license_server_url = license_server_url or "https://license.cyberrotate.pro/api/v1"
        self.local_cache_path = Path(local_cache_path)
        self.local_cache = {}
        self.validation_interval = 3600  # 1 hour
        self.encryption_key = self._get_encryption_key()
        self.license_info: Optional[LicenseInfo] = None
        
        # Load cached license data
        self._load_cache()
        
        # Start background validation thread
        self._start_validation_thread()
    
    def _get_encryption_key(self) -> bytes:
        """Generate encryption key from machine-specific data"""
        # Use machine-specific data for key derivation
        machine_id = self._get_machine_id()
        password = machine_id.encode()
        salt = b'cyberrotate_pro_license_salt'
        
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=100000,
        )
        return base64.urlsafe_b64encode(kdf.derive(password))
    
    def _get_machine_id(self) -> str:
        """Get unique machine identifier"""
        try:
            import platform
            import socket
            
            # Combine multiple machine identifiers
            machine_data = [
                platform.machine(),
                platform.processor(),
                platform.platform(),
                socket.gethostname(),
            ]
            
            # Create hash of combined data
            combined = ''.join(machine_data)
            return hashlib.sha256(combined.encode()).hexdigest()[:16]
        except Exception:
            # Fallback to random UUID if machine detection fails
            return str(uuid.uuid4())[:16]
    
    def _encrypt_data(self, data: str) -> str:
        """Encrypt sensitive data"""
        f = Fernet(self.encryption_key)
        return f.encrypt(data.encode()).decode()
    
    def _decrypt_data(self, encrypted_data: str) -> str:
        """Decrypt sensitive data"""
        f = Fernet(self.encryption_key)
        return f.decrypt(encrypted_data.encode()).decode()
    
    def _load_cache(self):
        """Load license cache from local storage"""
        try:
            if self.local_cache_path.exists():
                with open(self.local_cache_path, 'r') as f:
                    encrypted_cache = json.load(f)
                
                # Decrypt cache data
                for key, encrypted_value in encrypted_cache.items():
                    try:
                        decrypted_value = self._decrypt_data(encrypted_value)
                        self.local_cache[key] = json.loads(decrypted_value)
                    except Exception:
                        # Skip corrupted cache entries
                        continue
        except Exception as e:
            print(f"Warning: Could not load license cache: {e}")
    
    def _save_cache(self):
        """Save license cache to local storage"""
        try:
            # Ensure directory exists
            self.local_cache_path.parent.mkdir(parents=True, exist_ok=True)
            
            # Encrypt cache data
            encrypted_cache = {}
            for key, value in self.local_cache.items():
                json_value = json.dumps(value, default=str)
                encrypted_cache[key] = self._encrypt_data(json_value)
            
            with open(self.local_cache_path, 'w') as f:
                json.dump(encrypted_cache, f)
        except Exception as e:
            print(f"Warning: Could not save license cache: {e}")
    
    async def validate_license(self, license_key: str) -> LicenseInfo:
        """Validate license with license server"""
        try:
            # Check local cache first
            cached_license = self.local_cache.get(license_key)
            if cached_license and self._is_cache_valid(cached_license):
                return self._dict_to_license_info(cached_license)
            
            # Validate with license server
            response = await self._check_license_server(license_key)
            
            if response and response.get("valid"):
                license_info = LicenseInfo(
                    license_key=license_key,
                    license_type=response["license_type"],
                    organization=response["organization"],
                    max_users=response["max_users"],
                    features=response["enabled_features"],
                    issue_date=datetime.datetime.fromisoformat(response["issue_date"]),
                    expiry_date=datetime.datetime.fromisoformat(response["expiry_date"]),
                    valid=True,
                    last_validated=datetime.datetime.now()
                )
                
                # Cache valid license
                self.local_cache[license_key] = asdict(license_info)
                self._save_cache()
                
                self.license_info = license_info
                return license_info
            else:
                raise Exception("Invalid license key")
                
        except Exception as e:
            # Fall back to cached license if server is unreachable
            if cached_license:
                print(f"License server unreachable, using cached license: {e}")
                return self._dict_to_license_info(cached_license)
            else:
                raise Exception(f"License validation failed: {e}")
    
    async def _check_license_server(self, license_key: str) -> Dict:
        """Check license with remote server"""
        try:
            machine_id = self._get_machine_id()
            timestamp = int(time.time())
            
            # Create request signature
            payload = f"{license_key}:{machine_id}:{timestamp}"
            signature = self._create_signature(payload)
            
            data = {
                "license_key": license_key,
                "machine_id": machine_id,
                "timestamp": timestamp,
                "signature": signature
            }
            
            response = requests.post(
                f"{self.license_server_url}/validate",
                json=data,
                timeout=10
            )
            
            if response.status_code == 200:
                return response.json()
            else:
                return {"valid": False, "error": "Invalid response from license server"}
                
        except Exception as e:
            return {"valid": False, "error": str(e)}
    
    def _create_signature(self, payload: str) -> str:
        """Create HMAC signature for license validation"""
        # Use machine ID as secret key
        secret = self._get_machine_id().encode()
        signature = hmac.new(secret, payload.encode(), hashlib.sha256).hexdigest()
        return signature
    
    def _is_cache_valid(self, cached_license: Dict) -> bool:
        """Check if cached license is still valid"""
        try:
            last_validated = datetime.datetime.fromisoformat(cached_license["last_validated"])
            expiry_date = datetime.datetime.fromisoformat(cached_license["expiry_date"])
            now = datetime.datetime.now()
            
            # Check if cache is not expired and license hasn't expired
            cache_expired = (now - last_validated).total_seconds() > self.validation_interval
            license_expired = now > expiry_date
            
            return not cache_expired and not license_expired
        except Exception:
            return False
    
    def _dict_to_license_info(self, license_dict: Dict) -> LicenseInfo:
        """Convert dictionary to LicenseInfo object"""
        return LicenseInfo(
            license_key=license_dict["license_key"],
            license_type=license_dict["license_type"],
            organization=license_dict["organization"],
            max_users=license_dict["max_users"],
            features=license_dict["features"],
            issue_date=datetime.datetime.fromisoformat(license_dict["issue_date"]),
            expiry_date=datetime.datetime.fromisoformat(license_dict["expiry_date"]),
            valid=license_dict["valid"],
            last_validated=datetime.datetime.fromisoformat(license_dict["last_validated"]) if license_dict["last_validated"] else None
        )
    
    def _start_validation_thread(self):
        """Start background thread for periodic license validation"""
        def validation_worker():
            while True:
                try:
                    if self.license_info:
                        # Re-validate current license
                        import asyncio
                        loop = asyncio.new_event_loop()
                        asyncio.set_event_loop(loop)
                        loop.run_until_complete(
                            self.validate_license(self.license_info.license_key)
                        )
                        loop.close()
                except Exception as e:
                    print(f"Background license validation failed: {e}")
                
                # Wait for next validation cycle
                time.sleep(self.validation_interval)
        
        thread = threading.Thread(target=validation_worker, daemon=True)
        thread.start()
    
    def get_license_info(self) -> Optional[LicenseInfo]:
        """Get current license information"""
        return self.license_info
    
    def is_feature_enabled(self, feature: str) -> bool:
        """Check if a specific feature is enabled"""
        if not self.license_info or not self.license_info.valid:
            return False
        
        return feature in self.license_info.features
    
    def get_max_users(self) -> int:
        """Get maximum allowed users"""
        if not self.license_info or not self.license_info.valid:
            return 1  # Default to single user
        
        return self.license_info.max_users
    
    def check_user_limit(self, current_users: int) -> bool:
        """Check if current user count is within license limit"""
        max_users = self.get_max_users()
        return current_users <= max_users
    
    def get_license_status(self) -> Dict:
        """Get comprehensive license status"""
        if not self.license_info:
            return {
                "status": "unlicensed",
                "message": "No valid license found"
            }
        
        now = datetime.datetime.now()
        days_until_expiry = (self.license_info.expiry_date - now).days
        
        if not self.license_info.valid:
            return {
                "status": "invalid",
                "message": "License is invalid"
            }
        elif days_until_expiry < 0:
            return {
                "status": "expired",
                "message": "License has expired",
                "expiry_date": self.license_info.expiry_date.isoformat()
            }
        elif days_until_expiry <= 30:
            return {
                "status": "expiring_soon",
                "message": f"License expires in {days_until_expiry} days",
                "expiry_date": self.license_info.expiry_date.isoformat(),
                "days_remaining": days_until_expiry
            }
        else:
            return {
                "status": "valid",
                "message": "License is valid",
                "license_type": self.license_info.license_type,
                "organization": self.license_info.organization,
                "max_users": self.license_info.max_users,
                "features": self.license_info.features,
                "expiry_date": self.license_info.expiry_date.isoformat(),
                "days_remaining": days_until_expiry
            }

# Global license manager instance
license_manager = None

def get_license_manager() -> LicenseManager:
    """Get global license manager instance"""
    global license_manager
    if license_manager is None:
        license_manager = LicenseManager()
    return license_manager

def require_license(feature: str = None):
    """Decorator to require valid license for function execution"""
    def decorator(func):
        def wrapper(*args, **kwargs):
            mgr = get_license_manager()
            
            if not mgr.license_info or not mgr.license_info.valid:
                raise Exception("Valid license required")
            
            if feature and not mgr.is_feature_enabled(feature):
                raise Exception(f"Feature '{feature}' not enabled in current license")
            
            return func(*args, **kwargs)
        return wrapper
    return decorator

def require_enterprise():
    """Decorator to require enterprise license"""
    return require_license("enterprise_features")

if __name__ == "__main__":
    # Test license manager
    mgr = LicenseManager()
    
    # Test with sample license key
    test_license = "CYBERROTATE-ENT-2024-SAMPLE-LICENSE-KEY"
    
    try:
        import asyncio
        license_info = asyncio.run(mgr.validate_license(test_license))
        print(f"License validated: {license_info}")
        print(f"License status: {mgr.get_license_status()}")
    except Exception as e:
        print(f"License validation failed: {e}")
