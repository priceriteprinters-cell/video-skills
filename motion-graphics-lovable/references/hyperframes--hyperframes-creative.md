

<!-- ===== FILE: hyperframes/hyperframes-creative/GUIDE.md ===== -->

---
name: hyperframes-creative
description: Non-animation creative direction for HyperFrames videos. Use for design spec (frame.md / design.md) handling, palettes, typography, narration, beat planning, audio-reactive visuals, composition patterns, and brand / style decisions. For atomic motion patterns and scene blueprints, use `hyperframes-animation`.
---

**Plugin installs:** Before setup or freshness commands, follow [plugin execution rules](../hyperframes/references/plugin-installation.md) when this skill is inside a HyperFrames plugin. Standalone installs keep the update instructions below.

# HyperFrames Creative

Brand, pacing, style, narration, and composition direction. Use after the technical contract from `hyperframes-core` is in place.

For motion patterns, scene blueprints, transitions, and CSS marker effects, use `hyperframes-animation` — this skill is intentionally non-animation.

> **Read these two FIRST for any non-trivial composition — they override web instincts:**
>
> - `references/house-style.md` — "interpret the prompt, generate real content," the lazy-default list, and the background/foreground layer recipe. This is what turns a literal restyle into a _concept_.
> - `references/video-composition.md` — video-medium scale, depth, and foreground detail. It explains how to avoid empty web-page layouts without imposing a universal element count.
>
> Skipping these is the single biggest cause of generic, web-page-looking output. They are not optional rows in the routing table below — for anything beyond a one-line edit, open both before you choose colors or write HTML.

## Workflow

1. If a project has a design spec, **read it first** and treat its frontmatter tokens as brand truth (colors, fonts, spacing, tone, constraints). Which file to read (precedence `frame.md` → `design.md` → `DESIGN.md`) and how to parse it (frontmatter = normative, prose = context) are defined once in [`references/design-spec.md`](references/design-spec.md) — resolve and load per that doc.
2. If no design spec exists and the user asks for visual direction, choose a route:
   - Ready-made frame-preset (optional) → `frame-presets/` (adopt a `FRAME.md` as `frame.md`; see `references/design-spec.md`)
   - Named style or mood → `references/visual-styles.md`
   - Fast defaults → `references/house-style.md`
   - Interactive selection → `references/design-picker.md`
3. For multi-scene work, plan beats and rhythm before writing HTML → `references/beat-direction.md`. For scene transitions, jump to `hyperframes-animation/transitions/`.
4. For motion-heavy work, read `references/motion-principles.md` (high-level guardrails), then go to `hyperframes-animation` for atomic rules.

## Routing

| Topic                                                                                                   | Read                                           |
| ------------------------------------------------------------------------------------------------------- | ---------------------------------------------- |
| Adopt a ready-made frame-preset as `frame.md` (optional)                                                | `frame-presets/` · `references/design-spec.md` |
| Default palettes, motion, typography, lazy defaults to question                                         | `references/house-style.md`                    |
| Named style presets, mood-to-style routing                                                              | `references/visual-styles.md`                  |
| Palette-specific color tokens                                                                           | `palettes/*.md`                                |
| Composition patterns — PiP, text-behind-subject, title card, slide show                                 | `references/composition-patterns.md`           |
| Stats / infographic presentation                                                                        | `references/data-in-motion.md`                 |
| Structured expansion for open-ended prompts                                                             | `references/prompt-expansion.md`               |
| Video-medium density, scale, color, frame composition                                                   | `references/video-composition.md`              |
| Per-beat direction, rhythm planning, transition timing                                                  | `references/beat-direction.md`                 |
| Post-authoring spec verification (colors, type, corners, spacing, depth)                                | `references/design-adherence.md`               |
| High-level motion guardrails and GSAP-quality rules                                                     | `references/motion-principles.md`              |
| Font selection, pairings, rendered-video type guardrails                                                | `references/typography.md`                     |
| Story doctrine — hook language, value-before-evidence, storyboard-as-proposal, source-traceable visuals | `references/story-spine.md`                    |
| Script pacing, tone, openings, number pronunciation                                                     | `references/narration.md`                      |
| Precomputed audio bands mapped to motion                                                                | `references/audio-reactive.md`                 |

## Scripts

- `scripts/contrast-report.mjs` — inspect contrast warnings from rendered frames.
- `scripts/extract-audio-data.py` — pre-extract audio bands for audio-reactive compositions.
- `scripts/package-loader.mjs` — support script for bundled creative tooling.

`contrast-report.mjs` resolves helper packages from the current project first, then can bootstrap the bundled HyperFrames package version. Set `HYPERFRAMES_SKILL_PKG_VERSION=<version>` only when running the skill outside the bundled CLI/skill install and you need to pin that bootstrap version explicitly.

Run with explicit paths, for example:

```bash
python <SKILL_DIR>/scripts/extract-audio-data.py <audio-file>
```

Animation analysis (`animation-map.mjs`) lives in `hyperframes-animation/scripts/`.

## Boundaries

- Do not override `hyperframes-core` technical rules.
- Do not require a design system for a minimal technical composition.
- Do not add extra scenes, narration, music, captions, or transitions unless the request calls for them or you first propose the expansion.
- Keep recipe references task-specific; do not read every reference for simple edits.


<!-- ===== FILE: hyperframes/hyperframes-creative/frame-presets/biennale-yellow/FRAME.md ===== -->

---
version: alpha
name: Biennale Yellow — Frame (video / frame layer)
description: >
  Video-first companion to Biennale Yellow's design.md. The unit is the frame (1920×1080). Atoms
  are identical and sacred — warm parchment grounds, a single deep indigo ink, solar yellow deployed
  as bloom / panel / tile underprint, Instrument Serif display + Archivo sans + JetBrains Mono data,
  1px hairline rules as the only border, atmospheric depth (no shadows), and the bottom-right
  pagenum. Composition + frame scale rewritten. Restraint is the rule; motion out of scope.
unit: the frame — 1920×1080 primary; 9:16 and 1:1 documented
principle: atoms are sacred · composition is free · numbers come from the script

colors:
  paper: "#E9E5DB"
  paper-deep: "#DCD6C4"
  sun: "#F1EE2E"
  sun-soft: "#F8F39B"
  haze: "#F0DA7C"
  ink: "#1B2566"
  ember: "#E26B4A"

typography:
  # — reading + data ramp —
  body:    { fontFamily: "Archivo", cqw: 0.85, weight: 400, lineHeight: 1.5, color: "ink" }
  body-lede:{ fontFamily: "Archivo", cqw: 0.95, weight: 400, lineHeight: 1.55 }
  micro-label:{ fontFamily: "Archivo", px: 13, weight: 600, tracking: "0.18em", upper: true }
  rail-label:{ fontFamily: "Archivo", px: 13, weight: 600, tracking: "0.32em", upper: true }
  mono-data:{ fontFamily: "JetBrains Mono", cqw: 0.73, weight: 400, tracking: "0.04em" }
  pagenum: { fontFamily: "JetBrains Mono", px: 13, weight: 400, tracking: "0.08em", opacity: 0.75 }
  # — display ramp (Instrument Serif 400, tight, negative tracking) —
  ledger-title:{ fontFamily: "Instrument Serif", cqw: 1.55, weight: 400, lineHeight: 1.15 }
  strand-title:{ fontFamily: "Instrument Serif", cqw: 1.7, weight: 400, lineHeight: 1.1 }
  headline-sm:{ fontFamily: "Instrument Serif", cqw: 2.9, weight: 400, lineHeight: 1.0 }
  headline:{ fontFamily: "Instrument Serif", cqw: 4.6, weight: 400, lineHeight: 1.06, tracking: "-0.005em" }
  date-rail:{ fontFamily: "Instrument Serif", cqw: 5.0, weight: 400, lineHeight: 0.96, tracking: "-0.005em" }
  display-it:{ fontFamily: "Instrument Serif", cqw: 7.0, weight: 400, italic: true, lineHeight: 1.04, tracking: "-0.005em" }
  numeral-md:{ fontFamily: "Instrument Serif", cqw: 7.5, weight: 400, lineHeight: 0.92, tracking: "-0.01em" }
  display:{ fontFamily: "Instrument Serif", cqw: 14.6, weight: 400, lineHeight: 0.86, tracking: "-0.018em" }
  numeral-jumbo:{ fontFamily: "Instrument Serif", cqw: 28.0, weight: 400, lineHeight: 0.84, tracking: "-0.04em" }

spacing:
  pad-edge: "4cqw"
  pad-region: "4.2cqw"
  gap-region: "2.5cqw"

components:
  sun-bloom:
    background: "radial gradient {colors.sun} core → {colors.sun-soft} → {colors.haze} → transparent on {colors.paper}"
    size: "42–70% of the frame, off-center or behind the focal element"
    description: "The primary depth layer. One per frame; a flat parchment frame reads as broken."
  ember-bloom:
    background: "radial {colors.ember} at 15–22% opacity"
    placement: "corner opposite the sun-bloom"
    description: "Subordinate counter-temperature balance; never dominant."
  block-tile:
    backgroundColor: "{colors.sun} at 40–70% opacity"
    layout: "rectangles on an 8×4 grid behind cover/colophon"
    description: "A layered poster underprint."
  yellow-panel:
    backgroundColor: "{colors.sun}"
    textColor: "{colors.ink}"
    rounded: "0"
    border: "none (meets paper directly)"
    description: "Full-bleed column/third — the strongest color statement, ink on top."
  hairline-rule:
    rule: "1px solid {colors.ink} (soft variant: {colors.ink} at 18–20%)"
    description: "The ONLY border — header underlines, footer tops, ledger separators. No thicker rule exists."
  strand-row:
    borderBottom: "1px {colors.ink} 18–20%"
    typography: "{typography.strand-title} + {typography.body}"
    description: "Serif numeral + serif title + sans body. Numbered editorial lists."
  ledger-row:
    borderBottom: "1px {colors.ink} 18–20%"
    typography: "{typography.mono-date} · {typography.ledger-title} · {typography.body} · {typography.mono-data}"
    description: "4-col tabular — mono date · serif title · sans venue · mono duration (right)."
  footer-band:
    borderTop: "1px solid {colors.ink} per cell"
    typography: "{typography.micro-label} + {typography.body-sm}"
    description: "4-column metadata strip at the foot of cover/colophon."
  vertical-rail:
    typography: "{typography.rail-label}"
    transform: "rotated up the left edge"
    description: "Section marker on chapter/divider frames."
  pagenum:
    typography: "{typography.pagenum}"
    color: "{colors.ink} at 75%"
    placement: "bottom-right"
    description: "The only persistent chrome."
---

# Biennale Yellow — Frame (video / frame layer)

## Overview

Biennale Yellow at frame scale is a **literary-editorial system** in the register of an art
biennale catalogue: warm parchment, a single deep indigo ink, and solar yellow as atmosphere. No
cards, no buttons, no shadows, no rounded corners — the structural vocabulary is just **paper, ink,
and yellow.** Depth is delivered by soft radial **sun blooms**, not elevation.

The voice is three faces in rigid roles: **Instrument Serif** (weight 400, tight line-height,
negative tracking) carries every display, numeral, and quote from 40px to 720px+; **Archivo** carries
body and the wide-tracked uppercase micro-label; **JetBrains Mono** carries every date, figure, and
the pagenum. Text is **always ink** — contrast comes from size and weight, never color. The mood
sits between a folded museum brochure and a slow-reading literary quarterly: confident, atmospheric,
deeply restrained.

**Key characteristics at frame scale:**

- **Warm parchment ground** on every frame; never white, never gray.
- **Single ink** (`{colors.ink}`) for all type and all rules; **solar yellow** as bloom / panel / tile.
- **Instrument Serif 400** display (tight, negative-tracked); **Archivo** body + micro-labels; **JetBrains Mono** data.
- **1px hairline rules** are the only border — no thicker weight exists; **no shadows, no rounded corners**.
- **Sun bloom** is the primary depth layer on every frame; an ember counter-bloom adds warm-cool tension.
- **Editorial-restrained** — sparse reads as elegant; crowding breaks the catalogue feel.

## The Frame

### Frame Craft Bar

Three eyeball tests gate every frame before any structural check:

- **Squint** — one Instrument Serif moment dominates at 3–6× its neighbor; the sun bloom centers the eye.
- **Silence** — frames read **55–60% empty**; the **ledger is the one dense exception** (density via quiet hairline repetition, not richness).
- **Restraint** — **one ink color** for all type and rules; **one sun bloom** per frame (+ optional subordinate ember); never invert (no yellow text on ink).
- **Reference** — aim at an **art-biennale catalogue / slow exhibition poster / literary quarterly**; failure looks like a **flat CMS template** (no bloom) or a **bordered-card deck**.

- **Primary:** 1920×1080 (16:9). Display authored in **`cqw`** (`px ÷ 1920 × 100 = cqw`).
- **Vertical:** 1080×1920 (9:16). **Square:** 1080×1080 (1:1).
- **Safe area:** `pad-edge` 4cqw (40–76px equivalent) — the elegance depends on edge negative space; only blooms, tiles, and panels bleed.

**The container law (load-bearing).** Every frame ground sets `container-type: size`; ALL
frame-relative units are `cqw`/`cqh` against it — never `vw`. Hairlines stay 1px; bloom sizes scale
as `%` of the frame.

## Colors

Tokens identical to the source. `{colors.paper}` is the universal ground; `{colors.ink}` (deep
indigo navy) is **every line of type and every rule** — there is no secondary text color.
`{colors.sun}` deploys three ways: the **bloom** (radial atmosphere), the **yellow-panel**
(full-bleed poster fill, ink on top), and the **block-tile** underprint. `{colors.sun-soft}`/`haze`
are bloom mid/outer stops. `{colors.ember}` appears **only** as a 15–22% counter-bloom — never a
fill, never text. **The system never inverts** — ink on sun is correct; yellow text on ink does not exist.

## Typography

Two ramps. The **reading/data ramp** (Archivo body 0.85cqw ink, micro-labels in px, JetBrains Mono
data) carries copy + chrome; the **display ramp** (Instrument Serif `ledger-title` 1.55cqw →
`numeral-jumbo` 28cqw) carries every headline, numeral, and quote.

- **Legibility floor:** any load-bearing line ≥ **1.4cqw**; mono/labels in px are chrome only.
- **Fit-to-measure:** size the headline to its length. Cap the block at **≤ 78cqw**; ≤3 words → `display`; 4–6 → `headline`; 7+ → `headline-sm`. The jumbo numeral is a divider's whole point — don't shrink it.
- **Instrument Serif is weight 400 only** (its contrast is the weight signal), tight line-height (0.84–1.06), negative tracking; **micro-labels uppercase Archivo 600, ≥0.16em**; **mono for all numerals/dates**. No bold serif, no second text color, no mono in body/display.

## Depth & Surface

Atmospheric, not structural. Depth from:

- **Sun bloom** — the primary layer: a layered radial (sun 70–95% core → sun-soft → haze 18–22% → paper 0%), 42–70% of the frame. One per frame.
- **Ember bloom** — a 15–22% peach counter-bloom in the opposite corner; always subordinate.
- **Block-tile underprint** — translucent yellow rectangles on an 8×4 grid (cover/colophon).
- **Yellow panel** — the one "hard" color statement: a flooded column/third, ink on top.
- **Hairline rules** — 1px ink for structural separation (soft 18–20% variant for dense rows).

**Ceiling:** zero box-shadow, zero text-shadow, zero rounded corner, no border thicker than 1px.

## Shapes

- **0 radius on everything** — strict rectangles. Blooms are edgeless (they fade into paper).

## Components

- **sun-bloom / ember-bloom / block-tile** — the atmospheric depth set. **yellow-panel** — the poster-fill statement.
- **hairline-rule** — the only border (1px ink; soft variant for dense rows).
- **strand-row / ledger-row / footer-band** — the editorial list, tabular calendar, and metadata strip.
- **vertical-rail** — rotated chapter marker. **pagenum** — the bottom-right mono chrome.

## Frame Treatments

> Recipe: ground · container · composes · focal · chrome · accent · silence · Fixed/Free · density.
> A sun bloom + bottom-right pagenum on every frame; sparse is the default.

### 1 · Cover (identity · move: display + sun bloom · left)

**Ground** paper + a large sun-bloom (left-of-center) + an ember counter-bloom (opposite corner).
**Composes** micro-label, display, date-rail, footer-band, pagenum. **Focal** a 2-line Instrument
Serif `display` (italic key word) in ink, left, under a micro-label. **Chrome** a serif date-rail
top-right; a 4-column footer-band at the foot. **Accent** the sun bloom + yellow. **Silence** the
bloom holds the open space. **Fixed** ink type, one bloom, 1px footer rules, no shadow. **Free**
title, date, footer cells. **Density** low.

### 2 · Chapter Divider (section · move: jumbo numeral · vertical rail)

**Ground** paper + a corner-anchored sun-bloom. **Composes** vertical-rail, numeral-jumbo,
headline-sm. **Focal** a single huge Instrument Serif `numeral-jumbo` (≈28cqw) dominating, with a
serif title beneath. **Chrome** a rotated vertical-rail label up the left edge; pagenum. **Accent**
the bloom behind the numeral. **Silence** ~60%. **Fixed** serif 400, jumbo numeral, rail label.
**Free** the ordinal, title, rail text. **Density** low.

### 3 · Ledger (catalog · move: hairline tabular rows · the dense frame)

**Ground** paper (bloom optional, subtle). **Composes** headline-sm + micro-label topbar, ledger-rows.
**Focal** a 4-column tabular calendar — mono date · serif title · sans venue · mono duration —
separated by hairline-soft rules under a 1px ink header rule. **Chrome** pagenum. **Accent** none —
density through quiet repetition, not color. **Silence** tight — the density exception (achieved by
repetition, not richness). **Fixed** hairline rules, mono dates, serif titles. **Free** rows, venues.
**Density** dense-exception.

### 4 · Manifesto / Quote (quote · move: italic serif · centered bloom)

**Ground** paper + a centered sun-bloom. **Composes** numeral-lg quote mark, display-it, attribution.
**Focal** a 2-line Instrument Serif **italic** `display-it` quote in ink, centered, under an
oversized serif quote mark. **Chrome** a micro-label attribution. **Accent** the centered bloom.
**Silence** ~60% — deliberately open. **Fixed** italic serif, one bloom, ink. **Free** quote,
attribution. **Density** low.

### 5 · Poster Panel (statement · move: yellow panel · split)

**Ground** paper with a full-bleed `{colors.sun}` `yellow-panel` (column or third). **Composes**
yellow-panel, micro-label, headline. **Focal** an Instrument Serif `headline` in ink sitting **on
the sun panel** (ink-on-yellow — a signature). **Chrome** micro-label; pagenum. **Accent** the panel
itself. **Silence** the paper side stays open. **Fixed** ink-on-sun, panel meets paper directly (no
border), no shadow. **Free** headline, panel side/width. **Density** low.

### 6 · Strand List (programme · move: numbered editorial rows · left)

**Ground** paper + a subtle sun-bloom. **Composes** micro-label, headline-sm, strand-rows. **Focal**
a numbered list — serif numeral + serif title + sans body, hairline-soft separators. **Chrome**
micro-label; pagenum. **Accent** the bloom. **Silence** moderate; rows breathe. **Fixed** serif
numerals, hairline-soft rules. **Free** items, copy. **Density** standard.

## Composition Rules

### Do

- Start on **warm parchment**; add **one sun bloom** (optionally an ember counter-bloom) — atmosphere is the depth.
- Set every line in **ink**; use **Instrument Serif 400** (tight, negative-tracked) for display, **Archivo** body, **JetBrains Mono** for all numerals/dates.
- Make every separator a **1px ink hairline** (soft variant for dense rows); flood a **yellow panel** for poster moments (ink on top).
- Keep micro-labels **uppercase Archivo 600, 0.16–0.32em**; pin the **pagenum** bottom-right.
- Lean sparse; left/asymmetric on cover/chapter/list, centered on manifesto.

### Don't

- No drop shadows, no rounded corners, no bordered cards, no border thicker than 1px.
- No second text color; no bold Instrument Serif; no inverted ink grounds.
- No mono for body/display; no font substitutes.
- Don't crowd the canvas — sparse reads as elegant; don't omit the bloom (flat parchment reads as a CMS template).
- Don't blow a headline edge-to-edge — step the ramp down.

## Aspect-Ratio Behavior

| Treatment       | 16:9                                           | 9:16                       | 1:1                        |
| --------------- | ---------------------------------------------- | -------------------------- | -------------------------- |
| Cover           | display left, date-rail top-right, footer foot | display top, footer stacks | display upper, footer foot |
| Chapter Divider | jumbo numeral, rail left                       | numeral centered, rail top | numeral centered           |
| Ledger          | 4-col rows                                     | drop venue col → 3-col     | 3-col                      |
| Manifesto       | centered italic                                | centered, taller           | centered                   |
| Poster Panel    | side panel + paper                             | top/bottom panel band      | panel third                |
| Strand List     | numbered rows                                  | rows (tighter)             | rows                       |

`pad-edge` holds on the short edge; display clamps use the shorter axis so portrait doesn't blow out
headlines. Keep load-bearing lines ≥ 1.4cqw. Ledger/strand fixed first columns may tighten on 9:16.

## Approved Entities

No real customers, logos, or vendors are defined in the source — render any such mark as a
placeholder. Programme titles, venues, and dates are content; the system supplies paper, ink, yellow.

## Numerals & Claims (hard rule)

Never invent figures, dates, durations, or counts at frame scale. Render slots as `— figure —`,
`{metric}`, `NN JUN`, `N m`. Ledger dates/durations and chart values especially carry placeholders
until the script supplies them. Chapter ordinals (01, 02…) are decorative.

## Pre-Render Self-Audit

- **Squint** — one serif display moment dominates; the bloom centers the eye.
- **Silence** — sparse frames 55–60% open; only the ledger runs dense (via repetition, not richness).
- **One color** — ink for all text + rules; sun for bloom/panel/tile; ember counter-bloom only; no inversion.
- **Type** — Instrument Serif 400 tight negative-tracked, fit-to-measure; micro-labels uppercase 0.16em+; mono numerals; ≥1.4cqw floor.
- **Depth** — 0 shadow, 0 rounded corner, 1px hairlines only; one sun bloom present.
- **Anchor** — left on cover/chapter/list, centered on manifesto; pagenum bottom-right.
- **Fabrication** — every numeral/date traces to the script, else placeholder.

## Known Gaps

- **Motion intentionally out of scope.** frame.md specifies composition only; the source's 280ms crossfade is a deck mechanic.
- **Instrument Serif + Archivo + JetBrains Mono via Google Fonts.** CJK: Smiley Sans (display) / Noto Serif SC (body) / Noto Sans SC (labels); italic serif and mono tabular figures have no exact Hanzi equal — keep ledger dates Latin.
- **9:16 / 1:1 are guidance**; the `min(vw,vh)` clamp pattern keeps display from blowing out — verify per ratio.
- Sun/ember blooms, block tiles, yellow panels, and hairline rules are CSS-only; no external imagery is required.


<!-- ===== FILE: hyperframes/hyperframes-creative/frame-presets/blockframe/FRAME.md ===== -->

---
version: alpha
name: BlockFrame — Frame (video / frame layer)
description: >
  Video-first companion to BlockFrame's design.md. The unit is the frame (1920×1080). Atoms are
  identical and sacred — 4px black borders + 8px hard offset shadows, the five-pastel candy palette
  (pink/blue/green/yellow/cream) plus black/white/off-white, Inter 800–900 uppercase display +
  Space Grotesk label chrome, square corners, label-pills, tilted decorations, star bursts, stripe
  blocks, dot grids. Composition + frame scale rewritten. Motion out of scope.
unit: the frame — 1920×1080 primary; 9:16 and 1:1 documented
principle: atoms are sacred · composition is free · numbers come from the script

colors:
  black: "#000000"
  white: "#FFFFFF"
  offwhite: "#FFFDF5"
  pink: "#FE90E8"
  blue: "#C0F7FE"
  green: "#99E885"
  yellow: "#F7CB46"
  cream: "#FFDC8B"

borders: { primary: "4px solid black", thin: "3px solid black" }
shadows: { default: "8px 8px 0 black", small: "4px 4px 0 black", hover: "6px 6px 0 black", close-yellow: "12px 12px 0 yellow", close-white: "6px 6px 0 white" }

