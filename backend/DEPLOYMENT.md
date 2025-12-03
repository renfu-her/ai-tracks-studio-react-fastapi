# Deployment Guide 部署指南

## Production Deployment 生產環境部署

### Using Gunicorn with Uvicorn Workers

Gunicorn is a production-grade WSGI HTTP server. When combined with Uvicorn workers, it provides the best performance for FastAPI applications.

### Quick Start 快速開始

```bash
cd backend

# Install dependencies
uv sync

# Run production server
uv run gunicorn app.main:app \
  --workers 4 \
  --worker-class uvicorn.workers.UvicornWorker \
  --bind 0.0.0.0:8000
```

### Recommended Production Configuration 推薦的生產配置

```bash
uv run gunicorn app.main:app \
  --workers 4 \
  --worker-class uvicorn.workers.UvicornWorker \
  --bind 0.0.0.0:8000 \
  --timeout 60 \
  --keepalive 5 \
  --access-logfile - \
  --error-logfile - \
  --log-level info \
  --max-requests 1000 \
  --max-requests-jitter 50
```

### Worker Configuration 工作進程配置

#### Calculate Optimal Workers 計算最佳工作進程數

Formula: `(2 x CPU cores) + 1`

```bash
# For 2 CPU cores: (2 x 2) + 1 = 5 workers
# For 4 CPU cores: (2 x 4) + 1 = 9 workers
# For 8 CPU cores: (2 x 8) + 1 = 17 workers
```

#### Using Configuration File 使用配置文件

Create `gunicorn.conf.py`:

```python
import multiprocessing

# Server socket
bind = "0.0.0.0:8000"
backlog = 2048

# Worker processes
workers = multiprocessing.cpu_count() * 2 + 1
worker_class = "uvicorn.workers.UvicornWorker"
worker_connections = 1000
timeout = 60
keepalive = 5

# Restart workers after this many requests (with some jitter)
max_requests = 1000
max_requests_jitter = 50

# Logging
accesslog = "-"
errorlog = "-"
loglevel = "info"
access_log_format = '%(h)s %(l)s %(u)s %(t)s "%(r)s" %(s)s %(b)s "%(f)s" "%(a)s" %(D)s'

# Process naming
proc_name = "ai-tracks-studio-api"

# Server mechanics
daemon = False
pidfile = None
umask = 0
```

Then run:
```bash
uv run gunicorn app.main:app --config gunicorn.conf.py
```

### Using Systemd Service (Linux) 使用 Systemd 服務

Create `/etc/systemd/system/studio-api.service`:

```ini
[Unit]
Description=AI-Tracks Studio API
After=network.target mysql.service

[Service]
Type=notify
User=www-data
Group=www-data
WorkingDirectory=/path/to/studio/backend
Environment="PATH=/path/to/studio/backend/.venv/bin"
ExecStart=/path/to/studio/backend/.venv/bin/gunicorn app.main:app \
  --workers 4 \
  --worker-class uvicorn.workers.UvicornWorker \
  --bind 0.0.0.0:8000 \
  --access-logfile /var/log/studio-api/access.log \
  --error-logfile /var/log/studio-api/error.log
ExecReload=/bin/kill -s HUP $MAINPID
KillMode=mixed
TimeoutStopSec=5
PrivateTmp=true

[Install]
WantedBy=multi-user.target
```

Manage service:
```bash
# Start service
sudo systemctl start studio-api

# Enable on boot
sudo systemctl enable studio-api

# View status
sudo systemctl status studio-api

# View logs
sudo journalctl -u studio-api -f

# Restart
sudo systemctl restart studio-api

# Reload configuration
sudo systemctl reload studio-api
```

### Using Docker 使用 Docker

Create `Dockerfile`:

