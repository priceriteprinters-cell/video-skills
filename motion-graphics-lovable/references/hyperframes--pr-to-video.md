

<!-- ===== FILE: hyperframes/pr-to-video/GUIDE.md ===== -->

---
name: pr-to-video
description: "Turn a GitHub pull request (a PR URL, owner/repo#N, or 'this PR' in a checked-out repo) into a code-change explainer video — changelog, feature reveal, fix, or refactor walkthrough built from the diff, commits, and files: the input is a code change, not a website. Not a product promo (/product-launch-video) or a no-PR topic explainer (/faceless-explainer). Unclear → /hyperframes."
---

**Plugin installs:** Before setup or freshness commands, follow [plugin execution rules](../hyperframes/references/plugin-installation.md) when this skill is inside a HyperFrames plugin. Standalone installs keep the update instructions below.

> **First, keep this skill fresh — confirm with the user before running:** `npx hyperframes skills update pr-to-video`. A fast no-op when everything is current; otherwise it refreshes this skill plus the core domain skills it depends on before you rely on them.

> **media-use**: Before sourcing audio/images/logos, call `/media-use` to resolve BGM/SFX/images from the HeyGen catalog and brand logos from their official sources. Run `--adopt` first to register existing assets. See `/media-use` skill. When the host app provides its own music or sound-effect tools, use those for music and sound effects.

# PR to HyperFrames

Use this skill to ingest a GitHub pull request, understand the change, plan a code-change explainer, and build it frame by frame in HyperFrames. The input is a **code change** (read via `gh`), not a website — there is **no capture step and no real assets** beyond the contributors' avatars.

> **The front door is `/hyperframes`.** You are the orchestrator. Run each step, verify its gate, and only then continue. This skill is for a **GitHub pull request** (a code change). Any other intent, a bare "make a video", or any uncertainty → read `/hyperframes` first — the intent layer owns every route decision, and a fresh creation arriving here without `BRIEF.md` goes through it anyway (Setup's opening rule).

You are the orchestrator. Work in the resolved external `PROJECT_DIR`, never in the caller repository by default. Run steps in order and pass each gate before continuing. User-gated steps are Step 0, Step 3, and Step 6. Read `../hyperframes/references/brief-contract.md` before Step 0 — it defines the gate types and how `BRIEF.md`'s `flow`/`storyboard` derive the mode that governs the Step 3/4/6 gates. Do every step yourself except Step 5, where you dispatch a bounded pool of frame workers. Do not put design or motion rules here; those live in the frame-worker sub-agent, this skill's local `../hyperframes-animation/rules/` + `../hyperframes-animation/blueprints/`, and `hyperframes-creative`.

Workflow: Step 0 setup → `hyperframes.json`; Step 1 ingest → `capture/extracted/` + `assets/<login>.png`; Step 2 design system → `frame.md`; Step 3 storyboard/script → `STORYBOARD.md` and `SCRIPT.md`; Step 3.1 audio → `audio_meta.json`; Step 4 visual design → enriched `STORYBOARD.md`; Step 5 frames → `compositions/frames/NN-*.html` and `index.html`; Step 6 final render → `renders/video.mp4`.

---

## Step 0: Setup

Goal: Enter with a confirmed brief — including the **PR reference** (a full URL, an `<owner>/<repo>#<N>` ref, or "this PR" in a checked-out repo) — create the HyperFrames project, and make the brief durable. The style is always **code-editorial** (fixed at Step 2, never asked).

**The brief is confirmed by the intent layer, not by questions asked here.** Opening rule, in order: **(1)** `BRIEF.md` exists → read it and ask nothing — the brief is settled, and its `flow`/`storyboard` derive the mode (brief contract § 1). **(2)** No `BRIEF.md` but the project exists (`hyperframes.json` / `STORYBOARD.md` on disk) → resume from the storyboard's frontmatter and the recorded preferences; never re-interrogate a half-built project. **(3)** Neither — a fresh creation request that arrived here directly → read `/hyperframes` and run its intent layer (`references/intent-interview.md`): it checks recipes and remembered defaults, and conducts this route's questions — including the PR-size → length doctrine, which lives whole in `../hyperframes/references/routes/pr-to-video.md` — then hands back the locked brief. Edit requests skip all of this — go do the edit.

Resolve the project directory before doing any other work. Preserve a user-supplied project directory; otherwise use the durable external cache location printed by the resolver. Never create `videos/` in the caller repository:

```bash
PR="<url | owner/repo#N>"
if [ -n "${EXPLICIT_PROJECT_DIR:-}" ]; then
  PROJECT_DIR="$(node <SKILL_DIR>/scripts/project-dir.mjs --pr "$PR" --project-dir "$EXPLICIT_PROJECT_DIR")"
else
  PROJECT_DIR="$(node <SKILL_DIR>/scripts/project-dir.mjs --pr "$PR")"
fi
echo "PR-to-video project: $PROJECT_DIR"
node <SKILL_DIR>/scripts/preflight.mjs
```

The capability preflight runs before fetch, story work, audio, or frame dispatch. If the installed CLI cannot run the validation command required by this skill, stop with its upgrade instruction rather than spending the run's context first.

Initialize only if `$PROJECT_DIR/hyperframes.json` is missing. Its basename comes from the PR, such as `acme-sdk-pr-1842`; never use the workspace name or a timestamp.

`npx hyperframes init "$PROJECT_DIR" --non-interactive --example=blank --skill=pr-to-video` — `init` checks the installed skills against the latest on GitHub and updates the global set if any are out of date.

Every relative-path command below runs with `$PROJECT_DIR` as its working directory. Examples without an explicit subshell mean `(cd "$PROJECT_DIR" && …)`; never change the caller repository's working tree.

**Write `BRIEF.md` immediately after init** (never before — `init` refuses a non-empty directory): the intent layer's locked brief, shape per `../hyperframes/references/brief-format.md`. Resolve `<MEDIA_DIR>` as the installed `/media-use` skill directory. Then record each preference-backed answer with `node <MEDIA_DIR>/scripts/prefs.mjs record --hyperframes .` (`brief-format.md` names the subset). If the intent layer adopted a recipe, run `node <MEDIA_DIR>/scripts/recipe.mjs use --hyperframes . --name <name>`; it copies its `frame.md` into the project (Step 2 is then skipped) and returns the skeletons Step 3 drafts from. A recipe fills answers, not approvals; the review gates still run.

**Show sign-in status before proceeding past Setup** — run `npx hyperframes auth status` and relay its output verbatim. It reports whether voice/BGM will use HeyGen or local engines and, when signed out, how to sign in. Apply one branch:

- **Collaborative:** wait for the user to sign in or explicitly choose `offline` / `go`.
- **Autonomous:** state the status and continue through the available local engines.

Do not silently omit a required capability when no offline provider exists; surface the blocker. Do not fold this decision into another question or write keys into a per-repo `.env`. Auth ownership and offline fallbacks: `/media-use` `references/setup-providers.md` § Providers.

**Gate:** `hyperframes.json` and `BRIEF.md` exist; the PR ref is captured in the brief; the preference-backed answers were recorded (brief contract § 2); sign-in status was shown (signed in, or continuing offline).

---

## Step 1: Ingest the PR (no capture)

Goal: Fetch the PR's facts and fold them into the project as the source of information. There is **no website capture**. `fetch-pr.mjs` runs `gh` deterministically — completing the files list via paginated `gh api` so a large PR doesn't truncate at ~100 files, and writing only `capture/pr.json` + `capture/diff.patch` (no scratch dir). For MERGED PRs it also resolves a best-effort `shipped_version` (+ `version_source`) into `pr.json`, so the end card can cite a real version instead of inventing one. Then `ingest.mjs` folds that into the synthetic capture package offline.

```bash
PR="<url | owner/repo#N | N>"

# Fetch the PR deterministically: runs gh, completes the files list via paginated
# gh api (so a big PR doesn't truncate at ~100 files), writes only capture/pr.json +
# capture/diff.patch — no scratch dir. gh auth / not-found / private errors exit 1 here.
(cd "$PROJECT_DIR" && node <SKILL_DIR>/scripts/fetch-pr.mjs --pr "$PR" --out-dir ./capture)

# Offline transform → capture/extracted/{tokens.json (colors:[] → code-editorial palette),
# visible-text.txt (the brief), people.json (contributors, bot-filtered, name+login,
# avatarFile=assets/<login>.png)}.
(cd "$PROJECT_DIR" && node <SKILL_DIR>/scripts/ingest.mjs \
  --pr-json ./capture/pr.json --diff ./capture/diff.patch --out-dir ./capture/extracted)

# The people front's one network step — download each contributor's GitHub avatar to
# assets/<login>.png for the credits close. Best-effort; always exits 0.
(cd "$PROJECT_DIR" && node <SKILL_DIR>/scripts/fetch-people-avatars.mjs \
  --people ./capture/extracted/people.json)
```

If `fetch-pr.mjs` exits 1 (gh auth / not found / private), report its stderr and stop — **do not fabricate PR contents**. If `ingest.mjs` exits 1, read its stderr (usually a malformed `pr.json`), fix, and rerun (deterministic). `fetch-people-avatars.mjs` always exits 0; missing avatars just mean no credits close to author.

`people.json` carries a `name` for whichever contributors `gh` already named (the PR author, commit authors, `mergedBy`) — `null` for the rest (reviewers/commenters/assignees, which `gh pr view` only ever gives a bare `login`). Before writing the credits close in Step 3, resolve any `null` name yourself for the 1-6 people who'll actually appear on that frame: `gh api users/<login> --jq .name` (you already have `gh` — no need to script this). If GitHub has no public name for that user either, fall back to the login on-screen and drop that person from the spoken line (see story-design.md's credits section — the voiceover must still say names, never raw handles).

