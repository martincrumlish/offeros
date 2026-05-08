# Changelog

## 0.13.0

- Adds the real Sales Page Studio renderer in `build_sales_page_studio.py`, with `build_sales_page.py` kept as a compatibility wrapper.
- Ports the useful AC Landing Agent structure into controlled OfferOS components: stacked VSL hero, top bar, what-this-is block, comparison table, proof/demo, mechanism steps, compact and expanded offer stacks, guarantee, sales letter, fit section, pricing, FAQ accordion, final CTA, 3D buttons, and responsive self-contained CSS.
- Extends `sales-page-blueprint.schema.json` with a real content contract for section copy, blocks, offer metadata, visual slots, and page assets.
- Hardens validation so deep sales pages must declare `data-offeros-sales-page-studio="sales-page-studio-v2"`, use the AC-inspired component library, include 3D CTAs, include the FAQ accordion, and record component integrity metadata.

## 0.12.0

- Replaces generated `scripts/build_offer_system.*` production control with plugin-owned OfferOS Studio builders and a public `scripts/offeros.py` dispatcher.
- Adds canonical studio source contracts and builders for visual planning, launch emails, Gotenberg/Chromium PDF workbooks, and editable VSL PPTX decks.
- Adds schemas for `visual-asset-plan.json`, `email-sequence.json`, workbook blueprint/content files, and `presentation/vsl-deck-plan.json`.
- Extends validation so deep runs fail on generated build controllers, missing studio source files, weak sales-page visual usage, missing email quality metadata, missing Gotenberg/PDF render evidence, and VSL decks without source/editability metadata.
- Updates initialization folders and self-tests for the production-studio architecture.

## 0.11.0

- Adds the OfferOS Page Kit sales-page framework: intake gate, sales-page blueprint schema, theme schema, archetypes, themes, partials, CSS, JS, and a static HTML builder.
- Makes deep-mode sales pages builder-generated instead of handwritten: `scripts/build_sales_page.py` must produce `index.html` with Page Kit metadata, stacked main-column VSL placement, and approved section markers.
- Limits Page Kit source options to the agreed release archetypes and theme presets, and makes the builder reject unapproved legacy/experimental values.
- Changes the default sales-page purchase handoff to `#checkout` and forbids embedded checkout/order/payment forms in generated sales pages.
- Extends validation and self-test coverage for non-builder pages, two-column hero drift, missing Page Kit metadata, missing blueprint/theme artifacts, and on-page checkout/order-form drift.

## 0.10.5

- Changes the logo workflow to single-final-logo mode: one imagegen logo lockup at `assets/logo.png`, not three options or alternate lockups.
- Requires downstream imagegen jobs that need branding to use `assets/logo.png` as the exact supplied logo reference.
- Replaces multi-logo metadata with `finalLogoCount`, `logoGenerationCount`, `singleFinalLogoOnly`, and `alternateLogosCreated`.
- Removes the default imagegen-composite logo fallback from generated-design runs.

## 0.10.4

- Removes `pil-generated` as an allowed registered artifact provenance.
- Clarifies that Pillow/PIL is only for inspection, cropping, resizing, or compositing already-sourced assets, never for authoring OfferOS customer-facing images.
- Adds sales-page source checks so product bundle and hero/VSL thumbnail images must be registered with imagegen/imagegen-composite/provided/licensed provenance.

## 0.10.3

- Closes the code-rendered PNG loophole for primary conversion visuals.
- Requires generated-design deep runs to use `imagegen` or `imagegen-composite` for product bundles, offer-stack bundles, product mockups, hero/VSL thumbnails, buyer-situation photos, and ad creatives unless the asset is provided or licensed.
- Keeps PIL/HTML/CSS/canvas/generated-by-code PNGs limited to diagrams, worksheets, previews, real screenshots, and QA evidence.
- Adds validator and self-test coverage for a Pillow-generated `product-bundle.png` being incorrectly treated as a finished creative asset.

## 0.10.2

- Adds a brand-lock step after final logo creation so `assets/logo.png` is the only downstream logo reference.
- Forbids downstream imagegen prompts from generating, redrawing, reinterpreting, or placing new logos/wordmarks in product, ad, PDF, VSL, dashboard, or page images.
- Excludes rejected logo attempts from visual worker context and visual asset plans.
- Adds validator and self-test coverage for logo drift in downstream asset plans.

## 0.10.1

- Makes SVG a hard failure for generated OfferOS visual assets, including logos, brand assets, ad images, page art, PDF art, VSL art, and diagram fallbacks.
- Removes secondary/vector SVG export allowances from the logo workflow.
- Adds validator and self-test coverage for registered `.svg` artifacts in deep OfferOS runs.
- Updates provenance guidance to use PNG/WebP/JPG bitmaps, HTML/CSS blocks, or rendered PNG diagrams instead of SVG files.

