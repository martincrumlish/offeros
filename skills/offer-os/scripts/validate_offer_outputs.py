import argparse
from datetime import datetime, timezone
from html import unescape
from io import BytesIO
import json
import math
import posixpath
from pathlib import Path
import re
import zipfile

from build_copy import (
    COPY_FRAMEWORK,
    STUDIO_VERSION as COPY_STUDIO_VERSION,
    validate_copy_plan as validate_copy_plan_source,
    section_rows as copy_plan_section_rows,
    list_of_dicts as copy_list_of_dicts,
    as_text as copy_as_text,
)


TEXT_EXTS = {".html", ".md", ".txt", ".json", ".css", ".js"}
IMAGE_EXTS = {".png", ".jpg", ".jpeg", ".webp", ".gif", ".svg"}
BITMAP_EXTS = {".png", ".jpg", ".jpeg", ".webp"}
BAD_TOKENS = [
    "lorem ipsum",
    "[placeholder]",
    "replace this",
    "todo:",
    "tbd",
    "your text here",
    "image placeholder",
]

DEEP_REQUIRED_IDS = [
    "offer-architecture",
    "design-guide",
    "logo",
    "copy-plan",
    "visual-asset-plan",
    "sales-copy",
    "sales-page-blueprint",
    "theme",
    "sales-page",
    "pdf-product-source",
    "pdf-product",
    "facebook-ads",
    "facebook-ad-image-1",
    "facebook-ad-image-2",
    "facebook-ad-image-3",
    "email-sequence",
    "vsl-deck",
    "vsl-preview",
    "delivery-dashboard",
    "qa-notes",
]

ALLOWED_PROVENANCE = {
    "imagegen",
    "imagegen-final",
    "imagegen-composite",
    "provided",
    "licensed",
    "screenshot",
    "html-css",
    "manual",
    "generated-by-code",
}

IMAGEGEN_CREATIVE_PROVENANCE = {
    "imagegen",
    "imagegen-final",
    "imagegen-composite",
    "provided",
    "licensed",
}

PRIMARY_CONVERSION_CREATIVE_PROVENANCE = {
    "imagegen-final",
    "provided",
    "licensed",
}

ALLOWED_LOCAL_POSTPROCESS = {
    "crop",
    "resize",
    "compression",
    "compress",
    "format-conversion",
    "format conversion",
    "format_conversion",
    "non-creative-qa-fix",
    "qa-fix",
}

CODE_RENDERED_PROVENANCE = {
    "html-css",
    "pil-generated",
    "generated-by-code",
    "manual",
    "screenshot",
}

IMAGEGEN_REQUIRED_CREATIVE_TERMS = {
    "product-bundle",
    "product bundle",
    "offer-stack-bundle",
    "offer stack bundle",
    "product-mockup",
    "product mockup",
    "hero-vsl-frame",
    "hero vsl frame",
    "hero-thumbnail",
    "hero thumbnail",
    "vsl-thumbnail",
    "vsl thumbnail",
    "buyer-situation-photo",
    "buyer situation photo",
}

MAJOR_ARTIFACTS = [
    "sales-page",
    "pdf-product",
    "facebook-ads",
    "email-sequence",
    "vsl-deck",
    "delivery-dashboard",
]

REQUIRED_SALES_PAGE_SECTIONS = [
    "header",
    "hero",
    "vsl",
    "problem",
    "agitation",
    "failed-alternatives",
    "mechanism",
    "proof",
    "before-after",
    "product",
    "offer-stack",
    "fit",
    "pricing",
    "guarantee",
    "faq",
    "final-cta",
]

ALLOWED_SALES_PAGE_TYPES = {
    "direct-response-long-form-vsl",
    "mechanism-led-product-page",
    "proof-led-case-study-page",
    "webinar-workshop-registration",
    "sales-letter-checkout",
}

ALLOWED_PAGE_KIT_ARCHETYPES = {
    "classic-vsl-longform",
    "modern-vsl-software",
    "one-page-tripwire",
    "challenge-workshop",
    "toolkit-workbook",
}

ALLOWED_PAGE_KIT_THEMES = {
    "light-saas-direct-response",
    "classic-direct-response",
    "bold-webinar",
    "premium-editorial",
    "fitness-performance",
    "creator-workshop",
}

BANNED_VISIBLE_VSL_STAGE_LABELS = {
    "hook",
    "problem",
    "agitate",
    "market",
    "mechanism",
    "proof",
    "offer",
    "cta",
    "objection",
    "close",
}

ALLOWED_VISUAL_KINDS = {
    "hero-vsl-frame",
    "product-mockup",
    "dashboard-mockup",
    "offer-stack-bundle",
    "mechanism-diagram",
    "comparison-visual",
    "proof-demo-visual",
    "buyer-situation-photo",
    "structured-panel",
    "worksheet-preview",
    "matrix-visual",
    "checklist-visual",
    "slide-pattern-interrupt",
    "ad-creative",
    "brand-frame",
}

MOCKUP_VISUAL_KINDS = {
    "product-mockup",
    "dashboard-mockup",
    "offer-stack-bundle",
}

IMAGEGEN_REQUIRED_VISUAL_KINDS = {
    "hero-vsl-frame",
    "product-mockup",
    "offer-stack-bundle",
    "buyer-situation-photo",
    "ad-creative",
}

REQUIRED_COPY_HEADINGS = [
    "# Sales Page Type",
    "# Section Blueprint",
    "# Hero",
    "# VSL Setup",
    "# Problem Diagnosis",
    "# Agitation",
    "# Failed Alternatives",
    "# Epiphany / New Insight",
    "# Unique Mechanism",
    "# Proof Or Demonstration",
    "# Before And After",
    "# Product Reveal",
    "## Feature-Benefit Breakdown",
    "## How It Works",
    "# Offer Stack",
    "# Who It Is For",
    "# Who It Is Not For",
    "# Pricing And Value",
    "# Guarantee",
    "# FAQ",
    "# Urgency / Scarcity Logic",
    "# Final CTA",
]

REQUIRED_BLUEPRINT_FIELDS = [
    "sectionId",
    "conversionJob",
    "targetWords",
    "beliefShift",
    "proofOrObjection",
    "visualKind",
    "copyAnchor",
    "ctaRole",
]

MIN_SECTION_WORDS = {
    "problem": 120,
    "agitation": 90,
    "failed-alternatives": 90,
    "mechanism": 120,
    "proof": 90,
    "before-after": 70,
    "product": 100,
    "fit": 70,
    "pricing": 60,
    "guarantee": 50,
}


def load_json(path: Path) -> dict:
    if not path.exists():
        raise SystemExit(f"Manifest not found: {path}")
    return json.loads(path.read_text(encoding="utf-8-sig"))


def scan_text(path: Path) -> list[str]:
    text = path.read_text(encoding="utf-8", errors="ignore").lower()
    return [token for token in BAD_TOKENS if token in text]


def text_for(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="ignore")


def markdown_section(text: str, heading: str) -> str:
    pattern = rf"(?ims)^\s*{re.escape(heading)}\s*$([\s\S]*?)(?=^\s*##\s+|\Z)"
    match = re.search(pattern, text)
    return match.group(1) if match else ""


def field_values(text: str, field: str) -> list[str]:
    pattern = rf"(?im)\b{re.escape(field)}\s*:\s*`?([^`\n|]+)"
    return [item.strip().strip("\"' .").lower() for item in re.findall(pattern, text)]


def markdown_field_rows(text: str) -> list[dict[str, str]]:
    rows = []
    current = {}
    for line in text.splitlines():
        match = re.match(r"\s*(?:-\s*)?([A-Za-z0-9_/-]+)\s*:\s*`?([^`\n|]+)", line)
        if not match:
            continue
        key = match.group(1).strip()
        value = match.group(2).strip().strip("\"' .")
        if key == "artifactTarget" and current:
            rows.append(current)
            current = {}
        current[key] = value
    if current:
        rows.append(current)
    return rows


def normalize_copy_anchor(value: str) -> str:
    value = value.strip().lower()
    section_match = re.search(r"data-offeros-section\s*=\s*[\"']?([a-z0-9-]+)", value)
    if section_match:
        return section_match.group(1)
    return re.sub(r"[^a-z0-9-]+", "", value)


def numeric_price(value) -> float:
    text = str(value or "")
    match = re.search(r"\d+(?:\.\d+)?", text.replace(",", ""))
    return float(match.group(0)) if match else 0.0


def pdf_targets(price: float) -> tuple[int, int, int]:
    if price and price <= 29:
        return 22, 8, 3500
    if price and price <= 99:
        return 25, 8, 4000
    return 35, 10, 6000


def pdf_tool_targets(price: float) -> tuple[int, int]:
    if price and price <= 29:
        return 8, 2
    if price and price <= 99:
        return 10, 3
    return 12, 3


def artifact_map(artifacts: list[dict]) -> dict[str, dict]:
    return {item.get("id", ""): item for item in artifacts if isinstance(item, dict)}


def artifact_path_map(artifacts: list[dict]) -> dict[str, dict]:
    by_path = {}
    for item in artifacts:
        if not isinstance(item, dict):
            continue
        for key in ["path", "preview"]:
            value = str(item.get(key, "")).replace("\\", "/").strip().lower()
            if value:
                by_path.setdefault(value, item)
    return by_path


def artifact_path(root: Path, artifact: dict | None) -> Path | None:
    if not artifact or not artifact.get("path"):
        return None
    return root / artifact["path"]


def validate_studio_source_control(root: Path, manifest: dict, issues: list[str]) -> None:
    generated_controllers = sorted((root / "scripts").glob("build_offer_system.*")) if (root / "scripts").exists() else []
    if generated_controllers:
        rels = ", ".join(str(path.relative_to(root)).replace("\\", "/") for path in generated_controllers[:5])
        issues.append(
            "Deep OfferOS runs must not use generated scripts/build_offer_system.* as the production source of truth. "
            "Use plugin-owned OfferOS Studio builders instead: " + rels
        )
    studios = manifest.get("quality", {}).get("studios", {})
    if isinstance(studios, dict) and studios.get("usesGeneratedBuildOfferSystem") is True:
        issues.append("Studio quality metadata says usesGeneratedBuildOfferSystem=true; production builders must live in the plugin.")


def count_pdf(path: Path) -> tuple[int | None, int | None]:
    try:
        from pypdf import PdfReader
    except Exception:
        return None, None
    reader = PdfReader(str(path))
    words = 0
    for page in reader.pages:
        try:
            words += len((page.extract_text() or "").split())
        except Exception:
            pass
    return len(reader.pages), words


def extract_pdf_text(path: Path) -> str:
    try:
        from pypdf import PdfReader
    except Exception:
        return ""
    try:
        reader = PdfReader(str(path))
    except Exception:
        return ""
    pages = []
    for page in reader.pages:
        try:
            pages.append(page.extract_text() or "")
        except Exception:
            pass
    return "\n".join(pages)


def count_pptx_slides(path: Path) -> int | None:
    try:
        with zipfile.ZipFile(path) as archive:
            return len([name for name in archive.namelist() if re.match(r"ppt/slides/slide\d+\.xml$", name)])
    except Exception:
        return None


def count_html_slides(text: str) -> int:
    patterns = [
        r"<section\b[^>]*class=[\"'][^\"']*\bslide\b",
        r"<div\b[^>]*class=[\"'][^\"']*\bslide\b",
        r"data-slide",
    ]
    return max(len(re.findall(pattern, text, re.I)) for pattern in patterns)


def has_section_marker(html_text: str, section_id: str) -> bool:
    escaped = re.escape(section_id)
    return bool(re.search(rf"data-offeros-section\s*=\s*[\"']{escaped}[\"']", html_text, re.I))


def section_html(html_text: str, section_id: str) -> str:
    escaped = re.escape(section_id)
    match = re.search(
        rf"<section\b(?=[^>]*data-offeros-section\s*=\s*[\"']{escaped}[\"'])[^>]*>.*?</section>",
        html_text,
        flags=re.I | re.S,
    )
    return match.group(0) if match else ""


def has_marker(html_text: str, marker: str) -> bool:
    return bool(re.search(rf"\b{re.escape(marker)}(?:\s|=|>)", html_text, flags=re.I))


def element_with_marker(html_text: str, marker: str) -> str:
    match = re.search(
        rf"<(?P<tag>[a-z][a-z0-9]*)\b(?=[^>]*\b{re.escape(marker)}(?:\s|=|>))[^>]*>.*?</(?P=tag)>",
        html_text,
        flags=re.I | re.S,
    )
    return match.group(0) if match else ""


def opening_tags_with_marker(html_text: str, marker: str) -> list[str]:
    return [
        match.group(0)
        for match in re.finditer(
            rf"<[a-z][a-z0-9]*\b(?=[^>]*\b{re.escape(marker)}(?:\s|=|>))[^>]*>",
            html_text,
            flags=re.I | re.S,
        )
    ]


def attr_value(tag_html: str, attr: str) -> str:
    match = re.search(rf"\b{re.escape(attr)}\s*=\s*[\"']([^\"']+)[\"']", tag_html, flags=re.I)
    return match.group(1).strip() if match else ""


def anchor_hrefs_with_marker(html_text: str, marker: str) -> list[str]:
    hrefs = []
    for match in re.finditer(r"<a\b([^>]*)>", html_text, flags=re.I | re.S):
        attrs = match.group(1)
        if not re.search(rf"\b{re.escape(marker)}(?:\s|=|>)", attrs, flags=re.I):
            continue
        href = re.search(r'\bhref\s*=\s*["\']([^"\']+)["\']', attrs, flags=re.I)
        if href:
            hrefs.append(href.group(1).strip())
    return hrefs


def html_attr_value(html_text: str, attr: str) -> str:
    match = re.search(rf"\b{re.escape(attr)}\s*=\s*[\"']([^\"']+)[\"']", html_text, flags=re.I)
    return match.group(1).strip() if match else ""


def order_form_signals(html_text: str) -> list[str]:
    signals = []
    lower = html_text.lower()
    if re.search(r"<form\b", html_text, flags=re.I):
        signals.append("contains a <form> element")
    marker_patterns = {
        "order form marker": r"data-offeros-section\s*=\s*[\"'](?:order|order-form|checkout|payment)[\"']|data-order-form|data-checkout-form",
        "payment field": r"\b(?:card number|credit card|cvv|cvc|expiry|expiration|billing address|stripe|paypal)\b",
        "order-form class/id": r"\b(?:order-form|checkout-form|payment-form|billing-form|card-field|order-bump)\b",
        "submit-order language": r"\b(?:complete order|submit order|place order|pay now)\b",
    }
    for label, pattern in marker_patterns.items():
        if re.search(pattern, lower, flags=re.I):
            signals.append(label)
    return signals


def section_opening_tag_has(html_text: str, section_id: str, pattern: str) -> bool:
    escaped = re.escape(section_id)
    match = re.search(
        rf"<section\b(?=[^>]*data-offeros-section\s*=\s*[\"']{escaped}[\"'])[^>]*>",
        html_text,
        flags=re.I | re.S,
    )
    return bool(match and re.search(pattern, match.group(0), flags=re.I))


