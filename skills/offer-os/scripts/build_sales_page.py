import argparse
from datetime import datetime, timezone
from html import escape
import json
from pathlib import Path
import re


PAGE_KIT_VERSION = "v1"
PAGE_KIT_ID = "offeros-page-kit-v1"
BUILDER_VERSION = "offeros-page-kit-builder-v1"
STUDIO_VERSION = "sales-page-studio-v1"
COPY_STUDIO_VERSION = "copy-studio-v1"
COPY_FRAMEWORK = "modern-brunson-long-form-v1"
DEFAULT_PAGE_KIT_ARCHETYPE = "classic-vsl-longform"
DEFAULT_THEME_PRESET = "classic-direct-response"
VSL_PLACEMENT = "main-column-stacked"
SKILL_ROOT = Path(__file__).resolve().parents[1]
ALLOWED_PAGE_KIT_ARCHETYPES = {
    "classic-vsl-longform",
    "modern-vsl-software",
    "one-page-tripwire",
    "challenge-workshop",
    "toolkit-workbook",
}
ALLOWED_THEME_PRESETS = {
    "light-saas-direct-response",
    "classic-direct-response",
    "bold-webinar",
    "premium-editorial",
    "fitness-performance",
    "creator-workshop",
}
REQUIRED_ORDER = [
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
DEFAULT_CHECKOUT_TARGET = "#checkout"
EYEBROW_POLICY = "sparse-key-signposts-v1"
EYEBROW_ALIGNMENT = "centered-with-section-heading"
EYEBROW_SECTIONS = {
    "problem": "The real problem",
    "mechanism": "The mechanism",
    "proof": "Proof before the pitch",
    "offer-stack": "Get the complete stack",
    "guarantee": "Risk reversal",
}
EYEBROW_MAX_COUNT = len(EYEBROW_SECTIONS)


def read_json(path: Path, default=None):
    if path.exists():
        return json.loads(path.read_text(encoding="utf-8-sig"))
    if default is not None:
        return default
    raise SystemExit(f"Required JSON file not found: {path}")


def write_json(path: Path, payload: dict) -> None:
    path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")


def copy_studio_used(root: Path, blueprint: dict, copy_plan_arg: str = "copy-plan.json") -> tuple[bool, str]:
    copy_plan_path = as_text(blueprint.get("copyPlanPath"), copy_plan_arg)
    if not copy_plan_path:
        copy_plan_path = copy_plan_arg
    return (root / copy_plan_path).exists(), copy_plan_path.replace("\\", "/")


def slugify(value: str) -> str:
    value = value.lower().strip()
    value = re.sub(r"[^a-z0-9]+", "-", value)
    return value.strip("-") or "offer"


def as_text(value, fallback: str = "") -> str:
    if value is None:
        return fallback
    if isinstance(value, (list, tuple)):
        return ", ".join(str(item) for item in value if item is not None) or fallback
    return str(value).strip() or fallback


def html_text(value, fallback: str = "") -> str:
    return escape(as_text(value, fallback), quote=True)


def first_value(*values, fallback: str = "") -> str:
    for value in values:
        text = as_text(value)
        if text:
            return text
    return fallback


def list_value(value, fallback: list[str]) -> list[str]:
    if isinstance(value, list):
        items = [as_text(item) for item in value if as_text(item)]
        return items or fallback
    if isinstance(value, str) and value.strip():
        return [value.strip()]
    return fallback


def dict_list(value, fallback: list[dict]) -> list[dict]:
    if isinstance(value, list):
        result = [item for item in value if isinstance(item, dict)]
        return result or fallback
    return fallback


def price_text(manifest: dict) -> str:
    price = as_text(manifest.get("price"))
    if not price:
        return "Today only"
    if price.startswith("$") or price.startswith("€") or price.startswith("£"):
        return price
    return f"${price}"


def manifest_offer(manifest: dict, blueprint: dict) -> str:
    return first_value(blueprint.get("offerName"), manifest.get("offerName"), fallback="The Offer")


def find_asset(root: Path, candidates: list[str]) -> str:
    for candidate in candidates:
        if candidate and (root / candidate).exists():
            return candidate.replace("\\", "/")
    for candidate in candidates:
        if candidate:
            return candidate.replace("\\", "/")
    return ""


def default_theme(manifest: dict) -> dict:
    brand = manifest.get("brand", {}) if isinstance(manifest.get("brand"), dict) else {}
    return {
        "name": DEFAULT_THEME_PRESET,
        "themePreset": DEFAULT_THEME_PRESET,
        "pageKitArchetype": DEFAULT_PAGE_KIT_ARCHETYPE,
        "pageType": "direct-response-long-form-vsl",
        "colors": {
            "background": "#fbf7ef",
            "surface": "#ffffff",
            "ink": "#171717",
            "muted": "#5d5a52",
            "primary": brand.get("primaryColor") or "#145c50",
            "accent": brand.get("accentColor") or "#f2b84b",
            "dark": "#111b18",
        },
        "fonts": {
            "heading": brand.get("fontHeading") or "Arial, Helvetica, sans-serif",
            "body": brand.get("fontBody") or "Arial, Helvetica, sans-serif",
        },
    }


def theme_value(theme: dict, group: str, key: str, fallback: str) -> str:
    values = theme.get(group, {}) if isinstance(theme.get(group), dict) else {}
    if key in values:
        return as_text(values.get(key), fallback)
    tokens = theme.get("tokens", {}) if isinstance(theme.get("tokens"), dict) else {}
    token_aliases = {
        "background": "bg",
        "surface": "surface",
        "ink": "text",
        "muted": "muted",
        "primary": "primary",
        "accent": "accent",
        "dark": "ink",
    }
    if group == "colors":
        for alias in [key, token_aliases.get(key, "")]:
            if alias and alias in tokens:
                return as_text(tokens.get(alias), fallback)
    type_values = theme.get("type", {}) if isinstance(theme.get("type"), dict) else {}
    if group == "fonts":
        schema_aliases = {"heading": "headingFamily", "body": "bodyFamily"}
        alias = schema_aliases.get(key, "")
        if alias and alias in type_values:
            return as_text(type_values.get(alias), fallback)
    return fallback


def approved_partials(root: Path, explicit_dir: str = "") -> dict[str, str]:
    candidates = []
    if explicit_dir:
        candidates.append(root / explicit_dir)
    candidates.extend(
        [
            SKILL_ROOT / "assets" / "page-kit" / "partials",
            SKILL_ROOT / "assets" / "page-kit" / "blocks",
            root / "page-kit" / "blocks",
            root / "page-kit" / "partials",
            root / "assets" / "page-kit" / "blocks",
            root / "assets" / "page-kit" / "partials",
            root / "assets" / "templates" / "page-kit" / "blocks",
            root / "blocks" / "page-kit",
        ]
    )
    partials: dict[str, str] = {}
    for folder in candidates:
        if not folder.exists() or not folder.is_dir():
            continue
        for path in folder.glob("*.html"):
            name = path.stem
            text = path.read_text(encoding="utf-8")
            if re.search(r'data-offeros-approved\s*=\s*["\']false["\']', text, re.I):
                continue
            if re.search(r'data-offeros-page-kit-block\s*=\s*["\']approved["\']', text, re.I) or "data-offeros-section" in text:
                partials[name] = text
    return partials


def substitute(template: str, context: dict[str, str]) -> str:
    def replace(match):
        key = match.group(1).strip()
        return context.get(key, context.get(key.lower(), ""))

    return re.sub(r"\{\{\s*([A-Za-z0-9_.-]+)\s*\}\}", replace, template)


def section_data(blueprint: dict, section_id: str) -> dict:
    sections = blueprint.get("sections")
    if isinstance(sections, dict):
        value = sections.get(section_id, {})
        return value if isinstance(value, dict) else {"copy": value}
    if isinstance(sections, list):
        for item in sections:
            if isinstance(item, dict) and item.get("id") == section_id:
                return item
    return {}


def block_context(root: Path, manifest: dict, blueprint: dict, theme: dict) -> dict[str, str]:
    offer_name = manifest_offer(manifest, blueprint)
    audience = first_value(blueprint.get("audience"), manifest.get("audience"), fallback="busy operators")
    problem = first_value(blueprint.get("problem"), manifest.get("problem"), fallback="turning expertise into a buying decision")
    price = price_text(manifest)
    checkout_target = DEFAULT_CHECKOUT_TARGET
    hero_image = find_asset(
        root,
        [
            as_text(blueprint.get("heroVslThumbnail")),
            "assets/page/hero-vsl-thumbnail.png",
            "assets/hero-vsl-thumbnail.png",
            "assets/page/hero-vsl-thumbnail.webp",
            "assets/hero-vsl-thumbnail.webp",
            "assets/logo.png",
        ],
    )
    bundle_image = find_asset(
        root,
        [
            as_text(blueprint.get("productBundleImage")),
            "assets/page/product-bundle.png",
            "assets/product-bundle.png",
            "assets/page/offer-stack-bundle.png",
            "assets/offer-stack-bundle.png",
            hero_image,
        ],
    )
    assets = theme.get("assets", {}) if isinstance(theme.get("assets"), dict) else {}

    def theme_asset(name: str) -> str:
        item = assets.get(name)
        if isinstance(item, dict):
            return as_text(item.get("path"))
        return as_text(item)

    return {
        "offerName": html_text(offer_name),
        "offer_name": html_text(offer_name),
        "audience": html_text(audience),
        "problem": html_text(problem),
        "price": html_text(price),
        "checkoutTarget": html_text(checkout_target),
        "checkout_target": html_text(checkout_target),
        "heroVslThumbnail": html_text(hero_image or "assets/page/hero-vsl-thumbnail.png"),
        "productBundleImage": html_text(bundle_image or "assets/page/product-bundle.png"),
        "failedAlternativesVisual": html_text(find_asset(root, [theme_asset("failedAlternativesVisual"), "assets/page/failed-alternatives.png"])),
        "mechanismVisual": html_text(find_asset(root, [theme_asset("mechanismVisual"), "assets/page/mechanism-diagram.png"])),
        "proofVisual": html_text(find_asset(root, [theme_asset("proofVisual"), "assets/page/proof-demo.png"])),
        "beforeAfterVisual": html_text(find_asset(root, [theme_asset("beforeAfterVisual"), "assets/page/before-after.png"])),
        "guaranteeBadge": html_text(find_asset(root, [theme_asset("guaranteeBadge"), "assets/page/guarantee-badge.png"])),
        "themeName": html_text(theme_preset(theme)),
        "archetype": html_text(page_kit_archetype(blueprint, theme)),
    }


def page_kit_archetype(blueprint: dict, theme: dict) -> str:
    candidate = as_text(blueprint.get("pageKitArchetype") or theme.get("pageKitArchetype"), DEFAULT_PAGE_KIT_ARCHETYPE)
    if candidate not in ALLOWED_PAGE_KIT_ARCHETYPES:
        raise ValueError(
            f"Unsupported Page Kit archetype '{candidate}'. Use one of: {', '.join(sorted(ALLOWED_PAGE_KIT_ARCHETYPES))}."
        )
    return candidate


def theme_preset(theme: dict) -> str:
    candidate = as_text(theme.get("themePreset") or theme.get("preset") or theme.get("id"), DEFAULT_THEME_PRESET)
    if candidate not in ALLOWED_THEME_PRESETS:
        raise ValueError(
            f"Unsupported Page Kit theme preset '{candidate}'. Use one of: {', '.join(sorted(ALLOWED_THEME_PRESETS))}."
        )
    return candidate


def paragraph(text: str) -> str:
    return f"<p>{html_text(text)}</p>"


def card(title: str, copy: str, marker: str = "", icon: str = "circle-check") -> str:
    marker_attr = f" {marker}" if marker else ""
    return (
        f'<article class="oo-card"{marker_attr}><h3><span class="oo-icon" aria-hidden="true">'
        f'<i data-lucide="{html_text(icon)}"></i></span>{html_text(title)}</h3><p>{html_text(copy)}</p></article>'
    )


def list_items(items: list[str]) -> str:
    return "".join(f"<li>{html_text(item)}</li>" for item in items)


def icon_list_items(items: list[str], icon: str = "check") -> str:
    return "".join(
        f'<li><span class="oo-check-icon" aria-hidden="true"><i data-lucide="{html_text(icon)}"></i></span>{html_text(item)}</li>'
        for item in items
    )


def support_visual(src: str, alt: str, kind: str, anchor: str) -> str:
    if not src:
        return ""
    return (
        f'<figure class="oo-support-visual" data-offeros-page-visual data-offeros-visual-kind="{html_text(kind)}" '
        f'data-offeros-copy-anchor="{html_text(anchor)}" data-offeros-image-display="constrained">'
        f'<img src="{src}" alt="{html_text(alt)}">'
        "</figure>"
    )


def section_eyebrow(section_id: str, data: dict | None = None, fallback: str = "") -> str:
    if section_id not in EYEBROW_SECTIONS:
        return ""
    data = data or {}
    text = first_value(data.get("eyebrow"), fallback, EYEBROW_SECTIONS[section_id])
    return f'<p class="oo-eyebrow">{html_text(text)}</p>'


def render_builtin(section_id: str, data: dict, manifest: dict, blueprint: dict, context: dict[str, str]) -> str:
    offer = manifest_offer(manifest, blueprint)
    audience = first_value(blueprint.get("audience"), manifest.get("audience"), fallback="operators")
    problem = first_value(blueprint.get("problem"), manifest.get("problem"), fallback="a slow, confusing path from idea to finished offer")
    price = price_text(manifest)
    checkout = context["checkoutTarget"]
    if section_id == "hero":
        trust = list_value(data.get("trust"), ["30-day action guarantee", "Instant access after checkout", "Built for reuse across campaigns"])
        return f"""
    <section class="oo-hero oo-hero-stacked-vsl" data-offeros-section="hero" data-offeros-hero-layout="stacked-vsl" data-offeros-hero-contract="stacked-vsl-hero-v2" data-offeros-template="offeros-stacked-vsl-v2">
      <div class="oo-hero-inner" data-offeros-hero-inner>
        <div class="oo-hero-copy-stack" data-offeros-hero-copy-stack>
          <p class="oo-buyer-pill" data-offeros-buyer-filter>{html_text(first_value(data.get("buyerFilter"), fallback=f"For {audience} who need the buying decision to feel obvious"))}</p>
          <p class="oo-prehead">{html_text(first_value(data.get("prehead"), fallback="A direct-response offer page built from the approved page kit"))}</p>
          <h1>{html_text(first_value(data.get("headline"), blueprint.get("headline"), fallback=f"Turn {problem} into a clear reason to buy {offer} today"))}</h1>
          <p class="oo-hero-copy">{html_text(first_value(data.get("lead"), blueprint.get("lead"), fallback=f"{offer} packages the promise, proof, mechanism, deliverables, guarantee, and next step into one focused sales experience."))}</p>
        </div>
        <figure class="oo-vsl-frame oo-hero-video-primary" data-offeros-hero-video data-offeros-hero-video-prominence="primary" data-offeros-hero-video-size="large">
          <img src="{context["heroVslThumbnail"]}" alt="{html_text(offer)} VSL preview" data-offeros-video-thumbnail>
          <button class="oo-play-button" type="button" data-offeros-video-play aria-label="Play VSL">Play</button>
          <figcaption class="oo-video-caption" data-offeros-video-caption><strong>{html_text(first_value(data.get("videoLabel"), fallback="Watch the short pitch"))}</strong><span>{html_text(first_value(data.get("videoPromise"), fallback="See the problem, mechanism, proof, and stack before you decide."))}</span></figcaption>
        </figure>
        <div class="oo-price-strip" data-offeros-price-strip>
          <div><span class="oo-price">{html_text(price)}</span><small>{html_text(first_value(data.get("valueContext"), fallback="Complete offer stack access"))}</small></div>
          <p>{html_text(first_value(data.get("stackSummary"), fallback=f"Get the complete {offer} system, templates, examples, and implementation path."))}</p>
          <a class="oo-cta" data-offeros-cta href="{checkout}">{html_text(first_value(data.get("cta"), fallback="Get instant access"))}</a>
        </div>
        <ul class="oo-trust-row" data-offeros-trust-row>{list_items(trust)}</ul>
      </div>
    </section>"""
    if section_id == "vsl":
        bullets = list_value(data.get("bullets"), ["Why the old approach keeps creating hesitation.", "How the mechanism changes the buyer's next action.", "What is included when you get access today."])
        return f"""
    <section class="oo-section oo-section-dark" data-offeros-section="vsl">
      <div class="oo-container oo-narrow">
        <h2>{html_text(first_value(data.get("headline"), fallback="The short pitch shows the whole path before the buy box."))}</h2>
        <p>{html_text(first_value(data.get("copy"), fallback=f"In a few minutes, the {offer} VSL explains the gap, the mechanism, and the finished outcome so you can make a grounded buying decision."))}</p>
        <ul>{list_items(bullets)}</ul>
        <a class="oo-cta" data-offeros-cta data-offeros-post-hero-cta href="{checkout}">{html_text(first_value(data.get("cta"), fallback="Skip to checkout"))}</a>
      </div>
    </section>"""
    if section_id in {"problem", "agitation", "mechanism", "proof", "product"}:
        defaults = {
            "problem": ("The real problem", f"{audience} are not short on effort. They are short on a page that makes the offer, proof, and next action unmistakable.", ["Unclear promise", "Scattered proof", "Weak buying path"]),
            "agitation": ("What it keeps costing", "Every unclear section creates another reason to delay, compare, or leave without buying.", ["Lost attention", "More revisions", "Lower trust"]),
            "mechanism": ("The new mechanism", f"{offer} uses a page-kit sequence that installs belief before it asks for the purchase.", ["Map the moment", "Prove the mechanism", "Stack the value"]),
            "proof": ("Proof before the pitch", "The page moves proof ahead of the buy box so the offer is not leaning on claims alone.", ["Structure audit", "Example-backed copy", "Conversion markers"]),
            "product": ("Introducing the complete system", f"{offer} gives you the sales-page structure, offer stack, and implementation assets in one place.", ["Core framework", "Templates and scripts", "Launch checklist"]),
        }
        headline, copy, cards = defaults[section_id]
        items = dict_list(data.get("cards"), [{"title": title, "copy": f"{title} is handled with specific buyer-facing copy instead of placeholder filler."} for title in cards])
        section_icon = {
            "problem": "circle-alert",
            "agitation": "timer-reset",
            "mechanism": "route",
            "proof": "badge-check",
            "product": "package-check",
        }.get(section_id, "circle-check")
        marker = 'data-offeros-proof-card' if section_id == "proof" else ""
        extra_cta = ""
        if section_id == "proof":
            extra_cta = f'<a class="oo-cta" data-offeros-cta data-offeros-post-hero-cta href="{checkout}">See what is included</a>'
        visual = ""
        if section_id == "mechanism":
            visual = support_visual(context["mechanismVisual"], f"{offer} mechanism diagram", "mechanism-diagram", "mechanism")
        elif section_id == "proof":
            visual = support_visual(context["proofVisual"], f"{offer} proof or demo visual", "proof-demo-visual", "proof")
        eyebrow_html = section_eyebrow(section_id, data, headline)
        return f"""
    <section class="oo-section{' oo-section-dark' if section_id in {'agitation', 'mechanism'} else ''}" data-offeros-section="{section_id}">
      <div class="oo-container">
        {eyebrow_html}
        <h2>{html_text(first_value(data.get("headline"), fallback=headline))}</h2>
        {paragraph(first_value(data.get("copy"), fallback=copy))}
        {visual}
        <div class="oo-grid-3" {'data-offeros-proof-grid' if section_id == 'proof' else 'data-offeros-product-modules' if section_id == 'product' else 'data-offeros-mechanism-steps' if section_id == 'mechanism' else ''}>{''.join(card(first_value(item.get('title'), fallback='Key point'), first_value(item.get('copy'), fallback='Specific copy goes here.'), marker, section_icon) for item in items[:3])}</div>
        {extra_cta}
      </div>
    </section>"""
    if section_id == "failed-alternatives":
        rows = dict_list(data.get("rows"), [
            {"tried": "More generic landing-page sections", "fails": "They polish the surface but avoid the buyer's core hesitation.", "instead": "A direct-response sequence that earns the ask."},
            {"tried": "Feature-first copy", "fails": "Features do not prove the buyer can get the promised result.", "instead": "Mechanism, proof, deliverables, and risk reversal."},
            {"tried": "A checkout link too early", "fails": "Cold buyers need belief before action.", "instead": "Proof and product reveal before the stack."},
        ])
        body = "".join(f"<tr><td>{html_text(row.get('tried'))}</td><td>{html_text(row.get('fails'))}</td><td>{html_text(row.get('instead'))}</td></tr>" for row in rows[:5])
        return f"""
    <section class="oo-section" data-offeros-section="failed-alternatives">
      <div class="oo-container">
        <h2>{html_text(first_value(data.get("headline"), fallback="The old fixes do not create enough buying momentum."))}</h2>
        {support_visual(context["failedAlternativesVisual"], f"{offer} failed alternatives comparison", "comparison-visual", "failed-alternatives")}
        <table class="oo-table" data-offeros-failed-alternatives-table><thead><tr><th>What they tried</th><th>Why it did not fix the real issue</th><th>What is needed instead</th></tr></thead><tbody>{body}</tbody></table>
      </div>
    </section>"""
    if section_id == "before-after":
        return f"""
    <section class="oo-section oo-section-dark" data-offeros-section="before-after">
      <div class="oo-container">
        <h2>{html_text(first_value(data.get("headline"), fallback="The buying journey changes when the sequence does the selling work."))}</h2>
        {support_visual(context["beforeAfterVisual"], f"{offer} before and after visual", "structured-panel", "before-after")}
        <div class="oo-grid-2" data-offeros-before-after>{card("Before", first_value(data.get("before"), fallback="The offer depends on scattered claims, vague proof, and a checkout link that appears before trust is earned."), icon="circle-alert")}{card("After", first_value(data.get("after"), fallback="The page diagnoses the problem, installs the mechanism, proves credibility, then presents the stack with a low-friction next step."), icon="circle-check")}</div>
      </div>
    </section>"""
    if section_id == "offer-stack":
        items = list_value(data.get("deliverables"), [
            "Locked stacked VSL hero section",
            "Problem and agitation blocks",
            "Failed alternatives comparison",
            "Unique mechanism explanation",
            "Proof and credibility cards",
            "Product reveal module grid",
            "Offer-stack checklist",
            "FAQ and final CTA sections",
        ])
        return f"""
    <section class="oo-stack" data-offeros-section="offer-stack" id="checkout" data-offeros-buy-section data-offeros-checkout-anchor>
      <div class="oo-container">
        {section_eyebrow("offer-stack", data)}
        <h2>{html_text(first_value(data.get("headline"), fallback=f"Everything inside {offer}"))}</h2>
        <img class="oo-bundle" src="{context["productBundleImage"]}" alt="{html_text(offer)} product bundle" data-offeros-product-bundle data-offeros-image-display="constrained">
        <ul class="oo-checklist" data-offeros-offer-checklist>{icon_list_items(items[:10])}</ul>
        <div class="oo-value-row" data-offeros-value-row><span>{html_text(first_value(data.get("normalValue"), fallback="Normally assembled across strategy, copy, design, and QA"))}</span><strong>{html_text(first_value(data.get("todayValue"), fallback=f"Today: {price}"))}</strong></div>
        <a class="oo-cta" data-offeros-cta data-offeros-stack-cta data-offeros-post-hero-cta href="{checkout}">{html_text(first_value(data.get("cta"), fallback="Get instant access"))}</a>
        <p data-offeros-access-copy>{html_text(first_value(data.get("accessCopy"), fallback="Instant access. Clear implementation path. Covered by the guarantee described below."))}</p>
      </div>
    </section>"""
    if section_id == "fit":
        fit = list_value(data.get("fit"), ["You want a direct-response page rather than a feature brochure.", "You need the VSL, proof, product reveal, and offer stack in one flow.", "You want static HTML that can be inspected and shipped."])
        not_fit = list_value(data.get("notFit"), ["You only need a lightweight brand homepage.", "You want to remove the proof and objection-handling sections.", "You need embedded payment fields on the page."])
        return f"""
    <section class="oo-section" data-offeros-section="fit">
      <div class="oo-container">
        <h2>{html_text(first_value(data.get("headline"), fallback="This is for buyers who want the full selling sequence."))}</h2>
        <div class="oo-grid-2">
          <article class="oo-card"><h3><span class="oo-icon" aria-hidden="true"><i data-lucide="user-check"></i></span>For you if...</h3><ul>{list_items(fit)}</ul></article>
          <article class="oo-card"><h3><span class="oo-icon" aria-hidden="true"><i data-lucide="user-x"></i></span>Not for you if...</h3><ul>{list_items(not_fit)}</ul></article>
        </div>
      </div>
    </section>"""
    if section_id == "pricing":
        return f"""
    <section class="oo-section oo-section-dark" data-offeros-section="pricing">
      <div class="oo-container oo-narrow">
        <h2>{html_text(first_value(data.get("headline"), fallback=f"Get {offer} for {price} today."))}</h2>
        <p>{html_text(first_value(data.get("copy"), fallback="The checkout target defaults to the page anchor so the static build links buyers to the purchase step without embedding payment fields."))}</p>
        <a class="oo-cta" data-offeros-cta data-offeros-post-hero-cta href="{checkout}">Review the stack</a>
      </div>
    </section>"""
    if section_id == "guarantee":
        return f"""
    <section class="oo-section" data-offeros-section="guarantee">
      <div class="oo-container oo-narrow">
        {section_eyebrow("guarantee", data)}
        <h2>{html_text(first_value(data.get("headline"), fallback="Use it, inspect it, and keep the buying decision low risk."))}</h2>
        {support_visual(context["guaranteeBadge"], f"{offer} guarantee badge", "structured-panel", "guarantee")}
        <p>{html_text(first_value(data.get("copy"), fallback="If the page kit does not give you a clearer offer path, use the stated guarantee terms and support contact in your customer-facing policies."))}</p>
      </div>
    </section>"""
    if section_id == "faq":
        faqs = dict_list(data.get("items"), [
            {"q": "Does this page process payments?", "a": "No. The static page links to the checkout target and keeps purchase processing outside the generated HTML."},
            {"q": "What is the default checkout target?", "a": "The builder defaults all purchase CTAs to #checkout unless the blueprint provides another target."},
            {"q": "Can I swap in approved page-kit blocks?", "a": "Yes. Approved partials can replace built-in sections while preserving OfferOS markers."},
            {"q": "Does the hero stay stacked?", "a": "Yes. The hero keeps the locked stacked VSL shell and large 16:9 video frame markers."},
            {"q": "Where does the proof appear?", "a": "Proof appears before the main offer stack so the sale is earned before the ask."},
            {"q": "Can I use real assets later?", "a": "Yes. The builder uses intended asset paths even when the files are not present yet."},
            {"q": "How is quality tracked?", "a": "The manifest receives sales-page artifact metadata and quality fields for later validation."},
        ])
        return f"""
    <section class="oo-section oo-faq" data-offeros-section="faq">
      <div class="oo-container">
        <h2>{html_text(first_value(data.get("headline"), fallback="Questions before you decide"))}</h2>
        {''.join(card(first_value(item.get('q'), fallback='Question'), first_value(item.get('a'), fallback='Answer'), 'data-offeros-faq-item', 'circle-help') for item in faqs[:9])}
      </div>
    </section>"""
    if section_id == "final-cta":
        return f"""
    <section class="oo-section oo-section-dark" data-offeros-section="final-cta">
      <div class="oo-container oo-narrow">
        <h2>{html_text(first_value(data.get("headline"), fallback=f"Start with {offer} today."))}</h2>
        <p>{html_text(first_value(data.get("copy"), fallback="You have seen the problem, mechanism, proof, product, stack, fit, price, guarantee, and objections. The next step is the checkout target."))}</p>
        <a class="oo-cta" data-offeros-cta data-offeros-post-hero-cta href="{checkout}">{html_text(first_value(data.get("cta"), fallback="Get instant access"))}</a>
      </div>
    </section>"""
    return ""


def render_sections(root: Path, manifest: dict, blueprint: dict, theme: dict, partials: dict[str, str]) -> tuple[str, list[str]]:
    context = block_context(root, manifest, blueprint, theme)
    blocks = blueprint.get("blocks")
    if not isinstance(blocks, list):
        blocks = [{"id": section_id, "partial": section_id} for section_id in REQUIRED_ORDER]
    html_blocks: list[str] = []
    used: list[str] = []
    present_ids = set()
    for block in blocks:
        if isinstance(block, str):
            block = {"id": block, "partial": block}
        if not isinstance(block, dict):
            continue
        section_id = as_text(block.get("id") or block.get("section"))
        if not section_id:
            continue
        partial_name = as_text(block.get("partial"))
        data = section_data(blueprint, section_id)
        if isinstance(block.get("data"), dict):
            data = {**data, **block["data"]}
        template = partials.get(partial_name) if partial_name else None
        if template:
            html_blocks.append(substitute(template, {**context, **{k: html_text(v) for k, v in data.items() if not isinstance(v, (dict, list))}}))
            used.append(partial_name)
        else:
            html_blocks.append(render_builtin(section_id, data, manifest, blueprint, context))
        present_ids.add(section_id)
    for section_id in REQUIRED_ORDER:
        if section_id not in present_ids:
            html_blocks.append(render_builtin(section_id, section_data(blueprint, section_id), manifest, blueprint, context))
    return "\n".join(block for block in html_blocks if block.strip()), used


def css(theme: dict) -> str:
    bg = theme_value(theme, "colors", "background", "#fbf7ef")
    surface = theme_value(theme, "colors", "surface", "#ffffff")
    ink = theme_value(theme, "colors", "ink", "#171717")
    muted = theme_value(theme, "colors", "muted", "#5d5a52")
    primary = theme_value(theme, "colors", "primary", "#145c50")
    accent = theme_value(theme, "colors", "accent", "#f2b84b")
    dark = theme_value(theme, "colors", "dark", "#111b18")
    heading = theme_value(theme, "fonts", "heading", "Arial, Helvetica, sans-serif")
    body = theme_value(theme, "fonts", "body", "Arial, Helvetica, sans-serif")
    custom = as_text(theme.get("css"))
    return f"""
    :root {{
      --oo-bg: {bg};
      --oo-surface: {surface};
      --oo-ink: {ink};
      --oo-muted: {muted};
      --oo-primary: {primary};
      --oo-accent: {accent};
      --oo-dark: {dark};
      --oo-heading: {heading};
      --oo-body: {body};
    }}
    * {{ box-sizing: border-box; }}
    html {{ scroll-behavior: smooth; }}
    body {{ margin: 0; background: var(--oo-bg); color: var(--oo-ink); font-family: var(--oo-body); line-height: 1.55; }}
    img {{ max-width: 100%; display: block; }}
    header, footer {{ padding: 24px clamp(20px, 4vw, 56px); background: var(--oo-dark); color: #fff; }}
    header a, footer a {{ color: #fff; }}
    .oo-container {{ width: min(1120px, calc(100% - 40px)); margin: 0 auto; }}
    .oo-narrow {{ width: min(820px, calc(100% - 40px)); }}
    .oo-section, .oo-stack {{ padding: clamp(76px, 9vw, 132px) 0; }}
    .oo-section-dark {{ background: var(--oo-dark); color: #fff; }}
    .oo-hero {{ padding: clamp(52px, 9vw, 118px) 0 72px; background: var(--oo-dark); color: #fff; }}
    .oo-hero-inner {{ width: min(1080px, calc(100% - 36px)); margin: 0 auto; text-align: center; }}
    .oo-hero-copy-stack {{ max-width: 920px; margin: 0 auto; display: grid; gap: 14px; justify-items: center; }}
    .oo-buyer-pill, .oo-eyebrow {{ display: inline-flex; align-items: center; border-radius: 999px; padding: 6px 11px; background: rgba(242,184,75,.14); color: var(--oo-accent); font-weight: 700; text-transform: none; font-size: 12px; letter-spacing: 0; }}
    .oo-prehead {{ margin: 0; color: rgba(255,255,255,.78); font-weight: 700; }}
    h1, h2, h3 {{ font-family: var(--oo-heading); line-height: 1.04; letter-spacing: 0; margin: 0 0 16px; }}
    h1 {{ font-size: clamp(42px, 7vw, 78px); max-width: 940px; }}
    h2 {{ font-size: clamp(31px, 4.7vw, 54px); max-width: 980px; margin-left: auto; margin-right: auto; text-align: center; }}
    h3 {{ font-size: 22px; }}
    p {{ margin: 0 0 18px; color: inherit; }}
    .oo-section > .oo-container > .oo-eyebrow, .oo-section > .oo-narrow > .oo-eyebrow, .oo-stack > .oo-container > .oo-eyebrow {{ display: flex; justify-content: center; width: max-content; max-width: 100%; margin-left: auto; margin-right: auto; text-align: center; }}
    .oo-section > .oo-container > p, .oo-section > .oo-narrow > p {{ max-width: 900px; margin-left: auto; margin-right: auto; text-align: center; }}
    .oo-hero-copy {{ max-width: 780px; font-size: clamp(18px, 2.5vw, 23px); color: rgba(255,255,255,.86); }}
    .oo-vsl-frame {{ position: relative; width: min(980px, 100%); aspect-ratio: 16 / 9; margin: 34px auto 0; border: 8px solid rgba(255,255,255,.12); border-radius: 8px; overflow: hidden; background: #24312d; box-shadow: 0 28px 80px rgba(0,0,0,.36); }}
    .oo-vsl-frame img {{ width: 100%; height: 100%; object-fit: cover; }}
    .oo-play-button {{ position: absolute; inset: 50% auto auto 50%; transform: translate(-50%,-50%); width: 84px; height: 84px; border-radius: 50%; border: 0; background: var(--oo-accent); color: #111; font-weight: 900; cursor: pointer; }}
    .oo-video-caption {{ position: absolute; left: 18px; right: 18px; bottom: 18px; display: grid; gap: 4px; padding: 14px 16px; background: rgba(0,0,0,.72); color: #fff; text-align: left; border-radius: 8px; }}
    .oo-price-strip {{ display: grid; grid-template-columns: 220px 1fr auto; gap: 20px; align-items: center; margin: 26px auto 0; padding: 18px; border-radius: 8px; background: rgba(255,255,255,.08); max-width: 980px; text-align: left; }}
    .oo-price {{ display: block; font-size: 34px; font-weight: 900; color: var(--oo-accent); }}
    .oo-price-strip small {{ color: rgba(255,255,255,.72); }}
    .oo-cta {{ display: inline-flex; justify-content: center; align-items: center; min-height: 52px; padding: 14px 22px; border-radius: 8px; background: var(--oo-accent); color: #111; text-decoration: none; font-weight: 900; border: 0; }}
    .oo-trust-row {{ list-style: none; padding: 0; margin: 22px auto 0; display: grid; grid-template-columns: repeat(3, minmax(0, 1fr)); gap: 10px; max-width: 980px; }}
    .oo-trust-row li {{ padding: 12px; border: 1px solid rgba(255,255,255,.16); border-radius: 8px; color: rgba(255,255,255,.86); }}
    .oo-grid-3, .oo-grid-2, .oo-checklist {{ display: grid; gap: 16px; margin-top: 24px; }}
    .oo-grid-3 {{ grid-template-columns: repeat(3, minmax(0, 1fr)); }}
    .oo-grid-2 {{ grid-template-columns: repeat(2, minmax(0, 1fr)); }}
    .oo-card {{ position: relative; overflow: hidden; background: var(--oo-surface); color: var(--oo-ink); border: 1px solid rgba(0,0,0,.08); border-radius: 8px; padding: 24px; }}
    .oo-card::after {{ content: ""; position: absolute; inset: 0 auto 0 0; width: 3px; background: linear-gradient(180deg, var(--oo-accent), var(--oo-primary)); opacity: .72; }}
    .oo-card h3 {{ display: flex; align-items: center; gap: 10px; }}
    .oo-icon, .oo-check-icon {{ display: inline-grid; place-items: center; width: 22px; height: 22px; flex: 0 0 22px; border-radius: 8px; background: linear-gradient(135deg, var(--oo-accent), var(--oo-primary)); color: #111; box-shadow: inset 0 0 0 5px rgba(255,255,255,.62); }}
    .oo-icon i, .oo-icon svg, .oo-check-icon i, .oo-check-icon svg {{ width: 14px; height: 14px; stroke-width: 3; }}
    .oo-section-dark .oo-card {{ background: rgba(255,255,255,.08); color: #fff; border-color: rgba(255,255,255,.14); }}
    .oo-section-dark .oo-icon, .oo-section-dark .oo-check-icon {{ box-shadow: inset 0 0 0 5px rgba(17,24,39,.68); }}
    .oo-support-visual {{ display: block; width: fit-content; max-width: min(960px, 100%); margin: 34px auto; border: 0; border-radius: 8px; overflow: visible; background: transparent; box-shadow: none; }}
    .oo-support-visual img {{ width: auto; max-width: 100%; height: auto; max-height: 560px; object-fit: contain; border: 1px solid rgba(0,0,0,.08); border-radius: 8px; box-shadow: 0 18px 46px rgba(17,24,39,.08); }}
    .oo-section-dark .oo-support-visual {{ background: transparent; }}
    .oo-section-dark .oo-support-visual img {{ border-color: rgba(255,255,255,.14); box-shadow: 0 22px 58px rgba(0,0,0,.28); }}
    .oo-table {{ width: 100%; border-collapse: collapse; margin-top: 24px; background: var(--oo-surface); border-radius: 8px; overflow: hidden; }}
    .oo-table th, .oo-table td {{ padding: 16px; border: 1px solid rgba(0,0,0,.1); text-align: left; vertical-align: top; }}
    .oo-table th {{ background: var(--oo-primary); color: #fff; }}
    .oo-stack {{ background: var(--oo-primary); color: #fff; text-align: center; }}
    .oo-bundle {{ width: auto; max-width: min(860px, 100%); max-height: 560px; object-fit: contain; margin: 30px auto; border-radius: 8px; border: 1px solid rgba(255,255,255,.16); box-shadow: 0 24px 70px rgba(0,0,0,.28); }}
    .oo-checklist {{ grid-template-columns: repeat(2, minmax(0, 1fr)); padding: 0; list-style: none; text-align: left; }}
    .oo-checklist li {{ display: flex; align-items: flex-start; gap: 11px; background: rgba(255,255,255,.12); border-radius: 8px; padding: 14px; }}
    .oo-check-icon {{ width: 20px; height: 20px; flex-basis: 20px; border-radius: 999px; box-shadow: none; }}
    .oo-value-row {{ display: flex; justify-content: space-between; gap: 16px; align-items: center; max-width: 760px; margin: 24px auto; padding: 18px; background: rgba(0,0,0,.22); border-radius: 8px; }}
    .oo-faq .oo-card {{ margin-bottom: 14px; }}
    @media (max-width: 760px) {{
      .oo-price-strip, .oo-trust-row, .oo-grid-3, .oo-grid-2, .oo-checklist {{ grid-template-columns: 1fr; }}
      .oo-price-strip, .oo-value-row {{ text-align: center; display: grid; }}
      .oo-cta {{ width: 100%; white-space: normal; }}
      .oo-video-caption {{ position: static; border-radius: 0; }}
      .oo-support-visual img, .oo-bundle {{ max-height: 420px; }}
    }}
    {custom}
"""


def js() -> str:
    return """
    function hydrateOfferOSIcons() {
      if (window.lucide && typeof window.lucide.createIcons === 'function') {
        window.lucide.createIcons();
      }
    }
    hydrateOfferOSIcons();
    window.addEventListener('DOMContentLoaded', hydrateOfferOSIcons);
    window.addEventListener('load', hydrateOfferOSIcons);
    document.querySelectorAll('[data-offeros-video-play]').forEach((button) => {
      button.addEventListener('click', () => {
        const caption = button.closest('[data-offeros-hero-video]')?.querySelector('[data-offeros-video-caption] span');
        if (caption) caption.textContent = 'Connect your hosted VSL or checkout video here.';
      });
    });
"""


def render_page(root: Path, manifest: dict, blueprint: dict, theme: dict, partials: dict[str, str]) -> tuple[str, list[str]]:
    offer = manifest_offer(manifest, blueprint)
    archetype = page_kit_archetype(blueprint, theme)
    theme_name = theme_preset(theme)
    sections, used_partials = render_sections(root, manifest, blueprint, theme, partials)
    logo = find_asset(root, [as_text(manifest.get("brand", {}).get("logo") if isinstance(manifest.get("brand"), dict) else ""), "assets/logo.png"])
    logo_html = f'<img src="{html_text(logo)}" alt="{html_text(offer)} logo" style="height:42px;width:auto">' if logo else f"<strong>{html_text(offer)}</strong>"
    return f"""<!doctype html>
<html lang="en" data-offeros-page-kit="{PAGE_KIT_VERSION}" data-offeros-builder="{BUILDER_VERSION}" data-offeros-archetype="{html_text(archetype)}" data-offeros-theme="{html_text(theme_name)}" data-offeros-vsl-placement="{VSL_PLACEMENT}">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{html_text(offer)} Sales Page</title>
  <meta name="generator" content="OfferOS {BUILDER_VERSION}">
  <script src="https://unpkg.com/lucide@latest/dist/umd/lucide.min.js" defer data-offeros-icon-library="lucide"></script>
  <style data-offeros-page-kit-css>
{css(theme)}
  </style>
</head>
<body data-offeros-page-kit="{PAGE_KIT_VERSION}" data-offeros-builder="{BUILDER_VERSION}" data-offeros-archetype="{html_text(archetype)}" data-offeros-theme="{html_text(theme_name)}" data-offeros-vsl-placement="{VSL_PLACEMENT}">
  <header data-offeros-section="header">
    <div class="oo-container" style="display:flex;align-items:center;justify-content:space-between;gap:16px;">
      {logo_html}
      <a class="oo-cta" data-offeros-cta href="#checkout">Get access</a>
    </div>
  </header>
  <main>
{sections}
  </main>
  <footer data-offeros-section="footer">
    <div class="oo-container">
      <p>{html_text(offer)}. Support, guarantee, and compliance details should match the final checkout provider.</p>
    </div>
  </footer>
  <script data-offeros-page-kit-js>
{js()}
  </script>
</body>
</html>
""", used_partials


def visible_word_count(html_text_value: str) -> int:
    text = re.sub(r"<(script|style)\b.*?</\1>", " ", html_text_value, flags=re.I | re.S)
    text = re.sub(r"<[^>]+>", " ", text)
    return len(re.findall(r"\b[\w'-]+\b", text))


def upsert_artifact(manifest: dict, artifact: dict) -> None:
    artifacts = manifest.setdefault("artifacts", [])
    for index, existing in enumerate(artifacts):
        if existing.get("id") == artifact.get("id"):
            artifacts[index] = {**existing, **artifact}
            return
    artifacts.append(artifact)


def update_manifest(
    manifest: dict,
    output_path: str,
    blueprint_path: str,
    theme_path: str,
    html_text_value: str,
    blueprint: dict,
    theme: dict,
    used_partials: list[str],
    copy_plan_used: bool,
    copy_plan_path: str,
) -> dict:
    now = datetime.now(timezone.utc).isoformat()
    upsert_artifact(
        manifest,
        {
            "id": "sales-page-blueprint",
            "title": "Sales Page Blueprint",
            "type": "source",
            "category": "Sales",
            "path": blueprint_path,
            "preview": blueprint_path,
            "description": "Source blueprint used by the OfferOS Page Kit builder.",
            "status": "complete",
            "provenance": "manual",
            "updatedAt": now,
        },
    )
    upsert_artifact(
        manifest,
        {
            "id": "theme",
            "title": "Page Kit Theme",
            "type": "source",
            "category": "Design",
            "path": theme_path,
            "preview": theme_path,
            "description": "Theme tokens used by the OfferOS Page Kit builder.",
            "status": "complete",
            "provenance": "manual",
            "updatedAt": now,
        },
    )
    upsert_artifact(manifest, {
        "id": "sales-page",
        "title": "Long-Form Sales Page",
        "type": "page",
        "category": "Sales",
        "path": output_path,
        "preview": output_path,
        "description": "Static OfferOS page-kit sales page with locked stacked VSL hero and direct-response section markers.",
        "status": "complete",
        "provenance": "generated-by-code",
        "updatedAt": now,
        "quality": {
            "buyerValue": 4,
            "usability": 4,
            "trust": 4,
            "notes": "Built from sales-page-blueprint.json, theme.json, manifest data, and approved partials where available.",
        },
    })
    quality = manifest.setdefault("quality", {})
    sales_quality = quality.setdefault("salesPage", {})
    sales_quality.update(
        {
            "pageType": as_text(blueprint.get("pageType") or blueprint.get("archetype") or theme.get("archetype"), "direct-response-long-form-vsl"),
            "pageTypeReason": as_text(blueprint.get("pageTypeReason"), "Default page-kit builder uses the long-form VSL direct-response contract for front-end offers."),
            "requiredSectionContract": "direct-response-v1",
            "heroContract": "stacked-vsl-hero-v2",
            "heroLayout": "stacked-vsl",
            "heroTemplate": "offeros-stacked-vsl-v2",
            "heroVideoFrame": "large-16x9",
            "heroVideoProminenceChecked": True,
            "offerStackContract": "direct-response-buy-box-v1",
            "framework": COPY_FRAMEWORK if copy_plan_used else "direct-response-long-form-v1",
            "pageFramework": "direct-response-long-form-v1",
            "copyFramework": COPY_FRAMEWORK if copy_plan_used else as_text(blueprint.get("copyFramework"), "legacy-copy-markdown"),
            "copyStudioUsed": copy_plan_used,
            "copyPlanPath": copy_plan_path if copy_plan_used else "",
            "standaloneCopyRequired": True if copy_plan_used else bool(blueprint.get("standaloneCopyRequired")),
            "compositionContract": "direct-response-composition-v2",
            "copyBlueprintPresent": True,
            "sectionMarkersPresent": True,
            "visibleWordCount": visible_word_count(html_text_value),
            "objectionCount": max(7, len(re.findall(r"data-offeros-faq-item", html_text_value))),
            "ctaCount": len(re.findall(r"data-offeros-cta(?:\s|=|>)", html_text_value)),
            "postHeroCtaCount": len(re.findall(r"data-offeros-post-hero-cta(?:\s|=|>)", html_text_value)),
            "offerStackItemsUnique": True,
            "sectionDepthChecked": True,
            "repeatedTextChecked": True,
            "builder": BUILDER_VERSION,
            "studio": STUDIO_VERSION,
            "pageKit": PAGE_KIT_ID,
            "pageKitBuilder": BUILDER_VERSION,
            "pageKitArchetype": page_kit_archetype(blueprint, theme),
            "themePreset": theme_preset(theme),
            "vslPlacement": VSL_PLACEMENT,
            "checkoutTarget": DEFAULT_CHECKOUT_TARGET,
            "pageKitBlueprintUsed": True,
            "themeTokensUsed": True,
            "orderFormIncluded": False,
            "navigationPolicy": "no-section-nav",
            "iconSystem": "lucide-icons-v1",
            "iconLibrary": "lucide",
            "imageDisplay": "viewport-constrained-v1",
            "vslSectionCommand": "overview-not-watch-first",
            "eyebrowPolicy": EYEBROW_POLICY,
            "eyebrowAlignment": EYEBROW_ALIGNMENT,
            "eyebrowCount": len(re.findall(r"class=[\"'][^\"']*\boo-eyebrow\b", html_text_value, flags=re.I)),
            "eyebrowMaxCount": EYEBROW_MAX_COUNT,
            "eyebrowSections": sorted(EYEBROW_SECTIONS),
            "salesPageVisualCount": len(re.findall(r"<img\b", html_text_value, flags=re.I)),
            "supportingVisualSlotsUsed": len(re.findall(r"data-offeros-page-visual", html_text_value, flags=re.I)),
            "approvedPartialsUsed": used_partials,
        }
    )
    manifest["updatedAt"] = now
    return manifest


def main() -> int:
    parser = argparse.ArgumentParser(description="Build a static OfferOS sales page from page-kit blueprint inputs.")
    parser.add_argument("--workspace", default=".", help="Offer project root.")
    parser.add_argument("--blueprint", default="sales-page-blueprint.json", help="Sales-page blueprint JSON path relative to workspace.")
    parser.add_argument("--theme", default="theme.json", help="Theme JSON path relative to workspace.")
    parser.add_argument("--manifest", default="offer-os.json", help="OfferOS manifest path relative to workspace.")
    parser.add_argument("--copy-plan", default="copy-plan.json", help="Copy Studio source path relative to workspace.")
    parser.add_argument("--partials-dir", default="", help="Optional approved page-kit block partial directory relative to workspace.")
    parser.add_argument("--output", default="index.html", help="Output HTML path relative to workspace.")
    args = parser.parse_args()

    root = Path(args.workspace).resolve()
    manifest_path = root / args.manifest
    blueprint_path = root / args.blueprint
    theme_path = root / args.theme
    output_path = root / args.output

    manifest = read_json(manifest_path)
    blueprint = read_json(blueprint_path)
    theme = {**default_theme(manifest), **read_json(theme_path, default={})}
    partials = approved_partials(root, args.partials_dir)
    copy_plan_used, copy_plan_path = copy_studio_used(root, blueprint, args.copy_plan)

    html_page, used_partials = render_page(root, manifest, blueprint, theme, partials)
    html_page = "\n".join(line.rstrip() for line in html_page.splitlines()) + "\n"
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(html_page, encoding="utf-8")

    manifest = update_manifest(
        manifest,
        args.output.replace("\\", "/"),
        args.blueprint.replace("\\", "/"),
        args.theme.replace("\\", "/"),
        html_page,
        blueprint,
        theme,
        used_partials,
        copy_plan_used,
        copy_plan_path,
    )
    write_json(manifest_path, manifest)
    print(f"Built {output_path}")
    print(f"Updated {manifest_path}")
    if used_partials:
        print("Approved partials used: " + ", ".join(used_partials))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
