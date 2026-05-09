# Page Kit Reference Standards

These standards define a release-grade OfferOS sales page kit: `offer-intake.json`, `sales-page-blueprint.json`, `theme.json`, built `index.html`, and QA notes.

## Schema Files

- `schemas/offer-intake.schema.json`: source-of-truth intake for buyer, offer, commercial terms, and page-kit policy.
- `schemas/sales-page-blueprint.schema.json`: section contract, hero contract, checkout policy, optional blocks, quality targets, and builder metadata.
- `schemas/theme.schema.json`: portable brand, color, type, layout, and asset contract for page generation.

## Required Page Contract

- Page type: `direct-response-long-form-vsl`.
- Page Kit archetype: choose exactly one of `classic-vsl-longform`, `modern-vsl-software`, `one-page-tripwire`, `challenge-workshop`, or `toolkit-workbook`; default to `classic-vsl-longform` unless the offer format clearly matches another archetype.
- Theme preset: choose exactly one of `light-saas-direct-response`, `classic-direct-response`, `bold-webinar`, `premium-editorial`, `fitness-performance`, or `creator-workshop`; never invent ad hoc theme names.
- Framework: `direct-response-long-form-v1`.
- Composition: `direct-response-composition-v2`.
- Hero: `stacked-vsl-hero-v2`, `stacked-vsl`, `offeros-stacked-vsl-v2`, large 16:9 VSL frame.
- Header/navigation: `navigationPolicy: "no-section-nav"`; logo/brand and optional primary CTA only, no sticky/hover section navigation.
- Visual polish contract: `iconSystem: "branded-icons-v1"` and `imageDisplay: "viewport-constrained-v1"`; card grids/checklists use branded icon/checkmark treatment and support images are constrained rather than rendered at full source size.
- Required section order: `header -> hero -> vsl -> problem -> agitation -> failed-alternatives -> mechanism -> proof -> before-after -> product -> offer-stack -> fit -> pricing -> guarantee -> faq -> final-cta`.
- Proof or proof substitute appears before the main offer stack.
- Offer stack uses `direct-response-buy-box-v1` with bundle visual, 8+ deliverables, value row, CTA, and access/guarantee copy.

## Checkout Policy

The page kit must not include an order form, embedded checkout, payment fields, or credit-card form. Default `checkout.target` to `#checkout`; use an external checkout URL only when supplied. The page may include a buy/checkout anchor section, but the transaction is handled outside the page kit.

## Builder Metadata

Every blueprint records:

- Generator/page-kit version.
- Source template.
- Theme path.
- Output path.
- Build mode.
- Generated timestamp.
- Content source and visual asset plan path.
- QA flags for section markers, no order form, desktop, mobile, and contrast checks.

Do not treat metadata as proof of quality. It is a routing and validation surface; browser QA and commercial review still have to run.
