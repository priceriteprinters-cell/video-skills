

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
