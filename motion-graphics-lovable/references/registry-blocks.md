

<!-- ===== FILE: registry-blocks/canopy-part-title/GUIDE.md ===== -->

---
name: canopy-part-title
description: Leaves sweep through the frame and part to reveal the headline. HyperFrames block, 1920×1080, 12s, 11 variables.
---

# Canopy Part Title

A dense canopy of textured leaves sweeps across the frame with shallow depth of field, then parts to uncover the first headline; a second, depth-lifted batch carries the second headline past the camera. A handful of leaves stay behind on the type and keep a light breeze. Font, weight, size, letter spacing, leaf counts, sweep speed and the retained-leaf breeze are variables.

Composition id: `canopy-part-title`. Duration 12 s at 30 fps, 1920×1080.

## Files

- `canopy-part-title.html` (57 KB)
- `assets/leaf-surface-color.webp` (64 KB)
- `assets/leaf-surface-normal.webp` (136 KB)

## Install

Install with `npx hyperframes add canopy-part-title`; by default the files above land under `compositions/canopy-part-title/`. Then mount the block from the host `index.html`:

```html
<div
  data-composition-id="canopy-part-title"
  data-composition-src="compositions/canopy-part-title/canopy-part-title.html"
  data-start="0"
  data-duration="12"
  data-track-index="1"
  data-width="1920"
  data-height="1080"
></div>
```

Render with custom values by targeting the composition file directly:

```sh
npx --yes hyperframes@0.8.12 render 'compositions/canopy-part-title/canopy-part-title.html' --variables '{"headline1":"Understory","headline2":"Move slowly"}'
```

## Variables

Read at runtime via `window.__hyperframes.getVariables()`; declared on the composition root as `data-composition-variables` (single-quoted attribute, plain JSON).

| id               | type   | default         | label / range                            |
| ---------------- | ------ | --------------- | ---------------------------------------- |
| `headline1`      | string | `"Understory"`  | Headline 1                               |
| `headline2`      | string | `"Move slowly"` | Headline 2                               |
| `font`           | string | `"Helvetica"`   | Headline font                            |
| `fontWeight`     | number | `900`           | Font weight 100–900 step 100             |
| `fontSize`       | number | `1`             | Font size (1 = auto-fit) 0.3–2 step 0.01 |
| `letterSpacing`  | number | `0.01`          | Letter spacing (em) -0.2–1 step 0.01     |
| `background`     | color  | `"#020805"`     | Background                               |
| `leafCount`      | number | `170`           | Leaves per sweep 40–320 step 1           |
| `stayCount`      | number | `5`             | Leaves left behind 0–20 step 1           |
| `sweepSpeed`     | number | `1`             | Sweep speed 0.3–3 step 0.05              |
| `retainedBreeze` | number | `1`             | Retained leaf breeze 0–2 step 0.05       |

## Runtime contract

- One paused GSAP timeline registered as `window.__timelines["canopy-part-title"]`.
- Re-syncs on the `hf-seek` CustomEvent; every frame is a closed-form function of time (seeded PRNG only, no rAF loops, no Date.now).
- Renderer: three.js 0.170.0, GSAP 3.14.2, Canvas 2D, Post-processing, Seeded PRNG, Shadow maps. Budget roughly 350 MB per live instance; run one at a time.
- External runtime dependencies: `https://cdn.jsdelivr.net/npm/gsap@3.14.2/dist/gsap.min.js`, `https://cdn.jsdelivr.net/npm/three@0.170.0/build/three.module.js`, `https://cdn.jsdelivr.net/npm/three@0.170.0/examples/jsm/postprocessing/EffectComposer.js`, `https://cdn.jsdelivr.net/npm/three@0.170.0/examples/jsm/postprocessing/RenderPass.js`, `https://cdn.jsdelivr.net/npm/three@0.170.0/examples/jsm/postprocessing/BokehPass.js`.
- Web fonts from Google Fonts: Gelasio.

## Editing rules (from the source project)

1. Keep `data-composition-variables` a single-quoted attribute with plain `"` JSON. Never save it through Studio's Design panel.
2. Do not put `<canvas>` in static markup; create it at runtime.
3. Keep every visual state a function of t; seek-safety is what makes the block renderable.


<!-- ===== FILE: registry-blocks/code-slice-hero/GUIDE.md ===== -->

---
name: code-slice-hero
description: A tiled headline surface flips cell by cell under a sweeping depth field to reveal the rear headline. HyperFrames block, 1920×1080, 8s, 18 variables.
---

# Code Slice Hero

A full square-tile surface carries one seamless headline. An imaginary cursor crosses the surface; nearby tiles respond to its Gaussian depth field with lift and tilt, and only the cells intersecting either headline silhouette turn over to reveal the rear headline. The whole grid is one instanced WebGL 2 draw with a shared front/rear texture pair, plus a batched projected-shadow pass. Copy, text size and square cell size are independent, so tiles never stretch. Sweep direction, easing strength, cursor radius, falloff, depth, bounce and shadow are all variables.

Composition id: `code-slice-hero`. Duration 8 s at 30 fps, 1920×1080.

## Files

- `code-slice-hero.html` (24 KB)
- `assets/Geist-Bold.ttf` (65 KB)
- `assets/Geist-OFL.txt` (4 KB)
- `assets/gsap-3.14.2.min.js` (128 KB)
- `assets/GSAP-NOTICE.txt` (1 KB)
- `shadows.js` (10 KB)
- `surface.js` (8 KB)

## Install

Install with `npx hyperframes add code-slice-hero`; by default the files above land under `compositions/code-slice-hero/`. Then mount the block from the host `index.html`:

```html
<div
  data-composition-id="code-slice-hero"
  data-composition-src="compositions/code-slice-hero/code-slice-hero.html"
  data-start="0"
  data-duration="8"
  data-track-index="1"
  data-width="1920"
  data-height="1080"
></div>
```

Render with custom values by targeting the composition file directly:

```sh
npx --yes hyperframes@0.8.12 render 'compositions/code-slice-hero/code-slice-hero.html' --variables '{"headline":"MAKE IT","reverseHeadline":"MATTER."}'
```

## Variables

Read at runtime via `window.__hyperframes.getVariables()`; declared on the composition root as `data-composition-variables` (single-quoted attribute, plain JSON).

| id                  | type   | default           | label / range                                     |
| ------------------- | ------ | ----------------- | ------------------------------------------------- | -------------- |
| `headline`          | string | `"MAKE IT"`       | Copy · Front headline max 32 chars                |
| `reverseHeadline`   | string | `"MATTER."`       | Copy · Rear headline max 32 chars                 |
| `direction`         | enum   | `"left-to-right"` | Motion · Sweep direction (left-to-right           | right-to-left) |
| `sweepDuration`     | number | `4.2`             | Motion · Sweep duration 2.6–4.5 step 0.05         |
| `sweepEaseStrength` | number | `3`               | Motion · Sweep easing strength 0–3 step 0.05      |
| `flipDuration`      | number | `0.75`            | Motion · Each tile flip 0.65–1.65 step 0.05       |
| `cursorRadius`      | number | `210`             | Cursor · Influence radius 160–480 step 10         |
| `cursorFalloff`     | number | `1.4`             | Cursor · Influence falloff 0.4–3.5 step 0.05      |
| `cursorDepth`       | number | `80`              | Cursor · Depth (+ toward camera) -320–320 step 10 |
| `tiltStrength`      | number | `55`              | Cursor · Pull / tilt strength 0–55 step 1         |
| `noiseStrength`     | number | `2`               | Motion · Organic variation 0–2 step 0.05          |
| `flipBounce`        | number | `0.15`            | Motion · Elastic flip bounce 0–0.8 step 0.05      |
| `cellSize`          | number | `112`             | Slices · Square cell size 24–120 step 4           |
| `formationScale`    | number | `1`               | Slices · Local formation scale 0.94–1 step 0.001  |
| `fontSize`          | number | `310`             | Type · Maximum size 160–480 step 5                |
| `behindColor`       | color  | `"#212121"`       | Surface · Behind-tile background                  |
| `shadowStrength`    | number | `0.19`            | Surface · Cast shadow strength 0–0.65 step 0.01   |
| `shadowSoftness`    | number | `4`               | Surface · Cast shadow softness 0.5–4 step 0.1     |