def section_positions(html_text: str) -> dict[str, int]:
    positions = {}
    for match in re.finditer(r"<section\b[^>]*\bdata-offeros-section\s*=\s*[\"']([^\"']+)[\"'][^>]*>", html_text, flags=re.I | re.S):
        positions.setdefault(match.group(1).strip().lower(), match.start())
    return positions


def markdown_top_section(text: str, heading: str) -> str:
    pattern = rf"(?ims)^\s*{re.escape(heading)}\s*$([\s\S]*?)(?=^\s*#\s+|\Z)"
    match = re.search(pattern, text)
    return match.group(1) if match else ""


def hero_two_column_signals(html_text: str, hero_html: str) -> list[str]:
    signals = []
    class_tokens = []
    for class_value in re.findall(r'\bclass\s*=\s*["\']([^"\']+)["\']', hero_html, flags=re.I):
        class_tokens.extend(class_value.lower().split())
    bad_class_tokens = {
        "hero-grid",
        "hero-split",
        "hero-visual",
        "hero-mockup",
        "hero-cols",
        "hero-columns",
        "hero-two-col",
        "hero-two-column",
        "split-hero",
        "two-col",
        "two-column",
        "two-columns",
    }
    matched = sorted({token for token in class_tokens if token in bad_class_tokens})
    if matched:
        signals.append("hero uses two-column/split class names: " + ", ".join(matched))

    for style_block in re.findall(r"<style\b[^>]*>(.*?)</style>", html_text, flags=re.I | re.S):
        for selector, body in re.findall(r"([^{}]+)\{([^{}]+)\}", style_block, flags=re.S):
            selector_lower = selector.lower()
            body_lower = body.lower()
            if "hero" not in selector_lower:
                continue
            if "grid-template-columns" in body_lower:
                signals.append("hero CSS uses grid-template-columns")
                break
    return signals


def contains_expected_price(html_text: str, price: float) -> bool:
    if not price:
        return True
    expected = int(price)
    visible = visible_text_from_html(html_text)
    return bool(re.search(rf"\$\s*{expected}\b|\b{expected}\s+dollars?\b", visible, flags=re.I))


def generated_claim(artifact: dict) -> bool:
    text = f"{artifact.get('title', '')} {artifact.get('description', '')}".lower()
    return any(term in text for term in ["generated image", "ai-generated", "imagegen", "generated product", "generated tactical"])


def artifact_identity_text(artifact: dict) -> str:
    return " ".join(
        str(artifact.get(key, ""))
        for key in ["id", "title", "path", "preview", "category", "description"]
    ).lower()


def is_imagegen_required_creative(artifact: dict) -> bool:
    artifact_id = str(artifact.get("id", "")).lower()
    category = str(artifact.get("category", "")).lower()
    artifact_type = str(artifact.get("type", "")).lower()
    if artifact_id.startswith("facebook-ad-image") or (category == "ads" and artifact_type == "image"):
        return True
    identity = artifact_identity_text(artifact)
    return any(term in identity for term in IMAGEGEN_REQUIRED_CREATIVE_TERMS)


def bool_field(value) -> bool | None:
    if isinstance(value, bool):
        return value
    if isinstance(value, str):
        lowered = value.strip().lower()
        if lowered in {"true", "yes", "1"}:
            return True
        if lowered in {"false", "no", "0"}:
            return False
    return None


def list_field(value) -> list[str]:
    if isinstance(value, list):
        return [str(item).strip().lower() for item in value if str(item).strip()]
    if isinstance(value, str):
        cleaned = value.strip().strip("[]")
        if not cleaned:
            return []
        return [item.strip().strip("\"'` ").lower() for item in re.split(r"[,;]", cleaned) if item.strip()]
    return []


def primary_conversion_metadata_issues(item: dict, label: str) -> list[str]:
    provenance = str(item.get("provenance") or item.get("source/provenance") or "").strip().lower()
    if provenance in {"provided", "licensed"}:
        return []
    item_id = str(item.get("id") or item.get("artifactTarget") or item.get("filePath") or label)
    issues = []
    if provenance == "imagegen-composite" and bool_field(item.get("imagegenNativeComposite")) is not True:
        issues.append(
            f"{label} uses imagegen-composite without imagegenNativeComposite: true: {item_id}. "
            "Local composition does not qualify."
        )
    elif provenance not in PRIMARY_CONVERSION_CREATIVE_PROVENANCE and provenance != "imagegen-composite":
        issues.append(
            f"{label} must use source/provenance imagegen-final, provided, or licensed: {item_id}. "
            f"Found {provenance or 'missing'}."
        )
    if str(item.get("finalPixelsGeneratedBy", "")).strip().lower() != "imagegen":
        issues.append(f"{label} must record finalPixelsGeneratedBy: imagegen: {item_id}.")
    if bool_field(item.get("localCreativeOverlay")) is not False:
        issues.append(f"{label} must record localCreativeOverlay: false: {item_id}.")
    postprocess = list_field(item.get("localPostprocess"))
    if not postprocess:
        issues.append(f"{label} must record localPostprocess with only crop/resize/compression/format-conversion: {item_id}.")
    disallowed = sorted({item for item in postprocess if item not in ALLOWED_LOCAL_POSTPROCESS})
    if disallowed:
        issues.append(
            f"{label} localPostprocess contains creative operations, which are not allowed: "
            + ", ".join(disallowed)
            + f": {item_id}."
        )
    return issues


def validate_registered_creative_src(html_text: str, marker: str, label: str, by_path: dict[str, dict], issues: list[str]) -> None:
    for tag in opening_tags_with_marker(html_text, marker):
        src = attr_value(tag, "src")
        if not src or re.match(r"^(?:https?:|data:|#)", src, flags=re.I):
            continue
        normalized = src.split("?", 1)[0].split("#", 1)[0].lstrip("./").replace("\\", "/").lower()
        artifact = by_path.get(normalized)
        if not artifact:
            issues.append(f"{label} source must be registered in offer-os.json with imagegen provenance: {src}")
            continue
        for issue in primary_conversion_metadata_issues(artifact, label):
            issues.append(f"{issue} Source: {src}")


def quality_number(value) -> int:
    try:
        return int(value)
    except Exception:
        return 0


def quality_float(value) -> float:
    try:
        return float(value)
    except Exception:
        return 0.0


def visible_text_from_html(html_text: str) -> str:
    text = re.sub(r"<(script|style)\b[^>]*>.*?</\1>", " ", html_text, flags=re.I | re.S)
    text = re.sub(r"<[^>]+>", "\n", text)
    text = unescape(text)
    return re.sub(r"[ \t\r\f\v]+", " ", text)


def html_word_count(html_text: str) -> int:
    return len(re.findall(r"\b[\w'-]+\b", visible_text_from_html(html_text)))


def long_paragraphs(html_text: str, limit: int = 55) -> list[str]:
    findings = []
    for index, match in enumerate(re.finditer(r"<p\b[^>]*>(.*?)</p>", html_text, flags=re.I | re.S), 1):
        text = visible_text_from_html(match.group(1))
        word_count = len(re.findall(r"\b[\w'-]+\b", text))
        if word_count > limit:
            findings.append(f"paragraph {index}: {word_count} words")
    return findings


def empty_table_cells(html_text: str) -> int:
    empty_count = 0
    for match in re.finditer(r"<t[dh]\b[^>]*>(.*?)</t[dh]>", html_text, flags=re.I | re.S):
        content = match.group(1)
        if "<img" in content.lower():
            continue
        if len(re.findall(r"\b[\w'-]+\b", visible_text_from_html(content))) == 0:
            empty_count += 1
    return empty_count


def repeated_sentences(text: str, threshold: int = 4) -> list[tuple[str, int]]:
    counts: dict[str, int] = {}
    for sentence in re.split(r"[.!?]\s+|\n+", text):
        normalized = re.sub(r"\s+", " ", sentence.strip().lower())
        normalized = re.sub(r"[^a-z0-9 $%'-]+", "", normalized)
        if len(normalized.split()) < 6:
            continue
        counts[normalized] = counts.get(normalized, 0) + 1
    return sorted(
        [(sentence, count) for sentence, count in counts.items() if count >= threshold],
        key=lambda item: item[1],
        reverse=True,
    )


def repeated_body_blocks(html_text: str, threshold: int = 2) -> list[tuple[str, int]]:
    counts: dict[str, int] = {}
    for match in re.finditer(r"<(?:p|li|dd|figcaption)\b[^>]*>(.*?)</(?:p|li|dd|figcaption)>", html_text, flags=re.I | re.S):
        text = visible_text_from_html(match.group(1))
        normalized = re.sub(r"\s+", " ", text.strip().lower())
        normalized = re.sub(r"[^a-z0-9 $%'-]+", "", normalized)
        if len(normalized.split()) < 6:
            continue
        counts[normalized] = counts.get(normalized, 0) + 1
    return sorted(
        [(text, count) for text, count in counts.items() if count >= threshold],
        key=lambda item: item[1],
        reverse=True,
    )


def visible_lines(text: str) -> list[str]:
    return [line.strip() for line in re.split(r"[\r\n]+", text) if line.strip()]


def pptx_slide_texts(path: Path) -> list[list[str]]:
    try:
        with zipfile.ZipFile(path) as archive:
            names = sorted(
                [name for name in archive.namelist() if re.match(r"ppt/slides/slide\d+\.xml$", name)],
                key=lambda name: int(re.search(r"slide(\d+)\.xml$", name).group(1)),
            )
            slides = []
            for name in names:
                xml = archive.read(name).decode("utf-8", errors="ignore")
                slides.append([unescape(text) for text in re.findall(r"<a:t>(.*?)</a:t>", xml)])
            return slides
    except Exception:
        return []


def pptx_note_texts(path: Path) -> list[list[str]]:
    try:
        with zipfile.ZipFile(path) as archive:
            names = sorted(
                [name for name in archive.namelist() if re.match(r"ppt/notesSlides/notesSlide\d+\.xml$", name)],
                key=lambda name: int(re.search(r"notesSlide(\d+)\.xml$", name).group(1)),
            )
            notes = []
            for name in names:
                xml = archive.read(name).decode("utf-8", errors="ignore")
                notes.append([unescape(text) for text in re.findall(r"<a:t>(.*?)</a:t>", xml)])
            return notes
    except Exception:
        return []


def count_pptx_media(path: Path) -> int | None:
    try:
        with zipfile.ZipFile(path) as archive:
            return len([name for name in archive.namelist() if name.startswith("ppt/media/") and Path(name).suffix.lower() in IMAGE_EXTS])
    except Exception:
        return None


def pillow_available() -> bool:
    try:
        from PIL import Image  # noqa: F401
        return True
    except Exception:
        return False


def pptx_relationship_targets(archive: zipfile.ZipFile, slide_name: str) -> dict[str, str]:
    slide_base = posixpath.basename(slide_name)
    rel_name = posixpath.join(posixpath.dirname(slide_name), "_rels", f"{slide_base}.rels")
    if rel_name not in archive.namelist():
        return {}
    xml = archive.read(rel_name).decode("utf-8", errors="ignore")
    targets: dict[str, str] = {}
    for rel in re.finditer(r"<Relationship\b[^>]*/?>", xml, flags=re.I):
        attrs = rel.group(0)
        rel_id = re.search(r'\bId="([^"]+)"', attrs)
        target = re.search(r'\bTarget="([^"]+)"', attrs)
        rel_type = re.search(r'\bType="([^"]+)"', attrs)
        if not rel_id or not target:
            continue
        target_value = unescape(target.group(1))
        type_value = rel_type.group(1).lower() if rel_type else ""
        if "image" not in type_value and "/media/" not in target_value and not target_value.startswith("../media/"):
            continue
        if target_value.startswith("/"):
            media_name = target_value.lstrip("/")
        else:
            media_name = posixpath.normpath(posixpath.join(posixpath.dirname(slide_name), target_value))
        targets[rel_id.group(1)] = media_name
    return targets


def pptx_image_dimensions(archive: zipfile.ZipFile, media_name: str) -> tuple[int, int] | None:
    try:
        from PIL import Image
    except Exception:
        return None
    if media_name not in archive.namelist():
        return None
    suffix = Path(media_name).suffix.lower()
    if suffix not in BITMAP_EXTS:
        return None
    try:
        with Image.open(BytesIO(archive.read(media_name))) as image:
            return image.size
    except Exception:
        return None


def bitmap_dimensions(path: Path) -> tuple[int, int] | None:
    try:
        from PIL import Image
    except Exception:
        return None
    if path.suffix.lower() not in BITMAP_EXTS:
        return None
    try:
        with Image.open(path) as image:
            return image.size
    except Exception:
        return None


def pptx_image_aspect_issues(path: Path, tolerance: float = 0.08) -> list[str]:
    findings = []
    try:
        with zipfile.ZipFile(path) as archive:
            names = sorted(
                [name for name in archive.namelist() if re.match(r"ppt/slides/slide\d+\.xml$", name)],
                key=lambda name: int(re.search(r"slide(\d+)\.xml$", name).group(1)),
            )
            dimensions_cache: dict[str, tuple[int, int] | None] = {}
            for slide_name in names:
                slide_index = int(re.search(r"slide(\d+)\.xml$", slide_name).group(1))
                rel_targets = pptx_relationship_targets(archive, slide_name)
                xml = archive.read(slide_name).decode("utf-8", errors="ignore")
                for pic_index, pic in enumerate(re.finditer(r"<p:pic\b.*?</p:pic>", xml, flags=re.I | re.S), 1):
                    block = pic.group(0)
                    embed = re.search(r'<a:blip\b[^>]*\br:embed="([^"]+)"', block, flags=re.I)
                    if not embed:
                        continue
                    media_name = rel_targets.get(embed.group(1))
                    if not media_name:
                        continue
                    if media_name not in dimensions_cache:
                        dimensions_cache[media_name] = pptx_image_dimensions(archive, media_name)
                    dimensions = dimensions_cache[media_name]
                    if not dimensions:
                        continue
                    source_w, source_h = dimensions
                    if source_w <= 0 or source_h <= 0:
                        continue
                    sppr = re.search(r"<p:spPr\b.*?</p:spPr>", block, flags=re.I | re.S)
                    ext = re.search(r'<a:ext\b[^>]*\bcx="(\d+)"[^>]*\bcy="(\d+)"', sppr.group(0) if sppr else block, flags=re.I)
                    if not ext:
                        continue
                    box_w = int(ext.group(1))
                    box_h = int(ext.group(2))
                    if box_w <= 0 or box_h <= 0:
                        continue
                    has_src_rect = bool(re.search(r"<a:srcRect\b", block, flags=re.I))
                    source_ratio = source_w / source_h
                    box_ratio = box_w / box_h
                    distortion = abs(math.log(box_ratio / source_ratio))
                    if distortion > tolerance and not has_src_rect:
                        findings.append(
                            f"slide {slide_index} picture {pic_index} ({posixpath.basename(media_name)}) "
                            f"uses box ratio {box_ratio:.2f}:1 for source ratio {source_ratio:.2f}:1 without sizing/crop metadata"
                        )
    except Exception:
        return []
    return findings


