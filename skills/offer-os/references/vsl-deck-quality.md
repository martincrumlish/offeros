# VSL Deck Quality

A VSL deck is a recording asset, not a summary page and not a contact sheet. The primary deliverable must be an editable `.pptx` unless the user explicitly requests another format.

## Production Path

1. Write a VSL narrative plan.
2. Create a slide layout palette.
3. Build the `.pptx`.
4. Add speaker notes that can guide a recording.
5. Export a browser-safe preview/contact sheet for dashboard viewing.
6. Browser-test the preview at desktop width and about 390px mobile width. Revise if there is horizontal overflow or broken imagery.
7. Inspect the preview and revise weak slides before marking complete.

HTML output is allowed only as `vsl-preview`, `vsl-contact-sheet`, or an auxiliary browser deck. Do not register HTML as `vsl-deck`.

When registering the `.pptx`, set the artifact `preview` to browser-safe HTML/image. The dashboard should iframe the preview and use the open action for the actual `.pptx`; it must not iframe the PowerPoint file.

## Viewer-Facing Copy

Internal stage labels are not allowed anywhere in visible slide copy.

Bad visible titles:

- Hook
- Problem
- Agitate
- Market
- Mechanism
- Proof
- Offer
- CTA
- Objection
- Close

Use buyer-facing titles instead:

- "Fit Is Not The Whole Race."
- "Race-Day Drift Leaks Minutes."
- "The First Mistake Rarely Stays Alone."
- "More Workouts Are Not The Missing Layer."
- "The Race-Day Control System."
- "Get The Complete Toolkit For $47."

Stage labels may appear in the private slide plan, notes metadata, or file comments, but not on-slide as titles, badges, eyebrows, footers, captions, or prefixes such as `Stage: Problem` or `Problem:`.

## Layout Palette

Use at least 8 distinct visual treatments across a 20-30 slide deck:

- full-bleed title or pattern interrupt
- audience identifier card
- problem map
- compounding cost chain
- failed-alternatives comparison
- mechanism diagram
- step-by-step method slide
- product/mockup reveal
- offer stack/value build
- proof/demo screenshot
- price/value contrast
- guarantee/risk reversal
- objection handling
- final CTA

No single layout family should account for more than 35% of the slides. A repeated two-column copy/placeholder design fails deep mode even if the deck has enough slides.

Layout family means structural composition. Color swaps, icon swaps, background color changes, tiny badges, or different placeholder labels do not create a new layout family. Record a slide-numbered layout audit in `quality.vsl.layoutAudit`.

## Visual Requirements

Key slides must include real visuals, diagrams, screenshots, generated frames, or product previews. Dark placeholder rectangles with small labels are not finished visuals.

Use the resolved design system, but vary composition, scale, contrast, and focal point. A consistent theme does not mean identical slide structure.

Before building the PPTX, create a slide-by-slide visual asset plan. A deep-mode 20-30 slide deck needs 12+ unique visual assets or distinct diagram treatments. Reusing the same 3 generated images as slide filler fails the deck even if the copy changes.

No single non-logo bitmap should appear on more than 25% of slides. Product bundle imagery should appear only on product reveal, offer stack, price/value, and final CTA slides. Use diagrams, comparison tables, matrices, screenshots, product previews, and generated frames to create visual variety instead of stretching a small image set across the whole VSL.

PowerPoint image placement must preserve aspect ratio. In `pptxgenjs`, do not place bitmaps with only arbitrary `x`, `y`, `w`, and `h` values unless the source image ratio already matches the box. Route every deck image through an explicit helper that sets `sizing: { type: "cover", w, h }` for full-bleed/photo boxes or `sizing: { type: "contain", w, h }` for logos, product previews, and UI screenshots. A stretched or compressed bitmap fails the VSL gate.

## Speaker Notes

Speaker notes should be narration guidance, not design labels.

Good notes:

- concrete spoken point
- transition into the next belief
- proof caveat or claim constraint
- CTA wording
- timing guidance

Bad notes:

- "Narration: Explain mechanism."
- "Agitate."
- "Show proof."
- "Visual: chart."

Every slide needs at least 25 words of usable recording guidance. Repeating the same generic note template across slides fails the deck.

Speaker notes must use manifest/source variables for price and offer name. Do not hard-code a price in narration notes. A note that says a different price from `offer-os.json.price` fails the deck.

## Required Metadata

Populate `quality.vsl`:

```json
{
  "slideCount": 24,
  "layoutCount": 9,
  "maxLayoutShare": 0.29,
  "primaryFormat": "pptx",
  "visualAssetCount": 14,
  "uniqueVisualAssetCount": 12,
  "maxRepeatedBitmapShare": 0.21,
  "visualReuseChecked": true,
  "presentationReady": true,
  "hasSpeakerNotes": true,
  "notesAreNarration": true,
  "visibleStageLabelsRemoved": true,
  "layoutDiversityChecked": true,
  "visualPlaceholdersRemoved": true,
  "hasOfferReveal": true,
  "hasPrice": true,
  "hasGuarantee": true,
  "hasObjections": true
}
```
