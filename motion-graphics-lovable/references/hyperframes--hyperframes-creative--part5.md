

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
