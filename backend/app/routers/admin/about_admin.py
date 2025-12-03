"""Admin API for managing about us content."""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.dependencies import require_admin
from app.models import User
from app.repositories import AboutUsRepository
from app.schemas import AboutUsCreate, AboutUsUpdate, AboutUsResponse

router = APIRouter(prefix="/api/admin/about", tags=["admin-about"])


def get_about_repo(db: Session = Depends(get_db)) -> AboutUsRepository:
    """Dependency to get about us repository."""
    return AboutUsRepository(db)


@router.get("", response_model=list[AboutUsResponse])
async def admin_list_about(
    repo: AboutUsRepository = Depends(get_about_repo),
    current_user: User = Depends(require_admin)
):
    """List all about us entries (admin)."""
    return repo.get_all(skip=0, limit=100)


@router.post("", response_model=AboutUsResponse, status_code=201)
async def admin_create_about(
    about: AboutUsCreate,
    repo: AboutUsRepository = Depends(get_about_repo),
    current_user: User = Depends(require_admin)
):
    """Create new about us entry (admin)."""
    return repo.create(about.model_dump())


@router.put("/{about_id}", response_model=AboutUsResponse)
async def admin_update_about(
    about_id: int,
    about: AboutUsUpdate,
    repo: AboutUsRepository = Depends(get_about_repo),
    current_user: User = Depends(require_admin)
):
    """Update about us entry (admin)."""
    updated = repo.update(about_id, about.model_dump(exclude_unset=True))
    if not updated:
        raise HTTPException(status_code=404, detail="About Us not found")
    return updated


@router.delete("/{about_id}", status_code=204)
async def admin_delete_about(
    about_id: int,
    repo: AboutUsRepository = Depends(get_about_repo),
    current_user: User = Depends(require_admin)
):
    """Delete about us entry (admin)."""
    success = repo.delete(about_id)
    if not success:
        raise HTTPException(status_code=404, detail="About Us not found")

