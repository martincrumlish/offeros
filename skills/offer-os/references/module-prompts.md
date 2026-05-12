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

## Visual Asset Plan

Purpose: define artifact-specific visuals before production so PDF, VSL, and ads are not built from leftover sales-page images.

Production rule: follow the Visual Asset Plan Recipe in `references/exact-build-recipes.md`. Create `visual-asset-plan.md` v2 after the logo/product outline, `copy-plan.json`, clean `copy.md`, `copy-blueprint.md`, and `sales-page-blueprint.json` exist. Do not create page/PDF/VSL/ad visuals from a pre-copy mood board.

Output:

1. Visual metadata: `visualPlanStage: post-content-blueprint`, `copyBlueprintUsed: true`, `copyStudioUsed: true`, `copyPlanPath: copy-plan.json`, `salesPageImageSystem: mixed-direct-response-v1`, `primaryConversionFinalPixelsPolicy: imagegen-final-v1`, and `mockupHeavyUserRequested`.
2. Global brand assets: logo lockup, brand mark, product bundle/mockup, reusable pattern/frame.
3. Sales page visuals: 4+ visuals with `visualKind`, `copyAnchor`, conversion job, file path, aspect ratio, and text rule.
4. PDF product visuals: 6+ visuals/treatments, including 4+ PDF-specific visuals that are not reused from the sales page.
5. VSL deck visuals: 12+ visuals/treatments, including 8+ VSL-specific visuals that are not reused from the sales page.
6. Ad visuals: 3+ ad-specific imagegen creatives.
7. Dashboard visuals: previews/thumbnails for core assets.
8. Reuse rules: what can be reused, where, and why.
9. Agent dispatch plan: whether imagegen visual workers should be dispatched, worker ownership, output folders, and references.
10. `quality.images` metadata.

Default sales-page image system: `mixed-direct-response-v1`. Use product/dashboard/offer-stack mockups where they sell the product or stack. Use diagrams, comparison visuals, proof/demo visuals, structured panels, screenshots, or restrained buyer-situation imagery for mechanism, failed alternatives, proof, objections, and feature specifics. Avoid treating the sales page as the master image pool. Avoid all-mockup sales pages unless the user explicitly requested mockup-heavy.

Primary creative source rule: in deep generated-design runs, `hero-vsl-frame`, `product-mockup`, `offer-stack-bundle`, `buyer-situation-photo`, and `ad-creative` outputs must be final-pixel `imagegen` assets. Record `source/provenance: imagegen-final`, `finalPixelsGeneratedBy: imagegen`, `localCreativeOverlay: false`, and `localPostprocess` limited to crop, resize, compression, or format-conversion. Use `imagegen-composite` only when imagegen performed the composition with reference images and the row records `imagegenNativeComposite: true`. Do not make those assets as HTML/CSS, canvas, screenshot, generated-by-code, manual PNG placeholders, or local composites. Do not use Pillow/PIL/canvas/local scripts to add logo, headline text, labels, UI cards, badges, mockups, overlays, or product-stack composition after imagegen. If the creative is wrong, regenerate or edit with imagegen. Those local methods are only for diagrams, matrices, worksheet previews, real screenshots of built artifacts, or QA evidence.

## Logo And Brand

Purpose: create a usable identity system across all offer assets.

Production rule: follow the Logo Recipe in `references/exact-build-recipes.md`. The primary logo for a deep generated-design run is `assets/logo.png`, created through one single-final-logo imagegen call with symbol plus exact readable offer-name wordmark. Do not create 3 logo options, option sheets, alternate lockups, symbol-only fallbacks, or text-composited repairs unless the user explicitly asks for options or a non-imagegen repair. Register the generated logo with `provenance: "imagegen"`. No SVG logo files at all, no icon-only primary logo, no illustrative mark, and no rough "mark plus default text" composite.

After the final logo is accepted, freeze it. Later imagegen prompts that need branding must pass `assets/logo.png` as the only logo reference and instruct imagegen to use the supplied logo exactly. Downstream product, ad, PDF, VSL, dashboard, and page images must not invent, redesign, recolor, redraw, reinterpret, replace, or substitute another logo/wordmark. No alternate logo attempts may be passed as references.

Output:

