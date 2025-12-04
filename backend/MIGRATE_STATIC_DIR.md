# 靜態目錄遷移指南 Static Directory Migration Guide

## 🎯 目標

將靜態文件目錄從 `backend/app/static/` 移動到 `backend/static/`，實現更清晰的目錄結構。

## 📁 目錄結構變更

### Before 之前
```
backend/
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── config.py
│   ├── models/
│   ├── routers/
│   └── static/              ← 靜態文件在這裡
│       ├── admin.html
│       ├── login.html
│       ├── js/
│       │   ├── admin.js
│       │   ├── common-ui.js
│       │   └── template-loader.js
│       ├── css/
│       │   ├── admin.css
│       │   └── admin-bootstrap.css
│       ├── admin/
│       │   ├── projects/
│       │   ├── news/
│       │   └── about/
│       └── uploads/
│           └── *.webp
├── pyproject.toml
└── .python-version
```

### After 之後
```
backend/
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── config.py
│   ├── models/
│   └── routers/
├── static/                  ← 移到這裡，與 app 同級
│   ├── admin.html
│   ├── login.html
│   ├── js/
│   │   ├── admin.js
│   │   ├── common-ui.js
│   │   └── template-loader.js
│   ├── css/
│   │   ├── admin.css
│   │   └── admin-bootstrap.css
│   ├── admin/
│   │   ├── projects/
│   │   ├── news/
│   │   └── about/
│   └── uploads/
│       └── *.webp
├── pyproject.toml
└── .python-version
```

## ✅ 優點

1. **清晰的分離**
   - 應用代碼（app/）和靜態資源（static/）分離
   - 更符合常見的 Python 項目結構

2. **更容易管理**
   - 靜態文件獨立，易於備份和遷移
   - 可以單獨設置權限

3. **更好的部署**
   - 可以單獨部署靜態文件到 CDN
   - Nginx 可以直接提供靜態文件（不經過 Python）

## 🔧 已修改的代碼

### 1. `backend/app/main.py`

```python
# Before
static_dir = Path(__file__).parent / "static"

# After
static_dir = Path(__file__).parent.parent / "static"
```

### 2. `backend/app/routers/admin/upload.py`

```python
# Before
UPLOAD_DIR = Path(__file__).parent.parent.parent / "static" / "uploads"

# After
UPLOAD_DIR = Path(__file__).parent.parent.parent.parent / "static" / "uploads"
```

## 🚀 遷移步驟

### 在開發環境（Windows）

```bash
# 1. 在本地創建新目錄並移動文件
cd d:\python\studio\backend
mkdir static
xcopy app\static static /E /I /H

# 2. 提交到 Git
git add backend/app/main.py
git add backend/app/routers/admin/upload.py
git add backend/static
git commit -m "Migrate static directory to backend/static"
git push origin main
```

### 在生產環境（Linux）

#### 方法 A：使用自動化腳本（推薦）

```bash
cd /home/ai-tracks-studio/htdocs/studio.ai-tracks.com/backend

# 1. 拉取最新代碼
git pull origin main

# 2. 運行遷移腳本
chmod +x migrate_static.sh
bash migrate_static.sh

# 3. 重啟服務
sudo systemctl restart studio-uvicorn

# 4. 驗證
curl http://127.0.0.1:9001/backend/static/js/admin.js
```

#### 方法 B：手動遷移

```bash
cd /home/ai-tracks-studio/htdocs/studio.ai-tracks.com/backend

# 1. 停止服務
sudo systemctl stop studio-uvicorn

# 2. 備份（安全起見）
cp -r app/static app/static.backup

# 3. 移動目錄
mv app/static ./static

# 4. 驗證結構
ls -la static/
# 應該看到：admin.html, login.html, js/, css/, uploads/, admin/

# 5. 重啟服務
sudo systemctl start studio-uvicorn

# 6. 測試
curl http://127.0.0.1:9001/backend
curl http://127.0.0.1:9001/backend/static/js/admin.js
```

