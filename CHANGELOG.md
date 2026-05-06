# Changelog

## 0.3.0

- Hardens generated-design runs so the primary logo must be an imagegen bitmap, not a generated SVG fallback.
- Requires deep OfferOS runs to use generator-first builds and treat validator warnings as failures.
- Adds stricter PDF product, launch email, dashboard, VSL deck, and QA metadata checks.
- Requires VSL decks to be editable PPTX artifacts, not HTML contact sheets.
- Adds PPTX image aspect-ratio validation so deck images cannot be stretched into arbitrary boxes.
- Adds the direct-response hero and buy-box offer-stack contracts for long-form sales pages.

## 0.2.0

- Initial distributable plugin shape with OfferOS skill, templates, references, dashboard generator, artifact registry, and output validator.
