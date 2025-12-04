# Systemd Service Setup Guide systemd 服務設置指南

## 問題診斷 Problem Diagnosis

### ModuleNotFoundError: No module named 'app'

**原因 Cause:**
- 直接使用 `.venv/bin/gunicorn` 可能無法正確設置 Python 路徑
- 使用 `uv` 管理的項目需要通過 `uv run` 來執行，以確保環境正確

**解決方案 Solution:**
使用 `uv run` 命令而不是直接調用 venv 中的可執行文件。

## 兩種 Service 文件 Two Service Files

我們提供了兩個版本：

### 1. `studio-uvicorn.service` - 使用 Gunicorn（推薦生產環境）
- ✅ 更好的進程管理
- ✅ 自動重啟故障的 worker
- ✅ 優雅的重載和關閉
- ✅ 適合高流量生產環境

### 2. `studio-uvicorn-simple.service` - 直接使用 Uvicorn（簡單）
- ✅ 配置簡單
- ✅ 更容易調試
- ✅ 適合中小型項目
- ✅ 啟動更快

## 安裝步驟 Installation Steps

### 步驟 1：選擇並複製 service 文件

**選項 A：使用 Gunicorn（推薦）**
```bash
sudo cp /home/ai-tracks-studio/htdocs/studio.ai-tracks.com/backend/studio-uvicorn.service \
    /etc/systemd/system/studio-uvicorn.service
```

**選項 B：使用簡單的 Uvicorn**
```bash
sudo cp /home/ai-tracks-studio/htdocs/studio.ai-tracks.com/backend/studio-uvicorn-simple.service \
    /etc/systemd/system/studio-uvicorn.service
```

### 步驟 2：創建日誌目錄（如果使用 Gunicorn）

```bash
sudo mkdir -p /var/log/uvicorn
sudo chown ai-tracks-studio:ai-tracks-studio /var/log/uvicorn
```

### 步驟 3：重新加載 systemd

```bash
sudo systemctl daemon-reload
```

### 步驟 4：啟用服務（開機自動啟動）

```bash
sudo systemctl enable studio-uvicorn
```

### 步驟 5：啟動服務

```bash
sudo systemctl start studio-uvicorn
```

### 步驟 6：檢查狀態

```bash
sudo systemctl status studio-uvicorn
```

## 常用命令 Common Commands

### 查看狀態 Check Status
```bash
sudo systemctl status studio-uvicorn
```

### 啟動服務 Start Service
```bash
sudo systemctl start studio-uvicorn
```

### 停止服務 Stop Service
```bash
sudo systemctl stop studio-uvicorn
```

### 重啟服務 Restart Service
```bash
sudo systemctl restart studio-uvicorn
```

### 查看日誌 View Logs
```bash
# 查看最新日誌 View recent logs
sudo journalctl -u studio-uvicorn -n 100

# 即時查看日誌 Follow logs in real-time
sudo journalctl -u studio-uvicorn -f

# 查看今天的日誌 View today's logs
sudo journalctl -u studio-uvicorn --since today

# 查看錯誤日誌 View error logs only
sudo journalctl -u studio-uvicorn -p err
```

### 禁用服務 Disable Service
```bash
sudo systemctl disable studio-uvicorn
```

## 故障排除 Troubleshooting

### 1. Service 無法啟動 Service won't start

**檢查日誌：**
```bash
sudo journalctl -u studio-uvicorn -n 50 --no-pager
```

**常見原因：**
- Port 已被佔用
- 資料庫連接失敗
- 環境變數設置錯誤
- 權限問題

### 2. ModuleNotFoundError 仍然出現

**檢查 WorkingDirectory：**
```bash
# 確認目錄存在
ls -la /home/ai-tracks-studio/htdocs/studio.ai-tracks.com/backend

# 確認 app 目錄存在
ls -la /home/ai-tracks-studio/htdocs/studio.ai-tracks.com/backend/app
```

**檢查 uv 命令：**
```bash
# 確認 uv 已安裝
which uv

# 如果沒有，安裝 uv
curl -LsSf https://astral.sh/uv/install.sh | sh
```

**手動測試命令：**
```bash
cd /home/ai-tracks-studio/htdocs/studio.ai-tracks.com/backend
uv run python -c "from app.config import settings; print('OK')"
```

### 3. Port 已被佔用

**查找佔用 port 的進程：**
```bash
sudo lsof -ti:9001
```

**終止進程：**
```bash
sudo lsof -ti:9001 | xargs kill -9
```

### 4. 權限問題

**確認用戶和群組：**
```bash
id ai-tracks-studio
```

**修正目錄權限：**
```bash
sudo chown -R ai-tracks-studio:ai-tracks-studio \
    /home/ai-tracks-studio/htdocs/studio.ai-tracks.com/backend
```