**Gate:** `capture/pr.json`, `capture/diff.patch`, `capture/extracted/tokens.json`, `capture/extracted/visible-text.txt`, and `capture/extracted/people.json` exist; you can state the PR's change in one clear sentence. `assets/<login>.png` is best-effort — its absence is not a failure.

---

## Step 2: Design System

Goal: Adopt the code-editorial frame preset; a script turns it into this video's `frame.md` + caption skin.

The style is fixed — **code-editorial** (warm editorial; a navy code surface built for diffs). Run:

```bash
node <SKILL_DIR>/scripts/build-frame.mjs --preset code-editorial --hyperframes .
```

The script copies the code-editorial preset's `FRAME.md` → `frame.md`, remixes it onto any brand tokens in `capture/extracted/tokens.json` (a PR has none → `colors:[]`/`fonts:[]` keeps code-editorial's own palette, a complete design), copies the preset's caption skin to `.hyperframes/caption-skin.html`, and self-validates (exits 1 on a broken mapping). Proceed as soon as it exits 0 — no hand-editing.

**Gate:** `build-frame.mjs` exited 0 — `frame.md` exists from the code-editorial preset, and `.hyperframes/caption-skin.html` exists as the caption skin source.

---

## Step 3: Storyboard and Script

Goal: Turn the PR into an approved frame-by-frame explanation plan.

Read `../hyperframes-creative/references/story-spine.md` (hook language, value-before-evidence, storyboard-as-proposal, source-traceable visuals), `references/story-design.md`, `../hyperframes-animation/blueprints-index.md`, `../hyperframes/references/storyboard-format.md`, and `../hyperframes/references/script-format.md`. Use them to write `STORYBOARD.md` and, when narration is needed, `SCRIPT.md`. Set the frontmatter `duration:` from the brief's `length` — a rough expectation; assembly reports where the cut lands against it.

Use `story-design.md` for the PR archetype (changelog / feature-reveal / fix-explainer / refactor-walkthrough), the PR-native frame types, hook, persuasion, beats, the per-frame word budget, and the credits close. The sequence comes from **narrative design, not the diff's file order** — explain the change, don't read the diff aloud. As a **soft guide**, consult the role→blueprint menu in `../hyperframes-animation/blueprints-index.md`: for each beat, write the voiceover in the shape its candidate blueprint implies and tag that candidate `blueprint:` id when one fits (story truth still decides which beats exist — never force a beat to fit a shape). Feature 2–4 real diff hunks (from `capture/diff.patch`), each a small legible snippet; name the `code-*` block each wants in the frame's `scene`. Frames carry no `asset_candidates` except the `credits` close (1–6 `assets/<login>.png` avatars). Use the exact required fields from the storyboard and script references.

After drafting, run the review loop's plan pass — `../hyperframes/references/review-loop.md` § 1: present the plan as a proposal, and ask the two questions — approve or change, and **sketches first** (recommended) or skip. Feedback arrives as a chat reply; loop until approved. This is a **checkpoint gate** (brief contract § 1): in autonomous mode there is nothing to ask — post the same summary as a heads-up and proceed; sketches collapse into the build, and the final preview with its one question comes at Step 6.

**Gate:** `STORYBOARD.md` exists, every frame has the required narrative fields, `SCRIPT.md` exists when narration is needed, and the user approved the plan (autonomous: the summary was posted as a heads-up).

---

## Step 3.1: Audio

Goal: Generate narration, word timings, music, and audio metadata from the approved script.

Start audio after Step 3 approval. Run it in the background, then continue to Step 4.

**Choose the narration voice from the user's ask before invoking.** If the request named a voice, gender, or tone, pick a matching voice id and pass it with `--voice <id>`. The pipeline default is otherwise **Marcia (female)** on HeyGen / `am_michael` on Kokoro — so a request like "a male voice" is silently ignored unless you pass the flag. Voice ids are provider-specific; resolve against whichever provider Step 0's sign-in status selected: **HeyGen** (signed in) via `node <MEDIA_DIR>/audio/scripts/heygen-tts.mjs --list` (or `GET /v3/voices?engine=starfish`); **Kokoro** (offline) via the voice table in `<MEDIA_DIR>/audio/references/tts.md` (prefixes `am_`/`bm_` male, `af_`/`bf_` female). When the user expressed no preference, fall back to the remembered voice (brief contract § 2) before the pipeline default, and say which one you used; omit `--voice` only when neither names one. When the user explicitly picked a voice this run, record it (`prefs.mjs record --key voice`).

`node <SKILL_DIR>/scripts/audio.mjs --script ./SCRIPT.md --storyboard ./STORYBOARD.md --hyperframes . --out ./audio_meta.json --voice <voice-id> &`

The audio script handles narration, word timings, BGM lookup from HeyGen's music library, and timing metadata. BGM mood comes from the storyboard's `music:` field. This uses the HeyGen Audio API for retrieval, not generation, and the same `~/.heygen` credential as TTS. For provider details, read `../media-use/audio/references/tts.md`. When the host app's own tools make the music or a sound effect, put the file under assets/ and list it in the audio_meta.json file marked `"source": "host"`: music as `bgm` `{ "path": "assets/…", "source": "host" }` with `music: none` in the storyboard; a sound as an `sfx` entry `{ "frame": <n>, "file": "assets/…", "offset_s": 0, "duration_s": <its length>, "source": "host" }`. Every audio pass keeps these, and a frame with a host sound gets no looked-up cue.

If there is no narration and no `SCRIPT.md`, skip voice generation. BGM may still run if the storyboard has a music mood.

**The canonical fully-silent marker** (shared across the workflows that reuse this audio model): `music: none` in the STORYBOARD.md top YAML block, no `SCRIPT.md`, **and** no `sfx:` cues or host audio. That combination marks the project silent — no narration, no BGM, no SFX. `audio.mjs` recognizes it and generates nothing (it removes any stale `audio_meta.json`; an absent `audio_meta.json` is what assemble treats as silent), so this step is a clean skip. Without narration but with `sfx:` cues or host audio the film is not silent: `audio.mjs` writes the audio_meta.json file for `fetch-sfx` to fill. `music: none` with narration keeps TTS and turns only BGM off. Use exactly this spelling — don't improvise other markers.

**Gate:** audio job has started, or the project is marked silent (`music: none`, no `SCRIPT.md`, no `sfx:` cues or host audio).

---

## Step 4: Frame Visual Design

Goal: Add the visual direction, layout intent, and motion choices to each storyboard frame.

**Sketch the storyboard sheet first (collaborative only).** The moment the plan is approved, run the sketch pass — `../hyperframes/references/review-loop.md` § 2 (don't wait on Step 3.1; the stills don't use timings): pose every frame yourself in its composition, mount each in `index.html` at its planned start, snapshot all the stills in one run and write the board, `boards/storyboard.html` (`../hyperframes-creative/references/storyboard-recipe.md`), mark each `built`, pause for the one layout question when every frame is `built`, and revise only the frames named until the board is confirmed. Stand-ins: for a **code beat**, a plain code panel with the filename and a few real diff lines as text — the `code-*` block wiring belongs to the workers. Only then write the visual design below onto the confirmed layouts. In autonomous mode, or when the user chose to skip sketches at Step 3, skip this pass — frames go straight from `outline` to `animated` at Step 5.

Edit `STORYBOARD.md` in place. Do not create another storyboard. Use `frame.md` as source of truth for color, type, layout feel, and style.

