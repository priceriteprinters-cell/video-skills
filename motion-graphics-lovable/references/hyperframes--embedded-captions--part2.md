

<!-- ===== FILE: hyperframes/embedded-captions/dna/README.md ===== -->

# DNA registry — pick a visual language, not a preset

A **DNA** is a complete, art-directed visual language: typeface, palette logic, motion
grammar, and hero orchestration. It **parameterizes per scene** instead of shipping a
fixed look: the accent color is sampled from THIS scene, the contact shadow falls along
THIS scene's light, embed text blur matches THIS scene's depth-of-field, and the hero's
entrance amplitude follows how hard the word was actually spoken (RMS).

This replaces the template grab-bag. Six deep languages × scene adaptation beats 54
shallow presets — every render is already fitted to its footage.

## Category lock (deliveries field, enforced by the compilers)

Every classic DNA's **home is Cinematic (column)** — that is where all ten were
built and validated. (Standard/rail mode was retired 2026-06-12; the verbatim-rail
need is served by the `anchor` theme. The old rail combos are archived outside
this repo and are not distributed with the skill.)

## The ten

| DNA             | Register       | Scene fit                                       | Voice                                                                                                                                                                       |
| --------------- | -------------- | ----------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **cream**       | premium-warm   | dark / mid warm scenes (band luma < 150)        | Inter, warm cream, screen blend, glowing emergence hero. The poetic default.                                                                                                |
| **ink**         | premium        | **bright scenes (band luma > 150)**             | Inter, near-black, multiply blend — type reads as _printed on_ the wall. Fixes the bright-scene hole.                                                                       |
| **editorial**   | editorial-luxe | introspective / fashion / poetic, mid-dark      | Bodoni Moda, bone, _lowercase italic hero_ — magazine elegance over shout.                                                                                                  |
| **keynote**     | tech-premium   | product / launch / founder updates              | Inter 800, opaque white, line-wipe reveals, hero wipes UP. Stillness = confidence.                                                                                          |
| **documentary** | formal         | interviews, serious subject matter              | Inter, bone, **burn-in reveals**, no hero. Gravitas IS the style.                                                                                                           |
| **loud**        | loud           | hype / sport / music / social                   | Anton, scene-sampled accent hero, single-unit slam + caption-layer ripple; **body announces in front** (`bodyLayer: "fg"` — k-pop depth, deliberate).                       |
| **neon**        | loud-neon      | neon-noir / nightlife / tech-noir (dark scenes) | Orbitron + electric cyan; words flicker-ignite like tubes; the hero **powers ON** with a strobe and hums (glow 0.5).                                                        |
| **glitch**      | loud-neon      | digital / hacker / AI / dystopia                | Space Grotesk; **RGB-split echo layers converge** as each beat lands; 0.10–0.12s machine percussion; landing bumps co-visible captions 2px.                                 |
| **chrome**      | loud-luxe      | Y2K / fashion-tech / music                      | Audiowide cast in a **liquid-metal gradient** (background-clip:text on the word spans); one sheen sweep crosses the hero during the hold.                                   |
| **velocity**    | loud-sport     | sport / automotive / fitness                    | Teko italic; every word arrives **along its motion vector** (streak + skew settling upright); the hero passes through with blurred speed-trail echoes and looms while held. |

### fx fields (hero block) the engine understands

`entrance: emergence | settle | slam | rise | wipe-up | flicker-on | streak` ·
`glow` (0–0.5) · `echoes: [{dx,dy,color,opacity,blur}]` (converge-on-land duplicates) ·
`sheen: true` (gradient sweep — pair with `wordCss` background-clip) · `wordCss`
(per-word treatment; required for background-clip:text, which can't clip through
composited children) · `ripple` (px — landing bump, captions only) · `loom` / `breathe`
(hold-life) · `letterBlur` · `bodyLayer` (top-level: default layer for narration lines).

## How to pick (agent)

1. Read `safe-zones.json` → `heroAnchor.bandLuma` + `palette.temperature`.
2. Bright band (>150) → **ink** (never fight a bright scene with cream/screen).
3. Else pick by content register: poetic/warm → **cream** · introspective/luxe →
   **editorial** · product/tech → **keynote** · serious/interview → **documentary** ·
   hype/social → **loud**.
4. State the pick + why in one line; the user decides (GUIDE.md Step 0 still applies).

## Authoring

- Cinematic mode: `cinematic.json` → `"dna": "<name>"` (drop the `template` field).
- Locked per DNA: family, palette scheme, blend, motion curves, hero orchestration.
- Open per group (unchanged): size / weight / style / case / spacing + planes.
- `var(--accent)` is available in per-group CSS — it resolves to the scene-sampled accent.

## What the engine generates from the DNA (no authoring needed)

- **Hero three-act**: co-visible captions dim 0.35s before the hero lands (setup) →
  entrance with per-letter stagger, amplitude ∝ spoken loudness (impact) → slow breathe
  - glow until exit (afterglow).
- **Scene optics**: depth-match blur on embed captions, light-direction contact shadow.
- All deterministic — measured from files, no randomness.

## Climax selection — what earns the promotion

Pick the **payoff, not the topic**: the words you would quote when paraphrasing the
beat. "The stars were only limited by the pixel size" — the payoff is **pixel size**
(the surprising claim), not "stars" (the subject). Test: would the word alone, big on
screen, make the listener nod? A topic word makes them wait.

- **Phrases are legal** (`match: "pixel size"` / `"skin food"`): a peak is a semantic
  unit, not necessarily one token. 2–4 words max — beyond that it's a sentence, not a
  peak.
- **Prefer clause-final** — nothing left dangling to place after the lift.
- **Never strand a determiner**: lifting "stars" out of "The stars…" leaves an orphan
  "The" that vanishes mid-air. The compiler auto-absorbs a line-leading article into
  the promoted phrase; mid-line, match the phrase including its article.
- Sizes are TARGETED by the compiler, not just floored — author sizes are hints:
  - **apex = frame event**: under 88% of usable width → raised toward a 93% fill.
    Std height cap = `sizeRange[1] × 1.25` (≤46cqh; formal register ×1.0) — a std apex
    bursts a rail, not a body composition. Cinematic cap = `sizeRange[1]`.
  - **short words fill with TRACKING**: when the height cap binds before the width
    target (SHINE — 5 glyphs), the compiler letterspaces up to +0.32em until the word
    owns ~88% of the width (film-title craft: HER / DUNE). Long words fill by scale,
    short words by air — impact is WIDTH-led either way.
  - **minor = damped beat in the apex family**: `max(3× rail, 0.55× apex-final)`,
    width-capped. A peak that reads as a label is a bug.
  - **lockup context is RATIO-LOCKED**: kicker/tail = `0.26× hero` (clamped
    0.05–0.085·h), recomputed after any width-fit raise. Don't hand-tune context
    sizes — size the hero; the context follows like a poster system.

## Climax placement — the lockup is the default, NOT the only composition

A hero line takes `"placement": "subject" | "column"`:

- **subject** (default) — the **ORBIT lockup** centered ON the subject. NOT a centered
  sandwich: context anchors to the hero's EDGES like a poster kicker/tagline —
  pre-context flush-left off the hero's top-left corner, post-context flush-right off
  its bottom-right — so the small lines land BESIDE the head/shoulder (on the scene),
  never on the face, and therefore EMBED (bg) like everything else. The eye reads a
  diagonal: kicker ↘ HERO ↘ tail. Only the hero crosses the silhouette (the
  matte-occlusion showcase). The context's job is reading continuity — it gets the
  margins; the hero's job is the cinematic event — it gets the subject. Right when the
  peak is THE dramatic moment: cream / loud / glitch / neon / velocity lean here.
- **column** — the apex stays IN its column's reading flow and BURSTS it (oversized,
  full hero motion + dim/glow privileges, but composed within the sentence's home
  zone; spills toward the subject naturally when oversized). Right when the content
  is a continuous read and the column is the narrative's home: keynotes, tutorials,
  explainers, documentary. Registers: keynote / documentary / editorial lean here.

Applying ONE composition to every peak is monoculture — the same failure the motion
review caught. Pick per beat: a 15s explainer might run column peaks throughout and
save the subject lockup for the single apex. (A third pattern — the editorial split,
bg context upper + fg hero lower-third — lives in references/composition-craft.md and
is the next placement candidate.)

## The motion language (five layers, each DNA answers all five)

A DNA's animation is not a parameter tweak on a shared fade — it's a distinct physics:

| Layer                  | What it governs                                                                                                    | Where it lives                                        |
| ---------------------- | ------------------------------------------------------------------------------------------------------------------ | ----------------------------------------------------- |
| **word entrance**      | how each word materializes on its beat ({y,x,blur,scale,rot,dur,ease} or burn)                                     | `motion.soft/present/impact`                          |
| **line exit**          | direction + speed of leaving, optional top-to-bottom cascade                                                       | `motion.exit` ({dur,y,x,scale,ease,stagger})          |
| **hold-life**          | what text does while on screen — stillness is a deliberate choice                                                  | `hero.breathe` / `hero.loom` (0 = print-still)        |
| **hero orchestration** | the three-act entrance signature (emergence / settle / slam / rise / **wipe-up**) + glow / letterBlur / **ripple** | `hero.*`                                              |
| **timing physics**     | the duration & easing register everything obeys (percussive 0.15s ↔ atmospheric 0.6s)                              | implied by the values above — keep one family per DNA |

Shipped signatures: cream = _light condenses_ (blur-settle, drift-up exits) · ink =
_letterpress_ (scale-press, no float, dead-still) · editorial = _the pen glides_
(x-glide with the italic, cascade-out page turns) · keynote = _surgical reveal_
(burn words + line wipe + hero wipe-up, exits never move) · documentary = _burn and
hold_ (motion's absence IS the language) · loud = _percussion_ (back-eased punches,
alternating tilt, hero ripple that bumps every caption — never the footage).

Rules inherited from hyperframes motion-principles: exits faster than entrances; vary
ease families BETWEEN DNAs (not within one); `.out` enters, `.in` leaves; never two
transform tweens on one element in the same window (wipe-up is clip-path so the
afterglow scale channel stays free; loom subsumes breathe).

