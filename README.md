# Izzy's Full Marketing Kit

Evidence-based operating system for running full-funnel marketing with reusable skills, governance gates, and update loops.

## What this repository includes
- **Governance docs** for evidence policy, risk controls, quality gates, and operating doctrine.
- **12 modular skills** under `skills/` for strategy, paid media, SEO, experiments, reporting, quality control, and orchestration.
- **Evaluation prompts** under `evals/` for routing, critical workflow coverage, and negative controls.
- **Operational templates** for weekly/monthly/quarterly reviews and proof-asset handoffs.
- **Validation automation** (`scripts/repo_validator.py`) to enforce baseline repository integrity.

## Quick start
1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
2. Run repository validation:
   ```bash
   python scripts/repo_validator.py
   ```
3. Run tests:
   ```bash
   pytest -q
   ```

## Acceptance run canonical-context workflow
For each acceptance run under `test_runs/`, maintain a canonical `RUN_CONTEXT.md` as the single business source of truth. Then run:

```bash
python scripts/acceptance_run_validator.py
python scripts/consistency_validator.py
python scripts/context_sync.py --dry-run
python scripts/context_governance_check.py
```

`consistency_validator.py` runs **strict mode** by default and requires a normalized `business_context` block (including `schema_version`) in front matter for each major acceptance artifact. It checks exact field-level parity against `RUN_CONTEXT.md` and fails on drift by severity class (Critical/Major/Minor).

### Schema evolution + sync workflow
1. Update canonical `business_context` in `RUN_CONTEXT.md` (including `schema_version`).
2. Preview drift safely with `python scripts/context_sync.py --dry-run`.
3. Apply updates with `python scripts/context_sync.py --write`.
4. Confirm governance compliance with `python scripts/context_governance_check.py`.
5. Re-run validators/tests before commit.

### Diff-aware governance guard (early process check)
- Guard command: `python scripts/context_diff_guard.py`
- Governed paths:
  - `test_runs/ecommerce_full_stack_acceptance_001/RUN_CONTEXT.md`
  - required acceptance artifacts containing `business_context`
- Required companion update:
  - `test_runs/ecommerce_full_stack_acceptance_001/BUSINESS_CONTEXT_CHANGELOG.md`

This guard checks the **change set** (not just final state). It fails early when governed context files change without corresponding governance trail updates.

### Local pre-commit enforcement (faster feedback)
Install local hooks:

```bash
python scripts/install_hooks.py
```

What it does:
- Configures `core.hooksPath` to `.githooks`
- Installs/uses `.githooks/pre-commit`
- Runs `context_diff_guard.py` against staged files before commit

Troubleshooting:
- If a commit is blocked, update `BUSINESS_CONTEXT_CHANGELOG.md` and required governance metadata, re-stage files, and retry.
- Emergency bypass (must be justified and documented): `git commit --no-verify`
- CI still enforces the same guard even if bypass is used locally.

## Operating model
All major outputs should include:
1. Objective tied to business KPI(s)
2. Assumptions
3. Source clarity (**Verified / Probable / Provisional**)
4. Implementation steps
5. Dependencies
6. Rollback path
7. Measurement plan
8. Next action with owner

## Deployment governance (launch readiness layer)
Deployment governance is distinct from repository-governance: it controls live-launch risk gates (supplier, claims, pricing/economics, paid budget, analytics QA, prelaunch QA, and final go/no-go decision).

Run before launch:

```bash
python scripts/launch_governance_validator.py
```

Required run artifacts:
- `SUPPLIER_SOURCING_INTAKE.md`
- `CLAIMS_SUBSTANTIATION_REVIEW.md`
- `PRICING_UNIT_ECONOMICS_APPROVAL.md`
- `PAID_BUDGET_APPROVAL.md`
- `ANALYTICS_LAUNCH_READINESS.md`
- `PRELAUNCH_QA_CHECKLIST.md`
- `GO_NO_GO_SCORECARD.md`
- `LAUNCH_SIGNOFF_QUEUE.md`
- `DEPLOYMENT_RISK_REGISTER.md`

Decision states in scorecard:
- `GO`
- `GO WITH CONDITIONS`
- `NO-GO`

Rollback control:
- Every deployment-governance artifact must include an explicit rollback section with trigger, actions, and owner.

## CI checks
`deploy/ci_cd_pipeline.yaml` runs:
- repository validator
- unit tests

This ensures structural quality and protects against incomplete-file regressions.

## Suggested next optimizations
- Add lightweight schema validation for YAML front matter versioning rules.
- Add KPI simulation fixtures for skill-level dry-runs.
- Add changelog automation to enforce update policy on version bumps.
