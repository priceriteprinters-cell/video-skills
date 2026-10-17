

<!-- ===== FILE: hyperframes/product-launch-video/GUIDE.md ===== -->

---
name: product-launch-video
description: "Turn a product or marketing URL, pasted script, or brief into a product launch / promo video — SaaS promos, feature reveals, product demos, app and company launches. Use when the user wants to market, launch, promote, or reveal a product; the default for any commercial URL. Site tours / showcases of a website route here too — the brief carries the show-it-as-is intent. Unclear → /hyperframes."
---

**Plugin installs:** Before setup or freshness commands, follow [plugin execution rules](../hyperframes/references/plugin-installation.md) when this skill is inside a HyperFrames plugin. Standalone installs keep the update instructions below.

> **First, keep this skill fresh — confirm with the user before running:** `npx hyperframes skills update product-launch-video`. A fast no-op when everything is current; otherwise it refreshes this skill plus the core domain skills it depends on before you rely on them.

> **media-use**: Before sourcing audio/images/logos, call `/media-use` to resolve BGM/SFX/images from the HeyGen catalog and brand logos from their official sources. Run `--adopt` first to register existing assets. See `/media-use` skill. When the host app provides its own music or sound-effect tools, use those for music and sound effects.

> **figma source**: If the source is a figma.com URL, run `/figma` first — asset export, brand tokens, and components/storyboard reconstruction if needed — then build this workflow from its output. Don't drive Figma via raw MCP tools directly: that skips SVG sanitization, `.media/manifest.jsonl` provenance, and brand-token `var()` binding, so a later brand change can't propagate without a full re-import.

# Product Launch to HyperFrames

Use this skill to capture a product, understand its brand, plan a launch video, and build it frame by frame in HyperFrames.

> **The front door is `/hyperframes`.** You are the orchestrator. Run each step, verify its gate, and only then continue to the next step. This skill is for a **product being marketed, launched, promoted, or revealed**, including requests such as "promo for our site" when the purpose is promotional. A site tour / showcase ask stays here too: `BRIEF.md` carries the show-it-as-is intent, and the captured screens become the assets the video features. Any other intent, a bare "make a video", or any uncertainty → read `/hyperframes` first — the intent layer owns every route decision, and a fresh creation arriving here without `BRIEF.md` goes through it anyway (Setup's opening rule).

You are the orchestrator. Work in `videos/<project>/`. Run steps in order and pass each gate before continuing. User-gated steps are Step 0, Step 3, and Step 6. Read `../hyperframes/references/brief-contract.md` before Step 0 — it defines the gate types and how `BRIEF.md`'s `flow`/`storyboard` derive the mode that governs the Step 3/4/6 gates. Do every step yourself except Step 5, where you dispatch one sub-agent per frame. Do not put design or motion rules here; those live in the frame-worker sub-agent, this skill's local `../hyperframes-animation/rules/` + `../hyperframes-animation/blueprints/`, and `hyperframes-creative`.

Workflow: Step 0 setup -> `hyperframes.json`; Step 1 capture -> `capture/`; Step 2 design system -> `frame.md`; Step 3 storyboard/script -> `STORYBOARD.md` and `SCRIPT.md`; Step 3.1 audio -> `audio_meta.json`; Step 4 visual design -> enriched `STORYBOARD.md`; Step 5 frames -> `compositions/frames/NN-*.html` and `index.html`; Step 6 final render -> `renders/video.mp4`.

---

## Step 0: Setup

Goal: Enter with a confirmed brief, create the HyperFrames project, and make the brief durable.

**The brief is confirmed by the intent layer, not by questions asked here.** Opening rule, in order: **(1)** `BRIEF.md` exists → read it and ask nothing — the brief is settled, and its `flow`/`storyboard` derive the mode (brief contract § 1). **(2)** No `BRIEF.md` but the project exists (`hyperframes.json` / `STORYBOARD.md` on disk) → resume from the storyboard's frontmatter and the recorded preferences; never re-interrogate a half-built project. **(3)** Neither — a fresh creation request that arrived here directly → read `/hyperframes` and run its intent layer (`references/intent-interview.md`): it checks recipes and remembered defaults, conducts this route's questions (`../hyperframes/references/routes/product-launch-video.md`), and hands back the locked brief. Edit requests skip all of this — go do the edit.

Initialize only if `hyperframes.json` is missing. Name `<project>` from the brand or domain in kebab-case, such as `acme-promo`; never use workspace name or timestamp.

`npx hyperframes init "videos/<project>" --non-interactive --example=blank --skill=product-launch-video` — `init` checks the installed skills against the latest on GitHub and updates the global set if any are out of date.

After init, let `<PROJECT_ROOT>` be `videos/<project>` and run every subsequent relative-path command with that directory as its working directory. In the commands below, `.` means `<PROJECT_ROOT>`; never write `.media`, `capture`, or output files in the caller directory.

**Write `BRIEF.md` immediately after init** (never before — `init` refuses a non-empty directory): the intent layer's locked brief, shape per `../hyperframes/references/brief-format.md`. Resolve `<MEDIA_DIR>` as the installed `/media-use` skill directory. Then record each preference-backed answer with `node <MEDIA_DIR>/scripts/prefs.mjs record --hyperframes .` (`brief-format.md` names the subset). If the intent layer adopted a recipe, run `node <MEDIA_DIR>/scripts/recipe.mjs use --hyperframes . --name <name>`; it copies its `frame.md` into the project (Step 2 is then skipped) and returns the skeletons Step 3 drafts from. A recipe fills answers, not approvals; the review gates still run.

**Show sign-in status before proceeding past Setup** — run `npx hyperframes auth status` and relay its output verbatim. It reports whether voice/BGM will use HeyGen or local engines and, when signed out, how to sign in. Note the exit code contract: `auth status` **exits 1 when not signed in** (and when the stored credential is rejected) — that non-zero exit is the normal signed-out state, not a command failure, so don't treat it as an error, don't retry it, and don't chain it with `&&`/`set -e` in a way that would abort the workflow. Apply one branch:

- **Collaborative:** wait for the user to sign in or explicitly choose `offline` / `go`.
- **Autonomous:** state the status and continue through the available local engines.

Do not silently omit a required capability when no offline provider exists; surface the blocker. Do not fold this decision into another question or write keys into a per-repo `.env`. Auth ownership and offline fallbacks: `/media-use` `references/setup-providers.md` § Providers.

**Gate:** `hyperframes.json` and `BRIEF.md` exist; the preference-backed answers were recorded (brief contract § 2); sign-in status was shown (signed in, or continuing offline).

---

## Step 1: Capture assets

Goal: Collect the source material, brand signals, and usable assets for the video.

Classify the input and choose the path. Explicit URL -> capture it and use the site for narration and assets. Pasted script/brief -> save verbatim as `user_script.txt`; `VO_MODE` (verbatim or restructured) comes from `BRIEF.md` — the intent layer asks it when a script arrives (ask once here only if the brief somehow lacks it). Then resolve capture target: URL in text -> use it; brand name only -> `WebSearch`, confirm URL in one line, then crawl; no URL/site (or the brief says don't scrape) -> no-capture path.

Run capture with: `npx hyperframes capture "<URL>" -o ./capture --json`. Keep the default
post-navigation budget unless the caller owns a smaller deadline; then pass a positive
`--capture-budget <milliseconds>` that leaves time for downstream work. `--timeout` controls page
navigation only. Use `--skip-vision` only when optional image captioning is intentionally disabled.

Inspect the command result and output directory immediately. A non-zero exit, JSON `ok: false`, or
`capture/BLOCKED.md` is a **hard stop** for the capture path: report the recorded reason and do not
consume partial screenshots, DOM, tokens, or assets. Do not manufacture a synthetic no-capture
fallback after a failed URL capture. Continue through the no-capture path only when the original
brief supplied the source material, or when the user explicitly switches to a provided screenshot
or brief after the failure.

Warnings such as `very little text content` together with an empty asset catalog are not proof of a
usable page. For a site tour or show-it-as-is brief, require trustworthy captured structure or a
provided screenshot; if neither exists, stop. Do not invent or rebuild the page merely because the
capture is unusable.

For a site tour or show-it-as-is brief, the captured page is the visual source of truth. Use the real screenshot instead of rebuilding the full website in HTML. If the shot needs internal movement, keep the screenshot as the base and overlay real captured assets at measured positions, or rebuild only the one component that moves. For a scroll shot, animate the viewport over `capture/screenshots/full-page.png` — the 1x plate of the whole document, pixel-exact for a 1920-wide viewport travelling down it. It is absent when the page was too tall to capture in one piece; fall back to the overlapping scroll-position shots in the same directory. Pushing in past 1:1 wants its own 2x capture of that region instead, since the plate has no headroom above 1x. Recreate the whole page only when the user explicitly asks for a stylized interpretation; an unusable capture alone is not authorization.

If `GEMINI_API_KEY`, `GOOGLE_API_KEY`, or an OpenRouter key exists, capture auto-captions assets into `capture/extracted/asset-descriptions.md`. This is not a review gate. Without a vision key, use DOM context and continue.

No-capture path: create `capture/extracted/tokens.json`, `capture/extracted/visible-text.txt`, `capture/extracted/asset-descriptions.md`, and `capture/assets/` by hand. `tokens.json` should be `{ "title": "", "description": "", "colors": [], "fonts": [] }`; fill title/description from the brief when possible. `visible-text.txt` contains the full brief or script. `asset-descriptions.md` should say no assets were captured unless the user gave asset notes.

**Gate:** capture JSON reported `ok: true`; `capture/BLOCKED.md` does not exist;
`capture/extracted/tokens.json`, `capture/extracted/visible-text.txt`,
`capture/extracted/asset-descriptions.md`, and `capture/assets/` exist; and you can state the brand in
one clear sentence. Treat `asset-descriptions.md` as the main asset inventory. If it is missing after
real capture, stop and report capture incomplete. Warnings about a degraded optional phase are
acceptable only when this structural gate still passes.

---

## Step 2: Design System

Goal: Choose one shipped frame preset; a script turns it into this video's `frame.md` + caption skin.

When `BRIEF.md` names a `style_preset` — the user picked it by eye from the showcases at the intent layer — use it; the judgment call is yours only when the brief is silent. Then you make the one call — **which preset**: read `../hyperframes-creative/references/design-spec.md` and pick the preset whose look best fits the brand and brief. Then run:

```bash
node <SKILL_DIR>/scripts/build-frame.mjs --preset <name> --hyperframes .
```

The script does the rest deterministically: copies the preset's `FRAME.md` → `frame.md` and **remixes** it onto the brand tokens in `capture/extracted/tokens.json` (brand colors mapped onto the preset's color keys by role — ink, canvas, accents — keeping keys/structure/components; the preset's display + body fonts swapped for the brand's), copies the preset's caption skin to `.hyperframes/caption-skin.html`, and self-validates (exits 1 on a broken mapping). Proceed to the next step as soon as it exits 0 — no hand-editing of the spec.

`tokens.json` with no brand colors/fonts (e.g. no capture) → the script keeps the preset's own palette, a complete shippable design. If the brief names brand colors/fonts the capture missed, add them to `capture/extracted/tokens.json` before running (or use the user's `design.md` to populate it); only adjust `frame.md` by hand afterward if a mapping truly needs it.

