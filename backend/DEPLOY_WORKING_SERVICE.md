# 部署正常工作的 Service Deploy Working Service

## 🎯 問題分析 Problem Analysis

### 手動運行（✅ 正常）
```bash
uv run uvicorn app.main:app --host 0.0.0.0 --port 9001
# ✓ 數據庫連接正常
# ✓ Admin 用戶初始化正常
# ✓ 服務啟動正常
```

### Systemd Service（❌ 不正常）
```bash
uv run gunicorn app.main:app --workers 8 ...
# ✗ 裡面不正常
```

### 差異 Differences

| 項目 | 手動命令 | Service 文件 |
|------|---------|-------------|
| 執行工具 | **uvicorn** | gunicorn + uvicorn workers |
| 複雜度 | 簡單 | 複雜 |
| 結果 | ✅ 正常 | ❌ 不正常 |

## 🚀 解決方案：使用與手動測試相同的命令

新的 service 文件：`studio-uvicorn-working.service`

### 關鍵改進

```ini
# 舊版（不正常）
ExecStart=/home/ai-tracks-studio/.local/bin/uv run gunicorn app.main:app \
    --workers 8 \
    --worker-class uvicorn.workers.UvicornWorker \
    --bind 127.0.0.1:9001

# 新版（應該正常）- 與手動命令一致
ExecStart=/home/ai-tracks-studio/.local/bin/uv run uvicorn app.main:app \
    --host 127.0.0.1 \
    --port 9001 \
    --workers 8
```

## 📋 部署步驟 Deployment Steps

### 1️⃣ 停止當前服務

```bash
sudo systemctl stop studio-uvicorn
```

### 2️⃣ 備份舊的 service 文件

```bash
sudo cp /etc/systemd/system/studio-uvicorn.service \
    /etc/systemd/system/studio-uvicorn.service.backup
```

### 3️⃣ 複製新的 service 文件

```bash
sudo cp /home/ai-tracks-studio/htdocs/studio.ai-tracks.com/backend/studio-uvicorn-working.service \
    /etc/systemd/system/studio-uvicorn.service
```

### 4️⃣ 重新加載 systemd

```bash
sudo systemctl daemon-reload
```

### 5️⃣ 啟動服務

```bash
sudo systemctl start studio-uvicorn
```

### 6️⃣ 檢查狀態

```bash
sudo systemctl status studio-uvicorn
```

應該看到：
```
● studio-uvicorn.service - AI-Tracks Studio Backend API (Uvicorn - Working Version)
   Loaded: loaded (/etc/systemd/system/studio-uvicorn.service; enabled)
   Active: active (running) since ...
```

### 7️⃣ 查看日誌

```bash
sudo journalctl -u studio-uvicorn -f
```

應該看到與手動運行相同的日誌：
```
INFO:     Started server process [...]
INFO:     Waiting for application startup.
Creating database tables...
Database tables created successfully!
Checking database schema...
Database schema check completed!
Admin user initialized!
INFO:     Application startup complete.
INFO:     Uvicorn running on http://127.0.0.1:9001
```

### 8️⃣ 測試 API

```bash
curl http://127.0.0.1:9001/docs
# 應該返回 HTML（Swagger UI）
```

## ✅ 驗證檢查 Verification Checklist

- [ ] Service 狀態為 `active (running)`
- [ ] 日誌顯示 "Database tables created successfully!"
- [ ] 日誌顯示 "Admin user initialized!"
- [ ] 日誌顯示 "Application startup complete"
- [ ] 可以訪問 http://127.0.0.1:9001/docs
- [ ] 沒有錯誤訊息

## 🔍 故障排除 Troubleshooting

### 如果服務還是不正常

#### 檢查 1：確認使用了新的 service 文件

```bash
cat /etc/systemd/system/studio-uvicorn.service | grep ExecStart
```

應該看到：
```
ExecStart=/home/ai-tracks-studio/.local/bin/uv run uvicorn app.main:app \
```

