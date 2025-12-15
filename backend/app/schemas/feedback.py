"""Pydantic schemas for Feedback endpoints."""

from datetime import datetime
from pydantic import BaseModel, Field, EmailStr


class FeedbackBase(BaseModel):
    """Base schema for Feedback with common fields."""
    
    name: str = Field(..., min_length=1, max_length=100, description="Sender name")
    email: EmailStr = Field(..., description="Sender email address")
    subject: str | None = Field(None, max_length=255, description="Feedback subject")
    message: str = Field(..., min_length=1, description="Feedback message")


class FeedbackCreate(FeedbackBase):
    """Schema for creating a new feedback (with captcha)."""
    
    captcha_id: str = Field(..., description="Captcha identifier")
    captcha_answer: str = Field(..., description="Captcha answer")


class FeedbackResponse(FeedbackBase):
    """Schema for feedback response."""
    
    id: int
    is_read: bool
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


class FeedbackListResponse(BaseModel):
    """Schema for list of feedback response."""
    
    total: int
    items: list[FeedbackResponse]


class FeedbackUpdate(BaseModel):
    """Schema for updating feedback (admin only)."""
    
    is_read: bool | None = Field(None, description="Mark feedback as read/unread")
