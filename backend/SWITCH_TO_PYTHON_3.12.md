# 切換到 Python 3.12 指南 Switch to Python 3.12 Guide

## 為什麼要切換？Why Switch?

### Python 3.14 vs Python 3.12

| 特性 | Python 3.14 | Python 3.12 |
|------|-------------|-------------|
| **穩定性** | ⚠️ 較新，可能有未知問題 | ✅ 非常穩定，廣泛測試 |
| **套件支援** | ⚠️ 部分套件可能未完全測試 | ✅ 所有套件完全支援 |
| **社群支援** | ⚠️ 較少經驗分享 | ✅ 豐富的社群資源 |
| **生產環境** | ❌ 不建議 | ✅ **強烈推薦** |
| **效能** | ✅ 略優 | ✅ 優秀 |

**結論：生產環境強烈建議使用 Python 3.12！**

## 🚀 自動化腳本（推薦）

我已經創建了一個全自動的切換腳本！

### 快速執行

```bash
cd /home/ai-tracks-studio/htdocs/studio.ai-tracks.com/backend
chmod +x switch_to_python_3.12.sh
bash switch_to_python_3.12.sh
```

### 腳本會自動執行

1. ✅ 檢查 Python 3.12 是否可用
2. ✅ 備份現有 `.venv` 目錄
3. ✅ 創建新的 Python 3.12 虛擬環境
4. ✅ 安裝所有依賴套件
5. ✅ 驗證所有套件是否正確安裝
6. ✅ 測試 `app` 模組導入
7. ✅ 快速測試伺服器啟動
8. ✅ 提供下一步操作指引

### 預計時間

- 小型項目：1-2 分鐘
- 中型項目：3-5 分鐘
- 大型項目：5-10 分鐘

## 📋 手動切換步驟（進階）

如果你想手動執行或理解每個步驟：

### 前置準備

#### 1. 確認 Python 3.12 已安裝

```bash
# 檢查是否已安裝
python3.12 --version

# 如果沒有，安裝 Python 3.12（Ubuntu/Debian）
sudo apt update
sudo apt install python3.12 python3.12-venv python3.12-dev

# CentOS/RHEL
sudo dnf install python3.12 python3.12-devel
```

#### 2. 停止當前服務

```bash
sudo systemctl stop studio-uvicorn
```

### 切換步驟

#### Step 1: 進入專案目錄

```bash
cd /home/ai-tracks-studio/htdocs/studio.ai-tracks.com/backend
```

#### Step 2: 備份現有虛擬環境

```bash
# 創建備份（帶時間戳）
mv .venv .venv.backup.$(date +%Y%m%d_%H%M%S)

# 或簡單備份
mv .venv .venv.old
```

#### Step 3: 創建新的 Python 3.12 虛擬環境

**選項 A：使用 uv（推薦，如果已安裝）**

```bash
uv venv --python 3.12
```

**選項 B：使用標準 venv**

```bash
python3.12 -m venv .venv
```

#### Step 4: 驗證新環境

```bash
# 檢查 Python 版本
.venv/bin/python --version
# 應該顯示：Python 3.12.x
```

#### Step 5: 安裝依賴

**選項 A：使用 uv sync（推薦）**

```bash
uv sync
```

**選項 B：使用 pip + requirements.txt**

```bash
.venv/bin/pip install --upgrade pip
.venv/bin/pip install -r requirements.txt
```

**選項 C：使用 pip + pyproject.toml**

```bash
.venv/bin/pip install --upgrade pip
.venv/bin/pip install -e .
```

#### Step 6: 驗證安裝

```bash
# 測試套件導入
.venv/bin/python << EOF
from app.config import settings
from app.main import app
print("✓ All imports successful!")
print(f"Database: {settings.DB_NAME}")
EOF
```

#### Step 7: 測試伺服器啟動

```bash
# 快速測試（按 Ctrl+C 停止）
.venv/bin/uvicorn app.main:app --host 127.0.0.1 --port 19999
```

在瀏覽器訪問：http://127.0.0.1:19999/docs

如果看到 Swagger UI，表示成功！

#### Step 8: 重啟生產服務

```bash
sudo systemctl start studio-uvicorn
sudo systemctl status studio-uvicorn
```

#### Step 9: 驗證生產服務

```bash
# 查看日誌
sudo journalctl -u studio-uvicorn -f

# 測試 API
curl http://127.0.0.1:9001/docs
```

#### Step 10: 清理備份（確認一切正常後）

```bash
# 等待幾天確認沒問題後
rm -rf /home/ai-tracks-studio/htdocs/studio.ai-tracks.com/backend/.venv.backup.*
```

## ❗ 故障排除 Troubleshooting

### 問題 1：Python 3.12 not found

**錯誤：**
```
bash: python3.12: command not found
```

**解決方案：**
```bash
# Ubuntu/Debian
sudo apt update
sudo apt install python3.12 python3.12-venv python3.12-dev

# 或添加 deadsnakes PPA（如果官方源沒有）
sudo add-apt-repository ppa:deadsnakes/ppa
sudo apt update
sudo apt install python3.12 python3.12-venv python3.12-dev
```

### 問題 2：套件安裝失敗

**錯誤：**
```
ERROR: Could not find a version that satisfies the requirement...
```

**解決方案：**
```bash
# 1. 更新 pip
.venv/bin/pip install --upgrade pip setuptools wheel

# 2. 如果是 C 擴展套件，安裝開發工具
sudo apt install build-essential python3.12-dev

# 3. 重新安裝
.venv/bin/pip install -r requirements.txt
```

### 問題 3：MySQL 連接失敗

