# Routing Change: Hash Router → Browser Router

## Overview 概述

Changed from Hash-based routing (`/#/game`) to Browser History routing (`/game`) for cleaner URLs.

從基於 Hash 的路由（`/#/game`）更改為瀏覽器歷史路由（`/game`），以獲得更清晰的 URL。

## Changes Made 所做的更改

### 1. Updated Router in App.tsx

**Before 之前:**
```typescript
import { HashRouter as Router } from 'react-router-dom';
```

**After 之後:**
```typescript
import { BrowserRouter as Router } from 'react-router-dom';
```

## URL Changes URL 更改

### Before (Hash Router) 之前

```
http://localhost:3000/#/
http://localhost:3000/#/game
http://localhost:3000/#/game/game-123
http://localhost:3000/#/website
http://localhost:3000/#/website/website-456
http://localhost:3000/#/news
http://localhost:3000/#/about
```

### After (Browser Router) 之後

```
http://localhost:3000/
http://localhost:3000/game
http://localhost:3000/game/game-123
http://localhost:3000/website
http://localhost:3000/website/website-456
http://localhost:3000/news
http://localhost:3000/about
```

## Benefits 優點

### 1. Cleaner URLs 更清晰的 URL
- No `#` in URLs
- More professional appearance
- Better for SEO (if needed in future)

### 2. Better User Experience 更好的用戶體驗
- URLs look like traditional web pages
- Easier to share links
- More intuitive for users

### 3. Modern Standard 現代標準
- BrowserRouter is the modern approach
- Better browser history integration
- Works well with analytics

## Development Setup 開發設置

### Vite (Development Server)

Vite automatically handles History API fallback. No additional configuration needed!

**How it works:**
1. User visits `/game`
2. Vite serves `index.html`
3. React Router renders `<GamesPage />`

### Testing 測試

**Start development server:**
```bash
cd frontend
npm run dev
```

**Test URLs:**
```bash
# Open in browser:
http://localhost:5173/
http://localhost:5173/game
http://localhost:5173/game/game-723884
http://localhost:5173/website
http://localhost:5173/news
http://localhost:5173/about
```

**All should work without 404 errors!** ✅

## Production Deployment 生產部署

### Option 1: Separate Frontend Server (Recommended)

Deploy frontend to services like:
- **Vercel** - Zero config needed
- **Netlify** - Automatic SPA handling
- **Cloudflare Pages** - Built-in support

**Example `_redirects` for Netlify:**
```
/* /index.html 200
```

**Example `vercel.json`:**
```json
{
  "rewrites": [
    { "source": "/(.*)", "destination": "/" }
  ]
}
```

### Option 2: Serve from Backend

If serving from FastAPI backend:

**Update `backend/app/main.py`:**

```python
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pathlib import Path

app = FastAPI()

# Mount static files
frontend_dir = Path(__file__).parent / "static" / "frontend"
app.mount("/static", StaticFiles(directory=str(frontend_dir)), name="static")

# API routes
app.include_router(api_router, prefix="/api")

# SPA fallback - MUST be last
@app.get("/{full_path:path}")
async def serve_spa(full_path: str):
    """Serve React app for all non-API routes."""
    # Serve static files if they exist
    file_path = frontend_dir / full_path
    if file_path.is_file():
        return FileResponse(file_path)
    
    # Otherwise serve index.html (SPA)
    return FileResponse(frontend_dir / "index.html")
```

### Option 3: Nginx Reverse Proxy

**nginx.conf:**
```nginx
server {
    listen 80;
    server_name example.com;

    # Frontend
    location / {
        root /var/www/frontend;
        try_files $uri $uri/ /index.html;
    }

    # Backend API
    location /api {
        proxy_pass http://localhost:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

## Build Configuration 構建配置

### Vite Config

No changes needed! Vite already supports BrowserRouter.

**`vite.config.ts`:**
```typescript
export default defineConfig({
  server: {
    port: 3000,
    host: '0.0.0.0',
  },
  plugins: [react()],
  // History API fallback is automatic
});
```

### Build Command

```bash
cd frontend
npm run build
```

Output will be in `dist/` folder.

## Troubleshooting 故障排除

### Issue: 404 on Page Refresh 刷新頁面時 404

**Cause:** Server doesn't have SPA fallback configured.

**Solution (Development):**
- Vite handles this automatically
- Ensure you're using `npm run dev`

**Solution (Production):**
- Configure server to serve `index.html` for all routes
- See "Production Deployment" section above

### Issue: Assets Not Loading 資源未載入

**Check:**
1. Base path in `vite.config.ts`
2. Asset paths in code
3. Browser console for errors

**Fix:**
```typescript
// vite.config.ts
export default defineConfig({
  base: '/', // Ensure base is correct
  // ...
});
```

### Issue: API Calls Failing API 調用失敗

**Check CORS:**
```python
# backend/app/main.py
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

