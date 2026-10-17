

<!-- ===== FILE: hyperframes/media-use/references/media-treatment-recipes.md ===== -->

# Media treatment recipes

These are optional tested seeds, not the complete capability surface. Read the
shared policy and choose one relevant section through `media-treatments.md`.
Agents may modify or combine a seed with compatible canonical controls after
inspecting the media, or assemble a bespoke payload from
`hyperframes media-treatment --capabilities --json` when no seed fits.

## Natural Portrait

Use for a talking head, interview, presenter, or people-focused photo whose
intended result is natural, polished, and restrained.

Do not use when the face is incidental or tiny, the source is intentionally
neon/monochrome/strongly stylized, or the requested result is beauty retouching.
This treatment changes the whole frame; it is not a face mask or skin-smoothing
effect.

Inspect face exposure, highlight retention, shadow detail, white balance, and
whether the existing look is intentional. Signalstats do not detect faces or
creative intent.

### Base payload

Start here, then tune only when the sampled frames justify it:

```json
{ "preset": "skin-soft", "intensity": 0.6 }
```

`skin-soft` is a global tonal/color preset whose vibrance math is reduced for
skin-like colors. It does not blur, retouch, segment, or track a face.

### Bounded tuning

Adjustment values are absolute values in the final payload, not deltas added to
the preset. Keep changes inside these conservative ranges unless the user asks
for a stylized result:

| Property    | Natural Portrait range |
| ----------- | ---------------------- |
| intensity   | 0.45 to 0.75           |
| exposure    | -0.06 to 0.14          |
| contrast    | -0.05 to 0.08          |
| highlights  | -0.18 to -0.04         |
| shadows     | 0.04 to 0.18           |
| whites      | -0.10 to 0.04          |
| blacks      | -0.06 to 0.06          |
| temperature | -0.05 to 0.10          |
| tint        | -0.03 to 0.05          |
| vibrance    | 0 to 0.06              |
| saturation  | -0.04 to 0.06          |

Leave grain, blur, and pixelate at zero. A vignette is optional at `0` to
`0.05` only when it improves subject focus without looking like an effect.

Manual controls must stay inside their schema section; they are never
top-level keys. A tuned Natural Portrait payload looks like this:

```json
{
  "preset": "skin-soft",
  "intensity": 0.58,
  "adjust": {
    "highlights": -0.08,
    "shadows": 0.08,
    "temperature": 0.02,
    "vibrance": 0.02
  },
  "details": { "vignette": 0.03 }
}
```

Use the same nested shape in `grade-compare` candidate files. `adjust` owns
tonal/color controls, `details` owns vignette/grain, and `effects` owns blur,
pixelate, chroma bleed, and the advanced treatment primitives below.

During the common comparison, reject any result that makes skin implausible,
loses highlight detail, flattens or desaturates dark skin, or casts clothing and
background colors accidentally.

## Product Polish

Use for photographed or filmed physical products when the goal is clean,
accurate, dimensional presentation. Protect product color, material texture,
label readability, specular highlights, and intentional lighting.

Do not use this treatment for literal app/site screenshots or screen captures;
follow UI Fidelity below. Do not neutralize a lifestyle scene's deliberate
ambient color, and do not infer exact brand-color correction without a neutral
reference or known product color.

Inspect the product separately from its background. Check white balance, label
legibility, surface texture, highlight clipping, shadow detail, white point,
and black point. Statistics cannot identify a white package, metallic
highlight, amber glass, or intentional warm light.

### Base payload

Compare this restrained correction against the untouched source:

```json
{
  "intensity": 0.7,
  "adjust": {
    "exposure": 0.01,
    "contrast": 0.06,
    "highlights": -0.1,
    "shadows": 0.04,
    "whites": 0.02,
    "blacks": -0.03,
    "vibrance": 0.03,
    "saturation": 0.02
  }
}
```

This is a comparison starting point, not an instruction to change an already
finished source. If the original has accurate color, clean endpoints, and good
texture, leave the pixels unchanged and polish through framing or motion.

### Bounded tuning

| Property    | Product Polish range |
| ----------- | -------------------- |
| intensity   | 0.45 to 0.8          |
| exposure    | -0.08 to 0.1         |
| contrast    | 0 to 0.1             |
| highlights  | -0.16 to 0           |
| shadows     | 0 to 0.12            |
| whites      | -0.08 to 0.05        |
| blacks      | -0.06 to 0.04        |
| temperature | -0.05 to 0.05        |
| tint        | -0.03 to 0.03        |
| vibrance    | 0 to 0.06            |
| saturation  | -0.04 to 0.05        |

Temperature and tint stay at zero unless the frames show a plausible cast.
Leave grain, vignette, blur, and pixelate at zero for catalog/e-commerce media.
For a lifestyle product shot, a vignette up to `0.04` is acceptable only when
it improves focus without changing the product itself.

During the common comparison, reject any result that clips white packaging,
muddies black products, shifts a known brand color, hides texture, or makes
labels harder to read. Report when preserving the original was the deliberate
decision.

## UI Fidelity

Use for literal app, website, dashboard, terminal, slide, or screen-recording
pixels whose colors and readability are part of the product being shown.

The default payload is **none**: do not add `data-color-grading`. Global color
changes affect brand colors, status colors, charts, screenshots, and tiny text
together, so even a tasteful photographic look can make the demonstration less
truthful.

Polish UI footage with crop, scale, pacing, cursor emphasis, surrounding DOM
overlays, or seek-safe motion outside the captured pixels. If the user
explicitly asks for a stylized UI look, preview it against the original and
state that exact UI color is no longer preserved. If a camera filmed a screen,
correct only a demonstrated capture cast or exposure issue and still verify
text and brand colors across representative frames.

## Film Memory

Use when the story explicitly calls for a warm memory, restrained flashback,
personal archive, or film-like recollection. This is not the default meaning of
"cinematic", and it is not scanned-film-stock emulation.

Do not use for literal UI, product catalog media, technical demonstrations, or
footage whose accurate current-day color is important. Use a separate camcorder
treatment for VHS/REC language. Do not add dust, scratches, light leaks, film
burns, or halation unless an owned component is available and the requested
story actually benefits from it.

Check that the source has enough highlight and shadow detail to tolerate a
faded treatment, and confirm nostalgia or temporal separation belongs in the
story. Compare the full moving treatment, not only a still preset card.

### Static pixel base

Start with this owned shader recipe:

```json
{
  "preset": "vintage-wash",
  "intensity": 0.6,
  "details": {
    "vignette": 0.12,
    "grain": 0.12,
    "grainSize": 0.2,
    "grainRoughness": 0.6
  }
}
```

Keep the static values inside these ranges:

| Property       | Film Memory range |
| -------------- | ----------------- |
| intensity      | 0.5 to 0.75       |
| vignette       | 0.08 to 0.16      |
| grain          | 0.08 to 0.16      |
| grainSize      | 0.16 to 0.24      |
| grainRoughness | 0.5 to 0.7        |

The stronger end can flatten dark skin, black clothing, or already-faded
footage. Compare against the source and lower strength when it does.

### Temporal character

Use the existing registered paused GSAP timeline on the same media element:

- author `--hf-color-grading-exposure: 0` in the media element's inline
  `style`;
- move it through a finite irregular sequence within `-0.03` to `0.03`, using
  gentle `sine.inOut` segments around `0.45` to `0.8` seconds;
- for gate weave, keep `x`/`y` within `0.15%` of the shorter composition edge,
  rotation within `0.03` degrees, and scale between `1.005` and `1.01` to
  protect the frame edges;
- return close to the starting exposure and transform at the treatment end.

Do not use randomness, infinite CSS keyframes, timers, or `onUpdate`. Flicker
is a gentle exposure pulse, not a flash. Weave is slight mechanical drift, not
handheld shake.

Also run focused keyframe diagnostics and seek directly to the final-minus-frame
position. Reject brightness pumping, distracting drift, clipped edges, or
skin/detail loss. Report the motion ranges and describe this as an HF
film-memory treatment, not camera-stock emulation. If motion reads as an effect
before it reads as a memory, reduce or remove it.

## Creator Camcorder

Use when the story explicitly calls for a creator-camera recording, consumer
camcorder memory, or restrained digital-video character. This treatment is a
modern camcorder language, not VHS restoration, CRT simulation, surveillance,
or a promise to reproduce a specific camera model.

Do not apply it to literal UI, product catalog media, tiny media tiles, or
already compressed footage that has distracting color bleed. Do not add a REC
HUD merely because the source contains a person talking; the camera-device
language must support the story or the user's requested style.

Check skin, saturated edges, fine text, source compression, and whether the
source already has a deliberate camera look. Reject softened chroma that
damages labels, graphics, or identifying product color. Judge chroma softness
and grain in motion, not one still.

### Static pixel base

Start with the proven shader payload below, then tune only inside the bounded
ranges when representative frames justify it:

```json
{
  "intensity": 0.72,
  "adjust": {
    "contrast": 0.08,
    "highlights": -0.05,
    "shadows": 0.02,
    "whites": 0.03,
    "blacks": -0.04,
    "temperature": -0.03,
    "tint": -0.015,
    "vibrance": -0.03,
    "saturation": -0.06
  },
  "details": {
    "vignette": 0.06,
    "grain": 0.08,
    "grainSize": 0.18,
    "grainRoughness": 0.58
  },
  "effects": { "chromaBleed": 0.55 }
}
```

