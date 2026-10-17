# Video Skills

One agent skill for **motion-graphics video production** — from narration audio or a script to a finished, synchronized, verified MP4 — plus the Remotion and HyperFrames animation knowledge behind it, and a standalone mode that generates verified AI PNG asset packs.

## Install

```bash
npx skills add priceriteprinters-cell/video-skills
```

That installs a single `video-skills` skill. Re-run the same command anytime to pull the latest version.

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

Animated explainers, kinetic typography, educational videos, product walkthroughs, social videos, and animated promos — any subject. For generated footage or live-action styles, the skill routes to the platform's matching video-generation workflow instead.

## The workflow

1. **Brief** — confirm aspect ratio, font pairing (with real rendered previews), color palette, and visual mode before production starts. Nothing is inferred from platform or source dimensions.
2. **Research & audit** — transcribe supplied audio, fact-check every checkable claim against authoritative sources, then audit the script. Mechanical fixes applied automatically; meaning-affecting changes always ask first.
3. **Asset acquisition** — source and stage every required asset from the supplied no-sign-up resource catalog and lawful public sources; generated images are clearly labeled illustrations, never fake evidence.
4. **Timing** — build a master clock from measured narration; scene, caption, music, and SFX cues share the same timebase.
5. **Production handoff** — pass a complete creative brief (fonts, licenses, glyph checks, palette tokens, asset provenance, audio targets) to the animation task.
6. **Verification** — scan sources/captions, detect black frames, review motion and audio separately, and apply the full acceptance matrix.
7. **Delivery** — MP4 plus asset pack with sources/licenses, finalized script and transcript, editable project files, and every stated limitation.

## What's inside

Everything is one skill — a single `SKILL.md` entry point with its support files beside it. There are no sub-skills to choose between.

```
video-skills/
├── SKILL.md      # routing, creative brief, asset rules, production pipeline, engine choice, QA, delivery
├── references/   # production stage docs, the Remotion tree, the HyperFrames tree, motion doctrine,
│                 # ready-made registry blocks, and format-level workflow folders
├── scripts/      # design_tools.py, production_check.py, asset_pack.py (+ their tests)
└── assets/       # design-presets.json — 29 font pairings, 24 palettes
```

`SKILL.md` covers the whole job in order: route the request, collect the creative brief, acquire assets, time the narration, hand off to the animation engine (Remotion or HyperFrames), mix and caption, verify, deliver, revise. Nested engine docs use `GUIDE.md` as their entry file name, and every path inside the guide resolves relative to the skill folder.

## A smaller copy for upload-limited platforms

Some platforms cap the number of files or the size of each one. To build a knowledge-only copy that fits, flatten `references/<group>/<name>/GUIDE.md` into `references/<group>--<name>.md`, keep only the `.md` knowledge files, and split any module over ~100 KB into `<name>--part2.md` continuations. Helper scripts, HTML templates, and JSON data can then be fetched from this repository instead of bundled:

```
https://raw.githubusercontent.com/priceriteprinters-cell/video-skills/main/<path>
```

## Notes

- Example media (png, fonts, mp3) referenced by the upstream engine docs was not bundled; fetch or generate replacements.
- The Remotion and HyperFrames docs were originally written as separate upstream skills; `SKILL.md` includes the path translation rules so their internal references still resolve here.
- Rendering MP4 needs Node + Chromium (`npx remotion render`) or Remotion Lambda — not a Worker runtime.
