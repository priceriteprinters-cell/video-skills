

<!-- ===== FILE: hyperframes/hyperframes-keyframes/GUIDE.md ===== -->

---
name: hyperframes-keyframes
description: >
  Use when a HyperFrames composition needs a punch-in, punch-out, zoom, reframe,
  Ken Burns treatment, camera move, visual match/whip handoff, or other seek-safe
  2D/3D keyframes; also for GSAP, CSS keyframes, Anime.js, WAAPI, FLIP, paths,
  masks, SVG morph/draw, text trails, 3D depth, or `hyperframes keyframes` diagnostics.
  Don't use for broad scene strategy, brand design, media sourcing, captions, or
  general video planning.
---

**Plugin installs:** Before setup or freshness commands, follow [plugin execution rules](../hyperframes/references/plugin-installation.md) when this skill is inside a HyperFrames plugin. Standalone installs keep the update instructions below.

# HyperFrames Keyframes

Keyframes are a pose contract: visible states, continuous subject identity, seek-safe runtime, verified pixels.

Use `hyperframes-animation` for broad scene recipes. Use `hyperframes-cli` for full command docs. Use `references/keyframe-patterns.md` only when choosing implementation mechanisms, not visual style.

## Creator editing boundary

Keyframes own visual motion, not clip assembly. Source-range hard cuts, trim,
splice, and reorder belong to `/hyperframes-core`: author one media element per
kept range, place it with `data-start` and `data-duration`, and select its source
offset with `data-media-start`. Adjacent ranges make a hard cut. A crossfade
uses overlapping clips on different tracks plus visual opacity keyframes; sound
fades use `/hyperframes-audio`.

| Creator request                         | Truthful mechanism                                                                                                                                                                                                          |
| --------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Punch-in / punch-out                    | Keyframe `scale` with `x`/`y` or percentage translation on a non-timed visual/crop wrapper inside the clip. Use a set/short tween for a hard punch and a tween for a smooth move.                                           |
| Smooth multi-state zoom or reframe      | Keep one subject wrapper alive and author multiple zoom/reframe states as a pose ladder with per-segment easing.                                                                                                            |
| Pan, reframe, or Ken Burns camera move  | Animate wrapper translation plus scale. Geometry is authored; this is not face tracking or automatic semantic reframing.                                                                                                    |
| Chained camera moves                    | Chain labeled transform beats on one registered seek-safe timeline.                                                                                                                                                         |
| Match cut or whip pan                   | `/hyperframes-animation` owns the visual handoff; `/hyperframes-registry` supplies primitives; keyframes preserve authored geometry, direction, and velocity. There is no automatic matching-frame discovery.               |
| Crop and mask reframe                   | Interpolate `clip-path` or a mask on an inner visual wrapper to crop/reframe without changing source time. Polygon keyframes can form a polygon/mask transition.                                                            |
| Directional wipe cut or iris/reveal cut | Animate a mask/clip boundary across overlapping visual clips; `/hyperframes-animation` owns the handoff choreography.                                                                                                       |
| Split-screen handoff                    | Keep both visual clips placed by core, then keyframe their inner crop/mask wrappers and divider geometry.                                                                                                                   |
| Constant source retime                  | `/hyperframes-core` owns normalized `data-playback-rate` (`0.1..10`) for render-safe picture and pitch-preserved sound. It is constant for the whole media element.                                                         |
| Source speed ramps                      | A `rate` lane in `data-automation` on the `<video>`/`<audio>` (`t` in clip seconds, `v` 0.1..10, log interpolation); it wins over the constant rate.                                                                        |
| Freeze / hold                           | A visual pose, final source frame, or finished sub-composition can hold. Arbitrary mid-source freeze is not supported; preprocess a still/derived segment, place it as its own clip, then resume with another source range. |

When editing picture and sound together, load `/hyperframes-core`, this skill for
visual motion, and `/hyperframes-audio` for fades, crossfades, volume automation,
ducking/carve, or effects on the placed tracks.

