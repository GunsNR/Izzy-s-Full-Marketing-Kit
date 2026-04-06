from pathlib import Path
import sys

REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT))

from scripts.acceptance_run_validator import run_validation as run_acceptance_validation
from scripts.repo_validator import run_validation as run_repo_validation


def test_repo_validator_passes() -> None:
    errors = run_repo_validation()
    assert not errors, "Expected repository validation to pass with zero errors."


def test_acceptance_run_validator_passes() -> None:
    issues = run_acceptance_validation()
    assert not issues, "Expected acceptance run validation to pass with zero issues."