1. Brand position: promise, personality, buyer perception, category signal, differentiation.
2. One final logo direction: idea, shape language, category signal, why it fits the buyer, and exact execution notes.
3. Final logo direction: symbol/wordmark type, proportions, small-size behavior, one-color behavior, production path, final selected lockup path `assets/logo.png`, and brand-lock status.
4. Identity system: color, typography, icon, pattern/texture, image rules, product badge rules.
5. Brand voice: tone, sentence style, words to use, words to avoid, claims style, CTA style.
6. Usage rules: sales page, PDF, ads, emails, VSL, dashboard.
7. `imagegen` prompt for one final complete logo lockup, plus downstream logo-reference rule for product/mockup imagegen jobs.
8. No vector/SVG export prompt. Generated OfferOS logo output is PNG/WebP bitmap only.
9. Logo QA: nav-size preview, one-color check, exact-name preservation check, wordmark kerning/spacing check, bitmap export/preview, and `quality.logo` metadata.

Avoid abstract swooshes, generic marks, fragile details, page-curl/folded-paper graphics, app-icon marks, illustrative cover-art marks, and visual ideas that cannot extend to product assets. In deep generated-design runs, do not use a hand-coded SVG, HTML/CSS render, PIL text graphic, or text compositor as the primary complete logo. The primary logo must be a horizontal bitmap lockup such as `.png` or `.webp`, must include the exact readable offer name, must use one final imagegen logo call, and must pass professional wordmark checks. Do not create or register SVG logo assets.

## Sales Copy

Purpose: produce full conversion copy based on the offer architecture through Copy Studio.

Production rule: follow the Sales Page Recipe in `references/exact-build-recipes.md`. Load `references/copywriter-quality-bar.md` before authoring. Write `copy-plan.json` first using `framework: "modern-brunson-long-form-v1"`, `standaloneCopyRequired: true`, and `vslDependency: "optional-supporting-asset"`. Write finished buyer-facing sales copy inside `sectionPlan[].copyBlocks`; do not write notes, scaffolds, internal labels, or reminders for a later copywriter. Then run `scripts/build_copy.py` to render exact page-copy `copy.md`, internal `copy-blueprint.md`, and `sales-page-blueprint.json`. `copy.md` must use bracketed section blocks (`[hero]...[/hero]`, `[mechanism]...[/mechanism]`, etc.) and the sales page must render those blocks exactly, with the markers converted to HTML comments. Do not summarize the copy into generic cards or slice sections down to three items. Apply `references/copy-critic-rubric.md` to the rendered copy. Use `copy.md` as the delivery-dashboard sales-copy artifact, and keep section tables/framework metadata in `copy-blueprint.md`. Default `quality.salesPage.pageType` to `direct-response-long-form-vsl` for complete front-end offers.

Output:

1. Sales page type from `references/sales-page-types.md`, with reason.
2. `copy-plan.json` with the Modern Brunson long-form spine: hook, story/insight, belief shift, unique mechanism, proof, product reveal, feature-benefit breakdown, how it works, offer stack, risk reversal, objections, and close.
3. Message map: big idea, promise, new insight, mechanism, objection, proof, CTA logic.
4. Product reveal: product type, plain-English description, who it is for, what it helps them do, why now, core components, how-it-works steps, look-inside proof, difference from alternatives, and bridge to offer stack.
5. Feature-benefit-reason rows for every core component and value-explained deliverables for the offer stack.
6. Objection matrix: 7+ real objections with answers and belief shifts; no generic FAQ labels.
7. Rendered clean `copy.md`, internal `copy-blueprint.md`, and generated `sales-page-blueprint.json` from `scripts/build_copy.py`.
8. Copy Critic pass: `copy.md` has 2,500+ customer-facing words, target 3,500-5,500, no meta copy, no repeated boilerplate, no VSL dependency, and section-level depth.

Composition rules: write the page as section-specific sales copy, not a single essay. The written page must stand alone without a VSL. Keep normal paragraphs under 55 words, keep the VSL setup under 220 words, and use comparison rows, checklists, callouts, proof/demo blocks, and CTA blocks to make the page scannable. Avoid vague hype, unsupported superlatives, fake urgency, wall-of-text sections, blank-looking cards, meta phrases such as "this section explains" or "belief shift", and copy that could sell any offer.
Never label the VSL or offer video as a "pitch" in buyer-facing copy. Use "walkthrough", "breakdown", "overview", "demo", or "presentation".

## Sales Page Build

Purpose: convert the copy/design into a production-ready page.

