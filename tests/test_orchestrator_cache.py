"""Second identical request must hit the cache and reuse the seed."""
from __future__ import annotations

from pathlib import Path

from texturegen.models.generation import GenerationRequest
from texturegen.services.orchestrator import GenerationOrchestrator


def test_cache_hit_is_deterministic(tmp_path: Path) -> None:
    orch = GenerationOrchestrator()
    req = GenerationRequest(prompt="brushed copper", size=128, backend="procedural", output_dir=tmp_path)
    first = orch.run(req)
    second = orch.run(req)
    assert first.seed_used == second.seed_used
    assert first.seam_score == second.seam_score
</invoke>