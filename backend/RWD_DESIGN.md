# RWD Responsive Design Guide 響應式設計指南

## 📱 完整的 RWD (Responsive Web Design)

所有管理頁面都採用 Bootstrap 5 的響應式設計，自動適應各種螢幕尺寸。

## 🎯 篩選欄 RWD 佈局

### Breakpoints 斷點設計

```
Mobile (< 768px):    搜尋框全寬，下拉選單各半寬，按鈕全寬
Tablet (≥ 768px):    搜尋框 4/12，下拉選單各 3/12，按鈕自動寬度
Desktop (≥ 992px):   搜尋框 3/12，下拉選單各 2/12，中間彈性空間，按鈕右對齊
```

### 完整的 RWD 篩選欄結構

```html
<div class="row g-3 mb-4 align-items-center">
    <!-- 搜尋框 -->
    <div class="col-12 col-md-4 col-lg-3">
        <input type="text" class="form-control" placeholder="搜尋標題...">
    </div>
    
    <!-- 類別下拉選單 -->
    <div class="col-6 col-md-3 col-lg-2">
        <select class="form-select">
            <option>所有類別</option>
        </select>
    </div>
    
    <!-- 每頁筆數 -->
    <div class="col-6 col-md-3 col-lg-2">
        <select class="form-select">
            <option>10筆/頁</option>
        </select>
    </div>
    
    <!-- 彈性空間 (大螢幕時推開) -->
    <div class="col-0 d-none d-lg-block" style="flex: 1;"></div>
    
    <!-- 新增按鈕 -->
    <div class="col-12 col-md-auto ms-md-auto">
        <a href="/add" class="btn btn-primary w-100">
            <i class="fas fa-plus me-2"></i> 新增
        </a>
    </div>
</div>
```

## 📐 Bootstrap 5 Grid System

### 響應式 Columns

| Class | 螢幕尺寸 | 寬度 | 說明 |
|-------|----------|------|------|
| `col-12` | < 576px | 100% | 手機全寬 |
| `col-sm-6` | ≥ 576px | 50% | 小螢幕半寬 |
| `col-md-4` | ≥ 768px | 33.33% | 平板 1/3 寬 |
| `col-lg-3` | ≥ 992px | 25% | 桌面 1/4 寬 |
| `col-xl-2` | ≥ 1200px | 16.67% | 大螢幕 1/6 寬 |

### 範例：三欄佈局

```html
<div class="row">
    <div class="col-12 col-md-6 col-lg-4">
        <!-- 手機全寬，平板半寬，桌面1/3寬 -->
    </div>
    <div class="col-12 col-md-6 col-lg-4">
        <!-- 同上 -->
    </div>
    <div class="col-12 col-md-12 col-lg-4">
        <!-- 第三欄：手機全寬，平板全寬，桌面1/3寬 -->
    </div>
</div>
```

## 🎨 分散式佈局 (Distributed Layout)

### 方法 1：Flexbox Utilities

```html
<div class="d-flex justify-content-between align-items-center">
    <div>左側</div>
    <div>中間</div>
    <div>右側</div>
</div>
```

### 方法 2：Grid with Auto Margins

```html
<div class="row">
    <div class="col-auto">左側</div>
    <div class="col-auto ms-auto">右側（自動推到右邊）</div>
</div>
```

### 方法 3：Flex with Gaps（我們使用的方式）

```html
<div class="row g-3">
    <div class="col-12 col-md-4">項目1</div>
    <div class="col-6 col-md-3">項目2</div>
    <div class="col-6 col-md-3">項目3</div>
    <div class="col-0 d-none d-lg-block" style="flex: 1;"></div>
    <div class="col-12 col-md-auto ms-md-auto">按鈕</div>
</div>
```

## 📱 RWD 測試

### 手機版 (< 768px)
```
[===== 搜尋框 =====]  (100% 寬)
[== 類別 ==][==筆數==]  (各 50% 寬)
[===== 新增按鈕 =====]  (100% 寬)
```

### 平板版 (768px - 991px)
```
[=== 搜尋 ===][= 類別 =][= 筆數 =][== 新增 ==]
   33%         25%       25%      auto
```

### 桌面版 (≥ 992px)
```
[== 搜尋 ==][類別][筆數].........[新增按鈕]
   25%      16%   16%   彈性空間   auto
```