def pptx_large_bitmap_reuse(path: Path, min_area: int = 200_000) -> dict:
    try:
        with zipfile.ZipFile(path) as archive:
            slide_names = sorted(
                [name for name in archive.namelist() if re.match(r"ppt/slides/slide\d+\.xml$", name)],
                key=lambda name: int(re.search(r"slide(\d+)\.xml$", name).group(1)),
            )
            media_hashes: dict[str, str] = {}
            dimensions_cache: dict[str, tuple[int, int] | None] = {}
            hash_slide_counts: dict[str, int] = {}
            for slide_name in slide_names:
                rel_targets = pptx_relationship_targets(archive, slide_name)
                xml = archive.read(slide_name).decode("utf-8", errors="ignore")
                slide_hashes = set()
                for embed in re.finditer(r'<a:blip\b[^>]*\br:embed="([^"]+)"', xml, flags=re.I):
                    media_name = rel_targets.get(embed.group(1))
                    if not media_name or media_name not in archive.namelist():
                        continue
                    if media_name not in dimensions_cache:
                        dimensions_cache[media_name] = pptx_image_dimensions(archive, media_name)
                    dimensions = dimensions_cache[media_name]
                    if not dimensions:
                        continue
                    width, height = dimensions
                    if width * height < min_area:
                        continue
                    if media_name not in media_hashes:
                        import hashlib

                        media_hashes[media_name] = hashlib.sha256(archive.read(media_name)).hexdigest()
                    slide_hashes.add(media_hashes[media_name])
                for media_hash in slide_hashes:
                    hash_slide_counts[media_hash] = hash_slide_counts.get(media_hash, 0) + 1
            slide_count = len(slide_names)
            most_repeated = max(hash_slide_counts.values(), default=0)
            return {
                "slideCount": slide_count,
                "uniqueLargeBitmapHashes": len(hash_slide_counts),
                "mostRepeatedLargeBitmapSlides": most_repeated,
                "mostRepeatedLargeBitmapShare": most_repeated / slide_count if slide_count else 0,
            }
    except Exception:
        return {}


def stale_price_mentions(text: str, expected_price: float) -> list[str]:
    if not expected_price:
        return []
    expected_int = int(expected_price)
    numeric_hits = [
        match.group(0)
        for match in re.finditer(r"\$\s*(\d+(?:\.\d+)?)|\b(\d+(?:\.\d+)?)\s+dollars?\b", text, flags=re.I)
        if int(float(match.group(1) or match.group(2))) != expected_int
    ]
    number_words = {
        17: ["seventeen"],
        27: ["twenty-seven", "twenty seven"],
        37: ["thirty-seven", "thirty seven"],
        47: ["forty-seven", "forty seven"],
        57: ["fifty-seven", "fifty seven"],
        67: ["sixty-seven", "sixty seven"],
        77: ["seventy-seven", "seventy seven"],
        97: ["ninety-seven", "ninety seven"],
    }
    text_lower = text.lower()
    for price, words in number_words.items():
        if price == expected_int:
            continue
        for word in words:
            if re.search(rf"\b{re.escape(word)}\s+dollars?\b", text_lower):
                numeric_hits.append(f"{word} dollars")
    return sorted(set(numeric_hits))


def visible_stage_labels(slides: list[list[str]]) -> list[str]:
    found = []
    stage = "|".join(sorted(BANNED_VISIBLE_VSL_STAGE_LABELS))
    for slide_index, texts in enumerate(slides, 1):
        for text in texts:
            compact = re.sub(r"\s+", " ", text.strip())
            lower = compact.lower()
            label = lower
            match = re.match(r"^\d{1,2}\s*/\s*([a-z ]+)$", lower)
            if match:
                label = match.group(1).strip()
            if (
                label in BANNED_VISIBLE_VSL_STAGE_LABELS
                or re.match(rf"^\d{{1,2}}\s*/\s*({stage})\b", lower)
                or re.match(rf"^(stage|section|beat)\s*[:/\-]\s*({stage})\b", lower)
                or re.match(rf"^({stage})\s*[:/\-]\s*", lower)
            ):
                found.append(f"slide {slide_index}: {compact}")
    return found


def audit_scores_ok(audit: dict, issues: list[str], warnings: list[str]) -> None:
    if not isinstance(audit, dict):
        issues.append("Commercial audit missing or invalid.")
        return
    status = str(audit.get("status", "")).lower()
    if status not in {"passed", "complete", "validated"}:
        issues.append("Commercial audit status is not passed/complete/validated.")
    scores = audit.get("scores", {})
    if not isinstance(scores, dict):
        issues.append("Commercial audit scores missing or invalid.")
        return
    for artifact_id in MAJOR_ARTIFACTS:
        score = scores.get(artifact_id)
        if score is None:
            issues.append(f"Commercial audit missing score for {artifact_id}.")
            continue
        if isinstance(score, dict):
            for metric in ["buyerValue", "usability", "trust"]:
                value = quality_number(score.get(metric))
                if value < 4:
                    issues.append(f"Commercial audit score below 4 for {artifact_id}.{metric}: {value or 'missing'}")
        else:
            value = quality_number(score)
            if value < 4:
                issues.append(f"Commercial audit score below 4 for {artifact_id}: {value or 'missing'}")
    if audit.get("blockingIssues"):
        warnings.append("Commercial audit lists blocking issues; do not mark the run complete until resolved.")


def validate_pdf(root: Path, manifest: dict, by_id: dict[str, dict], issues: list[str], warnings: list[str]) -> None:
    pdf_artifact = by_id.get("pdf-product")
    pdf_path = artifact_path(root, pdf_artifact)
    if not pdf_path or not pdf_path.exists():
        issues.append("PDF product missing; cannot validate depth.")
        return

    price = numeric_price(manifest.get("price"))
    min_pages, min_surfaces, min_words = pdf_targets(price)
    min_named_tools, min_example_pairs = pdf_tool_targets(price)
    page_count, word_count = count_pdf(pdf_path)
    if page_count is None:
        warnings.append("Could not inspect PDF page count because pypdf is unavailable or failed.")
    elif page_count < min_pages:
        issues.append(f"PDF product is too thin for the price point: {page_count} pages found, {min_pages}+ expected.")
    if word_count is not None and word_count < min_words:
        issues.append(f"PDF extracted text is light for a paid product: {word_count} words found, {min_words}+ expected.")
    pdf_text = extract_pdf_text(pdf_path).lower()
    action_surface_mentions = len(re.findall(r"\baction surface\b", pdf_text))
    if action_surface_mentions > 2:
        issues.append(f"PDF repeats generic 'Action Surface' labels {action_surface_mentions} times; use named buyer tools/templates instead.")

    pdf_quality = manifest.get("quality", {}).get("pdf", {})
    if not isinstance(pdf_quality, dict):
        pdf_quality = {}
    action_count = quality_number(pdf_quality.get("actionSurfaceCount"))
    if action_count < min_surfaces:
        issues.append(f"PDF action-surface count below target: {action_count or 'missing'} found, {min_surfaces}+ expected.")
    named_tool_count = quality_number(pdf_quality.get("namedToolCount"))
    if named_tool_count < min_named_tools:
        issues.append(f"PDF named tool/template count below target: {named_tool_count or 'missing'} found, {min_named_tools}+ expected.")
    page_archetype_count = quality_number(pdf_quality.get("pageArchetypeCount"))
    if page_archetype_count < 7:
        issues.append(f"PDF page archetype count below target: {page_archetype_count or 'missing'} found, 7+ expected.")
    max_page_archetype_share = quality_float(pdf_quality.get("maxPageArchetypeShare"))
    if not max_page_archetype_share:
        issues.append("PDF quality metadata must record maxPageArchetypeShare.")
    elif max_page_archetype_share > 0.35:
        issues.append(f"PDF repeats one page archetype too often: maxPageArchetypeShare {max_page_archetype_share:.2f}, must be <= 0.35.")
    completed_example_count = quality_number(pdf_quality.get("completedExampleCount"))
    blank_template_count = quality_number(pdf_quality.get("blankTemplateCount"))
    if completed_example_count < min_example_pairs:
        issues.append(f"PDF completed example count below target: {completed_example_count or 'missing'} found, {min_example_pairs}+ expected.")
    if blank_template_count < min_example_pairs:
        issues.append(f"PDF blank template count below target: {blank_template_count or 'missing'} found, {min_example_pairs}+ expected.")
    pdf_visual_count = quality_number(pdf_quality.get("visualAssetCount"))
    pdf_specific_visual_count = quality_number(pdf_quality.get("pdfSpecificVisualAssetCount"))
    if pdf_visual_count < 6:
        issues.append(f"PDF visual asset/treatment count below target: {pdf_visual_count or 'missing'} found, 6+ expected.")
    if pdf_specific_visual_count < 4:
        issues.append(f"PDF-specific visual asset/treatment count below target: {pdf_specific_visual_count or 'missing'} found, 4+ expected.")
    if pdf_quality.get("genericActionSurfaceLabelsRemoved") is not True:
        issues.append("PDF quality metadata must confirm genericActionSurfaceLabelsRemoved.")
    if pdf_quality.get("hasCompletedExamples") is not True:
        issues.append("PDF quality metadata must confirm completed examples.")
    if pdf_quality.get("hasBlankTemplates") is not True:
        issues.append("PDF quality metadata must confirm blank buyer-fillable templates.")
    if pdf_quality.get("renderChecked") is not True:
        issues.append("PDF quality metadata must confirm rendered page visual QA.")
    if pdf_quality.get("studio") != "pdf-workbook-studio-v1":
        issues.append("PDF quality metadata must record studio: pdf-workbook-studio-v1.")
    if pdf_quality.get("renderBackend") != "gotenberg-chromium":
        issues.append("PDF quality metadata must record renderBackend: gotenberg-chromium for PDF Workbook Studio deep runs.")
    source_html = str(pdf_quality.get("sourceHtmlPath", "")).strip()
    if not source_html:
        issues.append("PDF quality metadata must record sourceHtmlPath.")
    elif not (root / source_html).exists():
        issues.append(f"PDF sourceHtmlPath does not exist: {source_html}")
    if pdf_quality.get("actualPdfRenderChecked") is not True:
        issues.append("PDF quality metadata must confirm actualPdfRenderChecked from final PDF page renders.")
    rendered_page_count = quality_number(pdf_quality.get("renderedPageImageCount"))
    if rendered_page_count < 1:
        issues.append("PDF quality metadata must record renderedPageImageCount from actual final PDF page images.")
    render_qa = str(pdf_quality.get("renderQaPath", "")).strip()
    if not render_qa:
        issues.append("PDF quality metadata must record renderQaPath.")
    elif not (root / render_qa).exists():
        issues.append(f"PDF renderQaPath does not exist: {render_qa}")
    page_audit = pdf_quality.get("pageArchetypeAudit")
    if not isinstance(page_audit, list) or not page_audit:
        issues.append("PDF quality metadata must include pageArchetypeAudit with page, archetype, namedTool, and visualAsset.")


def validate_email_sequence(root: Path, manifest: dict, by_id: dict[str, dict], issues: list[str], warnings: list[str]) -> None:
    email_artifact = by_id.get("email-sequence")
    email_path = artifact_path(root, email_artifact)
    if not email_path or not email_path.exists():
        issues.append("Email sequence artifact missing; cannot validate launch email readiness.")
        return
    if email_path.suffix.lower() not in TEXT_EXTS:
        return
    raw_text = text_for(email_path)
    visible = visible_text_from_html(raw_text) if email_path.suffix.lower() in {".html", ".htm"} else raw_text
    lower = visible.lower()

    email_count = max(
        len(re.findall(r"\bemail\s+\d+\b", lower)),
        len(re.findall(r"<article\b[^>]*class=[\"'][^\"']*\bemail\b", raw_text, flags=re.I)),
    )
    if email_count < 5:
        issues.append(f"Email sequence is too thin: {email_count} numbered emails found, 5+ expected.")
    if "launch email sequence" in lower and email_count < 7:
        issues.append(f"Launch email sequence must include 7+ numbered emails: {email_count} found.")

    subject_count = max(
        len(re.findall(r"\bsubject\s*:", lower)),
        len(re.findall(r"<h[12]\b[^>]*>", raw_text, flags=re.I)) - 1,
    )
    preview_count = len(re.findall(r"\bpreview\s*:", lower))
    cta_count = len(re.findall(r"\bcta\s*:", lower))
    send_count = max(len(re.findall(r"\bsend\s*(?:timing|date|day)?\s*:", lower)), len(re.findall(r"\bday\s+\d+\b", lower)))
    role_count = max(
        len(re.findall(r"\b(?:campaign\s+)?role\s*:", lower)),
        len(re.findall(r"class=[\"'][^\"']*\brole\b", raw_text, flags=re.I)),
    )
    required_counts = {
        "subject line": subject_count,
        "preview text": preview_count,
        "CTA": cta_count,
        "send timing": send_count,
        "campaign role": role_count,
    }
    target_count = min(email_count or 7, 7)
    for label, count in required_counts.items():
        if count < target_count:
            issues.append(f"Email sequence missing {label} metadata: {count} found, {target_count}+ expected.")

    repeated = repeated_sentences(visible, threshold=3)
    if repeated:
        examples = "; ".join(f"'{sentence[:80]}' x{count}" for sentence, count in repeated[:3])
        issues.append("Email sequence contains repeated boilerplate copy: " + examples)
    repeated_blocks = repeated_body_blocks(raw_text, threshold=2)
    if repeated_blocks:
        examples = "; ".join(f"'{sentence[:80]}' x{count}" for sentence, count in repeated_blocks[:3])
        issues.append("Email sequence contains repeated body blocks: " + examples)
    email_source = artifact_path(root, by_id.get("email-sequence-source"))
    if not email_source or not email_source.exists():
        issues.append("Email Launch Studio requires canonical email-sequence.json source registered as email-sequence-source.")
    email_quality = manifest.get("quality", {}).get("emails", {})
    if not isinstance(email_quality, dict):
        email_quality = {}
    if email_quality.get("studio") != "email-launch-studio-v1":
        issues.append("Email quality metadata must record studio: email-launch-studio-v1.")
    if quality_number(email_quality.get("emailCount")) < target_count:
        issues.append("Email quality metadata emailCount is below the rendered sequence target.")
    for key, label in {
        "hasSendTiming": "send timing",
        "hasPreviewText": "preview text",
        "hasCampaignRoles": "campaign roles",
        "repeatedBodyBlocksChecked": "repeated body block check",
        "urgencyBasisValid": "valid urgency basis",
    }.items():
        if email_quality.get(key) is not True:
            issues.append(f"Email quality metadata must confirm {label}.")
    if quality_number(email_quality.get("distinctConversionJobs")) < target_count:
        issues.append("Email quality metadata must record distinct conversion jobs for the sequence.")


