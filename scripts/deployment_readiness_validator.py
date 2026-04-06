#!/usr/bin/env python3
"""Deployment-readiness validator wrapper for acceptance run gating."""

from __future__ import annotations

import importlib.util
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parent
MODULE_PATH = ROOT / "acceptance_run_validator.py"
SPEC = importlib.util.spec_from_file_location("acceptance_run_validator", MODULE_PATH)
if SPEC is None or SPEC.loader is None:
    raise SystemExit("Failed to load acceptance_run_validator module.")
MODULE = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = MODULE
SPEC.loader.exec_module(MODULE)


def main() -> int:
    issues = MODULE.run_validation()
    if issues:
        print("Deployment readiness validation failed:")
        for issue in issues:
            print(f"- {issue.file}: {issue.message}")
        return 1

    print("Deployment readiness validation passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