**Gate:** `build-frame.mjs` exited 0 — `frame.md` exists from a named preset, and (when the preset ships one) `.hyperframes/caption-skin.html` exists as the caption skin source; the chosen preset was recorded as a preference (`--key style_preset --workflow <this workflow>`, brief contract § 2).

---

## Step 3: Storyboard and Script

Goal: Turn the brief and captured material into an approved frame-by-frame story plan.

Read `../hyperframes-creative/references/story-spine.md` (hook language, value-before-evidence, storyboard-as-proposal, source-traceable visuals), `references/story-design.md`, `../hyperframes-animation/blueprints-index.md`, `../hyperframes/references/storyboard-format.md`, and `../hyperframes/references/script-format.md`. Use them to write `STORYBOARD.md` and, when narration is needed, `SCRIPT.md`. Set the frontmatter `duration:` from the brief's `length` — a rough expectation; assembly reports where the cut lands against it.

Use `story-design.md` for story blueprint, hook, persuasion logic, beats, `VO_MODE`, and asset choices. As a **soft guide**, consult the role→blueprint menu in `../hyperframes-animation/blueprints-index.md`: for each beat, note a candidate blueprint id when one fits. Story truth still decides which beats exist — never force a beat to fit a blueprint, and never invent a beat just because a proven shape is available. Choose each visual frame's `asset_candidates` from `capture/extracted/asset-descriptions.md` (the canonical inventory) — don't browse raw `capture/assets/`. Do not ask the user to pick assets unless that inventory is missing or unusable. Use the exact required fields from the storyboard and script references.

After drafting, run the review loop's plan pass — `../hyperframes/references/review-loop.md` § 1: present the plan as a proposal, and ask the two questions — approve or change, and **sketches first** (recommended) or skip. Feedback arrives as a chat reply; loop until approved. This is a **checkpoint gate** (brief contract § 1): in autonomous mode there is nothing to ask — post the same summary as a heads-up and proceed; sketches collapse into the build, and the final preview with its one question comes at Step 6.

**Gate:** `STORYBOARD.md` exists, every visual frame has `asset_candidates`, `SCRIPT.md` exists when narration is needed, and the user approved the frame-by-frame plan (autonomous: the summary was posted as a heads-up).

---

## Step 3.1: Audio

Goal: Generate narration, word timings, music, and audio metadata from the approved script.

Start audio after Step 3 approval. Run it in the background, then continue to Step 4.

**Choose the narration provider and voice from the user's ask before invoking.** Pass the provider selected in Step 0 with `--provider <provider>` (or set `HF_TTS_PROVIDER`). If the request named a voice, gender, or tone, pick a matching voice id and pass it with `--voice <id>`. The pipeline default is otherwise **Marcia (female)** on HeyGen / `am_michael` on Kokoro — so a request like "a male voice" is silently ignored unless you pass the flag. Voice ids are provider-specific; resolve against whichever provider Step 0's sign-in status selected: **HeyGen** (signed in) via `node <MEDIA_DIR>/audio/scripts/heygen-tts.mjs --list` (or `GET /v3/voices?engine=starfish`); **Kokoro** (offline) via the voice table in `<MEDIA_DIR>/audio/references/tts.md` (prefixes `am_`/`bm_` male, `af_`/`bf_` female). When the user expressed no preference, fall back to the remembered voice (brief contract § 2) before the pipeline default, and say which one you used; omit `--voice` only when neither names one. When the user explicitly picked a voice this run, record it (`prefs.mjs record --key voice`).

`node <SKILL_DIR>/scripts/audio.mjs --script ./SCRIPT.md --storyboard ./STORYBOARD.md --hyperframes . --out ./audio_meta.json --provider <provider> --voice <voice-id> &`

The audio script handles narration, word timings, BGM lookup from HeyGen's music library, and timing metadata. BGM mood comes from the storyboard's `music:` field; **`music: none` turns BGM off**. This uses the HeyGen Audio API for retrieval, not generation, and uses the same `~/.heygen` credential as TTS. For provider details, read `../media-use/audio/references/tts.md`. When the host app's own tools make the music or a sound effect, put the file under assets/ and list it in the audio_meta.json file marked `"source": "host"`: music as `bgm` `{ "path": "assets/…", "source": "host" }` with `music: none` in the storyboard; a sound as an `sfx` entry `{ "frame": <n>, "file": "assets/…", "offset_s": 0, "duration_s": <its length>, "source": "host" }`. Every audio pass keeps these, and a frame with a host sound gets no looked-up cue.

If there is no narration and no `SCRIPT.md`, skip voice generation. BGM may still run if the storyboard has a music mood.

**The canonical fully-silent marker:** `music: none` in the STORYBOARD.md top YAML block, no `SCRIPT.md`, **and** no `sfx:` cues or host audio. That combination marks the project silent — no narration, no BGM, no SFX. `audio.mjs` recognizes it and generates nothing (it removes any stale `audio_meta.json`; an absent `audio_meta.json` is what assemble treats as silent), so Step 3.1 is a clean skip. Without narration but with `sfx:` cues or host audio the film is not silent: `audio.mjs` writes the audio_meta.json file for `fetch-sfx` to fill. Use it when the user asks for a silent / music-free video — don't improvise other spellings.

**Gate:** audio job has started, or the project is marked silent (`music: none`, no `SCRIPT.md`, no `sfx:` cues or host audio).

---

## Step 4: Frame Visual Design

Goal: Add the visual direction, layout intent, and motion choices to each storyboard frame.

**Sketch the storyboard sheet first (collaborative only).** The moment the plan is approved, run the sketch pass — `../hyperframes/references/review-loop.md` § 2 (don't wait on Step 3.1; the stills don't use timings): pose every frame yourself in its composition, mount each in `index.html` at its planned start, snapshot all the stills in one run and write the board, `boards/storyboard.html` (`../hyperframes-creative/references/storyboard-recipe.md`), mark each `built`, pause for the one layout question when every frame is `built`, and revise only the frames named until the board is confirmed. Stand-ins: plain labeled blocks for the captured assets — the real files arrive with Step 5's workers. Only then write the visual design below onto the confirmed layouts. In autonomous mode, or when the user chose to skip sketches at Step 3, skip this pass — frames go straight from `outline` to `animated` at Step 5.

Edit `STORYBOARD.md` in place. Do not create another storyboard. Use `frame.md` as source of truth for color, type, layout feel, and style.

Read `references/visual-design.md`, `../hyperframes-animation/blueprints-index.md`, `references/motion-language.md`, and `../hyperframes-animation/rules-index.md`. Use `visual-design.md` for the method (the time-coded shot sequence, the inline Layout vocabulary, and the required `## Video direction` block). Use `../hyperframes-animation/blueprints-index.md` to pick each frame's shot shape. Use `motion-language.md` (the motion vocabulary + the motion doctrine) and `../hyperframes-animation/rules-index.md` (valid rule names) for motion — do not invent motion names.

**Search the live catalog before you design any named look.** For every look, effect, treatment or transition the brief names — "CRT scanlines", "glitch", "film grain", "shimmer sweep", "confetti burst" — run `npx hyperframes catalog --query "<the look, in plain English>" --json` and read the top results BEFORE you write that look into `STORYBOARD.md`. The search needs **nothing installed**: no project, no prior `add`, no account. It ranks the whole hosted registry (~400 blocks and components) from any directory. A block that already does the job becomes the frame's `focal` — name it here; Step 5 pre-installs it once before dispatch, and its worker customizes it instead of rebuilding it. Hand-author a look only after a search for it came back with nothing that fits.

For every visual frame, write a **time-coded shot sequence** into `STORYBOARD.md` per `visual-design.md`'s method: pick the frame's blueprint (or compose), instantiate it with THIS product's content, and pace each Scene's reveal to the voiceover so the frame develops across its full duration instead of front-loading then freezing. State layout and motion **inline** per Scene (vocabularies in `visual-design.md` and `motion-language.md`). Add one video-wide `## Video direction` block.

When an element visibly continues across a frame boundary, give both workers the same numerical handoff in `STORYBOARD.md`: add `handoff_out:` to the outgoing frame and a matching `handoff_in:` to the incoming frame. Name the element and its exact x/y position, scale, opacity, and motion direction/speed at the cut — state every field even when it does not change, because a constant is `opacity: 1`, not an omission. Omit the whole block only for a deliberate clean cut. The goal is simple: parallel workers must not invent two different versions of the same seam.

Do not change story, script, asset choices, `asset_candidates`, `transition_in`, or captured source material. Do not write HTML in this step beyond the sketch pass's poses.

Stage named assets after visual design is locked:

`node <SKILL_DIR>/scripts/stage-assets.mjs --storyboard ./STORYBOARD.md --hyperframes .`

**Gate:** every visual frame has a time-coded shot sequence whose reveals are paced to the voiceover (no front-loading); `## Video direction` exists; `assets/` contains the named assets. Collaborative: the sketch sheet was confirmed.

---

## Step 5: Build Frames

Goal: Build every storyboard frame as an HTML composition and assemble the playable video.

Wait for Step 3.1 audio to finish if audio was started. Then sync durations and fetch SFX; skip both if silent.

`node <SKILL_DIR>/scripts/audio.mjs sync-durations --audio-meta ./audio_meta.json --storyboard ./STORYBOARD.md`

`node <SKILL_DIR>/scripts/audio.mjs fetch-sfx --storyboard ./STORYBOARD.md --hyperframes .`

