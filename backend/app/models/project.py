"""Project model for games and websites."""

from datetime import datetime
from sqlalchemy import Column, String, Text, Date, Enum, JSON, DateTime
from sqlalchemy.dialects.mysql import LONGTEXT
from app.database import Base
import enum


class CategoryEnum(str, enum.Enum):
    """Project category enumeration."""
    
    GAME = "GAME"
    WEBSITE = "WEBSITE"


class Project(Base):
    """Project model representing games and websites."""
    
    __tablename__ = "projects"
    
    id = Column(String(50), primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    description = Column(LONGTEXT, nullable=True)
    image = Column(String(500), nullable=True)
    category = Column(Enum(CategoryEnum), nullable=False)
    date = Column(Date, nullable=True)
    tags = Column(JSON, nullable=True, default=list)
    link = Column(String(500), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    def __repr__(self) -> str:
        """String representation of the project."""
        return f"<Project(id={self.id}, title={self.title}, category={self.category})>"

