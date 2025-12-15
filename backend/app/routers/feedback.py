"""API routes for feedback (public submission)."""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.repositories import FeedbackRepository
from app.schemas import FeedbackCreate, FeedbackResponse
from app.core.email import email_service
from app.core.captcha import generate_captcha, validate_captcha
from pydantic import BaseModel

router = APIRouter(prefix="/feedback", tags=["feedback"])


def get_feedback_repo(db: Session = Depends(get_db)) -> FeedbackRepository:
    """Dependency to get feedback repository."""
    return FeedbackRepository(db)


class CaptchaResponse(BaseModel):
    """Response model for captcha generation."""

    captcha_id: str
    image_base64: str


@router.get("/captcha", response_model=CaptchaResponse)
def get_feedback_captcha() -> CaptchaResponse:
    """Generate a new captcha for feedback form."""
    captcha_id, image_base64 = generate_captcha()
    return CaptchaResponse(captcha_id=captcha_id, image_base64=image_base64)


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
    # Validate captcha
    try:
        validate_captcha(
            captcha_id=feedback_in.captcha_id,
            answer=feedback_in.captcha_answer,
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    # Remove captcha fields before persistence
    payload = feedback_in.model_dump(exclude={"captcha_id", "captcha_answer"})

    # Create feedback in database
    feedback = repo.create(payload)
    
    # Send email notification (non-blocking, failures are logged but don't affect response)
    try:
        email_service.send_feedback_notification(
            name=feedback.name,
            email=feedback.email,
            subject=feedback.subject,
            message=feedback.message
        )
    except Exception as e:
        # Log error but don't fail the request
        import logging
        logger = logging.getLogger(__name__)
        logger.error(f"Failed to send feedback email: {str(e)}")
    
    return feedback
