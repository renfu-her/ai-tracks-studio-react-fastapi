"""API routes for feedback (public submission)."""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.repositories import FeedbackRepository
from app.schemas import FeedbackCreate, FeedbackResponse
from app.core.email import email_service

router = APIRouter(prefix="/feedback", tags=["feedback"])


def get_feedback_repo(db: Session = Depends(get_db)) -> FeedbackRepository:
    """Dependency to get feedback repository."""
    return FeedbackRepository(db)


@router.post("", response_model=FeedbackResponse, status_code=201)
def create_feedback(
    feedback_in: FeedbackCreate,
    repo: FeedbackRepository = Depends(get_feedback_repo),
):
    """
    Create a new feedback submission.
    
    Args:
        feedback_in: Feedback data
        repo: Feedback repository instance
        
    Returns:
        Created feedback
        
    Note:
        This endpoint sends an email notification to the configured email address.
    """
    # Create feedback in database
    feedback = repo.create(feedback_in.model_dump())
    
    # Send email notification (non-blocking, failures are logged but don't affect response)
    try:
        email_service.send_feedback_notification(
            name=feedback_in.name,
            email=feedback_in.email,
            subject=feedback_in.subject,
            message=feedback_in.message
        )
    except Exception as e:
        # Log error but don't fail the request
        import logging
        logger = logging.getLogger(__name__)
        logger.error(f"Failed to send feedback email: {str(e)}")
    
    return feedback
