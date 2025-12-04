# Bootstrap 5 Integration Guide

## 🎨 完整的 Bootstrap 5 + jQuery 管理系統

### 📦 已整合的技術

1. **Bootstrap 5.3.2** - 現代 UI 框架
2. **jQuery 3.7.1** - DOM 操作庫
3. **Font Awesome 6.5.1** - 圖標庫

### 🏗️ Base Template 結構

**base.html** - 基礎模板（參考用）
```
├── Bootstrap 5 CSS
├── Font Awesome 6
├── Custom admin-bootstrap.css
├── Sidebar (動態載入)
├── Header (動態載入)
├── Main Content Area
├── jQuery
├── Bootstrap 5 JS
└── common-ui.js
```

### 📝 使用 Base Template

**方法 1：參考 base.html 結構**

每個頁面包含相同的基礎結構：
```html
<!DOCTYPE html>
<html lang="zh-TW">
<head>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/css/bootstrap.min.css" rel="stylesheet">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.1/css/all.min.css">
    <link rel="stylesheet" href="/static/css/admin-bootstrap.css">
</head>
<body>
    <div class="admin-layout">
        <aside class="sidebar" id="adminSidebar"></aside>
        <main class="main-content">
            <div class="admin-header" id="adminHeader"></div>
            <div class="container-fluid p-4">
                <!-- 頁面內容 -->
            </div>
        </main>
    </div>
    
    <script src="https://code.jquery.com/jquery-3.7.1.min.js"></script>
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/js/bootstrap.bundle.min.js"></script>
    <script src="/static/js/admin.js"></script>
    <script src="/static/js/common-ui.js"></script>
</body>
</html>
```

**方法 2：使用 common-ui.js 共用組件**

Sidebar 和 Header 會自動載入：
```javascript
$(document).ready(function() {
    // Sidebar 和 Header 自動載入
    setPageTitle('您的頁面標題');
    
    // 您的代碼...
});
```

### 🎯 Full-Width Filter Bar 全寬篩選欄

參考圖片設計：

```html
<div class="d-flex gap-3 mb-4 align-items-center flex-wrap">
    <!-- 搜尋 -->
    <div class="flex-grow-1" style="max-width: 400px;">
        <input type="text" class="form-control" placeholder="搜尋標題...">
    </div>
    
    <!-- 類別下拉選單 -->
    <div class="dropdown">
        <button class="btn btn-outline-secondary dropdown-toggle" data-bs-toggle="dropdown">
            <span>所有類別</span>
        </button>
        <ul class="dropdown-menu">
            <li><a class="dropdown-item" href="#">所有類別</a></li>
            <li><a class="dropdown-item" href="#">遊戲 (GAME)</a></li>
            <li><a class="dropdown-item" href="#">網站 (WEBSITE)</a></li>
        </ul>
    </div>
    
    <!-- 每頁筆數 -->
    <div class="dropdown">
        <button class="btn btn-outline-secondary dropdown-toggle" data-bs-toggle="dropdown">
            <span>10筆/頁</span>
        </button>
        <ul class="dropdown-menu">
            <li><a class="dropdown-item" href="#">10筆/頁</a></li>
            <li><a class="dropdown-item" href="#">20筆/頁</a></li>
            <li><a class="dropdown-item" href="#">50筆/頁</a></li>
        </ul>
    </div>
    
    <!-- 新增按鈕 (ms-auto 推到右側) -->
    <a href="/add" class="btn btn-primary ms-auto">
        <i class="fas fa-plus me-2"></i> 新增 Project
    </a>
</div>
```

### 📊 Bootstrap 5 Components 組件使用

#### Tables 表格
```html
<div class="table-responsive">
    <table class="table table-hover align-middle">
        <thead>
            <tr>
                <th>欄位名稱</th>
            </tr>
        </thead>
        <tbody>
            <tr>
                <td>資料</td>
            </tr>
        </tbody>
    </table>
</div>
```

#### Badges 標籤
```html
<span class="badge bg-success">啟用</span>
<span class="badge bg-danger">停用</span>
<span class="badge badge-game">GAME</span>
```

#### Buttons 按鈕
```html
<button class="btn btn-primary">主要按鈕</button>
<button class="btn btn-outline-primary">外框按鈕</button>
<button class="btn btn-sm btn-danger">小型危險按鈕</button>
```

#### Modals 彈窗
```javascript
// 使用 common-ui.js 提供的函數
confirmDelete('確定要刪除嗎？', function() {
    // 刪除邏輯
});
```

#### Toasts 提示
```javascript
showSuccessToast('操作成功！');
showErrorToast('操作失敗！');
```

### 🔧 jQuery 常用操作

#### 選擇器
```javascript
$('#elementId')           // ID 選擇器
$('.className')           // Class 選擇器
$('button')               // 標籤選擇器
$('[data-id="123"]')      // 屬性選擇器
```

