

<!-- ===== FILE: hyperframes/hyperframes-cli/GUIDE.md ===== -->

---
name: hyperframes-cli
description: >
  Use the HyperFrames CLI development loop: init, add, catalog, capture, lint, check, snapshot,
  compare, grade-compare, preview, play, present, beats, keyframes, single or batch render, publish,
  cloud, cloudrun, feedback, lambda, doctor, browser, info, upgrade, skills, compositions, timeline, history, clean, docs,
  benchmark, telemetry, transcribe, auth, tts, and remove-background. Also use when diagnosing build
  or render failures. validate, inspect, and layout are deprecated aliases; use check. Covers local,
  HeyGen-hosted cloud, AWS Lambda, and Google Cloud Run rendering.
---

**Plugin installs:** Before setup or freshness commands, follow [plugin execution rules](../hyperframes/references/plugin-installation.md) when this skill is inside a HyperFrames plugin. Standalone installs keep the update instructions below.

# HyperFrames CLI

Run commands as `npx hyperframes ...` unless project instructions provide a wrapper. Obey the wrapper when present. The CLI requires Node.js 22 or newer and FFmpeg.

## Development loop

1. **Scaffold:** `npx hyperframes init <project>` (centered blank). Or capture a site. Pass `--example=<name>` only to start from a named example.
2. **Find the move:** if the request names an asset, sound, image, voice or fast visual edit, resolve it through `/media-use` before proposing a plan. Otherwise, before authoring motion by hand, search for a primitive that already does it: `npx hyperframes catalog --query "reveal a headline one line at a time"`. Ask for the effect you want rather than the mechanism you have in mind. Install with `npx hyperframes add <name>` (see `/hyperframes-registry`). Author by hand only once nothing fits.
3. **Author:** write the composition using `/hyperframes-core`. To know what is on a project's timeline (tracks, clips, starts, ends, what plays), run `npx hyperframes timeline --json` instead of reading `index.html` and every sub-composition file: nested rows carry absolute main-timeline `absStart`/`absEnd` and their owning `file`, not just their local, per-sub-composition time. Prefer `--json` over the text form; it costs fewer tokens for the same or better correctness. See `references/upgrade-info-misc.md` for one-liners that answer common questions without reading the whole output.
4. **Get fast feedback while editing:** run `npx hyperframes lint` after the first HTML pass and after structural changes.
5. **Run the final gate:** run `npx hyperframes check`; it reruns lint before opening the browser. Do not prepend a redundant standalone lint invocation. Add `--snapshots` for annotated overview frames and finding crops.
6. **Inspect sub-compositions:** when `index.html` mounts `data-composition-src`, capture midpoint snapshots and inspect each mounted scene. Inspect the opening 30 seconds and reported problem times at full resolution; zoom into fine geometry, text, and WebGL edges rather than judging a contact sheet alone.
7. **Open the final Studio preview:** run `npx hyperframes preview --background`, verify the URL returns HTTP 200, hand the timeline project URL to the user, and ask whether to revise or render. Keep it alive until review ends.
8. **Render only after approval:** use `--quality draft` while iterating, `--quality looks` for the first real encode (the CLI default), and `--quality delivery` for final delivery.
9. **Hand the project to the desktop app (on offer):** when the render's Framey line ends in `hyperframes open …`, offer `npx hyperframes open [dir]`. It opens the project in the HyperFrames desktop app and adds it to Home; under Claude Code, Codex or Grok its chat picks up this conversation. Without the app it exits 1 and prints the download link. `--json` for agents. When `open` says to run `catch-up` once the person is back, or any command ends with a line naming it, run `npx hyperframes catch-up [dir]` before your next change: it lists what was asked and changed in the app since the hand-off. An older CLI has no `catch-up`.
10. **Verify the output:** confirm the file exists and is non-empty. Read the render summary's second line (`beginframe` vs `screenshot`, GPU, stage timings). `screenshot` + `software gpu` on Linux is the slow path. `ffprobe -v error -show_format -show_streams` and compare duration (and fps if the brief set it) to the root `data-duration`. Visually inspect decoded output frames at the same times as the preview, including close-ups; a successful check or encode does not certify the pixels inside a canvas.

<!-- history (trial): remove this block together with the command -->

### Project history in your turn

Every write to the project is kept as an entry that can be undone. Use it at two moments only, never on every step:

- **Start of a turn:** `npx hyperframes history begin --who <your-name> --label "<what you are about to do>"`, then `npx hyperframes history --since mine --who <your-name>` to see what the person changed since your last turn. Build on their edits; never overwrite them.
- **A check failed, or the person says it got worse:** `npx hyperframes history undo --who <your-name>` undoes your newest turn and leaves the person's edits alone. Do not hand-edit back. On a conflict it exits 2 and prints both choices.

End each turn with `npx hyperframes history end`, so your writes read as yours, not as "Changed outside the app". While a turn is open, every write to the project counts as yours until 10 minutes pass without one; after that the turn has ended by itself.

<!-- /history (trial) -->

## Mandatory creator-edit cross-references

- Before authoring or diagnosing a zoom, punch-in/punch-out, reframe, camera
  move, or any keyframe motion, read `/hyperframes-keyframes` first.
- Before `hyperframes keyframes`, read `/hyperframes-keyframes`; the command
  surfaces animation trajectories and does not diagnose clip cuts.
- For a cut, trim, splice, reorder, or source timing edit, read
  `/hyperframes-core` and use its clip/timeline contract.
- For fade-in/fade-out, crossfade, track gain, volume automation, ducking,
  voiceover carve, or FX on placed audio, read `/hyperframes-audio`. Load core
  alongside it when clip placement or picture timing also changes.
- A request naming an asset, sound, image, voice or fast visual edit resolves through `/media-use` before a plan is proposed.
  Copy creator edit markup from `/hyperframes-core` → `references/creator-editing-recipes.md`.

```bash
# Fast iteration check; repeat while authoring as needed.
npx hyperframes lint

# Required final gate; includes lint.
npx hyperframes check
npx hyperframes preview --background
npx hyperframes render --quality looks --output out.mp4
test -s out.mp4
ffprobe -v error -show_format -show_streams out.mp4
```

`check` runs lint first, then uses one browser session and one seek pass to audit runtime errors, failed requests, layout, `*.motion.json` assertions, and WCAG contrast. Persistent findings gate the exit code; transient entrance or exit findings are informational. Use `--strict` to gate warnings. `validate`, `inspect`, and `layout` remain aliases for compatibility but must not appear in new instructions or scripts.

## Preview before render

Open the final composition preview (`#project/<name>`) only after `check` passes, to review the assembled timeline. The plan in chat and the storyboard board (`boards/storyboard.html`, format in `hyperframes-creative/references/storyboard-recipe.md`) are not approval of the final video. Rendering always requires the final approval defined by `hyperframes/references/review-loop.md`.

## Sub-composition smoke test

Static audits cannot catch every mount failure. When the project uses sub-compositions, capture at least one visible midpoint for each host slot:

```bash
npx hyperframes snapshot --at <t1>,<t2>,<t3>
# For multiple samples within one scene or interval:
npx hyperframes snapshot --composition <data-composition-id> --frames 8
npx hyperframes snapshot --range 3:5 --frames 8
```

Treat tiny unstyled content, canvas-sized icons, missing hero elements, or timeline-registration timeouts as render-blocking mount defects. See `hyperframes-core/references/sub-compositions.md` for the corresponding fixes.

## Agent conventions

- **Search the catalog before writing motion by hand.** `npx hyperframes catalog --query "<the beat, in plain English>"`. Search is entirely local: there is no hosted tier, no account, and the query text is never sent anywhere. By default it ranks on vocabulary shared with the item's name, title, description and tags, which misses any phrasing that does not reuse the catalog's own wording. Add `--on-device` to rank by meaning instead (see the offline tier below).
- **Query in English even when the video is not.** Both tiers index an English catalog, so a query in another script produces no searchable terms and returns nothing. Describe the move in English; the on-screen copy stays in whatever language the video needs. `No searchable words in query` means exactly this and is not a missing component, so do not report it as a catalog gap.
- **Read which tier answered; never infer it from results appearing.** With `--json` the envelope carries `query`, `tier` (`on-device` or `words`), `tier_detail`, `dropped`, `unindexed`, `shown`, `total` and `results`, plus `top_score` when the answering tier produces one and `warnings` when a tier was asked for and could not run, or when a search returned nothing and a better tier is still waiting on someone's consent. A weak result on `words` is expected; the same result on `on-device` is a bug. `top_score` is on-device only and has no threshold behind it: the ranker returns the whole catalog in some order for every query, so read it as evidence rather than as a pass or fail.
- **`dropped` and `unindexed` are opposite skews between the registry and the on-device index, and rewording the query fixes neither.** `dropped` counts ranked names this registry cannot install, so the strongest matches are the ones being lost. `unindexed` counts registry moves the index cannot see at all, which no query can ever return. Refreshing the registry is not the answer to either: its manifest carries a 24h TTL and heals itself, while the vectors are a separately published artifact fetched into `~/.hyperframes/catalog/`. Re-running with `--on-device` refetches that index when `unindexed` is above zero, so that is the remedy to hand the user. A pure over-coverage skew (`dropped` above zero while `unindexed` is zero) does not trigger the refetch; clearing `~/.hyperframes/catalog/` is the only way out of that one. Both counts are of names rather than of results, so either can exceed `total`.
- **When a search comes back with nothing worth installing, say so.** `npx hyperframes feedback --search-miss "<the query you ran>" --wanted "<the move you needed>" --tier <the tier that answered>`. You do not have to assemble that line: `catalog --query` prints it pre-filled, and every `--json` search envelope carries it as `report_gap` with the query and tier already correct — fill in `--wanted` and send. This is the only path that sends a query anywhere, and it is a separate deliberate command precisely so plain `catalog --query` keeps its promise of sending nothing. **Report on either tier**, whenever the results do not do the thing; do not hold out for the on-device tier, which needs a consented 33 MB download and is therefore off in most agent runs — waiting for it means never reporting at all. The tier rides along in the report, so a vocabulary miss stays distinguishable from a meaning miss without you having to judge which one you hit. What comes back is a list of moves the catalog does not have yet, read directly rather than guessed from install counts, so the phrasing that matters is the effect you wanted, not the item name you imagined. It carries no rating and never lands in the rating metric.
- **Offer the offline tier; never enable it silently.** A one-time ~33 MB download (a quantized ONNX build of `bge-small-en-v1.5` plus its tokenizer, pinned to a fixed revision) and the catalog vectors from the registry, both cached under `~/.hyperframes/`, neither added to the project or any package. Once cached it ranks by meaning with nothing sent. Say the size out loud and let the person decide, then pass `--on-device` (with `-y` to skip the prompt) once they agree. The interactive offer only fires on a TTY. Under `--json` there is no prompt, but a search that found nothing puts the same ask in `warnings`, so read that array and put the decision to the user yourself. When the person asks what the download is, why this model, or what leaves the machine, point them to https://hyperframes.heygen.com/developers/catalog-search.

- Prefer `--json` for agent and CI calls. Server-mode `render`, `preview`, and `play` do not provide ordinary JSON output; `preview --selection --json` and `preview --context --json` are query-mode exceptions.
- `doctor --json` always exits zero. Gate on its payload:

  ```bash
  npx hyperframes doctor --json | jq -e '.ok' >/dev/null
  ```

- Non-TTY mode is automatic and scaffolds the centered blank. Pass `--example` only to start from a named example. Use `--non-interactive` to force flag-only mode on a TTY.
- Use one `HYPERFRAMES_RUN_ID` for all commands in the same verification loop.
- When disk is tight, run `npx hyperframes clean` (`--dry-run` to list first); it removes what dead renders left and idle caches that rebuild themselves, never outputs, sources or anything a running render uses. Write disposable QC frames to a temp dir, then remove only that owned directory. Managed snapshot runs retain the newest 10 plus current/latest/rendered evidence; active captures and runs younger than 24 hours are protected. Copy intentional before/after evidence outside managed storage before it ages out. Never delete `.hyperframes` wholesale: it also holds project history.
- Use `--strict`, `--strict-all`, and `--strict-variables` when the corresponding warnings, variables, or CI conditions must gate the render.
- For `shader_unbounded_cosine_pow`, clamp the cosine to `[0, 1]` before `pow(1 - cosine, exponent)`; a lower-only `max` is insufficient. Follow `/hyperframes-animation` → `adapters/three.md` for the source fix and affected-GPU preview/export verification. Lint only recognizes static shader expressions, and software rendering can miss hardware-specific invalid pixels.
- JSON paths redact the home directory as `$HOME`; do not try to reverse the redaction.
- When a hosted cloud project approaches or exceeds the 200 MB upload limit, use `cloud render --dry-run --json` and follow the `.hyperframesignore` investigation in `references/cloud.md`. Never ignore an asset merely because it is large.
- Never render merely because checks pass. Pause at the final preview and wait for approval.

## Studio-directed edits

When the user refers to “this element” or the current selection, query Studio instead of guessing:

