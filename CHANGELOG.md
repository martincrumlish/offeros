# Changelog

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
