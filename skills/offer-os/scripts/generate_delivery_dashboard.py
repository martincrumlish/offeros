import argparse
from collections import defaultdict
import html
import json
from pathlib import Path


IMAGE_EXTS = {".png", ".jpg", ".jpeg", ".webp", ".gif"}
HTML_EXTS = {".html", ".htm"}
PDF_EXTS = {".pdf"}
DECK_EXTS = {".pptx", ".ppt"}


def load_manifest(path: Path) -> dict:
    if not path.exists():
        raise SystemExit(f"Manifest not found: {path}")
    return json.loads(path.read_text(encoding="utf-8"))


def infer_type(path_value: str, explicit: str = "") -> str:
    if explicit:
        return explicit
    suffix = Path(path_value).suffix.lower()
    if suffix in IMAGE_EXTS:
        return "image"
    if suffix in HTML_EXTS:
        return "page"
    if suffix in PDF_EXTS:
        return "pdf"
    if suffix in DECK_EXTS:
        return "deck"
    return "document"


def esc(value: str) -> str:
    return html.escape(str(value or ""), quote=True)


def browser_safe_preview(artifact: dict, artifacts: list[dict]) -> str:
    path = artifact.get("path", "")
    preview = artifact.get("preview") or path
    kind = infer_type(path, artifact.get("type", ""))
    if kind == "deck" and Path(preview).suffix.lower() in DECK_EXTS:
        category = artifact.get("category")
        for candidate in artifacts:
            if candidate is artifact:
                continue
            if category and candidate.get("category") != category:
                continue
            candidate_path = candidate.get("path", "")
            candidate_suffix = Path(candidate_path).suffix.lower()
            if candidate_suffix in HTML_EXTS or candidate_suffix in IMAGE_EXTS:
                return candidate.get("preview") or candidate_path
    return preview


def card(artifact: dict, artifacts: list[dict]) -> str:
    path = artifact.get("path", "")
    preview = browser_safe_preview(artifact, artifacts)
    title = artifact.get("title") or Path(path).name
    kind = infer_type(path, artifact.get("type", ""))
    description = artifact.get("description", "")
    status = artifact.get("status", "")
    provenance = artifact.get("provenance", "")
    quality = artifact.get("quality", {})
    score_text = ""
    if isinstance(quality, dict) and any(quality.get(key) for key in ["buyerValue", "usability", "trust"]):
        score_text = f" value {quality.get('buyerValue', '-')}/5 | use {quality.get('usability', '-')}/5 | trust {quality.get('trust', '-')}/5"
    meta_bits = [esc(kind)]
    if status:
        meta_bits.append(esc(status))
    if provenance:
        meta_bits.append("prov: " + esc(provenance))
    if score_text:
        meta_bits.append(esc(score_text))
    thumb = ""
    if Path(preview).suffix.lower() in IMAGE_EXTS:
        thumb = f'<img src="{esc(preview)}" alt="{esc(title)}">'
    return f"""
        <button class="card" type="button" data-title="{esc(title)}" data-type="{esc(kind)}" data-path="{esc(path)}" data-preview="{esc(preview)}">
          <div class="thumb">{thumb}</div>
          <div class="card-copy">
            <span>{" - ".join(meta_bits)}</span>
            <strong>{esc(title)}</strong>
            <small>{esc(description)}</small>
          </div>
        </button>"""


def grouped_cards(artifacts: list[dict]) -> str:
    groups = defaultdict(list)
    for artifact in artifacts:
        groups[artifact.get("category") or "General"].append(artifact)
    if not groups:
        return '<section class="group"><p>No artifacts registered yet.</p></section>'
    html_parts = []
    for category in sorted(groups):
        cards = "\n".join(card(item, artifacts) for item in groups[category])
        html_parts.append(f"""
      <section class="group">
        <div class="group-head">
          <h2>{esc(category)}</h2>
          <p>{len(groups[category])} asset{'s' if len(groups[category]) != 1 else ''}</p>
        </div>
        <div class="grid">{cards}
        </div>
      </section>""")
    return "\n".join(html_parts)


