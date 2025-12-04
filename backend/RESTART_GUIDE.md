# 完整重啟指南 Complete Restart Guide

## 🚨 遇到 "Internal Server Error" 時執行

### 步驟 1：清除瀏覽器所有緩存

**重要！必須完全清除：**

1. 按 `Ctrl + Shift + Delete`
2. 選擇時間範圍：**不限時間**
3. 勾選：
   - ☑ Cookie 和其他網站資料
   - ☑ 快取的圖片和檔案
   - ☑ 託管應用程式資料
4. 點擊「清除資料」
5. **關閉所有瀏覽器標籤**
6. **重新開啟瀏覽器**

### 步驟 2：驗證資料庫結構

```bash
cd backend
mysql -u root studio -e "DESCRIBE projects; DESCRIBE news; DESCRIBE about_us;"
```

**應該看到所有表都有 `image` 欄位：**
- projects.image ✅
- news.image ✅
- about_us.image ✅

### 步驟 3：完全重啟後端服務器

**方法 A：使用現有終端（推薦）**

1. 切換到運行服務器的終端
2. 按 `Ctrl + C` 停止服務器
3. 等待完全停止（看到提示符）
4. 重新啟動：

```bash
cd backend
uv run uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

**方法 B：Kill 並重啟**

```bash
# Windows (PowerShell)
taskkill /F /IM python.exe

# 然後啟動
cd backend
uv run uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### 步驟 4：驗證啟動成功

**應該看到：**
```
Creating database tables...
Database tables created successfully!
Checking database schema...
Database schema check completed!
Admin user initialized!
INFO:     Application startup complete.
INFO:     Uvicorn running on http://0.0.0.0:8000
```

**不應該看到任何錯誤！**

### 步驟 5：重新訪問後台

1. 開啟新的瀏覽器標籤
2. 訪問：`http://localhost:8000/backend`
3. 登入（admin@admin.com / admin123）
4. 檢查 Console（F12）

**Console 應該顯示：**
```
[admin.js] Loading v2024120401
[admin.js] uploadImage defined: function
[admin.js] getImageUrl defined: function
[admin.js] All functions loaded successfully
[admin.js] Functions available: {checkAuth: "function", ...}
```

**不應該有任何紅色錯誤（忽略瀏覽器擴展錯誤）！**

### 步驟 6：測試專案列表

1. 導航到「專案管理」
2. 應該看到專案列表（或「暫無資料」）
3. **不應該看到 "Internal Server Error"**

### 步驟 7：測試圖片上傳

1. 點擊「新增專案」
2. 點擊「上傳圖片」
3. 選擇圖片檔案

**Console 應該顯示：**
```
[uploadImage] Uploading file: test.jpg 123456 bytes
[uploadImage] Upload success: {filename: "20251204-xxx.webp", ...}
[getImageUrl] generated URL: /static/uploads/20251204-xxx.webp
```

**圖片預覽應該立即顯示！** ✅

## 🔍 故障排除

### 如果還是看到 500 錯誤

**檢查服務器日誌：**

在運行服務器的終端中查找：
```
ERROR:    Exception in ASGI application
...
pymysql.err.OperationalError: (1054, "Unknown column...")
```

**如果看到 "Unknown column 'thumbnail_url'"：**

資料庫還沒更新，執行：
```bash
cd backend
mysql -u root studio -e "ALTER TABLE projects CHANGE thumbnail_url image VARCHAR(500);"
mysql -u root studio -e "ALTER TABLE news CHANGE image_url image VARCHAR(500);"
```

**然後重啟服務器！**

### 如果還是看到 "uploadImage is not defined"

**在 Console 執行：**
```javascript
// 手動載入 admin.js
$.getScript('/static/js/admin.js?v=' + Date.now(), function() {
    console.log('Reloaded, uploadImage:', typeof window.uploadImage);
});
```

### 如果圖片上傳成功但不顯示

**檢查：**
```javascript
// 在 Console 執行
$('#imagePreview').show();
console.log('Preview:', $('#imagePreview').is(':visible'));
console.log('Image src:', $('#previewImg').attr('src'));
```

## ✅ 完整檢查清單

執行前確認：

- [ ] 資料庫有 `image` 欄位（不是 thumbnail_url 或 image_url）
- [ ] 服務器已完全重啟
- [ ] 瀏覽器緩存已清除
- [ ] 瀏覽器標籤已關閉並重新開啟
- [ ] Console 中沒有 "not defined" 錯誤
- [ ] 服務器日誌沒有 500 錯誤

全部 ✅ 後，功能應該完全正常！

## 🎊 預期結果

**專案管理頁面：**
- ✅ 載入專案列表（無錯誤）
- ✅ 可以新增專案
- ✅ 可以上傳圖片
- ✅ 圖片立即顯示預覽
- ✅ 可以刪除圖片重新上傳
- ✅ 可以儲存專案

**Console：**
- ✅ 只有調試信息（綠色/藍色）
- ✅ 沒有紅色錯誤
- ⚠️ 可能有瀏覽器擴展的黃色警告（可忽略）

**Network 標籤：**
- ✅ `/api/admin/projects` → 200 OK
- ✅ `/api/admin/upload/image` → 200 OK
- ✅ `/static/uploads/xxx.webp` → 200 OK