## 🎯 實際應用範例

**Projects Index 完整 RWD：**

```html
<div class="row g-3 mb-4 align-items-center">
    <!-- 搜尋 -->
    <div class="col-12 col-md-4 col-lg-3">
        <input type="text" class="form-control" placeholder="搜尋標題...">
    </div>
    
    <!-- 類別 -->
    <div class="col-6 col-md-3 col-lg-2">
        <select class="form-select">
            <option>所有類別</option>
            <option>遊戲 (GAME)</option>
            <option>網站 (WEBSITE)</option>
        </select>
    </div>
    
    <!-- 筆數 -->
    <div class="col-6 col-md-3 col-lg-2">
        <select class="form-select">
            <option>10筆/頁</option>
            <option>20筆/頁</option>
        </select>
    </div>
    
    <!-- 彈性空間 (只在大螢幕顯示) -->
    <div class="col-0 d-none d-lg-block" style="flex: 1;"></div>
    
    <!-- 新增按鈕 -->
    <div class="col-12 col-md-auto ms-md-auto">
        <a href="/add" class="btn btn-primary w-100">
            <i class="fas fa-plus me-2"></i> 新增 Project
        </a>
    </div>
</div>
```

## 🔧 Bootstrap 5 RWD Classes

### Display 顯示控制
```html
<div class="d-none d-md-block">   <!-- 手機隱藏，平板以上顯示 -->
<div class="d-block d-md-none">   <!-- 手機顯示，平板以上隱藏 -->
<div class="d-none d-lg-block">   <!-- 桌面才顯示 -->
```

### Flex 佈局
```html
<div class="d-flex justify-content-between">   <!-- 兩端對齊 -->
<div class="d-flex justify-content-around">    <!-- 分散對齊 -->
<div class="d-flex justify-content-evenly">    <!-- 均分對齊 -->
<div class="d-flex gap-3">                     <!-- 間距 1rem -->
```

### Width 寬度
```html
<div class="w-100">    <!-- 100% 寬 -->
<div class="w-75">     <!-- 75% 寬 -->
<div class="w-auto">   <!-- 自動寬度 -->
```

### Margins 邊距
```html
<div class="ms-auto">   <!-- margin-start: auto (推到右邊) -->
<div class="me-auto">   <!-- margin-end: auto (推到左邊) -->
<div class="mx-auto">   <!-- 水平置中 -->
```

## 📊 表格 RWD

### 響應式表格
```html
<div class="table-responsive">
    <table class="table table-hover">
        <!-- 自動橫向滾動 -->
    </table>
</div>
```

### 手機版優化
```html
<table class="table table-sm">  <!-- 緊湊模式 -->
    <thead class="d-none d-md-table-header-group">  <!-- 手機隱藏表頭 -->
    <!-- 或使用 card 佈局替代表格 -->
</table>
```

## 🎨 Spacing System 間距系統

Bootstrap 5 使用 `0-5` 和 `auto` 的間距級別：

```
0 = 0
1 = 0.25rem (4px)
2 = 0.5rem (8px)
3 = 1rem (16px)
4 = 1.5rem (24px)
5 = 3rem (48px)
```

**範例：**
```html
<div class="p-3">      <!-- padding: 1rem -->
<div class="mt-4">     <!-- margin-top: 1.5rem -->
<div class="mb-2">     <!-- margin-bottom: 0.5rem -->
<div class="g-3">      <!-- gap: 1rem (用於 grid) -->
```

## 🖥️ 實際佈局效果

### 桌面 (≥ 992px)
```
┌─────────────────────────────────────────────────────┐
│ [搜尋框 25%] [類別 16%] [筆數 16%] ........ [新增按鈕] │
└─────────────────────────────────────────────────────┘
```

### 平板 (768px - 991px)
```
┌─────────────────────────────────────────┐
│ [搜尋框 33%] [類別 25%] [筆數 25%]      │
│                            [新增按鈕]    │
└─────────────────────────────────────────┘
```

### 手機 (< 768px)
```
┌──────────────────┐
│ [搜尋框 100%]    │
│ [類別 50%][筆數 50%] │
│ [新增按鈕 100%]  │
└──────────────────┘
```

## ✅ RWD Checklist

