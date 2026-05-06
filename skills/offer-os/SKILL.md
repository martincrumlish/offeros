---
name: offer-os
description: Build complete commercial offer systems in Codex. Use when the user asks to run OfferOS, ProductOS, build a full offer, create a digital product funnel, create a low-ticket offer, produce sales copy plus sales page plus ads plus emails plus VSL plus PDF product, generate a delivery dashboard, or systemize an offer-building workflow for workshop/student use.
---

# OfferOS

OfferOS builds complete offer systems from sparse input. Treat the offer as the root object and make every asset support the same buyer, promise, mechanism, and deliverable.

Default to `deep` mode unless the user explicitly asks for a fast or lightweight run. `deep` mode means full strategy, full artifacts, critique/revision passes, real visual assets, a customer-ready PDF, a coded page, a presentation-ready VSL deck, a dashboard, and separate technical and commercial QA. Do not produce a thin scaffold, summary, or outline when the user asks for a complete OfferOS run.

## Operating Principle

Prefer action over interrogation. Ask questions only when a missing answer would materially change the offer, legal/compliance risk, brand ownership, or production path. Otherwise make a clear assumption and continue.

## Run Modes

- `deep`: default. Full workshop-grade build with subagents when authorized, rich copy, real assets, product PDF, VSL deck, dashboard, and QA.
- `standard`: full asset set with fewer iterations and less exhaustive research.
- `fast`: useful draft only. Must be explicitly requested.

If output quality feels light, revise it before moving on. The user should not have to ask for depth after choosing a complete run.

## Standard Full Build

Create these outputs for a full run:

1. `offer-os.json` manifest
2. offer architecture
3. `design.md`
4. primary `assets/logo.png`/`.webp` imagegen logo or brand-mark asset
5. long-form sales copy
6. coded sales page
7. supporting images
8. customer-ready PDF product
9. Facebook ads and ad images
10. launch emails
11. VSL deck
12. delivery dashboard
13. QA notes

Every artifact must be a finished working file where possible. Avoid "strategy-only" substitutes for files the user asked to use, publish, record, or give to customers.

## Commercial Quality Rules

These rules are mandatory in `deep` mode:

- Do not confuse file existence with launch readiness. Technical QA can pass while commercial QA fails.
- When the user asks for generated images or a generated design direction with visual assets, use the `imagegen` skill/tool for bitmap hero/product/ad imagery unless blocked. Hand-coded SVGs, CSS diagrams, PIL text cards, and browser screenshots are allowed as diagrams or fallbacks, but they must be labeled with their real provenance and cannot be described as AI-generated images.
- A paid PDF product must feel deliverable. Match depth to price: a low-ticket paid product generally needs a full workbook/playbook with modules, worksheets, examples, blank templates, implementation steps, and visual render QA.
- The coded sales page must follow the OfferOS direct-response section contract and include `data-offeros-section` markers. Do not substitute a short branded product page for the full sales page.
- A VSL deck must be a presentation-ready `.pptx` PowerPoint artifact. HTML, contact sheets, and browser decks are previews, not the primary deck.
- The delivery dashboard must preserve the standard OfferOS modal/iframe preview template. Theme it; do not reinvent it as a static link grid.
- Every major artifact needs a value audit: would the buyer pay for it, use it without extra explanation, and trust the brand more after opening it?

## Source-Generation Mandates

Build from these source patterns instead of inventing replacements:

- Exact recipes: in deep mode, load `references/exact-build-recipes.md` before creating any buyer-facing artifact. Start with the Build Controller Recipe, then follow the artifact recipes. Do not substitute another production path.
- Generator-first: create or maintain a reproducible offer build script under `scripts/build_offer_system.*` or equivalent. If QA finds a defect, fix the generator and regenerate from a clean output. Do not manually patch generated files as the final state.
- Sales page: load `assets/templates/sales-page/section-map.md` and start from `assets/templates/sales-page/page-skeleton.html`. Fill every required `data-offeros-section`; preserve the direct-response hero and buy-box offer-stack contracts exactly, then add/remove only optional sub-blocks inside those sections.
- Sales page type: load `references/sales-page-types.md` before sales copy and choose a page type. Use `direct-response-long-form-vsl` by default for complete low-ticket, cold-traffic, or internet-marketing offers. Record the selected type in `quality.salesPage.pageType`.
- Logo: create a real logo direction before producing the final asset. In deep generated-design runs, use the `imagegen` skill/tool to create the primary logo/brand-mark bitmap (`.png` or `.webp`) unless the user supplied a logo or imagegen is blocked. SVG may be a secondary export, but do not mark a code-vector SVG, HTML/CSS render, or PIL raster as the complete primary logo.
- PDF product: follow the PDF Product Recipe. For $30-$99 paid offers, extracted PDF text below 4,000 words or a product that is mostly repeated explanation/blank lines is a failed product, not a warning.
- Emails: follow the Email Sequence Recipe. Every launch email must include send timing, subject, preview text, campaign role, body copy, and CTA. Repeated boilerplate paragraphs across emails are a failure.
- Dashboard: generate `delivery-dashboard.html` with `scripts/generate_delivery_dashboard.py`. After generation, edit theme variables, logo, imagery, and copy only. Preserve `data-offeros-dashboard="v2-modal"`, modal markup, iframe/image preview behavior, and artifact `data-path`/`data-preview` cards.
- VSL: load `references/vsl-deck-quality.md`, then create the primary `vsl-deck` as `.pptx` using a PowerPoint-capable tool such as `pptxgenjs` or the Presentations plugin when available. Create HTML/contact-sheet output only as `vsl-preview`. The deck artifact `preview` must be browser-safe HTML/image, never the `.pptx` itself.
- Manifest: register source metadata as the artifact is created, including quality fields. Do not backfill optimistic quality scores at the end.
- QA notes: write QA notes from measured outputs and validator/browser results. Do not hard-code page counts, CTA counts, pass/fail status, or warning counts.

