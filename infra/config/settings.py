"""
Configuration settings for the AI-Native PaaS Platform.
"""

import os
from typing import Optional
from pydantic import BaseModel


class Settings(BaseModel):
    """Application settings."""
    
    # Environment
    environment: str = os.getenv("PAAS_ENVIRONMENT", "development")
    debug: bool = os.getenv("PAAS_DEBUG", "false").lower() == "true"
    log_level: str = os.getenv("PAAS_LOG_LEVEL", "INFO")
    
    # API Configuration
    api_host: str = os.getenv("API_HOST", "0.0.0.0")
    api_port: int = int(os.getenv("API_PORT", "8000"))
    api_prefix: str = os.getenv("API_PREFIX", "/api/v1")
    
    # Security
    jwt_secret_key: str = os.getenv("JWT_SECRET_KEY", "your-secret-key-change-in-production")
    jwt_algorithm: str = os.getenv("JWT_ALGORITHM", "HS256")
    jwt_expiration_hours: int = int(os.getenv("JWT_EXPIRATION_HOURS", "24"))
    
    # AWS Configuration
    aws_region: str = os.getenv("AWS_REGION", "us-east-1")
    aws_account_id: Optional[str] = os.getenv("AWS_ACCOUNT_ID")
    
    # Database
    database_url: Optional[str] = os.getenv("DATABASE_URL")
    redis_url: Optional[str] = os.getenv("REDIS_URL")
    
    class Config:
        env_file = ".env"
