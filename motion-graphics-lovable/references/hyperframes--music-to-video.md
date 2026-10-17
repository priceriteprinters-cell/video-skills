

<!-- ===== FILE: hyperframes/music-to-video/GUIDE.md ===== -->

---
name: music-to-video
description: "Turn a music track (an audio file, a video to pull audio from, or a track generated from a mood brief) into a beat-synced video — lyric video, slideshow, or kinetic promo. The music drives all pacing; any user-supplied images/videos are cut onto the same beat grid, and a complete video needs zero assets. Narrated pieces → the input-matched workflow (see /hyperframes). Unclear → /hyperframes."
---

**Plugin installs:** Before setup or freshness commands, follow [plugin execution rules](../hyperframes/references/plugin-installation.md) when this skill is inside a HyperFrames plugin. Standalone installs keep the update instructions below.

> **First, keep this skill fresh — confirm with the user before running:** `npx hyperframes skills update music-to-video`. A fast no-op when everything is current; otherwise it refreshes this skill plus the core domain skills it depends on before you rely on them.

# music-to-video — one music-grounded, beat-synced video workflow

Use this skill to turn a **music track** into a beat-synced HyperFrames video. You analyze the track once, lay out the frames, fill in a per-frame plan, and build each frame as a composition. The input is a music track plus optional user images or videos — there is **no narration and no website capture**. Typography and templates are the floor (a complete video needs zero assets); any media the user supplies is cut in on the same beat grid.

You are the **orchestrator**. Work in `videos/<project>/`. Run the steps in order and pass each **Gate** before moving on. Two steps need the user: **Step 3** (plan approval) and **Step 6** (render approval) — both are checkpoint gates per `../hyperframes/references/brief-contract.md` (read it before Step 0): in autonomous mode, post the Step 3 summary as a heads-up and proceed; Step 6 render approval is still asked, as the one kept question. Do every step yourself except **Step 4**, where you dispatch **one sub-agent per frame**. Keep design and motion rules out of this file — they live in `references/` and the `frame-worker` sub-agent.

`SKILL_DIR` = this skill directory. `PROJECT_DIR` = `videos/<project-name>/`.

Workflow: Step 0 setup → `hyperframes.json` + `assets/bgm.mp3`; Step 1 analyze → `audiomap.json`; Step 2 skeleton → `STORYBOARD.md` (frames, groups `TBD`); Step 3 plan → complete `STORYBOARD.md` + `frame.md`; Step 4 build → `compositions/frames/NN-*.html`; Step 5 assemble → `index.html`; Step 6 render → `renders/video.mp4`.

## Two ideas that shape everything

- **One analyzer, and you trust it.** `analyze-beatgrid.py` is the only beat analyzer — never re-measure beats with another tool or by ear. Its energy / density / rolls / onsets / silences are always reliable. Its `bpm` and `beats_sec` are reliable **only when the music is genuinely rhythmic**; on calm music the grid is a metronome the tracker imposed, so pace by phrases and energy instead and never hard-cut to it. Deciding which case you're in is each frame's `pacing` (Step 2).
- **One frame = one file; groups live inside.** Step 2 cuts the track into **frames**, and each frame becomes one composition file `compositions/frames/NN-<frame_id>.html`, built by one frame-worker. A frame can subdivide into **groups** (each a template or a motion-primitives combo). Extra density goes _inside_ a group, so **frame count tracks distinct treatments, not beats** — a fast track does not blow up the number of sub-agents.

---

## Step 0: Setup, BGM, and inputs

Goal: Establish the music source, create the HyperFrames project, and note any user-supplied media.

**The brief starts at the intent layer.** Opening rule, in order: **(1)** `BRIEF.md` exists → read it and ask nothing it answers — its `flow`/`storyboard` derive the mode (brief contract § 1). **(2)** No `BRIEF.md` but the project exists → resume from what's on disk; never re-interrogate. **(3)** A fresh creation request that arrived here directly → read `/hyperframes` and run its intent layer (`references/intent-interview.md`): it confirms this route's must-haves (the music source, destination → aspect — `../hyperframes/references/routes/music-to-video.md`) and announces what stays deferred — brand and genre are chosen at Step 3 by design. Write `BRIEF.md` immediately after init (never before — `init` refuses a non-empty directory) and record the preference-backed answers (`brief-format.md`). Edit requests skip all of this.

The **music is the spine** — establish one track before anything else. This skill is tuned for **fast, high-energy BGM**: a strong beat grid drives the cuts (calm tracks work, but pace by phrase rather than beat). If the user supplied audio — a music file, or a video to pull audio from — use it. Otherwise choose the mood from the request and generate a track through `/media-use` (`audio/references/bgm.md`); when the host app provides its own music tool, use that. Before the first authenticated provider action, run `npx hyperframes auth status` and relay its output verbatim. If signed out, apply one branch:

- **Collaborative:** wait for sign-in or an explicit choice to continue offline with the local provider.
- **Autonomous:** state the status and continue through the available local provider.

If no offline provider can satisfy the required music capability, surface the blocker. Never write keys into a per-repo `.env`. Auth ownership and offline fallbacks live in `/media-use` `references/setup-providers.md` § Providers. The resulting track lands at `assets/bgm.mp3`. Stage supplied images or videos so frames can use them on the beat grid; otherwise typography carries the video.

**Lyric videos:** for lyrics synced to the vocals, get word/line timing by transcribing the track via `/media-use`, or ask the user for the lyrics text and place lines on the beat grid.

Initialize only if `hyperframes.json` is missing. Name `<project>` from the brief in kebab-case, such as `midnight-drive-loop` — never a timestamp. `init` checks the installed skills against the latest on GitHub and updates the global set if any are out of date.

```bash
npx hyperframes init "videos/<project>" --non-interactive --example=blank --skill=music-to-video
mkdir -p "$PROJECT_DIR/assets" "$PROJECT_DIR/renders"
cp "<user-music>" "$PROJECT_DIR/assets/bgm.mp3"   # extract from a video first if needed
# only if the user gave you images/videos:
node <SKILL_DIR>/scripts/stage-assets.mjs --from <dir> --hyperframes "$PROJECT_DIR" --into public
```

The **brand** (font + palette) is chosen at Step 3, not here. Don't pick a genre or a track type up front — assets are just an optional ingredient, and the genre emerges from the per-frame choices.

**Gate:** `hyperframes.json` + `assets/bgm.mp3` exist; aspect / length / fps and (if any) the asset inventory are noted.

---

## Step 1: Analyze the music

Goal: Produce the one canonical timing analysis the whole video is built on.

`analyze-beatgrid.py` is the **only** beat analyzer — never re-measure beats with another tool or by ear. It reads the track once and writes `audiomap.json`: energy phases (level / density / feel), onsets + `onset_rate`, rolls, silences, `hard_stops`, `key_moments`, phrases, tempo / grid, and `audio.duration_sec`. It's deterministic — the same file always gives the same map. Most fields are reliable on any music; `bpm` and `beats_sec` are reliable only when the music is genuinely rhythmic, and judging that is the call you make at Step 2.

Prerequisites: Python 3 with `librosa`, `numpy`, and `soundfile` available. If import fails, install them into the active Python environment before running the analyzer:

```bash
python3 -m pip install librosa numpy soundfile
```

```bash
python3 <SKILL_DIR>/scripts/analyze-beatgrid.py "$PROJECT_DIR/assets/bgm.mp3" \
  -o "$PROJECT_DIR/audiomap.json" --print
```

**Gate:** `audiomap.json` exists; `audio.duration_sec` is known.

---

## Step 2: Frame skeleton (structure only)

Goal: Read the music and lay out the frames — the skeleton of `STORYBOARD.md`.

