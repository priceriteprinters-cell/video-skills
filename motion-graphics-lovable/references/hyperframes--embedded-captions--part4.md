

<!-- ===== FILE: hyperframes/embedded-captions/references/layout-heuristics.md ===== -->

# Layout Heuristics

How to pick `wall_position` / `crown_position` in plan.json.

## Step 1: Sample 3 frames

```bash
ffmpeg -y -ss 0.5 -i source.mp4 -vframes 1 frame0.jpg
ffmpeg -y -ss <mid> -i source.mp4 -vframes 1 frame1.jpg
ffmpeg -y -ss <end-0.5> -i source.mp4 -vframes 1 frame2.jpg
```

Read all three. Note: subject's head bbox, shoulder top line, and wherever hands move during gestures. Worst-case foreground envelope = union across all 3.

## Step 2: Find the clean zone

The caption plane should live in pixels that are **always background** across the clip. Never where the body lands.

Annotate approximate ranges:

- Head bbox: `head_x_min`, `head_x_max`, `head_y_min`, `head_y_max`
- Hand gesture envelope (if any): usually below `y = shoulder_top ≈ head_y_max + 40`
- Props (mic, cup): typically static, note bbox

**Clean zones**, in priority order:

1. **Corner farthest from head** (usually opposite the gaze direction)
2. **Upper strip above head_y_min minus 30px margin**
3. **Lower-third** if upper is occupied (last resort — breaks "embedded" aesthetic)

## Step 2.5: Which side of the subject?

Once you know where the subject and baked graphics are, decide which side (left or right of the subject) hosts the caption column. Order of precedence:

### 1. Hard constraints first — baked graphics

Logos, watermarks, date stamps, "60 Overtime"-style lower-thirds are already in the source. They occupy permanent zones you must avoid. Map them out from frame samples:

- Jobs 60 Minutes: "2003" at upper-left (x=280-460, y=30-90); "60 Overtime" at bottom-left (x=280-770, y=960-1080). Left side partially constrained; still usable above/below these.
- TikTok re-uploads: username watermark that rotates corners every few seconds — hard to plan around, often a refusal reason.

If one side has a hard constraint that eats > 60% of that side's clean zone, default to the other side.

### 2. Subject body bias — pick the bigger clean zone

Compute clean-zone widths on both sides:

```
left_clean_width  = body_x_min − safe_left_margin
right_clean_width = safe_right_margin − body_x_max
```

Pick the side where clean zone is wider. If the difference is within 10% of frame width, the sides are ~equivalent → fall through to step 3.

Worked examples:

- **Champion** (Djokovic, 1920×1080): body x ≈ 550-1200. Left clean = 510, right clean = 720. Right is wider → but we put captions LEFT because of gaze (see step 3). The narrow difference made either workable.
- **Jobs**: body x ≈ 700-1480 (right-of-center). Left clean = 420, right clean = 160. Left wins decisively. Captions went LEFT.
- **Memory Wall**: surface location dictated the side (see note below about wall-embed).

### 3. Gaze direction — the "looking room" rule (tiebreaker and aesthetic)

Classic cinematic framing: leave more empty space on the side the subject is **looking toward**. This preserves their gaze path and feels uncluttered. **Captions go to the OPPOSITE side** (the side the subject is facing away from), so they don't steal looking room.

Quick check: sample 3 frames. Estimate the eye-line vector. Does it point more left or right?

- Looking screen-right → captions on LEFT
- Looking screen-left → captions on RIGHT
- Looking forward at camera → no preference from gaze, use step 2 only

The champion / Djokovic shot has him addressing camera slightly from the left — captions on LEFT actually read like text he's looking toward, which can feel like he's acknowledging them. That's fine here but is a flavor choice; generally prefer gaze-opposite.

### 4. Narrative emphasis (for optional crown)

If you're using a **center-stage crown**, it sits across the subject — no left/right choice for it. But the other captions (the column) still follow steps 1-3.

If you're using a **clean-zone crown** (shrunk, placed in one clean zone instead of crossing the body), put it in the **same side as the main column** for visual consistency. Don't split crown and column on opposite sides — it creates ping-pong.

### Special case — wall-embed

When the template is `wall-embed`, the side is **dictated by where the usable surface is**, not by body bias or gaze. Memory Wall's foam panel was on the right, so captions went right even though the subject was slightly left-of-center. Surface location wins because the whole effect depends on the text sitting ON that specific surface.

### Decision summary

```
Side = f(baked graphics, body bias, gaze, surface)

priority:
1. Hard constraints (baked logos)    — never place here
2. Wall-embed surface location       — wins if using wall-embed
3. Bigger clean zone                 — default for corner-column
4. Gaze direction (looking room)     — tiebreaker when both sides similar
```

If the subject actively swings their gaze across the clip (turning head L→R), pick a side that works for both extremes, not just the most frequent. Or accept that looking room will briefly be violated — it's a 10-second video, nobody cares.

## Step 3: Pick template + position

### If scene has a flat back wall (acoustic foam, plaster, fabric backdrop)

→ `wall-embed.html`

```
wall_position: {
  top:       max(40, head_y_min - 40),
  right:     20-60 (hug outer edge),
  width:     video_width * 0.35 – 0.50,
  height:    shoulder_top - top,
  rotateY:   -10 to -16 deg if wall angles away on the left,
             +10 to +16 deg if mirrored, 0 if wall is parallel,
  rotateX:   0-3 deg subtle downtilt only
}
```

`mix-blend-mode: overlay` in this template — works on mid-tone walls. If wall is near-black (luminance < 60), switch CSS to `screen`.

