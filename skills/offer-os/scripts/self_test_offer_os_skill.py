import argparse
import json
from pathlib import Path
import shutil
import subprocess
import sys


SKILL_ROOT = Path(__file__).resolve().parents[1]


SOURCE_CHECKS = [
    {
        "id": "skill_loads_exact_recipes",
        "path": "SKILL.md",
        "needles": [
            "references/exact-build-recipes.md",
            "references/direct-response-framework.md",
            "Start with the Build Controller Recipe",
            "Studio-owned production",
            "scripts/offeros.py",
            "warnings are not shippable",
            "preserve the direct-response hero and buy-box offer-stack contracts exactly",
        ],
    },
    {
        "id": "build_controller_recipe_is_explicit",
        "path": "references/exact-build-recipes.md",
        "needles": [
            "## Build Controller Recipe",
            "plugin-owned OfferOS Studio dispatcher",
            "Do not create `scripts/build_offer_system.*`",
            "Treat validator warnings as build failures in deep mode.",
            "VSL preview mobile",
            "qa-notes.md",
            "Create `copy-plan.json` before `copy.md`, then run `scripts/build_copy.py`.",
            "sectionPlan[].copyBlocks",
            "Apply the Copy Critic rubric",
            "clean `copy.md`, `copy-blueprint.md`, and `sales-page-blueprint.json`",
        ],
    },
    {
        "id": "studio_dispatcher_and_builders_exist",
        "path": "references/exact-build-recipes.md",
        "needles": [
            "## OfferOS Production Studio Recipe",
            "`scripts/offeros.py`",
            "`build_copy.py`",
            "`build_visual_asset_plan.py`",
            "`build_email_sequence.py`",
            "`build_workbook.py`",
            "`build_vsl_deck.js`",
            "quality.copy.studio: \"copy-studio-v1\"",
            "quality.copy.framework: \"modern-brunson-long-form-v1\"",
            "quality.pdf.renderBackend: \"gotenberg-chromium\"",
            "quality.vsl.studio: \"vsl-deck-studio-v1\"",
            "quality.emails.studio: \"email-launch-studio-v1\"",
        ],
    },
    {
        "id": "copy_studio_recipe_is_explicit",
        "path": "references/exact-build-recipes.md",
        "needles": [
            "references/copy-studio-framework.md",
            "references/copy-plan-contract.md",
            "references/copywriter-quality-bar.md",
            "references/copy-critic-rubric.md",
            "references/product-reveal-framework.md",
            "references/feature-benefit-rules.md",
            "references/objection-matrix.md",
            "schema: \"offeros/copy-plan/v1\"",
            "framework: \"modern-brunson-long-form-v1\"",
            "standaloneCopyRequired: true",
            "vslDependency: \"optional-supporting-asset\"",
            "scripts/build_copy.py",
            "finished buyer-facing sales copy",
            "exact-copy-sections-v1",
            "[hero]...[/hero]",
            "1,800+ buyer-facing copy-block words",
            "2,500+ customer-facing words",
            "3,500-5,500",
            "specific epiphany/new insight",
            "feature-benefit-reason rows",
            "value-explained offer-stack items",
            "non-fake urgency basis",
            "quality.copy.studio: \"copy-studio-v1\"",
            "quality.copy.copyCriticPassed: true",
            "quality.copy.hasFeatureBenefitBreakdown: true",
        ],
    },
    {
        "id": "copywriter_quality_refs_exist",
        "path": "references/copywriter-quality-bar.md",
        "needles": [
            "finished buyer-facing copy",
            "Hook, Story/Insight, Offer",
            "The written page must stand alone if the VSL is removed",
            "Forbidden Copy",
            "do not call the video a pitch",
            "Product reveal",
            "Feature-benefit breakdown",
            "Offer stack",
            "FAQ",
        ],
    },
    {
        "id": "copy_critic_rubric_exists",
        "path": "references/copy-critic-rubric.md",
        "needles": [
            "2,500+ customer-facing words",
            "3,500-5,500",
            "can sell if the VSL is removed",
            "If the copy fails, revise `copy-plan.json` first",
            "Do not continue to images or page generation",
        ],
    },
    {
        "id": "visual_asset_plan_recipe_is_explicit",
        "path": "references/exact-build-recipes.md",
        "needles": [
            "## Visual Asset Plan Recipe",
            "`# Visual Asset Plan`",
            "`## Visual Plan Metadata`",
            "visualPlanStage: post-content-blueprint",
            "copyBlueprintUsed: true",
            "copyStudioUsed: true",
            "copyPlanPath: copy-plan.json",
            "salesPageImageSystem: mixed-direct-response-v1",
            "visualKind",
            "copyAnchor",
            "mixed-direct-response-v1",
            "busy fake UI",
            "requiredTool",
            "requiredAction",
            "CALL THE imagegen SKILL/TOOL FOR THIS EXACT ROW",
            "`## PDF Product Visuals`",
            "`## VSL Deck Visuals`",
            "PDF product: 6+ PDF visuals/treatments",
            "VSL deck: 12+ unique visual assets or distinct diagram treatments",
            "3+ ad-specific imagegen creatives",
            "visualReusePolicy",
            "artifact-specific-v1",
            "aspectRatioPolicy: slot-aware-v1",
            "aspectRatioReason",
            "displayIntent",
            "every buyer-facing sales-page image row",
            "data-offeros-page-visual",
            "If the PDF visuals are only sales-page images",
            "If the VSL visuals are only sales-page images",
            "dispatch imagegen visual workers",
            "agentDispatchUsed",
        ],
    },
    {
        "id": "logo_recipe_requires_imagegen_png",
        "path": "references/exact-build-recipes.md",
        "needles": [
            "## Logo Recipe",
            "Call the `imagegen` skill/tool",
            "one final logo direction",
            "Do not create 3 logo files",
            "Do not create any logo or brand asset as SVG",
            "assets/logo.png",
            "--provenance imagegen",
            "includesReadableOfferName",
            "imagegenCompleteLogoLockupAttempted",
            "finalLogoCount",
            "logoGenerationCount",
            "finalLogoLocked",
            "downstreamLogoReference",
            "downstreamImagegenLogoReference",
            "singleFinalLogoOnly",
            "alternateLogosCreated",
            "exactOfferNamePreserved",
            "markNotIllustration",
            "wordmarkTypographyChecked",
            "wordmarkKerningChecked",
            "professionalLockupApproved",
            "output/qa/logo-lockup-preview.png",
            "logoLockup",
            "If any generated logo, brand, ad, page, PDF, VSL, or visual artifact path is `.svg`",
            "If imagegen was not used for the single final complete logo lockup",
            "If the wordmark is just default text pasted beside the mark",
            "If provenance is not `imagegen`, stop and rebuild the generated logo.",
        ],
    },
    {
        "id": "runbook_requires_logo_recipe",
        "path": "references/runbook.md",
        "needles": [
            "Follow the Logo Recipe in `references/exact-build-recipes.md`.",
            "`assets/logo.png`",
            "`brand.logo = \"assets/logo.png\"`",
            "`quality.logo.brandMarkSource = \"imagegen\"`",
            "`quality.logo.includesReadableOfferName = true`",
            "`quality.logo.imagegenCompleteLogoLockupAttempted = true`",
            "`quality.logo.exactOfferNamePreserved = true`",
            "`quality.logo.professionalLockupApproved = true`",
            "`quality.logo.finalLogoLocked = true`",
            "`quality.logo.downstreamLogoReference = \"assets/logo.png\"`",
            "`quality.logo.downstreamImagegenLogoReference = \"assets/logo.png\"`",
            "`quality.logo.alternateLogosCreated = false`",
            "Do not create or register any SVG logo file.",
        ],
    },
    {
        "id": "sales_page_recipe_is_explicit",
        "path": "references/exact-build-recipes.md",
        "needles": [
            "## Sales Page Recipe",
            "`quality.salesPage.pageType` to `direct-response-long-form-vsl`",
            "copy-plan.json",
            "modern-brunson-long-form-v1",
            "optional-supporting-asset",
            "scripts/build_copy.py",
            "references/direct-response-framework.md",
            "`copy-blueprint.md` must include these exact headings",
            "# Section Blueprint",
            "`copy.md` must be clean written long-form sales copy only",
            "copySectionContract: \"exact-copy-sections-v1\"",
            "pageRendersExactCopy: true",
            "typed `copy-plan.json.sectionPlan[].copyBlocks`",
            "must not summarize, rewrite, delete, compress, slice to three cards",
            "direct-response-long-form-v1",
            "framework: \"modern-brunson-long-form-v1\"",
            "pageFramework: \"direct-response-long-form-v1\"",
            "copyStudioUsed: true",
            "copyPlanPath: \"copy-plan.json\"",
            "sales-page-blueprint.json",
            "theme.json",
            "scripts/build_sales_page.py",
            "data-offeros-page-kit=\"v1\"",
            "data-offeros-builder=\"offeros-page-kit-builder-v1\"",
            "data-offeros-vsl-placement=\"main-column-stacked\"",
            "checkoutTarget: \"#checkout\"",
            "orderFormIncluded: false",
            "Use the exact stacked VSL-first hero v2 contract",
            "Use the exact offer-stack buy-box contract",
            "including the separate `agitation`, `failed-alternatives`, `mechanism`, and pre-offer `proof` sections",
            "Proof/demo must appear before the main offer stack",
            "compositionContract: \"direct-response-composition-v2\"",
            "heroContract: \"stacked-vsl-hero-v2\"",
            "heroLayout: \"stacked-vsl\"",
            "heroTemplate: \"offeros-stacked-vsl-v2\"",
            "heroVideoProminenceChecked: true",
            "offerStackContract: \"direct-response-buy-box-v1\"",
            "navigationPolicy: \"no-section-nav\"",
            "iconSystem: \"lucide-icons-v1\"",
            "iconLibrary: \"lucide\"",
            "imageDisplay: \"viewport-constrained-v1\"",
            "buyerFacingImagePolicy: \"imagegen-final-or-provided-v1\"",
            "pageVisualImagegenFinalRequired: true",
            "localCreativeImageFallbackAllowed: false",
            "eyebrowPolicy: \"sparse-key-signposts-v1\"",
            "eyebrowAlignment: \"centered-with-section-heading\"",
            "data-offeros-image-display=",
            "data-lucide",
            "Watch this first",
            "Do not call the VSL a pitch",
            "Hero order is fixed",
            "Use typed section components",
            "The offer-stack component must read `copy-plan.json.offerStack.items`",
            "Do not render the whole offer stack as 10+ identical generic boxes.",
            "Do not use a two-column",
            "2,500 visible words",
            "VSL section becomes a wall of text",
            "at least 7 FAQ objections",
            "at least 4 CTA placements",
            "data-offeros-faq-item",
            "data-offeros-cta",
            "Do not map a repeated sentence over multiple cards.",
        ],
    },
    {
        "id": "direct_response_framework_is_explicit",
        "path": "references/direct-response-framework.md",
        "needles": [
            "## Core Spine",
            "Copy Studio adds the Modern Brunson layer",
            "Message match",
            "Failed alternatives",
            "Unique mechanism",
            "Proof or demonstration",
            "The blueprint is the source of truth",
            "Do not move proof only after the buy box",
            "reads as hero/features/price/FAQ",
        ],
    },
    {
        "id": "page_kit_builder_is_explicit",
        "path": "scripts/build_sales_page.py",
        "needles": [
            "PAGE_KIT_ID = \"offeros-page-kit-v1\"",
            "BUILDER_VERSION = \"offeros-page-kit-builder-v1\"",
            "COPY_FRAMEWORK = \"modern-brunson-long-form-v1\"",
            "DEFAULT_CHECKOUT_TARGET = \"#checkout\"",
            "VSL_PLACEMENT = \"main-column-stacked\"",
            "ALLOWED_PAGE_KIT_ARCHETYPES",
            "ALLOWED_THEME_PRESETS",
            "Unsupported Page Kit archetype",
            "Unsupported Page Kit theme preset",
            "data-offeros-page-kit",
            "data-offeros-builder",
            "data-offeros-vsl-placement",
            "sales-page-blueprint",
            "navigationPolicy",
            "iconSystem",
            "lucide-icons-v1",
            "data-lucide",
            "imageDisplay",
            "buyerFacingImagePolicy",
            "pageVisualImagegenFinalRequired",
            "localCreativeImageFallbackAllowed",
            "preflight_buyer_facing_images",
            "EYEBROW_POLICY = \"sparse-key-signposts-v1\"",
            "EYEBROW_SECTIONS",
            "section_eyebrow",
            "copy_plan_section_rows",
            "copy_plan_offer_stack_items",
            "oo-stack-featured",
            "render_typed_hero",
            "refused to infer section layout from Markdown",
            "copyStudioUsed",
            "orderFormIncluded",
        ],
    },
    {
        "id": "vsl_recipe_is_explicit",
        "path": "references/exact-build-recipes.md",
        "needles": [
            "## VSL Deck Recipe",
            "Create `output/presentation/[slug]-vsl.pptx` as the primary deck. Do not create HTML first.",
            "No layout family may be used on more than 35% of slides.",
            "Visible slide copy must be buyer-facing.",
            "Speaker notes must be recording notes of at least 25 words per slide.",
            "HTML/contact-sheet only after the PPTX exists",
            "Every bitmap image added to the PPTX must preserve aspect ratio.",
            "sizing: { type: fit, w, h }",
            "never to the `.pptx` itself",
            "Browser-test `output/presentation/vsl-preview.html`",
            "quality.vsl.layoutAudit",
            "uniqueVisualAssetCount",
            "vslSpecificVisualAssetCount",
            "maxRepeatedBitmapShare",
            "8+ VSL visuals/treatments must be specific",
            "same large bitmap appears on more than 25% of slides",
        ],
    },
    {
        "id": "pdf_and_email_recipes_are_explicit",
        "path": "references/exact-build-recipes.md",
        "needles": [
            "## PDF Product Recipe",
            "4,000 extracted words",
            "fulfill the `## PDF Product Visuals` section",
            "pdfSpecificVisualAssetCount",
            "generic visible label \"Action Surface\"",
            "namedToolCount",
            "pageArchetypeCount",
            "If extracted text is below the price-point target, revise before QA.",
            "## Email Sequence Recipe",
            "send timing",
            "preview text",
            "campaign role",
            "If two or more body blocks repeat verbatim, revise before QA.",
        ],
    },
    {
        "id": "init_defaults_generated_design",
        "path": "scripts/init_offer_project.py",
        "needles": [
            "default=\"generated\"",
        ],
    },
    {
        "id": "validator_blocks_known_regressions",
        "path": "scripts/validate_offer_outputs.py",
        "needles": [
            "Deep OfferOS runs must not use generated scripts/build_offer_system.* as the production source of truth.",
            "Copy Studio source missing",
            "Copy quality metadata must record {field}: {expected}.",
            "copy.md exists but sales-copy artifact provenance is not copy-studio-v1",
            "copy.md is too thin for long-form sales copy",
            "Sales copy quality failed",
            "copy-plan.json copyBlocks contain only",
            "finishedCopySource",
            "copyCriticPassed",
            "copy-plan.sectionPlan must place proof/demo before offer-stack",
            "Product reveal component",
            "Offer stack item",
            "sales-page-studio-v1",
            "email-launch-studio-v1",
            "pdf-workbook-studio-v1",
            "gotenberg-chromium",
            "vsl-deck-studio-v1",
            "editableTextChecked",
            "actualPdfRenderChecked",
            "renderedPageImageCount",
            "Deep OfferOS runs must not create or register SVG artifacts.",
            "OfferOS generated runs must not create or register SVG logo files.",
            "Logo quality metadata must confirm svgAssetCreated: false.",
            "Logo quality metadata must confirm finalLogoLocked.",
            "Logo quality metadata must record downstreamLogoReference: assets/logo.png.",
            "Logo quality metadata must record downstreamImagegenLogoReference: assets/logo.png.",
            "Visual asset plan must not ask imagegen to generate/redraw/reinvent logos or wordmarks",
            "Deep generated-design runs must register the primary logo with provenance: imagegen.",
            "includesReadableOfferName",
            "exactOfferNamePreserved",
            "professionalLockupApproved",
            "imagegenCompleteLogoLockupAttempted",
            "finalLogoCount",
            "logoGenerationCount",
            "Primary logo artifact cannot point at a mark-only file",
            "Logo generationTool must record imagegen-single-final-logo.",
            "brand.logo must match the registered primary logo artifact path.",
            "Primary logo bitmap must be a horizontal lockup",
            "Sales page contains repeated boilerplate copy",
            "Visual asset plan missing",
            "final buyer-facing pixels from imagegen",
            "localCreativeOverlay",
            "Pillow/PIL-generated image artifacts are not allowed in OfferOS deep runs",
            "Sales-page product bundle image",
            "Hero/VSL thumbnail image",
            "Sales-page support visual image",
            "Sales-page visual plan row must explicitly set requiredTool: imagegen",
            "Sales-page visual generationPrompt must directly instruct CALL THE imagegen SKILL/TOOL FOR THIS EXACT ROW",
            "hasArtifactSpecificPlan",
            "visualPlanStage: post-content-blueprint",
            "copyBlueprintUsed",
            "salesPageImageSystem: mixed-direct-response-v1",
            "primaryConversionFinalPixelsPolicy: imagegen-final-v1",
            "aspectRatioPolicy: slot-aware-v1",
            "Sales-page visual plan must use slot-aware varied aspect ratios",
            "imagegen-final",
            "finalPixelsGeneratedBy: imagegen",
            "localCreativeOverlay: false",
            "buyerFacingImagePolicy: imagegen-final-or-provided-v1",
            "pageVisualImagegenFinalRequired",
            "localCreativeImageFallbackAllowed: false",
            "fields tied to copy sections",
            "Sales-page visual plan is all mockup/UI-style visuals",
            "PDF-specific visual asset/treatment count below target",
            "VSL-specific visual asset/treatment count below target",
            "compositionContract",
            "stacked-vsl-hero-v2",
            "direct-response-long-form-v1",
            "Copy blueprint Section Blueprint",
            "Direct-response page sections must follow the required persuasion order",
            "Direct-response proof/demo section must appear before the main offer stack",
            "heroLayout: stacked-vsl",
            "heroVideoProminenceChecked",
            "Direct-response hero must not use a two-column/split SaaS layout",
            "Direct-response long-form sales pages must not include a nav menu",
            "Post-hero VSL section must not say",
            "data-offeros-image-display=",
            "Direct-response sales page must include Lucide icon markers via data-lucide.",
            "iconLibrary: lucide",
            "eyebrowPolicy: sparse-key-signposts-v1",
            "Direct-response Page Kit must use sparse section eyebrows/pills",
            "data-offeros-hero-layout=\"stacked-vsl\"",
            "VSL setup section is too text-heavy",
            "data-offeros-faq-item",
            "data-offeros-cta",
            "Direct-response hero must include a VSL/video frame marked data-offeros-hero-video",
            "Direct-response offer stack must include a deliverable checklist marked data-offeros-offer-checklist",
            "Deep sales pages must be built by OfferOS Page Kit",
            "data-offeros-builder=\"offeros-page-kit-builder-v1\"",
            "data-offeros-vsl-placement=\"main-column-stacked\"",
            "Sales page must not contain an order form or checkout form",
            "href=\"#checkout\"",
            "pageKitBlueprintUsed",
            "themeTokensUsed",
            "orderFormIncluded: false",
            "Facebook ads contain repeated boilerplate copy",
            "Email sequence contains repeated boilerplate copy",
            "PDF extracted text is light for a paid product",
            "PDF repeats generic 'Action Surface' labels",
            "PDF named tool/template count below target",
            "VSL deck exposes internal stage labels",
            "VSL deck preview must be browser-safe HTML or image",
            "VSL speaker notes are too thin",
            "VSL speaker notes mention prices that differ from manifest.price",
            "VSL PPTX image aspect ratio distortion detected",
            "VSL deck repeats the same large bitmap too often",
            "Cannot validate VSL PPTX image aspect ratios because Pillow is unavailable",
            "layoutAudit",
            "VSL repeats one layout too often",
            "QA notes contain stale PDF page-count claims",
            "QA notes record browser horizontal overflow",
        ],
    },
    {
        "id": "agent_dispatch_supports_imagegen_workers",
        "path": "references/agent-dispatch.md",
        "needles": [
            "### Imagegen Visual Workers",
            "after the initial offer architecture, `design.md`, final logo lockup, `assets/logo.png`, `copy-plan.json`, clean `copy.md`, internal `copy-blueprint.md`, `sales-page-blueprint.json`, and `visual-asset-plan.md` v2 exist",
            "copyAnchor",
            "visualKind",
            "mixed-direct-response-v1",
            "Page visual worker",
            "PDF visual worker",
            "VSL visual worker",
            "Ad visual worker",
            "use the `imagegen` skill/tool",
            "The main agent owns integration",
        ],
    },
]


