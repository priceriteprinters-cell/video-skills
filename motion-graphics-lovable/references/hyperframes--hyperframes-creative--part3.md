

<!-- ===== FILE: hyperframes/hyperframes-creative/frame-presets/coral/FRAME.md ===== -->

---
version: alpha
name: Coral — Frame (video / frame layer)
description: >
  Video-first companion to Coral's design.md. The unit is the frame (1920×1080), not the
  slide-in-a-deck. Atoms are identical and sacred — the three-surface system (coral fire /
  ink black / warm cream), Bebas Neue uppercase tracked + Inter body, the 45° diagonal hatch,
  decorative wallpaper numerals, hard color-region splits, zero shadow, zero radius (save
  circles). Composition, frame scale, and aspect-ratio behavior are rewritten for the frame.
  Motion is out of scope.
unit: the frame — 1920×1080 primary; 9:16 and 1:1 documented
principle: atoms are sacred · composition is free · numbers come from the script

colors:
  coral: "#E85D5D"
  coral-dark: "#D44A4A"
  cream: "#F5F0E8"
  cream-dark: "#E8E0D4"
  black: "#1A1A1A"
  gray: "#6B6B6B"
  light-gray: "#B0B0B0"
  white: "#FFFFFF"

typography:
  # — reading ramp (Inter) —
  body:          { fontFamily: "Inter", cqw: 1.0,  weight: 400, lineHeight: 1.7 }
  body-light:    { fontFamily: "Inter", cqw: 1.5,  weight: 300, lineHeight: 1.5, note: "pull-quote voice" }
  section-label: { fontFamily: "Inter", px: 12, weight: 700, tracking: "4px", upper: true }
  item-label:    { fontFamily: "Inter", px: 11, weight: 700, tracking: "3px", upper: true }
  quote-attribution: { fontFamily: "Inter", px: 14, weight: 600, tracking: "3px", upper: true }
  quote-role:    { fontFamily: "Inter", px: 12, weight: 400, tracking: "1px" }
  # — display / hero ramp (Bebas Neue, uppercase, tracked) —
  card-title:    { fontFamily: "Bebas Neue", cqw: 1.9, weight: 400, lineHeight: 1.1, tracking: "1px", upper: true }
  sidebar-value: { fontFamily: "Bebas Neue", cqw: 2.3, weight: 400, lineHeight: 1.0, upper: true }
  bar-title:     { fontFamily: "Bebas Neue", cqw: 2.3, weight: 400, lineHeight: 1.0, tracking: "2px", upper: true }
  card-stat:     { fontFamily: "Bebas Neue", cqw: 2.5, weight: 400, lineHeight: 1.0, upper: true }
  column-title:  { fontFamily: "Bebas Neue", cqw: 3.7, weight: 400, lineHeight: 1.0, tracking: "2px", upper: true }
  section-headline:{ fontFamily: "Bebas Neue", cqw: 4.2, weight: 400, lineHeight: 1.0, tracking: "2px", upper: true }
  stat-numeral:  { fontFamily: "Bebas Neue", cqw: 5.0, weight: 400, lineHeight: 1.0, upper: true }
  hero-title:    { fontFamily: "Bebas Neue", cqw: 6.5, weight: 400, lineHeight: 0.9, tracking: "4px", upper: true }
  jumbo-feature: { fontFamily: "Bebas Neue", cqw: 9.0, weight: 400, lineHeight: 1.0, tracking: "12px", upper: true }
  # — decorative —
  background-numeral: { fontFamily: "Bebas Neue", cqw: 10.0, weight: 400, color: "rgba(0,0,0,0.12)", note: "wallpaper numeral inside a coral region" }
  giant-mark:    { fontFamily: "Bebas Neue", cqw: 14.0, weight: 400, color: "rgba(0,0,0,0.35)", note: "decorative quote mark inside a coral region" }

spacing:
  pad-x: "5cqw"       # standard horizontal frame padding
  pad-y: "4cqw"
  pad-col: "3cqw"
  gap-grid: "1.7cqw"
  card-pad: "2cqw"

components:
  diagonal-hatch:
    backgroundImage: "repeating-linear-gradient(45deg, transparent 0 20px, rgba(0,0,0,.06) 20px 40px)"
    placement: "::before overlay on {colors.coral} regions"
    description: "Signature 45° hatch (6% ink). Variants −45° 30/60px, 90° vertical 60/62px 10% ink. Texture, never depth."
  region-split:
    layout: "two/three solid surfaces meeting at a hard edge; ratios 38/62 rows, 40/60 cols, 50/50"
    rounded: "0"
    description: "The primary layout device — no gradient, no rounded junction; the boundary is the layout."
  card:
    backgroundColor: "{colors.white}"
    borderTop: "0.26cqw solid {colors.coral}"
    rounded: "0"
    shadow: "none"
    typography: "{typography.card-title} + {typography.body}"
    description: "5px coral TOP border is the only chrome; holds a card-icon, title, body, coral card-stat."
  sidebar-item:
    backgroundColor: "{colors.white}"
    borderLeft: "0.2cqw solid {colors.coral}"
    rounded: "0"
    typography: "{typography.sidebar-value} + {typography.section-label}"
    description: "4px coral LEFT border is the only chrome."
  card-icon:
    backgroundColor: "{colors.coral}"
    textColor: "{colors.white}"
    size: "2.5cqw square"
    rounded: "0"
    description: "The card mark — one white Bebas glyph centered."
  accent-line:
    backgroundColor: "{colors.coral}"
    size: "4cqw × 0.25cqw (60×4 closing variant)"
    rounded: "0"
    description: "Sub-headline accent rule."
  background-numeral:
    typography: "{typography.background-numeral}"
    color: "rgba(0,0,0,0.12)"
    placement: "behind a {colors.coral} region's title"
    description: "The wallpaper-numeral signature (12% ink)."
  giant-mark:
    typography: "{typography.giant-mark}"
    color: "rgba(0,0,0,0.35)"
    placement: "inside a {colors.coral} region"
    description: "Oversized quote mark / character, half-decorative."
  timeline:
    line: "0.2cqw solid {colors.black} (gradient-dashed ::after)"
    node: "{colors.coral} circle, {colors.cream} halo, 50% radius"
    description: "Ink line with coral nodes + cream halos."
  info-bar:
    backgroundColor: "{colors.cream-dark}"
    typography: "{typography.bar-title} + uppercase {typography.section-label}"
    rounded: "0"
    shadow: "none"
    description: "Footer band beneath a feature region — Bebas title left, Inter meta right."
---

# Coral — Frame (video / frame layer)

## Overview

Coral at frame scale is a **bold magazine poster** built from three solid surfaces — coral fire,
ink black, warm cream — that meet at **hard color edges.** The region boundary IS the layout: a
frame splits into a coral plane + a cream plane, or a coral panel + an ink panel, each holding a
self-contained composition. No gradient transitions, no rounded junctions, no drop shadows.

The voice is a two-face hierarchy: **Bebas Neue** — tall condensed caps, always uppercase, always
tracked (1–12px) — carries every headline, stat, title, and meta figure; **Inter** carries every
body line, label, and attribution across weights 300–700. Bebas declares; Inter explains. The
signature atmospherics are the **45° diagonal hatch** (6% ink) over coral regions and the
**oversized wallpaper numeral** (12% ink) behind a region's title.

**Key characteristics at frame scale:**

- **Three surfaces, hard edges** — `{colors.coral}` / `{colors.black}` / `{colors.cream}` as solid regions.
- **Bebas uppercase + tracking** on every display element; **Inter** on every body/label.
- **45° hatch** (6% ink) on coral regions; **wallpaper numerals** (12%) and **giant marks** (35%) behind content.
- **Ink-on-fire** — Bebas on coral is always ink, never white. Eyebrows coral on cream/ink, ink on coral.
- **Flat** — no shadow, no elevation; radius only on circles (nav dots, timeline nodes).
- **Coral as accent AND environment** — 4–5px coral borders, 48px coral icon squares, and full coral regions.

### Frame Craft Bar

Three eyeball tests gate every frame before any structural check:

- **Squint** — one element dominates at **3–6× its nearest neighbor**: the `hero-title`/`jumbo-feature` or a wallpaper numeral behind a region's title, never two rival headlines.
- **Silence** — coral/cream/ink regions read **40–55% empty**; the **three-column catalog is the one dense exception**. A coral region underfilled gets a wallpaper numeral, never more content.
- **Restraint** — coral fires as **either accent or one full region per frame** (not both at full strength); one giant-mark per quote; ink-on-fire (never white on coral).
- **Reference** — aim at a **sports-magazine cover / Saul Bass travel poster** (solid planes at hard edges, condensed caps as architecture); failure looks like a **soft drop-shadowed card deck**.

## The Frame

- **Primary:** 1920×1080 (16:9). Display sizes authored in **`cqw`** (`px ÷ 1920 × 100 = cqw`).
- **Vertical:** 1080×1920 (9:16). **Square:** 1080×1080 (1:1).
- **Safe area:** `5cqw` (pad-x) standard frame padding; region edges may bleed full-frame.

**The container law (load-bearing).** Every frame ground sets `container-type: size`; ALL
frame-relative units are `cqw`/`cqh` resolved against it — **never `vw`.** A `vw`-sized frame
inflates whenever it isn't full-screen; `cqw` resolves against the frame at any render size.

## Colors

Tokens identical to the source. At frame scale the three surfaces are intermixed by composition —
coral/cream, coral/ink, ink/cream, or single-surface. `{colors.coral}` is both accent (borders,
icon squares, timeline nodes, eyebrows on cream/ink) and environment (full regions). Headlines:
ink on cream/coral, cream on ink — **never gray, never white-on-coral.** Eyebrows: coral on
cream/ink, ink on coral — coral-on-coral does not exist. The only sanctioned gradient is the rare
135° coral-dark→coral feature region; everything else is flat.

## Typography

Two ramps. The **reading ramp** (Inter body 1.0cqw, body-light 1.5cqw, labels in px) carries copy
and eyebrows; the **display/hero ramp** (Bebas, `card-title` 1.9cqw → `jumbo-feature` 9.0cqw, plus
the decorative `background-numeral` 10cqw and `giant-mark` 14cqw) carries every headline and stat.

- **Legibility floor:** any load-bearing line ≥ **1.4cqw**; px labels are chrome only.
- **Fit-to-measure:** size the headline to its line length. Cap the block at **≤ 78cqw**; ≤3 words → `hero-title`/`jumbo-feature`; 4–6 → `section-headline`; 7+ → `column-title`.
- **Every Bebas element is uppercase with ≥1px tracking** (2px standard, 4px hero, 12px jumbo). **Every Inter label is uppercase, 1–4px tracked.** No italic, no underline, no sentence-case Bebas.

