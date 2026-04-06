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

# PAID_MEDIA_SYSTEM

## Objective
Define a controlled paid acquisition plan with clear guardrails and test logic.

## Channel Selection Logic
- Primary: Meta prospecting + retargeting.
- Secondary: Google Search high-intent terms.
- Tertiary: Creator whitelisting once baseline CAC is stable.

## Campaign Architecture
- TOF: 3 angle sets x 3 creative formats.
- MOF: social proof + ingredient transparency retargeting.
- BOF: offer + urgency for cart/checkout abandoners.

## Budget Guardrails
- **Provisional:** Start at $150/day blended until stable CVR baseline.
- **Risk gate:** Budget increases >20% in a week require human approval.

## Creative Test Matrix
- Hooks: fatigue dip, schedule overload, training consistency.
- Formats: UGC talk-through, founder explainer, static pain/solution.
- Offers: starter protocol, bundle savings, subscription convenience.

## Stop-loss Rules
- Pause ad set after 2.5x target CPA without improving CTR trend.
- Pause creative after frequency >3.5 with declining CVR.
