"""Repository for About Us operations."""

from sqlalchemy.orm import Session
from app.models import AboutUs
from app.repositories.base import BaseRepository


class AboutUsRepository(BaseRepository[AboutUs]):
    """Repository for managing About Us content."""
    
    def __init__(self, db: Session):
        """
        Initialize about us repository.
        
        Args:
            db: Database session
        """
        super().__init__(AboutUs, db)
    
    def get_latest(self) -> AboutUs | None:
        """
        Get the most recent about us entry.
        
        Returns:
            Latest AboutUs instance or None
        """
        return (
            self.db.query(AboutUs)
            .order_by(AboutUs.updated_at.desc())
            .first()
        )
    
    def increment_views(self, about_id: int) -> AboutUs | None:
        """
        Increment view count for about us content.
        
        Args:
            about_id: About Us identifier
            
        Returns:
            Updated about us content or None if not found
        """
        about = self.get_by_id(about_id)
        if not about:
            return None
        
        about.views += 1
        self.db.commit()
        self.db.refresh(about)
        return about

