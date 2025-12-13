"""Repository for News operations."""

from sqlalchemy.orm import Session
from app.models import News
from app.repositories.base import BaseRepository


class NewsRepository(BaseRepository[News]):
    """Repository for managing News entities."""
    
    def __init__(self, db: Session):
        """
        Initialize news repository.
        
        Args:
            db: Database session
        """
        super().__init__(News, db)
    
    def increment_views(self, news_id: str) -> News | None:
        """
        Increment view count for a news article.
        
        Args:
            news_id: News identifier
            
        Returns:
            Updated news article or None if not found
        """
        news = self.get_by_id(news_id)
        if not news:
            return None
        
        news.views += 1
        self.db.commit()
        self.db.refresh(news)
        return news

