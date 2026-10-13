"""Registry mapping backend ids to generator backend classes."""
from __future__ import annotations

from texturegen.services.backends.base import BaseGeneratorBackend
from texturegen.services.backends.procedural import ProceduralBackend

_BACKENDS: dict[str, type[BaseGeneratorBackend]] = {
    "procedural": ProceduralBackend,
}


def _try_register_optional() -> None:
    """Register GPU backends only if their deps are importable."""
    try:
        from texturegen.services.backends.diffusion import DiffusionBackend

        _BACKENDS["diffusion"] = DiffusionBackend
    except ImportError:  # torch not installed
        pass


_try_register_optional()


def get_backend(backend_id: str) -> BaseGeneratorBackend:
    if backend_id not in _BACKENDS:
        raise KeyError(f"unknown backend {backend_id!r}; have {sorted(_BACKENDS)}")
    return _BACKENDS[backend_id]()


def list_backends() -> dict[str, str]:
    return {bid: (cls.__doc__ or "").strip().splitlines()[0] for bid, cls in _BACKENDS.items()}