typography:
  # — reading + chrome ramp —
  body:    { fontFamily: "Inter", cqw: 0.95, weight: 500, lineHeight: 1.6 }
  card-title:{ fontFamily: "Inter", cqw: 1.15, weight: 700, upper: true, lineHeight: 1.2 }
  label:   { fontFamily: "Space Grotesk", px: 13, weight: 600, tracking: "0.08em", upper: true }
  counter: { fontFamily: "Space Grotesk", px: 14, weight: 700, tracking: "0.1em", upper: true }
  # — display ramp (Inter 800–900, uppercase, negative tracking) —
  heading-md:{ fontFamily: "Inter", cqw: 2.1, weight: 700, lineHeight: 1.1, tracking: "-0.01em", upper: true }
  quote-text:{ fontFamily: "Inter", cqw: 2.7, weight: 900, lineHeight: 1.15, tracking: "-0.02em", upper: true }
  stat-number:{ fontFamily: "Inter", cqw: 3.3, weight: 900, lineHeight: 1.0 }
  heading-lg:{ fontFamily: "Inter", cqw: 3.3, weight: 800, lineHeight: 1.0, tracking: "-0.02em", upper: true }
  close-title:{ fontFamily: "Inter", cqw: 4.2, weight: 900, lineHeight: 0.95, tracking: "-0.03em", upper: true }
  heading-xl:{ fontFamily: "Inter", cqw: 5.0, weight: 900, lineHeight: 0.95, tracking: "-0.03em", upper: true }

spacing:
  slide-pad: "3.1cqw"   # 60px @1920
  gap-md: "1.7cqw"

components:
  card-elevated:
    backgroundColor: "{colors.white}"
    border: "0.4cqw solid {colors.black}"
    rounded: "0"
    shadow: "0.8cqw 0.8cqw 0 {colors.black}"
    description: "Primary card. Border/shadow coupled: 4px↔8px, 3px↔4px."
  card-small:
    backgroundColor: "{colors.white}"
    border: "0.3cqw solid {colors.black}"
    rounded: "0"
    shadow: "0.4cqw 0.4cqw 0 {colors.black}"
    description: "Stat cards, team cards, timeline steps."
  label-pill:
    border: "0.3cqw solid {colors.black}"
    backgroundColor: "any pastel / {colors.white}"
    rounded: "9999px"
    shadow: "0.4cqw 0.4cqw 0 {colors.black}"
    typography: "{typography.label}"
    description: "The universal eyebrow — never plain text."
  button-primary:
    backgroundColor: "{colors.yellow}"
    textColor: "{colors.black}"
    border: "0.3cqw solid {colors.black}"
    rounded: "0"
    shadow: "0.4cqw 0.4cqw 0 {colors.black}"
    typography: "Inter 700"
    description: "The CTA."
  star-burst:
    backgroundColor: "any pastel"
    border: "0.3cqw solid {colors.black}"
    clip: "10-point clip-path star"
    description: "Corner attention-grabber."
  stripe-block:
    backgroundImage: "45° {colors.black} + pastel diagonal stripes"
    border: "0.3cqw solid {colors.black}"
    description: "Poster decoration."
  bg-dot-grid:
    backgroundImage: "radial-dot ~1.2px dots, 24px grid, {colors.black}"
    description: "Faint corner/ground overlay."
  tilt-deco:
    transform: "rotate(±2°–12°)"
    description: "Rotated rectangle/badge/star. Stat cards alternate −2/+2°. The grid-puncture signature."
  stat-deco-dot:
    backgroundColor: "any pastel"
    border: "2px solid {colors.black}"
    rounded: "50%"
    size: "12px"
    description: "The ONLY round shape, pinned to stat cards."
  close-frame:
    backgroundColor: "{colors.black}"
    textColor: "{colors.white}"
    border: "0.4cqw solid {colors.white}"
    rounded: "0"
    shadow: "1.2cqw 1.2cqw 0 {colors.yellow}"
    description: "Inverted closer — the only colored shadow."
---

# BlockFrame — Frame (video / frame layer)

## Overview

BlockFrame at frame scale is a **maximalist neobrutalist** system on five laws: every region has a
4px black border, every elevated element an 8px hard offset shadow, every corner square, every
accent a saturated pastel, and every layout allowed to be a little crooked. The joy is the
deliberate collision — bordered cards meeting bordered cards, shadows stacking, tilted decorations
puncturing the grid.

The voice is **Inter** at weight 800–900 in tight uppercase with negative tracking (display) +
weight 500 sentence body, and **Space Grotesk** weight 600 uppercase 0.08em as the label/chrome
voice. Five candy pastels (pink/blue/green/yellow/cream) cycle as full-bleed grounds across frames
— the color cycling is the primary rhythm. Depth is **hard offset shadow** (8px/4px, solid black,
zero blur, bottom-right); the close-frame's 12px yellow shadow is the one colored exception.

**Key characteristics at frame scale:**

- **4px black borders + 8px hard shadows** on primary cards; 3px + 4px on chrome (weights coupled).
- **Five-pastel palette** cycled as full-bleed grounds; black/white/off-white structural.
- **Inter 800–900 uppercase** negative-tracked display; **Space Grotesk** label chrome.
- **Square corners** everywhere (only the stat-deco dot is round); **tilted decorations** puncture the grid.
- **Label-pills** open every region; star bursts, stripe blocks, dot grids are reusable attention units.
- **Comfortably dense** — packed reads as authoritative; empty corners read as broken.

## The Frame

### Frame Craft Bar

Three eyeball tests gate every frame before any structural check:

- **Squint** — one Inter display moment dominates at 3–6× its neighbor; cards read as a system, not rivals.
- **Silence** — cover/quote/close keep air (decorations, not content); the **feature-card and stat grids are the dense exception**.
- **Restraint** — the 4px→08px / 3px→4px coupling holds; black borders only (white on close); pastel ground **cycles** one per frame; no sixth pastel.
- **Reference** — aim at a **zine / 1990s sticker-book / toy-packaging spread** (bordered blocks, tilted decorations); failure looks like a **flat, borderless, blurred-shadow web card grid**.

- **Primary:** 1920×1080 (16:9). Display authored in **`cqw`** (`px ÷ 1920 × 100 = cqw`).
- **Vertical:** 1080×1920 (9:16). **Square:** 1080×1080 (1:1).
- **Safe area:** `slide-pad` ~3.1cqw; decorations may bleed off edges.

**The container law (load-bearing).** Every frame ground sets `container-type: size`; ALL
frame-relative units are `cqw`/`cqh` against it — never `vw`. Borders/shadows scale in `cqw` so the
4px↔8px coupling holds proportionally; corners stay square.

## Colors

Tokens identical to the source. `{colors.offwhite}` is the default ground, but frames **cycle**
through `{colors.cream}`/`blue`/`pink`/`green`/`yellow` grounds — the cycle is the rhythm.
`{colors.black}` is every border + structural text; `{colors.white}` is card fills. The five pastels
are interchangeable with **no semantic meaning** — pair by juxtaposition (pink+blue+green trio,
cream+yellow warm pair). `{colors.yellow}` is the CTA + the one colored (close) shadow;
`{colors.black}` ground is the close surface. **No sixth pastel.**

## Typography

Two ramps. The **reading/chrome ramp** (Inter body 0.95cqw weight 500, Space Grotesk labels in px)
carries copy + chrome; the **display ramp** (Inter `heading-md` 2.1cqw → `heading-xl` 5cqw, weight
800–900 uppercase) carries every headline + stat.

- **Legibility floor:** any load-bearing line ≥ **1.4cqw**; px labels are chrome only.
- **Fit-to-measure:** size the headline to its length. Cap the block at **≤ 78cqw**; ≤3 words → `heading-xl`; 4–6 → `heading-lg`; 7+ → `heading-md`.
- **Inter display is uppercase, weight 800–900, negative-tracked** (−0.01..−0.03em); body weight 500 sentence case; **Space Grotesk labels uppercase 0.08em**. No sentence-case display, no untracked display.

## Depth & Surface

Hard offset shadow, solid black, zero blur, bottom-right:

- **0.8cqw (8px)** primary cards; **0.4cqw (4px)** chrome; **0.6cqw (6px)** hover.
- **Border-based depth** — the 4px/3px borders do much of the lift; shadow makes it "elevated."
- **Tilt** — ±2°–12° rotation breaks the grid for perceived dimension.
- **Inverted close** — 12px YELLOW shadow (and 6px white on close-btn) — the only colored shadows.

**Ceiling:** no blurred shadow, no rounded corner (save the stat-deco dot), no gradient depth.

## Shapes

- **0 radius everywhere** except the 12px stat-deco dot (50%). Square corners are the structural identity.

## Components

- **card-elevated / card-small** — the bordered+shadowed content cards (weight-coupled).
- **label-pill** — the universal eyebrow (border+shadow+pastel). **button-primary** — yellow CTA.
- **star-burst / stripe-block / bg-dot-grid / tilt-deco** — the reusable decoration units (one per frame min).
- **stat-deco-dot** — the lone round shape. **close-frame** — the inverted black+white+yellow-shadow closer.

## Frame Treatments

> Recipe: ground · container · composes · focal · chrome · accent · silence · Fixed/Free · density.
> Cycle the ground color; add ≥1 decoration per frame; open with a label-pill.

### 1 · Cover (identity · move: decorations puncture · left)

**Ground** `{colors.cream}` (or offwhite) + faint dot-grid. **Composes** label-pill, heading-xl, tilt-deco rect, star-burst, counter. **Focal** a 2–3 line Inter `heading-xl` uppercase, left, under a label-pill; tilted pastel rects + a star burst puncture the right. **Chrome** counter pill. **Accent** the decorations' pastels. **Silence** right third holds decorations. **Fixed** 4px/8px coupling, uppercase display, square. **Free** title, decoration placement/colors. **Density** comfortable.

### 2 · Feature Cards (catalog · move: 3-up bordered grid · blue ground)

**Ground** `{colors.blue}`, `slide-pad`. **Composes** label-pill, heading-lg, 3× card-elevated (icon-square + card-title + body). **Focal** three white bordered+shadowed cards. **Chrome** label-pill eyebrow. **Accent** the pastel icon-squares (pink/green/yellow). **Silence** tight — dense by design. **Fixed** 4px border + 8px shadow, square, uppercase card-titles. **Free** card content, icon hues. **Density** dense-exception.

### 3 · Stat Grid (data · move: tilted stat cards · green ground)

**Ground** `{colors.green}`, `slide-pad`. **Composes** label-pill, heading-lg, 3× card-small (tilted −2/+2°, stat-deco dot, stat-number + label). **Focal** three tilted bordered stat cards. **Accent** the deco-dots' pastels + black stat numerals. **Silence** moderate. **Fixed** alternating tilt, 3px+4px, round deco-dot only. **Free** figures (from script), dot hues. **Density** dense-exception.

### 4 · Closing Plate (closer · move: inverted black · centered)

**Ground** `{colors.black}`. **Composes** close-frame (4px white border, 12px yellow shadow), label-pill (inverted), close-title, star-burst. **Focal** a white `close-title` inside the white-bordered frame with the yellow offset shadow; a pink star punctures a corner. **Accent** the yellow shadow + pink star. **Silence** ~50%. **Fixed** white-on-black, 12px yellow shadow (only here), square. **Free** sign-off, star placement. **Density** low.

### 5 · Quote (quote · move: bordered quote frame · pink ground)

**Ground** `{colors.pink}` (or offwhite). **Composes** label-pill, quote-text in a card-elevated, attribution. **Focal** an Inter `quote-text` (900 uppercase) inside a white bordered+shadowed frame. **Accent** the ground + one decoration. **Silence** moderate. **Fixed** uppercase quote, 4px/8px. **Free** quote, ground. **Density** comfortable.

### 6 · Timeline (process · move: stepped bordered cards · offwhite)

**Ground** `{colors.offwhite}`. **Composes** label-pill, heading-lg, 3–4 card-small steps + step-connectors. **Focal** a row of bordered step cards linked by black connector bars, each a pastel + step-num. **Accent** the step pastels. **Silence** moderate. **Fixed** 3px+4px steps, square, connectors. **Free** steps, hues. **Density** standard.

## Composition Rules

### Do

- Pair **4px borders with 8px shadows**, **3px with 4px** — the coupling is non-negotiable.
- **Cycle pastel grounds** across frames; keep the deck visually rhythmic.
- Set Inter display **uppercase, 800–900, negative-tracked**; open every region with a **label-pill**.
- Render shadows **solid black, zero blur, bottom-right**; add **≥1 decoration** (tilt/star/stripe/dots) per frame.
- Use **yellow** for CTAs; use the **inverted black + 12px yellow shadow** close-frame for the closer.
- Tilt decorations ±2°–12°; lean left on most frames.

### Don't

- No rounded corners (save the stat-deco dot); no blurred shadows.
- No colored borders (black only, save the close-frame white); no sixth pastel.
- No sentence-case Inter display; no untracked display; no label as plain text.
- Don't keep everything perfectly aligned (tilt is the signature); don't leave corners empty.
- Don't blow a headline edge-to-edge — fit to measure.

## Aspect-Ratio Behavior

| Treatment     | 16:9                          | 9:16                         | 1:1                      |
| ------------- | ----------------------------- | ---------------------------- | ------------------------ |
| Cover         | title left, decorations right | title top, decorations below | title, fewer decorations |
| Feature Cards | 3 across                      | 3 stacked                    | 2+1                      |
| Stat Grid     | 3 tilted across               | 3 tilted stacked             | 2×2                      |
| Closing       | centered close-frame          | centered, taller             | centered                 |
| Quote         | quote frame                   | quote stacked                | centered                 |
| Timeline      | horizontal steps              | vertical (connectors hidden) | 2×2                      |

`slide-pad` holds on the short edge; re-step display above the 1.4cqw floor. Decoration count drops
on tighter ratios so the frame stays bordered, not cluttered.

## Approved Entities

No real customers, logos, or vendors are defined in the source — render any such mark as a
placeholder. Pastel fills, decorations, and tilts are content-agnostic.

## Numerals & Claims (hard rule)

Never invent figures, stats, or counts at frame scale. Render slots as `— figure —`, `{metric}`,
`N×`. Stat cards and charts carry placeholders until the script supplies values. Slide counters and
list numbers are decorative.

## Pre-Render Self-Audit

- **Squint** — one Inter display moment dominates; cards read as a system.
- **Silence** — only feature/stat grids run dense; cover/quote/close keep air with decorations.
- **Borders/shadows** — 4px↔8px / 3px↔4px coupling holds; solid black, zero blur.
- **Color** — pastel ground cycles; black borders only (white on close); no sixth pastel.
- **Type** — Inter uppercase 800–900 negative-tracked, fit-to-measure; Space Grotesk labels 0.08em; ≥1.4cqw floor.
- **Shape** — square corners (only stat-deco dot round); ≥1 tilt/decoration per frame.
- **Fabrication** — every numeral traces to the script, else placeholder.

## Known Gaps

- **Motion intentionally out of scope.** frame.md specifies composition only; the source toggles slides via display, no transition.
- **Inter + Space Grotesk via Google Fonts.** CJK: Noto Sans SC 900 (sentence case — the uppercase signal drops); lean harder on borders/shadows/decoration to carry the brutalist identity.
- **9:16 / 1:1 are guidance**; verify the floor and that decoration count scales down.
- Star bursts (clip-path), stripe blocks, dot grids, and tilts are CSS-only; no external imagery is required.


<!-- ===== FILE: hyperframes/hyperframes-creative/frame-presets/blue-professional/FRAME.md ===== -->

