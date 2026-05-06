# VSL Slide Outline

Aim for 20 to 30 slides with low text and speaker notes.

The deliverable must be a presentation-ready PowerPoint deck. A browser HTML contact sheet or presenter page may be created as `vsl-preview`, but `vsl-deck` must be an editable `.pptx` file unless the user explicitly asks for HTML-only delivery.

The slide jobs below are internal planning labels, not visible slide copy. Visible titles, badges, footers, captions, and prefixes must be buyer-facing. Do not show labels like "Agitate", "Problem", "Proof", "Offer", "CTA", "Stage: Problem", or "Problem:" anywhere on the slides.

| Slide | Job |
| --- | --- |
| 1 | Pattern interrupt |
| 2 | Identify the viewer |
| 3 | Name the painful current state |
| 4 | Show the cost of staying there |
| 5 | Invalidate common fixes |
| 6 | Introduce the new belief |
| 7 | Name the mechanism |
| 8 | Explain why it works |
| 9 | Show the desired future state |
| 10 | Method overview |
| 11 | Step 1 |
| 12 | Step 2 |
| 13 | Step 3 |
| 14 | Proof or demonstration |
| 15 | Product reveal |
| 16 | What is included |
| 17 | Bonus 1 |
| 18 | Bonus 2 |
| 19 | Value stack |
| 20 | Price |
| 21 | Guarantee |
| 22 | Objection: time |
| 23 | Objection: fit |
| 24 | Objection: trust |
| 25 | Final CTA |
| 26 | Closing reminder |

## Deep-Mode Requirements

- 20-30 slides.
- Primary artifact is `.pptx`.
- 8+ distinct layouts or visual treatments.
- No single layout family above 35% of the deck.
- Layout families are structural compositions. Color/icon/background swaps do not count as new layouts.
- `quality.vsl.layoutAudit` records slide number, layout family, and visual asset for every slide.
- Speaker notes or narration guidance on every slide.
- Notes are recording guidance, not labels such as "Explain the proof".
- Real visuals or generated frames on key slides: hook, problem, mechanism, proof/demo, product reveal, stack, price, guarantee, objections, CTA.
- Dashboard-safe contact sheet or HTML preview as a separate artifact.

Fails if every slide is the same card design, if the deck is a grid of cards, if the primary deck is HTML, if stage labels are visible as titles, or if the speaker notes are generic visual placeholders instead of usable narration.
