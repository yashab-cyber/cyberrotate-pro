#!/usr/bin/env python3
"""
Logger - Advanced logging system for CyberRotate Pro
Created by Yashab Alam - Founder & CEO of ZehraSec
"""

import logging
import logging.handlers
import os
import sys
import time
from typing import Optional
from pathlib import Path
import json
from datetime import datetime

def setup_logger(name: str = "CyberRotate", 
                 debug: bool = False,
                 log_file: Optional[str] = None,
                 log_level: str = "INFO") -> logging.Logger:
    """
    Setup advanced logging system
    
    Args:
        name: Logger name
        debug: Enable debug mode
        log_file: Custom log file path
        log_level: Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        
    Returns:
        Configured logger instance
    """
    
    # Create logs directory
    log_dir = Path("data/logs")
    log_dir.mkdir(parents=True, exist_ok=True)
    
    # Configure log file
    if not log_file:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        log_file = log_dir / f"cyberrotate_{timestamp}.log"
    
    # Create logger
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG if debug else getattr(logging, log_level.upper()))
    
    # Clear existing handlers
    logger.handlers.clear()
    
    # Create formatters
    detailed_formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(filename)s:%(lineno)d - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    
    simple_formatter = logging.Formatter(
        '%(asctime)s - %(levelname)s - %(message)s',
        datefmt='%H:%M:%S'
    )
    
    # Console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(logging.DEBUG if debug else logging.INFO)
    console_handler.setFormatter(simple_formatter)
    logger.addHandler(console_handler)
    
    # File handler with rotation
    file_handler = logging.handlers.RotatingFileHandler(
        log_file,
        maxBytes=10*1024*1024,  # 10MB
        backupCount=5,
        encoding='utf-8'
    )
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(detailed_formatter)
    logger.addHandler(file_handler)
    
    # Error file handler
    error_log_file = log_dir / f"cyberrotate_errors_{datetime.now().strftime('%Y%m%d')}.log"
    error_handler = logging.FileHandler(error_log_file, encoding='utf-8')
    error_handler.setLevel(logging.ERROR)
    error_handler.setFormatter(detailed_formatter)
    logger.addHandler(error_handler)
    
    return logger

