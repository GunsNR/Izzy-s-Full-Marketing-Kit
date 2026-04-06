#!/usr/bin/env python3
"""Install repository git hooks for context governance enforcement."""

from __future__ import annotations

import argparse
import os
import stat
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HOOKS_DIR = ROOT / ".githooks"
PRE_COMMIT = HOOKS_DIR / "pre-commit"
MANAGED_MARKER = "managed-by: scripts/install_hooks.py"


def _run_git(*args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(["git", *args], cwd=ROOT, capture_output=True, text=True)


def ensure_git_repo() -> None:
    result = _run_git("rev-parse", "--is-inside-work-tree")
    if result.returncode != 0 or result.stdout.strip() != "true":
        raise RuntimeError("Git repository metadata unavailable. Run from a git checkout.")


def install_pre_commit(force: bool = False) -> str:
    HOOKS_DIR.mkdir(parents=True, exist_ok=True)

    if not PRE_COMMIT.exists():
        raise RuntimeError("Missing .githooks/pre-commit template. Cannot install hooks.")

    content = PRE_COMMIT.read_text(encoding="utf-8")
    if MANAGED_MARKER not in content:
        if not force:
            raise RuntimeError(
                ".githooks/pre-commit is not managed by installer. Use --force only after manual review."
            )

    mode = PRE_COMMIT.stat().st_mode
    PRE_COMMIT.chmod(mode | stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH)

    config_result = _run_git("config", "core.hooksPath", ".githooks")
    if config_result.returncode != 0:
        raise RuntimeError(f"Unable to set core.hooksPath: {config_result.stderr.strip()}")

    return "Installed git hooks path to .githooks and ensured pre-commit executable."


def main() -> int:
    parser = argparse.ArgumentParser(description="Install repository git hooks for governance checks.")
    parser.add_argument("--force", action="store_true", help="Allow install even if hook template marker is missing")
    args = parser.parse_args()

    try:
        ensure_git_repo()
        message = install_pre_commit(force=args.force)
        print(message)
        print("Hook install complete. Test with: .githooks/pre-commit")
        return 0
    except RuntimeError as exc:
        print(f"Hook installation failed: {exc}")
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