Read `references/visual-design.md`, `../hyperframes-animation/blueprints-index.md`, `references/motion-language.md`, `references/code-vocabulary.md`, and `../hyperframes-animation/rules-index.md`. Use `visual-design.md` for the method (the time-coded shot sequence, the inline Layout vocabulary, and the code-beat treatment), plus the required `## Video direction` block. Use `../hyperframes-animation/blueprints-index.md` to pick each frame's shot shape. Use `code-vocabulary.md` to pick the right `code-*` block per code beat (diff = `code-diff`, refactor = `code-morph`, new code = `code-typing`, …). Use `motion-language.md` (the motion vocabulary + the motion doctrine) and `../hyperframes-animation/rules-index.md` (valid rule names) for motion — do not invent motion or block/blueprint names.

**Search the live catalog before you design any named look.** `code-vocabulary.md` covers the code beats; it does not cover the rest. For every other look, effect, treatment or transition the brief names — "CRT scanlines", "glitch", "film grain", "shimmer sweep", "confetti burst" — run `npx hyperframes catalog --query "<the look, in plain English>" --json` and read the top results BEFORE you write that look into `STORYBOARD.md`. The search needs **nothing installed**: no project, no prior `add`, no account. It ranks the whole hosted registry (~400 blocks and components) from any directory. Name the block you found here; Step 5 pre-installs every block the storyboard names. Hand-author a look only after a search for it came back with nothing that fits.

For every frame, write a **time-coded shot sequence** into `STORYBOARD.md` per `visual-design.md`'s method: pick the frame's blueprint (or compose), instantiate it with THIS frame's content, and pace each Scene's reveal to the voiceover so the frame develops across its full duration instead of front-loading then freezing. **For a code beat, the `code-*` block is the frame's `focal`** and the Scenes choreograph the surrounding code-editorial Code Surface (the entry of the file/header, the camera onto the hunk, the landing line) — **not** the code animation itself, which the block owns. Immediately after each code frame's fields, add a `### Source excerpt` fenced `diff` block containing only the exact real hunk the worker must render (12 lines maximum). Select it here from `capture/diff.patch`; workers are forbidden from reopening that full diff. State layout and motion **inline** per Scene (vocabularies in `visual-design.md` and `motion-language.md`). Add one video-wide `## Video direction` block.

Do not change story, script, `transition_in`, `asset_candidates`, or the PR source. Do not write HTML in this step beyond the sketch pass's poses. There is **no asset-staging step** — the only real assets are the credits avatars, already in `assets/`.

**Gate:** every frame has a time-coded shot sequence whose reveals are paced to the voiceover (no front-loading); code frames name a `code-*` block as the `focal`; `## Video direction` exists. Collaborative: the sketch sheet was confirmed.

---

## Step 5: Build Frames

Goal: Build every storyboard frame as an HTML composition and assemble the playable video.

Wait for Step 3.1 audio to finish if audio was started. Then sync durations and fetch SFX; skip both if silent.

`node <SKILL_DIR>/scripts/audio.mjs sync-durations --audio-meta ./audio_meta.json --storyboard ./STORYBOARD.md`

`node <SKILL_DIR>/scripts/audio.mjs fetch-sfx --storyboard ./STORYBOARD.md --hyperframes .`

Duration sync is mechanical: real voice duration wins; silent frames keep estimates; never hand-edit synced durations.

**Pre-install the registry blocks** named across `STORYBOARD.md` once, before dispatch, so parallel workers don't race on the registry:

`for b in <each registry block named in the storyboard>; do npx hyperframes add "$b"; done`

Before dispatch, read `../hyperframes/references/subagent-dispatch.md`. Build bounded packets and the worker role payload:

```bash
node <SKILL_DIR>/scripts/frame-packets.mjs --project "$PROJECT_DIR" --storyboard "$PROJECT_DIR/STORYBOARD.md"
```

The packet builder hard-fails a code frame without the upstream-selected `### Source excerpt`, and hard-caps packet bytes. It also writes `_role.md` (`../hyperframes/references/frame-worker-core.md` + this skill's `sub-agents/frame-worker.md`, concatenated verbatim — the complete worker role). Dispatch **at most three workers total**, balanced across the packet paths; each worker's prompt carries `_role.md` and its assigned packet paths — paste the role in full or hand its path (equivalent; the worker starts from exactly those documents) — and each worker may build multiple assigned frames sequentially, reading the role once. Workers read only their packet(s) and `frame.md`. They never open the full `STORYBOARD.md`, `capture/diff.patch`, or `capture/extracted/visible-text.txt`. Each worker writes only its assigned `compositions/frames/NN-*.html`; workers never edit `STORYBOARD.md`. When a frame has a **confirmed sketch** on disk (collaborative runs — review loop § 3), say so in that worker's dispatch context: the sketch is the existing `compositions/frames/NN-*.html`, and the worker dresses that layout rather than redrawing it (frame-worker core § When a confirmed sketch exists).

On a failed frame, re-dispatch **that frame only**, with its existing packet plus the exact validator/lint finding. One retry maximum. Do not replay a whole batch and do not retry without a concrete finding.

**Full-bleed backgrounds ride on a `class="clip"` layer, never the `#root`.** A frame's ground (color field / gradient / grid) is its own full-duration background clip — a `background` set on the `#root` / `data-composition-id` element is clip-gated to the frame's window and is not a dependable ground, so dark content can land on the black host `body` and render invisible. The video's base ground is painted by the assembler from `frame.md`'s `canvas` color onto the index `#root`. (Full rule + self-check: `../hyperframes/references/frame-worker-core.md`.)

As each worker returns, mark that frame `animated` in `STORYBOARD.md`.

After audio timings exist, build captions in the background and assemble the index:

`node <SKILL_DIR>/scripts/captions.mjs build --storyboard ./STORYBOARD.md --audio-meta ./audio_meta.json --hyperframes . --out ./caption_groups.json &`

`node <SKILL_DIR>/scripts/assemble-index.mjs --storyboard ./STORYBOARD.md --hyperframes .`

`captions.mjs` uses the project's `.hyperframes/caption-skin.html` (code-editorial's, copied in Step 2), injecting brand tokens from `frame.md`; `captions: skipped (<reason>)` is valid. `assemble-index.mjs` stages the credits avatars from `assets/` as an idempotent backstop.

**Gate:** every frame is marked `animated` (collaborative: the sketch sheet was confirmed at Step 4), `index.html` exists, and captions are built or explicitly skipped.

---

## Step 6: Finalize

Goal: Verify the assembled video, get user approval, and render the final MP4.

Inject transitions, run checks, pause for review, then render.

`node <SKILL_DIR>/scripts/transitions.mjs inject --storyboard ./STORYBOARD.md --hyperframes .`

`node <SKILL_DIR>/scripts/transitions.mjs verify --storyboard ./STORYBOARD.md --index ./index.html`

`npx hyperframes lint`

`npx hyperframes check`

`npx hyperframes snapshot --at <frame-midpoints>`

`snapshot` stitches the captured frames into one contact sheet (`.hyperframes/artifacts/snapshots/<id>/contact-sheet.jpg`; the command prints the path). Glance at it; if nothing is obviously broken, move on — don't linger here.

If a command fails, surface stderr and stop — don't pile on recovery commands. Fix it yourself: the cheapest safe edit to `compositions/frames/NN-*.html`, then rerun the failed check.

**Known false-positive — do not chase it.** `check` may report a handful of `text_box_overflow` errors of ~1–4px on the **caption** highlight words (selector `#caption-word-*` / `.caption-line`). The caption pill uses a deliberately snug `line-height` (set once in `scripts/captions.mjs`) and has **no `overflow:hidden`**, so a heavy display glyph's ink spills a few px into the pill's own padding — nothing is actually clipped. Treat these as expected and proceed. Do **not** inflate the caption `line-height` (it balloons the pill, which is worse). Only act on a `text_box_overflow` when it names a **frame** element (`#el-NN-*`), not a caption word.

After checks pass, pause for user review — the review loop's final look (`../hyperframes/references/review-loop.md` § 4): one question, on the final Studio preview — render now, or what changes? (Autonomous: the same, as the one kept question — open the preview with the command below even though the user didn't ask for one.) Then deliver the MP4 with the contact sheet and the frame ids so revisions can target a single frame.

Preview: `npx hyperframes preview "$PROJECT_DIR" --background`

Render only after user approval (autonomous mode: after the render-or-changes question):

`npx hyperframes render --skill=pr-to-video --quality high --output renders/video.mp4`

Do not rerun `lint`, `check`, or `snapshot` after rendering unless the user asks.

After the user is done reviewing (or after render when no more live edits are expected), stop only this project's background server: `npx hyperframes preview "$PROJECT_DIR" --stop`. Never tear it down while waiting for review.

