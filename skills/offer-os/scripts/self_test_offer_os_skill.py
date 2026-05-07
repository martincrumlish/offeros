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
            "Generator-first",
            "warnings are not shippable",
            "preserve the direct-response hero and buy-box offer-stack contracts exactly",
        ],
    },
    {
        "id": "build_controller_recipe_is_explicit",
        "path": "references/exact-build-recipes.md",
        "needles": [
            "## Build Controller Recipe",
            "Do not hand-fix generated files after QA without also fixing the generator.",
            "Treat validator warnings as build failures in deep mode.",
            "VSL preview mobile",
            "qa-notes.md",
            "Create `visual-asset-plan.md` v2 only after `copy.md` contains the sales-page section blueprint.",
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
            "3 complete logo lockup candidates",
            "The first logo task is not a mark-only task.",
            "Do not create the primary logo with SVG",
            "assets/logo.png",
            "--provenance imagegen-composite",
            "includesReadableOfferName",
            "imagegenCompleteLogoLockupAttempted",
            "imagegenLogoCandidateCount",
            "exactOfferNamePreserved",
            "markNotIllustration",
            "wordmarkTypographyChecked",
            "wordmarkKerningChecked",
            "professionalLockupApproved",
            "logo-mark.png",
            "output/qa/logo-lockup-preview.png",
            "logoLockup",
            "If the primary logo path is `.svg`, stop and rebuild the logo.",
            "If imagegen was not first used for complete logo lockup candidates",
            "If the wordmark is just default text pasted beside the mark",
            "If provenance is not `imagegen` or `imagegen-composite`, stop and rebuild the logo.",
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
            "Do not create or register a primary SVG logo.",
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
            "Deep generated-design runs must not use SVG as the primary logo",
            "Deep generated-design runs must register the primary logo with provenance: imagegen or imagegen-composite.",
            "includesReadableOfferName",
            "exactOfferNamePreserved",
            "professionalLockupApproved",
            "imagegenCompleteLogoLockupAttempted",
            "Primary logo artifact cannot point at a mark-only file",
            "Logo generationTool must record imagegen-complete-logo attempts before any fallback compositor.",
            "Imagegen-composite logos must record wordmarkSource: professional-wordmark-compositor.",
            "brand.logo must match the registered primary logo artifact path.",
            "Primary logo bitmap must be a horizontal lockup",
            "Sales page contains repeated boilerplate copy",
            "Visual asset plan missing",
            "hasArtifactSpecificPlan",
            "visualPlanStage: post-content-blueprint",
            "copyBlueprintUsed",
            "salesPageImageSystem: mixed-direct-response-v1",
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
            "data-offeros-hero-layout=\"stacked-vsl\"",
            "VSL setup section is too text-heavy",
            "data-offeros-faq-item",
            "data-offeros-cta",
            "Direct-response hero must include a VSL/video frame marked data-offeros-hero-video",
            "Direct-response offer stack must include a deliverable checklist marked data-offeros-offer-checklist",
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
            "after the initial offer architecture, `design.md`, selected logo concept, `assets/logo.png`, `copy.md` with the sales-page section blueprint, and `visual-asset-plan.md` v2 exist",
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
    "must not use SVG as the primary logo",
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
        "Sales-page visual plan must include 4+ copyAnchor fields",
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
