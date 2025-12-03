"""Main FastAPI application."""

from contextlib import asynccontextmanager
from pathlib import Path
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from starlette.middleware.sessions import SessionMiddleware
import logging

from app.config import settings
from app.database import create_tables
from app.routers import projects, news, about
from app.routers.admin import router as admin_router
from app.init_admin import init_admin_user

logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Application lifespan context manager.
    Handles startup and shutdown events.
    """
    # Startup: Create database tables
    print("Creating database tables...")
    create_tables()
    print("Database tables created successfully!")
    
    # Initialize admin user
    try:
        init_admin_user()
        print("Admin user initialized!")
    except Exception as e:
        logger.warning(f"Failed to initialize admin user: {e}")
    
    yield
    
    # Shutdown: Cleanup if needed
    print("Application shutdown")


# Create FastAPI application
app = FastAPI(
    title="AI-Tracks Studio API",
    description="Backend API for AI-Tracks Studio - managing games, websites, news, and about content",
    version="1.0.0",
    lifespan=lifespan,
)

# Add Session middleware (must be before CORS)
app.add_middleware(
    SessionMiddleware,
    secret_key=settings.SESSION_SECRET_KEY,
    max_age=3600 * 24,  # 24 hours
    same_site="lax"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(projects.router, prefix=settings.API_PREFIX)
app.include_router(news.router, prefix=settings.API_PREFIX)
app.include_router(about.router, prefix=settings.API_PREFIX)
app.include_router(admin_router)  # Admin routes (already have /api/admin prefix)

# Mount static files
static_dir = Path(__file__).parent / "static"
static_dir.mkdir(exist_ok=True)
app.mount("/static", StaticFiles(directory=str(static_dir)), name="static")


@app.get("/")
def root():
    """Root endpoint with API information."""
    return {
        "message": "Welcome to AI-Tracks Studio API",
        "version": "1.0.0",
        "docs": "/docs",
        "redoc": "/redoc",
        "backend": "/backend"
    }


@app.get("/health")
def health_check():
    """Health check endpoint."""
    return {"status": "healthy"}


@app.get("/backend")
async def backend_admin():
    """Backend admin home - redirect to login."""
    return FileResponse(static_dir / "login.html")


@app.get("/backend/login")
async def backend_login():
    """Backend admin login page."""
    return FileResponse(static_dir / "login.html")


@app.get("/backend/projects")
async def backend_projects():
    """Projects management page - list."""
    return FileResponse(static_dir / "admin" / "projects" / "index.html")


@app.get("/backend/projects/add")
async def backend_projects_add():
    """Projects management page - add."""
    return FileResponse(static_dir / "admin" / "projects" / "add-edit.html")


@app.get("/backend/projects/edit")
async def backend_projects_edit():
    """Projects management page - edit."""
    return FileResponse(static_dir / "admin" / "projects" / "add-edit.html")


@app.get("/backend/news")
async def backend_news():
    """News management page - list."""
    return FileResponse(static_dir / "admin" / "news" / "index.html")


@app.get("/backend/news/add")
async def backend_news_add():
    """News management page - add."""
    return FileResponse(static_dir / "admin" / "news" / "add-edit.html")


@app.get("/backend/news/edit")
async def backend_news_edit():
    """News management page - edit."""
    return FileResponse(static_dir / "admin" / "news" / "add-edit.html")


@app.get("/backend/about")
async def backend_about():
    """About Us management page - list."""
    return FileResponse(static_dir / "admin" / "about" / "index.html")


@app.get("/backend/about/add")
async def backend_about_add():
    """About Us management page - add."""
    return FileResponse(static_dir / "admin" / "about" / "add-edit.html")


@app.get("/backend/about/edit")
async def backend_about_edit():
    """About Us management page - edit."""
    return FileResponse(static_dir / "admin" / "about" / "add-edit.html")

