# Python 3.14 相容性說明 Python 3.14 Compatibility Notes

## 關於 ModuleNotFoundError 的問題

### ❌ Python 3.14 不是導致 `ModuleNotFoundError: No module named 'app'` 的原因

**實際原因：**
- ✓ 工作目錄設置不正確
- ✓ PYTHONPATH 沒有包含 backend 目錄
- ✓ systemd service 執行時的路徑配置問題

**證據：**
如果你在命令行手動執行以下命令成功：
```bash
cd /home/ai-tracks-studio/htdocs/studio.ai-tracks.com/backend
.venv/bin/python -c "from app.config import settings; print('OK')"
```

這證明 Python 3.14 本身可以正確導入 `app` 模組，問題在於 systemd service 的環境設置。

## Python 3.14 可能的影響

### 1. 套件相容性 Package Compatibility

Python 3.14 是較新的版本，某些套件可能還沒有完全測試或優化：

#### 本項目使用的主要套件：

| 套件 | Python 3.14 支援狀況 | 備註 |
|------|---------------------|------|
| FastAPI | ✅ 應該支援 | 通常快速支援新版本 |
| Uvicorn | ✅ 應該支援 | 基於 asyncio，相容性好 |
| Gunicorn | ✅ 應該支援 | 穩定的 WSGI server |
| Pydantic | ✅ 支援 | v2.x 支援 Python 3.14 |
| SQLAlchemy | ✅ 支援 | v2.x 支援新版本 Python |
| PyMySQL | ✅ 支援 | 純 Python 實現，相容性好 |

### 2. 已知的 Python 3.14 變更

Python 3.14 的主要變更（可能影響你的項目）：

#### 標準庫改進
- ✅ 更好的錯誤訊息
- ✅ 效能改進
- ✅ 類型系統增強

#### 可能的不相容性
- ⚠️ 一些舊的警告可能變成錯誤
- ⚠️ 某些已棄用的功能可能被移除
- ⚠️ C 擴展模組可能需要重新編譯

### 3. 建議的 Python 版本

**生產環境建議：**

| Python 版本 | 建議等級 | 原因 |
|------------|---------|------|
| **3.12** | ⭐⭐⭐⭐⭐ | 最穩定，廣泛測試，所有套件完全支援 |
| **3.13** | ⭐⭐⭐⭐ | 新特性，大部分套件支援 |
| **3.14** | ⭐⭐⭐ | 最新，可能有套件相容性問題 |
| 3.11 | ⭐⭐⭐⭐ | 穩定，但較舊 |

**如果堅持使用 Python 3.14：**
- ✅ 定期更新所有依賴套件
- ✅ 密切關注錯誤訊息
- ✅ 準備好降級到 3.12 的備案

## 測試你的 Python 3.14 環境

### 快速測試腳本

我已經創建了詳細的測試腳本：

```bash
cd /home/ai-tracks-studio/htdocs/studio.ai-tracks.com/backend
chmod +x check_python_compatibility.sh
bash check_python_compatibility.sh
```

這個腳本會檢查：
1. ✓ Python 版本資訊
2. ✓ 模組導入是否正常
3. ✓ 所有依賴套件是否可用
4. ✓ Uvicorn/Gunicorn 是否能啟動
5. ✓ API 是否可以正常回應

### 手動測試步驟

#### 測試 1：基本導入測試
```bash
cd /home/ai-tracks-studio/htdocs/studio.ai-tracks.com/backend
.venv/bin/python << EOF
import sys
print(f"Python: {sys.version}")

from app.config import settings
print(f"✓ Config imported")
print(f"  DB: {settings.DB_NAME}")

from app.main import app
print(f"✓ FastAPI app imported")

print("\nAll imports successful!")
EOF
```

#### 測試 2：啟動測試
```bash
cd /home/ai-tracks-studio/htdocs/studio.ai-tracks.com/backend
.venv/bin/uvicorn app.main:app --host 127.0.0.1 --port 19999
```

按 Ctrl+C 停止，如果啟動成功就沒問題。

#### 測試 3：Gunicorn 測試
```bash
cd /home/ai-tracks-studio/htdocs/studio.ai-tracks.com/backend
.venv/bin/gunicorn app.main:app \
    --workers 2 \
    --worker-class uvicorn.workers.UvicornWorker \
    --bind 127.0.0.1:19999
```

## 如果遇到 Python 3.14 的問題

### 方案 A：更新所有套件到最新版本

```bash
cd /home/ai-tracks-studio/htdocs/studio.ai-tracks.com/backend

# 如果使用 uv
uv sync --upgrade

# 如果使用 pip
.venv/bin/pip install --upgrade fastapi uvicorn gunicorn pydantic sqlalchemy pymysql
```

### 方案 B：降級到 Python 3.12（推薦生產環境）

```bash
cd /home/ai-tracks-studio/htdocs/studio.ai-tracks.com/backend

# 1. 備份現有環境
mv .venv .venv.bak

# 2. 使用 uv 指定 Python 3.12
uv venv --python 3.12

# 3. 安裝依賴
uv sync

# 或使用 pip
python3.12 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

# 4. 測試
.venv/bin/python --version  # 應該顯示 3.12.x
.venv/bin/python -c "from app.config import settings; print('OK')"

# 5. 如果成功，刪除備份
rm -rf .venv.bak
```

### 方案 C：使用 Docker（隔離環境）

創建 `Dockerfile`：
```dockerfile
FROM python:3.12-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application
COPY . .

# Run
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

## 結論與建議

### 關於 `ModuleNotFoundError` 問題：

**Python 3.14 不是問題的根源。**

你的問題 100% 是因為 systemd service 的路徑配置。使用我提供的 `studio-uvicorn-direct.service` 文件可以解決。

### 關於 Python 3.14 使用建議：

✅ **可以繼續使用 Python 3.14**，但要：
1. 定期更新套件
2. 監控日誌是否有警告
3. 遇到問題時考慮降級

⭐ **推薦在生產環境使用 Python 3.12**：
- 更穩定
- 所有套件完全支援
- 社群經驗豐富
- 問題更容易解決

### 下一步行動：

1. **先運行相容性測試：**
   ```bash
   bash check_python_compatibility.sh
   ```

2. **如果測試通過（很可能會通過）：**
   - 使用 `studio-uvicorn-direct.service`
   - 問題與 Python 版本無關

3. **如果測試失敗：**
   - 查看錯誤訊息
   - 考慮更新套件或降級 Python

## 常見問題 FAQ

### Q1: Python 3.14 太新了嗎？
**A:** 對於實驗性項目可以，但生產環境建議使用 3.12 或 3.13。

### Q2: 需要降級 Python 嗎？
**A:** 不一定。先運行測試腳本，如果一切正常就不需要。

### Q3: 如何檢查是否有 Python 3.14 相關的問題？
**A:** 查看日誌中是否有 DeprecationWarning 或類似警告。

### Q4: 如果套件不支援 Python 3.14 怎麼辦？
**A:** 可以嘗試：
1. 更新到最新版本
2. 使用較舊但穩定的套件版本
3. 降級 Python 到 3.12

### Q5: Python 3.14 有什麼優勢？
**A:** 
- 更好的效能
- 改進的錯誤訊息
- 最新的語言特性
- 但這些優勢在生產環境中可能不如穩定性重要

## 參考資源

- Python 3.14 Release Notes: https://docs.python.org/3.14/whatsnew/3.14.html
- FastAPI Python Support: https://fastapi.tiangolo.com/#requirements
- Pydantic Compatibility: https://docs.pydantic.dev/latest/
- SQLAlchemy Support: https://docs.sqlalchemy.org/