**Gate:** `lint` and `check` passed and the snapshots were inspected before render; user approved at the review pause (autonomous: checks passed and the delivery includes the contact sheet); `renders/video.mp4` exists. Final reply states the MP4 path and final duration.

---

## Quick Reference

**Formats:** landscape `1920x1080`; portrait `1080x1920`; square `1080x1080` — derived from the destination (brief contract § 2). Set the format once in the storyboard frontmatter.

**PR deltas vs a captured-asset workflow:** no Step 1 capture (the `gh` CLI ingests the PR into a synthetic `capture/extracted/` package — `tokens.json` + `visible-text.txt` + `people.json`); the only real assets are the contributors' `assets/<login>.png` avatars (the credits close); no `asset-descriptions.md`, no asset-staging step. Code beats are rendered by the `code-*` registry blocks on code-editorial's navy Code Surface; the style is always **code-editorial**.

**Background scripts:** the workflow ships these under `scripts/`: `fetch-pr` (PR → `capture/pr.json` + `diff.patch` via `gh`; large-PR-safe, no scratch), `ingest` (→ synthetic capture package; offline), and `fetch-people-avatars` (contributor avatars → `assets/`); plus the shared engine — `build-frame` (adopt + brand-remix a preset into `frame.md` + caption skin), `audio` (TTS, BGM, SFX, duration sync), `captions`, `transitions` (inject + verify), and `assemble-index`. Everything else is the `hyperframes` CLI. Code blocks install via `npx hyperframes add <name>`.

The reusable, domain-agnostic shot shapes live in `../hyperframes-animation/blueprints/` (indexed by `../hyperframes-animation/blueprints-index.md`); the `code-*` registry blocks are the code-beat vocabulary (`references/code-vocabulary.md`).

| Read                                                                                                                                                        | When                                                                                                     |
| ----------------------------------------------------------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------- |
| `[../hyperframes/references/brief-contract.md](../hyperframes/references/brief-contract.md)`                                                                | Gate types, mode derivation from `BRIEF.md`, field semantics.                                            |
| `[../hyperframes-creative/references/story-spine.md](../hyperframes-creative/references/story-spine.md)`                                                    | Step 3: story doctrine — hook language, value-before-evidence, proposal shape, source-traceable visuals. |
| `[references/story-design.md](references/story-design.md)`                                                                                                  | Step 3: plan the PR explanation.                                                                         |
| `[../hyperframes-animation/blueprints-index.md](../hyperframes-animation/blueprints-index.md)`                                                              | Step 3: role→blueprint menu. Step 4: pick the shot shape.                                                |
| `[../hyperframes/references/storyboard-format.md](../hyperframes/references/storyboard-format.md)`                                                          | Step 3: write `STORYBOARD.md`.                                                                           |
| `[../hyperframes/references/script-format.md](../hyperframes/references/script-format.md)`                                                                  | Step 3: write `SCRIPT.md`.                                                                               |
| `[../media-use/audio/references/tts.md](../media-use/audio/references/tts.md)`                                                                              | Step 3.1: choose or understand TTS providers.                                                            |
| `[references/visual-design.md](references/visual-design.md)`                                                                                                | Step 4: write the frame's shot sequence (+ Layout vocabulary).                                           |
| `[references/code-vocabulary.md](references/code-vocabulary.md)`                                                                                            | Step 4 + 5: pick + fill the `code-*` block for a code beat.                                              |
| `[references/motion-language.md](references/motion-language.md)`                                                                                            | Step 4: the motion vocabulary + the motion doctrine.                                                     |
| `[references/cut-catalog.md](references/cut-catalog.md)`                                                                                                    | Step 4-5: the cut catalog (worker builds within-frame seams).                                            |
| `[../hyperframes-animation/rules-index.md](../hyperframes-animation/rules-index.md)` + `[../hyperframes-animation/rules/](../hyperframes-animation/rules/)` | Step 5: local rule recipe bodies for the cited motions.                                                  |
| `[../hyperframes/references/frame-worker-core.md](../hyperframes/references/frame-worker-core.md)`                                                          | Step 5: the shared worker contract (packet builder prepends it to the delta).                            |
| `[sub-agents/frame-worker.md](sub-agents/frame-worker.md)`                                                                                                  | Step 5: the workflow's frame-worker delta.                                                               |
| `[../hyperframes/references/subagent-dispatch.md](../hyperframes/references/subagent-dispatch.md)`                                                          | Step 5: dispatch sub-agents safely.                                                                      |
| `[../hyperframes-creative/frame-presets/code-editorial/FRAME.md](../hyperframes-creative/frame-presets/code-editorial/FRAME.md)`                            | Step 2: the code-editorial preset (fixed style).                                                         |


<!-- ===== FILE: hyperframes/pr-to-video/references/code-vocabulary.md ===== -->

# Code vocabulary — the `code-*` animation blocks

<!-- registry-items: allow=data-duration,number-lockup,dark-plus,light-plus,dark-modern,light-modern,dark-2026,light-2026,solarized-light,visual-studio-dark,visual-studio-light,high-contrast,high-contrast-light,clear-dark,clear-light,man-page,red-sands,silver-aerogel,solid-colors -->

**The live search is the source of truth for what the registry has.** The table(s) below are a hand-maintained sample and under-cover by design: run `npx hyperframes catalog --query "<what you want>" --json` — it needs nothing installed — before concluding the registry lacks something. Item names here are checked against `registry/registry.json` by `bun run lint:skills`.

PR videos run on two kinds of moving picture: **code** (the lines that changed) and **behavior** (what the change _does_ at runtime). This file is the vocabulary for both — the `code-*` blocks for code beats, and the **mechanism beat** (an invented animated diagram, or a `flowchart` / `data-chart`) for behavior beats. A video that is _all_ code reads flat; **alternate the two** (story-design plans the rhythm; see "Showing behavior" below).

For code beats the registry ships purpose-built **code animation blocks** that render a diff, a typed-on snippet, a morph, a highlight, a scroll, or a 3D/particle/dissolve reveal — far better than hand-built motion. **Reach for one of these first** for any code beat; fall back to hand-authored composition only when none fits.

- **Step 4 (visual design):** for each `diff` / `before_after` / code beat, name the block in the frame's `scene` (e.g. "the `request()` retry block, ~6 lines, `code-diff`"). One judgment call: which block.
- **Step 5 (frame worker):** install the named block and fill it with the real diff/snippet (below). The block is the frame's centerpiece, composited onto code-editorial's navy **Code Surface**.

## Install + use

Every block installs the same way (confirmed `packages/cli/src/commands/add.ts`):

```bash
npx hyperframes add <block-name>     # writes compositions/<block-name>.html
```

It is a self-contained sub-composition (inlined engine; a paused GSAP timeline the engine seeks per frame). Mount it in the frame as a sub-composition clip:

```html
<div
  data-composition-id="code-diff"
  data-composition-src="compositions/code-diff.html"
  data-start="0"
  data-duration="6"
  data-track-index="1"
  data-width="1920"
  data-height="1080"
></div>
```

**Customize by editing two globals** in the installed HTML's inline `<script>`:

- `window.__TOKENS` — the code content, baked as Shiki tokens: `{ <seq>: { lang, theme, bg, fg, states: [ { code, tokens:[ {key, content, color, fontStyle} ] } ] } }`. Replace `code`/`tokens` with the PR's real snippet(s). `fontStyle` is a bitmask (`&1` italic, `&2` bold). The blocks bake `theme: "github-dark"` independently of the `code-snippet-*` themes below.
- `window.__BLOCK` — selects the effect + timing: 2D `{ id, effect, seq, line?, duration }`; WebGL `{ id, effect, seq, duration, seed }`.

The timeline registers synchronously at `window.__timelines[id]`. All blocks are **1920×1080** and **deterministic / seek-safe** (no CSS transitions, no rAF, seeded randomness — never `Math.random` / `Date.now`).

## The animation blocks

