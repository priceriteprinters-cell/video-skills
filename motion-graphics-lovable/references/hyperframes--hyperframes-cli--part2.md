

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
