"""Environment settings for the API (local / staging / production)."""

from __future__ import annotations

from functools import lru_cache
from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict

_ROOT = Path(__file__).resolve().parents[3]
_ENV_FILES = (
    str(_ROOT / ".env"),
    ".env",
    "../../.env",
)


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=_ENV_FILES,
        env_file_encoding="utf-8",
        extra="ignore",
    )

    app_env: str = "local"
    api_host: str = "0.0.0.0"
    api_port: int = 8000
    cors_origins: str = "http://localhost:3000"

    next_public_supabase_url: str = ""
    next_public_supabase_anon_key: str = ""
    next_public_supabase_publishable_key: str = ""
    supabase_service_role_key: str = ""
    database_url: str = ""

    @property
    def supabase_url(self) -> str:
        return self.next_public_supabase_url.rstrip("/")

    @property
    def supabase_anon_key(self) -> str:
        return (
            self.next_public_supabase_anon_key
            or self.next_public_supabase_publishable_key
        )

    @property
    def cors_origins_list(self) -> list[str]:
        return [o.strip() for o in self.cors_origins.split(",") if o.strip()]


@lru_cache
def get_settings() -> Settings:
    return Settings()
