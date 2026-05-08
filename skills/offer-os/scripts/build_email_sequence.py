import argparse
from datetime import datetime, timezone
from html import escape
import json
from pathlib import Path
import re


def read_json(path: Path) -> dict:
    if not path.exists():
        raise SystemExit(f"Email Launch Studio source missing: {path}. Create email-sequence.json first.")
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, payload: dict) -> None:
    path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")


def as_text(value, fallback: str = "") -> str:
    if value is None:
        return fallback
    return str(value).strip() or fallback


def slugify(value: str) -> str:
    value = value.lower().strip()
    value = re.sub(r"[^a-z0-9]+", "-", value)
    return value.strip("-") or "offer"


def upsert_artifact(manifest: dict, artifact: dict) -> None:
    artifacts = manifest.setdefault("artifacts", [])
    for index, item in enumerate(artifacts):
        if item.get("id") == artifact.get("id"):
            artifacts[index] = {**item, **artifact}
            return
    artifacts.append(artifact)


def body_blocks(email: dict) -> list[str]:
    blocks = email.get("bodyBlocks")
    if isinstance(blocks, list):
        return [as_text(item) for item in blocks if as_text(item)]
    body = as_text(email.get("body") or email.get("bodyText") or email.get("bodyHtml"))
    if body:
        return [body]
    raise SystemExit(f"Email {email.get('id', '?')} missing body/bodyBlocks.")


def validate_source(sequence: dict) -> list[str]:
    issues = []
    emails = sequence.get("emails")
    if not isinstance(emails, list):
        return ["email-sequence.json must contain an emails array."]
    if len(emails) < 7 and sequence.get("sequenceType", "launch") == "launch":
        issues.append(f"Launch Email Studio requires 7+ emails: {len(emails)} found.")
    required = [
        "sendTiming",
        "subject",
        "previewText",
        "campaignRole",
        "conversionJob",
        "beliefShift",
        "primaryObjection",
        "ctaLabel",
        "ctaUrl",
        "complianceNotes",
    ]
    seen_blocks: dict[str, int] = {}
    for index, email in enumerate(emails, 1):
        for key in required:
            if not as_text(email.get(key)):
                issues.append(f"Email {index} missing {key}.")
        blocks = body_blocks(email)
        if len(" ".join(blocks).split()) < 140:
            issues.append(f"Email {index} body is too thin for a publishable launch email.")
        for block in blocks:
            normalized = re.sub(r"\s+", " ", block.strip().lower())
            if len(normalized.split()) >= 8:
                seen_blocks[normalized] = seen_blocks.get(normalized, 0) + 1
    repeated = [block for block, count in seen_blocks.items() if count > 1]
    if repeated:
        issues.append("Email source repeats body blocks verbatim; revise before rendering.")
    urgency = as_text(sequence.get("urgencyBasis"))
    if sequence.get("framework", "").lower().find("launch") >= 0 and not urgency:
        issues.append("Launch email sequence must record a real urgencyBasis; fake urgency is not allowed.")
    return issues


def render_markdown(sequence: dict) -> str:
    lines = [
        "# Launch Email Sequence",
        "",
        f"Framework: {as_text(sequence.get('framework'), 'Belief-Shift Launch Sequence')}",
        f"Urgency basis: {as_text(sequence.get('urgencyBasis'), 'None recorded')}",
        "",
    ]
    for index, email in enumerate(sequence["emails"], 1):
        lines.extend(
            [
                f"## Email {index}",
                "",
                f"Send timing: {as_text(email.get('sendTiming'))}",
                f"Subject: {as_text(email.get('subject'))}",
                f"Preview: {as_text(email.get('previewText'))}",
                f"CTA: {as_text(email.get('ctaLabel'))} -> {as_text(email.get('ctaUrl'))}",
                "",
            ]
        )
        for block in body_blocks(email):
            lines.extend([block, ""])
    return "\n".join(lines).strip() + "\n"


