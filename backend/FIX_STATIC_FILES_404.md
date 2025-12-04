# 修復靜態文件 404 錯誤 Fix Static Files 404 Error

## 🔍 錯誤診斷

### 瀏覽器控制台錯誤

```
Failed to load resource: the server responded with a status of 404 ()
- template-loader.js:1
- admin.js:1

Uncaught ReferenceError: checkAuth is not defined
```

### 問題分析

1. ❌ 瀏覽器無法加載 `/static/js/template-loader.js`
2. ❌ 瀏覽器無法加載 `/static/js/admin.js`  
3. ❌ 因為 JS 文件未加載，導致 `checkAuth` 函數未定義

## 🎯 根本原因

**靜態文件沒有正確部署到生產環境！**

生產服務器的 `backend/app/static/` 目錄可能：
- 文件缺失
- 權限錯誤
- 路徑不正確

## ✅ 解決方案

### 步驟 1：檢查生產環境文件是否存在

```bash
# SSH 到生產服務器
cd /home/ai-tracks-studio/htdocs/studio.ai-tracks.com/backend

# 檢查靜態文件目錄
ls -la app/static/js/

# 應該看到：
# - admin.js
# - template-loader.js
# - common-ui.js
```

### 步驟 2：如果文件缺失，從 Git 拉取

```bash
cd /home/ai-tracks-studio/htdocs/studio.ai-tracks.com

# 拉取最新代碼
git pull origin main

# 檢查文件是否存在
ls -la backend/app/static/js/
```

### 步驟 3：確認文件權限

```bash
# 修正權限
sudo chown -R ai-tracks-studio:ai-tracks-studio \
    /home/ai-tracks-studio/htdocs/studio.ai-tracks.com/backend/app/static

# 確保可讀
chmod -R 755 /home/ai-tracks-studio/htdocs/studio.ai-tracks.com/backend/app/static
```

### 步驟 4：驗證靜態文件路徑

```bash
cd /home/ai-tracks-studio/htdocs/studio.ai-tracks.com/backend

# 檢查 static 目錄結構
tree app/static/js/
# 或
find app/static/js/ -type f
```

應該顯示：
```
app/static/js/
├── admin.js
├── common-ui.js
└── template-loader.js
```

### 步驟 5：測試靜態文件訪問

```bash
# 測試 API 是否運行
curl http://127.0.0.1:9001/

# 測試靜態文件是否可訪問
curl http://127.0.0.1:9001/static/js/admin.js
# 應該返回 JavaScript 代碼

curl http://127.0.0.1:9001/static/js/template-loader.js
# 應該返回 JavaScript 代碼
```

### 步驟 6：重啟服務

```bash
sudo systemctl restart studio-uvicorn
sudo systemctl status studio-uvicorn
```

### 步驟 7：清除瀏覽器緩存

在瀏覽器中：
1. 按 `Ctrl + Shift + Delete`（或 `Cmd + Shift + Delete`）
2. 選擇「清除緩存圖片和文件」
3. 點擊「清除數據」
4. 重新加載頁面（`Ctrl + F5` 強制重新加載）

## 🔧 如果文件確實不存在

### 選項 A：從開發環境複製

```bash
# 在你的本地開發機器上
cd d:\python\studio
git add backend/app/static/js/*.js
git commit -m "Add missing static JS files"
git push origin main

# 在生產服務器上
cd /home/ai-tracks-studio/htdocs/studio.ai-tracks.com
git pull origin main
sudo systemctl restart studio-uvicorn
```

### 選項 B：手動上傳

使用 SCP 或 SFTP 上傳文件：

```bash
# 在本地機器上
scp -r d:\python\studio\backend\app\static\js\* \
    ai-tracks-studio@your-server:/home/ai-tracks-studio/htdocs/studio.ai-tracks.com/backend/app/static/js/
```

## 🐛 深度診斷

### 檢查 FastAPI 日誌

```bash
# 查看服務日誌
sudo journalctl -u studio-uvicorn -n 100 --no-pager

# 查看是否有靜態文件相關錯誤
sudo journalctl -u studio-uvicorn | grep static
```

### 手動測試靜態文件掛載

在生產服務器上創建測試腳本：

