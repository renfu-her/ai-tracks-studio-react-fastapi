"""Admin API for managing banners."""

from pathlib import Path
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.dependencies import require_admin
from app.models import User
from app.repositories import BannerRepository
from app.schemas import BannerCreate, BannerUpdate, BannerResponse, BannerListResponse
from app.models.banner import PageTypeEnum

router = APIRouter(prefix="/api/admin/banners", tags=["admin-banners"])

# Upload directory for image deletion
UPLOAD_DIR = Path(__file__).parent.parent.parent.parent / "static" / "uploads"


def get_banner_repo(db: Session = Depends(get_db)) -> BannerRepository:
    """Dependency to get banner repository."""
    return BannerRepository(db)


@router.get("", response_model=BannerListResponse)
async def admin_list_banners(
    skip: int = 0,
    limit: int = 100,
    repo: BannerRepository = Depends(get_banner_repo),
    current_user: User = Depends(require_admin)
):
    """List all banners (admin)."""
    total = repo.count()
    items = repo.get_all(skip=skip, limit=limit)
    return BannerListResponse(total=total, items=items)


@router.get("/{banner_id}", response_model=BannerResponse)
async def admin_get_banner(
    banner_id: str,
    repo: BannerRepository = Depends(get_banner_repo),
    current_user: User = Depends(require_admin)
):
    """Get banner by ID (admin)."""
    banner = repo.get_by_id(banner_id)
    if not banner:
        raise HTTPException(status_code=404, detail="Banner not found")
    return banner


@router.get("/page/{page_type}", response_model=BannerResponse)
async def admin_get_banner_by_page_type(
    page_type: PageTypeEnum,
    repo: BannerRepository = Depends(get_banner_repo),
    current_user: User = Depends(require_admin)
):
    """Get banner by page type (admin)."""
    banner = repo.get_by_page_type(page_type)
    if not banner:
        raise HTTPException(status_code=404, detail=f"Banner for page type {page_type} not found")
    return banner


@router.post("", response_model=BannerResponse, status_code=201)
async def admin_create_banner(
    banner: BannerCreate,
    repo: BannerRepository = Depends(get_banner_repo),
    current_user: User = Depends(require_admin)
):
    """Create new banner (admin)."""
    # Check if banner with same ID exists
    existing = repo.get_by_id(banner.id)
    if existing:
        raise HTTPException(status_code=400, detail="Banner with this ID already exists")
    
    # Check if banner for this page type already exists
    existing_by_page = repo.get_by_page_type(banner.page_type)
    if existing_by_page:
        raise HTTPException(
            status_code=400, 
            detail=f"Banner for page type {banner.page_type} already exists. Please update instead."
        )
    
    return repo.create(banner.model_dump())


@router.put("/{banner_id}", response_model=BannerResponse)
async def admin_update_banner(
    banner_id: str,
    banner: BannerUpdate,
    repo: BannerRepository = Depends(get_banner_repo),
    current_user: User = Depends(require_admin)
):
    """Update banner (admin)."""
    # Get existing banner to delete old image
    existing = repo.get_by_id(banner_id)
    if not existing:
        raise HTTPException(status_code=404, detail="Banner not found")
    
    # If updating image, delete old image file
    if banner.image and existing.image and banner.image != existing.image:
        old_image_path = UPLOAD_DIR / existing.image
        if old_image_path.exists():
            try:
                old_image_path.unlink()
            except Exception as e:
                # Log error but don't fail the update
                print(f"Failed to delete old image {existing.image}: {e}")
    
    updated = repo.update(banner_id, banner.model_dump(exclude_unset=True))
    if not updated:
        raise HTTPException(status_code=404, detail="Banner not found")
    return updated


@router.delete("/{banner_id}", status_code=204)
async def admin_delete_banner(
    banner_id: str,
    repo: BannerRepository = Depends(get_banner_repo),
    current_user: User = Depends(require_admin)
):
    """Delete banner (admin)."""
    # Get banner to delete associated image
    banner = repo.get_by_id(banner_id)
    if not banner:
        raise HTTPException(status_code=404, detail="Banner not found")
    
    # Delete image file
    if banner.image:
        image_path = UPLOAD_DIR / banner.image
        if image_path.exists():
            try:
                image_path.unlink()
            except Exception as e:
                print(f"Failed to delete image {banner.image}: {e}")
    
    success = repo.delete(banner_id)
    if not success:
        raise HTTPException(status_code=404, detail="Banner not found")

