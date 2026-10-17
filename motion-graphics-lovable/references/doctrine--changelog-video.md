

<!-- ===== FILE: doctrine/changelog-video/GUIDE.md ===== -->

---
name: changelog-video
description: Turn a weekly changelog .md into a finished branded changelog video (square 1080, ~45-60s, Annie VO, animated brand background, mock-UI visualizations, lowkey captions). Use when the user provides a changelog/digest markdown and wants the weekly video, or says "changelog video". Self-contained — fonts, background, lexicon, and scripts ship in this skill.
metadata:
  internal: true
---

# Changelog → Branded Video

Input: a changelog .md (themes + items, like the weekly HyperFrames digest).
Output: a lint-clean, seam-gate-green HyperFrames project in
`projects/active/weekly-changelog-<range>/`. Render only when asked.

**Load first, non-negotiable:** `motion-doctrine` (+ `cut-the-curve`,
`oversized-cursor` if a cursor appears, `seam-craft`) and `captions-overlay`.
This skill supplies the changelog-specific pipeline; the doctrine supplies the
motion law.

## The prime directive: visualize, don't list

Every theme is illustrated by an **animated mock of the actual UI or a
faithful analog** acting out the change in experience — never text bullets.
Route every theme/item through `references/visualization-registry.md` BEFORE
writing the script; the registry decides ui-recreate / ui-analog / terminal /
checklist. Text checklist is the LAST resort, reserved for genuinely
non-visual items (reliability fix lists).

## Pipeline

### 0 · Bootstrap the project from THIS skill's assets — non-negotiable

**Do this before writing any composition HTML. Skipping it always produces a video that looks like a similar project you built before, NOT this skill's brand — that's the single most common way this skill goes off-brand.** The skill's assets, fonts, and scaffold are the skill; the GUIDE.md prompt is a router.

```bash
mkdir -p project/assets/fonts
cp <SKILL_DIR>/assets/fonts/*.woff2 project/assets/fonts/
cp <SKILL_DIR>/assets/bgm.mp3 project/bgm.mp3
ffmpeg -y -stream_loop 15 -i <SKILL_DIR>/assets/bg-pattern.mp4 -t <TOTAL> \
  -vf "scale=1080:1080,fps=30,eq=saturation=0.72,drawbox=c=black@0.5:t=fill" \
  -an -c:v libx264 -crf 20 -pix_fmt yuv420p project/assets/bg-pattern-<TOTAL>s.mp4
cp <SKILL_DIR>/examples/master-skeleton.html project/index.html
```

Then **read `references/build-spec.md` end-to-end** (not skimmed) — it defines the brand tokens (TT Norms Pro + ABC Solar Display + TT Norms Mono, cream `#f5f6f4`, rationed green `#5ef17c`, glass cards with green-tinted borders, kicker/sec-chip pill shape, 32px caption rail at `top: 990`) that every scene inherits from the scaffold.

Only THEN begin steps 1-6 below. Steps 1-4 (parse, route, script, VO) plan what goes into the scaffold; step 5 fills placeholders (`<RANGE>`, `<TOTAL>`, `<CUT_N>`, `<DUR_N>`, scene bodies) inside the already-copied `project/index.html` — you do NOT rewrite the scaffold's chrome, fonts, palette, or layout shell.

If you catch yourself reaching for `cp` on a prior video's `index.html`, or writing your own `@font-face` declarations, or designing a WebGL shader background instead of using the encoded bg-pattern MP4 above: STOP. Delete the current `index.html` and restart at the `cp` of the master-skeleton scaffold. Rebuilding scene content on the right scaffold is cheaper than retrofitting brand into the wrong scaffold.

### 1 · Parse + editorial cut

- Extract: week range, headline stats (releases, commits), themes, items.
- **Budget: 45-60s total.** Title ≤2s, outro ≤3.5s, 4 themes ≈ 9-12s each.
- Per theme keep ONE hero visualization + at most 3 spoken items. Everything
  else exists only as the outro's "full digest" pointer. Cutting is the job:
  a changelog with 30 items still yields ≤14 spoken beats.
