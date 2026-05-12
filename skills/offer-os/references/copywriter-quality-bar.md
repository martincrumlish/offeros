# Copywriter Quality Bar

Use this reference before writing `copy-plan.json`. Copy Studio is not a planning scaffold. It is the finished sales-letter source.

## Core Rule

Write finished buyer-facing copy inside `copy-plan.json.sectionPlan[].copyBlocks`.

Do not write notes, outlines, section descriptions, strategy labels, or reminders for a later writer. `scripts/build_copy.py` renders `copy.md` from these blocks. If the blocks are thin, generic, or meta, the finished sales copy will be thin, generic, or meta, and the build must stop.

## Required Sales-Letter Style

- Use a Modern Brunson-style long-form argument: Hook, Story/Insight, Offer.
- The written page must stand alone if the VSL is removed. The VSL can support the argument, but it cannot carry the mechanism, proof, product reveal, price logic, guarantee, or objections by itself.
- Write concrete copy for the specific buyer, problem, mechanism, and product. Avoid generic AI phrases that could fit any offer.
- Use short paragraphs, specific examples, proof cues, and clean direct-response rhythm.
- Use the buyer's language. Show the lived situation, the failed fixes, and the cost of continuing.
- Introduce a specific epiphany/new insight before the unique mechanism.
- Name the unique mechanism before proof and product reveal.
- Put proof/demo before the offer stack and price.
- Explain the product in plain English, then list feature-benefit-reason bullets.
- Explain why each stack item matters; do not only name deliverables.
- Use a real guarantee and a real urgency basis. If there is no real urgency, say none and sell on value/risk reversal.

## Forbidden Copy

Do not put any of this in buyer-facing copy:

- "this section explains"
- "this section should"
- "the buyer can see"
- "makes this point"
- "conversion job"
- "framework role"
- "belief shift"
- "visual need"
- "copy anchor"
- "CTA role"
- "write a headline"
- "include a paragraph"
- repeated template sentences mapped over cards
- internal labels such as Problem, Agitate, Mechanism, Proof used as visible slide/page titles unless they are natural customer-facing headings
- VSL labels such as "pitch", "short pitch", or "watch the pitch"; use "walkthrough", "breakdown", "overview", "demo", or "presentation" instead

## Section Writing Jobs

Hero:
- buyer filter or prehead
- big promise headline
- lead that names the painful situation and desired outcome
- early CTA/price hint

VSL setup:
- short supporting setup only
- do not imply the reader must watch the video to understand the offer
- do not call the video a pitch; frame it as a walkthrough, breakdown, overview, demonstration, or presentation

Problem diagnosis:
- diagnose the real problem behind the surface problem
- use concrete signs the buyer recognizes

Cost of staying stuck:
- show what continuing costs in time, money, confidence, missed launches, race performance, client trust, or whatever matters in the offer

Failed alternatives:
- name at least three things the buyer already tried
- explain why each fails and what is needed instead

New insight:
- give the epiphany that reframes the problem
- make it specific enough that it could not be swapped into a different market unchanged

Unique mechanism:
- name it
- explain why it works
- break it into steps the buyer can understand

Proof/demo:
- show why the mechanism is believable before asking for the main purchase
- use preview, demonstration, before/after logic, screenshots, examples, samples, or process proof if formal case studies are unavailable

Product reveal:
- describe what the buyer gets in plain English
- say who it is for, what it helps them do, and why now
- bridge naturally from the mechanism into the product

Feature-benefit breakdown:
- for every core component, write feature, benefit, reason it matters, buyer problem solved, proof/preview, and one plain sales bullet

Offer stack:
- explain each deliverable as a buyer outcome, not just a file name
- connect every item to the promise, mechanism, proof, or objection it supports

Pricing/value:
- contrast the price against the cost of the current problem or a believable alternative
- do not use fake value stacking

Guarantee:
- make the terms concrete
- explain why the guarantee is fair and what the buyer must do

FAQ:
- include 7+ specific objections
- each answer must create a belief shift, not only say "yes"

Final close:
- summarize the decision
- restate the promise, risk reversal, and CTA without adding new logic
