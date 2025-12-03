"""Pydantic schemas for About Us endpoints."""

from datetime import datetime
from pydantic import BaseModel, Field


class ValueItem(BaseModel):
    """Schema for a value item in About Us."""
    
    icon: str = Field(..., description="Icon identifier (e.g., 'Star', 'Zap')")
    title: str = Field(..., description="Value title")
    description: str = Field(..., description="Value description")


class AboutUsBase(BaseModel):
    """Base schema for About Us with common fields."""
    
    title: str | None = Field(None, max_length=255, description="About page title")
    subtitle: str | None = Field(None, description="About page subtitle")
    description: str | None = Field(None, description="About page description")
    values: list[ValueItem] | None = Field(default_factory=list, description="Company values")
    contact_email: str | None = Field(None, max_length=255, description="Contact email")


class AboutUsCreate(AboutUsBase):
    """Schema for creating about us content."""
    pass


class AboutUsUpdate(AboutUsBase):
    """Schema for updating about us content."""
    pass


class AboutUsResponse(AboutUsBase):
    """Schema for about us response."""
    
    id: int
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True

