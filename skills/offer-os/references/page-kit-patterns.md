# Page Kit Patterns

Use these patterns when translating intake into the sales page blueprint and built page.

## Stacked VSL Hero

The hero is a centered vertical stack, not a split product hero:

1. Buyer filter, prehead, headline, and benefit lead.
2. Large 16:9 VSL frame with thumbnail, play control, and caption.
3. Price strip with value context and primary CTA.
4. Trust row with three or more concrete reassurances.

Do not use two-column, split-screen, dashboard mockup, product mockup, or SaaS feature hero layouts for the default page kit.

## Long-Form Header

The header is not a website navigation system. Use logo/brand and, at most, one primary CTA. Do not add sticky/hover nav bars, section jump links, or menus that encourage skipping the sales argument.

## Section Blocks

Required sections carry the persuasion arc. Optional blocks may deepen a section, but cannot replace it. Valid optional choices are founder note, case study, demo screens, comparison table, bonus stack, use cases, implementation roadmap, risk-reversal callout, testimonial strip, and technical requirements.

Place proof before the offer stack. Place fit/not-fit before or near pricing. Keep the VSL setup short and make long explanations scannable with tables, checklists, and callouts.

Use restrained eyebrow/prehead labels, wider centered H2s for major sections, and enough vertical space for the argument to breathe. Card grids and checklist stacks need branded icon or checkmark treatments; plain boxes with text are not enough. Sales-page images must use constrained display frames so support visuals and bundles do not dominate the viewport.

## No Order Form

A page kit sells the click; it does not collect payment details. Use CTA links to `#checkout` by default or to the supplied checkout URL. Disallow `order-form`, `embedded-checkout`, `payment-fields`, and `credit-card-form` blocks in both blueprint and generated markup.

## Theme Pattern

Theme files should be portable across offers: brand name/logo, color tokens, type families, layout density, and named assets. Primary conversion visuals such as hero VSL thumbnails and product bundles need honest provenance and should be `imagegen-final` unless supplied or licensed. `imagegen-composite` qualifies only when imagegen performed the reference-image composition; local script/PIL/canvas/HTML/CSS composition does not qualify.
