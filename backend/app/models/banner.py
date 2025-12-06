"""Banner model for page banners."""

from datetime import datetime
from sqlalchemy import Column, String, Enum, DateTime
from app.database import Base
import enum


class PageTypeEnum(str, enum.Enum):
    """Page type enumeration for banners."""
    
    HOME = "HOME"
    GAME = "GAME"
    WEBSITE = "WEBSITE"
    NEWS = "NEWS"
    ABOUT = "ABOUT"


class Banner(Base):
    """Banner model representing page banners."""
    
    __tablename__ = "banners"
    
    id = Column(String(50), primary_key=True, index=True)
    page_type = Column(Enum(PageTypeEnum), nullable=False, unique=True)
    image = Column(String(500), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    def __repr__(self) -> str:
        """String representation of the banner."""
        return f"<Banner(id={self.id}, page_type={self.page_type}, image={self.image})>"