Duration sync is mechanical: real voice duration wins; silent frames keep estimates; never hand-edit synced durations.

Check the music against the final cut before assembly. A library track can match the requested mood but open on a quiet build that drains the first seconds of a short launch video. Compare the opening with later five-second sections; when a later section has a stronger, musically clean start, trim from there and keep a short fade-in plus a longer fade-out. If frame or narration timing changes, redo this check against the new final duration so the music never ends early or leaves silence at the tail.

**Pre-install the registry blocks** named across `STORYBOARD.md` once, before dispatch, so parallel workers don't race on the registry:

`for b in <each registry block named in the storyboard>; do npx hyperframes add "$b"; done`

Before dispatch, read `../hyperframes/references/subagent-dispatch.md`. Build the per-frame packets and the worker role payload:

`node <SKILL_DIR>/scripts/frame-packets.mjs --project "$PROJECT_DIR" --storyboard "$PROJECT_DIR/STORYBOARD.md"`

The builder writes one bounded packet per frame under `.hyperframes/frame-packets/` (the frame's exact storyboard block + the blueprint body + every cited rule recipe, inlined) and `_role.md` (`../hyperframes/references/frame-worker-core.md` + this skill's `sub-agents/frame-worker.md`, concatenated verbatim — the complete worker role). Dispatch one sub-agent per frame, in parallel if possible; otherwise run workers in waves. Each worker gets exactly one frame: its prompt carries `_role.md` and that frame's packet — paste both in full, or hand the two file paths for the worker to read first (equivalent; the worker starts from exactly those two documents either way) — plus a dispatch context with `PROJECT_DIR`, `frame_id`, whether the frame has a **confirmed sketch** on disk (the worker dresses that layout rather than redrawing it — frame-worker core § When a confirmed sketch exists), canvas size, and caption status + keep-out band if captions are enabled.

Workers read only their packet and `frame.md`; they never open `STORYBOARD.md` or the skill documents (the packet inlines what was selected upstream). Each worker writes only `compositions/frames/NN-*.html`. Workers must never edit `STORYBOARD.md`.

**Full-bleed backgrounds ride on a `class="clip"` layer, never the `#root`.** A frame's ground (color field / gradient / grid) is its own full-duration background clip — a `background` set on the `#root` / `data-composition-id` element is clip-gated to the frame's window and is not a dependable ground, so dark content can land on the black host `body` and render invisible. The video's base ground is painted by the assembler from `frame.md`'s `canvas` color onto the index `#root`. (Full rule + self-check: `../hyperframes/references/frame-worker-core.md`.)

As each worker returns, the orchestrator marks that frame as `animated` in `STORYBOARD.md`.

After audio timings exist, build captions in the background and assemble the index:

`node <SKILL_DIR>/scripts/captions.mjs build --storyboard ./STORYBOARD.md --audio-meta ./audio_meta.json --hyperframes . --out ./caption_groups.json &`

`node <SKILL_DIR>/scripts/assemble-index.mjs --storyboard ./STORYBOARD.md --hyperframes .`

`captions.mjs` uses the project's `.hyperframes/caption-skin.html` (copied in Step 2) as the caption look, injecting brand tokens from `frame.md`; with no skin present it renders the built-in default pill. `captions: skipped (<reason>)` is valid. Continue without captions when explicitly skipped.

**Gate:** every frame is marked `animated` (collaborative: the sketch sheet was confirmed at Step 4), `index.html` exists, and captions are built or explicitly skipped.

---

## Step 6: Finalize

Goal: Verify the assembled video, get user approval, and render the final MP4.

Inject transitions, run checks, pause for review, then render.

`node <SKILL_DIR>/scripts/transitions.mjs inject --storyboard ./STORYBOARD.md --hyperframes .`

`node <SKILL_DIR>/scripts/transitions.mjs verify --storyboard ./STORYBOARD.md --index ./index.html`

**When a music bed plays under any voice track, carve the bed after assembly and transition injection, before checks.** The assembler's `data-volume` (0.12 by default under voice) is a fixed whole-bed gain, not the required spectral carve; the carve leaves it in place, so both apply. Read `/hyperframes-audio` → Voiceover carve.

The assembler emits separate narration clips without an audio group. Before carving, add `data-audio-group="voiceover"` to each narration `<audio id="el-<frame_id>-voice">` in `index.html`, including any other voice clips that should join the same narration group. Keep the music bed and SFX outside that group. Multiple voice clips must be carved against their voice group, so later clips remain covered when the analysis is rerun. Then run from the composition project:

`node <HYPERFRAMES_AUDIO_SKILL_DIR>/scripts/carve.mjs --comp ./index.html`

`<HYPERFRAMES_AUDIO_SKILL_DIR>` is the installed `hyperframes-audio` skill directory. The script needs `ffmpeg` on PATH and `@hyperframes/core` installed in the composition project (`npm i -D @hyperframes/core`, or `bun add -D @hyperframes/core` in a Bun project). It detects the bed and overlapping voice tracks; use `--bed el-bgm` and repeat `--voice <voice-element-id>` when detection needs an explicit choice. Confirm the bed carries `data-fx-carve`, `data-fx-chain`, and `data-automation`; when multiple narration clips overlap the bed, `data-fx-carve.sources` should name the `voiceover` group, not individual clip ids. Skip this step only when no music plays under voice. Reassembling replaces `index.html`, so restore the narration group and rerun the carve after any reassembly.

`npx hyperframes lint`

`npx hyperframes check`

`npx hyperframes snapshot --at <frame-midpoints-and-each-cut-minus-0.1s-and-plus-0.2s>`

`snapshot` stitches the captured frames into one contact sheet (`.hyperframes/artifacts/snapshots/<id>/contact-sheet.jpg`; the command prints the path). Inspect the midpoint frames for layout failures, then compare the two images around every cut. A continuing element must keep the promised position, scale, opacity, and direction; fix any visible pop before rendering.

If a command fails, surface stderr and stop — don't pile on recovery commands. Fix it yourself: the cheapest safe edit to `compositions/frames/NN-*.html`, then rerun the failed check.

After checks pass, pause for user review — the review loop's final look (`../hyperframes/references/review-loop.md` § 4): one question, on the final Studio preview — render now, or what changes? (Autonomous: the same, as the one kept question — open the preview even though the user didn't ask for one.) Then deliver the MP4 with the contact sheet and the frame ids so revisions can target a single frame.

Preview: `npx hyperframes preview --background`

Render only after user approval (autonomous mode: after the render-or-changes question):

`npx hyperframes render --skill=product-launch-video --quality high --output renders/video.mp4`

Do not rerun `lint`, `check`, or `snapshot` after rendering unless the user asks.

**Gate:** `lint` and `check` passed and the snapshots were inspected before render; user approved at the review pause (autonomous: checks passed and the delivery includes the contact sheet); `renders/video.mp4` exists. Final reply states MP4 path and final duration.

---

## Quick Reference

**Formats:** landscape `1920x1080`; portrait `1080x1920`; square `1080x1080` — derived from the destination (brief contract § 2). Set the format once in the storyboard frontmatter.

**Background scripts:** the workflow ships only these scripts under `scripts/`: `build-frame` for adopting + brand-remixing a frame preset into `frame.md` (+ caption skin); `audio` for TTS, transcription, BGM, SFX, and duration syncing; `captions`; `transitions` for inject and verify; `stage-assets` for copying frame-named assets into `assets/`; and `assemble-index`. Everything else is handled by the `hyperframes` CLI.

The reusable, product-agnostic shot shapes live in `../hyperframes-animation/blueprints/` (indexed by `../hyperframes-animation/blueprints-index.md`).

| Read                                                                                                                                                        | When                                                                                                     |
| ----------------------------------------------------------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------- |
| `[../hyperframes/references/brief-contract.md](../hyperframes/references/brief-contract.md)`                                                                | Gate types, mode derivation from `BRIEF.md`, field semantics.                                            |
| `[../hyperframes-creative/references/story-spine.md](../hyperframes-creative/references/story-spine.md)`                                                    | Step 3: story doctrine — hook language, value-before-evidence, proposal shape, source-traceable visuals. |
| `[../hyperframes-creative/frame-presets/](../hyperframes-creative/frame-presets/)`                                                                          | Step 2: choose and adopt a frame preset.                                                                 |
| `[../hyperframes-creative/references/design-spec.md](../hyperframes-creative/references/design-spec.md)`                                                    | Step 2: apply brand tokens correctly.                                                                    |
| `[references/story-design.md](references/story-design.md)`                                                                                                  | Step 3: plan the product-launch story.                                                                   |
| `[../hyperframes-animation/blueprints-index.md](../hyperframes-animation/blueprints-index.md)`                                                              | Step 3: role→blueprint menu. Step 4: pick the shot shape.                                                |
| `[../hyperframes/references/storyboard-format.md](../hyperframes/references/storyboard-format.md)`                                                          | Step 3: write `STORYBOARD.md`.                                                                           |
| `[../hyperframes/references/script-format.md](../hyperframes/references/script-format.md)`                                                                  | Step 3: write `SCRIPT.md`.                                                                               |
| `[../media-use/audio/references/tts.md](../media-use/audio/references/tts.md)`                                                                              | Step 3.1: choose or understand TTS providers and voices.                                                 |
| `[references/visual-design.md](references/visual-design.md)`                                                                                                | Step 4: write the frame's shot sequence (+ Layout vocabulary).                                           |
| `[references/motion-language.md](references/motion-language.md)`                                                                                            | Step 4: the motion vocabulary + the motion doctrine.                                                     |
| `[references/cut-catalog.md](references/cut-catalog.md)`                                                                                                    | Step 4-5: the cut catalog (worker builds within-frame seams).                                            |
| `[../hyperframes-animation/rules-index.md](../hyperframes-animation/rules-index.md)` + `[../hyperframes-animation/rules/](../hyperframes-animation/rules/)` | Step 5: local rule recipe bodies for the cited motions.                                                  |
| `[../hyperframes/references/frame-worker-core.md](../hyperframes/references/frame-worker-core.md)`                                                          | Step 5: the shared worker contract (packet builder prepends it to the delta).                            |
| `[sub-agents/frame-worker.md](sub-agents/frame-worker.md)`                                                                                                  | Step 5: the workflow's frame-worker delta.                                                               |
| `[../hyperframes/references/subagent-dispatch.md](../hyperframes/references/subagent-dispatch.md)`                                                          | Step 5: dispatch sub-agents safely.                                                                      |


