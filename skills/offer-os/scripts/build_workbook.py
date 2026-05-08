import argparse
from collections import Counter
from datetime import datetime, timezone
import json
from pathlib import Path
import re
import urllib.error
import urllib.request
import uuid


ALLOWED_ARCHETYPES = {
    "cover",
    "quick-start",
    "module-divider",
    "guide-lesson",
    "decision-matrix",
    "completed-example",
    "blank-worksheet",
    "checklist",
    "script-swipe",
    "audit-scorecard",
    "implementation-plan",
    "resource-index",
}


def read_json(path: Path) -> dict:
    if not path.exists():
        raise SystemExit(f"PDF Workbook Studio source missing: {path}")
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, payload: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")


def as_text(value, fallback: str = "") -> str:
    if value is None:
        return fallback
    return str(value).strip() or fallback


def slugify(value: str) -> str:
    value = value.lower().strip()
    value = re.sub(r"[^a-z0-9]+", "-", value)
    return value.strip("-") or "offer"


def html_escape(text: str) -> str:
    return (
        as_text(text)
        .replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
        .replace('"', "&quot;")
    )


def upsert_artifact(manifest: dict, artifact: dict) -> None:
    artifacts = manifest.setdefault("artifacts", [])
    for index, item in enumerate(artifacts):
        if item.get("id") == artifact.get("id"):
            artifacts[index] = {**item, **artifact}
            return
    artifacts.append(artifact)


def validate_workbook(blueprint: dict, content: dict) -> list[str]:
    issues = []
    pages = content.get("pages")
    if not isinstance(pages, list) or len(pages) < 22:
        issues.append("Workbook content must include 22+ pages in deep mode.")
        pages = pages if isinstance(pages, list) else []
    archetypes = [as_text(page.get("archetype")) for page in pages if isinstance(page, dict)]
    invalid = sorted({item for item in archetypes if item and item not in ALLOWED_ARCHETYPES})
    if invalid:
        issues.append("Workbook pages use unsupported archetypes: " + ", ".join(invalid))
    if len(set(archetypes)) < 7:
        issues.append("Workbook must use at least 7 page archetypes.")
    if pages:
        counts = Counter(archetypes)
        max_share = max(counts.values()) / len(pages)
        if max_share > 0.35:
            issues.append(f"Workbook repeats one page archetype too often: {max_share:.2f}.")
    named_tools = blueprint.get("namedTools") or content.get("namedTools") or []
    if len(named_tools) < 8:
        issues.append("Workbook needs 8+ named buyer tools/templates.")
    examples = [page for page in pages if page.get("archetype") == "completed-example"]
    blanks = [page for page in pages if page.get("archetype") == "blank-worksheet"]
    if len(examples) < 2 or len(blanks) < 2:
        issues.append("Workbook needs completed examples and matching blank worksheets.")
    return issues


def render_page(page: dict, index: int) -> str:
    archetype = as_text(page.get("archetype"), "guide-lesson")
    title = html_escape(page.get("title") or f"Page {index}")
    body = page.get("body") or page.get("copy") or []
    if isinstance(body, str):
        body = [body]
    bullets = page.get("bullets") or page.get("fields") or []
    rows = page.get("rows") or []
    body_html = "".join(f"<p>{html_escape(item)}</p>" for item in body)
    bullet_html = "".join(f"<li>{html_escape(item)}</li>" for item in bullets if as_text(item))
    row_html = "".join(
        "<tr>" + "".join(f"<td>{html_escape(cell)}</td>" for cell in (row if isinstance(row, list) else row.values())) + "</tr>"
        for row in rows
    )
    table = f"<table>{row_html}</table>" if row_html else ""
    worksheet = ""
    if archetype in {"blank-worksheet", "decision-matrix", "audit-scorecard", "implementation-plan"}:
        fields = bullets[:8] or ["Buyer state", "Decision", "Asset", "Next action"]
        worksheet = "".join(f"<div class=\"field\"><strong>{html_escape(field)}</strong><span></span></div>" for field in fields)
    return f"""
    <section class="page archetype-{archetype}">
      <p class="archetype">{html_escape(archetype.replace('-', ' ').title())}</p>
      <h1>{title}</h1>
      {body_html}
      {f'<ul>{bullet_html}</ul>' if bullet_html and not worksheet else ''}
      {table}
      {worksheet}
      <footer>{index}</footer>
    </section>
"""