## Runtime contract

- One paused GSAP timeline registered as `window.__timelines["code-slice-hero"]`.
- Re-syncs on the `hf-seek` CustomEvent; every frame is a closed-form function of time (seeded PRNG only, no rAF loops, no Date.now).
- Renderer: GSAP, Canvas 2D, Seeded PRNG.
- External runtime dependencies: none (served locally).
- Local fonts: assets/Geist-Bold.ttf.

## Editing rules (from the source project)

1. Keep `data-composition-variables` a single-quoted attribute with plain `"` JSON. Never save it through Studio's Design panel.
2. Do not put `<canvas>` in static markup; create it at runtime.
3. Keep every visual state a function of t; seek-safety is what makes the block renderable.


<!-- ===== FILE: registry-blocks/cuboid-carousel/GUIDE.md ===== -->

---
name: cuboid-carousel
description: A chain of bevelled cuboids rides a travelling wave as a content carousel. HyperFrames block, 1920×1080, 6.666666666666667s, 40 variables.
---

# Cuboid Carousel

Rounded, bevelled cuboids carrying card content fly in from the right as one rigid group, cruise with a per-cuboid rotation stagger, decelerate to a hero hold, then exit left. Spacing is derived from the cuboid dimensions and the largest reachable X half-extent, so cuboids can never overlap. Forty variables carry the original DialKit schema: geometry, materials, lights, shadows, backdrop, camera and every segment duration and easing. Cards come from the built-in list or a JSON variable.

Composition id: `cuboid-carousel`. Duration 6.666666666666667 s at 30 fps, 1920×1080.

## Files

- `cuboid-carousel.html` (38 KB)
- `assets/Three-LICENSE.txt` (1 KB)
- `assets/addons/environments/RoomEnvironment.js` (5 KB)
- `assets/addons/utils/BufferGeometryUtils.js` (36 KB)
- `assets/cuboid-motion.js` (593 KB)
- `assets/gsap-3.14.2.min.js` (128 KB)
- `assets/GSAP-NOTICE.txt` (1 KB)
- `assets/three.core.min.js` (554 KB)
- `assets/three.module.min.js` (468 KB)

## Install

Install with `npx hyperframes add cuboid-carousel`; by default the files above land under `compositions/cuboid-carousel/`. Then mount the block from the host `index.html`:

```html
<div
  data-composition-id="cuboid-carousel"
  data-composition-src="compositions/cuboid-carousel/cuboid-carousel.html"
  data-start="0"
  data-duration="6.666666666666667"
  data-track-index="1"
  data-width="1920"
  data-height="1080"
></div>
```

Render with custom values by targeting the composition file directly:

```sh
npx --yes hyperframes@0.8.12 render 'compositions/cuboid-carousel/cuboid-carousel.html' --variables '{"cardsJson":"","heroCard":4}'
```

## Variables

Read at runtime via `window.__hyperframes.getVariables()`; declared on the composition root as `data-composition-variables` (single-quoted attribute, plain JSON).

| id                  | type   | default     | label / range                                        |
| ------------------- | ------ | ----------- | ---------------------------------------------------- |
| `cardsJson`         | string | `""`        | Content · Cards JSON (optional, see CARDS in source) |
| `heroCard`          | number | `4`         | Content · Hero card (1-based) 1–12 step 1            |
| `count`             | number | `8`         | Content · Repeating card count 1–12 step 1           |
| `gap`               | number | `0.01`      | Layout · Extra gap between cuboids 0–1.5 step 0.005  |
| `cuboidWidth`       | number | `1.7`       | Cuboid · Width 0.3–5 step 0.01                       |
| `cuboidHeight`      | number | `2.4`       | Cuboid · Height 0.3–6 step 0.01                      |
| `cuboidDepth`       | number | `0.14`      | Cuboid · Thickness (depth) 0.02–2 step 0.01          |
| `cornerRadius`      | number | `0.105`     | Cuboid · Corner radius 0–0.6 step 0.005              |
| `bevelSize`         | number | `0.03`      | Cuboid · Bevel size (edge chamfer) 0–0.3 step 0.001  |
| `bevelThickness`    | number | `0.04`      | Cuboid · Bevel thickness 0–0.3 step 0.001            |
| `smoothness`        | number | `32`        | Cuboid · Smoothness (segments) 1–32 step 1           |
| `bodyColor`         | color  | `"#242424"` | Cuboid · Body colour                                 |
| `roughness`         | number | `0.6`       | Cuboid · Roughness 0–1 step 0.01                     |
| `metalness`         | number | `0.4`       | Cuboid · Metalness 0–1 step 0.01                     |
| `heroScale`         | number | `1`         | Hero · Isolated scale 1–1.6 step 0.01                |
| `heroFillIntensity` | number | `0.55`      | Hero · Face light intensity 0–2 step 0.05            |
| `heroExitX`         | number | `288`       | Hero · Exit X rotation degrees -720–720 step 1       |
| `heroExitY`         | number | `-234`      | Hero · Exit Y rotation degrees -720–720 step 1       |
| `heroExitZ`         | number | `198`       | Hero · Exit Z rotation degrees -720–720 step 1       |
| `ambientIntensity`  | number | `0.35`      | Lights · Ambient intensity 0–4 step 0.01             |
| `ambientColor`      | color  | `"#ffffff"` | Lights · Ambient colour                              |
| `topIntensity`      | number | `3.1`       | Lights · Top rig intensity 0–12 step 0.05            |
| `topColor`          | color  | `"#ffffff"` | Lights · Top rig colour                              |
| `bottomIntensity`   | number | `2.15`      | Lights · Bottom rig intensity 0–12 step 0.05         |
| `bottomColor`       | color  | `"#ffcaad"` | Lights · Bottom rig colour                           |
| `keyIntensity`      | number | `5`         | Lights · Key rig intensity 0–12 step 0.05            |
| `keyColor`          | color  | `"#ffe9d6"` | Lights · Key rig colour                              |
| `shadowRadius`      | number | `44.5`      | Shadows · Softness at map size 2048 0–50 step 0.5    |
| `shadowMapSize`     | number | `2048`      | Shadows · Map size 512–4096 step 256                 |
| `backdrop`          | color  | `"#0b0d13"` | Background · Colour                                  |
| `cameraFov`         | number | `11`        | Camera · Initial Field of view 10–90 step 0.5        |
| `cameraX`           | number | `-1.65`     | Camera · Initial X -20–20 step 0.05                  |
| `cameraY`           | number | `8.5`       | Camera · Initial Y -20–20 step 0.05                  |
| `cameraZ`           | number | `-8.508708` | Camera · Initial Z (distance) -20–50 step 0.1        |
| `cameraSettleFrame` | number | `70`        | Camera · Settle frame (30 fps) 20–90 step 1          |
| `handheldStrength`  | number | `1`         | Camera · Handheld hold strength 0–1 step 0.05        |
| `cameraTargetFov`   | number | `34`        | Camera target · Field of view 10–90 step 0.5         |
| `cameraTargetX`     | number | `-7.25`     | Camera target · X -20–20 step 0.05                   |
| `cameraTargetY`     | number | `1.15`      | Camera target · Y -20–20 step 0.05                   |
| `cameraTargetZ`     | number | `6.2`       | Camera target · Z 2–50 step 0.1                      |

## Runtime contract

