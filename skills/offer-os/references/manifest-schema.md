# Manifest Schema

`offer-os.json` is the project registry. Create it early and update it after every artifact.

## Required Shape

```json
{
  "schema": "offer-os/v1",
  "mode": "deep",
  "offerName": "Example Offer",
  "slug": "example-offer",
  "audience": "specific buyer segment",
  "price": "27",
  "status": "in_progress",
  "designSource": {
    "type": "design-md|url|screenshots|generated|hybrid|unresolved",
    "path": "",
    "url": "",
    "notes": ""
  },
  "brand": {
    "logo": "assets/logo.png",
    "primaryColor": "",
    "accentColor": "",
    "fontHeading": "",
    "fontBody": ""
  },
  "modules": [],
  "artifacts": [],
  "assumptions": [],
  "qa": {
    "lastRun": "",
    "status": "not_run",
    "technical": {
      "status": "not_run",
      "issues": []
    },
    "commercial": {
      "status": "not_run",
      "issues": []
    },
    "issues": []
  },
  "commercialAudit": {
    "status": "not_run",
    "scores": {},
    "blockingIssues": []
  }
}
```

## Artifact Shape

```json
{
  "id": "sales-page",
  "title": "Long-Form Sales Page",
  "type": "page",
  "category": "Sales",
  "path": "index.html",
  "preview": "index.html",
  "description": "Coded sales page for the offer.",
  "status": "complete",
  "provenance": "imagegen|imagegen-composite|provided|licensed|screenshot|html-css|manual|generated-by-code",
  "quality": {
    "buyerValue": 5,
    "usability": 5,
    "trust": 5,
    "notes": ""
  }
}
```

Use `provenance` for all images and previews. Use honest labels:

- `imagegen`: imagegen skill/tool output
- `imagegen-composite`: imagegen output composited with deterministic rendered text/layout
- `provided`: supplied by user
- `licensed`: licensed external asset
- `screenshot`: rendered screenshot from a real artifact
- `html-css`: rendered HTML/CSS visual
- `manual`: hand-authored document/page/deck
- `generated-by-code`: deterministic script output

Do not use words like "generated image", "AI-generated", or "imagegen" in an artifact title or description unless provenance is `imagegen` or `imagegen-composite`.

Do not register `pil-generated` artifacts. Pillow/PIL may be used for inspection, cropping, resizing, or compositing only when the underlying creative source is already `imagegen`, `provided`, or `licensed`.

For deep generated-design runs, primary conversion visuals must not use `html-css`, `generated-by-code`, `manual`, or `screenshot` provenance. Product bundles, offer-stack bundles, product mockups, hero/VSL thumbnails, buyer-situation photos, and ad creatives require `imagegen` or `imagegen-composite` unless the asset is genuinely `provided` or `licensed`.

## Artifact Types

Use these values:

- `page`
- `document`
- `source`
- `image`
- `pdf`
- `deck`
- `email`
- `ad`
- `dashboard`
- `qa`

## Required Artifact IDs

A deep run should register:

- `offer-architecture`
- `design-guide`
- `logo`
- `visual-asset-plan`
- `sales-copy`
- `sales-page-blueprint`
- `theme`
- `sales-page`
- `pdf-product-source`
- `pdf-product`
- `facebook-ads`
- `facebook-ad-image-1`
- `facebook-ad-image-2`
- `facebook-ad-image-3`
- `email-sequence`
- `vsl-deck`
- `vsl-preview`
- `delivery-dashboard`
- `qa-notes`

## Deep-Mode Quality Metadata

For deep mode, include module-level quality metadata when applicable:

