# Exact Build Recipes

Use these recipes in `deep` mode. Do not replace them with a similar-looking workflow. If a step cannot be performed, mark the artifact `needs_revision`, record the blocker in `qa-notes.md`, and continue only after the blocker is visible in `offer-os.json`.

## Build Controller Recipe

Use this controller for every deep run. This is the highest-level recipe and it overrides softer wording in other files.

1. Create or maintain a reproducible build script in `scripts/build_offer_system.*` or an equivalent checked-in script for the generated offer.
2. Generate buyer-facing artifacts from structured data/functions in that script. Do not hand-fix generated files after QA without also fixing the generator.
3. Treat validator warnings as build failures in deep mode. A warning is not acceptable handoff status for complete paid offers.
4. Run browser QA captures for:
   - sales page desktop
   - sales page mobile at about 390px wide
   - delivery dashboard desktop
   - delivery dashboard mobile at about 390px wide
   - VSL preview desktop
   - VSL preview mobile at about 390px wide
5. Browser QA must fail the build if any captured page has horizontal overflow or broken images.
6. Write `qa-notes.md` from live build variables and validation results. Do not hard-code page counts, CTA counts, warnings, or pass/fail claims.
7. Copy the final build script into the output project before handoff.
8. Create `visual-asset-plan.md` before building sales-page graphics, the PDF product, ads, or the VSL deck. Reusing sales-page images as the default visual pool fails deep mode.

Stop conditions:

- If QA requires a manual patch, patch the generator and rerun from clean output.
- If `validate_offer_outputs.py --strict --no-write` returns issues or warnings, revise before handoff.
- If `qa-notes.md` contradicts `offer-os.json`, revise before handoff.

## Logo Recipe

Use this recipe for every deep generated-design run.

1. Read `offer-os.json`, `offer-architecture.md`, and `design.md`.
2. Write 3 logo concepts in `design.md` under `## Logo Concepts`. Each concept must include: concept name, visual idea, buyer/category signal, reason to select/reject.
3. Select 1 concept and write the reason in `design.md` under `## Selected Logo Concept`.
4. Call the `imagegen` skill/tool for the selected concept to generate at least 3 complete logo lockup candidates. The first logo task is not a mark-only task. It must ask imagegen for a complete commercial logo with a symbol and exact wordmark in one bitmap. Do not create the primary logo with SVG, HTML/CSS, PIL, canvas, screenshots, icon fonts, or CSS text alone.
5. Use this prompt structure for each complete-lockup `imagegen` call:

```text
Use case: logo-brand
Asset type: complete bitmap logo lockup, symbol plus exact wordmark
Offer name: [exact offer name]
Audience: [specific audience]
Positioning: [one-sentence promise/mechanism]
Visual direction: [selected concept from design.md]
Style: flat, premium, simple, high-contrast, commercial identity logo, usable at 24px in a website header and at large size on a product cover
Composition: complete horizontal logo lockup on a plain background; simple symbol on the left; professionally designed wordmark on the right; strong silhouette; 1-2 main symbol shapes; minimal internal detail
Text handling: include the exact offer name "[exact offer name]" once as the wordmark. Do not insert spaces, split camel-case names, change capitalization, add slogans, add tiny text, or add secondary lines.
Avoid: mark-only output, icon-only output, illustration, app icon, map pin unless absolutely core to the concept, page curl, folded paper, 3D, shadows, photorealism, mockup scenes, tiny UI diagrams, busy funnel layers, clip art, stock icons, watermarks, fake UI, illegible letters, extra words, gradients that destroy small-size clarity
Output: finished complete logo lockup suitable to save as assets/logo.png
```

6. Inspect the complete logo candidates against this logo-lockup acceptance contract:
   - exact offer name appears once, readable, unbroken, and with the same capitalization as `offer-os.json.offerName`
   - wordmark looks integrated and designed, not default typed text pasted beside a mark
   - symbol is a simple flat logo symbol, not an illustration or rough cover graphic
   - no page curl, folded paper, 3D lighting, photoreal texture, mockup, or scene
   - no tiny UI/detail that disappears at nav size
   - usable at 24px in a header
   - usable in one color
   - visually connected to the selected logo concept, not a generic icon
