# Exact Build Recipes

Use these recipes in `deep` mode. Do not replace them with a similar-looking workflow. If a step cannot be performed, mark the artifact `needs_revision`, record the blocker in `qa-notes.md`, and continue only after the blocker is visible in `offer-os.json`.

## Build Controller Recipe

Use this controller for every deep run. This is the highest-level recipe and it overrides softer wording in other files.

1. Use the plugin-owned OfferOS Studio dispatcher and builders as the production source of truth. Start with `scripts/offeros.py`, then call the relevant studio builder: `build_visual_asset_plan.py`, `build_sales_page.py`, `build_email_sequence.py`, `build_workbook.py`, `build_vsl_deck.js`, `generate_delivery_dashboard.py`, and `validate_offer_outputs.py`.
2. Do not create `scripts/build_offer_system.*` in the generated project as the production controller. Generated projects may contain source JSON, static artifacts, previews, and tiny helper scripts, but the real builders live in the plugin.
3. Generate buyer-facing artifacts from canonical source files: `offer-intake.json`, `offer-architecture.json`, `design.md`, `theme.json`, `copy.md`, `copy-plan.json`, `visual-asset-plan.json`, `sales-page/sales-page-blueprint.json` or `sales-page-blueprint.json`, `workbook/workbook-blueprint.json`, `workbook/workbook-content.json`, `email-sequence.json`, and `presentation/vsl-deck-plan.json`.
4. Write quality metadata from measured builder output and validator checks. Do not backfill optimistic quality scores at the end.
5. Treat validator warnings as build failures in deep mode. A warning is not acceptable handoff status for complete paid offers.
6. Run browser QA captures for:
   - sales page desktop
   - sales page mobile at about 390px wide
   - delivery dashboard desktop
   - delivery dashboard mobile at about 390px wide
   - VSL preview desktop
   - VSL preview mobile at about 390px wide
7. Browser QA must fail the build if any captured page has horizontal overflow or broken images.
8. Write `qa-notes.md` from live build variables and validation results. Do not hard-code page counts, CTA counts, warnings, or pass/fail claims.
9. Create `visual-asset-plan.json` and `visual-asset-plan.md` v2 only after `copy.md` contains the sales-page section blueprint. Reusing sales-page images as the default visual pool fails deep mode.

Stop conditions:

- If QA requires a manual patch, patch the plugin-owned studio builder or canonical source file and rerun from clean output.
- If a generated project contains `scripts/build_offer_system.*` as the production controller, remove that path and rebuild through the OfferOS Studio dispatcher.
- If `validate_offer_outputs.py --strict --no-write` returns issues or warnings, revise before handoff.
- If `qa-notes.md` contradicts `offer-os.json`, revise before handoff.

## OfferOS Production Studio Recipe

Use this recipe for complete OfferOS builds.

1. Run or follow `scripts/offeros.py` as the command dispatcher. Valid public commands are `intake`, `plan`, `build-assets`, `build-sales-page`, `build-emails`, `build-workbook`, `build-vsl`, `build-dashboard`, `validate`, and `build-all`.
2. Intake Studio creates or updates `offer-intake.json`. Ask blocking questions if buyer, promise, mechanism, proof level, price, guarantee, checkout target, design/image constraints, or urgency basis are missing.
3. Strategy + Copy Studio creates `offer-architecture.json`, `offer-architecture.md`, `copy.md`, and `copy-plan.json`. The sales copy and section blueprint must exist before sales-page visual planning.
4. Visual Asset Studio creates canonical `visual-asset-plan.json` and human-readable `visual-asset-plan.md`. Every visual row must carry `visualKind`, `copyAnchor`, `conversionJob`, `artifactTarget`, `aspectRatio`, `textRule`, and `source/provenance`.
5. Sales Page Studio builds `index.html` from the Page Kit builder and records `quality.salesPage.studio: "sales-page-studio-v1"`.
6. Email Launch Studio builds from `email-sequence.json`, renders Markdown/HTML, and records `quality.emails.studio: "email-launch-studio-v1"`.
7. PDF Workbook Studio builds from `workbook/workbook-blueprint.json` and `workbook/workbook-content.json`, renders HTML, renders PDF through Gotenberg/Chromium in deep mode, and records `quality.pdf.renderBackend: "gotenberg-chromium"`.
8. VSL Deck Studio builds from `presentation/vsl-deck-plan.json` through `pptxgenjs` by default, outputs `.pptx`, creates a browser-safe preview, and records `quality.vsl.studio: "vsl-deck-studio-v1"`.
9. Dashboard Studio uses `scripts/generate_delivery_dashboard.py` and preserves the v2 modal/iframe shell.
10. QA + Critic Studio runs `validate_offer_outputs.py --strict --no-write`; QA notes are written from measured results only.

## Logo Recipe

Use this recipe for every deep generated-design run.

1. Read `offer-os.json`, `offer-architecture.md`, and `design.md`.
2. Write exactly one final logo direction in `design.md` under `## Logo Direction`. Do not create a set of 3 logo options. The direction must include: symbol/wordmark idea, exact color treatment, buyer/category signal, small-size behavior, and why it fits the offer.
3. Call the `imagegen` skill/tool once for that final direction to generate one complete commercial logo lockup. Do not create 3 logo files, option sheets, alternate lockups, or a variation grid. The logo task is not a mark-only task. It must ask imagegen for a complete commercial logo with a symbol and exact wordmark in one bitmap. Do not create any logo or brand asset as SVG. Do not create the primary logo with HTML/CSS, PIL, canvas, screenshots, icon fonts, CSS text alone, or deterministic text compositing.
4. Use this prompt structure for the single final logo `imagegen` call:

