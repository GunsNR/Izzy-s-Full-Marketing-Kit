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

# LIFECYCLE_CRM_SYSTEM

## Objective
Build lifecycle automation and CRM logic that increases repeat purchase while controlling messaging risk.

## Core Flows
1. Welcome (3 emails + 1 SMS): onboarding protocol.
2. Abandoned Cart (2 emails + 1 SMS): objection + trust reinforcement.
3. Browse Abandonment: category education + social proof.
4. Post-purchase: usage success milestones + refill timing.
5. Cross-sell/Upsell: flavor expansion at day 21.
6. Review request: day 14 product experience capture.
7. Winback: 45/60/90 day reactivation sequence.

## Segmentation Model
- New buyer (<30 days)
- Active subscriber
- One-time repeat buyer
- At-risk lapse (>45 days no purchase)

## CRM Field Logic
- `primary_use_case`
- `flavor_preference`
- `training_frequency`
- `subscription_status`
- `last_objection_tag`

## Risk Controls
- **Risk gate:** High-blast-radius automations (pricing, cancellation flow changes) require human review.
- Frequency cap: max 4 promotional messages/week per profile.
