/**
 * CyberRotate Pro - Dashboard JavaScript
 * Real-time dashboard functionality with Socket.IO
 */

class CyberRotateDashboard {
    constructor() {
        this.socket = null;
        this.connectionChart = null;
        this.isConnected = false;
        this.currentStatus = {};
        this.activityLog = [];
        
        this.init();
    }
    
    init() {
        // Initialize Socket.IO connection
        this.initSocket();
        
        // Initialize charts
        this.initCharts();
        
        // Bind event listeners
        this.bindEvents();
        
        // Initialize theme
        this.initTheme();
        
        // Start periodic updates
        this.startPeriodicUpdates();
        
        console.log('CyberRotate Pro Dashboard initialized');
    }
    
    initSocket() {
        this.socket = io();
        
        this.socket.on('connect', () => {
            console.log('Connected to server');
            this.addActivity('Connected to CyberRotate Pro server', 'success');
        });
        
        this.socket.on('disconnect', () => {
            console.log('Disconnected from server');
            this.addActivity('Disconnected from server', 'error');
        });
        
        this.socket.on('status_update', (data) => {
            this.updateStatus(data);
        });
        
        this.socket.on('connection_event', (data) => {
            this.handleConnectionEvent(data);
        });
    }
    
    initCharts() {
        const ctx = document.getElementById('connection-chart');
        if (ctx) {
            this.connectionChart = new Chart(ctx, {
                type: 'line',
                data: {
                    labels: [],
                    datasets: [{
                        label: 'Response Time (ms)',
                        data: [],
                        borderColor: 'rgb(59, 130, 246)',
                        backgroundColor: 'rgba(59, 130, 246, 0.1)',
                        borderWidth: 2,
                        fill: true,
                        tension: 0.4
                    }]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    plugins: {
                        legend: {
                            display: false
                        }
                    },
                    scales: {
                        y: {
                            beginAtZero: true,
                            grid: {
                                color: 'rgba(156, 163, 175, 0.2)'
                            }
                        },
                        x: {
                            grid: {
                                color: 'rgba(156, 163, 175, 0.2)'
                            }
                        }
                    }
                }
            });
        }
    }
    
    bindEvents() {
        // Connection control buttons
        document.getElementById('connect-btn')?.addEventListener('click', () => this.connect());
        document.getElementById('disconnect-btn')?.addEventListener('click', () => this.disconnect());
        document.getElementById('rotate-btn')?.addEventListener('click', () => this.rotateIP());
        
        // Speed test button
        document.getElementById('speed-test-btn')?.addEventListener('click', () => this.runSpeedTest());
        
        // Auto rotation toggle
        document.getElementById('auto-rotation')?.addEventListener('change', (e) => {
            this.toggleAutoRotation(e.target.checked);
        });
        
        // Rotation interval slider
        document.getElementById('rotation-interval')?.addEventListener('input', (e) => {
            document.getElementById('interval-value').textContent = `${e.target.value} min`;
        });
        
        // Theme toggle
        document.getElementById('theme-toggle')?.addEventListener('click', () => this.toggleTheme());
    }
    
    initTheme() {
        const savedTheme = localStorage.getItem('theme');
        if (savedTheme) {
            document.documentElement.classList.toggle('dark', savedTheme === 'dark');
        } else {
            // Auto-detect theme preference
            const prefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches;
            document.documentElement.classList.toggle('dark', prefersDark);
        }
    }
    
    startPeriodicUpdates() {
        // Request status update every 10 seconds
        setInterval(() => {
            if (this.socket?.connected) {
                this.socket.emit('request_status');
            }
        }, 10000);
        
        // Update chart data
        setInterval(() => {
            this.updateChart();
        }, 5000);
    }
    
