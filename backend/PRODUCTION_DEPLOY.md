# Production Deployment Guide 生產環境部署指南

## Quick Start 快速啟動

### Method 1: Using Start Script (Recommended) 使用啟動腳本（推薦）

```bash
cd /home/ai-tracks-studio/htdocs/studio.ai-tracks.com/backend
chmod +x start.sh
./start.sh
```

### Method 2: Direct Uvicorn Command 直接使用 Uvicorn 命令

```bash
cd /home/ai-tracks-studio/htdocs/studio.ai-tracks.com/backend
uv run uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 4
```

### Method 3: Gunicorn with Uvicorn Workers (Alternative) 使用 Gunicorn

⚠️ **IMPORTANT**: You MUST run this from the `backend/` directory!

```bash
cd /home/ai-tracks-studio/htdocs/studio.ai-tracks.com/backend
uv run gunicorn app.main:app \
  --workers 4 \
  --worker-class uvicorn.workers.UvicornWorker \
  --bind 0.0.0.0:8000 \
  --timeout 60 \
  --access-logfile - \
  --error-logfile -
```

## Common Issues 常見問題

### ModuleNotFoundError: No module named 'app'

**Problem**: Gunicorn/Uvicorn cannot find the `app` module.

**Solution**: Make sure you're running the command from the `backend/` directory:

```bash
# Wrong (will fail) ❌
gunicorn app.main:app

# Correct (will work) ✅
cd /path/to/backend
gunicorn app.main:app
```

### Port Already in Use

**Problem**: Port 8000 is already in use.

**Solution**: 
1. Kill the existing process:
```bash
lsof -ti:8000 | xargs kill -9
```

2. Or use a different port:
```bash
uv run uvicorn app.main:app --host 0.0.0.0 --port 8001
```

## Environment Variables 環境變數

Make sure your `.env` file in the `backend/` directory contains:

```env
DB_HOST=localhost
DB_PORT=3306
DB_USER=studio
DB_PASSWORD=your-password
DB_NAME=studio
SECRET_KEY=your-secret-key
ENVIRONMENT=production
DEBUG=False
CORS_ORIGINS=https://studio.ai-tracks.com,http://localhost:9001
```

## Running as a Service 作為服務運行

### Using systemd

Create `/etc/systemd/system/ai-tracks-studio.service`:

```ini
[Unit]
Description=AI-Tracks Studio Backend API
After=network.target mysql.service

[Service]
Type=simple
User=ai-tracks-studio
WorkingDirectory=/home/ai-tracks-studio/htdocs/studio.ai-tracks.com/backend
ExecStart=/home/ai-tracks-studio/htdocs/studio.ai-tracks.com/backend/start.sh
Restart=always
RestartSec=10
StandardOutput=journal
StandardError=journal

[Install]
WantedBy=multi-user.target
```

Enable and start the service:

```bash
sudo systemctl daemon-reload
sudo systemctl enable ai-tracks-studio
sudo systemctl start ai-tracks-studio
sudo systemctl status ai-tracks-studio
```

View logs:

```bash
sudo journalctl -u ai-tracks-studio -f
```

## Performance Tuning 性能調優

### Worker Count 工作進程數

Recommended formula: `(2 x CPU cores) + 1`

For a 4-core server:
```bash
--workers 9
```

### Timeout Settings 超時設定

For long-running requests:
```bash
--timeout 120
```

### Keep-Alive 保持連接

```bash
--keep-alive 5
```

## Nginx Configuration Nginx 配置

Example Nginx reverse proxy config:

```nginx
server {
    listen 80;
    server_name studio.ai-tracks.com;

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        
        # WebSocket support (if needed)
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
    }

    # Increase upload size limit
    client_max_body_size 10M;
}
```

## Monitoring 監控

### Check if server is running 檢查服務是否運行

```bash
curl http://localhost:8000/docs
```

### Check logs 查看日誌

```bash
# If running as systemd service
sudo journalctl -u ai-tracks-studio -n 100

# If running in terminal
# Check the terminal output
```

### Check process 檢查進程

```bash
ps aux | grep uvicorn
# or
ps aux | grep gunicorn
```

## Security Checklist 安全檢查清單

- [ ] Change `SECRET_KEY` in production
- [ ] Change `SESSION_SECRET_KEY` in production
- [ ] Change default admin password
- [ ] Set `DEBUG=False` in production
- [ ] Set `ENVIRONMENT=production`
- [ ] Configure proper CORS origins
- [ ] Use HTTPS (SSL/TLS)
- [ ] Set up firewall rules
- [ ] Regular security updates
- [ ] Database backups

## Troubleshooting 故障排除

### Server won't start 服務無法啟動

1. Check if port is available:
```bash
lsof -i:8000
```

2. Check environment variables:
```bash
cd backend
cat .env
```

3. Check database connection:
```bash
mysql -u studio -p studio
```

4. Check Python environment:
```bash
cd backend
uv run python -c "from app.config import settings; print(settings.database_url)"
```

### Cannot connect to MySQL 無法連接 MySQL

```bash
# Test connection
mysql -h localhost -u studio -p studio

# Check if MySQL is running
sudo systemctl status mysql
```

## Resources 資源

- FastAPI Documentation: https://fastapi.tiangolo.com/
- Uvicorn Documentation: https://www.uvicorn.org/
- Gunicorn Documentation: https://gunicorn.org/

