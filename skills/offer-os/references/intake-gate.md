# OfferOS Intake Gate

Use this gate before creating a sales page page kit. The intake can be short, but it must produce enough structured data to fill `schemas/offer-intake.schema.json` without guessing core commercial facts.

## Required Inputs

- Offer name, category, promise, mechanism, and concrete deliverables.
- Buyer segment, urgent problem, desired outcome, awareness level, objections, and failed alternatives.
- Price, currency, normal/value context, guarantee, and proof level.
- Page-kit decision: page type `direct-response-long-form-vsl`, one Page Kit archetype, one theme preset, checkout target, and `no-embedded-order-form`.
- Brand inputs: voice, logo/design source, constraints, and any forbidden claims.

## Assumption Policy

Prefer `assume-and-record` unless a missing answer changes the offer, compliance posture, price, ownership of supplied assets, or checkout path. Record every meaningful assumption in the intake `assumptions` array and carry it into the blueprint notes when it affects copy or layout.

## Pass Criteria

- `pageKit.pageType` is `direct-response-long-form-vsl`.
- `pageKit.pageKitArchetype` is one of `classic-vsl-longform`, `modern-vsl-software`, `one-page-tripwire`, `challenge-workshop`, or `toolkit-workbook`.
- `pageKit.themePreset` is one of `light-saas-direct-response`, `classic-direct-response`, `bold-webinar`, `premium-editorial`, `fitness-performance`, or `creator-workshop`.
- `pageKit.checkoutTarget` defaults to `#checkout` when no checkout URL is supplied.
- `pageKit.orderFormPolicy` is `no-embedded-order-form`.
- At least three objections are known or responsibly assumed.
- Proof level is explicit, including `substitute` when hard proof is unavailable.
- The offer has enough deliverables to support an 8+ item offer-stack checklist.

If the gate fails, create the smallest useful intake draft, mark unresolved items clearly, and do not mark the page kit release-ready.