    async connect() {
        const serviceType = document.getElementById('service-type')?.value;
        const serverLocation = document.getElementById('server-location')?.value;
        
        this.setButtonLoading('connect-btn', true);
        this.addActivity(`Connecting to ${serviceType.toUpperCase()} server...`, 'info');
        
        try {
            const response = await fetch('/api/connect', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    service: serviceType,
                    server: serverLocation !== 'auto' ? serverLocation : null
                })
            });
            
            const result = await response.json();
            
            if (result.success) {
                this.addActivity(`Connected to ${serviceType.toUpperCase()} successfully`, 'success');
                this.updateConnectionButtons(true);
            } else {
                this.addActivity(`Connection failed: ${result.message}`, 'error');
                this.showNotification('Connection failed', 'error');
            }
        } catch (error) {
            console.error('Connection error:', error);
            this.addActivity(`Connection error: ${error.message}`, 'error');
            this.showNotification('Connection error', 'error');
        } finally {
            this.setButtonLoading('connect-btn', false);
        }
    }
    
    async disconnect() {
        this.setButtonLoading('disconnect-btn', true);
        this.addActivity('Disconnecting...', 'info');
        
        try {
            const response = await fetch('/api/disconnect', {
                method: 'POST'
            });
            
            const result = await response.json();
            
            if (result.success) {
                this.addActivity('Disconnected successfully', 'success');
                this.updateConnectionButtons(false);
            } else {
                this.addActivity(`Disconnect failed: ${result.message}`, 'error');
            }
        } catch (error) {
            console.error('Disconnect error:', error);
            this.addActivity(`Disconnect error: ${error.message}`, 'error');
        } finally {
            this.setButtonLoading('disconnect-btn', false);
        }
    }
    
    async rotateIP() {
        this.setButtonLoading('rotate-btn', true);
        this.addActivity('Rotating IP address...', 'info');
        
        try {
            const response = await fetch('/api/rotate', {
                method: 'POST'
            });
            
            const result = await response.json();
            
            if (result.success) {
                this.addActivity(`IP rotated to ${result.new_ip}`, 'success');
                this.showNotification('IP address rotated successfully', 'success');
            } else {
                this.addActivity(`IP rotation failed: ${result.message}`, 'error');
                this.showNotification('IP rotation failed', 'error');
            }
        } catch (error) {
            console.error('Rotation error:', error);
            this.addActivity(`Rotation error: ${error.message}`, 'error');
        } finally {
            this.setButtonLoading('rotate-btn', false);
        }
    }
    
    async runSpeedTest() {
        this.setButtonLoading('speed-test-btn', true);
        this.addActivity('Running speed test...', 'info');
        
        // Reset performance metrics
        document.getElementById('ping-time').textContent = '-- ms';
        document.getElementById('download-speed').textContent = '-- Mbps';
        document.getElementById('upload-speed').textContent = '-- Mbps';
        
        try {
            const response = await fetch('/api/speed-test', {
                method: 'POST'
            });
            
            const result = await response.json();
            
            if (result.success) {
                const { ping, download, upload } = result.data;
                
                document.getElementById('ping-time').textContent = `${ping} ms`;
                document.getElementById('download-speed').textContent = `${download} Mbps`;
                document.getElementById('upload-speed').textContent = `${upload} Mbps`;
                
                this.addActivity(`Speed test completed: ${download}/${upload} Mbps`, 'success');
            } else {
                this.addActivity(`Speed test failed: ${result.message}`, 'error');
            }
        } catch (error) {
            console.error('Speed test error:', error);
            this.addActivity(`Speed test error: ${error.message}`, 'error');
        } finally {
            this.setButtonLoading('speed-test-btn', false);
        }
    }
    
    toggleAutoRotation(enabled) {
        this.addActivity(`Auto rotation ${enabled ? 'enabled' : 'disabled'}`, 'info');
        
        // Send to backend
        fetch('/api/auto-rotation', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                enabled: enabled,
                interval: document.getElementById('rotation-interval')?.value || 15
            })
        });
    }
    
    updateStatus(status) {
        this.currentStatus = status;
        
        // Update connection status indicator
        const statusElement = document.getElementById('connection-status');
        const statusText = document.getElementById('status-text');
        const statusIcon = document.getElementById('status-icon');
        
        if (status.connected) {
            statusElement.innerHTML = `
                <div class="w-3 h-3 bg-green-500 rounded-full status-indicator connected"></div>
                <span class="text-sm text-green-600">Connected</span>
            `;
            statusText.textContent = 'Connected';
            statusText.className = 'text-2xl font-bold text-green-600';
            statusIcon.className = 'fas fa-check text-green-600';
            
            this.isConnected = true;
        } else {
            statusElement.innerHTML = `
                <div class="w-3 h-3 bg-red-500 rounded-full status-indicator disconnected"></div>
                <span class="text-sm text-red-600">Disconnected</span>
            `;
            statusText.textContent = 'Disconnected';
            statusText.className = 'text-2xl font-bold text-red-600';
            statusIcon.className = 'fas fa-times text-red-600';
            
            this.isConnected = false;
        }
        
        // Update IP address
        document.getElementById('current-ip').textContent = status.ip_address || 'Not Connected';
        
        // Update location
        document.getElementById('location').textContent = status.country || 'Unknown';
        
        // Update data transfer
        const dataTransfer = status.data_transferred || 0;
        document.getElementById('data-transfer').textContent = this.formatBytes(dataTransfer);
        
        // Update button states
        this.updateConnectionButtons(status.connected);
        
        // Update performance metrics if available
        if (status.stats) {
            document.getElementById('success-rate').textContent = `${status.stats.success_rate || 0}%`;
        }
    }
    
    updateConnectionButtons(connected) {
        const connectBtn = document.getElementById('connect-btn');
        const disconnectBtn = document.getElementById('disconnect-btn');
        const rotateBtn = document.getElementById('rotate-btn');
        
        if (connectBtn) connectBtn.disabled = connected;
        if (disconnectBtn) disconnectBtn.disabled = !connected;
        if (rotateBtn) rotateBtn.disabled = !connected;
    }
    
    updateChart() {
        if (!this.connectionChart || !this.isConnected) return;
        
        const now = new Date();
        const timeLabel = now.toLocaleTimeString();
        
        // Simulate response time data (in production, this would come from real data)
        const responseTime = Math.random() * 100 + 20;
        
        // Add new data point
        this.connectionChart.data.labels.push(timeLabel);
        this.connectionChart.data.datasets[0].data.push(responseTime);
        
        // Keep only last 20 data points
        if (this.connectionChart.data.labels.length > 20) {
            this.connectionChart.data.labels.shift();
            this.connectionChart.data.datasets[0].data.shift();
        }
        
        this.connectionChart.update('none');
    }
    
    addActivity(message, type = 'info') {
        const timestamp = new Date().toLocaleTimeString();
        const activity = {
            id: Date.now(),
            message,
            type,
            timestamp
        };
        
        this.activityLog.unshift(activity);
        
        // Keep only last 50 activities
        if (this.activityLog.length > 50) {
            this.activityLog.pop();
        }
        
        this.renderActivityLog();
    }
    
    renderActivityLog() {
        const container = document.getElementById('activity-log');
        if (!container) return;
        
        container.innerHTML = this.activityLog.map(activity => `
            <div class="activity-item">
                <div class="activity-icon activity-${activity.type}">
                    <i class="fas fa-${this.getActivityIcon(activity.type)}"></i>
                </div>
                <div class="flex-1">
                    <p class="text-sm text-gray-900 dark:text-white">${activity.message}</p>
                    <p class="text-xs text-gray-500">${activity.timestamp}</p>
                </div>
            </div>
        `).join('');
    }
    
    getActivityIcon(type) {
        const icons = {
            success: 'check',
            error: 'exclamation-triangle',
            warning: 'exclamation-circle',
            info: 'info-circle'
        };
        return icons[type] || 'info-circle';
    }
    
    setButtonLoading(buttonId, loading) {
        const button = document.getElementById(buttonId);
        if (!button) return;
        
        if (loading) {
            button.disabled = true;
            button.classList.add('btn-loading');
            const icon = button.querySelector('i');
            if (icon) {
                icon.className = 'loading-spinner mr-2';
            }
        } else {
            button.disabled = false;
            button.classList.remove('btn-loading');
            const icon = button.querySelector('i');
            if (icon) {
                // Restore original icon based on button type
                if (buttonId === 'connect-btn') icon.className = 'fas fa-play mr-2';
                else if (buttonId === 'disconnect-btn') icon.className = 'fas fa-stop mr-2';
                else if (buttonId === 'rotate-btn') icon.className = 'fas fa-sync-alt mr-2';
                else if (buttonId === 'speed-test-btn') icon.className = 'fas fa-tachometer-alt mr-2';
            }
        }
    }
    
    showNotification(message, type = 'info', duration = 5000) {
        const notification = document.createElement('div');
        notification.className = `notification ${type}`;
        notification.innerHTML = `
            <div class="flex items-center justify-between">
                <span>${message}</span>
                <button class="ml-4 text-white hover:text-gray-200" onclick="this.parentElement.parentElement.remove()">
                    <i class="fas fa-times"></i>
                </button>
            </div>
        `;
        
        document.body.appendChild(notification);
        
        // Auto-remove after duration
        setTimeout(() => {
            if (notification.parentElement) {
                notification.remove();
            }
        }, duration);
    }
    
    toggleTheme() {
        const isDark = document.documentElement.classList.toggle('dark');
        localStorage.setItem('theme', isDark ? 'dark' : 'light');
    }
    
    formatBytes(bytes) {
        if (bytes === 0) return '0 B';
        
        const k = 1024;
        const sizes = ['B', 'KB', 'MB', 'GB', 'TB'];
        const i = Math.floor(Math.log(bytes) / Math.log(k));
        
        return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
    }
    
    handleConnectionEvent(data) {
        switch (data.event) {
            case 'connecting':
                this.addActivity(`Connecting to ${data.server}...`, 'info');
                break;
            case 'connected':
                this.addActivity(`Connected to ${data.server}`, 'success');
                break;
            case 'disconnected':
                this.addActivity('Disconnected', 'warning');
                break;
            case 'error':
                this.addActivity(`Connection error: ${data.message}`, 'error');
                break;
            case 'ip_rotated':
                this.addActivity(`IP rotated to ${data.new_ip}`, 'success');
                break;
        }
    }
}

// Initialize dashboard when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    window.dashboard = new CyberRotateDashboard();
});
