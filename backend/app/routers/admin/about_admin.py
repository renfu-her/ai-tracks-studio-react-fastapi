"""Admin API for managing about us content."""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.dependencies import require_admin
from app.models import AboutUs, User
from app.schemas import AboutUsCreate, AboutUsUpdate, AboutUsResponse

router = APIRouter(prefix="/api/admin/about", tags=["admin-about"])


@router.get("", response_model=list[AboutUsResponse])
async def admin_list_about(
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin)
):
    """List all about us entries (admin)."""
    return db.query(AboutUs).all()


@router.post("", response_model=AboutUsResponse, status_code=201)
async def admin_create_about(
    about: AboutUsCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin)
):
    """Create new about us entry (admin)."""
    db_about = AboutUs(**about.model_dump())
    db.add(db_about)
    db.commit()
    db.refresh(db_about)
    return db_about


@router.put("/{about_id}", response_model=AboutUsResponse)
async def admin_update_about(
    about_id: int,
    about: AboutUsUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin)
):
    """Update about us entry (admin)."""
    db_about = db.query(AboutUs).filter(AboutUs.id == about_id).first()
    if not db_about:
        raise HTTPException(status_code=404, detail="About Us not found")
    
    update_data = about.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_about, field, value)
    
    db.commit()
    db.refresh(db_about)
    return db_about


@router.delete("/{about_id}", status_code=204)
async def admin_delete_about(
    about_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin)
):
    """Delete about us entry (admin)."""
    db_about = db.query(AboutUs).filter(AboutUs.id == about_id).first()
    if not db_about:
        raise HTTPException(status_code=404, detail="About Us not found")
    
    db.delete(db_about)
    db.commit()

