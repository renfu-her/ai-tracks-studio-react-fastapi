"""Base repository with common CRUD operations."""

from typing import Generic, TypeVar, Type
from sqlalchemy.orm import Session
from app.database import Base

ModelType = TypeVar("ModelType", bound=Base)


class BaseRepository(Generic[ModelType]):
    """Base repository with common CRUD operations."""
    
    def __init__(self, model: Type[ModelType], db: Session):
        """
        Initialize repository with model and database session.
        
        Args:
            model: SQLAlchemy model class
            db: Database session
        """
        self.model = model
        self.db = db
    
    def get_by_id(self, id: str | int) -> ModelType | None:
        """
        Get a single record by ID.
        
        Args:
            id: Record identifier
            
        Returns:
            Model instance or None if not found
        """
        return self.db.query(self.model).filter(self.model.id == id).first()
    
    def get_all(self, skip: int = 0, limit: int = 100) -> list[ModelType]:
        """
        Get all records with pagination.
        
        Args:
            skip: Number of records to skip
            limit: Maximum number of records to return
            
        Returns:
            List of model instances
        """
        return self.db.query(self.model).offset(skip).limit(limit).all()
    
    def count(self) -> int:
        """
        Count total records.
        
        Returns:
            Total count of records
        """
        return self.db.query(self.model).count()
    
    def create(self, obj_in: dict) -> ModelType:
        """
        Create a new record.
        
        Args:
            obj_in: Dictionary with record data
            
        Returns:
            Created model instance
        """
        db_obj = self.model(**obj_in)
        self.db.add(db_obj)
        self.db.commit()
        self.db.refresh(db_obj)
        return db_obj
    
    def update(self, id: str | int, obj_in: dict) -> ModelType | None:
        """
        Update an existing record.
        
        Args:
            id: Record identifier
            obj_in: Dictionary with updated data
            
        Returns:
            Updated model instance or None if not found
        """
        db_obj = self.get_by_id(id)
        if not db_obj:
            return None
        
        for field, value in obj_in.items():
            if value is not None:
                setattr(db_obj, field, value)
        
        self.db.commit()
        self.db.refresh(db_obj)
        return db_obj
    
    def delete(self, id: str | int) -> bool:
        """
        Delete a record.
        
        Args:
            id: Record identifier
            
        Returns:
            True if deleted, False if not found
        """
        db_obj = self.get_by_id(id)
        if not db_obj:
            return False
        
        self.db.delete(db_obj)
        self.db.commit()
        return True

