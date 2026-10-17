

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


<!-- ===== FILE: hyperframes/media-use/references/media-treatment-recipes.md ===== -->

# Media treatment recipes

These are optional tested seeds, not the complete capability surface. Read the
shared policy and choose one relevant section through `media-treatments.md`.
Agents may modify or combine a seed with compatible canonical controls after
inspecting the media, or assemble a bespoke payload from
`hyperframes media-treatment --capabilities --json` when no seed fits.

## Natural Portrait

Use for a talking head, interview, presenter, or people-focused photo whose
intended result is natural, polished, and restrained.

Do not use when the face is incidental or tiny, the source is intentionally
neon/monochrome/strongly stylized, or the requested result is beauty retouching.
This treatment changes the whole frame; it is not a face mask or skin-smoothing
effect.

Inspect face exposure, highlight retention, shadow detail, white balance, and
whether the existing look is intentional. Signalstats do not detect faces or
creative intent.

### Base payload

Start here, then tune only when the sampled frames justify it:

```json
{ "preset": "skin-soft", "intensity": 0.6 }
```

`skin-soft` is a global tonal/color preset whose vibrance math is reduced for
skin-like colors. It does not blur, retouch, segment, or track a face.

### Bounded tuning

Adjustment values are absolute values in the final payload, not deltas added to
the preset. Keep changes inside these conservative ranges unless the user asks
for a stylized result:

| Property    | Natural Portrait range |
| ----------- | ---------------------- |
| intensity   | 0.45 to 0.75           |
| exposure    | -0.06 to 0.14          |
| contrast    | -0.05 to 0.08          |
| highlights  | -0.18 to -0.04         |
| shadows     | 0.04 to 0.18           |
| whites      | -0.10 to 0.04          |
| blacks      | -0.06 to 0.06          |
| temperature | -0.05 to 0.10          |
| tint        | -0.03 to 0.05          |
| vibrance    | 0 to 0.06              |
| saturation  | -0.04 to 0.06          |

Leave grain, blur, and pixelate at zero. A vignette is optional at `0` to
`0.05` only when it improves subject focus without looking like an effect.

Manual controls must stay inside their schema section; they are never
top-level keys. A tuned Natural Portrait payload looks like this:

```json
{
  "preset": "skin-soft",
  "intensity": 0.58,
  "adjust": {
    "highlights": -0.08,
    "shadows": 0.08,
    "temperature": 0.02,
    "vibrance": 0.02
  },
  "details": { "vignette": 0.03 }
}
```

Use the same nested shape in `grade-compare` candidate files. `adjust` owns
tonal/color controls, `details` owns vignette/grain, and `effects` owns blur,
pixelate, chroma bleed, and the advanced treatment primitives below.

During the common comparison, reject any result that makes skin implausible,
loses highlight detail, flattens or desaturates dark skin, or casts clothing and
background colors accidentally.

## Product Polish

Use for photographed or filmed physical products when the goal is clean,
accurate, dimensional presentation. Protect product color, material texture,
label readability, specular highlights, and intentional lighting.

Do not use this treatment for literal app/site screenshots or screen captures;
follow UI Fidelity below. Do not neutralize a lifestyle scene's deliberate
ambient color, and do not infer exact brand-color correction without a neutral
reference or known product color.

Inspect the product separately from its background. Check white balance, label
legibility, surface texture, highlight clipping, shadow detail, white point,
and black point. Statistics cannot identify a white package, metallic
highlight, amber glass, or intentional warm light.

### Base payload

Compare this restrained correction against the untouched source:

```json
{
  "intensity": 0.7,
  "adjust": {
    "exposure": 0.01,
    "contrast": 0.06,
    "highlights": -0.1,
    "shadows": 0.04,
    "whites": 0.02,
    "blacks": -0.03,
    "vibrance": 0.03,
    "saturation": 0.02
  }
}
```

This is a comparison starting point, not an instruction to change an already
finished source. If the original has accurate color, clean endpoints, and good
texture, leave the pixels unchanged and polish through framing or motion.

### Bounded tuning

| Property    | Product Polish range |
| ----------- | -------------------- |
| intensity   | 0.45 to 0.8          |
| exposure    | -0.08 to 0.1         |
| contrast    | 0 to 0.1             |
| highlights  | -0.16 to 0           |
| shadows     | 0 to 0.12            |
| whites      | -0.08 to 0.05        |
| blacks      | -0.06 to 0.04        |
| temperature | -0.05 to 0.05        |
| tint        | -0.03 to 0.03        |
| vibrance    | 0 to 0.06            |
| saturation  | -0.04 to 0.05        |

Temperature and tint stay at zero unless the frames show a plausible cast.
Leave grain, vignette, blur, and pixelate at zero for catalog/e-commerce media.
For a lifestyle product shot, a vignette up to `0.04` is acceptable only when
it improves focus without changing the product itself.

During the common comparison, reject any result that clips white packaging,
muddies black products, shifts a known brand color, hides texture, or makes
labels harder to read. Report when preserving the original was the deliberate
decision.

## UI Fidelity

Use for literal app, website, dashboard, terminal, slide, or screen-recording
pixels whose colors and readability are part of the product being shown.

The default payload is **none**: do not add `data-color-grading`. Global color
changes affect brand colors, status colors, charts, screenshots, and tiny text
together, so even a tasteful photographic look can make the demonstration less
truthful.

Polish UI footage with crop, scale, pacing, cursor emphasis, surrounding DOM
overlays, or seek-safe motion outside the captured pixels. If the user
explicitly asks for a stylized UI look, preview it against the original and
state that exact UI color is no longer preserved. If a camera filmed a screen,
correct only a demonstrated capture cast or exposure issue and still verify
text and brand colors across representative frames.

## Film Memory

Use when the story explicitly calls for a warm memory, restrained flashback,
personal archive, or film-like recollection. This is not the default meaning of
"cinematic", and it is not scanned-film-stock emulation.

Do not use for literal UI, product catalog media, technical demonstrations, or
footage whose accurate current-day color is important. Use a separate camcorder
treatment for VHS/REC language. Do not add dust, scratches, light leaks, film
burns, or halation unless an owned component is available and the requested
story actually benefits from it.

Check that the source has enough highlight and shadow detail to tolerate a
faded treatment, and confirm nostalgia or temporal separation belongs in the
story. Compare the full moving treatment, not only a still preset card.

### Static pixel base

Start with this owned shader recipe:

```json
{
  "preset": "vintage-wash",
  "intensity": 0.6,
  "details": {
    "vignette": 0.12,
    "grain": 0.12,
    "grainSize": 0.2,
    "grainRoughness": 0.6
  }
}
```

Keep the static values inside these ranges:

| Property       | Film Memory range |
| -------------- | ----------------- |
| intensity      | 0.5 to 0.75       |
| vignette       | 0.08 to 0.16      |
| grain          | 0.08 to 0.16      |
| grainSize      | 0.16 to 0.24      |
| grainRoughness | 0.5 to 0.7        |

The stronger end can flatten dark skin, black clothing, or already-faded
footage. Compare against the source and lower strength when it does.

### Temporal character

Use the existing registered paused GSAP timeline on the same media element:

- author `--hf-color-grading-exposure: 0` in the media element's inline
  `style`;
- move it through a finite irregular sequence within `-0.03` to `0.03`, using
  gentle `sine.inOut` segments around `0.45` to `0.8` seconds;
- for gate weave, keep `x`/`y` within `0.15%` of the shorter composition edge,
  rotation within `0.03` degrees, and scale between `1.005` and `1.01` to
  protect the frame edges;
- return close to the starting exposure and transform at the treatment end.

Do not use randomness, infinite CSS keyframes, timers, or `onUpdate`. Flicker
is a gentle exposure pulse, not a flash. Weave is slight mechanical drift, not
handheld shake.

Also run focused keyframe diagnostics and seek directly to the final-minus-frame
position. Reject brightness pumping, distracting drift, clipped edges, or
skin/detail loss. Report the motion ranges and describe this as an HF
film-memory treatment, not camera-stock emulation. If motion reads as an effect
before it reads as a memory, reduce or remove it.

## Creator Camcorder

Use when the story explicitly calls for a creator-camera recording, consumer
camcorder memory, or restrained digital-video character. This treatment is a
modern camcorder language, not VHS restoration, CRT simulation, surveillance,
or a promise to reproduce a specific camera model.

Do not apply it to literal UI, product catalog media, tiny media tiles, or
already compressed footage that has distracting color bleed. Do not add a REC
HUD merely because the source contains a person talking; the camera-device
language must support the story or the user's requested style.

Check skin, saturated edges, fine text, source compression, and whether the
source already has a deliberate camera look. Reject softened chroma that
damages labels, graphics, or identifying product color. Judge chroma softness
and grain in motion, not one still.

### Static pixel base

Start with the proven shader payload below, then tune only inside the bounded
ranges when representative frames justify it:

```json
{
  "intensity": 0.72,
  "adjust": {
    "contrast": 0.08,
    "highlights": -0.05,
    "shadows": 0.02,
    "whites": 0.03,
    "blacks": -0.04,
    "temperature": -0.03,
    "tint": -0.015,
    "vibrance": -0.03,
    "saturation": -0.06
  },
  "details": {
    "vignette": 0.06,
    "grain": 0.08,
    "grainSize": 0.18,
    "grainRoughness": 0.58
  },
  "effects": { "chromaBleed": 0.55 }
}
```

| Property       | Creator Camcorder range |
| -------------- | ----------------------- |
| intensity      | 0.55 to 0.8             |
| contrast       | 0.03 to 0.1             |
| highlights     | -0.1 to 0               |
| shadows        | 0 to 0.06               |
| whites         | 0 to 0.05               |
| blacks         | -0.08 to -0.01          |
| temperature    | -0.06 to 0.04           |
| tint           | -0.03 to 0.02           |
| vibrance       | -0.06 to 0.02           |
| saturation     | -0.12 to -0.02          |
| vignette       | 0.03 to 0.1             |
| grain          | 0.04 to 0.12            |
| grainSize      | 0.14 to 0.24            |
| grainRoughness | 0.45 to 0.7             |
| chromaBleed    | 0.35 to 0.7             |

Leave blur and pixelate at zero. Square pixels, scanlines, RGB splitting, and
tracking noise are different visual languages and are not defaults for this
treatment.

### Optional camera HUD

When the narrative benefits from explicit recording-device language, install
the Registry overlay block:

```bash
npx hyperframes add camcorder-hud --no-clipboard
```

Insert the printed `data-composition-src` host over the intended media range.
Edit the displayed date/time/mode/counter in
`compositions/camcorder-hud.html`. The block's paused GSAP timeline derives
its counter and REC blink from composition time, so play, scrub, and render
agree. Keep the HUD finite and scoped to the shot.

The HUD is an optional authored overlay. The pixel payload remains useful
without it, and the HUD alone is not evidence that the footage was treated.

### Optional source-to-camera reveal

