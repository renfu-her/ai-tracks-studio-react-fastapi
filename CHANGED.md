# CHANGED.md - 更新紀錄 / Change Log

## 2025-12-03 22:01:56 TST

### Complete Admin Backend System 完整後台管理系統

參考 shopping-react-flask 項目，實現完整的後台管理系統。

#### New Dependencies 新增依賴
- `python-jose[cryptography]` - JWT token handling  
- `passlib` + `bcrypt` - Password hashing
- `python-multipart` - Form data handling
- `itsdangerous` - Session management

#### User Model & Authentication 用戶模型與認證
**Created `app/models/user.py`:**
- User model with roles (ADMIN, USER)
- User status (ACTIVE, INACTIVE, SUSPENDED)
- Password hash storage
- Email unique constraint

**Created `app/core/security.py`:**
- Password hashing with bcrypt
- JWT token creation/decoding
- Secure authentication utilities

#### Admin APIs 管理 API
**Authentication APIs** (`app/routers/admin/`):
- `POST /api/admin/login` - Admin login with session
- `POST /api/admin/logout` - Clear session
- `GET /api/admin/me` - Get current admin info

**Projects Management APIs:**
- `GET /api/admin/projects` - List all projects (admin only)
- `GET /api/admin/projects/{id}` - Get project details
- `POST /api/admin/projects` - Create new project
- `PUT /api/admin/projects/{id}` - Update project
- `DELETE /api/admin/projects/{id}` - Delete project

**News Management APIs:**
- `GET /api/admin/news` - List all news
- `POST /api/admin/news` - Create news article
- `PUT /api/admin/news/{id}` - Update news
- `DELETE /api/admin/news/{id}` - Delete news

**About Us Management APIs:**
- `GET /api/admin/about` - List about entries
- `POST /api/admin/about` - Create about entry
- `PUT /api/admin/about/{id}` - Update about
- `DELETE /api/admin/about/{id}` - Delete about

#### Dependencies & Security 依賴與安全
**Created `app/dependencies.py`:**
- `get_db()` - Database session dependency
- `get_current_user_from_session()` - Get user from session
- `require_admin()` - Admin authentication guard

**Session Management:**
- Session-based authentication (24 hour expiry)
- Secure cookie handling
- CSRF protection with same_site=lax

#### Admin Initialization 管理員初始化
**Created `app/init_admin.py`:**
- Auto-create admin user on startup
- Default credentials:
  - Email: `admin@admin.com`
  - Password: `admin123` ⚠️ (change in production!)
- Updates existing users to admin if needed

#### Configuration Updates 配置更新
**Updated `app/config.py`:**
- Added `SECRET_KEY` for JWT signing
- Added `SESSION_SECRET_KEY` for session encryption  
- Added `ALGORITHM` (HS256) for JWT
- Added `ACCESS_TOKEN_EXPIRE_MINUTES` (30)
- Added `FRONTEND_URL` and `BACKEND_URL`

#### Files Created 創建的文件
**Models:**
- `backend/app/models/user.py` - User model with roles

**Core:**
- `backend/app/core/security.py` - Security utilities
- `backend/app/core/__init__.py` - Core exports

**Admin APIs:**
- `backend/app/routers/admin/__init__.py` - Admin router
- `backend/app/routers/admin/login.py` - Login API
- `backend/app/routers/admin/logout.py` - Logout API
- `backend/app/routers/admin/me.py` - Current user API
- `backend/app/routers/admin/projects_admin.py` - Projects CRUD
- `backend/app/routers/admin/news_admin.py` - News CRUD
- `backend/app/routers/admin/about_admin.py` - About CRUD

**Dependencies:**
- `backend/app/dependencies.py` - FastAPI dependencies

**Initialization:**
- `backend/app/init_admin.py` - Admin user setup

**Documentation:**
- `backend/ADMIN_SYSTEM.md` - Complete admin system guide

#### Next Steps 下一步
**To complete the admin system:**
1. Update `backend/app/main.py`:
   - Add `SessionMiddleware`
   - Import and include `admin_router`
   - Call `init_admin_user()` on startup
   - (Optional) Add `/backend` routes for admin UI

2. Create admin frontend:
   - Login page at `/backend`
   - Admin dashboard
   - CRUD interfaces for Projects, News, About

#### Security Notes 安全提示
⚠️ **IMPORTANT - Change in Production:**
- `SECRET_KEY` - JWT signing key
- `SESSION_SECRET_KEY` - Session encryption key
- Admin password (currently: admin123)

Set via `.env` file:
```env
SECRET_KEY=your-super-secret-key-here
SESSION_SECRET_KEY=your-session-key-here
```