7. If one complete logo candidate passes every item, crop or place it onto a horizontal logo canvas if needed, save it as `assets/logo.png`, set provenance to `imagegen`, and record `quality.logo.imagegenCompleteLogoAccepted = true`. The final `assets/logo.png` must be a horizontal lockup file, not a square raw imagegen canvas.
8. If all complete logo candidates fail because imagegen mangled the exact wordmark, do a second imagegen round for a text-free logo-grade symbol only. Use this prompt structure:

```text
Use case: logo-symbol-fallback
Asset type: text-free bitmap brand symbol for a complete logo lockup
Offer name context: [exact offer name]
Audience: [specific audience]
Positioning: [one-sentence promise/mechanism]
Visual direction: [selected concept from design.md]
Style: flat, premium, simple, high-contrast, commercial identity symbol, usable at 24px in a website header and at large size on a product cover
Composition: centered standalone symbol on a plain background, generous padding, strong silhouette, 1-2 main shapes, minimal internal detail
Text handling: no text, no letters, no slogans, no tiny labels
Avoid: illustration, app icon, map pin unless absolutely core to the concept, page curl, folded paper, 3D, shadows, photorealism, mockup scenes, tiny UI diagrams, busy funnel layers, clip art, stock icons, watermarks, fake UI, gradients that destroy small-size clarity
Output: finished text-free bitmap symbol suitable to combine into assets/logo.png
```

9. Inspect the fallback symbol against this symbol acceptance contract:
   - simple flat symbol, not an illustration or rough cover graphic
   - no page curl, folded paper, 3D lighting, photoreal texture, mockup, or scene
   - no tiny UI/detail that disappears at nav size
   - usable at 24px in a header
   - usable in one color
   - visually connected to the selected logo concept, not a generic icon
10. If the fallback symbol fails any item, do not use it. Retry imagegen with a simpler prompt. Do not composite a bad symbol with text and call it complete.
11. If the fallback symbol passes, build the final lockup with a professional wordmark compositor, not a rough "mark plus default text" image:
   - preserve the exact offer name string from `offer-os.json.offerName`; do not insert spaces, split camel-case names, change capitalization, or create accidental two-word spacing
   - use the typography system from `design.md`; if none exists, choose one professional display wordmark font and record the choice in `design.md`
   - use a real scalable font available on the machine or bundled into the project; do not use a default bitmap font or browser-default font
   - adjust weight, optical alignment, tracking, and mark-to-wordmark spacing intentionally
   - mark height must be visually balanced with the wordmark, usually 0.85-1.15x the wordmark cap height for header use
   - export as a horizontal lockup on transparent or plain background, not a square icon canvas
   - create a nav-size and cover-size preview at `output/qa/logo-lockup-preview.png`
12. Move or copy the fallback symbol imagegen output into the project as `assets/logo-mark.png` only when the complete-lockup attempts failed exact text. Build `assets/logo.png` as the complete horizontal logo lockup. The final primary logo must include the readable offer name in the bitmap itself and must not look like a rough text paste-up.
13. Set `brand.logo` in `offer-os.json` to `assets/logo.png`.
14. Register the logo artifact. Use `imagegen` only when the final `assets/logo.png` came directly from imagegen as a complete readable lockup. Use `imagegen-composite` only when complete-lockup imagegen attempts failed exact text and `assets/logo.png` combines an imagegen fallback symbol with exact rendered professional wordmark text:

```powershell
.\.venv\Scripts\python.exe plugins\offer-os\skills\offer-os\scripts\register_artifact.py --id logo --title "Primary Logo" --type image --category Brand --path assets/logo.png --provenance imagegen-composite --buyer-value 4 --usability 4 --trust 4
```

15. Set `quality.logo`:

```json
{
  "conceptCount": 3,
  "selectedConcept": "[concept name]",
  "primaryFormat": "png",
  "generationTool": "imagegen-complete-logo-attempts+imagegen-symbol+professional-wordmark-compositor",
  "imagegenNotUsedReason": "",
  "imagegenCompleteLogoLockupAttempted": true,
  "imagegenLogoCandidateCount": 3,
  "imagegenCompleteLogoAccepted": false,
  "fallbackWordmarkCompositeReason": "complete imagegen logo candidates failed exact-name text check",
  "brandMarkSource": "imagegen",
  "wordmarkSource": "professional-wordmark-compositor",
  "wordmarkCompositeMethod": "scripted-professional-compositor",
  "logoLockup": true,
  "includesReadableOfferName": true,
  "exactOfferNamePreserved": true,
  "markIsLogoSymbol": true,
  "markNotIllustration": true,
  "markOneColorUsable": true,
  "wordmarkTypographyChecked": true,
  "wordmarkKerningChecked": true,
  "professionalLockupApproved": true,
  "lockupPreviewChecked": true,
  "lockupPreviewPath": "output/qa/logo-lockup-preview.png",
  "vectorPrimaryUserRequested": false,
  "smallSizeChecked": true,
  "oneColorChecked": true,
  "exportedPng": true,
  "critiquePassed": true
}
```

Stop conditions:

- If the primary logo path is `.svg`, stop and rebuild the logo.
- If the primary `logo` artifact points to `assets/logo-mark.png` or any mark-only file, stop and rebuild the logo.
- If the primary logo is an icon or mark without the readable offer name, stop and rebuild the logo lockup.
- If imagegen was not first used for complete logo lockup candidates, stop and run the required complete-logo imagegen step.
- If `quality.logo.imagegenLogoCandidateCount` is less than `3`, stop and generate more complete-lockup candidates.
- If `quality.logo.imagegenCompleteLogoAccepted` is false and `quality.logo.fallbackWordmarkCompositeReason` is empty, stop and document why the fallback compositor was used.
- If the imagegen complete logo or fallback symbol is illustrative, page-curl/folded-paper, 3D, app-icon-like, a rough cover graphic, or too detailed for nav use, stop and regenerate it.
- If the wordmark is just default text pasted beside the mark, has awkward spacing, splits the exact offer name incorrectly, or looks like a rough composite, stop and rebuild the lockup.
- If provenance is not `imagegen` or `imagegen-composite`, stop and rebuild the logo.
- If `quality.logo.brandMarkSource` is not `imagegen`, stop and rebuild the logo.
- If `quality.logo.logoLockup`, `quality.logo.includesReadableOfferName`, `quality.logo.imagegenCompleteLogoLockupAttempted`, `quality.logo.exactOfferNamePreserved`, `quality.logo.markNotIllustration`, `quality.logo.wordmarkTypographyChecked`, `quality.logo.wordmarkKerningChecked`, or `quality.logo.professionalLockupApproved` is not `true`, stop and rebuild the logo.
- If `output/qa/logo-lockup-preview.png` does not exist, create the preview and inspect it before marking the logo complete.
- If `assets/logo.png` does not exist, do not register `logo` as complete.
- If imagegen is unavailable, set `quality.logo.imagegenNotUsedReason`, mark `logo` as `needs_revision`, and do not set project status to complete.

## Visual Asset Plan Recipe

Use this recipe for every deep generated-design run after the logo and product outline exist and before creating sales-page graphics, PDF pages, ad images, VSL slides, or the dashboard.

1. Create `visual-asset-plan.md`.
2. Divide the plan into these exact headings:
   - `# Visual Asset Plan`
   - `## Global Brand Assets`
   - `## Sales Page Visuals`
   - `## PDF Product Visuals`
   - `## VSL Deck Visuals`
   - `## Ad Visuals`
   - `## Dashboard Visuals`
   - `## Reuse Rules`