class SecurityLogger:
    """
    Security-focused logger for sensitive operations
    """
    
    def __init__(self, logger: logging.Logger):
        self.logger = logger
        self.security_log_file = Path("data/logs/security.log")
        self.security_log_file.parent.mkdir(parents=True, exist_ok=True)
        
        # Setup security file handler
        self.security_handler = logging.FileHandler(self.security_log_file, encoding='utf-8')
        self.security_handler.setLevel(logging.INFO)
        
        security_formatter = logging.Formatter(
            '%(asctime)s - SECURITY - %(levelname)s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        self.security_handler.setFormatter(security_formatter)
    
    def log_rotation(self, method: str, success: bool, ip_address: str = None):
        """Log IP rotation events"""
        event = {
            'type': 'ip_rotation',
            'method': method,
            'success': success,
            'ip_address': self._mask_ip(ip_address) if ip_address else None,
            'timestamp': time.time()
        }
        
        self._log_security_event(event)
    
    def log_connection_attempt(self, target: str, method: str, success: bool):
        """Log connection attempts"""
        event = {
            'type': 'connection_attempt',
            'target': self._sanitize_target(target),
            'method': method,
            'success': success,
            'timestamp': time.time()
        }
        
        self._log_security_event(event)
    
    def log_leak_detection(self, leak_type: str, details: dict):
        """Log leak detection events"""
        event = {
            'type': 'leak_detection',
            'leak_type': leak_type,
            'details': self._sanitize_details(details),
            'timestamp': time.time()
        }
        
        self._log_security_event(event)
    
    def log_security_violation(self, violation_type: str, details: str):
        """Log security violations"""
        event = {
            'type': 'security_violation',
            'violation_type': violation_type,
            'details': details,
            'timestamp': time.time()
        }
        
        self._log_security_event(event)
    
    def _log_security_event(self, event: dict):
        """Log security event to file"""
        try:
            with open(self.security_log_file, 'a', encoding='utf-8') as f:
                f.write(json.dumps(event) + '\n')
        except Exception as e:
            self.logger.error(f"Failed to write security log: {e}")
    
    def _mask_ip(self, ip_address: str) -> str:
        """Mask IP address for privacy"""
        if not ip_address:
            return None
        
        parts = ip_address.split('.')
        if len(parts) == 4:
            return f"{parts[0]}.{parts[1]}.{parts[2]}.xxx"
        else:
            return ip_address[:len(ip_address)//2] + 'x' * (len(ip_address)//2)
    
    def _sanitize_target(self, target: str) -> str:
        """Sanitize target information"""
        # Remove sensitive information from target
        if '@' in target:
            # Remove credentials from URLs
            parts = target.split('@')
            if len(parts) > 1:
                return f"***@{parts[-1]}"
        return target
    
    def _sanitize_details(self, details: dict) -> dict:
        """Sanitize sensitive details"""
        sanitized = {}
        sensitive_keys = ['password', 'token', 'key', 'secret', 'auth']
        
        for key, value in details.items():
            if any(sensitive in key.lower() for sensitive in sensitive_keys):
                sanitized[key] = '***'
            else:
                sanitized[key] = value
        
        return sanitized

class PerformanceLogger:
    """
    Performance monitoring logger
    """
    
    def __init__(self, logger: logging.Logger):
        self.logger = logger
        self.performance_data = []
        self.max_entries = 1000
    
    def log_operation_time(self, operation: str, duration: float, success: bool = True):
        """Log operation performance"""
        entry = {
            'operation': operation,
            'duration': duration,
            'success': success,
            'timestamp': time.time()
        }
        
        self.performance_data.append(entry)
        
        # Limit entries
        if len(self.performance_data) > self.max_entries:
            self.performance_data.pop(0)
        
        # Log slow operations
        if duration > 10.0:  # 10 seconds threshold
            self.logger.warning(f"Slow operation detected: {operation} took {duration:.2f}s")
    
    def get_performance_stats(self) -> dict:
        """Get performance statistics"""
        if not self.performance_data:
            return {}
        
        total_operations = len(self.performance_data)
        successful_operations = sum(1 for entry in self.performance_data if entry['success'])
        total_duration = sum(entry['duration'] for entry in self.performance_data)
        
        return {
            'total_operations': total_operations,
            'successful_operations': successful_operations,
            'success_rate': (successful_operations / total_operations) * 100,
            'average_duration': total_duration / total_operations,
            'total_duration': total_duration
        }
    
    def export_performance_data(self, filename: str) -> bool:
        """Export performance data to file"""
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump({
                    'performance_data': self.performance_data,
                    'statistics': self.get_performance_stats(),
                    'export_timestamp': time.time()
                }, f, indent=2)
            return True
        except Exception as e:
            self.logger.error(f"Failed to export performance data: {e}")
            return False

class AuditLogger:
    """
    Audit trail logger for compliance
    """
    
    def __init__(self, logger: logging.Logger):
        self.logger = logger
        self.audit_file = Path("data/logs/audit.log")
        self.audit_file.parent.mkdir(parents=True, exist_ok=True)
    
    def log_user_action(self, action: str, user: str = "system", details: dict = None):
        """Log user actions for audit trail"""
        audit_entry = {
            'timestamp': datetime.now().isoformat(),
            'user': user,
            'action': action,
            'details': details or {},
            'source_ip': self._get_source_ip()
        }
        
        self._write_audit_entry(audit_entry)
    
    def log_configuration_change(self, config_type: str, old_value: any, new_value: any, user: str = "system"):
        """Log configuration changes"""
        audit_entry = {
            'timestamp': datetime.now().isoformat(),
            'type': 'configuration_change',
            'config_type': config_type,
            'old_value': str(old_value),
            'new_value': str(new_value),
            'user': user
        }
        
        self._write_audit_entry(audit_entry)
    
    def log_access_attempt(self, resource: str, success: bool, user: str = "system"):
        """Log access attempts"""
        audit_entry = {
            'timestamp': datetime.now().isoformat(),
            'type': 'access_attempt',
            'resource': resource,
            'success': success,
            'user': user,
            'source_ip': self._get_source_ip()
        }
        
        self._write_audit_entry(audit_entry)
    
    def _write_audit_entry(self, entry: dict):
        """Write audit entry to file"""
        try:
            with open(self.audit_file, 'a', encoding='utf-8') as f:
                f.write(json.dumps(entry) + '\n')
        except Exception as e:
            self.logger.error(f"Failed to write audit entry: {e}")
    
    def _get_source_ip(self) -> str:
        """Get source IP address"""
        try:
            import socket
            hostname = socket.gethostname()
            return socket.gethostbyname(hostname)
        except:
            return "unknown"

def cleanup_old_logs(days_to_keep: int = 30):
    """Clean up old log files"""
    log_dir = Path("data/logs")
    if not log_dir.exists():
        return
    
    cutoff_time = time.time() - (days_to_keep * 24 * 60 * 60)
    
    for log_file in log_dir.glob("*.log*"):
        try:
            if log_file.stat().st_mtime < cutoff_time:
                log_file.unlink()
                print(f"Deleted old log file: {log_file}")
        except Exception as e:
            print(f"Error deleting log file {log_file}: {e}")

def get_log_summary() -> dict:
    """Get summary of log files"""
    log_dir = Path("data/logs")
    if not log_dir.exists():
        return {}
    
    summary = {
        'total_files': 0,
        'total_size': 0,
        'files': []
    }
    
    for log_file in log_dir.glob("*.log*"):
        try:
            stat = log_file.stat()
            summary['total_files'] += 1
            summary['total_size'] += stat.st_size
            summary['files'].append({
                'name': log_file.name,
                'size': stat.st_size,
                'modified': datetime.fromtimestamp(stat.st_mtime).isoformat()
            })
        except Exception as e:
            print(f"Error reading log file {log_file}: {e}")
    
    return summary

class Logger:
    """
    Main Logger class for CyberRotate Pro GUI and CLI applications
    Provides a unified interface for all logging operations
    """
    
    def __init__(self, name: str = "CyberRotate", debug: bool = False, log_file: Optional[str] = None):
        """Initialize logger with security, performance, and audit capabilities"""
        self.logger = setup_logger(name, debug, log_file)
        self.security_logger = SecurityLogger(self.logger)
        self.performance_logger = PerformanceLogger(self.logger)
        self.audit_logger = AuditLogger(self.logger)
    
    def debug(self, message: str):
        """Log debug message"""
        self.logger.debug(message)
    
    def info(self, message: str):
        """Log info message"""
        self.logger.info(message)
    
    def warning(self, message: str):
        """Log warning message"""
        self.logger.warning(message)
    
    def error(self, message: str):
        """Log error message"""
        self.logger.error(message)
    
    def critical(self, message: str):
        """Log critical message"""
        self.logger.critical(message)
    
    def log_rotation(self, method: str, success: bool, ip_address: str = None):
        """Log IP rotation events"""
        self.security_logger.log_rotation(method, success, ip_address)
    
    def log_connection_attempt(self, target: str, method: str, success: bool):
        """Log connection attempts"""
        self.security_logger.log_connection_attempt(target, method, success)
    
    def log_operation_time(self, operation: str, duration: float, success: bool = True):
        """Log operation performance"""
        self.performance_logger.log_operation_time(operation, duration, success)
    
    def log_user_action(self, action: str, user: str = "system", details: dict = None):
        """Log user actions for audit trail"""
        self.audit_logger.log_user_action(action, user, details)
    
    def get_performance_stats(self) -> dict:
        """Get performance statistics"""
        return self.performance_logger.get_performance_stats()
