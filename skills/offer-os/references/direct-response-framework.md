# Direct Response Long-Form Framework

Use this as the default persuasion spine for complete paid front-end OfferOS pages. Do not copy a single reference page. Build the argument.

## Core Spine

Every `direct-response-long-form-vsl` page must move the buyer through this sequence:

1. Message match
2. Hook / VSL lead
3. Problem recognition
4. Agitation and cost of delay
5. Failed alternatives
6. Unique mechanism
7. Proof or demonstration
8. Before/after value picture
9. Product reveal
10. Offer stack
11. Risk reversal
12. Objection handling
13. Final close

This blends AIDA, PAS, PASTOR, 4P, and problem-mechanism-proof-offer. Those frameworks can shape sections, but they cannot remove the spine.

## Mandatory Conversion Jobs

- **Message match:** continue the same audience, promise, problem, and emotional frame from the prompt, ad angle, or offer architecture.
- **Hook / VSL lead:** make one specific promise or contrarian insight obvious before asking for attention.
- **Problem recognition:** name the buyer's current situation in concrete terms.
- **Agitation:** show the cost of staying stuck without melodrama.
- **Failed alternatives:** explain why the buyer's likely past attempts did not solve the problem.
- **Unique mechanism:** explain why this approach works differently and why the buyer should believe the promise now.
- **Proof or demonstration:** support the mechanism before the main offer stack. Use real proof when available; otherwise use proof substitutes such as worked examples, sample outputs, process logic, screenshots, or transparent demonstrations.
- **Before/after:** make the transformation concrete.
- **Product reveal:** introduce the product after the belief argument has been built.
- **Offer stack:** show exactly what they get, how it is delivered, why each piece matters, bonuses, value context, price, and CTA.
- **Risk reversal:** make the guarantee, access, and next steps clear.
- **Objection handling:** answer fit, time, implementation, trust, price, refund, and "is this just more information?"
- **Final close:** restate the outcome, cost of inaction, price, guarantee, and CTA.

## Copy Blueprint Schema

Before `index.html` or `visual-asset-plan.md`, `copy.md` must include `# Section Blueprint` with one row per required page section.

Each row must contain:

- `sectionId`
- `conversionJob`
- `targetWords`
- `beliefShift`
- `proofOrObjection`
- `visualKind`
- `copyAnchor`
- `ctaRole`

The blueprint is the source of truth for the page, sales-page visuals, and QA. If the blueprint is vague, the page will become generic.

## Mandatory Section Order

Use this order for `direct-response-long-form-vsl`:

`header -> hero -> vsl -> problem -> agitation -> failed-alternatives -> mechanism -> proof -> before-after -> product -> offer-stack -> fit -> pricing -> guarantee -> faq -> final-cta -> footer`

Do not move proof only after the buy box. Buyers need belief before price.

## CTA Rhythm

Minimum CTA rhythm:

- 1 CTA in or directly below the hero price strip.
- 1 CTA after proof/demo or product reveal.
- 1 primary CTA in the offer stack.
- 1 final CTA after FAQ.

Use one buying action and repeat it. Do not introduce competing actions unless the user explicitly requested them.

## Visual Roles

Use visuals to clarify the argument:

- Hero: large VSL/video frame, not a small dashboard/product mockup card.
- Failed alternatives: comparison table or contrast graphic.
- Mechanism: named framework diagram or structured panel.
- Proof/demo: screenshots, sample output, case snapshot, before/after, or proof substitute.
- Product reveal and offer stack: bundle/mockup visuals are appropriate here.
- FAQ/objections: light callouts, not decorative filler.

## Fail States

The page fails if it:

- reads as hero/features/price/FAQ
- has section markers but empty or generic sections
- presents product/price before the mechanism and proof
- uses mockup visuals as the main argument
- uses a two-column SaaS hero with a small right-side video/card
- turns the VSL section into a wall of text
- replaces the offer stack with generic pricing cards
- has no clear new mechanism
- has no proof, demonstration, or proof substitute before the buy box
