# Agent Dispatch

Use subagents only when the user explicitly allows delegation or asks to dispatch agents.

## Dispatch Principles

- Delegate bounded sidecar tasks.
- Keep immediate blocking work local.
- Avoid duplicate work.
- Give clear ownership.
- Ask workers not to revert or overwrite others' work.
- Integrate and QA in the main agent.

## Suggested Splits

### Strategy Agent

Owns market diagnosis, offer architecture, objections, mechanism, and positioning.

### Copy Agent

Owns sales copy, ad copy, email copy, and VSL narrative.

### Visual Agent

Owns design resolver, image prompts, asset sequencing, and visual QA notes.

### Imagegen Visual Workers

Use these workers only after the initial offer architecture, `design.md`, final logo lockup, `assets/logo.png`, `copy-plan.json`, rendered `copy.md` with the sales-page section blueprint, and `visual-asset-plan.md` v2 exist. At that point the workers have enough content anchors to create coherent visuals instead of inventing separate styles.

Dispatch them in parallel when the user has allowed agents and the run needs a full visual asset set:

- **Page visual worker**: owns `assets/page/` or equivalent sales-page visuals from the `## Sales Page Visuals` plan. It must use the `copyAnchor`, `visualKind`, conversion job, aspect ratio, and text rule for each row.
- **PDF visual worker**: owns `output/pdf/assets/` or equivalent PDF-only visuals/treatments from PDF page archetypes: cover, module dividers, matrices, completed examples, blank templates, checklist/implementation visuals.
- **VSL visual worker**: owns `output/presentation/assets/` or equivalent slide visuals from the slide plan: pattern interrupt, problem map, failed alternatives, mechanism diagram, product reveal, stack, price/value, guarantee, objection, final CTA.
- **Ad visual worker**: owns `assets/ads/` or equivalent ad-specific imagegen creatives from the ad angle map. It must not crop sales-page images and call them ads.

Give every visual worker the same source references:

- `offer-architecture.md`
- `design.md`
- `copy-plan.json`
- `copy.md`
- `visual-asset-plan.md`
- frozen final `assets/logo.png` only
- product outline/module list and PDF page archetypes
- VSL slide plan
- ad angle map
- required output paths from the plan

Tell every worker:

- you are not alone in the codebase; do not revert or overwrite others' files
- write only inside your assigned output folder and update only the visual rows you own if asked to edit `visual-asset-plan.md`
- use the `imagegen` skill/tool for bitmap visuals when available
- for primary conversion visuals, produce the final buyer-facing image with imagegen and record `source/provenance: imagegen-final`, `finalPixelsGeneratedBy: imagegen`, `localCreativeOverlay: false`, and `localPostprocess` limited to crop, resize, compression, or format-conversion
- use `imagegen-composite` only when imagegen performed the reference-image composition; local PIL/canvas/HTML/CSS/script composition does not qualify
- preserve the design system: palette, typography cues, image treatment, logo style, density, and texture rules
- if a visual needs the logo visible, pass `assets/logo.png` as the only logo reference image to imagegen and instruct it to use the supplied logo exactly
- do not invent, redesign, recolor, redraw, reinterpret, replace, or substitute the logo/wordmark
- do not use any other logo image, old attempt, sketch, or alternative mark as a reference
- do not add logo, headline text, labels, UI cards, badges, mockups, overlays, or product-stack composition locally after imagegen; if the creative is wrong, regenerate or edit with imagegen
- follow `salesPageImageSystem: mixed-direct-response-v1` unless the user explicitly requested another image system
- use mockup-style visuals mainly for product reveal, offer stack, dashboard preview, and CTA bundle sections
- use diagrams, comparisons, proof/demo visuals, structured panels, screenshots, or restrained buyer-situation imagery for mechanism, failed alternatives, proof, objections, and feature specifics
- include generation prompts and provenance notes beside the output assets when practical
- return changed file paths and any assets that need parent integration

Imagegen prompt structure for workers:

```text
Use case: [sales-page|pdf-product|vsl-deck|ad-creative]
Offer: [exact offer name]
Audience: [specific buyer]
Artifact target: [page/PDF/VSL/ad and section or slide/page]
visualKind: [approved visualKind from visual-asset-plan.md]
copyAnchor: [data-offeros-section or PDF/VSL/ad anchor]
Visual job: [belief/action the visual must support]
conversionJob: [conversion job from copy-plan.json/copy.md/slide plan/ad angle]
Style references: design.md rules, frozen assets/logo.png only, color palette, product mockup direction
Composition: [specific layout, focal point, aspect ratio]
Text rule: [no text | large exact text only | labels from plan only]
Logo rule: if this visual needs a logo, use assets/logo.png as the exact supplied logo reference; do not invent, redesign, recolor, redraw, reinterpret, replace, or substitute it
Final-pixel rule: the final buyer-facing image must be produced by imagegen. Do not add local overlays, labels, badges, UI cards, mockups, product stacks, or logo placement after imagegen. Local processing may only crop, resize, compress, convert format, or perform non-creative QA fixes.
Required metadata: source/provenance=imagegen-final; finalPixelsGeneratedBy=imagegen; localCreativeOverlay=false; localPostprocess=[crop, resize, compression, format-conversion]
Must feel: [commercial, useful, direct-response, buyer-specific]
Avoid: alternate logos, old logo attempts, logo option sheets, generic stock look, unrelated metaphors, illegible text, fake UI unless requested, busy mockup filler, hallucinated dashboards, reusing sales-page image concepts as filler
Output: [exact file path]
```

The main agent owns integration: check visual consistency, register artifacts/provenance, wire files into PDF/VSL/page/ad builds, and run validation.

### Build Agent

Owns HTML/CSS pages, scripts, dashboard implementation, and manifest wiring.

### QA Agent

Owns broken links, missing files, PDF/deck/dashboard checks, mobile overflow, and placeholder scans.

## When Not To Dispatch

Do not dispatch if:

- the task is tiny
- the next step is blocked on the answer
- the output requires tight single-threaded judgment
- the user has not allowed agents