- One paused GSAP timeline registered as `window.__timelines["cuboid-carousel"]`.
- Re-syncs on the `hf-seek` CustomEvent; every frame is a closed-form function of time (seeded PRNG only, no rAF loops, no Date.now).
- Renderer: WebGL, GSAP, Canvas 2D, PMREM, Shadow maps. Budget roughly 350 MB per live instance; run one at a time.
- External runtime dependencies: `./assets/three.module.min.js`, `./assets/addons/`.
- Web fonts from Google Fonts: Inter.

## Editing rules (from the source project)

1. Keep `data-composition-variables` a single-quoted attribute with plain `"` JSON. Never save it through Studio's Design panel.
2. Do not put `<canvas>` in static markup; create it at runtime.
3. Keep every visual state a function of t; seek-safety is what makes the block renderable.


<!-- ===== FILE: registry-blocks/frost-sequence-camera-orbit/GUIDE.md ===== -->

---
name: frost-sequence-camera-orbit
description: An orbiting camera follows an ice logo as it breaks apart, reforms into two text moments, and fades. HyperFrames block, 1920×1080, 22.5s, 216 variables.
---

# Frost Sequence Camera Orbit

A complete 22.5-second ice sequence: logo, first text, second text, breakup, and fade. The camera orbits the fixed objects with slower front-facing passes for reading. The same particle field carries each transition. Customize the two text moments and SVG logo; the source includes editable camera and assembly timing.

Composition id: `frost-sequence-rig`. Duration 22.5 s at 30 fps, 1920×1080.

## Files

- `frost-sequence-camera-orbit.html` (131 KB)
- `assets/example-logo.svg` (1 KB)
- `assets/fonts/Geist-Bold.ttf` (65 KB)
- `assets/fonts/Geist-OFL.txt` (4 KB)
- `assets/fonts/Geist-Regular.ttf` (65 KB)
- `assets/fonts/Geist-SemiBold.ttf` (65 KB)
- `assets/frost.js` (1.5 MB)
- `assets/Three-LICENSE.txt` (1 KB)
- `assets/ThreeMeshBVH-LICENSE.txt` (1 KB)
- `assets/OpentypeJS-LICENSE.txt` (1 KB)
- `assets/Clipper-LICENSE.txt` (3 KB)
- `assets/gsap-3.14.2.min.js` (128 KB)
- `assets/GSAP-NOTICE.txt` (1 KB)
- `assets/logo.svg` (1 KB)
- `assets/shards-atlas.png` (fetched from the CDN at install)
- `assets/test-mark.svg` (1 KB)
- `assets/textures/bluenoise64.png` (12 KB)
- `assets/textures/ice-inclusions-generated.png` (fetched from the CDN at install)

## Install

Install with `npx hyperframes add frost-sequence-camera-orbit`; by default the files above land under `compositions/frost-sequence-camera-orbit/`. Then mount the block from the host `index.html`:

```html
<div
  data-composition-id="frost-sequence-rig"
  data-composition-src="compositions/frost-sequence-camera-orbit/frost-sequence-camera-orbit.html"
  data-start="0"
  data-duration="22.5"
  data-track-index="1"
  data-width="1920"
  data-height="1080"
></div>
```

Render with custom values by targeting the composition file directly:

```sh
npx --yes hyperframes@0.8.12 render 'compositions/frost-sequence-camera-orbit/frost-sequence-camera-orbit.html' --variables '{"headline1":"Hard to|break.","headline2":"Easy to|remember."}'
```

## Variables

Read at runtime via `window.__hyperframes.getVariables()`; declared on the composition root as `data-composition-variables` (single-quoted attribute, plain JSON).

