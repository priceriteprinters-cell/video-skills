

<!-- ===== FILE: hyperframes/hyperframes-core/GUIDE.md ===== -->

---
name: hyperframes-core
description: The HyperFrames composition contract — build one renderable project. Use for composition structure, the `data-*` timing attributes, `class="clip"`, tracks, sub-compositions, variables, framework-owned media playback, deterministic-render rules, and validation. Read before writing composition HTML.
---

**Plugin installs:** Before setup or freshness commands, follow [plugin execution rules](../hyperframes/references/plugin-installation.md) when this skill is inside a HyperFrames plugin. Standalone installs keep the update instructions below.

# HyperFrames Core

**Agent pitfalls (read first):**

- Center with flex/`inset`, not CSS `transform: translate(-50%,-50%)` on a node you then GSAP `x`/`y`. Lint: `gsap_css_transform_conflict`. Use `fromTo` or `xPercent`/`yPercent`.
- Do not add a scene-exit `tl.set(..., {visibility:"hidden"})`. The runtime already hides timed clips. Opacity fades on inner nodes (or `opacity` on `.clip`) are enough. Caption hard-kills are a different rule.
- `window.__timelines["id"]` must match the root `data-composition-id`.
- After `render`, read the summary's second line: `beginframe` vs `screenshot`, GPU mode, stage timings. `screenshot` + `software gpu` on Linux is the slow path.

HyperFrames renders video from HTML. A composition is an HTML file whose DOM declares timing with `data-*` attributes, whose animation runtime is seekable, and whose media playback is owned by the framework.

This skill is the **technical contract** — how to build one hyperframes project. The body below is the build guide; per-topic detail lives in `references/` (index next), read on demand. Process docs (brief, storyboard, review, production, dispatch, frame-worker) live in `/hyperframes` → `references/`. Other concerns live in the sibling domain skills — `hyperframes-animation`, `hyperframes-creative`, `media-use`, `hyperframes-cli`, `hyperframes-registry`. The capability map in `/hyperframes` says what each one covers.

## References

