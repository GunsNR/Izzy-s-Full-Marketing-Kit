from pathlib import Path
import shutil
import sys
import tempfile

REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT))

from scripts.context_governance_check import run_governance_check

RUN_DIR = REPO_ROOT / "test_runs" / "ecommerce_full_stack_acceptance_001"


def _mutate_front_matter_value(path: Path, key: str, value: str) -> None:
    lines = path.read_text(encoding="utf-8").splitlines()
    for idx, line in enumerate(lines):
        if line.strip().startswith(f"{key}:"):
            indent = line[: len(line) - len(line.lstrip())]
            lines[idx] = f"{indent}{key}: {value}"
            break
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def test_governance_check_passes_with_valid_record() -> None:
    issues = run_governance_check(RUN_DIR)
    assert not issues


def test_governance_check_fails_when_context_changes_without_log_update() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        fixture = Path(tmp) / "run"
        shutil.copytree(RUN_DIR, fixture)
        _mutate_front_matter_value(fixture / "RUN_CONTEXT.md", "brand_name", "Unlogged Brand")

        issues = run_governance_check(fixture)
        assert any(issue.severity == "CRITICAL" for issue in issues)


def test_governance_check_fails_material_change_without_ack() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        fixture = Path(tmp) / "run"
        shutil.copytree(RUN_DIR, fixture)
        _mutate_front_matter_value(fixture / "RUN_CONTEXT.md", "core_offer", "new offer")
        _mutate_front_matter_value(fixture / "BUSINESS_CONTEXT_CHANGELOG.md", "material_change_ack", "false")

        issues = run_governance_check(fixture)
        assert any("material context change" in issue.message for issue in issues)


def test_governance_check_fails_schema_change_without_note() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        fixture = Path(tmp) / "run"
        shutil.copytree(RUN_DIR, fixture)
        _mutate_front_matter_value(fixture / "RUN_CONTEXT.md", "schema_version", "2.0")
        _mutate_front_matter_value(fixture / "BUSINESS_CONTEXT_CHANGELOG.md", "schema_version_impact", "")

        issues = run_governance_check(fixture)
        assert any("schema_version" in issue.message and issue.severity == "CRITICAL" for issue in issues)


def test_governance_check_is_deterministic() -> None:
    first = run_governance_check(RUN_DIR)
    second = run_governance_check(RUN_DIR)
    assert first == second
