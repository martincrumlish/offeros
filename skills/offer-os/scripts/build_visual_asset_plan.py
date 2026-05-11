import argparse
from datetime import datetime, timezone
import json
from pathlib import Path
import re


SALES_VISUALS = [
    ("hero-vsl-frame", "hero", "Make the opening video feel worth watching", "assets/page/hero-vsl-thumbnail.png", "16:9", "no tiny UI text"),
    ("buyer-situation-photo", "problem", "Make the buyer's current situation concrete", "assets/page/problem-scene.png", "4:3", "no tiny UI text"),
    ("structured-panel", "agitation", "Show the cost of delay without melodrama", "assets/page/cost-of-delay.png", "3:2", "short captions only"),
    ("comparison-visual", "failed-alternatives", "Show why the old options fail", "assets/page/failed-alternatives.png", "16:9", "labels only"),
    ("mechanism-diagram", "mechanism", "Make the unique mechanism easy to understand", "assets/page/mechanism-diagram.png", "3:2", "short labels only"),
    ("proof-demo-visual", "proof", "Show proof or a transparent proof substitute", "assets/page/proof-demo.png", "16:10", "no fake testimonials"),
    ("structured-panel", "before-after", "Make the before/after contrast concrete", "assets/page/before-after.png", "2:1", "short captions only"),
    ("product-mockup", "product", "Reveal the product and feature-benefit breakdown", "assets/page/product-reveal.png", "4:3", "use supplied logo exactly"),
    ("offer-stack-bundle", "offer-stack", "Make the stack feel tangible at the buy box", "assets/page/product-bundle.png", "16:9", "use supplied logo exactly"),
    ("structured-panel", "guarantee", "Make the risk reversal easy to trust", "assets/page/guarantee.png", "3:2", "short captions only"),
]

PDF_VISUALS = [
    ("brand-frame", "cover", "Open with a premium workbook cover", "assets/pdf/cover-frame.png", "8.5:11"),
    ("structured-panel", "quick-start", "Show the one-sitting implementation path", "assets/pdf/quick-start-map.png", "4:3"),
    ("matrix-visual", "decision-matrix", "Make the buyer choose with a matrix", "assets/pdf/decision-matrix.png", "4:3"),
    ("worksheet-preview", "completed-example", "Show a filled-in example", "assets/pdf/completed-example.png", "4:3"),
    ("worksheet-preview", "blank-worksheet", "Show the blank worksheet version", "assets/pdf/blank-worksheet.png", "4:3"),
    ("checklist-visual", "implementation-plan", "Make completion feel concrete", "assets/pdf/implementation-checklist.png", "4:3"),
]

VSL_VISUALS = [
    ("slide-pattern-interrupt", "hook", "Stop the scroll inside the deck", "assets/vsl/pattern-interrupt.png", "16:9"),
    ("buyer-situation-photo", "problem", "Show the current messy state", "assets/vsl/problem-scene.png", "16:9"),
    ("comparison-visual", "failed-alternatives", "Show the failed paths", "assets/vsl/failed-alternatives.png", "16:9"),
    ("mechanism-diagram", "mechanism", "Explain the mechanism visually", "assets/vsl/mechanism.png", "16:9"),
    ("proof-demo-visual", "proof", "Show a demo/proof substitute", "assets/vsl/proof-demo.png", "16:9"),
    ("product-mockup", "product", "Reveal the product clearly", "assets/vsl/product-reveal.png", "16:9"),
    ("offer-stack-bundle", "offer-stack", "Show the offer stack", "assets/vsl/offer-stack.png", "16:9"),
    ("structured-panel", "pricing", "Show price/value contrast", "assets/vsl/price-value.png", "16:9"),
    ("structured-panel", "guarantee", "Show risk reversal", "assets/vsl/guarantee.png", "16:9"),
    ("structured-panel", "faq", "Handle objections", "assets/vsl/objections.png", "16:9"),
    ("brand-frame", "final-cta", "Close the deck", "assets/vsl/final-cta.png", "16:9"),
    ("dashboard-mockup", "delivery", "Show how access works", "assets/vsl/delivery-preview.png", "16:9"),
]

