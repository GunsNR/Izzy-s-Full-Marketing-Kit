#!/usr/bin/env python3
"""Diff-aware governance guard for business_context changes."""

from __future__ import annotations

import argparse
import subprocess
from dataclasses import dataclass
from pathlib import Path

RUN_DIR_DEFAULT = Path("test_runs/ecommerce_full_stack_acceptance_001")
RUN_CONTEXT = "RUN_CONTEXT.md"
CHANGELOG = "BUSINESS_CONTEXT_CHANGELOG.md"

GOVERNED_ARTIFACTS = {
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
}


@dataclass(frozen=True)
class GuardIssue:
    severity: str
    message: str


def _extract_front_matter(text: str) -> list[str]:
    lines = text.splitlines()
    if len(lines) < 3 or lines[0].strip() != "---":
        raise ValueError("missing YAML front matter")
    for idx in range(1, len(lines)):
        if lines[idx].strip() == "---":
            return lines[1:idx]
    raise ValueError("unterminated YAML front matter")


def _parse_key_values(lines: list[str], block: str, indent: str) -> dict[str, str]:
    values: dict[str, str] = {}
    in_block = False
    for line in lines:
        stripped = line.strip()
        if stripped == block:
            in_block = True
            continue
        if in_block:
            if line.startswith(indent) and ":" in stripped:
                key, value = stripped.split(":", 1)
                values[key.strip()] = value.strip().strip('"')
            elif stripped:
                break
    return values


def _parse_run_context_schema_version(run_context_path: Path) -> str:
    context_lines = _extract_front_matter(run_context_path.read_text(encoding="utf-8"))
    business_context = _parse_key_values(context_lines, "business_context:", "  ")
    return business_context.get("schema_version", "")


def _parse_changelog_governance(changelog_path: Path) -> dict[str, str]:
    lines = _extract_front_matter(changelog_path.read_text(encoding="utf-8"))
    governance = _parse_key_values(lines, "governance:", "  ")
    tracked_context = _parse_key_values(lines, "tracked_context:", "    ")
    governance["tracked_schema_version"] = tracked_context.get("schema_version", "")
    return governance


def detect_changed_files_from_git() -> list[str]:
    commands = [
        ["git", "diff", "--name-only", "HEAD~1", "HEAD"],
        ["git", "diff", "--name-only"],
        ["git", "status", "--porcelain"],
    ]
    for cmd in commands:
        result = subprocess.run(cmd, capture_output=True, text=True)
        if result.returncode != 0:
            continue
        lines = [line.strip() for line in result.stdout.splitlines() if line.strip()]
        if not lines:
            continue
        if cmd[:2] == ["git", "status"]:
            files = [line[3:].strip() for line in lines if len(line) > 3]
        else:
            files = lines
        if files:
            return sorted(set(files))
    return []


def evaluate_diff_guard(changed_files: list[str], run_dir: Path) -> list[GuardIssue]:
    issues: list[GuardIssue] = []
    normalized = sorted({path.replace("\\", "/") for path in changed_files})

    run_context_path = run_dir / RUN_CONTEXT
    changelog_path = run_dir / CHANGELOG
    run_context_changed = any(path.endswith(f"/{RUN_CONTEXT}") or path == RUN_CONTEXT for path in normalized)
    changelog_changed = any(path.endswith(f"/{CHANGELOG}") or path == CHANGELOG for path in normalized)
    artifact_changed = sorted(
        [
            path
            for path in normalized
            if any(path.endswith(f"/{name}") or path == name for name in GOVERNED_ARTIFACTS)
        ]
    )

    if run_context_changed and not changelog_changed:
        issues.append(GuardIssue("CRITICAL", "RUN_CONTEXT.md changed without BUSINESS_CONTEXT_CHANGELOG.md update"))

    if artifact_changed and not changelog_changed:
        issues.append(
            GuardIssue(
                "MAJOR",
                f"business_context artifact changed without changelog update: {', '.join(artifact_changed)}",
            )
        )

    if (run_context_changed or artifact_changed) and changelog_changed:
        if not run_context_path.exists() or not changelog_path.exists():
            issues.append(GuardIssue("MAJOR", "ambiguous diff state: run context or changelog file missing"))
        else:
            run_schema = _parse_run_context_schema_version(run_context_path)
            governance = _parse_changelog_governance(changelog_path)
            tracked_schema = governance.get("tracked_schema_version", "")
            schema_impact = governance.get("schema_version_impact", "")

            if run_schema != tracked_schema:
                issues.append(
                    GuardIssue(
                        "CRITICAL",
                        f"schema_version changed without synced tracked_context (run={run_schema}, tracked={tracked_schema})",
                    )
                )

            if run_schema != tracked_schema and not schema_impact:
                issues.append(GuardIssue("CRITICAL", "schema_version changed without schema rationale note"))

            if run_context_changed and not schema_impact:
                issues.append(GuardIssue("MAJOR", "RUN_CONTEXT.md changed but schema_version_impact is empty"))

    return sorted(issues, key=lambda i: (i.severity, i.message))


def main() -> int:
    parser = argparse.ArgumentParser(description="Diff-aware governance guard for business_context changes.")
    parser.add_argument("--changed-file", action="append", default=[], help="Changed file path (repeatable)")
    parser.add_argument("--run-dir", default=str(RUN_DIR_DEFAULT), help="Acceptance run directory")
    args = parser.parse_args()

    run_dir = Path(args.run_dir)
    changed_files = sorted(set(args.changed_file)) if args.changed_file else detect_changed_files_from_git()

    if not changed_files:
        print("Context diff guard: no changed files detected; pass.")
        return 0

    issues = evaluate_diff_guard(changed_files, run_dir)
    print("Context diff guard inspected files:")
    for path in changed_files:
        print(f"- {path}")

    if issues:
        print("Context diff guard failed:")
        for issue in issues:
            print(f"- [{issue.severity}] {issue.message}")
        return 1

    print("Context diff guard passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
