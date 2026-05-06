# Module Prompts

Use these as internal prompts/checklists. Each module must produce work that can be handed to the next module without interpretation.

## Offer Architecture

Purpose: turn raw context into a complete offer strategy.

Output:

1. Offer diagnosis: market category, sophistication, pain intensity, trust gap, conversion difficulty.
2. Ideal customer profile: primary buyer, disqualifying buyer, trigger event, emotional drivers, constraints.
3. Desire stack: conscious desire, hidden desire, identity desire, status/freedom/control desire.
4. Failed alternatives: what they tried, why it failed, what they now distrust.
5. Core offer: name, promise, transformation, mechanism, deliverables, timeline, format, support, buyer effort.
6. Value stack: core product, bonuses, tools/templates/assets, fast-action incentive if real.
7. Risk reversal: guarantee, terms, buyer responsibilities, credibility.
8. Pricing logic: price, anchoring, ROI argument, price objection response.
9. Messaging foundation: headline angle, problem frame, mechanism frame, proof frame, CTA frame.
10. Conversion path: ad role, sales page role, email role, VSL role, dashboard role.

Avoid broad audiences, generic promises, fake scarcity, unsupported claims, and bonuses that do not reduce buying friction.

## Design Resolver

Purpose: translate the offer strategy into a practical visual system.

Output:

1. Design strategy: visual positioning, emotional target, category fit, trust signals, conversion principles.
2. Style direction: aesthetic, density, spacing, radius, shadows, image treatment, icon style.
3. Color system: primary, secondary, accent, backgrounds, text, states, usage rules, colors to avoid.
4. Typography system: heading, body, accent, numerals, hierarchy.
5. Component direction: buttons, cards, testimonials, pricing, forms, navigation, progress, dashboard panels, PDF callouts, deck slides.
6. Asset direction: hero, product mockup, ad creative, PDF cover, VSL slides, dashboard interface, and expected provenance for each.
7. Do/don't list: at least 10 concrete rules.

Avoid mood-board words unless they become implementation rules.

## Logo And Brand

Purpose: create a usable identity system across all offer assets.

Production rule: follow the Logo Recipe in `references/exact-build-recipes.md`. The primary logo for a deep generated-design run is `assets/logo.png`, built from an imagegen brand mark and saved as a complete logo lockup with the readable offer name. Register it with `provenance: "imagegen"` only if imagegen produced the final readable lockup directly; otherwise use `provenance: "imagegen-composite"`. No primary SVG and no icon-only primary logo.

Output:

1. Brand position: promise, personality, buyer perception, category signal, differentiation.
2. Three logo concepts: idea, shape language, category signal, why it fits the buyer, and why it was rejected or selected.
3. Final logo direction: symbol/wordmark type, proportions, small-size behavior, one-color behavior, and production path.
4. Identity system: color, typography, icon, pattern/texture, image rules, product badge rules.
5. Brand voice: tone, sentence style, words to use, words to avoid, claims style, CTA style.
6. Usage rules: sales page, PDF, ads, emails, VSL, dashboard.
7. `imagegen` prompt for the brand mark or complete logo, plus the exact text-composite plan for the final readable logo lockup.
8. Optional secondary vector export prompt only if the user requested vector output.
9. Logo QA: nav-size preview, one-color check, bitmap export/preview, and `quality.logo` metadata.

Avoid abstract swooshes, generic marks, fragile details, and visual ideas that cannot extend to product assets. In deep generated-design runs, do not use a hand-coded SVG, HTML/CSS render, or PIL text graphic as the primary complete logo. The primary logo must be a bitmap file such as `.png` or `.webp`, must include the exact readable offer name, and must use imagegen for the brand mark; SVG is secondary only unless the user explicitly requests vector-only delivery.

## Sales Copy

Purpose: produce full conversion copy based on the offer architecture.

