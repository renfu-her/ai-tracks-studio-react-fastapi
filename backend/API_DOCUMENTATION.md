# API Documentation

## Base URL
```
http://localhost:8000
```

## API Prefix
All API endpoints are prefixed with `/api`

---

## Projects API

Manage games and website projects.

### List Projects
```http
GET /api/projects
```

**Query Parameters:**
- `category` (optional): Filter by category (`GAME` or `WEBSITE`)
- `skip` (optional, default: 0): Number of items to skip
- `limit` (optional, default: 100, max: 100): Number of items to return

**Response:**
```json
{
  "total": 12,
  "items": [
    {
      "id": "game-1",
      "title": "Super Adventure",
      "description": "An exciting game",
      "thumbnail_url": "https://example.com/image.jpg",
      "category": "GAME",
      "date": "2024-01-15",
      "tags": ["action", "adventure"],
      "link": "https://example.com/game",
      "created_at": "2024-01-01T00:00:00",
      "updated_at": "2024-01-01T00:00:00"
    }
  ]
}
```

### Get Project by ID
```http
GET /api/projects/{project_id}
```

**Response:** Single project object

### Create Project
```http
POST /api/projects
```

**Request Body:**
```json
{
  "id": "game-1",
  "title": "Super Adventure",
  "description": "An exciting game",
  "thumbnail_url": "https://example.com/image.jpg",
  "category": "GAME",
  "date": "2024-01-15",
  "tags": ["action", "adventure"],
  "link": "https://example.com/game"
}
```

**Response:** Created project object (201 Created)

### Update Project
```http
PUT /api/projects/{project_id}
```

**Request Body:** Partial project object (all fields optional except you want to update)

**Response:** Updated project object

### Delete Project
```http
DELETE /api/projects/{project_id}
```

**Response:** 204 No Content

---

## News API

Manage news articles and announcements.

### List News
```http
GET /api/news
```

**Query Parameters:**
- `skip` (optional, default: 0): Number of items to skip
- `limit` (optional, default: 100, max: 100): Number of items to return

**Response:**
```json
{
  "total": 4,
  "items": [
    {
      "id": "news-1",
      "title": "AI-Tracks Studio Launches New AI Engine",
      "excerpt": "We are proud to announce...",
      "content": "Full content here...",
      "date": "2024-05-20",
      "image_url": "https://example.com/news.jpg",
      "author": "Renfu Her",
      "created_at": "2024-05-20T00:00:00",
      "updated_at": "2024-05-20T00:00:00"
    }
  ]
}
```

### Get News by ID
```http
GET /api/news/{news_id}
```

**Response:** Single news object

### Create News
```http
POST /api/news
```

**Request Body:**
```json
{
  "id": "news-1",
  "title": "AI-Tracks Studio Launches New AI Engine",
  "excerpt": "We are proud to announce...",
  "content": "Full content here...",
  "date": "2024-05-20",
  "image_url": "https://example.com/news.jpg",
  "author": "Renfu Her"
}
```

**Response:** Created news object (201 Created)

### Update News
```http
PUT /api/news/{news_id}
```

**Request Body:** Partial news object

**Response:** Updated news object

### Delete News
```http
DELETE /api/news/{news_id}
```

**Response:** 204 No Content

---

## About Us API

Manage About page content.

### Get Current About Us Content
```http
GET /api/about
```

**Response:**
```json
{
  "id": 1,
  "title": "About Us",
  "subtitle": "We are a passionate team...",
  "description": "AI-Tracks Studio is an innovative...",
  "values": [
    {
      "icon": "Star",
      "title": "Creativity First",
      "description": "We believe in lively, vibrant designs..."
    },
    {
      "icon": "Zap",
      "title": "Powered by AI",
      "description": "Leveraging cutting-edge generative models..."
    }
  ],
  "contact_email": "renfu.her@gmail.com",
  "created_at": "2024-01-01T00:00:00",
  "updated_at": "2024-01-01T00:00:00"
}
```

### Get About Us by ID
```http
GET /api/about/{about_id}
```

**Response:** Single about us object

### Create About Us
```http
POST /api/about
```

**Request Body:**
```json
{
  "title": "About Us",
  "subtitle": "We are a passionate team...",
  "description": "AI-Tracks Studio is an innovative...",
  "values": [
    {
      "icon": "Star",
      "title": "Creativity First",
      "description": "We believe in lively, vibrant designs..."
    }
  ],
  "contact_email": "renfu.her@gmail.com"
}
```

**Response:** Created about us object (201 Created)

### Update About Us
```http
PUT /api/about/{about_id}
```

**Request Body:** Partial about us object

**Response:** Updated about us object

### Delete About Us
```http
DELETE /api/about/{about_id}
```

**Response:** 204 No Content

---

## Error Responses

All endpoints may return the following error responses:

### 400 Bad Request
```json
{
  "detail": "Project with this ID already exists"
}
```

### 404 Not Found
```json
{
  "detail": "Project not found"
}
```

### 422 Validation Error
```json
{
  "detail": [
    {
      "loc": ["body", "category"],
      "msg": "value is not a valid enumeration member",
      "type": "type_error.enum"
    }
  ]
}
```

---

## Testing with curl

### Create a Game Project
```bash
curl -X POST http://localhost:8000/api/projects \
  -H "Content-Type: application/json" \
  -d '{
    "id": "game-1",
    "title": "Super Adventure",
    "description": "An exciting adventure game",
    "category": "GAME",
    "tags": ["action", "adventure", "3D"]
  }'
```

### Get All Games
```bash
curl "http://localhost:8000/api/projects?category=GAME"
```

### Create News Article
```bash
curl -X POST http://localhost:8000/api/news \
  -H "Content-Type: application/json" \
  -d '{
    "id": "news-1",
    "title": "New Release",
    "excerpt": "Check out our latest update",
    "author": "Studio Team",
    "date": "2024-12-03"
  }'
```

### Update About Us
```bash
curl -X PUT http://localhost:8000/api/about/1 \
  -H "Content-Type: application/json" \
  -d '{
    "title": "About AI-Tracks Studio",
    "contact_email": "contact@aitracks.studio"
  }'
```

---

## Interactive Documentation

FastAPI provides auto-generated interactive API documentation:

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

These interfaces allow you to:
- View all endpoints
- See request/response schemas
- Test endpoints directly in the browser
- Download OpenAPI specification

