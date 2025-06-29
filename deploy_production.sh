#!/bin/bash
#
# CyberRotate Pro - Enhanced Production Deployment Script
# Automated deployment for production environments with full enterprise features
#

set -e  # Exit on any error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

# Configuration
PROJECT_NAME="cyberrotate-pro"
INSTALL_DIR="/opt/cyberrotate-pro"
SERVICE_USER="cyberrotate"
PYTHON_VERSION="3.11"
NGINX_ENABLED=true
SSL_ENABLED=false
DOCKER_ENABLED=false
DATABASE_TYPE="sqlite"  # sqlite or postgresql
REDIS_ENABLED=true

echo -e "${BLUE}================================================${NC}"
echo -e "${BLUE}  CyberRotate Pro Enterprise Production Setup  ${NC}"
echo -e "${BLUE}================================================${NC}"

# Function to print status messages
print_status() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARN]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_header() {
    echo -e "\n${CYAN}=== $1 ===${NC}"
}

# Check if running as root
check_root() {
    if [[ $EUID -eq 0 ]]; then
        print_error "This script should not be run as root for security reasons"
        print_status "Please run as a non-root user with sudo privileges"
        exit 1
    fi
}

# Parse command line arguments
parse_arguments() {
    while [[ $# -gt 0 ]]; do
        case $1 in
            --docker)
                DOCKER_ENABLED=true
                shift
                ;;
            --no-nginx)
                NGINX_ENABLED=false
                shift
                ;;
            --ssl)
                SSL_ENABLED=true
                shift
                ;;
            --database=*)
                DATABASE_TYPE="${1#*=}"
                shift
                ;;
            --no-redis)
                REDIS_ENABLED=false
                shift
                ;;
            --help)
                show_help
                exit 0
                ;;
            *)
                print_error "Unknown option: $1"
                show_help
                exit 1
                ;;
        esac
    done
}

show_help() {
    echo "CyberRotate Pro Production Deployment Script"
    echo ""
    echo "Usage: $0 [OPTIONS]"
    echo ""
    echo "Options:"
    echo "  --docker               Deploy using Docker containers"
    echo "  --no-nginx            Skip Nginx installation and configuration"
    echo "  --ssl                 Enable SSL/TLS with Let's Encrypt"
    echo "  --database=TYPE       Database type: sqlite (default) or postgresql"
    echo "  --no-redis            Skip Redis installation"
    echo "  --help                Show this help message"
    echo ""
    echo "Examples:"
    echo "  $0                              # Standard deployment"
    echo "  $0 --docker --ssl              # Docker deployment with SSL"
    echo "  $0 --database=postgresql       # Use PostgreSQL database"
}

# Check system requirements
check_requirements() {
    print_header "Checking System Requirements"
    
    # Check Python version
    if ! command -v python3 &> /dev/null; then
        print_error "Python 3 is required but not installed"
        exit 1
    fi
    
    python_version=$(python3 -c "import sys; print(f'{sys.version_info.major}.{sys.version_info.minor}')")
    if ! python3 -c "import sys; exit(0 if sys.version_info >= (3, 8) else 1)"; then
        print_error "Python 3.8+ is required, found $python_version"
        exit 1
    fi
    
    print_status "Python $python_version found ✓"
    
    # Check pip
    if ! command -v pip3 &> /dev/null; then
        print_error "pip3 is required but not installed"
        exit 1
    fi
    
    # Check git (optional)
    if command -v git &> /dev/null; then
        print_status "Git found ✓"
    else
        print_warning "Git not found - manual installation required"
    fi
    
    # Check available disk space (minimum 1GB)
    available_space=$(df . | awk 'NR==2 {print $4}')
    if [ "$available_space" -lt 1048576 ]; then
        print_error "Insufficient disk space. At least 1GB required"
        exit 1
    fi
    
    print_status "System requirements check passed ✓"
}

# Create directory structure
create_directories() {
    print_status "Creating directory structure..."
    
    mkdir -p $INSTALL_DIR/{config,data,logs,backups}
    mkdir -p $INSTALL_DIR/data/{logs,reports,stats}
    mkdir -p $INSTALL_DIR/config/{openvpn,proxies,profiles}
    
    print_status "Directory structure created ✓"
}