Production rule: follow the Sales Page Recipe in `references/exact-build-recipes.md`. Use the exact required `copy.md` headings and default `quality.salesPage.pageType` to `direct-response-long-form-vsl` for complete front-end offers.

Output:

1. Sales page type from `references/sales-page-types.md`, with reason.
2. Message map: big idea, promise, mechanism, objection, proof, CTA logic.
3. Headline set: 10 primary headlines, 10 subheads, 10 CTA labels, top 3 ranked.
4. Long-form copy: hero, VSL setup, problem, agitation, failed alternatives, mechanism, product intro, value stack, proof/demo, who it is for/not for, bonuses, guarantee, pricing, FAQ, final CTA.
5. Objection handling: price, time, trust, complexity, fit, prior failure, delay.
6. Microcopy: form labels, checkout reassurance, helper text, confirmation copy.

Composition rules: write the page as section-specific sales copy, not a single essay. Keep normal paragraphs under 55 words, keep the VSL setup under 220 words, and use comparison rows, checklists, callouts, proof/demo blocks, and CTA blocks to make the page scannable. Avoid vague hype, unsupported superlatives, fake urgency, wall-of-text sections, blank-looking cards, and copy that could sell any offer.

## Sales Page Build

Purpose: convert the copy/design into a production-ready page.

Source pattern: follow the Sales Page Recipe in `references/exact-build-recipes.md`. Start from `assets/templates/sales-page/page-skeleton.html`, then apply the design system. Fill the direct-response sections; do not design a new page structure from scratch.

Output:

1. Page strategy: selected page type, objective, buyer stage, conversion action, friction, trust approach.
2. Section blueprint: section name, conversion job, content, layout, visual treatment, CTA, asset, mobile behavior.
3. Component spec: header, manual-style direct-response hero, VSL, CTA blocks, proof, problem, mechanism, buy-box offer stack, pricing, guarantee, FAQ, footer.
4. Depth check: visible word count, objection count, CTA count, unique offer-stack item copy, repeated-text scan.
5. Implementation: responsive breakpoints, image sizes, performance, accessibility, form behavior, tracking events.
6. QA checklist: mobile scan, CTA, links, forms, proof, pricing, objections, speed, accessibility.

The coded page must use real copy and assets. Do not leave placeholders unless the user explicitly requests them. Do not create a giant VSL text block or a polished feature page; the section blueprint must drive the HTML structure.

Use the direct-response section contract from `assets/templates/sales-page/section-map.md`. Keep `data-offeros-section` markers for required sections. For `direct-response-long-form-vsl`, keep the exact hero and buy-box offer-stack contracts: hero video frame, price strip, CTA to `#buy`, trust row, bundle image, deliverable checklist, normally/today value row, large stack CTA, and guarantee/access reassurance. Do not ship a short branded product page, polished feature page, or generic card stack in place of the long-form sales page.

If the page uses SVG/CSS diagrams as temporary visuals, mark them as fallbacks and do not describe them as generated images.

## PDF Product

Purpose: create a buyer-ready productized asset.

Output:

1. Product strategy: title, promise, reader outcome, funnel role, completion action, next step.
2. Table of contents with section purpose and estimated pages.
3. Page-by-page plan: title, job, content, layout, visuals, fields, CTA/prompt.
4. Core content: section copy, examples, checklists, worksheets, templates, scoring models, implementation steps.
5. Design spec: cover, typography, colors, callouts, tables, worksheets, page furniture.
6. Exported PDF and source file.
7. Depth metadata: page count, action-surface count, named tool count, page archetype count, completed example count, blank template count, render check.

Avoid blog-post content, filler introductions, generic tips, vague worksheet prompts, repeated "Action Surface" boxes, identical page layouts, and no clear next step. A paid workbook must contain named tools, completed examples, matching blank templates, and distinct page archetypes.

## Facebook Ads

Purpose: create buyer-attracting Meta/Facebook strategy, copy, and creative.

Output:

