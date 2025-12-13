"""Repositories package initialization."""

from app.repositories.base import BaseRepository
from app.repositories.project import ProjectRepository
from app.repositories.news import NewsRepository
from app.repositories.about import AboutUsRepository
from app.repositories.banner import BannerRepository
from app.repositories.feedback import FeedbackRepository

__all__ = [
    "BaseRepository",
    "ProjectRepository",
    "NewsRepository",
    "AboutUsRepository",
    "BannerRepository",
    "FeedbackRepository",
]