def validate_sales_copy(root: Path, manifest: dict, by_id: dict[str, dict], issues: list[str], warnings: list[str]) -> None:
    copy_plan_artifact = by_id.get("copy-plan")
    copy_plan_path = artifact_path(root, copy_plan_artifact) or (root / "copy-plan.json")
    copy_plan = {}
    if not copy_plan_path.exists():
        issues.append("Copy Studio source missing; copy-plan.json is required before copy.md, visual planning, or page build.")
    else:
        try:
            copy_plan = json.loads(copy_plan_path.read_text(encoding="utf-8-sig"))
        except json.JSONDecodeError as exc:
            issues.append(f"copy-plan.json is not valid JSON: {exc}")
            copy_plan = {}
    if copy_plan:
        for issue in validate_copy_plan_source(copy_plan):
            issues.append("Copy Studio plan invalid: " + issue)

    copy_quality = manifest.get("quality", {}).get("copy", {})
    if not isinstance(copy_quality, dict):
        copy_quality = {}
    required_quality = {
        "studio": COPY_STUDIO_VERSION,
        "framework": COPY_FRAMEWORK,
        "standaloneCopyRequired": True,
        "vslDependency": "optional-supporting-asset",
        "hasNewInsight": True,
        "hasUniqueMechanism": True,
        "hasFailedAlternatives": True,
        "hasProofBeforeOffer": True,
        "hasFeatureBenefitBreakdown": True,
        "hasObjectionMatrix": True,
        "renderedFromCopyPlan": True,
    }
    for field, expected in required_quality.items():
        if copy_quality.get(field) != expected:
            issues.append(f"Copy quality metadata must record {field}: {expected}.")

    copy_artifact = by_id.get("sales-copy")
    copy_path = artifact_path(root, copy_artifact) or (root / "copy.md")
    if not copy_path or not copy_path.exists():
        issues.append("Sales copy missing; copy.md with # Section Blueprint is required before visual planning or page build.")
        return
    if copy_artifact and copy_artifact.get("provenance") != COPY_STUDIO_VERSION:
        issues.append("copy.md exists but sales-copy artifact provenance is not copy-studio-v1; render it from Copy Studio.")
    if copy_quality.get("copyPath") and not (root / str(copy_quality.get("copyPath"))).exists():
        issues.append("Copy quality metadata copyPath does not exist.")

    text = text_for(copy_path)
    lower = text.lower()
    missing_headings = [heading for heading in REQUIRED_COPY_HEADINGS if heading.lower() not in lower]
    if missing_headings:
        issues.append("Sales copy missing required direct-response headings: " + ", ".join(missing_headings))

    blueprint = markdown_top_section(text, "# Section Blueprint")
    if not blueprint.strip():
        issues.append("Sales copy must include # Section Blueprint before page build.")
        return

    missing_fields = [field for field in REQUIRED_BLUEPRINT_FIELDS if field.lower() not in blueprint.lower()]
    if missing_fields:
        issues.append("Sales copy Section Blueprint missing required fields: " + ", ".join(missing_fields))

    blueprint_lower = blueprint.lower()
    missing_sections = [
        section
        for section in REQUIRED_SALES_PAGE_SECTIONS
        if section != "footer" and not re.search(rf"\b{re.escape(section)}\b", blueprint_lower)
    ]
    if missing_sections:
        issues.append("Sales copy Section Blueprint missing required section rows: " + ", ".join(missing_sections))

    if COPY_FRAMEWORK not in lower:
        issues.append(f"Sales copy must record copyFramework: {COPY_FRAMEWORK}.")
    if "direct-response-long-form-v1" not in lower:
        issues.append("Sales copy must record pageFramework: direct-response-long-form-v1.")
    if "proof" in blueprint_lower and "offer-stack" in blueprint_lower:
        proof_pos = blueprint_lower.find("proof")
        stack_pos = blueprint_lower.find("offer-stack")
        if stack_pos >= 0 and proof_pos >= 0 and proof_pos > stack_pos:
            issues.append("Sales copy Section Blueprint must place proof/demo before offer-stack.")
    if copy_plan:
        row_ids = [copy_as_text(row.get("sectionId")) for row in copy_plan_section_rows(copy_plan)]
        for required in ["new-insight", "mechanism", "proof", "product", "feature-benefit", "how-it-works", "offer-stack"]:
            if required not in row_ids:
                issues.append(f"copy-plan.sectionPlan missing required sales argument section: {required}.")
        if "proof" in row_ids and "offer-stack" in row_ids and row_ids.index("proof") > row_ids.index("offer-stack"):
            issues.append("copy-plan.sectionPlan must place proof/demo before offer-stack.")
        if "new-insight" in row_ids and "mechanism" in row_ids and row_ids.index("new-insight") > row_ids.index("mechanism"):
            issues.append("copy-plan.sectionPlan must place epiphany/new insight before unique mechanism.")
        product = copy_plan.get("productReveal", {}) if isinstance(copy_plan.get("productReveal"), dict) else {}
        components = copy_list_of_dicts(product.get("coreComponents"))
        if len(components) < 3:
            issues.append("Product reveal is too thin; productReveal.coreComponents must include feature-benefit-reason bullets.")
        for index, component in enumerate(components, start=1):
            if not copy_as_text(component.get("benefit")) or not copy_as_text(component.get("reasonItMatters")):
                issues.append(f"Product reveal component {index} lacks benefit or reasonItMatters.")
        offer_items = copy_list_of_dicts(copy_plan.get("offerStack", {}).get("items") if isinstance(copy_plan.get("offerStack"), dict) else [])
        for index, item in enumerate(offer_items, start=1):
            if len(copy_as_text(item.get("copy"))) < 8:
                issues.append(f"Offer stack item {index} lacks buyer-facing value logic.")
        urgency = copy_plan.get("urgencyBasis", {}) if isinstance(copy_plan.get("urgencyBasis"), dict) else {}
        if urgency.get("fakeUrgency") is not False:
            issues.append("Urgency is fake or unsupported; urgencyBasis.fakeUrgency must be false.")


def validate_page_kit_contract(
    root: Path,
    html_text: str,
    manifest: dict,
    by_id: dict[str, dict],
    sales_quality: dict,
    issues: list[str],
) -> None:
    if manifest.get("mode") != "deep":
        return

    if html_attr_value(html_text, "data-offeros-page-kit") != "v1":
        issues.append('Deep sales pages must be built by OfferOS Page Kit and declare data-offeros-page-kit="v1".')
    if html_attr_value(html_text, "data-offeros-builder") != "offeros-page-kit-builder-v1":
        issues.append('Deep sales pages must declare data-offeros-builder="offeros-page-kit-builder-v1".')
    if html_attr_value(html_text, "data-offeros-vsl-placement") != "main-column-stacked":
        issues.append('Deep sales pages must declare data-offeros-vsl-placement="main-column-stacked".')

    html_archetype = html_attr_value(html_text, "data-offeros-archetype")
    html_theme = html_attr_value(html_text, "data-offeros-theme")
    archetype = str(sales_quality.get("pageKitArchetype") or html_archetype).strip()
    theme = str(sales_quality.get("themePreset") or html_theme).strip()
    if archetype not in ALLOWED_PAGE_KIT_ARCHETYPES:
        issues.append("Sales page quality metadata must record a valid pageKitArchetype from the OfferOS Page Kit.")
    if theme not in ALLOWED_PAGE_KIT_THEMES:
        issues.append("Sales page quality metadata must record a valid themePreset from the OfferOS Page Kit.")
    if html_archetype and archetype and html_archetype != archetype:
        issues.append("Sales page pageKitArchetype metadata must match data-offeros-archetype.")
    if html_theme and theme and html_theme != theme:
        issues.append("Sales page themePreset metadata must match data-offeros-theme.")

    expected_quality = {
        "pageKit": "offeros-page-kit-v1",
        "pageKitBuilder": "offeros-page-kit-builder-v1",
        "checkoutTarget": "#checkout",
        "vslPlacement": "main-column-stacked",
    }
    for field, expected in expected_quality.items():
        if sales_quality.get(field) != expected:
            issues.append(f"Sales page quality metadata must record {field}: {expected}.")
    if sales_quality.get("pageKitBlueprintUsed") is not True:
        issues.append("Sales page quality metadata must confirm pageKitBlueprintUsed.")
    if sales_quality.get("themeTokensUsed") is not True:
        issues.append("Sales page quality metadata must confirm themeTokensUsed.")
    if sales_quality.get("orderFormIncluded") is not False:
        issues.append("Sales page quality metadata must confirm orderFormIncluded: false.")

    blueprint_path = artifact_path(root, by_id.get("sales-page-blueprint"))
    if not blueprint_path or not blueprint_path.exists():
        issues.append("Deep sales pages must register a sales-page-blueprint artifact before index.html.")
    theme_path = artifact_path(root, by_id.get("theme"))
    if not theme_path or not theme_path.exists():
        issues.append("Deep sales pages must register a theme artifact before index.html.")

    signals = order_form_signals(html_text)
    if signals:
        issues.append("Sales page must not contain an order form or checkout form; link CTAs to #checkout instead: " + "; ".join(signals[:5]) + ".")

    cta_hrefs = anchor_hrefs_with_marker(html_text, "data-offeros-cta")
    stack_cta_hrefs = anchor_hrefs_with_marker(html_text, "data-offeros-stack-cta")
    if "#checkout" not in cta_hrefs:
        issues.append('Sales page must include at least one data-offeros-cta link to the checkout placeholder href="#checkout".')
    if stack_cta_hrefs and "#checkout" not in stack_cta_hrefs:
        issues.append('Offer-stack purchase CTA must link to the checkout placeholder href="#checkout".')
    banned_targets = [href for href in cta_hrefs if href.lower() in {"#order", "#order-form", "#payment", "#checkout-form"}]
    if banned_targets:
        issues.append("Sales page CTAs must not target on-page order/payment form anchors: " + ", ".join(sorted(set(banned_targets))) + ".")