<!-- ===== FILE: hyperframes/product-launch-video/references/cut-catalog.md ===== -->

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

| Subject                                                | Peak blur   | Why                                                                                                                                                                                                                                                 |
| ------------------------------------------------------ | ----------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Text-scale (headline, line, word group)                | **10px**    | At 20px text smears into illegibility — the eye loses the word it was tracking and the cut reads as a glitch, not speed. (Learned 2026-06-10: the until-now inverse zooms shipped at 20px and read mushy; 10px keeps letterforms readable mid-cut.) |
| Full-frame surface (terminal window, card, screenshot) | **18–20px** | Big surfaces have edges and texture that survive heavy blur; lighter blur on a full-frame move reads as a rendering hiccup instead of motion.                                                                                                       |

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

Shipped examples: `boring → until-now` and `B3 → "That changes today."` (sfx-music-launch);
seams 3/4 in editorial-paper (`follow-up → thinking`, `thinking → compose UI`).

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

Shipped example: `until-now.html` B1→B2→B3 (sfx-music-launch).

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


<!-- ===== FILE: hyperframes/product-launch-video/references/motion-language.md ===== -->

# Motion language — the move vocabulary + the motion doctrine + the seek-safe core

> The motion layer for **Step 4 (Visual design)**. When you write a frame's **time-coded shot sequence**, you name each scene's move **inline from the vocabulary below** — a named palette of the moves the golden corpus actually uses. Each move carries the **backing rule id** in this skill's local `../../hyperframes-animation/rules/`; cite that id so the move resolves to a real recipe when a **frame worker** implements it in Step 5 (the worker reads the rule body in `../../hyperframes-animation/rules/<id>.md` — it reproduces the move, it does not guess from the name). You name motion by **role / move name**, never by raw GSAP curve, ms, or stagger formula — the worker maps the curve. Between-frame **transitions are not yours**: story names `transition_in`, the harness injects it; that injected transition **is** the frame's exit. For cuts a worker builds INSIDE a frame (within-scene swaps, scene-to-scene seams), see the catalog in `cut-catalog.md`.

A good promo feels like one continuous film — one camera, one motion feel, **smooth and timed to the voiceover** — not a pile of slides that animate once and freeze. The doctrine in Part 2 is load-bearing: when in doubt, do what it says.

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

These four rules are the difference between a clip that reads as a serious launch video and one that reads as an agent-made PowerPoint. Follow them as written.

## 1. Smooth beats bouncy — `power3` is the default

Elements should use **long-tail decel curves that let them settle smoothly. `power3` is enough in most cases.** No bouncy, no overshoot, no `back.out` / `bounce.out` / `elastic.out` as a default.

Bouncy is the **#1 instant turn-off** in user-made Remotion / HyperFrames videos, and the agent almost never gets it right — it thinks bouncy adds emphasis, but it buys that emphasis at the cost of cleanliness. The serious launch-video shops feel the same. **Smooth always wins.** Overshoot is demoted to a **rare, explicitly-playful exception** (a consumer/fun logo slam, a deliberate bell-hit) — never the house style. Name the intent as a long-tail settle; the worker maps `power3` (or `expo.out` on a fast arrival). See `../../hyperframes-animation/rules/spring-pop-entrance.md` — it now leads with the smooth settle. (The exact form of that settle is a critically-damped spring; the worker has a baked, seek-safe `springEase` — ζ=1 — in `../../hyperframes-animation/adapters/gsap-easing-and-stagger.md` → Spring Eases for when the settle is the hero. Real physics, same doctrine — not a license for bounce.)

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

