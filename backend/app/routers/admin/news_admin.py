"""Admin API for managing news."""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.dependencies import require_admin
from app.models import News, User
from app.schemas import NewsCreate, NewsUpdate, NewsResponse, NewsListResponse

router = APIRouter(prefix="/api/admin/news", tags=["admin-news"])


@router.get("", response_model=NewsListResponse)
async def admin_list_news(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin)
):
    """List all news (admin)."""
    total = db.query(News).count()
    items = db.query(News).offset(skip).limit(limit).all()
    return NewsListResponse(total=total, items=items)


@router.post("", response_model=NewsResponse, status_code=201)
async def admin_create_news(
    news: NewsCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin)
):
    """Create new news (admin)."""
    db_news = News(**news.model_dump())
    db.add(db_news)
    db.commit()
    db.refresh(db_news)
    return db_news


@router.put("/{news_id}", response_model=NewsResponse)
async def admin_update_news(
    news_id: str,
    news: NewsUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin)
):
    """Update news (admin)."""
    db_news = db.query(News).filter(News.id == news_id).first()
    if not db_news:
        raise HTTPException(status_code=404, detail="News not found")
    
    update_data = news.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_news, field, value)
    
    db.commit()
    db.refresh(db_news)
    return db_news


@router.delete("/{news_id}", status_code=204)
async def admin_delete_news(
    news_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin)
):
    """Delete news (admin)."""
    db_news = db.query(News).filter(News.id == news_id).first()
    if not db_news:
        raise HTTPException(status_code=404, detail="News not found")
    
    db.delete(db_news)
    db.commit()

