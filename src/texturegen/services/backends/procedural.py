"""Deterministic procedural backend — no ML deps, always available.

Synthesises a seamless pattern by summing periodic value-noise octaves
on a torus. Useful as a fallback and for tests.
"""
from __future__ import annotations

import hashlib

import numpy as np

from texturegen.models.tile import Tile
from texturegen.services.backends.base import BaseGeneratorBackend


def _prompt_hash(prompt: str) -> int:
    return int.from_bytes(hashlib.sha256(prompt.encode()).digest()[:8], "big")


def _torus_noise(size: int, freq: int, rng: np.random.Generator) -> np.ndarray:
    """Value noise sampled on an integer lattice that wraps at `freq`."""
    lattice = rng.random((freq, freq), dtype=np.float32)
    ys = np.linspace(0, freq, size, endpoint=False)
    xs = np.linspace(0, freq, size, endpoint=False)
    yi = np.floor(ys).astype(int) % freq
    xi = np.floor(xs).astype(int) % freq
    yf = (ys - np.floor(ys))[:, None]
    xf = (xs - np.floor(xs))[None, :]
    y1 = (yi + 1) % freq
    x1 = (xi + 1) % freq
    a = lattice[np.ix_(yi, xi)]
    b = lattice[np.ix_(yi, x1)]
    c = lattice[np.ix_(y1, xi)]
    d = lattice[np.ix_(y1, x1)]
    sy = yf * yf * (3 - 2 * yf)
    sx = xf * xf * (3 - 2 * xf)
    top = a + (b - a) * sx
    bot = c + (d - c) * sx
    return top + (bot - top) * sy


class ProceduralBackend(BaseGeneratorBackend):
    """Deterministic torus-noise backend. No GPU, no torch, always works."""

    backend_id = "procedural"
    requires_seam_fix = False

    def generate(self, prompt: str, size: int, seed: int) -> Tile:
        rng = np.random.default_rng(seed ^ _prompt_hash(prompt))
        acc = np.zeros((size, size), dtype=np.float32)
        amp = 1.0
        norm = 0.0
        for freq in (2, 4, 8, 16, 32):
            acc += amp * _torus_noise(size, freq, rng)
            norm += amp
            amp *= 0.5
        acc /= norm
        rgb = np.stack([acc, np.roll(acc, 7, axis=0), np.roll(acc, 13, axis=1)], axis=-1)
        rgb = np.clip(rgb, 0.0, 1.0).astype(np.float32)
        return Tile(pixels=rgb, meta={"backend": self.backend_id, "prompt": prompt})