def validate_sales_page(root: Path, manifest: dict, by_id: dict[str, dict], issues: list[str], warnings: list[str]) -> None:
    page_artifact = by_id.get("sales-page")
    page_path = artifact_path(root, page_artifact)
    if not page_path or not page_path.exists():
        issues.append("Sales page missing; cannot validate direct-response structure.")
        return
    html_text = text_for(page_path)
    by_path = artifact_path_map(list(by_id.values()))
    local_images = [
        src
        for src in re.findall(r"<img\b[^>]*\bsrc\s*=\s*[\"']([^\"']+)[\"']", html_text, flags=re.I | re.S)
        if not re.match(r"^(?:https?:|data:|#)", src, flags=re.I)
    ]
    missing_images = [src for src in local_images if not (root / src.split("?", 1)[0].split("#", 1)[0].lstrip("./")).exists()]
    if missing_images:
        issues.append("Sales page references missing local images: " + ", ".join(missing_images[:8]))
    missing = [section for section in REQUIRED_SALES_PAGE_SECTIONS if not has_section_marker(html_text, section)]
    if missing:
        issues.append("Sales page missing required direct-response section markers: " + ", ".join(missing))
    if "data-offeros-section" not in html_text.lower():
        issues.append("Sales page must use data-offeros-section markers from the OfferOS section map.")
    sales_quality = manifest.get("quality", {}).get("salesPage", {})
    if not isinstance(sales_quality, dict):
        sales_quality = {}
    if sales_quality.get("requiredSectionContract") not in {"direct-response-v1", "direct-response"}:
        issues.append("Sales page quality metadata must record requiredSectionContract: direct-response-v1.")
    if sales_quality.get("sectionMarkersPresent") is not True:
        issues.append("Sales page quality metadata must confirm sectionMarkersPresent.")
    page_type = str(sales_quality.get("pageType", "")).strip()
    if page_type not in ALLOWED_SALES_PAGE_TYPES:
        issues.append("Sales page quality metadata must record a valid pageType from references/sales-page-types.md.")
    price = numeric_price(manifest.get("price"))
    if price and price <= 99 and sales_quality.get("pageTypeOverrideUserRequested") is not True and page_type != "direct-response-long-form-vsl":
        issues.append("Paid front-end offers at $99 or below must use pageType: direct-response-long-form-vsl unless pageTypeOverrideUserRequested is true.")
    if sales_quality.get("sectionDepthChecked") is not True:
        issues.append("Sales page quality metadata must confirm sectionDepthChecked.")
    if sales_quality.get("repeatedTextChecked") is not True:
        issues.append("Sales page quality metadata must confirm repeatedTextChecked.")
    if sales_quality.get("offerStackItemsUnique") is not True:
        issues.append("Sales page quality metadata must confirm offerStackItemsUnique.")
    if sales_quality.get("studio") != "sales-page-studio-v1":
        issues.append("Sales page quality metadata must record studio: sales-page-studio-v1.")
    if page_type == "direct-response-long-form-vsl":
        if sales_quality.get("framework") != COPY_FRAMEWORK:
            issues.append(f"Direct-response sales page quality metadata must record framework: {COPY_FRAMEWORK}.")
        if sales_quality.get("pageFramework") != "direct-response-long-form-v1":
            issues.append("Direct-response sales page quality metadata must record pageFramework: direct-response-long-form-v1.")
        if sales_quality.get("copyStudioUsed") is not True:
            issues.append("Direct-response sales page quality metadata must confirm copyStudioUsed.")
        if sales_quality.get("copyPlanPath") != "copy-plan.json":
            issues.append("Direct-response sales page quality metadata must record copyPlanPath: copy-plan.json.")
        if sales_quality.get("standaloneCopyRequired") is not True:
            issues.append("Direct-response sales page quality metadata must confirm standaloneCopyRequired.")
        if sales_quality.get("copyBlueprintPresent") is not True:
            issues.append("Direct-response sales page quality metadata must confirm copyBlueprintPresent.")
        if sales_quality.get("compositionContract") != "direct-response-composition-v2":
            issues.append("Direct-response sales page quality metadata must record compositionContract: direct-response-composition-v2.")
    validate_page_kit_contract(root, html_text, manifest, by_id, sales_quality, issues)

    visible_text = visible_text_from_html(html_text)
    word_count = len(re.findall(r"\b[\w'-]+\b", visible_text))
    recorded_word_count = quality_number(sales_quality.get("visibleWordCount"))
    if recorded_word_count and abs(recorded_word_count - word_count) > max(250, word_count * 0.25):
        warnings.append("Sales page visibleWordCount metadata differs substantially from inspected page text.")
    if page_type == "direct-response-long-form-vsl" and word_count < 2500:
        issues.append(f"Direct-response long-form VSL page is too thin: {word_count} visible words found, 2500+ expected.")
    faq_marker_count = len(re.findall(r"data-offeros-faq-item(?:\s|=|>)", html_text, flags=re.I))
    cta_marker_count = len(re.findall(r"data-offeros-cta(?:\s|=|>)", html_text, flags=re.I))
    if page_type == "direct-response-long-form-vsl" and faq_marker_count < 7:
        issues.append(f"Direct-response long-form VSL page must include 7+ FAQ items marked data-offeros-faq-item: {faq_marker_count} found.")
    if page_type == "direct-response-long-form-vsl" and cta_marker_count < 4:
        issues.append(f"Direct-response long-form VSL page must include 4+ CTA elements marked data-offeros-cta: {cta_marker_count} found.")
    page_visual_count = len(re.findall(r"data-offeros-page-visual|data-offeros-video-thumbnail|data-offeros-product-bundle", html_text, flags=re.I))
    if page_type == "direct-response-long-form-vsl" and page_visual_count < 6:
        issues.append(f"Direct-response long-form VSL page must include 6+ meaningful page visuals: {page_visual_count} found.")
    copy_plan_path = root / str(sales_quality.get("copyPlanPath") or "copy-plan.json")
    if copy_plan_path.exists():
        try:
            copy_plan = json.loads(copy_plan_path.read_text(encoding="utf-8-sig"))
        except json.JSONDecodeError:
            copy_plan = {}
        copy_sections = {copy_as_text(row.get("sectionId")) for row in copy_plan_section_rows(copy_plan)}
        page_sections = set(re.findall(r'data-offeros-section=["\']([^"\']+)["\']', html_text, flags=re.I))
        missing_copy_sections = sorted(
            section
            for section in page_sections
            if section != "header" and section in REQUIRED_SALES_PAGE_SECTIONS and section not in copy_sections
        )
        if missing_copy_sections:
            issues.append("Sales page sections do not map back to copy-plan.sectionPlan: " + ", ".join(missing_copy_sections))
    recorded_page_visual_count = quality_number(sales_quality.get("salesPageVisualCount"))
    if recorded_page_visual_count and recorded_page_visual_count < 6:
        issues.append("Sales page quality metadata salesPageVisualCount below target: 6+ expected.")
    post_hero_cta_count = len(re.findall(r"data-offeros-post-hero-cta(?:\s|=|>)", html_text, flags=re.I))
    if page_type == "direct-response-long-form-vsl" and post_hero_cta_count < 3:
        issues.append(f"Direct-response long-form VSL page must include 3+ post-hero CTA elements marked data-offeros-post-hero-cta: {post_hero_cta_count} found.")
    if page_type == "direct-response-long-form-vsl" and quality_number(sales_quality.get("objectionCount")) < 7:
        issues.append("Direct-response long-form VSL page must record 7+ objections handled.")
    if page_type == "direct-response-long-form-vsl" and quality_number(sales_quality.get("ctaCount")) < 4:
        issues.append("Direct-response long-form VSL page must record 4+ CTA placements.")
    if page_type == "direct-response-long-form-vsl" and quality_number(sales_quality.get("postHeroCtaCount")) < 3:
        issues.append("Direct-response long-form VSL page must record 3+ post-hero CTA placements.")
    if page_type == "direct-response-long-form-vsl":
        if sales_quality.get("navigationPolicy") != "no-section-nav":
            issues.append('Direct-response sales page quality metadata must record navigationPolicy: no-section-nav.')
        if sales_quality.get("iconSystem") != "lucide-icons-v1":
            issues.append('Direct-response sales page quality metadata must record iconSystem: lucide-icons-v1.')
        if sales_quality.get("iconLibrary") != "lucide":
            issues.append('Direct-response sales page quality metadata must record iconLibrary: lucide.')
        if "data-lucide" not in html_text:
            issues.append("Direct-response sales page must include Lucide icon markers via data-lucide.")
        if sales_quality.get("imageDisplay") != "viewport-constrained-v1":
            issues.append('Direct-response sales page quality metadata must record imageDisplay: viewport-constrained-v1.')
        if sales_quality.get("eyebrowPolicy") != "sparse-key-signposts-v1":
            issues.append('Direct-response sales page quality metadata must record eyebrowPolicy: sparse-key-signposts-v1.')
        if sales_quality.get("eyebrowAlignment") != "centered-with-section-heading":
            issues.append('Direct-response sales page quality metadata must record eyebrowAlignment: centered-with-section-heading.')
        eyebrow_count = len(re.findall(r"class=[\"'][^\"']*\boo-eyebrow\b", html_text, flags=re.I))
        if eyebrow_count > 6:
            issues.append(f"Direct-response Page Kit must use sparse section eyebrows/pills, not one on every section: {eyebrow_count} found, 6 maximum.")
        recorded_eyebrow_count = quality_number(sales_quality.get("eyebrowCount"))
        if recorded_eyebrow_count and recorded_eyebrow_count > 6:
            issues.append("Direct-response sales page quality metadata eyebrowCount exceeds sparse policy maximum of 6.")
        if re.search(r"<nav\b", html_text, flags=re.I):
            issues.append("Direct-response long-form sales pages must not include a nav menu or section-jump navigation.")
        if re.search(r"\bposition\s*:\s*sticky\b", html_text, flags=re.I):
            issues.append("Direct-response long-form sales pages must not use sticky header/navigation behavior.")
        if "watch this first" in visible_text_from_html(section_html(html_text, "vsl")).lower():
            issues.append('Post-hero VSL section must not say "Watch this first" when the hero already contains the primary VSL frame.')
        for label, marker in [
            ("support visual", "data-offeros-page-visual"),
            ("product bundle", "data-offeros-product-bundle"),
        ]:
            tags = re.findall(
                rf"<(?:figure|img)\b(?=[^>]*{re.escape(marker)})[^>]*>",
                html_text,
                flags=re.I | re.S,
            )
            unconstrained = [tag for tag in tags if "data-offeros-image-display" not in tag.lower()]
            if unconstrained:
                issues.append(f"Direct-response {label} elements must be marked data-offeros-image-display=\"constrained\".")
        vsl_words = html_word_count(section_html(html_text, "vsl"))
        if vsl_words > 220:
            issues.append(f"Direct-response VSL setup section is too text-heavy: {vsl_words} visible words found, 220 maximum.")
        section_limits = [
            section
            for section in REQUIRED_SALES_PAGE_SECTIONS
            if section not in {"header", "hero", "offer-stack", "faq", "footer"}
        ]
        oversized_sections = []
        for section in section_limits:
            section_words = html_word_count(section_html(html_text, section))
            if section_words > 500:
                oversized_sections.append(f"{section}: {section_words} words")
        if oversized_sections:
            issues.append("Direct-response page has wall-of-text sections above 500 words: " + "; ".join(oversized_sections[:5]))
        paragraph_findings = long_paragraphs(html_text, limit=55)
        if paragraph_findings:
            issues.append("Sales page has paragraphs above the 55-word direct-response limit: " + "; ".join(paragraph_findings[:5]))
        blank_cells = empty_table_cells(html_text)
        if blank_cells:
            issues.append(f"Sales page contains {blank_cells} blank table cells; required comparison cells must contain visible copy.")
        thin_sections = []
        for section, minimum in MIN_SECTION_WORDS.items():
            words = html_word_count(section_html(html_text, section))
            if words < minimum:
                thin_sections.append(f"{section}: {words} words")
        if thin_sections:
            issues.append("Direct-response page has thin required sections: " + "; ".join(thin_sections[:8]))
        validate_registered_creative_src(html_text, "data-offeros-product-bundle", "Sales-page product bundle image", by_path, issues)
        validate_registered_creative_src(html_text, "data-offeros-video-thumbnail", "Hero/VSL thumbnail image", by_path, issues)
        validate_direct_response_page_contract(html_text, manifest, sales_quality, issues)

    repeated = repeated_sentences(visible_text)
    if repeated:
        examples = "; ".join(f"'{text[:80]}' x{count}" for text, count in repeated[:3])
        issues.append("Sales page contains repeated boilerplate copy: " + examples)
    repeated_blocks = repeated_body_blocks(html_text, threshold=2)
    if repeated_blocks:
        examples = "; ".join(f"'{text[:80]}' x{count}" for text, count in repeated_blocks[:3])
        issues.append("Sales page contains repeated card/body copy: " + examples)


def validate_direct_response_page_contract(html_text: str, manifest: dict, sales_quality: dict, issues: list[str]) -> None:
    if sales_quality.get("heroContract") != "stacked-vsl-hero-v2":
        issues.append("Direct-response sales page quality metadata must record heroContract: stacked-vsl-hero-v2.")
    if sales_quality.get("heroLayout") != "stacked-vsl":
        issues.append("Direct-response sales page quality metadata must record heroLayout: stacked-vsl.")
    if sales_quality.get("heroTemplate") != "offeros-stacked-vsl-v2":
        issues.append("Direct-response sales page quality metadata must record heroTemplate: offeros-stacked-vsl-v2.")
    if sales_quality.get("heroVideoFrame") != "large-16x9":
        issues.append("Direct-response sales page quality metadata must record heroVideoFrame: large-16x9.")
    if sales_quality.get("heroVideoProminenceChecked") is not True:
        issues.append("Direct-response sales page quality metadata must confirm heroVideoProminenceChecked.")
    if sales_quality.get("offerStackContract") != "direct-response-buy-box-v1":
        issues.append("Direct-response sales page quality metadata must record offerStackContract: direct-response-buy-box-v1.")

    price = numeric_price(manifest.get("price"))
    hero = section_html(html_text, "hero")
    if hero:
        if not section_opening_tag_has(html_text, "hero", r'\bdata-offeros-hero-layout\s*=\s*["\']stacked-vsl["\']'):
            issues.append('Direct-response hero must use data-offeros-hero-layout="stacked-vsl".')
        if not section_opening_tag_has(html_text, "hero", r'\bdata-offeros-hero-contract\s*=\s*["\']stacked-vsl-hero-v2["\']'):
            issues.append('Direct-response hero must use data-offeros-hero-contract="stacked-vsl-hero-v2".')
        if not section_opening_tag_has(html_text, "hero", r'\bdata-offeros-template\s*=\s*["\']offeros-stacked-vsl-v2["\']'):
            issues.append('Direct-response hero must use data-offeros-template="offeros-stacked-vsl-v2".')
        if not section_opening_tag_has(html_text, "hero", r'\bclass\s*=\s*["\'][^"\']*\boo-hero\b[^"\']*\boo-hero-stacked-vsl\b'):
            issues.append("Direct-response hero must preserve oo-hero oo-hero-stacked-vsl shell classes.")
        if not has_marker(hero, "data-offeros-hero-inner"):
            issues.append("Direct-response hero must preserve the data-offeros-hero-inner wrapper.")
        if not has_marker(hero, "data-offeros-hero-copy-stack"):
            issues.append("Direct-response hero must include a centered copy stack marked data-offeros-hero-copy-stack.")
        for signal in hero_two_column_signals(html_text, hero):
            issues.append("Direct-response hero must not use a two-column/split SaaS layout: " + signal + ".")
        if not has_marker(hero, "data-offeros-buyer-filter"):
            issues.append("Direct-response hero must include a buyer filter marked data-offeros-buyer-filter.")
        if not has_marker(hero, "data-offeros-hero-video"):
            issues.append("Direct-response hero must include a VSL/video frame marked data-offeros-hero-video.")
        else:
            hero_video = element_with_marker(hero, "data-offeros-hero-video")
            if "oo-vsl-frame" not in hero_video.lower():
                issues.append("Direct-response hero video must use the oo-vsl-frame large 16:9 shell.")
            if not re.search(r'\bdata-offeros-hero-video-prominence\s*=\s*["\']primary["\']', hero_video, flags=re.I):
                issues.append("Direct-response hero video must be marked data-offeros-hero-video-prominence=\"primary\".")
            if not re.search(r'\bdata-offeros-hero-video-size\s*=\s*["\']large["\']', hero_video, flags=re.I):
                issues.append("Direct-response hero video must be marked data-offeros-hero-video-size=\"large\".")
            if not has_marker(hero_video, "data-offeros-video-thumbnail"):
                issues.append("Direct-response hero video frame must include a thumbnail marked data-offeros-video-thumbnail.")
            if not has_marker(hero_video, "data-offeros-video-play"):
                issues.append("Direct-response hero video frame must include a visible play control marked data-offeros-video-play.")
            if not has_marker(hero_video, "data-offeros-video-caption"):
                issues.append("Direct-response hero video frame must include a caption marked data-offeros-video-caption.")
            if "<img" not in hero_video.lower():
                issues.append("Direct-response hero video frame must include a thumbnail/image.")
            if not re.search(r"\b(play|watch|video|vsl|pitch)\b", visible_text_from_html(hero_video), flags=re.I):
                issues.append("Direct-response hero video frame must include a play/watch/pitch cue.")
        if not has_marker(hero, "data-offeros-price-strip"):
            issues.append("Direct-response hero must include an in-hero price strip marked data-offeros-price-strip.")
        else:
            price_strip = element_with_marker(hero, "data-offeros-price-strip")
            if not contains_expected_price(price_strip, price):
                issues.append("Direct-response hero price strip must show manifest.price.")
            if not re.search(r"\b(total value|value|normally|regular|today|includes?)\b", visible_text_from_html(price_strip), flags=re.I):
                issues.append("Direct-response hero price strip must include value context and a short stack summary.")
        hero_cta_hrefs = anchor_hrefs_with_marker(hero, "data-offeros-cta")
        expected_checkout_target = str(sales_quality.get("checkoutTarget") or "#checkout")
        if expected_checkout_target not in hero_cta_hrefs:
            issues.append(f'Direct-response hero must include a primary data-offeros-cta link with href="{expected_checkout_target}".')
        if not has_marker(hero, "data-offeros-trust-row"):
            issues.append("Direct-response hero must include a trust row marked data-offeros-trust-row.")
        else:
            trust_row = element_with_marker(hero, "data-offeros-trust-row")
            trust_items = len(re.findall(r"<li\b", trust_row, flags=re.I))
            if trust_items < 3:
                issues.append(f"Direct-response hero trust row must include 3+ trust bullets: {trust_items} found.")
        h1_pos = hero.lower().find("<h1")
        video_pos = re.search(r"\bdata-offeros-hero-video(?:\s|=|>)", hero, flags=re.I)
        price_pos = re.search(r"\bdata-offeros-price-strip(?:\s|=|>)", hero, flags=re.I)
        trust_pos = re.search(r"\bdata-offeros-trust-row(?:\s|=|>)", hero, flags=re.I)
        if h1_pos >= 0 and video_pos and price_pos and trust_pos:
            positions = [h1_pos, video_pos.start(), price_pos.start(), trust_pos.start()]
            if positions != sorted(positions):
                issues.append("Direct-response hero must stack in this order: H1/lead, VSL video, price strip/CTA, trust row.")

    positions = section_positions(html_text)
    ordered_sections = [section for section in REQUIRED_SALES_PAGE_SECTIONS if section not in {"header", "footer"}]
    missing_for_order = [section for section in ordered_sections if section not in positions]
    if not missing_for_order:
        ordered_positions = [positions[section] for section in ordered_sections]
        if ordered_positions != sorted(ordered_positions):
            issues.append("Direct-response page sections must follow the required persuasion order: " + " -> ".join(ordered_sections) + ".")
    if "proof" in positions and "offer-stack" in positions and positions["proof"] > positions["offer-stack"]:
        issues.append("Direct-response proof/demo section must appear before the main offer stack.")
    if "mechanism" in positions and "offer-stack" in positions and positions["mechanism"] > positions["offer-stack"]:
        issues.append("Direct-response unique mechanism must appear before the main offer stack.")

    failed_alternatives = section_html(html_text, "failed-alternatives")
    if failed_alternatives and not (has_marker(failed_alternatives, "data-offeros-failed-alternatives-table") or "<table" in failed_alternatives.lower()):
        issues.append("Direct-response failed-alternatives section must include a table or contrast block marked data-offeros-failed-alternatives-table.")
    mechanism = section_html(html_text, "mechanism")
    if mechanism and not has_marker(mechanism, "data-offeros-mechanism-steps"):
        issues.append("Direct-response mechanism section must include a named mechanism step/framework block marked data-offeros-mechanism-steps.")
    proof = section_html(html_text, "proof")
    if proof:
        proof_cards = len(re.findall(r"data-offeros-proof-card(?:\s|=|>)", proof, flags=re.I))
        if proof_cards < 2:
            issues.append(f"Direct-response proof section must include 2+ proof/demo cards marked data-offeros-proof-card: {proof_cards} found.")
    before_after = section_html(html_text, "before-after")
    if before_after and not has_marker(before_after, "data-offeros-before-after"):
        issues.append("Direct-response before/after section must include a before-after block marked data-offeros-before-after.")

    offer_stack = section_html(html_text, "offer-stack")
    if offer_stack:
        if not section_opening_tag_has(html_text, "offer-stack", r'\bid\s*=\s*["\']checkout["\']|\bdata-offeros-buy-section(?:\s|=|>)'):
            issues.append('Direct-response offer stack must be the checkout section with id="checkout" or data-offeros-buy-section.')
        if not has_marker(offer_stack, "data-offeros-product-bundle"):
            issues.append("Direct-response offer stack must include a product bundle visual marked data-offeros-product-bundle.")
        if not has_marker(offer_stack, "data-offeros-offer-checklist"):
            issues.append("Direct-response offer stack must include a deliverable checklist marked data-offeros-offer-checklist.")
        else:
            checklist = element_with_marker(offer_stack, "data-offeros-offer-checklist")
            checklist_items = len(re.findall(r"<li\b", checklist, flags=re.I))
            if checklist_items < 8:
                issues.append(f"Direct-response offer checklist must include 8+ concrete deliverables: {checklist_items} found.")
        if not has_marker(offer_stack, "data-offeros-value-row"):
            issues.append("Direct-response offer stack must include a normally/today value row marked data-offeros-value-row.")
        else:
            value_row = element_with_marker(offer_stack, "data-offeros-value-row")
            value_text = visible_text_from_html(value_row)
            if not re.search(r"\b(normally|regular|total value|value)\b", value_text, flags=re.I) or not re.search(r"\b(today|now)\b", value_text, flags=re.I):
                issues.append("Direct-response offer value row must contrast normal/total value with today's price.")
            if not contains_expected_price(value_row, price):
                issues.append("Direct-response offer value row must show manifest.price.")
        if not has_marker(offer_stack, "data-offeros-stack-cta"):
            issues.append("Direct-response offer stack must include a large stack CTA marked data-offeros-stack-cta.")
        if not anchor_hrefs_with_marker(offer_stack, "data-offeros-cta"):
            issues.append("Direct-response offer stack must include a data-offeros-cta purchase/access link.")
        if not has_marker(offer_stack, "data-offeros-access-copy"):
            issues.append("Direct-response offer stack must include guarantee/instant-access reassurance marked data-offeros-access-copy.")


