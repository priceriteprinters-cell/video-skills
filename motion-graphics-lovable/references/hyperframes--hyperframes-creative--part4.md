

<!-- ===== FILE: hyperframes/hyperframes-creative/references/beat-direction.md ===== -->

# Beat Direction

How to plan and direct individual scenes (beats) in a multi-scene composition. Read before writing any multi-scene video.

## Contents

- Per-beat direction
- Concept
- Mood direction
- Animation choreography
- Transition
- Depth layers
- SFX cues
- Rhythm planning
- Velocity-matched transitions

---

## Per-Beat Direction

Each beat is a WORLD, not a layout. Before writing CSS specs and GSAP instructions, describe what the viewer EXPERIENCES. The difference between a great storyboard and a mediocre one:

**Mediocre:** "Dark navy background. '$1.9T' in white, 280px. Logo top-left. Wave image bottom-right."
**Great:** "Camera is already mid-flight over a vast dark canvas. The gradient wave sweeps across the frame like aurora borealis — alive, shifting. '$1.9T' SLAMS into existence with such force the wave ripples in response. This isn't a slide — it's a moment."

The first describes pixels. The second describes an experience. Write the second, then figure out the pixels.

Each beat should have:

### Concept

The big idea for this beat in 2-3 sentences. What visual WORLD are we in? What metaphor drives it? What should the viewer FEEL? This is the most important part — everything else flows from it.

### Mood direction

Cultural and design references, not hex codes:

- "Geometric, rhythmic, precise. Think Josef Albers or Bauhaus color studies."
- "Warm workspace. Nice notebook energy, not technical blueprint."
- "Cinematic title sequence. The kind of opening where you lean forward."

### Animation choreography

Specific motion verbs per element — not "it animates in" but HOW. Verbs come from the beat's concept and content, not from an energy bucket. A wellness brand's "slow" beat might still have something that DROPS if the content is about letting go. A stats beat might FLOAT if the brand's identity is weightless.

The vocabulary of motion verbs (organized by physical character, not by energy level):

**Impact / weight:** SLAMS, CRASHES, PUNCHES, STAMPS, SHATTERS, DROPS (with force)
**Directional / deliberate:** SLIDES, PUSHES, PULLS, WIPES, CUTS
**Reveals / builds:** DRAWS, FILLS, GROWS, EXPANDS, ASSEMBLES, COUNTS UP
**Organic / ambient:** FLOATS, DRIFTS, BREATHES, PULSES, ORBITS, MORPHS
**Mechanical / precise:** TYPES ON, CLICKS, LOCKS IN, SNAPS, STEPS

Every element gets a verb. If you can't name the verb, the element is not yet designed. The verb should follow from the beat's concept — not from a lookup of what "high energy" or "low energy" beats use.

For text elements specifically, you can name a deterministic, named effect by ID (e.g. `typewriter`, `kinetic-center-build`, `soft-blur-in`) instead of inventing timing from scratch — the 24-effect vocabulary and how to load it live in `skills/hyperframes-animation/adapters/animate-text.md`.

### Transition

How this beat hands off to the next. Specify the type and parameters.

**When to pick which:**

| Choose shader transition for                                                    | Choose CSS transition for                                                           | Choose hard cut for                                            |
| ------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------- | -------------------------------------------------------------- |
| Reveals, big reaction shots, product/logo unveils, energy shifts, "wow" moments | Continuous camera-motion beats where the scene feels like one move broken into cuts | Rapid-fire lists, percussive edits on the beat, comedic timing |
| Any moment the music/VO punctuates with a downbeat or SFX hit                   | Beats that ease from one composition into the next with shared motion vocabulary    | Sequences of 3+ quick tempo-matched switches                   |
| Brand moments where the transition itself _is_ the visual                       | Minimal/editorial pacing                                                            | Anytime a 0.3-0.8s transition would feel too slow              |

Rule of thumb: if the beat is the _centerpiece_ of the video, shader-transition into it. If the beat is connective tissue, a CSS crossfade is fine. A brand reel of 5-7 beats usually wants 1-2 shader transitions (the hero reveal + the CTA) — too many flatten their impact.

