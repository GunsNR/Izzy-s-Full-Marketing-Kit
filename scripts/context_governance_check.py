#!/usr/bin/env python3
"""Governance checks for versioned business_context changes."""

from __future__ import annotations

import argparse
from dataclasses import dataclass
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from scripts.consistency_validator import run_validation as run_consistency_validation

DEFAULT_RUN_DIR = Path("test_runs/ecommerce_full_stack_acceptance_001")
CHANGELOG_FILE = "BUSINESS_CONTEXT_CHANGELOG.md"

REQUIRED_FIELDS = [
    "schema_version",
    "run_id",
    "brand_name",
    "product_category",
    "niche",
    "core_offer",
    "pricing_band",
    "purchase_model",
    "primary_icp",
    "secondary_icp",
    "risk_class",
    "compliance_sensitivity",
    "approved_claims_boundary",
    "primary_channels",
    "retention_model",
    "primary_kpis",
]

MATERIAL_FIELDS = {
    "brand_name",
    "product_category",
    "core_offer",
    "risk_class",
    "compliance_sensitivity",
    "approved_claims_boundary",
}


@dataclass(frozen=True)
class GovernanceIssue:
    severity: str
    file: str
    message: str


def _extract_front_matter(text: str) -> list[str]:
    lines = text.splitlines()
    if len(lines) < 3 or lines[0].strip() != "---":
        raise ValueError("missing YAML front matter")
    for idx in range(1, len(lines)):
        if lines[idx].strip() == "---":
            return lines[1:idx]
    raise ValueError("unterminated YAML front matter")


def _parse_business_context(front_matter_lines: list[str]) -> dict[str, str]:
    context: dict[str, str] = {}
    in_context = False
    for line in front_matter_lines:
        if line.strip() == "business_context:":
            in_context = True
            continue
        if in_context:
            if line.startswith("  ") and ":" in line:
                key, value = line.strip().split(":", 1)
                context[key.strip()] = value.strip().strip('"')
            elif line.strip():
                break
    return context


def _parse_governance(front_matter_lines: list[str]) -> dict[str, str] | dict:
    governance: dict[str, str] = {}
    tracked_context: dict[str, str] = {}
    in_governance = False
    in_tracked = False

    for line in front_matter_lines:
        stripped = line.strip()
        if stripped == "governance:":
            in_governance = True
            continue

        if not in_governance:
            continue

        if stripped == "tracked_context:":
            in_tracked = True
            continue

        if in_tracked:
            if line.startswith("    ") and ":" in stripped:
                key, value = stripped.split(":", 1)
                tracked_context[key.strip()] = value.strip().strip('"')
                continue
            if stripped:
                in_tracked = False

        if line.startswith("  ") and ":" in stripped and not in_tracked:
            key, value = stripped.split(":", 1)
            governance[key.strip()] = value.strip().strip('"')

    governance["tracked_context"] = tracked_context
    return governance


def run_governance_check(run_dir: Path = DEFAULT_RUN_DIR) -> list[GovernanceIssue]:
    issues: list[GovernanceIssue] = []

    run_context_path = run_dir / "RUN_CONTEXT.md"
    changelog_path = run_dir / CHANGELOG_FILE

    if not run_context_path.exists():
        return [GovernanceIssue("CRITICAL", "RUN_CONTEXT.md", "missing canonical run context")]
    if not changelog_path.exists():
        return [GovernanceIssue("CRITICAL", CHANGELOG_FILE, "missing business context changelog")]

    run_context = _parse_business_context(_extract_front_matter(run_context_path.read_text(encoding="utf-8")))
    governance = _parse_governance(_extract_front_matter(changelog_path.read_text(encoding="utf-8")))
    tracked = governance.get("tracked_context", {})

    for field in REQUIRED_FIELDS:
        if field not in run_context:
            issues.append(GovernanceIssue("CRITICAL", "RUN_CONTEXT.md", f"missing required field: {field}"))
        if field not in tracked:
            issues.append(GovernanceIssue("MAJOR", CHANGELOG_FILE, f"tracked_context missing field: {field}"))

    diffs = sorted([field for field in REQUIRED_FIELDS if run_context.get(field) != tracked.get(field)])

    required_review_fields = ["reviewer", "approver", "approval_date"]
    for field in required_review_fields:
        if not governance.get(field):
            issues.append(GovernanceIssue("MAJOR", CHANGELOG_FILE, f"missing governance field: {field}"))

    if diffs:
        required_change_fields = [
            "rationale",
            "business_impact",
            "validation_impact",
            "schema_version_impact",
            "resync_scope",
            "rollback_note",
        ]
        for field in required_change_fields:
            if not governance.get(field):
                issues.append(GovernanceIssue("MAJOR", CHANGELOG_FILE, f"missing change rationale field: {field}"))

        if any(field in MATERIAL_FIELDS for field in diffs) and governance.get("material_change_ack", "").lower() != "true":
            issues.append(
                GovernanceIssue(
                    "CRITICAL",
                    CHANGELOG_FILE,
                    "material context change detected without material_change_ack=true",
                )
            )

        if "schema_version" in diffs and not governance.get("schema_version_impact"):
            issues.append(GovernanceIssue("CRITICAL", CHANGELOG_FILE, "schema_version changed without schema_version_impact note"))

    key_changes = set(run_context.keys()) ^ set(tracked.keys())
    if key_changes and not governance.get("schema_change_note"):
        issues.append(
            GovernanceIssue(
                "CRITICAL",
                CHANGELOG_FILE,
                f"schema fields added/removed without schema_change_note: {', '.join(sorted(key_changes))}",
            )
        )

    consistency_issues = run_consistency_validation(run_dir, strict_mode=True)
    if consistency_issues:
        issues.append(GovernanceIssue("CRITICAL", "consistency_validator", "artifacts are not resynced to canonical context"))

    return sorted(issues, key=lambda i: (i.severity, i.file, i.message))


def main() -> int:
    parser = argparse.ArgumentParser(description="Check governance requirements for business_context changes.")
    parser.add_argument("--run-dir", default=str(DEFAULT_RUN_DIR), help="Acceptance run directory")
    args = parser.parse_args()

    issues = run_governance_check(Path(args.run_dir))
    if issues:
        print("Business context governance check failed:")
        for issue in issues:
            print(f"- [{issue.severity}] {issue.file}: {issue.message}")
        return 1

    print("Business context governance check passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