## Depth & Surface

Flat, with hard color edges. Depth signals only:

- **Hard region boundaries** — the primary structural device.
- **Accent borders** — 5px coral top (cards), 4px coral left (sidebar tiles), 4px ink (timeline).
- **45° hatch** — 6% ink texture on coral regions (no depth).
- **Wallpaper typography** — numerals at 12%, giant marks at 35%, layered behind content.

**Ceiling:** no box-shadow, no elevated card, no soft gradient (save the one 135° coral feature), no rounded rectangle.

## Shapes

- **0 radius** on every rectangle — regions, cards, sidebar tiles, icon squares, info bars, accent lines.
- **50%** on circles only — nav dots (10px), nav arrows (44px), timeline nodes (20px).

## Components

- **region-split** — the layout device; surfaces meet at a hard edge.
- **card** (5px coral top) / **sidebar-item** (4px coral left) / **card-icon** (48px coral square) — the only chrome on each is its single coral border.
- **diagonal-hatch** / **background-numeral** / **giant-mark** — the atmospheric + wallpaper signatures on coral regions.
- **accent-line** — coral sub-headline rule. **timeline** — ink line, coral nodes, cream halos. **info-bar** — cream-dark footer band.

## Frame Treatments

> Recipe per plate: ground · container · composes · focal · chrome · accent · silence · Fixed/Free · density.
> Lean centered where the move allows; vary anchor; one idea per region.

### 1 · Region-Split Cover (identity · move: hard region edge · left)

**Ground** 38/62 split — `{colors.coral}` top band (hatch + wallpaper numeral) over `{colors.cream}`.
**Container** grid rows; brand + meta in the coral band, hero title in the cream field. **Composes**
region-split, diagonal-hatch, background-numeral, hero-title. **Focal** a 2-line `hero-title` in
ink, second line in `{colors.coral}`, left-anchored in the cream field. **Chrome** Bebas brand left

- Bebas meta right in the coral band. **Accent** coral band + coral second line. **Silence** the
  cream field ~45% empty. **Fixed** ink-on-fire in band, hatch on coral, hard edge. **Free** title
  copy, which line is coral, meta. **Density** sparse.

### 2 · Feature Stat (anchor · move: scale · coral environment · left)

**Ground** full `{colors.coral}` with hatch. **Composes** diagonal-hatch, background-numeral,
section-label, stat headline, body-light. **Focal** a `stat-numeral`/`jumbo-feature` figure or
2-line headline in ink, with a `background-numeral` (12% ink) behind it as wallpaper. **Chrome** an
ink `section-label` eyebrow; an optional Inter-300 support line ≤44cqw. **Accent** the coral ground
IS the environment; ink type, no white. **Silence** ~40% of the coral field empty. **Fixed**
ink-on-coral, hatch present, wallpaper numeral behind. **Free** the figure, headline, support copy.
**Density** sparse.

### 3 · Quote Layout (quote · move: panel split · giant mark)

**Ground** 40/60 split — `{colors.coral}` left panel (hatch + giant-mark) + `{colors.black}` right
panel. **Composes** region-split, giant-mark, body-light, accent-line, quote-attribution.
**Focal** a 2–3 line pull quote in `{colors.cream}` Inter **weight 300** on the ink panel.
**Chrome** a `giant-mark` (35% ink) on the coral panel; a `60×4` coral accent-line above the
attribution. **Accent** coral panel + coral accent-line. **Silence** the coral panel is mostly the
mark. **Fixed** Inter-300 quote, ink panel, ink-on-coral mark. **Free** quote, attribution, mark
glyph. **Density** sparse.

### 4 · Closing Plate (closer · move: cream field + coral band · centered)

**Ground** `{colors.cream}` field with a bottom `{colors.coral}` band (hatch). **Composes**
section-label, section-headline/hero-title, accent-line, info-bar. **Focal** a 2-line sign-off in
ink, centered, with a coral `accent-line` beneath. **Chrome** an ink eyebrow above; a coral band
footer carrying a Bebas sign-off + year. **Accent** coral band + coral accent-line. **Silence**
~55% empty cream. **Fixed** centered, ink type, one coral band. **Free** sign-off copy, band
contents. **Density** sparse.

### 5 · Three-Column Catalog (catalog · move: density — the dense frame · centered head)

**Ground** `{colors.cream}` (or `{colors.black}`), `pad-x`. **Composes** section-headline, 3× card.
**Focal** a centered `section-headline` over three white `card`s (5px coral top, 48px icon square,
Bebas title, Inter body, coral stat). **Accent** the three coral top borders + icon squares.
**Silence** tight — the density exception. **Fixed** 5px coral top as sole chrome, no shadow/radius.
**Free** the three cards' content. **Density** dense-exception.

### 6 · Timeline (process · move: horizontal rail · left)

**Ground** `{colors.cream}`, `pad-x`. **Composes** section-headline, timeline. **Focal** the ink
timeline-line with 4–5 coral nodes (cream halos) and Bebas labels. **Accent** coral nodes.
**Silence** moderate. **Fixed** ink line, coral nodes, cream halos. **Free** node count, labels.
**Density** standard.

## Composition Rules

### Do

- Compose as **multi-surface region splits** — coral / ink / cream meeting at hard edges; the boundary is the layout.
- Set every Bebas element **uppercase + tracked** (2px standard, 4px hero, 12px jumbo); every Inter label uppercase, 1–4px.
- Render eyebrows **coral on cream/ink, ink on coral**; headlines ink on cream/coral, cream on ink.
- Apply the **45° hatch** (6% ink) on coral regions; fill underweight coral regions with a **12% wallpaper numeral**.
- Use the **5px coral top** (cards) / **4px coral left** (tiles) as the only chrome on those elements.
- Lean centered on cover sign-offs and catalog heads; left/panel-split on features and quotes.

### Don't

- Don't render Bebas in sentence case or untracked; don't pair it with a non-Inter body sans.
- Don't add a fourth surface, a drop shadow, an elevation, or a rounded rectangle.
- Don't put white headlines on coral (always ink) or gray headlines anywhere (gray is body/meta).
- Don't soften a region boundary with a gradient (except the rare 135° coral feature).
- Don't fill a coral region with sparse fragments — fully populate it or add a wallpaper numeral / giant mark.
- Don't blow a headline edge-to-edge — step the ramp down for long lines.

## Aspect-Ratio Behavior

| Treatment            | 16:9                       | 9:16                                 | 1:1                  |
| -------------------- | -------------------------- | ------------------------------------ | -------------------- |
| Region-Split Cover   | 38/62 rows, title left     | taller coral band, title below       | 40/60, title lower   |
| Feature Stat         | figure left, numeral right | figure top, numeral behind           | centered figure      |
| Quote Layout         | 40/60 coral+ink            | stacked: coral mark top, quote below | stacked              |
| Closing Plate        | cream + bottom coral band  | cream + taller band                  | centered, band below |
| Three-Column Catalog | head over 3-up             | head top, 3 stacked                  | head top, 2+1        |
| Timeline             | horizontal rail            | vertical rail                        | compact horizontal   |

Safe area holds the `5cqw` padding on the short edge; re-step display per ratio so no load-bearing
line drops below the 1.4cqw floor. Bebas runs ~20% wider in CJK — adjust line breaks per ratio.

## Approved Entities

No real customers, logos, or vendors are defined in the source — render any such mark as a
placeholder. The system supplies surfaces and geometry, not brands.

## Numerals & Claims (hard rule)

Never invent figures, stats, dates, or counts at frame scale. Render slots as `— figure —`,
`{metric}`, `N×`. Real numerals appear only when the script supplies them — the feature stat,
catalog, and timeline especially carry placeholders, not fabricated values. Wallpaper numerals
(01, 02…) are decorative and may be ordinal.

## Pre-Render Self-Audit

- **Squint** — one focal element per region dominates at 3–5× its neighbor.
- **Silence** — sparse frames 40–55% empty; only the catalog runs dense.
- **Surfaces** — two or three of coral/ink/cream, meeting at hard edges; no fourth surface.
- **Type** — Bebas uppercase + tracked, fit-to-measure; ink-on-coral; eyebrow color correct for surface; ≥1.4cqw floor.
- **Depth** — 0 shadow, 0 rounded rectangle; hatch + wallpaper carry texture.
- **Anchor** — centered on sign-offs/heads, panel/left on features/quotes; no 3 consecutive frames share an anchor.
- **Fabrication** — every numeral traces to the script, else placeholder.

## Known Gaps

- **Motion intentionally out of scope.** frame.md specifies composition only; timing and transitions are a later stage. The 0.6s opacity fade in the source is a deck mechanic, not a frame spec.
- **Bebas Neue + Inter via Google Fonts.** CJK pairing (ZCOOL XiaoWei / Yozai) carries over from the source's CJK section; Bebas runs ~20% wider in CJK.
- **9:16 / 1:1 are guidance**, not pixel-locked; verify the legibility floor per ratio.
- The 45° hatch, wallpaper numerals, giant marks, and timeline dash are CSS-only; no external imagery is required.


<!-- ===== FILE: hyperframes/hyperframes-creative/frame-presets/creative-mode/FRAME.md ===== -->

---
version: alpha
name: Creative Mode — Frame (video / frame layer)
description: >
  Video-first companion to Creative Mode's design.md. The unit is the frame (1920×1080),
  not the slide-in-a-deck. Atoms are identical and sacred — warm cream canvas, 4px ink
  borders, hard offset shadows (no blur), Archivo Black uppercase at 0.92 line-height,
  JetBrains Mono taxonomy, Space Grotesk body, the four-accent palette. Composition,
  frame scale, and aspect-ratio behavior are rewritten for the frame. Motion is out of scope.
unit: the frame — 1920×1080 primary; 9:16 and 1:1 documented
principle: atoms are sacred · composition is free · numbers come from the script

colors:
  cream: "#EFE9D9"
  cream-2: "#E4DCC4"
  ink: "#0F0F0F"
  ink-2: "#2A2A2A"
  green: "#1F8A4C"
  green-dark: "#136636"
  pink: "#F06CA8"
  pink-dark: "#D14E8B"
  orange: "#E85A1F"
  yellow: "#F5C518"

