# Update Policy

## Update Cadence
- Weekly: learning memo + minor backlog reprioritization.
- Monthly: strategy review + KPI tree check.
- Quarterly: playbook review + benchmark/regression analysis.

## Proposed vs Approved
- Proposed updates are quarantined until gate checks and approvals complete.
- Approved updates require changelog entry + version bump.

## Version Bump Rules
- Patch: wording/template fixes, no logic changes.
- Minor: workflow or decision-rule changes without architecture break.
- Major: orchestration, gate logic, or dependency model changes.

## Rollback
All non-trivial updates require explicit rollback note and trigger conditions.