## 0.10.0

- Adds a canonical `direct-response-long-form-v1` framework for paid front-end sales pages: message match, hook/VSL, problem, agitation, failed alternatives, mechanism, proof/demo, before/after, product, offer stack, guarantee, objections, and close.
- Requires `copy.md` to include a structured `# Section Blueprint` before visual planning or page build.
- Rebuilds the sales-page skeleton from comment placeholders into a real scaffold with VSL, problem, agitation, failed alternatives table, mechanism steps, proof/demo, before/after, product reveal, offer stack, pricing, guarantee, FAQ, and final CTA blocks.
- Moves proof/demo before the main offer stack and validates the required persuasion order.
- Adds validator and self-test coverage for fake product pages with markers, missing section blueprint, proof-after-price drift, thin required sections, missing failed-alternatives/mechanism/proof blocks, and weak post-hero CTA rhythm.

## 0.9.0

- Changes the direct-response hero contract to a stacked VSL-first layout with centered copy, large centered video, price/CTA below the video, and trust row below.
- Rejects two-column, split-screen, and SaaS-style heroes for `direct-response-long-form-vsl` pages.
- Adds validator and self-test checks for `stacked-vsl-hero-v1`, hero layout metadata, hero video prominence, and common two-column hero signals.

## 0.8.0

- Moves visual planning to a post-copy-blueprint stage so sales-page visuals are anchored to real direct-response sections instead of pre-copy mood-board prompts.
- Adds the `mixed-direct-response-v1` sales-page image system with explicit `visualKind`, `copyAnchor`, conversion job, aspect ratio, and text-rule fields.
- Hardens validation and self-tests against pre-copy visual plans, missing copy anchors, missing image taxonomy, and all-mockup sales-page visual plans.

## 0.7.0

- Hardens the logo recipe so imagegen must generate complete logo lockups with symbol plus exact wordmark before any mark-only fallback is allowed.
- Requires final `assets/logo.png` to be a professional horizontal lockup with exact offer-name preservation, typography, kerning, mark scale, spacing, and nav/cover preview checks.
- Adds validator checks so `logo-mark` files, rough text composites, and missing professional lockup metadata cannot pass as the primary logo.

## 0.6.0

- Adds explicit imagegen visual worker dispatch after offer architecture, design, logo, product outline, and `visual-asset-plan.md` exist.
- Defines bounded worker ownership for page visuals, PDF visuals, VSL visuals, and ad creatives with shared style references and disjoint output folders.
- Updates visual planning metadata to record whether visual agent dispatch was used or why it was skipped.

## 0.5.0

- Adds a required `visual-asset-plan.md` artifact before sales-page graphics, PDF, ads, VSL, and dashboard production.
- Splits visual budgets by artifact so PDF products and VSL decks need their own supporting visuals/treatments instead of reusing only sales-page imagery.
- Requires deep runs to plan 6+ PDF visuals/treatments with 4+ PDF-specific, 12+ VSL visuals/treatments with 8+ VSL-specific, and 3+ ad-specific imagegen creatives.
- Adds manifest metadata and validator checks for artifact-specific visual plans, PDF-specific visuals, VSL-specific visuals, and sales-page-reuse-only failures.

## 0.4.0

- Replaces loose logo wording with a hard logo-lockup recipe: imagegen brand mark plus readable offer-name bitmap, no icon-only primary logo.
- Tightens direct-response sales-page generation with a required agitation section, VSL word cap, paragraph limits, composition metadata, and blank-card/table prevention.
- Raises the $27 PDF product bar with named tools/templates, page archetype diversity, completed example counts, and repeated "Action Surface" rejection.
- Adds VSL visual-reuse controls: 12+ unique visual assets/treatments and no large non-logo bitmap repeated on more than 25% of slides.
- Extends validation and self-tests to catch the FunnelPlanner-style failures at source and QA.

## 0.3.0

- Hardens generated-design runs so the primary logo must be an imagegen bitmap, not a generated SVG fallback.
- Requires deep OfferOS runs to use generator-first builds and treat validator warnings as failures.
- Adds stricter PDF product, launch email, dashboard, VSL deck, and QA metadata checks.
- Requires VSL decks to be editable PPTX artifacts, not HTML contact sheets.
- Adds PPTX image aspect-ratio validation so deck images cannot be stretched into arbitrary boxes.
- Adds the direct-response hero and buy-box offer-stack contracts for long-form sales pages.

## 0.2.0

- Initial distributable plugin shape with OfferOS skill, templates, references, dashboard generator, artifact registry, and output validator.
