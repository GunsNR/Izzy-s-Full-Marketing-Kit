#!/usr/bin/env python3
"""Repository validation checks for Izzy's Full Marketing Kit."""

from __future__ import annotations

import argparse
import csv
import re
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable

ROOT = Path(__file__).resolve().parents[1]

REQUIRED_DOCS = [
    "README.md",
    "PLANS.md",
    "docs/OPERATING_DOCTRINE.md",
    "docs/EVIDENCE_POLICY.md",
    "docs/QUALITY_GATES.md",
    "docs/BUILD_LOG.md",
    "docs/INTEGRATED_PILOT_PLAN.md",
    "docs/UPDATE_POLICY.md",
    "docs/CHANGELOG_POLICY.md",
    "docs/BUSINESS_CONTEXT_CHANGE_POLICY.md",
    "docs/BUSINESS_CONTEXT_CHANGE_LOG_TEMPLATE.md",
    "docs/DEPLOYMENT_GOVERNANCE_POLICY.md",
    "docs/LAUNCH_APPROVAL_FRAMEWORK.md",
    "docs/CLAIMS_SUBSTANTIATION_POLICY.md",
    "docs/PRICING_AND_UNIT_ECONOMICS_POLICY.md",
    "docs/ANALYTICS_LAUNCH_READINESS_STANDARD.md",
    "docs/PRELAUNCH_QA_STANDARD.md",
    "test_runs/ecommerce_full_stack_acceptance_001/TEST_PLAN.md",
    "test_runs/ecommerce_full_stack_acceptance_001/RUN_CONTEXT.md",
    "test_runs/ecommerce_full_stack_acceptance_001/BUSINESS_CONTEXT_CHANGELOG.md",
]

REQUIRED_SKILL_FRONT_MATTER = {
    "name",
    "description",
    "version",
    "owner_role",
    "risk_level",
    "autonomy_mode",
}

REQUIRED_SKILL_HEADINGS = [
    "## Role",
    "## Mission",
    "## Inputs Required",
    "## Outputs",
    "## Core Workflow",
    "## Evidence Policy",
    "## Quality Bar",
    "## Escalation Triggers",
    "## Success Metrics",
    "## Update Logic",
]

REQUIRED_EVAL_COLUMNS = {
    "evals/skill-routing.prompts.csv": {"prompt", "expected_skill", "notes"},
    "evals/critical-workflows.prompts.csv": {"workflow_id", "prompt", "required_checks"},
    "evals/negative-controls.prompts.csv": {"prompt", "expected_behavior"},
}


@dataclass
class ValidationError:
    location: str
    message: str


def _collect_markdown_front_matter(text: str) -> dict[str, str]:
    match = re.match(r"^---\n(.*?)\n---\n", text, re.DOTALL)
    if not match:
        return {}

    metadata = {}
    for line in match.group(1).splitlines():
        if ":" not in line:
            continue
        key, value = line.split(":", 1)
        metadata[key.strip()] = value.strip().strip('"')
    return metadata


def validate_required_docs(errors: list[ValidationError]) -> None:
    for rel_path in REQUIRED_DOCS:
        full_path = ROOT / rel_path
        if not full_path.exists():
            errors.append(ValidationError(rel_path, "missing required documentation file"))


def validate_skill_files(errors: list[ValidationError]) -> None:
    for skill_path in sorted((ROOT / "skills").glob("*/SKILL.md")):
        rel = skill_path.relative_to(ROOT).as_posix()
        text = skill_path.read_text(encoding="utf-8")
        metadata = _collect_markdown_front_matter(text)

        missing_front_matter = REQUIRED_SKILL_FRONT_MATTER.difference(metadata.keys())
        if missing_front_matter:
            errors.append(
                ValidationError(
                    rel,
                    f"missing front matter fields: {', '.join(sorted(missing_front_matter))}",
                )
            )

        for heading in REQUIRED_SKILL_HEADINGS:
            if heading not in text:
                errors.append(ValidationError(rel, f"missing required section heading '{heading}'"))


