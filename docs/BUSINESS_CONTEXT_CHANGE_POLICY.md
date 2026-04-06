# Business Context Change Policy

## Objective
Prevent ad-hoc business-context drift by requiring explicit governance records for any `business_context` change.

## Allowed Change Conditions
1. Canonical source is `test_runs/<run-id>/RUN_CONTEXT.md`.
2. Changes are allowed only when a matching changelog governance record is updated.
3. Required artifacts must be resynced after canonical updates via `python scripts/context_sync.py --write`.

## Schema Version Rules
- `schema_version` is mandatory in all `business_context` blocks.
- Bump/review `schema_version` when a field is added, removed, or renamed.
- If schema fields change, `schema_change_note` is mandatory in changelog governance metadata.

## Rationale Rules
- Material fields (brand, product category, core offer, risk class, compliance boundary) require explicit `material_change_ack=true` and rationale.
- Minor non-material updates still require rationale and impact notes.

## Resync Rules
- After canonical change, run:
  1. `python scripts/context_sync.py --dry-run`
  2. `python scripts/context_sync.py --write`
  3. validators/tests
- If artifacts remain out of sync, validation must fail.

## Operator Responsibilities
- Keep changelog governance metadata complete (reviewer, approver, approval date).
- Maintain rollback note for every approved change.
- Ensure governance check passes before commit.

## Rollback Expectations
- Revert to last approved tracked context in changelog if drift is discovered.
- Re-run sync + validators after rollback.
