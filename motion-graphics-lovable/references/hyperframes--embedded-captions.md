

<!-- ===== FILE: hyperframes/embedded-captions/GUIDE.md ===== -->

---
name: embedded-captions
description: >
  Add captions or subtitles to an existing single-subject talking-head video without editing the
  footage. Use for plain verbatim captions, cinematic captions embedded behind the subject, VFX
  captions, “炸/特效/酷炫字幕,” or a named identity from the 35-style catalog. Route by visual
  identity, not by backend engine. The quiet `anchor` rail is the default; embed every word only
  when the user explicitly wants a fully cinematic treatment. The workflow runs locally end to end,
  including transcription and subject matting; split multi-shot footage before applying it.
---

**Plugin installs:** Before setup or freshness commands, follow [plugin execution rules](../hyperframes/references/plugin-installation.md) when this skill is inside a HyperFrames plugin. Standalone installs keep the update instructions below.

> **First, keep this skill fresh — confirm with the user before running:** `npx hyperframes skills update embedded-captions`. A fast no-op when everything is current; otherwise it refreshes this skill plus the core domain skills it depends on before you rely on them.

# Embedded Captions

**One catalog, picked up front** ([CATALOG.md](CATALOG.md) — 35 identities; the engines behind it are backend detail). **Standard** (default) builds a clean verbatim **rail** (lower-third subtitle carrying most text) + an **embed** climax composited _into_ the scene behind the subject at the peak. **Cinematic** is pure embed — no rail, every caption composited behind the subject (hero typography, accumulation, occlusion as the effect). **Theme** is a complete themed constitution — body paradigm × hero setpiece × front fx × plate reaction, composed from registries ([themes/README.md](themes/README.md)): `ordnance` `terminal` `neonsign` `stardust` `stomp`. Most explainer / voiceover is **Standard**; **embed is the scarce, earned peak** — embedding every word is the common mistake; Theme is for VFX-grade asks ("炸", "特效", "像 AE 做的").

---

## Runtime prerequisites

Plugin installs use the bundled, manifest-pinned CLI for matting, transcription,
and rendering; no source checkout is required. The local preview and caption
measurement helpers also need Sharp, Puppeteer (with its Chromium browser), and
GSAP. Install these in the **caption project**, not inside the read-only plugin:

```bash
npm install --prefix <project> --save-dev --save-exact sharp@0.35.3 puppeteer@25.8.0 gsap@3.15.0
```

Keep the project's lockfile. If these dependencies already exist, use its locked
versions instead of overwriting them. Bash and FFmpeg/ffprobe must be on PATH.
Matting and transcription may download their own models on first use.

Rendering waits for the CLI to exit successfully before compositing. The old
`HF_TIMEOUT_S` shell watchdog is no longer used: a large partial file is not proof
that rendering finished. An explicit built-checkout argument or `HYPERFRAMES_ROOT`
selects the contributor CLI instead of the plugin pin. Cancel a stalled render normally through the CLI/terminal;
the caption helper does not force-kill or recover a render from a process snapshot.

## Operational flow (TL;DR)

Routed through `/hyperframes`, the intent layer confirms only the input (which clip) and **announces** the identity pick as a deferred ask — the shortlist needs the probed clip, so it stays at step 1 below; the layer's run-shape questions don't apply (the footage is untouched, there is no storyboard to review). A `BRIEF.md`, when present, carries the confirmed input and any user notes — read it first.

The craft prose below is long; the **pipeline itself is short** — and everything deterministic is computed or compiled, never hand-written:

1. **Decision gate** (refuse bad clips) → **pick ONE identity from [CATALOG.md](CATALOG.md)** (35 identities; engine/compiler derived by lookup — never surface a mode/category question)
2. `hyperframes init` (skip it if the project dir already exists with the video inside — `matte.cjs`/`transcribe.cjs` adopt any video in the dir as source.mp4) → **`bash scripts/prepare.sh <project>`** (matte ∥ transcribe ∥ audio-envelope in parallel, then safe-zones v2 with scene palette/optics/lighting — one command, nothing forgotten)
3. **author a small JSON of creative choices** (read `safe-zones.json` first): Cinematic → `cinematic.json` → `make-cinematic.cjs` (derives `plan.json` and compiles it); Theme → `theme.json` → `make-theme.cjs` (rail/panel/poem/takeover paradigms; `anchor` is the quiet rail default)
4. **Visual QA**: `node scripts/preview-frames.cjs <project>` → faithful composite previews in ~2s/frame (no render). Check § Visual QA before paying for a render.
5. `render-and-composite.sh` → gates (timing / occlusion+hero / overflow / hand-off) → `final.mp4`

Load-bearing rules people miss:

