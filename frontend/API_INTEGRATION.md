# Frontend API Integration Guide

## Overview 總覽

The frontend is now fully integrated with the FastAPI backend. All data is fetched dynamically from the API instead of using hardcoded constants.

## Architecture 架構

```
frontend/
├── api/                    # API Layer
│   ├── config.ts          # API configuration
│   ├── client.ts          # HTTP client
│   ├── projects.ts        # Projects API
│   ├── news.ts            # News API
│   ├── about.ts           # About Us API
│   └── index.ts           # Exports
├── components/            # React components
├── App.tsx               # Main app with API calls
├── types.ts              # TypeScript interfaces
└── constants.ts          # Static constants (HERO_IMAGES)
```

## Routes 路由

| Route      | API Endpoint                    | Description                    |
|------------|---------------------------------|--------------------------------|
| `/`        | `/api/projects?category=GAME`   | Home (featured games)          |
| `/game`    | `/api/projects?category=GAME`   | All games                      |
| `/website` | `/api/projects?category=WEBSITE`| All websites                   |
| `/news`    | `/api/news`                     | News articles                  |
| `/about`   | `/api/about`                    | About Us content               |

## Configuration 配置

### Environment Variables

Create `.env` file in frontend directory:

```env
VITE_API_BASE_URL=http://localhost:8000
```

### API Settings

Located in `api/config.ts`:
- **BASE_URL**: `http://localhost:8000` (default)
- **API_PREFIX**: `/api`
- **TIMEOUT**: 30000ms (30 seconds)

## API Services API 服務

### Projects API

```typescript
import { projectsApi } from './api';

// Get all projects
const response = await projectsApi.getProjects();

// Get games only
const games = await projectsApi.getGames();

// Get websites only
const websites = await projectsApi.getWebsites();

// Get single project
const project = await projectsApi.getProject('game-1');
```

### News API

```typescript
import { newsApi } from './api';

// Get all news
const response = await newsApi.getNews();

// Get single news article
const article = await newsApi.getNewsItem('news-1');
```

### About Us API

```typescript
import { aboutApi } from './api';

// Get current about content
const about = await aboutApi.getAbout();

// Get by ID
const about = await aboutApi.getAboutById(1);
```

## Component Pattern 組件模式

### Standard Data Fetching Pattern

```typescript
const ExamplePage: React.FC = () => {
  const [data, setData] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const fetchData = async () => {
    setLoading(true);
    setError(null);
    try {
      const response = await someApi.getData();
      setData(response.items);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to load');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchData();
  }, []);

  if (loading) return <LoadingSpinner />;
  if (error) return <ErrorMessage message={error} onRetry={fetchData} />;
  if (data.length === 0) return <EmptyState />;
  
  return <div>{/* Render data */}</div>;
};
```

## UI Components UI 組件

### LoadingSpinner

```typescript
<LoadingSpinner message="Loading games..." />
```

Shows animated spinner with optional message.

### ErrorMessage

```typescript
<ErrorMessage 
  message="Failed to load data" 
  onRetry={() => refetchData()}
/>
```

Shows error with retry button.

## Error Handling 錯誤處理

The API client handles various error scenarios:

1. **Network Errors**: Connection refused, timeout
2. **HTTP Errors**: 404, 500, etc.
3. **Timeout**: Request exceeds 30 seconds
4. **Parsing Errors**: Invalid JSON response

Example error handling:

```typescript
try {
  const data = await projectsApi.getGames();
} catch (error) {
  if (error instanceof ApiError) {
    console.error('API Error:', error.message, error.status);
  }
}
```

## Type Safety 類型安全

All API responses are typed:

```typescript
interface ProjectItem {
  id: string;
  title: string;
  description: string;
  thumbnail_url: string;
  category: Category;
  date: string;
  tags: string[];
  link?: string;
  created_at: string;
  updated_at: string;
}

interface ProjectListResponse {
  total: number;
  items: ProjectItem[];
}
```

