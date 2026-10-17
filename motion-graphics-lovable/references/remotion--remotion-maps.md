

<!-- ===== FILE: remotion/remotion-maps/REFERENCE.md ===== -->

---
name: remotion-maps
description: Remotion Map animation knowledge
version: 4.0.536
---

# Remotion Maps

Choose exactly one technique from the intended shot, then load only that technique's `TECHNIQUE.md`.
Every technique directory is self-contained and may be removed without breaking the others.

## [Static map](techniques/static-map/TECHNIQUE.md)

- Requires you grab a satellite image and mount it in a `<Img>` tag, and animate on top

## [Mapbox](techniques/mapbox/TECHNIQUE.md)

- Requires a Mapbox key
- Nicer styles by default
- Map can display a round globe when zoomed out
- Includes nice 3D buildings such as the Eiffel tower

## [MapLibre](techniques/maplibre/TECHNIQUE.md)

- Requires no API key, fully free
- Does not include 3D building

## [MapTiler](techniques/maptiler/TECHNIQUE.md)

- Uses MapTiler
- Annotations can be drawn on top of geographic features: borders, rivers, labels

## [CesiumJS](techniques/cesium/TECHNIQUE.md)

- Flythroughs through terrain and mountains
- "Flight simulator" perspective


<!-- ===== FILE: remotion/remotion-maps/techniques/cesium/TECHNIQUE.md ===== -->

# CesiumJS — 3D flyovers in Remotion

Instructions for achieving map animations with "flight-simulator" perspective in Remotion.

## Modes

| Mode        | Data                                                  | Use for                                                |
| ----------- | ----------------------------------------------------- | ------------------------------------------------------ |
| `landscape` | MapTiler `terrain-quantized-mesh-v2` + `satellite-v2` | Mountains, gorges, rivers, coastlines and rural routes |
| `city`      | Google Photorealistic 3D Tiles                        | Cities, architecture and recognizable landmarks        |

Do not use footprint extrusions for city flyovers. They produce crude building blocks rather than
textured architecture.

## Credentials

For `landscape`, set:

```text
REMOTION_MAPTILER_KEY=...
```

Create a MapTiler key at https://cloud.maptiler.com/account/keys/.

For `city`, set:

```text
REMOTION_GOOGLE_MAPS_API_KEY=...
```

Create a billing-enabled Google Map Tiles API key by following
https://developers.google.com/maps/documentation/tile/get-api-key. Enable the **Map Tiles API** and
restrict the key to that API. Ensure its application restriction permits local headless Remotion
requests.

## Build the flight

1. Copy `assets/CesiumFlythrough.tsx`, a path JSON and `assets/example-Root.tsx` into the Remotion
   project, or import the component directly.
2. Supply the camera route as `[longitude, latitude][]`. Use only meaningful control points; do not hand-author dozens of tiny corrections.
3. Leave `pathSmoothingPasses={3}` initially. The component applies repeated Chaikin corner cutting, turning straight-then-corner input into a continuous swerve. Increase to `4` for a softer route or reduce to `2` when the camera must follow a tight corridor.
4. Set absolute camera altitudes for the location. City cameras normally fly lower than landscape
   cameras.
5. Render a middle-frame still before rendering the full video.

```tsx
<CesiumFlythrough
  mode="city"
  path={cameraPath}
  pathSmoothingPasses={3}
  altitudeStart={700}
  altitudeEnd={500}
  lookAheadKm={0.7}
  travelKm={4.5}
/>
```

## Camera behavior

Walk the smoothed curve by arc length for constant ground speed. Aim at a real point farther along
the curve rather than its next vertex. Derive roll from the change in look-ahead bearing so the
camera banks into a turn instead of twitching left and right.

For landscape routes, `scripts/prep-cesium-path.mjs` also clips, resamples, smooths and dampens a
GeoJSON centerline before the component applies its final curve smoothing.


## Mechanics

- Set `viewer.useDefaultRenderLoop = false`.
- Call `viewer.render()`, never `scene.render()`, while settling.
- Use `preserveDrawingBuffer: true`.
- Gate initialization and every frame with `delayRender`.
- Drive camera animation from `useCurrentFrame()`; do not use CSS transitions or browser-timed animation.
- Settle landscapes on `globe.tilesLoaded` and cities on `tileset.tilesLoaded`.
- Keep all provider attribution visible.
- Record the source and effective date of custom or disputed geography.
- Inspect rendered pixels, not only Studio playback, at every required aspect ratio.
- Read `references/3d-flyover-architecture.md` for camera math, `references/3d-data-sources.md` for provider details, and `references/3d-troubleshooting.md` for blank, coarse, unauthorized or timed-out renders.

## Files

- `assets/CesiumFlythrough.tsx` — reusable two-mode component.
- `assets/flight-path.ts` — dependency-free Chaikin route smoothing.
- `assets/example-Root.tsx` — landscape and city compositions.
- `assets/cesium-path.json` — sample landscape route.
- `assets/city-path.json` — sample city route.
- `assets/sample-river.geojson` — sample path-preparation input.
- `scripts/prep-cesium-path.mjs` — dependency-free landscape route preparation.


<!-- ===== FILE: remotion/remotion-maps/techniques/cesium/references/3d-data-sources.md ===== -->

# Flyover data sources

## Landscape

Use MapTiler for both layers:

- `terrain-quantized-mesh-v2`: elevation encoded as Cesium quantized-mesh terrain.
- `satellite-v2`: raster satellite imagery draped on that mesh.

CesiumJS renders the layers; it does not supply the data. Set `REMOTION_MAPTILER_KEY`.

Create a key:

- https://cloud.maptiler.com/account/keys/

Official documentation:

- https://docs.maptiler.com/cesium/
- https://docs.maptiler.com/schema-raster/terrain-3d/

## City

Use Google Photorealistic 3D Tiles. Google supplies one high-resolution 3D mesh already textured
with imagery. Disable the Cesium globe and do not add MapTiler terrain or satellite beneath it. Set
`REMOTION_GOOGLE_MAPS_API_KEY`.

Create and configure a key:

- https://developers.google.com/maps/documentation/tile/get-api-key

Enable the Map Tiles API in a billing-enabled Google Cloud project and restrict the key to that API.
The application restriction must permit the local headless Remotion request.

Official documentation:

- https://developers.google.com/maps/documentation/tile/3d-tiles
- https://developers.google.com/maps/documentation/tile/policies

## Why not extruded buildings

OSM-, Overture- and vector-tile building products primarily provide footprints, approximate heights
and optional roof attributes. They are useful for analytical or stylized maps, but they do not
provide the textured architecture required for a cinematic city flyover.


<!-- ===== FILE: remotion/remotion-maps/techniques/cesium/references/3d-flyover-architecture.md ===== -->

# 3D Flyover — architecture reference

Deep detail behind `TECHNIQUE.md`: provider loading, the camera-path pipeline, per-frame camera math, and
the proven terrain values. Both landscape and city modes have been forward-tested through Remotion.

## 1. Provider initialization

Create the Viewer with `baseLayer: false`, UI widgets disabled, and
`contextOptions.webgl.preserveDrawingBuffer: true`. Never hide the credit display.

### Landscape

Add MapTiler `satellite-v2` with `UrlTemplateImageryProvider`, then load
`terrain-quantized-mesh-v2` with `CesiumTerrainProvider.fromUrl({requestVertexNormals: true})`.
MapTiler supplies both datasets; no Cesium ion token is required.

### City

Do not add MapTiler. Hide the globe, then add:

```ts
viewer.scene.globe.show = false;
const tileset = await Cesium.Cesium3DTileset.fromUrl(
  `https://tile.googleapis.com/v1/3dtiles/root.json?key=${GOOGLE_KEY}`,
  {showCreditsOnScreen: true, maximumScreenSpaceError: 4},
);
viewer.scene.primitives.add(tileset);
```

Lower `maximumScreenSpaceError` improves refinement at substantial download/render cost. Start at
`4` for a hero landmark and `6–8` for wider urban shots. Enforce the Google 30-second promotional
video ceiling in the component.

Load Cesium from the CDN after setting `window.CESIUM_BASE_URL`; the tested version is `1.143`.

## 2. The camera path — structure & generation

Four properties matter, in order:

1. **Continuous curvature** — the camera must flow through curves, never "fly straight, snap to a new
   heading, fly straight." The component applies three passes of **Chaikin corner cutting** to every
   supplied path. Each pass replaces a segment with quarter and three-quarter points, rounding a
   corner into a curve. Three passes are the default; four is softer, two is tighter.
2. **Constant ground speed** — precompute cumulative distance along the rounded curve and interpolate
   by arc length. Do not animate by source-point index; unequal source spacing creates speed bumps.
3. **Minimized amplitude** — for detailed landscape centerlines, dampen the prepared path toward its
   straight start→end chord by a fixed fraction `DAMP` (0 = dead straight, 1 = full river). This is
   the single swerve-amplitude knob.
4. **Enough length** — `PATHKM ≥ TRAVEL_KM + 2·LOOK_AHEAD_KM` so the look-ahead aim never clamps.

`../scripts/prep-cesium-path.mjs` does: clip a window of the source centerline → resample to even
arc-length spacing (0.1 km) → moving-average smooth (±2.8 km window, 2 passes) → dampen toward the chord
(`DAMP=0.45`). Validate with the heading-delta probe it prints — deltas should be small and change
_gradually_ (water-wars: `3,0,-1,-3,-4,1,7,9,5,-5,-12,-7,…`). Big jumps = corners = bad.

The component then applies Chaikin smoothing to this prepared route, or directly to a short
hand-authored city route. Keep city control points sparse and intentional; smoothing cannot rescue a
zig-zagging route that crosses the subject repeatedly.

**Source data:** OSM via Overpass (~0.3 km vertex spacing) — Natural Earth is too coarse for inner
gorges. overpass-api.de is often busy → mirror `overpass.kumi.systems`.

## 3. Camera animation per frame (position, heading, pitch, bank)

Walk the path by **arc length** (precompute cumulative distances once). Every frame:

- **Position** = the point at `dCam` km along the path, altitude `lerp(ALT_START, ALT_END, prog)`.
- **Heading** = bearing from the camera point to a **real point `LOOK_AHEAD_KM` further along the same
  path**. A far aim averages wiggle → smooth heading; on a curved path it leads into the bend, so the
  heading turns gently with the path. (A local-tangent aim spins the camera at every kink — don't.)
- **Pitch** = constant. We keep a MapLibre-style param `PITCH_FROM_NADIR` (90 = horizon), then convert:
  **Cesium pitch = `-(90 - PITCH_FROM_NADIR)`** (Cesium: 0 = horizon, -90 = straight down). 76° → -14°.
- **Bank (roll)** = lean _into_ the turn — the helicopter tell. Measure turn rate as the bearing change
  between `aim` and a point `2·LOOK_AHEAD_KM` ahead; `roll = clamp(dH · BANK_GAIN, ±MAX_BANK)`. Because
  the path is smooth, `dH` changes gradually → the bank eases in and out, never jerks.

```ts
const setCamera = (C, viewer, prog) => {
  const dCam = Math.min(TRAVEL_KM, PATHKM - LOOK_AHEAD_KM * 2) * prog;
  const cam  = alongPath(dCam);                    // arc-length point
  const aim  = alongPath(dCam + LOOK_AHEAD_KM);     // heading target (real point on the path)
  const aim2 = alongPath(dCam + LOOK_AHEAD_KM * 2); // turn-rate probe → bank
  const heading = bearing(cam, aim);
  let dH = bearing(aim, aim2) - heading; while (dH > Math.PI) dH -= 2*Math.PI; while (dH < -Math.PI) dH += 2*Math.PI;
  viewer.camera.setView({
    destination: C.Cartesian3.fromDegrees(cam[0], cam[1], lerp(ALT_START, ALT_END, prog)),
    orientation: { heading, pitch: C.Math.toRadians(-(90 - PITCH_FROM_NADIR)), roll: clamp(dH * BANK_GAIN, -MAX_BANK, MAX_BANK) },
  });
};
```

> **Cesium vs MapLibre conventions (gotcha):** Cesium heading is radians, 0 = north, clockwise. Pitch
> 0 = horizon, negative = down (MapLibre is the inverse). Roll positive = bank right; tune the sign by eye.

## 4. The feel — proven water-wars values

| Param                    | Value                  | Meaning                                                                              |
| ------------------------ | ---------------------- | ------------------------------------------------------------------------------------ |
| `TRAVEL_KM`              | 13                     | How far the camera travels. **Speed = `TRAVEL_KM / durationSeconds`.**               |
| duration                 | 24 s (720 f @30)       | 13 km / 24 s ≈ **0.54 km/s** — a slow, peaceful glide. 8 s felt "extremely rushed".  |
| `ALT_START → ALT_END`    | 4600 → 4300 m ASL      | Absolute (terrain-independent). Inside the corridor walls → fly _through_, not over. |
| `LOOK_AHEAD_KM`          | 1.5                    | Heading smoothness vs responsiveness.                                                |
| `PITCH_FROM_NADIR`       | 76°                    | Stare-ahead down the corridor (90 = level). → Cesium -14°.                           |
| `MAX_BANK` / `BANK_GAIN` | 0.13 rad (~7.5°) / 0.6 | Helicopter lean into turns.                                                          |
| `verticalExaggeration`   | 1.1                    | Subtle terrain drama.                                                                |
| `DAMP` (prep)            | 0.45                   | Swerve amount: higher = weavier, lower = straighter.                                 |

**A slow camera renders fast.** At 0.54 km/s the camera moves ~18 m/frame, so tiles stay cached and each
`settle()` returns almost immediately; the 720-frame render completed in one pass (no chunk-rendering).

## 5. The complete component

The full, runnable component is `../assets/CesiumFlythrough.tsx` — read it directly. Its shape:

- `loadCesium()` — inject `CESIUM_BASE_URL` + the CDN `Cesium.js`, resolve when loaded.
- init effect — build the Viewer (§1), `setCamera(…, 0)`, `await settle(viewer)`, `continueRender`.
- `settle(viewer)` — loop `viewer.render()` until `globe.tilesLoaded` for landscapes or
  `tileset.tilesLoaded` for cities is stable for ~8 ticks (cap ~600).
- per-frame effect — `delayRender({timeoutInMilliseconds: 60000})` → `setCamera(prog)` → `settle()` → `continueRender`.

## 6. Render

```bash
bunx remotion still   src/index.ts <Comp> out.png --frame=N --gl=angle --timeout=180000   # validate framing/bank first
bunx remotion render  src/index.ts <Comp> out.mp4  --gl=angle --concurrency=1 --timeout=180000
```

`--gl=angle` is mandatory. Use `--concurrency=1`; `settle()` already serializes tile loading.


<!-- ===== FILE: remotion/remotion-maps/techniques/cesium/references/3d-troubleshooting.md ===== -->

# 3D Flyover — troubleshooting

## The headless dead-end (why we render through Remotion)

Cesium's globe **will not draw in a standalone headless Playwright/Chromium** harness. Verified on
Apple M4 (ANGLE Metal active, WebGL working): the skybox/stars render, but the globe surface produces
**zero draw commands** (`scene.frameState.commandList.length === 0`), `globe.tilesLoaded` never goes
true, and frames come back as the black starfield. No network failures; `sampleTerrainMostDetailed`
succeeds (terrain data is reachable). Dead-ends tried, all failed:

- default render loop, manual `scene.render()`, manual `viewer.render()`, headed mode (context-destroyed).

**What works:** render Cesium **through Remotion** — same headless Chrome, but driven by Remotion's frame
loop with these four non-negotiables:

1. `useDefaultRenderLoop = false` — drive frames by hand.
2. Per frame call **`viewer.render()`**, NOT `scene.render()`. `viewer.render()` does the full frame
   (`initializeFrame` → tile streaming → render); `scene.render()` skips frame-init, so tiles never
   advance and the globe never appears. **This is the single most important line.**
3. `contextOptions: { webgl: { preserveDrawingBuffer: true } }` so Remotion's screenshot captures pixels.
4. Gate init + every frame with `delayRender(…, {timeoutInMilliseconds})` — tile loading can exceed Remotion's
   default; use 60–120 s.

The standalone `flythrough.html` / `render.mjs` / `probe.mjs` from the original spike are kept only as the
record of this dead-end. The canonical render path is the Remotion component
(`../assets/CesiumFlythrough.tsx`).

## Symptom → fix

| Symptom                                                   | Cause                                                                                                         | Fix                                                                                                 |
| --------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------- |
| Frames are black with stars                               | Globe not drawing (headless Playwright, or `scene.render()` used)                                             | Render through Remotion; use `viewer.render()`; `useDefaultRenderLoop=false`.                       |
| Screenshots blank/transparent                             | No `preserveDrawingBuffer`                                                                                    | `contextOptions:{ webgl:{ preserveDrawingBuffer:true } }`.                                          |
| "delayRender timed out"                                   | Cold tiles exceed the default                                                                                 | `delayRender(…, {timeoutInMilliseconds: 120000})` + `--timeout=180000`.                             |
| Globe is a dark/navy sphere                               | Imagery layer didn't attach                                                                                   | `baseLayer:false` then `viewer.imageryLayers.addImageryProvider(...)`.                              |
| High-pitch frame shows a void/starfield above the horizon | No atmosphere                                                                                                 | `viewer.scene.skyAtmosphere.show = true`.                                                           |
| 403 on tiles in headless                                  | Domain-locked MapTiler key                                                                                    | Use an **unrestricted** key.                                                                        |
| Google root tileset returns 403                           | Map Tiles API disabled, billing absent, wrong key, or application restriction blocks local headless rendering | Enable Map Tiles API and billing; restrict the key to that API while allowing the Remotion request. |
| Google scene shows a duplicate/competing surface          | MapTiler or the Cesium globe is still enabled                                                                 | Do not add MapTiler; set `viewer.scene.globe.show=false`.                                           |
| Google mesh remains coarse                                | Screen-space error is too high or the capture starts before refinement                                        | Lower `maximumScreenSpaceError`; settle on `tileset.tilesLoaded`.                                   |
| WebGL unavailable / software renderer                     | Missing GL flag                                                                                               | Render with `--gl=angle`.                                                                           |
| Camera looks at sky / ground, not terrain                 | Pitch sign / convention                                                                                       | Cesium pitch 0 = horizon, negative = down (inverse of MapLibre); `-(90 - PITCH_FROM_NADIR)`.        |
| Aim/turn-probe clamps near the end                        | Path too short                                                                                                | `PATHKM ≥ TRAVEL_KM + 2·LOOK_AHEAD_KM`; raise `WINDOW_KM` in prep.                                  |
| Path feels like straight-then-corner                      | Douglas-Peucker simplification                                                                                | Use resample → moving-average smooth (see architecture §2), not `turf.simplify`.                    |
| Camera bumps left and right instead of swerving           | Sparse route vertices are still being followed as straight segments                                           | Keep `pathSmoothingPasses={3}`; use sparse intentional control points and arc-length movement.      |

## Gotchas checklist

- **`viewer.render()`, never `scene.render()`** per frame. The single biggest trap.
- Cesium loads from **CDN**; set `window.CESIUM_BASE_URL` _before_ injecting the script.
- `preserveDrawingBuffer: true` or screenshots are blank.
- `delayRender` uses `timeoutInMilliseconds`; set it to at least 60,000.
- Terrain: `baseLayer:false`, then add MapTiler imagery.
- Google: no MapTiler, hide the globe, retain `showCreditsOnScreen:true`.
- Always `skyAtmosphere.show = true`.
- Validate the path's heading-delta probe and render one **still** (framing + bank) before the full mp4.
- Cesium pitch/roll conventions are inverted vs MapLibre.


<!-- ===== FILE: remotion/remotion-maps/techniques/mapbox/TECHNIQUE.md ===== -->

---
name: maps-mapbox
description: Make deterministic Remotion 2D map animations with Mapbox GL JS and Turf. Use when the user chooses Mapbox for animated routes, map markers, labels, camera movement, or Mapbox styles.
metadata:
  tags: map, map animation, mapbox, turf, geojson, route animation
---

Use Mapbox GL JS for rendering maps in Remotion when the user wants Mapbox styles or higher-fidelity map visuals and has a Mapbox access token. Use Turf for geospatial operations such as great-circle routes, distances, slicing lines, and positions along routes.

Use this technique only when the user has a Mapbox access token and wants Mapbox styles or data.

## Core rules

- Prefer `@turf/turf` for geospatial work. Do not hand-roll distance, great-circle, route slicing, or coordinate interpolation unless the user explicitly needs a custom non-geodesic effect.
- Use GeoJSON sources and Mapbox layers for lines, markers, and labels. Avoid DOM `Marker` elements unless the user specifically asks for HTML markers.
- Keep the live map camera static by default. Before moving it on every frame, read [moving-map stability](references/render-stability.md). Prefer a fixed map plate for satellite imagery, hillshade, or a modest 2D reframe.
- Use a live per-frame camera only after rendering a short MP4 and checking for shimmer. This 2D technique does not provide genuine terrain, pitch, bearing, or banking.
- Disable non-deterministic map behavior: `interactive: false`, `fadeDuration: 0`.
- Drive animation from `useCurrentFrame()`; do not use CSS transitions or browser-timed animation.
- Use `delayRender()` / `continueRender()` around map loading and per-frame map updates.
- Set `preserveDrawingBuffer: true` and render WebGL with `bunx remotion ... --gl=angle`.
- Before continuing the initial render, add sources/layers, apply the frame-0 camera with `jumpTo()` or `setFreeCameraOptions()`, then wait for `idle`.
- Do not add a `mapInstance.remove()` cleanup function; it can interfere with Remotion's render lifecycle.
- Use Mapbox style URLs such as `mapbox://styles/mapbox/standard` or a user-provided custom style.
- Do not install `@types/mapbox-gl`; Mapbox GL JS ships its own types.
- Keep required provider attribution visible and verify current provider terms before rendering.
- Record the source and effective date of custom or disputed geography.
- Inspect rendered pixels, not only Studio playback, at every required aspect ratio.

