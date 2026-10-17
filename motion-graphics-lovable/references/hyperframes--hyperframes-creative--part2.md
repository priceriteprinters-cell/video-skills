

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
