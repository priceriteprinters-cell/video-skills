# Production-Ready Standards and Premium Motion

## Contents

- Art-direction bar
- Motion technique palette
- Animation intensity levels
- Asset quality gate
- Zero-placeholder rule
- Automated content scan
- Final full-length review
- Delivery package

## Art-direction bar

The result must read as intentionally designed by an experienced motion designer — not a template slideshow. Define, before handoff, a short style sheet: type scale, palette roles, grid/safe areas, corner radii, stroke weights, icon style, shadow/lighting model, easing curves, transition family, and pacing rules. Every scene follows it.

Every animation must serve communication: reveal order follows narration order, emphasis lands on the spoken keyword, and motion never competes with reading.

## Motion technique palette

Choose techniques per scene from this list according to purpose; do not use them all everywhere:

- Kinetic typography: per-word/per-line reveals timed to word timestamps, masked slides, weight/scale emphasis on keywords.
- Seamless transitions: match cuts on shape/color, masked wipes, morphs, camera push-through; one coherent transition family.
- Cinematic camera: slow push/pan, parallax layers (3+ depth planes), depth-of-field blur on background planes.
- Animated SVG: path draw-on, morphing icons, Lucide/Simple Icons strokes animated consistently.
- Infographics: animated counters, bar/line/donut charts drawn from verified data, labeled with source.
- Layering: masks, shape mattes, gradients, soft shadows, light sweeps, subtle grain/texture for depth.
- Sound design: whooshes on transitions, ticks on counters, soft hits on reveals; music ducked under narration.
- Rhythm: cuts and accents on narration phrase boundaries or musical beats; hold key text long enough to read.

Easing: prefer cubic/expo ease-out for entrances, ease-in for exits, spring with low overshoot for UI-like elements. Avoid linear motion except for continuous drift.

## Animation intensity levels

Ask (or default) during briefing:

| Level | Character |
|---|---|
| Subtle | Fades, gentle slides, minimal camera; corporate, health, finance |
| Balanced (default) | Kinetic type, parallax, purposeful transitions |
| Energetic | Fast cuts, bold scale/rotation, beat-synced accents; social, gaming, promos |

## Asset quality gate

For every asset, before composition:

1. Inspect at 100% and at final on-screen size: sharpness, resolution ≥ displayed pixel size (×2 for logos/text where possible), clean alpha edges, no stray text or artifacts, consistent style.
2. Blurry or low-res: first search for a better original (official press kit, SVG, higher-res source); only then AI-enhance or regenerate.
3. Missing: generate a replacement with the image-generation tool as high-quality PNG (transparent when used as a cutout); inspect and repair.
4. Never generate, redraw, or "enhance" an official logo into something new. Use the authentic file or a neutral wordmark/diagram, clearly not posing as the brand.
5. Prefer SVG for vector elements (icons, logos, diagrams); generated rasters are PNG.
6. Organize: `assets/<category>/<scene-id>_<slug>.<ext>` plus `assets/manifest.json` with source URL, license, attribution, dimensions, provenance (authentic / downloaded / generated / enhanced), and review status.

Do not start final composition while any required asset row is missing or unreviewed.

## Zero-placeholder rule

The export must contain none of:

- Placeholder copy (lorem ipsum, "your text here", "insert title", "TBD", "TODO", "sample", "XXX").
- Developer notes, debug overlays, frame counters, safe-area guides, temporary labels, console text.
- Missing/broken images, fallback-font boxes (tofu), clipped or overflowing text, misaligned elements.
- Unauthorized watermarks (stock previews, generator marks).
- Unintended black/blank frames, empty scenes, dead air, abrupt cuts.
- Spelling errors, wrong subtitles, unexplained abbreviations.

## Automated content scan

Run the bundled scanner over composition source, captions, and storyboard text before rendering and again on any extracted on-screen text:

```bash
python scripts/production_check.py scan <project-dir-or-files...>
python scripts/production_check.py blackframes OUTPUT.mp4   # needs ffmpeg
```

`scan` reports placeholder phrases, TODO/FIXME/debug markers, and references to local asset files that do not exist. `blackframes` reports black or frozen-blank stretches. A clean scan is necessary, not sufficient: visual review still decides.

## Final full-length review

Review the actual rendered file, start to end, not only the composition source:

- Extract frames at every scene start/middle/end and at each text peak; inspect for clipping, alignment, safe areas, sharpness, contrast, tofu.
- Watch/scrub transitions for smoothness and intent; check pacing feels natural.
- Check captions/text against narration timestamps and the approved script.
- Measure audio: integrated loudness (target about −14 LUFS for web/social, −16 for podcasts-style), true peak ≤ −1 dBTP, narration intelligible over music.
- Probe technical settings: resolution, fps, aspect ratio, codec (H.264/AAC MP4 by default), duration.
- Fix, re-render, and re-review. Repeat until clean. A successful render is not proof of correctness.

## Delivery package

Deliver, where applicable:

1. Final MP4.
2. Asset pack ZIP with `manifest.json` (sources, licenses, attribution).
3. Finalized script and transcript.
4. Project/source files when the environment produces editable sources.
5. Corrections and assumptions list (from the script audit).
6. Honest review statement: what was inspected (frames, motion, audio) and anything not verified.

Never claim something was created, inspected, or exported unless that actually happened.