### If scene has a cluttered but dark backdrop (bookshelf, plants, set dressing)

→ `corner-column-crown.html`

```
wall_position: {
  top:       40,
  left:      40,               // anchor to clean corner opposite head
  width:     video_width * 0.40,
  height:    clamp(360, 520),  // don't reach below shoulder top
  rotateY:   3-6 deg (subtle, not flashy)
}
crown_position: {
  top:       video_height * 0.40   // center-ish; body will cut middle letters
}
```

`mix-blend-mode: screen` is correct here (bookshelf is dark).

### If subject fills >70% of frame

Template doesn't matter — there's nowhere clean. **Refuse**, suggest classic lower-third.

## Step 3.5: Crown placement (when using `corner-column-crown`)

**Default preference: center-stage crown.** A big, centered crown word (think "WIMBLEDON CHAMPION", "BEATLES", "SHARP AGAIN") that crosses the subject is the most powerful embed move — body occludes the middle letters, clean zones on both sides hold the outer letters, and the word reads as a title drop. **Use this whenever conditions allow.**

### Conditions where a centered crown works

Sample 3 frames, eyeball the subject's horizontal envelope across the clip. Let `body_x_min / body_x_max` = tightest horizontal bounds that contain the head+shoulders+arms in any frame.

A centered crown at font size F (where `crown_width ≈ F × 0.55 × char_count`) reads as dramatic IF:

1. **Subject is roughly centered**: `|body_center_x − frame_width/2| < frame_width × 0.10`. The body sits in the middle third.
2. **Clean zones on both sides are non-trivial**: `body_x_min > frame_width × 0.15` AND `body_x_max < frame_width × 0.85`. There's ≥15% of frame width clean on each side.
3. **The crown word is wide enough to poke out both sides**: `crown_width > body_width + 400px`. If the word ends before reaching the body's right edge, most letters just get swallowed — ugly.

If all three hold, centered crown is right. Go big — font sized so the word spans `0.8 × frame_width` or more. "BEATLES" at 140px (~500px wide) fails condition 3 on an 1920 frame with Jobs-sized body (780px wide). "WIMBLEDON CHAMPION" at 140px (~1700px) on the same frame passes easily.

### When center fails — move crown to the clean zone

If any of the three conditions fails, center-stage eats too much and the word becomes illegible ("THE BEATLES" → "THE" and a sliver of "S"). Two strategies:

**Option A — shrink crown to fit cleanly in the larger clean zone.** Pick the side opposite the subject's bias. Compute `clean_zone_width` on that side. Pick crown font such that the word wraps to 1-2 lines inside it. Tail letters can touch the subject edge for a hint of embed, but the body of the word lives on backdrop.

```
// Jobs: subject center ≈ x=1100 (right of frame center 960). Left clean zone is larger.
crown_plane: { left: 200, width: 560, text-align: center }
font-size: 118px  →  "THE / BEATLES" wraps to 2 lines, fits in x=230-770
                      leaving "S" tail at x~760 lightly touching Jobs's shoulder
```

**Option B — drop the crown entirely, promote the word to `emph` in the main column.** Simpler when the phrase doesn't deserve dramatic center-stage treatment. Works fine for 2-word emph like "the Beatles" or "incredible things" — they become large bold text in the left column with body occluding their tails.

### Rules of thumb for choosing

| Subject occupies center X%+ of frame | Clean zones L/R          | Crown approach                                  |
| ------------------------------------ | ------------------------ | ----------------------------------------------- |
| < 50%, roughly centered              | both ≥ 15% of width      | Centered crown, go BIG (frame_w × 0.8+)         |
| 50-70%, slightly offset              | one side ≥ 25%           | Crown shifted to larger clean zone              |
| > 70%, fills most of frame           | neither side wide enough | Drop crown, use `emph` in column                |
| Close-crop face, fills > 80%         | essentially none         | No crown. All captions in a header/footer strip |

## Step 4: Respect these invariants

1. **Never cover the eyes.** Eye bbox is sacred. Add 20px margin around it when checking caption bbox intersection.
2. **Caption bbox must not exit frame.** Reserve 4% broadcast-safe margin on all edges.
3. **Large emphasis words should have horizontal slack.** At `cap-emph` (92px), an 8-char word ≈ 580px. Plane needs ≥ 620px width OR rely on wrapping at 2 lines.
4. **Crown lives at `top ≈ shoulder_top − crown_font_size/2`** so it sits across the upper body, not the face.
5. **If aspect ratio is portrait (9:16), rotate layout**: wall-plane becomes a **top band** (full width, height ≈ 20%), crown goes below it if used at all.

## Step 5: Validate before render

Before calling `render-and-composite.sh`, sanity check:

