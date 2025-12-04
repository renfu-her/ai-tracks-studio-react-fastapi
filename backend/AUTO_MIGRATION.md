# Auto Migration 自動遷移

## 概述 Overview

從現在開始，應用程式會在每次啟動時**自動檢查並升級**資料庫結構，將所有描述欄位從 `TEXT` 升級為 `LONGTEXT`。

## 工作原理 How It Works

### 啟動流程

```
1. uv sync (安裝依賴)
   ↓
2. 啟動應用 (uv run python run.py)
   ↓
3. 創建資料表 (如果不存在)
   ↓
4. ✨ 自動檢查欄位類型 ✨
   ↓
5. 如果是 TEXT → 自動升級為 LONGTEXT
   ↓
6. 初始化管理員用戶
   ↓
7. 應用程式就緒
```

### 自動遷移的欄位

應用會自動檢查並升級以下欄位：

| 表格 | 欄位 | 目標類型 |
|------|------|----------|
| projects | description | LONGTEXT |
| news | excerpt | LONGTEXT |
| news | content | LONGTEXT |
| about_us | subtitle | LONGTEXT |
| about_us | description | LONGTEXT |

## 使用方式 Usage

### 方法一：正常啟動（推薦）⭐

```bash
# 1. 安裝/更新依賴
cd backend
uv sync

# 2. 啟動應用（會自動遷移）
uv run python run.py
```

**啟動時會看到：**
```
Creating database tables...
Database tables created successfully!
Checking database schema...
INFO:app.db_migrate:✅ Migrated projects.description to LONGTEXT
INFO:app.db_migrate:✅ Migrated news.excerpt to LONGTEXT
INFO:app.db_migrate:✅ Migrated news.content to LONGTEXT
INFO:app.db_migrate:✅ Migrated about_us.subtitle to LONGTEXT
INFO:app.db_migrate:✅ Migrated about_us.description to LONGTEXT
INFO:app.db_migrate:🎉 Auto-migration completed: 5 columns upgraded to LONGTEXT
Database schema check completed!
Admin user initialized!
INFO:     Uvicorn running on http://0.0.0.0:8000
```

### 方法二：手動遷移（可選）

如果你想在啟動前手動執行遷移：

```bash
cd backend
uv run python migrate_to_longtext.py
```

## 特性 Features

### ✅ 智能檢測
- 只在需要時執行 ALTER TABLE
- 如果已經是 LONGTEXT，跳過不處理
- 不會重複遷移

### ✅ 安全性
- 不會影響現有資料
- 向下兼容
- 失敗時只記錄警告，不中斷啟動

### ✅ 自動化
- 無需手動干預
- 每次啟動自動檢查
- 開發和生產環境統一

### ✅ 日誌記錄
- 清楚顯示遷移進度
- 記錄所有變更
- 便於追蹤和調試

## 技術細節 Technical Details

### 檢測邏輯

```python
# 1. 檢查表格是否存在
if table in existing_tables:
    # 2. 查詢欄位類型
    SELECT COLUMN_TYPE FROM INFORMATION_SCHEMA.COLUMNS
    
    # 3. 如果是 TEXT
    if column_type == 'text':
        # 4. 升級為 LONGTEXT
        ALTER TABLE table MODIFY column LONGTEXT
```

### 執行時機

自動遷移在以下時機執行：
1. `create_tables()` 之後
2. `init_admin_user()` 之前
3. 應用啟動的 `lifespan` 事件中

### 錯誤處理

- **表格不存在**：跳過（首次啟動會先創建表格）
- **權限不足**：記錄警告，繼續啟動
- **其他錯誤**：記錄警告，不影響應用運行

## 驗證 Verification

### 檢查遷移結果

**方法 1：查看啟動日誌**
```
✅ Migrated projects.description to LONGTEXT
✅ Migrated news.excerpt to LONGTEXT
...
```

**方法 2：SQL 查詢**
```sql
SELECT 
    TABLE_NAME, 
    COLUMN_NAME, 
    COLUMN_TYPE
FROM 
    INFORMATION_SCHEMA.COLUMNS
WHERE 
    TABLE_SCHEMA = 'studio'
    AND COLUMN_NAME IN ('description', 'excerpt', 'content', 'subtitle');
```

**預期結果：**
```
+------------+-------------+-----------+
| TABLE_NAME | COLUMN_NAME | COLUMN_TYPE |
+------------+-------------+-----------+
| about_us   | description | longtext  |
| about_us   | subtitle    | longtext  |
| news       | content     | longtext  |
| news       | excerpt     | longtext  |
| projects   | description | longtext  |
+------------+-------------+-----------+
```

## 優勢 Benefits

### 開發流程簡化
```bash
# 以前：
git pull
cd backend
uv sync
python migrate_to_longtext.py  # ← 需要記得執行
uv run python run.py

# 現在：
git pull
cd backend
uv sync
uv run python run.py  # ← 自動處理一切！
```

### 部署更容易
- 不需要額外的遷移步驟
- CI/CD 流程更簡單
- 減少人為錯誤

### 團隊協作更順暢
- 新成員不需要知道遷移腳本
- 所有環境自動一致
- 減少文檔維護

## 相關檔案 Related Files

- `app/db_migrate.py` - 自動遷移邏輯
- `app/main.py` - 集成到應用啟動
- `migrate_to_longtext.py` - 獨立遷移腳本（備用）
- `migrate_longtext.sql` - SQL 遷移腳本（備用）
- `MIGRATION_GUIDE.md` - 手動遷移指南（備用）

## 結論 Conclusion

🎉 **從現在開始，只需要 `uv sync` 和啟動應用，資料庫會自動升級！**

不需要手動執行遷移腳本，應用會在每次啟動時自動處理！✨