3. For every planned visual, list: artifact target, file path, visual job, source/provenance, generation prompt or production method, reuse permission, and whether it is specific to that artifact or shared.
4. Use these minimum visual budgets in deep mode:
   - Global/shared: logo lockup, brand mark, product bundle/mockup, and one reusable texture/pattern or brand frame.
   - Sales page: 4+ page-specific visuals: hero/VSL thumbnail, mechanism/framework, before/after or failed-alternative visual, proof/demo or product-stack visual.
   - PDF product: 6+ PDF visuals/treatments, with 4+ not reused from the sales page. Include cover art, at least one module/divider treatment, one decision matrix, one completed example visual, one blank worksheet/template visual, and one implementation/checklist visual.
   - VSL deck: 12+ unique visual assets or distinct diagram treatments, with 8+ not reused from the sales page. Include pattern interrupt, problem map, failed-alternatives comparison, mechanism diagram, product reveal, offer stack, price/value contrast, guarantee, objection, and final CTA visuals.
   - Ads: 3+ ad-specific imagegen creatives. Do not crop sales-page art and call it ad creative.
   - Dashboard: logo, product bundle/preview, and thumbnail/preview choices for the main assets.
5. If agents are authorized, load `references/agent-dispatch.md` and dispatch imagegen visual workers after this plan exists. Use separate workers for page visuals, PDF visuals, VSL visuals, and ad visuals. Each worker gets `offer-architecture.md`, `design.md`, `visual-asset-plan.md`, `assets/logo.png`, `assets/logo-mark.png` if present, and its assigned output folder. The main agent keeps ownership of integration, manifest registration, and QA.
6. If agents are not authorized or not available, create the visuals locally and set `quality.images.agentDispatchUsed` to `false` with a short `agentDispatchNotUsedReason`.
7. Register `visual-asset-plan` in `offer-os.json`:

```powershell
.\.venv\Scripts\python.exe plugins\offer-os\skills\offer-os\scripts\register_artifact.py --id visual-asset-plan --title "Visual Asset Plan" --type document --category Strategy --path visual-asset-plan.md --provenance manual --buyer-value 4 --usability 4 --trust 4
```

8. Set `quality.images`:

```json
{
  "hasArtifactSpecificPlan": true,
  "visualPlanPath": "visual-asset-plan.md",
  "visualReusePolicy": "artifact-specific-v1",
  "agentDispatchUsed": true,
  "agentDispatchNotUsedReason": "",
  "salesPageVisualCount": 4,
  "pdfVisualCount": 6,
  "pdfSpecificVisualCount": 4,
  "vslVisualCount": 12,
  "vslSpecificVisualCount": 8,
  "adImageCount": 3,
  "pdfUsesOnlySalesPageImages": false,
  "vslUsesOnlySalesPageImages": false,
  "salesPageReuseOnly": false
}
```

Stop conditions:

- If `visual-asset-plan.md` does not exist, stop before creating PDF, ads, or VSL.
- If the user explicitly allowed agents and no imagegen visual workers were dispatched, record the reason in `quality.images.agentDispatchNotUsedReason`.
- If the PDF visuals are only sales-page images, create PDF-specific visuals/treatments before building the PDF.
- If the VSL visuals are only sales-page images or the same few bitmaps repeated, create slide-specific visuals/treatments before generating the PPTX.
- If ad images are crops or text-card variants of sales-page visuals, create ad-specific imagegen creatives.

## Sales Page Recipe

Use this recipe for every complete paid front-end offer unless the user explicitly asks for a different page type.

1. Set `quality.salesPage.pageType` to `direct-response-long-form-vsl`.
2. Write `copy.md` before `index.html`.
3. Before writing the copy body, write a section-by-section copy blueprint with the conversion job, target word count, proof/objection handled, visual block, and CTA role for every section. This blueprint is not optional; it prevents a generic wall of text.
4. `copy.md` must include these exact headings:
   - `# Sales Page Type`
   - `# Hero`
   - `# VSL Setup`
   - `# Problem Diagnosis`
   - `# Agitation`
   - `# Failed Alternatives`
   - `# Unique Mechanism`
   - `# Before And After`
   - `# Product Reveal`
   - `# Offer Stack`
   - `# Proof Or Demonstration`
   - `# Who It Is For`
   - `# Who It Is Not For`
   - `# Pricing And Value`
   - `# Guarantee`
   - `# FAQ`
   - `# Final CTA`
