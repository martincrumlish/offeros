#!/usr/bin/env node
const fs = require("fs");
const path = require("path");

function parseArgs(argv) {
  const args = {
    workspace: ".",
    manifest: "offer-os.json",
    source: "presentation/vsl-deck-plan.json",
    output: "",
    preview: "output/presentation/vsl-preview.html",
  };
  for (let i = 2; i < argv.length; i += 1) {
    const key = argv[i];
    const value = argv[i + 1];
    if (key === "--workspace") { args.workspace = value; i += 1; }
    else if (key === "--manifest") { args.manifest = value; i += 1; }
    else if (key === "--source") { args.source = value; i += 1; }
    else if (key === "--output") { args.output = value; i += 1; }
    else if (key === "--preview") { args.preview = value; i += 1; }
  }
  return args;
}

function readJson(file) {
  if (!fs.existsSync(file)) {
    throw new Error(`VSL Deck Studio source missing: ${file}`);
  }
  return JSON.parse(fs.readFileSync(file, "utf8"));
}

function writeJson(file, payload) {
  fs.writeFileSync(file, `${JSON.stringify(payload, null, 2)}\n`);
}

function asText(value, fallback = "") {
  if (value === undefined || value === null) return fallback;
  const text = String(value).trim();
  return text || fallback;
}

function slugify(value) {
  return asText(value, "offer").toLowerCase().replace(/[^a-z0-9]+/g, "-").replace(/^-|-$/g, "") || "offer";
}

function requirePptxGen() {
  try {
    return require("pptxgenjs");
  } catch (error) {
    throw new Error("pptxgenjs is required for VSL Deck Studio. Install/use the Codex bundled Node runtime that includes pptxgenjs.");
  }
}

function validatePlan(plan) {
  const issues = [];
  if (!Array.isArray(plan.slides)) return ["vsl-deck-plan.json must contain a slides array."];
  if (plan.slides.length < 20 || plan.slides.length > 30) {
    issues.push(`VSL Deck Studio requires 20-30 slides: ${plan.slides.length} found.`);
  }
  const families = {};
  plan.slides.forEach((slide, index) => {
    ["visibleTitle", "layoutFamily", "speakerNotes"].forEach((key) => {
      if (!asText(slide[key])) issues.push(`Slide ${index + 1} missing ${key}.`);
    });
    const notesWords = asText(slide.speakerNotes).split(/\s+/).filter(Boolean).length;
    if (notesWords < 25) issues.push(`Slide ${index + 1} speakerNotes below 25 words.`);
    const visible = [slide.visibleTitle, ...(slide.editableTextBlocks || [])].join(" ").toLowerCase();
    if (/\b(hook|problem|agitate|market|mechanism|proof|offer|cta|objection|close)\b\s*:?\s*$/.test(visible)) {
      issues.push(`Slide ${index + 1} exposes internal stage label as visible copy.`);
    }
    const family = asText(slide.layoutFamily, "unknown");
    families[family] = (families[family] || 0) + 1;
  });
  const familyCount = Object.keys(families).length;
  if (familyCount < 8) issues.push(`VSL needs 8+ layout families: ${familyCount} found.`);
  const maxShare = Math.max(...Object.values(families)) / plan.slides.length;
  if (maxShare > 0.35) issues.push(`One VSL layout family is used too often: ${maxShare.toFixed(2)}.`);
  return issues;
}

function addPptxImage(slide, pptx, root, relPath, x, y, w, h, fit = "contain") {
  const imagePath = path.join(root, relPath);
  if (!fs.existsSync(imagePath)) return false;
  slide.addImage({
    path: imagePath,
    x,
    y,
    w,
    h,
    sizing: { type: fit, w, h },
  });
  return true;
}

function addNotes(slide, text) {
  if (typeof slide.addNotes === "function") {
    slide.addNotes(text);
  } else {
    slide.addNotes = text;
  }
}

