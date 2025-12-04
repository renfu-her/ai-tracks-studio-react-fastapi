# 生產環境完整部署指南 Production Deployment Guide

## 🔍 當前問題

### 問題 1：頁面一直「載入中...」
- 前端無法連接到後端 API
- API 請求失敗或超時

### 問題 2：靜態資源 404 錯誤
```
GET https://studio.ai-tracks.com/index.css net::ERR_ABORTED 404
```
- 前端靜態文件沒有正確部署

## 🎯 完整解決方案

### 架構說明

```
用戶瀏覽器
    ↓
Nginx (studio.ai-tracks.com)
    ↓
    ├─→ 前端靜態文件 (React)
    └─→ 後端 API (FastAPI on 127.0.0.1:9001)
```

## 📋 步驟 1：部署後端

### 1.1 確認後端運行

```bash
# SSH 到服務器
cd /home/ai-tracks-studio/htdocs/studio.ai-tracks.com/backend

# 檢查 Python 版本
uv run python --version
# 應該是 3.12.x

# 測試後端
uv run uvicorn app.main:app --host 127.0.0.1 --port 9001

# 在另一個終端測試
curl http://127.0.0.1:9001/
curl http://127.0.0.1:9001/api/projects
```

### 1.2 確認靜態文件存在

```bash
cd /home/ai-tracks-studio/htdocs/studio.ai-tracks.com/backend

# 檢查後端靜態文件
ls -la app/static/js/
# 應該有：admin.js, template-loader.js, common-ui.js

# 測試訪問
curl http://127.0.0.1:9001/static/js/admin.js
```

### 1.3 使用正確的 Service 文件

```bash
# 使用 working service
sudo cp backend/studio-uvicorn-working.service \
    /etc/systemd/system/studio-uvicorn.service

sudo systemctl daemon-reload
sudo systemctl restart studio-uvicorn
sudo systemctl status studio-uvicorn
```

## 📋 步驟 2：構建前端

### 2.1 創建生產環境配置

在**開發機器**上（Windows）：

```bash
cd d:\python\studio\frontend

# 創建 .env.production 文件
```

創建 `frontend/.env.production`：
```env
VITE_API_BASE_URL=https://studio.ai-tracks.com
```

### 2.2 構建生產版本

```bash
cd d:\python\studio\frontend

# 安裝依賴（如果還沒安裝）
npm install

# 構建生產版本
npm run build
```

這會在 `frontend/dist/` 目錄生成生產文件。

### 2.3 檢查構建結果

```bash
cd d:\python\studio\frontend\dist

# 應該看到：
# - index.html
# - assets/
#   - index-*.js
#   - index-*.css
```

## 📋 步驟 3：部署前端到服務器

### 3.1 上傳構建文件

**方法 A：使用 Git**

```bash
# 在開發機器上
cd d:\python\studio
git add frontend/dist
git add frontend/.env.production
git commit -m "Add production build"
git push origin main

# 在生產服務器上
cd /home/ai-tracks-studio/htdocs/studio.ai-tracks.com
git pull origin main
```

**方法 B：使用 SCP**

```bash
# 在開發機器上
scp -r d:\python\studio\frontend\dist\* \
    ai-tracks-studio@your-server:/home/ai-tracks-studio/htdocs/studio.ai-tracks.com/frontend/dist/
```

**方法 C：使用 FTP/SFTP 客戶端**

使用 FileZilla 或 WinSCP 上傳 `frontend/dist/` 目錄的內容。

### 3.2 在服務器上設置前端目錄

```bash
# 創建前端目錄
mkdir -p /home/ai-tracks-studio/htdocs/studio.ai-tracks.com/public

# 複製構建文件
cp -r /home/ai-tracks-studio/htdocs/studio.ai-tracks.com/frontend/dist/* \
    /home/ai-tracks-studio/htdocs/studio.ai-tracks.com/public/

# 或者直接使用 dist 目錄
ln -s /home/ai-tracks-studio/htdocs/studio.ai-tracks.com/frontend/dist \
    /home/ai-tracks-studio/htdocs/studio.ai-tracks.com/public
```

## 📋 步驟 4：配置 Nginx

### 4.1 創建 Nginx 配置

創建 `/etc/nginx/sites-available/studio.ai-tracks.com`：

```nginx
server {
    listen 80;
    listen [::]:80;
    server_name studio.ai-tracks.com;

    # SSL configuration (if using HTTPS)
    # listen 443 ssl http2;
    # ssl_certificate /path/to/cert.pem;
    # ssl_certificate_key /path/to/key.pem;

    # Root directory for frontend
    root /home/ai-tracks-studio/htdocs/studio.ai-tracks.com/public;
    index index.html;

    # Frontend static files
    location / {
        try_files $uri $uri/ /index.html;
    }

    # Backend API
    location /api/ {
        proxy_pass http://127.0.0.1:9001;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        
        # CORS headers (handled by FastAPI, but can add here too)
        add_header Access-Control-Allow-Origin * always;
    }

    # Backend static files (uploads, admin JS, etc.)
    location /static/ {
        proxy_pass http://127.0.0.1:9001/static/;
        proxy_set_header Host $host;
    }

    # Backend admin interface
    location /backend {
        proxy_pass http://127.0.0.1:9001/backend;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    # Increase upload size limit
    client_max_body_size 10M;

    # Gzip compression
    gzip on;
    gzip_vary on;
    gzip_min_length 10240;
    gzip_proxied expired no-cache no-store private must-revalidate auth;
    gzip_types text/plain text/css text/xml text/javascript application/javascript application/xml+rss application/json;
}
```

### 4.2 啟用站點並測試

