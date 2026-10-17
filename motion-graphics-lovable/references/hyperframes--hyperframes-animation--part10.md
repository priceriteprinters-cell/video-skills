

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