- Did you place the plane in the opposite quadrant from the face? ✓
- Does the plane exit the frame anywhere? If yes, shrink.
- Is the font too big for the plane width? Calculate: longest word in words[] × 0.55 × font_size < plane_width - padding\*2.
- For `corner-column-crown`, did you set `crown_position.top` so the crown actually crosses the body (not above the head, not below the torso)?
- **Pillarbox / letterbox hard check.** If the source has black bars (see pre-flight probe in GUIDE.md), compute `leftmost_text_x` using the correct formula for the text alignment:

  | Alignment                   | Formula                                            |
  | --------------------------- | -------------------------------------------------- |
  | Left-aligned                | `plane_left + padding_left`                        |
  | Right-aligned (main column) | `plane_right − padding_right − longest_word_width` |
  | Center-aligned (crown)      | `plane_center − longest_word_width / 2`            |

  Where `longest_word_width ≈ font_size × char_count × 0.55` (adjust 0.55 down to ~0.50 for italic, up to ~0.62 for uppercase bold). **All** of these must be ≥ `pillarbox_left_edge + 10–20px` (safety margin). Mirror for the right bar.

  **Gotcha from past iteration**: setting `plane_left = 180` with a right-aligned column on a Jobs 60 Minutes clip (pillarbox at 280) looked "inside the plane" but the right-aligned text at font 108px produced `leftmost = plane_right − padding − 468 = 180 + 700 − 36 − 468 = 376` … wait, that IS past pillarbox. The actual bug was different: for a 3-line wrap ("four very / talented / guys") the widest line is "talented" at ~468px, not the whole phrase. Compute against the longest **single line** after wrap, not total phrase width.

  **Re-check after font-size changes** — bumping font 84→104 shifts right-aligned text leftward by ~30px. If the budget was already tight, the bump blows through the pillarbox.

  **Empirical target**: leftmost text at pillarbox + 10-20px looks "anchored" to the bar (visually grounded). Pushing it much deeper (50px+) makes captions feel floaty in the middle of the frame.

## Worked examples

### memory-wall (1280×720, acoustic foam wall)

```json
{
  "template": "wall-embed",
  "wall_position": {
    "top": 40,
    "right": 30,
    "width": 720,
    "height": 520,
    "rotateY": -13,
    "rotateX": 1
  }
}
```

### champion (1920×1080, bookshelf backdrop)

```json
{
  "template": "corner-column-crown",
  "wall_position": { "top": 40, "left": 40, "width": 720, "height": 420, "rotateY": 4 },
  "crown_position": { "top": 440 }
}
```


<!-- ===== FILE: hyperframes/embedded-captions/references/motion-vocabulary.md ===== -->

# Motion Vocabulary — named word-entry moves

10 motion primitives the skill uses. Each has a specific timing + easing + situational fit. Agent picks by **content tone**, not default to one.

**Easing philosophy:** `cubic-bezier(.2,.7,.2,1)` is the "considered confident" default. `linear` is almost always wrong. Back-easing (elastic) is for playful content only — never documentary.

**Exit rules:** Default exit is the same tween reversed at 60% duration. Never exit with a different motion than entry unless doing a rhetorical pivot. Never fade out during speech — only during the gap between phrases.

---

## The 10 moves

### 1. typewriter

Char-by-char reveal, 25–35ms/char, linear easing. Documentary / data-heavy / tense / interrogative.

```js
// GSAP
words.forEach((w, i) => {
  const chars = w.textContent.split("");
  w.textContent = "";
  chars.forEach((c, j) => {
    const span = document.createElement("span");
    span.textContent = c;
    span.style.opacity = 0;
    w.appendChild(span);
    tl.to(span, { opacity: 1, duration: 0 }, wordStart + j * 0.028);
  });
});
```

### 2. word-fade-up (DEFAULT)

Per-word, 80ms stagger, `opacity 0→1 + translateY 8→0`, `cubic-bezier(.2,.7,.2,1)` (ease-out). Default for conversational content.

```js
tl.fromTo(
  word,
  { opacity: 0, y: 8 },
  { opacity: 1, y: 0, duration: 0.45, ease: "power2.out" },
  wordStart,
);
```

### 3. word-pop

Per-word, 60ms stagger, `scale 0.85→1 + opacity 0→1`, elastic-light `cubic-bezier(.34,1.56,.64,1)`. Energetic / YouTube-vlog / high-tempo. **Never for documentary.**

### 4. swipe-reveal

Whole phrase at once, 400ms, `clip-path inset 0 100% 0 0 → 0 0 0 0`, expo `cubic-bezier(.77,0,.175,1)`. Keynote / tech product / announcement.

```css
.cap {
  clip-path: inset(0 100% 0 0);
}
/* animate to inset(0 0 0 0) */
```

### 5. drop-and-settle

Per-word, 120ms stagger, `y: -30→0` with back-bounce `cubic-bezier(.68,-.55,.27,1.55)`. Playful but controlled. **Not for documentary.**

### 6. etch

Whole word at once, 600ms, opacity ramp `0→1` with slight blur→sharp transition. Ease-in-out. Poetic / lyrical / "quote on wall" direction.

### 7. crosshair

Per-word, 200ms total: two 1px lines converge on word center (linear 150ms), then word snaps in (expo-out 50ms). Thriller / investigative doc.

### 8. breathing-hold

**Static but alive.** No entry animation. Once visible, micro-scale loop `1.00↔1.008` over 2s, sine ease. Used on climax lines held 1.5s+.

### 9. cascade

Each word from alternating direction: L, R, L, R. `translateX: ±40→0`, ease-out 300ms. **Rhythm-break move** — use sparingly, once per 30s max.

### 10. burn-in

**Zero animation.** Sudden 1-frame opacity 1. No fade, no transform. Interview-doc style. Use for every 6–8th phrase in a documentary direction for variety (Standard mode; see direction-catalog §1).

---

## Tone → timing lookup table

| Tone           | Stagger                   | Hold        | Entry move                         |
| -------------- | ------------------------- | ----------- | ---------------------------------- |
| documentary    | 150ms                     | 600ms       | burn-in (70%) + word-fade-up (30%) |
| conversational | 80ms                      | 400ms       | word-fade-up                       |
| energetic      | 50ms                      | 300ms       | word-pop                           |
| poetic         | 250ms                     | 1200ms      | etch                               |
| broadcast      | 0 (burn-in)               | BBC timings | burn-in                            |
| investigative  | 25ms/char                 | 500ms       | typewriter                         |
| keynote        | 0 per-word (phrase swipe) | 600ms       | swipe-reveal                       |