```text
Use case: logo-brand
Asset type: one final complete bitmap logo lockup, symbol plus exact wordmark
Offer name: [exact offer name]
Audience: [specific audience]
Positioning: [one-sentence promise/mechanism]
Visual direction: [single final logo direction from design.md]
Style: flat, premium, simple, high-contrast, commercial identity logo, usable at 24px in a website header and at large size on a product cover
Composition: complete horizontal logo lockup on a plain background; simple symbol on the left; professionally designed wordmark on the right; strong silhouette; 1-2 main symbol shapes; minimal internal detail
Text handling: include the exact offer name "[exact offer name]" once as the wordmark. Do not insert spaces, split camel-case names, change capitalization, add slogans, add tiny text, or add secondary lines.
Avoid: multiple logo options, option sheet, mark-only output, icon-only output, illustration, app icon, map pin unless absolutely core to the direction, page curl, folded paper, 3D, shadows, photorealism, mockup scenes, tiny UI diagrams, busy funnel layers, clip art, stock icons, watermarks, fake UI, illegible letters, extra words, gradients that destroy small-size clarity
Output: finished complete logo lockup suitable to save as assets/logo.png
```

5. Inspect the single final logo against this logo-lockup acceptance contract:
   - exact offer name appears once, readable, unbroken, and with the same capitalization as `offer-os.json.offerName`
   - wordmark looks integrated and designed, not default typed text pasted beside a mark
   - symbol is a simple flat logo symbol, not an illustration or rough cover graphic
   - no page curl, folded paper, 3D lighting, photoreal texture, mockup, or scene
   - no tiny UI/detail that disappears at nav size
   - usable at 24px in a header
   - usable in one color
   - visually connected to the final logo direction, not a generic icon
6. If the generated logo fails the contract, discard it and rerun the same single-final-logo step with a simpler final direction. Do not keep multiple alternatives in the project, do not show three options, and do not let rejected attempts become downstream references.
7. When the single final logo passes, save it as `assets/logo.png`, set provenance to `imagegen`, and record `quality.logo.imagegenCompleteLogoAccepted = true`. The final `assets/logo.png` must be a horizontal lockup file, not a square raw imagegen canvas.
8. Do not use a symbol-only fallback or professional wordmark compositor unless the user explicitly approves a non-imagegen logo repair. In normal deep generated-design runs, a failed wordmark means rerun the single final imagegen logo, not build a separate text composite.
9. Set `brand.logo` in `offer-os.json` to `assets/logo.png`.
10. Freeze the final logo before any other image generation:
   - write the final single logo file in `design.md` under `## Final Logo Lockup`
   - set `quality.logo.finalLogoLocked = true`
   - set `quality.logo.downstreamLogoReference = "assets/logo.png"`
   - set `quality.logo.downstreamImagegenLogoReference = "assets/logo.png"`
   - set `quality.logo.singleFinalLogoOnly = true`
   - set `quality.logo.alternateLogosCreated = false`
   - set `quality.logo.downstreamImagegenMustUseLogoReference = true`
   - do not pass any old logo attempts, sketches, rejected images, or screenshots as downstream logo references
   - for downstream imagegen visuals that need the logo visible, pass `assets/logo.png` as the only logo reference image and prompt: `Use the supplied assets/logo.png exactly as the product/brand logo. Do not invent, redesign, recolor, redraw, reinterpret, replace, or substitute the logo or wordmark.`
11. Register the logo artifact with `provenance: imagegen`. Do not register a generated-design logo as `imagegen-composite`; if the logo needs repair, regenerate or edit it with imagegen:

```powershell
.\.venv\Scripts\python.exe plugins\offer-os\skills\offer-os\scripts\register_artifact.py --id logo --title "Primary Logo" --type image --category Brand --path assets/logo.png --provenance imagegen --buyer-value 4 --usability 4 --trust 4
```

12. Set `quality.logo`:

```json
{
  "logoMode": "single-final-logo-v1",
  "logoDirectionCount": 1,
  "finalLogoDirection": "[single final direction name]",
  "finalLogoLocked": true,
  "downstreamLogoReference": "assets/logo.png",
  "downstreamImagegenLogoReference": "assets/logo.png",
  "singleFinalLogoOnly": true,
  "alternateLogosCreated": false,
  "downstreamImagegenMustUseLogoReference": true,
  "primaryFormat": "png",
  "generationTool": "imagegen-single-final-logo",
  "imagegenNotUsedReason": "",
  "imagegenCompleteLogoLockupAttempted": true,
  "finalLogoCount": 1,
  "logoGenerationCount": 1,
  "imagegenCompleteLogoAccepted": true,
  "fallbackWordmarkCompositeReason": "",
  "brandMarkSource": "imagegen",
  "wordmarkSource": "imagegen",
  "wordmarkCompositeMethod": "",
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
  "svgAssetCreated": false,
  "smallSizeChecked": true,
  "oneColorChecked": true,
  "exportedPng": true,
  "critiquePassed": true
}
```

Stop conditions:

- If any generated logo, brand, ad, page, PDF, VSL, or visual artifact path is `.svg`, stop and rebuild it as PNG/WebP/JPG or HTML/CSS with no SVG file.
- If the primary `logo` artifact points to `assets/logo-mark.png` or any mark-only file, stop and rebuild the logo.
- If the primary logo is an icon or mark without the readable offer name, stop and rebuild the logo lockup.
- If imagegen was not used for the single final complete logo lockup, stop and run the required single-final-logo imagegen step.
- If `quality.logo.finalLogoCount` is not `1`, stop and remove the multi-logo workflow.
- If `quality.logo.logoGenerationCount` is not `1`, stop and remove the multi-logo workflow.
- If `quality.logo.singleFinalLogoOnly` is not true, stop before downstream visuals.
- If `quality.logo.alternateLogosCreated` is not false, stop and remove alternate logo files from the run.
- If the imagegen complete logo is illustrative, page-curl/folded-paper, 3D, app-icon-like, a rough cover graphic, or too detailed for nav use, stop and regenerate it as the single final logo.
- If the wordmark is just default text pasted beside the mark, has awkward spacing, splits the exact offer name incorrectly, or looks like a rough composite, stop and rebuild the lockup.
- If provenance is not `imagegen`, stop and rebuild the generated logo.
- If `quality.logo.svgAssetCreated` is not false, stop and remove the SVG path from the generated artifact set.
- If `quality.logo.finalLogoLocked` is not true, stop before creating downstream visuals.
- If `quality.logo.downstreamLogoReference` is not `assets/logo.png`, stop before dispatching image workers or building visual assets.
- If `quality.logo.downstreamImagegenLogoReference` is not `assets/logo.png`, stop before dispatching image workers or building visual assets.
- If any downstream imagegen prompt asks for a logo, wordmark, or brand name but does not pass `assets/logo.png` as the exact logo reference, stop and rewrite the prompt.
- If any downstream imagegen prompt asks imagegen to invent, redesign, recolor, redraw, reinterpret, replace, or substitute the logo, stop and rewrite the prompt.
- If `quality.logo.brandMarkSource` is not `imagegen`, stop and rebuild the logo.
- If `quality.logo.logoLockup`, `quality.logo.includesReadableOfferName`, `quality.logo.imagegenCompleteLogoLockupAttempted`, `quality.logo.exactOfferNamePreserved`, `quality.logo.markNotIllustration`, `quality.logo.wordmarkTypographyChecked`, `quality.logo.wordmarkKerningChecked`, or `quality.logo.professionalLockupApproved` is not `true`, stop and rebuild the logo.
- If `output/qa/logo-lockup-preview.png` does not exist, create the preview and inspect it before marking the logo complete.
- If `assets/logo.png` does not exist, do not register `logo` as complete.
- If imagegen is unavailable, set `quality.logo.imagegenNotUsedReason`, mark `logo` as `needs_revision`, and do not set project status to complete.

## Visual Asset Plan Recipe

Use this recipe for every deep generated-design run after the logo, product outline, and `copy.md` sales-page blueprint exist and before creating sales-page graphics, PDF pages, ad images, VSL slides, or the dashboard. This is a post-content-blueprint plan, not a loose pre-copy mood board.

1. Create `visual-asset-plan.md`.
2. Divide the plan into these exact headings:
   - `# Visual Asset Plan`
   - `## Visual Plan Metadata`
   - `## Global Brand Assets`
   - `## Sales Page Visuals`
   - `## PDF Product Visuals`
   - `## VSL Deck Visuals`
   - `## Ad Visuals`
   - `## Dashboard Visuals`
   - `## Reuse Rules`
3. In `## Visual Plan Metadata`, record these exact fields:
   - `visualPlanStage: post-content-blueprint`
   - `copyBlueprintUsed: true`
   - `salesPageImageSystem: mixed-direct-response-v1`
   - `primaryConversionFinalPixelsPolicy: imagegen-final-v1`
   - `aspectRatioPolicy: slot-aware-v1`
   - `logoReference: assets/logo.png`
   - `logoUsagePolicy: use-locked-logo-reference`
   - `alternateLogosCreated: false`
   - `mockupHeavyUserRequested: false` unless the user explicitly requested mockup-heavy art direction
   - `sourceBlueprints: copy.md, product blueprint/page archetypes, VSL slide plan, ad angle map`
