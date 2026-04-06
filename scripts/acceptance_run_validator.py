#!/usr/bin/env python3
"""Validator for required acceptance-test artifacts and minimum quality sections."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RUN_DIR = ROOT / "test_runs" / "ecommerce_full_stack_acceptance_001"

REQUIRED_FILES = [
    "RUN_CONTEXT.md",
    "BUSINESS_CONTEXT_CHANGELOG.md",
    "TEST_PLAN.md",
    "REPO_READINESS_REPORT.md",
    "TEST_LEDGER.md",
    "PRODUCT_SELECTION_MATRIX.md",
    "STRATEGY_FOUNDATION.md",
    "BRAND_SYSTEM.md",
    "WEBSITE_UX_SYSTEM.md",
    "COPY_SYSTEM.md",
    "SEO_CONTENT_SYSTEM.md",
    "PAID_MEDIA_SYSTEM.md",
    "LIFECYCLE_CRM_SYSTEM.md",
    "MEASUREMENT_REPORTING_SYSTEM.md",
    "PROOF_ASSET_SYSTEM.md",
    "QA_AUDIT_CYCLE_01.md",
    "REPO_GAP_ANALYSIS_CYCLE_01.md",
    "REPAIR_LOG_CYCLE_01.md",
    "RERUN_RESULTS_CYCLE_01.md",
    "QA_AUDIT_CYCLE_02.md",
    "REPO_GAP_ANALYSIS_CYCLE_02.md",
    "REPAIR_LOG_CYCLE_02.md",
    "RERUN_RESULTS_CYCLE_02.md",
    "QA_AUDIT_CYCLE_03.md",
    "REPO_GAP_ANALYSIS_CYCLE_03.md",
    "REPAIR_LOG_CYCLE_03.md",
    "RERUN_RESULTS_CYCLE_03.md",
    "FINAL_ACCEPTANCE_REVIEW.md",
    "HUMAN_QUALITY_REVIEW.md",
    "CHANGELOG_PROPOSAL.md",
    "HUMAN_REVIEW_REQUIRED.md",
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

DELIVERY_SECTIONS = [
    "## Objective",
    "## Assumptions",
    "## Source Clarity",
    "## Dependencies",
    "## Rollback",
    "## Next Action",
]

EVIDENCE_LABELS = ["**Verified:**", "**Probable:**", "**Provisional:**"]

MAJOR_OUTPUT_FILES = [
    "TEST_PLAN.md",
    "PRODUCT_SELECTION_MATRIX.md",
    "STRATEGY_FOUNDATION.md",
    "BRAND_SYSTEM.md",
]

CONTEXT_REQUIRED_FILES = [
    "RUN_CONTEXT.md",
    "PRODUCT_SELECTION_MATRIX.md",
    "STRATEGY_FOUNDATION.md",
    "BRAND_SYSTEM.md",
    "WEBSITE_UX_SYSTEM.md",
    "COPY_SYSTEM.md",
    "SEO_CONTENT_SYSTEM.md",
    "PAID_MEDIA_SYSTEM.md",
    "LIFECYCLE_CRM_SYSTEM.md",
    "MEASUREMENT_REPORTING_SYSTEM.md",
    "PROOF_ASSET_SYSTEM.md",
    "FINAL_ACCEPTANCE_REVIEW.md",
    "HUMAN_REVIEW_REQUIRED.md",
]


@dataclass
class ValidationIssue:
    file: str
    message: str


def run_validation() -> list[ValidationIssue]:
    issues: list[ValidationIssue] = []

    if not RUN_DIR.exists():
        return [ValidationIssue(str(RUN_DIR), "acceptance run directory is missing")]

    for filename in REQUIRED_FILES:
        path = RUN_DIR / filename
        if not path.exists():
            issues.append(ValidationIssue(filename, "required file missing"))

    for filename in MAJOR_OUTPUT_FILES:
        path = RUN_DIR / filename
        if not path.exists():
            continue
        text = path.read_text(encoding="utf-8")
        for section in DELIVERY_SECTIONS:
            if section not in text:
                issues.append(ValidationIssue(filename, f"missing delivery section: {section}"))

        if not any(label in text for label in EVIDENCE_LABELS):
            issues.append(ValidationIssue(filename, "missing evidence labels"))

    for filename in CONTEXT_REQUIRED_FILES:
        path = RUN_DIR / filename
        if not path.exists():
            continue
        text = path.read_text(encoding="utf-8")
        has_context = text.startswith("---") and "business_context:" in text.split("---", 2)[1]
        if not has_context:
            issues.append(ValidationIssue(filename, "missing structured business_context front matter block"))
            continue
        if "schema_version:" not in text.split("---", 2)[1]:
            issues.append(ValidationIssue(filename, "missing schema_version in business_context block"))

    return issues


def main() -> int:
    issues = run_validation()
    if issues:
        print("Acceptance-run validation failed:")
        for issue in issues:
            print(f"- {issue.file}: {issue.message}")
        return 1

    print("Acceptance-run validation passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