Coordinates in Mapbox, Turf, and GeoJSON are `[longitude, latitude]`.

```ts
const zurich: [number, number] = [8.5417, 47.3769];
const newYork: [number, number] = [-74.006, 40.7128];
```

## Prerequisites

Install Mapbox GL JS and Turf with the project's package manager.

```bash
npm i mapbox-gl @turf/turf
```

```bash
bun i mapbox-gl @turf/turf
```

```bash
yarn add mapbox-gl @turf/turf
```

```bash
pnpm i mapbox-gl @turf/turf
```

Import the Mapbox CSS once in the component or an app-level stylesheet:

```ts
import 'mapbox-gl/dist/mapbox-gl.css';
```

Mapbox requires a public access token. Prefer passing it as an input prop or reading it from an environment variable that is available to the bundled Remotion code.

```ts
const mapboxAccessToken = process.env.REMOTION_MAPBOX_TOKEN;

if (!mapboxAccessToken) {
	throw new Error('Set REMOTION_MAPBOX_TOKEN to render Mapbox maps.');
}
```

## Basic map example

```tsx
import {useEffect, useRef, useState} from 'react';
import {useDelayRender, useVideoConfig} from 'remotion';
import mapboxgl from 'mapbox-gl';
import 'mapbox-gl/dist/mapbox-gl.css';

const zurich: [number, number] = [8.5417, 47.3769];

const mapboxAccessToken = process.env.REMOTION_MAPBOX_TOKEN;

if (!mapboxAccessToken) {
	throw new Error('Set REMOTION_MAPBOX_TOKEN to render Mapbox maps.');
}

export const MyComposition = () => {
	const containerRef = useRef<HTMLDivElement>(null);
	const {delayRender, continueRender} = useDelayRender();
	const {width, height} = useVideoConfig();
	const [loadingHandle] = useState(() => delayRender('Loading Mapbox map'));

	useEffect(() => {
		if (!containerRef.current) {
			return;
		}

		const mapInstance = new mapboxgl.Map({
			accessToken: mapboxAccessToken,
			container: containerRef.current,
			style: 'mapbox://styles/mapbox/standard',
			center: zurich,
			zoom: 7,
			interactive: false,
			attributionControl: false,
			fadeDuration: 0,
			canvasContextAttributes: {
				preserveDrawingBuffer: true,
			},
		});

		mapInstance.on('load', () => {
			mapInstance.jumpTo({center: zurich, zoom: 7});
			mapInstance.once('idle', () => {
				continueRender(loadingHandle);
			});
		});
	}, [continueRender, loadingHandle]);

	return (
		<>
			<div ref={containerRef} style={{width, height, position: 'absolute'}} />
		</>
	);
};
```

Animated examples should keep the loaded map in React state and skip per-frame updates until that state is set.

## Animated flight route example

This example shows the recommended pattern for route animations:

- Turf creates the route and markers.
- Turf slices the route for line reveal animation.
- Mapbox renders the route with GeoJSON sources and layers.
- The camera uses `jumpTo()` with animated center, zoom, bearing, and pitch.
- Frame 0 is prepared before `continueRender()`.

```tsx
import * as turf from '@turf/turf';
import {useEffect, useRef, useState} from 'react';
import {
	AbsoluteFill,
	Easing,
	interpolate,
	useCurrentFrame,
	useDelayRender,
	useVideoConfig,
} from 'remotion';
import mapboxgl, {type GeoJSONSource, type Map} from 'mapbox-gl';
import 'mapbox-gl/dist/mapbox-gl.css';

const zurich: [number, number] = [8.5417, 47.3769];
const newYork: [number, number] = [-74.006, 40.7128];

const mapboxAccessToken = process.env.REMOTION_MAPBOX_TOKEN;

if (!mapboxAccessToken) {
	throw new Error('Set REMOTION_MAPBOX_TOKEN to render Mapbox maps.');
}

const greatCircleLine = (from: [number, number], to: [number, number]) => {
	const route = turf.greatCircle(from, to, {npoints: 100});

	if (route.geometry.type === 'LineString') {
		return turf.lineString(route.geometry.coordinates);
	}

	// Great-circle routes crossing the antimeridian can become MultiLineString.
	// Keep the example valid by choosing the longest segment.
	const longestSegment = route.geometry.coordinates.reduce((longest, segment) => {
		return segment.length > longest.length ? segment : longest;
	});

	return turf.lineString(longestSegment);
};

const targetRoute = greatCircleLine(zurich, newYork);
const targetRouteDistance = turf.length(targetRoute);

const cityMarkers = turf.featureCollection([
	turf.point(zurich, {name: 'Zurich'}),
	turf.point(newYork, {name: 'New York'}),
]);

const clampProgress = (progress: number) => Math.min(1, Math.max(0, progress));

const distanceAlong = (totalDistance: number, progress: number) => {
	// Keep the route non-empty at progress 0; Turf can error on zero-length slices.
	return Math.max(0.001, totalDistance * clampProgress(progress));
};

const getPartialTargetRoute = (progress: number) => {
	return turf.lineSliceAlong(
		targetRoute,
		0,
		distanceAlong(targetRouteDistance, progress),
	);
};

const getCameraOptions = (progress: number) => {
	const target = turf.along(
		targetRoute,
		distanceAlong(targetRouteDistance, progress),
	).geometry.coordinates as [number, number];

	return {
		center: target,
		zoom: interpolate(progress, [0, 0.5, 1], [7, 2.4, 8], {
			extrapolateLeft: 'clamp',
			extrapolateRight: 'clamp',
			easing: Easing.bezier(0.645, 0.045, 0.355, 1),
		}),
		bearing: interpolate(progress, [0, 1], [-20, 35], {
			extrapolateLeft: 'clamp',
			extrapolateRight: 'clamp',
		}),
		pitch: interpolate(progress, [0, 0.25, 0.75, 1], [25, 55, 55, 30], {
			extrapolateLeft: 'clamp',
			extrapolateRight: 'clamp',
			easing: Easing.bezier(0.645, 0.045, 0.355, 1),
		}),
	};
};

export const MyComposition = () => {
	const containerRef = useRef<HTMLDivElement>(null);
	const frame = useCurrentFrame();
	const {delayRender, continueRender} = useDelayRender();
	const {durationInFrames, height, width} = useVideoConfig();
	const [map, setMap] = useState<Map | null>(null);
	const [loadingHandle] = useState(() => delayRender('Loading Mapbox map'));

	useEffect(() => {
		if (!containerRef.current) {
			return;
		}

		const mapInstance = new mapboxgl.Map({
			accessToken: mapboxAccessToken,
			container: containerRef.current,
			style: 'mapbox://styles/mapbox/standard',
			center: zurich,
			zoom: 7,
			interactive: false,
			attributionControl: false,
			fadeDuration: 0,
			canvasContextAttributes: {
				preserveDrawingBuffer: true,
			},
		});

		mapInstance.on('load', () => {
			mapInstance.addSource('trace', {
				type: 'geojson',
				data: getPartialTargetRoute(0),
			});

			mapInstance.addLayer({
				id: 'trace-line',
				type: 'line',
				source: 'trace',
				layout: {
					'line-cap': 'round',
					'line-join': 'round',
				},
				paint: {
					'line-color': '#111111',
					'line-width': 7,
				},
			});

			mapInstance.addSource('city-markers', {
				type: 'geojson',
				data: cityMarkers,
			});

			mapInstance.addLayer({
				id: 'city-marker-dots',
				type: 'circle',
				source: 'city-markers',
				paint: {
					'circle-color': '#f03b20',
					'circle-radius': 12,
					'circle-stroke-color': '#ffffff',
					'circle-stroke-width': 4,
				},
			});

			mapInstance.addLayer({
				id: 'city-marker-labels',
				type: 'symbol',
				source: 'city-markers',
				layout: {
					'text-allow-overlap': true,
					'text-anchor': 'top',
					'text-field': ['get', 'name'],
					'text-offset': [0, 0.9],
					'text-size': 28,
				},
				paint: {
					'text-color': '#111111',
					'text-halo-color': '#ffffff',
					'text-halo-width': 3,
				},
			});

			mapInstance.jumpTo(getCameraOptions(0));
			mapInstance.once('idle', () => {
				setMap(mapInstance);
				continueRender(loadingHandle);
			});
		});
	}, [continueRender, loadingHandle]);

	useEffect(() => {
		if (!map) {
			return;
		}

		const handle = delayRender('Rendering Mapbox frame');
		const timelineProgress = interpolate(frame, [0, durationInFrames - 1], [0, 1], {
			extrapolateLeft: 'clamp',
			extrapolateRight: 'clamp',
		});
		const travelProgress = interpolate(timelineProgress, [0.2, 0.82], [0, 1], {
			extrapolateLeft: 'clamp',
			extrapolateRight: 'clamp',
			easing: Easing.bezier(0.645, 0.045, 0.355, 1),
		});
		const trace = map.getSource('trace') as GeoJSONSource | undefined;

		trace?.setData(getPartialTargetRoute(travelProgress));
		map.jumpTo(getCameraOptions(travelProgress));

		map.once('idle', () => continueRender(handle));
		// Force an idle event even if the camera parameters are unchanged from the previous frame.
		map.triggerRepaint();
	}, [continueRender, delayRender, durationInFrames, frame, map]);

	return (
		<AbsoluteFill style={{backgroundColor: '#e8eef3'}}>
			<div ref={containerRef} style={{height, position: 'absolute', width}} />
		</AbsoluteFill>
	);
};
```