| Property       | Creator Camcorder range |
| -------------- | ----------------------- |
| intensity      | 0.55 to 0.8             |
| contrast       | 0.03 to 0.1             |
| highlights     | -0.1 to 0               |
| shadows        | 0 to 0.06               |
| whites         | 0 to 0.05               |
| blacks         | -0.08 to -0.01          |
| temperature    | -0.06 to 0.04           |
| tint           | -0.03 to 0.02           |
| vibrance       | -0.06 to 0.02           |
| saturation     | -0.12 to -0.02          |
| vignette       | 0.03 to 0.1             |
| grain          | 0.04 to 0.12            |
| grainSize      | 0.14 to 0.24            |
| grainRoughness | 0.45 to 0.7             |
| chromaBleed    | 0.35 to 0.7             |

Leave blur and pixelate at zero. Square pixels, scanlines, RGB splitting, and
tracking noise are different visual languages and are not defaults for this
treatment.

### Optional camera HUD

When the narrative benefits from explicit recording-device language, install
the Registry overlay block:

```bash
npx hyperframes add camcorder-hud --no-clipboard
```

Insert the printed `data-composition-src` host over the intended media range.
Edit the displayed date/time/mode/counter in
`compositions/camcorder-hud.html`. The block's paused GSAP timeline derives
its counter and REC blink from composition time, so play, scrub, and render
agree. Keep the HUD finite and scoped to the shot.

The HUD is an optional authored overlay. The pixel payload remains useful
without it, and the HUD alone is not evidence that the footage was treated.

### Optional source-to-camera reveal

Global grading intensity fades only primary correction and LUT output; it does
not fade the independent camcorder effects. For a visible source-to-camera
mode change, use two synchronized media layers and a finite opacity crossfade
from untreated to treated footage. Fade the HUD in on that same paused GSAP
timeline. Do not animate shader state with callbacks or an independent clock.

Also verify HUD placement and framing in each aspect ratio the project supports.
Report whether the HUD was used and describe this as an HF camcorder treatment,
not camera/VHS emulation. If an effect artifact is more noticeable than the
subject, reduce chroma bleed/grain or keep the source unchanged.

## VHS Playback

Use when the story explicitly calls for analog home-video tape, a dated archive,
or a visibly degraded VHS playback. This treatment is not Creator Camcorder,
generic pixelation, CRT display simulation, or a default retro look.

Do not use for literal UI, product catalog media, small text, clean modern
creator footage, or any source whose identifying color/detail must remain exact.
Inspect high-contrast vertical edges, faces, saturated objects, and the bottom
of the frame in motion. Analog damage must support the story without making the
subject hard to read.

### Pixel payload

Start with the complete proven combination, not `tapeDamage` alone:

```json
{
  "intensity": 1,
  "adjust": { "contrast": -0.04, "saturation": -0.08 },
  "details": {
    "grain": 0.16,
    "grainSize": 0.12,
    "grainRoughness": 0.72
  },
  "effects": {
    "tapeDamage": 0.82,
    "tapeTracking": 0.85,
    "tapeNoise": 0.3,
    "tapeSpeed": 0.5,
    "chromaBleed": 0.5,
    "chromaticAberration": 0.18,
    "chromaticAngle": 0,
    "scanlines": 0.35,
    "scanlineCount": 0.17,
    "scanlineSoftness": 1,
    "digitalGlitch": 0.32,
    "digitalGlitchColorSplit": 0,
    "digitalGlitchLineTear": 0.08,
    "digitalGlitchPixelate": 0,
    "digitalGlitchBlockAmount": 0,
    "digitalGlitchBlockDisplacement": 0,
    "digitalGlitchBlockOpacity": 0,
    "digitalGlitchSpeed": 0.5
  }
}
```

| Property              | VHS Playback range |
| --------------------- | ------------------ |
| intensity             | 0.75 to 1          |
| contrast              | -0.1 to 0          |
| saturation            | -0.16 to 0         |
| grain                 | 0.08 to 0.18       |
| grainSize             | 0.08 to 0.18       |
| grainRoughness        | 0.55 to 0.8        |
| tapeDamage            | 0.65 to 0.9        |
| tapeTracking          | 0.5 to 0.9         |
| tapeNoise             | 0.15 to 0.45       |
| tapeSpeed             | 0.35 to 0.65       |
| chromaBleed           | 0.35 to 0.65       |
| chromaticAberration   | 0.08 to 0.22       |
| scanlines             | 0.2 to 0.4         |
| scanlineCount         | 0.14 to 0.2        |
| digitalGlitch         | 0.2 to 0.4         |
| digitalGlitchLineTear | 0.04 to 0.1        |

`tapeDamage` owns deterministic horizontal line jitter, slow time-base wobble,
bottom-edge head switching, luma bandwidth loss, restrained ghosting, noise,
and sparse dropouts. Its subordinate tracking/noise/speed controls add bounded
moving tape tears and control their signal character without introducing a new
clock. `chromaBleed` separately reduces horizontal chroma detail. The restrained
scanline and chromatic settings supply the remaining tape-playback character.
The digital stage is used only for rare horizontal row tears: keep its color
split, pixelation, block displacement, block opacity, and corruption values at
zero. Leave blur, CRT curvature, generic pixelation, and a camera HUD off.

These values are an original HyperFrames recipe calibrated on the same public
Orange Cat source used for the external visual reference. They are not copied
shader code or a claim of pixel-identical output from the external reference. The scanline count is
mapped to the reference's approximately 127-cycle primary line pattern; the HF
tracking math stays bounded in media pixels and uses the composition clock.

The shader damage evolves from the existing deterministic media time, so it
needs no CSS loop or private timeline. Global grading intensity does not fade
tape damage or other independent effects. If the story requires a finite
source-to-tape reveal, crossfade synchronized untreated and treated media layers
on the host's paused GSAP timeline. During the common workflow, inspect dense
consecutive frames and reject hard edge tearing, face
smearing, frozen noise, square blocks, blank borders, or a bottom disturbance
that competes with the subject.

## 8mm Home Movie

Use for personal archive, family-memory, childhood, travel-memory, or explicit
small-gauge home-movie language. This is stronger and more materially film-like
than Film Memory, but it is still an owned HyperFrames treatment rather than a
claim to reproduce a named film stock, camera, or laboratory process.

Do not use for literal UI, technical demonstrations, catalog products, clean
interviews, or footage where dust/scratches would imply false provenance. Check
skin, highlights, dark clothing, and frame edges before applying it.

### Pixel payload

```json
{
  "preset": "vintage-wash",
  "intensity": 0.72,
  "details": {
    "vignette": 0.28,
    "vignetteMidpoint": 0.54,
    "vignetteFeather": 0.72,
    "grain": 0.34,
    "grainSize": 0.18,
    "grainRoughness": 0.72
  },
  "effects": { "filmArtifacts": 0.62 }
}
```

| Property       | 8mm Home Movie range |
| -------------- | -------------------- |
| intensity      | 0.6 to 0.8           |
| vignette       | 0.18 to 0.34         |
| grain          | 0.22 to 0.42         |
| grainSize      | 0.12 to 0.24         |
| grainRoughness | 0.6 to 0.8           |
| filmArtifacts  | 0.35 to 0.7          |

`filmArtifacts` owns only deterministic sparse dust and short scratches. The
existing preset/details own color, vignette, and grain; the host's paused GSAP
timeline owns optional gate weave. Keep weave within `0.15%` of the shorter
composition edge, rotation within `0.03` degrees, and scale between `1.005` and
`1.015`. Use finite `sine.inOut` segments around `0.6` to `1` second, return
near the starting transform, and never use randomness, timers, `onUpdate`, or
an infinite CSS animation.

Reject a result when dust is constantly visible, scratches persist unnaturally,
the frame pumps, weave exposes an edge, highlights turn muddy, or the material
artifacts are more noticeable than the memory. For a subtler nostalgic result,
use Film Memory instead.

## Editorial Halftone

Use for print/editorial transitions, poster frames, comic/newsprint language,
stylized product or portrait beats, and graphic sequences where visible ink
screening is the point. This is a real four-angle CMYK raster treatment, not a
dotted DOM overlay.

Do not use on literal UI, dense text, tiny labels, footage that must remain
photorealistic, or a long talking-head segment unless the user explicitly asks
for strong print stylization. Preserve text/captions as ungraded DOM above the
media whenever they must stay readable.

### Pixel payload

```json
{
  "intensity": 1,
  "adjust": { "contrast": 0.04, "saturation": 0.04 },
  "effects": { "halftone": 0.94, "halftoneSize": 0.36 }
}
```

| Property     | Editorial Halftone range |
| ------------ | ------------------------ |
| intensity    | 0.8 to 1                 |
| contrast     | -0.02 to 0.08            |
| saturation   | -0.04 to 0.08            |
| halftone     | 0.75 to 1                |
| halftoneSize | 0.15 to 0.55             |

The shader uses fixed C/M/Y/K screen angles of 15/75/0/45 degrees, separate ink
coverage, a warm paper base, and resolution-aware dot-cell sizing. Keep those
screen semantics fixed; tune only amount and size unless a future visual proof
justifies a broader schema. Judge the result at final output resolution because
browser zoom can misrepresent the screen. Reject unstable moire, unreadable
subjects, clipped ink detail, excessive dot size, or any treatment that looks
like a transparent dot texture laid over unchanged footage.

## Two-Ink Editorial Print

Use for poster frames, editorial portraits, music/social cutaways, zine
graphics, and bold print-led transitions where two visible spot inks are more
appropriate than photographic color. This is a fixed original HyperFrames
vermilion/teal treatment, not a claim to emulate a named printer, ink set, or
commercial print process.

Do not use for literal UI, brand-color-critical products, small labels, natural
talking heads, or media that must remain photorealistic. Keep captions and
graphics as normal DOM above the treated media.

### Pixel payload

```json
{
  "intensity": 1,
  "adjust": { "contrast": 0.08, "highlights": -0.06, "shadows": 0.04 },
  "effects": { "twoInkPrint": 1, "twoInkPrintSize": 0.42 }
}
```

