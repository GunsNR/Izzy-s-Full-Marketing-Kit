---
business_context:
  schema_version: "1.0"
  run_id: ecommerce_full_stack_acceptance_001
  brand_name: Field Current
  product_category: electrolyte hydration sticks
  niche: performance hydration for active professionals
  core_offer: 30-stick variety pack
  pricing_band: ">=65% gross margin list / >=55% post-discount"
  purchase_model: subscription-first with one-time option
  primary_icp: Commuter Athletes (25-40)
  secondary_icp: Desk-to-Gym Operators
  risk_class: medium-high
  compliance_sensitivity: hydration and performance-language claims require review
  approved_claims_boundary: allow hydration/routine claims; disallow disease-treatment and guaranteed-performance claims
  primary_channels: Meta paid social, Google Search
  retention_model: lifecycle email and sms
  primary_kpis: Revenue (sessions x CVR x AOV), retention, MER/CAC payback/contribution margin
---

# MEASUREMENT_REPORTING_SYSTEM

## Objective
Establish a source-of-truth measurement framework for launch and optimization loops.

## KPI Tree
- Primary: Net revenue, contribution margin.
- Secondary: CVR, AOV, MER, CAC payback.
- Retention: subscription retention rate, repeat purchase rate, churn.

## Tracking Plan
- GA4 + ad platform + Shopify reconciliation.
- Event set: `view_item`, `add_to_cart`, `begin_checkout`, `purchase`, `subscribe_start`, `subscribe_cancel`.

## Dashboard Spec
- Daily pulse: spend, revenue, MER, CVR.
- Weekly strategy: cohort retention, creative fatigue, landing-page performance.
- Monthly executive: contribution margin, payback trajectory, top bottlenecks.

## Experiment Log Format
- Hypothesis
- Evidence label
- Change implemented
- Metric window
- Result
- Decision (scale/hold/rollback)

## Weekly Memo Format
- What we learned
- What we will do next
- What we will stop