- Order themes by story: marquee feature → product surface → performance →
  reliability (the digest usually already reads this way).

### 2 · Visualization routing

For each theme, pick the surface from `references/visualization-registry.md`
and write one line: `theme → surface → the 2-4 sequenced actions the mock
performs, each tied to a script phrase`. If no registry surface fits and no
faithful analog exists, it's a checklist scene — don't invent fake UI for
something we can't represent honestly.

### 3 · Two-layer script (spoken vs display)

Write the script as **token lines** per `references/script-voice.md`:
conversational register, every technical term carrying a `spoken` phonetic
form from `references/lexicon.json` while `display` keeps standard spelling.
Captions show `display`; the VO reads `spoken`. Any term not in the lexicon:
STOP and ask the user how it's pronounced, then add it to the lexicon.
Save as `script-tokens.json` in the project.

### 4 · VO — Annie (HeyGen, pinned)

```bash
# spoken-layer text only; words JSON = ground-truth timestamps of the SPOKEN text
# Repo-native path: the changelog-video skill runs from the hyperframes repo root,
# so it uses the tracked hyperframes-media TTS helper directly (no `npx hyperframes
# skills` install step). If you've copied the skill into another repo, swap in
# your own path to the media-use / hyperframes-media heygen-tts.mjs.
node skills/hyperframes-media/scripts/heygen-tts.mjs ./vo-spoken.txt \
  -o voiceover.mp3 --words vo-words.json \
  --voice 330290724a1b470fb63153f34d4c0183   # Annie — lifelike (do not substitute)
```

Requires `heygen` CLI ≥0.3.0 authenticated (`heygen auth login --oauth`).
Then align spoken timestamps back to display tokens:

```bash
node <SKILL_DIR>/scripts/align-captions.mjs \
  --tokens script-tokens.json --words vo-words.json --out captions.json
```

`captions.json` is the caption-rail input (display spelling, spoken timing).
The aligner prints `MISMATCH` warnings — resolve every one before building
(usually a lexicon spelling the TTS renders as multiple words). **The audio
is the clock**: all beat times come from `vo-words.json`; a VO regen re-opens
every seam.

**Word-timings are a hard gate.** Before moving on to step 5, verify
`vo-words.json` is non-empty and has a `words: [...]` array with `start`/`end`
per word. If it's empty (0 bytes) or missing the array — a known failure mode
when the TTS provider returns audio but no timestamp payload — DO NOT proceed
without them. Fallback: forced-align the produced audio against the display
script using local whisper:

```bash
uvx --from openai-whisper whisper voiceover.mp3 \
  --model base.en --language en --word_timestamps True \
  --output_format json --output_dir .
# then run align-captions.mjs with --words voiceover.json (same shape)
```

Whisper mishears TTS renderings ("gee-sap" → "gsap", "heyjen" → "hey Jen",
etc.) — captions still use the DISPLAY spelling from `script-tokens.json`;
whisper only supplies the timestamps. `align-captions.mjs` handles the join.
This fallback is the difference between a captioned build and a silently
uncaptioned one.

### 5 · Build

Follow `references/build-spec.md` exactly: brand tokens + fonts (bundled in
`<SKILL_DIR>/assets/`), the animated background encode, scene scaffold,
chrome, caption rail, one rationed green moment per scene. Then the doctrine
order: `ledger.json` (all ordinary seams cut-the-curve LEFT) → seam-stamp →
internal beats on VO words → seam-gate verify.

**Captions are non-optional.** The master-skeleton ships a caption-rail IIFE
that reads a `LINES` array — leaving that array empty is a shipped bug, not a
style choice. Populate it from `captions.json` before proceeding to step 6:

```javascript
// paste in place of "const LINES = /* … */ []" in the caption-rail IIFE:
const LINES = /* contents of captions.json */ [
  { id: 0, end: 2.74, w: [["This", 0.0], ["week,", 0.30], …] },
  …
];
```

If `align-captions.mjs` was skipped or `LINES` is `[]`, the frame check in
step 6 will fail — do not paper over it by removing `#cap-line` from the
scaffold.

