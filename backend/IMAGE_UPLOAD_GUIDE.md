# Image Upload Guide 圖片上傳指南

## 📸 WebP 圖片上傳功能

所有管理頁面（Projects、News、About）都支持圖片上傳並自動轉換為 WebP 格式。

## 🚀 Quick Start 快速開始

### 1. 訪問管理頁面

```
http://localhost:8000/backend/projects/add
http://localhost:8000/backend/news/add
```

### 2. 上傳圖片

1. 點擊「📤 上傳圖片」按鈕
2. 選擇圖片文件（JPEG、PNG、GIF）
3. 自動上傳並轉換為 WebP
4. URL 自動填入表單
5. 顯示預覽和檔案資訊

## 📋 Supported Formats 支持格式

### Input 輸入格式
- ✅ JPEG / JPG
- ✅ PNG (含透明背景)
- ✅ GIF
- ✅ WebP

### Output 輸出格式
- ✅ WebP (統一格式)
- ✅ Quality: 85%
- ✅ Optimized compression

## 🔧 Technical Details 技術細節

### API Endpoint

**Upload Image:**
```
POST /api/admin/upload/image
Content-Type: multipart/form-data
```

**Request:**
```bash
curl -X POST http://localhost:8000/api/admin/upload/image \
  -H "Content-Type: multipart/form-data" \
  -F "file=@image.jpg" \
  --cookie cookies.txt
```

**Response:**
```json
{
  "success": true,
  "url": "/static/uploads/20251203_225703_123456.webp",
  "filename": "20251203_225703_123456.webp",
  "size": 45678
}
```

### File Processing 文件處理

**1. Transparency Handling 透明度處理**
```python
# RGBA/LA/P modes → RGB with white background
if image.mode in ('RGBA', 'LA', 'P'):
    background = Image.new('RGB', image.size, (255, 255, 255))
    background.paste(image, mask=...)
```

**2. WebP Conversion**
```python
image.save(
    filepath,
    'WEBP',
    quality=85,      # 85% quality
    method=6,        # Best compression
    optimize=True    # Additional optimization
)
```

**3. Filename Generation**
```python
# Format: YYYYMMDD_HHMMSS_microseconds.webp
timestamp = datetime.now().strftime('%Y%m%d_%H%M%S_%f')
filename = f"{timestamp}.webp"
```

## 📁 Storage Structure 儲存結構

```
backend/app/static/uploads/
├── 20251203_225703_123456.webp
├── 20251203_225704_789012.webp
└── ...
```

**Public URL:**
```
http://localhost:8000/static/uploads/{filename}.webp
```

## 💡 Usage in Forms 表單使用

### Projects 專案

**縮圖上傳：**
1. 欄位：「縮圖」
2. 可選：輸入 URL 或上傳圖片
3. 上傳後自動填入 URL
4. 顯示預覽圖

### News 新聞

**圖片上傳：**
1. 欄位：「圖片」
2. 上傳新聞配圖
3. 自動轉 WebP
4. 預覽功能

### About 關於我們

About 頁面的圖片通常在 values JSON 中設定：
```json
[
  {
    "icon": "Star",
    "title": "Creativity",
    "description": "...",
    "image": "/static/uploads/xxx.webp"
  }
]
```

## 🎨 UI Features UI 功能

### Upload Button 上傳按鈕
- 📤 圖標 + 文字
- 藍色主按鈕樣式
- 點擊觸發文件選擇器

### Preview 預覽
- 最大寬度：300px
- 最大高度：200px
- 圓角邊框
- 自動縮放

### Info Display 資訊顯示
- ✅ 上傳成功：綠色文字
- ❌ 上傳失敗：紅色文字
- 📊 檔案資訊：名稱、大小、格式

### Progress 進度
- 上傳中...（loading 狀態）
- 完成：顯示結果
- 錯誤：顯示錯誤訊息

## 🔒 Security 安全性

### File Validation 文件驗證
- ✅ Content-Type 檢查
- ✅ File size limit (10MB)
- ✅ Admin authentication required
- ✅ File extension validation

### Limits 限制
- Maximum file size: 10MB
- Allowed types: JPEG, PNG, GIF, WebP
- Admin access only

## ⚡ Performance 性能

### WebP Advantages WebP 優勢
- 📉 30-50% smaller file size vs JPEG/PNG
- 🚀 Faster page loading
- 💾 Reduced bandwidth usage
- 🎨 Better quality at same size

### Compression Settings 壓縮設定
- Quality: 85% (視覺上無損，體積大幅減少)
- Method: 6 (最佳壓縮，稍慢但文件更小)
- Optimize: true (額外優化)

## 🧪 Testing 測試

### Test Upload 測試上傳

1. **Via UI (推薦):**
   - 訪問 http://localhost:8000/backend/projects/add
   - 點擊「上傳圖片」
   - 選擇圖片
   - 查看預覽和資訊

2. **Via API:**
```bash
curl -X POST http://localhost:8000/api/admin/upload/image \
  -F "file=@test.jpg" \
  --cookie cookies.txt
```

### Verify Conversion 驗證轉換

1. 上傳 PNG/JPEG 圖片
2. 檢查 `backend/app/static/uploads/` 目錄
3. 確認文件是 `.webp` 格式
4. 用瀏覽器打開確認可正常顯示

## 📊 File Size Comparison 文件大小對比

Example (typical results):
- Original JPEG (1920x1080): 850 KB
- Converted WebP: 420 KB (50% smaller)

- Original PNG (1920x1080): 2.3 MB
- Converted WebP: 380 KB (83% smaller)

## 🛠️ Troubleshooting 疑難排解

### Upload Failed 上傳失敗

**File too large:**
- Solution: Resize image before upload or increase `MAX_FILE_SIZE`

**Invalid format:**
- Solution: Use JPEG, PNG, or GIF only

**Permission denied:**
- Solution: Ensure uploads directory has write permission

### Preview Not Showing 預覽未顯示

- Check browser console for errors
- Verify URL is correct
- Check if file exists in uploads directory

## 🎯 Best Practices 最佳實踐

1. **Image Dimensions 圖片尺寸**
   - Projects thumbnail: 600x400 推薦
   - News image: 800x600 推薦
   - Keep aspect ratio

2. **File Size 文件大小**
   - Resize large images before upload
   - Target < 500KB for web use

3. **Naming Convention 命名規範**
   - System auto-generates unique names
   - No manual intervention needed

## ✨ Features Summary 功能總結

✅ **Auto WebP Conversion** - 自動轉換為 WebP  
✅ **Transparency Support** - 透明度轉白色背景  
✅ **Image Preview** - 即時預覽  
✅ **Size Optimization** - 最佳化壓縮  
✅ **Unique Filenames** - 時間戳命名  
✅ **Error Handling** - 完整錯誤處理  
✅ **Progress Feedback** - 上傳狀態提示  
✅ **Clean UI** - 簡潔的界面  

---

**圖片上傳功能已完成！** 🎊  
現在可以在所有管理頁面上傳並自動轉換圖片為 WebP 格式！

