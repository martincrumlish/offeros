# Quality Gates

OfferOS operates in default `deep` mode. A complete run must produce a commercial offer system, not a scaffold, outline, or placeholder bundle.

Deep mode means every artifact must be specific to the offer, audience, mechanism, objections, delivery model, and conversion path. Generic copy, decorative design, fake strategy, stock UX, or half-built assets fail the gate.

## System Gate

A completed OfferOS output must include:

- offer architecture
- `design.md`
- logo and image assets
- long-form sales copy
- coded sales page
- customer-ready PDF product
- Facebook ads and ad images
- launch email sequence
- VSL deck
- delivery dashboard
- QA report

All artifacts must share one coherent positioning strategy, promise, mechanism, terminology, visual identity, and conversion logic.

Technical completion is not commercial completion. Passing link checks, file existence checks, and overflow checks is necessary but not enough. A deep run must also pass a commercial value audit before the manifest status can become `complete`.

## Offer Architecture Gate

Must define:

- target customer, pain state, desired state, and buying context
- conscious desire and hidden desire
- core promise and measurable outcome
- unique mechanism or strategic angle
- failed alternatives
- offer stack, bonuses, pricing logic, guarantee, urgency, and risk reversal
- objection map with rebuttals
- proof strategy, even when source proof is limited
- funnel path from ad to sale to delivery

Fails if the offer is vague, commodity-like, internally inconsistent, or lacks a reason to buy now.

## Design Gate

`design.md` must define:

- brand personality and visual principles
- color palette with usage roles
- typography hierarchy
- layout and spacing rules
- image direction and asset style
- component patterns for page, PDF, ads, deck, and dashboard
- accessibility and responsive requirements

Fails if it reads like a mood board without implementation guidance.

## Image Provenance Gate

Every logo, product image, page graphic, ad image, deck visual, and dashboard preview must record provenance in `offer-os.json`.

Allowed provenance values:

- `imagegen`: created with the imagegen skill/tool from a prompt.
- `imagegen-composite`: final bitmap composed from an imagegen mark/frame plus deterministic rendered text or layout.
- `provided`: supplied by the user.
- `licensed`: externally sourced with permission/license.
- `screenshot`: captured from a real page, deck, PDF, or product artifact.
- `html-css`: browser-rendered HTML/CSS visual.
- `generated-by-code`: deterministic script output.

These values are not interchangeable. Deep mode requires real imagegen/imagegen-composite bitmap assets for primary conversion visuals when the user asks for generated design direction, generated images, ad images, or supporting images. Product bundles, offer-stack bundles, product mockups, hero/VSL thumbnails, buyer-situation photos, and ad creatives must be `imagegen` or `imagegen-composite` unless the user provided/licensed the asset. `html-css`, `generated-by-code`, `manual`, and `screenshot` can support diagrams, worksheets, rendered previews, QA evidence, or real artifact screenshots, but they do not count as AI image generation and cannot satisfy those primary creative slots. Pillow/PIL-authored image artifacts are not allowed in deep OfferOS runs; Pillow may only inspect, crop, resize, or composite already-sourced assets. SVG files are not allowed generated visual assets or fallbacks.

Fails if:

- an SVG file is created or registered as a generated visual artifact
- an image artifact is registered as `pil-generated`
- a PIL card, CSS block, or screenshot is described as a generated image
- a product bundle, offer-stack bundle, product mockup, hero/VSL thumbnail, buyer-situation photo, or ad creative is made as a PIL/HTML/CSS/canvas/screenshot/generated-by-code/manual PNG instead of imagegen/imagegen-composite
- the manifest omits provenance for image artifacts
- all visual assets are code-generated diagrams with no real bitmap hero/product/ad imagery
- ad images are mostly text blocks rather than persuasive creative
- the logo is a disposable placeholder and is not marked as draft/fallback

## Visual Asset Plan Gate

Deep generated-design runs must create `visual-asset-plan.md` v2 after `copy.md` contains the sales-page section blueprint and before artifact production. The plan must split visuals by artifact instead of treating sales-page imagery as the default pool.

Must include:

- `visualPlanStage: post-content-blueprint`
- `copyBlueprintUsed: true`
- `salesPageImageSystem: mixed-direct-response-v1`
- global brand assets
- 4+ sales-page visuals tied to real copy/page section anchors
- 6+ PDF visuals/treatments, with 4+ PDF-specific and not reused from the sales page
- 12+ VSL visuals/treatments, with 8+ VSL-specific and not reused from the sales page
- 3+ ad-specific imagegen creatives
- dashboard preview/thumbnail choices
- allowed `visualKind` values and required `copyAnchor`, `conversionJob`, `artifactTarget`, `aspectRatio`, and `textRule` fields for sales-page visuals
- explicit reuse rules
- visual worker dispatch plan when agents are authorized
- `quality.images.hasArtifactSpecificPlan = true`
- `quality.images.visualPlanStage = "post-content-blueprint"`
- `quality.images.copyBlueprintUsed = true`
- `quality.images.visualReusePolicy = "artifact-specific-v1"`
- `quality.images.salesPageImageSystem = "mixed-direct-response-v1"`

Fails if the plan was created before the copy blueprint, if sales-page visuals are not anchored to real page sections, if visual taxonomy fields are missing, if the PDF or VSL visuals are only sales-page images, if ads are just crops/text-card variants of page art, or if the plan does not specify artifact-specific visual jobs and file paths. Also fails if every sales-page visual is mockup/UI/product-bundle style unless the user explicitly requested a mockup-heavy aesthetic.

When the user explicitly allowed agents, the build should dispatch imagegen visual workers after logo/style references, `copy.md`, and post-content-blueprint `visual-asset-plan.md` exist. If it does not, record `quality.images.agentDispatchUsed = false` and a concrete `agentDispatchNotUsedReason`.

## Logo Gate

A deep-mode logo must be treated as an identity asset, not a quick decoration.

Must include:

- one final logo direction before final production
- primary final logo lockup as `.png` or `.webp` that includes the readable offer name and uses the `imagegen` skill/tool in deep generated-design runs
- brand lock metadata confirming `assets/logo.png` is the only downstream logo reference and `singleFinalLogoOnly` is true
- imagegen single-final-logo complete lockup, not a 3-option logo set, option sheet, alternate lockups, symbol-only fallback, or script-composited wordmark
- logo symbol that is simple, flat, one-color usable, and not an illustration, app icon, page-curl/folded-paper graphic, mockup, or rough cover image
- professional wordmark composition that preserves the exact offer name, does not insert accidental spaces, and has checked typography, kerning, mark scale, and spacing
- nav-size and cover-size lockup preview at `output/qa/logo-lockup-preview.png`
- no SVG/vector logo export; generated logo output is PNG/WebP bitmap only
- bitmap preview/export for dashboard and QA review
- small-size navigation check
- one-color legibility check
- `quality.logo` metadata

Fails if the primary logo is not an `imagegen` horizontal bitmap in a deep generated-design run unless the user supplied the logo or imagegen was blocked and the blocker is recorded. Also fails if any generated SVG logo/brand file exists, if more than one logo option is created, if the logo is icon-only, lacks the readable offer name, points at a mark-only file, uses an illustrative/page-curl/app-icon mark, breaks the exact offer name into the wrong spacing, or looks like default text pasted beside a mark.

Fails if downstream product, ad, page, PDF, VSL, or dashboard image prompts ask imagegen to invent, redesign, recolor, redraw, reinterpret, replace, or substitute the logo/wordmark. When a generated visual needs a logo, the imagegen job must receive `assets/logo.png` as the exact supplied logo reference.

## Copy Gate

Long-form sales copy must include:

- headline and lead
- problem agitation
- market diagnosis
- failed alternatives
- unique mechanism
- offer reveal
- stack and value build
- proof or proof substitute
- objection handling
- guarantee
- urgency/scarcity logic
- FAQ
- repeated CTA sections

Fails if it is short-form copy disguised as a sales page, uses generic claims, lacks objections, or cannot plausibly sell the offer.

## Page Gate

The coded sales page must:

- start from `assets/templates/sales-page/page-skeleton.html` unless the user supplied an existing page to modify
- declare a page type from `references/sales-page-types.md`
- implement the final sales copy
- use the resolved design system
- include the required direct-response section contract from `assets/templates/sales-page/section-map.md`
- mark each core section with `data-offeros-section`
- include VSL, problem, agitation, failed alternatives, mechanism, proof/demo before the buy box, before/after, product, offer stack, pricing, guarantee, FAQ, and final CTA areas
- work on mobile and desktop
- have no broken links, missing assets, overflow, unreadable text, or placeholder content
- use maintainable HTML/CSS/JS

