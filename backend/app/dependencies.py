"""Dependency functions for FastAPI."""

from typing import Optional
from fastapi import Depends, HTTPException, status, Request
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.models.user import User, UserRole
from app.core.security import decode_access_token


def get_db():
    """
    Database session dependency.
    
    Yields:
        Database session
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_current_user_from_session(
    request: Request,
    db: Session = Depends(get_db)
) -> Optional[User]:
    """
    Get current user from session.
    
    Args:
        request: FastAPI request object
        db: Database session
        
    Returns:
        Current user or None
    """
    user_id = request.session.get("user_id")
    if not user_id:
        return None
    
    user = db.query(User).filter(User.id == user_id).first()
    return user


def require_admin(
    request: Request,
    db: Session = Depends(get_db)
) -> User:
    """
    Require admin authentication.
    
    Args:
        request: FastAPI request object
        db: Database session
        
    Returns:
        Admin user
        
    Raises:
        HTTPException: If not authenticated or not admin
    """
    user = get_current_user_from_session(request, db)
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated"
        )
    
    if user.role != UserRole.ADMIN:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions"
        )
    
    return user

