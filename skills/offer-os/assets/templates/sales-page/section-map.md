# Sales Page Section Map

Use this as the required direct-response sales-page contract for complete OfferOS runs. Adapt copy, layout density, and theme to the offer, but do not remove the conversion jobs or reinvent the sequence.

Before writing copy or HTML, choose a page type from `references/sales-page-types.md`. The default for complete front-end offers is `direct-response-long-form-vsl`; other types still use these markers but vary depth and emphasis.

Each section must include `data-offeros-section="<id>"` so QA can validate structure.

| Section | ID | Conversion Job | Required Content | Visual/Asset |
| --- | --- | --- | --- | --- |
| Header | `header` | Establish brand and orientation | Logo, minimal links if needed | Logo |
| Hero | `hero` | Create immediate desire and buying momentum | Centered buyer filter pill, prehead, specific headline, benefit lead, large stacked VSL/video frame, price strip, CTA to `#checkout`, trust row | Large hero VSL thumbnail/video frame |
| VSL | `vsl` | Deepen the pitch after the hero | VSL thumbnail/preview, play CTA, short promise, bridge from hero | VSL thumbnail |
| Problem Diagnosis | `problem` | Make the buyer feel understood | Specific pain, hidden cost, current state | Problem visual |
| Agitation | `agitation` | Make inaction feel expensive | Cost of delay, compounding consequence, emotional frustration, business/operational drag | Cost-of-delay graphic or callout |
| Failed Alternatives | `failed-alternatives` | Invalidate what they already tried | Common fixes and why they fail | Comparison table |
| Unique Mechanism | `mechanism` | Install the new belief | Mechanism name, explanation, why it works | Framework diagram |
| Proof/Credibility | `proof` | Reduce trust gap before price | Case study, founder credibility, examples, screenshots, proof substitute, or demo | Proof/demo block |
| Before/After | `before-after` | Make value concrete | Weak current state vs desired state | Before/after graphic |
| Product Reveal | `product` | Show what they get | Product name, promise, modules | Bundle mockup |
| Offer Stack | `offer-stack` | Build value and close the purchase decision | Product bundle image, big deliverable checklist, normally/today value row, large access CTA, guarantee/instant-access reassurance | Bundle mockup plus checklist |
| Who It Is For | `fit` | Filter buyers | Fit and disqualifiers | Checklist |
| Pricing | `pricing` | Clarify the buying decision | Price, payment note, what happens after purchase | Pricing panel |
| Guarantee | `guarantee` | Reduce risk | Guarantee, terms, reassurance | Guarantee badge |
| FAQ | `faq` | Handle objections | Price, time, fit, trust, implementation | Accordion |
| Final CTA | `final-cta` | Convert | Offer recap, price, CTA, guarantee | CTA block |

Every section must have a sales job. Remove decorative sections that do not create belief, desire, trust, or action.

## Structure Gate

Do not ship a short branded product page as the sales page. Deep-mode pages must follow the internet-marketing/direct-response arc:

1. Big promise and VSL.
2. Problem diagnosis.
3. Agitation and cost of status quo.
4. Failed alternatives.
5. Unique mechanism.
6. Proof or proof substitute before the buy box.
7. Product reveal and stack.
8. Price, value, guarantee.
9. Objection handling.
10. Final CTA.

For `direct-response-long-form-vsl`, section markers alone are not enough. The page must have enough copy, specificity, proof/demo, objection handling, and repeated CTA momentum to plausibly sell the offer to a cold buyer.

The hero and offer stack must use the manual direct-response structure. Do not replace them with a branded hero, feature grid, pricing card, generic card stack, or two-column SaaS hero.

Required hero contract:

