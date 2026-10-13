"""Command-line front door for the texture generator.

Thin layer only: parse args, build a request model, hand to the
orchestrator service, print the result path. No generation logic here.
"""
from __future__ import annotations

from pathlib import Path

import typer
from rich.console import Console

from texturegen.models.generation import GenerationRequest
from texturegen.services.orchestrator import GenerationOrchestrator
from texturegen.utils.logging import configure_logging

app = typer.Typer(add_completion=False, help="AI seamless texture & pattern generator.")
console = Console()


@app.command()
def generate(
    prompt: str = typer.Option(..., "--prompt", "-p", help="Text prompt for the pattern."),
    size: int = typer.Option(512, "--size", "-s", help="Output tile size in pixels (square)."),
    seed: int = typer.Option(0, "--seed", help="RNG seed. 0 = random."),
    backend: str = typer.Option("procedural", "--backend", "-b", help="Backend id."),
    out: Path = typer.Option(Path("outputs"), "--out", "-o", help="Output directory."),
    debug: bool = typer.Option(False, "--debug", help="Verbose logging."),
) -> None:
    """Generate one seamless tile from a text prompt."""
    configure_logging(debug=debug)
    request = GenerationRequest(
        prompt=prompt, size=size, seed=seed, backend=backend, output_dir=out
    )
    orchestrator = GenerationOrchestrator()
    result = orchestrator.run(request)
    console.print(f"[green]wrote[/] {result.tile_path}  (seam score={result.seam_score:.4f})")


@app.command()
def backends() -> None:
    """List available generation backends."""
    from texturegen.services.backend_registry import list_backends

    for bid, desc in list_backends().items():
        console.print(f"[cyan]{bid}[/]  {desc}")


if __name__ == "__main__":
    app()