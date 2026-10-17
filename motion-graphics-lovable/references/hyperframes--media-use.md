

<!-- ===== FILE: hyperframes/media-use/GUIDE.md ===== -->

---
name: media-use
description: Agent Media OS for a HyperFrames project. Resolve BGM, SFX, image, icon, brand logo, voice, color grade, or LUT into a frozen local file or paste-ready block + ledger record (one verb, `resolve`); generate via TTS / music / image models when the catalog misses; produce voiceover, transcription, captions, and background removal through one shared audio engine; operate on media (cut / reframe / transform); and reuse assets across projects. Also use for vague feedback that real footage looks dark, flat, boring, should feel retro/camcorder/print/ASCII, needs privacy, or needs a media reveal. When the host app provides its own music or sound-effect tools, use those for music and sound effects; `resolve --type bgm|sfx` needs the heygen CLI. When `HEYGEN_API_BASE` is set, HeyGen calls go through that host with no CLI sign-in.
---

**Plugin installs:** Before setup or freshness commands, follow [plugin execution rules](../hyperframes/references/plugin-installation.md) when this skill is inside a HyperFrames plugin. Standalone installs keep the update instructions below.

# media-use

The media OS for HyperFrames: resolve · generate · operate · remember — every media type, one skill, zero context noise.

Only when `HEYGEN_API_BASE` is set in your environment (a host app set it and pays for HeyGen with its own key): HeyGen media is already paid for. Do not ask the person to install or sign in to the `heygen` CLI and do not offer its OAuth allowance; catalog search, TTS and avatar calls here go through the host. When that same host also gives you its own HeyGen tools, use those first. When a call through the host is refused, tell the person the host's message as written (it names the fix, such as adding or replacing the key in the app's Settings) and stop; do not switch to another provider unless they ask.

First run otherwise (no `HEYGEN_API_BASE`), when you will use HeyGen media (catalog search, TTS, avatar video): install and sign in to the `heygen` CLI (the free-usage path), then verify with `npx hyperframes media-use resolve --doctor`. Setup and providers: `references/setup-providers.md`.

Music and sound effects inside a host app: when the app you run in gives you its own music or sound-effect tools, use those. Without `HEYGEN_API_BASE`, `resolve --type bgm` and `--type sfx` search the HeyGen catalog through the `heygen` CLI; without it they fail and say so (`sfx` still answers from its bundled library).

Without `HEYGEN_API_BASE`, before generating a voiceover or an avatar video, tell the person: signing in to the heygen CLI with OAuth (`heygen auth login --oauth`) gives a free allowance for TTS voiceover and avatar videos, while an API key bills API credits.

## Resolve — the one verb

```bash
npx hyperframes media-use resolve --type <type> --intent "<description>" --project <dir>
```

Returns one line: `resolved <id> → <path> (<type>, <metadata>)`. All search noise stays on disk.

| Type    | One-line intent                                                                  |
| ------- | -------------------------------------------------------------------------------- |
| `bgm`   | background music (HeyGen catalog via the `heygen` CLI, 10k+ tracks)              |
| `sfx`   | sound effects (bundled 19-file library + catalog via the `heygen` CLI)           |
| `image` | photos, backgrounds (HeyGen asset search, 75k+ vectors)                          |
| `icon`  | icons, symbols (transparent)                                                     |
| `logo`  | official brand marks (theSVG → GitHub avatar → favicon; never redrawn)           |
| `voice` | TTS voiceover (HeyGen free-usage path; optional local Kokoro)                    |
| `grade` | measured correction candidate; broad polish/stylization follows Media Treatments |
| `lut`   | user-provided or explicitly chosen reusable validated `.cube` file               |

Before resolving fresh, list reusable candidates with `--candidates` and judge fit yourself — reuse rules, all flags, ingest (`--from`), and adopt are in `references/resolve.md`.

## Treat broad visual feedback as media intent

When a user explicitly asks to fix, polish, stylize, obscure, emphasize, or
reveal photographic media, read `references/media-treatments.md` even if they
do not name color grading or an effect. Inspect the real `<img>`/`<video>`,
choose one primary intent, then use deterministic persistence and verification.
Use a matching recipe as an optional tested seed, or inspect
`hyperframes media-treatment --capabilities --json`, then request one relevant
family/effect with `--capability <id>` and assemble a custom treatment from
canonical controls. Never load `--all` for ordinary authoring. A treatment may
compose correction, a preset, finishing, compatible shader effects, supported
keyframes, and optional Registry overlays. Add only source-justified bounded
tuning and compatible parts, never effects merely to make the result look more
sophisticated. Persist the final combined payload with
`hyperframes media-treatment`.

Use one progressively escalating workflow. For video, inspect one labeled
early/middle/late contact sheet rather than reading frames separately. Apply one
candidate and inspect one after-sheet for ordinary correction or polish.
Escalate to individual frames or moving draft evidence only when the result is
ambiguous, temporal, stylized, LUT-based, HDR/LOG-sensitive, private, or
brand-critical.

For ordinary correction or polish, persist the final treatment's
preset/adjustment JSON.
Do not generate a `.cube` LUT merely to encode exposure, shadows, contrast, or
warmth. Use a LUT only when the user supplies one or the selected treatment
explicitly owns one. `resolve --type grade --for ... --analyze` is measurement
evidence, not permission to replace the chosen treatment with a generated LUT.
Do not recreate supported vignette, grain, blur, pixelate, color, or treatment
effects with CSS/SVG overlays; that bypasses Studio controls and the canonical
preview/render shader path.

## Be proactive — run a media opportunity pass

The human usually can't tell which media would lift the piece. You can. When you build or review a composition, do **one** grounded scan and then **ask once** — don't silently add, and don't nag per asset.

Surface an opportunity only when a concrete signal is present:

| Signal detected                                          | Offer                                                                                                  |
| -------------------------------------------------------- | ------------------------------------------------------------------------------------------------------ |
| On-screen text / a script with no voiceover              | TTS voiceover (audio engine)                                                                           |
| Emoji or a `<div>` styled as an icon                     | resolve real `icon`s                                                                                   |
| Image that is a placeholder, tiny, or upscaled-looking   | a better `image` (and/or upscale — see `references/operations.md`)                                     |
| Hard scene cuts / transitions with no sound              | transition `sfx`                                                                                       |
| A piece over ~10s with no music bed                      | `bgm`                                                                                                  |
| Footage that reads under/over-exposed or color-cast      | a corrective grade (inspect it with `hyperframes media-treatment --selector '#hero' --analyze --json`) |
| Photographic media that feels visually flat or off-topic | one specific source-appropriate preset or custom treatment, with the intended target named             |
| A meaningful media entrance/reveal that feels static     | one supported seek-safe treatment animation; preserve color unless the request also justifies a preset |

Rules that keep this a help, not nagware: **grounded, not generic** (no signal → no suggestion); **opinionated + concrete** (propose the specific fix with defaults chosen — the human approves **all / some / none**); **once per project** (one consolidated ask; respect "leave it"); **surface, never silently mutate** (color grades especially: propose and preview — a gray-world "correction" ruins an intentional sunset or neon look).

## Where to look — read only the file your task needs

| Task                                                                      | Read                             |
| ------------------------------------------------------------------------- | -------------------------------- |
| resolve / reuse / adopt / ingest, flags, cascade, inventory               | `references/resolve.md`          |
| color grading, LUTs, smart grade (`--for`), grade-compare                 | `references/grading.md`          |
| voiceover / TTS, music, SFX, captions, transcription (audio engine)       | `references/audio.md`            |
| cut / reframe / transform existing media, exact error diffusion, HEVC     | `references/operations.md`       |
| source-aware creative treatments, realtime effects, overlays, reveals     | `references/media-treatments.md` |
| install + auth, provider table, RAM ladders, `--local-only`, `--provider` | `references/setup-providers.md`  |
| remembered preferences + frozen recipes (user memory)                     | `references/memory.md`           |
| ownership matrix, usage stats, telemetry, privacy (maintainer-facing)     | `references/meta.md`             |


<!-- ===== FILE: hyperframes/media-use/audio/assets/sfx/CREDITS.md ===== -->

# SFX Credits