Global grading intensity fades only primary correction and LUT output; it does
not fade the independent camcorder effects. For a visible source-to-camera
mode change, use two synchronized media layers and a finite opacity crossfade
from untreated to treated footage. Fade the HUD in on that same paused GSAP
timeline. Do not animate shader state with callbacks or an independent clock.

Also verify HUD placement and framing in each aspect ratio the project supports.
Report whether the HUD was used and describe this as an HF camcorder treatment,
not camera/VHS emulation. If an effect artifact is more noticeable than the
subject, reduce chroma bleed/grain or keep the source unchanged.

## VHS Playback

Use when the story explicitly calls for analog home-video tape, a dated archive,
or a visibly degraded VHS playback. This treatment is not Creator Camcorder,
generic pixelation, CRT display simulation, or a default retro look.

Do not use for literal UI, product catalog media, small text, clean modern
creator footage, or any source whose identifying color/detail must remain exact.
Inspect high-contrast vertical edges, faces, saturated objects, and the bottom
of the frame in motion. Analog damage must support the story without making the
subject hard to read.

### Pixel payload

Start with the complete proven combination, not `tapeDamage` alone:

```json
{
  "intensity": 1,
  "adjust": { "contrast": -0.04, "saturation": -0.08 },
  "details": {
    "grain": 0.16,
    "grainSize": 0.12,
    "grainRoughness": 0.72
  },
  "effects": {
    "tapeDamage": 0.82,
    "tapeTracking": 0.85,
    "tapeNoise": 0.3,
    "tapeSpeed": 0.5,
    "chromaBleed": 0.5,
    "chromaticAberration": 0.18,
    "chromaticAngle": 0,
    "scanlines": 0.35,
    "scanlineCount": 0.17,
    "scanlineSoftness": 1,
    "digitalGlitch": 0.32,
    "digitalGlitchColorSplit": 0,
    "digitalGlitchLineTear": 0.08,
    "digitalGlitchPixelate": 0,
    "digitalGlitchBlockAmount": 0,
    "digitalGlitchBlockDisplacement": 0,
    "digitalGlitchBlockOpacity": 0,
    "digitalGlitchSpeed": 0.5
  }
}
```

| Property              | VHS Playback range |
| --------------------- | ------------------ |
| intensity             | 0.75 to 1          |
| contrast              | -0.1 to 0          |
| saturation            | -0.16 to 0         |
| grain                 | 0.08 to 0.18       |
| grainSize             | 0.08 to 0.18       |
| grainRoughness        | 0.55 to 0.8        |
| tapeDamage            | 0.65 to 0.9        |
| tapeTracking          | 0.5 to 0.9         |
| tapeNoise             | 0.15 to 0.45       |
| tapeSpeed             | 0.35 to 0.65       |
| chromaBleed           | 0.35 to 0.65       |
| chromaticAberration   | 0.08 to 0.22       |
| scanlines             | 0.2 to 0.4         |
| scanlineCount         | 0.14 to 0.2        |
| digitalGlitch         | 0.2 to 0.4         |
| digitalGlitchLineTear | 0.04 to 0.1        |

`tapeDamage` owns deterministic horizontal line jitter, slow time-base wobble,
bottom-edge head switching, luma bandwidth loss, restrained ghosting, noise,
and sparse dropouts. Its subordinate tracking/noise/speed controls add bounded
moving tape tears and control their signal character without introducing a new
clock. `chromaBleed` separately reduces horizontal chroma detail. The restrained
scanline and chromatic settings supply the remaining tape-playback character.
The digital stage is used only for rare horizontal row tears: keep its color
split, pixelation, block displacement, block opacity, and corruption values at
zero. Leave blur, CRT curvature, generic pixelation, and a camera HUD off.

These values are an original HyperFrames recipe calibrated on the same public
Orange Cat source used for the external visual reference. They are not copied
shader code or a claim of pixel-identical output from the external reference. The scanline count is
mapped to the reference's approximately 127-cycle primary line pattern; the HF
tracking math stays bounded in media pixels and uses the composition clock.

The shader damage evolves from the existing deterministic media time, so it
needs no CSS loop or private timeline. Global grading intensity does not fade
tape damage or other independent effects. If the story requires a finite
source-to-tape reveal, crossfade synchronized untreated and treated media layers
on the host's paused GSAP timeline. During the common workflow, inspect dense
consecutive frames and reject hard edge tearing, face
smearing, frozen noise, square blocks, blank borders, or a bottom disturbance
that competes with the subject.

## 8mm Home Movie

Use for personal archive, family-memory, childhood, travel-memory, or explicit
small-gauge home-movie language. This is stronger and more materially film-like
than Film Memory, but it is still an owned HyperFrames treatment rather than a
claim to reproduce a named film stock, camera, or laboratory process.

Do not use for literal UI, technical demonstrations, catalog products, clean
interviews, or footage where dust/scratches would imply false provenance. Check
skin, highlights, dark clothing, and frame edges before applying it.

### Pixel payload

```json
{
  "preset": "vintage-wash",
  "intensity": 0.72,
  "details": {
    "vignette": 0.28,
    "vignetteMidpoint": 0.54,
    "vignetteFeather": 0.72,
    "grain": 0.34,
    "grainSize": 0.18,
    "grainRoughness": 0.72
  },
  "effects": { "filmArtifacts": 0.62 }
}
```

| Property       | 8mm Home Movie range |
| -------------- | -------------------- |
| intensity      | 0.6 to 0.8           |
| vignette       | 0.18 to 0.34         |
| grain          | 0.22 to 0.42         |
| grainSize      | 0.12 to 0.24         |
| grainRoughness | 0.6 to 0.8           |
| filmArtifacts  | 0.35 to 0.7          |

`filmArtifacts` owns only deterministic sparse dust and short scratches. The
existing preset/details own color, vignette, and grain; the host's paused GSAP
timeline owns optional gate weave. Keep weave within `0.15%` of the shorter
composition edge, rotation within `0.03` degrees, and scale between `1.005` and
`1.015`. Use finite `sine.inOut` segments around `0.6` to `1` second, return
near the starting transform, and never use randomness, timers, `onUpdate`, or
an infinite CSS animation.

Reject a result when dust is constantly visible, scratches persist unnaturally,
the frame pumps, weave exposes an edge, highlights turn muddy, or the material
artifacts are more noticeable than the memory. For a subtler nostalgic result,
use Film Memory instead.

## Editorial Halftone

Use for print/editorial transitions, poster frames, comic/newsprint language,
stylized product or portrait beats, and graphic sequences where visible ink
screening is the point. This is a real four-angle CMYK raster treatment, not a
dotted DOM overlay.

Do not use on literal UI, dense text, tiny labels, footage that must remain
photorealistic, or a long talking-head segment unless the user explicitly asks
for strong print stylization. Preserve text/captions as ungraded DOM above the
media whenever they must stay readable.

### Pixel payload

```json
{
  "intensity": 1,
  "adjust": { "contrast": 0.04, "saturation": 0.04 },
  "effects": { "halftone": 0.94, "halftoneSize": 0.36 }
}
```

| Property     | Editorial Halftone range |
| ------------ | ------------------------ |
| intensity    | 0.8 to 1                 |
| contrast     | -0.02 to 0.08            |
| saturation   | -0.04 to 0.08            |
| halftone     | 0.75 to 1                |
| halftoneSize | 0.15 to 0.55             |

The shader uses fixed C/M/Y/K screen angles of 15/75/0/45 degrees, separate ink
coverage, a warm paper base, and resolution-aware dot-cell sizing. Keep those
screen semantics fixed; tune only amount and size unless a future visual proof
justifies a broader schema. Judge the result at final output resolution because
browser zoom can misrepresent the screen. Reject unstable moire, unreadable
subjects, clipped ink detail, excessive dot size, or any treatment that looks
like a transparent dot texture laid over unchanged footage.

## Two-Ink Editorial Print

Use for poster frames, editorial portraits, music/social cutaways, zine
graphics, and bold print-led transitions where two visible spot inks are more
appropriate than photographic color. This is a fixed original HyperFrames
vermilion/teal treatment, not a claim to emulate a named printer, ink set, or
commercial print process.

Do not use for literal UI, brand-color-critical products, small labels, natural
talking heads, or media that must remain photorealistic. Keep captions and
graphics as normal DOM above the treated media.

### Pixel payload

```json
{
  "intensity": 1,
  "adjust": { "contrast": 0.08, "highlights": -0.06, "shadows": 0.04 },
  "effects": { "twoInkPrint": 1, "twoInkPrintSize": 0.42 }
}
```

| Property        | Two-Ink range |
| --------------- | ------------- |
| intensity       | 0.8 to 1      |
| contrast        | 0.02 to 0.1   |
| highlights      | -0.1 to 0     |
| shadows         | 0 to 0.08     |
| twoInkPrint     | 0.8 to 1      |
| twoInkPrintSize | 0.18 to 0.55  |

The shader maps warm midtones to vermilion, deep/cool shadows to teal, and
shared dark coverage to a dark overprint on warm paper. It uses separate
15/75-degree screens, a subtle fixed registration offset, deterministic paper
texture, and resolution-aware dot sizing. Do not combine it with `halftone` or
a duotone LUT: that re-separates the result and defeats the two-ink contract.

Judge it at output resolution and across multiple frames. Reject missing second
ink, crushed faces, unstable moire, illegible silhouettes, or a result that
reads as a red tint with dots rather than two screened inks.

## Monochrome Screen Print

Use for graphic portrait beats, posterized social inserts, newspaper-like
screens, or a finite transition into visible monochrome cells. Keep captions
and typography as normal DOM above the treated media.

```json
{
  "intensity": 1,
  "effects": {
    "monoScreen": 1,
    "monoScreenSize": 0.35,
    "monoScreenAngle": 0.25,
    "monoScreenSpread": 0.3,
    "monoScreenShape": 0,
    "monoScreenInvert": 0
  },
  "palette": ["#111319", "#f2ecdc"]
}
```

Use `monoScreenShape` `0..4` for circle, square, diamond, triangle, or line.
Keep cell size within `0.15..0.55` and spread within `0.15..0.55`. Reject faces
that lose their silhouette, unstable moire, or cells too small to survive the
final encoded resolution.

## Engraved Illustration

Use for editorial portraits, historical/technical illustration, title-card
cutaways, or a source-to-line-art reveal. It is not routine correction and
should not be applied to literal UI or brand-color-critical product footage.

```json
{
  "intensity": 1,
  "effects": {
    "engraving": 1,
    "engravingSpacing": 0.4118,
    "engravingMinThickness": 0.2,
    "engravingMaxThickness": 0.4571,
    "engravingAngle": 0.25,
    "engravingContrast": 0.4667,
    "engravingSharpness": 0.59,
    "engravingWave": 0.2,
    "engravingWaveFrequency": 0.2222
  },
  "palette": ["#101216", "#f3eddf"]
}
```

