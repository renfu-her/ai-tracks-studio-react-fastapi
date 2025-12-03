"""Admin user info API."""

from fastapi import APIRouter, Depends
from pydantic import BaseModel
from app.models.user import User
from app.dependencies import require_admin

router = APIRouter(prefix="/api/admin", tags=["admin-auth"])


class UserResponse(BaseModel):
    """User response model."""
    id: int
    name: str
    email: str
    role: str
    status: str
    
    class Config:
        from_attributes = True


@router.get("/me", response_model=UserResponse)
async def get_current_admin(current_user: User = Depends(require_admin)):
    """
    Get current admin user info.
    
    Args:
        current_user: Current authenticated admin
        
    Returns:
        User information
    """
    return UserResponse(
        id=current_user.id,
        name=current_user.name,
        email=current_user.email,
        role=current_user.role.value,
        status=current_user.status.value
    )

