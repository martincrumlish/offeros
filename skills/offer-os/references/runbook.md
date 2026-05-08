# OfferOS Runbook

Use this runbook for complete offer builds. Default to `deep` mode.

## 1. Intake

Collect or infer:

- offer idea
- audience
- problem or desired result
- price point
- delivery format
- proof or credibility
- design source
- tone/brand constraints
- compliance constraints

Record assumptions in `offer-os.json` and `offer-architecture.md`.

Ask a follow-up only when a missing answer would materially change the product, claims, legal/compliance posture, or brand ownership.

## 2. Initialize The Project

Create the manifest and folders:

```powershell
.\.venv\Scripts\python.exe plugins\offer-os\skills\offer-os\scripts\init_offer_project.py --name "Offer Name" --audience "buyer segment" --problem "problem/result" --price "27" --mode deep --design-source-type generated --force
```

If `.venv` does not exist, use any available Python. If the user supplied an existing design file, URL, or screenshots, replace `generated` with the exact source type. Do not leave deep runs at `unresolved`.

Before creating artifacts in deep mode, load `references/exact-build-recipes.md` and follow the Build Controller Recipe. Keep a reproducible build script in the output project. If QA finds a defect, fix the build script and regenerate clean output instead of hand-patching final files.

## 3. Offer Architecture

Create `offer-architecture.md`. Include:

- market diagnosis
- buyer profile
- desire stack
- failed alternatives
- unique mechanism
- offer stack
- bonuses
- guarantee
- pricing logic
- objections and rebuttals
- proof strategy
- conversion path

Run the offer architecture quality gate before moving on.

Register:

```powershell
.\.venv\Scripts\python.exe plugins\offer-os\skills\offer-os\scripts\register_artifact.py --id offer-architecture --title "Offer Architecture" --type document --category Strategy --path offer-architecture.md
```

## 4. Design Resolver

Resolve design from:

- existing `design.md`
- URL reference
- screenshots
- generated archetype
- hybrid instructions

Create or update `design.md` before visual production. The guide must include concrete production rules.

Register `design-guide`.

## 5. Brand And Logo

Follow the Logo Recipe in `references/exact-build-recipes.md`.

Required result:

- `assets/logo.png`
- `brand.logo = "assets/logo.png"`
- primary logo is a complete lockup with readable offer name, not an icon-only mark
- imagegen was used for exactly one final complete logo lockup with symbol plus exact offer-name wordmark
- no 3-option logo set, option sheet, alternate lockups, symbol-only fallback, or script-composited wordmark was created
- wordmark preserves the exact offer name and has checked typography, kerning, mark scale, and spacing
- `output/qa/logo-lockup-preview.png` shows nav-size and cover-size logo previews
- `logo` artifact registered with `provenance: "imagegen"`
- `quality.logo.brandMarkSource = "imagegen"`
- `quality.logo.logoMode = "single-final-logo-v1"`
- `quality.logo.logoDirectionCount = 1`
- `quality.logo.finalLogoCount = 1`
- `quality.logo.logoGenerationCount = 1`
- `quality.logo.singleFinalLogoOnly = true`
- `quality.logo.alternateLogosCreated = false`
- `quality.logo.logoLockup = true`
- `quality.logo.includesReadableOfferName = true`
- `quality.logo.imagegenCompleteLogoLockupAttempted = true`
- `quality.logo.exactOfferNamePreserved = true`
- `quality.logo.professionalLockupApproved = true`
- `quality.logo.finalLogoLocked = true`
- `quality.logo.downstreamLogoReference = "assets/logo.png"`
- `quality.logo.downstreamImagegenLogoReference = "assets/logo.png"`
- `quality.logo.downstreamImagegenMustUseLogoReference = true`

Do not create or register any SVG logo file. Do not create an icon-only mark, illustrative mark, rough text composite, PIL/HTML/CSS raster fallback, or text-only graphic and call it complete.

After logo approval, freeze the brand lockup. Downstream imagegen work must use `assets/logo.png` as the exact supplied logo reference whenever the visual needs a logo. It must not invent, redesign, recolor, redraw, reinterpret, replace, or substitute the logo, and it must not use old logo attempts or alternate logo files.

Update `offer-os.json`:

- `brand.logo`
- primary/accent colors
- fonts if known

Register `logo`.

## 6. Product And Offer Stack

