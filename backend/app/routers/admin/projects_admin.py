"""Admin API for managing projects."""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.dependencies import require_admin
from app.models import User
from app.repositories import ProjectRepository
from app.schemas import ProjectCreate, ProjectUpdate, ProjectResponse, ProjectListResponse

router = APIRouter(prefix="/api/admin/projects", tags=["admin-projects"])


def get_project_repo(db: Session = Depends(get_db)) -> ProjectRepository:
    """Dependency to get project repository."""
    return ProjectRepository(db)


@router.get("", response_model=ProjectListResponse)
async def admin_list_projects(
    skip: int = 0,
    limit: int = 100,
    repo: ProjectRepository = Depends(get_project_repo),
    current_user: User = Depends(require_admin)
):
    """List all projects (admin)."""
    total = repo.count()
    items = repo.get_all(skip=skip, limit=limit)
    return ProjectListResponse(total=total, items=items)


@router.get("/{project_id}", response_model=ProjectResponse)
async def admin_get_project(
    project_id: str,
    repo: ProjectRepository = Depends(get_project_repo),
    current_user: User = Depends(require_admin)
):
    """Get project by ID (admin)."""
    project = repo.get_by_id(project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    return project


@router.post("", response_model=ProjectResponse, status_code=201)
async def admin_create_project(
    project: ProjectCreate,
    repo: ProjectRepository = Depends(get_project_repo),
    current_user: User = Depends(require_admin)
):
    """Create new project (admin)."""
    # Check if project with same ID exists
    existing = repo.get_by_id(project.id)
    if existing:
        raise HTTPException(status_code=400, detail="Project with this ID already exists")
    
    return repo.create(project.model_dump())


@router.put("/{project_id}", response_model=ProjectResponse)
async def admin_update_project(
    project_id: str,
    project: ProjectUpdate,
    repo: ProjectRepository = Depends(get_project_repo),
    current_user: User = Depends(require_admin)
):
    """Update project (admin)."""
    updated = repo.update(project_id, project.model_dump(exclude_unset=True))
    if not updated:
        raise HTTPException(status_code=404, detail="Project not found")
    return updated


@router.delete("/{project_id}", status_code=204)
async def admin_delete_project(
    project_id: str,
    repo: ProjectRepository = Depends(get_project_repo),
    current_user: User = Depends(require_admin)
):
    """Delete project (admin)."""
    success = repo.delete(project_id)
    if not success:
        raise HTTPException(status_code=404, detail="Project not found")

