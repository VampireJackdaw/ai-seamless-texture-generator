"""Seamless-tile enforcement and scoring.

Two jobs:
  * enforce() — blend opposite edges so the tile wraps cleanly.
  * score()   — 1.0 means perfectly seamless, 0.0 means the wrap is a scar.
"""
from __future__ import annotations

import numpy as np

from texturegen.models.tile import Tile


class SeamService:
    """Edge blending + seam quality metric on float32 tiles."""

    def __init__(self, band: int = 8) -> None:
        self._band = band

    def enforce(self, tile: Tile, mode: str = "torus") -> Tile:
        px = tile.pixels
        band = min(self._band, px.shape[0] // 4, px.shape[1] // 4)
        for i in range(band):
            t = (i + 1) / (band + 1)
            top, bottom = px[i].copy(), px[-1 - i].copy()
            left, right = px[:, i].copy(), px[:, -1 - i].copy()
            px[i] = top * (1 - t) + bottom * t
            px[-1 - i] = bottom * (1 - t) + top * t
            px[:, i] = left * (1 - t) + right * t
            px[:, -1 - i] = right * (1 - t) + left * t
        return Tile(pixels=px, meta={**tile.meta, "seam_mode": mode})

    def score(self, tile: Tile) -> float:
        px = tile.pixels
        top_bottom = float(np.mean(np.abs(px[0] - px[-1])))
        left_right = float(np.mean(np.abs(px[:, 0] - px[:, -1])))
        raw = (top_bottom + left_right) * 0.5
        return float(np.clip(1.0 - raw * 4.0, 0.0, 1.0))