-- Rename image columns to 'image'
-- 將圖片欄位重命名為 'image'

USE studio;

-- Projects: thumbnail_url -> image
ALTER TABLE projects CHANGE thumbnail_url image VARCHAR(500);

-- News: image_url -> image  
ALTER TABLE news CHANGE image_url image VARCHAR(500);

-- Verify changes
SELECT 
    TABLE_NAME as '表格',
    COLUMN_NAME as '欄位名稱',
    COLUMN_TYPE as '類型'
FROM 
    INFORMATION_SCHEMA.COLUMNS
WHERE 
    TABLE_SCHEMA = 'studio'
    AND COLUMN_NAME = 'image';