Outline the PDF product before writing page graphics or VSL. Define:

- product modules
- worksheets/templates/checklists
- examples
- product completion outcome
- final CTA or next step

## 7. Sales Copy

Follow the Sales Page Recipe in `references/exact-build-recipes.md` before writing `index.html` or creating sales-page graphics.

Required result:

- `copy.md` with the required headings from the recipe
- section-by-section sales-page blueprint with conversion job, visual block, suggested `visualKind`, `copyAnchor`, proof/objection handled, and CTA role
- direct-response-long-form-v1 spine: message match, hook/VSL, problem, agitation, failed alternatives, mechanism, proof/demo, before/after, product, offer stack, guarantee, objections, close
- `quality.salesPage.pageType = "direct-response-long-form-vsl"` unless the user explicitly requested another page type
- full copy, not an outline

Register `sales-copy`.

## 8. Visual Asset Plan

Follow the Visual Asset Plan Recipe in `references/exact-build-recipes.md` after `copy.md` has the section blueprint and before creating sales-page graphics, PDF pages, ads, VSL slides, or dashboard previews.

Required result:

- `visual-asset-plan.md` v2
- `visualPlanStage: post-content-blueprint`
- `copyBlueprintUsed: true`
- `salesPageImageSystem: mixed-direct-response-v1`
- sales-page visuals with `visualKind`, `copyAnchor`, `conversionJob`, `artifactTarget`, `aspectRatio`, and `textRule`
- separate visual inventories for sales page, PDF product, VSL deck, ads, and dashboard
- 6+ PDF visuals/treatments, with 4+ not reused from the sales page
- 12+ VSL visuals/treatments, with 8+ not reused from the sales page
- 3+ ad-specific imagegen creatives
- agent dispatch plan for visual workers when the user allowed agents
- `quality.images.hasArtifactSpecificPlan = true`
- `quality.images.visualPlanStage = "post-content-blueprint"`
- `quality.images.copyBlueprintUsed = true`
- `quality.images.visualReusePolicy = "artifact-specific-v1"`
- `quality.images.salesPageImageSystem = "mixed-direct-response-v1"`

Register `visual-asset-plan`.

If the user has allowed agents, load `references/agent-dispatch.md` and dispatch imagegen visual workers immediately after registering the post-copy plan. Use separate workers for sales-page visuals, PDF visuals, VSL visuals, and ad images. Keep integration and QA in the main agent.

## 9. Sales Page

Follow the Sales Page Recipe in `references/exact-build-recipes.md`.

Required result:

- `sales-page-blueprint.json` and `theme.json` created before HTML
- `index.html` generated by `scripts/build_sales_page.py`, not handwritten
- every required `data-offeros-section` marker retained
- separate `problem`, `agitation`, and `failed-alternatives` sections retained
- proof/demo appears before the main offer stack
- stacked VSL-first hero contract retained: centered copy stack, large centered video frame below the headline, price strip below the video, CTA to `#checkout`, trust row
- offer-stack buy-box contract retained: `id="checkout"` or `data-offeros-buy-section`, bundle image, 8+ item checklist, value row, large CTA, guarantee/access reassurance
- no embedded checkout, order form, payment fields, or credit-card form
- at least 2,500 visible words for `direct-response-long-form-vsl`
- VSL setup section under 220 visible words
- normal paragraphs under 55 words
- at least 7 FAQ objections
- at least 4 CTA placements
- at least 3 post-hero CTA placements
- unique buyer-facing copy for each offer-stack card

Verify:

- desktop rendering
- mobile rendering
- image loading
- no horizontal overflow
- CTA links

Register `sales-page`.

## 10. Supporting Graphics

Generate assets in sequence:

1. logo
2. visual asset plan
3. product bundle
4. hero/VSL thumbnail
5. mechanism/framework visual
6. before/after visual
7. PDF-specific cover/product/tool visuals
8. VSL-specific slide visuals/treatments
9. ad-specific imagegen creatives
10. deck/dashboard preview graphics

Register each useful image.

Record provenance for every visual artifact. If an asset is HTML/CSS, generated-by-code, or a screenshot, label it honestly. If the run asks for generated images, use imagegen for hero/product/ad bitmaps unless blocked and record the blocker in `quality.images.imagegenNotUsedReason`. Do not create or register SVG visual files. Do not create or register Pillow/PIL-authored image artifacts. Do not use only sales-page visuals for the PDF or VSL.

