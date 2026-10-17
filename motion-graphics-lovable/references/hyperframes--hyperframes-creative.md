

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