A visual transition or cropping treatment is not a temporal source trim or
splice. `/hyperframes-core` owns the timeline, clip timing, and source ranges;
keyframes only animate the visible handoff or crop on wrappers inside those clips.
For copyable combined picture/sound recipes, use `/hyperframes-core` → `references/creator-editing-recipes.md`.

## Procedure

1. Identify the animated subject, visible states, final state, and runtime.
2. Choose the smallest mechanism that proves the prompt. Read `references/keyframe-patterns.md` only if the mechanism is unclear.
3. Author seek-safe keyframes in the declared runtime. Register the runtime instance only after the build completes; building inside `document.fonts.ready` is fine.
4. Verify with `hyperframes check` (it runs lint), `hyperframes keyframes`, one focused `--shot`, and snapshots at proof times.
5. If proof fails, fix the source keyframes and rerun the smallest failing diagnostic before rendering.

## Contract

- Name the moving subject.
- Name the poses needed to prove the intended motion, including the final state.
- Keyframe visible channels, not hidden helper state.
- Preserve object identity when continuity matters.
- Crossfade only when the intended motion is replacement or dissolve.
- Hold readable or semantic states long enough to see.
- Final frame is part of the animation, not cleanup.
- Do not reset to rest unless requested.
- Do not end on black unless requested.
- If editing a starter scene, preserve layout, copy, assets, colors, and final state unless asked to redesign.

## Runtime Rules

GSAP:

- build at page load or inside `document.fonts.ready`, and register only after the build completes
- use `gsap.timeline({ paused: true })`
- register as `window.__timelines[compositionId]`
- registry key must match `data-composition-id`
- do not call `tl.play()` for render-critical motion
- keep repeats finite

CSS keyframes:

- finite duration and iteration count
- deterministic delay
- `animation-fill-mode: both`
- use `data-start` when timing belongs to a clip

Anime.js:

- create synchronously
- `autoplay: false`
- finite duration and loops
- push every instance to `window.__hfAnime`

WAAPI:

- finite `duration`
- `fill: "both"`
- deterministic construction
- the text surface does not list WAAPI; verify with `--shot` (it seeks WAAPI) and snapshots

Never use for render-critical motion:

- `Date.now()`
- `performance.now()`
- unseeded `Math.random()`
- hover/scroll triggers
- timers
- a timeline registered before its async build finishes
- unregistered `requestAnimationFrame`
- infinite loops

## GSAP Skeleton

```js
const root = document.querySelector("[data-composition-id]");
const compositionId = root.dataset.compositionId;
const tl = gsap.timeline({ paused: true });

tl.addLabel("state-a", 0);
tl.to(".subject", {
  keyframes: [
    { x: 0, opacity: 1, duration: 0.2 },
    { x: 120, opacity: 1, duration: 0.4, ease: "power2.out" },
    { x: 100, opacity: 1, duration: 0.2, ease: "power2.inOut" },
  ],
  ease: "none",
});

window.__timelines = window.__timelines || {};
window.__timelines[compositionId] = tl;
```

Use labels for semantic states. Use position parameters instead of chained delays. Use `immediateRender: false` for later `from()`/`fromTo()` tweens touching the same property.

## Keyframe Forms

- Array keyframes: pose ladder with per-step duration/ease.
- Percentage keyframes: exact timing inside one tween.
- Property arrays: compact multi-stop changes.
- `ease: "none"` on the parent when each stop carries its own easing.
- `easeEach` when every segment should share the same feel.

Do not copy numeric distances or timing from examples. Derive them from the actual composition geometry and duration.

For one subject moving between two boxes, prefer one continuous transform tween or FLIP. Split `x/y/scale` into multiple eased keyframes only when the viewer should feel distinct beats; every segment changes velocity and can read as a hitch.

## Channels

Prefer compositor/visual channels: `x/y/z`, `xPercent/yPercent`, `scale`, `rotationX/Y/Z`, `skew`, `transformOrigin`, `svgOrigin`, `opacity`, `autoAlpha`, `clip-path`, masks, CSS vars, SVG path/dash values, camera transforms, shader uniforms.

Avoid layout/lifecycle channels: `top/left/right/bottom`, `width/height`, `margin/padding`, `display`, `visibility`, late DOM creation, helper overlays doing subject motion.