#### Features Implemented 實現功能
✅ **User Authentication** - Secure session-based auth  
✅ **Role-Based Access** - Admin-only endpoints  
✅ **Password Security** - Bcrypt hashing  
✅ **JWT Tokens** - Token generation/validation  
✅ **Auto Admin Init** - Default admin creation  
✅ **Complete CRUD** - All content management  
✅ **Type Safety** - Full Pydantic validation  
✅ **Clean Architecture** - Separated concerns  

---

## 2025-12-03 21:43:58 TST

### Frontend API Integration 前端 API 整合

#### Connected Frontend to Backend API 連接前端到後端 API

Successfully integrated the React frontend with the FastAPI backend, replacing all hardcoded data with real API calls.

#### New API Layer 新增 API 層
Created comprehensive API client layer:
- **`frontend/api/config.ts`** - API configuration and base URL management
- **`frontend/api/client.ts`** - HTTP client with error handling and timeouts
- **`frontend/api/projects.ts`** - Projects/Games API service
- **`frontend/api/news.ts`** - News API service
- **`frontend/api/about.ts`** - About Us API service
- **`frontend/api/index.ts`** - Central export point

#### Updated Types 更新類型
- Updated `frontend/types.ts` with API response types
- Added `ProjectListResponse`, `NewsListResponse`
- Added `AboutUs` and `AboutValue` interfaces
- Added `LoadingState` interface
- Matched backend schema (snake_case: `thumbnail_url`, `image_url`)

#### Route Changes 路由變更
Updated routing structure as requested:
- `/games` → `/game` (displays games from API: `category=GAME`)
- `/websites` → `/website` (displays websites from API: `category=WEBSITE`)
- `/news` → `/news` (fetches from news API)
- `/about` → `/about` (fetches from about API)
- `/` → Home (displays featured games)

#### Component Updates 組件更新
**`frontend/App.tsx`** - Complete rewrite:
- Removed hardcoded data (GAMES, WEBSITES, NEWS constants)
- Added data fetching with `useEffect` hooks
- Created separate page components: `GamesPage`, `WebsitesPage`, `NewsPage`, `AboutPage`
- Added `LoadingSpinner` component
- Added `ErrorMessage` component with retry functionality
- Implemented proper error handling for all API calls

**`frontend/components/Layout.tsx`**:
- Updated navigation links to use new routes
- Desktop menu: `/game`, `/website` instead of `/games`, `/websites`
- Mobile menu: Updated all route references
- Footer: Updated quick links

**`frontend/components/ItemGrid.tsx`**:
- Updated to use `thumbnail_url` instead of `thumbnailUrl`
- Matches backend API response format

**`frontend/constants.ts`**:
- Removed hardcoded GAMES, WEBSITES, NEWS arrays
- Kept HERO_IMAGES for hero sections

#### Features Implemented 實現功能
✅ **Dynamic Data Loading** - All content from backend API  
✅ **Loading States** - Spinner during data fetch  
✅ **Error Handling** - User-friendly error messages  
✅ **Retry Functionality** - Try again on failed requests  
✅ **Empty States** - Handled when no data available  
✅ **Type Safety** - Full TypeScript throughout  
✅ **Clean Architecture** - Separated API layer from components  

#### API Configuration API 配置
- Base URL: `http://localhost:8000` (development)
- Configurable via `VITE_API_BASE_URL` environment variable
- 30-second timeout for requests
- Proper error handling for network issues

#### Data Flow 數據流
1. Component mounts → `useEffect` triggered
2. Display loading spinner
3. API call via service layer
4. On success: Display data
5. On error: Show error message with retry option

---

## 2025-12-03 21:31:51 TST

### Added Gunicorn for Production Deployment

#### New Dependency 新增依賴
- **Gunicorn 23.0.0** - Python WSGI HTTP Server for production

#### Production Server Setup 生產環境設定
- Added Gunicorn with Uvicorn workers configuration
- Created `run_production.py` with optimal production settings
- Updated documentation with production deployment instructions

#### Running Commands 執行命令
**Development 開發環境:**
```bash
uv run uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

**Production 生產環境:**
```bash
uv run gunicorn app.main:app \
  --workers 4 \
  --worker-class uvicorn.workers.UvicornWorker \
  --bind 0.0.0.0:8000