5. Create `index.html` from `assets/templates/sales-page/page-skeleton.html`. Do not start from a blank page.
6. Use the exact hero contract from `assets/templates/sales-page/section-map.md`: buyer filter, prehead, H1, benefit lead, `data-offeros-hero-video`, `data-offeros-price-strip`, CTA to `#buy`, and `data-offeros-trust-row`.
7. Use the exact offer-stack buy-box contract from `assets/templates/sales-page/section-map.md`: `id="buy"`, product bundle visual, `data-offeros-offer-checklist` with 8+ deliverables, `data-offeros-value-row`, large `data-offeros-stack-cta`, and `data-offeros-access-copy`.
8. Keep every required `data-offeros-section` marker from `assets/templates/sales-page/section-map.md`, including the separate `agitation` section.
9. Write unique benefit copy for every offer-stack item. Do not map a repeated sentence over multiple cards.
10. Use direct-response composition rules:
    - Hero visible copy: 90-180 words, plus price strip and trust bullets.
    - VSL section: 80-220 words, one thumbnail/video block, 3-5 bullets, and one CTA. Do not put the whole sales letter in the VSL section.
    - Problem, agitation, failed alternatives, mechanism, product, proof, offer stack, guarantee, FAQ, and close must be separate visible sections.
    - No normal paragraph may exceed 55 words. Split long explanations into bullets, comparison rows, labeled callouts, or short copy blocks.
    - No section except FAQ or offer stack may exceed 500 visible words.
    - Failed alternatives tables, before/after blocks, product cards, and proof/demo blocks must have visible buyer-facing copy in every cell/card.
    - The design must use high-contrast text/background pairs; white text on white, low-contrast badges, and blank-looking cards are build failures.
11. Include at least 7 FAQ objections, at least 4 CTA placements, and at least 2,500 visible words for `direct-response-long-form-vsl`.
12. Mark every FAQ item with `data-offeros-faq-item`.
13. Mark every CTA link or button with `data-offeros-cta`.
14. Set `quality.salesPage.visibleWordCount`, `objectionCount`, `ctaCount`, `offerStackItemsUnique`, `sectionDepthChecked`, `repeatedTextChecked`, `compositionContract: "direct-response-composition-v1"`, `heroContract: "direct-response-hero-v1"`, and `offerStackContract: "direct-response-buy-box-v1"`.

Stop conditions:

- If `index.html` has fewer than 2,500 visible words for `direct-response-long-form-vsl`, revise before QA.
- If the VSL section becomes a wall of text or exceeds 220 visible words, revise before QA.
- If any normal paragraph exceeds 55 words, revise before QA.
- If required comparison/card sections contain blank-looking cells or empty cards, revise before QA.
- If the hero does not include the video frame, price strip, CTA to `#buy`, and trust row, revise before QA.
- If the offer stack is only cards or a pricing panel instead of the buy-box checklist stack, revise before QA.
- If any sentence appears 4+ times in buyer-facing page copy, revise before QA.
- If the page can be summarized as hero/features/price/FAQ, revise before QA.

## PDF Product Recipe

Use this recipe for every paid front-end offer.

1. Choose a product type: toolkit, workbook, playbook, scorecard, checklist pack, implementation guide, or prompt bank.
2. Write a product blueprint before generating pages. The blueprint must define:
   - buyer outcome and completion criteria
   - module list
   - named buyer tools/templates
   - completed examples
   - matching blank worksheets/templates
   - page archetype list
   - how the buyer uses the product in one sitting or one implementation cycle