For visibility changes, use `autoAlpha` on the registered seekable GSAP timeline, or a zero-duration `tl.set()` at an explicit boundary. Target only a non-clip element or a wrapper inside the clip; never target `.clip` itself. Never duration-tween raw `visibility`, and never tween `display`.

## Mechanism Choice

Choose the smallest mechanism that proves the prompt:

| Need                                  | Mechanism                                          |
| ------------------------------------- | -------------------------------------------------- |
| Same subject changes box or hierarchy | shared element / FLIP                              |
| Subject travels a visible route       | path travel                                        |
| Stroke grows or traces                | stroke draw                                        |
| Shape becomes another shape           | shape interpolation                                |
| Reveal boundary is visible            | clip, mask, or shader uniform                      |
| Many items move with order            | stagger / indexed delay                            |
| Text itself moves                     | line, word, character, or band subdivision         |
| Surface bends, stretches, or crops    | parent/child counter-transform                     |
| UI has states                         | explicit state machine                             |
| Scene has depth                       | DOM 3D, Three.js, or WebGL camera/object keyframes |

Mechanisms can combine, but each one must clarify the idea. Decoration is not proof.

## Timing

- Anticipation only when it clarifies cause or direction.
- Acceleration leaves rest.
- Peak proof shows the mechanism unmistakably.
- Follow-through sells energy and direction.
- Overshoot only when the subject should feel elastic or tactile.
- Constant-speed path travel usually needs `ease: "none"`.
- Discrete UI states usually need a sharp ease-out.
- Repeated elements need ordered offsets, not identical timing.
- Final lockups need longer holds than transition poses.
- Smoothness means continuous velocity on the same subject.
- Do not overlap tweens that write the same transform property unless the overlap is intentional and verified.
- Avoid animating large `clip-path`/mask changes while the same hero surface is also scaling or traveling; use nested reveals after the main move settles.

## Text

Preserve line boxes, word spacing, readability, and final fit. If text moves internally, move the glyphs or masked bands, not only decorations around the text. Snapshot readable frames.

## SVG

For stroke growth prefer `DrawSVGPlugin`, then `stroke-dasharray`/`stroke-dashoffset`. For shape interpolation prefer `MorphSVGPlugin`; convert primitives to paths when needed and split complex silhouettes into simpler parts.

## 3D

Scale alone is fake depth. Use perspective on a stable parent, `transform-style: preserve-3d`, z travel, rotation, camera/world motion, occlusion, and layer order when objects cross.

Use one or two diagnostic angles that expose the depth relationship. If angled proof shows no depth crossing, improve z/camera/occlusion.

## Canvas / WebGL

Keyframe camera position, camera target, object transform, material opacity, shader uniforms, and postprocess intensity through deterministic state. Render from HyperFrames time. Use `--ghost` because marker boxes cannot see internal canvas motion.

## CLI Proof

```bash
npx hyperframes check
npx hyperframes keyframes .
npx hyperframes keyframes . --json
npx hyperframes keyframes . --runtime all
npx hyperframes keyframes . --selector "<selector>" --shot "<file>" --samples <n>
npx hyperframes keyframes . --selector "<selector>" --shot "<file>" --layout strip --from <t0> --to <t1>
npx hyperframes keyframes . --shot "<file>" --ghost --angle <angle>
npx hyperframes snapshot . --at <times>
```

Choose `<selector>` for the real animated subject. Choose `<times>` for first frame, proof poses, final-minus-hold, and exact final. Choose `<angle>` only when depth must be proven.

| Tool             | Proves                                                                                              |
| ---------------- | --------------------------------------------------------------------------------------------------- |
| `keyframes`      | targets, explicit stops, paths, traces, composed parent/child motion, CSS stops, Anime registration |
| `--shot`         | ghosts, route shape, time spacing, DOM 3D projection, focused selector proof                        |
| `--layout strip` | in-place motion, overlaps, contact, subtle scale/opacity, text waves                                |
| `--ghost`        | canvas, WebGL, shader motion, rendered 3D                                                           |
| `snapshot --at`  | masks, text readability, full state, final lockup, black/reset tails                                |

