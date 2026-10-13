"""Filesystem boundary. The only place tiles touch disk as images."""
from __future__ import annotations

import re
from pathlib import Path

import numpy as np
from PIL import Image

from texturegen.models.tile import Tile

_SLUG = re.compile(r"[^a-z0-9]+")


def _slugify(prompt: str, limit: int = 48) -> str:
    slug = _SLUG.sub("-", prompt.lower()).strip("-")
    return slug[:limit] or "tile"


def write_tile(tile: Tile, output_dir: Path, prompt: str, seed: int) -> Path:
    output_dir.mkdir(parents=True, exist_ok=True)
    name = f"{_slugify(prompt)}-{seed:08x}.png"
    path = output_dir / name
    arr = (np.clip(tile.pixels, 0.0, 1.0) * 255.0).astype(np.uint8)
    Image.fromarray(arr, mode="RGB").save(path, format="PNG", optimize=True)
    return path