PRIMARY_CONVERSION_VISUAL_KINDS = {
    "hero-vsl-frame",
    "product-mockup",
    "offer-stack-bundle",
    "buyer-situation-photo",
    "comparison-visual",
    "mechanism-diagram",
    "proof-demo-visual",
    "structured-panel",
    "ad-creative",
}


def read_json(path: Path, default: dict | None = None) -> dict:
    if path.exists():
        return json.loads(path.read_text(encoding="utf-8-sig"))
    if default is not None:
        return default
    raise SystemExit(f"Required JSON file not found: {path}")


def write_json(path: Path, payload: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")


def upsert_artifact(manifest: dict, artifact: dict) -> None:
    artifacts = manifest.setdefault("artifacts", [])
    for index, item in enumerate(artifacts):
        if item.get("id") == artifact.get("id"):
            artifacts[index] = {**item, **artifact}
            return
    artifacts.append(artifact)


def visual_row(kind: str, anchor: str, job: str, path: str, ratio: str, text_rule: str = "short labels only", provenance: str = "imagegen") -> dict:
    if kind in PRIMARY_CONVERSION_VISUAL_KINDS and provenance in {"imagegen", "imagegen-composite"}:
        provenance = "imagegen-final"
    logo_prompt = ""
    if kind in {"product-mockup", "offer-stack-bundle", "dashboard-mockup", "ad-creative"}:
        logo_prompt = " logoReference: assets/logo.png. Use the supplied assets/logo.png exactly; do not redesign, recolor, redraw, reinterpret, replace, or substitute the logo."
    row = {
        "artifactTarget": path,
        "filePath": path,
        "visualKind": kind,
        "copyAnchor": anchor,
        "conversionJob": job,
        "aspectRatio": ratio,
        "aspectRatioReason": f"Chosen for the {anchor} page slot, not copied from a generic default.",
        "displayIntent": "content-hugging-constrained-frame",
        "maxDisplayHeight": "560px desktop / 420px mobile",
        "textRule": text_rule,
        "requiredTool": "imagegen",
        "requiredAction": "call-imagegen-skill-tool",
        "imagegenRequired": True,
        "fallbackAllowed": False,
        "source/provenance": provenance,
        "finalPixelsGeneratedBy": "imagegen" if provenance in {"imagegen-final", "imagegen-composite"} else provenance,
        "localPostprocess": ["crop", "resize", "compression", "format-conversion"] if provenance in {"imagegen-final", "imagegen-composite"} else [],
        "localCreativeOverlay": False,
        "reusePermission": "artifact-specific",
        "artifactSpecific": True,
        "generationPrompt": f"CALL THE imagegen SKILL/TOOL FOR THIS EXACT ROW. Save the imagegen output to {path}. Create a {kind} for the {anchor} section. {job}. Aspect ratio {ratio}; compose for the actual page slot and a content-hugging constrained frame, not a generic repeated 4:3 mockup. Do not create this image with Python, Pillow, canvas, HTML/CSS, screenshots, SVG, or any local renderer. Do not create a local substitute if imagegen is unavailable; mark the asset needs_revision instead. Do not add logo, text, UI cards, badges, mockups, overlays, or product-stack composition locally after imagegen. Avoid busy fake UI/mockup filler.{logo_prompt}",
    }
    if provenance == "imagegen-composite":
        row["imagegenNativeComposite"] = True
    return row


def markdown_rows(rows: list[dict]) -> str:
    chunks = []
    for row in rows:
        chunks.extend(
            [
                f"- artifactTarget: `{row['artifactTarget']}`",
                f"  filePath: `{row['filePath']}`",
                f"  visualKind: `{row['visualKind']}`",
                f"  copyAnchor: `{row['copyAnchor']}`",
                f"  conversionJob: `{row['conversionJob']}`",
                f"  aspectRatio: `{row['aspectRatio']}`",
                f"  aspectRatioReason: `{row['aspectRatioReason']}`",
                f"  displayIntent: `{row['displayIntent']}`",
                f"  maxDisplayHeight: `{row['maxDisplayHeight']}`",
                f"  textRule: `{row['textRule']}`",
                f"  requiredTool: `{row['requiredTool']}`",
                f"  requiredAction: `{row['requiredAction']}`",
                f"  imagegenRequired: `{str(row['imagegenRequired']).lower()}`",
                f"  fallbackAllowed: `{str(row['fallbackAllowed']).lower()}`",
                f"  source/provenance: `{row['source/provenance']}`",
                f"  finalPixelsGeneratedBy: `{row['finalPixelsGeneratedBy']}`",
                f"  localPostprocess: `{', '.join(row['localPostprocess'])}`",
                f"  localCreativeOverlay: `{str(row['localCreativeOverlay']).lower()}`",
                *([f"  imagegenNativeComposite: `{str(row['imagegenNativeComposite']).lower()}`"] if "imagegenNativeComposite" in row else []),
                f"  reusePermission: `{row['reusePermission']}`",
                f"  artifactSpecific: `{str(row['artifactSpecific']).lower()}`",
                f"  generationPrompt: `{row['generationPrompt']}`",
                "",
            ]
        )
    return "\n".join(chunks)


def copy_blueprint_exists(root: Path) -> bool:
    copy_blueprint_path = root / "copy-blueprint.md"
    sales_page_blueprint_path = root / "sales-page-blueprint.json"
    if not copy_blueprint_path.exists() or not sales_page_blueprint_path.exists():
        return False
    text = copy_blueprint_path.read_text(encoding="utf-8", errors="ignore").lower()
    return "# section blueprint" in text and bool(re.search(r"\bsectionid\b", text))


def read_copy_plan(root: Path) -> dict:
    path = root / "copy-plan.json"
    if path.exists():
        try:
            return json.loads(path.read_text(encoding="utf-8-sig"))
        except json.JSONDecodeError:
            return {}
    return {}


def sales_visuals_from_copy_plan(root: Path) -> list[dict]:
    copy_plan = read_copy_plan(root)
    rows = copy_plan.get("sectionPlan") if isinstance(copy_plan.get("sectionPlan"), list) else []
    by_section = {item.get("sectionId"): item for item in rows if isinstance(item, dict)}
    section_specs = [
        ("hero-vsl-frame", "hero", "assets/page/hero-vsl-thumbnail.png", "16:9", "no tiny UI text"),
        ("buyer-situation-photo", "problem", "assets/page/problem-scene.png", "4:3", "no tiny UI text"),
        ("structured-panel", "agitation", "assets/page/cost-of-delay.png", "3:2", "short captions only"),
        ("comparison-visual", "failed-alternatives", "assets/page/failed-alternatives.png", "16:9", "labels only"),
        ("mechanism-diagram", "mechanism", "assets/page/mechanism-diagram.png", "3:2", "short labels only"),
        ("proof-demo-visual", "proof", "assets/page/proof-demo.png", "16:10", "no fake testimonials"),
        ("product-mockup", "product", "assets/page/product-reveal.png", "4:3", "use supplied logo exactly"),
        ("offer-stack-bundle", "offer-stack", "assets/page/product-bundle.png", "16:9", "use supplied logo exactly"),
        ("structured-panel", "guarantee", "assets/page/guarantee.png", "3:2", "short captions only"),
    ]
    visuals = []
    for kind, section_id, path, ratio, text_rule in section_specs:
        row = by_section.get(section_id, {})
        job = row.get("conversionJob") or row.get("visualNeed") or f"Support the {section_id} section from Copy Studio."
        visuals.append(visual_row(kind, section_id, job, path, ratio, text_rule))
    return visuals


def build_plan(root: Path, manifest: dict) -> dict:
    sales = sales_visuals_from_copy_plan(root) if read_copy_plan(root) else [visual_row(*item) for item in SALES_VISUALS]
    copy_plan_used = bool(read_copy_plan(root))
    pdf = [visual_row(item[0], item[1], item[2], item[3], item[4], provenance="imagegen-composite" if item[0] in {"matrix-visual", "worksheet-preview", "checklist-visual"} else "imagegen") for item in PDF_VISUALS]
    vsl = [visual_row(item[0], item[1], item[2], item[3], item[4], provenance="imagegen-composite" if item[0] in {"mechanism-diagram", "comparison-visual", "structured-panel"} else "imagegen") for item in VSL_VISUALS]
    ads = [
        visual_row("ad-creative", "ad-angle-1", "Lead with the painful false belief", "assets/ads/facebook-ad-1.png", "1:1"),
        visual_row("ad-creative", "ad-angle-2", "Lead with the mechanism shift", "assets/ads/facebook-ad-2.png", "1:1"),
        visual_row("ad-creative", "ad-angle-3", "Lead with the tangible stack", "assets/ads/facebook-ad-3.png", "1:1"),
    ]
    return {
        "schema": "offeros/visual-asset-plan/v2",
        "visualPlanStage": "post-content-blueprint",
        "copyBlueprintUsed": copy_blueprint_exists(root),
        "copyStudioUsed": copy_plan_used,
        "copyPlanPath": "copy-plan.json" if copy_plan_used else "",
        "salesPageImageSystem": "mixed-direct-response-v1",
        "primaryConversionFinalPixelsPolicy": "imagegen-final-v1",
        "aspectRatioPolicy": "slot-aware-v1",
        "logoReference": "assets/logo.png",
        "logoUsagePolicy": "use-locked-logo-reference",
        "alternateLogosCreated": False,
        "mockupHeavyUserRequested": False,
        "sourceBlueprints": ["copy-plan.json", "copy-blueprint.md", "sales-page-blueprint.json", "copy.md", "workbook/workbook-blueprint.json", "presentation/vsl-deck-plan.json", "facebook-ads.md"],
        "globalBrandAssets": [
            visual_row(
                "brand-frame",
                "global",
                "Keep every artifact tied to the same brand identity with one final logo lockup",
                "assets/logo.png",
                "3:1",
                "readable full wordmark lockup only",
                provenance="imagegen-final",
            )
        ],
        "salesPageVisuals": sales,
        "pdfProductVisuals": pdf,
        "vslDeckVisuals": vsl,
        "adVisuals": ads,
        "dashboardVisuals": [
            visual_row("dashboard-mockup", "delivery-dashboard", "Show the buyer where assets live", "assets/dashboard/dashboard-preview.png", "16:9")
        ],
    }


def write_markdown(path: Path, plan: dict) -> None:
    lines = [
        "# Visual Asset Plan",
        "",
        "## Visual Plan Metadata",
        "",
        f"- visualPlanStage: {plan['visualPlanStage']}",
        f"- copyBlueprintUsed: {str(plan['copyBlueprintUsed']).lower()}",
        f"- copyStudioUsed: {str(plan['copyStudioUsed']).lower()}",
        f"- copyPlanPath: {plan['copyPlanPath']}",
        f"- salesPageImageSystem: {plan['salesPageImageSystem']}",
        f"- primaryConversionFinalPixelsPolicy: {plan['primaryConversionFinalPixelsPolicy']}",
        f"- aspectRatioPolicy: {plan['aspectRatioPolicy']}",
        f"- logoReference: {plan['logoReference']}",
        f"- logoUsagePolicy: {plan['logoUsagePolicy']}",
        f"- alternateLogosCreated: {str(plan['alternateLogosCreated']).lower()}",
        f"- mockupHeavyUserRequested: {str(plan['mockupHeavyUserRequested']).lower()}",
        "- sourceBlueprints: copy-plan.json, copy-blueprint.md, sales-page-blueprint.json, copy.md, product blueprint/page archetypes, VSL slide plan, ad angle map",
        "",
        "## Global Brand Assets",
        "",
        markdown_rows(plan["globalBrandAssets"]),
        "## Sales Page Visuals",
        "",
        markdown_rows(plan["salesPageVisuals"]),
        "## PDF Product Visuals",
        "",
        markdown_rows(plan["pdfProductVisuals"]),
        "## VSL Deck Visuals",
        "",
        markdown_rows(plan["vslDeckVisuals"]),
        "## Ad Visuals",
        "",
        markdown_rows(plan["adVisuals"]),
        "## Dashboard Visuals",
        "",
        markdown_rows(plan["dashboardVisuals"]),
        "## Reuse Rules",
        "",
        "- Sales-page visuals are not the default pool for PDF, VSL, or ads.",
        "- PDF and VSL require their own supporting visuals/treatments.",
        "- Use `assets/logo.png` as the only downstream logo reference.",
        "- Do not generate/redraw/reinvent logos or wordmarks in downstream prompts.",
        "- Avoid busy fake UI/mockup filler unless the copy anchor specifically needs a product mockup.",
        "",
    ]
    path.write_text("\n".join(lines), encoding="utf-8")


def update_manifest(root: Path, manifest: dict, plan: dict) -> None:
    now = datetime.now(timezone.utc).isoformat()
    upsert_artifact(
        manifest,
        {
            "id": "visual-asset-plan",
            "title": "Visual Asset Plan",
            "type": "source",
            "category": "Strategy",
            "path": "visual-asset-plan.md",
            "preview": "visual-asset-plan.md",
            "description": "Post-copy-blueprint artifact-specific visual asset plan.",
            "status": "complete" if plan["copyBlueprintUsed"] else "needs_revision",
            "provenance": "manual",
            "updatedAt": now,
        },
    )
    quality = manifest.setdefault("quality", {}).setdefault("images", {})
    quality.update(
        {
            "hasArtifactSpecificPlan": True,
            "visualPlanPath": "visual-asset-plan.md",
            "visualPlanJsonPath": "visual-asset-plan.json",
            "visualPlanStage": "post-content-blueprint",
            "copyBlueprintUsed": plan["copyBlueprintUsed"],
            "copyStudioUsed": plan["copyStudioUsed"],
            "copyPlanPath": plan["copyPlanPath"],
            "visualReusePolicy": "artifact-specific-v1",
            "salesPageImageSystem": "mixed-direct-response-v1",
            "primaryConversionFinalPixelsPolicy": "imagegen-final-v1",
            "aspectRatioPolicy": "slot-aware-v1",
            "logoReference": "assets/logo.png",
            "logoUsagePolicy": "use-locked-logo-reference",
            "alternateLogosCreated": False,
            "mockupHeavyUserRequested": False,
            "agentDispatchUsed": False,
            "agentDispatchNotUsedReason": "No subagent/imagegen workers were authorized or available during this deterministic plan build.",
            "salesPageVisualCount": len(plan["salesPageVisuals"]),
            "pdfVisualCount": len(plan["pdfProductVisuals"]),
            "pdfSpecificVisualCount": len(plan["pdfProductVisuals"]),
            "vslVisualCount": len(plan["vslDeckVisuals"]),
            "vslSpecificVisualCount": len(plan["vslDeckVisuals"]),
            "adImageCount": len(plan["adVisuals"]),
            "pdfUsesOnlySalesPageImages": False,
            "vslUsesOnlySalesPageImages": False,
            "salesPageReuseOnly": False,
        }
    )
    manifest["updatedAt"] = now
    (root / "offer-os.json").write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description="Create OfferOS visual-asset-plan v2 after copy blueprint.")
    parser.add_argument("--workspace", default=".")
    parser.add_argument("--manifest", default="offer-os.json")
    parser.add_argument("--plan-only", action="store_true", help="Create source plan only; do not attempt image generation.")
    args = parser.parse_args()
    root = Path(args.workspace).resolve()
    manifest = read_json(root / args.manifest)
    plan = build_plan(root, manifest)
    write_json(root / "visual-asset-plan.json", plan)
    write_markdown(root / "visual-asset-plan.md", plan)
    update_manifest(root, manifest, plan)
    if not plan["copyBlueprintUsed"]:
        print("Created visual plan, but copyBlueprintUsed=false. Build copy-blueprint.md and sales-page-blueprint.json before image generation.")
        return 2
    print("Created visual-asset-plan.json and visual-asset-plan.md")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
