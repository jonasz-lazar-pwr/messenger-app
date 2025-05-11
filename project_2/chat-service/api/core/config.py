# api/core/config.py

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    PSQL_HOST: str
    PSQL_PORT: str
    PSQL_USER: str
    PSQL_PASSWORD: str
    PSQL_NAME: str
    NOTIFICATION_SERVICE_HOST: str
    NOTIFICATION_SERVICE_PORT: int
    NOTIFICATION_RECEIVER_EMAIL: str
    MEDIA_SERVICE_HOST: str
    MEDIA_SERVICE_PORT: int
    CORS_ALLOW_ORIGINS: str

    model_config = SettingsConfigDict(
        env_file=".env",
        extra="allow"
    )

settings = Settings()
