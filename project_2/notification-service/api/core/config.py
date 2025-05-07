# api/core/config.py

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    LOCALSTACK_HOST: str
    LOCALSTACK_PORT: str
    DYNAMODB_ENDPOINT: str
    DYNAMODB_NOTIFICATION_TABLE_NAME: str
    SNS_ENDPOINT: str
    SNS_TOPIC_NAME: str
    SNS_TOPIC_ARN: str
    AWS_REGION: str
    AWS_ACCESS_KEY_ID: str
    AWS_SECRET_ACCESS_KEY: str
    AWS_SESSION_TOKEN: str

    model_config = SettingsConfigDict(
        env_file=".env",
        extra="allow"
    )

settings = Settings()