| File                                    | Read it to…                                                                                                                                                         |
| --------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `references/minimal-composition.md`     | start from the smallest renderable composition skeleton                                                                                                             |
| `references/composition-patterns.md`    | choose monolithic vs modular; structure a modular `index.html`; pick a sub-comp archetype                                                                           |
| `references/data-attributes.md`         | look up any `data-*` (root / clip / sub-comp host / legacy aliases); use `class="clip"`                                                                             |
| `references/tracks-and-clips.md`        | understand what `data-track-index` does (and does not) control, z-index, time a clip relative to another; list every track and clip with `npx hyperframes timeline` |
| `references/creator-editing-recipes.md` | copy truthful cut/trim/reorder/retime/freeze/camera/mask/crossfade/audio editing recipes and their limits                                                           |
| `references/sub-compositions.md`        | wire a sub-composition (host attrs, `<template>`, per-instance vars) and animate inside it                                                                          |
| `references/variables-and-media.md`     | declare variables; place `<video>`/`<audio>`, set volume, trim                                                                                                      |
| `references/determinism-rules.md`       | build a seekable timeline; determinism bans; layout / text fit                                                                                                      |
| `references/full-screen-motion.md`      | author full-frame motion with shared backgrounds                                                                                                                    |
| `references/tailwind.md`                | work in a Tailwind v4 project (`init --tailwind`; runtime contract differs from Studio's v3)                                                                        |

For animation runtime specifics (GSAP API, Lottie, Three.js, etc.) go to `hyperframes-animation` → `adapters/<runtime>.md`.

## Building a composition

### Two root forms (not interchangeable)

- **Standalone** (top-level `index.html`): root `<div data-composition-id="…">` sits directly in `<body>`, **no `<template>` wrapper**. Wrapping a standalone root hides all content and `lint` rejects it (`standalone_composition_wrapped_in_template`, error).
- **Sub-composition** (loaded via `data-composition-src`): wrap the root in `<template>`. This is the shape to write: the loader also accepts a plain full document and falls back to its `<body>`, but the templated form is what the examples and tooling assume.

> ⚠ Transport rule: for a **templated** sub-composition the assembler drops the file's own `<head>` `<style>`/`<script>` (`packages/core/src/compiler/compositionAssembly.ts`, the `hasTemplate` gate), so put `<style>`/`<script>` **inside** the template. `<link>` is hoisted either way.
> ⚠ Host-id convention: give the host slot, the inner template, and the `window.__timelines["<id>"]` key the **same** id. A different local id is supported (the assembler falls back to the first root in the file) but the mismatch is silent, so match them unless you have a reason not to.

File shape, host wiring, and the pre-render checklist → `references/sub-compositions.md`.

### Root must be sized (silent layout bug)

The standalone root authors `width`/`height: 100%`. Canvas size is `data-width`/`data-height`. The runtime stamps those pixels onto the composition root. Do not hardcode `1920px`/`1080px` on `#root`. Skeleton → `references/minimal-composition.md`.

### One paused timeline

Each composition registers **exactly one** `gsap.timeline({ paused: true })` at `window.__timelines["<id>"]` (key = root `data-composition-id`). Building it inside an async callback (`document.fonts.ready`) is supported; what matters is that you **register only after the build completes**. Render length is the root's `data-duration`, **not** the timeline's length: a timeline that runs past it is cut off, and one that ends early holds its last frame. Omit the root `data-duration` and the length is inferred instead (timeline, media window, or adapter). You do not need `window.__timelines = window.__timelines || {}`: the runtime creates the registry before your inline scripts run, and `lint` no longer asks for it. Don't manually nest sub-timelines into the host; the runtime auto-nests registered child timelines. Full contract (incl. non-GSAP runtimes) → `references/determinism-rules.md` + `hyperframes-animation/adapters/`.

### First-pass lint gotchas (a guaranteed first build failure)

Rules that `lint` **does** catch, but only after the fact. Write them right the first time:

- Never pair a CSS initial `transform` with a GSAP tween on the **same** property — the CSS value and the tween's start fight and `lint` rejects it with `gsap_css_transform_conflict`. Set the initial state inside the tween with `gsap.fromTo(el, { x: -40 }, { x: 0 })` instead of a CSS `transform: translateX(-40px)`.
- Never put `crossorigin` on `<video>`/`<audio>`. `lint` rejects it unconditionally with `media_crossorigin_breaks_preview` (error), including for canvas/WebGL/WebAudio readback. There is no suppression.
- Never give a `<video data-start>` an ancestor that also carries `data-start`. `lint` rejects it with `video_nested_in_timed_element` (error). Time the wrapper **or** the video, not both.
- Every `<audio>` needs an `id`. `lint` rejects it with `media_missing_id`, and an id-less `<audio>` is never picked up by the mixer, so the render is **silent**.
- Never tween a `.clip` with `autoAlpha` or `visibility` — `lint` rejects it with `gsap_animates_clip_element`. Animate a child instead.
- A named CSS `font-family` needs an in-file `@font-face` to a shipped local file, or `lint` fires `font_family_without_font_face`.
- Sub-composition `#root` uses `width`/`height: 100%` (or `inset: 0`), not hardcoded `1920px`/`1080px`. Canvas size is `data-width`/`data-height`.

A lint **error** also switches off the layout and contrast audits: `check` then reports `0 sample(s)` and `0/0 text checks`, which reads like a clean file but means nothing ran. Clear lint errors before you trust those numbers.

### Non-negotiable rules (silent bugs automated gates may miss)

Surfaced here; full rationale in the linked reference. Do not violate:

- No render-time clocks / unseeded `Math.random` / network / input-state; `repeat: -1` only under a finite root `data-duration` (export clips to it — otherwise use a finite count). → `determinism-rules.md`
- Never tween `display`, `visibility`, or `autoAlpha` on a `.clip` element. The framework owns clip visibility, and `lint` rejects it (`gsap_animates_clip_element`). Animate a child instead. → `determinism-rules.md`
- No `<br>` in body text; transformed elements must be block-level + sized; pulsing absolute decoratives need peak clearance. → `determinism-rules.md`
- `<video>`/`<audio>` are found by a flat document query, so the framework seeks and decodes them at **any nesting depth** (including inside a sub-comp `<template>` or wrapper). One hard limit: `lint` errors if a `<video data-start>` sits inside another **plain** element that also has `data-start`, and the failure is real (wrong source frames, then the clip vanishes mid-slot), so put the timing on the wrapper or on the video, never both. Sub-composition hosts are exempt: media inside a sub-composition renders correctly. The other caveat is timelines, not placement: a sub-comp timeline can't animate host-root elements. → `variables-and-media.md`
- Keep every `id` unique across the **assembled** page (prefix sub-comp ids with the composition id, `#<id>-hero`) so your own `#id` CSS and `getElementById` calls resolve. Frame injection no longer depends on it: the compiler stamps a document-unique `data-hf-render-id` on every `video[src]`/`audio[src]`/`img[src]`. Media that uses `<source>` children instead of a `src` attribute is **not** stamped, so unique ids still matter there. → `composition-patterns.md`
- A full-screen fill on the composition **root** is fine on a normal render. It is dropped only on the layered-composite path (HDR content, or a composition using shader transitions), where the engine forces every composition root transparent so the layer beneath shows through. If your composition uses shader transitions or HDR media, put the fill on a full-bleed **child** (`position:absolute; inset:0`). → `composition-patterns.md`

## Editing existing compositions

- Read the files first. Preserve unrelated timing, tracks, IDs, variables, media paths.
- To know what is on a project's timeline (tracks, clips, starts, ends, what plays), run `npx hyperframes timeline [--json]` instead of reading `index.html` and every sub-composition file.
- Match existing composition IDs and timeline keys.
- Adding a clip: set its `data-start`/`data-duration` intentionally against the clips around it. `data-track-index` is a Studio display lane, not a timing constraint, so it does not need to be free.
- A clip that ends past the root `data-duration` is cut off: extend the root `data-duration` to the clip's end in the same edit (`lint` warns `clip_ends_past_root_duration`).
- A clip nested inside another timed element counts its `data-start` from the composition, not from that
  element, and shows only while that element shows. `timeline` lists it under its parent and warns
  `never visible` when the windows miss (`lint` reports `nested_clip_never_visible`).
- `data-hidden` on any composition element hides it in BOTH preview and render, overriding its time window; it is non-destructive/reversible and toggled by Studio's timeline eye icon.
- Adding a sub-composition: verify its internal `data-composition-id` before wiring the host.

## Validation

Use `hyperframes-cli` for command details

- [ ] `npx hyperframes check` passes (0 findings across lint, runtime, layout, motion, and contrast)
- [ ] Projects with sub-compositions: `npx hyperframes snapshot --at <midpoints>` and eyeball each frame
- [ ] `npx hyperframes preview --background` for review (the user can edit anything in Studio's timeline, and the server survives the invoking command)
- [ ] `npx hyperframes render` only after the user approves


<!-- ===== FILE: hyperframes/hyperframes-core/references/composition-patterns.md ===== -->

# Composition Patterns

How to architect a project: the `index.html` orchestrator at scale, and the common sub-composition archetypes. Pair with `minimal-composition.md` (single-file shape) and `sub-compositions.md` (mechanics of a sub-comp file).

## Two Architectures

|                       | Monolithic (single file)                                | Modular (sub-compositions)                                                           |
| --------------------- | ------------------------------------------------------- | ------------------------------------------------------------------------------------ |
| Project layout        | `index.html` only                                       | `index.html` + `compositions/<scene>.html` per scene                                 |
| Where scenes live     | Inline `<section class="clip">` siblings under the root | Each scene is a separate file wrapped in `<template>`                                |
| Timeline registration | One timeline keyed at the root's `data-composition-id`  | Root timeline (often near-empty) + one timeline per sub-comp, each keyed by its `id` |
| Routing entry         | `references/minimal-composition.md`                     | `references/sub-compositions.md`                                                     |

Both architectures use the same runtime contract — `data-*` attributes + `window.__timelines[id]`. The choice is structural, not behavioral.

## Modular Orchestrator Pattern

When using sub-compositions, `index.html` should be **thin**. Its job is to declare slots, lay them out in time, mount the audio track, and register a (usually empty) root timeline. All scene animation lives inside the sub-comps.

```html
<!doctype html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <script src="https://cdn.jsdelivr.net/npm/gsap@3.14.2/dist/gsap.min.js"></script>
    <style>
      body {
        margin: 0;
        background: #000;
      }
      #root {
        position: relative;
        width: 100%;
        height: 100%;
        overflow: hidden;
      }
      /* Sub-comp slots stretch to fill the root. */
      [data-composition-id="root"] > div[data-composition-src] {
        position: absolute;
        inset: 0;
      }
    </style>
  </head>
  <body>
    <div
      id="root"
      data-composition-id="root"
      data-width="1920"
      data-height="1080"
      data-duration="30"
    >
      <!-- Sequential scenes — each one a sub-composition slot. -->
      <div
        id="el-intro"
        data-composition-id="intro"
        data-composition-src="compositions/intro.html"
        data-start="0"
        data-duration="6"
        data-track-index="1"
      ></div>

      <div
        id="el-body"
        data-composition-id="body"
        data-composition-src="compositions/body.html"
        data-start="6"
        data-duration="18"
        data-track-index="1"
      ></div>

      <div
        id="el-outro"
        data-composition-id="outro"
        data-composition-src="compositions/outro.html"
        data-start="24"
        data-duration="6"
        data-track-index="1"
      ></div>

      <!-- Continuous audio at the root — survives scene cuts. -->
      <audio
        id="el-bgm"
        src="assets/bgm.mp3"
        data-start="0"
        data-duration="30"
        data-track-index="10"
        data-volume="0.6"
      ></audio>
    </div>

    <script>
      window.__timelines["root"] = gsap.timeline({ paused: true });
    </script>
  </body>
</html>
```

Key properties of this layout:

- **Visual scenes on the same `data-track-index`** (e.g. `1`), authored sequentially. For a cross-fade, overlap their times by the fade duration; giving the incoming scene its own track keeps Studio's timeline readable, but the render accepts an overlap either way.
- **Audio on a separate, higher track index** (e.g. `10`). Keeps the linter's overlap rules clear of any visual collisions.
- **Root timeline is near-empty.** All animation lives in the sub-comps. A root-level fade-to-black at the very end is fine; do not stage a parallel animation track from the root.
- **Host slot ids** use `el-<name>` or `<scene-id>`. The slot's `data-composition-id` must still equal the sub-comp's internal id (see `sub-compositions.md`).

## Sub-Composition Archetypes

### A. Content scene (default)

The sub-comp contains the scene's full DOM, scoped CSS, and timeline. This is the standard pattern in `sub-compositions.md` — most scenes are this.

### B. Host media + main-timeline driver (one pattern for `<video>`/`<audio>`)

`<video>`/`<audio>` seek and decode at any nesting depth, so a scene-specific clip can live inside its scene's sub-comp with scene-local `data-start` and be driven by that sub-comp's own timeline. Use this host-media pattern instead when you want the media's motion authored on the **main** timeline: put the `<video>`/`<audio>` as a host-root sibling positioned over the scene's frame.

The reason to reach for it: a sub-comp timeline **cannot** drive host elements (a global selector or `document.querySelector` does not resolve across the boundary). So if the media lives at the host root, author its per-scene motion (scale/opacity/morph/tilt/breathing) on the **main timeline** in `index.html`, at **global time** = scene-local time + the scene slot's `data-start`.

```html
<!-- index.html (host) -->
<div
  id="el-final"
  data-composition-id="final-anim"
  data-composition-src="compositions/final-anim.html"
  data-start="20"
  data-duration="6"
  data-track-index="1"
></div>

<!-- media is a DIRECT root child; sits over the sub-comp's frame -->
<video
  id="final-video"
  class="clip"
  src="assets/final.mp4"
  data-start="20"
  data-duration="6"
  data-track-index="2"
  muted
  playsinline
  style="position:absolute; left:360px; top:100px; width:1200px; height:680px; object-fit:cover; border-radius:24px;"
></video>

<script>
  // MAIN timeline drives the host video. Global time: scene starts at 20.
  const main = window.__timelines["main"];
  main.fromTo(
    "#final-video",
    { scale: 1.4, filter: "blur(14px)" },
    { scale: 1.0, filter: "blur(0px)", duration: 0.9, ease: "power3.out" },
    20,
  ); // = slot data-start (+ any scene-local offset)
</script>

<!-- compositions/final-anim.html — frame/shell only, no <video>, no host-element animation -->
<template>
  <div
    data-composition-id="final-anim"
    data-width="1920"
    data-height="1080"
    data-duration="6"
    style="position:absolute; inset:0; pointer-events:none;"
  >
    <script>
      const tl = gsap.timeline({ paused: true });
      // animate ONLY this sub-comp's own elements here (labels, frame, overlays)
      window.__timelines["final-anim"] = tl;
    </script>
  </div>
</template>
```

Caveats:

- In this pattern the media is a host-root child, static in `index.html`, so the main timeline's selector resolves it. (Media nested in a sub-comp is also driven fine; it just can't be reached by the main timeline's selectors — drive it from the sub-comp's own timeline.)
- Clip lifecycle owns the media element's visibility across its `[data-start, data-start+data-duration]` window. The main-timeline opacity/scale tweens compose with it fine; for an opacity reveal/crossfade prefer a host **wrapper** so you are not fighting the lifecycle on the media element itself.
- Two media elements sharing the same `src` + `data-start` trigger `duplicate_media_discovery_risk` (benign — both still render).

### C. Multi-scene merge

When several beat-level scenes share continuous state — a chat thread that grows, a persistent headline word that carries across the cut, a single canvas with internal phase changes — collapse them into one sub-comp and use **internal phase divs** rather than multiple sub-comp slots.

```html
<!-- compositions/act2-merged.html -->
<template>
  <div data-composition-id="act2-merged" data-width="1920" data-height="1080" data-duration="9">
    <style>
      [data-composition-id="act2-merged"] .phase {
        position: absolute;
        inset: 0;
        opacity: 0;
      }
    </style>
    <div class="phase" id="phase-a">…</div>
    <div class="phase" id="phase-b">…</div>
    <div class="phase" id="phase-c">…</div>
    <script>
      const tl = gsap.timeline({ paused: true });
      tl.set("#phase-a", { opacity: 1 }, 0);
      tl.to("#phase-a", { opacity: 0, duration: 0.4 }, 3.0);
      tl.set("#phase-b", { opacity: 1 }, 3.0);
      // …
      window.__timelines["act2-merged"] = tl;
    </script>
  </div>
</template>
```

Reach for this over multiple sequential slots when scenes share DOM, share a canvas, or need to cross-fade with persistent elements (a headline that survives the cut between phases). Each phase is just a div inside the same sub-comp — the parent timeline never has to know about the internal phase boundaries.

### D. Audio at root, reactive visual inside

Audio always lives at the host (`index.html`) as a root-level `<audio>` so playback survives scene cuts. A sub-comp that visualizes audio should read a **pre-baked** frequency curve at init, then sample the baked curve from its timeline — the visual must still be a deterministic function of `tl.time()`, not of `audio.currentTime`. See `determinism-rules.md` and `hyperframes-creative` for the authoring pattern.

## Naming Conventions

| Thing                               | Convention                                  | Example                                    |
| ----------------------------------- | ------------------------------------------- | ------------------------------------------ |
| Sub-comp file                       | `compositions/<scene-id>.html`              | `compositions/act0-intro-bell.html`        |
| Sub-comp `<template>` id (optional) | `<scene-id>-template`                       | `<template id="act0-intro-bell-template">` |
| Sub-comp root `data-composition-id` | `<scene-id>` (must match host slot)         | `data-composition-id="act0-intro-bell"`    |
| Timeline registry key               | matches `data-composition-id`               | `window.__timelines["act0-intro-bell"]`    |
| Host slot `id`                      | `el-<short>` or `<scene-id>`                | `id="el-intro"`, `id="act0"`               |
| Element ids inside a sub-comp       | prefix with the scene id                    | `#act0-bell`, `#b1-tape`                   |
| Audio at root                       | `data-track-index` well above visual tracks | `10` while visuals use `1`                 |

The `-template` suffix on `<template>` is conventional but not required — the runtime extracts contents from whichever `<template>` is in `<body>`, regardless of id. The prefix on inner element ids is the only safeguard against id collisions when multiple sub-comps are mounted into the same host page at once.


<!-- ===== FILE: hyperframes/hyperframes-core/references/creator-editing-recipes.md ===== -->

# Creator Editing Recipes

Use these copyable contracts after `tracks-and-clips.md`. Global math: **consumed source = timeline duration × rate**; **natural timeline duration = remaining source / rate**.

Before any edit, run `npx hyperframes timeline` (add `--json` for a machine-readable list) to see the project's tracks and clips instead of reading the HTML.

These recipes keep a video's sound on the `<video>` (`data-has-audio="true"`, no `muted`), so cutting the video cuts its sound. Use a separate `<audio>` only when picture and sound must be cut independently (J/L cuts, replacement audio) or for other sound (music, voiceover) — the recipes that do say so. Silent footage or b-roll: replace `data-has-audio="true"` with `muted` in these blocks.

**Every `<video>` and `<audio>` below carries an `id`, and that is not cosmetic**: `lint` errors with `media_missing_id` on timed media without one, and an id-less `<audio>` is never picked up by the mixer, so the render comes out silent. Keep the ids when you copy a recipe.

## Hard cut

```html
<video
  id="a"
  src="take.mp4"
  data-start="0"
  data-duration="2"
  data-media-start="4"
  data-track-index="0"
  playsinline
  data-has-audio="true"
></video>
<video
  id="b"
  src="take.mp4"
  data-start="2"
  data-duration="3"
  data-media-start="10"
  data-track-index="0"
  playsinline
  data-has-audio="true"
></video>
```

Timeline math: B starts at A start + duration. Source math: each range starts at `data-media-start`; consumed source = timeline duration × rate. Audio follows: the sound moves with each video clip. Owner: `/hyperframes-core`. Limit: adjacent windows only; author the two windows edge to edge. Same-track overlap is valid; both clips paint in CSS order.

## Trim in/out

```html
<video
  id="shot-1"
  src="take.mp4"
  data-start="1"
  data-duration="3"
  data-media-start="6"
  data-track-index="0"
  playsinline
  data-has-audio="true"
></video>
```

Timeline math: visible window is `[1,4]`. Source math: in=6, out=6+3 at 1x; never invent source-end syntax. Audio follows: the sound moves with the video clip, using the same three attributes. Owner: `/hyperframes-core`. Limit: use another clip for another range.

## Split / splice

```html
<video
  id="shot-1"
  src="take.mp4"
  data-start="0"
  data-duration="2"
  data-media-start="0"
  data-track-index="0"
  playsinline
  data-has-audio="true"
></video>
<video
  id="shot-2"
  src="take.mp4"
  data-start="2"
  data-duration="2"
  data-media-start="8"
  data-track-index="0"
  playsinline
  data-has-audio="true"
></video>
```

Timeline math: splice at t=2. Source math: independent source offsets select kept pieces. Audio follows: the sound moves with each video clip, so it splits identically. Owner: `/hyperframes-core`. Limit: source cuts are core, never keyframes.

## Duplicate / reuse same source

```html
<video
  id="shot-1"
  src="take.mp4"
  data-start="0"
  data-duration="1"
  data-media-start="2"
  data-track-index="0"
  playsinline
  data-has-audio="true"
></video>
<video
  id="shot-2"
  src="take.mp4"
  data-start="4"
  data-duration="1"
  data-media-start="2"
  data-track-index="0"
  playsinline
  data-has-audio="true"
></video>
```

Timeline math: copies may occupy different starts. Source math: identical offsets reuse identical source. Audio follows: the sound moves with each video clip, so each copy carries its own. Owner: `/hyperframes-core`. Limit: every element needs a unique id when ids are present.

## Reorder

```html
<video
  id="shot-1"
  src="take.mp4"
  data-start="0"
  data-duration="2"
  data-media-start="10"
  data-track-index="0"
  playsinline
  data-has-audio="true"
></video>
<video
  id="shot-2"
  src="take.mp4"
  data-start="2"
  data-duration="2"
  data-media-start="2"
  data-track-index="0"
  playsinline
  data-has-audio="true"
></video>
```

Timeline math: `data-start` defines authored order. Source math: source offsets need not be chronological. Audio follows: the sound moves with the video clip, so reordering clips reorders their sound. Owner: `/hyperframes-core`. Limit: reordering changes placement only, not source ranges.

## Freeze / hold

```html
<img src="held-frame.png" data-start="2" data-duration="1" data-track-index="0" class="clip" />
```

Timeline math: the still owns its hold duration. Source math: final-source frame, subcomp final state, and visual pose holds are supported. Audio follows: continue, trim, or silence audio deliberately. Owner: `/hyperframes-core` + `/media-use`. Limit: arbitrary mid-source freeze requires preprocess of a still/segment.

## Constant speed / slow motion

```html
<video
  id="shot-1"
  src="take.mp4"
  data-start="0"
  data-duration="2"
  data-media-start="4"
  data-playback-rate="0.5"
  data-track-index="0"
  playsinline
  data-has-audio="true"
></video>
```

Timeline math: duration is authored timeline time. Source math: consumed source = timeline duration × rate; natural timeline duration = remaining source / rate. Audio follows: the sound moves with the video clip and plays at the same constant rate. Owner: `/hyperframes-core`. Limit: normalized 0.1..10. For a speed ramp put a `rate` lane in `data-automation`, e.g. `{"version":1,"lanes":[{"target":"rate","points":[{"t":0,"v":1},{"t":2,"v":4}]}]}`; it wins over the constant.

## Zoom / punch

```js
tl.to("#clip .inner", { scale: 1.35, xPercent: -8, duration: 0.18 }, 1);
```

Timeline math: tween positions are composition seconds. Source math: unchanged; the core clip still selects source time. Audio follows: unchanged unless separately edited. Owner: `/hyperframes-keyframes`. Limit: target the inner wrapper, not the timed clip element.

## Pan / Ken Burns

```js
tl.fromTo(
  "#clip .inner",
  { scale: 1.05, xPercent: 0 },
  { scale: 1.2, xPercent: -12, duration: 4, ease: "none" },
  0,
);
```

Timeline math: move spans four authored seconds. Source math: unchanged. Audio follows: the sound stays on the video clip; the tween does not touch it. Owner: `/hyperframes-keyframes`. Limit: authored geometry, not automatic face tracking.

## Crop / reframe

```js
tl.to("#clip .inner", { clipPath: "inset(8% 12% 6% 10%)", xPercent: -4, duration: 1 }, 2);
```

Timeline math: crop interpolates over `[2,3]`. Source math: unchanged. Audio follows: no automatic change. Owner: `/hyperframes-keyframes`. Limit: inner wrapper only, not temporal trim.

## Clip-path wipe / reveal / mask / split-screen

```js
tl.fromTo(
  "#next .inner",
  { clipPath: "polygon(0 0,0 0,0 100%,0 100%)" },
  { clipPath: "polygon(0 0,100% 0,100% 100%,0 100%)", duration: 0.5 },
  2,
);
```

Timeline math: overlap placed clips for the 0.5s handoff. Source math: each clip keeps its own range. Audio follows: the sound stays on each video clip. Owner: `/hyperframes-keyframes` + `/hyperframes-animation`. Limit: visual mask/polygon/split-screen only; source cuts stay `/hyperframes-core`.

## Crossfade

```html
<div id="a-visual" class="inner">
  <video
    id="a"
    data-start="0"
    data-duration="3"
    data-track-index="0"
    src="a.mp4"
    data-automation='{"version":1,"lanes":[{"target":"volume","points":[{"t":0,"v":1},{"t":2.5,"v":1},{"t":3,"v":0}]}]}'
    playsinline
    data-has-audio="true"
  ></video>
</div>
<div id="b-visual" class="inner">
  <video
    id="b"
    data-start="2.5"
    data-duration="3"
    data-track-index="1"
    src="b.mp4"
    data-automation='{"version":1,"lanes":[{"target":"volume","points":[{"t":0,"v":0},{"t":0.5,"v":1},{"t":3,"v":1}]}]}'
    playsinline
    data-has-audio="true"
  ></video>
</div>
<script>
  const tl = gsap.timeline({ paused: true });
  tl.set("#b-visual", { opacity: 0 }, 0)
    .to("#a-visual", { opacity: 0, duration: 0.5 }, 2.5)
    .to("#b-visual", { opacity: 1, duration: 0.5 }, 2.5);
  window.__timelines["main"] = tl;
</script>
```

Timeline math: distinct tracks overlap by 0.5s with opposing opacity envelopes. Source math: each source range remains independent. Audio follows: opposing volume envelopes on each video's own `data-automation`, because the sound stays on the video. Owner: `/hyperframes-core` + `/hyperframes-keyframes` + `/hyperframes-audio`. Limit: the crossfade is the opacity/volume envelopes, not a source-level dissolve.

## Volume fades / ducking

```html
<audio
  id="music-bed"
  src="music.wav"
  data-start="0"
  data-duration="5"
  data-track-index="10"
  data-automation='{"version":1,"lanes":[{"target":"volume","points":[{"t":0,"v":0},{"t":1,"v":1},{"t":2,"v":1},{"t":2.2,"v":0.3},{"t":3,"v":0.3},{"t":3.2,"v":1},{"t":4,"v":1},{"t":5,"v":0}]}]}'
></audio>
```

Timeline math: lane `t` is clip-local authored time: fade-in 0–1, duck down 2–2.2, hold 2.2–3, duck up 3–3.2, fade-out 4–5. Source math: source selection still uses core attributes. Audio follows: the explicit down-hold-up envelope affects this `<audio>` (music is separate sound). The same lane works on a `<video data-has-audio="true">`. Owner: `/hyperframes-audio`. Limit: automation is not source retiming.

**One rule for volume over time: use the lane.** `lint` accepts a timeline tween on `volume` too, but when a track has both, the lane wins and the tween is ignored (`audio_volume_double_automation`). Never add a lane to a track that already has a `volume` tween, and never add a tween to a track that has a lane; edit the one that exists. To ramp 0.1 to 0.5 over ten seconds, write `{"t":0,"v":0.1},{"t":10,"v":0.5}`. `t` is seconds from the clip's own start, so a ramp past `data-duration` never finishes: check the clip's length before choosing the times. `data-volume` stays as the static level of the clip and combines with nothing else you author here.

## Audio alignment

```html
<video
  id="shot-1"
  src="take.mp4"
  data-start="3"
  data-duration="2"
  data-media-start="8"
  data-playback-rate="2"
  data-track-index="0"
  playsinline
  data-has-audio="true"
></video>
```

Timeline math: picture and sound share start/duration because the sound stays on the clip (`data-has-audio="true"`). Source math: both consume four source seconds. Audio follows: identical timing, range, and rate, with nothing to keep in sync. Owner: `/hyperframes-core` + `/hyperframes-audio`. Limit: no waveform auto-sync or drift correction.

A J cut or L cut is the case that needs a separate `<audio>`: picture and sound are cut independently, so the sound gets its own element (the same goes for replacement audio, a voiceover, or music). Mute the video whose sound you are replacing.

```html
<!-- Outgoing shot: picture runs 0-5, its own sound is a separate clip that ends at the audio cut (4). -->
<video
  id="shot-1"
  src="intro.mp4"
  data-start="0"
  data-duration="5"
  data-track-index="0"
  muted
  playsinline
></video>
<audio
  id="shot-1-audio"
  src="intro.mp4"
  data-start="0"
  data-duration="4"
  data-track-index="10"
></audio>
<!-- Incoming shot: picture starts at 5, its sound leads it by one second. -->
<video
  id="shot-2"
  src="take.mp4"
  data-start="5"
  data-duration="3"
  data-media-start="12"
  data-track-index="0"
  muted
  playsinline
></video>
<audio
  id="shot-2-audio"
  src="take.mp4"
  data-start="4"
  data-duration="4"
  data-media-start="11"
  data-track-index="10"
></audio>
```

The sound leads the picture by one second (a J cut): `shot-2-audio` starts at 4 and reads from source 11, while the picture starts at 5 and reads from 12. Both stay on the same source clock. Every video in a J or L cut is `muted` and its sound is its own `<audio>`: the outgoing shot's `<audio>` ends at the audio cut (4) while its picture carries on to 5, so two sounds never overlap on the same source. An audible `<video>` and an `<audio>` on the same file are only flagged when their time windows overlap.

## Align a sound to an on-screen event

```html
<audio
  id="sfx-click-3"
  src="click.mp3"
  data-start="7.48"
  data-duration="0.07"
  data-track-index="103"
  data-volume="0.85"
></audio>
```

Timeline math: an audio element in the root composition has `data-start` in absolute root time; audio inside a scene file uses scene-local time and the host's `data-start` is added for you. An event inside a sub-composition happens at the host's `data-start` plus the event's local time in that sub-composition's own timeline, so `data-start = host start + local time`. Move only the audio's `data-start`; leave the picture alone. Source math: if the sound's transient is not at the file's first sample, subtract that lead-in from `data-start` (or trim it with `data-media-start`). Audio follows: nothing links audio to picture, so re-derive after every retime of the host. Owner: `/hyperframes-core`. Limit: no waveform auto-sync; for a beat grid use `hyperframes beats` and place each start on a beat time.

## Copy a group of clips to another time

```html
<audio
  id="sfx-click-0"
  src="click.mp3"
  data-start="1.6"
  data-duration="0.07"
  data-track-index="100"
></audio>
<audio
  id="sfx-type-0"
  src="typenew.mp3"
  data-start="7.8"
  data-duration="0.57"
  data-track-index="109"
></audio>
<audio
  id="sfx-click-0-copy"
  src="click.mp3"
  data-start="41.6"
  data-duration="0.07"
  data-track-index="186"
></audio>
<audio
  id="sfx-type-0-copy"
  src="typenew.mp3"
  data-start="47.8"
  data-duration="0.57"
  data-track-index="187"
></audio>
```

Timeline math: pick the clips first and say which ones you picked (by id) if the request does not match the file exactly; then add one `delta` to every member's `data-start`, so relative spacing is preserved (here `delta = 40`). Give each copy a new unique `id` and the next unused `data-track-index`; keep `src`, `data-duration`, `data-media-start`, `data-volume` and any `data-automation` as they are. Leave the originals untouched. Check the copies still end inside the composition's duration. Owner: `/hyperframes-core`. Limit: copies of a `<video>` or a sub-composition host follow the same rule, and a copied sub-composition needs its own host `id`.

## Add media (image, video, audio)

Write what Studio writes when a person drops a file on the timeline, so an agent-added clip behaves the same as a dropped one; the one difference is that video and audio need no `data-duration`. Studio's source of truth is `DEFAULT_TIMELINE_ASSET_DURATION` in `packages/studio/src/utils/studioHelpers.ts` and `buildTimelineAssetInsertHtml` in `packages/studio/src/utils/timelineAssetDrop.ts`; a test keeps this section equal to them.

- **Image: `data-duration` is optional and defaults to 3 seconds**, the same as a dropped image, because a still has no length of its own. Write it only for another length. A test keeps the 3 equal to the default in code.
- **Video and audio: `data-start` is enough.** The length comes from the media itself. An authored `data-duration` shorter than the file is a trim, never a requirement; leave it out unless the request asks for a shorter clip.
- **Start: the playhead or the requested time, never a silent `0`.** Studio's asset-panel Add uses the playhead time on track `0`; a drop uses the drop point.
- Give every clip `id`, `class="clip"`, `data-start` and `data-track-index`. A video with sound is `playsinline data-has-audio="true"`; silent footage and b-roll is `muted playsinline`. Audio carries `data-volume="1"`.
- Then make sure the root composition's `data-duration` is at least the clip's end (`data-start` plus its length: 3 for an image unless you set another, the media's length for video and audio): Studio raises a declared root duration to cover the new clip, so an agent must too, or the clip lies past the end and never plays.
- **Images and video fill the whole frame**: absolutely positioned at `left: 0; top: 0`, `width` and `height` equal to the composition's `data-width` and `data-height`, `object-fit: contain`. Studio does not know a dropped file's natural size, so it does not centre a smaller one.
- `z-index` is the number of top-level clips already in that file plus one (at least `1`); later clips stack above earlier ones.
- Several files dropped together share the drop's track and run end to end.

```html
<img
  id="photo"
  class="clip"
  src="assets/photo.png"
  data-start="4"
  data-track-index="1"
  style="position: absolute; left: 0px; top: 0px; width: 1920px; height: 1080px; object-fit: contain; z-index: 2"
/>
```

```html
<video
  id="broll"
  class="clip"
  src="assets/broll.mp4"
  data-start="4"
  data-track-index="2"
  muted
  playsinline
  style="position: absolute; left: 0px; top: 0px; width: 1920px; height: 1080px; object-fit: contain; z-index: 3"
></video>
```

```html
<audio
  id="whoosh"
  class="clip"
  src="assets/whoosh.mp3"
  data-start="4"
  data-track-index="3"
  data-volume="1"
></audio>
```

Inside a sub-composition file, `data-start` is scene-local (see `## Align a sound to an on-screen event`). Owner: `/hyperframes-core`.

## Swap a media file

```html
<video
  id="hero"
  src="assets/product-v2.mp4"
  data-start="2"
  data-duration="4"
  data-media-start="0"
  data-track-index="0"
  playsinline
  data-has-audio="true"
></video>
```

Timeline math: change only `src`. Source math: reset `data-media-start` to the offset you want in the NEW file, and set `data-duration` no longer than the new file's remaining length (probe it with `ffprobe`). Audio follows: the sound moves with the video clip; a separate `<audio>` that pointed at the old file (music, voiceover) needs its own `src` swap. Keep `id`, `data-start`, `data-track-index` and any `data-automation` so nothing else moves. Run `lint`: `audio_src_not_found` and `media_src_kind_mismatch` catch a wrong path or kind. Owner: `/hyperframes-core`. Limit: a still swapped for a video (or the reverse) is a tag change, not a swap.

## Split a section and change its speed

Timeline math: a section that is a sub-composition or a group of clips has no `data-playback-rate` of its own to set; split it by giving each half its own host or clips and shift everything after the cut by the length change. New length of a part = old length / rate. Every later `data-start` (clips, audio, root-timeline tweens) moves by the same delta. Source math: `<video>` and `<audio>` parts use `data-playback-rate` (0.1 to 10, constant) per the constant-speed recipe above, the sound moves with the video. A speed ramp (a rate that changes within one clip) is a `rate` lane in `data-automation` on the `<video>`/`<audio>`; see `docs/reference/speed-ramps`. Say which you did.


<!-- ===== FILE: hyperframes/hyperframes-core/references/data-attributes.md ===== -->

# Data Attributes Reference

Every HyperFrames composition uses `data-*` attributes to declare timing and structure to the framework. This is the full attribute table — pair with `tracks-and-clips.md` for the rules behind `data-track-index`.

## Composition Root

Every renderable composition needs one root element:

| Attribute                    | Required      | Meaning                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                  |
| ---------------------------- | ------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `data-composition-id`        | Yes           | Unique ID. Must match the animation registry key on `window.__timelines`.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                |
| `data-width` / `data-height` | Yes           | Pixel frame size. Common values: `1920x1080`, `1080x1920`, `1080x1080`.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                  |
| `data-duration`              | Conditional\* | Render duration in seconds (total length / frame count), not the GSAP timeline length. **Read once at compile time, like `data-width` / `data-height`**: a static root `data-duration` is locked before scripts run, so a script (`root.setAttribute("data-duration", ...)`) or a `--variables`-driven value cannot change the render length. To vary length per render, author the root `data-duration` directly. (A clip's `data-duration` is different: re-read from the live DOM, so scripts/variables can drive it.) Only when the root omits `data-duration` does the renderer derive total length from the live DOM / timeline after scripts run. |
| `data-fps`                   | No            | Optional frame rate hint. CLI render flags can override output fps.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                      |
| `data-composition-variables` | No            | JSON array of variable declarations (on `<html>`). See `variables-and-media.md`.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                         |

\*`data-duration` is optional whenever the runtime can auto-infer duration: a registered GSAP timeline, a finite CSS animation, a finite WAAPI `element.animate()`, a registered Lottie animation, or timed clips (the root then ends at its latest clip end, and lint only warns `root_composition_duration_derived`). It is **required** for Three.js (no auto-inference), for infinite/unbounded CSS or WAAPI animations, and for any composition with no GSAP timeline, no animation signal and no timed clip with a length. `npx hyperframes lint` enforces this (`root_composition_missing_duration_source`). Per-runtime inference lives in `hyperframes-animation/adapters/`.

The root should be `position: relative`, have explicit pixel dimensions, and hide overflow unless intentionally composing outside the frame.

## Clip Attributes

**`data-start` is what makes an element a clip.** The runtime collects `[data-start]` and drives visibility off that attribute, so any element carrying it is timed.

`class="clip"` is a **convention, not a requirement**: the runtime never reads it. Keep writing it: drop it and the full-frame box collapses unless you supply that layout yourself, Studio uses it as an edit hint, and `lint` warns (`timed_element_missing_clip_class`) when a timed element lacks it. Omit it on `<video>` and `<audio>`.

**Nesting is allowed.** A timed element inside a wrapper is still timed, and a timed ancestor clamps its descendants: a child cannot be visible while its timed ancestor is hidden. Direct children of the root get automatic layout (see "Root-level clips get automatic layout" below); nested ones do not, so give them their own positioning.

| Attribute          | Required                                           | Meaning                                                                                                                                                                                                                                                                                                                                                            |
| ------------------ | -------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| `id`               | Yes on `<video>`/`<audio>`, else recommended       | `lint` errors with `media_missing_id` on media without one, and an id-less `<audio>` is never mixed, so the render is **silent**. Elsewhere it is a warning (`studio_missing_editable_id`): Studio needs a stable edit target, and timeline targets reference it.                                                                                                  |
| `data-start`       | Yes                                                | Start time in seconds, or a supported clip-time reference. This attribute is what marks the element as timed.                                                                                                                                                                                                                                                      |
| `data-duration`    | Required for `div` and sub-compositions            | Duration in seconds. An `img` with `data-start` defaults to 3 s; video/audio default to the source length (less the playback offset, over the rate) once known; an authored value trims. Without any resolvable duration the element has no end and stays visible for the rest of the composition.                                                                 |
| `data-track-index` | No                                                 | Studio timeline lane, display only. The render never reads it, and clips on one track may overlap in time. Absent, the parser defaults it and Studio lays out one lane per clip. Two `<audio>` elements on the same index that overlap in time raise a `lint` warning.                                                                                             |
| `data-media-start` | No                                                 | Offset into the media source, in seconds.                                                                                                                                                                                                                                                                                                                          |
| `data-volume`      | No                                                 | Static audio gain, default `1` (0 dB). `0` is silence and values above `1` boost, up to `3.98` (+12 dB) — Studio's fader writes this. For fades and ducking, use the `data-automation` volume lane (see `creator-editing-recipes.md`).                                                                                                                             |
| `data-has-audio`   | Required on a timed `<video>` unless it is `muted` | `"true"` keeps the file's sound on this clip (the default for footage with sound). Silent footage uses `muted` instead; a video with neither fails lint (`video_missing_muted`).                                                                                                                                                                                   |
| `data-link`        | No                                                 | Editing contract only (render ignores it): clips sharing an id, e.g. a video and the `<audio>` detached from it in Studio, are edited as one. Keep every member's `data-start`, `data-duration`, `data-media-start` and `data-playback-rate` equal; to unlink, remove the attribute from all members. See [tracks-and-clips.md](tracks-and-clips.md#linked-clips). |
| `data-sync-origin` | No                                                 | Editing contract only: a video and audio from one source file share it (written by Detach, and by Link for same-file pairs; kept by Unlink). Studio flags the pair out of sync when their source-zero points differ. See [tracks-and-clips.md](tracks-and-clips.md#linked-clips).                                                                                  |

**The visibility window is half-open: `[start, start + duration)`.** A clip shows while `start ≤ t < start + duration` and is hidden at exactly `t = start + duration`. Land an animation's resolved end state slightly **before** `data-duration`, not on it, or its last frame is never rendered. Two clips can therefore be authored back to back (`b.start === a.start + a.duration`) with no overlapping frame.

**Root-level clips get automatic layout.** For direct children of the composition root that carry `data-start`, the runtime forces `position: absolute` and anchors them at `top: 0; left: 0`, sizing them to 100% when they have no computed size, so scenes stack in the same viewport layer. Elements **without** `data-start` are skipped entirely: an untimed full-bleed background needs its own `position: absolute; inset: 0`, or it collapses to zero height.

## Sub-Composition Host Attributes

When a clip is a sub-composition host (loads another composition file):

| Attribute                    | Required    | Meaning                                                                                                                                                     |
| ---------------------------- | ----------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `data-composition-id`        | Recommended | The composition ID of the loaded file. Matching it is the convention; a host that names a different id, or none at all, is supported but resolves silently. |
| `data-composition-src`       | Yes         | Path to the sub-composition HTML file.                                                                                                                      |
| `data-width` / `data-height` | No          | Render dimensions for the instance. The compiler backfills them from the loaded file's root when absent.                                                    |
| `data-variable-values`       | No          | Per-instance variable overrides as JSON. See `variables-and-media.md`.                                                                                      |
| `data-var-src`               | No          | Binds the element's `src` to a declared variable id (media/image substitution, authored src = fallback).                                                    |
| `data-var-text`              | No          | Binds the element's own text to a scalar variable id; children are preserved.                                                                               |

See `sub-compositions.md` for the full wiring pattern.

## Authoring Hints

- `id="root"` — template convention used by scaffolds and the transition catalog so CSS can target the composition root with `#root` instead of `[data-composition-id="main"]`. Not required by the runtime, but consistent with the rest of the ecosystem.
- `class="clip"`: layout and tooling convention on visible timed elements (`<div>`, `<img>`, …), not a runtime requirement. See Clip Attributes above.
- `data-root="true"`: names the composition root explicitly. Without it the runtime picks the outermost `[data-composition-id]` element, which is right for almost every file; set it when compositions nest and you need to be unambiguous.
- `data-layout-allow-overflow` — tells `hyperframes check` that overflow on this element (or its descendants) is intentional. Notes:
  - The `check` layout audit measures `getBoundingClientRect` at sampled timestamps, not rendered pixels. `overflow: hidden` clips the visual but does **not** suppress a layout finding. This attribute is the escape hatch; CSS overflow is not.
  - Can be set on the composition **root** as well as on any child. When the cited offender is `div.<comp>-root inside div.<comp>-root` (the root reports its own children's union as overflowing), the fix goes on the root, not on individual text descendants — shrinking font sizes will not converge.
  - In a multi-scene `group_wN.html` (continue runs), every scene-local element stays in the DOM during the other scenes' time windows; the layout-box union almost always overflows the canvas during morph seams. Mark the root and every scene-local primary/supporting element with this attribute **at construction**, not after `check` flags it.
  - **Blast radius — it silences more than the overflow audit.** The attribute is inherited down the subtree (the perception probe walks ancestors), so it also suppresses the rendered-perception checks `text-clipping`, `content-cramped-container`, and `foreground-over-panel` for every descendant. Putting it on a persistent panel that also hosts real foreground content disables collision checks on that content for the panel's whole lifetime. Prefer the narrowest opt-out: scope it to the smallest decorative wrapper, or use per-element `data-layout-bleed="true"` for one intentional primary-text crop. The two canvas/edge checks `primary-offscreen` and `foreground-over-panel` deliberately run **even under** allow-overflow, so it cannot hide a wordmark sliced by the frame or text bleeding onto a panel edge.
- `data-layout-ignore` — exclude this element from layout audits entirely.
- `data-layout-allow-caption-zone` — opt out of `--caption-zone` / `caption_zone_collision` for intentional lower-third copy (applies to the element and every descendant via `closest`; does **not** suppress overflow, overlap, occlusion, or other layout audits — pair those attrs if needed).

## Legacy / Removed Attributes

These names appear in older projects and examples. Use the current names when authoring or editing:

| Legacy name  | Use instead        |
| ------------ | ------------------ |
| `data-layer` | `data-track-index` |
| `data-end`   | `data-duration`    |


<!-- ===== FILE: hyperframes/hyperframes-core/references/determinism-rules.md ===== -->

# Determinism, Animation Runtime, and Layout

HyperFrames seeks compositions frame-by-frame. Every frame must be reproducible from its time value alone — same input time → same pixels. Three contracts enforce this: the **animation runtime contract**, the **determinism rules**, and the **layout contract**.

## Animation Runtime Contract

GSAP is the primary runtime. The core requirement is generic: animation state must be seekable from HyperFrames time.

For GSAP:

- Use `gsap.timeline({ paused: true })`.
- Register it on `window.__timelines["<composition-id>"]`, keyed by the composition root's `data-composition-id`. You do **not** need to write `window.__timelines = window.__timelines || {}` first: the runtime creates the registry before your inline scripts evaluate.
- **Building inside an async callback is supported.** `document.fonts.ready(...)` and friends are the documented setup path. What you must not do is **register the key before the build finishes**. An empty timeline registered early is treated as ready and nested empty, so the animation renders blank (`lint`: `gsap_timeline_registered_before_async_build`, error). Assign `window.__timelines[id] = tl` at the **end** of the callback, after the tweens are added, and optionally call `window.__hfForceTimelineRebind()` right after.
- If the key does not match the root's `data-composition-id`, the runtime still binds it **when it is the only registered timeline**. With two or more registered, a mismatched key leaves the render frozen at t=0.
- **Do not** call `tl.play()` for render-critical motion.
- **Do not** create empty tweens only to set duration; use `data-duration` on the clip instead.

Use the `hyperframes-animation` skill for tween syntax, position parameters, eases, and performance rules. Non-GSAP duration inference lives in `hyperframes-animation/adapters/`.

## Determinism Rules

Rendered frames must be reproducible from the requested time. Do **not** use any of the following for visual state:

- `Date.now()`, `performance.now()`, or any render-time clock.
- Unseeded `Math.random()`. Use a seeded PRNG if random-looking placement is needed.
- Render-time network fetches for required assets. Inline or pre-bundle them.
- Hover, scroll, pointer, or focus state. The renderer has no input events.
- Unbounded infinite loops. `repeat: -1` is allowed only when the root declares a finite `data-duration` — deterministic seeking and export clip to that explicit window (`gsap_infinite_repeat` demotes to a warning). Without a finite composition duration it stays a hard error: the timeline can report an unbounded length and render planning fails. When the loop itself must end **before** the composition does, compute a finite count: `repeat: Math.max(0, Math.floor(duration / cycleDuration) - 1)` — **`floor`, not `ceil`** (`ceil` overshoots `data-duration` and trips the `gsap_repeat_ceil_overshoot` lint; `max(0, …)` avoids a negative repeat = infinite).

Also avoid:

- Tweening `display`, raw `visibility`, or `autoAlpha` **on a clip element**: HyperFrames timing owns a clip's visibility, and `lint` rejects it (`gsap_animates_clip_element`). Fade with `opacity`, or tween a child wrapper. Do not tween `class="clip"`.
- There is no fixed allowlist of animatable properties. `lint` enforces a **denylist**, so `filter`, `clipPath`, `strokeDashoffset`, `width`, `height` and similar are all legitimate targets. Prefer transforms and opacity where you have the choice, for performance rather than correctness. The per-runtime detail lives in `hyperframes-animation/adapters/`.
- Animating the same property on the same element from multiple timelines at the same time — GSAP's overwrite behavior is order-dependent and can flip between renders.

## Layout Contract

Build the visible end-state in static HTML and CSS first, then animate from/to that state.

- The composition root has fixed pixel frame dimensions.
- **The root composition's total duration (render length / frame count) is fixed at compile time**, read once from the static root `data-duration` before scripts run, like `data-width` / `data-height`. A script or `--variables` value that rewrites the root `data-duration` afterward is ignored. To vary render length per output, author the root `data-duration` directly. (A _clip's_ own `data-duration` is re-read from the live DOM, so scripts/variables can still drive clip lengths. Only when the root omits `data-duration` does the renderer probe the live DOM / timeline for total length.)
- Scene containers should fill the scene with `width: 100%; height: 100%; box-sizing: border-box`.
- Use padding, flex, grid, and `max-width` for layout. Avoid positioning main content with hardcoded `top`/`left` offsets when a layout container can do it.
- Use `position: absolute` for layers and decorative elements, not as the default content-layout strategy.
- Prefer transforms and opacity for animation.
- Keep text inside its intended container. For dynamic text, use `max-width`, wrapping, or `window.__hyperframes.fitTextFontSize(text, { maxWidth, fontFamily, fontWeight })`.
- For text measurement without DOM reflow, use `window.__hyperframes.pretext`. Measure off a canvas instead of writing into the page and reading it back, so nothing reflows: `pretext.prepare(text, font)` then `pretext.layout(prepared, maxWidth, lineHeight)` → `{ lineCount, height }`. `prepare` does the font measurement; everything downstream of a prepared string is arithmetic and cheap enough to run per frame. `fitTextFontSize` is built on it.
  - `layout` gives you height, not width. To size a container to its text (shrinkwrap), use `pretext.prepareWithSegments(text, font)` and then `pretext.measureNaturalWidth(prepared)` for the single-line width, or `pretext.measureLineStats(prepared, maxWidth)` for `{ lineCount, maxLineWidth }`.
  - `font` is a CSS font shorthand string, e.g. `"700 90px Inter"`.
  - `clearCache` and `setLocale` are deliberately not exposed: they mutate state shared across compositions, which would make a render depend on what ran before it.
- **Do not** use `<br>` in body text. Forced breaks ignore the actual rendered font width and produce an extra break when the line already wraps naturally, causing overlap. Let text wrap via `max-width`. Exception: short display titles where each word is deliberately on its own line.
- **Transformed elements must be block-level + sized.** `transform`/`scaleX`/`scaleY` is a no-op on an inline `<span>`, and scaling an auto-width (0px) element shows nothing → invisible bars/fills. Give them `display: block`/`inline-block`/flex-item **and** a real `width`/`height` (e.g. `width: 100%` inside a sized parent). _(Silent — automated gates may miss it.)_
- **Absolutely-positioned decoratives that pulse or overshoot** (`yoyo` scale, `back.out`) need clearance at their **peak** size and must not straddle an `overflow: hidden` edge — else they overlap a neighbor or get clipped. Position for the largest frame, not the resting one. _(silent.)_


<!-- ===== FILE: hyperframes/hyperframes-core/references/full-screen-motion.md ===== -->

# Full-Screen Motion Pattern

For full-frame motion (continuous backgrounds, color washes, full-bleed visual states that span multiple clips), prefer a **shared background layer + transparent timed content layers** over stacked opaque scene backgrounds.

## Pattern

```html
<style>
  /* The runtime auto-positions root children that carry data-start. The shared
     background deliberately has none, so it gets NO automatic layout and must
     size itself, or #bg is 0px tall and the tween paints nothing. */
  #bg.full-bleed {
    position: absolute;
    inset: 0;
  }
  .clip.transparent {
    background: transparent;
  }
</style>

<div id="root" data-composition-id="main" data-width="1920" data-height="1080" data-duration="20">
  <!-- Shared background — NOT a clip. Always visible. Driven by the timeline. -->
  <div id="bg" class="full-bleed"></div>

  <!-- Timed content layers — transparent backgrounds. -->
  <section
    id="scene1"
    class="clip transparent"
    data-start="0"
    data-duration="6"
    data-track-index="1"
  >
    <!-- content -->
  </section>
  <section
    id="scene2"
    class="clip transparent"
    data-start="6"
    data-duration="14"
    data-track-index="1"
  >
    <!-- content -->
  </section>
</div>

<script>
  const tl = gsap.timeline({ paused: true });

  // Drive the shared background from the seekable timeline.
  tl.to("#bg", { backgroundColor: "#0a1530", duration: 6, ease: "sine.inOut" }, 0);
  tl.to("#bg", { backgroundColor: "#1a0a30", duration: 14, ease: "sine.inOut" }, 6);

  // Scene-local animations stay transparent on top.
  tl.from("#scene1 h1", { y: 48, opacity: 0, duration: 0.6 }, 0.2);

  window.__timelines["main"] = tl;
</script>
```

## Rules

- **The background is not a clip.** No `data-start` / `data-duration`. It exists for the whole composition.
- **Because it is not a clip, it gets no automatic layout.** The runtime only positions and sizes root children that carry `data-start`. An untimed background must set its own `position: absolute; inset: 0`, or it collapses to zero height and nothing you animate on it is visible. This is the most common way this pattern is copied wrong.
- **Content scenes have transparent backgrounds.** Whatever you put in the shared `#bg` shows through.
- **Drive global state from the shared layer.** Hue shifts, vignettes, grain, film-look filters — animate them once on the shared layer, not per-scene.
- **Do not animate visibility on `.clip` elements.** HyperFrames already shows/hides clips based on `data-start` and `data-duration`. Animating `display` / `visibility` on the clip itself races with the framework's own show/hide. Animate a _child wrapper_ inside the clip instead.
- **Verify intentional overflow with snapshots.** Before adding `data-layout-allow-overflow` to silence an inspect warning, run `npx hyperframes snapshot` and confirm the overflow is what you want.


<!-- ===== FILE: hyperframes/hyperframes-core/references/minimal-composition.md ===== -->

# Minimal Composition

The smallest renderable HyperFrames composition — a standalone (top-level) root with one clip and one tween:

```html
<!doctype html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=1920, height=1080" />
    <title>Minimal HyperFrames Composition</title>
    <script src="https://cdn.jsdelivr.net/npm/gsap@3.14.2/dist/gsap.min.js"></script>
    <style>
      body {
        margin: 0;
        background: #0b0f14;
        color: white;
        font-family: Inter, system-ui, sans-serif;
      }
      #root {
        position: relative;
        width: 100%;
        height: 100%;
        overflow: hidden;
      }
      .clip {
        position: absolute;
        inset: 0;
        display: grid;
        place-items: center;
      }
      h1 {
        margin: 0;
        font-size: 96px;
      }
    </style>
  </head>
  <body>
    <div
      id="root"
      data-composition-id="main"
      data-start="0"
      data-width="1920"
      data-height="1080"
      data-duration="5"
    >
      <section id="title-card" class="clip" data-start="0" data-duration="5">
        <h1 id="title">Hello HyperFrames</h1>
      </section>
    </div>
    <script>
      const tl = gsap.timeline({ paused: true });
      tl.from("#title", { y: 48, opacity: 0, duration: 0.6, ease: "power3.out" }, 0.2);
      window.__timelines["main"] = tl;
    </script>
  </body>
</html>
```

What the runtime actually requires:

- Root `<div>` with `data-composition-id`, `data-width`, `data-height`. Root `data-start="0"` is written above by convention and every shipped block has it, but the runtime stamps it when absent, so it is not required.
- A duration source: root `data-duration` (as above), or a GSAP timeline, or media, or an adapter that can infer one.
- Timed elements carry `data-start` plus a duration. That attribute alone is what makes an element a clip: `class="clip"` is a layout and tooling convention, and `data-track-index` is a Studio display lane. Neither is required, and a composition with no clips at all renders fine.
- A GSAP timeline created paused and registered on `window.__timelines["<composition-id>"]`.

Everything else in the skeleton is ordinary HTML and CSS: the `#root` box, `.clip` positioning, and fonts are yours to choose.

This pattern is **standalone** (top-level `index.html`) — no `<template>` wrapper around the root. For sub-compositions (files loaded by `data-composition-src`), see `sub-compositions.md`.


<!-- ===== FILE: hyperframes/hyperframes-core/references/sub-compositions.md ===== -->

# Sub-Compositions

A sub-composition is a separate HTML file embedded in a host composition. HyperFrames loads it, seeks it independently, and composites the result into the host at `data-start`.

## Host Wiring

In the host composition, the sub-composition appears as a clip with `data-composition-src`:

```html
<div
  id="chart"
  data-composition-id="data-chart"
  data-composition-src="compositions/data-chart.html"
  data-start="2"
  data-duration="8"
  data-track-index="2"
  data-width="1920"
  data-height="1080"
></div>
```

- `data-composition-id` on the host must match the internal `data-composition-id` of the file at `data-composition-src`.
- The host clip needs its own `data-start`, `data-duration`, `data-track-index`, `data-width`, `data-height`.

## Sub-Composition File Structure

### Mental model — what the runtime actually does

When a host loads a sub-composition via `data-composition-src`, the runtime:

1. `fetch`es the HTML file.
2. Parses it with `DOMParser`.
3. **Finds the `<template>` element and clones ONLY its contents into the host slot.**
4. Everything **outside** the `<template>` (including the entire `<head>`) is **discarded**.

So `<template>` is not just a wrapper — it is the **transport container**. If a node needs to exist in the live render, it must be inside `<template>`. Full stop.

### File shape

```html
<!doctype html>
<html>
  <head>
    <meta charset="UTF-8" />
    <!-- head is metadata for the source file only; the runtime ignores it -->
  </head>
  <body>
    <template>
      <!-- EVERYTHING the runtime needs goes here: styles, markup, scripts -->
      <style>
        /* Root: style by #root, never a class. lint: subcomposition_root_styled_by_class. See Pitfall 3. */
        #root {
          position: absolute;
          inset: 0;
          color: #fff;
        }
        /* .label, #bar, … — descendants, plain selectors */
      </style>

      <div id="root" data-composition-id="data-chart" data-width="1920" data-height="1080">
        <!-- sub-composition markup -->
      </div>

      <script>
        const tl = gsap.timeline({ paused: true });
        // ... build timeline ...
        window.__timelines["data-chart"] = tl;
      </script>
    </template>
  </body>
</html>
```

Contrast with **standalone** compositions, which put the root directly in `<body>` with no `<template>` wrapper.

## Common pitfalls that pass static checks but break at render

Static file checks cannot prove the **cross-file mount contract**. These failures appear only when the runtime mounts the sub-composition.

### Pitfall 1 — `<style>` in `<head>` instead of inside `<template>`

```html
<!-- ❌ WRONG — looks normal, ships catastrophically broken -->
<head>
  <style>
    #root { font-size: 88px; ... }
  </style>
</head>
<body>
  <template>
    <div id="root" data-composition-id="data-chart" ...>...</div>
  </template>
</body>

<!-- ✅ RIGHT — styles are inside the template, root styled by #root (see Pitfall 3) -->
<head></head>
<body>
  <template>
    <style>
      #root { font-size: 88px; ... }
    </style>
    <div id="root" data-composition-id="data-chart" ...>...</div>
  </template>
</body>
```

**Why this happens:** standard HTML conventions tell you to put `<style>` in `<head>`. In a standalone HTML file that's correct. In a HyperFrames sub-composition it is **not** — the runtime only clones `<template>` contents, so `<head><style>` is dropped on the floor.

**Symptom:** isolated checks pass and the render completes, but every text element appears as tiny unstyled default text in the top-left and SVGs expand to canvas size because no CSS reached the live DOM. The same trap applies to `<script>` blocks, `<link rel="stylesheet">`, and custom-element registrations: anything that must execute or apply in the render belongs inside `<template>`.

### Pitfall 2 — Host `data-composition-id` ≠ inner template `data-composition-id`

```html
<!-- ❌ WRONG — host renames the slot; runtime can't find the timeline -->
<!-- host file (e.g. index.html) -->
<div data-composition-id="chart-mount" data-composition-src="compositions/chart.html" ...></div>

<!-- chart.html -->
<template>
  <div data-composition-id="data-chart" ...>...</div>
  <script>
    window.__timelines["data-chart"] = tl;
  </script>
</template>

<!-- ✅ RIGHT — both ids match, and the timeline key matches them too -->
<div data-composition-id="data-chart" data-composition-src="compositions/chart.html" ...></div>
<!-- chart.html template root: data-composition-id="data-chart" -->
<!-- timeline: window.__timelines["data-chart"] = tl; -->
```

**Why this happens:** it feels natural to give the host slot a different name like `chart-mount` ("the mount point") vs `data-chart` ("the actual chart"). HyperFrames does not work that way — **the host's `data-composition-id` is the lookup key the framework uses to find the registered timeline**. Lint passes because each file's ids are individually valid; the cross-file mismatch only blows up at render.

**Symptom:** the render logs `Sub-composition timelines not registered after 45000ms: <host-id>` for every mismatched slot, waits 45s per scene, then captures static initial-state frames (so the video is full-length but no animation plays).

### Pitfall 3 — Styling the root by a class instead of `#root`

`lint` still errors (`subcomposition_root_styled_by_class`) if a sub-composition styles the host root's own class. Style the root with `#root`.

## What HyperFrames Does With the Sub-Composition

- Loads the file and registers its timeline under its internal `data-composition-id`.
- Seeks the sub-composition's timeline independently from the host's playhead.
- Plays the sub-composition's content from `data-start` of the host clip, for `data-duration` seconds.

**Do not** manually `master.add(child)` a sub-composition timeline into the host timeline. HyperFrames already drives them independently — nesting them in GSAP causes double-seeks.

### The host clip's `data-duration` is the slot's visible window

`data-duration` on the host clip defines **how long the slot is visible**, and it takes precedence over the sub-composition's internal GSAP timeline length. Two consequences follow:

- **Internal timeline shorter than the slot → the slot holds.** If the sub-composition's GSAP timeline finishes before `data-duration` elapses, the slot keeps showing its final frame for the rest of the window. You do **not** need to pad the timeline with empty tweens.
- **`data-duration` shorter than the host composition → the slot ends (and goes blank) when its own `data-duration` elapses.** This is intended: the clip is a fixed-length window on the timeline, not "fill until the composition ends." To keep a sub-composition visible for the whole composition, set its `data-duration` to span the host window (or add another clip to cover the remaining time). Leaving a single full-bleed sub-composition shorter than the composition is almost always a mistake — the linter flags it as `subcomposition_blanks_before_host`.

## Animations Inside Sub-Compositions

Prefer `gsap.fromTo()` over `gsap.from()` for entrance tweens. The host re-seeks the sub-composition every time its clip becomes visible; `gsap.from()` records the starting state at registration and can desync on seek-back, while `gsap.fromTo()` declares both endpoints explicitly and replays cleanly.

## Per-Instance Variables

If the sub-composition declares variables on its `<html>` element (`data-composition-variables`), the host can override values per instance:

```html
<div
  data-composition-id="data-chart"
  data-composition-src="compositions/data-chart.html"
  data-variable-values='{"title":"Q4 Revenue","accent":"#66d9ef"}'
  data-start="2"
  data-duration="8"
  data-track-index="2"
  data-width="1920"
  data-height="1080"
></div>
```

The host can render the same sub-composition multiple times with different `data-variable-values` to produce per-instance variations. See `variables-and-media.md` for variable declaration syntax.


<!-- ===== FILE: hyperframes/hyperframes-core/references/tailwind.md ===== -->

# HyperFrames Tailwind

HyperFrames `init --tailwind` uses the Tailwind browser runtime pinned by the scaffold. Treat it as Tailwind v4, not Studio's Tailwind v3 setup.

## Version Contract

- **Pinned: `@tailwindcss/browser@4.2.4`** (source of truth: `packages/cli/src/commands/init.ts` `TAILWIND_BROWSER_VERSION`).
- Do not replace the scaffolded runtime with `cdn.tailwindcss.com` (unpinned, defeats reproducibility).
- Keep the readiness shim deterministic; HyperFrames waits for `window.__tailwindReady` before frame 0 capture.
- For offline / locked-down / production-stable renders, compile Tailwind to CSS and ship the stylesheet instead of the browser runtime.

## v4 Browser Runtime Rules

Tailwind v4 is CSS-first:

```html
<style type="text/tailwindcss">
  @theme {
    --color-brand: oklch(0.68 0.2 252);
    --font-display: "Inter", sans-serif;
  }

  @utility headline-balance {
    text-wrap: balance;
    letter-spacing: 0;
  }
</style>
```

Avoid v3-only patterns in browser-runtime compositions:

```css
@tailwind base;
@tailwind components;
@tailwind utilities;
```

Do not add `tailwind.config.js` only for composition colors, fonts, spacing, or utilities. Use `@theme` and `@utility`.

**`@config` / `@plugin` abort the browser compile.** The pinned `@tailwindcss/browser` build does not support JS config or plugins. Theme and utilities stay in a `text/tailwindcss` block.

## Composition Pattern

Use Tailwind for static layout and style. Keep render-critical timing in GSAP or another seekable HyperFrames adapter.

```html
<section
  id="hero"
  class="clip absolute inset-0 grid place-items-center bg-zinc-950 text-white"
  data-start="0"
  data-duration="5"
  data-track-index="1"
>
  <div class="w-[1280px] max-w-[82vw] text-center">
    <h1 class="text-7xl font-black leading-none text-balance">Render-ready Tailwind</h1>
  </div>
</section>
```

For repeated items, **parameterize via CSS variables** — keep the class list static so the runtime sees every utility:

```html
<span class="translate-y-[calc(var(--i)*6px)] opacity-80" style="--i: 0"></span>
<span class="translate-y-[calc(var(--i)*6px)] opacity-80" style="--i: 1"></span>
<span class="translate-y-[calc(var(--i)*6px)] opacity-80" style="--i: 2"></span>
```

## Dynamic Class Safety

The browser runtime scans classes it can see. Do not build render-critical class names only at seek time:

```js
// Risky: the runtime may never see every generated class.
element.className = `bg-${color}-500`;
```

Prefer complete class tokens in HTML, data variants, or explicit CSS:

```html
<div data-tone="blue" class="bg-blue-500 data-[tone=rose]:bg-rose-500"></div>
```

If a generated class is unavoidable, make sure the full class token appears in a `text/tailwindcss` block before validation.

## Video-Specific Guardrails

v4 + render-mode footguns. Every bullet is a hard rule:

- **Stable dimensions only** — use `w-[…]` / `h-[…]` / `aspect-video` / grid / flex. **No `md:` / `lg:` breakpoints** (renderer is fixed-viewport).
- **Animate via transforms / opacity** — `translate-*`, `scale-*`, `opacity-*` are seek-safe; animating Tailwind sizing utilities is not.
- **No `transition-*` for render-critical motion** — a seekable runtime (GSAP) must own the state.
- **No interaction variants** — `hover:` / `focus:` / `active:` / `group-*:` / `peer-*:` / scroll / pointer variants never fire during render.
- **Bare `border` is broken in v4** — v4 default is `currentColor` (v3 was `gray-200`). Always write the color: `border border-white/20`.
- **v4 utility renames** — `shadow-sm` → `shadow-xs`, `rounded-sm` → `rounded-xs`, `outline-none` → `outline-hidden`, `flex-shrink-*` → `shrink-*`, `flex-grow-*` → `grow-*`.
- **Modern CSS is fine** — `color-mix()`, container queries, logical properties work; the renderer is current Chrome.

## Validation

```bash
npx hyperframes check

# Render proof — frame 0 must NOT flash unstyled content. Preview alone can hide this.
npx hyperframes render . --workers 1 --quality draft --output tailwind-proof.mp4
```


<!-- ===== FILE: hyperframes/hyperframes-core/references/tracks-and-clips.md ===== -->

# Tracks and Clips

Clips are timed elements inside a composition. Tracks are a Studio display concept: the render never reads them.

## What is a Clip

A clip is any DOM element with `data-start` and, where required, `data-duration`. `data-track-index` is optional. Common kinds:

- **Visual `<div>` clips** — scenes, cards, overlays. Always require `data-duration`.
- **Sub-composition hosts** — `<div>` with `data-composition-src`. Always require `data-duration`.
- **Video clips** — `<video playsinline>`. With sound: `data-has-audio="true"` (the sound stays on the clip). Silent: `muted`. Duration can default to media length.
- **Audio clips** — `<audio>`. Duration can default to media length.
- **Image clips** — `<img>`. `data-duration` is optional and defaults to 3 seconds; write it only for another length.

Add `class="clip"` to authored visual clips. The runtime does not read it, but the scaffold's shared `.clip { position: absolute; inset: 0 }` rule is what gives a scene its full-frame box, Studio treats it as an edit hint, and `lint` warns without it.

## Tracks Are a Display Lane

`data-track-index` is the row a clip occupies in Studio's timeline. It is **not** read by the render, and it constrains nothing:

- **Two clips on the same track may overlap in time.** Nothing rejects it and the render is well defined: both are visible, painted in CSS order.
- **Visual layering (front/back)** is controlled by CSS `z-index`, not by track index.
- **Omitting it is fine.** The parser defaults it, and Studio then lays out one lane per clip.

A clip on track `5` is not "above" a clip on track `1`. Use CSS for layering, `data-start`/`data-duration` for sequencing.

The one place the value carries meaning: two `<audio>` elements that share a track index **and** overlap in time raise a `lint` warning (`duplicate_audio_track`), which is a useful nudge that you are about to double up a bed.

## Picking a Track Index

Purely a readability choice for whoever opens the file in Studio. Common patterns, owned by `/hyperframes-studio` (one caption track, one element kind per track).

When adding a clip to an existing composition, set its `data-start`/`data-duration` against the clips around it. You do not need to hunt for a free lane, and you never need to renumber tracks after a retime.

## Clip Time Inside the Composition

`data-start` is in seconds, measured from the start of the _composition_. For sub-compositions, the sub-composition's internal timeline (its own `data-duration` and child clips) runs from `data-start` to `data-start + data-duration` of the host.

`data-media-start` (on `<video>`/`<audio>`) is an offset _into the source media_. Use it to skip the first few seconds of a media file without trimming the file itself.

## Cut one source into multiple ranges

For a hard cut, trim, splice, or reorder, duplicate the same video source into
multiple clip elements. Each copy selects its source range with
`data-media-start` plus `data-duration`, and places that range on the authored
timeline with `data-start`. Change the source offsets and placement order; do
not try to keyframe source cutting.

Each video segment keeps its sound: the sound stays on the clip (`data-has-audio="true"`), so cutting the video cuts its sound. A separate `<audio>` is for other sound (music, voiceover, replacement audio, J/L cuts).

## Linked clips

`data-link="<id>"` marks clips that are edited as one: in Studio, moving, trimming, splitting or deleting one member does the same to the others. Detach audio in Studio produces a pair, a muted `<video>` and an `<audio>` over the same file:

```html
<video
  id="talk"
  src="talk.mp4"
  muted
  data-link="lk-1"
  data-sync-origin="lk-1"
  data-start="2"
  data-duration="6"
  data-media-start="1"
  data-track-index="0"
></video>
<audio
  id="talk-audio"
  src="talk.mp4"
  data-link="lk-1"
  data-sync-origin="lk-1"
  data-start="2"
  data-duration="6"
  data-media-start="1"
  data-track-index="2"
></audio>
```

- **Link offer.** Studio offers Link for exactly one video and one audio, neither already linked; their timing and source file don't matter. A linked pair that is offset moves together (the offset is kept), and a trim carries to the partner only when its edge sits at the same time. Merge back needs the same file and an in-sync pair.
- **Keep members in sync.** Every member needs the same `data-start`, `data-duration`, `data-media-start` (absent = 0) and `data-playback-rate` (absent = 1). Track index, volume, fades and FX may differ. When you retime one member by hand, retime all of them, or `lint` warns `linked_clips_out_of_sync`.
- **Unlink** by removing `data-link` from every member. Removing it from one leaves the other alone with the id, which `lint` flags as `linked_clip_orphan`.
- The render ignores `data-link`: an out-of-sync pair still plays exactly what its timings say.
- Prefer a single `<video data-has-audio="true">` for footage with sound. Link only when the sound needs its own clip (its own track, volume or FX); to undo a detach, move the audio attributes back onto the video and delete the `<audio>`.
- **Sync origin.** `data-sync-origin="<id>"` marks a video and an audio from one source file; Detach writes it, Link writes it only for a pair from one source file, and Unlink keeps it. When the pair drifts (their source-zero points, `data-start − data-media-start / data-playback-rate`, differ), Studio shows a red offset in frames on both halves with Move into Sync / Slip into Sync, `hyperframes timeline` prints `out-of-sync=±Nf`, and the SDK offers `syncOffset`, `moveIntoSync` and `slipIntoSync`. Leave it alone when retiming by hand; remove it only when the clips are no longer one source.
- `@hyperframes/sdk` `setTiming` applies to link partners by default; pass `{ linked: false }` to edit one member, which unlinks it.

## Relative Timing

`data-start` accepts a clip ID instead of a number, meaning "start when that clip ends". Add `+ N` / `- N` to offset; negative produces overlap (useful for crossfades).

```html
<video id="intro" data-start="0" data-duration="10" data-track-index="0" src="..."></video>
<video id="main" data-start="intro" data-duration="20" data-track-index="0" src="..."></video>
<video
  id="scene-a"
  data-start="intro + 2"
  data-duration="20"
  data-track-index="0"
  src="..."
></video>
<video
  id="scene-b"
  data-start="intro - 0.5"
  data-duration="20"
  data-track-index="1"
  src="..."
></video>
```

Rules, and three ways this fails **silently**. Nothing in `lint` checks any of them, so read them before you use a reference:

- **Spaces around the operator are required.** `data-start="intro - 0.5"` means "0.5s before `intro` ends". `data-start="intro-0.5"` (no spaces) is parsed as a reference to an element whose id is literally `intro-0.5`; that element does not exist, so the clip silently starts at 0.
- **An unresolved reference resolves to 0**, it does not error. A typo'd id, or a target that is not in the document, puts the clip at the start of the composition.
- **If the target has no resolvable duration, the reference lands on the target's START, not its end.** So `data-start="hero"` where `hero` has no `data-duration` and no known media length silently means "same time as `hero`" rather than "after `hero`".
- **A cycle resolves to 0** rather than erroring. `A → B → A` puts one of them at 0.
- Lookup is **document-wide** (`getElementById`, then `[data-composition-id]`). A reference can therefore reach a target in another composition on the assembled page. Keep referenced ids unique and keep the reference and its target in the same file, or the result depends on assembly order.
- A value that parses as a number is always absolute seconds. Otherwise the resolver expects `<id>`, `<id> + <number>`, or `<id> - <number>`.
- References can chain (`A → B → C`). Keep chains under 3-4 levels for readability.
- Negative offsets create overlap, which is allowed. Overlapping clips do **not** need different tracks.

Because every failure mode above is a silent 0, snapshot a reference-timed composition and check the clip actually starts where you meant.


<!-- ===== FILE: hyperframes/hyperframes-core/references/variables-and-media.md ===== -->

# Variables and Media

Two separate concerns, grouped because both control "what flows in from outside the HTML": runtime parameters (variables) and external media files (video/audio).

## Variables

Declare variables on the `<html>` element with `data-composition-variables`. Each declaration needs `id`, `type`, `label`, and `default`:

```html
<html
  data-composition-variables='[
    {"id":"title","type":"string","label":"Title","default":"Hello"},
    {"id":"accent","type":"color","label":"Accent","default":"#66d9ef"}
  ]'
></html>
```

**Prefer declarative bindings — no script needed** for direct substitution:

```html
<img class="clip" data-start="0" data-duration="5" data-var-src="heroImage" src="fallback.jpg" />
<h1 class="clip" data-start="0" data-duration="5" data-var-text="title">Fallback</h1>
<style>
  .card {
    color: var(--accent);
  }
</style>
```

- `data-var-src="id"` substitutes the element's `src` (URL string or image `{url}`); the authored `src` is the fallback.
- `data-var-text="id"` substitutes the element's own text; element children (nested clips, animated spans) are preserved.
- Every scalar variable is applied automatically as a `--{id}` CSS custom property on the composition root, so `var(--id)` CSS responds to overrides — no `setProperty` boilerplate.
- Bindings resolve identically in preview and render, and per-instance for sub-compositions.
- Caveat: media with audio should keep a real fallback `src` — render audio extraction reads the authored attribute (lint: `media_variable_src_no_fallback`).

For logic beyond direct substitution (loops, conditionals, derived values), read values once during initialization:

```js
const { title, accent } = window.__hyperframes.getVariables();
document.getElementById("title").textContent = title;
```

### Variable Rules

- Supported types and their extra options (consumed by Studio's editing UI):
  - `string` — optional `placeholder`, `maxLength`
  - `number` — optional `min`, `max`, `step`, `unit`
  - `color` — none
  - `boolean` — none
  - `enum` — **required** `options: [{ "value": "...", "label": "..." }, ...]`
- Always provide useful `default` values so preview works without CLI overrides.
- Use `data-variable-values='{"title":"Pro"}'` on sub-composition hosts for per-instance overrides.
- Use `npx hyperframes render --variables '{"title":"Q4 Report"}'` or `--variables-file` for render-time overrides.
- Add `--strict-variables` in CI: turns undeclared keys, type mismatches, and enum values not in `options` into errors instead of warnings.
- Read values once during init, not on every animation tick — variables don't change mid-render.
- Media color grading can use exact variable references inside `data-color-grading` JSON. Use `$gradingPreset` or `${gradingIntensity}` as the whole field value; the runtime resolves it from the current composition's variables before applying shader adjustments, finishing details, blur/pixelate effects, and custom LUTs.

### Two JSON Shapes (Easy to Confuse)

- `data-composition-variables` is an **array of declarations** (the schema): `[{id, type, label, default}, ...]`
- `--variables` and `data-variable-values` are **objects keyed by id** (the values): `{"title":"Q4","accent":"#fff"}`

## Media

**`<video>`/`<audio>` work at any nesting depth, including inside a sub-composition `<template>` or a wrapper `<div>`.** The runtime discovers media with a flat `document.querySelectorAll("video, audio")`, resolves each element's host composition via `element.closest("[data-composition-id]")`, and rebases its local `data-start` by the accumulated absolute start of every ancestor composition. A host at `2` with child media at `2` therefore starts that media at root time `4`, consistently in preview, snapshot, extraction, and render. Legacy projects that deliberately authored a media start in root time must mark that element with `data-hf-media-start-basis="global"`; never infer the basis from overlapping numbers. New compositions should always use scene-local `data-start`. If a panel renders blank after a render, capture a per-frame `snapshot` and treat it as render-blocking.

The one real constraint is about **timelines, not media placement**: a sub-composition timeline **cannot reach or animate host elements** — neither `document.querySelector("#host-id")` nor a gsap selector string (`tl.to("#host-id", …)`) resolves across the boundary; a sub-comp timeline only drives its own subtree. So if a media element lives at the host root, **its per-scene motion (scale/opacity/morph/tilt/breathing) must be authored on the MAIN timeline in `index.html`, at GLOBAL time** (scene-local time + the scene slot's `data-start`). Keeping the media inside the scene sub-comp instead lets that sub-comp's own timeline animate it with scene-local time. For 3D tilt without a perspective parent, use gsap `transformPerspective` on the element. See `composition-patterns.md` archetype B.

A video with sound keeps it on the `<video>` (`data-has-audio="true"`, no `muted`). Use a separate `<audio>` for music, voiceover, replacement audio, J/L cuts, or audio detached in Studio. Silent footage and b-roll: `muted`.

```html
<video
  id="a-roll"
  class="clip"
  src="assets/demo.mp4"
  playsinline
  data-has-audio="true"
  data-start="0"
  data-duration="12"
  data-track-index="0"
  data-volume="1"
></video>

<!-- Separate <audio> only for other sound: music, voiceover, replacement audio. -->
<audio
  id="music"
  src="assets/bed.mp3"
  data-start="0"
  data-duration="12"
  data-track-index="2"
  data-volume="0.4"
></audio>
```

### Media Rules

- **Do not** call `video.play()`, `audio.play()`, pause, or seek in composition code. HyperFrames owns playback.
- **Do not** drive host-root media from a sub-comp timeline: a sub-comp timeline cannot reach elements outside its subtree, so it has no effect. Drive host-root media from the main timeline at global time (or keep the media inside the sub-comp whose timeline animates it).
- **Do not** animate timed media element dimensions; animate a non-timed wrapper instead.
- **Do not** nest video inside a timed wrapper. `lint` rejects a `<video data-start>` whose ancestor also carries `data-start` (`video_nested_in_timed_element`, error), and the failure is real: the frame extractor resolves the video's start from its own `data-start` without the wrapper's offset, while visibility uses the wrapper's window. The clip then shows the wrong source frames and disappears partway through its slot. Put the timing on the wrapper **or** on the media element, never both.
- **Sub-compositions are exempt and work.** A `<video>`/`<audio>` inside a sub-composition renders identically to one at the host root, because a composition host propagates its offset. Only plain timed wrappers (a `<section data-start>` around a `<video data-start>`) break.
- **Never** add `crossorigin` to `<video>`/`<audio>`. `lint` rejects it unconditionally (`media_crossorigin_breaks_preview`, error) because a media host without `Access-Control-Allow-Origin` then fails silently in preview while renders still work, hiding the bug. There is no suppression, so this holds even for the canvas/WebGL/WebAudio readback case.
- **Every `<audio>` needs an `id`.** The mixer selects `audio[id][src]`, so an id-less `<audio>` is never mixed and the render is **silent**. `lint` catches it as `media_missing_id`.
- A video's own sound stays on the `<video>` (`data-has-audio="true"`, no `muted`). Add a separate `<audio>` only for other sound (music, voiceover, replacement audio, J/L cuts) and mute the video it replaces.
- For volume fades and ducking, use the `data-automation` volume lane; the exact form is in `creator-editing-recipes.md`. `data-volume` is the static baseline. A timeline `volume` tween is ignored when a lane is present.

For media duration: `<video>` and `<audio>` can omit `data-duration` if the media's intrinsic length is known and you want the full clip. Otherwise provide `data-duration` explicitly.

Input codecs: render decodes video via FFmpeg (frames are pre-extracted and injected), so HEVC/H.265 assets (8/10-bit) render correctly everywhere; live preview auto-proxies any browser-hostile asset (transcodes and caches an H.264 copy on first use, opt out with `--no-proxy` or `media.autoProxy: false`), and `lint` emits an info-level `hevc_preview_codec` note naming affected assets.
