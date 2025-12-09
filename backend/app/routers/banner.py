"""Public Banner API endpoints."""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.repositories import BannerRepository
from app.schemas import BannerResponse
from app.models.banner import PageTypeEnum

router = APIRouter(prefix="/api/banners", tags=["banners"])


def get_banner_repo(db: Session = Depends(get_db)) -> BannerRepository:
    """Dependency to get banner repository."""
    return BannerRepository(db)


@router.get("/page/{page_type}", response_model=BannerResponse)
async def get_banner_by_page_type(
    page_type: PageTypeEnum,
    repo: BannerRepository = Depends(get_banner_repo)
):
    """
    Get banner by page type (public endpoint).
    
    Args:
        page_type: Page type (HOME, GAME, WEBSITE, NEWS, ABOUT)
        repo: Banner repository
        
    Returns:
        Banner response
        
    Raises:
        HTTPException: If banner not found
    """
    banner = repo.get_by_page_type(page_type)
    if not banner:
        raise HTTPException(status_code=404, detail=f"Banner for page type {page_type} not found")
    return banner





