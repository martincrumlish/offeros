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

- Up to $29: 22+ pages, 3,500+ extracted words, 4+ modules, 8+ buyer-action surfaces, 8+ named tools/templates.
- $30-$99: 25+ pages, 4,000+ extracted words, 5+ modules, 8+ buyer-action surfaces, 10+ named tools/templates.
- $100+: 35+ pages, 6,000+ extracted words, 6+ modules, 10+ buyer-action surfaces.

Buyer-action surfaces include worksheets, calculators, scorecards, scripts, swipe files, checklists, templates, station cards, planners, examples, implementation plans, and audits. At least one core tool should have both a filled example and a blank worksheet.

Deep-mode PDFs must also use distinct page archetypes. Use at least 7 archetypes such as cover, quick start, guide lesson, decision matrix, completed example, blank worksheet, checklist, script/swipe, audit/scoring, implementation plan, and resource index. No single archetype should account for more than 35% of pages.

Do not ship pages that repeat the same header/body/"Action Surface" box layout. Do not use "Action Surface" as repeated buyer-facing page furniture. Name the actual tool the buyer is using.

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
- named tools/templates are counted
- page archetype variety is counted
- no repeated generic "Action Surface" boxes or identical page layouts dominate the product

Use the PDF skill when rendering, inspecting, or layout-checking PDFs.
