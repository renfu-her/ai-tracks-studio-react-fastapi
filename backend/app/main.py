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
from app.db_migrate import auto_migrate_to_longtext

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
    
    # Auto-migrate TEXT to LONGTEXT
    print("Checking database schema...")
    try:
        auto_migrate_to_longtext()
        print("Database schema check completed!")
    except Exception as e:
        logger.warning(f"Schema migration warning: {e}")
    
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

# Mount static files under /backend/static
# This way it's handled by the existing Nginx location ~ ^/(docs|backend|...) rule
static_dir = Path(__file__).parent / "static"
static_dir.mkdir(exist_ok=True)
app.mount("/backend/static", StaticFiles(directory=str(static_dir)), name="static")


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
    """Backend admin - SPA (Single Page Application)."""
    return FileResponse(static_dir / "admin.html")


@app.get("/backend/login")
async def backend_login():
    """Backend admin login page."""
    return FileResponse(static_dir / "login.html")


# Legacy routes for backward compatibility
@app.get("/backend/{module}")
async def backend_module_legacy(module: str):
    """Legacy route - redirect to SPA."""
    return FileResponse(static_dir / "admin.html")


@app.get("/backend/{module}/{action}")
async def backend_module_action_legacy(module: str, action: str):
    """Legacy route - redirect to SPA."""
    return FileResponse(static_dir / "admin.html")