## Adding a DNA

Copy an existing `dna/<name>.json`, change the voice, keep the schema. The engine
(`modes/cinematic/engine.html`) and both compilers consume it as-is. A DNA earns its
place by being a _distinct voice with a reason to exist_ — not a recolor.


<!-- ===== FILE: hyperframes/embedded-captions/modes/cinematic/README.md ===== -->

# Cinematic mode (pure embed) — one engine, six DNAs

> Cinematic mode compiles **[../../dna/](../../dna/README.md)** through
> **[engine.html](engine.html)** (`make-composition.cjs`). The old per-template HTML
> shells are retired — `cinematic-cream` maps to `dna: "cream"` automatically; the other
> archived templates (memory-wall / champion / portrait-header, in [\_archive/](_archive/))
> remain as design references only.

Use this mode for pure-embed asks (no rail): brand film, hype, social reel, showcase.
The **DNA** locks the visual language (type, palette scheme, blend, motion grammar, hero
three-act); **safe-zones v2** parameterizes it to the scene (sampled accent, light-
direction contact shadow, depth-match blur); **the agent decides layout only** (planes,
blocks, per-line typography within the DNA).

## Workflow

1. `bash scripts/prepare.sh <project>` → matte ∥ transcript ∥ envelope → safe-zones v2
2. Pick a DNA ([../../dna/README.md](../../dna/README.md)): bright hero band → `ink`,
   else by register (cream / editorial / keynote / documentary / loud). Recommend, let
   the user pick.
3. Author `<project>/cinematic.json` — `"dna": "<name>"` + thought-blocks (schema:
   `scripts/make-cinematic.cjs` header)
4. `node scripts/make-cinematic.cjs <project>` → plan.json → engine-compiled index.html
5. `node scripts/preview-frames.cjs <project>` → § Visual QA (failure checks + the 5
   positive checks in [../../references/reference-bar.md](../../references/reference-bar.md))
6. `bash scripts/render-and-composite.sh <project>` → gates → final.mp4

## What the engine generates (never author these)

- word timings from the transcript; accumulate-within-block / page-flip-between-blocks
- the hero hand-off + **three-act orchestration** (dim → RMS-coupled per-letter entrance
  → breathe + glow), per the DNA's `hero` block
- scene tokens: `--accent` (sampled), contact shadow, depth blur
- reading order, re-slot from measured heights, hero size/collision post-pass

## What you DON'T do

- Override `.cap` color / blend / shadow / filter / motion curves — that's the DNA.
  Scene fights the look → pick a different DNA (bright → `ink`), never recolor.
- Hand-position the hero into a clean margin (it belongs ON the subject, ~30–55%
  occluded — safe-zones `heroBands.best`).
- Add full-frame grades/textures over the footage (hard rule: the video ships untouched).

## Adding a DNA

`dna/<name>.json` — copy one, change the voice (see [../../dna/README.md](../../dna/README.md)
§ Adding). The engine consumes it with no code change. A DNA must be a distinct voice
with a reason to exist, not a recolor.


<!-- ===== FILE: hyperframes/embedded-captions/modes/cinematic/_archive/champion/spec.md ===== -->

# Template: champion

**Look:** podcast / interview, upper-side column with intro→phrase→emph
beats building toward a center-stage CROWN that crosses the subject's body.
"Wimbledon Champion" energy.

**Visual identity (LOCKED):**