## Development Setup 開發設定

### 1. Start Backend

```bash
cd backend
uv run python run.py
```

Backend runs on: http://localhost:8000

### 2. Start Frontend

```bash
cd frontend
pnpm install  # First time only
pnpm dev
```

Frontend runs on: http://localhost:5173

### 3. Test API Connection

Open browser console and check for:
- No CORS errors
- Successful API calls
- Data loading properly

## Testing 測試

### Manual Testing

1. **Home Page**: Should show 3 featured games from API
2. **Games Page** (`/game`): Should load all games
3. **Websites Page** (`/website`): Should load all websites
4. **News Page**: Should display news articles
5. **About Page**: Should show about content

### Check Loading States

1. Open browser DevTools → Network tab
2. Throttle connection to "Slow 3G"
3. Refresh page
4. Should see loading spinner

### Check Error Handling

1. Stop backend server
2. Refresh frontend
3. Should see error message with retry button
4. Start backend
5. Click retry
6. Should load data successfully

## Common Issues 常見問題

### CORS Errors

**Problem**: `Access-Control-Allow-Origin` error

**Solution**: 
- Ensure backend CORS is configured for `http://localhost:5173`
- Check `backend/app/config.py` for CORS_ORIGINS setting

### API Not Found

**Problem**: 404 errors on API calls

**Solution**:
- Verify backend is running on port 8000
- Check API_BASE_URL in frontend config
- Verify database has data

### Empty Data

**Problem**: Pages show "No data available"

**Solution**:
- Check backend database has records
- Use Swagger UI to verify API works: http://localhost:8000/docs
- Check browser console for errors

## Production Deployment 生產部署

### Environment Variables

Set production API URL:

```env
VITE_API_BASE_URL=https://api.yourdomain.com
```

### Build Frontend

```bash
pnpm build
```

Outputs to `dist/` directory.

### Serve Static Files

Use any static file server or integrate with backend:

```bash
# Example with simple HTTP server
npx serve dist -p 3000
```

## API Response Examples API 響應範例

### Projects List

```json
{
  "total": 12,
  "items": [
    {
      "id": "game-1",
      "title": "Super Adventure",
      "description": "An exciting game...",
      "thumbnail_url": "https://example.com/image.jpg",
      "category": "GAME",
      "date": "2024-01-15",
      "tags": ["action", "adventure"],
      "link": null,
      "created_at": "2024-01-01T00:00:00",
      "updated_at": "2024-01-01T00:00:00"
    }
  ]
}
```

### News List

```json
{
  "total": 4,
  "items": [
    {
      "id": "news-1",
      "title": "AI-Tracks Studio Launches",
      "excerpt": "We are proud to announce...",
      "content": "Full content...",
      "date": "2024-05-20",
      "image_url": "https://example.com/news.jpg",
      "author": "Renfu Her",
      "created_at": "2024-05-20T00:00:00",
      "updated_at": "2024-05-20T00:00:00"
    }
  ]
}
```

### About Us

```json
{
  "id": 1,
  "title": "About Us",
  "subtitle": "We are a passionate team...",
  "description": "AI-Tracks Studio is...",
  "values": [
    {
      "icon": "Star",
      "title": "Creativity First",
      "description": "We believe in lively designs..."
    }
  ],
  "contact_email": "renfu.her@gmail.com",
  "created_at": "2024-01-01T00:00:00",
  "updated_at": "2024-01-01T00:00:00"
}
```

## Next Steps 下一步

1. ✅ Test all pages with real API data
2. ✅ Add loading states where needed
3. ✅ Implement error retry logic
4. ✅ Test with slow network
5. ✅ Configure production API URL
6. ✅ Deploy frontend and backend

## Support 支援

For issues:
- Check backend logs
- Check browser console
- Verify API with Swagger UI: http://localhost:8000/docs
- Review network tab in DevTools

---

**Integration complete!** 🎉 Frontend is now fully connected to the backend API.