Preserve the calibrated base first. Tune spacing within `0.25..0.6`, contrast
within `0.3..0.65`, and wave within `0..0.35`. Reject squeezed framing, broken
contours, noisy flat backgrounds, or lines that flicker across moving frames.

## Crosshatched Sketch

Use for hand-rendered editorial beats, comic/documentary cutaways, and short
illustrative transformations where multiple line directions should preserve
the subject contour.

```json
{
  "intensity": 1,
  "effects": {
    "crosshatch": 1,
    "crosshatchSpacing": 0.28,
    "crosshatchThickness": 0.25,
    "crosshatchAngle": 0.25,
    "crosshatchContrast": 0.3333,
    "crosshatchEdges": 0.5,
    "crosshatchLineWeight": 0,
    "crosshatchWave": 0.33,
    "crosshatchWaveFrequency": 0.2222
  },
  "palette": ["#101216", "#f3eddf"]
}
```

Tune spacing within `0.18..0.5`, edge detail within `0.3..0.7`, and wave within
`0.1..0.45`. Reject distorted aspect ratio, dense black fill that hides the
subject, or temporal shimmer stronger than the intended sketch language.

## CRT Display

Use when the media is intentionally shown as an older monitor, terminal, game
screen, or broadcast display. Curvature alone is geometry, not a complete CRT
treatment, so pair it with restrained scanlines and only slight channel
separation.

```json
{
  "intensity": 1,
  "effects": {
    "crtCurvature": 0.2,
    "scanlines": 0.35,
    "scanlineCount": 0.17,
    "scanlineSoftness": 1,
    "chromaticAberration": 0.08,
    "chromaticAngle": 0
  }
}
```

Keep curvature within `0.08..0.28`, scanlines within `0.18..0.45`, and channel
separation within `0..0.12`. Reject excessive black corners, unreadable UI,
large color fringes, or applying the display language to ordinary footage when
the user only asked for correction.

## Procedural ASCII

Use for a deliberate terminal, code, data, surveillance, editorial, or
source-to-character reveal. This is a real shader-generated 5x7 glyph field,
not monospace text placed over unchanged footage.

Do not use as routine talking-head polish, on literal UI or dense text, or when
recognizing a face/product precisely matters. Keep captions and graphics as
normal DOM above the treated media.

Choose one of these proven starting points:

```json
{
  "effects": { "ascii": 1, "asciiSize": 0.08, "asciiInvert": 1 },
  "palette": ["#020605", "#38ff78"]
}
```

The first is **Terminal ASCII**: dark field, bright green glyphs, appropriate
for code/data/device language. For a warmer print-like **Editorial ASCII**, use:

```json
{
  "effects": { "ascii": 1, "asciiSize": 0.066, "asciiInvert": 0 },
  "palette": ["#0b0d0d", "#eee9db"]
}
```

Keep `ascii` between `0.75` and `1` for a fully readable treatment and
`asciiSize` between `0.04` and `0.15`. A finite reveal may author
`--hf-color-grading-ascii: 0` inline and tween it to `1` with the registered
paused GSAP timeline. Reject unstable cells, lost silhouette/face structure,
unreadable composition, or a palette that conflicts with the project.

## Ordered Palette Dither

Use for posterized social beats, music/editorial cutaways, pixel-art language,
or a finite source-to-palette reveal. The shader uses a stable 4x4 Bayer
threshold matrix and an explicit dark-to-light palette. Do not describe it as
Floyd-Steinberg, Atkinson, or another sequential error-diffusion process.

Do not use on literal UI, brand-color-critical products, tiny labels, or long
photorealistic sections. Start with one of these original palettes:

```json
{
  "effects": { "dither": 1, "ditherSize": 0.25 },
  "palette": ["#17121a", "#824c50", "#e09873", "#f7ddb1"]
}
```

The four-color option is **Warm Print**. For a louder social/music beat, use
the six-color **Electric Ink** palette:

```json
{
  "effects": { "dither": 1, "ditherSize": 0.4 },
  "palette": ["#080717", "#3c185f", "#7e2278", "#d9339f", "#ff6b66", "#aafae0"]
}
```

HyperFrames also owns these named ramps. The name is an authoring shortcut;
persist the listed colors through the existing `palette` array:

| Group       | Palette ID       | Ordered colors                                                   |
| ----------- | ---------------- | ---------------------------------------------------------------- |
| Classic     | `noir`           | `#000000`, `#ffffff`                                             |
| Classic     | `ink-paper`      | `#1a1a2e`, `#f5f5dc`                                             |
| Classic     | `terminal`       | `#001100`, `#00ff00`                                             |
| Classic     | `amber-glow`     | `#1a0f00`, `#ffcc00`                                             |
| Classic     | `handheld-green` | `#0f380f`, `#306230`, `#8bac0f`, `#9bbc0f`                       |
| Mood        | `golden-hour`    | `#1a1205`, `#4a3510`, `#8b6914`, `#d4a017`, `#fff8dc`            |
| Mood        | `deep-sea`       | `#0a1628`, `#1a3a5c`, `#2d6187`, `#5ba4c9`, `#a8dce8`            |
| Mood        | `arctic-night`   | `#0a0a14`, `#1a2a4a`, `#3a5a8a`, `#6a9aca`, `#cae8ff`            |
| Mood        | `synthwave`      | `#120458`, `#7b2cbf`, `#e040fb`, `#ff6ec7`, `#fff59d`            |
| Mood        | `vaporwave`      | `#1a0a2e`, `#3d1a5c`, `#ff71ce`, `#01cdfe`, `#fffb96`            |
| Mood        | `forest`         | `#1a2e1a`, `#2d4a2d`, `#4a7c4a`, `#7ab37a`, `#c8e6c8`            |
| Mono        | `sepia`          | `#1a1610`, `#3d3020`, `#6b5a40`, `#a89070`, `#e8dcc8`            |
| Mono        | `blueprint`      | `#001830`, `#003060`, `#0050a0`, `#0080e0`, `#e0f0ff`            |
| HyperFrames | `warm-print`     | `#17121a`, `#824c50`, `#e09873`, `#f7ddb1`                       |
| HyperFrames | `electric-ink`   | `#080717`, `#3c185f`, `#7e2278`, `#d9339f`, `#ff6b66`, `#aafae0` |

Choose by inspected source and project language, not by palette name alone.
For example, `terminal` fits device/code language, `warm-print` fits editorial
print, and `synthwave` is an intentional stylization rather than generic polish.

`palette` must contain two to six exact `#RRGGBB` colors in authored order. Use
dark-to-light order for this treatment; the runtime validates colors but does
not reorder them, so reversing the array intentionally inverts the mapping.
Keep `dither` between `0.7` and `1` and `ditherSize` between `0.1` and `0.5`.
A finite reveal may author `--hf-color-grading-dither: 0` inline and tween it
to the chosen amount with GSAP. Judge the moving result at output resolution;
reject shimmer, lost subject structure, accidental muddy intermediate colors,
or a palette chosen without regard to the project's design language.

## Cached Error Diffusion

Use exact error diffusion for a deliberate 1-bit Macintosh, newspaper/print,
limited-palette game, or crunchy editorial treatment. It bakes a new image or
MP4 because every processed block depends on error from earlier blocks; it is
not a realtime shader setting.

Choose the algorithm by visible intent:

- `floyd-steinberg`: balanced default with organic fine texture.
- `atkinson`: higher-contrast, more open and distinctly early-Macintosh.
- `jarvis-judice-ninke`: smoother gradients with a wider 12-neighbor field.
- `stucki`: smooth, slightly sharper alternative to JJN.
- `burkes`: compact two-row texture.
- `sierra`, `sierra-lite`, `two-row-sierra`: progressively different
  speed/texture tradeoffs; use only after comparing frames.

Run the exact processor and register its output through the existing media
ledger/cache:

```bash
node <SKILL_DIR>/scripts/dither.mjs \
  --input .media/videos/video_001.mp4 \
  --out .media/generated/video_001.atkinson.mp4 \
  --algorithm atkinson \
  --palette '#17121a,#824c50,#e09873,#f7ddb1' \
  --point-size 3

npx hyperframes media-use resolve \
  --from .media/generated/video_001.atkinson.mp4 --type video --project .
```

Use the registered output path on a real `<img>` or `<video>`. Keep text,
captions, logos, and interface graphics outside the processed media. For a
finite reveal, overlap the original and processed media with identical framing
and crossfade or wipe them using the registered paused GSAP timeline. Do not
label the realtime Bayer shader as Floyd-Steinberg/Atkinson, and do not process
PQ/HLG footage without an explicit SDR tone-map decision.

## Organic Light Leak

Use for one motivated memory beat, time shift, warm scene handoff, or tactile
transition. It is a finite deterministic CSS/GSAP overlay, not a looping
texture, generic flash, or film-stock emulation.

Install the Registry overlay block:

```bash
npx hyperframes add organic-light-leak-overlay --no-clipboard
```

Insert the printed `data-composition-src` host at the intended beat and keep
its duration finite. Its paused timeline owns one rise, peak, and complete
recovery and scales those phases to the placed duration. Inspect the source
before, at the brightest frame, and after recovery. Reject clipped faces, an
unmotivated warm wash, visible black from incorrect blend mode, or a leak that
conceals the subject longer than the transition needs.

## Freeze-Frame Cutout

Use for a social introduction, speaker emphasis, chapter punctuation, sports
or creator beat, or a scrapbook/editorial hold. This requires a real alpha
matte; decoration may not conceal a poor subject edge.

Extract the exact deterministic source frame first, then remove its background:

```bash
ffmpeg -ss <seconds> -i <source-video> -frames:v 1 -y .media/generated/freeze-source.png
npx hyperframes remove-background .media/generated/freeze-source.png \
  -o .media/generated/freeze-cutout.png --json
npx hyperframes add freeze-frame-dressing --no-clipboard
```

Add the transparent result as a direct-root timed media layer and insert the
printed overlay block above the same time range. The block owns the paper,
tape, and flash; the host timeline only animates the real cutout:

```html
<img
  id="hf-freeze-cutout"
  class="clip"
  src="./.media/generated/freeze-cutout.png"
  alt=""
  data-start="6"
  data-duration="3"
  data-track-index="20"
/>
```

```js
tl.fromTo(
  "#hf-freeze-cutout",
  { y: 42, scale: 0.86, rotation: -2 },
  { y: 0, scale: 1, rotation: 0.4, duration: 0.5, ease: "back.out(1.35)" },
  freezeAt,
);
```

Inspect the matte over both light and dark temporary plates before styling it.
Reject missing hair/fingers, background halos, a cutout that changes identity,
overly thick outline, exposed frame edges, or a flash that obscures the reveal.
If the matte is not acceptable, choose another frame or keep the original media.

## Social Flash / Editorial Reveal

Use this treatment for one meaningful high-energy cut, creator reveal, product
beat, or before/after handoff. It is not a default transition for every scene.
Avoid it for calm long-form footage, accessibility-sensitive contexts, already
clipped highlights, literal UI that must remain readable through the cut, or
any request for repeated strobing.

