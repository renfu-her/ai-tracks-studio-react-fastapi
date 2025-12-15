"""Admin profile management APIs."""

from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session

from app.dependencies import get_db, require_admin
from app.models.user import User
from app.core.security import verify_password, get_password_hash


router = APIRouter(prefix="/api/admin/profile", tags=["admin-profile"])


class ProfileResponse(BaseModel):
    """Profile response model (email is read-only)."""

    id: int
    name: str
    email: str
    role: str
    status: str

    class Config:
        from_attributes = True


class ProfileUpdateRequest(BaseModel):
    """Payload for updating profile. Email is immutable."""

    name: Optional[str] = Field(None, description="Display name")
    current_password: Optional[str] = Field(
        None, description="Current password, required when changing password"
    )
    new_password: Optional[str] = Field(
        None, min_length=6, description="New password (min length 6)"
    )


@router.get("", response_model=ProfileResponse)
async def get_profile(current_user: User = Depends(require_admin)) -> ProfileResponse:
    """Return the current admin profile."""
    return ProfileResponse(
        id=current_user.id,
        name=current_user.name,
        email=current_user.email,
        role=current_user.role.value,
        status=current_user.status.value,
    )


@router.put("", response_model=ProfileResponse)
async def update_profile(
    payload: ProfileUpdateRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin),
) -> ProfileResponse:
    """
    Update admin profile.

    - Name can be updated directly.
    - Email is immutable.
    - Password change requires current_password + new_password.
    """
    updated = False

    # Update name if provided
    if payload.name is not None:
        current_user.name = payload.name.strip()
        updated = True

    # Change password if requested
    if payload.new_password:
        if not payload.current_password:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Current password is required to change password",
            )

        if not verify_password(payload.current_password, current_user.password_hash):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Current password is incorrect",
            )

        current_user.password_hash = get_password_hash(payload.new_password)
        updated = True

    if not updated:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No changes provided",
        )

    db.add(current_user)
    db.commit()
    db.refresh(current_user)

    return ProfileResponse(
        id=current_user.id,
        name=current_user.name,
        email=current_user.email,
        role=current_user.role.value,
        status=current_user.status.value,
    )

