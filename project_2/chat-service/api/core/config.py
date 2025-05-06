# api/core/config.py

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    PSQL_HOST: str
    PSQL_PORT: str
    PSQL_USER: str
    PSQL_PASSWORD: str
    PSQL_NAME: str

    model_config = SettingsConfigDict(
        env_file=".env",
        extra="allow"
    )

settings = Settings()