#### DOM 操作
```javascript
$('#container').html('<p>內容</p>');     // 設定 HTML
$('#input').val('value');                 // 設定值
$('#input').val();                        // 取得值
$('.element').addClass('active');         // 添加 class
$('.element').removeClass('active');      // 移除 class
$('.element').toggleClass('active');      // 切換 class
```

#### 事件監聽
```javascript
$('#btn').click(function() { });         // 點擊事件
$('#input').on('input', function() { }); // 輸入事件
$('.item').on('change', function() { }); // 改變事件
```

#### AJAX 請求
```javascript
// GET 請求
$.ajax({
    url: '/api/admin/projects',
    method: 'GET',
    success: function(data) {
        console.log(data);
    },
    error: function(xhr) {
        console.error('Error:', xhr);
    }
});

// POST 請求
$.ajax({
    url: '/api/admin/projects',
    method: 'POST',
    contentType: 'application/json',
    data: JSON.stringify({ id: '1', title: 'Test' }),
    success: function(data) {
        showSuccessToast('新增成功！');
    }
});

// 簡化的 GET
$.get('/api/admin/projects', function(data) {
    console.log(data);
});

// 簡化的 POST
$.post('/api/admin/projects', { data }, function(response) {
    console.log(response);
});
```

### 🎨 Custom Styles 自定義樣式

`admin-bootstrap.css` 提供：
- Sidebar 深藍色主題
- 導航高亮效果
- 表格 hover 效果
- 自定義 badge 顏色
- 響應式佈局

### 📱 Responsive Design 響應式設計

Bootstrap 5 的 Grid System：
```html
<div class="row">
    <div class="col-12 col-md-6 col-lg-4">
        <!-- 手機全寬，平板半寬，桌面 1/3 寬 -->
    </div>
</div>
```

Flexbox Utilities：
```html
<div class="d-flex justify-content-between align-items-center">
    <div>左側</div>
    <div class="ms-auto">右側</div>
</div>
```

### 🚀 示範頁面

**已創建：**
- `admin/projects/index-bootstrap.html` - 完整的 Bootstrap 5 示範

**訪問：**
```
http://localhost:8000/backend/projects
```

（需要更新 main.py 路由指向新的 bootstrap 版本，或直接訪問文件）

### 📋 頁面結構模板

**index 列表頁：**
```html
<div class="container-fluid p-4">
    <div class="admin-card">
        <!-- 篩選欄 -->
        <div class="d-flex gap-3 mb-4">
            <input class="form-control" placeholder="搜尋...">
            <div class="dropdown">...</div>
            <a href="/add" class="btn btn-primary ms-auto">新增</a>
        </div>
        
        <!-- 表格 -->
        <div class="table-responsive">
            <table class="table">...</table>
        </div>
        
        <!-- 分頁資訊 -->
        <div class="d-flex justify-content-between">
            <div>顯示資訊</div>
            <nav>分頁按鈕</nav>
        </div>
    </div>
</div>
```

**add-edit 表單頁：**
```html
<div class="container-fluid p-4">
    <div class="admin-card">
        <h2>新增/編輯</h2>
        <form class="w-100">
            <div class="mb-3">
                <label class="form-label">標題 *</label>
                <input type="text" class="form-control" required>
            </div>
            <!-- 更多欄位... -->
            <div class="mt-4">
                <button type="submit" class="btn btn-primary">
                    <i class="fas fa-save me-2"></i> 儲存
                </button>
                <a href="/list" class="btn btn-secondary">取消</a>
            </div>
        </form>
    </div>
</div>
```

### ✨ Common UI Functions 共用函數

**載入相關：**
- `showBootstrapLoading(id)` - 顯示載入動畫
- `showBootstrapError(id, msg)` - 顯示錯誤

**提示相關：**
- `showSuccessToast(msg)` - 成功提示（右上角）
- `showErrorToast(msg)` - 錯誤提示（右上角）

**對話框：**
- `confirmDelete(msg, callback)` - 刪除確認 Modal

**頁面相關：**
- `setPageTitle(title)` - 設定標題
- `loadSidebar()` - 載入側邊欄
- `loadHeader()` - 載入頁首

### 🎯 Benefits 優勢

✅ **統一風格** - Bootstrap 5 一致的設計語言  
✅ **響應式** - 自動適應各種螢幕  
✅ **組件豐富** - 表格、表單、按鈕等  
✅ **jQuery 簡化** - DOM 操作更簡單  
✅ **共用組件** - Sidebar/Header 重用  
✅ **美觀 Toast** - 優雅的提示訊息  
✅ **Modal 對話框** - 互動式確認  

### 📚 Resources 資源

- Bootstrap 5: https://getbootstrap.com/docs/5.3/
- jQuery: https://api.jquery.com/
- Font Awesome: https://fontawesome.com/icons

---

**Bootstrap 5 + jQuery 系統已就緒！** 🎊  
參考 `index-bootstrap.html` 開始使用新的模板系統！