| Block                        | What it does                                                                                                      | Inputs of note                                                                                        | PR beat                                                                                   |
| ---------------------------- | ----------------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------- |
| **`code-diff`**              | Unified diff inside an editor window: removed lines collapse in red, added lines expand in green, staggered. (6s) | `__TOKENS.diff.states` needs **exactly 2 states** (before, after) — the engine LCS-diffs them.        | The diff hunk (before→after); literal add/remove semantics. **The default PR block.**     |
| **`code-morph`**             | One snippet transforms into another — shared tokens glide (FLIP), leavers fade out, enterers fade in. (7s)        | `__TOKENS.morph.states` (2+); reuse the same token `key` across states for a token that should glide. | A refactor / rename / signature change where continuity matters (not add/remove framing). |
| **`code-typing`**            | Per-character typewriter reveal with a gliding caret. (5s)                                                        | single state in `__TOKENS.feature.states[0]`.                                                         | A new function / file **written on screen** ("here's what we added").                     |
| **`code-highlight`**         | A blue band sweeps one line; the rest dim. (5s)                                                                   | `__BLOCK.line` = target line, **0-based here**. single state.                                         | "This one line is the change" — spotlight a changed/important line. Quick callout.        |
| **`code-scroll`**            | "Camera" scrolls a long file to center a target line, dims the rest. (6s)                                         | `__BLOCK.line` = target, **1-based here**. one long state.                                            | Locating the change in a large file. The only block built for long files.                 |
| **`code-3d-extrude`**        | Code on a lit, beveled 3D slab that rotates and settles. (8s, WebGL)                                              | single state; `__BLOCK.seed`. `<canvas id="gl">`.                                                     | A hero / title code moment ("the feature"). Style over density — not for reading a diff.  |
| **`code-particle-assemble`** | GPU particles scatter, then fly to the exact glyph pixels and resolve to syntax color. (8s, WebGL)                | single state; `__BLOCK.seed`.                                                                         | A dramatic climax reveal of a key snippet. Flashiest; not for line-by-line reading.       |
| **`code-shader-dissolve`**   | Code "compiles into existence" out of seeded noise with a moving dissolve front + edge glow. (7s, WebGL)          | single state; `__BLOCK.seed`.                                                                         | A "compiles / builds / works now" beat, or a polished snippet reveal.                     |

