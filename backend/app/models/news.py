"""News model for articles and updates."""

from datetime import datetime
from sqlalchemy import Column, String, Text, Date, DateTime
from sqlalchemy.dialects.mysql import LONGTEXT
from app.database import Base


class News(Base):
    """News model representing articles and updates."""
    
    __tablename__ = "news"
    
    id = Column(String(50), primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    excerpt = Column(LONGTEXT, nullable=True)
    content = Column(LONGTEXT, nullable=True)
    date = Column(Date, nullable=True)
    image_url = Column(String(500), nullable=True)
    author = Column(String(100), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    def __repr__(self) -> str:
        """String representation of the news article."""
        return f"<News(id={self.id}, title={self.title}, author={self.author})>"