| id                          | type    | default             | label / range                                                                                 |
| --------------------------- | ------- | ------------------- | --------------------------------------------------------------------------------------------- | ------------- | -------------------------- | ------- | ------- |
| `headline1`                 | string  | `"Hard to           | break."`                                                                                      | First text (  | = line break) max 60 chars |
| `headline2`                 | string  | `"Easy to           | remember."`                                                                                   | Second text ( | = line break) max 60 chars |
| `logoUrl`                   | string  | `"assets/logo.svg"` | Logo SVG asset path (upload in Assets, then paste path) max 200 chars                         |
| `assemblyMode`              | enum    | `"hybrid"`          | Assembly response (physical                                                                   | directed      | hybrid)                    |
| `materialBaseColor`         | color   | `"#ffffff"`         | Base color                                                                                    |
| `baseRoughness`             | number  | `0.31`              | Base roughness 0–0.5 step 0.005                                                               |
| `materialTransmission`      | boolean | `true`              | Transmission                                                                                  |
| `materialBacklight`         | number  | `0.27`              | Backlight through ice 0–2 step 0.01                                                           |
| `ior`                       | number  | `1.675`             | Index of refraction 1–2 step 0.005                                                            |
| `thicknessScale`            | number  | `2.04`              | Thickness scale 0.1–3 step 0.01                                                               |
| `materialAbsorption`        | boolean | `true`              | Absorption / tint                                                                             |
| `attenuationColor`          | color   | `"#d5f4ff"`         | Attenuation colour (white = no absorption, clear glass)                                       |
| `attenuationDistance`       | number  | `6.54`              | Attenuation distance 0.05–12 step 0.01                                                        |
| `materialDispersion`        | boolean | `false`             | Dispersion                                                                                    |
| `dispersion`                | number  | `0.12`              | Dispersion (0 = off; on/off reloads) 0–0.3 step 0.005                                         |
| `materialReflections`       | boolean | `true`              | Reflections                                                                                   |
| `envIntensity`              | number  | `2.04`              | Environment intensity 0–3 step 0.01                                                           |
| `specularIntensity`         | number  | `1.44`              | Specular intensity 0–2 step 0.01                                                              |
| `materialFrost`             | boolean | `true`              | Frost                                                                                         |
| `materialInteriorFrost`     | number  | `0`                 | Uniform frost 0–1 step 0.01                                                                   |
| `frostScale`                | number  | `0.7`               | Scale 0.2–6 step 0.05                                                                         |
| `frostThreshold`            | number  | `0.62`              | Threshold (1 = no frost, clear glass) 0–1 step 0.01                                           |
| `frostSoftness`             | number  | `0.24`              | Softness 0.01–1 step 0.01                                                                     |
| `frostRoughness`            | number  | `0.73`              | Roughness 0–1 step 0.01                                                                       |
| `frostDiffuse`              | number  | `0.11`              | Diffuse (how much light frosted areas catch) 0–1 step 0.01                                    |
| `materialSurfaceBumps`      | boolean | `false`             | Object surface bumps / crack notches                                                          |
| `materialCrystals`          | boolean | `true`              | Crystal bumps                                                                                 |
| `crystalBump`               | number  | `0.01`              | Crystal bump 0–1 step 0.01                                                                    |
| `crystalScale`              | number  | `4`                 | Crystal scale 4–80 step 1                                                                     |
| `materialGrain`             | boolean | `true`              | Grain bumps                                                                                   |
| `materialGrainAmount`       | number  | `0.47`              | Grain strength 0–2 step 0.01                                                                  |
| `materialGrainScale`        | number  | `150`               | Grain scale 1–150 step 1                                                                      |
| `materialCutNormals`        | boolean | `true`              | Fracture normals                                                                              |
| `materialMicro`             | boolean | `true`              | Micro bumps                                                                                   |
| `microBump`                 | number  | `0.445`             | Micro bump 0–1 step 0.005                                                                     |
| `microScale`                | number  | `10`                | Micro scale 10–200 step 1                                                                     |
| `microCoverage`             | number  | `0.25`              | Micro coverage 0–1 step 0.01                                                                  |
| `bumpMaskScale`             | number  | `1.45`              | Mask scale 0.1–6 step 0.05                                                                    |
| `materialRipples`           | boolean | `true`              | Ripples                                                                                       |
| `rippleBump`                | number  | `0.22`              | Ripple bump 0–1 step 0.01                                                                     |
| `rippleScale`               | number  | `23`                | Ripple scale 2–30 step 0.5                                                                    |
| `materialSmudges`           | boolean | `true`              | Smudges                                                                                       |
| `smudgeAmount`              | number  | `0.78`              | Amount 0–1 step 0.01                                                                          |
| `smudgeCoverage`            | number  | `0.58`              | Coverage 0–1 step 0.01                                                                        |
| `smudgeMaskScale`           | number  | `1.85`              | Mask scale 0.1–6 step 0.05                                                                    |
| `smudgeAnisotropy`          | number  | `16.5`              | Anisotropy 1–20 step 0.5                                                                      |
| `smudgeRoughness`           | number  | `0.75`              | Roughness 0–1 step 0.01                                                                       |
| `smudgeWhiteness`           | number  | `0.035`             | Whiteness 0–0.5 step 0.005                                                                    |
| `smudgeScale`               | number  | `1.3`               | Scale 0.5–10 step 0.1                                                                         |
| `materialCracks`            | boolean | `true`              | Cracks                                                                                        |
| `crackLargeScale`           | number  | `2.45`              | Large scale 0.3–8 step 0.05                                                                   |
| `crackWarp`                 | number  | `0.22`              | Warp 0–1.5 step 0.01                                                                          |
| `crackCoverage`             | number  | `0.19`              | Coverage 0–1 step 0.01                                                                        |
| `crackRegionScale`          | number  | `1.8`               | Region scale 0.1–4 step 0.05                                                                  |
| `crackRegionCoverage`       | number  | `0.6`               | Region coverage 0–1 step 0.01                                                                 |
| `veinScale`                 | number  | `8`                 | Vein scale 1–20 step 0.25                                                                     |
| `veinContrast`              | number  | `0.55`              | Vein contrast 0–1 step 0.01                                                                   |
| `crackWidth`                | number  | `0.0025`            | Width 0.0005–0.02 step 0.0005                                                                 |
| `crackBrightness`           | number  | `0.65`              | Brightness 0–3 step 0.01                                                                      |
| `crackDarkness`             | number  | `0.69`              | Darkness 0–1 step 0.01                                                                        |
| `crackRefraction`           | number  | `0.076`             | Refraction 0–0.1 step 0.001                                                                   |
| `crackSurfaceStrength`      | number  | `0.16`              | Surface strength 0–1 step 0.01                                                                |
| `fineScale`                 | number  | `18.4`              | Fine scale 2–20 step 0.1                                                                      |
| `fineAmount`                | number  | `0.52`              | Fine amount 0–1 step 0.01                                                                     |
| `fineCoverage`              | number  | `1`                 | Fine coverage 0–1 step 0.01                                                                   |
| `materialScatter`           | boolean | `true`              | Internal scattering                                                                           |
| `materialInclusionScale`    | number  | `0.05`              | Inclusion scale 0.05–3 step 0.01                                                              |
| `materialInclusionAmount`   | number  | `2`                 | Photographic inclusions 0–2 step 0.01                                                         |
| `interiorScatter`           | number  | `0.09`              | Interior scatter 0–1 step 0.01                                                                |
| `materialClearcoat`         | boolean | `true`              | Clearcoat                                                                                     |
| `clearcoat`                 | number  | `0`                 | Clearcoat 0–1 step 0.01                                                                       |
| `clearcoatRoughness`        | number  | `0`                 | Clearcoat roughness 0–1 step 0.005                                                            |
| `materialShardNormals`      | boolean | `true`              | Shard normals                                                                                 |
| `spriteNormal`              | number  | `0.15`              | Sprite normal strength 0–2.5 step 0.05                                                        |
| `materialShardFrost`        | boolean | `true`              | Shard frost                                                                                   |
| `materialShardTransmission` | boolean | `true`              | Shard transparency                                                                            |
| `spriteSeeThrough`          | number  | `1`                 | See-through (0 = off; on/off reloads) 0–1 step 0.01                                           |
| `materialShardReflections`  | boolean | `true`              | Shard reflections                                                                             |
| `minPixelSize`              | number  | `0.25`              | Minimum pixel size 0–4 step 0.05                                                              |
| `grainSizeMultiplier`       | number  | `1.05`              | Grain size multiplier 0.2–4 step 0.05                                                         |
| `spriteSize`                | number  | `1.9`               | Sprite size 0.3–4 step 0.05                                                                   |
| `spriteTilt`                | number  | `12`                | Sprite tilt 0–70 step 1                                                                       |
| `spriteAlphaCut`            | number  | `0.6`               | Alpha cut 0.05–0.6 step 0.01                                                                  |
| `fontWeight`                | enum    | `"600"`             | Type · Weight (Geist) (400                                                                    | 600           | 700)                       |
| `letterSpacing`             | number  | `0.01`              | Type · Letter spacing -0.1–0.4 step 0.005                                                     |
| `shardAmount`               | number  | `0.44`              | Shards · Visible fraction of the broken volume (Powder amount) 0.02–1 step 0.01               |
| `strayDust`                 | number  | `24`                | Shards · Ambient dust motes around the object (the experiment had 40) 0–200 step 1            |
| `sliceRadius`               | number  | `0.6`               | Break · First (diagonal) slice radius 0.05–1.5 step 0.01                                      |
| `sliceStrength`             | number  | `21.5`              | Break · First slice strength 1–40 step 0.5                                                    |
| `finalEjectBoost`           | number  | `2.5`               | Break · Last break: eject speed and speed cap multiplier 1–6 step 0.1                         |
| `shatterRadius`             | number  | `0.45`              | Break · Follow-up slice radius (sets their spacing too) 0.1–1.5 step 0.01                     |
| `shatterStrength`           | number  | `32.5`              | Break · Follow-up slice strength 1–40 step 0.5                                                |
| `cutThreshold`              | number  | `0.3`               | Tune break · Cut threshold (surface gone above this erosion) 0.3–0.98 step 0.01               |
| `cutSoftness`               | number  | `0.19`              | Tune break · Cut softness 0.005–0.3 step 0.005                                                |
| `edgeWidth`                 | number  | `0.19`              | Tune break · Crumbly edge band width 0.05–0.8 step 0.01                                       |
| `edgeInset`                 | number  | `0`                 | Tune break · Edge inset 0–0.3 step 0.005                                                      |
| `brushSoftness`             | number  | `0.15`              | Tune break · Brush softness (edge falloff of a slice) 0.02–1 step 0.01                        |
| `brushNoise`                | number  | `0.4`               | Tune break · Brush noise (ragged boundary) 0–1 step 0.01                                      |
| `crumbleRate`               | number  | `4.3`               | Tune break · Crumble rate along cracks (high = the whole shape goes at once) 0–6 step 0.05    |
| `crumbleCrackBias`          | number  | `5.1`               | Tune break · Crumble crack bias 0–6 step 0.05                                                 |
| `crumbleDuration`           | number  | `0.35`              | Tune break · Crumble duration after a stroke 0–2 step 0.01                                    |
| `ejectSpeed`                | number  | `0.91`              | Flight · Eject speed 0–4 step 0.01                                                            |
| `ejectSpread`               | number  | `0.48`              | Flight · Eject spread along the normal 0–3 step 0.01                                          |
| `ejectTurbulence`           | number  | `4`                 | Flight · Eject turbulence 0–4 step 0.01                                                       |
| `drag`                      | number  | `0`                 | Flight · Drag (speed decays by this per second) 0–8 step 0.01                                 |
| `gravity`                   | number  | `0`                 | Flight · Gravity (0 = shards never fall) 0–2 step 0.005                                       |
| `turbulence`                | number  | `4`                 | Flight · Turbulence strength (curl noise) 0–4 step 0.01                                       |
| `turbulenceScale`           | number  | `2.65`              | Flight · Turbulence scale 0.2–8 step 0.05                                                     |
| `turbulenceDecay`           | number  | `3.65`              | Flight · Turbulence decay with age (low = keeps swirling) 0.05–4 step 0.01                    |
| `clumpCohesion`             | number  | `0.9`               | Flight · Clump cohesion (shards orbit a leader; 0 = none) 0–10 step 0.05                      |
| `followObject`              | number  | `30`                | Flight · Shards follow the object motion for (s; 30 = whole flight) 0–30 step 0.5             |
| `settleTime`                | number  | `2.2`               | Flight · Settle time (velocity is killed after this; 12 = never) 0.3–12 step 0.05             |
| `settledDrift`              | number  | `1`                 | Flight · Organic drift once settled (curl noise) 0–1 step 0.005                               |
| `maxSpeed`                  | number  | `26.3`              | Flight · Speed cap 1–40 step 0.1                                                              |
| `repelStrength`             | number  | `30`                | Flight · Push out of the solid shape while it breaks 0–30 step 0.1                            |
| `repelRange`                | number  | `0.97`              | Flight · Push range outside the surface 0.02–2 step 0.01                                      |
| `repelRadial`               | number  | `17.5`              | Flight · Push away from the shape centre (clears pockets and the hole) 0–60 step 0.5          |
| `repelRadialRange`          | number  | `3.3`               | Flight · Radial push range (object radii) 1–4 step 0.05                                       |
| `tumble`                    | number  | `1.05`              | Flight · Tumble rate 0–12 step 0.05                                                           |
| `returnGroupStagger`        | number  | `1.35`              | Assembly · Regional delay (seconds) 0–1.5 step 0.05                                           |
| `returnGroupScale`          | number  | `2.55`              | Assembly · Region / noise size 0.1–3 step 0.05                                                |
| `returnGroupSeed`           | number  | `60765`             | Return · Group timing seed 0–65535 step 1                                                     |
| `formSpread`                | number  | `0`                 | Return · Wave spread (nearest shards leave first, seconds) 0–4 step 0.05                      |
| `waveReach`                 | number  | `10`                | Return · Distance over which the wave spreads 0.2–10 step 0.1                                 |
| `formJitter`                | number  | `2.8`               | Return · Per-shard stagger (random delay up to this) 0–3 step 0.05                            |
| `formFill`                  | number  | `3`                 | Return · Fill-in rate for voxels no shard returns to 0.05–3 step 0.05                         |
| `returnSpring`              | number  | `29.9`              | Return · Spring stiffness 0.5–40 step 0.1                                                     |
| `returnDamping`             | number  | `1.34`              | Return · Spring damping 0.2–2 step 0.01                                                       |
| `returnRamp`                | number  | `0.45`              | Return · Spring ramp-in (seconds until it pulls at full strength) 0–3 step 0.05               |
| `returnMaxSpeed`            | number  | `60`                | Return · Speed cap on the way home 1–60 step 0.5                                              |
| `alignToSurface`            | number  | `1`                 | Return · Shards turn to lie on the surface (0 = keep tumbling) 0–1 step 0.01                  |
| `alignCurve`                | number  | `3.75`              | Return · Alignment curve over the flight home (1 linear, higher = later) 0.2–4 step 0.05      |
| `healRate`                  | number  | `3`                 | Return · Neighbour heal rate 0.02–3 step 0.01                                                 |
| `cellRestore`               | number  | `60`                | Return · Cell restore rate 0–60 step 0.5                                                      |
| `landedFade`                | number  | `1.65`              | Return · Landed shard fade 0–2 step 0.01                                                      |
| `refrostTime`               | number  | `10.6`              | Return · Refrost time 0.2–12 step 0.1                                                         |
| `keyColor`                  | color   | `"#f0f7ff"`         | Light · Key colour                                                                            |
| `keyIntensity`              | number  | `5.05`              | Light · Key intensity 0–12 step 0.05                                                          |
| `keyElevation`              | number  | `42`                | Light · Key elevation 10–89 step 0.5                                                          |
| `keyAzimuth`                | number  | `-38`               | Light · Key azimuth -90–90 step 0.5                                                           |
| `keySize`                   | number  | `1.25`              | Light · Key size (softbox) 0.2–3 step 0.01                                                    |
| `fill`                      | number  | `0.18`              | Light · Fill intensity (hemisphere, diffuse only: barely shows on clear ice) 0–1.5 step 0.005 |
| `fillColor`                 | color   | `"#cadde9"`         | Light · Fill sky colour                                                                       |
| `fillGroundColor`           | color   | `"#172635"`         | Light · Fill ground colour                                                                    |
| `rim`                       | number  | `2.5`               | Light · Rim spot intensity 0–5 step 0.01                                                      |
| `rimColor`                  | color   | `"#d9f1ff"`         | Light · Rim colour                                                                            |
| `rimElevation`              | number  | `20`                | Light · Rim elevation (0 = straight behind) 0–89 step 0.5                                     |
| `swayAmplitude`             | number  | `0`                 | Light · Key sway amplitude 0–0.15 step 0.001                                                  |
| `swayPeriod`                | number  | `35`                | Light · Key sway period 2–40 step 0.5                                                         |
| `envSoftbox`                | number  | `1.1`               | Light · Environment softbox (the main light on glass) 0–3 step 0.01                           |
| `envRim`                    | number  | `1.4`               | Light · Environment rim strip 0–3 step 0.01                                                   |
| `envFill`                   | number  | `0.22`              | Light · Environment front fill 0–1 step 0.005                                                 |
| `backdropTop`               | color   | `"#050505"`         | Backdrop · Top colour                                                                         |
| `backdropMid`               | color   | `"#050505"`         | Backdrop · Mid colour                                                                         |
| `backdropBottom`            | color   | `"#050505"`         | Backdrop · Bottom colour                                                                      |
| `backdropCenterX`           | number  | `0.73`              | Backdrop · Bloom centre X 0–1 step 0.005                                                      |
| `backdropCenterY`           | number  | `0.22`              | Backdrop · Bloom centre Y 0–2 step 0.005                                                      |
| `backdropRadius`            | number  | `0.8`               | Backdrop · Bloom radius 0.1–2 step 0.005                                                      |
| `backdropFalloff`           | number  | `0.85`              | Backdrop · Bloom falloff 0.5–6 step 0.01                                                      |
| `backdropNoise`             | number  | `0`                 | Backdrop · Dither noise 0–3 step 0.05                                                         |
| `bloomThreshold`            | number  | `3`                 | Post · Bloom threshold 0–3 step 0.01                                                          |
| `bloomIntensity`            | number  | `0.04`              | Post · Bloom intensity 0–1.5 step 0.005                                                       |
| `bloomRadius`               | number  | `1`                 | Post · Bloom radius 0–1 step 0.005                                                            |
| `monochrome`                | number  | `0.04`              | Post · Monochrome 0–1 step 0.01                                                               |
| `tonemap`                   | enum    | `"aces"`            | Post · Tonemap (agx                                                                           | aces          | neutral                    | linear) |
| `exposure`                  | number  | `1`                 | Post · Exposure 0.1–4 step 0.01                                                               |
| `contrast`                  | number  | `1.03`              | Post · Contrast 0.6–1.6 step 0.005                                                            |
| `blackLift`                 | number  | `0`                 | Post · Black lift 0–0.1 step 0.001                                                            |
| `vignetteStrength`          | number  | `0.14`              | Post · Vignette strength 0–1 step 0.005                                                       |
| `vignetteSoftness`          | number  | `1.2`               | Post · Vignette softness 0.1–1.5 step 0.005                                                   |
| `vignetteRadius`            | number  | `1.2`               | Post · Vignette radius 0.2–1.6 step 0.005                                                     |
| `grainStrength`             | number  | `0`                 | Post · Film grain 0–0.15 step 0.001                                                           |
| `quality`                   | enum    | `"full"`            | Performance · Quality profile (full                                                           | lite)         |
| `upscaler`                  | enum    | `"fsr1"`            | Performance · Upscaler (fsr1                                                                  | taau          | bilinear                   | native) |
| `renderScale`               | number  | `1`                 | Performance · Scene resolution scale (upscaled to 1080p) 0.35–1 step 0.05                     |
| `shapeResolution`           | enum    | `"256"`             | Shape voxel resolution (128                                                                   | 256           | 384)                       |
| `erosionResolution`         | enum    | `"96"`              | Performance · Erosion field resolution (voxels per axis) (64                                  | 96            | 128                        | 192)    |
| `particleCount`             | enum    | `"100k"`            | Performance · Powder particles (100k                                                          | 250k          | 500k                       | 1M)     |
| `logoMeshDetail`            | number  | `2`                 | Shape · Logo mesh detail (1-4; higher = finer surface) 1–4 step 1                             |
| `deformStrength`            | number  | `0`                 | Geometry · Ice deformation strength (0 = original) 0–0.08 step 0.001                          |
| `deformScale`               | number  | `0.41`              | Geometry · Noise feature size (larger = broader) 0.001–0.5 step 0.001                         |
| `deformSeed`                | number  | `7`                 | Geometry · Deformation seed 0–65535 step 1                                                    |
| `rimAzimuth`                | number  | `-146`              | Light · Rim azimuth -180–180 step 1                                                           |
| `rimAngle`                  | number  | `26`                | Light · Rim beam angle 10–89 step 1                                                           |
| `rimSize`                   | number  | `0.45`              | Light · Rim reflection size 0.1–3 step 0.05                                                   |
| `fillReflectionStrength`    | number  | `0.3`               | Light · Fill reflection strength 0–2 step 0.01                                                |
| `accentCoolIntensity`       | number  | `3.71`              | Studio Cool accent · intensity 0–4 step 0.01                                                  |
| `accentCoolReflection`      | number  | `2.31`              | Studio Cool accent · reflection 0–3 step 0.01                                                 |
| `accentCoolElevation`       | number  | `63`                | Studio Cool accent · elevation -85–85 step 1                                                  |
| `accentCoolAzimuth`         | number  | `22`                | Studio Cool accent · azimuth -180–180 step 1                                                  |
| `accentCoolSize`            | number  | `2.65`              | Studio Cool accent · size 0.1–3 step 0.05                                                     |
| `accentCoolColor`           | color   | `"#ff5900"`         | Studio Cool accent · color                                                                    |
| `accentWarmIntensity`       | number  | `2.99`              | Studio Warm accent · intensity 0–4 step 0.01                                                  |
| `accentWarmReflection`      | number  | `0.34`              | Studio Warm accent · reflection 0–3 step 0.01                                                 |
| `accentWarmElevation`       | number  | `30`                | Studio Warm accent · elevation -85–85 step 1                                                  |
| `accentWarmAzimuth`         | number  | `-30`               | Studio Warm accent · azimuth -180–180 step 1                                                  |
| `accentWarmSize`            | number  | `1.2`               | Studio Warm accent · size 0.1–3 step 0.05                                                     |
| `accentWarmColor`           | color   | `"#75aaff"`         | Studio Warm accent · color                                                                    |
| `returnNoiseAmount`         | enum    | `"2"`               | Assembly · Regional pattern (2                                                                | 1             | 0)                         |
| `assemblyFrontDuration`     | number  | `3.2`               | Assembly · Growth duration (seconds) 0–6 step 0.05                                            |
| `assemblyOriginX`           | number  | `-0.65`             | Assembly · Growth start X -1–1 step 0.01                                                      |
| `assemblyOriginY`           | number  | `0.55`              | Assembly · Growth start Y -1–1 step 0.01                                                      |
| `assemblyAngle`             | number  | `-35`               | Assembly · Seam direction (degrees) -180–180 step 1                                           |
| `assemblySpread`            | number  | `0.65`              | Assembly · Outward spread vs seam travel 0–1 step 0.01                                        |
| `assemblyFrontNoise`        | number  | `0.35`              | Assembly · Growth edge irregularity 0–1 step 0.01                                             |
| `assemblySpeedVariation`    | number  | `0.65`              | Assembly · Return speed variation 0–1 step 0.01                                               |
| `assemblyBend`              | number  | `1.2`               | Assembly · Approach path bend 0–3 step 0.05                                                   |
| `assemblySwirl`             | number  | `1.1`               | Assembly · Approach twist 0–3 step 0.05                                                       |
| `assemblyLandingVariation`  | number  | `0.8`               | Assembly · Landing transition variation 0–1 step 0.01                                         |
| `rendererProfile`           | enum    | `"studio"`          | Renderer experiment (reload required) (original                                               | lookup        | mesh                       | studio  | matcap) |
| `textWidth`                 | number  | `6.5`               | Type · Headline block width (the mark is 2.6 wide) 1.2–9 step 0.05                            |
| `textLineHeight`            | number  | `0.95`              | Type · Line height 0.7–1.4 step 0.01                                                          |
| `textDepth`                 | number  | `0.16`              | Type · Extrusion depth (fraction of the font size) 0.05–0.8 step 0.01                         |
| `textBevel`                 | number  | `0.04`              | Type · Bevel (fraction of the font size) 0–0.12 step 0.005                                    |
| `textCorner`                | number  | `0.008`             | Type · Corner rounding (fraction of the font size) 0–0.06 step 0.002                          |
| `textMeshDetail`            | number  | `4`                 | Type · Text mesh detail (1-4; higher = smoother deformation) 1–4 step 1                       |

