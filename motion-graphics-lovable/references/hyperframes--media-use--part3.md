

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
