# 使用 UV 切換 Python 版本 Switch Python Version with UV

## 🎯 超簡單！使用 UV 切換到 Python 3.12

如果你的項目使用 `uv`，切換 Python 版本只需要 **2 步**！

## 📝 步驟

### 1️⃣ 修改 `.python-version` 文件

```bash
cd /home/ai-tracks-studio/htdocs/studio.ai-tracks.com/backend

# 方法 A：直接寫入（推薦）
echo "3.12" > .python-version

# 方法 B：手動編輯
nano .python-version
# 改為：3.12
```

### 2️⃣ 讓 UV 重建環境

```bash
# 刪除舊的虛擬環境
rm -rf .venv

# UV 會自動使用 .python-version 指定的版本
uv sync
```

就這麼簡單！✨

## 🔍 完整操作流程

```bash
# 1. 停止服務
sudo systemctl stop studio-uvicorn

# 2. 進入目錄
cd /home/ai-tracks-studio/htdocs/studio.ai-tracks.com/backend

# 3. 備份（可選，但建議）
mv .venv .venv.backup.$(date +%Y%m%d_%H%M%S)

# 4. 修改 Python 版本
echo "3.12" > .python-version

# 5. 重建環境
uv sync

# 6. 驗證版本
.venv/bin/python --version
# 應該顯示：Python 3.12.x

# 7. 測試導入
.venv/bin/python -c "from app.config import settings; print('✓ OK')"

# 8. 重啟服務
sudo systemctl start studio-uvicorn

# 9. 檢查狀態
sudo systemctl status studio-uvicorn
```

## 📊 `.python-version` 文件說明

### 當前內容（Windows 開發環境）
```
cpython-3.14.0-windows-x86_64-none
```

### 修改為（Linux 生產環境）
```
3.12
```

UV 會自動：
- ✅ 檢測操作系統（Linux）
- ✅ 下載對應的 Python 3.12 版本
- ✅ 創建虛擬環境
- ✅ 安裝所有依賴

## 🚀 一鍵腳本

我創建一個簡化版的腳本：

```bash
cd /home/ai-tracks-studio/htdocs/studio.ai-tracks.com/backend
chmod +x switch_python_uv.sh
bash switch_python_uv.sh
```

## ⚠️ 注意事項

### 1. UV 會自動下載 Python

UV 有內建的 Python 管理功能，會自動下載指定版本的 Python，不需要系統預先安裝 Python 3.12！

### 2. 跨平台設置

如果你在 Windows 開發，Linux 部署，建議：

**開發環境（Windows）：**
```
# .python-version
3.12
```

**或使用平台特定的：**
```
# .python-version.windows (Windows)
cpython-3.14.0-windows-x86_64-none

# .python-version.linux (Linux)
cpython-3.12-linux-x86_64-gnu
```

但最簡單的是統一使用：
```
3.12
```

### 3. Git 處理

建議將 `.python-version` 提交到 Git：
```bash
git add .python-version
git commit -m "Switch to Python 3.12 for stability"
git push
```

這樣所有環境都會使用相同版本。

## 🔄 回滾

如果需要回滾到 Python 3.14：

```bash
# 恢復版本文件
echo "3.14" > .python-version

# 刪除並重建
rm -rf .venv
uv sync
```

## ✅ 驗證檢查

```bash
# 檢查 .python-version
cat .python-version

# 檢查實際 Python 版本
.venv/bin/python --version

# 檢查 UV 使用的 Python
uv run python --version

# 測試應用
uv run python -c "from app.config import settings; print(f'Database: {settings.DB_NAME}')"
```

## 💡 UV 的優勢

使用 UV 切換 Python 版本的好處：

1. ✅ **自動化** - UV 自動下載和管理 Python 版本
2. ✅ **隔離** - 不依賴系統 Python
3. ✅ **快速** - UV 比 pip 快 10-100 倍
4. ✅ **一致性** - 團隊成員使用相同版本
5. ✅ **簡單** - 只需修改一個文件

## 📚 UV 命令參考

```bash
# 查看 UV 使用的 Python
uv python list

# 安裝特定 Python 版本
uv python install 3.12

# 查看當前項目使用的 Python
uv run python --version

# 同步依賴（使用 .python-version 指定的版本）
uv sync

# 添加新套件
uv add package_name

# 移除套件
uv remove package_name

# 更新所有依賴
uv sync --upgrade
```

## 🎯 最佳實踐

### 建議的 `.python-version` 內容

**開發 + 生產環境統一（推薦）：**
```
3.12
```

**或指定更精確的版本：**
```
3.12.7
```

**或使用 UV 完整格式（最精確）：**
```
cpython-3.12.7
```

### pyproject.toml 中也可以指定

```toml
[project]
requires-python = ">=3.12"
```

## 🔗 相關文件

- UV Python Management: https://docs.astral.sh/uv/concepts/python-versions/
- UV Project Guide: https://docs.astral.sh/uv/guides/projects/

## 總結

使用 UV 切換 Python 版本就是這麼簡單：

```bash
echo "3.12" > .python-version
rm -rf .venv
uv sync
```

三行命令，搞定！🎉

