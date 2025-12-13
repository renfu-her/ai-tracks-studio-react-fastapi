"""Repository for Project operations."""

from sqlalchemy.orm import Session
from app.models import Project, CategoryEnum
from app.repositories.base import BaseRepository


class ProjectRepository(BaseRepository[Project]):
    """Repository for managing Project entities."""
    
    def __init__(self, db: Session):
        """
        Initialize project repository.
        
        Args:
            db: Database session
        """
        super().__init__(Project, db)
    
    def get_by_category(
        self, 
        category: CategoryEnum, 
        skip: int = 0, 
        limit: int = 100
    ) -> list[Project]:
        """
        Get projects filtered by category.
        
        Args:
            category: Project category (GAME or WEBSITE)
            skip: Number of records to skip
            limit: Maximum number of records to return
            
        Returns:
            List of projects in the specified category
        """
        return (
            self.db.query(Project)
            .filter(Project.category == category)
            .offset(skip)
            .limit(limit)
            .all()
        )
    
    def count_by_category(self, category: CategoryEnum) -> int:
        """
        Count projects by category.
        
        Args:
            category: Project category
            
        Returns:
            Count of projects in category
        """
        return self.db.query(Project).filter(Project.category == category).count()
    
    def increment_views(self, project_id: str) -> Project | None:
        """
        Increment view count for a project.
        
        Args:
            project_id: Project identifier
            
        Returns:
            Updated project or None if not found
        """
        project = self.get_by_id(project_id)
        if not project:
            return None
        
        project.views += 1
        self.db.commit()
        self.db.refresh(project)
        return project

