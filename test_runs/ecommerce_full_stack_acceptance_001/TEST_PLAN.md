# TEST_PLAN — ecommerce_full_stack_acceptance_001

## Objective
Validate this repository as a real operating system by building a full DTC e-commerce company and pressure-testing governance, skills, handoffs, and quality gates.

## Assumptions
- **Verified:** Repository contains 12 core skills, governance docs, eval CSVs, and validator/test automation.
- **Provisional:** No live market-data tools are available in this environment; demand and media assumptions will be marked and queued for live validation.

## Scope
- Skills in scope: orchestrator, customer-research-and-voc, positioning-and-offer-strategy, landing-page-builder, content-strategy-engine, seo-technical-audit, paid-search-operator, lifecycle-nurture-builder, experimentation-program-manager, measurement-reporting-operator, quality-control-auditor, skill-updater-and-benchmark-engine.
- Governance in scope: evidence policy, quality gates, handoff SLA, safe mode, benchmark/update rules.

## Pass/Fail Criteria
1. End-to-end company build artifacts complete (Pass if all required documents exist and are coherent).
2. Evidence labels present on meaningful claims (Pass if all major recommendation blocks use Verified/Probable/Provisional).
3. Delivery-gate completeness (Pass if each major artifact includes objective, assumptions, source clarity, steps, dependencies, rollback, measurement, next action).
4. Rerun loop (Pass if at least 3 cycles executed with logged fixes and rerun outcomes).
5. Repo hardening (Pass if at least one structural repository improvement is implemented and validated).

## Bottlenecks to hunt
- Missing handoff packets.
- Weak evidence labeling consistency.
- Missing human-quality review mechanics.
- Missing acceptance-run regression checks.

## Good-enough-to-launch definition
- **Verified:** 0 critical unresolved issues, 0 unresolved major handoff failures, all first-wave skills exercised at least once, and human-quality rubric average >= 4.0.

## Repo-hardened definition
- **Verified:** Acceptance-run artifacts are machine-checkable; validator and tests pass after fixes.

## Source Clarity
- **Verified:** Validator/test commands and repository file checks in this plan are executable in this environment.
- **Provisional:** Live channel benchmarks require external platform data.

## Dependencies
- Repository scripts/tests.
- Human legal and finance reviewers for high-risk approvals.

## Rollback
If this run introduces low-quality artifacts, remove `test_runs/ecommerce_full_stack_acceptance_001/` and rerun with corrected templates.

## Next Action
Execute product selection and strategy build (Phase 3 onward).
