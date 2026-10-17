

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