EXPECTED_BAD_WORKSPACE_ISSUES = [
    "must not create or register SVG",
    "provenance: imagegen",
    "valid pageType",
    "Sales page contains repeated boilerplate copy",
    "Facebook ads contain repeated boilerplate copy",
    "VSL deck exposes internal stage labels",
]


def source_check() -> list[dict]:
    results = []
    for check in SOURCE_CHECKS:
        path = SKILL_ROOT / check["path"]
        if not path.exists():
            results.append({"id": check["id"], "ok": False, "missingFile": check["path"]})
            continue
        text = path.read_text(encoding="utf-8", errors="ignore")
        missing = [needle for needle in check["needles"] if needle not in text]
        results.append({"id": check["id"], "ok": not missing, "missing": missing})
    return results


def run_validator(workspace: Path) -> dict:
    validator = SKILL_ROOT / "scripts" / "validate_offer_outputs.py"
    completed = subprocess.run(
        [
            sys.executable,
            str(validator),
            "--workspace",
            str(workspace),
            "--manifest",
            "offer-os.json",
            "--strict",
            "--no-write",
        ],
        text=True,
        capture_output=True,
        check=False,
    )
    try:
        payload = json.loads(completed.stdout)
    except json.JSONDecodeError:
        payload = {"parseError": True, "stdout": completed.stdout, "stderr": completed.stderr}
    payload["returncode"] = completed.returncode
    return payload