| Property        | Two-Ink range |
| --------------- | ------------- |
| intensity       | 0.8 to 1      |
| contrast        | 0.02 to 0.1   |
| highlights      | -0.1 to 0     |
| shadows         | 0 to 0.08     |
| twoInkPrint     | 0.8 to 1      |
| twoInkPrintSize | 0.18 to 0.55  |

The shader maps warm midtones to vermilion, deep/cool shadows to teal, and
shared dark coverage to a dark overprint on warm paper. It uses separate
15/75-degree screens, a subtle fixed registration offset, deterministic paper
texture, and resolution-aware dot sizing. Do not combine it with `halftone` or
a duotone LUT: that re-separates the result and defeats the two-ink contract.

Judge it at output resolution and across multiple frames. Reject missing second
ink, crushed faces, unstable moire, illegible silhouettes, or a result that
reads as a red tint with dots rather than two screened inks.

## Monochrome Screen Print

Use for graphic portrait beats, posterized social inserts, newspaper-like
screens, or a finite transition into visible monochrome cells. Keep captions
and typography as normal DOM above the treated media.

```json
{
  "intensity": 1,
  "effects": {
    "monoScreen": 1,
    "monoScreenSize": 0.35,
    "monoScreenAngle": 0.25,
    "monoScreenSpread": 0.3,
    "monoScreenShape": 0,
    "monoScreenInvert": 0
  },
  "palette": ["#111319", "#f2ecdc"]
}
```

Use `monoScreenShape` `0..4` for circle, square, diamond, triangle, or line.
Keep cell size within `0.15..0.55` and spread within `0.15..0.55`. Reject faces
that lose their silhouette, unstable moire, or cells too small to survive the
final encoded resolution.

## Engraved Illustration

Use for editorial portraits, historical/technical illustration, title-card
cutaways, or a source-to-line-art reveal. It is not routine correction and
should not be applied to literal UI or brand-color-critical product footage.

```json
{
  "intensity": 1,
  "effects": {
    "engraving": 1,
    "engravingSpacing": 0.4118,
    "engravingMinThickness": 0.2,
    "engravingMaxThickness": 0.4571,
    "engravingAngle": 0.25,
    "engravingContrast": 0.4667,
    "engravingSharpness": 0.59,
    "engravingWave": 0.2,
    "engravingWaveFrequency": 0.2222
  },
  "palette": ["#101216", "#f3eddf"]
}
```

Preserve the calibrated base first. Tune spacing within `0.25..0.6`, contrast
within `0.3..0.65`, and wave within `0..0.35`. Reject squeezed framing, broken
contours, noisy flat backgrounds, or lines that flicker across moving frames.

## Crosshatched Sketch

Use for hand-rendered editorial beats, comic/documentary cutaways, and short
illustrative transformations where multiple line directions should preserve
the subject contour.

```json
{
  "intensity": 1,
  "effects": {
    "crosshatch": 1,
    "crosshatchSpacing": 0.28,
    "crosshatchThickness": 0.25,
    "crosshatchAngle": 0.25,
    "crosshatchContrast": 0.3333,
    "crosshatchEdges": 0.5,
    "crosshatchLineWeight": 0,
    "crosshatchWave": 0.33,
    "crosshatchWaveFrequency": 0.2222
  },
  "palette": ["#101216", "#f3eddf"]
}
```

Tune spacing within `0.18..0.5`, edge detail within `0.3..0.7`, and wave within
`0.1..0.45`. Reject distorted aspect ratio, dense black fill that hides the
subject, or temporal shimmer stronger than the intended sketch language.

## CRT Display

Use when the media is intentionally shown as an older monitor, terminal, game
screen, or broadcast display. Curvature alone is geometry, not a complete CRT
treatment, so pair it with restrained scanlines and only slight channel
separation.

```json
{
  "intensity": 1,
  "effects": {
    "crtCurvature": 0.2,
    "scanlines": 0.35,
    "scanlineCount": 0.17,
    "scanlineSoftness": 1,
    "chromaticAberration": 0.08,
    "chromaticAngle": 0
  }
}
```

Keep curvature within `0.08..0.28`, scanlines within `0.18..0.45`, and channel
separation within `0..0.12`. Reject excessive black corners, unreadable UI,
large color fringes, or applying the display language to ordinary footage when
the user only asked for correction.

## Procedural ASCII

Use for a deliberate terminal, code, data, surveillance, editorial, or
source-to-character reveal. This is a real shader-generated 5x7 glyph field,
not monospace text placed over unchanged footage.

Do not use as routine talking-head polish, on literal UI or dense text, or when
recognizing a face/product precisely matters. Keep captions and graphics as
normal DOM above the treated media.

Choose one of these proven starting points:

```json
{
  "effects": { "ascii": 1, "asciiSize": 0.08, "asciiInvert": 1 },
  "palette": ["#020605", "#38ff78"]
}
```

The first is **Terminal ASCII**: dark field, bright green glyphs, appropriate
for code/data/device language. For a warmer print-like **Editorial ASCII**, use:

```json
{
  "effects": { "ascii": 1, "asciiSize": 0.066, "asciiInvert": 0 },
  "palette": ["#0b0d0d", "#eee9db"]
}
```

Keep `ascii` between `0.75` and `1` for a fully readable treatment and
`asciiSize` between `0.04` and `0.15`. A finite reveal may author
`--hf-color-grading-ascii: 0` inline and tween it to `1` with the registered
paused GSAP timeline. Reject unstable cells, lost silhouette/face structure,
unreadable composition, or a palette that conflicts with the project.

## Ordered Palette Dither

Use for posterized social beats, music/editorial cutaways, pixel-art language,
or a finite source-to-palette reveal. The shader uses a stable 4x4 Bayer
threshold matrix and an explicit dark-to-light palette. Do not describe it as
Floyd-Steinberg, Atkinson, or another sequential error-diffusion process.

Do not use on literal UI, brand-color-critical products, tiny labels, or long
photorealistic sections. Start with one of these original palettes:

```json
{
  "effects": { "dither": 1, "ditherSize": 0.25 },
  "palette": ["#17121a", "#824c50", "#e09873", "#f7ddb1"]
}
```

The four-color option is **Warm Print**. For a louder social/music beat, use
the six-color **Electric Ink** palette:

```json
{
  "effects": { "dither": 1, "ditherSize": 0.4 },
  "palette": ["#080717", "#3c185f", "#7e2278", "#d9339f", "#ff6b66", "#aafae0"]
}
```

HyperFrames also owns these named ramps. The name is an authoring shortcut;
persist the listed colors through the existing `palette` array:

| Group       | Palette ID       | Ordered colors                                                   |
| ----------- | ---------------- | ---------------------------------------------------------------- |
| Classic     | `noir`           | `#000000`, `#ffffff`                                             |
| Classic     | `ink-paper`      | `#1a1a2e`, `#f5f5dc`                                             |
| Classic     | `terminal`       | `#001100`, `#00ff00`                                             |
| Classic     | `amber-glow`     | `#1a0f00`, `#ffcc00`                                             |
| Classic     | `handheld-green` | `#0f380f`, `#306230`, `#8bac0f`, `#9bbc0f`                       |
| Mood        | `golden-hour`    | `#1a1205`, `#4a3510`, `#8b6914`, `#d4a017`, `#fff8dc`            |
| Mood        | `deep-sea`       | `#0a1628`, `#1a3a5c`, `#2d6187`, `#5ba4c9`, `#a8dce8`            |
| Mood        | `arctic-night`   | `#0a0a14`, `#1a2a4a`, `#3a5a8a`, `#6a9aca`, `#cae8ff`            |
| Mood        | `synthwave`      | `#120458`, `#7b2cbf`, `#e040fb`, `#ff6ec7`, `#fff59d`            |
| Mood        | `vaporwave`      | `#1a0a2e`, `#3d1a5c`, `#ff71ce`, `#01cdfe`, `#fffb96`            |
| Mood        | `forest`         | `#1a2e1a`, `#2d4a2d`, `#4a7c4a`, `#7ab37a`, `#c8e6c8`            |
| Mono        | `sepia`          | `#1a1610`, `#3d3020`, `#6b5a40`, `#a89070`, `#e8dcc8`            |
| Mono        | `blueprint`      | `#001830`, `#003060`, `#0050a0`, `#0080e0`, `#e0f0ff`            |
| HyperFrames | `warm-print`     | `#17121a`, `#824c50`, `#e09873`, `#f7ddb1`                       |
| HyperFrames | `electric-ink`   | `#080717`, `#3c185f`, `#7e2278`, `#d9339f`, `#ff6b66`, `#aafae0` |

Choose by inspected source and project language, not by palette name alone.
For example, `terminal` fits device/code language, `warm-print` fits editorial
print, and `synthwave` is an intentional stylization rather than generic polish.

`palette` must contain two to six exact `#RRGGBB` colors in authored order. Use
dark-to-light order for this treatment; the runtime validates colors but does
not reorder them, so reversing the array intentionally inverts the mapping.
Keep `dither` between `0.7` and `1` and `ditherSize` between `0.1` and `0.5`.
A finite reveal may author `--hf-color-grading-dither: 0` inline and tween it
to the chosen amount with GSAP. Judge the moving result at output resolution;
reject shimmer, lost subject structure, accidental muddy intermediate colors,
or a palette chosen without regard to the project's design language.

## Cached Error Diffusion

Use exact error diffusion for a deliberate 1-bit Macintosh, newspaper/print,
limited-palette game, or crunchy editorial treatment. It bakes a new image or
MP4 because every processed block depends on error from earlier blocks; it is
not a realtime shader setting.