### 6 · Gates (all green before presenting)

1. `node packages/cli/bin/hyperframes.mjs check --caption-zone "x0=0;y0=.90;x1=1;y1=1;severity=error;seek=.02,.06,.10,.14,.18,.22,.26,.30,.34,.38,.42,.46,.50,.54,.58,.62,.66,.70,.74,.78,.82,.86,.90,.94,.98"` (or the installed
   `hyperframes` CLI from the repo-local `skills/hyperframes-cli/` skill) —
   0 errors (contrast: dim text ≥ .66 alpha; scene content stays above the
   caption rail). Do NOT reach for
   `npx hyperframes@latest`; the tracked repo-local CLI is the source of
   truth for the composition contract this skill produces against.
2. `seam-gate.mjs verify` — 0 fail.
3. Restart the preview server (it caches the bundle), spot-check 3-4 beats
   via `__player.seek` on the raw comp page.
4. Do NOT render unless the user asks. After a requested render, verify
   frames from the MP4 (`ffmpeg -ss <t> … -frames:v 1`): captions present,
   background video not black, no tiny/frozen frames.
5. **Caption presence gate — hard fail.** Sample 3-4 frames spread across
   the VO's spoken window (e.g. `t=3`, `t=15`, `t=30`, `t=42` for a 48s VO)
   and confirm the caption rail at `top: 990` renders visible text on each.
   If any frame in a spoken interval is missing captions, the build ships
   uncaptioned — treat it as a red gate and re-check step 5's `LINES`
   population. This is exactly what went wrong on the Jul 13-20 v4 build.

## Project layout

```
projects/active/weekly-changelog-<range>/
├── index.html            # single-doc master (scenes as slides, stamped seams)
├── ledger.json           # vector ledger (seam-stamp input)
├── script-tokens.json    # two-layer script (source of truth for VO + captions)
├── vo-spoken.txt         # generated: spoken layer, one line
├── voiceover.mp3 + vo-words.json + captions.json
├── bgm.mp3               # copy from <SKILL_DIR>/assets/bgm.mp3 (the house track) unless the user supplies one
└── assets/fonts/ + assets/bg-pattern-<dur>s.mp4
```

## Anti-patterns

