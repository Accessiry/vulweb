# Deployment Guide

This guide covers various deployment scenarios for the VulWeb platform.

## Table of Contents
- [Docker Deployment](#docker-deployment)
- [Manual Deployment](#manual-deployment)
- [Production Considerations](#production-considerations)
- [Scaling](#scaling)
- [Monitoring](#monitoring)

## Docker Deployment

### Quick Deploy

The fastest way to deploy the platform using Docker Compose:

```bash
# Clone the repository
git clone https://github.com/Accessiry/vulweb.git
cd vulweb

# Set environment variables (optional)
export SECRET_KEY="your-production-secret-key"

# Start all services
docker-compose up -d

# View logs
docker-compose logs -f

# Check status
docker-compose ps
```

Services will be available at:
- Frontend: http://localhost (port 80)
- Backend API: http://localhost:5000
- Redis: http://localhost:6379

### Custom Configuration

1. **Environment Variables**

Create a `.env` file in the root directory:

```env
SECRET_KEY=your-secret-key-here
FLASK_ENV=production
DATABASE_URL=sqlite:///app.db
CELERY_BROKER_URL=redis://redis:6379/0
CELERY_RESULT_BACKEND=redis://redis:6379/0
```

2. **Persistent Storage**

Modify `docker-compose.yml` to use named volumes:

```yaml
volumes:
  - ./backend/uploads:/app/uploads
  - ./backend/training_outputs:/app/training_outputs
  - ./backend/app.db:/app/app.db
```

3. **Custom Port**

Change the port mapping in `docker-compose.yml`:

```yaml
frontend:
  ports:
    - "8080:80"  # Access via http://localhost:8080
```

### SSL/HTTPS Setup

For production, use a reverse proxy like nginx with SSL:

1. **Install Certbot**
```bash
sudo apt-get install certbot python3-certbot-nginx
```

2. **Obtain SSL Certificate**
```bash
sudo certbot --nginx -d yourdomain.com
```

3. **Update nginx configuration**

Create `/etc/nginx/sites-available/vulweb`:

```nginx
server {
    listen 80;
    server_name yourdomain.com;
    return 301 https://$server_name$request_uri;
}

server {
    listen 443 ssl http2;
    server_name yourdomain.com;

    ssl_certificate /etc/letsencrypt/live/yourdomain.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/yourdomain.com/privkey.pem;

    location / {
        proxy_pass http://localhost:80;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    location /api {
        proxy_pass http://localhost:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

4. **Enable and restart nginx**
```bash
sudo ln -s /etc/nginx/sites-available/vulweb /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

## Manual Deployment

### Prerequisites

- Ubuntu 20.04+ or similar Linux distribution
- Python 3.10+
- Node.js 18+
- Redis
- Nginx (optional, for production)

### Backend Deployment

1. **Install system dependencies**
```bash
sudo apt-get update
sudo apt-get install python3.10 python3.10-venv python3-pip redis-server
```

2. **Set up application**
```bash
# Clone repository
git clone https://github.com/Accessiry/vulweb.git
cd vulweb/backend

# Create virtual environment
python3.10 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Set up environment
cp .env.example .env
# Edit .env with production settings
```

3. **Configure systemd service**

Create `/etc/systemd/system/vulweb-backend.service`:

```ini
[Unit]
Description=VulWeb Backend
After=network.target

[Service]
Type=simple
User=www-data
WorkingDirectory=/var/www/vulweb/backend
Environment="PATH=/var/www/vulweb/backend/venv/bin"
ExecStart=/var/www/vulweb/backend/venv/bin/gunicorn --bind 0.0.0.0:5000 --workers 4 run:app
Restart=always

[Install]
WantedBy=multi-user.target
```

4. **Configure Celery worker**

Create `/etc/systemd/system/vulweb-celery.service`:

```ini
[Unit]
Description=VulWeb Celery Worker
After=network.target redis.service

[Service]
Type=simple
User=www-data
WorkingDirectory=/var/www/vulweb/backend
Environment="PATH=/var/www/vulweb/backend/venv/bin"
ExecStart=/var/www/vulweb/backend/venv/bin/celery -A app.celery worker --loglevel=info
Restart=always

[Install]
WantedBy=multi-user.target
```

5. **Start services**
```bash
sudo systemctl daemon-reload
sudo systemctl enable vulweb-backend vulweb-celery redis
sudo systemctl start vulweb-backend vulweb-celery redis
```

### Frontend Deployment

1. **Build frontend**
```bash
cd vulweb/frontend
npm install
npm run build
```

2. **Configure nginx**

Create `/etc/nginx/sites-available/vulweb`:

```nginx
server {
    listen 80;
    server_name localhost;
    
    root /var/www/vulweb/frontend/build;
    index index.html;

    location / {
        try_files $uri $uri/ /index.html;
    }

    location /api {
        proxy_pass http://localhost:5000;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host $host;
        proxy_cache_bypass $http_upgrade;
    }
}
```

3. **Enable and start nginx**
```bash
sudo ln -s /etc/nginx/sites-available/vulweb /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

## Production Considerations

### Security

1. **Change Secret Key**
```bash
# Generate a strong secret key
python3 -c "import secrets; print(secrets.token_hex(32))"
```

2. **Database Security**
- Use PostgreSQL instead of SQLite for production
- Enable SSL connections
- Regular backups

3. **File Upload Security**
- Implement file size limits
- Scan uploaded files for malware
- Use separate storage for uploads

4. **API Security**
- Implement rate limiting
- Add authentication and authorization
- Use HTTPS only
- Enable CORS properly

### Performance

1. **Database Optimization**

Switch to PostgreSQL:

```python
# In config/config.py
DATABASE_URL = 'postgresql://user:pass@localhost/vulweb'
```

2. **Caching**

Add Redis caching for frequently accessed data:

```python
from flask_caching import Cache

cache = Cache(config={'CACHE_TYPE': 'redis', 'CACHE_REDIS_URL': 'redis://localhost:6379/1'})
cache.init_app(app)
```

3. **CDN for Frontend**
- Use a CDN for static assets
- Enable gzip compression
- Optimize images

### Monitoring

1. **Application Monitoring**

Add logging configuration:

```python
import logging
from logging.handlers import RotatingFileHandler

handler = RotatingFileHandler('logs/app.log', maxBytes=10000000, backupCount=3)
handler.setLevel(logging.INFO)
app.logger.addHandler(handler)
```

2. **Health Checks**

The platform includes health check endpoints:

```bash
# Check backend health
curl http://localhost:5000/health

# Check if services are running
systemctl status vulweb-backend
systemctl status vulweb-celery
systemctl status redis
```

3. **Error Tracking**

Integrate with error tracking services (e.g., Sentry):

```python
import sentry_sdk
from sentry_sdk.integrations.flask import FlaskIntegration

sentry_sdk.init(
    dsn="your-sentry-dsn",
    integrations=[FlaskIntegration()],
)
```

### Backup Strategy

1. **Database Backup**

For SQLite:
```bash
# Automated backup script
#!/bin/bash
DATE=$(date +%Y%m%d_%H%M%S)
cp /var/www/vulweb/backend/app.db /backups/app_${DATE}.db
```

For PostgreSQL:
```bash
pg_dump vulweb > backup_$(date +%Y%m%d).sql
```

2. **File Backup**
```bash
# Backup uploads and training outputs
tar -czf backup_files_$(date +%Y%m%d).tar.gz \
    /var/www/vulweb/backend/uploads \
    /var/www/vulweb/backend/training_outputs
```

## Scaling

### Horizontal Scaling

1. **Multiple Backend Instances**

Use a load balancer (nginx) to distribute requests:

```nginx
upstream backend_servers {
    server backend1:5000;
    server backend2:5000;
    server backend3:5000;
}

server {
    location /api {
        proxy_pass http://backend_servers;
    }
}
```

2. **Celery Workers**

Add more Celery workers:

```bash
# Start multiple workers
celery -A app.celery worker --loglevel=info --concurrency=4 -n worker1@%h &
celery -A app.celery worker --loglevel=info --concurrency=4 -n worker2@%h &
```

### Database Scaling

1. **PostgreSQL with Read Replicas**

```python
# Configure read/write splitting
SQLALCHEMY_DATABASE_URI = 'postgresql://user:pass@primary/vulweb'
SQLALCHEMY_BINDS = {
    'read': 'postgresql://user:pass@replica/vulweb'
}
```

2. **Connection Pooling**

```python
SQLALCHEMY_ENGINE_OPTIONS = {
    'pool_size': 10,
    'max_overflow': 20,
    'pool_recycle': 3600,
}
```

## Troubleshooting

### Common Issues

1. **Backend won't start**
```bash
# Check logs
journalctl -u vulweb-backend -f

# Check permissions
sudo chown -R www-data:www-data /var/www/vulweb
```

2. **Database connection issues**
```bash
# Verify database exists
sqlite3 app.db ".tables"

# Check database permissions
ls -la app.db
```

3. **Celery tasks not running**
```bash
# Check Redis is running
redis-cli ping

# Check Celery worker status
celery -A app.celery inspect active
```

4. **Frontend not updating**
```bash
# Clear browser cache
# Rebuild frontend
cd frontend && npm run build
```

## Maintenance

### Regular Tasks

1. **Update Dependencies**
```bash
# Backend
cd backend
source venv/bin/activate
pip list --outdated
pip install -U package_name

# Frontend
cd frontend
npm outdated
npm update
```

2. **Clean Old Training Data**
```bash
# Remove training outputs older than 30 days
find /var/www/vulweb/backend/training_outputs -mtime +30 -delete
```

3. **Monitor Disk Space**
```bash
df -h
du -sh /var/www/vulweb/backend/uploads/*
```

## Support

For deployment issues:
- Check logs in `/var/log/nginx/` and application logs
- Review systemd service status
- Check Redis and database connectivity
- Ensure all ports are accessible

For additional help, create an issue on GitHub.
