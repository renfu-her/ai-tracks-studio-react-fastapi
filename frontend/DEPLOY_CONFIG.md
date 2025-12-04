# 前端部署配置 Frontend Deployment Configuration

## 🎯 生產環境配置

### 步驟 1：創建生產環境變數文件

在 `frontend/` 目錄創建 `.env.production`：

```env
# Production Environment Variables
VITE_API_BASE_URL=https://studio.ai-tracks.com
```

### 步驟 2：構建生產版本

```bash
cd frontend

# 安裝依賴（首次）
npm install

# 構建
npm run build
```

### 步驟 3：檢查構建結果

```bash
cd dist

# 應該看到：
# - index.html
# - assets/
#   - index-[hash].js
#   - index-[hash].css
#   - 其他靜態資源
```

## 📋 環境變數說明

### `VITE_API_BASE_URL`

指定前端連接的後端 API 地址。

**開發環境** (`.env.development` 或不設置)：
```env
VITE_API_BASE_URL=http://localhost:8000
```

**生產環境** (`.env.production`)：
```env
VITE_API_BASE_URL=https://studio.ai-tracks.com
```

**或者如果後端在子路徑：**
```env
VITE_API_BASE_URL=https://studio.ai-tracks.com/api-backend
```

## 🚀 快速部署（Windows 開發機器）

### 方法 1：使用 PowerShell 腳本

創建 `deploy.ps1`：

```powershell
# Build and prepare for deployment
Write-Host "Building frontend..." -ForegroundColor Green

# Set production env
$env:VITE_API_BASE_URL = "https://studio.ai-tracks.com"

# Build
npm run build

Write-Host "Build complete! Files are in dist/" -ForegroundColor Green
Write-Host "Upload dist/* to server's public directory" -ForegroundColor Yellow
```

運行：
```powershell
.\deploy.ps1
```

### 方法 2：使用 npm scripts

在 `package.json` 添加：

```json
{
  "scripts": {
    "build:prod": "vite build --mode production"
  }
}
```

運行：
```bash
npm run build:prod
```

## 📤 上傳到服務器

### 選項 A：使用 Git

```bash
# 在 Windows 開發機器
git add frontend/dist
git commit -m "Add production build"
git push origin main

# 在 Linux 服務器
cd /home/ai-tracks-studio/htdocs/studio.ai-tracks.com
git pull origin main
cp -r frontend/dist/* public/
```

### 選項 B：使用 SCP (PowerShell)

```powershell
scp -r .\dist\* ai-tracks-studio@your-server:/home/ai-tracks-studio/htdocs/studio.ai-tracks.com/public/
```

### 選項 C：使用 WinSCP / FileZilla

1. 連接到服務器
2. 上傳 `dist/` 目錄的所有內容
3. 目標路徑：`/home/ai-tracks-studio/htdocs/studio.ai-tracks.com/public/`

## 🔍 驗證部署

### 在服務器上檢查

```bash
# 檢查文件
ls -la /home/ai-tracks-studio/htdocs/studio.ai-tracks.com/public/

# 應該看到：
# - index.html
# - assets/ (目錄)
# - vite.svg (可能)
```

### 在瀏覽器檢查

1. 訪問：https://studio.ai-tracks.com
2. 打開開發者工具（F12）
3. 檢查 Network tab：
   - 應該看到成功載入 `index.html`
   - 應該看到成功載入 `assets/*.js`
   - 應該看到成功載入 `assets/*.css`
   - 應該看到 API 請求到 `/api/projects` 等

4. Console tab 應該沒有錯誤

## ⚙️ Vite 配置（可選）

如果需要自定義構建，編輯 `vite.config.ts`：

```typescript
import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

export default defineConfig({
  plugins: [react()],
  
  // Base URL (if deployed in subdirectory)
  base: '/',
  
  // Build options
  build: {
    outDir: 'dist',
    assetsDir: 'assets',
    sourcemap: false, // Set to true for debugging
    minify: 'terser',
    
    // Rollup options
    rollupOptions: {
      output: {
        manualChunks: {
          vendor: ['react', 'react-dom', 'react-router-dom'],
        }
      }
    }
  },
  
  // Server proxy for development
  server: {
    proxy: {
      '/api': {
        target: 'http://localhost:8000',
        changeOrigin: true,
      }
    }
  }
})
```

