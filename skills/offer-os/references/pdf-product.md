# PDF Product

The PDF product is a core deliverable for full OfferOS runs. It must be complete enough to deliver to a paying customer.

## Required Contents

- cover page
- product title and promise
- quick-start instructions
- who it is for
- how to use it
- modules or chapters
- worksheets/checklists/templates
- examples or scripts
- completed examples and blank fill-in versions
- final implementation checklist
- resource index or next steps

Use concise practical language. Prefer decision tools, checklists, examples, scripts, tables, and worksheets over long explanation.

## Deep-Mode Depth Standard

Do not ship a thin PDF. In `deep` mode, the product should feel like the buyer's main deliverable, not a summary of the sales page.

Minimum paid-product targets:

- Up to $29: 18+ pages, 2,500+ extracted words, 4+ modules, 5+ buyer-action surfaces.
- $30-$99: 25+ pages, 4,000+ extracted words, 5+ modules, 8+ buyer-action surfaces.
- $100+: 35+ pages, 6,000+ extracted words, 6+ modules, 10+ buyer-action surfaces.

Buyer-action surfaces include worksheets, calculators, scorecards, scripts, swipe files, checklists, templates, station cards, planners, examples, implementation plans, and audits. At least one core tool should have both a filled example and a blank worksheet.

If the product genuinely needs fewer pages or fewer extracted words because it is intentionally visual, explicitly record the user-approved reason in the QA notes and commercial audit. Do not silently call a short or low-substance PDF complete.

## Product Types

Choose the format that matches the offer:

- toolkit
- workbook
- scorecard
- playbook
- checklist pack
- prompt bank
- implementation guide
- challenge workbook

## Output Files

Create:

- editable source file when useful (`.md`, `.html`, `.docx`, or equivalent)
- final `.pdf`
- supporting assets used by the PDF

Save final PDFs under `output/pdf/`.

## Validation

Verify:

- PDF opens
- pages render cleanly
- no clipped text
- no empty sections
- no placeholders/TODOs/internal notes
- content matches the offer promise
- buyer can act without extra explanation
- filename is delivery-ready
- page count and action-surface count meet the price-point depth target
- extracted text meets the price-point target unless the user approved a visual exception
- rendered screenshots or page images were inspected

Use the PDF skill when rendering, inspecting, or layout-checking PDFs.