def bad_workspace_check(workspace: Path) -> dict:
    payload = run_validator(workspace)
    issue_text = "\n".join(payload.get("issues", []))
    missing = [expected for expected in EXPECTED_BAD_WORKSPACE_ISSUES if expected not in issue_text]
    return {
        "workspace": str(workspace),
        "ok": payload.get("returncode") != 0 and not missing,
        "validatorOk": payload.get("ok"),
        "issueCount": payload.get("issueCount"),
        "missingExpectedIssues": missing,
        "issues": payload.get("issues", []),
    }

def synthetic_visual_plan_regression() -> dict:
    expected = [
        "Visual asset plan v2 requires copy-blueprint.md",
        "Visual asset plan metadata must include visualPlanStage: post-content-blueprint.",
        "Visual asset plan metadata must include copyStudioUsed: true.",
        "Visual asset plan metadata must include copyPlanPath: copy-plan.json.",
        "Image quality metadata must record visualPlanStage: post-content-blueprint.",
        "Image quality metadata must confirm copyBlueprintUsed.",
        "Image quality metadata must confirm copyStudioUsed.",
        "Image quality metadata must record copyPlanPath: copy-plan.json.",
        "Image quality metadata must record salesPageImageSystem: mixed-direct-response-v1.",
        "Image quality metadata must record aspectRatioPolicy: slot-aware-v1.",
        "Sales-page visual plan must include 4+ copyAnchor fields",
        "Sales-page visual plan must use slot-aware varied aspect ratios",
        "Sales-page visual plan is all mockup/UI-style visuals",
    ]
    workspace = SKILL_ROOT / "tests" / "fixtures" / "bad-visual-plan"
    payload = run_validator(workspace)
    issue_text = "\n".join(payload.get("issues", []))
    missing = [item for item in expected if item not in issue_text]
    return {
        "id": "synthetic_visual_plan_regression",
        "ok": payload.get("returncode") != 0 and not missing,
        "missingExpectedIssues": missing,
        "issueCount": payload.get("issueCount"),
    }


def synthetic_copy_studio_regression() -> dict:
    expected = [
        'copy-plan.json must record framework: "modern-brunson-long-form-v1"',
        "copy-plan.json must set standaloneCopyRequired: true.",
        'copy-plan.json must set vslDependency: "optional-supporting-asset".',
        "uniqueMechanism must include a named mechanism.",
        "proofPlan.proofBeforeOffer must be true.",
        "productReveal.coreComponents must include 3+ feature-benefit-reason rows.",
        "objectionMatrix must include 7+ objections.",
        "urgencyBasis.fakeUrgency must be false.",
        "sectionPlan must place proof before offer-stack.",
        "copy.md exists but sales-copy artifact provenance is not copy-studio-v1",
        "Copy blueprint missing",
        "Copy quality metadata must record studio: copy-studio-v1.",
        "productReveal.coreComponents[1] missing benefit.",
        "offerStack.items[1] must include title and buyer-facing value copy.",
    ]
    workspace = SKILL_ROOT / "tests" / "fixtures" / "bad-copy-studio"
    payload = run_validator(workspace)
    issue_text = "\n".join(payload.get("issues", []))
    missing = [item for item in expected if item not in issue_text]
    return {
        "id": "synthetic_copy_studio_regression",
        "ok": payload.get("returncode") != 0 and not missing,
        "missingExpectedIssues": missing,
        "issueCount": payload.get("issueCount"),
    }


