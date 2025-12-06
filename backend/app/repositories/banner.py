"""Repository for Banner operations."""

from sqlalchemy.orm import Session
from app.models.banner import Banner, PageTypeEnum
from app.repositories.base import BaseRepository


class BannerRepository(BaseRepository[Banner]):
    """Repository for managing Banner entities."""
    
    def __init__(self, db: Session):
        """
        Initialize banner repository.
        
        Args:
            db: Database session
        """
        super().__init__(Banner, db)
    
    def get_by_page_type(self, page_type: PageTypeEnum) -> Banner | None:
        """
        Get banner by page type.
        
        Args:
            page_type: Page type (HOME, GAME, WEBSITE, NEWS, ABOUT)
            
        Returns:
            Banner instance or None if not found
        """
        return self.db.query(Banner).filter(Banner.page_type == page_type).first()

