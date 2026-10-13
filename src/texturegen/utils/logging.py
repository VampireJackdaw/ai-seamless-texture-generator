"""Logging bootstrap driven by config/logging.yaml."""
from __future__ import annotations

import logging
import logging.config
from pathlib import Path

import yaml

_CONFIGURED = False


def configure_logging(debug: bool = False) -> None:
    global _CONFIGURED
    if _CONFIGURED:
        return
    cfg_path = Path(__file__).parents[1] / "config" / "logging.yaml"
    if cfg_path.exists():
        with cfg_path.open("r", encoding="utf-8") as fh:
            logging.config.dictConfig(yaml.safe_load(fh))
    logging.getLogger("texturegen").setLevel(logging.DEBUG if debug else logging.INFO)
    _CONFIGURED = True