def synthetic_two_column_hero_regression() -> dict:
    expected = [
        "Direct-response sales page quality metadata must record heroContract: stacked-vsl-hero-v2.",
        "Direct-response sales page quality metadata must record heroTemplate: offeros-stacked-vsl-v2.",
        "Direct-response sales page quality metadata must record heroVideoFrame: large-16x9.",
        "Direct-response sales page quality metadata must record heroLayout: stacked-vsl.",
        "Direct-response sales page quality metadata must confirm heroVideoProminenceChecked.",
            "Direct-response sales page quality metadata must record framework: modern-brunson-long-form-v1.",
            "Direct-response sales page quality metadata must record pageFramework: direct-response-long-form-v1.",
            "Direct-response sales page quality metadata must confirm copyStudioUsed.",
        "Direct-response sales page quality metadata must record compositionContract: direct-response-composition-v2.",
        "Direct-response hero must use data-offeros-hero-layout=\"stacked-vsl\".",
        "Direct-response hero must use data-offeros-hero-contract=\"stacked-vsl-hero-v2\".",
        "Direct-response hero must use data-offeros-template=\"offeros-stacked-vsl-v2\".",
        "Direct-response hero must include a centered copy stack marked data-offeros-hero-copy-stack.",
        "Direct-response hero must not use a two-column/split SaaS layout",
        "Direct-response hero video must be marked data-offeros-hero-video-prominence=\"primary\".",
    ]
    workspace = SKILL_ROOT / "tests" / "fixtures" / "bad-two-column-hero"
    payload = run_validator(workspace)
    issue_text = "\n".join(payload.get("issues", []))
    missing = [item for item in expected if item not in issue_text]
    return {
        "id": "synthetic_two_column_hero_regression",
        "ok": payload.get("returncode") != 0 and not missing,
        "missingExpectedIssues": missing,
        "issueCount": payload.get("issueCount"),
    }


def synthetic_product_page_regression() -> dict:
    expected = [
        "Copy blueprint missing",
        "Direct-response page sections must follow the required persuasion order",
        "Direct-response proof/demo section must appear before the main offer stack.",
        "Direct-response page has thin required sections",
        "Direct-response failed-alternatives section must include a table or contrast block",
        "Direct-response mechanism section must include a named mechanism step/framework block",
        "Direct-response proof section must include 2+ proof/demo cards",
        "Direct-response long-form VSL page must include 3+ post-hero CTA elements marked data-offeros-post-hero-cta",
    ]
    workspace = SKILL_ROOT / "tests" / "fixtures" / "bad-product-page"
    payload = run_validator(workspace)
    issue_text = "\n".join(payload.get("issues", []))
    missing = [item for item in expected if item not in issue_text]
    return {
        "id": "synthetic_product_page_regression",
        "ok": payload.get("returncode") != 0 and not missing,
        "missingExpectedIssues": missing,
        "issueCount": payload.get("issueCount"),
    }


def synthetic_page_kit_regression() -> dict:
    expected = [
        'Deep sales pages must be built by OfferOS Page Kit and declare data-offeros-page-kit="v1".',
        'Deep sales pages must declare data-offeros-builder="offeros-page-kit-builder-v1".',
        'Deep sales pages must declare data-offeros-vsl-placement="main-column-stacked".',
        "Sales page must not contain an order form or checkout form",
        'Sales page must include at least one data-offeros-cta link to the checkout placeholder href="#checkout".',
        'Offer-stack purchase CTA must link to the checkout placeholder href="#checkout".',
        "Sales page CTAs must not target on-page order/payment form anchors",
        "Direct-response hero must not use a two-column/split SaaS layout",
        "Direct-response sales page quality metadata must record iconLibrary: lucide.",
    ]
    workspace = SKILL_ROOT / "tests" / "fixtures" / "bad-page-kit-handwritten"
    payload = run_validator(workspace)
    issue_text = "\n".join(payload.get("issues", []))
    missing = [item for item in expected if item not in issue_text]
    return {
        "id": "synthetic_page_kit_regression",
        "ok": payload.get("returncode") != 0 and not missing,
        "missingExpectedIssues": missing,
        "issueCount": payload.get("issueCount"),
    }


def synthetic_svg_artifact_regression() -> dict:
    expected = [
        "Deep OfferOS runs must not create or register SVG artifacts.",
    ]
    workspace = SKILL_ROOT / "tests" / "fixtures" / "bad-svg-artifact"
    payload = run_validator(workspace)
    issue_text = "\n".join(payload.get("issues", []))
    missing = [item for item in expected if item not in issue_text]
    return {
        "id": "synthetic_svg_artifact_regression",
        "ok": payload.get("returncode") != 0 and not missing,
        "missingExpectedIssues": missing,
        "issueCount": payload.get("issueCount"),
    }


def synthetic_logo_drift_regression() -> dict:
    expected = [
        "Logo quality metadata must confirm finalLogoLocked.",
        "Logo quality metadata must record downstreamLogoReference: assets/logo.png.",
        "Logo quality metadata must record downstreamImagegenLogoReference: assets/logo.png.",
        "Logo quality metadata must confirm singleFinalLogoOnly.",
        "Logo quality metadata must confirm alternateLogosCreated: false.",
        "Logo quality metadata must record finalLogoCount: 1",
        "Logo quality metadata must record logoGenerationCount: 1",
        "Visual asset plan must not ask imagegen to generate/redraw/reinvent logos or wordmarks",
        "Visual asset plan must not reference rejected, old, or alternate logos",
    ]
    workspace = SKILL_ROOT / "tests" / "fixtures" / "bad-logo-drift"
    payload = run_validator(workspace)
    issue_text = "\n".join(payload.get("issues", []))
    missing = [item for item in expected if item not in issue_text]
    return {
        "id": "synthetic_logo_drift_regression",
        "ok": payload.get("returncode") != 0 and not missing,
        "missingExpectedIssues": missing,
        "issueCount": payload.get("issueCount"),
    }


def synthetic_code_rendered_creative_regression() -> dict:
    expected = [
        "Image artifact has invalid provenance 'pil-generated'",
        "Pillow/PIL-generated image artifacts are not allowed",
        "Generated-design deep runs must create primary conversion visuals with final buyer-facing pixels from imagegen",
        "local overlays cannot satisfy product bundle",
        "uses imagegen-composite without imagegenNativeComposite: true",
        "must record finalPixelsGeneratedBy: imagegen",
        "must record localCreativeOverlay: false",
        "localPostprocess contains creative operations",
        "Sales-page support visual image must use source/provenance imagegen-final",
    ]
    workspace = SKILL_ROOT / "tests" / "fixtures" / "bad-code-rendered-creative"
    payload = run_validator(workspace)
    issue_text = "\n".join(payload.get("issues", []))
    missing = [item for item in expected if item not in issue_text]
    return {
        "id": "synthetic_code_rendered_creative_regression",
        "ok": payload.get("returncode") != 0 and not missing,
        "missingExpectedIssues": missing,
        "issueCount": payload.get("issueCount"),
    }


def synthetic_generated_controller_regression() -> dict:
    expected = [
        "Deep OfferOS runs must not use generated scripts/build_offer_system.* as the production source of truth.",
        "Studio quality metadata says usesGeneratedBuildOfferSystem=true",
    ]
    workspace = SKILL_ROOT / "tests" / "fixtures" / "bad-generated-controller"
    payload = run_validator(workspace)
    issue_text = "\n".join(payload.get("issues", []))
    missing = [item for item in expected if item not in issue_text]
    return {
        "id": "synthetic_generated_controller_regression",
        "ok": payload.get("returncode") != 0 and not missing,
        "missingExpectedIssues": missing,
        "issueCount": payload.get("issueCount"),
    }


def synthetic_page_kit_builder_rejects_unapproved_sources() -> dict:
    builder = SKILL_ROOT / "scripts" / "build_sales_page.py"
    workspace = SKILL_ROOT / "tests" / "fixtures" / "bad-page-kit-unapproved-source"
    completed = subprocess.run(
        [
            sys.executable,
            str(builder),
            "--workspace",
            str(workspace),
            "--manifest",
            "offer-os.json",
            "--blueprint",
            "sales-page-blueprint.json",
            "--theme",
            "theme.json",
            "--output",
            "index.html",
        ],
        text=True,
        capture_output=True,
        check=False,
    )
    combined = f"{completed.stdout}\n{completed.stderr}"
    return {
        "id": "synthetic_page_kit_builder_rejects_unapproved_sources",
        "ok": completed.returncode != 0 and "Unsupported Page Kit archetype" in combined,
        "returncode": completed.returncode,
        "expected": "Unsupported Page Kit archetype",
    }