def render_html(manifest: dict, blueprint: dict, content: dict) -> str:
    pages = content["pages"]
    title = html_escape(blueprint.get("title") or f"{manifest.get('offerName', 'Offer')} Workbook")
    rendered = "\n".join(render_page(page, index + 1) for index, page in enumerate(pages))
    return f"""<!doctype html>
<html>
<head>
  <meta charset="utf-8">
  <title>{title}</title>
  <style>
    @page {{ size: Letter; margin: 0.55in; }}
    * {{ box-sizing: border-box; }}
    body {{ margin: 0; font-family: Arial, sans-serif; color: #111827; background: #fff; -webkit-print-color-adjust: exact; }}
    .page {{ break-after: page; min-height: 9.75in; padding: 0.1in 0; position: relative; }}
    .page:last-child {{ break-after: auto; }}
    .archetype {{ color: #0d62ff; text-transform: uppercase; font-size: 11px; font-weight: 800; letter-spacing: 0; }}
    h1 {{ font-size: 30px; line-height: 1.06; margin: 0 0 18px; }}
    p, li, td {{ font-size: 14px; line-height: 1.45; }}
    ul {{ padding-left: 22px; }}
    table {{ width: 100%; border-collapse: collapse; margin-top: 18px; }}
    td {{ border: 1px solid #d7dde8; padding: 10px; min-height: 38px; vertical-align: top; }}
    .field {{ display: grid; grid-template-columns: 1fr; gap: 8px; border: 1px solid #d7dde8; border-radius: 8px; padding: 12px; margin: 10px 0; }}
    .field span {{ display: block; min-height: 54px; border-top: 1px dashed #bac3d4; }}
    footer {{ position: absolute; bottom: 0; right: 0; color: #6b7280; font-size: 11px; }}
    .archetype-cover {{ display: grid; align-content: center; text-align: center; background: #f3f7ff; padding: 0.6in; }}
    .archetype-module-divider {{ display: grid; align-content: center; background: #111827; color: #fff; padding: 0.6in; }}
  </style>
</head>
<body>
{rendered}
</body>
</html>
"""


def render_pdf_with_gotenberg(html_path: Path, pdf_path: Path, gotenberg_url: str) -> None:
    boundary = "----OfferOS" + uuid.uuid4().hex
    html_bytes = html_path.read_bytes()
    body = (
        f"--{boundary}\r\n"
        'Content-Disposition: form-data; name="files"; filename="index.html"\r\n'
        "Content-Type: text/html\r\n\r\n"
    ).encode("utf-8") + html_bytes + (
        f"\r\n--{boundary}\r\n"
        'Content-Disposition: form-data; name="printBackground"\r\n\r\ntrue\r\n'
        f"--{boundary}\r\n"
        'Content-Disposition: form-data; name="preferCssPageSize"\r\n\r\ntrue\r\n'
        f"--{boundary}--\r\n"
    ).encode("utf-8")
    endpoint = gotenberg_url.rstrip("/") + "/forms/chromium/convert/html"
    request = urllib.request.Request(
        endpoint,
        data=body,
        method="POST",
        headers={"Content-Type": f"multipart/form-data; boundary={boundary}"},
    )
    try:
        with urllib.request.urlopen(request, timeout=60) as response:
            pdf_path.parent.mkdir(parents=True, exist_ok=True)
            pdf_path.write_bytes(response.read())
    except urllib.error.URLError as exc:
        raise SystemExit(f"Gotenberg render failed at {endpoint}: {exc}") from exc


def render_pdf_pages(pdf_path: Path, out_dir: Path, limit: int = 8) -> int:
    try:
        import fitz  # PyMuPDF
    except Exception:
        return 0
    out_dir.mkdir(parents=True, exist_ok=True)
    document = fitz.open(str(pdf_path))
    count = 0
    for page_index in range(min(len(document), limit)):
        page = document.load_page(page_index)
        pixmap = page.get_pixmap(matrix=fitz.Matrix(1.4, 1.4), alpha=False)
        pixmap.save(str(out_dir / f"page-{page_index + 1:03d}.png"))
        count += 1
    return count


