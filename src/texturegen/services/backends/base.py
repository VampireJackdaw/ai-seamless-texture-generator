"""Abstract base for all texture generation backends."""
from __future__ import annotations

from abc import ABC, abstractmethod
from typing import ClassVar

from texturegen.models.tile import Tile


class BaseGeneratorBackend(ABC):
    """Contract every backend must satisfy.

    Implementations MUST return a Tile whose edges are already wrap-safe
    OR document that they require the seam service to run afterwards.
    """

    backend_id: ClassVar[str]
    requires_seam_fix: ClassVar[bool] = True

    @abstractmethod
    def generate(self, prompt: str, size: int, seed: int) -> Tile:
        """Produce a single HxWx3 float32 tile in [0, 1]."""
        raise NotImplementedError