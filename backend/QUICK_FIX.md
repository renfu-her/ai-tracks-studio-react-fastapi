# Quick Fix for ModuleNotFoundError 快速修復指南

## 問題 Problem

```
ModuleNotFoundError: No module named 'app'
```

## 快速診斷 Quick Diagnosis

運行診斷腳本：

```bash
cd /home/ai-tracks-studio/htdocs/studio.ai-tracks.com/backend
chmod +x diagnose.sh
bash diagnose.sh
```

## 方案 A：使用新的 Direct Service 文件（最可靠）

這個版本使用 bash 來確保正確的工作目錄和 PYTHONPATH。

### 步驟 Steps

```bash
# 1. 停止當前服務
sudo systemctl stop studio-uvicorn

# 2. 複製新的 service 文件
sudo cp /home/ai-tracks-studio/htdocs/studio.ai-tracks.com/backend/studio-uvicorn-direct.service \
    /etc/systemd/system/studio-uvicorn.service

# 3. 確保日誌目錄存在
sudo mkdir -p /var/log/uvicorn
sudo chown ai-tracks-studio:ai-tracks-studio /var/log/uvicorn

# 4. 重新加載 systemd
sudo systemctl daemon-reload

# 5. 啟動服務
sudo systemctl start studio-uvicorn

# 6. 檢查狀態
sudo systemctl status studio-uvicorn

# 7. 查看日誌
sudo journalctl -u studio-uvicorn -f
```

### 測試 Test

```bash
# 等待 5 秒讓服務啟動
sleep 5

# 測試 API
curl http://127.0.0.1:9001/docs

# 應該看到 HTML 輸出（Swagger UI）
```

## 方案 B：手動測試命令（驗證環境）

在修改 systemd service 之前，先手動測試命令是否可行：

```bash
# 進入 backend 目錄
cd /home/ai-tracks-studio/htdocs/studio.ai-tracks.com/backend

# 測試 Python import
python3 -c "from app.config import settings; print('OK')"

# 或使用 venv 中的 Python
.venv/bin/python -c "from app.config import settings; print('OK')"

# 如果上面成功，測試啟動服務
.venv/bin/uvicorn app.main:app --host 127.0.0.1 --port 9001
```

### 如果 Python import 失敗

檢查是否在正確的目錄：

```bash
pwd
# 應該輸出：/home/ai-tracks-studio/htdocs/studio.ai-tracks.com/backend

ls -la app/
# 應該看到 __init__.py, main.py, config.py 等文件
```

檢查 PYTHONPATH：

```bash
export PYTHONPATH=/home/ai-tracks-studio/htdocs/studio.ai-tracks.com/backend
python3 -c "from app.config import settings; print('OK')"
```

## 方案 C：使用 Screen 或 Tmux（臨時解決方案）

如果 systemd 一直有問題，可以暫時使用 screen 或 tmux：

### 使用 Screen

```bash
# 安裝 screen（如果沒有）
sudo apt install screen

# 創建新 session
screen -S studio-backend

# 在 screen 中啟動服務
cd /home/ai-tracks-studio/htdocs/studio.ai-tracks.com/backend
.venv/bin/gunicorn app.main:app \
    --workers 8 \
    --worker-class uvicorn.workers.UvicornWorker \
    --bind 127.0.0.1:9001 \
    --timeout 120

# 按 Ctrl+A 然後按 D 來 detach
# 服務會在背景繼續運行

# 重新連接到 session
screen -r studio-backend
```

### 使用 Tmux

```bash
# 安裝 tmux（如果沒有）
sudo apt install tmux

# 創建新 session
tmux new -s studio-backend

# 在 tmux 中啟動服務
cd /home/ai-tracks-studio/htdocs/studio.ai-tracks.com/backend
.venv/bin/gunicorn app.main:app \
    --workers 8 \
    --worker-class uvicorn.workers.UvicornWorker \
    --bind 127.0.0.1:9001 \
    --timeout 120

# 按 Ctrl+B 然後按 D 來 detach

# 重新連接到 session
tmux attach -t studio-backend
```

## 常見問題 Common Issues

### 1. Port 已被佔用

```bash
# 查找佔用 port 的進程
sudo lsof -ti:9001

# 終止進程
sudo lsof -ti:9001 | xargs kill -9

# 或者使用不同的 port
# 修改 service 文件中的 --bind 127.0.0.1:9002
```

### 2. 權限問題

```bash
# 確認目錄權限
ls -la /home/ai-tracks-studio/htdocs/studio.ai-tracks.com/backend

# 修正權限
sudo chown -R ai-tracks-studio:ai-tracks-studio \
    /home/ai-tracks-studio/htdocs/studio.ai-tracks.com/backend
```

### 3. Virtual Environment 損壞

```bash
cd /home/ai-tracks-studio/htdocs/studio.ai-tracks.com/backend

# 刪除舊的 venv
rm -rf .venv

# 重新創建（如果使用 uv）
uv sync

# 或使用 pip
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### 4. Database 連接問題

```bash
# 測試 MySQL 連接
mysql -h localhost -u studio -p studio

# 檢查 .env 文件
cat /home/ai-tracks-studio/htdocs/studio.ai-tracks.com/backend/.env

# 確認 DB_HOST, DB_USER, DB_PASSWORD, DB_NAME 正確
```

## 檢查清單 Checklist

執行以下檢查：

- [ ] 在正確的目錄：`pwd` 顯示 `/home/ai-tracks-studio/htdocs/studio.ai-tracks.com/backend`
- [ ] app 目錄存在：`ls -la app/`
- [ ] Python 可以 import：`.venv/bin/python -c "from app.config import settings"`
- [ ] .env 文件存在：`ls -la .env`
- [ ] Virtual environment 存在：`ls -la .venv/`
- [ ] Service 文件已複製：`ls -la /etc/systemd/system/studio-uvicorn.service`
- [ ] Systemd 已重載：`sudo systemctl daemon-reload`
- [ ] 日誌目錄存在：`ls -la /var/log/uvicorn/`
- [ ] Port 未被佔用：`sudo lsof -ti:9001` (應該沒有輸出)
- [ ] 權限正確：目錄和文件屬於 `ai-tracks-studio` 用戶

## 成功標誌 Success Indicators

當一切正常時，你應該看到：

```bash
# systemctl status 顯示 active (running)
sudo systemctl status studio-uvicorn
● studio-uvicorn.service - AI-Tracks Studio Backend API
     Loaded: loaded (/etc/systemd/system/studio-uvicorn.service; enabled)
     Active: active (running) since ...

# API 可以訪問
curl http://127.0.0.1:9001/docs
# 應該返回 HTML

# 日誌沒有錯誤
sudo journalctl -u studio-uvicorn -n 20
# 應該看到 "Started AI-Tracks Studio Backend API" 或類似訊息
```

## 需要更多幫助？

如果以上方法都不行，請提供以下信息：

1. 診斷腳本輸出：`bash diagnose.sh`
2. Service 狀態：`sudo systemctl status studio-uvicorn -l`
3. 最近的日誌：`sudo journalctl -u studio-uvicorn -n 50 --no-pager`
4. 手動測試結果：
   ```bash
   cd /home/ai-tracks-studio/htdocs/studio.ai-tracks.com/backend
   .venv/bin/python -c "from app.config import settings; print('OK')"
   ```

