# Sales Page Types

Choose the page type before writing `copy.md` or `index.html`. A copy framework is not the same thing as a page type: the framework shapes persuasion logic, while the page type defines section depth, length, visuals, CTAs, and proof burden.

Record the selected type in `offer-os.json` under `quality.salesPage.pageType`. If no type is selected, the page is not complete.

## Default Rule

Use `direct-response-long-form-vsl` by default for complete OfferOS builds, low-ticket products, cold traffic, info products, toolkits, templates, workshops, and "internet marketing" style offers.

Use another type only when the user explicitly asks for a non-long-form page or the conversion action is not a paid front-end purchase. Record the reason in `quality.salesPage.pageTypeReason` and set `quality.salesPage.pageTypeOverrideUserRequested: true` only when the user explicitly requested the override.

## Types

### `direct-response-long-form-vsl`

Use for: cold traffic, low-ticket/front-end offers, new mechanisms, generated offers, VSL-first pages, and buyers who need belief shift before checkout.

Minimum structure:

- Header with logo, CTA, and minimal links.
- Hero built from the locked `offeros-stacked-vsl-v2` shell: centered buyer filter pill, prehead, specific headline, benefit lead, large 16:9 VSL/video frame below the headline, price strip below the VSL, CTA to `#checkout`, and trust row.
- VSL section below the hero that deepens the pitch; do not move the first VSL/video cue out of the hero.
- Problem diagnosis with at least 3 specific symptoms and hidden costs.
- Agitation section that shows the cost of delay or compounding pain.
- Failed alternatives with a table or contrast block.
- Unique mechanism with named framework, why it works, and why it is different.
- Proof, demonstration, or proof substitute before the main offer stack.
- Before/after section.
- Product reveal with product image/mockup.
- Offer stack buy box with product bundle image, big deliverable checklist, normally/today value row, large access CTA, and guarantee/instant-access reassurance. Cards can support this, but cannot replace it.
- Fit and not-fit filters.
- Pricing with value logic and what happens after purchase.
- Guarantee with terms and buyer responsibility.
- FAQ with at least 7 real objections.
- Final CTA that restates promise, price, and guarantee.

Depth targets:

- 16+ meaningful sections or subsections.
- 2,500+ visible page words for a paid complete offer.
- 3+ CTA placements after the hero.
- Hero contract `stacked-vsl-hero-v2` and offer stack contract `direct-response-buy-box-v1`.
- Framework `direct-response-long-form-v1`: message match, hook/VSL, problem, agitation, failed alternatives, mechanism, proof/demo, before/after, product, offer stack, guarantee, objections, close.
- Composition contract `direct-response-composition-v2`: separate problem/agitation/failed-alternatives sections, proof before offer stack, VSL setup under 220 words, normal paragraphs under 55 words, no non-FAQ/non-stack section above 500 words, and no blank-looking cards/tables.
- No repeated boilerplate sentences across offer-stack cards.

### `mechanism-led-product-page`

Use for: warmer traffic, products where the mechanism is already persuasive, buyers who mostly need clarity about what they get.

Minimum structure:

- Hero, mechanism, product walkthrough, examples, stack, proof, price, guarantee, FAQ, final CTA.
- 1,500+ visible page words.
- Product screenshots/mockups carry more weight than long agitation.

Do not use this for cold front-end offers unless there is strong pre-existing demand or proof.

### `proof-led-case-study-page`

Use for: offers with real case studies, client outcomes, or before/after evidence.

Minimum structure:

- Hero, case-study lead, before state, intervention/mechanism, after state, evidence, product bridge, stack, objections, price, guarantee, CTA.
- Proof must be concrete and caveated where needed.
- If proof is weak or synthetic, use `direct-response-long-form-vsl` instead.

### `webinar-workshop-registration`

Use for: live or recorded training registrations where the page action is opt-in, not purchase.

Minimum structure:

- Big training promise, host credibility, what they will learn, who should attend, agenda, bonuses, schedule/replay details, opt-in CTA, privacy/reassurance, FAQ.
- Do not use checkout/pricing sections unless the webinar itself is paid.

### `sales-letter-checkout`

Use for: text-forward offers, email-list traffic, or simple products where a classic written sales letter is better than a visual product page.

Minimum structure:

- Letter-style lead, problem, story or diagnosis, mechanism, product reveal, proof, stack, price, guarantee, FAQ, repeated order links.
- Design should support reading rather than decorative section hopping.

## Selection Notes

- Generated-design complete offers must start with `direct-response-long-form-vsl` unless the user explicitly requested a different page type.
- A "nice" brand page is not enough for a paid front-end offer.
- If the coded page looks like hero/features/price/FAQ, it fails deep mode even if the section markers exist.
- If the page type changes after copywriting, revise `copy.md`, not only the HTML.

## Required Metadata

Populate `quality.salesPage`:

```json
{
  "pageType": "direct-response-long-form-vsl",
    "pageTypeReason": "Cold front-end toolkit offer needs belief shift and VSL-first sales arc.",
    "requiredSectionContract": "direct-response-v1",
    "heroContract": "stacked-vsl-hero-v2",
    "heroLayout": "stacked-vsl",
    "heroTemplate": "offeros-stacked-vsl-v2",
    "heroVideoFrame": "large-16x9",
    "offerStackContract": "direct-response-buy-box-v1",
    "framework": "direct-response-long-form-v1",
    "compositionContract": "direct-response-composition-v2",
    "copyBlueprintPresent": true,
    "sectionMarkersPresent": true,
  "visibleWordCount": 3200,
  "objectionCount": 8,
  "ctaCount": 5,
  "postHeroCtaCount": 3,
  "offerStackItemsUnique": true,
  "sectionDepthChecked": true,
  "repeatedTextChecked": true
}
```