### 5. 環境變數問題

**測試環境變數：**
```bash
sudo -u ai-tracks-studio bash -c 'cd /home/ai-tracks-studio/htdocs/studio.ai-tracks.com/backend && cat .env'
```

## 配置調整 Configuration Tuning

### Worker 數量 Worker Count

根據 CPU 核心數調整：
```bash
# 查看 CPU 核心數
nproc

# 建議公式：(CPU 核心數 × 2) + 1
# 例如：4 核心 → 9 workers
# 例如：8 核心 → 17 workers
```

修改 service 文件中的 `--workers` 參數。

### 記憶體使用 Memory Usage

每個 worker 大約使用 50-100MB 記憶體。監控記憶體使用：
```bash
# 查看記憶體使用
free -h

# 查看服務記憶體使用
sudo systemctl status studio-uvicorn
```

### Timeout 設置

如果有長時間運行的請求，增加 timeout：
```bash
--timeout 300  # 5 分鐘
```

## 安全設置 Security Settings

### 限制服務權限

在 `[Service]` 區段添加：
```ini
# 禁止提升權限
NoNewPrivileges=true

# 使用私有 tmp 目錄
PrivateTmp=true

# 只讀根文件系統（可選，較嚴格）
# ReadOnlyPaths=/
# ReadWritePaths=/home/ai-tracks-studio/htdocs/studio.ai-tracks.com/backend

# 禁止訪問 /home（可選，較嚴格）
# ProtectHome=true
```

### 防火牆設置

確保只有 Nginx 可以訪問後端：
```bash
# 確認服務綁定到 127.0.0.1（localhost only）
# 在 service 文件中：-b 127.0.0.1:9001
```

## 更新部署 Updating Deployment

### 更新代碼後重啟

```bash
# 1. 拉取最新代碼
cd /home/ai-tracks-studio/htdocs/studio.ai-tracks.com
git pull

# 2. 更新依賴（如果需要）
cd backend
uv sync

# 3. 重啟服務
sudo systemctl restart studio-uvicorn

# 4. 檢查狀態
sudo systemctl status studio-uvicorn
```

### 無停機重載（使用 Gunicorn）

```bash
# 發送 HUP 信號重載 workers
sudo systemctl reload studio-uvicorn

# 或使用 kill 命令
sudo kill -HUP $(cat /run/studio-uvicorn.pid)
```

## 監控 Monitoring

### 實時監控日誌

```bash
# 終端 1：查看 systemd 日誌
sudo journalctl -u studio-uvicorn -f

# 終端 2：查看 access log（如果使用 Gunicorn）
tail -f /var/log/uvicorn/studio-access.log

# 終端 3：查看 error log（如果使用 Gunicorn）
tail -f /var/log/uvicorn/studio-error.log
```

### 性能監控

```bash
# CPU 和記憶體使用
top -p $(pgrep -f studio-uvicorn)

# 或使用 htop
htop -p $(pgrep -f studio-uvicorn | tr '\n' ',')
```

## 備份與恢復 Backup and Recovery

### 備份 service 文件

```bash
sudo cp /etc/systemd/system/studio-uvicorn.service \
    /home/ai-tracks-studio/studio-uvicorn.service.backup
```

### 恢復 service 文件

```bash
sudo cp /home/ai-tracks-studio/studio-uvicorn.service.backup \
    /etc/systemd/system/studio-uvicorn.service
sudo systemctl daemon-reload
sudo systemctl restart studio-uvicorn
```

## 測試清單 Testing Checklist

部署後測試：

- [ ] Service 啟動成功：`sudo systemctl status studio-uvicorn`
- [ ] 日誌無錯誤：`sudo journalctl -u studio-uvicorn -n 50`
- [ ] API 可訪問：`curl http://127.0.0.1:9001/docs`
- [ ] 資料庫連接正常：檢查 API 回應
- [ ] 開機自動啟動：`sudo systemctl is-enabled studio-uvicorn`
- [ ] 優雅關閉測試：`sudo systemctl stop studio-uvicorn`（無錯誤）
- [ ] 重啟測試：`sudo systemctl restart studio-uvicorn`（成功）

## 常見錯誤代碼 Common Error Codes

- **Exit code 1**: 一般錯誤（檢查日誌）
- **Exit code 2**: 配置錯誤
- **Exit code 3**: Worker 啟動失敗
- **Exit code 137**: 記憶體不足（OOM killed）
- **Exit code 143**: 正常關閉（SIGTERM）

## 額外資源 Additional Resources

- Systemd Documentation: https://www.freedesktop.org/software/systemd/man/
- Gunicorn Documentation: https://docs.gunicorn.org/
- Uvicorn Documentation: https://www.uvicorn.org/
- FastAPI Deployment: https://fastapi.tiangolo.com/deployment/

