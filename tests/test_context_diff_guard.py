from pathlib import Path
import shutil
import sys
import tempfile
from unittest.mock import patch

REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT))

from scripts.context_diff_guard import detect_changed_files_from_git, evaluate_diff_guard

RUN_DIR = REPO_ROOT / "test_runs" / "ecommerce_full_stack_acceptance_001"
RUN_PREFIX = "test_runs/ecommerce_full_stack_acceptance_001"


def _mutate_front_matter_value(path: Path, key: str, value: str) -> None:
    lines = path.read_text(encoding="utf-8").splitlines()
    for idx, line in enumerate(lines):
        if line.strip().startswith(f"{key}:"):
            indent = line[: len(line) - len(line.lstrip())]
            lines[idx] = f"{indent}{key}: {value}"
            break
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def test_diff_guard_passes_when_run_context_and_changelog_both_change() -> None:
    changed = [f"{RUN_PREFIX}/RUN_CONTEXT.md", f"{RUN_PREFIX}/BUSINESS_CONTEXT_CHANGELOG.md"]
    issues = evaluate_diff_guard(changed, RUN_DIR)
    assert not issues


def test_diff_guard_fails_when_run_context_changes_alone() -> None:
    changed = [f"{RUN_PREFIX}/RUN_CONTEXT.md"]
    issues = evaluate_diff_guard(changed, RUN_DIR)
    assert any(issue.severity == "CRITICAL" for issue in issues)


def test_diff_guard_fails_when_artifact_changes_without_changelog() -> None:
    changed = [f"{RUN_PREFIX}/COPY_SYSTEM.md"]
    issues = evaluate_diff_guard(changed, RUN_DIR)
    assert any(issue.severity == "MAJOR" for issue in issues)


def test_diff_guard_fails_schema_version_change_without_schema_rationale() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        fixture = Path(tmp) / "run"
        shutil.copytree(RUN_DIR, fixture)
        _mutate_front_matter_value(fixture / "RUN_CONTEXT.md", "schema_version", "2.0")
        _mutate_front_matter_value(fixture / "BUSINESS_CONTEXT_CHANGELOG.md", "schema_version_impact", "")

        changed = [f"{RUN_PREFIX}/RUN_CONTEXT.md", f"{RUN_PREFIX}/BUSINESS_CONTEXT_CHANGELOG.md"]
        issues = evaluate_diff_guard(changed, fixture)
        assert any("schema_version" in issue.message and issue.severity == "CRITICAL" for issue in issues)


def test_diff_guard_is_deterministic() -> None:
    changed = [f"{RUN_PREFIX}/COPY_SYSTEM.md", f"{RUN_PREFIX}/BUSINESS_CONTEXT_CHANGELOG.md"]
    first = evaluate_diff_guard(changed, RUN_DIR)
    second = evaluate_diff_guard(changed, RUN_DIR)
    assert first == second


def test_diff_guard_explicit_changed_file_mode_behavior() -> None:
    changed = [f"{RUN_PREFIX}/COPY_SYSTEM.md", f"{RUN_PREFIX}/BUSINESS_CONTEXT_CHANGELOG.md"]
    issues = evaluate_diff_guard(changed, RUN_DIR)
    assert not issues


def test_diff_guard_git_mode_detects_files_when_available() -> None:
    with patch("scripts.context_diff_guard.subprocess.run") as mocked_run:
        mocked_run.return_value.returncode = 0
        mocked_run.return_value.stdout = f"{RUN_PREFIX}/RUN_CONTEXT.md\n{RUN_PREFIX}/BUSINESS_CONTEXT_CHANGELOG.md\n"
        files = detect_changed_files_from_git()
        assert files == sorted({f"{RUN_PREFIX}/RUN_CONTEXT.md", f"{RUN_PREFIX}/BUSINESS_CONTEXT_CHANGELOG.md"})