Choose the algorithm by visible intent:

- `floyd-steinberg`: balanced default with organic fine texture.
- `atkinson`: higher-contrast, more open and distinctly early-Macintosh.
- `jarvis-judice-ninke`: smoother gradients with a wider 12-neighbor field.
- `stucki`: smooth, slightly sharper alternative to JJN.
- `burkes`: compact two-row texture.
- `sierra`, `sierra-lite`, `two-row-sierra`: progressively different
  speed/texture tradeoffs; use only after comparing frames.

Run the exact processor and register its output through the existing media
ledger/cache:

```bash
node <SKILL_DIR>/scripts/dither.mjs \
  --input .media/videos/video_001.mp4 \
  --out .media/generated/video_001.atkinson.mp4 \
  --algorithm atkinson \
  --palette '#17121a,#824c50,#e09873,#f7ddb1' \
  --point-size 3

npx hyperframes media-use resolve \
  --from .media/generated/video_001.atkinson.mp4 --type video --project .
```

Use the registered output path on a real `<img>` or `<video>`. Keep text,
captions, logos, and interface graphics outside the processed media. For a
finite reveal, overlap the original and processed media with identical framing
and crossfade or wipe them using the registered paused GSAP timeline. Do not
label the realtime Bayer shader as Floyd-Steinberg/Atkinson, and do not process
PQ/HLG footage without an explicit SDR tone-map decision.

## Organic Light Leak

Use for one motivated memory beat, time shift, warm scene handoff, or tactile
transition. It is a finite deterministic CSS/GSAP overlay, not a looping
texture, generic flash, or film-stock emulation.

Install the Registry overlay block:

```bash
npx hyperframes add organic-light-leak-overlay --no-clipboard
```

Insert the printed `data-composition-src` host at the intended beat and keep
its duration finite. Its paused timeline owns one rise, peak, and complete
recovery and scales those phases to the placed duration. Inspect the source
before, at the brightest frame, and after recovery. Reject clipped faces, an
unmotivated warm wash, visible black from incorrect blend mode, or a leak that
conceals the subject longer than the transition needs.

## Freeze-Frame Cutout

Use for a social introduction, speaker emphasis, chapter punctuation, sports
or creator beat, or a scrapbook/editorial hold. This requires a real alpha
matte; decoration may not conceal a poor subject edge.

Extract the exact deterministic source frame first, then remove its background:

```bash
ffmpeg -ss <seconds> -i <source-video> -frames:v 1 -y .media/generated/freeze-source.png
npx hyperframes remove-background .media/generated/freeze-source.png \
  -o .media/generated/freeze-cutout.png --json
npx hyperframes add freeze-frame-dressing --no-clipboard
```

Add the transparent result as a direct-root timed media layer and insert the
printed overlay block above the same time range. The block owns the paper,
tape, and flash; the host timeline only animates the real cutout:

```html
<img
  id="hf-freeze-cutout"
  class="clip"
  src="./.media/generated/freeze-cutout.png"
  alt=""
  data-start="6"
  data-duration="3"
  data-track-index="20"
/>
```

```js
tl.fromTo(
  "#hf-freeze-cutout",
  { y: 42, scale: 0.86, rotation: -2 },
  { y: 0, scale: 1, rotation: 0.4, duration: 0.5, ease: "back.out(1.35)" },
  freezeAt,
);
```

Inspect the matte over both light and dark temporary plates before styling it.
Reject missing hair/fingers, background halos, a cutout that changes identity,
overly thick outline, exposed frame edges, or a flash that obscures the reveal.
If the matte is not acceptable, choose another frame or keep the original media.

## Social Flash / Editorial Reveal

Use this treatment for one meaningful high-energy cut, creator reveal, product
beat, or before/after handoff. It is not a default transition for every scene.
Avoid it for calm long-form footage, accessibility-sensitive contexts, already
clipped highlights, literal UI that must remain readable through the cut, or
any request for repeated strobing.

Inspect representative frames on both sides of the cut first. Grade each media
layer for its own subject using the appropriate contract above; the flash is
not a substitute for correction. For people, a restrained `skin-soft` payload
is a safe starting point. For literal UI, preserve the pixels and use only the
authored light/motion layers when they do not obscure required information.

Install the Registry overlay block:

```bash
npx hyperframes add editorial-flash-overlay --no-clipboard
```

Insert the printed `data-composition-src` host so the block's midpoint lands
on the cut. Its own paused timeline drives the finite flash. The host timeline
may coordinate outgoing and incoming media motion without reaching into the
block:

```js
tl.to(
  "#outgoing-media",
  {
    scale: 1.035,
    "--hf-color-grading-exposure": 0.82,
    duration: 0.12,
    ease: "power3.in",
  },
  cutAt - 0.16,
);
tl.fromTo(
  "#incoming-media",
  { scale: 1.1 },
  { scale: 1, duration: 0.42, ease: "power3.out" },
  cutAt,
);
tl.to(
  "#incoming-media",
  {
    "--hf-color-grading-exposure": 0,
    "--hf-color-grading-intensity": 0.58,
    duration: 0.24,
    ease: "power2.out",
  },
  cutAt,
);
```

When the shader steps are used, author
`--hf-color-grading-exposure: 0.72` and
`--hf-color-grading-intensity: 0` inline on the incoming media so a fresh seek
has the correct start state. Set the final intensity to the source-approved
value instead of copying `0.58` blindly. Skip the shader intensity step when
the incoming source should remain ungraded.

Keep the rise between roughly `0.035` and `0.055` seconds and the recovery
between `0.24` and `0.38` seconds. Default to one neutral/warm flash event,
never saturated red, never a looping strobe, and never more than one authored
flash inside a one-second treatment window. Verify frames immediately before,
at, and after the cut, then inspect moving playback and a rendered draft. The
peak must hide the cut; the recovery must reveal a correctly framed source with
no retained prior canvas, clipped face, or unexpected highlight damage.


<!-- ===== FILE: hyperframes/media-use/references/media-treatments.md ===== -->

# Media treatments

A media treatment is a source-aware plan that composes existing HyperFrames
color, effect, timeline, and Registry primitives. It is not a second runtime
schema. Use this file to choose a primary direction. A matching recipe is an
optional tested seed; bespoke requests may assemble a validated treatment from
the canonical capability catalog.

## Permission and scope

- An explicit request such as "polish this", "make it look better", or "make it
  fit the topic" delegates a conservative treatment. Apply it, verify it, and
  report what changed.
- During an unsolicited opportunity scan, show or suggest the treatment first.
- Target meaningful photographic media. Skip text, SVG, logos, icons, UI
  chrome, and intentionally stylized footage unless the user asks.
- Realtime grading and effects apply to the entire selected real `<img>` or
  `<video>`. They do not isolate or track a face, plate, address, or other
  region. For region-only work, first create a separate cropped/masked media
  layer or use an external segmentation/tracking tool; never imply that a
  whole-media Blur or Pixelate performed region isolation.
- The realtime treatment path is Rec.709/SDR. Do not silently process HDR, HLG,
  PQ, or camera LOG sources through it.

## Classify the request

Choose the smallest lane that satisfies the request before choosing a recipe
or assembling a custom treatment:

| User intent                                         | Lane                                       |
| --------------------------------------------------- | ------------------------------------------ |
| too dark, flat, too warm, too many shadows          | correction                                 |
| shape shadows/highlights or selected colors         | wheels, curves, or HSL secondary           |
| polished, premium, warm, cinematic, fit the topic   | preset or custom treatment                 |
| retro, print, ASCII, glitch, camcorder              | shader effect or effect-bearing preset     |
| obscure the whole selected media                    | privacy Blur or Pixelate                   |
| hide one face, plate, address, or screen region     | separate crop/mask/asset or external tool  |
| draw attention to media without changing its pixels | framing, motion, or optional overlay       |
| reveal, focus, depixelate, fade the treatment       | finite seek-safe treatment keyframes       |
| REC HUD, light leak, flash, freeze-frame cutout     | Registry overlay plus any justified pixels |

The lane identifies the primary reason for the change; it is not a one-feature
limit. A final treatment may combine correction, a preset, finishing, multiple
compatible shader effects, finite keyframed values, and optional overlays when
the inspected media and user intent justify the complete combination. Keep one
primary intent as the creative anchor so the result remains coherent and
deterministic.

Do not add a stylized Effect when correction solves the complaint. Do not
change color when the request is only temporal, and do not install an overlay
when the selected media alone communicates the result.

Match strength to intent. When the user explicitly names a bold look such as
VHS, glitch, ASCII, halftone, camcorder, print, or engraving, apply its
signature effects strongly enough to read unmistakably. The guard against
unrequested additions does not mean under-delivering an effect the user asked
for. Correction and polish stay restrained; named stylization must be obvious
in the after-frame.

### Translate vague feedback conservatively

| User feedback                         | First action                                                                                    | Add only when the frames justify it                             | Never infer                                     |
| ------------------------------------- | ----------------------------------------------------------------------------------------------- | --------------------------------------------------------------- | ----------------------------------------------- |
| too many shadows and a bit boring     | lift shadows/protect highlights, then compare one restrained source-appropriate preset          | mild contrast or vibrance                                       | retro texture, HUD, or palette effect           |
| make the product footage feel premium | protect product color and labels, compare Product Polish                                        | restrained vignette on lifestyle footage                        | a cinematic LUT or crushed blacks               |
| make this reveal cooler               | preserve color and animate one supported effect or treatment value                              | a short owned overlay block                                     | unrelated whole-clip styling                    |
| make it feel like an old home video   | compare 8mm and VHS language against the source                                                 | finite weave/flicker or justified HUD                           | that every old-video request means VHS          |
| hide this face                        | explain that realtime effects are whole-media; isolate the region first or use an external tool | whole-media Blur/Pixelate only when the user accepts that scope | face tracking or masking that was not performed |
| keep the brand colors exact           | leave UI/logo pixels unchanged; use framing and motion                                          | demonstrated exposure-only correction                           | stylized preset, palette, or LUT                |

