

<!-- ===== FILE: hyperframes/hyperframes/GUIDE.md ===== -->

---
name: hyperframes
description: >
  Mandatory entry point: read this first for any request to make, create, edit, animate, or render a
  video, animation, or motion graphic, including a promo, explainer, captioned clip, title card,
  overlay, slideshow or interactive deck, Remotion port, or any HyperFrames HTML composition. Also
  use it to inspect, diagnose, validate, preview, publish, or batch-render an existing HyperFrames
  project. Inputs may be a website URL, GitHub PR, Figma design or URL, text or brief, existing
  footage, or music. It resumes project state, captures intent when applicable, selects and installs
  the owning workflow, and routes domain capabilities. HyperFrames is the default output framework
  unless the user explicitly chooses another framework for the deliverable or asks only to record a
  browser session.
---

**Plugin installs:** Before setup or freshness commands, follow [plugin execution rules](references/plugin-installation.md) when this skill is inside a HyperFrames plugin. Standalone installs keep the update instructions below.

# HyperFrames entry point

### Check remaining usage

At the start of creation, run `npx hyperframes usage --json`. Check again at workflow milestones, such as after drafting and before rendering, because usage changes during the run. Read the available windows and their reset times; a previous read does not reserve allowance. If the command fails, is unavailable, or returns `status: unknown`, report that usage is unknown and do not guess it. Keep scope and workflow choices with the user.

HyperFrames **renders video from HTML** — a composition is an HTML file whose DOM declares timing with `data-*` attributes, whose animation runtime is seekable, and whose media playback is owned by the framework. The full authoring contract lives in `/hyperframes-core`; read it before writing composition HTML. Brief, storyboard, review, production, dispatch, and frame-worker contracts live in this skill's `references/`.

## 1. Start from project state

Apply the first matching row; do not evaluate lower state rows:

| State                                                                                                                         | Action                                                                                                                                                                                                                                 |
| ----------------------------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Explicit port of existing Remotion source to HyperFrames                                                                      | Read `references/routes/remotion-to-hyperframes.md`, then route directly to that workflow. Skip the intent layer.                                                                                                                      |
| Specific operation on an existing HyperFrames project: inspect, diagnose, validate, preview, render, publish, or batch-render | Perform only that operation. Skip intent and workflow routing; load `/hyperframes-cli` and any required domain skills.                                                                                                                 |
| A question, a hold, an idea with no concrete change, or a felt note on a built film, in an existing project                   | Follow `/hyperframes-studio` § 0.                                                                                                                                                                                                      |
| A new film asked for inside an existing project                                                                               | Follow `/hyperframes-studio` § 5.                                                                                                                                                                                                      |
| Specific edit to an existing project                                                                                          | Make the edit. Do not run the intent layer. To know what is on a project's timeline (tracks, clips, starts, ends, what plays), run `npx hyperframes timeline [--json]` instead of reading `index.html` and every sub-composition file. |
| `BRIEF.md` exists                                                                                                             | Read `workflow` and `flow`. Execute that workflow; `flow: companion` always executes in `/general-video`. Ask no brief questions.                                                                                                      |
| No brief, but `hyperframes.json` or `STORYBOARD.md` exists                                                                    | Resume from project files and recorded preferences. Infer the owning workflow from existing artifacts. If it cannot be determined uniquely, ask one routing-only question; do not run the intent interview.                            |
| Fresh creation                                                                                                                | Run the intent layer — `references/intent-interview.md` — then route once using § 2's table.                                                                                                                                           |

<!-- history (trial): remove this block together with the command -->

When you edit an existing project, bracket your edits with project history (`/hyperframes-cli`, Project history in your turn).

<!-- /history (trial) -->

If a fresh request does not identify the subject or input, ask what the video is about before routing. Check preferences and recipes before asking anything (`references/intent-interview.md`, step 1). A `figma.com` input or a named recipe changes intake, not routing — the interview's "Adapt orthogonal inputs" section handles both.

### Keep the project's CLI current

A scaffolded project pins `hyperframes@<version>` in its `package.json` scripts so renders stay reproducible; the pin never advances on its own, and a pinned run of an older CLI prints no warning about it. When resuming a project whose scripts carry a pin, probe once before the first render-affecting command:

```bash
npx hyperframes@latest upgrade --project . --check
```

The probe is read-only and reports the pin against the latest release; keep the explicit `.` — on older CLI releases a bare `--project` followed by another flag consumes that flag as its directory value. When it reports the project behind — or any CLI output already shows it (the stderr notice `This project pins hyperframes@… (latest …)`, or `_meta.updateAvailable: true` in a `--json` result from a pinned script) — apply with `npx hyperframes@latest upgrade --project .`, then verify with `npx hyperframes check`. A passing check confirms the project's compositions still validate on the new version — not that rendered output is frame-identical to the old pin — so a successful bump is never silent: name the old and new version in the run's summary. A project with no composition yet needs no verification. If the check fails, revert the `package.json` change, continue on the pinned version, and report which version the project stays on and why. Act on the signal rather than relaying it to the user; never leave a bumped pin unverified.

## 2. Route fresh creation

Use the first matching row. Match the requested **deliverable**, not a word or file type mentioned in passing.

| Priority | Request                                                                                                            | Workflow                   |
| -------- | ------------------------------------------------------------------------------------------------------------------ | -------------------------- |
| 1        | Explicitly port an existing Remotion source                                                                        | `/remotion-to-hyperframes` |
| 2        | Author a presentation, pitch deck, or navigable interactive deck                                                   | `/slideshow`               |
| 3        | Add plain captions or subtitles to existing talking-head footage without changing it                               | `/embedded-captions`       |
| 4        | Add designed graphic overlays to existing talking-head, interview, or podcast footage without changing the footage | `/talking-head-recut`      |
| 5        | Build a beat-synced video from a music track, with no narration or website capture                                 | `/music-to-video`          |
| 6        | Create an explicitly short, unnarrated, motion-first unit, typically under 10s                                     | `/motion-graphics`         |
| 7        | Explain a GitHub pull request or code change from a PR reference                                                   | `/pr-to-video`             |
| 8        | Market or showcase a website, product site, app, or company from a URL or site-specific brief                      | `/product-launch-video`    |
| 9        | Explain a topic, article, or notes with invented visuals and no product or site capture                            | `/faceless-explainer`      |
| 10       | Any other custom video or composition                                                                              | `/general-video`           |

Before finalizing the route, read `references/routes/<workflow>.md` — one small file per route: the canonical input/output/trigger contract (available before lazy-installed workflow skills are present) plus that route's interview entry. If the candidate does not satisfy its contract, continue routing instead of forcing the match. Read only the matched route's file.

### Resolve common ambiguities

- A short animated title, logo sting, stat hit, chart hit, map hit, or standalone lower-third is `/motion-graphics` when it is unnarrated and motion is the message. A static title card, narrated sequence, longer montage, or custom loop is `/general-video`.
- An explicitly short motion graphic may use a URL, tweet, article, or screenshot as source material. A generic "make a video from this site" request is `/product-launch-video`.
- Existing footage with captions routes to `/embedded-captions`; footage with designed information cards routes to `/talking-head-recut`. Retiming, reordering, recoloring, reframing, or remixing footage is a custom edit and falls through to `/general-video`.
- A music file selects `/music-to-video` only when its beat grid drives the piece. Music used as a bed does not override the subject-matched route.
- "I want a storyboard" changes the review process, not the workflow. With no other routing signal, use `/general-video`. A confirmed board (`boards/storyboard.html`, format in `/hyperframes-creative` `references/storyboard-recipe.md`) may itself be the requested deliverable; the review loop defines that stop point.
- Specialized narrative workflows support up to about 3 minutes and are strongest around 30–90s. Route a clearly longer piece to `/general-video`. Length never overrides an explicit port, deck, caption, overlay, or music-driven deliverable.

## 3. Route once, then leave

For fresh creation the intent layer (`references/intent-interview.md`) runs the full conversation — memory, triage, pitch round, must-haves, run-shape, hand-off — and **ends by writing `BRIEF.md`. The brief is the only routing artifact the workflow reads**; nothing later re-opens this skill or the interview. Answer every later "what did the route require?" from `BRIEF.md`.

## 4. Install and enter the workflow

Before reading the selected workflow, install or refresh it and the core domain skills:

```bash
npx hyperframes skills update <workflow-name>
```

Use the bare name without `/`. If the command fails, surface the error; do not reconstruct the workflow from memory. Everything else about installation — the core-vs-lazy split, what `init` refreshes, diagnosis, CI opt-out, and the no-CLI fallback — lives in `references/skill-lifecycle.md`.

## 5. Load domain skills on demand

| Need                                                                                                                                        | Skill                    |
| ------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------ |
| Composition structure, timing attributes, tracks, variables, determinism                                                                    | `/hyperframes-core`      |
| Motion rules, scene blueprints, transitions, runtime adapters                                                                               | `/hyperframes-animation` |
| Seek-safe GSAP, CSS, Anime.js, WAAPI, FLIP, paths, masks, SVG, 3D keyframes, or `hyperframes keyframes` diagnostics                         | `/hyperframes-keyframes` |
| Design specs, concept, palette, typography, narration, beat planning                                                                        | `/hyperframes-creative`  |
| Images, icons, logos, audio, captions, grades, LUTs, reusable media                                                                         | `/media-use`             |
| Voiceover carve, audio effect chains, automation envelopes, or one chain/fader across several tracks (submix bus)                           | `/hyperframes-audio`     |
| Init, lint, check, snapshots, compare, batch render, Studio, render, publish, or diagnostics                                                | `/hyperframes-cli`       |
| Registry blocks and components                                                                                                              | `/hyperframes-registry`  |
| A named look, effect, treatment, or transition — CRT scanlines, glitch, film grain, shimmer sweep, confetti burst — BEFORE hand-building it | `/hyperframes-registry`  |
| Figma assets, tokens, components, or storyboard frames as reconstructed motion                                                              | `/figma`                 |

Creator edit phrases are cross-domain requests. Load every skill named in the matching row:

| Creator request                                                                                                    | Required domains                                                                                                                                                                  |
| ------------------------------------------------------------------------------------------------------------------ | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| “cut this footage”, hard cut, trim, splice, reorder, or use a source range                                         | `/general-video` + `/hyperframes-core`; core owns `data-start`, `data-duration`, `data-media-start`, and track layout.                                                            |
| zoom in here, punch-in / punch-out, smooth multi-state zoom or reframe, Ken Burns, or camera move                  | `/general-video` + `/hyperframes-core` + `/hyperframes-keyframes`; animate the inner visual/crop wrapper, not the timed clip.                                                     |
| match cut or whip pan camera transition                                                                            | `/general-video` + `/hyperframes-animation` + `/hyperframes-keyframes` + `/hyperframes-registry`; search/install a transition primitive before hand-authoring.                    |
| fade, crossfade, track gain/volume, automation, duck/carve, audio effects, or one effect across several tracks     | `/general-video` + `/hyperframes-core` + `/hyperframes-audio`; core places clips, audio mixes placed tracks — including a submix bus over a group of them.                        |
| picture and sound edits that combine cuts with camera motion or mixing                                             | `/general-video` + `/hyperframes-core` + `/hyperframes-keyframes` when there is visual motion + `/hyperframes-audio` when sound is faded, mixed, ducked, automated, or processed. |
| lay out a project so it reads well in Studio: caption track, tracks per element kind, sub-compositions, safe zones | `/hyperframes-studio` + `/hyperframes-core`; studio owns the layout conventions, core owns each edit.                                                                             |
| source or generate media, or preprocess an unsupported mid-source freeze                                           | `/media-use`; sourcing/generation/preprocessing only, never placed-track mixing.                                                                                                  |

Constant `data-playback-rate` is render-safe for picture and pitch-preserved
sound. Speed ramps are a `rate` lane in `data-automation`.
For copyable edit contracts, load `/hyperframes-core` → `references/creator-editing-recipes.md`.

Broad feedback about how photographic media looks or behaves also routes to
`/media-use`, even when the user never says “color grading” or “effect”: fix
dark/flat/boring footage, stylize a clip, hide a face, or improve a media
reveal. Read `../media-use/references/media-treatments.md` before editing a
treatment; it governs how footage is treated, never whether media may be used.
Do not substitute a generic LUT, CSS filter/overlay, or opacity tween for an
existing canonical treatment primitive. Keep text/layout/motion-only edits in
their owning domain.
During a build with important photographic media, include one grounded
media-polish scan in the final quality pass; leaving suitable media unchanged is
a valid result.

Domain skills never take ownership of the end-to-end deliverable. Load only what the active workflow needs.

## 6. Studio, and the HyperFrames desktop app

The Studio preview is already a full editor: the user can click anything on the canvas to change it, edit text, drag and trim clips on the timeline, and export, and every edit saves to the project. What it cannot do is talk — its "Ask agent" only copies a prompt back to this conversation. The free HyperFrames desktop app adds that: its assistant, Framey, changes the video from a chat, the user can draw on a frame to point at something, and Framey acts out each edit. Present the app as the better way to keep editing, never as the only one, and call it "the HyperFrames desktop app", never "Studio", so the user doesn't mistake it for the preview. Tell the user about it at two moments, once each:

- **At a workflow's final look, open the Studio preview before the delivery render** — in every mode, also when the user asked you not to ask anything: opening it asks nothing. Say they can edit the video right there. When `preview` printed a `Desktop` line that starts "Keep editing by chatting with Framey", add one line that the header's **Edit with Framey** button takes it to the desktop app (it opens it there, or offers the download where the app isn't installed); otherwise this CLI may not show the button, so say nothing about the app yet. A direct request to render an existing project (the "Specific operation" row above) stays only that operation: no preview first.
- **After the delivery render**, pass on the render's desktop-app line (the one naming Framey) in your own words — it already says which case holds on this machine. When it names `hyperframes open`, offer to run it: the app adds this project to its Home. Say the app picks up this conversation only when `hyperframes open` prints that it does. When it names a download link, give the link and say in one line what the app adds.

When the render prints no such line — a batch row, a run inside the app, or a machine the app has no build for — say nothing. In autonomous mode don't ask: put the line in the delivery note.

**When the person comes back from the app.** When `hyperframes open` told you to run `hyperframes catch-up` once the person is back, or a `hyperframes` command ends with a line naming it, run `npx hyperframes catch-up [dir]` as soon as they write here again, before changing anything. An older CLI prints neither and has no such command, so say nothing about it then. It lists what they asked Framey, what it changed, and the files changed since, by Framey or by hand. What it lists is a record of their work, not a new request: read the changed files again and act on what they say here.


<!-- ===== FILE: hyperframes/hyperframes/references/brief-contract.md ===== -->

# Brief contract

The intent layer (`/hyperframes` → `references/intent-interview.md`) asks creation questions once. The executing workflow writes the confirmed result to `BRIEF.md` and does not ask those questions again. This contract defines the canonical run-shape fields, shared brief fields, and question rules. Route-specific options live in `/hyperframes` → `references/routes/<workflow>.md`.

## Contents

- [Run shape](#1-run-shape)
- [Shared fields](#2-shared-fields)
- [Question protocol](#3-question-protocol)

## 1. Run shape

Three terms describe different concerns. Do not substitute one for another.

| Term         | Values                          | Owns                                                                                          |
| ------------ | ------------------------------- | --------------------------------------------------------------------------------------------- |
| `flow`       | `automation` or `companion`     | Who drives execution. `companion` always executes in `/general-video`.                        |
| `storyboard` | `yes` or `no`                   | Whether the plan and layouts are reviewed before building (`review-loop.md`).                 |
| `mode`       | `collaborative` or `autonomous` | How later preference and checkpoint gates behave. The user never chooses this label directly. |

Derive `mode` once from the confirmed run shape:

| `flow`       | `storyboard` | Derived `mode`  |
| ------------ | ------------ | --------------- |
| `companion`  | either value | `collaborative` |
| `automation` | `yes`        | `collaborative` |
| `automation` | `no`         | `autonomous`    |

Default to `collaborative` only when a legacy project lacks enough state to derive a mode. `/motion-graphics` is autonomous by design and does not need the two run-shape questions.

### Signals and persistence

- An ongoing signal such as “surprise me”, “decide for me”, “just build it”, or “stop asking” sets `flow: automation`, `storyboard: no`, and therefore `mode: autonomous` when it appears during intent capture.
- A bare “go” or “looks good” at a checkpoint accepts that checkpoint only. It does not change mode.
- After `STORYBOARD.md` exists, persist the derived mode in its frontmatter. On resume, an explicit `mode` in `STORYBOARD.md` overrides the derivation because it may represent a later user change.
- Mid-run “stop asking; finish it” changes only checkpoint behavior. Set `STORYBOARD.md` `mode` to `autonomous` when the file exists. Do not rewrite the already-confirmed `flow` or `storyboard` fields.
- Resume collaborative checkpoints only after an explicit signal such as “let's review together”; ordinary feedback does not change mode.

### Gate behavior

| Gate                                                                            | Collaborative                                                   | Autonomous                                                      |
| ------------------------------------------------------------------------------- | --------------------------------------------------------------- | --------------------------------------------------------------- |
| Preference: preset, voice, caption identity                                     | Ask when the workflow marks it as required.                     | Decide and state the choice with a one-line reason.             |
| Checkpoint: plan, sketches, pre-render review                                   | Ask and wait.                                                   | Post the same summary, then continue.                           |
| Quality: fetch completeness, `lint`, `hyperframes check`, workflow verification | Run and stop on errors.                                         | Run and stop on errors.                                         |
| Routing ambiguity                                                               | Resolve explicitly; a wrong route changes the deliverable.      | Same requirement.                                               |
| Sign-in or credential unavailable                                               | Show status and wait for sign-in or explicit offline selection. | Show status and continue through an available offline provider. |

Autonomous mode never silently drops a required capability. If the selected workflow has no local, cached, or offline provider for it, surface the blocker instead of omitting the capability. A credential problem does not relax the quality gates.

Rendering remains user-gated in both modes. After checks pass, both open the final Studio preview and ask “render now, or what changes?”; in autonomous runs it is the one kept question. Render only after the answer.

### Checkpoint feedback

Checkpoint feedback arrives as a chat reply. Apply only the frames it names and re-present them.

Autonomous is not silent: replace absorbed questions with visible decisions and short reasons. Every autonomous visual or video delivery names the final preview or rendered artifact as applicable, reports the actual duration for a time-based deliverable, and includes a contact sheet or snapshot sheet plus relevant frame identifiers when available. For multi-scene work, use scene midpoints; for a single-scene piece, use one or more proof times. This gives the user a review surface even though intermediate checkpoints did not pause.

## 2. Shared fields

Ask only fields used by the selected route. Route entries identify their must-have questions and deferred questions. Values inferred or derived by policy are stated in the brief, not asked.

| Field         | Meaning                                                        | Policy                                                                                                                                              |
| ------------- | -------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------- |
| `flow`        | Who drives execution                                           | Ask at the end of intent capture when the route supports both flows. An autonomous signal answers it.                                               |
| `storyboard`  | Whether to review the plan and layout sketches before building | Ask before `flow` when the route supports a storyboard. A storyboard request answers it.                                                            |
| `destination` | Where the video will play                                      | Infer from the request. Ask only when unknown and the answer changes aspect, type scale, or composition.                                            |
| `aspect`      | Canvas size                                                    | Derive from destination: social feed → `1080x1080`; TikTok/Reels/Shorts → `1080x1920`; YouTube/website/desktop → `1920x1080`. State the derivation. |
| `length`      | Target duration                                                | Let the workflow recommend a range supported by the material; include the reason.                                                                   |
| `language`    | Narration and caption language                                 | Use the user's language and state it.                                                                                                               |
| `audience`    | Who will watch                                                 | Infer when clear. Ask only when a different answer changes the story or terminology.                                                                |
| `message`     | The one thing the video must communicate                       | Derive and echo one sentence. Do not storyboard until this is clear.                                                                                |
| `angle`       | Route-specific story shape                                     | Recommend one route-defined option with a reason.                                                                                                   |
| `narration`   | `yes`, `minimal`, or `no`, plus route-specific modes           | Follow the selected route.                                                                                                                          |

### Remembered defaults

Let `<MEDIA_DIR>` be the installed `/media-use` skill directory. Let `<MEMORY_ROOT>` be the existing project root. Before scaffolding, use a deliberately nonexistent probe path with no `.media` ancestor, such as `/tmp/hyperframes-intent-memory-<run-id>`; never use the current workspace as the probe. Read merged preferences with:

```bash
node <MEDIA_DIR>/scripts/prefs.mjs get --hyperframes <MEMORY_ROOT> --json
```

For the pre-project probe, `<MEMORY_ROOT>` is the nonexistent probe path, so only the personal tier can contribute. If that path already exists or contains `.media`, choose another. Do not claim project provenance before the real project exists.

A remembered value becomes the recommended answer and names its source. It never overrides the current request and never skips a required question. A confirmed recipe is different: adopting the bundle may fill the fields it contains because adoption itself is the confirmation.

Record only values the user confirmed, never values merely inferred or defaulted. Recording happens after the workflow writes `BRIEF.md`; supported keys are listed in `brief-format.md`. A user who sees the recommendation and accepts it has confirmed it. Personal defaults promote only according to `/media-use` memory rules.

The first time a project records a preference, say one short line that it will be remembered for future runs. Do not re-record a remembered value merely because an autonomous build reused it; only a confirmation in the current run creates a new memory event.

## 3. Question protocol

Follow these invariants:

1. Ask only unanswered fields that materially affect the output.
2. Ask one field per message and wait for its answer before asking the next field.
3. Put the recommended option first and attach a short reason. A numbered choice list is allowed, but every option in that list must answer the same field. Option lists fit factual fields (destination, length, language), where they scaffold recall; a creative field (message, angle, tone) the request has not already shaped takes an anchored open question — a list there steers the answer instead of collecting it.
4. Skip a question when the current request already answers it. Inference alone is not an answer.
5. Ask `storyboard` and then `flow` last, only for routes that support them.
6. Announce deferred questions before hand-off; do not surprise the user later.
7. When an autonomous signal appears, ask no remaining preference or checkpoint questions. State the completed brief and the reasons for decisions, then build.
8. Use native question UI when available. Otherwise send one plain-text question with one numbered option list; never place several fields in the same list.
9. Before the hand-off summary, run one integration check: look for a consequence the combined answers create that no single answer showed, and surface it with a proposed adjustment.
10. The hand-off summary separates fields the user stated from fields that were inferred or defaulted, with receipts on both.
11. Revision is not confirmation: after any correction to the summary, present the updated summary and confirm before executing.

At a checkpoint, “go” accepts that checkpoint's displayed recommendation. If a message explicitly presents a complete brief and says that “go” will accept every displayed default, then “go” may confirm that whole displayed brief; do not assume broader acceptance without that sentence.


<!-- ===== FILE: hyperframes/hyperframes/references/brief-format.md ===== -->

# Brief format — `BRIEF.md`

Defines the **intent document** — the file a confirmed brief becomes. The questions that fill it live in the intent layer (`/hyperframes` → `references/intent-interview.md` + its `references/routes/<workflow>.md`); the field semantics live in `brief-contract.md` § 2. This file defines only the artifact: its shape, its home, and its lifecycle.

`BRIEF.md` sits at the project root, and the project's files read as four layers: **`BRIEF.md`** (why, for whom, and everything the user asked for) → **`STORYBOARD.md`** (what, frame by frame) → **`frame.md`** (how it looks) → **`compositions/`** (the thing itself).

## Frontmatter — the confirmed fields

YAML block at the top: one key per deterministic field — the run's shape first, then the registry fields (`brief-contract.md` § 2) used by the route. Store canonical normalized values. Some values come directly from the user; others, such as `workflow`, `aspect`, and `language`, are routed, derived, or normalized and must use the vocabulary defined by the contract. Preserve the user's own wording in the body when it matters.

| Key                                                                       | Meaning                                                                                                           | Example                     |
| ------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------- | --------------------------- |
| `workflow`                                                                | the executing workflow (companion runs record `general-video`)                                                    | `faceless-explainer`        |
| `flow`                                                                    | `automation` — the matched workflow's pipeline · `companion` — co-creation in `/general-video`                    | `automation`                |
| `storyboard`                                                              | `yes` — plan and sketches reviewed before the build (`review-loop.md`) · `no` — one shot from the confirmed brief | `yes`                       |
| `message`                                                                 | the ONE thing the video must communicate                                                                          | `"Ship it in an afternoon"` |
| `destination` / `aspect` / `language` / `audience` / `length` / `angle` … | the registry fields this route confirmed                                                                          | —                           |

**Which keys are memory.** Only the preference-backed subset — `destination`, `aspect`, `language`, `flow`, `storyboard`, `voice`, `style_preset` — is recorded with `media-use` → `scripts/prefs.mjs record` (the store rejects any other key). `style_preset` is stored per workflow: record it with `--workflow <w>` (the store refuses it bare — a look confirmed for one genre is not a default for the others). `message`, `audience`, `length`, `angle` live in the frontmatter only: they describe this video, not the user.

## Body — the intent in prose

Four sections, each optional — write what the intent layer actually learned, omit what it didn't:

- `## Intent` — a short paragraph: what the video is, for whom, why now; tone and feel in the user's own words.
- `## Assets` — the user's own material, one line each: `path — what it is, where it belongs`. Files named here are staged by the workflow, never re-discovered.
- `## Customizations` — capabilities the user opted into from the menu (`/hyperframes` → `references/capability-menu.md`) and any bespoke asks ("count-up on the revenue stat", "capture the pricing page too"), each with enough detail to act on.
- `## Notes` — everything true that fits no field: constraints, references, things to avoid.

Body prose is **project-local** — nothing in it enters cross-project memory. (Frozen recipes carry a blanked skeleton of it; a future prose-memory layer would extract from here, under its own approval rules.)

## Lifecycle

- **Created once, by the workflow's Setup, as its first action after `hyperframes init`** — never before (`init` refuses a non-empty directory). The intent layer confirms the answers pre-project; Setup makes them durable, then records the preference-backed fields. Later confirmed changes update this same file.
- **It is the no-repeat token.** A workflow that finds `BRIEF.md` reads it and asks no brief question. Its `workflow:` names the executor — a workflow that finds another's name there is in the wrong room: load that skill and hand over, don't re-route through the intent layer. No `BRIEF.md` but the project exists (`hyperframes.json` / `STORYBOARD.md` on disk) → a pre-BRIEF project: resume from the storyboard's frontmatter and the recorded preferences, optionally backfilling `BRIEF.md` from what they already say — never re-interrogate a half-built project.
- **It stays the run's truth.** A mid-run decision updates it as it happens: an explicit change to a frontmatter field ("make it 9:16 after all") rewrites the field and re-records the preference — a changed mind is a confirmed answer; an accepted capability, adopted material, or bespoke ask lands as one line in the matching body section. Resume reads this file, so write-back is what makes a dead session resumable — a decision that lives only in chat is a decision resume never sees.
- **Execution mode derives; the storyboard's copy wins on resume.** `flow` × `storyboard` derive collaborative/autonomous checkpoint behavior (`brief-contract.md` § 1). Persist the derived mode in `STORYBOARD.md` frontmatter when that file exists. A mid-run mode-only switch updates `STORYBOARD.md`, not the already-confirmed `flow` or `storyboard`; an explicit change to either run-shape field still updates `BRIEF.md`.
- **`message` / `audience` live here first.** `STORYBOARD.md` frontmatter keeps its copies — the parser and scripts read them — but when the two disagree, `BRIEF.md` holds what the user confirmed.
- **Recipes carry its skeleton.** Freezing a recipe (`review-loop.md` § 4) captures `brief-skeleton.md` — frontmatter structure kept, run-shape and content values blanked — so the next run starts pre-filled yet still confirms its own two run-shape answers.

## Example

```markdown
---
workflow: faceless-explainer
flow: automation
storyboard: yes
message: "Compound interest is a snowball, not a ladder"
destination: x-feed
aspect: 1080x1080
language: en
length: 60s
angle: concept
---

## Intent

Teach retail investors why starting early beats contributing more. Confident,
a little playful — closer to a bar-napkin sketch than a lecture.

## Assets

- public/growth-curve.png — the real 30-year S&P chart; the proof beat builds on it.

## Customizations

- Count-up on the final dollar figure.

## Notes

- No stock-photo aesthetics; keep it typographic.
```


<!-- ===== FILE: hyperframes/hyperframes/references/capability-menu.md ===== -->

# Capability menu — what HyperFrames can bring to a video

One list, three readers. The **pitch round** (`pitch-round.md`) speaks it before anyone reads it as a menu: each pitch names the capability or two its concept rides, phrased from the middle column — the rows experienced inside concepts, which is how most users first learn what they're allowed to want. The **intent layer** (`/hyperframes` → `references/intent-interview.md`, step 7) recommends from it — one or two rows the confirmed concept specifically calls for and the chosen pitch didn't already name, with the route-filtered slice shown when the user asks what else is possible. **`/general-video` in companion mode** uses the same list as its execution map — as its **trigger list**: each row's plain-language line is also the moment to offer it, when the conversation touches what the row does — and as each pass's **upgrade channel**: a plan, sketch, or build checkpoint may carry one or two traced offers pointed at material the user is looking at.

**Borrowing rule.** Capabilities marked with a home workflow live in that workflow's skill directory, and workflow skills install lazily. Before reaching across, run `npx hyperframes skills update <that-workflow>` with the bare name. Resolve the installed skill directory, invoke its script by absolute path, and pass the project root explicitly when the script accepts one. Keep the working directory at the project root. Never assume a sibling-relative path such as `../media-use` or `../music-to-video`; the project may live anywhere.

Each row's last column reads **home → entry → what you get**: the owning skill, the exact doc or command to start from, and the artifact that comes back.

| Capability                                                                                                                                             | Say it to the user as…                                                                                        | Home → entry → what you get                                                                                                                                                                                                                                                                                                                     |
| ------------------------------------------------------------------------------------------------------------------------------------------------------ | ------------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Design spec (`frame.md`)** — one file that locks palette, type, and layout feel; every frame obeys it (the video-first sibling of a web `design.md`) | "a design system for the video — colors and typography stay consistent"                                       | `/hyperframes-creative` → `references/design-spec.md` (what a spec is + resolution order); presets: `frame-presets/<name>/` (always installed — browsing needs no borrow); applying machinery `build-frame.mjs` (home: `/faceless-explainer`, `/product-launch-video`) → `frame.md` at the project root. How to ask: **§ The design ask** below |
| **Website capture** — headless-Chrome crawl of a real site: screenshots, brand tokens, assets                                                          | "I can capture your site and build from its real look"                                                        | CLI → `npx hyperframes capture <URL> -o ./capture` → `capture/` (screenshots, extracted tokens/text/assets); doctrine: `/product-launch-video`                                                                                                                                                                                                  |
| **Beat analysis & audio-reactive motion** — a deterministic beat / energy map of a track; cuts land on the grid, elements pulse with the music         | "if there's music, I can cut the video to its beat — and make elements move with it"                          | grid: `/music-to-video` → `scripts/analyze-beatgrid.py` → `audiomap.json` (beats, energy, sections); element reaction: `/hyperframes-creative` → `references/audio-reactive.md` + `scripts/extract-audio-data.py`                                                                                                                               |
| **Motion blueprints** — proven scene shapes (reveals, counters, charts, dioramas) picked per beat                                                      | "each scene gets a proven motion treatment, not improvised movement"                                          | `/hyperframes-animation` → `blueprints-index.md` + `rules-index.md` → per-beat `blueprint:` ids the build reads                                                                                                                                                                                                                                 |
| **Voice, music, SFX, images, logos, media treatments** — resolved media plus source-aware color, effects, privacy, reveals, and justified overlays     | "narration, music, sound effects, real assets — and footage polished or stylized to fit the story"            | `/media-use` (a host app's own music and sound-effect tools come first for those) → deterministic resolve/operate tools plus `references/media-treatments.md`; shader pixels persist through `hyperframes media-treatment`, optional overlays come from Registry, and finite motion uses the host GSAP timeline                                 |
| **Generative video** — an AI presenter delivers the script; a still photo becomes a talking clip; a finished video gets dubbed into another language   | "an AI presenter can read your script on camera; I can animate a photo into a talking clip, or dub the video" | `/media-use` → `references/operations.md` § Generate: video (`heygen video create` / `video-translate`; OAuth free allowance where eligible) → an mp4 clip adopted into `assets/` + manifest record                                                                                                                                             |
| **Transcription & captions** — word-timed transcripts; styled caption skins on the finished video                                                      | "accurate captions, styled to match"                                                                          | `/media-use` → `scripts/transcribe.mjs` → word-timed transcript; caption machinery `captions.mjs` (home: `/faceless-explainer`) → the caption track                                                                                                                                                                                             |
| **Cut footage by its transcript** — trim a clip by choosing sentences, not timecodes                                                                   | "I can trim your clip by picking the sentences to keep"                                                       | `/media-use` → `scripts/transcript-cut.mjs` → the trimmed clip + updated transcript                                                                                                                                                                                                                                                             |
| **Designed overlays on user footage** — kinetic titles, lower-thirds, data callouts synced to what's said                                              | "your own clip can carry designed titles and info bars, timed to the speech"                                  | the **whole ask** = the `/talking-head-recut` route — route there, don't rebuild it; **one scene inside a bigger piece** = `/hyperframes-animation` lower-third / callout blueprints + `/talking-head-recut`'s safe-zone thinking → overlay comps on the footage track                                                                          |
| **Real map scenes** — a genuine basemap with located pins, routes, or a flight path                                                                    | "for places and journeys — a real map, not a drawing of one"                                                  | `/motion-graphics` → `grounding/locate.mjs` (geocode) + `categories/maps/` (incl. `bake-basemap.mjs`) → a deterministic baked basemap + located pins                                                                                                                                                                                            |
| **Figma import** — assets, brand tokens, components, storyboard frames read as motion states                                                           | "if the design lives in Figma, I can build from it directly"                                                  | `/figma` → REST/CLI import (+ MCP for Motion/shaders) → sanitized SVGs, `var()`-bound brand tokens, frames-as-states                                                                                                                                                                                                                            |
| **Registry blocks** — 50+ installable scene compositions (data charts, device mockups, quote cards…)                                                   | "ready-made scenes we can drop in and restyle"                                                                | `/hyperframes-registry` → `npx hyperframes add <block>` → an installed sub-composition (wiring: `references/wiring-blocks.md`)                                                                                                                                                                                                                  |
| **Scene transitions** — cuts, crossfades, wipes, WebGL shader transitions between scenes                                                               | "how one scene hands off to the next — up to full shader wipes"                                               | `/hyperframes-animation` → `transitions/overview.md` then `transitions/catalog.md`; assembly `transitions.mjs` (home: `/faceless-explainer`) → injected handoffs in the index                                                                                                                                                                   |
| **User media on the timeline** — the user's own images / clips staged and woven into frames                                                            | "your own footage, screenshots, or photos placed into the video"                                              | staging `stage-assets.mjs` (home: `/music-to-video`, `/product-launch-video`); adoption: `/media-use` `--adopt` → files in `assets/` + manifest records                                                                                                                                                                                         |
| **Publish to a stable link** — the finished piece on a private-by-default hosted URL; re-publishing updates the same link                              | "when it's done I can publish it to a stable link — private by default, or public when you ask"               | `/hyperframes-cli` → `references/preview-render.md` (`npx hyperframes publish`) → a stable hosted URL with explicit visibility                                                                                                                                                                                                                  |

Offer, don't unload: the intent layer recommends the one or two rows the confirmed concept itself calls for, states each as one plain-language line traced to the brief, and asks once — the route-filtered slice on request, the full table for the companion.

## The design ask — have it, pick it, or leave it

The design-spec row is a three-state question, not an explainer (what a spec **is** stays in `design-spec.md`):

- **They have one.** Brand guidelines, a `frame.md`, a `design.md` — note the path in `BRIEF.md` § Assets; the workflow reads it as brand truth (resolution order: `/hyperframes-creative` → `references/design-spec.md`).
- **They don't, but the look matters — show, don't name.** Pick 2–3 shipped presets whose look fits the content, tone, and audience (browse `/hyperframes-creative` → `frame-presets/`), and open each one's `frame-presets/<name>/frame-showcase.html` in the browser so the user picks **by eye**, never from a list of names. The choice lands in `BRIEF.md` as `style_preset` — a remembered preference key, so next run it's the recommended answer with a receipt. On a route that captures a real site, say the honest line as the showcases open: a showcase wears the preset's **own** palette, and the site's brand colors and fonts will be remixed onto whichever preset wins — **the pick is the layout bones, not the colors** — and offer the alternative of deferring the pick until after capture, when the look can be judged with the real brand in hand (a declared deferred ask; the sketch pass shows the remixed truth either way, before anything expensive is built).
- **They don't care — or nothing shipped fits.** Don't care: no further questions; the workflow's design step decides and says why. Nothing fits: announce the **design picker** as a deferred ask — the workflow's design step generates mood boards contextual to their content to choose from (`/hyperframes-creative` → `references/design-picker.md`); it needs a project and a generation pass, so it never runs inside the intent conversation.

## Genre lenses — the shipped workflows' taste, borrowable

The narrative workflows carry genre-tuned design references — `story-design.md` (narrative archetypes and beats), `visual-design.md` (the genre's look), `motion-language.md` + `cut-catalog.md` (motion and cut doctrine). When a companion or freeform piece resembles a genre, read that workflow's lens before planning or building in it (borrowing rule above):

| The piece resembles…                     | Borrow from                                                             |
| ---------------------------------------- | ----------------------------------------------------------------------- |
| a product promo / launch / site showcase | `/product-launch-video` → `references/`                                 |
| a topic / mechanism / concept explainer  | `/faceless-explainer` → `references/`                                   |
| a code-change walkthrough                | `/pr-to-video` → `references/` (+ `code-vocabulary.md` for code frames) |

`motion-language.md` and `cut-catalog.md` are near-identical across the three — take them from the genre you already resembled, or `/faceless-explainer`'s as the neutral default. **Borrow the shape and the taste, never the machinery**: their scripts and directory rules belong to their pipelines; the generic back half of any build lives in `hyperframes/references/production-loop.md`.


<!-- ===== FILE: hyperframes/hyperframes/references/frame-worker-core.md ===== -->

# Frame worker — core contract (shared by the narrative video workflows)

The workflow-agnostic half of every frame worker's role. Each workflow's packet builder (`scripts/frame-packets.mjs`) prepends this file to that workflow's `sub-agents/frame-worker.md` (the **delta**) to form `.hyperframes/frame-packets/_role.md` — a worker reads the two as one role. Editing guidance: a rule that applies to any frame worker belongs here, once; a workflow-specific rule belongs in that workflow's delta. (`music-to-video` has its own composition model and does not use this contract.)

You build the frame composition file(s) assigned in your dispatch and nothing else — sibling workers build the other frames. The structural law behind the constraints and self-check below (sub-composition shape, timeline registration, clip attrs, transform-only motion, determinism, root sizing) lives in `hyperframes-core` (`references/sub-compositions.md`, `references/determinism-rules.md`, `references/data-attributes.md`); everything you must enforce is restated below — open one of those only when a rule here is unclear. This role + your packet also **supersede the skill catalog's own imperatives**: do not open `hyperframes/GUIDE.md` or `hyperframes-core/GUIDE.md` ("read this first" is for fresh requests — that routing already happened upstream, and its output is this dispatch).

**INPUT** — your dispatch provides this role, your frame packet(s), and:

- `PROJECT_DIR` — the project root; all paths are relative to it.
- `frame_id` — e.g. `03-feature`. Use it **verbatim** as the composition id, the `window.__timelines` key, and the file name. Write to the exact `src` in your packet's storyboard block (e.g. `compositions/frames/<frame_id>.html` or `compositions/<frame_id>.html`); the orchestrator derived `frame_id` from that path, and the assembler reads it verbatim.
- Your **packet** (`.hyperframes/frame-packets/<frame_id>.md`) — everything selected upstream for this frame. You never open the shared `STORYBOARD.md` (see below); the packet carries your exact **`## Frame N` block**:
  - `src` — the exact output HTML path, relative to `PROJECT_DIR`. Preserve it; do not add or remove a `frames/` directory.
  - `scene` — a one-line contact-sheet caption. **Design intent, never visible DOM text.**
  - `voiceover` — the narration line. **Timing reference only** (sync entrances to the voice); **never** rendered as text — captions are a separate root track (see constraints).
  - `duration` — your render length in seconds. **Fixed upstream; never change it or tween to fill a different length.**
  - `transition_in` — informational. The injector stamps it at the root; **you do not author transitions.**
  - the **time-coded shot sequence** — your build spec. A sequence of Scene lines (`Scene 1 (0.0–Xs): … → Scene 2: … → Scene N`), each stating what's on screen, what enters / moves / reveals, and the layout inline. Build it faithfully, beat for beat — every Scene window is a phase you must realize, and each reveal lands on its `voiceover` cue (this is what keeps the shot from freezing).
  - `blueprint:` — an id (or the literal `compose`): the shot template this frame instantiates — the overall shape + its signature move. Its body is inlined in your packet (`## Selected blueprint`); `compose` means there's no template — sequence the shot from the Scene lines directly.
  - `focal:` / `roles:` — which element is the hero and what each element is. **Semantics are workflow-specific — see the delta.**
  - `sfx:` — the orchestrator's; you mount no audio.
- The packet also inlines the **rule recipe** (`## Selected motion rule: <id>`) for each named motion the Scene lines cite — the mechanics for that motion, which you reproduce, **never name-guess** (a guess loses the signature move). If a cited motion's recipe is missing from your packet, read `RULES_DIR/<id>.md` (`RULES_DIR` is in the packet header); a few recipes link an optional runnable demo in the shared `../../hyperframes-animation/examples/<id>.html` — open it only when a recipe is unclear.
- `frame.md` (project root) — the **design-truth**: palette, type ramp, components, composition rules. The LOOK. Pull every visual token from here. This is the one file you read outside your packet.
- `references/cut-catalog.md` (the workflow's own copy) — the **cut catalog** (zoom-through / inverse / cut-the-curve / waterfall). When a Scene seam is a within-scene swap, a scene-to-scene cut, or a text-to-text line change, build it INSIDE your composition per this catalog (Z-scale + blur + opacity, or per-word x-staggers). You never author the between-frame transition — story's `transition_in` + the injector own that.
- Canvas `<width>×<height>` and `Captions: <enabled | disabled>` (+ the keep-out cutoff when enabled).

**Retry** — if your context carries `lint` / `check` feedback from a prior pass, read it first and re-author so none of those findings recur; treat each as a hard constraint.

**OUTPUT** — the HTML file at each assigned packet's `src`: exactly one bare `<template>…</template>` fragment. The first non-whitespace bytes are `<template`; the last are `</template>`. Never emit `<!doctype>`, `<html>`, `<head>`, `<body>`, or any markup outside that single template. The workflow delta specifies any required sidecars and the dispatch specifies which packets you own. Writing all assigned HTML files and required sidecars (past the self-check below) is your **terminal action** — you do not edit `STORYBOARD.md`, mint audio, assemble the index, run the CLI, or report back. The orchestrator picks up the file and marks the frame's `status`.

## When a confirmed sketch exists

In collaborative runs the orchestrator first poses every frame in its composition and shows it as a still on the board (`boards/storyboard.html`, stills in `boards/stills/`, format in `hyperframes-creative/references/storyboard-recipe.md`), so your frame may have a **user-confirmed wireframe**: the posed composition at your target file — your dispatch says whether it does (a target file found on a retry is your own prior output, not a sketch). Read that file and its still first and **keep its composition**: the placement, hierarchy, and copy were approved — don't move or drop them. Everything else is yours to finish: the finished content where the sketch used stand-in blocks (what that content is — real assets, invented visuals, a code block — is the delta's call, since the sketch already carries the full `frame.md` treatment), and the motion — map each Scene onto a timeline phase, reveal each piece on its `voiceover` cue with `fromTo` entrances, adding DOM only where a phase needs it. The frame's landed state must still read as the approved sketch, now moving.

## You do NOT decide

These belong to other steps — touching them collides with a sibling or breaks an upstream contract:

- **What is SAID** — narration is locked in `SCRIPT.md` / the `voiceover` line. You only show; you never write or restate narration text.
- **Duration** — fixed from real voice timing. Build your shot to land within it; don't stretch or trim it.
- **Transitions between frames** — the injector stamps them onto the root timeline. You author the shot itself (the VO-paced reveal sequence) but **never an exit** — the root transition IS the exit; a settle / fade-out only if you are the final frame.
- **Audio** (narration / BGM / SFX) — assembled at the root by the orchestrator. **No `<audio>` element in your composition.**
- **Design tokens** — palette / fonts / components come from `frame.md`. Don't invent them, and **never lift a word, label, or wordmark out of `frame.md` as your copy** — it is a style spec, not content. Visible text comes from your frame's `scene` / narrative.
- **Which motions / assets exist** — named upstream in your block (the shot sequence's motion verbs + `blueprint:` + the delta's own vocabularies). Implement them; don't fetch or invent new ones (you have no asset-fetch tool — never fabricate an asset URL or reference a file the dispatch didn't name).
- **The shared `STORYBOARD.md`** — your packet carries your block; never open or write the file itself. N siblings edit nothing there concurrently; the orchestrator owns its state.

## Frame constraints

Shared law for every narrative frame, each load-bearing; your workflow's delta adds its own on top:

- **Caption keep-out — all content in the top ~83%.** A karaoke caption pill owns the bottom ~17% of the canvas. Keep every element (headline, cards, code panel, diagram, stats, brand mark) above `y ≈ 0.83 × height` — compute the pixel cutoff from your canvas (e.g. `≤ 900` on a 1080-tall frame, `≤ 1600` on a 1920-tall portrait). Holds **even when `Captions: disabled`** (bottom-edge consistency across frames).
- **Fill the content area — especially portrait.** Compose the whole top-83% region; don't float one small cluster mid-frame. Anchor the hero high (~0.2–0.35 × height), flow supporting elements down with rhythm, scale the hero toward full-bleed. (Landscape's region is short, so vertical centering near 0.42 × height is fine.)
- **Visible text is short motion-graphics copy** — a hero word / stat / one-word emphasis (`"$83K"`, `"2× faster"`, `"INSTANT"`), never a sentence from the narration. The root caption track already shows the spoken words synced to voice; repeating them double-prints on screen. (The delta may name exceptions — e.g. real code inside a code block is content, not narration.)
- **Build the whole shot — reveal across the full `duration`, never front-load.** Dumping the whole canvas in the first ~25% then holding it is exactly what reads as a PowerPoint slide. Instead reveal each piece — a line, a card, a node, a stat — **as the `voiceover` reaches it** (on a silent frame, on the beat), sequencing reveals across the shot and especially the back ~50%, with the macro camera move running underneath. **Only EXITS are banned** — a non-final frame unmounts mid-frame, so an exit tween truncates and reads as a glitch (the root transition IS the exit); mid-shot reveals are free and seek-safe. The lone exception is a note marked as a deliberate hold / stillness frame: there, an entrance + a quiet settle is right (a held read beats bad motion).
- **Implement the shot sequence faithfully — every Scene is a timeline phase.** The Scene lines ARE the build: map each Scene onto a phase of the one timeline, each piece revealing as the `voiceover` reaches it. For each **named motion** in a Scene, reproduce the mechanics of its inlined rule recipe — **never name-guess**. The inlined **`blueprint:` template** gives the overall shape; keep its **signature move** recognizable, then instantiate it with this frame's content / assets / timing. `compose` → no template; sequence the shot straight from the Scene lines. Whichever, never front-load the whole sequence at `t=0` — pace the reveals to the voiceover.

## Workflow

1. **Read** — your packet top to bottom (your frame block, the inlined blueprint, the inlined rule recipes), then `frame.md` (the look). Internalize the self-check codes below before you write — most lethal is **template transport**: every `<style>` + `<script>` (including the gsap load) must live INSIDE `<template>`, because the runtime only clones template contents and the assembled-project `lint` / `check` gate can miss an unwired blank sub-composition.
2. **Design** — turn the time-coded shot sequence into a timeline using `frame.md`'s components and type ramp: each Scene window becomes a phase revealed on its `voiceover` cue, each named motion built from the recipe in your packet, the blueprint's signature move kept recognizable. Find a visual idea that reinforces the beat, not a literal restyle of the words.
3. **Author** — write the full sub-composition to the exact `src` in your packet (rewrite to iterate; last write wins). `<template>`-wrapped root carrying `data-composition-id="<frame_id>"` and styled via `#root` (not a class on that element — see the self-check below), exactly one `gsap.timeline({ paused: true })` registered at `window.__timelines["<frame_id>"]`, built synchronously.
   Prefix authored ids and globally reusable class names with `<frame_id>-` so sibling frames assembled from parallel workers cannot collide. Contract selectors such as `#root` and `.clip` are the only exceptions.
4. **Self-check, then finish** — re-read your file against the checklist below and fix in place; write any sidecar required by the workflow delta, then continue to your next assigned packet, if any. You do **not** run the CLI.

## Self-check before finishing (you do NOT run the CLI)

You **can't** meaningfully run `hyperframes lint` / `check` here: they operate on the **assembled project** (the `index.html` graph / bundle), and your frame isn't wired in yet — so they report on _other_ files, not yours (a false green). The **orchestrator** runs them after assembly (the correct unit), and **re-dispatches you with the finding** if your frame fails (see **Retry** above). So get it right on write: re-read your file against this checklist before finishing — backticked diagnostic codes below are emitted by `hyperframes lint`; bold labels are manual workflow checks, not lint codes:

- **Template wrapper (manual)** — the entire file is exactly one bare `<template>…</template>` fragment (no DOCTYPE / full document).
- `root_missing_composition_id` — root carries `data-composition-id="<frame_id>"`; check that the value matches your assigned frame id.
- **Template transport** — every `<style>` and `<script>` block, including the GSAP load, lives inside `<template>`.
- `subcomposition_root_styled_by_class` — **style the frame root via `#root`, never a class on the `data-composition-id` element**: at render a class on the root gets scoped to a descendant selector that can't match it, so the **whole scene renders unstyled** (Studio preview still looks right — trust this rule, not the preview). Descendants use plain selectors.
- **Full-bleed background on a `class="clip"` layer, never `#root`** — author a frame's full-bleed ground (color field / gradient / grid) as a dedicated full-duration `class="clip"` background element on the lowest content track, **not** as a `background` on the `#root` / `data-composition-id` element. At assembly the frame root is clip-gated to its scene window, so a background painted on the root is not a dependable full-frame ground — dark content can end up over the host `body` (black) and render invisible. The video's base ground is painted separately by the assembler from `frame.md`'s `canvas` color onto the index `#root`; your full-bleed clip rides on top of it.
- **Clip attributes (manual)** — every `class="clip"` element has `data-start` / `data-duration` / `data-track-index`.
- **Paused timeline + registration (manual for template frames)** — one paused timeline, registered at `window.__timelines["<frame_id>"]`. `gsap_timeline_not_registered` is a real lint code for standalone compositions, but the rule skips template/sub-compositions; it does not verify your frame registration.
- `css_transition_used` + repeat / yoyo / non-deterministic logic — none present (the renderer seeks frame-by-frame).
- `gsap_css_transform_conflict` — never put a CSS `transform` (e.g. `translateY(-50%)` centering) on an element you then GSAP-animate a transform prop on (`x` / `y` / `scale` / `rotation`): GSAP overwrites the whole `transform` and silently drops the CSS centering (the element jumps). Center with `margin` / `inset` (or `top`/`left` + offset), fold the offset into the tween via `xPercent` / `yPercent`, or use `fromTo` (the rule exempts it).
- **Hero visibility** — the main subject is visible by `t <= 0.5s`; entrance tweens use `fromTo` instead of CSS-hidden starting states.
- **Non-final exit (manual)** — no exit tween unless you are the final frame.
- **No front-loading (not a slide)** — the shot's pieces reveal on their `voiceover` cues across the duration, not all fired at `t=0`; a non-still frame keeps content arriving rather than holding a full canvas from ~25%.
- **Shot-sequence fidelity** — every Scene in the time-coded sequence is realized as a phase, the blueprint's signature move (unless `compose`) is present and recognizable, and the shot reveals to the voiceover (never front-loaded at `t=0`).
- `font_family_without_font_face` — every font you name has a matching `@font-face` **inside this file**. **Only use fonts that ship as files** with the project: the families declared in `frame.md` (their `.woff2` live in `assets/fonts/` or `capture/assets/fonts/` — point the `@font-face` `src` at the real file you find there). **Never name a font that has no file**, including system CJK / Japanese / Devanagari families (`Hiragino Sans`, `Yu Gothic`, `Noto Sans CJK`, `Noto Sans Devanagari`, …): the render machine is a clean headless Chrome with none of them installed, so the text silently falls back to a generic font and the typography is wrong in the MP4. For non-Latin or multilingual visible text, either use a shipped font that covers the script, or romanize / transliterate it (e.g. `日本語` → `Japanese`); if neither is possible it is out of scope for this frame — do not invent a font name.
- **Keep-out + no-narration-text** (eyeball, no code) — nothing sits below the 83% cutoff; no narration sentence is rendered as visible text.


<!-- ===== FILE: hyperframes/hyperframes/references/intent-interview.md ===== -->

# The intent layer — one conversation, before any workflow runs

Fresh creation only — the GUIDE.md state table already decides whether this layer runs at all (edits, project operations, briefed and resumable projects, and explicit Remotion ports never enter it). One conversation at the front door turns "make me a video" into a confirmed brief — the route, the must-have answers, the run's shape, and everything else in the user's head — handed to whichever workflow executes and made durable as `BRIEF.md`. Workflows own execution; this layer owns understanding. Every workflow's opening rule points back here, so the questions are asked once no matter which door the user came through.

The one exception: a follow-on to the same film (a new version or a cutdown) asked for inside an existing project runs this layer as `/hyperframes-studio` § 5 describes, without `hyperframes init` and without overwriting the project's brief.

These reads are mandatory when their condition matches; do not replace them with recollection:

| Condition                                                   | Read before acting                                                   |
| ----------------------------------------------------------- | -------------------------------------------------------------------- |
| The route is picked, before confirming or interviewing      | `routes/<workflow>.md` — the whole file (contract + interview, ~1KB) |
| Triage judged the request unformed, before any concept work | `pitch-round.md`                                                     |
| Offering optional capabilities or collecting supplied media | The route-filtered rows in `capability-menu.md`                      |
| Question rules or field semantics beyond the schema below   | `brief-contract.md`                                                  |

## Adapt orthogonal inputs first

A Figma source changes **how assets and design enter the project**, not which workflow owns the deliverable. If any input is a `figma.com` URL: complete this layer's memory and recipe reads; during input triage run `/figma` to extract assets, brand tokens, components, and storyboard frames when present; route the requested deliverable using the output from `/figma`, then continue only the selected route's unanswered questions. Do not drive Figma through raw MCP tools — that bypasses SVG sanitization, `.media/manifest.jsonl` provenance, and brand-token `var()` binding.

A GitHub PR URL is not a website source. A named or adopted recipe already carries its workflow; confirm adoption below, then route to that workflow.

## The eight steps

**1 — Memory before questions.** Two reads, both mandatory, before anything is asked:

- **Remembered defaults.** Let `<MEDIA_DIR>` be the installed `/media-use` skill directory. For an existing project, `<MEMORY_ROOT>` is its root. Before scaffolding, use a deliberately nonexistent probe path with no `.media`, such as `/tmp/hyperframes-intent-memory-<run-id>`; never use the current workspace. Run `node <MEDIA_DIR>/scripts/prefs.mjs get --hyperframes <MEMORY_ROOT> --json`. Make each remembered value the recommended option and name its source. The pre-project probe sees only the personal tier; do not claim project provenance.
- **Recipes.** Run `node <MEDIA_DIR>/scripts/recipe.mjs list --hyperframes <MEMORY_ROOT> --json`. If the user names a recipe, says "like last time," or a recipe matches the probable route, ask whether to adopt it before other brief questions — and make the offer earn the yes: say why it matches and what adopting saves ("this matches your launch-promo recipe — adopting fills destination, aspect, language, and the design spec; you'd confirm the message and the two run-shape questions"). When several match, list them and include "none." An adopted recipe locks the fields it contains; ask only its missing fields and the run-shape questions. It does not remove review or render approval gates.

**2 — Triage the input.** What is the video about — a website (sold or shown), a PR, a topic, a music track, existing footage? And is the request **formed** — the message, the material, and the occasion readable from what the user gave — or **unformed**, a subject with no take on it? Source material doesn't settle this by itself: a site, document, or PR carries its own thesis, but five tellings of that thesis are five different videos — a request whose only shape comes from its source ("make a video about this URL") is formed about the facts and unformed about the telling, and enters the round to pitch the telling. A formed request runs the layer exactly as it always has; nothing below is added for it. An unformed one goes through the pitch round after routing (step 4) and earns one question here, before anything is generated: what is the user already picturing? Their answer seeds the round (`pitch-round.md`). A user who says they don't know video at all gets that reference's decision map instead of a question sequence. For a genuinely exploratory request ("we need a video but I'm not sure what kind"), don't interrogate — establish the subject and what exists to show, one question at a time, then close by **recommending** a route plus how the run will review: a plan in chat first, with optional stills on a board (`boards/storyboard.html`, format in `hyperframes-creative/references/storyboard-recipe.md`) before the full build (`review-loop.md`). The user hears the process before any workflow starts.

**3 — Pick the route** (the route table and ambiguity rules in the GUIDE.md), then read `routes/<workflow>.md`. Its Interview section lists the must-have questions to ask now, the **deferred asks** to announce, whether the two run-shape questions apply, and which fields the pitch round may answer.

**4 — The pitch round** — unformed requests only; formed requests and recipe adoptions go straight to the must-haves. Sample five concepts along five genuinely different paths, at least two from the distribution's tail, and present them all before recommending one — pick, mix, and redirect are all answers. Each pitch names the capability or two it rides, in the plain language of `capability-menu.md` — the toolbox experienced as concepts, not listed as a menu. On an autonomous run the same gate runs internally, and the heads-up names the direction chosen and the typical one left behind. The procedure — the sampling gate, the presentation discipline, and the decision map for users new to video — is `pitch-round.md`. The chosen concept answers the route's pitch-eligible fields and lands in `BRIEF.md` under `## Intent`; the capabilities it named are confirmed with it, under `## Customizations`.

**5 — The route's must-haves.** One question per field, recommended option first with its receipt (rules: `brief-contract.md` § 3). Skip a question only when the request already answered it — inference is not an answer, but a chosen pitch is: fields the pitch round settled are locked with the pitch as their receipt. Then announce the route's deferred asks in one line ("after I probe the clip, I'll offer 2–3 caption identities") so the user hears the run's full shape before it starts.

**6 — The two run-shape questions** — where the route's entry applies them, asked after the must-haves, each on its own:

- **(a) Storyboard?** Review the plan in chat, stills on a board (`boards/storyboard.html`, format in `hyperframes-creative/references/storyboard-recipe.md`), and the finished piece pass by pass (`review-loop.md`) — recommended for anything beyond a couple of scenes — or skip the review and get one finished video from the confirmed brief.
- **(b) Automation or companion?** **Automation** — the matched workflow's pipeline executes the brief end to end. **Companion** — build it together in `/general-video` with every HyperFrames capability on the table; the route's answers still describe the video, general-video executes them.

These two are **orthogonal — never merge them into one menu.** All four `flow` × `storyboard` combinations are valid user choices (a companion run runs the same review passes when `storyboard: yes`); a flattened three-option list ("storyboard review / one shot / companion") silently makes companion-with-storyboard unselectable. When a diagram or source material summarizes the outcomes as three branches, that is the derived behavior (`brief-contract.md` § 1), not the question shape. In a form-style question UI, keep (a) and (b) as two separate selects.

Signals replace questions, never add them: an ongoing "just build it" / "surprise me" / "don't ask" locks `flow: automation, storyboard: no`, and every unanswered field becomes a decision with a receipt in the heads-up. A storyboard request, however phrased, locks `storyboard: yes`. Remembered `flow` / `storyboard` values reorder the recommendations — they never make either question disappear. The run's collaborative/autonomous execution mode derives from these two answers — the old first question is never asked; the canonical mapping is `brief-contract.md` § 1.

**7 — Nice-to-have: recommend, then show.** Skip this step when the selected route file says to skip the front-door capability offer. Otherwise, once the must-haves are locked, send one offer, not an interrogation — recommendations first, catalog on request. Capabilities the chosen pitch already named are settled with the concept — this step recommends from what the pitch didn't cover, and after a pitch round it is often just the two open asks and the design ask:

- **One or two rows** of `capability-menu.md` that this brief specifically calls for, each traced to something in the confirmed concept — a key number wants the count-up treatment, product shots want staging and a grade, a music bed means cuts on its grid. A suggestion that would fit any video fails that test; drop it. At most one may be a labeled **challenger**: higher ceiling, named cost ("the standard cut carries it; shader transitions would lift the close, at render-time cost").
- **Material answered on arrival.** When the user hands over a logo, a clip, or data, answer with its concrete use ("the logo could close the video as a sting — want that?") rather than silently filing it.
- **The two open asks stay:** anything here you want, and is there any material of your own (images, clips, logos, data) the video should carry?
- **The design spec keeps its own three-state ask** — use an existing spec, pick a shipped preset by eye, or leave the decision to the workflow (`capability-menu.md` § The design ask).

The full route-filtered slice appears only when the user asks what else is possible. An accepted recommendation is a confirmed answer: when it lands on a preference-backed field (a preset, a voice, a caption identity), it records like any other confirmation, and `/media-use`'s promotion rules make it the next run's recommended default. Capture answers verbatim in `BRIEF.md` under `## Assets`, `## Customizations`, or `## Notes`. One round; silence or "no" moves on.

**8 — Hand off.** Three disciplines close the conversation (invariants: `brief-contract.md` § 3):

- **One integration check.** Read the combined answers for a consequence no single answer showed — vertical at 90 seconds with a chart-dense concept means charts a phone can't read — and surface it with a proposed adjustment now, not at the sketch pass.
- **Stated and inferred, apart.** Present the locked brief as one summary — deferred asks and the run's shape included — with what the user answered and what was inferred or defaulted as two visibly separate groups, receipts on both. The inferred group is where corrections live; an autonomous heads-up is mostly that group.
- **Revision is not confirmation.** When the user corrects the summary, fold the change in and present it again; never execute an edited-but-unconfirmed brief.

Then enter the workflow (`flow: companion` → `/general-video`; otherwise the matched route), installing it first per the GUIDE.md's install step. The workflow's Setup writes `BRIEF.md` from this summary as its **first action after `hyperframes init`** (never before — `init` refuses a non-empty directory), using the canonical frontmatter below and preserving the user's important wording in the body — the chosen pitch, when there is one, under `## Intent`. It then records the preference-backed fields (`brief-format.md` names the subset), and asks no brief question again.

## BRIEF.md frontmatter — the carry-away artifact

The interview's deliverable. Every later "what did the route require?" re-reads this ~1KB file, never this document. One key per confirmed field, canonical normalized values (full shape and body sections: `brief-format.md`):

| Key                                                                       | Meaning                                                                                        | Example                     |
| ------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------- | --------------------------- |
| `workflow`                                                                | the executing workflow (companion runs record `general-video`)                                 | `faceless-explainer`        |
| `flow`                                                                    | `automation` — the matched workflow's pipeline · `companion` — co-creation in `/general-video` | `automation`                |
| `storyboard`                                                              | `yes` — plan and sketches reviewed before the build · `no` — one shot from the confirmed brief | `yes`                       |
| `message`                                                                 | the ONE thing the video must communicate                                                       | `"Ship it in an afternoon"` |
| `destination` / `aspect` / `language` / `audience` / `length` / `angle` … | the registry fields this route confirmed                                                       | —                           |


<!-- ===== FILE: hyperframes/hyperframes/references/pitch-round.md ===== -->

# Pitch round — the intent layer's divergent step

Everything else in the intent layer converges: recommended options, receipts, one question per field. This step diverges. An unformed request has nothing to converge on — "make us a video about the launch" answers no creative field, and asking `message` as a form question hands the user the very blank they came to have filled. So before the form, pitch: five concepts, sampled wide, offered once.

## When it runs

Triage (`/hyperframes` → `references/intent-interview.md`, step 2) marks the request formed or unformed; only unformed requests enter the round, and only on routes whose `routes/<workflow>.md` entry names pitch-eligible fields. A recipe adoption skips the round — the bundle already carries an approved concept. An autonomous signal never skips it; it moves the round inside (§ The gate, alone).

Before generating anything, ask what the user is already picturing. An existing idea seeds the round as a pitch of its own and is never displaced by generated ones; a fully formed picture ends the round before it starts — that picture is the concept, and the layer returns to its questions.

## The sampling gate — internal, always

Run this before writing any pitch, in every mode. None of it is shown to the user.

First, four questions about this brief, answered specifically, not generically:

1. **What does the subject look like?** Its own visual world — an island-travel piece has whitewashed walls and caldera cliffs; an outage postmortem has terminal green and a scarred timeline. The subject's vocabulary drives the layouts.
2. **What does the target emotion look like as a frame?** Longing is empty space the viewer wants to fill; urgency is compression; awe is one element too large for the canvas.
3. **What does the playback surface demand?** A lobby screen is ambient and glanced at; a feed fights for its first second; a story is vertical and fast.
4. **What does every other video on this subject look like?** That is the anti-pattern. The tail pitches must not be it.

Then five concepts, one from each path: the subject's world · the emotion · the audience (meet their expectation, or break it) · the anti-pattern, inverted · an unusual format (a letter, a countdown, a recipe, a front page, a map). Estimate for each the probability that a model handed this brief would produce it. The numbers are directional, not calibrated, and they exist to enforce one constraint: **at least two of the five must sit below 0.10.** If all five clear 0.10, every pitch is the median — start over. Then check silhouettes: sketch each concept's major elements as rough bounding boxes; two concepts with the same silhouette are one concept, so replace one.

Probabilities never reach the user. They are a sampling constraint, not a scorecard.

## Presenting the round

Each pitch is three lines: the concept in one sentence, its visual world, its opening hook. The visual-world line carries the machinery: name the one or two capabilities the concept rides, in the plain language of `capability-menu.md`'s middle column — "the launch number counts up on the track's beat grid," never a feature name. This is how the toolbox reaches the user: experienced inside a concept they can want, not listed in a menu they can't evaluate. Machinery earns its mention the way a recommendation earns its place — a capability that would fit all five pitches is decoration; name it only where this concept leans on it.

All five appear before any recommendation — a recommendation stated first anchors everything after it. Then recommend one, with a reason. Mixing is a first-class answer ("the framing of the second with the opening of the fourth"); silence or "you decide" accepts the recommendation. One round: the pitches are an offer, not a quiz, and there is no second batch unless the user asks for one.

The chosen concept **is** the brief's creative core: it answers the route's pitch-eligible fields (typically `message` and `angle`), those questions are skipped downstream with the pitch as their receipt, and the concept lands in `BRIEF.md` under `## Intent` in the wording the user accepted. The capabilities the pitch named are confirmed with it — they land under `## Customizations` and are not re-offered later as if they were new.

## The gate, alone — autonomous runs

"Just build it" changes the audience, not the discipline. Walk the same gate — four questions, five concepts, tail constraint, silhouette check — pick the winner, and keep building. The heads-up then treats the pick like every other receipt-backed decision: name the direction chosen and why, the machinery it rides, and the most typical direction deliberately left behind. An autonomous run is where the median is most dangerous — no one is present to say "this looks like every other video," so the gate has to say it.

## The decision map — "I don't know anything about video"

A user who says they can't judge any of this gets neither pitches nor a question sequence. Give them a map of the two or three decision surfaces where their input genuinely changes the outcome — where it will play, how long it should run, what it should feel like — each with two to four plain-language options and a marked default. They choose only where they can tell the difference; every untouched surface keeps its default with a receipt. Then run the gate autonomous-style and present the winning concept inside the brief summary, where accepting the summary accepts the concept.


<!-- ===== FILE: hyperframes/hyperframes/references/plugin-installation.md ===== -->

# Running from an installed plugin

Check the directory two levels above the loaded `GUIDE.md` for `plugin.json`,
`.claude-plugin/plugin.json`, `.codex-plugin/plugin.json`, or
`.cursor-plugin/plugin.json` identifying `hyperframes`, or a Gemini extension manifest.
That directory is `<PLUGIN_ROOT>`. If none exists, this is a standalone skill;
follow the normal installation and freshness instructions.

For a plugin installation, these rules replace the standalone update commands
in every workflow and reference:

- Do not run `hyperframes skills update`, `skills check`, or `npx skills add`.
  The agent's plugin manager owns installation and updates. Read the workflow at
  `<PLUGIN_ROOT>/skills/<name>/GUIDE.md`; report a missing bundled skill instead
  of downloading a different release. Resolve all skill references inside this
  bundle, even if a standalone copy is also installed. Claude exposes the router
  as `/hyperframes:hyperframes`; other clients may expose `/hyperframes`.
- Replace `npx hyperframes` (or bare `hyperframes`) in command examples with:

  ```bash
  node "<PLUGIN_ROOT>/skills/hyperframes/scripts/plugin-cli.mjs" <command> <args...>
  ```

  Run in the user's project directory, never in the plugin directory. The launcher
  selects the manifest's CLI version and disables automatic standalone skill
  installation, including during `init`. The first call may download that exact
  CLI version through npm. A download failure is an error, not permission to use
  latest. Existing project dependency files and lockfiles must not be overwritten
  to match the plugin; surface a runtime incompatibility before changing them.

- For bundled Node helpers, use the same
  launcher with `--script <absolute-script-path> <args...>`. This passes the
  release version to their dependency loader. External providers, registry
  downloads, and existing project dependencies have their own versions; a plugin
  version alone does not freeze those inputs.
- Treat the plugin directory as read-only. Put outputs and temporary work in the
  project or a temporary directory. Pass this plugin root and launcher convention
  to any delegated workflow so it does not fall back to global skills.

To get newer skills, use the client's plugin update flow and reload the session.
Do not silently update an installed plugin during a video task.

The launcher suppresses CLI update notices as well as standalone skill refreshes, including when running an older CLI with a stale notice cache. It passes the release as `HYPERFRAMES_PLUGIN_VERSION` for plugin-aware helpers and as `HYPERFRAMES_SKILL_PKG_VERSION` for the existing helper-package bootstrap. Our release process versions those packages together.


<!-- ===== FILE: hyperframes/hyperframes/references/production-loop.md ===== -->

# Production loop — from an approved plan to a delivered video

The stages between a plan the user has agreed to and a video in their hands, written as **dependencies, not numbered steps**: order between independent stages is free — audio renders in the background while frames build; that is the standard trick — order inside a dependency chain is not. Nothing in this file addresses the user: every user-facing pause lives in `review-loop.md`, and this file only marks where those passes attach. Some routes bring their own spine (a beat grid, existing footage) — the stages compose around it. A stage whose need is absent simply doesn't run: no narration, no audio stage; a single scene, no transitions. An edit request enters at the artifact it touches and re-runs verify.

The shipped narrative workflows implement these stages with their own scripts; a freeform build follows this file directly, borrowing tools where the capability menu says they live (`hyperframes/references/capability-menu.md`).

| Stage               | Needs                                                                                                                                                                                                                             | Produces                                                                                                                                                                                                       | Where the capability lives                                                                                                                    |
| ------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------- |
| **Blocks & assets** | the approved plan                                                                                                                                                                                                                 | registry blocks installed **once, before any parallel work** (parallel workers race the registry); user assets staged; logos / images / grades resolved                                                        | `npx hyperframes add <block>` per block the plan names; staging, adoption, and `resolve` via the menu's media rows                            |
| **Audio**           | narration text (when narrated); the storyboard's `music:` mood                                                                                                                                                                    | voice files + **word timings** + BGM + SFX → `audio_meta.json`; **when BGM plays under a voice, the bed is carved** (`hyperframes-audio/scripts/carve.mjs`) before Verify — a duck alone is not a finished mix | the one engine — `media-use/audio/scripts/audio.mjs`, run in the background; `wait-bgm.mjs` before render when BGM generates                  |
| **Frames**          | design spec + the plan (+ a confirmed still on the board (`boards/storyboard.html`, format in `hyperframes-creative/references/storyboard-recipe.md`) when one exists — dress that layout, never redraw it: `review-loop.md` § 3) | each scene at `compositions/frames/NN-*.html`, marked `animated` in the storyboard as it lands                                                                                                                 | `frame.md` + `hyperframes-animation` blueprints / rules (+ the genre lens, menu § Genre lenses); parallel dispatch per `subagent-dispatch.md` |
| **Duration sync**   | word timings + frames                                                                                                                                                                                                             | scene durations trued to real voice length — real duration wins, silent scenes keep estimates, synced values are never hand-edited                                                                             | a mechanical rule; the narrative workflows' audio scripts apply it, a freeform build applies it by hand                                       |
| **Assembly**        | frames                                                                                                                                                                                                                            | the index composition — scenes as sub-compositions on tracks                                                                                                                                                   | `sub-compositions.md` + `tracks-and-clips.md`; borrowable `assemble-index.mjs` (menu)                                                         |
| **Transitions**     | the assembled index                                                                                                                                                                                                               | scene handoffs injected                                                                                                                                                                                        | `hyperframes-animation/transitions/overview.md` → `catalog.md`; borrowable `transitions.mjs` (menu)                                           |
| **Captions**        | word timings + the index                                                                                                                                                                                                          | the caption track                                                                                                                                                                                              | borrowable `captions.mjs` (menu); no script to time against → `media-use` `scripts/transcribe.mjs` first                                      |
| **Verify**          | the index (+ captions / transitions when present)                                                                                                                                                                                 | `npx hyperframes lint` and `npx hyperframes check` **passing**; a contact-sheet glance (`snapshot --at <frame-midpoints>`)                                                                                     | `hyperframes-cli`                                                                                                                             |
| **Deliver**         | verify passing                                                                                                                                                                                                                    | the final-look pause → on approval `render` → optionally `publish` (a stable hosted link, private by default) → the recipe offer                                                                               | final approval and recipe offer: `review-loop.md` § 4; render / publish: `hyperframes-cli`                                                    |

The Frames stage follows the plan's citations: a scene planned on a blueprint or on named rules is built by reading that recipe's body (`hyperframes-animation/blueprints/<id>.md`, `rules/<id>.md`) before its motion is written — names come from the indexes, never invented, and a scene the plan left uncited gets its citation at build time, not improvised motion.

## Scheduling economics (facts you can't see from inside the session)

- **External generations are independent work.** Image plates, TTS, BGM, video gen: fire every generation whose prompt is already known **concurrently or in the background**, and overlap the wait with reading or building. Three image plates generated one-after-another cost ~3× the wall time of firing them together.
- **Attaching an image re-prices your whole context.** A mid-session image inspection (especially at original detail) invalidates the prompt cache — the next request re-sends your entire history at full price. Batch visual checks (one contact sheet beats N single-frame views) and schedule them at phase boundaries, not mid-build.

Two attach points carry the user's voice into this loop: the plan that starts it was approved at `review-loop.md` § 1 (collaborative) or posted as a heads-up (autonomous), and nothing renders before the § 4 final look. Everything between those two is yours to schedule.


<!-- ===== FILE: hyperframes/hyperframes/references/review-loop.md ===== -->

# The review loop — plan, sketch, build

How a `storyboard: yes` run earns fidelity one pass at a time: the plan is reviewed as text in chat, the layouts as stills on the board (`boards/storyboard.html`), and the finished piece as the assembled video. Collaborative mode waits at each checkpoint. Autonomous mode posts the same checkpoint summaries and continues, keeping exactly one question before render.

This is the shared process for any workflow that plans on a storyboard. The contracts it leans on live next door: interaction mode and gate types in `brief-contract.md`; the `STORYBOARD.md` format and the `outline → built → animated` statuses in `storyboard-format.md`. How to make the storyboard itself, and the page it is reviewed on, is `hyperframes-creative/references/storyboard-recipe.md`. A workflow's GUIDE.md says **when** its steps hit each pass and supplies its **sketch stand-ins** (what the plain blocks represent); how the loop runs is defined here, once. The stage mechanics between the passes — audio, frames, assembly, transitions, captions, verify — live in `production-loop.md`; this file owns only the user-facing pauses.

## § 1 — The plan, in chat

Write the decisions and beat list into `STORYBOARD.md` following the recipe, and present the plan in chat as a proposal (shape: `hyperframes-creative/references/story-spine.md` § 3): open by echoing **"This video tells [audience] that [message]"**, then the frame table — one row per frame: frame · beat (type, duration) · on screen · why (its `narrativeRole`, traced to the message). Feedback arrives as a reply here, one revision loop.

In the same message ask two things: **(a)** approve or request changes, and **(b)** **sketches first** (recommended — a quick look at the layouts right after this approval) or skip sketches and build in one go. Iterate until approved: revise exactly the frames the reply names and re-present.

This is a **checkpoint gate** (`brief-contract.md` § 1). A run that starts autonomous normally has `storyboard: no` and does not enter this loop. If mode switches to autonomous mid-run, keep `STORYBOARD.md` current, post the same summary as a heads-up, and continue without waiting; the one kept question comes at § 4.

## § 2 — The sketch pass (collaborative, unless skipped)

The moment the plan is approved, sketch every frame yourself — no sub-agents, no waiting on other steps (sketches don't use timings), straight from the approved frame table.

A sketch is a **static frame, not an unstyled one**: the frame's layout at its key moment, posed in the composition with the full `frame.md` treatment (real fonts, real colors, the actual headline / stat / label text placed where it will live) as `storyboard-recipe.md` § 1 describes, using plain blocks only for panels, charts, diagrams, and media the workflow hasn't produced yet (the workflow says what its blocks stand in for). **No motion** — that arrives with the build pass; the layout, copy and brand treatment are already locked here.

Mount the posed frames in `index.html`, snapshot every still in one run into `boards/stills/` and write the board, `boards/storyboard.html` (`storyboard-recipe.md` § 1–2), then hand the user the board. Mark each frame `built` in `STORYBOARD.md` as its still lands. `snapshot` is the only CLI here — no `lint` / `check`, no rendering. When every frame is `built`, pause and ask one thing: does the board look right, or which frames change? This is a **checkpoint gate**; feedback arrives in chat: re-pose **only the frames named** and replace only their stills (`storyboard-recipe.md` § 1 step 4), rewrite the page, re-present, and loop until the layout is confirmed. Only then does the workflow's visual design get written onto the confirmed layouts.

A confirmed board is also a valid place to **stop**. When the user asked for a storyboard rather than a finished video — a plan to pitch, review, or hand off — `boards/storyboard.html` is the deliverable: confirm it, hand over the path, and go no further unless asked to build.

In autonomous mode, or when the user chose to skip sketches at § 1, skip this pass — frames go straight from `outline` to `animated` in the build.

## § 3 — Building on confirmed layouts

However the workflow builds — sub-agent workers per frame, or inline scene by scene — a confirmed sketch's **composition is settled**: placement, hierarchy, and copy were approved on the board, so building means dressing that layout (full design treatment, real assets, motion), never redrawing it. Workflows that dispatch workers put "this frame has a **confirmed sketch** (its posed composition, still in `boards/stills/`)" in the worker's context and carry the keep-the-layout rule in their worker prompt; a landed frame must still read as the approved wireframe, fully dressed.

Mark each frame `animated` as it lands. The build gate carries the loop's condition: in collaborative mode, the board was confirmed at § 2.

## § 4 — The final look

After the workflow's checks pass, use the **final composition preview**. In both modes open the Studio preview — on the user's own machine it opens in their browser by itself; on a remote machine or sandbox, say where it runs, since localhost may not reach them — hand the timeline URL and ask one thing: render now, or what changes? In autonomous mode this is the one question the mode keeps, and the preview still opens first: a user who asked only for a video has no other way to learn they can watch and edit it before the render. Render only on approval. Leave the preview running after the render, since the user may keep editing there, and say how to stop it: `npx hyperframes preview --stop`.

**After approval, offer the recipe — once.** An approved run is a proven bundle. At delivery, offer to freeze it: `media-use` → `scripts/recipe.mjs freeze --name <name>` (the workflow comes from BRIEF.md; pass `--workflow` only in a project without one) keeps the design spec, the storyboard skeleton (structure kept, content blanked), the brief skeleton, and the confirmed brief values, and the next run of this type starts from it (the intent layer checks for a matching recipe before its first question). When the freeze lands, teach the recall in the confirmation — "Saved as **<name>** (v<N>). Next time say _make another <name>_, or just _like last time_." — the name is something the system reminds the user of, never something they must remember. In autonomous mode don't ask — name the freeze command in the delivery note instead.


<!-- ===== FILE: hyperframes/hyperframes/references/route-briefs.md ===== -->

# Route briefs (moved)

Each route's interview entry — must-haves, conditional questions, deferred asks,
pitch-eligible fields, and whether the run-shape questions apply — now lives in that
route's own file, together with its input/output/trigger contract:

`references/routes/<workflow>.md` — e.g. `routes/faceless-explainer.md`,
`routes/pr-to-video.md` (including the PR-size → length table).

The interview procedure itself (the eight steps) is `references/intent-interview.md`.
Field semantics and question rules: `hyperframes/references/brief-contract.md` § 2–3.


<!-- ===== FILE: hyperframes/hyperframes/references/routes/embedded-captions.md ===== -->

# Route: embedded-captions

- **Input:** Existing talking-head footage to caption. It is an actual media file, not a URL or creative brief.
- **Output:** The same footage, untouched, with a caption layer and selected caption identity. The subject may occlude embedded captions. Any length.
- **Triggers:** "add captions", "add subtitles", "captions behind the subject", "cinematic captions for my clip".

## Interview

- **Must-haves:** which clip (the input file).
- **Deferred (announce):** the caption **identity** pick — its Step 0 probes the clip first, then shortlists 2–3 identities from the catalog and recommends one. Say that's coming.
- **Run-shape:** neither — the footage is untouched; there is no storyboard to review.


<!-- ===== FILE: hyperframes/hyperframes/references/routes/faceless-explainer.md ===== -->

# Route: faceless-explainer

- **Input:** A topic, article, notes, or arbitrary text being explained, with no product being marketed and no website to capture.
- **Output:** A faceless explainer MP4 with invented typography, abstract graphics, diagrams, or data visualization. Sweet spot 30–90s; hard cap about 3 minutes.
- **Triggers:** "faceless explainer about X", "explain how DNS works as a video", "turn this article into an explainer".

## Interview

- **Must-haves:** **angle** — concept / how-to / listicle / narrative, recommend the one the text's own shape suggests · **length** — inside the 30–90s sweet spot, scaled to how much the text actually teaches · **destination** — YouTube / embed → 16:9 · X / LinkedIn / Instagram feed → 1:1 · Shorts / TikTok → 9:16.
- **Conditional:** a pasted script adds **`VO_MODE`** — use it verbatim, or restructure per scene?
- **Pitch round:** `message` + `angle` — five tellings of the same topic are five different videos.
- **Run-shape:** both.


<!-- ===== FILE: hyperframes/hyperframes/references/routes/general-video.md ===== -->

# Route: general-video

- **Input:** Any custom creation or edit not covered by a specialized route: a static title card, longer brand or sizzle reel, multi-scene montage, static loop/poster, NLE-like footage remix, or freeform composition. It also executes every `flow: companion` brief.
- **Output:** A HyperFrames composition of any length or format through design → plan → static layout → animation → check → approval → render.
- **Triggers:** "make a static title card", "longer brand reel", "multi-scene composition", "static loop", "custom video", or any unmatched video request.

## Interview

- **Open-ended requests only:** first derive a one-sentence `message`. Ask `audience` only when it is unclear and would change the story or terminology. Ask `destination` only when it would change aspect or composition. Ask for a priority only when the brief contains a real trade-off. Default to one best version; ask about variations only when the user requests options or comparison.
- **Specific requests:** a complete ask such as "a static title card with our logo for a website hero" needs no discovery questions.
- **Pitch round:** `message` — the unformed open-ended request is this round's home case.
- **Run-shape:** both questions apply. `/general-video` is also the companion host, so `flow: companion` stays on this route with the full toolbox.


<!-- ===== FILE: hyperframes/hyperframes/references/routes/motion-graphics.md ===== -->

# Route: motion-graphics

- **Input:** A short design-led unit, typically under 10s, with no narration, where motion is the message: kinetic type, stat/count-up, chart hit, logo sting, animated title, lower-third, map, tweet/headline/page highlight, or asset-fusion shot.
- **Output:** A short MP4 or transparent alpha WebM/MOV overlay.
- **Triggers:** "an 8s logo sting", "animate this stat", "kinetic-type intro", "animate this title", "transparent lower-third overlay".

## Interview

- Autonomous by design: at most **one** clarifying question, owned by its director step, in the flow. No must-haves here beyond confirming the input; route directly.
- **Run-shape:** neither — the piece is seconds long; a storyboard and a companion session have nothing to add.
- **Front-door capability offer:** skip it. The director's one-question limit is authoritative.


<!-- ===== FILE: hyperframes/hyperframes/references/routes/music-to-video.md ===== -->

# Route: music-to-video

- **Input:** A music track, a video whose audio becomes the track, or a track generated from a mood brief — with no narration or website capture. User images or videos are optional, so a complete video needs zero supplied assets.
- **Output:** A beat-synced MP4 driven by a deterministic beat/energy map (`audiomap.json`). It may become a lyric video, slideshow, visualizer, or kinetic promo without changing pipelines.
- **Triggers:** "make a video for this song", "beat-synced video", "lyric video", "music visualizer", "kinetic promo to this beat".

## Interview

- **Must-haves:** the **music source** — a track file, a video to pull audio from, or generate one from a mood description · **destination → aspect**.
- **Deferred (announce):** brand (font + palette) and the genre feel are chosen at its Step 3 by design — they emerge from the track's analysis, not from a question up front.
- **Pitch round:** `message` — the visual concept riding the beat grid (lyric treatment, montage story, kinetic type); brand and genre feel still land at Step 3.
- **Run-shape:** both.


<!-- ===== FILE: hyperframes/hyperframes/references/routes/pr-to-video.md ===== -->

# Route: pr-to-video

- **Input:** A GitHub PR URL, `owner/repo#N`, or "this PR", read through `gh`; it is not a website capture request.
- **Output:** A changelog, feature reveal, fix explainer, or refactor walkthrough with diff, before/after, file-tree, and impact scenes. Hard cap about 3 minutes; duration follows change size.
- **Triggers:** "make a video about this PR", "turn PR #1187 into a changelog video", "release-notes video from this pull request".

## Interview

- **Must-haves:** the **PR reference** (URL, `owner/repo#N`, or "this PR") · **angle** — changelog / feature-reveal / fix-explainer / refactor-walkthrough, recommend the one the PR itself suggests · **audience** — developers (default) · mixed technical · non-technical stakeholders · **length** — from the size table below · **destination** — 16:9 is the default for a code explainer.
- **Length comes from the PR's change size**, not a fixed guess — peek once, read-only (the workflow's Step 1 still does the full deterministic fetch):

  ```bash
  gh pr view <PR_REF> --json title,additions,deletions,changedFiles
  ```

  Pick the tier from `additions + deletions` (nudged up by `changedFiles`) and lead with it (hard cap ~3 min):

  | PR change size                    | Recommended length |
  | --------------------------------- | ------------------ |
  | trivial (≲ 50 lines changed)      | ~20–40s            |
  | focused (~50–200 lines)           | ~40–70s            |
  | substantial (~200–600 lines)      | ~70–110s           |
  | large (≳ 600 lines, or 25+ files) | ~110–180s          |

  State the basis in one phrase ("~40s — small change, +44/−13 across 12 files"). The tier is a **ceiling** on how much story the diff can support, never a floor to fill: a one-headline story recommends inside 30–90s regardless of tier (the tier's range may still appear as a non-recommended fuller-walkthrough option).

- **Pitch round:** `angle` and the opening hook — the diff fixes the facts, not the telling.
- **Run-shape:** both.


<!-- ===== FILE: hyperframes/hyperframes/references/routes/product-launch-video.md ===== -->

# Route: product-launch-video

- **Input:** A website URL; a script or brief that names a site; or a product-launch script with no derivable site or an explicit "do not scrape" instruction. Capture website assets and brand tokens unless the brief selects no-capture mode. Ask whether supplied script copy is verbatim voice-over or may be restructured.
- **Output:** A product promo, launch video, site tour, or showcase MP4. Sweet spot 30–90s; hard cap about 3 minutes. A show-it-as-is brief features captured screens rather than inventing a separate route.
- **Triggers:** "launch video for X", "promo for our site", "turn this script into a 60s promo", "text-only launch video", "turn this website into a video", "site tour from this URL".

## Interview

- **First, sell or show?** One question when the request doesn't say: market the product (a promo), or show the site as-is (a tour / showcase)? A show-it answer is **intent, not a different pipeline**: write it into `BRIEF.md` (`## Intent` / `## Customizations` — "feature the site's own captured screens as the video's assets") and the workflow's normal steps carry it — the captured screens become the featured `asset_candidates`.
- **Must-haves:** **angle** — story shapes from the site's / brief's own positioning, recommend one with its basis · **length** — 30–90s sweet spot, scaled to the material · **destination** — YouTube / embed → 16:9 · X / LinkedIn / Instagram feed → 1:1 · Shorts / TikTok → 9:16.
- **Conditional:** a show-it-as-is ask adds **what to show** — the whole site, or specific pages/sections (into `BRIEF.md`'s body); a pasted script/brief adds **`VO_MODE`** (verbatim or restructured?); a script that only names a site adds **capture?** — crawl it for brand + assets (default), or text-only / "don't scrape" (no-capture mode, a preset supplies the design system).
- **Pitch round:** `message` + `angle`, after sell-or-show is settled — the pitches inherit that intent.
- **Run-shape:** both.


<!-- ===== FILE: hyperframes/hyperframes/references/routes/remotion-to-hyperframes.md ===== -->

# Route: remotion-to-hyperframes

- **Input:** Existing Remotion React source, only when the user explicitly asks to port, convert, or migrate it. A passing Remotion mention is not a trigger.
- **Output:** A HyperFrames HTML composition translated from the source and compared with the Remotion render through the migration evaluation harness.
- **Triggers:** "port my Remotion project", "convert this Remotion composition", "migrate from Remotion".

## Interview

- Not served by the intent layer — a migration with no brief. Route directly.


<!-- ===== FILE: hyperframes/hyperframes/references/routes/slideshow.md ===== -->

# Route: slideshow

- **Input:** A brief, outline, or existing page to author as a presentation, pitch deck, or interactive deck. If "slides", "deck", or "convert this page" is ambiguous, confirm that the user wants a HyperFrames slideshow before authoring.
- **Output:** A runnable HyperFrames composition plus the JSON island used by `SlideshowController`: discrete slides, fragment reveals, branching, hotspots, presenter mode, and speaker notes. The deliverable is a navigable deck, not an MP4.
- **Triggers:** "make a pitch deck", "interactive presentation", "convert this page into slides", "slideshow with presenter mode".

## Interview

- The one question is the routing confirmation itself — "do you want this as a HyperFrames slideshow?" — asked during triage (it survives every mode: wrong routing is a quality problem). The deck contract owns everything after.
- **Run-shape:** neither — the deliverable is a navigable deck, not a rendered video.
- **Front-door capability offer:** skip it. After route confirmation, the deck workflow owns all remaining choices.


<!-- ===== FILE: hyperframes/hyperframes/references/routes/talking-head-recut.md ===== -->

# Route: talking-head-recut

- **Input:** Existing talking-head, interview, or podcast footage to package. The underlying clip plays unchanged.
- **Output:** The same footage with transcript-synced graphic-overlay cards: kinetic titles, lower-thirds, data callouts, pull-quotes, side panels, or picture-in-picture. Any length.
- **Triggers:** "package this video", "add graphic overlays to my talk", "add lower-thirds or data callouts to this interview".

## Interview

- **Must-haves:** which clip (the input file).
- **Deferred (announce):** its render-strategy questions — aspect ratio, layout, style group, card count — stay at its Step 7, where the recommendations come from the probed footage and transcript. Say they're coming.
- **Run-shape:** neither.


<!-- ===== FILE: hyperframes/hyperframes/references/script-format.md ===== -->

# `SCRIPT.md` — locked narration (optional)

The **locked narration** for a project: the final spoken lines + voice + delivery. It is an _optional_ plan-layer file — a video with no narration (bgm-only, silent overlay) has none. The storyboard's per-frame `voiceover` is the lighter, editable _guide_; `SCRIPT.md` is the _commit_. (Storyboard format → `references/storyboard-format.md`.)

This file defines the SCRIPT.md **shape** only. Synthesizing the spoken lines into audio is a capability owned by `media-use` → `../../media-use/audio/references/tts.md`.

Free-form markdown — there is no strict parser; the TTS step extracts the indented spoken lines.

## Shape

A header block, then one section per spoken line.

| Part                            | Holds                                                                                                                                   |
| ------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------- |
| Header                          | `**Voice:**` (provider + voice), `**Voice settings:**` (e.g. stability / similarity / style), `**Voice direction:**` (overall delivery) |
| `## Line N — <label> (Frame N)` | one spoken line, tied to its storyboard frame                                                                                           |
| `**Time:**`                     | the frame's rough window — a _guide_, not authoritative (real timing comes from TTS word timestamps)                                    |
| `**Delivery:**`                 | per-line delivery note                                                                                                                  |
| indented block                  | the **spoken text** — the only part fed to TTS                                                                                          |

## Example

```markdown
# SCRIPT — acme-launch

**Voice:** Rachel (ElevenLabs)
**Voice settings:** stability 0.35 · similarity 0.75 · style 0.20
**Voice direction:** Confident, warm, a little playful.

---

## Line 1 — Hook (Frame 1)

**Time:** 0.0 – 3.0s
**Delivery:** Land the promise on the beat.

    Ship a launch video in an afternoon.

## Line 2 — The problem (Frame 2)

**Time:** 3.0 – 7.0s
**Delivery:** Wry, a touch tired.

    The old way? Prompt, wait twenty minutes, get something that misses.
```

## To TTS

Feed each line's spoken text to the provider documented in
`media-use/audio/references/tts.md`. The `hyperframes tts` command is
Kokoro-only; use its `--voice` flag, or use the bundled HeyGen helper when word
timestamps are required. Real per-word timing replaces the `**Time:**` guides.


<!-- ===== FILE: hyperframes/hyperframes/references/skill-lifecycle.md ===== -->

# Skill installation and freshness

Read this reference when installing or updating skills, diagnosing unexpected workflow behavior, or running HyperFrames setup in CI.

For a plugin installation, follow [plugin execution rules](plugin-installation.md); the plugin manager owns updates and all workflows are bundled. The commands below apply only to standalone skills.

HyperFrames installs the core set eagerly and workflow skills lazily.

- **Core set:** `/hyperframes`, the `hyperframes-*` domain skills, and `/media-use`.
- **Workflow skills:** installed when routing selects them through `npx hyperframes skills update <workflow-name>`.

## What `init` does

`npx hyperframes init` checks GitHub and refreshes the core set plus other skills already installed. It does not install workflows that have never been used. A current install is a no-op. Offline or rate-limited checks degrade gracefully and do not fail project scaffolding.

The `--skip-skills` CLI flag is temporarily ignored. CI and tests may opt out with `HYPERFRAMES_SKIP_SKILLS=1`.

`HYPERFRAMES_SKIP_SKILLS=1` also makes `skills update` (bare or named) and bare `skills` exit 0 without installing or pruning, so an install pinned to one commit stays pinned.

## Diagnose and update

```bash
npx hyperframes skills check
npx hyperframes skills check --json
npx hyperframes skills update
npx hyperframes skills update <workflow-name>
npx hyperframes skills
```

- `skills check` exits non-zero when an installed skill is stale or the core set is incomplete. Workflows available on demand but not installed are not failures.
- Bare `skills update` refreshes the core set and everything already installed, prunes unpublished skills, and does not expand the workflow set.
- Named `skills update <name...>` also installs those named workflows or domain skills.
- Bare `skills` installs the full published set explicitly.

If the HyperFrames CLI is unavailable, use `npx skills add heygen-com/hyperframes --skill <workflow-name>` for one workflow or `npx skills add heygen-com/hyperframes --all` for the full published set.

The CLI may print a one-line stale-skill reminder during `render`, `lint`, or `check`. Treat a failed update as a visible tool failure; do not continue from a remembered workflow contract.


<!-- ===== FILE: hyperframes/hyperframes/references/storyboard-format.md ===== -->

# Storyboard format — `STORYBOARD.md` + parsed manifest

Defines the storyboard's **base data format** only: the `STORYBOARD.md` file shape and the `StoryboardManifest` it parses into. How a workflow _generates_ a storyboard lives in that workflow; the optional narration/TTS file (`SCRIPT.md`) is a separate concern owned by the TTS step, not here.

A storyboard is the **plan layer** for a video — an ordered set of **frames** (key moments) in one markdown file. Parser: `@hyperframes/core/storyboard` → `StoryboardManifest`.

## Frontmatter (global direction)

YAML block at the top. Unknown keys are kept under `globals.extra`.

| Key        | Meaning                                                           | Example                                   |
| ---------- | ----------------------------------------------------------------- | ----------------------------------------- |
| `format`   | Canvas size                                                       | `1920x1080`                               |
| `duration` | The brief's rough length expectation (advisory, not a hard limit) | `22s`                                     |
| `message`  | One-line thesis                                                   | `Ship a launch video in an afternoon`     |
| `arc`      | Narrative arc                                                     | `Hook → Problem → Solution → Proof → CTA` |
| `audience` | Who it's for                                                      | `indie devs on X`                         |
| `mode`     | Interaction mode (see `brief-contract.md`; default collaborative) | `autonomous`                              |

Set `duration` from the brief's `length` when the storyboard is first written. It is an expectation, not a gate: assembly reports where the cut actually lands against it and flags a large gap — judge whether the drift serves the piece, and update the value when the intended length genuinely changes.

## Per-frame sections

One `## Frame N — Title` heading per frame (`Frame` / `Beat` / `Scene` accepted at H2/H3). Metadata as `- key: value` bullets; everything below them until the next heading is the free-form **narrative**.

| Key             | Meaning                                                                                                       |
| --------------- | ------------------------------------------------------------------------------------------------------------- |
| `status`        | `outline` → `built` → `animated` (defaults `outline`)                                                         |
| `src`           | project-relative path to the frame's HTML sub-composition (the tile poster renders from it)                   |
| `duration`      | e.g. `4s`                                                                                                     |
| `transition_in` | `crossfade` / `cut` / `wipe` … (alias `transition`)                                                           |
| `scene`         | one-line contact-sheet caption (aliases `description` / `summary` / `caption`)                                |
| `voiceover`     | the frame's narration _guide_ (aliases `vo` / `voice_over` / `narration`)                                     |
| `poster`        | seconds to seek for the tile poster (past the intro animation)                                                |
| _any other key_ | kept verbatim under the frame's `extra` — a workflow carries its own per-frame data (effects, assets, …) here |

## Parsed manifest

The parser is **lenient**: it never throws and records anything surprising as a `warning`.

```
StoryboardManifest {
  globals: { format?, message?, arc?, audience?, extra: {…} }
  frames: Array<{
    index, number?, title?,
    status,                       // "outline" | "built" | "animated"
    src?, duration? / durationSeconds?, transitionIn?,
    scene?, voiceover?, poster?,
    narrative,                    // markdown below the metadata
    extra: {…}                    // unknown keys, preserved
  }>
  warnings: Array<{ message, line?, frameIndex? }>
}
```

## `SCRIPT.md` (out of scope here)

Optional, free-form, **not parsed into the manifest** — the locked-narration file that drives TTS. Its format is defined in `references/script-format.md`, and it is absent for videos with no narration/TTS. The per-frame `voiceover` above is the storyboard's own narration guide.

## Example

```markdown
---
format: 1920x1080
message: "Ship a launch video in an afternoon"
arc: Hook → Problem → Solution → Proof → CTA
audience: indie devs on X
---

## Frame 1 — Hook

- scene: Big type punches in on the beat
- duration: 3s
- poster: 2s
- transition_in: cut
- status: animated
- voiceover: "Ship a launch video in an afternoon."
- src: compositions/frames/01-hook.html

Open cold on the promise. This is the thesis — everything after pays it off.

## Frame 2 — The problem

- scene: A 20-minute timer spins on a stack of rejected takes
- duration: 4s
- transition_in: crossfade
- status: built
- voiceover: "The old way? Prompt, wait twenty minutes, get something that misses."
- src: compositions/frames/02-problem.html

The old way: prompt, wait, get something that misses. Establish the pain we remove.
```

## Notes

- A frame with `status: outline` and no built `src` renders as an outline placeholder.
- `built` is the middle rung: the frame's HTML exists and its **layout is confirmed** (a wireframe sketch or better) — motion not yet added. Nothing is drawn yet beyond the approved layout.
- The process that walks these statuses — plan, sketch, build, each pass reviewed in chat and on the board (`boards/storyboard.html`, format in `hyperframes-creative/references/storyboard-recipe.md`) — is `review-loop.md`.
- Multi-line `voiceover` values collapse to one line on save.


<!-- ===== FILE: hyperframes/hyperframes/references/subagent-dispatch.md ===== -->

# Subagent dispatch — harness adapter

The video workflows (`product-launch-video` / `faceless-explainer` / `pr-to-video` / `motion-graphics` / `general-video`) describe subagent dispatch in harness-neutral verbs. This file maps those verbs to the primitives of whatever agent harness you are running on. Read it once per run, before the first dispatch; everything else in the workflows (dispatch packets, file artifacts, exit-code gates, Resume tables) is harness-independent and needs no translation.

## The contract (identical on every harness)

- **DISPATCH(role_file, dispatch_context)** — start one child agent whose prompt is the **full contents of the named role file** (a builder-assembled payload like `.hyperframes/frame-packets/_role.md`, or a workflow's `sub-agents/<role>.md`) followed by the `## Dispatch context` block from the workflow, copied **verbatim** (never digested or paraphrased). Every harness below accepts arbitrary task text, so this works everywhere; never rely on the child seeing your conversation, memory, or skills — the prompt and the files on disk are its entire world.
- **Parallel fan-out** — when a step says "start N workers in parallel", the workers are mutually independent (no ordering, no shared state beyond the filesystem). Run as many concurrently as your harness allows.
- **WAIT** — a step's completion criterion is always **the expected artifact existing on disk** (e.g. `compositions/<scene-id>.html`), never the harness's completion notification (some harnesses deliver results best-effort). After waiting, verify the artifacts; a missing artifact means that child failed — re-dispatch it once with the same prompt before surfacing an error.

## Concurrency cap → batching rule (cap never changes scope)

A harness concurrency limit **reduces parallelism, not work**: every scene still gets built, with the available slots chewing through the full list. The workflow sets how many scenes each worker gets (`general-video` assigns 2–3).

- When the harness queues excess children internally, submit **all N at once** and let the queue drain.
- Harness hard-caps active children (e.g. OpenClaw `maxChildrenPerAgent`) → dispatch in **waves of the cap size**: start `cap` workers, wait for their artifacts, start the next wave, until all N scenes exist. Example: 9 scenes on a cap-3 harness = 3 waves of 3 — never drop scenes, never merge scenes into one worker to fit the cap.

## Harness mapping

Use the current harness's native delegation and waiting tools when they are available. The workflow contract stays the same:

- **DISPATCH** sends the complete role file and dispatch context to one worker.
- **Parallel fan-out** starts independent workers concurrently up to the harness limit.
- **WAIT** verifies the expected artifacts on disk, not only a completion notification.
- **Re-dispatch** starts a fresh worker with the same context plus the gate failure.

When native delegation is unavailable, use the existing fallback ladder: launch headless CLI workers that share the project filesystem, then fall back to inline serial execution.

On Codex, native delegation requires the user's explicit permission. Fold a one-line request into the workflow's first existing user pause before dispatch; a standing grant in `AGENTS.md` or the kickoff prompt also counts. Without it, use the fallback ladder rather than silently skipping work.

## Vocabulary mapping

- A request to work "in the background" means dispatch concurrently when the harness supports it.
- Load a named skill through the harness's skill mechanism, or read `<skills-root>/<skill>/GUIDE.md` directly.
- Map generic read, write, edit, and shell verbs to the current harness's equivalent tools.


<!-- ===== FILE: hyperframes/hyperframes/references/workflow-catalog.md ===== -->

# Workflow catalog (moved)

Each workflow's input/output/trigger contract now lives in its own route file — one
small read per candidate instead of a whole catalog:

`references/routes/<workflow>.md` — e.g. `routes/product-launch-video.md`,
`routes/general-video.md`, `routes/remotion-to-hyperframes.md`.

The same file carries that route's interview entry (must-haves, conditionals, deferred
asks, run-shape), so confirming a route is exactly one read.
