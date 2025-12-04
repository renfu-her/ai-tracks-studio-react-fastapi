# Database Migration Guide 資料庫遷移指南

## 目的 Purpose

將所有描述欄位從 `TEXT` (最大 64KB) 升級為 `LONGTEXT` (最大 4GB)，以支援更長的 Markdown 內容。

## 方法一：Python 自動遷移腳本 (推薦)

### 步驟：

```bash
# 1. 進入 backend 目錄
cd backend

# 2. 執行遷移腳本
uv run python migrate_to_longtext.py

# 3. 確認提示後輸入 yes
# Continue with migration? (yes/no): yes
```

### 輸出示例：

```
============================================================
Database Migration: TEXT → LONGTEXT
============================================================

🔗 Connected to database
📊 Database: ai_tracks_studio

⏳ Migrating projects.description... ✅ Success
⏳ Migrating news.excerpt... ✅ Success
⏳ Migrating news.content... ✅ Success
⏳ Migrating about_us.subtitle... ✅ Success
⏳ Migrating about_us.description... ✅ Success

============================================================
✅ Migration completed: 5/5 columns updated
============================================================

📋 Updated columns:
   - projects.description → LONGTEXT
   - news.excerpt → LONGTEXT
   - news.content → LONGTEXT
   - about_us.subtitle → LONGTEXT
   - about_us.description → LONGTEXT

🎉 All description fields now support up to 4GB of content!
```

## 方法二：手動執行 SQL

### 選項 A - 執行 SQL 檔案：

```bash
# 使用 MySQL 命令列執行
mysql -u root -p studio < migrate_longtext.sql
```

### 選項 B - 直接執行 SQL 命令：

```sql
-- 連接到資料庫
USE studio;

-- Projects 表
ALTER TABLE projects MODIFY description LONGTEXT;

-- News 表
ALTER TABLE news MODIFY excerpt LONGTEXT;
ALTER TABLE news MODIFY content LONGTEXT;

-- About_us 表
ALTER TABLE about_us MODIFY subtitle LONGTEXT;
ALTER TABLE about_us MODIFY description LONGTEXT;
```

## 驗證遷移 Verify Migration

### 檢查欄位類型：

```sql
SELECT 
    TABLE_NAME as '資料表',
    COLUMN_NAME as '欄位',
    COLUMN_TYPE as '類型'
FROM 
    INFORMATION_SCHEMA.COLUMNS
WHERE 
    TABLE_SCHEMA = 'studio'
    AND COLUMN_NAME IN ('description', 'excerpt', 'content', 'subtitle')
ORDER BY 
    TABLE_NAME, COLUMN_NAME;
```

### 預期結果：

| 資料表 | 欄位 | 類型 |
|--------|------|------|
| about_us | description | longtext |
| about_us | subtitle | longtext |
| news | content | longtext |
| news | excerpt | longtext |
| projects | description | longtext |

## 備份建議 Backup Recommendation

**⚠️ 重要：執行遷移前建議備份資料庫**

```bash
# 備份整個資料庫
mysqldump -u root -p studio > backup_$(date +%Y%m%d_%H%M%S).sql

# 或只備份資料（不含結構）
mysqldump -u root -p --no-create-info studio > data_backup_$(date +%Y%m%d_%H%M%S).sql
```

## 回滾 Rollback

如果需要回滾到 TEXT：

```sql
-- 回滾到 TEXT
ALTER TABLE projects MODIFY description TEXT;
ALTER TABLE news MODIFY excerpt TEXT;
ALTER TABLE news MODIFY content TEXT;
ALTER TABLE about_us MODIFY subtitle TEXT;
ALTER TABLE about_us MODIFY description TEXT;
```

## 注意事項 Notes

1. ✅ **無資料損失** - ALTER MODIFY 不會影響現有資料
2. ✅ **向下兼容** - LONGTEXT 完全兼容 TEXT
3. ⚠️ **鎖表時間** - 大表可能需要較長時間
4. ✅ **安全操作** - 可以在生產環境執行

## 效能影響 Performance Impact

- **儲存空間**: LONGTEXT 使用更多儲存空間（但只在需要時）
- **查詢速度**: 對短文本無影響
- **索引**: 這些欄位本來就不應該建索引

## 完成後 After Migration

重啟應用程式以使用新的 schema：

```bash
cd backend
uv run python run.py
```

現在可以儲存超長的 Markdown 內容（最多 4GB）！🎉