If selector proof looks wrong:

1. rerun `--json`
2. find the actual animated target
3. shoot that target
4. snapshot full frames
5. trust painted pixels over logs

## Diagnostic Reading

`flat` means no explicit middle poses. `keyframes` means explicit stops exist. `motionPath` means a route exists. `trace` means multi-stroke drawing. `composed with` means child motion inherits parent motion.

Even ghost spacing means constant speed. Clustered ghosts mean slow-in or settle. Large gaps mean fast travel.

A helper-selector shot is not proof. An onion shot over a broken full frame is not proof.

## Error Handling

| Failure            | Fix                                                                                |
| ------------------ | ---------------------------------------------------------------------------------- |
| endpoint-only      | add middle poses, hold peak proof, rerun `--shot`                                  |
| identity break     | keep one element alive, use shared source/final boxes, remove substitute crossfade |
| fake 3D            | add z/camera travel, occlusion, angled proof                                       |
| wrong final        | add final hold, snapshot final-minus-hold and exact final                          |
| unseekable runtime | pause autoplay, remove timers, register the instance after the build completes     |
| unreadable text    | preserve line boxes, reduce displacement, add final hold, snapshot text frames     |

## Done

Run `hyperframes check` (it runs lint), `hyperframes keyframes`, one focused `--shot`, and snapshots. Confirm first frame, proof poses, final-minus-hold, exact final, subject-owned motion, and no debug overlays.


<!-- ===== FILE: hyperframes/hyperframes-keyframes/references/keyframe-patterns.md ===== -->

# Keyframe Mechanism Reference

Use this after `GUIDE.md` when choosing a concrete implementation mechanism. It is a parts shelf, not a style guide. Start with one primary mechanism; add supporting motion only when it clarifies the idea.

## Runtime Skeletons

GSAP:

```js
const root = document.querySelector("[data-composition-id]");
const id = root.dataset.compositionId;
const tl = gsap.timeline({ paused: true });
tl.to("<selector>", {
  keyframes: [
    /* derive poses from the scene */
  ],
  ease: "none",
});
window.__timelines = window.__timelines || {};
window.__timelines[id] = tl;
```

CSS:

```css
.<subject > {
  animation: <name> <duration> <ease> both;
  animation-iteration-count: 1;
}
@keyframes <name> {
  0% {
    transform: <pose-a>;
    opacity: <a>;
  }
  100% {
    transform: <pose-b>;
    opacity: <b>;
  }
}
```

Anime.js:

```js
const animation = anime.createTimeline({ autoplay: false });
animation.add("<selector>", {
  /* derived channels */
});
window.__hfAnime = window.__hfAnime || [];
window.__hfAnime.push(animation);
```

Three/WebGL:

```js
const state = { progress: 0 };
tl.to(state, {
  progress: 1,
  duration: <duration>,
  onUpdate: () => {
    // derive camera/object/material values from state.progress
    renderer.render(scene, camera);
  },
});
```

## Mechanisms

