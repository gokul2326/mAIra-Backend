from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    APP_NAME: str = "mira-backend"
    APP_ENV: str = "development"
    DEBUG: bool = True
    PORT: int = 8000
    HOST: str = "0.0.0.0"

    SECRET_KEY: str = "org-super-secret-system-key-change-in-production-0987654321"
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60
    SET_PASSWORD_TOKEN_EXPIRE_MINUTES: int = 15
    OTP_EXPIRE_MINUTES: int = 5

    ALLOWED_EMAIL_DOMAIN: str = "company.com"

    class Config:
        env_file = ".env"
        extra = "ignore"

settings = Settings()