When more than one lane could fit, generate at most two candidates and choose
from inspected before/after evidence. Ordinary correction or polish starts with
one candidate; a second candidate is an escalation, not the default. Do not
stack effects merely to make the answer look more sophisticated.

## Seed or assemble

Use the table when a tested recipe directly fits. Read only that recipe
section. Recipes are optional macros, not a closed list of allowed results.

| Intent or source                                         | Recipe heading to read                            |
| -------------------------------------------------------- | ------------------------------------------------- |
| Talking head, interview, presenter, people-focused photo | `Natural Portrait`                                |
| Product footage, lifestyle footage, clean social polish  | `Product Polish`                                  |
| Screen capture, dashboard, website, app UI               | `UI Fidelity`                                     |
| Warm memory, restrained nostalgia                        | `Film Memory`                                     |
| Creator/UGC handheld camera character                    | `Creator Camcorder`                               |
| Analog tape playback                                     | `VHS Playback`                                    |
| Small-gauge home-movie character                         | `8mm Home Movie`                                  |
| Editorial dots or ink print                              | `Editorial Halftone` or `Two-Ink Editorial Print` |
| Monochrome dot/line screen print                         | `Monochrome Screen Print`                         |
| Engraved or hand-hatched illustration                    | `Engraved Illustration` or `Crosshatched Sketch`  |
| Curved scanlined display                                 | `CRT Display`                                     |
| Glyph-based art                                          | `Procedural ASCII`                                |
| Realtime palette quantization                            | `Ordered Palette Dither`                          |
| Exact historical error diffusion                         | `Cached Error Diffusion`                          |
| Finite warm flare layer                                  | `Organic Light Leak`                              |
| Held-frame graphic interruption                          | `Freeze-Frame Cutout`                             |
| Short exposure-flash transition                          | `Social Flash / Editorial Reveal`                 |

Use `rg -n '^## <heading>$' <SKILL_DIR>/references/media-treatment-recipes.md`,
then read only from that heading to the next `##`. Do not load the entire
cookbook for one request.

When source intent is unclear, inspect the concise capability overview:

```bash
hyperframes media-treatment --capabilities --json
```

It lists the complete surface by family with one-line descriptions. Then load
only the family, effect, preset, or palette relevant to the inspected source:

```bash
hyperframes media-treatment --capability <id> --json
```

The focused result provides legal controls, recommended apply values, render
cost, palette support, and the exact animation contract when supported. Use
`--all` only for tooling/tests or a genuinely exhaustive audit. Compose one
nested payload from these existing parts. Recipes and catalog-built payloads
use the same renderer and persistence contract.

Treat `renderLane: "multipass"` as a cost signal. Blur, Bloom, and Kuwahara are
bounded but more expensive than single-pass effects; avoid stacking several of
them across many simultaneous media elements unless the composition needs it,
then verify playback and a draft render.
Cost follows treated pixel area as well as element count. More than two
simultaneously visible full-frame multipass media layers requires a continuous
playback check on the target machine; simplify or pre-render the stack if it
drops frames. Do not impose or claim a universal hard cap from one machine.

## Common workflow

1. Confirm the target is a real `<img>` or `<video>` and inspect source color
   metadata.
2. For an image, read it once. For video, capture early/middle/late output as
   one labeled sheet and read that one image:

   ```bash
   hyperframes snapshot <project> --frames 3 --no-end --describe false \
     --output snapshots/treatment-before
   ```

   Read `snapshots/treatment-before/contact-sheet.jpg`; do not spend separate
   model turns reading each frame unless the sheet exposes a specific problem.
   Do not infer semantics from signal statistics alone.

3. Choose one primary lane. Use one matching recipe as a tested seed, or read
   the overview and one focused capability detail when the request is bespoke.
   A seed may be changed or combined with compatible catalog controls when the
   contact sheet justifies it. Do not invent keys, exceed reported ranges, or
   stack effects without a visual reason. Do not run the generic grade/LUT
   resolver first; it adds irrelevant candidates and may download an unused
   LUT. Use `media-treatment --selector "#hero" --analyze --json` only when
   correction needs measured signal evidence.
4. Persist pixel settings with `hyperframes media-treatment`; it validates and
   merges a patch into the existing nested `data-color-grading` contract. Use registered
   GSAP only for supported animated values and Registry overlay blocks only
   for authored dressing.
   ```bash
   hyperframes media-treatment --selector "<selector>" \
     --grading '<nested JSON patch>' --apply --json
   ```
   A selector that matches several images or videos patches every match, each
   merged into its own current grading (the JSON reports `count` and each
   target); run `--clear` first for an identical look, or add
   `--selector-index` to patch only one.
   For a temporal reveal, use the focused capability result's `animation`
   contract. If it is `null`, the capability is static. Author the starting CSS
   property inline on the real media element and return temporary treatment
   values to neutral so the finished shot preserves its existing pixels.
   Prefer that bounded media animation first; if an overlay is justified,
   install the owned Registry block instead of recreating it with bespoke
   overlay markup.
   For correction and ordinary polish, keep those values as editable
   preset/adjustment JSON; do not generate a LUT for controls the realtime shader
   already owns.
   Use the canonical `details`/`effects` fields for vignette, grain, blur,
   pixelate, and related primitives. Do not duplicate them with CSS filters,
   SVG turbulence, opacity, or decorative DOM overlays.
5. When the treatment calls for an overlay, install that named block with
   `hyperframes add <name> --dir <project> --no-clipboard --json`, inspect its
   returned `data-composition-src` host, and place it once using the block's
   timing contract. Check for the installed file and host element
   ID before insertion; never duplicate an existing overlay block. This is one
   treatment workflow: do not make the user discover Catalog or separately ask
   for the recipe's justified overlay.
6. For ordinary correction/polish, capture one after-sheet with the same three
   timestamps under `snapshots/treatment-after`, compare it to the before-sheet,
   and stop when the result is clearly better. Run the normal project check;
   do not encode a draft solely to prove a static correction.
7. Escalate only when evidence requires it. Read individual frames to diagnose a
   specific visual problem. Preview and render moving evidence when judging
   treatment keyframes, glitch/tape motion, overlays, playback smoothness, LUT
   timing, or any other temporal behavior. HDR/LOG, privacy, and brand-sensitive
   work also require the existing explicit caveats and stronger verification.
   If the treatment is not clearly better, keep the source unchanged.
8. Report the selected media, primary intent, recipe seed if used, final
   composed controls, optional overlays, and the frames/render that were
   actually checked. Do not report visual quality from command success alone.

`media-treatment --analyze` provides deterministic clipping and signal
evidence for local composition media, not subject recognition or automatic
taste. It reports HDR/metadata caveats and a bounded primary-correction patch;
it does not invent wheels, curves, or HSL selections from statistics.


<!-- ===== FILE: hyperframes/media-use/references/memory.md ===== -->

# User memory — preferences and recipes

## Preferences — remembered defaults

The lightweight tier of user memory: confirmed brief answers (destination, aspect, language, flow, storyboard, voice, style preset) persisted on the same two-tier split as assets — project `.media/preferences.json` (committed, the team inherits it) and personal `~/.media/preferences.json`. A value earns the personal tier by being confirmed in **two different projects**, so a one-off choice never pollutes the global defaults.

```bash
node <SKILL_DIR>/scripts/prefs.mjs get --hyperframes . --json      # merged view (project overrides user)
node <SKILL_DIR>/scripts/prefs.mjs record --hyperframes . --key destination --value x-feed
node <SKILL_DIR>/scripts/prefs.mjs record --hyperframes . --key style_preset --value pin-and-paper --workflow faceless-explainer
```

Only what the user actually confirmed gets recorded — never an inferred or defaulted value. How workflows consume these (a remembered value becomes the recommended default with a receipt, and never skips a question) is the brief contract's rule: `hyperframes/references/brief-contract.md` § 2, Remembered defaults.

## Recipes — frozen video bundles

The heavyweight tier of user memory: one approved run frozen as a named, versioned bundle — `frame.md`, the storyboard skeleton (structure kept, content blanked to per-frame fill-ins), the brief skeleton (from `BRIEF.md` when the project has one — reusable frontmatter kept, run-shape and prose blanked), and the confirmed brief values. Same two tiers: project `.media/recipes/<name>/` (committed) and `~/.media/recipes/<name>/` (a freeze is already a confirmed bundle, so it promotes immediately — no two-project rule). Re-freezing a name bumps `version` and archives the old folder as `<name>@v<N>`.

```bash
node <SKILL_DIR>/scripts/recipe.mjs freeze --hyperframes . --name weekly-promo   # workflow read from BRIEF.md (--workflow only for briefless projects)
node <SKILL_DIR>/scripts/recipe.mjs list --hyperframes . --workflow product-launch-video
node <SKILL_DIR>/scripts/recipe.mjs use --hyperframes . --name weekly-promo   # also: resolve.mjs --type recipe --entity weekly-promo
```

The freeze is offered once after the final approval (`hyperframes/references/review-loop.md` § 4), and the intent layer (`/hyperframes` → `references/intent-interview.md`, step 1) checks for a match before its first question. Adopting a recipe fills the brief, the design spec, and the storyboard skeleton — and unlike preferences it may skip the questions it answers: the bundle was approved as a whole, and adoption itself is the question.

## Files

- `.media/manifest.jsonl`: machine SSOT, one JSON record per line. Records are keyed by path and only appended, so
  the last record for a path is the file's record; a file moved or replaced by hand keeps (or loses) its record by path.
