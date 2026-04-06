#!/usr/bin/env python3
"""Cross-artifact consistency validator for acceptance runs with strict context mode."""

from __future__ import annotations

import argparse
from dataclasses import dataclass
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RUN_DIR = ROOT / "test_runs" / "ecommerce_full_stack_acceptance_001"
RUN_CONTEXT_FILE = RUN_DIR / "RUN_CONTEXT.md"

CHECK_FILES = [
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

REQUIRED_CONTEXT_FIELDS = [
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

CRITICAL_FIELDS = {"brand_name", "product_category", "risk_class", "compliance_sensitivity", "core_offer"}
MAJOR_FIELDS = {"primary_channels", "pricing_band", "secondary_icp", "retention_model", "purchase_model"}
EXPECTED_SCHEMA_VERSION = "1.0"


@dataclass(frozen=True)
class ConsistencyIssue:
    severity: str
    file: str
    message: str


def _extract_front_matter(text: str) -> list[str]:
    lines = text.splitlines()
    if len(lines) < 3 or lines[0].strip() != "---":
        return []

    for idx in range(1, len(lines)):
        if lines[idx].strip() == "---":
            return lines[1:idx]
    return []


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


def parse_context_from_file(path: Path) -> dict[str, str]:
    text = path.read_text(encoding="utf-8")
    return _parse_business_context(_extract_front_matter(text))


def _severity_for_field(field: str) -> str:
    if field in CRITICAL_FIELDS:
        return "CRITICAL"
    if field in MAJOR_FIELDS:
        return "MAJOR"
    return "MINOR"


def run_validation(base_dir: Path = RUN_DIR, strict_mode: bool = True) -> list[ConsistencyIssue]:
    issues: list[ConsistencyIssue] = []

    context_path = base_dir / "RUN_CONTEXT.md"
    if not context_path.exists():
        return [ConsistencyIssue("CRITICAL", "RUN_CONTEXT.md", "Canonical run context file missing")]

    canonical = parse_context_from_file(context_path)
    if not canonical:
        return [ConsistencyIssue("CRITICAL", "RUN_CONTEXT.md", "Missing business_context block in RUN_CONTEXT.md")]

    for field in REQUIRED_CONTEXT_FIELDS:
        if field not in canonical:
            severity = "MAJOR" if field == "schema_version" else "CRITICAL"
            issues.append(ConsistencyIssue(severity, "RUN_CONTEXT.md", f"Missing canonical field: {field}"))

    if canonical.get("schema_version") and canonical["schema_version"] != EXPECTED_SCHEMA_VERSION:
        issues.append(
            ConsistencyIssue(
                "CRITICAL",
                "RUN_CONTEXT.md",
                f"Canonical schema_version mismatch: expected '{EXPECTED_SCHEMA_VERSION}', got '{canonical['schema_version']}'",
            )
        )

    for rel in CHECK_FILES:
        path = base_dir / rel
        if not path.exists():
            issues.append(ConsistencyIssue("MAJOR", rel, "Required artifact missing for consistency checks"))
            continue

        if not strict_mode:
            continue

        artifact_context = parse_context_from_file(path)
        if not artifact_context:
            issues.append(ConsistencyIssue("MAJOR", rel, "Missing structured business_context block"))
            continue

        for field in REQUIRED_CONTEXT_FIELDS:
            if field not in artifact_context:
                issues.append(ConsistencyIssue("MAJOR", rel, f"Missing context field: {field}"))
                continue

            if artifact_context[field] != canonical.get(field, ""):
                if field == "schema_version":
                    severity = "CRITICAL"
                else:
                    severity = _severity_for_field(field)
                issues.append(
                    ConsistencyIssue(
                        severity,
                        rel,
                        f"Field drift on '{field}': expected '{canonical.get(field, '')}', got '{artifact_context[field]}'",
                    )
                )

    return sorted(issues, key=lambda i: (i.severity, i.file, i.message))


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate cross-artifact business-context consistency.")
    parser.add_argument("--mode", choices=["strict"], default="strict")
    parser.parse_args()

    issues = run_validation(strict_mode=True)
    if issues:
        print("Consistency validation failed (strict mode):")
        for issue in issues:
            print(f"- [{issue.severity}] {issue.file}: {issue.message}")
        return 1

    print("Consistency validation passed in strict mode with no field-level drift detected.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