# Install Python dependencies
install_dependencies() {
    print_status "Installing Python dependencies..."
    
    # Create virtual environment
    python3 -m venv $INSTALL_DIR/venv
    source $INSTALL_DIR/venv/bin/activate
    
    # Upgrade pip
    pip install --upgrade pip
    
    # Install requirements
    if [ -f "requirements.txt" ]; then
        pip install -r requirements.txt
        print_status "Core dependencies installed ✓"
    fi
    
    if [ -f "requirements-dashboard.txt" ]; then
        pip install -r requirements-dashboard.txt
        print_status "Dashboard dependencies installed ✓"
    fi
    
    if [ -f "requirements-full.txt" ]; then
        pip install -r requirements-full.txt
        print_status "Full feature dependencies installed ✓"
    fi
    
    deactivate
}

# Copy application files
copy_files() {
    print_status "Copying application files..."
    
    # Copy core application
    cp -r core/ $INSTALL_DIR/
    cp -r ui/ $INSTALL_DIR/
    cp -r utils/ $INSTALL_DIR/
    cp -r manual/ $INSTALL_DIR/
    
    # Copy configuration files
    cp config/config.json $INSTALL_DIR/config/config.json.example
    cp config/api_config.json $INSTALL_DIR/config/
    
    # Copy main scripts
    cp ip_rotator.py $INSTALL_DIR/
    cp gui_launcher.py $INSTALL_DIR/
    cp setup.py $INSTALL_DIR/
    
    # Copy documentation
    cp README.md LICENSE AUTHORS.md $INSTALL_DIR/
    
    print_status "Application files copied ✓"
}

# Configure services
configure_services() {
    print_status "Configuring system services..."
    
    # Create systemd service for API server
    cat > $INSTALL_DIR/cyberrotate-api.service << 'EOF'
[Unit]
Description=CyberRotate Pro API Server
After=network.target

[Service]
Type=simple
User=cyberrotate
WorkingDirectory=/opt/cyberrotate-pro
Environment=PATH=/opt/cyberrotate-pro/venv/bin
ExecStart=/opt/cyberrotate-pro/venv/bin/python core/api_server_enterprise.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
EOF

    # Create systemd service for dashboard
    cat > $INSTALL_DIR/cyberrotate-dashboard.service << 'EOF'
[Unit]
Description=CyberRotate Pro Analytics Dashboard
After=network.target

[Service]
Type=simple
User=cyberrotate
WorkingDirectory=/opt/cyberrotate-pro
Environment=PATH=/opt/cyberrotate-pro/venv/bin
ExecStart=/opt/cyberrotate-pro/venv/bin/python ui/analytics_dashboard.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
EOF

    print_status "Service configuration created ✓"
}

