# Workshop Usage

OfferOS is for building complete commercial offer systems from a small brief. It should create the offer strategy, design direction, sales copy, sales page, PDF product, ads, emails, VSL deck, delivery dashboard, and QA notes.

Use it when you want Codex to turn an idea into a working offer package, not just brainstorm copy.

## Expected Setup

```text
workspace/
  .agents/plugins/marketplace.json
  plugins/offer-os/
```

A finished project usually contains:

```text
offer-os.json
offer-architecture.md
design.md
copy.md
index.html
emails.html
facebook-ads.html
delivery-dashboard.html
qa-notes.md
assets/
assets/ads/
output/pdf/
output/presentation/
output/playwright/
```

## Basic Prompt

```text
Use OfferOS in deep mode to build a complete offer from this idea.

Offer: [name]
Price: [price point]
Audience: [specific buyer]
Problem: [pain/desire]
Product: [what they get]
Promise: [result or transformation]
Tone/design preference: [optional]

Dispatch agents where useful.
```

OfferOS is designed to work from sparse input. The prompt should describe the offer, not repeat internal operating rules. Missing details should become explicit assumptions unless the gap materially changes the project.

## Design Source Prompts

Existing guide:

```text
Use OfferOS with the existing design.md in this workspace.
Build the full offer system for: [brief]
```

URL reference:

```text
Use OfferOS with this URL as the design reference: [URL].
Create the full offer system for: [brief]
```

Screenshots:

```text
Use OfferOS with the uploaded screenshots as visual reference.
Create design.md first, then build the full offer system.
```

## Modes

`deep` is the default and recommended workshop mode.

- `deep`: full strategy, assets, critique loops, visual QA, product PDF, VSL deck, dashboard.
- `standard`: complete but less exhaustive.
- `fast`: first-pass prototype only; not the final quality bar.

## If Output Is Too Shallow

Use:

```text
This OfferOS output is too shallow.
Run the deep quality gates. Strengthen the offer architecture, mechanism, proof logic, objections, examples, PDF product, ads, emails, VSL, and dashboard. Read the current files first, then update the weak outputs.
```

For thin product content:

```text
The PDF product feels too thin. Expand it into a customer-ready implementation guide with frameworks, checklists, examples, scripts, exercises, and action steps.
```

For weak design:

```text
Rewrite design.md into a practical production guide with colors, typography, layout rules, component treatment, image style, motion style, and do/do-not notes.
```

For weak logo output:

```text
The logo is a one-pass placeholder, icon-only mark, illustrative/page-curl/app-icon mark, rough text composite, SVG file, or non-imagegen bitmap. Re-run the Logo Gate: create 3 logo concepts, select one with rationale, use imagegen for 3 complete logo lockup candidates first, use a text-free symbol fallback only if exact text fails, reject illustrative marks, save assets/logo.png as a professional readable horizontal PNG/WebP logo lockup with the exact offer name, create output/qa/logo-lockup-preview.png, check small-size, one-color, typography, kerning, mark scale, and spacing, and record quality.logo metadata with `svgAssetCreated: false`.
```

For weak sales-page structure:

```text
The sales page is too short/product-page-like or reads as a wall of text. Load direct-response-framework.md, select direct-response-long-form-vsl, then rewrite copy.md with # Section Blueprint and rebuild index.html to include the full message match, hook/VSL, problem, agitation, failed alternatives, mechanism, proof/demo before the buy box, before/after, product reveal, offer stack, price, guarantee, objection, and close arc. Keep VSL setup short, paragraphs under 55 words, and use tables/callouts/checklists instead of generic essay sections.
```

For weak or random sales-page visuals:

```text
The sales-page visuals are too random, busy, or mockup-heavy. Rebuild the visual plan after copy.md: use visualPlanStage post-content-blueprint, anchor each sales-page visual to a real copyAnchor/data-offeros-section, use salesPageImageSystem mixed-direct-response-v1, keep mockups mainly for product reveal/offer stack/dashboard, and use diagrams, comparisons, proof/demo visuals, structured panels, screenshots, or restrained buyer-situation imagery for mechanism, failed alternatives, proof, objections, and feature specifics.
```

For weak PDF product:

```text
The PDF is not a paid workbook; it repeats the same page layout or generic Action Surface boxes. Rebuild it from the PDF Product Recipe: define named buyer tools/templates, add completed examples and matching blank versions, use 7+ page archetypes, raise the extracted word count to the price-point target, and render representative pages from every archetype.
```

For weak VSL output:

```text
The VSL deck is not presentation-ready. Rebuild the PPTX using vsl-deck-quality.md: remove visible stage labels, create at least 8 layout families, use 12+ unique visual assets/treatments, stop recycling the same few images, replace placeholder blocks with real visuals/diagrams/product previews, and make speaker notes usable narration.
```

For incomplete QA:

```text
Run an OfferOS QA pass. Check expected files, unresolved placeholders, broken links, rendering issues, missing previews, honest image provenance, PDF depth, VSL readiness, and consistency across the offer architecture, sales page, PDF, ads, emails, VSL, and dashboard.

Technical QA is not enough. Record commercial QA too: buyer value, usability, and trust for the sales page, PDF product, ads, emails, VSL deck, and delivery dashboard.
```

For structural misses:

```text
This OfferOS output drifted from the source templates.
Rebuild the sales page from page-skeleton.html with all required data-offeros-section markers, regenerate the dashboard with generate_delivery_dashboard.py and preserve the modal iframe template, and create vsl-deck as a PowerPoint PPTX with HTML only as vsl-preview.
```