4. For every planned visual, list these exact fields: `artifactTarget`, `filePath`, `visualKind`, `copyAnchor`, `conversionJob`, `aspectRatio`, `aspectRatioReason`, `displayIntent`, `maxDisplayHeight`, `textRule`, `source/provenance`, `finalPixelsGeneratedBy`, `localPostprocess`, `localCreativeOverlay`, `reusePermission`, `artifactSpecific`, and `generationPrompt` or `productionMethod`.
5. Use only these `visualKind` values unless the user supplied a specific visual system that requires an extra kind: `hero-vsl-frame`, `product-mockup`, `dashboard-mockup`, `offer-stack-bundle`, `mechanism-diagram`, `comparison-visual`, `proof-demo-visual`, `buyer-situation-photo`, `structured-panel`, `worksheet-preview`, `matrix-visual`, `checklist-visual`, `slide-pattern-interrupt`, `ad-creative`, `brand-frame`.
6. For `## Sales Page Visuals`, every row must include a `copyAnchor` matching a real sales-page section from `copy.md` and the page skeleton, such as `hero`, `vsl`, `failed-alternatives`, `mechanism`, `proof`, `product`, `offer-stack`, `pricing`, `guarantee`, or `faq`.
7. Use `mixed-direct-response-v1` by default:
   - use `product-mockup`, `dashboard-mockup`, or `offer-stack-bundle` mainly for product reveal, offer stack, dashboard preview, and CTA/product bundle sections
   - use `mechanism-diagram`, `comparison-visual`, `proof-demo-visual`, `structured-panel`, or restrained `buyer-situation-photo` for mechanism, failed alternatives, proof/demo, objections, feature specifics, and problem/agitation sections
   - do not make every sales-page image a polished fake UI/product mockup unless `mockupHeavyUserRequested: true`
   - avoid busy fake UI, hallucinated dashboards, illegible tiny text, decorative abstract mockups, and visuals that do not support a specific copy claim
   - use slot-aware aspect ratios instead of repeating one default size: hero/VSL and offer-stack visuals are usually wide 16:9, comparison visuals often need 16:9, mechanism diagrams often work as 3:2, proof/demo visuals often work as 16:10, and before/after panels may need a wide 2:1 composition
   - add `aspectRatioReason`, `displayIntent`, and `maxDisplayHeight` so imagegen workers know the actual destination shape before generation
   - set `source/provenance: imagegen-final`, `finalPixelsGeneratedBy: imagegen`, `localCreativeOverlay: false`, and `localPostprocess` limited to crop, resize, compression, or format-conversion for `hero-vsl-frame`, `product-mockup`, `offer-stack-bundle`, `buyer-situation-photo`, and `ad-creative` rows unless the asset is user-provided or licensed
   - use `imagegen-composite` only when the composition itself was performed by imagegen using reference images; in that case also set `imagegenNativeComposite: true`, `finalPixelsGeneratedBy: imagegen`, and `localCreativeOverlay: false`
   - do not set `productionMethod`, `source/provenance`, or fallback notes for those rows to `Pillow`, `PIL`, `html-css`, `canvas`, `screenshot`, `generated-by-code`, or `manual`; HTML/CSS, canvas, screenshots, and generated-by-code are allowed only for diagrams, worksheets, matrices, previews, QA screenshots, and real screenshots of built artifacts. Pillow/PIL is never allowed as an output authoring method.
   - do not use Pillow, canvas, HTML/CSS screenshots, or local scripts to add logo, headline text, labels, UI cards, badges, mockups, overlays, or product-stack composition after imagegen. If the creative is wrong, regenerate or edit with imagegen.
   - if a row needs the logo visible inside a generated product bundle, product mockup, dashboard mockup, ad, PDF visual, or VSL visual, its `generationPrompt` must include `logoReference: assets/logo.png` and must instruct imagegen to use that supplied logo exactly with no redesign, recolor, redraw, reinterpretation, replacement, or substitute logo
8. Use these minimum visual budgets in deep mode:
   - Global/shared: logo lockup, brand mark, product bundle/mockup, and one reusable texture/pattern or brand frame.
   - Sales page: 4+ page-specific visuals anchored to copy sections: hero/VSL thumbnail, mechanism/framework, failed-alternative or before/after visual, proof/demo or product-stack visual.
   - PDF product: 6+ PDF visuals/treatments, with 4+ not reused from the sales page. Include cover art, at least one module/divider treatment, one decision matrix, one completed example visual, one blank worksheet/template visual, and one implementation/checklist visual.
   - VSL deck: 12+ unique visual assets or distinct diagram treatments, with 8+ not reused from the sales page. Include pattern interrupt, problem map, failed-alternatives comparison, mechanism diagram, product reveal, offer stack, price/value contrast, guarantee, objection, and final CTA visuals.
   - Ads: 3+ ad-specific imagegen creatives. Do not crop sales-page art and call it ad creative.
   - Dashboard: logo, product bundle/preview, and thumbnail/preview choices for the main assets.
9. If agents are authorized, load `references/agent-dispatch.md` and dispatch imagegen visual workers after this plan exists. Use separate workers for page visuals, PDF visuals, VSL visuals, and ad visuals. Each worker gets `offer-architecture.md`, `design.md`, `copy.md`, `visual-asset-plan.md`, the frozen final `assets/logo.png`, the product blueprint/page archetypes, VSL slide plan, ad angle map, and its assigned output folder. Do not give workers any other logo image. The main agent keeps ownership of integration, manifest registration, and QA.
10. If agents are not authorized or not available, create the visuals locally and set `quality.images.agentDispatchUsed` to `false` with a short `agentDispatchNotUsedReason`.
11. Register `visual-asset-plan` in `offer-os.json`:

```powershell
.\.venv\Scripts\python.exe plugins\offer-os\skills\offer-os\scripts\register_artifact.py --id visual-asset-plan --title "Visual Asset Plan" --type document --category Strategy --path visual-asset-plan.md --provenance manual --buyer-value 4 --usability 4 --trust 4
```

12. Set `quality.images`:

