# Contributing to ai-seamless-texture-generator

Thanks for wanting to push pixels. This repo is a Windows-first desktop
tool that generates seamless, tileable textures and repeating surface
patterns from text prompts, reference images, or procedural seeds.

## Ground rules

- Python 3.11+ is the reference interpreter. C++/CUDA kernels live under
  `native/` and are optional build targets.
- Every service must be importable without a GPU. GPU backends are
  adapters, not hard dependencies.
- Seamless is the contract. A texture that does not tile end-to-end is a
  bug, not a style choice.

## Dev setup

```
git clone https://github.com/yourname/ai-seamless-texture-generator
cd ai-seamless-texture-generator
python -m venv .venv
.venv\Scripts\activate
pip install -e ".[dev]"
pre-commit install
pytest -q
```

## Branching

- `main` — stable, tiling, ships.
- `feat/<short-name>` — new generator, new adapter, new post-process.
- `fix/<short-name>` — bugfix, always with a regression test under
  `tests/`.

## Style

- `ruff` + `black` + `mypy --strict` on `src/`. Run `pre-commit run -a`.
- Type everything public. `Any` needs a comment explaining why.
- Services take and return pydantic models from `src/texturegen/models/`.
- No service touches the filesystem directly — route through
  `services/io_service.py`.

## Adding a new generator backend

1. Drop a module under `src/texturegen/services/backends/`.
2. Subclass `BaseGeneratorBackend` from `services/backends/base.py`.
3. Register it in `services/backend_registry.py`.
4. Add a golden-tile test in `tests/test_seamless_contract.py`.

## Pull requests

- One feature per PR.
- Include a 512x512 tiled preview in the PR description (or a hash of
  the deterministic output if the model is non-deterministic).
- CI runs `pytest`, `ruff`, `mypy`, and a seam-check on the sample prompt.

## Reporting issues

Use the issue templates. Attach the prompt, seed, backend, and the
`--debug` log from `config/logging.yaml`.