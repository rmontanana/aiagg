import os
from pydantic import BaseModel, PostgresDsn, field_validator
from pydantic_settings import BaseSettings
from typing import Any, Dict, Optional


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""
    
    # Application
    PROJECT_NAME: str = "AI News Aggregator"
    VERSION: str = "1.0.0"
    ENVIRONMENT: str = "development"
    DEBUG: bool = True
    
    # Security
    SECRET_KEY: str = "default-secret-key-change-in-production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # Database
    DATABASE_URL: PostgresDsn = "postgresql://postgres:postgres@localhost:5432/aiagg"
    
    # Redis
    REDIS_URL: str = "redis://localhost:6379"
    
    # OpenAI
    OPENAI_API_KEY: str = "test-openai-key"
    
    # Logging
    LOG_LEVEL: str = "INFO"
    
    # CORS
    BACKEND_CORS_ORIGINS: list[str] = ["http://localhost:3000", "http://localhost:8000"]
    
    @field_validator("BACKEND_CORS_ORIGINS", mode="before")
    @classmethod
    def assemble_cors_origins(cls, v: str | list[str]) -> list[str]:
        if isinstance(v, str) and not v.startswith("["):
            return [i.strip() for i in v.split(",")]
        elif isinstance(v, (list, str)):
            return v
        raise ValueError(v)
    
    model_config = {
        "env_file": ".env.test" if os.getenv("ENVIRONMENT") == "test" else ".env",
        "case_sensitive": True,
    }


# Global settings instance
settings = Settings()