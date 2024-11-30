import os
from dotenv import load_dotenv
from pydantic import BaseSettings

load_dotenv()

class Settings(BaseSettings):
    # Database Configuration
    DATABASE_URL: str = os.getenv('DATABASE_URL', 'postgresql+asyncpg://user:password@localhost/hushh_db')
    
    # OpenAI API Configuration
    OPENAI_API_KEY: str = os.getenv('OPENAI_API_KEY', '')
    
    # Local ML Model Path
    LOCAL_MODEL_PATH: str = os.getenv('LOCAL_MODEL_PATH', './models/local_llm')
    
    # Security Settings
    SECRET_KEY: str = os.getenv('SECRET_KEY', 'your-secret-key')
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # Logging Configuration
    LOG_LEVEL: str = os.getenv('LOG_LEVEL', 'INFO')
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

settings = Settings()