3. Read `visual-asset-plan.md` and fulfill the `## PDF Product Visuals` section before rendering the PDF. PDF visuals are not limited to sales-page images. Create 6+ PDF visuals/treatments, including 4+ that are specific to the PDF product and not reused from the sales page.
4. Build a real product, not an ebook with repeated worksheet boxes. Every buyer-action page must have a specific name and job, such as "Funnel Fit Matrix", "Traffic Source Reality Check", "Buyer Awareness Mapper", "Offer Path Selector", or "Final Funnel Blueprint". Do not use the generic visible label "Action Surface" as a repeated page heading or box title.
5. Use at least 7 distinct page archetypes in deep mode: cover, quick start, guide lesson, comparison/decision matrix, completed example, blank worksheet, checklist, implementation plan, script/swipe, scoring/audit, or resource index. No single page archetype may exceed 35% of the PDF.
6. Create an editable source file under `output/pdf/`.
7. Create the customer PDF under `output/pdf/`.
8. For offers up to $29, the product must have at least:
   - 22 pages
   - 3,500 extracted words unless the user explicitly approved a highly visual workbook
   - 8 buyer-action surfaces
   - 8 named buyer tools/templates
   - 2 completed examples and matching blank templates for core tools
9. For $30-$99 offers, the product must have at least:
   - 25 pages
   - 4,000 extracted words unless the user explicitly approved a highly visual workbook
   - 8 buyer-action surfaces
   - 10 named buyer tools/templates
   - 3 completed examples and matching blank templates for core tools
10. Use buyer-action surfaces: audits, calculators, cards, examples, worksheets, templates, scripts, checklists, implementation plans, and debriefs.
11. Render representative pages from every page archetype to `output/pdf/render-check/`.
12. Set `quality.pdf.pageCount`, `actionSurfaceCount`, `namedToolCount`, `pageArchetypeCount`, `maxPageArchetypeShare`, `completedExampleCount`, `blankTemplateCount`, `visualAssetCount`, `pdfSpecificVisualAssetCount`, `genericActionSurfaceLabelsRemoved`, `hasCompletedExamples`, `hasBlankTemplates`, and `renderChecked` from the generated artifact, not from memory.

Stop conditions:

- If the PDF is mostly repeated explanation plus blank lines, rebuild it as a toolkit/workbook.
- If most pages reuse the same heading/body/"worksheet box" layout, rebuild with distinct page archetypes.
- If the phrase "Action Surface" appears as repeated buyer-facing page furniture, rebuild with named tools/templates.
- If the PDF has page count but lacks named tools, completed examples, and matching blank templates, rebuild before QA.
- If `quality.pdf.visualAssetCount` is below 6 or `quality.pdf.pdfSpecificVisualAssetCount` is below 4, create PDF-specific visuals/treatments and rebuild.
- If extracted text is below the price-point target, revise before QA.
- If page count or QA notes disagree with the actual PDF, revise before handoff.

## Email Sequence Recipe

Use this recipe for every launch or sales email artifact.

1. Choose a sequence framework from `references/email-frameworks.md`.
2. For a complete launch sequence, create at least 7 emails.
3. Every email must include:
   - send timing
   - subject line
   - preview text
   - campaign role
   - body copy
   - CTA
4. Each email must have a distinct conversion job. Do not paste the same product paragraph into every email.
5. Use objection progression: false belief, cost of belief, new insight, proof or demonstration, offer reveal, risk reversal, urgency or final close.

Stop conditions:

- If the email artifact lacks send timing, preview text, or campaign role, revise before QA.
- If two or more body blocks repeat verbatim, revise before QA.

## VSL Deck Recipe

Use this recipe for every VSL deck.

1. Create `output/presentation/[slug]-vsl.pptx` as the primary deck. Do not create HTML first.
2. Create a slide plan with 20-30 slides before generating the PPTX.
3. Assign every slide one of at least 8 layout names before generating the PPTX:
   - full-bleed-title
   - audience-filter
   - problem-map
   - compounding-chain
   - failed-alternatives-table
   - mechanism-diagram
   - product-reveal
   - proof-demo
   - offer-stack
   - price-value
   - guarantee
   - objection
   - final-cta