**Mixing shader and CSS crossfade transitions in one composition is supported.** Omit `shader` on any transition entry to get a smooth opacity crossfade — HyperShader manages all scene visibility regardless. Let HyperShader create the timeline (don't pass a pre-built `timeline:` option) and add all composition tweens to the returned `tl` after `init()`. Config snippet in `skills/hyperframes-animation/transitions/overview.md` → "CSS vs Shader".

**CSS transitions** — 30+ patterns across 13 categories. Full code in `skills/hyperframes-animation/transitions/` (route via `catalog.md`). Pick based on the energy and feel:

| Category           | Patterns                                                                 | Motion character                                                           |
| ------------------ | ------------------------------------------------------------------------ | -------------------------------------------------------------------------- |
| **Push / slide**   | Push slide, vertical push, elastic push, squeeze                         | Content moves through the frame as if on a continuous surface              |
| **Scale / zoom**   | Zoom through, zoom out                                                   | Perspective shifts — moving toward or away from content                    |
| **Radial / clip**  | Circle iris, diamond iris, diagonal split                                | Geometric reveal — content emerges or is covered by a shape                |
| **3D**             | 3D card flip                                                             | Physical — content flips like a tangible object                            |
| **Dissolve**       | Crossfade, blur crossfade, focus pull, color dip                         | Overlap and blend — both scenes exist simultaneously during the transition |
| **Cover / blinds** | Staggered color blocks, horizontal blinds (6/12 strips), vertical blinds | Structural — content is sliced, layered, or covered                        |
| **Light**          | Light leak overlays, overexposure burn, film burn                        | Organic film — light bleeds across the frame                               |
| **Distortion**     | Glitch (CSS RGB jitter), chromatic aberration, ripple, VHS tape          | Instability — the image itself appears to malfunction                      |
| **Blur**           | Blur through, directional blur                                           | Soft defocus — content blurs in or out                                     |
| **Mechanical**     | Shutter (two-half), clock wipe (9-point wedge)                           | Precision — transitions with visible mechanical logic                      |
| **Grid**           | Grid dissolve (12/120 cells)                                             | Fragmentation — the frame breaks into pieces                               |
| **Destruction**    | Page burn (SVG clip-path + canvas rim)                                   | Dramatic decay — the previous scene is destroyed                           |
| **Other**          | Gravity drop, morph circle                                               | Physical or shape-based motion that doesn't fit other categories           |

Common quick-picks:

- **Velocity-matched upward**: exit `y:-150, blur:30px, 0.33s power2.in` → entry `y:150→0, blur:30px→0, 1.0s power2.out`
- **Whip pan**: exit `x:-400, blur:24px, 0.3s power3.in` → entry `x:400→0, blur:24px→0, 0.3s power3.out`
- **Blur through**: exit `blur:20px, 0.3s` → entry `blur:20px→0, 0.25s power3.out`
- **Zoom through**: exit `scale:1→1.2, blur:20px, 0.2s power3.in` → entry `scale:0.75→1, blur:20px→0, 0.5s expo.out`
- **Hard cut / smash cut**: instant, for rapid-fire sequences

Timing presets: snappy (0.2s), smooth (0.4s), gentle (0.6s), dramatic (0.5s), instant (0.15s), luxe (0.7s).

**Shader transitions** — 14 built-in WebGL GPU effects. Install with `npx hyperframes add <name>` (block name ≠ shader name — see `skills/hyperframes-registry/references/discovery.md`); full API in `packages/shader-transitions/README.md`.

| Shader                  | Visual description                                                                             | Duration range |
| ----------------------- | ---------------------------------------------------------------------------------------------- | -------------- |
| **domain-warp**         | Organic FBM dissolve — both scenes warp toward each other with an accent flash at the midpoint | 0.5–0.8s       |
| **ridged-burn**         | Multifractal mask reveals the incoming scene through a burn ramp with sparks at the edge       | 0.5–0.8s       |
| **whip-pan**            | 10-sample horizontal motion blur + lateral crossfade — reads like a camera pan between shots   | 0.3–0.5s       |
| **sdf-iris**            | Circle SDF expands from center, with accent-tinted glow rings at the expanding edge            | 0.5–0.7s       |
| **ripple-waves**        | Radial standing-wave UV displacement — content ripples outward as scenes cross                 | 0.6–1.0s       |
| **gravitational-lens**  | Pinch pull toward center + R/B chromatic separation — content bends inward then releases       | 0.6–1.0s       |
| **cinematic-zoom**      | 12 RGB-offset radial zoom blur samples — motion streak radiating from center                   | 0.4–0.6s       |
| **chromatic-split**     | R/B radial channel shift outward, G fixed — channels separate then rejoin                      | 0.3–0.5s       |
| **swirl-vortex**        | CCW swirl with FBM noise — content spirals away and the new scene spirals in                   | 0.5–0.8s       |
| **thermal-distortion**  | Vertical sine + FBM horizontal displacement — heat-haze shimmer across the frame               | 0.5–0.8s       |
| **flash-through-white** | Fade through white midpoint — almost invisible at 0.01s, noticeable at 0.3s                    | 0.01s–0.3s     |
| **cross-warp-morph**    | FBM vector field displaces both scenes; a third FBM biases the wipe direction                  | 0.5–0.8s       |
| **light-leak**          | Fixed off-frame light source with exponential falloff, warmth, and a ridge flare               | 0.5–0.8s       |
| **glitch**              | Line displacement + RGB lateral split + scan modulation + posterization + flicker              | 0.3–0.5s       |

**You are not limited to what's listed here.** These are the built-in options, but you can and should:

- **Write custom GLSL shaders** from scratch for unique transition effects
- **Search online** for shader code (ShaderToy, GLSL Sandbox, GitHub) and adapt it
- **Build custom CSS transitions** that aren't in any category — combine clip-path, transforms, filters in new ways
- **Ask the user** to provide or find specific effects if you need something specialized

If the storyboard calls for an effect that doesn't exist yet — build it. The framework renders anything a browser can run.

### Depth layers

What's in foreground, midground, and background. Every beat should have at least 2 layers:

- "BG: dark navy fill + subtle radial glow. MG: stat cards with drop shadow. FG: brand logo bottom-right."

### SFX cues

What sounds at what moment:

- "On the capture pulse — a soft, warm analog shutter click."
- "Left side carries a faint low drone. On fold: drone cuts. Silence. Then a single clean chime."

---

## Rhythm Planning

Before writing HTML, declare your scene rhythm: which scenes are quick hits, which are holds, where do shaders land, where does energy peak. Name the pattern — fast-fast-SLOW-fast-SHADER-hold — before implementing.

**Derive the rhythm from the storyboard and the brand, not from a lookup.** A 15-second social ad for an architectural firm and a 15-second social ad for a gaming brand have different rhythms — both are 15 seconds, but one is slow-reveal-hold-CTA and the other is rapid-fire-SLAM-hook. Video type sets constraints (duration, approximate beat count); the brand and content determine whether those beats are slow or fast, sparse or dense, dramatic or controlled.

Questions that drive rhythm decisions:

- What emotional journey should the viewer take? Where is the peak moment?
- Where does the narration land its heaviest emphasis? That's usually where energy should peak.
- What does the brand's own visual pacing suggest — unhurried or urgent?
- How many beats can the duration actually support without feeling rushed or padded?

A social ad that tries to hook in 2s, showcase 3 features, and end with a CTA in 15s will feel like noise. Sometimes "hook-hold-CTA" with one strong feature is the right rhythm for 15 seconds. Name the rhythm you've planned before implementing.

---

## Velocity-Matched Transitions

Exit the outgoing beat with an accelerating ease (power2.in or power3.in) plus a blur ramp. Enter the incoming beat with a decelerating ease (power2.out or power3.out) plus blur clear. The fastest point of both easing curves meets at the cut — the viewer perceives continuous camera motion, not two discrete animations. Match exit velocity to entry velocity within ~5% tolerance.


<!-- ===== FILE: hyperframes/hyperframes-creative/references/composition-patterns.md ===== -->

# Composition Patterns

## Contents

- Picture-in-picture
- Text behind subject
- Title card with fade
- Slide show with section headers
- Top-level composition example

## Picture-in-Picture (Video in a Frame)

Animate a wrapper div for position/size. The video fills the wrapper. The wrapper has NO data attributes.

```html
<div
  id="pip-frame"
  style="position:absolute;top:0;left:0;width:1920px;height:1080px;z-index:50;overflow:hidden;"
>
  <video
    id="el-video"
    data-start="0"
    data-duration="60"
    data-track-index="0"
    src="talking-head.mp4"
    data-has-audio="true"
    playsinline
  ></video>
</div>
```

```js
tl.to(
  "#pip-frame",
  { top: 700, left: 1360, width: 500, height: 280, borderRadius: 16, duration: 1 },
  10,
);
tl.to("#pip-frame", { left: 40, duration: 0.6 }, 30);
```

## Text Behind Subject (transparent webm overlay)

Put a headline _behind_ a presenter so their silhouette occludes the text. Requires a transparent cutout produced by `npx hyperframes remove-background presenter.mp4 -o presenter.webm`.

Three layers, plus one critical rule:

```html
<!-- z=1 base — full opaque mp4 (lobby + presenter), always visible -->
<video
  id="cf-base"
  data-start="0"
  data-duration="6"
  data-media-start="0"
  data-track-index="0"
  src="presenter.mp4"
  data-has-audio="true"
  playsinline
></video>

<!-- z=2 headline — visible the whole time -->
<h1
  id="cf-headline"
  style="position:absolute;top:50%;left:50%;
     transform:translate(-50%,-50%); z-index:2; font-size:220px; font-weight:900;
     color:#fff; text-shadow:0 6px 32px rgba(0,0,0,.55); clip-path:inset(0 0 100% 0);"
>
  MAKE IT IN HYPERFRAMES
</h1>

<!-- z=3 cutout — same source, alpha around presenter, hidden until the cut -->
<!-- WRAPPER has the opacity, NOT the video itself (see rule below). -->
<div class="cutout-wrap" style="position:absolute;inset:0;z-index:3;opacity:0">
  <video
    id="cf-cutout"
    data-start="0"
    data-duration="6"
    data-media-start="0"
    data-track-index="1"
    src="presenter.webm"
    muted
    playsinline
  ></video>
</div>
```

```js
const tl = gsap.timeline({ paused: true });
const CUT = 3.3;

// Reveal headline early
tl.to("#cf-headline", { clipPath: "inset(0 0 0% 0)", duration: 0.6, ease: "expo.out" }, 0.25);

// At the cut, flip the cutout wrapper visible — the presenter's silhouette
// punches through the headline.
tl.set(".cutout-wrap", { opacity: 1 }, CUT);

// Sentinel: extend timeline to the composition's full duration so the
// renderer doesn't bail past the last meaningful tween.
tl.set({}, {}, 6);

window.__timelines["cover-flip"] = tl;
```

**Why a wrapper div, not opacity on the video itself?**

The framework forces `opacity: 1` on any element with `data-start`/`data-duration` while it's "active" — that's how it manages clip lifecycles. A CSS `opacity: 0` on the video element is silently overwritten. Wrap the video in a div with no `data-*` attributes; the wrapper is owned by your CSS/GSAP.

**Why both videos at `data-start="0"`?**

So both decode in sync from t=0. Late-mounting the cutout (`data-start=3.3`) makes Chrome do a seek + decoder warm-up at mount, which can land a frame off the base mp4 — visible as a one-frame jitter at the cut.

**Color match:** `remove-background` defaults to `--quality balanced` (crf 18) which keeps the cutout's RGB nearly identical to the source mp4 — minimal edge halo or color shift when overlaid. Use `--quality best` (crf 12) for hero shots; only drop to `--quality fast` (crf 30) when the cutout sits over a _different_ background and the size matters.

## Title Card with Fade

```html
<div
  id="title-card"
  data-start="0"
  data-duration="5"
  data-track-index="5"
  style="display:flex;align-items:center;justify-content:center;background:#111;z-index:60;"
>
  <h1 style="font-size:64px;color:#fff;opacity:0;">My Video Title</h1>
</div>
```

```js
tl.to("#title-card h1", { opacity: 1, duration: 0.6 }, 0.3);
tl.to("#title-card", { opacity: 0, duration: 0.5 }, 4);
```

## Slide Show with Section Headers

Use separate elements on the same track, each with its own time range. Slides auto-mount/unmount based on `data-start`/`data-duration`.

```html
<div class="slide" data-start="0" data-duration="30" data-track-index="3">...</div>
<div class="slide" data-start="30" data-duration="25" data-track-index="3">...</div>
<div class="slide" data-start="55" data-duration="20" data-track-index="3">...</div>
```

## Top-Level Composition Example

```html
<div
  id="comp-1"
  data-composition-id="my-video"
  data-start="0"
  data-duration="60"
  data-width="1920"
  data-height="1080"
>
  <!-- Primitive clips -->
  <video
    id="el-1"
    data-start="0"
    data-duration="10"
    data-track-index="0"
    src="..."
    muted
    playsinline
  ></video>
  <video
    id="el-2"
    data-start="el-1"
    data-duration="8"
    data-track-index="0"
    src="..."
    muted
    playsinline
  ></video>
  <img id="el-3" data-start="5" data-duration="4" data-track-index="1" src="..." />
  <audio id="el-4" data-start="0" data-duration="30" data-track-index="2" src="..." />

  <!-- Sub-compositions loaded from files -->
  <div
    id="el-5"
    data-composition-id="intro-anim"
    data-composition-src="compositions/intro-anim.html"
    data-start="0"
    data-track-index="3"
  ></div>

  <div
    id="el-6"
    data-composition-id="captions"
    data-composition-src="compositions/caption-overlay.html"
    data-start="0"
    data-track-index="4"
  ></div>

  <script>
    // Just register the timeline — framework auto-nests sub-compositions
    const tl = gsap.timeline({ paused: true });
    window.__timelines["my-video"] = tl;
  </script>
</div>
```


<!-- ===== FILE: hyperframes/hyperframes-creative/references/data-in-motion.md ===== -->

# Data in Motion

Light guidance for data and stats in video compositions. `house-style.md` handles aesthetics; this just addresses data-specific pitfalls.

## Visual Continuity

When successive stats belong to the same concept (Q1 → Q2 → Q3 → Q4, or three metrics for the same product), keep them in the same visual space with the same aesthetic. Only the VALUE changes. An aesthetic change should signal a new concept, not just a new number.

## Numbers Need Visual Weight

A number on its own floats in empty space. Pair every metric with a visual element that gives it presence — a proportional fill bar, a background color shift, a shape that represents the value, a progress ring. The visual doesn't need to be a chart — it just needs to fill the frame and make the data feel tangible rather than just text on a background.

## Avoid Web Patterns

- **No pie charts** — hard to compare, looks like PowerPoint
- **No multi-axis charts** — viewer can't study intersections in a 3-second window
- **No 6-panel dashboards** — 2-3 related metrics side-by-side is fine, 6+ is a web pattern
- **No gridlines, tick marks, or legends** — visual noise that adds nothing in motion
- **No chart library output** — build with GSAP + SVG/CSS, not D3 or Chart.js


<!-- ===== FILE: hyperframes/hyperframes-creative/references/design-adherence.md ===== -->

# Design Adherence

Post-authoring verification that the composition follows the design spec. Run it after building, before serving the preview.

If a design spec (`frame.md` / `design.md`) exists, read the HTML and check:

1. **Colors** — every hex value in the composition appears in the spec's palette section (however the user labeled it: Colors, Palette, Theme, etc.). Flag any invented colors.
2. **Typography** — font families and weights match the spec's type spec. No substitutions.
3. **Corners** — border-radius values match the declared corner style, if specified.
4. **Spacing** — padding and gap values fall within the declared density range, if specified.
5. **Depth** — shadow usage matches the declared depth level, if specified (flat = none, subtle = light, layered = glows).
6. **Avoidance rules** — if the spec has a section listing things to avoid (commonly "What NOT to Do", "Don'ts", "Anti-patterns", or "Do's and Don'ts"), verify none are present.

Report violations as a checklist. Fix each one before serving.

If no design spec exists (house-style-only path), verify:

1. **Palette consistency** — the same bg, fg, and accent colors are used across all scenes. No per-scene color invention.
2. **No lazy defaults** — check the composition against `house-style.md`'s "Lazy Defaults to Question" list. If any appear, they must be a deliberate choice for the content, not a default.


<!-- ===== FILE: hyperframes/hyperframes-creative/references/design-picker.md ===== -->

# Design Picker

Two-phase visual picker: mood boards first (pick a complete direction), then fine-tune individual categories.

## Contents

- Prerequisites
- Building the picker
- Serving and user selection

## Prerequisites

Read these before generating options — they define the rules your options must follow:

- `references/typography.md`
- `house-style.md`
- `references/video-composition.md`
- `visual-styles.md`
- `references/beat-direction.md`

## Building the picker

1. Generate options **deeply contextual to the user's prompt**. Every category — not just architectures — must reflect the specific product, brand, audience, and mood. Generic options that could appear on any picker are a failure.

   **Mood boards** — as many as the creative space warrants (4-8). Every board must tell a different STORY about the brand, not just reshuffle the same elements. Ask: "what are the genuinely different ways to position this product?" A cat food brand might be: playful chaos, premium positioning, comfort/cozy, social-native, flavor showcase, humor-led, sensory/appetizing. Each is a different narrative, not a different font on the same layout.

   **Architectures** — one per mood board minimum, each visually distinct. Use `{{prompt_headline}}` and `{{prompt_sub}}` tokens. If the user provided media assets, use them as background images (use `url(path)` without quotes — single quotes inside `style='...'` break the attribute).

   **Palettes** (5-6) — named after the brand's world, not generic moods. The palette names and colors should feel like they belong to THIS specific product. Always mix dark + light + tinted. **Every palette must be visually distinct at swatch size.** If two palettes share the same background lightness AND a similar accent hue, cut one. Test: would a user see the difference in a 14px swatch chip? If not, they're duplicates.

   **Type pairings** (5-6) — **RUN the font discovery script from typography.md BEFORE generating pairings.** This is not optional. Download Google Fonts metadata, run the script, and pick from its output. You will otherwise reach for the same 8 fonts every time (Bricolage Grotesque, Instrument Serif, Fraunces, Archivo Black, DM Serif Display, Space Grotesk, Fredoka) — that's your training data default, not a contextual choice. Match the brand's energy and audience. Cross-category per typography.md (never two sans-serifs).

2. `mkdir -p .hyperframes` then copy [../templates/design-picker.html](../templates/design-picker.html) to `.hyperframes/pick-design.html`.
3. Replace these placeholders using Python (don't hand-escape quotes in sed):
   - `__ARCHITECTURES_JSON__` — array of architecture objects
   - `__PALETTES_JSON__` — array of palette objects
   - `__TYPEPAIRS_JSON__` — array of type pairing objects
   - `__MOODBOARDS_JSON__` — array of mood board objects (see format below)
   - `__PROMPT_JSON__` — object with prompt context (see format below)

### Architecture data format

Each architecture object must include a `preview_html` field — the HTML that renders in the preview panel. Use token placeholders that the template replaces at runtime: `{{bg}}`, `{{fg}}`, `{{ac}}`, `{{mt}}`, `{{hf}}`, `{{hw}}`, `{{bf}}`, `{{bw}}`, `{{cr}}` (corner radius), `{{pad}}`, `{{gap}}`, `{{shadow}}`, `{{g}}` (grid line color), `{{fg3}}`/`{{fg6}}`/`{{fg8}}`/`{{fg15}}` (fg at opacity), `{{ac3}}`/`{{ac5}}`/`{{ac25}}` (accent at opacity).

**Every token must be used.** Apply `{{cr}}` to all cards, buttons, and containers. Apply `{{shadow}}` to elevated elements (cards, buttons, code blocks). Apply `{{pad}}` and `{{gap}}` to control spacing. If a token isn't used in the preview_html, that option will have no visible effect.

**Density matters.** Each architecture preview must include 15+ distinct elements to give the user a real sense of the layout. Include: headline, subhead, body paragraph, label/overline, stat with number, secondary stat, quote/testimonial, attribution, card with title+body, second card (different treatment), code/command block, primary button, secondary button, list or tags, accent divider/rule, and a data element (table row, progress bar, or chart).

Optionally include `components` (component styling rules) and `dos` (do's and don'ts) as strings — these appear in the generated design.md.

**Layout constraint:** All preview HTML must use percentage widths or `max-width: 100%`. Use `flex-wrap: wrap` on all flex rows. Absolute-positioned decoratives must stay within a parent with `overflow: hidden`.

**Security:** Architecture `preview_html` must not contain `<script>` tags, event handlers (`onclick`, `onerror`, etc.), or `javascript:` URLs. It is injected via `innerHTML`.

**Image URLs:** When using background images in `preview_html`, use `url(path/to/image.jpg)` WITHOUT quotes around the path. Single quotes like `url('path.jpg')` break because `preview_html` is inside a `style='...'` attribute — the inner single quotes terminate the outer attribute.

**Palette variety:** Always include a mix of light, dark, and tinted backgrounds across the 6 palettes — even for calm/wellness prompts.

### Example architecture object

```json
{
  "name": "Editorial Stack",
  "description": "Vertical rhythm with large type, pull quotes, and data callouts",
  "tag": "editorial / longform / narrative",
  "mood": "Confident, unhurried, typographically driven",
  "preview_html": "<div style='background:{{bg}};color:{{fg}};padding:{{pad}};min-height:100vh;font-family:\"{{bf}}\",sans-serif;font-weight:{{bw}};'><div style='max-width:100%;display:flex;flex-direction:column;gap:{{gap}};'><div style='font-size:10px;text-transform:uppercase;letter-spacing:0.12em;color:{{mt}};'>Overline Label</div><div style='font-family:\"{{hf}}\",serif;font-weight:{{hw}};font-size:48px;line-height:1.1;letter-spacing:-0.02em;'>The Headline Goes Here</div><div style='font-size:20px;color:{{mt}};max-width:70%;line-height:1.5;'>Subheading text that introduces the narrative arc of this composition with enough words to fill two lines.</div><div style='font-size:15px;line-height:1.7;color:{{fg}};max-width:65%;'>Body paragraph with real sentences. The quick brown fox jumps over the lazy dog. This gives a sense of text density and reading rhythm at the chosen type size.</div><div style='display:flex;gap:{{gap}};flex-wrap:wrap;'><div style='background:{{fg6}};border-radius:{{cr}};padding:{{pad}};flex:1;min-width:200px;box-shadow:{{shadow}};'><div style='font-size:36px;font-family:\"{{hf}}\",serif;font-weight:{{hw}};color:{{ac}};'>2.4M</div><div style='font-size:12px;color:{{mt}};margin-top:4px;'>Primary Stat</div></div><div style='background:{{fg6}};border-radius:{{cr}};padding:{{pad}};flex:1;min-width:200px;box-shadow:{{shadow}};'><div style='font-size:36px;font-family:\"{{hf}}\",serif;font-weight:{{hw}};color:{{fg}};'>87%</div><div style='font-size:12px;color:{{mt}};margin-top:4px;'>Secondary Stat</div></div></div><div style='border-left:3px solid {{ac}};padding:12px {{pad}};background:{{ac3}};border-radius:0 {{cr}} {{cr}} 0;'><div style='font-size:18px;font-style:italic;color:{{fg}};line-height:1.5;'>\"A pull quote that captures the key insight of the piece.\"</div><div style='font-size:12px;color:{{mt}};margin-top:8px;'>— Attribution Name</div></div><div style='background:{{fg3}};border-radius:{{cr}};padding:{{pad}};box-shadow:{{shadow}};'><div style='font-size:14px;font-weight:{{hw}};margin-bottom:8px;'>Card Title</div><div style='font-size:13px;color:{{mt}};line-height:1.5;'>Card body text with a different treatment than the main content area.</div></div><div style='background:{{ac5}};border:1px solid {{ac25}};border-radius:{{cr}};padding:{{pad}};box-shadow:{{shadow}};'><div style='font-size:14px;font-weight:{{hw}};color:{{ac}};margin-bottom:8px;'>Accent Card</div><div style='font-size:13px;color:{{fg}};line-height:1.5;'>Second card with a tinted accent treatment for variety.</div></div><div style='font-family:monospace;font-size:13px;background:{{fg8}};border-radius:{{cr}};padding:{{pad}};color:{{fg15}};box-shadow:{{shadow}};'>$ hyperframes render --output video.mp4</div><div style='display:flex;gap:12px;flex-wrap:wrap;'><button style='background:{{ac}};color:{{bg}};border:none;padding:10px 24px;border-radius:{{cr}};font-size:14px;font-weight:600;box-shadow:{{shadow}};cursor:pointer;'>Primary Action</button><button style='background:transparent;color:{{fg}};border:1px solid {{fg15}};padding:10px 24px;border-radius:{{cr}};font-size:14px;cursor:pointer;'>Secondary</button></div><div style='display:flex;gap:8px;flex-wrap:wrap;'><span style='background:{{fg6}};border-radius:100px;padding:4px 12px;font-size:11px;color:{{mt}};'>Tag One</span><span style='background:{{fg6}};border-radius:100px;padding:4px 12px;font-size:11px;color:{{mt}};'>Tag Two</span><span style='background:{{ac5}};border-radius:100px;padding:4px 12px;font-size:11px;color:{{ac}};'>Accent Tag</span></div><div style='height:1px;background:linear-gradient(to right,{{ac25}},{{fg6}},{{ac25}});'></div><div style='display:flex;justify-content:space-between;font-size:12px;color:{{mt}};border-bottom:1px solid {{g}};padding:8px 0;'><span>Data row label</span><span style='color:{{fg}};font-weight:600;'>1,234</span></div></div></div>"
}
```

### Mood board data format

Each mood board pre-selects one option from each category. The user picks a mood board in Phase 1, then fine-tunes in Phase 2 with those selections pre-filled.

```json
{
  "name": "Terminal Precision",
  "description": "Code-forward, data-dense, CLI energy. Dark canvas, monospace body, sharp corners.",
  "theme": "dark",
  "arch_index": 0,
  "palette_index": 0,
  "type_index": 0,
  "corners_index": 0,
  "density_index": 0,
  "depth_index": 1,
  "easing_index": 0,
  "corners": "0px",
  "padding": "12px",
  "gap": "8px",
  "shadow": "0 2px 16px rgba(0,230,255,0.15)"
}
```

Indices reference into the ARCHITECTURES, PALETTES, and TYPEPAIRS arrays. The template renders a mini preview of each mood board using its architecture's `preview_html` with the mood board's palette/type applied.

### Prompt context data format

```json
{
  "title": "AI Coding Assistant",
  "headline": "Your Code, Understood.",
  "subline": "An AI coding assistant that reads your entire codebase.",
  "section_desc": "Layout options for your product launch"
}
```

`title` appears in the Phase 1 header. `headline` and `subline` replace `{{prompt_headline}}` and `{{prompt_sub}}` in architecture preview_html so previews show real content.

### Content tokens in preview_html

In addition to the standard design tokens (`{{bg}}`, `{{fg}}`, `{{ac}}`, etc.), architecture `preview_html` can use:

- `{{prompt_headline}}` — the user's actual headline text
- `{{prompt_sub}}` — the user's actual subline text

This makes previews contextual — the user sees their own content styled, not generic placeholders.

## Serving and user selection

4. Serve the file: `cd <project-dir> && python3 -m http.server 8723 &` (use port 8723 or any unused port above 8000; if the curl check fails, try the next port). Verify: `curl -s -o /dev/null -w "%{http_code}" http://localhost:8723/.hyperframes/pick-design.html` — only share the link if it returns 200. Do NOT use `npx hyperframes preview` for the picker — it blocks. Only start the HTTP server from the main conversation thread. If you are running as a dispatched task or subagent, return the file path and let the caller serve it.
5. Once the user picks, tell them: "Copy the design.md from the picker and paste it here." The user pastes the markdown back into the conversation. Save it verbatim to `design.md` in the project root — it's already in spec format (YAML frontmatter + prose sections). After the user pastes, kill the background server: `kill %1` or `kill $(lsof -ti:8723)`. Then proceed with construction.

The picker outputs a [google-labs-code/design.md](https://github.com/google-labs-code/design.md) spec-compliant file: YAML frontmatter with `colors`, `typography`, `rounded`, and `spacing` tokens, followed by `## Overview`, `## Colors`, `## Typography`, `## Layout`, `## Elevation`, `## Components`, and `## Do's and Don'ts` prose sections.


<!-- ===== FILE: hyperframes/hyperframes-creative/references/design-spec.md ===== -->

# Design Spec — `frame.md` / `design.md`

The single source of truth for **what a design spec is, how to find it, and how to read it.** Other references defer here for resolution + format; the _consumption_ contract ("brand, not layout") lives in `video-composition.md`.

## What `frame.md` is

`frame.md` is the **frame-scale design system** for a video / hyperframes project — the video-first companion to `design.md` (which is written for web / static pages). Same file format as `design.md`; it reframes the brand with the frame as the unit.

A spec is **YAML frontmatter + a markdown body**, and the two layers are not equal:

- **Frontmatter is the normative layer** — `colors`, `typography`, `spacing`, `components` are the real, machine-readable values. Quote them verbatim (exact hex, font family, weight); never invent or round them.
- **Prose is context** — the `##` sections (Overview, The Frame, Composition Rules, …) carry intent, when-to-use, and constraints the tokens can't hold. Read them for judgment, not for values.

## Resolving which spec to read

Precedence — read the **first that exists**, ignore the rest:

```
frame.md  →  design.md  →  DESIGN.md
```

```bash
SPEC=$(ls frame.md design.md DESIGN.md 2>/dev/null | head -1)
```

- `frame.md` is the preferred spec for video / hyperframes projects and wins when more than one exists.
- `frame.md` is **always lowercase** — there is no `FRAME.md` variant. (`design.md` and `DESIGN.md` are genuinely different files on Linux; a frame-preset ships an uppercase `FRAME.md` _template_, adopted as lowercase `frame.md` — see "Starting from a preset" below.)

Load the spec **once, in Step 1**; every later step (expansion, authoring, adherence) consumes the already-loaded spec rather than re-resolving it.

## Starting from a preset (optional)

Optionally seed `frame.md` from a ready-made **frame-preset** in `[../frame-presets/](../frame-presets/)` — a fixed set, each shipping a `FRAME.md` template a workflow's design step copies in and overlays with brand tokens. Referencing a preset is **not required**; a bespoke or [picker](design-picker.md)-generated spec is equally valid.

| Preset                                                             | Look                                                                                                                                                                                                                                                                                                                     | Pick when                                                                                                                        |
| ------------------------------------------------------------------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ | -------------------------------------------------------------------------------------------------------------------------------- |
| `[biennale-yellow](../frame-presets/biennale-yellow/FRAME.md)`     | Literary-editorial catalogue — warm parchment ground, single deep indigo ink, solar yellow as radial bloom / panel / tile underprint, Instrument Serif 400 display (tight, negative-tracked) + Archivo body + JetBrains Mono data, strict rectangles (0 rounded corners), 1px hairline rules as sole border, no shadows  | confident / atmospheric / restrained; a product that wants museum-catalogue elegance and editorial authority                     |
| `[blockframe](../frame-presets/blockframe/FRAME.md)`               | Maximalist neobrutalist — 4px black borders, 8px hard offset shadows, five candy pastels, Inter 800–900 uppercase, square corners, tilted decorations                                                                                                                                                                    | bold / punchy / playful-loud; a product that wants to feel confident and graphic                                                 |
| `[blue-professional](../frame-presets/blue-professional/FRAME.md)` | Consulting-grade restraint — warm cream canvas, single saturated cobalt (#1e2bfa) accent only, Space Grotesk + Inter typography, soft tinted cards (4% fill / 20% border / 10–14px radius) with NO shadows, pill chrome (100px), 3-step gray text ladder, cobalt progress bar                                            | measured / executive-readable / premium-signal; a product that wants investment-research rigor and refined restraint             |
| `[bold-poster](../frame-presets/bold-poster/FRAME.md)`             | Populist editorial poster — Shrikhand display tilted −6°..+2°, Libre Baskerville serif body, Space Grotesk mono chrome, four colors only (white / brown-black ink / tomato red / off-white), double-border grids (3px+1.5px), red leftbar cards, red em-dash bullets, stacked text-shadow on red display, square corners | powerful / printed / restrained; a product that wants editorial authority and vintage gravitas                                   |
| `[broadside](../frame-presets/broadside/FRAME.md)`                 | Protest-poster system — two-register flat plane (ink-black / fire-orange), massive lowercase Barlow 900 treated as graphic primitive, IBM Plex Mono chrome (uppercase, 0.14em), fire-orange sole accent, 1px hairlines, sharp corners, no shadow                                                                         | bold / typographic / declarative; a product that wants presence and authority                                                    |
| `[capsule](../frame-presets/capsule/FRAME.md)`                     | Playful editorial — every container a pill (2px ink outline), cream canvas, nine candy accents, Bodoni Moda + Space Grotesk, soft offset shadows, floating-pill wallpaper                                                                                                                                                | friendly / soft / editorial; a product that wants warmth and approachability                                                     |
| `[cartesian](../frame-presets/cartesian/FRAME.md)`                 | Museum-catalog editorial — 1px taupe hairline grid, five warm-stone palette (#EDE8E0 / #E2DBD1 / #1A1A1A / #5A5A5A / #8A8178), Playfair Display 400 + Inter, sharp corners, compass-drafted geometric rings, zero shadow / zero fill                                                                                     | sparse / literary / restrained; a product that wants quiet authority and editorial rigor                                         |
| `[code-editorial](../frame-presets/code-editorial/FRAME.md)`       | Warm-editorial brand book — warm cream paper (never pure white), terracotta coral (#CC785C) as scarce voltage, hairline ink elevation (no heavy shadow), EB Garamond serif display + Inter body + JetBrains Mono index / code on a warm-navy code surface, sentence-case display, ✱ coral spike                          | considered / literary / developer-facing; a code change, launch, or doc that wants editorial calm and a first-class code surface |
| `[cobalt-grid](../frame-presets/cobalt-grid/FRAME.md)`             | Modernist two-color risograph — cream paper, electric cobalt ink, permanent graph-paper grid (10% cobalt), top/bottom cobalt hairlines, Newsreader 400 serif + Hanken Grotesk + DM Mono, 0° corners, pixel-glitch column + QR-block patches                                                                              | restrained / systemic / editorial; a product that wants clarity and measured authority                                           |
| `[coral](../frame-presets/coral/FRAME.md)`                         | Bold editorial magazine — three solid surfaces (coral fire / ink black / warm cream) meeting at hard edges, 45° diagonal hatch on coral, Bebas Neue + Inter tracked caps, zero shadows/radius (circles 50%), oversized wallpaper numerals and giant marks                                                                | bold / structuralist / editorial; a product that wants graphic confidence and hard-edged confidence                              |
| `[creative-mode](../frame-presets/creative-mode/FRAME.md)`         | Neo-brutalist editorial — cream canvas, 4px ink borders, hard offset shadows (no blur), four accents rationed two-to-three, Archivo Black uppercase at 0.92 line-height, JetBrains Mono taxonomy, Space Grotesk body, square corners save one pill chip                                                                  | sparse / graphic / punchy-restrained; a product that wants editorial presence and geometric confidence                           |
| `[daisy-days](../frame-presets/daisy-days/FRAME.md)`               | Cheerful picture-book — 3px charcoal outlines, 6/4px hard offset shadows (no blur), nine sunny-garden pastels (cream + turquoise/soft-pink/butter/mint/lavender/peach/sky + coral accent), Fredoka One + Quicksand, generous radii (20–50px), hand-drawn SVG ornament layer (daisies/stars/suns/clouds/rainbows)         | playful / childlike / sticker-sheet kawaii; a product that wants warmth and whimsy                                               |
| `[editorial-forest](../frame-presets/editorial-forest/FRAME.md)`   | Serif-led literary-editorial — green / pink / cream editorial triad, Source Serif 4 weight 500 (opsz) for display + JetBrains Mono 500 uppercase chrome, flat paper depth (no shadows), 2px hairline rules, 6/8px card radii, monogram circle stamp                                                                      | spacious / restrained / editorial; a product that wants quiet confidence and literary tone                                       |

Each preset folder also ships a `frame-showcase.html` — a preview contact sheet of its frame treatments; open it to _see_ the look, never include it in a project.

## Consuming it

How to apply the spec to a frame — strict on brand (hex, fonts, weight relationships, Do's / Don'ts), free on layout — is the consumption contract in `[video-composition.md](video-composition.md)` ("The Design Spec Is Brand, Not Layout"). Read it before choosing colors or writing HTML; this doc only covers finding and parsing the spec.


<!-- ===== FILE: hyperframes/hyperframes-creative/references/house-style.md ===== -->

# House Style

Creative direction for compositions when no design spec (`frame.md` or `design.md`) is provided. These are starting points — override anything that doesn't serve the content. When a design spec exists, its brand values take precedence; house-style fills gaps.

## Before Writing HTML

1. **Interpret the prompt.** Generate real content. A recipe lists real ingredients. A HUD has real readouts.
2. **Pick a palette.** Light or dark? Declare bg, fg, accent before writing code.
3. **Pick typefaces.** Run the font discovery script in [typography.md](typography.md) — or pick a font you already know that fits the theme. The script broadens your options; it's not the only source.

## Lazy Defaults to Question

These patterns are AI design tells — the first thing every LLM reaches for. If you're about to use one, pause and ask: is this a deliberate choice for THIS content, or am I defaulting?

- Gradient text (`background-clip: text` + gradient)
- Left-edge accent stripes on cards/callouts
- Cyan-on-dark / purple-to-blue gradients / neon accents
- Pure `#000` or `#fff` (tint toward your accent hue instead)
- Identical card grids (same-size cards repeated)
- Everything centered with equal weight (lead the eye somewhere)
- Banned fonts (see [typography.md](typography.md) for full list)

If the content genuinely calls for one of these — centered layout for a solemn closing, cards for a real product UI mockup, a banned font because it's the perfect thematic match — use it. The goal is intentionality, not avoidance.

## Color

- Match light/dark to content: food, wellness, kids → light. Tech, cinema, finance → dark.
- One accent hue. Same background across all scenes.
- Tint neutrals toward your accent (even subtle warmth/coolness beats dead gray).
- **Contrast:** enforced by `hyperframes check` (WCAG AA). Text must be readable with decoratives removed.
- Declare palette up front. Don't invent colors per-element.

## Background Layer

Every scene needs visual depth — persistent decorative elements that stay visible while content animates in. Without these, scenes feel empty during entrance staggering.

Ideas (mix and match, 2-5 per scene):

- Radial glows (accent-tinted, low opacity, breathing scale)
- Ghost text (theme words at 3-8% opacity, very large, slow drift)
- Accent lines (hairline rules, subtle pulse)
- Grain/noise overlay, geometric shapes, grid patterns
- Thematic decoratives (orbit rings for space, vinyl grooves for music, grid lines for data)

All decoratives should have slow ambient GSAP animation — breathing, drift, pulse. Static decoratives feel dead.

**Decorative count vs motion count.** The "2-5 per scene" count refers to decorative _elements_. If a project's design spec says "single ambient motion per scene", it means one looping motion applied to these decoratives (a shared breath/drift/pulse) — not one element total. A scene with 4 decoratives sharing one breathing motion is correct; a scene with 1 decorative is under-dressed.

## Motion

See [motion-principles.md](motion-principles.md) for full rules. Quick: 0.3–0.6s, vary eases, combine transforms on entrances, overlap entries.

## Typography

See [typography.md](typography.md) for full rules. Quick: 700-900 headlines / 300-400 body, serif + sans (not two sans), 60px+ headlines / 20px+ body.

## Palettes

Declare one background, one foreground, one accent before writing HTML.

| Category          | Use for                                       | File                                                          |
| ----------------- | --------------------------------------------- | ------------------------------------------------------------- |
| Bold / Energetic  | Product launches, social media, announcements | [palettes/bold-energetic.md](../palettes/bold-energetic.md)   |
| Warm / Editorial  | Storytelling, documentaries, case studies     | [palettes/warm-editorial.md](../palettes/warm-editorial.md)   |
| Dark / Premium    | Tech, finance, luxury, cinematic              | [palettes/dark-premium.md](../palettes/dark-premium.md)       |
| Clean / Corporate | Explainers, tutorials, presentations          | [palettes/clean-corporate.md](../palettes/clean-corporate.md) |
| Nature / Earth    | Sustainability, outdoor, organic              | [palettes/nature-earth.md](../palettes/nature-earth.md)       |
| Neon / Electric   | Gaming, tech, nightlife                       | [palettes/neon-electric.md](../palettes/neon-electric.md)     |
| Pastel / Soft     | Fashion, beauty, lifestyle, wellness          | [palettes/pastel-soft.md](../palettes/pastel-soft.md)         |
| Jewel / Rich      | Luxury, events, sophisticated                 | [palettes/jewel-rich.md](../palettes/jewel-rich.md)           |
| Monochrome        | Dramatic, typography-focused                  | [palettes/monochrome.md](../palettes/monochrome.md)           |

Or derive from OKLCH — pick a hue, build bg/fg/accent at different lightnesses, tint everything toward that hue.


<!-- ===== FILE: hyperframes/hyperframes-creative/references/motion-principles.md ===== -->

# Motion Principles

## Contents

- Guardrails
- What you do not do without being told
- Visual composition
- Image motion treatment
- Load-bearing GSAP rules

## Guardrails

You know these rules but you violate them. Stop.

- **Don't use the same ease on every tween.** You default to `power2.out` on everything. Vary eases like you vary font weights — no more than 2 independent tweens with the same ease in a scene.
- **Don't use the same speed on everything.** You default to 0.4-0.5s for everything. The slowest scene should be 3× slower than the fastest. Vary duration deliberately.
- **Don't enter everything from the same direction.** You default to `y: 30, opacity: 0` on every element. Vary: from left, from right, from scale, opacity-only, letter-spacing.
- **Don't use the same stagger on every scene.** Each scene needs its own rhythm.
- **Don't use ambient zoom on every scene.** Pick different ambient motion per scene: slow pan, subtle rotation, scale push, color shift, or nothing. Stillness after motion is powerful.
- **Don't start at t=0.** Offset the first animation 0.1-0.3s. Zero-delay feels like a jump cut.

## What You Don't Do Without Being Told

### Easing is emotion, not technique

The transition is the verb. The easing is the adverb. A slide-in with `expo.out` = confident. With `sine.inOut` = dreamy. With `elastic.out` = playful. Same motion, different meaning. Choose the adverb deliberately.

**Direction rules — these are not optional:**

- `.out` for elements entering. Starts fast, decelerates. Feels responsive. This is your default.
- `.in` for elements leaving. Starts slow, accelerates away. Throws them off.
- `.inOut` for elements moving between positions.

You get this backwards constantly. Ease-in for entrances feels sluggish. Ease-out for exits feels reluctant.

### Speed communicates weight

- Fast (0.15-0.3s) — energy, urgency, confidence
- Medium (0.3-0.5s) — professional, most content
- Slow (0.5-0.8s) — gravity, luxury, contemplation
- Very slow (0.8-2.0s) — cinematic, emotional, atmospheric

### Scene structure: build / breathe / resolve

Every scene has three phases. You dump everything in the build and leave nothing for breathe or resolve.

- **Build (0-30%)** — elements enter, staggered. Don't dump everything at once.
- **Breathe (30-70%)** — content visible, alive with ONE ambient motion.
- **Resolve (70-100%)** — exit or decisive end. Exits are faster than entrances.

### Transitions are meaning

- **Crossfade** = "this continues"
- **Hard cut** = "wake up" / disruption
- **Slow dissolve** = "drift with me"

You crossfade everything. Use hard cuts for disruption and register shifts.

### Choreography is hierarchy

The element that moves first is perceived as most important. Stagger in order of importance, not DOM order. Don't wait for completion — overlap entries. Total stagger sequence under 500ms regardless of item count.

### Asymmetry

Entrances need longer than exits. A card takes 0.4s to appear but 0.25s to disappear.

## Visual Composition

You build for the web. Video frames are not pages.

- **Two focal points minimum per scene.** The eye needs somewhere to travel. Never a single text block floating in empty space.
- **Fill the frame.** Hero text: 60-80% of width. You will try to use web-sized elements. Don't.
- **Three layers minimum per scene.** Background treatment (glow, oversized faded type, color panel). Foreground content. Accent elements (dividers, labels, data bars).
- **Background is not empty.** Radial glows, oversized faded type bleeding off-frame, subtle border panels, hairline rules. Pure solid #000 reads as "nothing loaded."
- **Anchor to edges.** Pin content to left/top or right/bottom. Centered-and-floating is a web pattern.
- **Split frames.** Data panel on the left, content on the right. Top bar with metadata, full-width below. Zone-based layouts, not centered stacks.
- **Use structural elements.** Rules, dividers, border panels. They create paths for the eye and animate well (scaleX from 0).
- **Connector lines earn their place.** Any beam, rail, scan line, or drawn underline must be able to name its start anchor, its end anchor (real elements, not empty space), and its job — revealing, routing, validating, or emphasizing something. A line the frame can lose without losing meaning is decoration: cut it. An edge-lit component (a card's top highlight, a state dot) usually reads as more designed than a free-floating arc.

## Image Motion Treatment

Never embed a raw flat image. Every image must have motion treatment:

- **Perspective tilt**: use `gsap.set(el, { transformPerspective: 1200, rotationY: -8 })` + `box-shadow` — creates depth. Do NOT use CSS `transform: perspective(...)` as GSAP will overwrite it.
- **Slow zoom (Ken Burns)**: GSAP `scale: 1` → `1.04` over beat duration — makes photos cinematic
- **Device frame**: Wrap in a laptop/phone shape using CSS `border-radius` and `box-shadow`
- **Floating UI**: Extract a key element and animate it at a different z-depth for parallax
- **Scroll reveal**: Clip the image to a viewport window and animate `y` position

## Load-Bearing GSAP Rules

Rules below came out of two independent website capture builds (2026-04-20) where compositions lint-clean and still ship broken — elements that never appear, ambient motion that doesn't scrub, entrance tweens that silently kill their target. The linter cannot catch these; the rules must be followed by the author.

- **No iframes for captured content.** Iframes do not seek deterministically with the timeline — the capture engine cannot scrub inside them, so they appear frozen (or blank) in the rendered output. If the source you're stylizing is a live web app, use the screenshots from `capture/` as stacked panels or layered images, not live embeds.

- **Never overlap conflicting transform tweens on the same element.** Sequential, non-overlapping transform phases are valid. The dangerous case is concurrent tweens or `from()` tweens whose `immediateRender` states overwrite one another: for example, a `y` entrance plus a simultaneous `scale` Ken Burns tween on the same `<img>`. The element can remain invisible or offscreen with no lint warning. Fix the overlap in one of two ways:

  ```html
  <!-- BAD: two transforms on one element -->
  <img class="hero" src="..." />
  <script>
    tl.from(".hero", { y: 50, opacity: 0, duration: 0.6 }, 0);
    tl.to(".hero", { scale: 1.04, duration: beat }, 0); // kills the entrance
  </script>

  <!-- GOOD option A: combine into one tween -->
  <script>
    tl.fromTo(
      ".hero",
      { y: 50, opacity: 0, scale: 1.0 },
      { y: 0, opacity: 1, scale: 1.04, duration: beat, ease: "none" },
      0,
    );
  </script>

  <!-- GOOD option B: split across parent + child -->
  <div class="hero-wrap"><img class="hero" src="..." /></div>
  <script>
    tl.fromTo(".hero-wrap", { y: 50, opacity: 0 }, { y: 0, opacity: 1, duration: 0.6 }, 0); // entrance on parent
    tl.to(".hero", { scale: 1.04, duration: beat }, 0); // Ken Burns on child
  </script>
  ```

- **Prefer `tl.fromTo()` over `tl.from()` inside `.clip` scenes.** `gsap.from()` sets `immediateRender: true` by default, which writes the "from" state at timeline construction — before the `.clip` scene's `data-start` is active. Elements can flash visible, start from the wrong position, or skip their entrance entirely when the scene is seeked non-linearly (which the capture engine does). Explicit `fromTo` makes the state at every timeline position deterministic:

  ```js
  // BRITTLE: immediateRender interacts badly with scene boundaries
  tl.from(el, { opacity: 0, y: 50, duration: 0.6 }, t);

  // DETERMINISTIC: state is defined at both ends, no immediateRender surprise
  tl.fromTo(el, { opacity: 0, y: 50 }, { opacity: 1, y: 0, duration: 0.6 }, t);
  ```

- **Ambient pulses must attach to the seekable `tl`, never bare `gsap.to()`.** Auras, shimmers, gentle float loops, logo breathing — all of these must be added to the scene's timeline, not fired standalone. Standalone tweens run on wallclock time and do not scrub with the capture engine, so the effect is absent in the rendered video even though it looks correct in the studio preview:

  ```js
  // BAD: lives outside the timeline, never renders in capture
  gsap.to(".aura", { scale: 1.08, yoyo: true, repeat: 5, duration: 1.2 });

  // GOOD: seekable, deterministic, renders
  tl.to(".aura", { scale: 1.08, yoyo: true, repeat: 5, duration: 1.2 }, 0);
  ```

- **Hard-kill exiting inner elements at a scene boundary, not the `.clip` itself.** A non-clip element or wrapper whose visibility changes at a beat boundary may need a deterministic zero-duration `tl.set()` kill after its fade, because a later tween or sibling `immediateRender` can resurrect it. This is the explicit-boundary exception to the ban on raw `visibility` tweens. HyperFrames alone controls `.clip` lifecycle; never apply this pattern to the clip container.

  ```js
  tl.to(innerEl, { opacity: 0, duration: 0.3 }, beatEnd);
  tl.set(innerEl, { opacity: 0, visibility: "hidden" }, beatEnd + 0.3); // non-clip kill
  ```

These are the exact rules with the exact code examples — don't summarize or shorten them. They exist because compositions that lint clean still ship broken without them.


<!-- ===== FILE: hyperframes/hyperframes-creative/references/narration.md ===== -->

# Narration & Script

How to write narration scripts for video compositions. Read when the composition includes voiceover or TTS.

## Pacing

- **2.5 words per second** is natural speaking pace
- 15s = ~37 words. 30s = ~75 words. 60s = ~150 words
- Leave room for pauses. Silence between sentences is a feature, not dead air
- The script should feel SHORTER than the video — visual breathing room matters

## Tone

Write like a person, not a brochure:

- Use contractions: "it's", "you'll", "that's", "we've"
- Vary sentence length — short punchy phrases mixed with longer flowing ones
- Read it out loud. If it sounds robotic, rewrite it
- Avoid jargon unless the audience expects it

## Number Pronunciation

Write what you want the voice to say. TTS reads literally.

| In the product | Write in script as                |
| -------------- | --------------------------------- |
| 135+           | more than one hundred thirty five |
| $1.9T          | nearly two trillion dollars       |
| 99.999%        | ninety nine point nine percent    |
| 200M+          | over two hundred million          |
| 10x            | ten times                         |
| API            | A P I                             |
| stripe.com     | stripe dot com                    |

The visual can show the exact figure while the voice rounds it.

## Structure

For product videos:

1. **Hook** — what's surprising or impressive about this product? A bold claim, a provocative question, a contrast, or a striking number. This is the opening line. **Vary the hook type** — don't default to a stat every time.
2. **Story** — what does the product do? Who uses it? Keep it concrete.
3. **Proof** — stats, customer names, social proof. Real numbers from the product.
4. **CTA** — what should the viewer do? "Start building at stripe dot com."

Not every video needs all four. A 15-second social ad might be Hook + Proof + CTA. A 60-second product tour uses all four with more Story.

## The Opening Line

The most important sentence in the video. It must create tension, curiosity, or surprise in the first 3 seconds.

Patterns that work:

- **A bold claim**: "The financial infrastructure that powers the internet economy."
- **A question that provokes**: "What if your database could think?"
- **A contrast**: "Your AI agent already knows how to make videos. It just needs the right format."
- **A number that shocks**: "Nearly two trillion dollars." (Use sparingly — not every video should open with a stat.)

If the opening is generic ("Welcome to Stripe" / "Introducing our product"), start over.

## Example

From a 62-second product launch video (team reference):

```
Your AI agent already knows how to make videos.
It just needs the right format.

This is Hyperframes. An open source framework. HTML in, video out.

A div is a keyframe. Data attributes are your timeline.
CSS is your look. G-Sap is your animation engine.

Anything a browser can render can be a frame in your video.

CSS animations. G-Sap. Lottie. Shaders. Three.js.

Drop in music, sound effects, footage — it all composes together.

No new framework for the agent to learn.
Just HTML.

The agent writes it. The renderer captures every frame as MP4.
It's deterministic. Identical outputs, every time.

Give your agent the CLI. Tell it what to make.
Watch it build.

Hyperframes. Go make something.
```

Note: ~140 words for 62 seconds — that's 2.3 words/sec, leaving room for pauses and visual breathing.


<!-- ===== FILE: hyperframes/hyperframes-creative/references/prompt-expansion.md ===== -->

# Prompt Expansion

Run on every composition. Expansion is not about lengthening a short prompt — it's about grounding the user's intent against the design spec (`frame.md` or `design.md`) and `house-style.md` and producing a consistent intermediate that every downstream agent reads the same way.

Runs AFTER design direction is established (Step 1). The expansion consumes the design spec (`frame.md` or `design.md`, if present) and produces output that cites its exact values.

## Prerequisites

Read before generating:

- the design spec — `frame.md` → `design.md` → `DESIGN.md` (read the first that exists) — extract brand colors, fonts, mood, and constraints. The expansion cites these exact values (hex codes, font names); it does not invent new ones.
- `references/beat-direction.md` — per-beat planning format (concept, mood, choreography verbs, transitions, depth layers, rhythm). The expansion outputs each scene using this format.
- `references/video-composition.md` — video-medium rules for density, scale, and color presence. The expansion applies these automatically.
- `house-style.md` — its rules for Background Layer (2-5 decoratives), Color, Motion, Typography apply to every scene. The expansion writes output that conforms to them.

If no design spec (`frame.md` or `design.md`) exists yet, run Step 1 (Design system) first. Expansion without a design context produces generic scene breakdowns that later agents ignore.

## Why always run it

**The expansion is never pass-through.** Every user prompt — no matter how detailed — is a _seed_. The expansion's job is to enrich it into a fully-realized per-scene production spec that the scene subagents can build from directly.

Even a detailed 7-scene brief lacks things only the expansion adds:

- **Atmosphere layers per scene** (required 2–5 from house-style: radial glows, ghost type, hairline rules, grain, thematic decoratives) — the user's prompt almost never lists these; expansion adds them.
- **Secondary motion for every decorative** — breath, drift, pulse, orbit. A decorative without ambient motion feels dead.
- **Micro-details that make a scene feel real** — registration marks, tick indicators, monospace coord labels, typographic accents, code snippets in the background, grid patterns. Things the user didn't think to request.
- **Transition choreography at the object level** — not "crossfade" but "X expands outward and becomes Y". Specific duration, ease, and morph source/target.
- **Pacing beats within each scene** — where tension builds, where a hold lets the viewer breathe, where the accent word lands.
- **Exact hex values, typography parameters, ease choices** from the design spec — no vagueness left for the scene subagent to guess.

Expansion's job on a detailed prompt is not to summarize or pass through — it's to **take what the user wrote and make it richer**. The user's content stays; the atmosphere, ambient motion, and micro-details are added on top. That's what makes the difference between a scene that matches the brief and a scene that feels alive.

The quality gap between a single-pass composition and a multi-scene-pipeline composition comes from this step. Expansion front-loads the richness so every scene subagent builds from a rich brief, not a terse one.

**Do not skip. Do not pass through.** Single-scene compositions and trivial edits are the only exceptions.

## What to generate

Expand into a full production prompt with these sections:

1. **Title + style block** — cite the design spec's exact hex values, font names, and mood. Do NOT invent a palette — quote what the design provides.

2. **Rhythm declaration** — name the scene rhythm before detailing any scene. Example: `hook-PUNCH-breathe-CTA` or `slow-build-BUILD-PEAK-breathe-CTA`. Use `references/beat-direction.md` for rhythm templates by video type.

3. **Global rules** — parallax layers, micro-motion requirements, transition style, primary + accent transitions. Match energy to mood (calm → slow eases, high → snappy eases).

4. **Per-scene beats** — for each scene, use the beat-direction format:
   - **Concept** — the big idea in 2-3 sentences. What visual WORLD? What metaphor? What should the viewer FEEL?
   - **Mood direction** — cultural/design references, not hex codes. ("Bauhaus color studies", "cinematic title sequence", "editorial calm")
   - **Depth layers** — BG treatment, MG content, and FG accents or structural details as the concept needs. Use `video-composition.md` to choose density; do not force an element count or invent content to fill one.
   - **Animation choreography** — specific verbs per element. High: SLAMS, CRASHES. Medium: CASCADE, SLIDES. Low: floats, types on, counts up. Every element gets a verb. If you can't name the verb, the element is not yet designed.
   - **Transition out** — shader or CSS, with specific type and parameters. Not "crossfade" but "blur crossfade, 0.4s, power2.inOut."

5. **Recurring motifs** — visual threads across scenes from the brand palette.

6. **Negative prompt** — what to avoid, informed by the design spec's constraints if present.

## Output

Write the expanded prompt to `.hyperframes/expanded-prompt.md` in the project directory. Do NOT dump it into the chat — it will be hundreds of lines.

Tell the user:

> "I've expanded your prompt into a full production breakdown. Review it here: `.hyperframes/expanded-prompt.md`
>
> It has [N] scenes across [duration] seconds with specific visual elements, transitions, and pacing. Edit anything you want, then let me know when you're ready to proceed."

Only move to construction after the user approves or says to continue.


<!-- ===== FILE: hyperframes/hyperframes-creative/references/story-spine.md ===== -->

# Story spine — value-first narrative doctrine

Applies to the narrated, story-driven creation workflows — `/product-launch-video`, `/pr-to-video`, `/faceless-explainer`, and `/general-video` when the piece tells a story. It does **not** apply to `/music-to-video` (the track drives the arc), `/motion-graphics` (no narration — motion is the message), `/embedded-captions` and `/talking-head-recut` (the footage's story is already fixed), or `/slideshow` (the presenter owns the story). Do not force these rules onto an exempt workflow.

Each workflow's own story-design reference owns its archetypes, beat sequences, and frame vocabulary. This file owns four cross-workflow rules about **order** and **justification** — the reverse iceberg: lead with why it's valuable, not with what it is or how it was made.

## 1. The hook speaks the viewer's language

The first beat answers "why should I care" in **outcome language** — what the viewer gains, avoids, or finally understands. Subject-internal vocabulary is banned in the hook: file / function / API names for a code change; a feature list for a product; the source article's section headings for an explainer. Numbers are welcome only when they carry stakes ("40% faster cold starts"), never inventory ("23 files changed").

## 2. Reverse iceberg — value before evidence

The value claim (the brief's `message`) lands **by the second beat**. Everything after it is evidence in service of that claim — the diff, the mechanism, the feature demo, the site's screenshots. Implementation is the footnote of the story, not the spine.

Self-check on the finished beat list:

- Delete every evidence beat — the remaining beats must still state the value on their own.
- Delete the value beats — if the video still seems to work, it was a feature tour / diff readout, not a story.

Structure is value-first; the **voice** stays whatever the workflow prescribes (a PR video keeps its plain, no-hype developer voice — leading with value is an ordering decision, not a marketing register).

## 3. The storyboard is a proposal, not a listing

When Step 3 presents the plan (a checkpoint gate — `hyperframes/references/brief-contract.md` § 1):

- Open by echoing the strategy line: **"This video tells [audience] that [message]."**
- Present the frames as a markdown table, one row per frame:

  | Frame            | Beat      | On screen                                               | Why                             |
  | ---------------- | --------- | ------------------------------------------------------- | ------------------------------- |
  | 01 — Not anymore | hook · 9s | States the old pain and resolves it in the same breath. | Lands the value claim in beat 1 |

  **Why** is the frame's job in the story (from its `narrativeRole`), traced back to the message — a frame whose why cannot be traced to the message is a frame to cut, not to decorate.

- Recommendations keep their receipts (brief-contract § 3): the archetype choice, the beat count, and any beat the user might question each state their basis.

How to write the storyboard itself, and the board it is reviewed on (`boards/storyboard.html`), is `storyboard-recipe.md`.

The proposal shape — echo line → frame table → style / duration footer → "approve or adjust" — is the cheapest place to iterate: a frame change here costs 30 seconds; the same change after build costs minutes.

## 4. Visuals point back to the source

When the piece derives from concrete source material — a PR, a repo, an article, a product page — mine that material for the visual vocabulary before inventing any: its phrases, entities, verbs, and recurring motifs are the props. Each frame's key visual should be traceable to a specific line of the source, the same way its **Why** traces to the message: real filenames over generic file icons, the product's own numbers over invented ones, the article's own metaphor over a stock one.

Self-check per visual: if the prop could appear unchanged in another product's video, it didn't come from the source. Swap it for something only this subject could produce before decorating it.


<!-- ===== FILE: hyperframes/hyperframes-creative/references/storyboard-recipe.md ===== -->

# Storyboard recipe — plan a video as stills the person approves

Applies wherever a run plans on a storyboard (`storyboard: yes` in `brief-contract.md`), and whenever a run makes or changes a storyboard, a sketch sheet or a board of frames, whatever skill or workflow asked for one. This file owns **how to make the board**. `review-loop.md` owns when the person is asked; `storyboard-format.md` owns the `STORYBOARD.md` file the scripts parse; `story-spine.md` owns the order of the story.

The person sees the plan as stills on the board, comments or draws on a frame, and says go. The board is `boards/storyboard.html`, and tools that show it find its frames by the classes in § 2; boxes marked any other way (`cell` boxes, `id="frame-NN"` markers) are not found.

## 1. The run

1. **Pose each shot** in the composition the project renders, the root `index.html`, at its key moment: real words, real fonts, real colors, the focal point big enough to read on a phone. A shot posed in its own file (`compositions/frames/NN-*.html`) shows only once it is mounted in `index.html` (`data-composition-src`) at its planned start; `snapshot` renders `index.html` and nothing else.
2. **Snapshot every still in one run** with your host's snapshot tool when one is offered (each shot's seconds, out `boards/stills`); otherwise `npx hyperframes snapshot --at <every shot's seconds, in film order> --no-end --describe false -o boards/stills`. Each still is named `frame-NN-at-<seconds>s.png`, NN its place in the film. Every `snapshot` run clears its `-o` folder and numbers from `00`, so never snapshot a single moment into `boards/stills/` itself (step 4). Look at every still yourself; fix and snapshot again until each one holds.
3. **Write `boards/storyboard.html`** (§ 2), styled as a finished board: Inter or the system sans-serif, a light page, each frame a rounded card with its still above its words, even gaps.
4. **Stop.** Hand the person the board and wait for their go. Notes on frames change only those frames. For each one: re-pose it, snapshot just its moment into `boards/stills/redo/` (`--at <its seconds>`), move that one file over the frame's old still under the old name (its new time in the name if the time changed, and the page's `src` with it), then rewrite the page and stop again. The other stills stay as approved.
5. **Once they say go**, animate from the approved stills.

## 2. The page

One `class="frame"` box per still, in film order, holding its image, a `class="title"` line "<two-digit number>: <name>" and a `class="time"` range in seconds. Optional: a `class="words"` line under it, and a `class="act"` heading before the first frame of each act.

```html
<section class="act">Act 1: The hook</section>
<div class="frame">
  <img src="stills/frame-00-at-1.5s.png" alt="" />
  <div class="title">01: The hook</div>
  <div class="time">0.0 to 3.0s</div>
  <p class="words">The headline pushes in on a dark canvas.</p>
</div>
```

Stills are written next to the page (`boards/stills/`), so `src` is relative to `boards/` and names the file `snapshot` wrote for that shot. A still written after the page shows by itself; never reopen or rename the page for it.

## 3. The plan beside it

`STORYBOARD.md` at the project root (format: `hyperframes/references/storyboard-format.md`) names the same frames in the same order, and its words win over the page's: one heading per frame like `## Frame 1: The hook (0-3s)`, a `- act:` bullet for its act, and `- status: outline` until its still is posed.
