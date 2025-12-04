-- Database Migration: TEXT to LONGTEXT
-- 將所有描述欄位從 TEXT 轉換為 LONGTEXT
-- 執行日期: 2025-12-04

-- Use the database
USE studio;

-- Projects table
ALTER TABLE projects MODIFY description LONGTEXT COMMENT '專案描述 (支援 Markdown)';

-- News table
ALTER TABLE news MODIFY excerpt LONGTEXT COMMENT '新聞摘要 (支援 Markdown)';
ALTER TABLE news MODIFY content LONGTEXT COMMENT '新聞內容 (支援 Markdown)';

-- About_us table
ALTER TABLE about_us MODIFY subtitle LONGTEXT COMMENT '副標題';
ALTER TABLE about_us MODIFY description LONGTEXT COMMENT '關於我們描述 (支援 Markdown)';

-- Verify changes
SELECT 
    TABLE_NAME as '資料表',
    COLUMN_NAME as '欄位',
    COLUMN_TYPE as '類型',
    COLUMN_COMMENT as '備註'
FROM 
    INFORMATION_SCHEMA.COLUMNS
WHERE 
    TABLE_SCHEMA = 'studio'
    AND COLUMN_TYPE LIKE '%longtext%'
ORDER BY 
    TABLE_NAME, ORDINAL_POSITION;