1. Market diagnosis.
2. 15 angles with buyer state, hook, why it works, filter effect.
3. 30 hooks split by problem, solution, "if X worked", and identifier hooks.
4. 10 creative concepts with visual idea, image text, process hint, emotional state.
5. 10 complete ads with primary text, headline, description, CTA, concept, image text, buyer attracted, non-buyer filtered.
6. Best 3 to test first.
7. At least 3 imagegen ad images when image generation is available, otherwise clearly recorded fallbacks with blocker reason.

Avoid personal-attribute violations, exaggerated claims, generic stock-photo ideas, and one angle repeated repeatedly.
Do not fill angle cards with repeated explanatory boilerplate. Each angle needs its own buyer state, hook logic, visual idea, and reason it should attract or filter a different segment.

## Email Sequence

Purpose: create a persuasive sequence, not isolated emails.

Output:

1. Sequence strategy: type, length, timing, buyer stage, conversion action.
2. Email map: send time, subject, preview, job, belief shift, objection, CTA.
3. Full emails: at least 7 in deep mode unless the funnel requires fewer.
4. Branches: opened/no click, clicked/no buy, bought, did not open, replied, expired deadline.
5. Optimization notes: subject tests, CTA tests, resend logic, suppression, deliverability.

Avoid seven versions of "buy now", fake personal stories, spam urgency, and generic subject lines.

## VSL Deck

Purpose: create a narratable video sales letter deck.

Source pattern: follow the VSL Deck Recipe in `references/exact-build-recipes.md`. Create a `.pptx` first. Use `pptxgenjs`, the Presentations plugin, or another PowerPoint-capable path. HTML is a preview/export only.

Output:

1. VSL strategy: target length, viewer stage, big idea, mechanism, proof, CTA.
2. Narrative arc: hook, problem, stakes, failed alternatives, insight, mechanism, proof, offer, stack, risk reversal, CTA.
3. Layout palette: at least 8 visual treatments and max share for the most-used layout.
4. Slide-by-slide plan for 20 to 30 slides: buyer-facing title, internal job, on-slide text, speaker notes, visual direction, motion notes, assets.
5. Visual asset plan: 12+ unique visual assets or distinct diagram treatments, no non-logo bitmap repeated on more than 25% of slides, and no recycling the same 3 images as filler.
6. Quality metadata: slide count, layout count, max layout share, speaker notes, visible stage labels removed, notes are narration, offer reveal, price, guarantee, objections, presentation-ready status.

Create the primary `vsl-deck` as a PowerPoint `.pptx`. Create HTML/contact-sheet output only as `vsl-preview`. Avoid repeated one-layout card grids. A contact sheet is a preview artifact, not the VSL deck.
7. Timing plan: seconds per slide, runtime, pace notes.
8. Production notes: voice tone, music, captions, aspect ratio, export requirements, end screen.

Avoid text-heavy slides, summary decks, decorative animations, and delayed offer reveals without reason. Do not put internal labels such as "Agitate", "Problem", "Proof", "Offer", "CTA", "Objection", "Stage: Problem", or "Problem:" anywhere in visible slide copy.

## Delivery Dashboard

Purpose: create the browser asset hub for reviewing and using the completed system.

Source pattern: run `scripts/generate_delivery_dashboard.py` after artifacts are registered, then theme the generated dashboard. Preserve the template structure.

Output:

1. Branded HTML dashboard.
2. Cards grouped by sales, product, traffic, email, VSL, brand assets, QA.
3. Modal previews for HTML, images, PDFs, and browser-safe deck previews.
4. Direct open/download action for every asset.
5. Mobile-responsive layout with no horizontal overflow.
6. Provenance and commercial-score display where useful.

Use `scripts/generate_delivery_dashboard.py` as the starting point. Theme the standard modal dashboard; do not replace it with a static link grid.
7. Manifest-driven artifact registration.

Avoid static file lists, owner-only notes, tiny thumbnails, and navigation that takes the user away for every preview.
