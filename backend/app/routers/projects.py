"""API routes for projects (games and websites)."""

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import CategoryEnum
from app.repositories import ProjectRepository
from app.schemas import (
    ProjectCreate,
    ProjectUpdate,
    ProjectResponse,
    ProjectListResponse,
)

router = APIRouter(prefix="/projects", tags=["projects"])


def get_project_repo(db: Session = Depends(get_db)) -> ProjectRepository:
    """Dependency to get project repository."""
    return ProjectRepository(db)


@router.get("", response_model=ProjectListResponse)
def list_projects(
    category: CategoryEnum | None = Query(None, description="Filter by category"),
    skip: int = Query(0, ge=0, description="Number of items to skip"),
    limit: int = Query(100, ge=1, le=100, description="Number of items to return"),
    repo: ProjectRepository = Depends(get_project_repo),
):
    """
    Get list of projects with optional category filter.
    
    Args:
        category: Optional category filter (GAME or WEBSITE)
        skip: Number of items to skip for pagination
        limit: Maximum number of items to return
        repo: Project repository instance
        
    Returns:
        List of projects with total count
    """
    if category:
        items = repo.get_by_category(category, skip=skip, limit=limit)
        total = repo.count_by_category(category)
    else:
        items = repo.get_all(skip=skip, limit=limit)
        total = repo.count()
    
    return ProjectListResponse(total=total, items=items)


@router.get("/{project_id}", response_model=ProjectResponse)
def get_project(
    project_id: str,
    repo: ProjectRepository = Depends(get_project_repo),
):
    """
    Get a single project by ID.
    
    Args:
        project_id: Project identifier
        repo: Project repository instance
        
    Returns:
        Project details
        
    Raises:
        HTTPException: If project not found
    """
    project = repo.get_by_id(project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    return project


@router.post("", response_model=ProjectResponse, status_code=201)
def create_project(
    project_in: ProjectCreate,
    repo: ProjectRepository = Depends(get_project_repo),
):
    """
    Create a new project.
    
    Args:
        project_in: Project data
        repo: Project repository instance
        
    Returns:
        Created project
        
    Raises:
        HTTPException: If project with same ID already exists
    """
    existing = repo.get_by_id(project_in.id)
    if existing:
        raise HTTPException(status_code=400, detail="Project with this ID already exists")
    
    return repo.create(project_in.model_dump())


@router.put("/{project_id}", response_model=ProjectResponse)
def update_project(
    project_id: str,
    project_in: ProjectUpdate,
    repo: ProjectRepository = Depends(get_project_repo),
):
    """
    Update an existing project.
    
    Args:
        project_id: Project identifier
        project_in: Updated project data
        repo: Project repository instance
        
    Returns:
        Updated project
        
    Raises:
        HTTPException: If project not found
    """
    project = repo.update(project_id, project_in.model_dump(exclude_unset=True))
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    return project


@router.delete("/{project_id}", status_code=204)
def delete_project(
    project_id: str,
    repo: ProjectRepository = Depends(get_project_repo),
):
    """
    Delete a project.
    
    Args:
        project_id: Project identifier
        repo: Project repository instance
        
    Raises:
        HTTPException: If project not found
    """
    success = repo.delete(project_id)
    if not success:
        raise HTTPException(status_code=404, detail="Project not found")

