# Getting Started with AI-Tracks Studio API

## 快速開始 / Quick Start

### Prerequisites 前置需求

1. **Python 3.14** (standard version, installed via UV automatically)
2. **MySQL Server** running locally
3. **Git** for version control

### Step 1: Database Setup 資料庫設定

Create the MySQL database:

```sql
CREATE DATABASE IF NOT EXISTS studio 
CHARACTER SET utf8mb4 
COLLATE utf8mb4_unicode_ci;
```

Default connection settings:
- Host: `localhost`
- Port: `3306`
- User: `root`
- Password: (empty)
- Database: `studio`

### Step 2: Install Dependencies 安裝依賴

```bash
cd backend
uv sync
```

This will:
- Download and install Python 3.14 (if needed)
- Create a virtual environment in `.venv/`
- Install all required packages

### Step 3: Run the Server 啟動伺服器

#### Development Mode 開發環境

**Option A: Using the run script (Recommended)**
```bash
uv run python run.py
```

**Option B: Using uvicorn directly**
```bash
uv run uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

**Option C: Activate venv and run**
```bash
# Windows
.venv\Scripts\activate

# Linux/Mac
source .venv/bin/activate

# Then run
uvicorn app.main:app --reload
```

#### Production Mode 生產環境

For production deployment, use Gunicorn with Uvicorn workers:

```bash
# Basic production command
uv run gunicorn app.main:app \
  --workers 4 \
  --worker-class uvicorn.workers.UvicornWorker \
  --bind 0.0.0.0:8000

# Recommended production settings
uv run gunicorn app.main:app \
  --workers 4 \
  --worker-class uvicorn.workers.UvicornWorker \
  --bind 0.0.0.0:8000 \
  --timeout 60 \
  --access-logfile - \
  --error-logfile - \
  --log-level info
```

**Worker Count Formula:** `(2 x CPU cores) + 1`

### Step 4: Verify Installation 驗證安裝

The server should start with output like:
```
Creating database tables...
Database tables created successfully!
INFO:     Uvicorn running on http://0.0.0.0:8000
```

Open your browser and visit:
- **API Root**: http://localhost:8000
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

### Step 5: Test the API 測試 API

#### Using Swagger UI (Recommended for beginners)

1. Go to http://localhost:8000/docs
2. Click on any endpoint (e.g., `POST /api/projects`)
3. Click "Try it out"
4. Fill in the request body
5. Click "Execute"

#### Using curl

Create a test project:
```bash
curl -X POST http://localhost:8000/api/projects \
  -H "Content-Type: application/json" \
  -d '{
    "id": "test-game-1",
    "title": "Test Game",
    "description": "A test game project",
    "category": "GAME",
    "tags": ["test", "demo"]
  }'
```

List all projects:
```bash
curl http://localhost:8000/api/projects
```

#### Using Python requests

```python
import requests

# Create a project
response = requests.post(
    "http://localhost:8000/api/projects",
    json={
        "id": "game-1",
        "title": "Super Adventure",
        "category": "GAME",
        "description": "An amazing game",
        "tags": ["action", "adventure"]
    }
)
print(response.json())

# List projects
response = requests.get("http://localhost:8000/api/projects")
print(response.json())
```

## Project Structure 專案結構

```
backend/
├── app/
│   ├── __init__.py              # Package initialization
│   ├── main.py                  # FastAPI app & startup
│   ├── config.py                # Settings & configuration
│   ├── database.py              # DB connection & session
│   │
│   ├── models/                  # SQLAlchemy ORM Models
│   │   ├── __init__.py
│   │   ├── project.py          # Project model (games/websites)
│   │   ├── news.py             # News model
│   │   └── about.py            # About Us model
│   │
│   ├── schemas/                 # Pydantic Schemas
│   │   ├── __init__.py
│   │   ├── project.py          # Project validation schemas
│   │   ├── news.py             # News validation schemas
│   │   └── about.py            # About Us validation schemas
│   │
│   ├── repositories/            # Data Access Layer
│   │   ├── __init__.py
│   │   ├── base.py             # Base repository with CRUD
│   │   ├── project.py          # Project repository
│   │   ├── news.py             # News repository
│   │   └── about.py            # About Us repository
│   │
│   └── routers/                 # API Endpoints
│       ├── __init__.py
│       ├── projects.py         # Projects CRUD endpoints
│       ├── news.py             # News CRUD endpoints
│       └── about.py            # About Us CRUD endpoints
│
├── pyproject.toml               # UV project config & dependencies
├── run.py                       # Quick start script
├── README.md                    # Project overview
├── API_DOCUMENTATION.md         # API reference
└── GETTING_STARTED.md          # This file
```

## Architecture 架構說明

This project follows **Clean Architecture** principles:

### 1. Models Layer (資料模型層)
- SQLAlchemy ORM models
- Define database structure
- Handle data persistence

### 2. Schemas Layer (驗證層)
- Pydantic models
- Request/response validation
- Data serialization/deserialization

### 3. Repository Layer (資料存取層)
- Abstract database operations
- Implement business logic
- Single responsibility principle

### 4. Router Layer (API 路由層)
- HTTP endpoints
- Request handling
- Dependency injection

### Benefits of This Architecture:

✅ **Separation of Concerns** - Each layer has one job  
✅ **Testability** - Easy to unit test each layer  
✅ **Maintainability** - Changes are localized  
✅ **Scalability** - Easy to extend functionality  
✅ **Type Safety** - Full type hints throughout  

## Configuration 設定

You can customize settings by creating a `.env` file:

```env
# Database
DB_HOST=localhost
DB_PORT=3306
DB_USER=root
DB_PASSWORD=
DB_NAME=studio

# API
API_PREFIX=/api
CORS_ORIGINS=["http://localhost:5173","http://localhost:3000"]
```

## Common Tasks 常見任務

### Add a New Endpoint

1. Create route in appropriate router file
2. Use dependency injection for repository
3. Add proper error handling
4. Document with docstrings

### Add a New Model

1. Create model in `app/models/`
2. Create schemas in `app/schemas/`
3. Create repository in `app/repositories/`
4. Create router in `app/routers/`
5. Register router in `app/main.py`

### Check Database Tables

```bash
mysql -u root -e "USE studio; SHOW TABLES;"
```

### View Table Structure

```bash
mysql -u root -e "USE studio; DESCRIBE projects;"
```

## Troubleshooting 疑難排解

### Database Connection Error

**Problem:** `Can't connect to MySQL server`

**Solution:**
1. Make sure MySQL is running
2. Check connection settings in `app/config.py`
3. Verify database exists: `CREATE DATABASE studio;`

### Import Errors

**Problem:** `ModuleNotFoundError: No module named 'app'`

**Solution:**
```bash
# Make sure you're in the backend directory
cd backend

# Use uv run
uv run python run.py
```

### Port Already in Use

**Problem:** `Address already in use`

**Solution:**
```bash
# Change port in run.py or use different port
uv run uvicorn app.main:app --port 8001
```

## Next Steps 下一步

1. ✅ Read [API_DOCUMENTATION.md](./API_DOCUMENTATION.md) for API reference
2. ✅ Explore Swagger UI at http://localhost:8000/docs
3. ✅ Create sample data using the API
4. ✅ Connect frontend to the backend
5. ✅ Implement authentication (if needed)
6. ✅ Add more endpoints as required

## Support 支援

For issues or questions:
- Check the [README.md](./README.md)
- Review [API_DOCUMENTATION.md](./API_DOCUMENTATION.md)
- Inspect logs in the terminal
- Use Swagger UI for endpoint testing

Happy coding! 🚀