```json
{
  "hasArtifactSpecificPlan": true,
  "visualPlanPath": "visual-asset-plan.md",
  "visualPlanStage": "post-content-blueprint",
  "copyBlueprintUsed": true,
  "visualReusePolicy": "artifact-specific-v1",
  "salesPageImageSystem": "mixed-direct-response-v1",
  "logoReference": "assets/logo.png",
  "logoUsagePolicy": "use-locked-logo-reference",
  "alternateLogosCreated": false,
  "mockupHeavyUserRequested": false,
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
- If `copy.md` with the sales-page section blueprint does not exist, stop before creating `visual-asset-plan.md`.
- If `quality.images.visualPlanStage` is not `post-content-blueprint` or `quality.images.copyBlueprintUsed` is not `true`, rebuild the plan after copy.
- If `quality.images.salesPageImageSystem` is not `mixed-direct-response-v1` and the user did not explicitly request another image system, rebuild the plan.
- If any sales-page visual lacks `visualKind`, `copyAnchor`, `conversionJob`, `artifactTarget`, `aspectRatio`, or `textRule`, rebuild the plan.
- If every sales-page visual is a mockup-style visual and `mockupHeavyUserRequested` is not `true`, revise to a mixed direct-response visual system.
- If a product bundle, offer-stack bundle, product mockup, hero/VSL thumbnail, buyer-situation photo, or ad creative is planned as PIL/HTML/CSS/canvas/screenshot/generated-by-code/manual, stop and replace it with an `imagegen-final` job or a provided/licensed asset.
- If a primary conversion visual says `imagegen-composite` but does not record `imagegenNativeComposite: true`, `finalPixelsGeneratedBy: imagegen`, and `localCreativeOverlay: false`, stop and regenerate/edit the final asset through imagegen.
- If local post-processing adds logo, headline text, labels, UI cards, badges, mockups, overlays, or product-stack composition after imagegen, stop and regenerate/edit with imagegen.
- If any artifact is registered with `provenance: pil-generated`, stop and rebuild. Pillow may inspect or transform source images but must not be the creative source of an OfferOS output.
- If a downstream imagegen row needs the logo and does not include `logoReference: assets/logo.png`, stop and rewrite the prompt.
- If a downstream imagegen row asks for a logo but asks imagegen to invent, redesign, recolor, redraw, reinterpret, replace, or substitute it, stop and rewrite the prompt.
- If the user explicitly allowed agents and no imagegen visual workers were dispatched, record the reason in `quality.images.agentDispatchNotUsedReason`.
- If the PDF visuals are only sales-page images, create PDF-specific visuals/treatments before building the PDF.
- If the VSL visuals are only sales-page images or the same few bitmaps repeated, create slide-specific visuals/treatments before generating the PPTX.
- If ad images are crops or text-card variants of sales-page visuals, create ad-specific imagegen creatives.

## Sales Page Recipe

Use this recipe for every complete paid front-end offer unless the user explicitly asks for a different page type.

1. Set `quality.salesPage.pageType` to `direct-response-long-form-vsl`.
2. Load `references/direct-response-framework.md` before writing `copy.md`.
3. Write `copy.md` before `index.html`.
4. Before writing the copy body, write `# Section Blueprint` as a Markdown table with one row for every required page section. Each row must include `sectionId`, `conversionJob`, `targetWords`, `beliefShift`, `proofOrObjection`, `visualKind`, `copyAnchor`, and `ctaRole`. This blueprint is not optional; it prevents a generic wall of text and becomes the source for `visual-asset-plan.md` v2.
5. `copy.md` must include these exact headings:
   - `# Sales Page Type`
   - `# Section Blueprint`
   - `# Hero`
   - `# VSL Setup`
   - `# Problem Diagnosis`
   - `# Agitation`
   - `# Failed Alternatives`
   - `# Unique Mechanism`
   - `# Proof Or Demonstration`
   - `# Before And After`
   - `# Product Reveal`
   - `# Offer Stack`
   - `# Who It Is For`
   - `# Who It Is Not For`
   - `# Pricing And Value`
   - `# Guarantee`
   - `# FAQ`
   - `# Final CTA`
6. Write `sales-page-blueprint.json` from `schemas/sales-page-blueprint.schema.json`. It must select exactly one Page Kit archetype from `classic-vsl-longform`, `modern-vsl-software`, `one-page-tripwire`, `challenge-workshop`, or `toolkit-workbook`; set the same value in `pageKitArchetype`; set `checkout.target` or `checkoutTarget` to `#checkout`; set `orderForm` to false; and map required plus optional sections to approved Page Kit blocks.
7. Write `theme.json` from `schemas/theme.schema.json` or a compatible Page Kit theme preset in `assets/page-kit/themes/`. It must select exactly one theme preset from `light-saas-direct-response`, `classic-direct-response`, `bold-webinar`, `premium-editorial`, `fitness-performance`, or `creator-workshop`. It controls style, typography, spacing, card treatment, and motion; it must not alter the conversion structure.
8. Build `index.html` only by running `scripts/build_sales_page.py`. Do not hand-write `index.html`, do not start from a blank page, and do not replace the locked hero or offer-stack shell with a custom layout.
9. Use the exact stacked VSL-first hero v2 contract from `assets/templates/sales-page/section-map.md`: `data-offeros-hero-layout="stacked-vsl"`, `data-offeros-hero-contract="stacked-vsl-hero-v2"`, `data-offeros-template="offeros-stacked-vsl-v2"`, `oo-hero oo-hero-stacked-vsl`, centered buyer filter, prehead, H1, benefit lead, `data-offeros-hero-copy-stack`, large centered `.oo-vsl-frame` with `data-offeros-hero-video`, `data-offeros-hero-video-prominence="primary"`, `data-offeros-hero-video-size="large"`, thumbnail marked `data-offeros-video-thumbnail`, play button marked `data-offeros-video-play`, caption marked `data-offeros-video-caption`, `data-offeros-price-strip` below the video, CTA to `#checkout`, and `data-offeros-trust-row`.
10. Use the exact offer-stack buy-box contract from `assets/templates/sales-page/section-map.md`: `id="checkout"` or `data-offeros-buy-section`, product bundle visual, `data-offeros-offer-checklist` with 8+ deliverables, `data-offeros-value-row`, large `data-offeros-stack-cta`, and `data-offeros-access-copy`. Do not include an embedded checkout, order form, payment fields, or credit-card form.
11. Keep every required `data-offeros-section` marker from `assets/templates/sales-page/section-map.md`, including the separate `agitation`, `failed-alternatives`, `mechanism`, and pre-offer `proof` sections.
   Proof/demo must appear before the main offer stack.
