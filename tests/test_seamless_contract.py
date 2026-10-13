"""Every backend must produce a tile that scores above the seam floor."""
from __future__ import annotations

import pytest

from texturegen.services.backends.procedural import ProceduralBackend
from texturegen.services.seam_service import SeamService

SEAM_FLOOR = 0.9


@pytest.mark.parametrize("seed", [1, 42, 1337])
def test_procedural_tiles_are_seamless(seed: int) -> None:
    tile = ProceduralBackend().generate("dark walnut planks", 256, seed)
    score = SeamService().score(tile)
    assert score >= SEAM_FLOOR, f"seam score {score:.4f} below floor {SEAM_FLOOR}"


def test_enforce_improves_or_holds_score() -> None:
    tile = ProceduralBackend().generate("marble veins", 256, 7)
    service = SeamService()
    before = service.score(tile)
    after = service.score(service.enforce(tile))
    assert after >= before - 1e-6