```bash
npx hyperframes preview --context --json --context-fields selection
```

Use `selection.target.hfId` when available, otherwise its selector and source file. If the result reports `no-selection`, ask the user to click the element and rerun. Request only the context slices you need; use `--context-detail full` only for computed styles or editable text metadata. Full behavior and failure codes live in `references/preview-render.md`.

## Render choices

| Need                                     | Command                                                                       |
| ---------------------------------------- | ----------------------------------------------------------------------------- |
| Fast local iteration                     | `npx hyperframes render --quality draft`                                      |
| First real encode                        | `npx hyperframes render --quality looks --output out.mp4`                     |
| Final local delivery                     | `npx hyperframes render --quality delivery --output out.mp4`                  |
| Reproducible container render            | `npx hyperframes render --docker --strict --output out.mp4`                   |
| Local variable-driven batch render       | `npx hyperframes render --batch rows.json --output "renders/{name}.mp4"`      |
| HeyGen-hosted zero-infrastructure render | `npx hyperframes cloud render`                                                |
| Self-managed distributed AWS render      | `npx hyperframes lambda render <project> --width 1920 --height 1080 --wait`   |
| Self-managed distributed GCP render      | `npx hyperframes cloudrun render <project> --width 1920 --height 1080 --wait` |

A render stops when whatever started it stops, so a Ctrl-C or a closed terminal never leaves Chrome running. If your tool kills its whole process group when a command times out or ends, a long render dies with it. Start such a render in its own process group with `HYPERFRAMES_RENDER_DETACHED=1`, for example `bash -c 'set -m; HYPERFRAMES_RENDER_DETACHED=1 npx hyperframes render --output out.mp4 < /dev/null > render.log 2>&1 &'` (works on macOS and Linux), then check the log and the output file instead of waiting on the command.

Skill attribution is automatic — the examples above need no `--skill`. A project scaffolded by a workflow (`hyperframes init --skill=<workflow>`) records its owning skill in `hyperframes.json`, and every later render inherits it on anonymous telemetry: re-renders, `npm run render`, and `--batch` alike. Pass `--skill=<slug>` explicitly only to stamp a project that was not created through a workflow (its first render then persists it).

Use cloud rendering when the user wants hosted rendering without local Chrome, FFmpeg, or AWS. Use Lambda only when AWS ownership is a requirement. Use Cloud Run only when GCP ownership is a requirement. Read the matching reference before running any cloud path.

After verifying a successful render, send one feedback report unless telemetry is disabled or the user opted out:

```bash
npx hyperframes feedback --rating <0-10> --comment "<specific result or friction>"
```

Keep clean-run feedback concise. For any bug or friction, capture a **reproduction packet** before submitting; do not send only a symptom summary. Include the rerunnable command (relative to the project directory — feedback is submitted to a public channel, so do **not** paste absolute paths, home-directory prefixes, or user/machine identifiers), expected versus actual behavior, exact error (also strip absolute paths from stack traces — keep basename + line, drop the leading directory), whether output completed/fell back/failed, workaround, and repro-project status. For a rating ≤ 7 that describes a visual defect (black frame, flicker, corrupt output, wrong frame, blank output, other visual anomaly), also include a `COMPOSITION_STRUCTURE:` block — a privacy-preserving structural anatomy (element census + attribute presence + timeline shape) so maintainers can pattern-match against known bug families without the composition ZIP. Agents auto-fill this via the composition-census helper; the human user does not fill it by hand. If the issue did not reproduce again, say so and still include the last failing command and logs. Use `--file-issue` only with consent: it publishes a minimal reproduction to a public URL. The required packet format and privacy warning live in `references/preview-render.md`.

Two more reports are a `--comment` with no `--rating`, so they never count in the rating metric. Send them unless telemetry is disabled or the user opted out, under the same privacy rules:

- **Missing feature.** Whenever the person asks for something HyperFrames or the host app cannot do, or can only do with a workaround, send one report per ask: `npx hyperframes feedback --comment "MISSING FEATURE: <what the person asked for, in their words, with names, clients, figures and paths left out> | WORKAROUND: <what you did instead, or none>"`. The report is about the capability they wanted, never their content or anything private. A catalog search that found nothing goes to `--search-miss` instead.
- **Host app.** When `HYPERFRAMES_CLIENT` is set, the CLI is running inside a host app. When that app itself gets in the way (a panel, button, preview or export that misbehaves), send `npx hyperframes feedback --comment "HOST APP: <what happened>"` with the reproduction packet.

## Read the matching reference before running a command

The following references and owning skills are mandatory command contracts, not optional background reading. Before running a command in the table, read its matching row.

| Need                                                                                               | Reference                             |
| -------------------------------------------------------------------------------------------------- | ------------------------------------- |
| `init`, `capture`, `skills`                                                                        | `references/init-and-scaffold.md`     |
| `lint`, `check`, motion sidecars, `snapshot`                                                       | `references/lint-validate-inspect.md` |
| `compare`, `grade-compare`, variable-driven `render --batch`                                       | `references/compare-and-batch.md`     |
| `beats` for an existing project's Studio beat grid                                                 | `references/beats.md`                 |
| `preview`, `play`, `render`, `publish`, Studio context, feedback                                   | `references/preview-render.md`        |
| `doctor`, browser management                                                                       | `references/doctor-browser.md`        |
| `auth`, HeyGen-hosted cloud rendering, and template variables                                      | `references/cloud.md`                 |
| AWS Lambda deployment and rendering                                                                | `references/lambda.md`                |
| Google Cloud Run deployment and rendering                                                          | `references/cloudrun.md`              |
| `info`, `upgrade`, `compositions`, `timeline`, `docs`, `benchmark`, telemetry, media preprocessing | `references/upgrade-info-misc.md`     |

For composition variables, also read `/hyperframes-core` → `references/variables-and-media.md`. For `hyperframes add` and `hyperframes catalog`, use `/hyperframes-registry`. Before `hyperframes present`, read `/slideshow`; before `hyperframes keyframes`, read `/hyperframes-keyframes`. For TTS, transcription, captions, or background removal choices, use `/media-use`.

The specialized commands are deliberately documented by their owning workflows:

```bash
npx hyperframes present <project-dir> --port 3004 --no-open
npx hyperframes beats <project-dir> --json
npx hyperframes keyframes <project-dir> --json
npx hyperframes media-treatment --capabilities
npx hyperframes figma asset KEY:10-20
```

`present` serves a navigable deck with presenter and audience synchronization. `beats` is the standalone Studio beat-grid utility defined in `references/beats.md`. `keyframes` surfaces seek-safe animation and motion-path diagnostics. `media-treatment` discovers, applies, and clears deterministic looks on local footage — start with `--capabilities` for the overview and `--capability <name>` for one family; `/media-use` owns which treatment a brief is asking for. `figma` imports over the REST API with the `asset`, `tokens`, and `component` subcommands and needs `FIGMA_TOKEN`; motion and shader import have no REST endpoint and are agent-only, so `/figma` owns those.

## Commands you should not run

Two entries in `hyperframes --help` are not part of the authoring loop, and reaching for them wastes a turn:

- `events` is the telemetry endpoint skills use to report their **own** invocation, ideally from a bundled script. It emits an anonymous event and exits 0 no matter what you pass it. It is not a way to read telemetry back, and an agent has no reason to call it by hand.
- `validate`, `inspect`, and `layout` are deprecated aliases kept for old scripts. `check` is the one that is maintained, and it is what every reference in this skill assumes.

## Remaining harness usage

Run `npx hyperframes usage --json` at the start of a video workflow and again at milestones such as after drafting and before rendering. A fresh read at handoff can serve as the start read. Use `--harness claude-code`, `--harness codex`, or `--harness grok` to select explicitly.

Known results contain `status: "known"`, `harness`, `planTier`, `session`, `weekly`, and `spend`. Each available window contains `usedPercent`, `remainingPercent`, and `resetsAt`; an unavailable window is `null`. `planTier` is the readable subscription tier when available, otherwise `null`. Claude Code reports its shared five-hour and weekly windows; a spend-metered plan (such as Enterprise) has neither and reports `spend`, the share of its billing-period spend limit already used, with `resetsAt: null`. Codex reports its shared session and weekly windows when available. Grok reports its included weekly allowance with `session: null`. Only Claude Code reports `spend`; it is `null` elsewhere. When no window is available the result is `status: "unknown"` with `reason: "no_usage_windows"`.

Unknown results contain `status: "unknown"` and a token-free `reason`. Missing, expired, unsupported, ambiguous, or unreadable logins and unavailable provider responses return unknown. Report the unknown state without guessing allowance. The command reads existing credentials without refreshing or rewriting them and emits no tokens or telemetry. Usage is a snapshot; it does not reserve allowance or estimate the next video's cost. Keep scope and workflow choices with the user.


<!-- ===== FILE: hyperframes/hyperframes-cli/references/beats.md ===== -->

# Generate a project beat grid

Use `hyperframes beats` when an existing HyperFrames project needs the Studio-compatible beat file for its music track. This is a CLI utility, not a complete video workflow.

```bash
npx hyperframes beats
npx hyperframes beats ./my-video
npx hyperframes beats ./my-video --json
```

The project must contain a local music `<audio>` source. Mark it with `data-timeline-role="music"`; an id containing `music`, `bgm`, or `soundtrack` is also recognized. The command decodes that file with ffmpeg, tracks its beats, and writes `beats/<audio-relative-path>.json`.

If the track has no steady beat, the command fails and writes nothing. If ffmpeg is missing, run `npx hyperframes doctor`.

For a complete beat-synced video, route through `/music-to-video`. That workflow owns a different audio-driven pipeline and its `audiomap.json`; do not replace its analyzer with this Studio utility.


<!-- ===== FILE: hyperframes/hyperframes-cli/references/cloud.md ===== -->

# cloud — HeyGen-hosted rendering (zero-infra)

`hyperframes cloud render` renders a composition on HeyGen's managed cloud. The CLI zips the project, uploads it, runs the render on HeyGen's infrastructure (Chromium + FFmpeg), and downloads the finished video. Nothing to deploy, and no Chrome/FFmpeg/AWS to manage; you pay per credit.

```bash
npx hyperframes auth login            # one-time sign-in
npx hyperframes cloud render          # zip, upload, render, download
```

## When to use managed cloud, Lambda, Cloud Run, or local

- **`hyperframes render`** (local): fastest iteration loop, use while authoring.
- **`hyperframes cloud render`**: zero-infra. HeyGen runs the render and you pay per credit. This is the default answer to "render in the cloud" when you don't want to manage Chrome/FFmpeg/AWS.
- **`hyperframes lambda render`**: bring-your-own-AWS distributed rendering with chunked parallelism. Only worth it when you've already invested in AWS (see `lambda.md`).
- **`hyperframes cloudrun render`**: bring-your-own-GCP distributed rendering through Cloud Run and Workflows. Use only when GCP ownership is explicit (see `cloudrun.md`).

## Authentication