Source pattern: follow the Sales Page Recipe in `references/exact-build-recipes.md`. Start from `assets/templates/sales-page/page-skeleton.html`, then apply the design system. Fill the direct-response sections; do not design a new page structure from scratch.

Output:

1. Page strategy: selected page type, objective, buyer stage, conversion action, friction, trust approach.
2. Section blueprint: section name, conversion job, content, layout, visual treatment, `copyAnchor`, `visualKind`, CTA, asset, mobile behavior.
3. Component spec: header, stacked VSL-first direct-response hero, VSL, problem, agitation, failed alternatives, mechanism, proof/demo before the buy box, before/after, product reveal, buy-box offer stack, pricing, guarantee, FAQ, final CTA, footer.
4. Depth check: visible word count, objection count, CTA count, unique offer-stack item copy, repeated-text scan.
5. Implementation: responsive breakpoints, image sizes, performance, accessibility, form behavior, tracking events.
6. QA checklist: mobile scan, CTA, links, forms, proof, pricing, objections, speed, accessibility.

The coded page must use real copy and assets. Do not leave placeholders unless the user explicitly requests them. Do not create a giant VSL text block or a polished feature page; the section blueprint must drive the HTML structure.

Use the direct-response section contract from `assets/templates/sales-page/section-map.md`. Keep `data-offeros-section` markers for required sections. For `direct-response-long-form-vsl`, use the `sales-page-blueprint.json` generated from `copy-plan.json`, write `theme.json`, then run `scripts/build_sales_page.py`. Preserve the locked `offeros-stacked-vsl-v2` hero: centered copy stack, large 16:9 `.oo-vsl-frame` hero video below the headline, thumbnail, play button, caption, price strip below the video, CTA to `#checkout`, trust row, proof/demo before the buy box, bundle image, deliverable checklist, normally/today value row, large stack CTA, and guarantee/access reassurance. Use a no-section-nav header, quiet eyebrow/prehead labels, sparse section eyebrows (`eyebrowPolicy: "sparse-key-signposts-v1"`) rather than a pill on every section, centered eyebrow alignment with the H2 (`eyebrowAlignment: "centered-with-section-heading"`), Lucide icon markers with CSS fallback for card grids and checklist items, and content-hugging constrained visual frames marked `data-offeros-image-display="constrained"`. If the hero already contains the main VSL frame, the later VSL section explains the video argument; it must not say "Watch this first". Do not ship a short branded product page, polished feature page, two-column SaaS hero, dashboard/product mockup hero, tiny right-side VSL card, proof-after-price-only page, embedded checkout, order form, payment fields, unconstrained full-size images, mismatched colored image mattes, an eyebrow/pill on every section, floating left-offset pills above centered H2s, or generic card stack in place of the long-form sales page.
The coded page must render from typed `copy-plan.json.sectionPlan[].copyBlocks` first. Do not infer every component from Markdown bullets. `copy.md` is the readable delivery artifact; typed copy blocks are the page layout source so each section can use its proper component pattern. The offer stack must also read `copy-plan.json.offerStack.items` and render a differentiated package component, not a long run of identical boxes.

If the page uses HTML/CSS diagrams as temporary visuals, mark them as fallbacks and do not describe them as generated images. Do not create SVG diagram files.

For sales-page graphics that need brand presence, pass `assets/logo.png` as the exact logo reference to imagegen. Do not let imagegen invent, redraw, recolor, reinterpret, replace, or substitute another logo.

## PDF Product

Purpose: create a buyer-ready productized asset.

Output:

1. Product strategy: title, promise, reader outcome, funnel role, completion action, next step.
2. Table of contents with section purpose and estimated pages.
3. Page-by-page plan: title, job, content, layout, visuals, fields, CTA/prompt.
4. Core content: section copy, examples, checklists, worksheets, templates, scoring models, implementation steps.
5. Design spec: cover, typography, colors, callouts, tables, worksheets, page furniture.
6. PDF-specific visuals/treatments from `visual-asset-plan.md`: cover, dividers, matrices, completed examples, blank templates, checklists, implementation maps.
7. Exported PDF and source file.
8. Depth metadata: page count, action-surface count, named tool count, page archetype count, completed example count, blank template count, PDF-specific visual count, render check.

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
5. Visual asset plan from `visual-asset-plan.md`: 12+ unique visual assets or distinct diagram treatments, 8+ VSL-specific visuals not reused from the sales page, no non-logo bitmap repeated on more than 25% of slides, and no recycling the same 3 images as filler.
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
