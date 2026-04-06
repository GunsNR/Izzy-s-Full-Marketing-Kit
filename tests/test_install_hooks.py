from pathlib import Path
import subprocess
import sys
from unittest.mock import patch

REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT))

import scripts.install_hooks as install_hooks


def test_install_hooks_script_is_idempotent() -> None:
    first = subprocess.run([sys.executable, "scripts/install_hooks.py"], cwd=REPO_ROOT, capture_output=True, text=True)
    second = subprocess.run([sys.executable, "scripts/install_hooks.py"], cwd=REPO_ROOT, capture_output=True, text=True)
    assert first.returncode == 0
    assert second.returncode == 0


def test_install_hooks_safe_handling_for_unmanaged_template() -> None:
    with patch.object(install_hooks, "HOOKS_DIR", REPO_ROOT / ".githooks"), patch.object(
        install_hooks, "PRE_COMMIT", REPO_ROOT / ".githooks" / "pre-commit"
    ), patch.object(install_hooks, "MANAGED_MARKER", "nonexistent-marker"):
        try:
            install_hooks.install_pre_commit(force=False)
            assert False, "Expected RuntimeError for unmanaged template"
        except RuntimeError as exc:
            assert "not managed" in str(exc)


def test_precommit_hook_invokes_diff_guard_and_prints_guidance() -> None:
    hook_text = (REPO_ROOT / ".githooks" / "pre-commit").read_text(encoding="utf-8")
    assert "python scripts/context_diff_guard.py" in hook_text
    assert "git diff --cached --name-only" in hook_text
    assert "--no-verify" in hook_text


def test_precommit_hook_exits_cleanly_with_no_staged_files() -> None:
    result = subprocess.run([".githooks/pre-commit"], cwd=REPO_ROOT, capture_output=True, text=True)
    assert result.returncode == 0