def render(manifest: dict) -> str:
    offer_name = manifest.get("offerName", "OfferOS Project")
    audience = manifest.get("audience", "")
    price = manifest.get("price", "")
    mode = manifest.get("mode", "deep")
    logo = manifest.get("brand", {}).get("logo", "")
    logo_markup = f'<img class="logo" src="{esc(logo)}" alt="{esc(offer_name)}">' if logo else '<strong class="wordmark">OfferOS</strong>'
    cards = grouped_cards(manifest.get("artifacts", []))
    meta = " - ".join([item for item in [mode.upper(), audience, f"${price}" if str(price).isdigit() else str(price)] if item])
    return f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{esc(offer_name)} Delivery Dashboard</title>
  <style>
    :root {{ --bg:#050505; --panel:#111611; --panel2:#080a08; --line:rgba(255,255,255,.12); --lime:#cfff05; --text:#fff; --muted:#c3c9d4; }}
    * {{ box-sizing:border-box; }}
    body {{ margin:0; background:radial-gradient(circle at 20% 0%,rgba(207,255,5,.12),transparent 30%),linear-gradient(rgba(255,255,255,.025) 1px,transparent 1px),linear-gradient(90deg,rgba(255,255,255,.025) 1px,transparent 1px),var(--bg); background-size:auto,56px 56px,56px 56px; color:var(--text); font-family:Arial,sans-serif; }}
    button {{ font:inherit; }}
    .shell {{ width:min(1180px,calc(100% - 36px)); margin:0 auto; }}
    header {{ border-bottom:1px solid var(--line); background:rgba(5,5,5,.72); }}
    .top {{ min-height:86px; display:flex; align-items:center; justify-content:space-between; gap:18px; }}
    .logo {{ max-width:min(280px,56vw); max-height:54px; object-fit:contain; }}
    .wordmark {{ color:var(--lime); letter-spacing:.08em; text-transform:uppercase; }}
    .label {{ color:var(--lime); font-size:13px; font-weight:900; letter-spacing:.12em; text-transform:uppercase; text-align:right; }}
    .hero {{ padding:38px 0 18px; }}
    h1 {{ max-width:900px; font-size:clamp(42px,8vw,82px); line-height:.96; margin:0 0 14px; }}
    .meta {{ color:var(--muted); font-size:18px; line-height:1.45; }}
    .group {{ padding:28px 0; }}
    .group-head {{ display:flex; justify-content:space-between; align-items:end; gap:16px; margin-bottom:16px; }}
    h2 {{ margin:0; font-size:clamp(28px,4vw,44px); }}
    .group-head p {{ margin:0; color:var(--muted); }}
    .grid {{ display:grid; grid-template-columns:repeat(3,1fr); gap:16px; }}
    .card {{ min-height:230px; display:grid; grid-template-rows:auto 1fr; text-align:left; color:inherit; background:rgba(17,22,17,.9); border:1px solid var(--line); border-radius:10px; padding:0; overflow:hidden; cursor:pointer; box-shadow:rgba(0,0,0,.45) 0 24px 60px -36px; }}
    .thumb {{ min-height:118px; display:grid; place-items:center; background:radial-gradient(circle at 50% 20%,rgba(207,255,5,.1),transparent 42%),var(--panel2); border-bottom:1px solid var(--line); }}
    .thumb img {{ width:100%; aspect-ratio:16/9; object-fit:contain; padding:12px; }}
    .card-copy {{ padding:18px; }}
    .card span {{ color:var(--lime); font-size:11px; font-weight:900; letter-spacing:.09em; text-transform:uppercase; }}
    .card strong {{ display:block; font-size:21px; line-height:1.1; margin:8px 0; }}
    .card small {{ display:block; color:var(--muted); line-height:1.4; }}
    .modal {{ display:none; position:fixed; inset:0; z-index:20; padding:22px; background:rgba(0,0,0,.78); backdrop-filter:blur(14px); }}
    .modal.open {{ display:grid; place-items:center; }}
    .frame {{ width:min(1380px,100%); height:min(880px,calc(100vh - 44px)); display:grid; grid-template-rows:auto 1fr; background:#050505; border:1px solid rgba(207,255,5,.24); border-radius:16px; overflow:hidden; box-shadow:rgba(207,255,5,.1) 0 0 0 3px,rgba(0,0,0,.7) 0 36px 90px -20px; }}
    .bar {{ display:flex; justify-content:space-between; align-items:center; gap:16px; padding:14px 16px; border-bottom:1px solid var(--line); background:#080a08; }}
    .bar-title {{ min-width:0; }}
    .bar-title span {{ display:block; color:var(--lime); font-size:11px; font-weight:900; letter-spacing:.1em; text-transform:uppercase; }}
    .bar-title strong {{ display:block; overflow:hidden; text-overflow:ellipsis; white-space:nowrap; font-size:20px; }}
    .actions {{ display:flex; gap:10px; align-items:center; flex-shrink:0; }}
    a,.close {{ background:var(--lime); color:#050505; border:0; border-radius:8px; padding:12px 16px; font-weight:900; text-decoration:none; cursor:pointer; }}
    .close {{ width:44px; padding:0; font-size:24px; }}
    iframe {{ width:100%; height:100%; border:0; background:white; }}
    .image-preview {{ width:100%; height:100%; display:grid; place-items:center; overflow:auto; padding:24px; background:#070807; }}
    .image-preview img {{ max-width:100%; max-height:100%; width:auto; border-radius:10px; border:1px solid var(--line); }}
    .note {{ max-width:680px; margin:0 auto 16px; color:var(--muted); text-align:center; line-height:1.45; }}
    @media (max-width:900px) {{ .grid {{ grid-template-columns:1fr; }} .group-head {{ display:block; }} .actions a {{ display:none; }} h1 {{ font-size:44px; }} }}
  </style>
</head>
<body data-offeros-dashboard="v2-modal">
  <header><div class="shell top">{logo_markup}<div class="label">Delivery Dashboard</div></div></header>
  <main class="shell">
    <section class="hero">
      <h1>{esc(offer_name)}</h1>
      <div class="meta">{esc(meta or "Preview and open every asset created for this offer.")}</div>
    </section>
    {cards}
  </main>
  <div class="modal" id="modal" aria-hidden="true">
    <div class="frame" role="dialog" aria-modal="true" aria-labelledby="modalTitle">
      <div class="bar">
        <div class="bar-title"><span id="modalType">Preview</span><strong id="modalTitle"></strong></div>
        <div class="actions"><a id="open" href="#" target="_blank" rel="noreferrer">Open File</a><button class="close" id="close" type="button" aria-label="Close">&times;</button></div>
      </div>
      <div id="body"></div>
    </div>
  </div>
  <script>
    const modal = document.getElementById('modal');
    const body = document.getElementById('body');
    const title = document.getElementById('modalTitle');
    const typeLabel = document.getElementById('modalType');
    const open = document.getElementById('open');
    const close = document.getElementById('close');
    function isImage(path) {{ return /\\.(png|jpe?g|webp|gif)$/i.test(path); }}
    function show(card) {{
      const preview = card.dataset.preview;
      const path = card.dataset.path;
      const type = card.dataset.type;
      title.textContent = card.dataset.title;
      typeLabel.textContent = type + ' preview';
      open.href = path;
      open.textContent = type === 'deck' ? 'Open Deck' : 'Open File';
      if (isImage(preview)) {{
        const note = type === 'deck' ? '<p class="note">This deck uses a browser-safe preview. Open the original deck from the button above.</p>' : '';
        body.innerHTML = `<div class="image-preview"><div>${{note}}<img src="${{preview}}" alt=""></div></div>`;
      }} else {{
        body.innerHTML = `<iframe src="${{preview}}" title="${{card.dataset.title}}"></iframe>`;
      }}
      modal.classList.add('open');
      modal.setAttribute('aria-hidden','false');
      close.focus();
    }}
    function hide() {{ modal.classList.remove('open'); modal.setAttribute('aria-hidden','true'); body.innerHTML=''; }}
    document.querySelectorAll('.card').forEach(card => card.addEventListener('click', () => show(card)));
    close.addEventListener('click', hide);
    modal.addEventListener('click', event => {{ if (event.target === modal) hide(); }});
    document.addEventListener('keydown', event => {{ if (event.key === 'Escape' && modal.classList.contains('open')) hide(); }});
  </script>
</body>
</html>
"""


def main() -> int:
    parser = argparse.ArgumentParser(description="Generate an OfferOS delivery dashboard from offer-os.json.")
    parser.add_argument("--manifest", default="offer-os.json")
    parser.add_argument("--output", default="delivery-dashboard.html")
    parser.add_argument("--force", action="store_true")
    args = parser.parse_args()

    manifest_path = Path(args.manifest)
    output_path = Path(args.output)
    if output_path.exists() and not args.force:
        raise SystemExit(f"{output_path} already exists. Use --force to overwrite.")
    output_path.write_text(render(load_manifest(manifest_path)), encoding="utf-8")
    print(f"Created {output_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