Agent picks tone → this table → GSAP parameters. Data, not guesswork.

---

## Per-word vs per-phrase animation axis

Orthogonal to the 10 moves above.

- **Per-word animation** (default): each word enters at its `w.start` timestamp. Tight sync with speech.
- **Per-phrase animation**: whole group enters/exits at `g.in`/`g.out`. Words appear together. Used for:
  - swipe-reveal moves
  - burn-in (no animation, but the "reveal" is a group event)
  - title cards / chapter breaks

Rule: per-word for content that tracks speech; per-phrase for moments that step outside the speech flow.

---

## Stagger breakdown by context

Fine-tune stagger within a tone:

- **Documentary dialog**: 150ms (measured)
- **Documentary punchline**: 250ms (weighted)
- **Vlog opener**: 50ms (fast hook)
- **Vlog narration**: 70ms (conversational but snappy)
- **Poem / lyric**: 250–400ms per word, with 500–1000ms gaps between phrases
- **Keynote hero**: per-phrase only (stagger = N/A)
- **Interview name card**: 0 stagger (static)

---

## Anti-patterns (banned, from anti-patterns.md)

- Animating `letter-spacing` → reflow
- Animating `filter:blur` → reflow + can wash out text
- `Math.random()` / `Date.now()` in timeline → non-deterministic render
- Entries under 100ms total → frantic, unreadable
- Same motion for every group for 30s+ → eye adapts, stops registering

---

## When to break the vocabulary

The 10 moves are a comfortable coverage, not a ceiling. For Standard mode, invent new moves when the scene demands it:

- Kyle Cooper's scratched typewriter for noir
- K-pop lyric's directional word-from-side
- Film-title flash-cut burn-in with chromatic aberration

When inventing: stay deterministic, stay transform+opacity only, state the motion in terms of the 4 axes (entry, hold, exit, stagger).


<!-- ===== FILE: hyperframes/embedded-captions/references/rail.md ===== -->

# Rail track — standard lower-third subtitle

The **default** caption track and the workhorse: a clean, readable subtitle that sits **in
front** of everything (never occluded by the matte) in the lower third. It carries **most**
of the transcript. It is deliberately **plain** — the cinematic craft (planes, occlusion,
Vogue-masthead, accumulation) lives in the _embed_ track only ([composition-craft.md](composition-craft.md)).

For talking-head / explainer / voiceover, the typical output is **the whole transcript on the rail**
with only the climax(es) promoted to embed. Rail is not a fallback — it's the baseline.

> **Implementation note.** A dedicated rail renderer is the next build step. The rail is a
> plain `fg` caption track and maps cleanly onto hyperframes' native caption pipeline
> (`media-use` captions) — prefer reusing that over hand-rolling. Until wired, render
> the rail as a simple `data-caption-layer="fg"` composition (no matte overlay for these caps).

## Position & safe area

- **Lower third, horizontally centered.** Landscape (16:9): baseline ~80–120px above the
  bottom edge. Portrait (9:16): lower-middle, ~ 600–700px from the bottom (clear of platform UI).
- **Title-safe margins:** keep text within the title-safe box (80% of the frame, `/hyperframes-studio` Safe zones) / inside any letterbox-pillarbox bars
  (see the letterbox probe). Never flush to the frame edge.
- **One caption group on screen at a time.** No accumulation, no cascade — that's embed-track behaviour.
- It rides above the subject; the matte does **not** occlude it (rail = in front).

## Lines, length, timing

- **≤ 2 lines.** Broadcast target ~ 32–42 chars/line; break at a clause/phrase boundary, never
  mid-word, never leave a dangling 1-word line.
- **Word-synced.** Each group's window envelops its words (`group.in ≤ first word.start`,
  `group.out ≥ last word.end`); each group ≥ 0.5s on screen; ~1.5s min gap discipline so it
  doesn't strobe. Word timings within 80ms of transcript (same gate as everywhere).
- **Grouping** = short readable phrases (see [caption-grouping.md](caption-grouping.md)) — not the
  embed track's "phrase = composition" rule; here it's just legible subtitle chunking.

## Look (restrained on purpose)

- **Size: ~`calc(0.045 * var(--h))`** (≈48px @1080, ≈58px @1290) — readable, _not_ hero. The rail is a subtitle; it is deliberately much smaller than the embed body/climax. Express as a `var(--h)` fraction (never hardcode px) so it scales across resolutions. The embed climax is sized to the frame independently (see composition-craft § POP) — **never** size the climax as a multiple of this rail.
- One clean sans (Inter / Helvetica Now / Neue Haas), weight 500–600; white (or near-white).
- **Legibility without grading the video:** a tight text treatment local to the glyphs only —
  a soft dark drop-shadow, or a subtle rounded gradient pill / 30–40% scrim **sized to the text
  box** (not a full-frame bar, never a frame-wide grade). On luminance > 180 backgrounds, keep
  the scrim; never rely on bare light text.
- Motion is minimal: 150–250ms fade-up in / fade-down out. No glitch, no scale-pop, no per-word
  choreography on the rail — that energy is reserved for embed.

## The `emphasis` flag (active-word highlight)

The only intensity the rail carries. When a word is graded `emphasis` (the 1–2 punch words in a
phrase), give it an **inline** lift on the rail — accent colour and/or +weight, optionally a
karaoke-style active-word pop (≤1.1× scale) as it's spoken. Keep it inline; it does **not**
leave the rail. Anything that wants to leave the rail is an `embed`, not an emphasis.

## What the rail never does

