

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
