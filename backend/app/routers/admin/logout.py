"""Admin logout API."""

from fastapi import APIRouter, Request
from pydantic import BaseModel

router = APIRouter(prefix="/api/admin", tags=["admin-auth"])


class LogoutResponse(BaseModel):
    """Logout response model."""
    success: bool
    message: str


@router.post("/logout", response_model=LogoutResponse)
async def admin_logout(request: Request):
    """
    Admin logout endpoint.
    
    Args:
        request: FastAPI request
        
    Returns:
        Logout response
    """
    # Clear session
    request.session.clear()
    
    return LogoutResponse(
        success=True,
        message="Logout successful"
    )