```json
{
  "quality": {
    "pdf": {
      "pageCount": 28,
      "actionSurfaceCount": 10,
      "namedToolCount": 10,
      "pageArchetypeCount": 8,
      "maxPageArchetypeShare": 0.25,
      "completedExampleCount": 3,
      "blankTemplateCount": 3,
      "visualAssetCount": 6,
      "pdfSpecificVisualAssetCount": 4,
      "genericActionSurfaceLabelsRemoved": true,
      "hasCompletedExamples": true,
      "hasBlankTemplates": true,
      "renderChecked": true
    },
    "logo": {
      "logoMode": "single-final-logo-v1",
      "logoDirectionCount": 1,
      "finalLogoDirection": "wordmark plus mechanism badge",
      "finalLogoLocked": true,
      "downstreamLogoReference": "assets/logo.png",
      "downstreamImagegenLogoReference": "assets/logo.png",
      "singleFinalLogoOnly": true,
      "alternateLogosCreated": false,
      "downstreamImagegenMustUseLogoReference": true,
      "primaryFormat": "png",
      "generationTool": "imagegen-single-final-logo",
      "imagegenNotUsedReason": "",
      "imagegenCompleteLogoLockupAttempted": true,
      "finalLogoCount": 1,
      "logoGenerationCount": 1,
      "imagegenCompleteLogoAccepted": true,
      "fallbackWordmarkCompositeReason": "",
      "brandMarkSource": "imagegen",
      "wordmarkSource": "imagegen",
      "wordmarkCompositeMethod": "",
      "logoLockup": true,
      "includesReadableOfferName": true,
      "exactOfferNamePreserved": true,
      "markIsLogoSymbol": true,
      "markNotIllustration": true,
      "markOneColorUsable": true,
      "wordmarkTypographyChecked": true,
      "wordmarkKerningChecked": true,
      "professionalLockupApproved": true,
      "lockupPreviewChecked": true,
      "lockupPreviewPath": "output/qa/logo-lockup-preview.png",
      "svgAssetCreated": false,
      "smallSizeChecked": true,
      "oneColorChecked": true,
      "exportedPng": true,
      "critiquePassed": true
    },
    "vsl": {
      "slideCount": 24,
      "layoutCount": 9,
      "maxLayoutShare": 0.29,
      "visualAssetCount": 8,
      "uniqueVisualAssetCount": 12,
      "vslSpecificVisualAssetCount": 8,
      "maxRepeatedBitmapShare": 0.21,
      "visualReuseChecked": true,
      "primaryFormat": "pptx",
      "presentationReady": true,
      "hasSpeakerNotes": true,
      "notesAreNarration": true,
      "visibleStageLabelsRemoved": true,
      "layoutDiversityChecked": true,
      "visualPlaceholdersRemoved": true,
      "layoutAudit": [
        { "slide": 1, "layoutFamily": "full-bleed-title", "visualAsset": "hero image" }
      ],
      "hasOfferReveal": true,
      "hasPrice": true,
      "hasGuarantee": true,
      "hasObjections": true
    },
    "salesPage": {
      "pageType": "direct-response-long-form-vsl",
      "pageTypeReason": "Cold front-end offer needs full belief-shift page.",
      "requiredSectionContract": "direct-response-v1",
      "heroContract": "stacked-vsl-hero-v2",
      "heroLayout": "stacked-vsl",
      "heroTemplate": "offeros-stacked-vsl-v2",
      "heroVideoFrame": "large-16x9",
      "heroVideoProminenceChecked": true,
      "offerStackContract": "direct-response-buy-box-v1",
      "framework": "direct-response-long-form-v1",
      "compositionContract": "direct-response-composition-v2",
      "pageKit": "offeros-page-kit-v1",
      "pageKitBuilder": "offeros-page-kit-builder-v1",
      "pageKitArchetype": "classic-vsl-longform",
      "themePreset": "classic-direct-response",
      "pageKitBlueprintUsed": true,
      "themeTokensUsed": true,
      "checkoutTarget": "#checkout",
      "vslPlacement": "main-column-stacked",
      "orderFormIncluded": false,
      "copyBlueprintPresent": true,
      "sectionMarkersPresent": true,
      "visibleWordCount": 3200,
      "objectionCount": 8,
      "ctaCount": 5,
      "postHeroCtaCount": 3,
      "offerStackItemsUnique": true,
      "sectionDepthChecked": true,
      "repeatedTextChecked": true
    },
    "dashboard": {
      "templateVersion": "v2-modal",
      "hasModalPreview": true,
      "hasIframePreview": true
    },
    "images": {
      "hasArtifactSpecificPlan": true,
      "visualPlanPath": "visual-asset-plan.md",
      "visualPlanStage": "post-content-blueprint",
      "copyBlueprintUsed": true,
      "visualReusePolicy": "artifact-specific-v1",
      "salesPageImageSystem": "mixed-direct-response-v1",
      "mockupHeavyUserRequested": false,
      "agentDispatchUsed": true,
      "agentDispatchNotUsedReason": "",
      "imagegenCount": 5,
      "salesPageVisualCount": 4,
      "pdfVisualCount": 6,
      "pdfSpecificVisualCount": 4,
      "vslVisualCount": 12,
      "vslSpecificVisualCount": 8,
      "adImageCount": 3,
      "pdfUsesOnlySalesPageImages": false,
      "vslUsesOnlySalesPageImages": false,
      "salesPageReuseOnly": false,
      "fallbackCount": 2,
      "notes": ""
    }
  }
}
```

These fields do not replace real files. They give the validator and future agents a way to distinguish a real commercial build from a folder of thin placeholders.

## Status Values

- `planned`
- `draft`
- `needs_revision`
- `complete`
- `validated`

Do not mark an artifact `complete` until it has passed its module critique gate.
