# Performance Optimization Guide

This guide covers performance optimization techniques and monitoring for CyberRotate Pro to ensure optimal speed and efficiency.

## 📋 Table of Contents

1. [Performance Overview](#performance-overview)
2. [System Optimization](#system-optimization)
3. [Network Performance](#network-performance)
4. [Memory Management](#memory-management)
5. [CPU Optimization](#cpu-optimization)
6. [Storage Optimization](#storage-optimization)
7. [Connection Pooling](#connection-pooling)
8. [Monitoring Tools](#monitoring-tools)
9. [Performance Metrics](#performance-metrics)
10. [Troubleshooting Slow Performance](#troubleshooting-slow-performance)

---

## 🚀 Performance Overview

CyberRotate Pro is designed for high-performance IP rotation with minimal impact on your system resources. This guide helps you optimize performance for different use cases.

### Key Performance Factors

- **Connection Speed**: Network latency and bandwidth
- **Rotation Frequency**: How often IPs are rotated
- **Concurrent Connections**: Number of simultaneous connections
- **Resource Usage**: CPU, memory, and disk utilization
- **Provider Selection**: VPN/Proxy provider performance

---

## ⚙️ System Optimization

### Hardware Requirements

```yaml
Minimum Configuration:
  CPU: 2 cores, 2.0 GHz
  RAM: 2GB
  Storage: 1GB free space
  Network: 10 Mbps

Recommended Configuration:
  CPU: 4+ cores, 3.0+ GHz
  RAM: 8GB+
  Storage: 5GB+ SSD
  Network: 100+ Mbps

High-Performance Configuration:
  CPU: 8+ cores, 3.5+ GHz
  RAM: 16GB+
  Storage: 10GB+ NVMe SSD
  Network: 1 Gbps+
```

### Operating System Tuning

#### Windows Optimization

```powershell
# Increase network buffer sizes
netsh int tcp set global autotuninglevel=normal
netsh int tcp set global chimney=enabled
netsh int tcp set global rss=enabled

# Optimize TCP settings
netsh int tcp set global tcp1323opts=enabled
netsh int tcp set global netdma=enabled

# Set high performance power plan
powercfg -setactive 8c5e7fda-e8bf-4a96-9a85-a6e23a8c635c
```

#### Linux Optimization

```bash
# Increase network buffers
echo 'net.core.rmem_max = 134217728' >> /etc/sysctl.conf
echo 'net.core.wmem_max = 134217728' >> /etc/sysctl.conf
echo 'net.ipv4.tcp_rmem = 4096 87380 134217728' >> /etc/sysctl.conf
echo 'net.ipv4.tcp_wmem = 4096 65536 134217728' >> /etc/sysctl.conf

# Optimize connection handling
echo 'net.ipv4.tcp_fin_timeout = 30' >> /etc/sysctl.conf
echo 'net.ipv4.tcp_keepalive_time = 120' >> /etc/sysctl.conf
echo 'net.core.netdev_max_backlog = 5000' >> /etc/sysctl.conf

# Apply settings
sysctl -p
```

#### macOS Optimization

```bash
# Increase socket buffer sizes
sudo sysctl -w kern.ipc.maxsockbuf=8388608
sudo sysctl -w net.inet.tcp.sendspace=1048576
sudo sysctl -w net.inet.tcp.recvspace=1048576

# Optimize TCP settings
sudo sysctl -w net.inet.tcp.delayed_ack=0
sudo sysctl -w net.inet.tcp.slowstart_flightsize=20
```

---

## 🌐 Network Performance

### Connection Optimization

#### VPN Performance Settings

```json
{
  "vpn_settings": {
    "protocol": "OpenVPN UDP",
    "encryption": "AES-256-GCM",
    "auth": "SHA256",
    "compression": "lz4",
    "mtu": 1500,
    "mssfix": 1460,
    "fast_io": true,
    "tcp_nodelay": true
  }
}
```

#### Proxy Performance Settings

```json
{
  "proxy_settings": {
    "connection_timeout": 10,
    "read_timeout": 30,
    "keep_alive": true,
    "max_connections_per_host": 10,
    "connection_pool_size": 100,
    "retry_attempts": 3,
    "retry_delay": 1
  }
}
```

### Bandwidth Optimization

```python
# Bandwidth throttling configuration
bandwidth_config = {
    "download_limit": "50MB/s",  # Set download speed limit
    "upload_limit": "10MB/s",    # Set upload speed limit
    "burst_allowance": 1.5,      # Allow burst up to 150% of limit
    "priority_traffic": {
        "control": "highest",
        "rotation": "high",
        "data": "normal"
    }
}
```

---

## 💾 Memory Management

### Memory Configuration

```yaml
memory_settings:
  # Cache settings
  connection_cache_size: 1000
  dns_cache_size: 5000
  response_cache_size: 10000
  
  # Buffer sizes
  read_buffer_size: 65536
  write_buffer_size: 65536
  
  # Garbage collection
  gc_threshold: 100MB
  gc_interval: 300  # seconds
```

### Memory Monitoring

```python
import psutil
import gc

def monitor_memory():
    """Monitor memory usage"""
    process = psutil.Process()
    memory_info = process.memory_info()
    
    return {
        'rss': memory_info.rss / 1024 / 1024,  # MB
        'vms': memory_info.vms / 1024 / 1024,  # MB
        'percent': process.memory_percent(),
        'available': psutil.virtual_memory().available / 1024 / 1024
    }

def optimize_memory():
    """Force garbage collection"""
    gc.collect()
    
    # Clear caches if memory usage is high
    if psutil.virtual_memory().percent > 80:
        clear_caches()
```

---

## ⚡ CPU Optimization

### Multi-threading Configuration

```json
{
  "threading": {
    "worker_threads": 8,
    "io_threads": 4,
    "rotation_threads": 2,
    "monitor_threads": 1,
    "thread_pool_size": 20,
    "max_concurrent_rotations": 5
  }
}
```

### CPU Affinity Settings

```python
import os
import psutil

def set_cpu_affinity():
    """Set CPU affinity for optimal performance"""
    cpu_count = psutil.cpu_count()
    
    if cpu_count >= 8:
        # Use specific cores for different tasks
        os.sched_setaffinity(0, {0, 1, 2, 3})  # Main process
    elif cpu_count >= 4:
        os.sched_setaffinity(0, {0, 1})  # Use first 2 cores
```

### Process Priority

```python
import psutil

def set_high_priority():
    """Set high process priority"""
    current_process = psutil.Process()
    
    # Windows
    if os.name == 'nt':
        current_process.nice(psutil.HIGH_PRIORITY_CLASS)
    # Unix-like
    else:
        current_process.nice(-10)  # Higher priority
```

---

## 💽 Storage Optimization

### Disk Configuration

```yaml
storage_settings:
  # Use SSD for better performance
  data_directory: "/path/to/ssd/cyberrotate"
  
  # Log settings
  log_level: "INFO"  # Use INFO instead of DEBUG for production
  log_rotation: true
  max_log_size: "100MB"
  log_retention: 7  # days
  
  # Database optimization
  database_cache_size: "256MB"
  database_sync_mode: "NORMAL"
  database_temp_store: "MEMORY"
```

### Temporary Files Management

```python
import tempfile
import shutil

class TempFileManager:
    def __init__(self, max_size=1024*1024*100):  # 100MB
        self.max_size = max_size
        self.temp_dir = tempfile.mkdtemp(prefix='cyberrotate_')
    
    def cleanup_old_files(self):
        """Clean up old temporary files"""
        total_size = 0
        for root, dirs, files in os.walk(self.temp_dir):
            for file in files:
                file_path = os.path.join(root, file)
                total_size += os.path.getsize(file_path)
        
        if total_size > self.max_size:
            shutil.rmtree(self.temp_dir)
            self.temp_dir = tempfile.mkdtemp(prefix='cyberrotate_')
```

---

## 🔗 Connection Pooling

### HTTP Connection Pool

```python
import urllib3
from urllib3.util.retry import Retry

# Configure connection pooling
retry_strategy = Retry(
    total=3,
    backoff_factor=1,
    status_forcelist=[429, 500, 502, 503, 504],
)

http = urllib3.PoolManager(
    num_pools=10,
    maxsize=20,
    block=False,
    retry=retry_strategy,
    timeout=urllib3.Timeout(connect=10, read=30)
)
```

### Connection Pool Monitoring

```python
def monitor_connection_pool():
    """Monitor connection pool statistics"""
    stats = {
        'active_connections': len(http.pools),
        'total_requests': http.num_requests,
        'pool_size': http.maxsize,
        'connection_timeouts': http.timeouts
    }
    return stats
```

---

## 📊 Monitoring Tools

### Performance Dashboard

```python
class PerformanceDashboard:
    def __init__(self):
        self.metrics = {
            'rotation_speed': [],
            'connection_latency': [],
            'throughput': [],
            'error_rate': [],
            'resource_usage': []
        }
    
    def collect_metrics(self):
        """Collect real-time performance metrics"""
        metrics = {
            'timestamp': time.time(),
            'cpu_percent': psutil.cpu_percent(),
            'memory_percent': psutil.virtual_memory().percent,
            'network_io': psutil.net_io_counters(),
            'disk_io': psutil.disk_io_counters(),
            'rotation_count': self.get_rotation_count(),
            'active_connections': self.get_active_connections()
        }
        return metrics
    
    def generate_report(self):
        """Generate performance report"""
        report = {
            'avg_rotation_time': np.mean(self.metrics['rotation_speed']),
            'avg_latency': np.mean(self.metrics['connection_latency']),
            'peak_throughput': max(self.metrics['throughput']),
            'error_percentage': np.mean(self.metrics['error_rate']) * 100
        }
        return report
```

### Real-time Monitoring

```bash
# Create monitoring script
#!/bin/bash

while true; do
    echo "=== CyberRotate Performance Monitor ==="
    echo "CPU Usage: $(top -bn1 | grep "Cpu(s)" | awk '{print $2}' | cut -d'%' -f1)"
    echo "Memory Usage: $(free | grep Mem | awk '{printf("%.1f%%"), $3/$2 * 100.0}')"
    echo "Network Connections: $(netstat -an | grep ESTABLISHED | wc -l)"
    echo "Active Rotations: $(curl -s http://localhost:8080/api/v1/status | jq '.active_rotations')"
    echo "Current IP: $(curl -s http://localhost:8080/api/v1/ip/current | jq -r '.ip')"
    echo "=================================="
    sleep 5
done
```

---

## 📈 Performance Metrics

### Key Performance Indicators

```python
class PerformanceMetrics:
    def __init__(self):
        self.start_time = time.time()
        self.rotation_times = []
        self.connection_times = []
        self.error_count = 0
        self.total_requests = 0
    
    def calculate_kpis(self):
        """Calculate key performance indicators"""
        uptime = time.time() - self.start_time
        
        return {
            'uptime_hours': uptime / 3600,
            'avg_rotation_time': np.mean(self.rotation_times) if self.rotation_times else 0,
            'min_rotation_time': min(self.rotation_times) if self.rotation_times else 0,
            'max_rotation_time': max(self.rotation_times) if self.rotation_times else 0,
            'success_rate': ((self.total_requests - self.error_count) / max(self.total_requests, 1)) * 100,
            'rotations_per_hour': len(self.rotation_times) / (uptime / 3600),
            'avg_connection_time': np.mean(self.connection_times) if self.connection_times else 0
        }
```

### Benchmarking

```python
def benchmark_rotation_speed():
    """Benchmark IP rotation performance"""
    import time
    
    rotation_times = []
    
    for i in range(10):
        start_time = time.time()
        
        # Perform rotation
        api.rotate_now()
        
        # Wait for completion
        while api.get_status()['rotation_in_progress']:
            time.sleep(0.1)
        
        end_time = time.time()
        rotation_times.append(end_time - start_time)
    
    return {
        'average': np.mean(rotation_times),
        'median': np.median(rotation_times),
        'min': min(rotation_times),
        'max': max(rotation_times),
        'std_dev': np.std(rotation_times)
    }
```

---

## 🔧 Troubleshooting Slow Performance

### Common Performance Issues

#### Slow Rotation Times

```python
def diagnose_slow_rotation():
    """Diagnose slow rotation performance"""
    diagnostics = {
        'network_latency': measure_network_latency(),
        'dns_resolution_time': measure_dns_time(),
        'provider_response_time': measure_provider_time(),
        'system_load': psutil.getloadavg(),
        'available_memory': psutil.virtual_memory().available
    }
    
    recommendations = []
    
    if diagnostics['network_latency'] > 200:  # ms
        recommendations.append("High network latency detected. Consider using faster providers.")
    
    if diagnostics['system_load'][0] > 2.0:
        recommendations.append("High system load. Close unnecessary applications.")
    
    if diagnostics['available_memory'] < 1024*1024*1024:  # 1GB
        recommendations.append("Low available memory. Consider adding more RAM.")
    
    return {
        'diagnostics': diagnostics,
        'recommendations': recommendations
    }
```

#### High Resource Usage

```python
def optimize_resource_usage():
    """Optimize resource usage automatically"""
    
    # Check memory usage
    memory_percent = psutil.virtual_memory().percent
    if memory_percent > 80:
        # Clear caches
        clear_all_caches()
        # Reduce worker threads
        reduce_thread_count()
    
    # Check CPU usage
    cpu_percent = psutil.cpu_percent(interval=1)
    if cpu_percent > 90:
        # Reduce rotation frequency
        increase_rotation_interval()
        # Lower process priority for non-critical tasks
        adjust_process_priorities()
    
    # Check disk usage
    disk_percent = psutil.disk_usage('/').percent
    if disk_percent > 90:
        # Clean up old logs
        cleanup_old_logs()
        # Clear temporary files
        cleanup_temp_files()
```

### Performance Optimization Checklist

- [ ] **System Requirements**: Verify minimum hardware requirements
- [ ] **Network Speed**: Test internet connection speed
- [ ] **Provider Selection**: Choose fastest VPN/proxy providers
- [ ] **Resource Monitoring**: Monitor CPU, memory, and disk usage
- [ ] **Connection Settings**: Optimize timeout and retry settings
- [ ] **Cache Configuration**: Configure appropriate cache sizes
- [ ] **Thread Settings**: Adjust worker thread counts
- [ ] **Log Levels**: Use appropriate logging levels
- [ ] **Cleanup Tasks**: Regular cleanup of temporary files
- [ ] **Update Software**: Keep CyberRotate Pro updated

---

## 📖 Additional Resources

- **Configuration Guide**: See [03-configuration.md](03-configuration.md) for detailed settings
- **Troubleshooting**: Check [14-troubleshooting.md](14-troubleshooting.md) for performance issues
- **API Reference**: Visit [06-api-reference.md](06-api-reference.md) for API optimization
- **System Requirements**: Review [README.md](README.md) for hardware requirements

---

**Performance Tips:**

1. Use SSD storage for better I/O performance
2. Ensure stable internet connection with good bandwidth
3. Choose geographically closer VPN/proxy servers
4. Monitor resource usage regularly
5. Keep the system updated and clean

---

*This guide is part of the CyberRotate Pro manual. For more information, visit the [main manual page](README.md).*
