"""Pydantic schemas for Banner endpoints."""

from datetime import datetime
from pydantic import BaseModel, Field
from app.models.banner import PageTypeEnum


class BannerBase(BaseModel):
    """Base schema for Banner with common fields."""
    
    page_type: PageTypeEnum = Field(..., description="Page type (HOME, GAME, WEBSITE, NEWS, ABOUT)")
    image: str = Field(..., max_length=500, description="Banner image filename")


class BannerCreate(BannerBase):
    """Schema for creating a new banner."""
    
    id: str = Field(..., max_length=50, description="Unique banner identifier")


class BannerUpdate(BaseModel):
    """Schema for updating an existing banner."""
    
    image: str | None = Field(None, max_length=500, description="Banner image filename")


class BannerResponse(BannerBase):
    """Schema for banner response."""
    
    id: str
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


class BannerListResponse(BaseModel):
    """Schema for list of banners response."""
    
    total: int
    items: list[BannerResponse]