```dockerfile
FROM python:3.14-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Install uv
RUN pip install uv

# Copy project files
COPY pyproject.toml .
COPY app ./app

# Install dependencies
RUN uv sync --no-dev

# Expose port
EXPOSE 8000

# Run with gunicorn
CMD ["uv", "run", "gunicorn", "app.main:app", \
     "--workers", "4", \
     "--worker-class", "uvicorn.workers.UvicornWorker", \
     "--bind", "0.0.0.0:8000"]
```

Build and run:
```bash
# Build image
docker build -t studio-api .

# Run container
docker run -d \
  --name studio-api \
  -p 8000:8000 \
  -e DB_HOST=host.docker.internal \
  studio-api

# View logs
docker logs -f studio-api
```

### Using Docker Compose 使用 Docker Compose

Create `docker-compose.yml`:

```yaml
version: '3.8'

services:
  api:
    build: .
    ports:
      - "8000:8000"
    environment:
      - DB_HOST=mysql
      - DB_PORT=3306
      - DB_USER=root
      - DB_PASSWORD=
      - DB_NAME=studio
    depends_on:
      - mysql
    restart: unless-stopped

  mysql:
    image: mysql:8.0
    environment:
      MYSQL_ROOT_PASSWORD: ""
      MYSQL_DATABASE: studio
      MYSQL_ALLOW_EMPTY_PASSWORD: "yes"
    ports:
      - "3306:3306"
    volumes:
      - mysql_data:/var/lib/mysql
    restart: unless-stopped

volumes:
  mysql_data:
```

Run:
```bash
docker-compose up -d
```

### Nginx Reverse Proxy Nginx 反向代理

Create `/etc/nginx/sites-available/studio-api`:

```nginx
upstream studio_api {
    server 127.0.0.1:8000;
}

server {
    listen 80;
    server_name api.yourdomain.com;

    # Client body size limit
    client_max_body_size 10M;

    # Timeouts
    proxy_connect_timeout 60s;
    proxy_send_timeout 60s;
    proxy_read_timeout 60s;

    location / {
        proxy_pass http://studio_api;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    # Health check endpoint
    location /health {
        proxy_pass http://studio_api/health;
        access_log off;
    }
}
```

Enable and reload:
```bash
sudo ln -s /etc/nginx/sites-available/studio-api /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl reload nginx
```

### Environment Variables 環境變數

For production, create `.env` file:

```env
# Database
DB_HOST=localhost
DB_PORT=3306
DB_USER=studio_user
DB_PASSWORD=your_secure_password
DB_NAME=studio

# API
API_PREFIX=/api
CORS_ORIGINS=["https://yourdomain.com"]

# Production settings
ENVIRONMENT=production
DEBUG=false
```

### Performance Tuning 性能調優

1. **Worker Count**: `(2 x CPU cores) + 1`
2. **Timeout**: 30-120 seconds depending on workload
3. **Keepalive**: 2-5 seconds
4. **Max Requests**: 1000-5000 (prevents memory leaks)
5. **Worker Class**: Always use `uvicorn.workers.UvicornWorker` for FastAPI

### Monitoring 監控

#### Health Check Endpoint

```bash
curl http://localhost:8000/health
```

Response:
```json
{"status": "healthy"}
```

#### Logs

```bash
# View access logs
tail -f /var/log/studio-api/access.log

# View error logs
tail -f /var/log/studio-api/error.log

# With systemd
sudo journalctl -u studio-api -f
```

### Security Checklist 安全檢查清單

- [ ] Use strong database password
- [ ] Configure CORS origins properly
- [ ] Enable HTTPS (SSL/TLS)
- [ ] Set up firewall rules
- [ ] Keep dependencies updated
- [ ] Use environment variables for secrets
- [ ] Enable rate limiting (if needed)
- [ ] Regular security audits

### Backup 備份

```bash
# Backup database
mysqldump -u root studio > backup_$(date +%Y%m%d).sql

# Restore database
mysql -u root studio < backup_20250101.sql
```

## Support 支援

For issues or questions:
- Check application logs
- Review [README.md](./README.md)
- Test endpoints with [API_DOCUMENTATION.md](./API_DOCUMENTATION.md)

