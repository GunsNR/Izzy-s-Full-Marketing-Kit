from pathlib import Path
import shutil
import sys
import tempfile

REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT))

from scripts.consistency_validator import run_validation

RUN_DIR = REPO_ROOT / "test_runs" / "ecommerce_full_stack_acceptance_001"


def _mutate_front_matter_value(path: Path, key: str, value: str) -> None:
    lines = path.read_text(encoding="utf-8").splitlines()
    for idx, line in enumerate(lines):
        if line.strip().startswith(f"{key}:"):
            indent = line[: len(line) - len(line.lstrip())]
            lines[idx] = f"{indent}{key}: {value}"
            break
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def test_consistency_validator_passes_on_current_run() -> None:
    issues = run_validation(RUN_DIR, strict_mode=True)
    assert not issues


def test_consistency_validator_fails_on_schema_version_mismatch() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        fixture_dir = Path(tmp) / "run"
        shutil.copytree(RUN_DIR, fixture_dir)
        _mutate_front_matter_value(fixture_dir / "COPY_SYSTEM.md", "schema_version", "2.0")

        issues = run_validation(fixture_dir, strict_mode=True)
        assert any("schema_version" in issue.message and issue.severity == "CRITICAL" for issue in issues)


def test_consistency_validator_fails_on_brand_drift_fixture() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        fixture_dir = Path(tmp) / "run"
        shutil.copytree(RUN_DIR, fixture_dir)
        _mutate_front_matter_value(fixture_dir / "BRAND_SYSTEM.md", "brand_name", "Different Brand")

        issues = run_validation(fixture_dir, strict_mode=True)
        assert any("brand_name" in issue.message and issue.severity == "CRITICAL" for issue in issues)


def test_consistency_validator_fails_on_offer_drift_fixture() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        fixture_dir = Path(tmp) / "run"
        shutil.copytree(RUN_DIR, fixture_dir)
        _mutate_front_matter_value(fixture_dir / "STRATEGY_FOUNDATION.md", "core_offer", "starter 12-stick sampler")

        issues = run_validation(fixture_dir, strict_mode=True)
        assert any("core_offer" in issue.message and issue.severity == "CRITICAL" for issue in issues)


def test_consistency_validator_fails_on_pricing_band_drift_fixture() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        fixture_dir = Path(tmp) / "run"
        shutil.copytree(RUN_DIR, fixture_dir)
        _mutate_front_matter_value(fixture_dir / "PRODUCT_SELECTION_MATRIX.md", "pricing_band", "<50% gross margin")

        issues = run_validation(fixture_dir, strict_mode=True)
        assert any("pricing_band" in issue.message and issue.severity == "MAJOR" for issue in issues)


def test_consistency_validator_is_deterministic() -> None:
    first = run_validation(RUN_DIR, strict_mode=True)
    second = run_validation(RUN_DIR, strict_mode=True)
    assert first == second
