

<!-- ===== FILE: hyperframes/hyperframes-animation/GUIDE.md ===== -->

---
name: hyperframes-animation
description: "All animation knowledge for HyperFrames — atomic motion rules, multi-phase scene blueprints, scene transitions, broader motion-design techniques, AND the seven runtime adapters (GSAP default, plus Lottie, Three.js, Anime.js, CSS keyframes, Web Animations API, TypeGPU). Use for any motion or animation task: pick 2-4 rules and compose, or load a blueprint, or look up runtime-specific API (e.g. GSAP eases / Lottie player / Three.js mixer). Also covers auditing an existing composition's choreography (animation map) and 24 named text-animation effects. HyperFrames-native: single paused timeline, seek-safe, deterministic."
---

**Plugin installs:** Before setup or freshness commands, follow [plugin execution rules](../hyperframes/references/plugin-installation.md) when this skill is inside a HyperFrames plugin. Standalone installs keep the update instructions below.

# HyperFrames Animation

All motion knowledge in one skill: **rules** (atomic recipes), **blueprints** (multi-phase scene templates), **transitions** (scene-to-scene), **techniques** (broader motion-design patterns), and **adapters** (per-runtime APIs).

For the composition contract (data attributes, sub-compositions, determinism) see `hyperframes-core`.

## Default: compose atomic rules

Pick 2-4 rules from `rules-index.md`, glue them together with a single paused GSAP timeline, done. This is faster and produces less code than starting from a blueprint.

## Load a blueprint when

- The scene matches an existing pre-designed multi-phase template (brand-reveal, social-proof, etc.) and reusing its phase pipeline saves real authoring time
- You want runnable ground-truth code for a complex 4-5 phase choreography

Blueprints live in `blueprints-index.md`. Each entry points to `blueprints/<id>.md` (recipe). Do not read it speculatively; load it when you've already decided you need scene-level orchestration.

## Routing

| Want to…                                                                       | Read                                                |
| ------------------------------------------------------------------------------ | --------------------------------------------------- |
| Pick an atomic motion pattern by trigger / tag                                 | `rules-index.md`                                    |
| Read one rule's full HTML / CSS / GSAP recipe                                  | `rules/<name>.md`                                   |
| Pick a multi-phase scene template                                              | `blueprints-index.md`                               |
| Read one blueprint's full recipe                                               | `blueprints/<id>.md`                                |
| Author a scene transition (CSS-driven, between two clips)                      | `transitions/overview.md`, `transitions/catalog.md` |
| Look up a broader motion-design technique                                      | `techniques.md`                                     |
| Motion blur — shutter smear on an element, and when not to use it              | `references/motion-blur.md`                         |
| Analyze an existing composition's animation map                                | `scripts/animation-map.mjs`                         |
| GSAP API — timeline / tweens / position parameters                             | `adapters/gsap.md`                                  |
| GSAP — drop-in effect recipes                                                  | `rules/gsap-effects.md`                             |
| GSAP — transforms / perf                                                       | `adapters/gsap-transforms-and-perf.md`              |
| GSAP — eases / stagger                                                         | `adapters/gsap-easing-and-stagger.md`               |
| GSAP — timeline / labels                                                       | `adapters/gsap-timeline-and-labels.md`              |
| Lottie / dotLottie (After Effects exports, `window.__hfLottie`)                | `adapters/lottie.md`                                |
| Character animation (walk cycle, mascot, jointed puppet, gestures)             | `adapters/lottie.md` → Characters                   |
| Three.js / WebGL (3D scenes, `AnimationMixer`, `hf-seek`)                      | `adapters/three.md`                                 |
| Anime.js (`window.__hfAnime`)                                                  | `adapters/animejs.md`                               |
| CSS keyframes (`animation-delay` / `play-state` / `fill-mode`)                 | `adapters/css-animations.md`                        |
| Web Animations API (`element.animate()`, `currentTime` seek)                   | `adapters/waapi.md`                                 |
| TypeGPU / WebGPU (`navigator.gpu`, WGSL, compute pipelines)                    | `adapters/typegpu.md`                               |
| HTML-as-texture + WebGL/GLSL post-fx (capture live DOM via `drawElementImage`) | `adapters/html-in-canvas-patterns.md`               |
| Named text-animation effects (24 IDs via external `animate-text` skill)        | `adapters/animate-text.md`                          |

## Picking a runtime

- **GSAP** is the default for 95% of motion work — covers timeline orchestration, transforms, easing, stagger. All atomic rules in this skill are GSAP-based.
- **Lottie** when an asset has its own pre-baked timeline (typically After Effects exports), including characters that walk, gesture or react.
- **Three.js** for 3D scenes, camera motion, shader-driven visuals.
- **Anime.js** for lightweight tweening when GSAP is overkill.
- **CSS** for simple repeated motifs, decoration, shimmer — no JavaScript animation cost.
- **WAAPI** for native browser keyframes without a GSAP dependency.
- **TypeGPU / WebGPU** for GPU-rendered canvases (particles, liquid glass, custom shaders).

Multiple runtimes can coexist in one composition. Each registers its instances on the runtime-specific global so HyperFrames can seek all of them in one pass.

## Critical Constraints

**Prerequisite: `hyperframes-core` → One paused timeline + Non-negotiable rules** (single paused timeline, `data-duration` governs length, no `Math.random` / `Date.now` / `performance.now`, no `repeat: -1` without a finite root `data-duration`, no page-load `gsap.set` on later-scene clips, no `display` or raw `visibility` tweens, and register the timeline only after it is fully built, including when the build runs inside an async callback such as `document.fonts.ready`). GSAP `autoAlpha` and zero-duration visibility sets at explicit timeline boundaries remain allowed by core. Use those exceptions only on non-clip elements or wrappers inside a clip; the framework owns `.clip` lifecycle. Don't restate the full contract here.

Animation-craft additions on top of core's contract:

- **Pre-calculated layout constants** — never derive positions from `getBoundingClientRect()` at tween time. Tween-time DOM measurements desync because the renderer samples in parallel; compute coordinates once at composition setup and reuse.
- **Spatial motion uses GSAP transform aliases only** (`x`, `y`, `scale`, `rotation`). Core's allowlist also permits `opacity` / `color` / `backgroundColor` / `borderRadius` for non-spatial property tweens — but never `width` / `height` / `top` / `left` for layout changes.

## Scripts

```bash
node <SKILL_DIR>/scripts/animation-map.mjs <composition-dir> \
  --out <composition-dir>/.hyperframes/anim-map
```

Reads every GSAP timeline registered on `window.__timelines`, enumerates tweens, samples bboxes, computes flags, outputs `animation-map.json`. Use it to audit choreography (dead zones, stagger consistency, lifecycle warnings) after authoring.

`animation-map.mjs` resolves helper packages from the current project first, then can bootstrap the bundled HyperFrames package version. Set `HYPERFRAMES_SKILL_PKG_VERSION=<version>` only when running the skill outside the bundled CLI/skill install and you need to pin that bootstrap version explicitly.

## See Also

- `hyperframes-core` — composition structure, data attributes, sub-compositions, deterministic render contract
- `hyperframes-creative` — palettes, typography, narration, beat planning (non-animation creative direction)
- `hyperframes-cli` — `npx hyperframes lint / check / snapshot / preview / render`


<!-- ===== FILE: hyperframes/hyperframes-animation/adapters/animate-text.md ===== -->

# Text Effects — Reference

For deterministic text-animation specs (e.g., `typewriter` at exact `240ms / 46ms stagger / steps(1, end) easing`), this skill defers to the separate **`animate-text`** skill maintained by Pixel Point at [github.com/pixel-point/animate-text](https://github.com/pixel-point/animate-text). It provides a catalog of 24 named text effects with portable contracts and per-library implementation recipes (GSAP, Anime.js, WAAPI).

**We do NOT ship the catalog inside this repo.** Pixel Point's `animate-text` is the source of truth; vendoring its files here would violate the upstream's licensing (no explicit license declared upstream as of this writing). Loading the skill separately keeps the legal picture clean while giving you the same catalog.

## How to use it

When a beat needs a deterministic text animation, load the upstream skill alongside this one:

```bash
# In your project root, install the upstream skill into .agents/skills/
npx skills add pixel-point/animate-text
```

Or in a skill-aware agent runtime, the skill is invoked by name:

```
/animate-text
```

Once installed, the specs live at:

```
.agents/skills/animate-text/assets/effects/<id>.json   # per-library implementation recipe
.agents/skills/animate-text/assets/specs/<id>.json     # portable motion contract
```

Sub-agents reading those files get exact GSAP timings, easing strings, DOM split rules, and stagger algorithms — no creative invention needed.

## When you don't need the upstream skill

If a beat's text animation is simple enough to describe in prose ("headline fades up word-by-word, 80ms stagger"), implement it inline using the GSAP knowledge already in these skills (`hyperframes-creative` → `references/motion-principles.md` and `references/beat-direction.md`; `hyperframes-animation` → `techniques.md`, entry #4 "Per-Word Kinetic Typography"). The upstream catalog is most valuable when:

- You want a specific NAMED effect across multiple beats (so they feel like one design system, not one-offs)
- You're choosing between several similar effects (typewriter vs per-character-rise vs bottom-up-letters) and want to see all 24 in one place
- You need layout-aware effects (`kinetic-center-build`, `short-slide-right`, `short-slide-down`) where parameters alone aren't enough — those ship with custom layout algorithms

## Effect names — vocabulary (do NOT use this as the implementation source)

For convenience while writing storyboards: the upstream skill provides 24 effects. Their IDs are listed here so you can name them in `STORYBOARD.md` even before loading the upstream skill. **The implementation specs are in the upstream skill, not here.**

- **Per-character (7):** soft-blur-in, per-character-rise, typewriter, bottom-up-letters, top-down-letters, stagger-from-center, stagger-from-edges
- **Per-word (8):** per-word-crossfade, spring-scale-in, shared-axis-y, blur-out-up, kinetic-center-build, short-slide-right, short-slide-down, depth-parallax-words
- **Per-line (2):** mask-reveal-up, line-by-line-slide
- **Whole element (7):** micro-scale-fade, shimmer-sweep, fade-through, shared-axis-z, scale-down-fade, focus-blur-resolve, shared-axis-x

For descriptions, durations, easing curves, and the per-library recipes: load `/animate-text` and read its own catalog page.

For `mask-reveal-up` and other line-mask effects, leave room for the font's painted glyphs at rest. Tight line-height plus `overflow: hidden` can cut descenders and accents after the reveal finishes. Follow the [text mask guidance](../techniques.md#12-clip-path-reveal-masks): start with block padding of `0.2em` at the text's font size and a compensating negative margin, or release the clip on the timeline once the entrance settles. Inspect a settled snapshot using the actual font and text; `data-layout-allow-overflow` also waives checks in the resting state.

## In the storyboard

Every text element in every beat can name an effect by ID, e.g.:

```markdown
**Text Animations:**

- Main headline: `kinetic-center-build`
- Eyebrow label: `soft-blur-in`
- Body copy 3 lines: `mask-reveal-up`
```

Sub-agents implementing the beat will load `/animate-text` if it's not already loaded, then read the spec for each named effect from the upstream skill's files.

If the upstream skill isn't available (offline build, network restrictions, agent runtime that doesn't support skill loading), sub-agents fall back to implementing the effect from the description alone — using GSAP knowledge plus the effect ID as a description of intent (e.g., "typewriter" = per-character stepped reveal with no interpolation).


<!-- ===== FILE: hyperframes/hyperframes-animation/adapters/animejs.md ===== -->

---
name: hyperframes-animejs
description: Anime.js adapter patterns for HyperFrames. Use when writing Anime.js animations or timelines inside HyperFrames compositions, registering animations on window.__hfAnime, making Anime.js seek-driven and deterministic, or translating Anime.js examples into render-safe HyperFrames HTML.
---

# Anime.js for HyperFrames

HyperFrames can seek Anime.js instances through its `animejs` runtime adapter. The composition owns the animation objects; HyperFrames owns the clock.

**This page targets v4 (examples pinned to 4.5.0, MIT).** v4 is a hard break from v3 — there is no callable `anime()`, `easing:` is now `ease:`, and ease names lost their `ease` prefix. Writing v3 from memory produces a composition that throws or silently animates nothing.

The repo's own producer fixtures pin `animejs@4.0.2/lib/anime.iife.min.js`, which still resolves — but that build predates `splitText` / `scrambleText` / `createSeededRandom` / `createLayout` used below, and 4.1+ moved the bundles to `dist/bundles/`, so a version bump needs the path changed too.

## Contract

- Create animations or timelines synchronously during composition initialization.
- Set `autoplay: false` so Anime.js does not advance on its own clock.
- Register every returned animation or timeline on `window.__hfAnime` — **explicitly. There is no working auto-discovery on v4** (see Avoid).
- Use finite durations and loop counts.
- Avoid callbacks that mutate DOM based on wall-clock time, network state, or unseeded randomness.

The adapter seeks every registered instance with `instance.seek(timeMs)`, where `timeMs` is HyperFrames time **in milliseconds** (`ctx.time` seconds × 1000). It also calls `pause()` and `play()` on each instance; anything exposing those three methods works, whatever created it.

## Loading v4

```html
<!-- UMD: the global `anime` is a NAMESPACE OBJECT, not a function -->
<script src="https://cdn.jsdelivr.net/npm/animejs@4.5.0/dist/bundles/anime.umd.min.js"></script>
```

`anime.animate(...)`, `anime.createTimeline(...)`, `anime.utils.*`, `anime.svg.*`, `anime.stagger(...)`. **Calling `anime(...)` is a TypeError** — every v4 build (UMD and IIFE alike) assigns a namespace object to the global, so v3's `anime({ targets })` form cannot work no matter which v4 file you load.

## Basic Pattern

```html
<script>
  const anim = anime.animate(".mark", {
    x: 280, // v4 shorthand for translateX
    rotate: "1turn",
    opacity: [0, 1],
    duration: 1200,
    ease: "outExpo", // NOT easing: "easeOutExpo"
    autoplay: false,
  });

  window.__hfAnime = window.__hfAnime || [];
  window.__hfAnime.push(anim);
</script>
```

## Timeline Pattern

`createTimeline` replaces `anime.timeline`, and `add()` takes **targets as its first argument** — `add(targets, parameters, position)`:

```html
<script>
  const tl = anime.createTimeline({
    autoplay: false,
    defaults: { ease: "outCubic" }, // per-timeline defaults, not a bare `easing`
  });

  tl.add(".title", { y: [40, 0], opacity: [0, 1], duration: 650 });
  tl.add(".accent", { scaleX: [0, 1], duration: 450 }, 250); // 250 = time position

  window.__hfAnime = window.__hfAnime || [];
  window.__hfAnime.push(tl);
</script>
```

Position accepts a number, a label, `"+=250"` / `"-=100"`, `"<"` (previous **end**) and `"<<"` (previous **start**).

## Module Builds

The adapter does not care how the instance was created — only that it exposes `seek()`, `pause()`, and `play()`:

```html
<script type="module">
  import { animate } from "https://cdn.jsdelivr.net/npm/animejs@4.5.0/+esm";

  const anim = animate(".chip", { x: "18rem", duration: 900, autoplay: false });

  window.__hfAnime = window.__hfAnime || [];
  window.__hfAnime.push(anim);
</script>
```

## Determinism

v4 ships `createSeededRandom(seed)` — use it instead of `Math.random()` when a composition needs scatter/jitter, so the same frame renders the same on every pass:

```js
const rnd = anime.createSeededRandom(1337);
anime.animate(".dot", { y: () => -40 * rnd(), duration: 800, autoplay: false });
```

`anime.utils.random()` / `randomPick()` / `shuffle()` are **not** seeded — they break frame-to-frame reproducibility.

## Good Uses

- Small SVG and DOM flourishes where Anime.js syntax is compact.
- Free `splitText` / `scrambleText` (Motion puts these behind Motion+; GSAP SplitText is the other free option).
- `svg.createDrawable` / `svg.morphTo` / `svg.createMotionPath` line-draw and path work.
- Multiple independent micro-animations pushed into the same registry.

Use GSAP for complex scene sequencing unless the user specifically asks for Anime.js. GSAP is still the primary HyperFrames authoring path.

## Avoid

- Leaving `autoplay` at the Anime.js default.
- **Relying on the adapter's `anime.running` auto-discovery — it cannot work on v4.** `running` is not among v4.5.0's exports (verified against the published bundle), so `discover()` returns immediately and any instance you did not `push()` is never seeked. Explicit registration is mandatory, not a nicety.
- `autoplay: onScroll(...)` — there is no scroll in a headless seek render, so the animation would never advance. Drive it off composition time instead.
- `waapi.animate()` for anything the adapter must seek — the adapter seeks via `.seek()`, and whether WAAPI-backed instances honor it is **unverified**. Use the JS engine (`animate`) for rendered compositions; `waapi` is an off-main-thread optimization for live pages.
- `createDraggable`, and any pointer-driven `createAnimatable` loop — input does not exist at render time.
- Infinite loops. Compute a finite repeat count from the composition duration (v4 `loop` counts **repeats**: `loop: 1` plays twice).
- Building animations in timers, promises, event handlers, or after async asset loads.

## Validation

After editing a composition that uses Anime.js:

```bash
npx hyperframes lint
npx hyperframes check
```

## Credits And References

- HyperFrames adapter source: `packages/core/src/runtime/adapters/animejs.ts`.
- Anime.js v4 docs: https://animejs.com/documentation/
- v3 → v4 migration (not on animejs.com): https://github.com/juliangarnier/anime/wiki/Migrating-from-v3-to-v4


<!-- ===== FILE: hyperframes/hyperframes-animation/adapters/css-animations.md ===== -->

---
name: hyperframes-css-animations
description: CSS animation adapter patterns for HyperFrames. Use when authoring CSS keyframes, animation-delay based timing, animation-fill-mode, animation-play-state, or CSS-only motion that HyperFrames must seek deterministically during preview and rendering.
---

# CSS Animations for HyperFrames

HyperFrames can seek CSS keyframe animations through its `css` runtime adapter. Use this for simple repeated motifs, background motion, shimmer, glow, masks, and non-sequenced decoration.

For scene choreography, GSAP is usually clearer. CSS animations work best when the motion belongs to one element and has a fixed duration.

## Contract

- Put the animated element in the DOM before runtime initialization finishes.
- Give timed elements a `data-start` value so local animation time matches the clip.
- Use finite `animation-duration` and `animation-iteration-count` because the negative-delay fallback cannot represent unbounded duration in environments without WAAPI-backed CSS animations.
- Prefer `animation-fill-mode: both` so seeked states hold before and after active motion.
- Avoid wall-clock JavaScript, hover-triggered state, and class toggles that depend on user events.

The adapter discovers elements with computed `animation-name`, seeks their browser `Animation` handles when available, and falls back to pausing with negative `animation-delay`.

## Basic Pattern

```html
<div
  id="pulse-ring"
  class="clip pulse-ring"
  data-start="0"
  data-duration="4"
  data-track-index="2"
></div>

<style>
  .pulse-ring {
    width: 280px;
    height: 280px;
    border: 4px solid rgba(255, 255, 255, 0.7);
    border-radius: 50%;
    animation-name: pulse-ring;
    animation-duration: 1200ms;
    animation-timing-function: cubic-bezier(0.2, 0, 0, 1);
    animation-iteration-count: 3;
    animation-fill-mode: both;
  }

  @keyframes pulse-ring {
    from {
      opacity: 0;
      transform: scale(0.82);
    }
    35% {
      opacity: 1;
    }
    to {
      opacity: 0;
      transform: scale(1.18);
    }
  }
</style>
```

## Stagger Pattern

Use CSS custom properties to avoid duplicating keyframes:

```html
<div class="clip dots" data-start="1" data-duration="3" data-track-index="3">
  <span style="--i: 0"></span>
  <span style="--i: 1"></span>
  <span style="--i: 2"></span>
</div>

<style>
  .dots span {
    display: inline-block;
    width: 18px;
    height: 18px;
    margin-right: 10px;
    border-radius: 50%;
    background: currentColor;
    animation: dot-pop 900ms ease-out both;
    animation-delay: calc(var(--i) * 120ms);
  }

  @keyframes dot-pop {
    from {
      opacity: 0;
      transform: translateY(18px) scale(0.75);
    }
    to {
      opacity: 1;
      transform: translateY(0) scale(1);
    }
  }
</style>
```

## Good Uses

- Decorative loops with a known repeat count.
- Mask, glow, shimmer, grain, and subtle parallax layers.
- Simple one-element entrances where a full JS timeline would be excessive.

## Avoid

- Infinite CSS animations unless you have verified the browser exposes seekable WAAPI-backed CSS animation handles. Prefer a finite iteration count covering the visible duration. If you do use `infinite`, add `data-duration` to the root element — see Composition Duration below.
- Animating layout properties like `top`, `left`, `width`, or `height` when transforms work.
- Relying on hover, focus, scroll, or media queries to trigger render-critical motion.
- Changing animation classes after startup unless another deterministic timeline controls that change.

## Composition Duration

The render engine needs to know the composition's total length. GSAP timelines report this automatically; CSS-only compositions have no timeline object, so the runtime infers duration from the longest running animation's computed end time (`animation-delay` + `animation-duration` × finite `animation-iteration-count`, per element with `data-start` added as an offset). `data-duration` on the root element is optional whenever every CSS animation on the page is finite — you don't need to add it just because the composition is CSS-driven.

`animation-iteration-count: infinite` (or any unresolved/unbounded animation) has no finite end time, so it cannot be auto-inferred. If the composition's only animation is infinite, you **must** add `data-duration="<seconds>"` to the root `[data-composition-id]` element with your intended total length — `npx hyperframes lint` errors on this case (`root_composition_missing_duration_source`) precisely because there is nothing for the runtime to infer.

```html
<div
  data-composition-id="root"
  data-start="0"
  data-duration="6"
  data-width="1920"
  data-height="1080"
>
  <div class="clip spinner" data-start="0" style="animation: spin 1s linear infinite"></div>
</div>
```

## Validation

After editing CSS animation compositions:

```bash
npx hyperframes lint
npx hyperframes check
```

## Credits And References

- HyperFrames adapter source: `packages/core/src/runtime/adapters/css.ts`.
- Duration auto-inference: `packages/core/src/runtime/init.ts` (`resolveAdapterDurationFloorSeconds`), `getInferredDurationSeconds` in the adapter above.
- MDN CSS animation documentation: https://developer.mozilla.org/en-US/docs/Web/CSS/Reference/Properties/animation
- MDN `animation-fill-mode`: https://developer.mozilla.org/en-US/docs/Web/CSS/animation-fill-mode


<!-- ===== FILE: hyperframes/hyperframes-animation/adapters/gsap-easing-and-stagger.md ===== -->

# Easing, Stagger, and Function-Based Values

## Easing

Built-in eases: `power1`, `power2`, `power3`, `power4`, `back`, `bounce`, `circ`, `elastic`, `expo`, `sine`, `none`.

Each has `.in`, `.out`, `.inOut` variants.

| Ease                                       | Use for                                                                                         |
| ------------------------------------------ | ----------------------------------------------------------------------------------------------- |
| `power1.out`, `power2.out`                 | Gentle motion for secondary elements (a caption fade, a small shift). NOT the entrance default. |
| `power3.out` (house default), `power4.out` | The standard long-tail settle. Entrances, title cards, hero reveals.                            |
| `sine.inOut`                               | Long, slow, calm motion. Crossfades, ambient drift.                                             |
| `back.out(1.7)`                            | Overshoot then settle. RARE — explicitly-playful register only, never a default.                |
| `elastic.out(1, 0.3)`                      | Springy bounce. Same playful-only rule; prefer a baked spring (see Spring Eases below).         |
| `expo.inOut`                               | Snappy, dramatic. Quick transitions between hero scenes.                                        |
| `none` (linear)                            | Camera moves with timed counterpoint, mechanical motion.                                        |

Pick `.out` for entrances, `.in` for exits, `.inOut` for symmetric moves and continuous motion.

**Smooth beats bouncy** — the motion doctrine (`rules/spring-pop-entrance.md`, the workflows' `motion-language.md`): entrances default to `power3.out` or the baked critically-damped spring (see Spring Eases below); overshoot eases (`back` / `elastic` / `bounce`) are a rare, explicitly-playful register, never the house style.

## Easing Vocabulary (character & mood)

Easings are tone of voice: a video that only whispers is boring; one that varies between whisper, normal, and punch is engaging. A composition should draw on ~3 easing characters across its beats — but vary **within the smooth families by energy** (`sine` / `power1` calm → `power3` standard → `power4` / `expo` punch); don't reach for overshoot to add variety. Overshoot is a _register_ (explicitly playful), not a spice. One ease everywhere reads flat; bounce everywhere reads cheap — the second failure is worse.

The full palette by character (each family has `.in`, `.out`, `.inOut` variants):

| Family               | Character                                                                    | Typical use                                                                                                                                  |
| -------------------- | ---------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------- |
| `power1`–`power4`    | Gentle (1) to aggressive (4) acceleration curves                             | General purpose. **power3 is the house workhorse**; power2 for gentle secondary motion, power4 for dramatic snaps                            |
| `back(N)`            | Overshoot then settle. N controls how far past the target (1=subtle, 4=wild) | RARE — explicitly-playful register only, never a default. Keep N ≤ 2; prefer a baked spring at ζ 0.6–0.7 (physical settle, see Spring Eases) |
| `elastic(amp, freq)` | Spring bounce. amp=magnitude, freq=oscillation speed                         | RARE — same playful-only rule; the baked spring (below) is the physical version                                                              |
| `bounce`             | Ball-drop bouncing                                                           | RARE — physical-comedy register only (something literally dropping)                                                                          |
| `expo`               | Extreme acceleration curve (much steeper than power4)                        | Premium/luxury reveals, dramatic entrances                                                                                                   |
| `sine`               | Smooth, organic, no hard edges                                               | Ambient float, breathing, Ken Burns, anything that loops. `.inOut` for yoyo motion                                                           |
| `circ`               | Circular acceleration (starts very fast, ends very gentle or vice versa)     | Camera moves, scene transitions, orbital motion                                                                                              |
| `steps(N)`           | Discrete N-step jumps, no interpolation                                      | Typing effects, cursor blink, counter ticks, retro/digital aesthetics                                                                        |

**Mood mapping:** Match easing character to the beat's emotional content. Smooth/organic easings (`sine`, `power1`) feel contemplative and drifting. Aggressive deceleration (`power4.out`, `expo.out`) feels snappy and confident. Spring overshoot (`back.out`) feels bouncy and physical — but bouncy is a register, not an emphasis tool; reach for it only on explicitly-playful beats. The storyboard's mood description should guide which character fits — not a formula.

## Defaults

```javascript
const tl = gsap.timeline({
  paused: true,
  defaults: { duration: 0.6, ease: "power3.out" }, // the house settle — smooth beats bouncy
});
```

Or globally:

```javascript
gsap.defaults({ duration: 0.6, ease: "power3.out" });
```

Setting defaults at timeline scope is preferred — it documents the motion language of that composition in one place.

## Spring Eases (baked physics, seek-safe)

The "iOS feel" is a **damped spring's velocity curve**, not a bounce: a fast launch into a long asymptotic settle. Well-made system animations are critically damped or close to it — they barely overshoot, or don't at all. `power3.out` / `expo.out` approximate that curve; when you want the exact one — or a _physical_ overshoot for the rare playful register — bake the spring's closed-form solution into a function ease.

Why not a real-time spring library: an interactive spring is a stateful integrator (velocity accumulates frame to frame), which cannot be seeked deterministically — you'd have to simulate frames 0…N−1 to render frame N. The closed form below is a **pure function of progress** — no state, nothing to desync, seek-safe by construction. This is also why interaction-lib spring solvers are banned in compositions.

```javascript
// springEase — a damped spring's exact position curve as a GSAP ease.
// response         ≈ seconds one oscillation would take (0.3–0.6 for entrances)
// dampingFraction  1.0       = critically damped — smooth settle, NO overshoot (house default)
//                  0.80–0.85 ≈ the iOS system register — ~1–1.5% overshoot, felt not seen
//                  0.60–0.70 = explicitly playful — ~5–10% overshoot (rare; replaces back.out)
function springEase({ response = 0.5, dampingFraction = 1 } = {}) {
  const w = (2 * Math.PI) / response; // undamped natural frequency
  const z = dampingFraction;
  let pos; // x(t): 0 → 1, starting at rest (v0 = 0)
  if (z < 1) {
    const wd = w * Math.sqrt(1 - z * z);
    pos = (t) => 1 - Math.exp(-z * w * t) * (Math.cos(wd * t) + ((z * w) / wd) * Math.sin(wd * t));
  } else if (z > 1) {
    const wo = w * Math.sqrt(z * z - 1);
    pos = (t) =>
      1 - Math.exp(-z * w * t) * (Math.cosh(wo * t) + ((z * w) / wo) * Math.sinh(wo * t));
  } else {
    pos = (t) => 1 - Math.exp(-w * t) * (1 + w * t);
  }
  // Settle time: last moment the curve sits outside ±0.1% of target.
  // Fixed-step scan, runs once at setup — deterministic (no Math.random / Date.now).
  const EPS = 0.001;
  const rate = z <= 1 ? z * w : (z - Math.sqrt(z * z - 1)) * w; // slowest decay mode
  const SCAN = 12 / rate;
  const N = 4800;
  let T = SCAN;
  for (let i = N; i >= 0; i--) {
    const t = (i / N) * SCAN;
    if (Math.abs(1 - pos(t)) > EPS) {
      T = ((i + 1) / N) * SCAN;
      break;
    }
  }
  const xT = pos(T);
  return {
    duration: T, // use as the tween's duration — the settle time IS the physics
    ease: (p) => pos(p * T) + p * (1 - xT), // normalized so ease(1) === 1 exactly
  };
}
```

Usage — take **both** the ease and the duration from the helper (the settle time is part of the physics; overriding the duration just re-times the same curve, so tune speed via `response` instead):

```javascript
const settle = springEase({ response: 0.4 }); // critically damped → duration ≈ 0.59s
tl.fromTo(
  "#hero",
  { scale: 0, opacity: 0 },
  { scale: 1, opacity: 1, duration: settle.duration, ease: settle.ease },
  0.2,
);
```

| dampingFraction   | overshoot       | register                                                                                                                                           |
| ----------------- | --------------- | -------------------------------------------------------------------------------------------------------------------------------------------------- |
| **1.0 (default)** | none (monotone) | The house settle — the exact curve `power3.out` approximates. Product / enterprise / serious tone.                                                 |
| 0.80–0.85         | ~1–1.5%         | "Alive, not bouncy" — the iOS system default register. The overshoot is felt, not seen.                                                            |
| 0.60–0.70         | ~5–10%          | Explicitly-playful ONLY (same rule as `back.out`, which this replaces — a spring's second-order settle reads physical where `back` reads cartoon). |
| < 0.55            | > 12%           | Don't. Cartoon-wobble territory.                                                                                                                   |

| response  | duration (ζ=1) | feel                                                         |
| --------- | -------------- | ------------------------------------------------------------ |
| 0.25–0.35 | 0.37–0.51s     | tight snap — chips, small UI                                 |
| 0.35–0.50 | 0.51–0.74s     | standard entrance                                            |
| 0.50–0.70 | 0.74–1.03s     | weighted hero landing — check the `t ≤ 0.5s` visibility rule |

Craft notes:

- **ζ=1 vs `power3.out`**: the true spring front-loads harder (~67% vs ~58% travelled at quarter-time) and settles on a longer asymptotic tail; max shape difference ~11%. That long tail is the "premium" read — use it when the settle IS the shot (a wordmark landing, a final lockup).
- **At ζ<1, overshooting curves go on transforms only** — never on `opacity` (it would push past 1) or color. Split opacity onto its own `power2.out` tween at the same timeline position.
- **Doctrine unchanged**: ζ below ~0.8 is still the rare, explicitly-playful exception (`rules/spring-pop-entrance.md`). The default of this section is ζ=1 — real spring physics is not a license for bounce.

## Stagger

```javascript
gsap.fromTo(".item", { y: 24, opacity: 0 }, { y: 0, opacity: 1, duration: 0.5, stagger: 0.08 });
```

Object form:

```javascript
gsap.fromTo(
  ".item",
  { y: 24, opacity: 0 },
  {
    y: 0,
    opacity: 1,
    stagger: {
      each: 0.08, // delay between each
      from: "center", // "start" | "end" | "center" | "edges" | "random" | index
      amount: 0.6, // total stagger time (overrides each if both set)
      grid: "auto", // for 2D stagger
      axis: "x" | "y",
    },
  },
);
```

Prefer `stagger` over N separate tweens with manual delays — it stays correct when the target count or order changes. Use `fromTo()` rather than `from()` so the start state is explicit (see `gsap-timeline-and-labels.md` → sub-composition entrances).

## Function-Based Values

Any var can be a function `(index, target, targets) => value`:

```javascript
gsap.to(".item", {
  x: (i, target, targets) => i * 50,
  rotation: (i) => (i % 2 === 0 ? 5 : -5),
  stagger: 0.1,
});
```

Use this for per-element values that depend on index, attributes, or measured size. Cheaper and more idiomatic than building tweens in a loop.

## gsap.matchMedia (preview only)

`matchMedia` runs setup only when a media query matches and auto-reverts when it stops matching. It is useful for **preview** in the browser at different viewport sizes, and for `prefers-reduced-motion`. It is **not** a substitute for rendering at the composition's actual `data-width`/`data-height` — HyperFrames renders at a fixed viewport.

```javascript
let mm = gsap.matchMedia();
mm.add(
  {
    isDesktop: "(min-width: 800px)",
    reduceMotion: "(prefers-reduced-motion: reduce)",
  },
  (context) => {
    const { isDesktop, reduceMotion } = context.conditions;
    gsap.to(".box", {
      rotation: isDesktop ? 360 : 180,
      duration: reduceMotion ? 0 : 2,
    });
  },
);
```


<!-- ===== FILE: hyperframes/hyperframes-animation/adapters/gsap-timeline-and-labels.md ===== -->

# Timelines and Labels

HyperFrames is a seek-driven runtime. Build one paused timeline per composition, attach it to `window.__timelines["<composition-id>"]`, and let HyperFrames seek it. Never call `.play()` for render-critical motion.

## Creating a Timeline

```javascript
const tl = gsap.timeline({
  paused: true,
  defaults: { duration: 0.5, ease: "power3.out" },
});

tl.to(".a", { x: 100 }).to(".b", { y: 50 }).to(".c", { opacity: 0 });
```

Timeline options:

- **paused: true** — required in HyperFrames. The framework drives the playhead.
- **repeat**, **yoyo** — apply to the whole timeline. `repeat: -1` requires a finite root `data-duration` (export clips to it); otherwise use finite counts.
- **defaults** — vars merged into every child tween. Use this instead of repeating `ease` and `duration` on every line.

## Position Parameter

The third argument to `.to()`/`.from()`/`.fromTo()` controls placement on the timeline:

| Form           | Meaning                              |
| -------------- | ------------------------------------ |
| `0`, `1.5`     | Absolute time in seconds             |
| `"+=0.5"`      | 0.5s after the end of the timeline   |
| `"-=0.2"`      | 0.2s before the end of the timeline  |
| `"intro"`      | At the `intro` label                 |
| `"intro+=0.3"` | 0.3s after the `intro` label         |
| `"<"`          | Same start as the previous tween     |
| `">"`          | Right after the previous tween ends  |
| `"<0.2"`       | 0.2s after the previous tween starts |
| `">-0.1"`      | 0.1s before the previous tween ends  |

```javascript
tl.to(".a", { x: 100 }, 0);
tl.to(".b", { y: 50 }, "<"); // same start as .a
tl.to(".c", { opacity: 0 }, "<0.2"); // 0.2s after .b starts
```

Prefer the position parameter over `delay:` — it composes naturally and survives refactors that re-order tweens.

## Labels

```javascript
tl.addLabel("intro", 0);
tl.to(".a", { x: 100 }, "intro");

tl.addLabel("outro", "+=0.5");
tl.to(".a", { opacity: 0 }, "outro");
```

Labels make a long timeline readable and let multiple tweens converge on the same beat without re-typing absolute times.

## Nesting Timelines

```javascript
const master = gsap.timeline({ paused: true });

const child = gsap.timeline();
child.to(".a", { x: 100 }).to(".b", { y: 50 });

master.add(child, 0);
```

In HyperFrames, **do not** nest sub-composition timelines into the host. Sub-compositions loaded via `data-composition-src` are seeked independently by HyperFrames from their own `data-start`. Nesting is only for grouping pieces of the _same_ composition's timeline.

## Inside Sub-Compositions: prefer `fromTo` over `from`

For entrance tweens inside a sub-composition, prefer `gsap.fromTo()` over `gsap.from()`:

```javascript
// Sub-composition entrance — survives re-seek cleanly
tl.fromTo(".title", { y: 60, opacity: 0 }, { y: 0, opacity: 1, duration: 0.6 }, 0.2);
```

Why: HyperFrames re-seeks the sub-composition every time its host clip becomes visible. `gsap.from()` snapshots the starting state at **registration time** (page load); when the playhead jumps back past `data-start`, that snapshot can desync from the actual CSS state and the element renders in the wrong position. `gsap.fromTo()` declares both endpoints explicitly, so the seek-back always produces the same start state.

In top-level (standalone) compositions either form works — there's no re-seek-through-mount cycle.

## Playback Control (debug / preview only)

```javascript
tl.play();
tl.pause();
tl.reverse();
tl.restart();
tl.time(2);
tl.progress(0.5);
tl.kill();
```

These are useful when previewing in the browser. In rendered output HyperFrames calls `seek()` internally — your timeline must produce identical state for the same time value every time it is seeked.


<!-- ===== FILE: hyperframes/hyperframes-animation/adapters/gsap-transforms-and-perf.md ===== -->

# Transforms and Performance

## Transform Aliases

Prefer GSAP's transform aliases over raw `transform` strings:

| GSAP property               | Equivalent            |
| --------------------------- | --------------------- |
| `x`, `y`, `z`               | `translateX/Y/Z` (px) |
| `xPercent`, `yPercent`      | `translateX/Y` in `%` |
| `scale`, `scaleX`, `scaleY` | `scale`               |
| `rotation`                  | `rotate` (deg)        |
| `rotationX`, `rotationY`    | 3D rotate             |
| `skewX`, `skewY`            | `skew`                |
| `transformOrigin`           | `transform-origin`    |

Aliases let GSAP track and interpolate each axis independently, which prevents accidental overwrites between separate tweens on the same element.

## autoAlpha

Prefer `autoAlpha` over `opacity` for show/hide:

```javascript
gsap.to(".panel", { autoAlpha: 0, duration: 0.4 });
```

`autoAlpha: 0` sets both `opacity: 0` and `visibility: hidden`, which removes the element from hit-testing and accessibility tree at zero alpha — closer to "gone" than plain `opacity: 0`. The registered seekable timeline still interpolates only opacity; visibility changes at the hidden endpoint. Use `autoAlpha` only on non-clip elements or wrappers inside a clip; HyperFrames owns `.clip` visibility. Never duration-tween raw `visibility` or `display`.

## clearProps

Removes inline styles set by GSAP when the tween completes:

```javascript
gsap.to(".item", { x: 100, rotation: 45, clearProps: "all" });
gsap.to(".item", { x: 100, rotation: 45, clearProps: "rotation,x" });
```

Useful at the end of an animation segment to hand the element back to CSS.

## CSS Variables

```javascript
gsap.to(".chart", { "--hue": 180, duration: 1 });
```

Animate any custom property. Works for color, length, number — anything CSS will interpolate.

## Relative and Directional Values

- Relative: `"+=20"`, `"-=10"`, `"*=2"`.
- Directional rotation: `"360_cw"`, `"-170_short"`, `"90_ccw"` — controls which way the angle takes when going between two values.

## SVG Specifics

- `svgOrigin` sets transform origin in the SVG's global coordinate space (not the element's local box). **Do not** combine `svgOrigin` with `transformOrigin` on the same element — pick one.
- Animate SVG transform attributes via the same alias names (`x`, `y`, `rotation`) — GSAP handles the SVG-specific quirks.
- **Resolve SVG geometry before building center-based transforms.** `createElementNS` is supported, but a detached, hidden, or zero-size element may not expose usable geometry when GSAP resolves a percentage `transformOrigin`. Attach and size the SVG before constructing the timeline, use an explicit `svgOrigin` when you know the canvas coordinates, or draw animated geometry around local `(0,0)` inside a positioning `<g>` for a center pivot that does not depend on a measured bounding box.

## Performance Rules

### Animate transforms, not layout properties

Animate `x`, `y`, `scale`, `rotation`, `opacity`. Never animate `left`, `right`, `top`, `bottom`, `width`, `height`, `margin*`, the text-reflow props `letterSpacing` / `wordSpacing` / `fontSize` — and never `roundProps`.

This is a **render-correctness** rule in HyperFrames, not just a GPU-performance nicety. The renderer seeks frame-by-frame and screenshots each frame, and the browser compositor snaps layout properties to whole device pixels. On a fast tween the per-frame step is several pixels, so the snap is invisible; on a slow tween or a long ease-out tail the value moves less than a pixel per frame — it holds the same pixel for several frames, then jumps a whole one. The result is motion that looks smooth when fast but visibly stutters when slow. Transforms interpolate sub-pixel and stay smooth at any speed. `roundProps` forces the same integer snap onto a transform — don't use it.

"Layout property" is broader than position: anything that triggers **reflow** snaps the same way. `letterSpacing` / `fontSize` are the common trap — a slow "settle" that crawls one of them by a fraction of a pixel per frame dwells on a handful of discrete glyph layouts (visible micro-stutter). The faithful smooth fix depends on which property — **do not reach for `scale` reflexively**:

- **`fontSize`** → animate `scale`. Scaling text up/down is the same visual and stays sub-pixel smooth (no reflow).
- **`letterSpacing` / `wordSpacing`** → uniform `scale` is **not** the same effect (it resizes the glyphs; it does not change the gaps between them). To animate spacing smoothly, split the text into per-character (or per-word) elements and animate each one's `x` — the glyph spread is a transform, sub-pixel smooth and visually identical to a letter-spacing tween. GSAP's `SplitText` does the split. If the spacing change is a minor flourish, hold the final value statically instead.

Unlike positional props, reflow props snap during browser **layout** — upstream of the canvas raster — so they stutter even in html-in-canvas, and the exception below does **not** apply to them.

#### Fixing a flagged animation — preserve the intent

The lint rule tells you a property will stutter; it does **not** tell you the fix, and a fix that merely passes lint can silently change the look. Swapping a `letterSpacing` tighten for a uniform `scale` lints clean but animates a _different thing_ (it resizes the glyphs instead of closing the gaps). Two rules:

1. **Reproduce the same visual** — same start/end state, same trajectory, only sub-pixel-smooth. Use the faithful equivalent (per-glyph `x` for spacing, `scale` for `fontSize`, `x`/`y` for position), not whichever transform is the least code.
2. **Verify against the original, not against the linter.** Render the original and the fixed version and compare the motion at its key moments — the fix should differ only by the removed stutter, not by _where things end up_. Lint-clean-and-smooth is not the bar; faithful-and-smooth is.

If the faithful fix is non-trivial (a per-glyph split, a measured offset), build it or surface the tradeoff — never downgrade to a cheaper, different effect just to satisfy the linter.

**Convert a position animation to a transform** by leaving the element at its resting `left`/`top` in CSS and animating the _offset_ with `x`/`y`:

```javascript
// CSS: #card { left: 1340px; top: 540px }   ← resting position stays in CSS
tl.to("#card", { left: 1340, top: 540, duration: 1 }); // ✗ stutters
tl.fromTo("#card", { x: 640, y: 0 }, { x: 0, y: 0, duration: 1 }); // ✓ x/y = delta from CSS rest (640 = startLeft − 1340)
```

For a parent-relative `left: "100%"` sweep, use `xPercent: 100` only when the element is the full width of its container; otherwise convert to pixels (`x: containerWidth`).

**The one exception:** elements drawn through the html-in-canvas API — those under a `<canvas layoutsubtree>` ancestor, e.g. the `liquid-glass-*` blocks. The canvas rasterizes from sub-pixel `getComputedStyle`, so layout props don't snap there and those elements keep `left`/`top`. Everything the browser lays out (plain DOM) follows the rule.

The `gsap_non_transform_motion` lint rule is the backstop, not the teacher — reach for transforms from the start instead of animating layout props and waiting for lint to reject them.

### will-change (sparingly)

```css
.title {
  will-change: transform;
}
```

Only on elements that _actually_ animate. Applied everywhere it becomes useless and burns memory.

### gsap.quickTo for frequent updates (preview-only)

For high-frequency updates driven by **events** — pointer move, scroll, audio scrub — `quickTo` reuses the same tween instead of creating a new one each frame:

```javascript
const xTo = gsap.quickTo("#cursor", "x", { duration: 0.4, ease: "power3" });
const yTo = gsap.quickTo("#cursor", "y", { duration: 0.4, ease: "power3" });

container.addEventListener("mousemove", (e) => {
  xTo(e.pageX);
  yTo(e.pageY);
});
```

> **Render mode has no input events.** The renderer seeks frame-by-frame; `mousemove`, `scroll`, etc. never fire. `quickTo`'s main use case applies in **live preview** in the browser only. For audio-reactive motion in renders, pre-extract audio data and drive the timeline declaratively (see `../rules/gsap-effects.md`).

### Stagger beats N tweens

One tween with `stagger` beats N tweens with manual delays for both readability and runtime cost.

### Cleanup

In live preview, pause or `kill()` off-screen animations. Render mode is unaffected (the renderer drives time directly).


<!-- ===== FILE: hyperframes/hyperframes-animation/adapters/gsap.md ===== -->

---
name: hyperframes-gsap-adapter
description: GSAP animation API reference for HyperFrames. Use when writing seekable GSAP timelines in HyperFrames compositions, including gsap.to(), from(), fromTo(), set(), timeline position parameters, labels, easing, stagger, finite repeats, and transform performance.
---

# HyperFrames GSAP

GSAP usage scoped to HyperFrames' seek-driven render model. This skill is the GSAP reference _as constrained by HyperFrames_ — for the framework's broader composition contract see `hyperframes-core`.

## HyperFrames Contract

HyperFrames controls GSAP through its `gsap` runtime adapter. Create a paused timeline, register it on `window.__timelines` with the exact `data-composition-id` after adding its tweens, and let HyperFrames seek it. Setup may run inside an async callback; register the completed timeline at the end of that callback.

```html
<script src="https://cdn.jsdelivr.net/npm/gsap@3.14.2/dist/gsap.min.js"></script>
<script>
  window.__timelines = window.__timelines || {};
  const tl = gsap.timeline({ paused: true });

  tl.from(".title", { y: 48, opacity: 0, duration: 0.6, ease: "power3.out" }, 0);
  tl.to(".accent", { scaleX: 1, duration: 0.5, ease: "power2.out" }, 0.25);

  window.__timelines["main"] = tl; // key must equal data-composition-id on the composition root
</script>
```

- The registry key must match the composition root's `data-composition-id`.
- Bracket and dot syntax both register: `window.__timelines["main"] = tl` and `window.__timelines.main = tl` are equivalent (the linter recognizes both). Bracket form is required when the id isn't a valid identifier (e.g. contains `-`).
- Do not call `tl.play()` for render-critical motion.
- Building inside an async callback such as `document.fonts.ready` is supported and common. What breaks is **registering the key before the build finishes**: an empty timeline registered early is treated as ready and nested empty, so it renders blank (`lint`: `gsap_timeline_registered_before_async_build`, error). Assign `window.__timelines[id] = tl` at the end of the callback. Do not drive render-critical motion from timers or event handlers.
- Keep loops finite. HyperFrames renders finite video durations.
- **Render duration comes from `data-duration` on the composition root, not from GSAP timeline length.** Do not pad the timeline with empty tweens like `tl.set({}, {}, 283)` to "extend" it. (Some external docs show this trick; in HyperFrames it conflicts with the seek-driven duration model — set `data-duration` instead.)

## Core Tween Methods

- **gsap.to(targets, vars)** — animate from current state to `vars`. Most common.
- **gsap.from(targets, vars)** — animate from `vars` to current state (entrances).
- **gsap.fromTo(targets, fromVars, toVars)** — explicit start and end.
- **gsap.set(targets, vars)** — apply immediately (duration 0).

Always use **camelCase** property names (e.g. `backgroundColor`, `rotationX`).

## Common vars (cheatsheet)

- **duration** — seconds (default 0.5).
- **delay** — seconds before start.
- **ease** — `"power1.out"` (default), `"power3.inOut"`, `"back.out(1.7)"`, `"elastic.out(1, 0.3)"`, `"none"`. See `./gsap-easing-and-stagger.md`.
- **stagger** — number or object. See `./gsap-easing-and-stagger.md`.
- **repeat** — finite number; never `-1` in HyperFrames. Compute repeats from the visible duration.
- **yoyo** — alternates direction with repeat.
- **overwrite** — `false` (default), `true`, or `"auto"`.
- **immediateRender** — default `true` for from()/fromTo(). Set `false` on later tweens targeting the same property+element.
- **onComplete**, **onStart**, **onUpdate** — callbacks.

For transforms, autoAlpha, clearProps, and SVG specifics see `./gsap-transforms-and-perf.md`.

## Animated Property Allowlist

HyperFrames is stricter than vanilla GSAP. Animate only:

- **Compositor-cheap**: `opacity`, `x`, `y`, `scale`, `scaleX`, `scaleY`, `rotation`, `rotationX`, `rotationY`, `skewX`, `skewY`, `transformOrigin`
- **Visual fills**: `color`, `backgroundColor`, `borderColor`, `borderRadius`
- **CSS variables**: `"--hue": 180` etc.
- **Media `volume`** (on `<audio>` / `<video>`): do not tween it for fades or ducking; use the `data-automation` volume lane (`creator-editing-recipes.md` in `hyperframes-core`). A lane wins over a tween on the same element.
- **DOM text `innerText`** (for numeric counters): tween it directly, e.g. `tl.to(el, { innerText: 100, snap: { innerText: 1 } })` — `snap` keeps it integer; the GSAP inspector recognizes it as a counter. Equivalent to the `onUpdate`-proxy form in `../rules/counting-dynamic-scale.md`; prefer that proxy form for locale formatting (`toLocaleString`) or suffix logic, and pair it with a separate transform-scale tween when the number should grow.

**Avoid** (use the transform alias instead):

- `width` / `height` / `top` / `left` / `right` / `bottom` / `margin*` / `padding*` — trigger layout reflows. Use `scaleX/Y` (with `transformOrigin`) or `x` / `y`.

**Forbidden** (breaks the renderer or the clip lifecycle):

- `display`, raw `visibility` **on a clip element**: never duration-tween these. HyperFrames owns a clip's visibility and `lint` rejects it. Use `autoAlpha` (opacity plus endpoint visibility) or a zero-duration timeline set at an explicit boundary. Animating a clip element's other visual properties is fine and the shipped catalog does it throughout; what is forbidden is taking over its visibility.
- Anything driven by `Math.random()`, `Date.now()`, `performance.now()`, or event handlers — animation state must be deterministic from time alone.

> **Note**: the list above is a **denylist**, not an allowlist. Properties outside it, including `width`, `height`, `filter`, `clipPath` and `strokeDashoffset`, are legitimate targets; prefer transforms and opacity where you have the choice, for performance rather than correctness. See `hyperframes-core/references/determinism-rules.md` for the full deterministic-render contract.

## References

- `./gsap-timeline-and-labels.md` — timeline creation, position parameter (`+=`, `<`, `>`), labels, nesting, sub-comp `fromTo` preference, playback control.
- `./gsap-easing-and-stagger.md` — easing families, stagger objects, function-based values, `gsap.matchMedia()`, `gsap.defaults()`.
- `./gsap-transforms-and-perf.md` — transform aliases, autoAlpha, `quickTo`, `will-change`, performance rules.
- `../rules/gsap-effects.md` — drop-in recipes: typewriter (with cursor / backspace / word rotation) + audio visualizer (uses `skills/hyperframes-creative/scripts/extract-audio-data.py`).

## Best Practices

- Use camelCase property names; prefer transform aliases and autoAlpha.
- Prefer timelines over chained tweens with delays; use the position parameter.
- Add labels with `addLabel()` for readable sequencing.
- Pass defaults into the timeline constructor.
- Store the tween/timeline return value when controlling playback.

## Do Not

- Animate layout properties (`width`/`height`/`top`/`left`) when transforms suffice.
- Use both `svgOrigin` and `transformOrigin` on the same SVG element.
- Chain animations with `delay` when a timeline can sequence them.
- Create tweens before the DOM exists.
- Use infinite `repeat: -1` without a finite root `data-duration` (with one, export clips to that window); when a loop must end before the composition does, use a finite repeat count computed from the visible duration.

## Credits And References

- HyperFrames adapter source: `packages/core/src/runtime/adapters/gsap.ts`.
- GSAP documentation: https://gsap.com/docs/v3/
- GSAP timeline pause and seek behavior: https://gsap.com/docs/v3/GSAP/Timeline/pause%28%29/


<!-- ===== FILE: hyperframes/hyperframes-animation/adapters/html-in-canvas-patterns.md ===== -->

# HTML-in-Canvas Patterns

HyperFrames' most powerful visual capability. Capture ANY live HTML/CSS as a GPU texture, then render it through WebGL shaders, Three.js 3D scenes, or post-processing effects — at 60fps, pixel-perfect, with every CSS feature supported.

**Read this file when a beat deserves cinematic treatment beyond flat GSAP animations.** Use for 1-3 hero beats per video, not every beat. The rest can use standard GSAP — the contrast between flat beats and HTML-in-Canvas beats IS part of the visual storytelling.

---

## Core Boilerplate (same in every HTML-in-Canvas composition)

Every HTML-in-Canvas effect shares this structure. Learn this once, adapt it for any effect.

```html
<!-- 1. Source HTML — your content goes inside a layoutsubtree canvas -->
<canvas
  id="hic-source"
  layoutsubtree
  width="1920"
  height="1080"
  style="position:absolute;inset:0;opacity:0;"
>
  <div id="hic-content" style="width:1920px;height:1080px;">
    <!-- YOUR HTML CONTENT HERE — text, images, cards, dashboards, anything -->
  </div>
</canvas>

<!-- 2. Render target — the visible canvas that shows the effect -->
<canvas id="hic-output" width="1920" height="1080" style="position:absolute;inset:0;"></canvas>
```

```js
// 3. Feature detection — always check, always provide fallback
function isHiCSupported() {
  var tc = document.createElement("canvas");
  if (!("layoutSubtree" in tc)) return false;
  tc.setAttribute("layoutsubtree", "");
  var ctx = tc.getContext("2d");
  return ctx && typeof ctx.drawElementImage === "function";
}
var apiOk = isHiCSupported();

// 4. Capture function — call this every frame in onUpdate
var capCanvas = document.getElementById("hic-source");
var capCtx = capCanvas.getContext("2d");
function captureContent() {
  if (apiOk) {
    capCtx.drawElementImage(document.getElementById("hic-content"), 0, 0, 1920, 1080);
  }
}

// 5. Drive from GSAP timeline — capture + render every frame
tl.to(
  proxy,
  {
    /* your animation properties */
    duration: BEAT_DURATION,
    ease: "sine.inOut",
    onUpdate: function () {
      captureContent();
      // render your effect here (Three.js or WebGL2)
    },
  },
  0,
);
```

**Fallback:** When `drawElementImage` is not available (preview without Chrome flag), draw a solid-color placeholder or use Canvas 2D text. The HyperFrames renderer auto-enables the flag — the effect WILL work in the final video. See the liquid-glass block for a complete fallback example.

---

## Effect Catalog

### 1. 3D Rotation with Bloom (Three.js)

**What it looks like:** Content floats in 3D space, slowly rotating with cinematic glow around bright edges. Like a product screenshot displayed in a dark theater.

**When to use:** Hero product showcase, feature reveal, CTA with premium feel.

**Key Three.js components:** `PlaneGeometry` + `CanvasTexture` + `EffectComposer` + `UnrealBloomPass`

```js
// After the boilerplate above, add:
var scene3d = new THREE.Scene();
var camera = new THREE.PerspectiveCamera(45, 1920 / 1080, 0.1, 100);
camera.position.set(0, 0, 4);

var renderer = new THREE.WebGLRenderer({
  canvas: document.getElementById("hic-output"),
  antialias: true,
  alpha: true,
});
renderer.setSize(1920, 1080);

var texture = new THREE.CanvasTexture(capCanvas);
var mesh = new THREE.Mesh(
  new THREE.PlaneGeometry(3.6, 2.2),
  new THREE.MeshBasicMaterial({ map: texture }),
);
scene3d.add(mesh);

// Post-processing: bloom for cinematic glow.
// EffectComposer / RenderPass / UnrealBloomPass are ES-module named imports
// (see the import block below) — they're NOT properties of THREE in modern
// versions. Three.js r150+ removed the UMD `examples/js/` globals.
var composer = new EffectComposer(renderer);
composer.addPass(new RenderPass(scene3d, camera));
composer.addPass(new UnrealBloomPass(new THREE.Vector2(1920, 1080), 0.3, 0.4, 0.85));

var proxy = { rotY: -0.12, zoom: 4.2 };
tl.to(
  proxy,
  {
    rotY: 0.12,
    zoom: 3.6,
    duration: BEAT_DURATION,
    ease: "sine.inOut",
    onUpdate: function () {
      captureContent();
      texture.needsUpdate = true;
      mesh.rotation.y = proxy.rotY;
      camera.position.z = proxy.zoom;
      composer.render();
    },
  },
  0,
);
```

**Load Three.js and post-processing via ESM (use a `type="module"` script):**

```html
<script type="module">
  import * as THREE from "https://cdn.jsdelivr.net/npm/three@0.181.2/+esm";
  import { EffectComposer } from "https://cdn.jsdelivr.net/npm/three@0.181.2/examples/jsm/postprocessing/EffectComposer.js";
  import { RenderPass } from "https://cdn.jsdelivr.net/npm/three@0.181.2/examples/jsm/postprocessing/RenderPass.js";
  import { ShaderPass } from "https://cdn.jsdelivr.net/npm/three@0.181.2/examples/jsm/postprocessing/ShaderPass.js";
  import { UnrealBloomPass } from "https://cdn.jsdelivr.net/npm/three@0.181.2/examples/jsm/postprocessing/UnrealBloomPass.js";
  // ... rest of composition code using these imports
</script>
```

The `examples/js/` path was removed in Three.js r152. Use `examples/jsm/` (ES modules) with `three@0.181.2` — the version used by the HyperFrames Three.js adapter.

---

### 2. Magnetic Cursor Distortion (Raw WebGL2)

**What it looks like:** Content warps and bends toward a moving point, like a magnet pulling on pixels. Chromatic aberration splits RGB channels at the distortion site.

**When to use:** Interactive feel, product demo with cursor, "look at THIS feature" moment.

**Key technique:** Custom fragment shader with Gaussian warp + chromatic split. No Three.js needed — just raw WebGL2.

```js
// WebGL2 setup
var gl = document.getElementById("hic-output").getContext("webgl2", {
  alpha: false,
  preserveDrawingBuffer: true,
});

// Vertex shader — full-screen quad
var VS = `#version 300 es
in vec2 a_pos;
out vec2 v_uv;
void main() {
  v_uv = a_pos * 0.5 + 0.5;
  gl_Position = vec4(a_pos, 0.0, 1.0);
}`;

// Fragment shader — magnetic warp + chromatic aberration
var FS = `#version 300 es
precision highp float;
in vec2 v_uv;
out vec4 fragColor;
uniform sampler2D u_tex;
uniform vec2 u_cursor;   // cursor position (0-1)
uniform float u_strength; // warp strength (0-1)

void main() {
  vec2 uv = v_uv;
  vec2 delta = uv - u_cursor;
  float dist = length(delta);
  float warp = u_strength * exp(-dist * dist * 8.0);
  vec2 warped = uv - delta * warp * 0.3;

  // Chromatic aberration at distortion site
  float aberration = warp * 0.008;
  float r = texture(u_tex, warped + vec2(aberration, 0.0)).r;
  float g = texture(u_tex, warped).g;
  float b = texture(u_tex, warped - vec2(aberration, 0.0)).b;
  fragColor = vec4(r, g, b, 1.0);
}`;

// Compile, link, setup quad geometry, upload texture...
// (See registry/blocks/vfx-magnetic/vfx-magnetic.html for complete implementation)

// Drive cursor position from GSAP
var proxy = { cx: 0.2, cy: 0.5, strength: 0.0 };
tl.to(
  proxy,
  {
    cx: 0.8,
    cy: 0.4,
    strength: 1.0,
    duration: BEAT_DURATION,
    ease: "power2.inOut",
    onUpdate: function () {
      captureContent();
      // Upload texture, set uniforms, draw
      gl.uniform2f(cursorLoc, proxy.cx, proxy.cy);
      gl.uniform1f(strengthLoc, proxy.strength);
      gl.drawArrays(gl.TRIANGLE_STRIP, 0, 4);
    },
  },
  0,
);
```

---

### 3. Shatter / Fragment Explosion (Three.js)

**What it looks like:** Content breaks into geometric fragments that fly apart, revealing what's behind.

**When to use:** Dramatic transition, "breaking free" moment, tension release.

**Key technique:** Subdivide the source texture into triangle mesh fragments using BufferGeometry, then animate each fragment's position/rotation with GSAP.

Study `registry/blocks/vfx-shatter/vfx-shatter.html` for the complete 1156-line implementation. The core idea:

```js
// 1. Capture content to texture (same boilerplate)
// Seeded PRNG for determinism — Math.random() is banned
function mulberry32(seed) {
  return function () {
    seed |= 0;
    seed = (seed + 0x6d2b79f5) | 0;
    var t = Math.imul(seed ^ (seed >>> 15), 1 | seed);
    t ^= t + Math.imul(t ^ (t >>> 7), 61 | t);
    return ((t ^ (t >>> 14)) >>> 0) / 4294967296;
  };
}
var rng = mulberry32(42);

// 2. Create N triangle fragments from the texture
var fragments = [];
for (var i = 0; i < NUM_FRAGMENTS; i++) {
  var geom = new THREE.BufferGeometry();
  var mesh = new THREE.Mesh(geom, new THREE.MeshBasicMaterial({ map: texture }));
  scene3d.add(mesh);
  fragments.push({ mesh: mesh, targetPos: randomExplosionVector(rng), delay: rng() * 0.5 });
}

// 3. Animate: first hold still, then EXPLODE
tl.to({}, { duration: holdTime }, 0);
fragments.forEach(function (frag) {
  tl.to(
    frag.mesh.position,
    {
      x: frag.targetPos.x,
      y: frag.targetPos.y,
      z: frag.targetPos.z,
      duration: 0.8,
      ease: "power3.in",
    },
    holdTime + frag.delay,
  );
  tl.to(
    frag.mesh.rotation,
    { x: rng() * 4, y: rng() * 4, duration: 0.8, ease: "power2.in" },
    holdTime + frag.delay,
  );
});
```

---

### 4. Liquid / Fluid Surface (Three.js)

**What it looks like:** Content floats above a rippling liquid surface with real-time wave dynamics. Or content IS the surface, undulating like water.

**When to use:** Organic/premium feel, ambient background, "living" product showcase.

**Key technique:** Subdivided PlaneGeometry with vertex displacement driven by noise functions in a vertex shader.

Study `registry/blocks/vfx-liquid-background/vfx-liquid-background.html` for the 1244-line implementation. Core idea:

```js
// Custom vertex shader with wave displacement
var vertexShader = `
  varying vec2 vUv;
  uniform float u_time;
  void main() {
    vUv = uv;
    vec3 pos = position;
    // Sine wave displacement
    pos.z += sin(pos.x * 3.0 + u_time * 2.0) * 0.15;
    pos.z += cos(pos.y * 2.5 + u_time * 1.5) * 0.1;
    gl_Position = projectionMatrix * modelViewMatrix * vec4(pos, 1.0);
  }
`;

var mesh = new THREE.Mesh(
  new THREE.PlaneGeometry(4, 3, 64, 64), // heavily subdivided for smooth waves
  new THREE.ShaderMaterial({
    vertexShader: vertexShader,
    fragmentShader: `varying vec2 vUv; uniform sampler2D u_tex;
      void main() { gl_FragColor = texture2D(u_tex, vUv); }`,
    uniforms: {
      u_tex: { value: texture },
      u_time: { value: 0 },
    },
  }),
);
```

---

### 5. Portal / Dimensional Reveal (Three.js)

**What it looks like:** A glowing circular portal opens and content emerges through it from another dimension.

**When to use:** Product reveal, "entering the app" moment, hero feature introduction.

Study `registry/blocks/vfx-portal/vfx-portal.html` for the complete 863-line implementation.

---

## When to Use HTML-in-Canvas vs Standard GSAP

| Scenario                         | Use                                  | Why                                  |
| -------------------------------- | ------------------------------------ | ------------------------------------ |
| Hero product screenshot showcase | HTML-in-Canvas (3D rotation + bloom) | Makes flat UI feel cinematic         |
| Feature list / stats             | Standard GSAP                        | Content-focused, doesn't need 3D     |
| CTA / brand reveal               | HTML-in-Canvas (portal or magnetic)  | Makes the moment memorable           |
| Social proof / logos             | Standard GSAP                        | Orderly cascade, trust is steady     |
| Transition between acts          | HTML-in-Canvas (shatter)             | Dramatic act break                   |
| Background atmosphere            | HTML-in-Canvas (liquid surface)      | Premium ambient feel                 |
| Quick feature cards              | Standard GSAP                        | Speed matters, 3D would slow it down |

---

## More Effects You Can Build

These aren't in the VFX blocks — build them yourself from the core boilerplate + a custom fragment shader. Each effect is a single GLSL function applied to the captured texture.

### 6. Noise Dissolve

Content dissolves into noise particles, revealing what's behind. Great for transitions.

```glsl
// Fragment shader — noise-based dissolve
uniform float u_progress; // 0.0 = fully visible, 1.0 = fully dissolved
uniform sampler2D u_tex;

float hash(vec2 p) {
  return fract(sin(dot(p, vec2(127.1, 311.7))) * 43758.5453);
}

void main() {
  vec2 uv = v_uv;
  float noise = hash(uv * 50.0);
  float threshold = u_progress;
  if (noise < threshold) {
    // Edge glow at the dissolve boundary
    float edge = smoothstep(threshold - 0.05, threshold, noise);
    fragColor = vec4(1.0, 0.6, 0.2, 1.0) * (1.0 - edge); // orange edge glow
  } else {
    fragColor = texture(u_tex, uv);
  }
}
```

### 7. Holographic / Iridescent

Content gets a rainbow-shifting holographic sheen that moves with time. Premium, futuristic feel.

```glsl
uniform float u_time;
uniform sampler2D u_tex;

void main() {
  vec4 color = texture(u_tex, v_uv);
  // Iridescent color shift based on position + time
  float angle = v_uv.x * 6.28 + v_uv.y * 3.14 + u_time * 0.5;
  vec3 holo = vec3(
    sin(angle) * 0.5 + 0.5,
    sin(angle + 2.094) * 0.5 + 0.5,
    sin(angle + 4.189) * 0.5 + 0.5
  );
  // Blend holographic over content (subtle overlay)
  fragColor = vec4(mix(color.rgb, holo, 0.15 + 0.1 * sin(u_time)), color.a);
}
```

### 8. Scan Lines + CRT

Retro CRT monitor look — scan lines, slight curvature, phosphor glow. Great for "code" or "terminal" beats.

```glsl
uniform sampler2D u_tex;
uniform float u_time;

void main() {
  vec2 uv = v_uv;
  // Barrel distortion (CRT curvature)
  vec2 centered = uv - 0.5;
  float dist = dot(centered, centered);
  uv = uv + centered * dist * 0.15;

  vec4 color = texture(u_tex, uv);
  // Scan lines
  float scanline = sin(uv.y * 800.0) * 0.04;
  color.rgb -= scanline;
  // Slight RGB offset (phosphor)
  color.r = texture(u_tex, uv + vec2(0.001, 0.0)).r;
  color.b = texture(u_tex, uv - vec2(0.001, 0.0)).b;
  // Vignette
  float vignette = 1.0 - dist * 2.0;
  fragColor = vec4(color.rgb * vignette, 1.0);
}
```

### 9. Frosted Glass Blur

Content behind frosted glass — visible but softened, with subtle light refraction. Good for "behind the scenes" or "coming soon" moments.

```glsl
uniform sampler2D u_tex;
uniform float u_blur; // 0.0 = clear, 1.0 = full frost

void main() {
  vec2 uv = v_uv;
  vec4 color = vec4(0.0);
  // Box blur with offset
  float radius = u_blur * 0.015;
  for (float x = -2.0; x <= 2.0; x += 1.0) {
    for (float y = -2.0; y <= 2.0; y += 1.0) {
      color += texture(u_tex, uv + vec2(x, y) * radius);
    }
  }
  color /= 25.0;
  // Add frost noise texture
  float frost = fract(sin(dot(uv * 200.0, vec2(12.9898, 78.233))) * 43758.5453);
  color.rgb += frost * 0.03 * u_blur;
  fragColor = color;
}
```

### 10. Pixel Sort / Glitch Art

Pixels rearrange themselves in vertical or horizontal strips — digital art aesthetic. Great for tech/creative brands.

```glsl
uniform sampler2D u_tex;
uniform float u_intensity; // 0-1

void main() {
  vec2 uv = v_uv;
  // Random horizontal displacement per row
  float row = floor(uv.y * 80.0);
  float noise = fract(sin(row * 127.1) * 43758.5);
  float displace = step(0.7, noise) * u_intensity * 0.1;
  // Shift UV with RGB split
  float r = texture(u_tex, uv + vec2(displace, 0.0)).r;
  float g = texture(u_tex, uv).g;
  float b = texture(u_tex, uv - vec2(displace * 0.5, 0.0)).b;
  fragColor = vec4(r, g, b, 1.0);
}
```

---

## Creating ANY Custom Effect

The fragment shaders above are templates. The pattern is always:

1. **Capture your HTML content** with `drawElementImage` (the boilerplate at the top)
2. **Upload the captured canvas as a WebGL texture**
3. **Write a fragment shader** that reads from the texture and outputs modified colors
4. **Drive shader uniforms from GSAP** via `onUpdate`

Any GLSL effect from ShaderToy, The Book of Shaders, CodePen, or anywhere else can be adapted:

1. Find an effect you like (search "GLSL [effect name]" or browse shadertoy.com)
2. Copy the fragment shader
3. Replace `iResolution` with `vec2(1920.0, 1080.0)`, `iTime` with your `u_time` uniform
4. Add `uniform sampler2D u_tex;` for the captured content texture
5. Wire the uniforms to GSAP proxy values

**Geometry ideas beyond flat planes:**

- `SphereGeometry` — content mapped onto a globe (world map, global reach)
- `CylinderGeometry` — content on a rotating cylinder (carousel/scroll feel)
- `TorusGeometry` — content wrapped around a ring (infinity, cycle)
- `BoxGeometry` — content on a 3D box (product packaging, dice)
- GLTF models — content mapped as screen texture on phone, laptop, monitor (see `vfx-iphone-device`)

**Post-processing stacking** (Three.js EffectComposer):

- Bloom + film grain = cinematic
- Bloom + chromatic aberration = lens effect
- Depth of field + vignette = focused attention
- Film grain + scan lines = retro
- Multiple passes stack — add as many as you want

**You are not limited to the effects listed here.** If you can imagine a visual treatment, you can build it. The HTML-in-Canvas API gives you the source material (any HTML rendered as a texture), and WebGL/Three.js gives you unlimited creative control over how that material is presented.


<!-- ===== FILE: hyperframes/hyperframes-animation/adapters/lottie.md ===== -->

---
name: hyperframes-lottie
description: Lottie and dotLottie adapter patterns for HyperFrames. Use when embedding lottie-web JSON animations, .lottie files, @lottiefiles/dotlottie-web players, registering instances on window.__hfLottie, or making After Effects exports deterministic in HyperFrames.
---

# Lottie for HyperFrames

HyperFrames can seek both `lottie-web` and dotLottie players through its `lottie` runtime adapter. Lottie is a strong fit because the animation timeline is already encoded in the asset; HyperFrames only needs a player object it can seek.

## Contract

- Load assets from local project files, usually under `assets/`.
- Set `autoplay: false`.
- Use `loop: false` for a one-shot and `loop: true` for a cycle (walk, idle, spinner). A looping animation is seeked to composition time modulo its own length, so it keeps cycling for the whole scene; a one-shot holds its last frame. Always set `loop`: lottie-web treats a missing `loop` as `true`. A numeric `loop` count does not repeat under seeking; bake the repeats into the file.
- Register every returned animation or player on `window.__hfLottie`.
- Keep the Lottie container dimensions stable with CSS.

The adapter seeks `lottie-web` with `goToAndStop(timeMs, false)` and dotLottie with frame or percentage APIs depending on player shape.

## lottie-web Pattern

```html
<div id="logo-lottie" class="lottie-layer"></div>
<script src="https://cdnjs.cloudflare.com/ajax/libs/bodymovin/5.12.2/lottie.min.js"></script>
<script>
  const anim = lottie.loadAnimation({
    container: document.getElementById("logo-lottie"),
    renderer: "svg",
    loop: false,
    autoplay: false,
    path: "assets/logo-reveal.json",
  });

  window.__hfLottie = window.__hfLottie || [];
  window.__hfLottie.push(anim);
</script>
```

```css
.lottie-layer {
  width: 100%;
  height: 100%;
}
```

## dotLottie Pattern

```html
<canvas id="product-lottie" class="lottie-canvas"></canvas>
<script src="https://unpkg.com/@lottiefiles/dotlottie-web"></script>
<script>
  const player = new DotLottie({
    canvas: document.getElementById("product-lottie"),
    src: "assets/product-flow.lottie",
    autoplay: false,
    loop: false,
  });

  window.__hfLottie = window.__hfLottie || [];
  window.__hfLottie.push(player);
</script>
```

```css
.lottie-canvas {
  width: 100%;
  height: 100%;
  display: block;
}
```

## Multiple Animations

Push each player into the same registry:

```js
window.__hfLottie = window.__hfLottie || [];
window.__hfLottie.push(backgroundAnim);
window.__hfLottie.push(iconAnim);
window.__hfLottie.push(confettiAnim);
```

HyperFrames seeks them all to the same composition time.

## Composition Duration

The render engine needs the composition's total length. GSAP timelines report duration automatically; a Lottie-only composition has no timeline object, so the runtime reads the registered animation's native length directly — `totalFrames / frameRate` for `lottie-web`, or the player's own `duration` for dotLottie. `data-duration` on the root element is optional for Lottie compositions: as long as every animation is registered on `window.__hfLottie` (per the contract above), the runtime has a finite duration to work with. With `loop: true` that length is one cycle, so a looping Lottie in a longer scene needs `data-duration` or a GSAP timeline to set the scene length.

## Characters

For a character that walks, gestures or reacts (a mascot, a walk cycle, a jointed puppet), put the acting in one Lottie and the stage in GSAP:

- **The Lottie owns the body.** Walk, stop, point and idle live in the file's own timeline, so limbs stay jointed and feet stay planted exactly as the animator made them.
- **GSAP owns everything around it.** Cards, captions and camera moves go on the paused timeline, timed to the Lottie's beats. Read the beat times from the file's `markers` array (`tm` is in frames, divide by `fr`) or from the animator's notes.
- **Every registered animation plays against composition time.** There is no per-animation start offset, so a gesture that should begin at 4 s must begin at 4 s inside its file. Author the whole performance as one Lottie, or offset the action inside the file, rather than stacking separate action files.
- **A short cycle is fine.** A 1 s walk cycle with `loop: true` cycles for the whole scene. Move the character across the stage with GSAP `x` only if the cycle walks in place, and match the travel speed to the stride or the feet slide.
- **License the character.** Use a file the user or their designer made, or one whose license allows redistribution, and say where it came from. Never ship a character ripped from a site.

The `lottie-character-walk` registry block is a working example: a jointed flat character walks in on planted feet, stops, and points at a card that GSAP brings in on the point (`npx hyperframes add lottie-character-walk`).

## Good Uses

- After Effects exports that are already known to render correctly in lottie-web.
- Logo reveals, icon loops, decorative accents, and product UI motion.
- Characters: walk cycles, mascots, gestures (see Characters above).
- Translating Remotion Lottie usage into plain HyperFrames HTML.

## Avoid

- Relying on remote `path` URLs at render time.
- Starting playback with `play()`.
- Assuming unsupported After Effects effects will survive export. Test the JSON or `.lottie` file in a browser first.
- Loading a player asynchronously and registering it after HyperFrames validation has already inspected the page.

## Validation

After editing a Lottie composition:

```bash
npx hyperframes lint
npx hyperframes check
```

## Credits And References

- HyperFrames adapter source: `packages/core/src/runtime/adapters/lottie.ts`.
- Duration auto-inference: `packages/core/src/runtime/init.ts` (`resolveAdapterDurationFloorSeconds`), `getInferredDurationSeconds` in the adapter above.
- lottie-web by Airbnb: https://github.com/airbnb/lottie-web
- lottie-web `loadAnimation` options: https://github.com/airbnb/lottie-web/wiki/loadAnimation-options
- dotLottie web player methods by LottieFiles: https://developers.lottiefiles.com/docs/dotlottie-player/dotlottie-web/methods


<!-- ===== FILE: hyperframes/hyperframes-animation/adapters/three.md ===== -->

---
name: hyperframes-three
description: Three.js and WebGL adapter patterns for HyperFrames. Use when creating deterministic Three.js scenes, WebGL canvas layers, AnimationMixer timelines, camera motion, shader-driven visuals, or canvas renders that respond to HyperFrames hf-seek events.
---

# Three.js for HyperFrames

HyperFrames supports Three.js through its `three` runtime adapter. The adapter does not own your scene. It publishes HyperFrames time and dispatches a seek event so your composition can render the exact frame.

## Contract

- Create the scene, camera, renderer, materials, and assets synchronously when possible.
- Render from HyperFrames time, not wall-clock time.
- Listen for the `hf-seek` event and render exactly that time.
- Load models, textures, and HDRIs before render-critical seeking. Do not fetch them at seek time.
- Avoid `requestAnimationFrame` or `renderer.setAnimationLoop` as the source of truth for render-critical motion.
- **Always set `data-duration="<seconds>"` on the root `[data-composition-id]` element.** Unlike CSS/WAAPI/Lottie, the `three` adapter has no duration auto-inference — it only forwards time via `hf-seek`/`__hfThreeTime`, it doesn't inspect your scene for an `AnimationClip`/`AnimationMixer` length. Without `data-duration` (and no GSAP timeline), the render engine has no way to know how long to capture and fails with "Composition has zero duration". `npx hyperframes lint` errors on this (`root_composition_missing_duration_source`).

The adapter sets `window.__hfThreeTime` and dispatches `new CustomEvent("hf-seek", { detail: { time } })` on each seek.

## Basic Pattern

```html
<canvas id="three-layer"></canvas>
<script type="module">
  import * as THREE from "https://cdn.jsdelivr.net/npm/three@0.181.2/+esm";

  const canvas = document.getElementById("three-layer");
  const renderer = new THREE.WebGLRenderer({ canvas, alpha: true, antialias: true });
  // Match these to your composition's frame size.
  renderer.setSize(1920, 1080, false);
  renderer.setPixelRatio(1);

  const scene = new THREE.Scene();
  const camera = new THREE.PerspectiveCamera(35, 1920 / 1080, 0.1, 100);
  camera.position.set(0, 0, 6);

  const mesh = new THREE.Mesh(
    new THREE.IcosahedronGeometry(1.4, 4),
    new THREE.MeshStandardMaterial({ color: 0x64d2ff, roughness: 0.38 }),
  );
  scene.add(mesh);
  scene.add(new THREE.HemisphereLight(0xffffff, 0x223344, 2));

  function renderAt(time) {
    mesh.rotation.y = time * 0.7;
    mesh.rotation.x = Math.sin(time * 0.6) * 0.16;
    renderer.render(scene, camera);
  }

  window.addEventListener("hf-seek", (event) => {
    renderAt(event.detail.time);
  });

  renderAt(window.__hfThreeTime || 0);
</script>
```

```css
#three-layer {
  width: 100%;
  height: 100%;
  display: block;
}
```

## Loading Addons (`GLTFLoader`, `OrbitControls`, etc.)

For anything under `three/addons/`, use an importmap so bare specifiers resolve. The HyperFrames lint recognizes both this form and the inline `+esm` import above — pick whichever your composition needs.

```html
<script type="importmap">
  {
    "imports": {
      "three": "https://cdn.jsdelivr.net/npm/three@0.181.2/build/three.module.js",
      "three/addons/": "https://cdn.jsdelivr.net/npm/three@0.181.2/examples/jsm/"
    }
  }
</script>
<script type="module">
  import * as THREE from "three";
  import { GLTFLoader } from "three/addons/loaders/GLTFLoader.js";
  import { OrbitControls } from "three/addons/controls/OrbitControls.js";
  // ...
</script>
```

Pin the `three` version in both entries to the same value. Mixing versions across the map and bare imports causes silent breakage.

## Heavy Setup (Large Meshes, Shader Compiles)

The runtime already waits for textures/models queued through Three's `DefaultLoadingManager` before publishing render-ready. It has no visibility into CPU-bound work you do yourself after assets load — building a large procedural mesh, compiling shaders, warming a pipeline. That work can leave the canvas blank for seconds after the runtime and player already say "ready".

If your setup does this kind of work, register a promise on `window.__hf.buildReady` (declared-compute hold: runtime waits, player shows its loading state instead of a blank frame):

```js
window.__hf = window.__hf || {};
window.__hf.buildReady = window.__hf.buildReady || {};
window.__hf.buildReady["<your-piece-name>"] = buildScene(); // resolves once the scene is actually drawable
```

Register it synchronously, in the same script block that starts the build — same timing as `DefaultLoadingManager`, so the runtime's first readiness check already sees it. Only do this for setup an adapter cannot see; render-critical seeking still comes from `hf-seek`, not this hold. The key must be unique within the composition — a second registration under the same key silently replaces the first, dropping its hold.

## AnimationMixer Pattern

For GLTF or authored clip animation, seek the mixer directly:

```js
function renderAt(time) {
  mixer.setTime(time);
  renderer.render(scene, camera);
}
```

If several mixers exist, seek all of them from the same `time`.

## Camera Cuts Inside One Canvas

When one scene switches camera shots by time, declare each cut once and read that constant everywhere: in the camera's shot selector and in every object's visibility window. A window written as its own literal near the cut (`t > 22.9` against a cut at `t < 23`) shows the next shot's objects in the last frames of the previous shot. At 30 fps that is a two-frame pop-in, which one still per shot will not show.

```js
const CUT_B = 23;
const CUT_C = 35;

function shotFor(t) {
  if (t < CUT_B) return shotA(t);
  if (t < CUT_C) return shotB(t);
  return shotC(t);
}

function renderAt(t) {
  const shot = shotFor(t);
  camera.position.copy(shot.position);
  camera.lookAt(shot.target);
  shotBProps.forEach((mesh) => {
    mesh.visible = t >= CUT_B && t < CUT_C;
  });
  renderer.render(scene, camera);
}
```

Verify each cut on the last frame before it and the first frame after it, not only somewhere inside each shot. The last frame before a cut is `(Math.ceil(cut * fps) - 1) / fps`: for a cut at 23 s in a 30 fps render, `npx hyperframes snapshot --at 22.9667,23 --no-end`.

## Lighting Lit Meshes

A `MeshStandardMaterial` lit by one `PointLight` or `DirectionalLight`, with no ambient light, environment map or emissive color, gets no light on its unlit side. When the camera faces that light, the mesh shows only that side and renders as a flat black cutout. Add a fill that stands in for the environment's bounce light, such as a `HemisphereLight` in the colors of the surrounding glow. If the key light's brightness changes over time, drive both lights from the same source at a fixed ratio, tuned by eye. Their intensity units differ, so do not copy the key light's number onto the fill.

## Shader Numeric Domains

Clamp a cosine before subtracting it from one and passing it to GLSL `pow`:

```glsl
float rim = pow(1.0 - clamp(dot(normal, view), 0.0, 1.0), 1.6);
```

`max(dot(normal, view), 0.0)` only protects the lower end. Interpolation and GPU rounding can put the dot product above one even when vectors were normalized at vertices. A negative `pow` base is undefined in GLSL, including with integer exponents. Invalid color values from an opaque glow shader can enter glass transmission textures and spread through mipmaps or bloom; inspect the source shaders before disabling glass or replacing bad pixels with black.

`hyperframes lint` warns with `shader_unbounded_cosine_pow` for this direct cosine-power pattern in static shader strings and GLSL script blocks. Project lint also reads directly linked local authored `.js`, `.mjs`, and `.cjs` files, excluding minified/vendor scripts. Dynamic shader assembly and imported modules are outside this narrow check. A clean lint or software-renderer frame does not certify GPU arithmetic: inspect the reported times and before/after frames on the affected hardware in both preview and export.

## Good Uses

- Deterministic 3D objects, product spins, particles with seeded data, and shader plates.
- Camera moves derived from `time`.
- GLTF animation clips when assets are local and loaded before validation completes.

## Avoid

- Using `Date.now()`, `performance.now()`, or clock deltas to update scene state.
- Leaving render-critical work inside a free-running animation loop.
- Loading remote models or textures at render time.
- Device-pixel-ratio dependent output. Pin renderer size and pixel ratio for video renders.
- Post-processing passes that depend on previous frame history unless you can reconstruct state from time.

## Validation

After editing a Three.js composition:

```bash
npx hyperframes lint
npx hyperframes check
```

## Credits And References

- HyperFrames adapter source: `packages/core/src/runtime/adapters/three.ts`.
- Why `data-duration` is required here specifically (no auto-inference for this adapter): `packages/core/src/runtime/init.ts` (`resolveAdapterDurationFloorSeconds`) and the CSS/WAAPI/Lottie adapters' `getInferredDurationSeconds`, which the `three` adapter deliberately does not implement.
- Three.js `WebGLRenderer` docs: https://threejs.org/docs/pages/WebGLRenderer.html
- Three.js `AnimationMixer.setTime()` docs: https://threejs.org/docs/pages/AnimationMixer.html
- GLSL `pow` domain: https://docs.vulkan.org/glsl/latest/chapters/builtinfunctions.html


<!-- ===== FILE: hyperframes/hyperframes-animation/adapters/typegpu.md ===== -->

---
name: hyperframes-typegpu
description: TypeGPU and raw WebGPU adapter patterns for HyperFrames. Use when creating GPU-rendered compositions with TypeGPU, raw WebGPU, WGSL fragment shaders, compute pipelines, liquid glass effects, particle systems, or any canvas layer driven by navigator.gpu that responds to HyperFrames hf-seek events.
---

# TypeGPU / WebGPU for HyperFrames

HyperFrames supports TypeGPU and raw WebGPU through its `typegpu` runtime adapter. The adapter does not own your pipeline. It publishes HyperFrames time and dispatches a seek event so your composition can render the exact GPU frame.

## Render-environment prerequisite (WebGPU + html-in-canvas)

The render engine auto-passes `--enable-unsafe-webgpu` and `--enable-features=CanvasDrawElement` to its Chrome launch args. Stock Chromium and the bundled headless-shell **do not** support WebGPU + `drawElementImage` together — the combo that liquid-glass blocks need (`ios26-liquid-glass`, `macos-tahoe-liquid-glass`, `liquid-glass-*`, `vfx-liquid-glass`). For those blocks, point the engine at Brave (or Chrome canary) by setting `PRODUCER_HEADLESS_SHELL_PATH` to the browser binary before running `npx hyperframes render` / `preview`. Plain TypeGPU layers without HTML-as-texture work in headless-shell — only the html-in-canvas + WebGPU combination needs the override.

## Contract

- Initialize WebGPU asynchronously (`await navigator.gpu.requestAdapter()`), but register all GSAP tweens **synchronously** — before any `await`. The HyperFrames player reads the timeline immediately at page load.
- Render from HyperFrames time, not `performance.now()`.
- Listen for the `hf-seek` event and re-render at exactly that time.
- Guard against environments where WebGPU is unavailable — the adapter does not check for you.
- If the composition cannot render without WebGPU, add `data-requires-webgpu` to its composition root. Local capture commands then report an actionable error instead of capturing a no-GPU fallback screen when auto-detection selects software rendering. To render it on a host without a GPU, set `PRODUCER_ALLOW_SOFTWARE_WEBGPU=true`: it renders on SwiftShader, several times slower.
- After submitting GPU work, register queue completion synchronously with `e.detail.waitUntil(device.queue.onSubmittedWorkDone())`. HyperFrames awaits registered work before screenshots and frame capture.

The adapter sets `window.__hfTypegpuTime` and dispatches an `hf-seek` event with `{ time, waitUntil }` on each seek. While Studio is paused, HyperFrames may dispatch the same time again to keep the WebGPU swapchain presented. Re-render that exact time; do not advance simulation state.

## Basic Pattern

```html
<canvas id="gpu-layer"></canvas>
<script>
  (async () => {
    if (!navigator.gpu) return;
    const adapter = await navigator.gpu.requestAdapter();
    if (!adapter) return;
    const device = await adapter.requestDevice();
    const canvas = document.getElementById("gpu-layer");
    canvas.width = 1920;
    canvas.height = 1080;
    const ctx = canvas.getContext("webgpu");
    const fmt = navigator.gpu.getPreferredCanvasFormat();
    ctx.configure({ device, format: fmt, alphaMode: "opaque" });

    // Build your pipeline, buffers, bind groups...
    const timeUniform = new Float32Array([0]);
    const timeBuf = device.createBuffer({
      size: 16,
      usage: GPUBufferUsage.UNIFORM | GPUBufferUsage.COPY_DST,
    });

    function render(t) {
      timeUniform[0] = t;
      device.queue.writeBuffer(timeBuf, 0, timeUniform);
      const enc = device.createCommandEncoder();
      const pass = enc.beginRenderPass({
        colorAttachments: [
          {
            view: ctx.getCurrentTexture().createView(),
            loadOp: "clear",
            clearValue: { r: 0, g: 0, b: 0, a: 1 },
            storeOp: "store",
          },
        ],
      });
      pass.setPipeline(pipeline);
      pass.setBindGroup(0, bindGroup);
      pass.draw(3);
      pass.end();
      device.queue.submit([enc.finish()]);
    }

    render(0);
    window.addEventListener("hf-seek", (e) => {
      render(e.detail.time);
      e.detail.waitUntil(device.queue.onSubmittedWorkDone());
    });
  })();
</script>
```

## Timeline Registration

GSAP tweens that drive text, captions, or HTML elements must be registered **synchronously** — before any `await`:

```js
const tl = gsap.timeline({ paused: true });

// Caption tweens: synchronous, added before WebGPU init
gsap.set(".cap", { opacity: 0 });
tl.to("#cap-1", { opacity: 1, duration: 0.3 }, 1.0);
tl.to("#cap-1", { opacity: 0, duration: 0.2 }, 3.5);

window.__timelines["my-comp"] = tl;

// GPU-dependent tweens can go inside the async IIFE
(async () => {
  // ... WebGPU init ...
  const proxy = { value: 0 };
  tl.to(proxy, { value: 1, duration: 2, onUpdate: render }, 0.5);
})();
```

## Video-Backed Effects (Liquid Glass, Distortion)

To use a `<video>` as the GPU input texture:

```js
const videoEl = document.getElementById("aroll");

// Wait for video metadata before creating the texture
await new Promise((r) => {
  if (videoEl.readyState >= 1) r();
  else videoEl.addEventListener("loadedmetadata", r, { once: true });
});

// Create texture at the video's NATIVE resolution
const vw = videoEl.videoWidth,
  vh = videoEl.videoHeight;
const bgTex = device.createTexture({
  size: [vw, vh],
  format: "rgba8unorm",
  usage:
    GPUTextureUsage.COPY_DST | GPUTextureUsage.TEXTURE_BINDING | GPUTextureUsage.RENDER_ATTACHMENT,
});

function render(t) {
  try {
    device.queue.copyExternalImageToTexture({ source: videoEl }, { texture: bgTex }, [vw, vh]);
  } catch (_) {
    /* frame not decoded yet */
  }
  // ... draw ...
}
```

**Render-mode caveat:** headless Chrome may fail `copyExternalImageToTexture` for video elements. For production renders, pre-extract key frames via FFmpeg as PNGs and load them as image textures instead.

## Frosted Blur via Downsample Pass

A single-pass Gaussian kernel is too weak for glass-like frosted blur. Use a two-pass approach:

1. **Pass 1 — Downsample:** render the full-res texture to a small texture (1/6 resolution). Bilinear filtering during the downsample naturally averages pixels.
2. **Pass 2 — Glass composite:** sample the small texture for the frosted interior (bilinear upscale = heavy smooth blur) and the full-res texture for sharp areas and chromatic refraction.

This matches TypeGPU's `textureSampleBias` mip-level approach without generating mipmaps.

## Transparent vs Opaque Canvas

- **`alphaMode: 'opaque'`** — the GPU canvas renders the full frame (video + effect). Use when the GPU pipeline handles all visual content.
- **`alphaMode: 'premultiplied'`** — the GPU canvas is transparent where alpha = 0, letting HTML elements below show through. Use for overlays (particles, path animations) on top of a regular `<video>` element.

## WGSL Full-Screen Triangle

The standard vertex shader for full-screen effects (no vertex buffer needed):

```wgsl
struct Vo { @builtin(position) pos: vec4f, @location(0) uv: vec2f }

@vertex fn vs(@builtin(vertex_index) vi: u32) -> Vo {
  let ps = array<vec2f, 3>(vec2f(-1., -1.), vec2f(3., -1.), vec2f(-1., 3.));
  let ts = array<vec2f, 3>(vec2f(0., 1.), vec2f(2., 1.), vec2f(0., -1.));
  return Vo(vec4f(ps[vi], 0., 1.), ts[vi]);
}
```

Draw with `pass.draw(3)` — one triangle that covers the viewport.

## Rounded-Rect SDF (Liquid Glass Pill)

```wgsl
fn sdf_box(p: vec2f, half_size: vec2f, corner_radius: f32) -> f32 {
  let d = abs(p) - half_size + vec2f(corner_radius);
  return length(max(d, vec2f(0.))) + min(max(d.x, d.y), 0.) - corner_radius;
}
```

Use this to define inside/ring/outside zones for glass effects. Negative values are inside the shape.

## Deterministic Rendering

- No `Math.random()` — use a seeded PRNG.
- Do not use an autonomous `requestAnimationFrame` simulation loop. Render in response to `hf-seek`; HyperFrames owns the paused-presentation heartbeat and may re-present the same time.
- No `performance.now()` for animation time — read `window.__hfTypegpuTime` or `e.detail.time`.
- Register GPU completion with `e.detail.waitUntil(device.queue.onSubmittedWorkDone())` before the event listener returns.


<!-- ===== FILE: hyperframes/hyperframes-animation/adapters/waapi.md ===== -->

---
name: hyperframes-waapi
description: Web Animations API adapter patterns for HyperFrames. Use when authoring element.animate() motion, Animation currentTime seeking, document.getAnimations(), KeyframeEffect timing, fill modes, or native browser animations that must render deterministically in HyperFrames.
---

# Web Animations API for HyperFrames

HyperFrames can seek Web Animations API animations through its `waapi` runtime adapter. WAAPI is useful when you want native browser keyframes with JavaScript-created timing and no GSAP dependency.

## Contract

- Create animations synchronously during composition initialization.
- Use `element.animate(...)` with finite `duration` and `iterations`.
- Use `fill: "both"` so seeked states persist.
- Pause animations after creation or let the adapter pause them on first seek.
- Avoid callbacks and promises for render-critical state.

The adapter calls `document.getAnimations()`, sets each animation's `currentTime` to HyperFrames time in milliseconds, then pauses it.

## Basic Pattern

```html
<div id="orb" class="clip orb" data-start="2" data-duration="3" data-track-index="2"></div>

<script>
  const orb = document.getElementById("orb");
  const animation = orb.animate(
    [
      { transform: "translate3d(-160px, 0, 0) scale(0.8)", opacity: 0 },
      { transform: "translate3d(0, 0, 0) scale(1)", opacity: 1, offset: 0.35 },
      { transform: "translate3d(120px, 0, 0) scale(1.08)", opacity: 1 },
    ],
    {
      duration: 3000,
      delay: 2000,
      easing: "cubic-bezier(0.2, 0, 0, 1)",
      fill: "both",
      iterations: 1,
    },
  );

  animation.pause();
</script>
```

## Stagger Pattern

```js
document.querySelectorAll(".token").forEach((token, index) => {
  const animation = token.animate(
    [
      { transform: "translateY(24px)", opacity: 0 },
      { transform: "translateY(0)", opacity: 1 },
    ],
    {
      duration: 620,
      delay: index * 80,
      easing: "cubic-bezier(0.2, 0, 0, 1)",
      fill: "both",
      iterations: 1,
    },
  );
  animation.pause();
});
```

## Good Uses

- Lightweight DOM motion where CSS keyframes are too rigid and GSAP is unnecessary.
- Generated animations from structured data.
- Simple timelines that can be represented as keyframes, delays, and offsets.

## Composition Duration

The render engine needs the composition's total length to know how many frames to capture. GSAP timelines report duration automatically; a WAAPI-only composition has no timeline object, so the runtime infers duration from every animation's `effect.getComputedTiming().endTime` (offset by when the animation was created relative to composition start). `data-duration` on the root element is optional as long as every `element.animate()` call uses finite `duration` and `iterations` — which the contract above already requires.

Infinite `iterations` has no finite `endTime`, so it can't be auto-inferred — that's one more reason to avoid it (see Avoid below). If you must use it, add `data-duration="<seconds>"` to the root `[data-composition-id]` element or `npx hyperframes lint` will error (`root_composition_missing_duration_source`).

## Avoid

- Infinite `iterations`.
- Depending on `animation.finished` to mutate render-critical DOM.
- Running separate clocks with `requestAnimationFrame`, timers, or `performance.now()`.
- Animating layout properties when transforms and opacity can express the motion.
- Assuming clip-local start time is automatic. WAAPI adapter seeks document-level animation time; model clip offsets with `delay` or create the animation on an element whose visibility is controlled by HyperFrames timing.

## Validation

After editing a WAAPI composition:

```bash
npx hyperframes lint
npx hyperframes check
```

## Credits And References

- HyperFrames adapter source: `packages/core/src/runtime/adapters/waapi.ts`.
- Duration auto-inference: `packages/core/src/runtime/init.ts` (`resolveAdapterDurationFloorSeconds`), `getInferredDurationSeconds` in the adapter above.
- MDN Web Animations API guide: https://developer.mozilla.org/docs/Web/API/Web_Animations_API/Using_the_Web_Animations_API
- MDN `Animation.currentTime`: https://developer.mozilla.org/en-US/docs/Web/API/Animation/currentTime


<!-- ===== FILE: hyperframes/hyperframes-animation/blueprints-index.md ===== -->

# Blueprints (the proven shapes)

> Entry point to the blueprint layer. Read this to find the shape for a frame; read `blueprints/<id>.md` to instantiate it. The Step-4 method (Reproduce / Adapt / Compose, what to write per frame) lives in `visual-design.md` — this file is the menu + the picker.

A **blueprint** is a product-agnostic, **time-coded shot template** — `Scene N (a–b s): …` with `[slots]` and one named **signature move** — reverse-engineered from 178 golden product-launch clips across two mining rounds (plus 13 legacy blueprints reverse-translated to the same brief format). It encodes a whole shot across its full duration — reveals paced to the spoken line, not dumped at t=0 — so instantiating one structurally keeps content arriving instead of freezing. The full template lives in `blueprints/<id>.md`. **Step 4 (visual design) instantiates one blueprint per frame** (or composes from the motion vocabulary when none fits).

## The 22 blueprints

<blueprints>
<blueprint id="kinetic-type-beats" roles="Hook, Problem, Product_Intro, Benefits, CTA, Brand_Outro" duration="3.0–12.9s">
Flat, centered, bold-type shot where the **motion IS the words changing** — a fixed line swaps tokens in place by hard cut, or a statement builds across full-screen beats (each its own move) onto a spring-pop payoff. The workhorse (6 roles). Reach for it whenever the words carry the shot and there's no set, surface, or click.
</blueprint>

<blueprint id="typewriter-reveal" roles="Hook, Brand_Outro" duration="3.6–7s">
A live text caret **types (and edits) a line as a human would**, then collapses it and pops a brand payoff, or holds it under a persistent mark while a sub-line types into the final CTA. Reach for it when "someone is typing this" should be the engine — a relatable typed pain → brand, or a standing logo + a typed CTA rail.
</blueprint>

<blueprint id="spatial-pan-stations" roles="Hook, Problem, Product_Intro" duration="7–10s">
Pre-placed labeled **stations on one oversized canvas, traversed by a single virtual camera** — repeated lateral/diagonal pans centering each station and revealing a callout, landing held on the last. Reach for it for a milestone timeline panned to "us," a connected web of pain stations ending in a tangled knot, or a two-shot concept-decode strip bridged by one lateral pan into a live demo.
</blueprint>

<blueprint id="camera-journey" roles="Benefits, Key_Feature" duration="5.6–11.1s">
The real viewport camera is the STORYTELLER — a **multi-leg motivated journey** (dive in → a beat fires → travel to the consequence / reposition → landing push) across one continuous world. Two sub-shapes: **(A) action roundtrip** — dive to a panel, a click/send fires, the camera swoops to where the consequence renders as element motion; **(B) cursorless flight** — pure cinematic 3D flight (motion blur, DoF, tilt-to-flatten), no cursor anywhere. Reach for it when the camera's travel itself tells the cause→effect (or spectacle) story — not when it chases a cursor (cursor-ui-demo) or presents one hero device (device-surface-showcase).
</blueprint>

<blueprint id="zoom-out-workspace-reveal" roles="Hook, Benefits" duration="6.8–11s">
Open TIGHT on one full-bleed detail — a graphic macro or a small UI region — let micro-action play in close-up, then **ONE continuous decelerating zoom-out reveals the containing whole** (design-tool workspace / multi-pane agent workspace); the frame locks and element-level payoff carries on. The zoom-out IS the engine — the structural inverse of the push-in shapes; no zoom-in anywhere. Reach for it to open on a mystery detail that re-scopes into "this is where it lives," or to land a scale/breadth payoff ("that was one corner of everything it did").
</blueprint>

<blueprint id="constellation-hub" roles="Hook, Social_Proof, CTA" duration="5–8s (scatter-drift end card ~2.5s)">
Iconned **nodes spring into a ring around a center**, then resolve on the core — a camera push-IN (depth-of-field collapsing onto it), a held hub mark with satellites orbiting it, or a cursor click that COLLAPSES the orbit and springs the product demo out of it (CTA). Reach for it for "it connects everything / one hub" or "sits at the center of your stack." Third finisher (scatter-drift end card): no ring, no camera — ~20 icons pop in scattered frame-wide around a serif headline and drift slowly outward under a fully static frame.
</blueprint>

<blueprint id="grid-card-assemble" roles="Key_Feature, Benefits, Social_Proof" duration="3.0–10.5s">
N items (tiles / cards / logos / list-lines) **self-assemble in a staggered cascade** into a grid or vertical list and hold; an optional camera zoom-OUT reveals the array inside a vaster whole. Reach for it to enumerate breadth at once — a feature grid, an accumulating benefit list, a logo wall, a self-populating live data board, or a streaming field that clears to a payoff line.
</blueprint>

<blueprint id="logo-assemble-lockup" roles="Product_Intro, CTA, Brand_Outro" duration="4.4–11s">
A brand mark / wordmark **comes to exist on screen** — built from parts (elements assemble/orbit, letters cascade, an outline draws on, a camera pushes through negative space), spring-bloomed whole from zero on a cleared stage, morphed in one unbroken chain out of the preceding phrase, absorbed from a pixel streak, or already assembled and settling as satellites clear — and resolves into a centered lockup, optionally extended to a URL/CTA/end card. Reach for it for a wordless premium brand sting, a logo build leading into the final ask, or any brand-outro lockup beat.
</blueprint>

<blueprint id="cursor-ui-demo" roles="Product_Intro, Key_Feature, Hook, Benefits" duration="4.0–12.9s">
A visible custom **cursor drives a reconstructed app UI** through clicks/hovers/drags so the screen changes state shot-to-shot, while the camera chases each interaction (or holds a locked static stage while element swaps do the "camera work"). Reach for it for a first cursor-led look at the surface (Product_Intro), one workflow demonstrated end-to-end onto the action button (Key_Feature), an ambient multi-cursor canvas hook, or a demo|text|demo Benefits sandwich.
</blueprint>

<blueprint id="device-surface-showcase" roles="Key_Feature, Product_Intro" duration="5–11.3s">
A **device mockup or floating window held as hero** while its screens cycle through a real flow, presented by a camera ranging from a static hold to a continuous 3D push. Mechanic-rich (static tour · floating-window push-scroll · 3D-hand demo · cursorless stepwise-flow · showcase-carousel); the stepwise-flow variant widens it to Product_Intro. Reach for it to show a feature experienced *inside its real interface*, or a product introduced by *completing its core loop*.
</blueprint>

<blueprint id="prompt-type-submit-generate" roles="Hook, Product_Intro, Key_Feature, CTA" duration="5.2–12s">
The AI-era demo shot: a **prompt/query/command types into a real product input and the machine answers** — status theater into a streaming answer / action log / diff cards / chart / generated artifact (full loop), an instant result surface that gets re-queried (search / generated page / preview flip), or the clip cuts at the submit and the ask itself is the show (incl. the install-command CTA end card). Reach for it whenever the beat is "watch me ask, watch it answer" — the keyboard drives, not a clicked-through UI (that's cursor-ui-demo) and not bare typed typography (that's typewriter-reveal).
</blueprint>

<blueprint id="agent-progress-theater" roles="Key_Feature" duration="4.2–11.6s">
Agent work performed as **working-state theater** — a single trigger beat (menu pick, modal click, a scan already running) hands the frame to the machine: loaders spin and status phrases swap while it visibly works, then the receipt cascades in — a checklist/findings card whose rows arrive and CHECK OFF (badge flips, strikethroughs, severity pills), or a conversation thread building message-by-message to a camera push-in on the confirmation. Reach for it to dramatize an agent doing multi-step work where the state mutation IS the demo — no typed prompt, no cursor-driven workflow, no static enumeration.
</blueprint>

<blueprint id="panel-edit-live-sync" roles="Key_Feature" duration="5.3–11.9s">
A bipartite stage — an inspector/editor **panel bound to a target surface** — where a cursor (or caret) continuously manipulates a control (value scrub, unit/codegen dropdown, easing-handle drag, inline retype) and the coupled surface **updates live in the same beat**; the camera holds or punch-and-returns but never loses the couple. Reach for it when the feature IS live editing/inspection — "change this, watch it change" — not a click-through workflow (that's `cursor-ui-demo`).
</blueprint>

<blueprint id="transcript-scroll-artifact-reveal" roles="Key_Feature" duration="5–11.8s">
The frame travels vertically along one LONG full-bleed content surface — an agent transcript, task feed, or analysis document (no device frame) — by camera pan or element scroll, **reading the generated work as evidence**; then ONE focal interaction (file-chip click, quote highlight, row expand) pivots into an artifact reveal (workspace zoom-out, spreadsheet scale-up onto highlighted cells, inline panel). Reach for it when "the AI did a lot of work → here's the deliverable" is the beat — the traversal is the proof, the artifact is the payoff.
</blueprint>

<blueprint id="dataviz-countup" roles="Hook, Problem, Product_Intro, Key_Feature, Social_Proof" duration="4–12s">
Numbers and charts are the hero — a **count-up ring/number, trend chart, tilted stat grid** — traversed by a camera that pushes THROUGH (or scrolls across) them to land on one hero metric. Reach for it when the data carries the argument: quantify a worsening problem, open confidently on "look at the result," cold-open on one exploding statistic, prove a feature with a dark cursor-scrubbed stat montage, or guest-star a single gauge count-up as one beat inside a type relay.
</blueprint>

<blueprint id="titlecard-reveal" roles="Benefits, Social_Proof, CTA, Product_Intro" duration="3–5s">
The calm **breather/landing beat** — one clean title or single brand/proof card revealed with exactly ONE restrained move (slide-up crossfade, or wipe-away-to-reveal), then a still hold. Low motion is the payload, not a deficiency. Reach for it for a two-line value title, or a busy open wiped to a clean lockup + a "loved by N+ teams" stat. Also runs as a card CHAIN — 2–3 near-still monochrome cards seamed by instant hard cuts (CTA end-card stack) or blur-snap handoffs (Product_Intro title prelude), terminating on the held logo; chains run 2–3s per card, ~5.5–9.5s total.
</blueprint>

<blueprint id="comparison-split" roles="Key_Feature" duration="4–6s">
Two paired items of equal weight enter from opposite wings with **mirrored 3D "book-open" tilts** and hold side-by-side, then an inner-edge pill badge spring-pops on each to punctuate. Reach for it for an A/B or "X + Y together" — two complementary capabilities weighed at once (not >2 items, not sequential steps).
</blueprint>

<blueprint id="overwhelm-surround" roles="Problem" duration="6–9s (clutter-shove variant ~10s)">
Overwhelm by accumulation — recognizable surfaces assemble, density-marker icons scatter in, the center one **morphs into the viewer's own avatar**, then elements close in from all sides (surrounded, not zoomed-into). Reach for it when the pain is "you're buried in tools," ending on a claustrophobic crowd. Second resolution (clutter-shove-to-question): the accumulation runs under a slow zoom-out, then a push-in shoves the clutter to the frame edges and a two-part serif question builds in the opened center — camera-driven, no avatar.
</blueprint>

<blueprint id="ticker-takeover" roles="Hook, Brand_Outro" duration="5–7s">
A typed lead-in + an accent word cycling through options, then a hero **crashes in from off-screen and physically shoves the text aside** — a collision, not a fade — settling alone. Reach for it when a "could be many things" build should be violently replaced by "this is it."
</blueprint>

<blueprint id="fixed-anchor-cycle" roles="Hook, Benefits, Brand_Outro" duration="6.6–11.1s">
One element stays PINNED — a wordmark, composer box, or anchor line that enters once and **never moves** — while the adjacent region (or the entire surrounding theme) cycles through many discrete states: hard-cut label swaps, a vertical carousel, per-word highlight stepping, or in-place theme morphs, cadence often manipulated (steady stepping or a slow→accelerating flurry), resolving on an emphasis beat into a completed lockup. Reach for it to assert breadth around one fixed identity — "everyone says / works everywhere / calling all X" — where the anchor's stillness IS the claim.
</blueprint>

<blueprint id="video-text-pivot" roles="Product_Intro, Key_Feature" duration="6–8s">
A product video holds center and breathes, then **slides aside to hand its weight to a hero stat**, then both clear and kinetic text types into the vacated center, sealed by a gradient pill. Reach for it for "see the feature → see the impact" where the video must stay visible (slides, never cuts).
</blueprint>

<blueprint id="cta-morph-press" roles="CTA, Hook" duration="4–6s (Hook opener 5–7.5s)">
A resting brand mark **condenses at the same center into a brighter CTA**, then a cursor arrives and lands a human-aimed click with feedback. Reach for it for a focused "click here" sign-off that walks the eye from identity to action — no spatial set, no multi-step UI. Role-widened to Hook: the same machinery as an OPENER — a lone widget (pill/chip) on a flat field morphs in place (pill→menu, chip→prompt card), performs its payload, then vanishes to a typed closing title.
</blueprint>
</blueprints>

## Role → blueprint menu

A **SOFT** menu: story truth comes first. Story-design reaches in **when the product's own beat calls for that shape** — it suggests a proven shape, it never dictates which beats exist. Each role has 4–11 options; if none fits the beat, compose freely (the menu is not a checklist). Each line is the **trigger** that should make you reach for that blueprint.

Roles here map 1:1 to the storyboard frame `type` enum: **Hook**=`hook` · **Problem**=`pain_point` · **Product_Intro**=`product_intro` · **Key_Feature**=`feature_showcase` · **Benefits**=`benefit_highlight` · **Social_Proof**=`social_proof` · **CTA**=`cta` · **Brand_Outro**=`branding`.

**Hook**

- `kinetic-type-beats` — a punchy rhetorical line / "you keep doing X" callout where the in-place word-swap is the joke, an escalating multi-beat statement landing a spring-pop payoff, word beats resolving into a logo reveal, or a centered beat triptych (a beat may be a non-text element).
- `typewriter-reveal` — type a relatable line, collapse it, pop the brand (logo or product-UI) — "here's the everyday pain, now here's us."
- `spatial-pan-stations` — a timeline of milestones panned to the present ("evolution leading up to us").
- `constellation-hub` — a constellation of tools/nodes + a camera push-in ("it connects everything").
- `cta-morph-press` — a lone widget on a flat field morphs in place (pill→menu, chip→prompt card), performs, then vanishes to a typed title ("one widget doing one thing" opener).
- `ticker-takeover` — a cycling accent word ("could be X, or Y…") violently replaced by a hero crashing in from off-screen.
- `fixed-anchor-cycle` — a static lead line holds while an accent line carousels through an audience/option roll-call beneath it, then clears into statement beats landing the brand line.
- `prompt-type-submit-generate` — "watch me ask": a typed headline → one push-in onto the product's input → the prompt types and the clip ends at the submit; or the whole demo loop runs and a second command starts before the cut.
- `cursor-ui-demo` — an ambient multi-cursor workshop: labeled teammate cursors work a design canvas live (grab-drag-drop, recolor on drop) while a headline builds over the demo — the live workshop itself is the hook.
- `dataviz-countup` — a cold-open counter burst: icons puncture in clustered at center, one dramatic statistic explodes upward in size as the icons fling outward to their marks, closed by a slow lean-in.
- `zoom-out-workspace-reveal` — a full-bleed graphic mystery (blob / blossom / macro) resolved by one unbroken decelerating pull-back through nesting levels into the design-tool workspace that made it; canvas keeps animating after the lock.

**Problem**

- `kinetic-type-beats` — 3–5 short pain statements each landing alone on a bare canvas, or a question/hook phrase relay scale-popping through center (optionally resolving on a product surface as an element move).
- `spatial-pan-stations` — pan a connected web of pain "stations" ending in a tangled knot.
- `dataviz-countup` — a count-up ring / chart / stat grid pushed-through to dramatize a worsening or large problem.
- `overwhelm-surround` — recognizable tools that morph into the viewer, then task bubbles close in from all sides ("you're buried").

**Product_Intro**

- `kinetic-type-beats` — "Introducing…" hard-cut name-drop resolving on the brand name/logo; also a fixed headline with one swapping word-slot, a word-by-word run with per-hero-word effect payoffs, or an anchored wordmark that transforms out.
- `logo-assemble-lockup` — a wordless premium brand sting (elements pulse/orbit and assemble around the mark).
- `cursor-ui-demo` — first look at the product surface; a cursor sweeps in to introduce the app.
- `dataviz-countup` — hard-cut into a data-viz card grid, camera scrolls to a glowing hero metric + a kinetic tagline.
- `video-text-pivot` — a product video that slides aside to hand its weight to a hero stat, then yields the center to kinetic impact text.
- `spatial-pan-stations` — a two-shot strip bridged by ONE lateral pan: a static phrase's accent word 3D-flap-decodes (the concept lands), then the camera pans with parallax into a live cursor-typing demo.
- `prompt-type-submit-generate` — the first look at the product is its composer or search bar — a long prompt (or short query) types with attachments / dropdown picks / live autocomplete, steering to the confirming control.
- `device-surface-showcase` — a cursorless end-to-end flow (setup/auth → action → success) completed inside the held surface, bookended by title cards.
- `titlecard-reveal` — a three-beat dark title prelude (logo pop → name+version append → tagline card) chained by blur-snap handoffs before any product UI.

**Key_Feature**

- `grid-card-assemble` — a labeled feature tile/pill grid that self-assembles (or glass cards revealed by a camera zoom-out; or a live-populating data board — skeleton fills, tethered cards, post-assembly status flips).
- `cursor-ui-demo` — a specific multi-step workflow demonstrated end-to-end, landing on the action button/result.
- `device-surface-showcase` — a device/window hero whose screens cycle (static tour · floating-window push-scroll · 3D-hand demo).
- `comparison-split` — two paired capabilities side-by-side with mirrored book-open tilts (an A/B / "X + Y together").
- `video-text-pivot` — a feature clip that slides aside to a frame-filling metric, then a typographic impact line.
- `dataviz-countup` — dark-scrub-montage: kinetic headline beats cut-stitched with self-drawing charts and a cursor-scrubbed dashboard (`chart-scrub-readout`).
- `prompt-type-submit-generate` — the capability as one prompt→response round trip: submit into thinking states, then a streaming answer, action log, diff cards, chart, or instant generated artifact.
- `agent-progress-theater` — the feature is the agent WORKING (plan / scan / fix / automation): loader + status theater resolving into a checklist that checks off, or a thread that builds to a confirmation payoff.
- `panel-edit-live-sync` — an inspector/editor panel edit-syncs a bound target live (scrub → it rotates, retype → it resizes, pick → it converts); for features whose value prop is the live coupling itself.
- `camera-journey` — a cursorless cinematic 3D flight over the product surface — motion blur, depth-of-field, tilt-to-flatten — landing violently on the CTA / hero card (sub-shape B).
- `transcript-scroll-artifact-reveal` — a long transcript/feed/document traversed vertically as evidence of generated work, then one interaction pivots into the artifact ("it did all this → here's the deliverable").

**Benefits**

- `kinetic-type-beats` — a rapid-fire staccato montage of 8–12 short value phrases, or a slow 2–4-statement relay each held ~1.5s+.
- `grid-card-assemble` — a vertical benefit list that accumulates, steps, or streams past a focal slot, optionally clearing to a payoff line.
- `titlecard-reveal` — a calm two-line value title card (a breather/stillness beat).
- `camera-journey` — a small action in one panel pays off in another region, and a real camera swoop physically connects cause to effect (sub-shape A).
- `zoom-out-workspace-reveal` — micro-actions in extreme close-up on one small UI region, then one fast decelerating zoom-out reveals the huge multi-pane agent workspace; the wide holds while the deliverable payoff completes.
- `fixed-anchor-cycle` — one product surface pinned dead-center while its whole theme re-skins per beat ("the same prompt, in every tool").
- `cursor-ui-demo` — the demo|text|demo sandwich: two static-stage demo beats bridged through a full-screen kinetic/title interlude and back.

**Social_Proof**

- `constellation-hub` — product mark as the hub, partner logos orbiting it ("works with your stack").
- `grid-card-assemble` — a logo wall that builds then pulls back to reveal a vast ecosystem.
- `titlecard-reveal` — wipe a busy open away to a clean brand lockup + a "loved by N+ teams" stat.
- `constellation-hub` — scatter-drift end card: ~20 app icons pop in frame-wide around a serif headline and drift outward under a static frame ("connects to thousands of apps").
- `dataviz-countup` — one radial-gauge count-up instrument embedded as a single beat inside a kinetic-type relay.

**CTA**

- `kinetic-type-beats` — a punchy closing line (or short value stack) snapping beat-by-beat onto the logo/URL, or a 3–5-beat chain where each beat carries its own kinetic gag before the logo forms.
- `logo-assemble-lockup` — a logo build → camera push-through into the final URL/CTA verb.
- `cta-morph-press` — a brand mark that condenses into the CTA at one center, then a cursor lands a human-aimed click.
- `titlecard-reveal` — a monochrome end-card chain (statement → CTA line → wordmark/logo) seamed by instant hard cuts, ending on the logo held to the final frame.
- `constellation-hub` — orbit-collapse: category icons drift around an empty central CTA, a cursor click implodes the orbit toward the click point, and the product demo springs OUT of the collapse.
- `prompt-type-submit-generate` — the install-command end card: headline demotes, a terminal pill springs in, the command types and holds with a blinking cursor.

**Brand_Outro**

- `kinetic-type-beats` — a rapid verb barrage resolving on the brand's one defining word, or a relaxed full-frame beat relay terminating in a long-held URL end card.
- `typewriter-reveal` — a persistent brand mark with a typed/swapping CTA rail beneath it.
- `logo-assemble-lockup` — feature/UI elements clear the stage and the lockup draws itself in.
- `ticker-takeover` — options cycle, then the brand mark crashes in and owns the frame.
- `fixed-anchor-cycle` — the wordmark pins while praise quotes / tagline highlights cycle beside it (optionally accelerating), resolving into the finished lockup.

> Coverage: every role has ≥2 options; every blueprint serves ≥1 role. `kinetic-type-beats` is the workhorse (6 roles); `dataviz-countup` now spans 5; `device-surface-showcase` (once role-narrow) now also serves Product_Intro via the mined stepwise-flow variant. Five shapes — `comparison-split`, `overwhelm-surround`, `ticker-takeover`, `video-text-pivot`, `cta-morph-press` — were added from the hyperframes-animation blueprints; seven more — `prompt-type-submit-generate`, `agent-progress-theater`, `panel-edit-live-sync`, `camera-journey`, `transcript-scroll-artifact-reveal`, `zoom-out-workspace-reveal`, `fixed-anchor-cycle` — were mined from the golden-clip corpus.

## Picking guidance

1. Find the frame's **role** in the menu above; pick the blueprint whose **shape fits this beat** (story may already have named a candidate id — confirm or override). If two fit, prefer the one whose motions are closer to your plan.
2. Open `blueprints/<id>.md` — read its time-coded template, `[slots]`, and named **signature move**.
3. Choose a posture — **Reproduce** (slots map cleanly), **Adapt** (structure fits, content/surface differs; keep the signature move), or **Compose** (nothing fits → build from the motion vocabulary). The _how_ of writing each — what to keep/change, the per-frame fields — is `visual-design.md`'s job; defer to it.
4. If nothing in the menu fits the beat, **compose** from the motion vocabulary in `motion-language.md` — still pace the reveals to the VO across the shot. Don't force a wrong blueprint.

## Motion coverage

Every recurring move in the golden vocabulary is backed by this skill's local `rules/` — including five added to round out the corpus: `depth-of-field-blur`, `motion-blur-streak`, `depth-scatter-assemble`, `spring-pop-entrance` (the canonical entrance pop, distinct from the click/press `press-release-spring`), and `ambient-glow-bloom`. Each blueprint's `rule mapping` cites the real rule.

Variant provenance (`from <shape-name>`) names the mined golden shape a variant was reverse-engineered from; the case-level golden map lives with the c2v-bench mining reports (maintainers only — consuming agents need only the shape names).

One genuine out-of-scope special remains: `device-surface-showcase`'s **3D-hand gesture-input + WebGL bloom/portal** needs R3F/Three.js + WebGL — a heavier capability than the rule library. Use it sparingly, or pick a simpler `device-surface-showcase` variant.


<!-- ===== FILE: hyperframes/hyperframes-animation/blueprints/agent-progress-theater.md ===== -->

# agent-progress-theater — Agent Progress Theater

**intent**: Agent work performed as WORKING-STATE theater — a short trigger beat hands the frame to the machine, which then visibly _works_: loaders spin, status phrases swap, dots pulse, counters tick — before the receipt arrives as a card whose rows cascade in and CHANGE STATE (badges flip to checks, labels strike through, severity pills read out), or as a conversation thread building message-by-message onto a camera push-in payoff. The subject is the machine performing labor over time. It is NOT a typed prompt awaiting output (no prompt/input is ever typed — the trigger is a click, a menu choice, or an already-running scan); NOT `cursor-ui-demo` (at most ONE igniting click here, then the cursor exits and the UI performs itself); NOT `grid-card-assemble` (rows there assemble into a static enumeration and hold — rows here are alive: they arrive as agent output and then MUTATE, checking off one by one while the viewer watches).

**roles served**

- Key_Feature (from `agent-progress-theater`): when the feature is the agent doing multi-step work (build a plan / scan a repo / fix a vulnerability / handle infra for you) and the proof is status theater — a loader lockup with a typed label, status couplets swapping under an `[accent]` spinner, then a checklist/findings card that populates and checks off in front of the viewer.
- Key_Feature (from `message-thread-payoff`): when the agent's work lives inside a conversation or automation thread — user/agent bubbles and tool-call/reply cards popping in sequence, the working state carried by pulsing loading dots or rapidly ticking diff counters, resolved by ONE camera push-in tight on the confirmation line (`[reaction pill]`, "Sent using `[@Bot]`", a thank-you bubble).

**duration**: 4.2–11.6s (short members are a single card-and-check-off or thread beat at ~4–5s; long members chain trigger → interstitial → status swaps → receipt card at ~9–12s; thread payoff spans 4.2–9.1s)

**shot structure** (a warm flat canvas — `[off-white / warm beige / near-white bg]`, optional `[faint grid / dot-grid / wavy-line]` texture; white rounded cards with soft drop shadows; ONE `[working accent]` color reserved for the machine (spinner, status words, active step) and one `[done color]` for completion (checks, "Completed"); camera static or ONE slow move — motion is overwhelmingly element-level springs, staggers, and state flips. Two folded sub-shapes — **(A) checklist/findings theater** and **(B) message-thread payoff**.)

- **Scene 1 (0.0–~1.5s) — the trigger.** Something asks the machine to work, in ONE beat:
  - _Variant — option menu (A)_: a centered white pill card poses `[the question]`; it SPRINGS open downward into a rounded menu — `[3–4 option rows]` fade/slide in staggered, each with a number badge. A cursor enters, hover-dances between rows (a pale `[hover fill]` highlight follows it), and CLICKS the chosen row (~press-down spring); the whole menu scales down toward its center and fades out. This is the only cursor appearance in the shot.
  - _Variant — modal click (A)_: close-up of a white modal with `[Dismiss]` / `[action button]`; a hand cursor clicks the action (quick press-down spring); the modal fades away. Optionally followed by a serif `[interstitial line]` on the bare canvas — words land staggered, hold, fade out word-staggered as the bg swaps.
  - _Variant — already working (A)_: a `[Scan in progress]`-style state — a thin `[accent]` arc spinner rotating over a heading + body copy + a `[Starting…]` pill (cursor resting on it, motionless); only the spinner moves. The whole scene then rapidly scales up and fades — a push-through exit.
  - _Variant — workspace push-through (A)_: a rapid camera push-in THROUGH a multi-panel `[workspace: builder / editor / terminal]` — panels scale past the viewport edges and clear away to the bare canvas.
  - _Variant — thread opener (B)_: a `[user bubble]` spring-pops in ("`[the ask]`"), OR a stats card pops in whose green/red `[diff counters]` rapidly tick and settle — the automation's opening receipt.

- **Scene 2 (~1–4s) — the working state (the machine performs).** The frame belongs to the machine; nothing is clickable. Pick 1–3 working motifs and CHAIN them:
  - A loader lockup: a spinning `[accent asterisk / arc]` beside a `[working label]` typed on rapidly ("`Buildi` → `Building plan…`"), a left→right shimmer sweep passing through the letters; the spinner may momentarily morph asterisk↔dot and back.
  - Status couplets: 2–3 centered pairs — a dark `[action line]` over an `[accent status word]` ("Thinking…", "Noodling…") with its spinner — swapping via quick fades/slides at a steady cadence.
  - A `[scan/tool label]` types/expands rightward to its full string, then SHRINKS and DOCKS to the top-left as a fixed corner header (the canvas now belongs to what it produces).
  - A status heading flips tense as rows land beneath it ("Using `[Tool]`" → "Used `[Tool]`"), with a gently pulsing "Thinking" and gray meta-lines ("Exploring `[N]` files…") fading in below.
  - _Variant — thread machinery (B)_: the `[agent reply]` fades/slides up, then a monospace `[tool_call]` line appears beneath it — small icon + `[tool name]` + three pulsing loading dots; OR an instruction bubble scrolls into view (internal window scroll, frame static) followed by a `[brand logo]` pop-in beside a "Sending message…" row. **The pulse dies the instant the result lands** — dots vanish as the payload arrives.

- **Scene 3 (~2–4s) — the receipt cascades in (the payoff engine).** The work materializes as a card that BUILDS:
  - _Variant — checklist (A)_: a white `[Progress / summary]` pill or card SPRING-pops in with a bounce, then springs open downward (or the summary card glides UP as a taller `[findings]` panel expands beneath it). Rows cascade in one by one — slide-up + fade, staggered — each with `[number badge / severity pill]` + `[label]` + optional gray `[meta line]`. Then the STATE MUTATION runs: badges flip one by one from numbered outline to a solid `[done color]` circle + white checkmark (slight scale bounce), the checked label simultaneously strikes through and dims; pending items keep partially-drawn arc outlines animating. End the run mid-list — some items checked, some still numbered — the work is visibly _ongoing_.
  - _Variant — thread payload (B)_: the camera pushes in / pans down centering the `[tool_call]` line as a white payload card expands downward from it — 2–4 light monospace `[key: value]` lines fading in. Then the `[resolution message]` expands into place below (inline `[code chips]` and `[link]` coloring), OR a dark `[thread card]` scales up from a status row to DOMINATE the frame while the background darkens, its `[reply]` expanding into place under a "1 reply" divider.

- **Scene 4 (final ~1–2.5s) — resolve.** Two endings:
  - _Variant — hold / scroll (A)_: the finished (or mid-mutation) card stack holds static to the end, OR the viewport scrolls down the final card (fast in the last beat) revealing `[a second heading + numbered list]`, ending mid-list. A slow continuous zoom into the card may run underneath (the header drifts off the top of frame).
  - _Variant — payoff push-in (B)_: ONE camera push-in + pan-down lands tight on the payoff line — "`Sent using [@Bot]`" / the confirmation + `[thank-you bubble]` spring-in — then a `[reaction button]` springs into an active pill with bouncy overshoot and a count. The push eases into a gentle near-imperceptible drift and the clip ends on the close-up. No end card.

**motion vocabulary**: pill springs open downward into a menu/checklist · option rows fade/slide in staggered · cursor hover-dance (pale highlight fill follows the cursor between rows) · single igniting click with press-down spring · menu scale-down fade exit · modal fade-away · thin `[accent]` arc spinner rotation · spinning asterisk loader · asterisk↔dot morph · typed-on loader label with caret · left→right text shimmer sweep · serif interstitial with word-staggered fade in/out · status couplets swapping via quick fades/slides under an `[accent]` spinner · pulsing "Thinking" label · status heading tense flip (Using→Used) · label types/expands rightward then shrinks and docks as a corner header · scene scale-up/fade push-through exit · rapid camera push-in through a multi-panel workspace · slow continuous zoom into a card (header drifts off frame) · summary card spring pop with bounce · card glides up as a panel expands beneath it · anchored downward panel/payload expansion · rows stagger in (slide-up + fade) · badge flip from numbered outline to solid circle + white checkmark with scale bounce · strikethrough + dim on completion · partially-drawn arc outlines animating on pending items · severity-pill readouts (Critical / High) · viewport scroll down the final card · chat bubble spring scale-up pop-in · reply fade/slide-up · monospace tool-call line with three pulsing loading dots (dots die the instant the result lands) · payload card expands downward from the line · green/red diff counters rapid tick-and-settle · internal window scroll (frame static) · brand logo pop-in beside a status row · card scales up from a row to dominate the frame while the background darkens · reply message expands into place · inline code chips / link coloring · reaction button springs into an active pill with bouncy overshoot + count · camera push-in + pan-down centering the payoff · slight pull-back · gentle end drift · static hold.

**rule mapping**

- pill springs open downward into a menu / panel expands beneath a gliding card / payload card expands downward from a tool-call line → `anchored-layout-expand` (edge-anchored container growth: height-masked wrapper + inner counter-translate, container drawn at final size); spring flavor from `spring-pop-entrance`
- option rows / findings rows / task rows stagger in (slide-up + fade) → `spring-pop-entrance` (staggered-group form, ≤500ms cap) or `gsap-effects` (plain fade+translate stagger) — NOT `waterfall-entry` (its binary no-fade arrival law contradicts this dialect's soft fade/slide cascade)
- cursor glides to a row and clicks; hand cursor clicks the modal button → `cursor-click-ripple` (move + press) + `press-release-spring` (the button's press-down spring)
- pale hover-highlight fill following the cursor between rows → `gsap-effects` (a background fill translated row-to-row; no dedicated rule needed)
- menu scale-down fade exit / scene scale-up push-through exit / palette-for-window swap → `scale-swap-transition`
- thin arc spinner rotation / spinning asterisk loader → `svg-icon-enrichment` (rotating internal SVG parts via `setAttribute('transform','rotate(deg cx cy)')`; timeline-driven, finite)
- asterisk↔dot morph and back → `scale-swap-transition` (two elements morphing at the same center)
- typed-on loader label ("Building plan…") / scan label typing to its full string → `discrete-text-sequence` (+ `context-sensitive-cursor` for the caret)
- left→right shimmer sweep through the loader letters → `ambient-glow-bloom` (single-pass traveling sheen) or `css-marker-patterns` (highlight sweep) — pick sheen for light-on-text, marker for a drawn band
- serif interstitial word-staggered fade in/out; status couplets swapping on a cadence → `dynamic-content-sequencing` (phrase windows) + `discrete-text-sequence` (the whole-state swaps); per-word stagger via `gsap-effects`
- pulsing "Thinking" label / three pulsing loading dots (phase-offset) → `sine-wave-loop` (finite repeats; kill the tween at the resolve beat — see doctrine note)
- status heading tense flip (Using→Used) / gray meta-lines fading in / final-token snaps → `discrete-text-sequence`
- label shrinks and docks to the top-left as a fixed corner header → `gsap-effects` (plain scale + translate tween; no dedicated rule needed)
- rapid camera push-in through the multi-panel workspace → `viewport-change` (the push) + `multi-phase-camera` (phasing) + optional `motion-blur-streak` (velocity blur as panels clear the frame)
- slow continuous zoom into the receipt card (header drifts off top) → `multi-phase-camera` (steady-push phase) or `viewport-change`
- summary card / progress pill / chat bubble / brand logo / file chip spring pop-in → `spring-pop-entrance`
- summary card glides up as the findings panel expands beneath → `gsap-effects` (the glide) + `anchored-layout-expand` (the panel)
- badge flip: numbered outline → solid circle + white checkmark with scale bounce → `scale-swap-transition` (outline↔solid swap at same center) + `svg-path-draw` (checkmark draw-in) + `spring-pop-entrance` (the bounce); the pending→active→complete progression itself → `dynamic-content-sequencing` (a snap state machine, per cursor-ui-demo's workflow-approve-press precedent)
- strikethrough + dim on the checked label → `css-marker-patterns` (strike-through draw) + `gsap-effects` (opacity dim)
- partially-drawn arc outlines animating on pending items → `svg-path-draw` (partial dashoffset, held mid-draw)
- viewport scroll down the final card / internal window scroll under a static frame → `gsap-effects` (transform-only content translate inside a masked window) — use `viewport-change` only if the FRAME moves
- green/red diff counters rapid tick-and-settle → `counting-dynamic-scale` (numeric proxy count-up; suppress the scale-growth component — these tick at fixed size)
- dark thread card scales up from a row to dominate the frame → `card-morph-anchor` (row → full-frame morph + handoff) with the background darkening as a `gsap-effects` overlay fade
- reply message / resolution line expands into place → `spring-pop-entrance` (soft overshoot) or `anchored-layout-expand` for a true downward growth
- reaction button springs into an active pill with overshoot + count → `spring-pop-entrance` (the pop) + `press-release-spring` (activation flavor) + `counting-dynamic-scale` (the count, if it ticks)
- camera push-in + pan-down centering the tool call / the payoff line → `coordinate-target-zoom` (non-centered target: scale + counter-translate) or `viewport-change`
- slight pull-back then gentle end drift → `multi-phase-camera` (pull-back phase + continuous micro-drift; keep the drift near-imperceptible)
- static hold on the final stack → no rule needed

**camera modifier** (default is a STATIC frame — the theater is element-level; at most ONE real move per shot, chosen from):

- Trigger push-through: a rapid push-in through the opening workspace that clears to the bare canvas → `viewport-change` + `multi-phase-camera`, optional `motion-blur-streak`.
- Receipt zoom: one slow continuous zoom into the checklist card across the whole mutation run, letting the header drift off the top → `multi-phase-camera` (steady push).
- Payoff push-in (sub-shape B's defining move): static through the build, then ONE push-in + pan-down tightening onto the confirmation line, easing to a micro-drift end → `coordinate-target-zoom` / `viewport-change` + `multi-phase-camera` (drift).
- Everything else — swaps, cascades, check-offs, scrolls — happens on a locked frame (any "scroll" is the content translating inside its window, not the camera).

**doctrine note (idle-motion ban)**: the working-state motifs (spinner rotation, pulsing dots, pulsing "Thinking") brush against motion-doctrine's idle-motion ban — here they are DIEGETIC: the pulse _performs_ "the machine is working" and is the narrative content of Scene 2, not decorative breathing. Keep every loop finite, timeline-driven, and seek-safe (`sine-wave-loop` finite repeats, `svg-icon-enrichment` rotation), and kill it at the exact frame the state resolves — the corpus does this explicitly (the loading dots vanish the instant the payload card expands; the spinner swaps out with the loader lockup).


<!-- ===== FILE: hyperframes/hyperframes-animation/blueprints/camera-journey.md ===== -->

# camera-journey — Camera Journey

**intent**: The real viewport camera is the STORYTELLER — a multi-leg journey (dive in → a mid-journey beat fires → travel to the consequence / reposition → landing push, at rest) across ONE continuous world, where the travel itself carries the narrative. Two folded sub-shapes: **(A) action roundtrip** — the camera dives into a UI panel, a cursor/typed action fires, and the camera swoops/pans to another region where the consequence renders as element motion; **(B) cursorless flight** — pure cinematic 3D flight (motion blur, depth-of-field, tilt-to-flatten rotations) over static or self-animating content, no cursor anywhere.

**boundary**: This is NOT `cursor-ui-demo` — there the camera _chases_ the cursor (a servo following the actor); here the camera IS the actor, moving on its own narrative motivation, and in sub-shape A the cursor acts only at the leg hinge (in B it never appears). This is NOT `device-surface-showcase` — there one DEVICE/surface is hero and the camera merely presents it; here no single surface is hero — the journey traverses multiple regions/panels/depth planes and the traversal is the story. This is NOT `spatial-pan-stations` — there pre-placed stations on a flat canvas are visited by repeated pans of the same type; here the legs are heterogeneous (push-in, swoop, pull-back-rotate, whip, dive) and each leg is _motivated_ (by a fired action, or by the reveal it lands on).

**roles served**

- Benefits (from `camera-swoop-panel-action-roundtrip`): when the benefit IS a cause→effect round trip — "do this small thing here, get this big thing there" (comment → chart morphs; agent finding → verified commit; chat message → receipt + ledger). The camera physically connects the action to its payoff, so the viewer _travels_ the value chain instead of being told it.
- Key_Feature (from `cursorless-camera-flight`): when the feature should feel cinematic and inevitable — a payout form or a generated content-plan calendar explored by a flying camera (dives, whip sweeps, tilt-to-flatten, violent final push onto the CTA/hero card), the content acting by itself (a dropdown self-selects; keyword cards simply exist in depth) with no hand on the wheel.

**duration**: 5.6–11.1s (sub-shape A 5.6–9.0s: 001 5.6s · 066 8.6s · 004 9.0s; sub-shape B 6.3–11.1s: Outrank 6.3s · 094 11.1s)

**shot structure** (one oversized `[world]` — a `[UI canvas: design tool / GitHub + agent panels / phone + desktop ledger]` (A) or a `[3D-laid-out space: floating form card / calendar grid with standing keyword cards]` (B) — wrapped by a single virtual camera; content animates as elements _inside_ the world while the camera travels; every leg is a sequential tween on the same camera state)

- **Scene 0 (optional, 0.0–~1.8s) — static prologue.** Camera locked on a `[prologue beat: static promo card with a floating 3D product card / typed headline with an accent word / wide establishing shot of the app]`. A typewriter line may finish (`[headline]` types on, accent word in `[accent color]`). The prologue BREAKS by a hard cut or by the headline shrinking and slipping away as the first dive begins — the stillness exists to make the journey's launch land.

- **Scene 1 (~0.5–2.0s) — LEG 1: dive in.** The camera pushes in FAST and TIGHT onto `[the focal element]`:
  - _Sub-shape A_: a flat whole-viewport push onto `[an actionable element: comment box / agent panel / chat bubble]` where `[typed text]` finishes typing or `[response text]` streams in. The header/context leaves the frame — commitment, not a polite zoom.
  - _Sub-shape B_: the push lands at an ANGLE — a tilted 3D close-up of `[the form region / the calendar grid]`, foreground elements motion-blurred during the travel, neighbors soft under depth-of-field. A huge `[foreground prop: date number / field label]` may dominate the frame, blurred by speed.

- **Scene 2 (~1.5–6.0s) — LEG 2: the mid-journey beat (the hinge).** The camera holds, drifts, or pulls slowly while the content ACTS:
  - _Sub-shape A — the action fires_: a `[cursor]` clicks `[Send / Create PR]` (or a `[message]` sends implicitly) and the acted element CLEARS/vanishes. Optional theater before the click: a `[status spinner]` cycles `[status words]`, `[to-do items]` strike through, `[response text]` streams. The click is the hinge that _motivates_ the next leg.
  - _Sub-shape B — the content self-acts_: a `[dropdown]` expands by itself (pushing `[the field below]` down), shows a `[row hover highlight]` with no cursor, and collapses with the new value selected; OR the flight decelerates INTO FOCUS on `[one card]` — its `[metrics]` sharp, neighboring cards blurred.

- **Scene 3 (~4.0–8.0s) — LEG 3: travel to the consequence / reposition.**
  - _Sub-shape A_: the camera pulls back / swoops / pans to `[region B]` while the CONSEQUENCE builds as element motion — `[bars shrink into the baseline while a node-dotted line draws left→right / a verified commit row slides into the timeline + a reaction pill pops / a receipt card expands row-by-row from a skeleton]`. An optional SECOND leg extends the trip: `[pan up-right to a toolbar → a dropdown cascades open / match cut into an extreme close-up → a fast decelerating zoom-out reveals a ledger table]`.
  - _Sub-shape B_: a repositioning move — a slow pull-back that ROTATES the world flat and centered (3D → straight-on 2D), or a heavily motion-blurred WHIP SWEEP that resolves into a flat lateral pan across `[a month calendar / the full card]`. On the flat hold, quiet element beats may play: a thin `[focus outline]` fades in around one `[field]` and sweeps down to the next; the card keeps a near-imperceptible tilt/scale drift so the hold never dies.

- **Scene 4 (final ~1–2s) — LEG 4: landing.** The journey resolves on the payoff:
  - _Sub-shape A_: the camera comes to REST; the `[cursor]` hovers or drifts toward `[the payoff: an open Export menu item / the commit link / the View-transaction button]`; ends still, on the changed state — the world is visibly different from where the trip began.
  - _Sub-shape B_: a sudden VIOLENT push-in/dive (motion-blurred) onto `[the CTA button scaled huge in frame / the hero keyword card]`, ending holding tight — or holding MID-DIVE (the last frames are still traveling; the flat overview is explicitly not the final image).

**motion vocabulary**: whole-viewport camera push-in (fast/tight and slow/subtle); camera pull-back reframe; camera pan up/right/down; dive/swoop between stacked panels; fast decelerating zoom-out to rest; sudden violent push-in onto a button scaled huge; continuous 3D flight through a card grid; dive into an angled 3D close-up; slow pull-back that rotates/flattens the world to straight-on; heavily motion-blurred whip sweep; motion blur on camera travel; depth-of-field with blurred neighbors; decelerate-into-focus; hard cut / match cut into extreme close-up; near-imperceptible tilt/scale drift on holds; typed text finishing in an input; typewriter headline; headline shrinks and slips away as the camera dives; streaming AI response text; status-word spinner cycling labels; to-do strikethrough draw; cursor click; clicked element clears/vanishes; dropdown cascades open / self-expands and collapses with a row hover highlight (displacing the field below); bar-to-line chart morph (bars shrink into the baseline while a node-dotted line draws left→right, labels persist); commit row slide-in on a timeline; reaction pill appears; skeleton→content card build; receipt/label rows expand row-by-row; thin focus outline fades in and sweeps between fields; camera drift toward a button; 3D card subtle float; cursor hover at rest.

**rule mapping**

- the multi-leg camera itself — sequential push / pull-back / pan / dive phases on one wrapper, plus the micro-drift that keeps holds alive → `multi-phase-camera` (phase sequencing + drift) over `viewport-change` (the base virtual-camera primitive: single `.world` wrapper, one `cam {scale,x,y}` state — one source of truth for every leg)
- diving TIGHT onto an off-center element (comment box, chat bubble, Send button, one keyword card) → `coordinate-target-zoom` (scale + counter-translate; measure the target, don't hand-derive — a journey amplifies centering error on every leg)
- fast decelerating zoom-out from an extreme close-up to rest (066's ledger reveal) → `coordinate-target-zoom` zoom-out variation / `multi-phase-camera` (pull phase, hard `power4.out`)
- motion blur on camera travel (dive, whip sweep, violent final push) → `motion-blur-streak` (Camera-travel carve-out — the blur envelope rides the `.world` wrapper during a leg: the world never leaves frame, the blur peaks at peak velocity and resolves sharp at each landing)
- depth-of-field on neighbors while one card is in focus; decelerate-into-focus → `depth-of-field-blur` (focal pull + blur-the-cluster-while-pushing-in are explicitly in scope; run the DoF tween at the same position as the camera leg)
- the 3D flight itself (sub-shape B's core) — a perspective camera traveling with `rotateX/rotateY/translateZ` through a 3D-laid-out world: the dive into an angled calendar grid, the tilt-to-flatten pull-back (angled 3D → straight-on 2D), the continuous flight between standing cards → `3d-camera-flight` (perspective wrapper + preserve-3d; the 2D camera rules keep owning any flat legs)
- whip sweep → composition: `nudge-curve` (burst-dominant tuning of the slow-fast-slow slide, applied to the world) + `motion-blur-streak` (camera-travel carve-out) on the same window
- typed text finishing in an input; typewriter headline; streaming AI response text; status spinner cycling `[status words]`; skeleton→content state swap → `discrete-text-sequence` (+ `gsap-effects` typewriter; `context-sensitive-cursor` for the input caret)
- which content appears per leg / receipt rows and findings arriving on script windows → `dynamic-content-sequencing`
- cursor click on `[Send / Create PR]` (sub-shape A's hinge) → `cursor-click-ripple` + `press-release-spring` (or `physics-press-reaction` for a weightier press)
- clicked element clears/vanishes; panel state A → B on the return leg → `scale-swap-transition` / `card-morph-anchor`
- to-do strikethrough draw; row hover highlight → `css-marker-patterns` (strike-through) · `asr-keyword-glow` (accent glow on the hovered/selected row)
- bar-to-line chart morph → composite, decomposes cleanly: `stat-bars-and-fills` (bars `scaleY` → baseline) + `svg-path-draw` (node-dotted line draws left→right) at the same timeline position — no single rule names the coordinated chart-type morph, but no new rule needed
- commit row slide-in; reaction pill appears; receipt rows expand row-by-row → `spring-pop-entrance` (single arrivals) / `waterfall-entry` (the row-by-row cascade)
- dropdown self-expands, displacing the field below (094) → `anchored-layout-expand` (the masked edge-anchored expansion of the dropdown body — never tween `height`) + `reactive-displacement` (the expansion tween drives the sibling's displacement)
- focus-ring travel between fields (094: a thin outline fades in on `From`, then sweeps down onto `Amount`) → `ai-tracking-box` restyled as a plain outline (offsets baked at setup; size morphed via scale, never width/height)
- 3D card subtle float; near-imperceptible tilt/scale drift on holds → `sine-wave-loop` (+ `multi-phase-camera`'s drift for the camera-side micro-motion; the _tilt_ component of the drift belongs to `3d-camera-flight`)
- camera drift toward a button; slow subtle zoom-ins riding a hold → `multi-phase-camera` (steady-push mode, tiny spread)

**camera grammar** (the defining layer — this blueprint IS its camera): every leg is a tween on ONE camera state (`viewport-change`'s single `.world` wrapper / `cam` object), sequenced by `multi-phase-camera`, aimed by `coordinate-target-zoom`. Legs must be _motivated_: sub-shape A moves because an action fired (click → swoop to the consequence); sub-shape B moves because the next reveal demands it (dive → focus → reposition → final dive). Vary the leg verbs — a journey of four identical pushes reads as a slideshow. Ease law: hard `out`-family on dives and landings (`power4.out` — violent arrival, sharp settle), `power2.inOut` on repositioning legs; spring/back easing on a camera feels wrong (per `multi-phase-camera`). Sub-shape B layers `3d-camera-flight`'s perspective wrapper under the same single-state discipline.

**Seek-safety (non-negotiable for this much camera):** the entire journey — every leg, every blur envelope, every DoF pull — lives on the ONE paused GSAP timeline, so any frame seek reproduces the exact mid-leg camera pose. One camera state object, transform composed in a single writer (`applyCamera()`), no CSS `transition` anywhere near the wrapper, blur via proxy-tweened attributes / `--dof` vars (both seek-safe), and ending mid-dive is fine — a seek to the last frame just lands mid-tween. Per-leg targets are measured ONCE at setup (after `fonts.ready`) and baked; never `getBoundingClientRect` in `onUpdate`.

**Overflow (required for a clean `check`):** a traveling camera deliberately moves world content past the frame edges on every leg. Keep `overflow: hidden` on the scene root AND mark the moving `.world` wrapper with `data-layout-allow-overflow` — otherwise `check` reports `text_box_overflow` / `container_overflow` for every panel the journey leaves behind (see the same note on `device-surface-showcase`).


<!-- ===== FILE: hyperframes/hyperframes-animation/blueprints/comparison-split.md ===== -->

# comparison-split — Comparison Split-Cards

**intent**: Two paired items of equal weight shown side-by-side with mirrored 3D "book-open" tilts — the eye reads them as a balanced comparison, then a pill badge lands at each card's inner edge to punctuate. The motion IS the symmetry: two cards arriving from opposite wings into a held spread.

**roles served**

- Key_Feature (from `comparison-split-cards`): when two complementary features / capabilities of equal weight should be presented **simultaneously, not sequentially** — an A/B, a "X + Y together," paired concepts the viewer must weigh side-by-side. Not for >2 items (use `grid-card-assemble`) or sequential steps.

**duration**: 4–6s

**shot structure** (a `[bg]` canvas carrying two faint ambient glow blooms — `[accent A]` near 30%, `[accent B]` near 70% — so each side owns a color identity across a 50% symmetry axis; equal-width cards under one shared perspective parent)

- **Scene 1 (0.0–~0.8s) — title sets the concept.** A centered `[title line]` with an `[accent keyword]` slides DOWN into place from just above (a short smooth settle). The downward arrival is deliberate: it forms a non-conflicting T-shape against the cards, which arrive from the sides next.
- **Scene 2 (~0.4–1.9s) — the split-tilt entry (signature move).** Two equal-width feature cards arrive from opposite wings — `[left card]` from the left, `[right card]` from the right ~0.2s behind — each carrying a **mirrored 3D `rotateY` tilt** (left faces right, right faces left, opening like a book) and scaling ~0.85→1 as it lands. The entry overlaps the title's tail so the whole thing reads as ONE arrival, not two beats. Each card holds `[image / label / subtitle]`; box-shadows fall **outward** from the tilt (left shadow right, right shadow left).
- **Scene 3 (~1.9–end) — badges punctuate, then hold.** A pill `[badge]` lands at each card's **inner edge** (left then right, ~0.3s apart), overlapping its card ~15% so it reads as attached, not orbiting. This is the lone overshoot in the shot — it earns the punctuation. Settles and holds.

**motion vocabulary**: title slide-down from above; mirrored opposite-wing card entry; static book-open `rotateY` tilt (`+tilt` left, `−tilt` right); tilt-matched outward box-shadow; inner-edge badge spring-pop; gentle phase-opposed idle float (left vs right, never synchronized) registered as subtle jitter; dual side-glow ambient.

**rule mapping**

- two cards entering from opposite wings with mirrored `rotateY` tilts + tilt-matched shadow → `split-tilt-cards` (the signature; keep the two-layer split so the entry `x`/`scale` and the idle never collide on one alias)
- title slide-down settle → `gsap-effects` (translate + opacity on a long-tail `power3`)
- inner-edge pill badge pop (the one overshoot) → `spring-pop-entrance` (overshoot register — earns the punctuation)
- phase-opposed idle float on the pair → `sine-wave-loop` (low-amplitude register — subtle jitter, NOT lazy breathing; left `sin(t)`, right `sin(t+π)` so they never conveyor-belt)
- the two faint side glows behind the cards → `ambient-glow-bloom` (un-triggered soft bloom, one per accent)

**camera modifier**: camera-static by default — the symmetry is the subject and a move would break the balance.


<!-- ===== FILE: hyperframes/hyperframes-animation/blueprints/constellation-hub.md ===== -->

# constellation-hub — Constellation / Hub + Satellites

**intent**: Labeled/iconned nodes spring into a ring/cluster around a center, then the shot resolves on the core — either by pushing the camera INTO the center (depth-of-field collapsing onto it) or by holding a hub mark while the satellites ORBIT it; the "everything connects to / sits around one center" beat.

**roles served**

- Hook (from `hook-cluster-push-in`): a constellation of tool/app nodes springs into a wide ring, then a sustained camera push-in with depth-of-field resolves on the inner core — "it connects everything / one hub for all your tools."
- Social_Proof (from `social-proof-orbit-ecosystem`): the product brand mark lands as the center hub and partner logos spring onto a ring and revolve around it — "plugs into / sits at the center of your stack."
- CTA (from `cta-orbit-collapse`): the ring resolves by COLLAPSE rather than a push-in — category icons drift around an empty central CTA, a cursor click implodes the orbit toward the click point, and the product demo springs OUT of that collapse as the answer (scope → choice → consequence → product).
- Social_Proof (from `proof-logo-chain`): a persistent center logo accrues proofs — its wordmark decodes, a claim ticker swaps, the logo glides to center, then avatars cascade into orbit with drawn connectors while partner logos scroll the bottom strip; four claims read as one statement.
- Social_Proof (from `scatter-drift-finisher`): the ecosystem beat as a
  static END CARD — a two-line serif `[headline]` is the center (no hub mark, no ring), `[~20 app
icons]` pop in scattered frame-wide in a quick stagger, then keep drifting very slowly OUTWARD
  to the end. "Connects to thousands of apps" said with count and spread, not geometry.

**duration**: 5–8s (Hook 5–6s · Social_Proof 5–8s · CTA orbit-collapse ~6s · Social_Proof
scatter-drift end card ~2.5s as a closing beat)

**shot structure**

Consolidated template — nodes ring a center, then one of two finishers resolves on the core.

- Scene 1 (0.0–~1.5s): `[bg]` (dark/space field, optionally slow-drifting diffused gradient blobs). `[primary nodes]` (circles carrying `[icon]` + label) SPRING-POP in (scale 0→1, ~1.15 elastic overshoot, staggered) arranged in a wide ring/cluster around an empty or marked center `[hub]`.
- Scene 2 (~0.7–2.5s, overlapping): smaller `[secondary nodes]` (platform / partner-logo chips) pop in staggered with the same elastic spring, filling the gaps; optional thin `[accent]` connector lines / orbit ring draw from hub→nodes. Camera holds.
- Scene 3 (~2.5–Xs, the resolve): see finisher variant below; lands and HOLDS on the magnified / orbited center to the end.

- Variant — Hook (push-in finisher): from Scene 3, a continuous smooth CAMERA PUSH-IN toward the center inner cluster — inner nodes scale up and stay sharp while outer nodes are pushed toward the edges and progressively BLUR (depth-of-field), background scales up smoothly; holds magnified on the core.
- Variant — Social_Proof (orbit finisher): the center `[brand mark]` snaps in via a quick 3D rotate that decelerates and settles; a thin `[accent]` orbit ring draws around it; `[N partner badges]` spring onto the ring (staggered overshoot) and revolve CLOCKWISE while staying upright, under a continuous slow camera ZOOM-OUT (ecosystem reveal).
- Variant — Social_Proof (optional type-push-through opener, prepended before Scene 1): centered `[headline]` types/slides in with a huge transparent-fill OUTLINE copy of the same words behind it; the outline text scales up exponentially toward camera (high-speed dolly / push-through), breaches the frame, then HARD-CUTS to the hub bg of Scene 1.
- Variant — Social_Proof (scatter-drift finisher, no ring): the center is a two-line serif
  `[headline]` building in place (not a mark); `[~20 app icons]` pop in SCATTERED across the whole
  frame in a quick stagger — no ring geometry, no connectors — then sustain a very slow outward
  drift to the end. Camera fully static: no push-in, no zoom-out; the "everything around one
  center" reads from the drift vectors pointing away from the headline. Often chained as the end
  card of a preceding UI beat (the prior card dissolves into it).

**motion vocabulary**: staggered elastic spring-pop node entrances (~1.15 overshoot); slow gradient-blob drift; connector-line / orbit-ring draw-on; 3D snap-rotate-settle on the hub mark; continuous camera push-in (inner sharp, outer depth-of-field blur, bg scale-up); clockwise orbital revolve of upright badges; continuous slow camera zoom-out (ecosystem reveal); optional outline-text push-through dolly entry. Scatter-drift finisher: frame-wide scattered icon pop-in (staggered, no ring); sustained slow
outward icon drift; in-place two-line serif headline build; static-frame hold to the end.

**rule mapping** (motion verb → `rules/<id>.md`)

- staggered spring-pop node entrances → `spring-pop-entrance` (elastic overshoot) + `gsap-effects` (stagger recipe); 3D-flip-in flavor → `orbit-3d-entry`
- ring / cluster layout of nodes around a center → `avatar-cloud-network` (nodes on an elliptical ring + SVG lines to a center)
- icons on the nodes → `svg-icon-enrichment`
- connector lines hub→node → `svg-path-draw`
- orbit-ring draw-on → `svg-path-draw`
- slow gradient-blob drift → `sine-wave-loop` (idle looped drift)
- 3D snap-rotate-settle on hub mark → `orbit-3d-entry` (3D-flip entry); technique CSS-3D
- clockwise orbital revolve of upright badges → `orbit-3d-entry` (continuous elliptical orbit); technique MotionPath
- camera push-in toward center → `multi-phase-camera` (PUSH-in) + `coordinate-target-zoom` (target the core)
- background scale-up during push-in → `multi-phase-camera`
- continuous slow zoom-out (ecosystem reveal) → `multi-phase-camera` (pull-back) / `coordinate-target-zoom`
- outline-text push-through dolly opener (Social_Proof) → `3d-text-depth-layers` (outline copy behind) + `multi-phase-camera` (push-through)
- depth-of-field blur on outer nodes during push-in → `depth-of-field-blur` (progressive DOF/focus-falloff blur on the off-center outer nodes while the inner core stays sharp)
- frame-wide scattered icon pop-in (no ring) → `spring-pop-entrance` (staggered group) +
  `gsap-effects` (stagger recipe); positions pre-baked scattered — NOT `avatar-cloud-network`'s
  elliptical ring
- sustained slow outward icon drift → `center-outward-expansion` (outward vectors, slow sustained
  register — drift targets sit slightly past the pop-in positions)
- in-place serif headline build → `gsap-effects` (staggered line/word reveal)

**camera modifier**: push-in-with-DOF (Hook) — `multi-phase-camera` PUSH-in targeted via `coordinate-target-zoom` onto the core; the focus-falloff blur half of it is backed by `depth-of-field-blur`. Orbit finisher (Social_Proof) — slow continuous zoom-out via `multi-phase-camera` (pull-back) while satellites revolve. Scatter-drift finisher (Social_Proof end card) — none: the frame never moves; the outward drift
is element-level.


<!-- ===== FILE: hyperframes/hyperframes-animation/blueprints/cta-morph-press.md ===== -->

# cta-morph-press — CTA Morph & Press

**intent**: A resting brand mark condenses at the same screen center into a smaller, brighter CTA, then a cursor arrives from off-stage and lands a human-aimed click on it. The viewer's eye is walked from "this is who we are" to "and this is what you do." The morph and the click are the two headline beats.

**roles served**

- CTA (from `cta-morph-press`): when the close moves from brand identity to a single user action, two elements share the same center sequentially (a morph, not a cut), and the payoff is a simulated click with physical feedback. Reach for it for a focused "click here" sign-off — no spatial set, no multi-step UI (that's `cursor-ui-demo`).
- Hook (ROLE-WIDENED, from `widget-morph-on-blank-field`): the same
  machinery run as an OPENER — a lone `[widget]` (pill / chip lockup) on a flat field transforms
  in place, performs its payload, then vanishes to a plain frame that a typed `[title]` resolves.
  The click, when present, ignites the morph rather than closing it; there may be no cursor at
  all. Reach for it when the product hook IS one widget doing one thing — still no spatial set,
  no multi-step UI (that's `cursor-ui-demo`). Mint-reconsideration trigger: if future mining
  brings 2+ more widget-morph openers with the vanish → typed-title resolve, promote this variant
  to its own blueprint (the beat order is fully inverted by then).

**duration**: 4–6s (Hook widget-morph opener 5–7.5s)

**shot structure** (a `[bg]` canvas; hero and CTA are flex-centered siblings sharing one `transform-origin`)

- **Scene 1 (0.0–~1.4s) — presence.** The `[hero mark / brand lockup]` holds dead-center, alive but resting — only a faint rotational breath on the mark; any title text under it stays rock-stable. Camera static.
- **Scene 2 (~1.4–2.4s) — the morph (signature move).** The hero CONDENSES at the same screen center into a smaller, brighter `[CTA]` (button / card): the outgoing mark shrink-fades exactly as the CTA scales up in its place. Because they share one `transform-origin`, the eye reads it as one element transforming, not a swap.
- **Scene 3 (~2.4–3.4s) — approach.** A `[cursor]` arrives from off-stage on a **decelerating** path (it "arrives," it does not pass through) and lands a few px **off** the CTA's geometric center, so the aim reads human, not scripted.
- **Scene 4 (~3.4–end) — press.** The cursor lands a physical CLICK — cursor and CTA compress together in lockstep, then release with feedback (an optional ripple / glow bloom). Holds on the clicked state.
- **Variant — Hook (widget-morph opener)** (from `widget-morph-on-blank-field`;
  reorders the beats — press first, morph second, title last). **(1) presence**: a lone
  `[pill / chip lockup]` sits centered on a flat `[field]`; optionally the `[cursor]` glides in, a
  hover pill-background appears behind the chip, and the click lands with the same lockstep press.
  **(2) the morph**: the widget transforms IN PLACE — expands downward anchored at its top edge
  into a `[menu]`, or spring-morphs outward into a `[prompt card]` with a small overshoot settle —
  new content fades/slides into place. **(3) payload**: the transformed state performs —
  `[placeholder]` types with a blinking caret, `[user text]` types while a control flips from
  muted to its vibrant active color, or the menu snap-collapses back to the pill carrying the
  `[new value]` + a checkmark pop; the background may snap to a new color under the persistent
  foreground card. **(4) resolve**: the widget VANISHES; a plain frame closes the beat — a
  `[closing title]` types on center, or a hold on the flipped solid.

**motion vocabulary**: faint rotation-only resting breath (logo scope only); same-center morph-swap (shrink-fade ↔ scale-up sharing `transform-origin`); cursor decel-arrival from off-stage; off-center human aim; lockstep press compression; release feedback ripple / glow. Hook opener: anchored downward expand of a pill into a menu and springy snap-collapse back;
chip-to-card spring morph with overshoot settle; placeholder / user-text typewriter with blinking
caret (may cut mid-word); control color-state flip muted → vibrant; background color snap under a
persistent foreground card; checkmark pop; widget vanish to blank frame; typed closing title.

**rule mapping**

- hero → CTA condense at one center → `scale-swap-transition` (shared `transform-origin: 50% 50%` is what sells the morph; CTA `position: absolute` so it doesn't shove the hero during the brief overlap)
- resting-hero aliveness (rotation only, scoped to the mark so the Phase-2 scale doesn't fight it) → `sine-wave-loop` (low-amplitude rotation register — subtle jitter, not a scale breath)
- cursor press + release in lockstep (single-target-array so both compress together) → `physics-press-reaction` (PRESS_DOWN + RELEASE portion)
- cursor approach (decel from off-stage, off-center landing, hard-cut opacity in) → `gsap-effects` (translate on `power2.out`)
- click ripple / release glow → `cursor-click-ripple` (attack-decay ring) and/or `ambient-glow-bloom` (release bloom)
- (Hook) chip → prompt-card spring morph at one center → `scale-swap-transition` (the base morph
  contract, run in the expand direction) + `card-morph-anchor` (corner-radius / surface ride-along)
- (Hook) anchored-edge expand / snap-collapse (pill ↔ menu, top edge pinned) →
  `anchored-layout-expand` (edge-anchored directional container growth — origin-pinned expansion
  with counter-scaled children; `card-morph-anchor` stays for uniform-scale morphs only)
- (Hook) placeholder + user typing, blinking caret, mid-word cut → `gsap-effects` (typewriter) +
  `context-sensitive-cursor` (blink) + `discrete-text-sequence` (mid-word cut states)
- (Hook) control color flip muted → vibrant → `press-release-spring` (color-transition variation)
- (Hook) checkmark pop / card-arrival overshoot → `spring-pop-entrance`
- (Hook) hover pill-background + igniting click → the base's `physics-press-reaction` +
  `cursor-click-ripple` mappings apply unchanged

**camera modifier**: camera-static — the morph and click happen in element space; a camera move would compete with the click as the climax. The Hook opener keeps the same contract — even the background color flip is an element-level
snap, not a camera event.


<!-- ===== FILE: hyperframes/hyperframes-animation/blueprints/cursor-ui-demo.md ===== -->

# cursor-ui-demo — Cursor-Driven UI Demo

**intent**: A visible custom cursor drives a real (reconstructed) app UI through clicks / hovers / drags so the screen changes state shot-to-shot, while the camera chases each interaction — the product surface is the subject and the cursor is the actor.

**roles served**

- Product_Intro (from `product-intro-cursor-ui-demo`): first look at the product surface — the cursor sweeps/hovers to \_introduce\* the app and reveal what it is, landing on a hovered hero element or freshly-popped result. Light, exploratory; backdrop steps colors as it goes.
- Key_Feature (from `key-feature-cursor-ui-demo`): one specific multi-step workflow demonstrated \_end-to-end\* (edit / configure / select across 2–4 discrete beats), each beat a real edit the UI responds to live, landing locked on the primary action button or the produced result.
- Key_Feature (from `workflow-approve-press`): an agency / confirmation workflow framed by a cockpit of 3D-tilted flanks — a step list ticks pending → active → complete (a snap state machine, CSS responding to `[data-state]`), and a flank button takes the PRESS as the payoff (its color flips to success, a checkmark stamps). The click is the climax, not a passing gesture.
- Key_Feature (from `cursor-app-state-tour`): the static-stage STATE TOUR — the cursor drives a reconstructed app through 2–4 discrete feature states on a LOCKED frame; every scene change is a click-triggered element swap/scale (modal springs from center, side panel slides in from the right edge, settings hard-swap, table populates, node-graph builds), never a real camera move; optional `[title card]` Scene 0 in front and a `[brand end beat]` behind.
- Key_Feature (from `drag-field-onto-document`): the DRAG-DROP journey — one continuous zoom-breathing shot of a document workspace: the cursor drags a ghosted `[field chip]` from an inputs sidebar onto the page, drop-snaps it into a placed field, a modal/typing beat completes it, and the placed element is adjusted in close-up before the cursor heads to the `[Finish/CTA]`.
- Product_Intro: the low-event BROWSE — the cursor roams ONE clean page state and the filter controls answer with slight hover updates; no typed input, no title beats, and the shot may end mid-roam.
- Product_Intro (from `hover-inspect-run`): the HOVER-INSPECT run — a click SPAWNS a labeled `[toolbar]`, the camera zooms out from a tight crop to the full page, then the cursor sweeps `[page elements]` while a floating `[inspector panel]` TRACKS the cursor, outline-highlighting and content-snapping per hovered element. (The slice's three-beat dark title prelude, scenes 1–3, belongs to `titlecard-reveal`, not here.)
- Hook: the ambient MULTI-CURSOR canvas — several labeled `[teammate cursors]` work a design canvas simultaneously (grab-drag-drop of components between mockups, recolor/identity swaps on drop) while the canvas group translate-PANS within a static frame and a `[headline]` builds word-group by word-group over the demo; the live workshop itself is the hook. One continuous beat, no cuts, no camera.
- Benefits (from `ui-demo-text-interlude-ui-demo`): the demo|text|demo SANDWICH — two static-stage demo beats of this blueprint bridge through a full-screen kinetic/title interlude and back (cursor acts, UI answers, all "zoom" element scale); the interlude beat is `kinetic-type-beats` material, and the sandwich itself is sequencing above the single-shot unit.

**duration**: 4.0–12.9s (Key_Feature 4.0–12.9s — the mined state tours run long, 10.4–12.9s, and the drag-drop journeys 9.8–10.6s, against the original 4.0–7.3s set; Product_Intro 4.5–9.3s — the low-event browse sets the 4.5s floor; Hook ~6.5s; the Benefits demo|text|demo sandwich totals 11.6–12.8s with each demo half ~4–5s)

**shot structure** (a `[product UI surface]` — fixed app window, dashboard/editor, parallax `[content card]` stack, or a `[container object/icon]` — centered over `[bg color/gradient]`, shown `[flat]` or `[3D-isometric]`; a custom `[brand-colored cursor with icon]` is the protagonist and the camera servos to whatever it touches; UI responds _live_ and in sync with each cursor action. Two role-tuned tempos fold in — Product_Intro **sweeps to introduce**, Key_Feature **performs a workflow** — and the camera spans a spectrum: the full CHASE, one continuous zoom-breathe, or a fully LOCKED static stage where the UI itself does all the moving.)

- **Scene 1 (0.0–~Xs) — surface establishes + first touch.** The `[product UI surface]` arrives centered over `[bg color/gradient]` — either it is simply present (fixed window / dashboard / editor), a 3D-parallax stack of `[content cards]`, or a `[container object/icon]` that FLIES IN with a 3D tumble and settles. The custom `[cursor]` enters. The cursor performs the FIRST action on `[cursor target 1]` and the UI responds live in the same beat. Camera holds or begins a slow push-in toward the acted-on region.
  - _Variant — Product_Intro_: low-commitment first touch — cursor HOVERS/sweeps a control or SWEEP-HIGHLIGHTS a field to `[accent color]`, OR the `[container]` fans open. An optional label/title fades/morphs onto the surface. The point is to _show the surface exists_ and is touchable.
  - _Variant — Key_Feature_: a concrete edit — cursor DRAGS a scrollbar / TYPES into a field / DRAGS a handle, and the UI responds materially (`[scroll]` / value climbs / region resizes). If the surface opened in `[3D-isometric]`, it may snap perspective-FLAT here to read the workflow.
  - _Variant — Key_Feature (static-stage tour)_: an optional Scene 0 — `[title card / kinetic brand word]` on a flat field — hard-cuts or window-SCALES-UP into the surface; the `[app UI]` is fully present from the first frame and the cursor enters and glides to the first control. The camera is LOCKED from the start and stays locked.
  - _Variant — Hook (ambient multi-cursor)_: no single protagonist — several labeled `[teammate cursors]` are already at work across `[N mockups]` on a design canvas; the canvas group translate-PANS within the static frame while a `[headline]` builds word-group by word-group over the top. One continuous beat, no cuts.

- **Scene 2 (~Xs–~Ys) — camera chases to the next interaction (the engine).** The camera MOVES to the next target — push-in + pan / whip-pan / pan-down to `[cursor target k]` — and the cursor performs action k as the UI updates live. Each beat is a discrete interaction connected by a fast camera move; the surface's inner content SWAPS per interaction.
  - _Variant — Product_Intro_: navigation is exploratory — a slow camera pan + depth-of-field FOCUS-PULL across a parallax `[content card]` stack, or the `[container]` fanning into `[N option/content cards]` that SPRING to position. As content swaps, the supporting backdrop STEPS its color (`[bg step 1]` → step 2 → …). Typically one or two such moves.
  - _Variant — Key_Feature_: repeat for `[2–4 beats total]`, each a distinct operation the UI answers — counter COUNTS UP, `[pill/swatch]` SELECTS, a modal SLIDES UP and TYPES — connected by whip-pans / progressive zoom. The workflow visibly advances toward a result.
  - _Variant — Key_Feature (static-stage tour)_: the camera never moves — every beat is a click-triggered ELEMENT response: a modal SPRINGS/scales up from center, a `[side detail panel]` SLIDES in from the right edge (a second panel may slide over the first), hamburger→sidebar slide-open, a settings panel HARD-swaps its content, a dropdown fills, a `[table]` populates row-by-row, a formula types into a cell and the range populates on enter, a type-to-filter list live-collapses, a `[block]` pops into the canvas, a node-graph BUILDS (cards + connecting lines radiate from center), a hover drops a `[popover]` below a tag. Any "zoom" is element scale of the UI only.
  - _Variant — Key_Feature (drag-drop)_: the cursor GRABS a `[field chip]` from an `[inputs sidebar]`, drags a semi-transparent GHOST across the page, and drops it — it SNAPS into a placed field with bounding box + corner handles; a completion beat follows (a `[modal]` springs up over the dimmed document, a name types letter-by-letter while a live `[cursive preview]` builds per keystroke, confirm click). The whole clip rides one continuous zoom-BREATHING arc (slow zoom-out / gentle zoom-in / final zoom-out) instead of discrete camera beats.
  - _Variant — Product_Intro (hover-inspect)_: the cursor's first click SPAWNS a labeled `[toolbar]`, the camera zooms OUT from a tight crop to the full page, then the cursor sweeps `[page elements]` — each hovered element gets an outline and a floating `[inspector panel]` TRACKS the cursor, its content snapping per element.

- **Scene 3 (~Ys–end) — payoff state, camera settles, HOLD.** The cursor lands on its final target and the screen reaches the payoff state; the camera comes to rest (static) and holds.
  - _Variant — Product_Intro_: the cursor HOVERS the hero element — a `[content card]` SCALES UP on hover, a node gets an `[Available]`-style pill, or a `[result card]` POPS/springs in — the "here's the product" payoff. Settles static, holds.
  - _Variant — Key_Feature_: locked close-up on the OUTCOME — cursor lands on the `[primary action button: Export / Save / Reimburse]` and a `[hover backdrop / highlight]` SPRING-pops in (the climax is the action button / produced result). Holds.
  - _Variant — Key_Feature (static-stage tour)_: optional detachable end beat — `[brand text beat / icon-ring lockup / end stat card]` — or the cursor simply comes to REST on the next target and holds (006_claudeai ends with the cursor on a panel's close X, the panel never closing).
  - _Variant — Key_Feature (drag-drop)_: close-up on the placed element ADJUSTED — a corner-handle drag proportionally resizes it — then the cursor sweeps toward the `[Finish / CTA]` as the clip ends.
  - _Variant — browse / hover-inspect_: no payoff lock at all — the shot ends MID-demo, cursor still roaming (browse and hover-inspect modes).

**motion vocabulary**: cursor-driven click / hover / sweep-highlight / drag / type; per-interaction live UI response (scroll, value climb, region resize, content swap); camera push-in + pan / whip-pan / pan-down servoing to each target; coordinate zoom onto the acted region; press-and-ripple on a clicked control; button press-compress; screen-state swap shot-to-shot; card fan-out to corners (spring); 3D container fly-in & tumble-settle; perspective-flatten (3D→2D snap); paginated/stepped backdrop color advance; depth-of-field focus-pull across a parallax card stack; counter count-up; pill/swatch select; modal slide-up + typing; label/title morph between states; UI-keyword highlight glow; terminal hover-scale or result-card pop-in; spring hover-backdrop on the final action button; hard panel swap (no easing); side detail panel slide-in from the right edge (second panel over the first); hamburger→sidebar slide-open; hover popover drop below a tag; element-scale fake zoom (UI window scales in/out on click, camera locked); table populates row-by-row; formula typed into a cell + instant cell-range populate on enter; fill-handle drag auto-fill down rows; type-to-filter list live-collapse; dropdown fill on click; block/element pop-in to canvas; node-graph build (cards + connecting lines radiate from center); character-by-character auto-typing with blinking caret; window scale-up with settle; ghost-chip drag (grip dots + icon) across the page; drop-snap into a placed field with bounding box + corner handles + trash icon; modal spring-up over a dimming document; letter-by-letter typing with a live cursive preview building per keystroke; corner-handle drag with proportional resize; continuous zoom-breathing single shot (zoom-out / zoom-in / zoom-out arcs); cursor sweep toward the CTA at clip end; multiple labeled collaborative cursors moving independently; cursor grab-drag-drop of components between mockups; element recolor/identity swap on drop; canvas-group translate-pan within a static frame; headline building word-group by word-group over the demo; hover-triggered micro content/sidebar update; click spawns a labeled toolbar; floating inspector panel tracking the cursor with per-element content snap; per-element hover outline highlight; motion-blur window fly-in; tight-crop open then zoom-out to full page; brand icon-ring end beat; 3D end-card float on the hold.

**rule mapping**

- viewport follows the cursor / camera servos to whatever it touches (primary) → `camera-cursor-tracking`
- cursor moves to a target, presses, emits a ripple (the click itself — primary interaction primitive) → `cursor-click-ripple`
- screen-state swap shot-to-shot (surface inner content changes between beats) → `scale-swap-transition`
- camera push-in + pan / whip-pan / pan-down to the next target → `viewport-change` (pan/zoom across the UI)
- sequencing the chase into discrete interaction beats → `multi-phase-camera`
- zoom onto the specific acted-on UI region → `coordinate-target-zoom`
- cursor icon/state changing with context (e.g. pointer↔grab over a draggable handle) → `context-sensitive-cursor`
- which content appears per beat / step-by-step UI state progression / per-interaction swaps → `dynamic-content-sequencing`
- sweep-highlight a field, highlight a UI keyword to `[accent color]` → `asr-keyword-glow` (keyword glow on the touched element)
- clicked button compresses on press, springs back on release → `press-release-spring`
- cursor + button compress together on a heavier press → `physics-press-reaction`
- panel/card morphs between two states (e.g. card → expanded card, surface state A → B) → `card-morph-anchor`
- terminal hover-scale, `[result card]` pop-in, spring hover-backdrop on the final action button → `spring-pop-entrance`
- card fan-out to corners / option cards springing to position → `split-tilt-cards` (fan/spread into tilted positions) + `spring-pop-entrance` (the spring settle)
- 3D-parallax content-card stack as the surface; UI shown 3D-isometric → `3d-page-scroll` (UI as a tilted scrolling/parallax card)
- node gets an `[Available]`-style pill / tracked badge appears on an element → `ai-tracking-box`
- counter / value count-up as the UI responds → `counting-dynamic-scale`
- a result bar / number FILLS as the workflow's outcome → `stat-bars-and-fills`
- a live `[video]` screen-capture clip used as the surface → technique: video compositing
- perspective-flatten (3D-isometric → flat 2D snap) and the 3D-isometric tilt itself → technique: CSS-3D (no dedicated rule; the tilt/flatten transform is a CSS-3D primitive)
- camera settles static on the payoff and HOLDS → (settle phase of `spring-pop-entrance` on the payoff element; the static hold itself needs no rule)
- 3D container/object fly-in & tumble-settle → `depth-scatter-assemble` (free-tumbling 3D object/container entrance that flies in and tumble-settles; `orbit-3d-entry` only orbits a flat element into place)
- depth-of-field focus-pull across the parallax card stack → `depth-of-field-blur` (rack-focus / DoF blur transition between near and far cards; `3d-page-scroll` supplies the tilted parallax stack and `viewport-change` the pan)
- paginated/stepped backdrop color advance synced to interactions (`[bg step 1]`→step 2→…) → `discrete-text-sequence` (discrete state stepping, here applied to a background-color state rather than text)
- modal slide-up + in-modal typing as one combined beat → `card-morph-anchor` / `scale-swap-transition` (the panel slide-in) + `discrete-text-sequence` (the in-modal typed text)
- element-scale fake zoom — the UI window scales, camera locked (static-stage tour) → `coordinate-target-zoom` (applied to the surface wrapper rather than the world)
- side detail panel slide-in from the right edge / hamburger→sidebar slide-open / hover popover drop → `card-morph-anchor` / `scale-swap-transition` (the panel arrival) + `dynamic-content-sequencing` (which content each panel shows per beat)
- hard panel swap / in-panel content snapping through states / hover-triggered micro update / type-to-filter live-collapse / element identity swap on drop → `dynamic-content-sequencing`
- table populates row-by-row / fill-handle auto-fill cascading down rows / log rows cascade in → `waterfall-entry`
- formula typed into a cell / character-by-character auto-typing with blinking caret / letter-by-letter typed name → `discrete-text-sequence` + `context-sensitive-cursor` (the caret)
- node-graph build (cards + connecting lines radiate from center) → `center-outward-expansion` (the cards) + `svg-path-draw` (the connecting lines draw)
- click spawns a labeled toolbar / dropdown fills on click / drop-snap settle of the placed field / window scale-up with settle → `spring-pop-entrance`
- modal spring-up over a dimming document → `spring-pop-entrance` (the modal) + `depth-of-field-blur` (the document dim/blur beneath)
- ghost-chip drag-and-drop / cursor grab-drag of components between mockups / fill-handle drag / corner-handle resize drag → `cursor-drag` (`cursor-click-ripple` covers move+click only)
- floating inspector panel TRACKS the cursor, content snapping per element → `ai-tracking-box` (the per-frame follow mechanics, restyled as an inspector panel) + `dynamic-content-sequencing` (the per-element content)
- live cursive preview building per typed keystroke → `svg-path-draw` (progressive stroke reveal keyed to typing progress)
- continuous zoom-breathing single shot (drag-drop variant) → `multi-phase-camera` (pull-back / focus / push phases + micro-drift)
- motion-blur window fly-in / tight-crop open then zoom-out to full page → `motion-blur-streak` (the fly-in) + `viewport-change` (the zoom-out)
- multiple labeled collaborative cursors moving independently → `multi-cursor-choreography` (N labeled independent cursor actors; the single-actor cursor rules assume one)
- canvas-group translate-pan within a static frame → `viewport-change` (the `.world` translate realizes the pan; semantically the camera stays locked)
- headline builds word-group by word-group over the demo → `waterfall-entry`
- brand icon-ring end beat → `svg-path-draw` (the ring) + `spring-pop-entrance` (the lockup)
- 3D end-card float on the hold → `sine-wave-loop` — CAUTION: motion-doctrine bans idle wobble; prefer a settle-and-hold

**camera modifier**: The defining motion is the camera CHASE — the viewport follows the cursor from target to target via `camera-cursor-tracking` (primary), realized as concrete push-in + pan / whip-pan / pan-down moves under `viewport-change`, sequenced into discrete interaction beats by `multi-phase-camera`, with each beat's destination targeted via `coordinate-target-zoom` (zoom to the acted-on region). Product_Intro biases toward a slow, exploratory pan + focus-pull that sweeps the surface; Key_Feature biases toward snappier whip-pans / progressive zoom that march through the workflow and lock static on the action button. This camera-servo-to-cursor is what separates the blueprint from hands-off camera scrolls (dataviz-scroll-reveal) and static device/window tours. The golden set widens this into a spectrum. At one pole the **static-stage state tour** (now the largest member set) LOCKS the camera for the entire clip and lets the UI itself do all the moving — panel slide-ins, element-scale fake zooms, content snaps — with the cursor alone carrying the eye. The **drag-drop** variant replaces discrete chase beats with ONE continuous zoom-breathing arc under `multi-phase-camera`. The **hover-inspect** variant inverts the push-in: a tight-crop open zooms OUT to the full page before the cursor sweep. Pick the pole per brief — chase for workflow marches, locked stage for dense reconstructed dashboards, a single breathe for one-document journeys. With the locked pole absorbed, what separates this blueprint from `device-surface-showcase` is the CURSOR-as-actor, not the camera: a fully static tour still belongs here as long as a visible cursor drives every state change.


<!-- ===== FILE: hyperframes/hyperframes-animation/blueprints/dataviz-countup.md ===== -->

# dataviz-countup — Data-Viz / Count-Up

**intent**: Make numbers and charts the hero — a count-up ring/number, a trend chart, a tilted stat/card grid — and traverse the data instruments with a camera that pushes THROUGH them (or scrolls across them) to land on one hero metric, so the data itself carries the argument.

**roles served**

- Problem (from `problem-dataviz-pushthrough`): quantifies the pain with real-looking instruments — a count-up ring → a trend chart → a stat grid — the camera pushing THROUGH each object into the next to dramatize a worsening / large-scale problem ("X% of people struggle with…").
- Product_Intro (from `product-intro-dataviz-scroll-reveal`): a confident "look at the result / the data" open — hard-cut from a hook word into a perspective-tilted grid of data-viz cards, then a hands-off camera scroll lands one glowing hero metric while a kinetic tagline assembles word-by-word.
- Hook (from `hook-counter-burst`): a cold-open hook on ONE dramatic statistic — the frame opens dark and empty, 3–5 thematic icons puncture in clustered at center, then the headline number EXPLODES upward in size as the icons fling outward to their marks (the count-up and the spread are one beat), closed by a slow camera lean-in. Kinetic from frame 1.
- Key_Feature (from dark-stat-scrub-montage): prove the feature with its own analytics — on a black canvas, kinetic headline beats alternate with self-drawing charts and a 3D-tilted dark dashboard that a cursor SCRUBS (tracking line + live tooltips), stitched by hard cuts and one zoom punch. The one variant where a cursor touches the data.
- Social_Proof (from `gauge-beat`): a single count-up instrument — radial gauge arc-draw + rapidly ticking metric + caption — embedded as ONE BEAT inside a kinetic-typography relay; entered and exited by element-level scale/blur push-throughs on a static frame. The instrument guest-stars; the relay itself belongs to kinetic-type-beats.

**duration**: ~4–12s (Hook ~4s · Product_Intro ~6s · dark-scrub-montage ~7.3–7.75s · Problem ~11–12s · gauge-beat ~2.5s inside a ~10.8s relay)

**shot structure** Data-viz field on `[bg color]` (dark or light, soft corner glows); `[gradient A→B]` brand stroke on charts/rings; clean sans-serif white/dark text; a continuous camera move runs underneath that traverses 2–3 data instruments and resolves on a hero metric. One instrument per beat; the camera carries the cut.

- Scene 1 (0.0–Xs): the first data instrument establishes centered — a `[stat]` reads as the hero. A bold center number COUNTS UP `[start]`→`[end]` while its transform scale grows to the static final type size, with `[stat label]` below; its paired graphic (a circular progress RING sweeping to `[pct]` with a `[gradient]` stroke, or a bar/fill) animates in on the SAME ease so number + graphic land as one beat. Supporting `[avatar/object]` elements pop in with spring overshoot into a scattered glowing orbit; a `[headline]` fades up. A very slow continuous camera zoom-in runs throughout.
- Scene 2 (Xs–Ys): the camera traverses to the next instrument and that instrument animates — a `[gradient]` trend line / area chart DRAWS left→right on grid lines (Problem), or off-center cards SCROLL away as the layout glides (Product_Intro). The arriving `[stat-2]` number counts up / the chart resolves.
- Scene 3 / Scene N (…–end): the camera lands the `[hero metric card]` (big number + label + delta + rising chart) in dead-center; a soft `[accent]` glow blooms behind it; the move reaches its peak then eases to a settled, slightly wider composition with the hero centered and supporting cards flanking it. HOLD on the final frame.

- Variant — Problem (push-THROUGH, count-up → trend → grid): Scene 1 is a centered circular progress ring + count-up center number with scattered glowing `[avatar/object]` orbit. Scene 2 is a fast camera PUSH-IN straight through the center of the ring (ring, number, orbiting elements scale up and fly out of frame) into a rounded `[card]` holding `[stat-2 header]` over a `[gradient]` line chart with grid lines + translucent area fill that draws left→right; camera pushes through then settles. Scene 3: camera PANS to a second `[card]` whose number counts up, holding a grid of the `[avatar/object]` elements — a subset dim/blur while the rest receive `[accent]` circular checkmark badges that SPRING-POP; camera settles to the end. The traversal is z-depth push-through between instruments.
- Variant — Product_Intro (scroll-to-hero + word-by-word tagline): a brief opener — Scene 0 (~0.0–0.85s): a full-frame `[hero-color orb]` with a bold white `[hook phrase]` over it; static shimmer, then HARD CUT. Scene 1 cuts to a slightly perspective-TILTED grid of `[data-viz / product cards]` (charts, heatmaps, stat cards with deltas + source footers) with `[tagline word 1]` centered; the grid begins SCROLLING (e.g. toward upper-left) with its tilt held. Scene 2: the grid keeps scrolling so the `[hero metric card]` glides into dead-center as off-center cards slide away; `[tagline word 1]` translates out and `[word 2]` rises in from a frame edge. Scene 3: hero card settles centered, `[accent]` glow blooms behind it, camera PUSHES IN slightly; `[word 2]` holds near it. Scene 4: `[word 2]` slides out, the final `[tagline word]` drops in from the opposite edge above the still-glowing hero, push-in peaks. Scene 5: overlay type clears, camera eases BACK OUT to a settled wider tilted composition — hero centered with glow, supporting cards flanking. The traversal is a hands-off camera SCROLL across a tilted card plane (no cursor, no clicks) + a one-word-at-a-time kinetic headline + push-in-then-out bookend.
- Variant — Key_Feature (dark-scrub-montage: kinetic beats × instruments, cut-stitched): on black, `[kinetic word]` beats ALTERNATE with data instruments; hard cuts stitch the beats and the camera is locked per beat — the traversal is a montage, not a continuous move. Beat A: a bold `[heading]` holds while a thick `[trend line]` DRAWS itself left→right inside a dark chart band, rising to break above the band's edge; at the peak a `[accent]` dot pops and a pill tooltip springs in, its label building to `[value + delta]`. Beat B: ONE fast zoom PUNCH lands a close-up, slightly 3D-tilted dark `[analytics dashboard]` (metric cards with deltas, translucent oversized numerals floating behind); a white cursor SCRUBS a chart — a vertical tracking line follows it and `[date: value]` tooltips read out live, then a second chart ACTIVATES with a color flip and its own scrubbing tooltip — while the tilted plane drifts gently sideways; quick pull-away/fade to black. Beat C: a `[glowing wave / typed line / impact word]` beat lands the closing stat LOCKUP — `[title]` + big `[stat]` counting up + `[green delta arrow + context line]` — and holds static to the end. Kinetic words between instruments scale up violently past the frame as element-level push-through transitions (no camera).
- Variant — Social_Proof (gauge-beat inside a relay): a static-camera kinetic-type relay hosts ONE instrument beat — thin concentric `[accent]` arcs radiate from center, a thick `[accent]` progress arc draws clockwise over them, a large `[metric]` rapidly ticks up to `[big value]` with a `[caption]` below; the group slowly scales up (element-level drift), then hard-cuts out to the next text beat. Entry/exit for every beat is scale-up-from-blur in / scale-up-and-blur-past-frame out — a fake push-through with no camera anywhere. Use when social proof is one number and the surrounding beats are typography.

**motion vocabulary** count-up number with transform-scale growth on the value; circular progress-ring sweep; growth bar / progress fill; gradient trend-line + area-fill left→right draw; spring-overshoot pop-in of scattered glowing avatar/object elements; perspective-tilted card grid; directional grid scroll (cards glide in/out of center); hero-card centering; soft accent glow bloom behind the hero; slow continuous zoom-in; fast camera push-IN / push-THROUGH the center of an instrument; lateral/vertical camera pan between cards; gentle push-in that peaks then eases back out to a wider settle; selective dim/blur of a subset + spring-pop checkmark badges; full-frame hook orb → hard cut; kinetic tagline assembled word-by-word (each word drops/rises from a frame edge, prior word slides out). Dark-scrub-montage additions: self-drawing chart line that breaks above its band; peak dot + pill tooltip spring-pop; cursor chart scrub with vertical tracking line + live date/value tooltip readouts; chart activation color flip; 3D-tilted dark dashboard plane with slow lateral drift; translucent oversized numerals floating behind cards; fast zoom punch-in; pull-away/fade-to-black beat exit; hard-cut beat stitching; kinetic word push-through (element scales up past the frame); typed line with blinking cursor; impact slam word + particle-dissolve punctuation; glowing wave draw; green delta arrow pop; stat lockup hold. Gauge-beat additions: concentric static arcs + thick clockwise progress-arc draw; rapid count-up tick; scale-up-from-blur entrance / scale-up-and-blur-past-frame exit (element-level fake push-through).

**rule mapping** (motion verb → `rules/<id>.md`)

- count-up number whose transform scale grows with the value → `counting-dynamic-scale` (primary text rule)
- circular progress-ring sweep (the ring fill) → `stat-bars-and-fills` (ring form) — its draw mechanics delegate to → `svg-path-draw`
- growth bars / progress fill paired beside a number → `stat-bars-and-fills` (primary data rule)
- gradient trend-line / area-chart left→right draw → `svg-path-draw` (a path/line draws itself)
- spring-overshoot pop-in of the avatar/object elements → `spring-pop-entrance` (elastic overshoot); the scattered-ring layout of glowing avatars/objects → `avatar-cloud-network`; if they keep drifting/orbiting → `orbit-3d-entry`
- spring-pop `[accent]` checkmark badges → `spring-pop-entrance`
- perspective-tilted card grid (tilt held static while content moves) → `3d-page-scroll`
- directional scroll across the tilted card plane (cards glide in/out of center) → `3d-page-scroll` (scroll) + `viewport-change` (lateral/vertical pan form)
- hero metric card centering (scroll/pan lands the target dead-center) → `coordinate-target-zoom` (target lands at viewport center) / `viewport-change`
- hard-cut from the hook orb into the grid → `scale-swap-transition`
- kinetic tagline assembled word-by-word → `kinetic-beat-slam` (one onset grid, distinct per-word entrances)
- slow continuous zoom-in + push-THROUGH the instruments + lateral/vertical pan between cards + push-in-then-out bookend → `multi-phase-camera` (see camera modifier)
- soft accent glow BLOOM behind the hero card → `ambient-glow-bloom` (un-triggered soft glow/bloom behind the static hero element — distinct from `press-release-spring`'s press-triggered glow and `asr-keyword-glow`'s word-timed envelope)
- selective dim/blur of a SUBSET of grid items (focus-falloff on the non-highlighted cards) → `depth-of-field-blur` (selective per-element blur/dim to spotlight the highlighted cards — the same focus-falloff rule used in `constellation-hub`)
- cursor chart scrub (cursor-tied vertical tracking line + live data readout in a tooltip) → `chart-scrub-readout` (the tracking line, tooltip pop, and seek-safe live value readout driven by cursor x)
- chart activation color flip (second chart lights up under the scrub) → `gsap-effects` (color/opacity chord at the scrub handoff — basic tween, no dedicated rule needed)
- 3D-tilted dashboard plane + slow lateral drift → `3d-page-scroll` (the tilt framing) + `sine-wave-loop` (the drift; keep amplitude tiny so the scrub stays legible)
- fast zoom punch-in to the dashboard → `multi-phase-camera` (one short aggressive push phase) aimed via `coordinate-target-zoom`; add `motion-blur-streak` at peak velocity
- kinetic word push-through / scale-up-and-blur-past-frame exit / scale-up-from-blur entrance → `kinetic-beat-slam` (the beat grammar) + `motion-blur-streak` (blur peaks at max speed, resolves at the settle — its entrance form runs the blur-in, its exit form the blow-past)
- typed line with blinking cursor → `discrete-text-sequence` + `context-sensitive-cursor` (square-wave blink)
- impact slam word → `kinetic-beat-slam`; its particle-dissolve punctuation → `particle-burst` (glyph→particles dissolve, deterministic)
- glowing wave draw → `svg-path-draw` (the draw) + `ambient-glow-bloom` (the glow envelope)
- green delta arrow pop / peak dot + pill tooltip → `spring-pop-entrance`
- concentric static arcs + clockwise progress-arc draw (gauge beat) → `stat-bars-and-fills` (ring form) → draw mechanics `svg-path-draw` (both already mapped above — the gauge is the existing ring with static concentric chrome behind it)

**camera modifier**: The camera is the through-line that traverses the data instruments — one camera wrapper sequenced by `multi-phase-camera`, with each stop targeted via `coordinate-target-zoom` onto the focal instrument/card.

- Problem — push-THROUGH: a slow continuous zoom-in (drift overlay) plus a fast PUSH-IN straight through the center of one instrument into the next (`multi-phase-camera`, Steady-push pattern), then a lateral/vertical PAN to the final card. Z-depth push-through is the signature (distinguishes it from a flat pan-tour).
- Product_Intro — scroll-to-hero + bookend push: a hands-off directional SCROLL across the tilted card plane (`3d-page-scroll` scroll / `viewport-change` pan) that lands the hero card center, then a gentle push-in that PEAKS and eases BACK OUT to a wider settle (`multi-phase-camera`, Bookend-pull pattern). No cursor, no clicks — the camera does the navigating.
- Key_Feature — montage-cut: the camera is NOT the through-line — hard cuts stitch the instrument beats, the frame is locked inside each beat, and exactly ONE fast zoom punch (`multi-phase-camera` single push phase + `coordinate-target-zoom`) lands the dashboard close-up; exits are pull-away/fade-to-black. Between instruments, ELEMENTS fake the push: kinetic words scale up past the frame (`kinetic-beat-slam` + `motion-blur-streak`). Gauge-beat form drops even the punch — fully static, all push-through element-level. Reach for this mode when the dialect is a dark rapid montage; the Problem/Product_Intro modes remain the default for a single continuous argument.


<!-- ===== FILE: hyperframes/hyperframes-animation/blueprints/device-surface-showcase.md ===== -->

# device-surface-showcase — Device / Surface Showcase

**intent**: A product surface — a device mockup or a floating browser/app window — is the hero held in frame while its screens cycle through a real flow, showcased by a camera move that ranges from a static hold to a continuous 3D push.

**roles served**

- Key_Feature (from key-feature-device-screen-tour, key-feature-floating-window-scroll, key-feature-3d-device-hand-demo): show a feature being \_experienced inside its real interface\* — the surface houses the action and its screens advance through a flow, rather than enumerating tiles or chasing a cursor across a workflow. (Note: the three founding drafts are Key_Feature and variants differ by MECHANIC, not role; the mined stepwise-flow variant widens the blueprint to Product_Intro.)
- Key_Feature (from demo-page-scroll-spotlight): the floating-window push-scroll variant carried to a spotlight climax — a real webpage rendered as a tilted 3D card coasts in (power2, like a phone held up — no spring), header keywords flare on a karaoke glow as the VO names them, the page rolls to the demoed section, and one element LIFTS off the surface (translateZ + scale) under a radial spotlight that dims the rest.
- Product_Intro (from stepwise-flow-completion): a compact end-to-end product flow — setup/auth → action → success/confirm — plays out cursorless as successive screen states inside the held surface, capped by a confirming button press; bookended by title-card beats. The surface introduces the product by \_completing its core loop\*, not by touring screens.
- Key_Feature (from `showcase-carousel`): the showcase-carousel — two surfaces in sequence (a widget card cycling brand skins, a phone frame with app screens sliding through it) gated by interstitial claim words; the screen cycle is a breadth carousel ("N brands / N apps"), not a flow.

**duration**: 5–11.3s (page-scroll-spotlight 5–9s · floating-window 7.8s · 3d-hand 7.9s · in-device approval 7.9s · stepwise-flow 8.5–9.4s · device-tour 9.6s · showcase-carousel 11.3s)

**shot structure** One product surface — a `[device mockup]` or a `[floating browser/app window]` — is the persistent hero on a `[styled backdrop: gradient / radial / stylized 3D void]`; its `[screens/sections]` cycle through a real `[product flow]` while a showcase camera (static-hold, push-in→zoom-out, or one continuous push) presents it. Each screen state holds ~1.0–1.5s.

- Scene 1 (0.0–~1.5s): The surface ESTABLISHES — it `[slides in from an edge / drifts in from a tilt / dissolves from a full-frame title card]` and settles, with a `[accent shape or backdrop]` resolving behind it; the first `[screen]` is visible. The showcase camera begins (see variants).
- Scene 2 (~1.5–~Xs): The surface is OPERATED on its own face — a `[tap/select/scroll]` triggers the first screen advance: old content `[pushes out / scrolls up]`, new `[screen/section]` `[pulls up / pushes in from the side]`; concurrently a `[label / header word / side headline]` updates. The camera continues its move.
- Scene 3+ (~Xs–end, repeat for `[2–4 screen beats]`): The surface ADVANCES through successive `[screens/sections]`, each a discrete swap or scroll synced to the surface's flow, while the secondary copy `[swaps out-up / in-up]` or stays marked to hold reading position. HOLDS on the final `[screen]` (or, for one variant, blooms out — see variant).

- Variant — static-tour (key-feature-device-screen-tour, 9.6s): a `[device mockup]` slides in from off-screen and settles (ease-out); an `[accent-color shape]` scales up behind it (spring overshoot). Camera STAYS STATIC the entire clip — all motion is element/UI-level: a tap COMPRESSES a button (95%→100%), the UI scrolls/transitions to the next view (old pushes out, new pulls up), and a `[side headline]` SWAPS beside the device (old slides up + fades, new slides up + in) per screen. Holds on the final screen. No camera move, no cursor.
- Variant — floating-window (key-feature-floating-window-scroll, 7.8s): OPENS on a full-frame `[title card]` (a small `[icon]` draws in at center, `[feature name]` below; holds ~2s), which DISSOLVES to a `[macOS-style browser/app window]` floating on a `[vivid gradient]` (traffic-lights + `[URL pill]` + tabs; left nav, central content, right `[sidebar]`). Camera PUSHES IN on a `[target region/sidebar]` (active item highlighted `[accent]`, a cursor drifts down the list), then ZOOMS BACK OUT to re-frame the whole window while the content SCROLLS through `[sections]`; the `[highlighted item]` stays marked. One push-in→zoom-out arc, gated by the title-card opener.
- Variant — 3d-hand (key-feature-3d-device-hand-demo, 7.9s): FULLY 3D — a `[3D device]` drifts in a `[stylized 3D void / bloom + particles]`, opening tilted and self-rotating to face the lens nearly flat as ONE CONTINUOUS forward camera push begins (no cuts). A glossy `[3D hand]` rises from the bottom-foreground and GESTURE-DRIVES the surface: it swipes to scroll a `[picker/sidebar panel]` of `[option cards]` and taps `[option]` (while a `[header word]` letter-flips in place); the selection APPLIES — a `[new layout]` grows from center to fill the device face, nav flips, a `[marquee]` scrolls horizontally; the hand swipes again to scroll the page upward through `[sections]`, then drifts out. The camera never stops pushing; the bright device face keeps growing toward the lens until it BLOOMS into a `[light]` wash — a zoom-through "portal" exit that fills the frame.
- Variant — stepwise-flow (Product_Intro, 8.5–9.4s; in-device Key_Feature sub-mode 7.9s): CURSORLESS end-to-end flow — the surface completes `[setup/auth → action → success]` as a narrative arc. Opens on a `[title card]` that fades in/out on an ambient gradient (or a typed `[command]` running character-by-character on a terminal field). The `[flow surface]` arrives (phone mock slides up oversized and settles / bordered log panel replaces the command) and step 1 completes via rapid sequential pops — `[OTP digits]` fill boxes left-to-right capped by a green check, or `[log steps]` pop top-down with highlighted tokens, ending on a trailing-dots waiting state. State advances laterally (old content slides out left, new in from right, chrome persists) or via a dark-to-light scene swap into a white `[detail/confirm card]` whose elements stagger in. COMMIT: the `[CTA button]` is pressed (press dip / spinner "Processing") and a `[success state]` renders with check bullets — in the in-device sub-mode the commit runs a biometric ritual: dim overlay, `[squircle]` spring-pops, a ring draws around an icon, the icon morphs to a checkmark and holds; a slight camera push-in fires ONLY at the state transition (camera punctuates the commit, then re-locks). EXIT: the surface leaves and closing `[title cards]` pop in and ease smaller — the surface exits before the coda instead of holding. Camera otherwise static. For this variant the persistent hero is the FLOW, not one surface: a terminal panel may hand off wholesale to a confirm card.
- Variant — showcase-carousel (Key_Feature, 11.3s): TWO surfaces in sequence on a slowly drifting `[pastel mesh gradient]`, static camera, gated by centered interstitial `[claim words]` (fade in with gentle scale-up, fade out). Act 1: a white `[widget card]` scales in, flips/morphs into a tilted vertical widget and CYCLES `[N brand skins]` (~0.8s each) — one shared layout, per-skin content and accent swaps — while a large `[brand logo]` crossfades below per flip; the widget scales away. Act 2: a `[phone frame]` enters oversized and tilted, settles upright at center; full `[app screens]` slide left through it (~1s each), holding on the last. The screen cycle is a breadth carousel, not a flow — no taps, no cursor, no camera.

**motion vocabulary** surface establish (edge slide-in + settle / tilt drift-in + self-rotate-to-camera / title-card dissolve); accent shape spring behind surface; element-level screen-cycling (scroll-swap, push-in-from-side, scale-swap); button tap-compress; staggered side-headline reveal + copy swap (out-up / in-up); in-place header-word letter-flip; floating browser-window-on-gradient idle float; full-frame title-card opener (icon draw-in + label); camera push-IN on a region; camera zoom-OUT re-frame; content scroll-through; one continuous 3D camera-follow push (no cuts); 3D device drift + self-rotate; stylized-environment bloom/particles; 3D-hand entrance + swipe-scroll + tap (gesture-driven); picker-panel slide-in; template-apply grow-from-center; horizontal marquee scroll; gesture-driven page scroll; zoom-through bloom/portal exit; static-hold (no camera) as the floor of the camera range. Stepwise-flow additions: title-card bookends (fade-in/out opener; closers pop in then ease smaller); typed terminal command with prompt chevron; sequential top-down log pops with sub-line reveals; animated trailing-dots wait state; sequential digit pops left-to-right + green check confirm; lateral screen slide with persistent chrome; dark-to-light scene swap; staggered card element build-in (fade + slide-up); button press dip + fill flip; spinner processing state; success check-bullet reveal; notification banner spring-in with overshoot; lockscreen fade/blur-away as a card expands to fill the device face; commit-synced micro push-in; dim overlay; squircle spring pop; circular ring draw; icon morph to checkmark; surface exit before a title coda. Showcase-carousel additions: interstitial claim-word gate; brand-skin cycling with per-flip logo crossfade; card flip/morph into a tilted widget; oversized-tilted surface entry settling upright; fast slide-left screen carousel inside a static frame; drifting mesh-gradient backdrop.

**rule mapping** (per motion verb → backing rule, or flagged special)

- screen-cycling — UI scrolls/sections scroll inside the surface (device-tour, floating-window scroll, 3d-hand page scroll) → `3d-page-scroll` (webpage/app as a tilted card whose content `translateY`-scrolls to sections; primary mechanic for the surface's screen flow)
- floating-window establish + the surface presented as a tilted/floating UI card → `3d-page-scroll` (the tilt/perspective framing) + `css-3d-transforms` (perspective/`translateZ` depth)
- screen / side-copy state swaps (discrete screen states; side headline content swapping per beat) → `discrete-text-sequence`
- side-headline reveal (staggered fade + slide-up) → `discrete-text-sequence`
- in-place header-word letter-flip (3d-hand) → `hacker-flip-3d`
- screen swap as a coordinated shrink-out / pop-in between two screen states → `scale-swap-transition`
- template-apply "new layout grows from center to fill the face" (3d-hand) → `center-outward-expansion` (clustered-at-center → expand to fill)
- the surface morphing between states / title-card→window dissolve as the eye-anchor transition → `card-morph-anchor`
- button tap-compress (95%→100% press feedback) → `press-release-spring` (or `physics-press-reaction` for a heavier press)
- floating-window cursor click on the highlighted list item → `cursor-click-ripple`
- accent-highlight pop on the active sidebar/list item → `asr-keyword-glow` (accent glow on the focused item)
- drifting cursor down the sidebar list (floating-window) → `camera-cursor-tracking` (flat-cursor drift; pairs with the push-in)
- floating browser-window idle float / 3D device drift-breathe → `sine-wave-loop`
- 3D device drift + self-rotate-to-camera + perspective depth (3d-hand) → `css-3d-transforms` (CSS-3D) **or** `3d.md` technique (true Three.js/R3F device); see camera modifier
- horizontal `[marquee]` scroll (3d-hand) → `viewport-change` (PAN mode on the marquee strip) — _thin fit; a literal CSS-marquee/translateX loop is closer to a `gsap-effects`/CSS recipe than a named motion rule_
- 3D-hand entrance + swipe + tap as the interaction DRIVER (gesture input that scrolls/selects) → **flagged special — needs a heavier capability beyond the rule library (R3F/Three.js + WebGL), NOT a motion-shape rule.** The 3D hand model + WebGL bloom have a _technique_ backing (`3d.md` — R3F, `useGLTF` HandModel, `--gl=swiftshader` for the shader/bloom), but no motion-shape rule models a 3D hand as the swipe-to-scroll / tap-to-select gesture protocol. `context-sensitive-cursor` / `camera-cursor-tracking` only model a flat typing/pointer cursor, not a 3D gesturing hand.
- zoom-through bloom / portal exit (3d-hand) → **flagged special — needs a heavier capability beyond the rule library (WebGL), NOT a named transition rule.** Capability is `techniques.md` → WebGL shader (via `3d.md` headless WebGL: `--gl=swiftshader --concurrency=1`), but no named transition rule covers a bloom/portal fly-through.
- typed terminal command / non-linear log text (stepwise-flow) → `discrete-text-sequence` (typing + threshold state replacement) with `dynamic-content-sequencing` computing each step's window from content length
- sequential top-down log pops / OTP digit pops left-to-right / staggered confirm-card build-in → `spring-pop-entrance` (staggered group form; low overshoot for log lines)
- trailing-dots wait state → `sine-wave-loop` (finite repeats; step the opacity of 3 dots on a shared phase)
- lateral screen slide with persistent chrome → the existing screen-cycling mapping (`3d-page-scroll` translateX form inside the clipped surface); chrome sits outside the sliding layer
- notification banner spring-in / squircle pop (in-device) → `spring-pop-entrance`
- lockscreen fade/blur-away + card expands to fill the device face → `card-morph-anchor` (uniform-scale container morph — never tween width/height) + `depth-of-field-blur` (the blur-away)
- commit-synced micro push-in (camera punctuates the Approve/tap, then re-locks) → `multi-phase-camera` (single short push phase placed at the state transition)
- button press dip + fill flip / Approve press-down spring-back → `press-release-spring` (already mapped; the fill flip is its color-transition variation)
- spinner processing state → `svg-icon-enrichment` (rotating internal element with explicit SVG center)
- success check bullets / biometric ring draw → `svg-path-draw` (check strokes; ring rotated −90° to start at 12 o'clock) + `spring-pop-entrance` for the bullet pops
- icon morph to checkmark (biometric ritual) → **flagged special — SVG path morph, see hyperframes-keyframes (morph)**; no motion-shape rule models it — mechanics live in `techniques.md` / the keyframes skill, same tier as the blueprint's existing WebGL flags
- interstitial claim-word gate (fade + gentle scale-up, then out) → `gsap-effects` (plain fade/scale chord; deliberately quieter than `kinetic-beat-slam`)
- brand-skin cycling with per-flip logo crossfade → `discrete-text-sequence` (whole-state content replacement at thresholds) + `scale-swap-transition` where a flip reads as shrink-out/pop-in; the card→tilted-widget flip/morph → `card-morph-anchor` + `css-3d-transforms`
- drifting mesh-gradient backdrop → `sine-wave-loop` (very-low-amplitude position/hue drift on gradient blobs)

**camera modifier**: The showcase camera spans a RANGE keyed by variant, all on a single content-wrapping virtual camera (`viewport-change`):

- static-tour → NO camera move (`viewport-change` held at scale 1, or omitted); all motion is element-level. This is the floor of the range and what distinguishes the device-tour from the rest.
- floating-window → a two-phase push-in → zoom-out arc → `multi-phase-camera` (e.g. dramatic-reveal 1.1→1.0→0.95 feel): push IN on the `[sidebar/region]` via `coordinate-target-zoom` (off-center target = scale + counter-translate), then `multi-phase-camera` zooms back OUT to re-frame the whole window while content scrolls.
- 3d-hand → ONE continuous forward push (no cuts) → `multi-phase-camera` in steady-push mode (1.0→1.03→1.06… plus its sine micro-drift) layered over `css-3d-transforms`/`3d.md` so the device self-rotates-to-lens during the push; the push runs unbroken into the bloom/portal exit (exit itself is the WebGL-shader flagged special above). Across all three: `viewport-change` is the base virtual-camera primitive; `multi-phase-camera` sequences the push/zoom phases (and supplies the always-on micro-drift that keeps even the "static" tour from feeling dead); `coordinate-target-zoom` aims the push at off-center screen detail.

**Overflow (pan/scroll surfaces — required for a clean `check`):** a panned or scrolled surface deliberately moves content PAST the edges of its framing card. Clip it at the card (`overflow: hidden` on the card/window) AND mark the moving inner layer (the `.world` / surface wrapper holding the screenshot + any markers/labels) with `data-layout-allow-overflow` — otherwise `check` reports `text_box_overflow` / `container_overflow` errors for the parts that scroll off (e.g. a marker label panned off the left edge). The card clips them visually; the attribute tells the layout audit it's intentional, not a layout bug.


<!-- ===== FILE: hyperframes/hyperframes-animation/blueprints/fixed-anchor-cycle.md ===== -->

# fixed-anchor-cycle — Fixed Anchor, Cycling World

**intent**: One element is PINNED — a wordmark, a composer box, an anchor line that enters once and never moves again — while the adjacent region (or the entire surrounding theme) cycles through many discrete states around it, cadence often manipulated (steady stepping, a fast carousel, or a slow→accelerating flurry), resolving on an emphasis beat into a completed lockup or a muted freeze. The stillness of the anchor IS the claim: everything changes, this stays. Distinct from `kinetic-type-beats` sub-shape A, where a word-slot inside a centered line swaps and the sentence itself is the subject — there the anchor is a sentence frame on a bare type field; here the anchor is the PRODUCT identity and what cycles around it can be non-text (whole theme skins, chrome/logo swaps, textured label chips, a carousel list), the cycle asserts breadth ("everyone says / works everywhere / calling all X"), and the resolve completes the anchor into a lockup. Distinct from `ticker-takeover`, whose cycle ends in a collision — a hero crashes in and shoves the text aside; here nothing ever collides with the anchor: the cycle stops, and a final element quietly joins it.

**roles served**

- Brand_Outro (from `static-anchor-rapid-text-swaps`): when the sign-off is the brand name sitting immovable while praise quotes / tagline words cycle beside or beneath it — steady per-word highlight stepping, or a hard-cut chip flurry that accelerates — landing on the finished lockup ("bolt.new / prompt, run, edit, deploy / enjoy."; "Opus 4.6 by ANTHROP\C").
- Benefits: when "works everywhere" is shown literally — one product surface (a prompt composer with one verbatim string) pinned dead-center while its ENTIRE shell morphs in place through N product themes (background, typography, radii, chrome, logos all crossfading at once), ending in a washed-out freeze.
- Hook: when the opener is a roll-call — a static anchor line holds while an accent-colored line beneath it runs as a fast vertical carousel through an audience/option list, then the block clears into follow-up statement beats that land the brand line.

**duration**: 6.6–11.1s (Benefits shortest ~6.6s at 4 theme beats; Brand_Outro ~9–9.4s; Hook longest ~11s when the anchor-cycle block hands off to follow-up statement beats). The cycle engine itself occupies ~3–5s regardless of role.

**shot structure** (flat static frame — camera locked in every member; a `[bg]` field, solid or subtly drifting; two folded sub-shapes — **(A) adjacent-region cycle**: the anchor holds and a neighboring slot swaps through N states; **(B) whole-context morph**: the anchor holds and everything AROUND it re-skins in place)

- **Scene 1 (0.0–~2.0s) — the anchor lands and PINS.** The `[anchor: wordmark / product name / composer box / lead line]` enters once — fade/scale-in centered, word-by-word build, or already present at frame one — at a fixed position it will hold for the entire clip. Zero movement from here on: no drift, no breathe, no re-layout. If the anchor is a UI surface (sub-shape B), it carries a `[verbatim string]` with a blinking cursor.

- **Scene 2 (~2.0s–~70% of runtime) — the cycle engine (signature move).** The world changes around the unmoved anchor. Choose by sub-shape:
  - **Sub-shape A (adjacent-region cycle)**: a region beside/beneath the anchor steps through N discrete states — pick ONE swap mechanic and ONE cadence:
    - _swap mechanics_: instant hard-cut label replacement (a `[chip / tape label]` slaps over the old one, texture/highlight shifting slightly, chip width re-fitting each `[phrase]` — growing away from the anchor, never over it); sequential per-word highlight stepping (one word of the `[tagline]` snaps bright/bold while the rest sits dim grey, the highlight walking the line); or a fast vertical carousel (each `[list item]` slide/fades through the accent slot ~0.5s/phrase).
    - _cadences_: steady stepping (~0.5–1s/state), or **slow→accelerating flurry** — ~1s beats compressing to ~0.15–0.3s per swap, breadth escalating into a blur of states (12–16 states read as "everyone"; 3–8 read as a roll-call).
    - Geometry law: the cycling region NEVER overlaps, touches, or displaces the anchor; size the layout so the longest state still fits inside the frame with clear margins.
  - **Sub-shape B (whole-context morph)**: at ~1.3s intervals the entire theme — `[bg color]`, typography, corner radii, toolbar icons, footer `[brand logos]`, contextual lines — morphs in place via quick (~0.3s) crossfades through N `[product skins]`, every property blending simultaneously. No hard cuts, no wipes; the anchor's content string is identical in every skin (chrome details like a `> ` prefix may adapt per skin).

- **Scene 3 (~70–85%) — the emphasis beat.** The cycle resolves — it does not just stop:
  - _Variant — Brand_Outro (highlight stepping)_: the whole `[tagline]` snaps solid bright at once — full-line illumination after the per-word walk.
  - _Variant — Brand_Outro (flurry)_: the flurry halts and HOLDS on the `[longest / weightiest phrase]` — a beat of stillness after acceleration.
  - _Variant — Benefits (theme morph)_: the final beat mutes — a faint `[dot-grid]` fades in across the background while the UI drops to low opacity, a washed-out blueprint freeze.
  - _Variant — Hook (carousel)_: the anchor block clears, handing off to 1–3 centered word-by-word statement beats (kinetic-type-beats territory) that carry toward the close.

- **Scene 4 (final beat → end) — lockup completion and HOLD.** A final element joins the still-unmoved anchor and the finished composition holds static to the end: a `[closing word]` drops in below, aligned to the last cycled state ("enjoy."); the chip vanishes on a hard cut and the `[brand sign-off]` appears beside the anchor on a shared baseline ("by ANTHROP\C"); or the final `[brand line]` builds word-by-word dead-center and holds ("with Copilot."). Long static hold — the lockup is the payoff, give it 20–30% of the runtime.

**motion vocabulary**: anchor fade/scale-in entrance; permanently pinned anchor (zero movement, no idle breathe); instant hard-cut label/chip replacement (slap-over with subtle texture/highlight shift); chip width resize-to-fit per phrase (grows away from the anchor); sequential per-word highlight stepping through a line; dim-to-grey line state; whole-line illumination snap; fast vertical carousel slide/fade of one line under a static line; cadence acceleration (slow ~1s beats into a ~0.15–0.3s flurry); hold-on-longest-phrase emphasis beat; in-place theme morph crossfade (~0.3s) blending background/fonts/radii/icons simultaneously; per-beat chrome/logo swap; blinking text cursor; contextual line appearing/disappearing across beats; dot-grid backdrop fade-in; global opacity washout; end freeze; word-by-word phrase build; block clear between scenes; drop-in entrance of a final word; hard cut to final lockup; long static hold.

**rule mapping**

- instant hard-cut chip/label/phrase swaps at time thresholds; per-word highlight stepping (color/weight state swaps); dim-line → full-line illumination snap; per-state chip width set (a per-state layout property, set discretely — never tweened) → `discrete-text-sequence`
- fast vertical carousel of the accent line under the static anchor (slide/fade stepped swaps in a masked slot) → `vertical-spring-ticker` (its footer-reveal step unused — Scene 4's lockup takes its place)
- per-phrase state windows computed from a script of N states (praise quotes, audience list, theme beats) → `dynamic-content-sequencing` (Accelerating cadence — for the flurry, pre-compute the beat array with shrinking `hold` values, geometric decay over the state list)
- word-by-word phrase builds (anchor line, follow-up statements, final brand line) → `dynamic-content-sequencing` + `waterfall-entry` (or `kinetic-beat-slam` when the statements should land percussively)
- anchor entrance fade/scale-in; drop-in of the final closing word → `spring-pop-entrance` (restrained overshoot — the register here is editorial, not bouncy)
- blinking cursor in the pinned composer → `context-sensitive-cursor` (color adapts per theme skin at segment boundaries)
- whole-context theme morph → `theme-crossfade-morph` (N pre-styled full-scene layers stacked at the same geometry, opacity-crossfaded, the shared anchor string rendered once on top); the composer shell's radius/surface component alone → `card-morph-anchor`
- subtly drifting background field beneath the cycle → `sine-wave-loop` (bounded drift; the anchor itself gets none)
- dot-grid fade-in + global opacity washout freeze; long static hold → `gsap-effects` (plain opacity tweens) / static hold (no rule needed)

**camera modifier**: none — every member is fully camera-static; the cycle is the only motion, and the pinned anchor's stillness is load-bearing. Do not add a push-in "for energy"; it would break the anchor contract.


<!-- ===== FILE: hyperframes/hyperframes-animation/blueprints/grid-card-assemble.md ===== -->

# grid-card-assemble — Grid / Card Assemble

**intent**: N items (tiles / cards / logos / list-lines) self-assemble in a staggered cascade into a grid or vertical list and hold — a "look how much / who / what it does" beat that enumerates breadth at once; an optional camera zoom-OUT pulls back to reveal the assembled array sitting inside a vaster whole.

**roles served**

- Key_Feature (from key-feature-card-grid-assemble): a grid of labeled feature tiles/pills (icon + label) cascades one-by-one into a 2-col-brick / 3×3 grid, then holds near-static with a slow push-in — enumerate many capabilities, no live UI, no cursor.
- Key_Feature (from key-feature-glass-card-camera-reveal): open TIGHT on 2–3 glowing icons; a camera zoom-OUT unfolds a row of glassmorphism cards that grow from behind the icons (icons shrink to card headers), center card scales forward, the group floats, then sweeps out — a "pillars revealed at once" reveal variant of the same assemble shape.
- Benefits (from benefits-vertical-list): short value phrases populate a single vertical list ~1 item/sec, co-resident and accumulating; each line enters via a spring marker-pop + check-draw + pill mask-wipe, OR the whole stack snaps up one slot per beat (slot-machine) so the newest lands in the bright focal slot.
- Social_Proof (from social-proof-logo-grid-zoom-out): a wall of partner/app logos builds into a center grid (whole-enter / randomized pop-in / column slide-up), an optional headline + accent-gradient proof-number fills in above, then a continuous camera zoom-OUT shrinks the array to reveal a vast ecosystem; optional fixed HUD/viewfinder brackets; optional grid slide-up fly-out exit.
- Key_Feature (from live-data-populate-board): the array assembles by POPULATING ITSELF — skeleton pills fill and swap to real data, cards spring in tethered to map markers — and its state keeps flipping live after assembly (status pills stepping through states); no cursor, locked frame. The "look how much" beat becomes "look, it's doing it right now."
- Benefits (from item-field-to-payoff-card): a breadth FIELD — a rapidly streaming list past a fixed focal slot, or a chip array with one highlighted hero — plays its breadth motion, then CLEARS to concise centered payoff text (claim / price / URL end card). The array is the argument's setup; the payoff line is its landing.

**duration**: 3.0–10.5s (Social_Proof 3.0–6s · live-populate 4.2–7.8s · Key_Feature grid 5.8–7.3s · Benefits stream/field-to-payoff 5.9–8.4s · Key_Feature glass-card 6.5s · Benefits list 6.5–10.5s, scaling ~1 item/sec with count)

**shot structure** (consolidated template — concrete motion verbs, [slots])

- **Scene 1 (0.0–~1.0s) — open + first arrivals.** On a `[gradient / radial / dark background]` (optional `[dot-grid / drifting-watermark]` texture), an empty `[grid or list region]` is established and items begin to ASSEMBLE in a quick staggered cascade (~0.04–0.08s gap; list pacing ~1 item/sec). Each `[item: feature tile / pill / logo tile / benefit line]` fades + slides/scales a short distance directly into its slot (low drama — no scatter, no big bounce; spring overshoot reserved for accent markers). Camera static. An opening `[headline / hook]` may fill in line-by-line above the array, with any `[proof number]` counting up in an `[accent gradient]`.
- **Scene 2 (~1.0s–~Xs) — array resolves + holds.** Remaining items finish arriving; layout resolves into the final `[2-col-brick / 3×3 grid / dense mosaic / stacked list]`. The completed array HOLDS, alive but resting: a gentle continuous parallax/sine FLOAT on the tiles and/or a slow camera push-in (faint scale-up). Optional `[accent-color]` glow TRAVELS across/behind the tiles.
- **Scene 3 (~Xs–end) — settle / reveal / exit.** Everything settles and holds to the end, OR the optional camera modifier runs (see below), OR a `[closing line / CTA]` book-ends the array. OR the field CLEARS to payoff copy — the array exits and a concise centered `[claim / price / URL]` lands (price via a very fast character snap-build with a split-second partial state; URL via a left-to-right reveal, holding in `[accent]` and flipping to `[ink]` only in the final beat) — OR the camera PUSHES THROUGH one highlighted `[hero item]` (single rapid accelerating push-in) and crossfades into a second, vaster receding `[word-grid depth field]` that continuously scales down to reveal ever more items before fading to the payoff.

Variants (where roles diverge from the template):

- **Variant — Key_Feature grid**: items are labeled `[icon + feature-label]` tiles/pills assembling into a 2-col-brick / 3×3 grid; near-static hold with slow push-in + optional traveling-glow sweep; headline book-ends (`[hook]` → `[CTA]`). No camera reveal.
- **Variant — Key_Feature glass-card-reveal**: the assemble is CAMERA-DRIVEN, not element-stagger. Open tight on `[2–3 glowing icons]`; camera zoom-OUT grows `[N]` glass cards out from behind the icons (icons shrink ~50% to become card headers), `[center card]` scales ~105% and moves forward to overlap the sides (quick spring); cards hold side-by-side with continuous parallax float; exit = fast motion-blur SWEEP slides the cards off-frame.
- **Variant — Benefits vertical-list**: a single vertical `[benefit-line]` stack, ~1 item/sec, three sub-modes — (a) BUILD: each line stays fully lit; entry = `[marker]` spring-pop + `[check/icon]` draw-in + `[pill]` mask-wipe of the text; (b) SNAP: the whole stack steps up one slot per beat (~0.1s eased) so the newest line lands in the bright focal slot and lines leaving it dim by position; (c) STREAM: the list scrolls rapidly and continuously past the focal slot — center item opaque `[ink]` and slightly enlarged, neighbors faded/shrunk — then DECELERATES to stop on the `[chosen item]`; optionally split-framed against a fixed static `[label]` on the opposite side; the field then clears to a centered `[payoff line]`. Static camera; optional perpetual `[decorative orbit/disc]` on the opposite side. No camera reveal.
- **Variant — Key_Feature live-populate**: the assemble is a DATA-POPULATION wave, cursorless, frame locked (± one gentle opening zoom-out that makes room for the `[headline]`). Two board shapes — (a) ANCHORED: `[white data cards]` spring in one-by-one, each tethered by a thin line to its `[marker]` on a `[map/board surface]` whose markers pulse (expanding fading rings); (b) TABULAR: new `[columns]` appear as grey skeleton pills, progress fills run left→right staggered top-to-bottom (colored fill with a leading tip), each bar SWAPPING to its real `[value/avatar chip]` on completion. After assembly the array stays LIVE: `[status pills]` flip states in quick snappy swaps (color-coded, several in succession), or the `[headline]` crossfades and a second population wave runs on a newly revealed region — the table content scrolling horizontally beneath a sticky first column to expose it. Hold lands on the fully populated, fully updated final state.
- **Variant — Social_Proof logo-wall-zoom-out**: intro beat (`[trusted-by headline]` card OR a `[product screenshot]`) crossfades/cuts to a center logo grid that builds (whole-enter / randomized pop-in / column slide-up); a continuous camera zoom-OUT then shrinks the whole grid toward center to reveal a vast ecosystem and holds; optional fixed HUD/viewfinder brackets; optional exit = whole grid SLIDES UP and flies out through the top.

**motion vocabulary**: item stagger-assemble (fade + short slide/scale into slot) · brick/grid/list layout resolve · randomized pop-in · column slide-up · vertical-list step (slot-machine snap-and-hold) · spring-overshoot marker pop · check/icon draw-in · pill/label mask-wipe reveal · dim-by-position de-emphasis · line-by-line headline fill · accent-gradient number count-up · near-static hold · gentle parallax/sine float on hold · slow camera push-in · camera zoom-OUT reveal (continuous OR phased pull-back) · cards-grow-from-behind-icons · icon-shrink-to-header · center-card scale-up + forward overlap (spring) · traveling-glow sweep · fixed HUD/viewfinder brackets · motion-blur slide-out sweep (exit) · grid slide-up fly-out (exit) · book-end headline fade · perpetual decorative orbit/loop · skeleton-pill progress fill (left→right, leading tip, color transition) · fill-completes-swap-to-real-data · staggered top-to-bottom fill cascade · live status-pill state flips (color-coded, post-assembly) · tethered-card spring-in (thin line to an anchor marker) · pulsing marker rings · two-wave populate with headline crossfade · sticky-column internal horizontal scroll · rapid vertical stream past a fixed focal slot + deceleration stop · split fixed-label layout · pill-widens-as-label-fills arrival · highlighted hero chip · push-through-the-hero-item exit · receding word-grid depth field · clear-to-payoff coda · price snap-build (split-second partial state) · left-to-right URL reveal + final-beat color flip.

**rule mapping** (motion verb → `rule-id`)

- item stagger-assemble into slot → `center-outward-expansion` (per-item stagger + short-path slide variant; for a wall too dense for a true center burst, use it in its "starting partially-spread"/direct-into-slot form — see merge tension)
- brick/grid/list layout resolve → `center-outward-expansion` (target positions = final layout slots)
- randomized pop-in stagger → `gsap-effects` (stagger recipe; randomized `from`/order)
- column slide-up into grid → `gsap-effects` (per-column staggered slide-up)
- vertical-list step / slot-machine snap-and-hold → `vertical-spring-ticker` (STEPS = number of line advances)
- spring-overshoot marker pop → `spring-pop-entrance` (back.out spring) — also `gsap-effects` for the staggered pop chain
- check / icon draw-in inside marker → `svg-path-draw`
- live line-art icon in a tile (internal parts) → `svg-icon-enrichment`
- pill / label mask-wipe text reveal → `techniques.md` (clip-path reveal)
- dim-by-position de-emphasis → `gsap-effects` (per-line opacity by slot position; no dedicated rule)
- line-by-line headline fill → `discrete-text-sequence`
- accent-gradient proof number count-up → `counting-dynamic-scale`
- gentle parallax / sine float on hold → `sine-wave-loop` (apply the concurrent-elements amplitude `/√N` rule for a held grid)
- slow camera push-in → `multi-phase-camera` (steady-push phase pattern)
- center-card scale-up + forward overlap → `spring-pop-entrance` (the quick spring) + `techniques.md` CSS-3D (z-depth overlap)
- cards-grow-from-behind-icons / icon-shrink-to-header → driven by the camera reveal (`multi-phase-camera`) — the grow/shrink are scale tweens chorded to the pull-back phase; no separate rule
- fixed HUD / viewfinder brackets → `ai-tracking-box` (static-bracket variant — overlay frame, not tracking)
- book-end headline fade → `discrete-text-sequence` (or `gsap-effects` fade)
- perpetual decorative orbit / disc / loop → `sine-wave-loop` (or `orbit-3d-entry` if it's an orbiting badge ring)
- traveling-glow sweep across/behind tiles → `ambient-glow-bloom` (one-pass traveling glow sweep across the tiles)
- motion-blur slide-out sweep (glass-card exit) → `motion-blur-streak` (directional velocity blur on the fast sweep that carries the cards off-frame)
- grid slide-up fly-out exit → `gsap-effects` (plain staggered translate-off-frame; no dedicated rule needed — a basic exit tween, not a missing capability)
- skeleton-pill progress fill → `stat-bars-and-fills` (progress-fill `scaleX` form; the leading tip is a chorded child element)
- fill-completes-swap-to-real-data / live status-pill flips / headline crossfade between waves → `discrete-text-sequence` (whole-state replacement at time thresholds — the pill's states are text states)
- staggered top-to-bottom fill cascade → `gsap-effects` (per-row stagger on the fill tweens)
- tethered-card spring-in → `spring-pop-entrance` (the card) + `avatar-cloud-network` (the thin connection-line-to-anchor layout; anchor coordinates must match the marker exactly) + `svg-path-draw` if the tether draws in
- pulsing marker rings → `cursor-click-ripple` (its expanding-ring + attack-decay opacity envelope, minus the cursor/click, on a bounded repeat)
- sticky-column internal horizontal scroll → `viewport-change` (PAN form on the inner column layer; the sticky column sits outside the panned layer) — mark the moving layer `data-layout-allow-overflow` and clip at the table card
- rapid vertical stream past a focal slot + deceleration stop → `vertical-spring-ticker` (continuous form: one long decelerating translate instead of its stepped tweens; focal-slot emphasis reuses the dim-by-position mapping above)
- pill-widens-as-label-fills → `card-morph-anchor`'s substitution law (uniform `scaleX`/clip-path — never tween `width`) + `discrete-text-sequence` for the label fill
- push-through-the-hero-item exit → `multi-phase-camera` (single accelerating push phase) aimed via `coordinate-target-zoom` at the highlighted chip, crossfading at peak
- receding word-grid depth field → `viewport-change` (one `.world` wrapper, `cam.scale` ↓ continuously — the zoom-OUT reveal grammar pointed at a word field; size/opacity tiers fake the depth)
- price snap-build (split-second partial state) → `discrete-text-sequence` (non-linear typing with bulk additions — exactly its typo/partial-state mechanic)
- left-to-right URL reveal → `techniques.md` (clip-path reveal — same mapping as the pill mask-wipe); the final-beat color flip → `gsap-effects` (a `tl.set` at the beat — basic, no rule needed)

**camera modifier — zoom-OUT reveal** (optional; the role-defining move for the glass-card and logo-wall variants): a camera wrapper around the whole array scales DOWN over the hold, revealing the assembled grid/cards sitting inside a larger environment (ecosystem scale, or a row of cards unfolding from tight icons).

- Continuous single-pass zoom-out (Social_Proof ecosystem pull-back) → `viewport-change` (one wrapper, `cam.scale` ↓ via onUpdate — single source of truth)
- Phased pull-back → focus → settle, with built-in drift (Key_Feature tight-icons → cards-unfold) → `multi-phase-camera` (use the "Dramatic reveal: push → neutral → pull" / pull-back phase pattern; grow/shrink of cards chords to the pull-back phase)

---

```
BLUEPRINT: grid-card-assemble — serves Key_Feature, Benefits, Social_Proof (folded 4 drafts + 2 mined clusters: live-data-populate-board, item-field-to-payoff-card)
RULE COVERAGE: complete, no gaps — traveling-glow sweep → ambient-glow-bloom; motion-blur slide-out sweep (exit) → motion-blur-streak; grid slide-up fly-out (exit) → gsap-effects (plain translate); skeleton-fill populate → stat-bars-and-fills + discrete-text-sequence; push-through-hero exit → multi-phase-camera + coordinate-target-zoom
```

Merge tension: `center-outward-expansion` (the natural backing for stagger-assemble) caps cleanly at 3–8 items and explicitly warns 8+ causes mid-flight overlap chaos — but a Social_Proof logo wall is deliberately dense (12+ tiles), so for that variant the items must NOT burst from a shared center; they slide a short distance directly into their own slot (the rule's "starting partially-spread"/short-path form, or a `gsap-effects` per-item stagger), which the consolidated Scene-1 verb already specifies as "short distance directly into its slot."


<!-- ===== FILE: hyperframes/hyperframes-animation/blueprints/kinetic-type-beats.md ===== -->

# kinetic-type-beats — Kinetic-Type Beats

**intent**: A flat, centered, bold-type shot where the motion IS the word/phrase changing — the line either swaps tokens in place by hard cut, or builds a statement across full-screen beats (each with its own move) that lands a spring-pop payoff.

**roles served**

- Hook (from `hook-kinetic-type-flash`): when one stationary line lands a punchy rhetorical question or "you keep doing X" callout and the in-place token swap itself is the joke.
- Hook (from `hook-kinetic-type-escalation`): when ONE statement should escalate across distinct full-screen beats (each a different move) and punctuate on a spring-pop payoff element — a rising-intensity / "transform X into Y" opener.
- Hook (from `kinetic-type-to-logo-reveal`): when rapid centered word beats are the warm-up for a typography-to-brand arc — the swaps resolve into a logo reveal (pop-in whole, or 3D parts assemble and flatten into the flat mark) that hands off to a value card / browser mockup sliding in.
- Hook (from `centered-beat-triptych`): when the open is three center-stage beats on a constant field, each element ALONE on screen — and a beat's payload may be non-text (a logo-lockup rotation-snap, a CTA button spring-pop with a one-shot glow-ring pulse, a benchmark chart that builds and holds); the last beat holds to the end.
- Problem (from `problem-kinetic-type-beats`): when the script is 3–5 short pain statements (or a "what-if?" framing) that should each land alone, on a bare canvas, before the next replaces it — no product visible yet.
- Problem (from `centered-phrase-relay-question-hook`): when the pain is an ordered chain of question/hook phrases that scale-pop through center relay-style (each exits as the next arrives) and land a specially-styled climax word — OR resolve the question on a `[product surface]` entering as an element move, never a camera zoom.
- Product_Intro (from `product-intro-kinetic-type-namedrop`): when the hook IS the words — hard-cut through "Introducing…" / tagline / value beats and resolve on the brand name or logo.
- Product_Intro (from `fixed-line-word-swap`): when a fixed headline holds and ONLY one word-slot changes — cursor-deleted-and-retyped once (optionally by a labeled collaborative cursor) or rapid-cycled through a `[role]` list — then hands off to the product/brand payoff; the purest sub-shape A.
- Product_Intro (from `flat-field-kinetic-word-run`): when a sentence builds word-by-word on a flat brand-color field and each `[hero word]` earns a bespoke one-shot effect payoff (letter-scramble, chromatic glitch, confetti burst, emoji morph) before a punch-word finale.
- Product_Intro (from `anchored-wordmark-transform`): when the anchored type itself mutates — an "Introducing" / predecessor beat builds or swaps into the `[wordmark]` in place, which then TRANSFORMS (a UI collage rushes outward from behind it, a word morphs into a pulsing icon, the title zoom-blurs away) into a short payoff beat.
- Benefits (from `benefits-kinetic-type`): when "what you get" is a rapid-fire staccato montage — 8–12 short value phrases, each flashing and clearing before the next at high tempo.
- Benefits (from `flat-void-statement-relay`): when the value reads as a SLOW statement relay — 2–4 full statements on a flat void, each built by its own engine (typewriter, oversized element-scroll, outline-echo stack, wave-mapped pattern) and held ~1.5s+ before the hard cut; the low-tempo sibling of the staccato montage.
- CTA (from `cta-kinetic-type`): when the sign-off is a punchy closing line (or a short stack of value lines) that snaps/fades in beat-by-beat and lands on the brand lockup or URL — no spatial set, no clicked button.
- CTA (from `kinetic-beat-chain-to-logo`): when the sign-off chains 3–5 message beats and each beat carries a DIFFERENT kinetic gag (marquee scroll-through, flash-swap word list, brief 3D letter extrude, spring-bounce prop, one interleaved mock-UI beat) before the logo/URL forms — optionally out of a preceding glow pulse — and holds.
- Brand_Outro (from `brand-outro-kinetic-type-resolve`): when the close is a rapid center-channel barrage of single-word verbs asserting breadth, resolving on the brand's one defining word (motion-is-the-message, no logo lockup).
- Brand_Outro (from `centered-beat-relay-to-url`): when the close is a short relay of full-frame beats — fade/scale swaps, a spring shrink-to-0, an `[icon]` bounce, a gradient-swept title card — terminating in a centered `[URL / domain]` end card held for the longest stretch of the shot (~40–75% of runtime); an optional `[product UI]` prologue scales down and fades to the canvas first.

**duration**: 3.0–12.9s (Benefits staccato fastest ~3.5–4s at 8–12 sub-0.5s beats, statement-relay Benefits up to ~8.3s; Product_Intro fixed-line as short as ~3.0s; Problem 4.1–12s; CTA spans 3.6–12.9s with beat count; Brand_Outro ~3.6s as a verb barrage, up to ~12.6s when the terminal URL hold carries 40–75% of the runtime)

**shot structure** (flat, fixed center anchor; bold sans-serif text on a solid `[bg color]`; type/tokens are the default subject, though a beat's payload may be ONE non-text center-stage element — a logo lockup, a CTA button, a chart — obeying the same arrive-hold-clear law; camera locked unless a modifier is noted; two folded sub-shapes — **(A) fixed-line token swap** and **(B) multi-beat statement build**)

- **Scene 1 (0.0–~1.0s) — first beat lands.** Solid `[bg color]` field. Bold `[type color]` text arrives dead-center via ONE entrance: type-on character-by-character with a trailing blinking caret, OR a hard-cut FLASH-in (no fade/slide), OR a per-word staggered fade/blur, OR an oversized word that smoothly SCALES DOWN to a small centered word. An optional `[accent color]` move plays on the key word(s): a left→right drawn underline / strike-through, a small particle/dot burst from behind the text, or a `[accent color]` selection-box framing the word.
  - _Variant — Hook (flash)_: just the fixed `[hook line]` (or its first word) parks at center; no escalation move.
  - _Variant — Hook (escalation)_: `[beat 1 text]` arrives big and scale-downs to centered, OR sits over a glowing `[motif]` with a slow camera push-in (see camera modifier); ends on a hard cut.
  - _Variant — Hook (logo reveal)_: centered bold words swap in with quick spring-scale pops on a flat/gradient field while flat `[accent]` circles/dots drift idly; a beat may hard-cut to a contrast bg and enter with an RGB-split glitch stretch that snaps sharp.
  - _Variant — Hook (triptych)_: beat 1 may be non-text — a `[logo mark]` rotates in 3D and snaps flat beside a `[version tag]`, or a statement resolves via a horizontal stretch/slice glitch on a subtle `[grid card]` — holds, then clears (scale-down + fade, or hard cut).
  - _Variant — Problem_: centered `[pain line 1]` reveals in chunks across one or two lines with its `[accent]` underline / particle burst.
  - _Variant — Problem (relay)_: `[hook phrase 1]` scale-pops into center with a quick spring on a flat solid OR drifting-gradient field — optionally the background itself morphs open first (a rounded `[accent shape]` expands into the full-bleed gradient); as the phrase holds, its word-spacing spreads slightly.
  - _Variant — Product_Intro_: bold `[hook word, e.g. "Introducing"]` enters with a typographic accent (split-and-slide apart, drawn underline, or `[accent]` selection-box).
  - _Variant — Product_Intro (fixed-line)_: the full fixed headline `[fixed phrase] [swap-slot]` parks centered (a faint `[plexus / ambient pattern]` may drift behind); no escalation move — the slot is the show.
  - _Variant — Product_Intro (word-run)_: a field-claiming open — horizontal `[brand color]` stripe wipes reveal the `[logo lockup]` then clear, or a giant blob expands from center repainting the frame in the brand color — before the sentence starts building.
  - _Variant — Product_Intro (wordmark transform)_: "Introducing" fades in over ambient sine-wave lines that undulate then snap taut, OR the `[old version wordmark]` holds and swaps away, OR oversized scattered `[gradient]` letters bounce-assemble into the `[name]` while the whole word scales down to center.
  - _Variant — Brand_Outro_: optional single-frame flash of `[product UI / hero asset]` precedes the verb channel, then `[verb 1]` hard-cuts in centered.
  - _Variant — Brand_Outro (relay-to-URL)_: optional prologue — the `[product UI window]` scrolls its content, then scales down and fades out to the flat canvas; the first text beat fades/scales in centered.

- **Scene 2..N — beats replace each other in place (the engine).** The center anchor advances one beat at a time; nothing from the prior beat lingers. Choose the swap mechanism by sub-shape:
  - **Sub-shape A (fixed-line token swap)**: the line stays fixed and only the variable slot changes by an instant hard CUT (no roll/scroll/blur) — `[token A]` → `[token B]` → `[token C]` — OR the final word(s) backspace out and a new word retypes (`[word A]` → `[word B]`). The rest of the line holds. The cycle may run a rapid `[role word]` list at the fixed slot, and the delete-retype may be performed by a labeled collaborative cursor; a faint `[plexus / ambient pattern]` may keep drifting behind the fixed line.
  - **Sub-shape B (multi-beat statement build)**: each full-screen beat hard-cuts to a NEW background/line, and each gets its own distinct entrance/exit MOVE — springy scale-in/scale-out overshoot, 3D letter-tumble (glyphs scatter into a rotating depth cloud, then reassemble into the next phrase), motion-blur fly-in that resolves sharp at center, prior text accelerates/zooms past the camera while fading, letter-spacing collapse, or a bottom-up masked slide. Background may hard-flip `[bg A]`↔`[bg B]` on selected beats with `[type color]` inverting to stay legible.
  - _Variant — Hook (escalation)_: beat 2 `[beat 2 text]` (more emphatic) snaps in; beat 3 `[beat 3 text]` (climax) holds, then a transition-out move on the type itself — a Z-dolly forward THROUGH an oversized glyph, OR a per-word karaoke highlight sweep lighting words left→right.
  - _Variant — Hook (triptych)_: a mid beat may be non-text — a `[CTA button]` spring-pops with overshoot, fires a one-shot blurry glow-ring pulse outward, and settles smaller — the element alone on screen, then cleared like any other beat.
  - _Variant — Problem_: each `[pain line k]` enters by chunk-reveal or motion-blur fly-in as the prior blurs/zooms off; an optional `[accent color]` interstitial word ("[what-if hook]") scales up from center, holds, then zooms past the camera and fades.
  - _Variant — Problem (relay)_: each `[phrase]` scale-pops into center while the prior shrinks and split-slides off toward BOTH left/right edges (clipping off-screen) with fade; an optional emphasis beat lands on a hard-cut contrast bg — a single `[word]` letter-tracking-tightens from wide spacing while scaling up as four thin `[accent]` arrows shoot in diagonally from the corners, converging on it; a left-aligned line-by-line value build may interleave.
  - _Variant — Product_Intro_: each `[tagline phrase]` is a hard-cut/push-through inverted-text beat with its own one-shot accent (strike-through, slider/toggle shapes sliding in, or a bg-invert cycle white→`[accent]`→black flipping fg/bg).
  - _Variant — Product_Intro (word-run)_: the `[sentence]` builds word-by-word with snappy pops (lines re-center as they add; an underline may draw beneath key words), then one beat per `[hero word]` — each lands large and performs its own one-shot effect: a letter-scramble resolve (with thin divider ticks), a chromatic-glitch jitter (offset color copies snapping back clean), a spring bounce + confetti burst that erupts up and drifts down, or a letter-slot swapped for a springing `[emoji / mark]` that morphs; the finale may run an alternating huge/small word scale chain.
  - _Variant — Product_Intro (wordmark transform)_: the `[wordmark]` completes in place — staggered part-by-part pop (`[part 1]` then `[part 2]`), an in-place swap replacing "Introducing", or a `[second phrase]` appending — with a gradient hue-sweep across the type that settles to a solid color snap.
  - _Variant — Benefits_: high tempo (~0.4s/beat) — each `[benefit phrase]` pops via springy scale-in/out or 3D letter-tumble; multiple bg light↔dark flips across the run with text-color invert.
  - _Variant — Benefits (statement relay)_: low tempo — each `[statement]` builds by its own engine and HOLDS ~1.5s+ before the hard cut: line 2 types char-by-char under a static line 1; an oversized `[phrase]` element-scrolls right→left through the frame (a moving window onto a wider line, a gradient sweeping the letters); a solid `[word]` holds while stacked outline-only echo copies cycle vertically behind it; a multi-line block builds fast as small `[accent shapes]` fly in from the edges then drift outward and thin (text may form as a masked grey fill, then snap solid).
  - _Variant — CTA_: each `[value line]` → `[value line]` → `[CTA verb line]` clears by hard cut / zoom-blur cut through near-black / fade-out, then the next pops/fades/slides in. Optional `[accent motif]` draws on behind (rising line-graph trim-path, thin wireframe guides, gutter geometry tiles).
  - _Variant — CTA (beat-chain)_: individual beats carry their own gag — a line enters right and marquee-scrolls continuously left across the frame (exiting); a `[use-case word]` list flash-swaps in place; a beat's letters briefly extrude into simple 3D and flatten back; a `[glyph + prop]` group spring-bounces in then slides off; ONE mock `[compose-window / product UI]` beat may interleave without breaking the chain.
  - _Variant — Brand_Outro_: a centered single `[verb / keyword]` HARD-CUTS to the next at a steady ~0.2s cadence (no fade/scale) over a continuous moving field (see camera modifier).
  - _Variant — Brand_Outro (relay-to-URL)_: 2–3 full-frame beats swap wholesale at a relaxed cadence — each fades/scales in and out, or scales up slightly then spring-shrinks to 0%, or an `[icon]` bounce-pops in from 0% and shrinks back out, or a `[title card]` holds with a continuous in-text horizontal gradient sweep before a HARD CUT to the bare canvas.

- **Scene N (final beat → end) — resolve and HOLD.** The last beat lands and holds to the end (settle only, no further scale-out). Resolution diverges by role:
  - _Variant — Hook (flash)_: last token swap lands and holds; optional tiny punctuation/emphasis snap (`?` → `?!`, or fill snaps to `[accent color]`).
  - _Variant — Hook (escalation)_: resolve on `[payoff bg]` — a `[payoff element]` (colored square / heart-eyes reaction emoji) SPRING-POPS in center; small `[accent motes]` drift outward; subtle settle.
  - _Variant — Hook (logo reveal)_: the word beats resolve on the brand — the `[logo]` pops in whole, or floating 3D `[shapes]` assemble and FLATTEN into the flat 2D mark as the `[wordmark]` slides in beside it; then a `[browser mockup / value card]` slides/scales in on a fresh bg and holds (a bottom caption may build).
  - _Variant — Hook (triptych)_: the final beat may be non-text — a `[benchmark chart]` fades in its framework and grows bars from zero width in a top-down stagger (the `[hero row]` bold/highlighted), then holds static for the back half of the shot; or a closing statement glitch-reveals and holds.
  - _Variant — Problem_: final `[pain line]` reveals (left→right swipe with leading-edge blur, OR letters explode radially then the resolving line fades up); holds the pain on screen.
  - _Variant — Problem (relay)_: the climax `[word]` scales in with special treatment (gradient fill, slight ~-8° rotation) and holds — OR the question resolves on a `[product surface]` as an ELEMENT move: a `[pill / search bar]` slides in from the right and keeps traveling leftward while its text progressively reveals (may end mid-slide, phrase cropped at the frame edge), or the `[page canvas]` scales down while `[app chrome + side panels]` slide in and frame it.
  - _Variant — Product_Intro_: resolve on the brand — `[logo mark]` / `[wordmark]` pops in centered (optional sting: liquid/ink splash, blob backing), OR the final value word holds inside an expanding-iris `[accent]` circle that scales to fill frame and hard-cuts the closing word through it.
  - _Variant — Product_Intro (wordmark transform)_: with the completed `[wordmark]` anchored dead-center, a dense `[UI-screenshot collage]` rushes in and expands outward from behind the text toward the frame edges with parallax (fast pull-back feel), then clears quickly to a clean `[wordmark]` end card; OR one `[word]` morphs into a pulsing `[icon]` completing an icon+text lockup before the field dissolves to its inverse; OR the title rapidly scales up and zoom-blurs away as the next context fades in.
  - _Variant — Benefits_: the last `[benefit phrase]` arrives (optionally on the inverted bg) and SETTLES — does not scale/tumble back out.
  - _Variant — CTA_: land on the lockup — `[logo mark]` SCALES UP small→full and holds, OR a `[logo]`/`[url]` builds segment-by-segment beside its icon. End-card holds dead static.
  - _Variant — CTA (glow-preceded formation)_: the prior letters scatter/clear, a soft `[accent]` glow pulses on the empty field, and the `[logo mark]` FORMS out of the glow with the `[url]` wordmark below; holds to the final frame.
  - _Variant — Brand_Outro_: hard cut to the `[resolve word / brand keyword]` (longest, still centered); HOLDS ~0.5s while the background field keeps moving.
  - _Variant — Brand_Outro (relay-to-URL)_: the centered `[URL / domain]` (+ optional CTA line above) fades/scales in and holds — the LONGEST beat of the shot, ~40–75% of the runtime — optionally fading at the very tail.

**motion vocabulary**: hard-cut / flash word swaps; in-place token cycle (instant cut, no roll/scroll/blur); type-on with trailing blinking caret; backspace-and-retype; per-word staggered fade/blur reveal; big→small scale-down; springy scale-in/scale-out overshoot; 3D letter-tumble scatter-and-reassemble; motion-blur fly-in / blur-off; prior text zoom-through-camera; letter-spacing collapse; bottom-up masked slide; drawn-on `[accent]` underline / strike-through; particle/dot burst from text; `[accent]` selection-box frame; bg-invert hard-flip with text-color invert; karaoke per-word highlight sweep; radial letter-explode; expanding-iris circle wipe-to-next; final spring-pop payoff element (square / emoji / logo mark); drifting `[accent]` motes / ambient shapes; segment-by-segment URL/wordmark build; final-token punctuation snap; settle-and-hold; scale-pop phrase relay (prior shrinks + split-slides off both edges with clip-fade); letter-tracking tighten-from-wide while scaling; corner arrows converging on a word; gradient-fill / hue-sweep across type with settle-to-solid snap; in-text traveling gradient sweep; background shape morph-open into a full-bleed field; RGB-split / chromatic-glitch jitter; horizontal stretch/slice glitch reveal; letter-scramble resolve with divider ticks; confetti burst up-and-drift; letter-slot emoji/mark swap + morph; alternating huge/small word scale chain; color-stripe wipes / blob expand frame-repaint; oversized phrase element-scroll (moving window); right→left marquee scroll-through; stacked outline-echo copies cycling behind a solid word; full-frame repeating-word pattern on a rolling 3D wave; accent shapes fly-in then drift-out-and-thin; masked grey fill snapping solid; brief 3D letter extrude-then-flatten; spring-bounce glyph+prop drop-in; glow-pulse-preceded logo formation; 3D shapes assemble-and-flatten into the mark; logo-lockup 3D rotation-snap; one-shot glow-ring pulse; chart bars growing in a top-down stagger; labeled collaborative cursor delete-and-retype; in-place role-word cycle; ambient plexus/pattern drift; spring shrink-to-0 exit / bounce-in from 0%; scattered-letter bounce-assembly with baseline settle; staggered wordmark part pop; phrase append; word→icon morph with continuous pulse; UI-collage rush-out with parallax from behind anchored type; zoom-blur title exit; long-held URL end card.

**rule mapping**

- hard-cut / flash word swaps, in-place token cycle, whole-line state swaps at time thresholds → `discrete-text-sequence`
- type-on character-by-character + blinking trailing caret → `discrete-text-sequence` (text/typing state progression) + `context-sensitive-cursor` (caret blink/color-switch)
- backspace-and-retype final word(s) → `discrete-text-sequence` (typos/holds/backspace is explicitly in-scope)
- one short distinct phrase per beat / script-driven phrase windows / word-by-word tagline assembly → `dynamic-content-sequencing`
- percussive per-beat phrase entrances on a shared beat array (distinct entrance per phrase, steady cadence) → `kinetic-beat-slam` (best fit for the multi-beat statement-build engine and the ~0.2s Brand_Outro verb march)
- per-word staggered fade/blur reveal → `kinetic-beat-slam` (per-phrase/per-word distinct entrances); the soft-focus blur component → `depth-of-field-blur` (selective-focus blur on the off-focus words)
- big→small scale-down on a word; springy scale-in/scale-out overshoot → `spring-pop-entrance` (spring pop/settle) backed by `gsap-effects` for the plain scale tween
- 3D letter-tumble scatter-into-depth-cloud then reassemble → `depth-scatter-assemble` (glyphs scatter into a 3D depth cloud and reassemble into the next phrase; combine w/ `3d-text-depth-layers` for the extruded read, or `hacker-flip-3d` for an in-place per-char flip flavor)
- karaoke per-word highlight sweep synced across words → `asr-keyword-glow` (keyword glow+scale on a synced rail) OR `css-marker-patterns` (highlight sweep) — choose ASR-driven vs. static-timeline sweep
- drawn-on `[accent]` underline / strike-through / loop / scribble under key word → `css-marker-patterns` (highlight sweep / circle / burst / scribble / sketchout)
- particle/dot burst from behind text → `css-marker-patterns` (burst) backed by `gsap-effects`
- `[accent]` selection-box frame around a word → `css-marker-patterns` (circle/box marker) + `gsap-effects`
- bg-invert hard-flip (light↔dark / white→accent→black) with text-color invert → `discrete-text-sequence` (whole-text/state swap covers the synchronized fg/bg state change)
- letter-spacing collapse; bottom-up masked slide → `gsap-effects` (tween letter-spacing / masked translate) + techniques: per-word kinetic typography / clip-path reveal
- expanding-iris circle wipe that morphs the current word into the next at the same center → `scale-swap-transition` (morph two elements at same center)
- final spring-pop payoff element (colored square / reaction emoji / logo mark) → `spring-pop-entrance` (or `physics-press-reaction` for a weightier pop)
- drifting `[accent]` motes / ambient shapes / soft drifting gradient field beneath the type → `sine-wave-loop` (idle drift loop)
- segment-by-segment URL / wordmark build beside its icon → `discrete-text-sequence` (segment-by-segment state reveal) or `dynamic-content-sequencing`
- final-token punctuation / emphasis snap (`?`→`?!`, fill→accent) → `discrete-text-sequence`
- settle-and-hold final frame → `spring-pop-entrance` (settle phase) / static hold (no rule needed)
- motion-blur fly-in / blur-off / zoom-through-camera streak on type → `motion-blur-streak` (directional velocity blur on a fast fly-in / zoom-through; the heavy motion-blur smear resolves sharp at center)
- radial letter-explode (glyphs explode outward radially then resolve) → `depth-scatter-assemble` (radial per-letter explode-and-resolve is in scope alongside the depth-cloud scatter)
- 3D letter-tumble depth-cloud scatter-and-reassemble → `depth-scatter-assemble` (free tumbling depth-cloud that flies out and snaps back into the next phrase)
- scale-pop phrase relay → `spring-pop-entrance` (the arriving phrase) + `gsap-effects` (the prior phrase's shrink + split-slide clear toward both edges)
- letter-tracking tighten-from-wide while scaling → `gsap-effects` (letter-spacing tween — the inverse of the letter-spacing collapse mapped above)
- corner arrows converging on a word → `css-marker-patterns` (burst geometry with inverted travel — lines converge instead of radiate) + `gsap-effects`
- gradient-fill climax word / hue-sweep across type / in-text traveling gradient sweep → `gradient-text-sweep` (gradient tweened THROUGH letterforms — position/hue sweep with settle-to-solid snap, seek-safe)
- background shape morph-open into a full-bleed field → `card-morph-anchor` (uniform scale + borderRadius paint tween, then the field takes over)
- RGB-split / chromatic-glitch jitter; horizontal stretch/slice glitch reveal → `chromatic-glitch` (deterministic offset color-copy layers, jitter + snap-clean; covers the stretch/slice glitch reveal)
- letter-scramble resolve with divider ticks → `hacker-flip-3d` (the deterministic glyph-substitution decode, minus the 3D rotation)
- 3D shapes assemble-and-flatten into the mark; scattered-letter bounce-assembly → `depth-scatter-assemble` (scatter-to-clean-layout settle) + `spring-pop-entrance` (the bounce settle)
- logo-lockup 3D rotation-snap → `orbit-3d-entry` (the 3D flip-in entry, skipping the orbit phase)
- one-shot glow-ring pulse; glow-pulse-preceded logo formation → `ambient-glow-bloom` (single-pass bloom-and-fade) + `spring-pop-entrance` (the mark forming out of it)
- chart framework fade-in + bars growing from zero width top-down; radial gauge arc-draw + count-up → `stat-bars-and-fills` (+ `counting-dynamic-scale` for the ticking value)
- labeled collaborative cursor delete-and-retype; in-place role-word cycle → `discrete-text-sequence` + `context-sensitive-cursor` (the labeled-pointer look itself is oversized-cursor doctrine, not a rule)
- ambient plexus/pattern drift; accent shapes drift-out-and-thin → `sine-wave-loop` (finite drift) after a `spring-pop-entrance` arrival
- letter-slot emoji/mark swap + morph; word→icon morph with continuous pulse → `scale-swap-transition` (same-center morph) + `svg-icon-enrichment` (the icon's internal pulse)
- oversized phrase element-scroll; right→left marquee scroll-through → `gsap-effects` (linear translate of an oversized element through a static frame)
- stacked outline-echo copies cycling behind a solid word → `3d-text-depth-layers` (the offset echo stack) + `vertical-spring-ticker` (the vertical cycle)
- brief 3D letter extrude-then-flatten → `3d-text-depth-layers` (build the extrusion offsets, then collapse them)
- full-frame repeating-word pattern on a rolling 3D wave → flagged special — a 3D wave-mapped text field is out of rule scope; `sine-wave-loop` only drives the undulation oscillator
- alternating huge/small word scale chain → `kinetic-beat-slam` (distinct per-beat entrances on the shared beat array)
- color-stripe wipes → `gsap-effects` (masked translate tweens); blob expand frame-repaint → `card-morph-anchor`
- UI-collage rush-out with parallax from behind anchored type → `center-outward-expansion` (clustered-at-center → outward to final positions; vary per-tile rates/scales for the parallax read)
- spring shrink-to-0 exit / bounce-in from 0% → `spring-pop-entrance` (in) / `gsap-effects` `back.in` shrink (out)
- product-surface resolve (pill slide with progressive text reveal; canvas scale-down as chrome frames in) → `nudge-curve` (the slide that reveals during travel) + `gsap-effects` (coordinated scale + panel slides)
- zoom-blur title exit as an in-shot beat handoff → `motion-blur-streak`; as a scene-out into the next scene it belongs to the transition layer
- staggered wordmark part pop / phrase append → `spring-pop-entrance` + `dynamic-content-sequencing`

**camera modifier** (optional, layered over the flat shot; most variants are camera-locked)

- Slow continuous global zoom-in / uniform push-in running underneath the whole sequence (Problem, Brand_Outro) → `multi-phase-camera` (push phase) — gives parallax between the fixed type and a moving background field.
- Camera dolly/zoom forward THROUGH an oversized glyph along Z as a beat transition-out (Hook escalation, Product_Intro push-through) → `coordinate-target-zoom` (target the glyph center) or `multi-phase-camera` (push).
- Slow push-in on Scene 1 over a glowing `[motif]` (Hook escalation) → `multi-phase-camera` (push) or `coordinate-target-zoom`.
- Slow continuous card/scene scale-up running UNDER hard-cut beats (Hook triptych) — a push-in feel rendered as element scale on the scene group, never a real dolly → `multi-phase-camera` (push phase) or a plain `gsap-effects` scale tween.
- Note: the in-place token swap (sub-shape A) and most Benefits/Hook-flash/CTA variants are fully camera-static — the swap is the only motion.


<!-- ===== FILE: hyperframes/hyperframes-animation/blueprints/logo-assemble-lockup.md ===== -->

# logo-assemble-lockup — Logo Assemble → Lockup

**intent**: A brand mark / wordmark comes to exist on screen and resolves into a centered logo lockup — built from parts (elements assemble or orbit in, letters cascade, an outline draws on, or a camera pushes through negative space), spring-BLOOMED whole from zero on a cleared stage, MORPHED in one unbroken chain out of the preceding phrase / glyph, absorbed from a kinetic streak, or already assembled and settling as decorations clear — optionally extended into a final URL / CTA / end card.

**roles served**

- Product_Intro (from product-intro-logo-system-assemble): A wordless, premium brand STING — an abstract system of elements pulses / grows / orbits and assembles around a FIXED central logo, carried by one cinematic camera tilt; no copy, no UI.
- CTA (from cta-camera-push-lockup): The logo build is a LEAD-IN to the final ask — a 3D mark assembles + wordmark cascades, then a fast camera PUSH-THROUGH the mark's negative space streaks giant CTA letters past the lens and resolves on a `[url]` / `[CTA verb]` lockup.
- CTA (from cta-button-wordmark-build): The "draws-its-own-outline → wordmark-builds-letter-by-letter" sub-shape — a `[CTA button]` pill strokes its own glowing border, a diagonal-band WIPE flips the frame, and the `[wordmark]` types in beside a slash to land the lockup. Camera static.
- Brand_Outro (from brand-outro-assemble-logo-lockup): The closing mark — a formation of `[feature pills / UI elements]` CLEARS the stage off all four edges, then on the empty frame the `[logo mark]` draws itself on stroke-by-stroke and the `[wordmark]` reveals to complete the lockup, then fades out.
- Product_Intro (from brand-reveal-assemble-zoom): a context-then-focus reveal — a companion tagline TYPES out to set context, the hero mark pops in beside it, then the companion exits as the layout recenters and the camera pushes IN to a held close-up on the mark (wide composition narrowing to a tight focus).
- Product_Intro (from logo-parts-lockup-assembly): the literal parts build — `[icon parts]` (a glowing dot traces a circle, semi-circles scale up and overlap, strokes rotate in) converge into the `[brand icon]` center-frame on a flat / gradient field, the `[wordmark]` joins (± a `[badge pill]` pops onto the lockup), then a payoff beat: a stepped bottom `[subtitle rail]`, a big `[count-up stat]` over a faint asset grid, or the lockup clears and a `[product UI window]` scales in. Static frame, all element-level.
- CTA (from text-clears-mark-blooms-lockup): the text-clear BLOOM — centered `[serif tagline]` beats (word-by-word staggered fades) hold, then CLEAR themselves to a blank frame; the `[brand mark]` spring-blooms from ZERO at dead center, slides left as the `[wordmark]` reveals to its right, and the balanced lockup holds (near-)still. Constant warm flat bg, static frame.
- Brand_Outro (from phrase-morphs-into-lockup): the MORPH chain — a centered `[phrase]` mutates in place, then collapses / swaps into an `[intermediate glyph]` whose line panels fan-and-flip around a central pivot with visible motion blur (page-flip feel) and interlock into the `[geometric mark]`, which slides apart into the lockup. One unbroken chain of transformation, never a cut-and-replace assembly; the finished lockup holds dead static for the final ~40–50% of runtime.
- Brand_Outro (from lead-text-then-mark-assembles): the parts-arrive build — a `[hand-off line]` holds and departs, then the mark is BUILT from arriving parts (`[icon]` drops in, letters slide in one by one, terminal punctuation lands, a confetti burst pops and instantly shrinks) OR a `[pixel stack]` streaks into full-width multicolor stripes whose tail retracts and is ABSORBED into the pixel mark — finishing as a lockup or a full end card (`[icon tile]` + `[title]` + `[URL pill]` + store badges) held static.
- Brand_Outro (from `settled-lockup-reveal`): the null-assembly boundary — the `[lockup]` is on stage from frame one; `[satellite shapes]` drift outward and fade, an accent underline sweeps beneath the wordmark, and the `[tagline]` wipes in to complete it. Settle-and-reveal: no predecessor beat, no morph, no relay.

**duration**: ~4.4–11.0s (Brand_Outro ~4.4–7.3s · brand-reveal ~5s · CTA text-clear bloom 6.0–8.9s · Product_Intro ~7s orbit sting, 7.0–9.8s parts-assembly · CTA push/build 5.4–11.0s)

**shot structure** (one consolidated time-coded template; `[slots]` are product-agnostic)

- Scene 1 — clear / ignite (0.0–~1.0s): the stage is prepared for the mark to build into.
  - _Variant — Product_Intro_: opens on a clean `[light bg]` with faint concentric guide rings under a flat top-down view; rings PULSE and expand from center; mid-beat the bg crossfades `[light]→[dark gradient: hero→secondary]`, tiny seed dots appear along the rings, and the central `[logo mark]`'s glow IGNITES (mark is present from t=0, fixed, front-facing).
  - _Variant — CTA push_: on a `[bg gradient]`, the `[logo mark]` is settling in object space (a 3D mark with thin wireframe edge-guides + a faint bracket motif behind center); a very slow continuous camera push-in may already be creeping.
  - _Variant — CTA button-build_: on a `[dark grid bg]`, a rounded `[CTA button "label"]` pill rises / scales into center (a prior headline clearing off the top); its thin border DRAWS ON as an animated glowing outline STROKE, with a small `[accent]` comet / spark icon at its left edge.
  - _Variant — Brand_Outro_: a PRE-ARRANGED formation of `[feature pills / element grid]` (each `[icon]`+`[label]`) DISPERSES — elements slide outward from their laid-out positions and fly off all four frame edges (edge-clearing drift, NOT a center-origin burst), emptying the frame onto a clean `[bg]`.
  - _Variant — Product_Intro parts-assembly_ (from logo-parts-lockup-assembly): optional text hook — a centered "`[Meet product]`" line wipes away right→left — or straight into the build; on a flat / gradient `[bg]`, the first `[icon parts]` arrive: a glowing dot traces a clockwise circle, a gradient semi-circle scales up inside it, or the mark scales-up-with-rotate into center.
  - _Variant — CTA text-clear bloom_ (from text-clears-mark-blooms-lockup): a centered `[serif tagline / question]` (± an outlined `[badge pill]`) finishes a left→right word-staggered reveal in the first ~0.5–1s (each word passing light-grey→dark) and HOLDS; optional rolling word-by-word swap to a second `[availability line]`. Then the CLEAR: text exits — shrink-toward-center + fade, or word-by-word left-first fade-out — leaving a blank frame for a beat.
  - _Variant — Brand_Outro morph-chain_ (from phrase-morphs-into-lockup): a centered `[phrase]` completes or mutates in place (a vertical slot-machine word swap — one word exits up as its replacement rises from below, rest of the line fixed — or a word-by-word landing) and holds. Nothing clears: the phrase IS the raw material for the mark.
  - _Variant — Brand_Outro parts-arrive_ (from lead-text-then-mark-assembles): a centered `[hand-off line: tagline / "Brought to you by"]` holds on a flat canvas, then exits — slides straight down off-frame with fade, or fades away behind the incoming flourish.
  - _Variant — Brand_Outro settled-reveal_ (from settled-lockup-reveal): the `[lockup]` is already centered at t=0; `[satellite shapes]` drift slowly outward around it — an INVERTED clear: the decorations leave, the mark stays.

- Scene 2 — assemble the mark (~1.0–~Ys): the mark builds itself from parts.
  - _Variant — Product_Intro_: seed dots SCALE UP into flat `[accent]` shapes arranged on the rings; concentric bands ripple outward (tunneling feel) and the shapes begin to ORBIT / drift around the still-fixed center.
  - _Variant — CTA push_: the `[wordmark]` CASCADES out from behind the mark (letters left→right with overshoot) into the full `[brand lockup]`; the 3D mark may assemble in beats (a terminal detaches + pops as a spring dot, a part hinges-open-and-snaps-shut elastic). Optional beat: a `[cursor]` arcs in and "clicks" the wordmark, OR a frosted-glass pill holding an intermediate `[CTA line]` springs in while layered mark shells fan to the edges.
  - _Variant — CTA button-build_: a graphic WIPE flips the frame to `[contrast bg]` — a thin `[accent]` diagonal line sweeps in, swells into a full-frame diagonal BAND, then collapses to a small `[accent]` slash.
  - _Variant — Brand_Outro_: on the now-clear frame, the `[logo mark]` DRAWS ON via stroke (built arc-by-arc / segment-by-segment).
  - _Variant — Product_Intro parts-assembly_: the overlapping parts COMPLETE the `[brand icon]` (a second circle overlaps to close the orb; strokes interlock); the `[wordmark]` slides out from behind the icon or in from its right; a small `[badge pill]` pops onto the lockup.
  - _Variant — CTA text-clear bloom_: on the blank frame the `[brand mark]` scales up from ZERO at dead center with a snappy spring ease (slight overshoot, hint of rotation as it grows) — the whole mark at once, no parts.
  - _Variant — Brand_Outro morph-chain_: the phrase collapses / wipes horizontally into the mark, OR is instantly swapped at the same center for a line-art `[intermediate icon]` whose strokes split into panels that fan-and-flip around a central pivot with visible motion blur, interlock-settling into the `[geometric mark]`. Never a cut to the finished logo — the transformation must stay unbroken.
  - _Variant — Brand_Outro parts-arrive_: the mark is BUILT from arriving parts — the `[icon]` drops in from above, letters slide in one by one, terminal punctuation lands, a tiny confetti burst pops and instantly shrinks — OR a colored `[pixel stack]` pops in at a text edge, shoots horizontally stretching into full-width multicolor stripes, then the stripe tail retracts and is ABSORBED into the `[pixel mark]` (mask retraction).
  - _Variant — Brand_Outro settled-reveal_: an accent underline sweeps left→right beneath the `[wordmark]` — the only "build" this variant performs.

- Scene 3 — resolve to lockup (~Ys–end): the lockup completes and holds (Product_Intro / Brand_Outro) or is flown into / extended to a CTA (CTA variants).
  - _Variant — Product_Intro (the ONE camera move)_: the whole system smoothly TILTS from flat top-down into an angled isometric perspective (ease-in-out) with a slight zoom-out — flat shapes become luminous 3D forms, bands become glowing orbit lines, while the central `[logo mark]` does NOT tilt (stays 2D, front-facing, fixed). Camera eases to a stop; elements keep continuous orbit/drift (inner faster than outer); the mark holds its steady glow. Final settled frame.
  - _Variant — CTA push (the signature)_: a single fast CAMERA PUSH-THROUGH the mark's negative space / through the glass pill — heavy horizontal motion-blur, giant `[CTA]` letters streaking past the lens (cursor drops out). Resolves to the final lockup on a saturated `[bg]`: a `[url badge]` / `[CTA line]` revealed by a left→right WIPE carrying an `[accent]` leading edge (or a clean fade), with solid mark-shapes parallax-sliding in behind. Settles to a dead-static hold (slow zoom-out / settle).
  - _Variant — CTA button-build_: the `[wordmark]` BUILDS letter-by-letter to the right of the slash, landing on the final "`[slash] [WORDMARK]`" lockup centered on the new bg. Slow settle to static.
  - _Variant — Brand_Outro_: the `[wordmark]` reveals beside the drawn mark (slide / fade) to complete the `[lockup]`; the lockup holds, then fades to `[black / bg]`.
  - _Variant — Product_Intro parts-assembly (the payoff beat)_: the finished lockup holds while a bottom `[subtitle box]` steps through `[tagline fragments]` (swap-in-place); or a big `[count-up stat]` line lands over a faint background asset grid; or the lockup scales-down / fades and a `[product UI window]` scales up on the flat bg (its panel content may swap once). The build hands off to product proof.
  - _Variant — CTA text-clear bloom_: the mark slides a short distance LEFT while the `[wordmark]` reveals to its right (letter-by-letter / slide-out wipe with visible partial states); the balanced "`[mark] + [wordmark]`" lockup centers and holds, one member continuing an almost imperceptible slow scale-up through the hold.
  - _Variant — Brand_Outro morph-chain_: the mark slides left as the `[wordmark]` is pulled out rightward trailing a motion-blur streak, the pair decelerating into the centered lockup (± a `[sub-line]` fades in below). The hold is LONG — dead static for the final ~40–50% of runtime.
  - _Variant — Brand_Outro parts-arrive_: the lockup rests centered and holds; or the full end card completes — a rounded-square `[icon tile]` scales up behind the mark, the `[title]` fades in word-by-word, and a bottom row (`[URL pill]` + `[store badges]`) fades / slides up — then holds static.
  - _Variant — Brand_Outro settled-reveal_: the `[tagline]` reveals left→right below the wordmark; the satellites finish drifting out and fade; the lockup holds centered (at most a very slow global zoom-out, no pan).

**motion vocabulary**: ring pulse / expand; background crossfade (light→dark); glow ignite; seed-dot scale-up; continuous orbit / drift (inner faster than outer); single 3D perspective tilt (flat→isometric) + slight zoom-out around a fixed 2D anchor; 3D logo assemble (part detach + spring dot, clapperboard hinge / snap, shell fan-out); wordmark cascade with overshoot (letters left→right); button pill rise / scale-in; animated stroke-outline DRAW + glow (button border AND logo mark); comet / spark accent; diagonal-band wipe (sweep → swell → collapse-to-slash); letter-by-letter wordmark build; pre-formed grid DISPERSE off all four edges; logo-mark stroke-draw (sequential arcs / segments); fast CAMERA PUSH-THROUGH with motion-blur (CTA spine); continuous slow push-in / push-out; cursor arc-in + click; parallax shape slide-in; left→right URL/badge wipe with glowing leading edge; static / fade-out end-lockup hold; optional idle breathe on the held mark; glowing-dot circular path trace; part-overlap icon completion (semi-circles scale up + overlap); scale-up-with-rotate mark entrance; wordmark slide-out-from-behind-icon; badge pill pop onto the lockup; stepped subtitle swap-in-place (bottom rail); count-up stat tick over a faint asset grid; lockup shrink / fade → UI-window scale-up payoff; word-by-word staggered fade-through-grey (in, and left-first out); rolling word-by-word line swap; shrink-toward-center + fade clearing exit; whole-mark spring BLOOM from zero (overshoot + slight rotation); near-imperceptible continuous scale-up through the hold; vertical slot-machine word swap; horizontal phrase collapse / wipe into the mark; instant same-center text→icon swap; line-panel fan-and-flip morph around a central pivot with motion blur (page-flip feel); interlock-settle into the geometric mark; wordmark pull-out trailing a motion-blur streak; lead-line slide-down-off-bottom exit; icon drop-in from above; sequential per-letter slide-in + terminal punctuation landing; confetti burst pop-then-instant-shrink; pixel-stack pop at a text edge; horizontal streak-stretch into full-width stripes; stripe-tail retraction absorbed into the mark (mask retraction); rounded-tile scale-up enclosing the mark; bottom metadata row fade / slide-up (URL pill + store badges); satellite shapes outward drift + fade; left→right underline sweep; left→right tagline wipe-in.

**rule mapping** (per motion verb → `rules/<id>.md`)

- ring pulse / expand from center → `center-outward-expansion` (radiate from a shared center; reuse the 0→1 progress driver)
- background crossfade (light→dark gradient) → plain opacity/background tween via `gsap-effects` (no dedicated rule needed)
- glow ignite on the mark → `asr-keyword-glow` (envelope-driven glow on the brand element)
- seed-dot scale-up into shapes → `spring-pop-entrance` (scale-in pop; alt `scale-swap-transition` if dots morph into shapes)
- continuous orbit / drift around fixed center → `orbit-3d-entry` (flip-in then continuous elliptical orbit; center label = the fixed mark)
- single 3D perspective tilt (flat→isometric) + slight zoom-out → `multi-phase-camera` (scripted scale phases on a scene-wrapping camera, for the zoom-out) — see camera modifier; the FLAT→ISOMETRIC plane tilt of the whole stage is a CSS-3D perspective move (`techniques.md` CSS-3D, animating the stage's `rotateX`) — no exact camera rule for the plane-tilt, approximate via CSS-3D (closest reference is `orbit-3d-entry`'s "Tilted orbit plane" variation animated over time)
- fixed 2D anchor logo amid moving universe → no motion rule needed (static anchor; intentional — it's the absence of motion, the universe moves around it)
- 3D logo assemble — part detach + spring dot → `spring-pop-entrance` (spring pop, `back.out` overshoot)
- 3D logo assemble — hinge open / snap (clapperboard) → `hacker-flip-3d` (the 3D-rotate axis) + `techniques.md` CSS-3D (the elastic open-and-snap-shut hinge is an adaptation of the 3D-rotate)
- 3D logo assemble — shell fan-out to edges → `center-outward-expansion` (run outward from the mark center)
- wordmark cascade with overshoot (letters left→right) → recipe `gsap-effects` (per-element staggered slide) + `spring-pop-entrance` (the `back.out` overshoot per letter)
- button pill rise / scale-in → `spring-pop-entrance` (scale-in; alt `scale-swap-transition`)
- animated stroke-outline draw + glow (button border) → `svg-path-draw` (stroke-dashoffset draw) + `asr-keyword-glow` (the glow on the drawn stroke)
- comet / spark accent on button → `asr-keyword-glow` (small glow accent); motion path via `techniques.md` GSAP MotionPathPlugin (#9)
- diagonal-band wipe (sweep → swell → collapse-to-slash) → `techniques.md` clip-path reveal (#12, animate a `polygon(...)` diagonal across the frame; the swell-then-collapse-to-slash is the same clip-path reveal driven through grow→shrink keyframes)
- letter-by-letter wordmark build → `discrete-text-sequence` (smooth-slice / per-state build); recipe `gsap-effects` (typewriter / appending words)
- pre-formed grid disperse off all four edges → not a rule gap: a formation flying off-frame is an EXIT, and the pipeline forbids mid-video exits — the harness transition IS the exit (only the final frame may exit the stage). Treat this as transition-handled / final-frame-only rather than an in-scene motion rule. (If staged in-scene as a reveal-the-mark clear, it reuses `center-outward-expansion` run OUTWARD — center→target machinery interpolating formation→offscreen targets, out-easing.)
- logo-mark stroke-draw (sequential arcs / segments) → `svg-path-draw` (the canonical multi-segment stagger draw)
- wordmark slide / fade reveal beside drawn mark → `svg-path-draw` (its "brand-line fades in after stroke" tail) ; slide via `spring-pop-entrance`
- fast camera push-through with motion-blur → `multi-phase-camera` (a hard push phase) — see camera modifier; the heavy motion-blur streak itself → `motion-blur-streak` (directional velocity blur on the fast push-through)
- continuous slow push-in / push-out → `multi-phase-camera` (phase scale + drift)
- cursor arc-in + click on the wordmark → `cursor-click-ripple` (move → click → ripple); arc path via `techniques.md` MotionPathPlugin (#9)
- parallax shape slide-in behind lockup → `depth-scatter-assemble` (parallax depth slide-in of shapes at differing depths; pair with `3d-text-depth-layers` for the depth ordering)
- left→right URL / badge wipe with glowing leading edge → `techniques.md` clip-path reveal (#12, animate `inset()` left→right); the glowing leading edge → `asr-keyword-glow`
- static / fade-out end-lockup hold → no motion rule needed (terminal hold / opacity fade; intentional)
- idle breathe on held mark (optional) → `sine-wave-loop` (post-settle breathing)
- glowing-dot circular path trace → `svg-path-draw` (the traced circle draws on) + `techniques.md` MotionPathPlugin (#9) for the leading dot riding the path tip
- part-overlap icon completion / semi-circle scale-up → `spring-pop-entrance` (per-part scale-in; place parts at their final overlap positions from setup — the overlap IS the completed mark)
- scale-up-with-rotate mark entrance → `spring-pop-entrance` (add a rotation from-value to the pop)
- wordmark slide-out-from-behind-icon → recipe `gsap-effects` (x-slide) under a clip / overflow mask via `techniques.md` clip-path reveal (#12); z-order the icon above the sliding text
- badge pill pop onto the lockup → `spring-pop-entrance`
- stepped subtitle swap-in-place (bottom rail) → `discrete-text-sequence` (whole-state replacement at time thresholds); derive the windows via `dynamic-content-sequencing`
- count-up stat tick over a faint asset grid → `counting-dynamic-scale`; the faint grid is a plain opacity fade (no rule needed)
- lockup shrink / fade → UI-window payoff → `scale-swap-transition` (exit cluster shrinks + fades at center; window pops in with `back.out`)
- word-by-word staggered fade-through-grey (in / left-first out) → recipe `gsap-effects` (per-word staggered opacity + color tween). Deliberately a quiet FADE register — do NOT substitute `waterfall-entry` here; its binary-arrival doctrine is the wrong voice for this serif beat
- rolling word-by-word line swap → two overlapping `gsap-effects` word staggers at the same timeline position (old line out left-first, new line in left→right)
- shrink-toward-center + fade clearing exit → `scale-swap-transition` (its exit half; the entrance half is the bloom)
- whole-mark spring BLOOM from zero → `spring-pop-entrance` (single hero, `back.out` overshoot, slight rotation from-value)
- near-imperceptible continuous scale-up through the hold → no motion rule needed (one long linear micro-tween on the held lockup; intentional life-in-the-hold)
- vertical slot-machine word swap → `vertical-spring-ticker` (masked column, stepped tween — one word slot cycles, rest of the line fixed)
- horizontal phrase collapse / wipe into the mark → `scale-swap-transition` (same-center morph) with the collapse via `techniques.md` clip-path reveal (#12)
- instant same-center text→icon swap → no motion rule needed (`tl.set` hard swap; intentional — the chain's continuity lives in the NEXT beat's morph)
- line-panel fan-and-flip morph (page-flip, motion-blurred) → `hacker-flip-3d` (the per-panel 3D rotation axis) + `motion-blur-streak` (the blur) + `techniques.md` CSS-3D; true stroke-interpolation glyph morphs live in `hyperframes-keyframes` (SVG morph) — reach there if panels can't sell it
- interlock-settle into the geometric mark → `center-outward-expansion` machinery run INWARD (per-panel transform offsets tween to 0 in lockstep with one driver)
- wordmark pull-out trailing a motion-blur streak → `motion-blur-streak` (echo / ghost trail collapsing into the lead) on the x-slide
- lead-line slide-down-off-bottom exit → in-scene clearing beat; same doctrine as the grid-disperse row above (offscreen target + out-easing; prefer the harness transition when the exit IS the scene boundary)
- icon drop-in from above → `spring-pop-entrance` (y-offset from-value, overshoot on landing)
- sequential per-letter slide-in + terminal punctuation landing → `waterfall-entry` (staggered arrival cascade on a lateral axis; the punctuation is the cascade's final, heaviest beat)
- confetti burst pop-then-instant-shrink → `press-release-spring` ("release burst" variation) for a small deterministic burst; a true multi-particle confetti field → `particle-burst`
- pixel-stack pop at a text edge → `spring-pop-entrance` (tight stagger down the stack)
- horizontal streak-stretch into full-width stripes → plain `scaleX` stretch via `gsap-effects` (transform-origin at the stack) + `motion-blur-streak` for the streak read
- stripe-tail retraction absorbed into the mark → `techniques.md` clip-path reveal (#12) run in REVERSE (animated `inset()` retraction reading as mask absorption into the mark)
- rounded-tile scale-up enclosing the mark → `spring-pop-entrance` (scale-in BEHIND the mark; z-order only, mark never moves)
- bottom metadata row fade / slide-up → `spring-pop-entrance` (staggered group, ≤500ms cap)
- satellite shapes outward drift + fade → `center-outward-expansion` run OUTWARD (drift targets past frame edge) + opacity tail; if the drift must idle first, seed it with `sine-wave-loop`
- left→right underline sweep → `css-marker-patterns` (highlight sweep re-skinned as an underline) or `stat-bars-and-fills` progress-fill `scaleX`
- left→right tagline wipe-in → the existing "left→right URL / badge wipe" row applies unchanged (clip-path `inset()`)

**camera modifier** (the push / tilt)

- **CTA push-through** (the CTA spine): a scripted hard zoom phase on a scene-wrapping camera → `multi-phase-camera` ("Steady push" / "Bookend pull" pattern; push phase = the climax). When the mark is OFF-center and the camera must fly through a specific point of negative space, combine with `coordinate-target-zoom` (outer scales, inner counter-translates so the target negative-space point lands at viewport center as scale ramps; measure the offset at setup). The signature heavy horizontal MOTION-BLUR on the streak → `motion-blur-streak` (directional velocity blur on the push); realize with a CSS `filter: blur()` / duplicated-streak layer on the camera during the push window.
- **Product_Intro tilt** (the one cinematic move): the flat→isometric perspective tilt + slight zoom-out is a single scripted camera beat → `multi-phase-camera` (scale phase + the "Targeted zoom into off-center element" / drift machinery) for the zoom-out. `multi-phase-camera` is scale+translate+drift only, so the perspective-PLANE rotateX (flat top-down → angled isometric) of the whole stage is the CSS-3D move noted above — approximate via `techniques.md` CSS-3D, animating the stage's `rotateX` (closest reference is `orbit-3d-entry`'s "Tilted orbit plane" variation animated over time).
- **Static-frame variants**: the parts-assembly, text-clear bloom, morph-chain, parts-arrive, and settled-reveal variants are all COMPLETELY static-frame (element-level motion only; settled-reveal tolerates at most a very slow global zoom-out). The camera modifier applies only to the CTA push and the Product_Intro tilt.


<!-- ===== FILE: hyperframes/hyperframes-animation/blueprints/overwhelm-surround.md ===== -->

# overwhelm-surround — Overwhelm / Close-In

**intent**: Convey overwhelm by accumulation. Recognizable subjects assemble, density markers scatter in to amplify "look how much," then the central subject morphs into the viewer's own avatar and elements close in from ALL sides — the frame feels surrounded, not zoomed-into. The emotional arc is recognition → claustrophobia.

**roles served**

- Problem (from `problem-mockup-overwhelm`): when the problem beat must first show "too many tools / too much surface area" and then put **the viewer inside it** — a literal swap of subject (product → person) followed by a closing-in that feels invasive. Reach for it when the pain is "you're buried," not "this metric is bad" (that's `dataviz-countup`).
- Problem (from `desktop-clutter-accumulation`): when the overwhelm is a **workspace**, not a tool
  count — live windows, stickies, and alert toasts pile up until the frame is chaotically full, and
  the beat resolves not by closing in but by shoving the clutter aside and asking the question.
  Reach for this variant when the pain lands on words ("how can you X… when you spend months on
  Y?"), not on a surrounded avatar.

**duration**: 6–9s (clutter-shove-to-question variant ~10s)

**shot structure** (a `[bg]` canvas; recognizable surfaces first, the viewer's avatar revealed underneath, then a radial crowd)

- **Scene 1 (0.0–~1.6s) — recognizable assembly.** Three `[product mockups / surfaces]` assemble into something the viewer knows — staggered scale-in, the **center** one full-size, the two flanks smaller (~0.86). Each rides a low-amplitude float so they feel like live context, not a static collage. Camera static.
- **Scene 2 (~1.6–3.0s) — density amplifies.** `[platform icons / logos]` scatter in around the mockups (staggered), used purely as **density markers** — "look how much surface area," not animated dials.
- **Scene 3 (~3.0–4.6s) — the morph (signature move).** The CENTER mockup MORPHS: its content fades out, the container reshapes, and the viewer's `[avatar]` is revealed **underneath** — a literal swap of subject, product → person.
- **Scene 4 (~4.6–end) — close-in.** `[task bubbles / demands]` close in from ALL sides toward the avatar (radial staggered entry). The avatar **stays put** while the bubbles invade — the claustrophobia comes from being surrounded, never from a camera push. Holds on the crowded state.
- **Variant — clutter-shove-to-question** (replaces Scenes 3–4 and
  inverts the camera contract — see modifier): accumulation runs under a **slow steady zoom-out** —
  `[sticky notes]` bounce in springy, `[dashboard / editor windows]` pop and slide up, a stack of
  `[alert toasts]` slides in at one edge, inner content keeps typing / log-scrolling as live density,
  windows overlap until the frame is chaotically full. The camera then REVERSES into a quick
  push-in that **shoves the clutter to the frame edges**, opening central negative space where a
  `[two-part serif question]` builds word-by-word (line 1 swaps in place to line 2); a `[cursor]`
  glides in from off-frame and comes to rest under the text; a very slow forward creep and hold.
  No morph, no avatar — the question is the payoff.

**motion vocabulary**: staggered scale-in assembly; resting-scale-preserving low float; density-marker icon scatter; content-fade → container-reshape → reveal-anchor-beneath morph; radial close-in entry from all compass points; held crowded end-state. Clutter-shove variant: slow steady zoom-out under accumulation; reverse quick push-in; clutter
shoved to frame edges opening center negative space; continuous live typing / log scroll inside
windows as ambient density; toast-stack slide-in; word-by-word serif build with in-place line swap;
cursor glide-to-rest; very slow forward creep + hold.

**rule mapping**

- staggered mockup + icon entries (smooth settle onto their resting scale) → `spring-pop-entrance` (smooth-settle register) backed by `gsap-effects`
- platform icons as density markers (positions pre-baked, scale/opacity only — NOT internal-parts animation) → `svg-icon-enrichment` (its DOM contract only)
- center mockup → avatar morph (HF forbids `width`/`height` tweens → drive the reshape on `scaleX`/`scaleY`, anchor = the avatar layer rendered beneath) → `card-morph-anchor`
- radial bubble close-in (positions baked once via `cos`/`sin`, staggered entry) → `gsap-effects` (radial layout) + `spring-pop-entrance` (per-bubble arrival)
- low-amplitude float on background mockups/icons → `sine-wave-loop` (low-amplitude register — subtle jitter that composes onto each element's resting scale, never a `fromTo` yoyo that re-tweens to its start)
- (variant) zoom-out under accumulation → quick push-in → slow forward creep → `multi-phase-camera`
  (pull-back / push / drift as sequential phases on one world wrapper; counter-translate math in
  `viewport-change`)
- (variant) clutter shoved to the edges as the push-in lands → `center-outward-expansion` (outward
  vectors to edge resting positions), fired at the same timeline position as the camera push so the
  shove reads as CAUSED by it (`reactive-displacement` register)
- (variant) word-by-word serif question build → `gsap-effects` (staggered word reveal); the
  in-place line-1 → line-2 swap → `discrete-text-sequence`
- (variant) live typing inside windows → `gsap-effects` (typewriter); the continuous inner
  log-scroll — composition: looping content translateY via `gsap-effects` (masked)
- (variant) cursor glide-in coming to rest → `cursor-click-ripple` (approach portion only — no click)

**camera modifier**: camera-static — the close-in must read as the world crowding the subject, so the frame holds; a push-in would convert "surrounded" into "zoomed-into" and kill the claustrophobia. The clutter-shove-to-question variant is the sanctioned exception: there the camera IS the
storyteller (zoom-out ↔ push-in via `multi-phase-camera`), and the claustrophobia comes from
accumulation, not surround — never mix the two resolutions in one shot.


<!-- ===== FILE: hyperframes/hyperframes-animation/blueprints/panel-edit-live-sync.md ===== -->

# panel-edit-live-sync — Panel Edit, Live Sync

**intent**: A bipartite stage — an inspector/editor **panel bound to a target surface** — where a cursor (or text caret) continuously manipulates a control (value scrub, unit/codegen dropdown pick, knob or easing-handle drag, inline retype) and the coupled surface updates **live, in the same beat**: the page button rotates as the value scrubs, preview icons resize per keystroke, the hex readout mirrors every hover, the code block converts on the pick. The motion IS the causality — one gesture, two surfaces changing in the same frame. The camera's job is co-visibility of the couple, not a chase.

**provenance** (7 mined Key_Feature goldens across 4 products, both dialects — three sync modes):

- _Write-sync (control → target)_ — the anchor mode: a visual-editor panel scrubs rotation/margin/padding while the live page button rotates and shifts in the same beat (plus unit + font-weight dropdown picks); an inline `className` retype in a glowing code callout resizes the preview icons per keystroke (caret-as-actor, push-in/pull-back roundtrip that must keep BOTH surfaces in frame); a motion editor drags a knob along a dotted motion path and bends easing handles into an S-curve, paying off with a big zoom-out where the finished toggle PERFORMS the edited ease (deferred payoff).
- _Read-sync (target → panel mirror)_: clicking a page button pops a toolbar → "Copy code" → the code editor fills with the element's CSS under one continuous slow zoom-out; hovering palette swatches live-updates a footer hex readout while the grid scrolls.
- _Self-conversion (panel is both control and target)_: unit dropdown conversions inside a 3D-tilted spacing panel snap-convert values in place (rem→px→%, `0,375 rem` → `6 px` → `4,871 %`); a codegen dropdown picks SwiftUI and the CSS block crossfades into SwiftUI under a rapid punch-in.

> **Concentration caveat**: 4 of 7 members are one video (CSS Scan Pro 2.0). The COUPLING engine is independently attested by 3 more products across 3 more videos and both dialects (Figma Dev Mode, Figma motion editor, bolt.new), each on a different surface pair — page+inspector, canvas+timeline+easing panel, IDE code+app preview — so the shape is real, not one film's house style. What IS CSS-Scan-Pro house style (marked optional below): the dark-slate capability title-card prelude, the oversized black cursor with white outline, the green success-checkmark flip, flash tooltips. Trigger is product-conditional: reach for this shape when the feature itself is live editing/inspection.

**roles served**

- Key_Feature (from `panel-edit-live-sync`, all 7 cases): one capability demonstrated as 2–4 edit beats on a single bound element — each beat a continuous manipulation the coupled surface answers in real time, resolving on the last edit held, a zoom-out to the finished product performing the edit, or a callout landing on the result. Three sub-shapes fold in:
  - **(A) write-sync** — cursor/caret edits a control; the TARGET transforms live (rotate/shift/stretch/resize/re-animate).
  - **(B) read-sync** — cursor selects/hovers the target; the PANEL readout mirrors live (CSS streams in, hex footer updates).
  - **(C) self-conversion** — the edit transforms the panel's own readout (units snap-convert, CSS crossfades to SwiftUI).

**duration**: 5.3–11.9s (read-sync hover demos shortest ~5.3s; multi-beat scrub/edit runs 8.7–11.9s)

**shot structure** (a `[target surface — webpage / design canvas / IDE + live preview]` sharing the frame with a `[bound panel — floating inspector / docked code panel / timeline + easing editor]`; a `[cursor or caret]` is the actor; every beat pairs ONE manipulation gesture with a SIMULTANEOUS response on the coupled surface; selection chrome declares which element is bound; camera ranges locked → active but always preserves the couple)

- **Scene 0 (optional, 0.0–2.0s) — capability title card.** Solid dark `[slate/charcoal]` card; a single white line names the capability (`"Edit CSS visually"`, `"Auto measurement units conversion"`, `"Check color palettes"`) — fades/drifts in, holds, then a HARD CUT or a fast motion-blurred zoom-out that settles the stage. (CSS-Scan-Pro-house-leaning; 071/017/080 open cold on the stage, 071 instead springs a giant lowercase `[verb word]` over the preview.)

- **Scene 1 (~1–3s) — the couple establishes.** The `[target surface]` arrives with the `[bound panel]` docked, floating in subtle 3D tilt, or SLIDING IN from an edge. Selection chrome pops on to declare the binding: `[bounding box + corner handles / red dashed inspection guides / redline measurement chips popping sequentially / green class-name header]`. The cursor enters and glides to the first control.

- **Scene 2..N (~2s each) — edit beats, gesture + mirror in the same frame (the engine).** Each beat is ONE continuous manipulation and its live answer:
  - _Variant — write-sync (A)_: the cursor CLICK-AND-DRAGS a numeric field (value counts up/down: `0°→-10°`, `0→38 px`) while the target `[button/element]` rotates/shifts/stretches in real time; OR drags a `[knob along a dotted motion path / easing handle bending the curve, coords readout updating]`; OR a caret INLINE-RETYPES a value (`1xl→4xl→2xl`) inside a `[glowing magnifier callout]` while `[preview elements]` resize per keystroke. A flash `[tooltip]` may name the gesture.
  - _Variant — read-sync (B)_: the cursor CLICKS/HOVERS the target element — a `[floating toolbar]` springs up above it, a menu pick fires (`Copy code` → icon flips to a green checkmark) and the `[code editor]` fills with streaming CSS; or hovered `[swatches]` outline and the `[footer hex]` updates instantly per hover as the grid scrolls.
  - _Variant — self-conversion (C)_: the cursor clicks a unit/codegen `[dropdown]` — it opens with hover-highlighted rows + checkmark — and on the pick the readout SNAP-CONVERTS in place (`rem→px`, value recalculates) or the whole `[code block]` crossfades to the new language, heading flipping (`Layout`→`HStack`).
  - Camera per beat: LOCKED wide holding both surfaces; or a PUNCH-IN to the acting surface (panel scroll reveals the next section) — but during a write-sync edit both gesture and mirror stay co-visible (071's law: the push-in never crops the preview out).

- **Scene N (final beat → end) — the edit proves out, HOLD.** Resolution diverges:
  - _Variant — last edit held_: the final pick lands (`100 - Thin` selected, `4,871 %` applied) and the state simply HOLDS — never end on the tooltip with the dropdown unopened.
  - _Variant — payoff zoom-out_: a big zoom-out reveals the finished product PERFORMING the edited parameter — the toggle slides with the new ease inside the full phone mockup, confetti drifting; or the pull-back returns to the identical full framing while a `[terminal]` appends an hmr line.
  - _Variant — callout lands_: a large `[arrow callout]` slides in pointing at the result / the export menu rests open under the cursor; frame drifts subtly outward.

**signature move**: the **live-sync couple** — a scrubbed/typed/dragged control and its bound surface changing simultaneously, in-frame together, every edit beat.

**motion vocabulary**: click-and-drag value scrubbing with live target sync (rotate / shift / stretch); per-keystroke live preview resize; inline retype with backspace + blinking caret; instant value snap-conversion; live hex/readout mirror on hover; unit/codegen dropdown with hover-highlight rows + checkmark, instant open/close; font-weight/dropdown row pick; knob drag along a dotted motion path with waypoints; easing-handle drag bending the curve (coords readout updating); playhead scrub; redline measurement chips popping sequentially; bounding box + corner handles; red dashed inspection guides; floating toolbar springs up above the selected element; code panel slides in from an edge; in-panel scroll to a new section; swatch-grid scroll; syntax-highlighted code streams/pastes in; code crossfade (CSS→SwiftUI) with heading flip; glowing magnifier callout over a code token; icon flips to green success checkmark; flash tooltip naming the gesture; oversized black cursor with white outline; grab-cursor drag; dark title-card prelude + hard cut; fast motion-blurred zoom-out settle; ONE continuous slow zoom-out spanning a demo shot; eased push-in → hold → eased pull-back roundtrip; quick punch-in to panel/timeline/code; subtle 3D tilt drift/parallax on a floating panel; big zoom-out to the product payoff; result element re-animates with the edited ease; confetti drift; terminal log append; large arrow callout slide-in; static hold.

**rule mapping**

- cursor glide to a control, presses, click feedback → `cursor-click-ripple`
- cursor state flips pointer↔grab over a scrubbable field / draggable handle → `context-sensitive-cursor`
- scrubbed numeric readout counts up/down under the drag → `counting-dynamic-scale`
- **the live-sync couple itself** (control gesture drives a second element's property in the same beat) → `control-target-sync` (concurrent tweens at the SAME timeline position — readout tween + target transform tween sharing one label)
- inline retype with backspace, typos, holds / keystroke thresholds → `discrete-text-sequence` (+ `context-sensitive-cursor` for the caret blink)
- per-keystroke preview resize → `discrete-text-sequence` (keystroke state thresholds) + `control-target-sync` (the coupled scale steps)
- instant value snap-conversion / hex readout swap / heading flip (`Layout`→`HStack`) / status text → `discrete-text-sequence`
- syntax-highlighted code streaming/pasting in, terminal log append → `discrete-text-sequence` (bulk additions are explicitly in-scope)
- dropdown/menu pops open; floating toolbar springs up; tooltip flash; redline chips pop sequentially (staggered, ≤500ms) → `spring-pop-entrance`
- dropdown row hover-highlight stepping and pick sequencing / which edit beat shows what → `dynamic-content-sequencing`
- dashed inspection guides / selection outline draw on → `svg-path-draw`; dotted motion path with waypoints → `svg-path-draw` (the path display)
- knob TRAVEL along the motion path → path following — see `hyperframes-keyframes` (paths)
- easing-handle drag bending the curve (SVG `d` interpolation) → SVG path morph — see `hyperframes-keyframes` (morph; `svg-path-draw` only draws strokes, it cannot morph a path); coords readout beside it → `discrete-text-sequence`
- glowing magnifier callout over a code token (incl. the live enlarged duplicate of a UI token) → composition: `ambient-glow-bloom` (the glow) + `spring-pop-entrance` (the callout pop)
- code panel slides in from an edge / panel docks → `card-morph-anchor` / `scale-swap-transition` (per cursor-ui-demo precedent for panel slide-in)
- code block crossfade CSS→SwiftUI; success-icon flip to green checkmark → `scale-swap-transition` (state swap at the same anchor)
- in-panel scroll / swatch-grid scroll (masked internal translate) → `gsap-effects`; on a 3D-tilted panel → `3d-page-scroll` (tilted plane w/ internal scroll)
- subtle 3D tilt drift/parallax on the floating panel; continuous micro-drift on holds → `multi-phase-camera` (micro-drift phase)
- punch-in to panel/timeline/code and settle → `coordinate-target-zoom` + `multi-phase-camera`
- eased push-in → hold → eased pull-back roundtrip (co-visibility preserved) → `multi-phase-camera` (pull-back / focus / push sequencing)
- ONE continuous slow zoom-out spanning the demo shot; big zoom-out to the product payoff → `viewport-change` (single `.world` composite transform)
- fast motion-blurred zoom-out settle transition → `motion-blur-streak` + `viewport-change`
- result element re-animates with the edited ease (toggle slides with the new S-curve) → `gsap-effects` (custom-ease tween on the payoff element)
- confetti drift on the payoff → `particle-burst` (deterministic confetti) + `sine-wave-loop` (bounded drift)
- large arrow callout slide-in + hold → `gsap-effects` (single slide tween)
- dark title-card prelude (capability line fades/drifts in, hard cut out) → cross-blueprint: `titlecard-reveal` territory; the drift/fade itself → `gsap-effects` — EXIT-N/A as a mapped rule here
- hard cuts between title and demo; final static hold → EXIT-N/A (transition registry / no rule needed)

**camera modifier**: The camera law is the INVERSE of cursor-ui-demo's chase: it serves **co-visibility of the couple**. Three attested postures — (1) LOCKED: fixed framing for the whole demo, panel + target both in frame, all motion element-level (CSS_39.0, CSS_102.8 after settle); (2) ONE CONTINUOUS MOVE: a single slow zoom-out (or drift) spanning the entire demo shot while edits fire inside it (CSS_10.9, CSS_63.5's tilt-drift) → `viewport-change`; (3) PUNCH-AND-RETURN: eased push-in onto the acting surface, tight hold through the edit, eased pull-back to the identical opening framing (071_bolt, 080_figma, 017_figma) → `multi-phase-camera` + `coordinate-target-zoom` — with the hard constraint that during a write-sync edit the mirror surface is never cropped out. If the camera is chasing the cursor target-to-target with per-beat state swaps, you're in `cursor-ui-demo`, not here.


<!-- ===== FILE: hyperframes/hyperframes-animation/blueprints/prompt-type-submit-generate.md ===== -->

# prompt-type-submit-generate — Prompt, Submit, Generate

**intent**: The AI-era demo shot — a `[prompt / query / command]` types character-by-character into a REAL product input (chat composer, search bar, terminal prompt, URL bar, sidebar assistant) and the machine answers: status theater into a streaming answer / agent action log / diff cards / chart / generated artifact — or the clip cuts at the submit and the ask itself is the show. The keyboard is the actor and the product is the responder. Distinct from `typewriter-reveal` (a line typed as bare typography on an empty field — no product surface, nothing answers) and from `cursor-ui-demo` (a cursor clicking a reconstructed UI through states — there the pointer drives every change; here any cursor work only primes the input or lands the submit, and every state change after that is the machine's own doing).

**roles served**

- Hook (from `app-window-push-in-prompt-typing`): when the opener is "watch me ask" — typed headline beat(s), ONE eased push-in lands tight on the product's input, the prompt types and the clip ends at / just after submission (sub-shape A).
- Hook (from `typed-command-output-scroll`): when the demo loop ITSELF is the hook — command in, output builds and scrolls, and a second command / retype starts before the cut, ending mid-action (sub-shapes B/C with the restart ending).
- Product_Intro (from `prompt-typing-composer`): when the first look at the product IS its composer — a brand beat opens onto the input surface, a long prompt types with hovers / attachments / dropdown picks, and the camera steers gently toward the input or the confirming control (sub-shape A, occasionally running through to an agent-log payoff).
- Product_Intro (from `search-query-walkthrough`): when the product is introduced through its search affordance — a short `[query]` types with a blinking caret, autocomplete / results populate LIVE, and a confirm click settles the result state (sub-shape C, search skin).
- Key_Feature (from `prompt-type-submit-generate`): when the capability is demoed as ONE prompt→response round trip — submit into thinking/status states, then a streaming answer, action-log rows with brand icons, green diff cards, a chart drawing itself, or an instant generated-app reveal (sub-shapes A/B/C — the family's widest role).
- CTA (from `install-command-end-card`): the install-command end card — the closing `[headline]` DEMOTES (shrinks, grays, lifts) to make room for a `[terminal pill]` that springs in and stretches wide, the `[install command]` types out with a blinking cursor, flanking metadata and a `[tool-icon row]` pop in, and the finished card holds long. No submit, no response — the typed command IS the ask (sub-shape A, terminal skin).

**duration**: 5.2–12s (A prompt-as-hook 5.2–12s, incl. the ~7.4s CTA end card; B full generate loop 5.45–11.9s; C instant-result surface 5.7–11.9s — a long-form family: most members run 7–12s because the response needs room to arrive)

**shot structure** (a `[product input]` on/inside a `[product surface — app window, web page, terminal, browser chrome, sidebar]` over `[bg color]`; the input is the gravitational center — the camera makes at most one or two purposeful moves toward or away from it and is otherwise LOCKED; typing is character-by-character behind a visible caret, and response content arrives progressively, never dumped; three folded sub-shapes — **(A) prompt-as-hook**: the clip ends at / just after the submit (or mid-word), the ask is the show; **(B) full generate loop**: submit → status theater → the output builds block by block; **(C) instant-result surface**: the machine answers with a finished surface, often re-queried before the cut)

- **Scene 0 (optional, 0.0–~2s) — lead-in beat.** ONE establishing move before the input owns the shot: a `[headline]` types on centered and clears; a `[title card]` hard-cuts away; a brand beat (`[logo/mascot]` centered, `[serif title]` building in word groups, logo shrinking-and-rising to dock top-center); an `[orb / mark]` forms with a glowing rim; the `[app window]` flies in with motion blur and settles; or a full-frame `[thumbnail grid]` parts at its vertical centerline to clear the stage. Keep it ≤2s — the input is the star.
  - _Variant — Hook_: typed headline beats carry the intro — "[Introducing X]" types on, holds, is replaced by the `[tagline]` typing in the identical style; the typing register is established before the product ever appears.
  - _Variant — Key_Feature_: the capability claim types as a bare title ("[Run a task across multiple models.]") then hard-cuts to the surface — or skip Scene 0 entirely and open on the live surface mid-workflow.
  - _Variant — CTA_: the `[closing line]` types on in two steps ("[Designed.] [Not generated.]") and holds — it will demote in Scene 2.

- **Scene 1 (~1–3s) — the input takes focus.** The `[product input]` arrives or is primed: a `[pill bar]` EXPANDS sideways from the mark/chip; a `[prompt palette / card]` SPRINGS in at center with a soft shadow; ONE smooth eased/accelerating push-in crops tight onto the composer inside the `[app window]` (headline chrome slides out of frame); a `[⌘K search modal]` springs to center while the page blurs behind it; a cursor clicks a `[menu row / Assistant button]` and the prompt block appears; or a `[✕ clear button]` empties the previous query back to `[placeholder]`. Optional composer ritual (pick 1–2, before or during typing): an `[attachment]` drags in and settles in a tray below the input; a `[model / option dropdown]` opens beneath the selector, rows hover-highlight, a checkmark lands and the toolbar label updates.
  - _Variant — Product_Intro_: the ritual is the introduction — a `[chip grid]` fades in and the cursor arcs across 2–3 hover highlights before clicking the one that opens the composer; the affordances are the tour.
  - _Variant — Key_Feature_: the surface already carries an old `[query]` and its previous `[result panel]` — clearing it says "this is a working tool, not a mockup".

- **Scene 2 (~2–6s) — the prompt types (the engine).** The `[prompt text]` types rapidly character-by-character behind a blinking caret; the input card GROWS downward / wraps as text fills, pushing footer controls and attachments down; a typed `[token]` may convert into an inline `[brand pill]` mid-typing (`[@browser]` → a colored `[Browser]` chip, typing continues around it); the camera may run ONE slow continuous push-in toward the input, decelerating to a near-hold on the typed ask. Sub-shape (A) may END here — cut mid-word with the caret blinking, or held on the finished prompt.
  - _Variant — Hook (A)_: the typed ask is the cliffhanger — end on the completed prompt, or on the submit click as the interface DIMS at the cut.
  - _Variant — Product_Intro (A)_: the camera dives toward the bottom input while `[option pills]` cascade in above it; the prompt is still mid-word at the cut — the product is introduced as something you talk to.
  - _Variant — CTA (A, install end card)_: the Scene-0 headline DEMOTES — scales ~50%, desaturates to gray, lifts upward — as a small `[$ chip]` spring-pops below and STRETCHES horizontally into a wide `[terminal pill]`; the `[install command]` types out inside it; a faint `[repo link]` and a "[Works with]" label fade in quietly; a row of `[tool icons]` pops in one after another with soft spring scale; the finished composition holds long, only the caret blinking.

- **Scene 3 (~4–7s) — submit + machine theater.** The `[submit control]` is clicked (cursor glide + press dip; the button may have MORPHED state on first keystroke — waveform → up-arrow — and may flip to a `[stop]` control while streaming) or the retype implies enter. The surface answers instantly with a working state: prior content VANISHES (chip grid gone, panel collapses to its slim header, whole layout swaps); then the theater — `[status phrases]` cross-dissolve with a left-to-right shimmer sweep ("[Thinking]" → "[Modeling…]" → "[Planning…]"), a `[spinner]` rotates over a loading strip, a row of `[loading cards]` lines up, or a `[checklist]` populates and its items flip one by one to green checks with strikethrough while a `[status heading]` flips tense ("[Using X]" → "[Used X]").
  - _Variant — (A) status-flare exit_: end the clip ON the theater — "[Generating…]" / the rotating spinner — the flare is the button; the answer is left to the imagination.

- **Scene 4 (rest) — the answer arrives.** Choose by sub-shape:
  - **Sub-shape B (full generate loop)**: the output BUILDS progressively, each block pushing content down — `[answer text]` streams paragraph by paragraph; `[action-log rows]` pop in sequentially, each with a `[brand icon]`; `[diff cards]` expand with green-highlight added lines; `[chart lines]` draw staggered left-to-right from a shared origin; an `[ASCII / summary table]` draws in; live counters tick; the surface auto-scrolls vertically to follow the newest line (page, terminal, or in-card scroll) — often under ONE slow continuous push-in on the result window.
  - **Sub-shape C (instant-result surface)**: the machine answers with a finished surface — the matching `[result / article]` renders in place; `[autocomplete chips]` stagger-pop below the bar WHILE the query types (the machine answers every keystroke), then a hover fills the `[Search button]` solid and a click confirms; the `[generated page]` rises as a rounded card and SCROLLS continuously beneath the pinned prompt; a blur-whip resolves onto the `[artifact window]` and a tab click FLIPS code → preview; or a zoom-out reveals the prompt pill was inside a full `[workspace]` where the `[content]` rewrites itself live.

- **Scene 5 (final beat) — resolve.** Diverges by role and sub-shape:
  - _Variant — Key_Feature (hold)_: HOLD on the completed output — chart finished, diff cards + `[action buttons]` fully rendered; no fade-out, no blank end frame.
  - _Variant — Product_Intro (confirm)_: the cursor lands the confirming click (`[Create PR]` / `[Generate]` / `[Search]`) as the clip ends, or extras fade and a final push-in leaves the clean end state; one member hard-cuts to a minimal `[end card]` — the submit button alone at dead center with a settle pop.
  - _Variant — Hook (restart — the signature)_: a SECOND `[prompt / command]` starts typing at a fresh prompt line, or the query BACKSPACES-AND-RETYPES and the output swaps wholesale to `[result 2]` — the clip ends MID-ACTION, mid-scroll or mid-word: the loop is endless, and that is the point.
  - _Variant — CTA_: the end card from Scene 2 simply holds to the last frame; the blinking cursor is the only motion.

**motion vocabulary**: character-by-character typing with blinking caret / block cursor; typed-headline beats replacing each other; input pill grows / wraps downward into a multi-line box; prompt palette / card springs in; pill bar expands sideways from a mark or chip; orb formation with glowing rim; typed token → inline brand-pill morph mid-typing; placeholder clear; ✕-click query clear; backspace-and-retype query swap; attachment drag-in and tray settle; dropdown open + row hover-highlight + checkmark select + toolbar label update; chip-grid hover dance; cursor glide / arc with hover highlight fills; click press dip; submit-button state morph (waveform→up-arrow, submit→stop); hover fill-state swap on a Search button; content vanish / panel collapse / layout swap on submit; status-phrase cross-dissolves with left-to-right shimmer sweep; pulsing "Thinking"; spinner rotation; loading strip; animated trailing dots; loading model-card row; status-heading tense flip (Using→Used); checklist squares flipping to green checks with strikethrough; action-log rows popping in sequentially with brand icons; streaming text blocks pushing content down; green-highlight diff cards expanding; staggered left-to-right chart line-draws; ASCII / summary table draw-in; count-up ticker; vertical output scroll (page / terminal / in-card) following the newest line; generated page rising as a rounded card and scrolling beneath a pinned prompt; autocomplete chips rapid stagger-pop; code↔preview instant flip on tab click; blur-whip transition; prompt jumps to a heading on submit; zoom-out reveal from prompt pill to full UI window; single eased / accelerating push-in landing on the input; slow continuous push-in on the result window; window fly-in with motion blur; zoom + pan cropping browser chrome; ⌘K modal spring-in with background blur; full-frame grid parting at the vertical centerline; headline demotion (scale-down + desaturate + lift); chip horizontal-stretch into a wide terminal pill; quiet low-contrast metadata fade-ins; sequential spring pop-ins of an icon row; second prompt typing at the cut; interface dim / fade at the cut; long static end hold with blinking cursor.

**rule mapping**

- character-by-character typing, placeholder clear, backspace-and-retype, second prompt at the cut, typed-headline beats → `discrete-text-sequence` (typing / typos / holds / backspace) backed by `gsap-effects` (typewriter recipe)
- blinking caret / block cursor (persisting through holds) → `context-sensitive-cursor`
- prompt / status / output phrase windows, script-driven beat durations → `dynamic-content-sequencing`
- input card grows downward / wraps as text fills → `anchored-layout-expand` (top-anchored downward growth, stepped at wrap boundaries)
- typed token → inline brand-pill morph mid-typing → composition: `scale-swap-transition` (token→chip swap at the conversion threshold) + `card-morph-anchor` (the reflow around the chip)
- prompt palette / modal / dropdown springs in; loading cards, log rows, diff cards, autocomplete chips, icon rows arriving staggered → `spring-pop-entrance` (single hero or staggered group)
- pill bar expands sideways from a mark; chip stretches into a wide terminal pill → `card-morph-anchor` (container morph)
- cursor glide to a control, press, ripple → `cursor-click-ripple`; the press dip + recovery → `press-release-spring` (or `physics-press-reaction` for cursor+button compressed together)
- hover highlight fills, Search-button instant solid fill, UI keyword accents → `asr-keyword-glow` (static-timeline glow variant) or `press-release-spring` (color-transition variation)
- attachment drag-in with cursor → `context-sensitive-cursor` (pointer↔grab) + `spring-pop-entrance` (tray settle)
- content vanish / layout swap / panel collapse on submit; code↔preview instant flip → `scale-swap-transition` (paired same-center swap) or a hard `tl.set` state swap via `discrete-text-sequence` semantics
- prompt jumps to a heading on submit → FLIP reposition — see `hyperframes-keyframes` (FLIP); the travel itself via `nudge-curve` (slow-fast-slow group slide)
- status-phrase cross-dissolves with shimmer sweep → `discrete-text-sequence` (phrase swaps) + `ambient-glow-bloom` (Shimmer sweep variation — single-pass traveling sheen, clipped to the text)
- spinner rotation, animated trailing dots, pulsing loader glyphs → `svg-icon-enrichment` (rotating / pulsing internal SVG elements); the bounded "Thinking" pulse → `sine-wave-loop` (finite repeats — this pulse PERFORMS status, it is not idle wobble)
- checklist state flips, status-heading tense flip, status-pill swaps → `discrete-text-sequence` (discrete state stepping); the checkmark stamp → `svg-path-draw` or `spring-pop-entrance`
- streaming text blocks / log rows pushing content down → `dynamic-content-sequencing` (per-block windows) + `spring-pop-entrance` (per-row arrival)
- vertical output scroll following the newest line (page / terminal / in-card) → composition: content translateY keyed to the same timeline as the content windows + a matched `viewport-change` counter-pan when the frame itself travels
- generated page as a rounded card whose internal content scrolls → `3d-page-scroll` (flat variant — internal scroll of a page card)
- staggered chart line-draws → `svg-path-draw` (stroke-dashoffset, staggered starts)
- count-up ticker / live counters → `counting-dynamic-scale`; result bars / fills → `stat-bars-and-fills`
- single eased push-in landing on the input; slow continuous push-in on the result → `multi-phase-camera` (push phase) with the destination framed via `coordinate-target-zoom`
- zoom-out reveal from prompt pill to full workspace; zoom + pan cropping chrome → `viewport-change` (composite pan+scale on the `.world` wrapper)
- window fly-in with motion blur; blur-whip transition → `motion-blur-streak`
- ⌘K modal with background blur → `depth-of-field-blur` (blur the page plane, keep the modal sharp) + `spring-pop-entrance`
- full-frame grid parting at the vertical centerline → `center-outward-expansion` (halves glide outward in lockstep)
- orb formation with glowing rim → `ambient-glow-bloom` + `spring-pop-entrance`
- headline demotion (scale-down + desaturate + lift) → `gsap-effects` (plain composite tween; no dedicated rule needed)
- interface dim at the cut, hard cut to a minimal end card, end mid-word / mid-scroll → exit conventions, no rule needed
- long static end hold with only the caret blinking → `context-sensitive-cursor` (the blink is the sanctioned residual motion)

**camera modifier** (the camera always serves the ask or the answer; many members are fully camera-static — typing, submit theater, and streaming carry the shot)

- ONE smooth eased / accelerating push-in that lands tight on the input and LOCKS (Hook, Product_Intro) → `multi-phase-camera` (push) + `coordinate-target-zoom` (target the input) — the defining move of the "watch me ask" opener.
- ONE slow continuous push-in running under the typing or under the output build, decelerating to a near-hold (Product_Intro, Key_Feature) → `multi-phase-camera` — gives the response weight without stealing from it.
- ONE zoom-out reveal — the prompt pill turns out to live inside a full workspace (Key_Feature, sub-shape C) → `viewport-change` (pull-back) — the inverse move; the ask was closer to the product than you thought.
- Entry-only flourishes: window fly-in with motion blur (`motion-blur-streak`), zoom + pan cropping browser chrome (`viewport-change`) — both settle before typing starts.
- Never more than two real viewport moves per shot; the frame is LOCKED during submit theater and streaming (the content scrolls, the camera does not).


<!-- ===== FILE: hyperframes/hyperframes-animation/blueprints/spatial-pan-stations.md ===== -->

# spatial-pan-stations — Spatial Pan / Stations

**intent**: Pre-place a sequence of labeled stations on one oversized canvas, then traverse it with a single virtual camera — repeated lateral/diagonal pans that center each station in turn and reveal a callout at every stop, landing held on a final station.

**roles served**

- Hook (from hook-pan-timeline): a horizontal timeline of evenly-spaced milestones, left-panned beat by beat, each marker getting a spring-popped callout, landing on the present moment ("evolution / milestone walk leading up to us").
- Problem (from problem-camera-pan-stations): a connected web of pain "stations" linked by hand-drawn leading lines, diagonally panned station to station, ending on a tangled scribble knot ("too many disconnected steps — it's a mess").
- Product_Intro (from concept-demo-decode-pan): a two-shot strip bridged by ONE lateral pan — shot 1 holds a static phrase whose accent word 3D-flap-DECODES (the concept lands), then the camera pans across the strip (with background parallax) into shot 2, where a cursor drives a live typing demo. Pairs this pan with `cursor-ui-demo`'s focal-locked tracked typing.

**duration**: 7–10s (union of Hook 8–10s, Problem ~7s, concept-demo ~7s)

**shot structure**
One oversized flat canvas on a solid `[bg color]`; all stations/markers pre-placed in world space; `[accent color]` text + simple line-icons; one virtual `.world` camera pans ease-in-out between stops. Each station holds ~1.0s.

- Scene 1 (0.0–~1.0s): Camera opens on station 1 — `[label 1 / first step]` centered. A reveal lands on it (see variants). Camera then begins to PAN toward station 2, sliding station 1 out of frame.
- Scene 2 → Scene N-1 (~1.0s each): Camera PANS (ease-in-out) to center the next station; on arrival its `[label k]` (+ optional `[secondary label]`) is REVEALED with the role reveal. Repeat per station.
- Scene N (final, ~last beat): One last pan lands on the terminal station; the final `[callout / landing element]` reveals and HOLDS to the end. Camera goes static on the punchline.

- Variant — Hook: stations sit as evenly-spaced `[markers]` on a thin horizontal `[timeline]` (lower third); pans are LEFT-only along the single axis (timeline scrolls left). Each callout is a bordered `[callout box]` + downward triangle (offset drop-shadow) that SPRING-POPS up (scale 0→100%, bouncy overshoot, transform-origin at triangle tip) reading `[label k]`; a `[secondary label, e.g. year]` fades in and RISES above it. Some mid markers arrive as plain static text revealed by the pan alone (no box). Final scene lands on the `[present-day label]`, springs, holds.
- Variant — Problem: stations are scattered across a 2D web; pans are DIAGONAL, STEERED by `[accent color]` hand-drawn lines — each station has a rough write-on line/arrow that draws toward the next and the camera follows it (Scene 1 also draws a loop/circle around the headline's key word). Each station = a white `[line-icon]` above its `[label]`, revealed plainly by the pan (no spring box). Final scene: the accent line spirals into a dense chaotic SCRIBBLE KNOT centered on the field; camera holds static on the tangle (visual punchline).

**motion vocabulary**
repeated ease-in-out camera pans (horizontal-left for Hook, diagonal-steered for Problem) across one large static canvas; pre-placed stations sliding through frame via the pan; spring-overshoot callout pop with triangle-tip origin (Hook); rise-and-fade secondary label (Hook); plain labels/icons arriving via the pan alone; rough hand-drawn "write-on" leading lines/arrows + loop/circle key-word mark (Problem); terminal chaotic-scribble knot draw (Problem); static hold on the final station/punchline.

**rule mapping**

- camera pan / traverse across the canvas (primary) → `viewport-change` (single `.world` wrapper transform; PAN mode)
- sequencing the repeated pan beats into stops → `multi-phase-camera`
- centering each station as the pan target → `coordinate-target-zoom` (used as pan-to-target, no zoom)
- spring-overshoot callout pop, triangle-tip origin (Hook) → `spring-pop-entrance`
- rise-and-fade secondary label + plain per-station label/icon reveals via the pan → `discrete-text-sequence`
- hand-drawn leading lines / arrows / loop-circle key-word mark / terminal scribble knot (Problem) → `svg-path-draw`
- station line-icons (Problem) → `svg-icon-enrichment`
- static hold on the final station / punchline → (no motion; sustained held frame, no rule needed)

**camera modifier**: The pan IS the camera. One `.world` virtual-camera transform in PAN mode — `viewport-change` — sequenced across stops by `multi-phase-camera`, each stop targeted via `coordinate-target-zoom` (pan-to-target). No depth push-in (that distinguishes this from the cluster-push-in / dataviz-pushthrough blueprints).


<!-- ===== FILE: hyperframes/hyperframes-animation/blueprints/ticker-takeover.md ===== -->

# ticker-takeover — Ticker Displace / Takeover

**intent**: A context phrase types in, an accent word cycles through options like a slot-machine to suggest "this could be many things," then a hero CRASHES in from off-screen and physically shoves the text aside — "actually, this is what it is." A collision, not a fade.

**roles served**

- Hook (from `takeover-ticker-displace`): when a static lead-in phrase + a cycling accent word should be **physically replaced** (not cross-dissolved) by a hero arriving with momentum, and the final frame is the hero alone. Reach for it when the takeover should read as an impact.
- Brand_Outro: the same collision used as a sign-off — options cycle, the brand mark crashes in and owns the frame.

**duration**: 5–7s

**shot structure** (a `[bg]` canvas; one text group on the left/center that gets ejected by an incoming hero)

- **Scene 1 (0.0–~1.4s) — context build.** A typewriter lays down a `[lead-in phrase]` character-by-character (smooth, no typos — selling confidence, not human chaos). Camera static.
- **Scene 2 (~1.4–3.0s) — the cycling beat.** An `[accent word]` slot inside the line ticks through 2–3 `[options]` on a vertical spring-roll (each click a new word), suggesting breadth — "many things this could be." (More than ~3 reads as filler.)
- **Scene 3 (~3.0–4.2s) — the collision (signature move).** A `[hero]` crashes in from off-screen with momentum and physically SHOVES the whole text group aside — the text reacts to the impact (gets displaced), it does not fade. The hero lands **heavy** — a longer settle, not a zip — so it reads as mass, not speed.
- **Scene 4 (~4.2–end) — the hero alone.** The hero settles dead-center and reads still. Holds.

**motion vocabulary**: smooth character typewriter; vertical spring-ticker word roll (2–3 steps); off-screen hero crash-in with momentum; reactive displacement of the struck text group; heavy long-tail landing (not bouncy); dual-axis subtle jitter on the resting hero.

**rule mapping**

- smooth single-phrase typewriter lead-in → `discrete-text-sequence` (smooth-slice / continuous `floor(progress)` form — no typo machinery)
- accent word slot-machine cycling through options → `vertical-spring-ticker` (`STEPS` = number of options the hero will replace; the rule's footer-reveal is unused — Scene 3 takes its place)
- hero shoves the text group aside on impact → `reactive-displacement` (the text is the displaced mass; express the hero's "heavy land" as a longer `power2` settle, not the rule's default `back.out`)
- hero's fast off-screen crash-in → `motion-blur-streak` (directional velocity blur resolving sharp as it lands)
- resting-hero aliveness → `sine-wave-loop` (low-amplitude dual-frequency register — scale + rotation jitter composing onto the hero's final landed scale; never a yoyo around 1)

**camera modifier**: camera-static — the displacement happens in element space (the hero moves the text), so there is no real camera move; the impact is the only motion.


<!-- ===== FILE: hyperframes/hyperframes-animation/blueprints/titlecard-reveal.md ===== -->

# titlecard-reveal — Title-Card / Single-Card Reveal

**intent**: The calm breather/landing beat — one clean title or single brand/proof card revealed with exactly one restrained move (a slide-up crossfade, or a wipe-away-to-reveal), then a still hold. Low motion is the payload, not a deficiency.

**roles served**

- Benefits (from `benefits-titlecard-crossfade`, #34): a calm two-line value title card — headline value line, then one slide-up crossfade to a qualifier/elaboration line that holds center.
- Social_Proof (from `social-proof-reveal-card`, #35): wipe a busy app-collage open away with one diagonal pill-sweep to reveal a clean brand lockup (icon + wordmark) plus a centered "loved by [N]+ [audience] teams" social-proof line that spring-settles and holds.
- CTA (from `hard-cut-card-stack-to-logo`): a monochrome end-card
  CHAIN — statement → CTA / availability line → brand wordmark/logo — separated by instant hard
  cuts at full opacity; each card is its own allocated stillness, and the sequence terminates on
  the logo held to the final frame.
- Product_Intro (from `title-card-prelude-chain`): a three-beat dark title
  PRELUDE before any product UI — `[logo]` pop → `[name]` (a `[version]` appends grey→bright) →
  `[tagline]` card — chained by clears and blur-snap handoffs rather than hard cuts.

**duration**: 3–5s (Benefits 3–4s; Social_Proof ~5s / observed 4.7s). Card chains run 2–3s per
card, ~5.5–9.5s total.

**shot structure**

```
Scene 1 (0.0–~0.4s): static camera on [neutral / dark background]. Establish the opening state.
  Variant — Benefits: empty-to-text — [benefit line 1] is about to fade in centered (no busy open).
  Variant — Social_Proof: a busy intro frame holds briefly — an [app-screenshot / use-case collage] of overlapping cards under a [setup line].

Scene 2 (~0.4–~1.5s): the ONE move executes — a single restrained reveal that brings the calm card to center.
  Variant — Benefits: [benefit line 1] fades in centered while scaling slightly (~95%→100%, smooth ease-out) and holds.
  Variant — Social_Proof: a large [accent-color] rounded pill sweeps diagonally bottom-left → top-right and exits the corner, clip-path wiping the collage away to reveal the [brand logo lockup] beneath as the [logo icon] strokes draw on.

Scene 3 (~1.5s–end): the revealed/settled card holds to the end (the allocated stillness). At most one subtle live element (a slow breathing pulse on the card, or a very slow camera drift). No second development phase.
  Variant — Benefits: [benefit line 1] translates up and fades out as [benefit line 2 — qualifier / elaboration] translates up from below center and fades in to take center; holds. (This single slide-up crossfade IS the one move — Benefits front-loads no Scene-2 wipe.)
  Variant — Social_Proof: the lockup — [logo icon] centered, [wordmark] below, centered [social-proof tagline] "Loved by [N]+ [audience] teams" (the [N]+ may count up) — spring-settles small, then holds.

Variant — card chain (CTA end-card stack / Product_Intro title prelude): the single-card contract
repeats 2–3 times in sequence. Each card is a complete Scene 1–3 in miniature — arrive (or simply
BE there), at most one restrained move, hold — and the seams between cards are INSTANT hard cuts
at full opacity (no crossfade, no fade-through-black) or, in the prelude flavor, a blur-away →
snap-into-focus handoff.
  Card moves stay on budget: a character-by-character type-on with visible partial states, a
  right-to-left backspace that resolves the [wordmark] into the small [logo icon], a grey→bright
  append ("[name]" gains "[version]"), a blur-snap into focus — or nothing beyond a
  barely-perceptible continuous slow scale-up across the hold.
  The final card is always the [brand logo / lockup], held static to the last frame.
```

**motion vocabulary**: single restrained reveal (gentle fade-in + subtle scale-up settle | diagonal clip-path pill-wipe), one slide-up crossfade between two centered lines (Benefits), icon stroke draw-on (Social_Proof), optional "[N]+ teams" count-up, logo+tagline spring-settle-and-hold, subtle breathing on the held card, hold-to-end. Calm register — no spring chains, no tumble, no per-beat flips, no second phase. Camera static (optional very slow drift only). Card-chain register: instant hard cut at full opacity as the only seam, barely-perceptible
continuous slow scale-up across each hold, character-by-character type-on with visible partial
states, right-to-left backspace collapsing the wordmark into the logo icon, grey→bright text
append, blur-away → snap-into-focus card handoff, logo pop with overshoot + glow (prelude opener),
monochrome text-on-solid throughout.

**rule mapping**

- gentle fade-in + subtle scale-up settle (Benefits Scene 2) → `rules/scale-swap-transition.md` (restrained in/settle; cross-reference the fade ease in `techniques.md`)
- single slide-up crossfade between two centered lines (Benefits Scene 3) → `rules/discrete-text-sequence.md` (one line hands off to the next; translate-up + crossfade)
- diagonal pill-wipe reveal (Social_Proof Scene 2) → `../techniques.md` (clip-path reveal masks — the wipe)
- icon stroke draw-on (Social_Proof Scene 2) → `rules/svg-path-draw.md`
- "[N]+ teams" count-up (Social_Proof Scene 3, optional) → `rules/counting-dynamic-scale.md`
- logo + tagline spring-settle-and-hold (Social_Proof Scene 3) → `rules/spring-pop-entrance.md` (single soft settle; intentionally one beat, not a chain)
- subtle breathing on the held card (the one live element during the hold) → `rules/sine-wave-loop.md`
- type-on / backspace / grey→bright append (chain cards) → `rules/discrete-text-sequence.md`
  (non-linear typing incl. backspace; drive the version append as a bulk addition)
- wordmark remainder resolves into the logo icon → `rules/scale-swap-transition.md` (same-center
  swap fired as the last character deletes)
- barely-perceptible slow scale-up across a hold → the camera-modifier drift
  (`rules/multi-phase-camera.md`, micro-drift register) applied per-card
- blur-away → snap-into-focus handoff (prelude flavor) → `rules/depth-of-field-blur.md` (single
  pull on the outgoing / incoming card)
- logo pop with overshoot + glow (prelude card 1) → `rules/spring-pop-entrance.md` +
  `rules/ambient-glow-bloom.md`
- instant hard cut at full opacity → not a rule: a timeline `tl.set` swap — deliberately NO
  transition entry.

**camera modifier**: optional — a single very slow drift/push under the hold only → `rules/multi-phase-camera.md`. Default is fully static; do not add unless the held beat would otherwise read as a freeze-frame.

**stillness note**: This is a legitimate allocated-stillness beat. The hold in Scene 3 is the deliverable, not an unanimated gap — do NOT manufacture a development phase, extra swaps, or force-animation. One restrained move + a subtle hold (optionally one breathing element or one slow drift) is the correct and complete shape. The card-chain variant does not break this: each card individually obeys the one-move + hold
contract, and the hard cut is a seam, not a move. Boundary: if the cards flip at sub-second tempo
or each beat carries its own entrance/exit energy, you have left this blueprint — that is
`kinetic-type-beats` (its CTA variant owns the high-tempo value-line stack).


<!-- ===== FILE: hyperframes/hyperframes-animation/blueprints/transcript-scroll-artifact-reveal.md ===== -->

# transcript-scroll-artifact-reveal — Transcript-Scroll Artifact Reveal

**intent**: The frame travels vertically along ONE long content surface — an agent transcript, a running task feed, an analysis document, a story draft — rendered full-bleed on a flat canvas (no device frame, no held mockup), by camera pan or element scroll; the traversal itself is the story ("look how much work happened / how much is here"), until ONE focal interaction — a file-chip click, a quote highlight, a collapsible-row expand — pivots the shot into an artifact/detail reveal: the deliverable behind the work.

**roles served**

- Key_Feature (modes: `pan-to-workspace` · `feed-rush` · `document-to-artifact` · `selection-pivot`): the x-viral AI-product grammar for "the agent did a lot of work → here's the deliverable." The long surface is the EVIDENCE (tool pills, checked progress items, task rows, headings, comps tables, story paragraphs), read at traversal pace; the artifact is the PAYOFF (full workspace with live mockup, spreadsheet with highlighted cells, inline ask-panel, sub-task stack). Reach for it when the feature's proof is the volume/depth of generated work and the beat should cash that in on one interaction — not a held device tour (`device-surface-showcase`), not a cursor-chased workflow (`cursor-ui-demo`).

**duration**: 5–11.8s (feed-rush 5.4s · pan-to-workspace 5.0s · selection-pivot 9.3s · document-to-artifact 11.75s)

**shot structure** One `[long content surface: agent chat transcript / task feed / analysis document / story doc]` sits full-bleed on a `[flat light canvas]` (goldens: warm off-white / cream / beige / plain white — the surface's own background IS the scene background); dark text with small `[accent]` marks (green verb highlights, model-tag pills, check circles, yellow cells). Three acts: TRAVERSE → HINGE → ARTIFACT. Camera discipline is the signature: at most TWO real camera moves in the whole shot, bracketing the hinge; everything else is element motion on a static frame.

- **Scene 1 (0.0–~40–60% of runtime) — establish + vertical traversal (the evidence).** The surface establishes with one small opener — a `[title]` types on / a centered `[title]` shrinks ~50% and glides to the top-left to dock as a fixed header / the frame opens tight on the `[chat panel]` — then the traversal begins: the frame travels DOWN the content (or the content streams UP through the frame), revealing progressive work in reading order: `[prompt → tool pills → checked progress items → typed summary]`, `[tagged task rows → muted tasks → checklist block]`, `[heading → paragraph → comps table → bullets]`, `[title → story paragraphs → dialogue]`. New rows may cascade in (staggered arrival) before the scroll takes over; a typed line may finish under the moving frame. Traversal texture varies by member: one continuous slow pan, a fast continuous feed rush, stepped scrolls decelerating at each stop (speed-blur between stops, content fading at frame edges), or one smooth scroll easing to a stop.
- **Scene 2 (~1–2s) — the hinge: ONE focal interaction.** The traversal settles and a single interaction pivots the shot: a `[file-attachment chip]` spring-pops in below a typed handoff line and a cursor glides in and CLICKS it; a `[sentence/quote]` gets a selection-highlight sweep and a `[tooltip pill]` spring-pops above it for the click; a `[collapsible row]` reaches the frame center and EXPANDS; or the typed `[verifier summary]` completes as the implicit trigger. This is the only interaction in the shot — the cursor (if any) appears here for the first time.
- **Scene 3 (rest) — artifact reveal + hold.** The hinge cashes in, choosing ONE reveal mechanic: a fast smoothly-DECELERATING zoom-OUT re-frames the whole `[workspace]` (the panel just traversed becomes a sidebar beside a `[live mockup]` and `[tool panel]`); an `[artifact window: spreadsheet]` scales up from small toward full frame, then a slow push-in + lateral pan settles on its `[highlighted cells]`; an `[inline panel]` expands below the highlighted line and a `[follow-up question]` types into it; or the row unfolds into a `[sub-task stack]` and the scroll settles on `[narration text]`. Optional coda: one cursor click instantly swaps a `[screen]` inside the revealed artifact (e.g. a phone tab click). Frame locks; element motion only to the end.

- Variant — _pan-to-workspace_ (001_claudeai, 5.0s): traversal is a REAL camera pan — opens tight on the chat panel, one single uninterrupted downward glide (never cutting away) over pills → checked list → typing verifier summary; hinge is the summary completing; reveal is ONE rapid decelerating zoom-out to the three-part workspace (chat-as-sidebar / phone mockup / tweaks panel); coda cursor click swaps the phone screen instantly. Exactly two camera moves total.
- Variant — _feed-rush_ (010_perplexity A, 5.4s): NO camera at all — title docks to header, five tagged rows cascade in, then a fast continuous upward ELEMENT scroll races through muted tasks and a checklist to a collapsible row; hinge is the row itself; reveal is the row expanding into a six-item sub-task stack, settling on narration. Cursorless.
- Variant — _document-to-artifact_ (010_perplexity B, 11.75s): traversal is a stepped ELEMENT scroll (static frame) — the document climbs in fast steps, decelerating at each stop, blur/fade between stops, clearing to blank canvas; hinge is a typed handoff line + file-chip pop + cursor click; reveal is the spreadsheet window scaling up then one slow continuous push-in + rightward pan onto the yellow-highlighted forecast columns.
- Variant — _selection-pivot_ (014_OpenAI, 9.3s): typed headline → document builds (bubble prompt + typed title + populating paragraphs) → one smooth upward element scroll eases to a stop; hinge is the selection-highlight sweep + the shot's ONE push-in framing the sentence + tooltip-pill click; reveal is the inline panel expanding below the line with the referenced quote and a rapidly-typed follow-up question. Camera locked at the pushed-in zoom to the end.

**motion vocabulary** continuous slow downward camera pan; fast continuous upward feed scroll; stepped document scroll decelerating at each stop; smooth scroll easing to a stop; speed-blur between scroll stops; content fade at frame edges; centered title shrinks ~50% and glides to a top-left header dock; task rows cascade in staggered; typed line / typed title / typed follow-up question (caret); green leading-verb highlights and model-tag pills riding past; checked-item strikethroughs riding past; file-attachment chip spring pop-in; tooltip pill spring pop; chat-bubble arrival; cursor glide-in + click; selection-highlight sweep across a sentence; ONE camera push-in onto the selection; fast decelerating zoom-out to the full workspace; artifact window scales up from small; slow push-in + lateral pan settling on highlighted cells; collapsible row expands into a sub-task stack; inline panel expands below the line; phone-screen instant swap on a coda tab click; frame-lock hold.

**rule mapping**

- vertical traversal by ELEMENT scroll — fast feed rush / stepped document scroll / smooth scroll-to-stop → `3d-page-scroll` (flat variant: tilt ≈ 0 — the surface's content `translateY`-scrolls to sections; the multi-phase scroll variant covers stepped stops; keep ONE ease family across all steps — `power3.out`/`power4.out` for UI-scroll feel)
- vertical traversal by CAMERA pan (transcript glide) → `viewport-change` (pan mode — the world translates up under a static frame; one continuous tween, no cuts)
- speed-blur between stepped-scroll stops → `motion-blur-streak` (blur peaks at max scroll velocity, resolves to 0 at each settle)
- which content each traversal beat reveals (stop-by-stop sequencing) → `dynamic-content-sequencing`
- centered title shrinks and glides to dock as a fixed header → `gsap-effects` (one simultaneous scale + translate tween; plain two-property move, no named rule required)
- task rows cascade in staggered before the scroll takes over → `waterfall-entry` (arrival cascade; goldens use fade + slide-up — the house rule prescribes binary-opacity whip-in, adopt the house form) or `spring-pop-entrance` (staggered group) for card-like rows
- typed lines — verifier summary, handoff line, document title, follow-up question, opening headline → `discrete-text-sequence` (+ `context-sensitive-cursor` for the trailing caret)
- file-attachment chip pop-in / tooltip pill pop / chat-bubble arrival → `spring-pop-entrance`
- cursor glides in, lands, clicks (hinge and coda) → `cursor-click-ripple` (+ `physics-press-reaction` to compress cursor and target together on the press)
- selection-highlight sweep across the sentence → `css-marker-patterns` (highlight sweep)
- ONE push-in onto the highlighted selection / slow push-in + lateral pan settling on highlighted cells → `coordinate-target-zoom` (measured off-center target — the lateral pan IS the counter-translate component), sequenced under `multi-phase-camera` when it follows the window scale-up
- fast decelerating zoom-OUT to the full workspace → `coordinate-target-zoom` (zoom-out variation: open at the zoomed-in framing, pull to scale 1 with `power3.out`/`power4.out`) or `viewport-change` (single continuous pull on the `cam` object)
- artifact window scales up from small toward full frame on the click → `spring-pop-entrance` (hero arrival scale-up; tune overshoot to ~0 / `power3.out` so the window reads weighty, not bouncy)
- collapsible row expands into a sub-task stack / inline panel expands below the highlighted line → `anchored-layout-expand` (in-flow accordion growth pushing subsequent content DOWN — never tween width/height) + `waterfall-entry` (or `spring-pop-entrance` stagger) on the arriving children
- phone-screen instant swap on the coda tab click → `discrete-text-sequence` (discrete whole-state swap; instant, no in-artifact camera move)
- green verb highlights, model-tag pills, check-circle strikethroughs, yellow forecast cells, edge fade masks → static styling of the surface content — no motion rule needed

**camera modifier**: The blueprint's camera law: **at most TWO real camera moves, bracketing the hinge** — the goldens are emphatic (their briefs carry CRITICAL camera notes). Pick the traversal mechanic first: camera pan (`viewport-change` pan — pan-to-workspace only) OR element scroll (`3d-page-scroll` flat — all others); never both at once. The reveal then spends the second (or only) move: one zoom-OUT to the workspace or one push-IN to the detail (`coordinate-target-zoom`, phases sequenced by `multi-phase-camera`), after which the frame LOCKS — all remaining motion is element-level (typing, expand, screen swap). The feed-rush variant spends zero camera moves: the whole shot is element scroll + expand. This restraint is what separates the shape from `cursor-ui-demo` (camera servos to every interaction) and from `device-surface-showcase` (a showcase camera presenting a held hero).

**Overflow (scrolled/panned surfaces — required for a clean `check`):** the traversal deliberately moves content past the frame edges. Clip at the scene (`overflow: hidden`) AND mark the moving inner layer (the `.page-content` / `.world` wrapper carrying the transcript/feed/document) with `data-layout-allow-overflow` — otherwise `check` reports `text_box_overflow` / `container_overflow` for every row that has scrolled off. The clip handles it visually; the attribute tells the layout audit it's intentional.


<!-- ===== FILE: hyperframes/hyperframes-animation/blueprints/typewriter-reveal.md ===== -->

# typewriter-reveal — Typewriter Reveal

**intent**: A live text caret types (and edits) a line as a human would, then either collapses it to a point and pops a brand payoff, or holds it under a persistent brand mark while a sub-line types/swaps into the final CTA — making "someone is typing this" the engine of the shot.

**roles served**

- Hook (from hook-typed-line-to-reveal): Type a relatable question/statement live, then COLLAPSE it and spring-pop the brand — a logo lockup OR a product-UI moment ("here's the everyday pain, now here's us").
- Brand_Outro (from brand-outro-persistent-mark-cta-rail): Hold the hero mark dead-center/top the whole shot while a sub-line beneath it swaps or types its way into the final CTA — landing the ask once the logo is already established.

**duration**: 3.6–7s (Brand_Outro 3.6–6.0s · Hook 5.5–7s)

**shot structure** (one consolidated template; `[slots]` are product-agnostic)

- Scene 1 (0.0–~2.0s): On a solid `[bg color]` field, a blinking text-input caret `|` sits at the line start, then `[primary line]` TYPES on character-by-character with the caret trailing.
  - _Variant — Hook_: nothing else is on screen; the typed `[hook line]` owns the frame. (Sub-variant: the line types inside UI chrome — a rounded `[input/pill]` — and the whole assembly continuously TRANSLATES leftward + scales slightly so the active caret stays pinned near frame-center while earlier words scroll off and clip past the left edge — a ticker push.)
  - _Variant — Brand_Outro_: a `[logo mark]` (+ optional `[wordmark]`) is already centered/upper and STAYS fully visible for the entire shot; an entry flourish plays on the mark itself (e.g. `[checkmark/icon]` strokes into the mark, or thin concentric rings ripple outward from it), and the typed `[tagline / product label]` is the SUB-LINE beneath the mark.

- Scene 2 (~2.0–4.5s): The typed line is MODIFIED in place — the active text is edited rather than re-shot.
  - _Variant — Hook_: final word(s) BACKSPACE out and a new word RETYPES (`[word A]` → `[word B]`), or the fill/caret snaps to `[accent color]` on the final word. Holds briefly.
  - _Variant — Brand_Outro_: the sub-line is REMOVED in place — a direct hard CUT/replace (NO backspace) or a moving mask-WIPE erases it — while the mark performs a small idle move (gentle rotate / sparkle reposition); the mark never leaves frame.

- Scene 3 — resolve:
  - _Variant — Hook (collapse, ~0.3–0.7s)_: caret vanishes; the whole text/assembly COLLAPSES to a point at center (horizontal X-collapse or scale-to-0 zoom-out) and disappears, leaving a clean `[bg]`. Then (remainder) a centered `[brand element]` SPRING-POPS in:
    - _logo-lockup sub-variant_: a `[mark/icon]` pops, then slides aside as a `[wordmark]` UNMASKS / slides out from behind it; both settle into a centered lockup.
    - _product-UI sub-variant_: a `[UI control]` (e.g. button) pops; a `[cursor]` sweeps in from a corner and homes onto it; on contact a ~150ms state-FLIP — base cross-fades to `[accent color]`, icon inverts, and a soft radial GLOW blooms outward and persists.
  - _Variant — Brand_Outro (~4.5s–end)_: the final `[CTA]` resolves in the sub-line slot — TYPED in with a caret and/or shown as a `[CTA in accent-color button]` beside plain text; an optional `[accent color]` GLOW ring / halo settles around the persistent mark. Holds to end. Final frame: `[logo mark]` + (glow ring) + `[CTA]`.

**motion vocabulary**: blinking text caret; character-by-character type-on; backspace-and-retype OR in-place hard-cut/mask-wipe text swap; optional leftward ticker push (assembly translates to keep caret centered); persistent centered hero mark (never vanishes) with entry flourish (icon stroke-draw, concentric ripple rings) and small idle move (rotate / sparkle); X-collapse / scale-to-0 zoom-out of the typed line; spring-pop brand reveal; wordmark unmask-slide into lockup; cursor sweep + UI state-flip + radial glow bloom; accent glow/halo ring settle; pill/button CTA reveal; hold.

**rule mapping** (per motion verb → `rules/<id>.md`)

- blinking text caret → `context-sensitive-cursor` (caret color-switch + blink)
- character-by-character type-on → `discrete-text-sequence` (typing/typos/holds/backspace); recipe `gsap-effects` (typewriter)
- backspace-and-retype → `discrete-text-sequence`
- in-place hard-cut / replace text swap → `discrete-text-sequence` (whole-text state swaps)
- mask-wipe erase of sub-line → `techniques.md` clip-path reveal (run in reverse)
- leftward ticker push (assembly translates to keep caret centered) → `camera-cursor-tracking` (viewport follows a moving caret)
- persistent hero mark hold → no motion rule needed (static anchor; intentional — it's the absence of motion)
- entry flourish: icon stroke-draw into mark → `svg-path-draw`
- entry flourish: concentric ripple rings from mark → `cursor-click-ripple` (ripple bloom)
- small idle mark move (rotate / sparkle reposition) → `sine-wave-loop` (idle)
- X-collapse / scale-to-0 zoom-out of typed line → `scale-swap-transition` (closest fit — it morphs/collapses elements at a shared center; approximation, since a standalone collapse-and-vanish without the paired same-center brand pop isn't its exact case)
- spring-pop brand reveal → `spring-pop-entrance` (alt `physics-press-reaction`)
- collapse-text → pop-brand as a same-center morph pair → `scale-swap-transition` (morph two elements at same center)
- wordmark unmask-slide into lockup → `techniques.md` clip-path reveal (unmask); slide via `spring-pop-entrance`
- cursor sweep onto UI control + press → `cursor-click-ripple` (cursor→target press + ripple)
- UI state-flip (base/icon invert on contact) → `hacker-flip-3d`
- radial glow bloom / accent glow-halo ring settle → `asr-keyword-glow` (accent glow); ring expansion via `center-outward-expansion`
- pill/button CTA reveal → `spring-pop-entrance` (alt `scale-swap-transition`)

**camera modifier**: none required — camera is static for both roles. The Hook ticker push is an ELEMENT translate (the typed assembly slides leftward to keep the caret centered), not a camera move → modeled by `camera-cursor-tracking` rather than a true camera rule.


<!-- ===== FILE: hyperframes/hyperframes-animation/blueprints/video-text-pivot.md ===== -->

# video-text-pivot — Video → Text Pivot

**intent**: A product video holds center and claims attention, then slides aside to hand its weight to a hero stat in the space it vacates, then both clear and kinetic text types into the center — accent words carrying the meaning the video used to carry — sealed by a gradient pill. The arc is "show → yield → pivot → stamp," and each handoff pairs an exit with a same-anchor entrance so two beats read, not four.

**roles served**

- Product_Intro (from `metric-video-text-pivot`): when the open is "see the feature" then "see the impact" and the `[product video]` must stay visible through the stat reveal — it slides, it doesn't cut.
- Key_Feature: a feature clip that yields to a frame-filling metric and a typographic impact line.

**duration**: 6–8s

**shot structure** (a `[bg]` canvas; one `[product video]` as a real muted `.mp4` clip, a hero stat, then kinetic text — each pair shares a screen anchor so the handoff reads as a weight-transfer)

- **Scene 1 (0.0–~1.6s) — the video shows.** The `[product video]` lands centered on a smooth scale-up and breathes (a small y-bob), claiming full attention. Camera static.
- **Scene 2 (~1.6–3.2s) — yield + stat (signature move).** The video SLIDES aside (x + scale down) **into the very space** the `[hero stat]` now fills as the stat pops in with 3D-depth type — one weight-transfer reading as a single event, not two. The stat breathes within this window.
- **Scene 3 (~3.2–5.0s) — pivot to text.** Both video and stat clear out and kinetic `[impact text]` TYPES into the vacated center, character by character; its `[accent words]` carry the meaning the video used to carry.
- **Scene 4 (~5.0–end) — stamp.** A gradient `[pill]` snaps shut around the closing line (`scaleX` 0→1), its glow halo resolving a beat behind so the silhouette reads before the bloom — sealing the statement as one graphic. Holds.

**motion vocabulary**: video scale-in + small breath; weight-transfer slide (video x + scale-down handing off to the stat at the same anchor); 3D-depth stat type; character-stream typing; gradient pill scaleX-snap; glow-halo bloom trailing the silhouette.

**rule mapping**

- video entrance (smooth) and the weight-transfer slide → `gsap-effects` (scale/opacity then x + scale on a long-tail `power3`); the video itself is a muted `<video class="clip">` direct child of the root
- hero stat's frame-filling 3D type → `3d-text-depth-layers` (static-depth variation — layers built at setup, no cascade fighting the entry)
- the same-anchor video-exit ↔ stat-entry handoff (if treated as a morph) → `scale-swap-transition` (shared center)
- character-by-character impact typing through segmented spans → `dynamic-content-sequencing` (clean character stream) or `discrete-text-sequence`
- pill `scaleX` snap + trailing glow halo → `gsap-effects` (scaleX) + `ambient-glow-bloom` (the halo, resolving a beat behind)
- video / stat breath within their windows → `sine-wave-loop` (low-amplitude register — subtle jitter, gated to each element's window, never a forever loop)

**camera modifier**: camera-static — all motion is element-space (the video translates), so the "pivot" is the elements moving, not a camera.


<!-- ===== FILE: hyperframes/hyperframes-animation/blueprints/zoom-out-workspace-reveal.md ===== -->

# zoom-out-workspace-reveal — Zoom-Out Workspace Reveal

**intent**: Open TIGHT on one full-bleed detail — a graphic macro or a small UI region — let micro-action play in close-up, then ONE continuous decelerating zoom-out reveals that everything seen so far lives inside a containing whole (a design-tool workspace / a multi-pane agent workspace); the frame locks at the wide and element-level payoff carries on. The zoom-out IS the narrative engine and the reveal-of-nesting is the payoff — distinct from `grid-card-assemble`, where a zoom-OUT is an optional camera modifier garnishing an element-stagger assemble; here nothing assembles, the world was whole all along, and the single outward move is what re-scopes its meaning. The structural inverse of every existing push-in shape (`constellation-hub`'s push-in, `device-surface-showcase`'s continuous push, `dataviz-countup`'s push-through).

**roles served**

- Hook (from `continuous-zoomout-nesting-reveal`): when the open should be a full-bleed graphic mystery — a blob morphing, a macro blossom blooming — resolved by one unbroken exponentially-decelerating zoom-out that passes THROUGH an intermediate composition (oversized headline / card artwork / web page) before revealing the whole thing is an artboard inside a design tool (panels, layers, inspector, timeline); the frame locks and the canvas keeps animating, ending mid-action.
- Benefits (from `close-up-open-single-zoom-out-reveal`): when the payoff is scale/breadth — micro-actions play in extreme close-up on one small UI region (file rows popping in, a highlight stepping, a guided glide down a list), then ONE fast smoothly-decelerating zoom-out (~0.5–1s) reveals the region was a corner of a huge multi-pane agent workspace (chat + artifact preview + sidebar); the wide holds static to the end while element-level payoff completes the story ("look how much the agent did — and here's the deliverable").

**duration**: 6.8–11s (Hook continuous-pull both 6.8s; Benefits dwell-then-snap 10.7–11s — the dwell and the post-lock payoff stretch, the reveal itself does not)

**HARD RULE — no zoom-in anywhere; camera static outside the single reveal.** Carried verbatim from both Benefits goldens and structurally true of both Hook goldens: the camera's only scale motion is OUTWARD. One zoom-out per shot. Before the reveal the camera either holds, glides/pans along the close-up surface, or is already running the (only) pull-back; after the reveal decelerates to a full stop the frame is LOCKED — every later change (pane swap, pane expansion, cursor travel, playhead scrub, canvas animation) is element/layout motion, never camera. No push-in, no punch, no re-zoom, no second reveal. Violating this collapses the shape back into a generic camera tour.

**shot structure** (one oversized static world — the full `[whole: workspace]` authored at final layout from frame 0 — with the camera starting scaled far in on the `[detail]`; the reveal is one scale animation on the world; two folded sub-shapes — **(A) continuous nesting pull** (Hook) and **(B) close-up dwell → snap reveal** (Benefits))

- **Scene 1 (0.0–~2.5s) — full-bleed detail + micro-action.** Extreme close-up: the `[detail: graphic macro — blob / blossom stem / small UI region — file list / browser corner]` fills the frame edge-to-edge with NO containing chrome, canvas, or neighboring panes visible. The detail PERFORMS in close-up — this beat is never a static hold:
  - _Variant — Hook (A)_: the graphic itself moves/morphs/blooms — an organic `[accent]` blob flows across and morphs into an undulating wavy line, or blurred macro forms sharpen as circular petals pop and expand outward into a flat vector `[motif]` — while the pull-back is ALREADY running underneath (the camera never waits).
  - _Variant — Benefits (B)_: camera holds (or glides) while UI micro-action plays — `[rows: filenames / list items]` pop in top-to-bottom, a soft `[highlight]` steps down row-by-row, or the camera rides down a list while gently pulling back. Optional blur-to-sharp resolve on the opening frame.

- **Scene 2 (~2.5s–reveal start) — the middle beat.** Diverges by sub-shape:
  - _Variant — Hook (A) — intermediate nesting level_: the continuing zoom-out resolves a mid-level composition, still full-bleed, still no chrome — oversized `[headline]` glyphs descend into frame as partial letterforms and settle centered (the "descent" is pure world-scale: the letters are static in world space, the camera pull produces the motion), or the `[motif]` is revealed living inside a `[card]` in a row of cards on a `[web page]`. The viewer re-scopes once — and still doesn't know the real container.
  - _Variant — Benefits (B) — close-up beat advances_: the close-up story develops at the same tightness — the view shifts to an adjacent `[panel]`, a new `[row]` fades/slides in and grows its panel, a `[cursor]` enters and hovers it with a soft highlight. This is the pre-reveal dwell; tension is "we're deep inside something."

- **Scene 3 (the reveal) — ONE decelerating zoom-out completes; frame LOCKS.** The signature move. The camera pulls back to scale 1 and eases to a full stop, revealing the containing `[whole]`:
  - _Variant — Hook (A)_: the pull is the tail of the SAME continuous zoom running since frame 0 (total travel ~4.3–4.5s of a 6.8s shot), with strong exponential deceleration — the `[intermediate composition]` turns out to be `[an artboard / a phone-screen mock]` on a `[design-tool canvas]`: light chrome, left pages/layers panel, right properties inspector, blue selection box, bottom animation timeline with keyframe bars.
  - _Variant — Benefits (B)_: the pull is a discrete rapid burst (~0.5–1s) from the held close-up — smooth, heavily decelerating — landing the full `[multi-pane agent workspace]`: left `[chat pane]` with the prompt + status + response, center/right `[artifact pane: spreadsheet / deck preview]`, optional `[sidebar: progress checklist + artifacts + context]`.
  - Both: the zoom-out ends BEFORE the shot does — always leave a post-lock act. The deceleration-to-stop is what makes the lock legible.

- **Scene 4 (lock–end) — element-level payoff on the locked wide.** The reveal is not the ending; the close-up's world keeps living inside the wide. All motion is element/layout:
  - _Variant — Hook (A)_: a `[cursor]` enters from off-frame and glides to hover/click the selected element, or a `[playhead]` scrubs left-to-right across the bottom timeline while the canvas artwork animates in sync (petals rotate about their hub, a starburst spins in place, a motif sweeps/shifts). Ends MID-ACTION — the tool is alive.
  - _Variant — Benefits (B)_: a `[file-attachment card]` fades in → the cursor clicks `[Open]` → the artifact pane swaps content via a quick white-out → the viewer pane expands full-width over its neighbor (LAYOUT motion, not camera) landing on the `[deliverable: full slide / dashboard]`; or the frame simply holds long and static while the cursor drifts to rest near the `[payoff stat]`. Struck-through checklist items in the sidebar read as completed work. Long hold to the end.

**motion vocabulary**: one continuous scale-driven zoom-out with exponential/eased deceleration (no cuts) · single fast decelerating zoom-out burst (~0.5–1s) · workspace-lock at zoom end · full-bleed no-chrome opening · blur-to-sharp macro focus resolve · organic blob flow + morph into undulating wavy line · squiggle-underline settle with residual undulation · circular petals popping/expanding outward (bloom) · oversized letters descending into frame as partial glyphs (world-scale, not element motion) · text scaling down through the frame to a centered settle · rows pop in top-to-bottom · selection highlight steps down row-by-row · camera rides/pans down a list while pulling back · new row fades/slides in and grows its panel · cursor hover with soft row highlight · cursor entering from off-frame and gliding to hover/click · timeline playhead scrub left-to-right · in-canvas rotation about a hub / spin-in-place · motif shift/sweep-in · file-attachment card fade-in · cursor click · pane content swap via quick white-out · pane expands full-width over neighbor (layout motion) · checklist items shown struck-through · long static hold · cursor drift to rest · ends mid-action (Hook).

**rule mapping** (motion verb → `rule-id`)

- the single decelerating zoom-out on the whole world → `viewport-change` (one `.world` wrapper; `cam` object as single source of truth via `onUpdate`; start `cam.scale` at the reveal ratio with `T = -offset × S` centering the detail, tween scale → 1 and translate → 0 with ONE shared ease — the detail drifts from frame-center to its home slot as the wide takes over, exactly the golden read)
- off-center detail framed at open, zoom-out to wide → `coordinate-target-zoom` ("Zoom out (target → wide view)" variation — nested wrappers, reverse phases: start zoomed on the measured target, tween outer scale → 1 + inner translate → 0 with shared duration/ease; measure the detail's center after `fonts.ready`, never hand-derive)
- pre-reveal glide/ride down a list while gently pulling back (Benefits B) → `viewport-change` (pan + scale composed on the one `cam` object) — sequencing the slow-glide → hold → fast-pull profile → `multi-phase-camera` (phase machinery; this shape runs the same scale-agnostic math at 4–12× outward — see `viewport-change`'s scale-guide range note)
- exponential deceleration-to-stop → ease selection (`expo.out` / `power4.out` on the reveal tween) — parameter guidance, no rule needed; after the stop, NO camera tweens exist on the timeline (hard rule above)
- blur-to-sharp macro resolve chorded to the early pull → `depth-of-field-blur` (refocus/settle variation: `--dof` ramps to 0 as the zoom recedes, same timeline position as the pull)
- oversized partial glyphs descending / text scaling down through the frame → no element tween — authored static in world space; `viewport-change`'s pull produces the motion (author trap: animating the letters separately double-moves them)
- organic blob flow + morph into wavy line → SVG path morph — see `hyperframes-keyframes` (morph); flagged special, like `device-surface-showcase`'s WebGL specials — substitute a non-morph accent when the capability isn't loaded
- squiggle-underline residual undulation → `sine-wave-loop` (finite bounded undulation)
- circular petals pop/expand outward (bloom) → `spring-pop-entrance` (staggered pops) + `center-outward-expansion` (petals expand from the hub to final positions)
- rows pop in top-to-bottom → `spring-pop-entrance` (staggered group, ≤500ms stagger cap) or `gsap-effects` (low-drama fade + short slide stagger)
- selection highlight steps down row-by-row → `gsap-effects` (stepped `tl.set` repositions at time thresholds — instant steps, no glide; trivial, no dedicated rule needed)
- new row fades/slides in → `spring-pop-entrance` (soft variant); its panel growing to fit → `anchored-layout-expand` (one-axis layout expansion)
- cursor enters off-frame → glides → hovers → clicks → `cursor-click-ripple` (move-to-target, co-depress, ripple); soft hover row-highlight → `gsap-effects` (background-color/opacity tween)
- timeline playhead scrub left-to-right → `gsap-effects` (linear `ease:"none"` translateX); in-sync canvas animation = place the artwork tweens at the same timeline position as the scrub (sync is free on one paused timeline)
- in-canvas rotation about a hub / spin-in-place (petal flower, starburst) → `svg-icon-enrichment` (SVG `setAttribute('transform','rotate(deg cx cy)')` for explicit centers)
- motif shift/sweep-in on a card → `gsap-effects` (masked translate) or `techniques.md` clip-path reveal
- file-attachment card fade-in → `spring-pop-entrance` (soft) / `gsap-effects` fade
- pane content swap via quick white-out → `discrete-text-sequence` (whole-state swap at a threshold) + `gsap-effects` (white flash overlay with attack-decay opacity envelope)
- pane expands full-width over neighbor (layout motion) → `anchored-layout-expand` (one-axis layout hand-off; width/height tweens stay forbidden)
- checklist items struck-through / status states → static content, or `discrete-text-sequence` if they check off on screen
- long static hold + cursor drift to rest → hold needs no rule; the drift is a single slow `gsap-effects` translate that ARRIVES somewhere meaningful (rests near the payoff stat) — it performs, it is not idle wobble
- ends mid-action (Hook) → the playhead/canvas tweens simply run to the composition edge — no exit move, no rule

**camera law — staging the one move** (the camera is the engine here, not a modifier)

- Build the ENTIRE `[whole]` workspace at final layout inside one `.world` wrapper; there is no second set. The open is `cam.scale = S0` (typically 4–12× — whatever makes the `[detail]` full-bleed) with counter-translate centering the detail; the reveal tweens to `scale 1, translate 0`. `overflow: hidden` on the scene; background on the scene, never the world.
- Crispness constraint: everything visible at open must survive S0 magnification — author the detail as DOM/vector (text, SVG, CSS shapes); any raster inside the close-up needs `sourceResolution ≥ rendered × S0`.
- Sub-shape A: the reveal tween spans ~0–4.5s with `expo.out`-class deceleration — one tween, no phases, no cuts; element beats (morph, bloom, glyph settle) are positioned along it.
- Sub-shape B: optional gentle pre-reveal pan/pull (`viewport-change` pan, or a slow scale ease-out ≤ ~15% travel) during the dwell, then the reveal burst (~0.5–1s, heavy decel) as its own tween; camera fully static after.
- Never: a zoom-in, a second zoom-out, camera motion after the lock, or replacing the reveal with a cut. One outward move is the whole grammar.

**boundary vs `grid-card-assemble`**: it already carries an optional zoom-OUT reveal modifier (glass-card / logo-wall variants), so the two shapes border each other. The test: if elements ASSEMBLE and the pull-back merely shows the assembled array in context, it's `grid-card-assemble`; if the world is whole from frame 0 and the single decelerating pull-back is itself the story — close-up mystery → nesting reveal → locked-frame payoff — it's this blueprint. Related evidence: a mined profile-page golden runs the same single UI zoom-out/scroll-up reveal at small scale inside a kinetic-type shot, corroborating the move's currency without sharing the shape.


<!-- ===== FILE: hyperframes/hyperframes-animation/references/motion-blur.md ===== -->

# Motion blur — shutter smear on any animated element

## Read this part before you blur anything

Blur is not polish. It is the smear a real shutter leaves while the subject
crosses the frame, so it only reads as correct when the subject crosses enough
of the frame to have smeared. Applied to motion that was never fast enough, it
reads as a soft, cheap render: the eye sees mush where it expected an edge.

Do not blur:

| Case                                             | Why                                                                                                    | Do instead                          |
| ------------------------------------------------ | ------------------------------------------------------------------------------------------------------ | ----------------------------------- |
| Travel under about one element-width per frame   | The copies pile up inside the element's own silhouette, so the result is a softer element, not a smear | Leave it sharp                      |
| A fade, a color change, a blur-in, a filter beat | Nothing reaches `transform`, so there is no trajectory to integrate and no smear to draw               | Leave it sharp                      |
| Text meant to be read at that moment             | A smeared word is an unreadable word, which is usually the opposite of the brief                       | Blur the approach, land sharp, hold |
| A slow drift, a parallax layer, a breathing loop | Below the half-pixel deadband it renders sharp anyway; above it, it looks like a mistake               | Leave it sharp                      |
| The whole scene, or a container of many elements | Cost is the copies of an entire subtree, and a container that never moves smears nothing inside it     | Point it at the element that moves  |

Blur the beats that snap: a slam, a whip, a hard cut in position, a spin, a
scale punch. One to three of them in a composition, not every tween.

## Two routes, and they are not interchangeable

| Route                                   | What it is                                                                                                       | Use when                                                                                                             |
| --------------------------------------- | ---------------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------- |
| The `motion-blur` registry component    | A DOM shutter synthesised in the page: N+1 additively blended copies of the element along its sampled trajectory | You want the smear visible in the preview, on selected elements, authored per element                                |
| The engine's `motionBlur` render option | The renderer integrates real sub-frame samples of the whole frame                                                | You want every moving thing smeared, including canvas, video and transformed ancestors, and only in the final render |

The component smears what a `transform` can express, on the elements you mark.
The engine smears the frame. The component is the one an agent authors; the
engine option is a render-time decision and shows nothing in a preview.

## The contract: one attribute

Paste the component's snippet into the composition, then mark the element:

```html
<div id="root" data-composition-id="hero" data-duration="4" data-fps="30">
  <div id="slam" data-hf-motion-blur></div>
  <div id="title" data-hf-motion-blur='{"shutterAngle": 360}'></div>
</div>
```

Nothing to call and no ordering to get right. A marked element is attached as
soon as its composition's timeline is registered, and the registry is also
polled for about eight seconds after load, so a composition that mounts
asynchronously is picked up too. An element takes the timeline registered under
the `data-composition-id` of its nearest ancestor carrying that attribute, so a
sub-composition's targets follow that sub-composition.

Empty attribute means defaults. Any other value must parse as a JSON object, so
it needs double quotes on the keys. A value that parses to something else,
`null` or a bare number, warns and is skipped rather than quietly taken as
defaults.

`attachMotionBlur(target, timeline, options)` is for an element created later
than that window. It has an ordering contract, after every tween so the
timeline's final duration is known, and getting it wrong is silent. For markup
that is already in the document, use the attribute.

## Options

| Option            | Default                                                      | Meaning                                                                                                                                                                                                                                                                                                         |
| ----------------- | ------------------------------------------------------------ | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `shutterAngle`    | 720                                                          | Degrees of the frame interval the shutter is open. 720 is two frames, measured off a real After Effects export. 360 is one frame. 0 disables the smear                                                                                                                                                          |
| `shutterPhase`    | -360                                                         | Degrees the window start sits from the frame time. -360 centres the window on the frame                                                                                                                                                                                                                         |
| `samplesPerFrame` | 16                                                           | Sub-intervals of the window, so this many plus one copies, each at 1 over this many opacity. Max 64                                                                                                                                                                                                             |
| `fps`             | the `data-fps` of the target's own composition root, else 30 | Composition frame rate. Pass it explicitly when rendering with an fps override                                                                                                                                                                                                                                  |
| `sharp`           | 1                                                            | 1 paints the element itself, crisp, over its smear. 0 hides it while it moves, leaving only the shutter average: a soft blur with no frame-time edge. It hides through a marker attribute, never the element's own visibility, so autoAlpha still works (an inline `visibility: visible !important` on it wins) |

A key that is none of these five, and a value that is not a finite number, are
both refused by name rather than read as defaults. `{"shutterAngle": "720deg"}`
is a refusal, not a 720 degree shutter.

There is no axis, no strength and no radius. The smear is the trajectory,
integrated; its extent is speed times shutter time and is not a free parameter.
A template that passes `axis`, `blurMax` or `blurScale` carries an older fork of
this snippet and its options do nothing in the current one.

## The failure modes are all silent

Every one of these renders a plausible-looking sharp element and reports
nothing except where noted:

| Symptom                                                                  | Cause                                                                                                               | Fix                                                                                  |
| ------------------------------------------------------------------------ | ------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------ |
| Console warns that no composition registered a timeline for an element   | The element is outside every `data-composition-id`, or that composition never registers a timeline                  | Put it inside the composition's root, or register the timeline                       |
| Console warns the attribute is not JSON                                  | Single quotes, unquoted keys, a trailing comma                                                                      | Double-quoted JSON, or an empty attribute for defaults                               |
| Console warns the attribute is not a JSON object                         | `null`, a bare number, a quoted string, an array                                                                    | An object, or an empty attribute for defaults                                        |
| Console warns the attribute names no such option                         | A misspelled key, for example `samplesperframe`                                                                     | Use one of the five names above, case-sensitive                                      |
| Console warns the attribute needs a number for an option                 | A quoted or unit-suffixed value, for example `"720deg"`                                                             | A bare JSON number                                                                   |
| Console warns it cannot blur a target inside another target              | Both an element and one of its ancestors carry the attribute                                                        | Mark one of them, the one that moves                                                 |
| Console warns one call cannot blur compositions at different frame rates | One `attachMotionBlur` call named elements in two compositions whose `data-fps` differ                              | One call per composition                                                             |
| Console warns a second timeline registered for an element                | The same `data-composition-id` key was registered twice with different timelines; the copies still follow the first | Register once per composition                                                        |
| No smear, no warning                                                     | The beat animates `left`, `top`, `width` or `height`; the snippet reads the resolved `transform`                    | Animate `x`, `y`, `scale`, `rotation`                                                |
| No smear on a container's children                                       | The marked element does not move; its children do                                                                   | Mark the elements that move                                                          |
| A smear that lags the element                                            | A transformed ancestor is doing the moving                                                                          | Move the element itself, or use the engine route                                     |
| Blur only on the first frame, or never in a preview                      | The host never seeks the timeline                                                                                   | HyperFrames seeks every frame; a paused timeline nobody seeks shows nothing          |
| A smear left behind in the old parent                                    | The target was reparented after attaching; the group stays where it was inserted and is never moved                 | Do not reparent a blurred element. Animate `x`/`y` instead, or attach after the move |
| A selector stops matching after attaching                                | A copy keeps the element's classes, because a class rule is the only thing that can style a copy's pseudo-elements  | Address the element by id or by reference, never by a class a copy also carries      |

## Cost

Each target costs N+1 copies of its whole subtree. Those are restyled on attach
and on resize, and re-transformed every frame, and the timeline is seeked N+1
times per frame to sample the trajectory. At the default 16 that is 17 copies
and 17 seeks per target per frame. Three marked elements is fine. Thirty is a
different render.

Drop `samplesPerFrame` before you drop the effect: 8 halves the cost and the
staircase is still smooth on a fast beat.

## The numbers, so you can argue with them

The defaults are measured against a 1920x1080 30 fps After Effects export of
translating text, not chosen. In that export the outermost trailing copy sits
exactly at the previous frame's position and the outermost leading copy exactly
at the next frame's, with 8 evenly spaced copies between on each side: a window
of two frames, phase minus one frame, 16 sub-intervals. The staircase across a
stroke steps by 0.063 plus or minus 0.002 of the sharp text intensity, a flat
1/16 per copy with no taper toward the window edges. Triangle weighting scores
1.6 dB worse against the same export.

Per-beat PSNR against that reference, sharp render versus this component:
translate +3.38 dB, scale +0.62, rotate X +0.43, rotate Y +0.84, rotate Z
+1.15. A beat that only scales or only rotates smears, which the earlier
SVG-filter stage could not do.

## See also

`../../../registry/components/motion-blur/motion-blur.html` is the snippet and its
full header. `shutter-slam` is the same model as an installable component: the
After Effects reference case, six beats, elastic to the container.


<!-- ===== FILE: hyperframes/hyperframes-animation/rules-index.md ===== -->

# Rules Index

Atomic motion recipes. Each lives at `rules/<name>.md`. Compose 2-4 per scene with a single paused timeline.

## The contract — every rule assumes this

Stated once here so individual rules don't repeat it. Every recipe in `rules/`:

- runs on ONE **paused** GSAP timeline registered on `window.__timelines` (never autoplay, never a second timeline);
- is **seek-safe both directions**: `fromTo` with explicit from-states (t=0 correct under seek; `immediateRender: false` when re-owning a target), absolute values — never relative `+=` tweens; state readable as a pure function of timeline time, no mutable trackers;
- is **deterministic**: no `Math.random()`, no `Date.now()` — index-derived pseudo-random and baked schedules only; finite repeats (`repeat: -1` only under a finite root `data-duration`);
- animates **transforms and paint-only properties** — `width`/`height`/`top`/`left` tweens are forbidden (use scale/translate proxies, masks, or `anchored-layout-expand`);
- caps group staggers so an arrival reads as one beat (`items × stagger ≤ ~0.5s`);
- puts **no CSS `transition`** on animated elements (they interpolate independently of seek and flicker) and hints compositors with `will-change: transform` where many tweens run at once;
- measures DOM (`offsetHeight`, `getBoundingClientRect`) at build time only in a **single-scene** composition — in a multi-scene montage, later clips may not be laid out yet: use authored CSS-matched constants;
- lives inside a standard scene clip per `hyperframes-core` (`class="clip"` + `data-*` timing) — rule snippets show mechanism DOM only, not the scene scaffold.

A rule's own **Critical Constraints** section lists only what is SPECIFIC to that rule beyond this contract.

## Text & Typography

<rules>
<hacker-flip-3d path="rules/hacker-flip-3d.md">Character-level 3D rotation with deterministic glyph substitution (decryption). GSAP `back.out` ease + per-glyph `onUpdate` for the flicker hash. Tags: text, 3d, reveal, decode</hacker-flip-3d>
<vertical-spring-ticker path="rules/vertical-spring-ticker.md">Slot-machine vertical scrolling using stepped GSAP tweens within a masked column. Tags: text, ticker, scroll, vertical</vertical-spring-ticker>
<counting-dynamic-scale path="rules/counting-dynamic-scale.md">Counter where transform scale grows with the value for escalating emphasis. A numeric proxy and scale tween share one timeline position. Tags: counter, scale, transform, number, dynamic</counting-dynamic-scale>
<discrete-text-sequence path="rules/discrete-text-sequence.md">Replace entire text states at time thresholds for non-linear typing (typos, holds, bulk additions, backspaces). GSAP onUpdate-driven reverse search. Tags: text, typing, discrete, threshold, non-linear</discrete-text-sequence>
<asr-keyword-glow path="rules/asr-keyword-glow.md">Highlight keywords with glow + scale + color synced to ASR word timestamps. Two GSAP tweens per word drive a CSS custom property `--glow` through attack-decay-rest envelope. Tags: asr, audio-sync, highlight, glow, keyword, text</asr-keyword-glow>
<3d-text-depth-layers path="rules/3d-text-depth-layers.md">Multiple offset text layers (N divs at `(i*dx, i*dy)` with decreasing alpha) create a stacked 3D extrusion illusion on large typography. Tags: text, 3d, depth, layers, shadow, typography, stacked</3d-text-depth-layers>
<context-sensitive-cursor path="rules/context-sensitive-cursor.md">Typing cursor whose `background-color` switches at segment boundaries plus square-wave blink via `(tl.time() % cycle) < cycle/2`. Tags: cursor, color, context, typewriter, styling, segment</context-sensitive-cursor>
<dynamic-content-sequencing path="rules/dynamic-content-sequencing.md">Pre-compute a flat `[{startTime, endTime, ...}]` array from a script of `{textMain, textAccent, charSpeed, hold}` entries. Each phrase's window = `chars × charSpeed + hold`. Content-driven duration, no hand-tuned offsets. Tags: timeline, sequencing, dynamic, duration, script-driven</dynamic-content-sequencing>
<kinetic-beat-slam path="rules/kinetic-beat-slam.md">Percussive kinetic typography — short phrases slam in on ONE shared beat array with DISTINCT per-phrase entrances (scale-slam / side-snap / rise-rotate), optional rhythm chrome (metronome ticks, beat bar), then a locked finale. The recipe for "punchy / rhythmic" taglines. Tags: text, kinetic, typography, beat, rhythm, slam, percussive, punchy</kinetic-beat-slam>
<gradient-text-sweep path="rules/gradient-text-sweep.md">A gradient tweened THROUGH letterforms — `background-clip: text` + an oversized-background `backgroundPosition` tween. Continuous sweep across a held headline, traveling word-to-word highlight (stacked-copy opacity envelopes), or a hue-sweep that settles to a solid via a pixel-identical twin crossfade. Glyphs never move; finite, seek-safe. Tags: gradient, text, sweep, background-clip, highlight, hue, headline</gradient-text-sweep>
<chromatic-glitch path="rules/chromatic-glitch.md">RGB-split / slice glitch that snaps sharp — offset color copies jitter on a deterministic hash of QUANTIZED timeline time (never Math.random), or horizontal slice bands displace and converge under a stepped ease; brief vibration, clean resolve, clamped rest state. Entrance stretch, emphasis burst, and slice-reveal forms. Tags: glitch, rgb-split, chromatic, slice, jitter, stutter, snap</chromatic-glitch>
</rules>

## Data & Stats

<rules>
<counting-dynamic-scale path="rules/counting-dynamic-scale.md">Counter whose transform scale grows with the value; seek-safe `onUpdate`, `Math.round`, `tabular-nums`, multi-stat chord. (Also listed under Text & Typography.) Tags: counter, number, stat, count-up</counting-dynamic-scale>
<stat-bars-and-fills path="rules/stat-bars-and-fills.md">Data-viz primitives that pair a number with a graphic — growth bars (CSS `scaleY` stagger), progress fill (bar `scaleX` or measured SVG ring), and fractional star-rating wipe (`clip-path`). Transforms only, seek-safe. Pick single-focus vs split-frame and hold it. Tags: data, stats, chart, bars, progress, ring, stars, rating, infographic</stat-bars-and-fills>
<chart-scrub-readout path="rules/chart-scrub-readout.md">Cursor/playhead scrubs an already-drawn chart — ONE driver moves a vertical tracking line + marker along a baked data polyline while a date/value tooltip steps through the data array (text writes only on index change); second series can activate on cross. Chart arrival belongs to `stat-bars-and-fills` / `svg-path-draw`; this is the read head. Tags: chart, scrub, tooltip, readout, tracking-line, data, playhead</chart-scrub-readout>
</rules>

## Camera & Viewport

<rules>
<coordinate-target-zoom path="rules/coordinate-target-zoom.md">Zoom into non-centered elements via scale (outer wrapper) + counter-translation (inner wrapper). Tags: camera, zoom, scale, translate</coordinate-target-zoom>
<camera-cursor-tracking path="rules/camera-cursor-tracking.md">Two-phase virtual camera that locks the viewport to a moving focal point (typing cursor) — static initial framing then focal-point-locked tracking. Uses browser-native `getBoundingClientRect()` / `ctx.measureText()` after `document.fonts.ready`. Tags: camera, tracking, viewport, two-phase, typing</camera-cursor-tracking>
<multi-phase-camera path="rules/multi-phase-camera.md">Sequential camera-zoom system (pull-back / focus / push) plus continuous micro-drift. Tags: camera, zoom, phase, drift, scale, cinematic</multi-phase-camera>
<viewport-change path="rules/viewport-change.md">Virtual camera — simulate zoom / pan / focus-lock by transforming a single `.world` wrapper containing all scene content. Single-element composite transform `translate(x,y) scale(S)`; counter-translate math is `T = -offset × S` (DIFFERENT from coordinate-target-zoom's `T = -offset`). Tags: viewport, camera, zoom, pan, focus-lock</viewport-change>
<3d-camera-flight path="rules/3d-camera-flight.md">Perspective camera FLIGHT through a 3D-laid-out world — one static `perspective` stage + `preserve-3d` `.world` whose pose (`translate3d` + `rotateX`/`rotateY`) is tweened leg-by-leg from a single camera state object: dive into an angled grid, tilt-to-flatten pull-back, flight past standing cards, decelerate-into-focus. `power4.out` landings, `power2.inOut` repositioning; DoF via depth-of-field-blur on non-focal planes. The only camera rule that rotates/travels in Z (the other three are 2D scale+translate). Tags: camera, 3d, flight, perspective, rotateX, translateZ, dive, tilt</3d-camera-flight>
<depth-of-field-blur path="rules/depth-of-field-blur.md">Selective rack-focus — GSAP-tween `filter: blur()` (+ slight opacity dim) on off-focus layers via a `--dof` var while the focal element stays sharp; single pull, two-plane rack, or blur-the-cluster-while-pushing-in. Finite, deterministic, seek-safe. Tags: blur, depth-of-field, focus, rack-focus, dim, spotlight</depth-of-field-blur>
</rules>

## Layout & Network

<rules>
<avatar-cloud-network path="rules/avatar-cloud-network.md">Avatars on an elliptical ring with SVG connection lines to a center point, staggered entry. Cloud center coordinates must match the centerpiece element exactly. Tags: avatar, cloud, network, social-proof, stagger</avatar-cloud-network>
<3d-page-scroll path="rules/3d-page-scroll.md">Full webpage rendered as a tilted 3D card whose internal content scrolls to reveal specific sections. Pair with asr-keyword-glow for on-page keyword highlighting. Tags: 3d, page, scroll, webpage, tilt, perspective, product-demo</3d-page-scroll>
<center-outward-expansion path="rules/center-outward-expansion.md">Elements start clustered at screen center and expand outward to final positions. Each element gets its target position via CSS once; GSAP tweens transform `x` / `y` offsets to 0 in lockstep with a shared driver. Tags: expansion, scatter, center, reveal, layout, sync</center-outward-expansion>
<split-tilt-cards path="rules/split-tilt-cards.md">Two cards side-by-side with opposing rotationY tilts (+/- baseTilt) and entry slides from their respective sides. Continuous floating runs in phase opposition (`Math.PI` offset). Tags: 3d, cards, split, tilt, comparison, symmetric</split-tilt-cards>
<orbit-3d-entry path="rules/orbit-3d-entry.md">Elements flip in from 3D space (`rotateX` + `rotateY` + `translateZ`) then settle into a continuous elliptical orbit. **Critical**: entry MUST flip in-place at the orbital starting position (`gsap.set` BEFORE phase 1), not at scene center. Tags: orbit, 3d, flip, ellipse, circular, icon, entry, continuous</orbit-3d-entry>
<ai-tracking-box path="rules/ai-tracking-box.md">AI detection overlay — yellow `#facc15` L-bracket corners + confidence label (fluctuating 95-99%) following a target on a sine arc path. Box position recomputed per-frame from target position (never tweened separately). Tags: ai, tracking, bounding-box, detection, corner, ml</ai-tracking-box>
<depth-scatter-assemble path="rules/depth-scatter-assemble.md">N elements scatter into / reassemble from a rotating 3D depth-cloud — each starts at a deterministic index-derived 3D offset (translateZ + rotateX/Y + scatter) and settles to a clean flat layout; tumble-swap and radial-explode variants. preserve-3d + perspective, transform-only, seek-safe. Tags: 3d, scatter, assemble, tumble, depth, perspective, glyphs</depth-scatter-assemble>
<anchored-layout-expand path="rules/anchored-layout-expand.md">Edge-pinned container grows/collapses along ONE axis and in-flow content reflows — pill springs open into a dropdown, panel grows a sub-task stack, input card steps taller as typed text wraps, pane expands over a neighbor. Transform-only (layout authored expanded; mask + sheet slide, or proxy-driven scaleY + inverse counter-scale) since width/height tweens are forbidden; the push on following content shares the SAME tween so the seam never separates. Tags: expand, collapse, anchored, dropdown, accordion, panel, reflow, push, mask, counter-scale</anchored-layout-expand>
</rules>

## SVG & Icons

<rules>
<svg-icon-enrichment path="rules/svg-icon-enrichment.md">Animate internal SVG elements (rotating hands, oscillating blades, pulsing dots, dash-flow lines) so icons feel alive. **Critical**: use SVG `setAttribute('transform', 'rotate(deg cx cy)')` for explicit center — CSS `transform-origin` + `transform-box: fill-box` interprets origin in bbox-local coords (off-center for thin lines). Tags: svg, icon, animation, micro-animation, rotation, pulse</svg-icon-enrichment>
<svg-path-draw path="rules/svg-path-draw.md">SVG outline draws itself stroke-by-stroke via `stroke-dasharray` / `stroke-dashoffset`. Measure with `getTotalLength()` at composition setup, set initial dashoffset = length, GSAP tweens to 0. For circular progress rings, rotate the stroke `-90deg` so drawing starts at 12 o'clock. Tags: svg, stroke, draw, vector, path, dasharray</svg-path-draw>
</rules>

## Idle & Ambient

<rules>
<sine-wave-loop path="rules/sine-wave-loop.md">Continuous breathing/idle ambient motion. Two forms: GSAP `sine.inOut` yoyo with finite repeats (preferred when standalone) or onUpdate reading `tl.time()` (preferred when multiplying onto another live value). Tags: idle, loop, breathing, sine, ambient</sine-wave-loop>
<ambient-glow-bloom path="rules/ambient-glow-bloom.md">Un-triggered soft radial glow that blooms in behind a hero element and holds with a bounded idle breathe, or a single-pass traveling sheen across a surface. No click, no word-sync; peak opacity ≤ ~0.45, finite/deterministic. Tags: glow, bloom, ambient, radial, sheen, hero</ambient-glow-bloom>
</rules>

## Transition & Motion

<rules>
<reactive-displacement path="rules/reactive-displacement.md">Physical-collision transition where an entering element's GSAP tween drives the exiting element's displacement. Three concurrent tweens at the same timeline position with victim durations 40-50% of the intruder's. Tags: transition, physics, collision, displacement, push</reactive-displacement>
<press-release-spring path="rules/press-release-spring.md">Tactile button press: linear compression then spring recovery via two adjacent GSAP tweens on the same property. Variations: color transition, shadow depth via CSS vars, release burst, background glow. Tags: spring, press, button, interaction, physics, glow, burst</press-release-spring>
<physics-press-reaction path="rules/physics-press-reaction.md">Physical click simulation — two sequential GSAP scale tweens (down to 0.9, up to 1.0) approximate a spring with overshoot. Pass a single targets array `["#cta", "#cursor"]` to compress both together for tactile contact feel. Tags: spring, click, physics, press, interaction, cursor</physics-press-reaction>
<cursor-click-ripple path="rules/cursor-click-ripple.md">Animated cursor moves to a target, depresses cursor + target together on click, emits an expanding ripple with attack-decay opacity envelope. Element lives in DOM from t=0 with `opacity: 0` (no conditional rendering). Tags: cursor, click, ripple, interaction, mouse, button, keyframes</cursor-click-ripple>
<cursor-drag path="rules/cursor-drag.md">The drag verb for driven cursors — grab (press dip + lift), travel (semi-transparent ghost rides the cursor in exact lockstep via matched tweens), drop-snap into a placed field with selection chrome. Variants: fill-handle auto-fill (linear travel + stepped `tl.set` cell reveals), corner-handle proportional resize (uniform scale, origin at the anchor corner — never width/height), grab-lift-reorder (tilt + shadow, neighbor springs into the vacated slot). Tags: cursor, drag, drop, ghost, handle, resize, reorder, snap, interaction</cursor-drag>
<multi-cursor-choreography path="rules/multi-cursor-choreography.md">N (2–4) labeled independent cursor actors work one canvas simultaneously — collaborative-canvas ambience. Per-actor deterministic waypoint tables (explicit fromTo legs + rests), name-tag pills in distinct colors, grab/drop/hover actions at chorus intensity on an interleaved beat grid (one payoff at a time, zone-partitioned paths, no collisions); camera locked — any pan is the canvas group translating. Tags: cursor, multi-cursor, collaboration, ensemble, canvas, name-tag, choreography, ambient</multi-cursor-choreography>
<control-target-sync path="rules/control-target-sync.md">Live-sync couple — a scrubbed/typed/picked control and its bound target change in the SAME beat: readout tween + target transform tween share one timeline label, duration, and ease (continuous scrub), or one threshold state array carries both sides (per-keystroke / dropdown-pick steps). Distinct from `reactive-displacement` (collision physics, one-shot transition). Tags: control, scrub, live-sync, mirror, panel, editor, readout, ui</control-target-sync>
<scale-swap-transition path="rules/scale-swap-transition.md">Coordinated morph between two DOM elements at the same screen center. Exit cluster shrinks + fades; entrance pops in with `back.out(2)` overshoot. Tags: transition, morph, scale, swap</scale-swap-transition>
<card-morph-anchor path="rules/card-morph-anchor.md">Container morphs apparent size + corner radius + surface treatment between two shots, then fades to reveal the real target underneath. HyperFrames substitutes uniform `scale` for the forbidden `width`/`height` tween, plus paint-only `borderRadius`/`background`/`boxShadow`. Tags: morph, anchor, transition, border-radius, container, shape, handoff</card-morph-anchor>
<theme-crossfade-morph path="rules/theme-crossfade-morph.md">Whole-theme in-place morph under a fixed anchor — background, typography, radii, icons, chrome and logos blend simultaneously (~0.3s) through N pre-styled skins while one anchor element never moves. Stacked complete layers + opacity-only crossfade, anchor rendered once on top (or per-layer at identical geometry); static camera. Single container instead → `card-morph-anchor`. Tags: theme, skin, crossfade, morph, anchor, reskin, cycle, ui</theme-crossfade-morph>
<spring-pop-entrance path="rules/spring-pop-entrance.md">The canonical ENTRANCE pop — an element (or staggered group) arrives by springing `scale: 0 → 1` with `back.out` overshoot, `fromTo` so it's correct at t=0 under seek. Single hero, staggered group (≤500ms cap), overshoot tuned by personality. Distinct from `press-release-spring` (a click/press reaction). Tags: spring, entrance, pop, scale-in, overshoot, stagger, arrival</spring-pop-entrance>
<motion-blur-streak path="rules/motion-blur-streak.md">Fake directional velocity blur on a fast entrance / camera push-through — blur peaks at max speed, resolves to 0 at the settle. Two paths: SVG `feGaussianBlur` stdDeviation on the motion axis (proxy-tweened), or a deterministic echo/ghost trail that collapses into the lead. Entrances / mid-shot only. Per-frame-driven form for an element riding a baked track: velocity-gated text-free silhouette ghosts (or a rotate/blur/counter-rotate filter sandwich when a true blur is the look), streak axis from `atan2` of the track delta. Tags: motion-blur, streak, velocity, ghost, echo, fast, driven, tracked</motion-blur-streak>
<waterfall-entry path="rules/waterfall-entry.md">Staggered ARRIVAL cascade — words/elements whip in from below, each starting before the previous settles, an accelerating wave that resolves composed. Title cards, segment openers, list intros. Binary 0→1 opacity via `tl.set` — never fade an arrival. Tags: entrance, cascade, stagger, kinetic-text, title-card, arrival, waterfall</waterfall-entry>
<particle-burst path="rules/particle-burst.md">Deterministic particle / confetti events — confetti pop that bursts up and drifts down on gravity (optional instant-shrink), dot burst from behind text, glyph dissolve to particles. Fixed pool, index-seeded launch values, one `ease: "none"` driver whose onUpdate computes each particle as a pure ballistic function of time — scrub-safe mid-flight, ≤ ~40 particles. Tags: particles, confetti, burst, dissolve, ballistic, deterministic, punctuation</particle-burst>
<nudge-curve path="rules/nudge-curve.md">Slow-fast-slow three-phase group slide (power3.in ramp → linear burst → power4.out tail, 10/65/25 distance, tail ≥3× ramp-in) to reposition a composed group and reveal content during the burst. Tags: slide, reposition, group-motion, nudge, slow-fast-slow</nudge-curve>
</rules>

## Effect Recipes (moved from hyperframes-creative)

<rules>
<gsap-effects path="rules/gsap-effects.md">Drop-in GSAP timeline patterns — typewriter, audio visualizer, and other reusable choreography blocks. Tags: gsap, recipe, drop-in, typewriter, audio-visualizer</gsap-effects>
<css-marker-patterns path="rules/css-marker-patterns.md">Pure CSS + GSAP implementations of marker-highlight drawing modes — highlight (yellow sweep), circle (hand-drawn ellipse), burst (radiating lines), scribble (chaotic), sketchout (rough rectangle outline). Tags: css, marker, highlight, text, emphasis</css-marker-patterns>
</rules>

## See Also

- `blueprints-index.md` — the scene-shape templates (this skill's "blueprints") that compose these rules into full shots
- `techniques.md` — broader motion-design techniques (SVG path drawing, Canvas 2D, CSS 3D, kinetic type, variable fonts, compositing); a few rules cite it
- `transitions/` — scene-transition catalog (shared skill; story owns `transition_in`, the harness injects it)


<!-- ===== FILE: hyperframes/hyperframes-animation/rules/3d-camera-flight.md ===== -->

---
name: 3d-camera-flight
description: Perspective camera FLIGHT through a 3D-laid-out world — one static perspective stage + preserve-3d world whose pose (translate3d + rotateX/rotateY) is tweened leg-by-leg from a single camera state object. Dive into an angled grid, tilt-to-flatten pull-back, continuous flight past standing cards, decelerate-into-focus. Hard power4.out landings, power2.inOut repositioning; DoF via depth-of-field-blur on non-focal planes.
metadata:
  tags: camera, 3d, flight, perspective, preserve-3d, rotateX, rotateY, translateZ, dive, tilt, world, cinematic
---

# 3D Camera Flight

Every other camera rule here is a **2D camera**: [viewport-change.md](viewport-change.md), [multi-phase-camera.md](multi-phase-camera.md), and [coordinate-target-zoom.md](coordinate-target-zoom.md) simulate the camera with `scale` + `translate` on a flat wrapper — the lens never tilts, and there is no depth axis to travel along. [3d-page-scroll.md](3d-page-scroll.md) is a **static tilt**: one angle held all scene while content scrolls inside. This rule is the missing camera that _flies_ — dives into an angled grid, pulls back while the world rotates flat, streaks past standing cards, decelerates out of a blur into focus: a **perspective camera traveling with `rotateX` / `rotateY` / `translateZ` through a 3D-laid-out world**, under the same single-camera discipline as `viewport-change`: **one perspective wrapper, one camera state object, one transform writer**, every leg a sequenced tween on that state.

## How It Works

Five layers, strictly separated:

1. **The lens** — `perspective: PERSPECTIVE_PX` on a static `.stage` wrapper. Set once, never tweened, never moved. Changing perspective mid-shot reads as the lens itself warping, not the camera moving.
2. **The world** — a `.world` div with `transform-style: preserve-3d`, laid out at final 1× size: the ground surface (grid, form card, canvas) as flat DOM, optional **props** (a giant date number, a floating label) at static `translateZ(PROP_Z)` offsets so travel produces parallax, and **standing cards** counter-tilted to face the camera at their landing pose.
3. **The camera state** — a single object `cam = { x, y, z, rx, ry }` (the world's pose), written to `world.style.transform` by ONE function, `applyCamera()`, in a **fixed order**: `translate3d(x, y, z) rotateX(rx) rotateY(ry)`. With translate composed _outside_ the rotations, `x`/`y`/`z` always move the world along **screen axes** no matter how it is currently tilted — pan is always sideways, `z` is always toward/away from the lens. Put the rotations first and every leg's numbers change meaning as the tilt changes.
4. **The legs** — sequential tweens on `cam`, each one camera move: dive in (`power4.out` — violent arrival, sharp settle), tilt-to-flatten pull-back (`power2.inOut` — a repositioning, no slam), lateral flight, final dive. Camera intent inverts onto the world pose exactly as in `viewport-change`: camera flies **in** → world `z` **increases** (comes toward the lens); camera pans **right** → world `x` **negative**; camera tilts **down** over the surface → world `rx` **positive** (far edge tips away).
5. **Depth cues** — DoF via [depth-of-field-blur.md](depth-of-field-blur.md) `--dof` tweens on the **non-focal planes** (cards, props — leaf elements, never the world itself), and velocity blur on travel legs via [motion-blur-streak.md](motion-blur-streak.md)'s Camera-Travel Carve-Out — applied to the **stage**, never the world (a `filter` on a `preserve-3d` element flattens it).

Landing poses are **authored, not derived**: set `cam` to candidate values at design time, call `applyCamera()`, screenshot, adjust, bake the numbers as constants. There is no counter-translate formula to get wrong in 3D — the pose IS the design decision. Never measure per-frame (`getBoundingClientRect` in `onUpdate` desyncs under parallel frame sampling), and don't hand-derive 3D projections — your eye at design time beats the math.

## Recipe

```html
<!-- The lens: static perspective, nothing else. -->
<div class="stage">
  <!-- The world: preserve-3d, laid out at final 1× size; the camera flies by
       tweening THIS element's pose. Travel legs push content past the frame
       edges by design — hence data-layout-allow-overflow. -->
  <div class="world" id="world" data-layout-allow-overflow>
    <div class="surface">
      <div class="grid">{gridCells}</div>
      <div class="card layer" id="card-a" data-depth="0">{cardA}</div>
      <div class="card layer" id="card-b" data-depth="0">{cardB}</div>
    </div>
    <!-- Foreground props float at PROP_Z for parallax; they blur and fly past,
         never carry a read. -->
    <div class="prop layer" data-depth="2" style="--px: PROP_X; --py: PROP_Y">{propGlyph}</div>
  </div>
</div>
```

```css
.scene {
  overflow: hidden; /* travel legs push world content past the frame on purpose */
  background: {sceneBg}; /* the void the flight exposes at frame edges — must be a
     designed surface (deep brand color / soft gradient), never default white */
}
.stage {
  position: absolute;
  inset: 0;
  perspective: PERSPECTIVE_PX; /* THE LENS — static, never tweened */
  /* travel blur (motion-blur-streak carve-out) attaches HERE, never on .world */
}
.world {
  position: absolute;
  inset: 0;
  transform-style: preserve-3d;
  transform-origin: 50% 50%;
  will-change: transform;
  /* keep CLEAN: no filter, opacity < 1, overflow, clip-path, or mask — each
     flattens preserve-3d. Background on .scene, blur on .stage or leaf cards. */
}
.surface {
  position: absolute;
  inset: WORLD_INSET; /* world runs larger than the frame so travel has runway */
  transform-style: preserve-3d;
}
.prop {
  position: absolute;
  left: var(--px);
  top: var(--py);
  /* static world-space pose; counter-tilt faces the camera at the dive pose */
  transform: translateZ(PROP_Z) rotateX(PROP_COUNTER_TILT);
}
.layer {
  --dof: 0px; /* DoF channel per depth-of-field-blur — leaf elements only */
  filter: blur(var(--dof));
  will-change: filter;
}
```

```js
const world = document.getElementById("world");

// Camera state — the ONLY source of truth for the world's pose. Every leg
// tweens this object; nothing else touches world.style.transform.
const cam = { x: 0, y: 0, z: WIDE_Z, rx: 0, ry: 0 };

function applyCamera() {
  // Fixed order: translate OUTSIDE the rotations → x/y/z stay screen-aligned
  // at any tilt. Changing this order changes what every baked pose means.
  world.style.transform = `translate3d(${cam.x}px, ${cam.y}px, ${cam.z}px) rotateX(${cam.rx}deg) rotateY(${cam.ry}deg)`;
}
applyCamera(); // seed frame 0 so a seek to t=0 renders the opening pose

// ── LEG 1 — DIVE IN: wide establishing pose → angled close-up on card A.
// fromTo states the opening pose explicitly; power4.out = violent arrival,
// razor-sharp settle. Travel blur: motion-blur-streak carve-out on .stage.
const DIVE_POSE = { x: DIVE_X, y: DIVE_Y, z: DIVE_Z, rx: DIVE_RX, ry: DIVE_RY };
tl.fromTo(
  cam,
  { x: 0, y: 0, z: WIDE_Z, rx: 0, ry: 0 },
  { ...DIVE_POSE, duration: DIVE_DUR, ease: "power4.out", onUpdate: applyCamera },
  DIVE_AT,
);
// Decelerate-INTO-FOCUS: non-focal planes' --dof ramps to BLUR_PER_DEPTH × data-depth
// on the SAME window/ease (depth-of-field-blur focal pull); card A stays at --dof: 0.

// ── LEG 2 — TILT-TO-FLATTEN PULL-BACK: every channel returns to neutral on ONE
// power2.inOut tween — a reposition, not a slam. DoF releases on the same window
// so the flat overview arrives fully crisp.
const FLAT_POSE = { x: 0, y: 0, z: 0, rx: 0, ry: 0 };
tl.to(
  cam,
  { ...FLAT_POSE, duration: FLATTEN_DUR, ease: "power2.inOut", onUpdate: applyCamera },
  FLATTEN_AT,
);
tl.to(".layer", { "--dof": "0px", duration: FLATTEN_DUR, ease: "power2.inOut" }, FLATTEN_AT);

// ── LEG 3 — LATERAL FLIGHT: screen-aligned pan (translate is outside the
// rotations, so x is a pure sideways move even mid-tilt).
tl.to(cam, { x: PAN_X, duration: PAN_DUR, ease: "power2.inOut", onUpdate: applyCamera }, PAN_AT);

// ── LEG 4 — FINAL DIVE onto card B: same grammar as leg 1; card A racks OUT of
// focus as card B racks in (depth-of-field-blur rack, shared window).
const LAND_POSE = { x: LAND_X, y: LAND_Y, z: LAND_Z, rx: LAND_RX, ry: LAND_RY };
tl.to(
  cam,
  { ...LAND_POSE, duration: LAND_DUR, ease: "power4.out", onUpdate: applyCamera },
  LAND_AT,
);
tl.to("#card-a", { "--dof": `${MAX_BLUR}px`, duration: LAND_DUR, ease: "power4.out" }, LAND_AT);
tl.to("#card-b", { "--dof": "0px", duration: LAND_DUR, ease: "power4.out" }, LAND_AT);
// Landing dwell: ≥1 s of stillness on card B — unless ending held mid-dive.
```

## Variations

- **Continuous flight past standing cards** — one long leg instead of dive-land-dive: sustained `z` + `x` travel (2–4 s, `power2.inOut` / `power1.inOut` near-constant cruise) through a corridor of cards and props at staggered `PROP_Z`. Parallax does the work — near props streak past while far ones crawl. Keep ONE plane sharp at a time via staggered `--dof` tweens. Props crossing the camera plane (`cam.z + PROP_Z` approaching `PERSPECTIVE_PX`) blow up to fill the frame and vanish — that IS the fly-past; never let a focal card cross it.
- **End held mid-dive** — give the final leg a window that overruns the composition (`LAND_AT + LAND_DUR > data-duration`); the last frame holds mid-tween — still traveling, blur not fully resolved. Seek-safe by construction (a seek to the last frame lands at a deterministic pose); don't fake it with a shorter leg plus a manual offset. Use when the brief wants momentum at the cut, not rest.
- **Whip sweep** — the heavily motion-blurred lateral whip that resolves into the next region: leg 3 driven by [nudge-curve.md](nudge-curve.md)'s three-phase chain (burst-dominant) on `cam.x`, with [motion-blur-streak.md](motion-blur-streak.md)'s Camera-Travel Carve-Out on the same window — blur ramps through the ramp-in, rides the burst at peak, resolves to 0 through the `power4.out` tail. Full recipe in that carve-out.
- **Hold drift (the hold never dies)** — between legs, fold `multi-phase-camera`-style micro-drift **through the same writer**: a driver tween writes tiny `dx`/`dy`/`drx` into a `drift` object and `applyCamera()` composes `cam.x + drift.dx`, `cam.rx + drift.drx`, etc. Never let drift write `world.style.transform` itself — two writers on one transform is the classic camera bug. Amplitudes per `multi-phase-camera` (2–8 px), rotation drift ≤ 0.5°.

## Values

| token                     | range                                                            | notes                                                                                                                                                                                     |
| ------------------------- | ---------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| PERSPECTIVE_PX            | 700–1400 px (moving cam best 800–1200)                           | smaller = wilder foreshortening, more violent dives; larger = near-orthographic, the flight flattens                                                                                      |
| WORLD_INSET               | −50% to −150% per side                                           | world 2–4× the frame so lateral legs have runway                                                                                                                                          |
| PROP_Z                    | 80–300 px                                                        | higher = stronger parallax, earlier fly-past                                                                                                                                              |
| PROP_COUNTER_TILT         | ≈ `-LAND_RX` of the leg that reads it                            | author by eye and bake                                                                                                                                                                    |
| DIVE_RX / LAND_RX         | 30–55°                                                           | "angled grid" starts ~30°; \|rx\| ≤ ~65°, \|ry\| ≤ ~30° — beyond that flat planes go edge-on, text unreadable                                                                             |
| DIVE_Z / LAND_Z           | 300–700 px at PERSPECTIVE_PX ≈ 1000                              | **Z budget**: `cam.z + PROP_Z ≤ ~0.6 × PERSPECTIVE_PX` for readable content — near the perspective distance, scale blows toward infinity and elements invert/vanish past the camera plane |
| WIDE_Z                    | −100 to −400 px                                                  | negative z = world pushed away = camera wide                                                                                                                                              |
| DIVE_X/Y, LAND_X/Y        | read off a screenshot at the baked tilt                          | screen-aligned (translate outside rotations)                                                                                                                                              |
| DIVE_DUR / LAND_DUR       | 0.6–1.0 s                                                        | commitment, not a polite zoom; under 0.5 s reads as a cut                                                                                                                                 |
| FLATTEN_DUR               | 1.2–2.0 s                                                        | the repositioning is the breath between dives                                                                                                                                             |
| PAN_DUR                   | 0.8–1.5 s plain; 0.5–0.8 s whip                                  |                                                                                                                                                                                           |
| Ease law                  | `power4.out` dives/landings; `power2.inOut` repositioning/cruise | spring/back on a camera reads as the world wobbling on a string; four identical pushes read as a slideshow — vary the leg verbs                                                           |
| Holds                     | ≥ 0.8 s between legs; final dwell ≥ 1 s                          | unless ending held mid-dive                                                                                                                                                               |
| BLUR_PER_DEPTH / MAX_BLUR | per [depth-of-field-blur.md](depth-of-field-blur.md)             | 3–6 px per step, terminal 8–24 px, leaf elements only; travel-blur peak per [motion-blur-streak.md](motion-blur-streak.md) (~18–20 px full-frame, on `.stage`)                            |

## Critical Constraints

- **One lens, one state, one writer** — `perspective` on the static `.stage` only (never on `.world`, never tweened, never a second perspective wrapper inside); every leg tweens the single `cam` object; only `applyCamera()` writes the transform — drift folds into the same writer via additive state. Two writers (or a second transform sneaking in via CSS) is the classic broken-camera bug, five channels of it here.
- **Fixed transform order: translate outside the rotations** — `translate3d(x,y,z) rotateX() rotateY()`. Reorder it and every pose you authored silently means something else.
- **Keep the world CLEAN** — `filter`, `opacity < 1`, `overflow` other than `visible`, `clip-path`, or `mask` on `.world` (or any intermediate wrapper) forces used `transform-style: flat` and collapses every `translateZ` in the scene. Travel blur goes on `.stage`; DoF on leaf cards; fades on children; background on `.scene`. `transform-style: preserve-3d` on `.world` and every intermediate wrapper between it and 3D-positioned children.
- **Camera intent inverts onto the world** — fly in = world z up, pan right = world x negative, tilt down = world rx positive. Same sign law as `viewport-change`, two more axes to get right.
- **Poses authored and baked** — never measured per-frame, never hand-derived projections.
- **First leg is a `fromTo`** AND `applyCamera()` runs once at setup — a seek to t=0 must render the exact establishing pose.
- **Z budget** — only sacrificial props may cross the camera plane.
- **Reads happen at landings** — angled, blurred, flying text is texture; anything the viewer must read gets a near-flat pose or a sharp held close-up ≥ 1 s (the tilt-to-flatten leg exists to hand the surface over for reading).
- **`overflow: hidden` on `.scene` + `data-layout-allow-overflow` on `.world`** — travel legs deliberately push panels past the frame; without the pairing, `check` reports `container_overflow` for every region the flight leaves behind.

## See also

[viewport-change.md](viewport-change.md) (2D counterpart, same single-writer law — right when the shot never tilts) · [multi-phase-camera.md](multi-phase-camera.md) (leg-sequencing grammar + hold micro-drift) · [coordinate-target-zoom.md](coordinate-target-zoom.md) (aim math for a flat-hold zoom while `rx`/`ry` are 0) · [depth-of-field-blur.md](depth-of-field-blur.md) (non-focal defocus / racks) · [motion-blur-streak.md](motion-blur-streak.md) (travel blur on the stage) · [nudge-curve.md](nudge-curve.md) (whip-sweep burst tuning) · [3d-page-scroll.md](3d-page-scroll.md) (static-tilt cousin — camera should NOT travel) · [orbit-3d-entry.md](orbit-3d-entry.md) / [depth-scatter-assemble.md](depth-scatter-assemble.md) (elements moving under a still camera — the inverse; don't run both on one beat). Capability background: `../techniques.md` § CSS 3D Transforms.


<!-- ===== FILE: hyperframes/hyperframes-animation/rules/3d-page-scroll.md ===== -->

---
name: 3d-page-scroll
description: Full webpage rendered as tilted 3D card that scrolls to reveal specific sections.
metadata:
  tags: 3d, page, scroll, webpage, tilt, product-demo, perspective
---

# 3D Page Scroll

A webpage (or long content) presented as a tilted 3D card. Spring-eased scroll reveals specific sections while the static 3D perspective adds physical depth. (For a camera that actually travels/tilts, see [3d-camera-flight.md](3d-camera-flight.md) — this rule's tilt never moves.)

## How It Works

Two independent transforms combine:

1. **3D tilt** — static `rotateY` + `rotateX` with `perspective` on the card. The angle does **not** change during the scene.
2. **Scroll** — the content inside the card translates vertically (`y` in GSAP) within a clipped container; spring-like deceleration via `power3.out` / `power4.out`.

Optional: **spotlight overlay** — a radial-gradient mask dims everything except a focal region after the scroll lands. It sits above the scrolling content, fixed relative to the card, never inside `.page-content`.

## Recipe

```html
<div class="tilt-card">
  <div class="page-content">
    <!-- Full {Brand} webpage recreation, taller than the card so scrolling
         matters. Each section is REAL DOM, not a screenshot — screenshots
         can't be individually highlighted or scrolled-to with precision. -->
    <section class="page-hero">{heroContents}</section>
    <section class="page-features">{featuresContents}</section>
    <section class="page-target" id="target-section">{targetContents}</section>
    <section class="page-cta">{ctaContents}</section>
  </div>
  <div class="spotlight"></div>
</div>
```

```css
.tilt-card {
  position: absolute;
  left: 50%;
  top: 50%;
  /* tilt + perspective in CSS only if no other transform tween touches this
     element — if GSAP also tweens scale on .tilt-card, set the tilt via
     gsap.set() instead to avoid matrix overwrites */
  transform: translate(-50%, -50%) perspective({perspectivePx}) rotateY({tiltYDeg}) rotateX({tiltXDeg});
  transform-style: preserve-3d;
  width: {cardWidth};
  height: {cardHeight};
  border-radius: 24px;
  background: {cardBackgroundColor};
  overflow: hidden; /* clip the scrolling content at the rounded corners */
  /* shadow X-offset sign must match tiltY sign (negative tiltY ⇒ positive X) */
  box-shadow: 40px 30px 80px rgba(0, 0, 0, 0.45);
}
.page-content {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  /* height intrinsic from sections — taller than the card */
}
.spotlight {
  position: absolute;
  inset: 0;
  pointer-events: none;
  opacity: 0;
  background: radial-gradient(ellipse 60% 35% at 50% 50%, transparent 50%, {spotlightDimColor} 100%);
}
```

```js
// SCROLL_DISTANCE is measured at design time from the real page layout
// (top of .page-content origin to vertical center of #target-section,
// accounting for card height) — NOT a free tunable.
tl.to(
  ".page-content",
  { y: -SCROLL_DISTANCE, duration: SCROLL_DUR, ease: "power3.out" },
  SCROLL_AT,
);

// Spotlight fades in on the target after the scroll settles.
tl.to(
  ".spotlight",
  { opacity: 1, duration: SPOTLIGHT_FADE_DUR, ease: "power1.inOut" },
  SPOTLIGHT_AT,
);
```

## Variations

**Multi-step scroll (scroll → pause → scroll)** — multiple `y:` tweens at different positions. Distances are both measured from the `.page-content` origin (NOT delta from the previous step); GSAP composes successive `y:` tweens on the same property, each starting from the value the previous one left:

```js
tl.to(
  ".page-content",
  { y: -SCROLL_DISTANCE_A, duration: SCROLL_DUR, ease: "power3.out" },
  SCROLL_AT_A,
);
tl.to(
  ".page-content",
  { y: -SCROLL_DISTANCE_B, duration: SCROLL_DUR, ease: "power3.out" },
  SCROLL_AT_B,
);
// SCROLL_AT_A + SCROLL_DUR ≤ SCROLL_AT_B — the two scrolls must not fight for y
```

## Values

| token              | range / rule                                                              | notes                                                                                 |
| ------------------ | ------------------------------------------------------------------------- | ------------------------------------------------------------------------------------- |
| tiltYDeg           | −12 to −4 (left-leaning) or 4 to 12                                       | bigger = more dramatic 3D; near 0 collapses to a flat panel                           |
| tiltXDeg           | 0–6                                                                       | positive tilts the top edge away                                                      |
| perspectivePx      | 800–2000 px                                                               | smaller = more foreshortening; larger = nearly orthographic                           |
| cardWidth / Height | card height < total content height                                        | otherwise the scroll has nothing to reveal                                            |
| sectionHeight      | Σ heights ≥ cardHeight + SCROLL_DISTANCE                                  | so the target section lands within frame                                              |
| SCROLL_AT          | ≥ end of prior tweens on `.page-content`                                  |                                                                                       |
| SCROLL_DUR         | 0.8–1.8 s                                                                 | shorter feels like a hard cut; longer feels programmatic                              |
| SCROLL_DISTANCE    | measured from the layout                                                  | from actual cumulative section heights — never estimated; don't overshoot content end |
| SPOTLIGHT_AT       | ≥ SCROLL_AT + SCROLL_DUR (or slightly earlier)                            | spotlight reveals the freshly-arrived section                                         |
| SPOTLIGHT_FADE_DUR | 0.4–0.8 s                                                                 |                                                                                       |
| Ease               | `power3.out` default; `power4.out` momentum; `power2.inOut` cinematic pan | pick ONE for all scrolls in the scene — mixing easings reads as jerky                 |

## Critical Constraints

- **Tilt is static** — the card holds its angle the whole scene.
- **Shadow direction matches tilt** — a left-leaning card casts shadow to the right (positive X offset); mismatch breaks the 3D illusion.
- **Page content is real HTML, not a screenshot**; scroll distances come from the real layout geometry.
- **`overflow: hidden` + `transform-style: preserve-3d` on `.tilt-card`** — clip at the rounded corners; preserve-3d for any 3D children / clean perspective composition.
- **Spotlight is an overlay above the scrolling content**, never inside `.page-content`.
- **Same easing across a multi-phase scroll**, and non-overlapping scroll windows.

## See also

[asr-keyword-glow.md](asr-keyword-glow.md) (on-page keyword highlight synced to VO) · [multi-phase-camera.md](multi-phase-camera.md) (camera zoom while the page scrolls) · [cursor-click-ripple.md](cursor-click-ripple.md) (cursor lands in the scrolled-into-view section) · [3d-camera-flight.md](3d-camera-flight.md) (when the camera itself should travel).


<!-- ===== FILE: hyperframes/hyperframes-animation/rules/3d-text-depth-layers.md ===== -->

---
name: 3d-text-depth-layers
description: Multiple offset text layers create a stacked 3D shadow / extrusion effect on large typography — more impactful than CSS text-shadow because each layer is a full DOM element.
metadata:
  tags: text, 3d, depth, layers, shadow, typography, stacked, extrusion
---

# 3D Text Depth Layers

The same text rendered N times at increasing offsets — back layers translucent, front layer full opacity and brand color — creates a physical "stacked extrusion" depth illusion on large typography. Distinct from `text-shadow` (which can't have per-layer hue / opacity / animation): each layer is a real DOM element.

## How It Works

A build script appends `LAYER_COUNT` copies back-to-front; each back layer sits at `translate(i × OFFSET_X, i × OFFSET_Y)` with alpha stepping down per layer, while the front copy (`i = 0`) is `position: relative` so it defines the container size (back layers stack absolutely behind it). The default entrance cascades the layers' fades back-to-front while a proxy tween grows the offsets from 0 → full, so the depth "builds forward" and lands as the last layer fades in.

## Recipe

```html
<!-- inside a standard scene clip (hyperframes-core) -->
<div class="depth-stack">
  <!-- layers injected by script — LAYER_COUNT copies of {label} -->
</div>
```

```css
.depth-stack {
  position: relative; /* front layer defines size; back layers stack behind */
}
.depth-text {
  font-weight: 900; /* black weight — thin text loses the illusion */
  font-size: HERO_FONT_SIZE;
  letter-spacing: HERO_LETTER_SPACING;
  line-height: 1;
  color: {frontColor};
}
.depth-text.is-back {
  position: absolute;
  top: 0;
  left: 0;
  pointer-events: none; /* decorative */
}
.depth-text.is-front {
  position: relative;
  z-index: 10;
}
```

```js
const stack = document.querySelector(".depth-stack");

// Build back-to-front so the FRONT (i=0) is appended LAST
for (let i = LAYER_COUNT - 1; i >= 0; i--) {
  const el = document.createElement("div");
  el.className = "depth-text " + (i === 0 ? "is-front" : "is-back");
  el.textContent = "{label}";
  if (i > 0) {
    const alpha = Math.max(BACK_ALPHA_MAX - i * BACK_ALPHA_STEP, BACK_ALPHA_MIN);
    el.style.color = `rgba({backHueRGB}, ${alpha})`; // rgba in color, NOT element opacity
    el.style.transform = `translate(${i * OFFSET_X}px, ${i * OFFSET_Y}px)`;
  }
  el.dataset.layer = String(i);
  stack.appendChild(el);
}

// Cascade entry — back layers fade in first, building forward
stack.querySelectorAll(".depth-text").forEach((el) => {
  const i = Number(el.dataset.layer);
  const finalAlpha = i === 0 ? 1 : Math.max(BACK_ALPHA_MAX - i * BACK_ALPHA_STEP, BACK_ALPHA_MIN);
  tl.fromTo(
    el,
    { opacity: 0 },
    { opacity: finalAlpha, duration: LAYER_FADE_DUR, ease: "power2.out" },
    LAYER_CASCADE_START + (LAYER_COUNT - 1 - i) * LAYER_CASCADE_STEP,
  );
});

// Depth grows on entry — offsets interpolate 0 → full
const depthState = { p: 0 };
tl.to(
  depthState,
  {
    p: 1,
    duration: DEPTH_GROW_DUR,
    ease: "power2.out",
    onUpdate: () => {
      stack.querySelectorAll(".depth-text.is-back").forEach((el) => {
        const i = Number(el.dataset.layer);
        el.style.transform = `translate(${i * OFFSET_X * depthState.p}px, ${i * OFFSET_Y * depthState.p}px)`;
      });
    },
  },
  LAYER_CASCADE_START, // align with the cascade so depth lands as the last layer fades in
);
```

## Variations

- **Static depth** (single hero shot) — render all layers at final positions from t=0; optionally fade the whole stack in with a subtle scale (0.94–0.98 → 1, 0.5–0.8s).
- **Dynamic depth pulse** — after the grow completes, modulate the offsets with a sine multiplier `1 + sin(p) × BEAT_AMP` (BEAT_AMP 0.2–0.6; one beat per 0.7–1.5s reads as a heartbeat).
- **Color-shift back layers** — instead of fading to translucent, step hue/lightness per layer: `hsla(HUE_BASE − i × HUE_STEP, SAT_PCT%, LIGHT_BASE − i × LIGHT_STEP%, 1)` (HUE_STEP 4–12°; larger reads as glitch). Depth reads as a colored cast shadow.

## Values

| token               | range                    | notes                                                                  |
| ------------------- | ------------------------ | ---------------------------------------------------------------------- |
| LAYER_COUNT         | 4–6                      | <4 doesn't read as 3D; >6 clutters on tight kerning                    |
| OFFSET_X / OFFSET_Y | 1–3px each               | >4px reads as glitch / chromatic aberration, not depth                 |
| BACK_ALPHA_MAX      | 0.6–0.85                 | nearest back layer; >0.9 fights the front for dominance                |
| BACK_ALPHA_STEP     | 0.08–0.15                | small = soft gradient; large = discrete plates                         |
| BACK_ALPHA_MIN      | 0.1–0.2                  | floor — below 0.1 the deepest layer vanishes on dark backgrounds       |
| HERO_FONT_SIZE      | 60px min; 200–340px hero | thin/small text loses the layered illusion                             |
| HERO_LETTER_SPACING | −0.03em–0                | tighter makes offsets read as depth, not repetition                    |
| LAYER_CASCADE_STEP  | 0.04–0.10s               | smaller ≈ simultaneous; larger feels stepped                           |
| LAYER_FADE_DUR      | 0.3–0.6s                 | per-layer fade                                                         |
| DEPTH_GROW_DUR      | 0.4–0.8s                 | ≈ `LAYER_FADE_DUR × LAYER_COUNT / 2` so depth lands with the last fade |

## Critical Constraints

- **Offset direction implies light direction** — `(+x, +y)` = light upper-left, `(-x, +y)` = upper-right; one sign convention for the whole composition.
- **Back layers translucent OR darker — never more saturated than the front** (reads as a halo, not depth).
- **Set back-layer color via `rgba()` in `color`, not element `opacity`** — opacity fades the whole rendered glyph including any shadow.
- **Front layer `position: relative` defines container size**; back layers absolute with `pointer-events: none`; offsets via `transform: translate()`, never `top`/`left`.
- **No CSS `text-shadow` alongside layered depth** — they compound and over-extrude.
- **No per-letter animation on top of the stack** — hacker-flip / typewriter over 6-layer depth is chaos; drop to 2–3 layers or apply depth only to the static post-reveal state.

## See also

`counting-dynamic-scale` (counter rendered with depth layers) · `sine-wave-loop` (idle breathing on the front layer post-reveal) · `center-outward-expansion` (depth-stacked wordmark after the burst lands).


<!-- ===== FILE: hyperframes/hyperframes-animation/rules/ai-tracking-box.md ===== -->

---
name: ai-tracking-box
description: Animated bounding box with L-shaped corner markers following an oscillating path — simulates AI object detection / tracking.
metadata:
  tags: ai, tracking, bounding-box, detection, corner, yellow, ml
---

# AI Tracking Box

A bounding box of four L-bracket corners + a confidence label that follows a moving target, simulating real-time AI detection. Rendered in detection yellow (`#facc15` family) on a dark background — the industry convention (AV HUDs, security CV, ML demos); red reads "warning", green "success", blue "info" — none read "detection."

## How It Works

ONE `ease: "none"` driver tween advances a phase `p`; its `onUpdate` computes the TARGET's position from trig, then derives the box's position/size FROM the target — every frame, in that order. The box never gets its own position tween: if it trails the target it reads as a broken tracker, not a smart AI. Size jitters a few percent off-tempo (non-integer frequency multiple) to mimic continuous re-fitting, and the confidence label flickers inside [95, 99].

## Recipe

```html
<!-- inside a standard scene clip (hyperframes-core) -->
<div class="bg-mascot" id="mascot">{targetGlyph}</div>
<div class="track-box" id="track-box">
  <div class="corner tl"></div>
  <div class="corner tr"></div>
  <div class="corner bl"></div>
  <div class="corner br"></div>
  <div class="label" id="label">{LABEL} · {confidence}%</div>
</div>
```

```css
.track-box {
  position: absolute; /* position + size written by the driver's onUpdate */
  pointer-events: none;
  will-change: transform, width, height;
}
.corner {
  position: absolute;
  width: 48px;
  height: 48px;
}
/* Each corner draws only its two outer borders — .tr/.bl/.br mirror this: */
.corner.tl {
  top: -8px;
  left: -8px;
  border-top: 6px solid {detectionYellow};
  border-left: 6px solid {detectionYellow};
}
.label {
  position: absolute;
  top: -56px;
  left: -8px;
  background: {detectionYellow};
  color: {labelTextColor}; /* near-black on yellow */
  font-family: {monoFont}; /* mono = machine readout */
  white-space: nowrap;
}
```

```js
const box = document.getElementById("track-box");
const mascot = document.getElementById("mascot");
const label = document.getElementById("label");
const C = { x: COMP_WIDTH / 2, y: COMP_HEIGHT / 2 };

// Entry — the AI "locks on"
gsap.set(box, { opacity: 0, scale: ENTRY_SCALE });
tl.to(
  box,
  { opacity: 1, scale: 1, duration: ENTRY_DUR, ease: `back.out(${ENTRY_BOUNCE})` },
  ENTRY_START,
);

// Tracking — target first, box derived from it, every frame
const tracking = { p: 0 };
tl.to(
  tracking,
  {
    p: Math.PI * 2 * CYCLES,
    duration: TRACK_DUR,
    ease: "none",
    onUpdate: () => {
      const mx = C.x + Math.cos(tracking.p) * DRIFT_X;
      const my = C.y + Math.sin(tracking.p) * DRIFT_Y;
      mascot.style.left = `${mx - MASCOT_SIZE / 2}px`;
      mascot.style.top = `${my - MASCOT_SIZE / 2}px`;

      const w = SIZE_BASE + Math.sin(tracking.p * SIZE_FREQ_MULT) * SIZE_VAR;
      const h = SIZE_BASE + Math.sin(tracking.p * SIZE_FREQ_MULT + Math.PI / 2) * SIZE_VAR;
      box.style.width = `${w}px`;
      box.style.height = `${h}px`;
      box.style.left = `${mx - w / 2}px`;
      box.style.top = `${my - h / 2}px`;

      const conf = Math.round(
        CONFIDENCE_MEAN + Math.sin(tracking.p * CONFIDENCE_FREQ_MULT) * CONFIDENCE_VAR,
      );
      label.textContent = `${LABEL_TEXT} · ${conf}%`;
    },
  },
  TRACK_START,
);
```

## Variations

- **Multi-object**: one driver per box/target pair, phases offset by `π / N` so they don't tick synchronously.
- **Lost-then-reacquired**: fade the box to ~0.2–0.4 opacity, then re-snap with a harder `back.out(1.8–2.5)` and flash a "REACQUIRED · 99%" label via `tl.set`.
- **Tracking-then-zoom**: hand off to [viewport-change.md](viewport-change.md) — "the AI found something, now show it."

## Values

| token                | range              | notes                                                                    |
| -------------------- | ------------------ | ------------------------------------------------------------------------ |
| ENTRY_SCALE          | 0.5–0.9            | < 1 — the box snaps UP into focus                                        |
| ENTRY_DUR / \_BOUNCE | 0.3–0.8s / 1.2–2.5 | `back.out` only — elastic reads cartoonish, power reads flat             |
| TRACK_START          | ≥ entry end        | a gap = pause for emphasis; none = seamless lock + follow                |
| TRACK_DUR            | 2–8s               | ≥ one full cycle or the drift never reads as oscillation                 |
| CYCLES               | 0.5–3              | keep effective rate < ~0.6 Hz or the motion blurs                        |
| DRIFT_X / DRIFT_Y    | 40–200px           | center ± drift must keep the target fully on screen                      |
| SIZE_BASE            | 200–500px          | must visibly enclose the target at all jitter sizes                      |
| SIZE_VAR             | 5–10% of SIZE_BASE | more reads broken, none reads like a screenshot; keep < 0.15×            |
| SIZE_FREQ_MULT       | 1.5–3, non-integer | integer ratios pulse in lock-step with drift = mechanical                |
| CONFIDENCE_MEAN/VAR  | 95–99 / 1–3        | mean ± var ⊂ [95, 99]; < 95 "uncertain", 100 "fake-precise"; 97 is sweet |
| CONFIDENCE_FREQ_MULT | 3–6                | > SIZE_FREQ_MULT — label flickers faster than the box breathes           |
| MASCOT_SIZE          | = rendered size    | mismatch drifts the target out of the box                                |

Tokens: `{detectionYellow}` `#facc15` family; `{bgInner}/{bgOuter}` dark low-chroma radial so the yellow pops; `{labelTextColor}` near-black; `{monoFont}` for the label.

## Critical Constraints

- **❗ Box recomputed per-frame FROM the target** — one driver computes the target position, then the box derives from it in the same `onUpdate`. Never tween the box's position separately.
- **Corner L-brackets, not a full border** — the genre signature; a full border reads as a generic UI box.
- **Yellow-on-dark** — substituting another hue loses genre legibility.
- **Confidence flickers in a tight band inside [95, 99]**, in a mono font.
- **`pointer-events: none`** on the box — it's a decorative overlay.

## See also

`viewport-change` (zoom into the detection) · `multi-phase-camera` (wide during tracking, push-in on lock) · `sine-wave-loop` (the target idle-breathes inside the box).


<!-- ===== FILE: hyperframes/hyperframes-animation/rules/ambient-glow-bloom.md ===== -->

---
name: ambient-glow-bloom
description: Un-triggered soft radial glow that blooms in behind a hero element and holds with a bounded idle breathe, or a single-pass traveling sweep across a surface. No click, no word-sync — it just blooms. Finite, deterministic, seek-safe.
metadata:
  tags: glow, bloom, ambient, radial, sweep, hero, presence, finite, un-triggered
---

# Ambient Glow Bloom

A soft radial glow that **blooms in behind a hero element** (card, logo, metric) and holds, giving it presence. Unlike `press-release-spring`'s click-triggered burst or `asr-keyword-glow`'s word-timed envelope, this glow is **un-triggered** — it blooms on the hero's settle and stays lit. Two forms: a **hero bloom** that swells behind a settling element then breathes, and a **traveling sweep** that translates a soft highlight across a surface exactly once.

## How It Works

A radial-gradient layer sits **behind** the hero (glow `z-index: 1`, hero `z-index: 2` — a glow in front occludes it), starting at `opacity: 0`. Over the bloom-in window it ramps `opacity: 0 → peak` with a gentle `scale` swell, timed so `BLOOM_START + BLOOM_DUR` lands on the hero's settle — glow and hero resolve as ONE beat ("powering on"), never glow-then-card. After bloom-in:

1. **Hero bloom** — a **bounded idle breathe** during the hold: a finite `ease: "none"` tween advances a `phase` proxy and `onUpdate` nudges opacity + scale a hair around peak (never a `yoyo` loop). `sin(0) = 0` → the breathe starts exactly at the bloom's resting state.
2. **Traveling sweep** — a narrow highlight band at one edge translates **once** across to the other (`x` off-surface to off-surface), clipped to the surface (`overflow: hidden`). One pass, no return — a repeating sweep reads as a loading shimmer, not a reveal accent (the shimmer-sweep variation below is the sanctioned exception).

Peak opacity stays restrained (**≤ 0.45 hard ceiling**) so the glow gives presence without washing the frame; the glow color is **darker + more saturated** than the element it backs (a same-hue, same-lightness glow disappears into the surface).

## Recipe

```html
<!-- inside a standard scene clip -->
<div class="bloom-stage">
  <div class="bloom-glow" id="bloom-glow"></div>
  <!-- z-index: 1; inset: GLOW_INSET (negative); background: {glowGradient} -->
  <div class="hero-card" id="hero-card">{HeroLabel}</div>
  <!-- z-index: 2 -->
</div>
<!-- sweep form: <div class="sweep" id="sweep"> inside the overflow:hidden surface -->
```

```js
// ── Form A: HERO BLOOM ── bloom in soft, landing on the hero's settle.
tl.fromTo(
  "#bloom-glow",
  { opacity: 0, scale: GLOW_START_SCALE },
  { opacity: GLOW_PEAK_OPACITY, scale: 1, duration: BLOOM_DUR, ease: "power2.out" },
  BLOOM_START,
);
// Bounded breathe during the hold — finite phase tween, NOT a yoyo loop.
const glow = document.getElementById("bloom-glow");
const phase = { p: 0 };
tl.to(
  phase,
  {
    p: Math.PI * 2 * BREATHE_CYCLES,
    duration: BREATHE_DUR,
    ease: "none",
    onUpdate: () => {
      const s = Math.sin(phase.p);
      glow.style.opacity = String(GLOW_PEAK_OPACITY + s * OPACITY_AMP);
      glow.style.transform = `scale(${1 + s * SCALE_AMP})`;
    },
  },
  BLOOM_START + BLOOM_DUR,
);

// ── Form B: TRAVELING SWEEP ── one finite pass, constant glide.
tl.fromTo(
  "#sweep",
  { x: SWEEP_START_X, opacity: 0 },
  { x: SWEEP_END_X, opacity: SWEEP_PEAK_OPACITY, duration: SWEEP_DUR, ease: "none" },
  SWEEP_START,
);
tl.to("#sweep", { opacity: 0, duration: SWEEP_FADE_DUR, ease: "power1.in" }, SWEEP_FADE_START);
```

## Variations

- **Bloom-and-hold** — for scenes <3s or a hero with its own idle, skip the breathe: the single `fromTo` is the whole recipe.
- **Pulse-on-arrival** — bloom slightly PAST peak (`GLOW_OVERSHOOT_OPACITY`, `scale: 1.06`), then a second adjacent tween eases down to a steady hold — one breath punctuating the landing, no ongoing loop.
- **Multi-hero relay** — stagger per-glow `BLOOM_START` by ~0.15–0.3s across a row; shrink `OPACITY_AMP` / `SCALE_AMP` per the `/√N` rule below.
- **Diagonal raked sweep** — angle `{sweepGradient}` (~105°) across a wordmark: the classic one-pass logo sheen. Narrower `SWEEP_WIDTH`, higher `SWEEP_PEAK_OPACITY`.

### Shimmer sweep (text-clipped status-phrase working-state)

The sweep re-aimed **inside type**: a soft highlight gradient clipped into a status phrase ("Thinking…", "Analyzing dataset…") via `background-clip: text` travels left→right through the letterforms — the grey-on-grey shimmer that says _still working_. Unlike every other form here it legitimately **repeats while the status is live**: the repetition is diegetic working-state, not idle wobble (same defense as a blinking caret — the motion performs status). Two things keep it honest: it is **bounded** (one finite tween whose pass count is computed from the status window, never `repeat: -1`), and it is **killed at resolve** — the moment the status completes, the shimmer stops dead; a shimmer surviving into the answer beat turns a working indicator into decoration.

```js
// Status shimmer — N passes as ONE bounded tween. Killed at resolve.
const status = document.getElementById("status-phrase");
// CSS on #status-phrase: background: {shimmerGradient}; background-size: 300% 100%;
// -webkit-background-clip: text; background-clip: text; color: transparent;
const shimmer = { p: 0 };
const PASSES = Math.round(STATUS_DUR / PASS_PERIOD); // whole passes, computed up front
tl.to(
  shimmer,
  {
    p: PASSES,
    duration: STATUS_DUR,
    ease: "none",
    onUpdate: () => {
      const t = shimmer.p % 1; // 0→1 within each pass; percent axis inverted → left→right travel
      status.style.backgroundPosition = `${(1 - t) * 100}% 50%`;
    },
  },
  STATUS_START,
);
tl.set(status, { backgroundPosition: "100% 50%" }, STATUS_START + STATUS_DUR); // resolve: dead.
```

Keep it a whisper: `{shimmerGradient}` is the status text's own grey with one slightly-lighter band (highlight stop a step above the base, nothing near white); `background-size` ~300% keeps the band narrow in the glyphs; `PASS_PERIOD` 1.2–1.8s — slower reads as a sheen accent, faster as a spinner. Whole-number `PASSES` lands the band at its start position exactly at the kill frame, so the `tl.set` is visually a no-op. This is the working-state cousin of `gradient-text-sweep`: reach **here** when the sweep _means_ "in progress," **there** when the gradient is the typographic treatment itself.

## Values

| token                   | range / default                                        | notes                                                                      |
| ----------------------- | ------------------------------------------------------ | -------------------------------------------------------------------------- |
| GLOW_PEAK_OPACITY       | 0.15 (subtle) → 0.30 (default) → **0.45 hard ceiling** | higher washes the frame; a glow you consciously notice is too strong       |
| GLOW_INSET              | −200 to −450px (1920×1080)                             | negative so the halo extends past the hero; too small reads as a tight rim |
| GLOW_START_SCALE        | 0.80–1.0                                               | ≤1.0 — grow into place, never shrink                                       |
| BLOOM_DUR / BLOOM_START | 0.6–1.4s                                               | `BLOOM_START + BLOOM_DUR` ≈ the hero's settle frame                        |
| OPACITY_AMP / SCALE_AMP | 0.02–0.05 / 0.01–0.03 default                          | `PEAK + OPACITY_AMP ≤ 0.45`; push only when the glow is the sole motion    |
| BREATHE_CYCLES          | period 2.5–4s per breath                               | glow breathes slower than element breathing                                |
| SWEEP_WIDTH             | 15–35% of surface (grid) / 8–15% (wordmark)            |                                                                            |
| SWEEP_DUR               | 0.8–1.6s                                               | one deliberate pass — slow enough to read as light                         |
| SWEEP_PEAK_OPACITY      | 0.10 → 0.25 (default) → 0.40                           | same ≤ ~0.45 wash limit; tight sweeps tolerate the high end                |
| SWEEP_START_X / END_X   | fully off-surface both ends                            | no visible spawn/despawn mid-surface; fade reaches 0 as the band clears    |
| PASS_PERIOD (shimmer)   | 1.2–1.8s                                               | with whole-number PASSES                                                   |

## Critical Constraints

- **Glow peak opacity ≤ 0.45** — including breathe amplitude; default to the LOW end (0.15–0.30).
- **Glow behind, hero in front**; glow color darker + more saturated than the hero surface.
- **Land glow and hero as one beat** — before or after reads as two separate events.
- **Breathe is bounded, sweep is one pass** — the only sanctioned repetition is the shimmer sweep, bounded and killed at resolve.
- **Concurrent halos compound** — per-glow amps ≤ default `/√N`, stagger breathe periods (2.6s / 2.9s / 3.3s) so they don't pulse in lockstep.
- **Don't combine a `boxShadow` glow on the hero with this halo layer** — they compete and read muddy; the glow lives on the dedicated layer.

## See also

`sine-wave-loop` (hero breathes on scale/y while the glow breathes on opacity, out of phase) · `press-release-spring` (the click-triggered sibling — never both behind one element) · `counting-dynamic-scale` / `stat-bars-and-fills` (bloom behind a landing stat) · `center-outward-expansion` (sweep across the assembled grid) · `gradient-text-sweep` (the design-beat gradient counterpart).


<!-- ===== FILE: hyperframes/hyperframes-animation/rules/anchored-layout-expand.md ===== -->

---
name: anchored-layout-expand
description: Edge-pinned container grows (or collapses) along ONE axis and in-flow content reflows with it — a pill springs open downward into a dropdown, a panel grows a sub-task stack, an input card stretches as typed text wraps, a pane expands over a neighbor. Transform-only (mask + slide, or proxy-driven scaleY + counter-scale) because width/height tweens are forbidden; the push on subsequent content is a matched translate on the same tween.
metadata:
  tags: expand, collapse, anchored, dropdown, menu, accordion, panel, reflow, push, mask, counter-scale, layout
---

# Anchored Layout Expand

> The law: **author the layout at its final (expanded) state in CSS, then fake the collapsed state with transforms.** The container never changes size — the _visible_ region does — and everything downstream rides a matched translate. The browser computes layout ONCE; every intermediate frame is pure transform.

THE one-axis growth primitive: a container pinned at one edge appears to grow along a single axis, and the in-flow content after it moves in perfect contact with the traveling edge — dropdown, sub-task stack, growing composer card, pane widening over a neighbor. Growth and push are ONE motion: if the panel's bottom edge and the pushed content ever separate or overlap, the illusion dies.

Distinct from [card-morph-anchor.md](card-morph-anchor.md) (a free-floating two-shot morph with no neighbors to push — this rule's container is a live layout participant), [spring-pop-entrance.md](spring-pop-entrance.md) (arrival at a point, no edge travel or reflow), and [reactive-displacement.md](reactive-displacement.md) (displacement by a colliding intruder; here content moves because the container's edge reached it — layout causality, not collision).

## How It Works

1. **Mask** — a wrapper at the final body height (`BODY_H`), `overflow: hidden`. Never tweened.
2. **Sheet** — the panel surface + content inside the mask, starting at `y: -BODY_H` (tucked above the mask window, behind the pinned header).
3. **Below** — ONE wrapper holding everything after the container, also starting at `y: -BODY_H`.
4. **Grow** — ONE `fromTo` drives sheet AND below from `y: -BODY_H → 0`. Shared tween ⇒ the descending bottom edge and the pushed content stay in exact contact by construction. Collapse = the same pair tweened back.

When the surface must visibly **stretch in place** (rows revealed top-first, or a pane growing sideways), use the proxy counter-scale variant below instead.

## Recipe

```html
<!-- inside a standard scene clip (hyperframes-core) -->
<div class="stack">
  <div class="expander">
    <div class="expander-head">{headerLabel}</div>
    <div class="expand-mask" id="expand-mask" data-layout-allow-overflow>
      <div class="expand-sheet" id="expand-sheet">
        <div class="expand-row">{rowA}</div>
        <div class="expand-row">{rowB}</div>
      </div>
    </div>
  </div>
  <!-- EVERYTHING that must be pushed lives in this one wrapper -->
  <div class="below" id="below">{followingContent}</div>
</div>
```

```css
/* Layout is the EXPANDED end state — no collapsed geometry exists in CSS. */
.expander-head {
  position: relative;
  z-index: 2; /* the sheet slides out from UNDER the header */
}
.expand-mask {
  height: BODY_H; /* authored final height — NEVER tweened */
  overflow: hidden;
}
.expand-sheet {
  height: BODY_H;
  border-radius: 0 0 SHEET_RADIUS SHEET_RADIUS; /* bottom-only — header + sheet read as one grown card */
  will-change: transform; /* + on .below */
}
```

```js
// BODY_H must equal the mask's CSS height exactly — measure once at build.
// (Montage caveat: per the contract, in a multi-scene master use an authored
// CSS-matched constant instead — later clips may not be laid out yet.)
const BODY_H = document.querySelector("#expand-mask").offsetHeight;

// The grow: ONE tween, BOTH sides of the seam.
tl.fromTo(
  ["#expand-sheet", "#below"],
  { y: -BODY_H },
  { y: 0, duration: GROW_DUR, ease: GROW_EASE },
  GROW_AT,
);

// Garnish: rows already ride the sheet; the fade stagger makes them read as "options arriving".
tl.fromTo(
  ".expand-row",
  { opacity: 0 },
  { opacity: 1, duration: ROW_FADE_DUR, stagger: ROW_STAGGER, ease: "power2.out" },
  GROW_AT + GROW_DUR * 0.25,
);

// Collapse — same machinery back; faster (closing is a snap decision).
tl.fromTo(
  ["#expand-sheet", "#below"],
  { y: 0 },
  { y: -BODY_H, duration: COLLAPSE_DUR, ease: "power3.in", immediateRender: false },
  COLLAPSE_AT,
);
```

## Variations

- **Proxy counter-scale — surface stretches in place** (rows revealed top-first holding their screen positions; the "payload card expands from the tool-call line"). Drive mask `scaleY` and the sheet's exact inverse from ONE proxy — two independent tweens are wrong: eased midpoints of `s` and `1/s` are not inverses and the content squashes mid-grow. Net content scale is `s × 1/s = 1` every frame; seek-safe because everything derives from the one interpolated proxy.

  ```js
  const grow = { h: COLLAPSED_H }; // 0 for fully collapsed
  tl.fromTo(
    grow,
    { h: COLLAPSED_H },
    {
      h: BODY_H,
      duration: GROW_DUR,
      ease: GROW_EASE,
      onUpdate: () => {
        const s = Math.max(grow.h / BODY_H, 0.0001); // clamp: no divide-by-zero
        gsap.set("#expand-mask", { scaleY: s, transformOrigin: "50% 0%" });
        gsap.set("#expand-sheet", { scaleY: 1 / s, transformOrigin: "50% 0%" });
        gsap.set("#below", { y: grow.h - BODY_H });
      },
    },
    GROW_AT,
  );
  ```

- **One-axis pane expand (X)**: same machinery rotated 90° — pin the left edge, sheet from `x: -PANE_W` (or proxy `scaleX` + counter-scale, origin `0% 50%`). Decide the neighbor's fate explicitly: **overlap** (pane paints over it, no neighbor tween) or **push** (neighbor rides the same tween). Never both.
- **Typed-wrap growth** — the composer card gets taller as typed text wraps. Quantize: one short step per wrap boundary, each moving the pair by one `LINE_H`; wrap times come from the deterministic typing schedule ([discrete-text-sequence.md](discrete-text-sequence.md)), never measured at render time. Two battle-tested traps:
  - **Composer cards have no pinned header** — a composer grows from its TOP edge (the send-button footer stays put), so a plain y-step clips the card's top out of the mask. Combine the proxy counter-scale with the wrap quantization (step the proxy by `LINE_H` at each wrap time) and split the surface into a **sheet** (carries the top radius) + **footer** (carries the bottom radius) so the growth seam stays invisible.
  - **Wrap TIME vs wrap POSITION are two different authorities** — the typing schedule decides _when_ a wrap fires, the browser's line-breaking decides _where_ text actually wraps, and with proportional fonts they silently disagree. Author an explicit `\n` in the typed string (with `white-space: pre-wrap`) at the chosen split point so both derive from the same authored fact.
- **Springy open** (rare, explicitly-playful): `back.out(1.2)` — the edge overshoots a few px; the pushed content bounces with the panel (correct — they're in contact). Default stays `power3.out`.
- **Row grows a sub-task stack**: the row is the pinned header, the stack is the sheet, every later row lives in `#below`; chain several scopes for progressive disclosure.
- **FLIP hand-off**: if the container also TRAVELS to a new layout slot while resizing (prompt promoted to heading, card docking into a sidebar), that's a FLIP problem — `/hyperframes-keyframes` (FLIP recipes). This rule stays the in-place one-axis specialist.

## Values

| token                    | range                       | notes                                                                 |
| ------------------------ | --------------------------- | --------------------------------------------------------------------- |
| BODY_H                   | measured / authored         | drift from the CSS height = visible gap or overlap at full open       |
| GROW_AT                  | trigger beat + 0–0.1s       | growth needs a cause (click / wrap / status beat) or it reads haunted |
| GROW_DUR                 | 0.35–0.6s                   | below ~0.3s the pushed content appears to teleport                    |
| GROW_EASE                | `power3.out` default        | `back.out(1.1–1.3)` only for the playful register                     |
| ROW_STAGGER / \_FADE_DUR | 0.04–0.08s / 0.2–0.3s       | start rows ~25% into the grow so none flash inside a closed panel     |
| COLLAPSE_DUR             | 0.2–0.35s, `power3.in`      | faster than open                                                      |
| STEP_DUR / LINE_H        | 0.12–0.2s / CSS line-height | typed-wrap variant; WRAP_TIMES from the typing script                 |

## Critical Constraints

- **NEVER tween `width` / `height` / `top` / `left` / `margin` / `padding`** — the mask's height is a CSS constant; only its children transform. Tweening the mask IS the forbidden move this rule replaces.
- **`data-layout-allow-overflow` on the mask** — the collapsed phase parks the sheet outside the mask's box by construction, which trips the `hyperframes check` layout gate (`container_overflow`). The flag is the sanctioned waiver: this overflow is the technique working as designed, not a bug.
- **Sheet + below share one tween (or one proxy)** — matched-but-separate tweens on the two sides of the contact edge are the classic seam bug.
- **Everything downstream rides `#below`** — content outside the wrapper is overlapped at t=0 and orphaned during the grow.
- **`overflow: hidden` on the mask** — without it the tucked sheet is visible above the header at t=0.
- **Counter-scale needs a proxy**, clamped `s ≥ 0.0001` (a fully-collapsed body divides by zero).
- **Deterministic sizes** — `BODY_H`, `LINE_H`, `WRAP_TIMES` are build-time constants or one-time measurements, never per-frame layout reads.

## See also

`cursor-click-ripple` (the igniting click) · `spring-pop-entrance` (richer per-row arrivals) · `discrete-text-sequence` (the typing that drives stepped growth) · `scale-swap-transition` (the grown menu's exit) · `/hyperframes-keyframes` FLIP (grow + travel).


<!-- ===== FILE: hyperframes/hyperframes-animation/rules/asr-keyword-glow.md ===== -->

---
name: asr-keyword-glow
description: Keywords glow + scale up when "spoken" — attack/sustain/release envelope synced to per-word timestamps. Even without real audio, hardcoded timings create a "narrator emphasis" effect.
metadata:
  tags: asr, audio-sync, highlight, glow, keyword, text, speech, emphasis
---

# ASR Keyword Glow

Words in a phrase visually activate (glow blur + scale) when "spoken", following an attack-sustain-release envelope over per-word `{ start, end }` timestamps. In a real ASR pipeline the timings come from a word-level transcript (`hyperframes transcribe` — same shape); for promo video, hand-author them to control emphasis pacing. The envelope never falls to zero after a word — it decays to a rest level, leaving a breadcrumb of recent emphasis.

## How It Works

A single linear driver tween (`ease: "none"` — any other ease distorts the per-word envelope; do not change) sweeps scene time; its `onUpdate` loops over ALL words computing each one's envelope: 0 before `start`, linear attack to 1 over `ATTACK_DUR`, sustain at 1 until `end`, decay to `REST_LEVEL` over `RELEASE`, then hold at rest. The envelope drives `text-shadow` blur and `scale` — one driver for the whole phrase, never one tween per word (60+ words would bloat the timeline).

## Recipe

```html
<!-- inside a standard scene clip (hyperframes-core) -->
<div class="phrase">
  <span class="word" data-word="{w1Key}">{w1}</span>
  <span class="word" data-word="{w2Key}">{w2}</span>
  <!-- … the final word may be the brand, with the .brand modifier -->
  <span class="word brand" data-word="{brandKey}">{brandWord}</span>
</div>
```

```css
.phrase {
  display: flex;
  flex-wrap: wrap;
  justify-content: center;
  color: {restColor};
}
.word {
  display: inline-block; /* required for transform on <span> */
  transform-origin: 50% 50%;
  text-shadow: 0 0 0 {glowColorTransparent};
}
.word.brand {
  color: {brandAccentColor};
}
```

```js
// Per-word spoken windows — one entry per span; brand word 1.5-2× a normal word's window.
const TIMINGS = {
  // {w1Key}: { start: …, end: … },  — seconds, local to the scene
};

function envelope(time, start, end) {
  if (time < start) return 0;
  if (time < end) return Math.min((time - start) / ATTACK_DUR, 1);
  const releaseEnd = end + RELEASE;
  if (time < releaseEnd) return 1 - ((time - end) / RELEASE) * (1 - REST_LEVEL);
  return REST_LEVEL;
}

const words = document.querySelectorAll(".word");
const driver = { t: 0 };
tl.to(
  driver,
  {
    t: SCENE_DURATION,
    duration: SCENE_DURATION,
    ease: "none", // linear — t maps 1:1 to scene time
    onUpdate: () => {
      words.forEach((el) => {
        const timing = TIMINGS[el.dataset.word];
        if (!timing) return;
        const env = envelope(driver.t, timing.start, timing.end);
        el.style.textShadow = `0 0 ${MAX_BLUR * env}px ${glowColorRgba(env)}`;
        el.style.transform = `scale(${1 + MAX_SCALE_BOOST * env})`;
      });
    },
  },
  0,
);
```

`glowColorRgba(env)` returns the glow color with `env`-modulated alpha.

## Variations

- **Karaoke style (RECOMMENDED for video narration)** — the default amplitudes read too subtle in video: inactive words still dominate. Render inactive words DIM and lerp the active word toward bright + larger; at any moment 1–2 words are bright (spoken + lingering rest) and the rest is dim. Use for short phrases (5–10 words) where one word at a time should POP; keep the subtle default for long dense text. Pushes MAX_BLUR, MAX_SCALE_BOOST, and REST↔ACTIVE contrast; everything else identical:

```js
function lerpChannel(a, b, t) {
  return Math.round(a + (b - a) * t);
}
function colorAt(env, isBrand) {
  const target = isBrand ? BRAND_RGB : ACTIVE_RGB;
  return `rgb(${lerpChannel(REST_RGB.r, target.r, env)}, ${lerpChannel(REST_RGB.g, target.g, env)}, ${lerpChannel(REST_RGB.b, target.b, env)})`;
}
// in onUpdate: el.style.color = colorAt(env, el.classList.contains("brand"));
```

- **Multi-octave glow** — multiply the sustain by `1 + sin(driver.t × PULSE_HZ) × PULSE_AMPLITUDE` so high-emphasis words breathe at peak.
- **Color shift on the peak** — same channel-lerp from `restColor` → `peakColor` as `env` rises (non-karaoke form).
- **3D pop-out** — add `translateZ(env × MAX_POP_Z)` so the spoken word leans toward camera; requires `perspective` on the parent.
- **From real ASR transcripts** — convert `{ word, start_ms, end_ms }` entries to seconds and feed in identically.

## Values

| token           | default style        | karaoke style | notes                                                      |
| --------------- | -------------------- | ------------- | ---------------------------------------------------------- |
| ATTACK_DUR      | 0.1–0.25s            | same          | must be < the shortest word's window or it never reaches 1 |
| RELEASE         | 0.2–0.5s             | same          | decay to rest                                              |
| REST_LEVEL      | 0.15–0.4             | 0.05–0.2      | > 0 (breadcrumb), < 1                                      |
| MAX_BLUR        | 15–25px              | 30–45px       | bigger = "shouting"                                        |
| MAX_SCALE_BOOST | 0.03–0.10            | 0.15–0.25     | additive at peak (0.08 ⇒ scale 1.08)                       |
| PULSE_HZ / AMP  | 4–10 rad/s / 0.1–0.3 | —             | multi-octave variation                                     |
| MAX_POP_Z       | 20–60px              | —             | 3D variation                                               |
| SCENE_DURATION  | = `data-duration`    | same          | driver must end in sync with the scene's seek window       |

## Critical Constraints

- **Timings monotonic, non-overlapping** — every entry's `end` < the next entry's `start`; overlapping windows make the envelope ambiguous.
- **Brand word window 1.5–2× a normal word** — the brand is the headline; let it sustain.
- **Driver ease stays `"none"`** — any other ease warps every word's envelope timing.
- **`text-shadow`, not `box-shadow`** — the glow must hug the GLYPH (speaking emphasis), not the inline-block rectangle.
- **One driver looping all words** — never one tween per word.
- **Commit to a style** — values between the default and karaoke columns yield awkward "half-loud" emphasis.
- **Climax dwell ≥1s** after the final word's emphasis — the last word IS the headline beat.

## See also

`3d-text-depth-layers` (depth on the active word at peak) · `sine-wave-loop` (idle breathe between emphasis moments) · `context-sensitive-cursor` (typewriter matching the ASR cadence) · `/media-use` for `hyperframes transcribe` and caption rendering.


<!-- ===== FILE: hyperframes/hyperframes-animation/rules/avatar-cloud-network.md ===== -->

---
name: avatar-cloud-network
description: Avatars distributed on an elliptical ring connected by SVG dashed lines to a center hub — social proof "community" reveal with staggered entry.
metadata:
  tags: avatar, cloud, network, social-proof, ellipse, connection, stagger
---

# Avatar Cloud Network

Avatars on an elliptical ring around a central hub (logo / counter), with SVG dashed lines drawing outward from the hub to each avatar — "community" / social proof. Distinct from [orbit-3d-entry.md](orbit-3d-entry.md) (continuous orbit): this settles into a static composed formation.

## How It Works

Three layers: SVG lines (z-index 1, behind), avatars (z-index 2), hub (z-index 5 — lines terminate AT its edge, never pass through). Avatar positions and lines are built once at setup from ONE shared center; the timeline then runs hub fade → avatar cascade → outward line draw → breathing dwell. Drawing FROM the center is the narrative: "the hub connects to its community."

## Recipe

```html
<!-- inside a standard scene clip (hyperframes-core) -->
<svg class="lines" viewBox="0 0 1920 1080"><!-- lines injected --></svg>
<div class="hub-wrap">
  <div class="hub">{counterValue} {counterLabel}</div>
  <!-- avatars injected -->
</div>
```

```css
.lines {
  position: absolute;
  inset: 0;
  z-index: 1;
  pointer-events: none;
}
.hub-wrap {
  position: absolute;
  inset: 0;
  display: grid;
  place-items: center;
}
.hub {
  position: relative;
  z-index: 5;
}
.avatar {
  position: absolute;
  z-index: 2;
  transform: translate(-50%, -50%); /* centers on the (left, top) the script sets */
  will-change: transform, opacity;
}
```

```js
// CENTER_X/Y must equal the hub's RENDERED center exactly — every avatar
// position and line endpoint derives from it. For a place-items:center hub on
// a 1920×1080 canvas: (W/2, H × CENTER_Y_FACTOR).
const C = { x: CENTER_X, y: CENTER_Y };
const wrap = document.querySelector(".hub-wrap");
const svg = document.querySelector(".lines");

for (let i = 0; i < AVATAR_COUNT; i++) {
  const a = (i / AVATAR_COUNT) * Math.PI * 2 - Math.PI / 2; // start at top
  const x = C.x + Math.cos(a) * RADIUS_X;
  const y = C.y + Math.sin(a) * RADIUS_Y;

  const av = document.createElement("div");
  av.className = "avatar"; // assign image / glyph from authoring data
  av.style.left = `${x}px`;
  av.style.top = `${y}px`;
  wrap.appendChild(av);

  const line = document.createElementNS("http://www.w3.org/2000/svg", "line");
  const attrs = {
    x1: C.x,
    y1: C.y,
    x2: x,
    y2: y,
    stroke: "{lineColor}",
    "stroke-dasharray": "6 8",
  };
  Object.entries(attrs).forEach(([k, v]) => line.setAttribute(k, String(v)));
  const len = Math.hypot(x - C.x, y - C.y); // straight line — Math.hypot, not getTotalLength()
  line.style.strokeDashoffset = String(len);
  svg.appendChild(line);
}

tl.from(".hub", { opacity: 0, scale: 0.8, duration: HUB_DUR, ease: `back.out(${HUB_BOUNCE})` }, 0);

const avatars = document.querySelectorAll(".avatar");
avatars.forEach((av, i) => {
  tl.from(
    av,
    { opacity: 0, scale: 0, duration: AVATAR_DUR, ease: `back.out(${AVATAR_BOUNCE})` },
    AVATAR_AT + i * AVATAR_STAGGER,
  );
});
svg.querySelectorAll("line").forEach((line, i) => {
  tl.to(
    line,
    { strokeDashoffset: 0, duration: LINE_DUR, ease: "power2.out" },
    LINES_AT + i * LINE_STAGGER,
  );
});

// Climax dwell — out-of-phase breathing holds the eye on the formed network:
// one phase proxy (0 → 2π·BREATH_CYCLES, ease "none"); onUpdate scales avatar i by
// 1 + sin(p + (i/n)·2π) · BREATH_AMP — sine-wave-loop's multiplicative onUpdate form.
// Keep the -50% centering in the same transform write.
```

## Variations

- **Size variety**: vary avatar sizes by a small index-keyed array so the ring doesn't read rigidly repetitive.
- **Solid lines**: drop the dash + draw; lines fade in via opacity — more corporate, less networky.
- **Multi-orbit**: inner ring (fewer, larger) connected to the hub; outer ring is an unconnected "halo."
- **Glyph avatars**: flags / emoji / icons instead of faces — reads "global community" or role spread.

## Values

| token          | range                        | notes                                                            |
| -------------- | ---------------------------- | ---------------------------------------------------------------- |
| AVATAR_COUNT   | 8–12                         | fewer feels sparse; more clutters the ellipse                    |
| RADIUS_X / \_Y | ~20–30% W / ~18–25% H        | ratio X/Y 1.5–3.0 reads as perspective; 1 (circle) reads flat    |
| avatar size    | 80–120px @1920               | ring must fit 10+ without overlap                                |
| HUB_DUR        | 0.4–0.6s                     | HUB_BOUNCE 1.4–1.8                                               |
| AVATAR_AT      | ≥ 0.6 × HUB_DUR              | hub established before satellites arrive                         |
| AVATAR_DUR     | 0.4–0.7s                     | AVATAR_BOUNCE 1.4–1.8, slightly firmer than hub                  |
| AVATAR_STAGGER | 0.06–0.10s                   | cascade reads "joining"; simultaneous reads "already there"      |
| LINES_AT       | overlaps last avatar settle  | start ~0.1–0.2s before it — draw reads as consequence of landing |
| LINE_DUR       | 0.4–0.7s                     | LINE_STAGGER 0.02–0.05s = a wave outward                         |
| BREATH_CYCLES  | 1.0–2.0 over the remaining s | under 1 = single sigh; over 2 = anxious. BREATH_AMP 0.02–0.06    |

Tokens: dark `{bgColor}` so the cloud reads as a constellation; translucent accent `{lineColor}`; soft border + glow keeps avatars legible on dark.

## Critical Constraints

- **CENTER_X/Y must match the hub's actual rendered center** — when composed with another scene (e.g. a recentered logo), bake them from the same source as the hub's final position, or lines visibly miss the hub.
- **Hub z-index above lines** — lines terminate at the hub edge, never cross it.
- **Lines draw outward** (dashoffset len → 0), starting after avatars are mostly settled.
- **`RADIUS_X > RADIUS_Y`** — a horizontal ellipse reads as perspective; a circle reads flat.
- **Climax dwell ≥ 1s** after lines complete so the formed network is readable.
- Straight lines: `Math.hypot` for length — `getTotalLength()` not needed.

## See also

`counting-dynamic-scale` (the hub IS a growing counter) · `sine-wave-loop` (the breathing form) · `orbit-3d-entry` (the continuously-orbiting cousin).


<!-- ===== FILE: hyperframes/hyperframes-animation/rules/camera-cursor-tracking.md ===== -->

---
name: camera-cursor-tracking
description: Two-phase virtual camera that locks viewport to a moving focal point with configurable initial positioning.
metadata:
  tags: camera, tracking, viewport, two-phase, spring
---

# Two-Phase Camera Cursor Tracking

Keeps a horizontally-growing element (a search bar with typing text, a long URL animating in) visible by switching between two camera modes.

## How It Works

Separate **World Space** (the full target element with all content) from **Screen Space** (the viewport). Two phases:

- **Phase 1 (Static)** — the world container sits at a fixed initial offset; the camera doesn't move. Anchors the viewer's eye before tracking begins.
- **Phase 2 (Tracking)** — activates when the focal point (cursor, highlight, last typed glyph) exceeds a target screen position (`CURSOR_TARGET_FRACTION × viewportWidth` from the left). The world translates leftward (`x: -delta`) keeping the focal point pinned at that screen position.

The offset math is **mathematically continuous** at the phase boundary — at the instant tracking starts, the world position equals what the static phase had, so the transition is seamless. The piecewise form:

```
finalWorldX = Math.min(INITIAL_OFFSET, trackingOffset)
```

`INITIAL_OFFSET` is the static-phase value; `trackingOffset` is whatever shift keeps the focal point at the target screen X. While the focal point hasn't grown past the target, `trackingOffset` is a less-negative number and `Math.min` returns the static value; once the focal point would cross the target, `trackingOffset` overtakes and tracking takes over. Do NOT replace this with a hard `if (typingProgress > threshold)` branch — the camera will visibly jump.

## Recipe

```html
<div class="viewport">
  <div class="world">
    <div class="search-bar">
      <span class="text" id="reveal-text">{phrase}</span><span class="cursor">|</span>
    </div>
  </div>
</div>
```

```css
.viewport {
  position: absolute;
  inset: 0;
  overflow: hidden; /* clip the world's left edge as it pans off-screen */
  display: flex;
  align-items: center;
  justify-content: flex-start;
  padding-left: VIEWPORT_PAD_LEFT; /* Phase-1 anchor X — must match the JS constant */
}
.world {
  display: flex;
  align-items: center;
  white-space: nowrap; /* text must stay on one line for the camera math */
}
.search-bar .text {
  display: inline-block;
  overflow: hidden;
  vertical-align: bottom;
}
.search-bar .cursor {
  display: inline-block; /* inline sibling of the text, NOT absolutely positioned —
     absolute positioning misaligns with the camera math */
  width: CURSOR_WIDTH;
  margin-left: CURSOR_GAP;
  background: {accentColor};
  height: CURSOR_HEIGHT_EM;
  vertical-align: bottom;
  /* no CSS blink animation — CSS clocks don't sync to seek; blink is a GSAP tween below */
}
```

```js
// Pre-measure the target text width to compute tracking distance.
// Measure SYNCHRONOUSLY — no fonts.ready gate (see Critical Constraints).
const textEl = document.getElementById("reveal-text");
const targetCursorScreenX = CURSOR_TARGET_FRACTION * VIEWPORT_WIDTH;
const fullWidth = textEl.scrollWidth; // total text width after full reveal
const trackingDelta = Math.max(0, VIEWPORT_PAD_LEFT + fullWidth - targetCursorScreenX);

// Phase 1 — text reveals progressively; camera holds. maxWidth tween
// (width/left/top tweens are forbidden); ease "none" = linear typing rate.
tl.fromTo(
  ".search-bar .text",
  { maxWidth: 0 },
  { maxWidth: fullWidth, duration: REVEAL_DUR, ease: "none" },
  REVEAL_START,
);

// Phase 2 — camera tracks. Start BEFORE full reveal so the handoff feels
// continuous (Math.min form above makes it mathematically continuous).
tl.to(".world", { x: -trackingDelta, duration: TRACK_DUR, ease: "power2.inOut" }, TRACK_START);

// Cursor blink — finite GSAP yoyo (never CSS @keyframes; CSS animation clocks
// aren't synced to HF's seek and flicker non-deterministically).
const blinkRepeats = Math.ceil(SCENE_DURATION / BLINK_HALF_PERIOD) - 1;
tl.to(
  ".search-bar .cursor",
  { opacity: 0, duration: BLINK_HALF_PERIOD, ease: "steps(1)", yoyo: true, repeat: blinkRepeats },
  0,
);
```

## Variations

- **Centered → center-tracked**: `.viewport { justify-content: center; padding: 0; }`, `CURSOR_TARGET_FRACTION = 0.5` — tracks once the focal point crosses the midline.
- **Left-aligned → right-tracked**: as written; best when content exceeds viewport width from the start.
- **Continuous typing driver**: replace the `maxWidth` tween with an `onUpdate` typing clock (`charsTyped = Math.floor(progress)`) plus per-frame `measureNodeWidth` driving the cursor screen X — required when the typed text is consumed elsewhere in the scene (e.g. by a parent strip's camera offset).

## Values

| token                  | range                       | notes                                                                           |
| ---------------------- | --------------------------- | ------------------------------------------------------------------------------- |
| VIEWPORT_PAD_LEFT      | 0 → ~10% of viewport width  | must match the CSS `padding-left` or the camera math drifts                     |
| VIEWPORT_WIDTH         | = the root's `data-width`   | never tweened                                                                   |
| CURSOR_TARGET_FRACTION | 0.5–0.75                    | lower = less revealed text in frame; higher delays tracking                     |
| CURSOR_WIDTH / GAP     | 4–10 px / a few px          | gap ≤ cursor width or it visually detaches                                      |
| CURSOR_HEIGHT_EM       | 0.85–1.0 em                 | matches the typed glyph height                                                  |
| REVEAL_DUR             | chars × 0.05–0.15s          | ease `"none"` — any easing distorts the per-keystroke cadence                   |
| TRACK_START            | < REVEAL_START + REVEAL_DUR | overlap the reveal so the handoff feels continuous                              |
| TRACK_DUR              | 0.8–2.0s                    | `power2.inOut`/`power3.inOut`; `back.out` reads as UI bounce, not camera        |
| BLINK_HALF_PERIOD      | 0.2–0.4s                    | `steps(1)` hard on/off; repeats derived from SCENE_DURATION (= `data-duration`) |

## Critical Constraints

- **Build the timeline SYNCHRONOUSLY — no `fonts.ready` gate.** HF renders frames in parallel workers, each a fresh browser. A `document.fonts.ready.then(...)` wrapper means some workers seek frames BEFORE the Promise resolves and find no timeline → those frames render at CSS initial state (`max-width: 0` ⇒ empty text) while others render correctly → visible flicker. Register the timeline at script-parse time: the camera math tolerates a few percent width error from fallback-font measurement; worker-race flicker is unacceptable. If precise post-font measurement matters, re-measure inside the tween's `onUpdate` (still deterministic per-frame), or set `font-display: block` on the @font-face.
- **Measure with `getBoundingClientRect()` / `scrollWidth` / probe nodes**, never character count × font-size — proportional fonts have variable glyph widths.
- **Continuous math at the phase boundary** — the `Math.min(INITIAL_OFFSET, trackingOffset)` form, never a hard threshold branch.
- **`white-space: nowrap` on the world** and pre-allocated width (tween `maxWidth` to the full target width) — prevents layout shift mid-tween.
- **Cursor is an inline sibling of the text**, and blinks via a finite GSAP yoyo — never CSS `@keyframes … infinite`.
- **`overflow: hidden` on `.viewport`** — clips the world as it pans.

## See also

[context-sensitive-cursor.md](context-sensitive-cursor.md) (cursor color per text segment) · [discrete-text-sequence.md](discrete-text-sequence.md) (non-linear text reveals under this camera).


<!-- ===== FILE: hyperframes/hyperframes-animation/rules/card-morph-anchor.md ===== -->

---
name: card-morph-anchor
description: Container morphs dimensions and border-radius between shots, serving as a visual transition anchor.
metadata:
  tags: morph, anchor, transition, border-radius, container, shape
---

# Card Morph Anchor

A free-floating container morphs apparent size, corner radius, and surface treatment between two shots — the morph itself IS the transition; the viewer's eye tracks the persistent container. Distinct from [anchored-layout-expand.md](anchored-layout-expand.md) (an edge-pinned live layout participant that grows along one axis and reflows neighbors — here nothing is pushed) and [theme-crossfade-morph.md](theme-crossfade-morph.md) (a whole-theme reskin under a fixed anchor — here a single container changes shape).

## How It Works

Since `width`/`height` tweens are forbidden, **substitute uniform `scale` for apparent size**; the remaining morph channels are **paint-only**: `borderRadius`, `background`, `boxShadow`. All channels ride ONE tween (one ease, one duration) so the shape morphs in lockstep. Content choreography: old content fades out during the first ~40% of the morph, new content fades in during the last ~40% — the shape-only gap between is the natural "blink." Optionally the morph card itself fades at the very end, revealing the real next-shot element rendered behind it.

## Recipe

```html
<!-- inside a standard scene clip (hyperframes-core) -->
<!-- DOM order = stacking: the anchor renders BEFORE the card, so the card is on top -->
<div class="next-shot-anchor"><img src="{nextShotAnchor}" alt="anchor" /></div>
<div class="morph-card">
  <div class="content-old">{shotOneContent}</div>
  <div class="content-new">{shotTwoContent}</div>
</div>
```

```css
.morph-card {
  width: SHOT_ONE_W;
  height: SHOT_ONE_H; /* shot-1 geometry; the morph is scale, never width/height */
  border-radius: SHOT_ONE_RADIUS;
  background: {surfaceShotOne};
  overflow: hidden; /* content must clip during the shape change */
  display: grid;
  place-items: center;
  will-change: transform;
}
.content-old,
.content-new {
  position: absolute;
  inset: 0;
  display: grid;
  place-items: center;
}
.content-new {
  opacity: 0; /* author its inner sizes at apparent-size ÷ END_SCALE — it scales with the card */
}
.next-shot-anchor {
  position: absolute;
  opacity: 0; /* fades in as the morph card fades out */
}
```

```js
const END_SCALE = SHOT_TWO_W / SHOT_ONE_W; // uniform — keep the two shots aspect-matched

// Hold shot 1 for HOLD_BEAT first — an instant morph reads as glitchy.

// One tween, all channels: uniform scale + paint-only properties.
tl.to(
  ".morph-card",
  {
    scale: END_SCALE,
    borderRadius: SHOT_TWO_RADIUS / END_SCALE, // borderRadius is pre-scale — divide to land the APPARENT radius
    background: "{surfaceShotTwo}",
    boxShadow: "{shadowShotTwo}",
    duration: MORPH_DUR,
    ease: "power2.inOut",
  },
  MORPH_START,
);

tl.to(
  ".content-old",
  { opacity: 0, duration: MORPH_DUR * OLD_FADE_FRAC, ease: "power1.in" },
  MORPH_START,
);
tl.to(
  ".content-new",
  { opacity: 1, duration: MORPH_DUR * NEW_FADE_FRAC, ease: "power1.out" },
  MORPH_START + MORPH_DUR * (1 - NEW_FADE_FRAC),
);

// Optional handoff — card fades out over the pixel-identical real anchor.
tl.to(
  ".morph-card",
  { opacity: 0, duration: MORPH_DUR * FINAL_FADE_FRAC, ease: "power1.in", immediateRender: false },
  MORPH_START + MORPH_DUR * (1 - FINAL_FADE_FRAC),
);
tl.to(
  ".next-shot-anchor",
  { opacity: 1, duration: MORPH_DUR * FINAL_FADE_FRAC, ease: "power1.out" },
  MORPH_START + MORPH_DUR * (1 - FINAL_FADE_FRAC),
);
```

## Morph channels

| channel        | how                                                                                            |
| -------------- | ---------------------------------------------------------------------------------------------- |
| apparent size  | uniform `scale` — the substitution for the forbidden `width`/`height` tween; aspect preserved  |
| `borderRadius` | paint-only; pre-scale units — tween to `APPARENT_RADIUS / END_SCALE`, ≤ half the smaller side  |
| `background`   | paint-only; gradients interpolate only with equal stop counts (solid→solid: `backgroundColor`) |
| `boxShadow`    | paint-only; base shadow → accent glow shifts emphasis                                          |

## Variations

- **Landing on a non-centered target** (dock icon, sidebar slot): add `x`/`y` to the same tween, computed as the FLIP-style delta between the card's and the target's rects — `getBoundingClientRect()` both at build time (single-scene only, per the contract) and tween the difference. Don't hand-compute from CSS values: paddings, borders, and parent transforms compound, and center-vs-edge arithmetic is the classic off-by-half bug.
- **Aspect change between shots**: uniform scale preserves aspect — morph to the nearest uniform fit and let the crossfade/handoff absorb the small delta, or drop the handoff and hold the card's final state.

## Values

| token             | range                     | notes                                                                                |
| ----------------- | ------------------------- | ------------------------------------------------------------------------------------ |
| HOLD_BEAT         | 0.6–1.5s                  | ≥ shot 1's entry settle; the viewer must register shot 1 first                       |
| MORPH_DUR         | 0.6–1.2s                  | < 0.5s can't fit both content fades                                                  |
| END_SCALE         | SHOT_TWO_W / SHOT_ONE_W   | icon-sized handoffs typically land at 80–400px apparent width                        |
| SHOT_TWO_RADIUS   | ≤ min(W, H)/2 apparent    | half the smaller side = perfect circle; beyond is clamped                            |
| OLD/NEW_FADE_FRAC | 0.3–0.5 each, sum ≤ 1     | the gap between is the shape-only "blink"                                            |
| FINAL_FADE_FRAC   | 0 (no handoff) or 0.1–0.2 | only when a pixel-identical anchor exists                                            |
| ease              | `power2.inOut` canonical  | `power3`/`expo.inOut` OK; never `back`/`elastic` — overshoot fights the shape change |

## Critical Constraints

- **❗ Uniform-scale substitution** — never tween `width`/`height`; `scale` + the paint-only channels (`borderRadius`, `background`, `boxShadow`) are the ONLY morph properties.
- **❗ Handoff anchor must be pixel-identical to the card's final state** — same apparent size, radius, background, shadow, inner icon dimensions. Any delta = a visible pop during the crossfade. Can't match exactly? Drop the handoff and hold the morph card.
- **❗ Stacking by DOM order, never a z-index snap mid-fade** — render the anchor before the card; a `tl.set({ zIndex })` during an active opacity tween flips stacking before the fade finishes and flickers.
- **`overflow: hidden`** on the card — content must clip as the radius changes.
- **Hold a beat before morphing**; same ease family for shape and crossfade (mixed eases read unsynchronized).

## See also

`anchored-layout-expand` (edge-pinned one-axis growth with reflow) · `theme-crossfade-morph` (whole-theme reskin under a fixed anchor) · `scale-swap-transition` (content swap without shape change) · `sine-wave-loop` (a breath on the final state).


<!-- ===== FILE: hyperframes/hyperframes-animation/rules/center-outward-expansion.md ===== -->

---
name: center-outward-expansion
description: Elements start clustered at screen center and expand outward to their final positions, driven by a shared progress value.
metadata:
  tags: expansion, scatter, center, reveal, layout, sync, burst
---

# Center-Outward Expansion

Elements begin at one shared center point and radiate outward to their final positions — the entry beat itself, or motion driven by another animation's progress (a counting number, a beat). Flat 2D cousin of [depth-scatter-assemble.md](depth-scatter-assemble.md) (per-element 3D cloud): here every element shares the SAME origin.

## How It Works

Each element carries its final offset as `data-target-x/y`. Its position lerps between center and target: `x = targetX × progress`. Self-centering is baked as `xPercent/yPercent: -50` so the tweened `x`/`y` are pure offsets from the stage center. Standalone burst = per-item staggered `fromTo`; driven burst = one shared proxy (see Variations).

## Recipe

```html
<!-- inside a standard scene clip (hyperframes-core) -->
<div class="burst-wrap">
  <div class="burst-item" data-target-x="-360" data-target-y="-180">{itemA}</div>
  <div class="burst-item" data-target-x="360" data-target-y="-180">{itemB}</div>
  <div class="burst-item" data-target-x="0" data-target-y="360">{itemC}</div>
</div>
```

```css
.burst-wrap {
  position: relative;
  width: 100%;
  height: 100%;
  display: grid;
  place-items: center;
}
.burst-item {
  position: absolute;
  top: 50%;
  left: 50%; /* GSAP xPercent/yPercent -50 bakes the centering; x/y tween the offset */
  will-change: transform;
}
```

```js
document.querySelectorAll(".burst-item").forEach((el, i) => {
  tl.fromTo(
    el,
    { xPercent: -50, yPercent: -50, x: 0, y: 0, scale: 0.6, opacity: 0 },
    {
      x: Number(el.dataset.targetX),
      y: Number(el.dataset.targetY),
      scale: 1,
      opacity: 1,
      duration: EXPAND_DUR,
      ease: EXPAND_EASE,
    },
    ENTRY_AT + i * STAGGER,
  );
});
```

## Variations

- **Synced to a driver (chord)**: when the burst shadows a counter / beat, drop the stagger and drive all items from ONE 0→1 proxy tween with the driver's exact duration AND ease; `onUpdate` writes `translate(-50%,-50%) translate(targetX*p, targetY*p)` per item — the two read as one beat.
- **Partially-spread start**: with 6+ items the full cluster piles up — start from `{ x: targetX * START_PROGRESS, ... }`.
- **Idle micro-float**: hand off to [sine-wave-loop.md](sine-wave-loop.md) after landing instead of freezing.

## Values

| token          | range                | notes                                                            |
| -------------- | -------------------- | ---------------------------------------------------------------- |
| ITEM_COUNT     | 3–8                  | > 8 = visual chaos mid-expansion; low counts want wider spread   |
| EXPAND_DUR     | 1.0–1.8s             | must equal the driver's duration in the synced variant           |
| EXPAND_EASE    | `power3.out` default | `power2.out` gentler, `expo.out` dramatic stop; NEVER `in` eases |
| STAGGER        | 0.04–0.08s           | tighter = chord; looser = lazy arpeggio                          |
| ENTRY_AT       | 0–0.5s               | a beat of compositional quiet before the burst                   |
| START_PROGRESS | 0–0.5                | 0 = dramatic full cluster; ~0.3 avoids the pile-up               |

## Critical Constraints

- **Tween `x`/`y` over the baked `xPercent/yPercent: -50`** — mutating `left`/`top` fights the centering and causes pixel jitter.
- **Out-easing only** — `in` easings read as items being sucked back mid-air.
- **No other absolute-positioned siblings inside `.burst-wrap`** — they'd steal the centered baseline.
- **❗ The burst IS the beat** — don't park a "real headline" label below it (the eye snaps to the label and ignores the burst). If a label is needed, reveal it post-burst in the same stack.
- Synced variant: identical duration + ease as the driver, or the chord falls apart.

## See also

`counting-dynamic-scale` (the classic chord driver) · `depth-scatter-assemble` (3D per-element cloud) · `card-morph-anchor` (burst out of a morphed card) · `sine-wave-loop` (post-landing life).


<!-- ===== FILE: hyperframes/hyperframes-animation/rules/chart-scrub-readout.md ===== -->

---
name: chart-scrub-readout
description: A cursor/playhead scrubs an already-drawn chart — one driver moves a vertical tracking line and marker along a baked data polyline while a date/value tooltip steps through the data array; a second series can activate on cross. Deterministic data, readout writes only on index change.
metadata:
  tags: chart, scrub, readout, tooltip, tracking-line, data, cursor, playhead
---

# Chart Scrub Readout

The chart is already ON screen — this rule **interrogates** it. A vertical tracking line rides the scrub position, a marker dot follows the series, and a live tooltip reads out `date: value` per position, values flickering past like an odometer. It's the "this data is real — look closer" beat: the scrub proves the chart is an instrument, not a picture.

Boundary with its neighbors: [stat-bars-and-fills.md](stat-bars-and-fills.md) owns the chart's ARRIVAL; [counting-dynamic-scale.md](counting-dynamic-scale.md) owns a single number swelling in place. This rule assumes the graphic already exists and adds a **read head** moving across it. The three chain naturally: the line draws in (svg-path-draw / stat-bars), this rule scrubs it, and the landing value hands off to a count-up lockup.

## How It Works

1. **Data baked at setup** — a literal `DATA` array of `{ d, v }` points (or a pure index formula). The polyline's `points` attribute is computed ONCE from `DATA` by pure mapping functions: chart and readout share one source of truth. The argument of the shot is "this data is real" — a random walk regenerated per render breaks both determinism and the rhetorical claim.
2. **One driver tween** `p: 0 → 1` derives everything in its `onUpdate`: tracking-line x, marker x/y, tooltip position. Every output is a pure function of `p` — any seek lands the identical frame. Parallel tweens that merely share timing drift apart under rounding and read as chart chrome, not a read head.
3. **The marker rides the polyline** — its y interpolates between the two neighboring baked points, from the same arrays that built the chart; a separately-keyframed marker inevitably floats off the line.
4. **The readout is threshold-stepped** — the nearest data index derives from `p`, and `textContent` is written ONLY when that index changes (last-index guard). Transforms glide per frame (compositor-cheap); text steps per data point — no per-frame DOM text thrash. The guard is an optimization, not state: any seek recomputes the same index and the same text.

## Recipe

```html
<!-- inside a standard scene clip. Size the SVG so viewBox units === CSS pixels:
     one coordinate space serves the polyline, tracking line, marker, AND the HTML tooltip. -->
<div class="chart-wrap">
  <!-- position: relative — the tooltip transforms against this box -->
  <svg class="chart" viewBox="0 0 CHART_W CHART_H" width="CHART_W" height="CHART_H">
    <polyline id="series-a" class="series" fill="none" />
    <line id="track-line" y1="0" y2="CHART_H" stroke-dasharray="6 6" />
    <circle id="marker" r="MARKER_R" />
  </svg>
  <div class="tooltip" id="tooltip">
    <span id="tip-date">{firstDate}</span>
    <span id="tip-value">{firstValue}</span>
  </div>
</div>
```

```css
.tooltip {
  position: absolute;
  top: 0;
  left: 0;
  min-width: TIP_MIN_WIDTH; /* fixed — the box must not resize as values change length */
}
#tip-value {
  font-variant-numeric: tabular-nums; /* MANDATORY — digits flicker past; widths must not */
}
```

```js
// Data baked at setup — literal values.
const DATA = [
  { d: "{date1}", v: V1 },
  // ... N points, chronological ...
];

// Pure mapping functions — geometry derives from DATA once.
const PAD = CHART_PAD;
const PLOT_W = CHART_W - PAD * 2;
const PLOT_H = CHART_H - PAD * 2;
const vals = DATA.map((p) => p.v);
const V_MIN = Math.min(...vals);
const V_MAX = Math.max(...vals);
const X = (i) => PAD + (i / (DATA.length - 1)) * PLOT_W;
const Y = (v) => PAD + PLOT_H * (1 - (v - V_MIN) / (V_MAX - V_MIN));

document
  .getElementById("series-a")
  .setAttribute("points", DATA.map((p, i) => `${X(i)},${Y(p.v)}`).join(" "));

const line = document.getElementById("track-line");
const marker = document.getElementById("marker");
const tooltip = document.getElementById("tooltip");
const tipDate = document.getElementById("tip-date");
const tipValue = document.getElementById("tip-value");

// Tooltip pops in as the scrub begins — a small fromTo scale/opacity spring at SCRUB_AT.

// ONE driver — line, marker, and tooltip are all projections of p.
const scrub = { p: 0 };
let lastIdx = -1;
tl.to(
  scrub,
  {
    p: 1,
    duration: SCRUB_DUR,
    ease: SCRUB_EASE,
    onUpdate: () => {
      const f = scrub.p * (DATA.length - 1); // fractional index
      const i = Math.min(DATA.length - 2, Math.floor(f));
      const t = f - i;
      const x = X(i) + (X(i + 1) - X(i)) * t;
      const y = Y(DATA[i].v) + (Y(DATA[i + 1].v) - Y(DATA[i].v)) * t;

      // Transforms glide every frame (cheap, deterministic)
      line.setAttribute("x1", x);
      line.setAttribute("x2", x);
      marker.setAttribute("cx", x);
      marker.setAttribute("cy", y);
      tooltip.style.transform = `translate(${x + TIP_DX}px, ${y - TIP_DY}px)`;

      // Text steps only when the nearest data point changes
      const idx = Math.round(f);
      if (idx !== lastIdx) {
        tipDate.textContent = DATA[idx].d;
        tipValue.textContent = `${DATA[idx].v.toLocaleString()} {unitLabel}`;
        lastIdx = idx;
      }
    },
  },
  SCRUB_AT,
);
// End hold: the driver finishes before the scene does — the landed value reads.
```

## Variations

- **Peak stop** — the scrub is the wind-up, the landing is the stat: `SCRUB_EASE: "power3.out"` decelerates onto the final/peak point, then pop the emphasis at landing (`fromTo` marker `scale: 1 → PEAK_POP_SCALE` at `SCRUB_AT + SCRUB_DUR`). Pair with a pill tooltip that springs to its final label ([spring-pop-entrance.md](spring-pop-entrance.md)) — the classic "line breaks above the band" climax.
- **Second-series activation on cross** — series B sits dimmed; at `SCRUB_AT + SCRUB_DUR * CROSS_P` tween its stroke to the lit color (0.25s, `power2.out`), and in the driver's `onUpdate` read from B's array once `scrub.p ≥ CROSS_P` (still index-guarded). The color flip lands ON the cross — same-frame causality.
- **Two-chart glide** — two scrub beats: sweep chart A, glide the cursor/tooltip group across the gutter (a plain `x` tween, no readout — dead travel, not data), then chart B activates with its own driver. One driver per chart.
- **Cursor-led scrub** — an oversized cursor is the visible actor: another projection of the SAME driver (positioned from `x` in the same `onUpdate`, tip at the tracking line's head) — never a second tween that merely matches timing. Cursor look and click grammar from [cursor-click-ripple.md](cursor-click-ripple.md).
- **Playhead form** — no cursor; the tracking line IS the actor (timeline scrubbers, audio waves, session replays). `ease: "none"` — mechanical playback, not a hand.

## Values

| token                   | range / default               | notes                                                                                                                    |
| ----------------------- | ----------------------------- | ------------------------------------------------------------------------------------------------------------------------ |
| N (data points)         | 10–40                         | <10 reads as a slideshow; >40 blurs into texture. The flicker is the point — only first and final values must be legible |
| SCRUB_DUR               | 1.5–3s                        | shorter = confident sweep; longer = inspection. Leave ≥0.8s of scene after the driver ends so the landed value holds     |
| SCRUB_EASE              | `power1.inOut` default        | `"none"` playhead form; `power3.out` peak stop. Never `back.out` — a read head that overshoots and re-reads looks broken |
| CROSS_P                 | 0.55–0.75                     | earlier and A never establishes; later and B's readout has no time to live                                               |
| TIP_DX / TIP_DY         | 16–48px, up-and-right         | flip the sign near the chart's right edge so the tooltip never exits the frame                                           |
| MARKER_R / stroke width | r 6–12 / 4–8px                | the marker must dominate the line it rides                                                                               |
| TIP_MIN_WIDTH           | ≥ longest `date: value` state | without it the box breathes as digits change                                                                             |

## Critical Constraints

- **`DATA` is literal at setup**; polyline points derive from it via pure functions — chart and readout share one source of truth.
- **Seed at setup** — call the scrub applier once with `p = 0` right after building (à la `3d-camera-flight`'s `applyCamera()`), or a seek to t=0 before the driver runs shows the tracking line/marker at their HTML-default positions.
- **Single driver** — one `p` tween; all scrub outputs (line, marker, tooltip, any cursor) computed in its `onUpdate`, each a pure function of `p`.
- **Readout writes guarded by index change** — `onUpdate` stays O(1): a few attribute sets, one transform, text only on step.
- **SVG `viewBox` units = CSS pixels** (`viewBox="0 0 W H"` with matching `width`/`height`) — one coordinate space must serve the SVG internals and the HTML tooltip's transform.
- **`tabular-nums` + fixed `min-width`** on the tooltip value.
- **The chart pre-exists** — draw-in belongs to `svg-path-draw` / `stat-bars-and-fills`; sequence it BEFORE the scrub, don't blend them.
- **Land the read** — hold the final value ≥0.8s (or hand off to a count-up lockup).

## See also

`svg-path-draw` (the series draws in first) · `stat-bars-and-fills` (surrounding dashboard chrome) · `spring-pop-entrance` (peak dot + pill pop at the landing) · `counting-dynamic-scale` (closing stat lockup) · `cursor-click-ripple` / `context-sensitive-cursor` (the cursor-led form's actor) · `control-target-sync` (the sibling WRITE direction — there a control edits a target; here a scrub reads a dataset).


<!-- ===== FILE: hyperframes/hyperframes-animation/rules/chromatic-glitch.md ===== -->

---
name: chromatic-glitch
description: RGB-split / slice glitch that snaps sharp — offset color copies jitter on a deterministic hash of quantized timeline time (never Math.random), or horizontal slices displace and converge; a brief vibration, then a clean resolve. Entrance or emphasis punctuation; finite, seek-safe.
metadata:
  tags: glitch, rgb-split, chromatic, slice, jitter, stutter, text, snap, distortion
---

# Chromatic Glitch

Digital interference as punctuation: for a fraction of a second the element **breaks** — offset color copies shudder behind it, or horizontal slices displace sideways — then it **snaps sharp** and holds clean. The payoff is the resolve; the glitch exists to make the clean state land harder. Two forms: an **RGB-split jitter** (warm + cool ghost copies vibrating behind the base) and a **slice displacement** (horizontal bands that arrive offset and converge).

Boundaries: [motion-blur-streak.md](motion-blur-streak.md) is velocity blur tied to **travel** — its element is going somewhere fast. A glitching element is **in place**; the disturbance is temporal, not directional. [hacker-flip-3d.md](hacker-flip-3d.md) substitutes **glyphs** (a decode); here the glyphs are fixed and only displaced copies of them move.

## How It Works

The subject is stacked: the **base copy on top** (full legibility at every frame), ghost copies behind. All motion comes from one finite **amplitude-envelope** tween read by an `onUpdate`:

1. **Quantized time** — `const step = Math.floor(tl.time() / JITTER_STEP)`. The stutter comes from offsets that hold for `JITTER_STEP` and then jump. Smoothly interpolated offsets read as wobble, not glitch — **the quantization IS the digital texture**.
2. **Deterministic hash** — offsets are a pure function of `(step, layerIndex)`:

   ```js
   const glitchHash = (n) => {
     const x = Math.sin(n * 127.1 + 311.7) * 43758.5453;
     return x - Math.floor(x); // 0..1, pure — a scrub to any t recomputes the same frame
   };
   ```

3. **Amplitude envelope** — a proxy tween carries `amp: 1 → 0` over `GLITCH_DUR`. Per-frame offset = `amp × (glitchHash(step * 13 + layer * 7) * 2 − 1) × MAX_SPLIT`. When the envelope hits zero the copies sit at exactly 0 — the snap-sharp is built into the math, and a final `tl.set` clamps the rest state so the hold is bit-exact.

The **slice form** swaps color copies for `SLICE_COUNT` full copies, each clipped to a horizontal band via `clip-path: inset()`; per-band `x` (and optional `scaleX` stretch) start at hash-derived offsets and converge to 0 under a stepped ease.

## Recipe

```html
<!-- inside a standard scene clip (hyperframes-core) -->
<!-- Form A: RGB-split — ghosts behind, base on top. Copies metric-identical (one grid cell, same font stack); aria-hidden on every non-base copy. -->
<div class="glitch-stack" id="glitch-stack">
  <span class="glitch-copy warm" aria-hidden="true">{glitchText}</span>
  <span class="glitch-copy cool" aria-hidden="true">{glitchText}</span>
  <span class="glitch-base">{glitchText}</span>
</div>
```

```css
.glitch-stack {
  display: grid; /* all copies share one cell — pixel-identical boxes */
}
.glitch-base,
.glitch-copy {
  grid-area: 1 / 1;
}
.glitch-base {
  z-index: 2; /* grid items take z-index without position */
  color: {textColor};
}
.glitch-copy {
  z-index: 1;
  opacity: 0; /* raised only while the envelope is live */
  will-change: transform; /* updates every frame while live */
  mix-blend-mode: screen; /* additive on dark bg; drop to normal (and lower opacity) on light */
}
.glitch-copy.warm {
  color: {warmSplit}; /* classic: red/orange */
}
.glitch-copy.cool {
  color: {coolSplit}; /* classic: cyan/blue */
}
```

```js
// Form A: RGB-split jitter — envelope snaps to full amplitude, decays to zero.
// All per-frame state derives from tl.time() + the envelope: pure, replays on seek.
const copies = gsap.utils.toArray("#glitch-stack .glitch-copy");
const amp = { a: 0 };
tl.set(amp, { a: 1 }, GLITCH_START);
tl.set(copies, { opacity: SPLIT_OPACITY }, GLITCH_START);
tl.to(
  amp,
  {
    a: 0,
    duration: GLITCH_DUR,
    ease: "power3.in", // most of the violence up front, dying fast
    onUpdate: () => {
      const step = Math.floor(tl.time() / JITTER_STEP); // quantized — the stutter
      copies.forEach((el, layer) => {
        const jx = (glitchHash(step * 13 + layer * 7) * 2 - 1) * MAX_SPLIT * amp.a;
        const jy = (glitchHash(step * 29 + layer * 11) * 2 - 1) * MAX_SPLIT * 0.35 * amp.a;
        gsap.set(el, { x: jx, y: jy });
      });
    },
  },
  GLITCH_START,
);
// The clean resolve: clamp ghosts to exact rest — never rely on the decay
// landing on zero. A ghost left 1px off reads as a bug every frame after.
tl.set(copies, { x: 0, y: 0, opacity: 0 }, GLITCH_START + GLITCH_DUR);

// Form B: slice displacement — N band copies of the same content converge.
const slices = gsap.utils.toArray("#slice-stack .slice");
const bandH = 100 / slices.length;
slices.forEach((el, i) => {
  gsap.set(el, { clipPath: `inset(${i * bandH}% 0 ${100 - (i + 1) * bandH}% 0)` });
  const dir = glitchHash(i * 3 + 1) > 0.5 ? 1 : -1;
  tl.fromTo(
    el,
    {
      x: dir * (SLICE_OFFSET_MIN + glitchHash(i * 5 + 2) * (SLICE_OFFSET_MAX - SLICE_OFFSET_MIN)),
      scaleX: 1 + glitchHash(i * 7 + 3) * SLICE_STRETCH,
      opacity: 1,
    },
    { x: 0, scaleX: 1, duration: SLICE_RESOLVE_DUR, ease: "steps(SLICE_STEPS)" },
    SLICE_START + glitchHash(i * 11 + 4) * SLICE_JITTER_LAG,
  );
});
```

## Variations

- **Glitch-stretch entrance** — the element ENTERS glitching: layer `fromTo(stack, { scaleX: STRETCH_FROM, opacity: 0 }, { scaleX: 1, opacity: 1, duration: GLITCH_DUR, ease: "power4.out" })` (`STRETCH_FROM` 1.3–1.8) on the whole stack while the envelope runs. Stretch, split, and envelope all die at the same frame — the word is simply _there_, sharp.
- **Emphasis burst on a held word** — a spasm, not an arrival: 2–3 short envelopes (`GLITCH_DUR` ~0.12–0.2s each) separated by clean gaps of ~0.2–0.4s, each its own `set(amp)/to(amp)/set(rest)` triplet. The clean frames between bursts make it read as energy instead of a rendering fault.
- **Slice reveal** — Form B as the arrival itself: bands start opaque but displaced, converge under the stepped ease. Drop the color copies for the monochrome version — the restrained enterprise read of this rule.
- **Card / non-text glitch** — the stacked-copy machinery is content-agnostic (logo lockup, small card). Keep `MAX_SPLIT` proportional (~1% of element width) — oversized splits read as broken layout, not interference.

## Values

| token                                        | range                                  | notes                                                                                         |
| -------------------------------------------- | -------------------------------------- | --------------------------------------------------------------------------------------------- |
| MAX_SPLIT                                    | 4–14px at headline sizes (~0.06–0.1em) | vertical ~35% of horizontal; base must stay legible at peak                                   |
| JITTER_STEP                                  | 1/30–1/12 s                            | shorter = frantic buzz, longer = VHS stutter; **≥ one render frame** or quantization vanishes |
| GLITCH_DUR                                   | 0.25–0.6s entrance; 0.12–0.2s burst    | ≥ ~1s stops reading as an event and starts reading as a broken render                         |
| SPLIT_OPACITY                                | 0.5–0.9 (screen on dark)               | 0.35–0.6 unblended on light — screen on white is invisible                                    |
| SLICE_COUNT                                  | 4–10                                   | more = finer tear, diminishing past ~10                                                       |
| SLICE_OFFSET_MIN / MAX                       | 12–60px                                | derive per-band values from `glitchHash(i)`, never uniform — equal offsets read mechanical    |
| SLICE_STRETCH                                | 0–0.5                                  | 0 pure displacement; ~0.3 stretched-scanline read                                             |
| SLICE_RESOLVE_DUR / SLICE_STEPS / JITTER_LAG | 0.2–0.4s / 3–6 / ≤0.08s per band       | the stepped ease keeps the settle digital                                                     |
| {warmSplit} / {coolSplit}                    | —                                      | classic red/cyan; any opposing warm+cool brand pair survives                                  |

## Critical Constraints

- **Quantize time — the stutter IS the effect.** Offsets hold for `JITTER_STEP` then jump; if the glitch looks like jelly, you interpolated. `JITTER_STEP` ≥ one render frame or the quantization silently disappears.
- **Pure functions of (quantized time, index)** — every per-frame value comes from `glitchHash`; the hash inputs use `tl.time()`, nothing else.
- **Clamp the rest state** — `tl.set({ x: 0, y: 0, opacity: 0 })` on the ghosts at envelope end; never rely on the decay landing exactly on zero.
- **Base on top, always legible** — ghosts vibrate _behind_ the base; a glitch that destroys legibility for more than ~2 frames is a tear-down, not an accent.
- **Brief, then clean** — the clean hold after the snap is the actual beat; `GLITCH_DUR` well under half the element's screen time. Emphasis bursts are separate finite triplets.
- **No CSS `@keyframes` glitch loops** — the classic CSS glitch snippet runs on the wall clock and desyncs from seek; every displacement goes through the timeline's `onUpdate`.
- **Match the register** — RGB-split is a loud consumer/tech gesture; the monochrome slice variant is the only form that belongs in a restrained enterprise composition.

## See also

`kinetic-beat-slam` (one beat lands with the glitch-stretch entrance) · `spring-pop-entrance` (pop clean, burst on the stress beat) · `gradient-text-sweep` (gradient carries the hold after the resolve) · `discrete-text-sequence` (state swap masked at max amplitude) · `motion-blur-streak` (the traveling sibling — if it's moving fast, blur it there).


<!-- ===== FILE: hyperframes/hyperframes-animation/rules/context-sensitive-cursor.md ===== -->

---
name: context-sensitive-cursor
description: Cursor color and styling that adapt to the current text segment being typed — accent color on highlights, dim on placeholders, etc.
metadata:
  tags: cursor, color, context, typewriter, styling, segment
---

# Context-Sensitive Cursor

In a typewriter sequence, the cursor's color (and optionally height / blink behavior) matches the **active text segment** — brand accent while typing the brand name, dim on placeholders, success color on the completion mark. The eye lands on the keyword being typed because the cursor shifts with it; a fixed single-color cursor is visual noise by comparison. Layers on top of [discrete-text-sequence](discrete-text-sequence.md)'s SEQUENCE pattern.

## How It Works

The text is authored as a SEQUENCE of `{ t, text, segment, color }` entries; a linear driver's `onUpdate` reverse-searches for the current entry and writes both the visible text and the cursor's `background` (the cursor is a colored block, so `background`, NOT `color`). A second linear tween sweeps a phase `p` through `2π × BLINK_CYCLES_PER_SCENE` and gates cursor opacity on `sin(p) > 0` — a deterministic square-wave blink on the timeline.

## Recipe

```html
<!-- inside a standard scene clip (hyperframes-core) -->
<div class="terminal">
  <div class="prompt">$</div>
  <div class="text-wrap">
    <span class="text" id="text"></span><span class="cursor" id="cursor">_</span>
  </div>
</div>
```

```css
.terminal {
  font-family: {monoFont}; /* proportional fonts drift the cursor mid-segment */
  display: flex;
  align-items: baseline;
  white-space: pre; /* preserve trailing spaces — cursor sits at segment end */
}
.text {
  white-space: pre;
}
.cursor {
  display: inline-block; /* inline ignores width/height */
  width: {cursorWidth}px;
  height: {cursorHeight}px;
  background: {textColor}; /* default — overridden per segment in onUpdate */
  vertical-align: {cursorBaselineFix}px; /* small negative — anchor to baseline, not line-height */
}
```

```js
// Adjacent entries usually share a text prefix but may differ in `segment` —
// that's what shifts the cursor color mid-line.
const SEQUENCE = [
  { t: 0, text: "", segment: "main", color: "{mainColor}" },
  { t: T_LEADIN_END, text: "{leadInChunk}", segment: "main", color: "{mainColor}" },
  { t: T_BRAND_IN, text: "{leadInBrandPrefix}", segment: "brand", color: "{brandColor}" },
  { t: T_BRAND_OUT, text: "{leadInBrandFull}", segment: "main", color: "{mainColor}" },
  { t: T_CMD_IN, text: "{leadInCmdPrefix}", segment: "cmd", color: "{cmdColor}" },
  { t: T_SUCCESS, text: "{leadInDone}", segment: "success", color: "{successColor}" },
];

function entryAt(time) {
  for (let i = SEQUENCE.length - 1; i >= 0; i--) {
    if (time >= SEQUENCE[i].t) return SEQUENCE[i];
  }
  return SEQUENCE[0];
}

const textEl = document.getElementById("text");
const cursorEl = document.getElementById("cursor");

const driver = { t: 0 };
tl.to(
  driver,
  {
    t: DURATION,
    duration: DURATION,
    ease: "none",
    onUpdate: () => {
      const entry = entryAt(driver.t);
      textEl.textContent = entry.text;
      cursorEl.style.background = entry.color;
    },
  },
  0,
);

// Deterministic square-wave blink
const blink = { p: 0 };
tl.to(
  blink,
  {
    p: Math.PI * 2 * BLINK_CYCLES_PER_SCENE,
    duration: DURATION,
    ease: "none",
    onUpdate: () => {
      cursorEl.style.opacity = Math.sin(blink.p) > 0 ? "1" : "0";
    },
  },
  0,
);
```

## Variations

- **Non-blinking during active typing** — suppress blink while letters are appearing (solid cursor), resume on idle. This MUST be a pure function of the driver's time: tracking a mutable `lastChangeTime` in `onUpdate` is not reverse-seek-safe (scrubbing backwards leaves the stale forward-pass value behind and the cursor blinks — or holds solid — at the wrong frames). Bake the change times from the SEQUENCE instead — every entry whose `text` differs from its predecessor is a typing event:

```js
// Baked once at build time — no runtime state.
const CHANGE_TIMES = SEQUENCE.filter((e, i) => i > 0 && e.text !== SEQUENCE[i - 1].text).map(
  (e) => e.t,
);
// In onUpdate — identical result at any seek, either direction:
const isTyping = CHANGE_TIMES.some((t) => t <= driver.t && driver.t - t < TYPING_GRACE);
cursorEl.style.opacity = isTyping ? "1" : Math.sin(blink.p) > 0 ? "1" : "0";
```

- **Cursor HEIGHT shifts on segment** — larger cursor on the brand segment: `cursorEl.style.height = entry.segment === "brand" ? cursorHeightEmphasis : cursorHeight` (1.1–1.25×; more reads as glitch).
- **Contrast reversal** — a dark-text-on-light segment needs a dark cursor too; keep `entry.color` as the single source of truth and read from it.

## Values

| token                  | range                       | notes                                                                                           |
| ---------------------- | --------------------------- | ----------------------------------------------------------------------------------------------- |
| DURATION               | 4–8s per typed line         | `≥ SEQUENCE[last].t + closing dwell`                                                            |
| entry `t` spacing      | 0.2–0.5s micro-additions    | ascending, non-uniform — slow down on highlights                                                |
| segment palette        | 3–4 colors max              | more reads as random; brand vs success should differ in saturation/luminance                    |
| cursorWidth / Height   | 8–24px / 0.85–1.0× fontSize | too thin vanishes in render compression; too tall outranks the text                             |
| cursorBaselineFix      | small negative px           | drop the block to the text baseline                                                             |
| BLINK_CYCLES_PER_SCENE | period ≈ 0.6–1.2s           | **whole number** — otherwise the sin sweep ends mid-cycle and the cursor pops on the last frame |
| TYPING_GRACE           | 0.15–0.3s                   | **< shortest dwell between adjacent entries** — otherwise the cursor never blinks               |

## Critical Constraints

- **Cursor color goes on `background`** — it's a colored block, not a glyph.
- **Blink is timeline-driven sin, pure of any mutable tracker** — the typing-grace variation shows the seek-safe form.
- **`white-space: pre` on text and container** — collapsed trailing spaces park the cursor in the wrong column.
- **Monospace font + `display: inline-block` cursor** — proportional faces drift the cursor mid-segment; inline ignores the block geometry.
- **BLINK_CYCLES_PER_SCENE is a whole number** for the fixed DURATION.

## See also

`discrete-text-sequence` (the underlying SEQUENCE pattern) · `camera-cursor-tracking` (camera follows the cursor) · `press-release-spring` (post-typing confirm press).


<!-- ===== FILE: hyperframes/hyperframes-animation/rules/control-target-sync.md ===== -->

---
name: control-target-sync
description: The live-sync couple — a scrubbed/typed/picked control drives a second element's property in the SAME beat. Readout tween + target transform tween share one timeline label (continuous scrub), or one threshold state array carries both sides (discrete steps). Makes "change this, watch it change" read as causality.
metadata:
  tags: control, scrub, live-sync, mirror, panel, editor, couple, readout, ui
---

# Control-Target Sync

THE live-editing move: an inspector/editor control is manipulated — a value scrubbed, a field retyped, a dropdown picked — and a **bound second element answers in the same frame**. The button rotates WHILE the rotation value scrubs; icons resize PER KEYSTROKE. The persuasion is causality — one gesture, two surfaces changing together — and this rule is the coupling contract that produces it.

Nearest precedent is [reactive-displacement.md](reactive-displacement.md): that rule also derives two elements' motion from one source, but it is **collision physics** — an entering intruder displaces an exiting victim, once, as a transition, and the victim leaves. This rule is a **live editing mirror**: the control is manipulated repeatedly across several beats, the target answers every time, and both sides hold the stage throughout. The numeric readout rides [counting-dynamic-scale.md](counting-dynamic-scale.md)'s proxy pattern; discrete steps ride [discrete-text-sequence.md](discrete-text-sequence.md)'s threshold pattern — what this rule adds is the law that binds either of them to the target.

## How It Works

An **edit beat** is a set of concurrent tweens at ONE timeline label: `tl.addLabel("edit1", …)`, then the **readout tween** (numeric proxy + `onUpdate` writing `textContent` only) and the **target transform tween** (`rotation` / `x` / `y` / `scale` to the same endpoint), both placed at the label with the same **duration** and **ease**. The two motions are two projections of one gesture — value at 40% ⇒ target at 40%, on every frame, under any seek. That mathematical lockstep reads as "the panel is editing the page," not "two animations happen to overlap."

For **discrete edits** (per-keystroke retypes, dropdown picks, unit snaps) the couple steps instead of glides: a single threshold state array carries BOTH sides — each state holds the readout text AND the target's property value — and one driver applies whichever state is active. Both sides read from the same state object, so they cannot desync.

Chain 2–4 edit beats with short holds between, and end on a **landed** edit — the last value applied and holding, never a tooltip with the dropdown unopened.

## Recipe

```html
<!-- Bipartite by construction: target surface + inspector panel share the frame.
     Every scrubbed readout gets `font-variant-numeric: tabular-nums` and a fixed
     min-width (≥ the longest value) or the panel edge jitters as digits change. -->
<div class="target-surface">
  <div class="target-button" id="target-button">{buttonLabel}</div>
  <div class="preview-row">
    <div class="preview-icon">{iconA}</div>
    …
  </div>
</div>
<div class="panel">
  <div class="field-row">
    <span>Rotation</span><span class="field-value" id="rotation-readout">0°</span>
  </div>
  <div class="field-row">
    <span>Class</span><span class="field-value mono" id="class-readout">text-1xl</span>
  </div>
</div>
```

```js
// ---- Continuous couple: ONE label; both tweens share duration AND ease ----
tl.addLabel("edit1", EDIT1_AT);
const rotState = { v: 0 };
const rotReadout = document.getElementById("rotation-readout");
tl.to(
  rotState,
  {
    v: ROT_TARGET,
    duration: SCRUB_DUR,
    ease: SCRUB_EASE,
    onUpdate: () => {
      rotReadout.textContent = `${Math.round(rotState.v)}°`;
    },
  },
  "edit1",
);
tl.to(
  "#target-button",
  { rotation: ROT_TARGET, duration: SCRUB_DUR, ease: SCRUB_EASE },
  "edit1", // same label — the mirror answers in the same frame
);

// ---- Discrete couple: ONE state array carries BOTH sides ----
const STEPS = [
  { t: 0.0, text: "text-1xl", scale: 1.0 }, // must equal the initial state
  { t: 0.4, text: "text-4xl", scale: 1.9 },
  { t: 1.0, text: "text-xl", scale: 0.85 }, // backspace
  { t: 1.35, text: "text-2xl", scale: 1.3 }, // lands
];
const stepAt = (time) => [...STEPS].reverse().find((s) => time >= s.t) ?? STEPS[0];

tl.addLabel("edit3", EDIT3_AT);
const classReadout = document.getElementById("class-readout");
const stepDriver = { t: 0 };
let lastStep = null;
tl.to(
  stepDriver,
  {
    t: STEPS_TOTAL,
    duration: STEPS_TOTAL,
    ease: "none",
    onUpdate: () => {
      const s = stepAt(stepDriver.t);
      if (s !== lastStep) {
        classReadout.textContent = s.text; // control steps
        gsap.set(".preview-icon", { scale: s.scale }); // target steps — same state object
        lastStep = s;
      }
    },
  },
  "edit3",
);
```

## Variations

- **Dropdown pick → instant conversion (self-conversion)** — the pick converts the panel's own readout in place (`tl.set("#padding-readout", { textContent: "6 px" }, "pick")`); control and target collapse into one element. Compose the dropdown from neighbors: menu pops via [spring-pop-entrance.md](spring-pop-entrance.md), row hover-stepping via [dynamic-content-sequencing.md](dynamic-content-sequencing.md). The conversion must be an INSTANT snap — tweening between unit strings reads as broken, and instantness is the feature being sold.
- **Easing-handle drag → target re-animates (deferred mirror)** — the edit authors a _behavior_, so the mirror is a **replay**, not a concurrent transform: beat 1 drags the handle (handle tween + coords readout), then at a later label the target performs its motion with the newly-authored curve (`tl.fromTo("#toggle-knob", { x: 0 }, { x: KNOB_TRAVEL, duration: REPLAY_DUR, ease: AUTHORED_EASE }, "replay")`), often under a zoom-out ([viewport-change.md](viewport-change.md)). The one sanctioned case where the response is not in the gesture's beat; the replay must still be unmistakably the edited parameter.
- **Read-sync mirror (reverse direction)** — the gesture happens ON the target (hovering swatches, selecting an element) and the PANEL readout is the bound side. Same discrete contract — one state array of `{ t, hoverTarget, readout }` drives both the highlight and the text.
- **Color couple** — the readout counts (`0 → 80`) while the target's `backgroundColor` tweens between two palette stops at the same label. Keep it two fixed stops (GSAP interpolates); never derive per-frame hex strings by hand.

## Values

| token                | range                           | notes                                                                                                                                 |
| -------------------- | ------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------- |
| SCRUB_DUR            | 0.8–1.6 s                       | the viewer must see BOTH sides move — under ~0.6 s the mirror registers subconsciously at best                                        |
| SCRUB_EASE           | `power1.inOut` / `power2.inOut` | shared verbatim by both tweens. Never `back.out` / `elastic.out` — an overshooting value reads as a broken hinge; the readout is data |
| edit endpoints       | visible but plausible           | −10° tilt, 38 px shift, 1xl → 4xl → 2xl; a 2° rotation doesn't demo anything                                                          |
| HOLD_BETWEEN         | 0.3–0.8 s                       | each landed value gets a breath; below 0.3 s the beats smear into one gesture                                                         |
| BEAT_COUNT           | 2–4                             | one edit is a moment, not a demo; past 4 the shot reads as a settings tour                                                            |
| STEP gaps (discrete) | 0.15–0.5 s                      | keystroke pacing per discrete-text-sequence; first state must equal the on-load state                                                 |
| VALUE_MIN_WIDTH      | ≥ longest value's width         | without it the panel edge jitters as digit counts change                                                                              |

## Critical Constraints

- **One label, one gesture** — readout tween and target tween share position, duration, AND ease; never sequence readout-then-target, and never stagger the target behind the readout even by 0.1 s — a delayed response reads as an animation following an edit, not a bound surface. A mismatched ease desyncs the mirror mid-tween even when endpoints agree.
- **Discrete steps share one state object** — both sides read the same array entry, so desync is impossible by construction; first entry mirrors the initial DOM state.
- **The readout is data** — no overshoot, no bounce on the settle; the target may carry the gesture's ease but lands exactly on the edited value.
- **Co-visibility is load-bearing** — control and target share the frame for every edit beat; a camera move must never crop the mirror out (punch-and-return around the beats, not through them).
- **`tabular-nums` + fixed `min-width`** on every scrubbed readout; `onUpdate` is O(1) — text writes only, discrete drivers guard writes with a last-state check.
- **End on a landed edit** — the final beat resolves with the value applied and holding (or the deferred-mirror replay); never mid-gesture or on an unopened menu.
- **The gesture's actor is a separate rule** — cursor glide, grab-cursor flip, and click feedback come from the cursor rules; this rule owns only the couple.

## See also

`cursor-click-ripple` / `context-sensitive-cursor` (the hand performing the gesture) · `counting-dynamic-scale` (the readout half alone, when there is no bound target) · `discrete-text-sequence` (retypes inside the control field) · `spring-pop-entrance` (dropdowns/chrome around the couple) · `multi-phase-camera` (punch-and-return framing) · `chart-scrub-readout` (the sibling READ direction — a scrub interrogates a chart instead of editing a target).


<!-- ===== FILE: hyperframes/hyperframes-animation/rules/coordinate-target-zoom.md ===== -->

---
name: coordinate-target-zoom
description: Zoom into a specific non-centered element by combining scale with counter-translation — target ends at viewport center after the zoom completes.
metadata:
  tags: camera, zoom, scale, translate, target, off-center, focus
---

# Coordinate Target Zoom

A simple `scale > 1` on a wrapper pushes off-center content OFF the visible canvas. To zoom _into_ a specific non-centered element, apply scale AND an inverse translation in lockstep so the target lands at viewport center.

## How It Works

Two nested wrappers, separated concerns — never scale and translate on the SAME element (`translate * scale` ≠ `scale * translate` in CSS transform composition):

1. **Outer wrapper** applies `scale` (the zoom) around `transform-origin: 50% 50%`
2. **Inner wrapper** applies `translate(x, y)` (the counter-shift)

The counter-translate is the **negation** of the target's offset from viewport center:

```
T = -offset
```

Derivation: the inner translate moves the target to `offset + T` in pre-scale units; the outer scale S (around center) maps that to `S × (offset + T)`; landing at center means `S × (offset + T) = 0` → **`T = -offset`**. The formula does NOT depend on S — the translate is identical at 1.5×, 2×, or 3×. A common wrong intuition is `T = -offset × (S - 1)`: it coincidentally matches at S = 2 and is wrong at every other scale.

⚠️ **This is the NESTED-wrapper formula.** The single-wrapper camera in [viewport-change.md](viewport-change.md) puts `translate(x,y) scale(S)` on ONE element, where CSS applies scale first — there the counter-translate is **`T = -offset × S`**. The two formulas are not interchangeable; match the formula to the wrapper structure.

## Getting the offset

`T = -offset` is only as good as `offset`. The #1 way this pattern ships broken is hand-computing `offset` from a layout formula, getting the **sign** or magnitude wrong, and letting the zoom amplify a small error off-screen. **Default to measuring the target's real laid-out center; reserve the formula for symmetric rows.**

**Default — measure the actual center (works for ANY layout).** Immune to sign errors because it reads the rendered DOM, not a mental model:

```js
await document.fonts.ready; // metrics final; fallback fonts are 10–30px off → tens of px after a 3×+ zoom
const W = 1920,
  H = 1080;
const r = document.getElementById("target-card").getBoundingClientRect();
const TARGET_OFFSET_X = r.left + r.width / 2 - W / 2;
const TARGET_OFFSET_Y = r.top + r.height / 2 - H / 2;
```

Measure **once at setup** and bake — never per-frame in `onUpdate`. Because the measurement is async (`fonts.ready`), build and register the timeline inside the same `async` setup so the baked offset is ready before `window.__timelines[id]` is published.

**Shortcut — symmetric equal-width row ONLY:**

```js
const index_offset = targetIndex - (N - 1) / 2;
const TARGET_OFFSET_X = index_offset * (CARD_WIDTH + CARD_GAP);
```

⚠️ This assumes every sibling is the **same width**. The moment the row is asymmetric, it gives the wrong answer — often the wrong **sign**: the heavier side shifts the centered target the _opposite_ way you'd guess (e.g. `companion(220) + gap + wordmark + gap + chip(110)` puts the wordmark ~55px **right** of center, but "chip − companion" intuition says left). For anything but equal cards, **measure**.

**Headroom budget — cap the scale from the measured size.** A zoom multiplies any centering error; keep the target ≤ ~88% of the canvas at peak:

```js
const maxScale = Math.min((0.88 * W) / r.width, (0.88 * H) / r.height);
const ZOOM_SCALE = Math.min(DESIRED_SCALE, maxScale);
```

A target filling 97%+ of the frame reads as cut-off the instant its center is slightly off — and a hand-baked offset always is. (The perception gate flags this as `primary-offscreen`; `data-layout-allow-overflow` does **not** exempt it.)

## Recipe

```html
<div class="zoom-outer" id="zoom-outer">
  <div class="zoom-inner" id="zoom-inner">
    <div class="content">
      <div class="card">{other}</div>
      <div class="card target" id="target-card">{target}</div>
      <div class="card">{other}</div>
    </div>
  </div>
</div>
```

```css
.scene {
  overflow: hidden; /* REQUIRED — at zoom > 1 the scaled content leaks past the frame */
}
.zoom-outer {
  width: 100%;
  height: 100%;
  display: grid;
  place-items: center;
  transform-origin: 50% 50%; /* center scaling is what the counter-translate math assumes */
  will-change: transform;
}
.zoom-inner {
  display: grid;
  place-items: center;
  will-change: transform;
}
```

```js
// TARGET_OFFSET_X/Y and ZOOM_SCALE come from "Getting the offset" — measured
// at setup (after fonts.ready), baked. Counter-translation = -offset.
const counterX = -TARGET_OFFSET_X;
const counterY = -TARGET_OFFSET_Y;

// Scale and counter-translate MUST share position, duration, AND ease —
// otherwise the target visibly wanders mid-zoom.
tl.to("#zoom-outer", { scale: ZOOM_SCALE, duration: ZOOM_DUR, ease: "power3.inOut" }, ZOOM_AT);
tl.to(
  "#zoom-inner",
  { x: counterX, y: counterY, duration: ZOOM_DUR, ease: "power3.inOut" },
  ZOOM_AT,
);
```

## Variations

- **Zoom out (target → wide view)**: reverse the phases — start zoomed-in, then tween to `scale: 1` + `x: 0, y: 0`; the "reveal" beat is the panorama.
- **Multi-target zoom sequence**: chain zooms (target A → pause → target B → pull back); each segment needs its own counter-translation pair.

## Values

| token      | range                                   | notes                                                                                      |
| ---------- | --------------------------------------- | ------------------------------------------------------------------------------------------ |
| ZOOM_SCALE | 1.5× modest → 3× dominant → 5×+ extreme | cap via the headroom budget; raster media needs `sourceResolution ≥ rendered × ZOOM_SCALE` |
| ZOOM_DUR   | 1.0–2.0s                                | under 0.8s feels like a teleport, over 2.5s drags; both tweens share it                    |
| ZOOM_AT    | after the layout lands + 0.5–1.5s       | give the viewer time to scan the layout before the camera commits                          |
| DWELL      | ≥ 1.0s after the zoom settles           | 1.5–2s ideal — the viewer must be able to read the target (climax dwell)                   |

## Critical Constraints

- **Outer scales, inner translates** — never both transforms on one element; nested wrappers keep the math clean.
- **`transform-origin: 50% 50%` on the outer wrapper** — non-center origin breaks the counter-translate derivation.
- **`overflow: hidden` on the scene root** — zoomed content leaks past the frame otherwise.
- **Scale and counter-translate share duration + ease** at the same timeline position, or the target drifts mid-zoom.
- **Offset measured once at setup** (after `fonts.ready`), baked — never recomputed per-frame, never hand-derived for a non-symmetric layout (wrong sign → target shoved off-frame).
- **Scale within the headroom budget** — target ≤ ~88% of the canvas at peak, derived from the measured size.

## See also

[viewport-change.md](viewport-change.md) (single-wrapper form, `T = -offset × S`) · [multi-phase-camera.md](multi-phase-camera.md) (a zoom phase inside a phased camera) · [sine-wave-loop.md](sine-wave-loop.md) (idle breathing after the zoom settles) · [discrete-text-sequence.md](discrete-text-sequence.md) (text assembly in the target before the zoom).


<!-- ===== FILE: hyperframes/hyperframes-animation/rules/counting-dynamic-scale.md ===== -->

---
name: counting-dynamic-scale
description: Counter animation where the value counts up while transform scale grows to its final size, creating escalating visual weight without per-frame text reflow.
metadata:
  tags: counter, counting, scale, transform, number, dynamic, emphasis
---

# Counting with Dynamic Scale

A number counts from A → B while its transform scale grows to the final size — escalating visual weight ("this is impressive") without tweening `font-size` or forcing text layout on every frame. The final font size is static CSS; only the transform changes.

## How It Works

Two synchronized tweens at the SAME timeline position with the SAME ease: (1) a proxy value rendered as text via `onUpdate` (`Math.round(...).toLocaleString()`), (2) the counter's transform `scale: START_SCALE → 1`, where `START_SCALE = START_SIZE / END_SIZE`. A suffix (`%`, `×`, `+`) slides in AFTER the count lands — the number gets its own beat — and a label fades in early.

## Recipe

```html
<!-- inside a standard scene clip (hyperframes-core) -->
<div class="counter-wrap">
  <span class="counter" id="counter">0</span><span class="counter-suffix">{suffix}</span>
</div>
<div class="counter-label">{label}</div>
```

```css
.counter-wrap {
  display: flex;
  align-items: baseline;
  justify-content: center;
  width: {counterContainerWidth}; /* fixed width — no layout shift as digit count changes */
}
.counter {
  font-variant-numeric: tabular-nums; /* MANDATORY — digits keep equal width */
  display: inline-block;
  font-size: {endSize}; /* final size is static; GSAP animates scale, not font-size */
  transform-origin: center center;
}
.counter-suffix {
  opacity: 0;
  transform: translateY(20px);
}
```

```js
const counter = document.getElementById("counter");
const state = { value: 0 };
const START_SCALE = START_SIZE / END_SIZE;

// Count value — onUpdate changes text only
tl.to(
  state,
  {
    value: TARGET_VALUE,
    duration: COUNT_DUR,
    ease: COUNT_EASE,
    onUpdate: () => {
      counter.textContent = Math.round(state.value).toLocaleString();
    },
  },
  0,
);

// Visual growth — compositor transform sharing the count's timing + ease
tl.fromTo(counter, { scale: START_SCALE }, { scale: 1, duration: COUNT_DUR, ease: COUNT_EASE }, 0);

// Suffix slides in AFTER the count completes
tl.to(
  ".counter-suffix",
  { opacity: 1, y: 0, duration: SUFFIX_DUR, ease: `back.out(${SUFFIX_BOUNCE_FACTOR})` },
  COUNT_DUR,
);

// Label fades in early
tl.from(".counter-label", { opacity: 0, y: 12, duration: LABEL_DUR, ease: "power2.out" }, LABEL_AT);
```

## Variations

- **Direct `innerText` tween (no proxy)** — GSAP can tween `innerText` directly for a number-only counter; keep the proxy form when you need locale formatting or suffix logic. The scale tween stays separate either way:

```js
tl.to(
  counter,
  { innerText: TARGET_VALUE, duration: COUNT_DUR, ease: COUNT_EASE, snap: { innerText: 1 } },
  0,
);
```

- **3D depth entry** — add a `tl.from(".counter", { z: -300, ... }, 0)` push-in; requires `perspective` on `.counter-wrap` and `transform-style: preserve-3d` on the counter.
- **Multi-stat coordinated reveal** — 3 stats counting in parallel share the SAME ease, duration, and start position so they finish together (a chord, not an arpeggio). Each stat usually also needs a paired graphic (bar / ring / stars) — don't stop at the number; see [stat-bars-and-fills.md](stat-bars-and-fills.md).

## Values

| token                 | range                                       | notes                                                                         |
| --------------------- | ------------------------------------------- | ----------------------------------------------------------------------------- |
| TARGET_VALUE          | 2–3 digits ideal                            | 4+ digits needs a wider container; must fit at END_SIZE without clipping      |
| START_SIZE / END_SIZE | START ≈ 40–60% of END                       | design inputs used once for START_SCALE; never tween either                   |
| COUNT_DUR             | 1.2–2.5s                                    | below ~0.8s reads as a flash — the eye must read the digits scrolling past    |
| COUNT_EASE            | `power2.out` / `power3.out` ⭐ / `expo.out` | shared by value + scale; more `.out` = more dramatic deceleration at the peak |
| SUFFIX_DUR            | 0.3–0.6s                                    | fires at `COUNT_DUR`, never during the count                                  |
| SUFFIX_BOUNCE_FACTOR  | 1.4–2.0                                     | overshoot is fine on the suffix (it's punctuation, not data)                  |
| LABEL_AT / LABEL_DUR  | AT < COUNT_DUR/2; 0.4–0.7s                  | label arrives before the count peaks                                          |

## Critical Constraints

- **`tabular-nums` mandatory** + fixed-width container as belt-and-suspenders — without them digit-count transitions (9 → 10 → 100) jitter as glyph widths change.
- **Never set `fontSize` in `onUpdate`** — final type size is static CSS; only the transform changes per frame. Keep `onUpdate` O(1): set text only, no style writes or DOM creation.
- **`Math.round`, not `Math.floor`** — halfway through the final integer should already display the final value.
- **Avoid `back.out` / `elastic.out` on the counter itself** — overshoot makes the number look unstable (it's data, not decoration). Grow in place, don't bounce.
- **Label is BIG TEXT, not a page-style caption** — a tiny paragraph under a hero-size number reads as visual noise in video. Display-size, uppercase, tracked: the label is part of the headline.

## See also

`stat-bars-and-fills` (the paired graphic — give it the same ease/duration so number and fill land as one beat) · `svg-path-draw` (icons drawing in around the number) · `center-outward-expansion` (icons bursting outward at the count peak).


<!-- ===== FILE: hyperframes/hyperframes-animation/rules/css-marker-patterns.md ===== -->

# CSS Patterns for Marker Highlighting

Pure CSS + GSAP implementations of all five MarkerHighlight.js drawing modes — no external library dependency, full timeline control. Snippets show mechanism DOM only, inside a standard scene clip (hyperframes-core); assume `tl` exists.

Shared scaffold for every mode: the wrap is `position: relative; display: inline`; the text copy is `position: relative` and z-indexed **above** the accent (below it for sketchout, where the lines cross the text).

## 1. Highlight Mode

Yellow marker sweep behind text — the most common mode.

```html
<span class="mh-highlight-wrap">
  <span class="mh-highlight-bar" id="hl-1"></span>
  <span class="mh-highlight-text">highlighted text</span>
</span>
```

```css
.mh-highlight-bar {
  position: absolute;
  inset: 0 -6px; /* bleed past the text edges */
  background: #fdd835;
  opacity: 0.35;
  transform: scaleX(0);
  transform-origin: left center;
  border-radius: 3px;
  z-index: 0;
}
```

```js
tl.to("#hl-1", { scaleX: 1, duration: 0.5, ease: "power2.out" }, 0.6);
// Optional hand-drawn skew: gsap.set("#hl-1", { skewX: -2 });
// Multi-line: tl.to(".mh-highlight-bar", { scaleX: 1, ..., stagger: 0.3 }, 0.6);
```

## 2. Circle Mode

Hand-drawn ellipse around text — `border-radius: 50%` plus a slight rotation for organic feel.

```html
<span class="mh-circle-wrap">
  <span class="mh-circle-text">IMPORTANT</span>
  <span class="mh-circle-ring" id="circle-1"></span>
</span>
```

```css
.mh-circle-ring {
  position: absolute;
  top: 50%;
  left: 50%;
  width: 130%; /* tight (short words): 150%; rounded-rect: 120% + border-radius: 30% */
  height: 160%;
  transform: translate(-50%, -50%) rotate(-3deg) scale(0);
  border: 3px solid #e53935;
  border-radius: 50%;
  z-index: 0;
}
```

```js
tl.to("#circle-1", { scale: 1, rotation: -3, duration: 0.6, ease: "back.out(1.7)" }, 0.7);
```

## 3. Burst Mode

Radiating lines from text center — each line a positioned span rotated to its angle. Use ~12 lines at 30° steps and **vary `--len` (40–80px)**; equal lengths look mechanical.

```html
<span class="mh-burst-wrap">
  <span class="mh-burst-text">WOW</span>
  <span class="mh-burst-container" id="burst-1">
    <span class="mh-burst-line" style="--angle: 0deg; --len: 70px;"></span>
    <span class="mh-burst-line" style="--angle: 30deg; --len: 55px;"></span>
    <!-- …one line per 30° step through 330deg, --len varied 40-80px -->
  </span>
</span>
```

```css
.mh-burst-container {
  position: absolute;
  top: 50%;
  left: 50%;
  width: 0;
  height: 0;
  z-index: 1; /* text copy at z-index: 2 */
}
.mh-burst-line {
  position: absolute;
  display: block;
  width: 3px;
  height: var(--len);
  background: #1e88e5;
  left: -1.5px;
  top: calc(-1 * var(--len));
  transform: rotate(var(--angle));
  transform-origin: bottom center;
  opacity: 0;
}
```

```js
tl.fromTo(
  "#burst-1 .mh-burst-line",
  { scaleY: 0, opacity: 0 },
  { scaleY: 1, opacity: 1, duration: 0.4, ease: "power2.out", stagger: 0.03 },
  0.7,
);
```

## 4. Scribble Mode

Wavy SVG underline that draws itself via `stroke-dashoffset`.

```html
<span class="mh-scribble-wrap">
  <span class="mh-scribble-text">underlined text</span>
  <svg class="mh-scribble-svg" viewBox="0 0 500 24" preserveAspectRatio="none">
    <path
      id="scribble-1"
      d="M0,12 Q31,0 62,12 Q93,24 125,12 Q156,0 187,12 Q218,24 250,12 Q281,0 312,12 Q343,24 375,12 Q406,0 437,12 Q468,24 500,12"
      fill="none"
      stroke="#FDD835"
      stroke-width="3"
      stroke-linecap="round"
    />
  </svg>
</span>
```

```css
.mh-scribble-svg {
  position: absolute;
  left: 0;
  bottom: -6px; /* strikethrough variant: top: 50%; transform: translateY(-50%) */
  width: 100%;
  height: 24px;
  z-index: 0;
}
```

```js
const path = document.querySelector("#scribble-1");
const len = path.getTotalLength();
gsap.set(path, { strokeDasharray: len, strokeDashoffset: len });
tl.to("#scribble-1", { strokeDashoffset: 0, duration: 0.8, ease: "power1.inOut" }, 0.7);
```

Path tuning: the `Q` control points alternate y between 0 and 24 for a natural wobble. Tighter waves = smaller x-increments (~25px per half-wave); looser = ~50px; subtler amplitude = y range 0–16.

## 5. Sketchout Mode

Cross-hatch over de-emphasized text — two angled lines create a "crossed out" effect.

```html
<span class="mh-sketchout-wrap">
  <span class="mh-sketchout-text">old price</span>
  <span class="mh-sketchout-lines" id="sketchout-1">
    <span class="mh-sketchout-line mh-sketchout-fwd"></span>
    <span class="mh-sketchout-line mh-sketchout-bwd"></span>
  </span>
</span>
```

```css
.mh-sketchout-lines {
  position: absolute;
  inset: 0 -4px;
  overflow: hidden;
  z-index: 1; /* text at z-index: 0 — the lines cross OVER it */
}
.mh-sketchout-line {
  position: absolute;
  display: block;
  top: 50%;
  left: 0;
  width: 100%;
  height: 2px;
  background: #e53935;
  transform-origin: left center;
}
.mh-sketchout-fwd {
  transform: scaleX(0) rotate(-12deg);
}
.mh-sketchout-bwd {
  transform: scaleX(0) rotate(12deg);
}
```

```js
// Forward slash first, backward follows
tl.to("#sketchout-1 .mh-sketchout-fwd", { scaleX: 1, duration: 0.3, ease: "power2.out" }, 1.0);
tl.to("#sketchout-1 .mh-sketchout-bwd", { scaleX: 1, duration: 0.3, ease: "power2.out" }, 1.15);
```

## Combining Modes in Captions

Cycle modes across caption groups for visual variety — every 2-3 groups for high energy, 3-4 for medium, 4-5 for low:

```js
const MODES = ["highlight", "circle", "burst", "scribble"];
GROUPS.forEach((group, gi) => {
  const mode = MODES[gi % MODES.length];
  group.emphasisWords.forEach((word) => applyMode(word.el, mode, tl, word.start));
});
```


<!-- ===== FILE: hyperframes/hyperframes-animation/rules/cursor-click-ripple.md ===== -->

---
name: cursor-click-ripple
description: Animated mouse cursor moves to target, clicks with scale depression and expanding ripple rings.
metadata:
  tags: cursor, click, ripple, interaction, mouse, button
---

# Cursor Click Ripple

An animated cursor moves to a target element, performs a click with visual depression, and emits expanding ripple rings from the click point. Three sequential phases on one timeline: **move** (eased translation to the target's center) → **click** (scale depression on cursor + target together, yoyo back) → **ripple** (1–3 staggered rings expand and fade from the click point). This is a _point event at one location_ — a sustained hold across space is [cursor-drag.md](cursor-drag.md).

## Recipe

```html
<button class="target-button">{ctaLabel}</button>
<div class="cursor"><!-- arrow SVG, positioned at the entry corner --></div>
<!-- Rings live in DOM from t=0 at the click-target CENTER, scale 0 + opacity 0 -->
<div class="ripple ripple-1"></div>
<div class="ripple ripple-2"></div>
<div class="ripple ripple-3"></div>
```

```css
.ripple {
  position: absolute;
  left: 50%;
  top: 50%; /* click-target center */
  width: 100px;
  height: 100px;
  border-radius: 50%;
  border: 2px solid {rippleColor};
  transform: translate(-50%, -50%) scale(0);
  opacity: 0;
  pointer-events: none;
}
```

```js
// Phase 1 — Move: eased, not linear
tl.to(".cursor", { x: TARGET_X, y: TARGET_Y, duration: MOVE_DUR, ease: MOVE_EASE }, 0);

// Phase 2 — Click: cursor + target depress together, then return
tl.to(
  ".cursor",
  { scale: CURSOR_PRESS_SCALE, duration: PRESS_DUR, ease: "power2.in", yoyo: true, repeat: 1 },
  CLICK_AT,
);
tl.to(
  ".target-button",
  { scale: TARGET_PRESS_SCALE, duration: PRESS_DUR, ease: "power2.in", yoyo: true, repeat: 1 },
  CLICK_AT,
);

// Phase 3 — Ripple burst, N rings staggered from the click point
tl.set([".ripple-1", ".ripple-2", ".ripple-3"], { opacity: 1 }, RIPPLE_AT);
tl.to(
  [".ripple-1", ".ripple-2", ".ripple-3"],
  {
    scale: RIPPLE_SCALE,
    opacity: 0,
    duration: RIPPLE_DUR,
    ease: RIPPLE_EASE,
    stagger: RIPPLE_STAGGER,
    immediateRender: false, // holds scale 0 / opacity 0 until the click moment
  },
  RIPPLE_AT,
);
```

## Variations

- **Single ring** — one `.ripple`, no stagger; more elegant when the rest of the scene is busy.
- **Keyframed attack-decay** — a `keyframes` block ramps opacity 0 → peak → 0 across the duration; a clearer "energy radiates and dissipates" envelope.
- **Multi-ring expanding pulse** — 3 rings at 0.08 s stagger when the click is the scene's climactic moment.

## Values

| token                       | range                       | notes                                                                                                                                  |
| --------------------------- | --------------------------- | -------------------------------------------------------------------------------------------------------------------------------------- |
| MOVE_DUR                    | 0.4–1.0 s                   | short darts; long reads as a "considered click." Must end before CLICK_AT or it reads as a misclick                                    |
| MOVE_EASE                   | discrete choice             | `power2.inOut` calm · `power3.out` decisive · `back.out(1.2–1.4)` settles onto the button with a tiny recoil (higher reads cartoonish) |
| CLICK_AT                    | `MOVE_DUR + 0–0.3 s`        | zero pause reads as autopilot; >0.3 s reads as hesitation                                                                              |
| PRESS_DUR                   | 0.06–0.12 s (half; yoyo ×2) | short crisp, long mushy; must finish before the next phase needs normal scale                                                          |
| CURSOR / TARGET_PRESS_SCALE | 0.80–0.90 / 0.92–0.97       | cursor compresses MORE than the target — the cursor is the actor, the target the recipient                                             |
| RIPPLE_AT                   | `CLICK_AT + 0–0.08 s`       | simultaneous feels causal; slight delay feels acoustic                                                                                 |
| RIPPLE_DUR                  | 0.5–1.0 s                   | sharp ping vs soft sonar; must complete before anything that needs the ring gone                                                       |
| RIPPLE_SCALE                | 3–6                         | 3 stays near the click site; if the ring would exit the frame before fading, lower it                                                  |
| RIPPLE_STAGGER              | 0.06–0.12 s (or 0)          | below ~0.06 s reads as one thick ring; above ~0.12 s as separate events                                                                |
| RIPPLE_EASE                 | discrete choice             | `power2.out` standard ping · `power3.out` sharper attack · `expo.out` strong distant pulse                                             |
| TARGET_X / TARGET_Y         | layout-derived              | must match the target's visual centroid — a 4 px miss reads as missing the button                                                      |

Reference values: `../examples/cta-orbit-collapse.html` — 0.5 s move on `back.out(1.3)`, click +0.2 s, press 0.08 s at 0.85/0.95, single ring to 5× over 0.7 s `power2.out`.

## Critical Constraints

- **Move before click** — trigger the click only after the move tween settles; clicking mid-motion reads as unintentional.
- **Rings live in DOM from t=0** at the click-target center with `scale: 0` + `opacity: 0` — never conditionally rendered; `immediateRender: false` on the expand so they hold invisible until the trigger.
- **Ripple from the click point** — the button's visual center, not any element's bounding-box origin.
- **Synchronized depression** — cursor + target depress at the same position with the same duration, and both yoyo back.
- **Cursor above all content** (high z-index) for the whole sequence; `pointer-events: none` on cursor + ripples.

## See also

`orbit-3d-entry` (click as the pivot that collapses orbiters) · `center-outward-expansion` (click triggers an outward burst) · `press-release-spring` (stronger physical feel on the target) · `scale-swap-transition` (the button's post-click state change).


<!-- ===== FILE: hyperframes/hyperframes-animation/rules/cursor-drag.md ===== -->

---
name: cursor-drag
description: The drag verb for driven cursors — grab, lift, travel, drop-snap. A semi-transparent ghost chip rides the cursor in exact lockstep and snaps into a placed field with selection chrome; variants cover fill-handle auto-fill down rows, corner-handle proportional resize (uniform scale only), and grab-lift-reorder with the neighbor springing into the vacated slot.
metadata:
  tags: cursor, drag, drop, ghost, handle, resize, reorder, snap, interaction, mouse
---

# Cursor Drag

> Cursor look, sizing, off-screen entry, and tip-targeting defer to the **oversized-cursor house doctrine** — this rule owns the drag _mechanics_ only.

THE held-journey verb: the cursor presses down on a payload, carries it, and releases it somewhere else. The load-bearing law is **lockstep**: the cursor tip and the payload's grip point move as one rigid object for the entire travel — a one-frame drift reads as the chip slipping out of the hand. Distinct from [cursor-click-ripple.md](cursor-click-ripple.md) (move → point event at a single location): a drag is a _sustained hold across space_, and the payload is the co-star. Reuse [physics-press-reaction.md](physics-press-reaction.md) for the grab's press dip (cursor + payload compress together); for N simultaneous actors see [multi-cursor-choreography.md](multi-cursor-choreography.md) — this rule is one protagonist performing a workflow beat.

## How It Works

Five beats: **approach** (cursor glides to the source chip, `power2.inOut`) → **grab** (press dip on cursor + chip together; on the down-beat `tl.set` reveals the **ghost** — a pre-rendered semi-transparent clone at the chip's position — plus a small lift `fromTo` to `GHOST_LIFT_SCALE` with a soft shadow, `immediateRender: false`) → **travel** (cursor and ghost move as **matched tweens**) → **drop** (ghost off, placed field pops in with selection chrome) → **adjust / exit** (optional handle resize, then the cursor glides to the next target).

Matched tweens = same timeline position, same duration, same ease, over straight lines — that keeps the pair rigidly locked at every eased midpoint. A shared `[cursor, ghost]` targets array only works when both need identical deltas; with different start points, use two matched `fromTo`s. Rule-specific corollary of the contract's absolute-values law: a relative `+=` travel on either partner breaks the lockstep under seek.

Measure chip and slot rects at build time — a 4 px miss on the drop line reads as a failed drag (montage: authored CSS-matched constants, per the contract). `TIP_OFFSET_X/Y` aligns the cursor's TIP (not its bbox) with the grip point.

## Recipe

```html
<!-- Ghost = clone of the chip AT the chip's position, in DOM from t=0, opacity: 0.
     Same silhouette as the chip — or hand and payload read as different objects.
     Placed field sits at the slot's final position, opacity: 0, with a .select-box
     and four corner .handle elements inside. -->
<div class="tray-chip" id="source-chip"><span class="grip-dots">⋮⋮</span> {chipLabel}</div>
<div class="drag-ghost" id="drag-ghost"><span class="grip-dots">⋮⋮</span> {chipLabel}</div>
<div class="placed-field" id="placed-field">
  {placedLabel}
  <!-- + selection chrome -->
</div>
<div class="cursor" id="cursor"><!-- arrow SVG --></div>
```

```js
const chipRect = document.querySelector("#source-chip").getBoundingClientRect();
const slotRect = document.querySelector("#placed-field").getBoundingClientRect();
const TRAVEL_DX = slotRect.left - chipRect.left;
const TRAVEL_DY = slotRect.top - chipRect.top;

// Travel — MATCHED tweens: same position, duration, ease; absolute endpoints.
tl.fromTo(
  "#drag-ghost",
  { x: 0, y: 0 },
  { x: TRAVEL_DX, y: TRAVEL_DY, duration: TRAVEL_DUR, ease: TRAVEL_EASE, immediateRender: false },
  TRAVEL_AT,
);
tl.fromTo(
  "#cursor",
  { x: chipRect.left + TIP_OFFSET_X, y: chipRect.top + TIP_OFFSET_Y },
  {
    x: chipRect.left + TIP_OFFSET_X + TRAVEL_DX,
    y: chipRect.top + TIP_OFFSET_Y + TRAVEL_DY,
    duration: TRAVEL_DUR,
    ease: TRAVEL_EASE,
    immediateRender: false,
  },
  TRAVEL_AT,
);

// Drop is a state commit: ghost off + placed field on at the SAME position.
tl.set("#drag-ghost", { opacity: 0 }, DROP_AT);
tl.fromTo(
  "#placed-field",
  { opacity: 0, scale: 0.92 },
  { opacity: 1, scale: 1, duration: SNAP_DUR, ease: "power3.out" },
  DROP_AT,
);
tl.fromTo(
  [".select-box", ".handle"],
  { opacity: 0, scale: 0.6 },
  { opacity: 1, scale: 1, duration: 0.18, ease: "power3.out", stagger: 0.02 },
  DROP_AT + SNAP_DUR * 0.4,
);
```

## Variations

- **Corner-handle proportional resize** — width/height tweens are forbidden, so the resize renders as uniform `scale` with `transform-origin` at the **opposite (anchor) corner**: the anchor stays put, the dragged corner travels. The corner's position is _linear in scale_ (`corner = anchor + scale × (corner₀ − anchor)`), so a cursor tween to the corner's end position with the **same duration and ease** stays glued to the handle exactly:

  ```js
  tl.to(
    "#placed-field",
    { scale: RESIZE_SCALE, transformOrigin: "0% 0%", duration: RESIZE_DUR, ease: "power2.inOut" },
    RESIZE_AT,
  );
  tl.to(
    "#cursor",
    { x: CORNER_END_X, y: CORNER_END_Y, duration: RESIZE_DUR, ease: "power2.inOut" },
    RESIZE_AT,
  );
  ```

  One-axis resizes are `scaleX`/`scaleY` on the same origin logic — stretch-safe boxes only; route to [anchored-layout-expand.md](anchored-layout-expand.md)'s counter-scale when content must stay undistorted.

- **Fill-handle auto-fill** — the spreadsheet verb: the cursor drags a cell's fill handle straight down on a `"none"` (linear) ease; each row commits via a snapped `tl.set` (never a fade) keyed to the handle's linear progress, so the fill edge and cursor never separate:

  ```js
  tl.fromTo(
    "#cursor",
    { y: HANDLE_Y },
    { y: HANDLE_Y + FILL_DIST, duration: FILL_DUR, ease: "none", immediateRender: false },
    FILL_AT,
  );
  gsap.utils.toArray(".fill-cell").forEach((cell, i) => {
    tl.set(cell, { opacity: 1 }, FILL_AT + ((i + 1) / CELL_COUNT) * FILL_DUR);
  });
  ```

- **Grab-lift-reorder** — lift = `y: -LIFT_RISE` + `rotation: LIFT_TILT` (sign from index parity) + shadow on; as the carried item crosses the neighbor's midpoint, the **neighbor springs into the vacated slot** (a `fromTo` translate at `TRAVEL_AT + TRAVEL_DUR * 0.5`, `power3.out`); drop = rotation → 0, shadow off, settle. The neighbor's counter-move sells the reorder — without it the list reads as broken.
- **Component grab between surfaces** — a chip dragged mockup-to-mockup, swapping identity on drop (`tl.set` recolor + label swap at `DROP_AT`, tiny settle pop); the drop chrome is just the identity swap, no handles.

## Values

| token                       | range                                        | notes                                                                                                                          |
| --------------------------- | -------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------ |
| approach / press            | per cursor-click-ripple                      | approach 0.4–1.0 s; press-dip halves 0.06–0.12 s; cursor compresses more than the payload                                      |
| GHOST_OPACITY               | 0.5–0.75                                     | below 0.5 vanishes on busy documents; ~1.0 reads as the original moving — then hide `#source-chip` at the grab                 |
| GHOST_LIFT_SCALE / LIFT_DUR | 1.03–1.08 / 0.12–0.2 s                       | the shadow is the "off the surface" cue; the scale is garnish                                                                  |
| TRAVEL_DUR / TRAVEL_EASE    | 0.6–1.2 s / `power2.inOut`                   | a considered drag decelerates into the slot; `power1.inOut` for a calmer carry. `TRAVEL_AT ≥ GRAB_AT + 2×PRESS_DUR + LIFT_DUR` |
| DROP_AT / SNAP_DUR          | `TRAVEL_AT + TRAVEL_DUR` exactly / 0.2–0.3 s | a gap between arrival and snap reads as the drop failing                                                                       |
| RESIZE_SCALE / RESIZE_DUR   | by story (≈0.4–0.6) / 0.6–1.0 s              | `power2.inOut`                                                                                                                 |
| LIFT_RISE / LIFT_TILT       | 6–12 px / 2–4°                               | reorder pickup; index-derived tilt sign                                                                                        |

## Critical Constraints

- **Lockstep is the law** — matched tweens over straight lines (or one shared tween when deltas are identical); verify at the eased midpoint, not just the endpoints. Absolute endpoints on both partners.
- **The ghost is pre-rendered** — a DOM clone at the source position from t=0, `opacity: 0`, revealed by `tl.set`; placed field and chrome likewise. Never cloned at runtime, never conditionally rendered.
- **Grab has weight** — press dip + lift shadow before any travel; a chip departing without a press reads as telekinesis.
- **Drop is a state commit** — ghost off and placed field on at the same timeline position, `DROP_AT = TRAVEL_AT + TRAVEL_DUR`.
- **Resizes are uniform `scale`, origin at the anchor corner** — never width/height; one-axis stretch on stretch-safe boxes only.
- **Linear ease on the fill-handle travel** — the evenly-spaced `tl.set` reveals depend on it; an eased handle bunches them at the ends.
- **One verb per beat** — drag, then resize, then exit; overlapping a travel with a resize turns choreography into mush.
- **`pointer-events: none`** on cursor, ghost, and chrome.

## See also

`physics-press-reaction` (the grab's press dip) · `cursor-click-ripple` (a plain click before/after) · `spring-pop-entrance` (the placed field's snap-settle) · `waterfall-entry` (kinetic fill cascade) · `multi-phase-camera` (the zoom-breathing carrier shot golden drag demos ride) · `multi-cursor-choreography` (this verb inside an ensemble).


<!-- ===== FILE: hyperframes/hyperframes-animation/rules/depth-of-field-blur.md ===== -->

---
name: depth-of-field-blur
description: Selective-focus rack-focus — pull the eye to a focal element by GSAP-tweening filter blur (+ a small opacity dim) on the off-focus layers while the focal one stays sharp. Drive blur via a `--dof` CSS var; finite tweens, no CSS transition, deterministic. Covers single focal pull, rack-focus between two depth planes, and blur-the-cluster-while-pushing-in.
metadata:
  tags: blur, focus, depth-of-field, dof, rack-focus, filter, dim, spotlight, cinematic, push-in
---

# Depth-of-Field Blur (Selective Focus / Rack Focus)

Pulls the eye to one focal element by **blurring** (and slightly **dimming**) everything around it while the focal layer stays sharp — the camera's depth-of-field falling off the background, or a rack-focus shifting which plane is in focus. `filter` and `opacity` are paint-only, so both tween seek-safe. This is the backing rule for the focus-falloff beat the blueprints reach for: outer nodes blurring during a push-in (`constellation-hub`), rack-focus across a parallax card stack (`cursor-ui-demo`), non-highlighted cards dimming to spotlight a hero metric (`dataviz-countup`).

## How It Works

Every layer carries a `--dof` custom property (px of blur), read by `filter: blur(var(--dof))`, plus its own `opacity`. A GSAP tween advances each layer's `--dof` from `0` to its target blur and its opacity from `1` to a dim level over the focus-shift window. The focal layer's `--dof` stays `0`. Per-layer targets derive from `data-depth` / index, so the falloff is identical on every seek.

Three mechanics, same primitive:

1. **Focal pull** — one window: off-focus layers go sharp(0) → blurred while the focal layer holds at 0. The eye is pulled to the only thing still crisp.
2. **Rack focus** — two adjacent windows on the same property: plane A's blur ramps 0 → max at the same position plane B's ramps max → 0. State continuity matters exactly as in `press-release-spring`: A's resting blur after the rack must equal what B held before it — author both as tweens on the same `--dof` at the same position so the hand-off is seamless.
3. **Blur-the-cluster-while-pushing-in** — the DoF tween runs at the SAME timeline position as a camera push-in (`multi-phase-camera` / `coordinate-target-zoom`): "the world recedes" and "we push in" read as one move.

## Recipe

```html
<div class="world" id="world">
  <!-- Focal layer — stays sharp -->
  <div class="layer focal" id="focal">{FocalLabel}</div>
  <!-- Off-focus layers — blur + dim; data-depth orders near→far -->
  <div class="layer ctx" data-depth="1">{Context A}</div>
  <div class="layer ctx" data-depth="2">{Context B}</div>
  <div class="layer ctx" data-depth="3">{Context C}</div>
</div>
```

```css
.world {
  /* single wrapper so a concurrent camera push-in transforms everything
     together; DoF is independent of the camera */
  position: relative;
  width: 100%;
  height: 100%;
  transform-origin: 50% 50%;
}
.layer {
  --dof: 0px; /* px of blur; filter reads it — starts sharp */
  filter: blur(var(--dof));
  will-change: filter; /* promotes the layer so per-frame re-rasterization is cheap */
}
.focal {
  z-index: 2; /* sharp layer must sit ABOVE the blurred ones, or its crisp
     edges read as bleeding into the haze */
}
.ctx {
  z-index: 1;
}
```

```js
// Mechanic 1 — FOCAL PULL. Blur scales with data-depth so far planes blur
// more than near ones; the focal layer (--dof: 0, opacity: 1) is untouched.
gsap.utils.toArray(".ctx").forEach((el) => {
  const depth = Number(el.dataset.depth) || 1;
  tl.to(
    el,
    {
      "--dof": `${BLUR_PER_DEPTH * depth}px`,
      opacity: DIM_LEVEL, // dim, not gone
      duration: FOCUS_DUR,
      ease: "power2.inOut",
    },
    FOCUS_START,
  );
});
```

## Variations

- **Rack focus between two depth planes** — `gsap.set` plane B pre-blurred BEFORE the rack (no pop), then two tweens sharing `RACK_START` + `RACK_DUR`: A → `MAX_BLUR` + `DIM_LEVEL`, B → `0px` + `1`. Shared window makes them cross at the midpoint.
- **Blur the cluster while pushing in** — run the focal-pull tweens at the same position + duration as a camera tween on `#world` (`scale/x/y`, `power2.inOut`). Camera transforms the world; DoF tweens the layers — independent property channels, no conflict.
- **Spotlight a hero metric in a card grid** — `gsap.utils.toArray(".card:not(.hero)")` all defocus (`GRID_BLUR` + `DIM_LEVEL`) on one shared window; heroes are skipped.
- **Refocus / settle** — if the beat resolves back to "everything visible" (or hands off to a crossfade needing a clean outgoing frame), ramp all `--dof` back to `0px` / opacity 1 over the tail (`REFOCUS_START + REFOCUS_DUR ≤ DURATION`).
- **Bounded focus-breathing on the focal layer (optional)** — a finite `ease:"none"` driver writes `Math.max(0, Math.sin(p)) * FOCAL_BREATH_PX` into the focal `--dof` during a hold. Keep it ≤ ~0.6px or it reads as "still focusing"; default to omitting it.

## Values

| token                 | range                                  | notes                                                                                                    |
| --------------------- | -------------------------------------- | -------------------------------------------------------------------------------------------------------- |
| BLUR_PER_DEPTH        | 3–6 px per depth step                  | a 3-plane stack tops out ~9–18 px; low = gentle DoF, high = tilt-shift falloff                           |
| MAX_BLUR              | 8 soft → 16 default → 24 heavy px      | terminal blur for a fully-defocused plane; above ~24 px on a big surface, shrink/group the layer instead |
| GRID_BLUR             | 6–12 px                                | pushes cards back without losing the grid's shape                                                        |
| DIM_LEVEL             | 0.4 strong → 0.55 default → 0.7 subtle | rarely below 0.35 — fully dark reads as "removed," not "defocused"                                       |
| FOCUS_DUR             | 0.5–1.2 s                              | a rack/pull is a deliberate move, not a snap; shorter = snap focus, longer = languid                     |
| RACK_START / RACK_DUR | shared by both planes                  | `gsap.set` the pre-blurred plane BEFORE `RACK_START`                                                     |
| FOCAL_BREATH_PX       | ≤ 0.6 px, period 2–3 s                 | barely-there nicety                                                                                      |
| FOCAL vs CTX sizing   | context smaller / grouped              | small context layers let a modest radius still read as "out of focus" — and blur cheaply                 |

Tokens: dark `{bgGradient}` so the sharp focal layer reads as lit and forward; heavy display `{font}` weight — blurred copy needs it to stay shape-legible.

## Critical Constraints

- **Tween the `--dof` variable on the timeline** — reading `filter: blur(var(--dof))` keeps the blur on the HF seek clock.
- **Blur the SMALL / GROUPED layers, not the giant one.** Filter cost scales with radius × pixel area; a 20 px blur on a full-frame background is the worst case. Keep per-layer radius ≤ ~24 px on large surfaces and lean on the `opacity` **dim** to do the push-back work — dim + modest blur reads more like real DoF than blur cranked to the max.
- **`will-change: filter`** on every layer whose blur animates (drop it after settle if the layer also does heavy transform work).
- **Focal layer stays genuinely sharp** — `--dof: 0`, untouched (or breathing ≤ 0.6 px). Any visible blur on the focal element kills the "this is the thing" read.
- **State continuity on a rack** — the outgoing plane starts at the blur the incoming plane was holding, and vice-versa; adjacent tweens on the same `--dof` at the same position.
- **DoF is independent of the camera** — blur the layers, transform `.world` for the push-in; don't fake DoF with the camera transform or vice-versa.
- **Settle sharp before a hand-off** — refocus to `--dof: 0` in the tail if the next beat is a crossfade/push; handing off mid-defocus reads as "the render glitched."
- **Sharp focal layer above blurred layers** (`z-index`).

## See also

[multi-phase-camera.md](multi-phase-camera.md) (the push-in this rule's falloff accompanies) · [coordinate-target-zoom.md](coordinate-target-zoom.md) (zoom onto the focal core — the `constellation-hub` hook) · [viewport-change.md](viewport-change.md) (pan + rack across a tilted card plane) · [counting-dynamic-scale.md](counting-dynamic-scale.md) (hero metric counts up sharp — the `dataviz-countup` spotlight) · [3d-page-scroll.md](3d-page-scroll.md) (the parallax stack to rack between) · [sine-wave-loop.md](sine-wave-loop.md) (post-rack idle; keep both amplitudes tiny).


<!-- ===== FILE: hyperframes/hyperframes-animation/rules/depth-scatter-assemble.md ===== -->

---
name: depth-scatter-assemble
description: N elements scatter into / reassemble from a rotating 3D depth-cloud, each starting at a deterministic index-derived 3D offset and settling to a clean flat layout.
metadata:
  tags: 3d, scatter, assemble, depth, cloud, tumble, kinetic, letter, fragment, logo, reassemble
---

# Depth Scatter ↔ Assemble

N elements (glyphs, cards, logo fragments) fly in from a rotating 3D depth-cloud and lock into a flat layout — or the reverse. Each element has its OWN index-derived point in the cloud (translateZ depth + rotateX/Y tumble + x/y scatter). Distinct from `orbit-3d-entry` (flip-in then continuous orbit) and `center-outward-expansion` (flat burst from one shared center): here the resolve is a flat assembled layout.

## How It Works

Each element's flat target lives in `data-target-x/y`; its scattered state is pure trig on its index — golden-angle spread, stepped depth — so the cloud is byte-identical every render with no `Math.random`:

```js
const GOLDEN = Math.PI * (3 - Math.sqrt(5)); // ~2.39943 rad — even spread, no clumping
const a = i * GOLDEN;
const scatterX = Math.cos(a) * RADIUS;
const scatterY = Math.sin(a) * RADIUS;
const scatterZ = Z_NEAR - (i / (n - 1)) * (Z_NEAR - Z_FAR); // stepped depth
const rotX = Math.sin(a) * TUMBLE;
const rotY = Math.cos(a) * TUMBLE;
```

Elements are PARKED at their scatter points (`gsap.set`, opacity 0) before any tween, then each tweens to its flat target while the whole stage slowly rotates so the scatter has life before it locks. Requires `perspective` on the scene root and `preserve-3d` on the stage AND each element, or depth + tumble flatten to a 2D scale.

## Recipe

```html
<!-- inside a standard scene clip (hyperframes-core) -->
<div class="cloud-stage">
  <div class="frag" data-target-x="-260" data-target-y="0">{glyph1}</div>
  <div class="frag" data-target-x="-130" data-target-y="0">{glyph2}</div>
  <!-- … one .frag per glyph / fragment … -->
</div>
```

```css
.scene-root {
  display: grid;
  place-items: center;
  perspective: 1400px; /* REQUIRED */
}
.cloud-stage {
  position: relative;
  display: grid;
  place-items: center;
  transform-style: preserve-3d;
  will-change: transform;
}
.frag {
  position: absolute;
  top: 50%;
  left: 50%;
  transform-style: preserve-3d;
  backface-visibility: hidden; /* hides the mirrored face mid-tumble */
  will-change: transform, opacity;
}
```

```js
const frags = Array.from(document.querySelectorAll(".frag"));
const n = frags.length;
const GOLDEN = Math.PI * (3 - Math.sqrt(5));

// 1) Park every fragment in the cloud BEFORE any tween fires
const scatter = frags.map((el, i) => {
  const a = i * GOLDEN;
  const depthT = n > 1 ? i / (n - 1) : 0;
  return {
    x: Math.cos(a) * RADIUS,
    y: Math.sin(a) * RADIUS,
    z: Z_NEAR - depthT * (Z_NEAR - Z_FAR),
    rotationX: Math.sin(a) * TUMBLE,
    rotationY: Math.cos(a) * TUMBLE,
  };
});
frags.forEach((el, i) => gsap.set(el, { xPercent: -50, yPercent: -50, ...scatter[i], opacity: 0 }));

// 2) The cloud rotates so the scatter has life during assembly
tl.to(
  ".cloud-stage",
  { rotationY: CLOUD_SPIN_DEG, duration: CLOUD_SPIN_DUR, ease: "power1.out" },
  0,
);

// 3) ASSEMBLE — cloud point → flat target, index stagger = cloud collapsing inward
frags.forEach((el, i) => {
  tl.to(
    el,
    {
      x: Number(el.dataset.targetX),
      y: Number(el.dataset.targetY),
      z: 0,
      rotationX: 0,
      rotationY: 0,
      opacity: 1,
      duration: ASSEMBLE_DUR,
      ease: ASSEMBLE_EASE,
    },
    i * STAGGER,
  );
});
```

## Variations

- **Tumble-swap** (the beat-change hand-off): two glyph sets share the cloud; ONE shared 0→1 progress tween drives both in its `onUpdate` — outgoing lerps layout→cloud with `opacity: 1−p`, incoming lerps cloud→layout with `opacity: p`. Two separate tweens drift out of phase under seek and the cross stops reading as one hand-off. Inject per-glyph spans per phrase at setup (measure advance widths after `document.fonts.ready` — single-scene only).
- **Radial letter-explode → resolve**: flat-plane special case — `Z_NEAR = Z_FAR = 0`, small `TUMBLE`; reverse the assemble for the explode. Pure in-plane.
- **Scatter-OUT**: reverse assemble (layout → cloud, opacity 1→0) ONLY as the composition's final beat — mid-shot it reads as the shot ending.
- **Parallax lockup**: back layers get deeper `|Z_FAR|` + longer `ASSEMBLE_DUR`, foreground shallower/shorter — depth-speeded slide-in that locks into the logo.

## Values

| token                  | range                 | notes                                                                         |
| ---------------------- | --------------------- | ----------------------------------------------------------------------------- |
| n                      | 4–14 (fragments 4–9)  | above ~14 individual paths stop reading                                       |
| RADIUS                 | 250–700px             | keep the farthest scatter in frame or fragments pop in with no travel         |
| Z_NEAR / Z_FAR         | +150…+450 / −150…−500 | large `\|z\|` needs a wider `perspective` or fragments smear                  |
| TUMBLE                 | 40–110°               | past 90° glyphs show blank mid-tween (intended); cap ~80° for one-faced cards |
| ASSEMBLE_DUR           | 0.7–1.4s              |                                                                               |
| ASSEMBLE_EASE          | `power3.out` default  | `expo.out` snaps, `back.out(1.4)` seats with overshoot; never `in`            |
| STAGGER                | 0.03–0.09s            | `n × STAGGER < ASSEMBLE_DUR` — one collapsing motion, not a queue             |
| CLOUD_SPIN_DEG / \_DUR | 15–60° over ≥ dur     | gentle life; too fast competes with the assembly                              |
| SWAP_DUR               | 0.5–1.0s              | on the beat boundary; shorter = hard cross                                    |

## Critical Constraints

- **Every scattered value is index-derived** — `cos/sin(i × GOLDEN)` + stepped `z`. The golden angle spreads points evenly with no clumps and no `Math.random`.
- **`gsap.set` the cloud BEFORE adding tweens** — skipping it leaves frame 0 showing the assembled layout, then a teleport when the first tween starts.
- **`perspective` + `preserve-3d` on stage AND each fragment** — missing any one flattens the depth.
- **Resolve flat** — settled state is `z: 0`, rotations 0; a still-tilted resolve reads unfinished.
- **Tumble-swap: one shared progress for both glyph sets.**
- **Depth ordering is automatic** inside `preserve-3d` (paint order follows actual Z) — no manual z-index, unlike the orbit case's capped band.

## See also

`orbit-3d-entry` (settles into a continuous orbit instead) · `hacker-flip-3d` (glyphs decode on arrival) · `3d-text-depth-layers` (extrude the locked wordmark) · `center-outward-expansion` (flat 2D cousin) · `sine-wave-loop` (idle breathe on the resolved layout).


<!-- ===== FILE: hyperframes/hyperframes-animation/rules/discrete-text-sequence.md ===== -->

---
name: discrete-text-sequence
description: Replace entire text states at frame thresholds for non-linear typing effects — typos, bulk additions, pauses, backspaces, simulated thinking.
metadata:
  tags: text, typing, discrete, threshold, non-linear, sequence
---

# Discrete Text Sequence

Instead of character-by-character typewriter, replace entire string states at time thresholds — enabling non-linear effects (typos, backspaces, bulk paste, "thinking" gaps) that smooth per-char typing can't achieve. If your effect is "type each character, no edits", this rule is overkill — use the smooth-slice variation below.

## How It Works

The typing is authored as a sparse array of `{ t, text }` states; on every `onUpdate` a **reverse search** finds the latest entry whose `t` has passed and renders its text. Display jumps between states with no animation between them — the realism comes from the schedule shape: fast keystroke clusters (0.06–0.20s apart), pauses at word breaks (0.3–0.6s), a typo, backspaces peeling back to the fork, then a bulk paste replacing many chars in one entry. A block cursor blinks via a deterministic sin square wave on the same timeline.

## Recipe

```html
<!-- inside a standard scene clip (hyperframes-core) -->
<div class="terminal">
  <div class="prompt">$</div>
  <div class="text-wrap">
    <span class="text" id="text"></span><span class="cursor" id="cursor">_</span>
  </div>
</div>
```

```css
.terminal {
  font-family: {monoFont}; /* monospace required — proportional jitters even in a fixed box */
  display: flex;
  align-items: baseline;
  font-size: TERMINAL_FONT_SIZE;
}
.text-wrap {
  display: inline-flex;
  align-items: baseline;
  min-width: TEXT_WRAP_MIN_WIDTH; /* ≥ widest state — stops right-edge jitter */
  white-space: nowrap;
}
.cursor {
  display: inline-block; /* inline ignores width */
  width: CURSOR_WIDTH;
}
```

```js
// Each entry shows from its t until the NEXT entry's t.
// Shape: keystrokes → typo → backspace to the fork → bulk paste → completion mark.
const SEQUENCE = [
  { t: 0.0, text: "" },
  { t: T_K1, text: "{p1}" }, // first keystrokes (~3-5 chars, 0.1-0.2s apart)
  { t: T_K2, text: "{p1 + ' ' + p2_typo}" }, // continuation containing a typo
  { t: T_BS, text: "{p1 + ' ' + p2_partial}" }, // backspace(s) — peel back to the fork
  { t: T_BULK, text: "{fullCorrectedText}" }, // bulk paste — many chars in one jump
  { t: T_DONE, text: "{fullCorrectedText + ' ✓'}" }, // completion marker
];

// Reverse-search for the latest entry whose t has passed
function textAt(time) {
  for (let i = SEQUENCE.length - 1; i >= 0; i--) {
    if (time >= SEQUENCE[i].t) return SEQUENCE[i].text;
  }
  return "";
}

const textEl = document.getElementById("text");
const cursorEl = document.getElementById("cursor");

const driver = { t: 0 };
tl.to(
  driver,
  {
    t: TOTAL_DURATION,
    duration: TOTAL_DURATION,
    ease: "none",
    onUpdate: () => {
      textEl.textContent = textAt(driver.t);
    },
  },
  0,
);

// Cursor blink — deterministic sin square wave, never a CSS animation
const blink = { p: 0 };
tl.to(
  blink,
  {
    p: Math.PI * 2 * BLINK_CYCLES,
    duration: TOTAL_DURATION,
    ease: "none",
    onUpdate: () => {
      cursorEl.style.opacity = Math.sin(blink.p) > 0 ? "1" : "0";
    },
  },
  0,
);
```

## Variations

- **Smooth character slice** (continuous typewriter — no pauses, no edits): faster to author but uniformly "machine-typed", missing the human realism:

```js
const fullText = "{fullPhrase}";
const len = { v: 0 };
tl.to(
  len,
  {
    v: fullText.length,
    duration: TYPE_DUR,
    ease: "power1.inOut",
    onUpdate: () => {
      textEl.textContent = fullText.substring(0, Math.floor(len.v));
    },
  },
  0,
);
```

- **Thinking pause** — hold one state for `THINK_HOLD_DUR` (0.8–2.0s; under 0.5s reads as a stutter, not thought) simply by leaving a gap before the next entry's `t`.
- **State pulse on completion** — when the final state lands, `tl.to(".text", { scale: 1.03–1.08, duration: 0.15–0.3, yoyo: true, repeat: 1 }, T_DONE)`.
- **Per-state color shift** — in `onUpdate`, branch on `driver.t` vs the milestones: success color after `T_DONE`, dim mid-edit, normal while typing.

## Values

| token               | range                                        | notes                                                                  |
| ------------------- | -------------------------------------------- | ---------------------------------------------------------------------- |
| TERMINAL_FONT_SIZE  | 48–96px                                      | full-bleed comps; smaller for terminal-style detail                    |
| TEXT_WRAP_MIN_WIDTH | ≥ widest state                               | measure with a hidden probe after `document.fonts.ready` if unsure     |
| milestone `t`s      | keystrokes 0.06–0.20s apart; pauses 0.3–0.6s | monotonically increasing; `T_DONE ≤ TOTAL_DURATION − ~1s` climax dwell |
| TYPE_DUR (smooth)   | `chars × 0.06–0.12s`                         | fast → relaxed                                                         |
| BLINK_CYCLES        | one cycle per 0.5–0.8s                       | `TOTAL_DURATION / 0.8 ≤ BLINK_CYCLES ≤ TOTAL_DURATION / 0.5`           |
| CURSOR_WIDTH        | ~0.3× font size                              | gap to text single-digit px so the cursor feels attached               |

## Critical Constraints

- **Reverse-search the array each frame** — O(n) with small n (≤30 typical); don't index by frame, the sequence is sparse.
- **`min-width` on the text wrap is mandatory** — without it the right edge jitters as state length changes.
- **Discrete jumps must be INSTANT** — any transition on the text turns the jump into a smear and kills the "typing" feel.
- **Cursor blink is sin/sequence-driven on the timeline**, `display: inline-block`, monospace font, `white-space: nowrap` (wrapping mid-state breaks the illusion; trailing spaces must survive).
- **Discrete vs smooth** — use discrete only for non-linear states (typos, pauses, bulk paste); plain typing takes the smooth-slice variation.

## See also

`context-sensitive-cursor` (same SEQUENCE pattern + segment-colored cursor) · `3d-text-depth-layers` (discrete text with layered depth) · `counting-dynamic-scale` (discrete label beside a smooth counter) · `press-release-spring` (post-completion press beat).


<!-- ===== FILE: hyperframes/hyperframes-animation/rules/dynamic-content-sequencing.md ===== -->

---
name: dynamic-content-sequencing
description: Auto-calculate timeline start/end times from content length + per-item duration config — longer content gets more screen time without hardcoded numbers.
metadata:
  tags: timeline, sequencing, dynamic, duration, content-aware, utility
---

# Dynamic Content Sequencing

A utility pattern (not a motion rule in itself) for scenes that show a SEQUENCE of items (cards, phrases, stats): each item's duration is computed from its content length + per-item config, and the sequencer assigns absolute start/end times automatically — no hardcoded offsets per item. Distinct from [discrete-text-sequence](discrete-text-sequence.md) (one text element changing states) — this rule swaps between distinct content blocks.

## How It Works

A content array of `{ eyebrow, title, body, speedFactor, hold }` entries is reduced once at build time into a flat `TIMELINE` of `{ …entry, start, end }` — duration per entry is `BASE_DURATION + body.length × SEC_PER_CHAR + hold`, so longer text earns more reading time. A single linear driver's `onUpdate` reverse-searches the active entry and swaps the DOM **only on transitions** (a `lastTitle` guard — per-frame `textContent` writes flicker in render); an optional progress bar fills 0→100% across the whole run.

## Recipe

```html
<!-- inside a standard scene clip (hyperframes-core) -->
<div class="display">
  <div class="eyebrow" id="eyebrow"></div>
  <div class="title" id="title"></div>
  <div class="body" id="body"></div>
  <div class="progress-bar"><div class="progress-fill" id="progress-fill"></div></div>
</div>
```

```css
.body {
  min-height: 160px; /* reserve space — content height varies; without this, layout jumps */
}
.progress-fill {
  height: 100%;
  width: 0%;
}
```

```js
// N entries, each with its own pacing (optionally a speedFactor multiplier);
// the final entry uses a larger hold (closing beat).
const CONTENT = [
  { eyebrow: "{eyebrow1}", title: "{title1}", body: "{body1}", hold: HOLD_MID },
  // …
  { eyebrow: "{eyebrowN}", title: "{titleN}", body: "{bodyN}", hold: HOLD_FINAL },
];

// Pre-compute absolute start/end ONCE — never in onUpdate.
let cumulative = 0;
const TIMELINE = CONTENT.map((entry) => {
  const dur = BASE_DURATION + entry.body.length * SEC_PER_CHAR + entry.hold;
  const start = cumulative;
  cumulative += dur;
  return { ...entry, start, end: cumulative };
});

function entryAt(time) {
  for (let i = TIMELINE.length - 1; i >= 0; i--) {
    if (time >= TIMELINE[i].start) return TIMELINE[i];
  }
  return TIMELINE[0];
}

const eyebrowEl = document.getElementById("eyebrow");
const titleEl = document.getElementById("title");
const bodyEl = document.getElementById("body");
const progressEl = document.getElementById("progress-fill");

const TOTAL_DURATION = cumulative + TAIL_PAD;
const driver = { t: 0 };
let lastTitle = "";

tl.to(
  driver,
  {
    t: TOTAL_DURATION,
    duration: TOTAL_DURATION,
    ease: "none",
    onUpdate: () => {
      const entry = entryAt(driver.t);
      // Swap content only on transitions — no per-frame DOM thrash
      if (entry.title !== lastTitle) {
        eyebrowEl.textContent = entry.eyebrow;
        titleEl.textContent = entry.title;
        bodyEl.textContent = entry.body;
        lastTitle = entry.title;
      }
      progressEl.style.width = `${(driver.t / TOTAL_DURATION) * 100}%`;
    },
  },
  0,
);
```

## Variations

- **Crossfade between items** — return BOTH adjacent entries during an overlap window (`time ≥ e.start − overlap && time ≤ e.end + overlap`, overlap ≈ 0.3s) and render them with opacities computed from distance to the boundary.
- **Per-item motion variation** — map an `entry.style` key to an existing rule per chapter (e.g. `3d-text-depth-layers` → `hacker-flip-3d` → `counting-dynamic-scale`); the sequencer only orchestrates timing.
- **Auto-extend composition duration** — you can set `data-duration` from the computed `TOTAL_DURATION` in script, but HF reads `data-duration` at composition load and setting it after init may not take effect — author the duration manually from a rough total.

### Accelerating cadence (geometric hold decay)

For rhetorical escalation — "everyone says…", a roll-call, a praise flurry — the beat grid itself accelerates: early entries hold ~1s (read speed), then windows shrink geometrically into a ~0.15–0.3s flurry, braking on an emphasis state before the resolve. The acceleration is pre-computed into the same flat `TIMELINE` — still content-driven, still deterministic, no speed-up tween anywhere:

```js
// Geometric decay on the hold, clamped at a flurry floor; the brake state holds longest.
const HOLDS = CONTENT.map((entry, i) => Math.max(FLURRY_FLOOR, HOLD_START * Math.pow(DECAY, i)));
HOLDS[CONTENT.length - 1] = HOLD_FINAL;

let cumulative = 0;
const TIMELINE = CONTENT.map((entry, i) => {
  // Past ~0.5s states are glanced as motion texture, not read —
  // drop the per-char term or you never reach flurry speed.
  const readable = HOLDS[i] >= READ_THRESHOLD;
  const dur = HOLDS[i] + (readable ? entry.body.length * SEC_PER_CHAR : 0);
  const start = cumulative;
  cumulative += dur;
  return { ...entry, start, end: cumulative };
});
```

Worked example — **praise-chip flurry**: ~16 short quotes hard-cut through a chip beside a pinned wordmark. First 3 states at `HOLD_START = 1.0` (each reads fully); `DECAY = 0.8` shrinks every following window until `FLURRY_FLOOR = 0.2` catches it (≈12 states over ~2.5s — a churn of acclaim, individually glanced); the longest phrase takes `HOLD_FINAL ≈ 1.6` as the brake before the closing lockup.

Values: `HOLD_START` 0.8–1.2s; `DECAY` 0.75–0.88 (higher = longer runway before the flurry bites); `FLURRY_FLOOR` 0.15–0.3s (below ~0.15s swaps strobe); `READ_THRESHOLD` ~0.5s; brake ≥ 4× the floor or the stop doesn't register as a beat. The 3–6 entry guidance relaxes here — 12–18 states are legal precisely because flurry states aren't individually read. The hard-cut discipline (`lastTitle` guard, instant swaps) is what lets 0.2s states render clean.

## Values

| token         | range                 | notes                                                                                                                 |
| ------------- | --------------------- | --------------------------------------------------------------------------------------------------------------------- |
| BASE_DURATION | 0.6–1.5s              | minimum per entry regardless of length — even one-word entries get read time                                          |
| SEC_PER_CHAR  | 0.03–0.06 s/char      | ≈17–33 chars/sec; uniform across the sequence so the pace reads as one engine; lean high for wide-character languages |
| HOLD_MID      | 0.5–1.0s              | dwell on a non-final entry; `< HOLD_FINAL`                                                                            |
| HOLD_FINAL    | 1.0–2.0s              | climax dwell — must exceed HOLD_MID by a clear margin so the close reads as a beat                                    |
| SPEED_FACTOR  | 0.5–2.0 (default 1.0) | per-entry only; if every entry shares a factor, fold it into SEC_PER_CHAR                                             |
| TAIL_PAD      | 0.0–1.0s              | quiet beat after the last entry; prefer 0 when the next composition owns the breath                                   |
| CONTENT N     | 3–6 entries           | <3 isn't a sequence; >6 drags (accelerating cadence relaxes this — see above)                                         |

Reference: `../examples/messaging-multi-phrase.html`.

## Critical Constraints

- **Pre-compute the TIMELINE once at build** — never recompute in `onUpdate`; the reverse search over the flat array is the whole per-frame cost.
- **DOM swap only on entry transition** (`lastTitle`/key guard) — per-frame `textContent` assignment flickers in HF render.
- **`min-height` on the body element** — without reservation, downstream elements (progress bar, brand) jitter as content height varies.
- **Sequential only** — for parallel tracks use a different reduction.
- **Titles fit one line at the chosen size; bodies fit inside `min-height` after wrapping.**

## See also

`discrete-text-sequence` (per-entry typewriter on the body) · `context-sensitive-cursor` (cursor color per chapter) · `vertical-spring-ticker` (animated word swap instead of hard cut) · `scale-swap-transition` (visual morph between entries).


<!-- ===== FILE: hyperframes/hyperframes-animation/rules/gradient-text-sweep.md ===== -->

---
name: gradient-text-sweep
description: A gradient tweened THROUGH letterforms — background-clip:text + a backgroundPosition tween. Three forms: a continuous horizontal sweep inside a held headline, a traveling word-to-word highlight, and a hue-sweep that settles to a solid. Glyphs never move; finite, deterministic, seek-safe.
metadata:
  tags: gradient, text, sweep, background-clip, highlight, hue, typography, headline
---

# Gradient Text Sweep

Color that lives **inside the glyphs**: the headline's fill is an oversized gradient clipped into the letterforms (`background-clip: text`), and the motion is the gradient sliding **through** the type — the letters never move. Three forms: a **continuous sweep** across a held title card, a **word-to-word highlight** that lights a line left→right, and a **hue-sweep** that settles to a solid.

Boundaries: [asr-keyword-glow.md](asr-keyword-glow.md) is word-timed emphasis railed to ASR timestamps — this rule is a design beat with no audio rail. [ambient-glow-bloom.md](ambient-glow-bloom.md)'s traveling sweep is a sheen riding **over a surface**; here the gradient is masked **into the type** (its "Shimmer sweep" variation is this mechanism re-aimed as a working-state loop). [css-marker-patterns.md](css-marker-patterns.md) draws accents _around_ text, never fills.

## How It Works

The text carries a gradient background **wider than its own box** (`background-size: SWEEP_SPAN 100%`, e.g. `300% 100%`) clipped into the glyphs, so tweening `backgroundPosition` slides the gradient through the visible letterforms. Two gotchas own this rule:

- **`background-position` percentages only produce travel when `background-size` exceeds 100%** — at 100% the image is pinned and the tween is a silent no-op.
- **The percent axis runs opposite to the perceived travel** — tweening `"100% 50%"` → `"0% 50%"` moves the highlight left→right through the text.

1. **Continuous sweep (held title card)** — one long **linear** `backgroundPosition` tween spanning the hold. First and last color stops equal, so the travel has no visible seam and reads as endless while remaining a single finite tween.
2. **Word-to-word highlight** — each word is two pixel-identical stacked copies: a base copy in the resting color and a gradient-clipped copy at `opacity: 0`. A per-word opacity envelope (rise, then fall as the next word rises) passes the highlight along on an index-derived stagger — an **envelope, not a moving mask**: no per-word position measurement.
3. **Hue-sweep → solid** — the gradient holds position while a `filter: hue-rotate()` tween sweeps its hues; the settle is a stacked-copy crossfade to a solid twin — never a color-stop tween (gradients with different stops don't interpolate reliably).

## Recipe

```html
<!-- inside a standard scene clip (hyperframes-core) -->
<!-- Forms A/C: gradient headline; solid twin behind for the Form C settle -->
<div class="headline-stack">
  <h1 class="headline solid-twin">{headlineText}</h1>
  <h1 class="headline gradient-fill" id="headline">{headlineText}</h1>
</div>

<!-- Form B: per-word stacked copies -->
<p class="line">
  <span class="word"><span class="w-base">{word1}</span><span class="w-hot">{word1}</span></span>
  <span class="word"><span class="w-base">{word2}</span><span class="w-hot">{word2}</span></span>
</p>
```

```css
.headline-stack,
.word {
  display: grid; /* twins share one cell — pixel-identical boxes */
}
.headline,
.w-base,
.w-hot {
  grid-area: 1 / 1;
}
.gradient-fill,
.w-hot {
  background-image: {gradient}; /* {sweepGradient} A/C, {highlightGradient} B */
  background-size: SWEEP_SPAN 100%; /* MUST exceed 100% or the position tween is dead */
  background-position: 100% 50%; /* start; tween toward 0% for left→right travel */
  -webkit-background-clip: text;
  background-clip: text;
  color: transparent;
}
.solid-twin {
  color: {settleColor};
}
.w-base {
  color: {restColor};
}
.w-hot {
  opacity: 0; /* the envelope raises it as the highlight passes */
}
```

```js
// Form A: continuous sweep. 100% → 0% reads left→right (percent axis inverted);
// ease "none" — an eased sweep reads as an object, not light.
tl.fromTo(
  "#headline",
  { backgroundPosition: "100% 50%" },
  { backgroundPosition: "0% 50%", duration: SWEEP_DUR, ease: "none" },
  SWEEP_START,
);

// Form B: traveling highlight — per-word rise/fall envelopes, index stagger.
gsap.utils.toArray(".w-hot").forEach((el, i) => {
  const at = HIGHLIGHT_START + i * WORD_LAG;
  tl.fromTo(el, { opacity: 0 }, { opacity: 1, duration: HOT_RISE, ease: "power2.out" }, at);
  tl.to(el, { opacity: 0, duration: HOT_FALL, ease: "power2.in" }, at + WORD_LAG);
});

// Form C: hue-sweep, then crossfade to the solid twin (never tween color stops).
tl.fromTo(
  "#headline",
  { filter: "hue-rotate(0deg)" },
  { filter: `hue-rotate(${HUE_RANGE}deg)`, duration: HUE_DUR, ease: "power1.inOut" },
  HUE_START,
);
tl.to(
  "#headline",
  { opacity: 0, duration: SETTLE_SNAP_DUR, ease: "power2.in" },
  HUE_START + HUE_DUR,
);
```

## Variations

- **Title-card crawl** — Form A stretched across a long terminal hold (3–8s end card): seamless-ended gradient, `ease: "none"`, `SWEEP_DUR` = the whole hold. One tween, no loop.
- **One-pass sheen inside type** — gradient is the resting fill everywhere except one narrow highlight band (≤ ~25% of the span); one `backgroundPosition` pass carries the band through and the text returns to rest with no crossfade.
- **Karaoke settle** — Form B with the fall tweens skipped: the line lights cumulatively left→right and holds fully lit; settle color = the hot state, base copies start dimmer.
- **Gradient climax word** — one emphasized word (often ~-8° rotated) carries the gradient while the line stays solid; static gradient + a short Form C hue shift on landing, settling to the brand accent. Pairs with a `kinetic-beat-slam` arrival.

## Values

| token               | range                  | notes                                                                                |
| ------------------- | ---------------------- | ------------------------------------------------------------------------------------ |
| SWEEP_SPAN          | 200–400%               | must exceed 100%; wider = softer/slower feel, narrower = busier color per glyph      |
| SWEEP_DUR           | 1.2–3s                 | match the card's hold exactly; slower than ~4s stops registering as motion           |
| WORD_LAG            | 0.25–0.5s              | HOT_FALL starts exactly WORD_LAG after the rise so envelopes cross — a gap = a blink |
| HOT_RISE / HOT_FALL | 0.15–0.3s / 0.25–0.45s | fall slightly longer — the highlight "trails"                                        |
| HUE_RANGE / HUE_DUR | 40–180° / 0.8–1.6s     | past ~180° the palette dissociates from itself mid-sweep                             |
| SETTLE_SNAP_DUR     | 0.1–0.35s              | the goldens snap (~0.15s)                                                            |
| {settleColor}       | —                      | one of the gradient's own stops (or the brand ink) so the settle reads as resolution |

## Critical Constraints

- **`background-size` > 100%** on any element whose `backgroundPosition` is tweened — otherwise the tween is a silent no-op.
- **Percent axis is inverted** — left→right perceived travel is `100% → 0%`.
- **Both `-webkit-background-clip: text` AND `background-clip: text`, with `color: transparent`** — missing the prefix renders a solid gradient block over the text in the capture browser.
- **`ease: "none"` on position sweeps** — this is supposed to read as light, not an accelerating object.
- **Seamless ends for a crawl** — first and last stops equal, or the wrap point flashes a hard edge mid-hold.
- **Stacked copies pixel-identical** — same box, font, weight, tracking, one grid cell; any metric drift makes the crossfade a double-exposure.
- **`data-layout-allow-occlusion` on the twin** — pixel-identical stacked copies trip `hyperframes check`'s `text_occluded` gate by construction; the flag is the sanctioned waiver for this mechanism.
- **Settle by crossfade, never by tweening stops**; and the glyphs never move — if the type must travel, that's a separate rule on the wrapper.
- **No CSS `@keyframes` shimmer** — wall-clock animation desyncs from seek; every sweep is a timeline tween.

## See also

`kinetic-beat-slam` (slam lands the climax word, hue settle finishes it) · `spring-pop-entrance` (pop in solid, sweep after) · `discrete-text-sequence` (swap-slot under a riding crawl) · `ambient-glow-bloom` (surface-level sibling) · `css-marker-patterns` (strokes around text; fills here).


<!-- ===== FILE: hyperframes/hyperframes-animation/rules/gsap-effects.md ===== -->

# GSAP Effects for HyperFrames

Drop-in animation patterns. Snippets show mechanism only, inside a standard scene clip (hyperframes-core); assume `tl` exists.

- [Typewriter](#typewriter) — character-by-character reveal with optional cursor / backspace / word rotation
- [Audio Visualizer](#audio-visualizer) — pre-extract audio data, drive Canvas/DOM rendering from the timeline

## Typewriter

Requires GSAP's TextPlugin alongside the core script:

```html
<script src="https://cdn.jsdelivr.net/npm/gsap@3.14.2/dist/TextPlugin.min.js"></script>
<script>
  gsap.registerPlugin(TextPlugin);
</script>
```

### Basic

```js
const text = "Hello, world!";
const cps = 10; // chars per second — see timing table
tl.to(
  "#typed-text",
  { text: { value: text }, duration: text.length / cps, ease: "none" },
  startTime,
);
```

### Blinking Cursor

Three rules: **one cursor visible at a time** (hide previous before showing next); **cursor must blink when idle** (after typing, during holds); **no gap between text and cursor** (elements flush in HTML).

```html
<span id="typed-text"></span><span id="cursor" class="cursor-blink">|</span>
```

```css
@keyframes blink {
  0%,
  100% {
    opacity: 1;
  }
  50% {
    opacity: 0;
  }
}
.cursor-blink {
  animation: blink 0.8s step-end infinite;
}
.cursor-solid {
  animation: none;
  opacity: 1;
}
.cursor-hide {
  animation: none;
  opacity: 0;
}
```

Pattern: blink → solid (typing starts) → type → blink (typing done):

```js
tl.call(() => cursor.classList.replace("cursor-blink", "cursor-solid"), [], startTime);
tl.to("#typed-text", { text: { value: text }, duration: dur, ease: "none" }, startTime);
tl.call(() => cursor.classList.replace("cursor-solid", "cursor-blink"), [], startTime + dur);
```

Multi-line handoff: hide previous cursor → blink new → brief pause (~0.5s) → solid when typing. Never go `hidden → solid` (skips the idle blink).

### Backspacing

TextPlugin removes from the front — wrong for backspace. Use manual substring removal:

```js
function backspace(tl, selector, word, startTime, cps) {
  const el = document.querySelector(selector);
  const interval = 1 / cps;
  for (let i = word.length - 1; i >= 0; i--) {
    tl.call(
      () => (el.textContent = word.slice(0, i)),
      [],
      startTime + (word.length - i) * interval,
    );
  }
  return word.length * interval;
}
```

### Spacing With Static Text

A typewriter word next to static text (`<span>Ship something</span><span style="margin-left:14px"><span id="word"></span><span id="cursor">|</span></span>` in a baseline-aligned flex row): use `margin-left` on the wrapper span. Don't use flex `gap` (it spaces the cursor from the text) and don't put a trailing space in the static text (it collapses when the dynamic span is empty).

### Word Rotation

Type → hold → backspace → next word; cursor blinks during every idle moment:

```js
let offset = 0;
words.forEach((word, i) => {
  const typeDur = word.length / 10;
  // cursor: solid while typing, blink during holds (same call pattern as above)
  tl.to("#typed-text", { text: { value: word }, duration: typeDur, ease: "none" }, offset);
  offset += typeDur + 1.5; // hold
  if (i < words.length - 1) offset += backspace(tl, "#typed-text", word, offset, 20) + 0.3;
});
```

### Appending Words

Build a sentence word-by-word into the same element: keep an `accumulated` string, each step tweens `text: { value: accumulated + " " + word }` with `duration: newChars / cps`, then advances the offset.

### Timing Guide

| CPS   | Feel             | Good for                   |
| ----- | ---------------- | -------------------------- |
| 3-5   | Slow, deliberate | Dramatic reveals, suspense |
| 8-12  | Natural typing   | Dialogue, narration        |
| 15-20 | Fast, energetic  | Tech demos, code           |
| 30+   | Near-instant     | Filling long blocks        |

## Audio Visualizer

Pre-extract audio data, drive Canvas / DOM rendering from the timeline. **Do not use the Web Audio API at render time** — there's no playback during seek.

### Extract Audio Data

Bundled extractor (requires `ffmpeg` + Python `numpy`):

```bash
python skills/hyperframes-creative/scripts/extract-audio-data.py audio.mp3 -o audio-data.json
python skills/hyperframes-creative/scripts/extract-audio-data.py video.mp4 --fps 30 --bands 16 -o audio-data.json
```

Output: `{ "fps": 30, "totalFrames": 5415, "frames": [{ "time": 0.0, "rms": 0.42, "bands": [0.8, 0.6, 0.3] }] }` — `rms` (0-1) is overall loudness; `bands[]` (0-1) are frequency magnitudes, index 0 = bass, each band normalized independently.

### Loading (Synchronously)

Inline the JSON for small files (< ~500 KB), or sync XHR for large ones:

```js
const xhr = new XMLHttpRequest();
xhr.open("GET", "audio-data.json", false); // synchronous — deliberate
xhr.send();
const AUDIO_DATA = JSON.parse(xhr.responseText);
```

**Do NOT use async `fetch()`** — HyperFrames reads `window.__timelines` synchronously after page load; building the timeline inside `.then()` means it isn't ready when capture starts.

### Driving the Timeline

Canvas 2D is the workhorse (bars, waveforms, circles, gradients) — one `tl.call` per frame:

```js
const ctx = document.getElementById("viz").getContext("2d");
for (let f = 0; f < AUDIO_DATA.totalFrames; f++) {
  tl.call(
    () => {
      const frame = AUDIO_DATA.frames[f];
      ctx.clearRect(0, 0, canvas.width, canvas.height);
      // draw using frame.rms and frame.bands
    },
    [],
    f / AUDIO_DATA.fps,
  );
}
```

WebGL / Three.js: HyperFrames patches `THREE.Clock` for deterministic time — update uniforms from audio data each frame. DOM elements: fine under ~20 elements, slower than Canvas beyond that.

### Smoothing

```js
let prev = null;
const smoothing = 0.25; // 0.1-0.2 snappy, 0.3-0.5 flowing
function smooth(f) {
  const raw = AUDIO_DATA.frames[f];
  if (!prev) prev = { rms: raw.rms, bands: [...raw.bands] };
  else {
    prev = {
      rms: prev.rms * smoothing + raw.rms * (1 - smoothing),
      bands: raw.bands.map((b, i) => prev.bands[i] * smoothing + b * (1 - smoothing)),
    };
  }
  return prev;
}
```

### Design Guide

- **Spatial mapping** — horizontal: bass left, treble right; vertical: bass bottom; circular: bass at 12 o'clock, wrap clockwise (mirror for a full circle).
- **Bass drives big moves** (scale, glow, position); **treble drives detail** (shimmer, flicker, edges); **RMS drives globals** (background brightness, overall energy).
- Pick 2-3 animated properties — more looks noisy. Keep minimums above zero so quiet sections still have life.
- **Band count**: 4 = background glow/pulse, 8 = bar charts, 16 = detailed EQ (default), 32 = dense radial layouts.
- **Layering**: stack canvases with `z-index` — a background layer driven by bass/rms under a foreground layer driven by individual bands gives depth without per-element complexity.


<!-- ===== FILE: hyperframes/hyperframes-animation/rules/hacker-flip-3d.md ===== -->

---
name: hacker-flip-3d
description: Character-level 3D rotation with random glyph substitution for a decryption reveal effect.
metadata:
  tags: text, 3d, reveal, decode, hacker, randomization, perspective
---

# Hacker Flip 3D Reveal

Characters flip down from 90° in 3D while cycling through pseudo-random glyphs, then settle on the target character — a "decryption" / airport flap-display reveal. Resolves to a short target word (typically a brand or label).

## How It Works

Each character gets its own per-char tween from `rotateX: 90deg` (hidden, hinged at the bottom edge) to `0deg` (upright), staggered across the word. Below `REVEAL_THRESHOLD` progress the char displays a seeded pseudo-random glyph that reshuffles every few frames; past it, the real target character clicks into place — so the eye catches the right letter just as the flip settles. A hidden ghost copy of the full word reserves layout width so narrow flicker glyphs never shift the line.

## Recipe

```html
<!-- inside a standard scene clip (hyperframes-core) -->
<div class="hacker-text-wrap" id="hacker-text" data-target="{phrase}">
  <!-- ghost row + per-char spans injected by the setup script -->
</div>
```

```css
/* the scene root (or nearest 3D ancestor) MUST set perspective: 1500px */
.hacker-text-wrap {
  font-family: {monoFont}; /* monospace so flicker glyphs hold width */
  font-weight: 900;
  font-size: HACKER_FONT_SIZE;
  position: relative; /* ghost stacks absolutely behind the live row */
}
.hacker-char {
  display: inline-block;
  transform-origin: bottom; /* flap-display hinge */
  transform-style: preserve-3d;
}
.hacker-ghost {
  opacity: 0;
  pointer-events: none;
  position: absolute;
  inset: 0 auto auto 0;
}
```

```js
const wrap = document.getElementById("hacker-text");
const targetWord = wrap.dataset.target;
const GLYPHS = "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!@#$%&*";

// Ghost row (reserves width) + live per-char spans
const ghost = document.createElement("div");
ghost.className = "hacker-ghost";
ghost.textContent = targetWord;
wrap.appendChild(ghost);
const charEls = [...targetWord].map((ch) => {
  const span = document.createElement("span");
  span.className = "hacker-char";
  span.textContent = ch === " " ? " " : ch;
  span.dataset.target = ch;
  wrap.appendChild(span);
  return span;
});

// Index-seeded hash — same frame always yields the same glyph
function pseudoGlyph(seed) {
  const h = ((seed * 9301 + 49297) % 233280) / 233280;
  return GLYPHS[Math.floor(h * GLYPHS.length)];
}

charEls.forEach((el, i) => {
  const state = { p: 0 };
  tl.to(
    state,
    {
      p: 1,
      duration: FLIP_DURATION,
      ease: "power3.out",
      onUpdate: () => {
        if (state.p < REVEAL_THRESHOLD) {
          el.textContent = pseudoGlyph(i * 1000 + Math.floor(state.p * 100));
        } else {
          el.textContent = el.dataset.target === " " ? " " : el.dataset.target;
        }
        el.style.transform = `rotateX(${90 - state.p * 90}deg)`;
        el.style.opacity = Math.min(1, state.p * 2);
      },
    },
    i * CHAR_STAGGER,
  );
});
```

## Variations

- **Top-down hinge** — `transform-origin: top` for a falling-flap look.
- **Center spin** — `transform-origin: center` reads as a barrel roll, not a flap.
- **Number-only pool** — restrict `GLYPHS` to digits for a price / countdown decode.
- **Two-pass decode** — chain two `FLIP_DURATION` tweens with different glyph pools (symbols → letters → real) for a longer reveal.

## Values

| token            | range                           | notes                                                                              |
| ---------------- | ------------------------------- | ---------------------------------------------------------------------------------- |
| HACKER_FONT_SIZE | 6–10% of viewport min-dimension | the flip IS the focal beat; ghost must use the identical size                      |
| FLIP_DURATION    | 0.4–1.0s                        | under 0.4s the flicker phase has no time; over 1.0s drags                          |
| CHAR_STAGGER     | 0.03–0.08s                      | total decode = `CHAR_STAGGER × (chars − 1) + FLIP_DURATION` — fit the phase budget |
| REVEAL_THRESHOLD | 0.5–0.7                         | lower reveals too early (no tension); higher reads as a hard end-reveal            |
| FLICKER_RATE     | 3–6 frames per glyph swap       | <3 looks like noise; >6 looks like discrete typing                                 |

Reference: `../examples/proof-logo-chain.html` (163px, 0.55s, 0.033s, 0.6).

## Critical Constraints

- **`perspective` on the scene root REQUIRED** — without parent perspective, `rotateX` renders as a 2D squash, not a 3D flip; `transform-style: preserve-3d` on each char.
- **Ghost placeholder** with identical content + font must back the live chars — without it, narrow glyphs shift the layout mid-flicker (monospace preferred; the ghost makes a proportional face recoverable).
- **Flicker seed = char index + quantized progress** — the same frame must show the same glyph.
- **Flicker rate ≥ ~3 frames per swap**; `onUpdate` work stays O(1) per char per frame.
- **Center the flip dead-center and add NO decorative chrome** (timestamp lines, "// AUTH" tags, status dots) — the flip is the beat. A necessary secondary label is BIG typography (56–72px caps + tracking) in the same stack, never a tiny corner annotation.

## See also

`card-morph-anchor` (flip reveals a phrase, card morphs into the next shot) · `counting-dynamic-scale` (the numeric counterpart).


<!-- ===== FILE: hyperframes/hyperframes-animation/rules/kinetic-beat-slam.md ===== -->

---
name: kinetic-beat-slam
description: Percussive kinetic typography — short phrases slam in on a steady beat with distinct per-phrase entrances, optional rhythm chrome (metronome ticks, beat bar), then a locked finale.
metadata:
  tags: text, kinetic, typography, beat, rhythm, slam, percussive, punchy
---

# Kinetic Beat Slam

Short phrases hit one at a time on a **steady beat**, each with a _different_ entrance, then stack into a locked finale — the recipe for "punchy / rhythmic" text-forward pieces (taglines, manifestos, hype intros). The difference between generic and rhythmic is (1) one shared **onset array** driving every element, (2) **distinct** entrances per phrase rather than one reused helper, and (3) optional **rhythm chrome** that visibly keeps the beat.

## How It Works

A single tempo grid — `PULSE` seconds per sub-beat, `BEATS = [t0, t1, t2, …]` on that grid — is the rhythmic spine; every phrase entrance, accent, and chrome tick reads its time from it, so the piece locks to one pulse instead of drifting hand-tuned offsets. Each phrase gets a different transform axis (scale+blur slam / side snap / rise+rotate) with short attacks (0.35–0.6s on the hit), then the stack holds with a finite low-amplitude breath.

## Recipe

```html
<!-- inside a standard scene clip (hyperframes-core) -->
<div class="kbs-stage">
  <div class="kbs-line" id="p1"><span class="verb">Notice</span> more.</div>
  <div class="kbs-line" id="p2"><span class="verb">Decide</span> faster.</div>
  <div class="kbs-line" id="p3"><span class="verb">Act</span> now.</div>
</div>
<!-- optional rhythm chrome -->
<div class="kbs-metronome" aria-hidden="true"><i></i><i></i><i></i><i></i><i></i></div>
```

```css
.kbs-stage {
  position: absolute;
  inset: 0;
  display: flex;
  flex-direction: column;
  justify-content: center;
  padding: 120px 160px; /* title-safe margin */
}
.kbs-line {
  font-family: "Archivo Black", "League Gothic", sans-serif; /* embedded display face */
  font-size: 150px;
  line-height: 0.96;
  letter-spacing: -0.03em;
  color: #f5f5f5;
}
.kbs-line .verb {
  color: #ff5b2e; /* exactly one accent hue */
}
.kbs-metronome {
  position: absolute;
  bottom: 64px;
  left: 50%;
  transform: translateX(-50%);
  display: flex;
  gap: 14px;
}
.kbs-metronome i {
  width: 6px;
  height: 28px;
  background: #ff5b2e;
  opacity: 0.25;
}
```

```js
// ONE tempo grid drives everything — phrases AND the metronome read it.
const PULSE = 0.4; // seconds per sub-beat
const BEATS = [PULSE * 1, PULSE * 5, PULSE * 9]; // phrase onsets, on the grid

// Distinct entrances per phrase (NOT one reused helper).
tl.fromTo(
  "#p1",
  { scale: 1.5, filter: "blur(16px)", opacity: 0 },
  { scale: 1, filter: "blur(0px)", opacity: 1, duration: 0.5, ease: "power4.out" },
  BEATS[0],
);
tl.fromTo(
  "#p2",
  { x: -320, opacity: 0 },
  { x: 0, opacity: 1, duration: 0.45, ease: "expo.out" },
  BEATS[1],
);
tl.fromTo(
  "#p3",
  { y: 90, rotation: 6, opacity: 0 },
  { y: 0, rotation: 0, opacity: 1, duration: 0.55, ease: "circ.out" },
  BEATS[2],
);

// Rhythm chrome: each tick flashes on the SAME grid, not a magic offset.
gsap.utils.toArray(".kbs-metronome i").forEach((tick, i) => {
  tl.to(tick, { opacity: 1, duration: 0.08, yoyo: true, repeat: 1, ease: "none" }, PULSE * (i + 1));
});

// Finale hold: floor (not ceil) so the repeat never overshoots data-duration;
// max(0,…) so a short hold never yields a negative repeat (GSAP reads negative as -1 = infinite).
const holdStart = BEATS[2] + 0.7,
  cycle = 1.6,
  holdDur = SCENE_DURATION - holdStart;
tl.to(
  ".kbs-stage",
  {
    scale: 1.01,
    duration: cycle / 2,
    ease: "sine.inOut",
    yoyo: true,
    repeat: Math.max(0, Math.floor(holdDur / cycle) - 1),
  },
  holdStart,
);
```

## Variations

- **Entrance easing by attack character** — `power4.out` hard slam ⭐ default hit · `expo.out` hardest snap (side-snaps, whip-ins) · `back.out(2)` overshoot pop (accents only, not body words) · `circ.out` heavy rise with momentum. Use **at least 3 distinct easings** across the piece.
- **Rhythm chrome alternatives** — a center beat bar or a `// label` monospace tag pulsing on-beat instead of the 5-tick metronome; mark any decorative that must survive a shader transition per `../transitions/overview.md`.
- **Finale dressing** — stack + accent underline sweep ([css-marker-patterns](css-marker-patterns.md)); don't just leave the last phrase sitting.

## Values

| token             | range                | notes                                                                                        |
| ----------------- | -------------------- | -------------------------------------------------------------------------------------------- |
| BEATS spacing     | 1.2–1.8s             | <0.8s frantic, >2.5s loses the pulse; keep spacing even — it's a beat                        |
| entrance duration | 0.35–0.6s            | the hit must resolve before the next beat; exits ≤0.25s                                      |
| accent hue        | exactly 1            | the verbs; the rest mono white / near-black                                                  |
| display face      | 150px+, heavy weight | Archivo Black / League Gothic / Oswald — see `hyperframes-creative/references/typography.md` |

## Critical Constraints

- **One beat array, not scattered offsets** — every element times off `BEATS[]` / `PULSE`; this is the single biggest lever for "rhythmic".
- **Different entrance per phrase** — a reused `punchIn()` for all lines is the flat-but-competent tell. Vary the motion axis, reuse the ease _family_.
- **Finale repeat math**: `repeat: Math.max(0, Math.floor(dur / cycle) - 1)` — `Math.ceil` overshoots `data-duration` and trips the `gsap_repeat_ceil_overshoot` lint rule; a negative repeat is read by GSAP as `-1` (infinite).
- **No banned exit animations between scenes** — in a montage the _transition_ is the exit (`../transitions/overview.md`); only a final scene may fade out.
- **Display font must be embedded** or it silently falls back at render — Anton / Bebas-as-literal are NOT embedded (`Bebas Neue` aliases to League Gothic; verify in `typography.md`).

## See also

`3d-text-depth-layers` (extruded depth on the slammed words) · `css-marker-patterns` (finale underline/circle) · `sine-wave-loop` (the finale breath) · `../adapters/gsap-easing-and-stagger.md` (easing vocabulary).


<!-- ===== FILE: hyperframes/hyperframes-animation/rules/motion-blur-streak.md ===== -->

---
name: motion-blur-streak
description: Fake directional velocity blur on a fast entrance or camera push-through — blur peaks at max speed and resolves to 0 at the settle, so the element streaks in then snaps sharp. Two paths — SVG feGaussianBlur on the motion axis, or an echo/ghost trail that collapses into the lead. Plus a per-frame-driven form for an element riding a baked track (tracked insert, shake-matched title): velocity-gated text-free silhouette ghosts (or a rotate/blur/counter-rotate filter sandwich when a true blur is the look), streak axis from the track delta.
metadata:
  tags: motion-blur, velocity, streak, entrance, fly-in, ghost, echo, svg-filter, kinetic, camera, snap, driven, tracked, baked-track
---

# Motion-Blur Streak

Real motion blur isn't available to a seeked renderer (it integrates over shutter time), so this rule **fakes** it for a fast fly-in or hard camera push-through. The whole point is the _coupling_: the blur envelope rides the **same ease and window** as the position tween, so peak blur lands exactly on peak speed and the element is razor-sharp the instant it stops. Two paths:

- **(A) Directional SVG blur** — inline `<feGaussianBlur stdDeviation="X 0">` (X on the motion axis, 0 across it), tweened via a proxy. Cleanest; a true directional smear.
- **(B) Echo / ghost trail** — 2–4 duplicates at decreasing opacity, offset backward along the motion vector, collapsing into the lead as it settles. No filter cost; a stylized "speed-line" trail.

Both paths assume a **tween window** — an element driven per frame from a baked track has none; that form is the Per-Frame-Driven Carve-In below.

**Entrances and mid-shot moves only — never a mid-composition exit.** A blurred element fleeing off-frame mid-composition reads as a glitch; a hard exit between scenes is the transition's job (`../transitions/overview.md`). Two sanctioned scope extensions: the envelope may ride the **camera wrapper** during a travel leg (Camera-Travel Carve-Out), or become a per-frame function of a baked track for a **driven element** (Per-Frame-Driven Carve-In).

## How It Works

A fast `out`-eased move front-loads velocity — fastest off the start, bleeding to zero at the settle. Map the blur/echo envelope onto that same curve: position travels from an off-frame / pushed-back start to rest over `MOVE_DUR`; in lockstep on the same window and ease the smear goes `PEAK_BLUR → 0` (A) or the ghosts collapse onto the lead (B). By the settle the element is fully crisp and dwells ≥1 s — the contrast between violent streak and still, sharp settle IS the effect. GSAP can't tween an SVG attribute directly: tween a plain `{ v }` proxy and write `setAttribute("stdDeviation", …)` in `onUpdate`, seeding it once at setup so a seek to t=0 shows the streaked start.

## Recipe

```html
<!-- inside a standard scene clip; overflow: hidden on the scene (the smear extends past rest) -->
<svg width="0" height="0" aria-hidden="true" style="position: absolute">
  <filter id="streak" x="-50%" y="-50%" width="200%" height="200%">
    <feGaussianBlur id="streak-blur" in="SourceGraphic" stdDeviation="0 0" />
  </filter>
</svg>
<div class="streak-el" id="streak-el" style="filter: url(#streak)">{phrase}</div>
<!-- Path B instead: N-1 aria-hidden .streak-ghost duplicates BEHIND the lead, no filter -->
```

```js
// Path A — proxy-tweened directional blur.
const blurNode = document.getElementById("streak-blur");
const blurProxy = { v: PEAK_BLUR };
const writeBlur = () => blurNode.setAttribute("stdDeviation", `${blurProxy.v} 0`); // X axis only
writeBlur(); // seed frame 0 — a seek to t=0 must show the streaked start, not a sharp pre-frame

tl.fromTo(
  "#streak-el",
  { x: ENTER_FROM_X, opacity: 0 },
  { x: 0, opacity: 1, duration: MOVE_DUR, ease: MOVE_EASE },
  MOVE_START,
);
tl.to(blurProxy, { v: 0, duration: MOVE_DUR, ease: MOVE_EASE, onUpdate: writeBlur }, MOVE_START);

// Path B — ghosts on the SAME window/ease; per-ghost variation by index.
gsap.utils.toArray(".streak-ghost").forEach((g) => {
  const i = Number(g.dataset.i); // 1..N-1, set in HTML
  tl.fromTo(
    g,
    { x: ENTER_FROM_X - i * ECHO_STEP_PX, opacity: GHOST_BASE_OPACITY / i },
    { x: 0, opacity: 0, duration: MOVE_DUR, ease: MOVE_EASE },
    MOVE_START,
  );
});
```

## Variations

- **Vertical streak** — swap axes: `y`, `stdDeviation="0 Y"`, vertical echo offsets.
- **Camera push-through** — `scale: SCALE_FROM → 1` with a symmetric `"B B"` envelope (depth-wise smear, not directional): the wordmark punches out of soft focus and snaps crisp at the lock.
- **Staggered grid streak-in** — each card streaks into its slot at `MOVE_START + i * CARD_STAGGER` with its own blur proxy / ghosts; sharp the instant it lands.
- **Hold-the-streak** — blur on a marginally slower curve than position (position `expo.out`, blur `power3.out`) so the last wisp resolves just after arrival. Sparingly; default is locked envelopes.

## Camera-Travel Carve-Out

The envelope is also sanctioned at **wrapper level**: on the `.world` / camera wrapper of a virtual-camera scene ([viewport-change.md](viewport-change.md), [multi-phase-camera.md](multi-phase-camera.md), [3d-camera-flight.md](3d-camera-flight.md)) during a **travel leg** — a dive, a whip sweep, a violent final push. This does **not** violate "never a mid-composition exit": the world never leaves frame — the camera travels _through_ it, and every leg ends with the world at rest, sharp, inside the frame. Each leg is an **arrival** at the next pose, so the entrance doctrine applies leg by leg. Three deltas from the element-level recipe:

- **Envelope follows the leg's ease.** An `out` leg (dive, final push) uses the base recipe unchanged. An `inOut` repositioning leg peaks mid-leg: split the envelope at the velocity peak — `0 → PEAK` on the in-half ease over the first half, `PEAK → 0` on the out-half over the second. Seed the proxy at **0** for these (the streaked state lives mid-leg, not at t=0; seed-at-`PEAK_BLUR` belongs to the entrance shape, where the first frame IS the fastest).
- **Filter placement.** 2D camera: `filter: url(#streak)` on the `.world` wrapper. 3D flight: on the **perspective stage** above the 3D context — a `filter` on a `preserve-3d` element flattens it and collapses every `translateZ`. Never per-element inside the world: one frame-wide envelope, not N desynced ones.
- **Full-frame blur is heavy** — cap `PEAK_BLUR` ~18–20 at wrapper level (vs 30 for one element); a brief whip may touch ~24. Axis rule as usual: `"X 0"` for a lateral whip/pan, `"B B"` for a dive/push.

### Whip sweep (named composition)

The heavily-blurred lateral whip that resolves into the next region — two rules on one window:

1. **Position** — [nudge-curve.md](nudge-curve.md)'s three-phase chain on the camera state, tuned burst-dominant (tail still ≥3× ramp-in in time).
2. **Blur** — `0 → PEAK` across the ramp-in, held at `PEAK` through the linear burst (constant velocity = constant smear), `PEAK → 0` across the tail.

Swap or reveal the next region's content DURING the burst — the smear masks the change; the `power4.out` tail lands it sharp. Reveal during the burst, read after the tail.

```js
tl.to(cam, { x: WHIP_X * 0.1, duration: 0.12, ease: "power3.in", onUpdate: applyCamera }, WHIP_AT);
tl.to(
  cam,
  { x: WHIP_X * 0.75, duration: 0.1, ease: "none", onUpdate: applyCamera },
  WHIP_AT + 0.12,
);
tl.to(
  cam,
  { x: WHIP_X, duration: 0.35, ease: "power4.out", onUpdate: applyCamera },
  WHIP_AT + 0.22,
);

tl.to(blurProxy, { v: PEAK_BLUR, duration: 0.12, ease: "power3.in", onUpdate: writeBlur }, WHIP_AT);
// blur holds at PEAK through the linear burst (no tween needed — value rests at PEAK)
tl.to(blurProxy, { v: 0, duration: 0.35, ease: "power4.out", onUpdate: writeBlur }, WHIP_AT + 0.22);
```

## Per-Frame-Driven Carve-In (baked tracks)

When the element is not tweened but **driven** — a tracked insert or callout riding a baked per-frame track, a title matched to camera shake — there is no move window to share. The envelope becomes a per-frame function of the track's own delta, computed in the same `onUpdate` that applies the position.

One element per transform, so no write clobbers another:

```html
<!-- .track: position + any fade, the only element either touches -->
<div class="track">
  <!-- ×2, the lead's box -->
  <div class="streak-ghost" aria-hidden="true" data-layout-allow-overlap></div>
  <!-- Path A only: rotate onto the travel axis; same box as .lead so both rotate about one center -->
  <div class="blur-wrap" style="filter: url(#streak)">
    <!-- counter-rotate only; no GSAP transform tweens on it -->
    <div class="lead">…</div>
  </div>
</div>
```

```js
// inside the frame-lookup driver (an ease:"none" proxy → frames[i]); TRACK.x / TRACK.y are baked arrays
const j = Math.max(1, i); // frame 0 borrows the frame-1 delta so a seek to t=0 has a defined state
const dx = TRACK.x[j] - TRACK.x[j - 1];
const dy = TRACK.y[j] - TRACK.y[j - 1];
const speed = Math.hypot(dx, dy); // px per frame
const angle = (Math.atan2(dy, dx) * 180) / Math.PI; // the streak axis IS the travel direction
track.style.transform = `translate(${TRACK.x[i]}px, ${TRACK.y[i]}px)`;

// Path B, driven form (the default here): text-free silhouette clones trail the lead along −delta.
const base = speed > TRAIL_GATE ? Math.min(TRAIL_MAX, TRAIL_K * speed) : 0;
ghost1.style.transform = `translate(${-dx * 0.25}px, ${-dy * 0.25}px)`;
ghost2.style.transform = `translate(${-dx * 0.5}px, ${-dy * 0.5}px)`;
ghost1.style.opacity = String(base); // a fade on .track multiplies in; never read another tween's value
ghost2.style.opacity = String(base * 0.5);

// Path A, driven form: rotate a filter wrapper onto the travel axis, blur along X only, counter-rotate the content.
const sigma = speed > TRAIL_GATE ? Math.min(SIGMA_MAX, 0.5 * speed) : 0;
blurWrap.style.transform = `rotate(${angle}deg)`;
lead.style.transform = `rotate(${-angle}deg)`;
blurNode.setAttribute("stdDeviation", `${sigma} 0`);
```

Three deltas from the tweened recipe:

- **Ghosts are text-free silhouettes** — the lead's box, border, radius and fill with **no content** (`aria-hidden="true"`, `data-layout-allow-overlap`). A 25–50%-opacity clone reads as shape; a clone carrying the text reads as a duplicate element, and content-free clones give the layout and contrast checkers nothing to flag.
- **Velocity-gated, not window-shaped** — the trail exists only above `TRAIL_GATE` px/frame and scales with speed (`min(TRAIL_MAX, TRAIL_K × speed)`): a slow drift shows nothing, a whip shows a 180°-shutter smear. Fade `.track`, never `.lead`: group opacity takes the trail with it, and the ghost opacity stays a pure function of the frame index whatever order frames are seeked in.
- **Axis from the baked delta** — `atan2(dy, dx)` per frame; the streak follows the track around corners with nothing to seed at setup.

**Which path for a driven subtree.** Path B is the default: it costs no filter raster (a full filter region re-rasterizes every frame under per-frame drive), its clones carry no text so the layout and contrast checkers see nothing new, and it degrades to nothing when the track is still. Path A in the driven form is legitimate when a true blur is the look. Both forms measured deterministic on the reference host (2026-09-08: single-card 120-frame and three-card 450-frame drives of each path, hardware-GL and software lanes, every double render bit-identical) — but a per-frame-driven filter is the first thing to re-measure on a new host: keep the double-render frame-hash comparison (`--format png-sequence` twice) in the pipeline rather than trusting one clean run. One earlier build (2026-08) observed 1-LSB `feGaussianBlur` jitter under per-frame load and shipped Path B for that reason.

## Values

| token               | range                                              | notes                                                                                           |
| ------------------- | -------------------------------------------------- | ----------------------------------------------------------------------------------------------- |
| MOVE_EASE           | `expo.out` / `power4.out` (default) / `power3.out` | `out`-family ONLY — `in`/`inOut` puts peak speed in the wrong place; position and blur share it |
| MOVE_DUR            | 0.25–0.6s                                          | over ~0.7s reads as a focus pull, not velocity                                                  |
| ENTER_FROM_X/Y      | 40–120% of the element's own dimension             | enough runway for the streak to read                                                            |
| PEAK_BLUR           | 8–30 (default 18)                                  | >30 erases the glyph at the start; ~18–20 cap at wrapper level                                  |
| SCALE_FROM          | 1.3–2.5                                            | push-through variation                                                                          |
| N (ghosts)          | 2–4                                                | >4 reads as strobe, not streak                                                                  |
| ECHO_STEP_PX        | 12–40px                                            | `N × step ≲ ENTER_FROM` so the furthest ghost starts inside the runway                          |
| GHOST_BASE_OPACITY  | 0.3–0.6                                            | opaque ghosts read as duplicate elements                                                        |
| CARD_STAGGER        | 0.05–0.12s                                         | one assembling wave, not separate arrivals                                                      |
| TRAIL_GATE          | 3–6 px/frame (default 4)                           | driven form: below it the track counts as still — no trail, no blur                             |
| TRAIL_K · TRAIL_MAX | 0.05 · 0.32                                        | driven form: ghost opacity `min(TRAIL_MAX, TRAIL_K × speed)` — hits the cap at ~6 px/frame      |
| TRAIL_OFFSETS       | 0.25 / 0.5 of the per-frame delta                  | two clones = a discrete 180° shutter; a third at 0.75 only for a long whip                      |
| SIGMA_MAX           | 8–12                                               | driven Path A: `σ = min(SIGMA_MAX, 0.5 × speed)` along the travel axis                          |

## Critical Constraints

- Blur peaks at peak speed and resolves to 0 at the settle — share the ease and window between position and envelope. A blur that lingers after the stop reads as a focus pull.
- Entrances / mid-shot arrivals only — never a mid-composition exit; wrapper-level use only per the Camera-Travel Carve-Out, per-frame-driven use only per the Per-Frame-Driven Carve-In.
- Seed `stdDeviation` at setup: at `PEAK_BLUR` for the entrance shape, at 0 for a whip / `inOut` leg.
- Generous filter region (`x="-50%" y="-50%" width="200%" height="200%"`) or the smear clips at the element's box edge.
- Directional axis: `"X 0"` horizontal, `"0 Y"` vertical, `"B B"` only for a depth/scale move — symmetric blur on a sideways move looks like defocus.
- Dwell ≥1 s sharp after the snap; a streak landing at the last beat reads as "flashed and gone".
- Heavy element on a solid field — thin type (< ~120px / 800 weight) or a busy backdrop swallows the smear.
- `overflow: hidden` on the scene — the smear / furthest ghost extends past the resting position during travel.
- Driven form: clones are text-free silhouettes (`aria-hidden`, `data-layout-allow-overlap`) inside the faded `.track`, axis from the baked delta; nothing is seeded at setup except the structural frame-0 state.

## See also

`kinetic-beat-slam` (streak as one beat's entrance) · `center-outward-expansion` (grid streak-in) · `scale-swap-transition` (same-footprint morph — not an arrival) · `nudge-curve` (the whip sweep's position half) · `3d-camera-flight` / `viewport-change` (the Camera-Travel Carve-Out's wrappers).


<!-- ===== FILE: hyperframes/hyperframes-animation/rules/multi-cursor-choreography.md ===== -->

---
name: multi-cursor-choreography
description: N labeled independent cursor actors work one canvas simultaneously (collaborative-canvas ambience) — per-cursor deterministic waypoint schedules, name-tag pills in distinct colors, grab/drop actions on an interleaved beat grid so paths and actions never collide; the camera stays locked, the liveness itself is the message.
metadata:
  tags: cursor, multi-cursor, collaboration, ensemble, canvas, name-tag, choreography, ambient, teamwork
---

# Multi-Cursor Choreography

> **The camera never chases anyone.** No real camera — any "pan" is the canvas group translating inside a static frame. And per the motion doctrine's idle-motion ban, every cursor must **perform**: travel to a target, act, then rest still. Scheduled rest is stillness; aimless wander loops are wobble.

THE ensemble primitive: **two to four labeled cursor actors** — each an arrow plus a name-tag pill in its own color — work one shared canvas at the same time. No single interaction is the subject; the **simultaneous liveness is** ("a team is in here, working"), usually as ambience under a headline building over the top. Distinct from [cursor-click-ripple.md](cursor-click-ripple.md) and [cursor-drag.md](cursor-drag.md): those are **one protagonist** the viewer follows click-by-click; here the actors are chorus, not lead — each action smaller and quieter than a solo cursor's, the value in the interleaving. Also distinct from [camera-cursor-tracking.md](camera-cursor-tracking.md): that locks the _viewport_ to one focal cursor; this rule forbids exactly that — the frame is static and the eye roams freely.

## How It Works

Everything hangs off one data table:

1. **The actor table** — a literal `ACTORS` array: per actor a name, a color, and a **waypoint schedule** (`{ x, y, at, dur }` legs plus action beats). All coordinates and times are hand-authored constants — the choreography is data: deterministic, seekable, and auditable for collisions before a single frame renders.
2. **Legs as explicit `fromTo`s** — each leg tweens the actor wrapper from the previous waypoint to the next at an absolute position. Gaps between legs are **rests**: the cursor sits still exactly where it landed.
3. **Actions** — a leg can end in a grab (press dip; the payload rides the next leg in lockstep — [cursor-drag.md](cursor-drag.md) mechanics at chorus intensity), a drop (`tl.set` identity swap + tiny settle pop), or a hover (a highlight fades in under the tip, once, then holds).
4. **The interleaved beat grid** — actions land on **alternating beats** (~1.2 / 2.6 / 4.0 s): at any moment at most one action lands while the others glide or rest. Each actor owns a home **zone** of the canvas; only one actor at a time leaves its zone, so paths never cross near-simultaneously. (Short specimens under ~5s can compress beat spacing to ~0.3–0.9s — zones still prevent collisions; the ≥1s spacing is for ambience-length shots.)
5. **Ambience staging** — cursors may already be mid-canvas at t=0 (the team was working before we arrived — the collaborative-canvas idiom), or enter off-frame on staggered starts. The canvas group may slowly translate-pan under the ensemble (element translate, not a camera).

## Recipe

```html
<!-- Canvas group (mockups + payload chips) may translate for an ambient pan.
     One wrapper per actor: arrow + name tag move as ONE object. -->
<div class="canvas-group" id="canvas-group">
  <div class="mockup" id="mockup-a">{mockupA}</div>
  <div class="canvas-chip" id="chip-1">{chipLabel}</div>
</div>
<div class="actor" id="actor-1">
  <svg class="actor-arrow"><!-- arrow path, fill: ACTOR_1_COLOR --></svg>
  <span class="actor-tag" style="background: ACTOR_1_COLOR">{actorName1}</span>
</div>
```

```js
// The choreography IS this table — all literals; read the `at` columns to
// verify beats interleave. Each actor owns a zone.
const ACTORS = [
  {
    id: "#actor-1", // zone: left mockup
    legs: [
      { from: { x: 180, y: 420 }, to: { x: 320, y: 300 }, at: 0.2, dur: 0.9 },
      { to: { x: 340, y: 480 }, at: 2.0, dur: 0.8 }, // rest 0.9s between legs
    ],
  },
  {
    id: "#actor-2", // zone: center mockup
    legs: [
      { from: { x: 900, y: 200 }, to: { x: 820, y: 360 }, at: 0.6, dur: 1.0 },
      { to: { x: 980, y: 380 }, at: 3.4, dur: 0.7 },
    ],
  },
  {
    id: "#actor-3", // zone: right panel — enters from off-frame
    legs: [{ from: { x: 1980, y: 520 }, to: { x: 1560, y: 460 }, at: 1.4, dur: 1.1 }],
  },
];

ACTORS.forEach((actor) => {
  let prev = actor.legs[0].from;
  tl.set(actor.id, { x: prev.x, y: prev.y }, 0); // on stage (or off) from t=0
  actor.legs.forEach((leg) => {
    tl.fromTo(
      actor.id,
      { x: prev.x, y: prev.y },
      { x: leg.to.x, y: leg.to.y, duration: leg.dur, ease: "power2.inOut", immediateRender: false },
      leg.at,
    );
    prev = leg.to;
  });
});

// Actions at chorus intensity — actor 1 grabs the chip: press dip, then the
// chip rides leg 2 in lockstep (matched tween: same position, duration, ease).
tl.to("#actor-1", { scale: 0.88, duration: 0.07, ease: "power2.in", yoyo: true, repeat: 1 }, 1.1);
tl.fromTo(
  "#chip-1",
  { x: 0, y: 0 },
  { x: CHIP_DX, y: CHIP_DY, duration: 0.8, ease: "power2.inOut", immediateRender: false },
  2.0, // = actor-1 leg 2 `at` and `dur`, exactly
);
// Drop: identity swap + tiny settle — quieter than a solo cursor's snap
tl.set("#chip-1", { backgroundColor: "{chipSwapColor}" }, 2.8);
tl.fromTo(
  "#chip-1",
  { scale: 1.06 },
  { scale: 1, duration: 0.2, ease: "power3.out", immediateRender: false },
  2.8,
);

// Optional ambient canvas pan (element translate, NOT a camera)
tl.fromTo("#canvas-group", { x: 0 }, { x: PAN_DX, duration: 6.0, ease: "none" }, 0.3);
```

## Variations

- **Ambient collaborative canvas (the Hook register)** — the default: actors mid-canvas at t=0, canvas slowly panning, a headline building over the top ([waterfall-entry.md](waterfall-entry.md)). The demo is set-dressing for the words; keep every action small and the beat grid loose.
- **One labeled editor (N = 1, still ensemble-styled)** — a single labeled teammate cursor performs one visible edit (deletes and retypes a headline word via [discrete-text-sequence.md](discrete-text-sequence.md), or drops one component). The name tag is the point: _a person_ did this.
- **Featured beat inside the ensemble** — one actor briefly becomes the lead: full [cursor-drag.md](cursor-drag.md) grab-carry-drop with chrome while the others explicitly REST for that window. Freeze the chorus; two things moving with intent at once splits the eye.
- **Staggered entrances** — cursors enter from off-frame at `ENTER_AT + i * ENTER_STAGGER`, each gliding to its zone ("the team assembles"); entry vectors from different edges, per the house cursor entry law.

## Values

| token               | range                     | notes                                                                                                                        |
| ------------------- | ------------------------- | ---------------------------------------------------------------------------------------------------------------------------- |
| ACTOR_COUNT         | 2–4                       | one is a solo rule's job; five+ reads as noise — no viewer tracks five pointers                                              |
| leg `dur`           | 0.6–1.2 s, `power2.inOut` | human, considered mouse movement; sub-0.5 s across long distances reads as a teleport                                        |
| rest gaps           | 0.5–1.5 s                 | rests make the ensemble read as people; zero-rest actors read as screensavers                                                |
| action beat spacing | ≥ 1.0 s                   | while one acts, others may glide but must not act — audit by sorting all `at` values                                         |
| zones               | one per actor             | only the acting actor crosses zones; two cursors within ~80 px reads as a glitch — check waypoint pairs at overlapping times |
| PAN_DX              | ~40–80 px, linear         | parallax life, not a camera move; omit for busier ensembles                                                                  |
| tag / arrow size    | smaller than a solo lead  | the oversized-cursor treatment is for protagonists; tags must stay legible at render resolution                              |
| colors              | one saturated hue each    | from the palette's accent range; tag pill and arrow fill share the hue                                                       |

## Critical Constraints

- **The table is the choreography** — all waypoints, times, and actions are literal data. If you can't verify non-collision by reading the `at` columns, the schedule is too clever.
- **Every leg is an explicit `fromTo`** with the previous waypoint as the from-state, `immediateRender: false` on all but each actor's initial placement — chained `.to()`s on shared properties capture stale starts under seek.
- **Interleave, never chord** — at most one action landing at any moment; simultaneous travel is fine (that's the liveness), simultaneous _payoffs_ compete.
- **Chorus intensity** — every action is a quieter version of its solo rule: smaller dips, subtler snaps, no ripple bursts; save full treatment for a featured beat.
- **Rest is stillness** — between legs a cursor holds exactly where it landed: no idle drift, no yoyo wander on any actor.
- **Payload lockstep** — a carried chip's tween matches its actor's leg exactly (position, duration, ease), per the cursor-drag law.
- **The wrapper moves, never the parts** — arrow + name tag are one element; tweening them separately shears the actor apart under seek.
- **Camera locked** — no viewport zoom/pan tweens; the only large-scale motion is the linear canvas-group translate. Never zoom to an actor (that's a solo-cursor shot).
- **Actors are people** — human-speed glides, pauses, one thing at a time; `pointer-events: none` on all actors. Check `tl.duration()` — ensembles accumulate long tails from late rests.

## See also

`cursor-drag` (full-treatment featured beat) · `cursor-click-ripple` (chorus click — press only, skip the ripple) · `discrete-text-sequence` (a labeled actor's retype edit) · `viewport-change` (the canvas-group translate math) · `spring-pop-entrance` (components popping in as drop results).


<!-- ===== FILE: hyperframes/hyperframes-animation/rules/multi-phase-camera.md ===== -->

---
name: multi-phase-camera
description: Sequential camera zoom with 2-3 distinct phases (pull-back / focus / push) plus continuous micro-drift for organic cinematic feel.
metadata:
  tags: camera, zoom, phase, drift, scale, cinematic
---

# Multi-Phase Camera

A camera wrapper around the ENTIRE scene that progresses through discrete zoom phases at scripted triggers, with continuous sine-driven micro-drift overlaid so the camera never feels static between phases. Distinct from a single linear zoom — multi-phase creates cinematic pacing (anticipation → reveal → settle).

## How It Works

The camera is one wrapping `<div>` whose `transform: scale() translate(x, y)` is composed from two channels inside a single `onUpdate` writer:

1. **Phase scale** — a proxy object `{ scale }` stepped through phases at trigger times (`PHASE_1_SCALE` at t=0 → `PHASE_2_SCALE` at `PHASE_2_AT` → `PHASE_3_SCALE` at `PHASE_3_AT`).
2. **Drift offset** — a continuous sine-based `translateX` / `translateY` (small amplitude, slow frequency) ADDED to the phase transform. X and Y run at slightly different frequencies (`DRIFT_FREQ_RATIO ≈ 1.3`) — equal frequencies produce a perfect diagonal that reads mechanical; ~1.3 gives an organic Lissajous.

## Recipe

```html
<div class="camera" id="camera">
  <div class="content">
    <div class="hero">{Brand}</div>
    <div class="tagline">{tagline}</div>
    <div class="cta">{ctaText}</div>
  </div>
</div>
```

```css
.scene {
  overflow: hidden; /* REQUIRED — any phase scale < 1 exposes the content's edges */
  background: {sceneBgColor}; /* background on .scene, NOT .camera — a camera-borne
     background warps/translates with the transform and reveals the outer void */
}
.camera {
  position: absolute;
  inset: 0;
  display: grid;
  place-items: center;
  transform-origin: 50% 50%; /* off-center origin creates phase-to-phase drift */
  will-change: transform;
}
```

```js
const camera = document.getElementById("camera");

// Three-phase scale plan: pullback → focus → push.
const phase = { scale: PHASE_1_SCALE }; // Phase 1 is the initial value — no tween

// Phase 2 — settle to neutral focus
tl.to(phase, { scale: PHASE_2_SCALE, duration: PHASE_2_DUR, ease: PHASE_2_EASE }, PHASE_2_AT);

// Phase 3 — slow push-in for the climax
tl.to(phase, { scale: PHASE_3_SCALE, duration: PHASE_3_DUR, ease: PHASE_3_EASE }, PHASE_3_AT);

// Drift driver — continuous sine motion overlaid on the phase scale.
// The ONE writer of camera.style.transform.
const drift = { p: 0 };
tl.to(
  drift,
  {
    p: Math.PI * 2 * DRIFT_CYCLES,
    duration: TOTAL_DURATION, // spans the whole composition
    ease: "none",
    onUpdate: () => {
      const dx = Math.sin(drift.p) * DRIFT_AMP_X;
      const dy = Math.sin(drift.p * DRIFT_FREQ_RATIO) * DRIFT_AMP_Y;
      camera.style.transform = `scale(${phase.scale}) translate(${dx}px, ${dy}px)`;
    },
  },
  0,
);

// Content reveals happen INSIDE the camera frame (hero/tagline/cta beats).
```

## Phase Patterns

| Pattern             | Scale sequence (1 → 2 → 3)        | Feel                            | When to use                   |
| ------------------- | --------------------------------- | ------------------------------- | ----------------------------- |
| **Focus-in**        | back → neutral → slight push      | Approach → settle → slight push | Default product reveal        |
| **Dramatic reveal** | push → neutral → pull             | Wide → focus → settle back      | Hero shot with breathing room |
| **Steady push**     | neutral → slight push → more push | Gradual forward momentum        | Continuous narrative push     |
| **Bookend pull**    | neutral → strong push → neutral   | Settle → push → release         | CTA emphasis then release     |

## Variations

- **Phase trigger by content beat**: align a camera tween's start with a content tween's end (entry completes → push begins) rather than a fixed clock value.
- **Camera shake (panic / impact)**: a brief higher-amplitude, higher-frequency drift tween over a short window — same `drift` mechanism with `SHAKE_AMP` / `SHAKE_CYCLES` / `SHAKE_DUR` at `SHAKE_AT`.
- **Targeted zoom into an off-center element**: combine scale with counter-translation so the target lands at viewport center — divide the measured offset by the current scale before feeding it into the writer:

```js
const tRect = document.querySelector(".cta").getBoundingClientRect();
const offsetX = (STAGE_W / 2 - (tRect.left + tRect.width / 2)) / phase.scale;
const offsetY = (STAGE_H / 2 - (tRect.top + tRect.height / 2)) / phase.scale;
// then in onUpdate: translate(offsetX + dx, offsetY + dy)
```

(Full counter-translate doctrine: [coordinate-target-zoom.md](coordinate-target-zoom.md).)

## Values

| token                       | range                                    | notes                                                                               |
| --------------------------- | ---------------------------------------- | ----------------------------------------------------------------------------------- |
| PHASE_1 / 2 / 3_SCALE       | 0.88–0.96 / 0.98–1.02 / 1.04–1.15        | tighter spread = subtler camera; scale < 1 REQUIRES `overflow: hidden` on `.scene`  |
| PHASE_2_AT / PHASE_2_DUR    | 0.3–1.0s / 1.0–1.8s                      | longer DUR = slower settle, more cinematic                                          |
| PHASE_3_AT / PHASE_3_DUR    | 2.0–4.0s / 1.0–2.0s                      | PHASE_3_AT ≥ PHASE_2_AT + PHASE_2_DUR or focus is preempted                         |
| PHASE_2_EASE / PHASE_3_EASE | `power2.out` `power3.out` `power2.inOut` | spring/back easing on a camera feels uncomfortable; each later phase settles deeper |
| TOTAL_DURATION              | = `data-duration`                        | the drift tween must span the whole composition                                     |
| DRIFT_CYCLES                | 1–3                                      | 1 = one slow breath; high values read as mechanical wobble                          |
| DRIFT_AMP_X / DRIFT_AMP_Y   | 2–8 px / 1–4 px                          | imperceptible per-frame, visible over time — if it reads as a shake, it's too much  |
| DRIFT_FREQ_RATIO            | 1.2–1.5                                  | 1.0 = perfect diagonal (mechanical); ~1.3 = organic Lissajous                       |
| HERO_AT (etc.)              | after Phase-2 settle lands               | a hero fading in mid-pull-back feels like it's flying away                          |

## Critical Constraints

- **Camera wraps EVERYTHING in the scene** — a per-element camera creates parallax bugs and breaks the "one viewpoint" read.
- **One writer**: phase scale and drift compose inside the single drift `onUpdate`; nothing else touches `camera.style.transform`.
- **`overflow: hidden` on `.scene`** — required whenever any phase scale < 1.
- **`transform-origin: 50% 50%` on `.camera`** — off-center origin creates unpredictable phase-to-phase drift.
- **Scene background on `.scene`, not `.camera`** — otherwise scaling/translating reveals the outer void.
- **Hero reveal starts AFTER the initial pull-back ease lands** — otherwise the headline feels like it's flying away.

## See also

[coordinate-target-zoom.md](coordinate-target-zoom.md) (counter-translate math for the targeted variation) · [orbit-3d-entry.md](orbit-3d-entry.md) (orbit inside a drifting camera) · [counting-dynamic-scale.md](counting-dynamic-scale.md) (climax push synced to counter peak) · [3d-text-depth-layers.md](3d-text-depth-layers.md) (depth-stacked hero under camera moves) · [sine-wave-loop.md](sine-wave-loop.md) (element idle inside the camera).


<!-- ===== FILE: hyperframes/hyperframes-animation/rules/nudge-curve.md ===== -->

---
name: nudge-curve
description: Slow-fast-slow three-phase group slide — reposition a composed group (word rows, card stacks, lists) to reveal content or make room. No single built-in ease produces it; chain power3.in ramp → linear burst → power4.out tail (10/65/25 distance, tail ≥3× ramp-in in time).
metadata:
  tags: slide, reposition, group-motion, easing, nudge, slow-fast-slow, reveal, layout
---

# Nudge Curve

Slow-fast-slow repositioning of a composed group (word rows, card stacks, lists) to
reveal content or make room. **In-scene group slide — not a seam.** No single built-in
ease produces it — `power4.inOut` smacks to a stop. Chain three tweens on one property:

| Phase     | Ease            | Distance | Time | Feel                                     |
| --------- | --------------- | -------- | ---- | ---------------------------------------- |
| 1 ramp-in | `power3.in`     | ~10%     | ~20% | barely moves — motion registers, no jolt |
| 2 burst   | `none` (linear) | ~65%     | ~18% | ~2× average px/frame — purposeful        |
| 3 tail    | `power4.out`    | ~25%     | ~62% | decaying creep to rest — kills the smack |

## Rules

- The tail is ≥3× the ramp-in in TIME. If it still smacks: extend the tail's time (not
  distance) or use `power5.out`.
- Phase 2 stays linear — easing it loses the burst contrast.
- Reveal new content DURING phase 2 — the burst masks its appearance.
- Same ratios vertical; scale distances proportionally, keep the time ratios.
- A cascade arrival usually precedes this slide — see [waterfall-entry.md](waterfall-entry.md).

## JS

Reference values for a 270px leftward slide (0.57s total). Scale distances
proportionally for other travels; preserve the TIME ratios; tail ≥3× ramp-in.

```js
var t = /* start after content settles */;
tl.to(".text-row", { x: -30,  duration: 0.12, ease: "power3.in"  }, t);          // ramp-in: 11% dist / 21% time
tl.to(".text-row", { x: -210, duration: 0.10, ease: "none"       }, t + 0.12);   // burst:   67% dist / 18% time
tl.to(".text-row", { x: -270, duration: 0.35, ease: "power4.out" }, t + 0.22);   // tail:    22% dist / 61% time
// vertical: same ratios on y. 150px variant: -15 / -115 / -150 at the same times.
```

## Anti-patterns

| Don't                                                    | Instead                                  |
| -------------------------------------------------------- | ---------------------------------------- |
| Single ease for a group slide (`power4.inOut`, `slow()`) | The three-phase chain above              |
| Nudge tail shorter than 3× the ramp-in                   | Extend the tail's TIME, not its distance |


<!-- ===== FILE: hyperframes/hyperframes-animation/rules/orbit-3d-entry.md ===== -->

---
name: orbit-3d-entry
description: Elements flip in from 3D space then settle into continuous elliptical orbit around a focal point.
metadata:
  tags: orbit, 3d, flip, ellipse, circular, icon, entry, continuous
---

# Orbit with 3D Entry

Elements flip in from 3D space (`rotateX` + `rotateY` + negative `z`) then settle into a continuous elliptical orbit around a center label. Distinct from one-shot reveals — the orbit keeps running, driven by a 0→1 progress tween INSIDE the timeline (never rAF).

## How It Works

Per element, two phases: (1) a `back.out` flip from a hidden 3D orientation to flat — **in place at its orbital starting position** (see Critical Constraints); (2) a continuous orbit where `onUpdate` computes `x/y` from `cos/sin(initialAngle + p·2π)` on the ellipse. The stage needs `perspective` on the scene root and `preserve-3d` on stage + items, or the flip flattens to a 2D scale.

## Recipe

```html
<!-- inside a standard scene clip (hyperframes-core) -->
<div class="orbit-stage">
  <div class="orbit-item" data-angle="0">{glyph1}</div>
  <div class="orbit-item" data-angle="60">{glyph2}</div>
  <!-- … evenly-spaced angles … -->
  <div class="orbit-center">{centerLabel}</div>
</div>
```

```css
.scene-root {
  display: grid;
  place-items: center;
  perspective: 1800px; /* REQUIRED */
}
.orbit-stage {
  position: relative;
  display: grid;
  place-items: center;
  transform-style: preserve-3d;
}
.orbit-item {
  position: absolute;
  top: 50%;
  left: 50%;
  transform-style: preserve-3d;
  will-change: transform;
}
.orbit-center {
  position: relative;
  transform: translateZ(220px); /* wins paint order inside preserve-3d */
  z-index: 9999;
}
```

```js
const items = document.querySelectorAll(".orbit-item");
const RADIUS_Y = RADIUS_X * Y_TO_X_RATIO; // perspective-flattened ellipse

items.forEach((el, i) => {
  const a0 = (Number(el.dataset.angle) / 360) * Math.PI * 2;
  const startX = Math.cos(a0) * RADIUS_X;
  const startY = Math.sin(a0) * RADIUS_Y;

  // 1) Park at the orbital position, hidden — BEFORE any tween fires
  gsap.set(el, {
    xPercent: -50,
    yPercent: -50,
    x: startX,
    y: startY,
    rotateX: ROTATE_X_FROM,
    rotateY: ROTATE_Y_FROM,
    z: Z_FROM,
    opacity: 0,
    scale: SCALE_FROM,
  });

  // 2) Flip in IN PLACE — rotation/opacity/scale only, never translate
  tl.to(
    el,
    {
      rotateX: 0,
      rotateY: 0,
      z: 0,
      opacity: 1,
      scale: 1,
      duration: ENTRY_DUR,
      ease: `back.out(${FLIP_BACK})`,
    },
    i * STAGGER,
  );

  // 3) Continuous orbit — each item gets its OWN progress tween (own initialAngle)
  const orbit = { p: 0 };
  tl.to(
    orbit,
    {
      p: 1,
      duration: ORBIT_DURATION,
      ease: "none",
      onUpdate: () => {
        const a = a0 + orbit.p * Math.PI * 2;
        const x = Math.cos(a) * RADIUS_X;
        const y = Math.sin(a) * RADIUS_Y;
        // capped z-index band [1, 50] — see center-label clearance below
        el.style.zIndex = String(1 + Math.round(((y + RADIUS_Y) / (2 * RADIUS_Y)) * 49));
        el.style.transform = `translate(-50%, -50%) translate(${x}px, ${y}px)`;
      },
    },
    i * STAGGER + ENTRY_DUR,
  );
});

tl.from(
  ".orbit-center",
  { opacity: 0, scale: 0.6, duration: ENTRY_DUR, ease: `back.out(${CENTER_BACK})` },
  CENTER_FADE_AT,
);
```

## Variations

- **Collapse to center**: a final 1→0 driver multiplies both radii (and item scale) in `onUpdate` — the ring condenses into the center element; pairs with a CTA "click" igniting the collapse.
- **Tilted orbit plane**: `rotateX(25deg)` on `.orbit-stage` — items visibly arc through the plane.

## Values

| token                   | range                         | notes                                                               |
| ----------------------- | ----------------------------- | ------------------------------------------------------------------- |
| RADIUS_X                | 300–900px                     | must also clear the center label horizontally (see below)           |
| Y_TO_X_RATIO            | 0.4–0.7                       | keep < 1 — a tilted ring, not a frontal halo                        |
| ORBIT_DURATION          | 4–25s per revolution          | ≥ time on screen, or the tween ends and items freeze                |
| ENTRY_DUR               | 0.4–0.8s                      |                                                                     |
| STAGGER                 | 0.06–0.12s                    | below reads "popcorn", above reads plodding                         |
| FLIP_BACK / CENTER_BACK | 1.2–2.0 / 1.2–1.8             | calm the center pop if both fire close together                     |
| CENTER_FADE_AT          | after 2–4 items land          | too early competes; too late leaves a hole                          |
| ROTATE_X/Y_FROM, Z_FROM | ±60–120°, ±45–120°, −200…−400 | one consistent rotation direction across items; mixed signs = noise |
| SCALE_FROM              | 0.2–0.6                       |                                                                     |
| item count              | 4–12                          | fewer feels empty, more crowds the center                           |

## Critical Constraints

- **❗ Entry must flip IN PLACE at the orbital position, NOT at center** — `gsap.set` each item at `(cos(a0)·RADIUS_X, sin(a0)·RADIUS_Y)` with `opacity: 0` BEFORE adding tweens, then phase 1 animates only rotation/opacity/scale. A fromTo that keeps `x/y: 0` flips at the stage center, collides with the center label, then teleports to the orbit when phase 2 starts.
- **❗ Center-label clearance** — `z-index` alone is unreliable inside `preserve-3d` (paint order follows actual Z): push the label forward with `translateZ(220px)` + `z-index: 9999`, cap item z-index to `[1, 50]`, AND size the ring so items clear the label horizontally at every angle: `RADIUS_X × min|cos(θ)| ≥ L_w + I_w + breathing_room` (label/item half-widths; for 6 items the worst case is `cos(30°) ≈ 0.866`). A heavier wordmark needs a wider ring.
- **Each item gets its OWN orbit tween** — a shared `targets: ".orbit-item"` tween can't carry per-item `initialAngle`.
- **The center element is the headline** — the orbit is ornament; if it dominates, grow the center or fade the items down.

## See also

`center-outward-expansion` (burst entry; reversed driver = the collapse finish) · `cursor-click-ripple` (the click that triggers a collapse) · `depth-scatter-assemble` (3D entrance that resolves flat instead of orbiting).


<!-- ===== FILE: hyperframes/hyperframes-animation/rules/particle-burst.md ===== -->

---
name: particle-burst
description: Deterministic particle / confetti events — a confetti pop that bursts up and drifts down (optionally instant-shrinking away), a dot burst from behind text, or a glyph dissolving to particles. Every particle's state is a pure ballistic function of timeline time from index-seeded values, so a scrub to any t shows the correct mid-flight frame.
metadata:
  tags: particles, confetti, burst, dissolve, celebration, ballistic, deterministic, punctuation
---

# Particle Burst

Discrete flying particles as a one-shot event: a **confetti pop** that erupts upward and drifts back down on gravity, a **dot burst** radiating from behind a landing word, or a **glyph dissolve** where text breaks into particles that scatter and die. Particles are ephemeral garnish — born from a beat, fly, gone; they never become layout.

Boundaries: [css-marker-patterns.md](css-marker-patterns.md)'s burst mode is radiating **drawn lines** — a static accent, no flight. [press-release-spring.md](press-release-spring.md)'s release burst is **one blurred radial layer** faking an explosion — enough when a single glow pop will do. [center-outward-expansion.md](center-outward-expansion.md) moves **real layout elements** to final resting slots; particles have no destination, only physics and a death.

## How It Works

The whole event is **one driver tween and one formula**:

1. **Seeded setup** — a fixed pool of `PARTICLE_COUNT` small divs is created once at composition setup (a deterministic loop — setup-time generation is fine; per-frame DOM creation is not). Each particle `i` derives everything from a pure hash:

   ```js
   // angle, speed, size, spin, color (palette[i % palette.length]) — all from prand(i * k)
   const prand = (n) => {
     const x = Math.sin(n * 127.1 + 311.7) * 43758.5453;
     return x - Math.floor(x); // 0..1, pure function of n
   };
   ```

2. **Ballistic formula** — a proxy tween advances `T: 0 → 1` over `FLIGHT_DUR` with `ease: "none"`; `onUpdate` positions every particle as a **pure function of T**:

   ```
   x(T) = vx · T·FLIGHT_DUR
   y(T) = vy · T·FLIGHT_DUR + ½ · G · (T·FLIGHT_DUR)²
   rot(T) = spin · T·FLIGHT_DUR
   ```

   Gravity `G` supplies the rise-decelerate-fall arc for free. Because position is computed from `T` (never accumulated per frame), a seek to any moment renders the exact mid-flight state — this is what makes DOM particles seek-safe. The driver's `ease: "none"` is load-bearing: the physics lives in the formula; an eased driver warps gravity and the arc stops reading as thrown objects.

3. **Death** — an opacity tail inside the same formula (fade over the last `FADE_FRAC` of flight), or the confetti signature: a separate **instant-shrink** tween scaling the pool to 0 in a blink at flight end. Either way the particles end invisible and stay invisible.

## Recipe

```html
<!-- inside a standard scene clip (hyperframes-core) -->
<div class="burst-stage">
  <div class="particle-field" id="particle-field"></div>
  <div class="burst-hero" id="burst-hero">{heroWord}</div>
</div>
```

```css
/* .burst-stage: position: relative; display: grid; place-items: center.
   .burst-hero: z-index: 2 — particles fly BEHIND the word. */
.particle-field {
  position: absolute;
  z-index: 1;
  left: 50%;
  top: 50%; /* the launch origin — offset to taste (e.g. the word's baseline) */
  width: 0;
  height: 0;
}
.particle {
  position: absolute;
  left: 0;
  top: 0;
  border-radius: 2px; /* confetti chip; 50% for dots */
  opacity: 0; /* invisible until the event fires */
  will-change: transform, opacity;
}
```

```js
// Setup: deterministic pool, generated ONCE.
const field = document.getElementById("particle-field");
const palette = ["{accentA}", "{accentB}", "{accentC}"]; // 3-5 brand tokens
const parts = [];
for (let i = 0; i < PARTICLE_COUNT; i++) {
  const el = document.createElement("div");
  el.className = "particle";
  const size = SIZE_MIN + prand(i * 3 + 1) * (SIZE_MAX - SIZE_MIN);
  el.style.width = `${size}px`;
  el.style.height = `${size * 0.7}px`; // slightly oblong = confetti chip
  el.style.background = palette[i % palette.length];
  field.appendChild(el);
  // Index-seeded launch parameters — the particle's whole life, fixed here.
  const angle = -Math.PI / 2 + (prand(i * 5 + 2) * 2 - 1) * CONE; // upward cone
  const speed = SPEED_MIN + prand(i * 7 + 3) * (SPEED_MAX - SPEED_MIN);
  parts.push({
    el,
    vx: Math.cos(angle) * speed,
    vy: Math.sin(angle) * speed, // negative = up
    spin: (prand(i * 11 + 4) * 2 - 1) * SPIN_MAX,
  });
}

// Confetti pop — one driver, pure ballistic formula.
const drive = { T: 0 };
tl.fromTo(
  drive,
  { T: 0 },
  {
    T: 1,
    duration: FLIGHT_DUR,
    ease: "none", // physics lives in the formula, not the ease
    onUpdate: () => {
      const t = drive.T * FLIGHT_DUR; // seconds of flight — pure function of T
      const fade = Math.min(1, (1 - drive.T) / FADE_FRAC); // opacity tail
      parts.forEach((p) => {
        const x = p.vx * t;
        const y = p.vy * t + 0.5 * G * t * t; // rise, stall, drift down
        p.el.style.transform = `translate(${x}px, ${y}px) rotate(${p.spin * t}deg)`;
        p.el.style.opacity = String(drive.T === 0 ? 0 : fade); // T===0 guard covers seeks before the event
      });
    },
  },
  BURST_AT,
);
```

## Variations

- **Confetti pop, then instant-shrink** — the playful signature: full burst, gravity drift, then every chip scales to 0 in a blink: `FADE_FRAC` near 0, plus `tl.to(".particle", { scale: 0, duration: SHRINK_DUR, ease: "power2.in" }, BURST_AT + FLIGHT_DUR - SHRINK_DUR)` with `SHRINK_DUR` 0.15–0.25s. Keep the whole event tiny relative to the subject — a garnish measured in a few dozen pixels, not a screen-filling cannon.
- **Dot burst behind a landing word** — radial instead of a cone: `angle = prand(i) * Math.PI * 2`, `G` near 0, short flight (0.4–0.7s), round dots (`border-radius: 50%`), pool z-indexed behind the word. Fire at the word's settle frame.
- **Glyph dissolve** — seed each particle's **origin** across the glyph block's box (`ox = (prand(i*13) - 0.5) * BLOCK_W`, same for `oy`, added inside the transform), gentle outward drift with low `G`; text fades out over the first ~30% of flight while particles fade in from its silhouette. Color every particle `{textColor}` so the swarm reads as the text's own material. (True per-pixel dissolves are Canvas-2D territory — `techniques.md`; this DOM version sells it up to ~40 particles.)
- **Two-stage burst (pop + stragglers)** — split the pool: 70% on the main driver, 30% on a second driver ~0.12s later with lower speeds; the split is index-derived (`i % 10 < 3`). Same formula, two windows.

## Values

| token                 | range                                        | notes                                                                           |
| --------------------- | -------------------------------------------- | ------------------------------------------------------------------------------- | --- | ----------------------- |
| PARTICLE_COUNT        | 10–18 pop/dots; 24–40 dissolve               | **cap ~40** — per-frame style writes; past that, seek perf and register degrade |
| G                     | 900–1600 px/s² confetti; 0–200 dots/dissolve | natural fall vs drift                                                           |
| SPEED_MIN / SPEED_MAX | 250–700 px/s                                 | per-particle via `prand`, never uniform                                         |
| CONE                  | 0.35–0.8 rad (~20–45°)                       | wider = splash, narrower = fountain                                             |
| FLIGHT_DUR            | 0.7–1.4s                                     | arc should peak ~35–45% of flight: check `                                      | vy  | / G ≈ 0.4 × FLIGHT_DUR` |
| SIZE_MIN / SIZE_MAX   | 5–14px chips; 4–8px dots                     | on a 1080p frame                                                                |
| SPIN_MAX              | 180–720 deg/s confetti; 0 dots               | tumble                                                                          |
| FADE_FRAC             | 0.2–0.35                                     | near 0 when using instant-shrink                                                |
| BURST_AT              | on a cause                                   | the word's settle, a click, a lockup completing — an uncaused burst is noise    |

## Critical Constraints

- **Position is a pure function of time, driver ease `"none"`** — `x(T)`, `y(T)`, `rot(T)` computed from the driver value every frame, never accumulated (`+=`) per tick (accumulation breaks the moment the renderer seeks); gravity is the ease — an eased driver bends the parabola.
- **Fixed pool, no per-frame DOM** — all particles exist after setup with `opacity: 0`; the event only writes `transform` / `opacity`. **`PARTICLE_COUNT ≤ ~40`** — per-frame style writes scale linearly; keep the event cheap.
- **Particles start AND end at `opacity: 0`** — the `drive.T === 0` guard covers seeks to before the event; the tail/shrink covers after. A chip frozen mid-air at driver end is a bug every subsequent frame.
- **Particles are punctuation** — one event per beat, fired on a cause, small relative to the subject, dead before the next beat; z-ordered behind or around the word it celebrates, never over it. A persistent particle system is a background, and that's not this rule.

## See also

`spring-pop-entrance` (confetti fires on the hero's settle frame) · `kinetic-beat-slam` (one beat earns the confetti payoff) · `press-release-spring` (single-layer glow alternative, or compose both) · `css-marker-patterns` (drawn-line burst when the accent should feel hand-annotated) · `scale-swap-transition` (glyph dissolve covers the exit).


<!-- ===== FILE: hyperframes/hyperframes-animation/rules/physics-press-reaction.md ===== -->

---
name: physics-press-reaction
description: Cursor + element synchronized press via subtractive spring forces — cursor lands on element, both compress together, then release. Distinct from press-release-spring (which has no cursor).
metadata:
  tags: spring, click, physics, cursor, subtractive, interaction, synchronized
---

# Physics Press Reaction (Cursor + Element Synced)

Models a real click: a cursor approaches a button, lands, and both compress IN SYNC, then release together. Distinct from [press-release-spring.md](press-release-spring.md) (no cursor — just a press happening); this rule is the COMBINED cursor + element behavior. A single `PRESS_INTENSITY` drives both: press down compresses both to `1 - PRESS_INTENSITY` via **one targets array**, release springs both back to 1.0 with overshoot. The cursor translates to the button's center BEFORE the press starts; after release it may move on or hold.

## Recipe

```html
<button class="btn" id="btn">{ctaCopy}</button>
<!-- Cursor at scene-root level so it translates freely; arrow TIP is the click
     point, so transform-origin: 0 0 — scaling around the tip keeps it stable. -->
<svg class="cursor" id="cursor" style="pointer-events: none; transform-origin: 0 0">…</svg>
```

```js
gsap.set("#cursor", { x: CURSOR_START_X, y: CURSOR_START_Y }); // off-screen / far corner

// Phase 1 — approach
tl.to(
  "#cursor",
  { x: BUTTON_CENTER_X, y: BUTTON_CENTER_Y, duration: APPROACH_DUR, ease: "power2.inOut" },
  APPROACH_START,
);

// Phase 2 — coordinated press down: ONE targets array, same scale
tl.to(
  ["#btn", "#cursor"],
  { scale: 1 - PRESS_INTENSITY, duration: PRESS_DOWN_DUR, ease: "power1.in" },
  PRESS_DOWN_AT,
);

// Phase 3 — release: both spring back together
tl.to(
  ["#btn", "#cursor"],
  { scale: 1, duration: RELEASE_DUR, ease: `back.out(${BOUNCE_FACTOR})` },
  RELEASE_AT,
);

// Phase 4 — inner glow during press, resting shadow on release (contact confirmation)
tl.to(
  "#btn",
  { boxShadow: "{btnPressedShadow}", duration: PRESS_DOWN_DUR, ease: "power1.in" },
  PRESS_DOWN_AT,
);
tl.to(
  "#btn",
  { boxShadow: "{btnRestingShadow}", duration: RELEASE_DUR, ease: "power2.out" },
  RELEASE_AT,
);

// Cursor optionally exits after the press settles
tl.to(
  "#cursor",
  { x: CURSOR_EXIT_X, y: CURSOR_EXIT_Y, duration: CURSOR_EXIT_DUR, ease: "power2.out" },
  CURSOR_EXIT_AT,
);
```

## Variations

- **Multiple-element chain press** — press button A → A triggers a swap → cursor moves to button B → presses again; each press is one full down-release sub-routine.
- **Hold press (continuous pressure)** — insert a `HOLD_DUR` window between press-down and release: both scales stay at `1 - PRESS_INTENSITY`, inner glow stays on. Suggests "thinking" or "loading."
- **Synchronized inner-glow pulse** — during the hold, pulse the inset glow with a sine driver: a `{ p: 0 }` proxy tweened to `Math.PI * GLOW_PULSE_CYCLES * 2` on `ease: "none"`, `onUpdate` writing `boxShadow` with `alpha = GLOW_BASE_ALPHA + sin(p) * GLOW_PULSE_AMP`. Suggests "processing."

## Values

| token               | range / rule                             | notes                                                                                  |
| ------------------- | ---------------------------------------- | -------------------------------------------------------------------------------------- |
| APPROACH_START      | 0–0.3 s                                  | long delays read as a dead frame                                                       |
| APPROACH_DUR        | 0.7–1.3 s                                | faster = urgent, slower = deliberate                                                   |
| PRESS_DOWN_AT       | `= APPROACH_START + APPROACH_DUR`        | cursor arrives exactly as the press begins — avoids "tapping on air"                   |
| PRESS_DOWN_DUR      | 0.1–0.25 s                               |                                                                                        |
| RELEASE_AT          | > `PRESS_DOWN_AT + PRESS_DOWN_DUR`       | optional 0.05–0.4 s hold (or `HOLD_DUR` 0.3–0.8 s) for "thinking" interactions         |
| RELEASE_DUR         | 0.4–0.7 s                                | long enough for the overshoot to settle                                                |
| PRESS_INTENSITY     | 0.05 subtle · 0.10 standard · 0.15 heavy | applied to both cursor and button via the single targets array                         |
| BOUNCE_FACTOR       | 1.6 soft · 2.0 firm · 2.4 cartoony       |                                                                                        |
| CURSOR_START / EXIT | off-screen or far corner                 | the approach must read as motion-in, not a teleport; exit ≥ `RELEASE_AT + RELEASE_DUR` |
| BUTTON_CENTER       | measured                                 | for `place-items: center` at 1920×1080: `(960, 540)`                                   |
| BRAND_REVEAL_AT     | < `PRESS_DOWN_AT`                        | context precedes interaction                                                           |
| glow pulse          | 1–4 cycles; base α 0.15–0.3; amp 0.1–0.2 | `GLOW_BASE_ALPHA − GLOW_PULSE_AMP ≥ 0`                                                 |
| CURSOR_SIZE         | 48–96 px at 1080p                        |                                                                                        |

## Critical Constraints

- **Same press scale on cursor AND button** (one targets array) — only the button scaling makes the cursor "tap on air"; only the cursor scaling makes the button feel disconnected.
- **Cursor arrives BEFORE the press starts** — a clear "cursor over target" moment, or the press is unattributed.
- **`back.out(BOUNCE_FACTOR)` on the release, for both together** — a linear release loses the tactile feel; release MUST come after press.
- **Inner glow appears DURING press, fades on release** — outer shadow shrinks (pushed in), inner glow appears (energy concentrated).
- **Cursor `transform-origin: 0 0`** — the arrow's tip is the click point; scale around the tip keeps it stable. `pointer-events: none` on the cursor.
- **Climax dwell ≥ 1 s** — after release the composition must continue ≥ 1 s; the press is a beat, the viewer needs time to see the result.
- **No real `mouseenter` / `click` events** — HF is a render context; everything runs via the timeline.

## See also

`press-release-spring` (the BUTTON-only press; this rule layers the cursor on top) · `cursor-click-ripple` (adds a ripple at the click point) · `scale-swap-transition` (the press TRIGGERS the swap).


<!-- ===== FILE: hyperframes/hyperframes-animation/rules/press-release-spring.md ===== -->

---
name: press-release-spring
description: Tactile button press with linear compression, spring-based elastic recovery, and layered visual feedback (shadow shrink + release burst + background glow).
metadata:
  tags: spring, press, interaction, button, physics, glow, burst, ui
---

# Press-Release Spring Chain

Separates input (linear compression) from output (spring recovery) to create tactile feel: the overshoot is a natural byproduct of the spring config, not manually coded, with secondary motion (shadow shrink, release burst, background glow) layered on the same trigger frame. This is a **reaction on an element already resting on screen** — an arrival that springs in from nothing is [spring-pop-entrance.md](spring-pop-entrance.md); add a visible cursor actor and it becomes [physics-press-reaction.md](physics-press-reaction.md).

Two phases split at the **release**:

1. **Press**: linear ease → compression (`scale: 1 → PRESS_SCALE`, shadow shrinks). Linear, not spring — the dip must read as instant/tactile, not squishy.
2. **Release**: `back.out(BOUNCE_FACTOR)` spring back to 1.0. Optional burst glow ring expands behind the button; optional environmental glow fades in.

State continuity is critical: the release tween's start value MUST equal the press tween's end value, or the spring snaps to a different position. GSAP threads this automatically when both tweens target the same property at **adjacent positions** — `RELEASE_START = PRESS_START + PRESS_DUR`; a gap or overlap breaks it.

## Recipe

```html
<div class="press-stage">
  <div class="bg-glow" id="bg-glow"></div>
  <!-- Burst sits BEHIND the button (z-index 1 vs 2), same footprint, blurred
       radial gradient, opacity 0. bg-glow is a full-stage radial at negative
       inset so it extends past the stage edges. -->
  <div class="burst" id="burst"></div>
  <button class="btn" id="btn">{buttonLabel}</button>
</div>
```

```js
// Phase 1 — press (linear compression)
tl.to(
  "#btn",
  { scale: PRESS_SCALE, boxShadow: "{btnPressedShadow}", duration: PRESS_DUR, ease: "power1.in" },
  PRESS_START,
);

// Phase 2 — release (spring back; start scale == PRESS_SCALE by adjacency)
tl.to(
  "#btn",
  {
    scale: 1,
    boxShadow: "{btnRestShadow}",
    duration: RELEASE_DUR,
    ease: `back.out(${BOUNCE_FACTOR})`,
  },
  RELEASE_START,
);

// Phase 3 — burst glow pops behind the button, then fades
tl.fromTo(
  "#burst",
  { scale: 1, opacity: 0 },
  {
    scale: BURST_PEAK_SCALE,
    opacity: BURST_PEAK_OPACITY,
    duration: BURST_GROW_DUR,
    ease: "power2.out",
  },
  RELEASE_START,
);
tl.to("#burst", { opacity: 0, duration: BURST_FADE_DUR, ease: "power2.in" }, BURST_FADE_START);

// Phase 4 — environmental glow fades in after release
tl.to(
  "#bg-glow",
  { opacity: BG_GLOW_PEAK_OPACITY, duration: BG_GLOW_FADE_DUR, ease: "power2.out" },
  RELEASE_START,
);
```

## Variations

- **Subtle press** (status save / muted CTA): `PRESS_SCALE` ~0.96, `BOUNCE_FACTOR` ~1.4, burst scale/opacity reduced.
- **Dramatic press** (hero CTA / "ship it"): `PRESS_SCALE` ~0.88, `BOUNCE_FACTOR` ~2.5, burst maxed.
- **Color shift during press** — darken mid-press, return on release; interpolated `backgroundColor` at the same timeline positions as the scale tweens. Same state-continuity rule.
- **State change at release** (approve / confirm) — instead of returning to the rest color, swap to `{successColor}` at `RELEASE_START` and pop a checkmark via a separate `back.out(CHECK_BOUNCE)` tween (1.4–2.0, firmer than the button's bounce — a punctuating "stamp"; pop 0.3–0.6 s) at the same position. The button is now terminal — no further presses expected.

## Values

| token                | range                                      | notes                                                                                      |
| -------------------- | ------------------------------------------ | ------------------------------------------------------------------------------------------ |
| button footprint     | ≥ 3–5% of canvas area                      | a 320×68 button at 1080p is ~1% and the press reads as visually insignificant              |
| PRESS_SCALE          | 0.88 dramatic · 0.92 default · 0.96 subtle | never <0.85 (broken) or >0.98 (no perceptible dip)                                         |
| PRESS_DUR            | 0.10–0.30 s                                | shorter = snappier; must be shorter than `RELEASE_DUR` (input faster than spring recovery) |
| RELEASE_DUR          | 0.40–0.90 s                                | shorter = tight pop; longer = loose, wobbly settle                                         |
| BOUNCE_FACTOR        | 1.4 soft · 2.0 firm · 2.8 cartoony         | or `elastic.out(amplitude, period)` for a rubbery oscillation instead of one overshoot     |
| RELEASE_START        | `= PRESS_START + PRESS_DUR`                | adjacency = automatic state continuity                                                     |
| BURST_PEAK_SCALE     | 3 subtle · 6 default · 8 max               | beyond ~8 the radial gradient pixelates visibly                                            |
| BURST_PEAK_OPACITY   | 0.4–1.0                                    | grow ≈ fade, 0.4–0.7 s each; blur 40–100 px (hard ring → ambient haze)                     |
| BG_GLOW_PEAK_OPACITY | 0.1 subtle · 0.25 default · 0.45 max       | higher washes the whole composition; fade-in 0.6–1.0 s; inset −300…−500 px at 1080p        |

Color tokens: pressed surface darker than rest; rest shadow large + diffuse, pressed small + tight (the button "sinks toward the surface"); burst gradient darker + more saturated than `{btnBg}` — same-color glow looks washed out; bg glow a low-opacity tint of the button's hue family.

## Critical Constraints

- **State continuity** — release start value exactly equals press end value; enforced by same-property adjacency at `RELEASE_START = PRESS_START + PRESS_DUR`.
- **Linear press, spring release** — both spring → squishy; both linear → mechanical, no overshoot punch.
- **Anchor compression on center** (`transform-origin: 50% 50%`) or the button collapses asymmetrically.
- **Burst behind, not in front** — burst `z-index: 1`, button `z-index: 2`; in front it occludes the button at peak opacity.
- **Don't tween `boxShadow` and `filter` on the same element** — they compete in the layout pipeline; shadow on the button, blur on the separate burst layer.
- **Climax dwell** — after the burst peak + reveal, the composition must run ≥ 1 s more (≥ 2 s for dramatic variants); a reveal at `t = DURATION − 0.2 s` reads as "flashed and gone."

## See also

`spring-pop-entrance` (the ENTRANCE counterpart — arrival, not reaction) · `physics-press-reaction` (this press with a visible cursor actor) · `cursor-click-ripple` (the cursor click that triggers the press) · `sine-wave-loop` (idle micro-float BEFORE the press) · `center-outward-expansion` (badge burst synced to the release).


<!-- ===== FILE: hyperframes/hyperframes-animation/rules/reactive-displacement.md ===== -->

---
name: reactive-displacement
description: Physical collision where an entering element's spring drives the exiting element's displacement — single source of truth makes the motion causally linked.
metadata:
  tags: transition, physics, collision, displacement, spring, causal
---

# Reactive Displacement

Exit animation of element A is mathematically DERIVED from the entry spring of element B — a causal link: "A moves _because_ B hit it." Distinct from [scale-swap-transition.md](scale-swap-transition.md) (which overlaps but isn't causal) and [card-morph-anchor.md](card-morph-anchor.md) (one container morphing).

A single 0→1 driver tween (the "entry spring") feeds three concurrent derived motions in one `onUpdate`:

- **Intruder** (B, entering): position interpolated off-stage → settled over the full driver, plus tilt settling to 0° and a sharp early opacity reveal.
- **Victim** (A, exiting): position interpolated settled → off-stage in the OPPOSITE direction, completing at `VICTIM_FRACTION` (~0.4–0.5) of the driver — NOT 1.0.

The victim finishing BEFORE the intruder's entry creates the "hit then settle" rhythm; sharing one eased driver makes the impact moment mathematically synchronized.

## Recipe

```js
// Both cards absolutely centered; overflow: hidden on the scene (off-stage travel);
// will-change: transform, opacity on both; intruder z-index ABOVE victim.
const INTRUDER_START_X = STAGE_W; // off-stage right
const VICTIM_END_X = -STAGE_W; // off-stage left — SAME axis, opposite direction

gsap.set("#victim", { x: 0, opacity: 1, rotation: 0 });
gsap.set("#intruder", { x: INTRUDER_START_X, opacity: 0, rotation: -INTRUDER_TILT });

const driver = { p: 0 };
tl.to(
  driver,
  {
    p: 1,
    duration: DRIVER_DUR,
    ease: `back.out(${BOUNCE_FACTOR})`, // the intruder spring
    onUpdate: () => {
      // Intruder: full 0→1 progress maps enter (off-stage → center)
      const intruderX = INTRUDER_START_X * (1 - driver.p);
      const intruderOpacity = Math.min(1, driver.p * FADE_IN_SHARPNESS);
      const intruderRot = -INTRUDER_TILT * (1 - driver.p); // settles to 0°
      const intruder = document.getElementById("intruder");
      intruder.style.transform = `translate(-50%, -50%) translateX(${intruderX}px) rotate(${intruderRot}deg)`;
      intruder.style.opacity = String(intruderOpacity);

      // Victim: completes its exit at VICTIM_FRACTION of the driver — by the
      // time the intruder centers, the victim is already off-stage.
      const victimP = Math.min(1, driver.p / VICTIM_FRACTION);
      const victimX = VICTIM_END_X * victimP;
      const victim = document.getElementById("victim");
      victim.style.transform = `translate(-50%, -50%) translateX(${victimX}px)`;
      victim.style.opacity = String(1 - victimP);
    },
  },
  DRIVER_AT,
);
// Climax dwell — intruder holds centered for ≥ DWELL_MIN before the scene ends.
```

## Variations

- **Impact rotation on victim** — the victim also rotates as it slides: `const victimRot = victimP * -VICTIM_KICK_DEG;` appended to its transform. `VICTIM_KICK_DEG` 15–25°, magnitude matched to the perceived intruder weight.
- **Vertical collision** — intruder from top, victim displaced downward; same math on Y. Reads as "weight dropped on it."
- **Wobble after settle** — after the intruder centers, a damped sine wobble (`±WOBBLE_AMP_DEG` rotation, linearly decaying over `WOBBLE_DUR` via a second `ease: "none"` driver at `DRIVER_AT + DRIVER_DUR`) before stillness — "impact aftermath."
- **Multi-victim ripple** — the intruder displaces multiple aligned cards, each victim's `victimP` on a slightly offset driver phase (cascade ripple).

## Values

| token             | range                  | notes                                                                                                      |
| ----------------- | ---------------------- | ---------------------------------------------------------------------------------------------------------- |
| DRIVER_AT         | phase-dependent        | after the prior reading beat resolves; must leave ≥ DWELL_MIN of climax dwell before the scene ends        |
| DRIVER_DUR        | 0.6–1.4 s              | short = zippy punch, long = heavy landed impact; higher bounce on long durations reads as floaty           |
| BOUNCE_FACTOR     | 1.2–2.0 (typ. 1.4–1.6) | stay in the `back.out` family (or `elastic.out` for oscillation) — changing family rewrites the feel       |
| VICTIM_FRACTION   | 0.4–0.5                | <0.4 the victim disappears before the impact reads; >0.5 feels parallel, not causal; hard cap ~0.6         |
| STAGE_W           | ≥ composition width    | smaller leaves the off-stage element partially visible at start                                            |
| INTRUDER_TILT     | 5–15° (typ. ~10°)      | low = clean glide, high = "spin-and-plant"; sign consistent with entry direction (momentum transfer)       |
| FADE_IN_SHARPNESS | 3–8                    | intruder reaches opacity 1 at `1/FADE_IN_SHARPNESS` of progress; must be > 1 or it's transparent at center |
| DWELL_MIN         | ≥ 1.0 s (typ. 1.0–1.5) | post-impact dwell is where the new content gets read — do not skip                                         |

## Critical Constraints

- **Single driver = single source of truth** — both motions computed inside ONE driver's `onUpdate`, never separate `tl.to()` calls per element; independent tweens destroy the causal link (they'd merely be near each other in time).
- **Victim completes at a fraction of the driver** — the "hit" is the overlap moment; after it the victim is just vacating space the intruder will fill.
- **Directional momentum transfer** — same axis, opposite directions; different axes read as passing, not colliding.
- **Intruder z-index above victim** — explicit, not DOM order; otherwise the victim looks like it tunneled through.
- **Intruder enters tilted, settles flat** — small initial tilt → 0° reads as "spinning in then planting."
- **Climax dwell after impact** — the impact is the headline beat; hold the settled intruder ≥ DWELL_MIN.
- **`overflow: hidden` on the scene** — off-stage motion exceeds the frame.

## See also

`control-target-sync` (the live-editing mirror — repeated coupled edits, nothing exits) · `hacker-flip-3d` (intruder text reveal during entry) · `sine-wave-loop` (idle breathing during the dwell) · `vertical-spring-ticker` (a ticker that "shoves" the previous content out).


<!-- ===== FILE: hyperframes/hyperframes-animation/rules/scale-swap-transition.md ===== -->

---
name: scale-swap-transition
description: Coordinated shrink-out + spring pop-in morph-like transition between two elements — no SVG path interpolation needed.
metadata:
  tags: transition, morph, scale, swap, spring, pop
---

# Scale-Swap Transition

Simulates a "morph" between two DOM elements by overlapping exit and entrance scale animations. Lighter weight than [card-morph-anchor.md](card-morph-anchor.md) (which morphs container dimensions — use that for SHAPE changes; this rule is for SAME-shape state swaps) and easier than SVG path interpolation.

At a single trigger, two coordinated tweens fire:

1. **Outgoing**: scale `1.0 → EXIT_SCALE` + opacity `1 → 0`, fast `power2.in` (rushing away).
2. **Incoming**: scale `EXIT_SCALE → 1.0` + opacity `0 → 1`, `back.out(BOUNCE_FACTOR)` (arriving with weight).

A small `OVERLAP` window during which both are mid-tween creates the morph illusion; the incoming sits on top via z-index so the outgoing's fade-tail doesn't bleed through.

## Recipe

```html
<!-- Both cards position: absolute; inset: 0 in one fixed-size wrapper — same
     footprint, same transform-origin: 50% 50%. Incoming starts opacity: 0,
     transform: scale(EXIT_SCALE), z-index above the outgoing. -->
<div class="swap-wrap">
  <div class="card outgoing" id="outgoing">{outgoingIcon} {outgoingLabel}</div>
  <div class="card incoming" id="incoming">
    {incomingIcon} {incomingLabel}
    <div class="sub" id="sub">{incomingSubline}</div>
  </div>
</div>
```

```js
// Outgoing: shrink + fade fast
tl.to(
  "#outgoing",
  { scale: EXIT_SCALE, opacity: 0, duration: EXIT_DUR, ease: "power2.in" },
  TRIGGER,
);

// Incoming: pops in with overshoot, starting OVERLAP before the exit finishes
tl.to(
  "#incoming",
  { scale: 1.0, opacity: 1, duration: ENTER_DUR, ease: `back.out(${BOUNCE_FACTOR})` },
  TRIGGER + EXIT_DUR - OVERLAP,
);

// Inner content reveals AFTER the incoming settles
tl.fromTo(
  "#sub",
  { opacity: 0, y: SUB_REVEAL_Y_PX },
  { opacity: 1, y: 0, duration: SUB_REVEAL_DUR, ease: "power3.out" },
  TRIGGER + EXIT_DUR + SUB_REVEAL_DELAY,
);
```

## Variations

- **Delayed inner content reveal** — the classic pattern above: morph the container, then reveal inner text once it settles; the 0.2–0.4 s gap lets the eye land on the new shape before reading.
- **Triple swap (3-state cycle)** — chain A→B→C with triggers `TRIGGER_AB` / `TRIGGER_BC`; each transition is its own tween pair, the previous incoming becoming the next outgoing. State-evolution narratives (early → mid → final labels).
- **Color-shift transition (no scale)** — for a flat morph between same-shape states, drop the scale and keep opacity + a brief background hue tween; less dramatic, more product-UI tone.

## Values

| token            | range                                 | notes                                                                                                  |
| ---------------- | ------------------------------------- | ------------------------------------------------------------------------------------------------------ |
| TRIGGER          | ≥ outgoing settled + a presence-dwell | the outgoing must "land" before transforming                                                           |
| EXIT_DUR         | 0.3–0.5 s                             |                                                                                                        |
| ENTER_DUR        | 0.45–0.7 s                            | longer than `EXIT_DUR` so the overshoot can settle                                                     |
| OVERLAP          | 0.1–0.2 s                             | >0.3 s both are clearly visible together (no morph); <0.05 s leaves a visible empty gap                |
| EXIT_SCALE       | 0.6–0.8                               | smaller exits feel dramatic but risk reading as "vanish" instead of "morph"                            |
| BOUNCE_FACTOR    | 1.4 soft · 1.8 firm · 2.2 cartoony    |                                                                                                        |
| SUB_REVEAL_DELAY | 0.2–0.4 s                             | reveals during the morph compete with the swap for attention                                           |
| BRAND_REVEAL_AT  | < TRIGGER                             | context (brand, eyebrow) sets the stage early; revealed AT the swap it competes with the headline beat |

## Critical Constraints

- **Incoming z-index ABOVE outgoing** — otherwise the outgoing's fade-tail (opacity 0.3–0.5) bleeds through and double-exposes the frame.
- **Both elements share `transform-origin: 50% 50%`** — different origins make the morph read as one thing teleporting elsewhere.
- **Bouncy ease ONLY on the incoming** — outgoing `power2.in`, incoming `back.out`; reversed, the swap feels mechanical.
- **Both cards `position: absolute; inset: 0`** in the same fixed-size wrapper (sized to fit both states; the wrap never resizes).
- **Don't `display: none` the outgoing** after the fade — leave it at `opacity: 0` so layout doesn't reflow.
- **Inner content reveals after the container settles**; **climax dwell ≥ 1 s** after the final state + subline land.

## See also

`press-release-spring` (a button press TRIGGERS the swap — cause and effect) · `card-morph-anchor` (shape-changing alternative) · `reactive-displacement` (when the replacement should read as a causal collision) · `sine-wave-loop` (idle breathing on the final state).


<!-- ===== FILE: hyperframes/hyperframes-animation/rules/sine-wave-loop.md ===== -->

---
name: sine-wave-loop
description: Bounded sine-driven idle — subtle jitter or a single genuinely-needed bounded ambient breath on a held element. De-emphasized: circular breathing as "aliveness" is cheap; prefer sequential reveal timed to the VO, then subtle jitter, before reaching here.
metadata:
  tags: idle, jitter, bounded-ambient, sine, trigonometry, low-amplitude, post-entry
---

# Sine Wave Loop (subtle jitter / bounded ambient)

> **Reach for this last.** Per the motion doctrine (`references/motion-language.md`): circular breathing — scaling text/cards up and down to look "alive" — is cheap, the agent's reflexive cheat, and reads weak. "I'd rather have NO motion than BAD motion." First fill the back of a shot with **sequential reveal timed to the VO**; if a frame has genuinely settled and still needs life, the **sanctioned move is subtle jitter** — this rule at the LOW end of its amplitude range. A full breathing loop is the rare last resort on a single held hero, never stamped on every element.

Keeps a settled element from feeling dead using `Math.sin` on the timeline clock. Two forms:

- **Yoyo form** — one `sine.inOut` tween with `yoyo: true` and a **finite** `repeat` count. Preferred when the idle stands alone on a property nothing else touches.
- **onUpdate form** — one long `ease: "none"` tween drives a `phase` proxy `0 → 2π·CYCLES`; `onUpdate` maps `Math.sin(phase)` into the transform. Required when the offset multiplies/adds onto another live value (compound transforms, amplitude envelopes, multi-octave).

Either way, idle begins where the entry settled: at `phase = 0`, `sin(0) = 0` — the offset is zero, so there is no jump from the entry's resting state.

## Recipe

```js
// onUpdate form — phase-driven, composable.
const phase = { p: 0 };
tl.to(
  phase,
  {
    p: Math.PI * 2 * CYCLES,
    duration: IDLE_DUR,
    ease: "none", // sine provides the easing; a non-linear phase tween distorts the wave
    onUpdate: () => {
      const s = Math.sin(phase.p);
      hero.style.transform = `translateY(${s * Y_AMP_PX}px) scale(${1 + s * SCALE_AMP})`;
      // secondary elements: offset by Math.PI / 2 — synced motion looks mechanical
      dot.style.transform = `scale(${1 + Math.sin(phase.p + Math.PI / 2) * DOT_SCALE_AMP})`;
    },
  },
  IDLE_START_TIME,
);

// Yoyo form — standalone property, finite repeats.
tl.to(
  "#badge",
  { y: -Y_AMP_PX, duration: PERIOD / 2, ease: "sine.inOut", yoyo: true, repeat: REPEATS },
  IDLE_START_TIME,
);
```

## Variations

- **Multi-octave** (organic): stack a higher-frequency overlay — `1 + Math.sin(p) * AMP_PRIMARY + Math.sin(p * OCTAVE_RATIO) * AMP_SECONDARY`, with `AMP_SECONDARY < AMP_PRIMARY` and the combined max inside the normal SCALE_AMP range.
- **Settle and fade** (strongly recommended when `IDLE_DUR > 6s`): ramp amplitude to zero over the last ~20% of idle so the scene visibly settles before the inter-scene transition, instead of handing off mid-drift:

```js
const t = phase.p / (Math.PI * 2 * CYCLES); // 0 → 1 across idle
const env = t < 1 - FADE_FRAC ? 1 : (1 - t) / FADE_FRAC; // FADE_FRAC ≈ 0.2
const scale = 1 + Math.sin(phase.p) * SCALE_AMP * env;
```

This is the single biggest fix when finalize snapshots show "everything's still moving at the end"; it pairs naturally with break-boundary transitions (the outgoing visual is static when the crossfade/push begins).

## Values

| token           | range / default                      | notes                                                                      |
| --------------- | ------------------------------------ | -------------------------------------------------------------------------- |
| SCALE_AMP       | **0.008–0.015 default**              | push to 0.02–0.04 only when isolated on canvas / scene <6s / kinetic brief |
| Y_AMP_PX        | **2–3px default**                    | 4–6px only under the same gating; rotation ±0.3–0.8° rarely needed at all  |
| period          | 1.5–3s (2.5–4s when idle is long)    | <1.5s frantic; >4s lifeless in a short window                              |
| CYCLES          | `IDLE_DUR/3 ≤ CYCLES ≤ IDLE_DUR/1.5` | derive from the period, not the other way round                            |
| IDLE_START_TIME | ≥ entry settle + ~0.1s               | `sin(0)=0` at this moment → no jump off the entry tail                     |
| IDLE_DUR        | `TOTAL_DURATION − IDLE_START_TIME`   | one long tween fills the hold — never restarted                            |
| DOT_SCALE_AMP   | 0.04–0.12                            | small accents tolerate more than the hero                                  |
| OCTAVE_RATIO    | 2.0–4.0                              | integer-ish reads musical; non-integer reads organic                       |

## Critical Constraints

- **Prefer reveal, then jitter, then breath** — the doctrine order above; default to the LOW end of every amplitude range. At the upper end across 5+ consecutive scenes the whole film reads as "shimmering".
- **Long idle window** (`IDLE_DUR > 6s` OR idle > 30% of composition): halve `SCALE_AMP` / `Y_AMP_PX`, slow the period to 3–4s, and add the settle-and-fade tail.
- **Concurrent idle on N elements** (columns, card grid, stat row): per-element amplitude ≤ default `/ √N`, AND stagger the periods (2.1s / 1.9s / 2.4s). Three columns at ±6px compound to ±18px of competing motion; three at ±2–3px read as one collective breath.
- **Compose, don't replace** — idle ADDS to the element's resting transform; never overwrite the entry's final translation.
- **Phase tween `ease: "none"`** — sine itself is the curve.
- **No CSS `@keyframes` for idle** — CSS animation runs on the browser's render clock, independent of the HF seek clock; a CSS-driven idle flickers/desyncs. Drive idle inside the timeline.

## See also

`ambient-glow-bloom` (the glow-layer counterpart, same bounded-breathe discipline) · `press-release-spring` / `counting-dynamic-scale` / `card-morph-anchor` / `orbit-3d-entry` (settled elements this can follow) · `spring-pop-entrance` (the arrival that precedes any idle).


<!-- ===== FILE: hyperframes/hyperframes-animation/rules/split-tilt-cards.md ===== -->

---
name: split-tilt-cards
description: Two cards side-by-side with opposing Y-rotation creating a symmetric 3D split-screen layout for comparisons or feature pairs.
metadata:
  tags: 3d, cards, split, tilt, comparison, symmetric, layout
---

# Split Tilt Cards

Two cards side-by-side with opposing `rotateY` (left `+TILT`, right `−TILT`) — a symmetric "book-open" 3D split for comparisons, before/after, feature pairs. Each card slides in from its own side (reinforcing "they came from their own worlds and met here"), then the pair idles in counter-phase.

## How It Works

`perspective` on the scene root (REQUIRED — without it `rotateY` flattens to a 2D layout) and `transform-style: preserve-3d` on the stage and both cards. Entry starts each card off-axis with `TILT + TILT_OVERSHOOT`, settling to `TILT` — a pivot-into-place. Idle is a gentle counter-phase y-bob (the two yoyo tweens run in opposite directions); copy fades up during the cards' settle, not after.

## Recipe

```html
<!-- inside a standard scene clip (hyperframes-core) -->
<div class="split-stage">
  <div class="card card-left">
    <div class="card-eyebrow">{leftEyebrow}</div>
    <div class="card-headline">{leftHeadline}</div>
    <div class="card-body">{leftBody}</div>
  </div>
  <div class="card card-right">…</div>
</div>
```

```css
.scene-root {
  display: grid;
  place-items: center;
  perspective: SCENE_PERSPECTIVE; /* REQUIRED */
}
.split-stage {
  display: flex;
  gap: STAGE_GAP;
  transform-style: preserve-3d;
}
.card {
  width: CARD_WIDTH;
  transform-style: preserve-3d;
  will-change: transform;
}
/* Shadow falls WITH the facing direction: left card faces right → shadow right. */
.card-left {
  box-shadow: -CARD_SHADOW_OFFSET CARD_SHADOW_DROP CARD_SHADOW_BLUR {shadowColor};
}
.card-right {
  box-shadow: CARD_SHADOW_OFFSET CARD_SHADOW_DROP CARD_SHADOW_BLUR {shadowColor};
}
```

```js
// Entry — from outside, opposing tilts settle with a small pivot
tl.fromTo(
  ".card-left",
  { x: -ENTRY_SLIDE_DIST, rotateY: TILT + TILT_OVERSHOOT, opacity: 0 },
  { x: 0, rotateY: TILT, opacity: 1, duration: ENTRY_DUR, ease: "power3.out" },
  LEFT_AT,
);
tl.fromTo(
  ".card-right",
  { x: ENTRY_SLIDE_DIST, rotateY: -TILT - TILT_OVERSHOOT, opacity: 0 },
  { x: 0, rotateY: -TILT, opacity: 1, duration: ENTRY_DUR, ease: "power3.out" },
  RIGHT_AT,
);

// Counter-phase idle bob — opposite signs = alive; synchronized = conveyor belt
tl.to(
  ".card-left",
  { y: -FLOAT_AMP, duration: FLOAT_DURATION / 2, ease: "sine.inOut", yoyo: true, repeat: 1 },
  IDLE_START,
);
tl.to(
  ".card-right",
  { y: FLOAT_AMP, duration: FLOAT_DURATION / 2, ease: "sine.inOut", yoyo: true, repeat: 1 },
  IDLE_START,
);

// Copy fades up during the settle
tl.from(
  ".card-eyebrow, .card-headline, .card-body",
  { opacity: 0, y: COPY_RISE, stagger: COPY_STAGGER, duration: COPY_DUR, ease: "power2.out" },
  COPY_REVEAL_AT,
);
```

## Variations

- **Badges / floating labels**: position them on the PARENT, never inside a card — inside they inherit the `rotateY` and tilt off-axis.
- **3+ cards**: center card stays flat (`rotateY: 0`), outer two tilt inward — "old way / nothing / our way."
- **Zoom-through**: a separate camera tween scaling `.split-stage` reads as the viewer crossing the gap between the tilted pair.

## Values

| token             | range                            | notes                                                   |
| ----------------- | -------------------------------- | ------------------------------------------------------- |
| SCENE_PERSPECTIVE | 1000–2400px                      | lower exaggerates the tilt; higher reads near-isometric |
| TILT              | 10–18°                           | < 10 reads almost flat; > 18 folds shut and copy blurs  |
| TILT_OVERSHOOT    | 4–12°                            | the pivot-into-place feel                               |
| STAGE_GAP         | 40–120px (~0.06–0.15×CARD_WIDTH) | small = fused pair; large = compared-but-separate       |
| CARD_WIDTH        | 480–820px @1920                  | `2×CARD_WIDTH + STAGE_GAP ≤ 0.95×stage` at full tilt    |
| ENTRY_SLIDE_DIST  | 200–500px (~0.3–0.6×CARD_WIDTH)  |                                                         |
| ENTRY_DUR         | 0.6–1.2s                         |                                                         |
| RIGHT_AT          | LEFT_AT + 0–0.3s                 | zero feels mechanical; large fragments the pair         |
| FLOAT_AMP         | 3–8px                            | subtle is the point                                     |
| FLOAT_DURATION    | 1.6–3.2s round trip              | breathing cadence; IDLE_START ≥ entry end               |
| COPY_REVEAL_AT    | during the entry tail            | copy popping in after cards are idle reads disconnected |

## Critical Constraints

- **`perspective` on the scene root is REQUIRED**; `preserve-3d` on the stage AND each card.
- **Shadow direction matches tilt** — left card faces right → shadow falls right (and mirrored). Wrong sign reads as broken 3D.
- **Counter-phase idle** — the two bobs run with opposite signs at the same position.
- **Badges outside the card divs** (they'd inherit the rotation).
- **Body copy ≤ 2 lines per card** — tilted long paragraphs collapse into perspective blur.
- **Symmetric weight** — same width, same vertical center, similar line counts; asymmetry breaks the comparison metaphor.

## See also

`card-morph-anchor` (the pair can morph into one unified shape afterward) · `counting-dynamic-scale` (numbers as each side's headline) · `sine-wave-loop` (the idle form).


<!-- ===== FILE: hyperframes/hyperframes-animation/rules/spring-pop-entrance.md ===== -->

---
name: spring-pop-entrance
description: The canonical entrance pop — an element (or staggered group) arrives by scaling 0 → 1 on a smooth long-tail settle (power3 default); bouncy overshoot is a rare, explicitly-playful exception. fromTo so it's correct at t=0 under seek.
metadata:
  tags: spring, entrance, pop, scale, power3, settle, stagger, reveal, arrival
---

# Spring-Pop Entrance

> **Smooth beats bouncy.** This entrance defaults to a smooth long-tail settle — `power3.out` (or `expo.out` for a faster front) — that decelerates cleanly into the resting size with **no overshoot**. Bouncy `back.out` is the **#1 instant turn-off** in agent-made videos and is almost never executed well; it is a rare, explicitly-playful exception (consumer / fun brand), never the default. When unsure, settle smoothly.

THE entrance primitive: an element (or staggered group) arrives by springing from nothing — `scale: 0 → 1`, optional small `y` rise — and settles without bouncing. This is **arrival**, not reaction: distinct from [press-release-spring.md](press-release-spring.md) (a click/press → release feedback chain on an element that already rests on screen). Many blueprints used to borrow that rule to fake an entrance; reach for this instead.

## How It Works

One `fromTo` carries the whole arrival: from `{ scale: 0, opacity: 0 }` (explicit, so t=0 is correct under seek) to `{ scale: 1, opacity: 1, ease: "power3.out" }`. For a **group**, the same `fromTo` runs per element at `i * STAGGER`, capped so the group reads as one arriving beat. The `scale` grow is load-bearing; the `y` rise is garnish — drop everything else and it must still read as a clean entrance. Let the ease produce the settle: never hand-key a `scale: 1.1` mid-state (it double-bounces against the curve).

## Recipe

```html
<!-- inside a standard scene clip (hyperframes-core) -->
<div class="pop-hero" id="hero">{heroLabel}</div>

<div class="pop-grid">
  <div class="pop-item">{itemA}</div>
  <div class="pop-item">{itemB}</div>
  <div class="pop-item">{itemC}</div>
</div>
```

```css
.pop-hero,
.pop-item {
  transform-origin: 50% 50%; /* in-place pop; move to the source point for the anchored variation */
  will-change: transform;
}
.pop-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: GRID_GAP;
  place-items: center;
}
```

```js
// Single hero pop — smooth long-tail settle, no overshoot.
tl.fromTo(
  "#hero",
  { scale: 0, opacity: 0 },
  { scale: 1, opacity: 1, duration: POP_DUR, ease: "power3.out" },
  ENTRY_AT,
);

// Staggered group pop — one arriving beat.
gsap.utils.toArray(".pop-item").forEach((el, i) => {
  tl.fromTo(
    el,
    { scale: 0, opacity: 0, y: Y_RISE },
    { scale: 1, opacity: 1, y: 0, duration: POP_DUR, ease: "power3.out" },
    GROUP_ENTRY_AT + i * STAGGER,
  );
});
```

## Variations

- **Calm settle** (premium / enterprise): `power3.out`, no rotation, `Y_RISE` 0–12px — a weighted, confident landing for a hero wordmark or product shot.
- **Firm settle** (everyday default): `power3.out` or `expo.out` for a punchier front, `Y_RISE` ~24px — cards, icons, callouts.
- **Exact-physics settle**: when the settle IS the shot, swap the ease for `springEase({ response: 0.4 })` (critically damped) from `../adapters/gsap-easing-and-stagger.md` → Spring Eases; take `duration` from the helper.
- **Origin-anchored pop**: a callout growing out of a specific point (marker, pointer tip) sets `transform-origin` to that point (e.g. `0% 100%`) so `scale: 0 → 1` reads as "emerging from the source", not "inflating in place".
- **Pop into a held slot**: land the pop and hold still — no idle loop baked into the entrance. If the held frame genuinely needs life, hand off to [sine-wave-loop.md](sine-wave-loop.md) for subtle jitter on a separate later tween; prefer revealing the next element on its VO cue.
- **Bouncy pop (RARE — explicitly-playful only)**: swap the ease for `back.out(OVERSHOOT)` and optionally settle a small `rotation: ROT_FROM → 0` so elements look hand-placed. Only for a deliberately playful register — never product / enterprise / serious tone:

```js
tl.fromTo(
  el,
  { scale: 0, opacity: 0, rotation: ROT_FROM },
  { scale: 1, opacity: 1, rotation: 0, duration: POP_DUR, ease: `back.out(${OVERSHOOT})` },
  GROUP_ENTRY_AT + i * STAGGER,
);
```

Even here keep `OVERSHOOT ≤ ~2` — past that it reads as cartoon wobble. Better still: the baked spring at `dampingFraction: 0.6–0.7` (same adapters doc) gives ~5–10% overshoot that reads physical where `back.out` reads cartoon.

## Values

| token      | range                                     | notes                                                            |
| ---------- | ----------------------------------------- | ---------------------------------------------------------------- |
| EASE       | `power3.out` default; `expo.out` punchier | `back.out(OVERSHOOT)` only in the playful variant                |
| POP_DUR    | 0.4–0.7s                                  | shorter = tight snap; hero must be visible by **t ≤ 0.5s**       |
| STAGGER    | 0.04–0.08s                                | `min(0.06, 0.5 / ITEM_COUNT)` — self-caps the window             |
| ITEM_COUNT | 3–9                                       | >9 makes the stagger vanish — switch to a wipe/sweep reveal      |
| Y_RISE     | 0–32px                                    | small; never large enough to read as a slide-up                  |
| ROT_FROM   | −10°–+10°                                 | playful variant only; alternate sign by index (`i % 2 ? 6 : -6`) |
| ENTRY_AT   | 0–0.4s                                    | a beat of quiet, but keep the subject landing by t ≤ 0.5s        |

## Critical Constraints

- Default ease `power3.out` (no overshoot); `back.out` only in the explicitly-playful variant, and there `OVERSHOOT ≤ ~2`.
- `ITEM_COUNT × STAGGER ≤ ~0.5s` — the group must land inside one beat.
- Entrances state the collapsed from-state in `fromTo` — never rely on a CSS-hidden start (it renders visible before the tween claims it under seek).
- `transform-origin: 50% 50%` for an in-place pop; the source point only for the anchored variation.
- This is a finite arrival — idle motion on a held element is a separate, later `sine-wave-loop` tween.

## See also

`center-outward-expansion` (pop while radiating to slots) · `press-release-spring` (the click-feedback counterpart) · `sine-wave-loop` (post-arrival jitter, sparingly).


<!-- ===== FILE: hyperframes/hyperframes-animation/rules/stat-bars-and-fills.md ===== -->

---
name: stat-bars-and-fills
description: Data-viz primitives that pair a number with a graphic — growth bars (CSS scaleY stagger), a progress fill (bar or ring), and a partial star-rating wipe. Seek-safe, deterministic.
metadata:
  tags: data, stats, chart, bars, progress, ring, stars, rating, infographic, number
---

# Stat Bars & Fills

The graphics that give a stat **visual weight** beside its number: a small bar chart, a progress bar/ring filling to a percentage, or a star row filling to a fractional rating. Pair these with [counting-dynamic-scale.md](counting-dynamic-scale.md) (the number) for a complete stat scene.

**Layout blueprint — pick ONE and hold it across all stats:**

- **Single-focus** — one centered frame, the number is the hero, a ring or bar sits under/around it. Cleanest for a sequential reveal (stat 1 → stat 2 → stat 3 in the same frame).
- **Split-frame** — big number on the left, paired graphic on the right. Better when stats are shown together or each needs a distinct visual.

Don't mix blueprints between stats in one piece — that reads as inconsistent.

## Recipe

### 1 — Growth Bars (CSS `scaleY` stagger)

Bars grow from the baseline with a stagger; the last bar is the accent. Heights are authored in CSS (inline height per bar); GSAP only reveals `scaleY: 0 → 1` — never animate `height`.

```css
.bars {
  display: flex;
  align-items: flex-end;
  gap: 14px;
  height: 280px;
}
.bar {
  width: 48px;
  background: #3a4a64;
  transform: scaleY(0);
  transform-origin: bottom center; /* grow UP from the baseline, not from center */
}
.bar:last-child {
  background: #ffc300; /* accent the final/current bar */
}
```

```js
tl.to(".bar", { scaleY: 1, duration: 0.7, ease: "power3.out", stagger: 0.08 }, 0.3);
```

### 2 — Progress Fill

**Bar form** — `scaleX` from a left origin:

```css
.track {
  width: 520px;
  height: 16px;
  background: #1b263b;
  border-radius: 8px;
  overflow: hidden;
}
/* width:100% is REQUIRED — an absolutely-positioned fill with no width is 0px, and scaleX of 0 is
   still 0 → the bar renders invisible (automated gates may miss a zero-width scaled element). */
.fill {
  width: 100%;
  height: 100%;
  background: #ffc300;
  transform: scaleX(0);
  transform-origin: left center;
}
```

```js
const PCT = 0.92; // 92%
tl.to(".fill", { scaleX: PCT, duration: 1.0, ease: "power2.out" }, 0.3);
```

**Ring form** — measured stroke draw (mechanics in [svg-path-draw.md](svg-path-draw.md)):

```js
const ring = document.querySelector("#ring");
const LEN = ring.getTotalLength(); // measure, don't hard-code the circumference
ring.style.strokeDasharray = LEN;
ring.style.strokeDashoffset = LEN; // empty
// rotate the <circle> -90deg in CSS so the fill starts at 12 o'clock
tl.to(ring, { strokeDashoffset: LEN * (1 - 0.92), duration: 1.1, ease: "power2.out" }, 0.3);
```

### 3 — Star-Rating Fill (fractional)

A gold star row revealed left-to-right to a fractional value (e.g. 4.6 / 5) via a clip wipe over a gold layer sitting on a gray layer.

```html
<div class="stars">
  <div class="stars-gray">★★★★★</div>
  <div class="stars-gold" id="goldStars">★★★★★</div>
</div>
```

```css
.stars {
  position: relative;
  font-size: 64px;
  letter-spacing: 8px;
}
.stars-gray {
  color: #2b3548;
}
.stars-gold {
  position: absolute;
  inset: 0;
  color: #ffc300;
  width: 100%;
  clip-path: inset(0 100% 0 0);
}
```

```js
const RATING = 4.6,
  MAX = 5;
tl.to(
  "#goldStars",
  { clipPath: `inset(0 ${100 - (RATING / MAX) * 100}% 0 0)`, duration: 1.0, ease: "power2.out" },
  0.3,
);
```

## Values

| token         | range       | notes                                                                               |
| ------------- | ----------- | ----------------------------------------------------------------------------------- |
| bar count     | 4–6         | reads as "a trend" without clutter; the last bar is the current/accent value        |
| fill duration | 0.8–1.2s    | matched to the paired count-up so number and graphic land together (share the ease) |
| stagger       | 0.06–0.1s   | larger feels sluggish, 0 loses the build                                            |
| accent hue    | exactly one | bars/fill/stars all use the same accent, the rest is muted                          |

## Critical Constraints

- **`scaleY` / `scaleX` / `clipPath`, never `height`/`width` tweens** — author each bar's final height in CSS and scale from 0.
- **`transform-origin`** must be `bottom` (bars grow up) / `left` (fills grow right) — the default center origin scales from the middle and looks wrong.
- **`.fill` needs `width: 100%`** — a zero-width fill scaled by any factor is still invisible, and automated gates may miss it.
- **Measure, don't hard-code** — ring length via `getTotalLength()`; a hard-coded circumference breaks if the radius changes.
- **Match the number's timing** — the fill and the count-up peak together (same start + ease) so the stat resolves as one beat, not two; a paired counter's `onUpdate` must be O(1) (see [counting-dynamic-scale.md](counting-dynamic-scale.md)).
- **One accent hue, consistent blueprint** — see `hyperframes-creative/references/data-in-motion.md`.

## See also

`counting-dynamic-scale` (the number beside the graphic — same ease/duration) · `svg-path-draw` (progress-ring draw mechanics) · `hyperframes-creative/references/data-in-motion.md` (stat layout + visual weight).


<!-- ===== FILE: hyperframes/hyperframes-animation/rules/svg-icon-enrichment.md ===== -->

---
name: svg-icon-enrichment
description: Animate internal SVG elements (rotating hands, opening blades, pulsing dots, dash flows) to make icons feel alive without replacing them.
metadata:
  tags: svg, icon, animation, internal, micro-animation, pulse, rotation
---

# SVG Icon Enrichment

Treats an SVG icon as a composition of animated PARTS, not an opaque image. Each meaningful internal element (a clock hand, scissor blade, recording dot, data line) gets its own micro-animation, targeted by id. Distinct from [svg-path-draw](svg-path-draw.md) (which animates the OUTLINE drawing) — enrichment animates INTERNAL PARTS, ideally after the outline has drawn.

Four signature patterns:

| Pattern     | Use For                            | Math                                  | Tip                                |
| ----------- | ---------------------------------- | ------------------------------------- | ---------------------------------- |
| Rotation    | Clock, gear, loader, dial          | `rotate(deg cx cy)` attribute, linear | see the transform-center gotcha    |
| Oscillation | Scissors, wings, toggle            | `rotate(±sin·amp)` on opposing groups | opposite signs on the two parts    |
| Pulse       | Recording dot, heart, notification | `scale(1 + sin·amp)` + opacity        | ring lags dot by π/2 for ripple    |
| Dash flow   | Cutting line, data stream          | `strokeDashoffset` linear via time    | negative for L→R, positive for R→L |

## ❗ The transform-center gotcha

**For rotation around an explicit point inside an SVG, use the SVG `transform` ATTRIBUTE, not CSS transform**: `el.setAttribute("transform", `rotate(${deg} ${cx} ${cy})`)`. The CSS combination `transform: rotate(...)` + `transform-origin: 60px 60px` + `transform-box: fill-box` interprets the origin in the element's OWN **bbox-local** coordinates, NOT viewBox coordinates. For a thin `<line>` (whose bbox is the line's narrow envelope), `60 60` bbox-local is a point OUTSIDE the line — the hand flies along an off-center arc instead of rotating in place. Same trap for small inner shapes (a dot circle whose bbox is the small circle, not the full viewBox).

**Scaling around a center point**: same attribute route — `el.setAttribute("transform", `translate(${cx} ${cy}) scale(${s}) translate(-${cx} -${cy})`)`.

## Recipe

```html
<!-- inside a standard scene clip — named children are the animation targets -->
<svg class="icon-svg" viewBox="0 0 120 120" xmlns="http://www.w3.org/2000/svg">
  <circle cx="60" cy="60" r="50" fill="none" stroke="{accentColor}" stroke-width="6" />
  <line
    id="hand-min"
    x1="60"
    y1="60"
    x2="60"
    y2="22"
    stroke="{textColor}"
    stroke-width="6"
    stroke-linecap="round"
  />
  <line
    id="hand-sec"
    x1="60"
    y1="60"
    x2="60"
    y2="30"
    stroke="{recordColor}"
    stroke-width="3"
    stroke-linecap="round"
  />
  <circle cx="60" cy="60" r="6" fill="{textColor}" />
</svg>
<!-- pulse icon: #rec-ring + #rec-dot circles; dash-flow: a <line> with stroke-dasharray="14 12" -->
```

```js
// Pattern 1 — Rotation. Proxy tween → SVG transform attribute (explicit center, see gotcha).
const hand = document.getElementById("hand-min");
const minState = { deg: 0 };
tl.to(
  minState,
  {
    deg: 360 * MIN_REVOLUTIONS,
    duration: TOTAL_DURATION,
    ease: "none", // linear motion is the point
    onUpdate: () => hand.setAttribute("transform", `rotate(${minState.deg} 60 60)`),
  },
  0,
);
// second hand: same shape with SEC_REVOLUTIONS (visibly faster).

// Pattern 3 — Pulse. One phase proxy drives dot + ring, ring offset by π/2.
const dot = document.getElementById("rec-dot");
const ring = document.getElementById("rec-ring");
const pulse = { p: 0 };
tl.to(
  pulse,
  {
    p: Math.PI * 2 * PULSE_CYCLES,
    duration: TOTAL_DURATION,
    ease: "none", // sine handles the curve
    onUpdate: () => {
      const sD = 1 + Math.sin(pulse.p) * PULSE_DOT_AMP;
      const sR = 1 + Math.sin(pulse.p + Math.PI / 2) * PULSE_RING_AMP;
      dot.setAttribute("transform", `translate(60 60) scale(${sD}) translate(-60 -60)`);
      ring.setAttribute("transform", `translate(60 60) scale(${sR}) translate(-60 -60)`);
      ring.style.opacity = String(
        PULSE_RING_OPACITY_BASE + Math.sin(pulse.p) * PULSE_RING_OPACITY_AMP,
      );
    },
  },
  0,
);

// Pattern 4 — Dash flow. Linear offset tween on a dashed stroke.
const flowState = { offset: 0 };
tl.to(
  flowState,
  {
    offset: DASH_FLOW_TOTAL_OFFSET, // negative = L→R
    duration: TOTAL_DURATION,
    ease: "none",
    onUpdate: () => {
      document.getElementById("data-flow").style.strokeDashoffset = String(flowState.offset);
    },
  },
  0,
);
```

## Variations

- **Stroke draw → enrichment chain** — draw the outline first via [svg-path-draw](svg-path-draw.md) (phase 1, `0 → OUTLINE_DUR`), then start enrichment at `OUTLINE_DUR`: the icon "wakes up" after assembly.
- **Per-icon entry stagger** — for a row of icons, each icon's enrichment starts as it fades in, not synchronized.

## Values

| token                           | range                | notes                                                                                           |
| ------------------------------- | -------------------- | ----------------------------------------------------------------------------------------------- |
| MIN_REVOLUTIONS                 | 0.5–2.0              | avoid integer revolutions if the end frame is visible (lands back at start)                     |
| SEC_REVOLUTIONS                 | 4–10                 | > MIN × 3 or the speed difference doesn't read                                                  |
| PULSE_CYCLES                    | 2–4 over a 3–5s comp | ≥5 reads as anxious flicker; ≤1 reads as forgotten                                              |
| PULSE_DOT_AMP                   | 0.05–0.20            | 0.05 = breathing; 0.20 = throbbing                                                              |
| PULSE_RING_AMP                  | 0.04–0.12            | must be < PULSE_DOT_AMP or the ring overshadows the dot                                         |
| PULSE_RING_OPACITY_BASE / \_AMP | 0.4–0.6 / 0.3–0.5    | BASE − AMP ≥ 0 and BASE + AMP ≤ 1                                                               |
| DASH_FLOW_TOTAL_OFFSET          | ±100–400             | must be an integer multiple of the dash period (dash + gap) or the end frame shows a phase jump |

## Critical Constraints

- **The transform-center gotcha above** — SVG `transform` attribute for any rotation/scale around an explicit interior point; never CSS `transform-origin` + `transform-box: fill-box` on thin lines or small inner shapes.
- **No `requestAnimationFrame`** — like CSS animation, it desyncs from HF's frame-by-frame seek; continuous motion lives inside the timeline as linear proxy tweens.
- **Amplitudes subtle** — icons are decorative, not headlines; calibrate rotation speed against composition length, not absolute time.
- **Phase-offset the parts** — minute vs second hand at different speeds, ring lagging dot by π/2. Pure sync looks mechanical.
- **`stroke-linecap: round`** on flowing/dashed lines for clean dash edges.
- **Climax dwell ≥1s** — if the enrichment is the headline beat, the composition continues ≥1s after the most dramatic moment.

## See also

`svg-path-draw` (outline draws first, enrichment second) · `orbit-3d-entry` (orbiting items are enriched icons) · `sine-wave-loop` (the whole icon floats while internal parts animate).


<!-- ===== FILE: hyperframes/hyperframes-animation/rules/svg-path-draw.md ===== -->

---
name: svg-path-draw
description: Animate SVG paths drawing progressively using stroke-dasharray and stroke-dashoffset.
metadata:
  tags: svg, stroke, draw, path, reveal, icon, vector
---

# SVG Path Draw

Reveals an SVG shape by animating its stroke as if a pen were tracing it. Two stroke properties together: **`stroke-dasharray = <pathLength>`** makes the entire path one dash; **`stroke-dashoffset`** starts at the path length (dash shifted fully out of view → invisible) and tweens to `0` (fully drawn). The length comes from the DOM API `path.getTotalLength()` — measured, never guessed.

Works on anything with a stroke: `<path>`, `<circle>`, `<rect>`, `<line>`, `<polyline>`, `<polygon>`, `<ellipse>`.

## Recipe

```html
<!-- inside a standard scene clip -->
<svg class="logo-mark" viewBox="0 0 200 200" xmlns="http://www.w3.org/2000/svg">
  <path id="bar-left" d="M 60 40 L 60 160" />
  <path id="bar-right" d="M 140 40 L 140 160" />
  <path id="bar-mid" d="M 60 100 L 140 100" />
</svg>
```

```css
.logo-mark path {
  fill: none; /* outline-only draw — a fill would appear immediately and ruin the reveal */
  stroke: {accentColor};
  stroke-width: 12;
  stroke-linecap: round; /* softer endpoints */
  stroke-linejoin: round;
}
```

```js
// Setup: measure each path and set its dash pattern. Real measured geometry, not a magic number.
document.querySelectorAll(".logo-mark path").forEach((p) => {
  const len = p.getTotalLength();
  p.style.strokeDasharray = `${len}`;
  p.style.strokeDashoffset = `${len}`;
});

// Stagger draws so the eye reads continuous motion — each segment starts at
// ~70-80% of the previous segment's duration, before it finishes.
tl.to(
  "#bar-left",
  { strokeDashoffset: 0, duration: SEGMENT_DRAW_DUR, ease: "power2.out" },
  SEG_1_START,
);
tl.to(
  "#bar-right",
  { strokeDashoffset: 0, duration: SEGMENT_DRAW_DUR, ease: "power2.out" },
  SEG_2_START,
);
tl.to(
  "#bar-mid",
  { strokeDashoffset: 0, duration: FINAL_SEGMENT_DUR, ease: "power2.out" },
  SEG_3_START,
);

// Companion wordmark fades in only after the last stroke settles.
tl.to(
  ".brand-line",
  { opacity: 1, duration: BRAND_FADE_DUR, ease: "power1.out" },
  BRAND_FADE_START,
);
```

## Variations

- **Ring starting at 12 o'clock** — `<circle>` / `<rect>` strokes start at 3 o'clock by default; rotate the element `-90deg` so a progress ring draws from the top:

```html
<circle
  cx="100"
  cy="100"
  r="60"
  id="ring"
  style="transform-origin: 100px 100px; transform: rotate(-90deg)"
/>
```

- **Linear (constant-speed) draw** — `ease: "none"` for a steady-rate "real pen" trace.
- **Draw then fill** — for filled shapes, tween `fillOpacity: 0 → 1` AFTER the stroke completes (requires `fill-opacity: 0` initially and a real `fill` in CSS):

```js
tl.to(
  "#path",
  { strokeDashoffset: 0, duration: SEGMENT_DRAW_DUR, ease: "power2.out" },
  SEG_1_START,
);
tl.to(
  "#path",
  { fillOpacity: 1, duration: FILL_FADE_DUR, ease: "power1.out" },
  SEG_1_START + SEGMENT_DRAW_DUR,
);
```

## Values

| token             | range                                   | notes                                                                                              |
| ----------------- | --------------------------------------- | -------------------------------------------------------------------------------------------------- |
| SEGMENT_DRAW_DUR  | 0.3–0.8s                                | fast snap vs deliberate pen trace; >~1s feels sluggish for a logo reveal                           |
| FINAL_SEGMENT_DUR | 60–80% of SEGMENT_DRAW_DUR              | proportional to segment length — a short connector at full duration reads slower than its siblings |
| SEG_N_START       | previous start + 70–80% of its duration | reads as continuous motion, not N isolated animations                                              |
| SEG_1_START       | 0–0.4s                                  | a small ~0.2s lead-in lets the viewer settle before motion                                         |
| BRAND_FADE_START  | ≥ last stroke end (+ ~0.2s beat)        | earlier and the wordmark competes with the draw                                                    |
| BRAND_FADE_DUR    | 0.3–0.8s                                | snap (urgent) vs glide (premium)                                                                   |

Ease families are discrete choices: **stroke draws** use `power2.out` (a hand lifting at end of stroke) or `none` for constant speed — never `back.out` / `elastic.out` (pens don't bounce). **Fades** use `power1.out`.

## Critical Constraints

- **`fill: none`** for outline-only draws — otherwise the fill appears immediately.
- **Dasharray/dashoffset = the measured `getTotalLength()`**, set at setup; requires the SVG in the DOM (inline SVG is fine; a loaded `<image>` SVG is not).
- **Complex paths**: if `getTotalLength()` looks wrong, overestimate slightly (`len * 1.05`) — too large is invisible at animation start; too small clips the end.
- **Stagger multi-path draws at ~70–80%** of the previous segment's duration.
- **A drawn line must land on something.** When the path is a connector (rail, beam, underline, callout) rather than a shape, both endpoints must sit on real elements and the draw must do a job — reveal, route, validate, or emphasize. A stroke that only decorates empty space reads as filler; attach it or cut it.

## See also

`svg-icon-enrichment` (internal parts animate after the outline draws) · `counting-dynamic-scale` (stroke draws an icon while a number counts up) · `hacker-flip-3d` (logo draws, wordmark decodes beneath).


<!-- ===== FILE: hyperframes/hyperframes-animation/rules/theme-crossfade-morph.md ===== -->

---
name: theme-crossfade-morph
description: Whole-theme in-place morph under a fixed anchor — background, typography, corner radii, icons, chrome and logos all blend simultaneously (~0.3s) through N pre-styled skins while one anchor element never moves. Recipe = stacked full layers + opacity crossfade, anchor rendered once on top. Seek-safe by construction.
metadata:
  tags: theme, skin, crossfade, morph, anchor, reskin, cycle, ui, stacked-layers
---

# Theme Crossfade Morph

The whole world re-skins while one thing holds still. A composer box cycles through four IDE themes; a checkout widget flips through brand skins — background, typography, corner radii, toolbar icons, footer logos all change **at once**, in place, in ~0.3s, N times — and through every flip one anchor element (the prompt string, the widget layout, the wordmark) **never moves**. The anchor's stillness is the rhetorical claim: _everything changes, this doesn't._

Boundary: [card-morph-anchor.md](card-morph-anchor.md) morphs **one container** between two shots — its dimensions, radius, and surface tween continuously. This rule re-skins an **entire scene** through **N discrete states**: nothing tweens property-by-property (fonts, icons, and logos can't interpolate); the "morph" is a fast simultaneous crossfade of complete pre-styled layers. ([scale-swap-transition.md](scale-swap-transition.md) swaps an element at center; here the surroundings swap and the element holds.)

## How It Works

1. **One skin = one complete layer.** Each theme state is a fully pre-styled, full-bleed layer (`position: absolute; inset: 0`) containing everything that changes: background, shell/chrome, toolbar icons, footer logos, typography. All `N_SKINS` layers exist in the DOM from `t=0`, stacked; skin 0 starts visible, the rest at `opacity: 0`.
2. **The morph is a crossfade.** At each boundary, two opposing opacity tweens run at the same timeline position over `MORPH_DUR` (~0.3s): outgoing `1 → 0`, incoming `0 → 1`. Because both layers are complete, every property "blends" simultaneously for free — including the un-tweenable ones (font families, icon glyphs, logos), which read as morphing precisely because everything else is mid-blend around them.
3. **The anchor renders once, on top.** The element that must not move lives in its own layer above all skins and is **excluded from every skin layer**. No transforms, no re-parenting, no per-skin restyle.
4. **Windows are precomputed.** `T_k = CYCLE_START + k × (SKIN_HOLD + MORPH_DUR)`. Steady cadence by default; hold the final skin longest when it's the resolve.

The only animated property is `opacity` — which is why this rule is seek-safe with zero special machinery.

## Recipe

```html
<!-- inside a standard scene clip (hyperframes-core) -->
<div class="theme-stage">
  <!-- One complete pre-styled layer per skin; skin-0 visible at t=0 -->
  <div class="skin skin-0"><div class="shell">…terminal chrome, mono type, footer badge…</div></div>
  <div class="skin skin-1">
    <div class="shell">…rounded composer, sans type, toolbar pills, logo…</div>
  </div>
  <div class="skin skin-2"><div class="shell">…dark shell, its own chrome and footer…</div></div>

  <!-- The anchor: rendered ONCE, above every skin. It never moves. -->
  <div class="anchor" id="anchor">{anchorText}</div>
</div>
```

```css
.theme-stage {
  position: absolute;
  inset: 0;
}
.skin {
  position: absolute;
  inset: 0;
  opacity: 0;
  /* Each skin fully self-styled: its own background, fonts, radii,
     icons, chrome, logos. Nothing inherited across skins. */
}
.skin-0 {
  opacity: 1; /* the opening state — matches the timeline's fromTo */
}
.shell {
  /* CRITICAL: shared geometry. The shell box (and any element that
     "persists" across skins — toolbar row, footer row) sits at the SAME
     coordinates in every skin, so mid-blend frames read as one UI
     changing clothes, not two UIs ghosting. */
  position: absolute;
  left: SHELL_LEFT;
  top: SHELL_TOP;
  width: SHELL_WIDTH;
  height: SHELL_HEIGHT;
}
.anchor {
  position: absolute;
  z-index: 10; /* above every skin */
  left: ANCHOR_LEFT;
  top: ANCHOR_TOP;
  /* No transforms, no transitions — the stillness is load-bearing. */
}
```

```js
const skins = gsap.utils.toArray(".skin");

// Boundary k→k+1 at T_k: outgoing fades down as incoming fades up —
// ONE simultaneous crossfade, everything blends at once.
skins.forEach((skin, k) => {
  if (k === 0) return; // skin-0 is the opening state
  const at = CYCLE_START + k * (SKIN_HOLD + MORPH_DUR);
  tl.fromTo(skin, { opacity: 0 }, { opacity: 1, duration: MORPH_DUR, ease: "power2.inOut" }, at);
  tl.to(
    skins[k - 1],
    { opacity: 0, duration: MORPH_DUR, ease: "power2.inOut" },
    at, // same position — the blend is simultaneous, never sequential
  );
});

// The anchor gets NO tweens. Its absence from the timeline is the point.
```

## Variations

- **Anchor-typography reskin (per-layer copies)** — when the anchor's own type treatment must change with the theme (mono in the terminal skin, sans in the editor skin), each skin carries its own copy of the anchor at **pixel-identical geometry** and there is no separate top layer; the invariant shifts from "one element" to "one geometry." Verify the copies overlay exactly (screenshot two skins at 50% opacity) — a 2px baseline drift reads as the anchor flinching, which breaks the whole claim.
- **Skin-cycle tour with logo relay** — a large brand logo outside the anchored shell crossfades **in the same windows** as the skins (logo k with skin k, same `MORPH_DUR`). The paired swap sells "same product, every brand."
- **Washout finale** — after the last skin, a final low-key layer (faint dot-grid, blueprint wash) fades in while the last shell drops to ~0.25 opacity — the cycle resolves into a held diagram of itself. One extra window; the anchor may fade with the shell or hold full-strength.
- **Emphasis brake** — steady cadence for `N−1` skins, then hold the final skin 2–3× `SKIN_HOLD`; the cycle demonstrates breadth, the brake lands the resolve. Precompute the hold array; don't drift the cadence without cause.

## Values

| token           | range                                       | notes                                                                                                |
| --------------- | ------------------------------------------- | ---------------------------------------------------------------------------------------------------- |
| N_SKINS         | 3–5                                         | two is a before/after (consider `card-morph-anchor`); past five the cycle pads                       |
| SKIN_HOLD       | 0.8–1.5s                                    | long enough to register the logo/footer identity, short enough to keep the churn rhetorical          |
| MORPH_DUR       | 0.25–0.4s, ~0.3s canonical                  | faster reads as a hard cut; slower reads as a mushy dissolve with lingering double-exposure          |
| CYCLE_START     | ≥ anchor settle + a beat                    | after the anchor and skin-0 have fully registered                                                    |
| SHELL geometry  | —                                           | shell / toolbar / footer coordinates identical across skins; contents inside the slots differ freely |
| ANCHOR position | —                                           | identical to the pixel across the scene (per-layer form: identical in every skin)                    |
| washout / brake | shell ~0.2–0.3 opacity; hold 2–3× SKIN_HOLD | —                                                                                                    |

## Critical Constraints

- **The anchor never moves.** No transforms, no opacity dips, no re-parenting, no restyle — the contrast between total churn and total stillness is the entire device; one flinch and the shot becomes a slideshow.
- **Nothing tweens but `opacity`** — no `borderRadius` / `background` tweens; radii and colors change by being different in the next layer. Visibility via `opacity` only, never `display` / `visibility` toggles (they can't blend mid-fade).
- **Pixel-align the shared geometry** — mid-blend both skins are partially visible; aligned shells read as one UI changing clothes, misaligned shells ghost into two UIs.
- **Pre-style everything** — each skin is complete and static; no class toggling, no runtime restyle mid-tween.
- **Outgoing and incoming tweens share one timeline position** — a staggered blend flashes the stage background between skins.
- **Adjacent windows only** — skin k crossfades with k+1, never k+2; at no frame are three skins partially visible.
- **Camera static — always.** A push-in on top of a theme cycle destroys the stillness that makes the anchor read.
- **Hard cuts are the cheaper sibling** — if the states should _snap_, that's `discrete-text-sequence` territory; the ~0.3s blend is specifically the "morph" read.

## See also

`context-sensitive-cursor` (caret color switches at each `T_k`) · `discrete-text-sequence` (type the anchor first; or the hard-cut alternative) · `card-morph-anchor` (the single-container sibling) · `spring-pop-entrance` (the lockup that joins the anchor at the resolve) · `sine-wave-loop` (drifting field under the cycle — never on the anchor).


<!-- ===== FILE: hyperframes/hyperframes-animation/rules/vertical-spring-ticker.md ===== -->

---
name: vertical-spring-ticker
description: Slot-machine style vertical scrolling using additive spring physics within a masked container — each spring contributes one "step" of scroll.
metadata:
  tags: text, ticker, spring, scroll, vertical, slot-machine, sequence
---

# Vertical Spring Ticker (Slot Machine)

Multiple spring tweens are ADDED TOGETHER to produce total Y translation — each spring contributes one discrete "step", so instead of a single linear scroll you get the slot-machine "click click click" rhythm with natural settling. Distinct from a continuous marquee: this rule's semantics are discrete steps that land; for endless linear motion see [sine-wave-loop.md](sine-wave-loop.md).

## How It Works

A masked window of fixed height `ITEM_HEIGHT` (`overflow: hidden`) holds a vertical stack of items, each exactly `ITEM_HEIGHT` tall. Each spring holds a 0→1 progress; a shared `onUpdate` sums them and applies `translateY(-sum × ITEM_HEIGHT)`. Springs fire sequentially with overlap (`STEP_SPACING ≤ STEP_DUR`), so each step snaps in while the previous is still settling — that overlap is what makes them additive, and the `back.out` overshoot is what makes each step read as a "click".

## Recipe

```html
<!-- inside a standard scene clip (hyperframes-core) -->
<div class="ticker" id="ticker">
  <div class="stack-inner" id="stack-inner">
    <div class="item">{item0}</div>
    <div class="item">{item1}</div>
    <div class="item">{itemN}</div>
  </div>
</div>
```

```css
.ticker {
  width: TICKER_WIDTH;
  height: ITEM_HEIGHT; /* MUST match .item height exactly */
  overflow: hidden; /* the mask is the window */
}
.stack-inner {
  display: flex;
  flex-direction: column; /* mandatory — vertical stacking */
}
.item {
  height: ITEM_HEIGHT; /* MUST equal .ticker height */
  display: flex;
  align-items: center;
  justify-content: center;
  /* font-variant-numeric: tabular-nums; — for numeric tickers */
}
```

```js
const innerEl = document.getElementById("stack-inner");
const springs = Array.from({ length: STEPS }, () => ({ p: 0 }));

function applyTransform() {
  const sumP = springs.reduce((acc, s) => acc + s.p, 0);
  innerEl.style.transform = `translateY(${-sumP * ITEM_HEIGHT}px)`;
}
applyTransform(); // initial state

springs.forEach((spring, i) => {
  tl.to(
    spring,
    {
      p: 1,
      duration: STEP_DUR,
      ease: `back.out(${BOUNCE_FACTOR})`,
      onUpdate: applyTransform,
    },
    STEP_START + i * STEP_SPACING,
  );
});
```

## Variations

- **Numeric ticker (price / counter rolling)** — items are the digit sequence; run the same spring-step pattern per decimal position. `font-variant-numeric: tabular-nums` required.
- **Reverse direction (countdown)** — flip the sign (`translateY(${sumP * ITEM_HEIGHT}px)`) and arrange items in reverse order.
- **Pause between groups** — several fast steps (small `STEP_SPACING`), a long pause, then one dramatic final step with a bigger `BOUNCE_FACTOR`. The pause is where the eye locks in.
- **Continuous infinite ticker** — NOT this rule (this rule is discrete steps); a looping news ticker is a single linear tween with duplicated items — see [sine-wave-loop.md](sine-wave-loop.md) for continuous-motion semantics.

## Values

| token         | range                 | notes                                                                                 |
| ------------- | --------------------- | ------------------------------------------------------------------------------------- |
| ITEM_HEIGHT   | ~`fontSize × 1.25`    | must hold capital descenders; `.ticker` height MUST equal it exactly                  |
| TICKER_WIDTH  | 30–60% viewport width | wide enough for the longest item without ellipsis                                     |
| STEPS         | 1–4                   | number of transitions, not items; `STEPS ≤ itemCount − 1`                             |
| STEP_DUR      | 0.3–0.7s              | under 0.3 the overshoot is invisible; over 0.7 the click reads as a slide             |
| STEP_SPACING  | 0.3–0.5s              | **≤ STEP_DUR** so springs overlap (additive); wider gaps read as a lazy linear scroll |
| BOUNCE_FACTOR | 1.4–2.5               | 1.4 gentle click / 2.0 firm / 2.5+ casino spin-and-land for a climax step             |

Reference: `../examples/proof-logo-chain.html` (204px, 1 step, 0.45s).

## Critical Constraints

- **Container height = item height, pixel-exact, all items equal** — mismatches show partial item edges above/below the mask and accumulate drift across steps.
- **`overflow: hidden` on the container, not the inner stack**; `flex-direction: column` on the stack.
- **Sum the springs in `onUpdate` — never tween the final position directly.** Each spring contributing its OWN snap is the slot-machine pacing.
- **Overlap steps and keep `back.out` per step** — non-overlapping steps or an out-only ease collapse into a linear scroll.
- **Never update items via `innerHTML` between steps** — the ticker moves the SAME items via translate; swapping content shows the previous item AS the new one (broken illusion).
- **Climax dwell ≥1s after the final step** (SKILL universal constraint).
- **`tabular-nums` for numeric tickers** — variable digit widths break alignment.

## See also

`reactive-displacement` (ticker pushed by an incoming element) · `scale-swap-transition` (ticker scales out after settling) · `press-release-spring` (button press triggers the spin).


<!-- ===== FILE: hyperframes/hyperframes-animation/rules/viewport-change.md ===== -->

---
name: viewport-change
description: Virtual camera — simulate zoom / pan / focus-lock by transforming a wrapper around all scene content. Camera moves right → world translates left.
metadata:
  tags: viewport, camera, zoom, pan, focus-lock, virtual-camera
---

# Viewport Change (Virtual Camera)

Simulates camera effects (zoom / pan / focus-lock on a moving element) by transforming a wrapper around ALL scene content. The "world" moves opposite to the perceived camera. Distinct from [multi-phase-camera](multi-phase-camera.md) (2-3 discrete phases + drift) — viewport-change is a single continuous zoom/pan, often used for focus-lock following a moving element.

## How It Works

Camera intent → world transform. Camera **pans right** → world `translateX(-distance)`; camera **zooms in** → world `scale(>1)`; camera **follows element X** → world `translateX(viewportCenter - elementWorldX)` per-frame. Get the sign right or everything moves the wrong way. The single `.world` wrapper holds the camera transform; elements inside are positioned in world space, unchanged.

**Single-element composite transform (this rule's form).** Both scale and translate live on ONE wrapper as `translate(x, y) scale(S)`. CSS applies scale FIRST, then translate (right-to-left matrix composition), so a point at world offset `(ox, oy)` lands on screen at `(S × ox + x, S × oy + y)`. To map the target to viewport center, solve `S × offset + T = 0`:

```
T = -offset × S
```

This is **different from [coordinate-target-zoom](coordinate-target-zoom.md)**, which uses two nested wrappers (outer scales, inner translates) and derives `T = -offset` (independent of S). Mixing up the two forms drifts the target off-center as scale changes. Use this single-wrapper form when you want one source of truth for camera state (`cam.scale`, `cam.x`, `cam.y`) written via `onUpdate`; use nested wrappers when scale and translate can tween independently with shared ease.

## Recipe

```html
<div class="world" id="world">
  <div class="content">
    <div class="hero">{Brand}</div>
    <div class="tagline">{tagline}</div>
    <div class="cta" id="cta">{ctaUrl}</div>
  </div>
</div>
```

```css
.scene {
  overflow: hidden; /* REQUIRED — any non-1.0 scale reveals edges or pushes content off-frame */
  background: {bgGradient}; /* on .scene, NOT .world — a world-borne background warps with the camera */
}
.world {
  position: absolute;
  inset: 0;
  display: grid;
  place-items: center;
  transform-origin: 50% 50%; /* centered scaling is what the math assumes */
  will-change: transform;
}
```

```js
const world = document.getElementById("world");

// Camera state — single source of truth. The world transform is composed from
// this object in ONE place so the transform string order is stable.
const cam = { scale: 1, x: 0, y: 0 };
function applyCamera() {
  world.style.transform = `translate(${cam.x}px, ${cam.y}px) scale(${cam.scale})`;
}
applyCamera(); // seed frame 0

// Zoom in on the CTA: single-element composite transform → T = -offset × S.
// TARGET_OFFSET_Y is the target's measured offset from viewport center at
// neutral camera (sign matters — positive = below center).
const counterY = -TARGET_OFFSET_Y * TARGET_SCALE;

tl.to(
  cam,
  {
    scale: TARGET_SCALE,
    y: counterY,
    duration: ZOOM_DUR,
    ease: "power3.inOut",
    onUpdate: applyCamera,
  },
  ZOOM_START,
);
```

## Scale Value Guide

| Effect      | Scale       | Feel                                |
| ----------- | ----------- | ----------------------------------- |
| Subtle      | 1.02 - 1.05 | Barely perceptible — "professional" |
| Medium      | 1.05 - 1.15 | "Ta-da" emphasis                    |
| Noticeable  | 1.15 - 1.30 | Focus on region                     |
| Dramatic    | 1.5 - 2.5   | Element fills screen                |
| Full-screen | 3.0+        | Element covers viewport             |

Perception: < 5% scale change is imperceptible; 10-15% is comfortable emphasis; > 30% is cinematic/dramatic. For a natural product feel, prefer 1.05-1.15× over 2-3s; save big > 1.3× zooms for dramatic narrative moments.

### Extreme range — 4–12× outward (workspace reveal)

The same single-cam math runs far past the table: a zoom-out workspace reveal opens punched-in at **4–12×** on one detail (a single cell, message, or button) and pulls out to the full workspace in one continuous move. The mechanics don't change — one `cam` object, `T = -offset × S`, one `applyCamera()` writer — only the authoring direction does:

- **Build the workspace at its final (1×) layout and OPEN scaled-in** (`cam.scale = 8`, counter-translate aiming the opening detail; state it in a `fromTo` / seed via `applyCamera()` so a seek to t=0 lands punched-in). The wide landing frame is then everything at native design size — text crisp, raster assets at source resolution.
- **Never the inverse** — authoring the close-up at 1× and scaling the world down to 0.08–0.25 for the wide frame drops every label below legible pixel size and softens raster media; the reveal lands on mush.
- **Measure the opening target** — at S = 8, a 1 px error in the baked offset is 8 px on screen at the opening pose. Take the offset from the target's real laid-out center (`getBoundingClientRect` after `fonts.ready`, once at setup — the measuring doctrine in [coordinate-target-zoom.md](coordinate-target-zoom.md)), never from a layout formula.
- **The opening detail must survive ×S** — it renders at `S ×` its design size on the first frames (vector/DOM text is safe; raster needs `sourceResolution ≥ rendered × S`).

## Variations

- **Focus-lock (camera follows a moving cursor/character)** — keep the element at a fixed screen X by computing the world offset per-frame inside the driver's `onUpdate`:

```js
const focusEl = document.querySelector(".moving-cursor");
const targetScreenX = VIEWPORT_WIDTH * FOCUS_SCREEN_X_FRAC; // 0.4–0.7; 0.5 = dead center
const focusUpdate = { p: 0 };
tl.to(
  focusUpdate,
  {
    p: 1,
    duration: FOLLOW_DUR, // matches how long the focused element is in motion
    ease: "power2.inOut",
    onUpdate: () => {
      const rect = focusEl.getBoundingClientRect();
      cam.x = targetScreenX - (rect.left + rect.width / 2);
      applyCamera();
    },
  },
  FOLLOW_START,
);
```

- **Composite scale (multi-phase)** — two proxy tweens multiplied through one writer: `cam.scale = scaleUp.v * scaleDown.v; applyCamera()`. Combine a slow push-in (~1.15) with a brief release (~0.9) for a breath/punch shape.
- **Camera mode transition (centered → follow)** — crossfade two camera modes via a 0→1 weight tween; intermediate frames interpolate between the modes' offsets.

## Values

| token           | range                                | notes                                                                                       |
| --------------- | ------------------------------------ | ------------------------------------------------------------------------------------------- |
| TARGET_OFFSET_Y | measured, not a free parameter       | target's offset from viewport center at neutral camera; measure via `getBoundingClientRect` |
| TARGET_SCALE    | 1.3× modest → 1.6–2.0× typical → 3×+ | raster media needs `sourceResolution ≥ rendered × TARGET_SCALE`                             |
| ZOOM_START      | content landed + ~0.5s scan time     | let the viewer read before the camera moves                                                 |
| ZOOM_DUR        | 1.0–2.0s                             | under 0.8s teleports, over 2.5s drags                                                       |
| DWELL           | ≥ 1.0s after the zoom settles        | the viewer must be able to read the focal point (climax dwell)                              |
| VIEWPORT_WIDTH  | = the root's `data-width`            | real value, not abstract                                                                    |

## Critical Constraints

- **One `.world` wrapper carries the whole camera** — every scene element lives inside it; a second transformed wrapper is a second camera.
- **Single source of truth via the `cam` object + `applyCamera()`** — when scale and translate both change, write them in ONE place; never split them across tweens that touch `world.style.transform` directly (the transform string composition order becomes unpredictable).
- **Single-wrapper counter-translate is `T = -offset × S`** — don't import the nested-wrapper `T = -offset` formula.
- **`overflow: hidden` on `.scene`**; **`transform-origin: 50% 50%` on `.world`**; **background on `.scene`, never on `.world`**.

## See also

[coordinate-target-zoom.md](coordinate-target-zoom.md) (nested-wrapper alternative, `T = -offset`) · [multi-phase-camera.md](multi-phase-camera.md) (viewport-change inside one phase) · [sine-wave-loop.md](sine-wave-loop.md) (idle micro-drift after the viewport settles).


<!-- ===== FILE: hyperframes/hyperframes-animation/rules/waterfall-entry.md ===== -->

---
name: waterfall-entry
description: Staggered ARRIVAL cascade — words/elements whip in from below (one consistent direction), each starting before the previous settles, an accelerating wave that resolves into a composed layout. Title cards, segment openers, list/feature intros. Opacity is BINARY 0→1 via tl.set — never fade an arrival.
metadata:
  tags: entrance, cascade, stagger, kinetic-text, title-card, segment-opener, arrival, waterfall, whip
---

# Waterfall Entry

Staggered ARRIVAL cascade: words/elements whip in from below (one consistent direction),
each starting before the previous settles — an accelerating wave that resolves into a
composed layout. Title cards, segment openers, list/feature intros.

**This is an in-scene arrival, not a seam.** Its seam sibling is the waterfall CUT
(`cut-the-curve` doctrine skill, `seams/waterfall-cut.md`); do not mix their rules:

|               | Entry (this rule — arrival)                   | Waterfall Cut (seam)                                      |
| ------------- | --------------------------------------------- | --------------------------------------------------------- |
| Opacity       | BINARY 0→1 via `tl.set` at entry — never fade | ignites at 0.35 mid-path — the fade IS the velocity trick |
| Axis default  | Y, from below                                 | X, riding the current                                     |
| Outgoing side | none                                          | words ramp out on mirrored power4.in                      |

## Choreography

- **Overlap, don't queue** — next element starts within ±2 frames of the previous
  settling; gaps SHRINK across the cascade; the last element snaps.
- **Velocity varies by weight** — heavy/anchor elements travel further and longer;
  light words/punctuation snap in tight:

| Parameter | Anchor/heavy | Normal word | Light/punctuation |
| --------- | ------------ | ----------- | ----------------- |
| Y offset  | 60–80px      | 40–50px     | 30–48px           |
| Duration  | 0.16–0.20s   | 0.13–0.16s  | 0.10–0.13s        |
| Overlap   | 0–2f gap     | 1f overlap  | 1–2f overlap      |

- Ease `power4.out` (`expo.out` for extra snap); never `.inOut` on an entry.
- One direction per cascade.
- Split the FINAL word into fragments to extend the climax; fragments travel further.
- Post-settle, the group usually slides to make room for the next beat — that's
  [nudge-curve.md](nudge-curve.md).

## JS

Each element: `tl.set` (instant reveal + offset) then `tl.to` (whip to rest).
`nextStart = prevStart + prevDuration − (overlapFrames × F)`; +overlap = cascade,
−overlap = deliberate gap. CSS: elements start `opacity: 0; display: inline-block`.

```js
var F = 1 / 60;
var t0 = 0.1;
// anchor (heaviest): biggest travel, longest settle
tl.set("#el-1", { opacity: 1, y: 80 }, t0);
tl.to("#el-1", { y: 0, duration: 0.18, ease: "power4.out" }, t0);
// normal word: 2 frames after the anchor finishes
var t1 = t0 + 0.18 + 2 * F;
tl.set("#el-2", { opacity: 1, y: 45 }, t1);
tl.to("#el-2", { y: 0, duration: 0.15, ease: "power4.out" }, t1);
// light word: 1 frame BEFORE the previous finishes (overlap)
var t2 = t1 + 0.15 - F;
tl.set("#el-3", { opacity: 1, y: 40 }, t2);
tl.to("#el-3", { y: 0, duration: 0.14, ease: "power4.out" }, t2);
// split final-word fragments: tightest overlap, extra travel (lighter)
var t3 = t2 + 0.14 - F;
tl.set("#frag-a", { opacity: 1, y: 70 }, t3);
tl.to("#frag-a", { y: 0, duration: 0.16, ease: "power4.out" }, t3);
var t4 = t3 + 0.14 - F;
tl.set("#frag-b", { opacity: 1, y: 70 }, t4);
tl.to("#frag-b", { y: 0, duration: 0.15, ease: "power4.out" }, t4);
// punctuation: lightest, fastest
var t5 = t4 + 0.13 - 2 * F;
tl.set("#dot", { opacity: 1, y: 48 }, t5);
tl.to("#dot", { y: 0, duration: 0.12, ease: "power4.out" }, t5);
```

## Anti-patterns

| Don't                                                  | Instead                                                                           |
| ------------------------------------------------------ | --------------------------------------------------------------------------------- |
| Queued entries (each waits for the previous to settle) | Overlap ±1–2 frames — the cascade is a wave, not a queue                          |
| Same offset/duration for every cascade element         | Vary by weight: anchors travel further, punctuation snaps                         |
| Gradual opacity fade on an arrival                     | Binary 0→1 via `tl.set` — fading fights the snap (seam cuts fade; arrivals don't) |


<!-- ===== FILE: hyperframes/hyperframes-animation/techniques.md ===== -->

# Visual Techniques Reference

13 proven techniques from production HyperFrames videos. Use these in your storyboard and compositions to create visually rich, professional output. Each technique includes a minimal code pattern you can adapt.

These are NOT advanced — they're standard motion design patterns that every composition should use at least 2-3 of.

## Contents

- SVG path drawing
- Canvas 2D procedural art
- CSS 3D transforms
- Per-word kinetic typography
- Lottie animation
- Video compositing
- Character-by-character typing
- Variable font axis animation
- GSAP MotionPathPlugin
- Velocity-matched transitions
- Audio-reactive animation
- Clip-path reveal masks
- WebGL fragment shader art
- When to use what

> **Capturing live HTML/CSS as a GPU texture** (3D rotation + bloom, magnetic warp, shatter, liquid surface, portal, plus GLSL post-processing) is a separate, heavier capability — see `adapters/html-in-canvas-patterns.md`. Use it for 1–3 hero beats per video, not every beat.
>
> **Easing vocabulary** — the full ease-family palette (character + mood mapping) lives in `adapters/gsap-easing-and-stagger.md`. Every composition should use at least 3 different easings.
>
> **Named text-animation effects** (24 IDs like `typewriter`, `kinetic-center-build`, `soft-blur-in`) come from the external `animate-text` skill — see `adapters/animate-text.md` for the vocabulary and how to load it.

---

## 1. SVG Path Drawing

A path draws itself in real-time, like someone tracing with a pen. Use for revealing diagrams, arrows, connector lines, or brand marks.

```html
<svg viewBox="0 0 400 200">
  <path
    class="draw-path"
    d="M 50 100 L 200 50 L 350 100"
    stroke="#c84f1c"
    stroke-width="4"
    fill="none"
    stroke-linecap="round"
  />
</svg>
<style>
  .draw-path {
    stroke-dasharray: 280;
    stroke-dashoffset: 280;
  }
</style>
<script>
  tl.to(".draw-path", { strokeDashoffset: 0, duration: 0.7, ease: "power2.out" }, 0.5);
</script>
```

Use `path.getTotalLength()` to calculate the dasharray value dynamically.

---

## 2. Canvas 2D Procedural Art

Animated noise, particle fields, data visualizations — anything that evolves frame-by-frame. Drive it with a GSAP proxy.

```html
<canvas id="proc-canvas" width="1920" height="1080"></canvas>
<script>
  var canvas = document.getElementById("proc-canvas");
  var ctx = canvas.getContext("2d");

  function hash(x, y) {
    var n = x * 374761393 + y * 668265263;
    n = (n ^ (n >> 13)) * 1274126177;
    return ((n ^ (n >> 16)) & 0x7fffffff) / 0x7fffffff;
  }

  function drawFrame(t) {
    ctx.fillStyle = "#0a0a0a";
    ctx.fillRect(0, 0, 1920, 1080);
    for (var i = 0; i < 200; i++) {
      var x = hash(i, 0) * 1920;
      var y = hash(i, 1) * 1080;
      var brightness = hash(i, Math.floor(t * 10)) * 255;
      ctx.fillStyle = "rgba(255, 255, 255, " + brightness / 255 + ")";
      ctx.beginPath();
      ctx.arc(x, y, 2, 0, Math.PI * 2);
      ctx.fill();
    }
  }

  var proxy = { time: 0 };
  tl.to(
    proxy,
    {
      time: 5,
      duration: 5,
      ease: "none",
      onUpdate: function () {
        drawFrame(proxy.time);
      },
    },
    0,
  );
</script>
```

The `hash()` function is deterministic — same frame renders identically every time.

---

## 3. CSS 3D Transforms

Perspective rotations create depth. Use for product showcases, card flips, architectural reveals.

```html
<div class="stage" style="perspective: 900px;">
  <div class="card-3d" style="transform-style: preserve-3d;">
    <div class="face front">Product</div>
    <div class="face back" style="transform: rotateY(180deg);">Details</div>
  </div>
</div>
<script>
  tl.to(".card-3d", { rotationY: 360, rotationX: 15, duration: 1.2, ease: "sine.inOut" }, 0);
</script>
```

Always set `perspective` on the parent, `transform-style: preserve-3d` on the animated element.

---

## 4. Per-Word Kinetic Typography

Words appear one-by-one, synced to transcript.json timestamps. The core technique for narration-driven videos.

```html
<div class="headline">
  <span class="word w-0">Anything</span>
  <span class="word w-1">a</span>
  <span class="word w-2">browser</span>
  <span class="word w-3">can</span>
  <span class="word w-4">render</span>
</div>
<style>
  .word {
    display: inline-block;
    opacity: 0;
    margin: 0 0.12em;
  }
</style>
<script>
  // Word onset times from transcript.json (seconds relative to beat start)
  var timings = [0.0, 0.23, 0.28, 0.63, 0.78];
  var slides = [80, 60, 50, 25, 12]; // horizontal slide decay (px)

  document.querySelectorAll(".word").forEach(function (word, i) {
    tl.from(
      word,
      {
        x: slides[i],
        y: 14,
        opacity: 0,
        duration: 0.35,
        ease: "power2.out",
      },
      timings[i],
    );
  });
</script>
```

The slide distance DECAYS per word (80→12px) — mimics a camera settling.

---

## 5. Lottie Animation

Vector animations that play inside a composition. Use for logos, character animations, icons.

```html
<div id="logo-anim" class="lottie" style="width:500px;height:500px;"></div>
<script src="https://cdnjs.cloudflare.com/ajax/libs/bodymovin/5.12.2/lottie.min.js"></script>
<script>
  window.__hfLottie = window.__hfLottie || [];

  const anim = lottie.loadAnimation({
    container: document.getElementById("logo-anim"),
    renderer: "svg",
    loop: false,
    autoplay: false,
    path: "../capture/assets/lottie/animation-0.json",
  });
  window.__hfLottie.push(anim); // REQUIRED — adapter seeks every registered instance

  gsap.set("#logo-anim", { scale: 0.3, opacity: 0 });
  tl.to("#logo-anim", { scale: 1, opacity: 1, duration: 0.35, ease: "back.out(1.6)" }, 0.2);
</script>
```

`autoplay: false` + `window.__hfLottie.push()` are mandatory — HyperFrames seeks each registered player to composition time, so a player left on `autoplay` runs in wall-clock and renders non-deterministically. `loop: true` is seek-safe: the adapter wraps composition time into the animation's own length, so a short cycle repeats for the whole scene. There is no playback-rate scaling: bake non-default speed into the Lottie asset. Characters (walk cycles, mascots, gestures) and the full `.lottie`/dotLottie contract: `adapters/lottie.md`.

---

## 6. Video Compositing

Embed real video footage inside compositions. Videos are `playsinline`; add `muted` for silent footage or b-roll, or `data-has-audio="true"` when the clip's own sound should play.

```html
<div class="video-frame" style="width:680px;height:840px;border-radius:16px;overflow:hidden;">
  <video
    id="footage"
    src="../capture/assets/videos/clip.mp4"
    muted
    playsinline
    style="width:100%;height:100%;object-fit:cover;"
  ></video>
</div>
<script>
  // Video playback is controlled by the framework — don't call play() manually
  tl.from(".video-frame", { scale: 0.9, opacity: 0, duration: 0.3, ease: "power2.out" }, 0);
</script>
```

The HyperFrames runtime handles video seeking and playback.

---

## 7. Character-by-Character Typing

Terminal typing effect using `tl.call()` to update text content character by character.

```html
<div class="terminal-line">
  <span class="prompt">❯</span>
  <span class="typed" id="typed-text"></span>
  <span class="cursor" style="width:11px;height:22px;background:#333;display:inline-block;"></span>
</div>
<script>
  var CMD = "npx hyperframes init";
  var typed = document.getElementById("typed-text");

  // Cursor blinks
  tl.to(".cursor", { opacity: 0, duration: 0.12, yoyo: true, repeat: 20, ease: "steps(1)" }, 0);

  // Type each character
  for (var i = 0; i < CMD.length; i++) {
    (function (idx) {
      tl.call(
        function () {
          typed.textContent = CMD.substring(0, idx + 1);
        },
        null,
        (idx / CMD.length) * 0.9,
      );
    })(i);
  }
</script>
```

Use `ease: "steps(1)"` for cursor blink — creates discrete on/off.

---

## 8. Variable Font Axis Animation

Animate font-variation-settings to reshape glyphs in real-time. Works with variable fonts that have axes like optical size (opsz), weight (wght), softness (SOFT).

```html
<style>
  /* Load the captured local variable font — do NOT use Google Fonts @import.
     Replace this placeholder with an @font-face pointing to ../capture/assets/fonts/. */
  @font-face {
    font-family: "Fraunces";
    src: url("../capture/assets/fonts/Fraunces-Variable.woff2") format("woff2");
    font-weight: 100 900;
    font-style: normal;
    font-display: block;
  }
  .wordmark {
    --opsz: 144;
    --wght: 440;
    font-family: "Fraunces", serif;
    font-variation-settings:
      "opsz" var(--opsz),
      "wght" var(--wght);
    font-size: 200px;
  }
</style>
<script>
  tl.to(".wordmark", { "--opsz": 72, "--wght": 300, duration: 0.45, ease: "power2.out" }, 0);
</script>
```

The glyph subtly reshapes as axes animate — optical size adjusts detail, weight changes thickness.

---

## 9. GSAP MotionPathPlugin

Animate an element along an arbitrary SVG path. Use for sliders following curves, particles along trajectories, guided reveals.

```html
<script src="https://cdn.jsdelivr.net/npm/gsap@3.14.2/dist/MotionPathPlugin.min.js"></script>
<div class="dot" style="width:20px;height:20px;background:#2a8a7c;border-radius:50%;"></div>
<script>
  gsap.registerPlugin(MotionPathPlugin);
  tl.to(
    ".dot",
    {
      motionPath: { path: "M 12 300 C 280 280 520 80 820 50 S 1200 48 1308 38" },
      duration: 1.5,
      ease: "power2.out",
    },
    0,
  );
</script>
```

---

## 10. Velocity-Matched Transitions

Exit one beat and enter the next with matched velocities — creates perceived continuous motion.

```javascript
// EXIT (in outgoing composition): accelerating with blur
tl.to(
  ".content",
  {
    y: -150,
    filter: "blur(30px)",
    opacity: 0,
    duration: 0.33,
    ease: "power2.in", // accelerates
  },
  beatDuration - 0.33,
);

// ENTRY (in incoming composition): decelerating from blur
gsap.set(".content", { y: 150, filter: "blur(30px)" });
tl.to(
  ".content",
  {
    y: 0,
    filter: "blur(0px)",
    duration: 1.0,
    ease: "power2.out", // decelerates
  },
  0,
);
```

The fastest point of both curves meets at the cut — the viewer perceives smooth camera motion. Match ease families: `.in` for exits, `.out` for entries.

---

## 11. Audio-Reactive Animation

Drive any GSAP-tweenable property from the playing audio. Bass pulses a logo on kick drums. Treble glows a CTA on cymbals. Amplitude breathes a background during quiet phrases. The result: motion that feels locked to the track in a way pre-authored tweens never can.

**When to use:** Any video with music or dramatic narration — brand reels, product launches, hype edits. Skip for calm/tutorial pacing.

**How it works:** Pre-extract audio frequency bands into a JSON file, then sample per-frame via `tl.call()`:

```js
// audio-data.json: { fps: 30, totalFrames: 900, frames: [{ bands: [0.82, 0.45, 0.31, ...] }, ...] }
for (var f = 0; f < AUDIO_DATA.totalFrames; f++) {
  tl.call(
    (function (frame) {
      return function () {
        var bass = frame.bands[0]; // 0–1
        var treble = frame.bands[13];
        gsap.set(".logo", { scale: 1 + bass * 0.04 }); // 3–4% pulse on bass
        gsap.set(".cta", { filter: `drop-shadow(0 0 ${treble * 24}px #00C3FF)` });
      };
    })(AUDIO_DATA.frames[f]),
    [],
    f / AUDIO_DATA.fps,
  );
}
```

Per-frame sampling is required — a single tween will not react. Use the extract script:

```bash
python3 skills/hyperframes-creative/scripts/extract-audio-data.py narration.wav --fps 30 --bands 16 -o audio-data.json
```

Keep text/logo intensity subtle (≤5% scale, ≤30% glow) — audio-reactive motion on tiny elements reads as jitter. Bigger backgrounds can push to 10–30%.

**Never do:** equalizer bars, spectrum analyzers, waveform displays, strobing, rainbow color cycling. The audio provides _timing and intensity_; the visual vocabulary still comes from the brand. See `skills/hyperframes-creative/references/audio-reactive.md` for the full API and anti-patterns.

---

## 12. Clip-Path Reveal Masks

A fixed window that content slides through — text or images enter from one side and are clipped by an invisible boundary. Different from SVG path drawing: the mask is static, the content moves.

```html
<div id="reveal-mask">
  <div id="reveal-content">Your headline text here</div>
</div>
<style>
  #reveal-mask {
    position: absolute;
    inset: 0;
    clip-path: inset(0 200px 0 0); /* clips 200px from right */
    display: flex;
    align-items: center;
    justify-content: center;
  }
  #reveal-content {
    font-size: 108px;
    white-space: nowrap;
  }
</style>
<script>
  // Content starts offscreen right, slides left through the mask window
  gsap.set("#reveal-content", { x: 400, opacity: 0 });
  tl.to("#reveal-content", { x: 0, opacity: 1, duration: 1, ease: "power2.out" }, 0);
</script>
```

Variations: `clip-path: circle(0% at 50% 50%)` → `circle(100%)` for iris reveals. `clip-path: polygon(...)` for custom shapes.

### Text masks need room for glyphs

A line box is not the full painted extent of its text. With tight display typography (`line-height: 1` or less), an `overflow: hidden` line mask can cut descenders (`g`, `p`, `y`, `j`) and accents or umlauts even after the entrance has finished.

Give the mask block padding and a compensating negative margin. Set the typography on the mask and inherit it on the line so the padding's `em` units use the text's font size:

```html
<div class="line-mask">
  <div class="line">Betreuung</div>
</div>
<style>
  .line-mask {
    font-size: 200px;
    line-height: 1;
    overflow: hidden;
    padding-block: 0.2em;
    margin-block: -0.2em;
  }
  .line-mask > .line {
    margin: 0;
    font: inherit;
    white-space: nowrap;
  }
</style>
```

Treat `0.2em` as a starting point: verify the actual font, weight, and text at a settled frame, including descenders and accented capitals. Keep the initial displaced line outside the enlarged mask so it remains hidden before the reveal. If the mask is no longer needed after the entrance, another option is to release its clipping properties (`overflow: visible` / `clip-path: none`) with `tl.set(...)` at the settle time.

`data-layout-allow-overflow` suppresses overflow checks for the marked element and its descendants throughout the timeline, including the resting state. A passing `hyperframes check` does not establish that the glyphs are intact; inspect a settled snapshot of the mask before considering the reveal complete.

---

## 13. WebGL Fragment Shader Art

Full GPU generative backgrounds — domain-warped FBM noise, cosine palette coloring, iridescent organic patterns. Far richer than Canvas 2D.

```html
<canvas id="shader-bg" width="1920" height="1080"></canvas>
<script>
  var canvas = document.getElementById("shader-bg");
  var gl = canvas.getContext("webgl");
  if (!gl) {
    /* fallback to gradient */
  }

  var fsrc = `
    precision mediump float;
    varying vec2 v_uv;
    uniform float u_time;
    uniform vec2 u_res;

    float hash(vec2 p) { return fract(sin(dot(p, vec2(127.1, 311.7))) * 43758.5453); }
    float noise(vec2 p) {
      vec2 i = floor(p), f = fract(p);
      f = f * f * (3.0 - 2.0 * f);
      return mix(mix(hash(i), hash(i+vec2(1,0)), f.x),
                 mix(hash(i+vec2(0,1)), hash(i+vec2(1,1)), f.x), f.y);
    }
    float fbm(vec2 p) {
      float v = 0.0, a = 0.5;
      mat2 R = mat2(0.8, 0.6, -0.6, 0.8);
      for (int i = 0; i < 5; i++) { v += a*noise(p); p = R*p*2.02; a *= 0.5; }
      return v;
    }
    vec3 palette(float t) {
      return vec3(0.5)+vec3(0.5)*cos(6.28318*(vec3(1)*t+vec3(0.0,0.33,0.67)));
    }
    void main() {
      vec2 uv = v_uv; uv.x *= u_res.x/u_res.y;
      float t = u_time * 0.4;
      vec2 q = vec2(fbm(uv*3.0+t*0.3), fbm(uv*3.0+vec2(5.2,1.3)+t*0.2));
      vec2 r = vec2(fbm(uv*3.0+q*4.0+vec2(1.7,9.2)+t*0.15), fbm(uv*3.0+q*4.0+vec2(8.3,2.8)+t*0.1));
      float n = fbm(uv*3.0+r*2.0);
      vec3 col = palette(n*2.0+t*0.2);
      col = mix(col, palette(length(q)*3.0+t*0.1), 0.4);
      col *= 0.7+0.3*n;
      float vig = 1.0-0.4*length(v_uv-0.5);
      gl_FragColor = vec4(col*vig, 1.0);
    }
  `;

  // Compile, link, set up fullscreen quad, then render via GSAP proxy:
  var proxy = { time: 0.5 };
  tl.to(
    proxy,
    {
      time: 5,
      duration: BEAT_DUR,
      ease: "none",
      onUpdate: function () {
        gl.uniform1f(uTime, proxy.time);
        gl.drawArrays(gl.TRIANGLE_STRIP, 0, 4);
      },
    },
    0,
  );
</script>
```

Always include a Canvas 2D gradient fallback for environments without WebGL.

---

## When to Use What

| Video energy                   | Techniques to combine                                           |
| ------------------------------ | --------------------------------------------------------------- |
| High impact (launches, promos) | Per-word typography + velocity transitions + counter animations |
| Cinematic (tours, stories)     | SVG path drawing + video compositing + 3D transforms            |
| Technical (dev tools, APIs)    | Character typing + Canvas 2D procedural + MotionPath            |
| Premium (luxury, enterprise)   | Variable font animation + Lottie + slow velocity transitions    |
| Data-driven (stats, metrics)   | Canvas 2D procedural + counter animations + SVG path drawing    |


<!-- ===== FILE: hyperframes/hyperframes-animation/transitions/TRANSITION-REGISTRY.md ===== -->

# Transition Registry — machine source of truth

Single source of truth for **PLV scene-to-scene transitions**. The deterministic
injector (`product-launch-video/scripts/transitions.mjs inject`) reads its vendored
copy of the JSON block below (`product-launch-video/scripts/lib/transitions.json`)
and stamps the matching `gsap_template` onto the master timeline.
The planner (`product-launch-video/references/story-design.md`) names a transition
by its `name` in each frame's `transition_in`; everything else is harness.

This file is **not** the catalog of all transitions — that is `catalog.md` +
`css-*.md` (≈40 CSS + shader). This registry is the curated subset that is
**Tier-B-ready**: pure transform / opacity / filter on the two scene **clip
wrappers** (`#el-<sid>`), no injected overlay DOM, no per-scene cooperation.
Overlay families (staggered blocks, blinds, light leak, grid dissolve, page
burn) and shader transitions are deferred to later phases.

## How the injector applies a transition

At a `break` boundary between scene _i_ (`from`) and scene _i+1_ (`to`), the
injector:

1. Extends `#el-<from>` wrapper `data-duration` by `duration_s` (holds its final
   frame — verified: `core/src/runtime/init.ts:1393-1410` external-slot branch).
2. Pulls `#el-<to>` wrapper `data-start` earlier by `duration_s` (creates the
   overlap window).
3. Reassigns **all** clip `data-track-index` as a 0/1 ping-pong so the two
   overlapping wrappers never share a track (a readability convention, not a
   render constraint,
   `core/src/lint/rules/composition.ts`). Higher track composites on top.
4. Stamps the `gsap_template` into `window.__timelines["main"]` at `T = overlap-start`.

Verified by prototype render (2026-05-31): the master-timeline wrapper tween is
seeked and rendered (no double-seek with the sub-comp's own paused timeline —
the runtime drives them independently), the extended wrapper holds scene _i_'s
final frame, and the higher-track incoming wrapper composites over + blends with
the outgoing one.

## Template placeholders

The injector substitutes these tokens in each `gsap_template` line:

| Token                              | Meaning                                                                  |
| ---------------------------------- | ------------------------------------------------------------------------ |
| `__OLD__`                          | `"#el-<from>"` — outgoing clip wrapper selector (quoted)                 |
| `__NEW__`                          | `"#el-<to>"` — incoming clip wrapper selector (quoted)                   |
| `__T__`                            | overlap-start time in seconds (master clock)                             |
| `__DUR__`                          | `duration_s` for this boundary                                           |
| `__DX__`                           | horizontal travel for directional types: `-1920` (LEFT) / `1920` (RIGHT) |
| `__DY__`                           | vertical travel: `-1080` (UP) / `1080` (DOWN)                            |
| `__ORIGIN_OUT__` / `__ORIGIN_IN__` | transformOrigin pair for `squeeze`                                       |

`filter` / `scaleX` / `transformOrigin` are lint-clean on the master timeline
(verified: `core/src/lint/rules/gsap.ts` has no per-property whitelist and scopes
its checks to `data-composition-id` ranges; the x/y/scale/rotation/opacity
whitelist is a _scene-worker_ prompt rule only — it does not bind index.html).

## Registry

```json
{
  "transitions": [
    {
      "name": "crossfade",
      "tier": "b",
      "overlay": false,
      "energy": "any",
      "default_duration_s": 0.5,
      "directions": [],
      "source": "css-dissolve.md",
      "gsap_template": [
        "tl.to(__OLD__, { opacity: 0, duration: __DUR__, ease: \"power2.inOut\" }, __T__);",
        "tl.fromTo(__NEW__, { opacity: 0 }, { opacity: 1, duration: __DUR__, ease: \"power2.inOut\" }, __T__);"
      ]
    },
    {
      "name": "blur-crossfade",
      "tier": "b",
      "overlay": false,
      "energy": "calm",
      "default_duration_s": 0.6,
      "directions": [],
      "source": "css-dissolve.md",
      "note": "Default when the two scenes' #root backgrounds differ a lot — the blur masks the background-color clash a plain crossfade would expose.",
      "gsap_template": [
        "tl.to(__OLD__, { filter: \"blur(10px)\", scale: 1.03, opacity: 0, duration: __DUR__, ease: \"power2.inOut\" }, __T__);",
        "tl.fromTo(__NEW__, { filter: \"blur(10px)\", scale: 0.97, opacity: 0 }, { filter: \"blur(0px)\", scale: 1, opacity: 1, duration: __DUR__, ease: \"power2.inOut\" }, __T__);"
      ]
    },
    {
      "name": "push-slide",
      "tier": "b",
      "overlay": false,
      "energy": "medium",
      "default_duration_s": 0.5,
      "directions": ["LEFT", "RIGHT", "UP", "DOWN"],
      "default_direction": "LEFT",
      "source": "css-push.md",
      "note": "Directional. The injector picks __DX__/__DY__ from the direction and emits the horizontal OR vertical pair (not both).",
      "gsap_template_horizontal": [
        "tl.to(__OLD__, { x: __DX__, duration: __DUR__, ease: \"power3.inOut\" }, __T__);",
        "tl.fromTo(__NEW__, { x: __DXIN__, opacity: 1 }, { x: 0, opacity: 1, duration: __DUR__, ease: \"power3.inOut\" }, __T__);"
      ],
      "gsap_template_vertical": [
        "tl.to(__OLD__, { y: __DY__, duration: __DUR__, ease: \"power3.inOut\" }, __T__);",
        "tl.fromTo(__NEW__, { y: __DYIN__, opacity: 1 }, { y: 0, opacity: 1, duration: __DUR__, ease: \"power3.inOut\" }, __T__);"
      ]
    },
    {
      "name": "zoom-through",
      "tier": "b",
      "overlay": false,
      "energy": "high",
      "default_duration_s": 0.4,
      "directions": [],
      "source": "css-scale.md",
      "gsap_template": [
        "tl.to(__OLD__, { scale: 2.5, opacity: 0, filter: \"blur(8px)\", duration: __DUR__, ease: \"power3.in\" }, __T__);",
        "tl.fromTo(__NEW__, { scale: 0.5, opacity: 0, filter: \"blur(8px)\" }, { scale: 1, opacity: 1, filter: \"blur(0px)\", duration: __DUR__, ease: \"power3.out\" }, __T__);"
      ]
    },
    {
      "name": "squeeze",
      "tier": "b",
      "overlay": false,
      "energy": "medium",
      "default_duration_s": 0.4,
      "directions": [],
      "source": "css-push.md",
      "note": "Old compresses to a vertical line on the left edge; new expands from the right edge. Incoming starts off (scaleX 0) so its higher-track stacking is harmless.",
      "gsap_template": [
        "tl.to(__OLD__, { scaleX: 0, transformOrigin: \"left center\", duration: __DUR__, ease: \"power3.inOut\" }, __T__);",
        "tl.fromTo(__NEW__, { scaleX: 0, transformOrigin: \"right center\", opacity: 1 }, { scaleX: 1, transformOrigin: \"right center\", opacity: 1, duration: __DUR__, ease: \"power3.inOut\" }, __T__);"
      ]
    }
  ],
  "tier_a_types": ["morph", "shared-element"],
  "default_high_energy": "zoom-through",
  "default_calm": "blur-crossfade",
  "max_duration_s": 2.0
}
```

## Default-derivation (used by prep.mjs when the planner omits `**Transition:**`)

A `break` boundary with no named transition gets a default:

1. If the incoming scene's creative brief reads HIGH energy (explosive / kinetic /
   frenetic keywords), use `default_high_energy` (`zoom-through`).
2. Otherwise use `default_calm` (`blur-crossfade`) — the universal default. The
   blur masks any background shift and reads intentional, which keeps the whole
   video to ~2 transition types (the "repeat 2-3" principle).

## Choosing as a planner (the only agent touchpoint)

Pick **2-3 types for the whole video** and repeat them — repetition is what reads
as professional (see `overview.md`). This budget counts the **Tier-B between-scene
types only** (the 5 in the registry above); the Tier-A `shared-element` morph is a
worker-authored bridge driven by narrative `intent: morph` — it is **exempt and
does not count** toward the 2-3. Name the entering transition on each scene:

```
**Transition:** blur-crossfade
**Transition:** push-slide LEFT
**Transition:** zoom-through 0.3s
```

Omit the anchor to accept the default above. Do NOT write GSAP, touch timing, or
edit index.html — the harness stamps the code, computes the overlap, and assigns
tracks.


<!-- ===== FILE: hyperframes/hyperframes-animation/transitions/catalog.md ===== -->

# Transition Catalog

Hard rules, scene template, and routing to implementation code. Read the reference file for the transition type you need — don't load all of them.

## Contents

- Hard rules for CSS transitions
- Shader transitions
- Scene template
- CSS transition examples
- Shader transition routing

## Hard Rules (CSS)

These cause real bugs if violated.

**Scene visibility:** Scene 1 visible by default (no `opacity: 0`). Scenes 2+ have `opacity: 0` on the CONTAINER div. GSAP reveals them. No visibility shim (`timedEls`).

**Fonts:** Just write the `font-family` you want — the compiler embeds supported fonts automatically via `@font-face` with inline data URIs. No need for `<link>` tags or `@import`. Works in all contexts including sandboxed iframes.

**Element structure:** No `class="clip"` on scene divs in standalone compositions. Only the root div gets `data-composition-id`/`data-start`/`data-duration`.

**Overlay elements:** Staggered blocks = full-screen 1920x1080, NOT thin strips. Glitch RGB overlays = normal blending at 35% opacity, NOT `mix-blend-mode: multiply` (invisible on dark backgrounds). Light leak overlays = larger than the frame (2400px+), never a visible shape. Overexposure = use `filter: brightness()` on the scene, not just a white overlay.

**VHS tape:** Clone actual scene content with `cloneNode(true)`, NOT colored bars. Each strip: wider than frame (2020px at left:-50px). Red+blue chromatic copies at z-index above main strip. Seeded PRNG for deterministic random offsets.

**Z-index:** Gravity drop, zoom out, diagonal split need outgoing scene ON TOP (`zIndex: 10`) so it exits while revealing the new scene behind (`zIndex: 1`).

**Page burn:** Content burns with the page — no falling debris. Hide scene1 via `tl.set` at burn end, NEVER `onComplete` (not reversible). `onUpdate` must restore `clipPath: "none"` when `wp <= 0` for rewind support. Incoming scene fades from black at 90% through burn.

**Clock wipe:** 9-point polygon with intermediate edge positions. Step through 4 quadrants with separate tweens.

**Grid dissolve:** Cycle 5 palette colors per cell, not monochrome.

**Blinds count by energy:** Calm: 4h/6v. Medium: 6-8h/8v. High: 12-16h/16v.

**Don't use:** Star iris (polygon interpolation broken), tilt-shift (no selective CSS blur), lens flare (visible shape, not optical), hinge/door (distorts too fast).

## Shader Transitions

Shader setup, WebGL init, capture, and fragment shaders are handled by `@hyperframes/shader-transitions` (`packages/shader-transitions/`). Read the package source for API details. Compositions using shaders must follow the shader-compatible CSS rules in `overview.md` (this directory).

## Scene Template

```html
<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <script src="https://cdn.jsdelivr.net/npm/gsap@3.14.2/dist/gsap.min.js"></script>
    <style>
      body {
        margin: 0;
        width: 1920px;
        height: 1080px;
        overflow: hidden;
        background: #000;
        font-family: "YOUR FONT", sans-serif; /* compiler embeds supported fonts automatically */
      }
      .scene {
        position: absolute;
        top: 0;
        left: 0;
        width: 1920px;
        height: 1080px;
        overflow: hidden;
      }
      #scene1 {
        z-index: 1;
        background: #color;
      }
      #scene2 {
        z-index: 2;
        background: #color;
        opacity: 0;
      }
    </style>
  </head>
  <body>
    <div
      id="root"
      data-composition-id="main"
      data-width="1920"
      data-height="1080"
      data-start="0"
      data-duration="TOTAL"
    >
      <div id="scene1" class="scene"><!-- visible --></div>
      <div id="scene2" class="scene"><!-- hidden --></div>
    </div>
    <script>
      window.__timelines = window.__timelines || {};
      var tl = gsap.timeline({ paused: true });
      // Transition code here
      window.__timelines["main"] = tl;
    </script>
  </body>
</html>
```

Every transition follows: position new scene → animate outgoing → swap → animate incoming → clean up overlays.

## CSS Transitions

All code examples use `old` for the outgoing scene-inner selector and `new` for the incoming, with `T` as the transition start time. Read the reference file for the type you need.

| Type           | Transitions                                          | Reference                        |
| -------------- | ---------------------------------------------------- | -------------------------------- |
| Push           | Push slide, vertical push, elastic push, squeeze     | `transitions/css-push.md`        |
| Radial / Shape | Circle iris, diamond iris, diagonal split            | `transitions/css-radial.md`      |
| 3D             | 3D card flip                                         | `transitions/css-3d.md`          |
| Scale / Zoom   | Zoom through, zoom out                               | `transitions/css-scale.md`       |
| Dissolve       | Crossfade, blur crossfade, focus pull, color dip     | `transitions/css-dissolve.md`    |
| Cover          | Staggered blocks, horizontal blinds, vertical blinds | `transitions/css-cover.md`       |
| Light          | Light leak, overexposure burn, film burn             | `transitions/css-light.md`       |
| Distortion     | Glitch, chromatic aberration, ripple, VHS tape       | `transitions/css-distortion.md`  |
| Mechanical     | Shutter, clock wipe                                  | `transitions/css-mechanical.md`  |
| Grid           | Grid dissolve                                        | `transitions/css-grid.md`        |
| Other          | Gravity drop, morph circle                           | `transitions/css-other.md`       |
| Blur           | Blur through, directional blur                       | `transitions/css-blur.md`        |
| Destruction    | Page burn                                            | `transitions/css-destruction.md` |

## Shader Transitions

WebGL shader transitions are provided by `@hyperframes/shader-transitions` (`packages/shader-transitions/`). The package handles setup, capture, WebGL init, render loop, and GSAP integration. Read the package source for available shaders and API — do not copy raw GLSL manually.

The built-ins are not a ceiling. For an effect no built-in covers, you can write custom GLSL from scratch, adapt shader code found online (ShaderToy, GLSL Sandbox, GitHub), or build a custom CSS transition that fits no existing category — combine clip-path, transforms, and filters in new ways. If the storyboard calls for an effect that doesn't exist yet, build it; the framework renders anything a browser can run.


<!-- ===== FILE: hyperframes/hyperframes-animation/transitions/css-3d.md ===== -->

## 3D

### 3D Card Flip

180° Y-axis rotation. Requires CSS: `backface-visibility: hidden; transform-style: preserve-3d;` on both scene-inners. Parent needs `perspective: 1200px`.

```js
tl.set(new, { rotationY: -180, opacity: 1 }, T);
tl.to(old, { rotationY: 180, duration: 0.6, ease: "power2.inOut" }, T);
tl.to(new, { rotationY: 0, duration: 0.6, ease: "power2.inOut" }, T);
tl.set(old, { opacity: 0 }, T + 0.6);
```


<!-- ===== FILE: hyperframes/hyperframes-animation/transitions/css-blur.md ===== -->

## Blur

All blur transitions scale with energy. See GUIDE.md "Blur Intensity by Energy" for the full table.

### Blur Through

Content becomes fully abstract before resolving. The heaviest blur transition.

**Calm (default for this type — it's inherently heavy):**

```js
tl.to(old, { filter: "blur(30px)", scale: 1.08, duration: 0.5, ease: "power1.in" }, T);
tl.to(old, { opacity: 0, duration: 0.3, ease: "power1.in" }, T + 0.3);
// Hold: both scenes in abstract blur state
tl.fromTo(new,
  { filter: "blur(30px)", scale: 0.92, opacity: 0 },
  { filter: "blur(30px)", scale: 0.92, opacity: 1, duration: 0.2, ease: "none" }, T + 0.5);
// Slow resolve
tl.to(new, { filter: "blur(0px)", scale: 1, duration: 0.7, ease: "power1.out" }, T + 0.7);
```

**Medium:**

```js
tl.to(old, { filter: "blur(15px)", scale: 1.05, opacity: 0, duration: 0.4, ease: "power2.in" }, T);
tl.fromTo(new,
  { filter: "blur(15px)", scale: 0.95, opacity: 0 },
  { filter: "blur(0px)", scale: 1, opacity: 1, duration: 0.4, ease: "power2.out" }, T + 0.2);
```

### Directional Blur

Blur + skew simulating motion in one direction. Scale blur and skew with energy.

**Medium (default):**

```js
tl.to(old, { filter: "blur(12px)", skewX: -8, x: -200, opacity: 0, duration: 0.4, ease: "power3.in" }, T);
tl.fromTo(new,
  { filter: "blur(12px)", skewX: 8, x: 200, opacity: 0 },
  { filter: "blur(0px)", skewX: 0, x: 0, opacity: 1, duration: 0.4, ease: "power3.out" }, T + 0.15);
```

**Calm (heavier blur, gentler motion):**

```js
tl.to(old, { filter: "blur(20px)", skewX: -4, x: -100, opacity: 0, duration: 0.6, ease: "power1.in" }, T);
tl.fromTo(new,
  { filter: "blur(20px)", skewX: 4, x: 100, opacity: 0 },
  { filter: "blur(0px)", skewX: 0, x: 0, opacity: 1, duration: 0.6, ease: "power1.out" }, T + 0.3);
```


<!-- ===== FILE: hyperframes/hyperframes-animation/transitions/css-cover.md ===== -->

## Cover

### Staggered Color Blocks

Full-screen (1920x1080) colored divs slide across staggered. Scene swaps while covered.

**2-block** (standard):

```js
tl.set("#wipe-a", { x: -1920 }, T - 0.01);
tl.set("#wipe-b", { x: -1920 }, T - 0.01);
tl.to("#wipe-a", { x: 0, duration: 0.25, ease: "power3.inOut" }, T);
tl.to("#wipe-b", { x: 0, duration: 0.25, ease: "power3.inOut" }, T + 0.06);
tl.set(old, { opacity: 0 }, T + 0.2);
tl.set(new, { opacity: 1 }, T + 0.2);
tl.to("#wipe-a", { x: 1920, duration: 0.25, ease: "power3.inOut" }, T + 0.28);
tl.to("#wipe-b", { x: 1920, duration: 0.25, ease: "power3.inOut" }, T + 0.34);
```

**5-block** (dense variant): same pattern with 5 blocks at 0.04s stagger. Use composition palette colors.

### Horizontal Blinds

Full-width strips slide across staggered. Each strip: `width: 1920px; height: Xpx`.

**6 strips** (180px each): `0.03s` stagger
**12 strips** (90px each): `0.018s` stagger

```js
for (var i = 0; i < N; i++) {
  tl.set("#blind-h-" + i, { x: -1920 }, T - 0.01);
  tl.fromTo("#blind-h-" + i, { x: -1920 }, { x: 0, duration: 0.2, ease: "power3.inOut" }, T + i * stagger);
}
tl.set(old, { opacity: 0 }, T + coverTime);
tl.set(new, { opacity: 1 }, T + coverTime);
for (var i = 0; i < N; i++) {
  tl.to("#blind-h-" + i, { x: 1920, duration: 0.2, ease: "power3.inOut" }, T + exitStart + i * stagger);
}
```

### Vertical Blinds

Same as horizontal but strips are tall and narrow, moving on Y axis.


<!-- ===== FILE: hyperframes/hyperframes-animation/transitions/css-destruction.md ===== -->

## Destruction

### Page Burn

The outgoing scene literally burns away from a corner. A fire front expands with noise-based irregular edges, a canvas draws the scorched char line at the burn boundary, and individual text characters/elements chip off and fall with gravity as the fire reaches them. The incoming scene reveals behind the burn.

This transition has three systems working together:

1. **Fire geometry** — a radial front expanding from a corner (e.g., bottom-right) with noise-based irregularity for organic edges
2. **Scene clipping** — the outgoing scene uses an SVG clip-path (with `fill-rule: evenodd`) that cuts a hole matching the fire front. As the fire expands, more of the scene is clipped away. All content (text, images, lines) burns with the page — no separate debris.
3. **Scorched edge** — a `<canvas>` overlay draws a radial gradient fringe at the fire boundary to simulate charring

**When to use:** Dramatic reveals, edgy/destructive mood, gaming, neon-noir. This is the most dramatic transition in the catalog — reserve it for hero moments.

**Requirements:**

- A `<canvas>` element for the burn edge overlay
- A noise function for organic fire edge geometry
- SVG clip-path with evenodd fill-rule for the inverted clip

**Fire geometry (deterministic noise):**

```js
function noise(x) {
  var ix = Math.floor(x),
    fx = x - ix;
  var a = Math.sin(ix * 127.1 + 311.7) * 43758.5453;
  var b = Math.sin((ix + 1) * 127.1 + 311.7) * 43758.5453;
  var t = fx * fx * (3 - 2 * fx);
  return a - Math.floor(a) + (b - Math.floor(b) - (a - Math.floor(a))) * t;
}

function fireRadiusAtAngle(angle, progress) {
  var base = progress * maxRadius;
  return (
    base +
    noise(angle * 3 + progress * 4) * 50 +
    noise(angle * 8 + progress * 9) * 20 +
    noise(angle * 15 + progress * 15) * 8
  );
}
```

**Incoming scene timing:** The incoming scene should NOT be visible during the burn. As the fire consumes the outgoing scene, **black shows through the holes** — this is the dramatic part. The viewer watches content being destroyed against blackness.

At ~90% through the burn, the incoming scene fades in SLOWLY from black — the background first, then content staggered. Use long, gentle fades (`power1.out`, 0.8-1.2s durations) so it feels like the new scene materializes from darkness, not a hard swap.

```js
// Scene 2 stays at opacity: 0 during the burn — black behind the fire
tl.set("#s2-title", { opacity: 0 }, T);
tl.set("#s2-subtitle", { opacity: 0 }, T);

// At 90% through, scene bg fades in slowly from black
var contentReveal = T + BURN_DURATION * 0.9;
tl.to("#scene2", { opacity: 1, duration: 1.2, ease: "power1.out" }, contentReveal);

// Content fades in staggered on top, even slower
tl.to("#s2-title", { opacity: 1, duration: 1.0, ease: "power1.out" }, contentReveal + 0.5);
tl.to("#s2-subtitle", { opacity: 1, duration: 0.8, ease: "power1.out" }, contentReveal + 0.7);
```

**Content burns with the page — no falling debris.** The clip-path on scene1 IS the effect — as the fire shape expands, everything behind the fire edge (text, images, lines) disappears naturally. Don't clone elements, don't create falling debris. The content is part of the page being consumed. The scorched canvas edge provides the visual char line at the burn boundary.

**Hide scene1 via `tl.set` at burn end — NEVER in `onComplete`.** Using `onComplete` to hide scene1 is not reversible when scrubbing. Instead, use a `tl.set` at the exact burn end time:

```js
tl.to(
  burnState,
  {
    progress: 1,
    duration: BURN_DURATION,
    ease: "none",
    onUpdate: function () {
      var wp = burnState.progress;
      var scene1 = document.getElementById("scene1");
      if (wp <= 0) {
        scene1.style.clipPath = "none"; // fully visible when rewound
      } else if (wp < 1) {
        scene1.style.clipPath = buildClipPath(wp);
      }
      drawEdge(wp);
    },
    // NO onComplete — use tl.set instead
  },
  T,
);

// Hide scene1 at exact burn end — reversible via timeline
tl.set("#scene1", { opacity: 0 }, T + BURN_DURATION);
tl.set("#scene1", { clipPath: "none" }, T + BURN_DURATION);
```

The `onUpdate` handles clip-path and canvas edge per-frame. The `tl.set` handles the final hide — and GSAP automatically reverses it when scrubbing backward, restoring scene1 to `opacity: 1`.

The `onUpdate` callback is the key — it runs every frame to advance the clip-path and canvas edge in sync with the timeline.


<!-- ===== FILE: hyperframes/hyperframes-animation/transitions/css-dissolve.md ===== -->

## Dissolve

### Crossfade

Simple opacity swap. The baseline.

```js
tl.to(old, { opacity: 0, duration: 0.5, ease: "power2.inOut" }, T);
tl.fromTo(new, { opacity: 0 }, { opacity: 1, duration: 0.5, ease: "power2.inOut" }, T);
```

### Blur Crossfade

Dissolve with blur + scale shift. **Scale blur amount by energy** — see GUIDE.md "Blur Intensity by Energy" section. The examples below show the medium (default) version. For calm compositions, increase to 20-30px with a 0.3-0.5s hold at peak blur. For high-energy, decrease to 3-6px with no hold.

**Medium (default):**

```js
tl.to(old, { filter: "blur(10px)", scale: 1.03, opacity: 0, duration: 0.5, ease: "power2.inOut" }, T);
tl.fromTo(new,
  { filter: "blur(10px)", scale: 0.97, opacity: 0 },
  { filter: "blur(0px)", scale: 1, opacity: 1, duration: 0.5, ease: "power2.inOut" }, T + 0.1);
```

**Calm (wellness, luxury) — heavy blur, holds at abstract color:**

```js
tl.to(old, { filter: "blur(25px)", scale: 1.05, duration: 0.6, ease: "power1.in" }, T);
tl.to(old, { opacity: 0, duration: 0.4, ease: "power1.in" }, T + 0.4);
tl.fromTo(new,
  { filter: "blur(25px)", scale: 0.95, opacity: 0 },
  { filter: "blur(25px)", scale: 0.95, opacity: 1, duration: 0.3, ease: "power1.inOut" }, T + 0.5);
tl.to(new, { filter: "blur(0px)", scale: 1, duration: 0.6, ease: "power1.out" }, T + 0.8);
```

### Focus Pull

Outgoing slowly blurs while incoming fades in sharp. Depth-of-field feel. **Scale blur amount and hold duration by energy.**

**Medium:**

```js
tl.to(old, { filter: "blur(15px)", duration: 0.5, ease: "power1.in" }, T);
tl.to(old, { opacity: 0, duration: 0.3, ease: "power2.in" }, T + 0.25);
tl.fromTo(new, { opacity: 0 }, { opacity: 1, duration: 0.3, ease: "power2.out" }, T + 0.25);
```

**Calm — slow rack focus with long hold at peak defocus:**

```js
tl.to(old, { filter: "blur(30px)", duration: 0.8, ease: "power1.in" }, T);
tl.to(old, { opacity: 0, duration: 0.5, ease: "power1.in" }, T + 0.6);
tl.fromTo(new, { opacity: 0, filter: "blur(20px)" },
  { opacity: 1, filter: "blur(20px)", duration: 0.3, ease: "power1.inOut" }, T + 0.7);
tl.to(new, { filter: "blur(0px)", duration: 0.6, ease: "power1.out" }, T + 1.0);
```

### Color Dip

Fade to solid color, hold, fade up new scene.

```js
tl.to(old, { opacity: 0, duration: 0.2, ease: "power2.in" }, T);
// Background color shows through
tl.fromTo(new, { opacity: 0 }, { opacity: 1, duration: 0.2, ease: "power2.out" }, T + 0.25);
```


<!-- ===== FILE: hyperframes/hyperframes-animation/transitions/css-distortion.md ===== -->

## Distortion

### Glitch

RGB-tinted overlays (NOT multiply blend — use normal blending at 35% opacity) jitter with large offsets. Scene itself also jitters.

```js
tl.set("#glitch-r", { opacity: 1, x: 40, y: -8 }, T);
tl.set("#glitch-g", { opacity: 1, x: -30, y: 12 }, T);
tl.set("#glitch-b", { opacity: 1, x: 15, y: -20 }, T);
tl.set(old, { x: -15 }, T);
// 6 jitter frames at 0.03s intervals with big offsets (±30-60px)
// ... swap and clear at T + 0.2
```

### Chromatic Aberration

RGB overlays start aligned then spread apart (±80px), scene fades, converge on new scene.

```js
tl.set("#glitch-r", { opacity: 0.6, x: 0 }, T);
tl.set("#glitch-g", { opacity: 0.6, x: 0 }, T);
tl.set("#glitch-b", { opacity: 0.6, x: 0 }, T);
tl.to("#glitch-r", { x: -80, opacity: 0.8, duration: 0.3, ease: "power2.in" }, T);
tl.to("#glitch-b", { x: 80, opacity: 0.8, duration: 0.3, ease: "power2.in" }, T);
tl.to("#glitch-g", { y: 30, duration: 0.3, ease: "power2.in" }, T);
// Swap at T + 0.3, converge back at T + 0.3
```

### Ripple

Rapid oscillation (±30px) + scale distortion (0.97-1.03) + increasing blur. Swap at peak distortion.

```js
tl.to(old, { x: 30, scale: 1.02, duration: 0.04, ease: "none" }, T);
tl.to(old, { x: -25, scale: 0.98, filter: "blur(4px)", duration: 0.04, ease: "none" }, T + 0.04);
// ... more oscillations with increasing blur
// Swap at peak, incoming stabilizes with decreasing wobble
```

### VHS Tape

Clone scene into 20 horizontal strips (each 54px, clip-path'd). Each strip shifts x independently with seeded pseudo-random offsets at per-bar random intervals. Add red+blue chromatic offset copies on each strip (z-index above main, 35% opacity). Make strips wider than frame (2020px at left:-50px) so edges never show.

See GUIDE.md for clone-based implementation pattern.


<!-- ===== FILE: hyperframes/hyperframes-animation/transitions/css-grid.md ===== -->

## Grid

### Grid Dissolve

Grid of colored cells covers the frame in a ripple from center. Scene swaps at 50% coverage. Cells fade out in ripple.

**12-cell** (4x3, each 480x270): standard
**120-cell** (12x10, each 160x108): dense variant — lower opacity (0.75), tighter ripple

Cells are created dynamically in JS, sorted by distance from center for ripple stagger.


<!-- ===== FILE: hyperframes/hyperframes-animation/transitions/css-light.md ===== -->

## Light

### Light Leak

Multiple warm-colored overlays wash across frame. Needs: a flat warm tint layer + 2-3 bright radial gradient divs, all larger than the frame so edges are never visible.

```js
// Warm tint washes over entire frame
tl.to("#leak-warm", { opacity: 0.4, duration: 0.3, ease: "power1.in" }, T);
// Bright leak elements drift in
tl.to("#leak-1", { opacity: 0.9, x: 300, duration: 0.5, ease: "sine.inOut" }, T + 0.05);
tl.to("#leak-2", { opacity: 0.8, x: 200, duration: 0.6, ease: "sine.inOut" }, T + 0.1);
// Peak warmth then swap
tl.to("#leak-warm", { opacity: 0.6, duration: 0.15, ease: "power2.in" }, T + 0.35);
tl.set(old, { opacity: 0 }, T + 0.45);
tl.set(new, { opacity: 1 }, T + 0.45);
// Leak fades
tl.to("#leak-warm", { opacity: 0, duration: 0.4, ease: "power2.out" }, T + 0.5);
tl.to("#leak-1", { opacity: 0, x: 600, duration: 0.35, ease: "power1.out" }, T + 0.5);
```

### Overexposure Burn

Scene progressively blows out to white using CSS `filter: brightness()`, then white overlay fades in. Swap at peak white. White recedes to reveal new scene.

```js
tl.to(old, { filter: "brightness(1.5)", scale: 1.03, duration: 0.2, ease: "power1.in" }, T);
tl.to(old, { filter: "brightness(3)", scale: 1.06, duration: 0.2, ease: "power2.in" }, T + 0.2);
tl.to("#flash-overlay", { opacity: 0.5, duration: 0.25, ease: "power1.in" }, T + 0.15);
tl.to("#flash-overlay", { opacity: 1, duration: 0.15, ease: "power2.in" }, T + 0.4);
tl.set(old, { opacity: 0, filter: "brightness(1)", scale: 1 }, T + 0.55);
tl.set(new, { opacity: 1 }, T + 0.55);
tl.to("#flash-overlay", { opacity: 0, duration: 0.35, ease: "power2.out" }, T + 0.55);
```

### Film Burn

Staggered warm overlays (amber, orange, red) bleed from one edge. Each overlay is a large radial gradient div at high z-index.

```js
tl.to("#burn-a", { opacity: 1, x: -300, duration: 0.4, ease: "power1.in" }, T);
tl.to("#burn-b", { opacity: 1, x: -500, duration: 0.5, ease: "power1.in" }, T + 0.05);
tl.to("#burn-c", { opacity: 1, x: -200, duration: 0.45, ease: "power1.in" }, T + 0.1);
tl.set(old, { opacity: 0 }, T + 0.35);
tl.set(new, { opacity: 1 }, T + 0.35);
tl.to("#burn-a", { opacity: 0, duration: 0.3, ease: "power2.out" }, T + 0.45);
tl.to("#burn-b", { opacity: 0, duration: 0.3, ease: "power2.out" }, T + 0.5);
tl.to("#burn-c", { opacity: 0, duration: 0.3, ease: "power2.out" }, T + 0.55);
```


<!-- ===== FILE: hyperframes/hyperframes-animation/transitions/css-mechanical.md ===== -->

## Mechanical

### Shutter

Two full-screen halves close from top and bottom, meet in the middle. Swap while closed. Open again.

```js
tl.to("#shutter-top", { y: 0, duration: 0.25, ease: "power3.in" }, T);
tl.to("#shutter-bot", { y: 0, duration: 0.25, ease: "power3.in" }, T);
tl.set(old, { opacity: 0 }, T + 0.25);
tl.set(new, { opacity: 1 }, T + 0.25);
tl.to("#shutter-top", { y: -540, duration: 0.25, ease: "power3.out" }, T + 0.3);
tl.to("#shutter-bot", { y: 540, duration: 0.25, ease: "power3.out" }, T + 0.3);
```

### Clock Wipe

Radial polygon sweep stepping through quadrants. Use 9-point polygon with intermediate edge positions for smooth sweep.

```js
tl.set(new, { opacity: 1, zIndex: 10 }, T);
var d = 0.1; // duration per quadrant
tl.set(new, { clipPath: "polygon(50% 50%, 50% 0%, 50% 0%, 50% 0%, 50% 0%, 50% 0%, 50% 0%, 50% 0%, 50% 0%)" }, T);
tl.to(new, { clipPath: "polygon(50% 50%, 50% 0%, 100% 0%, 100% 50%, 100% 50%, 100% 50%, 100% 50%, 100% 50%, 100% 50%)", duration: d, ease: "none" }, T);
tl.to(new, { clipPath: "polygon(50% 50%, 50% 0%, 100% 0%, 100% 50%, 100% 100%, 50% 100%, 50% 100%, 50% 100%, 50% 100%)", duration: d, ease: "none" }, T + d);
tl.to(new, { clipPath: "polygon(50% 50%, 50% 0%, 100% 0%, 100% 50%, 100% 100%, 50% 100%, 0% 100%, 0% 50%, 0% 50%)", duration: d, ease: "none" }, T + d*2);
tl.to(new, { clipPath: "polygon(50% 50%, 50% 0%, 100% 0%, 100% 50%, 100% 100%, 50% 100%, 0% 100%, 0% 50%, 0% 0%)", duration: d, ease: "none" }, T + d*3);
tl.set(new, { clipPath: "none", zIndex: "auto" }, T + d*4 + 0.02);
tl.set(old, { opacity: 0, zIndex: "auto" }, T + d*4 + 0.02);
```


<!-- ===== FILE: hyperframes/hyperframes-animation/transitions/css-other.md ===== -->

## Other

### Gravity Drop

Old scene falls down with slight rotation. New scene was behind it. Needs z-index.

```js
tl.set(new, { opacity: 1, zIndex: 1 }, T);
tl.set(old, { zIndex: 10 }, T);
tl.to(old, { y: 1200, rotation: 4, duration: 0.5, ease: "power3.in" }, T);
tl.set(old, { opacity: 0, zIndex: "auto" }, T + 0.5);
tl.set(new, { zIndex: "auto" }, T + 0.5);
```

### Morph Circle

A circle scales up from center to fill frame (becoming the new scene's background color). New scene content fades in on top.

```js
tl.set("#morph-circle", { background: newBgColor, opacity: 1, scale: 0 }, T);
tl.to("#morph-circle", { scale: 30, duration: 0.5, ease: "power3.in" }, T);
tl.set(old, { opacity: 0 }, T + 0.4);
tl.set(new, { opacity: 1 }, T + 0.4);
tl.to("#morph-circle", { opacity: 0, duration: 0.15, ease: "power2.out" }, T + 0.5);
```


<!-- ===== FILE: hyperframes/hyperframes-animation/transitions/css-push.md ===== -->

## Linear / Push

### Push Slide

Both scenes move together — new pushes old out.

```js
tl.to(old, { x: -1920, duration: 0.5, ease: "power3.inOut" }, T);
tl.fromTo(new, { x: 1920, opacity: 1 }, { x: 0, opacity: 1, duration: 0.5, ease: "power3.inOut" }, T);
```

### Vertical Push

Same as push slide but vertical.

```js
tl.to(old, { y: -1080, duration: 0.5, ease: "power3.inOut" }, T);
tl.fromTo(new, { y: 1080, opacity: 1 }, { y: 0, opacity: 1, duration: 0.5, ease: "power3.inOut" }, T);
```

### Elastic Push

Push with overshoot bounce on the incoming scene.

```js
tl.to(old, { x: -1920, duration: 0.5, ease: "power3.in" }, T);
tl.fromTo(new, { x: 1920, opacity: 1 }, { x: 30, opacity: 1, duration: 0.4, ease: "power4.out" }, T + 0.1);
tl.to(new, { x: -15, duration: 0.15, ease: "sine.inOut" }, T + 0.5);
tl.to(new, { x: 0, duration: 0.1, ease: "sine.out" }, T + 0.65);
```

### Squeeze

Old compresses, new expands from opposite side.

```js
tl.to(old, { scaleX: 0, transformOrigin: "left center", duration: 0.4, ease: "power3.inOut" }, T);
tl.fromTo(new, { scaleX: 0, transformOrigin: "right center", opacity: 1 },
  { scaleX: 1, opacity: 1, duration: 0.4, ease: "power3.inOut" }, T + 0.1);
tl.set(old, { opacity: 0 }, T + 0.5);
```


<!-- ===== FILE: hyperframes/hyperframes-animation/transitions/css-radial.md ===== -->

## Radial / Shape

### Circle Iris

Expanding circle from center reveals new scene.

```js
tl.set(new, { opacity: 1 }, T);
tl.fromTo(new,
  { clipPath: "circle(0% at 50% 50%)" },
  { clipPath: "circle(75% at 50% 50%)", duration: 0.5, ease: "power2.out" }, T);
tl.set(old, { opacity: 0 }, T + 0.5);
```

### Diamond Iris

Expanding diamond shape from center.

```js
tl.set(new, { opacity: 1 }, T);
tl.fromTo(new,
  { clipPath: "polygon(50% 50%, 50% 50%, 50% 50%, 50% 50%)" },
  { clipPath: "polygon(50% -20%, 120% 50%, 50% 120%, -20% 50%)", duration: 0.5, ease: "power2.out" }, T);
tl.set(old, { opacity: 0 }, T + 0.5);
```

### Diagonal Split

Old scene shrinks to a triangle in one corner.

```js
tl.set(new, { opacity: 1, zIndex: 1 }, T);
tl.set(old, { zIndex: 10, clipPath: "polygon(0% 0%, 100% 0%, 100% 100%, 0% 100%)" }, T);
tl.to(old, { clipPath: "polygon(60% 0%, 100% 0%, 100% 40%, 60% 0%)", duration: 0.5, ease: "power3.inOut" }, T);
tl.set(old, { opacity: 0, zIndex: "auto", clipPath: "none" }, T + 0.5);
tl.set(new, { zIndex: "auto" }, T + 0.5);
```


<!-- ===== FILE: hyperframes/hyperframes-animation/transitions/css-scale.md ===== -->

## Scale / Zoom

### Zoom Through

Old zooms past camera + blurs, new zooms in from behind.

```js
tl.to(old, { scale: 2.5, opacity: 0, filter: "blur(8px)", duration: 0.4, ease: "power3.in" }, T);
tl.fromTo(new,
  { scale: 0.5, opacity: 0, filter: "blur(8px)" },
  { scale: 1, opacity: 1, filter: "blur(0px)", duration: 0.4, ease: "power3.out" }, T + 0.15);
```

### Zoom Out

Old shrinks away, new was behind it. Needs z-index management.

```js
tl.set(new, { opacity: 1, zIndex: 1 }, T);
tl.set(old, { zIndex: 10, transformOrigin: "50% 50%" }, T);
tl.to(old, { scale: 0.3, opacity: 0, duration: 0.4, ease: "power3.in" }, T);
tl.set(old, { zIndex: "auto" }, T + 0.4);
tl.set(new, { zIndex: "auto" }, T + 0.4);
```


<!-- ===== FILE: hyperframes/hyperframes-animation/transitions/overview.md ===== -->

# Scene Transitions

A transition tells the viewer how two scenes relate. A crossfade says "this continues." A push slide says "next point." A blur crossfade says "drift with me." Choose transitions that match what the content is doing emotionally, not just technically.

## Contents

- Animation rules for multi-scene compositions
- Energy and mood transition selection
- Narrative position
- Blur intensity
- Presets
- Implementation
- CSS vs shader guidance
- Shader-compatible CSS rules
- Visual pattern warnings

## Animation Rules for Multi-Scene Compositions

These are non-negotiable for every multi-scene composition:

1. **Every composition uses transitions.** No exceptions. Scenes without transitions feel like jump cuts.
2. **Every scene uses entrance animations.** Elements animate IN — opacity, position, scale, etc. No scene should pop fully-formed onto screen. Use `gsap.fromTo()` (not `gsap.from()`) so the start state is explicit: `from()` animates _to_ current CSS, so pairing it with CSS `opacity: 0` is a 0→0 noop and the element never appears (see `/hyperframes-core` → sub-compositions).
3. **Exit animations are BANNED** except on the final scene. Do NOT use `gsap.to()` to animate elements out before a transition fires. The transition IS the exit. Outgoing scene content must be fully visible when the transition starts — the transition handles the visual handoff.
4. **Final scene exception:** The last scene MAY fade elements out (e.g., fade to black at the end of the composition). This is the only scene where exit animations are allowed.

```js
// ❌ BANNED — fading the outgoing scene out, then the next scene just runs its entrance.
//    This is a jump cut with a dip, not a transition.
tl.to("#s1", { opacity: 0, duration: 0.4 }, 4.0);
tl.from("#s2 .headline", { y: 40, opacity: 0 }, 4.4);

// ✅ CORRECT — outgoing and incoming animate AT THE SAME TIME T; the motion IS the handoff.
const T = 4.0;
tl.to("#s1", { yPercent: -100, filter: "blur(8px)", duration: 0.5, ease: "power3.in" }, T);
tl.fromTo("#s2", { yPercent: 100 }, { yPercent: 0, duration: 0.5, ease: "power3.out" }, T);
```

> **You are NOT done after this file.** This overview gives you _which_ transition and _when_. Before writing any transition you MUST open **`catalog.md`** in this directory for the GSAP code and the hard rule every transition follows — _position new scene → animate outgoing → swap → animate incoming → clean up overlays_ — plus the per-category `css-*.md` files for specifics. Authoring transitions from this overview alone is how you end up shipping the ❌ pattern above.

## Energy → Primary Transition

| Energy                                   | CSS Primary                  | Shader Primary                       | Accent                         | Duration  | Easing                 |
| ---------------------------------------- | ---------------------------- | ------------------------------------ | ------------------------------ | --------- | ---------------------- |
| **Calm** (wellness, brand story, luxury) | Blur crossfade, focus pull   | Cross-warp morph, thermal distortion | Light leak, circle iris        | 0.5-0.8s  | `sine.inOut`, `power1` |
| **Medium** (corporate, SaaS, explainer)  | Push slide, staggered blocks | Whip pan, cinematic zoom             | Squeeze, vertical push         | 0.3-0.5s  | `power2`, `power3`     |
| **High** (promos, sports, music, launch) | Zoom through, overexposure   | Ridged burn, glitch, chromatic split | Staggered blocks, gravity drop | 0.15-0.3s | `power4`, `expo`       |

Pick ONE primary (60-70% of scene changes) + 1-2 accents. Never use a different transition for every scene.

## Mood → Transition Type

Think about what the transition _communicates_, not just what it looks like.

| Mood                     | Transitions                                                                                                                          | Why it works                                                                                |
| ------------------------ | ------------------------------------------------------------------------------------------------------------------------------------ | ------------------------------------------------------------------------------------------- |
| **Warm / inviting**      | Light leak, blur crossfade, focus pull, film burn · **Shader:** thermal distortion, light leak, cross-warp morph                     | Soft edges, warm color washes. Nothing sharp or mechanical.                                 |
| **Cold / clinical**      | Squeeze, zoom out, blinds, shutter, grid dissolve · **Shader:** gravitational lens                                                   | Content transforms mechanically — compressed, shrunk, sliced, gridded.                      |
| **Editorial / magazine** | Push slide, vertical push, diagonal split, shutter · **Shader:** whip pan                                                            | Like turning a page or slicing a layout. Clean directional movement.                        |
| **Tech / futuristic**    | Grid dissolve, staggered blocks, blinds, chromatic aberration · **Shader:** glitch, chromatic split                                  | Grid dissolve is the core "data" transition. Shader glitch adds posterization + scan lines. |
| **Tense / edgy**         | Glitch, VHS, chromatic aberration, ripple · **Shader:** ridged burn, glitch, domain warp                                             | Instability, distortion, digital breakdown. Ridged burn adds sharp lightning-crack edges.   |
| **Playful / fun**        | Elastic push, 3D flip, circle iris, morph circle, clock wipe · **Shader:** ripple waves, swirl vortex                                | Overshoot, bounce, rotation, expansion. Swirl vortex adds organic spiral distortion.        |
| **Dramatic / cinematic** | Zoom through, zoom out, gravity drop, overexposure, color dip to black · **Shader:** cinematic zoom, gravitational lens, domain warp | Scale, weight, light extremes. Shader transitions add per-pixel depth.                      |
| **Premium / luxury**     | Focus pull, blur crossfade, color dip to black · **Shader:** cross-warp morph, thermal distortion                                    | Restraint. Cross-warp morph flows both scenes into each other organically.                  |
| **Retro / analog**       | Film burn, light leak, VHS, clock wipe · **Shader:** light leak                                                                      | Organic imperfection. Warm color bleeds, scan line displacement.                            |

## Narrative Position

| Position                   | Use                                                                        | Why                                                   |
| -------------------------- | -------------------------------------------------------------------------- | ----------------------------------------------------- |
| **Opening**                | Your most distinctive transition. Match the mood. 0.4-0.6s                 | Sets the visual language for the entire piece.        |
| **Between related points** | Your primary transition. Consistent. 0.3s                                  | Don't distract — the content is continuing.           |
| **Topic change**           | Something different from your primary. Staggered blocks, shutter, squeeze. | Signals "new section" — the viewer's brain resets.    |
| **Climax / hero reveal**   | Your boldest accent. Fastest or most dramatic.                             | This is the payoff — spend your best transition here. |
| **Wind-down**              | Return to gentle. Blur crossfade, crossfade. 0.5-0.7s                      | Let the viewer exhale after the climax.               |
| **Outro**                  | Slowest, simplest. Crossfade, color dip to black. 0.6-1.0s                 | Closure. Don't introduce new energy at the end.       |

## Blur Intensity by Energy

| Energy     | Blur    | Duration | Hold at peak |
| ---------- | ------- | -------- | ------------ |
| **Calm**   | 20-30px | 0.8-1.2s | 0.3-0.5s     |
| **Medium** | 8-15px  | 0.4-0.6s | 0.1-0.2s     |
| **High**   | 3-6px   | 0.2-0.3s | 0s           |

## Presets

| Preset     | Duration | Easing            |
| ---------- | -------- | ----------------- |
| `snappy`   | 0.2s     | `power4.inOut`    |
| `smooth`   | 0.4s     | `power2.inOut`    |
| `gentle`   | 0.6s     | `sine.inOut`      |
| `dramatic` | 0.5s     | `power3.in` → out |
| `instant`  | 0.15s    | `expo.inOut`      |
| `luxe`     | 0.7s     | `power1.inOut`    |

## Implementation

Read `catalog.md` in this directory for GSAP code and hard rules for every transition type, and the `css-*.md` files for per-category implementation details.

| Category    | CSS                                                            | Shader (WebGL)                                                            |
| ----------- | -------------------------------------------------------------- | ------------------------------------------------------------------------- |
| Push/slide  | Push slide, vertical push, elastic push, squeeze               | Whip pan                                                                  |
| Scale/zoom  | Zoom through, zoom out, gravity drop, 3D flip                  | Cinematic zoom, gravitational lens                                        |
| Reveal/mask | Circle iris, diamond iris, diagonal split, clock wipe, shutter | SDF iris                                                                  |
| Dissolve    | Crossfade, blur crossfade, focus pull, color dip               | Cross-warp morph, domain warp                                             |
| Cover       | Staggered blocks, horizontal blinds, vertical blinds           | —                                                                         |
| Light       | Light leak, overexposure burn, film burn                       | Light leak (shader), thermal distortion                                   |
| Distortion  | Glitch, chromatic aberration, ripple, VHS tape                 | Glitch (shader), chromatic split, ridged burn, ripple waves, swirl vortex |
| Pattern     | Grid dissolve, morph circle                                    | —                                                                         |

## Transitions That Don't Work in CSS

Avoid: star iris, tilt-shift, lens flare, hinge/door. See catalog.md for why.

## CSS vs Shader

CSS transitions animate scene containers with opacity, transforms, clip-path, and filters. Shader transitions composite both scene textures per-pixel on a WebGL canvas — they can warp, dissolve, and morph in ways CSS cannot.

**Both are first-class options.** Shaders are provided by the `@hyperframes/shader-transitions` package — import from the package instead of writing raw GLSL. CSS transitions are simpler to set up. Choose based on the effect you want, not based on which is easier.

**Mixing is supported.** You can have some transitions use WebGL shaders and others use a CSS crossfade in the same composition. Omit the `shader` field on any `TransitionConfig` entry to get a smooth opacity crossfade instead of a WebGL effect:

```js
var tl = HyperShader.init({
  bgColor: "#000",
  accentColor: "#6366f1",
  scenes: ["s1", "s2", "s3", "s4"],
  transitions: [
    { time: 4.0, shader: "sdf-iris", duration: 0.7 }, // WebGL shader
    { time: 8.5, duration: 0.8 }, // no shader → CSS crossfade
    { time: 13.0, shader: "domain-warp", duration: 0.6 }, // WebGL shader
  ],
});
```

HyperShader manages all scene visibility regardless of transition type. Let it create the timeline (don't pass `timeline:` into `init()`) and add your beat animations to the returned `tl` after the call.

## Shader-Compatible CSS Rules

Shader transitions capture DOM scenes to WebGL textures via html2canvas. The canvas 2D rendering pipeline doesn't match CSS exactly. Follow these rules to avoid visible artifacts at transition boundaries:

1. **No `transparent` keyword in gradients.** Canvas interpolates `transparent` as `rgba(0,0,0,0)` (black at zero alpha), creating dark fringes. Always use the target color at zero alpha: `rgba(200,117,51,0)` not `transparent`.
2. **No gradient backgrounds on elements thinner than 4px.** Canvas can't match CSS gradient rendering on 1-2px elements. Use solid `background-color` on thin accent lines.
3. **No CSS variables (`var()`) on elements visible during capture.** html2canvas doesn't reliably resolve custom properties. Use literal color values in inline styles.
4. **Mark uncapturable decorative elements with `data-no-capture`.** The capture function skips these. They're present on the live DOM but absent from the shader texture. Use for elements that can't follow the rules above.
5. **No gradient opacity below 0.15.** Gradient elements below 10% opacity render differently in canvas vs CSS. Increase to 0.15+ or use a solid color at equivalent brightness.
6. **Every `.scene` div must have explicit `background-color`, AND pass the same color as `bgColor` in the `init()` config.** The package captures scene elements via html2canvas. Both the CSS `background-color` on `.scene` and the `bgColor` config must match. Without either, the texture renders as black.

These rules only apply to shader transition compositions. CSS-only compositions have no restrictions.

## Visual Pattern Warning

Avoid transitions that create visible repeating geometric patterns — grids of tiles, hexagonal cells, uniform dot arrays, evenly-spaced blob circles. These look cheap and artificial regardless of the math behind them. Organic noise (FBM, domain warping) is good because it's irregular. Geometric repetition is bad because the eye instantly sees the grid.