Inspect representative frames on both sides of the cut first. Grade each media
layer for its own subject using the appropriate contract above; the flash is
not a substitute for correction. For people, a restrained `skin-soft` payload
is a safe starting point. For literal UI, preserve the pixels and use only the
authored light/motion layers when they do not obscure required information.

Install the Registry overlay block:

```bash
npx hyperframes add editorial-flash-overlay --no-clipboard
```

Insert the printed `data-composition-src` host so the block's midpoint lands
on the cut. Its own paused timeline drives the finite flash. The host timeline
may coordinate outgoing and incoming media motion without reaching into the
block:

```js
tl.to(
  "#outgoing-media",
  {
    scale: 1.035,
    "--hf-color-grading-exposure": 0.82,
    duration: 0.12,
    ease: "power3.in",
  },
  cutAt - 0.16,
);
tl.fromTo(
  "#incoming-media",
  { scale: 1.1 },
  { scale: 1, duration: 0.42, ease: "power3.out" },
  cutAt,
);
tl.to(
  "#incoming-media",
  {
    "--hf-color-grading-exposure": 0,
    "--hf-color-grading-intensity": 0.58,
    duration: 0.24,
    ease: "power2.out",
  },
  cutAt,
);
```

When the shader steps are used, author
`--hf-color-grading-exposure: 0.72` and
`--hf-color-grading-intensity: 0` inline on the incoming media so a fresh seek
has the correct start state. Set the final intensity to the source-approved
value instead of copying `0.58` blindly. Skip the shader intensity step when
the incoming source should remain ungraded.

Keep the rise between roughly `0.035` and `0.055` seconds and the recovery
between `0.24` and `0.38` seconds. Default to one neutral/warm flash event,
never saturated red, never a looping strobe, and never more than one authored
flash inside a one-second treatment window. Verify frames immediately before,
at, and after the cut, then inspect moving playback and a rendered draft. The
peak must hide the cut; the recovery must reveal a correctly framed source with
no retained prior canvas, clipped face, or unexpected highlight damage.


<!-- ===== FILE: hyperframes/media-use/references/media-treatments.md ===== -->

# Media treatments

A media treatment is a source-aware plan that composes existing HyperFrames
color, effect, timeline, and Registry primitives. It is not a second runtime
schema. Use this file to choose a primary direction. A matching recipe is an
optional tested seed; bespoke requests may assemble a validated treatment from
the canonical capability catalog.

## Permission and scope

- An explicit request such as "polish this", "make it look better", or "make it
  fit the topic" delegates a conservative treatment. Apply it, verify it, and
  report what changed.
- During an unsolicited opportunity scan, show or suggest the treatment first.
- Target meaningful photographic media. Skip text, SVG, logos, icons, UI
  chrome, and intentionally stylized footage unless the user asks.
- Realtime grading and effects apply to the entire selected real `<img>` or
  `<video>`. They do not isolate or track a face, plate, address, or other
  region. For region-only work, first create a separate cropped/masked media
  layer or use an external segmentation/tracking tool; never imply that a
  whole-media Blur or Pixelate performed region isolation.
- The realtime treatment path is Rec.709/SDR. Do not silently process HDR, HLG,
  PQ, or camera LOG sources through it.

## Classify the request

Choose the smallest lane that satisfies the request before choosing a recipe
or assembling a custom treatment:

| User intent                                         | Lane                                       |
| --------------------------------------------------- | ------------------------------------------ |
| too dark, flat, too warm, too many shadows          | correction                                 |
| shape shadows/highlights or selected colors         | wheels, curves, or HSL secondary           |
| polished, premium, warm, cinematic, fit the topic   | preset or custom treatment                 |
| retro, print, ASCII, glitch, camcorder              | shader effect or effect-bearing preset     |
| obscure the whole selected media                    | privacy Blur or Pixelate                   |
| hide one face, plate, address, or screen region     | separate crop/mask/asset or external tool  |
| draw attention to media without changing its pixels | framing, motion, or optional overlay       |
| reveal, focus, depixelate, fade the treatment       | finite seek-safe treatment keyframes       |
| REC HUD, light leak, flash, freeze-frame cutout     | Registry overlay plus any justified pixels |

The lane identifies the primary reason for the change; it is not a one-feature
limit. A final treatment may combine correction, a preset, finishing, multiple
compatible shader effects, finite keyframed values, and optional overlays when
the inspected media and user intent justify the complete combination. Keep one
primary intent as the creative anchor so the result remains coherent and
deterministic.

Do not add a stylized Effect when correction solves the complaint. Do not
change color when the request is only temporal, and do not install an overlay
when the selected media alone communicates the result.

Match strength to intent. When the user explicitly names a bold look such as
VHS, glitch, ASCII, halftone, camcorder, print, or engraving, apply its
signature effects strongly enough to read unmistakably. The guard against
unrequested additions does not mean under-delivering an effect the user asked
for. Correction and polish stay restrained; named stylization must be obvious
in the after-frame.

### Translate vague feedback conservatively

| User feedback                         | First action                                                                                    | Add only when the frames justify it                             | Never infer                                     |
| ------------------------------------- | ----------------------------------------------------------------------------------------------- | --------------------------------------------------------------- | ----------------------------------------------- |
| too many shadows and a bit boring     | lift shadows/protect highlights, then compare one restrained source-appropriate preset          | mild contrast or vibrance                                       | retro texture, HUD, or palette effect           |
| make the product footage feel premium | protect product color and labels, compare Product Polish                                        | restrained vignette on lifestyle footage                        | a cinematic LUT or crushed blacks               |
| make this reveal cooler               | preserve color and animate one supported effect or treatment value                              | a short owned overlay block                                     | unrelated whole-clip styling                    |
| make it feel like an old home video   | compare 8mm and VHS language against the source                                                 | finite weave/flicker or justified HUD                           | that every old-video request means VHS          |
| hide this face                        | explain that realtime effects are whole-media; isolate the region first or use an external tool | whole-media Blur/Pixelate only when the user accepts that scope | face tracking or masking that was not performed |
| keep the brand colors exact           | leave UI/logo pixels unchanged; use framing and motion                                          | demonstrated exposure-only correction                           | stylized preset, palette, or LUT                |

When more than one lane could fit, generate at most two candidates and choose
from inspected before/after evidence. Ordinary correction or polish starts with
one candidate; a second candidate is an escalation, not the default. Do not
stack effects merely to make the answer look more sophisticated.

## Seed or assemble

Use the table when a tested recipe directly fits. Read only that recipe
section. Recipes are optional macros, not a closed list of allowed results.

| Intent or source                                         | Recipe heading to read                            |
| -------------------------------------------------------- | ------------------------------------------------- |
| Talking head, interview, presenter, people-focused photo | `Natural Portrait`                                |
| Product footage, lifestyle footage, clean social polish  | `Product Polish`                                  |
| Screen capture, dashboard, website, app UI               | `UI Fidelity`                                     |
| Warm memory, restrained nostalgia                        | `Film Memory`                                     |
| Creator/UGC handheld camera character                    | `Creator Camcorder`                               |
| Analog tape playback                                     | `VHS Playback`                                    |
| Small-gauge home-movie character                         | `8mm Home Movie`                                  |
| Editorial dots or ink print                              | `Editorial Halftone` or `Two-Ink Editorial Print` |
| Monochrome dot/line screen print                         | `Monochrome Screen Print`                         |
| Engraved or hand-hatched illustration                    | `Engraved Illustration` or `Crosshatched Sketch`  |
| Curved scanlined display                                 | `CRT Display`                                     |
| Glyph-based art                                          | `Procedural ASCII`                                |
| Realtime palette quantization                            | `Ordered Palette Dither`                          |
| Exact historical error diffusion                         | `Cached Error Diffusion`                          |
| Finite warm flare layer                                  | `Organic Light Leak`                              |
| Held-frame graphic interruption                          | `Freeze-Frame Cutout`                             |
| Short exposure-flash transition                          | `Social Flash / Editorial Reveal`                 |

Use `rg -n '^## <heading>$' <SKILL_DIR>/references/media-treatment-recipes.md`,
then read only from that heading to the next `##`. Do not load the entire
cookbook for one request.

When source intent is unclear, inspect the concise capability overview:

```bash
hyperframes media-treatment --capabilities --json
```

It lists the complete surface by family with one-line descriptions. Then load
only the family, effect, preset, or palette relevant to the inspected source:

```bash
hyperframes media-treatment --capability <id> --json
```

The focused result provides legal controls, recommended apply values, render
cost, palette support, and the exact animation contract when supported. Use
`--all` only for tooling/tests or a genuinely exhaustive audit. Compose one
nested payload from these existing parts. Recipes and catalog-built payloads
use the same renderer and persistence contract.

Treat `renderLane: "multipass"` as a cost signal. Blur, Bloom, and Kuwahara are
bounded but more expensive than single-pass effects; avoid stacking several of
them across many simultaneous media elements unless the composition needs it,
then verify playback and a draft render.
Cost follows treated pixel area as well as element count. More than two
simultaneously visible full-frame multipass media layers requires a continuous
playback check on the target machine; simplify or pre-render the stack if it
drops frames. Do not impose or claim a universal hard cap from one machine.

## Common workflow

1. Confirm the target is a real `<img>` or `<video>` and inspect source color
   metadata.
2. For an image, read it once. For video, capture early/middle/late output as
   one labeled sheet and read that one image:

   ```bash
   hyperframes snapshot <project> --frames 3 --no-end --describe false \
     --output snapshots/treatment-before
   ```

   Read `snapshots/treatment-before/contact-sheet.jpg`; do not spend separate
   model turns reading each frame unless the sheet exposes a specific problem.
   Do not infer semantics from signal statistics alone.

3. Choose one primary lane. Use one matching recipe as a tested seed, or read
   the overview and one focused capability detail when the request is bespoke.
   A seed may be changed or combined with compatible catalog controls when the
   contact sheet justifies it. Do not invent keys, exceed reported ranges, or
   stack effects without a visual reason. Do not run the generic grade/LUT
   resolver first; it adds irrelevant candidates and may download an unused
   LUT. Use `media-treatment --selector "#hero" --analyze --json` only when
   correction needs measured signal evidence.
4. Persist pixel settings with `hyperframes media-treatment`; it validates and
   merges a patch into the existing nested `data-color-grading` contract. Use registered
   GSAP only for supported animated values and Registry overlay blocks only
   for authored dressing.
   ```bash
   hyperframes media-treatment --selector "<selector>" \
     --grading '<nested JSON patch>' --apply --json
   ```
   A selector that matches several images or videos patches every match, each
   merged into its own current grading (the JSON reports `count` and each
   target); run `--clear` first for an identical look, or add
   `--selector-index` to patch only one.
   For a temporal reveal, use the focused capability result's `animation`
   contract. If it is `null`, the capability is static. Author the starting CSS
   property inline on the real media element and return temporary treatment
   values to neutral so the finished shot preserves its existing pixels.
   Prefer that bounded media animation first; if an overlay is justified,
   install the owned Registry block instead of recreating it with bespoke
   overlay markup.
   For correction and ordinary polish, keep those values as editable
   preset/adjustment JSON; do not generate a LUT for controls the realtime shader
   already owns.
   Use the canonical `details`/`effects` fields for vignette, grain, blur,
   pixelate, and related primitives. Do not duplicate them with CSS filters,
   SVG turbulence, opacity, or decorative DOM overlays.
