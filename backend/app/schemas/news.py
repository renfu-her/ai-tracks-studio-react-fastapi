"""Pydantic schemas for News endpoints."""

from datetime import date as Date, datetime
from pydantic import BaseModel, Field


class NewsBase(BaseModel):
    """Base schema for News with common fields."""
    
    title: str = Field(..., max_length=255, description="News title")
    excerpt: str | None = Field(None, description="News excerpt")
    content: str | None = Field(None, description="News full content")
    date: Date | None = Field(None, description="News publication date")
    image: str | None = Field(None, max_length=500, description="News image filename")
    author: str | None = Field(None, max_length=100, description="Author name")
    views: int = Field(0, description="View count")


class NewsCreate(NewsBase):
    """Schema for creating a new news article."""
    
    id: str = Field(..., max_length=50, description="Unique news identifier")


class NewsUpdate(NewsBase):
    """Schema for updating an existing news article."""
    
    title: str | None = Field(None, max_length=255, description="News title")


class NewsResponse(NewsBase):
    """Schema for news response."""
    
    id: str
    views: int
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


class NewsListResponse(BaseModel):
    """Schema for list of news response."""
    
    total: int
    items: list[NewsResponse]

