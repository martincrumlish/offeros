# QA Checklist

Run final QA before marking a full OfferOS build complete. Separate technical QA from commercial QA.

## Offer Coherence

Check:

- promise is clear and specific
- audience is clear
- mechanism is explained
- deliverables match the sales promise
- price and scope are consistent
- objections are addressed
- CTA language is consistent
- sales page follows the required direct-response section contract
- sales page declares a page type from `references/sales-page-types.md`

## File Completeness

Check required outputs:

- `offer-os.json`
- offer architecture
- `design.md`
- logo
- sales copy
- sales page
- supporting graphics
- PDF product
- ad copy and images
- email sequence
- VSL deck
- delivery dashboard
- QA notes

## Visual QA

Check:

- sales page loads
- required `data-offeros-section` markers are present
- sales page follows the direct-response-long-form-v1 spine and proof/demo appears before the main offer stack
- sales page declares `data-offeros-page-kit="v1"`, `data-offeros-builder="offeros-page-kit-builder-v1"`, and `data-offeros-vsl-placement="main-column-stacked"`
- direct-response hero has `data-offeros-hero-layout="stacked-vsl"`, centered copy stack, large centered `data-offeros-hero-video`, `data-offeros-price-strip` below it, CTA to `#checkout`, and `data-offeros-trust-row`; it is not a two-column/split SaaS hero
- offer stack uses `id="checkout"` or `data-offeros-buy-section`, `data-offeros-product-bundle`, `data-offeros-offer-checklist`, `data-offeros-value-row`, `data-offeros-stack-cta`, and `data-offeros-access-copy`
- no broken images
- no mobile horizontal overflow
- text is readable
- buttons are consistent
- logo is not a placeholder, icon-only mark, illustrative/page-curl/app-icon mark, or rough text composite; exactly one final imagegen logo lockup was created, it includes the exact readable offer name, professional wordmark typography/kerning checks, small-size check, one-color check, and bitmap lockup preview are recorded
- logo is frozen as `assets/logo.png`; no alternate logo options were created, and later imagegen prompts that need branding use `assets/logo.png` as the exact supplied logo reference
- generated graphics fit their containers
- image provenance is recorded honestly
- no SVG files were created or registered as generated visual artifacts
- no Pillow/PIL-authored image artifacts were created or registered; CSS/code/screenshot fallbacks are not mislabeled as imagegen outputs
- `visual-asset-plan.md` exists after the copy blueprint, records `visualPlanStage: post-content-blueprint`, uses `salesPageImageSystem: mixed-direct-response-v1`, and splits visuals by sales page, PDF, VSL, ads, and dashboard
- sales-page visuals have `visualKind`, `copyAnchor`, `conversionJob`, `artifactTarget`, `aspectRatio`, and `textRule`, are not all mockup-style unless the user requested that, and primary creative slots are `imagegen-final` or provided/licensed rather than PIL/HTML/CSS/generated-by-code placeholders or local composites
- primary conversion image artifacts record `finalPixelsGeneratedBy: imagegen`, `localCreativeOverlay: false`, and `localPostprocess` limited to crop, resize, compression, or format conversion
- PDF and VSL visuals are not only reused sales-page images
- dashboard previews work
- dashboard uses the standard v2 modal/iframe template
- VSL preview loads at desktop and mobile widths with no horizontal overflow
- browser QA results in `qa-notes.md` do not contain `overflowX: true` or broken image entries

## PDF QA

Check:

- PDF opens
- pages render cleanly
- no clipped text
- no missing images
- no placeholders/TODOs
- product is actionable
- page count meets the price-point depth target or the exception is justified
- extracted text meets the price-point depth target unless the user explicitly approved a highly visual workbook
- action surfaces are present: worksheets, templates, examples, checklists, scripts, planners, or scorecards
- completed examples and blank buyer-fillable templates exist for the core tool
- buyer-action pages use named tools/templates instead of repeated "Action Surface" boxes
- page archetypes vary across the guide/workbook; the PDF is not one repeated page layout
- PDF has 6+ visuals/treatments, including 4+ PDF-specific visuals/treatments
- rendered pages/screenshots were inspected visually

## Deck QA

Check:

- deck opens
- primary VSL deck is `.pptx`
- slide count matches intended VSL length
- PPTX images preserve aspect ratio; no bitmap is stretched or compressed into a mismatched box
- slides have restrained text
- brand visuals are consistent
- browser-safe preview exists for dashboard
- dashboard card uses browser-safe preview for the PPTX and the open action points to the actual `.pptx`
- deck is presentation-ready, not just a contact-sheet grid
- deck uses varied layouts; no single layout family dominates
- deck uses 12+ unique visual assets/treatments and does not repeat the same few large images as filler
- deck uses 8+ VSL-specific visuals/treatments instead of only sales-page imagery
- visible slide copy is buyer-facing everywhere, with no internal labels such as "Agitate", "Stage: Problem", or "CTA"
- speaker notes are usable narration guidance, not author reminders
- placeholder visual blocks were replaced or clearly recorded as drafts
- deck includes offer reveal, stack, price, guarantee, objections, and final CTA

## Commercial QA

Score each major artifact from 1-5:

- buyer value
- usability
- trust

Major artifacts:

- sales page
- PDF product
- ad copy and images
- email sequence
- VSL deck
- delivery dashboard

Any score below 4 is a blocking issue unless the final response clearly labels the artifact as a draft or limitation.

Validator warnings are also blocking in deep mode. Do not hand off a complete offer with warning count above zero.

## Email QA

Check:

- 7+ emails for a complete launch sequence
- each email has send timing, subject line, preview text, campaign role, body copy, and CTA
- each email has a distinct conversion job
- no repeated product paragraph is pasted across the sequence
- objections progress logically from belief shift through offer and risk reversal

## Metadata QA

Check:

- `qa-notes.md` page counts match the actual PDF and `quality.pdf.pageCount`
- `quality.salesPage.ctaCount` matches inspected CTA markers
- artifact preview paths exist
- `vsl-deck.preview` is not the `.pptx`
- image provenance matches actual asset source

## Final Response

Report:

- what was created
- what was validated
- technical QA status and commercial QA status
- what could not be validated
- where the user should start
