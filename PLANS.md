# Build Plan and Validation Model

## Definition of Done
Done when required docs/skills/evals/scripts exist, pass milestone validations, and integrated pilot plan is ready with risk-aware execution logic.

## Milestones

### M1 — Doctrine + Governance Foundation
**Scope:** doctrine, AGENTS, plans, build log, quality gates, evidence policy, architecture.
**Acceptance criteria:**
- Required governance docs exist.
- Three gates documented and actionable.
- Evidence labels + source ladder documented.
**Validation checks:**
- File existence check.
- Manual consistency review across doctrine, evidence, gates.
**Stop/Fix rule:** stop expansion; patch docs; revalidate.

### M2 — Core Skill Wave (12 Skills)
**Scope:** orchestrator + 11 core execution/support skills.
**Acceptance criteria:**
- Every skill has required YAML metadata and required section structure.
- Every skill includes KPI link, evidence policy, QA bar, escalation policy, update logic.
**Validation checks:**
- Pattern checks for required section headings.
- Spot-check cross-skill handoffs.
**Stop/Fix rule:** freeze new skill creation until structure and handoffs pass.

### M3 — Quality + Proof + Reviews
**Scope:** proof-asset pipeline, handoff SLA, review templates, safe mode, update/changelog/benchmark docs.
**Acceptance criteria:**
- Proof asset templates exist and are reusable.
- Weekly/monthly/quarterly review formats include: learned / next / stop.
**Validation checks:**
- Template completeness and consistency check.
**Stop/Fix rule:** repair templates before updater logic.

### M4 — Eval + Updater Layer
**Scope:** eval prompt CSVs + benchmark/regression/update scripts.
**Acceptance criteria:**
- Routing, critical workflows, negative controls covered.
- Repeated-error and change-detection logic documented.
**Validation checks:**
- CSV header/row sanity checks.
- Script markdown completeness review.
**Stop/Fix rule:** quarantine updater changes and fix logic gaps.

### M5 — Integrated Pilot
**Scope:** one practical pilot with offer, ICP, channels, experiments, nurture, reporting standard.
**Acceptance criteria:**
- Includes runbook, gates, measurements, and review format.
**Validation checks:**
- Pilot includes all mandated components.
**Stop/Fix rule:** revise pilot before declaring done.

## Expansion Criteria
Expand to lower-priority modules only after M1–M5 validations pass or failures are logged with explicit remediation owner/date in `docs/BUILD_LOG.md`.
