# Design Resolver

Resolve design direction before page or asset production.

## Supported Inputs

- Existing `design.md`
- URL reference
- Uploaded screenshots
- Generated design archetype
- Hybrid instructions

## Source Priority

1. Explicit user instruction
2. Existing `design.md`
3. Uploaded screenshots
4. URL-derived design
5. Generated archetype
6. Model judgment

If following the priority creates an incoherent result, state the tradeoff briefly and choose the practical path.

## Existing design.md

If `design.md` exists, read it and treat it as the source of truth unless the user overrides it.

## URL Reference

If the user provides a URL, inspect the page and extract production traits:

- page structure
- layout density
- color palette
- typography feel
- button treatment
- cards/panels/forms
- image style
- motion style
- conversion layout patterns

Create a new `design.md` from the reference before building.

Do not clone protected logos, exact brand identity, proprietary illustrations, or copyrighted assets unless the user owns them.

## Screenshots

Use screenshots as concrete visual evidence. Prefer screenshot evidence over vague style words unless the user says the screenshot is only inspirational.

## Generated Archetype

If no design source exists, generate an archetype from:

- offer category
- audience sophistication
- price point
- trust requirement
- emotional tone
- delivery format

A generated archetype is not the same thing as generated imagery. If the final offer needs hero/product/ad visuals, use imagegen for those bitmap assets or record a fallback reason. Put expected image prompts and provenance notes in `design.md`.

Useful archetypes:

- premium expert offer
- tactical toolkit
- creator/coach offer
- SaaS-style operational product
- bold direct-response launch
- minimalist editorial
- dark VSL funnel
- clean workshop/bootcamp

## Output Standard

The resolved `design.md` should include:

- brand feel
- color palette
- typography direction
- layout rules
- component treatment
- image/graphic style
- imagegen prompt direction and fallback rules
- icon style
- motion style
- do/do-not notes

Keep it practical enough for another agent to build from without interpretation.