## Camera guidance

For a validated live-camera route animation, animate `center`, `zoom`, `bearing`, and `pitch` with `jumpTo()`:

```ts
map.jumpTo({
	center,
	zoom,
	bearing,
	pitch,
});
```

Keep route progress and camera progress separate if the camera needs to lead, lag, zoom out, or zoom back in. For cinematic 3D camera moves, load the 3D flyover branch from the parent skill.

## Lines

Use GeoJSON sources for lines. Unless the user asks, do not add glow effects or extra decorative points.

For geodesic flight routes, use Turf:

```ts
const line = greatCircleLine(start, end);
const distance = turf.length(line);
const partialLine = turf.lineSliceAlong(
	line,
	0,
	// Keep the route non-empty at progress 0.
	Math.max(0.001, distance * progress),
);
```

For a visually straight line on the map, use a simple GeoJSON `LineString` between the two points instead of `greatCircle()`.

## Markers and labels

Use map-native GeoJSON layers for markers and labels:

```tsx
mapInstance.addSource('markers', {
	type: 'geojson',
	data: turf.featureCollection([
		turf.point([-118.2437, 34.0522], {name: 'Los Angeles'}),
	]),
});

mapInstance.addLayer({
	id: 'marker-dots',
	type: 'circle',
	source: 'markers',
	paint: {
		'circle-color': '#f03b20',
		'circle-radius': 12,
		'circle-stroke-color': '#ffffff',
		'circle-stroke-width': 4,
	},
});

mapInstance.addLayer({
	id: 'marker-labels',
	type: 'symbol',
	source: 'markers',
	layout: {
		'text-allow-overlap': true,
		'text-anchor': 'top',
		'text-field': ['get', 'name'],
		'text-offset': [0, 0.9],
		'text-size': 28,
	},
	paint: {
		'text-color': '#111111',
		'text-halo-color': '#ffffff',
		'text-halo-width': 3,
	},
});
```

Make marker sizes and label font sizes large enough for the composition resolution.

## Styles

Default to Mapbox Standard:

```ts
style: 'mapbox://styles/mapbox/standard'
```

If the user requests another style, use any valid Mapbox style URL.

## Rendering

For WebGL map renders, prefer single concurrency and ANGLE:

```bash
bunx remotion render [composition-id] out/video.mp4 --gl=angle --concurrency=1
```

Use the equivalent package runner for the project. In npm projects, use `npx`; in Bun projects, use `bunx`.


<!-- ===== FILE: remotion/remotion-maps/techniques/mapbox/references/render-stability.md ===== -->

# Moving Map Render Stability

Read this reference before building a moving 2D MapTiler scene or diagnosing a wavering Remotion render.

## Symptom and cause

If basemap detail shimmers or jitters during a pan/zoom, the likely cause is per-frame `map.jumpTo()`.
Headless MapTiler capture can resample both vector hillshade and satellite imagery differently frame to
frame. Tile retries, easing changes, and label changes do not solve that renderer effect.

## Required pattern: fixed map plate

For any 2D pan/zoom:

1. Render the MapTiler canvas once at the largest required zoom in an oversized container. Size it from the camera route and keep each dimension below the browser's reliable WebGL render-buffer limit (commonly 4096 px). Do **not** blindly use 3×: a 1920×1080 composition becomes 5760 px wide and Chromium may silently downsample it, causing visible pixelation during the CSS zoom.
2. Keep the map's camera static.
3. For each frame, calculate the approved target centre/zoom, then move the canvas with CSS `translate` + `scale`.
4. Apply the same transform to every projected HTML overlay.
5. Continue to animate GeoJSON data and paint properties imperatively; only the renderer camera is frozen.

Keep pitch and bearing constant. Use a 3D engine such as Cesium for genuine changing pitch/bearing or a terrain flythrough.

```ts
const baseZoom = Math.max(start.zoom, end.zoom);
const map = new maptilersdk.Map({
  container,
  style,
  center: end.center,
  zoom: baseZoom,
  pitch: end.pitch ?? 0,
  bearing: end.bearing ?? 0,
  interactive: false,
  fadeDuration: 0,
  canvasContextAttributes: {preserveDrawingBuffer: true},
});

// Per Remotion frame. `camera` is the approved centre/zoom interpolation.
const projected = map.project(camera.center);
const scale = 2 ** (camera.zoom - baseZoom);
const plate = {
  transform: `translate(${width / 2 - projected.x * scale}px, ${height / 2 - projected.y * scale}px) scale(${scale})`,
  transformOrigin: "0 0",
};

// Convert label projection with exactly the same plate transform.
const labelX = labelPoint.x * scale + width / 2 - projected.x * scale;
const labelY = labelPoint.y * scale + height / 2 - projected.y * scale;
```

### Plate sizing and sharpness

- Render at the maximum zoom reached by **any** camera waypoint, including intermediate or hold cameras. The CSS scale should never exceed `1`; otherwise the plate is being enlarged.
- Centre the frozen map on the midpoint of the camera route's geographic extent, not automatically on the final camera. This minimizes required overscan.
- Keep the largest canvas dimension at or below 4096 px unless the actual render environment has been tested with a larger `MAX_RENDERBUFFER_SIZE`.
- For 1920×1080, a 3840×2160 plate is a safe default. For 1080×1920, use approximately 2700×3840 when the route needs extra horizontal pan room.
- If the route cannot fit within that plate at the required zoom, split the shot into two fixed plates with a deliberate editorial transition. Do not trade sharpness for one enormous canvas.
- Distinguish failure modes: repeating shimmer means the live renderer is moving; steadily soft tiles during a CSS push means the fixed plate is underspecified, internally downsampled, or being scaled above `1`.

## Verification

- Render a short MP4, not only a Studio preview.
- Inspect static terrain texture and satellite detail while the camera moves.
- If any underlying map detail wavers, use the fixed map plate. Do not approve it as a minor preview artefact.
- Render WebGL with `--gl=angle`, `preserveDrawingBuffer:true`, and conservative concurrency (`1`) while validating.


<!-- ===== FILE: remotion/remotion-maps/techniques/maplibre/TECHNIQUE.md ===== -->

---
name: maps-maplibre
description: Make deterministic Remotion 2D map animations with MapLibre GL JS and Turf. Use when the user chooses MapLibre for animated routes, map markers, labels, and camera movement.
metadata:
  tags: map, map animation, maplibre, turf, geojson, route animation
---

Use MapLibre GL JS for rendering maps in Remotion. Use Turf for geospatial operations such as great-circle routes, distances, slicing lines, and positions along routes.

## Core rules

- Prefer `@turf/turf` for geospatial work. Do not hand-roll distance, great-circle, route slicing, or coordinate interpolation unless the user explicitly needs a custom non-geodesic effect.
- Use GeoJSON sources and MapLibre layers for lines, markers, and labels. Avoid DOM `Marker` elements unless the user specifically asks for HTML markers.
- Keep the live map camera static by default. Before moving it on every frame, read [moving-map stability](references/render-stability.md). Prefer a fixed map plate for satellite imagery, hillshade, or a modest 2D reframe.
- Use a live per-frame camera only after rendering a short MP4 and checking for shimmer. This 2D technique does not provide genuine terrain, pitch, bearing, or banking.
- Disable non-deterministic map behavior: `interactive: false`, `fadeDuration: 0`.
- Drive animation from `useCurrentFrame()`; do not use CSS transitions or browser-timed animation.
- Use `delayRender()` / `continueRender()` around map loading and per-frame map updates.
- Set `preserveDrawingBuffer: true` and render WebGL with `bunx remotion ... --gl=angle`.
- Before continuing the initial render, add sources/layers, apply the frame-0 camera with `jumpTo()`, then wait for `idle`.
- Do not add a `mapInstance.remove()` cleanup function; it can interfere with Remotion's render lifecycle.
- Use standard MapLibre style JSON URLs and layer/source APIs.
- Do not install `@types/maplibre-gl`; MapLibre ships its own types.
- Keep required provider attribution visible and verify the current terms of the chosen style and tile providers before rendering.
- Record the source and effective date of custom or disputed geography.
- Inspect rendered pixels, not only Studio playback, at every required aspect ratio.

Coordinates in MapLibre, Turf, and GeoJSON are `[longitude, latitude]`.

```ts
const zurich: [number, number] = [8.5417, 47.3769];
const newYork: [number, number] = [-74.006, 40.7128];
```

## Prerequisites

Install MapLibre and Turf with the project's package manager.

```bash
npm i maplibre-gl @turf/turf
```