5. When the treatment calls for an overlay, install that named block with
   `hyperframes add <name> --dir <project> --no-clipboard --json`, inspect its
   returned `data-composition-src` host, and place it once using the block's
   timing contract. Check for the installed file and host element
   ID before insertion; never duplicate an existing overlay block. This is one
   treatment workflow: do not make the user discover Catalog or separately ask
   for the recipe's justified overlay.
6. For ordinary correction/polish, capture one after-sheet with the same three
   timestamps under `snapshots/treatment-after`, compare it to the before-sheet,
   and stop when the result is clearly better. Run the normal project check;
   do not encode a draft solely to prove a static correction.
7. Escalate only when evidence requires it. Read individual frames to diagnose a
   specific visual problem. Preview and render moving evidence when judging
   treatment keyframes, glitch/tape motion, overlays, playback smoothness, LUT
   timing, or any other temporal behavior. HDR/LOG, privacy, and brand-sensitive
   work also require the existing explicit caveats and stronger verification.
   If the treatment is not clearly better, keep the source unchanged.
8. Report the selected media, primary intent, recipe seed if used, final
   composed controls, optional overlays, and the frames/render that were
   actually checked. Do not report visual quality from command success alone.

`media-treatment --analyze` provides deterministic clipping and signal
evidence for local composition media, not subject recognition or automatic
taste. It reports HDR/metadata caveats and a bounded primary-correction patch;
it does not invent wheels, curves, or HSL selections from statistics.


<!-- ===== FILE: hyperframes/media-use/references/memory.md ===== -->

# User memory — preferences and recipes

## Preferences — remembered defaults

The lightweight tier of user memory: confirmed brief answers (destination, aspect, language, flow, storyboard, voice, style preset) persisted on the same two-tier split as assets — project `.media/preferences.json` (committed, the team inherits it) and personal `~/.media/preferences.json`. A value earns the personal tier by being confirmed in **two different projects**, so a one-off choice never pollutes the global defaults.

```bash
node <SKILL_DIR>/scripts/prefs.mjs get --hyperframes . --json      # merged view (project overrides user)
node <SKILL_DIR>/scripts/prefs.mjs record --hyperframes . --key destination --value x-feed
node <SKILL_DIR>/scripts/prefs.mjs record --hyperframes . --key style_preset --value pin-and-paper --workflow faceless-explainer
```

Only what the user actually confirmed gets recorded — never an inferred or defaulted value. How workflows consume these (a remembered value becomes the recommended default with a receipt, and never skips a question) is the brief contract's rule: `hyperframes/references/brief-contract.md` § 2, Remembered defaults.

## Recipes — frozen video bundles

The heavyweight tier of user memory: one approved run frozen as a named, versioned bundle — `frame.md`, the storyboard skeleton (structure kept, content blanked to per-frame fill-ins), the brief skeleton (from `BRIEF.md` when the project has one — reusable frontmatter kept, run-shape and prose blanked), and the confirmed brief values. Same two tiers: project `.media/recipes/<name>/` (committed) and `~/.media/recipes/<name>/` (a freeze is already a confirmed bundle, so it promotes immediately — no two-project rule). Re-freezing a name bumps `version` and archives the old folder as `<name>@v<N>`.

```bash
node <SKILL_DIR>/scripts/recipe.mjs freeze --hyperframes . --name weekly-promo   # workflow read from BRIEF.md (--workflow only for briefless projects)
node <SKILL_DIR>/scripts/recipe.mjs list --hyperframes . --workflow product-launch-video
node <SKILL_DIR>/scripts/recipe.mjs use --hyperframes . --name weekly-promo   # also: resolve.mjs --type recipe --entity weekly-promo
```

The freeze is offered once after the final approval (`hyperframes/references/review-loop.md` § 4), and the intent layer (`/hyperframes` → `references/intent-interview.md`, step 1) checks for a match before its first question. Adopting a recipe fills the brief, the design spec, and the storyboard skeleton — and unlike preferences it may skip the questions it answers: the bundle was approved as a whole, and adoption itself is the question.

## Files

- `.media/manifest.jsonl`: machine SSOT, one JSON record per line. Records are keyed by path and only appended, so
  the last record for a path is the file's record; a file moved or replaced by hand keeps (or loses) its record by path.
- `.media/index.md`: agent-readable table (id, type, dur, dims, path, description)
- `.media/preferences.json`: the project's remembered defaults (committed)
- `~/.media/`: global cross-project reuse cache (content-addressed, SHA-256)
- `~/.media/preferences.json`: personal remembered defaults (promoted after two projects)
- `.media/recipes/<name>/`: frozen video bundles — recipe.json + frame.md + storyboard skeleton (committed)
- `~/.media/recipes/<name>/`: personal recipe tier (promoted on freeze)
- `~/.media/misses.jsonl`: local-only resolve misses, including intent text for `--stats`


<!-- ===== FILE: hyperframes/media-use/references/meta.md ===== -->

# Ownership matrix, usage stats, telemetry, privacy

Maintainer-facing reference. Nothing here changes how you resolve or operate on media.

## What it owns (the gaps HyperFrames leaves)

HyperFrames owns media _playback_; media-use owns everything else. Each row is enforced by `packages/cli/src/media-use/lib/coverage.test.mjs` so the claim can't rot.

| HyperFrames gap                            | media-use owns it via                                                                                                                                                                                                                                    |
| ------------------------------------------ | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Audio-only, no image/icon                  | `resolve --type image\|icon` (heygen asset search)                                                                                                                                                                                                       |
| No third-party brand logos                 | `resolve --type logo` (theSVG → GitHub org avatar → domain favicon)                                                                                                                                                                                      |
| No voice / audio generation                | `resolve --type voice` (HeyGen TTS free-usage path; optional local Kokoro) + the audio engine (`audio/scripts/audio.mjs`)                                                                                                                                |
| Scattered/duplicated audio engine          | one consolidated engine under `audio/` (hyperframes-media retired)                                                                                                                                                                                       |
| No agent media-ops (cut/reframe/transform) | `references/operations.md` + `resolve --from` to register outputs                                                                                                                                                                                        |
| No transcript-driven cutting               | `scripts/transcript-cut.mjs` compiles word-timestamp edits into cut lists                                                                                                                                                                                |
| No auto-duck / publish loudness            | `scripts/audio-duck.mjs` + `references/operations.md` loudnorm/sidechain recipes                                                                                                                                                                         |
| No cross-project memory                    | global content-addressed cache + auto-promote (`~/.media`)                                                                                                                                                                                               |
| Grade recipes and LUT freezing             | `resolve --type grade` emits a paste-ready recipe and `resolve --type lut` freezes validated `.cube` files; direct element analysis/authoring lives in `hyperframes media-treatment`                                                                     |
| No image generation                        | `resolve --type image` — RAM-graded local mflux (FLUX), codex `image_gen` upsell                                                                                                                                                                         |
| No video generation                        | `resolve --type video` — HeyGen avatar video first (free-usage path, sign-in nudge on auth failure), local LTX fallback (`videogen` ladder); image-to-video, photo-avatar, dub/translate remain manual `heygen` CLI recipes (`references/operations.md`) |
| Weak local-model defaults                  | HeyGen free-usage path via the `heygen` CLI; local open-source tools only as opt-in alternatives                                                                                                                                                         |

## Usage stats

Use `resolve --stats` for a local, shareable report over the current project's `.media/` manifest, the global `~/.media/` cache, and local resolve misses. Human output is compact; add `--json` for a single machine-readable object, and `--days N` to window timestamped records.

```bash
npx hyperframes media-use resolve --stats --project . --days 7
# media-use stats
# total resolves: 12
# misses: 2
# hit rate: 86%
```

## Telemetry

`resolve` and the edit tools (transcribe / transcript-cut / audio-duck) send an
anonymous usage event to PostHog (`scripts/lib/telemetry.mjs`), so we can see
which capabilities are actually used. It records only the media TYPE, the
resolution SOURCE, and the winning PROVIDER: never the intent text, file names,
or paths, and `$ip:null` so no IP is stored. Best-effort and non-blocking (a
resolve never waits on or fails from telemetry).

Opt out with `DO_NOT_TRACK=1` or `HYPERFRAMES_NO_TELEMETRY=1` (also off in CI and
dev). Same public PostHog project key and opt-outs as the `hyperframes` CLI.

HeyGen request tagging: every generating `heygen` call (TTS, avatar video, catalog
search) carries the allowlisted `X-HeyGen-Client-Source: media-use` header, sourced
from one shared constant (`HEYGEN_CLIENT_SOURCE_ARGV` in `packages/cli/src/media-use/lib/heygen-cli.mjs`)
so a future call site can't silently ship untagged. Read-only discovery calls
(`voice list`, `avatar list`) are intentionally left untagged.

## Privacy

media-use uses the same shared install id as the `hyperframes` CLI/studio
(`~/.hyperframes/config.json`). When you are signed in to HeyGen, usage is
linked to your account email, or username when email is unavailable, matching
the CLI behavior. The events stay coarse: media type, source, provider, and
small counts only; intent text and paths stay local. Disable telemetry with
`HYPERFRAMES_NO_TELEMETRY=1` or `DO_NOT_TRACK=1`.


<!-- ===== FILE: hyperframes/media-use/references/operations.md ===== -->

# Media operations: agent guidance

media-use resolves and remembers assets. For **operating** on them: cutting,
reframing, stitching, transforming, it does not wrap every action as a bespoke
command. Instead it points you at the right local tool (decision OP1). Run the
tool, then register the output with `resolve --from <output> --type <type>` so the
result lands in the ledger and the global cache like any other asset.

All tools below are local and free. ffmpeg is assumed present (it backs the
engine already).

## Cut / trim: keep a slice

```bash
ffmpeg -i in.mp4 -ss 00:00:12 -to 00:00:20 -c copy out.mp4   # 0:12–0:20, no re-encode
```

In-composition trimming usually needs **no new file**: a clip plays a sub-window
via `data-media-start` + `data-duration` (see hyperframes-core). Only cut a
physical file when exporting/assembling outside the composition.

## Reframe / crop: change aspect ratio

```bash
# 16:9 -> 9:16, crop centered
ffmpeg -i in.mp4 -vf "crop=ih*9/16:ih,scale=1080:1920" out.mp4
```

For a non-destructive crop, set a `clip-path` on the element in the composition
itself (render-time, source file untouched) instead of re-encoding with ffmpeg.

## Montage / stitch: join clips