- `.media/index.md`: agent-readable table (id, type, dur, dims, path, description)
- `.media/preferences.json`: the project's remembered defaults (committed)
- `~/.media/`: global cross-project reuse cache (content-addressed, SHA-256)
- `~/.media/preferences.json`: personal remembered defaults (promoted after two projects)
- `.media/recipes/<name>/`: frozen video bundles — recipe.json + frame.md + storyboard skeleton (committed)
- `~/.media/recipes/<name>/`: personal recipe tier (promoted on freeze)
- `~/.media/misses.jsonl`: local-only resolve misses, including intent text for `--stats`


<!-- ===== FILE: hyperframes/media-use/references/meta.md ===== -->

# Ownership matrix, usage stats, telemetry, privacy

Maintainer-facing reference. Nothing here changes how you resolve or operate on media.

## What it owns (the gaps HyperFrames leaves)

HyperFrames owns media _playback_; media-use owns everything else. Each row is enforced by `packages/cli/src/media-use/lib/coverage.test.mjs` so the claim can't rot.

| HyperFrames gap                            | media-use owns it via                                                                                                                                                                                                                                    |
| ------------------------------------------ | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Audio-only, no image/icon                  | `resolve --type image\|icon` (heygen asset search)                                                                                                                                                                                                       |
| No third-party brand logos                 | `resolve --type logo` (theSVG → GitHub org avatar → domain favicon)                                                                                                                                                                                      |
| No voice / audio generation                | `resolve --type voice` (HeyGen TTS free-usage path; optional local Kokoro) + the audio engine (`audio/scripts/audio.mjs`)                                                                                                                                |
| Scattered/duplicated audio engine          | one consolidated engine under `audio/` (hyperframes-media retired)                                                                                                                                                                                       |
| No agent media-ops (cut/reframe/transform) | `references/operations.md` + `resolve --from` to register outputs                                                                                                                                                                                        |
| No transcript-driven cutting               | `scripts/transcript-cut.mjs` compiles word-timestamp edits into cut lists                                                                                                                                                                                |
| No auto-duck / publish loudness            | `scripts/audio-duck.mjs` + `references/operations.md` loudnorm/sidechain recipes                                                                                                                                                                         |
| No cross-project memory                    | global content-addressed cache + auto-promote (`~/.media`)                                                                                                                                                                                               |
| Grade recipes and LUT freezing             | `resolve --type grade` emits a paste-ready recipe and `resolve --type lut` freezes validated `.cube` files; direct element analysis/authoring lives in `hyperframes media-treatment`                                                                     |
| No image generation                        | `resolve --type image` — RAM-graded local mflux (FLUX), codex `image_gen` upsell                                                                                                                                                                         |
| No video generation                        | `resolve --type video` — HeyGen avatar video first (free-usage path, sign-in nudge on auth failure), local LTX fallback (`videogen` ladder); image-to-video, photo-avatar, dub/translate remain manual `heygen` CLI recipes (`references/operations.md`) |
| Weak local-model defaults                  | HeyGen free-usage path via the `heygen` CLI; local open-source tools only as opt-in alternatives                                                                                                                                                         |

## Usage stats

Use `resolve --stats` for a local, shareable report over the current project's `.media/` manifest, the global `~/.media/` cache, and local resolve misses. Human output is compact; add `--json` for a single machine-readable object, and `--days N` to window timestamped records.

```bash
npx hyperframes media-use resolve --stats --project . --days 7
# media-use stats
# total resolves: 12
# misses: 2
# hit rate: 86%
```

## Telemetry

`resolve` and the edit tools (transcribe / transcript-cut / audio-duck) send an
anonymous usage event to PostHog (`scripts/lib/telemetry.mjs`), so we can see
which capabilities are actually used. It records only the media TYPE, the
resolution SOURCE, and the winning PROVIDER: never the intent text, file names,
or paths, and `$ip:null` so no IP is stored. Best-effort and non-blocking (a
resolve never waits on or fails from telemetry).

Opt out with `DO_NOT_TRACK=1` or `HYPERFRAMES_NO_TELEMETRY=1` (also off in CI and
dev). Same public PostHog project key and opt-outs as the `hyperframes` CLI.

HeyGen request tagging: every generating `heygen` call (TTS, avatar video, catalog
search) carries the allowlisted `X-HeyGen-Client-Source: media-use` header, sourced
from one shared constant (`HEYGEN_CLIENT_SOURCE_ARGV` in `packages/cli/src/media-use/lib/heygen-cli.mjs`)
so a future call site can't silently ship untagged. Read-only discovery calls
(`voice list`, `avatar list`) are intentionally left untagged.

## Privacy

media-use uses the same shared install id as the `hyperframes` CLI/studio
(`~/.hyperframes/config.json`). When you are signed in to HeyGen, usage is
linked to your account email, or username when email is unavailable, matching
the CLI behavior. The events stay coarse: media type, source, provider, and
small counts only; intent text and paths stay local. Disable telemetry with
`HYPERFRAMES_NO_TELEMETRY=1` or `DO_NOT_TRACK=1`.


<!-- ===== FILE: hyperframes/media-use/references/operations.md ===== -->

# Media operations: agent guidance

media-use resolves and remembers assets. For **operating** on them: cutting,
reframing, stitching, transforming, it does not wrap every action as a bespoke
command. Instead it points you at the right local tool (decision OP1). Run the
tool, then register the output with `resolve --from <output> --type <type>` so the
result lands in the ledger and the global cache like any other asset.

All tools below are local and free. ffmpeg is assumed present (it backs the
engine already).

## Cut / trim: keep a slice

```bash
ffmpeg -i in.mp4 -ss 00:00:12 -to 00:00:20 -c copy out.mp4   # 0:12–0:20, no re-encode
```

In-composition trimming usually needs **no new file**: a clip plays a sub-window
via `data-media-start` + `data-duration` (see hyperframes-core). Only cut a
physical file when exporting/assembling outside the composition.

## Reframe / crop: change aspect ratio

```bash
# 16:9 -> 9:16, crop centered
ffmpeg -i in.mp4 -vf "crop=ih*9/16:ih,scale=1080:1920" out.mp4
```

For a non-destructive crop, set a `clip-path` on the element in the composition
itself (render-time, source file untouched) instead of re-encoding with ffmpeg.

## Montage / stitch: join clips

```bash
printf "file '%s'\n" a.mp4 b.mp4 c.mp4 > list.txt
ffmpeg -f concat -safe 0 -i list.txt -c copy out.mp4
```

## Silence-cut / highlight: trim dead air, grab the best moment

```bash
auto-editor in.mp4 --edit audio:threshold=4% -o tight.mp4   # pip install auto-editor
scenedetect -i in.mp4 detect-adaptive list-scenes           # pip install scenedetect
```

## Transforms with a quality choice (process)

These have a local option AND a higher-quality HeyGen-CLI option. Run the local
one for free/offline; use the HeyGen CLI when quality matters. Showing the user
a **side-by-side** (local vs HeyGen) is the honest way to let them choose.

| Op                 | Local (free)                                       | HeyGen CLI (quality)        |
| ------------------ | -------------------------------------------------- | --------------------------- |
| Background removal | `hyperframes remove-background in.png` (u2net)     | `heygen background-removal` |
| Upscale            | `realesrgan-ncnn-vulkan -i in.png -o out.png -s 4` | n/a                         |
| Lipsync (dub)      | n/a                                                | `heygen lipsync`            |
| Translate          | n/a                                                | `heygen video-translate`    |

After any op: `resolve --from out.ext --type <type>` to register the derived
asset (it records provenance and auto-promotes to the global cache).

> ponytail: media-use doesn't re-wrap ffmpeg/heygen here, that's deliberate
> (OP1). The value it adds is the ledger + global reuse on the _output_, via
> `--from`. Add a thin `process` verb only if agents repeatedly fumble these
> recipes.

## Exact error-diffusion dither

Use the local processor when the requested look specifically calls for
Floyd-Steinberg, Atkinson/Macintosh, Jarvis-Judice-Ninke, Stucki, Burkes, or a
Sierra variant. These are sequential error-diffusion algorithms, not the
realtime Bayer `effects.dither` shader.

```bash
node <SKILL_DIR>/scripts/dither.mjs \
  --input source.mp4 \
  --out source.atkinson.mp4 \
  --algorithm atkinson \
  --palette '#0f380f,#306230,#8bac0f,#9bbc0f' \
  --point-size 3

npx hyperframes media-use resolve \
  --from source.atkinson.mp4 --type video --project .
```

Available algorithms: `floyd-steinberg`, `atkinson`,
`jarvis-judice-ninke`, `stucki`, `burkes`, `sierra`, `sierra-lite`, and
`two-row-sierra`. The default is balanced Floyd-Steinberg with a black/white
palette. Palettes contain 2-6 `#rrggbb` colors in authored dark-to-light order;
reversing the order intentionally inverts the mapping. `--point-size` controls
1-20px blocks; `--brightness` and `--contrast` accept 0.5-2; `--detail` accepts
0.1-1.

The processor supports ordinary SDR images and MP4 video, preserves video
audio, and emits BT.709 MP4. It rejects tagged PQ/HLG input rather than silently
tone-mapping it. To animate the transformation, keep the original and processed
files as two real media layers and use the seek-safe GSAP timeline to reveal or
crossfade between them. Use the realtime Bayer shader instead when the dither
amount itself must animate continuously.

## Transcription (default: Parakeet, better than whisper.cpp)