Read [`references/frame-skeleton.md`](references/frame-skeleton.md). Turn `audiomap.json` into the **skeleton** of `STORYBOARD.md` yourself — there is no intermediate JSON. Cut the track into **frames** at real musical changes (`hard_stops`, SURGE / DROP `key_moments`, the edges of a roll, a stretch with no onsets, a big energy jump), snapping every boundary to an audiomap anchor. For each frame set `span_sec`, `pacing` (the verdict from Step 1's trust call — `beat_cut` when the grid is real, `phrase_flow` when it's a metronome imposed on calm music), `mood`, and a one-line `feel` (the plain music situation Step 3 matches a template against). Only classify and lay out here: leave every frame's `### Groups` as `TBD (Step 3)` and the frontmatter `style` blank — no templates, copy, color, or fonts. Expect ~1–6 frames.

**Gate:** frames tile the track (first at 0, last at `duration_s`); each carries `span_sec` + `pacing` + `mood` + `feel`; every `### Groups` is `TBD`; no content anywhere.

---

## Step 3: Fill the plan (user-gated)

Goal: Turn the skeleton into an approved, complete `STORYBOARD.md`.

Read [`references/planning.md`](references/planning.md), [`storyboard-format.md`](references/storyboard-format.md), [`template-catalog.md`](references/template-catalog.md), [`motion-primitive-catalog.md`](references/motion-primitive-catalog.md), and [`montage.md`](references/montage.md) (only if the user supplied assets). Editing the same file in place, do two things:

1. **Pick the brand.** Choose one preset from `../hyperframes-creative/frame-presets/` using the table in `../hyperframes-creative/references/design-spec.md` (match the track's mood; **only its fonts and colors matter** — templates own composition). Copy it into `frame.md` **unmodified** and fill the frontmatter `style` (font + a ≤4–6 swatch palette) from it.
2. **Fill every frame.** Decide its groups and give each a treatment: a matched template from the catalog (with bound params and real audiomap anchors), a free-compose from the primitive catalog, or an asset treatment that **obeys `pacing`**. **Before you free-compose a named look, search the live catalog for it**: for every look, effect, treatment or transition the user asked for — "CRT scanlines", "glitch", "film grain", "shimmer sweep" — run `npx hyperframes catalog --query "<the look, in plain English>" --json` and read the top results. `template-catalog.md` and `motion-primitive-catalog.md` list only this skill's own local materials; the search ranks the whole hosted registry (~400 blocks and components) and needs **nothing installed** — no project, no prior `add`, no account. Free-compose a look only after a search for it came back with nothing that fits. Write the copy. You own WHAT (template / primitives + content + anchors); the frame-worker owns HOW — **never write millisecond tweens into the storyboard**.

```bash
node <SKILL_DIR>/scripts/validate-plan.mjs --storyboard "$PROJECT_DIR/STORYBOARD.md" \
  --audiomap "$PROJECT_DIR/audiomap.json" --templates <SKILL_DIR>/references/templates
```

Fix every `✗` (hard errors: duration mismatch, frames not tiling the track, a missing `src`); warnings are best-effort. Then present the frame-by-frame summary in chat as a proposal (`../hyperframes/references/review-loop.md` § 1) and iterate on the user's replies until they approve; for `storyboard: yes`, also show it as the board, `boards/storyboard.html` (`../hyperframes-creative/references/storyboard-recipe.md`). In autonomous mode this is a checkpoint gate: post the summary as a heads-up and proceed (the `validate-plan.mjs` pass is a quality gate and still blocks).

**Gate:** `frame.md` is a verbatim preset copy; `validate-plan.mjs` exits 0; the user approved the plan (autonomous: the summary was posted as a heads-up).

---

## Step 4: Build frames from the plan

Goal: Build every frame as a self-contained composition file.

Create `compositions/frames/`. Read [`sub-agents/frame-worker.md`](sub-agents/frame-worker.md) and `../hyperframes/references/subagent-dispatch.md`. Dispatch **one frame-worker per frame**, in parallel where possible (otherwise in waves). Each worker gets exactly one frame and this context:

```text
PROJECT_DIR: <abs path>
frame_id: <NN-frame_id>              # = the frame file stem, e.g. 02-f2; the composition id
Your block: the `## Frame N — <frame_id>` block in PROJECT_DIR/STORYBOARD.md
audiomap: PROJECT_DIR/audiomap.json
frame.md: PROJECT_DIR/frame.md
Materials: for each group, <SKILL_DIR>/references/templates/<id>/index.html (templates) and
           <SKILL_DIR>/references/motion-primitives/<id>/ (free); staged assets/ (asset groups)
Contracts: ../hyperframes-core/references/sub-compositions.md + determinism-rules.md
Canvas: <w>×<h>   Pacing: <beat_cut|phrase_flow>
Write to: PROJECT_DIR/compositions/frames/<frame_id>.html
```

The worker forks the cited materials, converts every anchor to frame-local seconds (`local_t = track_t − span_sec[0]`), gates its groups with 0ms cuts, and writes one seek-safe frame file. **The worker never runs the `hyperframes` CLI** — those commands operate on the assembled project, which doesn't exist yet, so they'd report on the wrong files. The worker just writes to the contract and stops; you verify after assembly (Step 6). As each worker returns, you can confirm its file landed on disk.

**Gate:** every frame has its `compositions/frames/NN-*.html` on disk.

---

## Step 5: Assemble

Goal: Wire the built frames + BGM into the playable `index.html`.

`assemble-index.mjs` is deterministic — no subagent, no judgment. It references each frame file at its cumulative `data-start`, mounts `assets/bgm.mp3` on track 11, and hard-cuts frame → frame (frames tile the track with no gaps, so there is **no transition injector**).

```bash
node <SKILL_DIR>/scripts/assemble-index.mjs --storyboard "$PROJECT_DIR/STORYBOARD.md" \
  --hyperframes "$PROJECT_DIR" --audiomap "$PROJECT_DIR/audiomap.json"
```

Fix any `✗` it reports — a missing or blank frame file means that worker wrote a partial file; re-dispatch it (Step 4) and re-assemble.

**Gate:** `index.html` exists; total duration == `audiomap.audio.duration_sec`.

---

## Step 6: Verify and render

Goal: Verify the assembled video, get user approval, and render the final MP4.

Run the CLI on the **assembled project** — that's the correct unit (the per-frame workers couldn't run it). `check` runs structural lint and the headless-browser runtime, layout, motion, and contrast gate in one pass; `--snapshots` also emits the review frames.

```bash
( cd "$PROJECT_DIR" && npx hyperframes check . --snapshots )
```

Inspect at `t=0`, each frame start, the strongest DROP / SURGE, every `hard_stops[].t`, and the final frame. On failure, make the **cheapest safe fix** yourself: edit the offending `compositions/frames/NN-*.html`. Never change duration or audio timing to hide a sync issue. Once the gates pass, open the final Studio preview (`( cd "$PROJECT_DIR" && npx hyperframes preview --background )`) and pause for user review — render now, or what changes? Render only on approval (autonomous mode: the same, as the one kept question), then deliver the MP4 with the contact sheet:

```bash
( cd "$PROJECT_DIR" && npx hyperframes render . --skill=music-to-video -q draft -o renders/video.mp4 --fps 30 )
```

**Gate:** `check` passed and the snapshots were inspected; the user approved (autonomous: checks passed and the delivery includes the contact sheet); `renders/video.mp4` exists with audio, duration == `audiomap.audio.duration_sec`. The final reply states the MP4 path and duration.

---

## Resume table

| You have                   | Continue from |
| -------------------------- | ------------- |
| `assets/bgm.mp3` only      | Step 1        |
| `audiomap.json`            | Step 2        |
| `STORYBOARD.md` (skeleton) | Step 3        |
| `STORYBOARD.md` (complete) | Step 4        |
| all frame files            | Step 5        |
| `index.html`               | Step 6        |

## Quick Reference

**Formats:** landscape `1920x1080` by default; portrait `1080x1920`; square `1080x1080`. Set the canvas once in the storyboard frontmatter (`canvas: { w, h, fps }`).

**Scripts** under `scripts/`: `analyze-beatgrid.py` (the one analyzer), `validate-plan.mjs` (plan check), `assemble-index.mjs` (index assembly), `stage-assets.mjs` (stage user media), `lib/storyboard.mjs` (vendored parser). Everything else is the `hyperframes` CLI.

| Read                                                                                                           | When                                                    |
| -------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------- |
| [`references/frame-skeleton.md`](references/frame-skeleton.md)                                                 | Step 2: read the music, lay out the frames, set pacing  |
| [`references/planning.md`](references/planning.md) · [`storyboard-format.md`](references/storyboard-format.md) | Step 3: pick the brand, fill each frame, write the plan |
| [`references/template-catalog.md`](references/template-catalog.md)                                             | Step 3: pick a template per group                       |
| [`references/motion-primitive-catalog.md`](references/motion-primitive-catalog.md)                             | Step 3/4: L0 recipes for free-compose                   |
| [`references/montage.md`](references/montage.md)                                                               | Step 3/4: asset treatments (beat-cut / ken-burns)       |
| [`sub-agents/frame-worker.md`](sub-agents/frame-worker.md)                                                     | Step 4: dispatch + build one frame                      |
| `../hyperframes/references/subagent-dispatch.md`                                                               | Step 4: dispatch sub-agents safely                      |
| `../hyperframes-creative/references/design-spec.md`                                                            | Step 3: pick the preset (the brand)                     |

## Directory layout

```
music-to-video/
  GUIDE.md
  references/   frame-skeleton.md · planning.md · storyboard-format.md
                template-catalog.md · motion-primitive-catalog.md · montage.md
                templates/<id>/          { index.html (+ assets/ · program.json) }  ← L1 catalog impls
                motion-primitives/<id>/  { index.html (mounts the scene), scene.html (the sub-composition) } (+ ../assets/gsap.min.js shared by recipes) ← L0 catalog impls
  scripts/      analyze-beatgrid.py · assemble-index.mjs · validate-plan.mjs · stage-assets.mjs · lib/storyboard.mjs
  sub-agents/   frame-worker.md   ← the one subagent (one per frame)
```


<!-- ===== FILE: hyperframes/music-to-video/references/frame-skeleton.md ===== -->

# Frame skeleton (Step 2) — read the music, lay out the frames

At Step 2 **you (the orchestrator)** read `audiomap.json` and write the **skeleton** of
`STORYBOARD.md` directly: cut the track into **frames** (one frame = one composition file =
one scene), and for each frame set its **span**, its **pacing** (does this stretch want hard
beat-cuts, or calm phrase/energy flow?), its **mood**, and a one-line **feel** note.

You **classify and lay out the spine only.** You do **not** pick templates, write copy, choose
colors/fonts, or decide a frame's groups — those are Step 3 (the plan fills each frame in
place). Leave every frame's `### Groups` as `TBD (Step 3)` and the frontmatter `style` blank.

There is **no intermediate JSON** — the skeleton _is_ the start of `STORYBOARD.md`. Step 3
edits the same file.

## The trust boundary (read this first)

`audiomap.json` is one analyzer's output. Some fields are robust on **any** music; some are
reliable only when the music is **actually rhythmic**. This decides each frame's `pacing`:

| Field                                                                                                                                                                                               | Trust                                                                                                                                                                                                                        |
| --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `energy_phases[]` (level / energy / density / feel), `events[]` + `onset_rate`, `rolls[]` (and their **absence**), `silences[]`, `hard_stops[]`, `key_moments[]`, `phrases[]`, `audio.duration_sec` | **Always** — robust measurements                                                                                                                                                                                             |
| `tempo.bpm`, `grid.beats_sec` / `downbeats_sec` **precision**                                                                                                                                       | **Only when the music is rhythmic.** On calm / sparse material the beat grid is a metronome the tracker _imposes_ (often octave-doubled) — usually **more grid beats than real onsets**. Do **not** anchor cuts to it there. |

- **Grid is reliable** when: rolls present, and/or dense phases, and/or high `onset_rate` with a steady grid.
- **Grid is fictional** when: `rolls`≈0, mostly `sparse` phases, low `onset_rate` → pace by `phrases[]` + `energy_phases[]`, not beats.

## How to lay out frames (run in order)

1. **Gestalt.** From `summary` / `tempo` / `audio.duration_sec` + the roll count, write the
   frontmatter `compositionId`, `duration_s` (== `audio.duration_sec`), `canvas`, and a
   one-line read of the track's density arc.
2. **Cut into frames.** Walk `energy_phases[]` and split where the music genuinely changes
   state — at `hard_stops[]`, `SURGE` / `DROP` `key_moments`, the start/end of a `rolls[]` run,
   an **onset desert** (a long gap in `events[]`), or a big energy-level jump. Collapse adjacent
   phases that are one gesture. Expect **~1–6 frames**; a short clip may be one.
   **Snap every boundary to an audiomap anchor**, then re-snap to the nearest `beats_sec`
   (tolerance ≤ ½ beat) **only when the grid is reliable**; on calm material snap to
   `phrases[]` / `energy_phases[]` edges instead. Frames **tile the track** (first at 0, last
   at `duration_s`, no gaps/overlaps).
3. **Per frame, set `pacing`** — the trust-boundary call:
   - **`beat_cut`** — genuinely rhythmic: a roll present, **or** dense, **or** (clearly high `onset_rate` **and** a steady grid). Hard cuts / per-onset reveals may anchor to beats.
   - **`phrase_flow`** — calm / sparse: `rolls`≈0, mostly sparse, low `onset_rate`. Do **not** anchor hard cuts to the grid; pace by `phrases[]` + the energy envelope (slow crossfades, long holds).
4. **Per frame, tag `mood`** (1–3 of: `warm` · `dark` · `hype` · `elegant` · `glitch` ·
   `cinematic` · `playful` · `tense` · `dreamy` · `aggressive`) from `energy_phases[].feel` +
   energy + any genre cue in the brief/title.
5. **Per frame, write a one-line `feel`** — the plain-language music situation Step 3 matches a
   template against (e.g. "accelerating onset stream into a held downbeat", "calm held pad, one
   onset desert", "fast sustained-fill roll, no readable message"). This is what the planner
   reads against the catalog's **Reach for it when** — keep it concrete, drawn from the robust
   fields, never invented.

## What the skeleton looks like

A valid `STORYBOARD.md` with the spine set and every frame's treatment left for Step 3
(full syntax in [`storyboard-format.md`](storyboard-format.md)):

```markdown
---
compositionId: bgm
duration_s: 30.0 # == audiomap.audio.duration_sec
canvas: { w: 1920, h: 1080, fps: 30 }
style: # blank — Step 3 fills it from the chosen frame.md preset
build_notes: ["one paused timeline per frame", "no remote assets"]
---

## Frame 1 — f1

- src: compositions/frames/01-f1.html
- duration: 7.198s # = span length; assembler sums these for cumulative data-start
- span_sec: [0.0, 7.198] # track seconds; frames tile the track
- pacing: beat_cut
- mood: [hype]
- feel: accelerating onset stream building into a held downbeat

### Groups

- TBD (Step 3)

## Frame 2 — f2

- src: compositions/frames/02-f2.html
- duration: 10.4s
- span_sec: [7.198, 17.598]
- pacing: phrase_flow
- mood: [warm, cinematic]
- feel: calm held pad, one long onset desert

### Groups

- TBD (Step 3)
```

## Self-check

- `duration_s == audiomap.audio.duration_sec`; frames tile the track gap-free (first at 0, last at `duration_s`).
- Every frame has `src` + `span_sec` + `duration` + `pacing` + `mood` + a one-line `feel`.
- `pacing` was set from the **robust** fields (energy / density / rolls / onset_rate), never from `bpm` / `beats_sec` alone.
- No frame boundary sits inside a `rolls[]` run or leaves a sub-1-bar fragment.
- Every frame's `### Groups` is `TBD (Step 3)`; `style` is blank. **No template, copy, color, or font anywhere.**


<!-- ===== FILE: hyperframes/music-to-video/references/montage.md ===== -->

# Asset treatments — weaving user media onto the beat spine

When the user supplies images/videos, a group can be an **asset treatment** instead of a
typographic template/free-compose. Assets are an **additive ingredient on the same beat
spine** — never a separate pipeline. Typography/templates stay the floor: if no asset fits a
group, fall back to a template/free group (a complete video needs zero assets).

The planner (Step 3) picks the treatment and the clips + anchors (WHAT); the frame-worker
realizes it inside the frame file (HOW). **Obey the frame's `pacing`.**

## The three treatments

### `beat_cut` — one clip per anchor (only on a `beat_cut` frame)

The asset-driven analogue of a per-onset typographic group: cut to a new clip on each anchor
(the frame's beats/onsets from the audiomap). Each clip is a `class="clip"` element
(`<img>` for a photo, **muted** `<video>` for a motion clip) placed at its anchor with
`data-start`/`data-duration`/`data-track-index` per the core clip contract. (Muted on purpose: the music track drives the sound.) Between clips,
crossfade the outgoing content to `opacity:0` ending **at** the next anchor.
Cut on the **strong** anchors; land a hero clip on a `key_moment`/downbeat.

### `ken_burns` — slow push on one clip (fits a `phrase_flow` frame)

For calm frames: one clip held over the span with a slow scale/translate push (e.g. scale
1.0→1.08 + a small drift) eased across the whole `span_sec` — paced by the frame, not by
beats. No hard cuts. Crossfade in/out at the frame edges. This is the right asset treatment
when the beat grid is unreliable (calm music).

### `bg_under_text` — clip dimmed behind a template/free group

A full-bleed clip dimmed ~30–50% as the background of a group whose foreground is a template
or free-compose typographic treatment. The text rides on the same anchors; the clip is the
bed. Use when the user wants their footage present but the message must stay readable.

## Rules

- **`pacing` decides the treatment**: `beat_cut` only on a `beat_cut` frame; on a
  `phrase_flow` frame use `ken_burns` or a slow crossfade — **never** per-onset hard cuts on
  the (unreliable) calm grid.
- **Clips are muted; the root owns audio.** Mount each `<video class="clip">` **muted**, as a
  direct child of the frame root (never nested in another timed element, or the renderer
  freezes it). The BGM is the only audio in v1.
- **Crossfades animate `opacity`/`autoAlpha`**, never `visibility`/`display` on a `.clip`
  (the framework owns clip visibility — that trips `gsap_animates_clip_element`).
- **Backgrounds dim ~30–50%** so any foreground text stays legible.
- Anchors are **track seconds from `audiomap.json`**; the worker subtracts the frame start
  to get frame-local time.
- Local staged assets only (`assets/` via `stage-assets.mjs`); never remote URLs.

## Deferred hook (not v1)

A clip that should play **its own sound** (interview cut, lyric clip) needs a sibling
`<audio>` mounted at the **root** by the assembler, with the BGM ducked under it (a
`data-automation` volume lane on the BGM, see `creator-editing-recipes.md` in `hyperframes-core`). The frame-worker mounts no audio. Keep clips muted in v1; wire clip-audio +
ducking only when the user asks.


<!-- ===== FILE: hyperframes/music-to-video/references/motion-primitive-catalog.md ===== -->

# Motion-primitive catalog — the free-compose menu

The atomic layer: one anchor → one micro-move. When no template fits a group, free-compose by
naming primitives from here. Scan **anchor** + **best span** + **what it does**, then pick the
smallest set that carries the group.

## Timing & latency (applies to every primitive)

- **Hard hits are 0ms.** Cuts, palette flips, content swaps, freezes are `tl.set(...)` with no duration — the percussion _is_ the motion. Easing a hit kills it.
- **Lead the anchor.** A move that must _land_ on a beat (a wipe covering the frame, a count-up locking, two blocks colliding) starts **~40–190ms early** so it completes ON the anchor. Reactive entrances (something appearing _because_ of the hit) fire 0–45ms after.
- **Eased entrances: 300–500ms** (scale punch, slides, camera pushes). **Macro builds: 800–2000ms** spanning a whole roll / silence.
- **Per-bar caps:** one accumulating element per hit (not a burst); a camera move at most once per phrase, never per beat; a dense flip/strobe system runs ≤2–3s.
- **Tension-builds lock.** A count-up / sequential build / morph must _resolve on_ a downbeat or hard_stop, never trail off mid-bar.
- **Best span means active motion.** The catalog's span guidance is not a license to stretch one primitive over a whole frame. If a free-composed group runs longer than the listed span, add a hold / bed / next primitive, or split the frame into another group at the next musical anchor.

## Catalog

| id                    | anchor                           | best span         | what it does                                                              |
| --------------------- | -------------------------------- | ----------------- | ------------------------------------------------------------------------- |
| `hypercut-whip`       | beat / hard_stop                 | 0.18-0.45s        | fast whip-pan hard cut between frames                                     |
| `kinetic-letter-in`   | downbeat / phrase                | 0.4-1.2s          | per-letter kinetic entrance                                               |
| `braam-punch`         | drop / surge                     | 0.2-0.9s active   | big impact: scale + weight slam                                           |
| `chromatic-split`     | snare / glitch / surge           | 0.1-0.6s          | RGB channel split / glitch on a word                                      |
| `mask-reveal`         | section_start / downbeat         | 0.5-1.2s          | clip-path mask wipe reveal                                                |
| `screen-shake`        | drop / crash / kick              | 0.1-0.5s          | camera / screen shake jitter                                              |
| `binary-decrypt`      | roll / build                     | 0.8-2.5s          | scramble→decode text (binary → word)                                      |
| `dolly-zoom`          | phrase / build                   | 1.2-2.5s          | vertigo dolly-zoom (scale vs perspective)                                 |
| `iris-open`           | section_start / reveal           | 0.6-1.2s          | circular iris-open reveal                                                 |
| `electric-arc`        | accent / glitch                  | 0.1-0.6s          | electric arc / lightning accent                                           |
| `neon-flicker`        | hold / texture                   | 0.5-2.5s          | neon-sign flicker                                                         |
| `chrome-sweep`        | downbeat / reveal                | 0.6-1.4s          | metallic specular sweep across text                                       |
| `slot-machine-reveal` | roll → downbeat                  | 0.8-2.0s          | slot-machine spin-to-land character reveal                                |
| `liquid-morph`        | phrase / transition              | 1.0-2.5s          | liquid / blob morph                                                       |
| `gooey-metaball`      | build / drop                     | 1.5-3.0s          | gooey metaball merge field                                                |
| `3d-card-flip`        | downbeat / swap                  | 0.8-1.6s          | 3D card flip (rotateY)                                                    |
| `crash-zoom-in`       | drop / surge                     | 0.2-0.8s          | violent crash zoom-in                                                     |
| `spotlight-sweep`     | reveal / hold                    | 0.8-2.0s          | spotlight / gradient sweep over text                                      |
| `outline-to-fill`     | downbeat / reveal                | 0.8-1.8s          | stroke outline → solid fill                                               |
| `counting-punch`      | roll → downbeat                  | 1.0-2.5s          | number count-up that punches & locks                                      |
| `particle-burst`      | drop / crash                     | 0.2-1.2s          | particle explosion burst                                                  |
| `radial-burst-lines`  | drop / surge                     | 0.2-0.8s          | radial speed-lines burst                                                  |
| `pixel-dissolve`      | transition / hard_stop           | 0.5-1.5s          | pixelated dissolve                                                        |
| `datamosh-smear`      | glitch / transition              | 0.4-1.2s          | datamosh / motion smear                                                   |
| `text-wave-distort`   | hold / texture                   | 1.0-2.5s          | wavy text distortion                                                      |
| `bg-flow-field`       | energy / whole span (bed)        | 4-12s bed         | generative curl-noise background bed; compose any foreground move over it |
| `blur-resolve`        | stop / final hold                | 0.7-2.0s          | blur-in to crisp focus, then blur-out on the cut                          |
| `chromatic-pressure`  | snare / glitch                   | 0.1-0.5s          | RGB split / digital tension on a transient                                |
| `color-grid-shuffle`  | onset                            | 0ms hits; ≤2s run | grid of cells recolored by a deterministic index per onset                |
| `content-swap`        | beat                             | 0ms hits; ≤3s run | 0ms swap of stacked nodes: the workhorse percussive move                  |
| `directional-fill`    | beat / reveal                    | 0.3-1.0s each     | directional wipe-fill (scaleX) sweeping across bars                       |
| `flash-cut`           | drop / crash                     | 0-0.6s            | full-frame flash masking a word / color state change                      |
| `freeze-hold`         | hard_stop                        | 0ms in; 0.5-2s    | freeze the moving system and hold it                                      |
| `hard-cut`            | beat / hard_stop                 | 0ms in; 0.3-2s    | sample-accurate color-block + word cut                                    |
| `mosaic-pack`         | beat / build                     | 1.5-3.5s          | scattered tiles fly in and pack into a grid                               |
| `negative-space-hold` | silence / hard_stop / final hold | 1-6s hold         | kill busy layers, hold one readable mark in empty space                   |
| `overlay-pop`         | accent                           | 0.2-0.6s in       | badge / lower-third overlay pops in over a base                           |
| `palette-flip`        | section change                   | 0ms flip; 0.5-4s  | same layout re-skins via 0ms palette-variable flips                       |
| `staggered-exit`      | phrase / transition              | 0.4-1.2s          | ordered cascade-out clearing the frame                                    |
| `staggered-reveal`    | build                            | 0.8-2.5s          | ordered cascade-in of a stack / list                                      |
| `system-replace`      | drop / regime change             | 0ms cut           | hard-cut the entire visual system, then boot the new one                  |
| `text-spectral-rays`  | phrase / sweep (hero text)       | 2.5-5s            | volumetric light-rays cast by a wordmark toward a sweeping light cursor   |
| `tile-mosaic`         | build / reveal                   | 1.5-3.5s          | grid of tiles revealed in a diagonal sweep, assembling a poster           |
| `typewriter-reveal`   | roll / build                     | 1.0-3.0s          | character / word type-on with caret                                       |
| `value-counter`       | roll → downbeat                  | 1.0-2.5s          | count-up that locks on a downbeat / hard_stop                             |
| `word-grid-burst`     | onsets → downbeat                | 1.8-3.2s          | grid of words revealed per onset, refocus one on a downbeat               |

## How to combine

- One dominant system per group; layer at most one texture primitive over one structural primitive.
- Structure on strong beats (cuts, camera, `system-replace` → downbeat / phrase / section_start); texture on weak / syncopated hits (`content-swap`, typewriter letters, chromatic accents).
- A roll is an accumulation container — build during it, hard-cut to a clean layout on the downbeat that ends it.
- `drop` ≠ `downbeat`: a downbeat is a cut within the regime; a drop is a regime change (`system-replace`, total clear, element-count jump).
- Let silence remove density (`negative-space-hold`).
- Background beds are a layer, not a move: one bed at a time, under foreground primitives.
- `text-spectral-rays` is the hero wordmark treatment; do not stack another visible copy of the same word on top.


<!-- ===== FILE: hyperframes/music-to-video/references/motion-primitives/text-spectral-rays/USAGE.md ===== -->

# Using `text-spectral-rays` — it OWNS its wordmark

`text-spectral-rays` is a **self-contained WebGL hero-text renderer**. From ONE rasterized
glyph mask it draws **both** the solid wordmark **and** the spectral rays that emanate from
it. Letters and rays share the same mask, so they are always perfectly registered.

## The one trap: never give the word a second source

The ghost / doubled-wordmark artifact comes from splitting the word across two sources:

- ❌ **Wrong** — use the shader as a "rays-only background" and draw the visible letters
  with a **separate DOM element** (or stack a second text move like `content_swap` /
  `chromatic_pressure` on the same word). The DOM font (e.g. Inter) and the shader's raster
  font (Arial Black / Impact fallback) differ in width, shape, and position, so the ray
  edges never line up with the DOM letters → a misregistered ghost. **Deleting the shader's
  letter terms does NOT fix it** — the ray mask itself is still the second, misaligned copy
  of the word.

- ✅ **Right** — let the shader render the wordmark. There is exactly ONE source, so a
  ghost is structurally impossible.

## Integrate in one pass

1. **It IS the wordmark.** Hide any DOM logo for that word (keep it only as an invisible
   layout spacer if a tagline/CTA below depends on its box). Never stack a discrete text
   move on the same word.
2. **One timeline.** Merge its `progress` / `effectMix` state tweens onto the group's master
   timeline and repaint via `tl.eventCallback("onUpdate", render)` — no second timeline, no
   `requestAnimationFrame`.
3. **Align the cursor to the word.** `mouse.y` must equal the mask's vertical center. If you
   move the rasterized word off frame-center (e.g. up, to leave room for a tagline), shift
   the cursor's `y` by the same amount — otherwise the rays cast at the wrong angle.
4. **Local raster only.** Rasterize the word with a bundled / system font (no CDN font);
   upload the mask + colour canvases as textures.
5. **Entrance.** Slam the whole canvas (autoAlpha + a scale punch, `transform-origin` on the
   word's optical center) on the hit; let `effectMix` bloom the rays just after. The solid
   letters are present the instant the canvas reveals.

## Pairs with

A background bed (`bg-flow-field`) or **separate** supporting elements (tagline, CTA, rule)
— never a second treatment of its own word.


<!-- ===== FILE: hyperframes/music-to-video/references/planning.md ===== -->

# Planning (Step 3) — pick the brand, fill every frame

At Step 3 **you (the orchestrator)** turn the Step-2 skeleton into a complete, approved
`STORYBOARD.md`. You edit the **same file** in place: pick the brand spine, then for each
frame decide its **groups**, give each group a treatment, bind real beat anchors, and write
the copy.

Your mantra: **music is the spine; a template is a head start, not a cage; typography is the
floor and assets are an optional ingredient on the same beat grid.**

**You own WHAT, not HOW.** You name the template / primitives, the content, the brand, the
anchor seconds, and the intent. The frame-worker (Step 4) decides HOW — micro-timing,
realization, intra-frame cuts. **Never write millisecond tweens into the storyboard.**

## Inputs

- The Step-2 skeleton already in `STORYBOARD.md` — frames with `span_sec` + `pacing` + `mood` + `feel`.
- `audiomap.json` — timing truth; read the real anchor seconds inside each frame's span.
- [`template-catalog.md`](template-catalog.md) — the template selection menu.
- [`motion-primitive-catalog.md`](motion-primitive-catalog.md) — the free-compose menu (L0 recipes).
- [`montage.md`](montage.md) — asset treatments (only if the user supplied images/videos).
- User brief / supplied copy — topic, mood, exact words to keep.

## Step A — pick the brand spine (one preset, unmodified)

The whole video shares one type family + palette. Pick **one ready-made preset** from
`../../hyperframes-creative/frame-presets/` using the preset table in
`../../hyperframes-creative/references/design-spec.md` — choose by the track's mood + the brief,
and **only its fonts + colors matter** (templates own composition + motion; the preset only
sets the look). Copy it in **unmodified**:

```bash
cp ../hyperframes-creative/frame-presets/<preset>/FRAME.md "$PROJECT_DIR/frame.md"
```

Then fill the storyboard frontmatter `style` from it: the `font` from its `typography:` and a
≤4–6 swatch `palette` from its `colors:`. **Quote the hex / family verbatim — never invent or
round.** Every group's palette params draw from this one palette; that unity is what makes
different templates read as one piece.

## Step B — per frame, decide its groups

A frame is usually **one group** (one template or one free composition spanning the frame).
Subdivide into 2+ groups **only when a single treatment can't cover the frame** — e.g. a busy
opener plus a closing lockup. When you split, cut at a **real audiomap anchor** inside the
frame's span (a `key_moment` / `phrase` edge / onset-cluster gap), **never inside a `rolls[]`
run**, and keep every group **≥ ~1 bar**. Density does **not** force more groups — a dense
frame is usually ONE group whose template absorbs the density internally (a meta-template like
`poster-tile-mosaic`). **Group count tracks distinct treatments, not beats.**

## Step C — per group, pick a treatment (exactly one of three)

### A. Match a template

Read [`template-catalog.md`](template-catalog.md). Match the group's `feel` + `mood` + `pacing`
to a template's **Reach for it when**; take the closest fit. Then bind it:

- Fill `params` (keys from the catalog entry) — your copy into text slots, palette from the brand spine, `duration` = the group's span length.
- Fill `role_bindings` with this group's **real anchor seconds** read from `audiomap.json` over its span (not example times).
- If the template's natural stop and the group's span end disagree, snap to the nearest anchor.

### B. Free-compose (no template fits)

Write a `free_design` — one visual thesis from [`motion-primitive-catalog.md`](motion-primitive-catalog.md)
(a dominant system + the named L0 primitives + a density topology) + `anchors` (the real
beat / onset seconds the moves ride). Free-compose is a **first-class** choice, written as
carefully as a matched group — never a failure.

### C. Asset treatment (only when the user supplied assets and they fit)

Make it an `asset` group ([`montage.md`](montage.md)). **Obey `pacing`:** on a `beat_cut`
frame use `beat_cut` (one clip per anchor) or `bg_under_text`; on a `phrase_flow` frame use
`ken_burns` or a slow crossfade — **never** per-onset hard cuts. Assets are additive: if none
fits a group, fall back to template / free (typography is the floor — a complete video needs
no assets).

## Copy (you own the words)

- Keep exact user words; else invent with taste, on the brief's mood.
- **Message vs texture:** a readable word holds ≥1 beat (headline 3–8, sentence 4–10), stable + focal; a word held <1 beat is texture (strobe / grid / ticks). Never force a message onto a sub-beat — demote it to texture.
- Place copy into the template's text params, onto a free group's anchors, or as an asset group's `overlay_copy`. Declare the anchor + accumulate / stagger intent; leave micro-timing to the worker.
- A closing logo / CTA lands on the final hit / hard stop and holds through trailing silence.

## Transitions (you do not emit them)

Everything is a **0ms hard cut** for now. **frame → frame** is owned by the assembler
(back-to-back files); adjacent `span_sec` already imply the cut. **group → group inside a
frame** is owned by the worker on its frame timeline; you only set each group's `span_sec`.

## Write + validate

Complete `STORYBOARD.md` ([`storyboard-format.md`](storyboard-format.md)), then run
`node scripts/validate-plan.mjs` and fix every `✗`. Present the frame-by-frame summary in chat
and iterate until approved (Step 3 in `GUIDE.md` says how).

## Self-check

- `frame.md` is a verbatim copy of one preset; frontmatter `style.font` / `style.palette` are drawn from it (exact values).
- Every frame became ≥1 group; groups tile the frame span in order; no group < ~1 bar; no group boundary inside a `rolls[]` run.
- Each group is exactly one of template / free_design / asset.
- Template `params` keys match the catalog entry; `role_bindings` / `anchors` use real audiomap seconds.
- Asset treatments obey `pacing` (no `beat_cut` on a `phrase_flow` frame).
- Every group's palette draws from the one brand palette.
- `duration_s == audiomap.audio.duration_sec`; `validate-plan.mjs` passes.


<!-- ===== FILE: hyperframes/music-to-video/references/storyboard-format.md ===== -->

# STORYBOARD.md format — frames → groups

`STORYBOARD.md` is the single reviewable plan the user approves at Step 3 and the **manual**
each frame-worker follows at Step 4. It is **hierarchical**: one block per **frame**, written
as a `## Frame N — <frame_id>` heading (the parser recognizes `Frame`). **One frame = one
scene = one composition file.** Inside each frame block are its **groups** (the treatment
units). The assembler reads the frame level (`duration` → `data-start`, `src`); the worker
reads its own frame block. A frame's **composition id = its `src` file stem**
(`compositions/frames/01-f1.html` → `01-f1`), which the worker uses as `data-composition-id`
and the `window.__timelines` key.

Step 2 writes the skeleton (frame fields, groups `TBD`); Step 3 fills the groups + brand. It
is a build spec, not code — the planner writes WHAT, the worker decides HOW. **Never write
millisecond tweens here.**

## File shape

YAML frontmatter (the video-wide spine) + one `## Frame N — <frame_id>` block per frame.

```markdown
---
compositionId: bgm
duration_s: 30.0 # == audiomap.audio.duration_sec, exactly
canvas: { w: 1920, h: 1080, fps: 30 }
style: # brand spine — from the chosen frame.md preset (Step 3)
  font: "EB Garamond / Inter / JetBrains Mono" # the preset's typography, verbatim
  palette: ["#FAF9F5", "#141413", "#CC785C", "#181715"] # ≤4–6 swatches from the preset's colors
assets: false # false, or a note like "assets/ has 6 user photos"
build_notes: ["one paused timeline per frame", "no remote assets"]
avoid: ["generic slideshow", "tiny unreadable hero text"]
---

## Frame 1 — f1

- src: compositions/frames/01-f1.html # worker writes here; assembler refs it; stem (01-f1) = composition id
- duration: 7.198s # = span length; the assembler reads this for cumulative data-start
- span_sec: [0.0, 7.198] # track seconds; frames tile the track
- pacing: beat_cut # beat_cut | phrase_flow (from the skeleton; obey it)
- mood: [hype]
- feel: accelerating onset stream into a held downbeat

### Groups

- **g1** — template: `intro-kinetic-cascade`
  - span_sec: [0.0, 4.017] # frame-LOCAL build is 0-based; these are TRACK seconds (worker subtracts frame start)
  - params: { theme: "light", icon: "bolt", phrases: "[…]", climax: "{…}" }
  - role_bindings: { phrase: { times: [0.14, 0.55, 0.87] }, climax: { in: 3.79, iconAt: 4.9 } }
  - copy: "GROWTH THROUGH CREATIVITY"
- **g2** — free_design
  - span_sec: [4.017, 7.198]
  - free_design: { dominant_system: "per-onset typography", primitives: ["content-swap", "braam-punch"], density_topology: "accumulate" }
  - anchors: [4.10, 4.80, 5.50, 6.20] # onset seconds the reveals ride (from audiomap)
  - copy: ["BUILD", "SHIP", "REPEAT"]

## Frame 2 — f2

…
```

## Frame block — required fields

| field                             | meaning                                                                                                                        |
| --------------------------------- | ------------------------------------------------------------------------------------------------------------------------------ |
| heading `## Frame N — <frame_id>` | `frame_id` matches the `src` stem; `N` = the 1-based index.                                                                    |
| `src`                             | `compositions/frames/NN-<frame_id>.html` — where the worker writes; the assembler references it. Stem = `data-composition-id`. |
| `duration`                        | the frame span length in seconds (e.g. `7.198s`) — **required**; the assembler sums these for cumulative `data-start`.         |
| `span_sec`                        | `[start, end]` track seconds. `duration = end − start`.                                                                        |
| `pacing`                          | `beat_cut` \| `phrase_flow` — from the skeleton; the worker must obey (no hard-cut on `phrase_flow`).                          |
| `mood`, `feel`                    | from the skeleton; tone + the one-line music situation the planner matched against.                                            |
| `### Groups` list                 | ≥1 group; groups tile the frame span in order.                                                                                 |

## Group entry — exactly one of three kinds

Every group is **template** OR **free_design** OR **asset** — never two, never none. All three
carry `span_sec` (track seconds, tiling the frame) and may carry `copy`.

- **template** — `template: <catalog id>` + `params` (keys from the catalog entry) + `role_bindings` (real audiomap anchor seconds) + `copy`.
- **free_design** — `free_design: { dominant_system, primitives: [catalog ids], density_topology }` + `anchors` (real beat / onset seconds) + `copy`.
- **asset** — `asset: { treatment, clips: [public/…], anchors?, overlay_copy? }`. `treatment` ∈ `beat_cut` (one clip per anchor — only on a `beat_cut` frame) | `ken_burns` (slow push — fits `phrase_flow`) | `bg_under_text` (clip dimmed behind a template / free group). See [`montage.md`](montage.md).

## Rules

- Frames tile the track (gap-free, first at 0, last at `duration_s`); a frame's groups tile its span; no group < ~1 bar; no group boundary inside a `rolls[]` run.
- `params` keys come from the template's [`template-catalog.md`](template-catalog.md) entry.
- All anchor seconds are **track seconds from `audiomap.json`** — the worker converts to frame-local by subtracting the frame start.
- A `phrase_flow` frame MUST NOT use `beat_cut` asset treatment or per-onset hard cuts.
- The brand `style` is set once; every group's palette draws from it.
- Reviewable prose-plus-data; keep it scannable. No GSAP, no millisecond timing.

## Self-check (the planner runs `validate-plan.mjs`)

- frontmatter has `compositionId`, `duration_s` (== audiomap), `canvas`, `style`.
- every frame has `span_sec` + `src` + positive `duration` + `pacing` + ≥1 group; frames tile the track.
- every group is exactly one of template / free_design / asset; template ids exist in the catalog; anchors are real audiomap seconds; `phrase_flow` frames have no `beat_cut`.


<!-- ===== FILE: hyperframes/music-to-video/references/template-catalog.md ===== -->

# Template catalog — the selection menu (Step 3)

Reverse-engineered, asset-free **group templates**. This file is the **only** thing the
planner reads to pick one — you do **not** open the template's `index.html` to choose. One
template realizes **one group** of a frame (a frame may stack several groups; the brand spine
unifies them).

**How to pick.** For each group, read its frame's `pacing` + `mood` + the one-line music
situation from the skeleton, then scan **Reach for it when** + **Best span** below and take the
closest fit. If nothing fits, **free-compose** from
[`motion-primitive-catalog.md`](motion-primitive-catalog.md) — that is a first-class choice, not a
failure.

**Brand comes from `frame.md`, not the template.** Templates ship their own demo palette
(`theme` / `palette` / color params). Fill those params from the project's `frame.md` (the
chosen preset's colors + fonts) so every group reads as one piece — the template supplies the
**motion + layout**, the preset supplies the **look**.

**Params** are listed so you can fill content slots in the storyboard. Exact semantics +
defaults live in each template's `index.html` (`data-composition-variables`) — the frame-worker
reads those at build time; you only name the values.

Pacing tag: every template below is **beat_cut** except `held-message-living-field`
(**phrase_flow**). Never put a beat_cut template on a phrase_flow frame.

## Group duration discipline

Template choice is per **group**, not per frame. A frame longer than a template's **Best span**
should usually split into multiple groups at real audiomap anchors (`SURGE`, `DROP`, roll edge,
hard_stop, phrase edge) instead of stretching one template across the whole frame.

- **Best span** below is the active treatment span: the part where the template's system is doing
  meaningful motion. A short readable hold at the end is fine; a long empty tail means pick another
  group.
- **Frames over ~6s** usually need 2+ groups. Beat-cut exceptions are rich programs with real
  sub-phases (`poster-tile-mosaic`, sometimes `card-flyby`); phrase-flow exceptions use
  `held-message-living-field`.
- **Roll templates are one-roll tools.** If a frame has two rolls or a drop between rolls, split it
  into two groups.
- Do not extend by slowing every tween. Preserve the template's motion feel, then fill extra time
  with a hold / palette change / new group.

---

### card-flyby

- **What** — a depth column of cards rolls forward through perspective; each landing beat tumbles the next card into the front slot with a solid colored wipe, the old front falls toward camera, dwells shrink card-to-card so the deck accelerates into a held final card.
- **Reach for it when** — a stream of discrete onsets that **accelerate** (gaps shrinking / a build into a downbeat) and you want to flash a **sequence of items** — titles, projects, posters, tiles — one per hit, climaxing on a held card.
- **Best span** — **4-6.5s** for 4-7 landings plus a short final hold; split at the next downbeat if it wants to run **>7s**.
- **Params** — `theme`, `bgColor`, `cards`, `landings`, `yaw`

### held-message-living-field · phrase_flow

- **What** — a readable mark (logo / word / title) held dead still over a soft, color-shifting blurred field; only the field breathes.
- **Reach for it when** — a **calm / sparse** stretch with an onset desert — energy present but few or no onsets (a held pad or riser); you have one word or mark to hold and let breathe.
- **Best span** — **6-16s**; this is the long-group exception. Under 4s feels underdeveloped; over ~20s needs a state change or another group.
- **Params** — `markText`, `titleText`, `tagText`, `palette`, `flowSpeed`, `duration`

### held-text-strobe-burst

- **What** — a dead-still word whose letters flip through texture-filled frames (texture-clipped fill + per-frame tint + bg color) every ~3 frames, in short bursts pinned to a roll.
- **Reach for it when** — a **dense, hard-hitting roll / fill** and a single word you want to strobe through textures for a few bars. (Ships texture-mask PNGs under `assets/`.)
- **Best span** — **1.2-3.5s**; strobe fatigue starts fast, so cap at ~4s and cut to a cleaner system.
- **Params** — `markText`, `fontStyle`, `markScale`, `idleColor`, `idleInk`, `frames`, `strobePlan`, `decor`, `duration`

### intro-kinetic-cascade

- **What** — a line laid out as a sequence of big editorial **phrases** (each a stacked poster with one enlarged hero word), revealed word-by-word on its anchors, hard cut between phrases, climaxing on a phrase that slides in with a swappable ringing **icon** (bell / cursor / sparkle / emoji / SVG).
- **Reach for it when** — an **intro / opening statement**: a short line to land word-by-word as big type, climaxing on one keyword + an icon. Medium-or-more energy, steady grid.
- **Best span** — **3.5-7s** for 2-4 phrase beats; if the statement needs more time, make the next clause a new group.
- **Params** — `theme`, `icon`, `phrases`, `climax`

### logo-split-lockup-pulse

- **What** — a two-part mark joined at center splits left↔right to open a gap, grows a center word-lockup one word per onset (key word lands on the downbeat surge), snap-closes on a hit, then pulses with the beat.
- **Reach for it when** — a short **logo / brand sting** (not a typed sentence): fast dense onsets + a sustained roll bed to pulse on, with a left/right bracketing mark.
- **Best span** — **2-4s**; at **>4.5s** it reads like a sting stretched too long. Follow with a separate held-lockup / next idea group.
- **Params** — `bgColor`, `markColor`, `textColor`, `leftMark`, `rightMark`, `word1`, `word2`, `word3`, `word4`

### poster-tile-mosaic

- **What** — a packed **mosaic** of different-sized colored tiles that tessellate to fill the frame (no overlap), driven by interchangeable beat-synced operations: staggered enter/exit, locked global recolor, snake-fill + overlay.
- **Reach for it when** — many discrete, individually-placeable onsets (a hit for every tile move) with distinct sub-phases you want articulated differently (accumulate → recolor-on-roll → fill-then-drop). A dense section best held as **one** rich tile program rather than split.
- **Best span** — **4-7s**, up to **8s** only when the program has clear sub-phases. If the music changes regime, split even if the tile system could continue.
- **Params** — `bgColor`, `tiles`, `bands`, `gap`, `showText`, `labels`, `program`

### roll-flipbook-word-cycle

- **What** — a hi-hat roll drives a centred word that flips every 16th-note through a word list; optionally the flicker resolves and locks into a final phrase.
- **Reach for it when** — a **fast sustained-fill roll** (hundreds of hits/min, ~16th-note) with no single readable message — fill the roll with a rapidly-cycling word flipbook.
- **Best span** — **1.2-3.8s**, one roll into one resolve. Two rolls, or a drop between rolls, means two groups.
- **Params** — `bgColor`, `textColor`, `accentColor`, `flipWords`, `resolveText`, `periodChar`

### split-anchor-word-slot

- **What** — a held left anchor column of fixed-word rows beside a torn-paper word-slot box on the right, driven by beat-synced operators: anchor lock-in, slot word-group cycle (in/out + per-line color), full-scene background flip, per-beat jitter, box-zoom exit wipe. Row count + number of flips are data.
- **Reach for it when** — a short section with a **held idea** (a brand / name to anchor on the left) **and** a stream of onsets popping separate words on the right, plus a dense run to ride a shake on and a strong downbeat to wipe out into.
- **Best span** — **3-6s**; above ~6.5s the fixed anchor goes stale unless the right slot enters a new group/program.
- **Params** — `bgColor`, `anchors`, `theme`, `showText`, `program`

### typewriter-phrase-keyword-shuffle

- **What** — words type in one-per-onset to spell a phrase, then one keyword cycles typefaces on the beat while everything else holds dead still.
- **Reach for it when** — a steady grid with a **continuous onset stream** (no desert): a phrase to type out, then a keyword to shuffle. The inverse of `held-message-living-field` (which wants an onset desert).
- **Best span** — **2.5-5s**; if the phrase cannot type and shuffle inside ~5s, reduce words or split the sentence across groups.
- **Params** — `bgColor`, `textColor`, `accentColor`, `lead1`, `lead2`, `lead3`, `keyword`, `periodChar`


<!-- ===== FILE: hyperframes/music-to-video/sub-agents/frame-worker.md ===== -->

# Frame worker — per-frame composition author (music-to-video)

You build one frame's composition file: `compositions/frames/<frame_id>.html`. Siblings build the other frames in parallel. The generic HyperFrames law — sub-composition shape, timeline registration, determinism, layout — lives in `hyperframes-core` (`references/sub-compositions.md`

- `determinism-rules.md` + `data-attributes.md`); read it first. This file covers the music-specific part.

Your job: **follow the manual, fetch the materials, assemble.** The storyboard tells you WHAT (the frame's groups, each group's template / primitives, content, brand, real beat-anchor seconds). You decide HOW (fetch the materials, bind them to this frame's audio seconds, micro-timing, layout, namespacing).

## Inputs (your dispatch context)

- `PROJECT_DIR` — project root; all paths relative to it.
- `frame_id` — the frame file's stem, e.g. `02-f2`. Use it verbatim as the composition id, the `window.__timelines` key, and the filename `compositions/frames/<frame_id>.html` (the assembler matches on it).
- Your **`## Frame N` block** in `STORYBOARD.md` — its `span_sec`, `pacing`, `mood`, `feel`, and its **`### Groups`** list. Each group is one of:
  - **template** — `template:<id>` + `params` + `role_bindings` (real audiomap anchor seconds) + `copy`.
  - **free_design** — `free_design:{dominant_system, primitives, density_topology}` + `anchors[]` + `copy`.
  - **asset** — `asset:{treatment, clips, anchors?, overlay_copy?}` (see `montage.md`).
- `audiomap.json` — timing truth; use the seconds you're given.
- `frame.md` — the brand (palette + type). Pull every visual token from here.
- **Materials** — `references/templates/<id>/index.html` (its `data-composition-variables` give the param semantics) for template groups; `references/motion-primitives/<id>/scene.html` (the sub-composition; `index.html` only mounts it and holds the page background and font) for free groups; staged `assets/…` for asset groups.
- Canvas `<width>×<height>` and the frame's `pacing`.

If your dispatch carries `lint` / `check` feedback from a prior pass, address each finding.

## What comes fixed — realize it as given

- **No plan = stop.** If your `### Groups` is `TBD`/empty (Step 3 was skipped), report back and write nothing — never invent groups, templates, or copy.
- **The plan** is set in your `## Frame` block: the groups, templates / primitives, copy, brand, and anchors. Build it as written. If a plan is genuinely wrong (wrong template or copy), stop and report — the orchestrator re-plans at Step 3.
- **Transitions** are the assembler's: it hard-cuts between frames. You author the frame's **internal** group→group cuts only.
- **Audio** lives on the root `index.html`; your frame is silent.
- **GSAP** is loaded by the host; use the global `gsap` (your frame carries no gsap `<script>`).
- **Duration** is the frame span length; build your timeline to run `0 … span_len`.

## Build

1. **Read** your `## Frame` block, `frame.md`, and the body of every template / primitive it cites. Reproduce those recipes.
2. **Work in frame-local time.** Subtract the frame start from every anchor: `local_t = track_t − span_sec[0]`.
3. **Author** `compositions/frames/<frame_id>.html`: a `<template>` wrapping `#stage` (`data-composition-id="<frame_id>"`), with all `<style>` / `<script>` inside it, and one paused `gsap.timeline({paused:true})` registered at `window.__timelines["<frame_id>"]`, built synchronously, ending in `tl.seek(0)`. Give each group its own container; show it across its frame-local span with `tl.set("#g1",{autoAlpha:1}, start)` / `tl.set("#g1",{autoAlpha:0}, end)` (this 0ms swap is the group→group cut); namespace each group's ids and shader uniforms `g1_` / `g2_`. When forking a template, inline its DOM / CSS / tweens and use the host's global `gsap`. On a `phrase_flow` frame, pace by phrase / energy.
4. **Self-check and finish.** Run the checklist and fix in place. Writing the file is your terminal action; the orchestrator runs `lint` / `check` and snapshots after assembly (Step 6) and re-dispatches you with any finding.

## Self-check

- `<template>`-wrapped `#stage`; `data-composition-id` == timeline key == filename stem == `<frame_id>`; all `<style>` / `<script>` inside `<template>`; uses the host's global `gsap`.
- One paused timeline, registered, ending in `tl.seek(0)`; `data-duration` == frame span length; silent.
- Each group shows across its frame-local span and hides outside it; `t=0` renders; group→group cuts are 0ms; ids / uniforms namespaced.
- Each group's text / palette match its block's `params` / `copy`, drawn from `frame.md`.
- `phrase_flow` frames pace by phrase / energy.
- Seek-safe per `hyperframes-core/determinism-rules.md` (derive variation from indices; swap text / numbers with `tl.set`).
- Asset clips: muted `<video>`, direct children of `#stage`, with `data-start` / `data-duration` / `data-track-index`. Crossfade outgoing clips to `opacity:0` ending at the next anchor.
- Final frame is intentional; hero text is readable and clear of the edges.