The fix for both is the same: **stagger element reveals in time with the script** (rule 2). And the governing principle: **"I'd rather have NO motion than BAD motion."** A held, still frame is better than a frame kept "alive" by breathing or a drifting camera. The **only sanctioned aliveness** during a hold is **subtle jitter** — a small low-amplitude jitter that keeps a frame from feeling dead without looking weak (it's in current video work now). Everything else holds.

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
> Scene 2 (1.0–3.0s): as the VO names each capability, five feature icons reveal **sequentially** via **cluster→outward expansion** (`center-outward-expansion`), then a **value-scaled counter** (`counting-dynamic-scale`) ticks up beneath them — the back-half reveal, timed to the script, not dumped at t=0.
> Scene 3 (3.0–4.2s): hold on the result; **keyword glow** (`asr-keyword-glow`) lands on the payoff word as the VO says it; settles and holds still — at most **subtle jitter** (`sine-wave-loop`, low amplitude) keeps it alive; no breathing, no drift.

Name the move + its rule id (or `cut-catalog.md` for a seam cut) per scene; let the worker pick curves, ms, and stagger — defaulting to `power3`.


<!-- ===== FILE: hyperframes/product-launch-video/references/story-design.md ===== -->

# Story design — product launch video

Step 3 of the product-launch flow. Output: `STORYBOARD.md` (the narrative plan, one frame per beat) and `SCRIPT.md` (the locked spoken narration).

This step decides **what the video says, in what order, and how each beat is said** — and it says each beat in the SHAPE of a proven script. It does not design layout, composition, or motion (that is Step 4). For exact file syntax follow `../../hyperframes/references/storyboard-format.md` and `../../hyperframes/references/script-format.md`.

## What story design produces

For every beat, four things:

1. **Position in the SEQUENCE** — the shot order. Story truth decides which beats exist and in what order (the arc).
2. **Voiceover written in a blueprint's script shape** — the spoken line, drafted to sound like the proven script for the shape this beat is reaching toward (see the script bank below).
3. **A candidate `blueprint:` id** — the proven shot SHAPE this beat leans toward (a tag, not a commitment; Step 4 confirms or overrides).
4. **`transition_in`** — how this beat enters from the one before it.

The big idea: **the blueprint is applied from the very first step.** The blueprints were reverse-engineered from 50 golden clips; each one implies a proven script. So we write the VO in that script's shape from the start — the voiceover is blueprint-shaped before Step 4 ever runs, which makes the blueprint's hit-rate downstream high.

This is still a SOFT discipline. Story truth comes first: **never invent, bend, drop, or reorder a beat to fit a blueprint.** The script patterns only shape HOW a beat is said and which proven shape it leans toward — they never decide which beats exist.

## Read first

1. `hyperframes.json` — locked brief: angle, length, aspect ratio, language.
2. `frame.md` — tone, mood, design system, brand register.
3. `capture/extracted/visible-text.txt` — product facts, page copy, positioning, proof, CTA.
4. `capture/extracted/asset-descriptions.md` — the ONLY source for the captured asset inventory.
5. `user_script.txt` and `VO_MODE`, when present.

Do not inspect `capture/assets/`, contact sheets, screenshots, or raw files in Step 3. Treat `asset-descriptions.md` as the canonical asset list. Never invent asset filenames.

## Method

### 1. Extract the product truth

From the brief and captured text, name:

- **Audience** — who the video speaks to.
- **Pain / desire** — what they already want fixed or achieved.
- **Promise** — the one-line thesis of the whole video.
- **Product role** — what the product does in the story.
- **Proof** — features, UI moments, metrics, logos, demos.
- **CTA** — what the viewer should do next.

Build the sequence around the **promise**, not a feature list. A website is an information layout; a video is an emotional sequence. Reorder, merge, and omit captured content freely — do not follow page order.

### 2. Choose the arc (the sequence backbone)

Pick ONE arc — it fixes the beat order. Compound only when useful (e.g. `PAS with feature-benefit progression`).

| Arc                       | Use when                                         | Beat order                                                                  |
| ------------------------- | ------------------------------------------------ | --------------------------------------------------------------------------- |
| `PAS`                     | Pain is known and urgent (broken B2B workflows). | hook → pain → agitation → solution tease → product intro → proof/demo → CTA |
| `Future Pacing`           | Sells a new future / category / paradigm.        | imagine → name product → remove pain → mechanism → outcome → CTA            |
| `Demo Loop`               | UI is self-explanatory; best shown working.      | question → product intro → demo cycle 1 → demo cycle 2 → trust → CTA        |
| `BAB`                     | Bridges an old workflow to a better one.         | before → after tease → bridge/product → step 1 → step 2 → wow → CTA         |
| `Feature-Benefit Cascade` | Feature-rich or desire/status-driven.            | category hook → feature → benefit → feature → benefit → climax → CTA        |

Use feature→benefit rhythm inside any arc when there are many capabilities — always translate a feature into viewer value, never stack raw features.

`frame.md` tunes the VOICE, not the arc: restrained/B2B → plain, low-hype; bold/launch → short, punchy; warm/human → friendly direct address; premium/cinematic → aspirational, fewer words.

### 3. Lay out the beats, each with a role

One clear job per beat — never "more benefits" or "another feature." Beat `type` (= blueprint **role**):

`hook | pain_point | product_intro | feature_showcase | benefit_highlight | social_proof | branding | cta`

The opening 3–5s needs ONE hook that creates tension, curiosity, or desire — a shocking stat, pain validation, a rhetorical question, direct address, an imagine/future-pace, a category announcement, or visual spectacle. Never open with generic company description. Per `../../hyperframes-creative/references/story-spine.md`: the hook speaks the viewer's outcome language (what they gain, never a feature list), and the promise (`message`) lands by beat 2 — features after that are its evidence.

A UI demo is usually a SEQUENCE of 3+ consecutive `feature_showcase` / `benefit_highlight` beats on the same surface (input → response → result → benefit), not one isolated frame.

### 4. Write each beat's VO in its blueprint's script shape

For each beat, look up its **role** in the script bank below, find the blueprint whose SHAPE fits the beat you already chose, and **draft the voiceover to sound like that blueprint's pattern.** Tag the candidate `blueprint:` id on the frame.

- The bank is the heart of this step: proven product-launch clips reversed into the one VO line each implies, grouped by role → blueprint, each with a **pattern** to imitate.
- If two blueprints fit the beat, prefer the one whose script shape matches the line you'd naturally write.
- If NO shape fits the beat, omit `blueprint:` and write the VO plainly — Step 4 composes that frame freely. Do not force a wrong shape.
- **Vary the shapes across the video.** Reaching for the same blueprint every beat re-creates the sameness this exists to avoid. `kinetic-type-beats` is the workhorse (6 roles) — lean on it, but not everywhere.
- **Write each VO as discrete cues, not one run-on breath.** Step 5 reveals each on-screen piece _when the voiceover names it_ (the anti-PowerPoint mechanism — `motion-language.md` Part 2). A line with clear phrase boundaries — "Content, sentiment, engagement — in one place" — hands the shot its reveal cadence for free; a single long clause leaves the frame nothing to pace to. The bank patterns are already cue-segmented — keep that rhythm.

Step 3 only TAGS the candidate id and writes the shaped VO. Step 4 (visual design) picks and instantiates the blueprint into a time-coded shot; it may override or drop a Step 3 candidate. The full menu with picking guidance lives in `../../hyperframes-animation/blueprints-index.md`.

---

## The script bank — what each beat's VO sounds like

> Proven product-launch clips, each reversed into the one spoken line it implies. Grouped by **role → blueprint**. Real product names kept (swap in your own). Draft your beat's VO in the SHAPE of the matching pattern. Kept 1:1 with the role declarations in `../../hyperframes-animation/blueprints-index.md` — when a blueprint gains a role there, add its script shape here.

### HOOK

**kinetic-type-beats** — the words ARE the motion

- Mailoji — "Still using a @gmail address? Or @outlook, or @hotmail, or @yahoo?"
- Outrank — "Getting traffic is hard. Insanely hard."
- AiAgent — "An AI agent that's easy to use — and optimised for you."
- Uizard — "Transform your sketches into prototypes — automatically."
- _Pattern:_ a punchy claim or rhetorical jab whose KEY WORD swaps in place (or escalates beat by beat) — the swap/escalation is the joke.

**typewriter-reveal** — someone is typing this

- "Need answers about your audience — right now?"
- Contra — "You are more than your job title. You are more than your resume."
- _Pattern:_ a relatable line typed live and edited mid-stream (a word backspaces and retypes) — the everyday thought, in your own words.

**spatial-pan-stations** — a panned timeline

- Rows — "From VisiCalc to Excel to Google Sheets — the spreadsheet has barely changed since 1979."
- _Pattern:_ a march of named milestones across time, landing on "...until now / ...up to us."

**constellation-hub** — nodes ring a center, camera pushes in

- "Content, sentiment, engagement, analysis — every platform you're on, in one place."
- _Pattern:_ a spread of tools/channels collapsing onto one center — "it connects everything."

**ticker-takeover** — options cycle, then a hero crashes in

- Notion — "A doc? A database? A wiki? — no, it's all of them, in one place."
- _Pattern:_ a "could be X, or Y, or Z?" cycle on one swapping word, then a hero claim crashes in and replaces it — "actually, this is what it is."

**prompt-type-submit-generate** — watch me ask

- "Build me a landing page for my coffee brand — dark, minimal, launch-ready."
- "What if you could just… ask?"
- _Pattern:_ the VO speaks (or frames) the ask itself while the prompt types live — the question is the whole hook; the answer stays off-screen, or a second ask starts before the cut.

**zoom-out-workspace-reveal** — the mystery re-scopes

- "This isn't a finished animation — it's your canvas."
- _Pattern:_ near-silence or one slow tease over the close-up mystery, with the landing line timed to the zoom-out — the words answer "what am I looking at?" exactly when the workspace does.

**fixed-anchor-cycle** — a roll-call around a pinned line

- "For founders, for designers, for marketers, for teams — for anyone who ships."
- _Pattern:_ one static claim holds while its audience/option list cycles fast beneath it — the list is the sentence's swapping object, and the brand line lands after the cycle clears.

**cursor-ui-demo** — a canvas already alive

- "Your whole team is already in here — designing, commenting, shipping."
- _Pattern:_ a "we're all here working" line over an ambient multi-cursor canvas — presence, not features; the live activity is the proof.

**dataviz-countup** — cold-open on one exploding stat

- "One million users. Ninety days."
- _Pattern:_ ONE statistic counts up as the VO speaks it — scale alone carries the tension; no product, no context yet.

**cta-morph-press** — a lone widget does its trick

- "It starts as a search bar. It becomes your whole workflow."
- _Pattern:_ one small widget on a bare field morphs in place and performs its payload while the VO names the transformation — small thing, big claim, hand off to the title.

### PROBLEM

**kinetic-type-beats** — pain lands alone on a bare canvas

- Butter — "What if your sessions didn't have to be boring and unstructured — or buried under a dozen tabs?"
- SmartCue — "You asked for better leads. We were the cure — MQLs that actually convert, a sales team that becomes your ally."
- _Pattern:_ 3–5 short pain statements (or a "what if?" framing), each landing solo before the next — no product yet.

**spatial-pan-stations** — a panned web of pain

- Vauban — "Coordinating legal documents, signatures, and cross-border transactions — it's a tangled mess."
- _Pattern:_ pain "stations" traversed one by one, ending on a knot — "too many disconnected steps."

**dataviz-countup** — the data IS the argument

- "67% of professionals say leadership is disconnected — and it's costing them a 65% boost in profitability."
- _Pattern:_ a count-up / chart / stat the camera pushes through to dramatize a worsening or large-scale problem.

**overwhelm-surround** — buried by your own tools

- "Slack, email, docs, tickets, three more tabs — and somehow it all lands on you."
- _Pattern:_ recognizable tools pile in until they surround and bury the viewer — the pain is being swamped, not one bad number.

### PRODUCT_INTRO

**kinetic-type-beats** — "Introducing…" name-drop

- "Elevating experiences, removing manual touchpoints, automating processes — so you can focus on the customer."
- Uizard — "Introducing Uizard — the design tool for everyone."
- _Pattern:_ hard-cut through "Introducing…" / tagline / value beats and resolve on the brand name or logo.

**logo-assemble-lockup** — wordless premium sting

- Manifold — "Manifold." _(wordless mark assembles; VO optional — just the name)_
- _Pattern:_ an abstract system assembles around a fixed mark — no copy, or just the product name landing.

**cursor-ui-demo** — first cursor-led look

- ClickUp — "This is ClickUp — click through and watch your whole workspace change."
- "Pull up any contact, find the right advisor, and you're matched in seconds."
- PaLM 2 — "Meet PaLM 2 — what is it, what can it do, and how was it built?"
- _Pattern:_ a cursor sweeps in to introduce the surface — a light first look landing on a hovered hero element or fresh result.

**dataviz-countup** — open on the result

- SuperX — "X growth — discover what really works: 19.6 million impressions."
- _Pattern:_ a confident "look at the data / the result" open — scroll a tilted card grid to one glowing hero metric, tagline assembling word by word.

**video-text-pivot** — show it work, then the number

- "Watch it run — then look at what it saved: 14 hours, every week."
- _Pattern:_ the product video plays, then slides aside to hand the frame to one impact stat — "see it work, now see what it's worth."

**prompt-type-submit-generate** — something you talk to

- "Meet Ada — describe what you need, attach what you have, and let it run."
- _Pattern:_ the first look IS the composer — the VO introduces the product as a conversation partner while a long prompt types with attachments and option picks, ending on (or just after) the submit.

**spatial-pan-stations** — decode the idea, then land on it live

- "Capture, structure, publish — that's the idea. Here it is running."
- _Pattern:_ a labeled concept strip read station by station, the final pan bridging into the live demo — "here's the idea → here it is working."

**device-surface-showcase** — introduced by completing its core loop

- "Open a space, drop in your notes, hit share — that's it, that's the product."
- _Pattern:_ the product introduced by DOING its core loop once inside its real interface, stepwise and cursorless — the VO narrates the steps plainly and lands on "that's it."

**titlecard-reveal** — a near-still title prelude

- "Relay. Docs that write themselves. Let's look inside."
- _Pattern:_ 2–3 near-still cards seamed by blur-snap handoffs — name, one-line claim, then into the product; each card carries one short spoken phrase.

### KEY_FEATURE

**grid-card-assemble** — enumerate breadth at once

- Postcards — "Want more? Unlimited exports, 1,400 fonts, an AI assistant, version history — and it's free to try."
- ClearVPN — "ClearVPN is built to help you: streaming access, secure browsing, location changing — only the essentials."
- Copilot — "Command bar, Zapier, white-labeling, API, SOC2 — and a whole lot more."
- _Pattern:_ a tile/pill/card grid self-assembles to show many capabilities at once — "look how much it does."

**cursor-ui-demo** — one workflow, end to end

- "Scroll your feed, then jump straight to your notifications — it's all one click away."
- Flowrite — "Pick your recipient, set your intention, choose a tone — and Flowrite writes it for you."
- Descript — "Tune your edits, add a crossfade, automate the volume, normalize loudness — then export."
- _Pattern:_ one specific multi-step workflow shown end-to-end across 2–4 real edits, landing on the action button or result.

**device-surface-showcase** — experienced inside its real interface

- HRS — "Your flight's cancelled — so book a hotel, a taxi, and get reimbursed, all in one digital journey."
- HelpKit — "A dynamic table of contents that follows your readers as they scroll."
- Graphite — "Use unique themes, recolor one element or several, and configure it all in a handy window."
- Contra — "Pick a template, make it yours, and launch a portfolio that's unmistakably you."
- _Pattern:_ a feature shown being USED inside its real surface — the device/window is the hero and its screens advance through a flow.

**comparison-split** — two paired capabilities, side by side

- "Design on the left, code on the right — always one source of truth."
- _Pattern:_ two complementary capabilities of equal weight shown together — "X and Y, in lockstep."

**video-text-pivot** — the feature, then its result

- "Here's the editor in action — and the result: a publish-ready cut in minutes."
- _Pattern:_ a feature clip runs, then yields the frame to a metric / impact line — the clip proves it, the number lands it.

**prompt-type-submit-generate** — one ask, one answer

- "Ask for revenue by region — and the chart draws itself."
- _Pattern:_ ONE prompt→response round trip — the VO names the ask, lets the status theater breathe a beat, then calls the result as it streams in.

**agent-progress-theater** — the machine visibly works

- "Kick off the scan — it checks every file, flags what's broken, and fixes what it can. Watch."
- _Pattern:_ trigger → working theater → receipt: the VO hands the work over, then reads the findings as rows land and check off — present tense, the machine is the subject.

**panel-edit-live-sync** — one gesture, two surfaces

- "Drag the value — the button follows. Pick a unit — the code converts. Live."
- _Pattern:_ 2–4 short cause→effect couplets, each pairing a gesture with its live mirror ("do X — Y answers"), ending held on the last edit.

**transcript-scroll-artifact-reveal** — the work, then the deliverable

- "It planned, researched, built, and tested — and left you the spreadsheet to prove it."
- _Pattern:_ a "look how much happened" line read down the transcript at traversal pace, then one pivot line cashes it in on the artifact — evidence first, payoff last.

**camera-journey** — a cinematic flight over the result

- "A month of content — planned, scheduled, and ready before you sat down."
- _Pattern:_ a flying camera explores the generated artifact while the VO makes one calm, sweeping claim; the content acts by itself — no hands, no clicks.

**dataviz-countup** — the numbers prove the feature

- "Response time, down 40%. Coverage, 3×. Every claim, a number."
- _Pattern:_ the feature proven by its metrics — a stat montage scrubbed / counted up while the VO reads each number as it lands.

### BENEFITS

**kinetic-type-beats** — rapid-fire value montage

- AiAgent — "No API keys, GPT-4 access, simple UX, clean UI — moving fast."
- Uizard — "Export to Sketch, create style guides, share, collaborate — and code less."
- _Pattern:_ a staccato montage of 8–12 short value phrases, each flashing and clearing at high tempo.

**grid-card-assemble** — an accumulating value list

- Lineicons — "Consistent and clean, tons of free icons, a Figma plugin, a powerful editor, every format you need."
- Plutio — "Manage projects, track time, send invoices, write proposals — all deeply customisable."
- _Pattern:_ short value phrases populate a vertical list ~1/sec, co-resident and accumulating, each popping into its slot.

**titlecard-reveal** — the calm value beat

- CSS Scan Pro — "A smart color picker — with instant tints and shades."
- _Pattern:_ one clean two-line value title, one slide-up crossfade, then held still. Low motion is the point.

**camera-journey** — travel the value chain

- "Leave one comment here — and the forecast updates over there."
- _Pattern:_ a cause→effect round trip: the VO's first half lands on the action, its second half on the payoff the camera travels to — "do this small thing here, get this big thing there."

**zoom-out-workspace-reveal** — this is just one corner

- "That one file it fixed? A corner of everything it already did."
- _Pattern:_ the VO tells the micro-story during the close-up dwell, then the scale line lands with the zoom-out — the benefit is breadth, revealed in one move.

**fixed-anchor-cycle** — everything changes, this stays

- "Same prompt. Every tool you own."
- _Pattern:_ one pinned claim while the entire surface re-skins around it — a short "works everywhere" line, then let the cycling themes speak.

**cursor-ui-demo** — demo, value line, demo

- "Watch it draft the reply — that's an hour back — now watch it file the ticket."
- _Pattern:_ a demo|text|demo sandwich — the VO alternates showing and telling, naming the value in the text beat between two live interactions.

### SOCIAL_PROOF

**constellation-hub** — the hub at the center of your stack

- kyvos — "On any BI tool — Tableau, Looker, Power BI — Kyvos sits at the center of your stack."
- "Connects to thousands of apps — including every one you already use."
- _Pattern:_ the product mark is the hub and partner logos orbit it — "sits at the center of everything you use." In the scatter-drift end-card variant there is no hub and no ring: a serif claim holds center while app icons pop in scattered and drift slowly outward — breadth said with count and spread, not geometry.

**grid-card-assemble** — a logo wall pulling back to a vast ecosystem

- Lineicons — "Used by more than 100,000 designers, developers, and companies — including these."
- ClickUp — "Connect Google Drive, Slack, GitHub, Stripe — your whole ecosystem in one place."
- Copilot — "With thousands of partner apps — Airtable, Calendly, Jira, Asana — you can embed anything."
- _Pattern:_ a wall of partner/app logos builds, then a camera zoom-out reveals a vast ecosystem.

**titlecard-reveal** — busy → clean proof card

- Trumpet — "We supply the trumpet, you bring the band — loved by 1,000+ sales, success, and marketing teams."
- _Pattern:_ wipe a busy open away to a clean lockup plus a "loved by N+ teams" line that settles and holds.

**dataviz-countup** — the numbers vouch

- "Twelve thousand teams. 4.9 stars. 99.98% uptime."
- _Pattern:_ proof by count-up — adoption, rating, and scale metrics tick up as the VO reads them; the biggest number lands last.

### CTA

**kinetic-type-beats** — punchy closing line beat-by-beat

- Stylebit — "Go pro, connect up to five Figma accounts — more features coming. Join now."
- revid.ai — "Boost your engagement and turbocharge your social media."
- _Pattern:_ a closing line (or short value stack) that snaps in beat by beat and lands on the logo or URL.

**logo-assemble-lockup** — logo build → push-through into the URL

- Strapi Cloud — "Deploy on Strapi Cloud — no server hassle, same flexibility. Try it now at strapi.io/cloud."
- Highlander — "Highlander is ready for the future you're building. Let's raise — at highlander.ai."
- STUDIO AI — "Get early access to STUDIO."
- Glorify — "Get started for free now — no credit card required."
- _Pattern:_ the logo builds, a fast camera push-through streaks giant CTA letters past the lens, resolving on the URL or action verb.

**cta-morph-press** — identity condenses into one click

- Linear — "This is Linear. Start building — it's free."
- _Pattern:_ the brand mark condenses straight into the single thing you click — "here's us → click here," no spatial set.

**prompt-type-submit-generate** — the command is the ask

- "One command — npm install relay — and you're live."
- _Pattern:_ the closing invitation IS a typed install command — the headline demotes, the terminal pill types it out, and the VO speaks the command (or one short line over it); the card holds with only the caret blinking.

**constellation-hub** — the orbit collapses into action

- "Everything you use, one hub — click, and it's yours."
- _Pattern:_ the ecosystem ring collapses onto the core on one click that springs the product open — the VO turns "it connects everything" into the action line.

**titlecard-reveal** — a calm end-card stack

- "Try it free. No credit card. relay.app."
- _Pattern:_ 2–3 near-still cards hard-cut in sequence, one short closing phrase each, terminating on the held logo/URL — the calm is the confidence.

### BRAND_OUTRO

**kinetic-type-beats** — a verb barrage resolving on one word

- Phantom — "Buy, store, stake, swap, send, connect, explore — multichain."
- _Pattern:_ a rapid center-channel barrage of single-word verbs asserting breadth, resolving on the brand's one defining word. No logo lockup needed.

**typewriter-reveal** — persistent mark + typed CTA rail

- Collato — "Next time, just Collato it — sign up for free today."
- _Pattern:_ the mark holds dead-center the whole time while a sub-line types or swaps into the final CTA.

**logo-assemble-lockup** — elements clear, the lockup draws itself in

- Copilot — "Copilot." _(pills disperse off-frame, the mark draws on; VO optional — just the name)_
- Dora AI — "Dora AI — join the waitlist."
- _Pattern:_ feature/UI elements clear the stage off all four edges, then the logo mark draws itself on and the wordmark completes the lockup.

**ticker-takeover** — use-cases cycle, the brand takes the frame

- "For notes, for tasks, for plans, for teams — [brand] holds it all."
- _Pattern:_ closing use-cases/verbs cycle through one slot, then the brand mark crashes in and owns the final frame.

**fixed-anchor-cycle** — the anchor holds, the words cycle

- bolt.new — "Prompt, run, edit, deploy — enjoy."
- Anthropic — "Opus 4.6 — by Anthropic."
- _Pattern:_ the brand name sits immovable while tagline words or praise quotes cycle beside it — per-word highlight stepping, or an accelerating flurry — landing on the completed lockup.

---

## VO_MODE handling

**No pasted script** — write the VO yourself, in the matching blueprint's script shape:

- 1–2 sentences per spoken beat, usually 6–20 words.
- Concrete and human; active verbs; say what the product does for a person.
- Avoid: "seamless experience," "unlock the power of," "streamline your workflow," long noun-phrase lists, a whole beat that is just "Or…".
- Silent beats are allowed when the visual proves the point — leave them out of `SCRIPT.md`.

**`VO_MODE = restructure`** — treat `user_script.txt` as source material. Rewrite, reorder, merge, or omit to fit the arc and target length. You may still shape each segment toward its beat's blueprint pattern.

**`VO_MODE = verbatim`** — do NOT change the user's words. Segment the script into beat-sized chunks at sentence/paragraph boundaries (split a long sentence only at a natural clause boundary). Final duration follows the provided script. Blueprint shaping does not apply to wording — only to which shape each verbatim chunk is paired with.

## Asset candidates

`asset_candidates` is the Step-3 → Step-4 handoff. Rules:

1. Read only `capture/extracted/asset-descriptions.md` to know what exists.
2. Use only filenames listed there; write as `assets/<basename>`.
3. One line, candidates separated by semicolons, a short description after `—`.
4. Prefer `[video]` assets when motion proves the product better than a still.
5. Use content assets (UI, screenshots, product photos, charts, demos). Skip tiny icons, favicons, badges, decorative chrome, repeated logo variants — unless the beat needs them. Partner / third-party logos come from `/media-use` (`resolve --type logo --entity <brand>`) — never redrawn by hand.
6. Pure-typography beats may use an empty asset list. Do not use nested lists.

Example:

```md
- asset_candidates: assets/dashboard-hero.png — dark analytics dashboard, wide screenshot; assets/demo-loop.mp4 — query-to-result interaction clip
```

## transition_in

Between-frame transition — how each frame ENTERS from the one before it. The harness's injector stamps it onto the two whole-frame clips (opacity / transform / filter on the frame wrappers). Name a **registry type** directly; optionally add a direction and/or a duration (`push-slide LEFT`, `crossfade 0.4s`). `cut` / `none` / empty = a hard cut.

The five registry types:

- **`crossfade`** — a plain opacity dissolve; the neutral choice when two frames sit in the same visual world.
- **`blur-crossfade`** — dissolve through a soft blur + slight scale; use when the two frames' backgrounds differ a lot, so the blur masks the color clash a plain crossfade would expose.
- **`push-slide`** `[LEFT|RIGHT|UP|DOWN]` — outgoing slides off, incoming pushes in from the opposite edge; a lateral "next beat" feel for a run of consecutive cards / feature beats.
- **`zoom-through`** — outgoing scales up + blurs out, incoming scales up from small into focus; for a STATE CHANGE / turning to a new section (hook → context).
- **`squeeze`** — outgoing compresses to a line on one edge as incoming expands from the other; a snappy, mechanical beat change.

Pick a small set and repeat them: default to `crossfade` (or `blur-crossfade` when the backgrounds clash), and reach for `zoom-through` at section boundaries. Frame 1's `transition_in` is a placeholder.

## Music & silence

The storyboard's top YAML block carries a `music:` field — the BGM mood the audio step retrieves against (e.g. `music: confident minimal tech underscore`). Omitting it falls back to `message:` → `arc:` → a neutral default, so BGM plays unless turned off explicitly.

- **`music: none`** — BGM off (narration, if any, still runs).
- **`music: none` + no `SCRIPT.md` + no `sfx:` cues or host audio** — the canonical **fully-silent marker**: no narration, no BGM, no SFX. `audio.mjs` generates nothing and Step 3.1 is a clean skip. Use exactly this spelling when the user asks for a silent / music-free video.

## Frame template

Use the exact fields required by the core storyboard format. The narrative shape each frame satisfies:

```md
## Frame N — Short name

- scene: one clear visual idea
- voiceover: "spoken line, written in the candidate blueprint's script shape, or empty"
- duration: rough estimate in seconds
- transition_in: crossfade
- status: outline
- src: compositions/frames/NN-short-name.html
- type: hook
- persuasion: Pain validation
- beat: urgency
- blueprint: kinetic-type-beats — candidate shape from the role→blueprint menu; omit when none fits
- asset_candidates: assets/example.png — short asset description

narrativeRole: what this beat does in the viewer journey.
keyMessage: the one idea the viewer should remember.
```

- `persuasion` — a concrete move (Pain agitation, Negative contrast, Friction reduction, Show-don't-tell proof, Feature-to-benefit translation, Statistical proof, Authority by association, Social proof, Risk reversal, Future pacing, Value stacking, Rule of three, Scarcity/urgency, Status seeking…). Never "show benefit." Invent one if none fits and explain it in the prose.
- `beat` — a specific emotion (anxiety, frustration, overwhelm, tension, urgency, skepticism, FOMO → relief, curiosity, clarity, intrigue, aspiration → trust, confidence, control, ease, power, awe, excitement, belonging → triumph, motivation, urgency-to-act, peace of mind, inevitability). Compound allowed (e.g. `relief + control`).

## Final checklist

- The arc is named; the sequence is narrative-driven, not page-order-driven.
- The opening uses one clear hook strategy that creates tension/curiosity/desire.
- Each beat has one job; every beat has `type`, `persuasion`, `beat`.
- Each beat's `voiceover` is written in its candidate blueprint's script shape (from the bank), with the candidate `blueprint:` tagged wherever a shape fits — and omitted where none does.
- Each `voiceover` is phrase-segmented into cues (each cue a piece Step 5 can reveal on) — not one long run-on clause.
- Shapes vary across the video; no single blueprint on every beat.
- Story truth was never bent to fit a blueprint — no beat invented/dropped/reordered for a shape.
- Every visual beat has suitable `asset_candidates` (filenames only from `asset-descriptions.md`), unless intentionally typography-only.
- UI/product demos use a multi-beat sequence when the value depends on workflow.
- `transition_in` is a registry type (`crossfade` / `blur-crossfade` / `push-slide` / `zoom-through` / `squeeze`) — default `crossfade` (`blur-crossfade` on a background clash), `zoom-through` at section boundaries, repeated across the video.
- `SCRIPT.md` contains only locked spoken narration; silent beats are intentional and omitted.


<!-- ===== FILE: hyperframes/product-launch-video/references/visual-design.md ===== -->

# Visual design — product-launch per-frame shot method

> The method behind **Step 4 (Frame visual design)**. You (the orchestrator) read it to **enrich `STORYBOARD.md` frames in place** — story-design wrote the skeleton (each frame's `scene`, `voiceover`, `transition_in`, the narrative fields, its `asset_candidates`, and optionally a candidate blueprint id); you add how each frame **looks and moves**. The unit you write per frame is a **time-coded shot sequence** — a shot directed across its whole duration, not a static slide. You write **no HTML** (that's the frame workers), you **never read `capture/`** (story already chose the assets), and you do **not** select assets or name transitions (story owns both). `frame.md` is your palette/type truth by role. Layout is a compact vocabulary in this file (the **Layout** section below), stated inline per Scene; motion vocabulary + the motion doctrine + the seek-safe core → `motion-language.md`; the proven shapes → `../../hyperframes-animation/blueprints-index.md` + `blueprints/<id>.md`; concrete rules resolve in Step 5 from this skill's local `../../hyperframes-animation/rules/`. Adding palette theory or a generic font rule here? Wrong home — `frame.md` + `hyperframes-creative`.

## The unit is a time-coded shot sequence

A frame's visual layer is **a sequence of time windows paced to the voiceover**, not a bag of effect tags. The failure that reads as PowerPoint is **front-loading**: the agent rushes the whole canvas on screen in the first ~25%, and then it just sits (the old representation — a flat set of effect names + a prose note — fired everything at entrance and left the rest empty). A time-coded shot sequence written **against the VO** makes that impossible: each window states what is on screen and what is moving, and **nothing appears before the voiceover reaches it.**

Write each frame as a handful of windows cued by the spoken line:

```
Scene 1 (0.0–Xs):  only what the VO is saying at t=0 enters — never the whole canvas
Scene 2 (Xs–Ys):   the next piece reveals as the VO names it (a line / card / stat / icon)
  …                one window per spoken cue — as many or as few as the line calls for
Scene N (…–end):   content has resolved; hold the read (stillness; subtle jitter at most)
```

- Each `Scene` line names **what's on screen**, **what moves in this window**, and **where it sits** (layout, inline). Times are real seconds across the frame's `duration`.
- **Pace reveals to the voiceover; never front-load.** This is the core anti-PowerPoint mechanism (→ `motion-language.md` Part 2 Rule 2). At t=0 show only what the VO is saying then; reveal each further piece — a line, a card, even an h1 — **when the VO names it**, spreading reveals across the shot and especially the **back ~50%**. **The window count = the number of spoken cues the line calls for** — a two-beat line is two windows, a five-feature list is five or six. There is **no fixed count and no mandatory "middle" act**; the only sin is dumping everything up front.
- **End on a held read.** Once the content has resolved it holds and reads — **prefer stillness to bad motion**: no forced camera drift, no lazy breathing, no back-half pan/push; at most a subtle jitter keeps it alive (→ `motion-language.md`). On a short shot the final reveal and the hold are the **same window** — the hold is not a separate mandatory act. Only the final frame has a real exit; every other frame's exit is the harness transition (story's `transition_in`).
- A **deliberately held** frame — content already revealed, now reading still — is legitimate and often right (a climax, a breather). The failure is never "too still"; it is **front-loaded-then-frozen** (everything dumped by ~25%, nothing cued to the VO). Place held beats deliberately for rhythm so the video isn't uniformly busy (allocate them in `## Video direction`). Reveal pacing + holds + the idle budget → `motion-language.md`.

## Pick the shape — instantiate a blueprint

Don't invent each shot from scratch. The frame's **role** (its `type` / `beat`) points to a proven shape:

1. **Match the role to a blueprint.** Open `../../hyperframes-animation/blueprints-index.md`, find the frame's role in the **role→blueprint menu**, and pick the blueprint whose intent fits this beat (story may already have named a candidate id — confirm or override it). Read that `blueprints/<id>.md`: it is a short, product-agnostic, **time-coded shot template with `[slots]`** and a named **signature move** (the thing that makes the shape itself — the SVG ring, the push-THROUGH, the in-place token swap).

2. **Instantiate its `[slots]` with THIS product's content** — three postures:
   - **Reproduce** — the blueprint fits the beat and your content maps onto its slots cleanly. Fill every `[slot]` with this product's word / asset / stat and follow its Scene timing. Write the resulting Scene lines.
   - **Adapt** — the _structure_ fits but the content / asset-count / surface doesn't (or you want a fresher surface to avoid templating). State **what you keep / what you change** in one line, then write the adapted Scene lines. You may extend or vary; you may **never** drop the **signature move** (drop it and you picked the wrong blueprint), and you keep the reveals **paced to the VO** — never collapse the shape to a single front-loaded dump.
   - **Compose** — no blueprint fits the beat. Build the shot from the **motion vocabulary** in `motion-language.md`: still pace the reveals to the VO across the shot, never fire everything at t=0. Mark it `blueprint: compose`.

3. **Keep the signature move.** Whichever posture, the blueprint's signature move (named in its file) is the spine of the shot — it usually lands on the shot's key reveal. Carry it through.

The blueprint's own Scene lines, motion vocabulary, and `rule mapping` are your raw material; you are choosing a shape and casting this product into it, not copying an engineering spec.

## What you add to each frame

Story-design's `## Frame N` block already carries the narrative + `asset_candidates`. You append the shot. Story's `scene` / `voiceover` / `transition_in` / role fields stay untouched.

```
## Frame 3 — The problem
- scene: a 20-minute timer over a stack of rejected takes   ← refine only if it could read sharper
- voiceover: "…"            ← story's; leave it
- transition_in: crossfade  ← story's; leave it
- type: pain_point          ← story's
- persuasion: Pain agitation
- beat: frustration
- blueprint: dataviz-countup (Adapt)   ← you add: the id you instantiated (or "compose")
- focal: assets/reject-stat.png         ← you add: the hero asset for this beat
- roles: reject-stat = cutout · timer = supporting · backdrop = background (dim ~40%)  ← you add: role per candidate
- sfx: impact-soft, riser               ← you add: the sound the beat wants (fetched + mounted at root; never yours to embed)

Adapt: keep the count-up-ring signature; one stat not three, and the trend chart becomes the rejected-takes count climbing.
Scene 1 (0.0–1.2s): solid backdrop (dim ~40%); a circular progress ring + bold center number seat dead-center, ring sweeps and number counts 0→20 on one heavy ease — Centered template, ~50% of frame. Slow push-in runs underneath.
Scene 2 (1.2–3.4s): as the VO names the count, the camera pushes THROUGH the ring into the rejected-takes stack lower-left; the stack grows beat-by-beat as a reject counter ticks up beside it (the count-up reveals on its spoken cue, not at t=0). Asymmetric 60/40, 3 depth layers.
Scene 3 (3.4–5.0s): land the hero stat card dead-center, accent glow blooms behind it and holds; the stat reads clean and STILL — no continuing push, no breathing (a held beat beats bad motion). The stillness reads against the prior motion.
```

The lightweight tags:

- **`blueprint:`** — the id you instantiated (with `(Reproduce)` / `(Adapt)`), or `compose`. One id per frame.
- **`focal:`** — which existing candidate is the hero of this beat.
- **`roles:`** — each candidate's role: `cutout` (foreground subject, lay text around it) · `background` (full-bleed, dim 30–50%) · `supporting` (secondary). You **consume** the candidates story chose — never add, swap, or drop one (coverage is story's call; if a frame truly has the wrong candidates, flag it back, don't reach into `capture/`).
- **`sfx:`** — name the sound the beat wants (an impact for a slam, a whoosh for a push, a riser into a reveal). The audio script's `fetch-sfx` pass retrieves it and the assembler mounts it at the root — you only **name** it, never embed an `<audio>` element.

**Layout is stated INLINE in each Scene line** — name the template, density, depth, and hierarchy as part of "where it sits" (`Centered, ~50% of frame`, `asymmetric 60/40, 3 depth layers`), drawing on the **Layout** vocabulary below; never write px / scale / shadow recipes (the worker writes those).

**Motion is named INLINE in each Scene line** — name the move from `motion-language.md`'s vocabulary (`ring sweeps`, `pushes THROUGH`, `count-up`, `glow blooms`) and let it settle on a long-tail curve (`power3` default — smooth beats bouncy; see `motion-language.md`). Never write ease curves / ms / stagger (those resolve in Step 5 from this skill's local `../../hyperframes-animation/rules/`).

