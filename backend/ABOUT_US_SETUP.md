# About Us Setup 關於我們設置

## Problem 問題

Frontend showed error: **"About Us content not found"**

前端顯示錯誤：「找不到關於我們的內容」

## Cause 原因

The `about_us` table in the database was empty. When the frontend called `/api/about`, the backend returned a 404 error because no About Us content existed.

數據庫中的 `about_us` 表是空的。當前端調用 `/api/about` 時，後端返回 404 錯誤，因為不存在關於我們的內容。

## Solution 解決方案

### 1. Created Seed Data Script 創建種子數據腳本

**File:** `backend/seed_about.sql`

This script inserts default About Us content:
- Title: "AI-Tracks Studio"
- Subtitle: "Innovative Web & Game Experiences Powered by AI"
- Description: Full Markdown content with sections:
  - Who We Are
  - Our Mission
  - What We Do
  - Our Approach
  - Get In Touch
- Contact Email: contact@ai-tracks.studio

### 2. Executed Seed Script 執行種子腳本

```bash
cd backend
mysql -u root studio < seed_about.sql
```

### 3. Verified API Response 驗證 API 響應

```bash
curl http://localhost:8000/api/about
```

**Result:** ✅ Returns complete About Us data

## How to Use 使用方法

### For Fresh Database 對於新數據庫

If you're setting up a fresh database:

```bash
cd backend

# Run migrations (creates tables)
uv run python run.py

# Seed About Us content
mysql -u root studio < seed_about.sql
```

### For Existing Database 對於現有數據庫

If you already have the tables but no About Us content:

```bash
cd backend
mysql -u root studio < seed_about.sql
```

### Via Backend Admin 通過後台管理

You can also add/edit About Us content via the admin panel:

```
1. Visit: http://localhost:8000/backend
2. Login: admin@admin.com / admin123
3. Navigate to: 關於我們
4. Click: 新增內容
5. Fill in the form
6. Click: 儲存
```

## Database Structure 數據庫結構

### about_us Table

```sql
CREATE TABLE about_us (
    id INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(255),
    subtitle LONGTEXT,
    description LONGTEXT,
    image VARCHAR(500),
    contact_email VARCHAR(255),
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);
```

### Field Descriptions 字段描述

| Field | Type | Description |
|-------|------|-------------|
| `id` | INT | Primary key, auto-increment |
| `title` | VARCHAR(255) | Company/Studio name |
| `subtitle` | LONGTEXT | Tagline or mission statement |
| `description` | LONGTEXT | Full content (supports Markdown) |
| `image` | VARCHAR(500) | Optional hero image filename |
| `contact_email` | VARCHAR(255) | Contact email address |
| `created_at` | DATETIME | Timestamp when created |
| `updated_at` | DATETIME | Timestamp when last updated |

## API Endpoints API 端點

### Get About Us Content

**Endpoint:** `GET /api/about`

**Response:**
```json
{
    "id": 1,
    "title": "AI-Tracks Studio",
    "subtitle": "Innovative Web & Game Experiences Powered by AI",
    "description": "## Who We Are\n\nAI-Tracks Studio...",
    "image": null,
    "contact_email": "contact@ai-tracks.studio",
    "created_at": "2025-12-04T12:13:12",
    "updated_at": "2025-12-04T12:13:12"
}
```

**Note:** Returns the first (and typically only) About Us entry.

### Admin Endpoints

- `GET /api/admin/about` - List all about entries
- `GET /api/admin/about/{id}` - Get specific entry
- `POST /api/admin/about` - Create new entry
- `PUT /api/admin/about/{id}` - Update entry
- `DELETE /api/admin/about/{id}` - Delete entry

## Frontend Integration 前端整合

### Usage in AboutPage

```typescript
import { aboutApi } from './api';

const AboutPage = () => {
  const [about, setAbout] = useState<AboutUs | null>(null);

  useEffect(() => {
    const fetchAbout = async () => {
      try {
        const data = await aboutApi.getAbout();
        setAbout(data);
      } catch (error) {
        console.error('Failed to load about:', error);
      }
    };
    fetchAbout();
  }, []);

  return (
    <div>
      <h1>{about?.title}</h1>
      <p>{about?.subtitle}</p>
      <div>{about?.description}</div>
    </div>
  );
};
```

## Customization 自定義

### Update Content via SQL

```sql
UPDATE about_us 
SET 
    title = 'Your Studio Name',
    subtitle = 'Your tagline',
    description = 'Your content...',
    contact_email = 'your@email.com'
WHERE id = 1;
```

### Add Image

```sql
UPDATE about_us 
SET image = '20251204-abc123.webp'
WHERE id = 1;
```

### Via Admin Panel

The easiest way is through the admin interface:

1. Login to backend admin
2. Go to "關於我們" (About Us)
3. Click edit button on existing entry
4. Update content
5. Upload image if needed
6. Save

## Markdown Support Markdown 支持

The `description` field supports full Markdown:

```markdown
## Section Title

Regular paragraph text.

- Bullet point 1
- Bullet point 2

**Bold text** and *italic text*

[Links](https://example.com)

> Blockquotes

\`\`\`
Code blocks
\`\`\`
```

## Best Practices 最佳實踐

### 1. Keep One Entry 保持一個條目

Typically, you should have only one About Us entry:
- The API returns the first entry
- Multiple entries can cause confusion
- Update existing entry rather than creating new ones

### 2. Use Markdown for Structure 使用 Markdown 結構

Structure your content with Markdown for:
- Better readability
- Consistent formatting
- Easy updates

### 3. Test After Changes 更改後測試

After updating content:

```bash
# Test API
curl http://localhost:8000/api/about

# Check frontend
# Visit: http://localhost:3000/about
```

### 4. Backup Before Major Changes 重大更改前備份

```bash
mysqldump -u root studio about_us > about_us_backup.sql
```

## Troubleshooting 故障排除

### Issue: Still Getting "Not Found" Error

**Check database:**
```bash
mysql -u root studio -e "SELECT COUNT(*) FROM about_us;"
```

**Should show at least 1 row.**

If empty:
```bash
cd backend
mysql -u root studio < seed_about.sql
```

### Issue: Content Not Updating

**Clear any caching:**
1. Restart backend: `Ctrl+C` then restart
2. Hard refresh frontend: `Ctrl+Shift+R`
3. Check database directly:
```bash
mysql -u root studio -e "SELECT * FROM about_us;"
```

### Issue: API Returns Wrong Data

**Verify API endpoint:**
```bash
curl -v http://localhost:8000/api/about
```

**Check response:**
- Status should be 200 (not 404)
- Content-Type should be application/json
- Body should contain about data

### Issue: Frontend Still Shows Error

**Check browser console:**
1. Open DevTools (F12)
2. Look for API errors
3. Check Network tab for failed requests

**Common causes:**
- Backend not running
- Wrong API URL in frontend config
- CORS issues
- Network errors

## Files Created 創建的文件

- ✅ `backend/seed_about.sql` - SQL script to seed data
- ✅ `backend/ABOUT_US_SETUP.md` - This documentation

## Quick Commands 快速命令

```bash
# Seed About Us data
cd backend && mysql -u root studio < seed_about.sql

# Check data exists
mysql -u root studio -e "SELECT id, title FROM about_us;"

# Test API
curl http://localhost:8000/api/about

# View in admin
# Visit: http://localhost:8000/backend → 關於我們
```

---

**Created:** 2025-12-04  
**Status:** ✅ Resolved  
**Issue:** About Us content not found  
**Solution:** Added seed data script

