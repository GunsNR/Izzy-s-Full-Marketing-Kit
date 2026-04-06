from pathlib import Path
import shutil
import sys
import tempfile

REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT))

from scripts.consistency_validator import run_validation
from scripts.context_sync import sync_context

RUN_DIR = REPO_ROOT / "test_runs" / "ecommerce_full_stack_acceptance_001"
TARGET_FILE = "COPY_SYSTEM.md"


def _mutate_front_matter_value(path: Path, key: str, value: str) -> None:
    lines = path.read_text(encoding="utf-8").splitlines()
    for idx, line in enumerate(lines):
        if line.strip().startswith(f"{key}:"):
            indent = line[: len(line) - len(line.lstrip())]
            lines[idx] = f"{indent}{key}: {value}"
            break
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def test_context_sync_dry_run_reports_differences_without_writing() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        fixture = Path(tmp) / "run"
        shutil.copytree(RUN_DIR, fixture)
        target = fixture / TARGET_FILE
        original = target.read_text(encoding="utf-8")
        _mutate_front_matter_value(target, "brand_name", "Drift Brand")

        changes, issues = sync_context(fixture, write=False)
        assert not issues
        assert any(TARGET_FILE in line and "brand_name" in line for line in changes)
        assert "Drift Brand" in target.read_text(encoding="utf-8")
        assert original != target.read_text(encoding="utf-8")


def test_context_sync_write_mode_normalizes_context_blocks() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        fixture = Path(tmp) / "run"
        shutil.copytree(RUN_DIR, fixture)
        target = fixture / TARGET_FILE
        _mutate_front_matter_value(target, "pricing_band", "<50%")

        changes, issues = sync_context(fixture, write=True)
        assert not issues
        assert any("pricing_band" in line for line in changes)

        issues_after = run_validation(fixture, strict_mode=True)
        assert not issues_after


def test_context_sync_malformed_front_matter_fails_safely() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        fixture = Path(tmp) / "run"
        shutil.copytree(RUN_DIR, fixture)
        target = fixture / TARGET_FILE
        target.write_text(target.read_text(encoding="utf-8").replace("---\n", "", 1), encoding="utf-8")

        changes, issues = sync_context(fixture, write=False)
        assert not changes
        assert any(issue.file == TARGET_FILE for issue in issues)


def test_synced_files_pass_strict_consistency_after_sync() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        fixture = Path(tmp) / "run"
        shutil.copytree(RUN_DIR, fixture)
        target = fixture / TARGET_FILE
        _mutate_front_matter_value(target, "risk_class", "low")

        before = run_validation(fixture, strict_mode=True)
        assert any("risk_class" in issue.message for issue in before)

        _, issues = sync_context(fixture, write=True)
        assert not issues
        after = run_validation(fixture, strict_mode=True)
        assert not after


def test_context_sync_is_deterministic_on_repeated_runs() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        fixture = Path(tmp) / "run"
        shutil.copytree(RUN_DIR, fixture)

        first_changes, first_issues = sync_context(fixture, write=False)
        second_changes, second_issues = sync_context(fixture, write=False)
        assert first_changes == second_changes
        assert first_issues == second_issues
