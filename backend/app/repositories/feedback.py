"""Repository for Feedback operations."""

from sqlalchemy.orm import Session
from app.models import Feedback
from app.repositories.base import BaseRepository


class FeedbackRepository(BaseRepository[Feedback]):
    """Repository for managing Feedback entities."""
    
    def __init__(self, db: Session):
        """
        Initialize feedback repository.
        
        Args:
            db: Database session
        """
        super().__init__(Feedback, db)
    
    def get_unread_count(self) -> int:
        """
        Get count of unread feedback.
        
        Returns:
            Count of unread feedback
        """
        return self.db.query(Feedback).filter(Feedback.is_read == False).count()
    
    def get_unread(self, skip: int = 0, limit: int = 100) -> list[Feedback]:
        """
        Get unread feedback.
        
        Args:
            skip: Number of records to skip
            limit: Maximum number of records to return
            
        Returns:
            List of unread feedback
        """
        return (
            self.db.query(Feedback)
            .filter(Feedback.is_read == False)
            .order_by(Feedback.created_at.desc())
            .offset(skip)
            .limit(limit)
            .all()
        )