| Mechanism           | Solves                                         | Keyframe                                                           | Runtime                                    | Verify                                         |
| ------------------- | ---------------------------------------------- | ------------------------------------------------------------------ | ------------------------------------------ | ---------------------------------------------- |
| Path travel         | Subject must visibly follow a route            | path progress, tangent rotation, follower offset, trail opacity    | GSAP MotionPath or sampled x/y/z           | strip shot at bends; final snapshot            |
| Stroke draw         | A line, ring, or outline appears over time     | dash/draw range, stroke opacity, endpoint state                    | DrawSVG or SVG dash fallback               | partial mid snapshot; complete final           |
| Shape interpolation | One silhouette becomes another                 | source path, middle path, target path, fill/stroke                 | MorphSVG or path tween                     | first/mid/final snapshots                      |
| Shared element      | Same subject changes box or hierarchy          | source box, target box, x/y, scale, radius, context opacity        | GSAP Flip or manual FLIP                   | one identity moves; no substitute crossfade    |
| Clip/mask reveal    | Animated boundary exposes content              | clip path, mask position/size, edge softness, inner counter-motion | CSS, SVG, GSAP, or shader                  | snapshot edge frames and final unclipped state |
| Ordered repetition  | Many items enter, leave, or transform in order | indexed delay, x/y, scale, opacity, final alignment                | GSAP stagger, Anime stagger, CSS vars      | check first/middle/last item timing            |
| Text subdivision    | Text motion needs readable internal timing     | line/word/char/band wrappers, y/x, opacity, final fit              | SplitText, authored spans, Anime splitText | strip shot plus final readability snapshot     |
| Surface transform   | Image/card stretches, crops, or changes shape  | parent scale/skew/clip, child counter-scale, transform origin      | GSAP/CSS keyframes                         | no accidental warped final                     |
| UI state machine    | Interface passes through semantic states       | closed, active, loading, success/error, final                      | GSAP/CSS/Anime                             | snapshots hit states in order                  |
| DOM depth           | HTML elements need 3D separation               | perspective, z, rotationX/Y, opacity, crossing layer order         | CSS 3D + GSAP/CSS/Anime                    | angled `--shot`; overlap snapshot              |
| Camera/object 3D    | Canvas/WebGL scene moves in depth              | camera, target, object transform, material opacity                 | Three.js/WebGL + GSAP proxy                | `--ghost`; snapshots at proof poses            |
| Shader uniform      | Pixel effect is driven by scalar progress      | progress, edge width, noise, color mix, opacity                    | ShaderMaterial/WebGL uniforms              | `--ghost`; snapshot 0/edge/mid/final           |
| Instanced system    | Many 3D objects move as one system             | instance transforms, scale, color/opacity, camera                  | Three InstancedMesh                        | snapshots, because DOM boxes miss internals    |
| Imported model      | Model animation must scrub deterministically   | `AnimationMixer.setTime`, camera, material, lights                 | Three AnimationMixer                       | drive from HyperFrames time; `--ghost`         |

## Source Links

- GSAP keyframes: https://gsap.com/resources/keyframes/
- GSAP timeline: https://gsap.com/docs/v3/GSAP/Timeline/
- GSAP MotionPathPlugin: https://gsap.com/docs/v3/Plugins/MotionPathPlugin/
- GSAP Flip: https://gsap.com/docs/v3/Plugins/Flip/
- GSAP DrawSVGPlugin: https://gsap.com/docs/v3/Plugins/DrawSVGPlugin/
- GSAP MorphSVGPlugin: https://gsap.com/docs/v3/Plugins/MorphSVGPlugin/
- GSAP SplitText: https://gsap.com/docs/v3/Plugins/SplitText/
- GSAP CSSPlugin: https://gsap.com/docs/v3/GSAP/CorePlugins/CSS/
- Anime.js documentation: https://animejs.com/documentation/
- Anime.js stagger grid: https://animejs.com/documentation/utilities/stagger/stagger-parameters/stagger-grid/
- Anime.js timeline: https://animejs.com/documentation/timeline/
- Anime.js SVG helpers: https://animejs.com/documentation/svg/createmotionpath/
- MDN CSS animations: https://developer.mozilla.org/en-US/docs/Web/CSS/CSS_animations/Using_CSS_animations
- MDN `@keyframes`: https://developer.mozilla.org/en-US/docs/Web/CSS/@keyframes
- MDN `clip-path`: https://developer.mozilla.org/en-US/docs/Web/CSS/clip-path
- MDN CSS masking: https://developer.mozilla.org/en-US/docs/Web/CSS/mask
- MDN perspective: https://developer.mozilla.org/en-US/docs/Web/CSS/perspective
- MDN transform-style: https://developer.mozilla.org/en-US/docs/Web/CSS/transform-style
- Three.js AnimationMixer: https://threejs.org/docs/#api/en/animation/AnimationMixer
- Three.js ShaderMaterial: https://threejs.org/docs/#api/en/materials/ShaderMaterial
- Three.js InstancedMesh: https://threejs.org/docs/#api/en/objects/InstancedMesh
