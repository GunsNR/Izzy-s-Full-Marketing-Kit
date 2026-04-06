# Repository Operating Rules

## Mission
Build and run an evidence-based, modular Codex skill system for full-funnel growth operations.

## Core Rules
1. Systems over personalities; reusable workflows only.
2. No fabricated data, outcomes, citations, or capabilities.
3. Link every major recommendation to business KPIs.
4. Enforce three gates on major outputs: Evidence, Risk, Delivery.
5. Use safe, reversible changes with rollback notes.

## Evidence + Safety
- Label meaningful claims/recommendations: **Verified / Probable / Provisional**.
- Follow source ladder in `docs/EVIDENCE_POLICY.md`.
- Route high-blast-radius changes to human review per `docs/QUALITY_GATES.md`.

## Naming + Versioning
- Skill folders: kebab-case under `/skills/<skill-name>/`.
- Skill files: `SKILL.md` with YAML front matter.
- Version bump rules and changelog policy: `docs/UPDATE_POLICY.md`, `docs/CHANGELOG_POLICY.md`.

## Validation Expectations
- Validate milestones before expansion.
- Stop/fix/revalidate on failed checks (see `PLANS.md`).
- Record assumptions, risks, and validation outcomes in `docs/BUILD_LOG.md`.

## Output Convention
Major outputs must include: objective, assumptions, source clarity, implementation steps, dependencies, rollback (if relevant), measurement plan, next action.