typography:
  # — reading ramp (px @ 1920, with cqw) —
  body-lg:    { fontFamily: "Space Grotesk", px: 28, cqw: 1.46, weight: 400, lineHeight: 1.4 }
  body-md:    { fontFamily: "Space Grotesk", px: 24, cqw: 1.25, weight: 400, lineHeight: 1.3 }
  mono-label: { fontFamily: "JetBrains Mono", px: 24, cqw: 1.25, weight: 400, tracking: "0.06em", upper: true }
  mono-kicker:{ fontFamily: "JetBrains Mono", px: 24, cqw: 1.25, weight: 400, tracking: "0.14em", upper: true }
  table-head: { fontFamily: "Archivo Black", px: 28, cqw: 1.46, weight: 400, upper: true }
  # — display / hero ramp (frame-native, cqw-first) —
  step-title: { fontFamily: "Archivo Black", px: 34,  cqw: 1.77, weight: 400, lineHeight: 1.0, upper: true }
  badge-label:{ fontFamily: "Archivo Black", px: 28,  cqw: 1.46, weight: 400, upper: true }
  marker:     { fontFamily: "Archivo Black", cqw: 2.4, weight: 400, lineHeight: 1.0, upper: true }
  stamp-num:  { fontFamily: "Archivo Black", cqw: 2.2, weight: 400, lineHeight: 0.9 }
  stat-num:   { fontFamily: "Archivo Black", cqw: 6.4, weight: 400, lineHeight: 0.88 }
  step-num:   { fontFamily: "Archivo Black", cqw: 7.0, weight: 400, lineHeight: 0.85 }
  display-head: { fontFamily: "Archivo Black", cqw: 4.2, weight: 400, lineHeight: 0.92, tracking: "-0.01em", upper: true }
  display-lg: { fontFamily: "Archivo Black", cqw: 8.0,  weight: 400, lineHeight: 0.9,  tracking: "-0.01em", upper: true }
  display-xl: { fontFamily: "Archivo Black", cqw: 11.0, weight: 400, lineHeight: 0.9,  tracking: "-0.01em", upper: true }
  display-hero:{ fontFamily: "Archivo Black", cqw: 15.5,weight: 400, lineHeight: 0.84, tracking: "-0.02em", upper: true }

spacing:
  frame-pad: "3.3cqw"        # 64px chrome gutter @1920
  content-gutter: "5cqw"     # 96px content gutter @1920
  grid-gap: "1.5cqw"         # 28px
  cell-pad: "1.7cqw"         # 32px

components:
  frame-chrome:
    typography: "{typography.mono-label}"
    placement: "topbar 2.5cqw from top, meta 2.5cqw from bottom, both inset {spacing.frame-pad}"
    rounded: "0"
    shadow: "none"
    description: "Mono topbar (section label left + 999px ink-stroked pill right) + meta footer (descriptor left + NN • NN counter right, 0.5cqw ink dot divider). Present on most frames."
  stat-cell:
    backgroundColor: "{colors.green} · {colors.pink} · {colors.orange} · {colors.cream}"
    textColor: "{colors.cream} on accent · {colors.ink} on cream"
    border: "0.4cqw solid {colors.ink}"
    rounded: "0"
    padding: "{spacing.cell-pad}"
    typography: "{typography.stat-num} + {typography.mono-label}"
    shadow: "none"
    description: "Flat accent/cream stat tile, square corners, no shadow."
  step-card:
    backgroundColor: "{colors.cream} · {colors.pink} · {colors.yellow} · {colors.green}"
    border: "0.4cqw solid {colors.ink}"
    rounded: "0"
    padding: "{spacing.cell-pad}"
    typography: "{typography.step-num} + {typography.step-title} + {typography.body-md}"
    shadow: "none"
    description: "Ink-bordered card; giant step-num top. Sequence alternates cream with accents and ENDS on green."
  marker-block:
    backgroundColor: "{colors.pink}"
    textColor: "{colors.ink}"
    border: "0.4cqw solid {colors.ink}"
    rounded: "0"
    typography: "{typography.marker}"
    shadow: "1.25cqw 1.25cqw 0 {colors.orange}, 1.25cqw 1.25cqw 0 0.2cqw {colors.ink}"
    description: "The one hard-offset featured callout per frame."
  kicker-block:
    backgroundColor: "{colors.ink}"
    textColor: "{colors.cream}"
    typography: "{typography.mono-kicker}"
    padding: "0.5cqw 1cqw"
    rounded: "0"
    description: "Inverted eyebrow chip."
  badge-rotated:
    backgroundColor: "{colors.yellow}"
    border: "0.4cqw solid {colors.ink}"
    typography: "{typography.badge-label}"
    rounded: "0"
    transform: "rotate(-4deg)"
    description: "Deliberate-imperfection annotation."
  pill-badge:
    backgroundColor: "{colors.cream}"
    border: "0.2cqw solid {colors.ink}"
    rounded: "999px"
    typography: "{typography.mono-label}"
    description: "The ONLY rounded element; reads as a chip, not a card."
  stamp:
    backgroundColor: "{colors.pink}"
    border: "0.4cqw solid {colors.cream}"
    size: "~18cqw square"
    rounded: "0"
    transform: "rotate(-6deg)"
    typography: "{typography.stamp-num}"
    description: "Closing seal with a cream circular inner ring."
  comparison-table:
    backgroundColor: "{colors.cream-2}"
    border: "0.4cqw solid {colors.ink}"
    rule: "0.3cqw solid {colors.ink}"
    rounded: "0"
    typography: "{typography.table-head} + {typography.body-md}"
    shadow: "none"
    description: "Ink head row with cream Archivo labels; pink/green column-fill variants."
  decorative-circle:
    backgroundColor: "{colors.yellow}"
    border: "0.4cqw solid {colors.ink}"
    rounded: "50%"
    description: "Decorative figure; pairs with a green panel for shape contrast."
---

# Creative Mode — Frame (video / frame layer)

## Overview

Creative Mode at frame scale is a **neo-brutalist editorial poster in motion's clothing** — warm
cream paper, near-black ink, and four accents that collide at full saturation. Every frame is one
flat color-blocked composition: no gradients, no blurred shadows, no rounded cards (save the one
pill chip). Depth is **hard offset shadow** (a solid same-direction duplicate) or **color-block
contrast**, never light.

The display voice is **Archivo Black in strict uppercase at 0.92 line-height** — letters overlap
their own cap height; that tightness is the brand. **JetBrains Mono** carries every label, kicker,
counter, and axis as a "technical artifact" register. **Space Grotesk** carries the few body lines.
The frame is loud by construction and calm by restraint: two or three accents per frame, the green
ground reserved for a single closing plate, the hard shadow spent on one featured element only.

**Key characteristics at frame scale:**

- **Cream ground** (`{colors.cream}`) on nearly every frame; `{colors.green}` reserved for the closing plate.
- **0.4cqw (4px @1920) ink borders** on every structural element; 0.3cqw internal rules.
- **Hard offset shadow** (≈1.25cqw, orange+ink) on one featured block per frame — never blurred.
- **Archivo Black uppercase**, 0.92 line-height, always; sentence-case Archivo Black does not exist.
- **Two or three accents per frame**, never all four; collisions are the design.
- **One pill chip** (999px) per frame as the sole rounded element.

### Frame Craft Bar

Three eyeball tests gate every frame before any structural check:

- **Squint** — exactly one element dominates, at **3–6× its nearest neighbor** (a chasm, not a ramp): the `display-hero`/`display-xl` claim or the `stat-num` figure, never two rival headlines.
- **Silence** — sparse frames (cover, claim, closer) read **45–60% empty**; the **stat grid and comparison ledger are the one dense exception**. Never fill a sparse frame to look complete.
- **Restraint** — the scarce gestures fire **once per frame**: at most one hard-offset shadow, two-to-three accents (never all four), the green ground reserved for the single closing plate.
- **Reference** — aim at a **Risograph editorial poster / punk-zine spread** (flat ink-bordered blocks, one big claim, vast cream); failure looks like a **rounded, soft-shadowed SaaS feature grid**.

## The Frame

- **Primary:** 1920×1080 (16:9). All display sizes authored in **`cqw`** (`px ÷ 1920 × 100 = cqw`).
- **Vertical:** 1080×1920 (9:16). **Square:** 1080×1080 (1:1).
- **Safe area:** chrome at `3.3cqw` (64px) inset; content at `5cqw` (96px) gutter. No load-bearing element crosses the `3.3cqw` line.

