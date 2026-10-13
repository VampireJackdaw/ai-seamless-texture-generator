"""Optional C++ kernel loader. Falls back to the pure-Python path."""
from __future__ import annotations

import logging
from pathlib import Path

log = logging.getLogger(__name__)

_LIB_NAMES = ("texturegen_kernel.pyd", "texturegen_kernel.so")


def try_load_kernel() -> object | None:
    """Return the compiled kernel module, or None if not built."""
    for name in _LIB_NAMES:
        candidate = Path(__file__).parents[3] / "native" / "build" / name
        if candidate.exists():
            import importlib.util

            spec = importlib.util.spec_from_file_location("texturegen_kernel", candidate)
            if spec and spec.loader:
                mod = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(mod)
                log.info("loaded native kernel from %s", candidate)
                return mod
    log.debug("native kernel not built; using pure-Python path")
    return None