`transcribe.mjs` is the default local transcription path. It runs **NVIDIA
Parakeet-TDT via parakeet-mlx**, which beats whisper.cpp on the Open ASR
Leaderboard (avg WER ~6.05% vs 7.44%; on NOISY audio 4.73% vs 5.96%, where
whisper-large-v3 hallucinated to 308% WER on meetings) and is 5-10x faster.
It emits `{ text, words:[{text,start,end}] }` with word timestamps (merged from
Parakeet's sub-word tokens), feeding transcript-cut, captions, and the audio
engine directly.

```bash
# install once: uv venv ~/.venvs/parakeet && VIRTUAL_ENV=~/.venvs/parakeet uv pip install parakeet-mlx
node <SKILL_DIR>/scripts/transcribe.mjs --input talk.mp4 --out talk.transcribe.json

# the hyperframes CLI runs Parakeet on macOS, Linux and Windows once it is installed:
npx hyperframes models install parakeet                 # once, ~640 MB, ask the user first
npx hyperframes transcribe talk.mp4 --engine parakeet   # or --engine auto (default)
```

VERIFIED on 24GB: accurate, ~3s (cached) for 8s audio. Parakeet covers 25
European languages, English included. For other languages, or when parakeet-mlx is not
installed, transcribe.mjs falls back to `hyperframes transcribe`, which uses the
CLI's Parakeet when `models install parakeet` has run and whisper.cpp (99
languages) otherwise. `--engine parakeet|whisper` forces one. (Cohere
Transcribe tops the leaderboard on paper but its mlx-audio quants produced
garbage and ran 40-70x slower on a Mac in testing, so it is not wired in.)

## Text-based editing (transcript cut)

`transcript-cut.mjs` is a compiler, not a wrapper: it turns word timestamps and
agent cut decisions into exact kept segments. It is provided even though the rest
of this file is guidance-only.

```bash
node <SKILL_DIR>/scripts/transcript-cut.mjs \
  --input talk.mp4 \
  --transcript talk.transcribe.json \
  --remove "12.41-15.02,88.3-91.7" \
  --remove-fillers "um,uh,like" \
  --cut-silence 0.8 \
  --out talk.cut.mp4

resolve --from talk.cut.mp4 --type video
```

Use `--plan` first when you want to inspect the kept segment JSON before encoding.

## Ducking (declare in-composition / bake for export)

B1, declare ducking in the composition. `audio-duck.mjs` emits a volume lane
as a `data-automation` attribute. Add it to the background `<audio>` element;
the source file stays untouched. Lane times are clip-local, so pass
`--composition` to let the script subtract the element's `data-start`.

```bash
node <SKILL_DIR>/scripts/audio-duck.mjs \
  --meta audio_meta.json \
  --target "#bgm" \
  --composition index.html
```

```html
<!-- auto-duck: #bgm under narration; add to its <audio> element -->
data-automation='{"version":1,"lanes":[{"target":"volume","points":[{"t":0,"v":0.6},{"t":3.42,"v":0.6},{"t":3.57,"v":0.15},{"t":9.87,"v":0.15},{"t":10.27,"v":0.6}]}]}'
```

B2, bake ducking only for exported or standalone files.

```bash
ffmpeg -i bgm.mp3 -i voice.wav \
  -filter_complex "[0][1]sidechaincompress=threshold=0.03:ratio=8:attack=200:release=400[ducked]" \
  -map "[ducked]" bgm.ducked.wav
```

Declare inside compositions. Bake only for assets leaving the hyperframes
pipeline.

## Publish loudness

Two-pass `loudnorm` measures first, then applies the measured values with the
target LUFS baked in.

Socials target, -14 LUFS:

```bash
ffmpeg -i mix.wav \
  -af loudnorm=I=-14:TP=-1.5:LRA=11:print_format=json \
  -f null -

ffmpeg -i mix.wav \
  -af loudnorm=I=-14:TP=-1.5:LRA=11:measured_I=<input_i>:measured_TP=<input_tp>:measured_LRA=<input_lra>:measured_thresh=<input_thresh>:offset=<target_offset>:linear=true:print_format=summary \
  mix.social.wav
```

Podcast target, -16 LUFS:

```bash
ffmpeg -i mix.wav \
  -af loudnorm=I=-16:TP=-1.5:LRA=11:print_format=json \
  -f null -

ffmpeg -i mix.wav \
  -af loudnorm=I=-16:TP=-1.5:LRA=11:measured_I=<input_i>:measured_TP=<input_tp>:measured_LRA=<input_lra>:measured_thresh=<input_thresh>:offset=<target_offset>:linear=true:print_format=summary \
  mix.podcast.wav
```

## Generate: images (local first, cloud upsell)

`resolve --type image` retrieves from the HeyGen catalog first; on a miss it
GENERATES. Two paths, best-for-the-machine picked automatically:

1. **Local (default, free, private): mflux** (FLUX-on-MLX). `resolve` spec-checks
   AVAILABLE RAM and runs the best FLUX-class model that fits, using the
   CLI-bundled `imagegen` ladder (its modules are not shipped in the standalone
   skill). The RAM ladder:

   | Tier   | Model                | Needs (available RAM) | Notes                               |
   | ------ | -------------------- | --------------------- | ----------------------------------- |
   | medium | FLUX.1 schnell int4  | ~8GB (`--low-ram`)    | ~20s/512px on 24GB. VERIFIED. Fast. |
   | large  | FLUX.2 Klein 4B int4 | ~32GB                 | higher quality, full-resident       |
   | xlarge | Qwen-Image           | ~64GB                 | top quality, 64GB+ Macs only        |

   Gotchas baked into the table: the official FLUX repos are HF-gated, so it
   points at non-gated community 4-bit re-uploads; and `--low-ram` is MANDATORY
   at the medium tier (without it a 768x512 run swap-thrashed to 90 minutes on
   24GB; with it, 20 seconds).

2. **Cloud upsell (better quality): the `codex` CLI** `image_gen` tool, on the
   user's ChatGPT subscription (codex owns auth, no key here, no per-call
   charge). It is the automatic fallback when no local model fits AND the
   explicit "make it better" choice on any machine. Users who just want codex
   can ask for it directly. Verified: prompt -> raster -> frozen + ledgered.

`--local-only` keeps mflux (once cached) and skips codex (network).

## Generate: video (`resolve --type video`, HeyGen avatar first)

`resolve --type video "<intent>"` is the default path. It generates a
script-driven HeyGen avatar video first (the free-usage allowance — OAuth
sessions ride the web-plan free avatar-video quota where eligible, API keys
follow normal API billing), falling back to local generative LTX only when
HeyGen is unavailable, uncredentialed, or `--local-only` is passed. The two
are non-substitutable outputs (a real presenter vs. a generic generative
clip), so treat the fallback as "HeyGen wasn't reachable," not "upgrade the
quality":

- **HeyGen avatar video (default, free for new API users):**
  The CLI-bundled provider shells the
  `heygen` CLI — never the raw API — auto-picking a public avatar and a
  starfish voice (override with `--avatar-id`/`--voice-id`, threaded through
  as `ctx.avatarId`/`ctx.voiceId`). If the CLI reports `not_authenticated`,
  the provider prints an onboarding recommendation (avatar video is free for
  new API users — sign in) to stderr and falls through to LTX instead of
  hard-failing.
- **Local fallback: LTX 2.3 on MLX** via `dgrauet/ltx-2-mlx`, the `videogen`
  ladder bundled in the HyperFrames CLI. Generative clips
  (t2v), spec-gated to RAM. Verified on 24GB: 512x320 x 33f with audio.

Every generating `heygen` call from media-use — TTS, avatar video, and
catalog search — sends the allowlisted `X-HeyGen-Client-Source: media-use`
header (persistent flag, works on every subcommand) via the shared
CLI-internal `HEYGEN_CLIENT_SOURCE_ARGV` constant, so usage
tags correctly in billing/resource meta and shows up in the API dashboards.
Read-only discovery (`avatar list`, `voice list`) doesn't need it.

For structured bodies `resolve --type video` doesn't expose yet (a specific
`avatar_id`/`voice_id` combination beyond the ctx overrides, or a
pre-recorded `audio_url` instead of a script), the raw `heygen video create`
recipe below remains the escape hatch:

```bash
# discover an avatar + a starfish voice, then create + wait
heygen avatar list --ownership public --limit 5
heygen voice list --engine starfish --limit 5
heygen video create --headers "X-HeyGen-Client-Source: media-use" --wait -d '{
  "type": "avatar",
  "avatar_id": "<avatar-id>",
  "script": "Your narration here.",
  "voice_id": "<voice-id>"
}'
```

Avatar videos are deterministic + script-driven (lip-sync from a script or a
pre-recorded `audio_url`), distinct from the generative LTX clips. After a
manual recipe renders, `resolve --from <downloaded.mp4> --type video` to
ledger it (not needed when generating via `resolve --type video` directly —
that already ledgers the result).

### Image-to-video (animate any still into a talking clip)

Not wired into `resolve --type video` (deferred — the `avatar` type covers
the default script-driven case). `heygen video create` takes the raw
`POST /v3/videos` body, so switching `type`
from `avatar` to `image` animates **any image of a person** into a lip-synced
talking video, with no avatar/photo-avatar creation step first. Point `image` at a
public URL or an uploaded `asset_id`, and drive speech with a `script`+`voice_id`
or a pre-recorded `audio_url`:

```bash
heygen video create --headers "X-HeyGen-Client-Source: media-use" --wait -d '{
  "type": "image",
  "image": { "type": "url", "url": "https://example.com/person.jpg" },
  "script": "Your narration here.",
  "voice_id": "<voice-id>"
}'
```

