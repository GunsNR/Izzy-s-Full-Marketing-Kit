from pathlib import Path
import shutil
import sys
import tempfile

REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT))

from scripts.launch_governance_validator import run_validation

RUN_DIR = REPO_ROOT / "test_runs" / "ecommerce_full_stack_acceptance_001"


def test_launch_governance_validator_passes_on_current_run() -> None:
    issues = run_validation(RUN_DIR)
    assert not issues


def test_launch_governance_validator_fails_missing_required_artifact() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        fixture = Path(tmp) / "run"
        shutil.copytree(RUN_DIR, fixture)
        (fixture / "GO_NO_GO_SCORECARD.md").unlink()
        issues = run_validation(fixture)
        assert any(issue.file == "GO_NO_GO_SCORECARD.md" and issue.severity == "CRITICAL" for issue in issues)


def test_launch_governance_validator_fails_missing_owner_field() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        fixture = Path(tmp) / "run"
        shutil.copytree(RUN_DIR, fixture)
        path = fixture / "PAID_BUDGET_APPROVAL.md"
        text = path.read_text(encoding="utf-8")
        text = text.replace("## Owner", "## Team")
        text = text.replace("Human Owner", "Human Lead")
        path.write_text(text, encoding="utf-8")
        issues = run_validation(fixture)
        assert any(issue.file == "PAID_BUDGET_APPROVAL.md" and "owner" in issue.message for issue in issues)


def test_launch_governance_validator_fails_missing_approval_field() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        fixture = Path(tmp) / "run"
        shutil.copytree(RUN_DIR, fixture)
        path = fixture / "SUPPLIER_SOURCING_INTAKE.md"
        path.write_text(path.read_text(encoding="utf-8").replace("## Approval Status", "## Approval"), encoding="utf-8")
        issues = run_validation(fixture)
        assert any(issue.file == "SUPPLIER_SOURCING_INTAKE.md" and "approval" in issue.message.lower() for issue in issues)


def test_launch_governance_validator_fails_missing_go_no_go_decision() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        fixture = Path(tmp) / "run"
        shutil.copytree(RUN_DIR, fixture)
        path = fixture / "GO_NO_GO_SCORECARD.md"
        text = path.read_text(encoding="utf-8").replace("GO WITH CONDITIONS", "PENDING")
        path.write_text(text, encoding="utf-8")
        issues = run_validation(fixture)
        assert any(issue.file == "GO_NO_GO_SCORECARD.md" and "decision" in issue.message for issue in issues)


def test_launch_governance_validator_fails_missing_rollback_section() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        fixture = Path(tmp) / "run"
        shutil.copytree(RUN_DIR, fixture)
        path = fixture / "LAUNCH_SIGNOFF_QUEUE.md"
        text = path.read_text(encoding="utf-8").replace("## Rollback Plan", "## Rollout Plan")
        path.write_text(text, encoding="utf-8")
        issues = run_validation(fixture)
        assert any(issue.file == "LAUNCH_SIGNOFF_QUEUE.md" and "rollback" in issue.message for issue in issues)


def test_launch_governance_validator_is_deterministic() -> None:
    first = run_validation(RUN_DIR)
    second = run_validation(RUN_DIR)
    assert first == second