## Layout — named inline per Scene

State each Scene's layout as part of "where it sits." **If the blueprint already implies a composition** (a ring around a center, stations on a wide canvas, two cards from opposite wings), that wins — describe it directly; the vocabulary below is for **composing freely** or a generic beat, not a menu you must pick from. Never write px / scale / shadow (the worker does). One frame's layout can EVOLVE across its Scenes (Scene 1 centered hero → Scene 2 rearranges to a grid).

- **Framing vocabulary** — centered (hero / climax) · rule-of-thirds · split-screen (comparison) · layered-depth (immersive) · asymmetric 60/40 or 70/30 (editorial) · triptych (three panels) · full-width strip. Vary the framing across the video so it doesn't read as one repeated template — let the beat decide, not a quota.
- **Density** — primary visual ≥ 40% of canvas; ≥ 3 depth layers (background + midground + foreground); never a lone small cluster floating in empty space. Squint test: after blur you can still pick out the #1 element.
- **Hierarchy** — combine ≥ 2 of size (3:1) / weight (800 vs 400) / contrast / position (upper-third is golden) / motion, so one element clearly dominates.
- **Depth** — layer 2–3 of: size, blur, opacity gradient, overlap, shadow-stack.
- **Don't show**: nav bars, footers, scrollbars, real cursors / browser chrome, generic decorative shapes standing in for a real asset, floating bokeh / purple-blue "AI" gradients — unless it's an intentional UI-demo reconstruction.

