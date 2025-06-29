FROM python:3.11-slim

LABEL maintainer="ZehraSec <support@zehrasec.com>"
LABEL version="2.0.0"
LABEL description="CyberRotate Pro - Enterprise IP Rotation Solution"

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1
ENV DEBIAN_FRONTEND=noninteractive

# Install system dependencies
RUN apt-get update && apt-get install -y \
    curl \
    wget \
    git \
    openvpn \
    tor \
    privoxy \
    iptables \
    net-tools \
    procps \
    supervisor \
    nginx \
    && rm -rf /var/lib/apt/lists/*

# Create app directory
WORKDIR /app

# Copy requirements first (for better caching)
COPY requirements*.txt ./
COPY setup.py ./

# Install Python dependencies
RUN pip install --no-cache-dir --upgrade pip setuptools wheel
RUN pip install --no-cache-dir -r requirements-full.txt

# Copy application code
COPY . .

# Create necessary directories
RUN mkdir -p /app/data/logs /app/data/stats /app/data/reports
RUN mkdir -p /var/log/cyberrotate /var/run/cyberrotate

# Set permissions
RUN chmod +x *.sh
RUN chmod +x deploy_production.sh

# Create non-root user
RUN useradd -m -s /bin/bash cyberrotate
RUN chown -R cyberrotate:cyberrotate /app /var/log/cyberrotate /var/run/cyberrotate

# Copy supervisor configuration
COPY docker/supervisord.conf /etc/supervisor/conf.d/supervisord.conf
COPY docker/nginx.conf /etc/nginx/sites-available/default

# Expose ports
EXPOSE 8080 8081 3000 80

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=60s --retries=3 \
    CMD curl -f http://localhost:8080/api/v1/health || exit 1

# Switch to non-root user
USER cyberrotate

# Start supervisor (manages all services)
CMD ["/usr/bin/supervisord", "-c", "/etc/supervisor/conf.d/supervisord.conf"]