```bash
printf "file '%s'\n" a.mp4 b.mp4 c.mp4 > list.txt
ffmpeg -f concat -safe 0 -i list.txt -c copy out.mp4
```

## Silence-cut / highlight: trim dead air, grab the best moment

```bash
auto-editor in.mp4 --edit audio:threshold=4% -o tight.mp4   # pip install auto-editor
scenedetect -i in.mp4 detect-adaptive list-scenes           # pip install scenedetect
```

## Transforms with a quality choice (process)

These have a local option AND a higher-quality HeyGen-CLI option. Run the local
one for free/offline; use the HeyGen CLI when quality matters. Showing the user
a **side-by-side** (local vs HeyGen) is the honest way to let them choose.

| Op                 | Local (free)                                       | HeyGen CLI (quality)        |
| ------------------ | -------------------------------------------------- | --------------------------- |
| Background removal | `hyperframes remove-background in.png` (u2net)     | `heygen background-removal` |
| Upscale            | `realesrgan-ncnn-vulkan -i in.png -o out.png -s 4` | n/a                         |
| Lipsync (dub)      | n/a                                                | `heygen lipsync`            |
| Translate          | n/a                                                | `heygen video-translate`    |

After any op: `resolve --from out.ext --type <type>` to register the derived
asset (it records provenance and auto-promotes to the global cache).

> ponytail: media-use doesn't re-wrap ffmpeg/heygen here, that's deliberate
> (OP1). The value it adds is the ledger + global reuse on the _output_, via
> `--from`. Add a thin `process` verb only if agents repeatedly fumble these
> recipes.

## Exact error-diffusion dither

Use the local processor when the requested look specifically calls for
Floyd-Steinberg, Atkinson/Macintosh, Jarvis-Judice-Ninke, Stucki, Burkes, or a
Sierra variant. These are sequential error-diffusion algorithms, not the
realtime Bayer `effects.dither` shader.

```bash
node <SKILL_DIR>/scripts/dither.mjs \
  --input source.mp4 \
  --out source.atkinson.mp4 \
  --algorithm atkinson \
  --palette '#0f380f,#306230,#8bac0f,#9bbc0f' \
  --point-size 3

npx hyperframes media-use resolve \
  --from source.atkinson.mp4 --type video --project .
```

Available algorithms: `floyd-steinberg`, `atkinson`,
`jarvis-judice-ninke`, `stucki`, `burkes`, `sierra`, `sierra-lite`, and
`two-row-sierra`. The default is balanced Floyd-Steinberg with a black/white
palette. Palettes contain 2-6 `#rrggbb` colors in authored dark-to-light order;
reversing the order intentionally inverts the mapping. `--point-size` controls
1-20px blocks; `--brightness` and `--contrast` accept 0.5-2; `--detail` accepts
0.1-1.

The processor supports ordinary SDR images and MP4 video, preserves video
audio, and emits BT.709 MP4. It rejects tagged PQ/HLG input rather than silently
tone-mapping it. To animate the transformation, keep the original and processed
files as two real media layers and use the seek-safe GSAP timeline to reveal or
crossfade between them. Use the realtime Bayer shader instead when the dither
amount itself must animate continuously.

## Transcription (default: Parakeet, better than whisper.cpp)

`transcribe.mjs` is the default local transcription path. It runs **NVIDIA
Parakeet-TDT via parakeet-mlx**, which beats whisper.cpp on the Open ASR
Leaderboard (avg WER ~6.05% vs 7.44%; on NOISY audio 4.73% vs 5.96%, where
whisper-large-v3 hallucinated to 308% WER on meetings) and is 5-10x faster.
It emits `{ text, words:[{text,start,end}] }` with word timestamps (merged from
Parakeet's sub-word tokens), feeding transcript-cut, captions, and the audio
engine directly.

```bash
# install once: uv venv ~/.venvs/parakeet && VIRTUAL_ENV=~/.venvs/parakeet uv pip install parakeet-mlx
node <SKILL_DIR>/scripts/transcribe.mjs --input talk.mp4 --out talk.transcribe.json

# the hyperframes CLI runs Parakeet on macOS, Linux and Windows once it is installed:
npx hyperframes models install parakeet                 # once, ~640 MB, ask the user first
npx hyperframes transcribe talk.mp4 --engine parakeet   # or --engine auto (default)
```

VERIFIED on 24GB: accurate, ~3s (cached) for 8s audio. Parakeet covers 25
European languages, English included. For other languages, or when parakeet-mlx is not
installed, transcribe.mjs falls back to `hyperframes transcribe`, which uses the
CLI's Parakeet when `models install parakeet` has run and whisper.cpp (99
languages) otherwise. `--engine parakeet|whisper` forces one. (Cohere
Transcribe tops the leaderboard on paper but its mlx-audio quants produced
garbage and ran 40-70x slower on a Mac in testing, so it is not wired in.)

## Text-based editing (transcript cut)

`transcript-cut.mjs` is a compiler, not a wrapper: it turns word timestamps and
agent cut decisions into exact kept segments. It is provided even though the rest
of this file is guidance-only.

```bash
node <SKILL_DIR>/scripts/transcript-cut.mjs \
  --input talk.mp4 \
  --transcript talk.transcribe.json \
  --remove "12.41-15.02,88.3-91.7" \
  --remove-fillers "um,uh,like" \
  --cut-silence 0.8 \
  --out talk.cut.mp4

resolve --from talk.cut.mp4 --type video
```

Use `--plan` first when you want to inspect the kept segment JSON before encoding.

## Ducking (declare in-composition / bake for export)

B1, declare ducking in the composition. `audio-duck.mjs` emits a volume lane
as a `data-automation` attribute. Add it to the background `<audio>` element;
the source file stays untouched. Lane times are clip-local, so pass
`--composition` to let the script subtract the element's `data-start`.

```bash
node <SKILL_DIR>/scripts/audio-duck.mjs \
  --meta audio_meta.json \
  --target "#bgm" \
  --composition index.html
```

```html
<!-- auto-duck: #bgm under narration; add to its <audio> element -->
data-automation='{"version":1,"lanes":[{"target":"volume","points":[{"t":0,"v":0.6},{"t":3.42,"v":0.6},{"t":3.57,"v":0.15},{"t":9.87,"v":0.15},{"t":10.27,"v":0.6}]}]}'
```

B2, bake ducking only for exported or standalone files.

```bash
ffmpeg -i bgm.mp3 -i voice.wav \
  -filter_complex "[0][1]sidechaincompress=threshold=0.03:ratio=8:attack=200:release=400[ducked]" \
  -map "[ducked]" bgm.ducked.wav
```

Declare inside compositions. Bake only for assets leaving the hyperframes
pipeline.

## Publish loudness

Two-pass `loudnorm` measures first, then applies the measured values with the
target LUFS baked in.

Socials target, -14 LUFS:

```bash
ffmpeg -i mix.wav \
  -af loudnorm=I=-14:TP=-1.5:LRA=11:print_format=json \
  -f null -

ffmpeg -i mix.wav \
  -af loudnorm=I=-14:TP=-1.5:LRA=11:measured_I=<input_i>:measured_TP=<input_tp>:measured_LRA=<input_lra>:measured_thresh=<input_thresh>:offset=<target_offset>:linear=true:print_format=summary \
  mix.social.wav
```

Podcast target, -16 LUFS:

```bash
ffmpeg -i mix.wav \
  -af loudnorm=I=-16:TP=-1.5:LRA=11:print_format=json \
  -f null -

ffmpeg -i mix.wav \
  -af loudnorm=I=-16:TP=-1.5:LRA=11:measured_I=<input_i>:measured_TP=<input_tp>:measured_LRA=<input_lra>:measured_thresh=<input_thresh>:offset=<target_offset>:linear=true:print_format=summary \
  mix.podcast.wav
```

## Generate: images (local first, cloud upsell)

`resolve --type image` retrieves from the HeyGen catalog first; on a miss it
GENERATES. Two paths, best-for-the-machine picked automatically:

1. **Local (default, free, private): mflux** (FLUX-on-MLX). `resolve` spec-checks
   AVAILABLE RAM and runs the best FLUX-class model that fits, using the
   CLI-bundled `imagegen` ladder (its modules are not shipped in the standalone
   skill). The RAM ladder:

   | Tier   | Model                | Needs (available RAM) | Notes                               |
   | ------ | -------------------- | --------------------- | ----------------------------------- |
   | medium | FLUX.1 schnell int4  | ~8GB (`--low-ram`)    | ~20s/512px on 24GB. VERIFIED. Fast. |
   | large  | FLUX.2 Klein 4B int4 | ~32GB                 | higher quality, full-resident       |
   | xlarge | Qwen-Image           | ~64GB                 | top quality, 64GB+ Macs only        |

   Gotchas baked into the table: the official FLUX repos are HF-gated, so it
   points at non-gated community 4-bit re-uploads; and `--low-ram` is MANDATORY
   at the medium tier (without it a 768x512 run swap-thrashed to 90 minutes on
   24GB; with it, 20 seconds).

2. **Cloud upsell (better quality): the `codex` CLI** `image_gen` tool, on the
   user's ChatGPT subscription (codex owns auth, no key here, no per-call
   charge). It is the automatic fallback when no local model fits AND the
   explicit "make it better" choice on any machine. Users who just want codex
   can ask for it directly. Verified: prompt -> raster -> frozen + ledgered.

`--local-only` keeps mflux (once cached) and skips codex (network).

## Generate: video (`resolve --type video`, HeyGen avatar first)

`resolve --type video "<intent>"` is the default path. It generates a
script-driven HeyGen avatar video first (the free-usage allowance — OAuth
sessions ride the web-plan free avatar-video quota where eligible, API keys
follow normal API billing), falling back to local generative LTX only when
HeyGen is unavailable, uncredentialed, or `--local-only` is passed. The two
are non-substitutable outputs (a real presenter vs. a generic generative
clip), so treat the fallback as "HeyGen wasn't reachable," not "upgrade the
quality":

- **HeyGen avatar video (default, free for new API users):**
  The CLI-bundled provider shells the
  `heygen` CLI — never the raw API — auto-picking a public avatar and a
  starfish voice (override with `--avatar-id`/`--voice-id`, threaded through
  as `ctx.avatarId`/`ctx.voiceId`). If the CLI reports `not_authenticated`,
  the provider prints an onboarding recommendation (avatar video is free for
  new API users — sign in) to stderr and falls through to LTX instead of
  hard-failing.
- **Local fallback: LTX 2.3 on MLX** via `dgrauet/ltx-2-mlx`, the `videogen`
  ladder bundled in the HyperFrames CLI. Generative clips
  (t2v), spec-gated to RAM. Verified on 24GB: 512x320 x 33f with audio.

Every generating `heygen` call from media-use — TTS, avatar video, and
catalog search — sends the allowlisted `X-HeyGen-Client-Source: media-use`
header (persistent flag, works on every subcommand) via the shared
CLI-internal `HEYGEN_CLIENT_SOURCE_ARGV` constant, so usage
tags correctly in billing/resource meta and shows up in the API dashboards.
Read-only discovery (`avatar list`, `voice list`) doesn't need it.

