import argparse
from datetime import datetime, timezone
import json
from pathlib import Path
import re


STUDIO_VERSION = "copy-studio-v1"
COPY_FRAMEWORK = "modern-brunson-long-form-v1"
PAGE_FRAMEWORK = "direct-response-long-form-v1"
COMPOSITION_CONTRACT = "direct-response-composition-v2"
PAGE_TYPE = "direct-response-long-form-vsl"
DEFAULT_CHECKOUT_TARGET = "#checkout"
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
REQUIRED_TOP_LEVEL = [
    "schema",
    "framework",
    "standaloneCopyRequired",
    "vslDependency",
    "offerName",
    "price",
    "audience",
    "awarenessLevel",
    "marketSophistication",
    "corePromise",
    "primaryPain",
    "failedAlternatives",
    "newInsight",
    "uniqueMechanism",
    "proofPlan",
    "productReveal",
    "offerStack",
    "bonuses",
    "valueLogic",
    "guarantee",
    "objectionMatrix",
    "urgencyBasis",
    "sectionPlan",
]
REQUIRED_SECTION_FIELDS = [
    "sectionId",
    "frameworkRole",
    "conversionJob",
    "buyerBeliefBefore",
    "buyerBeliefAfter",
    "primaryClaim",
    "proofOrSupport",
    "copyBlocks",
    "visualNeed",
    "ctaRole",
    "maxWords",
]
PAGE_SECTION_ORDER = [
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
COPY_SPINE_SECTIONS = [
    "hero",
    "vsl",
    "problem",
    "agitation",
    "failed-alternatives",
    "new-insight",
    "mechanism",
    "proof",
    "before-after",
    "product",
    "feature-benefit",
    "how-it-works",
    "offer-stack",
    "bonuses",
    "pricing",
    "guarantee",
    "fit",
    "faq",
    "final-cta",
]
GENERIC_OBJECTIONS = {
    "what is this",
    "how does it work",
    "is it for me",
    "will this work",
    "what do i get",
    "how much is it",
    "can i get a refund",
}
VALID_URGENCY_TYPES = {"none", "launch-window", "cohort-start", "expiring-bonus", "price-change", "user-provided"}
COPY_BLOCK_WORD_MINIMUM = 1800
SALES_COPY_WORD_MINIMUM = 2500
SALES_COPY_TARGET_MINIMUM = 3500
SALES_COPY_TARGET_MAXIMUM = 5500
COPY_SECTION_REQUIREMENTS = {
    "hero": {"minWords": 110, "requiredTypes": {"headline", "lead", "cta"}},
    "vsl": {"minWords": 70, "requiredTypes": {"headline", "paragraph"}},
    "problem": {"minWords": 170, "requiredTypes": {"headline", "paragraph"}},
    "agitation": {"minWords": 130, "requiredTypes": {"headline", "paragraph"}},
    "failed-alternatives": {"minWords": 130, "requiredTypes": {"headline", "paragraph"}},
    "new-insight": {"minWords": 120, "requiredTypes": {"headline", "paragraph"}},
    "mechanism": {"minWords": 170, "requiredTypes": {"headline", "paragraph"}},
    "proof": {"minWords": 120, "requiredTypes": {"headline", "paragraph"}},
    "before-after": {"minWords": 90, "requiredTypes": {"headline", "paragraph"}},
    "product": {"minWords": 170, "requiredTypes": {"headline", "paragraph"}},
    "feature-benefit": {"minWords": 120, "requiredTypes": {"headline", "paragraph"}},
    "how-it-works": {"minWords": 110, "requiredTypes": {"headline", "paragraph"}},
    "offer-stack": {"minWords": 160, "requiredTypes": {"headline", "paragraph", "cta"}},
    "bonuses": {"minWords": 60, "requiredTypes": {"headline", "paragraph"}},
    "pricing": {"minWords": 80, "requiredTypes": {"headline", "paragraph"}},
    "guarantee": {"minWords": 80, "requiredTypes": {"headline", "paragraph"}},
    "fit": {"minWords": 80, "requiredTypes": {"headline", "paragraph"}},
    "faq": {"minWords": 80, "requiredTypes": {"headline", "paragraph"}},
    "final-cta": {"minWords": 90, "requiredTypes": {"headline", "paragraph", "cta"}},
}
SALES_COPY_SECTION_MIN_WORDS = {
    "problem": 170,
    "agitation": 130,
    "failed-alternatives": 180,
    "new-insight": 140,
    "mechanism": 220,
    "proof": 160,
    "product": 230,
    "feature-benefit": 260,
    "how-it-works": 180,
    "offer-stack": 260,
    "pricing": 120,
    "guarantee": 100,
    "faq": 420,
    "final-cta": 110,
}
FORBIDDEN_META_COPY_PHRASES = [
    "this section explains",
    "this section should",
    "the buyer can see",
    "makes this point",
    "this page explains",
    "the page should",
    "framework role",
    "conversion job",
    "belief shift",
    "buyer belief",
    "proof/support",
    "visual need",
    "copy anchor",
    "cta role",
    "write a headline",
    "include a paragraph",
    "use this section",
]
VSL_DEPENDENCY_PHRASES = [
    "watch the video to understand",
    "the video explains the mechanism",
    "the video explains the offer",
    "the vsl explains the mechanism",
    "the vsl explains the offer",
    "before you can understand the offer",
]


def read_json(path: Path, default=None):
    if path.exists():
        return json.loads(path.read_text(encoding="utf-8-sig"))
    if default is not None:
        return default
    raise SystemExit(f"Required JSON file not found: {path}")


def write_json(path: Path, payload: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")


def as_text(value, fallback: str = "") -> str:
    if value is None:
        return fallback
    if isinstance(value, (list, tuple)):
        return ", ".join(as_text(item) for item in value if as_text(item)) or fallback
    return str(value).strip() or fallback


def slugify(value: str) -> str:
    value = value.lower().strip()
    value = re.sub(r"[^a-z0-9]+", "-", value)
    return value.strip("-") or "offer"


def list_of_dicts(value) -> list[dict]:
    return [item for item in value if isinstance(item, dict)] if isinstance(value, list) else []


def section_rows(plan: dict) -> list[dict]:
    return list_of_dicts(plan.get("sectionPlan"))


def section_by_id(plan: dict) -> dict[str, dict]:
    return {as_text(row.get("sectionId")): row for row in section_rows(plan)}


def block_text(row: dict, *types: str, fallback: str = "") -> str:
    for block in list_of_dicts(row.get("copyBlocks")):
        if as_text(block.get("type")) in types:
            text = as_text(block.get("text"))
            if text:
                return text
    return fallback


def block_list(row: dict, *types: str) -> list[str]:
    values = []
    for block in list_of_dicts(row.get("copyBlocks")):
        if as_text(block.get("type")) in types:
            text = as_text(block.get("text"))
            if text:
                values.append(text)
    return values


def value_item_title(item: dict, fallback: str = "Item") -> str:
    return as_text(item.get("title") or item.get("feature") or item.get("name"), fallback)


def value_item_copy(item: dict, fallback: str = "") -> str:
    return as_text(
        item.get("copy")
        or item.get("plainBullet")
        or item.get("benefit")
        or item.get("answer")
        or item.get("whyItFails")
        or fallback
    )


def word_count(text: str) -> int:
    return len(re.findall(r"\b[\w'-]+\b", text or ""))


def copy_block_texts(row: dict) -> list[str]:
    return [as_text(block.get("text")) for block in list_of_dicts(row.get("copyBlocks")) if as_text(block.get("text"))]


def copy_block_types(row: dict) -> set[str]:
    return {as_text(block.get("type")) for block in list_of_dicts(row.get("copyBlocks")) if as_text(block.get("type"))}


def row_copy_word_count(row: dict) -> int:
    return word_count(" ".join(copy_block_texts(row)))


def normalize_for_repetition(text: str) -> str:
    return re.sub(r"\s+", " ", re.sub(r"[^a-z0-9' -]+", "", text.lower())).strip()


def repeated_sentence_findings(text: str, minimum_words: int = 8, max_repeats: int = 2) -> list[str]:
    counts: dict[str, int] = {}
    originals: dict[str, str] = {}
    for sentence in re.split(r"(?<=[.!?])\s+", text or ""):
        normalized = normalize_for_repetition(sentence)
        if word_count(normalized) < minimum_words:
            continue
        if normalized.startswith("cta "):
            continue
        counts[normalized] = counts.get(normalized, 0) + 1
        originals.setdefault(normalized, sentence.strip())
    return [f"'{originals[key][:90]}' repeated {count} times" for key, count in counts.items() if count > max_repeats]


def repeated_paragraph_findings(text: str, minimum_words: int = 20) -> list[str]:
    counts: dict[str, int] = {}
    originals: dict[str, str] = {}
    for paragraph in re.split(r"\n\s*\n", text or ""):
        normalized = normalize_for_repetition(paragraph)
        if word_count(normalized) < minimum_words:
            continue
        counts[normalized] = counts.get(normalized, 0) + 1
        originals.setdefault(normalized, paragraph.strip())
    return [f"'{originals[key][:90]}' repeated {count} times" for key, count in counts.items() if count > 1]


def forbidden_meta_copy_hits(text: str) -> list[str]:
    lower = (text or "").lower()
    return [phrase for phrase in FORBIDDEN_META_COPY_PHRASES if phrase in lower]


def vsl_dependency_hits(text: str) -> list[str]:
    lower = (text or "").lower()
    return [phrase for phrase in VSL_DEPENDENCY_PHRASES if phrase in lower]


def h2_markdown_section(text: str, heading: str) -> str:
    pattern = rf"(?ims)^\s*##\s+{re.escape(heading)}\s*$([\s\S]*?)(?=^\s*##\s+|\Z)"
    match = re.search(pattern, text or "")
    return match.group(1) if match else ""


def copy_block_quality_issues(plan: dict) -> list[str]:
    issues: list[str] = []
    total_words = 0
    for row in section_rows(plan):
        section_id = as_text(row.get("sectionId"))
        texts = copy_block_texts(row)
        section_text = "\n".join(texts)
        total_words += word_count(section_text)
        requirement = COPY_SECTION_REQUIREMENTS.get(section_id)
        if not requirement:
            continue
        section_words = word_count(section_text)
        if section_words < requirement["minWords"]:
            issues.append(
                f"sectionPlan[{section_id}].copyBlocks are too thin: {section_words} words found, "
                f"{requirement['minWords']}+ required."
            )
        missing_types = sorted(requirement["requiredTypes"] - copy_block_types(row))
        if missing_types:
            issues.append(f"sectionPlan[{section_id}].copyBlocks missing required block types: {', '.join(missing_types)}.")
        if forbidden_meta_copy_hits(section_text):
            issues.append(
                f"sectionPlan[{section_id}].copyBlocks contain internal/meta copy: "
                + ", ".join(forbidden_meta_copy_hits(section_text)[:4])
            )
        repeated = repeated_sentence_findings(section_text, max_repeats=1)
        if repeated:
            issues.append(f"sectionPlan[{section_id}].copyBlocks repeat boilerplate sentences: " + "; ".join(repeated[:2]))
    if total_words < COPY_BLOCK_WORD_MINIMUM:
        issues.append(
            f"copy-plan.json copyBlocks contain only {total_words} buyer-facing words; "
            f"{COPY_BLOCK_WORD_MINIMUM}+ required before rendering copy.md."
        )
    return issues


def sales_copy_markdown_quality_issues(plan: dict, copy_markdown: str) -> list[str]:
    issues: list[str] = []
    total_words = word_count(copy_markdown)
    if total_words < SALES_COPY_WORD_MINIMUM:
        issues.append(f"copy.md is too thin for long-form sales copy: {total_words} words found, {SALES_COPY_WORD_MINIMUM}+ required.")
    forbidden_hits = forbidden_meta_copy_hits(copy_markdown)
    if forbidden_hits:
        issues.append("copy.md contains internal/meta copy: " + ", ".join(forbidden_hits[:6]))
    vsl_hits = vsl_dependency_hits(copy_markdown)
    if vsl_hits:
        issues.append("copy.md depends on the VSL instead of standing alone: " + ", ".join(vsl_hits[:4]))
    repeated_sentences = repeated_sentence_findings(copy_markdown)
    if repeated_sentences:
        issues.append("copy.md repeats boilerplate sentences: " + "; ".join(repeated_sentences[:4]))
    repeated_paragraphs = repeated_paragraph_findings(copy_markdown)
    if repeated_paragraphs:
        issues.append("copy.md repeats full paragraphs: " + "; ".join(repeated_paragraphs[:3]))
    for section_id, minimum in SALES_COPY_SECTION_MIN_WORDS.items():
        heading = section_title(section_id)
        section = h2_markdown_section(copy_markdown, heading)
        section_words = word_count(section)
        if section_words < minimum:
            issues.append(f"copy.md section '{heading}' is too thin: {section_words} words found, {minimum}+ required.")
    faq_section = h2_markdown_section(copy_markdown, section_title("faq"))
    faq_items = len(re.findall(r"(?im)^\s*###\s+", faq_section))
    if faq_items < 7:
        issues.append(f"copy.md FAQ must include 7+ specific objection questions: {faq_items} found.")
    if plan.get("standaloneCopyRequired") is True:
        required_terms = [
            as_text(plan.get("uniqueMechanism", {}).get("name")),
            as_text(plan.get("productReveal", {}).get("productType")),
            as_text(plan.get("guarantee", {}).get("name")),
            as_text(plan.get("valueLogic", {}).get("todayPrice") or plan.get("price")),
        ]
        lower = copy_markdown.lower()
        missing = [term for term in required_terms if term and term.lower() not in lower]
        if missing:
            issues.append("copy.md is not self-contained; it misses core offer terms: " + ", ".join(missing[:4]))
    return issues


def validate_copy_plan(plan: dict) -> list[str]:
    issues: list[str] = []
    missing = [key for key in REQUIRED_TOP_LEVEL if key not in plan]
    if missing:
        issues.append("copy-plan.json missing required fields: " + ", ".join(missing))
    if plan.get("schema") != "offeros/copy-plan/v1":
        issues.append('copy-plan.json must record schema: "offeros/copy-plan/v1".')
    if plan.get("framework") != COPY_FRAMEWORK:
        issues.append(f'copy-plan.json must record framework: "{COPY_FRAMEWORK}".')
    if plan.get("standaloneCopyRequired") is not True:
        issues.append("copy-plan.json must set standaloneCopyRequired: true.")
    if plan.get("vslDependency") != "optional-supporting-asset":
        issues.append('copy-plan.json must set vslDependency: "optional-supporting-asset".')
    if len(as_text(plan.get("price"))) < 1:
        issues.append("copy-plan.json field price is missing.")
    for key in ["offerName", "audience", "corePromise", "primaryPain", "newInsight"]:
        if len(as_text(plan.get(key))) < 8:
            issues.append(f"copy-plan.json field {key} is missing or too thin.")

    failed = list_of_dicts(plan.get("failedAlternatives"))
    if len(failed) < 3:
        issues.append("copy-plan.json must include 3+ failedAlternatives.")
    for index, item in enumerate(failed, start=1):
        for key in ["name", "whyItFails", "whatIsNeededInstead"]:
            if len(as_text(item.get(key))) < 6:
                issues.append(f"failedAlternatives[{index}] missing {key}.")

    mechanism = plan.get("uniqueMechanism") if isinstance(plan.get("uniqueMechanism"), dict) else {}
    if len(as_text(mechanism.get("name"))) < 3:
        issues.append("uniqueMechanism must include a named mechanism.")
    if len(as_text(mechanism.get("explanation"))) < 20:
        issues.append("uniqueMechanism.explanation is too thin.")
    if len(list_of_dicts(mechanism.get("steps"))) < 3:
        issues.append("uniqueMechanism.steps must include 3+ steps.")

    proof = plan.get("proofPlan") if isinstance(plan.get("proofPlan"), dict) else {}
    if proof.get("proofBeforeOffer") is not True:
        issues.append("proofPlan.proofBeforeOffer must be true.")
    if len(list_of_dicts(proof.get("proofItems"))) < 2:
        issues.append("proofPlan.proofItems must include 2+ proof/demo items.")

    product = plan.get("productReveal") if isinstance(plan.get("productReveal"), dict) else {}
    for key in [
        "productType",
        "plainEnglishDescription",
        "whoItIsFor",
        "whatItHelpsThemDo",
        "whyNow",
        "differenceFromAlternatives",
        "bridgeToOfferStack",
    ]:
        if len(as_text(product.get(key))) < 8:
            issues.append(f"productReveal.{key} is missing or too thin.")
    components = list_of_dicts(product.get("coreComponents"))
    if len(components) < 3:
        issues.append("productReveal.coreComponents must include 3+ feature-benefit-reason rows.")
    for index, item in enumerate(components, start=1):
        for key in ["feature", "benefit", "reasonItMatters", "buyerProblemSolved", "proofOrPreview", "plainBullet"]:
            if len(as_text(item.get(key))) < 3:
                issues.append(f"productReveal.coreComponents[{index}] missing {key}.")
    if len(list_of_dicts(product.get("howItWorksSteps"))) < 3:
        issues.append("productReveal.howItWorksSteps must include 3+ steps.")

    offer_stack = plan.get("offerStack") if isinstance(plan.get("offerStack"), dict) else {}
    if len(list_of_dicts(offer_stack.get("items"))) < 8:
        issues.append("offerStack.items must include 8+ value-explained deliverables.")
    for index, item in enumerate(list_of_dicts(offer_stack.get("items")), start=1):
        if len(value_item_title(item)) < 3 or len(value_item_copy(item)) < 8:
            issues.append(f"offerStack.items[{index}] must include title and buyer-facing value copy.")

    objections = list_of_dicts(plan.get("objectionMatrix"))
    if len(objections) < 7:
        issues.append("objectionMatrix must include 7+ objections.")
    for index, item in enumerate(objections, start=1):
        objection = as_text(item.get("objection"))
        if objection.lower() in GENERIC_OBJECTIONS:
            issues.append(f"objectionMatrix[{index}] uses generic objection wording: {objection}")
        for key in ["objection", "answer", "beliefShift"]:
            if len(as_text(item.get(key))) < 6:
                issues.append(f"objectionMatrix[{index}] missing {key}.")

    urgency = plan.get("urgencyBasis") if isinstance(plan.get("urgencyBasis"), dict) else {}
    if urgency.get("fakeUrgency") is not False:
        issues.append("urgencyBasis.fakeUrgency must be false.")
    if as_text(urgency.get("type")) not in VALID_URGENCY_TYPES:
        issues.append("urgencyBasis.type is invalid or missing.")
    if as_text(urgency.get("type")) != "none" and len(as_text(urgency.get("description"))) < 8:
        issues.append("urgencyBasis.description is required for real urgency.")

    rows = section_rows(plan)
    row_ids = [as_text(row.get("sectionId")) for row in rows]
    if len(rows) < 16:
        issues.append("sectionPlan must include 16+ section rows.")
    for section_id in COPY_SPINE_SECTIONS:
        if section_id not in row_ids:
            issues.append(f"sectionPlan missing required Copy Studio spine section: {section_id}.")
    for index, row in enumerate(rows, start=1):
        missing_row = [key for key in REQUIRED_SECTION_FIELDS if key not in row]
        if missing_row:
            issues.append(f"sectionPlan[{index}] missing fields: " + ", ".join(missing_row))
        if not list_of_dicts(row.get("copyBlocks")):
            issues.append(f"sectionPlan[{index}] has no copyBlocks.")
    issues.extend(copy_block_quality_issues(plan))
    if "proof" in row_ids and "offer-stack" in row_ids and row_ids.index("proof") > row_ids.index("offer-stack"):
        issues.append("sectionPlan must place proof before offer-stack.")
    if "new-insight" in row_ids and "mechanism" in row_ids and row_ids.index("new-insight") > row_ids.index("mechanism"):
        issues.append("sectionPlan must place new-insight before mechanism.")
    return issues


def markdown_section(title: str, lines: list[str]) -> list[str]:
    return [f"# {title}", "", *[line for line in lines if line is not None], ""]


def render_copy_blueprint_markdown(plan: dict) -> str:
    by_section = section_by_id(plan)
    product = plan["productReveal"]
    mechanism = plan["uniqueMechanism"]
    proof = plan["proofPlan"]
    offer_stack = plan["offerStack"]
    guarantee = plan["guarantee"]
    value_logic = plan["valueLogic"]
    urgency = plan["urgencyBasis"]
    lines: list[str] = [
        f"# {plan['offerName']} Sales Copy",
        "",
        "# Sales Page Type",
        "",
        f"- pageType: {PAGE_TYPE}",
        f"- copyFramework: {COPY_FRAMEWORK}",
        f"- pageFramework: {PAGE_FRAMEWORK}",
        "- standaloneCopyRequired: true",
        "- vslDependency: optional-supporting-asset",
        "",
        "# Section Blueprint",
        "",
        "| sectionId | conversionJob | targetWords | beliefShift | proofOrObjection | visualKind | copyAnchor | ctaRole |",
        "| --- | --- | ---: | --- | --- | --- | --- | --- |",
    ]
    for row in section_rows(plan):
        section_id = as_text(row.get("sectionId"))
        belief = f"{as_text(row.get('buyerBeliefBefore'))} -> {as_text(row.get('buyerBeliefAfter'))}"
        lines.append(
            "| "
            + " | ".join(
                [
                    section_id,
                    as_text(row.get("conversionJob")),
                    as_text(row.get("maxWords"), "120"),
                    belief,
                    as_text(row.get("proofOrSupport")),
                    as_text(row.get("visualNeed")),
                    section_id,
                    as_text(row.get("ctaRole")),
                ]
            )
            + " |"
        )
    lines.extend([""])

    hero = by_section.get("hero", {})
    vsl = by_section.get("vsl", {})
    problem = by_section.get("problem", {})
    agitation = by_section.get("agitation", {})
    before_after = by_section.get("before-after", {})
    fit = by_section.get("fit", {})
    pricing = by_section.get("pricing", {})
    final_cta = by_section.get("final-cta", {})

    lines.extend(
        markdown_section(
            "Hero",
            [
                f"Buyer filter: {block_text(hero, 'prehead', fallback='For ' + plan['audience'])}",
                f"Headline: {block_text(hero, 'headline', fallback=plan['corePromise'])}",
                block_text(hero, "lead", "paragraph", fallback=plan["corePromise"]),
                f"CTA: {block_text(hero, 'cta', fallback='Get instant access')}",
            ],
        )
    )
    lines.extend(
        markdown_section(
            "VSL Setup",
            [
                block_text(vsl, "headline", fallback="The short breakdown shows the whole argument."),
                *[f"- {item}" for item in block_list(vsl, "bullet", "paragraph")[:5]],
                "Note: The written page carries the complete selling argument even if the VSL is removed.",
            ],
        )
    )
    lines.extend(
        markdown_section(
            "Problem Diagnosis",
            [
                block_text(problem, "headline", fallback="The real problem is not what it looks like."),
                block_text(problem, "paragraph", "lead", fallback=plan["primaryPain"]),
            ],
        )
    )
    lines.extend(
        markdown_section(
            "Agitation",
            [
                block_text(agitation, "headline", fallback="The cost compounds when the wrong fix keeps winning."),
                block_text(agitation, "paragraph", "lead", fallback="Waiting keeps the buyer stuck with the same gap."),
            ],
        )
    )
    lines.extend(["# Failed Alternatives", ""])
    for item in plan["failedAlternatives"]:
        lines.append(f"- {item['name']}: {item['whyItFails']} What is needed instead: {item['whatIsNeededInstead']}")
    lines.extend([""])
    lines.extend(
        markdown_section(
            "Epiphany / New Insight",
            [
                plan["newInsight"],
            ],
        )
    )
    lines.extend(["# Unique Mechanism", "", f"Mechanism: {mechanism['name']}", "", mechanism["explanation"], "", mechanism["whyItWorks"], ""])
    for step in mechanism["steps"]:
        lines.append(f"- {value_item_title(step)}: {value_item_copy(step)}")
    lines.extend([""])
    lines.extend(["# Proof Or Demonstration", ""])
    for item in proof["proofItems"]:
        lines.append(f"- {value_item_title(item)}: {value_item_copy(item)}")
    lines.extend([""])
    lines.extend(
        markdown_section(
            "Before And After",
            [
                block_text(before_after, "headline", fallback="The before and after is concrete."),
                block_text(before_after, "paragraph", "lead", fallback="Before, the buyer keeps guessing. After, the next action is clear."),
            ],
        )
    )
    lines.extend(
        [
            "# Product Reveal",
            "",
            f"Product type: {product['productType']}",
            "",
            product["plainEnglishDescription"],
            "",
            f"Who it is for: {product['whoItIsFor']}",
            "",
            f"What it helps them do: {product['whatItHelpsThemDo']}",
            "",
            f"Why now: {product['whyNow']}",
            "",
            "## Feature-Benefit Breakdown",
            "",
        ]
    )
    for component in product["coreComponents"]:
        lines.extend(
            [
                f"- Feature: {component['feature']}",
                f"  Benefit: {component['benefit']}",
                f"  Reason it matters: {component['reasonItMatters']}",
                f"  Buyer problem solved: {component['buyerProblemSolved']}",
                f"  Proof or preview: {component['proofOrPreview']}",
                f"  Plain bullet: {component['plainBullet']}",
            ]
        )
    lines.extend(["", "## How It Works", ""])
    for step in product["howItWorksSteps"]:
        lines.append(f"- {value_item_title(step)}: {value_item_copy(step)}")
    lines.extend(["", "## Look Inside Proof", ""])
    for item in product["lookInsideProof"]:
        lines.append(f"- {value_item_title(item)}: {value_item_copy(item)}")
    lines.extend(["", product["differenceFromAlternatives"], "", product["bridgeToOfferStack"], ""])
    lines.extend(["# Offer Stack", ""])
    for item in offer_stack["items"]:
        value = as_text(item.get("value"))
        suffix = f" ({value})" if value else ""
        lines.append(f"- {value_item_title(item)}{suffix}: {value_item_copy(item)}")
    if plan.get("bonuses"):
        lines.extend(["", "## Bonuses / Accelerators", ""])
        for item in plan["bonuses"]:
            lines.append(f"- {value_item_title(item)}: {value_item_copy(item)}")
    lines.extend(
        [
            "",
            "# Who It Is For",
            "",
            block_text(fit, "paragraph", "lead", fallback=product["whoItIsFor"]),
            "",
            "# Who It Is Not For",
            "",
            "This is not for buyers who want the old failed alternatives renamed as a new product.",
            "",
            "# Pricing And Value",
            "",
            block_text(pricing, "headline", fallback=value_logic["comparison"]),
            "",
            value_logic["priceJustification"],
            "",
            f"Today price: {value_logic['todayPrice']}",
            "",
            "# Guarantee",
            "",
            f"{guarantee['name']}: {guarantee['terms']} {guarantee['reassurance']}",
            "",
            "# FAQ",
            "",
        ]
    )
    for item in plan["objectionMatrix"]:
        lines.extend([f"## {item['objection']}", "", item["answer"], "", f"Belief shift: {item['beliefShift']}", ""])
    lines.extend(
        [
            "# Urgency / Scarcity Logic",
            "",
            f"Urgency type: {urgency['type']}",
            "",
            urgency.get("description", "") or "No fake urgency is used. The decision is driven by value, clarity, and risk reversal.",
            "",
            "# Final CTA",
            "",
            block_text(final_cta, "headline", fallback=f"Get {plan['offerName']} today."),
            "",
            block_text(final_cta, "paragraph", "lead", fallback=plan["corePromise"]),
            "",
            f"CTA: {block_text(final_cta, 'cta', fallback=offer_stack['cta'])}",
            "",
        ]
    )
    return "\n".join(lines)


def section_title(section_id: str) -> str:
    return {
        "hero": "Big Promise",
        "vsl": "Short Breakdown Setup",
        "problem": "Problem Diagnosis",
        "agitation": "Cost Of Staying Stuck",
        "failed-alternatives": "Failed Alternatives",
        "new-insight": "Epiphany / New Insight",
        "mechanism": "Unique Mechanism",
        "proof": "Proof Or Demonstration",
        "before-after": "Before And After",
        "product": "Product Reveal",
        "feature-benefit": "Feature-Benefit Breakdown",
        "how-it-works": "How It Works",
        "offer-stack": "Offer Stack",
        "bonuses": "Bonuses / Accelerators",
        "pricing": "Pricing And Value",
        "guarantee": "Guarantee",
        "fit": "Who It Is For",
        "faq": "FAQ",
        "final-cta": "Final Close",
    }.get(section_id, section_id.replace("-", " ").title())


def render_copy_blocks(row: dict) -> list[str]:
    lines: list[str] = []
    for block in list_of_dicts(row.get("copyBlocks")):
        block_type = as_text(block.get("type"))
        text = as_text(block.get("text"))
        if not text:
            continue
        if block_type == "headline":
            lines.extend([text, ""])
        elif block_type == "prehead":
            lines.extend([text.upper(), ""])
        elif block_type == "bullet":
            lines.append(f"- {text}")
        elif block_type == "cta":
            lines.extend(["", f"CTA: {text}", ""])
        elif block_type in {"question", "answer"}:
            lines.extend([text, ""])
        else:
            lines.extend([text, ""])
    return lines


def render_sales_copy_markdown(plan: dict) -> str:
    by_section = section_by_id(plan)
    product = plan["productReveal"]
    mechanism = plan["uniqueMechanism"]
    proof = plan["proofPlan"]
    offer_stack = plan["offerStack"]
    guarantee = plan["guarantee"]
    value_logic = plan["valueLogic"]
    urgency = plan["urgencyBasis"]
    lines: list[str] = [
        f"# {plan['offerName']} Sales Copy",
        "",
        f"For {plan['audience']}.",
        "",
    ]

    for section_id in COPY_SPINE_SECTIONS:
        row = by_section.get(section_id, {})
        lines.extend([f"## {section_title(section_id)}", ""])
        rendered = render_copy_blocks(row)
        if rendered:
            lines.extend(rendered)

        if section_id == "failed-alternatives":
            for item in plan["failedAlternatives"]:
                lines.append(f"- {item['name']}: {item['whyItFails']} What is needed instead: {item['whatIsNeededInstead']}")
            lines.append("")
        elif section_id == "new-insight":
            lines.extend([plan["newInsight"], ""])
        elif section_id == "mechanism":
            lines.extend([f"{mechanism['name']}: {mechanism['explanation']}", "", mechanism["whyItWorks"], ""])
            for step in mechanism["steps"]:
                lines.append(f"- {value_item_title(step)}: {value_item_copy(step)}")
            lines.append("")
        elif section_id == "proof":
            for item in proof["proofItems"]:
                lines.append(f"- {value_item_title(item)}: {value_item_copy(item)}")
            lines.append("")
        elif section_id == "product":
            lines.extend(
                [
                    product["plainEnglishDescription"],
                    "",
                    f"Who it is for: {product['whoItIsFor']}",
                    "",
                    f"What it helps them do: {product['whatItHelpsThemDo']}",
                    "",
                    f"Why now: {product['whyNow']}",
                    "",
                ]
            )
        elif section_id == "feature-benefit":
            for component in product["coreComponents"]:
                lines.append(f"- {component['feature']}: {component['plainBullet']} Benefit: {component['benefit']} Reason it matters: {component['reasonItMatters']}")
            lines.append("")
        elif section_id == "how-it-works":
            for step in product["howItWorksSteps"]:
                lines.append(f"- {value_item_title(step)}: {value_item_copy(step)}")
            lines.extend(["", "Look inside proof:", ""])
            for item in product["lookInsideProof"]:
                lines.append(f"- {value_item_title(item)}: {value_item_copy(item)}")
            lines.extend(["", product["differenceFromAlternatives"], "", product["bridgeToOfferStack"], ""])
        elif section_id == "offer-stack":
            for item in offer_stack["items"]:
                value = as_text(item.get("value"))
                suffix = f" ({value})" if value else ""
                lines.append(f"- {value_item_title(item)}{suffix}: {value_item_copy(item)}")
            lines.extend(["", f"CTA: {offer_stack['cta']}", offer_stack["accessCopy"], ""])
        elif section_id == "bonuses":
            for item in list_of_dicts(plan.get("bonuses")):
                lines.append(f"- {value_item_title(item)}: {value_item_copy(item)}")
            lines.append("")
        elif section_id == "pricing":
            lines.extend([value_logic["comparison"], "", value_logic["priceJustification"], "", f"Today price: {value_logic['todayPrice']}", ""])
        elif section_id == "guarantee":
            lines.extend([f"{guarantee['name']}: {guarantee['terms']} {guarantee['reassurance']}", ""])
        elif section_id == "faq":
            for item in plan["objectionMatrix"]:
                lines.extend([f"### {item['objection']}", "", item["answer"], ""])
        elif section_id == "final-cta":
            if urgency.get("type") != "none":
                lines.extend(["Urgency:", urgency.get("description", ""), ""])

    return "\n".join(line.rstrip() for line in lines).strip() + "\n"


def page_section_copy(plan: dict, section_id: str) -> dict:
    row = section_by_id(plan).get(section_id, {})
    data: dict = {}
    headline = block_text(row, "headline")
    if headline:
        data["headline"] = headline
    lead = block_text(row, "lead", "paragraph")
    if lead:
        data["copy"] = lead
    bullets = block_list(row, "bullet")
    if bullets:
        data["bullets"] = bullets
    cta = block_text(row, "cta")
    if cta:
        data["cta"] = cta
    return data


def build_sales_page_blueprint(plan: dict) -> dict:
    product = plan["productReveal"]
    mechanism = plan["uniqueMechanism"]
    proof = plan["proofPlan"]
    value_logic = plan["valueLogic"]
    guarantee = plan["guarantee"]
    checkout = as_text(plan.get("checkoutTarget"), DEFAULT_CHECKOUT_TARGET)
    page_kit_archetype = as_text(plan.get("pageKitArchetype"), "classic-vsl-longform")
    theme_preset = as_text(plan.get("themePreset"), "classic-direct-response")
    if page_kit_archetype not in ALLOWED_PAGE_KIT_ARCHETYPES:
        raise SystemExit(f"Unsupported Page Kit archetype in copy-plan.json: {page_kit_archetype}")
    if theme_preset not in ALLOWED_THEME_PRESETS:
        raise SystemExit(f"Unsupported Page Kit theme preset in copy-plan.json: {theme_preset}")

    sections = {section_id: page_section_copy(plan, section_id) for section_id in PAGE_SECTION_ORDER}
    sections["failed-alternatives"]["rows"] = [
        {
            "tried": item["name"],
            "fails": item["whyItFails"],
            "instead": item["whatIsNeededInstead"],
        }
        for item in plan["failedAlternatives"]
    ]
    mechanism_steps = [{"title": value_item_title(item), "copy": value_item_copy(item)} for item in mechanism["steps"]]
    sections["mechanism"]["headline"] = sections["mechanism"].get("headline") or mechanism["name"]
    sections["mechanism"]["copy"] = sections["mechanism"].get("copy") or mechanism["explanation"]
    sections["mechanism"]["cards"] = mechanism_steps[:3]
    sections["proof"]["cards"] = [{"title": value_item_title(item), "copy": value_item_copy(item)} for item in proof["proofItems"][:3]]
    sections["product"]["headline"] = sections["product"].get("headline") or f"Introducing {plan['offerName']}"
    sections["product"]["copy"] = product["plainEnglishDescription"]
    product_cards = [
        {
            "title": component["feature"],
            "copy": component["plainBullet"],
        }
        for component in product["coreComponents"][:3]
    ]
    sections["product"]["cards"] = product_cards
    sections["offer-stack"]["deliverables"] = [
        f"{value_item_title(item)} so {value_item_copy(item)}" for item in plan["offerStack"]["items"]
    ]
    sections["offer-stack"]["cta"] = plan["offerStack"]["cta"]
    sections["offer-stack"]["accessCopy"] = plan["offerStack"]["accessCopy"]
    sections["pricing"]["headline"] = sections["pricing"].get("headline") or value_logic["comparison"]
    sections["pricing"]["copy"] = value_logic["priceJustification"]
    sections["guarantee"]["headline"] = sections["guarantee"].get("headline") or guarantee["name"]
    sections["guarantee"]["copy"] = f"{guarantee['terms']} {guarantee['reassurance']}"
    sections["faq"]["items"] = [{"q": item["objection"], "a": item["answer"]} for item in plan["objectionMatrix"]]

    required_sections = [
        {
            "id": "header",
            "job": "Establish brand and orientation without section navigation.",
            "requiredContent": ["Logo/brand", "optional primary CTA only", "no section navigation"],
            "marker": "data-offeros-section=\"header\"",
        }
    ]
    for section_id in PAGE_SECTION_ORDER:
        row = section_by_id(plan).get(section_id, {})
        required_sections.append(
            {
                "id": section_id,
                "job": as_text(row.get("conversionJob"), f"Render {section_id} copy from Copy Studio."),
                "requiredContent": [as_text(row.get("primaryClaim"), "Copy Studio section claim")],
                "marker": f"data-offeros-section=\"{section_id}\"",
                "visual": as_text(row.get("visualNeed")),
            }
        )

    return {
        "schema": "offeros/sales-page-blueprint/v1",
        "pageType": PAGE_TYPE,
        "pageKitArchetype": page_kit_archetype,
        "themePreset": theme_preset,
        "framework": PAGE_FRAMEWORK,
        "copyFramework": COPY_FRAMEWORK,
        "compositionContract": COMPOSITION_CONTRACT,
        "copyPlanPath": "copy-plan.json",
        "copyStudioUsed": True,
        "standaloneCopyRequired": True,
        "vslDependency": "optional-supporting-asset",
        "offerName": plan["offerName"],
        "audience": plan["audience"],
        "problem": plan["primaryPain"],
        "checkout": {"target": checkout, "mode": "anchor" if checkout == DEFAULT_CHECKOUT_TARGET else "external-link", "orderForm": False},
        "hero": {
            "contract": "stacked-vsl-hero-v2",
            "layout": "stacked-vsl",
            "template": "offeros-stacked-vsl-v2",
            "videoFrame": "large-16x9",
            "stackOrder": ["copy-stack", "vsl-frame", "price-strip", "trust-row"],
        },
        "requiredSections": required_sections,
        "sections": sections,
        "offerStack": {
            "contract": "direct-response-buy-box-v1",
            "anchorId": "checkout",
            "requiredMarkers": [
                "data-offeros-product-bundle",
                "data-offeros-offer-checklist",
                "data-offeros-value-row",
                "data-offeros-cta",
                "data-offeros-stack-cta",
                "data-offeros-access-copy",
            ],
            "minimumDeliverables": 8,
            "orderForm": False,
        },
        "optionalBlocks": ["comparison-table", "bonus-stack", "risk-reversal-callout"],
        "qualityTargets": {
            "minimumVisibleWords": 2500,
            "minimumFaqItems": 7,
            "minimumCtas": 4,
            "minimumPostHeroCtas": 3,
            "maxVslSetupWords": 220,
            "maxParagraphWords": 55,
        },
        "builder": {
            "version": "offeros-page-kit-builder-v1",
            "sourceTemplate": "assets/templates/sales-page/page-skeleton.html",
            "themePath": "theme.json",
            "outputPath": "index.html",
            "buildMode": "deep",
            "generatedAt": datetime.now(timezone.utc).isoformat(),
            "generator": STUDIO_VERSION,
            "contentSource": "copy-plan.json",
            "assetPlanPath": "visual-asset-plan.md",
        },
        "disallowedBlocks": ["order-form", "embedded-checkout", "payment-fields", "credit-card-form"],
    }


def upsert_artifact(manifest: dict, artifact: dict) -> None:
    artifacts = manifest.setdefault("artifacts", [])
    for index, item in enumerate(artifacts):
        if item.get("id") == artifact.get("id"):
            artifacts[index] = {**item, **artifact}
            return
    artifacts.append(artifact)


def update_manifest(
    manifest: dict,
    copy_path: str,
    copy_blueprint_path: str,
    copy_plan_path: str,
    blueprint_path: str,
    plan: dict,
    copy_markdown: str,
) -> dict:
    now = datetime.now(timezone.utc).isoformat()
    upsert_artifact(
        manifest,
        {
            "id": "copy-plan",
            "title": "Copy Studio Plan",
            "type": "source",
            "category": "Sales",
            "path": copy_plan_path,
            "preview": copy_plan_path,
            "description": "Structured Modern Brunson-style sales argument source.",
            "status": "complete",
            "provenance": "manual",
            "updatedAt": now,
        },
    )
    upsert_artifact(
        manifest,
        {
            "id": "sales-copy",
            "title": "Long-Form Sales Copy",
            "type": "copy",
            "category": "Sales",
            "path": copy_path,
            "preview": copy_path,
            "description": "Clean written long-form sales copy rendered from Copy Studio source.",
            "status": "complete",
            "provenance": STUDIO_VERSION,
            "updatedAt": now,
        },
    )
    upsert_artifact(
        manifest,
        {
            "id": "copy-blueprint",
            "title": "Copy Blueprint",
            "type": "source",
            "category": "Sales",
            "path": copy_blueprint_path,
            "preview": copy_blueprint_path,
            "description": "Copy Studio blueprint, section map, and rendering contract.",
            "status": "complete",
            "provenance": STUDIO_VERSION,
            "updatedAt": now,
        },
    )
    upsert_artifact(
        manifest,
        {
            "id": "sales-page-blueprint",
            "title": "Sales Page Blueprint",
            "type": "source",
            "category": "Sales",
            "path": blueprint_path,
            "preview": blueprint_path,
            "description": "Page Kit blueprint generated from Copy Studio source.",
            "status": "complete",
            "provenance": STUDIO_VERSION,
            "updatedAt": now,
        },
    )
    manifest["offerName"] = as_text(manifest.get("offerName"), plan["offerName"])
    manifest["audience"] = as_text(manifest.get("audience"), plan["audience"])
    manifest["problem"] = as_text(manifest.get("problem"), plan["primaryPain"])
    manifest["price"] = as_text(manifest.get("price"), plan["price"])
    copy_quality = manifest.setdefault("quality", {}).setdefault("copy", {})
    copy_quality.update(
        {
            "studio": STUDIO_VERSION,
            "framework": COPY_FRAMEWORK,
            "pageFramework": PAGE_FRAMEWORK,
            "standaloneCopyRequired": True,
            "vslDependency": "optional-supporting-asset",
            "copyPlanPath": copy_plan_path,
            "copyPath": copy_path,
            "copyBlueprintPath": copy_blueprint_path,
            "copyIsCustomerFacing": True,
            "salesPageBlueprintPath": blueprint_path,
            "hasNewInsight": bool(as_text(plan.get("newInsight"))),
            "hasUniqueMechanism": bool(as_text(plan.get("uniqueMechanism", {}).get("name"))),
            "hasFailedAlternatives": len(list_of_dicts(plan.get("failedAlternatives"))) >= 3,
            "hasProofBeforeOffer": plan.get("proofPlan", {}).get("proofBeforeOffer") is True,
            "hasFeatureBenefitBreakdown": len(list_of_dicts(plan.get("productReveal", {}).get("coreComponents"))) >= 3,
            "hasObjectionMatrix": len(list_of_dicts(plan.get("objectionMatrix"))) >= 7,
            "sectionPlanCount": len(section_rows(plan)),
            "productComponentCount": len(list_of_dicts(plan.get("productReveal", {}).get("coreComponents"))),
            "offerStackItemCount": len(list_of_dicts(plan.get("offerStack", {}).get("items"))),
            "urgencyBasisType": as_text(plan.get("urgencyBasis", {}).get("type")),
            "fakeUrgency": plan.get("urgencyBasis", {}).get("fakeUrgency"),
            "renderedFromCopyPlan": True,
            "finishedCopySource": "copy-plan.sectionPlan.copyBlocks",
            "copyBlocksBuyerFacing": True,
            "copyCriticRubric": "copy-critic-rubric-v1",
            "copyCriticPassed": True,
            "copyWordCount": word_count(copy_markdown),
            "copyBlockWordCount": sum(row_copy_word_count(row) for row in section_rows(plan)),
            "minimumCopyWords": SALES_COPY_WORD_MINIMUM,
            "targetCopyWords": f"{SALES_COPY_TARGET_MINIMUM}-{SALES_COPY_TARGET_MAXIMUM}",
        }
    )
    manifest["updatedAt"] = now
    return manifest


def main() -> int:
    parser = argparse.ArgumentParser(description="Build OfferOS Copy Studio artifacts from copy-plan.json.")
    parser.add_argument("--workspace", default=".", help="Offer project root.")
    parser.add_argument("--manifest", default="offer-os.json", help="Manifest path relative to workspace.")
    parser.add_argument("--copy-plan", default="copy-plan.json", help="Copy plan JSON path relative to workspace.")
    parser.add_argument("--copy-output", default="copy.md", help="Clean written sales-copy Markdown path relative to workspace.")
    parser.add_argument("--copy-blueprint-output", default="copy-blueprint.md", help="Rendered Copy Studio blueprint Markdown path relative to workspace.")
    parser.add_argument("--blueprint-output", default="sales-page-blueprint.json", help="Generated sales-page blueprint path relative to workspace.")
    parser.add_argument("--no-write", action="store_true", help="Validate only; do not write rendered artifacts.")
    args = parser.parse_args()

    root = Path(args.workspace).resolve()
    manifest_path = root / args.manifest
    copy_plan_path = root / args.copy_plan
    copy_output_path = root / args.copy_output
    copy_blueprint_output_path = root / args.copy_blueprint_output
    blueprint_output_path = root / args.blueprint_output

    manifest = read_json(manifest_path)
    plan = read_json(copy_plan_path)
    issues = validate_copy_plan(plan)
    if issues:
        for issue in issues:
            print(issue)
        return 1
    copy_markdown = render_sales_copy_markdown(plan)
    copy_quality_issues = sales_copy_markdown_quality_issues(plan, copy_markdown)
    if copy_quality_issues:
        for issue in copy_quality_issues:
            print(issue)
        return 1
    copy_blueprint_markdown = render_copy_blueprint_markdown(plan)
    blueprint = build_sales_page_blueprint(plan)
    if args.no_write:
        print(json.dumps({"ok": True, "issues": [], "copyPath": args.copy_output, "copyBlueprintPath": args.copy_blueprint_output, "blueprintPath": args.blueprint_output}, indent=2))
        return 0
    copy_output_path.write_text(copy_markdown, encoding="utf-8")
    copy_blueprint_output_path.write_text(copy_blueprint_markdown, encoding="utf-8")
    write_json(blueprint_output_path, blueprint)
    manifest = update_manifest(
        manifest,
        args.copy_output.replace("\\", "/"),
        args.copy_blueprint_output.replace("\\", "/"),
        args.copy_plan.replace("\\", "/"),
        args.blueprint_output.replace("\\", "/"),
        plan,
        copy_markdown,
    )
    write_json(manifest_path, manifest)
    print(f"Built {copy_output_path}")
    print(f"Built {copy_blueprint_output_path}")
    print(f"Built {blueprint_output_path}")
    print(f"Updated {manifest_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
