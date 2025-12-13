"""API routes for About Us content."""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.repositories import AboutUsRepository
from app.schemas import (
    AboutUsCreate,
    AboutUsUpdate,
    AboutUsResponse,
)

router = APIRouter(prefix="/about", tags=["about"])


def get_about_repo(db: Session = Depends(get_db)) -> AboutUsRepository:
    """Dependency to get about us repository."""
    return AboutUsRepository(db)


@router.get("", response_model=AboutUsResponse)
def get_about_us(
    repo: AboutUsRepository = Depends(get_about_repo),
):
    """
    Get the current About Us content.
    
    Args:
        repo: About Us repository instance
        
    Returns:
        About Us content
        
    Raises:
        HTTPException: If no content exists
    """
    about = repo.get_latest()
    if not about:
        raise HTTPException(status_code=404, detail="About Us content not found")
    return about


@router.get("/{about_id}", response_model=AboutUsResponse)
def get_about_us_by_id(
    about_id: int,
    repo: AboutUsRepository = Depends(get_about_repo),
):
    """
    Get specific About Us content by ID.
    
    Args:
        about_id: About Us identifier
        repo: About Us repository instance
        
    Returns:
        About Us content
        
    Raises:
        HTTPException: If content not found
    """
    about = repo.get_by_id(about_id)
    if not about:
        raise HTTPException(status_code=404, detail="About Us content not found")
    return about


@router.post("", response_model=AboutUsResponse, status_code=201)
def create_about_us(
    about_in: AboutUsCreate,
    repo: AboutUsRepository = Depends(get_about_repo),
):
    """
    Create new About Us content.
    
    Args:
        about_in: About Us data
        repo: About Us repository instance
        
    Returns:
        Created About Us content
    """
    return repo.create(about_in.model_dump())


@router.put("/{about_id}", response_model=AboutUsResponse)
def update_about_us(
    about_id: int,
    about_in: AboutUsUpdate,
    repo: AboutUsRepository = Depends(get_about_repo),
):
    """
    Update existing About Us content.
    
    Args:
        about_id: About Us identifier
        about_in: Updated About Us data
        repo: About Us repository instance
        
    Returns:
        Updated About Us content
        
    Raises:
        HTTPException: If content not found
    """
    about = repo.update(about_id, about_in.model_dump(exclude_unset=True))
    if not about:
        raise HTTPException(status_code=404, detail="About Us content not found")
    return about


@router.delete("/{about_id}", status_code=204)
def delete_about_us(
    about_id: int,
    repo: AboutUsRepository = Depends(get_about_repo),
):
    """
    Delete About Us content.
    
    Args:
        about_id: About Us identifier
        repo: About Us repository instance
        
    Raises:
        HTTPException: If content not found
    """
    success = repo.delete(about_id)
    if not success:
        raise HTTPException(status_code=404, detail="About Us content not found")


@router.post("/{about_id}/view", response_model=AboutUsResponse)
def increment_about_views(
    about_id: int,
    repo: AboutUsRepository = Depends(get_about_repo),
):
    """
    Increment view count for About Us content.
    
    Args:
        about_id: About Us identifier
        repo: About Us repository instance
        
    Returns:
        Updated About Us content with incremented views
        
    Raises:
        HTTPException: If content not found
    """
    about = repo.increment_views(about_id)
    if not about:
        raise HTTPException(status_code=404, detail="About Us content not found")
    return about

