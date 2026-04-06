#!/usr/bin/env python3
"""Synchronize business_context front matter from RUN_CONTEXT.md to required artifacts."""

from __future__ import annotations

import argparse
from dataclasses import dataclass
from pathlib import Path

DEFAULT_RUN_DIR = Path("test_runs/ecommerce_full_stack_acceptance_001")
REQUIRED_FILES = [
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

CONTEXT_FIELD_ORDER = [
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


@dataclass(frozen=True)
class SyncIssue:
    file: str
    message: str


def _extract_front_matter(text: str) -> tuple[list[str], str]:
    lines = text.splitlines()
    if len(lines) < 3 or lines[0].strip() != "---":
        raise ValueError("missing YAML front matter")

    end_idx = None
    for idx in range(1, len(lines)):
        if lines[idx].strip() == "---":
            end_idx = idx
            break

    if end_idx is None:
        raise ValueError("unterminated YAML front matter")

    front_matter_lines = lines[1:end_idx]
    body = "\n".join(lines[end_idx + 1 :])
    return front_matter_lines, body


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


def _render_front_matter(canonical_context: dict[str, str]) -> list[str]:
    lines = ["business_context:"]
    for key in CONTEXT_FIELD_ORDER:
        value = canonical_context[key]
        lines.append(f'  {key}: "{value}"')
    return lines


def _replace_front_matter_context(front_matter_lines: list[str], canonical_context: dict[str, str]) -> list[str]:
    start_idx = None
    end_idx = None

    for idx, line in enumerate(front_matter_lines):
        if line.strip() == "business_context:":
            start_idx = idx
            end_idx = idx + 1
            while end_idx < len(front_matter_lines):
                line_value = front_matter_lines[end_idx]
                if line_value.startswith("  "):
                    end_idx += 1
                    continue
                if line_value.strip() == "":
                    end_idx += 1
                    continue
                break
            break

    if start_idx is None:
        raise ValueError("missing business_context block")

    return front_matter_lines[:start_idx] + _render_front_matter(canonical_context) + front_matter_lines[end_idx:]


def _diff_fields(current: dict[str, str], canonical: dict[str, str]) -> list[str]:
    changed = []
    for key in CONTEXT_FIELD_ORDER:
        if current.get(key) != canonical.get(key):
            changed.append(key)
    return changed


def sync_context(run_dir: Path, write: bool) -> tuple[list[str], list[SyncIssue]]:
    canonical_file = run_dir / "RUN_CONTEXT.md"
    if not canonical_file.exists():
        return [], [SyncIssue("RUN_CONTEXT.md", "missing canonical RUN_CONTEXT.md")]

    try:
        canonical_front_matter, _ = _extract_front_matter(canonical_file.read_text(encoding="utf-8"))
        canonical_context = _parse_business_context(canonical_front_matter)
    except ValueError as exc:
        return [], [SyncIssue("RUN_CONTEXT.md", f"{exc}")]

    missing_fields = [k for k in CONTEXT_FIELD_ORDER if k not in canonical_context]
    if missing_fields:
        return [], [SyncIssue("RUN_CONTEXT.md", f"missing canonical fields: {', '.join(missing_fields)}")]

    changes: list[str] = []
    issues: list[SyncIssue] = []

    for rel in REQUIRED_FILES:
        path = run_dir / rel
        if not path.exists():
            issues.append(SyncIssue(rel, "required artifact missing"))
            continue

        try:
            front_matter_lines, body = _extract_front_matter(path.read_text(encoding="utf-8"))
            current_context = _parse_business_context(front_matter_lines)
        except ValueError as exc:
            issues.append(SyncIssue(rel, str(exc)))
            continue

        changed_fields = _diff_fields(current_context, canonical_context)
        if not changed_fields:
            continue

        changes.append(f"{rel}: {', '.join(changed_fields)}")

        if write:
            try:
                new_front_matter_lines = _replace_front_matter_context(front_matter_lines, canonical_context)
            except ValueError as exc:
                issues.append(SyncIssue(rel, str(exc)))
                continue

            new_text = "---\n" + "\n".join(new_front_matter_lines) + "\n---\n" + body
            if not new_text.endswith("\n"):
                new_text += "\n"
            path.write_text(new_text, encoding="utf-8")

    return changes, issues


def main() -> int:
    parser = argparse.ArgumentParser(description="Sync business_context front matter from RUN_CONTEXT.md")
    parser.add_argument("--run-dir", default=str(DEFAULT_RUN_DIR), help="Acceptance run directory path")
    parser.add_argument("--dry-run", action="store_true", help="Preview differences only")
    parser.add_argument("--write", action="store_true", help="Apply synchronization changes")
    args = parser.parse_args()

    if args.dry_run == args.write:
        print("Choose exactly one mode: --dry-run or --write")
        return 1

    run_dir = Path(args.run_dir)
    changes, issues = sync_context(run_dir, write=args.write)

    mode_name = "WRITE" if args.write else "DRY-RUN"
    print(f"Context sync mode: {mode_name}")

    if changes:
        print("Out-of-sync fields:")
        for change in sorted(changes):
            print(f"- {change}")
    else:
        print("No out-of-sync fields found.")

    if issues:
        print("Sync issues:")
        for issue in sorted(issues, key=lambda i: (i.file, i.message)):
            print(f"- {issue.file}: {issue.message}")
        return 1

    if args.write and changes:
        print("Synchronization applied.")
    elif args.dry_run and changes:
        print("Dry run complete. Re-run with --write to apply changes.")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
