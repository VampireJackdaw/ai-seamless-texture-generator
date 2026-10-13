"""Top-level generation orchestrator.

Wires the prompt -> backend -> seam-fix -> cache -> write pipeline.
This is the only service the CLI talks to.
"""
from __future__ import annotations

import logging

from texturegen.models.generation import GenerationRequest, GenerationResult
from texturegen.services.backend_registry import get_backend
from texturegen.services.cache_service import CacheService
from texturegen.services.io_service import write_tile
from texturegen.services.seam_service import SeamService

log = logging.getLogger(__name__)


class GenerationOrchestrator:
    """Coordinates a single generation request end to end."""

    def __init__(self) -> None:
        self._cache = CacheService()
        self._seam = SeamService()

    def run(self, request: GenerationRequest) -> GenerationResult:
        seed = request.seed or self._cache.derive_seed(request.prompt)

        cached = self._cache.lookup(request, seed)
        if cached is not None:
            log.info("cache hit for prompt=%r seed=%d", request.prompt, seed)
            tile = cached
        else:
            backend = get_backend(request.backend)
            tile = backend.generate(request.prompt, request.size, seed)
            tile = self._seam.enforce(tile, mode=request.wrap_mode)
            self._cache.store(request, seed, tile)

        seam_score = self._seam.score(tile)
        path = write_tile(tile, request.output_dir, request.prompt, seed)
        return GenerationResult(
            tile_path=path,
            width=tile.width,
            height=tile.height,
            seam_score=seam_score,
            backend=request.backend,
            seed_used=seed,
        )