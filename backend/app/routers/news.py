"""API routes for news articles."""

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.database import get_db
from app.repositories import NewsRepository
from app.schemas import (
    NewsCreate,
    NewsUpdate,
    NewsResponse,
    NewsListResponse,
)

router = APIRouter(prefix="/news", tags=["news"])


def get_news_repo(db: Session = Depends(get_db)) -> NewsRepository:
    """Dependency to get news repository."""
    return NewsRepository(db)


@router.get("", response_model=NewsListResponse)
def list_news(
    skip: int = Query(0, ge=0, description="Number of items to skip"),
    limit: int = Query(100, ge=1, le=100, description="Number of items to return"),
    repo: NewsRepository = Depends(get_news_repo),
):
    """
    Get list of news articles.
    
    Args:
        skip: Number of items to skip for pagination
        limit: Maximum number of items to return
        repo: News repository instance
        
    Returns:
        List of news articles with total count
    """
    items = repo.get_all(skip=skip, limit=limit)
    total = repo.count()
    
    return NewsListResponse(total=total, items=items)


@router.get("/{news_id}", response_model=NewsResponse)
def get_news(
    news_id: str,
    repo: NewsRepository = Depends(get_news_repo),
):
    """
    Get a single news article by ID.
    
    Args:
        news_id: News identifier
        repo: News repository instance
        
    Returns:
        News article details
        
    Raises:
        HTTPException: If news not found
    """
    news = repo.get_by_id(news_id)
    if not news:
        raise HTTPException(status_code=404, detail="News not found")
    return news


@router.post("", response_model=NewsResponse, status_code=201)
def create_news(
    news_in: NewsCreate,
    repo: NewsRepository = Depends(get_news_repo),
):
    """
    Create a new news article.
    
    Args:
        news_in: News data
        repo: News repository instance
        
    Returns:
        Created news article
        
    Raises:
        HTTPException: If news with same ID already exists
    """
    existing = repo.get_by_id(news_in.id)
    if existing:
        raise HTTPException(status_code=400, detail="News with this ID already exists")
    
    return repo.create(news_in.model_dump())


@router.put("/{news_id}", response_model=NewsResponse)
def update_news(
    news_id: str,
    news_in: NewsUpdate,
    repo: NewsRepository = Depends(get_news_repo),
):
    """
    Update an existing news article.
    
    Args:
        news_id: News identifier
        news_in: Updated news data
        repo: News repository instance
        
    Returns:
        Updated news article
        
    Raises:
        HTTPException: If news not found
    """
    news = repo.update(news_id, news_in.model_dump(exclude_unset=True))
    if not news:
        raise HTTPException(status_code=404, detail="News not found")
    return news


@router.delete("/{news_id}", status_code=204)
def delete_news(
    news_id: str,
    repo: NewsRepository = Depends(get_news_repo),
):
    """
    Delete a news article.
    
    Args:
        news_id: News identifier
        repo: News repository instance
        
    Raises:
        HTTPException: If news not found
    """
    success = repo.delete(news_id)
    if not success:
        raise HTTPException(status_code=404, detail="News not found")


@router.post("/{news_id}/view", response_model=NewsResponse)
def increment_news_views(
    news_id: str,
    repo: NewsRepository = Depends(get_news_repo),
):
    """
    Increment view count for a news article.
    
    Args:
        news_id: News identifier
        repo: News repository instance
        
    Returns:
        Updated news article with incremented views
        
    Raises:
        HTTPException: If news not found
    """
    news = repo.increment_views(news_id)
    if not news:
        raise HTTPException(status_code=404, detail="News not found")
    return news

