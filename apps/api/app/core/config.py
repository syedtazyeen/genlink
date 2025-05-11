from enum import Enum
from pydantic import EmailStr
from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict

class EnvironmentType(str, Enum):
    DEVELOPMENT = "development"
    PRODUCTION = "production"


class Settings(BaseSettings):
    """
    Settings for the application.
    """

    API_V1_STR: str = "/api/v1"
    DATABASE_URL: str  = "mongodb://localhost:27017"
    DATABASE_NAME: str  = "fastapi"
    SECRET_KEY: str  = "secret-key"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60

    # Server settings
    ENVIRONMENT: EnvironmentType = EnvironmentType.DEVELOPMENT
    WORKERS: int = 4
    PORT: int = 8000
    LOG_LEVEL: str = "debug"
    
    # Application Settings
    APP_NAME: str = "Genlink"
    APP_SECRET_KEY: str = "secret-key"
    PASSWORD_RESET_CODE_EXPIRE_MINUTES: int = 15
    EMAIL_VERIFICATION_CODE_EXPIRE_MINUTES: int = 15
    
    # SMTP server settings
    SMTP_HOST: str = "smtp.gmail.com"
    SMTP_PORT: int = 587
    SMTP_USERNAME: str
    SMTP_PASSWORD: str
    SMTP_SENDER_EMAIL: EmailStr
    SMTP_USE_TLS: bool = True
    
    # Google OAuth settings
    GOOGLE_CLIENT_ID: str
    GOOGLE_CLIENT_SECRET: str
    GOOGLE_REDIRECT_URI: str
    GOOGLE_REDIRECT_FRONTEND_URL: str

    model_config = SettingsConfigDict(
        env_file=".env", use_enum_values=True, extra="ignore"
    )


@lru_cache()
def get_config() -> Settings:
    return Settings()
