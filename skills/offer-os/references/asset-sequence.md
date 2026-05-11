# Asset Sequence

Generate assets in dependency order. Earlier assets define constraints for later ones.

## Core Sequence

1. Offer/page direction
2. Design guide
3. Single final logo lockup
4. Product outline and offer stack
5. `copy-plan.json` from Copy Studio
6. Clean written `copy.md`, internal `copy-blueprint.md`, and `sales-page-blueprint.json`
7. `visual-asset-plan.md` v2 anchored to Copy Studio
8. Sales page graphics
9. Sales page structure/build
10. Product bundle
11. PDF product visuals
12. VSL frames
13. Ads and social creative
14. Delivery dashboard
15. Secondary exports and variants

## Provenance Requirements

Record provenance for every visual artifact in `offer-os.json`.

- Use `imagegen` for bitmap hero, product, offer-stack, product-bundle, buyer-situation, and ad imagery when the user asks for generated images, a generated design direction, or ad images.
- Do not use SVG files for generated diagrams or visuals. Use HTML/CSS blocks, canvas, or rendered PNG diagrams when a structured diagram is needed.
- Pillow/PIL is not an OfferOS creative generator. Do not use it to author customer-facing images or register `pil-generated` image artifacts. It may only inspect, crop, resize, compress, or convert imagegen/provided/licensed inputs while preserving the source provenance.
- Use `html-css`, `generated-by-code`, or `screenshot` only when that is the honest source for a real diagram, worksheet preview, rendered page preview, or QA artifact.
- Do not use HTML/CSS, canvas, screenshots, or generated-by-code PNGs as substitutes for primary conversion visuals. In deep generated-design runs, product bundles, offer-stack bundles, product mockups, hero/VSL thumbnails, buyer-situation photos, and ad creatives must be `imagegen-final` unless the user provided/licensed the asset.
- For sales-page primary conversion visuals, the final buyer-facing image must be produced by `imagegen`, not assembled locally. Do not use Pillow, canvas, HTML/CSS screenshots, or local scripts to add logo, headline text, labels, UI cards, badges, mockups, overlays, or product-stack composition after imagegen. Local post-processing is limited to crop, resize, compression, format conversion, and non-creative QA fixes.
- `imagegen-composite` means an imagegen edit/composition using reference images. It does not mean a local PIL/compositor-built final. A primary conversion visual using `imagegen-composite` must record `imagegenNativeComposite: true`, `finalPixelsGeneratedBy: imagegen`, and `localCreativeOverlay: false`; otherwise it fails.
- Do not describe CSS panels, rendered diagrams, or screenshots as "generated images." They can be useful diagram/preview fallbacks, but they must be labeled as such. SVG files are not an allowed fallback in OfferOS deep generated-design runs.

Deep mode should include at least:

- one professional logo lockup made from a single final imagegen logo call, exact readable wordmark, and lockup preview
- one hero or product image that sells the offer visually
- three ad images with actual creative direction
- 6+ PDF-specific visuals/treatments, with 4+ not reused from the sales page
- 12+ VSL visual assets/treatments, with 8+ not reused from the sales page
- deck or VSL preview imagery

## Visual Asset Plan

Create `visual-asset-plan.md` v2 after `copy-plan.json`, clean `copy.md`, `copy-blueprint.md`, and `sales-page-blueprint.json` exist and before building sales-page graphics, the PDF product, ad images, the VSL deck, or the delivery dashboard.

The plan must split visuals into:

- visual plan metadata
- global brand assets
- sales page visuals
- PDF product visuals
- VSL deck visuals
- ad visuals
- dashboard visuals
- reuse rules

Record `visualPlanStage: post-content-blueprint`, `copyBlueprintUsed: true`, `copyStudioUsed: true`, `copyPlanPath: copy-plan.json`, `salesPageImageSystem: mixed-direct-response-v1`, `logoReference: assets/logo.png`, `logoUsagePolicy: use-locked-logo-reference`, and `alternateLogosCreated: false`.

Do not treat sales-page graphics as the default image library for every artifact. Each artifact has its own job:

- Sales page visuals sell belief and the offer stack. They must be tied to real copy anchors and use a mixed direct-response system, not an all-mockup image set by default. Primary conversion visuals in the sales page must be `imagegen-final` or a provided/licensed asset; coded PNG placeholders and local composites do not satisfy the slot.
- PDF visuals help the buyer use the product: covers, module dividers, matrices, completed examples, blank worksheets, checklists, and implementation maps.
- VSL visuals help a spoken pitch hold attention: pattern interrupts, problem maps, comparison tables, mechanism diagrams, product reveal, stack, value, guarantee, objection, and CTA visuals.
- Ad visuals interrupt the feed and should be generated specifically for the ad angle.

