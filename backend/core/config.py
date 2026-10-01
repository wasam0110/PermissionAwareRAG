from functools import lru_cache
from typing import Literal

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    app_name: str = "permission-aware-rag"
    app_env: Literal["development", "test", "staging", "production"] = "development"
    log_level: str = "INFO"
    api_host: str = "0.0.0.0"
    api_port: int = Field(default=8000, ge=1, le=65535)
    frontend_origin: str = "http://localhost:3000"
    database_url: str = "postgresql+asyncpg://rag_dev:change-me@localhost:5432/rag_dev"
    migration_database_url: str = (
    "postgresql+psycopg://rag_migration_admin:change-me-migration@localhost:5432/rag_dev"
)

    redis_url: str = "redis://:change-me@localhost:6380/0"
    jwt_secret_key: str = "development-only-secret-change-me-please"

    @property
    def is_production(self) -> bool:
        return self.app_env == "production"


@lru_cache
def get_settings() -> Settings:
    return Settings()