- Never goes behind the subject (that's embed).
- Never accumulates into a multi-line poem (that's embed).
- Never crosses the face / uses occlusion as an effect.
- Never grades or textures the underlying video.
- Doesn't drop content to "fit fewer blocks" — split into more groups instead. The only drops
  are filler (um/uh, exact stutters, self-corrections); dense conversational `narrator` glue
  ("you know", "sort of") may be trimmed for readability, content/structure words stay.

## Hand-off to embed

Rail + embed coexist in one render: the rail runs the whole clip; an embedded peak appears over
it at its moment (the rail can briefly clear or dim under the embed if they'd collide). Decide
which phrases promote via the role read in GUIDE.md § Caption model; author the promoted ones
with [composition-craft.md](composition-craft.md).


<!-- ===== FILE: hyperframes/embedded-captions/references/reference-bar.md ===== -->

# The reference bar — what world-class looks like

Self-review without an external bar always passes. Before shipping, hold the render
against these references — not "is anything broken" (the gates did that) but "would a
designer at these houses sign it".

## Per register

**premium-warm / editorial (cream, editorial)** — the bar is a _Vogue cover_ and the
A24 title card: type interacts with the subject (masthead behind the head), one or two
sizes feel chosen not defaulted, the frame would work printed as a poster. Check: does
the climax frame, screenshotted alone, look like a designed cover — or like a subtitle
that grew?

**tech-premium (keynote, ink)** — the bar is an _Apple keynote slide_ over footage:
opaque, weighty, dead-center confidence; negative space is doing the work; nothing
decorating. Check: would this frame look at home in a WWDC sizzle?

**formal (documentary)** — the bar is _Errol Morris / PBS Frontline_: the type has the
restraint of a court document; stillness reads as authority. Check: does ANY motion call
attention to itself? If yes, cut it.

**loud** — the bar is a _k-pop lyric video / Nike spot_: type fights the subject and
wins on purpose, color is saturated and scene-true, the beat hits WITH the word. Check:
does the hero frame make you want to replay it?

## The five positive checks (run on the preview sheet, after the failure checks)

1. **Poster test** — screenshot the climax frame alone. Would you post it as a still?
   If it needs the motion to excuse the composition, the composition isn't done.
2. **Timid test** — is any body caption apologizing (tiny, corner-parked, far from the
   silhouette)? Small is a choice; timid is a default. Hug the subject or commit to the
   margin as a designed column.
3. **One-glance hierarchy** — at thumbnail size (shrink the sheet), can you still tell
   opener / body / hero apart? If the tiers blur together, the contrast ratios are off.
4. **Scene handshake** — name three ways the type acknowledges THIS footage (accent
   sampled from the scene, occlusion crossing, shadow direction, depth blur, palette
   temperature). Fewer than two = it's a sticker, not an embed.
5. **Dead-air audit** — scrub the no-caption stretches. Are they _composed rests_
   (subject carries the frame) or _gaps_ (the design just stopped)? Rests are earned by
   rhythm; gaps are bugs in pacing.

## How to use with fresh-eyes review

Give the sub-agent the preview sheet + the 5 failure checks (GUIDE.md § Visual QA) +
these 5 positive checks, and ask for verdicts on both lists. A render ships when it
passes the failure checks AND at least 4/5 positive checks with specific evidence.


<!-- ===== FILE: hyperframes/embedded-captions/references/scene-types.md ===== -->

# Scene Types — picking the right template

The three templates differ in one thing: **what surface (if any) the text physically sits on**. Pick by reading the scene, not by the genre label.

## wall-embed — "text is printed on a real surface"

Original Memory Wall render used this. Text uses perspective transform + `mix-blend-mode: overlay` to look like it was silk-screened onto a wall behind the subject. The illusion is strong when it works and completely broken when forced.

### Four conditions — ALL must hold

1. **A flat or near-flat surface exists somewhere in the frame, larger than the caption block.** Good: acoustic foam panel, painted wall, door, stone facade, large backdrop cloth, blackboard. Bad: bookshelf (3D depth + decorative items), mic shield (too small), window (transparent, content behind it shifts), brick wall with mortar patterns (competes).
2. **The surface is at a non-zero angle to the camera.** Perspective is what sells "embedded". If the wall is perfectly parallel (0° rotation relative to camera), pasting rotateY:0 text onto it looks like a sticker, not embedded. Memory Wall's foam wall was tilted ~13° — perfect. A wall directly behind a centered frontal subject usually has no exploitable angle.
3. **The surface is mid-luminance.** Overlay blend neutralizes mid-tones — text keeps contrast against a mid-grey wall. On near-black surfaces (luminance < 60), overlay makes text vanish → switch to `mix-blend-mode: screen`. On near-white surfaces (> 180), overlay also fails → switch to `mix-blend-mode: normal` with opaque color.
4. **The surface has no competing graphical content.** Plain paint, uniform acoustic foam, blurred OOF background all work. Printed wallpaper, picture frames, text on signage, busy bookshelves all compete with the caption and ruin the embed illusion.

If **any** condition fails, **do not use wall-embed**. Pick another template.

### What memory-wall looked like

The acoustic foam wall to the right of the subject took ~40% of frame width, tilted ~13° toward the viewer, mid-grey color, uniform dimpled texture. Perfect. Text with `rotateY(-13deg)` and overlay blend sat on it like printed letters.

### Anti-examples (wall-embed would FAIL)

- **champion / demo1_avatarv** — bookshelf background with books, white vases, picture frames. Cluttered + 3D depth. Fails condition 1 and 4. Used corner-column-crown instead.
- **Jobs 60 Minutes** — blurry potted plant background. No flat surface at all. Fails condition 1.
- **Randy Pausch "Time is all we have"** — completely black backdrop. No perspective to exploit, no mid-tone surface. Fails 2 and 3. Used portrait-header.
- **Any vlog / selfie with handheld camera** — surface moves frame-to-frame, can't lock perspective. Even if conditions 1-4 hold briefly, motion breaks the illusion.

## corner-column-crown — "text sits in a clean region next to the subject"

The default for most talking-head content. Works when wall-embed doesn't.

### Conditions

1. **Single subject, fixed camera.** Handheld is tolerable if drift is small.
2. **At least one clean zone (≥ 15% of frame width) to the left or right of the subject** where captions can sit without continuous body occlusion.
3. **Background can be cluttered or 3D** — we're not relying on a flat surface, just readable contrast. Screen blend mode picks up darker backgrounds (bookshelves, dark walls) naturally.
4. **Landscape aspect** (16:9 or similar). For portrait, use `portrait-header`.

### When to add the crown vs when to skip it

- Add crown if there's a natural "title drop" line — the one phrase that lands the story (e.g. "WIMBLEDON CHAMPION", "BEATLES", "SHARP AGAIN"). Check [layout-heuristics.md § Crown placement](layout-heuristics.md) for the three geometric conditions.
- Skip crown for factual / neutral monologues where no phrase carries the climax. Short videos (<10s) often don't need it.

## portrait-header — "subject fills center, text lives in top banner"

For 9:16 aspect where the subject inevitably fills the middle.

### Conditions

1. **Portrait aspect** (9:16, 1080×1920 etc.).
2. **Subject occupies the vertical middle of frame**, leaving ~15-25% of the frame height clear at the top.
3. **Optional crown at bottom** — only works if there's also clean space beneath the subject's waist, which is rare in close-crop portrait.

### What to watch

- Subject's head top often approaches y=40 — top banner captions at `top: 30px` will get partially occluded by hair. Accept the partial occlusion (it reads as embed) or bump the caption size down to clear the hair.
- If the subject already has **baked-in captions** (like the burned-in subtitles test case with yellow subtitles burned in), the skill should refuse — two caption systems compete.

## Quick decision flow

```
START
  │
  ├─ Aspect is 9:16 / portrait?
  │    ├─ YES → portrait-header
  │    └─ NO ──▼
  │
  ├─ Does the scene have a flat uniform surface that passes
  │  ALL 4 wall-embed conditions?
  │    ├─ YES → wall-embed
  │    └─ NO ──▼
  │
  ├─ Single subject + fixed camera + ≥15% clean zone on one side?
  │    ├─ YES → corner-column-crown
  │    └─ NO ──▼
  │
  └─ Refuse with reason:
     "No flat surface for embed, no clean caption zone for column.
      Suggest a classic lower-third instead."
```

## Mode checklist (run this before committing to wall-embed)

Read 3 frames (start, mid, end). For each, honestly answer:

- [ ] Is there a single surface behind/beside the subject that occupies ≥ 30% of the frame?
- [ ] Is that surface relatively flat (not curved, not 3D-stacked shelving)?
- [ ] Does that surface angle at 5-20° to the camera (not perfectly parallel, not warped)?
- [ ] Is the surface mid-luminance (not near-black like dark bookshelves, not near-white like a sunny window)?
- [ ] Does the surface contain NO printed/decorative elements that compete with caption text?
- [ ] Does the surface remain visible across all 3 frames (subject doesn't step in front of it)?

**Need all six YES to use wall-embed.** Even one NO → step down to corner-column-crown or portrait-header.


<!-- ===== FILE: hyperframes/embedded-captions/references/typographic-moves.md ===== -->

# Typographic moves — a palette, not a cage

`cinematic-cream` template locks DNA only (font-family, motion, color
palette defaults). It does NOT enforce slot structure. The agent writes
each caption group's typography from scratch via the plan.json `css`
field.

This doc is a **palette** of tried combinations — pick what fits the
scene, invent new ones, skip these if the content demands. These are
recommendations, not rules.

## Size vs text length — DO THIS BEFORE PICKING SIZE

Bigger is NOT better if the word doesn't fit the frame width. Every time
you pick a font-size, sanity-check against word length:

**Rough rule for Inter 900 uppercase at -0.03em tracking:**
`max_font_px ≈ frame_width / (longest_word_chars × 0.72)`

The 0.72 multiplier is intentionally conservative — it targets the text
filling ~90% of the frame width so there's a small side margin. If you
want edge-to-edge, drop to 0.65, but you lose a bit of safety margin.

720px portrait:

- 3-char word (15%): max ~330px (a single big number like "15%")
- 5-char word (TAKE): max ~200px
- 7-char word (AUGMENT / QUANTUM / MATTERS): max ~143px
- 10-char word (CREATIVITY): max ~100px
- 13-char word (UNPRECEDENTED): max ~77px

1920px landscape:

- 7-char word: max ~380px
- 10-char word: max ~267px

For italic/upright 500-700 it's slightly narrower — increase max by ~10%.

**If you want the word bigger than it fits:**

- Split into multiple words per group (natural wrap), OR
- Add explicit `<br>` between syllables, OR
- Drop letter-spacing to -0.05em, OR
- Accept that the matte will cut part of it (Vogue-cover embed effect —
  only works when the cut area is exactly where the subject is)

Never let the text OVERFLOW the frame edge — that's not cinematic, that's
just broken. Use the heuristic.

## Sizing discipline (frame-height-relative)

Portrait 9:16 (720×1290) and landscape 16:9 (1920×1080) have very
different comfort ranges. Use `calc(<pct> * var(--h))` for responsive:

| Feel                   | % of frame height | Example calc            |
| ---------------------- | ----------------- | ----------------------- |
| Whisper / label        | 4-6%              | `calc(0.05 * var(--h))` |
| Soft opener            | 6-9%              | `calc(0.07 * var(--h))` |
| Narrative body         | 9-14%             | `calc(0.11 * var(--h))` |
| Emphasis               | 14-22%            | `calc(0.18 * var(--h))` |
| Climax / monumental    | 22-35%            | `calc(0.28 * var(--h))` |
| Title-bigger-than-face | 40%+              | `calc(0.48 * var(--h))` |

Use absolute px only when a specific scale needs to look identical
across frame sizes (rare). Prefer `calc` + `var(--h)`.

## Named moves — pick per group

**Italic contemplative opener** (memory-wall cap-1 lineage):

```css
font-weight: 600;
font-style: italic;
letter-spacing: -0.01em;
font-size: calc(0.075 * var(--h));
```

**Italic continuation / dreamier continuation** (cap-2 lineage):

```css
font-weight: 500;
font-style: italic;
letter-spacing: -0.005em;
font-size: calc(0.065 * var(--h));
```

**Upright pivot / statement** (cap-3 lineage — "but suddenly"):

```css
font-weight: 700;
letter-spacing: -0.015em;
font-size: calc(0.07 * var(--h));
```

**Uppercase climax / monumental** (cap-4 lineage — "EVERYTHING IS SHARP AGAIN"):

```css
font-weight: 900;
text-transform: uppercase;
letter-spacing: -0.03em;
line-height: 0.95;
font-size: calc(0.18 * var(--h));
```

**Chapter card / full-frame Adam Curtis manifesto**:

```css
font-weight: 700;
text-transform: uppercase;
letter-spacing: -0.015em;
line-height: 0.9;
font-size: calc(0.14 * var(--h));
```

**News chyron / broadcast label** (small, locked):

```css
font-weight: 500;
letter-spacing: 0.02em;
font-size: calc(0.038 * var(--h));
```

**Tiny side note / caption-on-surface**:

```css
font-weight: 400;
font-style: italic;
font-size: calc(0.045 * var(--h));
```

**Vogue-masthead monumental**:

```css
font-weight: 900;
text-transform: uppercase;
letter-spacing: -0.04em;
line-height: 0.85;
font-size: calc(0.32 * var(--h));
```

## Narrative arcs (suggestions, not required)

**Poem arc** — memory-wall canonical: italic opener → italic continuation
→ upright pivot → uppercase climax. Four steps.

**Question-answer arc**: italic question small → uppercase answer big.
Two steps.

**List-of-three arc**: three equal-weight narration segments, one
climactic uppercase. Four steps.

**Single-statement arc**: one monumental uppercase held long. One step.

**Whisper-hook arc** (short-form): tiny italic hook → massive uppercase
reveal. Two steps.

The **number** of groups comes from the **content**. A 25s Pausch talk
has ~8 beats. A 7s TikTok hook has 2-3 beats. Don't force 4 or 5 or 7 —
read the transcript and mark breath-groups.

## Position + layer vocabulary

**Position** is where the caption lives in frame. Use:

- `top / left / right / bottom` (percentages or px) for anchor
- `transform: translateX/Y` for fine offsets
- `text-align: center / left / right` for alignment

**Layer** per group:

- `bg` (default) — behind subject. Matte occludes. Cinematic embed. Works
  on clean zones (sky, walls) OR intentionally crosses subject for the
  Vogue-masthead effect.
- `fg` — on top of subject. Announcement. Use for climax breakthroughs or
  when bg would be 100% occluded by body.

**Tone** per group:

- `soft` — gentle per-word opacity+y drift (0.45s power2.out). Use for
  introspective, dreamy, or narrative content.
- `present` — snappy per-word opacity+y+scale pop (0.22s power3.out). Use
  for emphatic or declarative beats.

## Anti-patterns the DNA protects against

The DNA defaults prevent most ugly outcomes. But avoid in per-group CSS:

- Multiple different `font-family` within one video (DNA is one family)
- Multiple saturated colors (one accent at most; DNA defaults cream or
  deep warm)
- `letter-spacing` above ±0.05em unless there's a specific reason
- `font-weight` 300 or below — too light for screen
- `font-style: italic` on emphasis — italic is for lyricism, not stress

## When cinematic-cream is wrong

This DNA assumes mid-to-dark backgrounds (luminance 60-180). For:

- Bright white studios → cinematic-cream's cream + `screen` washes out, and the DNA is
  **locked** (you cannot recolour it) → use **Standard mode** (opaque rail) instead
- Documentary formal → Standard mode (documentary-dignified direction; see references/direction-catalog.md §1)
- Energetic vlog hooks → future `kinetic-vlog` DNA (not yet shipped)

## Example: memory-wall original, expressed in freeform

Same output as the canonical memory-wall.html, but using slot-free plan:

```json
{
  "template": "cinematic-cream",
  "caption_layer": "bg",
  "groups": [
    {
      "id": "cg-0",
      "tone": "soft",
      "in": 0.2,
      "out": 4.85,
      "css": "top: 14%; right: 6%; left: auto; text-align: right; font-size: calc(0.09 * var(--h)); font-weight: 600; font-style: italic; letter-spacing: -0.01em;",
      "words": [
        { "text": "Some", "start": 0.24, "end": 0.44 },
        { "text": "memories", "start": 0.48, "end": 0.82 },
        { "text": "feel", "start": 0.92, "end": 1.14 },
        { "text": "soft", "start": 1.2, "end": 1.64 }
      ]
    },
    {
      "id": "cg-1",
      "tone": "soft",
      "in": 2.55,
      "out": 4.85,
      "css": "top: 26%; right: 10%; left: auto; text-align: right; font-size: calc(0.075 * var(--h)); font-weight: 500; font-style: italic;",
      "words": [
        { "text": "like", "start": 2.66, "end": 2.78 },
        { "text": "old", "start": 2.88, "end": 3.02 },
        { "text": "film", "start": 3.16, "end": 3.46 }
      ]
    },
    {
      "id": "cg-2",
      "tone": "present",
      "in": 4.9,
      "out": 8.04,
      "css": "top: 18%; right: 6%; left: auto; text-align: right; font-size: calc(0.085 * var(--h)); font-weight: 700;",
      "words": [
        { "text": "but", "start": 5.04, "end": 5.18 },
        { "text": "suddenly", "start": 5.24, "end": 5.76 }
      ]
    },
    {
      "id": "cg-3",
      "tone": "present",
      "in": 6.7,
      "out": 8.04,
      "css": "top: 32%; right: 6%; left: auto; text-align: right; font-size: calc(0.11 * var(--h)); font-weight: 900; text-transform: uppercase; letter-spacing: -0.03em; line-height: 0.95;",
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

Same visual, no slot constraint. Each group owns its typography.


<!-- ===== FILE: hyperframes/embedded-captions/references/typography-presets.md ===== -->

# Typography Presets

Five named styles corresponding to the `cap-*` CSS classes. Pick one per caption group in `plan.json` based on the line's semantic role.

| style    | CSS                         | Use when                                                                                                                  |
| -------- | --------------------------- | ------------------------------------------------------------------------------------------------------------------------- |
| `intro`  | 66px italic 500             | First line, filler ("You know…", "So…"), contemplative openings. Low visual weight.                                       |
| `phrase` | 78px upright 600            | Main statement clauses. Default for most lines.                                                                           |
| `emph`   | 92px upright 800            | Lines with emotional peak or key achievement ("I've achieved incredible things").                                         |
| `dream`  | 82px italic 700             | Aspirational / "was dreaming of…" style lines. Italic signals memory/imagination.                                         |
| `crown`  | 140px upright 900 uppercase | **Only for the climax line.** Used in center-stage `crown-plane`. Maximum one per composition — ideally the last caption. |

## Tone field

Independent of style, each group has `tone`: `soft` or `present`.

- **soft** — gentle fade + 8px y-drift entrance, `power2.out` ease. Feels floaty, nostalgic. Use for memory, intro, dream.
- **present** — snappy 6px y + 1.04 scale pop, `power3.out`, transformOrigin center. Feels assertive, in-the-moment. Use for emphasis and crown.

## Picking automatically

Scan each group's words:

1. Does it contain superlatives (incredible, best, only, never, always) or brand/proper nouns? → `emph` + `present`
2. Does it start with discourse markers (you know, so, well, look) or is it short (≤3 words)? → `intro` + `soft`
3. Does it reference dreams, hopes, memory, past tense verbs like "was dreaming"? → `dream` + `soft`
4. Is it the final sentence-clinching line and feels like a title/headline? → `crown` + `present` (only one per video)
5. Otherwise → `phrase` + (match the group's neighbors' tone; default `soft`)

## Font-size scales with column width

The `.cap-*` defaults in each template are tuned for a **~560px column** (the original champion composition). When the caption plane is wider than that, the fonts feel underweight — too much negative space around text. Scale up accordingly.

| Plane width         | intro | phrase | emph | dream | crown (centered, full-frame) | crown (clean-zone only) |
| ------------------- | ----- | ------ | ---- | ----- | ---------------------------- | ----------------------- |
| 460-580 px (tight)  | 66    | 78     | 92   | 82    | 140                          | n/a                     |
| 600-760 px (medium) | 78    | 108    | 128  | 100   | 220                          | 118                     |
| 780+ px (wide)      | 90    | 128    | 150  | 116   | 260                          | 140                     |

Notes:

- Crown sizes assume landscape (1920×1080). For portrait 1080×1920, divide all crown sizes by 1.5.
- "full-frame crown" = centered, designed to span `0.8+ × frame_width` and cross the subject's body. Use only when [layout-heuristics.md § Crown placement](layout-heuristics.md) conditions pass.
- "clean-zone only crown" = crown positioned inside one clean zone, smaller font, tail letters lightly touch subject. Fallback when centered crown would eat too much.

Also: if a plane's `rotateY` is non-trivial (say > 8°), effective visible width shrinks. Scale fonts up ~10% to compensate.

## What NOT to do

- Don't use more than **one crown** per render. The whole point is that it's a singular payoff.
- Don't use `emph` on more than ~30% of groups. Emphasis loses meaning when everything is emphasized.
- Don't pick `intro` for the main content just because the words are short. "I won" (2 words) is `emph` or `crown`, not `intro`.
- Don't mix `soft` and `present` alternately for no reason. Tone should follow the story arc: soft opening → present build → emph peak → (optional crown climax).

## When scene luminance affects color choice

The default color is warm bone-white (`#fff5df`). Adjust in the template CSS:

- Wall is mostly warm wood / tan → keep default, or shift cooler `#e8f0ff`
- Wall is cool blue / tech-lab → push warmer `#fff0c0`
- Wall has strong primary color → desaturate default, luminance first

These adjustments happen in the HTML template, not plan.json. If you repeatedly need different palettes, make new template variants.