---
version: alpha
name: Blue Professional — Frame (video / frame layer)
description: >
  Video-first companion to Blue Professional's design.md. The unit is the frame (1920×1080). Atoms
  are identical and sacred — the warm cream canvas, a single saturated cobalt (#1e2bfa) as the only
  accent, the three-step gray text ladder, Space Grotesk (display/numerals/chrome) + Inter (body),
  soft cobalt-tinted cards (4% fill / 20% border / 10–14px radius) with NO shadows, pill chrome, and
  the cobalt progress bar. Composition + frame scale rewritten. Motion out of scope.
unit: the frame — 1920×1080 primary; 9:16 and 1:1 documented
principle: atoms are sacred · composition is free · numbers come from the script

colors:
  bg: "#fdfae7"
  primary: "#1e2bfa"
  text: "#111111"
  text-muted: "#6b6b6b"
  text-light: "#9a9a9a"
  accent-light: "rgba(30,43,250,0.08)"
  accent-medium: "rgba(30,43,250,0.15)"
  border: "rgba(30,43,250,0.2)"
  card-bg: "rgba(30,43,250,0.04)"
  positive: "#059669"
  negative: "#dc2626"

radii:
  pill: "100px"
  card-lg: "14px"
  card-md: "12px"
  card-sm: "10px"
  bar: "6px"
  circle: "50%"

typography:
  # — reading ramp (Inter body + Space Grotesk chrome) —
  body:    { fontFamily: "Inter", cqw: 0.85, weight: 400, lineHeight: 1.6, color: "text-muted" }
  h4-eyebrow:{ fontFamily: "Space Grotesk", cqw: 0.8, weight: 600, tracking: "0.08em", upper: true, color: "primary" }
  tag:     { fontFamily: "Space Grotesk", px: 12, weight: 500, color: "primary" }
  counter: { fontFamily: "Space Grotesk", px: 13, weight: 500, tracking: "0.05em", color: "text-muted" }
  # — display / numerical ramp (Space Grotesk, near-black headings / cobalt numerals) —
  h3:      { fontFamily: "Space Grotesk", cqw: 1.25, weight: 500, lineHeight: 1.3, tracking: "-0.02em", color: "text" }
  stat-num:{ fontFamily: "Space Grotesk", cqw: 1.9, weight: 700, lineHeight: 1.0, color: "primary" }
  blockquote:{ fontFamily: "Space Grotesk", cqw: 2.4, weight: 500, lineHeight: 1.35, color: "text" }
  h2:      { fontFamily: "Space Grotesk", cqw: 2.6, weight: 600, lineHeight: 1.1, tracking: "-0.02em", color: "text" }
  metric-value:{ fontFamily: "Space Grotesk", cqw: 3.0, weight: 700, lineHeight: 1.0, color: "primary" }
  h1:      { fontFamily: "Space Grotesk", cqw: 4.2, weight: 700, lineHeight: 1.08, tracking: "-0.02em", color: "text" }
  quote-mark:{ fontFamily: "Space Grotesk", cqw: 8.0, weight: 700, lineHeight: 0.5, color: "primary", opacity: 0.15 }

spacing:
  pad-x: "5cqw"
  pad-y-top: "5cqw"
  gap-cards: "1.4cqw"
  accent-line: "60px × 4px"

components:
  card-tinted:
    backgroundColor: "{colors.card-bg}"
    border: "1.5px solid {colors.border}"
    rounded: "{radii.card-lg}"
    shadow: "none"
    description: "Universal content card. Never solid-colored, never opaque-bordered, NO shadow."
  metric-card:
    backgroundColor: "{colors.card-bg}"
    border: "1.5px solid {colors.border}"
    rounded: "{radii.card-lg}"
    typography: "{typography.metric-value} ({colors.primary}) + {typography.metric-label} + {typography.metric-desc}"
    description: "+ optional inline ↑/↓ change chip ({colors.positive}/{colors.negative} text, no fill)."
  tag-pill:
    backgroundColor: "{colors.accent-light}"
    textColor: "{colors.primary}"
    rounded: "{radii.pill}"
    typography: "{typography.tag}"
    description: "Top-right of the slide-header."
  cta-button:
    backgroundColor: "{colors.primary}"
    textColor: "{colors.bg}"
    rounded: "{radii.pill}"
    typography: "Space Grotesk 600"
    shadow: "soft cobalt on hover only — the system's only shadow"
    description: "The one solid element."
  accent-line:
    backgroundColor: "{colors.primary}"
    size: "60×4, 2px radius"
    description: "Above cover titles / eyebrow separators."
  bar-track:
    backgroundColor: "{colors.accent-light}"
    fill: "{colors.primary} (display:block so width resolves)"
    rounded: "{radii.bar}"
    description: "28px track; fill carries the value."
  step-circle:
    backgroundColor: "{colors.primary}"
    textColor: "{colors.bg}"
    rounded: "50%"
    size: "56px"
    description: "Sequential steps fade opacity 1.0→0.85→0.7→0.55."
  split-highlight:
    backgroundColor: "{colors.accent-light}"
    borderLeft: "4px solid {colors.primary}"
    rounded: "{radii.card-md}"
    description: "Inline pull-quote callout."
  slide-header:
    typography: "{typography.h4-eyebrow} (cobalt) left, tag-pill right; {typography.h2} below"
    description: "Top band of every content frame."
  atmosphere:
    elements: "clipped diagonal cobalt-tint panel, 3×3 cobalt dot grid, concentric closing rings"
    description: "Cover/closing only. Never on content frames."
  progress-bar:
    backgroundColor: "{colors.primary}"
    size: "3px tall, bottom edge, width grows with index"
    description: "Persistent progress strip."
---

# Blue Professional — Frame (video / frame layer)

## Overview

Blue Professional at frame scale is a **consulting-grade system: restraint with one strong
commitment.** A warm cream canvas and a single saturated cobalt that carries every accent —
eyebrow, metric, CTA, chart fill, progress bar. No secondary brand color, no pastels, just cream,
cobalt, and a tight ladder of grays. The register is investment-research / McKinsey briefing:
measured, data-dense without crowding, executive-readable at distance.

The voice is two faces in fixed roles: **Space Grotesk** (display, every numeral, all chrome —
eyebrows uppercase 0.08em) and **Inter** (body, muted gray, line 1.6). Headlines are near-black;
cobalt is reserved for accent moments. Depth is **soft and tinted** — 4% cobalt card fills with 20%
cobalt borders and 10–14px radii — never shadowed. The lack of harsh shadows is the premium signal.

**Key characteristics at frame scale:**

- **Warm cream ground** on every frame; **single cobalt** as the only accent.
- **Space Grotesk** (display/numerals/chrome) + **Inter** (body) — near-black headlines, cobalt numerals.
- **Tinted cards** — cobalt 4% fill, cobalt 20% 1.5px border, 10–14px radius, **no shadow**.
- **Pill chrome** (100px) — tag pills + the one solid cobalt CTA; cobalt **progress bar**.
- **Soft rounded corners everywhere** (no square corners save the progress bar).
- **Atmosphere** (diagonal panel, dot grid, concentric rings) on cover/closing only.

## The Frame

### Frame Craft Bar

Three eyeball tests gate every frame before any structural check:

- **Squint** — one **near-black headline or cobalt numeral** dominates at 3–6× its neighbor.
- **Silence** — content frames read **balanced, not crowded**; the **dashboard is the one dense exception**.
- **Restraint** — a **single cobalt accent** carries everything; headlines stay near-black (never cobalt); no shadows (tinted cards do the lift); positive/negative inline-text only.
- **Reference** — aim at an **investment-research / McKinsey quarterly briefing**; failure looks like a **heavy-outlined, multi-color dashboard**.

- **Primary:** 1920×1080 (16:9). Display authored in **`cqw`** (`px ÷ 1920 × 100 = cqw`).
- **Vertical:** 1080×1920 (9:16). **Square:** 1080×1080 (1:1).
- **Safe area:** `pad-x` 5cqw; bottom reserves room for the counter + progress bar.

**The container law (load-bearing).** Every frame ground sets `container-type: size`; ALL
frame-relative units are `cqw`/`cqh` against it — never `vw`. Card radii stay px (10–14px); the
pill radius stays 100px; borders stay 1–1.5px.

## Colors

Tokens identical to the source. `{colors.bg}` cream is the universal ground; `{colors.primary}`
cobalt is the **only** accent — every eyebrow, numeral, CTA, chart fill, progress bar, and the 4px
highlight left-rule. Headlines are `{colors.text}` near-black (never cobalt); body is
`{colors.text-muted}`; tertiary is `{colors.text-light}`. Cards fill `{colors.card-bg}` (4%) with
`{colors.border}` (20%) borders. `{colors.positive}`/`{colors.negative}` appear **only inline** on
directional change chips — never as fills. **No second accent color.**

## Typography

Two ramps. The **reading ramp** (Inter body 0.85cqw muted; Space Grotesk eyebrow uppercase 0.08em
cobalt) carries copy + chrome; the **display/numerical ramp** (Space Grotesk `h3` 1.25cqw → `h1`
4.2cqw near-black; numerals `stat-num`/`metric-value` in cobalt) carries headings and figures.

- **Legibility floor:** any load-bearing line ≥ **1.4cqw**; px chrome (tag/counter) is colophon only.
- **Fit-to-measure:** size the headline to its length. Cap the block at **≤ 78cqw**; ≤3 words → `h1`; 4–6 → `h2`; 7+ → `h3`. Cobalt numerals scale `metric-value`→`stat-num` by card size.
- **Headlines near-black, −0.02em**; **eyebrows cobalt, uppercase, 0.08em**; **numerals cobalt 600–700**; **body Inter 400 muted, line 1.6**. No italic, no uppercase body, no cobalt headline.

## Depth & Surface

Soft and tinted — never offset. Depth from:

- **Tinted cards** — 4% cobalt fill + 20% cobalt 1.5px border + 10–14px radius reads as lifted without offset.
- **Border-left accent** — the 4px cobalt rule on split-highlight blocks pulls a callout forward.
- **Rounded corners** — the 10–14px radius is part of the softness; square corners break it.

**Ceiling:** zero box-shadow on content (the only shadow is a soft cobalt CTA _hover_); no opaque cobalt borders; no harsh outlines.

## Shapes

- **100px** — tag pills, CTA, nav buttons (pill chrome).
- **14/12/10px** — cards by size (large metric / standard stat / detail + mini).
- **6px** — bar tracks + fills. **50%** — step circles, nav circles, dots, closing rings.
- **0** — only the progress bar. No square-cornered content.

## Components

- **card-tinted / metric-card** — the universal soft-tint content cards (no shadow).
- **tag-pill / cta-button / accent-line** — the cobalt pill chrome + the one solid CTA + the 60×4 rule.
- **bar-track / step-circle / split-highlight** — cobalt data + sequence + callout patterns.
- **slide-header** (eyebrow + tag pill) — the structural rhythm; **atmosphere** (diagonal/dots/rings) on cover/closing only; **progress-bar** on every frame.

## Frame Treatments

> Recipe: ground · container · composes · focal · chrome · accent · silence · Fixed/Free · density.
> Atmosphere only on cover/closing; content frames carry the slide-header rhythm.

### 1 · Cover (identity · move: diagonal accent · left)

**Ground** cream + the clipped diagonal cobalt-tint panel (right ~36%) + a 3×3 cobalt dot grid.
**Composes** accent-line, meta, h1, body sub. **Focal** a 2-line Space Grotesk `h1` near-black, left,
under a cobalt accent-line + meta. **Chrome** counter + progress bar. **Accent** the cobalt line +
diagonal panel. **Silence** the diagonal panel holds the right third. **Fixed** near-black h1, cobalt
accents, atmosphere here only. **Free** title, meta. **Density** low.

### 2 · Dashboard (data · move: 3-up metric grid · the dense frame)

**Ground** cream, `pad-x`. **Composes** slide-header (eyebrow + tag-pill), h2, 3× metric/tinted card.
**Focal** a row of tinted cards — cobalt `metric-value` + Inter label + muted desc + optional
green/red change chip. **Chrome** eyebrow left, tag-pill right; progress bar. **Accent** the cobalt
numerals. **Silence** tight — the density exception. **Fixed** 4% tint cards, 20% borders, no shadow,
cobalt numerals. **Free** figures (from script), labels. **Density** dense-exception.

### 3 · Bar Ranking (data · move: cobalt bars · left)

**Ground** cream, `pad-x`. **Composes** eyebrow, h2, bar-track rows. **Focal** 3–5 labeled
cobalt-fill bars on cobalt-8% tracks with cobalt percentages. **Chrome** eyebrow; progress bar.
**Accent** the cobalt fills + figures. **Silence** moderate. **Fixed** 6px tracks, cobalt fills.
**Free** rows, values (from script). **Density** standard.

### 4 · Pull Quote (quote · move: concentric rings · centered)

**Ground** cream, centered, with faint concentric closing-rings behind. **Composes** quote-mark,
blockquote, cite. **Focal** a Space Grotesk `blockquote` near-black under a 15%-opacity cobalt
quote-mark; an uppercase cobalt-muted cite beneath. **Accent** the faint rings + quote-mark. **Silence**
~55%. **Fixed** near-black quote, soft rings. **Free** quote, cite. **Density** low.

### 5 · Split + Highlight (content · move: asymmetric split · left)

**Ground** cream, two columns. **Composes** eyebrow, h2, body, split-highlight block. **Focal** an
Inter body column beside a cobalt-8% highlight block (4px cobalt left rule) carrying an inline pull
quote. **Accent** the highlight's left rule. **Silence** generous gutter. **Fixed** tinted highlight,
4px cobalt rule. **Free** body, callout. **Density** standard.

### 6 · Closing / CTA (closer · move: centered rings + CTA)

**Ground** cream + concentric closing-rings. **Composes** accent-line, h1, body, cta-button. **Focal**
a Space Grotesk `h1` near-black, centered, with the one solid cobalt `cta-button` pill below. **Accent**
the CTA + rings. **Silence** ~60%. **Fixed** one CTA, near-black h1, soft rings. **Free** sign-off, CTA
label. **Density** low.

## Composition Rules

### Do

- Start every frame on **warm cream**; let **cobalt carry every accent** (eyebrow, numeral, CTA, bar, progress).
- Set headlines **near-black, −0.02em**; eyebrows **cobalt uppercase 0.08em**; numerals **cobalt 600–700**.
- Use **tinted cards** (4% fill, 20% border, 10–14px radius, no shadow); body Inter 400 muted, line 1.6.
- Keep all chrome **pill-shaped (100px)**; one solid cobalt CTA per closing frame.
- Reserve **atmosphere** (diagonal panel, dots, rings) for cover/closing; content frames keep the slide-header rhythm.
- Lean left on cover/dashboard/split, centered on quote/closer.

### Don't

- No second accent color; no cobalt headlines.
- No drop shadows on content (only the soft cobalt CTA hover); no opaque cobalt borders.
- No square corners (save the progress bar); no font substitutes; no uppercase body.
- Don't use the green/red change chips as general accents — directional comparisons only.
- Don't fill space with heavier borders — add substance; don't blow a headline edge-to-edge.

## Aspect-Ratio Behavior

| Treatment         | 16:9                       | 9:16                           | 1:1                      |
| ----------------- | -------------------------- | ------------------------------ | ------------------------ |
| Cover             | title left, diagonal right | title top, diagonal band below | title upper, dots corner |
| Dashboard         | 3 cards across             | 3 stacked                      | 2×2                      |
| Bar Ranking       | 3–5 bars                   | 3–5 bars (tighter)             | 3 bars                   |
| Pull Quote        | centered, rings behind     | centered, taller               | centered                 |
| Split + Highlight | side-by-side               | stacked                        | stacked                  |
| Closing / CTA     | centered + CTA             | centered + CTA                 | centered + CTA           |

`pad-x` holds on the short edge; re-step display above the 1.4cqw floor. The diagonal cover panel
becomes a top/bottom band on 9:16. Numerals stay Latin Arabic digits in CJK builds.

## Approved Entities

No real customers, logos, or vendors are defined in the source — render any such mark as a
placeholder. Figures, metrics, and quotes are content; the system supplies cream + cobalt + grays.

## Numerals & Claims (hard rule)

Never invent figures, financials, percentages, or dates at frame scale. Render slots as `— figure —`,
`{metric}`, `+NN%`, `↑ —`. Metric cards, bar values, and stat cells especially carry placeholders
until the script supplies them. Directional chips require a real comparison from the script.

## Pre-Render Self-Audit

- **Squint** — one near-black headline or cobalt numeral dominates per frame.
- **Silence** — content frames balanced, not crowded; only the dashboard runs dense.
- **Single accent** — cobalt only; headlines near-black; positive/negative inline only.
- **Type** — Space Grotesk headings −0.02em near-black, cobalt eyebrows 0.08em + numerals; Inter body muted line 1.6; ≥1.4cqw floor.
- **Depth** — tinted cards (no shadow), soft rounded corners, 20% cobalt borders; no square content corners.
- **Anchor** — left on cover/dashboard/split, centered on quote/closer; atmosphere on cover/closing only.
- **Fabrication** — every numeral traces to the script, else placeholder.

## Known Gaps

- **Motion intentionally out of scope.** frame.md specifies composition only; the source's 500ms translateX transitions + bar-fill animations are deck mechanics.
- **Space Grotesk + Inter via Google Fonts.** CJK pairing (Noto Sans SC 700 display / Noto Serif SC 400 body) carries over; the eyebrow's uppercase+tracking signal weakens in CJK — pair it with the accent-line.
- **9:16 / 1:1 are guidance**; verify the floor and that the diagonal panel reflows to a band.
- Diagonal panel (clip-path), dot grid, concentric rings, and bars are CSS-only; no external imagery is required.


<!-- ===== FILE: hyperframes/hyperframes-creative/frame-presets/bold-poster/FRAME.md ===== -->

---
version: alpha
name: Bold Poster — Frame (video / frame layer)
description: >
  Video-first companion to Bold Poster's design.md. The unit is the frame (1920×1080). Atoms are
  identical and sacred — the four-color palette (white / brown-black ink / tomato red / off-white),
  the three-face stack (Shrikhand display tilted at poster scale, Libre Baskerville serif body,
  Space Grotesk mono chrome), the stacked text-shadow on red display, the 3px+1.5px double-border
  grid, red leftbar cards, red em-dash bullets, and the red progress bar. Composition + frame scale
  rewritten. Motion out of scope.
unit: the frame — 1920×1080 primary; 9:16 and 1:1 documented
principle: atoms are sacred · composition is free · numbers come from the script

colors:
  bg: "#FFFFFF"
  dark: "#1C1410"
  red: "#D8000F"
  light: "#F5F2EF"

typography:
  # — reading + chrome ramp —
  body:    { fontFamily: "Libre Baskerville", cqw: 0.85, weight: 400, lineHeight: 1.75, color: "dark" }
  body-cell:{ fontFamily: "Libre Baskerville", cqw: 0.7, weight: 400, lineHeight: 1.55 }
  label:   { fontFamily: "Space Grotesk", px: 10, weight: 600, tracking: "2px", upper: true, color: "red" }
  bullet-body:{ fontFamily: "Space Grotesk", cqw: 0.62, weight: 400, lineHeight: 1.45 }
  # — display / hero ramp (Shrikhand 400, tilted) —
  card-title:{ fontFamily: "Shrikhand", cqw: 1.9, weight: 400, lineHeight: 1.1, color: "dark" }
  cell-number:{ fontFamily: "Shrikhand", cqw: 2.7, weight: 400, lineHeight: 1.0, color: "red" }
  section-header:{ fontFamily: "Shrikhand", cqw: 3.3, weight: 400, lineHeight: 1.0, color: "dark" }
  red-quote:{ fontFamily: "Shrikhand", cqw: 4.7, weight: 400, lineHeight: 1.15, color: "bg", shadow: "stacked" }
  hero-title-bottom:{ fontFamily: "Shrikhand", cqw: 10.4, weight: 400, lineHeight: 0.9, color: "dark", rotate: "2deg" }
  hero-title:{ fontFamily: "Shrikhand", cqw: 11.5, weight: 400, lineHeight: 0.88, color: "dark" }
  hero-title-red:{ fontFamily: "Shrikhand", cqw: 13.5, weight: 400, lineHeight: 0.85, color: "red", rotate: "-4deg" }
  close-big:{ fontFamily: "Shrikhand", cqw: 13.5, weight: 400, lineHeight: 0.88, color: "red", rotate: "-5deg" }
  stat-big:{ fontFamily: "Shrikhand", cqw: 22.0, weight: 400, lineHeight: 0.82, color: "red", rotate: "-6deg" }

spacing:
  pad-slide: "3cqw 3.6cqw"
  gap-grid: "1.5cqw 2cqw"

components:
  progress-bar:
    backgroundColor: "{colors.red}"
    size: "0.5cqw tall, bottom edge, width grows with index"
    description: "The most prominent chrome."
  hero-title-stack:
    typography: "{typography.hero-title} + {typography.hero-title-red} + {typography.hero-title-bottom}"
    transform: "≥4 tilt (−4°/+2°), ≥1 line in {colors.red}"
    description: "A 3-line Shrikhand composition — the signature opener."
  stat-big:
    typography: "{typography.stat-big}"
    color: "{colors.red} (or {colors.bg} on red with stacked shadow)"
    transform: "rotate(-6deg)"
    description: "Hero numeral at poster scale."
  fin-grid:
    border: "0.3cqw solid {colors.dark} outer"
    rule: "0.15cqw solid {colors.dark} inner (touching at intersections)"
    rounded: "0"
    typography: "{typography.cell-number} ({colors.red}) + {typography.label} + {typography.body-cell}"
    description: "The double-border tabular signature."
  red-leftbar-card:
    borderLeft: "4px solid {colors.red}"
    padding: "0 0 0 ~1cqw"
    rounded: "0"
    shadow: "none"
    typography: "{typography.card-title} + {typography.body} + red em-dash bullets"
    description: "Editorial card cantilevered off a red left rule — no outline."
  red-panel:
    backgroundColor: "{colors.red}"
    textColor: "{colors.bg}"
    description: "Full-bleed statement surface; display carries the stacked text-shadow."
  dark-panel:
    backgroundColor: "{colors.dark}"
    textColor: "{colors.bg}"
    description: "Full-bleed dark statement surface; red accents."
  stacked-text-shadow:
    shadow: "2px 2px 0 rgba(28,20,16,.25), 4px 4px 0 rgba(28,20,16,.2), 6px 6px 0 rgba(28,20,16,.15)"
    appliesTo: "red display text on red panels only"
    description: "The ONLY shadow in the system — text-shadow, not box-shadow."
  bullet:
    marker: "red em-dash (—) or round (•) glyph at absolute-left"
    color: "{colors.red}"
    description: "No default disc bullets; capped at three."
---

# Bold Poster — Frame (video / frame layer)

## Overview

Bold Poster at frame scale is a **populist editorial poster** — vintage Italian sports-magazine
display, classical serif body, one saturated tomato red, grids ruled in ink. Every frame should
feel _printed_: heavy display type at poster scale, locked to one red accent, on a white/off-white
sheet (or a full red/dark statement panel), with decoration kept to a strict minimum.

The voice is a three-face stack: **Shrikhand** (heavy slab-script, weight 400 only, routinely
tilted −6°..+2°) carries every hero title, section header, stat, and card title; **Libre
Baskerville** (literary serif) carries every body paragraph — it's what makes the system feel
printed; **Space Grotesk** (uppercase, 2–3px tracked) is chrome only — labels, eyebrows, counters,
bullet bodies. The plane is flat; the _only_ shadow is the stacked text-shadow on red display.

**Key characteristics at frame scale:**

- **Four colors only** — white / brown-black ink / tomato red / off-white. Red is the lone accent.
- **Shrikhand display, tilted** (−6° stat, −5° close, −4° hero-red, +2° hero-bottom) — the signature movement.
- **Libre Baskerville serif body** (line 1.75); **Space Grotesk** chrome (uppercase tracked).
- **Double-border grids** (3px outer + 1.5px inner ink); **red leftbar cards**; **red em-dash bullets** (max 3).
- **Stacked text-shadow** on red display — the only shadow; flat plane otherwise; square corners.
- **Red progress bar** at the bottom edge of every frame.

## The Frame

### Frame Craft Bar

Three eyeball tests gate every frame before any structural check:

- **Squint** — **one display moment dominates** at 3–6× everything else (the hero stack, `stat-big`, or `close-big`); nothing competes.
- **Silence** — statement frames reserve **~50–60% negative space**; the **financial grid is the one dense exception**.
- **Restraint** — **four colors only**, red the lone accent; one display moment per frame; the stacked text-shadow on red is the only shadow; bullets capped at three.
- **Reference** — aim at a **vintage Italian sports-magazine cover / mid-century European annual report**; failure looks like a **rounded, soft-shadowed multi-accent slide**.

- **Primary:** 1920×1080 (16:9). Display authored in **`cqw`** (`px ÷ 1920 × 100 = cqw`).
- **Vertical:** 1080×1920 (9:16). **Square:** 1080×1080 (1:1).
- **Safe area:** `pad-slide` ~3cqw — deliberately tight so the poster type crowds the frame.

**The container law (load-bearing).** Every frame ground sets `container-type: size`; ALL
frame-relative units are `cqw`/`cqh` against it — never `vw`. Borders stay px; rotation transforms hold.

## Colors

Tokens identical to the source. `{colors.bg}` white is the default ground; `{colors.dark}` is body,
borders, headers; `{colors.red}` is the only accent — every numeral, section rule, eyebrow,
leftbar, bullet, progress bar, and the full statement-panel ground. `{colors.light}` off-white
stripes alternating panels. **No fifth color** (no green/blue/yellow); categorical difference comes
from position, label, and tilt. Red is never body text, never a tint, never an untexted fill.

## Typography

Two ramps. The **reading/chrome ramp** (Baskerville body 0.85cqw, Space Grotesk labels in px)
carries copy + chrome; the **display ramp** (Shrikhand `section-header` 3.3cqw → `stat-big` 22cqw)
carries every statement and numeral.

- **Legibility floor:** any load-bearing line ≥ **1.4cqw**; mono labels are chrome only.
- **Fit-to-measure:** size the headline to its length. Cap the block at **≤ 78cqw**; ≤2 words → `stat-big`/`hero-title-red`; 3–4 → `hero-title`; 5+ → `section-header`. The hero is a stacked 3-line composition.
- **Shrikhand is weight 400, tilted on statement/hero elements, red on numerals**; **Baskerville body at line ≥1.5**; **Space Grotesk chrome uppercase, 2–3px**. Inline `<strong>` switches face to Space Grotesk 600. No italic display, no untilted red hero.

## Depth & Surface

Flat plane. Depth from:

- **Heavy borders** — 3px+1.5px double-border grids, 2px global-card outline, 4px red leftbar rules.
- **Surface inversion** — full-bleed red or dark statement panels.
- **Tilt** — rotated Shrikhand breaks the baseline for perceived dimension.
- **The single shadow** — stacked text-shadow on red display only (text-shadow, three steps).

**Ceiling:** no box-shadow, no rounded surface (square corners; only the hint pill is 4px), no gradient.

## Shapes

- **0 radius everywhere** except the hint pill (4px). Cards, cells, panels, callouts — sharp rectangles.

## Components

- **hero-title-stack** — the 3-line tilted opener. **stat-big** — the poster numeral.
- **fin-grid** — the double-border tabular signature. **red-leftbar-card** — the cantilevered editorial card.
- **red-panel / dark-panel** — statement surfaces. **stacked-text-shadow** — the one shadow.
- **bullet** — red em-dash (max 3). **progress-bar** — the red bottom strip.

## Frame Treatments

> Recipe: ground · register · composes · focal · chrome · accent · silence · Fixed/Free · density.
> One display moment per frame; statement frames reserve massive negative space.

### 1 · Hero Stack (identity · move: 3-line tilted stack · left)

**Ground** white. **Composes** hero-title-stack, label, body tagline, progress-bar. **Focal** a
3-line Shrikhand stack (e.g. ink / red-tilted / paper) — one red line, one+ tilted. **Chrome** mono
eyebrow + Baskerville tagline; bottom progress bar + counter. **Accent** the red line. **Silence**
right half open. **Fixed** Shrikhand 400, ≥1 tilt + ≥1 red, square. **Free** the words, line sizes.
**Density** low.

### 2 · Hero Stat (statement · move: poster numeral · red panel · centered)

**Ground** full `{colors.red}`. **Composes** stat-big, label, body sub. **Focal** a `stat-big`
numeral rotated −6° in white with the stacked shadow, centered, with a mono label above + Baskerville
sub below. **Accent** the ink stacked-shadow on white. **Silence** ~60%. **Fixed** white-on-red +
stacked shadow, −6° tilt. **Free** the figure (from script), label. **Density** low.

### 3 · Financial Grid (data · move: double-border matrix · the dense frame)

**Ground** white, `pad-slide`. **Composes** label, section-header, fin-grid. **Focal** a 3px-outer/
1.5px-inner ink grid of cells (red Shrikhand numeral + mono label + Baskerville body). **Chrome** mono
eyebrow; progress bar. **Accent** the red numerals. **Silence** tight — the density exception.
**Fixed** double-border, red numerals, serif body. **Free** figures (from script), labels. **Density** dense-exception.

### 4 · Pull Quote (quote · move: tilted/stacked display · red panel · left)

**Ground** full `{colors.red}`. **Composes** red-quote, Baskerville cite. **Focal** a 2-line Shrikhand
quote in white with the stacked shadow; a Baskerville cite beneath. **Accent** the stacked shadow.
**Silence** ~50%. **Fixed** white-on-red + stacked shadow. **Free** quote, cite. **Density** low.

### 5 · Editorial Cards (content · move: red leftbar cards · left)

**Ground** white (or alternating off-white stripes). **Composes** label, section-header, 2–3×
red-leftbar-card. **Focal** cards cantilevered off 4px red rules — Shrikhand title + Baskerville body

- red em-dash bullets (max 3). **Accent** the red left rules + bullets. **Silence** moderate. **Fixed**
  4px red leftbar, em-dash bullets, no outline. **Free** card content. **Density** standard.

### 6 · Closing Statement (closer · move: tilted close-big · centered/left)

**Ground** white or `{colors.dark}`. **Composes** close-big, label, body sub, progress-bar. **Focal**
a Shrikhand `close-big` (rotated −5°, red) sign-off; mono eyebrow + Baskerville contact line. **Accent**
the red tilted title. **Silence** ~60%. **Fixed** −5° tilt, red close-big. **Free** sign-off, contact.
**Density** low.

## Composition Rules

### Do

- Stack hero titles in 3 Shrikhand lines — at least one tilted, at least one red.
- Make every numeral **red Shrikhand**; tilt statement display **−5° to −6°**.
- Set eyebrows in **Space Grotesk 600 uppercase, 2–3px**, red; body in **Baskerville, line 1.75**.
- Build data grids with the **3px outer + 1.5px inner double border**; use red leftbar cards elsewhere.
- Use **red em-dash bullets, capped at three**; apply the stacked text-shadow on red display.
- One display moment per frame; reserve negative space on statement frames.

### Don't

- No second accent color; no rounded corners (square only, save the hint pill).
- No drop shadow — the stacked text-shadow on red is the only one.
- No font substitutes; no Shrikhand body, no Baskerville labels, no Space Grotesk headlines.
- No default disc bullets; no untilted red statement display.
- Don't crowd a statement frame; don't blow a long line edge-to-edge (step down).

## Aspect-Ratio Behavior

| Treatment       | 16:9                      | 9:16                     | 1:1                  |
| --------------- | ------------------------- | ------------------------ | -------------------- |
| Hero Stack      | stack left, tagline below | stack centered, taller   | stack, tagline below |
| Hero Stat       | numeral centered          | numeral centered, taller | centered             |
| Financial Grid  | 3 cells across            | 2 across / stacked       | 2×2                  |
| Pull Quote      | quote left                | quote stacked            | centered             |
| Editorial Cards | 2–3 across                | stacked                  | stacked              |
| Closing         | close-big centered        | close-big stacked        | centered             |

`pad-slide` stays tight on the short edge; re-step display so the line stays ≤78cqw above the floor.
Tilts hold; the progress bar spans the bottom on every ratio.

## Approved Entities

No real customers, logos, or vendors are defined in the source — render any such mark as a
placeholder. The system supplies type, one red, and ink rules, not brands.

## Numerals & Claims (hard rule)

Never invent figures, financials, percentages, or dates at frame scale. Render slots as `— figure —`,
`{metric}`, `+NN%`. Fin-grid cells and stat-big especially carry placeholders until the script
supplies them. Catalogue numbers / progress are decorative.

## Pre-Render Self-Audit

- **Squint** — one display moment dominates; nothing competes.
- **Silence** — statement frames reserve ~50–60% negative space; only the fin-grid runs dense.
- **Color** — four colors only; red is the lone accent; no red body text.
- **Type** — Shrikhand 400 tilted on statements, red numerals, fit-to-measure; Baskerville body line 1.75; mono chrome uppercase 2–3px; ≥1.4cqw floor.
- **Depth** — flat; the stacked text-shadow on red display is the only shadow; square corners.
- **Bullets** — red em-dash, capped at three.
- **Fabrication** — every numeral traces to the script, else placeholder.

## Known Gaps

- **Motion intentionally out of scope.** frame.md specifies composition only; the source's 550ms slide transitions are deck mechanics.
- **Shrikhand + Libre Baskerville + Space Grotesk via Google Fonts.** CJK: Noto Serif SC 900/400 + Noto Sans SC; Shrikhand's slab-script has no Hanzi equal — keep tilts + red + double-borders to carry the identity.
- **9:16 / 1:1 are guidance**; verify the one big line ≤78cqw per ratio and that tilts don't clip.
- Grids, leftbar cards, and the stacked shadow are CSS-only; no external imagery is required.


<!-- ===== FILE: hyperframes/hyperframes-creative/frame-presets/broadside/FRAME.md ===== -->

---
version: alpha
name: Broadside — Frame (video / frame layer)
description: >
  Video-first companion to Broadside's design.md. The unit is the frame (1920×1080). Atoms are
  identical and sacred — the two-register surface system (dark ink-black / fire-orange), massive
  Barlow in lowercase weight 900 treated as graphic primitive, IBM Plex Mono chrome (uppercase,
  0.14em), the single fire-orange accent, the flat plane, and 1px hairline dividers. Composition +
  frame scale rewritten for the frame. Motion out of scope.
unit: the frame — 1920×1080 primary; 9:16 and 1:1 documented
principle: atoms are sacred · composition is free · numbers come from the script

colors:
  ink-black: "#111111"
  ink-black-alt: "#1A1A18"
  fire-orange: "#E85D26"
  cream: "#F0ECE5"
  cream-muted: "#888880"
  cream-hint: "#505048"
  border-dark: "#282826"
  ink-on-orange-muted: "rgba(17,17,17,0.75)"
  ink-on-orange-hint: "rgba(17,17,17,0.55)"
  ink-on-orange-faint: "rgba(17,17,17,0.40)"
  ink-on-orange-border: "rgba(17,17,17,0.20)"

typography:
  # — reading ramp —
  body:    { fontFamily: "Barlow", cqw: 1.2, weight: 400, lineHeight: 1.6 }
  lead:    { fontFamily: "Barlow", cqw: 1.6, weight: 400, lineHeight: 1.5 }
  caption: { fontFamily: "Barlow", cqw: 0.9, weight: 400, lineHeight: 1.5 }
  label:   { fontFamily: "IBM Plex Mono", cqw: 0.72, weight: 500, tracking: "0.14em", upper: true }
  # — display / hero ramp (Barlow, lowercase, negative tracking) —
  h3:      { fontFamily: "Barlow", cqw: 2.8, weight: 600, lineHeight: 1.2, lower: true }
  quote-text:{ fontFamily: "Barlow", cqw: 3.8, weight: 700, lineHeight: 1.15, tracking: "-0.02em", lower: true }
  h2:      { fontFamily: "Barlow", cqw: 4.5, weight: 700, lineHeight: 1.1, tracking: "-0.02em", lower: true }
  stat-value:{ fontFamily: "Barlow", cqw: 5.5, weight: 900, lineHeight: 1.0, tracking: "-0.04em" }
  h1:      { fontFamily: "Barlow", cqw: 7.5, weight: 800, lineHeight: 0.9, tracking: "-0.03em", lower: true }
  fadelist-item:{ fontFamily: "Barlow", cqw: 7.5, weight: 900, lineHeight: 1.0, tracking: "-0.03em", lower: true }
  quote-mark:{ fontFamily: "Barlow", cqw: 10.0, weight: 900, lineHeight: 0.6 }
  fadelist-title:{ fontFamily: "Barlow", cqw: 10.5, weight: 900, lineHeight: 0.9, tracking: "-0.04em", lower: true }
  display: { fontFamily: "Barlow", cqw: 13.0, weight: 900, lineHeight: 0.88, tracking: "-0.04em", lower: true }

spacing:
  pad-x: "5.5cqw"
  pad-y: "5.5cqw"
  gap-lg: "3.5cqw"
  gap-md: "2cqw"
  gap-sm: "1cqw"

components:
  registers:
    dark: "ground {colors.ink-black}, text {colors.cream}, accent {colors.fire-orange}"
    orange: "ground {colors.fire-orange}, text {colors.ink-black}"
    description: "Two surfaces only — no cream/paper register. One register per frame."
  slide-chrome:
    rule: "1px solid {colors.border-dark} (dark) / 20% ink (orange)"
    placement: "top + bottom bars (label left, number right)"
    description: "SUPPRESSED on cover/chapter/statement/quote/end — declarative frames let type fill the field."
  kicker:
    typography: "{typography.label}"
    color: "{colors.fire-orange} (dark) / 55% ink (orange)"
    description: "Uppercase mono eyebrow."
  rule:
    backgroundColor: "{colors.fire-orange} (dark) / {colors.ink-black} (orange)"
    size: "36×2px"
    description: "Stub accent bar — the system's only ornament."
  broadside-num:
    typography: "{typography.label}"
    placement: "top-left of orange cover/chapter, low opacity"
    description: "Mono catalogue numeral."
  stat-card:
    borderTop: "1px solid {colors.border-dark}"
    typography: "{typography.stat-value} (orange on dark / ink on orange) + {typography.body} + {typography.label}"
    description: "Top-border-only block, no other borders."
  bullet:
    marker: "orange `/` mono via ::before"
    typography: "{typography.lead}"
    description: "Capped at THREE items."
  bar-track:
    borderLeft: "1px solid {colors.border-dark}"
    bars: "{colors.cream-hint}, one .accent {colors.fire-orange}"
    typography: "{typography.label} axis"
    description: "Vertical bar chart, left axis only."
  compare-panel:
    layout: "two equal panels split by a 1px vertical rule"
    payoff: "right panel may fill {colors.fire-orange}"
    description: "Before/after."
  fadelist:
    typography: "{typography.fadelist-item} ×3 at opacity 1.0/0.5/0.22 + {typography.fadelist-title}"
    description: "Three stacked words + one oversized title opposite."
---

# Broadside — Frame (video / frame layer)

## Overview

Broadside at frame scale is a **protest-poster system where type is so large it stops reading as
text and becomes graphic primitive.** Barlow `display` at 13cqw puts a single lowercase word
nearly across the frame. The system runs in **two registers**: a dark ink-black ground with cream
text for documentation, and a fire-orange ground with dark ink for declaration. Fire-orange is the
_only_ color — accent on dark, environment on orange. The plane is flat; hierarchy is weight, size,
and 1px hairlines.

**Barlow** carries every text role from display to body — expressive range from weight (400–900)
and size, not face contrast. **IBM Plex Mono** is chrome only (numbers, kickers, tags, axis labels,
the `/` bullet marker), always uppercase and tracked. Display is **lowercase** — the system's most
distinctive single decision, a deliberate inversion of the brutalist norm.

**Key characteristics at frame scale:**

- **Two registers** — dark (cream text) / orange (ink text). No cream/paper register.
- **Massive lowercase Barlow 900**, negative-tracked, as graphic primitive (display 13cqw).
- **Fire-orange is the only color** — accent on dark, full environment on orange.
- **IBM Plex Mono chrome** — uppercase, 0.14em; the `/` bullet marker; mono catalogue numbers.
- **Flat plane** — no shadow, no radius (save nav dots), no gradient; 1px hairlines carry structure.
- **Low density** — one statement per frame, bullets capped at three, chrome suppressed on declarative frames.

## The Frame

### Frame Craft Bar

Three eyeball tests gate every frame before any structural check:

- **Squint** — exactly **one display moment dominates** at 3–6× everything else; nothing competes.
- **Silence** — declarative frames read **45–55% empty**; the **stat grid is the one dense exception**.
- **Restraint** — **one register per frame**; **fire-orange is the only color** (accent on dark, environment on orange); one display moment; bullets capped at three.
- **Reference** — aim at **broadside printing / a SPACE10 report / a Wim Crouwel grid with one loud color**; failure looks like a **multi-accent corporate slide deck**.

- **Primary:** 1920×1080 (16:9). Type authored in **`cqw`** (`px ÷ 1920 × 100 = cqw`; or carry the source's `vw` 1:1).
- **Vertical:** 1080×1920 (9:16). **Square:** 1080×1080 (1:1).
- **Safe area:** `pad-x`/`pad-y` 5.5cqw — deliberately tight so the massive type crowds the frame edge.

**The container law (load-bearing).** Every frame ground sets `container-type: size`; ALL
frame-relative units are `cqw`/`cqh` against it — never `vw` (a `vw`-sized frame inflates when not
full-screen). 1px hairlines stay 1px.

## Colors

Tokens identical to the source, in two registers. **Dark:** `{colors.ink-black}` ground,
`{colors.cream}` text, `{colors.fire-orange}` accent (kickers, accent stat, bullet `/`, lead bar,
quote mark, rule stub). **Orange:** `{colors.fire-orange}` ground, `{colors.ink-black}` headlines +
body, with the dark-ink overlays (75/55/40/20%) as the muted tones. Choose one register per frame
and commit. **No second accent color** — on orange, emphasis is weight/opacity on the ink, never a
new hue. Cream text on orange does not exist (ink-on-fire is absolute).

## Typography

Two ramps. The **reading ramp** (Barlow body 1.2cqw, mono label 0.72cqw) carries copy + chrome; the
**display ramp** (Barlow `h2` 4.5cqw → `display` 13cqw, weight 700–900) carries every statement.

- **Legibility floor:** any load-bearing line ≥ **1.4cqw**; mono labels are chrome only.
- **Fit-to-measure:** size the headline to its length. Cap the block at **≤ 78cqw**; ≤2 words → `display`; 3–4 → `h1`; 5+ → `h2`. Broadside packs only ONE display moment per frame.
- **Barlow display is lowercase, weight 700–900, negative-tracked** (−0.04em largest, −0.02em h2). **Mono chrome is uppercase, 0.1em+.** No italic, no underline, no uppercase display.

## Depth & Surface

Flat plane, the only technique. Hierarchy from:

- **Weight + size contrast** — the dominant signal (900 lowercase display).
- **1px hairlines** — chrome bars, stat-card top, compare divider, bar-track left, chart baseline.
- **Color shift** — orange on ink, ink on cream, cream-muted on cream.
- **Negative space** — generous, intentional empty regions.

**Ceiling:** no box-shadow, no elevation, no rounded surface (save nav dots), no gradient ground.

## Shapes

- **0 radius everywhere** except nav dots (50%). Cards, panels, tags, stat blocks, bars — sharp rectangles.

## Components

- **registers** — the two-surface system. **slide-chrome** — optional hairline bars, suppressed on declarative frames.
- **kicker** (mono eyebrow) / **rule** (36×2 stub) / **broadside-num** (catalogue mark) — the chrome ornament set.
- **stat-card** (top-border only) / **bullet** (orange `/`, max 3) / **bar-track** (one accent bar) / **compare-panel** (orange payoff) / **fadelist** (1.0/0.5/0.22 stack).

## Frame Treatments

> Recipe: ground · register · composes · focal · chrome · accent · silence · Fixed/Free · density.
> One statement per frame; chrome suppressed on declarative frames.

### 1 · Cover (identity · move: massive type · ORANGE register · left)

**Ground** fire-orange. **Composes** broadside-num, rule, kicker, display, lead. **Focal** a 1–2 word
Barlow `display` (13cqw) lowercase in ink, left-anchored, over a small ink rule stub + mono kicker; a
Barlow lead line beneath in 75% ink. **Chrome** mono catalogue number top-left, mono meta top-right
(no chrome bars). **Accent** the ink itself is the pop on orange. **Silence** ~45%. **Fixed** ink-on-fire,
lowercase 900, flat. **Free** the word, kicker, lead. **Density** low.

### 2 · Statement (declarative · move: type IS composition · DARK register · left)

**Ground** ink-black. **Composes** kicker, display. **Focal** a 2–4 word Barlow `display`/`h1`
lowercase in cream, with ONE clause inked `{colors.fire-orange}`. **Chrome** mono kicker; no bars.
**Accent** the orange clause. **Silence** ~55%. **Fixed** lowercase 900, one orange clause, flat.
**Free** the statement, which clause is orange. **Density** low.

### 3 · Stat Grid (data · move: top-border cards · DARK · the dense frame)

**Ground** ink-black, chrome bars present. **Composes** slide-chrome, kicker, 3× stat-card. **Focal** a
row of three top-border-only stat-cards — big Barlow-900 numeral in `{colors.fire-orange}`, Barlow
label, mono note. **Chrome** top + bottom hairline bars (label + number). **Accent** the orange
numerals. **Silence** moderate — the density exception. **Fixed** top-border-only cards, orange
numerals, 1px hairlines. **Free** figures (from script), labels. **Density** dense-exception.

### 4 · Fadelist (narrative · move: opacity stack · DARK)

**Ground** ink-black. **Composes** fadelist (3 stacked Barlow-900 words at 1.0/0.5/0.22), fadelist-title.
**Focal** the three-stage word stack opposite an oversized display title in `{colors.fire-orange}`
(before/during/after). **Accent** the orange title. **Silence** moderate. **Fixed** the opacity
ladder, lowercase 900. **Free** the three words, the title. **Density** low-moderate.

### 5 · Pull Quote (quote · move: oversized mark · DARK · left)

**Ground** ink-black, chrome suppressed. **Composes** quote-mark, quote-text, attribution. **Focal** a
Barlow `quote-text` (700, lowercase) at ≤78cqw under an oversized fire-orange `quote-mark` (10cqw,
line-height 0.6). **Chrome** mono attribution (name + role). **Accent** the orange quote mark. **Silence**
~50%. **Fixed** orange mark, lowercase quote. **Free** quote, attribution. **Density** low.

### 6 · Compare (argument · move: split + orange payoff · DARK→ORANGE)

**Ground** ink-black left panel + fire-orange right (payoff) panel, 1px divider. **Composes**
compare-panel pair, kicker, h3. **Focal** two panels — left documents (cream on dark), right declares
(ink on orange). **Chrome** mono panel labels. **Accent** the orange payoff panel. **Silence** moderate.
**Fixed** ink-on-fire right panel, 1px divider, flat. **Free** the before/after content. **Density** standard.

## Composition Rules

### Do

- Set every Barlow display in **lowercase weight 900**, negative-tracked — the system's signature.
- Use **fire-orange as full environment** on declarative frames, the **lone accent** on dark.
- Keep chrome in **IBM Plex Mono uppercase, 0.14em**; use the `/` mono bullet marker.
- **Cap bullets at three; one statement per frame**; build hierarchy from weight, size, 1px hairlines.
- Suppress chrome bars on cover/chapter/statement/quote/end; let type fill the field.
- Lean left on most frames; the type IS the composition.

### Don't

- Never uppercase Barlow display; never add a second accent color.
- Never put cream text on orange (ink-on-fire is absolute); never a cream/paper register.
- No drop shadow, no rounded surface (save nav dots), no gradient ground.
- No serif companion; chrome is never Barlow.
- Don't pack two display moments into one frame; don't blow a long line edge-to-edge — step down.

## Aspect-Ratio Behavior

| Treatment  | 16:9                       | 9:16                       | 1:1              |
| ---------- | -------------------------- | -------------------------- | ---------------- |
| Cover      | word left, lead below      | word top, lead below       | centered word    |
| Statement  | display left               | display stacked taller     | display centered |
| Stat Grid  | 3 across                   | 3 stacked                  | 2+1              |
| Fadelist   | stack + title side-by-side | stack over title           | stack over title |
| Pull Quote | mark + quote left          | mark top, quote below      | centered         |
| Compare    | side-by-side panels        | stacked (dark over orange) | stacked          |

`pad-x` holds tight on the short edge; re-step display so the one big line stays ≤78cqw and above the
1.4cqw floor. Mono chrome stays Latin/digit-only.

## Approved Entities

No real customers, logos, or vendors are defined in the source — render any such mark as a
placeholder (the dashed `img-placeholder` at 55cqh). The system supplies type and one color, not brands.

## Numerals & Claims (hard rule)

Never invent figures, percentages, dates, or counts at frame scale. Render slots as `— figure —`,
`{metric}`, `NN%`. Stat-card numerals and bar heights carry placeholders until the script supplies
them. Catalogue numbers (No. 01) are decorative chrome and may be sequential.

## Pre-Render Self-Audit

- **Squint** — exactly one display moment dominates; nothing competes.
- **Silence** — declarative frames ~45–55% empty; only the stat grid runs dense.
- **Register** — one register per frame; ink-on-fire on orange, cream on dark; no second hue.
- **Type** — Barlow lowercase 900 negative-tracked, fit-to-measure; mono chrome uppercase 0.14em; ≥1.4cqw floor.
- **Depth** — 0 shadow, 0 radius (save nav dots); 1px hairlines only.
- **Bullets** — capped at three, orange `/` marker.
- **Fabrication** — every numeral traces to the script, else placeholder.

## Known Gaps

- **Motion intentionally out of scope.** frame.md specifies composition only; the source's 0.8s deck slide + per-element entry animations are deck mechanics.
- **Barlow + IBM Plex Mono via Google Fonts**; Noto Sans SC is the CJK fallback (the lowercase-display signal has no CJK equivalent — the two-register color system carries the identity, per the source).
- **9:16 / 1:1 are guidance**; verify the one big line stays ≤78cqw and above the floor per ratio.
- Bars, compare panels, and the dashed image placeholder are CSS-only; no external imagery is required.


<!-- ===== FILE: hyperframes/hyperframes-creative/frame-presets/capsule/FRAME.md ===== -->

---
version: alpha
name: Capsule — Frame (video / frame layer)
description: >
  Video-first companion to Capsule's design.md. The unit is the frame (1920×1080). Atoms are
  identical and sacred — the pill geometry (9999px small / 2rem cards) with a 2px ink outline on
  everything, the sun-bleached cream canvas, the nine-color candy palette, Bodoni Moda + Space
  Grotesk, soft hard-offset shadows (4/6/8/12px in 8% ink), floating decorative-pill wallpaper,
  radial accent glows, and the grain overlay. Composition + frame scale rewritten. Motion out of scope.
unit: the frame — 1920×1080 primary; 9:16 and 1:1 documented
principle: atoms are sacred · composition is free · numbers come from the script

colors:
  cream: "#F5F5F0"
  ink: "#1A1A1A"
  outline: "#1E1E1E"
  white: "#FFFFFF"
  coral: "#E85D4E"
  lime: "#C4D94E"
  lavender: "#C5B5E0"
  sky: "#8BB4F7"
  violet: "#A06CE8"
  yellow: "#F2D160"
  peach: "#F5B895"
  mint: "#A8E6CF"
  shadow: "rgba(26,26,26,0.08)"

typography:
  # — reading ramp (Space Grotesk) —
  body:      { fontFamily: "Space Grotesk", cqw: 0.85, weight: 400, lineHeight: 1.6 }
  subtitle:  { fontFamily: "Space Grotesk", cqw: 0.95, weight: 400, tracking: "0.18em", upper: true }
  pill-text: { fontFamily: "Space Grotesk", cqw: 0.75, weight: 600, tracking: "0.12em", upper: true }
  label:     { fontFamily: "Space Grotesk", px: 14, weight: 500, tracking: "0.1em", upper: true }
  # — display / hero ramp (Bodoni Moda, ink, sentence case) —
  card-headline:{ fontFamily: "Bodoni Moda", cqw: 1.9, weight: 700, lineHeight: 1.1 }
  orbit-numeral:{ fontFamily: "Bodoni Moda", cqw: 2.6, weight: 700, lineHeight: 1.0 }
  quote-display:{ fontFamily: "Bodoni Moda", cqw: 4.2, weight: 600, lineHeight: 1.3, tracking: "-0.01em" }
  stat-number: { fontFamily: "Bodoni Moda", cqw: 3.6, weight: 800, lineHeight: 1.0, tracking: "-0.03em" }
  section-headline:{ fontFamily: "Bodoni Moda", cqw: 4.0, weight: 700, lineHeight: 1.05, tracking: "-0.01em" }
  headline:    { fontFamily: "Bodoni Moda", cqw: 5.0, weight: 700, lineHeight: 1.05, tracking: "-0.02em" }
  closing-display:{ fontFamily: "Bodoni Moda", cqw: 8.5, weight: 800, lineHeight: 0.95, tracking: "-0.03em" }
  display:     { fontFamily: "Bodoni Moda", cqw: 12.0, weight: 800, lineHeight: 0.88, tracking: "-0.03em" }

spacing:
  pad: "5cqw"
  gap-md: "2cqw"
  card-pad: "2cqw 1.6cqw"

components:
  pill:
    rounded: "9999px (small) / 2rem (cards)"
    border: "0.2cqw solid {colors.outline}"
    backgroundColor: "any candy or {colors.white}"
    description: "The universal container — every chip/button/label/stat tile/node/bar. No unstroked pill exists."
  pill-card:
    backgroundColor: "{colors.white}"
    border: "0.2cqw solid {colors.outline}"
    rounded: "2rem"
    shadow: "0.4cqw 0.4cqw 0 {colors.shadow}"
    typography: "{typography.card-headline} + {typography.body}"
    description: "Holds a circular card-icon, Bodoni headline, Space Grotesk body."
  stat-pill:
    backgroundColor: "{colors.white}"
    border: "0.2cqw solid {colors.outline}"
    rounded: "2rem"
    shadow: "0.3cqw 0.3cqw 0 {colors.shadow}"
    typography: "{typography.stat-number} (COLORED) + {typography.pill-text}"
    description: "The one place color touches a numeral; + a 40px accent bar."
  title-pill:
    backgroundColor: "{colors.yellow}"
    border: "0.2cqw solid {colors.outline}"
    rounded: "9999px"
    shadow: "0.3cqw 0.3cqw 0 {colors.shadow}"
    typography: "{typography.pill-text}"
    description: "Sits above the display headline on cover/closing."
  card-icon:
    backgroundColor: "any candy"
    border: "0.2cqw solid {colors.outline}"
    rounded: "50%"
    size: "60px"
    typography: "Bodoni numeral/letter in {colors.ink}"
    description: "Card mark."
  floating-pill:
    backgroundColor: "any candy"
    border: "0.2cqw solid {colors.outline}"
    rounded: "9999px / 50%"
    transform: "rotate(−20°..+25°)"
    shadow: "none"
    typography: "{typography.pill-text}"
    description: "Decorative wallpaper confetti, 5–8 per declarative frame. Flat — no shadow."
  quote-highlight:
    backgroundColor: "{colors.lime} / {colors.sky}"
    border: "0.2cqw solid {colors.outline}"
    rounded: "9999px"
    description: "Inline candy pill wrapping a phrase inside a Bodoni quote — the emphasis mechanism, replacing bold/italic."
  bar-track:
    backgroundColor: "{colors.cream}"
    border: "0.2cqw solid {colors.outline}"
    rounded: "9999px"
    fill: "child candy pill, value at right edge"
    description: "36px pill chart track."
  accent-line:
    backgroundColor: "{colors.coral}"
    rounded: "9999px"
    size: "60×4 (80×4 closing)"
    description: "Coral pill rule."
  atmosphere:
    background: "1–3 radial candy glows (6–15% opacity) over {colors.cream} + 4% grain overlay"
    description: "Baseline canvas layers on every frame. Never absent."
---

# Capsule — Frame (video / frame layer)

## Overview

Capsule at frame scale is a **playful editorial system where every container is a pill.** The
`border-radius: 9999px` (small) / `2rem` (cards) rule plus a 2px ink outline wraps every chip,
card, icon, bar, and node — inflated, friendly, graphically distinct. The canvas is sun-bleached
cream warmed by soft radial candy glows and a permanent 4% grain overlay.

The voice is a two-face conversation: **Bodoni Moda** (didone serif, weight 700–800, always ink,
always sentence case) carries every headline, stat, and quote; **Space Grotesk** carries body and
all uppercase tracked pill/label text. Nine candy accents fill pills interchangeably with no
semantic meaning. Depth is a **soft hard-offset shadow** (4/6/8/12px in 8% ink) — lifted, not
stamped — reserved for content-bearing containers; decorative floating pills are flat.

**Key characteristics at frame scale:**

- **Pill geometry everywhere** — 9999px small, 2rem cards — each wrapped in a 2px `{colors.outline}` stroke.
- **Bodoni Moda** display (ink, sentence case) + **Space Grotesk** body/pills (uppercase, tracked).
- **Nine candy accents**, interchangeable; color touches stat numerals + pill fills, never headlines.
- **Soft offset shadows** (4/6/8/12px, 8% ink) on content containers only; floating pills are flat.
- **Floating decorative-pill wallpaper** (5–8, tilted) + radial glows + 4% grain on declarative frames.
- **Cream canvas** warmed by atmosphere — bare corners read as broken.

## The Frame

### Frame Craft Bar

Three eyeball tests gate every frame before any structural check:

- **Squint** — one Bodoni headline or stat dominates at **3–6× its nearest neighbor**.
- **Silence** — declarative frames carry **atmosphere, not clutter** (pills as wallpaper, not content); the **pillar-cards and stat grid are the dense exception**.
- **Restraint** — every pill carries the 2px outline; color touches **fills + stat numerals only** (never a headline); soft shadow on content-bearing pills only (floating pills are flat); no tenth accent.
- **Reference** — aim at a **Memphis / ice-cream-parlor editorial spread**; failure looks like a **flat, sticker-less SaaS card grid**.

- **Primary:** 1920×1080 (16:9). Display authored in **`cqw`** (`px ÷ 1920 × 100 = cqw`).
- **Vertical:** 1080×1920 (9:16). **Square:** 1080×1080 (1:1).
- **Safe area:** `pad` (5cqw); floating pills may bleed off edges as wallpaper.

**The container law (load-bearing).** Every frame ground sets `container-type: size` AND carries
the radial-glow + grain atmosphere; ALL frame-relative units are `cqw`/`cqh` against it — never
`vw`. Pill radii stay `9999px`/`2rem` (shape, not scale); shadow offsets scale in `cqw`.

## Colors

Tokens identical to the source. `{colors.cream}` is the ground; `{colors.ink}`/`{colors.outline}`
is type + the universal 2px stroke; the nine candy accents fill pills with **no semantic mapping**
— pair a warm (coral/yellow/peach) with a cool (sky/lavender/violet/mint) with a neutral-bright
(lime); never two same-family adjacent. Color appears on **stat numerals and pill fills only** —
never on a Bodoni headline. Shadow is always `{colors.shadow}` (8% ink). No tenth color.

## Typography

Two ramps. The **reading ramp** (Space Grotesk body 0.85cqw, uppercase tracked pill/label text)
carries copy + chips; the **display ramp** (Bodoni `card-headline` 1.9cqw → `display` 12cqw, all
700–800) carries every headline, stat, and quote.

- **Legibility floor:** any load-bearing line ≥ **1.4cqw**; px labels are chrome only.
- **Fit-to-measure:** size the headline to its length. Cap the block at **≤ 78cqw**; ≤3 words → `display`/`closing-display`; 4–6 → `headline`; 7+ → `section-headline`.
- **Bodoni 700+ in ink, sentence case** (italic via `<em>` only, color allowed on the italic key word as a candy hue); **Space Grotesk pills/labels uppercase, 0.08em+ tracked**; negative-track Bodoni display.

## Depth & Surface

Soft hard-offset shadow is the only depth, in `{colors.shadow}` (8% ink), bottom-right:

- **0.2cqw (4px)** small nodes; **0.3cqw (6px)** stat-pills, orbit pills, diagram nodes; **0.4cqw (8px)** pillar-cards; **0.6cqw (12px)** the visual frame.
- The **2px outline** does most of the lift against cream; the shadow adds the float.
- **Decorative floating pills cast no shadow** — this separates content from atmosphere at a glance.

**Ceiling:** no blurred shadow, no re-colored shadow, no gradient depth.

## Shapes

- **9999px** — all small pills (chips, buttons, bars, nodes, floating pills, quote highlights, accent lines).
- **2rem** — larger cards (pillar-card, stat-pill, chart container, visual frame).
- **50%** — circular pills (card-icon 60px, step-node 56px, orbit-center 160px, nav dots).
- **0** — only the grain overlay and the gradient region inside a visual frame. No sharp-cornered text container exists.

## Components

- **pill** — the universal 2px-outlined container. **pill-card / stat-pill / title-pill** — the white/yellow content pills with soft shadows.
- **card-icon** — circular candy mark; **floating-pill** — flat tilted wallpaper confetti; **quote-highlight** — inline candy emphasis pill.
- **bar-track** — pill-shaped chart bar; **accent-line** — coral pill rule; **atmosphere** — the baseline glow + grain on every frame.

## Frame Treatments

> Recipe: ground · container · composes · focal · chrome · accent · silence · Fixed/Free · density.
> Atmosphere (glow + grain) on every frame; declarative frames carry floating-pill wallpaper.

### 1 · Cover (identity · move: title pill + display · centered)

**Ground** cream + atmosphere, floating-pill wallpaper. **Composes** title-pill, display, accent-line, floating-pills (5–8). **Focal** a 1–2 line Bodoni `display` headline in ink (italic key word in a candy hue), centered, under a yellow title-pill; a coral accent-line below. **Chrome** uppercase Space Grotesk sub. **Accent** the italic word + candy floating pills. **Silence** content centered; pills fill the edges. **Fixed** pill outlines, Bodoni ink, flat floating pills. **Free** title, which candy hues, pill words/positions. **Density** medium-atmospheric.

### 2 · Pillar Cards (catalog · move: 3-up grid · left — the dense frame)

**Ground** cream + atmosphere. **Composes** title-pill (lavender), section-headline, 3× pill-card. **Focal** three white 2rem pill-cards (circular candy card-icon, Bodoni card-headline, Space Grotesk body) with 0.4cqw shadows, under a Bodoni section-headline. **Chrome** a lavender header tag-pill. **Accent** the three card-icon fills (coral/sky/lime sequence). **Silence** tight — the density exception (no floating pills here). **Fixed** 2px outlines, soft shadows, ink headlines. **Free** card content, icon hues. **Density** dense-exception.

### 3 · Stat Grid (data · move: stat pills · centered head)

**Ground** cream + atmosphere. **Composes** section-headline, 3–4× stat-pill. **Focal** a row of white stat-pills, each a COLORED Bodoni stat-number + uppercase label + accent bar. **Accent** the colored numerals + bars (the one place color meets type). **Silence** moderate. **Fixed** 2rem pills, colored numerals only, soft shadow. **Free** figures (from script), hues. **Density** standard.

### 4 · Pull Quote (quote · move: highlight pill · left)

**Ground** cream + atmosphere, a few floating pills. **Composes** quote-display, quote-highlight, accent-line. **Focal** a Bodoni quote in ink with one phrase wrapped in a lime/sky `quote-highlight` pill (the emphasis mechanism — never bold). **Chrome** uppercase attribution. **Accent** the highlight pill. **Silence** ~50%. **Fixed** Bodoni 600, highlight-pill emphasis. **Free** quote, highlight color/phrase. **Density** sparse.

### 5 · Orbit (concept · move: gravitational pills · centered)

**Ground** cream + atmosphere. **Composes** orbit-center (160px lime circle, Bodoni ordinal), 4–6 orbit-pill satellites (candy, tilted, soft shadow). **Focal** the lime center anchored by orbiting candy pills. **Accent** the satellite hues. **Silence** moderate. **Fixed** circular center, outlined satellites with shadow. **Free** ordinal, satellite words/positions. **Density** medium.

### 6 · Closing Plate (closer · move: title pill + display · centered)

**Ground** cream + atmosphere, floating-pill wallpaper. **Composes** title-pill (yellow), closing-display, accent-line, floating-pills. **Focal** a Bodoni `closing-display` sign-off in ink (italic word in violet/candy), centered. **Accent** the italic word + pills. **Silence** content centered. **Fixed** Bodoni ink, flat pills. **Free** sign-off, pill words. **Density** medium-atmospheric.

## Composition Rules

### Do

- Make every text container a **pill** (9999px / 2rem) with the **2px ink outline**.
- Set **Bodoni headlines in ink, sentence case**; color lives on stat numerals + pill fills.
- Use **soft offset shadows** (4/6/8/12px, 8% ink) on content containers; keep floating pills flat.
- Float **5–8 candy pills** + radial glows + grain on declarative frames; bare corners read as broken.
- Wrap inline emphasis in a **candy quote-highlight pill**, never bold/italic-alone.
- Pair warm+cool+neutral-bright accents; lean centered on cover/closer, left on cards/quote.

### Don't

- No sharp-cornered text container; no unstroked pill.
- No colored Bodoni headline; no uppercase Bodoni.
- No blurred or re-colored shadow; no tenth accent color.
- No shadow on decorative floating pills.
- Don't blow a headline edge-to-edge — fit to measure.

## Aspect-Ratio Behavior

| Treatment    | 16:9                           | 9:16                        | 1:1                   |
| ------------ | ------------------------------ | --------------------------- | --------------------- |
| Cover        | display centered, pills around | display top, pills band     | centered, fewer pills |
| Pillar Cards | head + 3-up                    | head + 3 stacked            | head + 2+1            |
| Stat Grid    | 3–4 across                     | 2×2                         | 2×2                   |
| Pull Quote   | quote left                     | quote top, highlight inline | centered              |
| Orbit        | center + 4–6 satellites        | center + 3 satellites       | center + 4            |
| Closing      | centered + pills               | centered, pills band        | centered              |

`pad` holds on the short edge; re-step display above the 1.4cqw floor. Floating-pill count drops
on tighter ratios so they stay wallpaper, not clutter.

## Approved Entities

No real customers, logos, or vendors are defined in the source — render any such mark as a
placeholder. Floating-pill words are neutral atmospheres ("VISION", "FUTURE", "NEXT"), never content-specific.

## Numerals & Claims (hard rule)

Never invent figures, stats, or counts at frame scale. Render slots as `— figure —`, `{metric}`,
`N%`. Stat-pill numbers and bar-track widths carry placeholders until the script supplies values.

## Pre-Render Self-Audit

- **Squint** — one Bodoni element dominates at 3–5× its neighbor.
- **Silence** — declarative frames carry atmosphere not clutter; only pillar/stat grids run dense.
- **Pills** — every container is a pill with a 2px outline; no sharp text container.
- **Color** — candy on fills + stat numerals only; headlines ink; no tenth hue.
- **Depth** — soft offset shadow on content only; floating pills flat; no blur.
- **Type** — Bodoni ink sentence-case, fit-to-measure; pills uppercase tracked; ≥1.4cqw floor.
- **Anchor** — centered on cover/closer/orbit, left on cards/quote; no 3 consecutive alike.
- **Fabrication** — every numeral traces to the script, else placeholder.

## Known Gaps

- **Motion intentionally out of scope.** frame.md specifies composition only; the 0.6s fade in the source is a deck mechanic.
- **Bodoni Moda + Space Grotesk via Google Fonts.** CJK pairing (ZCOOL XiaoWei / Yozai) carries over from the source.
- **9:16 / 1:1 are guidance**; verify the floor and that floating-pill count scales down.
- The grain overlay, radial glows, floating pills, and bar fills are CSS-only; no external imagery is required.


<!-- ===== FILE: hyperframes/hyperframes-creative/frame-presets/cartesian/FRAME.md ===== -->

---
version: alpha
name: Cartesian — Frame (video / frame layer)
description: >
  Video-first companion to Cartesian's design.md. The unit is the frame (1920×1080). Atoms are
  identical and sacred — the five-tone warm-stone palette, Playfair Display 400 + Inter, the
  universal 1px taupe hairline as the only structural device, compass-drafted geometric rings,
  and zero shadow / zero fill. Composition, frame scale, and aspect-ratio behavior are rewritten
  for the frame. Restraint is the rule; motion is out of scope.
unit: the frame — 1920×1080 primary; 9:16 and 1:1 documented
principle: atoms are sacred · composition is free · numbers come from the script

colors:
  bg-primary: "#EDE8E0"
  bg-secondary: "#E2DBD1"
  text-primary: "#1A1A1A"
  text-secondary: "#5A5A5A"
  accent: "#8A8178"
  line: "#B8B0A4"
  white-overlay: "rgba(255,255,255,0.3)"

typography:
  # — reading ramp (Inter) —
  body:        { fontFamily: "Inter", cqw: 1.0,  weight: 400, lineHeight: 1.6, color: "text-secondary" }
  body-sm:     { fontFamily: "Inter", cqw: 0.85, weight: 400, lineHeight: 1.6 }
  subtitle:    { fontFamily: "Inter", cqw: 1.3,  weight: 400, lineHeight: 1.5 }
  label:       { fontFamily: "Inter", px: 14, weight: 500, tracking: "3px", upper: true, color: "accent" }
  attribution: { fontFamily: "Inter", px: 15, weight: 400, tracking: "2px", upper: true, color: "accent" }
  micro:       { fontFamily: "Inter", px: 12, weight: 400, tracking: "2px", upper: true, color: "accent" }
  # — display / hero ramp (Playfair Display 400, sentence case) —
  h3:          { fontFamily: "Playfair Display", cqw: 1.8, weight: 400, lineHeight: 1.1 }
  timeline-headline:{ fontFamily: "Playfair Display", cqw: 1.9, weight: 400, lineHeight: 1.1 }
  card-headline:{ fontFamily: "Playfair Display", cqw: 2.0, weight: 400, lineHeight: 1.15 }
  stat-figure: { fontFamily: "Playfair Display", cqw: 3.0, weight: 400, lineHeight: 1.0 }
  quote-mark:  { fontFamily: "Playfair Display", cqw: 9.0, weight: 400, lineHeight: 0.5, color: "line" }
  h2:          { fontFamily: "Playfair Display", cqw: 4.0, weight: 400, lineHeight: 1.1 }
  h1:          { fontFamily: "Playfair Display", cqw: 6.2, weight: 400, lineHeight: 1.06 }
  display:     { fontFamily: "Playfair Display", cqw: 8.0, weight: 400, lineHeight: 1.04 }

spacing:
  pad-x: "7cqw"
  pad-y: "5cqw"
  gap-xl: "6cqw"
  gap-lg: "5cqw"

components:
  hairline:
    rule: "0.07cqw solid {colors.line}"
    description: "The universal structural device — every separator (agenda rule, timeline connector, card border, stats top) is this 1px taupe line. No thick borders exist."
  card:
    backgroundColor: "{colors.white-overlay}"
    border: "0.07cqw solid {colors.line}"
    rounded: "0"
    shadow: "none"
    description: "Faint white-overlay fill (canvas bleeds through) is what makes a card distinct from a bare region."
  card-icon:
    border: "0.07cqw solid {colors.line}"
    rounded: "50%"
    size: "40px circle"
    textColor: "{colors.accent}"
    typography: "Playfair numeral/letter"
    description: "Ringed circle mark."
  agenda-row:
    borderBottom: "0.07cqw solid {colors.line}"
    typography: "{typography.h3} (numeral {colors.accent}, label {colors.text-primary})"
    description: "Numeral left, label right over a taupe rule."
  timeline:
    borderTop: "0.07cqw solid {colors.line}"
    typography: "{typography.timeline-headline} + {typography.body-sm}"
    description: "A single taupe top rule across items — no nodes, no dots."
  stats-cluster:
    borderTop: "0.07cqw solid {colors.line}"
    typography: "{typography.stat-figure} + uppercase {colors.accent} labels"
    description: "Inline modest stat figures (no hero numeral)."
  geo-ring:
    border: "1px solid {colors.line} (inner dashed ::before ~70–80%)"
    rounded: "50%"
    size: "10–50cqw"
    opacity: "0.2–0.5"
    description: "Compass-construction rings behind content. 1–2 per frame, never more."
  horizontal-accent:
    backgroundColor: "{colors.text-primary}"
    size: "~18cqw × 1px"
    description: "The system's only INK-BLACK rule — a strong terminal accent on cover/closing, sparingly."
  vertical-line:
    backgroundColor: "{colors.line}"
    size: "1px × full height, ~5cqw from edge"
    opacity: "0.3–0.4"
    description: "Drafting-paper alignment guide. Optional."
  image-placeholder:
    backgroundColor: "{colors.bg-secondary}"
    mark: "crossed +30°/−30° 1px taupe diagonals (an X)"
    typography: "small uppercase {typography.micro}"
    description: "The signature image-not-wired mark."
  team-photo:
    backgroundColor: "{colors.bg-secondary}"
    border: "0.07cqw solid {colors.line}"
    rounded: "50%"
    typography: "Playfair initial in {colors.accent}"
    description: "Circular portrait frame."
---

# Cartesian — Frame (video / frame layer)

## Overview

Cartesian at frame scale is a **quiet museum-catalog editorial system** — restraint through 1px
lines. Every structural separator is a single 1px taupe hairline; there are no thick borders, no
fills (save the faint white-overlay card), no shadows, no rounded rectangles. Hierarchy comes from
**type contrast and negative space**, and atmosphere from **compass-drafted geometric rings**
drifting behind content.

The voice is a literary pairing: **Playfair Display** at weight 400 (the thin-stroke didone, never
bold, always sentence case) carries every headline, numeral, and quote mark in ink; **Inter**
carries body in warm gray and labels in uppercase taupe with 2–3px tracking. The palette is five
warm stones plus ink — no populist accent color exists. The correct density is **sparse and
breathing**: one clear idea, well-framed, on stone paper.

**Key characteristics at frame scale:**

- **1px taupe hairline** as the universal structural device — every separator is this one line.
- **Playfair Display 400** (ink, sentence case) for display; **Inter** body (gray) + labels (taupe, tracked).
- **Five warm stones + ink** — no red/blue/green; the only "color" is type contrast.
- **Compass-drafted geometric rings** (solid + dashed, 20–50% opacity) behind content for mood.
- **Flat** — zero shadow, zero rounded rectangle (circles only); the lone ink line is the `horizontal-accent`.
- **Sparse and breathing** — generous negative space; crowding reads as broken.

## The Frame

### Frame Craft Bar

Three eyeball tests gate every frame before any structural check:

- **Squint** — one Playfair element dominates at **3–6× its nearest neighbor**; the serif/sans + size contrast carries hierarchy, not weight.
- **Silence** — declarative frames read **55–60% empty**; Cartesian has **no dense frame** — even the agenda/index breathes (the system breaks when crowded).
- **Restraint** — **at most two geo rings** per frame; the single INK-BLACK `horizontal-accent` rule used sparingly; no populist accent color ever.
- **Reference** — aim at a **Vignelli editorial / Cooper Hewitt catalogue / pencil-and-tracing-paper plan**; failure looks like a **shadowed, rounded-card SaaS deck**.

- **Primary:** 1920×1080 (16:9). Display authored in **`cqw`** (`px ÷ 1920 × 100 = cqw`).
- **Vertical:** 1080×1920 (9:16). **Square:** 1080×1080 (1:1).
- **Safe area:** `pad-x` (7cqw) generous gutters; geometry may bleed off an edge.

**The container law (load-bearing).** Every frame ground sets `container-type: size`; ALL
frame-relative units are `cqw`/`cqh` against it — never `vw`. The 1px hairlines and geo rings hold
their proportion against the frame at any render size.

## Colors

Tokens identical to the source. `{colors.bg-primary}` is the ground; `{colors.text-primary}` ink is
headlines and the one black accent rule; `{colors.text-secondary}` gray is body; `{colors.accent}`
taupe is labels, numerals, small text; `{colors.line}` taupe is every 1px structural border.
`{colors.bg-secondary}` is the only secondary fill (placeholders, photo frames). **No populist
accent** — when emphasis is needed, grow the type, switch sans→serif, or add a single
`horizontal-accent` ink line. Headlines are never taupe; small text is never ink.

## Typography

Two ramps. The **reading ramp** (Inter body 1.0cqw gray, labels in px taupe) carries copy + chrome;
the **display ramp** (Playfair `h3` 1.8cqw → `display` 8.0cqw, all weight 400) carries every headline.

- **Legibility floor:** any load-bearing line ≥ **1.4cqw**; px labels are chrome only.
- **Fit-to-measure:** size the headline to its length. Cap the block at **≤ 78cqw**; ≤3 words → `display`/`h1`; 4–6 → `h2`; 7+ → `h3`. Cartesian has no hero-stat numeral — stats stay modest (`stat-figure` 3cqw).
- **Playfair at 400, ink, sentence case** — never bold, never uppercase, never taupe. **Inter labels uppercase, 2–3px tracked, taupe.** Italic via Playfair italic for emphasis only.

## Depth & Surface

The flat plane is the only technique. Hierarchy from:

- **Type contrast** — Playfair serif vs Inter sans; the 8cqw→0.7cqw scale.
- **1px taupe hairlines** — every divider, card outline, timeline rule, photo ring.
- **Tone** — ink vs gray vs taupe.
- **Negative space** — generous padding.
- **Geometric atmosphere** — compass rings that suggest depth without creating it.

**Ceiling:** no box-shadow, no elevated card, no gradient, no rounded rectangle. The single ink line
(`horizontal-accent`) is the only non-taupe rule.

## Shapes

- **50% (circle)** — card-icon, team-photo, nav-dot, every geo ring.
- **0** — everything else; soft-rounded corners do not exist.

## Components

- **hairline** — the universal 1px taupe separator (the identity).
- **card** (1px taupe + white-overlay) / **card-icon** (ringed circle) / **agenda-row** / **timeline** (line, no nodes) / **stats-cluster** — all built on the hairline.
- **geo-ring** — compass decoration (solid + dashed), 1–2 per frame. **horizontal-accent** — the one ink line, sparingly. **vertical-line** — drafting guide.
- **image-placeholder** (crossed-X) / **team-photo** (ringed initial) — the stone-fill placeholders.

## Frame Treatments

> Recipe: ground · container · composes · focal · chrome · accent · silence · Fixed/Free · density.
> Every frame is sparse and breathing; 1–2 geo decorations max.

### 1 · Cover (identity · move: serif + compass ring · left)

**Ground** `{colors.bg-primary}`, `pad-x`. **Composes** geo-ring (right, ~34cqw, solid+dashed), vertical-line (left), label, display/h1. **Focal** a 2–3 line Playfair `display`/`h1` headline in ink (italic on the key word), left-anchored, with a taupe `label` above and an Inter subtitle below. **Chrome** optional bottom meta row (Playfair value + taupe label). **Accent** the geo ring; optionally one `horizontal-accent` ink line (if it clears the meta). **Silence** ~55% empty. **Fixed** Playfair 400 ink sentence-case, ≤2 geo elements, 1px lines. **Free** title, ring placement, meta. **Density** sparse.

### 2 · Agenda / Index (index · move: hairline list · left)

**Ground** `{colors.bg-primary}`, `pad-x`. **Composes** label, h2, agenda-rows. **Focal** a Playfair `h2` over 4–6 agenda rows (Playfair numeral in taupe + Playfair label in ink), each on a 1px taupe rule. **Chrome** taupe `label` eyebrow. **Accent** none — taupe numerals carry it. **Silence** moderate; rows generously spaced. **Fixed** 1px taupe rules, Playfair 400. **Free** items, count. **Density** standard (sparse rows).

### 3 · Pull Quote (quote · move: centered statement · compass ring)

**Ground** `{colors.bg-primary}`, centered. **Composes** geo-ring (centered dashed, ~26cqw), quote-mark, h2/display-quote, attribution. **Focal** a 2-line Playfair quote in ink, centered, under a 50%-taupe Playfair quote-mark; a taupe uppercase attribution beneath. **Accent** the faint centered ring. **Silence** ~60% — deliberately open. **Fixed** Playfair 400, one ring, centered. **Free** quote, attribution. **Density** sparse.

### 4 · Closing Plate (closer · move: centered ring · centered)

**Ground** `{colors.bg-primary}`, centered. **Composes** geo-ring (centered, ~40cqw, solid+dashed), label, h1/display, horizontal-accent. **Focal** a 1–2 line Playfair sign-off in ink (italic key word), centered inside the largest compass ring; a short ink `horizontal-accent` beneath. **Accent** the ring + the one ink line. **Silence** ~60%. **Fixed** Playfair 400, centered, ≤2 geo. **Free** sign-off, ring scale. **Density** sparse.

### 5 · Two-Column Editorial (content · move: asymmetric split · left)

**Ground** `{colors.bg-primary}`, `pad-x`, two columns with `gap-xl`. **Composes** label, h2, body, image-placeholder (crossed-X) or card. **Focal** a Playfair `h2` + Inter body in the text column; an image-placeholder or card in the other. **Accent** none. **Silence** generous gutter. **Fixed** 1px taupe card/placeholder borders, white-overlay fill. **Free** which side is text, body copy. **Density** standard.

### 6 · Stats / Timeline (data · move: hairline rail · left)

**Ground** `{colors.bg-primary}`, `pad-x`. **Composes** label, h3, stats-cluster or timeline. **Focal** a modest Playfair stat row (or a 1px-rule timeline with year + headline + body, no nodes), framed by a 1px taupe top rule. **Accent** none. **Silence** moderate. **Fixed** modest stat scale, hairline rule, no nodes. **Free** figures, phases. **Density** standard.

## Composition Rules

### Do

- Use a **single 1px taupe line** for every separator — the hairline is the identity.
- Set every **Playfair headline at 400, ink, sentence case**; render labels taupe, uppercase, 2–3px tracked.
- Layer **one or two compass rings** (solid + dashed, 20–50% opacity) behind content for atmosphere.
- Let frames **breathe** — sparse, generous negative space; 55–60% empty on declarative frames.
- Lean centered on quote/closer; asymmetric/left on cover/agenda/editorial. Use `bg-secondary` for placeholder fills.

### Don't

- Don't introduce a populist accent color — stone and ink only.
- Don't bold Playfair, render headlines in taupe, or use thick (2px+) borders.
- Don't add shadows, elevated cards, or rounded rectangles (circles only).
- Don't crowd the frame — packed layouts read as broken.
- Never more than two geo decorations per frame; don't blow a headline edge-to-edge.

## Aspect-Ratio Behavior

| Treatment            | 16:9                       | 9:16                                | 1:1                         |
| -------------------- | -------------------------- | ----------------------------------- | --------------------------- |
| Cover                | headline left, ring right  | headline top, ring below            | headline upper, ring behind |
| Agenda / Index       | h2 + rows                  | h2 + rows (tighter)                 | h2 + rows                   |
| Pull Quote           | centered, ring behind      | centered, taller                    | centered                    |
| Closing Plate        | centered in ring           | centered, ring scaled               | centered                    |
| Two-Column Editorial | text + visual side-by-side | stacked (collapse)                  | stacked                     |
| Stats / Timeline     | horizontal rail            | vertical stack (drop timeline rule) | compact                     |

Generous `pad-x` holds on the short edge; re-step display per ratio above the 1.4cqw floor. On
9:16, the timeline rule loses meaning when stacked — switch to a vertical list (per source).

## Approved Entities

No real customers, logos, or vendors are defined in the source — render any such mark as a
placeholder (the crossed-X image-placeholder, or a ringed initial for portraits).

## Numerals & Claims (hard rule)

Never invent figures, dates, or counts at frame scale. Render slots as `— figure —`, `{metric}`.
Stats and timeline years carry placeholders until the script supplies them. Agenda ordinals
(01, 02…) are decorative and may be sequential.

## Pre-Render Self-Audit

- **Squint** — one Playfair element dominates; the serif/sans contrast carries hierarchy.
- **Silence** — declarative frames 55–60% empty; nothing is crowded.
- **Palette** — five stones + ink only; no populist accent; headlines ink, labels taupe.
- **Lines** — every separator is a 1px taupe hairline; the only ink line is `horizontal-accent`.
- **Type** — Playfair 400 sentence-case, fit-to-measure; labels uppercase 2–3px; ≥1.4cqw floor.
- **Depth** — 0 shadow, 0 rounded rectangle; ≤2 geo rings per frame.
- **Anchor** — centered on quote/closer, left/asymmetric on cover/agenda/editorial; no 3 in a row alike.
- **Fabrication** — every numeral traces to the script, else placeholder.

## Known Gaps

- **Motion intentionally out of scope.** frame.md specifies composition only; the 0.6s fade in the source is a deck mechanic.
- **Playfair Display + Inter via Google Fonts.** CJK pairing (Noto Serif SC 700/400) carries over; Playfair has no Hanzi italic — substitute weight/taupe for emphasis.
- **9:16 / 1:1 are guidance**; verify the legibility floor and that the timeline collapses to a vertical list.
- Geo rings, the crossed-X placeholder, and the dashed inner ring are CSS-only; no external imagery is required.


<!-- ===== FILE: hyperframes/hyperframes-creative/frame-presets/cobalt-grid/FRAME.md ===== -->

---
version: alpha
name: Cobalt Grid — Frame (video / frame layer)
description: >
  Video-first companion to Cobalt Grid's design.md. The unit is the frame (1920×1080). Atoms
  are identical and sacred — warm cream paper, electric cobalt ink (the only ink), the permanent
  graph-paper grid, Newsreader serif 400 + Hanken Grotesk + DM Mono, the top/bottom cobalt
  hairlines, and the pixel-glitch + QR-block signatures. Composition, frame scale, and
  aspect-ratio behavior are rewritten for the frame. Motion is out of scope.
unit: the frame — 1920×1080 primary; 9:16 and 1:1 documented
principle: atoms are sacred · composition is free · numbers come from the script

colors:
  paper: "#F0EBDE"
  paper-2: "#E6E0CE"
  ink: "#1F2BE0"
  ink-soft: "#5560E5"
  grid: "rgba(31,43,224,0.10)"
  ink-faint: "rgba(31,43,224,0.18)"

typography:
  # — reading ramp —
  body:        { fontFamily: "Hanken Grotesk", cqw: 0.83, weight: 400, lineHeight: 1.5 }
  body-lede:   { fontFamily: "Hanken Grotesk", cqw: 0.95, weight: 400, lineHeight: 1.5 }
  micro:       { fontFamily: "Hanken Grotesk", px: 13, weight: 600, tracking: "0.16em", upper: true }
  micro-strong:{ fontFamily: "Hanken Grotesk", px: 16, weight: 600, tracking: "0.18em", upper: true }
  mono-tag:    { fontFamily: "DM Mono", cqw: 0.78, weight: 400, tracking: "0.05em" }
  mono-chrome: { fontFamily: "DM Mono", px: 13, weight: 400, tracking: "0.06em" }
  # — display / hero ramp (Newsreader 400, negative tracking) —
  table-name:  { fontFamily: "Newsreader", cqw: 1.5, weight: 400, lineHeight: 1.15 }
  row-headline:{ fontFamily: "Newsreader", cqw: 2.1, weight: 400, lineHeight: 1.05 }
  ed-callout:  { fontFamily: "Newsreader", cqw: 2.6, weight: 400, lineHeight: 1.1, italic: true }
  headline:    { fontFamily: "Newsreader", cqw: 4.6, weight: 400, lineHeight: 0.95 }
  headline-index:{ fontFamily: "Newsreader", cqw: 5.0, weight: 400, lineHeight: 0.95 }
  display-quote:{ fontFamily: "Newsreader", cqw: 5.7, weight: 400, lineHeight: 1.05, tracking: "-0.005em" }
  display-chapter:{ fontFamily: "Newsreader", cqw: 6.8, weight: 400, lineHeight: 1.0, tracking: "-0.005em" }
  display-closing:{ fontFamily: "Newsreader", cqw: 9.4, weight: 400, lineHeight: 0.96, tracking: "-0.005em" }
  display-hero:{ fontFamily: "Newsreader", cqw: 10.4, weight: 400, lineHeight: 0.9, tracking: "-0.008em" }
  vbig-numeral:{ fontFamily: "Newsreader", cqw: 12.5, weight: 400, lineHeight: 0.9, tracking: "-0.015em" }

spacing:
  edge: "4cqw"          # standard frame edge inset (~80px@1920)
  pad-top: "7cqw"
  pad-bottom: "6cqw"
  gap-md: "2cqw"

components:
  graph-grid:
    backgroundImage: "linear-gradient grid, ~2cqw cells, 10% {colors.ink} ({colors.grid})"
    placement: "behind EVERY frame on the ground"
    description: "Permanent graph-paper grid — never disabled; the canvas tone."
  hairlines:
    rule: "0.12cqw solid {colors.ink}"
    placement: "≈3cqw from top + bottom, inset {spacing.edge}"
    description: "Two persistent cobalt rules framing every composition."
  page-chrome:
    typography: "{typography.pagenum}"
    color: "{colors.ink}"
    placement: "page number bottom-right, nav/meta hint bottom-left, above the bottom hairline"
    description: "The only persistent chrome."
  pixel-glitch:
    backgroundColor: "{colors.paper}"
    fill: "repeating-linear-gradient(90deg, {colors.ink} 0 2px, transparent 2px 8px)"
    size: "14–30cqw wide, full height, stair-stepped"
    placement: "right on cover/data, left on chapter/colophon; z above grid, below headline"
    description: "Stair-stepped scanline column. Decorative."
  qr-block:
    backgroundColor: "{colors.paper}"
    cells: "8×8, {colors.ink} on / {colors.grid} off"
    size: "3–9cqw square"
    shadow: "0 0 0 0.12cqw {colors.paper} (anti-shadow for readability, not elevation)"
    description: "QR mosaic patch — corner punctuation."
  topbar-rule:
    typography: "{typography.headline-index} + {typography.mono-tag}"
    borderBottom: "0.12cqw solid {colors.ink}"
    description: "Section header on index/data/table frames."
  ledger-row:
    layout: "grid: mono num · Newsreader name · Hanken desc · mono delta"
    borderBottom: "0.06cqw solid {colors.ink-faint} (header 0.12cqw solid {colors.ink})"
    typography: "{typography.mono-tag} + {typography.table-name} + {typography.body}"
    description: "Dense matrix row with ↑/↓/— delta."
  pixel-stack-bar:
    cells: "column-reverse, {colors.grid} off / {colors.ink} on"
    baseline: "0.12cqw solid {colors.ink} + {typography.mono-tick} ticks"
    description: "Data as grid-unit cells; echoes the glitch."
  vstack-label:
    typography: "{typography.mono-tick}"
    transform: "writing-mode: vertical-rl"
    description: "Catalogue chrome along a frame edge."
---

# Cobalt Grid — Frame (video / frame layer)

## Overview

Cobalt Grid at frame scale is a **two-color risograph trend-report** — warm cream paper, electric
cobalt ink, and a **permanent graph-paper grid** behind every frame. Cobalt is the _only_ ink:
headlines, body, rules, the grid, the pixel-glitch decoration, the QR patches. There is no accent
color and no second surface.

The voice is a three-face conversation: **Newsreader** serif at weight 400 (size, not weight,
makes hierarchy) carries every display and headline; **Hanken Grotesk** carries body and
uppercase tracked labels; **DM Mono** carries all chrome — page numbers, tags, ticks, vertical
stacks. Every frame is framed by top + bottom cobalt hairlines; declarative frames carry the
**pixel-glitch column** and a **QR-block** patch.

**Key characteristics at frame scale:**

- **Strictly two-color** — cream paper + cobalt ink; no accent, no second surface.
- **Permanent ~2cqw graph-paper grid** (10% cobalt) behind every frame; cannot be disabled.
- **Top + bottom 1.5px cobalt hairlines** frame every composition, inset by `edge`.
- **Newsreader 400** for all display (negative tracking); **Hanken 600** uppercase 0.16em labels; **DM Mono** chrome.
- **Pixel-glitch column + QR-block** as the signature decorative patches on declarative frames.
- **Pixel-stack bars** render data as grid-unit cells (cobalt on / 10% off).

## The Frame

### Frame Craft Bar

Three eyeball tests gate every frame before any structural check:

- **Squint** — one Newsreader element dominates at **3–6× its nearest neighbor** (`display-hero`/`vbig-numeral`); hierarchy is size, never weight.
- **Silence** — declarative frames (cover, chapter, quote, colophon) read **45–60% empty** with the grid showing; the **index ledger and data frame are the one dense exception** (density via quiet repetition, not richness).
- **Restraint** — **two-color only** (cream + cobalt, never a second hue); one pixel-glitch column and at most one QR-block per declarative frame.
- **Reference** — aim at a **WIRED Japan / Shift two-color risograph monograph**; failure looks like a **colorful dashboard with a second accent hue**.

- **Primary:** 1920×1080 (16:9). Display authored in **`cqw`** (`px ÷ 1920 × 100 = cqw`).
- **Vertical:** 1080×1920 (9:16). **Square:** 1080×1080 (1:1).
- **Safe area:** `edge` (4cqw) inset; hairlines + page chrome live on the safe line.

**The container law (load-bearing).** Every frame ground sets `container-type: size` AND carries
the graph-paper `background-image`; ALL frame-relative units are `cqw`/`cqh` against it — never
`vw`. The grid `background-size` is `~2cqw 2cqw` so cell density holds at any render size.

## Colors

Tokens identical to the source. `{colors.paper}` is the ground; `{colors.ink}` cobalt is the only
ink (type, rules, grid lines, glitch, QR). `{colors.ink-soft}` is a secondary cobalt for editorial
subtitles only; `{colors.grid}` (10%) is the permanent grid + chart "off" cells; `{colors.ink-faint}`
(18%) is faint row dividers. **Never a second hue** — emphasis comes from size, from switching
Hanken→Newsreader, from a mono delta arrow, or from opacity, never from color.

## Typography

Two ramps. The **reading ramp** (Hanken body 0.83cqw, mono chrome in px) carries copy + labels;
the **display/hero ramp** (Newsreader `headline` 4.6cqw → `vbig-numeral` 12.5cqw) carries every
statement and figure.

- **Legibility floor:** any load-bearing line ≥ **1.4cqw**; mono chrome (px) is colophon only.
- **Fit-to-measure:** size the headline to its line length. Cap the block at **≤ 78cqw**; ≤3 words → `display-hero`/`vbig-numeral`; 4–6 → `display-chapter`; 7+ → `headline`.
- **Newsreader at 400 only**, in cobalt, with negative tracking (hero −0.008em, numeral −0.015em). **Hanken labels uppercase, 0.16–0.18em.** **DM Mono 0.04–0.08em.** No bold serif.

## Depth & Surface

Flat. Depth is structural only:

- **1.5px cobalt rules** — slide hairlines, topbar rule, chart baseline.
- **1px ink-faint dividers** — dense list / ledger rows.
- **The graph-paper grid** — measured-plane tone behind everything.
- **Pixel-glitch + QR** — texture and graphic punctuation, no z-axis.

**Ceiling:** no drop shadow (the QR's 1.5px paper outset is an anti-shadow for readability, not elevation), no gradient, no rounded corner, no second color.

## Shapes

- **0 radius everywhere** — frames, ledger rows, QR cells, glitch blocks, charts. Zero circular elements; this squareness is part of the identity.

## Components

- **graph-grid / hairlines / page-chrome** — the permanent frame furniture, inherited by every composition.
- **pixel-glitch** (edge column) + **qr-block** (corner patch) — the signature decoration on declarative frames.
- **topbar-rule** — the index/data/table section header. **ledger-row** — dense matrix row with delta arrows.
- **pixel-stack-bar** — data as grid-unit cells. **vstack-label** — vertical mono catalogue chrome.

## Frame Treatments

> Recipe: ground · container · composes · focal · chrome · accent · silence · Fixed/Free · density.
> The grid + hairlines are present on every frame. Choose density by type: declarative = sparse, index/data = dense.

### 1 · Hero Cover (identity · move: serif + glitch · left)

**Ground** paper + grid, hairlines. **Composes** pixel-glitch (right, ~26cqw), qr-block (top-right), display-hero, ed-callout. **Focal** a 1–2 line `display-hero` Newsreader headline in cobalt, left-anchored, with an italic `ed-callout` subtitle in `{colors.ink-soft}`. **Chrome** Hanken kicker; mono meta top + page number. **Accent** none (cobalt is the only ink). **Silence** ~45% paper. **Fixed** Newsreader 400, glitch + QR present, grid + hairlines. **Free** title, glitch step pattern, QR placement. **Density** sparse.

### 2 · Index Ledger (catalog · move: dense matrix · left — the dense frame)

**Ground** paper + grid, hairlines, `pad-top`/`pad-bottom`. **Composes** topbar-rule, ledger-rows. **Focal** a topbar (`headline-index` + mono lab-tag, 1.5px rule) over 4–6 ledger rows (mono num · Newsreader name · Hanken desc), ink-faint dividers. **Chrome** page number. **Accent** mono delta arrows. **Silence** tight — the density exception (the grid wants filling). **Fixed** 1.5px topbar rule, 1px ink-faint dividers, Newsreader names. **Free** rows, lab-tag, deltas. **Density** dense-exception.

### 3 · Chapter Opener (section · move: scale · sparse · left)

**Ground** paper + grid, hairlines. **Composes** pixel-glitch (left, ~14cqw, low opacity), mono index, display-chapter, body-lede. **Focal** a `display-chapter` Newsreader title, with a small mono `CHAPTER NN` index above and an optional Hanken lede ≤42cqw. **Accent** none. **Silence** ~60% — let the grid breathe. **Fixed** Newsreader 400, glitch low-opacity, grid showing. **Free** title, lede, glitch side. **Density** sparse.

### 4 · Data Frame (chart · move: pixel-stack · left)

**Ground** paper + grid, hairlines, `pad-top`. **Composes** topbar-rule, pixel-stack-bar row. **Focal** a row of 6–8 pixel-stack bars (cobalt on / 10% off) over a 1.5px cobalt baseline with mono ticks. **Chrome** topbar headline + mono fig-tag; page number. **Accent** none — data is cobalt cells. **Silence** moderate. **Fixed** grid-unit cells, cobalt baseline, mono ticks. **Free** bar values (from script), tick labels. **Density** standard/dense.

### 5 · Manifesto / Quote (quote · move: centered statement · sparse)

**Ground** paper + grid, hairlines. **Composes** display-quote (or display-manifesto), attribution rule, optional compact glitch. **Focal** a 2–3 line Newsreader pull in cobalt, with a Hanken kicker above and a 1px cobalt attribution rule + mono byline beneath. **Accent** none. **Silence** ~55% — deliberately open. **Fixed** Newsreader 400, attribution rule, grid showing. **Free** quote, byline. **Density** sparse.

### 6 · Colophon (closer · move: right-aligned close · sparse)

**Ground** paper + grid, hairlines. **Composes** pixel-glitch (left edge, mirroring the cover), display-closing, mono credit columns. **Focal** a right-aligned `display-closing` Newsreader title with a Hanken kicker above. **Chrome** 3–4 column mono credit grid at the foot; page number. **Accent** none. **Silence** ~50%. **Fixed** glitch on left, Newsreader 400. **Free** closing line, credits. **Density** sparse.

## Composition Rules

### Do

- Keep the **graph-paper grid + top/bottom hairlines** on every frame — they are the system.
- Set **Newsreader at 400 in cobalt**; make hierarchy with size, not weight; negative-track display.
- Track **Hanken labels uppercase 0.16em**; **DM Mono chrome 0.04–0.08em**.
- Render data as **pixel-stack cells** (cobalt on / 10% off); echo the glitch language.
- Use the **pixel-glitch column + QR patch** on declarative frames (cover, chapter, quote, colophon).
- Lean: declarative frames sparse and breathing; index/data dense. Vary anchor (left for index/chapter, centered for quote/closer).

### Don't

- Don't introduce a second ink color — cream + cobalt only.
- Don't bold Newsreader, round any corner, or add a drop shadow (QR outset is an anti-shadow only).
- Don't disable the grid or suppress the hairlines.
- Don't crowd chapter / quote / colophon — those let the grid show.
- Don't blow a serif headline edge-to-edge — fit to measure.

## Aspect-Ratio Behavior

| Treatment         | 16:9                        | 9:16                                 | 1:1                          |
| ----------------- | --------------------------- | ------------------------------------ | ---------------------------- |
| Hero Cover        | headline left, glitch right | headline top, glitch full-width band | headline upper, glitch lower |
| Index Ledger      | topbar + rows               | topbar + fewer rows                  | 2-col compresses to 1        |
| Chapter Opener    | title left, glitch left     | title top, glitch side               | centered title               |
| Data Frame        | 6–8 bars                    | 4–5 bars taller                      | square chart                 |
| Manifesto / Quote | centered pull               | centered, taller                     | centered                     |
| Colophon          | right-aligned, glitch left  | stacked, glitch top                  | centered close               |

Grid + hairlines hold on the short edge for every ratio; re-step display so no load-bearing line
drops below 1.4cqw. Mono chrome stays Latin/digit-only.

## Approved Entities

No real customers, logos, or vendors are defined in the source — render any such mark as a
placeholder. Trend names, signals, and figures are content; the system supplies the grid and chrome.

## Numerals & Claims (hard rule)

Never invent figures, deltas, dates, or signal counts at frame scale. Render slots as `— figure —`,
`{metric}`, `↑ —`. Pixel-stack bar heights and ledger deltas especially carry placeholders until the
script supplies values. Mono catalogue ordinals (001, 002…) are decorative and may be sequential.

## Pre-Render Self-Audit

- **Squint** — one Newsreader element dominates at 3–5× its neighbor.
- **Silence** — declarative frames 45–60% empty; only index/data run dense.
- **Two-color** — cream + cobalt only; no second hue anywhere.
- **Furniture** — grid present, top/bottom hairlines present, page chrome above the hairline.
- **Type** — Newsreader 400 negative-tracked, fit-to-measure; Hanken labels 0.16em; ≥1.4cqw floor.
- **Depth** — 0 shadow (QR outset excepted), 0 rounded corner.
- **Anchor** — left on index/chapter/cover, centered on quote/closer; no 3 consecutive frames share an anchor.
- **Fabrication** — every numeral/delta traces to the script, else placeholder.

## Known Gaps

- **Motion intentionally out of scope.** frame.md specifies composition only; the 280ms cross-fade in the source is a deck mechanic.
- **Pixel-glitch is rendered in CSS here** (stacked scanline blocks) rather than the source's inline SVG, to keep the showcase SVG-free; fidelity is preserved.
- **Three Google Fonts** (Newsreader, Hanken Grotesk, DM Mono); CJK pairing (Noto Serif SC 700/400) carries over from the source.
- **9:16 / 1:1 are guidance**; verify the legibility floor and grid density per ratio.
- The QR mosaic and glitch step patterns are hand-authored; there is no generative layer.


<!-- ===== FILE: hyperframes/hyperframes-creative/frame-presets/code-editorial/FRAME.md ===== -->

---
version: alpha
name: Code editorial — Frame (video / frame layer)
description: >
  Video-first companion to Code editorial's design.md. The unit is the frame (1920×1080). Atoms are
  identical and sacred — warm cream paper (never pure white, never cool), a single terracotta coral
  as scarce "voltage", hairline ink elevation (no heavy shadow), EB Garamond for all
  display + Inter body + JetBrains Mono for the index/code voice on a warm-navy code surface,
  sentence-case display, and the ✱ coral spike mark. Composition + frame scale rewritten. Motion out
  of scope.
unit: the frame — 1920×1080 primary; 9:16 and 1:1 documented
principle: atoms are sacred · composition is free · numbers come from the script

colors:
  ink: "#141413"
  cream: "#FAF9F5"
  tile: "#EFE9DE"
  tile-strong: "#ECE3D4"
  coral: "#CC785C"
  navy: "#181715"
  navy-soft: "#1F1E1B"
  navy-elev: "#252320"

borders: { hairline: "1px solid ink@12%", hairline-strong: "1px solid ink@20%", dark: "1px solid cream@14% (on navy)" }
shadows: { card: "0 1px 3px ink@8%, 0 4px 16px ink@4%", none: "none" }

typography:
  # — reading + chrome ramp —
  body:    { fontFamily: "Inter", cqw: 1.5, weight: 400, lineHeight: 1.5 }
  lead:    { fontFamily: "Inter", cqw: 2.08, weight: 400, lineHeight: 1.5 }
  card-title:{ fontFamily: "Inter", cqw: 2.3, weight: 500, lineHeight: 1.25, tracking: "-0.005em" }
  button:  { fontFamily: "Inter", cqw: 1.46, weight: 500, lineHeight: 1.0 }
  tag-upper:{ fontFamily: "Inter", cqw: 1.35, weight: 500, tracking: "0.18em", upper: true }
  kicker:  { fontFamily: "JetBrains Mono", px: 28, cqw: 1.46, weight: 500, tracking: "0.16em", upper: true }
  mono-label:{ fontFamily: "JetBrains Mono", px: 26, cqw: 1.35, weight: 500, tracking: "0.02em" }
  code:    { fontFamily: "JetBrains Mono", cqw: 1.67, weight: 400, lineHeight: 1.6 }
  # — display ramp (EB Garamond 400, sentence case, negative tracking. Renderer embeds only 400/700 — author at 400; italic is the synthesized slant) —
  headline:{ fontFamily: "EB Garamond", cqw: 4.6, weight: 400, lineHeight: 1.06, tracking: "-0.018em" }
  quote-pull:{ fontFamily: "EB Garamond", cqw: 5.0, weight: 400, lineHeight: 1.12, tracking: "-0.012em", italic: true }
  display-italic:{ fontFamily: "EB Garamond", cqw: 6.7, weight: 400, lineHeight: 1.05, tracking: "-0.012em", italic: true }
  display:{ fontFamily: "EB Garamond", cqw: 7.3, weight: 400, lineHeight: 1.02, tracking: "-0.022em" }
  number-hero:{ fontFamily: "EB Garamond", cqw: 9.4, weight: 400, lineHeight: 0.95, tracking: "-0.025em" }
  display-cover:{ fontFamily: "EB Garamond", cqw: 9.9, weight: 400, lineHeight: 0.98, tracking: "-0.028em" }
  number-unit:{ fontFamily: "JetBrains Mono", cqw: 2.08, weight: 500, lineHeight: 1.0 }

spacing:
  slide-pad: "4.2cqw"   # ~80px @1920
  gap-md: "1.7cqw"
  hairline: "1px"
  radius-sm: "6px"
  radius-md: "8px"
  radius-lg: "12px"
  radius-pill: "9999px"

components:
  card-hairline:
    backgroundColor: "{colors.cream} or {colors.tile}"
    border: "1px solid {colors.ink}@12%"
    rounded: "{spacing.radius-lg}"
    shadow: "{shadows.card}"
    typography: "{typography.card-title} + {typography.body}"
    description: "The editorial content card. Elevation is the hairline + ONE soft warm shadow — never a heavy drop, glow, or gradient."
  kicker-spike:
    typography: "{typography.kicker}"
    mark: "✱ coral spike prefix"
    description: "The eyebrow — JetBrains Mono uppercase, indexical (2–5 words), prefixed with the coral ✱. Never plain text, never a sentence."
  coral-callout:
    backgroundColor: "{colors.coral} (full-bleed) or {colors.cream} with a coral edge"
    textColor: "{colors.cream} on coral"
    rounded: "{spacing.radius-md}"
    typography: "{typography.button} / {typography.h2}"
    description: "The ONE voltage moment per frame — the CTA, the single inline link, OR the full-bleed band. Never two corals in one frame."
  number-lockup:
    typography: "{typography.number-hero} figure + {typography.number-unit} unit"
    description: "Hero stat — a EB Garamond figure paired with a JetBrains Mono unit (200K, +1,204, −318, 17 files). Figure is serif; the unit is ALWAYS mono, never the serif."
  pull-quote:
    typography: "{typography.quote-pull} (EB Garamond italic) + {typography.tag-upper} cite"
    description: "A commit message, a reviewer line, or the thesis. EB Garamond italic, small Inter uppercase cite beneath."
  section-rule:
    rule: "1px solid {colors.ink}@12% (or {colors.cream}@14% on navy)"
    description: "The only separator. A coral 1px rule may draw on to introduce a section. Never 2px+, never a heavy divider."
  code-surface:
    backgroundColor: "{colors.navy} body / {colors.navy-elev} title bar + status strip"
    textColor: "{colors.cream} (JetBrains Mono); syntax in coral (keywords) / teal #5DB8A6 (strings) / amber #E8A55A (numbers)"
    border: "1px solid {colors.cream}@14%"
    rounded: "{spacing.radius-md}"
    description: "The warm-navy code / terminal surface. The CODE ITSELF is rendered by the code-* registry blocks (code-diff / code-typing / code-snippet-*); this preset owns the surrounding surface, title bar, status strip, and mono chrome — not the code rendering."
  spike-mark:
    glyph: "✱ (U+2731), always {colors.coral}"
    description: "The brand mark. Fades + scales 0.92→1 on a single emphasis beat; never spins."
---

# Code editorial — Frame (video / frame layer)

## Overview

Code editorial at frame scale is a **warm-editorial brand book come to life** — the register of a literary
imprint or a research note. The thesis is three colors: **cream is the ground, ink is the voice,
coral is the voltage** — and a fourth (warm navy) only where code shows itself. Every surface is
**warm cream** (never pure white, never cool gray); content gathers on a **tile** surface half a
step darker — the demarcation is a half-step, never a hard contrast. Elevation is a **1px hairline**
ink border at low alpha plus, rarely, one soft warm shadow. There are no heavy drops, no glows, no
gradients on content.

Three editorial voices, each in its own face: **EB Garamond** carries every display moment — covers,
headlines, pull-quotes, big stat numerals — at large display sizes with gentle negative tracking;
its **italic** is the expressive register. **Inter** carries body, leads, card titles, buttons, and
UI chrome. **JetBrains Mono** carries the indexical layer — kickers, technical labels, the code
window, status strips. Switching a voice's face collapses the register: a sans headline or a serif
label reads as a different brand.

**Key characteristics at frame scale:**

- **Cream / ink / coral trinity** + a warm-navy code surface; cream is the default ground, ink the voice, coral the scarce voltage.
- **EB Garamond** (sentence case, negative-tracked) for all display; **Inter** body/chrome; **JetBrains Mono** index + code.
- **Hairline elevation** — a 1px low-alpha ink border + at most one soft warm shadow. No heavy drop, glow, or gradient.
- **Coral is rationed** — at most ONE coral moment per frame (CTA, inline link, OR full-bleed band); coral never sets a headline or a body run.
- **Density is free** — fill the frame as the content wants; a frame may stand on a single focal or carry a dense, layered composition.
- **The ✱ coral spike** opens kickers; warm navy is reserved for the code/terminal surface.

## The Frame

### Frame Craft Bar

Eyeball tests gate every frame before any structural check:

- **Squint** — one EB Garamond display moment dominates at 3–6× its neighbor.
- **Trinity** — cream/tile ground, ink text, coral exactly **once**; warm navy only on the code surface; no cool gray / pure white / fourth hue.
- **Type** — EB Garamond sentence-case display (negative-tracked); Inter 400 body; JetBrains Mono kickers (uppercase 0.16em, coral ✱) + code.

- **Primary:** 1920×1080 (16:9). Display authored in **`cqw`** (`px ÷ 1920 × 100 = cqw`).
- **Vertical:** 1080×1920 (9:16). **Square:** 1080×1080 (1:1).
- **Safe area:** `slide-pad` ~4.2cqw; the kicker/mono chrome sit inside it.

**The container law (load-bearing).** Every frame ground sets `container-type: size`; ALL
frame-relative units are `cqw`/`cqh` against it — never `vw`. Hairlines stay 1px; card radii stay
6/8/12px; the warm-paper reading must survive every ratio.

## Colors

Tokens identical to the source. Default ground `{colors.cream}`; content gathers on
`{colors.tile}` / `{colors.tile-strong}` (half-step warm steps, never a hard contrast).
**Headlines & body:** `{colors.ink}` on cream/tile; `{colors.cream}` on navy. **Coral**
(`{colors.coral}`) is the scarce voltage — one moment per frame (CTA, inline link, or full-bleed
band), never body text, never a card fill. **Warm navy** (`{colors.navy}` / `navy-soft` /
`navy-elev`) is the code / terminal / dark-card surface — a structural anchor, not a fourth brand
hue. **No cool grays, no pure white, no pure black.**

**Fixed syntax colors (decoration, NOT remixable brand hues).** When a code line is hand-set rather
than rendered by a `code-*` block, keywords are coral, strings are **teal `#5DB8A6`**, numbers are
**amber `#E8A55A`**; status reads success `#5DB872` / warn `#C64545`. These track the code surface,
not the brand trinity — keep them out of the brand palette.

## Typography

Two ramps. The **reading/chrome ramp** (Inter `body` 1.5cqw / `lead` 2.08cqw weight 400; JetBrains
Mono `kicker`/`mono-label` in px) carries copy + chrome; the **display ramp** (EB Garamond `headline` 4.6cqw
→ `display-cover` 9.9cqw, weight 400, negative-tracked) carries every headline + stat.

- **Legibility floor:** any load-bearing line ≥ **1.4cqw**; mono px labels are chrome only.
- **Fit-to-measure:** size the headline to its length. Cap the block at **≤ 78cqw**; ≤3 words → `display-cover`; 4–6 → `display`; 7+ → `headline`. Reserve the 7.3–9.9cqw tier for cover / statement / stat.
- **EB Garamond display is sentence case** (NOT title case, NOT uppercase), weight 400, negative-tracked (−0.012..−0.028em); reach for **italic** when the line is a stance or a definition. **Inter body** sentence case weight 400. **JetBrains Mono** kickers UPPERCASE 0.16em with the coral ✱. No uppercase serif, no sans headline, no serif label.

## Depth & Surface

Hairline elevation:

- **1px hairline** ink border at ~12% alpha is the primary lift (cream@14% on navy).
- **One soft warm shadow** (`0 1px 3px ink@8%, 0 4px 16px ink@4%`) — used rarely, never heavy.
- **Half-step surface** — a `{colors.tile}` block on cream reads elevated by the warm step, not by a cast shadow.

**Ceiling:** no heavy drop shadow, no glow, no gradient on content, no tilt. The system has no light
to emit; it reads by warmth and hairline.

## Shapes

- **6px** small chrome, **8px** cards / code surface, **12px** large cards / quote frames, **9999px** true pills only. No square corners, no heavy rounding; the editorial register is gently rounded, never hard.

## Components

- **card-hairline** — the editorial content card (hairline + one soft shadow). **section-rule** — the only separator (1px, coral may draw on).
- **kicker-spike** — the ✱ coral eyebrow. **coral-callout** — the one voltage moment (CTA / inline link / full-bleed band).
- **number-lockup** — EB Garamond figure + mono unit (the PR `+N / −M`, `200K`, file counts). **pull-quote** — EB Garamond italic + cite (a commit message / reviewer line).
- **code-surface** — the warm-navy code / terminal surface; the code itself comes from the **`code-*` registry blocks**, this owns the surface + mono chrome.
- **spike-mark** — the ✱ brand glyph, always coral.

## Frame Treatments

> Recipe: ground · container · composes · focal · chrome · accent · Fixed/Free · density.
> One coral moment per frame; open with a kicker-spike.

### 1 · Cover (identity · move: oversized EB Garamond · cream)

**Ground** `{colors.cream}`, `slide-pad`. **Composes** kicker-spike, display-cover, lead, mono-label index. **Focal** a 2–3 line EB Garamond `display-cover` (sentence case, ink) under a coral ✱ kicker. **Chrome** mono index strip (repo · branch). **Accent** the single coral ✱. **Fixed** EB Garamond 400 sentence case, hairline, cream ground. **Free** title, the mono index, layout + how full the frame runs. **Density** free.

### 2 · Statement (statement · move: single EB Garamond line · cream or navy)

**Ground** `{colors.cream}` (or `{colors.navy}` for gravity). **Composes** kicker-spike, display, optional lead. **Focal** one 2-line EB Garamond `display` carrying the change in a sentence — reach for **italic** if it's a stance. **Chrome** mono kicker. **Accent** none — the serif carries it (or one coral word). **Fixed** sentence-case serif. **Free** the line, ground, layout + density. **Density** free.

### 3 · Code Surface (code · move: warm-navy code window · the PR-critical frame)

**Ground** `{colors.cream}` framing a `{colors.navy}` **code-surface** (8px, cream@14% hairline, `navy-elev` title bar + filename in mono). **Composes** mono-label filename, the **`code-*` block** (code-diff / code-typing / code-snippet-_), optional `section-rule`. **Focal** the code panel — the diff / before→after / typed-on snippet. **Chrome** mono filename + status strip. **Accent** syntax coral/teal/amber inside the panel; one coral marker outside (e.g. a `+`/`−` gutter cue). **Fixed** warm-navy surface, mono code, hairline. **Free** which code-_ block, the code (from the diff), how large the panel runs. **Density** dense.

### 4 · Number / Impact (data · move: oversized figure · cream)

**Ground** `{colors.cream}`, `slide-pad`. **Composes** kicker-spike, number-lockup, lead/caption, optional `section-rule`. **Focal** a EB Garamond `number-hero` figure with a mono unit over a 1px rule — the PR impact (`+1,204 / −318`, `17 files`, `2.1× faster`). **Chrome** mono tag. **Accent** the figure in ink; at most one coral unit. **Fixed** serif figure + mono unit, hairline rule. **Free** the figures (from the script), tag, layout + density. **Density** free.

### 5 · Pull-quote (quote · move: EB Garamond italic · cream)

**Ground** `{colors.cream}`. **Composes** kicker-spike, pull-quote, tag-upper cite. **Focal** a EB Garamond **italic** `quote-pull` — a commit message, a reviewer line, or the thesis — with a small Inter uppercase cite (author · role) beneath. **Chrome** mono kicker. **Accent** none, or one coral mark. **Fixed** EB Garamond italic quote + uppercase cite. **Free** quote, attribution, layout + density. **Density** free.

### 6 · Closing / CTA (closer · move: coral voltage · cream or navy)

**Ground** `{colors.cream}` (or `{colors.navy}`). **Composes** display sign-off, coral-callout, optional contributor row (`assets/<login>.png` avatars + mono names). **Focal** a short EB Garamond sign-off with the one **coral-callout** (the CTA or full-bleed band) and, for a "shipped-by" close, a row of hairline-ringed avatar chips. **Chrome** mono index. **Accent** the single coral voltage. **Fixed** one coral moment, hairline avatar rings, sentence-case serif. **Free** sign-off, who ships, layout + density. **Density** free.

## Composition Rules

### Do

- Stand every frame on the **warm cream floor**; gather content on a **half-step tile** surface.
- Set all display in **EB Garamond, sentence case**, negative-tracked; **Inter 400** body; **JetBrains Mono** kickers (uppercase, 0.16em, coral ✱) + code.
- Ration **coral to one moment per frame** — CTA, inline link, OR full-bleed band.
- Elevate with a **1px hairline** + at most one soft warm shadow; reserve **warm navy** for the code/terminal surface.
- Lead with **one clear focal**; open regions with a **kicker-spike**. Fill the frame as the content wants.
- Pair a EB Garamond figure with a **mono unit** for every stat; render code via the **`code-*` blocks** on the navy surface.

### Don't

- No pure white, no cool gray, no pure black; no fourth brand hue (navy is structural, syntax colors are decoration).
- No heavy drop shadow, glow, gradient on content, or tilt — hairline elevation only.
- No uppercase or title-case EB Garamond display; no sans headline; no serif label; no serif-set numeric unit.
- No two coral moments in one frame; coral never sets a headline or body run.
- Don't blow a headline past the measure — step the ramp down.

## Aspect-Ratio Behavior

| Treatment     | 16:9                    | 9:16                        | 1:1                    |
| ------------- | ----------------------- | --------------------------- | ---------------------- |
| Cover         | display left, index top | display top, index below    | display, index corner  |
| Statement     | line left/centered      | line stacked                | centered               |
| Code Surface  | panel framed in cream   | panel taller, fewer lines   | panel centered, square |
| Number/Impact | figure left             | figure centered, taller     | centered               |
| Pull-quote    | quote left              | quote stacked               | centered               |
| Closing/CTA   | sign-off + avatar row   | sign-off top, avatars below | centered, avatars wrap |

`slide-pad` holds on the short edge; re-step display above the 1.4cqw floor. The code surface keeps
its hairline + mono chrome on every ratio; the avatar row wraps rather than shrinks below legibility.

## Approved Real Entities

No real customers, logos, or vendors are defined in the source — render any such mark as a
placeholder. Contributor avatars come from the project's `assets/<login>.png` (staged from the PR's
people graph); the ✱ spike, hairlines, and the code surface are CSS-only and need no external imagery.

## Numerals & Claims (hard rule)

Never invent figures, stats, diffs, or counts at frame scale. Render slots as `— figure —`,
`{metric}`, `+N / −M`. Number-lockups, code panels, and impact stats carry placeholders until the
script (from the PR ingest) supplies real values. Branch names, file counts, and `+/−` totals trace
to the diff; commit/issue numbers are chrome.

## Pre-Render Self-Audit

- **Squint** — one EB Garamond display moment dominates.
- **Trinity** — cream floor + tile step + ink voice; coral appears exactly once; warm navy only on the code surface; no cool gray / pure white / fourth hue.
- **Type** — EB Garamond sentence-case display (negative-tracked); Inter 400 body; JetBrains Mono kickers (uppercase 0.16em, coral ✱) + code; ≥1.4cqw floor.
- **Depth** — 1px hairline + at most one soft warm shadow; no heavy drop / glow / gradient / tilt; 6/8/12px radii.
- **Code** — code rendered by a `code-*` block on the warm-navy surface; syntax coral/teal/amber; figures paired with a mono unit.
- **Fabrication** — every numeral / diff traces to the PR, else placeholder.

## Known Gaps

- **Motion intentionally out of scope.** frame.md specifies composition only. Code editorial's motion register — short cross-dissolves, no overshoot/bounce/elastic, coral the only "draw-on", numbers count up, code types on line by line — lives in the workflow's `motion-language.md` + `hyperframes-animation`, not here.
- **EB Garamond + Inter + JetBrains Mono ship as licensed local WOFF2 assets with this preset.** `build-frame.mjs` stages weights 400 + 700 into `assets/fonts/` and appends the exact `@font-face` block to the generated `frame.md`, so Studio, snapshots, and renders resolve them offline without a first-run Google Fonts fetch. Author display at **weight 400** (700 reads as a heavy bold, off-register), and treat italic as the browser-synthesized slant (acceptable for the pull-quote register; add a real italic face only if a project leans hard on it). EB Garamond is a warm old-style serif (low contrast, humanist); if it ever fails, fall to Georgia or another old-style serif — never to a sans. CJK: Noto Serif SC (display) / Noto Sans SC (body) / Noto Sans Mono CJK (code); the sentence-case warmth carries when the serif drops.
- **Syntax colors (teal `#5DB8A6` / amber `#E8A55A` / status) are fixed decoration**, declared in §Colors — they are NOT in the remixable `colors:` block, so a brand remix never repaints them.
- **The code itself is the `code-*` registry blocks**, not this preset — this preset owns only the surrounding warm-navy surface + mono chrome.
- **9:16 / 1:1 are guidance**; verify the legibility floor and that the cream/tile warmth + one-coral discipline hold per ratio.


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


<!-- ===== FILE: hyperframes/hyperframes-creative/references/typography.md ===== -->

# Typography

The compiler **pre-bundles a fixed set** of fonts (the table below) — write one of those families in `font-family` and it renders deterministically, offline, with no setup and no warning. A name _outside_ that set is **not silently dropped**: if it's a real Google font the compiler fetches it from Google Fonts at **build time** and embeds it, so it _does_ render — but that implicit path (a) trips a `font_family_without_font_face` lint warning, and (b) is **fail-closed in distributed/cloud renders** — if Google is unreachable the render _errors_ rather than quietly substituting a system font. Beyond that, **local renders auto-capture fonts you actually have**: a family installed on your machine, a local `@font-face` path, or an external CDN stylesheet all get compressed to woff2 and inlined at build time. So a name on **neither** the bundle **nor** Google Fonts only truly falls back to a generic system font when it's _also_ not installed locally and not declared in an `@font-face` — and even that logs a compiler warning. **One caveat**: distributed/cloud (Lambda) renders disable system-font capture, so don't rely on a locally-installed-only font for those. So don't assume an un-bundled display name will Just Work: for anything that must render predictably, pick a bundled family below **or embed your own `@font-face`** (see "Finding Fonts").

## Contents

- Fonts that embed (auto-resolve)
- Banned fonts
- Guardrails
- What you do not do without being told
- Finding fonts
- Selection thinking
- Similar-font pairing
- Dark backgrounds
- OpenType features for data

## Fonts That Embed (auto-resolve)

These **18 families** are the ones the renderer **pre-bundles** — embedded as local data URIs with no network fetch, so they render offline and deterministically with zero setup, no lint warning, and no fail-closed fetch risk. Write any of them as a `font-family` and it renders; **only the listed weights exist** (asking for a weight a family doesn't ship gives a synthetic/fallback weight, not a real cut). (Any _other_ real Google font still works via the implicit build-time fetch described in the intro — but only these render with none of those caveats.)

| Family            | Weights         | Role              |
| ----------------- | --------------- | ----------------- |
| Inter             | 400 · 700 · 900 | sans (body/UI)    |
| Roboto            | 400 · 700 · 900 | sans              |
| Open Sans         | 400 · 700       | sans              |
| Lato              | 400 · 700 · 900 | sans              |
| Nunito            | 400 · 700 · 900 | sans (rounded)    |
| Montserrat        | 400 · 700 · 900 | geometric sans    |
| Poppins           | 400 · 700 · 900 | geometric sans    |
| Outfit            | 400 · 700 · 900 | geometric sans    |
| Oswald            | 400 · 700       | condensed sans    |
| **League Gothic** | **400 only**    | condensed display |
| **Archivo Black** | **400 only**    | heavy display     |
| Playfair Display  | 400 · 700 · 900 | serif (display)   |
| EB Garamond       | 400 · 700       | serif (text)      |
| Space Mono        | 400 · 700       | mono              |
| IBM Plex Mono     | 400 · 700       | mono              |
| JetBrains Mono    | 400 · 700       | mono              |
| Source Code Pro   | 400 · 700       | mono              |
| Noto Sans JP      | 400 · 700       | CJK (Japanese)    |

> ⚠ **League Gothic and Archivo Black ship weight 400 ONLY** — they are already heavy/condensed display faces. Do not request `font-weight: 700/900` on them.

**Aliases** — these common names resolve to an embedded family, so you may safely write them: `Helvetica Neue` / `Helvetica` / `Arial` → Inter · `Futura` / `DIN Alternate` / `Arial Black` → Montserrat · `Bebas Neue` → League Gothic · `Segoe UI` → Roboto · `Courier New` / `Courier` → JetBrains Mono · `Garamond` → EB Garamond. (This is why a "safe" `Helvetica Neue` stack always renders — it maps to embedded Inter.)

**Reconciling with the Banned list below:** several embedded families (Inter, Roboto, Open Sans, Lato, Nunito, Poppins, Outfit, Playfair Display, EB Garamond) are _also_ on the Banned monoculture list — they render fine but read as generic. The families that are **embedded AND not banned** — your safe-and-distinctive picks — are: **Montserrat, Oswald, League Gothic, Archivo Black, Space Mono, IBM Plex Mono, JetBrains Mono, Source Code Pro, Noto Sans JP**. Reach for these (or a non-bundled font you've confirmed via the Finding-Fonts step). A non-bundled name isn't guaranteed-broken — a real Google font is auto-fetched and embedded — but it carries a lint warning and a fail-closed fetch in cloud renders, so for anything that must render predictably, **embed it yourself via `@font-face`** (see "Finding Fonts") rather than relying on the implicit fetch.

## Banned

Training-data defaults that every LLM reaches for. These produce monoculture across compositions.

Inter, Roboto, Open Sans, Noto Sans, Arimo, Lato, Source Sans, PT Sans, Nunito, Poppins, Outfit, Sora, Playfair Display, Cormorant Garamond, Bodoni Moda, EB Garamond, Cinzel, Prata, Syne

**Syne in particular** is the most overused "distinctive" display font. It is an instant AI design tell.

## Guardrails

You know these rules but you violate them. Stop.

- **Don't pair two sans-serifs.** You do this constantly — one for headlines, one for body. Cross the boundary: serif + sans, or sans + mono.
- **One expressive font per scene.** You pick two interesting fonts trying to make it "better." One performs, one recedes.
- **Weight contrast must be extreme.** You default to 400 vs 700. Video needs 300 vs 900. The difference must be visible in motion at a glance.
- **Video sizes, not web sizes.** Full-screen viewing (YouTube / website embed): body 20px minimum, headlines 60px+, data labels 16px. **In-feed viewing** (destination = X / LinkedIn / Instagram feed — `hyperframes/references/brief-contract.md` § 2): the video plays small inside a scrolling feed, so scale up — body ≥32px, headlines ≥90px, data labels ≥24px (first-pass values; calibrate against real renders). You will try to use 14px. Don't.

## What You Don't Do Without Being Told

- **Tension should mean something.** Don't pattern-match pairings. Ask WHY these two fonts disagree. The pairing should embody the content's contradiction — mechanical vs human, public vs private, institutional vs personal. If you can't articulate the tension, it's arbitrary.
- **Register switching.** Assign different fonts to different communicative modes — one voice for statements, another for data, another for attribution. Not hierarchy on a page. Voices in a conversation.
- **Tension can live inside a single font.** A font that looks familiar but is secretly strange creates tension with the viewer's expectations, not with another font.
- **One variable changed = dramatic contrast.** Same letterforms, monospaced vs proportional. Same family at different optical sizes. Changing only rhythm while everything else stays constant.
- **Double personality works.** Two expressive fonts can coexist if they share an attitude (both irreverent, both precise) even when their forms are completely different.
- **Time is hierarchy.** The first element to appear is the most important. In video, sequence replaces position.
- **Motion is typography.** How a word enters carries as much meaning as the font. A 0.1s slam vs a 2s fade — same font, completely different message.
- **Fixed reading time.** 3 seconds on screen = must be readable in 2. Fewer words, larger type.
- **Tracking tighter than web.** -0.03em to -0.05em on display sizes. Video encoding compresses letter detail.

## Finding Fonts

Don't default to what you know. If the content is luxury, a grotesque sans might create more tension than the expected Didone serif. Decide the register first, then search.

Save this script to `/tmp/fontquery.py` and run with `curl -s 'https://fonts.google.com/metadata/fonts' > /tmp/gfonts.json && python3 /tmp/fontquery.py /tmp/gfonts.json`:

```python
import json, sys, random
from collections import OrderedDict

random.seed()  # true random each run

with open(sys.argv[1]) as f:
    data = json.load(f)
fonts = data.get("familyMetadataList", [])

ban = {"Inter","Roboto","Open Sans","Noto Sans","Lato","Poppins","Source Sans 3",
       "PT Sans","Nunito","Outfit","Sora","Playfair Display","Cormorant Garamond",
       "Bodoni Moda","EB Garamond","Cinzel","Prata","Arimo","Source Sans Pro","Syne"}
skip_pfx = ("Roboto","Noto ","Google Sans","Bpmf","Playwrite","Anek","BIZ ",
            "Nanum","Shippori","Sawarabi","Zen ","Kaisei","Kiwi ","Yuji ","Radio ")

def ok(f):
    if f["family"] in ban: return False
    if any(f["family"].startswith(b) for b in skip_pfx): return False
    if "latin" not in (f.get("subsets") or []): return False
    return True

seen = set()
R = OrderedDict()

# Trending Sans — recent (2022+), popular (<300)
R["Trending Sans"] = []
for f in fonts:
    if not ok(f) or f["family"] in seen: continue
    if f.get("category") in ("Sans Serif","Display") and f.get("dateAdded","") >= "2022-01-01" and f.get("popularity",9999) < 300:
        R["Trending Sans"].append(f); seen.add(f["family"])

# Trending Serif — recent (2018+), popular (<600)
R["Trending Serif"] = []
for f in fonts:
    if not ok(f) or f["family"] in seen: continue
    if f.get("category") == "Serif" and f.get("dateAdded","") >= "2018-01-01" and f.get("popularity",9999) < 600:
        R["Trending Serif"].append(f); seen.add(f["family"])

# Monospace — recent (2018+), popular (<600)
R["Monospace"] = []
for f in fonts:
    if not ok(f) or f["family"] in seen: continue
    if f.get("category") == "Monospace" and f.get("dateAdded","") >= "2018-01-01" and f.get("popularity",9999) < 600:
        R["Monospace"].append(f); seen.add(f["family"])

# Impact & Condensed — heavy display fonts with 800+ weight
R["Impact & Condensed"] = []
for f in fonts:
    if not ok(f) or f["family"] in seen: continue
    has_heavy = any(k in list(f.get("fonts",{}).keys()) for k in ("800","900"))
    is_display = f.get("category") in ("Sans Serif","Display")
    if has_heavy and is_display and f.get("popularity",9999) < 400:
        R["Impact & Condensed"].append(f); seen.add(f["family"])

# Script & Handwriting — popular (<300)
R["Script & Handwriting"] = []
for f in fonts:
    if not ok(f) or f["family"] in seen: continue
    if f.get("category") == "Handwriting" and f.get("popularity",9999) < 300:
        R["Script & Handwriting"].append(f); seen.add(f["family"])


# Randomize the top 5 in each category so the LLM doesn't always pick the same first result
for cat in R:
    R[cat].sort(key=lambda x: x.get("popularity",9999))
    top5 = R[cat][:5]
    rest = R[cat][5:]
    random.shuffle(top5)
    R[cat] = top5 + rest
limits = {"Trending Sans":15,"Trending Serif":12,"Monospace":8,
          "Impact & Condensed":12,"Script & Handwriting":10}
for cat in R:
    items = R[cat][:limits.get(cat,10)]
    if not items: continue
    print(f"--- {cat} ({len(items)}) ---")
    for ff in items:
        var = "VAR" if ff.get("axes") else "   "
        print(f'  {ff.get("popularity"):4d} | {var} | {ff["family"]}')
    print()
```

Five categories: trending sans, trending serif, monospace, impact/condensed, script/handwriting. All dynamically filtered from Google Fonts metadata — no hardcoded font names. Cross classification boundaries when pairing.

## Selection Thinking

Don't pick fonts by category reflex (editorial → serif, tech → mono, modern → geometric sans). That's pattern matching, not design.

1. **Name the register.** What voice is the content speaking in? Institutional authority? Personal confession? Technical precision? Casual irreverence? The register narrows the field more than the category.
2. **Think physically.** Imagine the font as a physical object the brand could ship — a museum exhibit caption, a hand-painted shop sign, a 1970s mainframe terminal manual, a fabric label inside a coat, a children's book printed on cheap newsprint, a tax form. Whichever physical object fits the register is pointing at the right _kind_ of typeface.
3. **Reject your first instinct.** The first font that feels right is usually your training-data default for that register. If you picked it last time too, find something else.
4. **Cross-check the assumption.** An editorial brief does NOT need a serif. A technical brief does NOT need a sans. A children's product does NOT need a rounded display font. The most distinctive choice often contradicts the category expectation.

## Similar-Font Pairing

Never pair two fonts that are similar but not identical — two geometric sans-serifs, two transitional serifs, two humanist sans. They create visual friction without clear hierarchy. The viewer senses something is "off" but can't articulate it. Either use one font at two weights, or pair fonts that contrast on multiple axes: serif + sans, condensed + wide, geometric + humanist.

## Dark Backgrounds

Light text on dark backgrounds creates two optical illusions you need to compensate for:

- **Increased apparent weight.** Light-on-dark reads heavier than dark-on-light at the same `font-weight`. Use 350 instead of 400 for body text. Headlines are less affected because size compensates.
- **Tighter apparent spacing.** Light halos around letterforms reduce perceived gaps. Increase `line-height` by 0.05-0.1 beyond your light-background value. For display sizes, add 0.01em `letter-spacing` to counteract.

## OpenType Features for Data

Most fonts ship with OpenType features that are off by default. Turn them on for data compositions:

```css
/* Tabular numbers — digits align vertically in columns */
.stat-value,
.timer,
.data-column {
  font-variant-numeric: tabular-nums;
}

/* Diagonal fractions — renders 1/2 as ½ */
.recipe-amount,
.ratio {
  font-variant-numeric: diagonal-fractions;
}

/* Small caps for abbreviations — less visual shouting */
.abbreviation,
.unit {
  font-variant-caps: all-small-caps;
}

/* Disable ligatures in code — fi, fl, ffi should stay separate */
code,
.code {
  font-variant-ligatures: none;
}
```

`tabular-nums` is essential any time numbers are stacked vertically — stat callouts, timers, scoreboards, data tables. Without it, digits have proportional widths and columns don't align.


<!-- ===== FILE: hyperframes/hyperframes-creative/references/video-composition.md ===== -->

# Video Composition

Video frames are not web pages. Use these rules for design-led compositions while respecting the requested format, brand, and scope. Minimal technical compositions and intentionally sparse formats may need less detail.

## The Design Spec Is Brand, Not Layout

The design spec (`frame.md` or `design.md`) defines what the brand looks like: colors, fonts, personality, constraints. It does NOT define how to compose a video frame. Use brand colors at video-appropriate intensity — not at web-UI opacity.

**Strict from the design spec:** hex values (including background color), font families, weight relationships, Do's and Don'ts. If the user chose a light canvas, use a light canvas. If they chose dark, use dark. Do not override their palette.

**Adapt for video:** type sizes, spacing, decorative opacity, border weight, component treatments. A web UI card at `border: 1px solid #e2e3e6` with `box-shadow: 0 2px 4px rgba(0,0,0,0.06)` is invisible on video. The brand color is sacred; the application is yours.

## Density

Choose density from the message and format. A brand or sizzle frame often needs several visual roles to feel produced; a lower-third, logo sting, or static title may need only a few.

For a scene that should feel layered, plan these roles:

- **Background treatment** — radial glow, oversized ghost type, color panel, grain, grid, or an intentionally flat field justified by the concept.
- **Midground content** — the actual message. Cards, stats, code blocks, images.
- **Foreground accents** — dividers, labels, data bars, registration marks, monospace metadata. The details that make it feel produced, not generated.

For produced marketing frames, roughly 6–10 visual roles can be a useful starting point, not a contract. Add decoration only when it reinforces hierarchy, motion, or the concept. Decorative treatment must not become new user-facing content, new scenes, or unrequested claims.

## Color Presence

Muted is fine. Flat is not. Every scene should have at least one color that pulls the eye.

- Brand accent should be VISIBLE — not a 5% opacity glow lost in compression. 15-25% for atmospheric, full saturation for focal elements.
- **Light canvases work differently than dark.** On dark: accent glows pop naturally. On light: use bolder borders (2px+ solid), stronger structural elements (rules, dividers), and full-saturation accent hits. Light backgrounds need texture (subtle grain, patterns) to avoid the "blank slide" feel. Don't switch to dark — make light cinematic.
- **No full-screen linear gradients on dark backgrounds.** They band visibly under H.264 compression. Use a radial gradient, a solid fill, or solid + localized glow instead.
- Tint neutrals toward the brand hue. Dead gray reads as undesigned.

## Scale

Web sizes are invisible on video. Everything scales up.

| Element            | Web     | Video    |
| ------------------ | ------- | -------- |
| Headlines          | 32-48px | 64-120px |
| Body text          | 14-16px | 28-42px  |
| Labels             | 12px    | 18-24px  |
| Decorative opacity | 3-8%    | 12-25%   |
| Borders            | 1px     | 2-4px    |
| Padding            | 16-32px | 60-140px |

If you're writing a font-size under 24px in a video composition, justify it. If you're writing decorative opacity under 10%, it's invisible.

## Motion Intensity

Subtle reads as static at 30fps. Err toward more movement than feels safe.

- Every decorative element should have ambient motion: breathe, drift, pulse, orbit. Static decoratives feel dead.
- Vary motion per scene — don't repeat the same ambient pattern.
- Scene entrances should use 3+ different eases and directions. If every element enters from `y: 30, opacity: 0`, the scene has no choreography.

## Frame Composition

- **Two focal points minimum.** The eye needs somewhere to travel.
- **Fill the frame.** Hero text: 60-80% of frame width.
- **Anchor to edges.** Pin content to left/top or right/bottom. Centered-and-floating is a web layout pattern.
- **Split frames.** Data panel left, content right. Top bar with metadata, full-width below. Zone-based layouts over centered stacks.
- **Structural elements.** Rules, dividers, border panels. They create visual paths and animate well (`scaleX: 0` → `1`).


<!-- ===== FILE: hyperframes/hyperframes-creative/references/visual-styles.md ===== -->

# Visual Style Library

Named visual identities for HyperFrames videos. Each style is grounded in a real graphic design tradition and expressed as a DESIGN.md-compatible token block. Use them as starters — copy the YAML into your project's `design.md` front matter, then customize.

**How to pick:** Match mood first, content second. Ask: _"What should the viewer FEEL?"_

**How to use:** Copy the style's YAML token block into `design.md` front matter. Add `## Overview`, `## Colors`, `## Typography`, `## Elevation`, `## Components`, `## Do's and Don'ts` prose sections to complete the file.

## Contents

- Quick reference
- Swiss Pulse
- Velvet Standard
- Deconstructed
- Maximalist Type
- Data Drift
- Soft Signal
- Folk Frequency
- Shadow Cut
- Mood to style guide
- Creating custom styles

## Quick Reference

| Style           | Mood                  | Best for                           | Transition shader                 |
| --------------- | --------------------- | ---------------------------------- | --------------------------------- |
| Swiss Pulse     | Clinical, precise     | SaaS, data, dev tools, metrics     | Cinematic Zoom or SDF Iris        |
| Velvet Standard | Premium, timeless     | Luxury, enterprise, keynotes       | Cross-Warp Morph                  |
| Deconstructed   | Industrial, raw       | Tech launches, security, punk      | Glitch or Whip Pan                |
| Maximalist Type | Loud, kinetic         | Big announcements, launches        | Ridged Burn                       |
| Data Drift      | Futuristic, immersive | AI, ML, cutting-edge tech          | Gravitational Lens or Domain Warp |
| Soft Signal     | Intimate, warm        | Wellness, personal stories, brand  | Thermal Distortion                |
| Folk Frequency  | Cultural, vivid       | Consumer apps, food, communities   | Swirl Vortex or Ripple Waves      |
| Shadow Cut      | Dark, cinematic       | Dramatic reveals, security, exposé | Domain Warp                       |

---

## 1. Swiss Pulse — Josef Müller-Brockmann

**Mood:** Clinical, precise | **Best for:** SaaS dashboards, developer tools, APIs, metrics

```yaml
name: Swiss Pulse
colors:
  primary: "#1a1a1a"
  on-primary: "#ffffff"
  accent: "#0066FF"
typography:
  headline:
    fontFamily: Helvetica Neue
    fontSize: 5rem
    fontWeight: 700
  label:
    fontFamily: Inter
    fontSize: 0.875rem
    fontWeight: 400
  stat:
    fontFamily: Helvetica Neue
    fontSize: 7rem
    fontWeight: 700
rounded:
  none: 0px
  sm: 2px
spacing:
  sm: 8px
  md: 16px
  lg: 32px
motion:
  energy: high
  easing:
    entry: "expo.out"
    exit: "power4.in"
    ambient: "none"
  duration:
    entrance: 0.4
    hold: 1.5
    transition: 0.6
  atmosphere:
    - grid-lines
    - registration-marks
  transition: cinematic-zoom
```

Grid-locked compositions. Every element snaps to an invisible 12-column grid. Numbers dominate the frame at 80–120px. Animated counters count up from 0. Hard cuts, no decorative transitions. Nothing floats.

---

## 2. Velvet Standard — Massimo Vignelli

**Mood:** Premium, timeless | **Best for:** Luxury products, enterprise software, keynotes, investor decks

```yaml
name: Velvet Standard
colors:
  primary: "#0a0a0a"
  on-primary: "#ffffff"
  accent: "#1a237e"
typography:
  headline:
    fontFamily: Inter
    fontSize: 3rem
    fontWeight: 300
    letterSpacing: 0.15em
    textTransform: uppercase
  body:
    fontFamily: Inter
    fontSize: 1rem
    fontWeight: 300
    lineHeight: 1.6
rounded:
  sm: 0px
  md: 2px
spacing:
  sm: 16px
  md: 32px
  lg: 64px
motion:
  energy: calm
  easing:
    entry: "sine.inOut"
    exit: "power1.in"
    ambient: "sine.inOut"
  duration:
    entrance: 1.2
    hold: 3.0
    transition: 1.5
  atmosphere:
    - subtle-grain
    - hairline-rules
  transition: cross-warp-morph
```

Generous negative space. Symmetrical, centered, architectural precision. Thin sans-serif, ALL CAPS, wide letter-spacing. Sequential reveals with long holds. Nothing snaps — everything glides with intention. Luxury takes its time.

---

## 3. Deconstructed — Neville Brody

**Mood:** Industrial, raw | **Best for:** Tech news, developer launches, security products, punk-energy reveals

```yaml
name: Deconstructed
colors:
  primary: "#1a1a1a"
  on-primary: "#f0f0f0"
  accent: "#D4501E"
typography:
  headline:
    fontFamily: Space Grotesk
    fontSize: 4rem
    fontWeight: 700
  label:
    fontFamily: Space Mono
    fontSize: 0.75rem
    fontWeight: 700
    textTransform: uppercase
rounded:
  none: 0px
spacing:
  sm: 4px
  md: 12px
  lg: 24px
motion:
  energy: high
  easing:
    entry: "back.out(2.5)"
    exit: "steps(8)"
    ambient: "elastic.out(1.2, 0.4)"
  duration:
    entrance: 0.3
    hold: 1.0
    transition: 0.5
  atmosphere:
    - scan-lines
    - glitch-artifacts
    - grain-overlay
  transition: glitch
```

Type at angles, overlapping edges, escaping frames. Bold industrial weight. Gritty textures: scan-line effects, glitch artifacts baked into design. Text SLAMS and SHATTERS. Letters scramble then snap to final position. Intentional irregularity — nothing should feel polished.

---

## 4. Maximalist Type — Paula Scher

**Mood:** Loud, kinetic | **Best for:** Big product launches, milestone announcements, high-energy hype videos

```yaml
name: Maximalist Type
colors:
  primary: "#0a0a0a"
  on-primary: "#ffffff"
  accent-red: "#E63946"
  accent-yellow: "#FFD60A"
typography:
  headline:
    fontFamily: Anton
    fontSize: 8rem
    fontWeight: 400
    textTransform: uppercase
  subhead:
    fontFamily: Space Grotesk
    fontSize: 3rem
    fontWeight: 700
rounded:
  none: 0px
spacing:
  sm: 0px
  md: 8px
motion:
  energy: high
  easing:
    entry: "expo.out"
    exit: "back.out(1.8)"
    ambient: "power3.out"
  duration:
    entrance: 0.3
    hold: 0.8
    transition: 0.4
  atmosphere:
    - type-layers
    - color-blocks
  transition: ridged-burn
```

Text IS the visual. Overlapping type layers at different scales and angles, filling 50–80% of frame. Bold saturated colors — maximum contrast. Everything kinetic: slamming, sliding, scaling. 2–3 second rapid-fire scenes. No static moments. Fast arrivals, hard stops.

---

## 5. Data Drift — Refik Anadol

**Mood:** Futuristic, immersive | **Best for:** AI products, ML platforms, data companies, speculative tech

```yaml
name: Data Drift
colors:
  primary: "#0a0a0a"
  on-primary: "#e0e0e0"
  accent-purple: "#7c3aed"
  accent-cyan: "#06b6d4"
typography:
  headline:
    fontFamily: Inter
    fontSize: 2.5rem
    fontWeight: 200
    letterSpacing: 0.05em
  body:
    fontFamily: Inter
    fontSize: 0.875rem
    fontWeight: 300
rounded:
  sm: 4px
  md: 12px
  full: 9999px
spacing:
  sm: 16px
  md: 32px
  lg: 64px
motion:
  energy: moderate
  easing:
    entry: "sine.inOut"
    exit: "power2.out"
    ambient: "sine.inOut"
  duration:
    entrance: 1.0
    hold: 2.5
    transition: 1.5
  atmosphere:
    - particle-field
    - light-traces
    - radial-glow
  transition: gravitational-lens
```

Thin futuristic sans-serif — floating, weightless, minimal. Fluid morphing compositions. Extreme scale shifts (micro → macro). Particles coalesce into numbers. Light traces data paths through the frame. Smooth, continuous, organic. Nothing hard.

---

## 6. Soft Signal — Stefan Sagmeister

**Mood:** Intimate, warm | **Best for:** Wellness brands, personal stories, lifestyle products, human-centered apps

```yaml
name: Soft Signal
colors:
  primary: "#FFF8EC"
  on-primary: "#2a2a2a"
  accent-amber: "#F5A623"
  accent-rose: "#C4A3A3"
  accent-sage: "#8FAF8C"
typography:
  headline:
    fontFamily: Playfair Display
    fontSize: 3rem
    fontWeight: 400
    fontStyle: italic
  body:
    fontFamily: Inter
    fontSize: 1rem
    fontWeight: 300
    lineHeight: 1.7
rounded:
  sm: 8px
  md: 16px
  lg: 24px
  full: 9999px
spacing:
  sm: 12px
  md: 24px
  lg: 48px
motion:
  energy: calm
  easing:
    entry: "sine.inOut"
    exit: "power1.inOut"
    ambient: "sine.inOut"
  duration:
    entrance: 1.0
    hold: 3.0
    transition: 1.5
  atmosphere:
    - soft-gradient
    - warm-grain
  transition: thermal-distortion
```

Handwritten-style or humanist serif fonts. Personal, lowercase, delicate. Close-up framing: single element fills the frame. Slow drifts and floats, never snaps. Soft organic motion. Nothing should feel hurried or polished. Intimate, never corporate.

---

## 7. Folk Frequency — Eduardo Terrazas

**Mood:** Cultural, vivid | **Best for:** Consumer apps, food platforms, community products, festive launches

```yaml
name: Folk Frequency
colors:
  primary: "#ffffff"
  on-primary: "#1a1a1a"
  accent-pink: "#FF1493"
  accent-blue: "#0047AB"
  accent-yellow: "#FFE000"
  accent-green: "#009B77"
typography:
  headline:
    fontFamily: Fredoka One
    fontSize: 4rem
    fontWeight: 400
  body:
    fontFamily: Nunito
    fontSize: 1rem
    fontWeight: 600
rounded:
  sm: 8px
  md: 16px
  lg: 32px
  full: 9999px
spacing:
  sm: 8px
  md: 16px
  lg: 32px
motion:
  energy: high
  easing:
    entry: "back.out(1.6)"
    exit: "elastic.out(1, 0.5)"
    ambient: "sine.inOut"
  duration:
    entrance: 0.5
    hold: 1.5
    transition: 0.8
  atmosphere:
    - pattern-tiles
    - confetti-burst
    - color-blocks
  transition: swirl-vortex
```

Bold warm rounded type. Pattern and repetition — folk art rhythm and density. Layered compositions with rich visual texture. Every frame feels handcrafted. Colorful motion: elements bounce, pop, spin into place with joy. Overshoots feel intentional. Celebratory energy.

---

## 8. Shadow Cut — Hans Hillmann

**Mood:** Dark, cinematic | **Best for:** Security products, dramatic reveals, investigative content, intense launches

```yaml
name: Shadow Cut
colors:
  primary: "#0a0a0a"
  on-primary: "#f0f0f0"
  surface: "#3a3a3a"
  accent: "#C1121F"
typography:
  headline:
    fontFamily: Oswald
    fontSize: 4rem
    fontWeight: 700
    textTransform: uppercase
  body:
    fontFamily: Inter
    fontSize: 0.875rem
    fontWeight: 400
rounded:
  none: 0px
  sm: 2px
spacing:
  sm: 8px
  md: 16px
  lg: 48px
motion:
  energy: moderate
  easing:
    entry: "power3.out"
    exit: "power4.in"
    ambient: "sine.inOut"
  duration:
    entrance: 0.8
    hold: 2.5
    transition: 1.2
  atmosphere:
    - deep-shadow
    - vignette
    - grain-overlay
  transition: domain-warp
```

Near-monochrome: deep blacks, cold greys, stark white + one blood accent. Sharp angular text like film noir title cards. Heavy contrast, no softness. Elements emerge from darkness — reveal is the narrative. Slow creeping push-ins, dramatic scale reveals. The pause before the hit matters. Domain Warp dissolves reality before the next scene.

---

## Mood → Style Guide

| If the content feels...            | Use...          |
| ---------------------------------- | --------------- |
| Data-driven, analytical, technical | Swiss Pulse     |
| Premium, enterprise, luxury        | Velvet Standard |
| Raw, punk, aggressive, rebellious  | Deconstructed   |
| Hype, loud, high-energy launch     | Maximalist Type |
| AI, ML, speculative, futuristic    | Data Drift      |
| Human, warm, personal, wellness    | Soft Signal     |
| Cultural, fun, consumer, festive   | Folk Frequency  |
| Dark, dramatic, intense, cinematic | Shadow Cut      |

---

## Creating Custom Styles

These 8 styles are starters — not constraints. Create your own:

1. **Name it** after a designer, art movement, or cultural reference
2. **Write YAML tokens** — `colors` (2–5 tokens), `typography` (2–3 scales), `rounded`, `spacing`, `motion` (energy + easing + duration + atmosphere + transition)
3. **Add prose** — one paragraph describing the feel, what to do, what to avoid
4. **Token references** — use `{colors.accent}`, `{typography.headline}` in component definitions

The pattern: **YAML tokens (what) → prose rationale (why) → components (how they combine).**
