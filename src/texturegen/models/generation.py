"""Request/response models for a generation run."""
from __future__ import annotations

from pathlib import Path

from pydantic import BaseModel, Field


class GenerationRequest(BaseModel):
    prompt: str = Field(min_length=1, max_length=2000)
    size: int = Field(default=512, ge=64, le=4096)
    seed: int = Field(default=0, ge=0)
    backend: str = "procedural"
    output_dir: Path = Path("outputs")
    wrap_mode: str = Field(default="torus", pattern="^(torus|mirror|offset)$")


class GenerationResult(BaseModel):
    tile_path: Path
    width: int
    height: int
    seam_score: float = Field(ge=0.0, le=1.0)
    backend: str
    seed_used: int