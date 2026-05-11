# Changelog

## 0.16.1

- Makes exact-copy sales pages skip support images unless the asset is registered with compliant buyer-facing image provenance.
- Prevents old local/code-made page panels from slipping into regenerated pages merely because a fallback filename exists.
- Keeps the stricter preflight refusal for hero thumbnails, product bundles, and rendered support visuals.

## 0.16.0

- Makes `copy.md` the exact sales-page copy source with bracketed section blocks such as `[hero]...[/hero]`.
- Makes `build_sales_page.py` render bracketed `copy.md` sections directly and convert markers to HTML comments.
- Prevents Page Kit partials from overriding exact Copy Studio sections in deep Copy Studio runs.
- Removes hidden copy injection from `build_copy.py`; required product, FAQ, feature-benefit, and offer-stack copy must be written in `sectionPlan[].copyBlocks` before page generation.
- Extends self-tests with a focused exact-copy page build so the HTML must contain exact-copy contract markers and the full Copy Studio spine.

## 0.15.2

- Removes ambiguous sales-page visual planning language: generated-design buyer-facing page images are explicit `imagegen` tasks.
- Adds `requiredTool: imagegen`, `requiredAction: call-imagegen-skill-tool`, `imagegenRequired: true`, and `fallbackAllowed: false` to generated visual plan rows.
- Makes each generated visual prompt start with `CALL THE imagegen SKILL/TOOL FOR THIS EXACT ROW` and the required save path.
- Extends validation and self-tests so visual plans fail when buyer-facing sales-page rows do not directly require imagegen.

## 0.15.1

- Closes the sales-page support-image loophole: every buyer-facing image rendered into `data-offeros-page-visual`, `data-offeros-video-thumbnail`, or `data-offeros-product-bundle` must be imagegen-final/provided/licensed.
- Makes `build_sales_page.py` refuse local/code-made page visuals that exist on disk but are not registered with final imagegen provenance and no local creative overlay.
- Extends visual planning so sales-page mechanism diagrams, comparison visuals, proof/demo visuals, structured panels, product reveals, offer stacks, and hero thumbnails are all imagegen-final jobs by default.
- Adds regression coverage for code-rendered sales-page support images.

## 0.15.0

- Hardens Copy Studio so `copy-plan.json.sectionPlan[].copyBlocks` must contain finished buyer-facing long-form sales copy, not scaffold notes.
- Adds `copywriter-quality-bar.md` and `copy-critic-rubric.md` so Copy Studio must write and critique a standalone Modern Brunson-style sales letter before visuals or page generation.
- Tightens `build_copy.py` to fail thin/missing/meta/repetitive copy blocks, enforce 2,500+ rendered copy words, render clean `copy.md`, and record copy critic metadata.
- Extends validation for long-form copy depth, repeated boilerplate, forbidden internal/meta phrases, VSL dependence, FAQ depth, product reveal depth, and Copy Studio provenance.
- Adds self-test coverage with a focused HYROX Copy Studio build fixture that renders a 4,000+ word sales letter before page/image generation.

## 0.14.1

- Splits Copy Studio rendering so `copy.md` is the clean written long-form sales copy shown in delivery dashboards.
- Moves the internal section blueprint, framework metadata, and copy map into `copy-blueprint.md`.
- Updates visual planning, validation, self-tests, and instructions so downstream assets depend on `copy-plan.json`, `copy-blueprint.md`, `sales-page-blueprint.json`, and clean `copy.md` without polluting the sales-copy deliverable.

## 0.14.0

- Adds Copy Studio as the mandatory deep-mode source of truth: `copy-plan.json` uses the `modern-brunson-long-form-v1` framework and renders `copy.md`, `copy-blueprint.md`, and `sales-page-blueprint.json`.
- Makes the written page argument standalone: VSL is optional support, while the copy plan must include hook, story/insight, new insight, unique mechanism, proof/demo, product reveal, feature-benefit breakdown, offer stack, guarantee, objections, and close.
- Requires structured product reveal fields with feature, benefit, reason-it-matters, buyer problem solved, proof/preview, and plain-bullet copy for every core component.
- Updates visual planning and sales-page generation to read Copy Studio output first, record Copy Studio metadata, and keep visual planning after the copy/content blueprint.
- Extends validation and self-tests for missing copy plans, no new insight, no unique mechanism, weak product reveal, proof after offer, generic objections, fake urgency, unmapped sales-page sections, and visual plans created without Copy Studio.

## 0.13.4

- Adds the Page Kit sparse eyebrow/pill policy: key signposts only, not one badge on every section.
- Centers section eyebrows with the H2 they precede and records `eyebrowPolicy`, `eyebrowAlignment`, and eyebrow counts in sales-page quality metadata.
- Updates validation and self-tests so overused/floating section pills fail instead of becoming the default page style.

## 0.13.3

- Adds Lucide icon markers as the Page Kit default for card grids, proof blocks, and checklist stacks.
- Makes sales-page image planning slot-aware with varied aspect ratios, `aspectRatioReason`, `displayIntent`, and `maxDisplayHeight`.
- Changes support-image framing so generated visuals render in content-hugging transparent frames with the border/shadow on the image itself, avoiding mismatched colored mattes.
- Extends validation and self-tests for Lucide metadata, slot-aware image metadata, and varied sales-page aspect ratios.

## 0.13.2

- Hardens the Page Kit against long-form sales-page UI drift: no sticky/hover section nav, no post-hero "Watch this first" label when the hero already contains the main VSL, and quieter eyebrow/prehead treatment.
- Adds branded icon/checkmark treatments to builder card grids and offer-stack checklists.
- Constrains sales-page support/product/bundle image display and records `data-offeros-image-display="constrained"` plus `quality.salesPage.imageDisplay`.
- Extends validation and self-tests for no-section-nav policy, branded icon metadata, constrained image display, and duplicate VSL instruction wording.

## 0.13.1

- Reverts the failed `0.13.0` Sales Page Studio rewrite, restoring the previous Page Kit behavior.
- Closes the `imagegen-composite` loophole for primary conversion visuals.
- Requires primary sales-page/ad conversion assets to be `imagegen-final` with `finalPixelsGeneratedBy: imagegen`, `localCreativeOverlay: false`, and non-creative-only local post-processing.
- Updates visual planning, schemas, validator checks, register-artifact metadata, and regression fixtures so local PIL/canvas/HTML/CSS/script composition cannot pass as finished generated creative.

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
