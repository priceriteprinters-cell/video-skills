

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
