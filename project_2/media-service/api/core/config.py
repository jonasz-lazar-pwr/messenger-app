# api/core/config.py

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    LOCALSTACK_HOST: str
    LOCALSTACK_PORT: str
    DYNAMODB_ENDPOINT: str
    DYNAMODB_TABLE_NAME: str
    AWS_REGION: str
    S3_ENDPOINT: str
    S3_BUCKET_NAME: str
    AWS_ACCESS_KEY_ID: str
    AWS_SECRET_ACCESS_KEY: str
    AWS_SESSION_TOKEN: str
    CHAT_SERVICE_HOST: str
    CHAT_SERVICE_PORT: str
    CORS_ALLOW_ORIGINS: str

    model_config = SettingsConfigDict(
        env_file=".env",
        extra="allow"
    )

settings = Settings()