## ✅ 驗證清單

遷移後檢查：

- [ ] 靜態目錄存在：`ls -la backend/static/`
- [ ] 關鍵文件存在：
  - [ ] `static/admin.html`
  - [ ] `static/login.html`
  - [ ] `static/js/admin.js`
  - [ ] `static/css/admin.css`
  - [ ] `static/uploads/` (如果有上傳文件)
- [ ] 後端服務啟動：`sudo systemctl status studio-uvicorn`
- [ ] API 可訪問：`curl http://127.0.0.1:9001/`
- [ ] 後台可訪問：`curl http://127.0.0.1:9001/backend`
- [ ] 靜態 JS 可訪問：`curl http://127.0.0.1:9001/backend/static/js/admin.js`
- [ ] 通過域名可訪問：`curl https://studio.ai-tracks.com/backend`
- [ ] 瀏覽器無 404 錯誤

## 🔧 故障排除

### 問題 1：後端啟動失敗

**症狀：**
```bash
sudo systemctl status studio-uvicorn
# 顯示 failed
```

**檢查：**
```bash
# 查看日誌
sudo journalctl -u studio-uvicorn -n 50

# 可能的錯誤：
# FileNotFoundError: static directory not found
```

**解決：**
```bash
# 確認目錄存在
ls -la /home/ai-tracks-studio/htdocs/studio.ai-tracks.com/backend/static

# 如果不存在，手動創建
mkdir -p /home/ai-tracks-studio/htdocs/studio.ai-tracks.com/backend/static
```

### 問題 2：靜態文件 404

**症狀：**
瀏覽器控制台顯示 `404 Not Found` for `/backend/static/js/admin.js`

**檢查：**
```bash
# 測試直接訪問
curl http://127.0.0.1:9001/backend/static/js/admin.js

# 檢查文件權限
ls -la backend/static/js/admin.js
```

**解決：**
```bash
# 修正權限
chmod -R 755 backend/static
chown -R ai-tracks-studio:ai-tracks-studio backend/static
```

### 問題 3：上傳功能失敗

**症狀：**
上傳圖片時出錯

**檢查：**
```bash
# 確認 uploads 目錄存在
ls -la backend/static/uploads/

# 檢查權限
ls -ld backend/static/uploads/
```

**解決：**
```bash
# 創建 uploads 目錄
mkdir -p backend/static/uploads

# 設置可寫權限
chmod 755 backend/static/uploads
chown ai-tracks-studio:ai-tracks-studio backend/static/uploads
```

## 🔄 回滾步驟

如果遷移後有問題，可以快速回滾：

```bash
cd /home/ai-tracks-studio/htdocs/studio.ai-tracks.com/backend

# 1. 停止服務
sudo systemctl stop studio-uvicorn

# 2. 恢復舊結構（如果有備份）
rm -rf app/static
cp -r app/static.backup app/static

# 3. 回滾代碼更改
git checkout HEAD~1 app/main.py
git checkout HEAD~1 app/routers/admin/upload.py

# 4. 重啟服務
sudo systemctl start studio-uvicorn
```

## 📊 遷移影響

### 不需要改變的

- ✅ Nginx 配置（仍然代理到 `/backend/static/`）
- ✅ 前端 API 調用（路徑保持 `/backend/static/uploads/...`）
- ✅ 數據庫（如果只存 filename）
- ✅ 用戶訪問方式

### 需要注意的

- ⚠️ 開發和生產環境都需要更新
- ⚠️ 如果有自動化部署腳本，需要更新
- ⚠️ 如果有備份腳本指向舊路徑，需要更新

## 🎉 完成後

遷移完成後，你的項目結構更清晰了：

```
backend/
├── app/           ← Python 應用代碼
└── static/        ← 靜態資源文件
```

符合標準的 Python Web 應用結構！

