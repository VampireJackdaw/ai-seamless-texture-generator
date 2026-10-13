"""Content-addressed tile cache keyed by prompt+seed+size."""
from __future__ import annotations

import hashlib
from pathlib import Path

import numpy as np

from texturegen.config.settings import get_settings
from texturegen.models.generation import GenerationRequest
from texturegen.models.tile import Tile


class CacheService:
    """Simple on-disk npz cache. Content-addressed, no eviction yet."""

    def __init__(self) -> None:
        self._root = get_settings().cache_dir
        self._root.mkdir(parents=True, exist_ok=True)

    def _key(self, request: GenerationRequest, seed: int) -> str:
        h = hashlib.sha256()
        h.update(request.prompt.encode())
        h.update(f"{seed}:{request.size}:{request.backend}".encode())
        return h.hexdigest()[:32]

    def derive_seed(self, prompt: str) -> int:
        return int.from_bytes(hashlib.sha256(prompt.encode()).digest()[:4], "big")

    def lookup(self, request: GenerationRequest, seed: int) -> Tile | None:
        path = self._root / f"{self._key(request, seed)}.npz"
        if not path.exists():
            return None
        data = np.load(path, allow_pickle=False)
        return Tile(pixels=data["px"], meta={"cached": "1"})

    def store(self, request: GenerationRequest, seed: int, tile: Tile) -> None:
        path = self._root / f"{self._key(request, seed)}.npz"
        np.savez_compressed(path, px=tile.pixels)