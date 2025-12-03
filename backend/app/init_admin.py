"""
Initialize admin user script.
Creates default admin: admin@admin.com / admin123
"""

from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.models.user import User, UserRole, UserStatus
from app.core.security import get_password_hash
import logging

logger = logging.getLogger(__name__)


def init_admin_user():
    """Create default admin account."""
    db: Session = SessionLocal()
    try:
        # Check if admin account already exists
        existing_admin = db.query(User).filter(
            User.email == "admin@admin.com"
        ).first()
        
        if existing_admin:
            logger.info("Admin account already exists, skipping creation")
            # Update existing account to ensure it's admin role
            if existing_admin.role != UserRole.ADMIN:
                existing_admin.role = UserRole.ADMIN
                existing_admin.status = UserStatus.ACTIVE
                db.commit()
                logger.info("Updated existing account to admin role")
            return
        
        # Create new admin account
        admin_user = User(
            name="Admin",
            email="admin@admin.com",
            password_hash=get_password_hash("admin123"),
            role=UserRole.ADMIN,
            status=UserStatus.ACTIVE
        )
        
        db.add(admin_user)
        db.commit()
        db.refresh(admin_user)
        
        logger.info("Admin account created successfully!")
        logger.info("  Email: admin@admin.com")
        logger.info("  Password: admin123")
        logger.info(f"  Role: {admin_user.role.value}")
        
    except Exception as e:
        logger.error(f"Failed to create admin account: {e}")
        db.rollback()
        raise
    finally:
        db.close()


if __name__ == "__main__":
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    print("Creating default admin account...")
    init_admin_user()
    print("Done!")

