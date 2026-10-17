

<!-- ===== FILE: hyperframes/remotion-to-hyperframes/GUIDE.md ===== -->

---
name: remotion-to-hyperframes
description: 'Port an existing Remotion (React) composition''s source to HyperFrames HTML. Use ONLY on an explicit ask to port/convert/migrate/translate a Remotion source — one-way, Remotion-only. A passing Remotion mention, reference-only code, or "make something like my Remotion video" is a fresh build (/general-video). Unclear → /hyperframes.'
---

**Plugin installs:** Before setup or freshness commands, follow [plugin execution rules](../hyperframes/references/plugin-installation.md) when this skill is inside a HyperFrames plugin. Standalone installs keep the update instructions below.

> **First, keep this skill fresh — confirm with the user before running:** `npx hyperframes skills update remotion-to-hyperframes`. A fast no-op when everything is current; otherwise it refreshes this skill plus the core domain skills it depends on before you rely on them.

# Remotion to HyperFrames

> **The front door is `/hyperframes`.** Use this **only** to port an existing **Remotion** (React) composition's source into HyperFrames, one way. Authoring a **new** composition, re-creating from a non-Remotion source (After Effects, Framer Motion, plain React / CSS — there is no Remotion source to translate), a passing Remotion mention, or any uncertainty → read `/hyperframes` first: the intent layer owns every route decision.

## Overview

Translate Remotion (React-based) video compositions into HyperFrames (HTML + GSAP) compositions. Most Remotion idioms have direct HyperFrames equivalents — the translation is mechanical for ~80% of typical compositions. This skill encodes the mapping and guards against the lossy 20% by refusing to translate patterns that don't fit HF's seek-driven model and recommending the runtime interop pattern from [PR #214](https://github.com/heygen-com/hyperframes/pull/214) instead.

The skill ships with a **tiered test corpus** (T1–T4, 4 fixtures total) that grades translations against measured SSIM thresholds. Don't translate without running the eval — a translation that "looks right" but renders 0.05 SSIM lower than the validated baseline is silently wrong.

## When to use

**Use this skill ONLY when the user explicitly asks to migrate from Remotion.** Example trigger phrases:

- "port my Remotion project to HyperFrames"
- "convert this Remotion code to HyperFrames"
- "migrate from Remotion"
- "translate this Remotion comp"
- "rewrite this as HyperFrames HTML"

**Do NOT use this skill when:**

- (a) The user is authoring a **new** HyperFrames composition, even if they have or are A/B-testing a similar Remotion video.
- (b) The user mentions Remotion in passing without asking for migration.
- (c) The user shares Remotion code as reference material rather than asking for a translation.
- (d) The user asks for "the same video as my Remotion one" without explicitly asking to migrate the source — treat that as a fresh HyperFrames build.

**NOT SUPPORTED (decline — this is not what this skill does):**

- **The reverse direction.** Exporting a HyperFrames composition back out _to_ Remotion (or to any other framework) is not a workflow — the translation is Remotion → HyperFrames only. Say so plainly.
- **Non-Remotion sources.** An After Effects project (`.aep`), a Framer Motion / plain-React / CSS animation, or any other tool's source is not a Remotion composition — there is no Remotion source to translate. Re-create it natively via `/general-video`, or decline if HyperFrames can't represent it.

When in doubt, return to `/hyperframes`; its intent layer picks the route.

## Workflow

### Step 1: Lint the source

Run [`scripts/lint_source.py`](scripts/lint_source.py) over the Remotion source directory. The lint detects patterns that can't translate cleanly:

- **Blockers** (refuse + recommend interop): `useState`, `useReducer`, `useEffect`/`useLayoutEffect` with non-empty deps, async `calculateMetadata`, third-party React UI libraries (MUI, Chakra, Mantine, antd, shadcn, Radix, NextUI).
- **Warnings** (translate after dropping the construct): `@remotion/lambda` config, `delayRender`, `useCallback`, `useMemo`, custom hooks.
- **Info** (translate with note): `staticFile`, `interpolateColors`.

If any blocker fires, **stop**. Read [`references/escape-hatch.md`](references/escape-hatch.md) and surface the recommendation message. Warnings don't stop translation — drop the offending construct in step 3 and note the gap in `TRANSLATION_NOTES.md`. `@remotion/lambda` config is the canonical warning case: the skill drops the import + `renderMediaOnLambda(...)` calls but translates the rest of the composition.

### Step 2: Plan the translation

Read [`references/api-map.md`](references/api-map.md) — the index of every Remotion API and its HF equivalent or per-topic reference. Identify which topic references you'll need based on what the source uses:

| Source contains                                                           | Load reference                                |
| ------------------------------------------------------------------------- | --------------------------------------------- |
| `Composition`, `defaultProps`, `schema`, `calculateMetadata`              | [`parameters.md`](references/parameters.md)   |
| `Sequence`, `Series`, `Loop`, `AbsoluteFill`, `Freeze`                    | [`sequencing.md`](references/sequencing.md)   |
| `useCurrentFrame`, `interpolate`, `spring`, `Easing`, `interpolateColors` | [`timing.md`](references/timing.md)           |
| `Audio`, `Video`, `Img`, `IFrame`, `staticFile`, `delayRender`            | [`media.md`](references/media.md)             |
| `TransitionSeries`, `@remotion/transitions`                               | [`transitions.md`](references/transitions.md) |
| `@remotion/lottie`                                                        | [`lottie.md`](references/lottie.md)           |
| `@remotion/google-fonts/<Family>`, `Font.loadFont`, `@font-face`          | [`fonts.md`](references/fonts.md)             |

Don't load all of them — load only what the specific source needs.

**Search the live catalog for any visual effect the table does not map.** When the source paints a look with no HF API equivalent — a scanline/CRT overlay, a glitch or chromatic-aberration pass, a shader wipe, a film-grain treatment — run `npx hyperframes catalog --query "<the effect, in plain English>" --json` before hand-writing it in GSAP. The search needs **nothing installed**: no project, no prior `add`, no account. It ranks the whole hosted registry (~400 blocks and components) from any directory, and `transitions.md` already takes this route for `clockWipe()` / `iris()` via `npx hyperframes add sdf-iris`. A real component is closer to the source than a hand-approximation, so it usually raises the SSIM rather than lowering it — but the render diff in Step 4 is still the arbiter. Hand-write the effect when a search returns nothing that fits, and record the substitution in `TRANSLATION_NOTES.md` either way.

### Step 3: Generate the HF composition

Emit `index.html` with:

- Root `<div id="stage">` carrying the composition's `data-composition-id`, `data-start="0"`, `data-duration` (in seconds), `data-fps`, `data-width`, `data-height`, plus one `data-*` per scalar prop.
- One host `<div>` per scene with `data-composition-src="compositions/<scene>.html"` and `data-start` / `data-duration` / `data-track-index`. The root holds no nested layout.
- One `compositions/<scene>.html` per scene (a `<template>` sub-composition): its inline `<style>` for layout (CSS sets the `from` state of every animated property), its markup, and one paused `gsap.timeline({paused: true})` in the scene's local time. Every Remotion `useCurrentFrame()` derivation becomes a tween on that timeline at the offset within the scene.
- `window.__timelines["<scene-id>"] = tl;` in each scene file, and `window.__timelines["<composition-id>"]` for the root's own (possibly empty) timeline.

Custom React subcomponents inline as repeated HTML using the prop interface as the template (see [`parameters.md`](references/parameters.md) for the per-instance `data-*` pattern).

### Step 4: Validate

Run the eval harness — [`references/eval.md`](references/eval.md) for the full guide. Quick path:

```bash
# Render Remotion baseline (after npm install in the fixture)
cd remotion-src && npx remotion render <CompositionId> out/baseline.mp4

# Render HF translation
cd ../hf-src && npx hyperframes render --skill=remotion-to-hyperframes --output ../hf.mp4

# SSIM diff
../../scripts/render_diff.sh ./remotion-src/out/baseline.mp4 ./hf.mp4 ./diff
```

Threshold: ~0.02 below `p05` of the source's complexity tier (see `eval.md`'s validated thresholds table). If the diff fails, run [`scripts/frame_strip.sh`](scripts/frame_strip.sh) to see _which_ frames diverged, then re-read the relevant timing/sequencing/media reference.

**Critical**: both renders must use matching pixel format. Set `Config.setVideoImageFormat("png")` + `Config.setColorSpace("bt709")` in the Remotion source's `remotion.config.ts` — otherwise the diff measures encoder differences (~0.05 SSIM hit), not translation fidelity.

### Step 5: Document gaps

Anything that didn't translate cleanly (volume ramps dropped, custom presentations approximated, fonts substituted) gets a `TRANSLATION_NOTES.md` written next to the HF output. See [`references/limitations.md`](references/limitations.md) for the format.

## What this skill explicitly does NOT do

