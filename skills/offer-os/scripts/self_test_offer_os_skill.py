import argparse
import json
from pathlib import Path
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
            "Create `visual-asset-plan.json` and `visual-asset-plan.md` v2 only after `copy.md` contains the sales-page section blueprint.",
        ],
    },
    {
        "id": "studio_dispatcher_and_builders_exist",
        "path": "references/exact-build-recipes.md",
        "needles": [
            "## OfferOS Production Studio Recipe",
            "`scripts/offeros.py`",
            "`build_visual_asset_plan.py`",
            "`build_email_sequence.py`",
            "`build_workbook.py`",
            "`build_vsl_deck.js`",
            "quality.pdf.renderBackend: \"gotenberg-chromium\"",
            "quality.vsl.studio: \"vsl-deck-studio-v1\"",
            "quality.emails.studio: \"email-launch-studio-v1\"",
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
            "salesPageImageSystem: mixed-direct-response-v1",
            "visualKind",
            "copyAnchor",
            "mixed-direct-response-v1",
            "busy fake UI",
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
            "references/direct-response-framework.md",
            "`copy.md` must include these exact headings",
            "# Section Blueprint",
            "direct-response-long-form-v1",
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
            "eyebrowPolicy: \"sparse-key-signposts-v1\"",
            "eyebrowAlignment: \"centered-with-section-heading\"",
            "data-offeros-image-display=",
            "data-lucide",
            "Watch this first",
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
            "EYEBROW_POLICY = \"sparse-key-signposts-v1\"",
            "EYEBROW_SECTIONS",
            "section_eyebrow",
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
            "fields tied to copy sections",
            "Sales-page visual plan is all mockup/UI-style visuals",
            "PDF-specific visual asset/treatment count below target",
            "VSL-specific visual asset/treatment count below target",
            "compositionContract",
            "stacked-vsl-hero-v2",
            "direct-response-long-form-v1",
            "Sales copy Section Blueprint",
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
            "after the initial offer architecture, `design.md`, final logo lockup, `assets/logo.png`, `copy.md` with the sales-page section blueprint, and `visual-asset-plan.md` v2 exist",
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
        "Visual asset plan v2 requires copy.md/sales-copy",
        "Visual asset plan metadata must include visualPlanStage: post-content-blueprint.",
        "Image quality metadata must record visualPlanStage: post-content-blueprint.",
        "Image quality metadata must confirm copyBlueprintUsed.",
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


def synthetic_two_column_hero_regression() -> dict:
    expected = [
        "Direct-response sales page quality metadata must record heroContract: stacked-vsl-hero-v2.",
        "Direct-response sales page quality metadata must record heroTemplate: offeros-stacked-vsl-v2.",
        "Direct-response sales page quality metadata must record heroVideoFrame: large-16x9.",
        "Direct-response sales page quality metadata must record heroLayout: stacked-vsl.",
        "Direct-response sales page quality metadata must confirm heroVideoProminenceChecked.",
        "Direct-response sales page quality metadata must record framework: direct-response-long-form-v1.",
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
        "Sales copy must include # Section Blueprint before page build.",
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


def main() -> int:
    parser = argparse.ArgumentParser(description="Self-test OfferOS skill source and known regression workspaces.")
    parser.add_argument("--bad-workspace", action="append", default=[], help="Known-bad generated output that must fail validator checks.")
    args = parser.parse_args()

    source_results = source_check()
    bad_results = [bad_workspace_check(Path(item).resolve()) for item in args.bad_workspace]
    synthetic_results = [
        synthetic_visual_plan_regression(),
        synthetic_two_column_hero_regression(),
        synthetic_product_page_regression(),
        synthetic_page_kit_regression(),
        synthetic_svg_artifact_regression(),
        synthetic_logo_drift_regression(),
        synthetic_code_rendered_creative_regression(),
        synthetic_generated_controller_regression(),
        synthetic_page_kit_builder_rejects_unapproved_sources(),
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