def render_html(sequence: dict) -> str:
    articles = []
    for index, email in enumerate(sequence["emails"], 1):
        blocks = "\n".join(f"<p>{escape(block)}</p>" for block in body_blocks(email))
        articles.append(
            f"""
      <article class="email" data-email="{index}">
        <p class="meta">{escape(as_text(email.get('sendTiming')))}</p>
        <h2>{escape(as_text(email.get('subject')))}</h2>
        <p class="preview">{escape(as_text(email.get('previewText')))}</p>
        {blocks}
        <p><a href="{escape(as_text(email.get('ctaUrl'), '#checkout'))}">{escape(as_text(email.get('ctaLabel'), 'Get access'))}</a></p>
      </article>"""
        )
    return f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Email Sequence</title>
  <style>
    body {{ margin: 0; font-family: Arial, sans-serif; background: #f6f5f1; color: #111827; line-height: 1.55; }}
    main {{ width: min(860px, calc(100% - 32px)); margin: 0 auto; padding: 48px 0; }}
    .email {{ background: #fff; border: 1px solid #ddd; border-radius: 8px; padding: 28px; margin: 0 0 22px; }}
    .meta, .preview {{ color: #53606f; font-weight: 700; }}
    a {{ color: #0d62ff; font-weight: 800; }}
  </style>
</head>
<body>
  <main>
    <h1>Launch Email Sequence</h1>
    {''.join(articles)}
  </main>
</body>
</html>
"""


def update_manifest(root: Path, manifest: dict, sequence: dict, markdown_path: str, html_path: str) -> None:
    now = datetime.now(timezone.utc).isoformat()
    upsert_artifact(
        manifest,
        {
            "id": "email-sequence",
            "title": "Launch Email Sequence",
            "type": "email",
            "category": "Emails",
            "path": markdown_path,
            "preview": html_path,
            "description": "Structured launch email sequence rendered by Email Launch Studio.",
            "status": "complete",
            "provenance": "generated-by-code",
            "updatedAt": now,
        },
    )
    upsert_artifact(
        manifest,
        {
            "id": "email-sequence-source",
            "title": "Email Sequence Source",
            "type": "source",
            "category": "Emails",
            "path": "email-sequence.json",
            "preview": "email-sequence.json",
            "description": "Canonical Email Launch Studio source.",
            "status": "complete",
            "provenance": "manual",
            "updatedAt": now,
        },
    )
    emails = sequence["emails"]
    quality = manifest.setdefault("quality", {}).setdefault("emails", {})
    quality.update(
        {
            "studio": "email-launch-studio-v1",
            "emailCount": len(emails),
            "framework": as_text(sequence.get("framework")),
            "hasSendTiming": all(as_text(item.get("sendTiming")) for item in emails),
            "hasPreviewText": all(as_text(item.get("previewText")) for item in emails),
            "hasCampaignRoles": all(as_text(item.get("campaignRole")) for item in emails),
            "distinctConversionJobs": len({as_text(item.get("conversionJob")) for item in emails}),
            "repeatedBodyBlocksChecked": True,
            "ctaCount": sum(1 for item in emails if as_text(item.get("ctaLabel")) and as_text(item.get("ctaUrl"))),
            "urgencyBasisValid": bool(as_text(sequence.get("urgencyBasis"))) or sequence.get("sequenceType") != "launch",
        }
    )
    manifest["updatedAt"] = now
    write_json(root / "offer-os.json", manifest)


def main() -> int:
    parser = argparse.ArgumentParser(description="Build launch emails from email-sequence.json.")
    parser.add_argument("--workspace", default=".")
    parser.add_argument("--manifest", default="offer-os.json")
    parser.add_argument("--source", default="email-sequence.json")
    parser.add_argument("--markdown-output", default="copy/launch-emails.md")
    parser.add_argument("--html-output", default="copy/launch-emails.html")
    args = parser.parse_args()
    root = Path(args.workspace).resolve()
    manifest = read_json(root / args.manifest)
    sequence = read_json(root / args.source)
    issues = validate_source(sequence)
    if issues:
        for issue in issues:
            print(f"Email Launch Studio blocked: {issue}")
        return 1
    markdown_path = root / args.markdown_output
    html_path = root / args.html_output
    markdown_path.parent.mkdir(parents=True, exist_ok=True)
    html_path.parent.mkdir(parents=True, exist_ok=True)
    markdown_path.write_text(render_markdown(sequence), encoding="utf-8")
    html_path.write_text(render_html(sequence), encoding="utf-8")
    update_manifest(root, manifest, sequence, args.markdown_output, args.html_output)
    print(f"Built {markdown_path}")
    print(f"Built {html_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
