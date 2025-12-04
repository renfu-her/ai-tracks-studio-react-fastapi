# Add-Edit Architecture 新增編輯架構

## Overview 概述

All admin modules (Projects, News, About) use a unified `add-edit.html` file that handles both create and edit operations.

所有管理模組（專案、消息、關於我們）都使用統一的 `add-edit.html` 文件來處理新增和編輯操作。

## File Structure 文件結構

```
backend/app/static/admin/
├── projects/
│   ├── list.html          # 列表頁面
│   └── add-edit.html      # 新增/編輯表單（統一）
├── news/
│   ├── list.html
│   └── add-edit.html
└── about/
    ├── list.html
    └── add-edit.html
```

## URL Routing 路由規則

### Pattern 模式

**Create Mode 新增模式:**
```
#projects/add
#news/add
#about/add
```
→ Loads `add-edit.html` with empty form

**Edit Mode 編輯模式:**
```
#projects/edit/game-123
#news/edit/news-456
#about/edit/789
```
→ Loads `add-edit.html` with existing data

### Routing Logic 路由邏輯

In `admin.html`:

```javascript
async function loadPage() {
    const hash = window.location.hash.slice(1) || 'projects/list';
    const [module, action = 'list', id] = hash.split('/');

    // Map add and edit actions to add-edit.html
    let actualAction = action;
    if (action === 'add' || action === 'edit') {
        actualAction = 'add-edit';
    }

    const contentPath = `/static/admin/${module}/${actualAction}.html`;
    // ... load content
}
```

## Form Behavior 表單行為

### Mode Detection 模式檢測

Each `add-edit.html` detects edit mode by checking the URL:

```javascript
// In projects/add-edit.html
const hash = window.location.hash;
const match = hash.match(/#projects\/edit\/(.+)/);
if (match) {
    isEditMode = true;
    editingId = match[1];
    $('#formTitle').text('編輯專案');
    $('#pageHeader').text('編輯專案');
    await loadProject(editingId);
}
// Otherwise: create mode (isEditMode = false)
```

### Title Updates 標題更新

| Mode 模式 | URL | Form Title | Page Header |
|-----------|-----|------------|-------------|
| Create | `#projects/add` | 新增專案 | 專案管理 |
| Edit | `#projects/edit/ID` | 編輯專案 | 專案管理 |
| Create | `#news/add` | 新增消息 | 最新消息 |
| Edit | `#news/edit/ID` | 編輯消息 | 最新消息 |
| Create | `#about/add` | 新增內容 | 關於我們 |
| Edit | `#about/edit/ID` | 編輯內容 | 關於我們 |

## API Calls API 調用

### Create Mode 新增模式

```javascript
await apiRequest('/api/admin/projects', {
    method: 'POST',
    body: JSON.stringify(data)
});
```

### Edit Mode 編輯模式

```javascript
await apiRequest(`/api/admin/projects/${editingId}`, {
    method: 'PUT',
    body: JSON.stringify(data)
});
```

## Benefits 優點

### 1. Single Source of Truth 單一真實來源
- One file per module for form logic
- No code duplication
- Easier to maintain

### 2. Clean URLs 清晰的 URL
- `/add` for create - clear intent
- `/edit/ID` for edit - clear intent
- No confusing redirects

### 3. Consistent Behavior 一致的行為
- All modules work the same way
- Easy to understand
- Predictable routing

### 4. Easy to Extend 易於擴展
- Add new modules by following the same pattern
- Copy any `add-edit.html` as template
- Update routing in `admin.html`

## Code Example 代碼示例

### Navigation Links 導航連結

In `list.html`:

```html
<!-- Create button -->
<a href="#projects/add" class="btn btn-primary">
    <i class="fas fa-plus me-2"></i> 新增專案
</a>

<!-- Edit button in table -->
<a href="#projects/edit/${project.id}" class="btn btn-sm btn-outline-primary">
    <i class="fas fa-edit"></i>
</a>
```

### Form Submission 表單提交

In `add-edit.html`:

```javascript
$('#projectForm').submit(async function(e) {
    e.preventDefault();
    
    const data = {
        id: projectId,
        title: $('#projectTitle').val(),
        // ... other fields
    };

    try {
        if (isEditMode) {
            // Update existing
            await apiRequest(`/api/admin/projects/${editingId}`, {
                method: 'PUT',
                body: JSON.stringify(data)
            });
            showSuccessToast('更新成功！');
        } else {
            // Create new
            await apiRequest('/api/admin/projects', {
                method: 'POST',
                body: JSON.stringify(data)
            });
            showSuccessToast('新增成功！');
        }

        setTimeout(() => window.location.hash = 'projects/list', 1000);
    } catch (error) {
        showErrorToast('儲存失敗: ' + error.message);
    }
});
```

## Testing Checklist 測試清單

### Projects 專案管理
- [ ] `#projects/add` → Shows "新增專案" form
- [ ] `#projects/edit/game-123` → Shows "編輯專案" with data
- [ ] Create: Saves new project
- [ ] Edit: Updates existing project

### News 最新消息
- [ ] `#news/add` → Shows "新增消息" form
- [ ] `#news/edit/news-456` → Shows "編輯消息" with data
- [ ] Create: Saves new news
- [ ] Edit: Updates existing news

### About 關於我們
- [ ] `#about/add` → Shows "新增內容" form
- [ ] `#about/edit/789` → Shows "編輯內容" with data
- [ ] Create: Saves new about
- [ ] Edit: Updates existing about

## Migration Notes 遷移說明

### From Previous Architecture 從之前的架構

**Before 之前:**
- Separate `add.html` and `edit.html` files
- `edit.html` redirected to `add.html` with ID
- Confusing URL patterns

**Now 現在:**
- Single `add-edit.html` per module
- Clean routing logic
- No redirects needed

**Files Renamed 重命名的文件:**
- `projects/add.html` → `projects/add-edit.html`
- `news/add.html` → `news/add-edit.html`
- `about/add.html` → `about/add-edit.html`

**Files Deleted 刪除的文件:**
- `projects/edit.html` ❌
- `news/edit.html` ❌
- `about/edit.html` ❌

## Future Enhancements 未來改進

### Potential Improvements 可能的改進

1. **URL State Preservation 保留 URL 狀態**
   - Preserve scroll position when returning to list
   - Remember filters/pagination

2. **Unsaved Changes Warning 未保存警告**
   - Alert user before leaving with unsaved changes

3. **Auto-save Draft 自動保存草稿**
   - Save form state to localStorage
   - Restore on page reload

4. **Duplicate Feature 複製功能**
   - Add "Duplicate" button to create copy of existing item
   - URL: `#projects/duplicate/ID`

## Support 支持

If you encounter any issues with the add-edit architecture:

1. Check browser console for JavaScript errors
2. Verify URL format matches expected pattern
3. Clear browser cache and hard refresh
4. Check that `add-edit.html` exists for the module
5. Verify routing logic in `admin.html`

---

**Last Updated:** 2025-12-04  
**Version:** 1.0  
**Architecture:** SPA with Hash-based Routing