## 🐛 常見問題

### 問題 1：構建後 API 請求失敗

**症狀：** 頁面載入但沒有數據

**原因：** `.env.production` 沒有設置或 API URL 錯誤

**解決：**
```bash
# 檢查 .env.production
cat .env.production

# 應該是：
# VITE_API_BASE_URL=https://studio.ai-tracks.com

# 重新構建
npm run build
```

### 問題 2：白屏或 404

**症狀：** 瀏覽器顯示白屏或 404

**原因：** 
- 文件沒有正確上傳
- Nginx 配置錯誤

**解決：**
```bash
# 檢查文件
ls -la /home/ai-tracks-studio/htdocs/studio.ai-tracks.com/public/index.html

# 檢查 Nginx 配置
sudo nginx -t

# 檢查 Nginx root 路徑
cat /etc/nginx/sites-available/studio.ai-tracks.com | grep root
```

### 問題 3：舊版本緩存

**症狀：** 更新後仍然看到舊版本

**解決：**

1. **清除瀏覽器緩存：** `Ctrl + Shift + Delete`
2. **強制重新加載：** `Ctrl + F5`
3. **添加 cache busting：** Vite 自動處理（文件名有 hash）

### 問題 4：資源載入慢

**症狀：** 頁面載入緩慢

**解決：**

1. **啟用 Gzip 壓縮** - 已在 Nginx 配置中
2. **使用 CDN** - 將靜態資源上傳到 CDN
3. **優化圖片** - 使用 WebP 格式
4. **Code splitting** - 已在 Vite 配置中

## 📊 部署檢查清單

### 構建前
- [ ] `.env.production` 文件存在且正確
- [ ] `npm install` 已執行
- [ ] 所有依賴已安裝

### 構建
- [ ] `npm run build` 成功
- [ ] `dist/` 目錄已生成
- [ ] `dist/index.html` 存在
- [ ] `dist/assets/` 目錄存在

### 上傳
- [ ] 所有 `dist/` 內容已上傳
- [ ] 上傳到正確的目錄
- [ ] 文件權限正確（755）

### 驗證
- [ ] 可以訪問首頁
- [ ] 沒有 404 錯誤
- [ ] API 請求成功
- [ ] 圖片正常顯示
- [ ] 路由正常工作

## 🔄 持續部署（CI/CD）

### 使用 GitHub Actions

創建 `.github/workflows/deploy.yml`：

```yaml
name: Deploy Frontend

on:
  push:
    branches: [ main ]
    paths:
      - 'frontend/**'

jobs:
  deploy:
    runs-on: ubuntu-latest
    
    steps:
    - uses: actions/checkout@v3
    
    - name: Setup Node.js
      uses: actions/setup-node@v3
      with:
        node-version: '18'
    
    - name: Install dependencies
      working-directory: frontend
      run: npm install
    
    - name: Build
      working-directory: frontend
      env:
        VITE_API_BASE_URL: https://studio.ai-tracks.com
      run: npm run build
    
    - name: Deploy to server
      uses: easingthemes/ssh-deploy@main
      env:
        SSH_PRIVATE_KEY: ${{ secrets.SSH_PRIVATE_KEY }}
        REMOTE_HOST: ${{ secrets.REMOTE_HOST }}
        REMOTE_USER: ${{ secrets.REMOTE_USER }}
        SOURCE: "frontend/dist/"
        TARGET: "/home/ai-tracks-studio/htdocs/studio.ai-tracks.com/public/"
```

## 📝 總結

**快速部署流程：**

1. 創建 `.env.production`
2. 運行 `npm run build`
3. 上傳 `dist/*` 到服務器 `public/` 目錄
4. 訪問 https://studio.ai-tracks.com 驗證

**完成！** 🎉

