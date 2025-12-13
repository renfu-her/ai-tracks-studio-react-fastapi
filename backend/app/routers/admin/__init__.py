"""Admin routers package."""

from fastapi import APIRouter
from app.routers.admin import login, logout, me, projects_admin, news_admin, about_admin, banner_admin, feedback_admin, upload

# Create main admin router
router = APIRouter()

# Include auth routers
router.include_router(login.router, tags=["admin-auth"])
router.include_router(logout.router, tags=["admin-auth"])
router.include_router(me.router, tags=["admin-auth"])

# Include CRUD routers
router.include_router(projects_admin.router, tags=["admin-projects"])
router.include_router(news_admin.router, tags=["admin-news"])
router.include_router(about_admin.router, tags=["admin-about"])
router.include_router(banner_admin.router, tags=["admin-banners"])
router.include_router(feedback_admin.router, tags=["admin-feedback"])

# Include upload router
router.include_router(upload.router, tags=["admin-upload"])

