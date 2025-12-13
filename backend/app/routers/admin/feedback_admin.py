"""Admin API routes for feedback management."""

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.database import get_db
from app.dependencies import require_admin
from app.repositories import FeedbackRepository
from app.schemas import (
    FeedbackResponse,
    FeedbackListResponse,
    FeedbackUpdate,
)

router = APIRouter(prefix="/feedback", tags=["admin-feedback"])


def get_feedback_repo(db: Session = Depends(get_db)) -> FeedbackRepository:
    """Dependency to get feedback repository."""
    return FeedbackRepository(db)


@router.get("", response_model=FeedbackListResponse)
def list_feedback(
    skip: int = Query(0, ge=0, description="Number of items to skip"),
    limit: int = Query(100, ge=1, le=100, description="Number of items to return"),
    unread_only: bool = Query(False, description="Show only unread feedback"),
    repo: FeedbackRepository = Depends(get_feedback_repo),
    _: None = Depends(require_admin),
):
    """
    Get list of feedback (admin only).
    
    Args:
        skip: Number of items to skip for pagination
        limit: Maximum number of items to return
        unread_only: If True, return only unread feedback
        repo: Feedback repository instance
        
    Returns:
        List of feedback with total count
    """
    if unread_only:
        items = repo.get_unread(skip=skip, limit=limit)
        total = repo.get_unread_count()
    else:
        items = repo.get_all(skip=skip, limit=limit)
        total = repo.count()
    
    return FeedbackListResponse(total=total, items=items)


@router.get("/{feedback_id}", response_model=FeedbackResponse)
def get_feedback(
    feedback_id: int,
    repo: FeedbackRepository = Depends(get_feedback_repo),
    _: None = Depends(require_admin),
):
    """
    Get a single feedback by ID (admin only).
    
    Args:
        feedback_id: Feedback identifier
        repo: Feedback repository instance
        
    Returns:
        Feedback details
        
    Raises:
        HTTPException: If feedback not found
    """
    feedback = repo.get_by_id(feedback_id)
    if not feedback:
        raise HTTPException(status_code=404, detail="Feedback not found")
    return feedback


@router.put("/{feedback_id}", response_model=FeedbackResponse)
def update_feedback(
    feedback_id: int,
    feedback_in: FeedbackUpdate,
    repo: FeedbackRepository = Depends(get_feedback_repo),
    _: None = Depends(require_admin),
):
    """
    Update feedback (admin only, e.g., mark as read/unread).
    
    Args:
        feedback_id: Feedback identifier
        feedback_in: Updated feedback data
        repo: Feedback repository instance
        
    Returns:
        Updated feedback
        
    Raises:
        HTTPException: If feedback not found
    """
    feedback = repo.update(feedback_id, feedback_in.model_dump(exclude_unset=True))
    if not feedback:
        raise HTTPException(status_code=404, detail="Feedback not found")
    return feedback


@router.delete("/{feedback_id}", status_code=204)
def delete_feedback(
    feedback_id: int,
    repo: FeedbackRepository = Depends(get_feedback_repo),
    _: None = Depends(require_admin),
):
    """
    Delete feedback (admin only).
    
    Args:
        feedback_id: Feedback identifier
        repo: Feedback repository instance
        
    Raises:
        HTTPException: If feedback not found
    """
    success = repo.delete(feedback_id)
    if not success:
        raise HTTPException(status_code=404, detail="Feedback not found")


@router.get("/stats/unread-count", response_model=dict)
def get_unread_count(
    repo: FeedbackRepository = Depends(get_feedback_repo),
    _: None = Depends(require_admin),
):
    """
    Get count of unread feedback (admin only).
    
    Args:
        repo: Feedback repository instance
        
    Returns:
        Dictionary with unread_count
    """
    count = repo.get_unread_count()
    return {"unread_count": count}
