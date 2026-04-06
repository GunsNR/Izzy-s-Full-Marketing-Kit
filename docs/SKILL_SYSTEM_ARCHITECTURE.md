# Skill System Architecture

## Topology
- **Control plane:** `marketing-company-orchestrator`, `quality-control-auditor`, `skill-updater-and-benchmark-engine`.
- **Strategy plane:** `positioning-and-offer-strategy`, `customer-research-and-voc`.
- **Acquisition/conversion plane:** `seo-technical-audit`, `content-strategy-engine`, `paid-search-operator`, `landing-page-builder`, `experimentation-program-manager`.
- **Retention/measurement plane:** `lifecycle-nurture-builder`, `measurement-reporting-operator`.

## Orchestration Loop
1. Set positioning, ICP, offer, proof system, KPI tree.
2. Validate measurement integrity.
3. Diagnose acquisition/conversion/retention/sales constraints.
4. Prioritize highest-leverage moves.
5. Delegate to relevant skill.
6. QA via Evidence, Risk, Delivery gates.
7. Route approved output to execution.
8. Capture performance + objections + learnings.
9. Publish weekly learning memo.
10. Propose/approve updates when justified.

## Trigger-Based Workflows
Supports: new intake, offer launch, SEO drop, crawl/index issues, paid inefficiency, weak lead quality, low close rate, low LP conversion, nurture underperformance, retention decline, churn spike, messaging confusion, broken analytics, repeated QA failures, CRM hygiene deterioration, proposal win-rate decline.

## Handoff Contract
Each delegated task must pass with:
- objective + KPI target
- assumptions + evidence labels
- dependencies
- execution owner
- due date + checkpoint
- rollback condition
