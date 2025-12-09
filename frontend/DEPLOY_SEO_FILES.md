# 部署 SEO 文件指南 Deploy SEO Files Guide

## 問題 Problem

執行以下命令時找不到文件：
```bash
curl https://studio.ai-tracks.com/robots.txt  # 404
curl https://studio.ai-tracks.com/sitemap.xml # 404
```

## 原因 Root Cause

`robots.txt` 和 `sitemap.xml` 在 `frontend/public/` 目錄中，但需要部署到生產服務器的根目錄。

## 解決方案 Solution

### 方法 1: 重新構建並部署前端（推薦）

Vite 會自動將 `public/` 目錄的文件複製到 `dist/` 根目錄。

#### 步驟 Steps:

**1. 在開發機器上重新構建：**

```bash
cd frontend

# 確保文件存在
ls -la public/
# 應該看到:
# - robots.txt
# - sitemap.xml

# 重新構建
npm run build

# 驗證文件在 dist/ 中
ls -la dist/
# 應該看到:
# - robots.txt
# - sitemap.xml
# - index.html
# - assets/
```

**2. 上傳到生產服務器：**

```bash
# 使用 SCP 上傳
scp -r dist/* ai-tracks-studio@your-server:/home/ai-tracks-studio/htdocs/studio.ai-tracks.com/public/

# 或者在服務器上重新構建
ssh ai-tracks-studio@your-server
cd /home/ai-tracks-studio/htdocs/studio.ai-tracks.com/frontend
npm run build
cp -r dist/* ../public/
```

**3. 驗證文件權限：**

```bash
# 在服務器上
cd /home/ai-tracks-studio/htdocs/studio.ai-tracks.com/public/

# 檢查文件是否存在
ls -la | grep -E 'robots.txt|sitemap.xml'

# 確保權限正確
chmod 644 robots.txt sitemap.xml

# 確保所有者正確
chown ai-tracks-studio:ai-tracks-studio robots.txt sitemap.xml
```

**4. 測試訪問：**

```bash
# 本地測試
curl http://localhost:3000/robots.txt
curl http://localhost:3000/sitemap.xml

# 生產測試
curl https://studio.ai-tracks.com/robots.txt
curl https://studio.ai-tracks.com/sitemap.xml
```

### 方法 2: 手動上傳文件（快速修復）

如果不想重新構建整個前端，可以手動上傳這兩個文件。

**1. 從本地複製文件：**

```bash
# 在開發機器上
cd frontend/public

# 使用 SCP 上傳
scp robots.txt ai-tracks-studio@your-server:/home/ai-tracks-studio/htdocs/studio.ai-tracks.com/public/
scp sitemap.xml ai-tracks-studio@your-server:/home/ai-tracks-studio/htdocs/studio.ai-tracks.com/public/
```

**2. 或者直接在服務器上創建：**

```bash
# SSH 到服務器
ssh ai-tracks-studio@your-server
cd /home/ai-tracks-studio/htdocs/studio.ai-tracks.com/public/

# 創建 robots.txt
cat > robots.txt << 'EOF'
# Robots.txt for AI-Tracks Studio
# https://studio.ai-tracks.com

User-agent: *
Allow: /

# Sitemap location
Sitemap: https://studio.ai-tracks.com/sitemap.xml
EOF

# 創建 sitemap.xml
cat > sitemap.xml << 'EOF'
<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
  <url>
    <loc>https://studio.ai-tracks.com/</loc>
    <lastmod>2025-12-04</lastmod>
    <changefreq>weekly</changefreq>
    <priority>1.0</priority>
  </url>
  <url>
    <loc>https://studio.ai-tracks.com/game</loc>
    <lastmod>2025-12-04</lastmod>
    <changefreq>weekly</changefreq>
    <priority>0.9</priority>
  </url>
  <url>
    <loc>https://studio.ai-tracks.com/website</loc>
    <lastmod>2025-12-04</lastmod>
    <changefreq>weekly</changefreq>
    <priority>0.9</priority>
  </url>
  <url>
    <loc>https://studio.ai-tracks.com/news</loc>
    <lastmod>2025-12-04</lastmod>
    <changefreq>daily</changefreq>
    <priority>0.8</priority>
  </url>
  <url>
    <loc>https://studio.ai-tracks.com/about</loc>
    <lastmod>2025-12-04</lastmod>
    <changefreq>monthly</changefreq>
    <priority>0.7</priority>
  </url>
</urlset>
EOF

# 設置權限
chmod 644 robots.txt sitemap.xml
chown ai-tracks-studio:ai-tracks-studio robots.txt sitemap.xml
```

### 方法 3: 檢查 Nginx 配置

確保 Nginx 正確處理這些文件：

```bash
# 在服務器上
sudo nano /etc/nginx/sites-available/studio.ai-tracks.com
```

確認配置包含：

```nginx
server {
    server_name studio.ai-tracks.com;
    
    # 前端靜態文件目錄
    root /home/ai-tracks-studio/htdocs/studio.ai-tracks.com/public;
    index index.html;
    
    # robots.txt 和 sitemap.xml
    location = /robots.txt {
        try_files $uri =404;
        access_log off;
    }
    
    location = /sitemap.xml {
        try_files $uri =404;
        access_log off;
    }
    
    # SPA routing (前端路由)
    location / {
        try_files $uri $uri/ /index.html;
    }
    
    # API 代理
    location /api/ {
        proxy_pass http://127.0.0.1:9001;
        # ... proxy settings
    }
    
    # 後端靜態文件
    location /backend/ {
        proxy_pass http://127.0.0.1:9001/backend/;
        # ... proxy settings
    }
}
```