4. Layout family means structural composition, not color, icon, or background variation. A two-column copy/visual slide remains the same layout family even when colors, icons, headings, or placeholder labels change.
5. No layout family may be used on more than 35% of slides.
6. Write a slide-numbered layout audit before registering the deck. Record it in `quality.vsl.layoutAudit` as an array with `slide`, `layoutFamily`, and `visualAsset` for every slide.
7. Visible slide copy must be buyer-facing. Do not put `Hook`, `Problem`, `Agitate`, `Market`, `Mechanism`, `Proof`, `Offer`, `CTA`, `Objection`, `Close`, `Stage: Problem`, `Problem:`, or similar internal labels anywhere on a slide, including badges, footers, eyebrows, and small captions.
8. Speaker notes must be recording notes of at least 25 words per slide. Do not use notes such as `Explain mechanism`, `Show proof`, or `Agitate`.
9. Key slides must include visuals, diagrams, generated frames, screenshots, or product previews. Do not use dark placeholder rectangles with labels as finished visuals.
10. Read `visual-asset-plan.md` and fulfill the `## VSL Deck Visuals` section before generating the PPTX:
   - 12+ unique visual assets or clearly distinct diagram treatments across a 20-30 slide deck.
   - 8+ VSL visuals/treatments must be specific to the VSL deck and not reused from the sales page.
   - No single non-logo bitmap may appear on more than 25% of slides.
   - Do not recycle the same 3 hero/product images across the deck. A repeated theme is allowed; repeated bitmap filler is not.
   - Product bundle imagery may appear on product reveal, offer stack, value, and CTA slides only.
   - Every slide must have a specific visual job: pattern interrupt, comparison, map, matrix, mechanism diagram, example, proof substitute, product view, objection card, price/value contrast, or close.
11. Every bitmap image added to the PPTX must preserve aspect ratio. Do not call `slide.addImage({ path, x, y, w, h })` for a visual box unless the image's source ratio exactly matches that box. Use a local helper and route every VSL image through it:

```js
function addPptxImage(slide, relPath, x, y, w, h, fit = "cover") {
  slide.addImage({
    path: path.join(OUT, relPath),
    x,
    y,
    w,
    h,
    sizing: { type: fit, w, h },
  });
}

// Use cover for full-bleed/photo boxes. Use contain for logos, product bundles, and UI/product previews.
addPptxImage(slide, "assets/images/hero.png", 6.6, 0, 6.73, 7.5, "cover");
addPptxImage(slide, "assets/logo.png", 5.15, 4.55, 3.0, 1.7, "contain");
```

12. Create HTML/contact-sheet only after the PPTX exists. Save it as `output/presentation/vsl-contact-sheet.png` or `output/presentation/vsl-preview.html`.
13. Register `vsl-deck` as the `.pptx`; set its `preview` to browser-safe `output/presentation/vsl-preview.html` or an image contact sheet, never to the `.pptx` itself.
14. Set `quality.vsl.maxLayoutShare`, `notesAreNarration`, `visibleStageLabelsRemoved`, `layoutDiversityChecked`, `visualPlaceholdersRemoved`, `visualAssetCount`, `uniqueVisualAssetCount`, `vslSpecificVisualAssetCount`, `maxRepeatedBitmapShare`, `visualReuseChecked`, and `layoutAudit`.
15. Browser-test `output/presentation/vsl-preview.html` at desktop and about 390px mobile width. The build must fail if the preview has horizontal overflow or broken images.

Stop conditions:

- If the primary deck is HTML, stop and rebuild as PPTX.
- If stage labels are visible as slide titles, revise before QA.
- If one layout dominates the deck, revise before QA.
- If the same large bitmap appears on more than 25% of slides, revise the visual plan before QA.
- If the deck uses fewer than 12 unique visual assets/treatments or fewer than 8 VSL-specific visuals/treatments, revise before QA.
- If notes are author labels instead of narration, revise before QA.
- If any PPTX bitmap appears in a box with a different aspect ratio and no PowerPoint `sizing`/crop metadata, revise the generator before QA.
- If the dashboard iframe preview points at the `.pptx`, revise manifest preview metadata before QA.