def validate_eval_csv(errors: list[ValidationError]) -> None:
    for rel_path, required_columns in REQUIRED_EVAL_COLUMNS.items():
        full_path = ROOT / rel_path
        if not full_path.exists():
            errors.append(ValidationError(rel_path, "missing eval csv"))
            continue

        with full_path.open(encoding="utf-8", newline="") as handle:
            reader = csv.DictReader(handle)
            header = set(reader.fieldnames or [])
            missing = required_columns.difference(header)
            if missing:
                errors.append(
                    ValidationError(
                        rel_path,
                        f"missing required columns: {', '.join(sorted(missing))}",
                    )
                )
                continue

            row_count = sum(1 for _ in reader)
            if row_count == 0:
                errors.append(ValidationError(rel_path, "must include at least one test row"))


def validate_no_placeholders(files: Iterable[str], errors: list[ValidationError]) -> None:
    placeholder_pattern = re.compile(r"\bPlaceholder\b", re.IGNORECASE)
    for rel_path in files:
        full_path = ROOT / rel_path
        if not full_path.exists():
            continue
        text = full_path.read_text(encoding="utf-8")
        if placeholder_pattern.search(text):
            errors.append(ValidationError(rel_path, "contains placeholder content"))


def run_validation() -> list[ValidationError]:
    errors: list[ValidationError] = []
    validate_required_docs(errors)
    validate_skill_files(errors)
    validate_eval_csv(errors)
    validate_no_placeholders(
        [
            "README.md",
            "requirements.txt",
            "deploy/ci_cd_pipeline.yaml",
            "configs/default_config.yaml",
            "scripts/acceptance_run_validator.py",
            "scripts/consistency_validator.py",
            "scripts/context_sync.py",
            "scripts/context_governance_check.py",
            "scripts/context_diff_guard.py",
            "scripts/launch_governance_validator.py",
        ],
        errors,
    )

    diff_guard_cmd = [sys.executable, str(ROOT / "scripts" / "context_diff_guard.py")]
    diff_guard_result = subprocess.run(diff_guard_cmd, capture_output=True, text=True)
    if diff_guard_result.returncode != 0:
        details = (diff_guard_result.stdout + diff_guard_result.stderr).strip().replace("\n", " | ")
        errors.append(
            ValidationError(
                "scripts/context_diff_guard.py",
                f"context diff guard failed: {details}",
            )
        )

    consistency_cmd = [sys.executable, str(ROOT / "scripts" / "consistency_validator.py")]
    result = subprocess.run(consistency_cmd, capture_output=True, text=True)
    if result.returncode != 0:
        details = (result.stdout + result.stderr).strip().replace("\n", " | ")
        errors.append(
            ValidationError(
                "scripts/consistency_validator.py",
                f"strict consistency check failed: {details}",
            )
        )

    governance_cmd = [sys.executable, str(ROOT / "scripts" / "context_governance_check.py")]
    governance_result = subprocess.run(governance_cmd, capture_output=True, text=True)
    if governance_result.returncode != 0:
        details = (governance_result.stdout + governance_result.stderr).strip().replace("\n", " | ")
        errors.append(
            ValidationError(
                "scripts/context_governance_check.py",
                f"context governance check failed: {details}",
            )
        )

    launch_gov_cmd = [sys.executable, str(ROOT / "scripts" / "launch_governance_validator.py")]
    launch_gov_result = subprocess.run(launch_gov_cmd, capture_output=True, text=True)
    if launch_gov_result.returncode != 0:
        details = (launch_gov_result.stdout + launch_gov_result.stderr).strip().replace("\n", " | ")
        errors.append(
            ValidationError(
                "scripts/launch_governance_validator.py",
                f"launch governance validation failed: {details}",
            )
        )

    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate repository structure and content quality.")
    parser.parse_args()

    errors = run_validation()
    if errors:
        print("Validation failed with the following issues:")
        for error in errors:
            print(f"- {error.location}: {error.message}")
        return 1

    print("All repository validations passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
