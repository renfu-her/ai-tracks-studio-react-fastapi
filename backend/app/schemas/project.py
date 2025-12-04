"""Pydantic schemas for Project endpoints."""

from datetime import date as Date, datetime
from pydantic import BaseModel, Field
from app.models.project import CategoryEnum


class ProjectBase(BaseModel):
    """Base schema for Project with common fields."""
    
    title: str = Field(..., max_length=255, description="Project title")
    description: str | None = Field(None, description="Project description")
    image: str | None = Field(None, max_length=500, description="Project image filename")
    category: CategoryEnum = Field(..., description="Project category (GAME or WEBSITE)")
    date: Date | None = Field(None, description="Project date")
    tags: list[str] | None = Field(default_factory=list, description="Project tags")
    link: str | None = Field(None, max_length=500, description="External link to project")


class ProjectCreate(ProjectBase):
    """Schema for creating a new project."""
    
    id: str = Field(..., max_length=50, description="Unique project identifier")


class ProjectUpdate(ProjectBase):
    """Schema for updating an existing project."""
    
    title: str | None = Field(None, max_length=255, description="Project title")
    category: CategoryEnum | None = Field(None, description="Project category")


class ProjectResponse(ProjectBase):
    """Schema for project response."""
    
    id: str
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


class ProjectListResponse(BaseModel):
    """Schema for list of projects response."""
    
    total: int
    items: list[ProjectResponse]