## `## Video direction` — write the invariants ONCE

The whole video shares one look and one motion grammar. Write a **`## Video direction`** block ONCE at the top of `STORYBOARD.md` so every frame inherits it and per-frame Scene lines carry only the **delta**. This block is load-bearing — it is what binds many independent shots into one film. **Keep it.**

- **palette system** — from `frame.md`: which roles map to which hues. Never invent.
- **motion grammar + reveal model** — long-tail eases (`power3` default, smooth over bouncy) + the **VO-paced reveal** model every frame follows (reveal each piece on its spoken cue; never front-load) + what may stay alive during a hold (subtle jitter at most; no lazy breathing) (→ `motion-language.md`).
- **rhythm / held-frame allocation** — name the **held / breather frames** (often before a climax) so the video varies its energy: most frames reveal to the VO, a few hold still (a held read beats bad motion; the anti-monotony discipline; → `motion-language.md`).
- **negative list** — what never appears: off-brand textures / effects the pack forbids, **plus both motion failure modes** — slideshow (front-load then freeze) and screensaver (everything floating independently) (→ `motion-language.md`).

Do **not** repeat these per frame — restating video-level rules in every frame is exactly the bloat this layer prevents.

## Palette & type — from `frame.md`, never invented

- **Palette** — `frame.md` (the adopted pack) is the color truth; apply its roles per frame. Generic basics (one accent, tint neutrals, avoid pure `#000`/`#fff`) → `hyperframes-creative/references/house-style.md`.
- **Type** — fonts resolve via `frame.md`'s type tokens; reference them **by role** (display / body / mono / the pack's ramp), never by raw family or px. Generic typography craft (embedded fonts, dark-bg optical compensation, `tabular-nums`) → `hyperframes-creative/references/typography.md`.