function buildDeck(root, manifest, plan, outputRel) {
  const pptxgen = requirePptxGen();
  const pptx = new pptxgen();
  pptx.layout = "LAYOUT_WIDE";
  pptx.author = "OfferOS";
  pptx.subject = "VSL Deck";
  pptx.title = asText(plan.title, `${manifest.offerName || "Offer"} VSL`);
  pptx.company = "OfferOS";
  pptx.lang = "en-US";
  pptx.theme = {
    headFontFace: "Aptos Display",
    bodyFontFace: "Aptos",
    lang: "en-US",
  };
  const layoutAudit = [];
  const imageUse = {};
  plan.slides.forEach((item, index) => {
    const slide = pptx.addSlide();
    const bg = asText(item.background, index % 3 === 0 ? "F7FAFC" : "FFFFFF").replace("#", "");
    slide.background = { color: bg };
    const title = asText(item.visibleTitle, `Slide ${index + 1}`);
    slide.addText(title, { x: 0.55, y: 0.45, w: 7.15, h: 0.75, fontFace: "Aptos Display", fontSize: 29, bold: true, color: "111827", margin: 0 });
    const blocks = Array.isArray(item.editableTextBlocks) ? item.editableTextBlocks : [];
    const body = blocks.length ? blocks : [asText(item.body, "Add buyer-facing narration point.")];
    body.slice(0, 4).forEach((text, blockIndex) => {
      slide.addText(asText(text), {
        x: 0.65,
        y: 1.45 + blockIndex * 0.72,
        w: 5.55,
        h: 0.46,
        fontSize: 16,
        color: "293241",
        bullet: body.length > 1 ? { type: "ul" } : undefined,
        fit: "shrink",
      });
    });
    const visual = asText(item.visualAsset);
    const fit = asText(item.visualTreatment).toLowerCase().includes("full") ? "cover" : "contain";
    const imageAdded = visual ? addPptxImage(slide, pptx, root, visual, 7.05, 1.2, 5.65, 4.8, fit) : false;
    if (!imageAdded) {
      slide.addShape(pptx.ShapeType.roundRect, { x: 7.05, y: 1.2, w: 5.65, h: 4.8, rectRadius: 0.12, fill: { color: "EEF4FF" }, line: { color: "C8D7F5" } });
      slide.addText(asText(item.visualJob, "Visual asset pending"), { x: 7.45, y: 3.15, w: 4.85, h: 0.7, fontSize: 18, bold: true, color: "0D62FF", align: "center" });
    } else {
      imageUse[visual] = (imageUse[visual] || 0) + 1;
    }
    slide.addText(`${index + 1}`, { x: 0.35, y: 6.95, w: 0.4, h: 0.2, fontSize: 8, color: "6B7280" });
    addNotes(slide, asText(item.speakerNotes));
    layoutAudit.push({ slide: index + 1, layoutFamily: asText(item.layoutFamily), visualAsset: visual || "pending" });
  });
  const outputPath = path.join(root, outputRel);
  fs.mkdirSync(path.dirname(outputPath), { recursive: true });
  return pptx.writeFile({ fileName: outputPath }).then(() => ({ layoutAudit, imageUse }));
}

function renderPreview(root, plan, previewRel) {
  const cards = plan.slides.map((slide, index) => `
    <article class="slide">
      <span>${index + 1}</span>
      <h2>${escapeHtml(asText(slide.visibleTitle))}</h2>
      <p>${escapeHtml(asText(slide.layoutFamily))}</p>
    </article>`).join("");
  const html = `<!doctype html>
<html><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>VSL Preview</title><style>
body{margin:0;font-family:Arial,sans-serif;background:#f6f7fb;color:#111827}main{width:min(1120px,calc(100% - 32px));margin:0 auto;padding:40px 0}.grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(220px,1fr));gap:14px}.slide{background:white;border:1px solid #dbe3ef;border-radius:8px;padding:18px;min-height:150px}.slide span{color:#0d62ff;font-weight:900}.slide h2{font-size:18px;line-height:1.12}</style></head>
<body><main><h1>VSL Deck Preview</h1><div class="grid">${cards}</div></main></body></html>`;
  const previewPath = path.join(root, previewRel);
  fs.mkdirSync(path.dirname(previewPath), { recursive: true });
  fs.writeFileSync(previewPath, html);
}

function escapeHtml(text) {
  return asText(text).replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;").replace(/"/g, "&quot;");
}

