# Copy Plan Contract

`copy-plan.json` is the canonical Copy Studio source. Codex authors it; `scripts/build_copy.py` validates and renders it into clean written `copy.md`, internal `copy-blueprint.md`, and `sales-page-blueprint.json`.

`copy.md` is the actual long-form sales copy shown in the delivery dashboard and rendered by the sales page. It must read like written sales copy, not a framework document, schema dump, or planning table.

`copy.md` must use exact page-copy section markers:

```text
[hero]
...
[/hero]

[mechanism]
...
[/mechanism]
```

The bracket markers are structural only. `scripts/build_sales_page.py` converts them to HTML comments such as `<!-- [hero] -->` and renders the contained buyer-facing text exactly. The page builder must not summarize, rewrite, delete, slice, or replace this copy with generic section cards.

`copy-blueprint.md` keeps the internal section blueprint, framework metadata, and copy-rendering map. Do not put those tables in `copy.md`.

`sectionPlan[].copyBlocks` are the finished copy source. They are not outline bullets, strategy notes, or section instructions. The builder renders bracketed `copy.md` from them and fails if they are thin or meta.

Required metadata:

- `schema: "offeros/copy-plan/v1"`
- `framework: "modern-brunson-long-form-v1"`
- `standaloneCopyRequired: true`
- `vslDependency: "optional-supporting-asset"`

Required commercial fields:

- offer name, price, audience, awareness level, market sophistication
- core promise and primary pain
- 3+ failed alternatives with why each fails and what is needed instead
- new insight / epiphany
- named unique mechanism with 3+ steps
- proof plan with proof before offer
- structured product reveal
- offer stack with 8+ value-explained deliverables
- value logic, guarantee, 7+ objections, and real urgency basis

Each `sectionPlan` row must include:

- `sectionId`
- `frameworkRole`
- `conversionJob`
- `buyerBeliefBefore`
- `buyerBeliefAfter`
- `primaryClaim`
- `proofOrSupport`
- `copyBlocks`
- `visualNeed`
- `ctaRole`
- `maxWords`

The section plan must include: `hero`, `vsl`, `problem`, `agitation`, `failed-alternatives`, `new-insight`, `mechanism`, `proof`, `before-after`, `product`, `feature-benefit`, `how-it-works`, `offer-stack`, `bonuses`, `pricing`, `guarantee`, `fit`, `faq`, and `final-cta`.

Depth contract:

- `copyBlocks` must contain 1,800+ buyer-facing words across the plan before rendering.
- Rendered `copy.md` must contain 2,500+ customer-facing words, target 3,500-5,500.
- Major sections must have real body copy, not only a headline or one sentence.
- Product reveal must include feature-benefit-reason bullets for all core components.
- FAQ must include 7+ specific objections with belief-shifting answers.
- Copy must not include internal phrases such as "this section explains", "conversion job", "belief shift", "visual need", or "copy anchor".