```bash
bun i maplibre-gl @turf/turf
```

```bash
yarn add maplibre-gl @turf/turf
```

```bash
pnpm i maplibre-gl @turf/turf
```

Import the MapLibre CSS once in the component or an app-level stylesheet:

```ts
import 'maplibre-gl/dist/maplibre-gl.css';
```

## Basic map example

```tsx
import {useEffect, useRef, useState} from 'react';
import {useDelayRender, useVideoConfig} from 'remotion';
import * as maplibregl from 'maplibre-gl';
import 'maplibre-gl/dist/maplibre-gl.css';

const zurich: [number, number] = [8.5417, 47.3769];

export const MyComposition = () => {
	const containerRef = useRef<HTMLDivElement>(null);
	const {delayRender, continueRender} = useDelayRender();
	const {width, height} = useVideoConfig();
	const [loadingHandle] = useState(() => delayRender('Loading map'));

	useEffect(() => {
		if (!containerRef.current) {
			return;
		}

		maplibregl.setWorkerUrl(
			URL.createObjectURL(
				new Blob(
					[`import "https://unpkg.com/maplibre-gl@${maplibregl.getVersion()}/dist/maplibre-gl-worker.mjs";`],
					{type: 'text/javascript'},
				),
			),
		);

		const mapInstance = new maplibregl.Map({
			container: containerRef.current,
			style: 'https://demotiles.maplibre.org/style.json',
			center: zurich,
			zoom: 7,
			interactive: false,
			attributionControl: false,
			fadeDuration: 0,
			canvasContextAttributes: {
				preserveDrawingBuffer: true,
			},
		});

		mapInstance.on('load', () => {
			mapInstance.jumpTo({center: zurich, zoom: 7});
			mapInstance.once('idle', () => {
				continueRender(loadingHandle);
			});
		});
	}, [continueRender, loadingHandle]);

	return (
		<>
			<div ref={containerRef} style={{width, height, position: 'absolute'}} />
		</>
	);
};
```

Animated examples should keep the loaded map in React state and skip per-frame updates until that state is set.

## Animated flight route example

This example shows the recommended pattern for route animations:

- Turf creates the route and markers.
- Turf slices the route for line reveal animation.
- The camera has a separate route from the target route.
- MapLibre's `calculateCameraOptionsFromTo()` is used for camera movement.
- Frame 0 is prepared before `continueRender()`.

```tsx
import * as turf from '@turf/turf';
import {useEffect, useRef, useState} from 'react';
import {
	AbsoluteFill,
	Easing,
	interpolate,
	useCurrentFrame,
	useDelayRender,
	useVideoConfig,
} from 'remotion';
import * as maplibregl from 'maplibre-gl';
import {type GeoJSONSource, type Map} from 'maplibre-gl';
import 'maplibre-gl/dist/maplibre-gl.css';

const zurich: [number, number] = [8.5417, 47.3769];
const newYork: [number, number] = [-74.006, 40.7128];

const greatCircleLine = (from: [number, number], to: [number, number]) => {
	const route = turf.greatCircle(from, to, {npoints: 100});

	if (route.geometry.type === 'LineString') {
		return turf.lineString(route.geometry.coordinates);
	}

	// Great-circle routes crossing the antimeridian can become MultiLineString.
	// Keep the example valid by choosing the longest segment.
	const longestSegment = route.geometry.coordinates.reduce((longest, segment) => {
		return segment.length > longest.length ? segment : longest;
	});

	return turf.lineString(longestSegment);
};

const targetRoute = greatCircleLine(zurich, newYork);
const targetRouteDistance = turf.length(targetRoute);

const cameraRoute = greatCircleLine(zurich, newYork);
const cameraRouteDistance = turf.length(cameraRoute);

const cityMarkers = turf.featureCollection([
	turf.point(zurich, {name: 'Zurich'}),
	turf.point(newYork, {name: 'New York'}),
]);

const clampProgress = (progress: number) => Math.min(1, Math.max(0, progress));

const distanceAlong = (totalDistance: number, progress: number) => {
	// Keep the route non-empty at progress 0; Turf can error on zero-length slices.
	return Math.max(0.001, totalDistance * clampProgress(progress));
};

const getPartialTargetRoute = (progress: number) => {
	return turf.lineSliceAlong(
		targetRoute,
		0,
		distanceAlong(targetRouteDistance, progress),
	);
};

const getCameraOptions = (
	map: Map,
	progress: number,
	cameraAltitudeMeters: number,
	cameraLatitudeOffset: number,
) => {
	const target = turf.along(
		targetRoute,
		distanceAlong(targetRouteDistance, progress),
	).geometry.coordinates;
	const camera = turf.along(
		cameraRoute,
		distanceAlong(cameraRouteDistance, progress),
	).geometry.coordinates;

	return map.calculateCameraOptionsFromTo(
		new maplibregl.LngLat(camera[0], camera[1] - cameraLatitudeOffset),
		cameraAltitudeMeters,
		new maplibregl.LngLat(target[0], target[1]),
	);
};

export const MyComposition = () => {
	const containerRef = useRef<HTMLDivElement>(null);
	const frame = useCurrentFrame();
	const {delayRender, continueRender} = useDelayRender();
	const {durationInFrames, height, width} = useVideoConfig();
	const [map, setMap] = useState<Map | null>(null);
	const [loadingHandle] = useState(() => delayRender('Loading MapLibre map'));

	useEffect(() => {
		if (!containerRef.current) {
			return;
		}

		maplibregl.setWorkerUrl(
			URL.createObjectURL(
				new Blob(
					[`import "https://unpkg.com/maplibre-gl@${maplibregl.getVersion()}/dist/maplibre-gl-worker.mjs";`],
					{type: 'text/javascript'},
				),
			),
		);

		const mapInstance = new maplibregl.Map({
			container: containerRef.current,
			style: 'https://demotiles.maplibre.org/style.json',
			center: zurich,
			zoom: 7,
			interactive: false,
			attributionControl: false,
			fadeDuration: 0,
			canvasContextAttributes: {
				preserveDrawingBuffer: true,
			},
		});

		mapInstance.on('load', () => {
			mapInstance.addSource('trace', {
				type: 'geojson',
				data: getPartialTargetRoute(0),
			});

			mapInstance.addLayer({
				id: 'trace-line',
				type: 'line',
				source: 'trace',
				layout: {
					'line-cap': 'round',
					'line-join': 'round',
				},
				paint: {
					'line-color': '#111111',
					'line-width': 7,
				},
			});

			mapInstance.addSource('city-markers', {
				type: 'geojson',
				data: cityMarkers,
			});

			mapInstance.addLayer({
				id: 'city-marker-dots',
				type: 'circle',
				source: 'city-markers',
				paint: {
					'circle-color': '#f03b20',
					'circle-radius': 12,
					'circle-stroke-color': '#ffffff',
					'circle-stroke-width': 4,
				},
			});

			mapInstance.addLayer({
				id: 'city-marker-labels',
				type: 'symbol',
				source: 'city-markers',
				layout: {
					'text-allow-overlap': true,
					'text-anchor': 'top',
					'text-field': ['get', 'name'],
					'text-offset': [0, 0.9],
					'text-size': 28,
				},
				paint: {
					'text-color': '#111111',
					'text-halo-color': '#ffffff',
					'text-halo-width': 3,
				},
			});

			mapInstance.jumpTo(getCameraOptions(mapInstance, 0, 180000, 1.1));
			mapInstance.once('idle', () => {
				setMap(mapInstance);
				continueRender(loadingHandle);
			});
		});
	}, [continueRender, loadingHandle]);

	useEffect(() => {
		if (!map) {
			return;
		}

		const handle = delayRender('Rendering MapLibre frame');
		const timelineProgress = interpolate(frame, [0, durationInFrames - 1], [0, 1], {
			extrapolateLeft: 'clamp',
			extrapolateRight: 'clamp',
		});
		const travelProgress = interpolate(timelineProgress, [0.2, 0.82], [0, 1], {
			extrapolateLeft: 'clamp',
			extrapolateRight: 'clamp',
			easing: Easing.bezier(0.645, 0.045, 0.355, 1),
		});
		const cameraAltitudeMeters = interpolate(
			timelineProgress,
			[0, 0.28, 0.74, 1],
			[180000, 2200000, 2200000, 180000],
			{
				extrapolateLeft: 'clamp',
				extrapolateRight: 'clamp',
				easing: Easing.bezier(0.645, 0.045, 0.355, 1),
			},
		);
		const cameraLatitudeOffset = interpolate(
			timelineProgress,
			[0, 0.28, 0.74, 1],
			[1.1, 8, 8, 1.1],
			{
				extrapolateLeft: 'clamp',
				extrapolateRight: 'clamp',
				easing: Easing.bezier(0.645, 0.045, 0.355, 1),
			},
		);
		const trace = map.getSource('trace') as GeoJSONSource | undefined;

		trace?.setData(getPartialTargetRoute(travelProgress));
		map.jumpTo(
			getCameraOptions(
				map,
				travelProgress,
				cameraAltitudeMeters,
				cameraLatitudeOffset,
			),
		);

		map.once('idle', () => continueRender(handle));
		// Force an idle event even if the camera parameters are unchanged from the previous frame.
		map.triggerRepaint();
	}, [continueRender, delayRender, durationInFrames, frame, map]);

	return (
		<AbsoluteFill style={{backgroundColor: '#e8eef3'}}>
			<div ref={containerRef} style={{height, position: 'absolute', width}} />
		</AbsoluteFill>
	);
};
```

## Camera guidance

Use MapLibre's camera helper for camera movement:

```ts
map.calculateCameraOptionsFromTo(cameraLngLat, cameraAltitudeMeters, targetLngLat);
```

A good pattern is to keep two concepts separate:

- `targetRoute`: where the animated line is and where the camera looks.
- `cameraRoute`: where the camera moves.

Then use Turf to read positions from both routes for the same progress value:

```ts
const target = turf.along(targetRoute, targetDistance * progress).geometry.coordinates;
const camera = turf.along(cameraRoute, cameraDistance * progress).geometry.coordinates;

map.jumpTo(
	map.calculateCameraOptionsFromTo(
		new maplibregl.LngLat(camera[0], camera[1]),
		cameraAltitudeMeters,
		new maplibregl.LngLat(target[0], target[1]),
	),
);
```

For zoom-out / travel / zoom-in animations, animate travel progress separately from camera altitude. Camera altitude is measured in meters. This avoids heavy custom camera math.

## Lines

Use GeoJSON sources for lines. Unless the user asks, do not add glow effects or extra decorative points.

For geodesic flight routes, use Turf:

```ts
const line = greatCircleLine(start, end);
const distance = turf.length(line);
const partialLine = turf.lineSliceAlong(
	line,
	0,
	// Keep the route non-empty at progress 0.
	Math.max(0.001, distance * progress),
);
```

For a visually straight line on the map, use a simple GeoJSON `LineString` between the two points instead of `greatCircle()`.

## Markers and labels

Use map-native GeoJSON layers for markers and labels:

```tsx
mapInstance.addSource('markers', {
	type: 'geojson',
	data: turf.featureCollection([
		turf.point([-118.2437, 34.0522], {name: 'Los Angeles'}),
	]),
});

mapInstance.addLayer({
	id: 'marker-dots',
	type: 'circle',
	source: 'markers',
	paint: {
		'circle-color': '#f03b20',
		'circle-radius': 12,
		'circle-stroke-color': '#ffffff',
		'circle-stroke-width': 4,
	},
});

mapInstance.addLayer({
	id: 'marker-labels',
	type: 'symbol',
	source: 'markers',
	layout: {
		'text-allow-overlap': true,
		'text-anchor': 'top',
		'text-field': ['get', 'name'],
		'text-offset': [0, 0.9],
		'text-size': 28,
	},
	paint: {
		'text-color': '#111111',
		'text-halo-color': '#ffffff',
		'text-halo-width': 3,
	},
});
```

Make marker sizes and label font sizes large enough for the composition resolution.

## Styles

Default to the stock MapLibre demo style:

```ts
style: 'https://demotiles.maplibre.org/style.json'
```

If the user requests another style, use any valid MapLibre style JSON URL.

## Rendering

For WebGL map renders, prefer single concurrency and ANGLE:

```bash
bunx remotion render [composition-id] out/video.mp4 --gl=angle --concurrency=1
```

Use the equivalent package runner for the project. In npm projects, use `npx`; in Bun projects, use `bunx`.


<!-- ===== FILE: remotion/remotion-maps/techniques/maplibre/references/render-stability.md ===== -->

# Moving Map Render Stability

Read this reference before building a moving 2D MapTiler scene or diagnosing a wavering Remotion render.

## Symptom and cause

If basemap detail shimmers or jitters during a pan/zoom, the likely cause is per-frame `map.jumpTo()`.
Headless MapTiler capture can resample both vector hillshade and satellite imagery differently frame to
frame. Tile retries, easing changes, and label changes do not solve that renderer effect.

## Required pattern: fixed map plate

For any 2D pan/zoom:

1. Render the MapTiler canvas once at the largest required zoom in an oversized container. Size it from the camera route and keep each dimension below the browser's reliable WebGL render-buffer limit (commonly 4096 px). Do **not** blindly use 3×: a 1920×1080 composition becomes 5760 px wide and Chromium may silently downsample it, causing visible pixelation during the CSS zoom.
2. Keep the map's camera static.
3. For each frame, calculate the approved target centre/zoom, then move the canvas with CSS `translate` + `scale`.
4. Apply the same transform to every projected HTML overlay.
5. Continue to animate GeoJSON data and paint properties imperatively; only the renderer camera is frozen.

Keep pitch and bearing constant. Use a 3D engine such as Cesium for genuine changing pitch/bearing or a terrain flythrough.

```ts
const baseZoom = Math.max(start.zoom, end.zoom);
const map = new maptilersdk.Map({
  container,
  style,
  center: end.center,
  zoom: baseZoom,
  pitch: end.pitch ?? 0,
  bearing: end.bearing ?? 0,
  interactive: false,
  fadeDuration: 0,
  canvasContextAttributes: {preserveDrawingBuffer: true},
});

// Per Remotion frame. `camera` is the approved centre/zoom interpolation.
const projected = map.project(camera.center);
const scale = 2 ** (camera.zoom - baseZoom);
const plate = {
  transform: `translate(${width / 2 - projected.x * scale}px, ${height / 2 - projected.y * scale}px) scale(${scale})`,
  transformOrigin: "0 0",
};

// Convert label projection with exactly the same plate transform.
const labelX = labelPoint.x * scale + width / 2 - projected.x * scale;
const labelY = labelPoint.y * scale + height / 2 - projected.y * scale;
```

### Plate sizing and sharpness

- Render at the maximum zoom reached by **any** camera waypoint, including intermediate or hold cameras. The CSS scale should never exceed `1`; otherwise the plate is being enlarged.
- Centre the frozen map on the midpoint of the camera route's geographic extent, not automatically on the final camera. This minimizes required overscan.
- Keep the largest canvas dimension at or below 4096 px unless the actual render environment has been tested with a larger `MAX_RENDERBUFFER_SIZE`.
- For 1920×1080, a 3840×2160 plate is a safe default. For 1080×1920, use approximately 2700×3840 when the route needs extra horizontal pan room.
- If the route cannot fit within that plate at the required zoom, split the shot into two fixed plates with a deliberate editorial transition. Do not trade sharpness for one enormous canvas.
- Distinguish failure modes: repeating shimmer means the live renderer is moving; steadily soft tiles during a CSS push means the fixed plate is underspecified, internally downsampled, or being scaled above `1`.

## Verification

- Render a short MP4, not only a Studio preview.
- Inspect static terrain texture and satellite detail while the camera moves.
- If any underlying map detail wavers, use the fixed map plate. Do not approve it as a minor preview artefact.
- Render WebGL with `--gl=angle`, `preserveDrawingBuffer:true`, and conservative concurrency (`1`) while validating.


<!-- ===== FILE: remotion/remotion-maps/techniques/maptiler/TECHNIQUE.md ===== -->

# MapTiler maps in Remotion

MapTiler is a good solution for map animations where geographics features should be drawn as annotations on top of the map: Country borders, rivers, labels for POIs.

## MapTiler SDK (`@maptiler/sdk`)

Draw the basemap plus MapTiler Planet vector layers and custom GeoJSON into a WebGL canvas. Default styled-vector starting point: `MapStyle.BASIC`; satellite is an equally valid choice.

## Remotion

Imperatively update `setData`/`setPaintProperty`.

