

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
