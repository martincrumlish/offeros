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

Stop conditions:

- If QA requires a manual patch, patch the generator and rerun from clean output.
- If `validate_offer_outputs.py --strict --no-write` returns issues or warnings, revise before handoff.
- If `qa-notes.md` contradicts `offer-os.json`, revise before handoff.

## Logo Recipe

Use this recipe for every deep generated-design run.

1. Read `offer-os.json`, `offer-architecture.md`, and `design.md`.
2. Write 3 logo concepts in `design.md` under `## Logo Concepts`. Each concept must include: concept name, visual idea, buyer/category signal, reason to select/reject.
3. Select 1 concept and write the reason in `design.md` under `## Selected Logo Concept`.
4. Call the `imagegen` skill/tool for the selected concept. Do not create the primary logo with SVG, HTML/CSS, PIL, canvas, screenshots, icon fonts, or CSS text.
5. Use this prompt structure for the `imagegen` call:

```text
Use case: logo-brand
Asset type: primary bitmap logo or brand mark for a digital offer
Offer name: [exact offer name]
Audience: [specific audience]
Positioning: [one-sentence promise/mechanism]
Visual direction: [selected concept from design.md]
Style: premium, simple, high-contrast, commercial, usable in a website header, product cover, ads, and dashboard
Composition: centered logo/brand mark on a plain background, generous padding, strong silhouette, legible at small size
Text handling: include no tiny text, no slogans, and no secondary lines. If exact text is included, use only "[exact offer name]".
Avoid: SVG/vector-code look, clip art, stock icons, mockup scenes, watermarks, fake UI, illegible letters, extra words, gradients that destroy small-size clarity
Output: finished bitmap logo/brand mark suitable to save as assets/logo.png
```

6. Inspect the image output. If the offer name is misspelled, malformed, or not legible, do one retry with a simpler prompt. If text still fails, use an imagegen text-free brand mark as `assets/logo.png` and render the offer name as live HTML text beside the logo in pages. Do not fall back to SVG.
7. Move or copy the selected imagegen output into the project as `assets/logo.png`.
8. Set `brand.logo` in `offer-os.json` to `assets/logo.png`.
9. Register the logo artifact exactly:

```powershell
.\.venv\Scripts\python.exe plugins\offer-os\skills\offer-os\scripts\register_artifact.py --id logo --title "Primary Logo" --type image --category Brand --path assets/logo.png --provenance imagegen --buyer-value 4 --usability 4 --trust 4
```

10. Set `quality.logo`:

```json
{
  "conceptCount": 3,
  "selectedConcept": "[concept name]",
  "primaryFormat": "png",
  "generationTool": "imagegen",
  "imagegenNotUsedReason": "",
  "vectorPrimaryUserRequested": false,
  "smallSizeChecked": true,
  "oneColorChecked": true,
  "exportedPng": true,
  "critiquePassed": true
}
```

Stop conditions:

- If the primary logo path is `.svg`, stop and rebuild the logo.
- If provenance is not `imagegen`, stop and rebuild the logo.
- If `assets/logo.png` does not exist, do not register `logo` as complete.
- If imagegen is unavailable, set `quality.logo.imagegenNotUsedReason`, mark `logo` as `needs_revision`, and do not set project status to complete.

## Sales Page Recipe

Use this recipe for every complete paid front-end offer unless the user explicitly asks for a different page type.