- 5 typography slots: intro / phrase / emph / dream / crown
- `mix-blend-mode: screen` over warm bone color (#fff5df)
- Deep text-shadow + brightness boost
- Single-caption-swap layout (caps stack at one point in the column)
- Center-stage crown crosses the subject for cinematic occlusion

## When to apply

✅ **Good fit:**

- Podcast / interview style with a single seated subject
- Cluttered backdrop (bookshelf, props, dark) — screen blend reads through
- Subject roughly centered with clear clean zones on one or both sides
- Speech has a clear payoff line that can become a "crown" (1-3 short words)
- 16:9 landscape, 1920×1080 ideal

❌ **Wrong fit:**

- Bright/sky/window backdrop (screen blend washes out)
- Subject heavily off-center such that there's no clean column zone
- Speech has no clear climax line
- Portrait 9:16 → use `portrait-header` template instead

## Layout decisions agent makes

| Field                         | What                                                                                                                                        | Example (1920×1080)                            |
| ----------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------- | ---------------------------------------------- |
| `plane.top/left/width/height` | Where the side column sits. Pick the side opposite the subject's gaze (looking room) and hug the cleanest backdrop zone.                    | `{top: 40, left: 40, width: 720, height: 420}` |
| `plane.rotateY`               | Slight perspective into the wall. Positive for left column (recedes right), negative for right column. Keep small (3-7°).                   | `4`                                            |
| `crown_top`                   | Y position of the crown. Should fall on the subject's chest/neck so the body occludes the middle letters.                                   | `420`                                          |
| `font_scale`                  | Multiplier on locked sizes.                                                                                                                 | `1.0` for 1920×1080                            |
| `crown_enabled`               | Whether to render a crown. Skip if the speech has no clean payoff line, or if the subject is too far off-center for a center crown to land. | `true`                                         |

### Crown placement rules

Before enabling the crown, verify all 3 conditions:

1. Subject body center within ±10% of frame horizontal center
2. Clean zones ≥15% of frame width on each side of subject
3. Crown text width (uppercase 140px × ~chars) > subject body width + 400px

If any fails: disable the crown OR use a smaller font + place it in the
larger clean zone instead of center. See `references/layout-heuristics.md`.

## Slot assignment

| Slot   | Use for                                                    |
| ------ | ---------------------------------------------------------- |
| intro  | Filler / discourse markers ("you know,", "for me,", "so…") |
| phrase | Main statement clauses                                     |
| emph   | Key achievement / superlative line                         |
| dream  | Aspirational lines, past-tense reflection                  |
| crown  | The single climax line — center-stage payoff               |

Aim for ≤3 slots per video (excluding crown). Don't use all 4 in a 12s clip.

## Plan.json shape

```json
{
  "mode": "template",
  "template": "champion",
  "duration": 12.08, "fps": 24, "width": 1920, "height": 1080,
  "plane": {
    "top": 40, "left": 40, "width": 720, "height": 420,
    "rotateY": 4
  },
  "crown_top": 420,
  "font_scale": 1.0,
  "groups": [
    { "id": "cg-0", "slot": "intro", "tone": "soft",
      "in": 0.10, "out": 1.45, "words": [...] },
    { "id": "cg-1", "slot": "phrase", "tone": "soft",
      "in": 1.55, "out": 4.20, "words": [...] },
    { "id": "cg-2", "slot": "emph", "tone": "present",
      "in": 6.50, "out": 8.30, "words": [...] }
  ],
  "crown_group": {
    "id": "cg-crown", "tone": "present",
    "in": 10.85, "out": 12.08,
    "words": [
      {"text": "Wimbledon", "start": 10.94, "end": 11.28},
      {"text": "Champion",  "start": 11.38, "end": 11.84}
    ]
  }
}
```

`crown_group` always uses the crown slot — no need to specify `slot`.
Set `crown_group: null` to disable.


<!-- ===== FILE: hyperframes/embedded-captions/modes/cinematic/_archive/memory-wall/spec.md ===== -->

# Template: memory-wall

**Look:** introspective monologue, italic poem stacking on a back wall,
right-aligned cascade for the climax. Sam Harris / Pico Iyer territory.

**Visual identity (LOCKED — do not change):**

- 4-slot typography arc: italic 600 → italic 500 hanging-indent → upright
  700 pivot → uppercase 900 climax
- `mix-blend-mode: screen` over warm-bone color (#fff4dc)
- soft text-shadow + brightness boost
- Per-word fade with subtle Y-drift (soft tone) or pop+scale (present tone)

## When to apply

✅ **Good fit:**

- Talking-head with a flat back wall (acoustic foam, plain plaster, soft
  bookshelf) on one side
- Single subject, fixed or near-fixed camera
- Voice-over feel: introspective, narrative, "I was thinking…"
- Mid-tone or dark backdrop (luminance < 180)

❌ **Wrong fit:**

- Bright window/sky backdrop → screen blend blows out
- Cluttered backdrop with text/graphics → conflicts with caption text
- Energetic / vlog / TikTok style → wrong vibe
- Multiple speakers / hard cuts → caption arc breaks

## What agent decides per scene

| Field                          | What                                                                                                               | Example                                                            |
| ------------------------------ | ------------------------------------------------------------------------------------------------------------------ | ------------------------------------------------------------------ |
| `plane.top/right/width/height` | Where the wall plane sits in frame. Plane should HUG the side of the wall, not float over the subject.             | `{top: 90, right: 30, width: 720, height: 520}` for 1280×720       |
| `plane.rotateY`                | Match the wall's perspective angle. Negative for right-side wall (text recedes left), positive for left-side wall. | `-13` for a right-side wall at slight angle                        |
| `plane.rotateX`                | Tiny vertical tilt if wall is angled up/down. Usually 0-2 deg.                                                     | `1`                                                                |
| `font_scale`                   | Multiplier on the locked cap-N base sizes. Tune for frame height.                                                  | `1.0` for 1280×720, `~1.5` for 1920×1080, `~0.7` for 720p portrait |
| `groups[].slot`                | Which of the 4 typography slots this group uses (1/2/3/4). Drives the arc.                                         | See below                                                          |
| `groups[].tone`                | "soft" or "present" — drives motion curve                                                                          | `"soft"` for opening lines, `"present"` for pivot+climax           |

## Slot assignment rules

Aim for ONE arc across the video: `1 → 2 → 3 → 4`. Don't repeat slots if you
can avoid it; don't skip slots without reason.

| Slot | Use for                                                                                                                                  |
| ---- | ---------------------------------------------------------------------------------------------------------------------------------------- |
| 1    | The opener. The "I was thinking" line. Italic, soft entry.                                                                               |
| 2    | The dreamy continuation / modifier. Smaller italic, hanging-indent — feels like the second half of a sentence with some staggered drift. |
| 3    | The pivot. Upright (no italic), the syntactic turn. ("but suddenly", "and then…")                                                        |
| 4    | The climax. Big uppercase 900. The payoff line. Aim for ≤4 short words so the right-aligned cascade naturally wraps to 2-3 lines.        |

If the script is longer than 4 groups, repeat slot 1 or 2 for additional
soft lines, but reserve slot 4 for the SINGLE climax.

## Plan.json shape

```json
{
  "mode": "template",
  "template": "memory-wall",
  "duration": 8.04,
  "fps": 24,
  "width": 1280,
  "height": 720,
  "plane": {
    "top": 90,
    "right": 30,
    "width": 720,
    "height": 520,
    "rotateY": -13,
    "rotateX": 1
  },
  "font_scale": 1.0,
  "groups": [
    {
      "id": "cg-0",
      "slot": 1,
      "tone": "soft",
      "in": 0.2,
      "out": 4.85,
      "words": [
        { "text": "Some", "start": 0.24, "end": 0.44 },
        { "text": "memories", "start": 0.48, "end": 0.82 },
        { "text": "feel", "start": 0.92, "end": 1.14 },
        { "text": "soft", "start": 1.2, "end": 1.64 }
      ]
    },
    {
      "id": "cg-1",
      "slot": 2,
      "tone": "soft",
      "in": 2.55,
      "out": 4.85,
      "words": [
        { "text": "like", "start": 2.66, "end": 2.78 },
        { "text": "old", "start": 2.86, "end": 3.02 },
        { "text": "film", "start": 3.16, "end": 3.46 }
      ]
    },
    {
      "id": "cg-2",
      "slot": 3,
      "tone": "present",
      "in": 4.9,
      "out": 8.04,
      "words": [
        { "text": "but", "start": 5.04, "end": 5.18 },
        { "text": "suddenly", "start": 5.24, "end": 5.76 }
      ]
    },
    {
      "id": "cg-3",
      "slot": 4,
      "tone": "present",
      "in": 6.7,
      "out": 8.04,
      "words": [
        { "text": "everything", "start": 6.82, "end": 7.14 },
        { "text": "is", "start": 7.18, "end": 7.28 },
        { "text": "sharp", "start": 7.32, "end": 7.52 },
        { "text": "again", "start": 7.58, "end": 7.92 }
      ]
    }
  ]
}
```

## Don't fight the template

If the user wants different typography, different blend, or different motion:
**use Standard mode** (`../../../standard/`). Don't try to override the locked CSS — the
template's visual consistency is the whole point.


<!-- ===== FILE: hyperframes/embedded-captions/modes/cinematic/_archive/portrait-header/spec.md ===== -->

# Template: portrait-header

**Look:** 9:16 portrait talking-head with captions on a horizontal strip
across the top of the frame, above the subject's head. Optional crown at
the bottom for shots that include the subject's waist or below.

**Visual identity (LOCKED):**

- 5 typography slots: intro / phrase / emph / dream / crown (centered)
- `mix-blend-mode: screen` over warm bone color (#fff5df)
- Single-caption swap (caps stack at one position in the header strip)
- Per-word fade with subtle Y-drift (soft) or pop+scale (present)

## When to apply

✅ **Good fit:**

- 9:16 portrait video (1080×1920 typical)
- Single subject filling the center of the frame
- Clean band visible above the head
- Speech is relatively dense (many short phrases) — crown only for the
  one true climax

❌ **Wrong fit:**

- Subject's head crops to the very top of frame (no header band exists)
- 16:9 landscape → use `champion` or `memory-wall` instead
- Multiple speakers / cuts

## Layout decisions

| Field           | What                                                                                                                    | Example (1080×1920)                  |
| --------------- | ----------------------------------------------------------------------------------------------------------------------- | ------------------------------------ |
| `header.top`    | Y of the header strip. Should sit above the subject's head with ~30px breathing room.                                   | `30` if hair top is around y=200     |
| `header.height` | Height of the strip. Bigger for longer captions / 2-line wraps.                                                         | `280`                                |
| `crown_top`     | Y of the crown line (bottom of frame). Skip if no waist visible.                                                        | `1620` for a near-full-body shot     |
| `crown_enabled` | Whether to render a bottom crown. Skip if subject body fills the lower half completely (matte will block crown anyway). | `false` for tight head-and-shoulders |
| `font_scale`    | Scale multiplier on locked sizes.                                                                                       | `1.0` for 1080×1920                  |

## Slot assignment

Same arc as champion: intro / phrase / emph / dream / crown.

For portrait-header specifically, header band is narrow (one strip), so:

- Most groups fit on 1-2 lines
- Don't use crown if it'd be hidden by the body matte (Pausch-style portraits
  often need to skip crown entirely and promote the climax to `emph` in the
  header instead)

## Plan.json shape

```json
{
  "mode": "template",
  "template": "portrait-header",
  "duration": 25.3, "fps": 24, "width": 1080, "height": 1920,
  "header": { "top": 30, "height": 280 },
  "crown_top": 1620,
  "font_scale": 1.0,
  "groups": [
    { "id": "cg-0", "slot": "intro", "tone": "soft",
      "in": 0.10, "out": 3.20, "words": [...] },
    { "id": "cg-1", "slot": "phrase", "tone": "soft",
      "in": 3.55, "out": 5.80, "words": [...] },
    { "id": "cg-2", "slot": "emph", "tone": "present",
      "in": 17.85, "out": 22.10,
      "words": [
        {"text": "Time", "start": 17.94, "end": 18.26},
        {"text": "is",   "start": 18.38, "end": 18.54},
        {"text": "all",  "start": 18.66, "end": 18.80},
        {"text": "we",   "start": 18.92, "end": 19.02},
        {"text": "have", "start": 19.12, "end": 19.38}
      ]}
  ],
  "crown_group": null
}
```

Set `crown_group: null` if you've checked that a crown would be blocked by
the subject body or the shot composition.


<!-- ===== FILE: hyperframes/embedded-captions/modes/cinematic/cinematic-cream/spec.md ===== -->

# cinematic-cream — spec

The authoritative spec lives in [template.html](template.html)'s header comment (DNA-only:
what's LOCKED vs OPEN, the LAYOUT/planes contract, READING ORDER + hand-off, hero sizing).
Read that header before authoring plan.json. Quick contract:

- LOCKED: Inter, soft/present motion, warm-cream palette, screen blend, shadow logic.
- OPEN per group (css field): size/weight/style/transform/spacing + position WITHIN a plane.
- LAYOUT: run scripts/safe-zones.cjs first. Narration planes HUG the silhouette — use
  zones.hugLeft/hugRight (2-6% gap from the subject's edge); a plane parked in the far
  corner reads as disconnected floating text, not an embed. The ONE hero stays BIG
  (~0.22-0.34·h) centered ON the subject (heroAnchor / heroBands.best), target ~30-55%
  occlusion. fg is the LAST resort: only when heroBands.feasible=false (no band ≤62%).
  hero BIG (~0.22-0.34·h) centered ON the subject (heroAnchor), target ~30-55% occlusion.
- plan.json: groups[] with per-word transcript timings (use scripts/fill-timings.cjs),
  fit via scripts/fit-fonts.cjs, compile via scripts/make-composition.cjs.


<!-- ===== FILE: hyperframes/embedded-captions/modes/standard/_anatomy.md ===== -->

---
name: caption-template-anatomy
description: The shared, reproducible scene engine every caption template is built on — a matted talking-head with a flowing verbatim foreground caption and a single climax word, driven by one paused GSAP timeline. Read it ONCE per session (it is identical for all 54 templates); each per-template file in templates/ only overrides the style tokens + the named climax entrance/exit.
metadata:
  tags: caption, talking-head, matte, occlusion, verbatim, climax, gsap, hyperframes
---

# Caption Template — Anatomy (the shared engine)

A **caption template** = one complete, reproducible HyperFrames scene:

> **the person (always in frame)** + a **flowing foreground caption** (verbatim, word-by-word, with appear **and** disappear) + a **climax word** (big, behind the speaker, with a designed entrance **and** exit) + a coherent **font / colour / motion** design.

Every file in `templates/` is the SAME engine described here with three things swapped: (1) the **style tokens** (font, fills, accent, optional gradient/stroke), (2) the named **climax entrance** + **exit** (see `_motion.md`), (3) the **copy** (flow lines + climax word) and **scene/person**. So read this once; each template file is short.

HyperFrames-native, so anyone can reproduce it:

- **One paused GSAP timeline per composition**, registered to `window.__timelines[data-composition-id]`.
- All timing in **seconds**; `data-start` / `data-duration` carry the scene window.
- **Deterministic + seek-safe** only — no `Math.random()`, no `Date.now()`, no `repeat: -1` without a finite root `data-duration`, no un-seekable CSS animations. Every state is reachable by seeking the timeline to a time `t`.
- GSAP transform aliases (`x`, `y`, `scale`, `rotation`); animate `opacity`, `filter`, `clipPath`, `textShadow`, `backgroundPosition`, `letterSpacing` — never layout props (width/top/left/margin).

For the composition contract see `hyperframes-core`; eases + the animated-property allowlist see `hyperframes-gsap`; caption grouping/positioning/exit guarantees see `hyperframes-captions`.

## 1 · Asset prep (two CLI calls)

```bash
# 1) The person — transparent talking-head cutout over the scene (VP9 + alpha)
bash scripts/prepare.sh   <project>      # matte ∥ transcribe ∥ safe-zones (THIS skill — not remove-background)
#    (a still works too:  remove-background portrait.jpg -o person.png)

# 2) The verbatim word timings that drive the flowing caption
npx hyperframes transcribe subject.mp4 --model small            # → transcript.json
#    shape: [{ "id":"w0","text":"Hello","start":0.0,"end":0.5 }, …]
```

The flow caption consumes that `transcript.json` directly (word `start`/`end` → reveal + active-word emphasis). The climax word is authored by hand (it is the headline beat, not part of the spoken transcript). In production the avatar/matte pipeline yields a pixel-perfect alpha for free — `remove-background` is the fallback for arbitrary footage.

## 2 · The matte sandwich (HTML)

Six layers, back-to-front. The person is layered ON TOP of the climax so they physically **occlude** it — this is what sells "behind the speaker" (blur/opacity alone reads as a flat overlay).

```html
<div
  class="stage {STYLE} {PERSON}"
  id="cap-{id}"
  data-composition-id="cap-{id}"
  data-start="0"
  data-duration="{SCENE_DUR}"
  data-track-index="0"
>
  <!-- z0  background plate (the original frame, full) -->
  <!--     supplied by .{PERSON} as background-image, or a <video> at z-index:0 -->

  <!-- z1  CLIMAX — big, BEHIND the person, occluded -->
  <div class="climax"><span>{CLIMAX_WORD}</span></div>

  <!-- z4  the person cutout (transparent webm/png), aligned to the plate -->
  <video class="cut" src="person.webm" muted playsinline></video>
  <!-- or:  <img class="cut" src="person.png"> -->

  <!-- z5  grade / vignette for depth + legibility -->
  <div class="grade"></div>

  <!-- z6  FLOW — the verbatim caption, IN FRONT, lower third -->
  <div class="flow"></div>
  <!-- words injected from transcript.json -->
</div>
```

## 3 · Base CSS (layout · z-order · sizing)

Caption size is in **`cqh`** (% of frame height) via a size container, so it honours broadcast spec at any resolution (~8% cap-height for a 16:9 word). The per-template file only sets the `--ff` / `--cfill` / `--cacc` tokens and any `.climax span` fill (gradient/stroke).

```css
.stage {
  position: relative;
  aspect-ratio: 16/9;
  overflow: hidden;
  container-type: size;
  background-size: cover;
  background-position: center 12%;
  background-color: #0a0a0e;
  font-family: var(--ff);
}
.stage > * {
  position: absolute;
}
.cut {
  z-index: 4;
  inset: 0;
  width: 100%;
  height: 100%;
  object-fit: cover;
  object-position: center 12%;
  pointer-events: none;
}
.grade {
  z-index: 5;
  inset: 0;
  pointer-events: none;
  background: radial-gradient(130% 100% at 50% 26%, transparent 40%, rgba(0, 0, 0, 0.6));
}

/* CLIMAX — big, behind person (z1), occluded. line-height ≥1.15 so clip-reveal
   entrances (inset(0)) never slice glyph tops; pad clips negative for script faces. */
.climax {
  z-index: 1;
  left: 50%;
  top: 37%;
  transform: translate(-50%, -50%);
  white-space: nowrap;
  text-align: center;
  line-height: 1.18;
  font-family: var(--ff);
  color: var(--cfill);
  font-weight: 900;
  font-size: 44cqh;
  text-transform: uppercase;
  text-shadow:
    0 2px 13px rgba(0, 0, 0, 0.6),
    0 0 48px rgba(0, 0, 0, 0.42);
}
.climax span {
  display: inline-block;
  opacity: 0;
} /* GSAP reveals it */

/* FLOW — verbatim caption, in front (z6), lower third */
.flow {
  z-index: 6;
  left: 50%;
  bottom: 9%;
  transform: translateX(-50%);
  width: 90%;
  text-align: center;
  line-height: 1.15;
  font-family: var(--ff);
  font-weight: 700;
  font-size: 7.5cqh;
  color: var(--cfill);
}
.flow .w {
  display: inline-block;
  opacity: 0;
  margin: 0 0.1em;
  color: var(--cfill);
}
.flow .w.act {
  color: var(--cacc);
} /* the currently-spoken word */

/* tokens every template overrides: */
.stage {
  --ff: "Inter";
  --cfill: #fff;
  --cacc: #10a37f;
}
```

**Legibility on busy/bright scenes:** a behind-the-person climax needs separation from the footage, not just a fill colour. For dark or gradient fills on lit scenes give the climax an outline — `-webkit-text-stroke:1px rgba(0,0,0,.5);paint-order:stroke fill` — a dark drop-shadow alone fails against highlights (e.g. a lamp). Gradient/clip fills must live on `.climax span` (the text node), never on the transformed `.climax` container, or the clip detaches and only the shadow shows.

## 4 · One paused GSAP timeline (the loop, made seek-safe)

The gallery used a `setInterval` loop; HyperFrames needs the same beats as **absolute-time tweens on one paused timeline**. The cycle is **FLOW line → (FLOW line) → CLIMAX in → hold → out**. Restraint is the rule: flow stays clean; the one big mood move happens only at the climax.

```html
<script src="https://cdn.jsdelivr.net/npm/gsap@3.14.2/dist/gsap.min.js"></script>
<script>
  window.__timelines = window.__timelines || {};
  const stage = document.getElementById("cap-{id}");
  const flow = stage.querySelector(".flow");
  const climax = stage.querySelector(".climax span");
  const tl = gsap.timeline({ paused: true });

  // --- FLOW: render words from transcript.json, reveal each at its start time ---
  // WORDS = grouped transcript lines: [{ words:[{text,start,end}], end }] in scene-local seconds.
  function renderLine(line) {
    flow.innerHTML = line.words
      .map((w, i) => `<span class="w" data-i="${i}">${w.text}</span>`)
      .join(" ");
    return [...flow.querySelectorAll(".w")];
  }
  WORDS.forEach((line) => {
    const spans = renderLine(line); // (one renderLine per active line; see captions skill for multi-line groups)
    spans.forEach((el, i) => {
      const w = line.words[i];
      tl.add(FLOW_IN(el), w.start); // FLOW_IN  = the template's flow entrance (see _motion.md)
      tl.set(spans, { className: "w" }, w.start); // active-word sweep: only the spoken word gets .act
      tl.set(el, { className: "w act" }, w.start);
    });
    tl.add(FLOW_OUT(spans), line.end); // FLOW_OUT = flow exit
    tl.set(flow, { autoAlpha: 0 }, line.end + FOUT); // hard-hide the group so old text can't linger
    tl.set(flow, { autoAlpha: 1 }, line.end + FOUT + 0.001);
  });

  // --- CLIMAX: entrance at the beat → hold ≥1s → exit (named recipes from _motion.md) ---
  const T = CLIMAX_AT; // beat time (after the flow lines)
  tl.add(CLIMAX_IN(climax), T); // e.g. SLAM / DEBLUR / INK-LOOM / CHROME-SWEEP …
  tl.add(CLIMAX_OUT(climax), T + CLIMAX_HOLD); // hold ≥1s, then exit. CLIMAX_OUT ends opacity:0 (hard exit)

  window.__timelines["cap-{id}"] = tl;
</script>
```

`FLOW_IN` / `FLOW_OUT` / `CLIMAX_IN` / `CLIMAX_OUT` are the named recipes in **`_motion.md`** — each returns a GSAP tween/timeline so the per-template file just picks four names. A simpler equivalent for the flow active-word _glow_ (rather than discrete reveal) is the single-driver envelope in `hyperframes-animation/rules/asr-keyword-glow.md`.

## 5 · How to choose values

- **SCENE_DUR** — must equal `data-duration`. Typical 6–10 s for a looping demo card.
- **WORDS grouping** — 2–4 words / line, ~380–520 ms per word (premium pacing is slower than Hormozi). Group from `transcript.json`; keep `end < next.start` (monotonic).
- **CLIMAX_AT** — place the climax _after_ the flow lines clear, on the narration's emphasis beat.
- **CLIMAX_HOLD** — **≥1 s** of settled dwell _after_ the entrance finishes (the climax is the headline beat). Entrances run 0.6–1.6 s, so e.g. hold = entranceDur + 1.0–1.6.
- **FOUT** — flow exit ≈ 0.5 s. **Exit ≈ 75 % of entry** for every element (arrival deliberate, departure swift; see `_motion.md`).
- **Climax size** — base 44 cqh; long words bleed off-frame (intended cinematic); 3-char words behind a centred subject need size + an outline so they peek.

## Critical constraints (HyperFrames)

- Timeline **paused**; registry key = `data-composition-id`.
- **No CSS keyframe animation** on caption elements — all motion is GSAP tweens at absolute times (seek-safe).
- No `Math.random` / `Date.now` / `repeat: -1` without a finite root `data-duration`.
- `display:inline-block` on every `.w` and the climax `span`.
- **Hard-hide** each flow group at its end time; **CLIMAX_OUT ends at `opacity:0`** (or fully-clipped) so nothing lingers.
- Gradient / `background-clip:text` / stroke fills go on `.climax span`, not the transformed `.climax`.
- `.climax` `line-height ≥ 1.15`; pad clip-reveal entrances with negative insets for script/decorative fonts.

## Pairs with HF skills

- `media-use` — `remove-background` (the matte) + `transcribe` (word timings).
- `hyperframes-captions` — transcript consumption, grouping, positioning, exit guarantees, `fitTextFontSize`.
- `hyperframes-animation/rules/asr-keyword-glow.md` — the verbatim active-word envelope.
- `hyperframes-gsap` — single paused timeline, transform aliases, ease palette.
- `_motion.md` (this folder) — the named flow/climax entrance + exit recipes.


<!-- ===== FILE: hyperframes/embedded-captions/modes/standard/_motion.md ===== -->

---
name: caption-template-motion
description: The named flow + climax entrance/exit recipes (GSAP, seek-safe) that the per-template files reference, plus the motion numerics (ease palette, exit=75% entry, climax dwell, restraint, mood→motion). Every template picks a FLOW_IN/OUT and a CLIMAX_IN/OUT from here — look up only the 2-3 recipes a template names (grep the `### name`), this is a catalog, not a read-through.
metadata:
  tags: gsap, easing, entrance, exit, timing, restraint, mood-matching, captions
---

# Caption Template — Motion Language

`_anatomy.md` wires four hooks onto one paused timeline: `FLOW_IN`, `FLOW_OUT`, `CLIMAX_IN`, `CLIMAX_OUT`. This file is the catalog each template picks from. Each recipe is a GSAP tween on the climax `span` (or a flow `.w`); placed at an absolute time it is fully **seek-safe**. Multi-stage looks use GSAP `keyframes:{}` (still seek-safe) — never CSS keyframes.

## Numerics (shared)

**Ease palette** (sanctioned — reads clean on video, stays distinct):

| Curve           | GSAP                                    | Use                                                 |
| --------------- | --------------------------------------- | --------------------------------------------------- |
| overshoot entry | `back.out(1.4–1.7)`                     | confident arrivals (premium/epic/creator)           |
| heavy/refined   | `power3.out`                            | hero/secondary entrances, slides                    |
| general         | `power2.out`                            | fades, scales                                       |
| exit accel      | `power2.in`                             | the _exit_ side of any move (departure accelerates) |
| snappy          | `expo.out`                              | warp/fly/sonic confident snaps                      |
| breathing       | `sine.inOut`                            | gentle wellness drift                               |
| impact thud     | `back.out(1.5–2)` or a quick `expo.out` | slam/stomp/stamp landings                           |
| linear driver   | `none`                                  | the asr active-word envelope driver only            |
| digital stutter | `steps(n)`                              | glitch/vhs/blink/possess/cut                        |

**Forbidden:** `bounce.out`, `elastic.out` everywhere **except** the Playful cluster (explicit playfulness — KIDS drop-bounce, CANDY jelly). Elsewhere real objects decelerate; they don't bounce. Use low `back.out` for sanctioned overshoot.

**Durations** — flow word enter 0.30–0.50 s · climax entrance 0.6–1.6 s · **exit ≈ 75 % of entry** (arrival deliberate, departure swift) · stagger 50–150 ms / word.

**Restraint (the rule that makes it premium):** the FLOW stays clean — a tasteful reveal + the active-word accent, no effects. The big mood move + any scene effect (flash, shockwave, shake) happens **only at the CLIMAX**, then clears. Never sprinkle effects across the flow.

**Climax dwell ≥ 1 s** after the entrance finishes — the climax is the headline beat.

**Mood → motion** (pick an entrance whose physics match the theme):

| Mood                            | Entrances                                            |
| ------------------------------- | ---------------------------------------------------- |
| premium                         | deblur · rise · expose · breathe · flip              |
| epic                            | slam · monument · fly · grandrise                    |
| cyber                           | glitch · type · scan · boot                          |
| horror                          | loom · possess · glimpse · seep (never bouncy/clean) |
| luxury                          | tracking-expand · hairrise                           |
| retro                           | vhs · stamp · blink · type                           |
| neon                            | ignite · buzz                                        |
| hype                            | stomp · punch · slap                                 |
| playful                         | jelly · dropb · scrawl · popr                        |
| creator                         | boxpop · slideup · flip · shimmer                    |
| ultra (flash in the type)       | volt · hyper · liquid · prism · shatter · extrude    |
| atelier (design)                | editwipe · rise · block · vert · ink · weight        |
| impact (scene effect at climax) | nuke · meteor · sonic · seismic · judge              |

---

## FLOW entrances / exits (per word `.w`)

The flow caption reveals word-by-word from the transcript. The active word gets `.act` (→ `--cacc`). Exit hard-hides the group.

- **fade-up** (premium/atelier default) — `fromTo(w,{opacity:0,y:14},{opacity:1,y:0,duration:.42,ease:'power3.out'})`
- **pop** (epic/hype) — `fromTo(w,{opacity:0,scale:.5},{opacity:1,scale:1,duration:.34,ease:'back.out(1.6)'})`
- **whip** (kinetic) — `fromTo(w,{opacity:0,x:-30,filter:'blur(10px)'},{opacity:1,x:0,filter:'blur(0)',duration:.32,ease:'expo.out'})`
- **glitch** (cyber) — `fromTo(w,{opacity:0,clipPath:'inset(45% 0 45% 0)'},{opacity:1,clipPath:'inset(0)',duration:.4,ease:'steps(6)'})`
- **type** (terminal/retro) — `fromTo(w,{opacity:0},{opacity:1,duration:.2,ease:'steps(3)'})` staggered as the cadence
- **blur-in** (horror) — `fromTo(w,{opacity:0,filter:'blur(10px)',y:'.1em'},{opacity:1,filter:'blur(0)',y:0,duration:.6,ease:'power2.out'})`
- **karaoke** (creator) — words start visible-dim; on `w.start` `set(w,{className:'w act'})` (active → `--cacc`), prior word back to spoken. The signature verbatim mechanic.
- **flow exits** — fade-up-out `to{opacity:0,y:-10}` · horror smear `to{opacity:0,x:6,skewX:10,filter:'blur(5px)'}` · all ≈0.4–0.55 s.

---

## CLIMAX entrances

Each is a `gsap.fromTo(span, {from}, {to, duration, ease})`. Where a `keyframes:{}` is shown, pass it as the 2nd arg's `keyframes`.

### premium

- **deblur** — `{opacity:0,scale:.96,filter:'blur(8px)'}→{opacity:1,scale:1,filter:'blur(0)',duration:.8,ease:'power3.out'}`
- **rise** — `{opacity:0,yPercent:48}→{opacity:1,yPercent:0,duration:.9,ease:'power3.out'}`
- **expose** — `{opacity:0,filter:'brightness(3.2) blur(5px)',scale:1.05}→{opacity:1,filter:'brightness(1) blur(0)',scale:1,duration:1,ease:'power2.out'}`
- **breathe** — `{opacity:0,scale:1.09,filter:'blur(8px)'}→{opacity:1,scale:1,filter:'blur(0)',duration:1.2,ease:'sine.out'}`
- **flip** — `{opacity:0,rotationX:93,transformPerspective:720}→{opacity:1,rotationX:0,duration:.9,ease:'power3.out'}`

### epic

- **slam** — `{opacity:0,scale:1.6,filter:'blur(12px)'}→{opacity:1,scale:1,filter:'blur(0)',duration:.7,ease:'back.out(1.6)'}` (lands with a thud; overshoot ~1.03 mid)
- **monument** — `{opacity:0,scale:1.42,letterSpacing:'.12em'}→{opacity:1,scale:1,letterSpacing:'0',duration:1.3,ease:'power3.out'}`
- **fly** — `{opacity:0,scale:.3,filter:'blur(14px)'}→{opacity:1,scale:1,filter:'blur(0)',duration:.8,ease:'expo.out'}`
- **grandrise** — `{opacity:0,yPercent:66,scale:1.05}→{opacity:1,yPercent:0,scale:1,duration:1.15,ease:'power3.out'}`

### cyber

- **glitch** — `{opacity:0}→{opacity:1,duration:.6,ease:'steps(8)',keyframes:{clipPath:['inset(40% 0 40% 0)','inset(0)','inset(60% 0 10% 0)','inset(0)'],x:[-8,5,-2,0],textShadow:['4px 0 #ff003c,-4px 0 #00ffd1','none']}}`
- **type** — `{opacity:1,clipPath:'inset(0 100% 0 0)'}→{clipPath:'inset(0 0 0 0)',duration:.85,ease:'steps(13)'}` (typewriter L→R)
- **scan** — `{opacity:0,scaleY:.02,filter:'brightness(2.4)'}→{opacity:1,scaleY:1,filter:'brightness(1)',duration:.75,ease:'power3.out'}`
- **boot** — `{opacity:0,scaleY:.1}→{opacity:1,scaleY:1,duration:1,ease:'steps(1)',keyframes:{opacity:[0,.6,.1,.85,.2,1]}}` (hologram power-up flicker)

### horror (never bouncy, never clean)

- **loom** — `{opacity:0,scale:.6,filter:'blur(17px)'}→{opacity:1,scale:1,filter:'blur(0)',duration:1.6,ease:'power2.in',keyframes:{scale:[.6,.93,1.07,1]}}` (slowly approaches out of the dark, then a lurch closer)
- **possess** — `{opacity:0}→{opacity:1,duration:1.15,ease:'steps(1)',keyframes:{x:[0,-5,6,-4,5,-2,0],skewX:[0,9,-10,7,-5,3,0],textShadow:['none','4px 0 #c00,-4px 0 #0aa','-6px 0 #c00,6px 0 #0aa','none']}}` (materialise then violent demonic shudder)
- **glimpse** — `{opacity:0}→{opacity:1,duration:1.35,ease:'steps(1)',keyframes:{opacity:[0,1,0,0,1,0,0,1,.05,1,.15,1],x:[0,0,0,3,0,-2,0]}}` (subliminal failing-light flicker)
- **seep** — `{opacity:0,clipPath:'inset(-15% -8% 100% -8%)',filter:'blur(4px)'}→{opacity:1,clipPath:'inset(-15% -8% -15% -8%)',filter:'blur(0)',duration:1.35,ease:'power1.inOut'}` (blood seeps down into the word; negative insets so script tops aren't clipped)

### luxury

- **tracking** — `{opacity:0,letterSpacing:'-.05em'}→{opacity:1,letterSpacing:'.28em',duration:1.4,ease:'power3.out'}` (the most "expensive" move)
- **hairrise** — `{opacity:0,yPercent:32,letterSpacing:'.07em'}→{opacity:1,yPercent:0,letterSpacing:'0',duration:1.1,ease:'power3.out'}`

### retro

- **vhs** — `{opacity:0}→{opacity:1,duration:.8,ease:'steps(1)',keyframes:{x:[0,-7,6,-3,2,0],textShadow:['none','3px 0 #ff3b5c,-3px 0 #3aa0ff','none']}}` (tracking-lock jitter + chroma)
- **stamp** — `{opacity:0,scale:1.7,rotation:-5}→{opacity:1,scale:1,rotation:0,duration:.7,ease:'back.out(2)'}` (printing-stamp thud)
- **blink** — `{opacity:0}→{opacity:1,duration:.75,ease:'steps(1)',keyframes:{opacity:[0,0,1,0,1,0,1,1]}}` (8-bit blink-in)

### neon

- **ignite** — `{opacity:0}→{opacity:1,duration:1.3,ease:'steps(1)',keyframes:{opacity:[.2,1,.2,1,.3,1,1]}}` (tube strikes + buzzes alight; glow is a style `text-shadow`)
- **buzz** — `{opacity:0}→{opacity:1,duration:1.2,ease:'steps(1)',keyframes:{opacity:[0,.7,.1,.85,.2,1,.5,1]}}` (slower warm-up rhythm)

### hype

- **stomp** — `{opacity:0,scale:1.5,filter:'blur(8px)'}→{opacity:1,scale:1,filter:'blur(0)',duration:.9,ease:'back.out(1.6)'}`
- **punch** — `{opacity:0,xPercent:-55,scale:1.1,filter:'blur(9px)'}→{opacity:1,xPercent:0,scale:1,filter:'blur(0)',duration:.6,ease:'expo.out'}` (whip from the side)
- **slap** — `{opacity:0,rotation:12,scale:1.5,filter:'blur(7px)'}→{opacity:1,rotation:0,scale:1,filter:'blur(0)',duration:.7,ease:'back.out(2)'}` (sticker/tag slap)

### playful (bounce allowed here)

- **jelly** — `{opacity:0,scale:.5}→{opacity:1,scale:1,duration:.8,ease:'back.out(2.2)',keyframes:{scale:[.5,1.12,.92,1.04,1],skewX:[0,0,6,-4,0]}}`
- **dropb** — `{opacity:0,yPercent:-85}→{opacity:1,yPercent:0,duration:.95,ease:'power2.out',keyframes:{yPercent:[-85,0,-22,0,-8,0]}}` (drop + multi-bounce). **❗opacity must reach 1 and stay** — declare it at the end of the keyframes.
- **scrawl** — `{opacity:0,clipPath:'inset(-12% 100% -12% 0)',rotation:-3}→{opacity:1,clipPath:'inset(-12% 0 -12% 0)',rotation:0,duration:.8,ease:'power2.out'}` (handwritten write-on, for script faces)
- **popr** — `{opacity:0,scale:.4,rotation:8}→{opacity:1,scale:1,rotation:0,duration:.6,ease:'back.out(2)'}`

### creator

- **boxpop** — `{opacity:0,scale:.5}→{opacity:1,scale:1,duration:.5,ease:'back.out(1.8)'}` (the active flow word's highlight box is a style)
- **slideup** — `{opacity:0,yPercent:44}→{opacity:1,yPercent:0,duration:.55,ease:'power3.out'}`
- **flip** — see premium
- **shimmer** — `{opacity:0,scale:.7,filter:'brightness(2.2)'}→{opacity:1,scale:1,filter:'brightness(1)',duration:.75,ease:'power2.out'}`

### ultra (the flash lives in the type)

- **volt** — `{opacity:0}→{opacity:1,duration:1.1,ease:'steps(1)',keyframes:{opacity:[0,1,.12,1,.35,1],x:[0,0,0,2,-2,0]}}` then settle to glow `text-shadow:0 0 8px #fff,0 0 22px #43f4ff,0 0 48px #1e90ff` (electric strike)
- **hyper** — `{opacity:0,scale:.05,filter:'blur(3px) brightness(3)'}→{opacity:1,scale:1,filter:'blur(0) brightness(1)',duration:.9,ease:'expo.out'}` (warp from depth)
- **liquid** — `{opacity:0,scale:.9,yPercent:6,filter:'blur(10px)'}→{opacity:1,scale:1,yPercent:0,filter:'blur(0)',duration:1,ease:'power2.out'}` + the `.climax` _container_ carries SVG `filter:url(#liquid)`; in HF drive `feDisplacementMap@scale` from the timeline (don't use SMIL — not seek-safe)
- **prism** — `{opacity:0,textShadow:'-38px 0 #ff003c,38px 0 #00ffd1',filter:'blur(5px)',scale:1.08}→{opacity:1,textShadow:'-3px 0 #ff003c,3px 0 #00ffd1',filter:'blur(0)',scale:1,duration:1,ease:'power3.out'}` (chromatic dispersion converge)
- **shatter** — `{opacity:0,scale:1.9,rotation:-3,filter:'blur(14px)'}→{opacity:1,scale:1,rotation:0,filter:'blur(0)',duration:1,ease:'back.out(1.4)',keyframes:{scale:[1.9,.9,1.06,.98,1]}}` (+ a 1-frame white `text-shadow` flash on landing)
- **extrude** — `{opacity:0,rotationY:42,scale:.9,transformPerspective:700}→{opacity:1,rotationY:-9,scale:1,duration:.9,ease:'power3.out'}` (3D turn; depth via stacked `text-shadow` in the style)

### atelier (design-forward)

- **editwipe** — `{opacity:1,clipPath:'inset(-15% 100% -15% 0)'}→{clipPath:'inset(-15% -4% -15% 0)',duration:.7,ease:'power4.inOut'}` (Swiss precise wipe; negative top/bottom so glyph tops aren't clipped)
- **rise** — see premium (slower, `duration:.9`)
- **block** — `{opacity:0,scaleY:0,transformOrigin:'bottom center'}→{opacity:1,scaleY:1,duration:.7,ease:'power3.out'}` (constructed/Bauhaus)
- **vert** — `{opacity:0,clipPath:'inset(0 0 100% 0)'}→{opacity:1,clipPath:'inset(0 0 0 0)',duration:.9,ease:'power2.out'}` (vertical ink-drop; `writing-mode:vertical-rl` is a style, climax sits at `left:81%`)
- **ink** — `{opacity:0,clipPath:'inset(-28% 100% -28% -4%)',filter:'blur(3px)'}→{opacity:1,clipPath:'inset(-28% -8% -28% -4%)',filter:'blur(0)',duration:.9,ease:'power2.out'}` (brush write-on; generous negative insets for the script face)
- **weight** — `{opacity:0,fontVariationSettings:"'wght' 100",letterSpacing:'.18em'}→{opacity:1,fontVariationSettings:"'wght' 900",letterSpacing:'0',duration:1,ease:'power2.out'}` (variable-font morph; needs a variable face, e.g. Inter `wght@100..900`)

### impact (the ONE sanctioned scene effect, at the climax only)

Each pairs the type move with a scene element (`<div class="flash">` / `<div class="ring">`) and/or a stage shake. Keep it to the climax beat.

- **nuke** — type: `{opacity:0,scale:.3,filter:'brightness(8) blur(10px)'}→{opacity:1,scale:1,filter:'brightness(1) blur(0)',duration:1,ease:'expo.out'}` + white `.flash` `to{opacity:0}` over 0.3 s + brief stage `x` shake
- **meteor** — `{opacity:0,yPercent:-45,scale:1.12,filter:'blur(12px) brightness(2.2)'}→{opacity:1,yPercent:0,scale:1,filter:'blur(0)',duration:1,ease:'power4.in'}` (accelerate DOWN) + on-land stage shake
- **sonic** — `{opacity:0,scale:1.4,filter:'blur(8px)'}→{opacity:1,scale:1,filter:'blur(0)',duration:.9,ease:'expo.out'}` + a `.ring` scaling `0→3` opacity `1→0`
- **seismic** — `{opacity:0,scale:1.1}→{opacity:1,scale:1,duration:.9,ease:'power3.out'}` + stage `x`/`y` quake `keyframes:[3,-3,2,-2,0]` decaying
- **judge** — `{opacity:0,yPercent:-45,scale:1.12,filter:'blur(12px) brightness(2.2)'}→{opacity:1,yPercent:0,scale:1,filter:'blur(0)',duration:1,ease:'power3.out'}` (descends from above) + light-shaft `.flash`

---

## CLIMAX exits

Default is **fade** unless a template names another. **Every exit ends at `opacity:0`** (or fully-clipped) so nothing lingers — declare opacity:0 at the end even on transform/clip exits.

- **fade** — `to{opacity:0,scale:1.03,duration:.6,ease:'power2.in'}` (premium/epic/most defaults)
- **rise-off** — `to{opacity:0,yPercent:-42,duration:.6}` · **sink** — `to{opacity:0,yPercent:16,scale:.97}` · **lift** — `to{opacity:0,yPercent:-26,letterSpacing:'.1em'}`
- **expose-off** — `to{opacity:0,filter:'brightness(3.6) blur(4px)'}` · **breathe-off** — `to{opacity:0,scale:1.08,filter:'blur(7px)'}`
- **flip-off** — `to{opacity:0,rotationX:-90}` · **fly-off** — `to{opacity:0,scale:2.5,filter:'blur(13px)'}`
- **untype** — `to{clipPath:'inset(-15% 100% -15% 0)',opacity:0,ease:'steps(11)'}` (backspace) · **scan-collapse** — `to{opacity:0,scaleY:.02}` · **power-off** — `keyframes:{opacity:[1,.3,1,.1,.5,0]}` + scaleY collapse
- **drag** (horror) — `to{opacity:0,xPercent:-40,skewX:-20,filter:'blur(11px)',duration:.55,ease:'power2.in'}` (dragged away)
- **snap** (horror) — `keyframes:{x:[0,7,-6,0],skewX:[0,-13,0],scale:[1,1.1,1.16,1.32],opacity:[1,1,1,0],textShadow:['none','8px 0 #c00,-8px 0 #0aa','none','none']}` (violent jerk then gone)
- **cut** (horror) — `keyframes:{opacity:[1,0,1,0,.8,0]},ease:'steps(1)'` (frame-drop) · **bleed** — `to{opacity:0,yPercent:50,scale:.97,filter:'blur(6px)'}` (drips down)
- **knock** — `to{opacity:0,xPercent:55,filter:'blur(9px)'}` · **peel** — `to{opacity:0,rotation:14,xPercent:42,scale:.9}` · **spin-out** — `to{opacity:0,rotation:180,scale:.3}`
- **hop** — `keyframes:{yPercent:[0,-26,120],opacity:[1,1,0]},scaleY:.7` · **popout** — `to{opacity:0,scale:.3,rotation:-10}` · **slidedown** — `to{opacity:0,yPercent:42}` · **scrawl-off** — `to{opacity:0,yPercent:-14,rotation:2}`
- **vhs-out** — `keyframes:{x:[0,-9,8,0],opacity:[1,1,0]},scaleY:.2` (tracking-lost roll) · **blink-out** — `keyframes:{opacity:[1,0,1,0,1,0,0]},ease:'steps(1)'` · **power-down** — `keyframes:{opacity:[1,.2,.7,.1,0]},ease:'steps(2)'` · **lift2** — `to{opacity:0,scale:1.12,filter:'blur(3px)'}` (stamp lift) · **shim-out** — `to{opacity:0,scale:.8,filter:'brightness(1.9)'}`
- **iris-close** — `to{opacity:0,clipPath:'circle(0% at 50% 46%)'}` (Bond) · **un-shine** — `to{opacity:0,clipPath:'inset(0 0 0 100%)',filter:'brightness(1.7)'}` · **sweep-off** — `to{opacity:1,clipPath:'inset(0 100% 0 0)'}`
- ultra family exits: **glitch-out**, **neon-out**, **hyper-out** `to{opacity:0,scale:2.6,filter:'blur(13px)'}`, **liquid-out** `to{opacity:0,yPercent:40,scale:.96,filter:'blur(9px)'}`, **prism-out** (channels split apart), **shatter-out** `to{opacity:0,scale:1.45,filter:'blur(9px)',textShadow:'7px 0 #ff003c,-7px 0 #00ffd1'}`

## Pairs with HF skills

- `hyperframes-gsap` — single paused timeline, transform aliases, ease list, the animated-property allowlist.
- `_anatomy.md` — where these four hooks attach.
- `hyperframes-animation/rules/asr-keyword-glow.md` — the verbatim active-word envelope for the flow.


<!-- ===== FILE: hyperframes/embedded-captions/references/aesthetic-principles.md ===== -->

# Aesthetic Principles for Cinematic Captions

The 18 rules that separate "designed" caption work from "preset-generated" caption work. This is the single most important reference in the skill — every plan.json and every Standard-mode HTML should be checked against these before committing.

The whole competitive thesis: every AI caption tool in 2026 (Veed, Submagic, Opus Clip, Captions.ai, CapCut) is a **preset picker**. They hand the user a box of crayons. This skill is a **director** — it exercises judgment. Beat them on taste, not feature count.

---

## The 18 rules

### 1. The subject always wins

Captions exist to serve the face, not compete with it. If the caption draws the eye before the speaker, the caption has failed. **Before shipping any plan.json, ask: "does the caption or the subject read first?"** If caption wins, shrink, dim, or move it.

### 2. Occlude, don't hover

World-class caption design puts text _into_ the scene. Letters that pass behind a shoulder, mic, or head feel diegetic. Letters that float uniformly above the lower-third feel like PowerPoint. Use the matte pipeline — that's the moat over every competitor.

### 3. Contrast is a hierarchy problem, not a brightness problem

A white box behind text is a failure of taste. Priority order:

1. `mix-blend-mode: overlay` or `screen` picking up scene luminance
2. 2–3px dark stroke + soft drop shadow
3. Narrow semi-opaque gradient bar (NOT a solid box)
4. Dim the background plate by 10–15% locally
5. (LAST RESORT) A hard white pill box — banned on cinematic directions

### 4. Kill the constant lower-third

Fixed-bottom captions are monotone. Caption zone shifts with shot:

- Tight close-up → upper sidebar or crown
- Mid-shot → embedded on back wall / foam / whiteboard
- Wide → classic lower-third offset to non-subject side

### 5. One family, two weights maximum

Hierarchy lives in **weight** (e.g., 500 → 800), not in **font**. Mixing Montserrat + script + serif in one clip is the #1 amateur tell. Ship Inter, SF Pro, Söhne, GT America, Aktiv Grotesk, or Neue Haas Grotesk with ≥5 weights and compose with weight + size.

### 6. Tracking tightens as size grows

Display-size (>40pt) wants negative tracking (-10 to -30 units, or `-0.015em` to `-0.035em`). Body-size (14–20pt equivalent) wants positive tracking (+5 to +15, or `+0.005em` to `+0.015em`). Apple SF Pro's optical-size model is the reference. Submagic defaults do the opposite — they look cheap because of it.

### 7. Cap height ≈ 3.5–5% of frame height for body captions

- 1080p vertical (1920 tall): body 65–95px, emph/hook 130–170px
- 1080p landscape (1080 tall): body 40–55px, emph 70–100px
- Hormozi-size (~7–9% of frame) is **hook** size, not body size. Reserve for punchlines.

### 8. Never italicize for emphasis in video text

Italics are a **print** convention for flow inside a paragraph. On 24fps motion they read as "tilted" not "stressed". Emphasize with weight (extrabold), color (single accent), or size (1.3–1.6×). Italics allowed only for:

- Literal quotation of written material
- Foreign word
- Thought vs spoken dichotomy

### 9. Color discipline: one hue + neutrals

Pick **one** saturated accent per video for keyword highlights. Hormozi's yellow+green+red works for him because his content is already loud. Cinematic = single accent + white/bone/charcoal. Default palette:

- Warm white `#F5EFE6` on dark
- Graphite `#1A1A1A` on light
- Accent chosen from scene sampling

### 10. Animate transform only, never the letter itself

`letter-spacing`, `filter:blur`, `font-weight` animations cause inline-block reflow → line-jumps. Animate `translateY`, `scale`, `opacity`, `clip-path`. This is locked from the embedded-captions debugging.

### 11. Minimum 0.4s per word visible

BBC reading speed is 160–180 wpm (0.33–0.38s/word). Cinematic feel wants more breathing room — 200–220ms stagger per word, hold full phrase 0.4–0.6s before exit. Entries under 150ms read as frantic.

### 12. Stagger is the primary expressive axis

Same phrase, different stagger, totally different feel:

| Stagger | Feel                             |
| ------- | -------------------------------- |
| 40ms    | machine-gun, urgent, TikTok-hook |
| 80ms    | conversational, default          |
| 150ms   | deliberate, documentary          |
| 250ms+  | poetic, ceremonial               |

Pick from content tone, not default to one value.

### 13. Emphasis escalates _within_ a phrase, not _between_ phrases

Every word bolded = no emphasis. Structure:

- 70% plain body
- 20% slight lift (color OR weight, not both)
- 8% full emphasis (bigger, brighter, held longer)
- 2% climax (biggest, held 1.5s, breath before + after)

### 14. Break rhythm once per 30s

Every-word-same-way = eye adapts, stops registering motion. Plant a rhythm-break every ~30s:

- Phrase enters from opposite direction
- A single word at 2× size
- A beat of pure silence with no caption
- A color shift

This is what separates Submagic-preset work from something designed.

### 15. Caption what adds, cut what restates

Transcribe everything. **Display** 70–85%. Remove:

- Filler ("um", "like", "you know", "I mean")
- Self-corrections ("I think... I mean actually...")
- Obvious visual echoes ("as you can see here" while pointing)

Editorial judgment — no existing AI caption tool does this. It's pure upside.

### 16. Segment on breath, not on duration

Chunk at natural pauses ≥ 250ms. A caption spanning a breath-break feels wrong. Whisper word-level timestamps make this trivial.

### 17. Safe zones per platform, always

- Use the safe boxes in `/hyperframes-studio` (Safe zones) for wide and vertical
  framings; that skill owns the values.

Bake into the layout solver. Never eyeball.

### 18. Letterbox/pillarbox is caption real estate

Black bars on 9:16 from 16:9 source? Those bars are the caption home. 2.35:1 cinematic frame on 16:9 export? Serif quotation in the letterbox reads as documentary.

---

## Rhetorical judgment rules (editorial)

These are the "what to caption" decisions. No existing tool exercises them.

- **Filler suppression** — off/light/strong. Default: light for documentary, strong for vlog.
- **Self-correction folding** — display only the final version.
- **Breath-group segmentation** — split on silences >250ms, never mid-phrase.
- **Semantic emphasis** — LLM-pass per phrase: "which 1–2 words carry the meaning?" Highlight those. Don't default to stressed syllables or loudest words.
- **Silence honor** — if speaker pauses 1.5s+ for rhetorical effect, don't back-fill with lingering prior caption. Let silence breathe.
- **Quote-sensing** — "he said, quote…" or air quotes → italic (one of the allowed italic exceptions).
- **No `[laughs]` / `[sighs]`** — those are accessibility captions. For aesthetic captions, they pollute the frame.

---

## Self-critique checklist (run before rendering)

The agent's own pre-render pass. Flag violations:

- [ ] Does the caption or subject read first? (Rule #1)
- [ ] Any hard white pill boxes? (Rule #3 — banned on cinematic)
- [ ] Still lower-third for a close-up? (Rule #4)
- [ ] More than 2 weights or more than 1 font family? (Rule #5)
- [ ] Italic used for emphasis? (Rule #8 — banned)
- [ ] More than 1 saturated accent color? (Rule #9)
- [ ] Letter-spacing or filter:blur animating? (Rule #10 — banned)
- [ ] Stagger same for documentary and vlog? (Rule #12)
- [ ] Every group emphasized? (Rule #13)
- [ ] 30s+ with no rhythm-break? (Rule #14)
- [ ] Displaying every filler word? (Rule #15)
- [ ] Caption crossing breath-break? (Rule #16)
- [ ] Caption in platform UI zone? (Rule #17)

Any "yes" to a violation question → regenerate the affected segment.


<!-- ===== FILE: hyperframes/embedded-captions/references/anti-patterns.md ===== -->

# Anti-Patterns

You default to these. Stop.

Each entry: the bad habit, what it produces, what to do instead. Written in the voice of someone who has watched an agent do this 10 times — because we have.

---

## Layout

### You default to center-aligned crown.

`.crown-plane { left: 0; right: 0; text-align: center }` is the template default, and you'll leave it on every video because it worked once. On a subject that sits right-of-center (Jobs in a 16:9 frame), the body eats the middle 60% of the word and "THE BEATLES" becomes "THE \_\_\_ S".

**Before using the default crown**, run the three conditions in [layout-heuristics.md § Crown placement](layout-heuristics.md):

1. Subject centered within 10% of frame center
2. Clean zones ≥ 15% on each side
3. Crown width > subject width + 400px

If any one fails, **move the crown to the larger clean zone** with a narrower container and smaller font. Don't keep centering a word that's about to be 60% occluded.

### You compute text leftmost as `plane_left + padding`.

That's correct for left-aligned. Wrong for the templates you're using, which are **right-aligned** on the main column and **center-aligned** on crowns. The real leftmost depends on the word width.

| Alignment | leftmost_x                                         |
| --------- | -------------------------------------------------- |
| Left      | `plane_left + padding_left`                        |
| Right     | `plane_right − padding_right − longest_line_width` |
| Center    | `plane_center − longest_line_width / 2`            |

Compute it against the **longest wrapped line**, not the whole phrase. "four very talented guys" wraps to 3 lines — the widest is "talented" (~8 chars), not 23.

### You treat `plane_left` as the text's leftmost edge.

It isn't. With `left: 180px` and a right-aligned 468px word, the text starts 104px **before** `plane_left` relative to the plane, but actually lands somewhere inside the plane box. The plane box just sets the coordinate space — the text positions inside it based on alignment. Check the compiled output, not the plane attribute.

### You center text on the frame when the subject is off-center.

Look at the subject's body center, not the frame center. Jobs sits at x=1100 in a 1920 frame. The **scene's** center of gravity is 1100, not 960. Center-aligning text to 960 is center-aligning to the empty left third, not to anything meaningful.

### You copy-paste position values from memory-wall to a new video.

`top: 40, right: 30, width: 720, rotateY: -13` worked for a 1280×720 frame with an acoustic foam wall on the right. It will not work on a 1920×1080 frame with a bookshelf backdrop. Run the 6-item checklist in [scene-types.md](scene-types.md) for the new video before reusing any numbers.

---

## Typography

### You use template default font sizes regardless of column width.

Template defaults (66/78/92/140) are tuned for a ~560px column. When you bump the plane to 700px+ and don't touch the fonts, the captions feel underweight — small text swimming in negative space.

Use the [Font-size × column-width matrix](typography-presets.md). For a 700px column, that's 78/108/128/220 — a 30-40% bump across the board. Re-check pillarbox safety after bumping (bigger right-aligned text extends further left).

### You pick `intro` style for every first caption.

Intro = italic, smaller, contemplative. Fine for filler discourse markers ("You know,", "So,", "Well,"). **Not** for the first line when it's actually the thesis ("I've had this kind of upbringing"). Read the words semantically, not positionally.

### You skip emphasis entirely because "every caption looks clean."

A story without an emph or crown is typographically flat — viewers can't feel the crescendo. Reserve at least ONE emph per video for the line that lands. Skip it only for truly monotone content (policy statements, warnings).

### You give every group its own style.

Style is supposed to signal _hierarchy_. Using `intro`/`phrase`/`emph`/`dream`/`crown` all in one 15-second video means none of them signal anything. Pick 2-3 styles max for a short clip.

### You only use the 5 preset class names.

`intro / phrase / emph / dream / crown` are scaffolding, not a closed set. The canonical `memory-wall.html` uses `cap-1 / cap-2 / cap-3 / cap-4` — **position-indexed** with bespoke typography per position. That's how it achieves the 3-line right-aligned cascade on the climax. You can't express "this cap has a hanging indent at position 2" with `"style": "dream"`.

The `"style"` field in plan.json accepts **any string** — it becomes `class="cap-<string>"`. Define the class in `custom_css`:

```json
"custom_css": ".cap-1 { font-size: 78px; ... } .cap-2 { padding-right: 44px; }",
"groups": [{"id": "cg-0", "style": "1", ...}]
```

When the scene needs per-position bespoke typography, do this. Don't force-fit into `intro / phrase / emph`.

### You regenerate from plan.json when a canonical example already has the answer.

When scene framing matches `references/example-renders/memory-wall.html` or `champion.html`, clone that HTML into `<project>/index.html` and only swap the GROUPS array. Don't re-derive the design from presets — you'll lose the specific per-position typography that took many iterations to validate. See [bespoke-vs-presets.md § The clone-and-tweak workflow](bespoke-vs-presets.md).

---

## Blending

### You default to `mix-blend-mode: overlay`.

Overlay works on **mid-tone** backgrounds. On dark bookshelves (<60 luminance), overlay makes white text render as black. On sunny backgrounds (>180 luminance), overlay blows out. Check the actual luminance of the caption region in a sampled frame. Pick:

- mid-tone surface (60-180) → `overlay`
- dark surface (<60) → `screen`
- bright surface (>180) → `normal` with opaque text

### You animate `letter-spacing` on the word entry.

You saw a "typewriter breath" effect somewhere and added `letterSpacing: "0.04em"` to the `fromTo` "from" state. Result: inline-block reflow every frame → the whole `.cap` line box recomputes → captions visibly jump between rows. See the "Some → line 2" bug from memory-wall.

**Animate only opacity + transform.** If you want a breath effect, use `scale` or `y`, not letter-spacing.

---

## Animation

### You fade both the group container AND each word.

Default feels safer: fade the container in, then fade each word in. But container.opacity × word.opacity produces a non-linear curve — at progress 40% the combined opacity is 16%, not 40%. Visible result: captions seem to "pop" into view around halfway.

Set container opacity to 1 at entrance via `tl.set`, then fade only the words. Single-layer opacity = linear perceived fade.

### You stack captions in a flex column.

Flex-direction: column with multiple `.cap` children looks tidy in source. At runtime, hidden captions (`visibility: hidden`) still reserve flex space. The newly-entering caption shows up at the _bottom_ of the column instead of the designed position — landing in the gesture zone, getting clipped.

Use `position: absolute` for each `.cap` inside the plane so hidden ones don't occupy layout. Both shipped templates do this.

### You start the timeline at t=0.

Caption at exactly t=0 feels like it was there before the video started. Offset 0.1-0.3s (hyperframes motion-principles.md agrees). Same for the very last caption — let it exit before the video fades.

---

## Scene admission

### You trust that "looks like one speaker" = "is one speaker throughout."

TV archive clips cut to B-roll mid-sentence. Interview clips insert cutaways to the interviewer. You didn't check frames beyond the first one, so you rendered captions across a shot transition. Result: captions designed for Subject A are placed relative to Subject B's position (or empty frame) for half the render.

Sample frames at 20%, 50%, 80% BEFORE planning. If the scene changes, trim to the largest single-subject segment.

### You ignore baked-in captions / pillarbox / watermarks.

You saw black bars on the sides and didn't computing the safe-zone. Your captions cross the pillarbox. Or: the source already has burned-in subtitles and you added more — two caption systems fighting for attention.

Run the **letterbox probe** first. If the source has existing captions, refuse with: "source already captioned, adding more would conflict."

### You ship Whisper's transcript without checking timings against the beat.

Transcription is Whisper (via `transcribe.cjs`, no API key) — good word timings, but not infallible: a word can land with a near-zero duration or a timestamp a beat off. This skill is verbatim + on-beat, so `check-timing.cjs --strict` (80ms tolerance) is the gate, not a suggestion — fix drift in `plan.json` before rendering, and never pack two transcript words into one timed entry (the second inherits the first's timestamp and fires early).

---

## Matting

### You enable CoreML for the matting ONNX.

It's the Apple way, obviously faster. No. CoreML partitions the ONNX graph across providers. The mixed-precision boundary produced (observed with the previous RVM engine) alpha=30 inside the subject's face while background correctly reads 0. Captions shine through face. Pin the CPU execution provider only (`onnxruntime-node`). Our `matte.cjs` already does this; don't "optimize" it by re-adding CoreML.

### You pick a matte model by "general vs human."

DECISION FLIPPED 2026-06-12 after a 5-model × 6-scene A/B with caption renders: the matte's job here is CAPTION LAYERING, not prop fidelity. `u2net_human_seg` (via hyperframes `remove-background`) usually excludes thin offset furniture (mic boom arms) from the matte — words stop being sliced by booms, which beat PP-MattingV2's prop-preserving behavior on real caption videos. It is NOT surgical: large salient objects near the subject (telescope rigs) can still leak in — always sample frames_fg/. Known cost: HELD products can drop out intermittently (captions pass in front) — route product-demo climaxes away from held objects. `isnet-general-use` lost outright (backlit-hair collapse). birefnet-portrait (MIT) beat everything semantically (keeps held items AND drops furniture) but is 928 MB / ~7 s-per-frame CPU — a future quality tier, not the default.

---

## Grouping

### You caption every word.

Transcripts are verbose — "you know, um, I, I mean, you know" is 5 words from a single beat. Captioning all of them clutters the screen and breaks reading rhythm.

Editorially drop filler. Use the rules in [caption-grouping.md](caption-grouping.md): merge short fragments, cut repeated discourse markers, keep the meaning, trim the noise. You are writing typography to support speech, not a court transcript.

### You group by fixed word-count.

"3 words per caption, always" makes every caption look the same and fights the natural cadence of speech. Break on sentence boundaries, 250ms+ pauses, and semantic units instead. Caption sizes will naturally vary from 2 words to 5 — that's correct.

---

## The meta anti-pattern

### You read one reference doc and skip the rest.

You'll read this file alone and feel covered. These anti-patterns reference concepts defined in `layout-heuristics.md`, `typography-presets.md`, `scene-types.md`. If you haven't read those, the fix advice here won't make sense.

**Order of reading for a new video**:

1. GUIDE.md (decision gate + pipeline + pre-flight probes)
2. bespoke-vs-presets.md (**first check if a canonical example fits — clone if so**)
3. scene-types.md (template selection — all 4 wall conditions)
4. layout-heuristics.md (positions, sides, crown, font scale, pillarbox formula)
5. typography-presets.md (font-size × column-width table, starting points)
6. caption-grouping.md (word → group)
7. **This file last** (to catch yourself before committing to plan.json)

If you're pressed for time, still read this one — it flags the failures you're about to make.
