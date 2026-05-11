# Copy Frameworks

Choose one primary sales framework, then use section-level frameworks where useful.

This file chooses persuasion logic. It does not choose the page archetype. Before writing `copy.md`, also choose a sales page type from `references/sales-page-types.md`.

## PASTOR

Use for coaching, consulting, courses, workshops, expert-led offers, and transformation products.

Best when trust matters and the buyer needs empathy before proof.

Structure:

- Problem
- Amplify
- Story/Solution
- Transformation
- Offer
- Response

## PAS

Use for direct-response sections, short pages, advertorial openings, and problem-aware audiences.

Structure:

- Problem
- Agitate
- Solution

## AIDA

Use for broad-market, cold traffic, productized services, and simple offers where clarity matters most.

Structure:

- Attention
- Interest
- Desire
- Action

## Direct-Response-Long-Form-V1

Use for complete paid front-end OfferOS pages, cold traffic, low-ticket offers, workshops, toolkits, templates, and internet-marketing style funnels.

Structure:

- message match
- hook / VSL lead
- problem recognition
- agitation and cost of delay
- failed alternatives
- unique mechanism
- proof or demonstration before price
- before/after value picture
- product reveal
- offer stack
- risk reversal
- objection handling
- final close

This is the required deep-mode page spine unless the user explicitly requested a different page type. Load `references/direct-response-framework.md` for the exact conversion jobs and copy blueprint schema.

## Modern-Brunson-Long-Form-V1

Use this as the required Copy Studio framework for complete paid front-end OfferOS pages.

Structure:

- buyer filter / prehead
- big promise headline
- lead / core hook
- optional VSL or hero visual
- early CTA / price hint
- problem diagnosis
- cost of staying stuck
- failed alternatives
- epiphany / new insight
- unique mechanism
- proof or demonstration
- product reveal
- feature-benefit breakdown
- how it works
- offer stack
- bonuses / accelerators
- price/value contrast
- guarantee
- fit / who it is for
- FAQ / objections
- final close

This framework produces `copy-plan.json` first, with finished buyer-facing copy in `sectionPlan[].copyBlocks`. Then `scripts/build_copy.py` renders clean written `copy.md`, internal `copy-blueprint.md`, and `sales-page-blueprint.json`. The written page must stand alone without the VSL, contain 2,500+ customer-facing words, and pass the Copy Critic rubric before visual planning or page generation.

## Problem-Mechanism-Proof-Offer

Use for sophisticated or skeptical markets where buyers have tried alternatives.

Structure:

- specific problem diagnosis
- failed common approaches
- unique mechanism
- proof
- offer
- risk reversal
- CTA

For skeptical sections inside complete paid front-end OfferOS sales pages, this is the core belief-change layer. PAS, AIDA, BAB, QUEST, PASTOR, and 4P can shape sections, but they cannot reduce deep-mode page depth or remove the required section contract from `assets/templates/sales-page/section-map.md`.

## Before-After-Bridge

Use for concise offer pages, hero sections, product summaries, and simple transformation messaging.

## 4P

Use for above-the-fold copy, offer summaries, checkout sections, and conversion blocks.

Structure:

- Promise
- Picture
- Proof
- Push

## QUEST

Use for educational sales pages, webinars, challenge funnels, and offers that require a belief shift.

Structure:

- Qualify
- Understand
- Educate
- Stimulate
- Transition

## Section-Level Tools

- FAB for feature/module descriptions
- So What Test for every feature or claim
- Objection Reversal for FAQ, guarantee, price, and final CTA
- Star-Story-Solution for founder story or case studies
- One Belief for VSL and new-category offers

## Default Choice

- Expert-led transformation: PASTOR
- Skeptical/high-sophistication market: Problem-Mechanism-Proof-Offer
- Simple productized offer: AIDA
- Short page or sharp section: PAS
