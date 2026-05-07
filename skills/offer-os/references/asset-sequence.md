# Asset Sequence

Generate assets in dependency order. Earlier assets define constraints for later ones.

## Core Sequence

1. Offer/page direction
2. Design guide
3. Logo or wordmark
4. Product outline and offer stack
5. Sales copy and section-by-section copy blueprint
6. `visual-asset-plan.md` v2 anchored to the copy blueprint
7. Sales page graphics
8. Sales page structure/build
9. Product bundle
10. PDF product visuals
11. VSL frames
12. Ads and social creative
13. Delivery dashboard
14. Secondary exports and variants

## Provenance Requirements

Record provenance for every visual artifact in `offer-os.json`.

- Use `imagegen` for bitmap hero, product, and ad imagery when the user asks for generated images, a generated design direction, or ad images.
- Do not use SVG files for generated diagrams or visuals. Use HTML/CSS blocks, canvas, or rendered PNG diagrams when a structured diagram is needed.
- Use `html-css`, `pil-generated`, or `screenshot` only when that is the honest source.
- Do not describe PIL text cards, CSS panels, rendered diagrams, or screenshots as "generated images." They can be useful fallbacks, but they must be labeled as such. SVG files are not an allowed fallback in OfferOS deep generated-design runs.

Deep mode should include at least:

- one professional logo lockup made from imagegen complete-lockup candidates first, exact readable wordmark, and lockup preview
- one hero or product image that sells the offer visually
- three ad images with actual creative direction
- 6+ PDF-specific visuals/treatments, with 4+ not reused from the sales page
- 12+ VSL visual assets/treatments, with 8+ not reused from the sales page
- deck or VSL preview imagery

## Visual Asset Plan

Create `visual-asset-plan.md` v2 after `copy.md` includes the sales-page section blueprint and before building sales-page graphics, the PDF product, ad images, the VSL deck, or the delivery dashboard.

The plan must split visuals into:

- visual plan metadata
- global brand assets
- sales page visuals
- PDF product visuals
- VSL deck visuals
- ad visuals
- dashboard visuals
- reuse rules

Record `visualPlanStage: post-content-blueprint`, `copyBlueprintUsed: true`, and `salesPageImageSystem: mixed-direct-response-v1`.

Do not treat sales-page graphics as the default image library for every artifact. Each artifact has its own job:

- Sales page visuals sell belief and the offer stack. They must be tied to real copy anchors and use a mixed direct-response system, not an all-mockup image set by default.
- PDF visuals help the buyer use the product: covers, module dividers, matrices, completed examples, blank worksheets, checklists, and implementation maps.
- VSL visuals help a spoken pitch hold attention: pattern interrupts, problem maps, comparison tables, mechanism diagrams, product reveal, stack, value, guarantee, objection, and CTA visuals.
- Ad visuals interrupt the feed and should be generated specifically for the ad angle.

Sales-page visual kinds:

- use `product-mockup`, `dashboard-mockup`, and `offer-stack-bundle` for product reveal, dashboard preview, offer stack, and CTA bundle visuals
- use `mechanism-diagram`, `comparison-visual`, `proof-demo-visual`, `structured-panel`, `buyer-situation-photo`, or `hero-vsl-frame` for mechanism, failed alternatives, proof/demo, objections, problem/agitation, and feature specifics
- require `copyAnchor`, `conversionJob`, `artifactTarget`, `aspectRatio`, and `textRule` for every planned sales-page visual
- avoid busy fake UI, random SaaS mockups, tiny hallucinated screen text, and decorative images that do not support a specific claim

Minimum deep-mode budgets:

- sales page: 4+ visual slots
- PDF product: 6+ visuals/treatments, with 4+ PDF-specific
- VSL deck: 12+ visuals/treatments, with 8+ VSL-specific
- ads: 3+ ad-specific imagegen creatives

Register `visual-asset-plan` and set `quality.images.hasArtifactSpecificPlan = true`. Record whether each visual is shared or artifact-specific.

When agents are authorized, dispatch imagegen visual workers immediately after the post-copy plan exists and before artifact production. Give each worker disjoint ownership:

- page visuals: `assets/page/`
- PDF visuals: `output/pdf/assets/`
- VSL visuals: `output/presentation/assets/`
- ad visuals: `assets/ads/`

Use the same `design.md`, `copy.md`, frozen final `assets/logo.png`, and visual plan as references for every worker. Do not give workers rejected logo concepts, rejected logo candidates, or `logo-mark` alternatives as style references.

## Dependencies

### Offer Direction

Required before:

- design guide
- logo
- sales page
- product visuals
- VSL
- ads

Defines audience, promise, mechanism, category, price point, tone, and conversion goal.

### Design Guide

Required before page design, logo refinement, graphics, bundle visuals, dashboard, and VSL style frames.

### Logo

Required before sales page graphics, product bundle, badges, VSL title cards, ad creatives, and dashboard branding.

Minimum logo prerequisites:

- offer name
- audience
- core promise
- market category
- desired tone
- 3 concept directions
- selected concept rationale
- small-size and one-color checks
- bitmap preview/export for QA

In deep generated-design runs, the primary logo artifact must be an `imagegen` or `imagegen-composite` `.png` or `.webp` horizontal logo lockup that includes the readable offer name. Start with imagegen complete logo lockup candidates. The imagegen brand mark alone can be saved as `assets/logo-mark.png` only as a fallback after complete-lockup attempts fail exact text; it is not the primary logo. Do not create or register SVG logo files, even as secondary exports or drafts. If imagegen was blocked, record the blocker in `quality.logo.imagegenNotUsedReason` and keep the logo/run out of complete status.

The mark must be a simple logo-grade symbol, not an illustration, page-curl/folded-paper image, app icon, mockup, or rough cover graphic. The final `assets/logo.png` must preserve the exact offer name and pass typography, kerning, mark scale, and spacing checks. A bad mark with text composited beside it is still a failed logo.

After the final logo is accepted, freeze the brand lockup:

- `assets/logo.png` is the only downstream logo reference.
- Rejected concept images and rejected candidate lockups are QA artifacts only and must not be used as imagegen references.
- Do not ask imagegen to generate or redraw the logo in product mockups, ads, VSL visuals, PDF visuals, or page graphics.
- If a visual needs the logo, leave a blank/safe logo area in the generated image and composite or place `assets/logo.png` later using the build script, HTML/CSS, or PPTX placement.

### Sales Copy Blueprint

Required before page-specific graphics, VSL visuals, ad angles, and checkout graphics. The copy blueprint defines the sales-page sections, objections, proof jobs, CTAs, visual blocks, `copyAnchor` values, and suggested `visualKind` values.

### Product Bundle

Required before dashboard, product mockups, VSL product reveal, offer stack graphics, and ads that show the deliverable.

The product bundle should show the buyer what they get. If it is a coded diagram, call it a diagram. If it is a generated bitmap mockup, save the prompt/provenance in the manifest.

## Fast Path

If speed matters, still preserve:

1. offer direction
2. lightweight design guide
3. primary `assets/logo.png`/`.webp` imagegen-based logo lockup with readable offer name
4. page/product graphics
5. ads/VSL/dashboard variants

Do not skip the design guide entirely.
