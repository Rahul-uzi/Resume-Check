from pydantic_settings import BaseSettings
from typing import Optional
import os

class Settings(BaseSettings):
    # API Settings
    API_TITLE: str = "Resume Parser API"
    API_VERSION: str = "1.0.0"
    
    # Google API
    GOOGLE_API_KEY: str = os.getenv("GOOGLE_API_KEY", "AIzaSyDB5wQ1ILlr7rv-ID0gEovx-du_eEqJk7U")
    
    # ChromaDB Settings
    CHROMA_DB_PATH: str = "./data/chromadb"
    
    # File Upload Settings
    MAX_FILE_SIZE: int = 10 * 1024 * 1024  # 10MB
    ALLOWED_EXTENSIONS: list = [".pdf", ".docx", ".doc", ".txt"]
    
    # CORS Settings
    CORS_ORIGINS: list = ["*"]
    
    class Config:
        env_file = ".env"
        case_sensitive = True

settings = Settings()