For `direct-response-long-form-vsl`, the page must include full problem diagnosis, agitation, failed alternatives, unique mechanism, proof/demo before the buy box, before/after, product reveal, offer stack, pricing/value logic, guarantee, objections, and repeated CTAs. Offer-stack cards must have unique benefit copy.

For `direct-response-long-form-vsl`, the hero must follow the stacked VSL-first direct-response hero contract: centered buyer filter, prehead, H1, benefit lead, large centered video/VSL frame below the headline, price strip below the video, CTA to `#buy`, and trust row. The offer stack must follow the buy-box contract: `id="buy"`, bundle image, 8+ item deliverable checklist, normally/today value row, large CTA, and guarantee/instant-access reassurance.

For `direct-response-long-form-vsl`, the page must also follow the composition contract: the direct-response-long-form-v1 spine, proof/demo before offer stack, separate problem/agitation/failed-alternatives sections, VSL setup under 220 words, normal paragraphs under 55 words, no non-FAQ/non-stack section above 500 words, and no blank-looking tables/cards.

Fails if it is visually thin, nonresponsive, missing core sections, reads like a short product page, skips the internet-marketing/direct-response arc, asks for the sale before mechanism/proof, uses a nice branded hero instead of the required stacked VSL-first direct-response hero, uses a two-column/split SaaS hero with a small side video, turns the VSL area into a wall of text, replaces the buy-box checklist stack with generic cards/pricing panels, repeats generic card blurbs, has invisible/low-contrast text, or contains scaffold remnants.

## PDF Product Gate

The PDF must be a deliverable a buyer could consume.

Must include:

- cover
- quick start
- orientation
- modules/chapters
- worksheets/checklists/templates/examples
- implementation plan
- professional layout
- PDF-specific visuals/treatments from the visual asset plan

Deep-mode minimums:

- At least 22 pages for a paid product up to $29.
- At least 25 pages for a $30-$99 paid product.
- At least 35 pages for a $100+ paid product, unless the user explicitly asks for a shorter deliverable.
- Extracted PDF text meets the price-point target from the validator unless the user explicitly approved a highly visual workbook.
- At least 8 buyer-action surfaces across worksheets, templates, calculators, scripts, scorecards, cards, checklists, examples, or implementation plans.
- At least 8 named buyer tools/templates for paid products up to $29 and 10+ for $30-$99 products.
- At least 7 distinct page archetypes, with no single archetype above 35% of pages.
- At least two completed examples and two blank fill-in versions for core worksheets/templates.
- At least 6 PDF visuals/treatments, including 4+ not reused from the sales page.
- Rendered page previews or screenshots proving that pages are not clipped, blank, or unreadable.

Fails if it is an outline, ebook shell, generic advice document, thin article, short checklist, repeated "Action Surface" box pages, identical page layouts, or lacks practical buyer value.

## Ads Gate

Must include distinct strategic angles, full ad copy, and generated or specified creative.

Fails if ads repeat the same angle, use repeated boilerplate explanations across angle cards, overpromise, ignore platform constraints, do not connect to the sales page, or use low-effort text-card images while claiming generated ad creative.

## Email Gate

The sequence must have a persuasive arc from anticipation to close.

Every email must include send timing, subject line, preview text, campaign role, body copy, and CTA. The sequence must progress through distinct beliefs/objections rather than paste the same product paragraph into each email.

Fails if emails are interchangeable, generic, too short to persuade, missing send/preview/role metadata, repeating boilerplate body copy, or disconnected from the offer strategy.

## VSL Gate

The deck must support a spoken sales presentation:

- hook
- problem reframe
- stakes
- mechanism
- proof/credibility
- offer reveal
- stack
- objections
- guarantee
- close

Deep-mode VSL requirements:

- `vsl-deck` must be an editable PowerPoint file (`.pptx`) unless the user explicitly asked for a non-PowerPoint format.
- the build path should use a PowerPoint-capable generator before any browser preview is made
- HTML is allowed only as `vsl-preview`, `vsl-contact-sheet`, or a browser-safe deck preview.
- 20-30 slides unless the offer format clearly requires otherwise.
- The PPTX and any preview must use distinct structural slide layouts; HTML presenter output is preview only.
- At least 8 visual treatments and no single layout family above 35% of slides.
- Real visuals, diagrams, screenshots, generated frames, or product previews on key slides.
- At least 12 unique visual assets or distinct diagram treatments.
- At least 8 VSL-specific visual assets or treatments not reused from the sales page.
- No single large non-logo bitmap repeated on more than 25% of slides.
- PPTX bitmap images preserve aspect ratio using contain/cover/crop sizing. Images must not be stretched into arbitrary boxes.
- Speaker notes or narration guidance.
- Speaker notes must be usable narration guidance, not private labels.
- Internal stage labels such as "Agitate", "Problem", "Proof", "Offer", "CTA", "Objection", "Stage: Problem", and "Problem:" must not appear anywhere in visible slide copy.
- Offer reveal, stack, value build, price, guarantee, objections, and final CTA.
- Browser-safe contact sheet or preview for dashboard use.
- `vsl-deck.preview` must point to browser-safe HTML/image, not the `.pptx`.
- Browser QA must include the VSL preview at desktop and mobile widths with no overflow or broken images.

Fails if it is only HTML registered as the primary VSL deck, only a summary deck, a contact sheet, a grid of cards, repeated one-layout slides, repeats the same few images as filler, placeholder-heavy, exposes production labels on slides, stretches/compresses bitmap images, or cannot guide a convincing VSL recording.

## Dashboard Gate

The delivery dashboard must be a branded browser hub with previews and direct access to assets.

Use the standard OfferOS dashboard structure generated by `scripts/generate_delivery_dashboard.py` unless the user explicitly requests a different dashboard. Theme it with colors, logo, and imagery from `design.md`; do not reinvent the interaction model.

Required structure:

- modal preview system
- iframe previews for HTML/PDF/text assets
- image preview modal for images
- direct open action
- `data-path` and `data-preview` artifact cards
- `data-offeros-dashboard="v2-modal"` marker

Fails if it is a static link grid, lacks modal/iframe preview behavior, lacks `data-preview` cards, or does not help the user present/use the offer system.

## Commercial Value Audit Gate

Before final response, score each major artifact from 1-5 for:

- buyer value: would the buyer reasonably pay for this?
- usability: can the buyer use it without extra explanation?
- trust: does it increase confidence in the offer?

Major artifacts are sales page, PDF product, ad creative, emails, VSL deck, and delivery dashboard. Scores below 4 require revision or a clearly stated limitation. Record the audit in `offer-os.json` under `commercialAudit` and summarize it in `qa-notes.md`.

## Critique Loop

For every major artifact:

1. Draft.
2. Critique against this file and the offer strategy.
3. Identify concrete weaknesses.
4. Revise.
5. Recheck failure conditions.

Do not mark an artifact complete until the critique finds no blocking issues.

## Forced Revision Conditions

Revision is mandatory when any appear:

- placeholder text, missing sections, fake links, or scaffold remnants
- generic positioning
- inconsistent promise, mechanism, audience, pricing, or visual identity
- claims without explanation, proof, caveat, or believable support
- weak or absent CTA
- missing objection handling
- illegible or nonresponsive design
- broken layout, missing assets, or unreadable mobile state
- PDF lacks actionable buyer value
- PDF is below the minimum page/action-surface depth for the price
- PDF extracted text is below the price-point target
- PDF repeats the same page layout or visible "Action Surface" box instead of named tools/templates
- PDF lacks PDF-specific visuals/treatments and only reuses sales-page imagery
- ads are repetitive, noncompliant, or visually unclear
- ad angle cards repeat boilerplate instead of unique strategy
- visual assets claim image generation but were actually PIL/CSS placeholders
- any generated SVG visual artifact is created or registered
- logo is a generic icon-only mark, illustrative/page-curl mark, or rough text composite marked complete without professional lockup QA
- emails lack sequence logic, send timing, preview text, campaign role, or repeat boilerplate body copy
- VSL deck lacks a persuasive sales arc, repeats one layout, exposes stage labels, or is only a contact sheet
- VSL primary deck is HTML instead of PPTX
- VSL deck recycles the same few large images across many slides
- VSL deck relies only on sales-page imagery instead of VSL-specific visuals/treatments
- VSL PPTX images are stretched or compressed instead of aspect-preserved with contain/cover/crop sizing
- VSL preview overflows on mobile or the dashboard tries to iframe the PPTX
- dashboard does not use the standard modal/iframe template
- QA notes contradict measured artifact metadata
- sales page skips the required direct-response section contract
- sales page does not declare a page type or uses a short product-page shape for a direct-response offer
- QA only checks technical existence and fails to name specific commercial defects