- **rail (default) + embed (promotion).** `drop` (filler, not shown) / `rail` (verbatim lower-third subtitle, in front, carries most text) / `embed` (a peak word composited behind the subject). **Standard mode does both**, embedding only the peak(s). See **§ Caption model**.
- **The video is delivered UNTOUCHED (Standard/Cinematic; **Theme mode's PLATE budget is the one sanctioned exception** — register-gated reaction beats (charge-dim, punch, shake, grain) defined per theme DNA and applied AFTER the matte composite so subject+text+plate move as one frame)** — captions are the only thing added; the matte just lets the subject occlude the embed track. Never grade/recolor/scanline the footage.
- Two rulebooks: **rail → [references/rail.md](references/rail.md)** (thin), **embed craft → [references/composition-craft.md](references/composition-craft.md)** (rich, embed-only). Skim by need.

---

## Caption model — rail + embed

Every spoken phrase is one of three things:

|           | What                                             | How it's shown                                                                                                                                                    |
| --------- | ------------------------------------------------ | ----------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **drop**  | filler — um/uh, stutters, self-corrections       | not shown                                                                                                                                                         |
| **rail**  | the default — ordinary spoken content (verbatim) | clean lower-third subtitle, **in front**, readable. A punch word can get an inline `emphasis` highlight (accent colour / active-word pop) — it stays on the rail. |
| **embed** | a promoted peak — the headline beat              | one big word composited **behind the subject** (matte occlusion), designed entrance + exit                                                                        |

**The rail carries most of the text; embed is the scarce, earned peak.** Scarcity is **per beat/block, not per clip**: ≤1 hero per block (thought), never two co-visible, ≥ a beat of air between hero windows (the compiler warns under 0.6s). A short clip → usually 1–2; a long explainer → ~one per section. Among multiple heroes, the **largest authored one is the APEX** (it alone gets the full lockup embed + width-fit raise); smaller ones are **MINOR peaks** that ride their column as oversized emphasis lines (fg, damped motion) — not every beat needs the matte showcase, which is exactly what keeps the apex an event. Embedding every word is still the common mistake.

Rail-surface identities build exactly this (rail = `rail.html`, embed = the climax in `index.html`). Column-flow identities drop the rail and make everything embed-style — recommend them only for mood-over-verbatim asks, never for explainer / voiceover where the words must read (CATALOG.md encodes this per identity).

---

## Step 0 — pick ONE identity from the CATALOG

**One front-end, three engines behind.** The user picks an IDENTITY from [CATALOG.md](CATALOG.md) (35 entries: 10 classic + 25 themed); the engine, compiler and authoring file are derived by lookup from the catalog row. **Never surface "Standard vs Cinematic vs Theme" as a question** — those are backend names (a product has one UX even with several engines). The catalog encodes everything routing needs: reading surface, voice, recommend-for, scene needs, adjacency notes for the genuinely-close pairs (loud↔ordnance, neon↔neonsign, cream↔stardust).

The identity pick is a **preference gate** (`../hyperframes/references/brief-contract.md` § 1): in autonomous mode ("surprise me" / "decide for me"), pick from your shortlist yourself and state the one-line why instead of asking.

Procedure: probe the clip → shortlist 2–3 identities from the catalog → recommend ONE with a one-line why → **the user picks** (autonomous mode: you pick, stating the why) → author that identity's file. Identities are engine-locked (no cross combos; opening one is a validation event — see dna/README.md).

**Always present your recommendation and let the user pick before you author.** Don't silently default.

(The full identity table lives in [CATALOG.md](CATALOG.md) — single source of truth for routing. The engine docs below describe each backend's authoring contract.)

**CATALOG.md is the whole answer space here: this workflow does not search the HyperFrames component registry.** The composition workflows run `npx hyperframes catalog` before authoring a named look; this one must not. Its engines are locked compilers that consume `cinematic.json` / `theme.json` and emit the composition themselves, so a registry item — the `caption-*` blocks included — has nothing to mount into. A registry block styles text on a designed canvas; this skill burns captions into somebody's footage through a matte. When no identity fits the ask, say so and pick the nearest, rather than reaching outside the catalog.

**Recommendation heuristic**: use the "Shortlisting heuristics" in [CATALOG.md](CATALOG.md) — they are identity-level (e.g. "炸" shortlists ordnance/stomp/terminal/loud and picks by WHAT should explode), never category-level. Unsure → `anchor`.

- **Cinematic** → write `cinematic.json` for a locked template, compiled by `make-cinematic.cjs`.
- **Theme** → read [themes/README.md](themes/README.md), author `theme.json`, run `scripts/render-theme.sh` (compiles + renders + plate reaction → **final_fx.mp4**).

---

## Decision gate — RUN FIRST

Probe the video and classify the scene before either mode.

```bash
ffprobe <video.mp4>                    # specs
ffmpeg -ss <t> -i <video.mp4> -vframes 1 sample.png   # at 20/50/80%
```

Read the samples. Refuse if:

- Multiple speakers / hard cuts (split & render each shot, or refuse)
- No human subject (this skill is for talking-head)
- Under 3 seconds, **no speech**, or face never clearly visible — `transcribe.cjs` warns when audio is near-silent (Whisper hallucinates words like "Thank you." over silence); **heed it and refuse** rather than caption fabricated words
- **Source already has burned-in captions / subtitles / heavy text graphics** — adding a second caption system conflicts and the footage ships untouched (no covering/inpainting). Burned text often appears only mid-clip: sample a **1fps contact sheet** (`ffmpeg -i in.mp4 -vf "fps=1,scale=160:-1,tile=10x5" sheet.png`), don't trust 3 spot frames.
- **Transcript is garbage** — non-native/heavy-accent speech can transcribe into confident gibberish. Sanity-read `transcript.json` before authoring; if it doesn't parse as language, try `WHISPER_MODEL=medium` once, else refuse (a verbatim rail of fabricated words is worse than no captions).
- Busy handheld with fast motion (matte flickers)

### Pre-flight probes (cost nothing, prevent the worst failures)

1. **Shot-cut probe.** Sample frames at 20%, 50%, 80%. If a different subject/scene appears, **trim the clip** before the cut.
2. **Letterbox / pillarbox probe.** Black bars on the first frame? Compute safe content rect and constrain caption placement inside it.
3. **Luminance probe.** Sample the caption region's average luminance — `under 60` → light text reads as-is, `60-180` → add the glyph scrim, `180+` → opaque text + scrim (never bare light text). **Cinematic templates are cream+`screen` and LOCKED** — use this probe to _pick a fitting identity_ (bright scenes → `ink`, or the opaque-rail `anchor` theme), never to recolour one.
4. **Identity recommendation by tone (you recommend; the user picks — see Step 0 + CATALOG.md).** explainer / interview / must-read words → rail/panel-surface identities; poetic / social / "cinematic" → column-flow identities by register; "炸 / 特效 / VFX" / named worlds → themed identities. When unsure → `anchor` (words read, scene safe) — but present a shortlist and let the user choose.

---

## Pipeline — 5 steps

```
1. hyperframes init <project> --non-interactive --video <video.mp4> --skill=embedded-captions
2. bash scripts/prepare.sh <project>       # matte ∥ transcribe (parallel) → safe-zones. One command.
                                           #   → frames_fg/ transcript.json safe-zones.json
3. [AGENT STEP — the only creative step] author a small JSON; see below by mode
   Cinematic: author cinematic.json → node scripts/make-cinematic.cjs <project>
   Theme:     author theme.json → bash scripts/render-theme.sh <project>   (compiles + renders + plate fx)
4. node scripts/preview-frames.cjs <project>   # ~2s/frame composite previews → § Visual QA (BEFORE the render)
5. bash scripts/render-and-composite.sh <project>  # gates → final.mp4 + history/ snapshot
   (Theme mode: SKIP steps 3b/5 — render-theme.sh already runs compile + render-and-composite
    + _postfx.sh; the deliverable is final_fx.mp4, final.mp4 is pre-plate-reaction)
```

Step 1's `init` checks the installed skills against the latest on GitHub and updates the global set if any are out of date.

Step 3 differs by mode:

### Step 3 — Cinematic mode (pure embed)

1. **Read `safe-zones.json` first.** Narration planes go in **`zones.hugLeft`/`hugRight`** — clean strips ABUTTING the silhouette (text far from the body reads as floating, not embedded; far corners are the fallback, not the default). The hero defaults to `heroAnchor`/`heroBands.best` (centered ON the subject, ~30–55% occluded). `recommendation:"fg"` moves NARRATION in front for legibility; **the hero stays embedded whenever `heroBands.feasible`** — hero-fg is the last resort.
2. **The DNA is the identity you picked in Step 0** (CATALOG.md) — do not re-open the choice here. Sanity-check it against the scene (bright hero band luma > 150 wants `ink`; full pick guidance lives in the catalog, covering all ten incl. neon / glitch / chrome / velocity). State your pick + why; the user decides. The DNA locks type/palette/blend/motion + hero three-act; safe-zones v2 (`palette`/`optics`/`lighting`) parameterizes it to THIS scene automatically.
3. **Author `<project>/cinematic.json`** — `"dna": "<name>"` + thought-BLOCKS, not raw groups: each block = lines of words (grouped 2–5 at clause boundaries) + the plane it stacks in + per-line `css` (size/weight/style only — no positions) + at most ONE line marked `"hero": true` (the promoted word; `"text"` for display form). Schema: `scripts/make-cinematic.cjs` header.
4. **Compile**: `node scripts/make-cinematic.cjs <project>` — lowers blocks → plan.json → index.html. Generated for you: transcript-sequenced timings, accumulate-within-block, page-flip-between-blocks, **the hero LOCKUP** (a hero block's pre-context, HERO and post-context stack as ONE bonded composition centered on the subject — reading order top→bottom = spoken order by construction; context floats in FRONT while the hero embeds BEHIND = the depth sandwich; a mass rule keeps the hero dominating its context), apex/minor hero split, **reading order by construction**, fg fallback per safe-zones. Then the gates run as usual. _(Hand-authoring plan.json directly remains possible for designs blocks can't express — then run `fill-timings.cjs` + `fit-fonts.cjs` + `make-composition.cjs` yourself.)_

### Step 3 — Theme mode (themed constitution)

**Read [themes/README.md](themes/README.md) FIRST** — paradigm/setpiece registries, linkages, hard rules, and the exact `theme.json` schema.

1. **Pick a theme DNA** by content register (each `themes/<name>.json` has `voice` + `when`). State your pick + why; the user decides.
2. **Author `<project>/theme.json`** — `dna`, `lines` (verbatim, transcript order; 1–5 words each — for `takeover` each line is one CARD), `minors` (emphasis words), `hero:{match}` (the climax word/phrase; leave it OUT of `lines` for embed setpieces, keep it IN for inline setpieces and panel+redact).
3. **Render**: `bash scripts/render-theme.sh <project>` — compiles (verbatim-completeness gate at compile time), renders both layers, composites, applies the plate reaction → `final_fx.mp4`. Use `preview-frames.cjs` between compile and render for Visual QA.

---

## Visual QA — preview BEFORE you render

`node scripts/preview-frames.cjs <project> [t…]` composites **faithful preview frames in ~2s each** (caption layers screenshotted at seek-time + real video frame + matte occlusion + rail overlay = what the final composite will look like at that moment). Default samples = each group/climax window. A full render costs minutes — never use it to _discover_ layout problems.

Check the previews (`<project>/preview/sheet.png`) against this list — these are the failures the geometric gates **cannot** catch:

1. **Washout** — light text over a bright region (window/sign/sky): unreadable → move the plane or change DNA/mode (bright scene → `ink`).
2. **Text-on-text** — captions over the scene's own text/graphics, or two caption groups colliding.
3. **Reading order** — on-screen vertical order must match spoken order; the hero must not sit below later words.
4. **Hero presence** — the climax should be BIG and visibly behind the subject (~30–55% occluded), not a floating label in a margin.
5. **Balance** — one coherent column/band, not scattered fragments; margins breathing; nothing clipped.

Then the **5 positive checks** in [references/reference-bar.md](references/reference-bar.md) (poster test · timid test · one-glance hierarchy · scene handshake · dead-air audit) — the failure list keeps a render from being broken; the positive list is what makes it _designed_. Ship when both pass.

**Fresh-eyes review (recommended for anything user-facing):** you have confirmation bias about your own layout. If you can spawn a subagent, give it ONLY the preview sheet + this checklist and ask for PASS/FIX verdicts per frame ("review these caption previews against the 5-point checklist; answer PASS or the specific fix per frame"). Apply fixes in cinematic.json / theme.json, recompile, re-preview — each loop costs seconds. Render once, when the previews pass.

---

## The DNA registry — ten visual languages (replaces the template catalog)

Both modes draw from **[dna/](dna/README.md)** — ten art-directed visual languages that **parameterize per scene** (accent sampled from the footage, contact shadow along the measured light direction, depth-match blur, RMS-coupled hero amplitude):

| DNA             | Register       | Scene fit                                       | Voice                                                                                              |
| --------------- | -------------- | ----------------------------------------------- | -------------------------------------------------------------------------------------------------- |
| **cream**       | premium-warm   | dark/mid warm scenes                            | Inter + warm cream + screen; glowing emergence hero (successor of cinematic-cream)                 |
| **ink**         | premium        | **bright scenes (luma > 150)**                  | near-black multiply — type printed ON the wall; the bright-scene answer                            |
| **editorial**   | editorial-luxe | introspective / fashion / poetic                | Bodoni Moda, lowercase-italic hero — magazine elegance                                             |
| **keynote**     | tech-premium   | product / launch                                | opaque white Inter 800, dead-center stillness                                                      |
| **documentary** | formal         | interview / serious                             | burn-in reveals, no hero — gravitas IS the style                                                   |
| **loud**        | loud           | hype / sport / social                           | Anton + scene-sampled accent, single-unit slam + ripple; body ANNOUNCES in front (`bodyLayer: fg`) |
| **neon**        | loud-neon      | neon-noir / nightlife / tech-noir (dark scenes) | electric-cyan signage, ignition flicker, the hero powers ON like a sign                            |
| **glitch**      | loud-neon      | digital / hacker / AI                           | RGB-split echoes snap together on landing; machine-percussive timing                               |
| **chrome**      | loud-luxe      | Y2K / fashion-tech / music                      | liquid-metal gradient hero + one sheen sweep during the hold                                       |
| **velocity**    | loud-sport     | sport / auto / fitness                          | every word arrives along its motion vector (streak+skew), hero passes with speed trails            |

Pick by `safe-zones.json` (`heroAnchor.bandLuma`, `palette.temperature`) × content register — [dna/README.md](dna/README.md) has the decision rule. Authoring: `cinematic.json` takes `"dna": "<name>"`.

The engine generates the **hero three-act** from the DNA (no authoring needed): co-visible captions dim (setup) → per-letter entrance with amplitude ∝ spoken loudness (impact) → breathe + glow until exit (afterglow).

(Legacy: `plan.template:"cinematic-cream"` maps to `dna:"cream"` automatically. The retired 54-template library is archived outside this repo and is not distributed with the skill; `_motion.md` remains in-skill as the motion-verb reference catalog.)

---

## Aesthetic decision — tone × shot × platform (input to the catalog shortlist, NOT a second router)

Classify the clip on 3 axes and feed the result into CATALOG.md's shortlisting — this section never picks a mode/engine by itself:

**Tone** (what feel does the content have?)

- documentary | conversational | energetic | poetic | keynote | investigative | music-video

**Shot** (what's the framing?)

- close-up (head + shoulders) | mid-shot (torso+) | wide (full body+) | cut-montage (mixed shots)

**Platform** (where will it play?)

- 9:16 portrait (TikTok/IG/Shorts) | 16:9 landscape (YouTube/web) | 1:1 square | broadcast export

Cross-reference in [references/direction-catalog.md § Classification matrix](references/direction-catalog.md) for direction language — then return to [CATALOG.md](CATALOG.md) to shortlist identities (this matrix informs the shortlist; the catalog is the only routing surface).

## Composition craft (embed track) — read before embedding

The full **embed-track** playbook lives in **[references/composition-craft.md](references/composition-craft.md)**: transcript role-annotation, phrase grouping, planes & clean-zone anchoring, zone coherence, climax pop & readability, edge-breathing, the occlusion 3-step judgement, and accumulation/persistence. It governs how a _promoted_ phrase sits INTO the scene — read it before authoring any embed (Cinematic `cinematic.json` or Standard `index.html`). The default **rail** track has its own, much simpler spec → **[references/rail.md](references/rail.md)**.

---

## Shared knowledge

| Doc                                                                      | What                                                                                                                               |
| ------------------------------------------------------------------------ | ---------------------------------------------------------------------------------------------------------------------------------- |
| [references/rail.md](references/rail.md)                                 | **The rail track** — standard lower-third subtitle spec (the default; carries most text).                                          |
| [references/composition-craft.md](references/composition-craft.md)       | **The embed-track playbook** — grouping, planes, climax pop, occlusion judgement, accumulation/persistence. Read before embedding. |
| [dna/README.md](dna/README.md)                                           | **The DNA registry** — ten scene-parameterized visual languages; how to pick.                                                      |
| [references/reference-bar.md](references/reference-bar.md)               | **The taste bar** — per-register world-class references + the 5 positive checks.                                                   |
| [references/aesthetic-principles.md](references/aesthetic-principles.md) | **The 18 rules.** Beat Veed AI on taste. Read first.                                                                               |
| [references/motion-vocabulary.md](references/motion-vocabulary.md)       | 10 named motion primitives + tone→timing lookup                                                                                    |
| [references/direction-catalog.md](references/direction-catalog.md)       | 10 ship-ready aesthetics + tone×shot×platform matrix                                                                               |
| [references/anti-patterns.md](references/anti-patterns.md)               | Bugs already locked out (CoreML, letter-spacing reflow, etc.)                                                                      |
| [references/scene-types.md](references/scene-types.md)                   | When a wall surface is usable (4 conditions)                                                                                       |
| [references/layout-heuristics.md](references/layout-heuristics.md)       | Plane positioning, clean-zone selection, crown 3 conditions, pillarbox math                                                        |
| [references/typography-presets.md](references/typography-presets.md)     | Font-size × column-width matrix (starting points)                                                                                  |
| [references/caption-grouping.md](references/caption-grouping.md)         | Word → group rules (pauses, sentence boundaries)                                                                                   |
| [references/failure-modes.md](references/failure-modes.md)               | Long tail of dev gotchas                                                                                                           |
| [references/bespoke-vs-presets.md](references/bespoke-vs-presets.md)     | Why presets fail sometimes; clone-and-tweak pattern                                                                                |

**Read the aesthetic principles and direction catalog FIRST.** Everything else is implementation detail.

---

## Non-negotiables

- **Face must never be 100%-covered continuously** — every 0.3s window, face bbox ≥30% uncovered.
- **WCAG contrast** — final render lints; fix palette if it fails.
- **Deterministic** — no `Math.random()`, no `Date.now()`, no `repeat:-1`.
- **Never grade/recolor the video.** The footage ships untouched — captions are the only addition. No full-frame scanlines / duotone / darken / vignette over the a-roll. neon-noir/CRT texture belongs _inside_ a caption element, not over the whole frame.
- **Rail-first for talking-head / explainer.** Don't embed the whole transcript — most text is the rail; embed only peaks. Embedding everything is the default mistake.
- **Embed is scarce + spaced.** ≤1 embed per sentence/beat, never two adjacent or co-visible, ≥ a beat apart, at most one `apex`. climax = per-beat peak, **not** "the single payoff of the entire clip."
- **Matte = the PERSON (hyperframes `remove-background`, u2net_human_seg, Apache-2.0).** Human segmentation by intent, but not surgically: thin offset furniture (mic boom arms) is usually excluded — captions render over it, behind the person — while large salient objects NEAR the subject (a telescope, a desk rig) can still leak into the matte and occlude captions. Objects HELD by the subject (products, phones) may drop out intermittently, letting captions pass in front. NEVER assume: sample `frames_fg/` at 2-3 timestamps before placing the hero, and prefer hero positions clear of any leaked furniture (`heroAnchor` can be skewed by leaks — cross-check against frames_bg).
- **safe-zones is PROP-BLIND — eyeball every band you use.** Zones/heroBands score _subject_ occlusion + luma only: a mic, telescope, or screen sitting inside a "clean" zone is invisible to them (and a prop leaking INTO the matte skews `heroAnchor.centerXPct` off the person). Before authoring, extract ONE frame of each band you intend to use; if a prop lives there, measure its bbox and move/shrink the plane. Two real cases shipped clean only because the agent did exactly this. (Auto prop-saliency is a known gap; zones' `peakLuma` only catches _moving_ bright objects.)
- **Captions stay on-frame.** Cinematic mode hard-gates frame-overflow; Standard mode runs `check-overflow.cjs` as a WARNING (intentional bleed is the only exception — read the warning).
- **Each caption ≥ 0.5s on screen** — shorter = unreadable.
- **Word timings must match transcript.json within 80ms** — a caption firing 500ms off-beat destroys the scene illusion. Cinematic runs `check-timing.cjs --strict` before rendering (via render-and-composite.sh); THEME mode enforces the same timings at compile time instead (make-theme's sequential transcript matcher + verbatim completeness gate — drift is a compile error). Never pack multiple transcript words into one entry (e.g. `"FUTURE OF"` or an `IT` + line-break + `ALL` stack with one start/end) — the second word inherits the first's timestamp and fires early. Split them into separate word entries with their own timings, even if you want them on the same visual line (use CSS `white-space` / natural wrap instead of `<br>`). Creative substitutions where caption text ≠ transcript (e.g. `"15%"` replacing `"fifteen percent"`) are supported — register them in `CREATIVE_SUBS` inside `check-timing.cjs`.
- **Group windows must envelop their words** — `group.in ≤ min(word.start)` and `group.out ≥ max(word.end)` for every group. If `group.in` is later than a word's start, the word is silently delayed until the container mounts (we've shipped 800ms lag bugs from this). The validator enforces this.
- **No two caption groups may overlap in both time AND screen region** — overlapping-in-time captions create text-on-text pileups. Options: (a) **spatial separation** — place each group in a non-overlapping vertical band so they can coexist (memory-wall cascade style); (b) **handoff** — set the earlier group's `out` ≤ the next group's `in` so only one is on screen; (c) **deliberate layered typography** — add `"allow_overlap": true` on one of the groups to silence the validator. The validator estimates each group's vertical bbox from its CSS and flags collisions. Pick (a) by default — it's what makes cinematic-cream feel like a poem accumulating, not a subtitle track replacing itself.
- **Screen-blend fails on bright backgrounds (>180 luminance).** **Cinematic** templates are cream + `screen` and that DNA is **locked** (the plan can't recolour them) → on a bright backdrop they wash out, so pick `ink` (letterpress built FOR bright surfaces) or the `anchor` theme (opaque rail surface) rather than overriding a look.
- **Don't animate `letter-spacing` or `filter:blur` on word entrance** — inline-block reflow causes line-jumps.
- **CoreML banned for matting** — the onnxruntime CoreML EP's mixed-precision partitioning corrupted face alpha (observed with the previous RVM engine; don't re-try it). Matting is CPU-only (~2 fps @1080p ≈ 2-3 min per 10s clip; budget for it on long clips).

---

## Dependencies

- **HyperFrames CLI:** plugin installs use the bundled manifest-pinned launcher. Source contributors can use a built checkout (`packages/cli/dist/cli.js`) via `HYPERFRAMES_ROOT`, the skill’s source tree, or `~/Downloads/hyperframes`.
- **Node-first; two Python touchpoints via `uvx` (no manual installs):** transcription runs WhisperX through `uvx` (word-level timings; falls back to an existing word-level `transcript.json`), and Theme's `drawon` setpiece shells `python3 scripts/gen-stroke-path.py` at compile time. Everything else runs on the toolchain hyperframes already ships: matting via the hyperframes CLI's **`remove-background`** (u2net_human_seg; weights auto-download once, ~168 MB, to `~/.cache/hyperframes/`), image/alpha math via **`sharp`**, layout/occlusion/overflow via **`puppeteer`**, plus **`ffmpeg`**. Install Sharp, Puppeteer, and GSAP in the caption project as described in **Runtime prerequisites** above. The helpers check that project first and retain checkout dependency lookup for source contributors.
- **Transcription = WhisperX via `uvx`** (word-level timings + alignment; no manual install — `transcribe.cjs` drives `uvx whisperx`). Falls back to an existing word-level `transcript.json` if present.
- **Source video** — `matte.cjs` / `transcribe.cjs` auto-resolve `source.mp4` (or glob the clip / read `hyperframes.json`), so `hyperframes init --video X.mp4` needs no manual rename.
- **fps** — `matte.cjs` extracts at the source's native rate and records `matte.fps`; `render-and-composite.sh` uses that so the matte stays frame-aligned.
- Matting weights are NOT bundled: `matte.cjs` shells the hyperframes CLI's `remove-background`, which downloads u2net_human_seg (~168 MB, Apache-2.0) once to `~/.cache/hyperframes/background-removal/models/`. First prepare on a fresh machine needs network for that one download.

If a hard dependency is missing, STOP and ask the user — don't silently skip steps.


<!-- ===== FILE: hyperframes/embedded-captions/CATALOG.md ===== -->

# THE CATALOG — one front-end, three engines behind

This is the skill's single selection surface. **The user picks an IDENTITY from
this table; everything else (engine, compiler, authoring file) is derived by
lookup — never ask the user (or yourself) "Standard or Cinematic or Theme?"**
Those are backend names; a product has one UX even when it has several engines.

Routing procedure (replaces any mode decision):

1. Probe the clip (decision gate + pre-flight probes as in GUIDE.md).
2. Shortlist 2–3 identities from this table by **content register + the user's
   own words + scene constraints**.
3. Recommend ONE with a one-line why; the user picks.
4. Author the identity's file (last column), then render with its engine's
   pipeline. Done — no category question ever surfaced.

## Identities

| Identity      | Reading surface                                          | Voice (one line)                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                      | Recommend for                                                                                                                                                                                                  | Scene needs                                                                                                            | Author → engine                 |
| ------------- | -------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------- | ------------------------------- |
| `cream`       | scene-embedded column flow                               | warm poetic light, emergence + glow                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                   | introspective, narrative, emotional monologues                                                                                                                                                                 | dark/mid-tone warm scenes (luma < 150)                                                                                 | cinematic.json → make-cinematic |
| `ink`         | scene-embedded column flow                               | letterpress pressed into bright surfaces                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                              | the bright scenes everything else washes out on                                                                                                                                                                | BRIGHT scenes (luma > 150)                                                                                             | cinematic.json → make-cinematic |
| `editorial`   | scene-embedded column flow                               | lowercase italic serif, pen-stroke glides                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                             | fashion / beauty / lyrical / premium brand films                                                                                                                                                               | mid/dark scenes                                                                                                        | cinematic.json → make-cinematic |
| `keynote`     | scene-embedded column flow                               | confident centered slides-in-the-scene                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                | launches, founder updates, tech explainers (mood over verbatim reading)                                                                                                                                        | any mid/dark                                                                                                           | cinematic.json → make-cinematic |
| `documentary` | scene-embedded column flow                               | burn-in stillness, bone on charcoal                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                   | interviews, journalism, testimony — gravitas IS the style                                                                                                                                                      | any                                                                                                                    | cinematic.json → make-cinematic |
| `loud`        | scene-embedded, body in front                            | percussion type that competes with the face                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                           | hype, social reels, sport, music, motivational                                                                                                                                                                 | any (counter-accent handles warm)                                                                                      | cinematic.json → make-cinematic |
| `neon`        | scene-embedded column flow                               | captions as neon signage in the dark                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                  | neon-noir / nightlife / tech-noir / music                                                                                                                                                                      | dark scenes                                                                                                            | cinematic.json → make-cinematic |
| `glitch`      | scene-embedded column flow                               | corrupted-feed RGB-split type                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                         | hacker / AI / dystopia content                                                                                                                                                                                 | mid/dark                                                                                                               | cinematic.json → make-cinematic |
| `chrome`      | scene-embedded column flow                               | liquid-metal hero with sheen sweeps                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                   | fashion-tech, Y2K, product-flex                                                                                                                                                                                | mid/dark                                                                                                               | cinematic.json → make-cinematic |
| `velocity`    | scene-embedded column flow                               | every word arrives along its motion vector                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                            | sport, automotive, fitness, kinetic content                                                                                                                                                                    | any mid/dark                                                                                                           | cinematic.json → make-cinematic |
| `anchor`      | verbatim lower-third rail + 1 settled climax             | the quiet professional — fade-up rail that simply reads; the apex settles behind the subject with a drawn accent underline. Discipline IS the style.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                  | explainers, tutorials, corporate, news-adjacent — **where every word must be read**; the conservative default                                                                                                  | any (opaque rail; settle carries a soft veil)                                                                          | theme.json → make-theme         |
| `ordnance`    | stamped verbatim rail + detonation apex                  | military marking system; everything has mass; the room reacts                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                         | punchy announcements, drops, "炸一点 / 像 AE 做的" asks                                                                                                                                                        | any (charge-dim makes its own contrast)                                                                                | theme.json → make-theme         |
| `terminal`    | typed console panel + glyph-decode apex                  | the transcript is a signal log; apex decodes from noise                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                               | tech / data / AI / investigative, "终端/控制台/解码" asks                                                                                                                                                      | cool/dusk preferred                                                                                                    | theme.json → make-theme         |
| `neonsign`    | warm tube rail + hand-written neon apex                  | a sign district at dusk; the apex is WRITTEN stroke by stroke                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                         | lifestyle / music / mood, "霓虹/手写" asks                                                                                                                                                                     | dusk/dark backdrop; needs `python3` (stroke-path gen)                                                                  | theme.json → make-theme         |
| `stardust`    | accumulating poem, condensing letters                    | words condense from dust and return to it                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                             | poetic / memory / science-wonder monologues                                                                                                                                                                    | one clear column side (probe fails → fall back to `cream`)                                                             | theme.json → make-theme         |
| `stomp`       | full-frame takeover cards                                | hard-cut typographic takeover with a void before the drop                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                             | hooks, manifestos, ad openers — the words ARE the show                                                                                                                                                         | any (plate runs dimmed)                                                                                                | theme.json → make-theme         |
| `lastpage`    | manuscript rail + a blurred future-field                 | the future hangs unreadable in the room; one rack-focus reveals every faint line was the apex word                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                    | visionary thesis, prophecy-toned talks, trailers, literary content                                                                                                                                             | mid/dark (the field needs air)                                                                                         | theme.json → make-theme         |
| `scoreboard`  | split-flap chyron rail + departures-board apex           | stadium split-flap mechanics — body words flip-cycle wrong words on tiles before clacking onto the real one; ROW counter + odometer chip furniture; the apex is a giant departures board behind the subject that locks the word letter-by-letter under floodlights and a crowd-flash, status ticker types on                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                          | sports, transit/travel, scores, countdowns, reveals, "翻牌/记分牌/机场大屏" asks                                                                                                                               | any (board + chyron bring their own dark metal contrast)                                                               | theme.json → make-theme         |
| `transit`     | LED departure-strip rail + illumination-wipe apex        | amber dot-matrix station PA — body words light column-by-column (L→R LED wipe + arrival flicker) on a docked departure strip whose lines page by scroll-snap; platform tag, ticking clock, ⚠ DELAYED → ● ON TIME gag; the apex panel expands behind the subject inside a chasing LED-marquee border, the word illuminates column-by-column under a PA flash + ding pulses, then pages up and collapses                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                | travel/transit, announcements, schedules, countdowns, retro-terminal, "LED屏/车站到站/点阵屏" asks                                                                                                             | any (LED strip + panel bring their own dark contrast)                                                                  | theme.json → make-theme         |
| `vhs`         | camcorder OSD rail + REC-FREEZE tracking-slam apex       | tape playback — permanent lens vignette + OSD furniture (▶ PLAY, ● REC, blinking green timestamp); body words carry a permanent red/cyan misregistration fringe, arrive by tracking glitch and REWIND off with flat-white echoes + scrub lines (the deck flips PLAY→REW in dead air); the apex is REC FREEZE: 1-frame white tear + head-switching noise bar, the word slams in behind the subject as three sheared tracking bands that SNAP into register, misregistration breathes through the hold under tape weave + auto-iris, then rewinds off                                                                                                                                                                                                                                                                                                                                                                                                                   | retro / nostalgia / found-footage / home-video, '90s tech, music & lifestyle edits, "录像带/VHS/复古/DV" asks                                                                                                  | any (backlight-comp scrim makes its own contrast on bright skies)                                                      | theme.json → make-theme         |
| `arcade`      | arcade HUD rail + pixel-block boss-intro apex            | 8-bit cabinet attract mode — the frame plays through CRT scanlines + a corner vignette; body words coin-pop onto a bordered HUD bar (blinking 1UP, CREDIT 01) with a 1-frame white blip each, emphasis words run a cyan→magenta palette swap, lines dissolve checkerboard; the apex is a BOSS INTRO behind the subject: the room dims, WARNING blinks twice, ~64 seeded pixel blocks fall quantized into a matrix grid over the word rect, the word flashes ON in Press Start 2P with chromatic ghost layers + a 3-frame palette strobe while letterbox bars slam in and a HI-SCORE odometer rolls top-right; everything dissolves checkerboard and the blocks drop away                                                                                                                                                                                                                                                                                              | gaming, retro-tech, playful hype, launches, achievement/level-up beats, "像素/街机/8-bit/打游戏" asks                                                                                                          | any (boss dim + dark HUD bar bring their own contrast)                                                                 | theme.json → make-theme         |
| `dossier`     | manila case-file strip + rubber-stamp apex               | cold-war case file — carbon Special Elite HAMMERS onto a manila transcript strip char by char (seeded baselines + ribbon ink, every strike kicks the paper; typed case header, CONFIDENTIAL watermark, red ink circles around the evidence; pages are X-row over-struck and carriage-fed away); the apex is a RUBBER STAMP behind the subject: the footage goes sepia-archival, the stamp crushes in at −8° with a double-strike ghost + thin-ink patches, then holds DEAD STILL — sold only by a breathing paper indent — until the page is filed away with a mechanical yank                                                                                                                                                                                                                                                                                                                                                                                        | investigations, exposés, true-crime, document-driven storytelling, declassified/archival framing, "档案/卷宗/解密/盖章" asks                                                                                   | any (the manila strip is self-lit; the stamp brings its own sepia charge)                                              | theme.json → make-theme         |
| `laser`       | beam-ignited rail + 6-beam laser-cage apex               | concert laser rig in a blackout — every body word is IGNITED where a green and a magenta beam converge on it two frames early (flare pop, snap-on, single strobe on emphasis; a sweeper beam carries each line away); the apex is the drop: a 6-beam array sweeps to one hot point, the word ignites behind the subject in an additive glow stack with two controlled strobe pops, a criss-cross beam cage draws around it, the array fans out wide through the hold, then the beams sweep everything off L→R                                                                                                                                                                                                                                                                                                                                                                                                                                                         | music, nightlife, festivals, drops, hype reveals, keynote 'one more thing' beats, "激光/灯光秀/蹦迪字幕" asks                                                                                                  | any (the concert blackout makes its own contrast, bright skies included)                                               | theme.json → make-theme         |
| `thunder`     | rain-washed rail + branched-bolt strike apex             | the storm is the editor — slate storm mood on the room, ambient slanted rain falling in front of the subject, and the sky "kisses" (1-frame brighten) on every body word; rail words arrive with a lit-bright lightning pop (emphasis = sheet-lightning double flash mirrored by a double sky-kiss); the apex is THE STRIKE: a hand-authored branched bolt flashes two frames before the word, the word slams in lit HARD with its shadow flipped toward the bolt, ozone under-glow breathes through the hold while the rain doubles, then everything washes downward with the rain                                                                                                                                                                                                                                                                                                                                                                                   | dramatic reveals, storm/weather content, epic hype beats, trailer-toned monologues, "雷电/闪电/暴风雨字幕" asks                                                                                                | any (charge-dim + radial word scrim make their own contrast, bright skies included)                                    | theme.json → make-theme         |
| `hologram`    | volumetric projection plate + hologram-boot apex         | every caption is LIGHT cast from an emitter — body words boot onto a scanlined projection plate with a rising sweep, a 1-frame interference glitch and a permanent cyan/magenta fringe (emphasis words drop out for 2 frames and restore brighter; lines drift in rotationY and exit by projector cut); the apex is the full volumetric boot: a desk emitter dot pops, the cone snaps wide, a seed beam fires, and the word materializes behind the subject as a 7-layer hologram with climbing interference bands — a hand passes through it before the projector cuts it back to the dot                                                                                                                                                                                                                                                                                                                                                                            | tech / sci-fi / AI / space / imaging explainers, futuristic product reveals, "全息/投影/科幻字幕" asks                                                                                                         | any (the apex scrim + dim make their own contrast; wants a lower frame edge for the emitter dots)                      | theme.json → make-theme         |
| `biolume`     | jellyfish glow-on rail + bioluminescent-bloom apex       | deep-sea bioluminescence — the clip sinks into an abyss grade with a breathing vignette and every caption is a living light: body words GLOW ON like jellyfish (radial bloom from center while a cyan glow breathes in; emphasis words pulse a slow propulsion double-beat) across two coexisting floating rows and SINK away dimming; seeded plankton motes drift the open water and the ones ringing the apex are pulled into the bloom; the apex is the BLOOM behind the subject: a creature pre-glow double-beats and crushes to a point, the word condenses in, six luminous tendrils draw outward like filaments while caustics shimmer, cyan light spills onto the scene and spores burst past — then all the light sinks back into the deep                                                                                                                                                                                                                   | ocean / nature / science-wonder docs, dreamy or meditative monologues, slow night-time reveals, "深海/发光水母/水下字幕" asks                                                                                  | any (the abyss grade + pocket scrim make their own contrast on bright scenes)                                          | theme.json → make-theme         |
| `aurora`      | iridescent sheen rail + silk-ribbon draw-on apex         | polar-night elegance — two huge aurora blobs drift the sky all clip; body words are silk serif ink whose rose→teal→violet sheen drifts continuously through the letters (entrance = 2-frame flow-on + y8 settle; emphasis = one bright highlight sweep marching through the word), lines share two coexisting rows like a woven couplet and dissolve UPWARD into drifting light streaks; the apex is a SILK RIBBON: the hero word is hand-WRITTEN into the sky behind the subject stroke by stroke (script single-line font, blurred halo + bright core, a light mote riding the pen) and the aurora gradient keeps FLOWING through the drawn ribbon during the hold while a soft spill tints the sky and light motes rise past the subject — gentle, no shake                                                                                                                                                                                                        | dreamy / romantic / wonder content, night-sky and travel pieces, poetry, weddings, elegant brand films, "极光/丝带/优雅手写字幕" asks                                                                          | any (apex scrim + dark understroke carry contrast on bright skies; loves dusk/night)                                   | theme.json → make-theme         |
| `spectrum`    | oscilloscope scope-band rail + phosphor trace-write apex | an oscilloscope is listening — a dark scope band hosts an ALWAYS-ALIVE waveform (seeded pseudo-RMS envelope: speech grows it, silence flattens it, every word arrival kicks a local burst) under VT323 phosphor lines that wipe in L→R over reserved slots with a 2-frame just-traced flash (emphasis words get a ticking frequency-readout chip, the trig LED blinks on every word); the apex is the trace itself LEAPING off the scope (surge column) to hand-WRITE the hero word in a thin phosphor script stroke, fill flicker-on, hum + breathe, then COLLAPSE to a flatline before the next spoken word — and on the FINAL word the trace explodes to max-amp chaos, flatlines to a single dot and stamps SIGNAL LOST                                                                                                                                                                                                                                           | science / signal / audio / measurement / astronomy explainers, data-nerd content, retro-lab or synth aesthetics, "示波器/波形/信号字幕" asks                                                                   | any (the scope band brings its own dark glass; the apex scrim handles bright skies); needs `python3` (stroke-path gen) | theme.json → make-theme         |
| `papercut`    | paper-chip craft rail + stop-motion papermat apex        | stop-motion paper craft — the frame becomes an animator's table: body words are cream paper chips PLACED one by one (steps(2) drop, seeded crooked, ~5fps wobble) on a kraft strip with torn top edge, washi-taped corners and a handwritten cut&paste tag; emphasis words get a washi-tape slap, the final word is an accent-red sign-off chip, and a red paper star stands in for the hero word; the apex is a torn kraft mat slapped down behind the subject where torn-edge letter chips DROP with stepped gravity + anticipation shadows, land crooked, settle in 12fps poses, wobble at 8fps while a warm vignette charges — then the FINAL word bumps the table and everything scatters off down-right                                                                                                                                                                                                                                                         | craft/DIY, kids & family, indie product demos, behind-the-scenes, maker channels, "手工/剪纸/定格动画字幕" asks                                                                                                | any (kraft strip + cream chips bring their own warm contrast)                                                          | theme.json → make-theme         |
| `popup`       | pop-up book page rail + centerfold starburst apex        | a pop-up book opens inside the frame — body words POP UP on a baseline hinge (rotationX back.out, paper overshoot, a growing back-shadow) along a cream page strip that unfolds from the bottom edge (center foldline, two alternating reading rows); emphasis words land bigger with a contact squash the page FEELS (1px strip dip), then flick-wobble with a blue paper strut leaning in behind; line exits fold flat in an L→R wave (the page closing), the whole page TILTS on the final word and the strip folds shut on the last frame; the apex is THE CENTERFOLD: blue + cream 12-point paper starbursts unfold behind the subject, the hero word pops up in three hinged clip-path segments, kraft struts lean in, backdrop + word wobble-settle TOGETHER and breathe through the hold — then the whole spread folds flat before the next sentence; a blue paper star holds the hero slot on the rail and paper confetti flicks past the subject at the pop | kids and family content, storytelling, education, greeting-card / wholesome brand spots, picture-book and craft channels, "立体书/弹出书/纸艺字幕" asks                                                        | any (the cream page strip is self-lit; the apex dusk scrim guards bright skies)                                        | theme.json → make-theme         |
| `chalkboard`  | chalk-band rail + hand-written chalkwrite apex           | night lecture — a worn deep-green chalk band where every word is SCRIBBLED in fast chalk (2-frame pop + steps(4) scribble reveal + dust puff at the base, seeded crooked); emphasis gets double underline dashes, the final word lands in yellow chalk, and between sentences an ERASER SWIPE smears the old words off (blurred light band, ghost smudges stay — chalk never fully erases); the apex: the band GROWS into a full blackboard behind the subject and the hero word is HAND-WRITTEN 130px tall stroke by stroke (jittered chalk nib, dust falling from the pen, blurred halo under a tight core), finished with a hand-slap dust CLAP in front of the subject + a 1-frame board shake and two violent accelerating underlines, then the halo breathes through the hold                                                                                                                                                                                   | education / explainers, science and lecture content, teacher channels, documentary asides, "黑板/粉笔/板书/老师讲课字幕" asks                                                                                  | any (the deep-green board brings its own contrast); needs `python3` (stroke-path gen)                                  | theme.json → make-theme         |
| `graffiti`    | marker rail + spray-tagged handstyle apex                | street bombing run — marker words FLICK onto the rail crooked (1-frame squeak skew, seeded rotation, back.out settle); emphasis takes alternating yellow/magenta paint + a spray-underline swoosh with overspray dots; spent lines are ROLLER-BUFFED away (gray roller sweep, wet smear lingers) and the final word lands BIG in yellow with the punch; the apex: the dusk wall dims, the can RATTLES, and the hero word is spray-TAGGED stroke by stroke behind the subject in fat yellow paint (dark under-stroke armor + blurred overspray halo + glowing nib + seeded overspray dots), paint DRIPS grow from the low points through the hold, a magenta paint splat pops at the pen-finish and the plate punches on it                                                                                                                                                                                                                                            | street culture, hip-hop / rap, sneaker & fashion drops, urban sports, skate/BMX, rebellious brand spots, "涂鸦/喷漆/街头字幕" asks                                                                             | any (the dark under-stroke armors the tag against bright skies); needs `python3` (stroke-path gen)                     | theme.json → make-theme         |
| `brush`       | washi paper-band rail + sumi-e brush-gesture apex        | sumi-e study — a deckle-edged washi paper band swipes in behind a traveling brush-head shadow; body words are brush-WIPED on in a Mincho serif (clip reveal behind a per-word brush head, seeded ±1° tilt), emphasis gets a double curved ink underline, and spent lines are wiped OFF right-to-left like a wet cloth (erase brush head riding the wipe); the apex: a warm paper wash charges behind the subject and the hero word is written in ONE violent calligraphic gesture — pressure-tapered wet brush (four stacked stroke widths, blurred bleed underneath), start-SPLAT at the first pen contact with ink flecks kicking past the subject, spatter droplets ejected at the sharpest curves — then the ink BLEEDS into the paper through the hold (the work breathes) and a vermilion SEAL chop (観) stamps beside the ink with the plate punch                                                                                                             | calm-authority explainers, craft / design / philosophy / Japan-adjacent content, tea / meditation / writing channels, elegant brand films, "水墨/毛笔/书法字幕" asks                                           | mid/bright scene band (dark ink + its paper wash carry the contrast); needs `python3` (stroke-path gen)                | theme.json → make-theme         |
| `inkwater`    | three-row ink rail + ink-drop bloom apex                 | sumi ink dropped in still water — paper-white radial washes back the text zones, Mincho-serif ink words BLEED into three fixed reading rows (blur+scale bleed over a paper-glow halo, dark blurred halo overshoots then tightens, an ink-settling hairline under each line, emphasis sheds a curling ink wisp) and spent lines re-dissolve upward like dispersing ink; the apex: a dark drop falls behind the subject, hits an invisible water surface at the word point and BLOOMS (three stacked blurred ink ellipses at counter-rotating rates + two thin ripple rings) while the world stills under a gentle vignette — the hero words resolve out of the blob on their own spoken times, breathe at the glyph edges through the hold, then re-dissolve before the next thought needs the reader                                                                                                                                                                  | contemplative / literary / scientific-wonder narration, astronomy / nature / memory / essay films, poetry and slow-craft channels — one liquid meditative event instead of an impact, "水墨滴落/墨水字幕" asks | mid/bright scene band (dark ink + its paper washes carry the contrast)                                                 | theme.json → make-theme         |
| `ransom`      | cutout-chip collage rail + ransom-note slam apex         | kidnapper's collage — every word is a chip clipped from a different page (cream Anton / black Inter / newsprint typewriter / accent-yellow marker, torn edges, hard offset shadows) PASTED crooked on the rail with misaligned baselines (the apex slam at low amplitude); emphasis words get a 1-frame RE-PASTE lift (shadow grows, rotation flips sign for good) and spent chips are RIPPED off one by one under 1-frame paper-tear flashes; the apex: a collage scrim darkens the sky and the hero word slams in letter by letter as a ransom note BEHIND the subject — each letter a different cutout chip, flight shadow popping tight on contact — the whole word JOLTS as the last letter lands (the plate punches with it), looms crooked through the hold, then is torn off chip by chip while the closing line speaks                                                                                                                                       | true crime, mystery / thriller, heist energy, punk / DIY zine aesthetics, edgy drops, unhinged-comedy hooks, "勒索信/剪贴/拼贴字幕" asks                                                                       | any (solid chip backgrounds carry their own contrast; the apex scrim guards bright skies)                              | theme.json → make-theme         |

## Shortlisting heuristics (identity-level, not category-level)

- **"每个词都要被读到 / accessibility / 教程·新闻"** → rail or panel surfaces:
  `anchor`, `ordnance`, `terminal` (all verbatim by construction).
- **"嵌进场景 / 电影感 / 高级"** → the column-flow ten; pick by register + scene luma
  (bright → `ink`; warm dark → `cream`; fashion → `editorial`; …). Bright + must-read → `anchor`.
- **"炸 / 特效 / 酷炫 / 像 AE"** → `ordnance`, `stomp`, `terminal`, `loud` — pick by
  what should explode: a word (`ordnance`), the frame (`stomp`), a decode (`terminal`),
  every beat (`loud`).
- **Named worlds** → direct hits: 控制台/终端 → `terminal`; 霓虹/招牌 → `neonsign`;
  诗/星尘/记忆 → `stardust`; 军事/重击 → `ordnance`; 预言/未来/悬念揭示 → `lastpage`;
- **Scene constraints veto last**: luma > 180 kills cream/screen column looks
  (→ `ink` or a rail/panel surface); dusk/dark unlocks `neon`/`neonsign`.
- **Unsure** → `anchor` (the conservative default: words read, scene safe, zero spectacle).
  EXCEPTION: if the ask literally says "嵌进场景 / embed into the scene / 电影感", that signal
  OUTRANKS the conservative default — go column-flow (pick by register + luma), not a rail.

Adjacencies worth knowing (these pairs are why the old mode question was hard —
recommend by the difference, don't agonize over category): `loud` vs `ordnance`
(percussive type vs a themed world with plate reaction) · `neon` vs `neonsign`
(neon-styled captions vs a sign being written) · `cream` vs `stardust` (warm
embedded flow vs an accumulating poem with semantic dispersal) · `terminal` vs
`glitch` (a console WORLD with typed log + decode vs corrupted-feed styling on
normal captions) · `stomp` vs `loud` (every beat takes over the dead-center
frame vs energetic type that still shares the frame with the subject).

## Rules

- Identities are **engine-locked** — no cross combos. Opening a new combo (e.g.
  another DNA under rail) is a validation event: render → user review → flip the
  DNA's `deliveries.rail` flag (see dna/README.md).
- New identities join via their family's registry rules (dna/README.md for
  classic, themes/README.md for themed — "any input, zero hand-fixing" bar).
- The engines' internals (Standard/Cinematic/Theme compilers, gates, layers)
  are documented in their own files; this catalog is the only routing surface.


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


<!-- ===== FILE: hyperframes/embedded-captions/references/bespoke-vs-presets.md ===== -->

# Bespoke design vs. presets — when to override, when to clone

The 5 preset styles (`intro / phrase / emph / dream / crown`) and the 3 templates (`wall-embed`, `corner-column-crown`, `portrait-header`) are **scaffolds**, not rules. The best renders we've shipped all override presets for specific groups because **typography is a per-scene decision**, not a general rule.

If you only use presets, your render will look generic. If you only copy existing renders, your skill won't adapt. The right workflow is:

1. **Decide the shape first** (template choice, plane position, blend mode).
2. **Check if a canonical example is close enough** → clone and tweak words + timings.
3. **Otherwise start from presets** → override per-group via `custom_css`.

---

## Canonical example renders

Full HTML for two validated renders is in `references/example-renders/`:

| File               | Scene                                                   | What makes it work                                                                                                                                                                                         |
| ------------------ | ------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `memory-wall.html` | Introspective monologue, right-side foam wall, mid-tone | Right-aligned cascade, per-group bespoke sizes (`cap-1` 78 italic / `cap-2` 66 italic + right hanging-indent / `cap-3` 72 upright / `cap-4` 90 uppercase). `mix-blend-mode: screen` for the dark-ish foam. |
| `champion.html`    | Podcast interview, cluttered bookshelf, 1920×1080       | Upper-left column + center-stage crown. Tuned preset class sizes (`cap-intro` 52 / `cap-phrase` 60 / `cap-emph` 70 / `cap-crown` 140). `screen` blend reads the shelves through text.                      |

**When a new scene matches one of these closely** (similar framing, similar subject-center, similar backdrop type): clone the HTML and only replace the GROUPS array + word timings. Don't re-derive the design from presets — you'll lose the specific choices that took many iterations to validate.

---

## When presets are wrong

You'll reach for presets like `"style": "emph"` when what the scene really needs is:

### "This cap is at position N and deserves its own treatment"

`memory-wall.html` uses `cap-1 / cap-2 / cap-3 / cap-4` — **position-indexed**, not role-indexed. Each one is a bespoke design for a specific phrase at a specific point in the arc:

- cap-1 (soft opener, 4 words): 78px italic 600 — feels like a whisper
- cap-2 (dreamy modifier, 3 words): 66px italic 500 + `padding-right: 44px` — hanging indent creates ragged right-edge stagger
- cap-3 (turn, 2 words): 72px upright 700 — the syntactic pivot, no italic
- cap-4 (climax, 4 words): 90px uppercase 900 — three lines cascade right-aligned

`phrase/emph/intro` can't express "this cap has a hanging indent" or "this cap is the syntactic pivot". When that matters, invent your own class names:

```json
{
  "template": "wall-embed",
  "custom_css": "
    .cap-1 { font-size: 78px; font-weight: 600; font-style: italic;
             letter-spacing: -0.01em; }
    .cap-2 { font-size: 66px; font-weight: 500; font-style: italic;
             padding-right: 44px; }
    .cap-3 { font-size: 72px; font-weight: 700; letter-spacing: -0.015em; }
    .cap-4 { font-size: 90px; font-weight: 900; letter-spacing: -0.03em;
             text-transform: uppercase; line-height: 1.0; }
  ",
  "groups": [
    { "id": "cg-0", "style": "1", "words": [...] },
    { "id": "cg-1", "style": "2", "words": [...] },
    ...
  ]
}
```

The `"style": "1"` field becomes `class="cap-1"` on the element — any string works, no validation.

### "The template's blend doesn't suit this backdrop" → pick a different template, do NOT override

**Cinematic mode does not override colour or blend.** A template's `mix-blend-mode` + fill are **locked DNA** — `make-composition.cjs` ignores `plan.cap_color` / `blend_mode` / `text_shadow` / `text_filter`. Selecting a template commits to its look; the only agent-authored things are layout (planes/positions) and per-group typography.

So use the caption-region luminance to **choose** a template that already fits — never to recolour one:

| Region luminance                  | What fits                                                                                     | Why                                                                        |
| --------------------------------- | --------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------- |
| < 60 (dark / low-key)             | a cream + `screen` template (`cinematic-cream`, `memory-wall`, `champion`, `portrait-header`) | light text glows, picks up the scene                                       |
| 60–180 (mid-tone)                 | a cream + `screen` template still reads (add a scrim via Standard if marginal)                | text picks up texture                                                      |
| > 180 (bright: window, pale wall) | **none of the cream/`screen` Cinematic templates — they wash out**                            | → use **Standard mode** (opaque rail, set per the chosen template) instead |

If the scene is bright and the cream/`screen` look washes out, that's the signal to switch to **Standard mode** (which sets opaque colour in the HTML), not to recolour a Cinematic template into something it isn't.

### "Hanging indent / outdent / letter-width tweak"

These are per-group affordances you'll occasionally need. Express via `custom_css`:

```css
#cg-2 {
  padding-right: 44px;
} /* right-aligned: shrinks right edge, creating left outdent */
#cg-2 {
  padding-left: 44px;
} /* left-aligned: offset right start */
.cap-emph .w:first-child {
  font-size: 110%;
} /* oversize first word only */
```

The `#cg-N` selector always works because `make-composition.cjs` writes `<div id="cg-N" ...>` for every group.

### "Caps should accumulate (flex stack) instead of swap"

All three templates default to `position: absolute` on `.cap` inside their plane — caps stack at one spot and only the active one shows (single-caption swap). This is correct for `portrait-header` and `corner-column-crown`, where each caption replaces the last.

`memory-wall` uses **flex column accumulation** — captions pile up like a poem. The template doesn't default to this, so override via custom_css:

```css
.wall-plane {
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: flex-end; /* or flex-start for left-aligned */
  text-align: right;
  gap: 14px;
}
.wall-plane .cap {
  position: static; /* un-do template's absolute */
  top: auto;
  right: auto;
  max-width: 100%;
}
```

With this + staggered `in` / `out` times, cap-0 fades in at t=0.2, cap-1 at t=2.55 (below cap-0 in flex order), cap-2 at t=4.90 (replaces both as they fade out together at t=4.85) — this is how the memory-wall poem pages work.

### "Font size doesn't match the scene"

Template preset sizes are tuned for a specific column width + frame size. Don't fight them — override:

```json
"custom_css": ".cap-intro { font-size: 52px; } .cap-phrase { font-size: 60px; }"
```

Then check [typography-presets.md § Font-size scales with column width](typography-presets.md) for what to aim at given your plane's actual dimensions.

---

## The clone-and-tweak workflow

For a new video that's clearly similar to an existing canonical example:

```bash
# 1. Scaffold the project
hyperframes init <project> --non-interactive --video <video.mp4> --skill=embedded-captions

# 2. Matte + transcribe
node scripts/matte.cjs <project>
node scripts/transcribe.cjs <project>

# 3. Copy the canonical HTML instead of writing plan.json
cp references/example-renders/memory-wall.html <project>/index.html

# 4. Replace GROUPS array with the new transcript's grouping (hand-edit index.html)

# 5. Render directly (skip make-composition.cjs since we're not using plan.json)
bash scripts/render-and-composite.sh <project>
```

This skips the preset-based plan.json entirely. Use when:

- Subject framing, shot composition, and backdrop type are similar to the example
- You just need to swap the words and timings
- The bespoke typography from the example is what you want

**Don't clone when**:

- Subject position differs significantly (e.g. centered vs off-center)
- Scene luminance / blend-mode needs are different
- You want to experiment with new typography

In those cases, start with plan.json + custom_css and iterate.

---

## Rendering history

`render-and-composite.sh` now snapshots `index.html` + `plan.json` into `<project>/history/` with a timestamp before every render. If the user says "the previous one was better", diff against the latest snapshot:

```bash
ls <project>/history/
diff <project>/history/index-20260422-203947.html <project>/index.html
```

This lets you recover a design you iterated away from, without re-reading the agent transcript.


<!-- ===== FILE: hyperframes/embedded-captions/references/caption-grouping.md ===== -->

# Caption Grouping

How to turn the Whisper word-level transcript into the `groups[]` array of plan.json.

## Goal

**Each group is one visual phrase**: enters, reveals word-by-word, exits. Rule of thumb: 1 group ≈ 1 comma-to-comma clause or 1 breath of speech.

## Input

`transcript.json` from `transcribe.cjs`:

```json
{
  "words": [
    { "text": "Some", "start": 0.24, "end": 0.44, "type": "word" },
    { "text": " ", "start": 0.44, "end": 0.48, "type": "spacing" },
    { "text": "memories", "start": 0.48, "end": 0.82, "type": "word" }
  ]
}
```

Drop `type: "spacing"` entries; you only need words.

## Break boundaries

Cut a new group at ANY of:

1. **Pause ≥ 500ms** (gap between word.end[i] and word.start[i+1]) — speaker took a breath.
2. **Sentence terminator** — word ends with `.`, `?`, `!`, or an em-dash-like pause.
3. **Strong comma** — `,` followed by pause ≥ 250ms.
4. **Discourse reset** — words like "but", "so", "and then", "you know" starting a clause often merit their own or new group.
5. **Group reaches 6 words OR 2.5 seconds** — whichever first. Long groups feel like subtitles, not embedded typography.

Hard constraints:

- Minimum 2 words per group (1-word exceptions: interjections like "Wait." or the crown line).
- Minimum 0.5s on screen. If a group is less, merge into neighbor.
- No overlapping groups — at most one visible at a time.

## Timing the group

For a group with words `w[0]..w[n-1]`:

- `in` = `w[0].start - 0.08` (enter slightly before first word)
- `out` = `min(next_group.in - 0.05, w[n-1].end + 0.6)` (linger ~0.6s after last word, but don't collide with next)

The last group extends to the video end if needed.

## Style & tone (cross-reference)

See `typography-presets.md` for how to pick `style` and `tone` per group. Work left-to-right through the groups and:

1. First group: default `intro` + `soft`.
2. Watch for emphasis signals (ALL CAPS in transcript is rare but possible; more often it's semantic — superlatives, proper nouns).
3. Escalate tone into `present` once the monologue shifts from setup to statement.
4. Reserve `crown` for at most ONE group, typically the final line.

## Editorial surgery is allowed

You do NOT have to caption every word. It's fine to:

- **Drop filler** like extra "you know"s, "um"s, "I mean"s if they bloat the visual pace.
- **Condense** a 6-word run into 4 by cutting function words, as long as the meaning and timing remain truthful.
- **Skip the whole thing** during obvious silence or non-speech (laugh, music interlude).

Editorial rule: you are writing typography to support the speech, not a court transcript. Keep meaning, trim noise.

## Example (champion)

Transcript: "You know, for me I've had this kind of upbringing, had the great foundation and, you know, I've achieved incredible things. I was dreaming of becoming number one in the world and becoming a Wimbledon champion"

Groups after editorial pass:

```json
[
  {
    "id": "cg-0",
    "style": "intro",
    "tone": "soft",
    "words": ["You", "know", "for", "me"],
    "in": 0.1,
    "out": 1.45
  },
  {
    "id": "cg-1",
    "style": "phrase",
    "tone": "soft",
    "words": ["I've", "had", "this", "kind", "of", "upbringing"],
    "in": 1.4,
    "out": 3.35
  },
  {
    "id": "cg-2",
    "style": "phrase",
    "tone": "soft",
    "words": ["the", "great", "foundation"],
    "in": 3.5,
    "out": 5.35
  },
  {
    "id": "cg-3",
    "style": "emph",
    "tone": "present",
    "words": ["I've", "achieved", "incredible", "things"],
    "in": 6.05,
    "out": 8.3
  },
  {
    "id": "cg-4",
    "style": "dream",
    "tone": "present",
    "words": ["dreaming", "of", "becoming", "number", "one"],
    "in": 8.5,
    "out": 10.4
  }
]
```

Plus the crown:

```json
{ "id": "cg-crown", "style": "crown", "words": ["Wimbledon", "Champion"], "in": 10.8, "out": 12.08 }
```

Notice "had" was dropped from cg-2 ("had the great foundation" → "the great foundation"), "I was" was dropped from cg-4, and "a" was dropped from crown — all for visual cadence.

## word.start/end inside groups

Pass through the original timestamps from the transcript. Don't retime individual words — only the group `in`/`out`. The word-level karaoke reveal inside each group uses the original w.start.


<!-- ===== FILE: hyperframes/embedded-captions/references/composition-craft.md ===== -->

# Composition craft — EMBED track only

This is the deep "how to lay a caption INTO the scene" manual — it governs the **embed**
track only (captions composited behind the subject). The default **rail** track (standard
lower-third subtitle, where most text lives) has its own, much simpler spec → [rail.md](rail.md).
Read this before authoring any **promoted** phrase, in either authoring mode (template
Cinematic `plan.json` or Standard `index.html`).

Topics: phrase grouping, planes & clean-zone anchoring, zone coherence, climax pop,
readability, edge breathing, the occlusion 3-step judgement, accumulation, and persistence.

> **Two-track model (GUIDE.md § Caption model).** Render states are `drop` / `rail` / `embed`.
> The `bg / fg / hybrid` axis used throughout the text below is **superseded**: read **"bg" as
> embed** (behind subject / in-scene), **"fg" as rail or promote-out** (in front), and "hybrid"
> as simply rail + embed coexisting. Everything here applies to the **embed** track — don't
> apply this craft to the rail.

(Granular sub-topics also have their own files — see GUIDE.md § Shared knowledge.)

---

### Caption layer: BG vs FG (aesthetic axis)

Separately from template choice, decide whether captions are **embedded** (behind subject, matte occludes — default "embed" cinematic feel) or **announced** (in front of subject, no occlusion — poster / lower-third feel):

- **bg** — classic embed. Captions sit behind the matte, subject's body partially occludes letters. **Default for any cap that fits the frame.** Partial occlusion is the cinematic feature — small narrator caps with face nibbling 20-30% of letters reads as embedded texture; climax words with face crossing 30-40% reads as Vogue masthead. The eating is what sells the embed. Don't shrink to avoid it.
- **fg** — captions float on top, subject can't occlude. **Fallback for when bg cannot work.** Two scenarios:
  - **Climax fg**: the climax word is so big at impactful size that subject + frame width together leave no place for bg to render at all (subject fills frame AND climax phrase is long; bg would be eaten past readability into broken).
  - **All-fg fallback**: rare, only when the entire scene has no usable bg zone for any caption.
- **hybrid** (per-group `layer:` field) — when one cap (usually the climax) hits the "no place to fit bg" wall but the others (smaller body caps) still work fine in bg. **Body bg + climax fg** is the canonical hybrid pattern.

**Rule of thumb:**

- Small narrator/emphasis captions: bg almost always. Subject eating a few letter-edges = embed feature.
- Climax: try bg first, sized to maximally cross subject. If that size won't fit frame width, AND no clean zone elsewhere, use fg.
- Don't invert the hybrid: body fg + climax bg is the WRONG direction (sacrifices the easy bg embed wins on body, while the climax that needed protection from over-occlusion gets sent into the fire).

**Hybrid worked example — Startup_Host (subject fills frame).**

Subject fills the frame top-to-bottom (head_top y=126 / 10% from top). For body captions there's no large clean zone, but small italic narrator caps in upper corners get eaten ~25% by subject — that's the embed showcase. For the climax "SUCCESSFUL STARTUP" at maximally cinematic size, bg would be eaten 40-50%+ → past cinematic into broken. Climax goes fg.

```json
{
  "caption_layer": "bg",
  "groups": [
    {
      "id": "cg-0",
      "plane": "body",
      "layer": "bg",
      "css": "font-size: calc(0.055 * var(--h)); font-style: italic; ..."
    }, // narrator bg — face eats edges, embed texture
    {
      "id": "cg-1",
      "plane": "body",
      "layer": "bg",
      "css": "font-size: calc(0.085 * var(--h)); font-weight: 800; text-transform: uppercase; ..."
    }, // emphasis bg — Vogue masthead
    {
      "id": "cg-5",
      "plane": "crown",
      "layer": "fg",
      "css": "font-size: calc(0.09 * var(--h)); font-weight: 900; text-transform: uppercase; ..."
    }
    // ↑ climax fg: subject too dense for bg to land readably; fg fallback. Sized to fit frame width fully (single line).
  ]
}
```

Result: body bg captures embed cinematic across the subject (eaten edges = texture not bug), climax fg sits on top fully visible because there was nowhere else for it to go. make-composition.cjs emits both `index.html` (bg groups) and `index_fg.html` (fg groups); render-and-composite.sh runs two parallel Chromium passes and ffmpeg screen-blends fg over bg+matte.

Set via `caption_layer: "bg" | "fg"` plan-level (default for groups without explicit `layer:`), and `layer: "bg" | "fg"` per-group to override for hybrid.

**Decision rule — bg is default, fg is fallback, hybrid is for mixed semantic content.**

For BODY captions (narrator + emphasis):

1. **Find the actual clean zone.** Sample frames at 20/50/80% and mentally trace where the subject is (head, shoulders, gesturing hands). The clean zone is what's left. Top band above the head, bottom band below the shoulders, or off-center side column.
2. **Anchor the plane in that zone.** Body caps fit comfortably with NO subject overlap → `layer: "bg"`.
3. **If body cap stack inherently overlaps subject heavily (>40% per check-occlusion peak)** even at smallest reasonable fonts → body `layer: "fg"`. Subject fills frame too much for embed.

For CLIMAX caption (the payoff):

1. **Default: `layer: "bg"`, sized to maximally cross subject for embed effect.** The face/body eating part of the climax word IS the visual win. Don't shrink to avoid occlusion. Use the largest size that fits frame WIDTH (sub-pixel readable letters fully on-screen) — vertical position should land it across the subject's hair / forehead / face.
2. **`layer: "fg"` for climax** ONLY when frame width physically can't hold a font big enough to feel climactic AND there's no compositional way to break the word across multiple lines that bg embed could carry.
3. **Hybrid (body bg + climax fg)** is the canonical pattern for subject-fills-frame scenes. Body small caps stay bg — subject eats letter edges = embed texture (cinematic, not a bug). Climax goes fg ONLY because at impactful size + subject filling frame there's no place where bg climax could land readably (would be 50%+ eaten = past cinematic into broken). The opposite direction (body fg + climax bg) sacrifices the easy bg embed wins on small caps and forces the climax into a slot it can't survive — never do that.

**Editorial split — the spatial form of body bg + climax fg.** When the hybrid above is laid out with **bg in the upper half and fg in the lower-third**, you get a magazine-cover composition for free — no separate template needed. The rule:

- **Body caps (BG)** — placed in the upper half (top: 6-30%), at the head/hair zone. They get partially occluded by hair/forehead = vogue-masthead embed texture.
- **Climax cap (FG)** — placed in lower-third (top: 70-85%), in front of subject's chest/below. It's fully clear, fully readable, dominates the bottom band.

The viewer's eye reads top-to-bottom: first the partially-veiled body line ("decorative, atmospheric"), then the clean climax statement ("the point"). Same Z-axis layering as Vogue / Apple Keynote (decorative top behind subject + clear bottom in front), but driven by cinematic-cream's existing per-cap `layer:` field — no new template, no separate masthead track.

Two timing modes inside this layout:

- **Sequential cross-fade (default)** — body fades out as climax fades in over 0.3-0.5s. The brief overlap window IS the editorial dual-layer moment. Standard cinematic-cream behavior.
- **Sustained overlap** — extend body's `out` to coincide with or extend past climax's `in` so both are visible together for 1-2s. Use sparingly: works when body line is short (≤3 words) and acts as a "kicker" above the climax. Long body phrases sustained alongside a fg climax = visual noise.

**The plane-conflict rule for sustained overlap (debugged in Startup_Host).** If you extend a body bg cap's `out` into a window that contains another cap with `layer: "fg"` IN THE SAME PLANE, the two will visually overlap in the final composite — bg pass renders the extended bg cap, fg pass renders the fg cap, both at identical plane position, screen-blended on top of each other. Result: muddy double-text at the same spot.

Before extending any body bg's `out`:

1. Check what other caps occupy the body plane during the extended window
2. If ANY of them is `layer: "fg"`, the extension causes plane overlap → don't do it
3. Workaround: either (a) skip sustained overlap and use sequential cross-fade only, or (b) author the body kicker on a DIFFERENT plane / absolute position so the two don't share a plane

Concrete example: Startup_Host has cg-3 "diving deep" (body bg, plane=body, 3.1–4.15s) and cg-4 "into what it really takes to build a" (body fg fallback, plane=body, 4.15–6.42s). Both occupy `plane=body`. Extending cg-3 to overlap with the climax cg-5 (6.42–8.06s) ALSO drags cg-3 across cg-4's window where cg-3 (bg) and cg-4 (fg) collide on the body plane. Sequential editorial-split (climax in lower-third, body bg already faded out) was the only safe option for this case. AI_Insights had no fg in body plane between kicker and climax, so sustained overlap worked there.

When NOT to use editorial split:

- Body and climax are both information-carrying full sentences → forces viewer to read both at once, fails. Editorial split needs the body line to be _atmospheric / setup_ (italic mood), climax to be _the payoff_ (bold uppercase).
- Subject takes the full vertical column (no top clean zone, no bottom clean zone) → there's no upper or lower band to anchor either layer. Fall back to all-fg with crown.
- Climax is a long phrase that wraps to 3+ lines in lower-third → eats too much vertical real estate, leaves no room for the body bg above. Either shrink climax or split into more groups.

This pattern was historically what we called "hybrid" but the spatial framing — upper bg behind / lower fg in front — is what makes it read as editorial design rather than just two unrelated caption tracks. Keep this in mind when authoring per-cap `layer:` for hybrid scenes.

Common mistakes (debugged in real cases):

- Defaulting to "right column" because memory-wall did it → narrow 400px column forces long phrases to wrap 4-5 lines, pushing the stack DOWN into the subject's body. Fix: use top-band full-width instead, wider wrap fits fewer lines.
- **Flipping climax to fg because "viewer needs to read it" → kills cinematic embed.** Climax is supposed to feel half-eaten by subject; that's the magazine masthead energy. Don't fix what isn't broken.
- All-fg whole plan when subject fills frame → safe but sterile. Hybrid (body bg + climax fg) is almost always better — small body caps eaten = embed texture, climax fully visible since it had no readable bg slot.
- Sizing caps before choosing the plane → typography is a function of plane geometry, not the other way round.
- **Putting LONG multi-line phrases on bg in subject-fills-frame scenes.** "Subject eats letter edges = embed texture" only holds for short caps (1-3 words / 1 line). A 6-8 word italic phrase wraps 3-4 lines, and when subject's head is high in frame, **whole lines** of the phrase land deep in the body/face zone — entire words obliterated, not edge-textured. That's not embed, it's broken. **For long body phrases on subject-dense scenes: switch THAT specific cap to `layer: "fg"` even if other body caps stay bg.** Hybrid lets you mix per-cap. Sample the matte at the cap's time window: if head_top y is climbing and the cap's stack height extends into y > head_top, that cap needs fg.
- **Subject doesn't move uniformly across the clip — sample matte per BLOCK time window, not just once per case.** Startup_Host's head_top swings y=224→96 across 8 seconds (128px / 10% of frame). A block plan that worked at t=2 (head low, plenty of space) breaks at t=5 (head high, no space left). Per-block matte sampling > one-shot per case.

### Step 0 for ANY plan — transcript role annotation (mandatory)

Before writing a single caption group, do a **pre-plan agentic pass** over the transcript. Read every word and grade it. This is judgment, not a lookup — context decides (e.g. "like" is content in "like this", filler in "like, um, yeah"). No hardcoded word lists; agent decides per token.

**The grade is the SELECTION INPUT — it picks the render state** (`drop` / `rail` / `embed`); it is not itself a typography class (see GUIDE.md § Caption model):

| Grade        | What it is                                                                                                                                               | → render state                                                                                    |
| ------------ | -------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------- |
| **drop**     | Interjections/hesitation (um, uh, er, ah), self-corrections ("I think— I mean actually…" keep only final), pure stutters ("the the the") collapse to one | **drop** (not shown)                                                                              |
| **normal**   | Ordinary spoken content — connective glue + the content words that carry the idea                                                                        | **rail** (dense conversational glue may be trimmed for readability; content/structure words stay) |
| **emphasis** | The 1–2 punch words in a phrase                                                                                                                          | **rail** + `emphasis` highlight (inline — stays on the rail)                                      |
| **peak**     | The payoff of a beat/section — the line you'd say out loud paraphrasing it                                                                               | **promote to embed** (apply the craft below); the single biggest of the whole piece = `apex`      |

A **peak** is per-beat, **not** per-clip: a short clip usually has one (its climax); a long/multi-section explainer has ~one per section. **Embed is scarce + spaced** — ≤1 per sentence/beat, never two adjacent or co-visible, ≥ a beat apart, at most one `apex`. (The old "1 climax / 2–4 emphasis / 4–10 body / 6–12 narrator / 2–8 drop per 10–20s clip" was calibrated for short single-beat clips; it generalises to "one peak per beat, spaced — everything else rides the rail.")

**This step replaces any filler-word list.** If you find yourself reaching for a regex, you're doing it wrong — go back and judge per-token.

Then build the plan from the annotated words:

- drops → do not appear in any word entry
- narrator → either fold into adjacent body groups OR become tiny italic subordinate groups if rhythm demands
- body/emphasis/climax → shape the group structure, with typography matching role

### The compositional unit is a PHRASE, not a chunk (read this twice)

A **caption group** is a semantic phrase — typically 2–8 words bound by intonation and meaning. It is NOT a mechanical "2–4 word chunk". A group has ONE typography (one font-size, one weight, one case, one position) matching its role; the "every-word" feel comes from **per-word GSAP stagger INSIDE the group**, not from splitting the phrase into many tiny groups.

Canonical reference — memory-wall, 12 spoken words, **4 groups**:

- cg-0 `"Some memories feel soft"` (4 words, italic 600, right-top)
- cg-1 `"like old film"` (3 words, italic 500, right-mid, smaller)
- cg-2 `"but suddenly"` (2 words, upright 700 pivot, right-center)
- cg-3 `"EVERYTHING IS SHARP AGAIN"` (4 words, uppercase 900 climax, spanning width)

Every word is shown. Groups **cascade and accumulate** — cg-0 stays on screen while cg-1 enters below; by the climax, all 4 are visible simultaneously as a poem. Per-word stagger (~80ms) animates each word into its group in sequence.

If you find yourself producing 15+ groups for a 10s clip, stop — you're treating verbatim as mechanical chunking. Go back, re-read the transcript, identify 4–7 phrases, and make them groups.

**Don't split idioms, collocations, or bound phrases across groups.** "Not even kidding", "at the end of the day", "as a matter of fact", "whole lot of", "more or less", "a little bit", "kind of", "sort of", proper nouns ("Blackmagic Pocket 4K"), brand phrases, and other fixed expressions are semantic units. The climax of "I'm not even kidding" is the whole idiom, not just "KIDDING". The climax of the memory-wall canonical is "EVERYTHING IS SHARP AGAIN" as one group, not just "AGAIN". Splitting these across group boundaries breaks meaning AND typography (you can't render "not even kidding" with "not even" italic-small and "kidding" uppercase-huge — it reads as two different statements).

### Captions are always verbatim

Every word the speaker says gets captioned. The skill no longer ships a "highlight" mode — curated/edited transcripts produced fewer beats but lost the rhythm of the spoken sentence and ended up feeling like generic subtitle tracks. Verbatim with strong typographic hierarchy (small italic narrator → emphasis upright → climax massive uppercase) gives the cinematic feel without dropping content.

The only words you remove from the transcript:

1. **Pure phonetic interjections** (um, uh, er, ah, hmm) — not words, not captioned.
2. **Exact immediate stutters** ("the the the" → keep one; "is is is is" → keep one, aligned with the phrase that follows). The viewer should see one "the", not three.
3. **Self-correction backtracks** ("I think— I mean actually…" → keep only "I mean actually").

**All content words AND structure words stay** (articles, conjunctions, prepositions, auxiliaries, pronouns). Dropping a structure word like "in some" or "and I've" or "out of it" is a bug, not a stylistic choice.

### Planes — shared parent containers for spatial coherence (RECOMMENDED)

The memory-wall and champion canonicals don't set `top:` on each caption. They have a **parent container** (`wall-plane` / `left-plane` / `crown-plane`) that owns the spatial anchor, and caps are children that stack automatically (flex column with gap) or replace (absolute at same anchor).

Your plan.json can opt into this by declaring `planes` and assigning each group to one:

```json
{
  "planes": {
    "body": {
      "css": "top: 4%; right: 4%; width: 720px; display: flex; flex-direction: column; align-items: flex-end; gap: 14px;"
    },
    "crown": {
      "css": "top: 32%; left: 0; right: 0; text-align: center;"
    }
  },
  "groups": [
    { "id": "cg-0", "plane": "body",  "css": "font-size: calc(0.08*var(--h)); font-weight: 600; font-style: italic;", ... },
    { "id": "cg-1", "plane": "body",  "css": "font-size: calc(0.10*var(--h)); font-weight: 800;", ... },
    { "id": "cg-2", "plane": "crown", "css": "font-size: calc(0.20*var(--h)); font-weight: 900; text-transform: uppercase;", ... }
  ]
}
```

The plane CSS owns positioning (top/left/right + display:flex/grid/block). Per-group CSS owns **typography only** (font-size, weight, style, case, letter-spacing, line-height). **No top/left/right/position on a group when it's inside a plane** — the parent decides.

**Typography is agent-authored per group, NOT looked up from a preset.** The `cinematic-cream` template locks only the DNA (Inter family, motion curves, `mix-blend-mode`, `cap_color` palette, text-shadow/filter derived from luminance). Everything else — `font-size`, `font-weight`, `font-style` (italic vs upright), `text-transform` (uppercase vs mixed), `letter-spacing`, `line-height` — is written by the agent, per group, in `plan.json`'s `css` field. No "cap-1 must be italic 600, cap-2 must be uppercase 900" rule. Read the scene + transcript, pick typography that matches the semantic role (narrator/body/emphasis/climax) and the visual weight the frame can carry. See [references/typographic-moves.md](typographic-moves.md) for _recommended_ combinations — treat as palette, not schema.

When to use planes:

- **Multi-phrase sentence in one home zone** — use a flex column plane. All body caps inside accumulate/stack automatically, no collision math. This is the memory-wall pattern.
- **Body zone + climax zone** — two planes: body (flex stack) + crown (center). Body caps live in body-plane; climax pops in crown-plane. Cross-plane transition = earned break.
- **Any clip with ≥3 body phrases** — single-plane flex stacking beats hand-placing each group's top% every time.

### Picking the plane anchor — find the ACTUAL clean zone in THIS scene

**Do not default to "right column" because memory-wall did.** Memory-wall worked because its subject sat left-center with a clean wall on the right. Different scenes have different clean zones:

- **Subject centered (most selfies, vlogs)** → top band above the head is usually cleanest (clear sky / ceiling / wall). Right or left columns get eaten by shoulders or hands.
- **Subject left (interview with right-column backdrop)** → right column cascade (memory-wall classic).
- **Subject right (reverse interview)** → left column cascade.
- **Two-shot or busy background** → may need to use a corner, or sit the caption on the ONE surface that's consistently clean (a solid jacket, a whiteboard, a ceiling).

Before writing plane CSS, look at a frame sample. Mentally trace the subject's bounding box and hand-gesture reach. The plane anchors into whatever's LEFT — negative space where the cascade won't be eaten by body or busy backdrop.

Small-size italic narrator text is especially vulnerable — it disappears into mottled backgrounds or body occlusion. Keep smallest caps in the cleanest part of the zone, not at the edges where subject extends.

When NOT to use planes (the remaining free-mode use cases):

- **1–2 isolated groups** with deliberately different positions — free mode is simpler.
- **Specific clip-spanning motion** where a group needs to drift/move independently.

Free mode (no `planes` declared) is still supported — each group's CSS owns its own top/left/right. Use when you genuinely need bespoke per-group placement.

Wrong: "primary slot for 9:16 is top:12%". That's a lookup; it produces generic output.
Right: look at THIS scene, find where captions will read cleanly, respect the speaker's framing, and pick a composition pattern that serves the content's narrative arc.

Example patterns an agent can pick (not exhaustive, not ranked):

- **Right cascade accumulating** (memory-wall): all groups right-aligned, stepping down in top%, they stay — final frame shows a poem. Works when subject is centered-left and there's clean right-column space.
- **Center stack climax** (Sunset): italic openers at top, upright pivot mid, uppercase climax takes the full top as the final beat, earlier groups fade out before climax. Works when subject is centered and scene has clean sky + clean below-shoulders.
- **Left-right split** (memory-wall variant): narrator voice on one side italic, statement voice on the other side upright, climax takes center. Works when subject has off-center clean zones.
- **Single-line subtitle rail**: legit choice when scene is dense and no clean zones exist (busy background, subject fills frame). This is the "accessibility" fallback, not the default.

Whichever pattern is picked, the agent's job is to **justify the choice**: "Subject is on the left, clean gradient sky on the right — I'll cascade right-aligned so captions have clean backdrop throughout." Write that reasoning as a `_notes` field in plan.json so the intent is inspectable.

Anti-patterns to NEVER ship:

- Alternating top↔bottom per chunk — reads as chaos (one sentence's words appearing in different vertical zones).
- Locking every group to the same `top` value — reads as subtitle track, kills cinematic feel.
- Placing body/narrator groups directly over the face when clean space exists — the Vogue-embed effect is for the CLIMAX word only, not default behavior.
- **Dropping transcript words to fit caps in fewer blocks.** NEVER. Verbatim is verbatim. If 4 caps don't fit in 1 block, split into 2 sub-blocks of 2 caps each — keep all words. The only legitimate drops are GUIDE.md's filler list (um/uh/exact-stutters/self-corrections), not "we ran out of room."
- **Mechanically aligning all caps in a plane to share `out` time.** This makes everyone stay on screen longer, _increasing_ density. Wrong fix for the no-jump problem. Correct fix: split natural-handoff caps into separate blocks where each block's caps share `out` (same exit moment, no jump), and `next_block.in ≥ prev_block.out` (clean handoff between blocks, no overlap).

**Block boundary three laws** (must hold for every plane in every plan):

1. Within a block, all caps share `out` — they fade together, no per-cap exit jitter.
2. Between adjacent blocks in the same plane, `next_block.in == prev_block.out` (or `next.in > prev.out` with a small gap). Caps from prev_block must FULLY exit before next_block's caps mount; otherwise the prev cap's exit at its `out` time triggers a flex reflow that yanks next_block's already-mounted caps upward = jump.
3. `prev_block.out ≤ next_block.first_word.start` so next_block's first word still animates from its real spoken time (the in-time only constrains when the container mounts; word animations fire at their per-word `start`).

A common mistake: setting `next_block.in` slightly EARLIER than `prev_block.out` to give the new block a head-start fade-in, while prev_block still has a different (later) `out`. The 50-300ms overlap looks invisible in the plan but produces a visible jump on screen because two caps with different `out` coexist in the same flex stack.

- **Vertical gap between body bottom and crown top.** Looks disconnected ("The pace is" at top:3% with "UNPRECEDENTED" at top:20% creates 144px void). Bond the setup phrase + climax word in the SAME crown plane via flex-stack — the Street_Talk "and being / CONSISTENT" pattern.

### Zone coherence — one sentence, one home zone

**Never switch spatial zones mid-sentence.** A full semantic unit (sentence or clause) should live in ONE home zone (e.g. right column, or top band). The viewer's eye follows the phrase group. Ping-ponging between top/bottom/left/right for consecutive phrases of the SAME sentence reads as chaos — the reader has to re-find the caption every beat.

Zone changes are earned at:

- **Sentence boundaries** (period, long pause, topic shift) — allowed to move to a new home zone, often paired with a tonal shift (italic body → uppercase emphasis)
- **The single climax** — the one break from the home zone, always allowed, often takes center-full-width

Heuristic: if you find cg-N and cg-N+1 are in different zones (top vs bottom, left vs right) AND they're parts of the same sentence (no period/long pause between them), you've violated zone coherence. Fix by picking one home zone for the whole sentence.

### The climax has to POP — not just "be a bit bigger"

A climax caption that's the same size as body emphasis is a failed climax. The viewer's eye needs a clear visual break: THIS is the payoff.

**Size the embedded climax to the FRAME, not to the rail (two-track rule).** The climax is a hero — its size is anchored to frame height: **`font-size: calc(0.16–0.22 * var(--h))`** (default ~0.18–0.20h; go bigger for more impact — it should dominate the frame, only width/readability caps it). It is **NOT** a multiple of the rail: the rail is a small standard subtitle (~0.045h), so "≥1.8× the rail" would yield a tiny, weak climax. Express rail, embed-body and embed-climax all as `var(--h)` fractions so they scale across resolutions — **never hardcode px**. The ratios below are a **floor / hierarchy check** (the climax must clear body-emphasis by ≥1.8× and the smallest tier by ≥2.5×), not the climax's sizing basis. Width is the real ceiling: shrink only if the word can't fit the frame at a legible size (see "Readability is a hard constraint").

Contrast floor — the climax must at least clear these:

| Ratio                      | Feels like                                                                                  |
| -------------------------- | ------------------------------------------------------------------------------------------- |
| **1.0-1.3× body emphasis** | Flat — the climax is just another beat. Fix it.                                             |
| **1.5-1.8× body emphasis** | Noticeable but not explosive. OK for subtle payoffs, weak for punchlines.                   |
| **≥1.8× body emphasis**    | Pops. Viewer's eye snaps to it. Target for "punchline" / "reveal" / "reaction" climaxes.    |
| **≥2.5× body italic**      | Compare against the SMALLEST body tier too — the multi-tier jump is what creates hierarchy. |

A quick audit script — before shipping, dump every plan's max-body vs max-crown font-size ratio, and flag anything <1.8×:

```js
const bodyMax = Math.max(...plan.groups.filter((g) => g.plane === "body").map(fsize));
const crownMax = Math.max(...plan.groups.filter((g) => g.plane === "crown").map(fsize));
const ratio = crownMax / bodyMax; // aim for ≥1.8
```

**Split pattern — when one word alone should carry the climax.** If the climax phrase is 2+ words ("and being consistent", "not even kidding") and one of them is the actual payoff, split into setup + payoff BUT keep them spatially bonded:

- Setup words → small italic narrator (soft, trailing off) on line 1
- Payoff word → massive uppercase on line 2, same plane, flex-stacked directly below
- **Both groups live in the SAME (crown) plane**, flex-column, gap 4-8px. Not two different planes — otherwise "and being" sits in the top band and "CONSISTENT" sits mid-frame and they read as two unrelated captions.

Crown plane CSS for split climax:

```
"crown": "top: 26%; left: 0; right: 0; display: flex; flex-direction: column; align-items: center; text-align: center; gap: 6px;"
```

Street_Talk canonical example: original was `"AND BEING CONSISTENT"` all in crown at 0.085h (same as body emphasis, ratio 1.0×). Rewrite: crown plane becomes a flex-column; `"and being"` → 0.055h italic at top of column (line 1); `"CONSISTENT"` → 0.11h 900 uppercase stacked below (line 2). The payoff POPs because of size contrast within a bonded 2-line composition, AND it crosses the subject's head since the crown column is anchored at ~26-30% top.

Timing: both groups share `out` (at clip end or block boundary) so neither fades alone — they hold together as one composition. Setup enters first (soft fade-in), payoff enters later when the word is spoken (snappier present scale-in).

**Readability is a hard constraint — bleed can't eat the word.** Your first move when a climax word overflows is NOT "accept the bleed, it's cinematic" — it's "shrink to the largest size that fits." Compute the max font size that fits the frame:

```
max_font_px = frame_width / (chars × char_ratio × letter_spacing_mult)
```

For "CONSISTENT" (10 chars), uppercase 900 (char_ratio 0.62), letter-spacing -0.05em (mult 0.95), 720px frame: `max = 720/(10*0.62*0.95) = 122px ≈ 0.095h`. Use 0.09h for a small safety buffer. The word fully occupies the frame edge-to-edge — that's already maximum visual impact without losing any letter.

Cinematic bleed is only OK when **a few pixels of 1-2 outer letters** get mild cropping from scale-in animation or sub-pixel rounding — that reads as "bigger than frame." Any bleed that forces the reader to mentally complete missing letters (>15-20px per side on a 10-char word) is a BUG, not style. "ONSISTE" with 80px each side clipped is NOT a valid climax — it's broken.

Hard rules:

- **Readable first.** Every letter should be fully on-screen, with at most a few-px crop on the first/last letter.
- **If max legible size doesn't meet ratio target**, raise impact via _other_ signals (weight 900, all-caps, bg head-cross, multi-line composition with setup word above), not via illegible bleed.
- **Never bleed body/narrator captions.** Only the crown/climax is allowed any edge crop at all.
- `OCCLUSION_SKIP=1` is an escape hatch for iterating; the shipped plan should pass `check-occlusion-v2.py --strict` (pixel-perfect via headless Chromium DOM).

### Edge breathing + climax-crosses-head (bg showcase)

Two placement tweaks that separate "looks like a caption sitting in the scene" from "looks like a pasted subtitle":

- **Non-climax caps need edge breathing room.** Body-plane groups should NOT hug `left: 0; right: 0` flush to the frame. Add `left: 3-6%; right: 3-6%` (or `right: 30-40px` for pixel-anchored planes). The breathing sells the compositional choice — flush edges read as "default subtitle track", indented edges read as "considered composition". Top edge the same: `top: 2-6%` not `top: 0`.

- **The climax SHOULD cross part of the subject's head — deliberately.** This is what makes bg-layer captions feel cinematic instead of just "text floating above the speaker". The effect is strongest when 20-40px of the word's last line dips behind the hair or forehead — viewer reads the word clearly AND sees it being occluded at the edge. Not "covered by the face" (unreadable), just "grazed by the hair" (legible + cinematic).

  How to place the crown with intent:
  1. Sample the matte PNG at climax time: `f_{frame_idx:04d}.png` where `frame_idx = round(climax_time * fps)`.
  2. Scan rows from top until `alpha > 128` — that y is the subject's topmost pixel (usually hair).
  3. Position crown so the _bottom of the last line_ lands 30-80px below that y. For a 2-line crown at 0.085h on 1290h frame, line heights ~104px each; total height ~200px. If subject top is at y=445, set `crown.top` such that `top + height = 445 + 50 ≈ 495` → `top = 295px ≈ 23%`.
  4. Verify with checker — the HERO/crown peak occlusion target is ~30–55% (the embed effect; the head crossing the middle). Below ~15% it reads as a floating label (the hero-weak advisory fires); above ~65% the word is eaten (the gate FAILs). Small narrator caps: ~20–30% texture.

  Practical rule of thumb: **crown peak occlusion 3-10%** is the sweet spot. The checker's number tells you directly — not a subjective "it looks good" judgment.

  **Crown defaults are scene-specific, not template-wide.** Don't set `crown.top: 6%` because "that's what the previous case used." If the subject's head_top is at y=380 (29% of frame) and your crown is at top:6% with 100px height, the crown bottom lands at y=200 — 180px ABOVE the head, completely floating in sky, zero embed effect. Always sample the matte once per case and compute `crown.top` from `head_top - crown_height + (30 to 80)` so the crown's bottom edge dips into hair. This was a real bug across 6 cases until enforced.

  FG-layer crowns skip this entirely (they render on top, no occlusion to showcase) — FG is announcement, not embed.

### Pre-render occlusion + frame-overflow gate

**`check-occlusion.cjs` (canonical, pixel-perfect)** is the only occlusion checker in `scripts/`. It auto-runs `measure-layout.cjs` (headless Chromium via Puppeteer) which loads the compiled `index.html`, seeks the GSAP timeline to 4 sample times per group (15/40/65/90% through window), and queries `getBoundingClientRect()` on every `.cap` and child `.w` span. Output is `_layout.json` with the actual rendered pixel coordinates of every word at every sample. Then it computes per-word, per-cap occlusion against the real subject-matte alpha (read via `sharp`):

- **Per-word peak occlusion** — the load-bearing metric: a 5-word phrase where 3 words are fully eaten averages the same as 8 words half-eaten, but only one of those is shippable, so per-WORD peak is what gates. Per-word peak ≥65% = `obliterated`, ≥35% = `warn`. A `WARN` band hit on a single climax word is OK (cinematic edge crop); two adjacent words obliterated is not.
- **Per-cap aggregate** — avg + peak occlusion across all samples. Cap fails at peak ≥50%.
- **fg-layer caps are auto-skipped** (they render above the matte; no occlusion possible).

**Why measure the real DOM, not estimate a bbox.** An earlier heuristic estimated each word's box from `char_ratio × font × text_length` and was wrong in both directions. Startup_Host case: it reported `cg-1 "podcast." OK at 9%/12%` because it guessed y=134 (above the subject's head), but the rendered DOM was at y=209 (mid-head) → actually `FAIL 54%/60%`. Same case, it reported `cg-3 "diving deep" FAIL at 76%/77%` while the real measurement was `WARN 36%/40%` (the box is wider than the head — most pixels clear, only descenders dip into the silhouette). Estimation is retired; `check-occlusion.cjs` measures the rendered pixels.

**Frame-edge overflow** — the checker also flags when a measured word bbox extends past the canvas (text the ffmpeg crop would clip), reported as `cg-N  [overflow] "word" off-frame: left Xpx, right Ypx (@Ts)`. Because cropped body text is always wrong, a clear glyph clip (>8px past an edge) **fails `--strict`**; a sub-glyph graze (≤8px — the first/last-letter crop the climax is allowed) is a non-blocking `[overflow-warn]`.

**The checker reports facts, the agent applies judgment.** A FAIL is NOT an automatic "must re-layout" signal — it's evidence to interpret. Two competing goals coexist:

1. **Readability** — every sentence must remain comprehensible to the viewer
2. **Cinematic embed** — partial occlusion is the desired vogue-masthead effect; zero occlusion looks like a pasted subtitle

When the checker reports a per-word obliteration (≥65%), apply this **3-step decision rule** before changing anything:

**Step 1 — POS check.** Is the obliterated word a function word (the / a / an / of / in / on / at / to / I / it / is / are / was / be / that / this / which / and / or / but)? Function words are grammatically optional in most contexts — a 100%-eaten "the" or "I" or "of" usually does NOT break the sentence. Content words (nouns, verbs, adjectives, climax words) carry meaning — they MUST stay legible.

**Step 2 — sentence parse without the word.** Mentally delete the obliterated word from the sentence. Does the remainder still convey the meaning?

- "like this are why I travel" minus "I" → "like this are why travel" — first-person obvious from context, **OK**
- "take it all in" minus "all" → "take it in" — complete English idiom on its own, **OK**
- "a whole lot of information" minus "of" → "a whole lot information" — slightly broken but recoverable, **OK**
- "diving deep into startups" minus "deep" → "diving into startups" — works fine, **OK**
- "diving deep into startups" minus "diving" → "deep into startups" — loses the verb, sentence breaks, **NOT OK**

**Step 3 — cinematic check.** A single content word at 30-65% partial occlusion is the _intended_ embed look (vogue-masthead "subject grazes the text"). Don't "fix" it. Only escalate to re-layout when:

- a content word is ≥80% gone (not just partially eaten — almost fully missing)
- two or more adjacent words are ≥50% obliterated (sequential damage compounds; "X X X really takes" with first three eaten is unrecoverable)
- the obliterated word IS the climax / key noun the viewer is supposed to read (e.g. the subject of a sentence, a brand name, a product feature)
- key letters of a climax word are eaten (e.g. "STARTUP" with the S gone reads as "TARTUP" — the partial-letter pattern matters more than the whole-word percentage)

**Real examples from the 13-case batch** — all four caps below got a per-word obliteration FAIL, all four were correctly judged OK by this rule:

| case               | obliterated word @% | sentence                              | rule applied                           |
| ------------------ | ------------------- | ------------------------------------- | -------------------------------------- |
| Sunset_Stroll cg-1 | "I" 100%            | "like this are why I travel"          | function word + parses without it → OK |
| Sunset_Stroll cg-3 | "all" 75%           | "take it all in"                      | "take it in" is a complete idiom → OK  |
| yt_gtds cg-6       | "of" 69%            | "a whole lot of information"          | function word + recoverable → OK       |
| AI_Insights cg-2   | "that" 66%          | "that don't replace human creativity" | relative pronoun, optional → OK        |

**When the rule says re-layout** — what to change:

- per-word obliterated AND content word AND breaks readability → switch THAT specific cap to `layer: "fg"` (per-cap override, not whole-plan), OR shrink/reposition, OR split the cap into a different block where the subject isn't crossing it.
- per-cap fail (peak ≥50%) when the whole stack is in the head zone → lift y or shrink the block.
- frame-edge overflow → shrink font OR tighten `letter-spacing` OR split the phrase. Cropped text is ALWAYS wrong, no aesthetic excuse.

**Override** (for iterating before shipping): `OCCLUSION_SKIP=1 bash render-and-composite.sh <project>` — don't ship past this without applying the 3-step rule and either fixing or consciously accepting each FAIL.

### Accumulation capacity — split into blocks when the plane can't hold more

Each scene's clean zone has a finite capacity for simultaneously-readable caps. **The agent must judge this before writing the plan**, not rely on CSS `bounded height` / `overflow: hidden` — those cause visual bugs (caps overflow off-screen, are clipped, or content is centered outside the plane bounds).

Rule of thumb (capacity = max caps visible SIMULTANEOUSLY in one block):

- **9:16 portrait, narrow right-column plane** (width ~380-420px) → max **2 caps** per block. Long phrases wrap to 2-3 lines; a 3rd cap starts spilling into the subject.
- **16:9 landscape, subject centered** (e.g. selfie vlog) → max **2 caps** per block. Even if the frame is wider, a centered subject leaves narrow columns on both sides and hands reach far.
- **16:9 landscape, subject on one side** (e.g. interview with clean opposite side — the memory-wall canonical scenario) → max **3-4 caps** per block. This is where accumulation shines.
- **Top-band full-width plane** (either orientation) → max 1-2 caps before overflow into face zone.

Capacity is about the specific scene — same orientation can have very different room depending on subject position and background complexity.

When your phrase count exceeds the capacity, split into multiple accumulation blocks at **sentence or clause boundaries**. Example memory-wall canonical on a 12-word clip:

- Block 1 (0–4.85s): `"Some memories feel soft"` + `"like old film"` — 2 caps accumulate, fade together at 4.85s
- Block 2 (4.90–8.04s): `"but suddenly"` + `"EVERYTHING IS SHARP AGAIN"` — 2 caps accumulate on a cleared plane

All caps in one block share the same `out` time (sentence boundary). Next block's `in` > previous block's `out` so the plane clears before the new accumulation starts. This gives each cap ~3-5s of read time, avoids overcrowding, and matches memory-wall's cinematic rhythm.

**Why the shared `out` is load-bearing.** The template's exit path is `tl.set(sel, { opacity: 0, display: "none" }, g.out)` — at `out`, each cap releases its flex space so the NEXT block's caps can take the top slot from the plane's origin (no permanent downward drift). If caps inside the same block had staggered `out` times, the plane would reflow mid-block (cap 1 vanishes, caps 2-3 jump up, cap 4 arrives… visible jitter). With block-synchronized `out`, the reflow happens ONCE at the boundary — invisible to the viewer because the block fades as a unit. **Never stagger `out` times within an accumulation block.** If you need individual fade-outs, you're not accumulating — switch to stagger-fade pattern (one group at a time, no flex plane needed).

**Anti-pattern: bounded `height` + `justify-content: center` on planes.** Do NOT write `height: 70%; justify-content: center` on a flex-column plane hoping to vertically center the caps. When the block's total cap height exceeds the bounded height, flex centering pushes content OUTSIDE the plane bounds on BOTH top and bottom — the topmost cap ends up above the frame (off-screen, unreadable). Instead:

- Let the plane grow with its content — set `top:` (origin anchor) and let caps stack down naturally.
- Use `gap:` between caps; don't try to "center the stack".
- Trust the block-capacity rule above to keep the stack within the clean zone — don't paper over overflow with `overflow: hidden` (it clips the very caps you wanted the viewer to read).

### Accumulation — vertical spacing, not single-line

Accumulation works with multi-line phrases too — memory-wall canonical's groups are multi-word, right-aligned cascade in 16:9 landscape, and several wrap to 2 lines. They don't collide because **each group's `top` is placed below the previous group's bottom extent with a margin**.

Math you must do before shipping accumulate:

For each group, estimate its rendered height:

- `line_count ≈ ceil(chars × font_px × 0.72 / usable_width_px)` (0.72 = Inter 900 uppercase; use 0.60 for italic/regular)
- `group_height_pct ≈ line_count × font_size_pct × line_height × 100`

Then for each pair (cg-N, cg-N+1) you want to coexist:

- `cg-(N+1).top ≥ cg-N.top + cg-N_height_pct + 2%` (margin)

If the math doesn't fit in the available clean zone (top-clear + bottom-clear zones minus face/body bbox), you have two options:

- **Shrink fonts or merge phrases** so they fit.
- **Switch persistence to stagger-fade** (groups don't coexist, no spacing constraint).

9:16 portrait specifically: clean zone is typically top 0–32% + bottom 72–90%, split by the subject. That's ~50% of frame height usable. At 15% per 2-line group + 2% margin, you can fit ~3 accumulating groups in top zone. A 4th must either (a) be smaller to fit, (b) go to the bottom zone (zone change allowed at sentence boundary), or (c) replace an earlier one as climax.

Landscape 16:9 has ~70–80% usable vertical — more room for 4–5 accumulating groups, which is why memory-wall canonical works cleanly there. Don't give up accumulation on portrait; just do the arithmetic first.

### Persistence — how long each group stays (agent decides per case)

The group's `out` time is not a default, not a rule, not a formula. It's an aesthetic choice. The same 5-group plan renders very differently depending on whether groups accumulate, stagger, crossfade, or roll — and each is right for different content.

Patterns to pick from:

| Pattern                                     | What happens                                                                 | Good for                                                                                            | Bad for                                                            |
| ------------------------------------------- | ---------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------ |
| **Accumulate-through-climax** (memory-wall) | All groups stay on screen until climax arrives, then all fade together       | Poetic builds; emotional crescendo; ≤5 groups where each word matters                               | 8+ groups (screen crowds); punchy comedic beats (breaks the laugh) |
| **Stagger-fade** (Sunset-style)             | Each group fades ~0.8–1.5s after its words end; next enters into clean space | Independent punchy beats; clip where each phrase is its own moment                                  | Long poetic builds that want the stanzas to coexist                |
| **Crossfade-handoff**                       | Current group fades during next's entrance (~200ms overlap)                  | Dense verbatim (6+ groups in short clip); conversational flow                                       | Short sparse clips — feels like subtitle track                     |
| **Rolling window**                          | Keep N=2–3 visible; earliest fades when N+1 enters                           | Longer transcripts (15s+) where full accumulation would crowd, but some layering is still cinematic | Clips <8s (rolling isn't perceptible)                              |

Decision axes:

- **Narrative arc** — crescendo/revelation → accumulate; list of independent points → stagger; dense conversation → crossfade
- **Group count** — ≤4: any pattern works. 5–7: prefer stagger or rolling. 8+: crossfade is usually forced.
- **Scene density** — busy background eats stale captions; accumulate only works when backdrop is clean enough that older captions stay legible.
- **Clip length** — ≥12s erodes accumulation (viewer loses connection to earliest caption); prefer stagger or rolling for long clips.

Write the reasoning in `_notes` in plan.json so the decision is inspectable and the agent's intent survives into review. e.g.:

```json
"_notes": "Morning_Jog: 5 groups in 8s. Narrative is crescendo (Okay→honestly→changed my life→KIDDING), and background is clean (trees, sky). Accumulate-through-climax — all 4 earlier groups stay visible so KIDDING lands on top of a built-up poem. Cascading right with varied top%/alignment so the stack reads as composition, not a subtitle column."
```

This is where per-case judgment earns its keep. The skill gives you a palette of patterns; the pick is yours.

### Spatial coherence — the main slot rule

**Every plan has ONE primary slot.** Most groups land there. Secondary slots exist only for intentional rhythm-breaks (once every ~30s, never per-chunk alternation). The old autogen rotation that threw each chunk to a different corner violated this and read as chaos.

Choose a primary slot based on scene:

- **9:16 portrait, subject mid-frame** → primary slot is `top: 4–20%` (sky / clean zone above the head). Secondary: `top: 72–78%` (below shoulders, above UI). Never: bottom 22% (UI/hand zone per [rule 17](aesthetic-principles.md)).
- **16:9 landscape, subject left** → primary slot is the right column (`left: 50–55%`, right-aligned or centered in the column). Secondary: below subject.
- **16:9 landscape, subject centered** → primary slot is `top: 10–20%` OR `top: 70–80%`. Pick one and stick.

Within the primary slot, vary **size and weight** to create hierarchy (narrator small, body mid, emphasis large, climax huge). That's the rhythm inside a coherent position. Secondary slots are for **break-rhythm moments**, not for adjacent chunks just to "avoid collision".

Collision validator still runs — but now the agent should be hitting it only in exceptional cases (intentional layering), not because every chunk is in a different place.

**Verbatim recipe** — every word is shown, but it is **not** a flat TikTok subtitle rail. Use the cinematic DNA: per-group typography variation, position variation, size modulation. Italic openers, upright pivots, uppercase climaxes, spatial cascade, per-word soft/present tones — all of it.

Chunking: walk the transcript and split into groups of **1–4 words** at pause boundaries (>0.25s gap = hard cut; within a phrase, chunk by emotional beat — short 1–2 word chunks for emphasis words, longer 3–4 word chunks for connective tissue).

Typography per chunk — treat each chunk as a mini-beat. The sizes below are a **starting palette, not rules.** The agent picks the actual `font-size` per group based on the scene's clean-zone width, the phrase's character count, and the desired visual weight relative to neighboring groups. Shift by ±30% whenever the scene demands (narrow portrait column → shrink; wide landscape hero → enlarge). Pick from [typographic-moves.md](typographic-moves.md):

- **Filler / connective** ("you know", "like", "so I was", pronouns, conjunctions) → italic 500–600, small (~0.05–0.08h starting point), softer tone, subordinate position. These read as narrator voice, not statement.
- **Emphasis / content words** (verbs, nouns carrying meaning) → upright 600–800, mid (~0.08–0.12h starting point), centered or cascaded position, present tone.
- **Climax / hook words** (the payoff word of the sentence) → uppercase 800–900, large (~0.14–0.22h starting point), full-frame or near-frame-width, present tone with scale pop.

**Size is always relative, never absolute.** What matters is the _contrast ratio_ between a group and its neighbors inside the same plane — climax should be ~2× the emphasis, emphasis ~1.3–1.5× the narrator. An agent that writes `0.08h / 0.08h / 0.08h` for three caps in a plane has failed regardless of which bucket it picked from. The hierarchy is the point.

Spatial composition: use the full frame as a canvas. Filler chunks tuck to corners or sit small at subordinate positions; emphasis chunks claim the middle; climax chunks own the frame. **Don't lock everything to `bottom: 12%`** — that's the boring-subtitle trap.

Time windows: either spatially-separate overlapping groups (cascade, poem-accumulation) or hand-off so only one chunk shows at a time. Handoff at the same slot reads jittery (too many cuts in a short window) — prefer spatial cascade where adjacent chunks coexist at different positions, or accumulation blocks bounded by sentences.

Layer: default `"bg"` for any chunk whose position has clean scene around it (sky, wall, the area above/below the subject) — that's the embed effect. Use `"fg"` only when the chunk's position would be ≥80% occluded by the body (e.g. chyron-style chunks at bottom in 9:16 portrait where the torso fills that zone).

**Climax chunks across the subject — readability first.** The Vogue-masthead effect (big uppercase crossing the body) is the most cinematic move, but only if the word is still readable. Use `bg` across the subject when **all** of:

1. The caption is multi-line (≥2 lines), so even if one line is mostly eaten, the others stay clean and the viewer can read the phrase. Single-line captions should never sit directly over the face/body — either reposition above/below the subject, or use `fg`.
2. The subject's bounding box covers ≤40% of the caption's total pixel area. For 9:16 portrait with a typical head-and-shoulders subject (~30% vertical × ~50% horizontal at mid-frame), a caption at `top: 16%` spanning 4 lines × 0.14h meets this — the face eats one line, the other three read clean. A caption at `top: 40%` sitting directly on the face does not.
3. Each individual word has visible letter endpoints on at least one side — a word that's split mid-letter with only interior strokes showing is unreadable even if "25% of total pixels" are covered.

If any of these fail, either **reposition** the BG caption to clean scene (above the head / below the shoulders / into an off-center corner), or **fall back to `fg`**. FG for climax is the right call when the scene has no clean zone big enough — don't force the embed aesthetic at the cost of legibility.

Rule of thumb: if you flattened your plan to just the climax chunks, the result should still read as a satisfying tweet-length headline. If it doesn't — you've under-varied your typography and the climax doesn't pop hard enough.


<!-- ===== FILE: hyperframes/embedded-captions/references/direction-catalog.md ===== -->

# Direction catalog

10 distinct aesthetic directions the skill can express. Each is a complete look: font, motion, color, placement, rhetorical defaults. The agent picks by **content tone × shot type × platform**, not preset name.

Current shipped templates (`modes/cinematic/*`) cover about 30% of this catalog. The rest are future ship-ready aesthetics.

Classification matrix — pick direction by intersection:

| Tone ↓ / Platform → | 9:16 portrait                            | 16:9 landscape           | 1:1 square               |
| ------------------- | ---------------------------------------- | ------------------------ | ------------------------ |
| **Documentary**     | documentary-dignified (vertical variant) | documentary-dignified    | broadcast-dignified      |
| **Conversational**  | portrait-header + default                | memory-wall OR champion  | broadcast-dignified      |
| **Energetic**       | high-energy-vlog                         | high-energy-vlog-wide    | high-energy-vlog-sq      |
| **Poetic**          | lyrical-poem-on-wall (portrait)          | lyrical-poem-on-wall     | chapter-card             |
| **Keynote/tech**    | — (9:16 not ideal)                       | tech-keynote-confident   | tech-keynote-confident   |
| **Investigative**   | —                                        | investigative-typewriter | investigative-typewriter |
| **Music video**     | k-pop-lyric                              | k-pop-lyric              | k-pop-lyric              |

---

## Direction specs

### 1. documentary-dignified _(Errol Morris / PBS Frontline)_ — Standard-mode direction (no prebuilt Cinematic template)

- **Family**: Söhne Mono OR GT Sectra for name cards; Inter for body
- **Weights**: 500 body, 700 name card
- **Color**: bone `#F5EFE6` on charcoal, OR charcoal `#1A1A1A` on bone. No accent.
- **Motion**: burn-in (no animation). Held 0.5s past last word.
- **Placement**: bottom-left block, 10% margin, locked position for whole interview.
- **Rules**: 2-line max. Speaker name card once at first utterance + after each cut. No emphasis styling — gravitas IS the style.
- **Rhetorical**: aggressive filler suppression. Every word is chosen.

### 2. cinematic-noir _(Kyle Cooper / Se7en)_

- **Family**: Distressed serif (Hoefler Text) + tight mono for detail
- **Weights**: 700 mostly; thin italic ONLY for whispers
- **Color**: off-white `#E8E0D0` with deep red `#8B0000` single-word accent for menace
- **Motion**: typewriter with 10% chance of 1px jitter on entry; scratched etch for chapter beats
- **Placement**: off-axis — avoid dead-center, slightly high-left or low-right
- **Rules**: no emoji, no rounded corners, everything hand-feeling

### 3. tech-keynote-confident _(Apple / Jony Ive ad)_

- **Family**: SF Pro Display OR Inter, nothing else
- **Weights**: 800 headline keyword, 400 context
- **Color**: pure white on any bg; `mix-blend-mode: difference` fallback for bright scenes
- **Motion**: swipe-reveal from bottom via clip-path (400ms); exit fades 400ms
- **Placement**: dead center, large. NOT lower-third.
- **Rules**: one caption on screen at a time. 2–5 words per caption. Long held silences between. Feels like slides.

### 4. lyrical-poem-on-wall _(extends current memory-wall template)_

- **Family**: Serif with personality — EB Garamond / GT Sectra / Caslon Italic
- **Weights**: 400–500 only. **This direction rejects bold.**
- **Color**: picks up wall via `mix-blend-mode: overlay`, opacity 0.85, no stroke
- **Motion**: etch in 600ms, hold 1.5–3s, etch out
- **Placement**: always on a surface in the scene (back wall, foam, whiteboard). Uses matte pipeline.
- **Rules**: captions are **fewer** than spoken text — 40–60%. Intentional silences. No other tool does this; strong differentiation.

### 5. high-energy-vlog _(controlled Hormozi)_

- **Family**: Inter ExtraBold, uppercase
- **Weights**: 900 always
- **Color**: white body + ONE accent (`#FFD600` or `#00E676`) + narrow 2px dark stroke
- **Motion**: word-pop with elastic, 60ms stagger; active word scales 1.15× on speech onset
- **Placement**: center-frame, ~35% from top
- **Rules**: max 3 words per frame. Hard break at breath pauses. Accent color on ~15% of words. **One full silence every 10s** (what Hormozi imitators miss).

### 6. chapter-card _(Wes Anderson / Grand Budapest)_

- **Family**: Futura Bold (modern) / Archer (warm) / Bodoni (formal)
- **Weights**: 700 chapter title, 400 attribution
- **Color**: pastel hue sampled from scene
- **Motion**: full-frame static card between interview segments
- **Placement**: centered card for chapters; lower-left name card during speech
- **Rules**: chapter cards get their own beat (0.8s silence before, 0.4s after). Feels authored.

### 7. investigative-typewriter _(Frontline / 60 Minutes / Morris Interrotron)_

- **Family**: IBM Plex Mono OR JetBrains Mono
- **Weights**: 500
- **Color**: white with 3px shadow, no stroke
- **Motion**: typewriter char-by-char 25ms/char; cursor blink 600ms after last char
- **Placement**: bottom band with 40% opacity gradient up — **NOT a hard box**
- **Rules**: one line only, two-line max. Every caption ends with 1-frame cursor-hold before next enters.

### 8. k-pop-lyric _(music video typographic flex)_

- **Family**: oversized display serif (Playfair Display / GT Super) + tiny mono detail line
- **Weights**: display 900, mono 400
- **Color**: deep saturated single hue per song/segment
- **Motion**: cascade entries alternating sides; words cross subject with mix-blend
- **Placement**: intentionally LARGE — sometimes bigger than the face
- **Rules**: emotional/musical moments only. Never informational content. **Breaks rule #1 (subject wins) on purpose** — that's the whole point.

### 9. broadcast-dignified _(BBC / NYT documentary standard)_

- **Family**: Helvetica Now / Neue Haas Grotesk
- **Weights**: 500 body, 700 name
- **Color**: white on 40% black gradient pill (not hard box, not plain shadow — gradient is the signature)
- **Motion**: 200ms fade-up, 150ms fade-down
- **Placement**: bottom-center, 10% margin, title-safe locked
- **Rules**: strict BBC — 160–180wpm, 32–34 chars/line, 2 lines max, 1.5s min gap. "Export to broadcast" mode. Boring on purpose. Never wrong.

### 10. conference-lower-third-killer _(B2B but not lame)_

- **Family**: GT America / Aktiv Grotesk
- **Weights**: dual-weight name card — role 400, name 700, same size
- **Color**: scene-sampled accent on name, white on role
- **Motion**: name card swipes in from left 400ms on first appearance only; subsequent static
- **Placement**: lower-left card + active-word highlight inline in dialogue above
- **Rules**: mode for podcast clips, founder interviews, keynote pulls. Sophisticated without being arty.

---

## Which to ship next

Current templates: `memory-wall` (roughly direction #4), `champion` (roughly a mix of #5 and #9), `portrait-header` (default vertical).

Priority ship order based on competitive gap:

1. **documentary-dignified** — no one else does this well; Errol Morris aesthetic is an unserved niche
2. **lyrical-poem-on-wall** (as distinct template) — the one that most uses our matte-embed moat
3. **high-energy-vlog** — matches but out-designs Hormozi/Submagic presets
4. **tech-keynote-confident** — big for product launch videos
5. **investigative-typewriter** — niche but highly distinctive

---

## How the agent picks

1. Classify the clip: `tone × shot × platform` (see matrix above)
2. Look up direction in matrix
3. Read that direction's spec in this file
4. Translate spec into plan.json parameters OR clone the canonical HTML from `examples/`
5. Tune layout per scene (agent judgment, see `aesthetic-principles.md §1–18`)

If no direction fits cleanly → **Standard mode**. Don't fake-fit an ill-matched direction.


<!-- ===== FILE: hyperframes/embedded-captions/references/failure-modes.md ===== -->

# Failure Modes — learned the hard way

Things that broke during skill development. Check against this list before you ship.

## Matting

### CoreML execution provider corrupts face alpha

Running the matting ONNX through the CoreML EP partitions the graph across providers; the mixed-precision boundary produced alpha ≈ 30 (out of 255) inside the subject's face while the background correctly read 0 (observed with the previous RVM engine — don't re-try). Result: caption text visibly shines THROUGH the face.

**Fix**: Only ever use `providers=["CPUExecutionProvider"]` for the matting ONNX. Our script does this; don't "optimize" it by adding CoreML.

### Aspect distortion / sharp channel-stride make the alpha garbage

(historical — the PP-MattingV2 engine was replaced 2026-06-12 by hyperframes `remove-background`; kept because the lessons generalize) Two earned scars from the ONNX era: (1) fixed-size model exports — squashing a portrait clip into a landscape canvas distorts humans; contain-pad (aspect preserved, centered, alpha cropped back) instead. (2) sharp returns a **3-channel** buffer from `.raw()` after resizing a 1-channel raw input — reading it with a 1-channel stride silently produces a smeared, striped, displaced matte that can _look_ plausible. Always `toBuffer({resolveWithObject:true})` and stride by `info.channels` (other scripts in this skill still use sharp).

**Fix**: both handled inside `matte.cjs`; preserve them if you touch it.

### isnet-general-use / u2net_human_seg miss props

rembg's general/human models capture the person but drop handheld props (mic, notebook). If the caption crosses the mic, it will NOT be occluded by the mic — text floats in front of it unnaturally.

**Fix**: For scenes where props matter, either (a) accept that the human-matting model captures what it captures, or (b) add a manual mask ROI for the prop region. We haven't productized (b) yet.

## Layout

### Flex-stacked captions push hidden ones into gesture zone

First champion iteration put all cap elements inside a flex column with `display: block`. Hidden captions (visibility: hidden) STILL reserve flex space. Result: cg-4 "dreaming" got pushed to y=700, landing right on the hand gesture zone and getting clipped.

**Fix**: Inside the caption plane, each `.cap` is `position: absolute` at the same coords. Hidden ones don't occupy layout. Both templates in this skill do it this way.

### Header-overlay on close-crop shots

First champion iteration used a full-width header band across the TOP of the frame (`top: 30, left: 40, right: 40, height: 360, rotateX: -3deg, justify-content: flex-start, align-items: center`). Subject's head crosses the center, eating the middle of every caption. "know, for me" became a faint "now, for" with the letters sliced apart.

**Fix**: On close-crop podcast shots, don't use symmetric full-width bands. Use `corner-column-crown` with caption column in the corner opposite the head.

### Text right-align + align-items: flex-end + no max-width → flows off-screen

If you set `align-items: flex-end` on the plane and don't constrain width, each `.cap` shrinks to content width. Long words then extend left beyond the plane's "visible" box without wrapping, clipping into the subject.

**Fix**: Set `max-width: calc(100% - padding*2)` on each `.cap`. Templates do this.

## Animation

### letterSpacing animation causes inline-block reflow jumps

Had `letterSpacing: "0.04em"` as the "from" value in `tl.fromTo(word, {opacity:0, letterSpacing: ".04em"}, {letterSpacing:"0"}, w.start)`. GSAP snaps the "from" state at w.start. The width of the word then changes over the tween → inline-block reflow → the `.cap` line box recomputes → "Some" visibly jumped between rows as "memories" entered.

**Fix**: Animate only **transform** properties (opacity, y, scale). NEVER animate letter-spacing, font-size, or filter:blur on `.w` spans. Templates follow this.

### Double-fade (container × word) produces a non-linear pop

Fading both the group container AND each word independently multiplies: effective_opacity = container.opacity × word.opacity. Even with matched eases, the combined curve is nonlinear and feels like a snap-in around the 40% mark.

**Fix**: Keep container at fixed `opacity: 1` during the group's life (set via `tl.set` just before first word). Animate only per-word opacity. Templates do this.

## Blending

### mix-blend-mode: overlay vanishes into dark regions

`overlay(white_text, black_bg) ≈ black`. If part of the caption falls on a dark shadow / dark prop, the letters disappear. The first champion render had `SHARP` become `ARP` because "S" and "H" landed in the dark mic's shadow.

**Fix**: For scenes with significant dark regions under the caption, use `mix-blend-mode: screen` (which preserves white on dark). `wall-embed` defaults to overlay (for mid-tone walls); `corner-column-crown` defaults to screen (for dark bookshelves).

### Bright backgrounds wash out screen blend

Opposite problem: `screen(white, bright) ≈ white` regardless of the text — letters become invisible on bright backgrounds like sunlit windows or white walls.

**Fix**: If average luminance of the caption region exceeds 180/255, switch CSS to `mix-blend-mode: normal` with an opaque color. Sample the background pixels in the caption bbox across the clip to check.

## Render pipeline

### Frame-rate mismatch between bg render and matte PNGs

If hyperframes renders at 30fps default but the matte was extracted at 24fps source rate, ffmpeg overlay gets a temporal mismatch — alpha from frame N is overlaid on bg content of some fractional frame ≠ N. Result: person's current silhouette and matte silhouette are shifted by a few frames, so the occlusion lags or leads the body.

**Fix**: Always pass `--fps` to hyperframes render matching the source's native FPS (usually 24). `render-and-composite.sh` reads fps from plan.json and passes it through.

### WebM alpha (VP8/VP9) flaky in Chromium

We tried making foreground an alpha-channel WebM. Chromium's support for VP9 alpha is inconsistent; VP8 alpha needs specific metadata the default ffmpeg encode doesn't produce.

**Fix**: Don't try to put the matte inside hyperframes. Do the overlay in post with ffmpeg against a PNG sequence. `render-and-composite.sh` does this.

## Crown / centered text

### Centered crown eaten by body

Default `.crown-plane` in `corner-column-crown` is `left: 0; right: 0; text-align: center`. That mechanically centers the word at `frame_width/2`. If the subject sits right of center (Jobs at x=1100 in a 1920 frame) OR the word isn't wide enough to poke both clean zones, the body eats 50-70% of the crown and it reads as "THE \_\_\_ S".

**Fix**: Check subject center_x vs frame center before choosing crown strategy (see [layout-heuristics.md § Crown placement](layout-heuristics.md)). Either size the crown large enough to cross both clean zones, or shift it into the larger clean zone with a narrower width. Keep `text-align: center` within the (re-positioned) box, not the frame.

### Crown font too small for frame → half-swallowed

On landscape 1920×1080, a centered crown at 140px is only ~500px wide. If the subject is 700-900px wide, the crown vanishes behind them. Symptom: only "THE" and "S" visible for "THE BEATLES".

**Fix**: For full-frame centered crown, font must be big enough that `crown_width > subject_width + 400`. See font-size table in [typography-presets.md](typography-presets.md). Prefer 180-260px for landscape centered crowns.

### Wider caption column + default font size → underweight

Template defaults (66/78/92/140) assume a ~560px column. Expanding the plane to 700+ px without bumping fonts makes the text feel too small relative to the column.

**Fix**: Column width 600-760 → phrase ~108px, emph ~128px, crown ~220px centered. See table in [typography-presets.md](typography-presets.md).

## Scene admission

### Handheld / fast camera → matte alpha flickers

The matte is temporally smoothed (EMA in matte.cjs) but moderate motion only. Fast camera pans (vlog selfie) still produce frame-to-frame alpha jitter that shows as flickering caption edges.

**Fix**: GUIDE.md decision gate lists handheld vlog as `⚠️` — degrade or refuse. Production version would add `vidstabdetect` compensation; v1 does not.

### Multi-person scenes → matte is ambiguous

The human-matting model segments "foreground" as a single alpha. With two people, it captures both but they're treated as one blob. Captions can't go "behind person A but in front of person B". If the scene has both speakers visible, the skill should split by shot boundaries first.

**Fix**: Either pre-split with PySceneDetect + per-shot planning, or refuse for `⚠️` multi-subject scenes.

### Undetected shot cut inside the clip

Some sources (interviews, broadcast clips) cut to B-roll/archive footage mid-clip. The matte + caption layout assumes the subject is the same person throughout — a hard cut mid-render creates garbage (caption placement relative to old subject applied to a totally different shot).

**Fix for v1**: Probe the clip at 3-5 timestamps before accepting it. If any frame doesn't contain the primary subject at the same position, trim the clip to end before the cut. `Steve Jobs 60 Minutes` cut to Beatles archival at t≈9s, was manually trimmed to 8.5s.

**Fix for future**: Run PySceneDetect as part of the admission gate; split into shots automatically.

### Pillarbox / letterbox content with baked-in graphics

TV archive clips often have pillarbox (black bars at sides) plus baked lower-third logos ("60 Overtime") and date labels ("2003"). These are part of the video file, can't be matted out, and shrink the usable frame area.

**Fix**: Detect black-bar margins in the first frame (scan rows/columns for all-black). Constrain caption safe-zone to `[left_margin+pad, right_margin-pad, top_margin+pad, bottom_margin-pad]`. For Jobs, safe content zone was x=280-1640 (not 0-1920). Layout positions must respect this.

### transcribe.cjs sees an existing transcript and skips

Transcription is Whisper now, via `transcribe.cjs` (it wraps `hyperframes transcribe` — no API key). `hyperframes init --video <mp4>` may itself auto-write a `transcript.json` in hyperframes' raw whisper shape (a flat word array, no top-level `language_code`). `transcribe.cjs` only treats a transcript as done when it's ALREADY in our normalized schema (`{ words: [...], language_code }`); otherwise it (re-)runs Whisper and normalizes the flat word list into `{ words:[{text,start,end,type:"word"}], language_code }`.

**Fix / expectation**: If you init via hyperframes first, expect `transcribe.cjs` to normalize that transcript into our schema. Don't hand-leave a half-normalized file (e.g. our `words` shape but no `language_code`) — that's the one state the skip-guard can misread.

### Transcript gaps > 3s with no speech

If the original audio has a long silence, leaving the caption plane empty feels wrong mid-video. Either (a) let the prior caption linger, (b) show a title-card crown during the silence, or (c) cut the silence out of the clip.

**Fix**: During caption-grouping, detect silences > 3s. The skill should prompt the user about this, not silently proceed.


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


<!-- ===== FILE: hyperframes/embedded-captions/themes/README.md ===== -->

# THEME mode — composed visual constitutions

Theme mode is the third compiler (`scripts/make-theme.cjs`), beside Standard and
Cinematic. It exists because "mode" was a bundle of orthogonal axes pretending
to be one switch. A theme DNA composes its identity from registries implemented
ONCE in the compiler — **paradigms are the unit of code; DNAs are the unit of
identity**. A new look is a JSON file; only a genuinely new paradigm/setpiece
(rare) touches the compiler.

```
theme DNA = body PARADIGM   how the transcript surface lives
          × body LAYER      fg-alpha (rail.html channel) | bg-embed
          × hero SETPIECE   the climax choreography
          × front FX        flash / rings / sparks / scanband / crowdflash / paflash (fg, over subject)
          × PLATE budget    charge-dim (in-page) + punch/shake/grain (_postfx.sh)
          × LINKAGES        declarative theme interactions
```

Standard and Cinematic were, in retrospect, two fixed points of this space.
Standard is now RETIRED (2026-06-12): its rail×embed-climax point is served by
the `anchor` theme (rail paradigm × settle setpiece — the quiet default).
Cinematic remains a separate compiler; do not re-implement it as a theme yet.

## Unification roadmap (strangler fig — interface first, engines later)

The user-facing model is already unified (GUIDE.md Step 0): one catalog of
LOOKS; classic looks pick a DELIVERY (rail | column), themed looks bind their
own. "Standard/Cinematic" are delivery/compiler names, not modes. Remaining
phases, each gated on need — never rewrite for tidiness alone:

- **Phase 2 — one authoring schema.** `lines`/`minors`/`hero` are already
  ~90% shared between standard.json and theme.json; a router that translates a
  single `caption.json` into the engine-specific file removes the last
  user-visible seam. cinematic.json's blocks/planes are the odd one — map the
  common fields, pass engine-specific ones through.
- **Phase 3 — engine convergence.** Port a classic delivery into make-theme
  ONLY when something forces it (e.g. a classic DNA wants a plate budget or a
  setpiece). Acceptance bar: blind A/B on the cap_multi regression scenes vs
  the old compiler — swap engines only when indistinguishable or better. Until
  then the old compilers are the reference implementation of 8 rounds of
  validated typography (lockup/orbit, multi-climax, ratio-lock, per-plane
  legibility, occlusion adjudication) — that machinery is the moat, not debt.

## Body paradigms (registry)

| paradigm      | surface                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                          | layer | entrance verbs                                                                                                                                                                                                                                                                                           | exit verbs                                                                                                                                                                                                                         |
| ------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ | ----- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `rail`        | lower-third lines, replace                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                       | fg    | `stamp` (1f hot appear→crush→recoil→cool), `flick` (tube double-flick), `bootflick` (corrupted-cyan boot 1–2f → settles to UI color; minors keep a cyan/red registration shadow). `stamp` minors cool to `palette.minorCool` (default amber)                                                             | `drop` (mass falls), `powercut` (bright→ghost→off)                                                                                                                                                                                 |
| `panel`       | docked glass console, accumulate + typed                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                         | fg    | `type` (width steps per word, $ prompt, caret blinks)                                                                                                                                                                                                                                                    | hold                                                                                                                                                                                                                               |
| `poem`        | open-space stanzas, accumulate; letters CONDENSE from seeded dust                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                | fg    | `condense`                                                                                                                                                                                                                                                                                               | `drift` (stanza hand-off) + optional dispersal linkage                                                                                                                                                                             |
| `takeover`    | full-frame hard-cut cards, plate dimmed throughout                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                               | bg    | `cut` (+ tension `creep` before silences, auto-detected)                                                                                                                                                                                                                                                 | hard cut / blur dissolve                                                                                                                                                                                                           |
| `lastpage`    | manuscript rail (typed serif) + a seeded field of BLURRED apex-word instances haunting the room from t=0                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                         | bg    | typed rail; field breathes imperceptibly                                                                                                                                                                                                                                                                 | rail fades; field resolves at apex (see `rackfocus`)                                                                                                                                                                               |
| `flaprail`    | split-flap word tiles on a chyron bar (tag + ROW flip-counter; optional odometer chip docks above the bar while the first emphasis line reads)                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                   | fg    | `splitflap` (3 flips: wrong word → wrong word → real word clacks on hot, squash → elastic settle → cools to bone; emphasis tiles keep amber text + underline)                                                                                                                                            | flip-to-blank cascade left→right (completes before the next line)                                                                                                                                                                  |
| `ledboard`    | amber LED departure strip docked lower-third (`body.board` geometry); lines page by vertical scroll-snap (steps(6)) inside the board window; furniture: green platform tag, ticking seconds clock (stacked digit reel), ⚠ DELAYED blinks then pages to ● ON TIME ~0.7s after the apex, idle LED shimmer in dead air ≥1.2s                                                                                                                                                                                                                                                                                                                        | fg    | `ledwipe-mini` (per-word L→R LED column wipe, clipPath steps(len), + 1-frame arrival flicker; emphasis words get the LED-refresh double-blink; last word gets one late refresh)                                                                                                                          | scroll-snap page-up (next line pages in at the same instant)                                                                                                                                                                       |
| `vhsrail`     | camcorder-playback lower third: every word carries a PERMANENT 1px red+cyan misregistration fringe (split clip-path halves); furniture: ▶ PLAY / ◀◀ REW top-left (REW gag in dead air ≥0.7s + the final rewind), ● REC top-right through the apex window, green timestamp bottom-right with 1 Hz blinking colon, idle tape-drift line in long silences, plus apex-coupled artifacts (1-frame white tear band + head-switching noise bar at REC FREEZE, scrub lines at the apex band on the hero rewind)                                                                                                                                          | fg    | `trackglitch` (instant on + 2-frame y-shake + 1-frame band-slice shift of the word's bottom half; emphasis = PAUSE jitter ±1px y oscillation + white noise-band flicker)                                                                                                                                 | REWIND streak left + flat-white echo copy + 2 scrub-line flickers                                                                                                                                                                  |
| `hudrail`     | arcade-cabinet HUD: whole frame plays through CRT overlays (scanlines `body.scan` + corner vignette); docked HUD bar (`body.bar` geometry, 2px accent border, glow) with `body.tags` 1UP / CREDIT furniture — the 1UP tag blinks on the classic 0.45s attract cadence all clip; HUD yields (`body.yield`) while the boss lands                                                                                                                                                                                                                                                                                                                   | fg    | `coinpop` (instant-on + steps(2) scale pop from the baseline + 1-frame white coin-blip tick over the word; emphasis = 3-frame palette swap body→accent→magenta→body)                                                                                                                                     | checkerboard dissolve (words vanish in 2 alternating 2-frame passes, line off ≤ DUR−0.02)                                                                                                                                          |
| `carbonstrip` | cold-war case-file transcript strip docked on the clearer side (manila gradient, punch holes, faint red `body.watermark`, typed `body.header` that types on by width steps); lines live on up to `body.rows` fixed slots; PAGES (broken at full rows, dead-air gaps > 0.7s, and after the hero hand-off line — it is filed away while the stamp owns the frame); the strip top-shadow breathes during the stamp's dead-still hold and the strip yields (`body.yield`) while it lands; the final page is pulled with the whole strip at clip end                                                                                                  | fg    | `hammer` (per-char sets 30ms apart, scale 1.35→1 in one frame = the stamp motif at low amplitude; seeded ±1.2px baselines + seeded ribbon-ink opacity; every strike kicks the strip 1px — y-channel locked while the strip itself tweens; emphasis words get a red ink ellipse drawn around them, 0.25s) | X-row over-strike (3 chunks per line, 0.05s apart, lines 0.16s apart) → carriage yank-down feed → return; roomy cadence in dead air, compressed when the next page is close — always completes before the next page's first strike |
| `laserrail`   | concert lower third: lines centered on a bottom rail (`body.bottomPx`), uppercase laser-green words with a neon text-glow; emphasis words render at `body.minorScale`× with a hotter glow; word centers are BAKED at compile time from the measured char-width table (`assets/fonts/char-widths.json`, ≤3px vs browser ground truth) so the beam aim can't be skewed by font-load timing; per-word furniture = two thin beams (accent from top-left, magenta from top-right) that sweep to CONVERGE on the word 2 frames early + a convergence flare; beams dim ×`yield.beamDim` inside the apex window and the visible line dims to `yield.dim` | fg    | `igniteconverge` (beams converge at st−0.083 → flare pop → word snaps on at opacity 1 with brightness 1.85, crush 0.09s power3.in → 2-frame contact squash → elastic settle → brightness cools; emphasis = single 1-frame strobe off/on + lingering beams)                                               | sweeper beam crosses L→R in 0.13s and each word streaks away (x+44, blur 5) as it passes; line off ≤ DUR−0.02                                                                                                                      |

| `stormrail` | rain-washed lower third: ambient rain = `body.rain.count` seeded thin streaks falling on repeating linear cycle tweens (pure f(t), one slanted wind vector, mid-fall at t=0); a second seeded set DOUBLES the rain for ~1s after the strike; lines sit on a bottom gradient scrim (stable reading surface); the visible line dims to `yield.dim` while the bolt lands and its text-shadow flips toward the strike (`hero.params.side`) for the flash frames | fg | `lightningpop` (the apex motif at low amplitude: instant on at brightness 2.2, y+4, scale 1.06 → 0.12s micro settle; emphasis = sheet-lightning double flash, 2-frame brightness 1.9/1.0/1.8 chain — the bg sky double-kisses at the same beats) | wash downward with the rain (y+22, blur 3, 0.18s power1.in); a line facing dead air washes early at lastWord+1.08s; line off ≤ DUR−0.02 |
| `holorail` | volumetric projection plate: a scanlined glass slab (`body.plateW`×`plateH`, centered at `H − bottomPx`) with corner brackets + feed tag (`body.tag` / `theme.plateTag` override) boots like a projector turning ON (scaleY 0.03→1 expo + 1-frame flicker) and breathes a finite yoyo luminance cycle sized to the clip length; lines sit centered IN the plate (`lineDy` below plate center) with a constant chromatic-fringe text-shadow (−1.5px accent / +1.5px magenta) and drift slowly in rotationY (it IS a projection); the whole railwrap — plate included — dims to `yield.dim` while the apex lands | fg | `sweepboot` (the apex motif at low amplitude: instant opacity + rising clip-wipe reveal 0.15s + 1-frame x interference glitch at st+0.05/0.09/0.13; emphasis = 2-frame projection DROPOUT at `body.emphDelay`, restores brighter in `palette.em` with a hotter fringe, then settles back — the delay auto-shrinks near the line's exit so dropout+restore always complete) | projector cut — brightness 2.2 pop → collapse to a horizontal slit (scaleY 0.045, 0.07s power3.in) → to a dot (scaleX 0.015, 0.06s) → off at exit+0.15; the plate itself gets the same cut at DUR−0.14 |
| `planktonrail` | deep-sea lower third on TWO coexisting row slots: even lines ride the upper row (`H − bottomPx − rowDy`), odd lines the lower (`H − bottomPx`) — couplets share the water like drifting strata. A line clears when its row is next needed (line i+2 in − 0.15) or ~0.3s after its couplet finishes speaking (staggered pair exits, +0.12s on odd rows); the pre-apex leftover clears at heroIn−0.21 while the FEEDING line (last to start before the apex) yields to `yield.dim` instead — no restore unless ≥1.2s of hold remains (it exits dimmed, by design); a line entering during the hold arrives at `yield.enter` and restores at I+`yield.post`; every line floats on a gentle y keyframe drift sized to its window. Furniture: `body.motes` = {count, near, seed} plankton motes on seeded drift walks f(t); the first `near` seed a ring around the apex heart (ring radius scales with hero fontPx/120) and get ATTRACTED to the bloom at I−0.19 (pulled 0.72× toward it, brightening to 0.42 at scale 1.7), wiggle through the hold, and sink at clip end | fg | `glowon` (the apex bloom at low amplitude: 2-frame opacity ramp + radial bloom from word center — scale 0.92→1, blur 5→0, brightness 0.45→1, 0.4s sine.out — while a cyan glow text-shadow grows in; emphasis = slow DOUBLE-BEAT propulsion pulse at st+0.52, 5-key brightness/scale 0.55s, guarded ≤ DUR−0.09) | light sinks — y+15 while dimming, 0.3s power1.in; the last line floats to the end of the clip; line off ≤ DUR−0.02 |
| `sheenrail` | iridescent silk lower third on TWO coexisting row slots: even lines ride the upper row (`H − bottomPx − rowDy`), odd lines the lower (`H − bottomPx`) — couplets read together like a woven pair. Words are aurora-gradient ink (background-clip:text over a rose→teal→violet 300% wash whose backgroundPosition drifts f(t) 0%→300% across the whole clip — the body's hold life) above a blurred dark understroke (top+3px, blur 3); a soft radial band scrim sits under the rows (stable reading surface). Line scheduling mirrors planktonrail: a row clears when next needed (line i+2 in − 0.15) or shortly after its couplet finishes speaking (pairEnd + 0.23 + 0.17 on odd rows); the pre-apex leftover clears at heroIn−0.32 while the FEEDING line stays and dims with the railwrap yield (`yield.dim` at I−`pre`, restore at I+`post` — band included); the last line holds to the end | fg | `flowon` (the ribbon's flow at low amplitude: 2-frame opacity + y8 settle 0.38s sine.out; emphasis = ONE bright sheen sweep — a white highlight marches through the word once at st+0.16 (backgroundPosition −80%→180%, 0.42s power2.inOut) + a brightness 1.55 pulse) | dissolve UPWARD — words to y−12, blur 3, 0.32s power1.in staggered 0.035; each line releases `body.streaks` seeded light streaks (rose/teal/violet verticals) that float up from its row (y 14→−78, 0.62s, start clamped ≤ DUR−0.66) |
| `scoperail` | oscilloscope lower third: a dark phosphor scope band (`body.bandH`, top border + glass shadow) hosts HUD readouts (`body.hudL` left, sample-rate `· TRIG` + amber trig LED right), a graticule, and an ALWAYS-ALIVE waveform — an SVG polyline rebuilt from baked point-set states (seeded pseudo-RMS envelope at ~12 states/s + 3-frame triplets on word arrivals: speech grows the amplitude, silence flattens it, every word kicks a local gaussian burst at its slot center — burst x BAKED at compile time from the measured char-width table; the hero words kick WIDE bursts spread from `HG.x` toward `HG.x + 0.6·halfW`, where the trace surges to write). Body lines sit centered on the band above the trace with reserved-width slots (sizer + clip — no re-center drift as words arrive); the whole band (lines + wave + HUD) dims to `yield.dim` while the apex writes. At the FINAL transcript word the scope DIES: band x-shake, trig LED panics red then dies, the trace explodes to max-amp chaos for ~0.3s, flatlines, collapses to a single dot (scaleX 0.015) and `body.siglost` stamps with a 2-frame flicker (all clamped ≤ DUR−0.02) | fg | `tracewipe` (the apex pen-write at low amplitude: clip wipes the word in L→R over 0.10s + a 2-frame just-traced flash — flash-white instantly, settle to phosphor green; the death word settles to `palette.em` amber; the trig LED blinks on every arrival; emphasis = a ticking frequency-readout chip above the word, 3 seeded ascending values stepping every 2 frames) | the line collapses INTO the waveform (y+30, 0.13s power2.in) — early into dead air (lastWordStart+0.67), else just before the next line needs the slot; the last line collapses as the trace flatlines (min(NZ+0.33, DUR−0.2)) |
| `paperrail` | stop-motion craft table: a kraft strip (torn top edge via seeded polygon clip-path, washi-taped corners, handwritten `body.tag` in the tag font) docked lower-third (`body.strip` geometry, centered by default); body words are cream paper chips (`palette.chip` on `palette.chipEdge` border, hard dy3 shadow) on centered replace-lines; the whole strip jitters ±0.7px every 4 frames (handmade stop-motion weave); the hero slot keeps a red paper star (`palette.accent`, rail↔climax hand-off) that pulses 1.18→1.06→1 as the apex chips land; the FINAL transcript word is an accent-red sign-off chip; emphasis words get a washi-tape slap (steps(2) scale 1.7→1 at `word.start + body.tapeDelay`, chip pressed 1 frame); strip + lines yield (`body.yield`) while the apex lands | fg | `place` (the papermat drop at low amplitude: opacity full in 0 frames + seeded ±2.5° rotation, y −16 + scale 1.06→1 steps(2) 0.12s; hold = rotation-only ~5fps wobble) | `peel` (rotation −8°, y −40, fade, steps(3), staggered 0.03s; last line clamped to finish on frame) |
| `popuprail` | pop-up book page: a cream page strip (`body.strip` geometry, center foldline, top border + paper glow inset) unfolds up from the bottom edge (scaleY 0.02→1 back.out at 0.14 — the stage is built) and hosts TWO reading rows (`body.rowA`/`rowB` px above H) that alternate per line; the whole page breathes a gentle y drift sized to the clip; the hero slot keeps a blue paper star chip (`palette.accent` clip-path star, rail↔climax hand-off — spliced into the line whose window holds heroIn); emphasis words land at `body.emPx` weight 800 with a contact squash (1.06/0.93 set → elastic settle) the strip FEELS (1px dip), then flick-wobble (5-key rotationX, squeezed to fit before the fold) with a blue paper strut leaning in behind (scaleY back.out(2)); the FINAL transcript word is a blue sign-off with a strut; page yields (`body.yield`) while the centerfold lands; on the final word the whole page TILTS 2° +x6 (paper physics, `body.tilt:false` opts out) and the strip folds shut on the last frame (scaleY power3.in ≤ DUR−0.017) | fg | `popup` (the centerfold motif at low amplitude: opacity 1 in 0 frames + rotationX 85→0 baseline hinge, 0.25s back.out(1.4), back-shadow grows as it rises) | `fold` (the page closing: rotationX 88 power2.in 0.12s, shadow off, L→R wave staggered 0.045s, slot hidden at +0.13; fold at next line in / lastWord+`body.maxHold` in silence, wave clamped ≤ DUR−0.017) |
| `chalkrail` | night-lecture chalk band: a deep-green board strip (`body.strip` geometry, worn top hairline, eraser smudges, handwritten `body.tag` header in the tag font, two chalk sticks bottom-right) docked at the bottom edge hosts `body.rows` reading rows that ACCUMULATE — lines fill the rows top→bottom in phases of rows.length; when the next phase needs the rows an ERASER SWIPE clears the board (blurred light band sweeps across 0.42s at `prevEnd + body.eraseDelay` clamped clear of the next phase, the old words SMEAR out scaleX 1.3 + x+24 + blur(8) staggered 0.06s, faint ghost smudges fade in and STAY — chalk never fully erases); the FINAL transcript word lands in yellow chalk (`palette.em` sign-off); the band yields (`body.yield`) while the apex writes | fg | `scribble` (the chalkwrite verb at low amplitude: 2-frame opacity pop + scribble clip-reveal steps(4) 0.12s + y4 drop-settle + 6 seeded dust specks puffing at the word base, seeded ±2° tilt; emphasis = double underline dashes drawn beneath at st+0.22/+0.38) | eraser-swipe smear between phases (scaleX 1.3, x+24, blur 8, power2.in 0.18s); the final phase holds to clip end |
| `markerrail` | street handstyle rail: centered marker lines on a bottom rail (`body.bottomPx`), `palette.body` cream paint with a heavy drop text-shadow; emphasis words take ALTERNATING paint colors (`palette.em`/`em2`, yellow/magenta) + a spray-underline SWOOSH (dash-revealed squiggle viewBox-stretched to the word) with 8 seeded overspray dots that pop and fade; the FINAL transcript word lands BIG (1.5×) in `palette.em` with mini apex-impact physics (crush 0.09s power3.in → 2-frame contact squash → elastic settle — it rides the plate punch); the line visible at the tag's onset yields (`body.yield`, restore only with runway before its buff — else it exits dimmed) | fg | `flick` (the spray-write verb at low amplitude: opacity full in 1 frame at scale 1.18, seeded ±6° rotation settling to ±2°, 1-frame squeak skewX 7, back.out(2.2) settle 0.18s) | ROLLER BUFF (gray paint roller scaleX-sweeps the line 0.15s power2.in, words vanish under it, the wet smear lingers at 0.15 + blur(2) before fading); the last line is never buffed — the sign-off stays painted |
| `brushrail` | washi paper band: a deckle-edged band (`body.strip` geometry, two faintly rotated `paperHi`→`paperLo` under-sheets at 0.42 + a translucent `sheetHi`→`sheetLo` main sheet with warm inset shadow) swipes in L→R behind a traveling brush-head shadow (clipPath wipe 0.2s power2.out + blurred `palette.bh` gradient head — the ink gesture at low amplitude), then the under-sheet breathes faintly (0.32 Hz baked f(t)); body lines are centered replace-lines on the band (`fonts.body` serif at `body.fontPx`/`body.weight`, seeded ±1° tilt); emphasis words get a DOUBLE curved ink underline (`palette.ulInk`, fat 7/0.3 wash + tight 2.6/0.95 core, dash-drawn at st+0.12/+0.15); band + the line under the gesture yield (`body.yield`) while the apex lands; the band exits with the last line on one final R→L wipe | fg | `brush-wipe` (the gesture at low amplitude: clipPath inset reveal L→R 0.16s power2.out with a blurred per-word brush-head shadow riding the reveal edge, then vanishing) | wet-cloth WIPE (the reveal in reverse: the line clipPath wipes R→L over 0.10–0.14s power2.in with an erase brush head riding it, at min(next line − 0.136, lastWord + `body.maxHold`); the LAST line and the band wipe together at DUR−0.142) |
| `inkrail` | sumi ink on still water: up to THREE fixed reading rows at the bottom center (`body.bottomPx` = last-row center, `body.rowGap` apart; rows cycle in pairs, the closing line takes the third row — the final thought ACCUMULATES instead of replacing); `fonts.body` Mincho serif at `body.fontPx`/`body.weight`/`body.letterSpacing`, `palette.body` ink over a paper-white text-shadow halo (`palette.paper`/`paper2` glow stack — readable on bright skies) with a duplicate blurred dark halo per word; an ink-settling RULE (86%-width gradient hairline, scaleX 0→1 over 0.9s) draws beneath each line at firstWord+0.12; emphasis words shed a faint ink wisp curling off the word top (st+0.55, ±dir by line parity, skipped near clip end); the rows visible under the bloom yield (`body.yield` — dim at heroIn+`delay`, restore at heroIn+`post` only with runway before the exit) | fg | `bleed` (the apex bloom at low amplitude: opacity snaps in 2 frames; blur 12→0 + scale 1.25→1 power2.out carry the bleed — late words bleed faster so they resolve before clip end; the dark halo overshoots scale 1.5→1.04 while its opacity decays 0.5→0.25) | RE-DISSOLVE (blur 9 + scale 1.13 + fade + y−8 power1.in — ink dispersing back into the water) as the line-after-next approaches (= the next occupant of its row, outDur 0.5−0.05·i, never mid-read); the closing TWO lines persist to clip end |
| `ransomrail` | kidnapper's collage rail: every transcript word is a cutout chip in one of 4 cycled recipes (cream/`fonts.body` Anton, black/`fonts.dark` Inter-800, newsprint/`fonts.news` Special Elite, accent/`fonts.accent` Permanent Marker — emphasis words snap to the accent chip, never two identical chips in a row) PASTED along the bottom rail line (`body.bottomPx`) with seeded crookedness (rot sign alternates with line+word parity, baseline dy leans the other way), seeded ±px sizes (`body.fontPx`−2..+1, emphasis +3) and torn edges (seeded 12-vertex tear polygon, same paper stock as the apex); chips carry a hard dy5 offset drop-shadow; lines breathe (5-key scale keyframes) through their hold; the whole railwrap yields (`body.yield`, container opacity — never contests per-chip channels) while the apex letters slam | fg | `paste` (the apex slam motif at low amplitude: opacity full in 1 frame at scale 1.12 / rot×1.5 / y−8 → power3.in crush 0.08s → 2-frame contact squash 1.05/0.95 → elastic settle; emphasis = 1-frame RE-PASTE lift at `body.emphDelay` — shadow grows to a flight blur, rotation flips sign for good, then crush + squash + elastic again, rip-runway-guarded) | RIPPED off one by one (rotation ±16/17° throw + y−30 + fade, power2.in, staggered 0.045s) with a 1-frame paper-tear flash under each chip — timed so the rip tail overlaps the next line's pastes a beat (collage chaos, by design); the last line tears off clamped to finish on frame |

fg body uses the **rail.html alpha-webm channel** (true alpha — dark panels and
scrims work; never the screen-blend index_fg path, which can only add light).

## Hero setpieces (registry)

| setpiece      | what happens                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                   | notes                                                                                                                                                                                                                                                                                                                                                                                                                         |
| ------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `detonation`  | charge-dim → sheared stencil slices crush in hot → SNAP into register → squash → elastic settle → paint cools to bone → bars/ticks/designation-tag deploy → shear-apart exit                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                   | pairs with fx flash/rings/sparks + plate punch/shake                                                                                                                                                                                                                                                                                                                                                                          |
| `decode`      | slot-machine glyph reels (steps() ease, seek-safe) lock left→right with RGB jitter → lock snap → CRT power-off exit                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                            | pairs with `redact-until-hero`                                                                                                                                                                                                                                                                                                                                                                                                |
| `drawon`      | the word is WRITTEN stroke-by-stroke from a single-line font (Hershey) — per-stroke paths revealed sequentially at constant pen speed, nib rides `getPointAtLength`, hops at pen lifts; then hum + buzz dip                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                    | any word, zero tuning: `gen-stroke-path.py` lays out glyph pen-paths at compile time                                                                                                                                                                                                                                                                                                                                          |
| `cpslam`      | acid-yellow stencil word slams in BEHIND the subject with REAL diagonal notch cuts (SVG mask = true transparency over footage), chromatic split that settles to a PERMANENT cyan/red registration error, seeded glitch ticks, katakana tag, glitch-out exit                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                    | bounded hold (~2.6s default, `params.hold` / `hero.exitAt` override) — a climax is an event, not wallpaper                                                                                                                                                                                                                                                                                                                    |
| `assembly`    | (inline, poem) apex word condenses BIG while star particles fly into it                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                        |                                                                                                                                                                                                                                                                                                                                                                                                                               |
| `colorflip`   | (inline, takeover) accent-color crush card + dim kick + squash/settle + loom                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                   | pairs with fx flash + plate punch/shake                                                                                                                                                                                                                                                                                                                                                                                       |
| `flapboard`   | split-flap departures board takeover: floodlight dim/scrim swing on, the housing clacks down (rotationX, squash, elastic) behind the subject, one giant flap tile per char flip-cycles 3–5 seeded wrong glyphs then LOCKS left→right across `params.lockWindow` (hot flash → cools to bone) under baked clack y-jitter; lock-complete = big clack + amber glow flicker + rule wipe + steps() status-ticker; hold = loom + one tile re-flutter; exit = tiles flip to blank cascade, housing flips away                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                          | pairs with `fx.crowdflash` (pops at lock start/end) and `plate.punchOffset = lockWindow` so the plate punch lands on the lock-complete clack, not the hero onset                                                                                                                                                                                                                                                              |
| `ledwipe`     | transit LED board takeover: cool scrim + dim charge, an amber dot-matrix panel EXPANDS upward (scaleY steps(6)) behind the subject, header tags + unlit LED ghost boot-flicker alive, then the word ILLUMINATES column-by-column (clipPath L→R, steps ≈ 1.4×chars over `params.wipeDur`) hot → cools to amber; contact = cell squash + elastic settle + PA "ding" double brightness pulse; an 8-phase chasing LED-marquee border runs to the exit; hold = glow breathe + seeded-look LED dropouts; exit = word pages up out of the window, panel collapses back down                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                           | pairs with `fx.paflash` (amber PA flash at wipe-complete contact). Panel geometry derives from fontPx (`panelH = 44 + 1.42×fontPx + 18`); `params.panelW` fixed, width-fit shrinks the type only. Plate: grain-only (no punch) is the demo register                                                                                                                                                                           |
| `vhsosd`      | REC FREEZE camcorder slam: permanent lens vignette (`params.vignette`) + backlight-comp scrim (peak = `plate.charge`, cools to 0.69×) kill the bright sky; the word crushes in as a huge OSD readout — 3 horizontal clip-path tracking bands (`params.bandClips`) sheared (`params.bandShear`) + blurred (power4.in over `params.crush`) SNAP into register on the contact frame, squash → elastic settle; red/cyan misregistration copies cool from ±`misregIn` to ±`misreg` px and keep BREATHING through the hold under tape-weave y jitter (`params.weave`) + slow loom; auto-iris pump (white wash 0.20, dark dip = `plate.dim`); exit at `I + params.hold` = REWIND streak left + flat-white echo copy                                                                                                                                                                                                                                                                                                                                                                   | pairs with the `vhsrail` paradigm, which emits the fg REC-FREEZE artifacts (tear band, head-switching bar, apex scrub lines, ● REC) at the same I/X times. Plate: grain-only (no punch) is the demo register; hold-life keyframes auto-clamp inside [contact, exit]                                                                                                                                                           |
| `bossintro`   | arcade BOSS INTRO: the room dims (gradient `plate.dim`) behind a CRT edge glow (cyan base wash that pulses on the last emphasis word before the boss and spills magenta on the strobe + the final word); `params.tag` (WARNING) blinks 2× above the word rect; ~COLS×ROWS (`params.rows`, cells 0.7×/0.5× fontPx) seeded pixel blocks fall steps(3) from above into a tight matrix grid covering the word rect, each landing with a 1-frame white tick; at `I + params.flashDelay` the word flashes ON (Press Start 2P, instant at opacity 1, scale 1.15 → steps(3) crush → 2-frame squash → elastic settle) with ±4px chromatic ghost layers + a 3-frame palette strobe (white→cyan→magenta→white); hold = quantized 1.6% breathe + CRT glow cycle + baked block shimmer blinks; exit at `I + params.hold` = per-letter checkerboard dissolve, blocks drop away steps(3)                                                                                                                                                                                                      | pairs with the `hudrail` paradigm; emits fg furniture via setpiece fg parts: letterbox bars (`params.letterbox` px) slam in steps(3) with a 1-frame overshoot and retract after the exit, HI-SCORE odometer (accent label, yellow digits) rolls every 0.066s through the hold, 1-frame white tick out. `fx.coinflash` adds the 1-frame radial impact flash at the strike; plate punch anchors at `punchOffset` = `flashDelay` |
| `rubberstamp` | the footage becomes an archive page (vignette charge = `plate.charge`, manila sepia wash `params.sepia`, dim kick = `plate.dim` that cools to 0.385×) and the verdict slams in BEHIND the subject as a bordered rubber stamp at `params.rotation`: a manila paper wash lights an instant before contact, the stamp crushes 2.2→1 power4.in over 0.115s, 2-frame contact squash, double-strike ghost print (`opacity 0.35`, offset +5/−4 rot 1.3), two thin-ink patches (`params.patches` clip-path circles in paper color), wet-ink saturate/brightness settle, paper indent shadow bloom; stamps don't move — the hold is DEAD STILL, sold by the breathing indent + a slow paper loom; exit at `C + params.hold` = mechanical 3-frame yank-down cut (the page is filed away), the archive plate releases 0.25s before                                                                                                                                                                                                                                                        | contact `C = heroIn + params.crush`; pairs with `fx.inkflecks` (seeded red spatter at C, ballistic with gravity) and `plate.punchOffset = params.crush` so the plate punch lands on the stamp contact; pairs with the `carbonstrip` paradigm (strip yield + shade breathe anchor at the same C); face chrome (border, radius, padding, ghost offset) scales with fontPx from the 120px demo cut                               |
| `lasercage`   | concert-blackout laser show: the plate dims to `plate.dim` at t=0 and deepens to `plate.charge` before the drop while haze cones breathe in the top corners; a 6-beam array (alternating accent/magenta, emitters along the top edge) snaps on at I−0.26 and SWEEPS to converge on the word center (staggered 0.022s), a hot core pops at convergence; the word IGNITES behind the subject as an additive glow stack (wide accent blur 0.22×fontPx + magenta fringe offset + tight soft blur + near-white core): scale 1.16 crush power4.in → 2-frame contact squash → elastic settle + 2 controlled strobe pops (brightness 2.05, 1s apart, runway-guarded); a criss-cross beam CAGE (6 lines derived from the word rect) draws itself dash-by-dash around the word and flickers; through the hold the array FANS OUT slowly to floor targets (the iconic concert fan) while the word looms; exit at `heroOut − 0.38` = cage un-draws, beams sweep away L→R (+0.74W) carrying the letters (per-letter streak + blur, stagger auto-clamped ≤ DUR), the room lifts back to 0.12 | word geometry is metric-exact via `assets/fonts/char-widths.json` (cage/spill/flash all derive from `halfW` + `fontPx`); pairs with `fx.laserflash` (accent contact flash at I+0.03, sized 2·halfW+80 × 4.8·fontPx) and the `laserrail` paradigm (same converge-ignite motif at low amplitude); plate punch anchors at `punchOffset` ≈ 0.07 (the ignite contact)                                                              |

| `boltstrike` | THE STRIKE: a slate storm mood (`params.mood`) sits on the room from t=0 and the sky KISSES (1-frame 6% gradient brighten) on every body word — double-kiss on emphasis words, re-flashes at I+0.84/I+1.44 during the hold; the room charge-dims to `plate.charge` under a radial word scrim from I−0.39; a hand-authored branched bolt (5-seg zigzag + 2 branches, haze/glow/core SVG stack in `palette.accent`/`glow`/`core`) flashes 2 frames BEFORE the word — leader 1 → 0.35 → return stroke 1 at contact — with a sky flash; the word slams in (Anton scale 3.1 crush power4.in 0.105s, blur 14→0, brightness 3.2→2.5) → 2-frame contact squash → elastic settle, lit HARD for 2 frames then cools to 1; SIGNATURE: the word's text-shadow flips toward the bolt side for the flash frames; ozone under-glow (accent, blur 26×fontPx/145) blooms at contact and breathes (6-key opacity cycle) through the hold + slow loom + 2-frame lit blips on the sheet re-flashes; the dim releases at the flash, settles to a `plate.dim` storm hold and lifts before the exit; exit at `min(heroOut−0.2, I+params.hold)` = washes downward with the rain (y+38, blur 6) | bolt geometry is baked at compile time as offsets from the word center (halfW/360 × fontPx/145 units, `params.side` flips it); word rect is metric-exact via `assets/fonts/char-widths.json`; word scrim = 2·halfW+380 × 2.28·fontPx; pairs with `fx.strikeflash` (full-frame fg flash with the same leader/return flicker grammar) and the `stormrail` paradigm (rain doubles + shadow flip at the same I); plate punch anchors at `punchOffset` ≈ 0.02 (the return stroke) |
| `holoboot` | full volumetric boot behind the subject: a desk emitter dot pops (back.out scale), the projection cone SNAPS wide (scaleX 0.07→1 expo, 0.11s, then dips 0.55→0.95), a seed beam fires up from the emitter (scaleY power3.in, fades after contact), and the word boots with a RISING clip sweep (opacity instant at I−0.055, the reveal is the wipe) into a 7-layer projection stack (dark backing shadow / wide `palette.glow` blur / magenta + cyan chromatic fringes / `palette.core` word / scanline mask / climbing interference bands, band pitch 0.39×fontPx); contact at I+0.07 = brightness 2.3 flash + scaleX 1.07 / scaleY 0.91 squash held 2 frames + elastic settle + 1-frame x interference jumps; fringes blow ±8px then settle to the permanent ±2px registration offset; hold = bands climb −6 pitches, rotationY oscillates [0,6,−7,5,0], glow/cone breathe, emitter dot pulses, slow 1.028 loom; at `I + params.passAt` (≥ I+1.25, runway-guarded) a hand "passes through" the projection (skew 6/−4/0 + blur + fringe blowout + scaleY ripple — pure projection logic); exit at `min(heroOut−0.22, DUR−0.3)` = projector cut: brightness 2.4 → collapse to a horizontal line (scaleY 0.018) → to the base dot (scaleX 0.015), cone fades, dot pops 2.2× and dies. A second smaller emitter cone (`params.coneW`) rises from the desk under the holorail plate ALL video with baked flicker cycles + dot pulses, and gets its own projector cut at DUR−0.2 | word rect is metric-exact via `assets/fonts/char-widths.json` (cone width 2·halfW+80, emitter at cy+2.4·fontPx, all rig geometry derives from `halfW` + `fontPx`; scene scrim is a radial centered on the hero's frame fractions); pairs with `fx.holoflash` (cyan fg lock flash at I+0.075, radial at the same hero fractions) and the `holorail` paradigm (same sweep-boot + interference-glitch motif at low amplitude; the body cone is aimed at ITS plate); plate: grain-only (no punch) is the demo register, scene reaction = `plate.scrim`/`charge`/`dim` |
| `biobloom` | bioluminescent BLOOM behind the subject: the abyss grade (`params.mood`) + a breathing vignette (6-key opacity cycle sized to the clip) sit on the room from t=0 — the world is underwater before anything speaks; a creature pre-glow (1.083×/0.717× fontPx ellipse) gathers with a double-beat anticipation at I−0.31 and crushes to a point at I−0.115; a dark pocket scrim (`plate.scrim`, 2·halfW+280 × 2.5·fontPx) opens behind the word zone at I−0.03; the word CONDENSES in (scale 2.35 crush power4.in over `params.crush`, blur 15→2, brightness 2.6→1.7) → 2-frame contact squash (1.09/0.93) → elastic settle while cyan light SPILLS onto the scene (radial at the hero's frame fractions: snap 0.55 at contact → 0.2 → shimmer keyframes); 6 luminous tendrils (paired blurred SVG strokes — glow w9/blur5 + core w3/blur1.1, accent/violet/ice alternating) draw outward from the word rect staggered 0.05s (stagger auto-clamps so the last filament completes before the sink); hold = glow breathes 8–14% (4-key scale/opacity), glow-layer flicker, two counter-drifting caustic gradients shimmer over the text zone, the bloom drifts slowly with the current (`params.drift` on the x channel); exit at `min(heroOut−0.2, DUR−0.3)` = the light SINKS — tendrils (via their HTML wrapper, never gsap-y on inner SVG), caustics, pocket, spill and the word all drift down (+14/+26) while dimming, word blurs out | tendril geometry is hand-authored from the demo and baked at compile time as offsets from the word center (x scaled by halfW/demoHalf, y by fontPx/120, endpoints frame-clamped); word rect is metric-exact via `assets/fonts/char-widths.json` (0.01em tracking); pairs with `fx.sporeburst` (seeded spore puffs burst PAST the bloom at contact in the fg layer, ballistic with slight sink) and the `planktonrail` paradigm (same glow-on motif at low amplitude + mote attraction anchored at the same I); plate: pushIn+grain (no punch) is the demo register — the demo's postfx profile was `push` |
| `silkribbon` | aurora silk WRITTEN into the night sky behind the subject: the hero word is a sequential Hershey-stroke reveal (one `<path>` per pen stroke at constant pen speed, `gen-stroke-path.py` baked at compile time — any word, zero tuning) in a blurred halo (`params.haloWidth`, feGaussianBlur 7) + tight core (`params.coreWidth`, white drop-shadow), BOTH stroked by ONE userSpaceOnUse rose→teal→violet linearGradient with reflect spread; SIGNATURE: the gradient's x1/x2 translate f(t) from I−0.07 to the clip end (shift 1.5× the gradient span) so the aurora colors FLOW THROUGH the drawn ribbon during the hold; a soft light mote (blurred halo + core dot) rides the pen, hops at lifts, and blooms out 2.4× at the final stroke; scene reaction = two huge aurora blobs (teal top-left / rose top-right, frame-fraction geometry) drift the sky f(t) from t=0 at `params.wash` and DEEPEN to `params.deepen` as the ribbon writes, a top scrim (`plate.scrim`, 0.653H) charges in at I−0.34 (sky washout guard), a light spill (`params.spill`) tints the sky at I+0.1 once the ribbon completes and flickers gently, and the halo breathes (5-key opacity cycle) through the hold; gentle — no shake, no contact squash: the apex verb is the writing itself; writing window = `params.window` clamped so the ribbon finishes + holds before ENDT = DUR−0.04 | canvas/gradient/spill all derive from `params.targetWidth` (demo: 880 ink on a 1010×280 canvas, baseline 200; svgW = tw+130, spill = (tw+60)×0.51, gradient span = 0.6364·tw), centered at the scene-aware HG (pref top 18, the sky band — same as drawon); pairs with `fx.silkmotes` (seeded aurora motes rise near the ribbon during the hold, fg layer, demo spread fractions keep the face gap) and the `sheenrail` paradigm (same flow motif at low amplitude); plate: pushIn+grain (no punch) is the demo register — the demo's postfx profile was `push` |
| `scopetrace` | the scope's own trace LEAPS off the band and WRITES the hero word behind the subject: a surge column (3px, bottom-anchored scaleY pop, landing at the pen-start point parsed from the baked path) jumps from the scope band at I−0.12; the word is a sequential Hershey-stroke reveal (one `<path>` per pen lift at constant pen speed, `gen-stroke-path.py` baked at compile time — any word, zero tuning; punctuation stripped for the pen) drawn CORE-ONLY in a thin phosphor stroke (`params.coreWidth`, bright `palette.bright` + accent drop-shadows — it is a trace, not a tube), nib rides `getPointAtLength` and pops 2.4× at DRAWN; the phosphor FILL (blurred halo strokes, `params.haloWidth`, blur 7) flicker-arrives AFTER the write at FLICK = DRAWN+`params.flickGap` (pre-arm 2 frames early, 5-step 1/0.25/1/0.55/1 blink, core dips 0.55 for a frame); hold = glow hum (7 Hz + 11.3 Hz sine keyframes, f(t)) + 1.6% breathe on an HTML wrapper with transformOrigin at the hero's frame fractions, ending exactly at the collapse; exit = the word COLLAPSES to a flatline (wrapper scaleY 0.02, 0.14s power3.in, same origin) + a horizontal flash bar (2·halfW wide at the word center) that shrinks out — scheduled at nextSpokenWord − `params.clearGap` (clamped ≥ FLICK+0.45, ≤ heroOut) so the trace clears BEFORE the next line speaks; scene reaction = phosphor radial scrim (`plate.scrim` at the hero fractions, I−0.18 → EXIT+0.05) + green spill sized from targetWidth (`params.spill`); second beat: a 1-frame phosphor pulse answers the FINAL transcript word — the same death beat the scoperail finale owns | trace geometry derives from `params.targetWidth` (svgW = tw+140, local baseline 215, ink center ≈ baseline−28 — the demo registration; surge x parsed from the first `M` of the path); centered at the scene-aware HG (pref top 25, ink height 115); pairs with the `scoperail` paradigm (tracewipe = the same pen-write at low amplitude; the paradigm's hero waveform kicks fire at the same word onsets) and needs no front fx; plate: grain-only (no punch) is the demo register |
| `papermat` | STOP-MOTION PAPERCUT behind the subject: a torn-edge kraft mat (two seeded torn polygon layers) DROPS from above with steps(2) gravity and slaps down (squash → rest, soft blob shadow); then one torn cream chip per char (`palette.paper`/`paper2`, hero-font ink `palette.ink`) drops with steps(3) gravity + 1-frame overshoot at `I + i·params.step`, each announced by an anticipation shadow 3 frames early, landing crooked (seeded ±3° ±4px), settling through three 12fps poses, then holding an 8fps wobble (baked set chain — the stop-motion heartbeat) while the whole tableau breathes 1.6% (camera-push loom); scene reaction = a warm vignette (`params.vig`) charging with the landing; on the FINAL word the table BUMPS (y4, 1 frame) and the chips SCATTER off down-right steps(4) staggered 0.045s, the mat swept off last (disperse-on-last-word, `hero.exitAt` overrides) | chip geometry derives from `hero.fontPx` (demo ratios: tile 0.91×/1.31× fontPx, pitch tile+14, mat N·pitch+80 × 1.846× fontPx), width-fit shrinks type and chips together; pairs with `fx.paperscraps` (paper scraps puff at each chip contact, fg) and the `paperrail` paradigm (same place verb at low amplitude); plate: grain only is the demo register |
| `centerfold` | POP-UP BOOK CENTERFOLD behind the subject: blue + cream 12-point paper starbursts (deterministic starPts polygon, `palette.accent`/`cream` fills with kraft-edge strokes) unfold on a baseline hinge (scaleY 0.03→1 back.out(1.6), cream staggered +0.06) starting I−0.272 while a blob shadow grows beneath; the hero word pops up at I in `params.segs` hinged clip-path segments (rotationX 85→0 back.out(1.4) staggered `params.segStagger` — the body's popup verb at full amplitude); two kraft struts lean in at I+0.33; backdrop + word wobble-settle TOGETHER (one `#cfWob` wrapper owns rotationX, 6-key) then breathe through the hold (word 5-key rotationX + shadow scaleX, both auto-squeezed into the window); scene reaction = a dusk radial scrim at the hero's frame fractions (`params.scrim`, bright-sky insurance) charging with the unfold; exit = the whole spread folds FLAT (segments rotationX 88 staggered, struts/bursts scaleY collapse cream-then-blue, scrim out) at `max(I+segStagger·(segs−1)+0.45, min(heroOut−0.33, DUR−0.39))` — the book closes before the next sentence | burst geometry derives from the word rect (metric-exact via char-widths: burstR = clamp(1.83·fontPx, 0.59·wordW, 0.42·H), box 2R+180 × 2R+fontPx, demo props scale at burstR/220), width-fit shrinks the type first; pairs with `fx.confetti` (seeded ballistic paper confetti launched from the hinge line at I+0.128, fg) and the `popuprail` paradigm (same baseline-hinge verb at low amplitude); plate: grain only is the demo register |
| `chalkwrite` | NIGHT LECTURE behind the subject: the lower chalk band grows into a FULL deep-green board (scaleY 0→1 power3.out from the bottom edge at I−0.3, the room dims `params.dim` + vignette `params.vig` with it); the hero word is HAND-WRITTEN in chalk — sequential Hershey stroke reveal (drawon pattern, `gen-stroke-path.py` baked at compile time), dry/rough via seeded ±1px jitter on every pen point (`params.jitterSeed`), a blurred halo (`params.haloWidth`, feGaussianBlur 3.2, group opacity `params.halo`) under a tight core (`params.coreWidth`), a chalk-stick nib (rotated rect) riding the pen — while `params.dustN` dust specks fall from the nib along the path; at write-complete a hand-slap CLAP shakes the board 1 frame (set-chain y 3/−2/1/0; the dust burst lives in the rail, in FRONT: `fx.chalkclap`), then TWO violent accelerating underlines slash beneath (seeded waviness, power3.in, the nib rides them, dust kicks at the ends), the chalk flicks away, and the halo breathes (baked 1.6/3.7 Hz f(t)) through the hold with two slow motes drifting off the letters | geometry registers on the MEASURED ink box (the stroke path is parsed at compile time; ink CENTER lands on scene-aware HG.y, pref top 44): the board rect (`params.boardGap`×inkH above the ink, bottom flush with the frame, width = the body strip), the underlines (inkL+14→inkR−4 at inkBot+30/+50) and the fg clap point (the pen's LAST contact point → HG.clapX/Y/T) all derive from it; x defaults to the board's LEFT margin + tw/2 — a hand writes from the left, never centered on the subject (`theme.hero.x` overrides); pairs with `fx.chalkclap` (12 seeded radial dust specks + a blurred puff at DRAWN, fg) and the `chalkrail` paradigm (same scribble verb at low amplitude); plate: grain only is the demo register; needs `python3` |
| `spraytag` | STREET TAG behind the subject: the dusk wall dims (`params.dim`) + a radial scrim charges (`params.scrim`) at I−0.42 as the writer steps up; the can RATTLES at the pen-start point (6 seeded set-chain nib jitters, I−0.30→I−0.02), then the hero word is spray-written stroke by stroke — sequential Hershey dash reveal at constant pen speed (`gen-stroke-path.py` baked at compile time) — as a TRIPLE stack per stroke: fat dark under-stroke `palette.under` (`params.underWidth`, sky-contrast armor) + blurred overspray halo (`params.haloWidth`, feGaussianBlur 7, group opacity `params.haloOpacity`) + wet paint core (`params.coreWidth`, drop-shadow), the glowing nib (r9, `palette.nib`) riding each stroke; `params.osprayN` seeded overspray dots pop near the nib as it passes; nib throws off 2.6× at DRAWN; through the hold `params.drips` seeded DRIPS (paint→`dripMid`→`dripLo` gradient bars) grow from painted low points (x-separated >110px) and KEEP growing, the halo hums (7/11 Hz baked f(t)) and the whole tag looms 1.014; writing window = `params.window` (demo 0.58s) clamped so write + splat + drip fit before ENDT = DUR−0.04 | geometry registers on the MEASURED ink box (ink CENTER lands on scene-aware HG.y, pref top 26 — the sky band, crossing the subject silhouette is the point; tag centers on the hero anchor, `targetWidth` capped at W−140); the pen-finish point is baked onto HG.splatX/Y/T for the fg splat; pairs with `fx.paintsplat` (hot `em2` ring + paint ring + seeded ballistic droplets at DRAWN, fg, in FRONT of the subject) and the `markerrail` paradigm (same flick verb at low amplitude); plate: punch with `punchOffset` ≈ window+0.05 so the punch lands on the splat, not the hero onset; needs `python3` |
| `brushwrite` | SUMI-E GESTURE behind the subject: a warm paper wash (`palette.wash`/`wash2` radial, `targetWidth`+380 × `params.washH`) charges at I−0.18 to `params.wash`, settling to `params.washSettle` through the hold; the brush SLAPS down at the first pen point — a start-SPLAT (irregular ink ellipse rotated −24° + 5 seeded satellite dots, scale 0.35→1 power3.out 0.12s; the fg fleck pass rides `fx.brushflecks`) — then the hero word is written in ONE sequential gesture (Hershey dash reveal at constant pen speed, `gen-stroke-path.py` baked at compile time) as a FOUR-layer stack per stroke: blurred bleed (`params.bleedWidth`, feGaussianBlur 6, group hidden until the hold) under fat/mid/core widths (`fatWidth` 0.25 / `midWidth` 0.6 / `coreWidth` 1.0 stroke-opacity = pressure-tapered wet brush), the round ink nib (r7.5, `palette.nib`) riding the pen and flicking off (+42,−30, scale 1.9) at DRAWN; ≤`params.spatterN` spatter droplets eject PERPENDICULAR at the sharpest-curvature points of the gesture (angle-delta > 0.55 rad, te-separated > 0.045s); through the hold the ink BLEEDS into the paper (bleed group fades to `params.bleed` over ≤1.7s) and the whole work breathes 0.6% (`params.breatheHz` baked f(t), svgOrigin = ink center); then the vermilion SEAL chop (`params.sealGlyph`, `palette.seal`/`sealMid`/`sealLo` radial face, `fonts.seal` glyph) stamps at DRAWN+`params.sealDelay` — power4.in crush 0.09s → 2-frame squash → elastic settle + 3 seeded red flecks — skipped entirely if the clip ends too soon; writing window = `params.window` (demo 0.45s) clamped so write + seal + bleed fit before ENDT = DUR−0.04 | geometry registers on the MEASURED ink box (ink CENTER lands on scene-aware HG.y, pref top 19 — the sky band, crossing the subject silhouette is the point; gesture centers on the hero anchor, `targetWidth` capped at W−240 — on scenes with a dark object near the pen start, set `theme.hero.x` so the slap-down lands clear, like the demo's 864); the pen-START point is baked onto HG.fleckX/Y/T for the fg flecks and the seal sits at (inkR−103, inkBot+72) clamped on frame (`params.sealDx/sealDy` override); pairs with `fx.brushflecks` (seeded upward ballistic ink flecks at the slap-down, fg, in FRONT of the subject) and the `brushrail` paradigm (same brush-wipe verb at low amplitude); plate: punch with `punchOffset` ≈ window+`sealDelay` so the punch lands on the seal CONTACT, not the hero onset; needs `python3` |
| `ransomnote` | RANSOM NOTE slam behind the subject: one cutout chip per letter (4 recipes cycled, seeded ±13% sizes around `hero.fontPx`, alternating-sign rotations ±2–5°, misaligned baselines ±2–6px, seeded tear-polygon edges) slams in oversized (scale 1.5, rot×1.8, flight drop-shadow) at S_k = I + 0.01 + `params.step`·k, crushes power3.in over 0.085s, and on contact the shadow POPS tight (1-frame filter swap) → 2-frame squash 1.07/0.93 → elastic settle; when the LAST letter lands the whole word takes a collective 1-frame JOLT (y6 → power3.out) + a scene pulse (`params.pulse` full-frame dark blink); hold = slow 5-key loom (the crooked grid never straightens); exit = letters RIPPED off one by one (rot+±15–22° throw, y−34, fade, 1-frame tear flash under each) at ripT = min(lastWord − `params.ripLead`, DUR-clamped), ≥ jolt+0.45; scene reaction = collage scrim (`params.scrim` top-dark gradient) charges at I−0.07, out with the rip | width-fit measures each glyph IN ITS OWN recipe font (`assets/fonts/char-widths.json`) + 0.20em chip padding + 6px margins so the collage never overflows; chip chrome (shadows, space width) scales with fontPx from the 130px demo cut; the setpiece RECOMPUTES `plate.punchOffset` = 0.01 + step·(N−1) + crush from the real letter count so the plate punch always lands on the collective jolt, whatever the hero word length; pairs with the `ransomrail` paradigm (same paste verb + tear flashes at low amplitude, same recipe classes/seeded tear polygon emitted into both layers); no front fx — the flashes live inside the chips |
| `inkbloom` | INK DROP IN STILL WATER behind the subject: paper-white radial washes charge the two text zones (`palette.wash` rail wash from t≈0.15, PERSISTS to clip end so the closing body lines keep their ground — it registers on the body row geometry `body.bottomPx`/`rowGap`; `palette.washApex` apex wash at I−0.077, out with the bloom) and a gentle vignette (`params.vig`) STILLS the world while the ink blooms; the drop (ink teardrop, `params.fall` 0.15s) appears above the word point at I−0.08, swells, falls power2.in with a scaleY stretch, squashes 1.7/0.35 on contact (2 frames) and merges into the BLOOM — 3 stacked blurred irregular ink ellipses (`palette.ink`, opacity snaps 0.82/0.62/0.5 then decays) scaling at different rates with counter-rotations (expo.out 1.15/1.35/1.5s) + 2 thin concentric ripple rings expanding 7.2×/9.6× on the water surface; the hero words RESOLVE out of the blob (opacity snaps, blur 16→0 + scale 1.12→1 power2.out) — the FIRST at contact+0.02, the following at their own spoken times (multi-word hero, per-word hand-off); through the hold the glyph edges BREATHE (baked 5-key blur keyframes per word, alternating 0.66/0.5s), the group looms 1.018 and two faint ink wisps curl off the word top (C+0.573/C+0.753, fit-guarded); exit: RE-DISSOLVE (blur 11 + scale 1.15 + fade, 0.52s power1.in) at XOUT = min(I+`params.maxHold`, next body line − `params.clearGap`, DUR−0.6) — the ink clears before the next thought needs the reader | geometry derives from the measured word rect (`assets/fonts/char-widths.json`; kx = halfW/demoHalf, ky = fontPx/132 scale the demo's blob/ring/wisp anchors; pref top 25 — the sky band, crossing the subject silhouette is the point); dark `palette.ink` + its paper washes carry the contrast on bright skies; pairs with the `inkrail` paradigm (same bleed verb at low amplitude); plate: quiet `pushIn`, no punch — the bloom is liquid, not percussive |

Inline setpieces (`hero.inline: true`) live inside the body paradigm — the hero
word stays in `lines`. Embed setpieces own the word: leave it OUT of `lines`
(rail↔climax hand-off), except `panel` + `redact-until-hero`, where the words
appear in the log as `█████` until the decode locks.

A setpiece may additionally return `fgCss/fgHtml/fgJs` — those parts are merged
into the fg alpha page (rail.html), for furniture that must ride ABOVE the matte
(e.g. a verbatim chip that may never be occluded) while the setpiece scenery
stays embedded behind the subject.

## Linkages

- `redact-until-hero` — panel log shows hero words as blocks; un-redacts at lock
- `corrupt-on-last-word` — panel jitters + hue-shifts on the final word
- `disperse-on-last-word` — every visible poem letter scatters back to dust
- `field-is-the-apex` — (lastpage) the blurred future-field rack-focuses at the
  apex: every faint line was the apex word all along; the main instance holds,
  the rest re-blur and die

## Hard rules inherited (do not relax)

- determinism: paused GSAP on `window.__timelines["main"]`, seeded PRNG only,
  set-chains / keyframes, no Math.random/Date.now/CSS-keyframes
- 80 ms word sync (timings come from transcript.json via the strict matcher;
  any uncovered transcript word is a compile ERROR — verbatim completeness)
- apex owns the frame: fg furniture must avoid the setpiece rect or yield
  (`body.yield`) during the hero window
- plate punch/shake ALWAYS post-composite (`_postfx.sh`) so subject + text +
  plate move as one photographed frame (matte never desyncs)

## SVG gotchas (paid for, do not rediscover)

- dash patterns restart on EVERY subpath → sequential per-stroke paths, never
  one dashoffset across a multi-stroke word
- round linecap renders a DOT at dashoffset=len → hide each stroke until its turn
- inline-block trailing spaces collapse → word gaps via margin, not text spaces
- SVG-font glyph y is UP → flip when converting (gen-stroke-path.py does)
- NEVER gsap x/y/scale on raw SVG children: it runs `_parseTransform`/getBBox, and
  zero-area shapes (fan-kit slivers) trip GSAP's bbox hack → `appendChild` on a
  null docElement in injected-gsap contexts (preview-frames, renderer). Jitter
  SVG pieces via `attr:{transform:"translate(...)"}` only; scale/loom belongs on
  an HTML wrapper div. Nuance: a ROOT `<svg>` inside a div has null
  ownerSVGElement → GSAP classifies it as HTML (CSS transforms, no getBBox), so
  scale/skew on the svg root is safe — but copying that onto an inner `<g>`
  becomes the fatal class. attr transforms can't TWEEN — use frame-quantized
  step chains (identical on screen at 24fps)

## Timeline ownership rules (audit-derived, do not relax)

- ONE owner per (target, property) at any instant. A duration tween re-renders
  every tick until it ends — any set/tween on the same property inside that
  window gets visually overwritten a frame later (1-frame ghosts, flash-backs).
  Known shapes: yield dim vs line exit; yield restore vs powercut set-chain;
  per-word line-y bounces with word gaps < 0.22s. The rail emitter guards these
  (bounce ownership tracker, dim clamped ≥ line-in, restore only with ≥0.3s
  runway before exit — else the line exits dimmed, by design).
- Inverted clamps: `Math.max(lo, Math.min(hi, x))` with lo > hi silently pins to
  lo. When a lockup is wider than the frame, CENTER it (x = W/2) instead of
  clamping — decorative bleed must be symmetric.
- The overflow gate only measures elements with direct text nodes — SVG-painted
  setpieces (mask text + rects) are invisible to it. Do not read its "ok" as
  proof for svg lockups; judge those on the preview frames.

## theme.json — full schema

```json
{ "dna": "<themes/*.json name>",            // required
  "lines": [["word","word",...], ...],       // required — verbatim transcript tokens, in order,
                                             //   INCLUDING punctuation ("size.", "noise.")
  "minors": ["word", ...],                   // optional — theme's inline emphasis treatment
  "hero": { "match": "word or phrase",       // required — exact transcript tokens (case-insensitive,
                                             //   punctuation-stripped match); first occurrence wins
            "text": "DISPLAY FORM",          // optional display override
            "out": 5.9, "exitAt": 3.3 },     // optional window overrides (seconds)
  "width": 1280, "height": 720,              // optional, default 1280x720 (theme DNAs are tuned
                                             //   for 16:9; vertical needs a DNA variant)
  "fps": 24,                                 // optional — matte.fps is AUTHORITATIVE when present
  "panelHeader": "..." }                     // optional (panel paradigm)
```

Scene awareness (inherited from the existing typography system): when
`safe-zones.json` is present the compiler re-anchors the hero setpiece to the
measured occlusion bands (`heroBands.profile`, 18–55% occlusion, closest to the
setpiece's preferred height) and `heroAnchor.centerXPct`, width-fits the hero
font to the actual word, and docks panel/poem furniture on
`subject.clearerSide`. Explicit `theme.json` values > scene auto > DNA fallback.

Expected (benign) log noise: `[Browser:REQUESTFAILED] GET source.mp4
net::ERR_ABORTED` during the fg-layer page load, reel-glyph overflow lint
lines, and `media_missing_data_start` — all cosmetic; the render is good if
render-theme.sh exits 0 and prints the gates summary.

## Authoring a project (this is ALL a user writes)

`<project>/theme.json`:

```json
{
  "dna": "ordnance",
  "lines": [
    ["The", "stars", "were", "only", "limited"],
    ["by", "the", "pixel", "size."],
    ["It's"],
    ["what", "you", "can", "actually"],
    ["recover", "from", "the", "noise."]
  ],
  "minors": ["stars"],
  "hero": { "match": "remarkable" }
}
```

- `lines` follow the transcript verbatim, in order (compile error otherwise);
  every transcript word must be covered by `lines` ∪ `hero.match` — the example
  above omits "remarkable" from `lines` precisely because `hero.match` covers it
  (it slots between `["It's"]` and `["what",...]`)
- leave the hero word(s) out of `lines` for embed setpieces; keep them for
  inline setpieces and for panel+redact
- `takeover`: each line is one CARD — group by beat (1–2 words), not subtitle
  length; `panel` scrolls automatically past ~5 lines (terminal scroll)
- the ordnance "charge" is an edge vignette + rail yield (the center stays
  clean by design) — judge it at the frame corners, not the center
- `minors`: words that get the theme's inline emphasis treatment
- preview first: `node scripts/make-theme.cjs <project>` then
  `node scripts/preview-frames.cjs <project> <t1> <t2> ...` (Visual QA)
- then: `bash scripts/render-theme.sh <project>` → **`final_fx.mp4`** (the
  deliverable; `final.mp4` is pre-plate-reaction)

Prereqs identical to other modes — `prepare.sh` outputs: transcript.json,
frames_fg/, matte.fps, safe-zones.json (scene awareness), source.mp4.
frames_bg/ is only needed by preview-frames.cjs, not by the render.

## Adding a theme DNA

Copy a `themes/*.json`, change identity fields. You may ONLY combine existing
paradigm/setpiece/linkage names — if the look you want needs a new mechanism,
that is a registry contribution (this file + make-theme.cjs), reviewed like an
engine change. A DNA that needs per-word visual tuning to ship is rejected:
**any input, zero hand-fixing** is the acceptance bar (the draw-on lesson).
