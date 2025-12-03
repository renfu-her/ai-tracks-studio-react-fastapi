"""Repositories package initialization."""

from app.repositories.base import BaseRepository
from app.repositories.project import ProjectRepository
from app.repositories.news import NewsRepository
from app.repositories.about import AboutUsRepository

__all__ = [
    "BaseRepository",
    "ProjectRepository",
    "NewsRepository",
    "AboutUsRepository",
]

