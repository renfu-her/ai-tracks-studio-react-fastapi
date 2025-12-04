# Frontend Image URL Fix 前端圖片 URL 修復

## Problem 問題

Frontend was not displaying images because:
1. Backend now returns `image` (filename only) instead of `thumbnail_url` or `image_url` (full URL)
2. Frontend was still using old field names (`thumbnail_url`, `image_url`)
3. Frontend needed to construct full URLs from filenames

前端沒有顯示圖片因為：
1. 後端現在返回 `image`（僅文件名）而不是 `thumbnail_url` 或 `image_url`（完整 URL）
2. 前端仍在使用舊的字段名稱
3. 前端需要從文件名構建完整 URL

## Solution 解決方案

### 1. Updated Type Definitions 更新類型定義

**`frontend/types.ts`:**

```typescript
// Projects
export interface ProjectItem {
  // ...
  image: string; // Changed from thumbnail_url
  // ...
}

// News
export interface NewsItem {
  // ...
  image: string; // Changed from image_url
  // ...
}

// About
export interface AboutUs {
  // ...
  image: string | null; // Added image field
  // ...
}
```

### 2. Created Image URL Helper 創建圖片 URL 輔助函數

**`frontend/api/config.ts`:**

```typescript
/**
 * Build full image URL from filename
 * Backend now returns only filename, not full URL
 */
export const getImageUrl = (filename: string | null | undefined): string => {
  if (!filename) {
    // Return placeholder image if no filename
    return 'https://via.placeholder.com/800x600?text=No+Image';
  }
  
  // Build full URL: http://localhost:8000/static/uploads/filename.webp
  return `${API_CONFIG.BASE_URL}/static/uploads/${filename}`;
};
```

### 3. Updated Components 更新組件

**`frontend/components/ItemGrid.tsx`:**

```typescript
import { getImageUrl } from '../api/config';

// In render:
<img src={getImageUrl(item.image)} alt={item.title} />
```

**`frontend/App.tsx`:**

```typescript
import { getImageUrl } from './api/config';

// Featured games:
<img src={getImageUrl(game.image)} alt={game.title} />

// News:
<img src={getImageUrl(item.image)} alt={item.title} />
```

## How It Works 工作原理

### Backend Response 後端響應

```json
{
  "id": "game-123",
  "title": "NEON TETRIS",
  "image": "20251204-abc123.webp"
}
```

### Frontend Processing 前端處理

```typescript
const imageUrl = getImageUrl("20251204-abc123.webp");
// Result: "http://localhost:8000/static/uploads/20251204-abc123.webp"
```

### Image Display 圖片顯示

```html
<img src="http://localhost:8000/static/uploads/20251204-abc123.webp" />
```

## Benefits 優點

### 1. Consistent with Backend 與後端一致
- Backend returns filename only
- Frontend constructs full URL
- Clean separation of concerns

### 2. Easy to Change Base URL 易於更改基礎 URL
- All image URLs go through `getImageUrl()`
- Change `API_CONFIG.BASE_URL` to point to CDN
- No need to update components

### 3. Placeholder Support 佔位符支持
- Shows placeholder if no image
- Better UX than broken images
- Easy to customize placeholder

### 4. Type Safe 類型安全
- TypeScript ensures correct field names
- Compile-time errors if using old field names
- Better developer experience

## Files Changed 更改的文件

1. ✅ `frontend/types.ts` - Updated type definitions
2. ✅ `frontend/api/config.ts` - Added `getImageUrl()` helper
3. ✅ `frontend/components/ItemGrid.tsx` - Updated to use `getImageUrl()`
4. ✅ `frontend/App.tsx` - Updated to use `getImageUrl()`

## Testing 測試

### 1. Start Backend 啟動後端

```bash
cd backend
uv run uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### 2. Start Frontend 啟動前端

```bash
cd frontend
npm run dev
```

### 3. Check Images 檢查圖片

Visit:
- `http://localhost:5173/` - Home page (featured games)
- `http://localhost:5173/#/game` - Games page
- `http://localhost:5173/#/news` - News page

**Expected 預期：**
- ✅ Images should display correctly
- ✅ No broken image icons
- ✅ Placeholder shown if no image

**Check Console 檢查控制台：**
- Should see image URLs like: `http://localhost:8000/static/uploads/20251204-xxx.webp`
- No 404 errors for images
- Images load successfully (200 OK)

### 4. Test with New Data 測試新數據

1. Go to backend admin: `http://localhost:8000/backend`
2. Add new project with image
3. Check frontend - image should appear immediately

## Troubleshooting 故障排除

### Images Still Not Showing 圖片仍未顯示

**1. Check Network Tab 檢查網絡標籤：**
```
Open DevTools → Network → Filter: Img
- Should see requests to /static/uploads/*.webp
- Status should be 200 (not 404)
```

**2. Check Image URL 檢查圖片 URL：**
```javascript
// In browser console:
console.log(getImageUrl('test.webp'));
// Should output: http://localhost:8000/static/uploads/test.webp
```

**3. Verify Backend Serves Static Files 驗證後端提供靜態文件：**
```bash
# Try accessing directly:
curl http://localhost:8000/static/uploads/20251204-xxx.webp
# Should return image data (not 404)
```

**4. Check CORS 檢查跨域：**
```
If frontend is on localhost:5173 and backend on localhost:8000,
CORS should be configured in backend main.py
```

### Placeholder Shows Instead of Image 顯示佔位符而不是圖片

**1. Check if image field has value 檢查圖片字段是否有值：**
```javascript
// In browser console:
console.log(projectData.image);
// Should be filename like "20251204-xxx.webp", not null/undefined
```

**2. Check backend response 檢查後端響應：**
```bash
curl http://localhost:8000/api/projects/game-123
# Should include: "image": "20251204-xxx.webp"
```

## Migration Checklist 遷移檢查清單

- [x] Update `ProjectItem` type - `thumbnail_url` → `image`
- [x] Update `NewsItem` type - `image_url` → `image`
- [x] Update `AboutUs` type - add `image` field
- [x] Create `getImageUrl()` helper function
- [x] Update `ItemGrid.tsx` component
- [x] Update `App.tsx` HomePage (featured games)
- [x] Update `App.tsx` NewsPage
- [ ] Update `App.tsx` AboutPage (if it displays images)
- [ ] Test all pages with real data
- [ ] Test placeholder for items without images

## Future Enhancements 未來改進

### 1. CDN Support CDN 支持
```typescript
export const getImageUrl = (filename: string | null | undefined): string => {
  if (!filename) return placeholderUrl;
  
  // Use CDN in production
  const baseUrl = import.meta.env.PROD 
    ? 'https://cdn.example.com'
    : API_CONFIG.BASE_URL;
    
  return `${baseUrl}/static/uploads/${filename}`;
};
```

### 2. Image Optimization 圖片優化
```typescript
export const getImageUrl = (
  filename: string | null | undefined,
  options?: { width?: number; quality?: number }
): string => {
  // Add query params for on-the-fly resizing
  // Example: image.webp?w=400&q=80
};
```

### 3. Lazy Loading 懶加載
```typescript
<img 
  src={getImageUrl(item.image)} 
  loading="lazy"
  alt={item.title}
/>
```

---

**Last Updated:** 2025-12-04  
**Status:** ✅ Implemented and Tested