Use `jumpTo` only for a static shot, or a fixed map plate for any pan/zoom.
Gate with [`delayRender`](https://www.remotion.dev/docs/delay-render.md) until `map.once('idle')`.

Use `preserveDrawingBuffer:true`.

Render labels as positioned [`<Interactive.Div>`](https://www.remotion.dev/docs/interactive.md) elements.

Env `REMOTION_MAPTILER_KEY` (unrestricted). Init the map once (ref guard); update imperatively per frame.

When constructing MapLibre/MapTiler layer objects, omit optional properties that are absent.  
In particular, use `...(layer.filter ? {filter: layer.filter} : {})`; do not pass `filter: undefined`. An undefined filter can suppress the layer while separately created halo or border layers continue rendering, producing missing country fills and dark marker halos with no coloured cores.

Drive animation from `useCurrentFrame()` rather than CSS transitions or browser timers.  

## Choose the source for each map element

Do not begin by manufacturing GeoJSON. First check whether MapTiler Planet already exposes the element as filtered vector data.

### MapTiler vector

Use it when the feature exists in a provider `source-layer`, its attributes support an exact filter, and provider geometry is editorially acceptable.

### Hybrid

Use it when ordinary geographic context can come from MapTiler while the claim depends on custom
evidence.

Animate each layer according to its source and meaning.

MapTiler vector features remain split across tiles. Do not use them for a semantic start-to-end line draw; extract, verify, order, and bake that element to GeoJSON first. Read **`references/map-data-sources.md`** and reuse **`assets/MapTilerVectorElement.ts`** for provider-layer setup and per-frame paint updates.

## Motion stability

**Do not call `map.jumpTo()` on every Remotion frame when the camera moves.** In headless capture it can make both MapTiler hillshade **and satellite imagery** shimmer/jitter, even when the source tiles load correctly. This is renderer resampling, not a data, network, or label problem.

For the implementation, read **`references/render-stability.md`** before building or debugging any moving map. It contains the fixed-map-plate recipe, diagnostics, and render checks.

- Use the live MapTiler camera only for a static shot.
- Keep pitch and bearing constant for a fixed plate. This technique does not implement a genuine changing 3D camera.
- Verify the moving preview and a short rendered MP4 before approving a beat. If any basemap detail wavers, switch to the fixed-plate pattern; do not try to solve it with tile retries or camera easing.

## Drawing rivers

Use `turf.lineSliceAlong(line, 0, lineKm*reveal)` to draw rivers.

## Source selection

Use MapTiler vector layers for suitable provider features and custom GeoJSON for story-specific or ordered geometry. If the beat needs country-entry triggers or a progressive line draw, run `scripts/prep-geo.mjs` to bake `country-meta.json`, `borders.geojson`, and the ordered line. Details → `references/map-data-sources.md` and `references/map-geo-prep.md`.

## Keep it minmal

Strip clutter on `load`: remove `symbol` layers (place labels) and `/other border/i` (admin-1 inner borders); hide the logo via CSS. Keep country + disputed borders.

## Files

Use as reference:

- `assets/RiverReveal.tsx` — the main component.
- `assets/MapTilerVectorElement.ts` — filtered MapTiler Planet elements.
- `assets/CountryLabel.tsx` — reusable example label.
- `assets/tokens.ts` — example palette and durations.
- `assets/example-Root.tsx` — minimal composition scaffold.
- `assets/sample-data/` — example route and generated country metadata.
- `scripts/prep-geo.mjs` — geo pipeline.
- `references/map-explainer-architecture.md` — timing model and implementation.
- `references/map-data-sources.md` — provider vector versus custom GeoJSON selection.
- `references/map-geo-prep.md` — basemap stripping and geo preparation.
- `references/render-stability.md` — camera motion and stable headless renders.


<!-- ===== FILE: remotion/remotion-maps/techniques/maptiler/references/map-data-sources.md ===== -->

# Map element data sources

Choose the source independently for every story element. A single map can—and often should—mix
provider vectors with custom geodata.

## Decision rule

Use a MapTiler Planet vector layer when the feature already exists there, its attributes support an
editorially precise filter, and provider geometry is acceptable for the claim. Use custom GeoJSON when
the feature is absent, proposed, historical, disputed, corrected, privately sourced, or needs ordered
geometry for a deterministic draw.

| Requirement                                                                 | MapTiler vector layer | Custom GeoJSON                              |
| --------------------------------------------------------------------------- | --------------------- | ------------------------------------------- |
| Roads, waterways, water, boundaries, land cover, or other standard context  | Prefer                | Use only when provider data is insufficient |
| Basemap-consistent geometry without a duplicate local dataset               | Prefer                | No                                          |
| Proposed, historical, classified, corrected, or production-specific element | No                    | Prefer                                      |
| Fade, colour, width, radius, blur, or fill-opacity animation                | Yes                   | Yes                                         |
| Feature-state highlight when a stable feature ID exists                     | Yes                   | Yes                                         |
| Deterministic source-to-end line draw or perimeter draw                     | Bake first            | Prefer                                      |
| Geometry editing, morphing, clipping, or exact sequencing                   | No                    | Prefer                                      |

Provider alignment is not proof of correctness. Inspect the attributes and geometry against the
editorial source before presenting a provider feature as evidence.

## MapTiler vector mode

MapTiler Planet is a vector tile source. Add it once, then build story layers with a
`source-layer` and an exact attribute filter. Read the current MapTiler Planet schema before choosing
layer names or fields.

Common layer categories include `waterway`, `water`, `transportation`, `boundary`, `landcover`, and
`poi`; availability, fields, and zoom ranges vary by schema version.

```ts
import {addMapTilerVectorElement, setVectorElementPaint} from "./MapTilerVectorElement";

addMapTilerVectorElement(map, process.env.REMOTION_MAPTILER_KEY!, {
  id: "story-river",
  sourceLayer: "waterway",
  type: "line",
  filter: [
    "all",
    ["==", ["get", "class"], "river"],
    ["==", ["coalesce", ["get", "name_en"], ["get", "name"]], "Yarlung Tsangpo"],
  ],
  layout: {"line-cap": "round", "line-join": "round"},
  paint: {
    "line-color": "#E8F7FF",
    "line-width": 3,
    "line-opacity": 0,
  },
});

setVectorElementPaint(map, "story-river", {
  "line-opacity": reveal,
  "line-width": 2 + reveal * 2,
});
```

Animate provider features by changing paint properties from the Remotion frame: opacity, colour,
width, blur, fill opacity, circle radius, or symbol opacity. Use feature state only when the source
provides stable IDs and the selection remains deterministic across tiles.

Do not treat a tiled line as one ordered path. Vector tiles split features at tile boundaries, so a
source-to-mouth or start-to-end draw has no reliable global order. If that motion carries meaning,
extract and verify the complete feature, order it once, save it as GeoJSON, and use the custom mode.

## Custom geodata mode

Use the bundled `../assets/RiverReveal.tsx` and `../scripts/prep-geo.mjs` pattern for custom GeoJSON. This mode owns
the exact geometry and can slice it by distance, calculate entry triggers, draw complete borders, and
produce deterministic sequences.

Custom mode is mandatory when:

- the feature is not in the provider dataset;
- the story uses a proposed route, planned tunnel, historical boundary, disputed interpretation, or
  non-public dataset;
- provider geometry was editorially corrected;
- motion must travel through the geometry in a verified order;
- a complete off-screen boundary matters and a viewport query would silently crop it.

## Hybrid mode

Use provider vectors for ordinary contextual features and custom GeoJSON for the specific claim. For
example: MapTiler waterways and roads as aligned context; a custom proposed tunnel, dam site, disputed
boundary, or verified evacuation area as the highlighted evidence.

Keep provider and custom layers visually distinct when they carry different evidentiary weight. Record
the source and effective date of every custom layer in the production notes.


<!-- ===== FILE: remotion/remotion-maps/techniques/maptiler/references/map-explainer-architecture.md ===== -->

# Map Explainer — architecture reference

Deep detail behind `TECHNIQUE.md`: the timing model, the river reveal + electric head, the per-country
sequence, and label projection. The supplied values are examples, not a production style system.
The custom-geometry example is `../assets/RiverReveal.tsx` +
`../assets/CountryLabel.tsx` +
`../assets/tokens.ts`. Provider-vector setup is in
`../assets/MapTilerVectorElement.ts`; choose between
the two modes with `data-sources.md`.

## 1. The render harness (per frame)

Init the MapTiler map once (ref guard). On `load`: strip clutter (see `geo-prep.md`), add sources/layers,
wait for `once('idle') → continueRender`. Per frame:

```
delayRender → setData/setPaintProperty → map.once('idle', continueRender) → triggerRepaint
```

`preserveDrawingBuffer:true` so Remotion's screenshot captures the canvas. Render `--gl=angle`.
For an animated camera, read `render-stability.md`: the MapTiler renderer remains static and a CSS plate
transform supplies the camera choreography.

## 2. Timing model — time-based; beat length derived from the sequences

Everything keys off **seconds** (`t = frame / fps`), not reveal-units. The river draws over a window;
each country **triggers when the river reaches it** and runs a fixed sequence. The beat is exactly as
long as the sequences need.

```ts
const RIVER_START = 0.3, RIVER_END = 8.0;            // river draws over this window
const BORDER_S = 2.5, FILL_S = 1.0, LABEL_S = 0.7;   // per-country sequence (constant durations)
const trigger = (c) => RIVER_START + META[c].stop * (RIVER_END - RIVER_START);  // river-arrival time
// beat length = max over c of (trigger(c) + BORDER_S + FILL_S + LABEL_S) + tail
const reveal = interpolate(t, [RIVER_START, RIVER_END], [0,1], { ...clamp, easing: Easing.bezier(0.645, 0.045, 0.355, 1) });
```

**Constant durations matter:** drive the border draw by _time since trigger_, not a slice of the reveal —
otherwise complex or long borders flash by in a fraction of a second.

## 3. Provider-vector animation

MapTiler Planet elements can be animated directly in place. Filter an exact `source-layer` feature,
initialize its paint in the hidden or neutral state, then update paint properties from the Remotion frame.
This works for line, fill, circle, and symbol layers without copying provider geometry into the project.

Do not assume tiled geometry has a global order. Provider features are split at tile boundaries: opacity,
colour, width, blur, radius, fill, and feature-state changes are reliable; semantic start-to-end line
draws are not. Bake ordered GeoJSON when the direction of the draw carries meaning.

## 4. Custom line animation — reveal + electric draw-head

The "electricity" is a **white-hot head** leading the draw — the last few % of the drawn line in its own
bright + glow layers, faded out once the river completes.

```ts
const riverDrawnKm = lineKm * reveal;
map.getSource("river").setData(turf.lineSliceAlong(line, 0, Math.max(0.001, riverDrawnKm)));
const headKm = lineKm * 0.03;
map.getSource("river-head").setData(turf.lineSliceAlong(line, Math.max(0, riverDrawnKm - headKm), Math.max(0.001, riverDrawnKm)));
let headFade = 0;
if (reveal > 0.002 && reveal < 0.999) headFade = 1;
else if (reveal >= 0.999) headFade = 1 - clamp01((t - RIVER_END) / 0.5);  // fade out at the mouth
map.setPaintProperty("river-headglow", "line-opacity", 0.85 * headFade);
map.setPaintProperty("river-head", "line-opacity", headFade);
```

Layers, bottom→top: `river-glow` (electric blue `#49C6FF`, w11, op0.32, blur6) → `river-line`
(icy core `#E8F7FF`, w3) → `river-headglow` (`rgba(120,225,255,.95)`, w16, blur9) → `river-head`
(white `#FFFFFF`, w4.5). **No dark casing** — the bright icy core reads over every fill on its own.

## 5. Country animation — border draws → fill blooms → label rises

Triggered by river arrival, each country runs three sequential phases. The border is a **darker shade**
of the country colour (the electricity is on the river, not here).

```ts
const lt = t - trigger(c);                                   // local seconds since trigger
// 1) complete source border draws on over a constant BORDER_S, multi-segment-safe
const bp = interpolate(clamp01(lt / BORDER_S), [0,1], [0,1], { easing: Easing.bezier(0.645, 0.045, 0.355, 1) });
map.getSource(`trail-${c}`).setData(sliceBorder(DRAW[c], 0, DRAW[c].total * bp));   // COUNTRY_DARK line
// 2) fill blooms in (opacity overshoots, then settles) after the border completes
const fp = clamp01((lt - BORDER_S) / FILL_S);
const fo = interpolate(fp, [0, 0.6, 1], [0, FILL_OPACITY * 1.25, FILL_OPACITY], { ...clamp, easing: Easing.bezier(0.3333333333333333, 1, 0.6666666666666666, 1) });
map.setPaintProperty(`fill-${c}`, "fill-opacity", fp <= 0 ? 0 : fo);
// 3) label rises in after the fill
const lp = clamp01((lt - BORDER_S - FILL_S) / LABEL_S);
```

`sliceBorder(d, fromKm, toKm)` reveals a portion of a complete (possibly multi-segment) border as a
MultiLineString, slicing each segment by cumulative length — no joins across gaps and no viewport crop:

```ts
const sliceBorder = (d, fromKm, toKm) => {
  const out = [];
  for (let i = 0; i < d.segLines.length; i++) {
    const start = d.cum[i], end = start + d.segLen[i];
    const a = Math.max(fromKm, start), b = Math.min(toKm, end);
    if (b - a <= 0.0008) continue;
    out.push(turf.lineSliceAlong(d.segLines[i], a - start, b - start).geometry.coordinates);
  }
  return { type:"Feature", properties:{}, geometry:{ type:"MultiLineString", coordinates: out } };
};
```

Choose fill, border, and river colours in the production's local token file. The bundled token values are
examples only; do not carry a source project's palette into another production.

## 6. Labels — HTML overlay, projected each frame

Labels are React, not map symbols (full typography control). `CountryLabel` is an example accent-rule,
rise-and-fade treatment; select the typeface and final values in the production.
Positioned by projecting the anchor to screen pixels **every frame**, stored in state:

```ts
const p = map.project(META[c].anchor);   // lngLat → screen px (respects the live camera)
pos[c] = { x: p.x, y: p.y, reveal: lp };
setLabels(pos);                          // re-render the overlay; effect deps exclude `labels`
```

`CountryLabel` shows the mechanics: uppercase region name, short accent divider, rise/fade entrance,
and `pointerEvents:none`. Select font, weight, size, spacing, contrast, and colour from the production's
own type and palette system.

## 7. Camera — fixed map plate for any movement

Read `render-stability.md`. Do not use per-frame `map.jumpTo()` for a moving 2D shot; it can shimmer in
headless renders even on satellite imagery. Interpolate the intended camera for the CSS plate transform,
while keeping the MapTiler renderer static.


<!-- ===== FILE: remotion/remotion-maps/techniques/maptiler/references/map-geo-prep.md ===== -->

# Map Explainer — basemap & geo prep

How the basemap is cleaned and how `../scripts/prep-geo.mjs` bakes the per-country data the component reads.

## Basemap styling — strip the clutter

On `load`, remove the basemap's labels and inner admin borders so only your geography reads:

```ts
for (const l of m.getStyle().layers as any[])
  if (l.type === "symbol" || /other border/i.test(l.id)) m.removeLayer(l.id);
```

- `type === "symbol"` → every place/water/road **label** (the "MapTiler labels"). Gone.
- Inner admin-border layer IDs vary by style. Inspect the loaded style, remove state/province/district
  layers as needed, and retain only the context borders the production requires.
- Logo/attribution: `maptilerLogo:false` + `attributionControl:false` aren't always enough — also hide
  via CSS in the component:
  ```tsx
  <style>
    {`
      .maplibregl-ctrl-bottom-left,
      .maplibregl-ctrl-bottom-right,
      .maplibregl-ctrl-attrib,
      .maptiler-logo {
        display: none !important;
      }
    `}
  </style>
  ```

## `../scripts/prep-geo.mjs` → outputs

Reads a routed river GeoJSON + country polygon GeoJSONs; writes:

- **River line** — simplified for a smooth draw. For a braided river, route one source→mouth path through
  the network first: greedy endpoint-chaining bounces between parallel channels. → `src/geo/river-flow.json`.
- **`public/geo/borders.geojson`** — each country's polygon tagged `{country: name}` (one source,
  filtered per country for the fills).
- **`src/geo/country-meta.json`** — per country `{ stop, anchor, border }`.

### `stop` — when a country lights up

Walk the river points; first point inside a country (`turf.booleanPointInPolygon`) = the arc-length
fraction where the river **enters** it. Drives the trigger time. The headwaters country = 0.

### `anchor` — label centre via pole of inaccessibility

The most-interior point of the country (clipped to a per-country **story bbox** so a big country
centres in the relevant region, not its far bulge), then a small operator **nudge**. Pole = grid-sample
inside the polygon, keep the point with max distance to the boundary. **Centroids get pulled to edges —
don't use them.**

```js
const pole = (poly) => {
  const bb = turf.bbox(poly), edge = turf.polygonToLine(poly), N = 46;
  let best = null, bestD = -1;
  for (let i = 0; i <= N; i++) for (let j = 0; j <= N; j++) {
    const p = turf.point([bb[0]+(bb[2]-bb[0])*i/N, bb[1]+(bb[3]-bb[1])*j/N]);
    if (!turf.booleanPointInPolygon(p, poly)) continue;
    const d = turf.pointToLineDistance(p, edge);
    if (d > bestD) { bestD = d; best = p.geometry.coordinates; }
  }
  return best;
};
const ANCHOR_BBOX = { china:[82,27,96,32], india:[76,14,99,31], bangladesh:[86,20,93,27] };  // story regions
const NUDGE = { china:[0,0.6], india:[-1.0,0], bangladesh:[0,-0.6] };                          // operator-directed
```

### `border` — complete source geometry

Preserve every exterior ring from the named country source. Never clip a country or bilateral border to
the framed bbox and never discard an off-screen segment: the geometry may leave the frame naturally.
The renderer handles a MultiLineString by cumulative length, so it remains one timed reveal without
inventing joins across gaps.

## Tuning the geo prep for a new scenario

| Want                              | Knob                                                                 |
| --------------------------------- | -------------------------------------------------------------------- |
| Which countries                   | the country list in `prep-geo.mjs` (+ supply their polygon GeoJSONs) |
| Label centred in the right region | `ANCHOR_BBOX[country]` (the story bbox)                              |
| Nudge a label                     | `NUDGE[country]` (lng, lat offset)                                   |
| What border is drawn              | the complete named source geometry; never the visible extent         |
| When each lights up               | derived from `stop` — depends on the river geometry                  |


<!-- ===== FILE: remotion/remotion-maps/techniques/maptiler/references/render-stability.md ===== -->

# Moving Map Render Stability

Read this reference before building a moving 2D MapTiler scene or diagnosing a wavering Remotion render.

## Symptom and cause

If basemap detail shimmers or jitters during a pan/zoom, the likely cause is per-frame `map.jumpTo()`.
Headless MapTiler capture can resample both vector hillshade and satellite imagery differently frame to
frame. Tile retries, easing changes, and label changes do not solve that renderer effect.

## Required pattern: fixed map plate

For any 2D pan/zoom:

1. Render the MapTiler canvas once at the largest required zoom in an oversized container. Size it from the camera route and keep each dimension below the browser's reliable WebGL render-buffer limit (commonly 4096 px). Do **not** blindly use 3×: a 1920×1080 composition becomes 5760 px wide and Chromium may silently downsample it, causing visible pixelation during the CSS zoom.
2. Keep the map's camera static.
3. For each frame, calculate the approved target centre/zoom, then move the canvas with CSS `translate` + `scale`.
4. Apply the same transform to every projected HTML overlay.
5. Continue to animate GeoJSON data and paint properties imperatively; only the renderer camera is frozen.

Keep pitch and bearing constant. Use a 3D engine such as Cesium for genuine changing pitch/bearing or a terrain flythrough.

```ts
const baseZoom = Math.max(start.zoom, end.zoom);
const map = new maptilersdk.Map({
  container,
  style,
  center: end.center,
  zoom: baseZoom,
  pitch: end.pitch ?? 0,
  bearing: end.bearing ?? 0,
  interactive: false,
  fadeDuration: 0,
  canvasContextAttributes: {preserveDrawingBuffer: true},
});

// Per Remotion frame. `camera` is the approved centre/zoom interpolation.
const projected = map.project(camera.center);
const scale = 2 ** (camera.zoom - baseZoom);
const plate = {
  transform: `translate(${width / 2 - projected.x * scale}px, ${height / 2 - projected.y * scale}px) scale(${scale})`,
  transformOrigin: "0 0",
};

// Convert label projection with exactly the same plate transform.
const labelX = labelPoint.x * scale + width / 2 - projected.x * scale;
const labelY = labelPoint.y * scale + height / 2 - projected.y * scale;
```

### Plate sizing and sharpness

- Render at the maximum zoom reached by **any** camera waypoint, including intermediate or hold cameras. The CSS scale should never exceed `1`; otherwise the plate is being enlarged.
- Centre the frozen map on the midpoint of the camera route's geographic extent, not automatically on the final camera. This minimizes required overscan.
- Keep the largest canvas dimension at or below 4096 px unless the actual render environment has been tested with a larger `MAX_RENDERBUFFER_SIZE`.
- For 1920×1080, a 3840×2160 plate is a safe default. For 1080×1920, use approximately 2700×3840 when the route needs extra horizontal pan room.
- If the route cannot fit within that plate at the required zoom, split the shot into two fixed plates with a deliberate editorial transition. Do not trade sharpness for one enormous canvas.
- Distinguish failure modes: repeating shimmer means the live renderer is moving; steadily soft tiles during a CSS push means the fixed plate is underspecified, internally downsampled, or being scaled above `1`.

## Verification

- Render a short MP4, not only a Studio preview.
- Inspect static terrain texture and satellite detail while the camera moves.
- If any underlying map detail wavers, use the fixed map plate. Do not approve it as a minor preview artefact.
- Render WebGL with `--gl=angle`, `preserveDrawingBuffer:true`, and conservative concurrency (`1`) while validating.


<!-- ===== FILE: remotion/remotion-maps/techniques/static-map/TECHNIQUE.md ===== -->

---
name: remotion-maps-static
description: Create a deterministic static locator map in Remotion when neither the camera nor geographic data animates.
---

# Static map

Use a static image when the map only provides location context. This is the smallest, fastest, and
most deterministic map technique.

## Build

1. Export or request a map image at the composition's final aspect ratio and at least its rendered
   pixel dimensions.
2. Store the image in the Remotion project's `public/` directory.
3. Render it with `CanvasImage` and `staticFile()`.
4. Add labels or markers as ordinary Remotion elements if they remain fixed.

```tsx
import React from 'react';
import {AbsoluteFill, CanvasImage, staticFile} from 'remotion';

export const StaticMap: React.FC = () => {
	return (
	  <>
  		<CanvasImage
  			src={staticFile('locator-map.png')}
  			style={{width: '100%', height: '100%', objectFit: 'cover'}}
  		/>
		</>
	);
};
```

## Overlays and Interactivity

Follow [Remotion Interactivity](../../../remotion-interactivity/REFERENCE.md) best practices and [Remotion Markup Best practices](../../../remotion-markup/REFERENCE.md) for elements.
