# Image Upload with UUID7 圖片上傳（UUID7）

## 概述 Overview

圖片上傳功能已升級，現在使用 **UUID7** 作為文件名，並且只保存文件名（不含路徑）。

## 工作原理 How It Works

### 上傳流程

```
1. 用戶選擇圖片
   ↓
2. 上傳到 /api/admin/upload/image
   ↓
3. 轉換為 WebP 格式
   ↓
4. 使用 UUID7 生成唯一文件名
   例如: 018e0e36-4f8a-7000-8000-123456789abc.webp
   ↓
5. 保存到 static/uploads/
   ↓
6. 返回文件名（不含路徑）
```

### 儲存方式

**資料庫中：**
- ✅ 只保存文件名：`018e0e36-4f8a-7000-8000-123456789abc.webp`
- ❌ 不保存完整路徑：~~`/static/uploads/xxx.webp`~~

**前端顯示時：**
- 使用 `getImageUrl(filename)` 函數自動加上路徑
- 自動生成：`/static/uploads/018e0e36-4f8a-7000-8000-123456789abc.webp`

## UUID7 優勢 Benefits

### 為什麼使用 UUID7？

**1. 時間排序 Time-Ordered**
- UUID7 包含時間戳，自然按時間排序
- 適合資料庫索引（B-tree 友好）
- 比 UUID4 更高效

**2. 全域唯一 Globally Unique**
- 跨伺服器不會衝突
- 分散式環境友好
- 無需中央協調

**3. 可讀性 Readability**
- 前綴包含時間戳
- 易於追蹤和調試
- 日誌中更有意義

**4. 安全性 Security**
- 無法猜測文件名
- 防止枚舉攻擊
- 不洩露上傳順序

### UUID7 vs 時間戳

| 特性 | 時間戳 | UUID7 |
|------|--------|-------|
| 唯一性 | ❌ 可能衝突 | ✅ 全域唯一 |
| 排序 | ✅ 按時間 | ✅ 按時間 |
| 安全性 | ❌ 可預測 | ✅ 不可預測 |
| 分散式 | ❌ 需協調 | ✅ 無需協調 |

## API 變更 API Changes

### 上傳 API Response

**舊版：**
```json
{
    "success": true,
    "url": "/static/uploads/20241204_143012_123456.webp",
    "filename": "20241204_143012_123456.webp",
    "size": 45678
}
```

**新版：**
```json
{
    "success": true,
    "filename": "018e0e36-4f8a-7000-8000-123456789abc.webp",
    "size": 45678
}
```

**主要變更：**
- ✅ 移除 `url` 欄位
- ✅ 只返回 `filename`
- ✅ 文件名使用 UUID7

## 前端使用 Frontend Usage

### 上傳圖片

```javascript
// 上傳圖片（返回文件名）
const filename = await uploadImage(file);

// 保存文件名到輸入框
$('#imageInput').val(filename);

// 顯示預覽（自動加上路徑）
const imageUrl = getImageUrl(filename);
$('#previewImg').attr('src', imageUrl);
```

### 輔助函數

**`uploadImage(file)`**
```javascript
// 上傳圖片，返回文件名
async function uploadImage(file) {
    const formData = new FormData();
    formData.append('file', file);
    
    const response = await fetch('/api/admin/upload/image', {
        method: 'POST',
        credentials: 'include',
        body: formData
    });
    
    const result = await response.json();
    return result.filename; // 只返回文件名
}
```

**`getImageUrl(filename)`**
```javascript
// 將文件名轉換為完整 URL
function getImageUrl(filename) {
    if (!filename) return '';
    if (filename.startsWith('http')) return filename; // 外部連結
    if (filename.startsWith('/static/uploads/')) return filename; // 已有路徑
    return `/static/uploads/${filename}`; // 加上路徑
}
```

## 資料庫欄位 Database Fields

### 受影響的欄位