## Runtime contract

- One paused GSAP timeline registered as `window.__timelines["frost-sequence-rig"]`.
- Re-syncs on the `hf-seek` CustomEvent; every frame is a closed-form function of time (seeded PRNG only, no rAF loops, no Date.now).
- Renderer: WebGPU, GSAP, Matcap.
- External runtime dependencies: none (served locally).

## Editing rules (from the source project)

1. Keep `data-composition-variables` a single-quoted attribute with plain `"` JSON. Never save it through Studio's Design panel.
2. Do not put `<canvas>` in static markup; create it at runtime.
3. Keep every visual state a function of t; seek-safety is what makes the block renderable.


<!-- ===== FILE: registry-blocks/glass-shard-title/GUIDE.md ===== -->

---
name: glass-shard-title
description: Glass shards fly in through fog and tile themselves into the headline. HyperFrames block, 1920×1080, 12.16s, 19 variables.
---

# Glass Shard Title

Voronoi-cut glass panes fly in from depth, rotating, and land as a tiled silhouette of the headline, then fly out past the camera. Each shard is a Sutherland–Hodgman clip of a jittered blob against its Voronoi cell, so the pieces always cover the type. Glass and matcap surfaces get per-fragment fog; the z-flight is decoupled from the ease so shards visibly traverse it. Tile count 1 gives a single pane.

