"""Configuration settings for the application."""

from typing import Union
from pydantic import field_validator
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings with environment variable support."""
    
    # Database settings
    DB_HOST: str = "localhost"
    DB_PORT: int = 3306
    DB_USER: str = "root"
    DB_PASSWORD: str = ""
    DB_NAME: str = "studio"
    
    # Security settings
    SECRET_KEY: str = "your-secret-key-change-in-production-please"
    SESSION_SECRET_KEY: str = "your-session-secret-key-change-in-production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # API settings
    API_PREFIX: str = "/api"
    CORS_ORIGINS: Union[str, list[str]] = ["http://localhost:5173", "http://localhost:3000", "http://localhost:8000"]
    
    @field_validator('CORS_ORIGINS', mode='before')
    @classmethod
    def parse_cors_origins(cls, v):
        """Parse CORS_ORIGINS from comma-separated string or list."""
        if isinstance(v, str):
            # Split by comma and strip whitespace
            return [origin.strip() for origin in v.split(',') if origin.strip()]
        return v
    
    # Frontend/Backend URLs
    FRONTEND_URL: str = "http://localhost:5173"
    BACKEND_URL: str = "http://localhost:8000"
    
    # Environment settings
    ENVIRONMENT: str = "development"  # development, staging, production
    DEBUG: bool = False
    
    # Email settings (Gmail)
    SMTP_HOST: str = "smtp.gmail.com"
    SMTP_PORT: int = 587
    SMTP_USER: str = ""  # Gmail address
    SMTP_PASSWORD: str = ""  # Gmail App Password
    SMTP_FROM_EMAIL: str = ""  # From email address (usually same as SMTP_USER)
    SMTP_FROM_NAME: str = "AI-Tracks Studio"
    FEEDBACK_TO_EMAIL: str = ""  # Email address to receive feedback
    
    @property
    def database_url(self) -> str:
        """Construct the database URL."""
        return f"mysql+pymysql://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"
    
    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()

