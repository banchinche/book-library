import secrets
from typing import List, Optional
from pydantic import AnyHttpUrl, BaseSettings, EmailStr


class Settings(BaseSettings):
    API_V1: str = '/api/v1'
    APP_NAME: str
    SECRET_KEY: str = secrets.token_urlsafe(32)

    # DATABASE
    POSTGRES_SERVER: str
    POSTGRES_PORT: str
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DATABASE: str

    @classmethod
    def database_uri(cls) -> Optional[str]:
        return f'postgresql+asyncpg://{cls.POSTGRES_USER}:{cls.POSTGRES_PASSWORD}' \
               f'@{cls.POSTGRES_SERVER}:{cls.POSTGRES_PORT}/{cls.POSTGRES_DATABASE}'

    # MAIL AGENT
    SMTP_TLS: bool = True
    SMTP_PORT: Optional[int] = None
    SMTP_HOST: Optional[str] = None
    SMTP_USER: Optional[str] = None
    SMTP_PASSWORD: Optional[str] = None

    EMAILS_FROM_EMAIL: Optional[EmailStr] = None
    EMAILS_FROM_NAME: Optional[str] = None

    EMAIL_TEMPLATES_DIRECTORY: str = '/app/app/core/email-templates'
    EMAIL_TEST_USER: EmailStr = 'test@example.com'

    # SUPERUSER
    MAIN_SUPERUSER: EmailStr
    MAIN_SUPERUSER_PASSWORD: str

    # JWT
    ACCESS_TOKEN_LIFETIME_MINUTES: int = 5
    REFRESH_TOKEN_LIFETIME_MINUTES: int = 60 * 24

    # BACKEND_CORS_ORIGINS is a JSON-formatted list of origins
    # e.g: '["http://localhost", "http://localhost:4200", "http://localhost:3000", \
    # "http://localhost:8080", "http://local.dockertoolbox.tiangolo.com"]'
    BACKEND_CORS_ORIGINS: List[AnyHttpUrl] = []

    class Config:
        case_sensitive = True


settings = Settings()
