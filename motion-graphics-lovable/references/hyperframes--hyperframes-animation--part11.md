

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