# Set up nginx reverse proxy
setup_nginx() {
    print_status "Setting up Nginx reverse proxy..."
    
    cat > $INSTALL_DIR/nginx-cyberrotate.conf << 'EOF'
server {
    listen 80;
    server_name your-domain.com;
    
    # API Server
    location /api/ {
        proxy_pass http://127.0.0.1:8080;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
    
    # Dashboard
    location /dashboard/ {
        proxy_pass http://127.0.0.1:8050;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
    
    # Static files
    location /static/ {
        alias /opt/cyberrotate-pro/static/;
        expires 30d;
    }
}
EOF

    print_status "Nginx configuration created ✓"
    print_warning "Please copy $INSTALL_DIR/nginx-cyberrotate.conf to /etc/nginx/sites-available/ and enable it"
}

# Configure security
configure_security() {
    print_status "Configuring security settings..."
    
    # Set appropriate permissions
    chmod 755 $INSTALL_DIR
    chmod -R 644 $INSTALL_DIR/config/
    chmod -R 700 $INSTALL_DIR/data/
    chmod +x $INSTALL_DIR/ip_rotator.py
    chmod +x $INSTALL_DIR/gui_launcher.py
    
    # Create security configuration
    cat > $INSTALL_DIR/config/security.json << 'EOF'
{
  "api_keys": {
    "rotation_enabled": true,
    "max_keys_per_user": 5,
    "key_expiry_days": 365
  },
  "rate_limiting": {
    "enabled": true,
    "requests_per_minute": 60,
    "requests_per_hour": 1000
  },
  "ssl": {
    "enabled": false,
    "cert_path": "/etc/ssl/certs/cyberrotate.crt",
    "key_path": "/etc/ssl/private/cyberrotate.key"
  },
  "firewall": {
    "allowed_ips": ["127.0.0.1"],
    "block_tor_exit_nodes": false
  }
}
EOF

    print_status "Security configuration created ✓"
}

# Create startup scripts
create_startup_scripts() {
    print_status "Creating startup scripts..."
    
    # Main startup script
    cat > $INSTALL_DIR/start.sh << 'EOF'
#!/bin/bash
cd /opt/cyberrotate-pro
source venv/bin/activate

echo "Starting CyberRotate Pro services..."

# Start API server
python core/api_server_enterprise.py --host 0.0.0.0 --port 8080 &
API_PID=$!
echo "API Server started (PID: $API_PID)"

# Start dashboard
python ui/analytics_dashboard.py --host 0.0.0.0 --port 8050 &
DASHBOARD_PID=$!
echo "Dashboard started (PID: $DASHBOARD_PID)"

# Save PIDs
echo $API_PID > data/api.pid
echo $DASHBOARD_PID > data/dashboard.pid

echo "CyberRotate Pro is running!"
echo "API Server: http://localhost:8080"
echo "Dashboard: http://localhost:8050"
EOF

    # Stop script
    cat > $INSTALL_DIR/stop.sh << 'EOF'
#!/bin/bash
cd /opt/cyberrotate-pro

echo "Stopping CyberRotate Pro services..."

if [ -f data/api.pid ]; then
    kill $(cat data/api.pid) 2>/dev/null
    rm data/api.pid
    echo "API Server stopped"
fi

if [ -f data/dashboard.pid ]; then
    kill $(cat data/dashboard.pid) 2>/dev/null
    rm data/dashboard.pid
    echo "Dashboard stopped"
fi

echo "CyberRotate Pro stopped"
EOF

    chmod +x $INSTALL_DIR/start.sh
    chmod +x $INSTALL_DIR/stop.sh
    
    print_status "Startup scripts created ✓"
}

# Install Docker and Docker Compose
install_docker() {
    if command -v docker &> /dev/null; then
        print_status "Docker already installed"
        return
    fi
    
    print_header "Installing Docker"
    
    # Update package index
    sudo apt-get update
    
    # Install prerequisites
    sudo apt-get install -y \
        apt-transport-https \
        ca-certificates \
        curl \
        gnupg \
        lsb-release
    
    # Add Docker's official GPG key
    curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg
    
    # Set up stable repository
    echo "deb [arch=amd64 signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
    
    # Install Docker Engine
    sudo apt-get update
    sudo apt-get install -y docker-ce docker-ce-cli containerd.io
    
    # Install Docker Compose
    sudo curl -L "https://github.com/docker/compose/releases/download/v2.12.2/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
    sudo chmod +x /usr/local/bin/docker-compose
    
    # Add user to docker group
    sudo usermod -aG docker $USER
    
    print_success "Docker installed successfully"
}

# Setup PostgreSQL database
setup_postgresql() {
    if [[ "$DATABASE_TYPE" != "postgresql" ]]; then
        return
    fi
    
    print_header "Setting up PostgreSQL Database"
    
    # Install PostgreSQL
    sudo apt-get install -y postgresql postgresql-contrib python3-psycopg2
    
    # Start and enable PostgreSQL
    sudo systemctl start postgresql
    sudo systemctl enable postgresql
    
    # Create database and user
    sudo -u postgres psql << EOF
CREATE DATABASE cyberrotate;
CREATE USER cyberrotate WITH ENCRYPTED PASSWORD 'secure_password_$(openssl rand -hex 8)';
GRANT ALL PRIVILEGES ON DATABASE cyberrotate TO cyberrotate;
ALTER USER cyberrotate CREATEDB;
\q
EOF
    
    print_success "PostgreSQL database configured"
}

# Setup Redis
setup_redis() {
    if [[ "$REDIS_ENABLED" != "true" ]]; then
        return
    fi
    
    print_header "Setting up Redis"
    
    # Install Redis
    sudo apt-get install -y redis-server
    
    # Configure Redis
    sudo sed -i 's/supervised no/supervised systemd/' /etc/redis/redis.conf
    sudo sed -i 's/# maxmemory <bytes>/maxmemory 256mb/' /etc/redis/redis.conf
    sudo sed -i 's/# maxmemory-policy noeviction/maxmemory-policy allkeys-lru/' /etc/redis/redis.conf
    
    # Start and enable Redis
    sudo systemctl restart redis-server
    sudo systemctl enable redis-server
    
    print_success "Redis configured successfully"
}

# Deploy with Docker
deploy_docker() {
    print_header "Deploying with Docker"
    
    # Install Docker if not present
    install_docker
    
    # Copy project files
    sudo mkdir -p $INSTALL_DIR
    sudo cp -r . $INSTALL_DIR/
    sudo chown -R $SERVICE_USER:$SERVICE_USER $INSTALL_DIR
    
    # Build and start containers
    cd $INSTALL_DIR
    
    # Generate secure passwords
    API_SECRET=$(openssl rand -hex 32)
    DB_PASSWORD=$(openssl rand -hex 16)
    
    # Create environment file
    cat > .env << EOF
ENVIRONMENT=production
API_KEY_SECRET=$API_SECRET
DATABASE_URL=postgresql://cyberrotate:$DB_PASSWORD@postgres:5432/cyberrotate
REDIS_URL=redis://redis:6379/0
FLASK_SECRET_KEY=$(openssl rand -hex 32)
EOF
    
    # Build and start services
    sudo docker-compose up --build -d
    
    # Wait for services to be ready
    print_status "Waiting for services to start..."
    sleep 30
    
    # Run database migrations
    sudo docker-compose exec cyberrotate-pro python -c "
from core.database_manager import get_database_manager
import asyncio
asyncio.run(get_database_manager().initialize_database())
"
    
    print_success "Docker deployment completed"
}

# Configure SSL with Let's Encrypt
configure_ssl() {
    if [[ "$SSL_ENABLED" != "true" ]]; then
        return
    fi
    
    print_header "Configuring SSL with Let's Encrypt"
    
    # Install Certbot
    sudo apt-get install -y certbot python3-certbot-nginx
    
    # Get domain name
    read -p "Enter your domain name: " DOMAIN_NAME
    
    if [[ -z "$DOMAIN_NAME" ]]; then
        print_error "Domain name is required for SSL setup"
        return
    fi
    
    # Obtain SSL certificate
    sudo certbot --nginx -d $DOMAIN_NAME --non-interactive --agree-tos --email admin@$DOMAIN_NAME
    
    # Setup auto-renewal
    sudo crontab -l 2>/dev/null | { cat; echo "0 12 * * * /usr/bin/certbot renew --quiet"; } | sudo crontab -
    
    print_success "SSL certificate configured for $DOMAIN_NAME"
}

# Setup monitoring and logging
setup_monitoring() {
    print_header "Setting up Monitoring and Logging"
    
    # Install logrotate configuration
    sudo tee /etc/logrotate.d/cyberrotate > /dev/null << EOF
/var/log/cyberrotate/*.log {
    daily
    missingok
    rotate 30
    compress
    delaycompress
    notifempty
    create 644 $SERVICE_USER $SERVICE_USER
    postrotate
        systemctl reload cyberrotate-api cyberrotate-dashboard || true
    endscript
}
EOF
    
    # Setup log directories
    sudo mkdir -p /var/log/cyberrotate
    sudo chown $SERVICE_USER:$SERVICE_USER /var/log/cyberrotate
    
    # Install monitoring tools
    sudo apt-get install -y htop iotop nethogs
    
    print_success "Monitoring and logging configured"
}

# Setup firewall
setup_firewall() {
    print_header "Configuring Firewall"
    
    # Install UFW if not present
    sudo apt-get install -y ufw
    
    # Default policies
    sudo ufw default deny incoming
    sudo ufw default allow outgoing
    
    # Allow SSH
    sudo ufw allow ssh
    
    # Allow HTTP and HTTPS
    if [[ "$NGINX_ENABLED" == "true" ]]; then
        sudo ufw allow 'Nginx Full'
    else
        sudo ufw allow 8080
        sudo ufw allow 8081
        sudo ufw allow 3000
    fi
    
    # Allow VPN ports
    sudo ufw allow 1194/udp
    sudo ufw allow 443/tcp
    
    # Enable firewall
    sudo ufw --force enable
    
    print_success "Firewall configured"
}

# Create backup script
create_backup_script() {
    print_header "Creating Backup Script"
    
    sudo tee /usr/local/bin/cyberrotate-backup.sh > /dev/null << 'EOF'
#!/bin/bash
# CyberRotate Pro Backup Script

BACKUP_DIR="/opt/backups/cyberrotate"
DATE=$(date +%Y%m%d_%H%M%S)
INSTALL_DIR="/opt/cyberrotate-pro"

mkdir -p $BACKUP_DIR

# Backup configuration files
tar -czf $BACKUP_DIR/config_$DATE.tar.gz -C $INSTALL_DIR config/

# Backup database
if [[ -f $INSTALL_DIR/data/cyberrotate.db ]]; then
    cp $INSTALL_DIR/data/cyberrotate.db $BACKUP_DIR/database_$DATE.db
fi

# Backup logs
tar -czf $BACKUP_DIR/logs_$DATE.tar.gz -C /var/log cyberrotate/

# Remove old backups (keep 30 days)
find $BACKUP_DIR -name "*.tar.gz" -mtime +30 -delete
find $BACKUP_DIR -name "*.db" -mtime +30 -delete

echo "Backup completed: $DATE"
EOF
    
    sudo chmod +x /usr/local/bin/cyberrotate-backup.sh
    
    # Setup daily backup cron job
    (sudo crontab -l 2>/dev/null | grep -v cyberrotate-backup; echo "0 2 * * * /usr/local/bin/cyberrotate-backup.sh") | sudo crontab -
    
    print_success "Backup script created and scheduled"
}

# Setup health checks
setup_health_checks() {
    print_header "Setting up Health Checks"
    
    sudo tee /usr/local/bin/cyberrotate-health.sh > /dev/null << 'EOF'
#!/bin/bash
# CyberRotate Pro Health Check Script

API_URL="http://localhost:8080/api/v1/health"
DASHBOARD_URL="http://localhost:8081"

# Check API server
if curl -f $API_URL > /dev/null 2>&1; then
    echo "API server: OK"
else
    echo "API server: FAILED"
    systemctl restart cyberrotate-api
fi

# Check dashboard
if curl -f $DASHBOARD_URL > /dev/null 2>&1; then
    echo "Dashboard: OK"
else
    echo "Dashboard: FAILED"
    systemctl restart cyberrotate-dashboard
fi

# Check disk space
DISK_USAGE=$(df /opt/cyberrotate-pro | awk 'NR==2 {print $5}' | sed 's/%//')
if [[ $DISK_USAGE -gt 80 ]]; then
    echo "WARNING: Disk usage is ${DISK_USAGE}%"
fi
EOF
    
    sudo chmod +x /usr/local/bin/cyberrotate-health.sh
    
    # Run health checks every 5 minutes
    (sudo crontab -l 2>/dev/null | grep -v cyberrotate-health; echo "*/5 * * * * /usr/local/bin/cyberrotate-health.sh") | sudo crontab -
    
    print_success "Health checks configured"
}

# Run initial setup
run_initial_setup() {
    print_status "Running initial setup..."
    
    cd $INSTALL_DIR
    source venv/bin/activate
    
    # Generate initial configuration
    if [ ! -f "config/config.json" ]; then
        cp config/config.json.example config/config.json
        print_status "Default configuration created"
    fi
    
    # Initialize database
    python -c "
from core.api_server_enterprise import CyberRotateAPIServer
import json
config = {}
server = CyberRotateAPIServer(config)
print('Database initialized')
"
    
    # Generate initial API key
    python -c "
from core.api_server_enterprise import CyberRotateAPIServer
import json
config = {}
server = CyberRotateAPIServer(config)
key_data = server.generate_api_key('admin', ['read', 'rotate', 'admin'])
print('Initial API key generated:')
print(f'Key ID: {key_data[\"key_id\"]}')
print(f'API Key: {key_data[\"api_key\"]}')
with open('data/initial_api_key.txt', 'w') as f:
    f.write(f'Key ID: {key_data[\"key_id\"]}\n')
    f.write(f'API Key: {key_data[\"api_key\"]}\n')
    f.write(f'Permissions: {key_data[\"permissions\"]}\n')
print('API key saved to data/initial_api_key.txt')
"
    
    deactivate
    
    print_status "Initial setup completed ✓"
}

# Main installation function
main() {
    echo -e "${BLUE}Starting CyberRotate Pro production installation...${NC}"
    
    check_root
    check_requirements
    create_directories
    install_dependencies
    copy_files
    configure_services
    setup_nginx
    configure_security
    create_startup_scripts
    create_backup_script
    run_initial_setup
    
    echo -e "${GREEN}======================================${NC}"
    echo -e "${GREEN}  Installation completed successfully!${NC}"
    echo -e "${GREEN}======================================${NC}"
    echo ""
    echo -e "${BLUE}Next steps:${NC}"
    echo "1. Review configuration files in $INSTALL_DIR/config/"
    echo "2. Update security settings in $INSTALL_DIR/config/security.json"
    echo "3. Set up SSL certificates for production use"
    echo "4. Configure your firewall to allow necessary ports"
    echo "5. Start services with: $INSTALL_DIR/start.sh"
    echo ""
    echo -e "${BLUE}Access points:${NC}"
    echo "• API Server: http://localhost:8080"
    echo "• Analytics Dashboard: http://localhost:8050"
    echo "• Initial API key: $INSTALL_DIR/data/initial_api_key.txt"
    echo ""
    echo -e "${BLUE}Management commands:${NC}"
    echo "• Start: $INSTALL_DIR/start.sh"
    echo "• Stop: $INSTALL_DIR/stop.sh"
    echo "• Backup: $INSTALL_DIR/backup.sh"
    echo ""
    echo -e "${GREEN}CyberRotate Pro is ready for production use!${NC}"
}

# Run main function
main "$@"