| Don't                                                 | Instead                                                                                                                                                                                          |
| ----------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| Bullet-point slides for UI changes                    | Mock the surface acting out the change                                                                                                                                                           |
| Fake UI for un-representable items                    | Honest checklist scene                                                                                                                                                                           |
| Plain "JSON"/"CLI" in the TTS text                    | Lexicon spoken forms; display stays standard                                                                                                                                                     |
| Phonetic spellings in captions                        | Captions always render the display layer                                                                                                                                                         |
| Guessing an unknown term's pronunciation              | Ask, then grow the lexicon                                                                                                                                                                       |
| Speaking every changelog item                         | ≤3 per theme; the digest link carries the rest                                                                                                                                                   |
| Green accents everywhere                              | One green moment per scene (#5ef17c)                                                                                                                                                             |
| Starting from a prior video's index.html              | Step 0 — copy `examples/master-skeleton.html` from this skill into `project/index.html`, always                                                                                                  |
| Hand-crafted `@font-face` / WebGL shader / custom BGM | Step 0 — copy this skill's `assets/` verbatim; the skill's assets ARE the brand                                                                                                                  |
| Delivered without CloudFront invalidation             | Run `aws cloudfront create-invalidation` on distribution `E2BSLVSZ7FG3U0` for the exact path after any S3 replace — CDN caches the old file otherwise                                            |
| Shipping with the `LINES` array empty in the scaffold | Step 4 must produce a populated `captions.json`; step 5 must paste it into the IIFE; step 6 gate 5 must confirm captions on rendered frames. An empty `LINES` = uncaptioned ship = re-do the run |
| No `vo-words.json` → skip captions and ship anyway    | Fall back to whisper forced alignment on the produced audio; captions are non-optional                                                                                                           |


<!-- ===== FILE: doctrine/changelog-video/references/build-spec.md ===== -->

# Build Spec — square 1080 changelog master

Single-doc `index.html`: scenes are absolutely-positioned `.slide` clips on
track 1; the master timeline `tl` (MUST be named `tl` — seam-stamp emits
`tl.*`) is paused, padded to total duration, registered as
`window.__timelines["main"]`. See `examples/master-skeleton.html` for the
verbatim scaffold.

## Brand tokens (HeyGen for Developers)

```css
@font-face {
  font-family: "ABC Solar Display";
  font-weight: 700;
  src: url(assets/fonts/ABCSolarDisplay-Bold.woff2) format("woff2");
}
@font-face {
  font-family: "TT Norms Pro";
  font-weight: 400;
  src: url(assets/fonts/TT_Norms_Pro_Normal.woff2) format("woff2");
}
@font-face {
  font-family: "TT Norms Pro";
  font-weight: 500;
  src: url(assets/fonts/TT_Norms_Pro_Medium.woff2) format("woff2");
}
@font-face {
  font-family: "TT Norms Pro";
  font-weight: 700;
  src: url(assets/fonts/TT_Norms_Pro_Bold.woff2) format("woff2");
}
@font-face {
  font-family: "TT Norms Mono";
  font-weight: 400;
  src: url(assets/fonts/tt_norms_pro_mono_regular-webfont.woff2) format("woff2");
}
/* ink #f5f6f4 · ink2 rgba(245,246,244,.72) · dim rgba(245,246,244,.66) —
   NOT .45: the contrast gate fails small text under 4.5:1 over the glass.
   green #5ef17c (RATIONED: one moment per scene) · bg #0a0c0b ·
   chip-bg rgba(10,12,11,.78) · glass-line rgba(190,255,205,.32) */
```

Copy fonts from `<SKILL_DIR>/assets/fonts/` into the project's
`assets/fonts/` (local @font-face with format('woff2') embeds at render).
Glass card: chip-bg fill, 1px glass-line border, radius 22,
`box-shadow: 0 24px 60px rgba(0,0,0,.5)`. NO backdrop-filter. Chips: mono
18-22px, radius 12, 1px rgba(255,255,255,.14) border on rgba(255,255,255,.05).
Display type: ABC Solar Display 700. Body: TT Norms Pro. Everything
code/UI-label: TT Norms Mono. Safe margins x/y ∈ [76, 1004].

## Animated background (the house pattern)

Encode the bundled source to the film's exact duration — the render
compiler shortens a video's slot to the media length, so the encode must be
≥ total:

```bash
ffmpeg -y -stream_loop 15 -i <SKILL_DIR>/assets/bg-pattern.mp4 -t <TOTAL> \
  -vf "scale=1080:1080,fps=30,eq=saturation=0.72,drawbox=c=black@0.5:t=fill" \
  -an -c:v libx264 -crf 20 -pix_fmt yuv420p assets/bg-pattern-<TOTAL>s.mp4
```

Keep the darkening crush — the raw pattern is far too loud. Mount as
`<video id="bg-video" class="clip" muted>` on track 0 + a static
`rgba(8,10,9,.25)` scrim div. `<video>` needs the id (silent/black
otherwise) and must stay flat 2D (no 3D ancestors).

## Scene anatomy

- Chrome (untimed, z 6): kicker chip top-left `HYPERFRAMES WEEKLY · <RANGE>`,
  progress dots top-right (one per theme; `tl.set` backgroundColor at each
  cut — active #f5f6f4, done .45; never tl.call for state).
- Title (≤2s): mono kicker date, ABC Solar h1 ~104px, green rule sweep.
- Theme scene: sec-chip `0N · THEME NAME` (top 128) + ABC Solar headline
  ~54px (top 186) + the mock (from the visualization registry) filling
  y ∈ [288, 944].
- Outro (≤3.5s): kicker FULL DIGEST, "See what shipped." ~96px, green rule,
  mono URL chip, tag line. Fade all + chrome ~0.5s before end.
- Caption rail per `script-voice.md` (top: 990, font-size: 32px, height: 52). Mandatory — populate the master-skeleton's `LINES` array from `captions.json` before render; see GUIDE.md step 5.

## Seams + internal life (doctrine mechanics)

- `ledger.json`: every ordinary seam `cut-the-curve LEFT` (x, dir −1), exit
  and entry selectors = the inner `.swrap` wrappers (`#w-*`), NEVER the `#s-*`
  clip element — `gsap_animates_clip_element` is an error-severity lint rule and
  every stamped seam writes `autoAlpha`. Outro entry `travel: 8`.
- `seam-stamp.mjs --ledger ledger.json --write index.html` owns ALL wrapper
  entries/exits — author none yourself. Title (film open) authors its own
  entry only, and that entry MUST pass `immediateRender: false`: the stamped
  zero-duration `tl.set(autoAlpha: 0)` at the title's cut renders at BUILD time,
  so an entry without the flag captures 0 as its start and tweens 0 → 0. The
  symptom is `exit-visible … op 0.00` with `exit-vector` PASSING — moving but
  invisible. Neither a CSS opacity base nor a longer clip window fixes it.
- Slides: the `.swrap` carries the CSS `opacity: 0` base, not the `.slide` clip
  element; `data-start` = exactly the cut time.
- Each scene's shell (chip, headline, mock chrome, initial state) is
  COMPOSED at local t=0 — the wrapper flies it in. Internal reveals start
  ≥0.4s after the cut and end ≥0.45s before the next cut (stamped exits
  begin at cut −0.34s).
- Every internal beat lands on a VO word from `vo-words.json`. Name each
  scene's sustained-motion route in the plan (sequenced UI life for mocks,
  staged reveals for checklists). One green moment per scene.
- Init states via `gsap.set(...)` at build time; animation via sequential
  `tl.to(...)` only (no plain-object keyframes, no repeat:-1, no tweening
  left/top — set base position in CSS, tween x/y). Counters: object tween
  with an `onUpdate` in the tween config (cache DOM refs; never
  `tl.eventCallback`).

## Lint/check gotchas (all hit before, all pre-solved)

- Mock containers with intentional stacking: `data-layout-allow-overlap` on
  each text block that deliberately participates, never on the slide root;
  elements a playhead/line crosses: `data-layout-allow-occlusion`.
- Dim text: `rgba(245,246,244,.66)` minimum (contrast gate).
- Audio: every `<audio>` carries an `id`. BGM: the house track ships at
  `<SKILL_DIR>/assets/bgm.mp3` (159s instrumental) — copy it to the project
  as `bgm.mp3` and mount on its own track:
  `<audio id="bgm" src="bgm.mp3" data-start="0" data-duration="<TOTAL>" data-track-index="2" data-volume="0.14" data-media-start="0">`
  (0.14 sits under the VO; use a user-supplied track only when given one).
- Preview server caches the bundle — RESTART after edits, then verify on the
  raw comp page (`/api/projects/<id>/preview/comp/index.html`) via
  `window.__player.seek(t)`.


<!-- ===== FILE: doctrine/changelog-video/references/script-voice.md ===== -->

# Script + Voice: the two-layer contract

The script is the single source of truth for BOTH the VO and the captions,
written as token lines. The VO reads the `spoken` layer; captions render the
`display` layer. This is a hard quality gate: a caption showing "jay-sawn" or
a VO saying "juh-son" ("JSON" read literally) are both build failures.

## Register (how it should sound)

- Conversational, not release-notes. "The big one this week —" beats
  "Theme 1:". Contractions welcome. Second person allowed ("your clips").
- Informational, never salesy; no superlatives the changelog doesn't earn.
- One breath per beat: sentences ≤ ~14 words; let punctuation pace the read.
- Numbers with meaning stay ("fifteen releases"); commit hashes, PR numbers,
  and version micro-detail are never spoken.
- Open with the week + the marquee, close with the digest pointer
  ("See everything at hyperframes dot heygen dot com").
- **Teach the simple command.** When a feature has a one-line invocation (a
  slash command, a CLI one-liner), the script says it verbatim ("start your
  prompt with /figma…") and the mock shows it being typed — the command is
  the visible CAUSE of the result. Slash commands speak as "slash <name>",
  caption as `/name`.

## Token-line format (`script-tokens.json`)

```json
{
  "lines": [
    {
      "id": "l1",
      "tokens": ["This", "week", "at", "HyperFrames,", { "display": "JSON", "spoken": "jay-sawn" }]
    }
  ]
}
```

- A bare string = display and spoken identical.
- An object = the layers diverge. `display` keeps standard spelling AND the
  punctuation captions should show; `spoken` is what the TTS reads.
- One line = one caption phrase (≤ ~40 chars of display text). Line grouping
  is an authoring decision made here, not downstream.
- Build `vo-spoken.txt` by joining every token's spoken form with spaces,
  lines joined into sentences/paragraphs as punctuated.

## Phonetics rules (ElevenLabs-style best practices, plain-text)

HeyGen TTS takes plain text (no SSML), so pronunciation is controlled by
spelling, hyphens, and spacing:

1. **Initialisms** (each letter said): space or hyphen the letters —
   `CLI → "C L I"`, `CDP → "C D P"`, `API → "A P I"`.
2. **Acronyms said as words**: respell phonetically —
   `JSON → "jay-sawn"`, `GSAP → "jee-sap"`.
3. **Mixed / pronounceable compounds**: hyphenated LOWERCASE phonetics, one
   fluid run — `ffmpeg → "ff-mpeg"` (ear-tested; the TTS reads "ff" as a
   fluid "eff-eff"), `WebM → "web em"`, `OAuth → "oh-auth"`. Never spaced
   capitals here: the TTS reads spaced caps as isolated letter names with
   hard stops ("F F em-peg" comes out "eff… eff… em-peg"). Reserve spaced
   capitals for TRUE initialisms (CLI, API) where a deliberate
   letter-by-letter read is the goal. When candidates are close, generate
   A/B takes of the real sentence and let the user pick by ear.
4. **Versions/numbers**: expand — `v0.7.36 → "version zero point seven
point thirty-six"` (usually: don't speak versions at all),
   `1080×1080 → "ten-eighty by ten-eighty"`.
5. **URLs**: `hyperframes.heygen.com → "hyperframes dot hey-jen dot com"`.
6. **Filenames/extensions**: `.mp4 → "dot em pee four"` — or rephrase so the
   extension isn't spoken.
7. **Emphasis/pauses**: commas and em-dashes, never caps. Ellipses are
   unreliable in TTS — use an em-dash.

The shared vocabulary lives in `references/lexicon.json`
(`display → spoken`). Consult it for EVERY technical term; if a term is
missing, ask the user for the pronunciation and add the entry — never guess,
never ship unheard. New entries: listen to that line in the generated VO
before accepting.

## Alignment (spoken timestamps → display captions)

`heygen-tts.mjs --words` returns word timestamps of the SPOKEN text.
`scripts/align-captions.mjs` walks the spoken stream against the token lines
(one display token may cover several spoken words — "C L I" is three) and
emits `captions.json`:

```json
{
  "lines": [
    {
      "end": 3.1,
      "w": [
        ["This", 0.22],
        ["week", 0.4],
        ["JSON", 1.1]
      ]
    }
  ]
}
```

Each display word carries the start time of its FIRST spoken word; a line's
`end` = the next line's start (last line: last word end + 0.6). The aligner
warns `MISMATCH` when the heard word doesn't fuzzy-match the expected spoken
form — every warning must be resolved (fix the lexicon spelling or the
transcript) before the captions are trusted.

## Caption rail (rendering)

Per `captions-overlay`: a quiet OVERLAY, never a reserved band. One line,
bottom-center (top: 990px, height: 52px on 1080-square), TT Norms Pro 500 32px,
ink .94, soft dark text-shadow, words fading in (0.12s) on their timestamps,
phrase swaps as sets. Keep critical small text out of the bottom ~100px
center span; everything else may run under the rail.


<!-- ===== FILE: doctrine/changelog-video/references/visualization-registry.md ===== -->

# Visualization Registry

The routing table for "show, don't tell". Classes, strongest first:

1. **ui-recreate** — the change lives in a surface we can faithfully mock.
2. **ui-analog** — no exact surface, but an honest UI metaphor exists
   (panel, meter, pipeline) whose behavior IS the change.
3. **terminal** — the change is a CLI command/flag; type it, show the result.
4. **checklist** — non-visual (fix lists, dependency bumps). Last resort.

Never invent UI that implies a screen that doesn't exist — an analog must
depict the _behavior_ (speed, batching, caching), not a fake product page.

## Known surfaces (ui-recreate)

| Surface                      | Mock anatomy                                                                                                                                            | Proven choreography                                                                                                                                                |
| ---------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| **Studio editor / timeline** | glass app frame: titlebar (traffic dots, mono app name, Export pill), preview strip w/ gradient art, ruler + ticks, lanes, playhead, mono-labeled clips | clips drop/stack into lanes; drag→edge/playhead snap w/ green snap-line flash; marquee → group move → group resize; playhead scrub drives preview art (hue-rotate) |
| **Inspector / design panel** | panel: MONO section headers (INSPECTOR / VARIABLES), key-value rows, hairline dividers, dashed empty slot                                               | binding pill (`{{ var }}`) flies into a property slot; value swap via masked slide (old up-out, new up-in); selection box draws on canvas                          |
| **Canvas + element**         | mini stage card, dashed selection box, live text element                                                                                                | text updates same-frame with panel edits (green underline pulse = the live-preview moment)                                                                         |
| **Variant renders**          | small cards: display-font title + mono filename                                                                                                         | cascade out diagonally, stagger ≤0.15s                                                                                                                             |
| **Storyboard view**          | row of scene thumbnails w/ mono scene labels                                                                                                            | thumbnails file in as a waterfall; one gets dragged to reorder                                                                                                     |
| **Terminal / CLI**           | glass strip, mono 19-20px, `$ ` prompt dim                                                                                                              | chars type (stagger .02), result line lands after a 0.3-0.5s beat                                                                                                  |
| **Render panel**             | RENDER header, big tabular-nums frame counter, progress bar (green fill = the moment), status chips                                                     | bar + counter run with `power2.in` (slow→fast reads as "faster"); chips land on their VO words                                                                     |

## Proven analogs (ui-analog)

| Change type                                  | Analog                                                                                                                               | Behavior                                                                                                                    |
| -------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------ | --------------------------------------------------------------------------------------------------------------------------- |
| Color grading / LUT                          | slider rows (label + track + knob) beside footage art                                                                                | each knob move re-filters the art SAME frame (causal)                                                                       |
| Render/extraction speed                      | render panel counter + bar                                                                                                           | ease tells the story; add a before/after time chip if the claim is numeric                                                  |
| Batching (frames, requests)                  | row of small ticks                                                                                                                   | brackets draw around groups; ticks nudge into clusters                                                                      |
| Caching                                      | two identical request rows                                                                                                           | first row runs a full bar; second short-circuits instantly to ✓ with a `cache` chip                                         |
| Import/translation pipelines (e.g. Figma→HF) | source artifact card morphs/docks into a HF comp card — a pure DOM/CSS mock of the source (NO Figma API, no tokens, nothing fetched) | staged: source card → arrow/flight of extracted chips (tokens, components, motion) → assembled comp; chips are the carriers |
| One-pass / dedupe                            | N parallel item rows collapse onto one shared lane                                                                                   | rows glide onto one bar; count chip decrements                                                                              |
| Concurrency caps / locks                     | queue of chips entering a gate                                                                                                       | first k pass, rest hold; gate chip shows the cap                                                                            |
| Error surfacing (toast, reason)              | the surface's corner grows a toast card                                                                                              | action fails subtly → toast slides in, mono reason text                                                                     |

## Checklist scene (last resort)

Glass card, ≤6 mono rows, green ✓ ticks landing on each item's VO word
(back.out(1.5), 0.3s) + row brightness pulse. Items beyond 6: cut, they live
in the digest link.

## Adding a surface

When a new UI area ships, add a row here (anatomy + choreography) the first
time it's mocked, so the next changelog reuses it instead of re-deriving it.
