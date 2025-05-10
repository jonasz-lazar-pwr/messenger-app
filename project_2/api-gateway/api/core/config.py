# api/core/config.py

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    CHAT_SERVICE_HOST: str
    CHAT_SERVICE_PORT: int

    MEDIA_SERVICE_HOST: str
    MEDIA_SERVICE_PORT: int

    NOTIFICATION_SERVICE_HOST: str
    NOTIFICATION_SERVICE_PORT: int

    COGNITO_ISSUER_URL: str
    COGNITO_POOL_ID: str
    COGNITO_CLIENT_ID: str

    CORS_ALLOW_ORIGINS: str

    model_config = SettingsConfigDict(
        env_file=".env",
        extra="allow"
    )

settings = Settings()