```bash
cd /home/ai-tracks-studio/htdocs/studio.ai-tracks.com/backend

# 創建測試腳本
cat > test_static.py << 'EOF'
import sys
from pathlib import Path

# 檢查靜態文件路徑
static_dir = Path(__file__).parent / "app" / "static"
print(f"Static directory: {static_dir}")
print(f"Exists: {static_dir.exists()}")
print(f"Is directory: {static_dir.is_dir()}")

# 列出文件
js_dir = static_dir / "js"
print(f"\nJS directory: {js_dir}")
print(f"Exists: {js_dir.exists()}")

if js_dir.exists():
    print("\nFiles in js directory:")
    for file in js_dir.iterdir():
        print(f"  - {file.name} ({file.stat().st_size} bytes)")
EOF

# 運行測試
uv run python test_static.py
```

### 檢查 Nginx 配置（如果使用）

如果你使用 Nginx 作為反向代理：

```bash
# 檢查 Nginx 配置
sudo nginx -t

# 查看站點配置
cat /etc/nginx/sites-available/studio.ai-tracks.com

# 確保靜態文件路徑正確
```

Nginx 配置應該包含：

```nginx
location /static/ {
    proxy_pass http://127.0.0.1:9001/static/;
    # 或直接提供靜態文件（更快）
    # alias /home/ai-tracks-studio/htdocs/studio.ai-tracks.com/backend/app/static/;
}
```

## 📋 快速修復清單

- [ ] 1. SSH 到生產服務器
- [ ] 2. 檢查文件是否存在：`ls -la backend/app/static/js/`
- [ ] 3. 如果缺失，從 Git 拉取：`git pull`
- [ ] 4. 修正權限：`chmod -R 755 backend/app/static`
- [ ] 5. 測試文件訪問：`curl http://127.0.0.1:9001/static/js/admin.js`
- [ ] 6. 重啟服務：`sudo systemctl restart studio-uvicorn`
- [ ] 7. 清除瀏覽器緩存並重新加載

## 🎯 預期結果

修復後，瀏覽器控制台應該：
- ✅ 沒有 404 錯誤
- ✅ 沒有 "checkAuth is not defined" 錯誤
- ✅ 後台管理頁面正常運行

## 💡 預防措施

### 1. 添加靜態文件到 Git

確保 `.gitignore` 不會排除這些文件：

```bash
# 檢查 .gitignore
cat backend/.gitignore

# 確保沒有排除 static/js/
```

### 2. 自動化部署腳本

創建 `deploy.sh`：

```bash
#!/bin/bash
set -e

echo "Deploying AI-Tracks Studio Backend..."

# Pull latest code
git pull origin main

# Sync dependencies
cd backend
uv sync

# Fix permissions
chmod -R 755 app/static

# Restart service
sudo systemctl restart studio-uvicorn

# Check status
sudo systemctl status studio-uvicorn

echo "Deployment complete!"
```

### 3. 添加健康檢查

在 `backend/app/main.py` 添加靜態文件檢查：

```python
@app.get("/health/static")
def check_static_files():
    """Check if static files are accessible."""
    static_dir = Path(__file__).parent / "static"
    js_dir = static_dir / "js"
    
    files = ["admin.js", "template-loader.js", "common-ui.js"]
    missing = []
    
    for file in files:
        if not (js_dir / file).exists():
            missing.append(file)
    
    if missing:
        return {
            "status": "error",
            "missing_files": missing
        }
    
    return {
        "status": "ok",
        "static_dir": str(static_dir),
        "files_checked": files
    }
```

測試：
```bash
curl http://127.0.0.1:9001/health/static
```

## 🔗 相關文檔

- FastAPI Static Files: https://fastapi.tiangolo.com/tutorial/static-files/
- File Permissions: `man chmod`
- Git Pull: `man git-pull`

## 總結

**最可能的原因：** 靜態文件沒有部署到生產環境

**快速修復：**
```bash
cd /home/ai-tracks-studio/htdocs/studio.ai-tracks.com
git pull
chmod -R 755 backend/app/static
sudo systemctl restart studio-uvicorn
```

然後清除瀏覽器緩存並重新加載！

