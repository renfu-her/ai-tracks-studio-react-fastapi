# Template System Guide 模板系統指南

## 🎨 Base Template 系統

所有管理頁面都使用統一的 base template 結構，實現代碼重用和一致性。

## 📁 核心文件

### 1. Template Loader
**`static/js/template-loader.js`** - 模板載入器
- `initAdminTemplate(options)` - 初始化管理頁面
- `loadAdminSidebar(activePage)` - 載入側邊欄
- `loadAdminHeader(pageTitle)` - 載入頁首
- 共用函數：Toast、Modal、Loading 等

### 2. Base HTML 結構
```html
<div class="admin-layout">
    <aside class="sidebar" id="adminSidebar"></aside>
    <main class="main-content">
        <div class="admin-header" id="adminHeader"></div>
        <div class="container-fluid p-4">
            <!-- 頁面內容 -->
        </div>
    </main>
</div>
```

### 3. 必要的 CDN
- Bootstrap 5.3.2
- jQuery 3.7.1
- Font Awesome 6.5.1

## 🚀 使用方式

### Index 列表頁模板

```html
<!DOCTYPE html>
<html lang="zh-TW">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>頁面標題</title>
    
    <!-- CDN -->
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
                <div class="admin-card">
                    <!-- RWD 篩選欄 -->
                    <div class="row g-3 mb-4 align-items-center">
                        <div class="col-12 col-sm-6 col-md-4 col-lg-3">
                            <input type="text" class="form-control" placeholder="搜尋...">
                        </div>
                        <div class="col-6 col-sm-3 col-md-2 col-lg-2">
                            <select class="form-select">...</select>
                        </div>
                        <div class="col-0 d-none d-lg-block" style="flex: 1;"></div>
                        <div class="col-12 col-md-auto ms-md-auto">
                            <a href="/add" class="btn btn-primary w-100 w-lg-auto">
                                <i class="fas fa-plus me-2"></i> 新增
                            </a>
                        </div>
                    </div>

                    <!-- 內容容器 -->
                    <div id="dataContainer"></div>
                </div>
            </div>
        </main>
    </div>

    <!-- Scripts -->
    <script src="https://code.jquery.com/jquery-3.7.1.min.js"></script>
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/js/bootstrap.bundle.min.js"></script>
    <script src="/static/js/admin.js"></script>
    <script src="/static/js/template-loader.js"></script>
    
    <script>
        // 使用 template loader 初始化
        initAdminTemplate({
            pageTitle: '您的頁面標題',
            activePage: 'projects',  // or 'news', 'about'
            onReady: async function(user) {
                // 您的初始化代碼
                await loadData();
            }
        });

        async function loadData() {
            // 載入資料邏輯
        }
    </script>
</body>
</html>
```

### Add/Edit 表單頁模板

```html
<!DOCTYPE html>
<html lang="zh-TW">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>表單頁面</title>
    
    <!-- Same CDN links -->
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
                <div class="admin-card">
                    <h2 class="mb-4" id="formTitle">表單標題</h2>
                    
                    <!-- RWD 表單 (兩欄佈局) -->
                    <form id="mainForm">
                        <div class="row g-3">
                            <!-- 左欄 -->
                            <div class="col-12 col-lg-6">
                                <div class="mb-3">
                                    <label class="form-label fw-bold">欄位 *</label>
                                    <input type="text" class="form-control" required>
                                </div>
                            </div>
                            
                            <!-- 右欄 -->
                            <div class="col-12 col-lg-6">
                                <div class="mb-3">
                                    <label class="form-label fw-bold">欄位</label>
                                    <input type="text" class="form-control">
                                </div>
                            </div>
                        </div>

                        <!-- 按鈕 -->
                        <div class="border-top pt-4 mt-4">
                            <div class="d-flex gap-2">
                                <button type="submit" class="btn btn-primary px-4">
                                    <i class="fas fa-save me-2"></i> 儲存
                                </button>
                                <a href="/list" class="btn btn-secondary px-4">
                                    <i class="fas fa-times me-2"></i> 取消
                                </a>
                            </div>
                        </div>
                    </form>
                </div>
            </div>
        </main>
    </div>

    <!-- Same scripts -->
    <script src="https://code.jquery.com/jquery-3.7.1.min.js"></script>
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/js/bootstrap.bundle.min.js"></script>
    <script src="/static/js/admin.js"></script>
    <script src="/static/js/template-loader.js"></script>
    
    <script>
        let isEditMode = false;

        initAdminTemplate({
            pageTitle: '新增項目',
            activePage: 'projects',
            onReady: async function(user) {
                // 檢查編輯模式
                const id = new URLSearchParams(window.location.search).get('id');
                if (id) {
                    isEditMode = true;
                    loadAdminHeader('編輯項目');
                    $('#formTitle').text('編輯項目');
                    await loadItem(id);
                }
            }
        });

        $('#mainForm').submit(async function(e) {
            e.preventDefault();
            // 表單提交邏輯
        });
    </script>
</body>
</html>
```