Sales-page visual kinds:

- use `product-mockup`, `dashboard-mockup`, and `offer-stack-bundle` for product reveal, dashboard preview, offer stack, and CTA bundle visuals
- use `mechanism-diagram`, `comparison-visual`, `proof-demo-visual`, `structured-panel`, `buyer-situation-photo`, or `hero-vsl-frame` for mechanism, failed alternatives, proof/demo, objections, problem/agitation, and feature specifics
- require `copyAnchor`, `conversionJob`, `artifactTarget`, `aspectRatio`, `aspectRatioReason`, `displayIntent`, `maxDisplayHeight`, and `textRule` for every planned sales-page visual
- choose aspect ratios by page slot instead of using one default image size for every asset; record `aspectRatioPolicy: slot-aware-v1`
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

Use the same `design.md`, `copy-plan.json`, clean `copy.md`, `copy-blueprint.md`, `sales-page-blueprint.json`, frozen final `assets/logo.png`, and visual plan as references for every worker. Do not give workers any other logo image, old logo attempt, rejected logo attempt, or `logo-mark` alternative as a style reference.

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

Required before page design, graphics, bundle visuals, dashboard, and VSL style frames.

### Logo

Required before sales page graphics, product bundle, badges, VSL title cards, ad creatives, and dashboard branding.

Minimum logo prerequisites:

- offer name
- audience
- core promise
- market category
- desired tone
- one final logo direction
- small-size and one-color checks
- bitmap preview/export for QA

In deep generated-design runs, the primary logo artifact must be an `imagegen` `.png` or `.webp` horizontal logo lockup that includes the readable offer name. Create exactly one final logo with imagegen and save it as `assets/logo.png`. Do not create a 3-option logo set, option sheet, alternate lockups, `logo-mark` fallback, SVG logo, or script-composited text logo. If imagegen was blocked, record the blocker in `quality.logo.imagegenNotUsedReason` and keep the logo/run out of complete status.

The mark must be a simple logo-grade symbol, not an illustration, page-curl/folded-paper image, app icon, mockup, or rough cover graphic. The final `assets/logo.png` must preserve the exact offer name and pass typography, kerning, mark scale, and spacing checks. A bad mark with text composited beside it is still a failed logo.

After the final logo is accepted, freeze the brand lockup:

- `assets/logo.png` is the only downstream logo reference.
- No alternate logo files should exist in the production asset set.
- Do not ask imagegen to invent, redesign, recolor, redraw, reinterpret, replace, or substitute the logo in product mockups, ads, VSL visuals, PDF visuals, or page graphics.
- If a visual needs the logo, pass `assets/logo.png` to imagegen as the only logo reference and instruct imagegen to use the supplied logo exactly.

### Copy Studio Blueprint

Required before page-specific graphics, VSL visuals, ad angles, and checkout graphics. `copy-plan.json`, clean `copy.md`, `copy-blueprint.md`, and `sales-page-blueprint.json` define the sales-page sections, objections, proof jobs, CTAs, visual blocks, `copyAnchor` values, and suggested `visualKind` values.

### Product Bundle

Required before dashboard, product mockups, VSL product reveal, offer stack graphics, and ads that show the deliverable.

The product bundle should show the buyer what they get. If it is a coded diagram, call it a diagram. If it is a generated bitmap mockup, save the prompt/provenance in the manifest.

In deep generated-design runs, the actual product-bundle or offer-stack visual used on the sales page must be generated as an `imagegen-final` asset. If the logo, text, product stack, or composition is wrong, regenerate or edit with imagegen. Do not repair it locally with PIL/canvas/HTML/CSS/script overlays. A CSS/canvas/generated-by-code block can be used as a temporary wireframe or diagram only; it must be registered as `needs_revision` and cannot satisfy `data-offeros-product-bundle` or primary product mockup requirements. Do not create a Pillow-authored product bundle at all.

## Fast Path

If speed matters, still preserve:

1. offer direction
2. lightweight design guide
3. primary `assets/logo.png`/`.webp` imagegen-based logo lockup with readable offer name
4. page/product graphics
5. ads/VSL/dashboard variants

Do not skip the design guide entirely.