12. Follow this DOM order: `hero`, `vsl`, `problem`, `agitation`, `failed-alternatives`, `mechanism`, `proof`, `before-after`, `product`, `offer-stack`, `fit`, `pricing`, `guarantee`, `faq`, `final-cta`.
13. Write unique benefit copy for every offer-stack item. Do not map a repeated sentence over multiple cards.
14. Use direct-response composition rules:
    - Header: simple logo/brand area and optional primary CTA only. Do not add sticky/hover section navigation, nav menus, or section jump links for long-form sales pages.
    - Eyebrows/preheads/buyer filters: quiet signposts, not loud mini-headlines. Use restrained weight, no heavy all-caps badge treatment by default, and do not let these labels visually overpower the actual H1/H2.
    - Section eyebrows/pills: use `eyebrowPolicy: "sparse-key-signposts-v1"` by default. Do not put an eyebrow/pill on every section. Use them only for key signposts such as problem, mechanism, proof, offer stack, and guarantee unless the page type explicitly needs fewer/more.
    - Eyebrow alignment: every visible section eyebrow/pill must use `eyebrowAlignment: "centered-with-section-heading"` and be centered with the H2 it precedes; no floating left-offset pills above centered H2s.
    - Section rhythm: H2s should be wide enough for direct-response readability, generally centered for major sections, with enough vertical space that the page does not become a tight stack of boxes.
    - Cards/checklists: use a branded icon or checkmark treatment for card groups, proof blocks, and deliverable lists. Plain text boxes with no iconography or visual hierarchy fail the page kit.
    - Icons: use Lucide icon markers (`data-lucide`) with CSS fallback for card groups and checklist treatments.
    - Image display: render every support image, product reveal, offer-stack bundle, and proof/demo visual inside a content-hugging constrained frame marked `data-offeros-image-display="constrained"`. The outer figure/frame must be transparent and unbordered; apply border/shadow to the image itself. Do not leave full-size source images to dominate an entire viewport, and do not place contained images inside visibly larger colored mattes. Default desktop max visual height is about 560px; mobile is about 420px unless a specific image type requires less.
    - Hero visible copy: 90-180 words, plus price strip and trust bullets.
    - Hero layout: stacked VSL-first only. Do not use a two-column, side-by-side, split-screen, `hero-grid`, `hero-split`, `hero-visual`, `hero-mockup`, product/dashboard mockup hero art, or SaaS product hero with the video small on the right.
    - VSL section: 80-220 words, 3-5 bullets, and one CTA. Do not put the whole sales letter in the VSL section. If the hero already contains the main VSL frame, do not label the later section "Watch this first"; use a label like "What the breakdown covers" or "The pitch in plain English".
    - Problem, agitation, failed alternatives, mechanism, proof, product, offer stack, guarantee, FAQ, and close must be separate visible sections.
    - Proof/demo must appear before the main offer stack. If real testimonials are unavailable, use proof substitutes: worked examples, sample outputs, screenshots, mini demos, process logic, or transparent caveated examples.
    - No normal paragraph may exceed 55 words. Split long explanations into bullets, comparison rows, labeled callouts, or short copy blocks.
    - No section except FAQ or offer stack may exceed 500 visible words.
    - Failed alternatives tables, before/after blocks, product cards, and proof/demo blocks must have visible buyer-facing copy in every cell/card.
    - The design must use high-contrast text/background pairs; white text on white, low-contrast badges, and blank-looking cards are build failures.
15. Include at least 7 FAQ objections, at least 4 CTA placements, at least 3 post-hero CTA placements, and at least 2,500 visible words for `direct-response-long-form-vsl`.
16. Mark every FAQ item with `data-offeros-faq-item`.
17. Mark every CTA link or button with `data-offeros-cta`; mark post-hero CTA placements with `data-offeros-post-hero-cta`; purchase CTAs must link to `#checkout` by default.
18. Set `quality.salesPage.visibleWordCount`, `objectionCount`, `ctaCount`, `postHeroCtaCount`, `offerStackItemsUnique`, `sectionDepthChecked`, `repeatedTextChecked`, `copyBlueprintPresent: true`, `framework: "direct-response-long-form-v1"`, `compositionContract: "direct-response-composition-v2"`, `heroContract: "stacked-vsl-hero-v2"`, `heroLayout: "stacked-vsl"`, `heroTemplate: "offeros-stacked-vsl-v2"`, `heroVideoFrame: "large-16x9"`, `heroVideoProminenceChecked: true`, `offerStackContract: "direct-response-buy-box-v1"`, `pageKit: "offeros-page-kit-v1"`, `pageKitBuilder: "offeros-page-kit-builder-v1"`, `pageKitArchetype`, `themePreset`, `pageKitBlueprintUsed: true`, `themeTokensUsed: true`, `navigationPolicy: "no-section-nav"`, `iconSystem: "lucide-icons-v1"`, `iconLibrary: "lucide"`, `imageDisplay: "viewport-constrained-v1"`, `eyebrowPolicy: "sparse-key-signposts-v1"`, `eyebrowAlignment: "centered-with-section-heading"`, `vslSectionCommand: "overview-not-watch-first"`, `checkoutTarget: "#checkout"`, `vslPlacement: "main-column-stacked"`, and `orderFormIncluded: false`.

Stop conditions:

- If `copy.md` does not contain `# Section Blueprint` with rows for every required section, revise before page or visual planning.
- If `sales-page-blueprint.json`, `theme.json`, or `quality.salesPage` uses an unapproved Page Kit archetype or theme preset, revise before building.
- If the page reads as `hero/features/price/FAQ`, revise before QA.
- If `index.html` has fewer than 2,500 visible words for `direct-response-long-form-vsl`, revise before QA.
- If the VSL section becomes a wall of text or exceeds 220 visible words, revise before QA.
- If the page contains a `<nav>` menu, sticky section navigation, or header section jump links, remove them before QA.
- If the post-hero VSL section says "Watch this first" when the hero already contains the primary VSL frame, revise the label and section framing before QA.
- If card grids, proof blocks, or offer-stack lists are plain boxes with no branded icon/checkmark treatment, revise before QA.
- If the page has no `data-lucide` icon markers, revise before QA.
- If section eyebrows/pills appear on every section, or more than 6 section eyebrows are visible by default, revise before QA.
- If any visible section eyebrow/pill is not centered with the H2 it precedes, revise before QA.
- If any support/product/offer-stack visual is not marked `data-offeros-image-display="constrained"`, renders as an unconstrained full-size image, or sits in a visibly larger colored matte/frame because the frame and source aspect ratios do not match, revise before QA.
- If any normal paragraph exceeds 55 words, revise before QA.
- If any required direct-response section has fewer than the minimum buyer-facing words, revise before QA.
- If required comparison/card sections contain blank-looking cells or empty cards, revise before QA.
- If `index.html` was not created by `scripts/build_sales_page.py` or lacks `data-offeros-page-kit="v1"`, `data-offeros-builder="offeros-page-kit-builder-v1"`, and `data-offeros-vsl-placement="main-column-stacked"`, rebuild through the Page Kit builder.
- If the hero does not use the locked `offeros-stacked-vsl-v2` Page Kit shell, revise before QA.
- If the hero uses a two-column/split-grid layout, product/dashboard mockup hero art, or puts the VSL as a small right-side thumbnail/card, revise before QA.
- If the hero does not include the large 16:9 VSL frame, thumbnail, play button, caption, price strip, CTA to `#checkout`, and trust row in that stacked order, revise before QA.
- If the page contains an embedded checkout, order form, payment fields, or credit-card form, remove it and link CTAs to `#checkout`.
- If proof/demo appears only after the offer stack or pricing, revise before QA.
- If the offer stack is only cards or a pricing panel instead of the buy-box checklist stack, revise before QA.
- If any sentence appears 4+ times in buyer-facing page copy, revise before QA.

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
6. Create `workbook/workbook-blueprint.json` and `workbook/workbook-content.json` before rendering.
7. Create inspectable HTML source at `output/pdf/[slug]-workbook.html`.
8. Render the customer PDF through Gotenberg/Chromium by default: `GOTENBERG_URL=http://localhost:3000`, endpoint `/forms/chromium/convert/html`. If Gotenberg is unavailable in deep mode, mark the PDF `needs_revision` and record the blocker; do not silently downgrade to a weak renderer.
9. Create the customer PDF under `output/pdf/[slug]-workbook.pdf`.
10. For offers up to $29, the product must have at least:
   - 22 pages
   - 3,500 extracted words unless the user explicitly approved a highly visual workbook
   - 8 buyer-action surfaces
   - 8 named buyer tools/templates
   - 2 completed examples and matching blank templates for core tools
11. For $30-$99 offers, the product must have at least:
   - 25 pages
   - 4,000 extracted words unless the user explicitly approved a highly visual workbook
   - 8 buyer-action surfaces
   - 10 named buyer tools/templates
   - 3 completed examples and matching blank templates for core tools
12. Use buyer-action surfaces: audits, calculators, cards, examples, worksheets, templates, scripts, checklists, implementation plans, and debriefs.
13. Render representative pages from the actual final PDF to `output/pdf/render-check/`. Synthetic QA preview images do not count.
14. Set `quality.pdf.pageCount`, `actionSurfaceCount`, `namedToolCount`, `pageArchetypeCount`, `maxPageArchetypeShare`, `completedExampleCount`, `blankTemplateCount`, `visualAssetCount`, `pdfSpecificVisualAssetCount`, `genericActionSurfaceLabelsRemoved`, `hasCompletedExamples`, `hasBlankTemplates`, `renderBackend`, `sourceHtmlPath`, `renderQaPath`, `renderedPageImageCount`, `actualPdfRenderChecked`, `pageArchetypeAudit`, and `renderChecked` from the generated artifact, not from memory.

Stop conditions:

- If the PDF is mostly repeated explanation plus blank lines, rebuild it as a toolkit/workbook.
- If most pages reuse the same heading/body/"worksheet box" layout, rebuild with distinct page archetypes.
- If the phrase "Action Surface" appears as repeated buyer-facing page furniture, rebuild with named tools/templates.
- If the PDF has page count but lacks named tools, completed examples, and matching blank templates, rebuild before QA.
- If `quality.pdf.visualAssetCount` is below 6 or `quality.pdf.pdfSpecificVisualAssetCount` is below 4, create PDF-specific visuals/treatments and rebuild.
- If `quality.pdf.renderBackend` is not `gotenberg-chromium`, revise the PDF build path.
- If `quality.pdf.actualPdfRenderChecked` is not true or `renderedPageImageCount` is missing, run actual PDF page render QA before handoff.
- If extracted text is below the price-point target, revise before QA.
- If page count or QA notes disagree with the actual PDF, revise before handoff.

