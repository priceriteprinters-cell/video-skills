# Video Skills

One agent skill that bundles three sub-guides behind a single router (`SKILL.md`):

| Sub-guide | What it's for |
|---|---|
| [`complete-video-production`](complete-video-production/GUIDE.md) | End-to-end production: narration or script → researched, timed, verified MP4 + asset packs |
| [`motion-graphics`](motion-graphics/GUIDE.md) | Unified Remotion + HyperFrames engine knowledge: animation, transitions, captions, 3D, maps, audio, rendering |
| [`motion-graphics-lovable`](motion-graphics-lovable/GUIDE.md) | The same motion-graphics knowledge in a flattened, Lovable-friendly reference layout |

Install it once; the router picks the sub-guide for the task. `complete-video-production` plans, sources and verifies, `motion-graphics` builds the animation.

---

A [Claude Code / agent skill](https://github.com/anthropics/skills) for **end-to-end motion-graphics video production** — from narration audio or a script to a finished, synchronized, verified MP4 — plus a standalone mode that generates verified AI PNG asset packs.

## Install

```bash
npx skills add priceriteprinters-cell/video-skills
```

That installs the single `video-skills` skill — all three sub-guides come with it. Re-run the same command anytime to pull the latest version.

## What it does

Turns an audio file, script, or topic brief into a complete motion-graphics video with:

- **Narration-first timeline** — scenes, captions, music, and sound effects are timed against the measured narration duration, not guessed.
- **Readable visuals** — selectable font pairings (29 presets), coordinated color palettes (24 presets across luxury, gaming, nature, corporate, playful, health, developer categories), and dark/light/matched visual modes.
- **Authentic assets** — searches, downloads, and inspects real logos, icons, illustrations, and photos before ever considering generated fallbacks; no fake screenshots or counterfeit logos.
- **Synchronized audio** — background music ducked under narration, SFX tied to meaningful visual events, integrated loudness around −14 LUFS.
- **Verified delivery** — automated checks (`production_check.py scan`, black-frame detection) plus a full review pass before anything is delivered, with honest qualification of every limitation.

### Two modes

| Mode | Use when | Output |
|---|---|---|
| **Full production** | You want a finished video | Narrated, animated MP4 + captions + project files |
| **Asset-pack mode** | You only want the PNG assets, or want all assets before production | Verified `motion-assets/v1` ZIP with scene mapping |

### Suitable video types

Animated explainers, kinetic typography, educational videos, product walkthroughs, social videos, and animated promos — any subject. For generated footage / live-action styles, the skill routes to the platform's matching video-generation workflow instead.

## The workflow

1. **Brief** — confirm aspect ratio, font pairing (with real rendered previews), color palette, and visual mode before production starts. Nothing is inferred from platform or source dimensions.
2. **Research & audit** — transcribe supplied audio, fact-check every checkable claim against authoritative sources, then audit the script. Mechanical fixes applied automatically; meaning-affecting changes always ask first.
3. **Asset acquisition** — source and stage every required asset from the supplied no-sign-up resource catalog and lawful public sources; generated images are clearly labeled illustrations, never fake evidence.
4. **Timing** — build a master clock from measured narration; scene, caption, music, and SFX cues share the same timebase.
5. **Production handoff** — pass a complete creative brief (fonts, licenses, glyph checks, palette tokens, asset provenance, audio targets) to the animation task.
6. **Verification** — scan sources/captions, detect black frames, review motion and audio separately, and apply the full acceptance matrix.
7. **Delivery** — MP4 plus asset pack with sources/licenses, finalized script and transcript, editable project files, and every stated limitation.

## Repository structure

Everything installs as one skill folder; `SKILL.md` at its root routes to the sub-guide that fits the task.

```
video-skills/
├── SKILL.md                     # Router: picks the sub-guide for the task
├── complete-video-production/   # GUIDE.md + assets/, references/, scripts/ (detailed below)
├── motion-graphics/             # GUIDE.md + references/ (remotion, hyperframes, doctrine, registry-blocks)
└── motion-graphics-lovable/     # GUIDE.md + references/ (flattened layout)
```

### complete-video-production

```
complete-video-production/
├── GUIDE.md                  # Entry point: scope, briefing, workflow, boundaries
├── assets/
│   └── design-presets.json   # 29 font pairings + 24 palette presets
├── references/
│   ├── brief-and-assets.md           # Intake and asset inventory
│   ├── asset-pack-intake.md          # Validating attached asset ZIPs
│   ├── asset-pack-contract.md        # motion-assets/v1 pack format
│   ├── asset-pack-generation-design.md # Asset-pack mode design rules
│   ├── audio-and-mixing.md           # Music, SFX, loudness targets
│   ├── automation-tools.md           # Bundled Python helper usage
│   ├── captured-workflow.md          # Calibration example and lessons
│   ├── delegation.md                 # Animation task handoff
│   ├── free-design-resources-no-signup.md # Asset discovery catalog
│   ├── motion-and-rendering.md       # Visual production rules
│   ├── production-standards.md       # Art direction and QA standards
│   ├── qa-and-delivery.md            # Verification and recovery
│   ├── research-and-script-audit.md  # Transcription and fact-checking
│   ├── resource-acquisition.md       # Sourcing and rights policy
│   ├── timing-and-storyboard.md      # Narration timing
│   ├── typography-and-palettes.md    # Font/palette direction
│   └── version-notes.md              # Changelog
└── scripts/
    ├── asset_pack.py          # Pack build + motion-assets/v1 validation
    ├── production_check.py    # QA scans (captions, blackframes)
    ├── design_tools.py        # Preset listings, contrast checks, downloads
    ├── test_asset_pack.py     # Tests
    ├── test_design_tools.py   # Tests
    └── test_production_check.py # Tests
```

## Scripts

All helpers are plain Python (standard library). Run tests with:

```bash
python3 scripts/test_asset_pack.py
python3 scripts/test_design_tools.py
python3 scripts/test_production_check.py
```

- `design_tools.py` — preset listings, brief validation, contrast checks, provenance-tracked HTTPS downloads, icon retrieval, licensed font acquisition.
- `asset_pack.py` — build and validate asset packs against the `motion-assets/v1` contract.
- `production_check.py` — QA scans on sources/captions and rendered exports.

## Key principles

- **Zero placeholders** — no lorem ipsum, dummy text, TODOs, broken assets, or watermarked content in any export.
- **Accuracy outranks speed** — research unclear details or ask; never silently change meaning.
- **Preserve your voice** — uploaded narration's words, voice, and speed stay intact unless editing is authorized.
- **Honest delivery** — every limitation (approximate sync, missing audio, unofficial assets, unchecked claims) is stated in the final report.

## Version

Current: **v7** (`complete-video-production_v7`), published as the combined `video-skills` skill.

---

## Motion Graphics

One skill that merges **all 12 Remotion skills** ([remotion-dev/skills](https://github.com/remotion-dev/skills)) and **all HyperFrames skills, doctrine guides and registry blocks** ([heygen-com/hyperframes](https://github.com/heygen-com/hyperframes)) behind a single router.

### How it works

1. **Pick the engine** — Remotion (React, in-app `<Player>`) or HyperFrames (HTML + GSAP, registry blocks). Existing projects keep their engine; the two are never mixed in one composition.
2. **Apply motion doctrine** — engine-agnostic rules for easing, scene seams, beats and typography (`motion-doctrine`, `cut-the-curve`, `seam-craft`).
3. **Route by task** — load only the reference needed: timing, transitions, captions, maps, 3D, Lottie, audio, voiceover, SFX, Studio, rendering, Lambda/SaaS, upgrades.
4. **Use a workflow** when the format fits — faceless explainer, product launch, music video, PR/changelog, slideshow, captions, talking-head overlays, cursor demos.
5. **Deliver** — live preview first, render only on request, verify frames, legibility and audio sync.

### Structure

```
motion-graphics/
├── GUIDE.md                 # Router: engine choice, doctrine, task routing, delivery
└── references/
    ├── remotion/            # All 12 Remotion skills (create, markup, captions, maps, render, studio, saas, upgrade…)
    ├── hyperframes/         # 21 HyperFrames skills + workflows, templates and helper scripts
    ├── doctrine/            # motion-doctrine, cut-the-curve, seam-craft, captions-overlay, oversized-cursor, changelog-video
    └── registry-blocks/     # 7 ready-made 3D title / carousel / camera-orbit blocks
```

### Lovable edition

Lovable skill uploads allow at most 200 files, 1 MB each, 10 MB total. [`motion-graphics-lovable/`](motion-graphics-lovable/) is the same knowledge packed into 69 files (scripts and templates are fetched from the full `motion-graphics/` folder on demand). Zip that folder and upload it in Lovable — the full combined skill (929 files, ~12 MB) exceeds those limits.

### Tested

Verified end-to-end: every path in `SKILL.md` resolves, internal links checked (missing templates restored), all bundled `.mjs/.cjs/.py/.sh` scripts pass syntax checks, and a Remotion kinetic-title composition built from the skill plays correctly in a React (TanStack Start) app.

Example media from upstream (images, fonts, music clips) is not bundled; the skill fetches or generates replacements.

Credits: Remotion skills © Remotion; HyperFrames skills © HeyGen. See each upstream repository for licenses.