For structured bodies `resolve --type video` doesn't expose yet (a specific
`avatar_id`/`voice_id` combination beyond the ctx overrides, or a
pre-recorded `audio_url` instead of a script), the raw `heygen video create`
recipe below remains the escape hatch:

```bash
# discover an avatar + a starfish voice, then create + wait
heygen avatar list --ownership public --limit 5
heygen voice list --engine starfish --limit 5
heygen video create --headers "X-HeyGen-Client-Source: media-use" --wait -d '{
  "type": "avatar",
  "avatar_id": "<avatar-id>",
  "script": "Your narration here.",
  "voice_id": "<voice-id>"
}'
```

Avatar videos are deterministic + script-driven (lip-sync from a script or a
pre-recorded `audio_url`), distinct from the generative LTX clips. After a
manual recipe renders, `resolve --from <downloaded.mp4> --type video` to
ledger it (not needed when generating via `resolve --type video` directly —
that already ledgers the result).

### Image-to-video (animate any still into a talking clip)

Not wired into `resolve --type video` (deferred — the `avatar` type covers
the default script-driven case). `heygen video create` takes the raw
`POST /v3/videos` body, so switching `type`
from `avatar` to `image` animates **any image of a person** into a lip-synced
talking video, with no avatar/photo-avatar creation step first. Point `image` at a
public URL or an uploaded `asset_id`, and drive speech with a `script`+`voice_id`
or a pre-recorded `audio_url`:

```bash
heygen video create --headers "X-HeyGen-Client-Source: media-use" --wait -d '{
  "type": "image",
  "image": { "type": "url", "url": "https://example.com/person.jpg" },
  "script": "Your narration here.",
  "voice_id": "<voice-id>"
}'
```

Common optional fields: `title`, `resolution` (`4k`/`1080p`/`720p`),
`aspect_ratio`, `remove_background`, `background`, `voice_settings`,
`motion_prompt` + `expressiveness` (photo-avatar animation), and
`callback_url`/`callback_id` for webhooks. Don't hardcode these from memory: the
CLI self-documents the full, current body with
`heygen video create --request-schema` (a discriminated union keyed on `type`),
so read the schema rather than trusting a stale field list. For a still you'll
reuse across many scripts, create a reusable **Photo Avatar** once instead
(`heygen avatar create`). Ledger the result with
`resolve --from <downloaded.mp4> --type video`. Docs:
<https://developers.heygen.com/image-to-video>.

## HEVC / H.265 sources

HEVC/H.265 sources need no conversion for **render** (FFmpeg pre-decodes all
input video) or for **preview** (auto-proxy transcodes and caches an H.264
copy on first use, disable with `--no-proxy` or `media.autoProxy: false` in
hyperframes.json). A manual H.264 proxy via `ffmpeg -i in.mp4 -c:v libx264
-crf 18 proxy.mp4`, registered with `resolve --from`, remains available for
edge cases (e.g. auto-proxy disabled, or ffmpeg unavailable at preview time).


<!-- ===== FILE: hyperframes/media-use/references/resolve.md ===== -->

# Resolve — command, flags, reuse, adopt, inventory

```bash
npx hyperframes media-use resolve --type <type> --intent "<description>" --project <dir>
```

Returns one line: `resolved <id> → <path> (<type>, <metadata>)`

## Types

| Type    | What it finds                    | Provider / cascade                                           |
| ------- | -------------------------------- | ------------------------------------------------------------ |
| `bgm`   | Background music                 | HeyGen audio catalog (10k+ tracks)                           |
| `sfx`   | Sound effects                    | Bundled 19-file library + HeyGen catalog                     |
| `image` | Photos, backgrounds              | HeyGen asset search (75k+ vectors)                           |
| `icon`  | Icons, symbols                   | HeyGen asset search (type=icon)                              |
| `logo`  | Official brand marks             | theSVG → GitHub org avatar → domain favicon                  |
| `voice` | TTS voiceover                    | HeyGen TTS free-usage path; optional local Kokoro            |
| `grade` | HyperFrames color-grading blocks | Core preset → look index params/CDN LUT → deterministic cube |
| `lut`   | Reusable `.cube` LUT files       | Look index params/CDN LUT → deterministic cube               |

## Examples

```bash
# Background music
npx hyperframes media-use resolve --type bgm --intent "upbeat tech launch" --project .
# → resolved bgm_001 → .media/audio/bgm/bgm_001.mp3 (bgm, 25s)

# Sound effect
npx hyperframes media-use resolve --type sfx --intent "whoosh" --project .
# → resolved sfx_001 → .media/audio/sfx/sfx_001.mp3 (sfx, 0.57s)

# Image
npx hyperframes media-use resolve --type image --intent "gradient tech background" --project .
# → resolved image_001 → .media/images/image_001.jpg (image)

# Icon
npx hyperframes media-use resolve --type icon --intent "rocket" --project .
# → resolved icon_001 → .media/images/icon_001.png (icon, transparent)

# Brand logo (official mark — never redrawn by hand)
npx hyperframes media-use resolve --type logo --entity linkedin --intent "LinkedIn logo" --project .
# → resolved logo_001 → .media/images/logo_001.svg (logo, official mark)

# Color grade block
npx hyperframes media-use resolve --type grade --intent "warm daylight" --project . --json
# → {"ok":true,"preset":"warm-daylight","grading":{"preset":"warm-daylight","intensity":1},...}

# LUT file
npx hyperframes media-use resolve --type lut --intent "teal orange blockbuster" --project .
# → resolved lut_001 → .media/luts/lut_001.cube (lut)
```

## Flags

| Flag            | Description                                                                          |
| --------------- | ------------------------------------------------------------------------------------ |
| `--type, -t`    | Media type: bgm, sfx, image, icon, logo, voice, grade, lut                           |
| `--intent, -i`  | What you need (natural language)                                                     |
| `--entity, -e`  | Entity name for cache matching (optional)                                            |
| `--project, -p` | Project directory (default: .)                                                       |
| `--candidates`  | List reusable assets (project + global cache) for `--type`; no download, no mutation |
| `--reuse <sha>` | Import a specific global-cache asset (by content sha/prefix, from `--candidates`)    |
| `--from`        | Freeze a local file or direct public URL (ingest)                                    |
| `--for`         | Analyze a local image/video and add measured adjust suggestions (`grade` only)       |
| `--local-only`  | Offline: skip every network provider (cache + local only)                            |
| `--provider`    | Force one generator (e.g. `codex`, `mflux`, `kokoro`, `heygen`)                      |
| `--adopt`       | Bulk-import existing assets/ into manifest                                           |
| `--doctor`      | Check local CLI dependencies; no manifest changes                                    |
| `--stats`       | Print local usage stats from `.media/` and `~/.media`; no manifest changes           |
| `--days N`      | Limit `--stats` to timestamped records/misses from the last N days                   |
| `--json`        | Output JSON instead of one-line result                                               |

## Reuse before you resolve

Before resolving bgm/sfx/image/icon/logo/grade/lut, **check what already exists and reuse it when it fits.** media-use does not semantically match for you — you are the judge. It surfaces candidates; you decide.

```bash
npx hyperframes media-use resolve --type bgm --intent "upbeat tech launch" --candidates --project .
#   [project] upbeat tech launch (25s, heygen.audio.sounds)
#           .media/audio/bgm/bgm_001.wav
#   [global]  energetic tech intro (22s, heygen.audio.sounds)
#           --reuse 06e052c075fd2b80
```

Read the list and judge semantic fit yourself — "upbeat tech launch" ≈ "energetic tech intro" is a call only you can make from the descriptions. Then:

- **A project candidate fits** → just reference its path in your composition. Nothing else to run.
- **A global candidate fits** → `resolve --type bgm --reuse <sha>` copies it into this project (self-contained render) and records it.
- **Nothing fits** → resolve fresh (`--type ... --intent ...`).

**Trust guardrail — when unsure, resolve fresh.** A redundant download is cheap; shipping the wrong asset is not. Judge fit from description + prompt + type + duration/dims. For **brand/entity** assets, reuse a _global_ candidate only when the entity matches exactly — the global cache aggregates every project you have worked on, so a `--candidates` list can surface another client's brand mark and its prompt text. Never reuse a cross-project brand asset on a loose match.

The deterministic floor still runs automatically: an identical (case/whitespace-insensitive) repeat auto-reuses with no `--candidates` step. `--candidates` is only for the semantic layer above that floor — and a fuzzy match is **never** auto-applied; reuse is always your explicit call. On a resolve that misses the floor and is about to fetch, media-use prints a one-line stderr hint when similar cached assets exist, pointing you back here.

## How it works

`resolve` runs an automatic floor, then falls through to fetching:

1. Check project `.media/manifest.jsonl` for a prompt match (case- and whitespace-insensitive) — auto-reuse
2. Scan existing `assets/` directory for unregistered files that share a word with the need
3. Check global cache `~/.media/` for a reusable asset matched on the same normalized prompt — auto-reuse
4. Search via provider (HeyGen audio catalog, HeyGen asset search), or resolve color locally
5. Freeze file to `.media/<type>/`, register in manifest, regenerate `index.md`, auto-promote to `~/.media/`

Steps 1 and 3 are the **deterministic floor**: they only auto-reuse an exact-normalized match, never a fuzzy one. Semantic reuse ("close enough") is the agent's explicit call via [Reuse before you resolve](#reuse-before-you-resolve) — it never happens automatically. The agent gets back **one line**; candidates, scores, provenance stay on disk.

## Stamping provenance when mounting a resolved video

`resolve` never writes composition HTML itself — mounting a `<video>` element
into a composition is always the agent's own edit. When the mounted video's
manifest record has `provenance.provider === "heygen.video"` (check
`.media/manifest.jsonl` or the one-line resolve output for the provider name),
add `data-media-source="heygen"` to that `<video>` tag. Leave the attribute off
entirely for every other provider (`ltx.local`, an adopted/local file, etc.) —
this is not a general provider taxonomy, just the one signal render telemetry
tracks today.

## Adopt existing projects

Most HyperFrames projects already have assets in `assets/`. media-use adopts them:

```bash
npx hyperframes media-use resolve --adopt --project .
# → adopted 9 assets from assets/
#   bgm_001 → assets/bgm/mango-fizz.mp3 (bgm, 146.6s)
#   image_001 → assets/images/avatar.jpg (image, 400×400)
```

`ffprobe` extracts real duration and dimensions. During resolve, unregistered files in `assets/` matching the intent are adopted on the fly.

## Reading the inventory

After resolve or adopt, read `.media/index.md` for the full inventory:

```
# .media · 4 assets

id         type   dur   dims       path                          description
bgm_001    bgm    25s   -          .media/audio/bgm/bgm_001.mp3  upbeat tech launch
sfx_001    sfx    0.6s  -          .media/audio/sfx/sfx_001.mp3  whoosh
image_001  image  -     1920×1080  .media/images/image_001.jpg   gradient tech background
icon_001   icon   -     200×200    .media/images/icon_001.png    rocket
```

## Cross-project reuse

Assets are cached automatically on resolve. Every resolved/ingested asset is auto-promoted to the global cache at `~/.media/`, so subsequent resolves for the same (or near-identical) prompt, in any project, hit the cache with no re-download and no provider call.

For a _semantically_ similar (not identical) need in another project, the exact-match floor won't fire — use [Reuse before you resolve](#reuse-before-you-resolve): `--candidates` lists the global assets, and `--reuse <sha>` imports the one you pick. This is how a track resolved in one project gets reused in the next when the wording differs.


<!-- ===== FILE: hyperframes/media-use/references/setup-providers.md ===== -->

# Setup and providers — install, auth, RAM ladders, forcing a provider

## Setup — install heygen first (free-usage path)

Install the HeyGen CLI through its [verified release instructions](https://developers.heygen.com/cli), then run:

```bash
heygen update             # free usage needs the OAuth-capable CLI (v0.3.0+)
heygen auth login --oauth # OAuth = free subscription credits; --api-key bills API credits
```

This unlocks the FREE path for bgm/sfx/image/icon catalog search, TTS (voice), and avatar videos. Sign in with `--oauth` — the free allowance rides on the OAuth session (an API key bills API credits instead). **media-use requires heygen >= v0.3.0 uniformly** (the OAuth free-usage path needs it), so `--doctor` nudges older CLIs to update even for API-key-only use. Before resolving anything, verify setup with:

```bash
npx hyperframes media-use resolve --doctor
```

## Host HeyGen access (no CLI sign-in)

A host app can give media-use HeyGen access of its own by setting
`HEYGEN_API_BASE` (its gateway), `HEYGEN_API_KEY` (the token that gateway
accepts) and, for a loopback gateway, `HEYGEN_ALLOW_HTTP=1`. The gateway adds
the host's key, so it never enters the agent's environment, and every
call is charged to that key's API credits. The `heygen` CLI honours the same
variables, so `resolve` (bgm/sfx/image/icon/voice/avatar-video) and the audio
engine's TTS all go through the host. With host access, skip CLI install and
sign-in, prefer the host's own HeyGen tools where it has them, never fall back
to a local or third-party generator on your own, and relay a refused call's
message (for example "add a key in Settings > Account") as written.

## Providers

media-use holds no keys; every external tool owns its auth. Generation is
centered on the HeyGen CLI free-usage path. Install and authenticate `heygen`
before resolving bgm/sfx/image/icon/voice/avatar-video; music and sound effects from
a host app's own tools need none of it. Local tools are opt-in
alternatives where they exist: mflux for image, Kokoro for voice, Parakeet for
transcription, and LTX for local video generation. `resolve` spec-checks
AVAILABLE RAM for those local ladders inside the CLI (the image tiers are listed
in `references/operations.md`).

| Type      | Provider / path                                                                                                                                                               |
| --------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| bgm/sfx   | heygen catalog free-usage path; a host app's own music and sound tools come first                                                                                             |
| image     | heygen search free-usage path; optional local mflux; codex `image_gen` upsell                                                                                                 |
| voice     | heygen tts free-usage path; optional local **Kokoro** (free, on-device)                                                                                                       |
| icon      | heygen asset search free-usage path                                                                                                                                           |
| logo      | theSVG (thesvg.org), then GitHub org avatar, then domain favicon (all free)                                                                                                   |
| grade/lut | local core-preset map, params/CDN look index, deterministic `buildCube` fallback                                                                                              |
| video     | heygen avatar video free-usage path (sign-in nudge on auth failure); optional local LTX (`videogen` ladder). Image-to-video / photo-avatar / dub stay manual `heygen` recipes |

Local Kokoro (voice), mflux (image), and LTX (video) run on-device (free,
private, offline once cached). The `codex` CLI remains the ChatGPT-sub image
upsell. Cost rule (X4): the agent confirms before an agent-initiated paid call;
a user-requested one just runs — `heygen.video` is flagged paid (metered free
allowance) so an agent-initiated `resolve --type video` confirms first.

To force a specific generator (e.g. a user says "make this image with codex"),
pass `--provider codex`: it pins resolution to that provider and skips the
free-usage default. See `references/operations.md` for the RAM ladders and
provider recipes.

`--local-only` skips every network provider, including the free HeyGen ones,
leaving the project + global cache and any installed local provider. For
HeyGen-only types, that means no fresh resolve.

## CLI tools used (what to run, and how to enable each)

`resolve` auto-cascades; each provider shells one CLI. HeyGen is the
free-usage path for bgm/sfx/image/icon catalog search, TTS (voice), and avatar
video, so those capabilities need `heygen` installed and authenticated. Local
tools are OPT-IN alternatives where they exist; install one to unlock its free,
private, on-device path instead of or ahead of HeyGen for that type. Only
`ffmpeg`/`ffprobe` are strictly required for the tool to run at all.

| Tool               | Serves                                                                          | Install                                                                                                                                                                                     |
| ------------------ | ------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `ffmpeg`/`ffprobe` | adopt probing, smart-grade signalstats, cut, duck bake, loudnorm                | system package (`brew install ffmpeg`)                                                                                                                                                      |
| `heygen`           | catalog (bgm/sfx/image/icon) + TTS (voice) + avatar video — the free-usage path | install through [verified HeyGen release instructions](https://developers.heygen.com/cli), then `heygen auth login --oauth` (needs >= v0.3.0)                                               |
| `mflux-generate`   | local image gen (FLUX), best-for-RAM                                            | `uv venv ~/.venvs/mflux && VIRTUAL_ENV=~/.venvs/mflux uv pip install mflux==0.9.6`                                                                                                          |
| `codex`            | image gen upsell (ChatGPT sub)                                                  | Codex CLI, logged in via ChatGPT (owns its own auth)                                                                                                                                        |
| `parakeet-mlx`     | local transcription (default ASR, best) on Apple Silicon                        | `uv venv ~/.venvs/parakeet && VIRTUAL_ENV=~/.venvs/parakeet uv pip install parakeet-mlx`                                                                                                    |
| `ltx-2-mlx`        | local video gen                                                                 | `git clone https://github.com/dgrauet/ltx-2-mlx && cd ltx-2-mlx && uv sync --all-extras`                                                                                                    |
| `npx hyperframes`  | Kokoro TTS (voice), Parakeet or whisper.cpp (transcribe), remove-background     | via the hyperframes CLI; Parakeet on macOS, Windows and glibc 2.32+ Linux: `npx hyperframes models install parakeet`; whisper.cpp is built on first use (Homebrew on macOS, else git+cmake) |

The RAM-graded local-model shortlist + exact per-tier install/invoke lives in
the CLI's bundled media-use engine, not in the standalone skill. Without a tool on PATH, its provider
prints a one-line diagnostic to stderr and resolve falls through where another
provider exists (e.g. no `mflux` -> codex image upsell; no `parakeet-mlx` -> whisper.cpp).

`heygen asset search` is a pre-launch command hidden from `heygen --help`, but it
runs; providers tag requests with the allowlisted `X-HeyGen-Client-Source` header
(v0.3.0+).


<!-- ===== FILE: hyperframes/media-use/references/telemetry-dashboard.md ===== -->

# media-use usage dashboard

Reproducible definition of the media-use usage dashboard. The dashboard answers
"how much is media-use used, for what, is reuse working, and what can't it
satisfy" from the telemetry `scripts/lib/telemetry.mjs` already emits. Build it
in an authorized HyperFrames analytics project; this doc is the source of truth
so it can be recreated. Local complement: `resolve --stats` (same questions,
from `.media/` + `~/.media`, no dashboard access needed).

## Identity (see `scripts/lib/telemetry.mjs`)

Events attribute to the **same person as the hyperframes CLI and studio**
— the shared install id in `~/.hyperframes/config.json` (`anonymousId`), stitched
to the HeyGen account (`$identify`, `distinct_id` = email/username) on sign-in.
Not fully anonymous by design; pseudonymous before sign-in, account-linked after.
`$ip:null`. Opt-out: `HYPERFRAMES_NO_TELEMETRY=1` / `DO_NOT_TRACK=1` (also CI, dev).

## Event catalog (verified present in-project)

Every event carries `surface: "media-use"`. Event **properties are coarse** —
never intent text, file names, or paths.

| Event                                                                  | Fires on                                  | Key properties                                                         |
| ---------------------------------------------------------------------- | ----------------------------------------- | ---------------------------------------------------------------------- |
| `media_use_resolve`                                                    | a resolve that produced/returned an asset | `type`, `source`, `provider`, `via`, `local_only`, `provider_override` |
| `media_use_resolve_miss`                                               | a resolve that found nothing              | `type`, `local_only`, `provider_override` (no intent)                  |
| `media_use_candidates`                                                 | `--candidates` / `--dry-run` listing      | `type`, counts                                                         |
| `media_use_doctor_run`                                                 | `--doctor`                                | `ok`, `checks_failed`, `failed[]`                                      |
| `media_use_compare`                                                    | `grade-compare` / `compare`               | `command`, `cells`, `truncated`, `total`, `render_ready_timed_out`     |
| `media_use_transcribe` · `media_use_duck` · `media_use_transcript_cut` | audio-engine ops                          | op-specific                                                            |

## Dashboard tiles

1. **Invocation volume** — `query-trends`, count of `media_use_resolve` over time (daily). "How much."
2. **By media type** — `media_use_resolve` broken down by `type` (bgm/sfx/image/icon/logo/voice/grade/lut). "For what."
3. **Resolve hit-rate** — trends formula: `A / (A + B)` where A = `media_use_resolve`, B = `media_use_resolve_miss`. "Is the catalog covering needs."
4. **Provider mix** — `media_use_resolve` broken down by `provider`; a second tile by `via` (`url` / `params-fallback` / `params`) to catch CDN→params LUT downgrades.
5. **Top misses** — `media_use_resolve_miss` broken down by `type` (the tuning signal — pair with local `resolve --stats`, which also shows the missed _intents_ that telemetry deliberately omits).
6. **Doctor health** — `media_use_doctor_run` broken down by `failed[]` (which dependency check fails most) + `checks_failed` distribution.
7. **Compare cost** — `media_use_compare` by `command`, plus `truncated` / `render_ready_timed_out` rates (observe before lifting the 16-cell cap).
8. **Adoption (optional)** — if the `first_run` property ships (plan U5), segment `media_use_resolve` first-run vs repeat.

## Recreate in an analytics dashboard

For each tile, confirm the event/property schema, build its trend or breakdown,
then add it to a dashboard. Keep names prefixed `media-use:` so the dashboard is
greppable. Cross-surface note: because identity is shared with CLI/studio, you
can also break these down by the same person across `cli_command*` and `studio:*`
events.