def good_hyrox_copy_plan() -> dict:
    sections = {
        "hero": [
            ("prehead", "For HYROX athletes who can train hard but still fade when running starts after heavy stations."),
            ("headline", "Build the race engine that still works after the sleds."),
            ("lead", "HYROX does not punish athletes because they lack toughness. It punishes the gap between fresh training numbers and compromised execution. HYROX Engine gives you a 21-day plan for holding pace after station fatigue, recovering fast enough to keep moving, and arriving at race day with a rehearsed sequence instead of another random hard week."),
            ("paragraph", "You get a practical race-specific plan, pacing tools, station cues, benchmark trackers, and race-week guidance that fit normal gym access. The goal is not to make training more brutal. The goal is to make the final third of the race feel planned."),
            ("cta", "Get HYROX Engine for $27 and start the first session today."),
        ],
        "vsl": [
            ("headline", "The short breakdown shows why strong athletes still fall apart late."),
            ("paragraph", "The video is a quick overview of the logic, but the full argument is here in writing. You will see why fresh running sessions do not predict race-day pacing, why stations change the next kilometer, and how the Compromised Engine Ladder trains the exact transition pattern that decides whether you keep moving or start negotiating with yourself."),
        ],
        "problem": [
            ("headline", "You are fit in pieces. HYROX tests everything together."),
            ("paragraph", "Most HYROX prep looks sensible on paper. There are run intervals, heavy sled days, lunges, farmer carries, wall balls, and conditioning circuits. The problem is that race day does not grade those pieces separately. It asks whether your run still has shape after the sled push, whether your grip still behaves after carries, and whether your breathing settles quickly enough to make the next station controlled."),
            ("paragraph", "That is why a good gym week can still produce a poor race simulation. You are not failing because you skipped suffering. You are failing because the sessions never taught the body what to do after the previous station damaged the next movement."),
        ],
        "agitation": [
            ("headline", "Race day becomes expensive feedback when training stays disconnected."),
            ("paragraph", "The worst part is not just losing time. It is discovering the gap after entry fees, travel, taper, and weeks of effort have already been spent. The first kilometer feels fine, the first station feels manageable, then the plan starts leaking. Splits drift, transitions get messy, grip changes your posture, and the final wall balls become survival instead of execution."),
            ("paragraph", "When the next training block repeats the same scattered pattern, the same race-day lesson repeats too. More effort gets added, but the missing link remains untrained."),
        ],
        "failed-alternatives": [
            ("headline", "The usual fixes make sense until they meet compromised running."),
            ("paragraph", "Adding mileage can raise your aerobic ceiling, but it does not teach you to run after a sled. Random grinders prove you can suffer, but they do not give you pacing decisions. Copying elite workouts can look impressive, yet it often ignores your current level, equipment access, and the exact station sequence that makes your race fall apart."),
            ("paragraph", "What you need is not another heroic session. You need a short ladder that starts with a pace floor, adds station pressure, and finishes with race execution so every week has a job."),
        ],
        "new-insight": [
            ("headline", "The missing link is not fitness. It is recovery control under station pressure."),
            ("paragraph", "Fresh fitness is only one part of HYROX. The deciding skill is how quickly you regain usable rhythm after a station changes your legs, breathing, grip, or posture. Once you train that rhythm deliberately, the race stops feeling like eight surprise collapses and starts feeling like a repeated pattern you have already rehearsed."),
            ("paragraph", "That is the epiphany behind HYROX Engine: do not chase more punishment first. Build the compromised engine that can return to pace after damage."),
        ],
        "mechanism": [
            ("headline", "The Compromised Engine Ladder trains the race in the order your body feels it."),
            ("paragraph", "The Compromised Engine Ladder is a three-step progression. First, you set a sustainable 1km pace floor so you know what controlled effort feels like. Second, you add station pressure in measured doses so your next run has a target instead of guesswork. Third, you lock race execution with sessions that combine transitions, pacing, and recovery cues before taper week."),
            ("paragraph", "This works because HYROX performance is not one maximal effort. It is repeated recovery from specific stress. The ladder lets you practice that recovery without burying yourself under random fatigue."),
        ],
        "proof": [
            ("headline", "You can inspect the plan before you trust it."),
            ("paragraph", "The proof is in the structure. Week one creates the pace floor and baseline station cues. Week two adds compromised running after station demands. Week three sharpens transitions, taper rhythm, and race-day decision rules. You can open the sample week, pace calculator, tracker, and station cue cards before you ever start."),
            ("paragraph", "There are no mystery workouts hiding behind motivation language. Every session has a purpose, target, station focus, and adjustment note so you can see why it exists."),
        ],
        "before-after": [
            ("headline", "Before, every hard session feels like progress. After, every session has a race-day job."),
            ("paragraph", "Before HYROX Engine, you can finish a brutal workout and still wonder whether it helped. After HYROX Engine, the session tells you what it is training: pace floor, station pressure, transition control, or race execution. That gives you a cleaner way to judge progress than sweat alone."),
        ],
        "product": [
            ("headline", "Introducing HYROX Engine in 21 Days."),
            ("paragraph", "HYROX Engine is a PDF training plan and race-day implementation kit for recreational and competitive HYROX athletes who want a practical final-block structure without hiring a private coach. It gives you a 21-day plan, pacing calculator, station cue cards, benchmark tracker, race-week taper guide, and action guarantee tracker in one package."),
            ("paragraph", "It is built for athletes with normal gym access. If you can run, use common conditioning equipment, and scale station work when needed, the plan gives you the structure to connect those pieces into one race-specific block."),
        ],
        "feature-benefit": [
            ("headline", "Here is what each part actually does for you."),
            ("paragraph", "The 21-day plan gives every week a job so training stops becoming a random collection of hard sessions. The pace calculator turns target finish time into repeatable kilometer targets. The station cue cards make technique reminders simple when fatigue is high. The benchmark tracker shows whether you are gaining control, not just collecting exhaustion."),
            ("paragraph", "The race-week guide keeps the final days from becoming panic training. The substitutions help you adapt sessions to a normal gym. The action tracker makes the guarantee fair because it shows the work completed and the confidence gained."),
        ],
        "how-it-works": [
            ("headline", "Open the kit, set your pace, then follow the ladder."),
            ("paragraph", "Start by setting your target pace and baseline station level. Then follow week one to establish the pace floor. In week two, add station pressure with controlled compromised runs. In week three, reduce noise, sharpen transitions, and rehearse the decisions you will make on race day."),
            ("paragraph", "Each session gives you the focus, target, scaling note, and completion marker. You are never left staring at a template wondering how hard it should be."),
        ],
        "offer-stack": [
            ("headline", "Get the complete 21-day HYROX Engine stack today."),
            ("paragraph", "The core plan gives you the training sequence. The calculator gives you pacing numbers. The station cards give you execution reminders. The benchmark tracker gives you feedback. The race-week guide protects the taper. The substitution sheet keeps normal gym limitations from becoming an excuse. The checklist gives race morning order. The guarantee tracker makes the outcome inspectable."),
            ("paragraph", "Together, those pieces create a short, focused race block instead of another folder of disconnected workouts."),
            ("cta", "Get instant access to HYROX Engine for $27."),
        ],
        "bonuses": [
            ("headline", "The accelerators make the plan easier to use under pressure."),
            ("paragraph", "You also get printable station cards, a race-day checklist, and a simple pace review sheet. They are not filler bonuses. They exist because the best plan still fails if the athlete forgets cues, overtrains during taper week, or reaches race morning without a repeatable setup routine."),
        ],
        "pricing": [
            ("headline", "$27 today is less than one drop-in class and clearer than another week of guessing."),
            ("paragraph", "A single compromised training block can protect months of preparation from turning into race-day confusion. You are not paying for generic fitness advice. You are paying for a short sequence, usable tools, and a clear next three weeks."),
        ],
        "guarantee": [
            ("headline", "Use the 12-Workout Action Guarantee."),
            ("paragraph", "Complete at least 12 workouts in 21 days and use the tracker. If you do not feel more confident holding pace under fatigue, send the completed tracker within 30 days and get a refund. The guarantee is fair because the plan is designed around action, not passive reading."),
        ],
        "fit": [
            ("headline", "This is for athletes who want structure, not another punishment contest."),
            ("paragraph", "HYROX Engine is for you if you already train, understand the basics, and want the next block to connect running, stations, pacing, and race-week decisions. It is not for someone who wants a bodybuilding split, a full beginner fitness course, or a private coach watching every session."),
        ],
        "faq": [
            ("headline", "Questions before you start."),
            ("paragraph", "The common questions are practical: level, equipment, timing, fatigue, scaling, refund terms, and whether a PDF can be enough. Each answer below is designed to help you decide whether this kit matches your current race prep."),
            ("paragraph", "Read these as decision checks, not decoration. If the plan fits your level, your equipment, and your race timeline, you can start quickly. If you need daily coaching, medical guidance, or a full beginner fitness education, the honest answer is to choose a different kind of support."),
            ("paragraph", "The right buyer should finish the FAQ knowing what happens on day one, how to scale the work, where the risk reversal applies, and why the kit is different from another downloaded workout list. That clarity protects the sale and prevents the final decision from depending on hype."),
        ],
        "final-cta": [
            ("headline", "Start the next 21 days with a plan instead of another random session."),
            ("paragraph", "If your HYROX prep already proves you can work hard, the next step is to make that work race-specific. Get the plan, set the pace floor, train the compromised engine, and arrive at race day with a sequence you have practiced."),
            ("cta", "Get HYROX Engine for $27."),
        ],
    }

    section_expansions = {
        "hero": "That matters because the athlete already has work capacity. The sale is not promising magic speed. It is promising a clearer final block where running, stations, and recovery cues finally point at the same race-day outcome.",
        "vsl": "A reader still gets the whole decision in writing. The video can make the idea easier to absorb, but the athlete should understand the diagnosis, the ladder, the product, the stack, and the guarantee without pressing play.",
        "problem": "The buyer recognizes this because the training log looks busy while race confidence stays unstable. Their effort is real, but the relationship between one station and the next kilometer has never been trained as its own skill.",
        "agitation": "That uncertainty changes behavior. Athletes either overtrain because they do not trust the plan, or they arrive hoping adrenaline solves a problem that should have been rehearsed weeks earlier.",
        "failed-alternatives": "Each alternative contains a useful piece, which is why the buyer keeps returning to them. The problem is that none of them alone connects fresh capacity to compromised execution in the order HYROX demands.",
        "new-insight": "Once the buyer sees the race as repeated recovery from specific station stress, the training choice becomes simpler. The next block should train that recovery loop instead of merely proving discipline.",
        "mechanism": "The ladder also gives the athlete a way to scale without losing the purpose. A beginner and an advanced racer can use different numbers while still training the same pace-pressure-execution sequence.",
        "proof": "This is the strongest proof available without pretending to have testimonials. The buyer can inspect the product logic, sample structure, and tracker before trusting the promise, which is more honest than vague claims.",
        "before-after": "The emotional change is important too. The athlete stops asking whether the last brutal circuit was enough and starts asking whether the right race-day skill improved.",
        "product": "The deliverable is intentionally practical. It can be printed, opened on a phone, taken to the gym, and used during the exact weeks when vague motivation usually creates the most noise.",
        "feature-benefit": "Those details make the kit feel tangible. The buyer is not imagining a folder of inspirational PDFs; they are seeing tools that answer the questions that usually derail the final block.",
        "how-it-works": "The sequence is short enough to begin today and structured enough to remove guessing. The athlete knows what to do first, what to measure, what to scale, and when to stop adding noise.",
        "offer-stack": "The stack is designed so every item has a job. If a deliverable does not help the athlete train, decide, track, taper, or execute, it does not belong in the offer.",
        "bonuses": "The bonus value is convenience under fatigue. Anything that reduces gym friction, decision clutter, or race-week uncertainty has a real role in helping the athlete complete the plan.",
        "pricing": "That makes the price easy to understand. The buyer is not comparing the kit against a free workout online; they are comparing it against the cost of another unfocused week before race day.",
        "guarantee": "The guarantee also filters for the right buyer. It rewards the person willing to do the sessions and track the work, not someone who wants confidence without action.",
        "fit": "That fit line protects the offer. A self-directed athlete gets structure and tools, while someone needing medical advice, total beginner instruction, or daily coaching knows this is not the right product.",
        "faq": "The answers should reduce practical friction, not dodge it. A strong FAQ helps the athlete decide whether the plan matches their level, gym, race timeline, and preferred way of training.",
        "final-cta": "The close brings the decision back to the next workout. The athlete can keep collecting hard sessions, or they can start a defined 21-day block with targets, cues, and a fair guarantee.",
    }

    section_depth_fillers = {
        "mechanism": "The important detail is that the ladder changes one variable at a time. That keeps the athlete from confusing exhaustion with progress. Pace comes first, station pressure comes second, and race execution comes third, so the buyer can understand why the system is different from another brutal conditioning circuit.",
        "product": "The buyer should be able to picture the product before the offer stack appears: a plan they open before training, tools they use during sessions, trackers they complete after sessions, and race-week guidance they follow when nerves usually create bad decisions. It is sold as a usable training kit, not as theory, so the copy must make the product feel openable, printable, and immediately actionable.",
        "feature-benefit": "Each component earns its place by removing a specific source of race-prep uncertainty. The plan removes programming uncertainty, the calculator removes pacing uncertainty, the cue cards remove station uncertainty, the tracker removes progress uncertainty, and the race-week guide removes taper uncertainty. That feature-benefit chain is what stops the product reveal from becoming a bland list of PDFs and makes every deliverable feel tied to a race-day decision. The athlete should know exactly how each piece changes the next workout and the next race-day decision.",
        "how-it-works": "The first action is simple enough to begin without a coaching call: pick the level, set the pace, and complete the first session. The later actions build on that evidence, so the athlete is not asked to trust an abstract plan while training decisions remain vague.",
        "offer-stack": "The value is cumulative because the pieces work together. A plan without pacing numbers is vague. Pacing numbers without station cues are fragile. Station cues without a tracker are hard to judge. A tracker without race-week guidance still leaves the final days exposed. The stack copy must therefore explain the job of each item instead of naming files and hoping the buyer imagines the value. It should make the bundle feel like one practical race-prep system that removes friction before, during, and after training, right through race morning and final execution confidence.",
        "pricing": "That comparison keeps the $27 decision grounded. One more drop-in class can make the athlete tired; this gives the next three weeks a clearer structure and gives every session a reason to exist.",
        "guarantee": "The refund terms also make the promise more believable. The buyer is not asked to accept a vague confidence claim. They complete visible work, track the sessions, and judge whether the plan improved confidence under fatigue.",
        "faq": "The FAQ is part of the selling argument, not a support afterthought. It handles practical reasons a good-fit athlete might delay: current level, equipment, short timeline, coaching overlap, missed sessions, product depth, and refund terms.",
        "final-cta": "The decision is deliberately small and concrete. Start the block, complete the sessions, track the work, and use the guarantee if honest action does not create more confidence under fatigue.",
    }

    faq_blocks = [
        ("question", "What if I am not advanced enough for HYROX-specific work?"),
        ("answer", "The plan includes scalable paths and substitution notes. You need basic training experience, not elite numbers, because the first job is finding your pace floor and applying station pressure responsibly."),
        ("question", "What if my gym does not have every HYROX station setup?"),
        ("answer", "The substitution sheet gives practical swaps for normal gyms so you can train the pressure pattern without needing a perfect race venue or dedicated HYROX facility."),
        ("question", "Can a 21-day block really help if I am already close to race day?"),
        ("answer", "The block is not trying to build years of base fitness. It sharpens the specific connection between running, stations, transitions, and taper decisions that often breaks late."),
        ("question", "Is this just another hard workout PDF?"),
        ("answer", "No. Each week has a job, each session has a target, and the tools connect pace, station fatigue, tracking, and race-week execution instead of dumping random workouts on you."),
        ("question", "What if I already have a coach?"),
        ("answer", "Use this only if it complements your coach's plan. The kit is best for self-directed athletes or as a structured final-block reference, not as a replacement for medical or individualized coaching."),
        ("question", "What if I miss a session during the 21 days?"),
        ("answer", "The tracker helps you recover the sequence without pretending missed work disappeared. You adjust the next session around the purpose of the week instead of chasing guilt volume."),
        ("question", "What if I do the work and still do not feel ready?"),
        ("answer", "That is why the 12-Workout Action Guarantee exists. Complete the tracked work and ask for a refund if confidence under fatigue does not improve after honest use."),
    ]

    def section_row(section_id: str, role: str, visual: str, cta_role: str = "none") -> dict:
        blocks = [{"type": block_type, "text": text} for block_type, text in sections[section_id]]
        blocks.append({"type": "paragraph", "text": section_expansions[section_id]})
        if section_id in section_depth_fillers:
            blocks.append({"type": "paragraph", "text": section_depth_fillers[section_id]})
        if section_id == "faq":
            blocks.extend({"type": block_type, "text": text} for block_type, text in faq_blocks)
        blocks.append(
            {
                "type": "paragraph",
                "text": (
                    f"In the {role} part of the decision, the athlete is choosing between another hard session "
                    "that may not transfer and a short block where the next workout has a race-day purpose. "
                    f"That {section_id} contrast keeps the copy concrete instead of drifting into generic fitness advice."
                ),
            }
        )
        return {
            "sectionId": section_id,
            "frameworkRole": role,
            "conversionJob": f"Move the HYROX buyer through the {section_id} belief step with concrete race-prep copy.",
            "buyerBeliefBefore": "Hard training should be enough if effort is high.",
            "buyerBeliefAfter": "Race-specific structure matters more than adding another random hard session.",
            "primaryClaim": sections[section_id][0][1],
            "proofOrSupport": "Uses the HYROX Engine offer architecture, sample week, pace calculator, and action guarantee.",
            "copyBlocks": blocks,
            "visualNeed": visual,
            "ctaRole": cta_role,
            "maxWords": 320,
        }

    return {
        "schema": "offeros/copy-plan/v1",
        "framework": "modern-brunson-long-form-v1",
        "standaloneCopyRequired": True,
        "vslDependency": "optional-supporting-asset",
        "offerName": "HYROX Engine",
        "price": "$27",
        "audience": "HYROX athletes who train hard but fade when running starts after heavy stations",
        "awarenessLevel": "problem-aware",
        "marketSophistication": "high enough to have tried generic running plans, random grinders, and copied HYROX workouts",
        "corePromise": "Build a race-specific 21-day engine that keeps pace, station control, and confidence intact under fatigue.",
        "primaryPain": "They feel fit in isolated sessions but lose pacing, posture, grip, and decision control when HYROX stations damage the next run.",
        "failedAlternatives": [
            {"name": "More mileage", "whyItFails": "It improves fresh running but does not rehearse the kilometer that follows a heavy station.", "whatIsNeededInstead": "A pace floor tested under station fatigue."},
            {"name": "Random grinder sessions", "whyItFails": "They prove suffering but rarely create repeatable pacing decisions or progression.", "whatIsNeededInstead": "A ladder that adds pressure in a planned order."},
            {"name": "Copied elite workouts", "whyItFails": "They ignore current level, equipment access, and the exact breakdown point.", "whatIsNeededInstead": "Scalable station pressure tied to the athlete's target pace."},
        ],
        "newInsight": "HYROX athletes usually do not need more random punishment first. They need recovery control under station pressure, because the race is decided by how quickly the next run returns to usable rhythm after each station changes the body.",
        "uniqueMechanism": {
            "name": "Compromised Engine Ladder",
            "explanation": "A three-step progression that sets a pace floor, adds station pressure, and locks race execution so the athlete practices the exact transition pattern that decides HYROX pacing.",
            "whyItWorks": "It trains the repeated recovery skill HYROX demands instead of treating running and stations as unrelated workouts.",
            "steps": [
                {"title": "Set the pace floor", "copy": "Find sustainable 1km repeat targets and station baselines before adding chaos."},
                {"title": "Add station pressure", "copy": "Pair target running with sled, carry, lunge, burpee, row, ski, and wall ball demands."},
                {"title": "Lock race execution", "copy": "Practice transitions, taper rhythm, and recovery cues before race day."},
            ],
        },
        "proofPlan": {
            "proofType": "process proof and look-inside preview",
            "proofBeforeOffer": True,
            "proofItems": [
                {"title": "Sample week preview", "copy": "Shows the three-week progression and the job of each session before purchase."},
                {"title": "Pace calculator preview", "copy": "Turns a finish target into working kilometer targets for compromised runs."},
                {"title": "Action tracker", "copy": "Shows exactly what was completed so confidence is tied to visible work."},
            ],
        },
        "productReveal": {
            "productType": "PDF training plan and race-day implementation kit",
            "plainEnglishDescription": "A 21-day HYROX training plan with pacing tools, station cue cards, benchmark tracking, race-week guidance, substitutions, and a completion tracker.",
            "whoItIsFor": "HYROX athletes with basic training experience who want a final race-specific block they can follow without private coaching.",
            "whatItHelpsThemDo": "Connect running, station fatigue, transitions, and taper decisions into one practical plan.",
            "whyNow": "A short block is most useful when the athlete already has fitness but needs the final weeks to become race-specific.",
            "coreComponents": [
                {"feature": "21-day ladder plan", "benefit": "Every week has a race-specific job.", "reasonItMatters": "The athlete stops guessing which hard sessions matter.", "buyerProblemSolved": "Disconnected training weeks.", "proofOrPreview": "Week-by-week sample schedule.", "plainBullet": "21-day HYROX plan so each week trains pace, pressure, or execution."},
                {"feature": "Pace calculator", "benefit": "Target splits are clear before the workout starts.", "reasonItMatters": "HYROX pacing collapses when effort has no number.", "buyerProblemSolved": "Drifting 1km repeats.", "proofOrPreview": "Target pace table.", "plainBullet": "Pace calculator so every compromised run has a working target."},
                {"feature": "Station cue cards", "benefit": "Technique reminders stay simple under fatigue.", "reasonItMatters": "Small mistakes become costly late in the race.", "buyerProblemSolved": "Messy stations and wasted energy.", "proofOrPreview": "Printable cue-card preview.", "plainBullet": "Station cue cards so sleds, carries, lunges, and wall balls stay controlled."},
                {"feature": "Benchmark tracker", "benefit": "Progress becomes visible in more than sweat.", "reasonItMatters": "Athletes need feedback on control, not only exhaustion.", "buyerProblemSolved": "No evidence that sessions are transferring.", "proofOrPreview": "Tracker sheet preview.", "plainBullet": "Benchmark tracker so you can see whether pace holds under pressure."},
                {"feature": "Race-week guide", "benefit": "The final days stay calm and specific.", "reasonItMatters": "Panic training can ruin a good block.", "buyerProblemSolved": "Overtraining during taper week.", "proofOrPreview": "Race-week checklist.", "plainBullet": "Race-week guide so taper, gear, warmup, and decisions are not improvised."},
            ],
            "howItWorksSteps": [
                {"title": "Choose your level", "copy": "Set the beginner, intermediate, or advanced path and record current station baselines."},
                {"title": "Calculate working pace", "copy": "Use the calculator to choose repeat targets that match the planned race outcome."},
                {"title": "Run the ladder", "copy": "Complete the three-week progression from pace floor to station pressure to race execution."},
                {"title": "Track and taper", "copy": "Record completed sessions and use the race-week guide to avoid panic training."},
            ],
            "lookInsideProof": [
                {"title": "Sample session", "copy": "Shows session focus, target, station pressure, scaling note, and completion marker."},
                {"title": "Completed tracker", "copy": "Shows what proof of action looks like for the guarantee."},
            ],
            "differenceFromAlternatives": "Most workout PDFs give a list of hard sessions. HYROX Engine gives a sequence that explains what each week trains and how it connects to race-day execution.",
            "bridgeToOfferStack": "That sequence becomes the offer stack: plan, calculator, cards, tracker, guide, substitutions, checklist, and guarantee tracker.",
        },
        "offerStack": {
            "items": [
                {"title": "21-Day HYROX Plan", "copy": "So your next three weeks have a specific race-prep sequence instead of random intensity.", "value": "$47"},
                {"title": "Pace Calculator", "copy": "So every 1km repeat starts with a target you can adjust under station fatigue.", "value": "$27"},
                {"title": "Station Cue Cards", "copy": "So key technique reminders stay visible when tired movement gets sloppy.", "value": "$17"},
                {"title": "Benchmark Tracker", "copy": "So you can see whether pace and station control are actually improving.", "value": "$17"},
                {"title": "Race-Week Taper Guide", "copy": "So the final days protect performance instead of adding panic volume.", "value": "$27"},
                {"title": "Equipment Substitution Sheet", "copy": "So normal gym limitations do not break the plan.", "value": "$17"},
                {"title": "Race-Day Checklist", "copy": "So warmup, gear, pacing, and station decisions are ready before the start line.", "value": "$17"},
                {"title": "Guarantee Tracker", "copy": "So your completed work is visible if you need to claim the action guarantee.", "value": "$17"},
            ],
            "cta": "Get instant access",
            "accessCopy": "Download the workbook and start with the pace calculator today.",
        },
        "bonuses": [
            {"title": "Printable Session Cards", "copy": "Bring the day's work to the gym without scrolling through a long document."},
            {"title": "Post-Session Review Sheet", "copy": "Record what held, what slipped, and what to adjust before the next session."},
        ],
        "valueLogic": {
            "comparison": "$27 today is less than one drop-in class and clearer than another week of guessing.",
            "priceJustification": "The value is not more information. It is a short race-specific sequence, usable targets, and decision tools for the final block.",
            "todayPrice": "$27",
            "totalValue": "$186",
        },
        "guarantee": {
            "name": "12-Workout Action Guarantee",
            "terms": "Complete at least 12 workouts in 21 days and send the completed tracker within 30 days if you do not feel more confident holding pace under fatigue.",
            "reassurance": "If the plan does not create more confidence after honest use, you get a refund.",
        },
        "objectionMatrix": [
            {"objection": "What if I am not advanced enough for HYROX-specific work?", "answer": "The plan includes scalable paths and substitution notes. You need basic training experience, not elite numbers, because the first job is finding your pace floor.", "beliefShift": "I can use the plan at my current level if I scale honestly."},
            {"objection": "What if my gym does not have every HYROX station setup?", "answer": "The substitution sheet gives practical swaps for normal gyms so you can train the pressure pattern without a perfect race venue.", "beliefShift": "Normal gym access is enough to follow the system."},
            {"objection": "Can a 21-day block really help?", "answer": "It is not trying to build years of base fitness. It sharpens the final race-specific connection between running, stations, transitions, and taper decisions.", "beliefShift": "A short block can be useful when it fixes a specific race-prep gap."},
            {"objection": "Is this just another hard workout PDF?", "answer": "No. Each week has a job, each session has a target, and the tools connect pace, station fatigue, tracking, and race-week execution.", "beliefShift": "The product is a sequence and toolset, not a random workout list."},
            {"objection": "What if I already have a coach?", "answer": "Use this only if it complements your coach's plan. The kit is best for self-directed athletes or as a structured final-block reference.", "beliefShift": "The product has a clear fit boundary."},
            {"objection": "What if I miss a session?", "answer": "The plan gives a short block, so the tracker helps you recover the sequence without pretending missed work disappeared.", "beliefShift": "I can adjust without losing the point of the block."},
            {"objection": "What if I do the work and still do not feel ready?", "answer": "That is why the 12-Workout Action Guarantee exists. Complete the tracked work and ask for a refund if confidence under fatigue does not improve.", "beliefShift": "The risk is tied to action, not vague promises."},
        ],
        "urgencyBasis": {"type": "none", "description": "No fake urgency. The reason to act is that the next 21 days can become a structured race-specific block instead of another guessing cycle.", "fakeUrgency": False},
        "sectionPlan": [
            section_row("hero", "hook", "hero-vsl-frame", "early"),
            section_row("vsl", "supporting overview", "hero-vsl-frame", "support"),
            section_row("problem", "problem diagnosis", "buyer-situation-photo"),
            section_row("agitation", "cost of staying stuck", "structured-panel"),
            section_row("failed-alternatives", "market diagnosis", "comparison-visual"),
            section_row("new-insight", "epiphany", "structured-panel"),
            section_row("mechanism", "unique mechanism", "mechanism-diagram"),
            section_row("proof", "proof before offer", "proof-demo-visual"),
            section_row("before-after", "before after", "comparison-visual"),
            section_row("product", "product reveal", "product-mockup"),
            section_row("feature-benefit", "feature benefit", "structured-panel"),
            section_row("how-it-works", "how it works", "mechanism-diagram"),
            section_row("offer-stack", "offer stack", "offer-stack-bundle", "buy"),
            section_row("bonuses", "bonuses", "checklist-visual"),
            section_row("pricing", "price value", "structured-panel", "buy"),
            section_row("guarantee", "risk reversal", "structured-panel"),
            section_row("fit", "fit filter", "checklist-visual"),
            section_row("faq", "objection handling", "structured-panel"),
            section_row("final-cta", "close", "offer-stack-bundle", "buy"),
        ],
        "pageKitArchetype": "classic-vsl-longform",
        "themePreset": "fitness-performance",
        "checkoutTarget": "#checkout",
    }