**The container law (load-bearing).** Every frame ground sets `container-type: size`. ALL
frame-relative units are `cqw`/`cqh` (1cqw = 1% of the frame's width), resolved against that
ground — **never `vw`.** `vw` measures the page viewport, so a frame inflates whenever it isn't
rendered full-screen; `cqw` resolves against the frame at any render size. This is why every size
in the display ramp is `cqw`.

## Colors

Tokens identical to the source. At frame scale: `{colors.cream}` is the **ground**, `{colors.ink}`
is borders + type, and the four accents (`green` / `pink` / `orange` / `yellow`) are **flat fills
rationed two-to-three per frame.** `{colors.orange}` is also the hard-shadow color. `{colors.green}`
doubles as the single closing-plate ground — its rarity is the impact. Never introduce a fifth
accent; never use pure white; never gradient.

## Typography

Two ramps. The **reading ramp** (body, mono labels, table heads) holds px+cqw for chrome and copy.
The **display/hero ramp** is frame-native and authored in `cqw` — from `display-head` (4.2cqw) up
to `display-hero` (15.5cqw) for a wordmark cover.

- **Legibility floor:** any load-bearing line ≥ **1.4cqw (≈27px@1920)**. Mono chrome at 1.15cqw is colophon only.
- **Fit-to-measure:** a headline's size tracks its line length. Cap the headline block at **≤ 78cqw** and never touch the safe margin. ≤3 words → `display-hero`/`display-xl`; 4–6 words → `display-lg`; 7+ words → `display-head`. Short lines go big; long lines step down.
- **Uppercase + 0.92 line-height on all Archivo Black**, always. Mono carries 0.06–0.14em tracking. Never letter-space Archivo Black beyond the encoded −0.01em; never set body centered.

## Depth & Surface

Zero blur. Two depth devices only:

- **Hard offset shadow** — a solid duplicate offset ≈1.25cqw in X and Y (`box-shadow: 1.25cqw 1.25cqw 0 {colors.orange}, 1.25cqw 1.25cqw 0 0.2cqw {colors.ink}`). **One featured block per frame** (marker, stamp). Diagram stacks may use a 0.95cqw ink-only offset.
- **Color-block contrast** — cream on cream-2, ink on cream, accent on cream. No shadow needed when contrast carries.

**Ceiling:** no blurred shadow, no gradient, no glow, anywhere.

## Shapes

- **0 radius** on every structural element — stat cells, step cards, table cells, markers, panels.
- **50%** on decorative circles, stamp inner ring, the meta dot.
- **999px** on the topbar pill chip only — the single rounded exception.
- **Rotation** only at the fixed brand angles: badge −4deg, stamp −6deg.

## Components

- **frame-chrome** — the mono topbar + meta footer. Present on most frames; dropped only on a pure full-bleed wordmark beat if it competes.
- **stat-cell / step-card** — ink-bordered flat-fill blocks; step sequences end on green.
- **marker-block** — the one hard-shadow featured callout per frame.
- **kicker-block** — inverted ink eyebrow chip; **badge-rotated** — −4deg yellow annotation; **pill-badge** — the lone rounded chip.
- **stamp** — the −6deg closing seal. **comparison-table** — cream-2 ledger with ink head row.
- **decorative-circle** — yellow disc for shape contrast against a green panel.

## Frame Treatments

> Recipe per plate: ground · container · composes · focal · chrome · accent · silence · Fixed/Free · density.
> Authored at 1920×1080. Lean centered; vary the anchor; one idea per frame.

### 1 · Wordmark Cover (identity · move: full-frame lockup · centered)

**Ground** `{colors.cream}`, `frame-pad`. **Container** grid, chrome top/bottom, focal centered.
**Composes** frame-chrome, the wordmark. **Focal** the two-line wordmark at `display-hero`
(15.5cqw), centered, second line in an accent (`{colors.pink}`/`orange`). **Chrome** mono topbar
(section label + pill) and meta footer (descriptor + 01•NN). **Accent** the second-line color only;
optionally one corner decorative-circle bleeding off an edge. **Silence** ~55% empty cream.
**Fixed** Archivo Black uppercase 0.84 lh, one accent on the wordmark, square corners. **Free** which
accent, line break, whether a circle bleeds a corner. **Density** sparse.

### 2 · Big Claim (oversized statement · move: scale · left)

**Ground** one full-bleed accent (`{colors.pink}`/`green`/`orange`), `content-gutter`. **Container**
flex, claim left-anchored and vertically centered. **Composes** kicker-block, the claim. **Focal**
a 2–3 line claim at `display-xl`/`display-lg`, ink on the accent (ink-on-fire — never white).
**Chrome** small ink kicker-block above the claim; mono meta footer. **Accent** the ground IS the
accent; no second accent competes. **Silence** ~45% of the colored field empty. **Fixed** ink type
on accent, fit-to-measure sizing, no shadow on type. **Free** the claim, which accent ground, which
word breaks. **Density** sparse — one idea.

### 3 · Stat Grid (catalog · move: density — the one dense frame · centered)

**Ground** `{colors.cream}`, `content-gutter`. **Container** grid: a centered `display-head` over a
3-up row of stat-cells. **Composes** frame-chrome, 3× stat-cell. **Focal** the row of three
ink-bordered cells (green / pink / orange), each a `stat-num` + mono label. **Chrome** mono topbar +
meta. **Accent** the three cell fills (the named density exception — three accents allowed here).
**Silence** ~25% — tight by design. **Fixed** 0.4cqw borders, square corners, no per-cell shadow,
mono labels. **Free** the three figures+labels, head copy, which three accents. **Density** dense-exception.

### 4 · Closing Plate (closer · move: ground-swap · centered)

**Ground** `{colors.green}` (the single green frame of the run), `frame-pad`. **Focal** a 2-line
sign-off at `display-lg` in `{colors.cream}`, centered. **Composes** frame-chrome (cream variant),
stamp. **Chrome** cream mono topbar + meta. **Accent** one `{colors.pink}` stamp rotated −6deg in
a corner, cream ring + stamp-num. **Silence** ~55% empty green. **Fixed** green ground reserved to
this beat, cream-on-green type, one stamp. **Free** sign-off copy, stamp text, stamp corner. **Density** sparse.

### 5 · Featured Marker (callout · move: hard-shadow focal · left/asymmetric)

**Ground** `{colors.cream}`. **Composes** frame-chrome, marker-block, optional body-md support line.
**Focal** the pink marker-block with the signature orange+ink hard offset shadow, set asymmetrically.
**Accent** pink block + orange shadow (two accents). **Silence** ~50%. **Fixed** exactly one hard
shadow on the frame, 0.4cqw borders. **Free** marker copy, block position, optional support line.
**Density** sparse.

### 6 · Comparison Ledger (data · move: matrix · left)

**Ground** `{colors.cream}`, `content-gutter`. **Composes** frame-chrome, comparison-table.
**Focal** the cream-2 table with ink head row; one column fill (pink or green) marks the winner.
**Accent** the single column fill. **Silence** tight — the second density exception. **Fixed**
cream-2 fill, 0.3cqw internal rules, ink head row with cream Archivo labels. **Free** rows, which
column fills, copy. **Density** dense-exception.

## Composition Rules

### Do

- Compose around **one idea per frame**, focal element **3–5× its neighbors** (squint test).
- **Lean centered** — cover, claim, stat grid, and closer all center their focal element; reserve left/asymmetric for the marker and ledger.
- Keep sparse frames **45–60% empty**; only the stat grid and ledger run dense.
- Use **two or three accents per frame**; reserve `{colors.green}` ground for the closing plate.
- Spend the hard offset shadow on **one featured block per frame**.
- Size headlines **fit-to-measure**; render Archivo Black uppercase at 0.92 lh.

### Don't

- Don't round corners (except the pill chip); don't gradient, blur, or glow.
- Don't set Archivo Black in sentence case or letter-space it beyond −0.01em.
- Don't use all four accents on one frame, a fifth accent, or pure white.
- Don't center body copy or set labels in anything but JetBrains Mono.
- Don't blow a headline edge-to-edge — step the ramp down for long lines.
- Don't put two hard shadows on one frame.

## Aspect-Ratio Behavior

| Treatment         | 16:9                            | 9:16                         | 1:1                      |
| ----------------- | ------------------------------- | ---------------------------- | ------------------------ |
| Wordmark Cover    | two lines centered              | stacked taller, circle top   | centered, tighter        |
| Big Claim         | claim left, full accent         | claim top, accent full       | claim centered           |
| Stat Grid         | head over 3-up row              | head top, 3 stacked          | head top, 2×2 (4th cell) |
| Closing Plate     | sign-off centered, stamp corner | stacked, stamp below         | centered, stamp corner   |
| Featured Marker   | marker asymmetric               | marker centered, shadow down | marker centered          |
| Comparison Ledger | full-width table                | table scrolls to fewer cols  | 2-col table              |

Safe area holds the `3.3cqw` chrome inset on the short edge for every ratio; re-step display per
ratio so no load-bearing line drops below the 1.4cqw floor.

## Approved Entities

No real customers, logos, or vendors are defined in the source — render any such mark as a
placeholder. Products/sections are content-agnostic; the system supplies geometry, not brands.

## Numerals & Claims (hard rule)

Never invent figures, percentages, counts, or dates at frame scale. Render data slots as
`— figure —`, `{metric}`, `N×`. Real numerals appear only when the script supplies them — the stat
grid and ledger especially carry placeholders, not fabricated values.

## Pre-Render Self-Audit

- **Squint** — one element dominates at 3–5× its neighbor, else rescale.
- **Silence** — sparse frames 45–60% empty; only stat grid / ledger run dense.
- **Accents** — two or three per frame, never all four; green ground only on the closer.
- **Depth** — 0 blur; at most one hard offset shadow; color-block contrast otherwise.
- **Geometry** — square corners except the pill; rotation only at −4/−6deg.
- **Type** — Archivo Black uppercase 0.92 lh, fit-to-measure, ≥1.4cqw on load-bearing lines.
- **Anchor** — centered default; left/asymmetric only on marker + ledger; no 3 consecutive frames share an anchor.
- **Fabrication** — every numeral traces to the script, else placeholder.

## Known Gaps

- **Motion intentionally out of scope.** frame.md specifies composition only; timing and transitions are a later stage. The closing green is described as a _plate_, not a transition.
- **Archivo Black requires Google Fonts**; fallback is `sans-serif`. CJK pairing (Noto Serif SC 900 / NSC 400) carries over from the source's CJK section.
- **9:16 / 1:1 are guidance**, not pixel-locked; verify the legibility floor per ratio.
- Decorative geometry (circle, stamp, stacked blocks) is CSS-only; no external imagery is required.


<!-- ===== FILE: hyperframes/hyperframes-creative/frame-presets/daisy-days/FRAME.md ===== -->

---
version: alpha
name: Daisy Days — Frame (video / frame layer)
description: >
  Video-first companion to Daisy Days' design.md. The unit is the frame (1920×1080). Atoms are
  identical and sacred — the sunny-garden pastel palette (cream + turquoise/pink/butter/mint/
  lavender/peach/sky + coral accent), charcoal 3px outlines, hard offset shadows (6/4px, no blur),
  the Fredoka + Quicksand pairing, generous radii, headline text-shadow on color, dot bullets, and
  the hand-drawn SVG ornament layer. Composition + frame scale rewritten. Motion out of scope.
unit: the frame — 1920×1080 primary; 9:16 and 1:1 documented
principle: atoms are sacred · composition is free · numbers come from the script

colors:
  cream: "#F5F0E6"
  turquoise: "#7ECDC0"
  soft-pink: "#F7C8D4"
  butter: "#FDE68A"
  mint: "#A8E6CF"
  lavender: "#D4A5E8"
  peach: "#FFCBA4"
  sky: "#A8D8F0"
  coral: "#F8635F"
  text-dark: "#2D2D2D"
  text-muted: "#6B6B6B"
  white: "#FFFFFF"

borders: { primary: "3px solid text-dark", thin: "2px solid text-dark" }
shadows: { default: "6px 6px 0 text-dark", small: "4px 4px 0 text-dark", text-headline: "3px 3px 0 text-dark", text-headline-soft: "3px 3px 0 rgba(0,0,0,0.2)" }

typography:
  # — reading ramp (Quicksand) —
  body:    { fontFamily: "Quicksand", cqw: 0.95, weight: 500, lineHeight: 1.6 }
  body-strong:{ fontFamily: "Quicksand", cqw: 0.95, weight: 600, lineHeight: 1.5 }
  meta:    { fontFamily: "Quicksand", cqw: 0.78, weight: 600, lineHeight: 1.45 }
  # — display ramp (Fredoka One / Fredoka 600 — single weight, never italic) —
  badge:   { fontFamily: "Fredoka One", cqw: 0.9, tracking: "0.02em" }
  label-display:{ fontFamily: "Fredoka One", cqw: 1.3, lineHeight: 1.3, tracking: "0.02em" }
  subtitle:{ fontFamily: "Fredoka One", cqw: 1.8, lineHeight: 1.2, tracking: "0.02em" }
  quote:   { fontFamily: "Fredoka One", cqw: 2.6, lineHeight: 1.35 }
  title:   { fontFamily: "Fredoka One", cqw: 3.0, lineHeight: 1.15, tracking: "0.02em" }
  headline:{ fontFamily: "Fredoka One", cqw: 4.5, lineHeight: 1.1, tracking: "0.02em" }
  display: { fontFamily: "Fredoka One", cqw: 6.5, lineHeight: 1.1, tracking: "0.02em" }

spacing:
  pad-slide: "3cqw"
  radius: "20px"
  radius-lg: "28px"
  radius-pill: "50px"
  radius-round: "50%"

components:
  card:
    backgroundColor: "{colors.white}"
    border: "3px solid {colors.text-dark}"
    rounded: "{spacing.radius} (28px featured)"
    shadow: "6px 6px 0 {colors.text-dark}"
    description: "The universal container; white-on-pastel is standard."
  framed-header:
    backgroundColor: "pastel cap + {colors.white} body"
    border: "3px solid {colors.text-dark} (one continuous)"
    rounded: "{spacing.radius-lg}"
    shadow: "6px 6px 0 {colors.text-dark}"
    description: "Pastel header strip flush above a white body — one unit, one shadow."
  badge-pill:
    backgroundColor: "{colors.butter}"
    border: "3px solid {colors.text-dark}"
    rounded: "{spacing.radius-pill}"
    typography: "{typography.badge}"
    shadow: "4px 4px 0 {colors.text-dark}"
    description: "Section tag. white-space:nowrap."
  circle-marker:
    backgroundColor: "any pastel"
    textColor: "{colors.white} (dark on butter)"
    border: "3px solid {colors.text-dark}"
    rounded: "50%"
    size: "bullet 20 / icon 44 / dot 48 / step 90"
    typography: "Fredoka numeral"
    description: "Steps carry a small shadow."
  bullet-dot:
    backgroundColor: "{colors.butter}"
    border: "2px solid {colors.text-dark}"
    rounded: "50%"
    size: "20px (::before, 4px from line top)"
    description: "Lists never use glyph bullets."
  ornament:
    type: "hand-drawn SVG (daisy, star, sun, cloud, rainbow)"
    stroke: "2.1px {colors.text-dark}"
    placement: "z-index:1 behind content (z-index:2), cropping past the frame edge"
    description: "3–7 per frame, clustered at corners/edges."
  quote-mark:
    typography: "oversized Fredoka quote glyph"
    color: "{colors.soft-pink} (charcoal stroke)"
    description: "Above a quote body."
  text-headline-shadow:
    shadow: "3px 3px 0 {colors.text-dark} (soft 20% variant on pink/mint)"
    appliesTo: "Fredoka headlines on saturated surfaces (cream headlines sit flat)"
    description: "Makes the headline read 'outlined' like the shapes."
---

# Daisy Days — Frame (video / frame layer)

## Overview

Daisy Days at frame scale is a **cheerful, childlike system** — picture-book illustration meets
sticker-sheet kawaii. Every shape carries a **3px charcoal outline**, every elevated element a
**solid hard offset shadow** (no blur), every surface a sunny-garden pastel. The voice is one
pairing: **Fredoka One** (chunky rounded, single weight) for every headline, **Quicksand** for
every body and meta line. The signature is the **hand-drawn SVG ornament layer** — daisies, stars,
suns, clouds, rainbows clustering at corners and cropping past the edge.

The palette is **multi-pastel with one warm pop**: cream canvas, seven pastel surfaces, and
`{colors.coral}` reserved for small high-attention markers only. Headlines on a saturated surface
get a 3px charcoal text-shadow (so they read "outlined" like the shapes) and switch to white;
headlines on cream sit flat in charcoal. Depth is 2D and graphic — thick outline + hard offset =
sticker-on-paper.

**Key characteristics at frame scale:**

- **Cream default + rotating pastel surfaces**; `{colors.coral}` is a marker accent, never a surface.
- **Fredoka One** headlines + **Quicksand 500/600** body — strict by role, never crossed.
- **3px charcoal outline + hard offset shadow** (6/4px, zero blur) on every elevated shape.
- **Generous radii** — 20px cards, 28px featured, pill badges, full-circle markers; no square corners.
- **Headline text-shadow on saturated surfaces** (white text); flat charcoal on cream.
- **Dot bullets** (outlined butter discs, never glyphs) + a **3–7 ornament wreath** per frame.

## The Frame

### Frame Craft Bar

Three eyeball tests gate every frame before any structural check:

- **Squint** — one Fredoka headline or content card dominates at 3–6× its neighbor.
- **Silence** — **one content container per frame** surrounded by an ornament wreath; the **info-card grid is the one dense exception**. Empty corners read as broken.
- **Restraint** — cream or **one** pastel surface; coral is a small-marker accent (never a surface); charcoal borders + hard offset shadows only; no ninth color.
- **Reference** — aim at a **children's picture-book / sticker-sheet kawaii zine**; failure looks like a **flat, square-cornered, blurred-shadow corporate slide**.

- **Primary:** 1920×1080 (16:9). Display authored in **`cqw`** (`px ÷ 1920 × 100 = cqw`).
- **Vertical:** 1080×1920 (9:16). **Square:** 1080×1080 (1:1).
- **Safe area:** `pad-slide` ~3cqw; ornaments deliberately bleed past the edge.

**The container law (load-bearing).** Every frame ground sets `container-type: size`; ALL
frame-relative units are `cqw`/`cqh` against it — never `vw`. Borders stay 3px/2px; radii stay
20/28/50px; shadow offsets scale in `cqw` so the sticker offset holds proportionally.

## Colors

Tokens identical to the source. Default ground `{colors.cream}`; rotate saturated pastels
(turquoise / soft-pink / butter / mint / lavender / peach / sky) for tonal mood. **Cards are white**
on any surface. **Borders + shadows are always `{colors.text-dark}` charcoal** — never colored,
never blurred, never `rgba` (save the soft text-shadow variant). `{colors.coral}` is the lone
high-saturation accent — small markers (step circles, dots, headers) **only**, never a surface.
Body is charcoal/muted; pastels carry **no semantic meaning**. No ninth color.

## Typography

Two ramps. The **reading ramp** (Quicksand 500 body 0.95cqw, 600 emphasis, meta) carries copy; the
**display ramp** (Fredoka One `label-display` 1.3cqw → `display` 6.5cqw, single weight) carries
every headline, title, quote, and marker numeral.

- **Legibility floor:** any load-bearing line ≥ **1.4cqw**; meta is chrome only.
- **Fit-to-measure:** size the headline to its length. Cap the block at **≤ 78cqw**; ≤3 words → `display`; 4–6 → `headline`; 7+ → `title`.
- **Fredoka One for all display, Quicksand for all body — never crossed.** Fredoka is single-weight (no italic, no underline, no alt weights); Quicksand stays 500/600/700. Fredoka tracking 0.02em; Quicksand body never uppercase.

## Depth & Surface

2D graphic depth — hard offset shadow, solid charcoal, zero blur, bottom-right:

- **`shadows.default` 6px** cards, frames, badges, chart containers.
- **`shadows.small` 4px** small cards, step circles, avatars.
- **Text-headline shadow** — 3px charcoal on Fredoka headlines over saturated surfaces (20% soft variant on pink/mint); cream headlines flat.
- **Outline + offset** together are the sticker-on-paper signature.

**Ceiling:** no blurred shadow, no `rgba` (except the soft text-shadow), no gradient, no glow; an element either casts a hard charcoal offset or none.

## Shapes

- **20px** cards, **28px** featured, **50px** pill (badges, counter), **50%** all circles, **4px** legend swatch. Zero square corners — every region is rounded.

## Components

- **card / framed-header** — the white-fill bordered containers (one shadow). **badge-pill** — butter section tag.
- **circle-marker** family (bullet 20 / icon 44 / dot 48 / step 90) + **bullet-dot** — outlined pastel discs, Fredoka numerals.
- **ornament** — the hand-drawn SVG sticker layer (3–7 per frame). **quote-mark** — soft-pink Fredoka anchor. **text-headline-shadow** — the on-color headline treatment.

## Frame Treatments

> Recipe: ground · container · composes · focal · chrome · accent · silence · Fixed/Free · density.
> One content container per frame + a 3–7 ornament wreath; empty corners read as broken.

### 1 · Cover (identity · move: ornament wreath · saturated · centered)

**Ground** a saturated pastel (e.g. `{colors.turquoise}`). **Composes** badge-pill, display, body sub, 3–7 ornaments, counter. **Focal** a 1–2 line Fredoka `display` in **white with the 3px charcoal text-shadow**, centered, under a butter badge-pill. **Chrome** counter pill. **Accent** the ornament wreath (daisies + stars at corners, cropping past edges). **Silence** content centered; ornaments fill the edges. **Fixed** text-shadow on color, 3px outlines, charcoal shadows. **Free** surface color, ornament mix/positions, copy. **Density** full-but-not-crowded.

### 2 · Info Cards (catalog · move: 3-up white cards · cream · the dense frame)

**Ground** `{colors.cream}`, `pad-slide`. **Composes** headline (flat charcoal), 3× card (circle-icon + Fredoka title + Quicksand body), a couple ornaments. **Focal** three white 3px-bordered cards with 6px shadows. **Chrome** flat headline. **Accent** the pastel circle-icons (rotate turquoise/coral/lavender). **Silence** tight — the density exception (fewer ornaments here). **Fixed** white cards, 3px + 6px, 20px radius. **Free** card content, icon hues. **Density** dense-exception.

### 3 · Process Steps (sequence · move: rotating circle markers · peach · centered)

**Ground** `{colors.peach}` (or another pastel). **Composes** headline (white + text-shadow), 3–4 step circles + `→` arrows, ornaments. **Focal** a row of 90px outlined step circles, fills **rotating coral → mint → sky → lavender**, Fredoka white numerals, linked by Fredoka arrows. **Chrome** white headline with text-shadow. **Accent** the rotating circle fills. **Silence** moderate. **Fixed** 3px circles + small shadow, rotating fills, arrow glyphs. **Free** step count, labels. **Density** standard.

### 4 · Quote (quote · move: quote-mark anchor · soft-pink · centered)

**Ground** `{colors.soft-pink}`. **Composes** a white quote card (28px radius, 6px shadow), quote-mark, Fredoka quote, Quicksand attribution, ornaments. **Focal** a Fredoka `quote` in charcoal inside the white card, under an oversized soft-pink quote-mark. **Chrome** Quicksand 700 attribution. **Accent** the quote-mark + a star or two. **Silence** card centered, ornaments at corners. **Fixed** quote-mark anchor, white card. **Free** quote, attribution. **Density** moderate.

### 5 · Framed Section (feature · move: cap+body card · cream)

**Ground** `{colors.cream}`. **Composes** framed-header (pastel cap + white body), bullet-dot list, ornaments. **Focal** a framed-header — a pastel cap strip (Fredoka title, optional text-shadow) above a white body with a butter-dot bullet list. **Accent** the cap color + bullet dots. **Silence** moderate. **Fixed** one continuous 3px border + one shadow, butter dot bullets. **Free** cap color, list. **Density** standard.

### 6 · Closing (closer · move: ornament wreath · saturated · centered)

**Ground** a saturated pastel (e.g. `{colors.lavender}`). **Composes** badge-pill, display (white + text-shadow), 3–7 ornaments. **Focal** a Fredoka `display` sign-off in white with the charcoal text-shadow, centered. **Accent** the ornament wreath. **Silence** content centered. **Fixed** text-shadow on color, ornaments fill corners. **Free** sign-off, surface, ornaments. **Density** full.

## Composition Rules

### Do

- Pair **Fredoka One headlines + Quicksand body** strictly by role.
- Outline every shape **3px charcoal + a hard offset shadow** (6/4px, no blur); white card fills on any surface.
- Give Fredoka headlines on **saturated surfaces a 3px charcoal text-shadow + white text**; flat charcoal on cream.
- Use **outlined butter-disc bullets** (never glyphs); cluster **3–7 hand-drawn ornaments** per frame (corners, cropping past edges).
- Keep **one content container per frame**; rotate marker colors (coral → mint → sky → lavender → butter); reserve coral for small markers.
- Center most frames; lean cream for content-dense frames, saturated for cover/closer/quote.

### Don't

- No square corners; no blurred or `rgba` shadows (save the soft text-shadow).
- No colored borders (charcoal only); no coral surface; no ninth color.
- No third font; no Quicksand headline or Fredoka body; no italic/underline Fredoka; no uppercase Quicksand body.
- No glyph bullets; no empty corners (ornaments fill them); no two competing content panels.
- Don't blow a headline edge-to-edge — fit to measure.

## Aspect-Ratio Behavior

| Treatment      | 16:9                       | 9:16                             | 1:1        |
| -------------- | -------------------------- | -------------------------------- | ---------- |
| Cover          | centered, corner ornaments | centered, taller, more ornaments | centered   |
| Info Cards     | 3 across                   | stacked                          | 2+1        |
| Process Steps  | horizontal + arrows        | vertical, arrows rotate down     | 2×2        |
| Quote          | centered card              | centered, taller                 | centered   |
| Framed Section | cap + body                 | cap + body taller                | cap + body |
| Closing        | centered, wreath           | centered, wreath                 | centered   |

`pad-slide` holds on the short edge; re-step display above the 1.4cqw floor. On tighter ratios keep
the ornament count toward the upper end (5–7) so corners never read empty.

## Approved Real Entities

No real customers, logos, or vendors are defined in the source — render any such mark as a
placeholder. Ornaments and pastels are content-agnostic; counters/badges carry per-deck text.

## Numerals & Claims (hard rule)

Never invent figures, dates, or counts at frame scale. Render slots as `— figure —`, `{metric}`,
`N`. Step numbers and any chart values carry placeholders until the script supplies them; the slide
counter is decorative chrome.

## Pre-Render Self-Audit

- **Squint** — one Fredoka headline or content card dominates per frame.
- **Silence** — one container per frame surrounded by an ornament wreath; only the info-card grid runs dense.
- **Color** — cream or one pastel surface; coral markers only; charcoal borders/shadows; no ninth hue.
- **Type** — Fredoka headlines (text-shadow + white on saturated, flat charcoal on cream), Quicksand body; ≥1.4cqw floor.
- **Depth** — 3px outline + hard offset (no blur, no rgba save soft text-shadow); rounded corners only.
- **Ornaments** — 3–7 per frame, cropping past edges; no empty corners. **Bullets** — outlined discs, never glyphs.
- **Fabrication** — every numeral traces to the script, else placeholder.

## Known Gaps

- **Motion intentionally out of scope.** frame.md specifies composition only; the source uses scroll-snap nav, no transition spec.
- **Fonts:** the source names _Fredoka One_; Google now serves the **Fredoka** variable family — request `Fredoka:wght@500;600;700` and set display weight 600 (visually equal to Fredoka One), with `Fredoka One` kept first in the stack for environments that still serve it. Quicksand loads normally. CJK: ZCOOL XiaoWei (display) / Yozai (body).
- **9:16 / 1:1 are guidance**; keep ornament count high so corners stay filled per ratio.
- Ornaments (daisy/star/sun/cloud/rainbow), markers, and framed headers are CSS/SVG-only; recoloring SVG ornaments requires editing their stroke values.
- **Contrast:** keep `{colors.text-muted}` off pastel surfaces (cream/white cards only); small text on saturated grounds should be charcoal or white.


<!-- ===== FILE: hyperframes/hyperframes-creative/frame-presets/editorial-forest/FRAME.md ===== -->

---
version: alpha
name: Editorial Forest — Frame (video / frame layer)
description: >
  Video-first companion to Editorial Forest's design.md. The unit is the frame (1920×1080). Atoms
  are identical and sacred — the green/pink/cream editorial triad, Source Serif 4 at weight 500
  (optical-size axis) for all display + JetBrains Mono 500 uppercase chrome, flat paper depth (no
  shadows), 2px hairline rules, 6/8px card radii, and the monogram circle stamp. Composition + frame
  scale rewritten. Motion out of scope.
unit: the frame — 1920×1080 primary; 9:16 and 1:1 documented
principle: atoms are sacred · composition is free · numbers come from the script

colors:
  green: "#2e4a2a"
  green-deep: "#243a21"
  green-lite: "#3a5a36"
  pink: "#e89cb1"
  pink-deep: "#d27e96"
  cream: "#efe7d4"
  cream-2: "#e6dcc4"
  ink: "#1a1a17"

typography:
  # — reading + chrome ramp —
  body:    { fontFamily: "Source Serif 4", cqw: 1.56, weight: 400, lineHeight: 1.38 }
  body-card:{ fontFamily: "Source Serif 4", cqw: 1.35, weight: 400, lineHeight: 1.34 }
  label:   { fontFamily: "JetBrains Mono", px: 26, cqw: 1.35, weight: 500, tracking: "0.18em", upper: true }
  caption-mono:{ fontFamily: "JetBrains Mono", px: 24, cqw: 1.25, weight: 500, tracking: "0.14em", upper: true }
  # — display ramp (Source Serif 4 weight 500, opsz, negative tracking) —
  title-card-sm:{ fontFamily: "Source Serif 4", cqw: 2.9, weight: 500, lineHeight: 0.98, tracking: "-0.01em" }
  title-card:{ fontFamily: "Source Serif 4", cqw: 3.5, weight: 500, lineHeight: 0.96, tracking: "-0.01em" }
  headline:{ fontFamily: "Source Serif 4", cqw: 4.4, weight: 500, lineHeight: 1.0, tracking: "-0.02em" }
  headline-xl:{ fontFamily: "Source Serif 4", cqw: 5.0, weight: 500, lineHeight: 0.96, tracking: "-0.02em" }
  display:{ fontFamily: "Source Serif 4", cqw: 7.3, weight: 500, lineHeight: 1.02, tracking: "-0.02em" }
  display-hero:{ fontFamily: "Source Serif 4", cqw: 11.5, weight: 500, lineHeight: 0.92, tracking: "-0.02em" }
  stat-figure:{ fontFamily: "Source Serif 4", cqw: 11.5, weight: 500, lineHeight: 0.92, tracking: "-0.03em" }
  stat-figure-unit:{ fontFamily: "Source Serif 4", cqw: 5.7, weight: 500, lineHeight: 0.92 }
  name:    { fontFamily: "Source Serif 4", cqw: 2.3, weight: 600, lineHeight: 1.0 }

spacing:
  slide-pad: "5cqw"
  rule: "2px"
  rule-card: "2.5px"
  radius-card: "6px"
  radius-step: "8px"

components:
  topbar:
    typography: "{typography.label} (JetBrains Mono) + monogram-circle or counter"
    placement: "top edge, label left, mark right"
    description: "On EVERY frame — the system's spine; a frame without it reads untreated."
  footline:
    typography: "{typography.caption-mono} ×2, space-between"
    placement: "absolute bottom edge"
    description: "On cover/data/summary frames."
  monogram-circle:
    border: "2px solid {colors.pink}"
    rounded: "50%"
    size: "130px"
    typography: "mono monogram"
    description: "The identity stamp. Cover/summary only."
  topic-tile:
    backgroundColor: "{colors.green} (pink text) / {colors.pink} (green-deep) / {colors.green-lite} (pink) / {colors.cream-2} + 2px {colors.green} border (green)"
    rounded: "{spacing.radius-card}"
    shadow: "none"
    typography: "{typography.caption-mono} ordinal + {typography.title-card-sm} + mono foot"
    description: "Fills rotate; never repeat one across a grid."
  step-tile:
    backgroundColor: "{colors.cream} + green border / {colors.green} / {colors.pink}"
    border: "2.5px solid"
    rounded: "{spacing.radius-step}"
    typography: "mono ordinal + {typography.title-card} + {typography.body-card} + mono marker over a top rule"
    description: "Framework/process card."
  kpi-block:
    typography: "{typography.caption-mono} tag → {typography.stat-figure} (+{typography.stat-figure-unit}) → {typography.body}"
    rule: "2px accent rule above"
    description: "Oversized serif figure."
  meta-dl:
    borderTop: "2px solid {colors.green}"
    typography: "{typography.caption-mono} dt + {typography.meta-value} dd"
    description: "3-column dt/dd grid."
  bar:
    backgroundColor: "{colors.pink} / {colors.cream} / {colors.green}"
    rounded: "3px 3px 0 0"
    size: "56px wide"
    typography: "mono value above"
    description: "Vertical chart bar."
  rule-thin:
    rule: "2px solid (green on cream / pink on green / green-deep on pink)"
    description: "The only separator. Never 1px, never 3px+."
---

# Editorial Forest — Frame (video / frame layer)

## Overview

Editorial Forest at frame scale is a **serif-led literary-editorial system** — the register of a
Penguin classic or a quiet annual report. One confident voice, **Source Serif 4 at weight 500**
(optical-size axis engaged), carries every headline and stat up to ~12cqw; **JetBrains Mono** at
weight 500 uppercase is the editorial chrome (labels, captions, axis ticks, footlines). Three
surfaces — forest green, dusty rose, oat cream — and nothing else. Depth is **flat and paper-based**:
no shadows, no gradients; elevation is color-block contrast + 2px hairlines + border-vs-fill.

The unmistakable signature is **weight 500** (never 400 display, never 700) and the **mono/serif
role inversion** (mono for chrome, serif for body and display). Body text drops to serif weight
400 — that 500→400 step is the reading rhythm. Every frame carries a mono topbar; the monogram
circle is the identity stamp.

**Key characteristics at frame scale:**

- **Green / pink / cream triad** — two surface tones per frame is typical, three is loud.
- **Source Serif 4 weight 500** (opsz, negative tracking) for all display; **serif 400** body; **JetBrains Mono 500** uppercase chrome.
- **Flat — no shadows, no gradients**; elevation is color-block + 2px hairline + border-vs-fill.
- **2px hairline rules** are the only separator (2.5px on step tiles); 6/8px card radii; the monogram circle is the only full round.
- **Topbar on every frame** (mono label + monogram/counter); footline on data/cover frames.
- **Spacious & committed** — one subject per frame in deep negative space; fewer elements at larger sizes.

## The Frame

### Frame Craft Bar

Three eyeball tests gate every frame before any structural check:

- **Squint** — one Source Serif 4 moment dominates at 3–6× its neighbor; the surface block centers the eye.
- **Silence** — one subject per frame in deep negative space; the **topic-tile and step grids are the one dense exception**.
- **Restraint** — **two surface tones max** per frame (three is loud); serif **weight 500** display / **400** body; green ground reserved for gravity moments.
- **Reference** — aim at a **Penguin classic / quiet annual report / art-book spread**; failure looks like a **shadowed, multi-color web dashboard**.

- **Primary:** 1920×1080 (16:9). Display authored in **`cqw`** (`px ÷ 1920 × 100 = cqw`).
- **Vertical:** 1080×1920 (9:16). **Square:** 1080×1080 (1:1).
- **Safe area:** `slide-pad` 5cqw (the source's generous 96–140px); the topbar/footline sit inside it.

**The container law (load-bearing).** Every frame ground sets `container-type: size`; ALL
frame-relative units are `cqw`/`cqh` against it — never `vw` (the source is a fixed 1920 canvas, so
its px map cleanly: `px ÷ 1920 × 100`). Hairlines stay 2px; card radii stay 6/8px.

## Colors

Tokens identical to the source. Default ground `{colors.cream}` for content; `{colors.green}` for
cover/statement/summary gravity. **Headlines:** green on cream, cream (or pink at hero scale) on
green, green-deep on pink. **Body:** ink on cream, cream on green, green-deep on pink. Labels/rules
take the region's accent (pink on green, green on cream, green-deep on pink). Tile fills rotate
green / pink / green-lite / cream-2-with-green-border. **No fourth color family** — the triad +
near-duplicates is the whole palette; never `rgba` transparency on a surface.

## Typography

Two ramps. The **reading/chrome ramp** (Source Serif 4 **400** body 1.56cqw; JetBrains Mono labels
in px) carries copy + chrome; the **display ramp** (Source Serif 4 **500** `title-card-sm` 2.9cqw →
`display-hero`/`stat-figure` 11.5cqw, opsz, negative-tracked) carries every headline + figure.

- **Legibility floor:** any load-bearing line ≥ **1.4cqw**; mono px labels are chrome only.
- **Fit-to-measure:** size the headline to its length. Cap the block at **≤ 78cqw**; ≤3 words → `display-hero`; 4–6 → `headline-xl`; 7+ → `headline`. Reserve the 7.3–11.5cqw tier for statement/stat/cover.
- **Serif is weight 500 for display, 400 for body** (the rhythm), 600 only for an attribution name. Negative tracking (−0.01..−0.03em), tight line-height (0.92–1.02). **Mono uppercase, 0.08–0.18em.** No italic, no underline, no third face, no serif body at 500.

## Depth & Surface

Flat, paper-based. Elevation from:

- **Color-block contrast** — a green tile on cream reads elevated by ink-block separation.
- **2px hairline rules** — section separators in the region's accent.
- **Border vs fill** — a cream-2 tile + 2px green border reads a different elevation than a solid tile.

**Ceiling:** zero shadow (none — adding `box-shadow` shatters the paper feel), no gradient, no glow; surfaces are solid ink-on-paper.

## Shapes

- **6px** topic tiles, **8px** step tiles, **2px** legend swatch, **3px 3px 0 0** bar tops, **50%** monogram circle. No square corners, no heavy rounding.

## Components

- **topbar** (the spine) + **footline** + **monogram-circle** (identity stamp) — the chrome set.
- **topic-tile** (6px, rotating fills) / **step-tile** (8px, 2.5px border) — the catalog + framework patterns.
- **kpi-block** (oversized serif figure) / **meta-dl** (3-col, 2px rule) / **bar** / **rule-thin** — data + structure.

## Frame Treatments

> Recipe: ground · container · composes · focal · chrome · accent · silence · Fixed/Free · density.
> Topbar on every frame; one subject per frame in deep negative space.

### 1 · Cover (identity · move: oversized serif · green · left)

**Ground** `{colors.green}`, `slide-pad`. **Composes** topbar (mono label + monogram-circle), display-hero, body lede, footline. **Focal** a 2-line Source Serif 4 `display-hero` in pink (one word in cream), left. **Chrome** mono topbar; mono footline. **Accent** pink display + the monogram circle. **Silence** ~50%. **Fixed** serif 500, flat, monogram 2px pink. **Free** title, which word is cream. **Density** low.

### 2 · Topic Tiles (catalog · move: rotating-fill grid · cream · the dense frame)

**Ground** `{colors.cream}`, `slide-pad`. **Composes** topbar, headline-xl, 3–4× topic-tile. **Focal** a row of 6px tiles, fills rotating green / pink / cream-2-with-border, each a mono ordinal + serif title. **Chrome** mono topbar. **Accent** the tile fills (mix 3 of 4, never repeat one). **Silence** tight — the density exception. **Fixed** 6px radius, rotating fills, no shadow. **Free** tile titles, which fills. **Density** dense-exception.

### 3 · KPI Stat (data · move: oversized figure · green)

**Ground** `{colors.green}`, `slide-pad`. **Composes** topbar, kpi-block (mono tag + 220px stat-figure + serif description), footline. **Focal** a Source Serif 4 `stat-figure` (~11.5cqw, +unit) in pink over a 2px pink rule. **Chrome** mono topbar + footline. **Accent** the pink figure. **Silence** ~55%. **Fixed** serif 500 figure, 2px accent rule, flat. **Free** the figure (from script), tag, description. **Density** low.

### 4 · Statement (quote · move: display serif · cream · left)

**Ground** `{colors.cream}`, generous pad. **Composes** topbar, display, name (600), caption-mono role. **Focal** a 2-line Source Serif 4 `display` (~7.3cqw) in green; a 600-weight attribution name + mono role beneath. **Chrome** mono topbar. **Accent** none — the serif carries it. **Silence** ~55%. **Fixed** serif 500 display + 600 name only, no italic. **Free** quote, name, role. **Density** low.

### 5 · Step Framework (process · move: 8px step tiles · cream/green)

**Ground** `{colors.cream}` (or green), `slide-pad`. **Composes** topbar, headline, 3–4× step-tile. **Focal** a row of 8px step tiles (2.5px border) — mono ordinal + serif 68px title + body + mono marker over a top rule; fills rotate cream-with-green-border / green / pink. **Accent** the tile fills. **Silence** moderate. **Fixed** 8px radius, 2.5px border, mono markers. **Free** steps, fills. **Density** standard.

### 6 · Chart (data · move: bars + meta · green)

**Ground** `{colors.green}`, `slide-pad`. **Composes** topbar, headline, bars + 2px axis rules, meta-dl. **Focal** 56px pink/cream/green bars on inner-edge 2px rules with mono ticks; an optional 3-col meta-dl beneath. **Chrome** mono topbar. **Accent** the bar fills. **Silence** moderate. **Fixed** 56px bars, 3px tops, 2px axes, mono ticks. **Free** values (from script), labels. **Density** standard.

## Composition Rules

### Do

- Run every display in **Source Serif 4 weight 500**, opsz, negative-tracked, tight line-height; **body at 400**.
- Set every label/caption/axis/footline in **JetBrains Mono 500 uppercase, 0.08–0.18em**.
- Give every frame a **topbar** (mono label + monogram or counter); footline on data/cover.
- Pick **one dominant surface per frame** (max two tones); **rotate tile fills**, never repeat one across a grid.
- Separate sections with **2px hairlines** in the region's accent; reserve the monogram circle for cover/summary.
- Scale display aggressively (7.3–11.5cqw) for statement/stat/cover; lean left/editorial, one subject per frame.

### Don't

- No box-shadow, gradient, or glow — flat, paper-based depth only.
- No third typeface; no italic/underline; no serif body at 500; no mono at headline scale.
- No fourth color family; no `rgba` surfaces; no 1px or 4px+ rules (2px / 2.5px only).
- No two competing content blocks; don't omit the topbar.
- Don't blow a headline edge-to-edge — step the ramp down.

## Aspect-Ratio Behavior

| Treatment      | 16:9                             | 9:16                        | 1:1                      |
| -------------- | -------------------------------- | --------------------------- | ------------------------ |
| Cover          | display left, monogram top-right | display top, monogram below | display, monogram corner |
| Topic Tiles    | 3–4 across                       | stacked                     | 2×2                      |
| KPI Stat       | figure left                      | figure centered, taller     | centered                 |
| Statement      | quote left                       | quote stacked               | centered                 |
| Step Framework | 3–4 across                       | stacked                     | 2×2                      |
| Chart          | bars + meta                      | bars taller, meta stacks    | square chart             |

`slide-pad` holds on the short edge; re-step display above the 1.4cqw floor. Topbar spans the top
on every ratio; the monogram may drop to a corner.

## Approved Real Entities

No real customers, logos, or vendors are defined in the source — render any such mark as a
placeholder. The monogram, footline strings, and tile counters carry per-deck identity; figures are content.

## Numerals & Claims (hard rule)

Never invent figures, KPIs, dates, or counts at frame scale. Render slots as `— figure —`,
`{metric}`, `— %`. KPI blocks, bars, and meta values especially carry placeholders until the script
supplies them. Issue numbers / counters are decorative chrome.

## Pre-Render Self-Audit

- **Squint** — one serif moment dominates; the surface block centers the eye.
- **Silence** — one subject per frame in deep negative space; only the topic-tile/step grids run dense.
- **Triad** — two surface tones max; headlines/body/labels use the correct per-surface color; no fourth family.
- **Type** — Source Serif 4 **500** display (opsz, negative-tracked) / **400** body; mono uppercase 0.08–0.18em; ≥1.4cqw floor.
- **Depth** — 0 shadow, 0 gradient; 2px hairlines; 6/8px radii; monogram the only full round.
- **Chrome** — topbar present on every frame; footline on data/cover.
- **Fabrication** — every numeral traces to the script, else placeholder.

## Known Gaps

- **Motion intentionally out of scope.** frame.md specifies composition only; the source relies on `deck-stage.js` for scaling/nav, no transition spec.
- **Source Serif 4 (opsz 8..60) + JetBrains Mono via Google Fonts** — the optical-size axis is critical; a non-opsz fallback flattens the size-aware letterforms. CJK: LXGW WenKai (display) / Noto Serif SC (body) / Noto Sans Mono CJK (chrome).
- **9:16 / 1:1 are guidance**; verify the floor and that two-tone discipline holds per ratio.
- Bars, hairlines, tiles, and the monogram circle are CSS-only; no external imagery is required.
- **Contrast:** green-on-pink / pink-on-green only at display scale (84px+); keep small text cream-on-green or ink-on-cream.


<!-- ===== FILE: hyperframes/hyperframes-creative/palettes/bold-energetic.md ===== -->

# Bold / Energetic

Product launches, social media, announcements, high-energy content.

```
#FFBE0B #FB5607 #FF006E #8338EC #3A86FF
#F72585 #7209B7 #3A0CA3 #4361EE #4CC9F0
#EF476F #FFD166 #06D6A0 #118AB2 #073B4C
#FF595E #FFCA3A #8AC926 #1982C4 #6A4C93
#9B5DE5 #F15BB5 #FEE440 #00BBF9 #00F5D4
#390099 #9E0059 #FF0054 #FF5400 #FFBD00
#3D348B #7678ED #F7B801 #F18701 #F35B04
#FFBC42 #D81159 #8F2D56 #218380 #73D2DE
```


<!-- ===== FILE: hyperframes/hyperframes-creative/palettes/clean-corporate.md ===== -->

# Clean / Corporate

Explainers, tutorials, presentations, professional content.

```
#FFFCF2 #CCC5B9 #403D39 #252422 #EB5E28
#22223B #4A4E69 #9A8C98 #C9ADA7 #F2E9E4
#3D5A80 #98C1D9 #E0FBFC #EE6C4D #293241
#2B2D42 #8D99AE #EDF2F4 #EF233C #D90429
#353535 #3C6E71 #FFFFFF #D9D9D9 #284B63
#E7ECEF #274C77 #6096BA #A3CEF1 #8B8C89
#CFDBD5 #E8EDDF #F5CB5C #242423 #333533
#2F6690 #3A7CA5 #D9DCD6 #16425B #81C3D7
```


<!-- ===== FILE: hyperframes/hyperframes-creative/palettes/dark-premium.md ===== -->

# Dark / Premium

Tech, finance, luxury, cinematic content.

```
#000000 #14213D #FCA311 #E5E5E5 #FFFFFF
#000814 #001D3D #003566 #FFC300 #FFD60A
#0D1B2A #1B263B #415A77 #778DA9 #E0E1DD
#0D1321 #1D2D44 #3E5C76 #748CAB #F0EBD8
#011627 #FDFFFC #2EC4B6 #E71D36 #FF9F1C
#0B090A #161A1D #660708 #A4161A #E5383B
#001427 #708D81 #F4D58D #BF0603 #8D0801
#001524 #15616D #FFECD1 #FF7D00 #78290F
```


<!-- ===== FILE: hyperframes/hyperframes-creative/palettes/jewel-rich.md ===== -->

# Jewel / Rich

Luxury, events, sophisticated, high-end content.

```
#5F0F40 #9A031E #FB8B24 #E36414 #0F4C5C
#780000 #C1121F #FDF0D5 #003049 #669BBC
#10002B #240046 #3C096C #5A189A #7B2CBF
#355070 #6D597A #B56576 #E56B6F #EAAC8B
#6F1D1B #BB9457 #432818 #99582A #FFE6A7
#231942 #5E548E #9F86C0 #BE95C4 #E0B1CB
#461220 #8C2F39 #B23A48 #FCB9B2 #FED0BB
#780116 #F7B538 #DB7C26 #D8572A #C32F27
```


<!-- ===== FILE: hyperframes/hyperframes-creative/palettes/monochrome.md ===== -->

# Monochrome

Dramatic, typography-focused, serious content.

```
#F8F9FA #E9ECEF #DEE2E6 #CED4DA #ADB5BD #6C757D #495057 #343A40 #212529
#0466C8 #0353A4 #023E7D #002855 #001233
#012A4A #013A63 #01497C #2A6F97 #468FAF #89C2D9
#582F0E #7F4F24 #936639 #A68A64 #C2C5AA
#463F3A #8A817C #BCB8B1 #F4F3EE #E0AFA0
#03071E #370617 #6A040F #9D0208 #DC2F02 #F48C06 #FFBA08
#590D22 #800F2F #A4133C #FF4D6D #FF8FA3 #FFCCD5
#220901 #621708 #941B0C #BC3908 #F6AA1C
```


<!-- ===== FILE: hyperframes/hyperframes-creative/palettes/nature-earth.md ===== -->

# Nature / Earth

Sustainability, outdoor, organic, wellness content.

```
#606C38 #283618 #FEFAE0 #DDA15E #BC6C25
#DAD7CD #A3B18A #588157 #3A5A40 #344E41
#386641 #6A994E #A7C957 #F2E8CF #BC4749
#CAD2C5 #84A98C #52796F #354F52 #2F3E46
#F0EAD2 #DDE5B6 #ADC178 #A98467 #6C584C
#132A13 #31572C #4F772D #90A955 #ECF39E
#6B9080 #A4C3B2 #CCE3DE #EAF4F4 #F6FFF8
#233D4D #FE7F2D #FCCA46 #A1C181 #619B8A
```


<!-- ===== FILE: hyperframes/hyperframes-creative/palettes/neon-electric.md ===== -->

# Neon / Electric

Gaming, tech, nightlife, Gen Z content.

```
#F72585 #B5179E #7209B7 #560BAD #3A0CA3
#70D6FF #FF70A6 #FF9770 #FFD670 #E9FF70
#7400B8 #6930C3 #5E60CE #5390D9 #48BFE3
#0B132B #1C2541 #3A506B #5BC0BE #6FFFE9
#540D6E #EE4266 #FFD23F #3BCEAC #0EAD69
#2D00F7 #6A00F4 #8900F2 #A100F2 #F20089
#FF6D00 #FF7900 #FF8500 #FF9100 #240046
#BBFBFF #8DD8FF #4E71FF #5409DA
```


<!-- ===== FILE: hyperframes/hyperframes-creative/palettes/pastel-soft.md ===== -->

# Pastel / Soft

Fashion, beauty, lifestyle, wellness content.

```
#CDB4DB #FFC8DD #FFAFCC #BDE0FE #A2D2FF
#CCD5AE #E9EDC9 #FEFAE0 #FAEDCD #D4A373
#FFD6FF #E7C6FF #C8B6FF #B8C0FF #BBD0FF
#FFA69E #FAF3DD #B8F2E6 #AED9E0 #5E6472
#EDAFB8 #F7E1D7 #DEDBD2 #B0C4B1 #4A5759
#555B6E #89B0AE #BEE3DB #FAF9F9 #FFD6BA
#006D77 #83C5BE #EDF6F9 #FFDDD2 #E29578
#0081A7 #00AFB9 #FDFCDC #FED9B7 #F07167
```


<!-- ===== FILE: hyperframes/hyperframes-creative/palettes/warm-editorial.md ===== -->

# Warm / Editorial

Storytelling, documentaries, case studies, narrative content.

```
#264653 #2A9D8F #E9C46A #F4A261 #E76F51
#335C67 #FFF3B0 #E09F3E #9E2A2B #540B0E
#F4F1DE #E07A5F #3D405B #81B29A #F2CC8F
#F6BD60 #F7EDE2 #F5CAC3 #84A59D #F28482
#003049 #D62828 #F77F00 #FCBF49 #EAE2B7
#588B8B #FFFFFF #FFD5C2 #F28F3B #C8553D
#283D3B #197278 #EDDDD4 #C44536 #772E25
#0D3B66 #FAF0CA #F4D35E #EE964B #F95738
```


<!-- ===== FILE: hyperframes/hyperframes-creative/references/audio-reactive.md ===== -->

# Audio-Reactive Animation

Drive visuals from music, voice, or sound. Any GSAP-animatable property can respond to pre-extracted audio data.

## Audio Data Format

```js
var AUDIO_DATA = {
  fps: 30,
  totalFrames: 900,
  frames: [{ bands: [0.82, 0.45, 0.31, ...] }, ...]
};
```

- `frames[i].bands[]` — frequency band amplitudes, 0-1. Index 0 = bass, higher = treble.
- Each band normalized independently across the full track.

## Mapping Audio to Visuals

| Audio signal           | Visual property                   | Effect                     |
| ---------------------- | --------------------------------- | -------------------------- |
| Bass (bands[0])        | `scale`                           | Pulse on beat              |
| Treble (bands[12-14])  | `textShadow`, `boxShadow`         | Glow intensity             |
| Overall amplitude      | `opacity`, `y`, `backgroundColor` | Breathe, lift, color shift |
| Mid-range (bands[4-8]) | `borderRadius`, `width`           | Shape morphing             |

Any GSAP-tweenable property works — `clipPath`, `filter`, SVG attributes, CSS custom properties.

## Content, Not Medium

Audio provides **timing and intensity**. The visual vocabulary comes from the narrative.

**Never add:** equalizer bars, spectrum analyzers, waveform displays, musical notes clip art, generic particle systems, rainbow color cycling, strobing white on beats, abstract pulsing orbs.

**Instead:** Let content guide the visual and audio drive its behavior. Bass makes warmth _swell_. Treble sharpens _contrast_. The visual choice comes from "what does this piece feel like?"

## Sampling Pattern

Audio reactivity requires per-frame sampling via a `for` loop with `tl.call()`, not a single tween:

```js
// ✅ Correct — sample every frame
for (var f = 0; f < AUDIO_DATA.totalFrames; f++) {
  tl.call(
    (function (frame) {
      return function () {
        draw(frame);
      };
    })(AUDIO_DATA.frames[f]),
    [],
    f / AUDIO_DATA.fps,
  );
}

// ❌ Wrong — single tween, doesn't react to audio
gsap.to(".el", { scale: 1.2, duration: totalDuration });
```

Without per-frame sampling, the composition doesn't actually react to audio.

## textShadow Gotcha

`textShadow` on a parent container with semi-transparent children (e.g., inactive caption words at `rgba(255,255,255,0.3)`) renders a visible glow rectangle behind all children. Fix: apply `scale` to the container for beat pulse, but apply `textShadow` to individual active words only.

## Guidelines

- **Subtlety for text** — 3-6% scale variation, soft glow. Heavy pulsing makes text unreadable.
- **Go bigger on non-text** — backgrounds and shapes can handle 10-30% swings.
- **Match the energy** — corporate = subtle; music video = dramatic.
- **Deterministic** — pre-extracted data, no Web Audio API, no runtime analysis.

## Constraints

- All audio data must be pre-extracted (use `extract-audio-data.py` from this skill's `scripts/`)
- No `Math.random()` or `Date.now()`
- Audio reactivity runs on the same GSAP timeline as everything else