## Caption-band keep-out (plan side)

The bottom ~17% of the canvas is reserved for the caption pill. Plan every frame's content into the **top ~83%** so nothing important lands in the band (the worker enforces the pixel cutoff; you plan the layout). Holds even when captions are disabled — bottom-edge consistency.

## Where the detail lives

| For…                                                                      | Read                                                                                         |
| ------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------- |
| the proven shapes + role→blueprint menu + how to pick                     | `../../hyperframes-animation/blueprints-index.md` → `blueprints/<id>.md` (local)             |
| motion — shot model, vocabulary, holds, idle budget, stillness, seek-safe | `motion-language.md` (local)                                                                 |
| layout — templates, density, depth, hierarchy, caption band               | the **Layout** vocabulary in this file                                                       |
| concrete eases / ms / stagger + rule recipe bodies (Step 5)               | local `../../hyperframes-animation/rules/` (the frame worker reads it; you don't)            |
| palette + type tokens                                                     | the project's `frame.md`; basics → `hyperframes-creative` `house-style.md` / `typography.md` |
| "produced, not generated" foreground density                              | `hyperframes-creative/references/video-composition.md`                                       |
| within-frame cuts / seams (zoom-through · cut-the-curve · waterfall)      | `cut-catalog.md` (the worker builds them inside the composition)                             |
| transitions                                                               | story-design owns `transition_in`; you don't touch it                                        |

## Before you finish — checklist

- **`## Video direction`** written once at the top (palette · motion grammar + shot model + idle budget · stillness allocation · negative list incl. both failure modes); per-frame entries are deltas, not restatements.
- Every frame is a **time-coded shot sequence** with real second windows across its `duration` — not a tag bag.
- **No frame front-loads** — at t=0 only what the VO is saying enters; each further piece reveals on its spoken cue, across the back ~50%. Window count follows the VO, not a fixed number.
- Every frame names an **`blueprint:`** id (Reproduce / Adapt) or `compose`; an Adapt states keep/change and **keeps the signature move**; nothing collapses to a single front-loaded dump — reveals stay paced to the VO.
- **Held frames are deliberate** — allocated in Video direction for rhythm; a held read is fine (prefer stillness to bad motion), but no frame may be front-loaded-then-frozen.
- Each frame's `asset_candidates` have a `focal` + per-candidate `roles`; none added, swapped, or dropped.
- Layout named **inline** per Scene (template / density / depth / hierarchy — the **Layout** vocabulary here); motion named **inline** per Scene from the vocabulary (`motion-language.md`). No px / ease curves / ms / JS.
- Content planned into the top ~83% (caption band clear).
- Palette / type pulled from `frame.md` by role — nothing invented.
- You wrote no HTML and never read `capture/`.


<!-- ===== FILE: hyperframes/product-launch-video/sub-agents/frame-worker.md ===== -->

# Frame worker — product-launch delta

> The shared law is the core contract above (the packet builder prepends `../../hyperframes/references/frame-worker-core.md` to this file as `_role.md`) — read the two as one role. This file carries only what's specific to a product-launch frame; you run N-up, **one frame each** — your dispatch carries exactly one packet. Tempted to add a generic GSAP / timeline rule here? Wrong home — it belongs in the core contract or `hyperframes-core`.

## Your `focal:` / `roles:` — real captured media

- `focal:` — which candidate is the hero.
- `roles:` — each candidate's role: `cutout` foreground / `background` full-bleed / supporting — plus the real media available (each `public/<basename> — description`; a **`[video]`** tag marks a `.mp4` motion source that cannot be mounted by this sub-composition worker).
- **Asset paths are project-root relative everywhere.** This includes HTML attributes and CSS `url(...)` values such as `@font-face src`: use `assets/...` (or the supplied `capture/assets/...` path), never `../` or `../../`. Shared fonts are staged before dispatch so every parallel frame resolves the same local files; never fall back to a network `@import`.

## Placing candidates (product-launch constraint)

**Place each candidate by its `roles`** (the `focal` is the hero): a `cutout` is a foreground subject — respect the 83% keep-out, lay text around it, not over its face; a `background` is full-bleed and dimmed ~30–50% so foreground content stays legible. Frame files are sub-compositions. Audio remains orchestrator-owned: never author `<audio>` in a frame. An approved `[video]` candidate may be declared as a frame-local `<video data-frame-video="approved" data-start="..." data-duration="..." data-track-index="...">`; `assemble-index.mjs` hoists it to the host root and translates its timing. Give every approved video explicit host geometry with numeric `data-frame-video-x`, `data-frame-video-y`, `data-frame-video-width`, and `data-frame-video-height`; optionally set `data-frame-video-fit="cover|contain|fill|none|scale-down"` (default `cover`). The assembler converts only those values to host CSS: frame-local classes and inline styles do not cross the hoist boundary. Do not use this declaration for audio, unapproved URLs, or videos without explicit timing and geometry. If no approved video is supplied, use an explicitly supplied static still/key art (`[video-still]` or another image candidate) as `<img>`; do not extract a frame, fabricate a URL, or silently embed an unapproved clip.

When a frame showcases a captured website, use the supplied screenshot as the page. Do not rebuild the full site in HTML: even a close recreation can change the real layout, spacing, or branding. If the shot needs motion inside the page, overlay the supplied real assets at measured positions or rebuild only the moving component.

Brand text comes from your frame's `scene` / narrative — never from `frame.md` (a style spec, not the product's content). Place the named assets, and never invent new ones.

## Cross-frame handoffs

If the packet includes `handoff_in:` or `handoff_out:`, treat those values as a hard boundary contract. Start or end the named element at the exact x/y position, scale, opacity, and motion direction/speed provided; a field the packet states as unchanged is still binding, not optional. Do not restyle or reinterpret that boundary state. The neighboring frame is being built by another worker and will use the matching values.
