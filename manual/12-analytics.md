# Analytics and Reporting

This guide covers the analytics and reporting features of CyberRotate Pro, helping you track usage, monitor performance, and generate detailed reports.

## 📋 Table of Contents

1. [Analytics Overview](#analytics-overview)
2. [Dashboard Features](#dashboard-features)
3. [Usage Statistics](#usage-statistics)
4. [Performance Reports](#performance-reports)
5. [Traffic Analysis](#traffic-analysis)
6. [Provider Analytics](#provider-analytics)
7. [Custom Reports](#custom-reports)
8. [Data Export](#data-export)
9. [Real-time Monitoring](#real-time-monitoring)
10. [Historical Data](#historical-data)

---

## 📊 Analytics Overview

CyberRotate Pro provides comprehensive analytics to help you understand your IP rotation patterns, performance metrics, and usage statistics.

### Analytics Features

- **Real-time Monitoring**: Live statistics and metrics
- **Historical Analysis**: Trend analysis over time
- **Performance Tracking**: Speed and reliability metrics
- **Usage Reports**: Detailed usage patterns
- **Provider Comparison**: Compare different VPN/proxy providers
- **Geographic Analysis**: IP location and country statistics
- **Error Tracking**: Monitor and analyze connection failures

---

## 🎛️ Dashboard Features

### Main Dashboard

The main dashboard provides an overview of key metrics:

```json
{
  "dashboard_widgets": {
    "current_status": {
      "rotation_active": true,
      "current_ip": "203.0.113.45",
      "current_country": "United States",
      "current_provider": "NordVPN",
      "connection_type": "OpenVPN UDP"
    },
    "today_stats": {
      "total_rotations": 156,
      "successful_rotations": 152,
      "failed_rotations": 4,
      "uptime_percentage": 97.4,
      "data_transferred": "2.3 GB"
    },
    "performance_metrics": {
      "avg_rotation_time": "3.2s",
      "avg_connection_speed": "85 Mbps",
      "success_rate": "97.4%",
      "current_latency": "45ms"
    }
  }
}
```

### Customizable Widgets

Configure dashboard widgets to show relevant metrics:

```yaml
widget_configuration:
  - type: "status_indicator"
    title: "Connection Status"
    position: [0, 0]
    size: [2, 1]
    
  - type: "line_chart"
    title: "Rotation Timeline"
    position: [2, 0]
    size: [4, 2]
    data_source: "rotation_history"
    
  - type: "pie_chart"
    title: "Provider Usage"
    position: [0, 1]
    size: [2, 2]
    data_source: "provider_stats"
    
  - type: "gauge"
    title: "Success Rate"
    position: [6, 0]
    size: [2, 1]
    data_source: "success_rate"
    min_value: 0
    max_value: 100
```

---

## 📈 Usage Statistics

### Daily Usage Reports

```python
def generate_daily_report(date):
    """Generate daily usage report"""
    return {
        "date": date,
        "total_rotations": 156,
        "successful_rotations": 152,
        "failed_rotations": 4,
        "unique_ips": 78,
        "countries_accessed": 12,
        "providers_used": ["NordVPN", "ExpressVPN", "ProxyMesh"],
        "peak_usage_hour": "14:00-15:00",
        "total_bandwidth": "2.3 GB",
        "average_session_duration": "15.2 minutes",
        "top_failure_reasons": [
            {"reason": "Timeout", "count": 2},
            {"reason": "Authentication failed", "count": 1},
            {"reason": "Server unavailable", "count": 1}
        ]
    }
```

### Weekly Trends

```python
def generate_weekly_trends():
    """Generate weekly trend analysis"""
    return {
        "week_start": "2025-06-17",
        "week_end": "2025-06-23",
        "daily_averages": {
            "rotations_per_day": 145,
            "success_rate": 96.8,
            "bandwidth_per_day": "2.1 GB",
            "unique_ips_per_day": 72
        },
        "trends": {
            "rotation_frequency": "increasing",
            "success_rate": "stable",
            "bandwidth_usage": "increasing",
            "geographic_diversity": "stable"
        },
        "recommendations": [
            "Consider upgrading to higher bandwidth plan",
            "Monitor increased rotation frequency",
            "Review provider performance for optimization"
        ]
    }
```

### Monthly Summary

```json
{
  "monthly_summary": {
    "month": "June 2025",
    "total_rotations": 4680,
    "successful_rotations": 4523,
    "overall_success_rate": 96.6,
    "total_bandwidth": "68.4 GB",
    "unique_ips_used": 2341,
    "countries_accessed": 45,
    "providers_performance": {
      "NordVPN": {"usage": 45%, "success_rate": 97.2},
      "ExpressVPN": {"usage": 30%, "success_rate": 96.8},
      "ProxyMesh": {"usage": 25%, "success_rate": 95.1}
    },
    "peak_usage_day": "2025-06-15",
    "cost_analysis": {
      "estimated_cost": "$47.99",
      "cost_per_gb": "$0.70",
      "cost_per_rotation": "$0.01"
    }
  }
}
```

---

## 🚀 Performance Reports

### Connection Performance

```python
def generate_performance_report():
    """Generate detailed performance metrics"""
    return {
        "connection_metrics": {
            "average_connection_time": "2.8s",
            "median_connection_time": "2.3s",
            "95th_percentile": "5.2s",
            "connection_timeout_rate": "1.2%",
            "dns_resolution_time": "0.3s"
        },
        "speed_metrics": {
            "average_download_speed": "85.4 Mbps",
            "average_upload_speed": "23.2 Mbps",
            "peak_download_speed": "142.8 Mbps",
            "speed_consistency": "89.2%",
            "speed_degradation": "12.3%"
        },
        "latency_metrics": {
            "average_latency": "45ms",
            "minimum_latency": "12ms",
            "maximum_latency": "189ms",
            "latency_stability": "94.1%",
            "geographic_latency": {
                "same_country": "23ms",
                "same_continent": "67ms",
                "different_continent": "145ms"
            }
        }
    }
```

### Provider Performance Comparison

```json
{
  "provider_comparison": {
    "NordVPN": {
      "connection_success_rate": 97.2,
      "average_speed": 89.3,
      "average_latency": 42,
      "server_availability": 98.7,
      "geographic_coverage": 59,
      "cost_effectiveness": 8.5
    },
    "ExpressVPN": {
      "connection_success_rate": 96.8,
      "average_speed": 92.1,
      "average_latency": 38,
      "server_availability": 99.1,
      "geographic_coverage": 94,
      "cost_effectiveness": 7.8
    },
    "ProxyMesh": {
      "connection_success_rate": 95.1,
      "average_speed": 76.4,
      "average_latency": 56,
      "server_availability": 97.3,
      "geographic_coverage": 12,
      "cost_effectiveness": 9.2
    }
  }
}
```

---

## 🌐 Traffic Analysis

### Geographic Distribution

```python
def analyze_geographic_usage():
    """Analyze geographic distribution of IP usage"""
    return {
        "by_country": {
            "United States": {"count": 1250, "percentage": 26.7},
            "United Kingdom": {"count": 890, "percentage": 19.0},
            "Germany": {"count": 634, "percentage": 13.5},
            "Canada": {"count": 523, "percentage": 11.2},
            "Australia": {"count": 445, "percentage": 9.5},
            "Others": {"count": 938, "percentage": 20.1}
        },
        "by_continent": {
            "North America": {"count": 1773, "percentage": 37.9},
            "Europe": {"count": 1889, "percentage": 40.4},
            "Asia Pacific": {"count": 778, "percentage": 16.6},
            "Others": {"count": 240, "percentage": 5.1}
        },
        "top_cities": [
            {"city": "New York", "country": "US", "count": 234},
            {"city": "London", "country": "UK", "count": 198},
            {"city": "Toronto", "country": "CA", "count": 167},
            {"city": "Sydney", "country": "AU", "count": 145},
            {"city": "Frankfurt", "country": "DE", "count": 134}
        ]
    }
```

### Traffic Patterns

```json
{
  "traffic_patterns": {
    "hourly_distribution": {
      "00-01": 2.3, "01-02": 1.8, "02-03": 1.5, "03-04": 1.2,
      "04-05": 1.4, "05-06": 2.1, "06-07": 3.8, "07-08": 5.9,
      "08-09": 7.8, "09-10": 9.2, "10-11": 8.7, "11-12": 7.9,
      "12-13": 6.8, "13-14": 8.1, "14-15": 9.5, "15-16": 8.9,
      "16-17": 7.6, "17-18": 6.4, "18-19": 5.7, "19-20": 4.9,
      "20-21": 4.2, "21-22": 3.8, "22-23": 3.1, "23-00": 2.7
    },
    "weekly_pattern": {
      "Monday": 18.2, "Tuesday": 16.8, "Wednesday": 15.9,
      "Thursday": 14.7, "Friday": 13.6, "Saturday": 10.4,
      "Sunday": 10.4
    },
    "rotation_intervals": {
      "1-5 minutes": 12.3,
      "5-15 minutes": 28.7,
      "15-30 minutes": 34.2,
      "30-60 minutes": 18.9,
      "1+ hours": 5.9
    }
  }
}
```

---

## 🏢 Provider Analytics

### Provider Usage Statistics

```python
def analyze_provider_usage():
    """Analyze provider usage and performance"""
    return {
        "usage_distribution": {
            "NordVPN": {
                "total_connections": 2106,
                "success_rate": 97.2,
                "average_duration": "18.5 minutes",
                "data_transferred": "31.2 GB",
                "cost": "$15.99/month",
                "servers_used": 89
            },
            "ExpressVPN": {
                "total_connections": 1404,
                "success_rate": 96.8,
                "average_duration": "22.3 minutes",
                "data_transferred": "23.1 GB",
                "cost": "$12.95/month",
                "servers_used": 67
            },
            "ProxyMesh": {
                "total_connections": 1170,
                "success_rate": 95.1,
                "average_duration": "12.7 minutes",
                "data_transferred": "14.1 GB",
                "cost": "$10.00/month",
                "servers_used": 45
            }
        },
        "performance_ranking": [
            {"provider": "ExpressVPN", "score": 94.2},
            {"provider": "NordVPN", "score": 92.8},
            {"provider": "ProxyMesh", "score": 87.3}
        ]
    }
```

### Server Performance Analysis

```json
{
  "server_analysis": {
    "best_performing_servers": [
      {
        "server": "us1.nordvpn.com",
        "provider": "NordVPN",
        "success_rate": 99.2,
        "avg_speed": 95.4,
        "avg_latency": 28
      },
      {
        "server": "uk-london-01.expressvpn.com",
        "provider": "ExpressVPN",
        "success_rate": 98.8,
        "avg_speed": 102.1,
        "avg_latency": 31
      }
    ],
    "problematic_servers": [
      {
        "server": "jp3.nordvpn.com",
        "provider": "NordVPN",
        "success_rate": 87.3,
        "issues": ["High latency", "Frequent timeouts"]
      }
    ]
  }
}
```

---

## 📋 Custom Reports

### Report Builder

```python
class ReportBuilder:
    def __init__(self):
        self.filters = {}
        self.metrics = []
        self.time_range = {}
    
    def add_filter(self, field, operator, value):
        """Add filter to report"""
        self.filters[field] = {"operator": operator, "value": value}
        return self
    
    def add_metric(self, metric_name, aggregation="sum"):
        """Add metric to report"""
        self.metrics.append({"name": metric_name, "aggregation": aggregation})
        return self
    
    def set_time_range(self, start_date, end_date):
        """Set time range for report"""
        self.time_range = {"start": start_date, "end": end_date}
        return self
    
    def generate(self):
        """Generate custom report"""
        query = {
            "filters": self.filters,
            "metrics": self.metrics,
            "time_range": self.time_range
        }
        return self._execute_query(query)

# Usage example
report = (ReportBuilder()
    .add_filter("provider", "in", ["NordVPN", "ExpressVPN"])
    .add_filter("country", "equals", "United States")
    .add_metric("rotation_count", "count")
    .add_metric("success_rate", "average")
    .set_time_range("2025-06-01", "2025-06-30")
    .generate())
```

### Automated Reports

```yaml
automated_reports:
  daily_summary:
    schedule: "0 9 * * *"  # 9 AM daily
    recipients: ["admin@company.com"]
    format: "email"
    template: "daily_summary"
    
  weekly_performance:
    schedule: "0 9 * * 1"  # 9 AM Mondays
    recipients: ["team@company.com"]
    format: "pdf"
    template: "weekly_performance"
    
  monthly_billing:
    schedule: "0 9 1 * *"  # 9 AM first day of month
    recipients: ["billing@company.com"]
    format: "csv"
    template: "monthly_usage"
```

---

## 📤 Data Export

### Export Formats

```python
def export_data(format_type, data_range, filters=None):
    """Export analytics data in various formats"""
    
    export_config = {
        "csv": {
            "delimiter": ",",
            "include_headers": True,
            "encoding": "utf-8"
        },
        "json": {
            "pretty_print": True,
            "include_metadata": True
        },
        "excel": {
            "sheets": ["Summary", "Details", "Charts"],
            "include_charts": True
        },
        "pdf": {
            "template": "standard_report",
            "include_charts": True,
            "page_size": "A4"
        }
    }
    
    data = fetch_analytics_data(data_range, filters)
    return generate_export(data, format_type, export_config[format_type])
```

### API Data Access

```python
# Export via API
import requests

def export_via_api(api_key, export_config):
    """Export data using REST API"""
    
    headers = {"Authorization": f"Bearer {api_key}"}
    
    response = requests.post(
        "http://localhost:8080/api/v1/analytics/export",
        headers=headers,
        json=export_config
    )
    
    if response.status_code == 200:
        return response.content
    else:
        raise Exception(f"Export failed: {response.text}")

# Usage
config = {
    "format": "csv",
    "date_range": {
        "start": "2025-06-01",
        "end": "2025-06-30"
    },
    "metrics": ["rotations", "success_rate", "bandwidth"],
    "group_by": ["date", "provider"]
}

exported_data = export_via_api("your-api-key", config)
```

---

## 📡 Real-time Monitoring

### Live Dashboard

```javascript
// Real-time dashboard updates
class LiveDashboard {
    constructor(apiKey) {
        this.apiKey = apiKey;
        this.ws = null;
        this.connect();
    }
    
    connect() {
        this.ws = new WebSocket(`ws://localhost:8080/ws/analytics?token=${this.apiKey}`);
        
        this.ws.onmessage = (event) => {
            const data = JSON.parse(event.data);
            this.updateDashboard(data);
        };
        
        this.ws.onclose = () => {
            // Reconnect after 5 seconds
            setTimeout(() => this.connect(), 5000);
        };
    }
    
    updateDashboard(data) {
        // Update various dashboard elements
        if (data.type === 'rotation_completed') {
            this.updateRotationCount(data.total_rotations);
            this.updateSuccessRate(data.success_rate);
        }
        
        if (data.type === 'performance_update') {
            this.updateSpeedGauge(data.current_speed);
            this.updateLatencyChart(data.latency_history);
        }
    }
}
```

### Alert System

```python
class AnalyticsAlerts:
    def __init__(self):
        self.thresholds = {
            "success_rate": {"min": 95.0, "alert_type": "warning"},
            "avg_rotation_time": {"max": 10.0, "alert_type": "warning"},
            "error_rate": {"max": 5.0, "alert_type": "critical"},
            "bandwidth_usage": {"max": 100.0, "alert_type": "info"}
        }
    
    def check_thresholds(self, current_metrics):
        """Check metrics against thresholds and trigger alerts"""
        alerts = []
        
        for metric, threshold in self.thresholds.items():
            value = current_metrics.get(metric, 0)
            
            if "min" in threshold and value < threshold["min"]:
                alerts.append({
                    "metric": metric,
                    "value": value,
                    "threshold": threshold["min"],
                    "type": threshold["alert_type"],
                    "message": f"{metric} is below threshold: {value} < {threshold['min']}"
                })
            
            if "max" in threshold and value > threshold["max"]:
                alerts.append({
                    "metric": metric,
                    "value": value,
                    "threshold": threshold["max"],
                    "type": threshold["alert_type"],
                    "message": f"{metric} exceeds threshold: {value} > {threshold['max']}"
                })
        
        return alerts
    
    def send_alerts(self, alerts):
        """Send alerts via configured channels"""
        for alert in alerts:
            if alert["type"] == "critical":
                self.send_email_alert(alert)
                self.send_slack_alert(alert)
            elif alert["type"] == "warning":
                self.send_slack_alert(alert)
```

---

## 📚 Historical Data

### Data Retention

```yaml
data_retention_policy:
  raw_events: 30 days
  hourly_aggregates: 1 year
  daily_aggregates: 5 years
  monthly_aggregates: forever
  
  compression:
    enabled: true
    algorithm: "gzip"
    compress_after: 7 days
  
  archival:
    enabled: true
    archive_after: 1 year
    archive_location: "s3://backup-bucket/cyberrotate-analytics"
```

### Historical Analysis

```python
def analyze_historical_trends(metric, time_period):
    """Analyze historical trends for a specific metric"""
    
    data = fetch_historical_data(metric, time_period)
    
    analysis = {
        "trend_direction": calculate_trend(data),
        "seasonal_patterns": detect_seasonality(data),
        "anomalies": detect_anomalies(data),
        "forecasting": forecast_future_values(data),
        "correlation_analysis": find_correlations(data)
    }
    
    return analysis

# Example usage
trend_analysis = analyze_historical_trends("success_rate", "last_6_months")
```

---

## 🔧 Configuration

### Analytics Settings

```json
{
  "analytics_config": {
    "data_collection": {
      "enabled": true,
      "sampling_rate": 1.0,
      "include_sensitive_data": false
    },
    "real_time_updates": {
      "enabled": true,
      "update_interval": 5,
      "batch_size": 100
    },
    "storage": {
      "database": "analytics.db",
      "max_size": "10GB",
      "auto_cleanup": true
    },
    "privacy": {
      "anonymize_ips": true,
      "data_retention_days": 365,
      "gdpr_compliance": true
    }
  }
}
```

### Dashboard Customization

```yaml
dashboard_config:
  theme: "dark"
  refresh_interval: 30  # seconds
  widgets:
    - type: "metric_card"
      title: "Active Rotations"
      metric: "active_rotations"
      format: "number"
    
    - type: "chart"
      title: "Success Rate Trend"
      chart_type: "line"
      metric: "success_rate"
      time_range: "24h"
    
    - type: "map"
      title: "Geographic Distribution"
      metric: "ip_locations"
      style: "world"
```

---

## 📖 Additional Resources

- **API Reference**: See [06-api-reference.md](06-api-reference.md) for analytics API endpoints
- **Performance Guide**: Check [11-performance.md](11-performance.md) for optimization tips
- **Configuration**: Visit [03-configuration.md](03-configuration.md) for settings
- **Troubleshooting**: Review [14-troubleshooting.md](14-troubleshooting.md) for analytics issues

---

**Analytics Best Practices:**

1. Monitor key metrics regularly
2. Set up automated alerts for critical thresholds
3. Use historical data for capacity planning
4. Export data regularly for backup
5. Customize dashboards for your use case

---

*This guide is part of the CyberRotate Pro manual. For more information, visit the [main manual page](README.md).*