| 表格 | 欄位 | 儲存內容 |
|------|------|----------|
| projects | thumbnail_url | UUID7文件名 |
| news | image_url | UUID7文件名 |
| about_us | banner_image_url | UUID7文件名 |

### 範例資料

**資料庫中：**
```sql
INSERT INTO projects VALUES (
    'game-001',
    'My Game',
    '018e0e36-4f8a-7000-8000-123456789abc.webp'  -- 只保存文件名
);
```

**前端顯示：**
```html
<img src="/static/uploads/018e0e36-4f8a-7000-8000-123456789abc.webp">
```

## 遷移指南 Migration Guide

### 現有資料處理

如果資料庫中有舊格式的路徑：

**舊格式：** `/static/uploads/20241204_143012.webp`
**新格式：** `018e0e36-4f8a-7000-8000-123456789abc.webp`

**`getImageUrl()` 函數會自動處理：**
```javascript
// 舊格式（已有路徑）- 直接返回
getImageUrl('/static/uploads/old.webp') 
// → '/static/uploads/old.webp'

// 新格式（只有文件名）- 加上路徑
getImageUrl('018e0e36-4f8a-7000-8000-123456789abc.webp')
// → '/static/uploads/018e0e36-4f8a-7000-8000-123456789abc.webp'

// 外部連結 - 直接返回
getImageUrl('https://cdn.example.com/image.jpg')
// → 'https://cdn.example.com/image.jpg'
```

### 不需要手動遷移

- ✅ `getImageUrl()` 向下兼容
- ✅ 新上傳自動使用 UUID7
- ✅ 舊圖片仍然可以正常顯示
- ✅ 逐步替換即可

## 檔案結構 File Structure

```
backend/
├── static/
│   └── uploads/
│       ├── 018e0e36-4f8a-7000-8000-123456789abc.webp  ← UUID7
│       ├── 018e0e36-5a2b-7000-8000-def123456789.webp
│       └── 018e0e36-6c4d-7000-8000-abc987654321.webp
│
├── app/
│   ├── routers/admin/upload.py  ← 上傳 API（使用 UUID7）
│   └── static/js/admin.js       ← 輔助函數
│
└── pyproject.toml               ← 添加 uuid7 依賴
```

## 安裝依賴 Install Dependencies

```bash
cd backend
uv sync  # 會自動安裝 uuid7
```

## 測試 Testing

### 測試上傳功能

1. 登入後台：http://localhost:8000/backend
2. 進入專案管理 → 新增專案
3. 點擊「上傳」按鈕選擇圖片
4. 觀察：
   - ✅ 顯示 UUID7 前綴
   - ✅ 圖片預覽正常
   - ✅ 輸入框只有文件名

### 驗證資料庫

```sql
-- 查看保存的文件名
SELECT id, title, thumbnail_url 
FROM projects 
WHERE thumbnail_url IS NOT NULL;

-- 應該看到類似：
-- 018e0e36-4f8a-7000-8000-123456789abc.webp
```

### 驗證檔案系統

```bash
# 查看上傳的檔案
ls -la backend/static/uploads/

# 應該看到 UUID7 格式的文件名
# 018e0e36-4f8a-7000-8000-123456789abc.webp
```

## 優勢總結 Benefits Summary

### 儲存空間
- ✅ 資料庫欄位更短（只有文件名）
- ✅ 便於備份和遷移
- ✅ 路徑可靈活配置

### 安全性
- ✅ UUID7 不可預測
- ✅ 防止檔案枚舉
- ✅ 無時間戳洩露

### 擴展性
- ✅ 易於切換 CDN
- ✅ 支援多儲存位置
- ✅ 分散式友好

### 維護性
- ✅ 文件名有意義（包含時間）
- ✅ 自動排序
- ✅ 易於追蹤

## 完成！✨

現在圖片上傳使用 UUID7，只保存文件名，更安全、更靈活、更高效！🎉