All sound effects in this directory are sourced from [Pixabay](https://pixabay.com/sound-effects/) and used under the [Pixabay Content License](https://pixabay.com/service/license-summary/).

The Pixabay license allows free use for commercial and non-commercial purposes without attribution, but attribution is appreciated and given here for transparency.

## Files

The following `.mp3` files are bundled with this skill:

- `chime.mp3`
- `click.mp3` / `click-soft.mp3`
- `error.mp3`
- `glitch-1.mp3` / `glitch-2.mp3` / `glitch-3.mp3`
- `impact-bass-1.mp3` / `impact-bass-2.mp3`
- `key-press.mp3`
- `notification.mp3`
- `ping.mp3`
- `pop.mp3`
- `riser.mp3`
- `sparkle.mp3`
- `typing.mp3`
- `whoosh.mp3` / `whoosh-short.mp3` / `whoosh-cinematic.mp3`

See `manifest.json` for per-file metadata (duration, energy character, recommended use).

## License

All files are distributed under the [Pixabay Content License](https://pixabay.com/service/license-summary/), which permits:

- Commercial and non-commercial use
- Modification and remixing
- Redistribution as part of derivative works (such as videos rendered with HyperFrames)

without any attribution requirement.


<!-- ===== FILE: hyperframes/media-use/audio/references/bgm.md ===== -->

# Background music (BGM)

One music bed per composition, produced by the shared audio engine (`scripts/audio.mjs` → `scripts/lib/bgm.mjs`). Two routes, chosen by the engine's one switch — whether a HeyGen credential is present:

- **HeyGen retrieval — the default when credentialed.** Search HeyGen's music catalog by mood, download the top track. No generation; same `~/.heygen` / `$HEYGEN_API_KEY` credential as TTS.
- **Local generation (Lyria → MusicGen) — the fallback when there is no credential** (or when asked for explicitly). Generate a WAV from a mood prompt. There is **no `npx hyperframes bgm` command**; the engine spawns `scripts/lyria-recipe.py` or an inline MusicGen script directly.

> **Run the Preflight first — no credential is not a green light to silently generate locally.** Before generating, complete the sign-in **Preflight** (see `../../GUIDE.md` → Preflight): run `npx hyperframes auth status`, recommend signing in, and **STOP for the user's choice** (sign in for HeyGen's music library, or continue offline with local generation). This applies to a one-off "generate a BGM" request just as much as inside a full workflow.

## Driving it from the request

`audio_request.json` → `bgm: { mode?, query?, prompt? }`:

- **`mode`** — `retrieve | generate | none`. Omit for **auto** (retrieve when credentialed, else generate). An **explicit** `retrieve` is strict: no credential ⇒ skip, never a detached generate (so a caller with no `wait-bgm` step, e.g. product-launch, can't get a pending job it won't await).
- **`query`** — the mood, used for retrieval and as a fallback prompt seed (e.g. a storyboard's `music:` field, falling back to `message` → `arc` → `"calm cinematic underscore"`).
- **`prompt`** — an explicit full prompt for generation; omit and the engine infers one (see Mood inference). Optional `blob` / `archetype` / `arc` feed that inference.

Both routes keep a file of yours already at the output name: the engine writes the next free name (`track-2.mp3`), reports it as an anomaly, and `bgm.path` carries the real path.

## HeyGen retrieval (default)

`searchSounds(query, "music", { limit: 5 })` → `GET /audio/sounds?query=<mood>&type=music&limit=5`. Take the top result (ranked by `score`), download its presigned `audio_url` → `assets/bgm/track.mp3`. Synchronous. No match → skip (BGM is optional; never fail the render over it). Cue written to `audio_meta.json`:

```jsonc
{
  "path": "assets/bgm/track.mp3",
  "volume": 0.12,
  "mode": "retrieve",
  "query": "calm cinematic underscore",
  "duration_s": 42.0,
}
```

`volume` comes from the engine's `bgmDefaultVolume()`: `BGM_BED_VOLUME` (currently `0.12` ≈ -18 dB — a bed under the voice) under narration, `BGM_SILENT_VOLUME` (currently `0.9`) for a silent film (no voice). Tune those constants in `scripts/lib/bgm.mjs`, not call sites. An explicit `volume` in `audio_meta.json` always overrides this default. `bgm_pending` is `false` — the file is on disk when the engine returns.

For short launch videos, do not assume the beginning of the retrieved file is the best edit point. Check the opening against later five-second sections. If the track starts with a quiet build but a later section has a stronger, clean musical entrance, trim from that section and apply a short fade-in and longer fade-out. Repeat this check whenever the composition duration changes; the final music file must cover the full cut without a silent tail.

## Local generation (fallback) — Lyria → MusicGen

Spawned **detached** so voice work isn't blocked; `audio_meta.bgm_pending: true` and `bgm_pid` / `bgm_log` are set until it finishes. **Run `scripts/wait-bgm.mjs` before assembling** — it polls the output file / process / log, detects crashes, and writes `bgm_status.json` (`status: ready | failed | timeout | disabled`). A failed/absent track is simply omitted; it never blocks voice/SFX.

| Order | Provider                             | Env / deps                                                                            | Speed                                   | Quality                     |
| ----- | ------------------------------------ | ------------------------------------------------------------------------------------- | --------------------------------------- | --------------------------- |
| 1     | Google Lyria RealTime                | `$GEMINI_API_KEY` or `$GOOGLE_API_KEY` + `google-genai` (auto-installed on demand)    | Real-time stream (≈ requested duration) | Production-grade            |
| 2     | MusicGen (`facebook/musicgen-small`) | Python `transformers + torch + soundfile + numpy` (~300 MB first run; auto-installed) | Slow on CPU; fast on Apple MPS / CUDA   | Decent; prompt-only control |

Output → `assets/bgm/track.wav`, target = total voice duration. MusicGen generates **one** seed clip (≤28–30s, under the decoder's positional limit) then crossfade-loops it up to the target (or trims down if shorter), avoiding per-segment seams. Backend selection is by what can actually **run**: Lyria only when `import google.genai` succeeds, else MusicGen; if neither can be made to run, BGM is skipped (voice + SFX still render).

## Mood inference (the generate prompt)

`inferBgmPrompt()` in `scripts/lib/bgm.mjs`: an explicit `prompt` wins; otherwise industry-keyword **base** → narrative-**archetype** shape → emotional-**arc** tiebreaker.

| Match in `blob` / `query`                              | Base prompt                                                                 | BPM |
| ------------------------------------------------------ | --------------------------------------------------------------------------- | --- |
| `crypto / nft / web3 / defi / token / blockchain`      | atmospheric electronic, deep bass, futuristic synths, restrained percussion | 100 |
| `finance / fintech / bank / payment / invest / wealth` | calm cinematic, soft strings, subtle piano, restrained percussion           | 92  |
| `creative / agency / design / studio / art / brand`    | playful electronic, warm pads, light percussion                             | 115 |
| _(default: SaaS / tech / platform)_                    | uplifting corporate tech, bright modern piano with synth pads               | 108 |

Archetype then reshapes the arc — PAS → "MINOR to MAJOR" build; BAB / future-pacing → aspirational rising; feature-cascade → +10 BPM driving; demo-loop → −8 BPM minimal. The emotional arc breaks remaining ties (tension→relief, excitement, trust/reassurance).

## Lyria knobs (direct recipe use)

The engine bakes BPM / scale into the **prompt text** (via the inference above) and passes only `--output` / `--duration` / `--prompt` to the recipe. If you invoke `scripts/lyria-recipe.py` directly you can also set: `--bpm` (90–110 calm, 110–130 energetic), `--brightness` (0–1, ≥0.7 promotional), `--density` (0–1, higher = fuller), `--scale` (`MAJOR` / `MINOR` / `PENTATONIC` / …), `--negative-prompt` (styles to exclude). MusicGen ignores all of these — put the mood in the prompt.

## Failure modes

| Failure                                       | Behavior                                                                                 |
| --------------------------------------------- | ---------------------------------------------------------------------------------------- |
| No music match (retrieve)                     | `bgm: null`, anomaly logged. Render proceeds without BGM.                                |
| Explicit `retrieve`, no credential            | Skipped (no silent generate fallback). Use `mode: generate` or omit `mode` for auto.     |
| Neither Lyria nor MusicGen can run (generate) | `bgm` disabled with a `pip install …` hint. Voice + SFX still render.                    |
| Generate still rendering at assemble time     | `bgm_pending: true`; `wait-bgm.mjs` waits/checks and writes `bgm_status.json` first.     |
| Generate crashed                              | `wait-bgm.mjs` → `bgm_status.json { status: "failed" }`; the `<audio>` track is omitted. |

BGM failure never blocks a render.


<!-- ===== FILE: hyperframes/media-use/audio/references/captions/authoring.md ===== -->

# Captions

<!-- registry-items: allow=max-width,data-composition-src,hyperframes-registry,blend-mode,caption-style,font-family -->

**The live search is the source of truth for what the registry has.** The table(s) below are a hand-maintained sample and under-cover by design: run `npx hyperframes catalog --query "<what you want>" --json` — it needs nothing installed — before concluding the registry lacks something. Item names here are checked against `registry/registry.json` by `bun run lint:skills`.

Before authoring: confirm the transcript came from the right Whisper model. CLI default `small.en` silently translates non-English audio — see [`../transcribe.md`](../transcribe.md) → "Language Rule" and [`transcript-handling.md`](transcript-handling.md) for the mandatory quality check.

Analyze spoken content to determine caption style. If user specifies a style, use that. Otherwise, detect tone from the transcript.

## Transcript Source

```json
[
  { "id": "w0", "text": "Hello", "start": 0.0, "end": 0.5 },
  { "id": "w1", "text": "world.", "start": 0.6, "end": 1.2 }
]
```

`id` (`w0`, `w1`, …) is the stable reference for per-word overrides and is added by `hyperframes transcribe`. It's optional for backwards compatibility with hand-authored transcripts. See [`../transcribe.md`](../transcribe.md) → "Output Shape" for how this is produced, and [`transcript-handling.md`](transcript-handling.md) for cleanup before consumption.

## Style Detection (When No Style Specified)

Read the full transcript before choosing. Four dimensions:

**1. Visual feel** — corporate→clean; energetic→bold; storytelling→elegant; technical→precise; social→playful.

**2. Color palette** — dark+bright for energy; muted for professional; high contrast for clarity; one accent color.

**3. Font mood** — heavy/condensed for impact; clean sans for modern; rounded for friendly; serif for elegance.

**4. Animation character** — scale-pop for punchy; gentle fade for calm; word-by-word for emphasis; typewriter for technical.

## Per-Word Styling

Scan for words deserving distinct treatment:

- **Brand/product names** — larger size, unique color
- **ALL CAPS** — scale boost, flash, accent color
- **Numbers/statistics** — bold weight, accent color
- **Emotional keywords** — exaggerated animation (overshoot, bounce)
- **Call-to-action** — highlight, underline, color pop
- **Marker highlight** — for beyond-color emphasis (highlight sweep, circle, burst, scribble, sketchout), see `hyperframes-animation/rules/css-marker-patterns.md`.

## Script-to-Style Mapping

| Tone         | Font mood                | Animation                          | Color                       | Size    |
| ------------ | ------------------------ | ---------------------------------- | --------------------------- | ------- |
| Hype/launch  | Heavy condensed, 800-900 | Scale-pop, back.out(1.7), 0.1-0.2s | Bright on dark              | 72-96px |
| Corporate    | Clean sans, 600-700      | Fade+slide, power3.out, 0.3s       | White/neutral, muted accent | 56-72px |
| Tutorial     | Mono/clean sans, 500-600 | Typewriter/fade, 0.4-0.5s          | High contrast, minimal      | 48-64px |
| Storytelling | Serif/elegant, 400-500   | Slow fade, power2.out, 0.5-0.6s    | Warm muted tones            | 44-56px |
| Social       | Rounded sans, 700-800    | Bounce, elastic.out, word-by-word  | Playful, colored pills      | 56-80px |

## Word Grouping

- **High energy:** 2-3 words. Quick turnover.
- **Conversational:** 3-5 words. Natural phrases.
- **Measured/calm:** 4-6 words. Longer groups.

Break on sentence boundaries, 150ms+ pauses, or max word count.

## Positioning

- **Landscape (1920x1080):** Bottom 80-120px, centered
- **Portrait (1080x1920):** Lower middle ~600-700px from bottom, centered
- Never cover the subject's face
- `position: absolute` — never relative
- One caption group visible at a time

## Text Overflow Prevention

Use `window.__hyperframes.fitTextFontSize()`:

```js
var result = window.__hyperframes.fitTextFontSize(group.text.toUpperCase(), {
  fontFamily: "Outfit",
  fontWeight: 900,
  maxWidth: 1600,
});
el.style.fontSize = result.fontSize + "px";
```

Options: `maxWidth` (1600 landscape, 900 portrait), `baseFontSize` (78), `minFontSize` (42), `fontWeight`, `fontFamily`, `step` (2).

CSS safety nets: `max-width` on container, `overflow: visible` (**not** `hidden` — hidden clips scaled emphasis words and glow effects), `position: absolute`, explicit `height`. When per-word styling uses `scale > 1.0`, compute `maxWidth = safeWidth / maxScale` to leave headroom.

**Container pattern:** Full-width absolute container, centered. Do **not** use `left: 50%; transform: translateX(-50%)` — causes clipping at composition edges.

## Caption Exit Guarantee

Every group **must** have a hard kill after exit animation:

```js
tl.to(groupEl, { opacity: 0, scale: 0.95, duration: 0.12, ease: "power2.in" }, group.end - 0.12);
// `tl.set` is an instant flip, not a tween — safe to set `visibility` here (core's "no animating
// visibility" rule applies to tweens, which can't smoothly interpolate non-numeric values anyway).
tl.set(groupEl, { opacity: 0, visibility: "hidden" }, group.end);
```

Self-lint after building timeline — place **before** `window.__timelines[id] = tl` so it runs at composition init:

```js
GROUPS.forEach(function (group, gi) {
  var el = document.getElementById("cg-" + gi);
  if (!el) return;
  tl.seek(group.end + 0.01);
  var computed = window.getComputedStyle(el);
  if (computed.opacity !== "0" && computed.visibility !== "hidden") {
    console.warn(
      "[caption-lint] group " + gi + " still visible at t=" + (group.end + 0.01).toFixed(2) + "s",
    );
  }
});
tl.seek(0);
```

## Pre-Built Caption Components

Before building caption styles from scratch, check the registry — 15 ready-to-use caption components cover the most common styles. Install with `npx hyperframes add <name>` and wire as a sub-composition via `data-composition-src` (see `hyperframes-registry`).

```bash
npx hyperframes catalog --tag caption-style   # list all caption components
npx hyperframes add caption-highlight         # install a specific one
```

| Style                     | Component                    | Best for                     |
| ------------------------- | ---------------------------- | ---------------------------- |
| TikTok-style highlight    | `caption-highlight`          | Social, high-energy          |
| Karaoke pill              | `caption-pill-karaoke`       | Music, lyric videos          |
| Cinematic editorial       | `caption-editorial-emphasis` | Documentary, storytelling    |
| Glitch / cyber            | `caption-glitch-rgb`         | Tech, gaming                 |
| Full-screen slam          | `caption-kinetic-slam`       | Hype, announcements          |
| Neon glow                 | `caption-neon-glow`          | Night, club, neon aesthetics |
| Neon accent (multi-color) | `caption-neon-accent`        | Colorful, playful            |
| Wipe reveal               | `caption-clip-wipe`          | Clean, modern                |
| Gradient fill             | `caption-gradient-fill`      | Vibrant, eye-catching        |
| Matrix decode             | `caption-matrix-decode`      | Sci-fi, tech reveals         |
| Emoji pop                 | `caption-emoji-pop`          | Social, casual               |
| Parallax layers           | `caption-parallax-layers`    | Depth, cinematic             |
| Particle burst            | `caption-particle-burst`     | Celebration, impact keywords |
| Lava texture              | `caption-texture`            | Bold, dramatic               |
| Weight shift              | `caption-weight-shift`       | Elegant, typographic         |

Related: `caption-blend-difference` (tagged `text` / `blend-mode`, not `caption-style`, so it won't appear under the filter above) auto-inverts text against any background via `mix-blend-mode: difference` — useful when the background is busy or unpredictable.

Browse all with previews: [hyperframes.heygen.com/catalog](https://hyperframes.heygen.com/catalog)

Caption components ship with transparent backgrounds — they're pure overlays. If the underlying video is bright or busy, add a contrast layer (e.g. a semi-transparent dark div) in the host composition beneath the caption sub-composition, not inside the component itself.

## Further References

- [`motion.md`](motion.md) — karaoke, marker effects, audio-reactive modulation, scatter exits.
- [`transcript-handling.md`](transcript-handling.md) — input formats, quality checks, cleaning, external API fallback.
- `hyperframes-animation/rules/css-marker-patterns.md` — marker highlighting (deterministic, fully seekable).

## Constraints

- Deterministic. No `Math.random()`, no `Date.now()`.
- Sync to transcript timestamps.
- One group visible at a time.
- Every group must have a hard `tl.set` kill at `group.end`.
- Fonts: the compiler auto-embeds only its **built-in mapped set** (Inter, Roboto, Montserrat, …) — for those, just declare `font-family` in CSS. Any **other** font (a brand/custom font like `TT Norms Pro`, or a non-Latin CJK/Devanagari family) is **not** auto-supplied: it needs an `@font-face` pointing at a real `.woff2` shipped with the project, or the text silently falls back to a generic font in the render. Don't assume a `font-family` you can see locally will render — the render machine is a clean headless Chrome with no installed fonts.


<!-- ===== FILE: hyperframes/media-use/audio/references/captions/motion.md ===== -->

# Dynamic Caption Techniques

You are here because GUIDE.md told you to read this file before writing animation code. Pick your technique combination from the table below based on the energy level you detected from the transcript, then implement using standard GSAP patterns.

## Technique Selection by Energy

| Energy level | Highlight                             | Exit                | Cycle pattern                             |
| ------------ | ------------------------------------- | ------------------- | ----------------------------------------- |
| High         | Karaoke with accent glow + scale pop  | Scatter or drop     | Alternate highlight styles every 2 groups |
| Medium-high  | Karaoke with color pop                | Scatter or collapse | Alternate every 3 groups                  |
| Medium       | Karaoke (subtle, white only)          | Fade + slide        | Alternate every 3 groups                  |
| Medium-low   | Karaoke (minimal scale change)        | Fade                | Single style, vary ease per group         |
| Low          | Karaoke (warm tones, slow transition) | Collapse            | Alternate every 4 groups                  |

**All energy levels use karaoke highlight as the baseline.** The difference is intensity — high energy gets accent color + glow + 15% scale pop on active words, low energy gets a gentle white shift with 3% scale.

**Emphasis words always break the pattern.** When a word is flagged as emphasis (emotional keyword, ALL CAPS, brand name), give it a stronger animation than surrounding words (larger scale, accent color, overshoot ease). This creates contrast.

**Marker highlight modes add a visual layer on top of karaoke.** For emphasis words that need more than color/scale, add a marker-style effect: highlight sweep, circle, burst, scribble, or sketchout. See `hyperframes-animation/rules/css-marker-patterns.md` for implementation details. Match mode to energy: burst for hype, circle for key terms, highlight for standard, scribble for subtle.

## Audio-Reactive Captions (Mandatory for Music)

**If the source audio is music (vocals over instrumentation, beats, any musical content), you MUST extract audio data and add audio-reactive animations.** This is not optional — music without audio reactivity looks disconnected. Even low-energy ballads get subtle bass pulse and treble glow.

No special wiring is needed. The group loop already iterates over every caption group to build entrance, karaoke, and exit tweens. At that point, read the audio data for each group's time range and use it to modulate the group's animation intensity with regular GSAP tweens.

```js
// Load audio data inline (same pattern as TRANSCRIPT)
var AUDIO = JSON.parse(audioDataJson); // { fps, totalFrames, frames: [{ bands: [...] }] }

GROUPS.forEach(function (group, gi) {
  var groupEl = document.getElementById("cg-" + gi);
  if (!groupEl) return;

  // Read peak energy for this group's time range
  var startFrame = Math.floor(group.start * AUDIO.fps);
  var endFrame = Math.min(Math.floor(group.end * AUDIO.fps), AUDIO.totalFrames - 1);
  var peakBass = 0;
  var peakTreble = 0;
  for (var f = startFrame; f <= endFrame; f++) {
    var frame = AUDIO.frames[f];
    if (!frame) continue;
    peakBass = Math.max(peakBass, frame.bands[0] || 0, frame.bands[1] || 0);
    peakTreble = Math.max(peakTreble, frame.bands[6] || 0, frame.bands[7] || 0);
  }

  // Modulate entrance — louder groups enter bigger and glowier
  tl.to(
    groupEl,
    {
      scale: 1 + peakBass * 0.06,
      textShadow:
        "0 0 " + Math.round(peakTreble * 12) + "px rgba(255,255,255," + peakTreble * 0.4 + ")",
      duration: 0.3,
      ease: "power2.out",
    },
    group.start,
  );

  // Reset at exit so audio-driven values don't persist
  tl.set(groupEl, { scale: 1, textShadow: "none" }, group.end - 0.15);
});
```

This shapes the animation at build time, not playback time — no per-frame callbacks, no `tl.call()` loops, no async fetch timing issues. Loud groups come in with more weight and glow; quiet groups come in soft. The audio data modulates _how much_, the content determines _what_.

Keep audio reactivity subtle — 3-6% scale variation and soft glow. Heavy pulsing makes text unreadable.

To generate the audio data file:

```bash
python3 skills/hyperframes-creative/scripts/extract-audio-data.py audio.mp3 --fps 30 --bands 8 -o audio-data.json
```

## Combining Techniques

Don't use the same highlight animation on every group — cycle through styles using the group index. Don't combine multiple competing animations on the same word at the same timestamp. Vary techniques across groups to match the content's pace changes.

**Marker highlight effects** layer well with karaoke — use karaoke for the word-by-word reveal, then add a marker effect on emphasis words only. For example: karaoke highlights each word in white, but brand names get a yellow highlight sweep and stats get a red circle. Cycle marker modes across groups for visual variety.

## Runtime Tools

Caption motion uses standard HyperFrames runtime APIs. Use the canonical sources:

- **GSAP timeline + tween syntax** — `hyperframes-animation/adapters/gsap.md` (eases, position parameter, performance)
- **`window.__hyperframes.fitTextFontSize` / `pretext`** — `hyperframes-core/references/determinism-rules.md` → Layout Contract (overflow prevention, per-frame text measurement)
- **Audio data extraction** — generate via `python3 skills/hyperframes-creative/scripts/extract-audio-data.py audio.mp3 --fps 30 --bands 8 -o audio-data.json`, then load inline as shown in "Audio-Reactive Captions" above


<!-- ===== FILE: hyperframes/media-use/audio/references/captions/transcript-handling.md ===== -->

# Transcript Guide

For the `transcribe` CLI invocation, the `.en`-translates-non-English rule, and whisper model selection, see [`../transcribe.md`](../transcribe.md). This file covers what to do with the resulting transcript when authoring captions: input formats, mandatory quality checks, cleaning code, external-API fallbacks.

## Supported Input Formats

The CLI auto-detects and normalizes these formats:

| Format                | Extension | Source                                                                      | Word-level?       |
| --------------------- | --------- | --------------------------------------------------------------------------- | ----------------- |
| whisper.cpp JSON      | `.json`   | `hyperframes init --video`, `hyperframes transcribe`                        | Yes               |
| OpenAI Whisper API    | `.json`   | `openai.audio.transcriptions.create({ timestamp_granularities: ["word"] })` | Yes               |
| SRT subtitles         | `.srt`    | Video editors, subtitle tools, YouTube                                      | No (phrase-level) |
| VTT subtitles         | `.vtt`    | Web players, YouTube, transcription services                                | No (phrase-level) |
| Normalized word array | `.json`   | Pre-processed by any tool                                                   | Yes               |

**Word-level timestamps produce better captions.** SRT/VTT give phrase-level timing, which works but can't do per-word animation effects.

## Transcript Quality Check (Mandatory)

After every transcription, **read the transcript and check for quality issues before proceeding.** Bad transcripts produce nonsensical captions. Never skip this step.

### What to look for

| Signal                       | Example                                | Cause                                                                        |
| ---------------------------- | -------------------------------------- | ---------------------------------------------------------------------------- |
| Music note tokens (`♪`, `�`) | `{ "text": "♪" }` or `{ "text": "�" }` | Whisper detected music, not speech                                           |
| Garbled / nonsense words     | "Do a chin", "Get so gay", "huh"       | Model misheard lyrics or background noise                                    |
| Long gaps with no words      | 20+ seconds of only `♪` tokens         | Instrumental section — expected, but high ratio means speech is being missed |
| Repeated filler              | Many "huh", "uh", "oh" entries         | Model is hallucinating on music                                              |
| Very short word spans        | Words with `end - start < 0.05`        | Unreliable timestamp alignment                                               |

### Automatic retry rules

**If more than 20% of entries are `♪`/`�` tokens, or the transcript contains obvious nonsense words, the transcription failed.** Do not proceed with the bad transcript. Instead:

1. **Retry with `medium.en`** if the original used `small.en` or smaller:
   ```bash
   npx hyperframes transcribe audio.mp3 --model medium.en
   ```
2. **If `medium.en` also fails** (still >20% music tokens or garbled), tell the user the audio is too noisy for local transcription and suggest:
   - Providing lyrics manually as an SRT/VTT file
   - Using an external API (OpenAI or Groq Whisper — see below)
3. **Always clean the transcript** before building captions — filter out `♪`/`�` tokens and entries where `text` is a single non-word character. Only real words should reach the caption composition.

### Cleaning a transcript

After transcription (even with a good model), strip non-word entries:

```js
var raw = JSON.parse(transcriptJson);
var words = raw.filter(function (w) {
  if (!w.text || w.text.trim().length === 0) return false;
  if (/^[♪�\u266a\u266b\u266c\u266d\u266e\u266f]+$/.test(w.text)) return false;
  if (/^(huh|uh|um|ah|oh)$/i.test(w.text) && w.end - w.start < 0.1) return false;
  return true;
});
```

For model-selection guidance by content type, see [`../transcribe.md`](../transcribe.md) → "Picking a model by content type".

## Using External Transcription APIs

For the best accuracy, use an external API and import the result:

**OpenAI Whisper API** (recommended for quality):

```bash
# Generate with word timestamps, then import
curl https://api.openai.com/v1/audio/transcriptions \
  -H "Authorization: Bearer $OPENAI_API_KEY" \
  -F file=@audio.mp3 -F model=whisper-1 \
  -F response_format=verbose_json \
  -F "timestamp_granularities[]=word" \
  -o transcript-openai.json

npx hyperframes transcribe transcript-openai.json
```

**Groq Whisper API** (fast, free tier available):

```bash
curl https://api.groq.com/openai/v1/audio/transcriptions \
  -H "Authorization: Bearer $GROQ_API_KEY" \
  -F file=@audio.mp3 -F model=whisper-large-v3 \
  -F response_format=verbose_json \
  -F "timestamp_granularities[]=word" \
  -o transcript-groq.json

npx hyperframes transcribe transcript-groq.json
```

## If No Transcript Exists

1. Check the project root for `transcript.json`, `.srt`, or `.vtt` files.
2. If none found, run [`../transcribe.md`](../transcribe.md) — pick the starting model from "Picking a model by content type" there.
3. Run the quality check above. If it fails, retry with a larger model or fall back to manual lyrics / external API.


<!-- ===== FILE: hyperframes/media-use/audio/references/remove-background.md ===== -->

# Background Removal

Make a transparent overlay (typical: a talking head over an arbitrary scene). Uses `u2net_human_seg` (Apache-2.0).

```bash
npx hyperframes remove-background subject.mp4 -o transparent.webm          # default: VP9 + alpha
npx hyperframes remove-background subject.mp4 -o transparent.mov           # ProRes 4444 (editing)
npx hyperframes remove-background portrait.jpg -o cutout.png               # single-image cutout
npx hyperframes remove-background subject.mp4 -o subject.webm \
  --background-output plate.webm                                           # both layers, one pass
npx hyperframes remove-background subject.mp4 -o transparent.webm --device cpu
npx hyperframes remove-background --info                                   # detected providers
```

## Output Format

- **`.webm` (VP9 alpha)** — default. Plug straight into `<video>` for Chrome-native transparent playback (~1 MB / 4s @ 1080p).
- **`.mov` (ProRes 4444)** — round-trip in editors (Premiere / Resolve / DaVinci). ~50 MB / 4s.
- **`.png`** — single-image cutout.

## Quality (`--quality`)

Controls VP9 encoder CRF only — segmentation quality is fixed. Higher quality keeps the cutout's RGB closer to the source MP4 (important when overlaying the cutout on its own source).

| Preset     | CRF | When                                          |
| ---------- | --- | --------------------------------------------- |
| `fast`     | 30  | Iterating, smaller files, looser color match  |
| `balanced` | 18  | **Default**; visually identical for most uses |
| `best`     | 12  | Master / final delivery, tightest color match |

## Device (`--device`)

`auto` (default) picks CoreML on Apple Silicon, CUDA when available, otherwise CPU. Force with `--device cpu | coreml | cuda`. CUDA requires `HYPERFRAMES_CUDA=1` plus a GPU-enabled `onnxruntime-node` build. Use `--info` to inspect detected providers without rendering.

## Compositing patterns — pick the right one

The cutout WebM is a **re-encoded copy** of the source MP4's RGB. What sits behind it matters.

| Pattern                                                  | Behind the cutout                       | Result                                                                                                          |
| -------------------------------------------------------- | --------------------------------------- | --------------------------------------------------------------------------------------------------------------- |
| **Cutout over a different scene** (most common)          | Static image, gradient, unrelated video | Looks great. Single RGB source for the subject.                                                                 |
| **Cutout over its own source mp4** (text-behind-subject) | Same mp4 the cutout came from           | At `balanced` doubling is barely visible; at `fast` you'll see color shift / edge halo. Use `best` for masters. |
| **Cutout over a different take of the same person**      | Footage of the same subject             | **Two overlapping people. Don't do this.**                                                                      |

## Text-behind-subject pattern (two non-obvious rules)

Putting a headline behind a presenter cutout:

```html
<video
  src="presenter.mp4"
  id="bg"
  data-start="0"
  data-duration="6"
  data-track-index="0"
  muted
  playsinline
></video>

<h1 id="headline" style="z-index:2; ...">MAKE IT IN HYPERFRAMES</h1>

<div class="cutout-wrap" style="position:absolute; inset:0; z-index:3; opacity:0">
  <video
    src="presenter.webm"
    data-start="0"
    data-duration="6"
    data-track-index="1"
    muted
    playsinline
  ></video>
</div>
```

```js
// Flip the wrapper's opacity at the cut, NOT the video's
tl.set(".cutout-wrap", { opacity: 1 }, 3.3);
```

Two rules that are easy to miss:

1. **Wrap the cutout `<video>` in a non-timed `<div>` and animate the wrapper's opacity, not the video element's.** The framework forces `opacity: 1` on active clips (any element with `data-start` / `data-duration`), so animating the video's opacity directly is silently overridden. The wrapper has no `data-*` attributes, so it's owned by your CSS / GSAP.
2. **Both videos use `data-start="0"` and `data-media-start="0"`** so the framework decodes them in sync from t=0. Late-mounting the cutout (`data-start=3.3`) introduces a seek + warm-up that lands a frame off the base mp4 — visible as one frame of misalignment at the cut.

## Layer separation (`--background-output`)

Emits a **second** transparent video alongside the cutout: same source RGB, alpha is `255 - mask` instead of `mask`. The cutout has the subject opaque; the plate has the surroundings opaque (with a transparent hole where the subject was). Use it when text / graphics need to live **between** the two layers.

| File                             | Alpha is…                                               | Use it for                                                       |
| -------------------------------- | ------------------------------------------------------- | ---------------------------------------------------------------- |
| `-o subject.webm`                | mask — subject opaque, background transparent           | Foreground layer (top)                                           |
| `--background-output plate.webm` | inverse mask — surroundings opaque, subject transparent | Bottom layer; place text / graphics between this and the subject |

Both share the same `--quality` and run from a single inference pass — only encode cost roughly doubles. Only valid for video inputs with `.webm` / `.mov` outputs.

**Hole-cut, not inpainted.** The subject region in `plate.webm` is fully transparent — composite something opaque under it to fill the hole.

**Single test for whether `--background-output` is the right tool:** _will anything ever be visible through the subject's silhouette where the subject used to be?_ If no, you don't need the plate — `subject.webm` alone over a different background is enough.

### Use case → right tool

| Use case                                                                            | Right tool                                                                         |
| ----------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------- |
| Text/graphics between the cutout and the plate (this command's reason for existing) | **Hole-cut** (`--background-output`)                                               |
| Subject onto an unrelated scene                                                     | Just `subject.webm`; ignore the plate                                              |
| Show the room _without_ the person, alone over no other content                     | **Clean plate** — needs an inpainter (LaMa, ProPainter, E2FGVI). Not this command. |
| Replace the subject with a different subject                                        | **Clean plate** — same as above                                                    |

### Canonical 3-layer template (plate + content + cutout)

Ship just the two transparent layers and let arbitrary content live between them — no original mp4 needed:

```html
<!-- z=1 plate: surroundings opaque, subject silhouette transparent -->
<video
  src="plate.webm"
  data-start="0"
  data-duration="6"
  data-track-index="0"
  muted
  playsinline
></video>

<!-- z=2 your content lives between the layers -->
<h1 id="headline" style="z-index:2; ...">MAKE IT IN HYPERFRAMES</h1>

<!-- z=3 cutout floats the subject back on top -->
<div class="cutout-wrap" style="position:absolute; inset:0; z-index:3">
  <video
    src="subject.webm"
    data-start="0"
    data-duration="6"
    data-track-index="1"
    muted
    playsinline
  ></video>
</div>
```

Functionally equivalent to the text-behind-subject pattern above, but doesn't require shipping the original mp4 — the plate replaces it. Use this when delivering just the two transparent layers as a reusable asset.

## When `remove-background` is NOT the right tool

If a user asks for "the room **without** the person, displayed standalone" (no subject anywhere, no compositing on top), `--background-output` is wrong — its plate has a transparent hole, not a filled-in clean plate. They need an **inpainter**: LaMa, ProPainter, or E2FGVI. Tell them this command can't do it.


<!-- ===== FILE: hyperframes/media-use/audio/references/requirements.md ===== -->

# Requirements & Caches

## Credential & key priority

Run `npx hyperframes auth status` to see what's configured and which engines a workflow will use (see the skill's **Preflight** section). Keys resolve in this order — **first match wins**:

| Provider                             | Resolution order (first non-empty wins)                                                                                                                                    | Local deps when used                             |
| ------------------------------------ | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------ |
| **HeyGen** (TTS + BGM/SFX retrieval) | `$HEYGEN_API_KEY` → `$HYPERFRAMES_API_KEY` → `~/.heygen/credentials` (shared with heygen-cli; `$HEYGEN_CONFIG_DIR` overrides the dir; written by `hyperframes auth login`) | none (REST)                                      |
| **ElevenLabs** (TTS fallback)        | `$ELEVENLABS_API_KEY`                                                                                                                                                      | `pip install elevenlabs`                         |
| **Lyria** (BGM fallback)             | `$GEMINI_API_KEY` → `$GOOGLE_API_KEY`                                                                                                                                      | `pip install google-genai`                       |
| **Kokoro** (TTS, no key)             | always — final voice fallback                                                                                                                                              | `pip install kokoro-onnx soundfile`              |
| **MusicGen** (BGM, no key)           | always — final music fallback                                                                                                                                              | `pip install transformers torch soundfile numpy` |

`hyperframes auth login` (browser OAuth) is the recommended setup: one sign-in, every project, no per-repo `.env`. An OAuth login is sent as `Authorization: Bearer`; an API key as `X-Api-Key`; both are tagged with `X-HeyGen-Source: cli`. OAuth CLI users can consume the web-plan free allowance for HeyGen TTS (10 min/month); API keys follow the normal API billing path. With no HeyGen credential, voice/BGM run fully locally (Kokoro / MusicGen) — `hyperframes auth status` and `hyperframes doctor` both report whether those local deps are installed.

## Model caches & system dependencies

Each command downloads its own model on first run and caches it under `~/.cache/hyperframes/`:

- **TTS (HeyGen)** — no local deps; needs a HeyGen credential + `ffmpeg` on PATH (to transcode the mp3 response to `.wav`). Credential resolves like the CLI: `$HEYGEN_API_KEY` → `$HYPERFRAMES_API_KEY` → `~/.heygen/credentials` (shared with heygen-cli; run `npx hyperframes auth login`). An OAuth login is sent as `Authorization: Bearer`; an API key as `X-Api-Key`; both include `X-HeyGen-Source: cli` so the backend can apply CLI OAuth free usage.
- **TTS (ElevenLabs)** — same as HeyGen: API key + `ffmpeg`.
- **TTS (Kokoro)** — Kokoro-82M (~311 MB) + voices (~27 MB) in `tts/`. Requires Python 3.8+ with `kokoro-onnx` and `soundfile` (`pip install kokoro-onnx soundfile`). Non-English text also needs `espeak-ng` system-wide.
- **BGM (Lyria)** — needs `$GEMINI_API_KEY` or `$GOOGLE_API_KEY` + `pip install google-genai`. No local model cache.
- **BGM (MusicGen)** — `pip install transformers torch soundfile`. `facebook/musicgen-small` (~300 MB) cached under `~/.cache/huggingface/` on first run.
- **Transcribe** — Whisper model size depending on choice (75 MB – 3.1 GB) in `whisper/`, downloaded from HuggingFace on first use. `whisper.cpp` itself is NOT bundled: the CLI resolves it from PATH, installs via Homebrew (macOS), or builds it from source with git+cmake on first use (`$HYPERFRAMES_WHISPER_PATH` overrides).
- **Remove-background** — `u2net_human_seg` (~168 MB ONNX) in `background-removal/models/`. Peak inference RAM ~1.5 GB.

Run `npx hyperframes doctor` if a command fails because of a missing dependency.


<!-- ===== FILE: hyperframes/media-use/audio/references/sfx.md ===== -->

# Sound effects (SFX)

Named sound effects, produced by the shared audio engine (`scripts/audio.mjs` → `scripts/lib/sfx.mjs`). **Provider-gated** by the engine's one switch — whether a HeyGen credential is present, decided once (not per cue):

- **HeyGen credential present → retrieve every cue** from HeyGen's audio library (`/v3/audio/sounds`, `type=sound_effects`, `min_score=0.4`). Search-and-download, **not** generation. The bundled library is NOT consulted.
- **No credential → the bundled 21-file library** (`assets/sfx/` + `manifest.json`): match each cue name, copy the matched file into the project. Offline, deterministic, free.

There is no `npx hyperframes sfx` command. SFX is never generated — it is retrieved (online) or taken from the bundled library (offline).

## Cues — request → meta

Each line names the effects it wants: `lines[].sfx: ["whoosh", "ui click"]`. The engine flattens these into cues, resolves them per the switch, dedupes identical `(id, name)` pairs (the same effect named twice downloads/copies once), and writes `audio_meta.sfx[]`:

```jsonc
{
  "id": "3",                       // joins the cue to the caller's model (frame / scene / segment)
  "name": "whoosh",
  "file": "assets/sfx/whoosh.mp3", // downloaded or copied, relative to project root
  "source": "heygen" | "local",    // which route resolved it
  "offset_s": 0,                   // delay from the line's start
  "duration_s": 0.57,
  "volume": 0.35                   // SFX sit UNDER voice + BGM
}
```

A cue that matches nothing is **skipped** (recorded as an anomaly); SFX never blocks a render. Neither route replaces a file of yours already at the output name: the cue gets the next free name (`whoosh-2.mp3`), reported as an anomaly, and `file` carries the real path.

## HeyGen retrieval (credentialed)

`searchSounds(name, "sound_effects", { limit: 3, minScore: 0.4 })` → top hit → `assets/sfx/<slug>.mp3`. Results are ranked by `score` (each carries a presigned `audio_url`, `duration`, `description`). The floor is **0.4** because good SFX hits score ~0.5–0.67 — below the API's default `0.7`, which would silently drop most named cues (only whoosh/swoosh-family clears 0.7). `duration_s` comes from the result (else 1.0). Name effects concretely (`glass shatter`, not `dramatic sound`); a vague query returns a poor match.

## Bundled library (no credential)

21 curated files in `assets/sfx/`, indexed by `manifest.json` — `{ file, duration, description }` per key (e.g. `whoosh`, `pop`, `click`, `chime`, `riser`, `impact-bass-1`, `glitch-1`, `typing`, …). A cue name resolves by **manifest key, file basename, or slug**, so `whoosh`, `whoosh.mp3`, or `"ui click"` (→ slug) all match. Matched files are copied into the project's `assets/sfx/`; `duration_s` comes from the manifest, so timing is known **offline** — e.g. `riser` is 10.03s, so trigger it at `climax − 10.03s`. The manifest's `description` field carries placement hints per effect; read `assets/sfx/manifest.json` for the full set and usage.

## Rules

- **Volume ~0.35.** SFX must sit under narration and BGM, not fight them.
- **No match → skip, don't fail.** A missing effect logs an anomaly and moves on; never a render blocker.
- **Retrieval (credentialed) or bundled library (offline) — never generation.** You search HeyGen by text, or match a name against the 21-file manifest.
- **One asset per distinct name.** Reuse across lines is deduped to a single download/copy, many cues.
- **The switch is global, not per cue.** With a credential, retrieval handles even the long tail (effects not in the 21); without one, only the 21 bundled names resolve.


<!-- ===== FILE: hyperframes/media-use/audio/references/transcribe.md ===== -->

# Transcription

Create normalized word-level timestamps. **Always specify `--model` explicitly** — the CLI default is `small.en`, which silently translates non-English audio into English.

```bash
npx hyperframes transcribe audio.mp3  --model small.en             # known English
npx hyperframes transcribe video.mp4  --model small --language es  # known Spanish
npx hyperframes transcribe audio.mp3  --model small                # unknown language (auto-detect)
npx hyperframes transcribe subtitles.srt                           # import existing
npx hyperframes transcribe subtitles.vtt
npx hyperframes transcribe openai-response.json
```

## Language Rule (Non-Negotiable)

`.en` models (`tiny.en` / `base.en` / `small.en` / `medium.en`) **translate** non-English audio into English. This silently destroys the original language.

1. **Known English** → `--model small.en` (or `medium.en` for music / noisy audio)
2. **Known non-English** → `--model small --language <iso-code>` (no `.en` suffix)
3. **Unknown language** → `--model small` (whisper auto-detects)

**CLI default is `small.en`** — do not rely on it; always pass `--model` to make the choice explicit. `--language` also filters out non-target-language segments from mixed-language audio.

## Model Sizes

| Model      | Size   | Speed    | When                                  |
| ---------- | ------ | -------- | ------------------------------------- |
| `tiny`     | 75 MB  | Fastest  | Quick previews, smoke tests           |
| `base`     | 142 MB | Fast     | Short clips, clear audio              |
| `small`    | 466 MB | Moderate | Default for most multilingual content |
| `medium`   | 1.5 GB | Slow     | Music with vocals, noisy audio        |
| `large-v3` | 3.1 GB | Slowest  | Production quality                    |

### Picking a model by content type

1. Speech over silence / light background → `small.en`
2. Speech over music, or music with vocals → start with `medium.en`
3. Produced music track (vocals + full instrumentation) → start with `medium.en`; expect to need manual lyrics or an external API ([`captions/transcript-handling.md`](captions/transcript-handling.md) → "Using External Transcription APIs")
4. Multilingual → `medium` or `large-v3` (no `.en` suffix), pair with `--language`

## Output Shape

Compositions consume a flat array of word objects. The `id` (`w0`, `w1`, …) is added during normalization for stable references in caption overrides; optional for backwards compatibility.

```json
[
  { "id": "w0", "text": "Hello", "start": 0.0, "end": 0.5 },
  { "id": "w1", "text": "world.", "start": 0.6, "end": 1.2 }
]
```

For mandatory caption-quality checks, retry rules, and the OpenAI/Groq Whisper API import path, see `captions/transcript-handling.md`.


<!-- ===== FILE: hyperframes/media-use/audio/references/tts-to-captions.md ===== -->

# TTS → Captions

When no recorded voiceover exists, generate one and obtain word-level caption timing. Two paths depending on which TTS provider is in use:

## Path A — HeyGen (single call, no Whisper)

HeyGen returns word timestamps in the same response as the audio. Use the
bundled REST helper (the `hyperframes tts` command is Kokoro-only):

```bash
node skills/media-use/audio/scripts/heygen-tts.mjs \
  script.txt --output narration.wav --words narration.words.json
```

`narration.words.json` is already in the `[{ id, text, start, end }]` shape the captions pipeline consumes — no separate transcribe pass.

## Path B — Gemini / ElevenLabs / Kokoro (TTS → transcription)

These adapters supply audio without word data. The shared audio engine runs
transcription automatically when timings are absent. For Gemini, use the
request in [Text to speech](tts.md#gemini-narration), then consume
`audio_meta.json` → `voices[].words`.

For a standalone local Kokoro generation, generate the audio, then transcribe:

```bash
npx hyperframes tts script.txt --voice af_heart --output narration.wav
npx hyperframes transcribe narration.wav --model small.en   # voice af_heart is American English
```

Whisper extracts precise word boundaries from the generated audio, so caption timing matches delivery without hand-tuning. Match `--model` to the voice's language (use `small.en` for `a`/`b` prefixes, `small --language <code>` otherwise). Then consume `transcript.json` via the caption references in `captions/`.

For Gemini, verify that transcription preserved the script, especially names,
numbers, and delivery pauses. If `words` is empty, resolve the transcription
failure before captioning. Generate and align again after changing the read.


<!-- ===== FILE: hyperframes/media-use/audio/references/tts.md ===== -->

# Text To Speech

`npx hyperframes tts` synthesizes locally with Kokoro. It does not accept a
`--provider` or `--words` flag. For HeyGen audio plus word timestamps, use the
bundled `heygen-tts.mjs` script below.

> **Run the Preflight first — no credential is not a green light to silently use the local voice.** Before generating a voiceover, complete the sign-in **Preflight** (see `../../GUIDE.md` → Preflight): run `npx hyperframes auth status`, recommend signing in, and **STOP for the user's choice** (sign in for HeyGen voices, or continue offline with local Kokoro). This applies to a one-off "generate a voiceover" request just as much as inside a full workflow.

## Narrating a HyperFrames docs video

Anything that will sit on hyperframes.heygen.com uses one narrator, so the site
does not sound like two products.

|                |                                                |
| -------------- | ---------------------------------------------- |
| Voice          | **River** — "Relaxed, Neutral, Informative"    |
| Provider       | ElevenLabs                                     |
| `voice_id`     | `SAz9YHcvj6GT2YYXdXww`                         |
| Model          | `eleven_multilingual_v2`                       |
| Pace           | 145–155 words per minute, with room to breathe |
| Music under it | about −31 LUFS, never masking the voice        |

```bash
curl -s -X POST "https://api.elevenlabs.io/v1/text-to-speech/SAz9YHcvj6GT2YYXdXww" \
  -H "xi-api-key: $ELEVENLABS_API_KEY" -H "Content-Type: application/json" \
  -d '{"text":"...","model_id":"eleven_multilingual_v2"}' -o take.mp3
```

This is the voice every user-journey film on the docs site already uses. Falling
back to local Kokoro because a key was not to hand produces a film that sounds
wrong beside the others — three docs videos were built that way and had to be
re-voiced. If you cannot reach ElevenLabs, say so and stop rather than
substituting a different voice.

Use another voice only for a documented reason, and write the reason down.

## Available routes

Gemini is an explicit alternative to the automatic provider order below. A
request to use Gemini already chooses the provider; do not redirect that user
to HeyGen sign-in. Read the Gemini section for its credential requirement.

| Order | Provider          | Env trigger                                                          | Voice IDs                                                                                  | Word timestamps                           | Audio format         |
| ----- | ----------------- | -------------------------------------------------------------------- | ------------------------------------------------------------------------------------------ | ----------------------------------------- | -------------------- |
| 1     | HeyGen (Starfish) | `$HEYGEN_ACCESS_TOKEN` / `$HEYGEN_API_KEY` / `~/.heygen/credentials` | UUIDs from `GET /v3/voices?engine=starfish`, or your cloned voice ids (`heygen-voice.mjs`) | **Yes** (`word_timestamps[]` in response) | mp3 → wav via ffmpeg |
| 2     | ElevenLabs        | `$ELEVENLABS_API_KEY`                                                | UUIDs from elevenlabs.io dashboard                                                         | No                                        | mp3 → wav via ffmpeg |
| 3     | Kokoro-82M        | always (local fallback)                                              | `am_michael`, `af_heart`, … (54 voices)                                                    | No                                        | wav direct           |

```bash
# Local Kokoro CLI
npx hyperframes tts "Welcome to HyperFrames" -o narration.wav
```

## Self-contained HeyGen (no CLI) — `scripts/heygen-tts.mjs`

The published `hyperframes tts` CLI synthesizes locally with Kokoro only. When you
want HeyGen specifically — best quality **plus** word timestamps in one call — use
the skill's bundled script, which calls the HeyGen v3 REST API directly and needs
no CLI provider plumbing:

The script resolves a HeyGen credential the same way the CLI does — first source
wins: a host-injected OAuth `$HEYGEN_ACCESS_TOKEN` → `$HEYGEN_API_KEY` →
`$HYPERFRAMES_API_KEY` → a project `.env` (auto-loaded,
walks up ≤5 dirs) → `~/.heygen/credentials` (shared with heygen-cli;
`$HEYGEN_CONFIG_DIR` overrides the dir). An OAuth login is sent as
`Authorization: Bearer`; an API key as `X-Api-Key`; both include
`X-HeyGen-Source: cli`. OAuth CLI users can consume the web-plan free allowance
(10 min/month) before paid usage; API keys follow normal API billing. If the
only credential is an expired OAuth token it stops with a hint to run
`npx hyperframes auth refresh`.

```bash
# Only needed if you haven't run `npx hyperframes auth login`:
export HEYGEN_API_KEY=...   # or put it in a project .env

# Synthesize + capture word timestamps in one call (skips a Whisper pass)
node skills/media-use/audio/scripts/heygen-tts.mjs \
  "Welcome to HyperFrames." -o narration.wav --words narration.words.json

node skills/media-use/audio/scripts/heygen-tts.mjs ./script.txt -o narration.wav
node skills/media-use/audio/scripts/heygen-tts.mjs --list   # public starfish voices
```

- **Voice:** `--voice <id>` must be a **starfish** voice_id (`--list`, or `GET /v3/voices?engine=starfish`) or one of your cloned voice ids (below). v2-catalog ids are rejected with HTTP 400. Omit `--voice` (English) and it defaults to **Marcia** (`05f19352e8f74b0392a8f411eba40de1`, a fixed default so the choice is deterministic). Non-English with no `--voice` falls back to the first matching catalog voice.
- **Output:** `.wav` → transcoded to 44.1k mono via ffmpeg; `.mp3` → raw bytes (no ffmpeg needed).
- **Words:** `--words <path>` writes the flat `[{id,text,start,end}]` shape below, drop-in for the captions pipeline. HeyGen's `<start>`/`<end>` boundary sentinels are filtered out and ids are re-contiguous.
- **Non-English:** `--lang <code>` (anything but `en`) is sent as the request `language`.

## Cloned voices — `scripts/heygen-voice.mjs`

Clone a voice from an mp3 or wav recording, then pass the printed id to
`heygen-tts.mjs --voice`. Same credential resolution as above. Any API refusal
(clone limit reached, plan upgrade required, voice not found) prints HeyGen's own
message to stderr and exits 1.

```bash
node skills/media-use/audio/scripts/heygen-voice.mjs clone take.mp3 --name "My voice"  # → {"voice_id":"..."}
node skills/media-use/audio/scripts/heygen-voice.mjs list --prefix "My"   # → [{"voice_id","name","created_at"}]
node skills/media-use/audio/scripts/heygen-voice.mjs delete <voice_id>
```

`clone` waits up to 120 s for the clone to finish. `list` reads
`GET /v3/voices?type=private`.

## When to use which provider

| Goal                                                      | Use                                                       |
| --------------------------------------------------------- | --------------------------------------------------------- |
| Best voice quality + word timestamps in one call          | **HeyGen**                                                |
| Drop-in cloud TTS, big voice catalog                      | **ElevenLabs**                                            |
| Offline, no API key, fast iteration                       | **Kokoro**                                                |
| Directed delivery with Gemini prebuilt or custom voices   | **Gemini** (explicit selection; transcription for timing) |
| Non-English multilingual with deterministic phonemization | **Kokoro** (`ef_dora`, `jf_alpha`, `zf_xiaobei`, …)       |

## Gemini narration

Use the shared audio engine, not `hyperframes tts`. Authenticate with either:

- `GEMINI_API_KEY` or `GOOGLE_API_KEY` (first set key wins).
- A service-account JSON file at `GOOGLE_APPLICATION_CREDENTIALS`, or injected
  JSON in `GCS_CREDS`. Install `google-auth requests` in the Python 3 environment
  used by the helper. A configured file takes precedence over injected JSON.

API keys take precedence over service accounts: unset both key variables to use
OAuth. Never put credentials in a request file or composition. The helper
obtains a fresh OAuth token for each generation with the
`generative-language.retriever` scope. The quota project resolves from
`GOOGLE_CLOUD_PROJECT`, then `GCLOUD_PROJECT_ID`, then the service-account JSON.
User ADC files and metadata-server authentication are not supported.

Both routes call the Gemini Developer Interactions API, not Cloud TTS or Vertex
AI. Those APIs have separate model catalogs and access requirements.

Save this as `audio_request.json` in the project:

```json
{
  "provider": "gemini",
  "tts_model": "gemini-3.8-flash-tts",
  "voice": "Kore",
  "lang": "en",
  "style": "Warm, clear, conversational. Leave a short pause between sentences.",
  "lines": [
    { "id": "intro", "text": "Every word has a moment. Let the picture follow the voice." }
  ],
  "bgm": { "mode": "none" }
}
```

```bash
node <SKILL_DIR>/audio/scripts/audio.mjs \
  --request ./audio_request.json --hyperframes . --out ./audio_meta.json --only tts
```

The engine saves `assets/voice/intro.wav` (or `intro-2.wav` when a file of yours already has that name; `voices[].path` says which), measures its duration, and transcribes
it into `voices[].words` in `audio_meta.json`. Check that every requested line
has audio and nonempty word timings before building a captioned video. Review
the timings against the actual audio; transcription is estimated alignment,
not native TTS timestamps. Do not distribute words evenly across a clip.

- **Models:** `gemini-3.8-flash-tts` (default), `gemini-3.8-flash-lite-tts`,
  `gemini-3.1-flash-tts-preview`, `gemini-2.5-pro-preview-tts`, and
  `gemini-2.5-flash-preview-tts`. Use these exact Developer API IDs; Cloud TTS
  aliases such as `gemini-2.5-flash-tts` are not accepted.
- **Voice:** `Kore` by default; pass another prebuilt voice or an existing custom
  voice ID for 3.8. Older models require prebuilt voices. Creating or replicating
  voices is outside this helper.
- **Delivery:** Put directions in `style`, not in spoken `text`. Each line can
  override `style`. 3.8 uses structured annotations; older models receive a
  delivery prompt before the transcript. Check that directions were not spoken.
  Use style for pacing; numeric `speed` must be omitted or 1.
- **Audio:** 3.8 returns a complete WAV. Older models return mono 16-bit PCM,
  which the helper wraps as WAV at the returned sample rate without resampling.
  No generation calls run during playback or rendering.
- **Timing:** This adapter requests no native word timestamps. It uses the
  existing transcription pass. `lang` selects transcription language; Gemini
  infers speech language from the text.
- **Workflow adapters:** Product-launch, faceless-explainer, and PR-video audio
  scripts accept `--provider gemini --voice Kore --tts-model gemini-3.8-flash-tts
--style "Warm and clear"`.

An API error is reported as a failed line; an explicitly chosen Gemini voice
never silently falls back to another provider. Check the engine's anomalies
and output metadata, not only its exit code.

API contract: [Google's speech generation guide](https://ai.google.dev/gemini-api/docs/speech-generation).

## ffmpeg requirement

HeyGen + ElevenLabs return mp3. The bundled HeyGen helper transcodes to wav
when `--output` ends in `.wav` (the default and what downstream `ffprobe` +
Whisper expect). If you'd rather skip the transcode, pass `-o file.mp3`.
Without `ffmpeg` on PATH, wav output from cloud providers fails; the local
Kokoro CLI writes wav directly.

## Voice selection (Kokoro)

Default `af_heart`. Curated picks:

| Content type      | Voice                  |
| ----------------- | ---------------------- |
| Product demo      | `af_heart`, `af_nova`  |
| Tutorial / how-to | `am_adam`, `bf_emma`   |
| Marketing / promo | `af_sky`, `am_michael` |
| Documentation     | `bf_emma`, `bm_george` |
| Casual / social   | `af_heart`, `af_sky`   |

Run `npx hyperframes tts --list` for the bundled set.

## Multilingual (Kokoro voice prefix → language)

The first letter of a Kokoro voice ID picks the phonemizer language; `--lang` overrides auto-detection.

| Prefix | Language             |
| ------ | -------------------- |
| `a`    | American English     |
| `b`    | British English      |
| `e`    | Spanish              |
| `f`    | French               |
| `h`    | Hindi                |
| `i`    | Italian              |
| `j`    | Japanese             |
| `p`    | Brazilian Portuguese |
| `z`    | Mandarin             |

```bash
npx hyperframes tts "La reunión empieza a las nueve" --voice ef_dora
npx hyperframes tts "Today is a nice day" --voice af_heart
```

Valid `--lang` codes (only needed to override the voice's auto-detected language): `en-us`, `en-gb`, `es`, `fr-fr`, `hi`, `it`, `pt-br`, `ja`, `zh`.

Non-English phonemization requires `espeak-ng` system-wide (`brew install espeak-ng` / `apt-get install espeak-ng`).

## Speed

- `0.7-0.8` — tutorial, complex content, accessibility
- `1.0` — natural pace (default)
- `1.1-1.2` — intros, transitions, upbeat content
- `1.5+` — rarely appropriate, test carefully

The `hyperframes tts` command honors `--speed` for Kokoro. Provider-specific
helpers document their own pacing controls.

## Long scripts

Past a few paragraphs, write the text to a `.txt` file and pass the path. Inputs over ~5 minutes of speech may benefit from splitting into segments.

## HeyGen word-timestamp shape

When `--words <path>` is passed to a HeyGen call, the file is written in the same flat shape `transcribe` produces — drop-in compatible with the captions pipeline:

```json
[
  { "id": "w0", "text": "Hi", "start": 0.0, "end": 0.21 },
  { "id": "w1", "text": "there", "start": 0.22, "end": 0.55 }
]
```

For ElevenLabs / Kokoro, run `npx hyperframes transcribe narration.wav --model small.en` to get the same shape.


<!-- ===== FILE: hyperframes/media-use/luts/README.md ===== -->

# LUT library (authoring)

`index.json` is the agent-consumed catalog of color-grade looks. Each entry resolves
on demand — no `.cube` bodies are committed to the repo.

Each look has:

- `id`, `description`, `tags`, `intensity` — matching + application metadata.
- `url` (optional) — a hosted `.cube` downloaded, validated, and frozen at resolve
  time, exactly like bgm/image assets.
- `params` (optional) — a deterministic `buildCube` spec used offline (`--local-only`)
  or as a fallback if the `url` download/validation fails.

An entry needs at least one of `url` or `params`; prefer both (CDN url with a params
fallback) so resolution is never blocked on the network.

## Hosting a new look (operators)

1. Generate the `.cube` (e.g. `resolve -t lut --params '{...}'` or a graded export).
2. Upload it to the public CDN origin bucket:

   ```
   aws s3 cp <id>.cube s3://heygen-public/luts/<id>.cube
   ```

   It is then served at `https://static.heygen.ai/luts/<id>.cube` (CloudFront).

3. Add an entry to `index.json` with that `url` (and ideally a `params` fallback).


<!-- ===== FILE: hyperframes/media-use/references/audio.md ===== -->

# Audio engine — voiceover, music, SFX, captions, transcription

For a full audio pass (TTS voiceover + background music + sound effects in one
shot), use the shared engine at `audio/scripts/audio.mjs`. It takes a neutral
`audio_request.json` and writes `audio_meta.json` plus assets under
`.media/audio/{voice,bgm,sfx}`:

```bash
node <SKILL_DIR>/audio/scripts/audio.mjs --request ./audio_request.json --out ./audio_meta.json
```

- **Request** `{ provider?, voice?, lang?, speed?, tts_model?, style?, lines: [{ id, text, style?, sfx?: [names] }], bgm: { mode?, query?, prompt? } }`: `id` joins each line back to your model; `bgm.mode` = `retrieve | generate | none` (omit for auto). `--only tts,bgm,sfx` runs a subset and merges into an existing `--out`.
- **Gemini narration** is opt-in with `provider: "gemini"` and an API key or service-account credentials. `tts_model` defaults to `gemini-3.8-flash-tts`; 3.8 Flash-Lite, 3.1 Flash Preview, and 2.5 Pro/Flash Preview TTS are also supported. `style` directs delivery; a line's style overrides the request's style. CLI overrides: `--tts-model`, `--style`. See `audio/references/tts.md` for a complete request. The existing automatic provider order is unchanged.
- **Output** `audio_meta.json` (id-keyed): `voices[].{path,duration_s,words[]}` (word timestamps for captions), `sfx[]`, `bgm`, `total_duration_s`.
- **HeyGen free-usage path**: HeyGen CLI auth unlocks TTS plus music/SFX retrieval. Local/provider-specific generators are explicit alternatives where installed; run `npx hyperframes media-use resolve --doctor` before assuming retrieval or TTS will work.
- If BGM took the generate path (`bgm_pending: true`), run `audio/scripts/wait-bgm.mjs` before final render.

Single-shot helpers: `audio/scripts/heygen-tts.mjs` (one voice file). Transcription / background removal / captions use the `hyperframes` CLI (`transcribe`, `remove-background`), see the per-topic guides in `audio/references/` (`tts.md`, `bgm.md`, `sfx.md`, `transcribe.md`, `remove-background.md`, `captions/`).

Transcription defaults to Parakeet (better than whisper.cpp: 6.05% vs 7.44% WER, 5-10x faster) via `scripts/transcribe.mjs`, with whisper.cpp auto-fallback (see `references/operations.md`).


<!-- ===== FILE: hyperframes/media-use/references/grading.md ===== -->

# Color grading — grade blocks and LUTs

Use `grade` when you need a canonical HyperFrames grading/effects payload for
an `<img>` or `<video>`. Core presets and params-backed LUT entries resolve
locally; future CDN-backed LUT entries require network unless already
frozen. Persist a decided payload with the CLI rather than editing HTML by
hand:

For a vague but explicit polish request, do not jump directly from intent to a
preset name. Read `media-treatments.md`, choose a treatment whose subject and
avoid rules match the actual media, apply its conservative base with only
justified bounded tuning, then complete its visual verification steps. A named
owned treatment uses the exact preset/payload in its recipe; do not run the
generic grade/LUT resolver first.

Stop here and use that treatment workflow for requests such as retro, old home
video, camcorder, film, print, ASCII, glitch, privacy, or a media reveal. Do not
assemble those from a generic LUT plus handmade CSS vignette/grain/opacity.

**Never `cat`/read a `.cube` file into context.** A 3D LUT is ~size^3 lines of raw numbers (33^3 ≈ 36k lines at the default size). It bloats context and carries zero human/agent-legible signal. To understand or choose a LUT, use `hyperframes grade-compare` to see it rendered. `npx hyperframes media-use resolve --type lut --intent "<look description>" --project .` validates generated or downloaded LUTs before freezing them; the validator is bundled in the CLI, not shipped as a standalone skill script. Read `<project>/.media/index.md` or `luts/index.json` for the description. Never read the LUT body itself.

```bash
npx hyperframes media-use resolve --type grade --intent "warm daylight" --project . --json
```

Preset-first output uses the core runtime vocabulary and does not freeze a file:

```json
{
  "preset": "warm-daylight",
  "intensity": 1
}
```

Apply that payload to one unambiguous real media element:

```bash
hyperframes media-treatment --project . --file index.html \
  --selector '#hero' \
  --grading '{"preset":"warm-daylight","intensity":1}' --apply --json
```

Use `--dry-run` before writing when scope is uncertain and `--clear` to remove
the treatment. The low-level persisted result is still normal HTML:

```html
<video
  class="clip"
  src="./media/scene.mp4"
  data-color-grading='{"preset":"warm-daylight","intensity":1}'
></video>
```

Direct attribute authoring is a fallback for environments where the CLI is not
available, not the primary agent workflow.

To build a treatment that is not already represented by a recipe, inspect the
canonical toolbox first:

```bash
hyperframes media-treatment --capabilities --json
```

It reports a concise family map. Read `--capability grading` for the processing
order, then request only the focused family needed to get its legal controls
and ranges from Core. Compose one nested payload and pass it back through
`hyperframes media-treatment`; the command rejects unknown keys before
mutation. Do not generate or hand-edit a LUT merely to combine controls already
owned by the realtime shader.

For seek-safe effect motion, animate only the runtime-supported CSS properties
on that same real media element with its registered paused GSAP timeline:

| CSS property                       | Range   |
| ---------------------------------- | ------- |
| `--hf-color-grading-intensity`     | 0 to 1  |
| `--hf-color-grading-lut-intensity` | 0 to 1  |
| `--hf-color-grading-exposure`      | -2 to 2 |
| `--hf-color-grading-blur`          | 0 to 1  |
| `--hf-color-grading-bloom`         | 0 to 3  |
| `--hf-color-grading-kuwahara`      | 0 to 1  |
| `--hf-color-grading-pixelate`      | 0 to 1  |
| `--hf-color-grading-ascii`         | 0 to 1  |
| `--hf-color-grading-dither`        | 0 to 1  |

Once set (inline, in a stylesheet or on a parent), a property overrides the
payload's value for that control, so set it only on media you animate: put the
tween's first value in the element's inline `style`, then use finite `tl.to()`
keyframes. Leave it unset for a static grade. Do not use a frame-zero `tl.set()`, CSS
animation clocks, timers, random values, or `onUpdate` callbacks. The static
`data-color-grading` payload remains the fallback and source of the other
controls.

For a reusable color transform beyond the preset vocabulary, freeze a validated
`.cube` under `.media/luts/` and return a block that references it:

```bash
npx hyperframes media-use resolve --type grade --intent "teal orange blockbuster" --project . --json
```

```json
{
  "intensity": 1,
  "lut": { "src": ".media/luts/grade_001.cube", "intensity": 0.85 }
}
```

Use `lut` when you only need the reusable `.cube` file:

```bash
npx hyperframes media-use resolve --type lut --intent "teal orange blockbuster" --project .
```

For a describable technical look, author an explicit parametric LUT with `--params`:

```bash
npx hyperframes media-use resolve --type lut --params '{"contrast":0.2,"temperature":-0.3}' --project .
npx hyperframes media-use resolve --type grade --params '{"exposure":0.2}' --project . --json
```

For a LUT generated by your own script, ingest it with `--from`; media-use validates it before registration and rejects invalid or oversized cubes:

```bash
npx hyperframes media-use resolve --type lut --from custom.cube --project .
```

Parametric math (`buildCube`) cannot reproduce real film stocks or emulsion
transforms. Use a CDN-backed scanned `.cube` entry or ingest a real scanned
`.cube` for those.

For visual selection, list reusable LUT candidates with
`resolve --type grade --candidates`, write the promising entries to a
`grades.json`, run
`hyperframes grade-compare --for <frame> --grades grades.json`, then commit the
winner with `resolve -t grade` as the final `data-color-grading` block.

For media already selected in a composition, use `media-treatment --analyze`
when you need side-effect-free `ffmpeg`/`ffprobe` signalstats evidence. It
returns source metadata, HDR/unknown-LOG warnings, and a bounded `adjust`
suggestion without modifying the composition. The suggestion is a starting
point for visual review, not an automatic neutralization of intentional color.

```bash
hyperframes media-treatment --project . --file index.html \
  --selector '#hero' --analyze --json
```

For an unbound source file, `resolve --type grade --for ... --analyze` remains
available. Without `--analyze`, that resolver records a grade candidate in
`.media`; use that form only when you intend to keep the candidate.

Library LUT entries live in `luts/index.json`. Each entry keeps `id`,
`description`, `tags`, and `intensity`, then supplies either compact `params`
for on-demand `buildCube(params)` generation or a direct CDN `url` for future
scanned `.cube` files. Do not commit generated `.cube` bodies; resolve
validates generated or downloaded cubes as it freezes them under
`.media/luts/`.

```bash
npx hyperframes media-use resolve --type lut --intent "teal orange blockbuster" --project . --json
```
