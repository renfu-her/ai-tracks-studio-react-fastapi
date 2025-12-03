"""Admin API for managing news."""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.dependencies import require_admin
from app.models import User
from app.repositories import NewsRepository
from app.schemas import NewsCreate, NewsUpdate, NewsResponse, NewsListResponse

router = APIRouter(prefix="/api/admin/news", tags=["admin-news"])


def get_news_repo(db: Session = Depends(get_db)) -> NewsRepository:
    """Dependency to get news repository."""
    return NewsRepository(db)


@router.get("", response_model=NewsListResponse)
async def admin_list_news(
    skip: int = 0,
    limit: int = 100,
    repo: NewsRepository = Depends(get_news_repo),
    current_user: User = Depends(require_admin)
):
    """List all news (admin)."""
    total = repo.count()
    items = repo.get_all(skip=skip, limit=limit)
    return NewsListResponse(total=total, items=items)


@router.post("", response_model=NewsResponse, status_code=201)
async def admin_create_news(
    news: NewsCreate,
    repo: NewsRepository = Depends(get_news_repo),
    current_user: User = Depends(require_admin)
):
    """Create new news (admin)."""
    return repo.create(news.model_dump())


@router.put("/{news_id}", response_model=NewsResponse)
async def admin_update_news(
    news_id: str,
    news: NewsUpdate,
    repo: NewsRepository = Depends(get_news_repo),
    current_user: User = Depends(require_admin)
):
    """Update news (admin)."""
    updated = repo.update(news_id, news.model_dump(exclude_unset=True))
    if not updated:
        raise HTTPException(status_code=404, detail="News not found")
    return updated


@router.delete("/{news_id}", status_code=204)
async def admin_delete_news(
    news_id: str,
    repo: NewsRepository = Depends(get_news_repo),
    current_user: User = Depends(require_admin)
):
    """Delete news (admin)."""
    success = repo.delete(news_id)
    if not success:
        raise HTTPException(status_code=404, detail="News not found")

