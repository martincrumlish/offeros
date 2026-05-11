# Copy Plan Contract

`copy-plan.json` is the canonical Copy Studio source. Codex authors it; `scripts/build_copy.py` validates and renders it into clean written `copy.md`, internal `copy-blueprint.md`, and `sales-page-blueprint.json`.

`copy.md` is the actual long-form sales copy shown in the delivery dashboard. It must read like written sales copy, not a framework document, schema dump, or planning table.

`copy-blueprint.md` keeps the internal section blueprint, framework metadata, and copy-rendering map. Do not put those tables in `copy.md`.

Required metadata:

- `schema: "offeros/copy-plan/v1"`
- `framework: "modern-brunson-long-form-v1"`
- `standaloneCopyRequired: true`
- `vslDependency: "optional-supporting-asset"`

Required commercial fields:

- offer name, price, audience, awareness level, market sophistication
- core promise and primary pain
- 3+ failed alternatives with why each fails and what is needed instead
- new insight / epiphany
- named unique mechanism with 3+ steps
- proof plan with proof before offer
- structured product reveal
- offer stack with 8+ value-explained deliverables
- value logic, guarantee, 7+ objections, and real urgency basis

Each `sectionPlan` row must include:

- `sectionId`
- `frameworkRole`
- `conversionJob`
- `buyerBeliefBefore`
- `buyerBeliefAfter`
- `primaryClaim`
- `proofOrSupport`
- `copyBlocks`
- `visualNeed`
- `ctaRole`
- `maxWords`

The section plan must include: `hero`, `vsl`, `problem`, `agitation`, `failed-alternatives`, `new-insight`, `mechanism`, `proof`, `before-after`, `product`, `feature-benefit`, `how-it-works`, `offer-stack`, `bonuses`, `pricing`, `guarantee`, `fit`, `faq`, and `final-cta`.