def validate_logo(root: Path, manifest: dict, by_id: dict[str, dict], issues: list[str], warnings: list[str]) -> None:
    logo_artifact = by_id.get("logo")
    logo_path = artifact_path(root, logo_artifact)
    if not logo_path or not logo_path.exists():
        issues.append("Logo missing; cannot validate identity quality.")
        return

    logo_quality = manifest.get("quality", {}).get("logo", {})
    if not isinstance(logo_quality, dict):
        logo_quality = {}

    logo_direction_count = quality_number(logo_quality.get("logoDirectionCount"))
    if logo_direction_count != 1:
        issues.append("Logo quality metadata must record logoDirectionCount: 1 for single-final-logo mode.")
    if logo_quality.get("smallSizeChecked") is not True:
        issues.append("Logo quality metadata must confirm smallSizeChecked.")
    if logo_quality.get("oneColorChecked") is not True:
        issues.append("Logo quality metadata must confirm oneColorChecked.")
    if logo_quality.get("exportedPng") is not True:
        issues.append("Logo quality metadata must confirm exportedPng/bitmap preview.")
    if logo_quality.get("critiquePassed") is not True:
        issues.append("Logo quality metadata must confirm critiquePassed.")
    if logo_quality.get("logoLockup") is not True:
        issues.append("Logo quality metadata must confirm logoLockup so the primary logo is not icon-only.")
    if logo_quality.get("includesReadableOfferName") is not True:
        issues.append("Logo quality metadata must confirm includesReadableOfferName.")
    for key, label in {
        "exactOfferNamePreserved": "exactOfferNamePreserved",
        "markIsLogoSymbol": "markIsLogoSymbol",
        "markNotIllustration": "markNotIllustration",
        "markOneColorUsable": "markOneColorUsable",
        "wordmarkTypographyChecked": "wordmarkTypographyChecked",
        "wordmarkKerningChecked": "wordmarkKerningChecked",
        "professionalLockupApproved": "professionalLockupApproved",
        "lockupPreviewChecked": "lockupPreviewChecked",
    }.items():
        if logo_quality.get(key) is not True:
            issues.append(f"Logo quality metadata must confirm {label}.")
    if logo_quality.get("finalLogoLocked") is not True:
        issues.append("Logo quality metadata must confirm finalLogoLocked.")
    if logo_quality.get("singleFinalLogoOnly") is not True:
        issues.append("Logo quality metadata must confirm singleFinalLogoOnly.")
    if logo_quality.get("alternateLogosCreated") is not False:
        issues.append("Logo quality metadata must confirm alternateLogosCreated: false.")
    if str(logo_quality.get("downstreamLogoReference", "")).replace("\\", "/") != "assets/logo.png":
        issues.append("Logo quality metadata must record downstreamLogoReference: assets/logo.png.")
    if str(logo_quality.get("downstreamImagegenLogoReference", "")).replace("\\", "/") != "assets/logo.png":
        issues.append("Logo quality metadata must record downstreamImagegenLogoReference: assets/logo.png.")
    if logo_quality.get("downstreamImagegenMustUseLogoReference") is not True:
        issues.append("Logo quality metadata must confirm downstreamImagegenMustUseLogoReference.")
    if str(logo_quality.get("logoMode", "")).strip() != "single-final-logo-v1":
        issues.append("Logo quality metadata must record logoMode: single-final-logo-v1.")
    preview_path = str(logo_quality.get("lockupPreviewPath", "")).strip()
    if not preview_path:
        issues.append("Logo quality metadata must record lockupPreviewPath.")
    elif not (root / preview_path).exists():
        issues.append(f"Logo lockup preview path does not exist: {preview_path}")
    logo_provenance_for_source = (logo_artifact or {}).get("provenance", "")
    if (
        manifest.get("mode") == "deep"
        and logo_provenance_for_source not in {"provided", "licensed"}
        and str(logo_quality.get("brandMarkSource", "")).strip().lower() != "imagegen"
    ):
        issues.append("Logo quality metadata must record brandMarkSource: imagegen for deep generated-design runs.")

    provenance = (logo_artifact or {}).get("provenance", "")
    deep_run = manifest.get("mode") == "deep"
    design_type = str(manifest.get("designSource", {}).get("type", "")).strip()
    if deep_run and design_type in {"", "unresolved"}:
        issues.append("Deep runs must resolve designSource.type before completion. Use generated when creating a generated design direction.")
    logo_requires_imagegen = deep_run and provenance not in {"provided", "licensed"}
    if logo_requires_imagegen and logo_quality.get("imagegenCompleteLogoLockupAttempted") is not True:
        issues.append("Logo quality metadata must confirm imagegenCompleteLogoLockupAttempted.")
    if logo_requires_imagegen and quality_number(logo_quality.get("finalLogoCount")) != 1:
        issues.append("Logo quality metadata must record finalLogoCount: 1; do not create multiple logo options.")
    if logo_requires_imagegen and quality_number(logo_quality.get("logoGenerationCount")) != 1:
        issues.append("Logo quality metadata must record logoGenerationCount: 1; do not create multiple logo options.")
    if logo_path.suffix.lower() == ".svg":
        issues.append("OfferOS generated runs must not create or register SVG logo files. Rebuild the logo as PNG/WebP.")
    if logo_quality.get("svgAssetCreated") is not False:
        issues.append("Logo quality metadata must confirm svgAssetCreated: false.")
    logo_rel_path = str((logo_artifact or {}).get("path", "")).replace("\\", "/").lower()
    brand = manifest.get("brand", {})
    if not isinstance(brand, dict):
        brand = {}
    brand_logo = str(brand.get("logo", "")).replace("\\", "/").strip()
    brand_logo_lower = brand_logo.lower()
    if logo_requires_imagegen:
        if not brand_logo:
            issues.append("Generated-design deep runs must set brand.logo to assets/logo.png.")
        elif brand_logo_lower != logo_rel_path:
            issues.append("brand.logo must match the registered primary logo artifact path.")
        if brand_logo_lower.endswith(".svg"):
            issues.append("Generated-design deep runs must not set brand.logo to an SVG file.")
        if brand_logo_lower.endswith("logo-mark.png") or brand_logo_lower.endswith("logo-mark.webp") or "logo-mark" in Path(brand_logo_lower).stem:
            issues.append("brand.logo cannot point at a mark-only file such as logo-mark.")
        if logo_rel_path.endswith("logo-mark.png") or logo_rel_path.endswith("logo-mark.webp") or "logo-mark" in Path(logo_rel_path).stem:
            issues.append("Primary logo artifact cannot point at a mark-only file such as logo-mark; register the complete lockup at assets/logo.png.")
        if logo_rel_path and logo_rel_path != "assets/logo.png":
            issues.append("Generated-design deep runs must register the primary logo artifact path as assets/logo.png.")
        if logo_path.suffix.lower() not in BITMAP_EXTS:
            issues.append("Generated-design deep runs must use a bitmap primary logo file such as PNG or WebP.")
        else:
            dimensions = bitmap_dimensions(logo_path)
            if not dimensions:
                warnings.append("Could not inspect primary logo bitmap dimensions; install Pillow or regenerate the logo with a readable bitmap.")
            else:
                width, height = dimensions
                if width < 300 or height < 80:
                    issues.append(f"Primary logo bitmap is too small for a paid offer identity: {width}x{height}.")
                if width / max(height, 1) < 1.6:
                    issues.append(f"Primary logo bitmap must be a horizontal lockup, not a square/icon-like canvas: {width}x{height}.")
    primary_format = str(logo_quality.get("primaryFormat", "")).lower().strip()
    if logo_requires_imagegen and primary_format not in {"png", "webp", "jpg", "jpeg"}:
        issues.append("Logo quality metadata must record bitmap primaryFormat for generated-design deep runs.")
    imagegen_blocker = str(logo_quality.get("imagegenNotUsedReason", "")).strip()
    if logo_requires_imagegen and not imagegen_blocker and provenance != "imagegen":
        issues.append("Deep generated-design runs must register the primary logo with provenance: imagegen.")
    generation_tool = str(logo_quality.get("generationTool", "")).strip().lower()
    if logo_requires_imagegen and generation_tool != "imagegen-single-final-logo":
        issues.append("Logo generationTool must record imagegen-single-final-logo.")
    if provenance == "imagegen" and logo_quality.get("imagegenCompleteLogoAccepted") is not True:
        issues.append("Imagegen logos must confirm imagegenCompleteLogoAccepted.")
    if provenance == "imagegen-composite":
        issues.append("Generated-design logos must not use imagegen-composite by default; create one complete logo with imagegen.")
    if logo_requires_imagegen and imagegen_blocker and (logo_artifact or {}).get("status") == "complete":
        issues.append("Logo cannot be complete when quality.logo.imagegenNotUsedReason is set.")

def validate_ads(root: Path, by_id: dict[str, dict], issues: list[str], warnings: list[str]) -> None:
    ads_artifact = by_id.get("facebook-ads")
    ads_path = artifact_path(root, ads_artifact)
    if not ads_path or not ads_path.exists():
        issues.append("Facebook ads artifact missing; cannot validate ad-copy depth.")
        return
    if ads_path.suffix.lower() not in TEXT_EXTS:
        return
    raw_text = text_for(ads_path)
    text = raw_text
    if ads_path.suffix.lower() in {".html", ".htm"}:
        text = visible_text_from_html(raw_text)
    repeated = repeated_sentences(text, threshold=5)
    if repeated:
        examples = "; ".join(f"'{sentence[:80]}' x{count}" for sentence, count in repeated[:3])
        issues.append("Facebook ads contain repeated boilerplate copy: " + examples)
    repeated_blocks = repeated_body_blocks(raw_text, threshold=2)
    if repeated_blocks:
        examples = "; ".join(f"'{sentence[:80]}' x{count}" for sentence, count in repeated_blocks[:3])
        issues.append("Facebook ads contain repeated card/body copy: " + examples)