If a required source pattern cannot be used, mark the artifact `needs_revision`, record the blocker in `qa-notes.md`, and do not set the manifest status to `complete`.

## Required Sequence

Follow this order unless the user explicitly requests a narrower module:

1. Intake and assumptions
2. Offer architecture
3. Design resolver
4. Brand/name refinement
5. Primary imagegen logo or brand-mark asset
6. PDF product outline and offer stack
7. Sales copy
8. Sales page build
9. Real supporting page graphics with provenance recorded
10. PDF product creation and rendered visual check
11. Ads and ad images
12. Email sequence
13. VSL deck
14. Delivery dashboard
15. Technical QA pass
16. Commercial value audit

Do not build downstream visual assets before upstream design/brand decisions exist. If an upstream asset is missing, create the smallest practical version first.

## Quality Gates

For each major module:

1. Draft the artifact.
2. Critique it against the relevant reference file.
3. Revise weak sections before continuing.
4. Register the artifact in `offer-os.json`.

This is mandatory in `deep` mode for offer architecture, sales copy, sales page, PDF product, ads, emails, VSL deck, and delivery dashboard.

Do not mark `status: complete` until both the module gate and commercial value audit pass. Use `needs_revision` for assets that exist but are thin, placeholder-like, visually weak, or not buyer-ready.

In deep mode, warnings are not shippable. If `validate_offer_outputs.py --strict --no-write` reports any issue or warning, revise the source generator and rerun before handoff.

Browser QA must include sales page, delivery dashboard, and VSL preview at desktop and mobile widths. Horizontal overflow or broken images fail the run.

## Self-Test Requirement

Before handing a revised OfferOS skill or generated offer back to the user, run:

```powershell
python plugins\offer-os\skills\offer-os\scripts\self_test_offer_os_skill.py
```

Maintainers may add `--bad-workspace <path-to-known-bad-output>` when testing against a local regression fixture.

Use the available Python executable. This self-test checks that the skill source contains the exact recipes and that known bad outputs fail for the expected reasons. If the self-test fails, fix the source instructions or validator before asking the user to test again.

## Reference Files

Load only the reference needed for the current step:

- `references/runbook.md`: full execution workflow
- `references/quality-gates.md`: depth standards and revision triggers
- `references/exact-build-recipes.md`: fixed source recipes for fragile artifacts
- `references/module-prompts.md`: internal module prompts/checklists
- `references/manifest-schema.md`: artifact registry contract
- `references/golden-standard.md`: minimum expected richness based on the workshop-quality build
- `references/design-resolver.md`: choosing or creating `design.md`
- `references/asset-sequence.md`: dependency order for visual assets
- `references/copy-frameworks.md`: sales page framework selection
- `references/sales-page-types.md`: sales-page archetype selection and depth rules
- `references/email-frameworks.md`: launch and sales email frameworks
- `references/ad-frameworks.md`: ad angle and creative selection
- `references/pdf-product.md`: customer-ready PDF product requirements
- `references/vsl-deck-quality.md`: VSL deck format, layout, and narration standards
- `references/delivery-dashboard.md`: browser delivery dashboard requirements
- `references/agent-dispatch.md`: how to split work when agents are authorized
- `references/qa-checklist.md`: final validation
- `references/workshop-usage.md`: how students should run OfferOS

## Scripts

Use scripts when helpful:

- `scripts/init_offer_project.py`: create a manifest and standard output folders.
- `scripts/register_artifact.py`: register or update an artifact in `offer-os.json`.
- `scripts/generate_delivery_dashboard.py`: generate a branded asset preview dashboard from `offer-os.json`.
- `scripts/validate_offer_outputs.py`: check expected files, unresolved placeholders, asset provenance, PDF depth, VSL readiness, and commercial QA metadata.
- `scripts/self_test_offer_os_skill.py`: self-test exact recipe coverage and known bad output regressions.

Run scripts from the project root. Keep generated files inside the active workspace.

## Design Inputs

Support:

- existing `design.md`
- URL reference
- uploaded screenshots
- generated design archetype
- hybrid instructions

If a URL or screenshot is used, extract a practical design guide before building pages or graphics. Do not clone protected brand assets unless the user owns them.

## Agent Use

Use subagents only when the user explicitly allows delegation or asks to dispatch agents. Delegate concrete, bounded work that can run in parallel. Keep final integration and QA in the main agent.

## Completion Standard

A full OfferOS run is complete only when the buyer-facing product exists, the funnel assets exist, the delivery dashboard links/previews the assets, validation has been run, and the final response clearly lists any limits or checks that could not be completed.