- Use the locked hero shell from `assets/templates/sales-page/page-skeleton.html`. Do not write a new hero from scratch.
- `data-offeros-section="hero"` must also include `data-offeros-hero-layout="stacked-vsl"`, `data-offeros-hero-contract="stacked-vsl-hero-v2"`, and `data-offeros-template="offeros-stacked-vsl-v2"`.
- Keep the hero section classes `oo-hero oo-hero-stacked-vsl`, the wrapper marked `data-offeros-hero-inner`, and the critical inline CSS for `.oo-hero`, `.oo-hero-inner`, `.oo-hero-copy-stack`, `.oo-vsl-frame`, `.oo-price-strip`, and `.oo-trust-row`.
- The hero must stack vertically in this order: buyer filter/prehead/H1/benefit lead, then large VSL/video frame, then price strip/CTA, then trust row.
- The hero copy stack must be centered and marked `data-offeros-hero-copy-stack`.
- The VSL/video frame must be centered below the headline, visually dominant, and marked `data-offeros-hero-video`, `data-offeros-hero-video-prominence="primary"`, and `data-offeros-hero-video-size="large"`.
- The hero video frame must use the `.oo-vsl-frame` 16:9 frame, include a real thumbnail marked `data-offeros-video-thumbnail`, a visible play button marked `data-offeros-video-play`, and a short caption marked `data-offeros-video-caption`. Do not fake the VSL with a small UI card, checklist panel, dashboard mockup, or decorative product screen.
- The price strip must sit below the VSL/video frame, show the actual price, normal/total value or value context, a short stack summary, and the primary CTA.
- The trust row must sit below the price/CTA area and include 3+ concrete trust bullets such as guarantee, instant access, reuse rights, support, or low-risk use.
- Do not use two-column, side-by-side, split-screen, `hero-grid`, `hero-split`, `hero-visual`, `hero-mockup`, dashboard/product mockup hero art, or SaaS product hero layouts for `direct-response-long-form-vsl`.
- A light SaaS aesthetic may change colors and surface polish, but it must keep the direct-response stacked VSL shell. It must not become a light SaaS landing-page hero.

Required direct-response order:

`hero -> vsl -> problem -> agitation -> failed-alternatives -> mechanism -> proof -> before-after -> product -> offer-stack -> fit -> pricing -> guarantee -> faq -> final-cta`

Proof/demo must appear before the main offer stack. Do not ask for the sale before the page has installed the mechanism and provided proof, proof substitute, or demonstration.

Required offer-stack contract:

- `data-offeros-section="offer-stack"` must also have `id="checkout"` or `data-offeros-buy-section`.
- It must include a product bundle visual marked `data-offeros-product-bundle`.
- It must include a large checklist marked `data-offeros-offer-checklist` with 8+ concrete deliverables; do not replace this with cards only.
- It must include a normally/today or total-value/today row marked `data-offeros-value-row`.
- It must include a large CTA marked both `data-offeros-cta` and `data-offeros-stack-cta`.
- It must include guarantee/instant-access reassurance marked `data-offeros-access-copy`.

Hard requirements for `direct-response-long-form-vsl`:

- 2,500+ visible words.
- 16+ meaningful sections or subsections.
- Separate `problem`, `agitation`, and `failed-alternatives` sections; do not combine them into one essay.
- VSL section visible copy must stay under 220 words and function as a video/pitch setup, not a long written sales letter.
- Normal paragraphs must stay under 55 words; use bullets, tables, proof cards, and callouts for longer ideas.
- No section except FAQ or offer stack may exceed 500 visible words.
- Every table cell, before/after card, proof/demo card, and product/bonus card must contain visible buyer-facing text.
- Text/background contrast must be checked in-browser; white text on white, invisible badges, or blank-looking cards fail the page.
- 7+ FAQ items marked with `data-offeros-faq-item`.
- 4+ CTA links/buttons marked with `data-offeros-cta`.
- 3+ CTA links/buttons after the hero marked with `data-offeros-post-hero-cta`.
- Unique buyer-facing copy for every offer-stack, angle, bonus, and product card.
- Repeated-text scan completed before QA.