Common optional fields: `title`, `resolution` (`4k`/`1080p`/`720p`),
`aspect_ratio`, `remove_background`, `background`, `voice_settings`,
`motion_prompt` + `expressiveness` (photo-avatar animation), and
`callback_url`/`callback_id` for webhooks. Don't hardcode these from memory: the
CLI self-documents the full, current body with
`heygen video create --request-schema` (a discriminated union keyed on `type`),
so read the schema rather than trusting a stale field list. For a still you'll
reuse across many scripts, create a reusable **Photo Avatar** once instead
(`heygen avatar create`). Ledger the result with
`resolve --from <downloaded.mp4> --type video`. Docs:
<https://developers.heygen.com/image-to-video>.

## HEVC / H.265 sources

HEVC/H.265 sources need no conversion for **render** (FFmpeg pre-decodes all
input video) or for **preview** (auto-proxy transcodes and caches an H.264
copy on first use, disable with `--no-proxy` or `media.autoProxy: false` in
hyperframes.json). A manual H.264 proxy via `ffmpeg -i in.mp4 -c:v libx264
-crf 18 proxy.mp4`, registered with `resolve --from`, remains available for
edge cases (e.g. auto-proxy disabled, or ffmpeg unavailable at preview time).


<!-- ===== FILE: hyperframes/media-use/references/resolve.md ===== -->

# Resolve — command, flags, reuse, adopt, inventory

```bash
npx hyperframes media-use resolve --type <type> --intent "<description>" --project <dir>
```

Returns one line: `resolved <id> → <path> (<type>, <metadata>)`

## Types

| Type    | What it finds                    | Provider / cascade                                           |
| ------- | -------------------------------- | ------------------------------------------------------------ |
| `bgm`   | Background music                 | HeyGen audio catalog (10k+ tracks)                           |
| `sfx`   | Sound effects                    | Bundled 19-file library + HeyGen catalog                     |
| `image` | Photos, backgrounds              | HeyGen asset search (75k+ vectors)                           |
| `icon`  | Icons, symbols                   | HeyGen asset search (type=icon)                              |
| `logo`  | Official brand marks             | theSVG → GitHub org avatar → domain favicon                  |
| `voice` | TTS voiceover                    | HeyGen TTS free-usage path; optional local Kokoro            |
| `grade` | HyperFrames color-grading blocks | Core preset → look index params/CDN LUT → deterministic cube |
| `lut`   | Reusable `.cube` LUT files       | Look index params/CDN LUT → deterministic cube               |

## Examples

```bash
# Background music
npx hyperframes media-use resolve --type bgm --intent "upbeat tech launch" --project .
# → resolved bgm_001 → .media/audio/bgm/bgm_001.mp3 (bgm, 25s)

# Sound effect
npx hyperframes media-use resolve --type sfx --intent "whoosh" --project .
# → resolved sfx_001 → .media/audio/sfx/sfx_001.mp3 (sfx, 0.57s)

# Image
npx hyperframes media-use resolve --type image --intent "gradient tech background" --project .
# → resolved image_001 → .media/images/image_001.jpg (image)

# Icon
npx hyperframes media-use resolve --type icon --intent "rocket" --project .
# → resolved icon_001 → .media/images/icon_001.png (icon, transparent)

# Brand logo (official mark — never redrawn by hand)
npx hyperframes media-use resolve --type logo --entity linkedin --intent "LinkedIn logo" --project .
# → resolved logo_001 → .media/images/logo_001.svg (logo, official mark)

# Color grade block
npx hyperframes media-use resolve --type grade --intent "warm daylight" --project . --json
# → {"ok":true,"preset":"warm-daylight","grading":{"preset":"warm-daylight","intensity":1},...}

# LUT file
npx hyperframes media-use resolve --type lut --intent "teal orange blockbuster" --project .
# → resolved lut_001 → .media/luts/lut_001.cube (lut)
```

## Flags

| Flag            | Description                                                                          |
| --------------- | ------------------------------------------------------------------------------------ |
| `--type, -t`    | Media type: bgm, sfx, image, icon, logo, voice, grade, lut                           |
| `--intent, -i`  | What you need (natural language)                                                     |
| `--entity, -e`  | Entity name for cache matching (optional)                                            |
| `--project, -p` | Project directory (default: .)                                                       |
| `--candidates`  | List reusable assets (project + global cache) for `--type`; no download, no mutation |
| `--reuse <sha>` | Import a specific global-cache asset (by content sha/prefix, from `--candidates`)    |
| `--from`        | Freeze a local file or direct public URL (ingest)                                    |
| `--for`         | Analyze a local image/video and add measured adjust suggestions (`grade` only)       |
| `--local-only`  | Offline: skip every network provider (cache + local only)                            |
| `--provider`    | Force one generator (e.g. `codex`, `mflux`, `kokoro`, `heygen`)                      |
| `--adopt`       | Bulk-import existing assets/ into manifest                                           |
| `--doctor`      | Check local CLI dependencies; no manifest changes                                    |
| `--stats`       | Print local usage stats from `.media/` and `~/.media`; no manifest changes           |
| `--days N`      | Limit `--stats` to timestamped records/misses from the last N days                   |
| `--json`        | Output JSON instead of one-line result                                               |

## Reuse before you resolve

Before resolving bgm/sfx/image/icon/logo/grade/lut, **check what already exists and reuse it when it fits.** media-use does not semantically match for you — you are the judge. It surfaces candidates; you decide.

```bash
npx hyperframes media-use resolve --type bgm --intent "upbeat tech launch" --candidates --project .
#   [project] upbeat tech launch (25s, heygen.audio.sounds)
#           .media/audio/bgm/bgm_001.wav
#   [global]  energetic tech intro (22s, heygen.audio.sounds)
#           --reuse 06e052c075fd2b80
```

Read the list and judge semantic fit yourself — "upbeat tech launch" ≈ "energetic tech intro" is a call only you can make from the descriptions. Then:

- **A project candidate fits** → just reference its path in your composition. Nothing else to run.
- **A global candidate fits** → `resolve --type bgm --reuse <sha>` copies it into this project (self-contained render) and records it.
- **Nothing fits** → resolve fresh (`--type ... --intent ...`).

**Trust guardrail — when unsure, resolve fresh.** A redundant download is cheap; shipping the wrong asset is not. Judge fit from description + prompt + type + duration/dims. For **brand/entity** assets, reuse a _global_ candidate only when the entity matches exactly — the global cache aggregates every project you have worked on, so a `--candidates` list can surface another client's brand mark and its prompt text. Never reuse a cross-project brand asset on a loose match.

The deterministic floor still runs automatically: an identical (case/whitespace-insensitive) repeat auto-reuses with no `--candidates` step. `--candidates` is only for the semantic layer above that floor — and a fuzzy match is **never** auto-applied; reuse is always your explicit call. On a resolve that misses the floor and is about to fetch, media-use prints a one-line stderr hint when similar cached assets exist, pointing you back here.

## How it works

`resolve` runs an automatic floor, then falls through to fetching:

1. Check project `.media/manifest.jsonl` for a prompt match (case- and whitespace-insensitive) — auto-reuse
2. Scan existing `assets/` directory for unregistered files that share a word with the need
3. Check global cache `~/.media/` for a reusable asset matched on the same normalized prompt — auto-reuse
4. Search via provider (HeyGen audio catalog, HeyGen asset search), or resolve color locally
5. Freeze file to `.media/<type>/`, register in manifest, regenerate `index.md`, auto-promote to `~/.media/`

Steps 1 and 3 are the **deterministic floor**: they only auto-reuse an exact-normalized match, never a fuzzy one. Semantic reuse ("close enough") is the agent's explicit call via [Reuse before you resolve](#reuse-before-you-resolve) — it never happens automatically. The agent gets back **one line**; candidates, scores, provenance stay on disk.

## Stamping provenance when mounting a resolved video

`resolve` never writes composition HTML itself — mounting a `<video>` element
into a composition is always the agent's own edit. When the mounted video's
manifest record has `provenance.provider === "heygen.video"` (check
`.media/manifest.jsonl` or the one-line resolve output for the provider name),
add `data-media-source="heygen"` to that `<video>` tag. Leave the attribute off
entirely for every other provider (`ltx.local`, an adopted/local file, etc.) —
this is not a general provider taxonomy, just the one signal render telemetry
tracks today.

## Adopt existing projects

Most HyperFrames projects already have assets in `assets/`. media-use adopts them:

```bash
npx hyperframes media-use resolve --adopt --project .
# → adopted 9 assets from assets/
#   bgm_001 → assets/bgm/mango-fizz.mp3 (bgm, 146.6s)
#   image_001 → assets/images/avatar.jpg (image, 400×400)
```

`ffprobe` extracts real duration and dimensions. During resolve, unregistered files in `assets/` matching the intent are adopted on the fly.

## Reading the inventory

After resolve or adopt, read `.media/index.md` for the full inventory:

```
# .media · 4 assets

id         type   dur   dims       path                          description
bgm_001    bgm    25s   -          .media/audio/bgm/bgm_001.mp3  upbeat tech launch
sfx_001    sfx    0.6s  -          .media/audio/sfx/sfx_001.mp3  whoosh
image_001  image  -     1920×1080  .media/images/image_001.jpg   gradient tech background
icon_001   icon   -     200×200    .media/images/icon_001.png    rocket
```

## Cross-project reuse

Assets are cached automatically on resolve. Every resolved/ingested asset is auto-promoted to the global cache at `~/.media/`, so subsequent resolves for the same (or near-identical) prompt, in any project, hit the cache with no re-download and no provider call.

For a _semantically_ similar (not identical) need in another project, the exact-match floor won't fire — use [Reuse before you resolve](#reuse-before-you-resolve): `--candidates` lists the global assets, and `--reuse <sha>` imports the one you pick. This is how a track resolved in one project gets reused in the next when the wording differs.
