# Copy Critic Rubric

Run this critic pass after `scripts/build_copy.py` renders `copy.md` and before visual planning, sales-page building, PDF, VSL, emails, ads, or dashboard work.

## Pass Conditions

`copy.md` passes only when all conditions are true:

- It is finished buyer-facing sales copy, not a blueprint, outline, schema, or notes.
- It contains 2,500+ customer-facing words; 3,500-5,500 is the target range for deep mode.
- It can sell if the VSL is removed.
- It contains a clear hook, story/insight, and offer flow.
- It contains a specific new insight before the named mechanism.
- It names and explains the unique mechanism before product reveal and offer stack.
- It has proof/demo before price and the main offer stack.
- It reveals the product in plain English.
- It includes feature-benefit-reason detail for all core components.
- It explains why every offer-stack item matters.
- It includes a believable price/value contrast.
- It includes a concrete guarantee.
- It includes 7+ specific FAQ objections with belief-shifting answers.
- It does not use repeated boilerplate sentences or repeated paragraphs.
- It does not expose internal labels such as conversion job, belief shift, visual need, copy anchor, framework role, or section instructions.

## Revision Rule

If the copy fails, revise `copy-plan.json` first, then rerun `scripts/build_copy.py`.

Do not patch `copy.md` directly in deep mode.

Do not continue to images or page generation with weak copy. Weak copy produces weak visuals, weak pages, weak emails, weak PDFs, and weak VSLs.

## Critic Questions

Ask these against the rendered `copy.md`:

1. Would a buyer understand the offer if every video/image disappeared?
2. Does the first screen make a specific promise to a specific buyer?
3. Does the problem section sound like the buyer's actual situation, or generic marketing prose?
4. Are failed alternatives named and explained?
5. Is there a real epiphany, or just "you need a system" filler?
6. Is the mechanism named and unpacked clearly?
7. Is proof shown before the main offer stack?
8. Does the product reveal make the deliverable feel tangible?
9. Do the feature bullets explain benefit and reason, not only feature names?
10. Does the price logic feel believable without fake urgency or fake value math?
11. Are FAQs specific enough that they could only belong to this offer?
12. Are repeated paragraphs, repeated cards, or meta phrases present?

If any answer is weak, revise `copy-plan.json` and render again.
