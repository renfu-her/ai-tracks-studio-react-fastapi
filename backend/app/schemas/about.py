"""Pydantic schemas for About Us endpoints."""

from datetime import datetime
from pydantic import BaseModel, Field


class AboutUsBase(BaseModel):
    """Base schema for About Us with common fields."""
    
    title: str | None = Field(None, max_length=255, description="About page title")
    subtitle: str | None = Field(None, description="About page subtitle")
    description: str | None = Field(None, description="About page description")
    image: str | None = Field(None, max_length=500, description="About image filename")
    contact_email: str | None = Field(None, max_length=255, description="Contact email")
    views: int = Field(0, description="View count")


class AboutUsCreate(AboutUsBase):
    """Schema for creating about us content."""
    pass


class AboutUsUpdate(AboutUsBase):
    """Schema for updating about us content."""
    pass


class AboutUsResponse(AboutUsBase):
    """Schema for about us response."""
    
    id: int
    views: int
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True