**Gotchas (call out so the worker doesn't trip):**

- **Fit the cadence to the frame's `data-duration`.** Each block carries its own internal timing — `code-typing` types at a fixed per-character speed, so a snippet that's long relative to a short frame **overruns**: the code never finishes typing within `data-duration`, and the chrome beats around it (an underline, a `+N/−M` count-up) never play. Check **char-count × per-char cadence** (plus the block's settle) against `data-duration`, and tune the timing so the **full block lands inside the frame**. This is the one code-motion knob you MUST set to the frame — you're fitting the _timing_, not redesigning the effect (the typewriter / diff / morph stays the block's).
- `code-diff` and `code-morph` need **≥2 baked states**; every other animation block uses a single state.
- **Line indexing differs:** `code-highlight` is **0-based** (`line: 1` = the 2nd line); `code-scroll` is **1-based**. Don't off-by-one.
- **No caption-safe band.** These are full-bleed 1920×1080 code surfaces with no reserved caption area. When captions are enabled, the frame must keep the code panel clear of the bottom caption keep-out band (composite the block in the top ~83%, or scale/inset it) — the worker owns that, not the block.

## The `code-snippet-*` theme family (standalone, not palettes)

These are **NOT palettes you attach to the animation blocks** — each is its own ready-made ~11–12s composition rendering a full developer UI with baked typing and its own timeline. Use one when you want **ambient realistic context** (a real IDE or terminal on screen), not a focused diff. Install the specific one: `npx hyperframes add code-snippet-<name>`.

- **VS Code workbench (12):** full VS Code window (activity bar, file-tree, tabs, editor with per-char typing, integrated terminal running `pytest`, status bar) in each theme. `dark-plus`, `light-plus`, `dark-modern`, `light-modern`, `dark-2026`, `light-2026`, `monokai`, `solarized-light`, `visual-studio-dark`, `visual-studio-light`, `high-contrast`, `high-contrast-light`. (Each pulls a `background.jpeg` into `assets/`.)
- **Apple Terminal (12):** macOS Terminal.app window typing a shell command per profile. `apple-terminal-` + `basic`, `clear-dark`, `clear-light`, `grass`, `homebrew`, `man-page`, `novel`, `ocean`, `pro`, `red-sands`, `silver-aerogel`, `solid-colors`.

The theme is baked into each block (not chosen at runtime); to use a given look, install that block and edit its `codeLines`. For code-editorial's editorial register, prefer the focused animation blocks on the navy Code Surface; reach for a `code-snippet-*` UI only when "show it in a real editor/terminal" is the point.

## Showing behavior — the mechanism beat (not a `code-*` block)

A `code-*` block shows **the code**. It does not show **what the code does**. The single biggest cause of a flat PR video is a body that is all code surfaces — so for any change with a visible runtime behavior, plan a **`mechanism` beat** that _animates the behavior_ (story-design owns the rhythm; this is the vocabulary).

A mechanism beat is **not** a registry `code-*` block. It is one of:

- an **invented animated diagram** — SVG / HTML / GSAP the frame worker builds from code-editorial's atoms (hairline-ink nodes / edges / lanes on cream, one coral marker on the active element), the build playing out the behavior across the shot; **or**
- a **`flowchart` / `flowchart-vertical`** registry block — a process / pipeline / state flow; **or**
- a **`data-chart`** registry block — a perf / metric comparison (two bars or timelines racing).

`flowchart`, `flowchart-vertical`, and `data-chart` install exactly like a code block (`npx hyperframes add <name>`) and mount as a sub-composition — so when a `mechanism` frame names one in its `scene`, Step 5 pre-installs it alongside the `code-*` blocks. An invented SVG/GSAP diagram needs no install (the worker hand-builds it).

**What to animate, by what the change touches** (the menu story-design plans from):

| The change touches…             | Animate (the behavior)                                                  | Use                    |
| ------------------------------- | ----------------------------------------------------------------------- | ---------------------- |
| Retry / backoff / resilience    | request lifecycle: fire → 500 → wait (delay growing) → retry → 200      | invented SVG/GSAP      |
| Caching / memoization           | two lanes racing: cold (hits DB) vs cached (hits cache)                 | invented SVG/GSAP      |
| Concurrency / parallelism       | a serial lane reshaping into parallel lanes                             | invented / `flowchart` |
| Race / ordering bug             | the broken flow (dropped items, colliding writers), then the fixed flow | invented SVG/GSAP      |
| Performance                     | two timelines / bars racing, the new one finishing first                | `data-chart`           |
| Refactor / migration            | a tangled call-graph untangling; same inputs → same outputs             | `flowchart` / invented |
| New endpoint / pipeline / state | data flowing the new path; a state machine lighting up step by step     | `flowchart-vertical`   |

Unlike a `code-*` block (which owns its own animation), the diagram's motion is **yours** — sequence ≥3 effects into entrance (draw the nodes / lanes) → development (run the flow) → settle (the resolved state + one coral emphasis). Never let it enter then freeze.

## PR beat → block cheat-sheet

| PR moment                                                | Block(s)                                                                                                                                                         |
| -------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Diff hunk (before → after)                               | `code-diff`                                                                                                                                                      |
| Refactor / rename / signature change (continuity)        | `code-morph`                                                                                                                                                     |
| Failing → passing test (red → green)                     | `code-morph` or `code-diff` + `code-highlight` on the green line; a `code-snippet-*` VS Code/terminal block for a literal test-runner UI                         |
| New function / file typed on                             | `code-typing`                                                                                                                                                    |
| Spotlight one changed line                               | `code-highlight`                                                                                                                                                 |
| Walk / scroll a long changed file                        | `code-scroll`                                                                                                                                                    |
| Hero / title code moment ("the feature")                 | `code-3d-extrude`                                                                                                                                                |
| "Compiles / builds / works now" reveal                   | `code-shader-dissolve`                                                                                                                                           |
| Big dramatic snippet reveal / climax                     | `code-particle-assemble`                                                                                                                                         |
| A benchmark / metric / count-up                          | **Not a `code-*` block** — use code-editorial's `number-lockup` (Number/Impact treatment) or the `data-chart` registry block                                     |
| **What the change DOES at runtime** (behavior, not code) | **Not a `code-*` block** — a `mechanism` beat: an invented SVG/GSAP diagram, or `flowchart` / `flowchart-vertical` / `data-chart`. See "Showing behavior" above. |
| Show the change in a realistic IDE / terminal (ambient)  | a `code-snippet-*` VS Code theme (editor) or Apple Terminal profile (CLI run)                                                                                    |


<!-- ===== FILE: hyperframes/pr-to-video/references/cut-catalog.md ===== -->

# Cut catalog — within-frame seams (worker-built)

> **A worker build-recipe (Step 5) — the sibling of `../../hyperframes-animation/rules/`, not a second motion doc.** These are within-frame cuts the **frame worker builds INSIDE its own composition** (Z-scale + blur + opacity tweens, or per-word x-staggers, all on the frame's own paused GSAP timeline). They are **not** the between-frame transition: story owns that via `transition_in`, which the harness's injector stamps from a **separate registry vocabulary** (`crossfade` / `blur-crossfade` / `push-slide` / `zoom-through` / `squeeze`) — the catalog names here (**cut-the-curve / inverse-zoom / waterfall**) are **not** valid `transition_in` values. Use this catalog when a frame's shot sequence has an internal seam — a within-scene text/element swap, a **Scene-to-Scene** cut (a `Scene` is a time window WITHIN one frame, **not** a frame-to-frame boundary), or a text-to-text line change — and you want it to read as one continuous move instead of a hard slideshow cut. (`zoom-through` lives in both worlds: a whole-frame wrapper transition in the registry, an element-level Z-cut here — same idea, different scope.)

Four techniques that create depth and continuity:

1. **Zoom-Through** — within-scene text swaps, Z-axis, moving TOWARD the viewer
2. **Inverse Zoom-Through** — Z-axis swaps moving AWAY from the viewer
3. **Cut the Curve** — between-scene transitions on x/y
4. **Waterfall Cut** — word-by-word cut-the-curve with staggered exits and entries

All four are the same underlying principle: **cut at peak velocity, match direction and
speed on both sides of the cut.** The differences are axis, scope, and granularity.

**Choosing which at a seam:** for an UNFINISHED phrase (building one larger idea across
several visually distinct scenes that still approach the same point — multi-line text, a
run of consecutive cards) use **cut-the-curve** / **waterfall**. For a STATE CHANGE (turning
to a NEW part of the video — most often hook → context, between two distinct chapters) use
**zoom-through**, and **inverse zoom-through** for an arrival / payoff beat. Chain these so
the frame's internal seams feel like one camera moving through the content.

---

## Blur Logic (applies to all Z-axis variants)

Blur sells the speed at the cut, but it must scale with the SUBJECT SIZE:

| Subject                                                | Peak blur   | Why                                                                                                                                                                                      |
| ------------------------------------------------------ | ----------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Text-scale (headline, line, word group)                | **10px**    | At 20px text smears into illegibility — the eye loses the word it was tracking and the cut reads as a glitch, not speed. At 20px letterforms go mushy mid-cut; 10px keeps them readable. |
| Full-frame surface (terminal window, card, screenshot) | **18–20px** | Big surfaces have edges and texture that survive heavy blur; lighter blur on a full-frame move reads as a rendering hiccup instead of motion.                                            |

Both sides of a cut use the SAME peak blur — the value must match at the swap frame.
Apply blur to the WRAPPER, never to individual children.

---

## 1. Zoom-Through (forward)

### The Problem

Text enters, holds, exits. Then next text enters, holds, exits. Each text block is
independent — no depth, no continuity. The video feels like a slideshow.

### The Principle

A velocity-matched cut on the Z-axis. You **never see both texts at the same time.** The
outgoing text scales toward the viewer (accelerating), blur and opacity peak at the cut
point hiding a hard swap, and the incoming text continues scaling up from behind
(decelerating into the focal plane). One continuous forward motion, two different texts.

### The Three Phases

**Phase 1: Exit** — text accelerates forward (toward viewer)

- Scale: `1.0 -> 1.2`, Blur: `0px -> 10px` (text-scale; see Blur Logic), Opacity: `1.0 -> 0.15`
- Scale/blur easing: `power3.in` (steep acceleration)
- Opacity easing: `none` (linear — even dimming, separated from scale)
- Duration: 0.2s

**Phase 2: Hard cut** at peak velocity + peak blur

- Outgoing: `opacity: 0` (instant via `tl.set`)
- Incoming: `opacity: 0.15, scale: 0.75, blur: 10px` (instant via `tl.set`)
- All properties match at the cut: blur, opacity, and scale DIRECTION (both scaling up)

**Phase 3: Entry** — text continues forward (growing into focal plane)

- Scale: `0.75 -> 1.0`, Blur: `10px -> 0px`, Opacity: `0.15 -> 1.0`
- Easing: `expo.out` (steep initial burst matching exit velocity, long settle)
- Duration: 0.5s

### Why Opacity Must Be Separate on Exit

Scale uses `power3.in` but that keeps opacity near 1.0 for most of the tween. Splitting
opacity to its own tween with linear ease makes the dimming even. On entry, all properties
can share `expo.out`.

---

## 2. Inverse Zoom-Through (backward)

The mirror: the camera "pulls back" instead of pushing through. The outgoing element
RECEDES away from the viewer; the incoming element arrives OVERSIZED (as if it had been
just behind the camera) and retracts into the focal plane. Both move in the shrinking
direction — same-direction rule preserved, just reversed.

**When to use over the forward variant:** arrival beats. The incoming element lands with
presence because it comes from larger-than-frame — right for a payoff line ("That changes
today."), a giant reply, or a held end-state. Forward zoom-through reads as _progressing
through_ content; inverse reads as _arriving at_ content.

### The Three Phases

**Phase 1: Exit** — element recedes (away from viewer)

- Scale: `1.0 -> 0.8`, Blur: `0px -> 10px` (text-scale)
- Scale/blur easing: `power3.in`; Opacity: `1.0 -> 0.15` on `none` (separate tween)
- Duration: 0.2s

**Phase 2: Hard cut**

- Outgoing: `opacity: 0` via `tl.set`
- Incoming: `opacity: 0.15, scale: 1.25, blur: 10px` via `tl.set`

**Phase 3: Entry** — incoming retracts into place

- Scale: `1.25 -> 1.0`, Blur: `10px -> 0px`, Opacity: `0.15 -> 1.0`
- Easing: `expo.out`, Duration: 0.5s

---

## 3. Cut the Curve (Scene Transitions)

### The Principle

Use cut-the-curve for **all scene-to-scene transitions** on x and y axes. The outgoing
scene's hero element accelerates in one direction, the cut lands mid-motion, and the
incoming scene's hero element continues moving in the **same direction** and decelerates.
Nothing exits fully off-screen and nothing enters from fully off-screen — **speed plus
opacity fading trick the eye**; the partial moves are enough.

### Same Path, Same Direction

If Scene A's hero slides left, Scene B's hero enters from the right and continues sliding
left. Both move leftward. One continuous motion.

| Direction | Scene A exit   | Scene B entry start | Scene B entry end |
| --------- | -------------- | ------------------- | ----------------- |
| Leftward  | `x: 0 -> -230` | `x: +230`           | `x: 0`            |
| Rightward | `x: 0 -> +230` | `x: -230`           | `x: 0`            |
| Upward    | `y: 0 -> -230` | `y: +230`           | `y: 0`            |
| Downward  | `y: 0 -> +230` | `y: -230`           | `y: 0`            |

### Velocity matching via mirrored eases

The cleanest match: exit `power4.in` and entry `power4.out` with the SAME distance and
duration — mathematically the two halves of one `power4.inOut` composite, so the entering
element picks up at exactly the 50% point of the notional path at identical velocity
(e.g. 230px / 0.3s ≈ 3,070 px/s at the cut on both sides).

The fade trick: the exit's opacity completes at ~25–30% of its travel (fade duration
≈ 0.18–0.3s vs motion 0.3–0.34s) — the element vanishes while still visibly accelerating,
and nothing has to reach the frame edge. Entry fades IN fast from ~0.35 under its
deceleration. Time the LAST fading element to die right at the hard cut — gaps where
nothing is moving read as awkward dead air.

### Rules

- Use cut-the-curve for all scene transitions — it's the default, not an accent
- Same direction on both sides; mirrored `.in`/`.out` eases, same distance + duration
- Exit duration short (0.2–0.4s), entry duration >= exit duration
- Partial travel + fade, never full off-screen moves

---

## 4. Waterfall Cut (word-by-word cut-the-curve)

Cut-the-curve at WORD granularity — the strongest version of the leftward cut for
text-to-text seams. Each word of the outgoing line ramps out on its own pronounced curve;
each word of the incoming line cascades in mid-flight. The stagger turns the cut into a
wave the eye rides across the seam.

### Exit (per word)

- Motion: `x: 0 -> -230` over 0.34s on **power4.in** — a much more pronounced ramp than
  the usual power2: the word barely creeps, then RIPS
- Fade: `opacity -> 0` over 0.18s (separate tween, `power1.in`) — completes when the word
  is only ~25–30% into its travel
- Stagger: reading order, ~0.022s per word, timed so the LAST word finishes fading right
  at the hard cut

### Entry (per word)

- `fromTo x: +230 -> 0, opacity: 0.35 -> 1` over 0.3s on **power4.out** — the mirrored
  back half of the composite; every word ignites already moving at matched velocity
- Waterfall stagger with SHRINKING gaps (start 0.05s, multiply by ~0.84 per word) so the
  cascade accelerates across the line — the cascade should speed up word over word, not run
  at a flat per-word delay
- Pre-set all words to `x: +230, opacity: 0` at build time — `immediateRender: false`
  alone leaves un-started words sitting visible at rest during the stagger window

### Whole-line variant

A single-line beat (e.g. a big intro line) exits as one group with the same pronounced
ramp, but stretch its fade to ~0.3s ending ~0.02s before the cut — a lone element that
fades early leaves dead air that a word cascade would have covered.

---

## Choosing a Variant

|                | Zoom-Through                | Inverse Zoom                | Cut the Curve     | Waterfall Cut             |
| -------------- | --------------------------- | --------------------------- | ----------------- | ------------------------- |
| Scope          | Within-scene text swap      | Arrival/payoff beat         | Between scenes    | Text-to-text seam         |
| Axis           | Z, toward viewer            | Z, away from viewer         | X / Y             | X, per-word               |
| Peak blur      | 10px text / 20px full-frame | 10px text / 20px full-frame | none required     | none (fade does the work) |
| Opacity at cut | 0.15                        | 0.15                        | exit faded by cut | last word dies at cut     |
| Feel           | progressing through         | arriving at                 | carried sideways  | a wave across the seam    |

---

## Anti-Patterns

| Don't                                    | Why                                         | Instead                                                |
| ---------------------------------------- | ------------------------------------------- | ------------------------------------------------------ |
| Two texts visible during a zoom-through  | Overlapping text breaks the Z-axis illusion | Hard cut at blur peak, one text at a time              |
| 20px blur on text-scale subjects         | Letterforms smear; reads as a glitch        | 10px for text, 18–20px only full-frame                 |
| Elements on different paths across a cut | Eye tracks one direction, cut goes another  | Same property, same direction                          |
| Mismatched blur/opacity at the swap      | Visible flash or brightness jump            | Identical values at the cut frame                      |
| Gentle easing on entry (`power2.out`)    | Entry velocity feels slower than exit       | Mirror the exit: `power4.out` / `expo.out`             |
| Full off-screen exits / entries          | Wastes time and breaks the speed illusion   | Partial travel + early fade                            |
| Lone element fading long before its cut  | Dead air at the seam                        | Fade ends ~0.02s before the cut, or use a word cascade |
| Zoom-through on body text                | Small text at 0.75 scale is unreadable      | Only headlines and short phrases                       |
| Scene cuts without cut-the-curve         | Static cuts feel like a slideshow           | Cut-the-curve is the default                           |


<!-- ===== FILE: hyperframes/pr-to-video/references/motion-language.md ===== -->

# Motion language — the move vocabulary + the motion doctrine + the seek-safe core

> The motion layer for **Step 4 (Visual design)**. When you write a frame's **time-coded shot sequence**, you name each scene's move **inline from the vocabulary below** — a named palette of the moves the golden corpus actually uses. Each move carries the **backing rule id** in this skill's local `../../hyperframes-animation/rules/`; cite that id so the move resolves to a real recipe when a **frame worker** implements it in Step 5 (the worker reads the rule body in `../../hyperframes-animation/rules/<id>.md` — it reproduces the move, it does not guess from the name). You name motion by **role / move name**, never by raw GSAP curve, ms, or stagger formula — the worker maps the curve. Between-frame **transitions are not yours**: story names `transition_in`, the harness injects it; that injected transition **is** the frame's exit. For cuts a worker builds INSIDE a frame (within-scene swaps, scene-to-scene seams), see the catalog in `cut-catalog.md`.

A good code-change explainer feels like one continuous film — one camera, one motion feel, **smooth and timed to the voiceover** — not a pile of slides that animate once and freeze. In a PR explainer the development often _is_ the reveal: the diff hunk typing in, the before→after morph, the impact stat landing. The doctrine in Part 2 is load-bearing: when in doubt, do what it says.

---

# Part 1 — the move vocabulary

Reach into this palette when naming a scene's motion. Pick the move that matches the beat, name it in the shot sequence, and cite the rule id after `→`. The blueprints (`../../hyperframes-animation/blueprints/`) name these same moves in their `rule mapping`; you're drawing from one shared palette. Compose 2–4 across a shot's scenes (entrance → sequential reveal → settle), not all at once.

## Kinetic type

- **hard-cut / flash word-swap** — a word or line replaces the previous one on an instant cut (no fade/roll); the swap itself is the beat. → `discrete-text-sequence`
- **in-place token cycle** — a fixed line holds and only its variable slot changes, token → token → token. → `discrete-text-sequence`
- **per-word staggered reveal** — a phrase assembles word-by-word (or chunk-by-chunk), each landing on its own beat. → `dynamic-content-sequencing`
- **kinetic beat-slam** — short phrases slam in on a shared percussive beat array, each with a distinct entrance, resolving on a locked finale; the recipe for "punchy / rhythmic" taglines. → `kinetic-beat-slam`

## Typewriter

- **type-on with caret** — text types in character-by-character behind a blinking caret. → `discrete-text-sequence` (+ `context-sensitive-cursor` for the caret blink / color)
- **backspace-and-retype** — the line types, deletes the last word(s), and retypes a new one (typo-correction, reframe). → `discrete-text-sequence` (+ `context-sensitive-cursor`)

## Count-up / data

- **value-scaled counter** — a number counts up and its font size grows with the value, so the climb itself escalates. → `counting-dynamic-scale`
- **bars / progress / star wipe** — a number paired with a graphic that fills: bar-height stagger, a progress bar / ring filling, a fractional star-rating wipe. → `stat-bars-and-fills`

## Reveal / decode

- **3D char flip-decode** — characters flip in 3D and resolve from scrambled glyphs to the real text (decryption feel). → `hacker-flip-3d`
- **SVG self-draw** — an outline / icon / ring draws itself stroke-by-stroke. → `svg-path-draw`

## Camera

- **push / focus / drift** — a sequential camera move on the frame root (pull-back → focus → push) plus continuous micro-drift; the cinematic baseline. → `multi-phase-camera`
- **zoom-to-target** — zoom into a non-centered element (scale + counter-translate to keep it framed). → `coordinate-target-zoom`
- **pan / focus-lock** — a virtual camera transforming one `.world` wrapper to pan / zoom / lock onto a region. → `viewport-change`
- **camera-cursor-tracking** — the viewport locks to a moving focal point (a typing cursor), static framing then focal-locked tracking. → `camera-cursor-tracking`

## Layout motion

- **cluster→outward expansion** — elements start clustered at center and expand outward to their final positions in lockstep. → `center-outward-expansion`
- **orbit** — elements flip in from 3D space and settle into a continuous elliptical orbit (entry flips in-place at the orbital position). → `orbit-3d-entry`
- **split-tilt cards** — two cards side-by-side with opposing rotationY tilts, entering from their respective sides (comparison / before-after). → `split-tilt-cards`
- **logo/avatar ring + connectors** — avatars or logos on an elliptical ring with SVG connection lines to a center point, staggered entry. → `avatar-cloud-network`

## Surface / UI

- **3D page-scroll reveal** — a full webpage as a tilted 3D card whose internal content scrolls to reveal specific sections. → `3d-page-scroll`
- **cursor click + ripple** — a cursor moves to a target, depresses with it on click, and emits an expanding ripple. → `cursor-click-ripple`
- **button press** — a tactile press: compression then spring recovery, optional release burst / glow. → `press-release-spring` (or `physics-press-reaction` for a click that compresses cursor + target together)
- **keyword glow** — keywords light up with glow + scale + color on an attack-decay-rest envelope, synced to a word rail. → `asr-keyword-glow`

## Morph / handoff

- **scale-swap** — two elements at the same screen center hand off: the outgoing cluster shrinks + fades as the incoming one arrives. → `scale-swap-transition`
- **card morph-anchor** — a container morphs apparent size + corner radius + surface between two shots, then fades to reveal the real target beneath (HyperFrames uses uniform `scale`, not `width`/`height`). → `card-morph-anchor`

## Seam cuts (worker-built, inside a frame)

The velocity-matched cuts a worker authors between a frame's own Scenes. Name the seam in the shot sequence; the recipe is in the catalog, not a single `../../hyperframes-animation/rules/` id.

- **zoom-through / inverse zoom-through** — a within-scene swap on the Z-axis; forward reads "progressing through", inverse reads "arriving at" (payoff). → `cut-catalog.md`
- **cut-the-curve** — a scene-to-scene cut where both sides move the same direction at matched velocity. → `cut-catalog.md`
- **waterfall cut** — cut-the-curve at word granularity, a wave across a text-to-text seam. → `cut-catalog.md`

## Emphasis / marker

- **highlight / circle / burst / scribble** — a marker-drawn emphasis on a word or element: yellow highlight sweep, hand-drawn circle, radiating burst, scribble, or rough sketch-outline. → `css-marker-patterns`

## Aliveness during a hold (use sparingly — see Part 2)

- **subtle jitter** — the sanctioned way to keep a settled frame alive: a small, low-amplitude positional/scale jitter on the held element. The motion-graphics trick that reads "alive" without reading "weak." → `sine-wave-loop` (low-amplitude register)
- **live SVG internals** — internal SVG parts move so an icon feels alive (rotating hands, oscillating blades, pulsing dots, dash-flow); fine because it's the subject doing something, not a card breathing. → `svg-icon-enrichment`
- **finite bounded ambient** — a single bounded breathe/drift on ONE held hero, only when genuinely needed; de-emphasized — prefer sequential reveal or jitter first. → `sine-wave-loop`

## The added moves — now backed by local rules

Five moves the golden corpus needs were added to this skill's `../../hyperframes-animation/rules/`, rounding out the vocabulary above:

- **depth-of-field / selective-blur** — blur the off-focus subset to spotlight the focal element → `depth-of-field-blur`
- **motion-blur streak** — directional velocity blur on a fast fly-in / camera push-through → `motion-blur-streak`
- **3D depth scatter-assemble** — glyphs/elements scatter into a tumbling 3D cloud, then reassemble → `depth-scatter-assemble`
- **spring-pop entrance** — the canonical entrance pop; default to a smooth long-tail settle, overshoot only when explicitly playful → `spring-pop-entrance`
- **ambient glow / bloom** — un-triggered soft glow blooming behind a static hero → `ambient-glow-bloom`

---

# Part 2 — the motion doctrine (load-bearing)

These four rules are the difference between a clip that reads as a serious code-change explainer and one that reads as an agent-made PowerPoint. Follow them as written.

## 1. Smooth beats bouncy — `power3` is the default

Elements should use **long-tail decel curves that let them settle smoothly. `power3` is enough in most cases.** No bouncy, no overshoot, no `back.out` / `bounce.out` / `elastic.out` as a default.

Bouncy is the **#1 instant turn-off** in user-made Remotion / HyperFrames videos, and the agent almost never gets it right — it thinks bouncy adds emphasis, but it buys that emphasis at the cost of cleanliness. The serious motion-design shops feel the same. **Smooth always wins.** Overshoot is demoted to a **rare, explicitly-playful exception** (a consumer/fun logo slam, a deliberate bell-hit) — never the house style. Name the intent as a long-tail settle; the worker maps `power3` (or `expo.out` on a fast arrival). See `../../hyperframes-animation/rules/spring-pop-entrance.md` — it now leads with the smooth settle. (The exact form of that settle is a critically-damped spring; the worker has a baked, seek-safe `springEase` — ζ=1 — in `../../hyperframes-animation/adapters/gsap-easing-and-stagger.md` → Spring Eases for when the settle is the hero. Real physics, same doctrine — not a license for bounce.)

## 2. Sequential reveal in the back ~50%, timed to the voiceover

This is the anti-PowerPoint mechanism — sharper than "put development in the middle."

- **Don't dump everything on screen in the first ~25%** of the scene. Rushing all content in up front is exactly what forces the slideshow feel.
- **Reveal each piece — a line, a card, even an h1 — when the voiceover mentions it**, sequencing reveals across the **later ~50%** of the scene. Same amount of agent work, but the cut becomes coherent and gains rhythm.
- **Less is more.** Fewer things on screen, each arriving on its VO beat, beats a full canvas that animated once and froze.

Practically: a frame's shot sequence front-loads almost nothing — the entrance carries only what the VO is saying at t=0, and the rest of the elements wait in the timeline for their spoken cue. A reveal maps onto a development-class move from Part 1 (`per-word staggered reveal`, `cluster→outward expansion`, a `count-up`, an `asr-keyword-glow` synced to the word rail).

## 3. No lazy breathing, no bad pan/push — "no motion over bad motion"

The agent's two reflexive ways to fake "aliveness" both read cheap:

- **No lazy breathing.** Scaling cards/text up and down in a circular loop to look "alive" is the cheap tell. Don't reach for it.
- **No bad slow pan / push in the back half.** A slow pan or push on elements in the later ~50% of a scene **disrupts the viewer's sightline and causes eye discomfort** — it actively makes the frame worse, not better.

The fix for both is the same: **stagger element reveals in time with the script** (rule 2). And the governing principle: **"I'd rather have NO motion than BAD motion."** A held, still frame is better than a frame kept "alive" by breathing or a drifting camera. The **only sanctioned aliveness** during a hold is **subtle jitter** — a small low-amplitude jitter that keeps a frame from feeling dead without looking weak (it's in Code editorial videos now). Everything else holds.

## 4. Internal seams are velocity-matched cuts

When a frame has an internal seam — a within-scene swap, a Scene-to-Scene cut, a text-to-text line change — make it a **velocity-matched cut**, not a hard slideshow cut: cut at peak velocity, match direction and speed on both sides. The catalog (the four techniques, the blur logic, and which to use when) is `cut-catalog.md`; the moves are listed under **Seam cuts** in Part 1.

## One-line summary

Smooth long-tail (`power3`) over bouncy; reveal sequentially in the back ~50% timed to the VO (not dumped in the first 25%); no lazy breathing and no bad slow pan/push — prefer stillness, with subtle jitter as the only aliveness; cut at peak velocity with matched direction/speed (→ `cut-catalog.md`).

---

# Part 3 — the seek-safe core (hard rules)

The frame is a **paused GSAP timeline seeked frame-by-frame**, so some "continuous" intents from a real-time engine can't render — don't name them. These are non-negotiable regardless of doctrine.

- **No infinite / forever motion** — "particles loop endlessly," "logo rotates forever," "marquee on repeat." Any aliveness (the subtle jitter, a live SVG internal, a needed bounded ambient) is a **finite tween over the hold**, never `repeat` / `yoyo`.
- **No randomness or wall-clock** — no `Math.random` particle fields, no `Date.now` drift. Every render must be identical; name deterministic motion only (stagger and any variation derive from the element index).
- **Entrances use `fromTo`** — state the from-state explicitly so a seek to `t=0` lands the element correctly; never rely on a CSS-hidden start (it renders visible before the tween claims it, and flickers under seek).
- **No CSS `transition` / `@keyframes` for motion** — CSS animation runs on the browser clock, independent of the HF seek clock; it desyncs and flickers. Drive all motion inside the paused GSAP timeline.
- **Entrance + sequential reveal only — no mid-video exit.** The frame unmounts via the harness transition; that injected `transition_in` **is** the exit. Exit motion belongs only to the final frame. (Worker-built seam cuts in `cut-catalog.md` are within-frame, not the frame's exit.)

## Forbidden — the failure modes

**Slideshow (the primary failure):** everything dumped on screen in the first ~25%; content enters then freezes; nothing revealed on its VO cue. Fix with rule 2 (sequential reveal timed to the VO).

**Cheap aliveness:** circular breathing as "life"; a slow pan/push in the back half disrupting the eye; many elements floating independently as "motion." Fix with rule 3 (stillness + subtle jitter only).

**Bouncy:** `back.out` / `bounce.out` / `elastic.out` as the default entrance; hand-keyed overshoot. Fix with rule 1 (`power3` long-tail; overshoot only when explicitly playful).

**Always:** no `repeat` / `yoyo`; no `Math.random` / `Date.now`; no all-elements-entering-simultaneously (sequence or stagger).

## Naming motion in a shot — example

> Scene 1 (0.0–1.0s): solid field; hero headline enters via **per-word staggered reveal** (`dynamic-content-sequencing`) on a smooth long-tail settle (`power3`); slow **push** on the root (`multi-phase-camera`) holds steady — no back-half re-push.
> Scene 2 (1.0–3.0s): as the VO names each changed file, five file chips reveal **sequentially** via **cluster→outward expansion** (`center-outward-expansion`), then a **value-scaled counter** (`counting-dynamic-scale`) ticks the +/− line total up beneath them — the back-half reveal, timed to the script, not dumped at t=0.
> Scene 3 (3.0–4.2s): hold on the result; **keyword glow** (`asr-keyword-glow`) lands on the payoff word as the VO says it; settles and holds still — at most **subtle jitter** (`sine-wave-loop`, low amplitude) keeps it alive; no breathing, no drift.

Name the move + its rule id (or `cut-catalog.md` for a seam cut) per scene; let the worker pick curves, ms, and stagger — defaulting to `power3`.