## Migration Checklist 遷移檢查清單

### Development 開發環境

- [x] Changed `HashRouter` to `BrowserRouter`
- [x] Tested all routes work
- [x] No 404 errors on direct URL access
- [x] Navigation works correctly
- [x] Back/forward browser buttons work

### Production 生產環境

- [ ] Configure server for SPA fallback
- [ ] Test build output
- [ ] Deploy to hosting service
- [ ] Test all routes in production
- [ ] Update documentation

## Testing Guide 測試指南

### 1. Test Navigation 測試導航

```
1. Visit: http://localhost:3000/
2. Click "Games" → URL should be /game (no #)
3. Click a game card → URL should be /game/game-123
4. Click back button → Should go back to /game
5. Click "Home" → URL should be /
```

### 2. Test Direct Access 測試直接訪問

```
1. Type in browser: http://localhost:3000/game
2. Press Enter
3. Should show games page (not 404)

4. Type: http://localhost:3000/game/game-123
5. Press Enter
6. Should show game detail page (not 404)
```

### 3. Test Browser Navigation 測試瀏覽器導航

```
1. Visit several pages
2. Click browser back button
3. Click browser forward button
4. Both should work correctly
```

### 4. Test Page Refresh 測試頁面刷新

```
1. Visit any page (e.g., /game)
2. Press F5 or Ctrl+R
3. Page should reload correctly (not 404)
```

## Performance Impact 性能影響

### Positive Effects 積極影響

- **Faster perceived load** - No hash to parse
- **Better caching** - Each route can be cached separately
- **Improved SEO** - Search engines prefer clean URLs

### No Negative Effects 無負面影響

- Performance is equivalent or better
- No additional overhead
- Modern browsers fully support this

## Browser Support 瀏覽器支持

BrowserRouter uses the HTML5 History API, supported by:

- ✅ Chrome (all recent versions)
- ✅ Firefox (all recent versions)
- ✅ Safari (all recent versions)
- ✅ Edge (all recent versions)
- ❌ IE11 (not supported - but IE11 is deprecated)

**Recommendation:** Modern browsers only. IE11 not supported.

## Rollback Plan 回滾計劃

If you need to revert to Hash Router:

```typescript
// frontend/App.tsx
import { HashRouter as Router } from 'react-router-dom';
// Change BrowserRouter back to HashRouter
```

That's it! No other changes needed.

## Additional Notes 附加說明

### Server-Side Rendering (SSR)

If you add SSR in the future (e.g., Next.js), BrowserRouter is required.

### Analytics

Update analytics to track route changes:

```typescript
import { useEffect } from 'react';
import { useLocation } from 'react-router-dom';

function App() {
  const location = useLocation();

  useEffect(() => {
    // Track page view
    gtag('config', 'GA_MEASUREMENT_ID', {
      page_path: location.pathname + location.search,
    });
  }, [location]);

  return <Router>{/* ... */}</Router>;
}
```

### Meta Tags

For better SEO, add dynamic meta tags:

```typescript
import { Helmet } from 'react-helmet';

function GameDetail() {
  return (
    <>
      <Helmet>
        <title>{game.title} | AI-Tracks Studio</title>
        <meta name="description" content={game.description} />
      </Helmet>
      {/* ... */}
    </>
  );
}
```

---

**Date:** 2025-12-04  
**Status:** ✅ Implemented  
**Impact:** Low risk, high benefit  
**Breaking Changes:** None (URLs still work, just cleaner)