## Email Sequence Recipe

Use this recipe for every launch or sales email artifact.

1. Choose a sequence framework from `references/email-frameworks.md`.
2. Create `email-sequence.json` as the canonical source before rendering Markdown/HTML.
3. For a complete launch sequence, create at least 7 emails.
4. Every email must include:
   - send timing
   - subject line
   - preview text
   - campaign role
   - conversion job
   - belief shift
   - primary objection
   - body copy
   - CTA
5. Each email must have a distinct conversion job. Do not paste the same product paragraph into every email.
6. Use objection progression: false belief, cost of belief, new insight, proof or demonstration, offer reveal, risk reversal, urgency or final close.
7. Render only through Email Launch Studio (`scripts/build_email_sequence.py`) and record `quality.emails.studio: "email-launch-studio-v1"`.

Stop conditions:

- If the email artifact lacks send timing, preview text, or campaign role, revise before QA.
- If `email-sequence.json` is missing, revise before rendering.
- If customer-facing email copy exposes internal campaign labels as headings, revise before QA.
- If two or more body blocks repeat verbatim, revise before QA.

## VSL Deck Recipe

Use this recipe for every VSL deck.

1. Create `presentation/vsl-deck-plan.json` as the canonical source before generating the PPTX.
2. Create `output/presentation/[slug]-vsl.pptx` as the primary deck. Do not create HTML first.
3. Create a slide plan with 20-30 slides before generating the PPTX.
4. Assign every slide one of at least 8 layout names before generating the PPTX:
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
5. Layout family means structural composition, not color, icon, or background variation. A two-column copy/visual slide remains the same layout family even when colors, icons, headings, or placeholder labels change.
6. No layout family may be used on more than 35% of slides.
7. Write a slide-numbered layout audit before registering the deck. Record it in `quality.vsl.layoutAudit` as an array with `slide`, `layoutFamily`, and `visualAsset` for every slide.
8. Visible slide copy must be buyer-facing. Do not put `Hook`, `Problem`, `Agitate`, `Market`, `Mechanism`, `Proof`, `Offer`, `CTA`, `Objection`, `Close`, `Stage: Problem`, `Problem:`, or similar internal labels anywhere on a slide, including badges, footers, eyebrows, and small captions.
9. Speaker notes must be recording notes of at least 25 words per slide. Do not use notes such as `Explain mechanism`, `Show proof`, or `Agitate`.
10. Key slides must include visuals, diagrams, generated frames, screenshots, or product previews. Do not use dark placeholder rectangles with labels as finished visuals.
11. Read `visual-asset-plan.md` and fulfill the `## VSL Deck Visuals` section before generating the PPTX:
   - 12+ unique visual assets or clearly distinct diagram treatments across a 20-30 slide deck.
   - 8+ VSL visuals/treatments must be specific to the VSL deck and not reused from the sales page.
   - No single non-logo bitmap may appear on more than 25% of slides.
   - Do not recycle the same 3 hero/product images across the deck. A repeated theme is allowed; repeated bitmap filler is not.
   - Product bundle imagery may appear on product reveal, offer stack, value, and CTA slides only.
   - Every slide must have a specific visual job: pattern interrupt, comparison, map, matrix, mechanism diagram, example, proof substitute, product view, objection card, price/value contrast, or close.
12. Every bitmap image added to the PPTX must preserve aspect ratio. Do not call `slide.addImage({ path, x, y, w, h })` for a visual box unless the image's source ratio exactly matches that box. Use a local helper and route every VSL image through it:

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

13. Create HTML/contact-sheet only after the PPTX exists. Save it as `output/presentation/vsl-contact-sheet.png` or `output/presentation/vsl-preview.html`.
14. Register `vsl-deck` as the `.pptx`; set its `preview` to browser-safe `output/presentation/vsl-preview.html` or an image contact sheet, never to the `.pptx` itself.
15. Set `quality.vsl.studio: "vsl-deck-studio-v1"`, `backend: "pptxgenjs"`, `sourcePlanPath`, `editableTextChecked`, `maxLayoutShare`, `notesAreNarration`, `visibleStageLabelsRemoved`, `layoutDiversityChecked`, `visualPlaceholdersRemoved`, `visualAssetCount`, `uniqueVisualAssetCount`, `vslSpecificVisualAssetCount`, `maxRepeatedBitmapShare`, `visualReuseChecked`, and `layoutAudit`.
16. Browser-test `output/presentation/vsl-preview.html` at desktop and about 390px mobile width. The build must fail if the preview has horizontal overflow or broken images.

Stop conditions:

- If the primary deck is HTML, stop and rebuild as PPTX.
- If `presentation/vsl-deck-plan.json` is missing, stop and write the slide plan source first.
- If the deck was not built through `pptxgenjs` or the Presentations plugin with the same quality contract, stop and rebuild.
- If `quality.vsl.editableTextChecked` is not true, stop and inspect the PPTX for flattened-image-only output.
- If stage labels are visible as slide titles, revise before QA.
- If one layout dominates the deck, revise before QA.
- If the same large bitmap appears on more than 25% of slides, revise the visual plan before QA.
- If the deck uses fewer than 12 unique visual assets/treatments or fewer than 8 VSL-specific visuals/treatments, revise before QA.
- If notes are author labels instead of narration, revise before QA.
- If any PPTX bitmap appears in a box with a different aspect ratio and no PowerPoint `sizing`/crop metadata, revise the generator before QA.
- If the dashboard iframe preview points at the `.pptx`, revise manifest preview metadata before QA.