def validate_vsl(root: Path, manifest: dict, by_id: dict[str, dict], issues: list[str], warnings: list[str]) -> None:
    deck_artifact = by_id.get("vsl-deck")
    deck_path = artifact_path(root, deck_artifact)
    if not deck_path or not deck_path.exists():
        issues.append("VSL deck missing; cannot validate readiness.")
        return
    deck_preview = str((deck_artifact or {}).get("preview", "")).strip()
    if deck_preview:
        preview_suffix = Path(deck_preview).suffix.lower()
        if preview_suffix in {".pptx", ".ppt"}:
            issues.append("VSL deck preview must be browser-safe HTML or image, not the PowerPoint file itself.")
        if not (root / deck_preview).exists():
            issues.append(f"VSL deck preview path does not exist: {deck_preview}")

    slide_count = None
    deck_text = ""
    suffix = deck_path.suffix.lower()
    vsl_quality = manifest.get("quality", {}).get("vsl", {})
    if not isinstance(vsl_quality, dict):
        vsl_quality = {}
    vsl_source = artifact_path(root, by_id.get("vsl-deck-source"))
    if not vsl_source or not vsl_source.exists():
        issues.append("VSL Deck Studio requires canonical presentation/vsl-deck-plan.json source registered as vsl-deck-source.")
    if vsl_quality.get("studio") != "vsl-deck-studio-v1":
        issues.append("VSL quality metadata must record studio: vsl-deck-studio-v1.")
    if vsl_quality.get("backend") not in {"pptxgenjs", "presentations-plugin"}:
        issues.append("VSL quality metadata must record backend: pptxgenjs or presentations-plugin.")
    if vsl_quality.get("editableTextChecked") is not True:
        issues.append("VSL quality metadata must confirm editableTextChecked; flattened-image-only decks are not acceptable.")
    if suffix != ".pptx" and vsl_quality.get("nonPptxUserRequested") is not True:
        issues.append("Primary VSL deck must be a PowerPoint .pptx artifact. HTML belongs in vsl-preview, not vsl-deck.")
    if suffix == ".pptx":
        slide_count = count_pptx_slides(deck_path)
        slides = pptx_slide_texts(deck_path)
        stage_label_hits = visible_stage_labels(slides)
        if stage_label_hits:
            issues.append("VSL deck exposes internal stage labels as visible slide copy: " + "; ".join(stage_label_hits[:5]))
        notes = pptx_note_texts(deck_path)
        if slide_count and len(notes) < slide_count:
            issues.append(f"VSL deck must include speaker notes for every slide: {len(notes)} note slides found for {slide_count} slides.")
        short_notes = []
        for index, note_texts in enumerate(notes[: slide_count or len(notes)], 1):
            note_text = " ".join(note_texts)
            word_count = len(re.findall(r"\b[\w'-]+\b", note_text))
            if word_count < 25:
                short_notes.append(f"slide {index}: {word_count} words")
        if short_notes:
            issues.append("VSL speaker notes are too thin for recording guidance: " + "; ".join(short_notes[:5]))
        price_mismatches = []
        expected_price = numeric_price(manifest.get("price"))
        for index, note_texts in enumerate(notes[: slide_count or len(notes)], 1):
            note_text = " ".join(note_texts)
            mismatches = stale_price_mentions(note_text, expected_price)
            if mismatches:
                price_mismatches.append(f"slide {index}: {', '.join(mismatches)}")
        if price_mismatches:
            issues.append("VSL speaker notes mention prices that differ from manifest.price: " + "; ".join(price_mismatches[:5]))
        media_count = count_pptx_media(deck_path)
        visual_asset_count = quality_number(vsl_quality.get("visualAssetCount"))
        if media_count == 0 and visual_asset_count < 6 and vsl_quality.get("usesVectorDiagrams") is not True:
            issues.append("VSL PPTX has no embedded media and visualAssetCount is below 6; replace placeholder blocks with real visuals, diagrams, screenshots, or product previews.")
        if media_count and not pillow_available():
            issues.append("Cannot validate VSL PPTX image aspect ratios because Pillow is unavailable in the active Python runtime.")
        else:
            aspect_issues = pptx_image_aspect_issues(deck_path)
            if aspect_issues:
                issues.append("VSL PPTX image aspect ratio distortion detected: " + "; ".join(aspect_issues[:8]))
            reuse = pptx_large_bitmap_reuse(deck_path)
            if reuse.get("mostRepeatedLargeBitmapShare", 0) > 0.25:
                issues.append(
                    "VSL deck repeats the same large bitmap too often: "
                    f"{reuse.get('mostRepeatedLargeBitmapSlides')} of {reuse.get('slideCount')} slides "
                    f"({reuse.get('mostRepeatedLargeBitmapShare'):.2f}), must be <= 0.25."
                )
    elif suffix in {".html", ".htm"}:
        deck_text = text_for(deck_path)
        slide_count = count_html_slides(deck_text)
        compact = re.sub(r"\s+", "", deck_text.lower())
        if "display:grid" in compact and "grid-template-columns" in compact:
            issues.append("VSL deck appears to be a grid/contact sheet. Register that as vsl-preview; vsl-deck must be presentation-ready.")
    if slide_count is not None and slide_count < 20:
        issues.append(f"VSL deck has too few slides: {slide_count} found, 20+ expected.")

    expected = {
        "presentationReady": "presentation-ready deck",
        "hasSpeakerNotes": "speaker notes or narration guidance",
        "hasOfferReveal": "offer reveal",
        "hasPrice": "price slide",
        "hasGuarantee": "guarantee slide",
        "hasObjections": "objection handling slides",
    }
    for key, label in expected.items():
        if vsl_quality.get(key) is not True:
            issues.append(f"VSL quality metadata must confirm {label}.")
    layout_count = quality_number(vsl_quality.get("layoutCount"))
    if layout_count < 8:
        issues.append(f"VSL layout count below target: {layout_count or 'missing'} found, 8+ expected.")
    unique_visual_count = quality_number(vsl_quality.get("uniqueVisualAssetCount"))
    if unique_visual_count < 12:
        issues.append(f"VSL unique visual asset/treatment count below target: {unique_visual_count or 'missing'} found, 12+ expected.")
    vsl_specific_visual_count = quality_number(vsl_quality.get("vslSpecificVisualAssetCount"))
    if vsl_specific_visual_count < 8:
        issues.append(f"VSL-specific visual asset/treatment count below target: {vsl_specific_visual_count or 'missing'} found, 8+ expected.")
    max_repeated_bitmap_share = quality_float(vsl_quality.get("maxRepeatedBitmapShare"))
    if "maxRepeatedBitmapShare" not in vsl_quality:
        issues.append("VSL quality metadata must record maxRepeatedBitmapShare.")
    elif max_repeated_bitmap_share > 0.25:
        issues.append(f"VSL maxRepeatedBitmapShare too high: {max_repeated_bitmap_share:.2f}, must be <= 0.25.")
    if vsl_quality.get("visualReuseChecked") is not True:
        issues.append("VSL quality metadata must confirm visualReuseChecked.")
    max_layout_share = quality_float(vsl_quality.get("maxLayoutShare"))
    if not max_layout_share:
        issues.append("VSL quality metadata must record maxLayoutShare.")
    elif max_layout_share > 0.35:
        issues.append(f"VSL repeats one layout too often: maxLayoutShare {max_layout_share:.2f}, must be <= 0.35.")
    layout_audit = vsl_quality.get("layoutAudit")
    if not isinstance(layout_audit, list) or not layout_audit:
        issues.append("VSL quality metadata must include layoutAudit with slide, layoutFamily, and visualAsset for every slide.")
    elif slide_count is not None:
        if len(layout_audit) != slide_count:
            issues.append(f"VSL layoutAudit must include one entry per slide: {len(layout_audit)} entries for {slide_count} slides.")
        family_counts: dict[str, int] = {}
        missing_layout_fields = 0
        missing_visual_assets = 0
        for item in layout_audit:
            if not isinstance(item, dict) or not item.get("slide") or not item.get("layoutFamily"):
                missing_layout_fields += 1
                continue
            family = str(item.get("layoutFamily")).strip().lower()
            family_counts[family] = family_counts.get(family, 0) + 1
            if not str(item.get("visualAsset", "")).strip():
                missing_visual_assets += 1
        if missing_layout_fields:
            issues.append(f"VSL layoutAudit has {missing_layout_fields} entries missing slide/layoutFamily.")
        if missing_visual_assets:
            issues.append(f"VSL layoutAudit has {missing_visual_assets} entries missing visualAsset.")
        if family_counts and slide_count:
            audit_max_share = max(family_counts.values()) / slide_count
            if audit_max_share > 0.35:
                issues.append(f"VSL layoutAudit shows one layout family dominates: {audit_max_share:.2f}, must be <= 0.35.")
    for key, label in {
        "notesAreNarration": "notesAreNarration",
        "visibleStageLabelsRemoved": "visibleStageLabelsRemoved",
        "layoutDiversityChecked": "layoutDiversityChecked",
        "visualPlaceholdersRemoved": "visualPlaceholdersRemoved",
    }.items():
        if vsl_quality.get(key) is not True:
            issues.append(f"VSL quality metadata must confirm {label}.")
    if vsl_quality.get("primaryFormat") not in {"pptx", "powerpoint"} and vsl_quality.get("nonPptxUserRequested") is not True:
        issues.append("VSL quality metadata must record primaryFormat: pptx.")
    if slide_count is not None and quality_number(vsl_quality.get("slideCount")) and quality_number(vsl_quality.get("slideCount")) != slide_count:
        warnings.append("VSL metadata slide count does not match the inspected deck.")


def validate_qa_notes(root: Path, manifest: dict, by_id: dict[str, dict], issues: list[str], warnings: list[str]) -> None:
    qa_artifact = by_id.get("qa-notes")
    qa_path = artifact_path(root, qa_artifact)
    if not qa_path or not qa_path.exists():
        issues.append("QA notes missing; cannot validate final QA record.")
        return
    qa_text = text_for(qa_path)
    qa_lower = qa_text.lower()
    pdf_pages = quality_number(manifest.get("quality", {}).get("pdf", {}).get("pageCount"))
    if pdf_pages:
        page_claims = [int(value) for value in re.findall(r"\b(\d{1,3})-page\s+(?:workbook|pdf|product|toolkit|source)", qa_lower)]
        mismatches = sorted({value for value in page_claims if value != pdf_pages})
        if mismatches:
            issues.append(f"QA notes contain stale PDF page-count claims {mismatches}; manifest records {pdf_pages}.")
    if '"overflowx": true' in qa_lower:
        issues.append("QA notes record browser horizontal overflow; fix responsive layout before completion.")
    if re.search(r'"brokenimages"\s*:\s*\[[^\]]*[^\s\]]', qa_lower):
        issues.append("QA notes record broken browser images; fix assets before completion.")
    if "vsl preview" not in qa_lower and "vsl-preview" not in qa_lower:
        issues.append("QA notes must include browser QA for the VSL preview at desktop and mobile widths.")


def validate_dashboard(root: Path, manifest: dict, by_id: dict[str, dict], issues: list[str], warnings: list[str]) -> None:
    dashboard_artifact = by_id.get("delivery-dashboard")
    dashboard_path = artifact_path(root, dashboard_artifact)
    if not dashboard_path or not dashboard_path.exists():
        issues.append("Delivery dashboard missing; cannot validate modal template.")
        return
    html_text = text_for(dashboard_path)
    compact = re.sub(r"\s+", "", html_text.lower())
    requirements = {
        "data-offeros-dashboard=\"v2-modal\"": "standard v2 modal dashboard marker",
        "class=\"modal\"": "modal preview container",
        "<iframe": "iframe preview support",
        "data-preview=": "artifact preview data attributes",
        "data-path=": "artifact path data attributes",
        "queryselectorall('.card')": "card click preview binding",
    }
    for token, label in requirements.items():
        if token not in compact:
            issues.append(f"Delivery dashboard missing {label}. Use scripts/generate_delivery_dashboard.py and theme it instead of hand-rolling a static grid.")
    deck_artifact = by_id.get("vsl-deck")
    if deck_artifact:
        deck_path = deck_artifact.get("path", "")
        deck_preview = deck_artifact.get("preview", "")
        if deck_path and f'data-path="{deck_path.lower()}"' not in compact:
            issues.append("Delivery dashboard must preserve the VSL deck data-path so Open Deck opens the PPTX.")
        if deck_preview and f'data-preview="{deck_preview.lower()}"' not in compact:
            issues.append("Delivery dashboard must use the browser-safe VSL deck preview in data-preview.")
        if deck_path and deck_preview and deck_path == deck_preview and Path(deck_path).suffix.lower() in {".pptx", ".ppt"}:
            issues.append("Delivery dashboard must not iframe the PPTX as its card preview; use vsl-preview HTML/image.")
    dashboard_quality = manifest.get("quality", {}).get("dashboard", {})
    if not isinstance(dashboard_quality, dict):
        dashboard_quality = {}
    if dashboard_quality.get("templateVersion") != "v2-modal":
        issues.append("Dashboard quality metadata must record templateVersion: v2-modal.")
    if dashboard_quality.get("hasModalPreview") is not True:
        issues.append("Dashboard quality metadata must confirm hasModalPreview.")
    if dashboard_quality.get("hasIframePreview") is not True:
        issues.append("Dashboard quality metadata must confirm hasIframePreview.")