**錯誤：**
```
Cannot connect to MySQL server
```

**解決方案：**
```bash
# 1. 確認 MySQL 運行
sudo systemctl status mysql

# 2. 測試連接
mysql -h localhost -u studio -p studio

# 3. 檢查 .env 文件
cat .env | grep DB_
```

### 問題 4：Import 仍然失敗

**錯誤：**
```
ModuleNotFoundError: No module named 'app'
```

**解決方案：**
```bash
# 1. 確認在正確的目錄
pwd
# 應該是：/home/ai-tracks-studio/htdocs/studio.ai-tracks.com/backend

# 2. 確認 app 目錄存在
ls -la app/

# 3. 手動測試
cd /home/ai-tracks-studio/htdocs/studio.ai-tracks.com/backend
.venv/bin/python -c "from app.config import settings; print('OK')"

# 4. 如果還是失敗，檢查 PYTHONPATH
export PYTHONPATH=/home/ai-tracks-studio/htdocs/studio.ai-tracks.com/backend
.venv/bin/python -c "from app.config import settings; print('OK')"
```

### 問題 5：權限錯誤

**錯誤：**
```
Permission denied
```

**解決方案：**
```bash
# 修正所有權
sudo chown -R ai-tracks-studio:ai-tracks-studio \
    /home/ai-tracks-studio/htdocs/studio.ai-tracks.com/backend

# 給腳本執行權限
chmod +x switch_to_python_3.12.sh
```

## ✅ 驗證檢查清單 Verification Checklist

切換完成後，檢查以下項目：

- [ ] Python 版本正確：`.venv/bin/python --version` 顯示 3.12.x
- [ ] 所有套件已安裝：`.venv/bin/pip list`
- [ ] 可以導入 app：`.venv/bin/python -c "from app.config import settings"`
- [ ] 伺服器可以啟動：手動測試 uvicorn
- [ ] systemd 服務運行：`sudo systemctl status studio-uvicorn`
- [ ] API 可訪問：`curl http://127.0.0.1:9001/docs`
- [ ] 日誌無錯誤：`sudo journalctl -u studio-uvicorn -n 50`
- [ ] 資料庫連接正常：測試 API 端點

## 🔄 回滾步驟 Rollback Steps

如果切換後有問題，快速回滾：

```bash
# 1. 停止服務
sudo systemctl stop studio-uvicorn

# 2. 刪除新環境
cd /home/ai-tracks-studio/htdocs/studio.ai-tracks.com/backend
rm -rf .venv

# 3. 恢復備份
mv .venv.backup.YYYYMMDD_HHMMSS .venv
# 或
mv .venv.old .venv

# 4. 重啟服務
sudo systemctl start studio-uvicorn
sudo systemctl status studio-uvicorn
```

## 📊 效能比較 Performance Comparison

切換前後的預期差異：

| 指標 | Python 3.14 | Python 3.12 | 差異 |
|------|-------------|-------------|------|
| 啟動時間 | ~2-3秒 | ~2-3秒 | 相似 |
| 記憶體使用 | ~50-70MB | ~50-70MB | 相似 |
| 請求處理速度 | 快 | 快 | 略慢 5-10%（可忽略）|
| **穩定性** | ⚠️ | ✅✅✅ | **大幅提升** |
| **套件相容性** | ⚠️ | ✅✅✅ | **大幅提升** |

**結論：效能差異可忽略，但穩定性和相容性大幅提升！**

## 🎯 最佳實踐 Best Practices

### 1. 使用 Python 版本管理

```bash
# 使用 pyenv（推薦）
curl https://pyenv.run | bash
pyenv install 3.12
pyenv local 3.12
```

### 2. 鎖定依賴版本

```bash
# 生成精確的依賴列表
.venv/bin/pip freeze > requirements.lock

# 或使用 uv
uv pip compile pyproject.toml -o requirements.lock
```

### 3. 定期更新套件

```bash
# 每月更新一次
.venv/bin/pip list --outdated
.venv/bin/pip install --upgrade package_name
```

### 4. 自動化測試

```bash
# 在切換前後運行測試
.venv/bin/pytest tests/
```

## 📚 相關資源

- Python 3.12 Release Notes: https://docs.python.org/3.12/whatsnew/3.12.html
- Python Version Support Policy: https://devguide.python.org/versions/
- FastAPI Deployment: https://fastapi.tiangolo.com/deployment/
- UV Documentation: https://github.com/astral-sh/uv

## 💡 常見問題 FAQ

### Q1: 需要多久才能完成切換？
**A:** 通常 2-5 分鐘，包含下載和安裝所有套件。

### Q2: 會影響現有資料嗎？
**A:** 不會。只是更換 Python 版本，資料庫和文件都不受影響。

### Q3: 需要停機嗎？
**A:** 是的，需要短暫停機（2-5 分鐘）來切換環境。

### Q4: 如果失敗怎麼辦？
**A:** 可以快速回滾到備份的舊環境，參考「回滾步驟」。

### Q5: Python 3.12 會支援到什麼時候？
**A:** 預計支援到 2028 年 10 月，還有 3+ 年的官方維護期。

## ✨ 總結

切換到 Python 3.12 的**優點**：
- ✅ 更穩定可靠
- ✅ 所有套件完全支援
- ✅ 豐富的社群資源
- ✅ 適合生產環境
- ✅ 長期支援保證

**建議**：立即執行切換腳本，5 分鐘內完成！

```bash
cd /home/ai-tracks-studio/htdocs/studio.ai-tracks.com/backend
chmod +x switch_to_python_3.12.sh
bash switch_to_python_3.12.sh
```