Do not let a code-rendered PNG or local composite satisfy a primary creative slot. In deep generated-design runs, product bundles, offer-stack bundles, product mockups, hero/VSL thumbnails, buyer-situation photos, and ad creatives must be `imagegen-final` unless supplied/licensed. HTML/CSS, canvas, screenshots, generated-by-code, or manual outputs are acceptable only for diagrams, worksheets, matrices, previews, real artifact screenshots, and QA evidence. Pillow may inspect, crop, resize, compress, or format-convert existing sourced images, but it must not add logo, headline text, labels, UI cards, badges, mockups, overlays, or product-stack composition after imagegen. If the creative is wrong, regenerate or edit with imagegen.

## 11. PDF Product

Follow the PDF Product Recipe in `references/exact-build-recipes.md`. Create a buyer-ready PDF under `output/pdf/`. Include an editable source file when useful.

Apply the depth target from `references/pdf-product.md`: page count, extracted word count, action surfaces, named tools/templates, page archetype variety, completed examples, blank templates, and rendered page QA. Do not call a short outline, repeated "Action Surface" page set, or thin workbook complete.

Use the PDF skill for generation/render checks when needed.

Register `pdf-product-source` and `pdf-product`.

## 12. Facebook Ads

Create `facebook-ads.html` or `facebook-ads.md` with:

- market diagnosis
- 15 angles
- 30 hooks
- 10 creative concepts
- 10 complete ads
- best 3 to test first
- generated ad images

Register ad copy and each ad image.

## 13. Launch Emails

Follow the Email Sequence Recipe in `references/exact-build-recipes.md`. Create `emails.html` with a copy-ready sequence. Deep mode should prefer at least 7 emails unless the launch clearly needs fewer.

Every email needs send timing, subject line, preview text, campaign role, body copy, and CTA. Repeated product boilerplate across emails is a blocker.

Register `email-sequence`.

## 14. VSL Deck

Follow the VSL Deck Recipe in `references/exact-build-recipes.md`.

Required result:

- primary deck saved as `output/presentation/[slug]-vsl.pptx`
- 20-30 slides
- 8+ layout names planned before generation
- no layout above 35% usage
- no visible internal stage labels
- 12+ unique visual assets/treatments
- 8+ VSL-specific visuals/treatments not reused from the sales page
- no non-logo bitmap repeated on more than 25% of slides
- speaker notes of at least 25 words per slide
- HTML/contact-sheet only after the PPTX exists and only registered as `vsl-preview`
- `vsl-deck.preview` points to browser-safe HTML/image, not the `.pptx`
- VSL preview is browser-tested at desktop and mobile widths with no overflow or broken images

Register `vsl-deck` and `vsl-preview`.

## 15. Delivery Dashboard

Generate `delivery-dashboard.html` from the manifest with the standard modal template, then improve theme styling manually if the offer needs richer presentation. Preserve the modal/iframe structure.

```powershell
.\.venv\Scripts\python.exe plugins\offer-os\skills\offer-os\scripts\generate_delivery_dashboard.py --manifest offer-os.json --output delivery-dashboard.html --force
```

Register `delivery-dashboard`.

Do not write a dashboard from scratch unless the user explicitly asks for a different layout. If you need a different visual feel, change theme variables and card styling while keeping the generated modal/iframe interaction model.

## 16. QA

Run validation:

```powershell
.\.venv\Scripts\python.exe plugins\offer-os\skills\offer-os\scripts\validate_offer_outputs.py --manifest offer-os.json --strict --write-report qa-notes.md
```

Deep mode is not complete if the validator reports issues or warnings. Revise source generation and rerun until both counts are zero.

When changing the OfferOS skill itself or assessing a generated regression workspace, run the self-test:

```powershell
.\.venv\Scripts\python.exe plugins\offer-os\skills\offer-os\scripts\self_test_offer_os_skill.py
```

Maintainers may add `--bad-workspace <path-to-known-bad-output>` when testing against a local regression fixture.

Then perform browser/visual checks for sales page, PDF, VSL preview, deck, and dashboard. Run a commercial value audit for sales page, PDF product, ads, emails, VSL deck, and dashboard. Fix blockers before final delivery.

Register `qa-notes`.

## Final Response

List:

- created files
- validation performed
- known limitations
- next recommended improvement