def validate_visual_asset_plan(root: Path, manifest: dict, by_id: dict[str, dict], issues: list[str], warnings: list[str]) -> None:
    plan_artifact = by_id.get("visual-asset-plan")
    plan_path = artifact_path(root, plan_artifact)
    if not plan_path or not plan_path.exists():
        issues.append("Visual asset plan missing; create visual-asset-plan.md before PDF, ads, VSL, and dashboard production.")
        return

    text = text_for(plan_path)
    lower_text = text.lower()
    required_headings = [
        "# Visual Asset Plan",
        "## Visual Plan Metadata",
        "## Global Brand Assets",
        "## Sales Page Visuals",
        "## PDF Product Visuals",
        "## VSL Deck Visuals",
        "## Ad Visuals",
        "## Dashboard Visuals",
        "## Reuse Rules",
    ]
    missing_headings = [heading for heading in required_headings if heading.lower() not in text.lower()]
    if missing_headings:
        issues.append("Visual asset plan missing required headings: " + ", ".join(missing_headings))
    if re.search(r"\b(?:generate|redraw|create|invent|redesign|recolor|reinterpret|replace|substitute)\b.{0,80}\b(?:logo|wordmark)\b", lower_text, flags=re.I | re.S):
        issues.append("Visual asset plan must not ask imagegen to generate/redraw/reinvent logos or wordmarks; pass assets/logo.png as the exact logo reference.")
    if re.search(r"\b(?:rejected|alternate|alternative|old)\b.{0,50}\b(?:logo|lockup|mark)\b", lower_text, flags=re.I | re.S):
        issues.append("Visual asset plan must not reference rejected, old, or alternate logos for downstream assets.")
    compact_plan = re.sub(r"\s+", "", text.lower())
    for token, label in {
        "logoreference:assets/logo.png": "logoReference: assets/logo.png",
        "logousagepolicy:use-locked-logo-reference": "logoUsagePolicy: use-locked-logo-reference",
        "alternatelogoscreated:false": "alternateLogosCreated: false",
    }.items():
        if token not in compact_plan:
            issues.append(f"Visual asset plan metadata must include {label}.")
    logo_prompt_leaks = []
    for line in text.splitlines():
        lower_line = line.lower()
        if "prompt" not in lower_line and "generationprompt" not in lower_line:
            continue
        if re.search(r"\b(?:logo|wordmark|brand mark)\b", lower_line) and "assets/logo.png" not in lower_line:
            logo_prompt_leaks.append(line.strip()[:140])
    if logo_prompt_leaks:
        issues.append(
            "Downstream imagegen prompts that need a logo must reference assets/logo.png as the exact supplied logo: "
            + "; ".join(logo_prompt_leaks[:5])
        )

    sales_copy = by_id.get("sales-copy")
    sales_copy_path = artifact_path(root, sales_copy)
    if not sales_copy_path or not sales_copy_path.exists():
        issues.append("Visual asset plan v2 requires copy.md/sales-copy with a section blueprint before visual planning.")

    for token, label in {
        "visualplanstage:post-content-blueprint": "visualPlanStage: post-content-blueprint",
        "copyblueprintused:true": "copyBlueprintUsed: true",
        "copystudioused:true": "copyStudioUsed: true",
        "copyplanpath:copy-plan.json": "copyPlanPath: copy-plan.json",
        "salespageimagesystem:mixed-direct-response-v1": "salesPageImageSystem: mixed-direct-response-v1",
        "aspectratiopolicy:slot-aware-v1": "aspectRatioPolicy: slot-aware-v1",
    }.items():
        if token not in compact_plan:
            issues.append(f"Visual asset plan metadata must include {label}.")

    image_quality = manifest.get("quality", {}).get("images", {})
    if not isinstance(image_quality, dict):
        image_quality = {}
    if image_quality.get("hasArtifactSpecificPlan") is not True:
        issues.append("Image quality metadata must confirm hasArtifactSpecificPlan.")
    plan_meta_path = str(image_quality.get("visualPlanPath", "")).strip()
    if plan_meta_path and not (root / plan_meta_path).exists():
        issues.append(f"Image quality metadata visualPlanPath does not exist: {plan_meta_path}")
    elif not plan_meta_path:
        issues.append("Image quality metadata must record visualPlanPath.")
    plan_json_path = str(image_quality.get("visualPlanJsonPath", "visual-asset-plan.json")).strip()
    if not (root / plan_json_path).exists():
        issues.append(f"Canonical visual-asset-plan.json missing: {plan_json_path}")
    if image_quality.get("visualReusePolicy") != "artifact-specific-v1":
        issues.append("Image quality metadata must record visualReusePolicy: artifact-specific-v1.")
    if image_quality.get("visualPlanStage") != "post-content-blueprint":
        issues.append("Image quality metadata must record visualPlanStage: post-content-blueprint.")
    if image_quality.get("copyBlueprintUsed") is not True:
        issues.append("Image quality metadata must confirm copyBlueprintUsed.")
    if image_quality.get("copyStudioUsed") is not True:
        issues.append("Image quality metadata must confirm copyStudioUsed.")
    if image_quality.get("copyPlanPath") != "copy-plan.json":
        issues.append("Image quality metadata must record copyPlanPath: copy-plan.json.")
    if image_quality.get("salesPageImageSystem") != "mixed-direct-response-v1":
        issues.append("Image quality metadata must record salesPageImageSystem: mixed-direct-response-v1.")
    if image_quality.get("primaryConversionFinalPixelsPolicy") != "imagegen-final-v1":
        issues.append("Image quality metadata must record primaryConversionFinalPixelsPolicy: imagegen-final-v1.")
    if image_quality.get("aspectRatioPolicy") != "slot-aware-v1":
        issues.append("Image quality metadata must record aspectRatioPolicy: slot-aware-v1.")
    if image_quality.get("logoReference") != "assets/logo.png":
        issues.append("Image quality metadata must record logoReference: assets/logo.png.")
    if image_quality.get("logoUsagePolicy") != "use-locked-logo-reference":
        issues.append("Image quality metadata must record logoUsagePolicy: use-locked-logo-reference.")
    if image_quality.get("alternateLogosCreated") is not False:
        issues.append("Image quality metadata must confirm alternateLogosCreated: false.")

    required_counts = {
        "salesPageVisualCount": 4,
        "pdfVisualCount": 6,
        "pdfSpecificVisualCount": 4,
        "vslVisualCount": 12,
        "vslSpecificVisualCount": 8,
        "adImageCount": 3,
    }
    for field, minimum in required_counts.items():
        value = quality_number(image_quality.get(field))
        if value < minimum:
            issues.append(f"Image quality metadata {field} below target: {value or 'missing'} found, {minimum}+ expected.")

    for field, label in {
        "pdfUsesOnlySalesPageImages": "PDF visuals cannot be only reused sales-page images.",
        "vslUsesOnlySalesPageImages": "VSL visuals cannot be only reused sales-page images.",
        "salesPageReuseOnly": "Visual system cannot be sales-page-reuse-only.",
    }.items():
        if image_quality.get(field) is True:
            issues.append(label)

    sales_visuals = markdown_section(text, "## Sales Page Visuals")
    visual_kinds = field_values(sales_visuals, "visualKind")
    copy_anchors = [normalize_copy_anchor(item) for item in field_values(sales_visuals, "copyAnchor")]
    required_sales_fields = {
        "visualKind": visual_kinds,
        "copyAnchor": copy_anchors,
        "conversionJob": field_values(sales_visuals, "conversionJob"),
        "artifactTarget": field_values(sales_visuals, "artifactTarget"),
        "aspectRatio": field_values(sales_visuals, "aspectRatio"),
        "textRule": field_values(sales_visuals, "textRule"),
    }
    for field, values in required_sales_fields.items():
        if len(values) < 4:
            issues.append(f"Sales-page visual plan must include 4+ {field} fields tied to copy sections.")
    aspect_values = field_values(sales_visuals, "aspectRatio")
    if len(set(aspect_values)) < 3:
        issues.append("Sales-page visual plan must use slot-aware varied aspect ratios, not one repeated default ratio.")
    if len(field_values(sales_visuals, "aspectRatioReason")) < 4:
        issues.append("Sales-page visual plan must include aspectRatioReason fields explaining page-slot fit.")
    if len(field_values(sales_visuals, "displayIntent")) < 4:
        issues.append("Sales-page visual plan must include displayIntent fields for page-slot fit.")
    invalid_kinds = sorted({kind for kind in visual_kinds if kind not in ALLOWED_VISUAL_KINDS})
    if invalid_kinds:
        issues.append("Sales-page visual plan uses invalid visualKind values: " + ", ".join(invalid_kinds))
    valid_anchors = set(REQUIRED_SALES_PAGE_SECTIONS)
    invalid_anchors = sorted({anchor for anchor in copy_anchors if anchor and anchor not in valid_anchors})
    if invalid_anchors:
        issues.append("Sales-page visual plan copyAnchor values must match real data-offeros-section anchors: " + ", ".join(invalid_anchors))
    if visual_kinds and all(kind in MOCKUP_VISUAL_KINDS or "mockup" in kind for kind in visual_kinds):
        if image_quality.get("mockupHeavyUserRequested") is not True:
            issues.append("Sales-page visual plan is all mockup/UI-style visuals; use mixed-direct-response-v1 unless mockupHeavyUserRequested is true.")

    sales_rows = markdown_field_rows(sales_visuals)
    primary_plan_rows = [
        row for row in sales_rows
        if str(row.get("visualKind", "")).strip().lower() in IMAGEGEN_REQUIRED_VISUAL_KINDS
    ]
    for row in primary_plan_rows:
        normalized = {key: value for key, value in row.items()}
        normalized["id"] = normalized.get("artifactTarget") or normalized.get("filePath") or normalized.get("visualKind")
        normalized["provenance"] = normalized.get("source/provenance", "")
        for issue in primary_conversion_metadata_issues(normalized, "Sales-page primary conversion visual plan row"):
            issues.append(issue)

    code_rendered_rows = []
    for line in text.splitlines():
        lower_line = line.lower()
        matched_kind = next((kind for kind in IMAGEGEN_REQUIRED_VISUAL_KINDS if kind in lower_line), "")
        if not matched_kind:
            continue
        if any(provenance in lower_line for provenance in CODE_RENDERED_PROVENANCE):
            code_rendered_rows.append(f"{matched_kind}: {line.strip()[:140]}")
    if code_rendered_rows:
        issues.append(
            "Imagegen-required creative visuals cannot use PIL/HTML/CSS/code/screenshot fallback provenance: "
            + "; ".join(code_rendered_rows[:5])
        )

    ad_visuals = markdown_section(text, "## Ad Visuals")
    ad_rows = markdown_field_rows(ad_visuals)
    ad_final_rows = [
        row for row in ad_rows
        if str(row.get("source/provenance", "")).strip().lower() in {"imagegen-final", "provided", "licensed"}
        or (
            str(row.get("source/provenance", "")).strip().lower() == "imagegen-composite"
            and str(row.get("finalPixelsGeneratedBy", "")).strip().lower() == "imagegen"
            and bool_field(row.get("imagegenNativeComposite")) is True
        )
    ]
    if ad_visuals and len(ad_final_rows) < 3:
        issues.append("Ad visual plan must include 3+ ad rows with final buyer-facing pixels from imagegen: source/provenance imagegen-final, or imagegen-composite with imagegenNativeComposite: true.")
    for row in ad_rows:
        if str(row.get("visualKind", "")).strip().lower() == "ad-creative":
            normalized = {key: value for key, value in row.items()}
            normalized["id"] = normalized.get("artifactTarget") or normalized.get("filePath") or "ad-creative"
            normalized["provenance"] = normalized.get("source/provenance", "")
            for issue in primary_conversion_metadata_issues(normalized, "Ad creative visual plan row"):
                issues.append(issue)


def validate_images(manifest: dict, artifacts: list[dict], issues: list[str], warnings: list[str]) -> None:
    imagegen_count = 0
    real_bitmap_count = 0
    deep_generated_design = manifest.get("mode") == "deep" and manifest.get("designSource", {}).get("type") == "generated"
    for artifact in artifacts:
        rel_path = artifact.get("path", "")
        suffix = Path(rel_path).suffix.lower()
        is_image = artifact.get("type") == "image" or suffix in IMAGE_EXTS or artifact.get("category") in {"Images", "Ads"}
        if not is_image:
            continue
        provenance = artifact.get("provenance", "")
        if not provenance:
            issues.append(f"Image artifact missing provenance: {artifact.get('id', rel_path)}")
        elif provenance not in ALLOWED_PROVENANCE:
            issues.append(f"Image artifact has invalid provenance '{provenance}': {artifact.get('id', rel_path)}")
        if manifest.get("mode") == "deep" and provenance == "pil-generated":
            issues.append(
                f"Pillow/PIL-generated image artifacts are not allowed in OfferOS deep runs: {artifact.get('id', rel_path)}. "
                "Use imagegen-final for primary creative images or render diagrams in HTML/CSS without registering a PIL-authored image."
            )
        if generated_claim(artifact) and provenance not in {"imagegen", "imagegen-final", "imagegen-composite"}:
            issues.append(f"Artifact claims generated imagery without imagegen/imagegen-final/imagegen-composite provenance: {artifact.get('id', rel_path)}")
        if deep_generated_design and is_imagegen_required_creative(artifact):
            primary_issues = primary_conversion_metadata_issues(artifact, "Primary conversion image artifact")
            if primary_issues:
                issues.extend(primary_issues)
                issues.append(
                    "Generated-design deep runs must create primary conversion visuals with final buyer-facing pixels from imagegen "
                    f"(or provided/licensed source), not local composition: {artifact.get('id', rel_path)} ({rel_path}). "
                    "PIL/HTML/CSS/canvas/screenshot/generated-by-code/manual PNGs and local overlays cannot satisfy product bundle, "
                    "hero/VSL thumbnail, product mockup, buyer-situation photo, or ad creative requirements."
                )
        if provenance in {"imagegen", "imagegen-final", "imagegen-composite"}:
            imagegen_count += 1
            if suffix == ".svg":
                issues.append(f"Imagegen artifact should be bitmap, not SVG: {artifact.get('id', rel_path)}")
        if provenance in {"imagegen", "imagegen-final", "imagegen-composite", "provided", "licensed"} and suffix in BITMAP_EXTS:
            real_bitmap_count += 1

    image_quality = manifest.get("quality", {}).get("images", {})
    if not isinstance(image_quality, dict):
        image_quality = {}
    if manifest.get("mode") == "deep":
        if manifest.get("designSource", {}).get("type") == "generated" and imagegen_count < 3 and not image_quality.get("imagegenNotUsedReason"):
            issues.append("Generated-design deep runs should include at least 3 imagegen bitmap artifacts or record imagegenNotUsedReason.")
        if real_bitmap_count < 3 and not image_quality.get("bitmapNotUsedReason"):
            warnings.append("Deep runs should include at least 3 real bitmap visual assets for hero/product/ad use.")


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate registered OfferOS outputs.")
    parser.add_argument("--manifest", default="offer-os.json")
    parser.add_argument("--workspace", default=".")
    parser.add_argument("--strict", action="store_true", help="Require all deep-mode core artifacts.")
    parser.add_argument("--write-report", default="", help="Optional QA report path.")
    parser.add_argument("--no-write", action="store_true", help="Do not update offer-os.json with QA results.")
    args = parser.parse_args()

    root = Path(args.workspace).resolve()
    manifest_path = root / args.manifest
    manifest = load_json(manifest_path)
    issues = []
    warnings = []

    for key in ["schema", "offerName", "audience", "modules", "artifacts"]:
        if key not in manifest:
            issues.append(f"Manifest missing key: {key}")

    artifacts = manifest.get("artifacts", [])
    if not isinstance(artifacts, list):
        issues.append("Manifest artifacts must be a list of artifact objects.")
        artifacts = []
    by_id = artifact_map(artifacts)

    deep_required = args.strict or manifest.get("mode") == "deep"
    if deep_required:
        for artifact_id in DEEP_REQUIRED_IDS:
            if artifact_id not in by_id:
                issues.append(f"Missing required deep artifact registration: {artifact_id}")

    ad_image_count = sum(1 for item in artifacts if item.get("category") == "Ads" and item.get("type") == "image")
    if deep_required and ad_image_count < 3:
        issues.append("Deep mode must register at least 3 Facebook ad images in category Ads.")

    for artifact in artifacts:
        rel_path = artifact.get("path", "")
        if not rel_path:
            issues.append(f"Artifact missing path: {artifact.get('id', 'unknown')}")
            continue
        if deep_required and Path(rel_path).suffix.lower() == ".svg":
            issues.append(
                f"Deep OfferOS runs must not create or register SVG artifacts. "
                f"Rebuild as PNG/WebP/JPG or HTML/CSS without .svg: {artifact.get('id', rel_path)} ({rel_path})"
            )
        path = root / rel_path
        if not path.exists():
            issues.append(f"Missing artifact file: {rel_path}")
            continue
        if path.suffix.lower() in TEXT_EXTS:
            tokens = scan_text(path)
            for token in tokens:
                issues.append(f"Possible unresolved token in {rel_path}: {token}")

        preview = artifact.get("preview")
        if preview and not (root / preview).exists():
            issues.append(f"Missing preview for {rel_path}: {preview}")

        if artifact.get("status") in {"draft", "needs_revision", "planned"}:
            warnings.append(f"Artifact is not complete: {artifact.get('id', rel_path)} ({artifact.get('status')})")

    if deep_required:
        validate_studio_source_control(root, manifest, issues)
        validate_sales_copy(root, manifest, by_id, issues, warnings)
        validate_visual_asset_plan(root, manifest, by_id, issues, warnings)
        validate_images(manifest, artifacts, issues, warnings)
        validate_logo(root, manifest, by_id, issues, warnings)
        validate_ads(root, by_id, issues, warnings)
        validate_email_sequence(root, manifest, by_id, issues, warnings)
        validate_sales_page(root, manifest, by_id, issues, warnings)
        validate_pdf(root, manifest, by_id, issues, warnings)
        validate_vsl(root, manifest, by_id, issues, warnings)
        validate_dashboard(root, manifest, by_id, issues, warnings)
        validate_qa_notes(root, manifest, by_id, issues, warnings)
        audit_scores_ok(manifest.get("commercialAudit", {}), issues, warnings)
        qa = manifest.get("qa", {})
        if not isinstance(qa, dict):
            issues.append("QA metadata missing or invalid.")
        else:
            technical = qa.get("technical", {})
            commercial = qa.get("commercial", {})
            if not isinstance(technical, dict) or str(technical.get("status", "")).lower() not in {"passed", "complete", "validated"}:
                issues.append("QA metadata must include technical.status passed/complete/validated.")
            if not isinstance(commercial, dict) or str(commercial.get("status", "")).lower() not in {"passed", "complete", "validated"}:
                issues.append("QA metadata must include commercial.status passed/complete/validated.")

    result = {
        "ok": not issues,
        "issueCount": len(issues),
        "warningCount": len(warnings),
        "issues": issues,
        "warnings": warnings,
    }

    if not args.no_write:
        qa = manifest.setdefault("qa", {})
        qa.update(
            {
                "lastRun": datetime.now(timezone.utc).isoformat(),
                "status": "passed" if not issues else "failed",
                "issues": issues,
                "warnings": warnings,
            }
        )
        qa.setdefault("technical", {})
        qa.setdefault("commercial", {})
        if issues:
            qa["technical"].setdefault("status", "failed")
            qa["commercial"].setdefault("status", "failed")
        manifest_path.write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")

    if args.write_report:
        report_path = root / args.write_report
        lines = [
            "# OfferOS QA Report",
            "",
            f"Status: {'PASSED' if not issues else 'FAILED'}",
            f"Issues: {len(issues)}",
            f"Warnings: {len(warnings)}",
            "",
            "## Issues",
            *(f"- {issue}" for issue in issues),
            "",
            "## Warnings",
            *(f"- {warning}" for warning in warnings),
            "",
        ]
        report_path.write_text("\n".join(lines), encoding="utf-8")

    print(json.dumps(result, indent=2))
    return 0 if not issues else 1


if __name__ == "__main__":
    raise SystemExit(main())