- ✅ 使用 Bootstrap Grid System (`row`, `col-*`)
- ✅ 響應式斷點 (`col-12`, `col-md-4`, `col-lg-3`)
- ✅ Flexbox utilities (`d-flex`, `justify-content-*`)
- ✅ 間距系統 (`g-3`, `mb-4`, `ms-auto`)
- ✅ 顯示控制 (`d-none`, `d-md-block`)
- ✅ 寬度控制 (`w-100`, `w-auto`)
- ✅ 響應式表格 (`table-responsive`)
- ✅ 自適應按鈕 (`w-100` on mobile, `w-auto` on desktop)

## 🎯 完整範例

參考 `admin/projects/index-bootstrap.html`:
- ✅ 完整的 RWD 篩選欄
- ✅ Bootstrap 5 組件
- ✅ jQuery 事件處理
- ✅ 響應式表格
- ✅ 分散式佈局

## 💡 Best Practices 最佳實踐

1. **Mobile First** - 先設計手機版 (`col-12`)
2. **Progressive Enhancement** - 逐步增強到大螢幕 (`col-md-*`, `col-lg-*`)
3. **Use Grid** - 優先使用 Grid System 而非固定寬度
4. **Flex Utilities** - 使用 `d-flex` 處理對齊
5. **Test Multiple Sizes** - 測試所有斷點

## 🧪 測試 RWD

### Chrome DevTools
1. 按 F12 開啟開發者工具
2. 點擊 Toggle Device Toolbar (Ctrl+Shift+M)
3. 選擇不同裝置測試：
   - iPhone SE (375px)
   - iPad (768px)
   - iPad Pro (1024px)
   - Desktop (1920px)

### 測試項目
- ✅ 搜尋框在各尺寸下的寬度
- ✅ 下拉選單是否正確排列
- ✅ 按鈕在手機上是否全寬
- ✅ 表格是否可橫向滾動
- ✅ 側邊欄在手機上是否適當

## 📊 實際效果

**手機版 (375px):**
- 搜尋框：100% 寬度
- 類別/筆數：各 50% 寬度，並排
- 新增按鈕：100% 寬度

**平板版 (768px):**
- 搜尋框：33.33% 寬度
- 類別：25% 寬度
- 筆數：25% 寬度
- 新增按鈕：自動寬度，右對齊

**桌面版 (1200px):**
- 搜尋框：25% 寬度
- 類別：16.67% 寬度
- 筆數：16.67% 寬度
- 中間：彈性空間（填充剩餘空間）
- 新增按鈕：自動寬度，完全靠右

## ✨ 關鍵 CSS Classes

**Row & Columns:**
- `row` - 建立網格行
- `g-3` - gutter (間距) = 1rem
- `col-12` - 全寬 (mobile)
- `col-md-4` - 平板 33.33%
- `col-lg-3` - 桌面 25%
- `col-auto` - 自動寬度

**Flex Utilities:**
- `d-flex` - 啟用 flexbox
- `justify-content-between` - 兩端對齊
- `align-items-center` - 垂直置中
- `flex-wrap` - 允許換行
- `gap-3` - 間距 1rem

**Spacing:**
- `mb-4` - margin-bottom: 1.5rem
- `ms-md-auto` - 平板以上 margin-start: auto
- `w-100` - width: 100%

**Display:**
- `d-none` - 隱藏
- `d-md-block` - 平板以上顯示
- `d-lg-flex` - 桌面以上使用 flex

## 🎯 完整系統 RWD

所有頁面都已實現 RWD：
- ✅ Login 頁面 - 居中響應式卡片
- ✅ Projects 列表 - 響應式篩選欄和表格
- ✅ News 列表 - 響應式佈局
- ✅ About 列表 - 響應式佈局
- ✅ Add/Edit 表單 - 全寬響應式表單
- ✅ Sidebar - 固定式/可摺疊 (可擴展)

## 💻 瀏覽器支持

Bootstrap 5 支持：
- ✅ Chrome (最新版)
- ✅ Firefox (最新版)
- ✅ Safari (最新版)
- ✅ Edge (最新版)
- ✅ Mobile browsers (iOS Safari, Chrome Mobile)

不支持 IE11（Bootstrap 5 已放棄支持）

---

**完整的 RWD 響應式設計已實現！** 📱💻🖥️  
所有頁面都能完美適應各種螢幕尺寸！

