# Frontend Deployment Steps 前端部署步驟

## 問題 Problem

前端圖片路徑缺少 `/backend` 前綴：
- ❌ 錯誤：`https://studio.ai-tracks.com/static/uploads/xxx.webp`
- ✅ 正確：`https://studio.ai-tracks.com/backend/static/uploads/xxx.webp`

## 原因 Root Cause

前端代碼已經修正（`frontend/api/config.ts` 包含正確路徑），但生產環境需要重新構建和部署。

## 解決方案 Solution

### 1. 創建生產環境配置文件

在 `frontend/` 目錄下創建 `.env.production`：

```bash
cd frontend
```

創建 `.env.production` 文件：
```env
VITE_API_BASE_URL=https://studio.ai-tracks.com
```

### 2. 重新構建前端

```bash
cd frontend

# 安裝依賴（如果需要）
npm install

# 使用生產環境配置構建
npm run build
```

這會在 `frontend/dist/` 目錄生成優化後的文件。

### 3. 上傳到生產服務器

**使用 SFTP/SCP:**

```bash
# 從本地機器上傳
scp -r dist/* ai-tracks-studio@your-server:/home/ai-tracks-studio/htdocs/studio.ai-tracks.com/public/
```

**或者在服務器上拉取並構建:**

```bash
# SSH 到服務器
ssh ai-tracks-studio@your-server

# 進入專案目錄
cd /home/ai-tracks-studio/htdocs/studio.ai-tracks.com

# 拉取最新代碼
git pull origin main

# 進入前端目錄
cd frontend

# 創建 .env.production
echo "VITE_API_BASE_URL=https://studio.ai-tracks.com" > .env.production

# 安裝依賴
npm install

# 構建
npm run build

# 複製到 public 目錄
cp -r dist/* ../public/
```

### 4. 驗證部署

訪問網站並檢查圖片 URL：

```bash
# 打開瀏覽器開發者工具 (F12)
# 檢查 Network 標籤
# 確認圖片請求 URL 包含 /backend/static/uploads/
```

**預期結果：**
```
✅ https://studio.ai-tracks.com/backend/static/uploads/20251204-xxx.webp
```

## 檢查清單 Checklist

- [ ] 創建 `.env.production` 文件（`VITE_API_BASE_URL=https://studio.ai-tracks.com`）
- [ ] 運行 `npm run build` 構建前端
- [ ] 上傳 `dist/*` 到服務器 `/public/` 目錄
- [ ] 清除瀏覽器緩存 (Ctrl+Shift+R 或 Cmd+Shift+R)
- [ ] 驗證圖片 URL 包含 `/backend/static/uploads/`
- [ ] 測試所有頁面的圖片顯示

## 技術細節 Technical Details

### getImageUrl 函數位置

File: `frontend/api/config.ts` (Lines 40-48)

```typescript
export const getImageUrl = (filename: string | null | undefined): string => {
  if (!filename) {
    return 'https://via.placeholder.com/800x600?text=No+Image';
  }
  
  // Build full URL: https://studio.ai-tracks.com/backend/static/uploads/filename.webp
  return `${API_CONFIG.BASE_URL}/backend/static/uploads/${filename}`;
};
```

### 環境變量工作原理

- **Development**: `VITE_API_BASE_URL` 默認為 `http://localhost:8000`
- **Production**: 從 `.env.production` 讀取 `VITE_API_BASE_URL=https://studio.ai-tracks.com`
- **構建時**: Vite 將環境變量內聯到最終的 JavaScript 代碼中

## 常見問題 Troubleshooting

### 1. 圖片仍然顯示錯誤路徑

**原因：** 瀏覽器緩存舊版本

**解決：**
```bash
# 強制刷新（清除緩存）
Chrome/Edge: Ctrl+Shift+R (Windows) or Cmd+Shift+R (Mac)
Firefox: Ctrl+F5 (Windows) or Cmd+Shift+R (Mac)
```

### 2. 構建失敗

**原因：** Node 模塊未安裝或版本不匹配

**解決：**
```bash
cd frontend
rm -rf node_modules package-lock.json
npm install
npm run build
```

### 3. 上傳後仍然顯示舊內容

**原因：** 未正確複製文件或權限問題

**解決：**
```bash
# 檢查文件是否存在
ls -la /home/ai-tracks-studio/htdocs/studio.ai-tracks.com/public/

# 修正權限
sudo chown -R ai-tracks-studio:ai-tracks-studio /home/ai-tracks-studio/htdocs/studio.ai-tracks.com/public/
chmod -R 755 /home/ai-tracks-studio/htdocs/studio.ai-tracks.com/public/
```

### 4. API_BASE_URL 未生效

**原因：** `.env.production` 文件位置錯誤或格式錯誤

**解決：**
```bash
# 確保文件在 frontend/ 根目錄
cd frontend
cat .env.production

# 內容應該是：
# VITE_API_BASE_URL=https://studio.ai-tracks.com
```

## 快速修復 Quick Fix

如果只是測試，可以直接修改構建後的文件（不推薦用於正式部署）：

```bash
# 在服務器上
cd /home/ai-tracks-studio/htdocs/studio.ai-tracks.com/public

# 搜索並替換（備份後再操作）
grep -r "static/uploads" assets/*.js
# 手動編輯 .js 文件，將 /static/uploads/ 改為 /backend/static/uploads/
```

**注意：** 這只是臨時方法，下次部署會被覆蓋。

---

**最後更新：** 2025-12-04  
**狀態：** Ready for Deployment











