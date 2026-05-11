# Copy Studio Framework

Copy Studio is the source of truth for the sales argument. In deep mode, create `copy-plan.json` before clean `copy.md`, internal `copy-blueprint.md`, `sales-page-blueprint.json`, visual planning, or page generation.

Use `framework: "modern-brunson-long-form-v1"`.

The default page copy must stand alone even if the VSL is removed or replaced with a static image. Record `standaloneCopyRequired: true` and `vslDependency: "optional-supporting-asset"`.

`copy.md` is the actual written sales copy used for the delivery dashboard and the sales page. It must be rendered as bracketed page-copy sections (`[hero]...[/hero]`, `[problem]...[/problem]`, `[new-insight]...[/new-insight]`, etc.). `copy-blueprint.md` is the internal framework and section map. Do not put the `# Section Blueprint` table in `copy.md`.

The sales page builder renders the text inside `copy.md` sections exactly and converts the bracket markers to HTML comments. Do not let a page builder summarize the copy, rewrite it, remove sections, or collapse sections into repeated three-card layouts.

Before authoring `copy-plan.json`, load `references/copywriter-quality-bar.md`. After rendering `copy.md`, apply `references/copy-critic-rubric.md`. If `copy.md` is thin, repetitive, generic, meta, or VSL-dependent, revise `copy-plan.json` and rerun `scripts/build_copy.py` before visual planning or page generation.

## Modern Brunson Long-Form Spine

Use Hook, Story/Insight, Offer as the macro flow. Use PAS only inside sections; do not reduce the whole page to PAS.

Required spine:

1. Buyer filter / prehead
2. Big promise headline
3. Lead / core hook
4. Optional VSL or hero visual
5. Early CTA / price hint
6. Problem diagnosis
7. Cost of staying stuck
8. Failed alternatives
9. Epiphany / new insight
10. Unique mechanism
11. Proof or demonstration
12. Product reveal
13. Feature-benefit breakdown
14. How it works
15. Offer stack
16. Bonuses / accelerators
17. Price/value contrast
18. Guarantee
19. Fit / who it is for
20. FAQ / objections
21. Final close

## Non-Negotiables

- `sectionPlan[].copyBlocks` must contain finished buyer-facing sales copy, not notes for a later writer.
- Deep-mode `copy.md` must contain 2,500+ customer-facing words; the target range is 3,500-5,500.
- The page must include a specific epiphany/new insight before the mechanism.
- The unique mechanism must be named before proof and product reveal.
- Proof/demo must appear before price and offer stack.
- Product reveal must include feature-benefit-reason bullets.
- Offer stack items must explain why each deliverable matters.
- Fake urgency is forbidden. Urgency must come from a real launch window, cohort, expiring bonus, price change, or explicit user-provided reason.
- Do not continue to image planning, sales-page generation, PDF, VSL, email, ad, or dashboard work until the Copy Critic pass is clean.
