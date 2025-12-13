-- Add views column to about_us, news, and projects tables
-- 為 about_us、news 和 projects 表添加 views 欄位

USE studio;

-- Add views column to about_us table
-- 為 about_us 表添加 views 欄位
ALTER TABLE about_us 
ADD COLUMN views INT DEFAULT 0 NOT NULL 
AFTER contact_email;

-- Add views column to news table
-- 為 news 表添加 views 欄位
ALTER TABLE news 
ADD COLUMN views INT DEFAULT 0 NOT NULL 
AFTER author;

-- Add views column to projects table
-- 為 projects 表添加 views 欄位
ALTER TABLE projects 
ADD COLUMN views INT DEFAULT 0 NOT NULL 
AFTER link;

-- Verify changes
-- 驗證變更
SELECT 
    TABLE_NAME as '表格',
    COLUMN_NAME as '欄位名稱',
    COLUMN_TYPE as '類型',
    COLUMN_DEFAULT as '預設值',
    IS_NULLABLE as '可為空'
FROM 
    INFORMATION_SCHEMA.COLUMNS
WHERE 
    TABLE_SCHEMA = 'studio'
    AND COLUMN_NAME = 'views'
ORDER BY TABLE_NAME;
