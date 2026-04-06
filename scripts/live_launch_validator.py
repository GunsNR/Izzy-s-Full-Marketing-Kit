#!/usr/bin/env python3
"""Compatibility entrypoint for live launch governance validation."""

from __future__ import annotations

import importlib.util
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parent
MODULE_PATH = ROOT / "launch_governance_validator.py"
SPEC = importlib.util.spec_from_file_location("launch_governance_validator", MODULE_PATH)
if SPEC is None or SPEC.loader is None:
    raise SystemExit("Failed to load launch_governance_validator module.")
MODULE = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = MODULE
SPEC.loader.exec_module(MODULE)


if __name__ == "__main__":
    raise SystemExit(MODULE.main())