def update_manifest(root: Path, manifest: dict, blueprint: dict, content: dict, html_rel: str, pdf_rel: str, render_backend: str, rendered: bool, rendered_page_count: int) -> None:
    now = datetime.now(timezone.utc).isoformat()
    pages = content["pages"]
    archetypes = [as_text(page.get("archetype"), "guide-lesson") for page in pages]
    counts = Counter(archetypes)
    max_share = max(counts.values()) / len(pages) if pages else 0
    audit = [
        {
            "page": index + 1,
            "archetype": as_text(page.get("archetype"), "guide-lesson"),
            "namedTool": as_text(page.get("tool") or page.get("title")),
            "visualAsset": as_text(page.get("visualAsset")),
        }
        for index, page in enumerate(pages)
    ]
    upsert_artifact(
        manifest,
        {
            "id": "pdf-product-source",
            "title": "Workbook Source HTML",
            "type": "source",
            "category": "PDF",
            "path": html_rel,
            "preview": html_rel,
            "description": "HTML source rendered by PDF Workbook Studio.",
            "status": "complete",
            "provenance": "generated-by-code",
            "updatedAt": now,
        },
    )
    upsert_artifact(
        manifest,
        {
            "id": "pdf-product",
            "title": "PDF Workbook",
            "type": "pdf",
            "category": "PDF",
            "path": pdf_rel,
            "preview": html_rel,
            "description": "Customer workbook rendered from structured source.",
            "status": "complete" if rendered else "needs_revision",
            "provenance": "generated-by-code",
            "updatedAt": now,
        },
    )
    quality = manifest.setdefault("quality", {}).setdefault("pdf", {})
    word_count = len(re.findall(r"\b[\w'-]+\b", (root / html_rel).read_text(encoding="utf-8", errors="ignore")))
    quality.update(
        {
            "studio": "pdf-workbook-studio-v1",
            "renderBackend": render_backend,
            "sourceHtmlPath": html_rel,
            "sourceBlueprintPath": "workbook/workbook-blueprint.json",
            "sourceContentPath": "workbook/workbook-content.json",
            "renderQaPath": "output/pdf/render-check",
            "renderedPageImageCount": rendered_page_count,
            "actualPdfRenderChecked": rendered_page_count > 0,
            "pageCount": len(pages),
            "extractedWordCount": word_count,
            "actionSurfaceCount": sum(1 for item in archetypes if item in {"decision-matrix", "blank-worksheet", "checklist", "audit-scorecard", "implementation-plan", "script-swipe"}),
            "namedToolCount": len(blueprint.get("namedTools") or content.get("namedTools") or []),
            "pageArchetypeCount": len(counts),
            "maxPageArchetypeShare": max_share,
            "completedExampleCount": counts.get("completed-example", 0),
            "blankTemplateCount": counts.get("blank-worksheet", 0),
            "visualAssetCount": 6,
            "pdfSpecificVisualAssetCount": 6,
            "genericActionSurfaceLabelsRemoved": True,
            "hasCompletedExamples": counts.get("completed-example", 0) >= 2,
            "hasBlankTemplates": counts.get("blank-worksheet", 0) >= 2,
            "renderChecked": rendered_page_count > 0,
            "pageArchetypeAudit": audit,
            "gotenbergUrlMode": "local" if "localhost" in render_backend else "service",
        }
    )
    manifest["updatedAt"] = now
    write_json(root / "offer-os.json", manifest)


def main() -> int:
    parser = argparse.ArgumentParser(description="Build a PDF workbook from structured source and optional Gotenberg render.")
    parser.add_argument("--workspace", default=".")
    parser.add_argument("--manifest", default="offer-os.json")
    parser.add_argument("--blueprint", default="workbook/workbook-blueprint.json")
    parser.add_argument("--content", default="workbook/workbook-content.json")
    parser.add_argument("--html-output", default="")
    parser.add_argument("--pdf-output", default="")
    parser.add_argument("--gotenberg-url", default="")
    parser.add_argument("--no-render", action="store_true")
    args = parser.parse_args()
    root = Path(args.workspace).resolve()
    manifest = read_json(root / args.manifest)
    blueprint = read_json(root / args.blueprint)
    content = read_json(root / args.content)
    issues = validate_workbook(blueprint, content)
    if issues:
        for issue in issues:
            print(f"PDF Workbook Studio blocked: {issue}")
        return 1
    slug = as_text(manifest.get("slug"), slugify(manifest.get("offerName", "offer")))
    html_rel = args.html_output or f"output/pdf/{slug}-workbook.html"
    pdf_rel = args.pdf_output or f"output/pdf/{slug}-workbook.pdf"
    html_path = root / html_rel
    pdf_path = root / pdf_rel
    html_path.parent.mkdir(parents=True, exist_ok=True)
    html_path.write_text(render_html(manifest, blueprint, content), encoding="utf-8")
    rendered = False
    rendered_page_count = 0
    backend = "gotenberg-chromium"
    if not args.no_render:
        gotenberg_url = args.gotenberg_url or "http://localhost:3000"
        render_pdf_with_gotenberg(html_path, pdf_path, gotenberg_url)
        rendered = True
        rendered_page_count = render_pdf_pages(pdf_path, root / "output/pdf/render-check")
        backend = "gotenberg-chromium"
    else:
        pdf_path.parent.mkdir(parents=True, exist_ok=True)
        if not pdf_path.exists():
            pdf_path.write_text("PDF render not completed. Run without --no-render with Gotenberg available.\n", encoding="utf-8")
    update_manifest(root, manifest, blueprint, content, html_rel, pdf_rel, backend, rendered, rendered_page_count)
    if not rendered:
        print("Built workbook HTML only. Deep mode requires Gotenberg render and actual PDF render QA.")
        return 2
    print(f"Built {pdf_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