重新加載 Nginx：

```bash
sudo nginx -t              # 測試配置
sudo systemctl reload nginx # 重新加載
```

## 驗證 Verification

### 1. 檢查文件是否存在

```bash
# 在服務器上
ls -la /home/ai-tracks-studio/htdocs/studio.ai-tracks.com/public/ | grep -E 'robots|sitemap'

# 應該看到：
# -rw-r--r-- 1 ai-tracks-studio ai-tracks-studio  xxx Dec  4 22:00 robots.txt
# -rw-r--r-- 1 ai-tracks-studio ai-tracks-studio xxxx Dec  4 22:00 sitemap.xml
```

### 2. 本地測試（在服務器上）

```bash
curl http://127.0.0.1/robots.txt
curl http://127.0.0.1/sitemap.xml
```

### 3. 生產測試（從外部）

```bash
# 測試 robots.txt
curl https://studio.ai-tracks.com/robots.txt

# 測試 sitemap.xml
curl https://studio.ai-tracks.com/sitemap.xml

# 檢查 HTTP 狀態碼
curl -I https://studio.ai-tracks.com/robots.txt
# 應該返回: HTTP/2 200
```

### 4. 瀏覽器測試

直接在瀏覽器訪問：
- https://studio.ai-tracks.com/robots.txt
- https://studio.ai-tracks.com/sitemap.xml

## 故障排除 Troubleshooting

### 問題 1: 404 Not Found

**可能原因：**
- 文件不存在
- Nginx root 路徑錯誤
- 權限問題

**解決：**
```bash
# 檢查文件
ls -la /home/ai-tracks-studio/htdocs/studio.ai-tracks.com/public/robots.txt

# 檢查 Nginx root
sudo nginx -T | grep "root"

# 檢查權限
sudo chmod 644 /home/ai-tracks-studio/htdocs/studio.ai-tracks.com/public/robots.txt
sudo chmod 644 /home/ai-tracks-studio/htdocs/studio.ai-tracks.com/public/sitemap.xml
```

### 問題 2: 403 Forbidden

**可能原因：**
- 權限不足
- SELinux 阻止

**解決：**
```bash
# 修正權限
sudo chmod 644 robots.txt sitemap.xml
sudo chown www-data:www-data robots.txt sitemap.xml

# 如果啟用了 SELinux
sudo chcon -t httpd_sys_content_t robots.txt sitemap.xml
```

### 問題 3: 內容不對

**可能原因：**
- 緩存問題
- 部署了舊版本

**解決：**
```bash
# 清除瀏覽器緩存
Ctrl+Shift+R (Chrome) or Cmd+Shift+R (Mac)

# 檢查文件內容
cat /home/ai-tracks-studio/htdocs/studio.ai-tracks.com/public/robots.txt

# 重新部署
cd /home/ai-tracks-studio/htdocs/studio.ai-tracks.com/frontend
npm run build
cp -r dist/* ../public/
```

## 快速修復命令 Quick Fix Commands

**一鍵部署 SEO 文件：**

```bash
# SSH 到服務器
ssh ai-tracks-studio@your-server

# 執行以下命令
cd /home/ai-tracks-studio/htdocs/studio.ai-tracks.com

# 從 Git 拉取最新代碼（包含 public/ 文件）
git pull origin main

# 重新構建前端
cd frontend
npm run build

# 複製到 public 目錄
cp -r dist/* ../public/

# 驗證
ls -la ../public/ | grep -E 'robots|sitemap'
curl -I http://127.0.0.1/robots.txt
curl -I http://127.0.0.1/sitemap.xml

# 如果成功，測試生產環境
curl https://studio.ai-tracks.com/robots.txt
curl https://studio.ai-tracks.com/sitemap.xml
```

## 完成檢查清單 Completion Checklist

部署完成後，確認以下項目：

- [ ] `robots.txt` 文件在 `/public/` 目錄
- [ ] `sitemap.xml` 文件在 `/public/` 目錄
- [ ] 文件權限為 644
- [ ] 文件所有者正確（ai-tracks-studio 或 www-data）
- [ ] 本地測試通過（`curl http://127.0.0.1/robots.txt`）
- [ ] 生產測試通過（`curl https://studio.ai-tracks.com/robots.txt`）
- [ ] 瀏覽器可以訪問
- [ ] 提交到 Google Search Console
- [ ] 提交到 Bing Webmaster Tools

## 提交到搜索引擎 Submit to Search Engines

文件部署成功後：

### Google Search Console

1. 訪問：https://search.google.com/search-console
2. 選擇您的網站
3. 左側菜單 → Sitemaps
4. 輸入：`https://studio.ai-tracks.com/sitemap.xml`
5. 點擊 "Submit"

### Bing Webmaster Tools

1. 訪問：https://www.bing.com/webmasters
2. 選擇您的網站
3. Sitemaps → Submit a sitemap
4. 輸入：`https://studio.ai-tracks.com/sitemap.xml`
5. 點擊 "Submit"

---

**最後更新：** 2025-12-04  
**狀態：** 待部署