## 🎯 initAdminTemplate() 參數

```javascript
initAdminTemplate({
    pageTitle: 'Projects 管理',  // 頁面標題
    activePage: 'projects',       // 當前頁面 (高亮側邊欄)
    onReady: async function(user) {
        // 認證成功後執行
        // user 是當前登入的用戶資訊
    }
});
```

**activePage 選項:**
- `'projects'` - Projects 管理
- `'news'` - News 管理
- `'about'` - About 管理

## 📐 RWD 篩選欄佈局

### 完整分散式佈局

```html
<div class="row g-3 mb-4 align-items-center">
    <!-- 搜尋 (手機全寬，平板 4/12，桌面 3/12) -->
    <div class="col-12 col-sm-6 col-md-4 col-lg-3">
        <input class="form-control" placeholder="搜尋...">
    </div>
    
    <!-- 篩選1 (手機半寬，桌面 2/12) -->
    <div class="col-6 col-sm-3 col-md-2 col-lg-2">
        <select class="form-select">...</select>
    </div>
    
    <!-- 篩選2 (手機半寬，桌面 2/12) -->
    <div class="col-6 col-sm-3 col-md-2 col-lg-2">
        <select class="form-select">...</select>
    </div>
    
    <!-- 彈性空間 (只在大螢幕顯示，填充剩餘空間) -->
    <div class="col-0 d-none d-lg-block" style="flex: 1;"></div>
    
    <!-- 按鈕 (手機全寬，平板後自動寬度右對齊) -->
    <div class="col-12 col-md-auto ms-md-auto">
        <a href="/add" class="btn btn-primary w-100 w-lg-auto">
            <i class="fas fa-plus me-2"></i> 新增
        </a>
    </div>
</div>
```

### 響應式效果

**手機 (< 576px):**
```
[=============== 搜尋 ===============]  100%
[====== 篩選1 ======][====== 篩選2 ======]  各50%
[=============== 按鈕 ===============]  100%
```

**平板 (768px):**
```
[===== 搜尋 =====][== 篩選1 ==][== 篩選2 ==]   [按鈕]
    33.33%           16.67%        16.67%      auto右對齊
```

**桌面 (1200px):**
```
[=== 搜尋 ===][篩選1][篩選2]................[按鈕]
    25%       16.67% 16.67%   彈性空間      auto
```

## 🎨 兩欄表單佈局

```html
<form>
    <div class="row g-3">
        <!-- 左欄 (手機全寬，桌面半寬) -->
        <div class="col-12 col-lg-6">
            <div class="mb-3">
                <label class="form-label fw-bold">欄位1</label>
                <input type="text" class="form-control">
            </div>
        </div>
        
        <!-- 右欄 (手機全寬，桌面半寬) -->
        <div class="col-12 col-lg-6">
            <div class="mb-3">
                <label class="form-label fw-bold">欄位2</label>
                <input type="text" class="form-control">
            </div>
        </div>
    </div>
</form>
```

## 🔧 jQuery 常用操作

### 取得/設定值
```javascript
const value = $('#inputId').val();        // 取得值
$('#inputId').val('new value');           // 設定值
const html = $('#container').html();      // 取得 HTML
$('#container').html('<p>New</p>');       // 設定 HTML
```

### 事件監聽
```javascript
$('#btn').click(function() { });          // 點擊
$('#input').on('input', function() { });  // 輸入
$('#select').on('change', function() { });// 改變
$('form').submit(async function(e) {      // 表單提交
    e.preventDefault();
});
```

### Class 操作
```javascript
$('.item').addClass('active');            // 添加 class
$('.item').removeClass('active');         // 移除 class
$('.item').toggleClass('active');         // 切換 class
$('.item').hasClass('active');            // 檢查 class
```

