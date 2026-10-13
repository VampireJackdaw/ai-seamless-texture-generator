"""In-memory tile representation used between services."""
from __future__ import annotations

from dataclasses import dataclass

import numpy as np


@dataclass(slots=True)
class Tile:
    """A single seamless tile as an HxWxC float32 array in [0, 1]."""

    pixels: np.ndarray
    meta: dict[str, str]

    def __post_init__(self) -> None:
        if self.pixels.ndim != 3:
            raise ValueError(f"expected HxWxC, got shape {self.pixels.shape!r}")
        if self.pixels.dtype != np.float32:
            self.pixels = self.pixels.astype(np.float32)

    @property
    def height(self) -> int:
        return int(self.pixels.shape[0])

    @property
    def width(self) -> int:
        return int(self.pixels.shape[1])