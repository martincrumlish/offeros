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
            "Image/source provenance: imagegen, imagegen-composite, provided, licensed, screenshot, "
            "html-css, pil-generated, manual, or generated-by-code. Deep generated-design primary "
            "conversion visuals (product bundle, offer stack, hero/VSL thumbnail, product mockup, ads) "
            "must be imagegen/imagegen-composite unless provided/licensed. Do not register generated SVG artifacts."
        ),
    )
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
