# BTDigg Clone - Deployment Guide

## Table of Contents
1. [Overview](#overview)
2. [Prerequisites](#prerequisites)
3. [Deployment Options](#deployment-options)
4. [Docker Deployment](#docker-deployment)
5. [Manual Deployment](#manual-deployment)
6. [Production Deployment](#production-deployment)
7. [Cloud Deployment](#cloud-deployment)
8. [Configuration](#configuration)
9. [Monitoring](#monitoring)
10. [Troubleshooting](#troubleshooting)

## Overview

This guide covers deploying the BTDigg Clone application in various environments, from local development to production cloud deployments.

### Deployment Scenarios
- **Development**: Local development environment
- **Testing**: Staging environment for testing
- **Production**: Live production environment
- **Cloud**: Cloud platform deployment

## Prerequisites

### System Requirements
- **OS**: Linux, macOS, or Windows
- **Docker**: Version 20.10+ (for containerized deployment)
- **Python**: 3.11+ (for manual deployment)
- **Memory**: Minimum 512MB RAM
- **Storage**: Minimum 1GB free space
- **Network**: Internet access for dependencies

### Software Dependencies
- **Docker & Docker Compose**: For containerized deployment
- **Python 3.11+**: For manual deployment
- **SQLite**: Database (included with Python)
- **Git**: Version control (optional)

## Deployment Options

### 1. Docker Deployment (Recommended)
- **Pros**: Consistent environment, easy setup, isolated
- **Cons**: Requires Docker knowledge
- **Best for**: All environments

### 2. Manual Deployment
- **Pros**: Full control, no Docker dependency
- **Cons**: Environment-specific setup
- **Best for**: Development, custom environments

### 3. Cloud Deployment
- **Pros**: Scalable, managed infrastructure
- **Cons**: Additional cost, complexity
- **Best for**: Production environments

## Docker Deployment

### Quick Start
```bash
# Clone the repository
git clone <repository-url>
cd btdg

# Build and start
docker-compose up --build

# Access the application
open http://localhost:5000
```

### Detailed Docker Setup

#### 1. Build the Image
```bash
# Build the Docker image
docker build -t btdig-clone .

# Verify the image
docker images | grep btdig-clone
```

#### 2. Run with Docker Compose
```bash
# Start all services
docker-compose up -d

# View logs
docker-compose logs -f

# Stop services
docker-compose down
```

#### 3. Environment Configuration
Create `.env` file:
```bash
# Application settings
FLASK_ENV=production
FLASK_DEBUG=0
DATABASE_PATH=/app/db/torrents.db

# Server settings
HOST=0.0.0.0
PORT=5000

# Database settings
DB_PATH=/app/db
DB_NAME=torrents.db

# Logging
LOG_LEVEL=INFO
LOG_FILE=/app/logs/app.log
```

#### 4. Production Docker Compose
```yaml
version: '3.8'

services:
  btdig-clone:
    build: .
    ports:
      - "80:5000"
    volumes:
      - ./db:/app/db
      - ./logs:/app/logs
    environment:
      - FLASK_ENV=production
      - FLASK_DEBUG=0
    restart: unless-stopped
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:5000/health"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 40s

  # Optional: Nginx reverse proxy
  nginx:
    image: nginx:alpine
    ports:
      - "443:443"
      - "80:80"
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf
      - ./ssl:/etc/nginx/ssl
    depends_on:
      - btdig-clone
    restart: unless-stopped

  # Optional: Redis for caching
  redis:
    image: redis:7-alpine
    ports:
      - "6379:6379"
    volumes:
      - redis_data:/data
    restart: unless-stopped

volumes:
  redis_data:
```

## Manual Deployment

### 1. System Setup

#### Ubuntu/Debian
```bash
# Update system
sudo apt update && sudo apt upgrade -y

# Install Python and dependencies
sudo apt install -y python3 python3-pip python3-venv sqlite3

# Install additional dependencies
sudo apt install -y curl git nginx
```

#### CentOS/RHEL
```bash
# Update system
sudo yum update -y

# Install Python and dependencies
sudo yum install -y python3 python3-pip sqlite

# Install additional dependencies
sudo yum install -y curl git nginx
```

#### macOS
```bash
# Install Homebrew (if not installed)
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Install Python
brew install python@3.11

# Install additional tools
brew install sqlite curl git nginx
```

### 2. Application Setup
```bash
# Clone repository
git clone <repository-url>
cd btdg

# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r backend/requirements.txt

# Initialize database
cd backend
python db/seed_data.py

# Test the application
python app.py
```

### 3. Systemd Service (Linux)
Create service file `/etc/systemd/system/btdig-clone.service`:
```ini
[Unit]
Description=BTDigg Clone Application
After=network.target

[Service]
Type=simple
User=www-data
Group=www-data
WorkingDirectory=/opt/btdg/backend
Environment=PATH=/opt/btdg/venv/bin
ExecStart=/opt/btdg/venv/bin/python app.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

Enable and start the service:
```bash
sudo systemctl daemon-reload
sudo systemctl enable btdig-clone
sudo systemctl start btdig-clone
sudo systemctl status btdig-clone
```

## Production Deployment

### 1. Security Considerations

#### Firewall Configuration
```bash
# UFW (Ubuntu)
sudo ufw allow 22/tcp    # SSH
sudo ufw allow 80/tcp    # HTTP
sudo ufw allow 443/tcp   # HTTPS
sudo ufw enable

# iptables (CentOS)
sudo iptables -A INPUT -p tcp --dport 22 -j ACCEPT
sudo iptables -A INPUT -p tcp --dport 80 -j ACCEPT
sudo iptables -A INPUT -p tcp --dport 443 -j ACCEPT
```

#### SSL/TLS Configuration
```bash
# Install Certbot
sudo apt install certbot python3-certbot-nginx

# Obtain SSL certificate
sudo certbot --nginx -d your-domain.com

# Auto-renewal
sudo crontab -e
# Add: 0 12 * * * /usr/bin/certbot renew --quiet
```

### 2. Nginx Configuration
Create `/etc/nginx/sites-available/btdig-clone`:
```nginx
server {
    listen 80;
    server_name your-domain.com;
    return 301 https://$server_name$request_uri;
}

server {
    listen 443 ssl http2;
    server_name your-domain.com;

    ssl_certificate /etc/letsencrypt/live/your-domain.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/your-domain.com/privkey.pem;

    # Security headers
    add_header X-Frame-Options DENY;
    add_header X-Content-Type-Options nosniff;
    add_header X-XSS-Protection "1; mode=block";
    add_header Strict-Transport-Security "max-age=31536000; includeSubDomains";

    # Proxy to Flask app
    location / {
        proxy_pass http://127.0.0.1:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    # Static files
    location /static/ {
        alias /opt/btdg/frontend/;
        expires 1y;
        add_header Cache-Control "public, immutable";
    }

    # Health check
    location /health {
        proxy_pass http://127.0.0.1:5000/health;
        access_log off;
    }
}
```

Enable the site:
```bash
sudo ln -s /etc/nginx/sites-available/btdig-clone /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl reload nginx
```

### 3. Database Configuration
```bash
# Create database directory
sudo mkdir -p /var/lib/btdig-clone
sudo chown www-data:www-data /var/lib/btdig-clone

# Initialize database
sudo -u www-data python3 /opt/btdg/backend/db/seed_data.py

# Backup script
sudo nano /opt/btdg/backup.sh
```

Backup script content:
```bash
#!/bin/bash
BACKUP_DIR="/var/backups/btdig-clone"
DATE=$(date +%Y%m%d_%H%M%S)
DB_FILE="/var/lib/btdig-clone/torrents.db"

mkdir -p $BACKUP_DIR
cp $DB_FILE $BACKUP_DIR/torrents_$DATE.db
gzip $BACKUP_DIR/torrents_$DATE.db

# Keep only last 7 days
find $BACKUP_DIR -name "torrents_*.db.gz" -mtime +7 -delete
```

## Cloud Deployment

### 1. AWS Deployment

#### EC2 Setup
```bash
# Launch EC2 instance
aws ec2 run-instances \
  --image-id ami-0c02fb55956c7d316 \
  --instance-type t3.micro \
  --key-name your-key-pair \
  --security-group-ids sg-xxxxxxxxx

# Connect to instance
ssh -i your-key.pem ubuntu@your-instance-ip
```

#### Application Deployment
```bash
# Install Docker
sudo apt update
sudo apt install -y docker.io docker-compose

# Clone and deploy
git clone <repository-url>
cd btdg
sudo docker-compose up -d
```

#### Load Balancer Setup
```bash
# Create Application Load Balancer
aws elbv2 create-load-balancer \
  --name btdig-clone-alb \
  --subnets subnet-xxxxxxxxx subnet-yyyyyyyyy \
  --security-groups sg-xxxxxxxxx

# Create target group
aws elbv2 create-target-group \
  --name btdig-clone-tg \
  --protocol HTTP \
  --port 5000 \
  --vpc-id vpc-xxxxxxxxx
```

### 2. Google Cloud Platform

#### Compute Engine Setup
```bash
# Create instance
gcloud compute instances create btdig-clone \
  --zone=us-central1-a \
  --machine-type=e2-micro \
  --image-family=debian-11 \
  --image-project=debian-cloud

# Deploy application
gcloud compute ssh btdig-clone --zone=us-central1-a
```

#### Container Registry
```bash
# Build and push image
docker build -t gcr.io/your-project/btdig-clone .
docker push gcr.io/your-project/btdig-clone

# Deploy to GKE
kubectl apply -f k8s-deployment.yaml
```

### 3. Azure Deployment

#### Azure Container Instances
```bash
# Build and push to Azure Container Registry
az acr build --registry your-registry --image btdig-clone .

# Deploy to Container Instances
az container create \
  --resource-group your-rg \
  --name btdig-clone \
  --image your-registry.azurecr.io/btdig-clone \
  --ports 5000 \
  --dns-name-label btdig-clone
```

## Configuration

### Environment Variables

#### Application Settings
```bash
# Flask settings
FLASK_ENV=production
FLASK_DEBUG=0
FLASK_APP=app.py

# Database settings
DATABASE_PATH=/var/lib/btdig-clone/torrents.db
DB_PATH=/var/lib/btdig-clone

# Server settings
HOST=0.0.0.0
PORT=5000

# Logging
LOG_LEVEL=INFO
LOG_FILE=/var/log/btdig-clone/app.log
```

#### Performance Settings
```bash
# Database settings
DB_POOL_SIZE=10
DB_MAX_OVERFLOW=20

# Cache settings
REDIS_URL=redis://localhost:6379
CACHE_TTL=3600

# Search settings
MAX_SEARCH_RESULTS=1000
SEARCH_TIMEOUT=30
```

### Configuration Files

#### Application Config
Create `config.py`:
```python
import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key'
    DATABASE = os.environ.get('DATABASE_PATH') or 'torrents.db'
    RESULTS_PER_PAGE = int(os.environ.get('RESULTS_PER_PAGE', 20))
    MAX_SEARCH_LENGTH = int(os.environ.get('MAX_SEARCH_LENGTH', 100))
    
    # Logging
    LOG_LEVEL = os.environ.get('LOG_LEVEL', 'INFO')
    LOG_FILE = os.environ.get('LOG_FILE', 'app.log')
    
    # Performance
    DB_POOL_SIZE = int(os.environ.get('DB_POOL_SIZE', 10))
    CACHE_TTL = int(os.environ.get('CACHE_TTL', 3600))

class DevelopmentConfig(Config):
    DEBUG = True
    FLASK_ENV = 'development'

class ProductionConfig(Config):
    DEBUG = False
    FLASK_ENV = 'production'
```

## Monitoring

### 1. Health Monitoring
```bash
# Health check script
#!/bin/bash
HEALTH_URL="http://localhost:5000/health"
RESPONSE=$(curl -s $HEALTH_URL)
STATUS=$(echo $RESPONSE | jq -r '.status')

if [ "$STATUS" = "healthy" ]; then
    echo "Application is healthy"
    exit 0
else
    echo "Application is unhealthy"
    exit 1
fi
```

### 2. Log Monitoring
```bash
# Log rotation
sudo nano /etc/logrotate.d/btdig-clone
```

Log rotation configuration:
```
/var/log/btdig-clone/*.log {
    daily
    missingok
    rotate 52
    compress
    delaycompress
    notifempty
    create 644 www-data www-data
    postrotate
        systemctl reload btdig-clone
    endscript
}
```

### 3. Performance Monitoring
```bash
# Install monitoring tools
sudo apt install -y htop iotop nethogs

# Monitor application
htop
iotop
nethogs
```

### 4. Database Monitoring
```bash
# Check database size
du -h /var/lib/btdig-clone/torrents.db

# Check database integrity
sqlite3 /var/lib/btdig-clone/torrents.db "PRAGMA integrity_check;"

# Database statistics
sqlite3 /var/lib/btdig-clone/torrents.db "SELECT COUNT(*) FROM torrents;"
```

## Troubleshooting

### Common Issues

#### Application Won't Start
```bash
# Check logs
sudo journalctl -u btdig-clone -f

# Check port availability
sudo netstat -tlnp | grep :5000

# Check permissions
ls -la /var/lib/btdig-clone/
```

#### Database Issues
```bash
# Check database file
ls -la /var/lib/btdig-clone/torrents.db

# Repair database
sqlite3 /var/lib/btdig-clone/torrents.db "VACUUM;"

# Recreate database
sudo -u www-data python3 /opt/btdg/backend/db/seed_data.py
```

#### Performance Issues
```bash
# Check system resources
htop
df -h
free -h

# Check application logs
tail -f /var/log/btdig-clone/app.log

# Database optimization
sqlite3 /var/lib/btdig-clone/torrents.db "ANALYZE;"
```

### Debug Commands
```bash
# Test application
curl http://localhost:5000/health

# Test search
curl "http://localhost:5000/api/search?q=ubuntu"

# Check Docker containers
docker ps
docker logs btdig-clone

# Check nginx
sudo nginx -t
sudo systemctl status nginx
```

### Recovery Procedures

#### Application Recovery
```bash
# Restart application
sudo systemctl restart btdig-clone

# Restart Docker containers
docker-compose restart

# Check application status
sudo systemctl status btdig-clone
```

#### Database Recovery
```bash
# Restore from backup
sudo cp /var/backups/btdig-clone/torrents_20240101_120000.db.gz /tmp/
sudo gunzip /tmp/torrents_20240101_120000.db.gz
sudo cp /tmp/torrents_20240101_120000.db /var/lib/btdig-clone/torrents.db
sudo chown www-data:www-data /var/lib/btdig-clone/torrents.db
```

---

## Quick Reference

### Commands
```bash
# Start application
docker-compose up -d
sudo systemctl start btdig-clone

# Stop application
docker-compose down
sudo systemctl stop btdig-clone

# View logs
docker-compose logs -f
sudo journalctl -u btdig-clone -f

# Health check
curl http://localhost:5000/health

# Backup database
sudo /opt/btdg/backup.sh
```

### URLs
- **Application**: http://localhost:5000
- **Health Check**: http://localhost:5000/health
- **API**: http://localhost:5000/api/search?q=test
- **RSS Feed**: http://localhost:5000/rss.xml

### Files
- **Application**: /opt/btdg/
- **Database**: /var/lib/btdig-clone/torrents.db
- **Logs**: /var/log/btdig-clone/
- **Backups**: /var/backups/btdig-clone/
- **Configuration**: /etc/systemd/system/btdig-clone.service

---

*This deployment guide covers all aspects of deploying the BTDigg Clone application. For additional support, refer to the main README or create an issue on GitHub.*