### 顯示/隱藏
```javascript
$('.element').show();                     // 顯示
$('.element').hide();                     // 隱藏
$('.element').toggle();                   // 切換
$('.element').addClass('d-none');         // Bootstrap 隱藏
$('.element').removeClass('d-none');      // Bootstrap 顯示
```

## 📊 示範頁面

### 已創建的新版本 (使用 base template):

1. **`admin/projects/index-v2.html`**
   - ✅ 使用 `initAdminTemplate()`
   - ✅ RWD 分散式篩選欄
   - ✅ Bootstrap 5 表格
   - ✅ jQuery 事件處理
   - ✅ Toast 通知
   - ✅ Modal 確認

2. **`admin/projects/add-edit-v2.html`**
   - ✅ 使用 `initAdminTemplate()`
   - ✅ 兩欄 RWD 表單
   - ✅ 圖片上傳（jQuery AJAX）
   - ✅ 自動 ID 生成
   - ✅ 編輯模式自動載入

### 使用這些頁面

更新 `main.py` 路由指向新版本：
```python
@app.get("/backend/projects")
async def backend_projects():
    return FileResponse(static_dir / "admin" / "projects" / "index-v2.html")

@app.get("/backend/projects/add")
async def backend_projects_add():
    return FileResponse(static_dir / "admin" / "projects" / "add-edit-v2.html")

@app.get("/backend/projects/edit")
async def backend_projects_edit():
    return FileResponse(static_dir / "admin" / "projects" / "add-edit-v2.html")
```

## ✨ 優勢

### 使用 Base Template 的好處:

✅ **代碼重用** - Sidebar/Header 只寫一次  
✅ **一致性** - 所有頁面外觀統一  
✅ **易維護** - 改一個地方，所有頁面都更新  
✅ **快速開發** - 新頁面只需寫內容部分  
✅ **RWD 支持** - Bootstrap 5 響應式  
✅ **jQuery 簡化** - DOM 操作更簡單  
✅ **Toast 通知** - 統一的提示方式  
✅ **Modal 對話** - 統一的確認方式  

### Template Loader 提供的功能:

- `initAdminTemplate()` - 一鍵初始化整個頁面
- `loadAdminSidebar()` - 自動載入導航
- `loadAdminHeader()` - 自動載入頁首
- `showSuccessToast()` - 成功提示
- `showErrorToast()` - 錯誤提示
- `confirmDelete()` - 刪除確認
- `showLoading()` - 載入動畫
- `showError()` - 錯誤訊息

## 📱 RWD Breakpoints

```
< 576px  (xs) - 手機
≥ 576px  (sm) - 大手機
≥ 768px  (md) - 平板
≥ 992px  (lg) - 桌面
≥ 1200px (xl) - 大桌面
≥ 1400px (xxl) - 超大螢幕
```

## 🎯 完整範例

參考已創建的文件：
- `admin/projects/index-v2.html` - 完整的列表頁
- `admin/projects/add-edit-v2.html` - 完整的表單頁

這兩個文件展示了：
- ✅ 如何使用 `initAdminTemplate()`
- ✅ RWD 響應式佈局
- ✅ Bootstrap 5 組件
- ✅ jQuery 操作
- ✅ 圖片上傳
- ✅ Toast 通知
- ✅ Modal 確認

## 🔄 從舊版遷移

**Step 1:** 保留 HTML body 結構
```html
<div class="admin-layout">
    <aside class="sidebar" id="adminSidebar"></aside>
    ...
</div>
```

**Step 2:** 添加 CDN links

**Step 3:** 引入 template-loader.js

**Step 4:** 使用 `initAdminTemplate()` 替代手動初始化

**Step 5:** 使用 jQuery 選擇器和事件

## 🎊 結果

**統一的 base template 系統已完成！**

所有頁面現在都：
- ✅ 共用相同的 Sidebar
- ✅ 共用相同的 Header
- ✅ 使用 Bootstrap 5 組件
- ✅ 支持 RWD 響應式
- ✅ jQuery 簡化操作
- ✅ 統一的 Toast/Modal

**新增頁面只需 3 步：**
1. 複製模板
2. 修改內容部分
3. 呼叫 `initAdminTemplate()`

完成！🚀

