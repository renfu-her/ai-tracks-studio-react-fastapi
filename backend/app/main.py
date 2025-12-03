"""Main FastAPI application."""

from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import settings
from app.database import create_tables
from app.routers import projects, news, about


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


@app.get("/")
def root():
    """Root endpoint with API information."""
    return {
        "message": "Welcome to AI-Tracks Studio API",
        "version": "1.0.0",
        "docs": "/docs",
        "redoc": "/redoc",
    }


@app.get("/health")
def health_check():
    """Health check endpoint."""
    return {"status": "healthy"}

