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

Use these workers only after the initial offer architecture, `design.md`, selected logo concept, `assets/logo.png`, and `visual-asset-plan.md` exist. At that point the workers have enough references to create coherent visuals instead of inventing separate styles.

Dispatch them in parallel when the user has allowed agents and the run needs a full visual asset set:

- **Page visual worker**: owns `assets/page/` or equivalent sales-page visuals: hero/VSL thumbnail, mechanism/framework visual, before/after or failed-alternatives visual, proof/demo or stack visual.
- **PDF visual worker**: owns `output/pdf/assets/` or equivalent PDF-only visuals/treatments: cover, module dividers, matrices, completed examples, blank templates, checklist/implementation visuals.
- **VSL visual worker**: owns `output/presentation/assets/` or equivalent slide visuals: pattern interrupt, problem map, failed alternatives, mechanism diagram, product reveal, stack, price/value, guarantee, objection, final CTA.
- **Ad visual worker**: owns `assets/ads/` or equivalent ad-specific imagegen creatives. It must not crop sales-page images and call them ads.

Give every visual worker the same source references:

- `offer-architecture.md`
- `design.md`
- `visual-asset-plan.md`
- `assets/logo.png`
- `assets/logo-mark.png` if present
- product outline/module list
- required output paths from the plan

Tell every worker:

- you are not alone in the codebase; do not revert or overwrite others' files
- write only inside your assigned output folder and update only the visual rows you own if asked to edit `visual-asset-plan.md`
- use the `imagegen` skill/tool for bitmap visuals when available
- preserve the design system: palette, typography cues, image treatment, logo style, density, and texture rules
- include generation prompts and provenance notes beside the output assets when practical
- return changed file paths and any assets that need parent integration

Imagegen prompt structure for workers:

```text
Use case: [sales-page|pdf-product|vsl-deck|ad-creative]
Offer: [exact offer name]
Audience: [specific buyer]
Artifact target: [page/PDF/VSL/ad and section or slide/page]
Visual job: [belief/action the visual must support]
Style references: design.md rules, logo lockup, brand mark, color palette, product mockup direction
Composition: [specific layout, focal point, aspect ratio, text/no-text rule]
Must feel: [commercial, useful, direct-response, buyer-specific]
Avoid: generic stock look, unrelated metaphors, illegible text, fake UI unless requested, reusing sales-page image concepts as filler
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
