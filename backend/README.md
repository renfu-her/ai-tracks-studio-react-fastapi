# AI-Tracks Studio API

FastAPI backend for AI-Tracks Studio with clean architecture.

## Features

- **Clean Architecture**: Separation of concerns with models, schemas, repositories, and routers
- **Repository Pattern**: Data access abstraction layer
- **Full CRUD Operations**: Complete Create, Read, Update, Delete for all resources
- **MySQL Database**: Using SQLAlchemy ORM
- **Type Safety**: Full type hints throughout the codebase
- **API Documentation**: Auto-generated with Swagger UI and ReDoc

## Project Structure

```
backend/
├── app/
│   ├── models/          # SQLAlchemy ORM models
│   ├── schemas/         # Pydantic validation schemas
│   ├── repositories/    # Data access layer
│   ├── routers/         # API endpoints
│   ├── config.py        # Configuration settings
│   ├── database.py      # Database connection
│   └── main.py          # FastAPI application
├── pyproject.toml       # UV project configuration
└── README.md
```

## Database Setup

The application uses MySQL with the following configuration:
- Host: localhost
- Port: 3306
- User: root
- Password: (empty)
- Database: studio

Make sure MySQL is running and the `studio` database exists:

```sql
CREATE DATABASE IF NOT EXISTS studio CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

The application will automatically create tables on startup.

## Installation

This project uses `uv` for dependency management with Python 3.14.

```bash
# The project uses Python 3.14 (standard version)
# Install dependencies
uv sync

# Or manually activate virtual environment
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

## Running the Server

### Development Mode (開發環境)

```bash
# Using quick start script
uv run python run.py

# Or using uvicorn directly with auto-reload
uv run uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# Or with activated venv
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### Production Mode (生產環境)

For production, use Gunicorn with Uvicorn workers:

```bash
# Using Gunicorn with 4 workers
uv run gunicorn app.main:app \
  --workers 4 \
  --worker-class uvicorn.workers.UvicornWorker \
  --bind 0.0.0.0:8000

# With specified timeout and log level
uv run gunicorn app.main:app \
  --workers 4 \
  --worker-class uvicorn.workers.UvicornWorker \
  --bind 0.0.0.0:8000 \
  --timeout 60 \
  --log-level info
```

The API will be available at:
- API: http://localhost:8000
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## API Endpoints

### Projects (Games & Websites)

- `GET /api/projects` - List all projects (with optional ?category=GAME|WEBSITE)
- `GET /api/projects/{id}` - Get single project
- `POST /api/projects` - Create new project
- `PUT /api/projects/{id}` - Update project
- `DELETE /api/projects/{id}` - Delete project

### News

- `GET /api/news` - List all news
- `GET /api/news/{id}` - Get single news article
- `POST /api/news` - Create news article
- `PUT /api/news/{id}` - Update news article
- `DELETE /api/news/{id}` - Delete news article

### About Us

- `GET /api/about` - Get current About Us content
- `GET /api/about/{id}` - Get specific About Us content
- `POST /api/about` - Create About Us content
- `PUT /api/about/{id}` - Update About Us content
- `DELETE /api/about/{id}` - Delete About Us content

## Environment Variables

You can create a `.env` file in the backend directory:

```env
DB_HOST=localhost
DB_PORT=3306
DB_USER=root
DB_PASSWORD=
DB_NAME=studio
API_PREFIX=/api
CORS_ORIGINS=["http://localhost:5173","http://localhost:3000"]
```

## Development

The codebase follows clean code principles:

- **Models**: Define database structure
- **Schemas**: Validate request/response data
- **Repositories**: Handle data access logic
- **Routers**: Define API endpoints
- **Separation of Concerns**: Each layer has a single responsibility

## Testing with curl

Create a project:
```bash
curl -X POST http://localhost:8000/api/projects \
  -H "Content-Type: application/json" \
  -d '{
    "id": "game-1",
    "title": "Super Adventure",
    "description": "An exciting game",
    "category": "GAME",
    "tags": ["action", "adventure"]
  }'
```

List projects:
```bash
curl http://localhost:8000/api/projects
```

Filter by category:
```bash
curl http://localhost:8000/api/projects?category=GAME
```

