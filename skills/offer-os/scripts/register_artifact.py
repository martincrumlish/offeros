import argparse
from datetime import datetime, timezone
import json
from pathlib import Path


def load_manifest(path: Path) -> dict:
    if path.exists():
        return json.loads(path.read_text(encoding="utf-8"))
    raise SystemExit(f"Manifest not found: {path}")


def main() -> int:
    parser = argparse.ArgumentParser(description="Register or update an artifact in offer-os.json.")
    parser.add_argument("--manifest", default="offer-os.json")
    parser.add_argument("--id", required=True)
    parser.add_argument("--title", required=True)
    parser.add_argument("--type", required=True)
    parser.add_argument("--path", required=True)
    parser.add_argument("--preview", default="")
    parser.add_argument("--category", default="General")
    parser.add_argument("--description", default="")
    parser.add_argument("--status", default="complete")
    parser.add_argument(
        "--provenance",
        default="",
        help=(
            "Image/source provenance: imagegen, imagegen-final, imagegen-composite, provided, licensed, screenshot, "
            "html-css, manual, or generated-by-code. Do not register pil-generated artifacts. "
            "Deep generated-design primary "
            "conversion visuals (product bundle, offer stack, hero/VSL thumbnail, product mockup, ads) "
            "must be imagegen-final unless provided/licensed. Do not register generated SVG artifacts."
        ),
    )
    parser.add_argument("--final-pixels-generated-by", default="", help="For primary image assets: imagegen, provided, licensed, or real-artifact-screenshot.")
    parser.add_argument("--local-postprocess", default="", help="Comma-separated non-creative operations only: crop, resize, compression, format-conversion.")
    parser.add_argument("--local-creative-overlay", default="", help="For primary image assets this must be false.")
    parser.add_argument("--imagegen-native-composite", action="store_true", help="Set only when imagegen performed the reference-image composition.")
    parser.add_argument("--buyer-value", type=int, default=0, help="Commercial audit score 1-5.")
    parser.add_argument("--usability", type=int, default=0, help="Commercial audit score 1-5.")
    parser.add_argument("--trust", type=int, default=0, help="Commercial audit score 1-5.")
    parser.add_argument("--quality-notes", default="", help="Short commercial quality note.")
    parser.add_argument("--workspace", default=".")
    args = parser.parse_args()

    root = Path(args.workspace).resolve()
    manifest_path = root / args.manifest
    manifest = load_manifest(manifest_path)

    artifact = {
        "id": args.id,
        "title": args.title,
        "type": args.type,
        "category": args.category,
        "path": args.path,
        "preview": args.preview or args.path,
        "description": args.description,
        "status": args.status,
        "updatedAt": datetime.now(timezone.utc).isoformat(),
    }
    if args.provenance:
        artifact["provenance"] = args.provenance
    if args.final_pixels_generated_by:
        artifact["finalPixelsGeneratedBy"] = args.final_pixels_generated_by
    if args.local_postprocess:
        artifact["localPostprocess"] = [item.strip() for item in args.local_postprocess.split(",") if item.strip()]
    if args.local_creative_overlay:
        artifact["localCreativeOverlay"] = args.local_creative_overlay.strip().lower() in {"true", "yes", "1"}
    if args.imagegen_native_composite:
        artifact["imagegenNativeComposite"] = True
    if args.buyer_value or args.usability or args.trust or args.quality_notes:
        artifact["quality"] = {
            "buyerValue": args.buyer_value,
            "usability": args.usability,
            "trust": args.trust,
            "notes": args.quality_notes,
        }

    artifacts = manifest.setdefault("artifacts", [])
    for index, existing in enumerate(artifacts):
        if existing.get("id") == args.id:
            artifacts[index] = {**existing, **artifact}
            break
    else:
        artifacts.append(artifact)

    manifest_path.write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
    print(f"Registered {args.id}: {args.path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
