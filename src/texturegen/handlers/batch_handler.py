"""Batch generation handler. Fans out over a prompt file."""
from __future__ import annotations

from pathlib import Path

from texturegen.models.generation import GenerationRequest, GenerationResult
from texturegen.services.orchestrator import GenerationOrchestrator


def run_batch(prompt_file: Path, size: int, backend: str, out_dir: Path) -> list[GenerationResult]:
    """One prompt per line; blank lines and '#' comments are skipped."""
    prompts = [
        line.strip()
        for line in prompt_file.read_text(encoding="utf-8").splitlines()
        if line.strip() and not line.lstrip().startswith("#")
    ]
    orchestrator = GenerationOrchestrator()
    results: list[GenerationResult] = []
    for idx, prompt in enumerate(prompts):
        results.append(
            orchestrator.run(
                GenerationRequest(
                    prompt=prompt, size=size, seed=idx + 1, backend=backend, output_dir=out_dir
                )
            )
        )
    return results