1. Set `quality.salesPage.pageType` to `direct-response-long-form-vsl`.
2. Write `copy.md` before `index.html`.
3. `copy.md` must include these exact headings:
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
4. Create `index.html` from `assets/templates/sales-page/page-skeleton.html`. Do not start from a blank page.
5. Use the exact hero contract from `assets/templates/sales-page/section-map.md`: buyer filter, prehead, H1, benefit lead, `data-offeros-hero-video`, `data-offeros-price-strip`, CTA to `#buy`, and `data-offeros-trust-row`.
6. Use the exact offer-stack buy-box contract from `assets/templates/sales-page/section-map.md`: `id="buy"`, product bundle visual, `data-offeros-offer-checklist` with 8+ deliverables, `data-offeros-value-row`, large `data-offeros-stack-cta`, and `data-offeros-access-copy`.
7. Keep every required `data-offeros-section` marker from `assets/templates/sales-page/section-map.md`.
8. Write unique benefit copy for every offer-stack item. Do not map a repeated sentence over multiple cards.
9. Include at least 7 FAQ objections, at least 4 CTA placements, and at least 2,500 visible words for `direct-response-long-form-vsl`.
10. Mark every FAQ item with `data-offeros-faq-item`.
11. Mark every CTA link or button with `data-offeros-cta`.
12. Set `quality.salesPage.visibleWordCount`, `objectionCount`, `ctaCount`, `offerStackItemsUnique`, `sectionDepthChecked`, `repeatedTextChecked`, `heroContract: "direct-response-hero-v1"`, and `offerStackContract: "direct-response-buy-box-v1"`.

Stop conditions:

- If `index.html` has fewer than 2,500 visible words for `direct-response-long-form-vsl`, revise before QA.
- If the hero does not include the video frame, price strip, CTA to `#buy`, and trust row, revise before QA.
- If the offer stack is only cards or a pricing panel instead of the buy-box checklist stack, revise before QA.
- If any sentence appears 4+ times in buyer-facing page copy, revise before QA.
- If the page can be summarized as hero/features/price/FAQ, revise before QA.

## PDF Product Recipe

Use this recipe for every paid front-end offer.

1. Choose a product type: toolkit, workbook, playbook, scorecard, checklist pack, implementation guide, or prompt bank.
2. Create an editable source file under `output/pdf/`.
3. Create the customer PDF under `output/pdf/`.
4. For $30-$99 offers, the product must have at least:
   - 25 pages
   - 4,000 extracted words unless the user explicitly approved a highly visual workbook
   - 8 buyer-action surfaces
   - 1 completed example and matching blank template for the core tool
5. Use buyer-action surfaces: audits, calculators, cards, examples, worksheets, templates, scripts, checklists, implementation plans, and debriefs.
6. Render at least 3 representative pages to `output/pdf/render-check/`.
7. Set `quality.pdf.pageCount`, `actionSurfaceCount`, `hasCompletedExamples`, `hasBlankTemplates`, and `renderChecked` from the generated artifact, not from memory.

Stop conditions:

- If the PDF is mostly repeated explanation plus blank lines, rebuild it as a toolkit/workbook.
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
10. Every bitmap image added to the PPTX must preserve aspect ratio. Do not call `slide.addImage({ path, x, y, w, h })` for a visual box unless the image's source ratio exactly matches that box. Use a local helper and route every VSL image through it:

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

11. Create HTML/contact-sheet only after the PPTX exists. Save it as `output/presentation/vsl-contact-sheet.png` or `output/presentation/vsl-preview.html`.
12. Register `vsl-deck` as the `.pptx`; set its `preview` to browser-safe `output/presentation/vsl-preview.html` or an image contact sheet, never to the `.pptx` itself.
13. Set `quality.vsl.maxLayoutShare`, `notesAreNarration`, `visibleStageLabelsRemoved`, `layoutDiversityChecked`, `visualPlaceholdersRemoved`, `visualAssetCount`, and `layoutAudit`.
14. Browser-test `output/presentation/vsl-preview.html` at desktop and about 390px mobile width. The build must fail if the preview has horizontal overflow or broken images.

Stop conditions:

- If the primary deck is HTML, stop and rebuild as PPTX.
- If stage labels are visible as slide titles, revise before QA.
- If one layout dominates the deck, revise before QA.
- If notes are author labels instead of narration, revise before QA.
- If any PPTX bitmap appears in a box with a different aspect ratio and no PowerPoint `sizing`/crop metadata, revise the generator before QA.
- If the dashboard iframe preview points at the `.pptx`, revise manifest preview metadata before QA.
