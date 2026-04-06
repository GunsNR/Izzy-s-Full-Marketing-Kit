# Business Context Change Log Template

Use this template inside `test_runs/<run-id>/BUSINESS_CONTEXT_CHANGELOG.md`.

## Required Entry Fields
- Change date
- Run ID
- Changed field(s)
- Old value
- New value
- Reason for change
- Business impact
- Validation impact
- Schema version impact
- Required resync scope
- Reviewer
- Approver
- Rollback note

## Suggested Structured Front Matter
```yaml
---
governance:
  run_id: <run-id>
  reviewer: <name>
  approver: <name>
  approval_date: <YYYY-MM-DD>
  rationale: <why>
  business_impact: <impact>
  validation_impact: <validator/test impact>
  schema_version_impact: <none|bump required|bump performed>
  schema_change_note: <required when fields are added/removed/renamed>
  resync_scope: <files or all required artifacts>
  rollback_note: <rollback path>
  material_change_ack: "true|false"
  tracked_context:
    schema_version: "1.0"
    run_id: <run-id>
    ...
---
```

## Reviewer Guidance
- Material meaning changes require explicit approval and material-change acknowledgement.
- Schema-impacting changes require schema-change note and version review.