def synthetic_good_copy_build() -> dict:
    workspace = SKILL_ROOT / "tests" / ".tmp" / "good-copy-studio-hyrox"
    if workspace.exists():
        shutil.rmtree(workspace)
    workspace.mkdir(parents=True, exist_ok=True)
    (workspace / "offer-os.json").write_text(
        json.dumps(
            {
                "schema": "offer-os/v1",
                "mode": "copy-test",
                "offerName": "HYROX Engine",
                "price": "$27",
                "audience": "HYROX athletes",
                "modules": [],
                "artifacts": [],
                "quality": {},
            },
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )
    (workspace / "copy-plan.json").write_text(json.dumps(good_hyrox_copy_plan(), indent=2) + "\n", encoding="utf-8")
    (workspace / "theme.json").write_text(
        json.dumps(
            {
                "themePreset": "fitness-performance",
                "pageKitArchetype": "classic-vsl-longform",
                "colors": {
                    "background": "#07110c",
                    "surface": "#111d15",
                    "ink": "#ffffff",
                    "muted": "#c8d7ce",
                    "primary": "#cfff05",
                    "accent": "#00b6ff",
                    "dark": "#030705",
                },
            },
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )
    builder = SKILL_ROOT / "scripts" / "build_copy.py"
    completed = subprocess.run(
        [sys.executable, str(builder), "--workspace", str(workspace)],
        text=True,
        capture_output=True,
        check=False,
    )
    copy_path = workspace / "copy.md"
    copy_text = copy_path.read_text(encoding="utf-8", errors="ignore") if copy_path.exists() else ""
    copy_words = len(copy_text.split())
    failures = []
    if completed.returncode != 0:
        failures.append("build_copy.py failed")
    if "# Section Blueprint" in copy_text or "| sectionId |" in copy_text:
        failures.append("copy.md contains blueprint material")
    if copy_words < 2500:
        failures.append(f"copy.md under 2500 words: {copy_words}")
    if "this section explains" in copy_text.lower() or "belief shift" in copy_text.lower():
        failures.append("copy.md contains meta copy")
    if not (workspace / "copy-blueprint.md").exists():
        failures.append("copy-blueprint.md missing")
    if not (workspace / "sales-page-blueprint.json").exists():
        failures.append("sales-page-blueprint.json missing")
    page_completed = subprocess.CompletedProcess(args=[], returncode=0, stdout="", stderr="")
    index_text = ""
    if completed.returncode == 0:
        page_builder = SKILL_ROOT / "scripts" / "build_sales_page.py"
        page_completed = subprocess.run(
            [sys.executable, str(page_builder), "--workspace", str(workspace), "--output", "index.html"],
            text=True,
            capture_output=True,
            check=False,
        )
        index_path = workspace / "index.html"
        index_text = index_path.read_text(encoding="utf-8", errors="ignore") if index_path.exists() else ""
        if page_completed.returncode != 0:
            failures.append("build_sales_page.py failed")
        if '<!-- [hero] -->' not in index_text or '<!-- [/hero] -->' not in index_text:
            failures.append("index.html missing exact-copy section comments")
        if 'data-offeros-copy-contract="exact-copy-sections-v1"' not in index_text:
            failures.append("index.html missing exact-copy contract markers")
        if 'data-offeros-section="new-insight"' not in index_text or 'data-offeros-section="feature-benefit"' not in index_text:
            failures.append("index.html missing Copy Studio spine sections")
        if "Approved partials used" in page_completed.stdout:
            failures.append("exact-copy page build used partials instead of copy.md sections")
    return {
        "id": "synthetic_good_copy_build",
        "ok": not failures,
        "returncode": completed.returncode if completed.returncode != 0 else page_completed.returncode,
        "copyWords": copy_words,
        "failures": failures,
        "stdout": (completed.stdout + page_completed.stdout)[-1000:],
        "stderr": (completed.stderr + page_completed.stderr)[-1000:],
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Self-test OfferOS skill source and known regression workspaces.")
    parser.add_argument("--bad-workspace", action="append", default=[], help="Known-bad generated output that must fail validator checks.")
    args = parser.parse_args()

    source_results = source_check()
    bad_results = [bad_workspace_check(Path(item).resolve()) for item in args.bad_workspace]
    synthetic_results = [
        synthetic_visual_plan_regression(),
        synthetic_copy_studio_regression(),
        synthetic_two_column_hero_regression(),
        synthetic_product_page_regression(),
        synthetic_page_kit_regression(),
        synthetic_svg_artifact_regression(),
        synthetic_logo_drift_regression(),
        synthetic_code_rendered_creative_regression(),
        synthetic_generated_controller_regression(),
        synthetic_page_kit_builder_rejects_unapproved_sources(),
        synthetic_good_copy_build(),
    ]
    ok = all(item["ok"] for item in source_results) and all(item["ok"] for item in bad_results) and all(item["ok"] for item in synthetic_results)

    print(
        json.dumps(
            {
                "ok": ok,
                "sourceChecks": source_results,
                "badWorkspaceChecks": bad_results,
                "syntheticChecks": synthetic_results,
            },
            indent=2,
        )
    )
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