Composition id: `glass-shard-title`. Duration 12.16 s at 30 fps, 1920×1080.

## Files

- `glass-shard-title.html` (16 KB)
- `assets/ferndale_studio_01_1k.hdr` (1.6 MB)
- `assets/fonts/Geist-Bold.ttf` (65 KB)
- `assets/fonts/Geist-Regular.ttf` (65 KB)
- `assets/fonts/Geist-SemiBold.ttf` (65 KB)
- `assets/fonts/Geist-OFL.txt` (4 KB)
- `assets/fonts/cormorant-garamond.woff2` (37 KB)
- `assets/fonts/CormorantGaramond-OFL.txt` (4 KB)
- `assets/glass-main.js` (549 KB)
- `assets/Three-LICENSE.txt` (1 KB)
- `assets/matcap-1.png` (fetched from the CDN at install)

## Install

Install with `npx hyperframes add glass-shard-title`; by default the files above land under `compositions/glass-shard-title/`. Then mount the block from the host `index.html`:

```html
<div
  data-composition-id="glass-shard-title"
  data-composition-src="compositions/glass-shard-title/glass-shard-title.html"
  data-start="0"
  data-duration="12.16"
  data-track-index="1"
  data-width="1920"
  data-height="1080"
></div>
```

Render with custom values by targeting the composition file directly:

```sh
npx --yes hyperframes@0.8.12 render 'compositions/glass-shard-title/glass-shard-title.html' --variables '{"headline":"Designed in glass","tileCount":8}'
```

## Variables

Read at runtime via `window.__hyperframes.getVariables()`; declared on the composition root as `data-composition-variables` (single-quoted attribute, plain JSON).

| id               | type   | default               | label / range                                 |
| ---------------- | ------ | --------------------- | --------------------------------------------- |
| `headline`       | string | `"Designed in glass"` | Headline max 40 chars                         |
| `tileCount`      | number | `8`                   | Tiles 1–400 step 1                            |
| `roundness`      | number | `0.4`                 | Roundness (0-1) 0–1 step 0.01                 |
| `bevel`          | number | `0.35`                | Bevel (0-1) 0–1 step 0.01                     |
| `meshSmooth`     | number | `0.6`                 | Surface smoothness (0-1) 0–1 step 0.01        |
| `flyInTime`      | number | `2.3`                 | Fly-in time (s) 0.2–6 step 0.05               |
| `flyOutTime`     | number | `2.4`                 | Fly-out time (s) 0.2–6 step 0.05              |
| `stagger`        | number | `0.27`                | Stagger (0-1) 0–1 step 0.01                   |
| `flyInRotation`  | number | `5`                   | Fly-in rotation (0-60) 0–60 step 0.1          |
| `flyOutRotation` | number | `6`                   | Fly-out rotation (0-6) 0–6 step 0.1           |
| `chaos`          | number | `0.25`                | Outline chaos (0-1) 0–1 step 0.01             |
| `padding`        | number | `1`                   | Edge padding (0-1) 0–1 step 0.01              |
| `sizeVariance`   | number | `0.35`                | Size variance (0-1) 0–1 step 0.01             |
| `gap`            | number | `0.03`                | Tile gap 0–0.3 step 0.002                     |
| `easePow`        | number | `10`                  | Fly-in position ease (1-10) 1–10 step 0.1     |
| `sideDist`       | number | `3`                   | Side fly distance 0–60 step 0.5               |
| `zDist`          | number | `-42`                 | Z fly-from (negative) -400–0 step 2           |
| `zOut`           | number | `14`                  | Z fly-out to (+ = past camera) -400–60 step 2 |
| `fog`            | number | `36`                  | Fog distance (0 = off) 0–400 step 2           |

## Runtime contract

- One paused GSAP timeline registered as `window.__timelines["glass-shard-title"]`.
- Re-syncs on the `hf-seek` CustomEvent; every frame is a closed-form function of time (seeded PRNG only, no rAF loops, no Date.now).
- Renderer: three.js 0.181.2 (bundled), GSAP 3.14.2, Canvas 2D, GLSL shaders, HDR environment, Matcap, Seeded PRNG, d3-delaunay, Shadow maps. Budget roughly 350 MB per live instance; run one at a time.
- External runtime dependencies: `https://cdn.jsdelivr.net/npm/gsap@3.14.2/dist/gsap.min.js`, `https://cdn.jsdelivr.net/npm/d3-delaunay@6.0.4/dist/d3-delaunay.min.js`.
- Local fonts: assets/fonts/Geist-Regular.ttf, assets/fonts/Geist-SemiBold.ttf, assets/fonts/Geist-Bold.ttf.
- Bundled code is inlined into the composition (assets/glass-main.js); rebuild with esbuild and re-inline after editing the .mjs source.

## Editing rules (from the source project)

1. Keep `data-composition-variables` a single-quoted attribute with plain `"` JSON. Never save it through Studio's Design panel.
2. Do not put `<canvas>` in static markup; create it at runtime.
3. Keep every visual state a function of t; seek-safety is what makes the block renderable.


<!-- ===== FILE: registry-blocks/orbit-card/GUIDE.md ===== -->

---
name: orbit-card
description: A single feature card orbits a dot sphere on approved Blender camera motion. HyperFrames block, 1920×1080, 10s, 4 variables.
---

# Orbit Card

One centred feature card with a circular cut-out framing a dot sphere. The card enters from the right (0.25–1.80 s), holds with a subtle bob and depth drift, orbits a full turn around the sphere's centre (smoothstep between 4.97 and 5.97 s), and exits left (7.35–8.55 s). The camera path and card F-curves are exported from the approved Blender rig at 30 fps and interpolated; the sphere keeps its own translation and a constant spin. Title, description, accent and the orbit angle are variables; 180° and 720° work without touching keys.

Composition id: `orbit-card`. Duration 10 s at 30 fps, 1920×1080.

## Files

- `orbit-card.html` (3 KB)
- `assets/Archivo-LICENSE.txt` (4 KB)
- `assets/Three-LICENSE.txt` (1 KB)
- `assets/archivo-regular.ttf` (108 KB)
- `assets/archivo-semibold.ttf` (109 KB)
- `assets/gsap-3.14.2.min.js` (128 KB)
- `assets/GSAP-NOTICE.txt` (1 KB)
- `assets/orbit-motion.js` (59 KB)
- `assets/orbit-scene.js` (8 KB)
- `assets/three.core.min.js` (554 KB)
- `assets/three.module.min.js` (468 KB)

## Install

Install with `npx hyperframes add orbit-card`; by default the files above land under `compositions/orbit-card/`. Then mount the block from the host `index.html`:

```html
<div
  data-composition-id="orbit-card"
  data-composition-src="compositions/orbit-card/orbit-card.html"
  data-start="0"
  data-duration="10"
  data-track-index="1"
  data-width="1920"
  data-height="1080"
></div>
```

Render with custom values by targeting the composition file directly:

```sh
npx --yes hyperframes@0.8.12 render 'compositions/orbit-card/orbit-card.html' --variables '{"feature1Title":"Always in sync","feature1Desc":"Changes reach every screen the moment they happen."}'
```

## Variables

Read at runtime via `window.__hyperframes.getVariables()`; declared on the composition root as `data-composition-variables` (single-quoted attribute, plain JSON).

| id                 | type   | default                                                | label / range                          |
| ------------------ | ------ | ------------------------------------------------------ | -------------------------------------- |
| `feature1Title`    | string | `"Always in sync"`                                     | Card title max 28 chars                |
| `feature1Desc`     | string | `"Changes reach every screen the moment they happen."` | Card description max 110 chars         |
| `feature1Accent`   | color  | `"#4cc9ff"`                                            | Card accent                            |
| `cardOrbitDegrees` | number | `360`                                                  | Card orbit degrees -36000–36000 step 1 |

## Runtime contract

- One paused GSAP timeline registered as `window.__timelines["orbit-card"]`.
- Re-syncs on the `hf-seek` CustomEvent; every frame is a closed-form function of time (seeded PRNG only, no rAF loops, no Date.now).
- Renderer: GSAP.
- External runtime dependencies: none (served locally).
- Local fonts: assets/archivo-regular.ttf, assets/archivo-semibold.ttf.

## Editing rules (from the source project)

1. Keep `data-composition-variables` a single-quoted attribute with plain `"` JSON. Never save it through Studio's Design panel.
2. Do not put `<canvas>` in static markup; create it at runtime.
3. Keep every visual state a function of t; seek-safety is what makes the block renderable.