```

---

## 2025-12-03 21:17:04 TST

### Created FastAPI Backend with Clean Architecture

**Update:** Changed to Python 3.14 (standard version, non-freethreaded) for better compatibility.

#### Project Structure 專案結構
- Created `backend/` directory with clean architecture
- Initialized UV project with Python 3.12
- Organized code into layers: models, schemas, repositories, routers

#### Dependencies 依賴套件
- **Python**: 3.14.0 (standard version, non-freethreaded)
- FastAPI >= 0.109.0 - Modern web framework
- Uvicorn >= 0.27.0 - ASGI server (development)
- Gunicorn >= 23.0.0 - WSGI server (production)
- SQLAlchemy >= 2.0.25 - ORM for database
- PyMySQL >= 1.1.0 - MySQL connector
- Pydantic >= 2.5.3 - Data validation
- Pydantic-settings >= 2.1.0 - Configuration management

#### Database Models 資料庫模型
Created three main models:
1. **Project** (`projects` table)
   - Fields: id, title, description, thumbnail_url, category (GAME/WEBSITE), date, tags, link
   - Supports both games and websites
   
2. **News** (`news` table)
   - Fields: id, title, excerpt, content, date, image_url, author
   - For blog posts and announcements
   
3. **AboutUs** (`about_us` table)
   - Fields: id, title, subtitle, description, values (JSON), contact_email
   - Dynamic content management for About page

#### API Endpoints API 端點
Implemented full CRUD operations for all resources:

**Projects 專案:**
- `GET /api/projects` - List with optional category filter
- `GET /api/projects/{id}` - Get single project
- `POST /api/projects` - Create new project
- `PUT /api/projects/{id}` - Update project
- `DELETE /api/projects/{id}` - Delete project

**News 新聞:**
- `GET /api/news` - List all news
- `GET /api/news/{id}` - Get single article
- `POST /api/news` - Create article
- `PUT /api/news/{id}` - Update article
- `DELETE /api/news/{id}` - Delete article

**About Us 關於我們:**
- `GET /api/about` - Get current content
- `GET /api/about/{id}` - Get by ID
- `POST /api/about` - Create content
- `PUT /api/about/{id}` - Update content
- `DELETE /api/about/{id}` - Delete content

#### Clean Code Architecture 乾淨架構
Implemented clean code principles:
- **Repository Pattern**: Abstracted data access layer
- **Dependency Injection**: Using FastAPI's dependency system
- **Separation of Concerns**: Models, Schemas, Repositories, Routers
- **Type Safety**: Full type hints throughout
- **Error Handling**: Proper HTTP exceptions
- **Validation**: Pydantic schemas for request/response

#### Configuration 設定
- Database: MySQL (root user, no password, studio database)
- CORS: Enabled for frontend (localhost:5173, localhost:3000)
- API Prefix: `/api`
- Auto-create tables on startup

#### Files Created 建立的檔案

**Core Application:**
- `backend/app/main.py` - FastAPI application entry point
- `backend/app/config.py` - Configuration settings
- `backend/app/database.py` - Database connection

**Models (SQLAlchemy ORM):**
- `backend/app/models/project.py` - Project model (games/websites)
- `backend/app/models/news.py` - News model
- `backend/app/models/about.py` - About Us model

**Schemas (Pydantic Validation):**
- `backend/app/schemas/project.py` - Project validation schemas
- `backend/app/schemas/news.py` - News validation schemas
- `backend/app/schemas/about.py` - About Us validation schemas

**Repositories (Data Access Layer):**
- `backend/app/repositories/base.py` - Base repository with CRUD operations
- `backend/app/repositories/project.py` - Project repository
- `backend/app/repositories/news.py` - News repository
- `backend/app/repositories/about.py` - About Us repository

**Routers (API Endpoints):**
- `backend/app/routers/projects.py` - Projects CRUD endpoints
- `backend/app/routers/news.py` - News CRUD endpoints
- `backend/app/routers/about.py` - About Us CRUD endpoints

**Configuration & Documentation:**
- `backend/pyproject.toml` - UV project configuration
- `backend/run.py` - Quick start script
- `backend/README.md` - Project overview
- `backend/API_DOCUMENTATION.md` - Complete API reference
- `backend/GETTING_STARTED.md` - Setup and usage guide
- `backend/.gitignore` - Git ignore file

#### Running the Server 啟動伺服器
```bash
cd backend
uv run python run.py
```

Or alternatively:
```bash
cd backend
uv run uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

Access:
- API: http://localhost:8000
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

#### Notes 備註
- Database tables will be created automatically on first run
- Make sure MySQL is running with `studio` database created
- All code follows clean code and SOLID principles
- Type hints and docstrings throughout for better maintainability
- Fixed type annotations to use modern Python 3.12 syntax (str | None instead of Optional[str])
- Resolved date type name collision in Pydantic schemas
- Verified all imports load successfully

