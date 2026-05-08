import argparse
from datetime import datetime, timezone
import json
import re
from pathlib import Path


DEFAULT_MODULES = [
    "offer-architecture",
    "design",
    "brand",
    "sales-copy",
    "sales-page",
    "images",
    "pdf-product",
    "facebook-ads",
    "emails",
    "vsl",
    "delivery-dashboard",
    "qa",
]


def slugify(value: str) -> str:
    value = value.lower().strip()
    value = re.sub(r"[^a-z0-9]+", "-", value)
    return value.strip("-") or "offer"


def main() -> int:
    parser = argparse.ArgumentParser(description="Initialize an OfferOS project manifest and folders.")
    parser.add_argument("--name", required=True, help="Offer name.")
    parser.add_argument("--audience", default="", help="Target audience.")
    parser.add_argument("--problem", default="", help="Problem or desired result.")
    parser.add_argument("--price", default="", help="Offer price.")
    parser.add_argument("--mode", default="deep", choices=["deep", "standard", "fast"], help="OfferOS run mode.")
    parser.add_argument("--design-source-type", default="generated", help="design-md, url, screenshots, generated, hybrid, or unresolved.")
    parser.add_argument("--design-source-path", default="", help="Path to design.md, screenshot, or design source file.")
    parser.add_argument("--design-source-url", default="", help="Reference URL when used.")
    parser.add_argument("--workspace", default=".", help="Workspace root.")
    parser.add_argument("--force", action="store_true", help="Overwrite an existing offer-os.json.")
    args = parser.parse_args()

    root = Path(args.workspace).resolve()
    manifest_path = root / "offer-os.json"
    if manifest_path.exists() and not args.force:
        raise SystemExit(f"{manifest_path} already exists. Use --force to overwrite.")

    for folder in [
        "assets",
        "assets/ads",
        "assets/page",
        "assets/pdf",
        "assets/vsl",
        "assets/dashboard",
        "copy",
        "sales-page",
        "workbook",
        "presentation",
        "output/email",
        "output/pdf",
        "output/pdf/render-check",
        "output/presentation",
        "output/qa",
        "output/playwright",
    ]:
        (root / folder).mkdir(parents=True, exist_ok=True)

    manifest = {
        "schema": "offer-os/v1",
        "mode": args.mode,
        "offerName": args.name,
        "slug": slugify(args.name),
        "audience": args.audience,
        "problem": args.problem,
        "price": args.price,
        "designSource": {
            "type": args.design_source_type,
            "path": args.design_source_path,
            "url": args.design_source_url,
            "notes": "",
        },
        "brand": {
            "logo": "",
            "primaryColor": "",
            "accentColor": "",
            "fontHeading": "",
            "fontBody": "",
        },
        "modules": DEFAULT_MODULES,
        "artifacts": [],
        "assumptions": [],
        "qa": {
            "lastRun": "",
            "status": "not_run",
            "technical": {
                "status": "not_run",
                "issues": [],
                "warnings": [],
            },
            "commercial": {
                "status": "not_run",
                "issues": [],
                "warnings": [],
            },
            "issues": [],
        },
        "quality": {
            "pdf": {},
            "logo": {},
            "vsl": {},
            "images": {},
            "salesPage": {},
            "dashboard": {},
        },
        "commercialAudit": {
            "status": "not_run",
            "scores": {},
            "blockingIssues": [],
        },
        "createdAt": datetime.now(timezone.utc).isoformat(),
        "status": "in_progress",
    }

    manifest_path.write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
    print(f"Created {manifest_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
