"""About Us model for dynamic content management."""

from datetime import datetime
from sqlalchemy import Column, Integer, String, Text, JSON, DateTime
from sqlalchemy.dialects.mysql import LONGTEXT
from app.database import Base


class AboutUs(Base):
    """AboutUs model for managing About page content."""
    
    __tablename__ = "about_us"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(255), nullable=True)
    subtitle = Column(LONGTEXT, nullable=True)
    description = Column(LONGTEXT, nullable=True)
    image = Column(String(500), nullable=True)
    contact_email = Column(String(255), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    def __repr__(self) -> str:
        """String representation of the about us entry."""
        return f"<AboutUs(id={self.id}, title={self.title})>"

