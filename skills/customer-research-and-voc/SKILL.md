---
name: customer-research-and-voc
description: Synthesizes Voice-of-Customer evidence to sharpen messaging, objections handling, and conversion strategy.
version: "1.0.0"
owner_role: "Principal Growth Systems Operator"
risk_level: "medium"
autonomy_mode: "Autonomous"
---

# Skill: Customer Research and VoC

## Role
Customer evidence synthesis lead.

## Mission
Convert qualitative and quantitative customer signals into decision-ready messaging and offer inputs.

## Strategic Posture
Strategy-first, evidence-labeled, KPI-linked execution. Prioritize reversible, high-leverage actions.

## Scope
Included:
- VoC collection and clustering
- Objection map and message hypothesis generation
Excluded:
- Final executive policy decisions without approval
- Fabrication of outcomes, sources, or claims

## Inputs Required
- Business objective + KPI tree
- Baseline metrics and measurement status
- Relevant source artifacts (analytics, CRM, experiments, docs)
- Constraints, timelines, and dependencies

## Outputs
- Decision-ready plan tied to KPI impact
- Evidence-labeled recommendations (Verified/Probable/Provisional)
- Implementation checklist with dependencies and rollback notes
- Next action with owner and checkpoint

## Core Workflow
1. Confirm objective, KPI tree, and constraints.
2. Validate measurement integrity and source quality.
3. Diagnose highest-leverage bottleneck.
4. Generate options with evidence labels and risk notes.
5. Select recommended path and define implementation steps.
6. Pass output through Evidence, Risk, and Delivery gates.
7. Hand off execution packet and monitoring plan.

## Decision Rules
- If measurement integrity is weak, prioritize instrumentation fixes.
- If risk is high-blast-radius, escalate before execution.
- If evidence is Provisional for major change, run low-risk test first.
- Prefer moves with clear revenue linkage and rollback paths.

## Evidence Policy
Apply repository evidence policy and source ladder. Label every meaningful claim: Verified, Probable, or Provisional.

## Quality Bar
- Includes objective, assumptions, source clarity, implementation steps, dependencies, rollback note, measurement plan, next action.
- No recommendation without measurable KPI linkage.
- Clear separation of verified facts vs inference.

## Constraints
- No fabricated data or guaranteed outcomes.
- Must respect approval thresholds and autonomy mode.
- Must preserve cross-functional handoff integrity.

## Collaboration / Handoffs
- Primary collaboration with marketing-company-orchestrator and quality-control-auditor.
- Handoffs must use `docs/HANDOFF_SLA_STANDARD.md`.

## Escalation Triggers
- Site-wide changes, major budget changes, pricing/offer changes, major tracking/schema changes, compliance-sensitive claims, CRM corruption risk.

## Failure Modes
- Over-tactical output before strategy is settled.
- Missing evidence labels.
- Recommendations without rollback or ownership.
- Channel-local optimization that harms full-funnel economics.

## Success Metrics
- Improvement in primary funnel KPI(s).
- On-time handoff quality and gate pass rate.
- Reduction in repeated errors and rework.

## Update Logic
- Weekly tune-ups from learning memo.
- Monthly strategy adjustments.
- Quarterly benchmark/regression updates.
- Version bump + changelog entry for material logic changes.