<!-- ===== FILE: registry-blocks/wireframe-portal-title/GUIDE.md ===== -->

---
name: wireframe-portal-title
description: A wireframe portal bursts open, the title comes through, then its letters swap into a second phrase. HyperFrames block, 1920×1080, 8s, 9 variables.
---

# Wireframe Portal Title

Extruded wireframe letterforms are built from the bundled Geist face with a TTF loader and polygon offsetting, then revealed through a portal burst whose chaos is a variable. A second beat swaps the letters into a replacement phrase with whole-word wrapping and auto type size, staggered with a tunable easing curve and settle glitch, with optional depth fog.

Composition id: `wireframe-portal-title`. Duration 8 s at 30 fps, 1920×1080.

## Files

- `wireframe-portal-title.html` (63 KB)
- `assets/fonts/Geist-Bold.ttf` (65 KB)
- `assets/fonts/Geist-Regular.ttf` (65 KB)
- `assets/fonts/Geist-SemiBold.ttf` (65 KB)
- `assets/fonts/Geist-OFL.txt` (4 KB)

## Install

Install with `npx hyperframes add wireframe-portal-title`; by default the files above land under `compositions/wireframe-portal-title/`. Then mount the block from the host `index.html`:

```html
<div
  data-composition-id="wireframe-portal-title"
  data-composition-src="compositions/wireframe-portal-title/wireframe-portal-title.html"
  data-start="0"
  data-duration="8"
  data-track-index="1"
  data-width="1920"
  data-height="1080"
></div>
```

Render with custom values by targeting the composition file directly:

```sh
npx --yes hyperframes@0.8.12 render 'compositions/wireframe-portal-title/wireframe-portal-title.html' --variables '{"title":"BREAKTHROUGH","replacementPhrase":"Lets do this sir!"}'
```

## Variables

Read at runtime via `window.__hyperframes.getVariables()`; declared on the composition root as `data-composition-variables` (single-quoted attribute, plain JSON).

| id                  | type    | default                      | label / range                                       |
| ------------------- | ------- | ---------------------------- | --------------------------------------------------- |
| `title`             | string  | `"BREAKTHROUGH"`             | Title max 18 chars                                  |
| `replacementPhrase` | string  | `"Lets do this sir!"`        | 3D replacement phrase (auto layout)                 |
| `phraseDuration`    | number  | `1.85`                       | Phrase transition duration (s) 0.65–2.9 step 0.05   |
| `phraseEasing`      | number  | `8`                          | Transition easing (1 gentle – 8 snap) 1–8 step 0.25 |
| `settleGlitch`      | number  | `0.2`                        | Letter settle glitch strength 0–4 step 0.05         |
| `depthFog`          | boolean | `true`                       | Depth fog (early fade always on)                    |
| `subtitle`          | string  | `"HYPERFRAMES PORTAL TITLE"` | Subtitle max 48 chars                               |
| `accent`            | color   | `"#F5C518"`                  | Accent                                              |
| `burstChaos`        | number  | `1`                          | Burst chaos (0-2) 0–2 step 0.01                     |

## Runtime contract

- One paused GSAP timeline registered as `window.__timelines["wireframe-portal-title"]`.
- Re-syncs on the `hf-seek` CustomEvent; every frame is a closed-form function of time (seeded PRNG only, no rAF loops, no Date.now).
- Renderer: three.js 0.181.2, GSAP 3.14.2, Canvas 2D, GLSL shaders, Post-processing, Seeded PRNG, Clipper. Budget roughly 350 MB per live instance; run one at a time.
- External runtime dependencies: `https://cdn.jsdelivr.net/npm/gsap@3.14.2/dist/gsap.min.js`, `https://cdn.jsdelivr.net/npm/clipper-lib@6.4.2/clipper.js`, `https://cdn.jsdelivr.net/npm/three@0.181.2/build/three.module.js`, `https://cdn.jsdelivr.net/npm/three@0.181.2/examples/jsm/`.
- Local fonts: assets/fonts/Geist-Regular.ttf, assets/fonts/Geist-SemiBold.ttf, assets/fonts/Geist-Bold.ttf.

## Editing rules (from the source project)

1. Keep `data-composition-variables` a single-quoted attribute with plain `"` JSON. Never save it through Studio's Design panel.
2. Do not put `<canvas>` in static markup; create it at runtime.
3. Keep every visual state a function of t; seek-safety is what makes the block renderable.


<!-- ===== FILE: registry-blocks/frost-sequence-camera-orbit/source/README.md ===== -->

# Source for assets/frost.js and assets/motion.js

This directory holds the TypeScript source and esbuild script that produce
the two bundled scripts the composition loads: `../assets/frost.js` (the
WebGPU/TSL ice rig, via `src/frost.ts`) and `../assets/motion.js` (the
lightweight WebGL editor helper, via `src/motion/editor.ts`).

## Build

```sh
npm install
npm run build
```

This regenerates `../assets/frost.js` and `../assets/motion.js`, plus a
`.LEGAL.txt` file next to each listing the bundled third-party notices
esbuild was able to extract automatically. `assets/Three-LICENSE.txt`,
`assets/ThreeMeshBVH-LICENSE.txt`, `assets/OpentypeJS-LICENSE.txt`, and
`assets/Clipper-LICENSE.txt` cover the same dependencies explicitly, since
automatic extraction doesn't catch every one of them.

`build.mjs` runs two checks before bundling: a source-only TypeScript pass
(`tools/compile-preflight.mjs`) and a headless shader-compile probe
(`tools/run-shard-compile.mjs`) that generates the WGSL for one shard
without a GPU, to catch a class of shader bug that only shows up at
compile time.

## Scope

This is the buildable subset: the TypeScript source, `build.mjs`, and the
two tool scripts it imports. The original project's test suite and a
standalone visual tuning UI (`workbench/`) are not included here.


<!-- ===== FILE: registry-blocks/frost-sequence-camera-orbit/source/src/vendor/clipper-README.md ===== -->

# ClipperLib

> forked from [Javascript Clipper](http://sourceforge.net/projects/jsclipper/)

## Description

The Javascript Clipper library performs clipping and offsetting for both lines and polygons. All four boolean clipping operations are supported - intersection, union, difference and exclusive-or. Polygons can be of any shape including self-intersecting polygons.

Javascript Clipper is a port of Angus Johnson's Clipper library: <https://sourceforge.net/projects/polyclipping/>

LIVE DEMO: <http://jsclipper.sourceforge.net/6.2.1.0/main_demo.html>

Information and examples:
<http://jsclipper.sourceforge.net/6.2.1.0/>

Donate Javascript Clipper Project: <https://sourceforge.net/p/jsclipper/wiki/Donations/>

Use cases:

- Over 1500 schools in the UK uses Javascript Clipper in Digimap for Schools service. Digimap for Schools is an online mapping service for use by teachers and pupils. Read more:
  <https://mobilegeo.wordpress.com/> and
  <http://digimapforschools.edina.ac.uk/cosmo-free/osmapper>

[Javascript Clipper Web Site](https://sourceforge.net/p/jsclipper/wiki/)

## Features

- Line and polygon clipping - intersection, union, difference & xor
- Line and polygon offsetting with 3 types of joining - miter, square and round
- Polygons can be of any shape, including self-intersecting polygons
- Minkowski Addition and Minkowski Difference functions included
- The library is written in Javascript
- Comprehensive documentation
- Demos use inline SVG and Canvas libraries
- The library is significantly faster than commercial alternatives
- Uses Tom Wu's fast big integer library
- UMD support

## Categories

Algorithms, Graphics

## Links

- [Documentation](./Documentation.md)
- [ChangeLog](./ChangeLog.txt)

## License

[Boost Software License (BSL1.0)](http://www.boost.org/LICENSE_1_0.txt)
