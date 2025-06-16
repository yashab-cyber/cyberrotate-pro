#!/usr/bin/env python3
"""
Stats Collector - Collects and analyzes rotation statistics
Created by Yashab Alam - Founder & CEO of ZehraSec
"""

import time
import json
import logging
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, asdict
from collections import defaultdict, deque
from pathlib import Path
import threading
import statistics

@dataclass
class RotationEvent:
    """Single rotation event data"""
    timestamp: float
    method: str
    success: bool
    response_time: float
    ip_address: Optional[str] = None
    country: Optional[str] = None
    error_message: Optional[str] = None

@dataclass
class MethodStats:
    """Statistics for a specific rotation method"""
    total_attempts: int = 0
    successful_attempts: int = 0
    failed_attempts: int = 0
    total_response_time: float = 0.0
    min_response_time: float = float('inf')
    max_response_time: float = 0.0
    last_success_time: Optional[float] = None
    last_failure_time: Optional[float] = None
    consecutive_failures: int = 0

class StatsCollector:
    """
    Statistics Collector and Analyzer
    
    Collects, stores, and analyzes rotation statistics including:
    - Success/failure rates
    - Response times
    - Method performance
    - Historical trends
    """
    
    def __init__(self, logger: logging.Logger):
        """Initialize stats collector"""
        self.logger = logger
        self.events = deque(maxlen=10000)  # Keep last 10k events
        self.method_stats = defaultdict(MethodStats)
        self.session_start_time = time.time()
        
        # Thread safety
        self._lock = threading.Lock()
        
        # Configuration
        self.stats_file = Path("data/stats/rotation_stats.json")
        self.stats_file.parent.mkdir(parents=True, exist_ok=True)
        
        # Load existing statistics
        self._load_stats()
        
        self.logger.info("Stats Collector initialized")
    
    def record_rotation(self, method: str, success: bool, response_time: float, 
                       ip_address: Optional[str] = None, country: Optional[str] = None,
                       error_message: Optional[str] = None):
        """Record a rotation event"""
        with self._lock:
            event = RotationEvent(
                timestamp=time.time(),
                method=method,
                success=success,
                response_time=response_time,
                ip_address=ip_address,
                country=country,
                error_message=error_message
            )
            
            self.events.append(event)
            self._update_method_stats(event)
            
            if len(self.events) % 100 == 0:  # Save every 100 events
                self._save_stats()
            
            self.logger.debug(f"Recorded rotation: {method} - {'Success' if success else 'Failed'}")
    
    def _update_method_stats(self, event: RotationEvent):
        """Update statistics for a specific method"""
        stats = self.method_stats[event.method]
        
        stats.total_attempts += 1
        
        if event.success:
            stats.successful_attempts += 1
            stats.last_success_time = event.timestamp
            stats.consecutive_failures = 0  # Reset consecutive failures
        else:
            stats.failed_attempts += 1
            stats.last_failure_time = event.timestamp
            stats.consecutive_failures += 1
        
        # Update response time statistics
        if event.response_time > 0:
            stats.total_response_time += event.response_time
            stats.min_response_time = min(stats.min_response_time, event.response_time)
            stats.max_response_time = max(stats.max_response_time, event.response_time)
    
    def get_stats(self) -> Dict[str, Any]:
        """Get comprehensive statistics"""
        with self._lock:
            current_time = time.time()
            session_duration = current_time - self.session_start_time
            
            # Overall statistics
            total_events = len(self.events)
            successful_events = sum(1 for event in self.events if event.success)
            failed_events = total_events - successful_events
            
            # Response time statistics
            response_times = [event.response_time for event in self.events if event.response_time > 0]
            avg_response_time = statistics.mean(response_times) if response_times else 0
            median_response_time = statistics.median(response_times) if response_times else 0
            
            # Method statistics
            method_stats = {}
            for method, stats in self.method_stats.items():
                success_rate = (stats.successful_attempts / stats.total_attempts * 100) if stats.total_attempts > 0 else 0
                avg_method_response_time = (stats.total_response_time / stats.successful_attempts) if stats.successful_attempts > 0 else 0
                
                method_stats[method] = {
                    'total_attempts': stats.total_attempts,
                    'successful_attempts': stats.successful_attempts,
                    'failed_attempts': stats.failed_attempts,
                    'success_rate': success_rate,
                    'avg_response_time': avg_method_response_time,
                    'min_response_time': stats.min_response_time if stats.min_response_time != float('inf') else 0,
                    'max_response_time': stats.max_response_time,
                    'consecutive_failures': stats.consecutive_failures,
                    'last_success_time': stats.last_success_time,
                    'last_failure_time': stats.last_failure_time
                }
            
            # Time-based statistics
            time_stats = self._get_time_based_stats()
            
            # Country statistics
            country_stats = self._get_country_stats()
            
            return {
                # Overall stats
                'session_duration': session_duration,
                'total_rotations': total_events,
                'successful_rotations': successful_events,
                'failed_rotations': failed_events,
                'success_rate': (successful_events / total_events * 100) if total_events > 0 else 0,
                'failure_rate': (failed_events / total_events * 100) if total_events > 0 else 0,
                
                # Response time stats
                'avg_response_time': avg_response_time,
                'median_response_time': median_response_time,
                'min_response_time': min(response_times) if response_times else 0,
                'max_response_time': max(response_times) if response_times else 0,
                
                # Method stats
                'method_stats': method_stats,
                
                # Time-based stats
                'hourly_stats': time_stats.get('hourly', {}),
                'daily_stats': time_stats.get('daily', {}),
                
                # Geographic stats
                'country_stats': country_stats,
                
                # Performance metrics
                'rotations_per_minute': (total_events / (session_duration / 60)) if session_duration > 0 else 0,
                'rotations_per_hour': (total_events / (session_duration / 3600)) if session_duration > 0 else 0,
            }
    
    def _get_time_based_stats(self) -> Dict[str, Dict]:
        """Get statistics broken down by time periods"""
        hourly_stats = defaultdict(lambda: {'success': 0, 'failure': 0})
        daily_stats = defaultdict(lambda: {'success': 0, 'failure': 0})
        
        for event in self.events:
            from datetime import datetime
            dt = datetime.fromtimestamp(event.timestamp)
            
            # Hourly stats
            hour_key = dt.strftime('%Y-%m-%d %H:00')
            if event.success:
                hourly_stats[hour_key]['success'] += 1
            else:
                hourly_stats[hour_key]['failure'] += 1
            
            # Daily stats
            day_key = dt.strftime('%Y-%m-%d')
            if event.success:
                daily_stats[day_key]['success'] += 1
            else:
                daily_stats[day_key]['failure'] += 1
        
        return {
            'hourly': dict(hourly_stats),
            'daily': dict(daily_stats)
        }
    
    def _get_country_stats(self) -> Dict[str, Dict]:
        """Get statistics by country"""
        country_stats = defaultdict(lambda: {'count': 0, 'success': 0, 'failure': 0})
        
        for event in self.events:
            if event.country:
                country_stats[event.country]['count'] += 1
                if event.success:
                    country_stats[event.country]['success'] += 1
                else:
                    country_stats[event.country]['failure'] += 1
        
        # Calculate success rates
        for country, stats in country_stats.items():
            stats['success_rate'] = (stats['success'] / stats['count'] * 100) if stats['count'] > 0 else 0
        
        return dict(country_stats)
    
    def get_performance_trends(self, hours: int = 24) -> Dict[str, Any]:
        """Get performance trends over specified time period"""
        cutoff_time = time.time() - (hours * 3600)
        recent_events = [event for event in self.events if event.timestamp >= cutoff_time]
        
        if not recent_events:
            return {}
        
        # Calculate trends
        time_buckets = defaultdict(list)
        bucket_size = 3600  # 1 hour buckets
        
        for event in recent_events:
            bucket = int(event.timestamp // bucket_size) * bucket_size
            time_buckets[bucket].append(event)
        
        trends = []
        for bucket_time in sorted(time_buckets.keys()):
            events = time_buckets[bucket_time]
            successful = sum(1 for e in events if e.success)
            total = len(events)
            avg_response = statistics.mean([e.response_time for e in events if e.response_time > 0]) or 0
            
            trends.append({
                'timestamp': bucket_time,
                'total_rotations': total,
                'successful_rotations': successful,
                'success_rate': (successful / total * 100) if total > 0 else 0,
                'avg_response_time': avg_response
            })
        
        return {
            'period_hours': hours,
            'total_events': len(recent_events),
            'trends': trends
        }
    
    def get_failure_analysis(self) -> Dict[str, Any]:
        """Analyze failures to identify patterns"""
        failed_events = [event for event in self.events if not event.success]
        
        if not failed_events:
            return {'no_failures': True}
        
        # Analyze by method
        method_failures = defaultdict(list)
        for event in failed_events:
            method_failures[event.method].append(event)
        
        # Analyze by error message
        error_analysis = defaultdict(int)
        for event in failed_events:
            if event.error_message:
                error_analysis[event.error_message] += 1
        
        # Analyze failure patterns
        consecutive_failures = []
        current_streak = 0
        for event in reversed(list(self.events)):
            if not event.success:
                current_streak += 1
            else:
                if current_streak > 0:
                    consecutive_failures.append(current_streak)
                current_streak = 0
        
        if current_streak > 0:
            consecutive_failures.append(current_streak)
        
        return {
            'total_failures': len(failed_events),
            'failure_rate': len(failed_events) / len(self.events) * 100 if self.events else 0,
            'method_failures': {method: len(failures) for method, failures in method_failures.items()},
            'error_messages': dict(error_analysis),
            'max_consecutive_failures': max(consecutive_failures) if consecutive_failures else 0,
            'avg_consecutive_failures': statistics.mean(consecutive_failures) if consecutive_failures else 0,
            'current_failure_streak': current_streak
        }
    
    def export_stats(self, filename: Optional[str] = None) -> str:
        """Export statistics to file"""
        if not filename:
            timestamp = time.strftime("%Y%m%d_%H%M%S")
            filename = f"data/stats/export_{timestamp}.json"
        
        try:
            stats_data = {
                'export_timestamp': time.time(),
                'session_start_time': self.session_start_time,
                'comprehensive_stats': self.get_stats(),
                'performance_trends': self.get_performance_trends(),
                'failure_analysis': self.get_failure_analysis(),
                'raw_events': [asdict(event) for event in list(self.events)[-1000:]]  # Last 1000 events
            }
            
            Path(filename).parent.mkdir(parents=True, exist_ok=True)
            
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(stats_data, f, indent=2, default=str)
            
            self.logger.info(f"Statistics exported to {filename}")
            return filename
            
        except Exception as e:
            self.logger.error(f"Error exporting statistics: {e}")
            raise
    
    def _save_stats(self):
        """Save current statistics to file"""
        try:
            stats_data = {
                'session_start_time': self.session_start_time,
                'method_stats': {method: asdict(stats) for method, stats in self.method_stats.items()},
                'last_events': [asdict(event) for event in list(self.events)[-100:]]  # Last 100 events
            }
            
            with open(self.stats_file, 'w', encoding='utf-8') as f:
                json.dump(stats_data, f, indent=2, default=str)
                
        except Exception as e:
            self.logger.error(f"Error saving statistics: {e}")
    
    def _load_stats(self):
        """Load existing statistics from file"""
        try:
            if self.stats_file.exists():
                with open(self.stats_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                
                # Load method stats
                for method, stats_dict in data.get('method_stats', {}).items():
                    stats = MethodStats(**stats_dict)
                    self.method_stats[method] = stats
                
                # Load recent events
                for event_dict in data.get('last_events', []):
                    event = RotationEvent(**event_dict)
                    self.events.append(event)
                
                self.logger.info("Loaded existing statistics")
                
        except Exception as e:
            self.logger.warning(f"Could not load existing statistics: {e}")
    
    def reset_stats(self):
        """Reset all statistics"""
        with self._lock:
            self.events.clear()
            self.method_stats.clear()
            self.session_start_time = time.time()
            
            # Remove stats file
            try:
                if self.stats_file.exists():
                    self.stats_file.unlink()
            except Exception as e:
                self.logger.error(f"Error removing stats file: {e}")
            
            self.logger.info("Statistics reset")
    
    def get_method_performance_ranking(self) -> List[Dict[str, Any]]:
        """Get methods ranked by performance"""
        rankings = []
        
        for method, stats in self.method_stats.items():
            if stats.total_attempts > 0:
                success_rate = stats.successful_attempts / stats.total_attempts * 100
                avg_response = (stats.total_response_time / stats.successful_attempts) if stats.successful_attempts > 0 else float('inf')
                
                # Performance score (higher is better)
                performance_score = success_rate - (avg_response * 10)  # Penalize slow responses
                
                rankings.append({
                    'method': method,
                    'success_rate': success_rate,
                    'avg_response_time': avg_response,
                    'total_attempts': stats.total_attempts,
                    'performance_score': performance_score
                })
        
        # Sort by performance score (descending)
        rankings.sort(key=lambda x: x['performance_score'], reverse=True)
        
        return rankings
