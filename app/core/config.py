# app/core/config.py

from pydantic import BaseSettings

class Settings(BaseSettings):
    DATABASE_URL: str = "sqlite:///./students.db"
    PROJECT_NAME: str = "Student Performance API"
    VERSION: str = "1.0.0"
    DEBUG: bool = True

    class Config:
        case_sensitive = True

settings = Settings()