```bash
# 創建符號連結
sudo ln -s /etc/nginx/sites-available/studio.ai-tracks.com \
    /etc/nginx/sites-enabled/

# 測試配置
sudo nginx -t

# 重啟 Nginx
sudo systemctl restart nginx

# 檢查狀態
sudo systemctl status nginx
```

## 📋 步驟 5：驗證部署

### 5.1 檢查後端

```bash
# 後端健康檢查
curl http://127.0.0.1:9001/health

# API 測試
curl http://127.0.0.1:9001/api/projects

# 靜態文件測試
curl http://127.0.0.1:9001/static/js/admin.js
```

### 5.2 檢查前端

```bash
# 通過 Nginx 訪問
curl http://localhost/
# 應該返回 HTML

# 檢查靜態文件
curl http://localhost/assets/
```

### 5.3 瀏覽器測試

1. **訪問前端：** https://studio.ai-tracks.com
   - 應該看到首頁，不是「載入中...」

2. **打開開發者工具：**
   - Network tab：檢查 API 請求
   - Console tab：應該沒有 404 錯誤

3. **測試功能：**
   - 瀏覽遊戲列表
   - 瀏覽網站列表
   - 查看新聞

4. **測試後台：** https://studio.ai-tracks.com/backend
   - 應該能登入
   - 沒有 JS 文件 404 錯誤

## 🔧 故障排除

### 問題 1：前端一直「載入中...」

**原因：** API 請求失敗

**檢查：**
```bash
# 在瀏覽器控制台查看 Network tab
# 應該看到 API 請求到 /api/projects, /api/news 等

# 如果請求失敗，檢查：
sudo journalctl -u studio-uvicorn -n 50
```

**解決：**
- 確認後端運行：`sudo systemctl status studio-uvicorn`
- 檢查 CORS 配置
- 確認 `.env.production` 中的 API URL 正確

### 問題 2：404 錯誤 - 找不到 CSS/JS

**原因：** 前端文件沒有正確部署

**檢查：**
```bash
# 檢查前端文件
ls -la /home/ai-tracks-studio/htdocs/studio.ai-tracks.com/public/
# 應該有 index.html 和 assets/ 目錄

# 檢查 Nginx 配置
sudo nginx -t
```

**解決：**
- 重新構建並上傳前端文件
- 檢查 Nginx root 路徑
- 清除瀏覽器緩存

### 問題 3：API 請求 CORS 錯誤

**症狀：** 
```
Access to fetch at 'https://studio.ai-tracks.com/api/projects' 
from origin 'https://studio.ai-tracks.com' has been blocked by CORS policy
```

**解決：**

檢查後端 `backend/app/config.py`：
```python
CORS_ORIGINS: Union[str, list[str]] = ["https://studio.ai-tracks.com", ...]
```

更新 `.env`：
```env
CORS_ORIGINS=https://studio.ai-tracks.com,http://localhost:9001
```

重啟後端：
```bash
sudo systemctl restart studio-uvicorn
```

### 問題 4：Nginx 502 Bad Gateway

**原因：** 後端沒有運行或端口錯誤

**檢查：**
```bash
# 檢查後端
sudo systemctl status studio-uvicorn

# 檢查端口
sudo lsof -ti:9001
```

## 📊 部署檢查清單

### 後端
- [ ] Python 3.12 環境
- [ ] 所有依賴已安裝（`uv sync`）
- [ ] `.env` 文件配置正確
- [ ] 靜態文件存在（`app/static/js/`）
- [ ] Service 運行（`studio-uvicorn.service`）
- [ ] 可以訪問 `http://127.0.0.1:9001/`
- [ ] API 端點正常（`/api/projects`, `/api/news`）

### 前端
- [ ] 構建完成（`npm run build`）
- [ ] `.env.production` 配置正確
- [ ] `dist/` 文件上傳到服務器
- [ ] 文件複製到 `public/` 目錄
- [ ] `index.html` 存在

### Nginx
- [ ] 配置文件已創建
- [ ] 配置測試通過（`nginx -t`）
- [ ] 站點已啟用
- [ ] Nginx 已重啟
- [ ] 可以訪問 https://studio.ai-tracks.com

### 瀏覽器
- [ ] 首頁正常顯示（不是載入中）
- [ ] 沒有 404 錯誤
- [ ] 沒有 CORS 錯誤
- [ ] API 請求成功
- [ ] 圖片正常顯示

## 🚀 快速部署腳本

創建 `deploy.sh`：

```bash
#!/bin/bash
set -e

echo "Deploying AI-Tracks Studio..."

# 1. Pull latest code
cd /home/ai-tracks-studio/htdocs/studio.ai-tracks.com
git pull origin main

# 2. Backend
cd backend
uv sync
chmod -R 755 app/static
sudo systemctl restart studio-uvicorn

# 3. Frontend
cd ../frontend
if [ -d "dist" ]; then
    rm -rf ../public/*
    cp -r dist/* ../public/
    echo "Frontend deployed"
else
    echo "Warning: frontend/dist not found. Run 'npm run build' first."
fi

# 4. Nginx
sudo nginx -t && sudo systemctl reload nginx

# 5. Check
echo ""
echo "Checking services..."
sudo systemctl status studio-uvicorn --no-pager
sudo systemctl status nginx --no-pager

echo ""
echo "Deployment complete!"
echo "Visit: https://studio.ai-tracks.com"
```

使用：
```bash
chmod +x deploy.sh
./deploy.sh
```

## 📝 總結

1. **後端**：FastAPI 運行在 127.0.0.1:9001
2. **前端**：React 構建後的靜態文件
3. **Nginx**：反向代理，處理前端和後端請求
4. **域名**：studio.ai-tracks.com 指向 Nginx

完成這些步驟後，你的網站應該完全正常運行！🎉

