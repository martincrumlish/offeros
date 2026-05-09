# OfferOS

OfferOS is a Codex plugin for building complete commercial offer systems through plugin-owned production studios: intake, offer architecture, design direction, professional no-SVG imagegen-based locked logo lockups/images, intake-gated copy-blueprint visual plans, OfferOS Page Kit direct-response sales pages, imagegen visual worker dispatch, long-form sales copy, coded sales page, Gotenberg/Chromium PDF workbook, ads, launch emails, editable VSL deck, delivery dashboard, and measured QA.

Current version: `0.13.4`.

## Repository Shape

This repo is the plugin root:

```text
offer-os/
  .codex-plugin/plugin.json
  skills/offer-os/SKILL.md
  skills/offer-os/references/
  skills/offer-os/assets/
  skills/offer-os/scripts/
```

Keep `.codex-plugin/plugin.json` at the repo root. Codex uses it to discover the plugin and load `skills/offer-os`.

## Install As A Codex Plugin

Clone the repo into the home-local plugin folder:

```powershell
$repo = "https://github.com/martincrumlish/offeros.git"
New-Item -ItemType Directory -Force "$HOME\plugins" | Out-Null
git clone $repo "$HOME\plugins\offer-os"
```

Create or update `$HOME\.agents\plugins\marketplace.json`.

If the file does not exist, create it with:

```json
{
  "name": "local",
  "interface": {
    "displayName": "Local Plugins"
  },
  "plugins": [
    {
      "name": "offer-os",
      "source": {
        "source": "local",
        "path": "./plugins/offer-os"
      },
      "policy": {
        "installation": "AVAILABLE",
        "authentication": "ON_INSTALL"
      },
      "category": "Productivity"
    }
  ]
}
```

If `marketplace.json` already exists, add only the `offer-os` object to its `plugins` array.

Restart Codex after installing or changing the marketplace file.

## Install Skill-Only Fallback

Plugin install is preferred. If a user only wants the skill, ask Codex:

```text
Install the OfferOS skill from https://github.com/martincrumlish/offeros/tree/v0.13.4/skills/offer-os
```

Restart Codex after installing the skill.

## Update

For a normal update:

```powershell
git -C "$HOME\plugins\offer-os" pull --ff-only
```

Restart Codex after pulling.

To pin a specific release:

```powershell
git -C "$HOME\plugins\offer-os" fetch --tags
git -C "$HOME\plugins\offer-os" checkout v0.13.4
```

To return to the latest main branch:

```powershell
git -C "$HOME\plugins\offer-os" checkout main
git -C "$HOME\plugins\offer-os" pull --ff-only
```

## Release Process

Before tagging a release:

```powershell
python skills/offer-os/scripts/self_test_offer_os_skill.py
```

Maintainers can also run regression checks against local known-bad generated outputs:

```powershell
python skills/offer-os/scripts/self_test_offer_os_skill.py --bad-workspace <path-to-known-bad-output>
```

Then:

```powershell
git status
git add .
git commit -m "Release OfferOS v0.13.4"
git tag v0.13.4
git remote add origin git@github.com:martincrumlish/offeros.git
git push -u origin main --tags
```

For later releases, bump `.codex-plugin/plugin.json`, update `CHANGELOG.md`, run self-test, commit, tag, and push.