- **Translate React state machines.** Compositions that drive animation via `useState` + `useEffect` are not deterministic frame-capture targets in HyperFrames' seek-driven model. Recommend the runtime interop pattern.
- **Run Remotion's render pipeline alongside HyperFrames.** That's the runtime interop pattern from [PR #214](https://github.com/heygen-com/hyperframes/pull/214) — a separate solution for compositions that fail this skill's lint.

(`@remotion/lambda` is _not_ a blocker — Lambda config is deployment, not animation. The skill drops it as a warning and translates the rest. See [`references/escape-hatch.md`](references/escape-hatch.md).)

## How to grade your own translation

Run the test corpus orchestrator:

```bash
./assets/test-corpus/run.sh
```

It runs T1, T2, T3 (render + diff) and T4 (lint validation), prints a per-tier pass/fail table, and emits an aggregate JSON report. Use this to verify the skill is working end-to-end on a clean checkout — and as a regression check after editing any reference.

Validated baseline (as of 2026-04-27):

| Tier | Composition shape                           | Mean SSIM | Threshold |
| ---- | ------------------------------------------- | --------- | --------- |
| T1   | single-element fade-in                      | 0.974     | 0.95      |
| T2   | multi-scene + spring + audio + image        | 0.985     | 0.95      |
| T3   | data-driven, custom subcomponents, count-up | 0.953     | 0.90      |
| T4   | escape-hatch (8 lint cases)                 | 8/8 pass  | n/a       |


<!-- ===== FILE: hyperframes/remotion-to-hyperframes/assets/test-corpus/tier-1-title-card/README.md ===== -->

# Tier 1 — title-card-fade

## What it tests

The simplest non-trivial Remotion → HyperFrames translation. A single text
element fades in over the first 0.5 s, holds for 2.0 s, and fades out over
the last 0.5 s. No audio, no media, no custom components.

If a translation can't pass T1, it's broken on table-stakes basics:
`AbsoluteFill`, `useCurrentFrame`, `interpolate` with multi-segment input,
and the timing offset between Remotion's frame-based driver and HF's
paused-GSAP driver.

## Translation walk-through

| Remotion                                                      | HyperFrames                                                                                             |
| ------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------- |
| `<AbsoluteFill style={{ backgroundColor: "#0a0a0a" }}>`       | `<body style="background: #0a0a0a">` + a positioned root div                                            |
| `useCurrentFrame()`                                           | dropped — HF seeks the timeline                                                                         |
| `interpolate(frame, [0, 15, 75, 90], [0, 1, 1, 0])` at fps=30 | `gsap.timeline({ paused: true })` with three `.to()` calls at offsets 0s/0.5s/2.5s, each `ease: "none"` |
| `<div style={{ opacity }}>HELLO</div>`                        | static markup; opacity is animated by the timeline                                                      |

The Remotion→HF time conversion is `time = frame / fps`. So
`[0, 15, 75, 90]` at 30 fps becomes `[0, 0.5, 2.5, 3.0]` seconds.

## How to render and evaluate

```bash
# Render Remotion baseline
cd remotion-src && npm install && npm run render
# Renders to remotion-src/out/baseline.mp4

# Render HyperFrames translation
cd ../hf-src && npx hyperframes render --output ../hf.mp4

# Compare with the eval harness (from skill scripts/)
../../../scripts/render_diff.sh ./remotion-src/out/baseline.mp4 ./hf.mp4 ./diff
```

`expected.json` documents the SSIM threshold (0.95) for this fixture; the
calibrated mean against Remotion @ 4.0 with PNG/BT.709 output is 0.974.


<!-- ===== FILE: hyperframes/remotion-to-hyperframes/assets/test-corpus/tier-2-multi-scene/README.md ===== -->

# Tier 2 — title-image-outro

## What it tests

Three-scene composition. Each scene exercises a different Remotion idiom:

1. **Scene 1 (0–2 s)** — TitleScene with `spring({damping:12, stiffness:100, mass:1})`
   driving a `transform: scale()` on text. Tests the lossy `spring → GSAP ease` translation.
2. **Scene 2 (2–4 s)** — ImageScene that fades in a `staticFile`-loaded image and
   linearly scales it from 0.8 → 1.0. Tests asset paths + linear `interpolate`.
3. **Scene 3 (4–6 s)** — OutroScene with a 1-s linear fade-in. Sanity check after
   the harder scenes.

A silent 6-second WAV plays throughout at `volume={0.5}`. Tests `<Audio>` translation.

If a translation passes T2, the skill correctly handles `<Sequence>` boundaries,
`<Audio>` / `<Img>` / `staticFile`, and the Remotion `spring → GSAP ease` heuristic.

## Translation walk-through

| Remotion                                                            | HyperFrames                                                                                                         |
| ------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------- |
| `<Sequence from={0} durationInFrames={60}>`                         | host `<div data-composition-src="compositions/scene-1.html" data-start="0" data-duration="2" data-track-index="0">` |
| `spring({frame, fps, config: {damping:12, stiffness:100, mass:1}})` | `gsap.to(target, { scale: 1, duration: 0.7, ease: "back.out(1.4)" })`                                               |
| `<Audio src={staticFile("music.wav")} volume={0.5} />`              | `<audio src="assets/music.wav" data-start="0" data-duration="6" data-volume="0.5" data-track-index="1">`            |
| `<Img src={staticFile("square.png")} />`                            | `<img src="../assets/square.png">` inside `compositions/scene-2.html` (with setup.sh copying into both trees)       |
| `interpolate(frame, [0, 15], [0, 1])` at 30 fps                     | `gsap.to(target, { opacity: 1, duration: 0.5, ease: "none" })`                                                      |

The scene crossfading is a HyperFrames idiom, not a Remotion one: at scene boundaries
each scene sub-composition sets its own `gsap.set(scene, { opacity: 0 })` at its local end so the scene disappears at the
right time. Remotion does this implicitly by virtue of `<Sequence>`'s durationInFrames.

## How to render and evaluate

```bash
# 1. Generate the binary assets (PNG + WAV) via ffmpeg
./setup.sh

# 2. Render Remotion baseline
cd remotion-src && npm install && npm run render

# 3. Render HyperFrames translation
cd ../hf-src && npx hyperframes render --output ../hf.mp4

# 4. Compare
../../../scripts/render_diff.sh ./remotion-src/out/baseline.mp4 ./hf.mp4 ./diff
```

## Why threshold 0.95?

Same threshold as T1 (`expected.json` codifies it for the orchestrator). Spring → `back.out(1.4)`
came in cleaner than predicted during calibration — the validated mean is 0.985 against the
0.95 gate. If the translation breaks anything else (spring overshoot wrong, stagger off,
asset path drift), mean SSIM will fall well below 0.95 — that's the failure signal.


<!-- ===== FILE: hyperframes/remotion-to-hyperframes/assets/test-corpus/tier-3-data-driven/README.md ===== -->

# Tier 3 — stargazed-data-driven

## What it tests

A purpose-built data-driven fixture that exercises the realistic shape of a
production Remotion composition without using the runtime adapter from
PR #214. If a translation passes T3, the skill correctly handles:

- A `<Composition>` with a `z.object` schema and typed `defaultProps`
- Custom React subcomponents reused with different props across scenes
- A nested data structure (`stats[]`) materialized as repeated HTML with
  per-instance attributes
- A frame-driven count-up animation (`AnimatedNumber` → GSAP `onUpdate`)
- Two different `spring` configs translated to two different `back.out` overshoots
- Per-instance delays via component props (`delayInFrames` → GSAP timeline offsets)

## Composition shape

```
Stargazed (10 s @ 30 fps, 1280×720)
├── Sequence 0–3 s   TitleScene
│                    ├── title  ← spring scale
│                    └── subtitle ← linear fade
├── Sequence 3–7 s   StatsScene
│                    ├── StatCard "Stars" 1247 #fbbf24 (delay 0 frames)
│                    ├── StatCard "Forks" 312 #60a5fa  (delay 12 frames)
│                    └── StatCard "Issues" 48 #f87171  (delay 24 frames)
└── Sequence 7–10 s  OutroScene
                     └── UnderlinedText "thanks for watching" ← scale-in underline
```

Each `StatCard` is a custom subcomponent that internally uses `AnimatedNumber`
to count from 0 to the target. `AnimatedNumber` itself derives the displayed
value from `useCurrentFrame()` + a manual `1 - (1 - t)^3` ease.

## The lossy parts (and why threshold = 0.90)

1. **`spring → back.out(N)`**: two different spring configs in this composition.
   - `{ damping: 12, stiffness: 100, mass: 1 }` (title) → `back.out(1.4)`
   - `{ damping: 14, stiffness: 90, mass: 1 }` (stat card) → `back.out(1.2)`

   Overshoot ratio (1.4 vs 1.2) approximates the damping difference. The
   late-tail curve of GSAP's back ease and Remotion's spring don't match
   exactly — costs ~0.03 mean SSIM per spring instance.

2. **Count-up easing**: `AnimatedNumber` uses `1 - (1 - t)^3` (cubic ease-out)
   manually computed in the component. GSAP's `power3.out` is the same curve
   shape — should match closely. The displayed integer is rounded each frame
   in both renderers; minor mismatches occur when the rounded value flips
   between two numbers on a sub-frame timing difference.

3. **Font rendering**: same caveat as T1/T2. System Helvetica/Arial fallback
   produces minor anti-aliasing differences between renderers. Affects the
   stat card numbers (large weight 800) most.

A mean SSIM below 0.90 in T3 indicates a _structural_ mismatch (wrong scene
durations, wrong stagger timing, missing prop wiring), not approximation
drift. That's the failure signal we care about. The calibrated mean against
Remotion @ 4.0 with PNG/BT.709 output is 0.953.

## Translation walk-through (skill cheat sheet)

| Remotion                                                                    | HyperFrames                                                                           |
| --------------------------------------------------------------------------- | ------------------------------------------------------------------------------------- |
| `<Composition schema={z.object({...})} defaultProps={...} />`               | data-\* attributes on root `#stage` div                                               |
| nested array prop (`stats[]`)                                               | repeated HTML markup with per-instance `data-*` attrs                                 |
| custom React subcomponent                                                   | inline repeated HTML using the component's prop interface as the template             |
| `<AnimatedNumber from={0} to={value} dur={45} />` (cubic ease-out count-up) | tween on `{ v: 0 }` object with `onUpdate` rewriting `textContent`, ease `power3.out` |
| `spring({damping:12, stiffness:100})`                                       | `back.out(1.4)` over ~0.7 s                                                           |
| `spring({damping:14, stiffness:90})`                                        | `back.out(1.2)` over ~0.7 s                                                           |
| `delayInFrames={i * 12}` (per-instance)                                     | GSAP timeline offset `(i * 0.4)` s                                                    |
| `useVideoConfig()` to get `fps`                                             | dropped — composition fps is in `data-fps` on `#stage`                                |

## How to render and evaluate

```bash
# Render Remotion baseline (no setup.sh — no binary assets in this fixture)
cd remotion-src && npm install && npm run render

# Render HyperFrames translation
cd ../hf-src && npx hyperframes render --output ../hf.mp4

# Compare
../../../scripts/render_diff.sh ./remotion-src/out/baseline.mp4 ./hf.mp4 ./diff
```


<!-- ===== FILE: hyperframes/remotion-to-hyperframes/assets/test-corpus/tier-4-escape-hatch/README.md ===== -->

# Tier 4 — escape-hatch

## What it tests

T4 is the **lint-only** tier. There are no renders to diff — the skill is
graded on whether it correctly _refuses_ to translate each case (and
recommends the runtime interop pattern from PR #214 instead) or, where
appropriate, translates after dropping warning-level decorations.

Each `cases/*.tsx` file is a minimal Remotion composition that
demonstrates one specific pattern. The skill should:

1. Run `scripts/lint_source.py` over the source.
2. Compare the JSON output to `expected.json` for that case.
3. Take the documented `skill_action`:
   - `refuse_translation_recommend_interop` — print the rationale + link to
     the PR #214 interop guide; do not produce HF output.
   - `drop_lambda_code_translate_remainder_if_clean` — drop the
     `@remotion/lambda` code with a note; translate the rest only if no
     other blockers are present.
   - `translate_after_dropping_wrappers` — translate normally; drop
     `useCallback` / `useMemo` / `delayRender` wrappers.
   - `inline_hook_body_if_pure` — inline the custom hook's body if it's a
     pure derivation of `useCurrentFrame`; otherwise bow out.

## Cases

| #   | File                       | Expected finding                    | Notes                                           |
| --- | -------------------------- | ----------------------------------- | ----------------------------------------------- |
| 01  | `01-use-state.tsx`         | blocker `r2hf/use-state`            | useState driving animation                      |
| 02  | `02-use-effect-deps.tsx`   | blocker `r2hf/use-effect-deps`      | useEffect/useLayoutEffect with non-empty deps   |
| 03  | `03-async-metadata.tsx`    | blocker `r2hf/async-metadata`       | calculateMetadata returns a Promise             |
| 04  | `04-third-party-react.tsx` | blocker `r2hf/third-party-react-ui` | imports `@mui/material`                         |
| 05  | `05-lambda-config.tsx`     | warning `r2hf/lambda-import`        | imports `@remotion/lambda` — drops, translates  |
| 06  | `06-warnings-only.tsx`     | warnings only                       | delayRender / useCallback / useMemo             |
| 07  | `07-custom-hook.tsx`       | warning `r2hf/custom-hook`          | locally-defined `useFadeIn` (export const form) |
| 08  | `08-mixed.tsx`             | 3 blockers + 1 warning              | aggregate-findings test                         |

## Validation

```bash
./validate.sh
```

The script runs `lint_source.py` against each case and asserts:

- Each expected blocker rule fires with severity `blocker`.
- Each expected warning rule fires with severity `warning` (or stronger).
- `lint_source.py`'s exit code is 1 when blockers are expected, 0 otherwise.

T4 passes when every case matches its expected output. No renders involved.


<!-- ===== FILE: hyperframes/remotion-to-hyperframes/references/api-map.md ===== -->

# Remotion → HyperFrames API Map

Authoritative translation table. Load this reference when starting a translation
to know the high-level mapping; load the per-topic references for fragile
details (timing, transitions, etc.).

## Reading this table

- **`drop`** = remove from output entirely. The HF runtime handles it.
- **`see references/X.md`** = the mapping is non-trivial; read the linked file.
- **`refuse + interop`** = the skill bows out and recommends the runtime adapter
  pattern from [PR #214](https://github.com/heygen-com/hyperframes/pull/214).

## Composition root

| Remotion                                             | HyperFrames                                                                                                          |
| ---------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------- |
| `<Composition id durationInFrames fps width height>` | root `<div id="stage" data-composition-id data-start="0" data-duration="<dur/fps>" data-fps data-width data-height>` |
| `defaultProps={...}`                                 | `data-*` attributes on `#stage` (one per scalar prop). Nested objects/arrays — see [parameters.md](parameters.md)    |
| `schema={z.object(...)}`                             | not represented in HTML; the schema lives in the agent's translation step only                                       |
| `calculateMetadata` (sync)                           | resolve at translation time, write concrete values into `data-*`                                                     |
| `calculateMetadata` (async)                          | **refuse + interop** — see [escape-hatch.md](escape-hatch.md)                                                        |
| `registerRoot(RemotionRoot)`                         | drop                                                                                                                 |
| `<AbsoluteFill style>`                               | `<div style="position:absolute;inset:0;{style}">`                                                                    |

## Sequencing

See [sequencing.md](sequencing.md) for nesting and stagger details.

| Remotion                                   | HyperFrames                                                                                                                                                                                                                 |
| ------------------------------------------ | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `<Sequence from={F} durationInFrames={D}>` | a host `<div data-composition-src="compositions/<name>.html" data-start="<F/fps>" data-duration="<D/fps>" data-track-index="N">` in the root, its content in that sub-composition file (see [sequencing.md](sequencing.md)) |
| `<Series>` + `<Series.Sequence>`           | sibling scene hosts with sequential `data-start` values                                                                                                                                                                     |
| `<Loop durationInFrames={D}>`              | not a primitive — emit a bounded GSAP repeat from the available duration                                                                                                                                                    |
| `<Freeze frame={F}>`                       | drop the wrapper; HF doesn't have running animation outside the seek-driven timeline so freeze is a no-op                                                                                                                   |

## Timing

See [timing.md](timing.md) — this is the highest-leverage section.

| Remotion                                                   | HyperFrames                                                                                                        |
| ---------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------ |
| `useCurrentFrame()`                                        | drop — HF seeks the timeline. The math derived from `frame` becomes an animatable property of a paused GSAP tween. |
| `useVideoConfig()` for `fps` / `durationInFrames`          | drop — read from `data-fps` / `data-duration` on `#stage`                                                          |
| `interpolate(frame, [a,b], [x,y])` (linear)                | `gsap.fromTo(t, {p:x}, {p:y, duration:(b-a)/fps, ease:"none"})` at offset `a/fps`                                  |
| `interpolate(frame, [a,b,c,d], [x,y,y,z])` (multi-segment) | three `gsap.to` calls at offsets `a/fps`, `b/fps`, `c/fps`                                                         |
| `interpolate(..., {easing: Easing.bezier})`                | GSAP `CustomEase.create("c", "M0,0 C${a},${b} ${c},${d} 1,1")`                                                     |
| `spring({frame, fps, config: {damping, stiffness, mass}})` | GSAP `back.out(N)` — see [timing.md](timing.md) for damping → overshoot table                                      |
| `interpolateColors(frame, range, colors)`                  | `gsap.to({...}, { backgroundColor, color, duration, ease })` — GSAP handles color tweens natively                  |
| `Easing.in / .out / .inOut(power)`                         | GSAP `power<N>.in` / `power<N>.out` / `power<N>.inOut`                                                             |

## Media

See [media.md](media.md) for trim, volume ramps, and decoder notes.

| Remotion                               | HyperFrames                                                                                                                                                                                                                                                                                                                                  |
| -------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `<Audio src volume>`                   | `<audio data-start data-duration data-track-index data-volume src>`                                                                                                                                                                                                                                                                          |
| `<Audio playbackRate startFrom endAt>` | `data-playback-rate`, `data-trim-start`, `data-trim-end`                                                                                                                                                                                                                                                                                     |
| `<Video src>`                          | `<video playsinline data-has-audio="true" data-start data-duration data-track-index src>` only when the file has an audio stream (check with `ffprobe -v error -select_streams a -show_entries stream=codec_type -of csv=p=0 <file>`: non-empty means it has audio) and the source is not `muted` or `volume={0}`; otherwise `muted` instead |
| `<OffthreadVideo>`                     | `<video>` — HF doesn't need the off-thread variant (uses headless Chrome)                                                                                                                                                                                                                                                                    |
| `<Img src>`                            | `<img>`                                                                                                                                                                                                                                                                                                                                      |
| `<IFrame src>`                         | `<iframe>` — HF auto-falls back to screenshot mode for nested iframes                                                                                                                                                                                                                                                                        |
| `staticFile("x.png")`                  | `"assets/x.png"` in the root, `"../assets/x.png"` inside a `compositions/` scene file — copy the file into `hf-src/assets/` next to `index.html`                                                                                                                                                                                             |
| `delayRender()` / `continueRender()`   | drop — HF waits on asset readiness via the Frame Adapter pattern                                                                                                                                                                                                                                                                             |

## Transitions

See [transitions.md](transitions.md).

| Remotion                                                                       | HyperFrames                                                                                               |
| ------------------------------------------------------------------------------ | --------------------------------------------------------------------------------------------------------- |
| `<TransitionSeries>` + `<TransitionSeries.Transition presentation={fade()} />` | manual `gsap.to(scene, {opacity: 0/1, duration})` crossfade at the boundary                               |
| `slide()`, `wipe()`, `clockWipe()`, `fade()`                                   | HF [shader-transitions](https://hyperframes.heygen.com/catalog/blocks) package presets — pick the closest |
| `linearTiming({durationInFrames})`                                             | duration in seconds (`/fps`)                                                                              |
| `springTiming({config})`                                                       | duration in seconds, ease `back.out` — see [timing.md](timing.md)                                         |

## Lottie

See [lottie.md](lottie.md).

| Remotion                        | HyperFrames                                                                                                       |
| ------------------------------- | ----------------------------------------------------------------------------------------------------------------- |
| `<Lottie animationData={data}>` | `<div id="lottie-N">` + `<script>const anim = lottie.loadAnimation({...}); window.__hfLottie.push(anim)</script>` |
| `loop` / `playbackRate` props   | translate only after checking player seek behavior; HF adapter seeks absolute time via `goToAndStop`              |
| `@remotion/lottie` runtime      | `lottie-web` from CDN — drop the React wrapper                                                                    |

## Fonts

See [fonts.md](fonts.md).

| Remotion                                            | HyperFrames                                                                                 |
| --------------------------------------------------- | ------------------------------------------------------------------------------------------- |
| `loadFont()` from `@remotion/google-fonts/<Family>` | `@font-face` rule referencing the Google Fonts CSS, OR `<link>` to Google Fonts in `<head>` |
| Local font via `@font-face`                         | same — paste the rule into `<style>`                                                        |
| System font fallback                                | document the font-fallback divergence cost (see [eval.md](eval.md))                         |

## Parameters

See [parameters.md](parameters.md).

| Remotion                      | HyperFrames                                                                                   |
| ----------------------------- | --------------------------------------------------------------------------------------------- |
| `z.object({foo: z.string()})` | `data-foo` on `#stage` (the schema is implicit in HTML structure)                             |
| nested array prop (`stats[]`) | repeated HTML markup with per-instance `data-*` attrs                                         |
| Zod default values            | bake defaults into the HTML directly                                                          |
| Zod runtime validation        | not represented; if validation matters, validate in the translation step before emitting HTML |

## React patterns

| Remotion                                           | HyperFrames                                                      |
| -------------------------------------------------- | ---------------------------------------------------------------- |
| Custom React subcomponent (pure, prop-driven)      | inline as repeated HTML using the prop interface as the template |
| `useState` driving animation                       | **refuse + interop**                                             |
| `useReducer` driving animation                     | **refuse + interop**                                             |
| `useEffect(fn, [deps])` (non-empty deps)           | **refuse + interop**                                             |
| `useEffect(fn, [])` (mount-once side effect)       | drop the effect; use `queueMicrotask` if startup work is needed  |
| `useCallback`, `useMemo`                           | drop the wrappers — decorative                                   |
| Custom hook (pure derivation of `useCurrentFrame`) | inline the body                                                  |
| Custom hook with state/effects                     | refuse + interop                                                 |

## Distributed rendering

`@remotion/lambda` and `@remotion/cloudrun` are deployment configuration —
orthogonal to the rendered composition itself. The skill emits these as
**warnings** (not blockers) and drops them in step 3 (Generate) with a note
in `TRANSLATION_NOTES.md`. HF is single-machine today; document the gap.

| Remotion                   | HyperFrames                                            |
| -------------------------- | ------------------------------------------------------ |
| `@remotion/lambda` import  | drop the import (warning `r2hf/lambda-import`)         |
| `renderMediaOnLambda(...)` | drop the call; note in `TRANSLATION_NOTES.md`          |
| `@remotion/cloudrun`       | drop the import + call; note in `TRANSLATION_NOTES.md` |

## When to bow out entirely

If any blocker pattern is present, recommend the runtime interop pattern from
[PR #214](https://github.com/heygen-com/hyperframes/pull/214) instead of
attempting translation. See [escape-hatch.md](escape-hatch.md).

The blockers are documented in [`scripts/lint_source.py`](../scripts/lint_source.py)
and tested by [tier-4-escape-hatch](../assets/test-corpus/tier-4-escape-hatch/).


<!-- ===== FILE: hyperframes/remotion-to-hyperframes/references/escape-hatch.md ===== -->

# When to bow out: the runtime interop pattern

Some Remotion compositions can't be translated cleanly. The skill should
recognize them upfront and recommend the **runtime interop pattern** from
[PR #214](https://github.com/heygen-com/hyperframes/pull/214) instead of
producing broken HTML.

## When to recommend interop

Run `scripts/lint_source.py` first. If it returns any blocker, recommend
interop. The blockers are:

| Rule                        | What it catches                                                |
| --------------------------- | -------------------------------------------------------------- |
| `r2hf/use-state`            | useState driving animation                                     |
| `r2hf/use-reducer`          | useReducer driving animation                                   |
| `r2hf/use-effect-deps`      | useEffect/useLayoutEffect with non-empty deps (side effects)   |
| `r2hf/async-metadata`       | calculateMetadata returns a Promise                            |
| `r2hf/third-party-react-ui` | Imports from MUI, Chakra, Mantine, antd, shadcn, Radix, NextUI |

Each of these breaks the seek-driven, deterministic-frame model that HF
relies on. Translating them produces silently-wrong output.

## What the interop pattern actually does

Per [PR #214](https://github.com/heygen-com/hyperframes/pull/214), the
runtime adapter:

1. Bundles the user's Remotion code with React + `@remotion/player` via esbuild.
2. Mounts a Remotion `<Player>` inside an HF composition's HTML.
3. Pauses the player on mount.
4. Registers the player on `window.__hfRemotion` with `seekTo(frame)`,
   `pause()`, `durationInFrames`, `fps`.
5. HF's render loop seeks the player frame-by-frame via `seekTo(frame)`.

Result: Remotion's React tree renders at HF's deterministic frame ticks.
Custom hooks, useState, useEffect, MUI components — all work because
Remotion's React reconciler is doing the rendering.

## The recommendation message

When the skill detects a blocker, output something like:

> The Remotion source uses `useState` (and others), which can't be
> translated to HF's seek-driven HTML model. The recommended path is the
> **runtime interop pattern**: bundle your Remotion code with `@remotion/player`
> and let HF drive it frame-by-frame.
>
> See https://github.com/heygen-com/hyperframes/pull/214 for the full
> implementation. Quick summary:
>
> 1. Bundle `entry.tsx` with esbuild: `npx esbuild entry.tsx --bundle --outfile=dist/bundle.js --format=iife --jsx=automatic`
> 2. Mount the Player and register on `window.__hfRemotion`:
>
>    ```tsx
>    const playerRef = useRef<PlayerRef>(null);
>    useEffect(() => {
>      playerRef.current?.pause();
>      window.__hfRemotion = window.__hfRemotion || [];
>      window.__hfRemotion.push({
>        seekTo: (f) => playerRef.current?.seekTo(f),
>        pause: () => playerRef.current?.pause(),
>        durationInFrames,
>        fps,
>      });
>    }, []);
>    ```
>
> 3. Reference the bundle from your HF `index.html` and render normally:
>    `<script src="dist/bundle.js"></script>`

## The lint output already includes recommendations

`lint_source.py` emits a `recommendation` field per finding. Surface those
verbatim — they're tuned per blocker rule:

```json
{
  "rule": "r2hf/use-state",
  "message": "useState detected — Remotion compositions that drive animation via React state are not deterministic frame-capture targets in HyperFrames",
  "recommendation": "Use the runtime interop pattern from PR #214 instead of attempting a translation"
}
```

## When NOT to bow out: warnings only

Some patterns produce warnings, not blockers — translate after dropping
the wrappers:

| Rule                      | Action                                                              |
| ------------------------- | ------------------------------------------------------------------- |
| `r2hf/lambda-import`      | drop the `@remotion/lambda` config; HF runs single-machine, log gap |
| `r2hf/delay-render`       | drop the call; HF handles asset readiness                           |
| `r2hf/use-callback`       | drop the wrapper, inline the function                               |
| `r2hf/use-memo`           | drop the wrapper, compute inline                                    |
| `r2hf/custom-hook` (pure) | inline the hook body if it's a derivation of `useCurrentFrame`      |
| `r2hf/static-file`        | replace `staticFile("x")` with `"assets/x"`                         |
| `r2hf/interpolate-colors` | translate to GSAP color tween (see [timing.md](timing.md))          |

These are documented in T4 cases 05–07.

`r2hf/lambda-import` is a warning — not a blocker — because Lambda
configuration is orthogonal to the rendered composition. Translating an
otherwise-clean Remotion comp shouldn't fail just because the author also
configured AWS Lambda for distributed rendering. The skill drops the
`@remotion/lambda` imports and `renderMediaOnLambda(...)` calls in step 3
(Generate) and writes a `TRANSLATION_NOTES.md` entry so the user knows to
set up HF rendering separately.

## When the source has BOTH blockers AND warnings

Bow out. The presence of a single blocker means the skill shouldn't
attempt translation — even if the rest of the composition is clean.
The user should use interop for the whole thing OR refactor the
blocker patterns out of their Remotion source first.


<!-- ===== FILE: hyperframes/remotion-to-hyperframes/references/eval.md ===== -->

# Eval: how to validate a translation end-to-end

Every translation should be measured. The skill ships three scripts and
a tiered test corpus that, together, gate translation quality.

## The three scripts

| Script                   | Input                       | Output                                                              |
| ------------------------ | --------------------------- | ------------------------------------------------------------------- |
| `scripts/lint_source.py` | Remotion source dir or file | JSON findings + exit code (0 clean, 1 has blockers)                 |
| `scripts/render_diff.sh` | two MP4 paths               | per-frame SSIM + JSON summary (`mean`, `min`, `p05`, `p95`, `pass`) |
| `scripts/frame_strip.sh` | two MP4 paths               | side-by-side comparison strip PNG for visual debugging              |

Run them in this order: **lint → render → diff → (if fail) strip**.

## Per-fixture flow

```bash
# 1. Lint the source — blockers mean stop
python3 ../../scripts/lint_source.py ./remotion-src/src/

# 2. Generate any binary assets (T2+T3 only)
[ -f setup.sh ] && ./setup.sh

# 3. Render Remotion baseline
cd remotion-src && npm install && npm run render
# -> remotion-src/out/baseline.mp4

# 4. Render HF translation
cd .. && node ../../../packages/cli/dist/cli.js render hf-src/ --output hf.mp4
# -> hf.mp4

# 5. SSIM diff
../../scripts/render_diff.sh ./remotion-src/out/baseline.mp4 ./hf.mp4 ./diff
# -> diff/summary.json

# 6. If diff fails, generate frame strip for visual inspection
../../scripts/frame_strip.sh ./remotion-src/out/baseline.mp4 ./hf.mp4 ./strip 8
# -> strip/strip.png
```

## Reading `diff/summary.json`

```json
{
  "frame_count": 90,
  "mean": 0.974,
  "min": 0.972,
  "max": 0.999,
  "p05": 0.972,
  "p95": 0.983,
  "threshold": 0.95,
  "pass": true
}
```

| Field         | What it tells you                                                           |
| ------------- | --------------------------------------------------------------------------- |
| `mean`        | average SSIM across all frames; the headline number                         |
| `min`         | worst frame; below threshold means at least one frame is structurally wrong |
| `p05` / `p95` | 5th / 95th percentile — most frames sit between these                       |
| `threshold`   | from `R2HF_SSIM_THRESHOLD` env var (default 0.85)                           |
| `pass`        | whether `mean >= threshold`                                                 |

## Validated tier thresholds

Calibrated against actual Remotion + HF renders:

| Tier | Composition shape                           | Mean  | Threshold | Margin |
| ---- | ------------------------------------------- | ----- | --------- | ------ |
| T1   | single-element fade-in                      | 0.974 | 0.95      | +0.022 |
| T2   | multi-scene + spring + audio + image        | 0.985 | 0.95      | +0.016 |
| T3   | data-driven, custom subcomponents, count-up | 0.953 | 0.90      | +0.038 |

Each fixture's `expected.json` carries:

- `ssim_threshold` — the gate for `pass`
- `validation` — the actual measured numbers from the calibration run
- `translation_notes` — what's lossy and why

## Critical: encoder config

Both Remotion and HF must output the same pixel format for SSIM to be
meaningful. Remotion's default JPEG output writes `yuvj420p` (full-range);
HF outputs `yuv420p` (limited-range). The mismatch costs ~0.05 SSIM.

Every fixture's `remotion.config.ts` sets:

```ts
Config.setVideoImageFormat("png");
Config.setColorSpace("bt709");
```

If the user's source doesn't have these, add them in the translation
step — otherwise the diff measures encoder differences, not translation
fidelity.

## What the noise floor looks like

The dominant non-translation noise is **system font fallback divergence**.
Remotion's bundled Chromium and HF's `chrome-headless-shell` interpret
`font-weight: 800` differently when there's no real font installed:

- Remotion HELLO at 160px: medium-weight stroke
- HF HELLO at 160px: heavy-weight stroke

This costs ~0.025 mean SSIM. Visible in T1's frame strip.
[fonts.md](fonts.md) covers how to mitigate (use Inter, load explicit
Google Fonts).

## Threshold rule of thumb

Set the threshold ~0.02 below measured `p05`:

- Real translation regressions drop mean by 0.05+ — caught.
- Encoder/font drift between CI runs is bounded at ~0.01 — not caught.

If a calibration run's measured mean is far above your initial threshold
guess, _don't_ tighten the threshold to fit. Leave headroom — fixtures
re-rendered on different hardware will drift.

## When the diff fails

1. **Look at `frame_strip.sh` output first.** A side-by-side strip at 6–10
   evenly-spaced timestamps shows whether the failure is structural
   (wrong scene durations, missing element) or cosmetic (different font
   weight, slight timing skew).
2. **Check `diff/ssim.log`.** Per-frame SSIM tells you _which_ frames
   failed. Cluster of bad frames in the middle of a scene = animation
   problem; bad frames at scene boundaries = sequencing problem.
3. **Re-read the relevant reference.** [timing.md](timing.md) for
   spring/easing issues, [sequencing.md](sequencing.md) for scene
   boundary issues, [media.md](media.md) for asset loading issues.

## CI integration

The fixtures are not yet wired into CI (`packages/producer/tests/` runs
inside Docker; the skill corpus needs the same). PR 7 of the stack adds
the orchestrator that runs all four tiers and emits an aggregated pass
report. For now, evaluate by hand per fixture.


<!-- ===== FILE: hyperframes/remotion-to-hyperframes/references/fonts.md ===== -->

# Font translation

Fonts are the dominant non-translation noise floor. Same `font-weight: 800`
renders perceptibly bolder on HF's `chrome-headless-shell` than on
Remotion's bundled Chromium when there's no real font installed. Validation
showed this costs ~0.025 mean SSIM at the noise floor.

## Pattern: `@remotion/google-fonts/<Family>`

```tsx
import { loadFont } from "@remotion/google-fonts/Inter";
loadFont("normal", { weights: ["400", "800"] });
```

Translate to a `<link>` tag in `<head>`:

```html
<head>
  <link rel="preconnect" href="https://fonts.googleapis.com" />
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
  <link
    href="https://fonts.googleapis.com/css2?family=Inter:wght@400;800&display=swap"
    rel="stylesheet"
  />
  <style>
    body {
      font-family: Inter, sans-serif;
    }
  </style>
</head>
```

Pull the family name and weights from the import path and `loadFont`
arguments. HF's compiler inlines the Google Fonts CSS at render time, so
you don't pay a network round-trip per render.

## Pattern: local fonts via `@font-face`

```tsx
import { Font } from "remotion";

Font.loadFont("/MyFont.woff2", "MyFont");
```

Translate to a `@font-face` rule:

```html
<style>
  @font-face {
    font-family: "MyFont";
    src: url("assets/MyFont.woff2") format("woff2");
    font-weight: 400;
    font-style: normal;
  }
</style>
```

Copy the font file into `hf-src/assets/` next to the HTML.

## Pattern: system font fallback (no font load)

```tsx
<div style={{ fontFamily: "Helvetica, Arial, sans-serif" }}>...</div>
```

Same string in HF — but be aware: on Linux without a real Helvetica
installed (typical CI environment), Remotion and HF fall back to
_different_ sans-serif system fonts because they bundle different
Chromium versions. This is the noise floor: ~0.025 mean SSIM cost,
visible as different stroke widths at large font weights (800+).

If matching the Remotion render exactly matters for a specific
fixture, load the same font explicitly — don't rely on system
fallback.

## When in doubt: use Inter

Inter renders identically across Chromium versions and is free.
Translate any "system sans-serif" Remotion comp to Inter when you
need to minimize font drift in the validation harness.

## Font loading and `delayRender`

Remotion uses `delayRender()` to defer the first frame until fonts
load. HF's compiler inlines Google Fonts at compile time and waits
on `@font-face` readiness via the Frame Adapter pattern — the
`delayRender` call drops in translation. See [media.md](media.md).

## Multi-weight loading

When Remotion loads multiple weights:

```tsx
loadFont("normal", { weights: ["400", "500", "700", "800"] });
```

Inline all weights in the Google Fonts URL:

```
?family=Inter:wght@400;500;700;800&display=swap
```

Translation rule: enumerate every distinct `font-weight` value
that appears in the composition's CSS (`font-weight: 800` →
weight 800 must be loaded). If the Remotion source loads weights
that aren't actually used, drop them.

## Font subsetting

Remotion's `loadFont` doesn't subset; HF's compiler doesn't either
(yet). Don't try to optimize this in translation — it's lossless to
keep the same weight set as the Remotion source.


<!-- ===== FILE: hyperframes/remotion-to-hyperframes/references/limitations.md ===== -->

# Translation limitations

What the skill explicitly cannot translate, separated from the
blocker-list (which is enforced by `lint_source.py`). These are
_known_ gaps — surface them to the user as translation notes
when translating the surrounding composition.

## React patterns the skill refuses

See [escape-hatch.md](escape-hatch.md). Any of these triggers
a bow-out:

- `useState`, `useReducer` driving animation
- `useEffect` / `useLayoutEffect` with non-empty deps (side effects)
- async `calculateMetadata`
- Third-party React UI libraries (MUI, Chakra, Mantine, antd, shadcn, Radix, NextUI)

`@remotion/lambda` is no longer in this list — it's a warning, not a
blocker, because Lambda config is orthogonal to composition rendering.
The skill drops the imports and `renderMediaOnLambda(...)` calls and
writes a `TRANSLATION_NOTES.md` entry. See
[escape-hatch.md](escape-hatch.md).

## Patterns that work with caveats

### Volume ramps on `<Audio>`

Remotion accepts a function for `volume`:

```tsx
<Audio src={...} volume={(f) => interpolate(f, [0, 30], [0, 1])} />
```

HF ramps volume with a `data-automation` volume lane on the `<audio>`
(form in `hyperframes-core/references/creator-editing-recipes.md`).
Translation: write the lane from the `interpolate` points, OR bake the ramp
into the audio file with `ffmpeg afade`. The dropped-ramp path produces audibly different
output but visually-identical video, so SSIM passes — just flag it.

### `<Loop>` with stateful children

```tsx
<Loop durationInFrames={30}>
  <CounterThatIncrementsViaUseRef />
</Loop>
```

A bounded GSAP repeat can reproduce _visual_ repetition when its finite count is derived
from the visible duration. If the looped child has cross-iteration state (a counter, a
randomness seed), HF won't reproduce it identically per iteration. Bow out unless the child
is fully deterministic per-iteration; use `repeat: -1` only when the root declares a finite `data-duration`.

### Remotion's `<Img>` with crossOrigin

```tsx
<Img src="https://other-domain.com/x.png" crossOrigin="anonymous" />
```

HF's renderer doesn't enforce CORS the same way Remotion does. Most
public images work; private images served with auth headers won't.
If the source uses `crossOrigin="use-credentials"`, the asset needs
to be downloaded and inlined at translation time.

### Custom `presentation` in `<TransitionSeries>`

```tsx
const customPresentation: PresentationComponent = ({ children, presentationProgress }) => {
  return <div style={{ filter: `blur(${(1 - presentationProgress) * 20}px)` }}>{children}</div>;
};
```

Pure presentations (transform/filter/opacity computed from progress)
translate to GSAP tweens cleanly. Presentations that read
`useCurrentFrame()` internally or have stateful children don't —
bow out.

### Code-split components (`React.lazy`)

```tsx
const HeavyChart = React.lazy(() => import("./HeavyChart"));
```

`React.lazy` is async and doesn't fit the deterministic-render model.
Translate to a regular import; the resulting HF composition will
just include all the code upfront.

## Patterns that always work

- `<AbsoluteFill>` and `<Sequence>` (any nesting)
- `useCurrentFrame()` derivations: `interpolate`, `spring`, `Easing`,
  `interpolateColors`, manual math
- `<Audio>`, `<Video>`, `<Img>`, `<IFrame>` with simple props
- `staticFile()` references
- Custom React subcomponents that are pure functions of props
- Custom hooks that are pure derivations of `useCurrentFrame`
- `@remotion/lottie` (translates to HF's Lottie adapter)
- `@remotion/google-fonts/<Family>` (translates to `<link>` or `@font-face`)
- Sync `calculateMetadata` (resolved at translation time)
- `<TransitionSeries>` with built-in presentations (`fade`, `slide`,
  `wipe`, `clockWipe`, `flip`, `iris`)

## What the skill never tries to translate

These are out-of-scope by design:

- **HDR rendering** — HF supports HDR but Remotion doesn't, so there's
  nothing to translate from.
- **Variable frame rate** — both tools assume constant fps.
- **Multi-composition `<Composition>` lists** — translate one at a
  time. The skill prompts the user to choose which composition.
- **Remotion Studio props panel** — visual prop editing in HF Studio
  needs different infrastructure; out of scope.

## Reporting gaps to the user

When translation produces _something_ but the something has gaps, write
a `TRANSLATION_NOTES.md` next to the output:

```markdown
# Translation notes

The following Remotion patterns were translated with caveats:

- `<Audio volume={(f) => ...}>` (line 15): volume ramp written as a
  `data-automation` volume lane (see `creator-editing-recipes.md`); the
  ffmpeg `afade` bake-in is the alternative.
- `<HeavyChart>` (line 30): translated as inline HTML. The original
  React.lazy boundary was dropped — bundle size unchanged because HF
  serves a single HTML file.

If any of these caveats matter, consider the runtime interop pattern
instead.
```

This file is also generated by the skill alongside the HF output, not
held in the corpus.


<!-- ===== FILE: hyperframes/remotion-to-hyperframes/references/lottie.md ===== -->

# Lottie translation: @remotion/lottie → HF lottie adapter

Lottie animations are a clean translation case — HF has a built-in
[Lottie adapter](https://github.com/heygen-com/hyperframes/blob/main/packages/core/src/runtime/adapters/lottie.ts)
that supports both `lottie-web` and `@lottiefiles/dotlottie-web`. The
adapter auto-discovers animations registered on `window.__hfLottie`
and seeks them per-frame via `goToAndStop`.

## Pattern

```tsx
import { Lottie } from "@remotion/lottie";
import animationData from "./hello.json";

export const MyComp = () => (
  <AbsoluteFill>
    <Lottie animationData={animationData} loop={false} />
  </AbsoluteFill>
);
```

Translates to:

```html
<div id="stage" ...>
  <div id="lottie-anim" style="width:100%;height:100%"></div>
  <script src="https://cdnjs.cloudflare.com/ajax/libs/bodymovin/5.12.2/lottie.min.js"></script>
  <script>
    const anim = lottie.loadAnimation({
      container: document.getElementById("lottie-anim"),
      renderer: "svg",
      loop: false,
      autoplay: false,
      path: "assets/hello.json",
    });
    window.__hfLottie = window.__hfLottie || [];
    window.__hfLottie.push(anim);
  </script>
</div>
```

Key differences from a typical Lottie embed:

- `autoplay: false` — HF drives playback by seeking
- `loop: false` typically (unless Remotion's `loop={true}`)
- `window.__hfLottie.push(anim)` is what hooks the animation into HF's
  per-frame seek

## Asset handling

Remotion bundles the animation JSON via webpack import. HF needs the JSON
on disk under `assets/` and references it via path:

1. Copy `hello.json` from the Remotion project into `hf-src/assets/`.
2. Reference as `path: "assets/hello.json"` in `loadAnimation`.

For dotlottie (binary) format, swap in `@lottiefiles/dotlottie-web`:

```html
<script src="https://unpkg.com/@lottiefiles/dotlottie-web"></script>
<canvas id="anim" style="width:100%;height:100%"></canvas>
<script>
  const player = new DotLottie({
    canvas: document.getElementById("anim"),
    src: "assets/hello.lottie",
    autoplay: false,
  });
  window.__hfLottie = window.__hfLottie || [];
  window.__hfLottie.push(player);
</script>
```

The HF adapter handles both player APIs (it duck-types `goToAndStop`
vs `setCurrentRawFrameValue` / `seek`).

## Multiple Lottie animations

Multiple `<Lottie>` instances in one composition work — push each one
onto `window.__hfLottie` and the adapter will seek all of them in sync:

```js
window.__hfLottie.push(anim1);
window.__hfLottie.push(anim2);
window.__hfLottie.push(anim3);
```

## Lottie source isn't actually translation-blocking

Lottie animations encode their own deterministic timeline. They're the
_easiest_ part of a Remotion composition to translate because the
animation logic is already self-contained — neither Remotion nor HF
"animate" them, both just seek them. Translation cost is near-zero.

## After Effects → Lottie limitations

Lottie supports a subset of After Effects features. Expressions, most
Effects (drop shadow, color overlay), all blend modes beyond Normal/Add/
Multiply, luma mattes, and most 3D parameters are not supported. If the
Remotion composition uses a Lottie file that depends on these, the
animation will break in BOTH Remotion and HF — this isn't a translation
problem, it's a Lottie limitation. See
[airbnb/lottie/after-effects.md](https://github.com/airbnb/lottie/blob/master/after-effects.md)
for the full supported feature list.

## Loop behavior

Remotion's `loop={true}` plays the animation continuously. Translate it
to `loop: true` on the player: the HF adapter wraps composition time into
the animation's own length, so the cycle repeats for the whole scene. It
does not add playback-rate scaling; bake a non-default rate into the
Lottie asset and verify the rendered output.

## Performance note

Per the [Lottie adapter](https://github.com/heygen-com/hyperframes/blob/main/packages/core/src/runtime/adapters/lottie.ts)
docs: lottie-web's `goToAndStop(time, isFrame=false)` takes time in ms;
the adapter passes `time * 1000` for precision. This is more accurate
than passing frame numbers (especially for animations whose internal
fps doesn't match the HF render fps).


<!-- ===== FILE: hyperframes/remotion-to-hyperframes/references/media.md ===== -->

# Media translation: Audio, Video, Img, IFrame, staticFile

## Asset paths

Remotion's `staticFile("x.png")` resolves to the project's `public/` directory.
HF uses relative paths from the composition's `index.html`, conventionally
`assets/`:

```tsx
<Img src={staticFile("logo.png")} />
```

```html
<img src="assets/logo.png" />
```

When translating, copy the asset from `remotion-src/public/x` to
`hf-src/assets/x`. Multiple files can be batched with a setup script;
see T2's `setup.sh` for an example pattern.

## `<Audio>`

```tsx
<Audio src={staticFile("music.wav")} volume={0.5} />
```

```html
<audio
  data-start="0"
  data-duration="6"
  data-track-index="2"
  data-volume="0.5"
  src="assets/music.wav"
></audio>
```

`data-start` and `data-duration` are required — the runtime needs them to
schedule the audio. Default to the composition's full duration if Remotion
didn't specify trim.

### Volume ramps

```tsx
<Audio src={staticFile("music.wav")} volume={(f) => interpolate(f, [0, 30], [0, 1])} />
```

Volume ramps become a `data-automation` volume lane on the `<audio>`
(form in `hyperframes-core/references/creator-editing-recipes.md`); `data-volume`
is the static baseline.

### Trim / playbackRate

```tsx
<Audio src={staticFile("music.wav")} startFrom={60} endAt={180} playbackRate={1.5} />
```

```html
<audio
  data-start="0"
  data-duration="<resolved from trim>"
  data-trim-start="2"
  data-trim-end="6"
  data-playback-rate="1.5"
  src="assets/music.wav"
></audio>
```

`startFrom` / `endAt` are frame indexes; convert to seconds.

## `<Video>` and `<OffthreadVideo>`

```tsx
<Video src={staticFile("intro.mp4")} playsInline />
<OffthreadVideo src={staticFile("intro.mp4")} />
```

```html
<!-- intro.mp4 has an audio stream -->
<video
  playsinline
  data-has-audio="true"
  data-start="0"
  data-duration="5"
  data-track-index="0"
  src="assets/intro.mp4"
></video>

<!-- intro.mp4 is silent (or the Remotion element is muted) -->
<video
  playsinline
  muted
  data-start="0"
  data-duration="5"
  data-track-index="0"
  src="assets/intro.mp4"
></video>
```

`<OffthreadVideo>` is a Remotion-specific optimization for headless
rendering. HF runs in headless Chrome already, so the off-thread variant
collapses to a regular `<video>`.

`playsinline` is required for the runtime to autoplay (browser policy); always
emit it. Check the source file for an audio stream first:
`ffprobe -v error -select_streams a -show_entries stream=codec_type -of csv=p=0 <file>`
(non-empty output means it has audio). Remotion `<Video>` maps to
`<video playsinline>` + `data-has-audio="true"` only when the file has an audio
stream and the Remotion source does not set `muted` or `volume={0}`; otherwise
emit `muted`. Silent b-roll with `data-has-audio="true"` aborts the render
(`ASSET_MEDIA_TYPE_MISMATCH`).

## `<Img>`

```tsx
<Img src={staticFile("logo.png")} style={{ width: 200, height: 200 }} />
```

```html
<img src="assets/logo.png" style="width: 200px; height: 200px;" />
```

Width/height get rounded to integer px. If the original style has
animated dimensions, the GSAP tween animates them — see [timing.md](timing.md).

## `<IFrame>`

```tsx
<IFrame src="https://example.com" />
```

```html
<iframe src="https://example.com"></iframe>
```

When HF detects a nested iframe in a composition, it auto-falls back to
**screenshot mode** rather than the deterministic BeginFrame mode. This
costs render performance but produces visibly-correct output. See
[hyperframes-vs-remotion.mdx](https://github.com/heygen-com/hyperframes/blob/main/docs/guides/hyperframes-vs-remotion.mdx)
for details.

## `delayRender()` / `continueRender()`

```tsx
const handle = delayRender();
useEffect(() => {
  loadAsset().then(() => continueRender(handle));
}, []);
```

Drop. HF waits on asset readiness via the [Frame Adapter pattern](https://hyperframes.heygen.com/concepts/frame-adapters)
— images, videos, fonts, and Lottie animations all signal load
completion natively. There's nothing to do at the application level.

## When the asset isn't a file

If Remotion's media source is a Buffer, dataURL, or URL.createObjectURL,
the asset doesn't exist on disk and can't be copied via setup.sh. Two
options:

1. Materialize the asset at translation time — write the buffer to a file
   in `hf-src/assets/`.
2. Embed as a data URL directly in the HTML (`src="data:image/png;base64,..."`)
   for small assets (< 100 KB).

For audio/video Buffers, option 1 is preferred — base64-encoded media
bloats the HTML and slows the renderer.


<!-- ===== FILE: hyperframes/remotion-to-hyperframes/references/parameters.md ===== -->

# Parameter translation: Zod schemas, defaultProps, calculateMetadata

How a typed Remotion `<Composition schema={...} defaultProps={...} />`
turns into a parameterized HF composition.

## Sync calculateMetadata (translatable)

```tsx
<Composition
  id="MyVideo"
  component={MyVideo}
  schema={z.object({ title: z.string(), duration: z.number() })}
  defaultProps={{ title: "Hello", duration: 90 }}
  calculateMetadata={({ props }) => ({
    durationInFrames: props.duration,
    fps: 30,
  })}
/>
```

When `calculateMetadata` is synchronous and only uses `props`, **resolve
it at translation time** — call it with `defaultProps` (or whatever the
caller specifies) and write the concrete result into the HTML:

```html
<div
  id="stage"
  data-composition-id="MyVideo"
  data-start="0"
  data-duration="3"          <!-- 90/30 -->
  data-fps="30"
  data-title="Hello"
></div>
```

The `data-title` attribute carries the value through. Code that originally
read `props.title` reads `document.getElementById("stage").dataset.title`
in HF.

Inside a scene sub-composition file that lookup does not reach the root
`#stage`. Pass a prop to a scene with `data-variable-values` on its host and
read it there with `window.__hyperframes.getVariables()` (declare defaults with
`data-composition-variables` on the scene's composition element).

## Async calculateMetadata (NOT translatable)

```tsx
<Composition
  calculateMetadata={async ({ props }) => {
    const res = await fetch(...);
    return { durationInFrames: res.duration };
  }}
/>
```

**Refuse + interop**. HF needs composition metadata up-front to seed the
HTML. Resolving network calls at translation time defeats the purpose
of having dynamic metadata. See [escape-hatch.md](escape-hatch.md).

The lint rule `r2hf/async-metadata` catches this. T4 case 03 tests it.

## Default props

```tsx
defaultProps={{
  title: "Hello",
  subtitle: "World",
  count: 42,
}}
```

Translate to `data-*` attributes on the root `#stage` div:

```html
<div id="stage" data-title="Hello" data-subtitle="World" data-count="42">...</div>
```

Convention: `propName` → `data-prop-name` (kebab-case). Inside the GSAP
script, read via `document.getElementById("stage").dataset.propName`.

## Nested object / array props

```tsx
defaultProps={{
  stats: [
    { label: "Stars", value: 1247, color: "#fbbf24" },
    { label: "Forks", value: 312, color: "#60a5fa" },
  ],
}}
```

Don't try to encode the array as a JSON `data-` attribute — HF's runtime
doesn't parse those. Materialize the array as **repeated HTML markup**:

```html
<div id="scene-stats">
  <div class="stat-card" data-stat-index="0" data-stat-value="1247" style="--card-color:#fbbf24">
    <div class="number">0</div>
    <div class="label">Stars</div>
  </div>
  <div class="stat-card" data-stat-index="1" data-stat-value="312" style="--card-color:#60a5fa">
    <div class="number">0</div>
    <div class="label">Forks</div>
  </div>
</div>
```

The component template (`StatCard.tsx`) becomes the markup template;
each instance gets its scalar props rendered as `data-*` and CSS
custom properties.

Validated in T3 — three StatCards reused with different props,
mean SSIM 0.953.

## Numeric props that need typed parsing

`document.getElementById("stage").dataset.count` is a string. Convert at
read time:

```js
const count = Number(stage.dataset.count);
```

Or inline values directly into the GSAP script when the data is known
at translation time and doesn't need to vary per render.

## Boolean props

```tsx
defaultProps={{ darkMode: true }}
```

Two conventions:

- `data-dark-mode="true"` — read as string, compare `=== "true"`
- `data-dark-mode` (presence/absence) — `<div data-dark-mode>` for true, omit for false

Pick one and be consistent. The presence/absence form is HTML-idiomatic
and pairs well with CSS attribute selectors:

```css
[data-dark-mode] .scene {
  background: #000;
}
```

## Zod runtime validation

Remotion's `schema` validates props at composition load. HF doesn't have
an equivalent — by the time the HTML is in the renderer, the schema is
already gone.

Validate at translation time instead. If the user passes invalid data,
fail with a translation error before emitting HTML. This matches Zod's
"fail loud" intent without requiring the runtime dependency.

## When the composition uses props for computed prop derivation

```tsx
const Composition: React.FC<Props> = ({ stats }) => {
  const total = stats.reduce((acc, s) => acc + s.value, 0);
  return <div>{total}</div>;
};
```

Compute the derived value at translation time and bake it into the HTML
or a `data-` attribute. Don't try to express the computation in JS in the
HF composition — that adds runtime overhead and makes the HTML stateful
in ways that complicate human editing.

If the derivation is non-trivial (involves the array itself, not just
scalars), materialize it as static text in the HTML.


<!-- ===== FILE: hyperframes/remotion-to-hyperframes/references/sequencing.md ===== -->

# Sequencing translation: Sequence, Series, Composition root

How Remotion's nested `Sequence` tree maps to one sub-composition host per
scene in the root, each with its own paused GSAP timeline in local time.

## The core idea

Remotion's `<Sequence from={F} durationInFrames={D}>` is a coordinate
transform: it shifts `useCurrentFrame()` by `F` and clips the child
component to the window `[F, F+D]`. HF doesn't have a per-element
"current frame" — there's a single composition seek time and the
runtime hides/shows elements based on their `data-start` / `data-duration`.

Result: the nested tree flattens into a list of scene hosts on the same
parent, each with its own time window; each scene's content lives in its
own sub-composition file.

## `<Composition>` → root `#stage`

```tsx
<Composition
  id="MyVideo"
  component={MyVideo}
  durationInFrames={300}
  fps={30}
  width={1280}
  height={720}
/>
```

```html
<div
  id="stage"
  data-composition-id="MyVideo"
  data-start="0"
  data-duration="10"      <!-- 300/30 -->
  data-fps="30"
  data-width="1280"
  data-height="720"
>
  <!-- composition content -->
</div>
```

`data-start="0"` is required on `#stage` (the runtime needs it to anchor
playback; missing it triggers a lint warning).

## `<AbsoluteFill>` → positioned div

```tsx
<AbsoluteFill style={{ backgroundColor: "#0a0a0a" }}>...children...</AbsoluteFill>
```

```html
<div style="position:absolute;inset:0;background-color:#0a0a0a;">...children...</div>
```

`AbsoluteFill` is just a styled div in Remotion. Translate to a div with
`position:absolute; inset:0` and copy through any other style props.

## `<Sequence>` → sub-composition host

```tsx
<Sequence from={0} durationInFrames={90}>
  <TitleCard />
</Sequence>
```

The root `#stage` only holds a host per scene; the scene's markup, styles
and timeline live in their own sub-composition file, so the Studio timeline
gets one readable row per scene and the lint has no nested structure to flag.

```html
<!-- index.html -->
<div
  id="scene-1"
  class="clip"
  data-composition-id="scene-1"
  data-composition-src="compositions/scene-1.html"
  data-start="0"
  data-duration="3"
  data-track-index="0"
></div>
```

```html
<!-- compositions/scene-1.html: TitleCard children inlined, timeline keyed "scene-1", local time starts at 0 -->
<template id="scene-1-template">
  <div data-composition-id="scene-1" data-width="1280" data-height="720" data-duration="3">
    <!-- TitleCard children -->
    <script>
      const tl = gsap.timeline({ paused: true });
      window.__timelines["scene-1"] = tl;
    </script>
  </div>
</template>
```

Convert frames to seconds: `from/fps`, `durationInFrames/fps`. Pick a
`data-track-index` per parallel rendering layer (background = 0,
overlays = 1, audio = 2, etc.). Sequential scenes can share an index.
Inside the sub-composition, time is local: a tween that started at `F/fps`
in the root starts at `0` here. Asset paths are relative to the
sub-composition file (`../assets/x.png`).

## Nested `<Sequence>` flattens

Remotion adds offsets when sequences nest:

```tsx
<Sequence from={60} durationInFrames={120}>
  <Sequence from={30} durationInFrames={60}>
    <ImageScene />
  </Sequence>
</Sequence>
```

The inner sequence's effective window is `[60+30, 60+30+60] = [90, 150]`.

Translate by computing the sum and emitting one host with the resolved
window; the scene's children go in its sub-composition file:

```html
<div
  data-composition-id="image-scene"
  data-composition-src="compositions/image-scene.html"
  data-start="3"
  data-duration="2"
  data-track-index="0"
></div>
```

## `<Series>` → siblings with sequential offsets

```tsx
<Series>
  <Series.Sequence durationInFrames={60}>
    <A />
  </Series.Sequence>
  <Series.Sequence durationInFrames={120}>
    <B />
  </Series.Sequence>
  <Series.Sequence durationInFrames={90}>
    <C />
  </Series.Sequence>
</Series>
```

Each `Sequence.Sequence` lives in the next time slot. Emit siblings
with `data-start` accumulating (each host mounts its scene file):

```html
<div
  data-composition-id="a"
  data-composition-src="compositions/a.html"
  data-start="0"
  data-duration="2"
  data-track-index="0"
></div>
<div
  data-composition-id="b"
  data-composition-src="compositions/b.html"
  data-start="2"
  data-duration="4"
  data-track-index="0"
></div>
<div
  data-composition-id="c"
  data-composition-src="compositions/c.html"
  data-start="6"
  data-duration="3"
  data-track-index="0"
></div>
```

## Crossfading scene boundaries

Remotion `<Sequence>` shows/hides at hard boundaries by default. HF does
the same — but if your composition needs a smooth fade between scenes,
you have to drive opacity explicitly with GSAP at the boundary. A scene can
hard-cut itself with `gsap.set` at its local end (the corpus fixtures do). A
fade between two scenes goes on the scene hosts from the root timeline, since
a scene's own timeline only sees its own file:

```js
const tl = gsap.timeline({ paused: true });
tl.set(scene1, { opacity: 1 }, 0);
tl.set(scene1, { opacity: 0 }, 2); // hard cut at 2s
tl.set(scene2, { opacity: 1 }, 2);
```

For a 0.5 s crossfade:

```js
tl.to(scene1, { opacity: 0, duration: 0.5 }, 1.5);
tl.to(scene2, { opacity: 1, duration: 0.5 }, 1.5);
```

For Remotion `<TransitionSeries>` translations see [transitions.md](transitions.md).

## `<Loop>`

```tsx
<Loop durationInFrames={30}>
  <Spinner />
</Loop>
```

HF doesn't have a `<Loop>` primitive. Translate it to a bounded GSAP timeline using
the time available at its insertion point:

```js
const cycleDuration = 1;
const availableDuration = compositionDuration - 3;
const repeat = Math.max(0, Math.floor(availableDuration / cycleDuration) - 1);
const spinTl = gsap.timeline({ paused: true, repeat, repeatRefresh: false });
spinTl.to(spinner, { rotate: 360, duration: 1.0, ease: "none" });
// Embed in the main composition timeline at the right offset:
mainTl.add(spinTl, 3);
```

This is fragile — Remotion's `<Loop>` resets internal state every iteration,
which GSAP repeat does too, but if the looped child has its own animation,
you need to be careful that GSAP's `repeatRefresh` is on or off as needed.
The finite count is required because HyperFrames seeks a bounded composition frame-by-frame.

## `<Freeze>`

```tsx
<Freeze frame={30}>
  <Animated />
</Freeze>
```

Drop the wrapper. `<Freeze>` pins `useCurrentFrame()` at a constant for
the children — but in HF, the children's animation is already driven by
explicit GSAP tweens, so freeze translates to "don't tween this element".

## Multiple parallel tracks

When you have a background video + overlay text + audio playing
simultaneously, use distinct `data-track-index` values:

```html
<div data-track-index="0">background video</div>
<div data-track-index="1">overlay text</div>
<audio data-track-index="2" ...></audio>
```

The runtime picks track ordering from the index. See [media.md](media.md)
for media-specific track conventions.


<!-- ===== FILE: hyperframes/remotion-to-hyperframes/references/timing.md ===== -->

# Timing translation: interpolate, spring, easing

The single highest-leverage reference. Easings and timings are what readers
notice; getting them wrong costs more SSIM than any other translation choice.
Empirically validated against tiers T1–T3.

## Conversion: frames → seconds

HF's timeline is in seconds. Remotion is frame-based. Always:

```
time_seconds = frame / fps
```

So at fps=30:

- frame 15 → 0.5 s
- frame 30 → 1.0 s
- frame 90 → 3.0 s

Do this conversion once when translating, not at runtime.

## interpolate — linear

```tsx
const opacity = interpolate(frame, [0, 30], [0, 1], { extrapolateRight: "clamp" });
```

Translates to:

```js
gsap.to(target, { opacity: 1, duration: 1.0, ease: "none" }, 0);
// fromTo if the property starts at 0 and CSS doesn't already set it
gsap.fromTo(target, { opacity: 0 }, { opacity: 1, duration: 1.0, ease: "none" }, 0);
```

`ease: "none"` matches Remotion's default linear interpolation. CSS sets the
`from` value if your initial state is in CSS; otherwise use `fromTo`.

`extrapolateLeft`/`extrapolateRight` defaults to `"extend"` in Remotion but
`"clamp"` is what the agent will see most often. GSAP doesn't extend — values
hold at the start and end of the tween. So for `clamp`, GSAP matches; for
`extend`, you'd need to extend the input range manually before emitting.

## interpolate — multi-segment

```tsx
const opacity = interpolate(frame, [0, 15, 75, 90], [0, 1, 1, 0]);
```

Three keyframed tweens at offsets `[0]/fps`, `[1]/fps`, `[2]/fps`:

```js
const tl = gsap.timeline({ paused: true });
tl.to(target, { opacity: 1, duration: 0.5, ease: "none" }, 0);
tl.to(target, { opacity: 1, duration: 2.0, ease: "none" }, 0.5);
tl.to(target, { opacity: 0, duration: 0.5, ease: "none" }, 2.5);
```

Validated in T1 — mean SSIM 0.974 against Remotion baseline.

## spring → GSAP back.out

Remotion's `spring()` is the most lossy translation. The mapping is approximate
but close enough that real-world compositions hold ≥ 0.92 SSIM (T2: 0.985, T3: 0.953).

| Remotion `spring` config                          | GSAP equivalent                                      | Validated in                     |
| ------------------------------------------------- | ---------------------------------------------------- | -------------------------------- |
| `{damping: 12, stiffness: 100, mass: 1}` (snappy) | `back.out(1.4)` over ~0.7 s                          | T2, T3 (TitleScene)              |
| `{damping: 14, stiffness: 90, mass: 1}` (calmer)  | `back.out(1.2)` over ~0.7 s                          | T3 (StatCard)                    |
| `{damping: 8, stiffness: 200}` (very bouncy)      | `back.out(2.0)` or `elastic.out(1, 0.5)` over ~0.6 s | not validated; budget ~0.05 SSIM |
| `{overshootClamping: true}`                       | `power3.out` over ~0.6 s (no overshoot)              | not validated                    |

**Rule of thumb**: `back.out(N)` overshoot ratio ≈ `(stiffness / damping^2) * 1.4`. For
`damping:12, stiffness:100` that gives `1.4 * 100/144 = 0.97`, which is close to
the validated 1.4 (the formula is rough; tune by visual). Default duration is
~0.7 s for the typical config.

When the spring's `delay`/`from`/`to` are non-default, scale the duration
proportionally.

## interpolate with custom easing

```tsx
import { Easing } from "remotion";
interpolate(frame, [0, 30], [0, 1], { easing: Easing.out(Easing.cubic) });
```

| Remotion                     | GSAP                                                                                   |
| ---------------------------- | -------------------------------------------------------------------------------------- |
| `Easing.in(Easing.linear)`   | `ease: "none"`                                                                         |
| `Easing.out(Easing.cubic)`   | `ease: "power3.out"`                                                                   |
| `Easing.inOut(Easing.cubic)` | `ease: "power3.inOut"`                                                                 |
| `Easing.out(Easing.poly(N))` | `ease: "power<N>.out"` (N=2 quad, 3 cubic, 4 quart, 5 quint)                           |
| `Easing.bezier(a,b,c,d)`     | `CustomEase.create("c", "M0,0 C${a},${b} ${c},${d} 1,1")` (requires CustomEase plugin) |
| `Easing.elastic(bounciness)` | `ease: "elastic.out(${bounciness}, 0.3)"`                                              |
| `Easing.bounce`              | `ease: "bounce.out"`                                                                   |
| `Easing.back(overshoot)`     | `ease: "back.out(${overshoot * 1.7})"` (Remotion's overshoot scale differs)            |

## interpolate driving non-numeric properties

```tsx
const color = interpolateColors(frame, [0, 30], ["#ff0000", "#0000ff"]);
```

GSAP does color tweens natively:

```js
gsap.to(target, { color: "#0000ff", duration: 1.0, ease: "none" }, 0);
```

Same for `backgroundColor`, `borderColor`. The `from` value is read from CSS
or the inline style.

## Custom count-up / number tweens

When Remotion uses a frame-driven number ramp (`Math.round(value * eased)`):

```tsx
const t = interpolate(frame, [0, 45], [0, 1]);
const eased = 1 - (1 - t) ** 3; // cubic ease-out
const value = Math.round(target * eased);
return <div>{value.toLocaleString()}</div>;
```

GSAP equivalent — tween a counter object, write `textContent` on update:

```js
const counter = { v: 0 };
tl.to(
  counter,
  {
    v: target,
    duration: 1.5,
    ease: "power3.out",
    onUpdate: () => {
      el.textContent = Math.round(counter.v).toLocaleString();
    },
  },
  0,
);
```

`power3.out` matches `1 - (1-t)^3` exactly. Validated in T3 (mean SSIM 0.953).
Per-frame digit mismatches occur on sub-frame timing offsets but final values
converge — no SSIM impact above the noise floor.

## Stagger via per-instance prop

When custom subcomponents take a `delayInFrames` prop:

```tsx
<StatCard delayInFrames={i * 12} value={...} />
```

Translate to GSAP timeline offsets:

```js
cards.forEach((card, i) => {
  const start = base + i * (12 / fps); // i * 0.4s at fps=30
  tl.to(card, { ... }, start);
});
```

Validated in T3 — three StatCards staggered at 0.0/0.4/0.8 s.
