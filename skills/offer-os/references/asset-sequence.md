# Asset Sequence

Generate assets in dependency order. Earlier assets define constraints for later ones.

## Core Sequence

1. Offer/page direction
2. Design guide
3. Logo or wordmark
4. Product outline and offer stack
5. `visual-asset-plan.md`
6. Sales page structure
7. Sales page graphics
8. Product bundle
9. PDF product visuals
10. VSL frames
11. Ads and social creative
12. Delivery dashboard
13. Secondary exports and variants

## Provenance Requirements

Record provenance for every visual artifact in `offer-os.json`.

- Use `imagegen` for bitmap hero, product, and ad imagery when the user asks for generated images, a generated design direction, or ad images.
- Use `code-vector` for hand-coded SVG diagrams only when a vector diagram is the right artifact.
- Use `html-css`, `pil-generated`, or `screenshot` only when that is the honest source.
- Do not describe SVGs, PIL text cards, CSS panels, or screenshots as "generated images." They can be useful fallbacks, but they must be labeled as such.

Deep mode should include at least:

- one brand/logo asset with clear production status
- one hero or product image that sells the offer visually
- three ad images with actual creative direction
- 6+ PDF-specific visuals/treatments, with 4+ not reused from the sales page
- 12+ VSL visual assets/treatments, with 8+ not reused from the sales page
- deck or VSL preview imagery

## Visual Asset Plan

Create `visual-asset-plan.md` before building sales-page graphics, the PDF product, ad images, the VSL deck, or the delivery dashboard.

The plan must split visuals into:

- global brand assets
- sales page visuals
- PDF product visuals
- VSL deck visuals
- ad visuals
- dashboard visuals
- reuse rules

Do not treat sales-page graphics as the default image library for every artifact. Each artifact has its own job:

- Sales page visuals sell belief and the offer stack.
- PDF visuals help the buyer use the product: covers, module dividers, matrices, completed examples, blank worksheets, checklists, and implementation maps.
- VSL visuals help a spoken pitch hold attention: pattern interrupts, problem maps, comparison tables, mechanism diagrams, product reveal, stack, value, guarantee, objection, and CTA visuals.
- Ad visuals interrupt the feed and should be generated specifically for the ad angle.

Minimum deep-mode budgets:

- sales page: 4+ visual slots
- PDF product: 6+ visuals/treatments, with 4+ PDF-specific
- VSL deck: 12+ visuals/treatments, with 8+ VSL-specific
- ads: 3+ ad-specific imagegen creatives

Register `visual-asset-plan` and set `quality.images.hasArtifactSpecificPlan = true`. Record whether each visual is shared or artifact-specific.

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

In deep generated-design runs, the primary logo artifact should be an `imagegen` or `imagegen-composite` `.png` or `.webp` logo lockup that includes the readable offer name. The imagegen brand mark alone can be saved as `assets/logo-mark.png`, but it is not the primary logo. A code-vector SVG can be registered only as a secondary export or draft unless the user explicitly requested vector-only delivery. If imagegen was blocked, record the blocker in `quality.logo.imagegenNotUsedReason` and keep the logo/run out of complete status.

### Sales Page Structure

Required before page-specific graphics, VSL visuals, ad angles, and checkout graphics.

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