#### 檢查 2：查看詳細日誌

```bash
sudo journalctl -u studio-uvicorn -n 100 --no-pager
```

#### 檢查 3：手動測試 service 命令

```bash
cd /home/ai-tracks-studio/htdocs/studio.ai-tracks.com/backend
/home/ai-tracks-studio/.local/bin/uv run uvicorn app.main:app \
    --host 127.0.0.1 \
    --port 9001 \
    --workers 8 \
    --log-level info
```

#### 檢查 4：確認 port 沒被佔用

```bash
sudo lsof -ti:9001
# 如果有輸出，說明 port 被佔用
sudo lsof -ti:9001 | xargs kill -9
```

## 📊 Uvicorn vs Gunicorn 比較

### Uvicorn（新 service）

**優點：**
- ✅ 簡單直接
- ✅ 與手動測試一致
- ✅ 已驗證可正常工作
- ✅ 支援多 workers
- ✅ 更容易調試

**缺點：**
- ⚠️ 進程管理相對簡單

### Gunicorn + Uvicorn Workers（舊 service）

**優點：**
- ✅ 更好的進程管理
- ✅ 優雅的重載
- ✅ Worker 健康檢查

**缺點：**
- ⚠️ 配置複雜
- ⚠️ 多一層抽象
- ⚠️ 目前有問題

**結論：先讓服務正常運行（用 Uvicorn），穩定後再考慮 Gunicorn。**

## 🔄 如果需要回滾

```bash
# 停止服務
sudo systemctl stop studio-uvicorn

# 恢復舊文件
sudo cp /etc/systemd/system/studio-uvicorn.service.backup \
    /etc/systemd/system/studio-uvicorn.service

# 重新加載
sudo systemctl daemon-reload

# 啟動
sudo systemctl start studio-uvicorn
```

## 📝 配置說明 Configuration Details

### Workers 數量

```ini
--workers 8
```

- 當前設置：8 個 workers
- 建議：`(CPU 核心數 × 2) + 1`
- 可根據實際負載調整

### Host 設置

```ini
--host 127.0.0.1
```

- 只監聽本地（透過 Nginx 反向代理）
- 更安全，不直接暴露到外網

### Log Level

```ini
--log-level info
```

- `debug` - 最詳細（開發用）
- `info` - 標準資訊（推薦）
- `warning` - 只顯示警告
- `error` - 只顯示錯誤

## 🎯 後續優化（可選）

當服務穩定運行後，可以考慮：

### 1. 添加日誌檔案

```ini
ExecStart=/home/ai-tracks-studio/.local/bin/uv run uvicorn app.main:app \
    --host 127.0.0.1 \
    --port 9001 \
    --workers 8 \
    --log-level info \
    --access-log \
    --log-config /path/to/logging.json
```

### 2. 使用環境變數檔案

```ini
EnvironmentFile=/home/ai-tracks-studio/htdocs/studio.ai-tracks.com/backend/.env
```

### 3. 健康檢查

添加監控腳本定期檢查服務健康狀態。

### 4. 自動重啟策略

```ini
Restart=always
RestartSec=3
StartLimitInterval=60
StartLimitBurst=3
```

## 💡 一鍵部署腳本

```bash
#!/bin/bash
# Quick deploy script

sudo systemctl stop studio-uvicorn
sudo cp /home/ai-tracks-studio/htdocs/studio.ai-tracks.com/backend/studio-uvicorn-working.service \
    /etc/systemd/system/studio-uvicorn.service
sudo systemctl daemon-reload
sudo systemctl start studio-uvicorn
sudo systemctl status studio-uvicorn
```

保存為 `deploy_service.sh` 並執行：
```bash
chmod +x deploy_service.sh
./deploy_service.sh
```

## 總結 Summary

**問題：** Gunicorn + Uvicorn workers 配置不正常

**解決：** 直接使用 Uvicorn（與手動測試一致）

**結果：** 應該會正常工作 ✅

立即部署新的 service 文件，應該就能解決問題！🚀

