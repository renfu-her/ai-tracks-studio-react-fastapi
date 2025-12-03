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

