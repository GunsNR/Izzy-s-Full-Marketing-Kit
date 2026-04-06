#!/usr/bin/env python3
"""Validate deployment-governance readiness artifacts for launch process."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RUN_DIR = ROOT / "test_runs" / "ecommerce_full_stack_acceptance_001"

REQUIRED_DOCS = [
    "docs/DEPLOYMENT_GOVERNANCE_POLICY.md",
    "docs/LAUNCH_APPROVAL_FRAMEWORK.md",
    "docs/CLAIMS_SUBSTANTIATION_POLICY.md",
    "docs/PRICING_AND_UNIT_ECONOMICS_POLICY.md",
    "docs/ANALYTICS_LAUNCH_READINESS_STANDARD.md",
    "docs/PRELAUNCH_QA_STANDARD.md",
]

REQUIRED_RUN_ARTIFACTS = [
    "SUPPLIER_SOURCING_INTAKE.md",
    "CLAIMS_SUBSTANTIATION_REVIEW.md",
    "PRICING_UNIT_ECONOMICS_APPROVAL.md",
    "PAID_BUDGET_APPROVAL.md",
    "ANALYTICS_LAUNCH_READINESS.md",
    "PRELAUNCH_QA_CHECKLIST.md",
    "GO_NO_GO_SCORECARD.md",
    "LAUNCH_SIGNOFF_QUEUE.md",
    "DEPLOYMENT_RISK_REGISTER.md",
]

REQUIRED_SECTIONS = {
    "SUPPLIER_SOURCING_INTAKE.md": ["## Supplier Status", "## Evidence Class", "## Approval Status", "## Unresolved Risks"],
    "CLAIMS_SUBSTANTIATION_REVIEW.md": [
        "## Claim Category",
        "## Allowed Claim Boundary",
        "## Disallowed Claim Examples",
        "## Substantiation Status",
        "## Legal/Compliance Review Status",
        "## Approval Status",
        "## Unresolved Risks",
    ],
    "PRICING_UNIT_ECONOMICS_APPROVAL.md": ["## Price Point", "## Approval Status", "## Evidence Class", "## Unresolved Risks"],
    "PAID_BUDGET_APPROVAL.md": ["## Test Budget", "## Approval Threshold", "## Approval Status", "## Unresolved Risks"],
    "ANALYTICS_LAUNCH_READINESS.md": [
        "## KPI Tracking Map",
        "## Primary Conversion Events",
        "## QA Completion Status",
        "## Approval Status",
        "## Unresolved Instrumentation Risks",
    ],
    "PRELAUNCH_QA_CHECKLIST.md": ["## Copy QA Complete", "## Signoff Status Complete", "## Approval Status", "## Unresolved Risks"],
    "GO_NO_GO_SCORECARD.md": [
        "## Decision",
        "## Unresolved Critical Risks",
        "## Unresolved Major Risks",
        "## Blocking Dependencies",
        "## Required Owners",
        "## Next Decision Date",
    ],
    "LAUNCH_SIGNOFF_QUEUE.md": ["## Signoff Queue", "## Owner Tracking", "## Approval Status", "## Unresolved Risks"],
    "DEPLOYMENT_RISK_REGISTER.md": ["## Critical Risks", "## Owners", "## Approval Status", "## Unresolved Risks"],
}

ROLLBACK_SECTION_OPTIONS = (
    "## Rollback Plan",
    "## Rollback",
    "## Rollback/Troubleshooting Owner",
)


@dataclass(frozen=True)
class LaunchGovernanceIssue:
    severity: str
    file: str
    message: str


def run_validation(run_dir: Path = RUN_DIR) -> list[LaunchGovernanceIssue]:
    issues: list[LaunchGovernanceIssue] = []

    for rel in REQUIRED_DOCS:
        if not (ROOT / rel).exists():
            issues.append(LaunchGovernanceIssue("MAJOR", rel, "missing required deployment-governance policy doc"))

    for rel in REQUIRED_RUN_ARTIFACTS:
        path = run_dir / rel
        if not path.exists():
            severity = "CRITICAL" if rel in {"GO_NO_GO_SCORECARD.md", "CLAIMS_SUBSTANTIATION_REVIEW.md"} else "MAJOR"
            issues.append(LaunchGovernanceIssue(severity, rel, "missing required deployment-governance artifact"))
            continue

        text = path.read_text(encoding="utf-8")
        for section in REQUIRED_SECTIONS.get(rel, []):
            if section not in text:
                issues.append(LaunchGovernanceIssue("MAJOR", rel, f"missing required section: {section}"))

        if "Human Owner" not in text and "## Owner" not in text and "## Owners" not in text and "## Owner Tracking" not in text:
            issues.append(LaunchGovernanceIssue("MAJOR", rel, "missing explicit owner field"))

        if "Approval Status" not in text:
            issues.append(LaunchGovernanceIssue("MAJOR", rel, "missing explicit approval/status field"))

        if "Evidence Class" not in text and "Evidence Status" not in text:
            issues.append(LaunchGovernanceIssue("MINOR", rel, "missing explicit evidence label field"))

        if "Unresolved" not in text:
            issues.append(LaunchGovernanceIssue("MAJOR", rel, "missing unresolved risk section"))

        if not any(section in text for section in ROLLBACK_SECTION_OPTIONS):
            issues.append(LaunchGovernanceIssue("MAJOR", rel, "missing explicit rollback section"))

    go_no_go_path = run_dir / "GO_NO_GO_SCORECARD.md"
    if go_no_go_path.exists():
        go_text = go_no_go_path.read_text(encoding="utf-8")
        decision_line = ""
        for line in go_text.splitlines():
            if line.strip().startswith("- Current Decision:"):
                decision_line = line.split(":", 1)[1].strip()
                break
        if decision_line not in {"GO", "GO WITH CONDITIONS", "NO-GO"}:
            issues.append(LaunchGovernanceIssue("CRITICAL", "GO_NO_GO_SCORECARD.md", "missing valid go/no-go decision"))

    return sorted(issues, key=lambda i: (i.severity, i.file, i.message))


def main() -> int:
    issues = run_validation()
    if issues:
        print("Launch governance validation failed:")
        for issue in issues:
            print(f"- [{issue.severity}] {issue.file}: {issue.message}")
        return 1

    print("Launch governance validation passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