Cloud rendering needs a HeyGen credential, stored at `~/.heygen/credentials` (`0600`) and shared with the [`heygen` CLI](https://github.com/heygen-com/heygen-cli): sign in with one and the other picks up the session.

```bash
npx hyperframes auth login              # OAuth 2.0 + PKCE, opens the browser
npx hyperframes auth login --api-key    # CI/headless: hidden prompt, or pipe: echo "$HEYGEN_API_KEY" | ... --api-key
npx hyperframes auth status             # active credential source, identity, billing snapshot
                                        #   exit 0 = signed in and verified; exit 1 = not signed in,
                                        #   or the credential was rejected — signed-out exit 1 is the
                                        #   normal offline state (scripts: `auth status || echo offline`),
                                        #   not a command failure
npx hyperframes auth refresh            # force-refresh an OAuth token before a long job
npx hyperframes auth logout             # clear the stored credential
```

Credential resolution order (first match wins): `HEYGEN_API_KEY`, then `HYPERFRAMES_API_KEY`, then `HEYGEN_ACCESS_TOKEN` (an OAuth token a host app injects; never refreshed or saved), then `~/.heygen/credentials`. Point at a different backend with `HEYGEN_API_URL` (default `https://api.heygen.com`).

## The render pipeline

`cloud render` runs end-to-end:

1. **Resolve the project**: a local directory (default `.`), or skip the upload with `--asset-id` / `--url`.
2. **Auto-detect aspect ratio** from the entry HTML's `data-width`/`data-height`.
3. **Zip** the project (same ignore set as `hyperframes publish`, including `.hyperframesignore`).
4. **Upload** the zip through the direct-to-S3 asset flow, yielding an `asset_id`.
5. **Submit** the render to `POST /v3/hyperframes/renders`, yielding a `render_id`.
6. **Poll** `GET /v3/hyperframes/renders/{id}` until it completes or fails (skip with `--no-wait`).
7. **Download** the signed video URL to disk.

## Archive size and `.hyperframesignore`

The direct-upload limit is 200 MB. HyperFrames automatically excludes root-level `renders/` and `snapshots/`, along with its existing development exclusions such as `.git`, `node_modules`, `dist`, `.next`, `coverage`, and dotfiles. Add project-specific gitignore-style rules to `<project>/.hyperframesignore` when other generated or intermediate assets are not required at render time. The same rules affect `hyperframes publish`.

Inspect the exact archive without authenticating, uploading, spending credits, or starting a render:

```bash
npx hyperframes cloud render <project> --dry-run --json
```

The result reports compressed `size_bytes`, `file_count`, the 200 MB limit, and the ten largest included files.

When a cloud upload reports a size-limit error, agents must use this workflow:

1. Run the dry-run command and inspect the largest included files and directories.
2. Classify obvious generated outputs first: old renders, extra snapshot/contact-sheet directories, caches, exported previews, and source media used only to produce final assets.
3. Before excluding anything else, search `src`, `href`, `url()`, `data-composition-src`, JavaScript strings, manifests, and variable-driven paths across every HTML, CSS, and JavaScript entry.
4. Preserve existing `.hyperframesignore` comments and rules. Add the narrowest verified-unneeded root-relative paths; prefer an exact directory or file over a broad wildcard.
5. Never ignore `index.html`, the selected composition, mounted sub-compositions, fonts, images, audio, video, scripts, or manifests merely because they are large. Never ignore all of `assets/`.
6. Rerun dry-run until the archive is below the limit, then run `npx hyperframes check`. Remember that `check` sees the source directory, so it cannot prove a dynamically computed asset path remains in the filtered archive; the reference audit is still required.

Example:

```gitignore
# Additional generated verification passes
/snapshots2/
/snapshots3/

# Master used only to produce the final background clips
/assets/bg-pattern.mp4
```

Rules support comments, globs, and negation. A later rule can override a default, for example `!/snapshots/` when that directory intentionally contains render inputs.

## Render options

| Flag                   | Default                     | Meaning                                                                                                                        |
| ---------------------- | --------------------------- | ------------------------------------------------------------------------------------------------------------------------------ |
| `--fps`                | `30`                        | Frames per second, 1–240.                                                                                                      |
| `--quality`            | `standard`                  | `draft`, `standard`, or `high`.                                                                                                |
| `--format`             | `mp4`                       | `mp4`, `webm`, or `mov` (webm/mov carry alpha).                                                                                |
| `--resolution`         | `1080p`                     | `1080p` or `4k` (4k billed at 1.5×).                                                                                           |
| `--aspect-ratio`       | auto                        | `16:9`, `9:16`, or `1:1`. Auto from a local project's `data-width`/`data-height`; defaults to `16:9` for `--asset-id`/`--url`. |
| `--composition` / `-c` | `index.html`                | Entry HTML file inside the zip.                                                                                                |
| `--output` / `-o`      | `renders/<render_id>.<ext>` | Local download destination.                                                                                                    |
| `--dry-run`            | off                         | Build and inspect a local project zip without authenticating, uploading, or rendering.                                         |

```bash
npx hyperframes cloud render . \
  --composition compositions/intro.html \
  --output ./renders/intro.mp4

npx hyperframes cloud render --quality high --fps 60
```

`--resolution 4k` cannot combine with `--format webm`/`mov`: the 4k supersampling path has no alpha channel. Render 4k as mp4, or render alpha at native resolution.

## Templates and variables

Cloud rendering supports [composition variables](../../hyperframes-core/references/variables-and-media.md#variables): declare `data-composition-variables` on the composition, then fill them at render time.

```bash
npx hyperframes cloud render --variables '{"title":"Q4 Recap","theme":"dark"}'
npx hyperframes cloud render --variables-file ./vars.json
npx hyperframes cloud render --variables '{"title":"Q4 Recap"}' --strict-variables
```

For a **local project** the CLI validates `--variables` against the declared schema _before_ uploading. For `--asset-id`/`--url` the schema lives server-side, so mismatches surface as a `hyperframes_project_invalid` API error.

**Upload once, re-render many** is the idiomatic template loop: render a local project to get its `asset_id`, then re-submit against that asset with new values (no re-zip, no re-upload).

```bash
npx hyperframes cloud render ./card-template                              # note the asset_id printed on upload
npx hyperframes cloud render --asset-id asst_abc123 --variables '{"name":"Ada"}'
npx hyperframes cloud render --asset-id asst_abc123 --variables '{"name":"Linus"}'
```

For high-volume personalized batches, both self-managed paths provide JSONL fan-out: AWS Lambda (`lambda.md`) and Google Cloud Run (`cloudrun.md`). The full variables schema (types, declarative bindings, sub-composition overrides, precedence) lives in the `hyperframes-core` skill.

## Fire-and-forget and webhooks

By default the CLI blocks, polls, and downloads. Combine `--no-wait` (submit and exit with just the `render_id`) with `--callback-url` (HTTPS webhook on terminal status) for true fire-and-forget:

```bash
npx hyperframes cloud render --callback-url https://example.com/hf-hook --no-wait
#    Poll later with: hyperframes cloud get hfr_def456
```

| Flag              | Meaning                                             |
| ----------------- | --------------------------------------------------- |
| `--no-wait`       | Submit and exit immediately; print the `render_id`. |
| `--callback-url`  | HTTPS webhook fired when the render terminates.     |
| `--callback-id`   | Opaque tracking ID echoed in webhook payloads.      |
| `--poll-interval` | Poll cadence in seconds (default `10`).             |
| `--max-wait`      | Max poll duration in minutes (default `60`).        |

## Managing renders

```bash
npx hyperframes cloud list                 # recent renders (--limit, --token, --all)
npx hyperframes cloud get hfr_def456       # full detail + short-lived signed video_url
npx hyperframes cloud delete hfr_def456    # soft-delete (--no-confirm to skip the prompt)
```

`video_url` and `thumbnail_url` are short-lived presigned URLs, so re-fetch with `cloud get` rather than caching them.

## Safe retries

The CLI transparently retries a `401` by force-refreshing the OAuth token and replaying. That's harmless for reads, but the zip upload (`POST /v3/assets`) is **not** idempotent: a blind retry creates a duplicate asset and bills twice. Pass `--idempotency-key` so retries are safe:

```bash
npx hyperframes cloud render . --idempotency-key "$(uuidgen)"
```

The key is forwarded to both upload and submit (the server scopes idempotency per-endpoint, so reusing one value is safe). Use any opaque string in `[A-Za-z0-9_:.-]`, 1–255 chars.

Full flag reference: docs `/deploy/cloud` and `/packages/cli#hyperframes-cloud`.


<!-- ===== FILE: hyperframes/hyperframes-cli/references/cloudrun.md ===== -->

# Cloud Run rendering on Google Cloud

Use `hyperframes cloudrun` only when the user explicitly wants self-managed Google Cloud infrastructure. It deploys Cloud Run, Workflows, and Cloud Storage. For a managed default use `hyperframes cloud`; for AWS use `hyperframes lambda`.

## Prerequisites

- `gcloud` is authenticated and the target project has billing enabled.
- Terraform 1.5 or newer is on `PATH`.
- Docker or permission to use Cloud Build is available.

## Lifecycle

```bash
npx hyperframes cloudrun deploy --project <gcp-project> --region us-central1
npx hyperframes cloudrun sites create ./project
npx hyperframes cloudrun render ./project --width 1920 --height 1080 --wait
npx hyperframes cloudrun progress <execution-name>
npx hyperframes cloudrun destroy --project <gcp-project>
```

`deploy` enables the required Google APIs, builds or accepts a container image, applies the bundled Terraform module, and stores the resulting coordinates in `~/.hyperframes/cloudrun-state.json`. Use deploy flags such as `--image`, `--repo`, `--cpu`, `--memory`, `--max-instances`, and `--timeout` only when the infrastructure needs those overrides.

`sites create` uploads a content-addressed project archive for reuse by `render-batch`; pass its `--site-id` to that command to skip the batch upload. Single `cloudrun render` currently resolves the project from its directory and does not consume `--site-id`. Both render commands require `--width` and `--height`; supported output formats are `mp4`, `mov`, `png-sequence`, and `webm`. Use `--output-resolution 4k` to supersample an authored composition without changing its layout dimensions.

Common render flags are `--fps 24|30|60`, `--quality draft|standard|high`, `--codec h264|h265` for MP4, `--chunk-size`, `--max-parallel-chunks`, `--target-chunk-frames`, `--render-id`, `--output-key`, `--wait`, and `--wait-interval-ms`. Use `--json` for machine-readable output.

For a variable-driven single render:

```bash
npx hyperframes cloudrun render ./template \
  --width 1920 --height 1080 \
  --variables-file ./alice.json \
  --strict-variables \
  --wait
```

Use exactly one of `--variables` and `--variables-file`. Read [`variables-and-media.md`](../../hyperframes-core/references/variables-and-media.md#variables) for the composition-side contract.

## JSONL batches

```bash
npx hyperframes cloudrun render-batch ./template \
  --batch ./users.jsonl \
  --width 1920 --height 1080 \
  --max-concurrent 10 \
  --site-id <site-id> \
  --json
```

Each nonblank line must contain an `outputKey`; `variables` is optional:

```json
{ "outputKey": "renders/alice.mp4", "variables": { "name": "Alice" } }
```

- `--max-concurrent` defaults to `50` and limits in-flight executions. `--max-parallel-chunks` separately limits chunks inside one render.
- `--dry-run` parses the file and prints `would-start` rows without starting executions.
- The template uploads once unless `--site-id` is supplied.
- Per-entry start errors remain visible and make the command exit nonzero.
- Do not rely on `--strict-variables` for `cloudrun render-batch`: the current command accepts the flag but does not validate batch rows. Validate the JSONL variable objects against the composition schema before dispatch. The strict gate does work for single `cloudrun render`.

`render` without `--wait` returns an execution name. Use `cloudrun progress <execution-name>` until it succeeds, then verify the reported GCS output. `destroy` removes the Terraform-managed stack and its scratch bucket; preserve any deliverables that must outlive the stack.


<!-- ===== FILE: hyperframes/hyperframes-cli/references/compare-and-batch.md ===== -->

# Compare and batch rendering

Use these commands for deliberate visual comparison or variable-driven template output. They do not replace `lint`, `check`, final preview approval, or output verification.

## Contents

- [Compare projects or variants](#compare-projects-or-variants)
- [Compare color grades](#compare-color-grades)
- [Batch template renders](#batch-template-renders)

## Compare projects or variants

Render the same timestamp from two or more project directories or HTML files into one labeled contact sheet:

```bash
npx hyperframes compare <path-a> <path-b> [<path-c> ...] \
  --at <seconds> \
  --labels baseline,candidate \
  --out compare.png \
  --cols 2
```

Useful options:

- `--at <seconds>` selects the shared comparison time.
- `--labels <a,b,...>` labels cells in input order.
- `--out <file>` chooses the sheet path.
- `--cols <n>` controls its grid.
- `--json` returns machine-readable results.
- `--timeout <ms>` changes the per-variant render-ready timeout.

One sheet accepts at most 16 variants. Extra inputs are truncated with a warning; split larger comparisons into several runs.

`compare` is a visual review surface, not a quality gate. Run it when checking a baseline against a candidate, comparing implementation variants, or verifying that a repair preserves the intended look. Inspect the generated image; do not treat command success as visual approval.

## Compare color grades

Create grade candidates from a source frame:

```bash
npx hyperframes grade-compare \
  --for frame.png \
  --grades grades.json \
  --project . \
  --out grade-compare.png
```

`grades.json` is an array of labeled HyperFrames grading blocks:

```json
[{ "label": "warm", "grading": { "adjust": { "temperature": 0.2, "contrast": 0.1 } } }]
```

Or compare explicit LUT files:

```bash
npx hyperframes grade-compare \
  --for source.mp4 \
  --luts warm.cube,cool.cube \
  --out grade-compare.png
```

- `--for` accepts an image or a video. For video input, the command extracts the first frame.
- Supply exactly one candidate source: `--grades <json>` or `--luts <a.cube,b.cube>`.
- A neutral baseline is included by default; pass `--no-baseline` only when the baseline is not a useful reference.
- The command accepts at most 16 candidate grades. With the default neutral baseline, the sheet may contain 17 cells. Extra candidates are truncated with a warning; split larger sets into several runs.
- `--timeout <ms>` changes the render-ready timeout for the generated comparison composition.
- Use `--json` for machine-readable output.

This command helps select a grade. It does not apply the selected grade to the composition or replace `/media-use` provenance and LUT validation.

## Batch template renders

`render --batch` accepts either a JSON array of variable objects or an object with a `rows` array:

```json
{
  "rows": [
    { "name": "alpha", "headline": "Hello" },
    { "name": "beta", "headline": "Welcome" }
  ]
}
```

Declare the variables in the composition, then run:

```bash
npx hyperframes render \
  --batch rows.json \
  --output "renders/{name}.mp4" \
  --batch-concurrency 1 \
  --strict-variables
```

Batch rules:

- Do not combine `--batch` with `--variables` or `--variables-file`; each row is the variable set for one render.
- If `--output` is omitted, the generated filename includes `{index}` so rows remain unique.
- Output templates support `{index}` and row keys containing letters, numbers, `_`, `.`, or `-`. A placeholder value must be a string, number, or boolean; `null`, objects, and arrays are invalid. Missing placeholders and output collisions are errors.
- `--batch-concurrency` defaults to `1`. Raise it conservatively because each render already uses workers.
- `--batch-fail-fast` stops scheduling after the first failure. Without it, independent rows keep running and failures remain visible in the manifest.
- `--strict-variables` validates every row before rendering and aborts before output when the declared variable contract is violated.
- `--json` emits progress events suitable for agents and CI.

The command writes `manifest.json` in the common output directory and updates it throughout the run. It records each row's variables, status, output, error, and timing. Completion means the manifest has no failed rows and every completed output exists, is non-empty, and has a plausible duration.


<!-- ===== FILE: hyperframes/hyperframes-cli/references/doctor-browser.md ===== -->

# doctor, browser

Environment diagnosis and bundled-Chrome management. Run these first when a render or preview fails.

## doctor

```bash
npx hyperframes doctor
npx hyperframes doctor --json     # CI / agent output (always exit 0; gate on payload `ok`)
```

Runs independent checks and reports each as ok/warn/fail:

- **Version** — installed CLI vs latest on npm (hints upgrade when stale)
- **Node.js** — ≥ 22 required
- **CPU**, **Memory**, **Disk** — host resources
- **Environment** — env vars that affect the renderer
- **FFmpeg** / **FFprobe** — found, version, codecs
- **Chrome** — bundled or system, version, path
- **Docker** / **Docker running** — required only for `render --docker`
- **/dev/shm** — inside containers only

Run `doctor` first when:

- `render` fails with a Chrome or FFmpeg error.
- `preview` opens but the composition fails to load.
- A fresh machine has never run HyperFrames.

Common issues:

- **Missing FFmpeg** — install via `brew install ffmpeg` (macOS) or your package manager, or [configure existing binaries](#configure-ffmpeg-without-a-package-manager).
- **Missing bundled Chrome** — run `npx hyperframes browser ensure`.
- **Low memory** — close other Chromes, reduce `--workers`, or use `--quality draft`.
- **Chrome exits instantly inside an agent sandbox (macOS)** — seatbelt-style sandboxes
  (e.g. codex `workspace-write`) block Chromium's Mach port bootstrap
  (`MachPortRendezvous`; openai/codex#21292), so every Chrome — bundled, system, or
  headless shell — dies at startup. This is a host-level block, not a HyperFrames or
  Chrome install problem: compile checks and audio still pass, only rendering is
  unavailable. State the blocker and deliver the checked composition; render outside the
  sandbox or via `render --docker` / cloud rendering where available. **Do not build a
  substitute rasterizer** (magick/PIL/SVG frame pipelines) — on a blocked-browser host
  the deliverable IS the checked composition plus this blocker note, and rendering is
  handed to `--docker`, cloud, or the user. Write your final summary the moment the
  blocker is identified, BEFORE any optional fallback work: a later session failure must
  not erase the report of work already done.

### Configure FFmpeg without a package manager

Get FFmpeg and FFprobe binaries for your operating system and architecture from the [FFmpeg download page](https://ffmpeg.org/download.html). Both must be executable. You can use them without Homebrew or a system-wide installation:

```bash
export HYPERFRAMES_FFMPEG_PATH="/absolute/path/to/ffmpeg"
export HYPERFRAMES_FFPROBE_PATH="/absolute/path/to/ffprobe"
npx hyperframes doctor --json
```

Set both variables in the environment that launches HyperFrames. On Windows, point them at `ffmpeg.exe` and `ffprobe.exe` using your shell's environment-variable syntax. A configured path takes precedence over automatic discovery; a missing configured file is reported as missing.

Alternatively, put the binaries in `.hyperframes/bin/ffmpeg` and `.hyperframes/bin/ffprobe` (`.exe` on Windows), then run HyperFrames from that project's directory. Discovery checks `PATH` before this project-local directory, so use the environment variables when you need a particular build.

Verify the **FFmpeg** and **FFprobe** entries in `doctor --json` report `ok: true` and the expected paths. To gate only these encoding dependencies with `jq`:

```bash
npx hyperframes doctor --json | jq -e \
  '[.checks[] | select(.name == "FFmpeg" or .name == "FFprobe")] | length == 2 and all(.ok)'
```

The report's top-level `ok` also includes optional tools such as Docker and local voice providers; those failures do not require installing them for a local video render. Check Chrome separately with the browser commands below.

## browser

```bash
npx hyperframes browser ensure    # find or download the pinned Chrome
npx hyperframes browser path      # print the browser executable path (for scripting)
npx hyperframes browser clear     # remove the cached Chrome download
```

Manage the Chrome build HyperFrames uses for rendering. The pinned version exists because pixel output drifts across Chrome versions — using the bundled build keeps rendered output reproducible across machines.

Use `path` to embed the binary in scripts: `$(npx hyperframes browser path)`.


<!-- ===== FILE: hyperframes/hyperframes-cli/references/init-and-scaffold.md ===== -->

# init, capture, skills

<!-- registry-items: allow=blank,landscape-4k,portrait-4k,square-4k,product-launch-video,hyperframes-core,media-use -->

Scaffolding commands. Use these instead of creating files by hand — they set up the right file structure, copy media, run transcription, and install AI coding skills.

## init

```bash
npx hyperframes init my-video                                    # centered blank (TTY: wizard)
npx hyperframes init my-video --example warm-grain               # pick an example
npx hyperframes init my-video --resolution portrait
npx hyperframes init my-video --video clip.mp4                   # with video file
npx hyperframes init my-video --audio track.mp3                  # with audio file
npx hyperframes init my-video --tailwind                         # Tailwind v4 browser runtime
npx hyperframes init my-video --non-interactive                  # CI — flag-only, same blank
```

**Default depends on TTY**: in a terminal, the CLI prompts for example/options (default: centered blank). Outside a TTY (CI, agents, piped output) it auto-switches to non-interactive and scaffolds that blank. Pass `--example` only to start from a named example. Pass `--non-interactive` to force flag-only mode on a TTY.

Templates: `blank`, `warm-grain`, `play-mode`, `swiss-grid`, `vignelli`, `decision-tree`, `kinetic-type`, `product-promo`, `nyt-graph`. (The closed set of `hyperframes:example` items in `registry/registry.json` plus the bundled `blank` template. `hyperframes catalog` does not list examples — its `--type` takes only `block` or `component` — so this list has no live equivalent and is checked by `bun run lint:skills`.)

Other useful flags:

- `--resolution` — preset: `landscape` (1920×1080), `portrait` (1080×1920), `landscape-4k`, `portrait-4k`, `square` (1080×1080), `square-4k`. Aliases: `1080p`, `4k`, `uhd`, `1080p-square`, `4k-square`.
- `--skill=<slug>` — record the owning authoring workflow (e.g. `product-launch-video`) in `hyperframes.json`, so every later render of this project — re-renders, `npm run render`, `--batch` — is attributed to it on anonymous telemetry without re-passing the flag. Creation workflows set this automatically; you rarely pass it by hand.
- `--skip-skills` — **temporarily ignored**: `init` always checks AI coding skills against GitHub while the skills.sh registry catches up. To opt out (CI/tests), set the `HYPERFRAMES_SKIP_SKILLS=1` env var instead.
- `--skip-transcribe` — don't auto-transcribe `--audio` / `--video` with Whisper.
- `--model`, `--language` — Whisper model / language for the auto-transcription.

When using `--tailwind`, invoke the `hyperframes-core` (Tailwind reference) skill before editing classes or theme tokens. The scaffold uses Tailwind v4 browser runtime patterns, not Studio's Tailwind v3 setup.

When `--audio` or `--video` is supplied, `init` transcribes the file with Whisper. For voice/model selection see the `media-use` skill.

## capture

```bash
npx hyperframes capture https://stripe.com                  # scaffold from a website
npx hyperframes capture https://linear.app -o linear-video  # custom output directory
npx hyperframes capture https://example.com --json          # JSON output for agents
npx hyperframes capture https://example.com --skip-assets   # skip image/SVG download
npx hyperframes capture https://example.com --skip-vision   # skip optional AI captions
npx hyperframes capture https://example.com --max-screenshots 12
npx hyperframes capture https://example.com --timeout 60000 # page-load timeout in ms
npx hyperframes capture https://example.com --capture-budget 90000 # post-navigation budget
```

Captures a live URL as an editable HyperFrames project: screenshots become layered scenes, assets are downloaded locally, and the result is a normal project you can `lint` / `preview` / `render`. Use this when the user supplies a URL as the starting point for a video.

`--timeout` bounds page navigation; `--capture-budget` is the separate cooperative budget for work
after navigation (fonts, assets, vision, and contact sheets). The latter is not a hard wall-clock
watchdog and cannot interrupt native work already in flight. An outer caller deadline is therefore a
third, distinct timeout. An outer caller timeout leaves the capture result unknown; it does not prove
HyperFrames hung or that the navigation timeout should be increased. Preserve the last phase and
classify the boundary that fired. `--skip-vision` disables only optional AI image captioning.

For agents, use `--json`. The result includes `ok`, warnings, and `lastPhase`. The command also emits
stable `HYPERFRAMES_CAPTURE_PHASE` records so a watchdog can report the last started, completed, or
degraded phase without retaining sensitive payloads.

Treat a non-zero exit, JSON `ok: false`, or an output `BLOCKED.md` as a **hard stop**. Do not render,
build, or infer brand/design data from partial files in a blocked capture. A successful capture may
degrade an optional phase within budget, but its structural output still has to satisfy the owning
workflow's gate. Exit zero and file existence alone are not semantic success: require the current
invocation's JSON `ok: true`, no `BLOCKED.md`, and artifacts usable for that workflow. Run each retry
into a fresh output directory; never merge or reuse a blocked attempt's partial output.

## skills

```bash
npx hyperframes skills    # install HyperFrames skills for AI coding tools
```

One-time setup that adds the HyperFrames skill pack (`hyperframes-core`, `-creative`, `-animation`, `-cli`, `-registry`, `-media`, plus the `product-launch-video` and `hyperframes` orchestrators) to the local AI coding environment so agents follow the framework conventions. Re-run after major HyperFrames upgrades.


<!-- ===== FILE: hyperframes/hyperframes-cli/references/lambda.md ===== -->

# Lambda rendering on AWS

Use `hyperframes lambda` when the user explicitly wants self-managed AWS infrastructure or needs distributed rendering. It wraps `@hyperframes/aws-lambda` and AWS SAM.

## Contents

- [Choose Lambda or local rendering](#choose-lambda-or-local-rendering)
- [Prerequisites](#prerequisites)
- [Deploy](#deploy)
- [Upload a reusable site](#upload-a-reusable-site)
- [Render one composition](#render-one-composition)
- [Render a JSONL batch](#render-a-jsonl-batch)
- [Inspect progress](#inspect-progress)
- [Destroy the stack](#destroy-the-stack)
- [IAM policies](#iam-policies)
- [State, cost, and cleanup](#state-cost-and-cleanup)

The basic lifecycle is:

```bash
npx hyperframes lambda deploy
npx hyperframes lambda render ./my-project --width 1920 --height 1080 --wait
npx hyperframes lambda destroy
```

## Choose Lambda or local rendering

- **Local `render`** — dev-loop iteration, single host, anything under a few minutes at 1080p.
- **`lambda render`** — long videos, 4K, large parallel batches, or anything where local Chrome would time out / exhaust RAM. Pay-per-invocation, no idle cost.

For one-off short renders Lambda is not worth the deploy overhead.

## Prerequisites

- AWS credentials configured (env vars, `~/.aws/credentials`, SSO, or IMDS).
- AWS SAM CLI on `PATH`.
- `bun` on `PATH` (builds the Lambda handler ZIP).

## Deploy

```bash
npx hyperframes lambda deploy \
  --stack-name=hyperframes-prod \
  --region=us-east-1 \
  --concurrency=8 \
  --memory=10240
```

Builds `packages/aws-lambda/dist/handler.zip` and SAM-deploys the stack (Lambda + Step Functions + S3 + IAM). Idempotent — re-running on the same `--stack-name` is a no-op when nothing changed. Writes `<cwd>/.hyperframes/lambda-stack-<name>.json` so later subcommands don't need to call `describe-stacks`.

| Flag              | Default                         | Description                            |
| ----------------- | ------------------------------- | -------------------------------------- |
| `--stack-name`    | `hyperframes-default`           | CloudFormation stack name              |
| `--region`        | `AWS_REGION` env or `us-east-1` | AWS region                             |
| `--profile`       | `AWS_PROFILE` env               | Named AWS credentials profile          |
| `--concurrency`   | `8`                             | Lambda reserved concurrency            |
| `--chrome-source` | `sparticuz`                     | `sparticuz` or `chrome-headless-shell` |
| `--memory`        | `10240`                         | Lambda memory in MB                    |
| `--skip-build`    | off                             | Reuse existing `handler.zip`           |

## Upload a reusable site

```bash
npx hyperframes lambda sites create ./my-project
# → siteId: abc1234deadbeef0  (stable across re-runs of the same tree)

npx hyperframes lambda render ./my-project --site-id=abc1234deadbeef0 ...
```

Tars + uploads `<projectDir>` to S3 with a content-addressed key. Returns a stable `siteId` you can reuse — re-renders of the same tree skip the upload.

## Render one composition

```bash
npx hyperframes lambda render ./my-project \
  --width 1920 --height 1080 --fps 30 --format mp4 \
  --chunk-size 240 --max-parallel-chunks 16 \
  --wait
```

Starts a Step Functions execution. Returns immediately with a `renderId` unless `--wait` is set, in which case the CLI blocks until completion and streams per-chunk progress lines. Add `--json` for machine-parseable output.

| Flag                    | Description                                                                                                                                                                                                                                                                                                                                                   |
| ----------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `--width` / `--height`  | Output dimensions in pixels                                                                                                                                                                                                                                                                                                                                   |
| `--output-resolution`   | Supersampling preset (engages Chrome `deviceScaleFactor`) — `landscape` / `landscape-4k` / `portrait` / `portrait-4k` / `square` / `square-4k`, plus aliases (`1080p`, `4k`, `uhd`, `hd`, `1080p-portrait`, `4k-portrait`, `1080p-square`, `4k-square`). Use this to render an authored-at-1080p composition at 4K without re-laying-out — see footgun below. |
| `--fps`                 | `24` / `30` / `60`                                                                                                                                                                                                                                                                                                                                            |
| `--format`              | `mp4` / `mov` / `png-sequence` / `webm` (default `mp4`)                                                                                                                                                                                                                                                                                                       |
| `--codec`               | `h264` / `h265` (mp4 only)                                                                                                                                                                                                                                                                                                                                    |
| `--quality`             | `draft` / `standard` / `high`                                                                                                                                                                                                                                                                                                                                 |
| `--chunk-size`          | Frames per chunk (default `240`)                                                                                                                                                                                                                                                                                                                              |
| `--max-parallel-chunks` | Max concurrent chunks (default `16`)                                                                                                                                                                                                                                                                                                                          |
| `--target-chunk-frames` | Cap frames per chunk and let the planner add chunks up to the parallel limit                                                                                                                                                                                                                                                                                  |
| `--site-id`             | Reuse an existing site (skip upload)                                                                                                                                                                                                                                                                                                                          |
| `--execution-name`      | Explicit Step Functions execution name                                                                                                                                                                                                                                                                                                                        |
| `--output-key`          | Explicit final S3 object key                                                                                                                                                                                                                                                                                                                                  |
| `--variables`           | Inline JSON object with composition variable values                                                                                                                                                                                                                                                                                                           |
| `--variables-file`      | JSON file containing one composition variable object                                                                                                                                                                                                                                                                                                          |
| `--strict-variables`    | Fail when supplied variables are undeclared or have the wrong type                                                                                                                                                                                                                                                                                            |
| `--wait`                | Block until completion, stream progress                                                                                                                                                                                                                                                                                                                       |
| `--wait-interval-ms`    | Poll cadence while waiting (default `5000`)                                                                                                                                                                                                                                                                                                                   |
| `--json`                | Machine-parseable progress snapshot                                                                                                                                                                                                                                                                                                                           |

**`--width` / `--height` footgun.** Setting `--width 3840 --height 2160` against a composition whose `data-width="1920"` silently produces 1080p — the runtime lays out the page at the composition's authored dimensions and the CLI flags are ignored for layout. To actually output at 4K, use `--output-resolution 4k` (supersamples via `deviceScaleFactor`). The CLI now prints a warning when CLI dimensions disagree with the composition's `data-width` / `data-height` and `--output-resolution` is not set; the warning is suppressed when `--json` is on or `index.html` isn't on disk (`--site-id` flows).

For variable-driven templates, declare the schema in the composition and pass either `--variables` or `--variables-file`, never both. `--strict-variables` checks local project input before any render starts. Also read [`variables-and-media.md`](../../hyperframes-core/references/variables-and-media.md#variables).

## Render a JSONL batch

Use `render-batch` to upload one template once and start one Step Functions execution per nonblank JSONL line:

```bash
npx hyperframes lambda render-batch ./template \
  --batch ./users.jsonl \
  --width 1920 --height 1080 \
  --max-concurrent 10 \
  --strict-variables \
  --json
```

Each line must be an object with a non-empty `outputKey`. Choose unique keys to prevent outputs from overwriting one another. `variables` and `executionName` are optional:

```json
{
  "outputKey": "renders/alice.mp4",
  "variables": { "name": "Alice" },
  "executionName": "alice-video"
}
```

Batch rules:

- The project is uploaded once unless `--site-id` reuses an earlier upload.
- `--max-concurrent` defaults to `50` and limits in-flight render executions. `--max-parallel-chunks` separately limits chunks inside each render.
- `--strict-variables` checks every entry, reports all variable issues, and aborts before AWS calls.
- `--dry-run` performs no upload or AWS render call. Every manifest row becomes `would-invoke`.
- The emitted manifest preserves input order and records `inputLine`, `outputKey`, `executionArn`, and `status` (`started`, `would-invoke`, or `failed-to-start`), plus an error when applicable.
- A per-entry start failure does not hide other rows. Human-output mode exits nonzero when a row fails to start. In `--json` mode the current CLI prints the manifest and exits zero, so gate on every row's `status`, not the process code alone. Dispatch success is not render completion; inspect each execution with `progress`.

## Inspect progress

```bash
npx hyperframes lambda progress hf-render-abcd1234
npx hyperframes lambda progress arn:aws:states:us-east-1:...:execution:...
```

Prints one snapshot — overall percent, frames rendered, Lambda invocations, accrued cost, and any errors. Accepts a bare `renderId` (resolved against the stack's state-machine ARN) or a full SFN execution ARN.

## Destroy the stack

```bash
npx hyperframes lambda destroy
```

Calls `sam delete --no-prompts` and drops the local state file. **The render S3 bucket is configured `Retain`** so it survives stack destruction — empty + delete it via the AWS console / CLI if you want the storage back.

### Non-retryable errors

A subset of failures the Step Functions state machine short-circuits instead of running through its 4× 15-min retry budget. `progress` surfaces these immediately with the error class name; do not re-issue `lambda render` blindly when you see one.

- **`ChromeBinaryUnavailableError`** — `@sparticuz/chromium` returned an empty/missing executable path. A prior chunk hit `Sandbox.Timedout` mid-extraction and the warm instance is wedged until the execution environment recycles. Remedy: bump a Lambda env var (forces a new exec env) or `lambda deploy` again. Not a transient render failure; retries will burn budget on the same wedged instance.
- **`FFMPEG_VERSION_MISMATCH`** / **`PLAN_HASH_MISMATCH`** — planner / executor version drift. Re-deploy.

## IAM policies

Print or validate the minimum IAM permissions the CLI needs.

```bash
npx hyperframes lambda policies user                                  # inline policy for an IAM user
npx hyperframes lambda policies role                                  # { TrustRelationship, InlinePolicy }
npx hyperframes lambda policies validate ./infra/iam/hf-deploy.json   # CI gate
```

`validate` reads a JSON policy doc and checks the union of its `Effect: Allow` actions (expanding `s3:*` / `s3:Get*` / `*` wildcards) against the CLI's required action set. Missing actions print to stderr; the command exits non-zero. Wire it into CI to catch policy drift before the next deploy fails.

The default action set is deliberately broad (`Resource: "*"`) because CloudFormation creates new ARNs on every adopter's first deploy. Tighten `Resource` after that first run if security posture requires it.

## State, cost, and cleanup

`hyperframes lambda` stores per-stack metadata under `<cwd>/.hyperframes/lambda-stack-<name>.json` (bucket name, state-machine ARN, region). Not secret, but AWS-account-identifying. Commit it to a repo or `.gitignore` it per your workflow.

- `lambda destroy` removes the SAM stack but **leaves the S3 bucket** (`Retain`). Delete it manually if you want the storage back.
- Lambda billing is per-invocation + duration. `progress` reports the accrued cost.
- `--concurrency` caps parallel Lambda invocations — keep it aligned with your account quota.
- `--chunk-size` and `--max-parallel-chunks` trade off per-chunk overhead against parallelism; larger chunks reduce coordinator overhead, smaller chunks parallelize more aggressively.


<!-- ===== FILE: hyperframes/hyperframes-cli/references/lint-validate-inspect.md ===== -->

# lint, check, snapshot

Use `lint` for fast static feedback while iterating. Use `check` as the required final gate: it reruns the same linter, then audits runtime, layout, motion, and contrast in one browser session. Do not chain a redundant standalone `lint` immediately before `check`. `snapshot` is the standalone utility for capturing still frames and zoomed crops. `validate`, `inspect`, and `layout` still run but are deprecated: `check` covers all of them in one invocation.

## Discipline (motion-heavy work)

When the composition is animation-driven, run the checks before you reach for `preview` or `render`:

- Run `lint` after the first HTML pass for early feedback. It is an iteration aid, not a separate final gate.
- Run `check --snapshots` at the first full pass: the overview frames and per-finding crops show you what the auditor saw.
- Look at the PNGs before tuning automated warnings: your eye catches what the auditor misses, and the auditor catches what your eye misses.
- Treat layout errors as defects unless a snapshot proves the layering is intentional, in which case mark it with `data-layout-allow-overflow` / `data-layout-allow-overlap` / `data-layout-allow-occlusion` / `data-layout-allow-caption-zone` (caption band only).
- State motion intent in a `*.motion.json` sidecar so `check` verifies it automatically (entrances firing under seek, stagger order, in-frame, liveness). This is the closest automated proxy for "watch the MP4" and catches render-vs-preview bugs the eye misses (see **Motion verification** below).

## lint

```bash
npx hyperframes lint                  # current directory
npx hyperframes lint ./my-project     # specific project
npx hyperframes lint --verbose        # info-level findings
npx hyperframes lint --json           # machine-readable
```

Lints `index.html` and all files in `compositions/`. Reports errors (must fix), warnings (should fix), and info (with `--verbose`). Catches missing `data-composition-id`, overlapping tracks on the same `data-track-index`, unregistered timelines, and GSAP/CSS transform conflicts.

`<video>`/`<audio>` work at any nesting depth, including inside a `compositions/*.html` sub-composition or a wrapper `<div>`: the runtime discovers media with a flat DOM query and seeks/decodes it wherever it lives (`packages/core/src/runtime/{media,startResolver}.ts`). After a render, `snapshot` each scene that has a video and confirm the panel actually shows footage (a blank/black panel where a clip should play is a real bug, not a placeholder).

## check

```bash
npx hyperframes check                    # current directory: the full browser gate
npx hyperframes check ./my-project       # specific project
npx hyperframes check --json             # agent-readable envelope {ok, browserSkipped, lint, runtime, layout, motion, contrast, hdr, snapshots}
npx hyperframes check --snapshots        # also write overview frames (annotated) + per-finding crops
npx hyperframes check --samples 15       # denser timeline sweep (default 9)
npx hyperframes check --at 1.5,4,7.25    # explicit hero-frame timestamps
npx hyperframes check --at-transitions   # also sample every tween start/end boundary
npx hyperframes check --tolerance 4      # allowed overflow px before reporting (default 2)
npx hyperframes check --timeout 30000    # initial render-ready + navigation minimum in ms (defaults: 3000 / 10000)
npx hyperframes check --no-contrast      # skip the WCAG audit while iterating
npx hyperframes check --strict           # exit non-zero on warnings too (default: only errors)
```

One command, one Chrome boot. `check` runs the linter first and skips the browser entirely when lint reports errors. When the browser never ran (lint errors, a linter crash, or a browser launch failure), `browserSkipped` is `true` and the `layout`, `motion` and `contrast` sections are empty, not clean. Otherwise it loads the bundled composition once, wires runtime listeners before navigation, and sweeps one seek grid running every audit per sample:

- **Runtime**: JavaScript console errors, unhandled exceptions, failed network requests (media-file `ERR_ABORTED` filtered out), HTTP 4xx/5xx.
- **Layout**: text extending outside its container or the canvas, text clipped by its own box, held text overlaps and occlusion (with an approximate covered fraction), children escaping clipping containers. Text under a transparent `<video>` (a `remove-background` cutout) is measured per word against the frame's alpha: partial cover is info with the share hidden, a word 80% hidden or two neighbouring words each half hidden is an error, and a frame that cannot be read falls back to opaque with a `video_alpha_unread` note.
- **Motion**: `*.motion.json` sidecar assertions against the same seeked timeline (see below).
- **Contrast**: WCAG AA on visible text, sampled at 5 grid points. Failures are **errors** and each finding carries the sampled fg/bg colors, measured vs required ratio, and a suggested compliant color in the same palette direction, so most contrast fixes need no screenshot at all.

Every finding carries a selector, the element's `data-*` identity, the composition source file, a bbox, and the sample time: jump straight from the JSON to the HTML you must edit and re-run.

**Severity is persistence-aware.** A dynamic issue observed at a single grid sample (an entrance/exit transient) demotes to info and never gates. Issues held across samples gate the exit code, a held `content_overlap` is an error, and a held, partially-visible `canvas_overflow` breaching ≥5% of the canvas promotes to warning. Coordinate-frame findings (`escaped_container`, `panel_out_of_canvas`, `connector_detached`) flag geometry computed in one frame but rendered in another — an element far outside its offset parent, a painted panel stuck across the canvas edge, a connector line detached from every node. Text drawn into a `<canvas>` has no DOM box, so `canvas_overflow` cannot see it; `canvas_content_at_edge` warns when a canvas's pixels show sharp content (drawn text, hard shapes) along the frame edge — mark intentional full-bleed art (particles, photos) with `data-layout-allow-overflow`. If a 3s+ composition shows no visible change across every sample, `check` fails with `sweep_static`: a frame that never changes while a GSAP timeline or tween, or a CSS or Web animation, holds the same time without ever finishing means the seek is not driving the page, so it refuses to pass. Any other frame that never changes (a still title card, an audio-only advance) is a warning that `--strict` fails; a composition meant to be still can take `data-no-timeline` on its root to skip it. The fingerprint includes per-element opacity, so opacity-only reveals (code typing, staggered fades) count as motion — but only while they're still in flight at the sampled times. The classic trap is a reveal that completes early and then holds a static frame for the rest of the duration: every sample lands on the settled state and check warns that nothing on screen moved (`--strict` fails it). Spread the reveal across the timeline or keep one continuously animated element alive (a blinking caret is idiomatic for code typing) — don't bolt on a slow position drift just to appease the check.

**Escape hatches** (mark intent in the HTML, then re-run):

- `data-layout-allow-overflow` — overflow is intentional (entrance/exit travel).
- `data-layout-allow-overlap` — deliberate text layering (e.g. a demo cursor label over a heading). Applies only to the marked text block; it is not inherited. Mark the specific layering participant, never a scene/root wrapper, so unrelated descendant collisions remain auditable.
- `data-layout-allow-occlusion` — an element is meant to cover text.
- `data-layout-allow-caption-zone` — intentional lower-third / caption-band copy under `--caption-zone`. Applies to the marked element and every descendant (`closest`); silences only `caption_zone_collision` (not overflow/overlap/occlusion). Prefer the narrowest wrapper that owns the intentional band copy.
- `data-layout-ignore` — decorative element that should never be audited.

**Opt-in pipeline gates** (used by orchestrators; off by default):

```bash
npx hyperframes check --caption-zone "x0=0;y0=.82;x1=1;y1=1;severity=error;seek=.25,1"
npx hyperframes check --frame-check     # media (img/svg/video/canvas) out-of-frame detection
```

`--caption-zone` takes fractional band geometry (`x0/y0/x1/y1` required, 0-1 fractions of the composition's own canvas, portrait included) with optional `severity` and comma-separated `seek` fractions; it flags a text element's DOM box (`getBoundingClientRect`) that overlaps the band. Waive intentional lower-third copy with `data-layout-allow-caption-zone` on the element or its nearest wrapper (see Escape hatches). `--frame-check` reports media elements breaching the canvas beyond `max(120px, 6% of the min canvas dimension)`.

**Fixing contrast errors** — thresholds are 4.5:1 for normal text, 3:1 for large text (24px+, or 19px+ bold). The finding's `suggestedColor` already picks the nearest compliant color in the right direction (brighten on dark backgrounds, darken on light); apply it or adjust within the palette family, then re-run `check`.

## Motion verification (`*.motion.json` sidecar)

`check` verifies **motion intent** against the same seeked timeline the renderer uses — the closest automated proxy for "render the MP4 and watch it". It catches render-vs-preview bugs layout sampling can't: an entrance reveal the seek lands past, a broken stagger order, an element drifting off-frame mid-tween, a frozen shot.

Drop a `*.motion.json` sidecar next to the composition (matching the html basename when several compositions share a dir). `check` discovers it automatically — no flag, no authoring-framework changes. With no sidecar, `check` behaves exactly as before.

```json
{
  "duration": 6,
  "assertions": [
    { "kind": "appearsBy", "selector": "#headline", "bySec": 0.5 },
    { "kind": "before", "a": "#headline", "b": "#cta" },
    { "kind": "staysInFrame", "selector": ".card" },
    { "kind": "keepsMoving", "withinSelector": ".scene" }
  ]
}
```

| Assertion                      | Fails (code) when                                                           |
| ------------------------------ | --------------------------------------------------------------------------- |
| `appearsBy(selector, bySec)`   | not visible (opacity ≥ 0.5) by `bySec` — `motion_appears_late`              |
| `before(a, b)`                 | `a` does not first appear strictly before `b` — `motion_out_of_order`       |
| `staysInFrame(selector)`       | once visible, its box leaves the canvas — `motion_off_frame`                |
| `keepsMoving(withinSelector?)` | a fully-static window exceeds `maxStaticSec` (default 2s) — `motion_frozen` |

`duration`, `withinSelector`, and `maxStaticSec` are optional. Findings are **errors by default** and appear in the same human and `--json` output as layout findings. A selector that matches nothing is reported as `motion_selector_missing` rather than silently passing — a typo'd selector fails loudly. Use this in the feedback loop instead of eyeballing the render: assert what the motion is supposed to do, and let `check` tell you when the seek diverges from intent.

## snapshot

```bash
npx hyperframes snapshot                       # 5 key frames as PNG
npx hyperframes snapshot ./my-project          # specific project
npx hyperframes snapshot --frames 10           # evenly-spaced N frames
npx hyperframes snapshot --range 3:5 --frames 8 # 8 frames within root-timeline seconds 3–5
npx hyperframes snapshot --composition intro --frames 8 # 8 frames within this data-composition-id
```

Still PNGs. Each run writes `.hyperframes/artifacts/snapshots/<id>/` unless `--output` is set. `snapshot` is the standalone capture; `check --snapshots` is the gate.

One of `--at`, `--range START:END` (seconds), or `--composition <data-composition-id>` (not a CSS selector). `--frames` defaults to 5. Range and composition sample just before the end and add no extra end frame; `--at` adds one unless `--no-end`.

### Keep verification clean and inspect the actual pixels

Inspect full-resolution frames in the opening 30 seconds, each mounted scene, and every reported problem interval. Contact sheets locate moments; use close-ups to judge thin edges, glass, particles, and WebGL geometry. Check the live preview and decoded render at matching times. Canvas shader defects can survive a successful DOM/layout audit. Record the browser/GPU and capture path when results differ across machines; isolate the failing material or pass before changing rendering defaults.

Managed snapshot storage keeps the newest 10 run folders, the newest evidence for the current revision and retained rendered revisions, and the latest snapshot. Live captures and folders younger than 24 hours are also preserved. Automatic cleanup removes whole eligible old UUID folders, including contact sheets and descriptions; arbitrary `--output` folders are untouched. Save intentional before/after evidence outside this managed storage.

For disposable checks, allocate a temporary output folder and remove that folder after inspecting it. Use `hyperframes clean --dry-run` to inspect broader cleanup. `clean --snapshots` explicitly discards snapshot evidence; use it only when that evidence is no longer needed. Never recommend removing all of `.hyperframes`, which also contains project history and other state.

### Zooming into a reported finding

`hyperframes check --snapshots` already writes a `finding-NN-<code>.png` crop for every error finding that carries a bbox, but the same zoom is available standalone once you know what to look at:

```bash
npx hyperframes check --snapshots               # reports a finding, e.g. content_overlap on "#cta"
npx hyperframes snapshot --zoom "#cta"           # crop the element to verify the defect, at 3x density
npx hyperframes snapshot --zoom "100,50,400,300" --zoom-scale 2   # or an exact pixel region
# fix the composition HTML, then re-check:
npx hyperframes check
```

`--zoom` takes a CSS selector or an exact `x,y,w,h` pixel region and always produces a real high-density crop (a raised `deviceScaleFactor`, never CSS zoom or a viewport resize), so the composition's layout — and its render determinism — is untouched. A selector matching nothing is a loud error, not a silent full-frame fallback, and a frame where the target has no visible box (collapsed or animated off-canvas) is skipped with a note instead of written as a sliver.

## Deprecated: validate, inspect, layout

All three keep working, print a deprecation notice on stderr, and mark `_meta.deprecated: true` in `--json`. Their functionality lives in `check`:

- `validate` (runtime errors + contrast) → `check` (contrast failures are now gating errors with fix payloads, not warnings).
- `inspect` / `layout` (layout sweep + motion sidecar) → `check` (same flags: `--samples`, `--at`, `--at-transitions`, `--tolerance`, `--strict`).

Migrate scripts by replacing the sequence with the single `check` invocation; scaffolded projects' `npm run check` already points there.


<!-- ===== FILE: hyperframes/hyperframes-cli/references/preview-render.md ===== -->

# preview, play, render, publish

Serve, render, and share commands.

## preview

```bash
npx hyperframes preview                   # foreground on a TTY; persistent in agent shells
npx hyperframes preview --background      # explicit persistent session
npx hyperframes preview --foreground --json # ready JSON, then remain attached
npx hyperframes preview --background --port 4567 # agent-safe custom port (default 3002)
npx hyperframes preview --selection --json # print the current Studio selection and exit
npx hyperframes preview --context --json  # print compact agent context from Studio
```

Hot-reloads on file changes. Opens Studio in the browser automatically — the full timeline editor, where the user can play the video and edit anything by hand before rendering. This is the review surface, not just a viewer.

When handing a project back to the user, use the Studio project URL, not the source `index.html` path:

```text
http://localhost:<port>/#project/<project-name>
```

Use the actual port and project directory name; treat `index.html` as source-code context, not the preview surface. For example, after `npx hyperframes preview --background --port 3017` in `codex-openai-video`, report `http://localhost:3017/#project/codex-openai-video`.

Two ways a handed URL turns out dead — check both before handing it back: the URL is missing its `#project/<project-name>` hash (Studio loads but has no project to open), or the server is not actually running. Bare `preview` automatically creates a managed persistent session in a non-TTY agent shell; `--background` remains the clearest explicit form. Verify the printed URL returns HTTP 200, keep it alive for the whole review, and stop it explicitly with `npx hyperframes preview --stop` afterward. Use the printed URL as-is: HyperFrames URL-encodes project names that contain route metacharacters.

### Agent context from Studio selection

`preview --context` and `preview --selection` are the agent bridge into a running Studio session. They do **not** start a new server; they find the active preview server for the current project, read agent-useful state from Studio, print it, and exit.

Use it when the user gives deictic edit instructions like "change this", "move the selected element", "make the card I clicked bigger", or "fix the current selection":

```bash
npx hyperframes preview --context --json --context-fields selection
```

The compact context payload includes the selected element's source file, composition path, current timeline time, `data-hf-id` / selector target, bounding box, text content, and a thumbnail URL for the selected element. Prefer `selection.target.hfId` when present; fall back to `selection.target.selector` only when no stable `data-hf-id` exists. If `selection` is `null`, inspect `errors.selection.code` (for example, `no-selection`).

Keep agent context small by asking only for the slices you need:

```bash
npx hyperframes preview --context --json --context-fields selection
npx hyperframes preview --context --json --context-fields lint
npx hyperframes preview --context --json --context-fields selection,lint
```

Use `--context-detail full` only when the edit genuinely needs heavy selection fields such as `computedStyles`, `inlineStyles`, `dataAttributes`, or editable text-field metadata:

```bash
npx hyperframes preview --context --json --context-fields selection --context-detail full
```

`preview --selection --json` remains available when you explicitly want the full selected-element payload and do not need lint/server context.

Failure modes:

| Code                       | Meaning                                                                    |
| -------------------------- | -------------------------------------------------------------------------- |
| `preview-not-running`      | Start Studio first with `npx hyperframes preview --background`.            |
| `ambiguous-preview-server` | Multiple matching Studio servers are open; rerun with one listed `--port`. |
| `preview-port-mismatch`    | The requested `--port` is not one of the matching Studio servers.          |
| `no-selection`             | Studio is open, but the user has not selected an element yet.              |
| `selection-unavailable`    | The running preview server does not expose selection context cleanly.      |

If there is no selection, ask the user to click the target element in Studio and rerun the command. If the server error lists candidate ports, rerun the same command with `--port <candidate>`. Do not infer the target from a screenshot when the CLI can give a stable element target.

## play (lightweight player)

```bash
npx hyperframes play                  # current project, port 3003
npx hyperframes play ./my-video       # specific project
npx hyperframes play --port 8080      # custom port
```

`play` serves the composition through the embeddable `<hyperframes-player>` web component instead of the full Studio UI. Use it when sharing a preview link or when Studio is heavier than needed (no editor, no panels). `play` reports the plain `http://localhost:<port>` URL — no `#project/<name>` fragment (that's a Studio routing convention only `preview` uses).

The player's `playback-rate` attribute (preview speed control, drives the timeline's `timeScale`) is clamped to `[0.1, 5]`; values `≤ 0` or non-finite fall back to `1`. This is a preview/playback knob, not a composition `data-*` attribute — authored motion still renders at `1×`.

### Launching with an external browser (preview + play)

Both `preview` and `play` can open inside an explicit Chromium-compatible browser instead of the OS default. Two use cases: isolated Chromium profile, or external CDP attach (DevTools / Playwright / Puppeteer / browser-MCP). **HyperFrames itself does not own CDP automation** — this only exposes the endpoint; whatever connects to it is your problem. Not to be confused with `--browser-gpu` (a `render` flag controlling Chrome GPU access during capture).

| Flag                      | Type            | Notes                                                                                                                                                                                           |
| ------------------------- | --------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `--browser-path`          | path            | Absolute path to a Chromium-compatible executable (`/usr/bin/chromium`, `/Applications/Brave Browser.app/...`).                                                                                 |
| `--user-data-dir`         | path            | Chromium-compatible profile directory. Requires `--browser-path`. Use a throwaway directory to keep state out of your main profile.                                                             |
| `--remote-debugging-port` | integer 1-65535 | Open a Chromium CDP endpoint on the given port. **Requires both** `--browser-path` and `--user-data-dir` — refused otherwise, so a CDP endpoint cannot leak into your main profile by accident. |

```bash
# Open preview in an isolated Chromium profile
npx hyperframes preview --background --browser-path /usr/bin/chromium --user-data-dir /tmp/hf-profile

# Same plus a CDP endpoint on :9222 (attach DevTools / Playwright / etc.)
npx hyperframes play --browser-path /usr/bin/chromium --user-data-dir /tmp/hf-profile --remote-debugging-port 9222
```

Validation runs before any server boots, so an invalid value exits cleanly without leaving a listening socket behind.

## render

> Render only after the user has reviewed in `preview` and approved. Don't auto-render when the checks pass.

```bash
npx hyperframes render                                # standard MP4 from cwd
npx hyperframes render ./my-video --output ./out.mp4  # render from outside the project dir
npx hyperframes render --output final.mp4             # named output (no timestamp)
npx hyperframes render -c compositions/intro.html -o intro.mp4  # render a specific sub-composition file
npx hyperframes render --quality draft                # fast iteration
npx hyperframes render --quality looks                # first real encode (default)
npx hyperframes render --fps 60 --quality delivery    # final delivery
npx hyperframes render --format webm                  # transparent WebM
npx hyperframes render --docker                       # byte-identical
```

> Default `--output` is `renders/<project-name>_<YYYY-MM-DD>_<HH-MM-SS>.<ext>` — timestamped per render so successive runs don't clobber each other. Pass `--output` to get a stable name.

| Flag                                 | Options                                                                                            | Default                        | Notes                                                                                                                                                                                                                                                                                                                                                                                                                                         |
| ------------------------------------ | -------------------------------------------------------------------------------------------------- | ------------------------------ | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `dir` (positional)                   | path                                                                                               | cwd                            | Project directory. Omit to use current working directory.                                                                                                                                                                                                                                                                                                                                                                                     |
| `--composition`, `-c`                | path to composition file                                                                           | `index.html`                   | Render a specific composition file (e.g. `compositions/intro.html`) instead of the project's `index.html`.                                                                                                                                                                                                                                                                                                                                    |
| `--output`, `-o`                     | path                                                                                               | `renders/<project>_<ts>.<ext>` | Output path. Default is timestamped (`<project-name>_YYYY-MM-DD_HH-MM-SS.<ext>`).                                                                                                                                                                                                                                                                                                                                                             |
| `--fps`                              | 24, 30, 60                                                                                         | 30                             | 60fps doubles render time                                                                                                                                                                                                                                                                                                                                                                                                                     |
| `--quality`                          | draft, looks, delivery, standard, high                                                             | looks                          | `looks` is CRF 16 on the standard preset. `delivery` is `high`. draft for iterating                                                                                                                                                                                                                                                                                                                                                           |
| `--format`                           | mp4, webm, mov, gif, png-sequence, hls                                                             | mp4                            | WebM/MOV render with transparency; gif for inline autoplay in GitHub PRs/READMEs/docs (two-pass palette encode, fps capped at 30 — prefer `--fps 15` — no audio, 1-bit transparency only, HDR falls back to SDR); png-sequence writes RGBA frames to a directory (AE/Nuke/Fusion ingest); hls writes an HLS VOD directory (master.m3u8 + video/audio playlists + MPEG-TS segments), SDR only, rejects `--gpu`, unavailable on lambda/cloudrun |
| `--gif-loop`                         | 0-65535                                                                                            | 0                              | GIF loop count; `0` loops forever. Only with `--format gif`.                                                                                                                                                                                                                                                                                                                                                                                  |
| `--hls-segment-seconds`              | 1-60                                                                                               | 4                              | HLS target segment length in whole seconds; also locks the encoder GOP so every segment starts on a keyframe. Only with `--format hls`.                                                                                                                                                                                                                                                                                                       |
| `--resolution`                       | landscape, portrait, landscape-4k, portrait-4k, square, square-4k (+ aliases `1080p`, `4k`, `uhd`) | —                              | Supersample via Chrome `deviceScaleFactor`. Aspect ratio must match composition; scale must be an integer. Not with `--hdr`.                                                                                                                                                                                                                                                                                                                  |
| `--crf`                              | 0-51                                                                                               | —                              | Encoder CRF (lower = higher quality). Mutually exclusive with `--video-bitrate`.                                                                                                                                                                                                                                                                                                                                                              |
| `--video-bitrate`                    | e.g. `10M`, `5000k`                                                                                | —                              | Target bitrate. Mutually exclusive with `--crf`.                                                                                                                                                                                                                                                                                                                                                                                              |
| `--hdr`                              | flag                                                                                               | off                            | Force HDR output even with SDR sources. MP4 only.                                                                                                                                                                                                                                                                                                                                                                                             |
| `--sdr`                              | flag                                                                                               | off                            | Force SDR even with HDR sources.                                                                                                                                                                                                                                                                                                                                                                                                              |
| `--workers`                          | number or `auto`                                                                                   | auto                           | Each worker spawns Chrome (~256 MB)                                                                                                                                                                                                                                                                                                                                                                                                           |
| `--docker`                           | flag                                                                                               | off                            | Reproducible output across hosts                                                                                                                                                                                                                                                                                                                                                                                                              |
| `--gpu`                              | flag                                                                                               | off                            | GPU-accelerated FFmpeg encoding (NVENC / VideoToolbox / VAAPI / QSV)                                                                                                                                                                                                                                                                                                                                                                          |
| `--browser-gpu` / `--no-browser-gpu` | flag                                                                                               | auto (local), off (docker)     | Host GPU for Chrome/WebGL capture                                                                                                                                                                                                                                                                                                                                                                                                             |
| `--browser-timeout`                  | seconds (0.001–86400)                                                                              | 60                             | Puppeteer page-navigation timeout for the entry HTML. Raise when heavy compositions (many videos / fonts / remote assets) can't reach `domcontentloaded` within the 60s default.                                                                                                                                                                                                                                                              |
| `--quiet`                            | flag                                                                                               | off                            | Suppress verbose output                                                                                                                                                                                                                                                                                                                                                                                                                       |
| `--strict`                           | flag                                                                                               | off                            | Fail on lint errors                                                                                                                                                                                                                                                                                                                                                                                                                           |
| `--strict-all`                       | flag                                                                                               | off                            | Fail on lint errors AND warnings                                                                                                                                                                                                                                                                                                                                                                                                              |
| `--variables`                        | JSON object                                                                                        | —                              | Override values declared in `data-composition-variables`                                                                                                                                                                                                                                                                                                                                                                                      |
| `--variables-file`                   | path                                                                                               | —                              | JSON file with variable values (alternative to `--variables`)                                                                                                                                                                                                                                                                                                                                                                                 |
| `--strict-variables`                 | flag                                                                                               | off                            | Fail render on undeclared keys or type mismatches in `--variables`                                                                                                                                                                                                                                                                                                                                                                            |

**Quality guidance:** `draft` while iterating, `looks` (the default) for the first real encode, `delivery` for final delivery. `standard` and `high` still work.

**Read the summary's second line.** After the output path and size, `render` prints the capture path, GPU mode, and per-stage timings, e.g. `beginframe capture · software gpu · compile 0.7s · setup 1.1s · capture 8.1s · encode 5.8s`. `capture` is the frame loop and `setup` is calibration plus session init; the capture path reads `a|b` when parallel workers diverged, and `encode (during capture)` means the streaming encoder overlapped the loop, so do not add it to the wall time. Local GPU `auto` (the default) requests BeginFrame. If the line still says `screenshot capture` with `software gpu` on Linux, a hint under it says BeginFrame did not run (needs chrome-headless-shell, no `--resolution` upscale). It only appears when the GPU was auto-probed, never under `--docker` or `--no-browser-gpu`, where software GL is the point. Heavy compositions can stall on software GL. Do not reach for `--debug` just to learn which path ran.

**Parametrized renders:** the composition declares its variables on the `<html>` root with **`data-composition-variables`** — a JSON **array of declarations** (`{id, type, label, default}` per entry) that defines the schema. Scripts inside read the resolved values via `window.__hyperframes.getVariables()`. The CLI `--variables '{"title":"Q4 Report"}'` is a JSON **object keyed by id** that overrides those declared defaults for one render; missing keys fall through, so the same composition runs unchanged in dev preview and in production. Sub-comp hosts can also override per-instance with `data-variable-values`. See the `hyperframes-core` skill for the full pattern.

### feedback (report after rendering)

After a render is verified, send one feedback line per task. This is the maintainers' primary signal — a render that finishes silently tells them nothing.

```bash
npx hyperframes feedback --rating 10                              # clean run, no notes
npx hyperframes feedback --rating 6 --comment "bg <video> renders grey in multi-scene; worked around with --format png-sequence"
```

`--rating` is an integer from 0-10; `--comment` is free text. A `--comment` with no `--rating` is a ratingless report (`MISSING FEATURE:` and `HOST APP:` in `GUIDE.md`) that never counts in the rating metric. Feedback is anonymous and attaches a `doctorSummary` (OS/Node/CPU/mem/ffmpeg) automatically, so don't repeat those fields. A clean run needs only a short result. Before sending any bug, workaround, or confusing behavior, collect this compact reproduction packet:

```text
REPRO COMMAND: <HF_*/PRODUCER_* env> npx hyperframes <exact command>   # run from the project directory; do NOT paste absolute paths
EXPECTED / ACTUAL: <expected behavior> / <observed behavior and isolated trigger>
EXACT ERROR: <verbatim error or warning; include frame/timestamp for visual defects>
OUTCOME: <output correct | output corrupt | fallback succeeded | hard exit | command hung>
WORKAROUND: <exact workaround, or none>
COMPOSITION_STRUCTURE:
  elements: video=<n> audio=<n> img=<n> svg=<n> canvas=<n> subComps=<n>
  attributes: <comma-joined subset of clip-path, filter, mix-blend-mode, transform, mask, position:fixed, overflow:hidden, z-index, data-has-audio, data-duration, data-start, data-composition-src, background-image:url, mask-image:url — or "(none present)">
  timeline: <flat | nested (<n> sub-comps)>; driver=<gsap | data-timeline | gsap+data-timeline | none>
  delta: <what differs between the working workaround-render and the broken default render>
  defect: <spatial location + frame index range, e.g. top-left / frames 0-30 — omit for non-visual defects>
```

`COMPOSITION_STRUCTURE:` is a privacy-preserving structural anatomy: counts + presence flags only, no file paths, no src URLs, no user text. It lets maintainers pattern-match the report against known bug families (e.g. "sub-comp mount + clip-path", "GSAP timeline + z-index") without receiving the composition ZIP. Required for any rating ≤ 7 that describes a visual defect (black frame, flicker, corrupt output, wrong frame, blank output, other visual anomaly); optional but appreciated on higher ratings. Agents on this skill can auto-fill the block by calling `buildCompositionCensus(html)` and `renderCompositionCensusBlock(census)` from `packages/cli/src/utils/compositionCensus.ts` against the composition HTML they already have access to — the human user does not fill this out by hand.

**Feedback is submitted to a public channel — anonymize before sending.** Redact absolute paths (which leak user home directory + machine identity), any user or project names embedded in paths, secrets, and credentials. Path arguments in the command should stay relative to the project directory (`./renders/out.mp4`, not `/Users/<user>/Documents/…/out.mp4`; `.hf-tmp/`, not `/home/<user>/projects/<real-name>/.hf-tmp/`). Similarly strip absolute paths from `EXACT ERROR:` stack traces and log excerpts — keep the file basename and line number, drop the leading directory. Preserve flags and relevant `HF_*` / `PRODUCER_*` variables verbatim. If the failure no longer reproduces, include the last failing command and log excerpt (redacted the same way). Share a project link only when one is already available and safe to share.

The `hyperframes feedback` command soft-warns when a non-10 `--comment` is missing `REPRO COMMAND:`, and when a rating-≤-7 visual-defect comment is missing `COMPOSITION_STRUCTURE:`. The warnings print above the submission ack and do not block — some legitimate reports (a one-line "cloudrun quota bumped yesterday, fine now") won't fit the mold. Fix the packet and rerun to silence them.

Hit a reproducible bug? Add `--file-issue` (optionally `--dir <project>` and `--yes` for non-interactive shells) to also publish a minimal repro to a public URL and open a pre-filled GitHub `bug` issue draft for a maintainer to file. This publishes the project publicly, so it is opt-in and consent-gated; the issue is never auto-submitted.

## publish

```bash
npx hyperframes publish              # upload current project privately, return stable URL
npx hyperframes publish ./my-video   # specific project
npx hyperframes publish --public     # allow anyone with the URL to view the claimed project
npx hyperframes publish --yes        # skip the confirmation prompt (scripts/CI)
```

Uploads the project's source (HTML + assets) and returns a stable hosted URL that renders in the browser. A fresh publish is private by default and requires authentication plus access to view. Use `--public` to allow anyone with the URL to view the claimed project. Updating a project in place keeps its existing visibility: re-publishing without `--public` never turns a public project private. `--yes` only skips the confirmation prompt; it does not change visibility. A signed-out publish returns an authentication-required claim URL rather than a public playback URL. Lint findings are surfaced before upload but do not block.


<!-- ===== FILE: hyperframes/hyperframes-cli/references/upgrade-info-misc.md ===== -->

# info, upgrade, compositions, timeline, docs, benchmark, telemetry, asset preprocessing

Catch-all reference for commands that don't fit the main dev loop.

## info

```bash
npx hyperframes info                   # project metadata
npx hyperframes info ./my-video        # specific project
npx hyperframes info --json
```

Prints **project** metadata: name, resolution, duration, element counts by type, track count, and total project size. Project-level — not environment. For environment health use `doctor`.

## upgrade

```bash
npx hyperframes upgrade                # check + interactive prompt
npx hyperframes upgrade --check        # check and exit, no prompt (agent-friendly)
npx hyperframes upgrade --check --json # machine-readable: current / latest / updateAvailable
npx hyperframes upgrade --yes          # print upgrade commands without prompting
```

Compares the installed CLI version against npm latest.

`--project [dir]` bumps a **project's** pinned scripts instead of the global install: it rewrites every `npx …hyperframes@<version>…` in `<dir>/package.json` (default cwd) to npm-latest. Always invoke it unpinned (`npx hyperframes@latest upgrade --project`) — a project scaffolded on an old CLI stays frozen otherwise. `--project . --check` reports the delta without writing; add `--json` for `{ changed, from, to, path }`. Pass the dir explicitly whenever another flag follows `--project` — on older releases a bare `--project` consumes the next flag as its directory value.

## timeline

```bash
npx hyperframes timeline [project-dir]          # tracks and clips as a table with bars
npx hyperframes timeline [project-dir] --json
```

Reach for `timeline` instead of opening `index.html` and each `data-composition-src` file when you need to know what is on the timeline: which clips exist, when they start and end, what they play, and how loud. It reads the project's files statically (no browser).

Text output is `timeline <N>s`, then one block per track kind (`video`, `graphics`, `captions`, `audio`) with one row per clip of that kind, ordered by absolute start:

```
graphics (2: 1 top-level, 1 nested)
  |██████                                  | sec-connector 0-6.7s src=compositions/connector-morph.html
  |██████████████                          | box 15.67-17.99s (local 0-2.32s) nested in sec-connector compositions/connector-morph.html
audio (1)
  | █                                      | vo 1.6-3.6s src=vo.mp3 vol=0.5 group=vo volume[0:0.2 2:1]
```

- The bar is 40 columns over the whole timeline. Times are seconds.
- `src=`, `vol=`, `rate=` (playback rate, only when not 1), `group=` (audio group), and `<target>[t:v ...]` (automation lane points, `t` in seconds from the clip start) appear only when the clip has them.
- The header counts every clip of that kind, nested ones included: `video (6: 2 top-level, 4 nested)`. The list is in absolute order, so the Nth row is the Nth clip of that kind on the main timeline. A clip inside a sub-composition prints its absolute start-end, then `(local <start>-<end>s)` (time inside that sub-composition), then `nested in <host row id> <file that declares it>`. Only one level of nesting is read: a sub-composition inside a sub-composition is listed as a row saying `children=unread`, and the clips inside it are not counted.
- With no `data-duration`/`data-end`, a media row still gets a resolved length and says where it came from: `duration=media` means ffprobe measured the source (with playback start and rate applied); `duration=default` means an `img` got the 3s default; `duration=inferred` means a composition host summed its children; `pending: <reason>` (dotted bar, `duration` 0) means the source could not be probed (missing file, remote `src`, ffprobe error). A non-media leaf with nothing to resolve prints no source.
- `lanes unreadable: ...` means the clip's `data-automation` or `data-fx-chain` did not parse; fix the attribute.

`--json` prints `{ timeline: { duration, tracks: [{ kind, rows: [...] }] } }`. A track's `rows` are every clip of that kind, nested ones included, by `absStart`; read them, never only the top level. Each row has `id`, `kind` (tag), `trackKind`, `start`, `duration`, `end` (local to the row's own file), **`absStart`, `absEnd`, `file`** (main-timeline time and the project-relative file that declares the clip — use these, not `start`/`end`, to compare clips across nesting), `trackIndex`, `src`, `sourceFile`, `volume`, `lanes`, `playbackRate`, `audioGroup`, `durationAuthored`, **`durationSource`** (`"authored" | "media" | "default" | "inner" | "pending"`, or `null` for a non-media leaf with nothing to resolve), **`pendingReason`** (why nothing resolved; `null` unless `durationSource` is `"pending"`), `laneError`, **`index`** (the row's position in its kind's `rows`; a position, not an id), **`nested`** (declared inside a sub-composition), **`host`** (plain id of the row that hosts a nested clip, else `null`), **`hostRow`** (`{kind, index}` of that host row), and `children` (`{kind, index}` pointers to the sub-composition's clips, one level; every clip is already a full row in its kind's `rows`, so nothing needs following).

### Query one-liners (jq, node fallback if jq is absent)

```bash
TL=$(npx hyperframes timeline --json)
# 1. what plays at absolute time T=12.5
jq --argjson t 12.5 '[.timeline.tracks[].rows[] | select(.absStart<=$t and .absEnd>$t)]' <<<"$TL"
node -e 'const t=12.5,j=JSON.parse(require("fs").readFileSync(0,"utf8"));j.timeline.tracks.forEach(tr=>tr.rows.forEach(x=>{if(x.absStart<=t&&x.absEnd>t)console.log(x.id,x.file)}))' <<<"$TL"
# 2. find a clip by id or src -> file, track, absStart, absEnd
jq --arg q tsfx-pet2 '[.timeline.tracks[].rows[] | select(.id==$q or .src==$q)] | .[] | {file,trackKind,absStart,absEnd}' <<<"$TL"
node -e 'const q="tsfx-pet2",j=JSON.parse(require("fs").readFileSync(0,"utf8"));j.timeline.tracks.forEach(tr=>tr.rows.forEach(x=>{if(x.id===q||x.src===q)console.log(x.file,x.trackKind,x.absStart,x.absEnd)}))' <<<"$TL"
# 3. every clip of one kind, nested included, in absolute order
jq --arg k video '.timeline.tracks[] | select(.kind==$k).rows[] | {id,absStart,absEnd}' <<<"$TL"
node -e 'const k="video",j=JSON.parse(require("fs").readFileSync(0,"utf8"));j.timeline.tracks.find(t=>t.kind===k).rows.forEach(r=>console.log(r.id,r.absStart,r.absEnd))' <<<"$TL"
# 4. gaps and overlaps within a kind (positive = gap, negative = overlap)
jq --arg k video '(.timeline.tracks[] | select(.kind==$k).rows) as $r|[range(0;($r|length)-1)|{a:$r[.].id,b:$r[.+1].id,delta:($r[.+1].absStart-$r[.].absEnd)}]' <<<"$TL"
node -e 'const k="video",j=JSON.parse(require("fs").readFileSync(0,"utf8"));const r=j.timeline.tracks.find(t=>t.kind===k).rows;for(let i=0;i<r.length-1;i++)console.log(r[i].id,r[i+1].id,r[i+1].absStart-r[i].absEnd)' <<<"$TL"
# 5. the Nth clip of a kind by absolute start (N=2)
jq --arg k video --argjson n 2 '.timeline.tracks[] | select(.kind==$k).rows[$n-1] | {index,id,absStart,file,nested}' <<<"$TL"
node -e 'const k="video",n=2,j=JSON.parse(require("fs").readFileSync(0,"utf8"));const r=j.timeline.tracks.find(t=>t.kind===k).rows[n-1];console.log(r.index,r.id,r.absStart,r.file)' <<<"$TL"
```

## compositions, docs

```bash
npx hyperframes compositions           # list compositions in project
npx hyperframes compositions --json
npx hyperframes docs                   # list available topics
npx hyperframes docs rendering         # print one topic inline in the terminal
```

`compositions` lists every `data-composition-id` in the project (including sub-comps) with duration, resolution, and element count.

`docs` prints inline documentation **in the terminal** — it does not open a browser. Topics: `data-attributes`, `examples`, `rendering`, `gsap`, `troubleshooting`, `compositions`. Run without a topic to see the list.

## benchmark

```bash
npx hyperframes benchmark              # run the preset matrix in current project
npx hyperframes benchmark ./my-video   # specific project
npx hyperframes benchmark --runs 5     # repeat each config N times (default 3)
npx hyperframes benchmark --json
```

Renders the project with 5 preset configurations — `30fps draft 2w`, `30fps standard 2w`, `30fps high 2w`, `30fps standard 4w`, `60fps standard 4w` — and prints a comparison of render speed and output file size. Use it to find the fastest acceptable preset for your machine. Not a single-render-with-stage-breakdown.

## telemetry

```bash
npx hyperframes telemetry status      # show telemetry state
npx hyperframes telemetry disable     # disable anonymous usage telemetry
npx hyperframes telemetry enable      # re-enable telemetry
```

Telemetry is anonymous usage counters only. Disable globally with `HYPERFRAMES_NO_TELEMETRY=1` if env-var control is preferred over the subcommand.

Events include two fingerprint properties used to distinguish managed-sandbox runs from real laptops — no PII, no env-var **values**, only existence checks:

- **`sandbox_runtime`**: `gvisor` / `firecracker` / `docker` / `kvm` / `wsl` / `null`. gVisor via kernel string + `/proc/version`. Firecracker via `/dev/vsock` + DMI sys_vendor. Docker via `/.dockerenv` + cgroup.
- **`agent_runtime`**: `claude_code` / `codex` / `cursor` / `copilot_agent` / `jules` / `replit` / `devin` / `aider` / `gemini_cli` / `hermes` / `openclaw` / `null`. Detected by the existence of well-known vendor env vars; the values themselves are never read.
- **`client`**: set only when an app launched the CLI with a `HYPERFRAMES_CLIENT` tag (`<app>/<version>/<channel>`), sent as-is when it is a short slug.

## Asset Preprocessing

```bash
npx hyperframes tts
npx hyperframes transcribe
npx hyperframes remove-background
```

These produce assets (narration audio, word-level transcripts, transparent video) that get dropped into a composition. Each may download its own model on first run.

For voice selection, Whisper model rules, output format choice, and the TTS → transcript → captions chain, invoke the `media-use` skill. This skill stays focused on the dev loop.

## Remaining harness usage

Run `npx hyperframes usage --json` at the start of a video workflow and again at milestones such as after drafting and before rendering. A fresh read at handoff can serve as the start read. Use `--harness claude-code`, `--harness codex`, or `--harness grok` to select explicitly.

Known results contain `status: "known"`, `harness`, `planTier`, `session`, `weekly`, and `spend`. Each available window contains `usedPercent`, `remainingPercent`, and `resetsAt`; an unavailable window is `null`. `planTier` is the readable subscription tier when available, otherwise `null`. Claude Code reports its shared five-hour and weekly windows; a spend-metered plan (such as Enterprise) has neither and reports `spend`, the share of its billing-period spend limit already used, with `resetsAt: null`. Codex reports its shared session and weekly windows when available. Grok reports its included weekly allowance with `session: null`. Only Claude Code reports `spend`; it is `null` elsewhere. When no window is available the result is `status: "unknown"` with `reason: "no_usage_windows"`.

Unknown results contain `status: "unknown"` and a token-free `reason`. Missing, expired, unsupported, ambiguous, or unreadable logins and unavailable provider responses return unknown. Report the unknown state without guessing allowance. The command reads existing credentials without refreshing or rewriting them and emits no tokens or telemetry. Usage is a snapshot; it does not reserve allowance or estimate the next video's cost. Keep scope and workflow choices with the user.