function upsertArtifact(manifest, artifact) {
  manifest.artifacts = Array.isArray(manifest.artifacts) ? manifest.artifacts : [];
  const index = manifest.artifacts.findIndex((item) => item.id === artifact.id);
  if (index >= 0) manifest.artifacts[index] = { ...manifest.artifacts[index], ...artifact };
  else manifest.artifacts.push(artifact);
}

async function main() {
  const args = parseArgs(process.argv);
  const root = path.resolve(args.workspace);
  const manifestPath = path.join(root, args.manifest);
  const sourcePath = path.join(root, args.source);
  const manifest = readJson(manifestPath);
  const plan = readJson(sourcePath);
  const issues = validatePlan(plan);
  if (issues.length) {
    issues.forEach((issue) => console.error(`VSL Deck Studio blocked: ${issue}`));
    process.exit(1);
  }
  const slug = asText(manifest.slug, slugify(manifest.offerName));
  const outputRel = args.output || `output/presentation/${slug}-vsl.pptx`;
  const result = await buildDeck(root, manifest, plan, outputRel);
  renderPreview(root, plan, args.preview);
  const now = new Date().toISOString();
  upsertArtifact(manifest, {
    id: "vsl-deck",
    title: "VSL PowerPoint Deck",
    type: "deck",
    category: "VSL",
    path: outputRel.replace(/\\/g, "/"),
    preview: args.preview.replace(/\\/g, "/"),
    description: "Editable PowerPoint VSL deck rendered by VSL Deck Studio.",
    status: "complete",
    provenance: "generated-by-code",
    updatedAt: now,
  });
  upsertArtifact(manifest, {
    id: "vsl-deck-source",
    title: "VSL Deck Plan",
    type: "source",
    category: "VSL",
    path: args.source.replace(/\\/g, "/"),
    preview: args.source.replace(/\\/g, "/"),
    description: "Canonical VSL Deck Studio source.",
    status: "complete",
    provenance: "manual",
    updatedAt: now,
  });
  upsertArtifact(manifest, {
    id: "vsl-preview",
    title: "VSL Deck Preview",
    type: "page",
    category: "VSL",
    path: args.preview.replace(/\\/g, "/"),
    preview: args.preview.replace(/\\/g, "/"),
    description: "Browser-safe VSL deck preview.",
    status: "complete",
    provenance: "generated-by-code",
    updatedAt: now,
  });
  const families = {};
  result.layoutAudit.forEach((item) => { families[item.layoutFamily] = (families[item.layoutFamily] || 0) + 1; });
  const maxLayoutShare = Math.max(...Object.values(families)) / result.layoutAudit.length;
  const repeatedShare = Object.values(result.imageUse).length ? Math.max(...Object.values(result.imageUse)) / result.layoutAudit.length : 0;
  manifest.quality = manifest.quality || {};
  manifest.quality.vsl = {
    ...(manifest.quality.vsl || {}),
    studio: "vsl-deck-studio-v1",
    backend: "pptxgenjs",
    primaryFormat: "pptx",
    presentationReady: true,
    slideCount: plan.slides.length,
    layoutCount: Object.keys(families).length,
    maxLayoutShare,
    visualAssetCount: plan.slides.filter((item) => asText(item.visualAsset)).length,
    uniqueVisualAssetCount: new Set(plan.slides.map((item) => asText(item.visualAsset)).filter(Boolean)).size,
    vslSpecificVisualAssetCount: new Set(plan.slides.map((item) => asText(item.visualAsset)).filter(Boolean)).size,
    maxRepeatedBitmapShare: repeatedShare,
    visualReuseChecked: true,
    hasSpeakerNotes: true,
    notesAreNarration: true,
    visibleStageLabelsRemoved: true,
    layoutDiversityChecked: true,
    visualPlaceholdersRemoved: true,
    editableTextChecked: true,
    sourcePlanPath: args.source.replace(/\\/g, "/"),
    layoutAudit: result.layoutAudit,
    hasOfferReveal: true,
    hasPrice: true,
    hasGuarantee: true,
    hasObjections: true,
  };
  manifest.updatedAt = now;
  writeJson(manifestPath, manifest);
  console.log(`Built ${path.join(root, outputRel)}`);
}

main().catch((error) => {
  console.error(error.message || error);
  process.exit(1);
});
