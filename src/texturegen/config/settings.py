"""Typed application settings loaded from YAML + environment."""
from __future__ import annotations

from pathlib import Path

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class AppSettings(BaseSettings):
    """Runtime settings. Env vars override YAML, e.g. TEXTUREGEN_TILE_SIZE."""

    model_config = SettingsConfigDict(env_prefix="TEXTUREGEN_", extra="ignore")

    tile_size: int = Field(default=512, ge=64, le=4096)
    default_backend: str = "procedural"
    cache_dir: Path = Path("cache/tiles")
    model_dir: Path = Path("models")
    bridge_host: str = "127.0.0.1"
    bridge_port: int = Field(default=8765, ge=1024, le=65535)
    max_batch: int = Field(default=8, ge=1, le=64)

    def ensure_dirs(self) -> None:
        for d in (self.cache_dir, self.model_dir):
            d.mkdir(parents=True, exist_ok=True)


_SETTINGS: AppSettings | None = None


def get_settings() -> AppSettings:
    """Process-wide singleton settings accessor."""
    global _SETTINGS
    if _SETTINGS is None:
        _SETTINGS = AppSettings()
        _SETTINGS.ensure_dirs()
    return _SETTINGS