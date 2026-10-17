

<!-- ===== FILE: hyperframes/motion-graphics/GUIDE.md ===== -->

---
name: motion-graphics
description: >
  A short, design-led motion graphic where motion is the message — kinetic
  typography, stat count-up, chart/data-viz hit, logo sting / brand lockup,
  lower-third / callout / social overlay, animated map (highlight regions,
  connect places, zoom to a location), animated tweet / news-article /
  headline, webpage / UI animation (scroll, cursor, callouts), or fusing a
  real image's geometry into a chart. Usually under 10s (up to ~30s), no
  narration or live-action subject; renders to MP4 or transparent overlay.
  Longer / narrated / multi-scene → /general-video. Unclear → /hyperframes.
---

**Plugin installs:** Before setup or freshness commands, follow [plugin execution rules](../hyperframes/references/plugin-installation.md) when this skill is inside a HyperFrames plugin. Standalone installs keep the update instructions below.

> **First, keep this skill fresh — confirm with the user before running:** `npx hyperframes skills update motion-graphics`. A fast no-op when everything is current; otherwise it refreshes this skill plus the core domain skills it depends on before you rely on them.

> **figma source**: If the logo/asset/animation to build from comes from a figma.com URL, run `/figma` first — asset export, brand tokens, and Motion→GSAP translation if the graphic is a Figma Motion import — then build from its output. Don't drive Figma via raw MCP tools directly: that skips SVG sanitization, `.media/manifest.jsonl` provenance, and brand-token `var()` binding, so a later brand change can't propagate without a full re-import.

# motion-graphics — dispatch entry

> **The front door is `/hyperframes`.** This skill makes a **short, design-led, unnarrated motion graphic** (motion is the message; ~under 10s, no voice-over). Anything longer, narrated, or multi-scene — or any uncertainty → read `/hyperframes` first: the intent layer owns every route decision.

This workflow is **autonomous by design** — at most one clarifying question (`agents/director.md`), then build through verification without intermediate review. The intent layer (`/hyperframes` → `references/intent-interview.md`) routes here directly without run-shape questions; a storyboard and companion session add little to a piece this short. Rendering is still user-gated: after checks and proof snapshots pass, open the Studio preview and ask the canonical “render now, or what changes?” question from `../hyperframes/references/brief-contract.md`. When a `BRIEF.md` exists, read it before the director's question.

A short design-led motion graphic. **Asset-first**: decide the asset strategy and source real material _before_ designing the shot, then design the shot around what you have, then compose by reusing catalog capabilities. All artifacts go to `PROJECT_DIR = videos/<project-name>/` (created in Step 0); all paths below are relative to it.

| Phase    | Execution                                                             | Primary artifact                                                 | Detailed flow                 |
| -------- | --------------------------------------------------------------------- | ---------------------------------------------------------------- | ----------------------------- |
| init     | Bash                                                                  | `hyperframes.json`                                               | Step 0                        |
| plan     | subagent — **decide search?** + classify + asset strategy             | `shot-plan.json` (draft: category, `asset_needs` queries, brief) | `agents/director.md` (Part 1) |
| source ◇ | Bash — media-use resolve (**skip if `asset_needs` is empty**)         | `assets/` + `assets/index.md`                                    | `phases/source/guide.md`      |
| design   | subagent — shot design around resolved assets                         | `shot-plan.json` (final: block(s) + layout + motion + positions) | `agents/director.md` (Part 2) |
| build    | subagent — reuse-first composition                                    | `compositions/index.html`                                        | `agents/builder.md`           |
| verify   | Bash — `lint`, `check`, proof snapshots; repair on failure            | `.hyperframes/artifacts/snapshots/<id>/contact-sheet.jpg`        | Step 5                        |
| approve  | Open the preview; ask render or changes; wait for the answer          | explicit render approval                                         | Step 6                        |
| render   | Bash — `hyperframes render` (MP4, or `--format webm/mov` for overlay) | `renders/video.mp4` or transparent overlay                       | Step 6                        |

`◇ source` runs only when the chosen category declares assets. Pure code/text categories (e.g. `kinetic-type`, most `charts`/`stat`) have `asset_needs: []` and skip straight from plan to design.

## Categories — split by the search decision

`plan`'s **first decision is: does this need a search?** That fork splits the categories into two groups; then the specific category is picked — for search-driven, **by the type of content the search returns**. Each category is one `categories/<id>/module.md` (its planning + build rules); the shared motion vocabulary lives in `references/motion-vocabulary.md` (→ `hyperframes-animation` rules/blueprints + registry blocks).

**Form categories — no search; the user supplies the content:**

| Category       | Intent                                                                                                         | Leans on                                                                    |
| -------------- | -------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------- |
| `kinetic-type` | punchy line / quote / title, motion-first text                                                                 | `caption-*` blocks + animation rules                                        |
| `stat`         | single hero number / count-up + ring                                                                           | `apple-money-count` / `rules/{counting-dynamic-scale, stat-bars-and-fills}` |
| `charts`       | bar / line / pie / race / % from data                                                                          | `data-chart` block                                                          |
| `logo-reveal`  | logo sting / brand lockup (user logo)                                                                          | `logo-outro` / `rules/svg-path-draw`                                        |
| `lower-thirds` | name / title bars, callouts, social overlays                                                                   | `caption-*` + registry overlay blocks                                       |
| `maps`         | geographic motion — highlight regions, connect places, zoom to a location (vector lane, or baked basemap lane) | `us-map` / `world-map` family + `bake-basemap.mjs`                          |

**Search-driven categories — search first, then animate by content type** (the RWA path):

| Returned content | Category       | Animation                                                      |
| ---------------- | -------------- | -------------------------------------------------------------- |
| webpage / link   | `webpage`      | webpage / UI animation (scroll, reveal, cursor, callouts)      |
| news article     | `news`         | headline reveal + source card + key-fact callouts              |
| tweet            | `tweet`        | animated tweet card                                            |
| image / entity   | `asset-fusion` | the asset's geometry _becomes_ the chart (RWA diegetic fusion) |

Build order: one at a time, coverage-first (rough is fine). `kinetic-type` ported from the prototype; the rest follow.

## Prerequisites

macOS Apple Silicon or Linux x64. System tools: `brew install node ffmpeg`. `npx hyperframes doctor` once. macOS GPU render: `export PRODUCER_BROWSER_GPU_MODE=hardware`.

Optional keys (local fallbacks if unset) — only needed by categories that source/generate assets via media-use:

| Key                                 | Used for                                                    | Fallback                        |
| ----------------------------------- | ----------------------------------------------------------- | ------------------------------- |
| `GEMINI_API_KEY` / `GOOGLE_API_KEY` | image generation (media-use resolve)                        | skip generate / search-only     |
| (asset_scout / search providers)    | `webpage`/`news`/`tweet` + `asset-fusion` real-asset search | category degrades to asset-free |

## Flow

### Step 0 — Initialize

cwd is the agent workspace root; write all artifacts under `PROJECT_DIR = videos/<project-name>/`. `<project-name>`: use the dir the user gave, else a short kebab-case name from the intent (`<subject>-motion`). Not the workspace basename or a timestamp.

Only when `$PROJECT_DIR/hyperframes.json` is absent:

```bash
PROJECT_DIR="${MOTION_GRAPHICS_DIR:-videos/<project-name>}"
mkdir -p "$(dirname "$PROJECT_DIR")"
npx hyperframes init "$PROJECT_DIR" --non-interactive --example=blank --skill=motion-graphics
```

`init` checks the installed skills against the latest on GitHub and updates the global set if any are out of date.

**Constraints:** never `hyperframes init` in the workspace root; never nest another `hyperframes/` inside `PROJECT_DIR`; every Bash command (master + subagents) is a `(cd "$PROJECT_DIR" && ...)` subshell — never bare `cd`.

### Step 1 — Plan (subagent: Director Part 1)

Dispatch one subagent. prompt = full `agents/director.md` + `## Dispatch context` (`SKILL_DIR` / `PROJECT_DIR` / the user's request / `Schema: <SKILL_DIR>/references/shot-plan-ir.md`). It must:

1. **Decide: does this need a search?** (the first fork)
   - **No** → pick a **form category** (kinetic-type / stat / charts / logo-reveal / lower-thirds / maps); content is user-supplied; `asset_needs: []`.
   - **Yes** → emit a **search plan** into `asset_needs[]` (news / web / tweet / image; two-pole queries). The specific **search-driven category** (webpage / news / tweet / asset-fusion) is confirmed by the content type returned in Step 2, and finalized in Step 3.
2. Write a draft `shot-plan.json` (envelope + chosen form category _or_ search intent + `asset_needs` + a one-paragraph shot brief). Schema: `references/shot-plan-ir.md`.

Validation: `[ -s "$PROJECT_DIR/shot-plan.json" ] && echo ok || echo missing`.

### Step 2 — Source ◇ (Bash: media-use, conditional)

If `shot-plan.json.asset_needs` is non-empty, resolve assets (search / generate / fetch → frozen project-local paths + ledger). See `phases/source/guide.md` (wraps `media-use resolve`; the search-driven categories use the news/web/tweet/image search). If `asset_needs` is empty, **skip to Step 3**.

Degrade gracefully: if a search/provider is unavailable, the category falls back to asset-free (note it in `context.log`).

### Step 3 — Design (subagent: Director Part 2)

Dispatch a subagent (prompt = `agents/director.md` Part 2 + dispatch context including the resolved `assets/index.md` if Step 2 ran + `catalog-map.md`). It designs the shot **around the available assets**: pick the catalog block(s) + the `hyperframes-animation` rules/blueprints, the layout, the motion, beats, and (for `asset-fusion`) the `element_positions` + eyedropper palette. Finalizes `shot-plan.json` (`content.block` + `content.customize` + per-category content).

### Step 4 — Build (subagent: Builder, reuse-first)

Include the shared [motion principles](../hyperframes-creative/references/motion-principles.md) in the Builder's dispatch context. For `charts` and `stat`, also include [data in motion](../hyperframes-creative/references/data-in-motion.md). The Builder reads these guides before writing the timeline.

Dispatch a subagent. prompt = full `agents/builder.md` + dispatch context (`shot-plan.json`, `catalog-map.md`, the category's `module.md`, `references/motion-vocabulary.md`, `references/builder-contract.md`). **Reuse-first**: `npx hyperframes add <block>` + customize in place; hand-author only gaps + the asset-fusion affordance. Output `compositions/index.html` honoring the HF contract (paused GSAP timeline on `window.__timelines`, `class="clip"` + stable ids, `tl.seek(0)`, deterministic).

### Step 5 — Verify (Bash → repair subagent on failure)

```bash
(cd "$PROJECT_DIR" && npx hyperframes check .)
(cd "$PROJECT_DIR" && npx hyperframes snapshot --at <proof-times>)
```

Choose proof times that show the opening state, signature move, and final hold. Inspect the generated contact or snapshot sheet before continuing. On `lint`, `check`, or snapshot failure, dispatch the repair subagent (`agents/finalize.md`) for one in-place fix pass, then rerun the failed gate. Never change a fixed duration merely to hide a defect.

### Step 6 — Approve and render (Bash)

Open Studio, then ask one question: “render now, or what changes?” After revisions, return to the same gate:

```bash
(cd "$PROJECT_DIR" && npx hyperframes preview --background)
```

Render only after an explicit render answer:

```bash
(cd "$PROJECT_DIR" && npx hyperframes render . --skill=motion-graphics -q high -o ./renders/video.mp4)
# transparent overlay variant: --format webm  (or mov)
```

Verify the output exists, is non-empty, and has the intended duration. The final handoff names the artifact, actual duration, composition or frame id, proof times, and the inspected contact or snapshot sheet. Flags live in `/hyperframes-cli` → `references/preview-render.md`.

## Resume table

| State                                                    | Continue from              |
| -------------------------------------------------------- | -------------------------- |
| no `shot-plan.json`                                      | Step 1 (plan)              |
| `shot-plan.json` has `asset_needs`, no `assets/`         | Step 2 (source)            |
| `shot-plan.json` final, no `compositions/index.html`     | Step 3/4 (design+build)    |
| `compositions/index.html` exists, proof snapshots absent | Step 5 (verify)            |
| checks and proof snapshots pass, no approved render      | Step 6 (approval)          |
| approved render exists                                   | verify output, then report |

## Design notes (maintainers — execution does not read this)

- **Asset-first rationale:** sourcing is front-loaded and informs shot design (the RWA flow: analyze → search → review → compose). the search-driven categories (`webpage`/`news`/`tweet`) and `asset-fusion` both lean on media-use search (news/web/tweet/image), which is media-use's documented RWA lineage.
- **Reuse-first:** the in-ecosystem analog of LLM-generated templates is "compose catalog blocks + `hyperframes-animation` rules". HF's paused GSAP timeline ≙ Remotion's `useCurrentFrame`.
- **Category module contract:** one `categories/<id>/module.md` (planning + build), sharing `references/motion-vocabulary.md` (+ optional eval). Adding a category = drop the folder + register its classifier line in `agents/director.md` + its row in `catalog-map.md`; the phase pipeline is untouched.
- **Directory shape:**
  ```
  videos/<project-name>/
    hyperframes.json  context.log
    shot-plan.json            # the IR (Director output)
    assets/  assets/index.md  # media-use output (if sourced)
    compositions/index.html   # Builder output
    renders/video.mp4
  ```
- **Registration:** in `hyperframes` router — add the "design-led short motion graphic" intent + Workflow description; carve the motion-graphics triggers out of `/general-video`; add reverse Do-NOT-use edges. See `motion-graphics-genre.md` §5-7.


<!-- ===== FILE: hyperframes/motion-graphics/agents/builder.md ===== -->

# Motion-Graphics Builder

Turn `shot-plan.json` into one renderable HyperFrames composition (`compositions/index.html`). Everything stays in the HF ecosystem — HTML is the source of truth; a single **paused** GSAP timeline carries all motion; the engine seeks it. Category-specific build rules live in `categories/<id>/module.md`; this file is the shared contract.

## Reuse-first (the default)

Default = **compose existing catalog capabilities, not hand-author**:

- **Search first, for every named effect** — `npx hyperframes catalog --query "<the move, in plain English>" --json`, including an effect the user names after the plan is written. It needs nothing installed and no project. Author by hand only after a search came back with nothing that does the job, and report that miss with `npx hyperframes feedback --search-miss`.
- `npx hyperframes add <block>` (registry) → customize in place. Most blocks bake content/data into their own script (only a few expose CSS-var params), so reuse = **add + edit**.
- `hyperframes-animation` rules / blueprints / transitions for motion; runtime adapters (GSAP default).

Hand-author only (a) gaps no block/rule covers, (b) the `asset-fusion` affordance binding. The Director named the block(s) + customizations in `shot-plan.json` (`content.block` + `content.customize`); see `catalog-map.md`.

## The HF contract (non-negotiable)

- Root `#stage` carries `data-composition-id`, `data-start="0"`, `data-duration=<s>`, `data-fps`, `data-width`, `data-height`.
- Exactly ONE `gsap.timeline({ paused:true })`; register `window.__timelines["<id>"] = tl;`; end with `tl.seek(0)`. **Never `tl.play()`** for render-critical motion. No timers / async / event-driven timeline build. Finite repeats only.
- **Timed clips** need `class="clip"` + a stable `id`. Timeline-driven groups inside one full-duration clip don't each need timing attrs.
- **Fonts**: prefer local `@font-face` (.woff2) for deterministic / offline render; CDN Google Fonts do render (compiler caches + injects `@font-face`) but warn + need network.
- **Deterministic only** — no `Date.now()` / `Math.random()` / network.

## Layout before animation

Build the **hero-frame end-state** in CSS first (flex + padding; never absolute offsets on content containers; the root must be sized). Use `fromTo()` for elements inside `.clip` and for any delayed entrance; `from()` is safe only for non-clip elements active from `t=0`. Exits belong to transitions or the final scene. Full rules: `references/builder-contract.md`.

## IR → composition

- `content.block` → `hyperframes add` it (or inline) + apply `content.customize`.
- per-category `content` (text scenes / chart data / fusion positions / news-tweet content) → realize per `categories/<id>/module.md`.
- resolved `asset_needs` → reference **frozen project-local paths** (never a remote URL or a prompt).
- `palette[-1]` / bg + `font` from the envelope.
- `export: alpha-overlay` → transparent bg; render `--format webm` (or `mov`).

## Critical correctness (GSAP / seek)

Opacity-gate delayed elements (set hidden until their entrance). Clamp at tween bounds (no overshoot past a held value). Allowed eases: `power1–4`, `back`, `bounce`, `circ`, `elastic`, `expo`, `sine` (`.in/.out/.inOut`). One motif per scene. Run `hyperframes check` for overflow / collisions.

## Motion quality

Before writing the timeline, read and follow the shared [motion principles](../../hyperframes-creative/references/motion-principles.md). For `charts` and `stat`, also read [data in motion](../../hyperframes-creative/references/data-in-motion.md) before laying out or animating the data.

## Hand off for verification

Self-check the authored file, then return it to the orchestrator. Step 5 runs `hyperframes lint`, `hyperframes check`, and proof snapshots on the assembled project. Do not render. When redispatched with a finding, fix the offending element and never change a fixed `data-duration` during repair. Remotion-source migrations use `/remotion-to-hyperframes` and its SSIM harness instead.


<!-- ===== FILE: hyperframes/motion-graphics/agents/director.md ===== -->

# Motion-Graphics Director

Turn a request into a `shot-plan.json` for a short (~3–30s) **design-led motion graphic**. You run in **two parts** around the asset-sourcing step: **Part 1 (plan)** before sourcing, **Part 2 (design)** after. You do NOT write composition code — that's the Builder. Schema: `references/shot-plan-ir.md`.

## Part 1 — Plan (before sourcing)

Emit a DRAFT `shot-plan.json`.

0. **Decide first: does this need a search?** No → a **form category** (user supplies content). Yes → emit a search plan; the specific **search-driven category** (`webpage` / `news` / `tweet` / `asset-fusion`) is confirmed by what the search returns (Step 2 → finalized in Part 2).

1. **Classify** — form categories by intent below; search-driven categories are picked post-search:

   | Category       | Pick when…                                                                                                                                                                         |
   | -------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
   | `kinetic-type` | a punchy line / quote / title; text is the hero                                                                                                                                    |
   | `stat`         | a single hero number / count-up                                                                                                                                                    |
   | `charts`       | bar / line / pie / race / % from data                                                                                                                                              |
   | `logo-reveal`  | a logo sting / brand lockup (user supplies the logo)                                                                                                                               |
   | `lower-thirds` | name/title bars, callouts, social overlays                                                                                                                                         |
   | `maps`         | a geographic shot — highlight regions, connect places, zoom to a location. Sub-fork: **vector** (D3, stylized) vs **basemap** (baked MapLibre — real satellite/dark/zoom-to-place) |
   | `webpage`      | highlight / animate a real captured web page or UI _(search-driven)_                                                                                                               |
   | `news`         | a news article → article-highlight: blur → zoom into keyword _(search-driven)_                                                                                                     |
   | `tweet`        | a tweet → animated card _(search-driven)_                                                                                                                                          |
   | `asset-fusion` | a real photo/asset's geometry _becomes_ the chart _(search-driven)_                                                                                                                |

   If genuinely ambiguous between two, ask exactly one question. Then load `categories/<id>/module.md` for that category's specifics.

2. **Asset strategy → `asset_needs[]`.** Each item: `{ role, kind: image|icon|logo|svg|news|web|tweet, query|source, treatment }`.
   - asset-free (`kinetic-type`, most `stat`/`charts`) → `asset_needs: []`.
   - `maps` → **vector** lane: `asset_needs: []` (D3/TopoJSON, runs live in HF). **basemap** lane (satellite/dark/zoom-to-place): `asset_needs: [{ type: "map-bake", … }]` (baked in Source — see `categories/maps/module.md`).
   - `webpage` / `news` / `tweet` → search the real source (page / article / tweet) + a supporting image. **Two-pole queries only**: atomic (1–3 words, composable: portraits, logos, objects) OR specific (5–15 words: a news event, a tweet). Never the middle. A failed specific query is dropped, not broadened.
   - `asset-fusion` → search or generate one hero asset.
   - `logo-reveal` → user-supplied logo (`source`).

3. **Envelope**: `duration_s` (3–30), `fps` (30), `canvas` (default 1080×1920; 16:9 / 1:1 per platform), `style`, `palette` (hex list, or `"derive-from-asset"`), `font` (from the HF embed list), `beats`, `export` (`mp4` | `alpha-overlay`).

4. **Shot brief**: one paragraph — what the viewer experiences + the single dominant motion idea.

## Part 2 — Design (after sourcing)

Given the draft + resolved `assets/index.md` (if Step 2 ran) + `catalog-map.md`, design the shot **around the assets**:

- **Run `npx hyperframes catalog --query "<the move, in plain English>" --json` for every look or effect the brief names**, before naming any block. It ranks the whole hosted registry and needs nothing installed. `catalog-map.md` is a partial snapshot; the search is the source of truth.
- Pick the **catalog block(s)** from those results + the `hyperframes-animation` rules / blueprints (see `catalog-map.md` for how each category customizes).
- Layout (hero-frame), motion (per `references/motion-vocabulary.md`), beats, pacing, exits.
- `asset-fusion`: read the asset's **geometric affordance** → `element_positions` (center / extent / safe-zones / avoid-zones) + **eyedropper palette** from the asset.
- Finalize `shot-plan.json`: `content.block` + `content.customize` + the per-category `content`.

## Heuristics (design-led short motion)

- **Motion IS the message**; no narration arc. Hook lands fast (~first 0.5s). **One dominant motif.** Pattern-interrupt if the piece runs >~2.5s (change exactly one thing). Effect intensity matches the energy. Legibility: a key element stays readable ≥~0.3s. Beats may be anticipated ~0.1s for perceived sync.
- **Reuse-first**: name a catalog block; ask for hand-authored motion only for gaps + the `asset-fusion` affordance.

Then hand `shot-plan.json` to the Builder.


<!-- ===== FILE: hyperframes/motion-graphics/agents/finalize.md ===== -->

# Finalize / repair subagent

Perform snapshot QA and one in-place repair pass. Dispatch only when Step 5 `lint`, `check`, or snapshot review reports a defect. The orchestrator owns final approval and render; this agent never renders.

## Dispatch context

`SKILL_DIR` / `PROJECT_DIR` / proof snapshot times / `lint` and `check` output tails, when present.

## Flow

1. **Snapshots** — run `npx hyperframes snapshot --at <proof-times>` and inspect overflow, off-canvas content, text collisions, empty frames, wrong content, and unreadable motion.
2. **One in-place repair pass** — edit `compositions/index.html` for the visible issues. Never change a fixed `data-duration`; timing is set upstream.
3. **Recheck** — rerun `npx hyperframes lint`, `npx hyperframes check`, and the affected snapshots. Return the result to the orchestrator without rendering.

## STOP / escalate

Only when the shot is **fundamentally wrong** (whole content off, needs recomposition) — return to Step 3/4 (re-design + re-build), don't force it with edits. Small fixes never escalate.


<!-- ===== FILE: hyperframes/motion-graphics/catalog-map.md ===== -->

# Director → catalog block map (reuse-first)

<!-- registry-items: allow=geo-highlight,geo-flow,flag-borders,pin-rollout,stat-motion,data-composition-src -->
<!-- allow= entries above are deliberately NOT registry items: geo-*/flag-borders/pin-rollout and stat-motion are hand-authored gaps this file names in order to say they are gaps. -->

**Search the live catalog before you use this table, and again before any hand-authored effect.** Run
`npx hyperframes catalog --query "<the move, in plain English>" --json` — once per named look or effect the
user asks for ("CRT scanlines", "glitch", "film grain", "shimmer sweep"), including effects asked for
mid-build. **The search needs nothing installed**: it ranks the whole hosted registry (~400 items) from any
directory, with no project, no prior `add`, and no account. The table below is a hand-maintained snapshot of
part of that registry and it under-covers by design — treat a miss here as unproven, and only the search's
own empty result as evidence the catalog lacks the move. When it does, say so with
`npx hyperframes feedback --search-miss "<query>" --wanted "<the move>" --tier <tier from the envelope>`
before hand-authoring. Full flags and tiers: `/hyperframes-registry` → § Discovery.

The Builder's **default is to compose existing HF catalog blocks, not hand-author.** `npx hyperframes add <block>` drops a block's source into `compositions/`; the Builder then **customizes in place** — most blocks bake their content/data into their own script (only a few expose CSS-var `params`), so reuse = **add + edit**, not pure variable injection. Hand-author only (a) gaps no block covers and (b) the asset-fusion affordance binding.

After classifying intent → category, the **Director names the block(s) + what to customize** in the shot-plan IR:

```jsonc
"content": { "block": "data-chart", "customize": { "data": [...], "headline": "…", "palette": ["…"] } }
```

## Category → block(s)

| Category               | Borrow from catalog                                                                                                                                                                                                                                                                                                                                                                         | Customize                                                                                        | Gaps → hand-author                                                                                             |
| ---------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------ | -------------------------------------------------------------------------------------------------------------- |
| **kinetic-typo**       | one of **17 `caption-*`** (kinetic-slam, editorial-emphasis, clip-wipe, gradient-fill, neon-glow, glitch-rgb, matrix-decode, particle-burst, weight-shift, pill-karaoke, highlight, blend-difference…)                                                                                                                                                                                      | words; `emphasis_words` → `word--emphasis`; palette; font; timing                                | a motif none of the 17 cover                                                                                   |
| **charts**             | `data-chart` (bar+line, staggered, value labels), `bar-chart-race` (a race)                                                                                                                                                                                                                                                                                                                 | edit the data array + headline/subtitle; `--bg`/`--text`                                         | pie/donut, ring/%                                                                                              |
| **stat**               | `apple-money-count` (finance: $ counter + burst + SFX) **or** hand-author a generic %/number + ring per `categories/stat/module.md` (there is no `stat-motion` block)                                                                                                                                                                                                                       | target, prefix/suffix, label, palette                                                            | —                                                                                                              |
| maps/geo               | **vector lane**: `us-map` (+bubble/hex/flow), `world-map`, `spain-map` + **hand-author** `geo-highlight`/`geo-flow`/`flag-borders`/`pin-rollout` (NOT in registry — build per `categories/maps/module.md`). **basemap lane** (real satellite/dark / zoom-to-place): bake via `categories/maps/bake-basemap.mjs` → `<video>` + geo-aligned SVG overlay (border draw-on + colour-block fills) | regions/data, palette, callouts/connectors, basemap style                                        | (basemap lane now covers real imagery + zoom-to-address — was the gap)                                         |
| diagram                | `flowchart` (SVG connectors + nodes)                                                                                                                                                                                                                                                                                                                                                        | nodes, edges, labels                                                                             | —                                                                                                              |
| **brand reveal**       | `logo-outro` (piece assembly + glow + tagline + URL pill)                                                                                                                                                                                                                                                                                                                                   | logo asset, tagline, URL, palette                                                                | —                                                                                                              |
| transitions            | 15+ shader transitions (domain-warp, whip-pan, sdf-iris, glitch…)                                                                                                                                                                                                                                                                                                                           | direction, timing                                                                                | —                                                                                                              |
| social overlay         | ig / tiktok / yt / x / reddit / spotify / macos cards                                                                                                                                                                                                                                                                                                                                       | handle, metrics, avatar                                                                          | —                                                                                                              |
| polish                 | grain-overlay, vignette, shimmer-sweep, texture-mask-text                                                                                                                                                                                                                                                                                                                                   | intensity                                                                                        | —                                                                                                              |
| **asset-fusion (RWA)** | **annotation kit from `north-korea-locked-down`** — scribble-circle draw-on, pop-up pill + pointer, red-wash, scanline, corners, camera push; + `us-map-bubble` callouts/connectors                                                                                                                                                                                                         | asset, annotation position (`element_positions`), label, palette **eyedropper'd from the asset** | **NET-NEW (not in catalog): the affordance binding — asset geometry _becomes_ the chart axis (straw → gauge)** |

## Reuse mechanics

- `npx hyperframes add <block>` → source lands in `compositions/<block>.html`; inline it or reference via `data-composition-src`; customize content/data/palette/positions in place.
- Blocks ship at fixed canvases (1920×1080 / 1080×1920 / 1080×1080) — match or adapt.
- Blocks already follow the HF contract (paused timeline, seek) — keep it.

## Asset-fusion: borrow + net-new (the only real net-new IP)

Borrow `north-korea-locked-down`'s annotation _language_; the net-new is the RWA fusion _logic_ (see the RWA study):

1. Classify the data type; read the asset's **geometric affordance** — linearity → timeline/gauge, volume/texture → pie, height → bar, container → exploded view.
2. **`element_positions`** — measure the asset's feature (center / extent / safe-zones / avoid-zones). This is the reverse-engineer step (vision); in the prototype it's hand-estimated.
3. **Eyedropper palette** from the asset (never generic #FFF/#000).
4. **Two layers** — asset (z0, full-bleed) + data graphics fused to its geometry (z1+), anchored by `element_positions`; connectors/scribble physically tie the data to the asset; the asset stays visible.


<!-- ===== FILE: hyperframes/motion-graphics/categories/asset-fusion/module.md ===== -->

# asset-fusion — category module (search-driven · the net-new IP)

**A real asset's geometry _becomes_ the chart** — RWA diegetic fusion (the straw becomes a gauge; a glass's liquid becomes a pie). Not in any catalog; the genuinely net-new capability. ~5–8s.

## Source (Step 2)

Search or generate one **hero asset** with strong geometric affordance. `asset_needs`: `{ kind: image, query|generate, treatment: cutout|none }`. Freeze it project-local.

## Plan (Director Part 2) — the fusion logic

1. Classify the **data type** (temporal / quantitative / proportion / spatial).
2. Read the asset's **geometric affordance** — linearity → timeline/gauge · volume/texture → pie · height → bar · container → exploded view.
3. `element_positions`: **GROUND with the locate protocol — never eyeball pixel coords.** Read **`grounding/PROTOCOL.md`** and run the loop with `node grounding/locate.mjs` (`overlay` → read strips → `region` → read crop → `final` → **`mark` + verify**). Zero keys/deps assumed (node + ffmpeg only); the optional `auto` fast path exists only when `GEMINI_API_KEY` happens to be set. Why: eyeballing put rings off-subject (~16–24% center error on weak vision models); the grid loop pulls it to ~2–4% (measured E2E: eyeball 6.5% → protocol 2.3% avg center error, no case worse).
4. **Eyedropper palette** from the asset (never generic #FFF/#000).

## Highlight + circle recipe (the common case)

"Ring / spotlight object X in a real image" → use the drop-in template **`samples/asset-fusion/_ref-circle-highlight.html`**: set `CFG.box` (from the locate protocol), `CFG.label`, `CFG.asset`, EVEN `CFG.W/H`, `CFG.mode` (`full` = ring+connector+label+brackets+scanlines, `circle` = ring only). It computes the radial wash, the amber double over-stroke ring, connector, callout, and corner-bracket reticle from the box. The whole pipeline is: locate (PROTOCOL.md) → fill template → render.

## Render gotchas (codified — skipping these breaks the render)

- **EVEN width & height** — odd width _or height_ (e.g. 1400×933) → `ffmpeg` encode fails / distorts. Resize the asset/stage to even dims (1400×932).
- **`data-width`/`data-height` must be STATIC HTML attrs on the stage** — the renderer's StaticGuard reads them at compile time, before JS runs. Setting them via `setAttribute` is too late → render falls back to portrait 1080×1920 and distorts. (The circle-highlight template now hard-codes them; keep them equal to `CFG.W/H`.)
- **Draw-on (`stroke-dashoffset`) must be `autoAlpha:0`-gated** — `getTotalLength()` can read 0 before layout → dash disabled → a solid line shows at t=0. Gate every draw-on element with `autoAlpha:0` until it draws, and fall back `getTotalLength() || <const>`.
- **CSS var tween scope** — `gsap.to(":root", {"--x":..})` won't reach an element that has its own inline `--x`; tween the var on the element itself.
- **No camera push under a fixed overlay** — scaling the image while the ring/wash stay fixed drifts the target out of the ring. Either skip the push or scale the whole scene together.
- Lossless delivery: `--format mov` (ProRes); `mp4` is lossy.

## Vocabulary / leans on

- Borrow the annotation kit from registry **`north-korea-locked-down`** (hand-drawn scribble circle draw-on, pop-up label + pointer, editorial wash, camera push).
- Primitives: gauge fill / marker-rise along the affordance · connector (data → asset point) · diegetic chart fused to the asset's geometry.
- Adapt the diegetic chart to each asset's affordance (read the geometry, fuse the data into it).

## Build (reuse-first + hand-author the affordance)

**Two layers**: asset (z0, full-bleed) + data graphics (z1+) fused to its geometry, anchored by `element_positions`; connectors/scribble physically tie the data to the asset; asset stays visible. Reference impl: the prototype `fusion-demo/index-annotated.html` (straw → gauge + borrowed annotation kit).


<!-- ===== FILE: hyperframes/motion-graphics/categories/charts/module.md ===== -->

# charts — category module

Animated **data-viz** from data. Asset-free (the "input" is the data). "One chart, one message" for short durations.

Read [data in motion](../../../hyperframes-creative/references/data-in-motion.md) before planning or building. Apply its guidance to default chart choices; preserve a chart type explicitly requested by the user.

## Plan (Director)

`content`: `{ type: bar|line|pie|race|pct, data[], labels[], headline, axes: bool }`. For `race`, data must be cumulative/time-staged.

## Vocabulary / leans on

- Block: **`data-chart`** (animated **bar + line**, staggered reveal, value labels — proven: borrowed + customized + rendered to MP4 in the prototype `charts-demo`).
- Also in the registry: **`bar-chart-race`** — install it rather than hand-authoring a race.
- Gaps (hand-author): **pie / donut, ring/%** — no registry block covers these. Search first (`npx hyperframes catalog --query "pie chart reveal" --json`), then use SVG/CSS for data→geometry + GSAP for motion.
- Signature animations: bar stagger-grow · line `stroke-dashoffset` draw-on · pie radial sweep · ring fill · KPI count-up · race reorder.

## Build (reuse-first)

Reuse `data-chart`: `npx hyperframes add data-chart` → edit the data arrays + scales + headline/labels + palette in place (its data is baked in the script, not a `--variables` flag). Axes hidden by default; show muted only when magnitude is the message. Determinism: drive any animation from the seek clock, never wall-clock.

## Dashboard-skeleton variant

For a **product-dashboard** case: lay out a skeleton dashboard — a top bar with a **real test logo** (e.g. the hyperframes logo in `samples/_assets/`) + a title, then a grid of 3–4 **KPI cards** (each a `stat` count-up) + one `data-chart` panel. Reveal order: header/logo in → cards stagger in → the chart animates. Composes the `stat` + `charts` primitives inside a dashboard frame; the logo is a frozen project-local asset.


<!-- ===== FILE: hyperframes/motion-graphics/categories/kinetic-type/module.md ===== -->

# kinetic-type — category module

Text is the hero; typography + motion carry the message. Usually asset-free (`asset_needs: []`).

## Plan (Director)

- **Style first.** If the project has a **`design.md` / `frame.md`** (precedence: `frame.md` → `design.md` → `DESIGN.md`), READ it and use its **exact palette / fonts / constraints** — do not invent. No spec → pick a named style, or ask: mood + light/dark + any brand color/font. (Style is an input the case must exercise; the same shot in two `design.md`s should look different.)
- Segment the copy into scenes by meaning / breath (EN ~3–7 words; ZH ~4–12 chars). Tag each scene **Hook → Build → Punch → Resolve**.
- 1–2 `emphasis_words` per scene. Per scene: `emotion` + `motion` (free-form) + `beats`.

## Vocabulary

Motion primitives + registry blocks: **`references/motion-vocabulary.md`** (slide / scale / fade / blur / typewriter / word_reveal / wave / bounce / slam / scale_pulse / shake / glow / color_shift, plus the 18 `caption-*` blocks).

## Build (reuse-first)

- Prefer a **`caption-*` block** when one fits (`caption-kinetic-slam` / `caption-editorial-emphasis` / …): `npx hyperframes add` + set words / `emphasis_words` / palette / font.
- Else hand-author: one full-duration `.clip`; a `.group` per scene (flex-centered); words as spans; explicit `gsap.fromTo()` entrances per scene `motion`; emphasis words → `glow` / `scale_pulse` on the beat; seek-safe `autoAlpha` only on inner non-clip elements. Honor `references/builder-contract.md`.
- Reference impl: prototype `v0-text-motion-demo` + `pipeline-demo`.


<!-- ===== FILE: hyperframes/motion-graphics/categories/logo-reveal/module.md ===== -->

# logo-reveal — category module

A **logo sting / brand lockup**. The logo is user-supplied, or resolved for a known brand (`resolve --type logo --entity <brand>`); `asset_needs` = one logo `source`. ~3–5s. Often `export: alpha-overlay` (sting to drop on other footage).

## Plan (Director)

`content`: `{ logo: <asset path>, tagline, url }`. Envelope: brand palette (or eyedropper from the logo), elegant pacing.

## Vocabulary / leans on

- Block: **`logo-outro`** (piece-by-piece assembly + glow bloom + tagline fade + URL pill).
- Rules: `rules/svg-path-draw` (draw-on for vector logos) · `rules/scale-swap-transition` · `rules/3d-text-depth-layers`.
- Primitives: draw-on / mask-reveal / particle-assemble · `glow` bloom · `underline_sweep` · hold.

## Build (reuse-first)

Reuse `logo-outro` + swap logo / tagline / url / palette; **or** hand-author: place the logo at its hero frame (CSS), reveal via draw-on (SVG `stroke-dashoffset`) or mask/scale, add a glow bloom + accent underline sweep, hold. For an SVG logo, prefer draw-on; for a raster logo, mask/scale + glow. Transparent bg when exporting as an overlay.


<!-- ===== FILE: hyperframes/motion-graphics/categories/lower-thirds/module.md ===== -->

# lower-thirds — category module

<!-- registry-items: allow= -->

**The live search is the source of truth for what the registry has.** The table(s) below are a hand-maintained sample and under-cover by design: run `npx hyperframes catalog --query "<what you want>" --json` — it needs nothing installed — before concluding the registry lacks something. Item names here are checked against `registry/registry.json` by `bun run lint:skills`.

**Name/title bars, callouts, social overlays** — graphics meant to sit over other footage. Asset-free (+ optional logo). Usually `export: alpha-overlay` (transparent). ~3–6s (or loop/hold).

## Plan (Director)

`content`: `{ name, role, position (lower-left / lower-third / corner), brand_colors[] }`. Default `export: alpha-overlay`.

## Vocabulary / leans on

- Blocks: `caption-*` (pill-karaoke, neon-accent, editorial-emphasis) + registry **overlay** blocks (`instagram-follow`, `tiktok-follow`, `yt-lower-third`, `x-post`, `spotify-card`, `macos-notification`).
- Primitives: slide/wipe-in · bar reveal · `glow` · fade/slide-out.

## Build (reuse-first)

Reuse the closest overlay/caption block + set name / role / handle / brand colors / position; **or** hand-author a bar that wipes in (`scaleX` from 0, `transform-origin:left`) with text sliding up behind it, hold, slide out. **Transparent background** (`export: alpha-overlay` → `render --format webm/mov`) so it composites over footage. Keep it in the title-safe lower band.


<!-- ===== FILE: hyperframes/motion-graphics/categories/maps/module.md ===== -->

# maps — category module

Geographic motion: highlight regions, connect places, zoom to a location. **First decision: does the shot need a real basemap** (satellite/street/terrain imagery, globe, or zoom to a real address)? That picks the lane.

## Plan (Director)

Set `content.lane` first:

- **vector** (default) — stylized region shapes, no real imagery. Native + live in HF, cheap. `asset_needs: []`.
- **basemap** — needs real satellite/dark tiles, globe, or zoom-to-real-place. `asset_needs: [{ type: "map-bake", … }]`. **Bake the imagery in Source**: HF forbids render-time network and requires determinism, so live tiles (which re-fetch and can change per render) can't be the imagery layer — baking freezes it (and is smooth as a bonus). See Basemap lane + Determinism.

`content`: `{ lane, shot: highlight|flow|choropleth|labels|flag|pin-rollout|zoom-to, regions[], points[], basemap: satellite|dark, palette, headline, overlays: [label|pin|callout-card] }`.

`overlays` are independent of `shot` and work in both lanes. **`callout-card`** = a pinned card (flag chip + stat + progress bar) — this is the "documentary popup" (top #13); compose it on any zoom-to/highlight shot rather than treating it as its own shot.

## Vocabulary / leans on

**Vector lane** (D3 + TopoJSON — reuse the existing map family, don't duplicate):

- Reuse: `us-map` (+bubble/hex/flow), `world-map`, `spain-map`.
- **Hand-author** these (NOT in the catalog — build per the signatures below, don't expect an `add`): `geo-highlight` (N countries colored + labels + border pulse), `geo-flow` (world arcs / hub network), `flag-borders` (flag clipped to a country), `pin-rollout` (cities pulse in sequence + counter).
- Signature: country fill-in stagger · pin drop + pulse ring · arc `stroke-dashoffset` draw-on + flyer · choropleth color reveal · **viewBox** zoom.

**Basemap lane** (MapLibre, baked in Source — validated pipeline, `bake-basemap.mjs`, fully env-parametric — runs for any country, not just the prototypes):

- **Bake** `bake-basemap.mjs` (puppeteer + MapLibre; env-driven: `NAME STYLE COUNTRIES CENTER ZSTART ZEND PITCH BEARING FPS DUR`): drive the camera **zoom→hold** (`easeInOutCubic`) and **`await map.once('idle')` before every frame** so each frame has complete tiles (Remotion `delayRender` technique → no tile pop). The helper resolves Chrome itself, pins deps exactly, derives the overseas-territory filter per subject, and **fails loud on idle-timeout** (suspect frames → non-zero exit). _External deps: the pinned CDN libs (maplibre/topojson/world-atlas) + the Esri/CARTO tile endpoints are third-party — re-verify availability + ToS on any version bump._ `preserveDrawingBuffer:true`, `fadeDuration:0`. The helper then **encodes the frames to an all-intra MP4 itself** (`ffmpeg -framerate FPS -i f%04d.png -c:v libx264 -g 1 -pix_fmt yuv420p`) and writes everything to **`$OUT` (default `cwd`)**, not the skill dir → `<NAME>.mp4` + `<NAME>-coords.json`.
- **Export geo→screen** at the hold view: `map.project()` each requested country → `<NAME>-coords.json` = `{ view, countries: [{ name, color, d (SVG path), bbox, label }] }`. The camera holds static after the zoom, so these paths stay pixel-aligned. `label` is an **approximate** anchor (vertex-average of the mainland ring — for concave countries nudge per Legibility). Consume `coords.countries[i]`; the `smooth-frde2`/`smooth-flag` example dirs predate this helper and use a flat `{fr,de,…}` shape, so adapt their wiring.
- **Builder**: `<video>` basemap on track 0 + an **SVG overlay** that, during the hold, animates country **borders (`stroke-dashoffset` draw-on)** + **fills (colour-block reveal)** + labels/pins/cards — all geo-aligned via `coords.json`. This reproduces the Hera "satellite + animated coloured borders/callouts" look.
  - The same projected path also doubles as an SVG **`clipPath`**: clip a **flag (or any texture) into the real border** for _flag-in-borders_ — a richer fill than flat colour, over real map context (validated: France tricolor over a dark basemap, `smooth-flag`). Export the feature's screen **bbox** alongside its path so the flag stripes/texture can be sized to the country.
- **Stretch / data gaps** (extend `bake-basemap.mjs` as needed — the eval agents did): a **globe intro** ("start from the globe") = MapLibre `projection:{type:'globe'}` for the opening phase, easing to mercator at the target (the helper defaults to mercator). **Sub-national** regions (states/provinces) aren't in world-atlas (country-only) → use a Natural Earth **admin-1** TopoJSON, or project centroids as pins (`pin-rollout`).

## Build (reuse-first)

Vector: `npx hyperframes add <block>` → edit regions/data/palette in place. Basemap: baked `map.mp4` as track-0 `<video>`, bind overlays to anchors.

**Restraint (no cheese — this is the #1 way auto-built maps go wrong):** every animated element must serve the message — region, connector, label, pin, camera. **NO decorative ambient glows, background light blobs, floating particles, lens flares, or gratuitous bloom.** Motion = a continuous camera move (viewBox push/zoom) + purposeful, overlapping element reveals — not a light show. Palette: color must **carry meaning** — a data scale (choropleth), categorical fills that distinguish regions (political map), or 1–2 accents for the subjects (highlighted countries / route) over neutral everything-else. Don't add color as **decoration** (a country amber just for contrast, a glow for "energy"). The frame should read like a clean broadcast map, not a screensaver.

**Legibility (hard rule):** offset labels from the highlighted shape and from each other; clamp to the safe area; a callout pill must not sit on another label or a border (the eval surfaced a DE/PL "Oder–Neisse" pill overlapping the POLAND label). A key element stays readable ≥~0.3s.

**Attribution (hard rule):** real basemap imagery carries usage terms — bake a credit element into the composition whenever a basemap is on screen (Esri satellite → "Esri, Maxar, Earthstar Geographics"; CARTO → "© CARTO, © OpenStreetMap"). A small low-corner label (see `smooth-jp`). Non-negotiable for anything published.

**Determinism (hard rules — each one bit us in the prototypes):**

- Drive everything from the seek clock; **never `tl.call`** for stateful updates (counters, text) → proxy tween + `onUpdate` (tl.call freezes the timeline under HF seek).
- SVG zoom = animate **viewBox** (don't hand-compute group transform origins).
- Centered overlays (cards/labels using `transform: translate(-50%,…)` to center): animate **opacity only**, or wrap in an outer centered div — GSAP animating `y`/`scale` overwrites the whole transform and kills the centering.
- Country geometry: filter to the polygon(s) **in a lon/lat box around the subject** — world-atlas bundles overseas territories that blow up the bbox (France + Guiana). Keep near islands (Corsica, Sicily), drop far ones. (`bake-basemap.mjs` anchors on the vertex-richest polygon ± `KEEPMARGIN` — no continent-specific constant.)
- **Tile world-scale**: MapLibre's internal world width is `512·2^zoom` regardless of the raster `tileSize`. Esri/CARTO raster → `tileSize:256` (correct); a 512px / @2x / retina / vector source needs `tileSize:512` or every zoom level is off by one (this silently over-zoomed a bake once — France overflowed the frame top-to-bottom).
- **Antimeridian**: a feature crossing ±180° (Russia, Fiji, NZ) smears under per-vertex `map.project()`. `bake-basemap.mjs` **unwraps longitudes around the camera-center ref** before projecting, which handles it; it still warns if a feature spans >180° even after unwrap.
- **Smoothness = per-frame complete tiles + eased camera.** In the bake, `await map.once('idle')` before each screenshot (= Remotion `delayRender`) and ease the camera with `easeInOutCubic` (= interpolate+Easing). `preserveDrawingBuffer:true`, `fadeDuration:0`, large `maxTileCacheSize`.
- **Overlay alignment**: project feature borders at a **held** camera and only animate the overlay during the hold — a moving camera + a fixed projected path drift apart.
- **Pre-hold hidden state**: an overlay revealed _at_ the hold must be `gsap.set` to its hidden state at build time (`scaleX:0`, full `stroke-dashoffset`, `opacity:0`) — a bare `fromTo` does **not** apply its "from" until the tween starts, so the element otherwise shows at its natural (visible, mispositioned) state during the zoom-in.
- **Why bake at all** (the real reason — not just smoothness): baking freezes the imagery into **deterministic** pixels. Live raster tiles re-fetch every render and can change, and render-time network is forbidden. MapLibre _does_ render live in HF (just janky: tiles pop, deep zooms outrun loading); exposing the engine's per-frame `onBeforeCapture` hook (it exists — `frameCapture.ts:~1250`) would make live **smooth** — but it would **not** remove the need to freeze tiles for **determinism + offline reproducibility**. So `onBeforeCapture` would replace the _smoothness_ role of baking, not the _freeze_ role.

## Out of scope

3D photorealistic landmarks (Cesium territory) · per-country / per-template blocks (parametrize instead) · charts (→ `charts`). (In-engine _live_ MapLibre is possible but janky today — bake instead; revisit if the engine gains a per-frame ready hook.)

## Register

`director.md` classifier line (the lane fork) + `catalog-map.md` `maps/geo` row (add the basemap lane). Phase pipeline untouched.


<!-- ===== FILE: hyperframes/motion-graphics/categories/news/module.md ===== -->

# news — category module (search-driven)

Search a real news article → animate it as an **article-highlight** — a faithful HF port of the centered-emphasis technique. Signature motion: the article text is laid out at a **readable size (NOT zoomed)**, slides + fades up, then the **keyword is highlighted in place** — a marker band grows left→right behind it. No blow-up zoom. ~5–7s.

Two layouts share that one highlight core — pick by aspect + whether there's a logo / person to feature:

| Layout                    | Aspect     | Use when                                                        | Has                                                                        |
| ------------------------- | ---------- | --------------------------------------------------------------- | -------------------------------------------------------------------------- |
| **A · centered-emphasis** | 9:16 / 1:1 | text-only, social vertical                                      | kicker + one centered sentence + keyword highlight                         |
| **B · full article**      | 16:9       | there's a real **outlet logo** and/or a **person** in the story | logo + date + multi-line headline highlight + dek + outlet + person cutout |

## Source (Step 2)

RWA / web search (or `hyperframes capture`) → a real article. The Director extracts the **keyword** (1–2 words / a number / a name — the hook) and, for Layout B, also a **brand logo**, a **date**, and a **person photo**. `asset_needs: { kind: news|web|image, query }` — request the logo (`media-use resolve --type logo`, theSVG-first) and the person photo (Wikimedia) as separate asset queries. Run the person photo through `hyperframes remove-background <in> -o <out>.png` to get a transparent cutout.

## The highlight core (shared by both layouts) — the marker-band technique

The keyword highlight is a marker band grown L→R via `background-size` (NOT a `transform:scaleX` bar):

```css
.hl {
  --hlw: 0%;
  background-image: linear-gradient(var(--hl), var(--hl)); /* --hl: rgba(250,222,99,.6) */
  background-repeat: no-repeat;
  background-position: 0 72%;
  background-size: var(--hlw) 64%;
  box-decoration-break: clone;
  -webkit-box-decoration-break: clone;
}
```

`box-decoration-break:clone` makes the band **wrap across line breaks** seamlessly — a multi-word keyword spanning 2–3 lines still highlights continuously (the old `scaleX` bar could not). GSAP tweens the CSS var `--hlw` 0%→100%, **swept on AFTER the text settles — never pre-applied**. Optionally scale the duration with keyword length ~0.5–1.5s.

## Layout A — centered-emphasis (9:16, text-only) — Builder

1. **Lay out the key SENTENCE at a readable size — do NOT zoom.** Paper-light stage; an outlet `#kicker` (e.g. "BBC NEWS · TECHNOLOGY", brand accent) at top; the key sentence centered, serif, **~70–76px / 700 / line-height ~1.4**, `max-width ≈ 900`. The whole sentence stays legible; the keyword is emphasized _within_ it.
2. Wrap the keyword inline: `… raised <span class="hl" id="kw">$750M</span> at …`.
3. **Timeline** (seek-safe, paused): kicker fades+slides in → **sentence slides+fades up** (`set{autoAlpha:0,y:52}`→`to{autoAlpha:1,y:0,duration:0.8,ease:"power3.out"}`, no zoom) → **keyword highlight grows** (`--hlw 0→100%`, after the sentence settles) → gentle hold (`scale 1.012`).

**Reference:** `samples/news/_ref-centered-emphasis.html` (+ `news/v2-*`).

## Layout B — full article (16:9, logo + person) — Builder

The editorial article-card layout (logo top-left + date + big serif headline with a multi-line keyword highlight + dek + outlet bottom-left + a background-removed **person cutout** bottom-right). 1920×1080, paper-light gradient stage, Georgia serif.

1. **Logo** top-left (`#logo`, ~64px) — inline the outlet/brand SVG, `fill:currentColor`, set `color` to the mark's own hue (or near-black for a monochrome mark). **Date** below it (`#date`, ~30px, muted).
2. **Headline** (`#headline`, Georgia **96px / 700**, `width≈1080`, `line-height 1.16`) with the keyword wrapped in `<span class="hl" id="kw">` — the highlight band sweeps across **all wrapped lines** of the phrase.
3. **Dek** (`#dek`, Helvetica ~38px gray) under the headline; **outlet** (`#outlet`, Georgia bold ~50px) bottom-left.
4. **Person cutout** (`#subject`, the bg-removed PNG, `height≈860`, `right:40; bottom:0`, `drop-shadow`) — **slides up from bottom-right** as the hero beat.
5. **Timeline** (seek-safe, paused): logo `back.out` @0.15 → date @0.4 → **subject slides up** (`set{autoAlpha:0,x:90,y:60}`→`to{autoAlpha:1,x:0,y:0,duration:0.85,ease:"power3.out"}`) @0.45 → headline @0.7 → dek @1.5 → outlet @1.9 → **keyword highlight** (`--hlw 0→100%`, `duration:0.8`) @2.2. duration ~6.5s.

**Reference:** `samples/news/_ref-article-layout.html` (a real article rendered with a real outlet logo + a background-removed person + a real story).

## Critical

Highlight is **grown in place, swept on AFTER the text — never pre-applied**. The text **stays readable — do NOT zoom the keyword to fill the frame** (team feedback 2026-06-09: zoom loses context and reads wrong; the technique never zooms — it presents the text and highlights the word). For Layout B, the person MUST be a `remove-background` cutout (no rectangular photo box). Deterministic; honor `references/builder-contract.md`.


<!-- ===== FILE: hyperframes/motion-graphics/categories/stat/module.md ===== -->

# stat — category module

A single **hero number** reveal. Asset-free (the "input" is the number). ~4–6s.

Read [data in motion](../../../hyperframes-creative/references/data-in-motion.md) before planning or building the number reveal.

## Plan (Director)

`content`: `{ value, prefix ($), suffix (% / x / K-M-B), label, ring: bool }`. Envelope: bold display font, restrained palette + one accent.

## Vocabulary / leans on

- Block: **`apple-money-count`** (finance-flavoured: $ counter + green flash + money burst + SFX) when it fits; otherwise hand-author.
- Rules: `hyperframes-animation/rules/{counting-dynamic-scale, stat-bars-and-fills}`.
- Primitives: `count_up` (odometer) · `scale_pop` · `ring_fill` (arc) · `label_stagger` (after value) · `hold`.

## Build (reuse-first)

Reuse `apple-money-count` + set target / prefix / suffix / label / palette; **or** hand-author per the proven prototype `v0-stat-motion-demo`:

- **count-up is timeline-driven** — tween a proxy `{v:0}→target` with `onUpdate` writing the formatted number (seek-safe; never setInterval/wall-clock).
- `font-variant-numeric: tabular-nums`; decelerating ease; ~1.2–1.6s then **hold** the final value.
- ring/arc via `stroke-dashoffset`, finishing in sync with the count-up; label fades in **after** the number lands (value → meaning).


<!-- ===== FILE: hyperframes/motion-graphics/categories/tweet/module.md ===== -->

# tweet — category module (search-driven)

**Search a tweet → animate the tweet card.** Grounded in a real post (RWA). ~4–8s.

## Source (Step 2)

RWA `search_tweets` (specific query, or a given tweet URL/id) → tweet: author, handle, avatar, text, timestamp, metrics (likes/reposts). `asset_needs`: `{ kind: tweet, query|source, treatment: none }`. Freeze the avatar + any embedded media.

## Vocabulary / leans on

- Block: registry **`x-post`** (animated X/Twitter post card overlay with engagement metrics) — reuse it directly.
- Primitives: card slide/scale-in · text type-on / line reveal · avatar pop · metrics **count-up** · optional emphasis on a keyword.

## Build (reuse-first)

`npx hyperframes add x-post` → fill author / handle / avatar / text / metrics from the resolved tweet; animate the card in, type-on the text (or line-by-line reveal), count-up the metrics. Frozen project-local avatar/media (never a remote URL). `export: alpha-overlay` if it's meant to sit over other footage.


<!-- ===== FILE: hyperframes/motion-graphics/categories/webpage/module.md ===== -->

# webpage — category module (search-driven)

**Animate a webpage / link** (the "website animation" use case). Search-driven: the user gives or names a URL → fetch/capture it → animate it (scroll-through, UI reveal, cursor demo, region callouts). Distinct from captioning an existing _video file_ (that's `/embedded-captions`) and from a narrated video _of_ a site (that's a `/product-launch-video` site-tour ask); here the source is a _web page_ and the output is a short, unnarrated highlight shot.

## Source (Step 2)

Fetch the page via `hyperframes capture --json` (DOM + screenshots) or a provided screenshot → frozen project-local image(s)/DOM. `asset_needs`: `{ kind: web, source: <url>, treatment: none }`.

Inspect the capture result before building. If `BLOCKED.md` exists, JSON reports `ok: false`, or the
command exits non-zero, stop the URL-capture path and report the reason. Continue with a provided
screenshot only when it was an explicit source from the user (or the user explicitly chooses it
after the failure). Do not animate a blocked partial capture, invent missing DOM, or eyeball element
coordinates from protection/challenge pages.

This web need cannot use the generic asset-free fallback: it requires a usable captured screenshot
or DOM, or a provided screenshot explicitly selected by the user. If none is available, stop.

## Vocabulary / leans on

- Rules: `hyperframes-animation/rules/{3d-page-scroll, demo-page-scroll-spotlight, cursor-click-ripple, coordinate-target-zoom, viewport-change}`.
- Primitives: scroll pan · spotlight/dim · cursor move + click-ripple · zoom-to-region · callout pin + label.

## Build (reuse-first)

Place the captured page as the base layer; animate a **scroll-through** (translateY over the page height), **spotlight** key regions (dim + highlight), a **cursor** that moves and clicks (ripple), **zoom** to a coordinate, and **callout** pins/labels anchored to page regions. Honor `builder-contract.md`.

**Two rules that match the news article-highlight (see `../news/module.md`):**

- **Highlights are swept/animated ON, never pre-applied** — a spotlight box wipes in (`scaleX 0→1`), a marker sweeps a region, a callout pops _after_ the zoom lands; the page never starts pre-annotated.
- **Anchor to REAL element positions** — `hyperframes capture` gives the page HTML/DOM, so measure the target element (`getBoundingClientRect` → stage-local) and zoom/highlight it exactly, step-by-step (the "highlight a real element" technique). Don't eyeball coords.


<!-- ===== FILE: hyperframes/motion-graphics/grounding/PROTOCOL.md ===== -->

# locate — find "X" in an image (no detector API assumed)

The single contract every consumer (asset-fusion ring, webpage highlight, future
explainer/recut overlays) uses:

```
locate(image, target-description) → { box: [x0,y0,x1,y1], center: [cx,cy] }   # normalized 0..1
```

## Why this exists

Author models are unreliable at **regressing pixel coordinates** on a cluttered
full image (measured: weak vision models ~16–24% center error → rings land off-target)
but reliable at **picking a numbered strip** (~3–4% with the loop below). So:
never eyeball coordinates; localize by discrete choice. (RSVP, ACL 2025.)

## Routing — pick the cheapest path that's actually available

1. **A strong detector is available** (e.g. `GEMINI_API_KEY` in env) →
   `node grounding/locate.mjs auto <img> "<target>"` — one call, done.
   **Never assume the key exists.** No key → path 2.
2. **No detector (the normal case)** → YOU are the localizer; run the grid loop.

## The grid loop (you read images between steps)

```
node grounding/locate.mjs overlay <img> --out /tmp/g
  → READ /tmp/g/gv.png (vertical strips 1-9) and gh.png (horizontal 1-9);
    decide which strip numbers the target spans (list EVERY strip it touches).
node grounding/locate.mjs region <img> --vids 4,5 --hids 6,7 --out /tmp/g
  → READ /tmp/g/gc.png (the region cropped + upscaled, finer 6×6 grid);
    pick the finer strips. (Pick strips again — do NOT switch to estimating
    coordinates; discrete choice is the whole point, at BOTH stages.)
node grounding/locate.mjs final <img> --region <from step 2> --vids 3,4 --hids 3,4
  → the final {box, center}.
node grounding/locate.mjs mark <img> --box <final box> --out /tmp/g/check.png
  → VERIFY: READ check.png. Red box ON the target → done. Off → redo
    region/final with corrected strips (you now know which direction). Never
    skip this step; it converts silent misses into one cheap retry.
```

## Ambiguity — resolve BEFORE localizing

If the target description can match several instances ("a drum" when the scene
has five), no geometry will save you. First make the reference unique
("the right-most drum", "the drum on the front boat"), asking the user if
needed — then run the loop.

## Degradation path (if locate.mjs itself is unavailable)

The idea is 5 lines — reproduce it with any image tool:
draw a numbered 9×9 grid → pick the strips the target spans → crop that region
(+pad ~0.4 strip) and upscale → draw a finer 6×6 grid → pick again → map back
(`global = region_origin + local × region_size`) → draw the box and LOOK at it.

## Notes

- Geometry is frozen in `locate.mjs` (node + ffmpeg, zero npm deps — both
  already required by hyperframes). Don't re-implement it ad hoc; the measured
  accuracy holds for THIS implementation.
- Consumers: `samples/asset-fusion/_ref-circle-highlight.html` takes `CFG.box`
  directly from `final`/`auto` output.
- Measured end-to-end (same agent, same template, only the localization step
  differs): eyeballing 6.5% avg center error → this protocol 2.3%, no case worse.


<!-- ===== FILE: hyperframes/motion-graphics/phases/source/guide.md ===== -->

# source phase — asset sourcing (asset-first)

Runs **only when `shot-plan.json.asset_needs` is non-empty** (the form categories never reach here). Sources each needed asset → a **frozen project-local path** + a ledger (`assets/index.md`). Uses `/media-use` (capture / asset prep) plus, **when an external asset-search skill such as media-use is installed**, its `resolve` step. If no such search capability is available, it **degrades to asset-free** (see below).

## Per asset_need

- `image / icon / logo / svg` → media-use `resolve`: **search** (asset_scout: Google Images / SerpAPI + Noun Project), **generate** (image model), or **user-supplied** (logo). Optional `treatment`: cutout (remove-bg) / recolor / vectorize.
- `news / web / tweet` → **RWA-style search** (media-use's documented lineage — `media-use/references/search-strategy.md` traces `resolve` to the RWA subagent). Two-pole queries: **atomic** (1–3 words, composable) or **specific** (5–15 words: a news event / tweet); never the middle. A failed specific query is dropped, not broadened.

## Steps

1. Read `asset_needs` from `shot-plan.json`.
2. For each: **analyze → search → review (use/maybe/reject — selection is the hard part; do NOT take the first/generated result) → freeze** the kept asset into `assets/` (rehost remote URLs).
3. Write `assets/index.md` — agent-readable ledger: `role → frozen path + provenance`.
4. For `asset-fusion`: also capture the asset's measurable geometry (so Director Part 2 can set `element_positions`) + an eyedropper palette.

## Degrade gracefully

If a provider / search is unavailable, mark the need unmet in `context.log`; the category falls back to asset-free where possible (e.g. `news` → typographic headline without the sourced image).

> Illustrative: `(cd "$PROJECT_DIR" && node <SKILL_DIR>/phases/source/resolve.mjs --plan ./shot-plan.json --out ./assets)` — or drive media-use's `resolve` procedure directly.


<!-- ===== FILE: hyperframes/motion-graphics/references/builder-contract.md ===== -->

# Builder contract — composition rules (detail behind agents/builder.md)

## Root must be sized

Root `#stage` (`data-composition-id`) needs `position: relative; width: <W>px; height: <H>px`. Without a resolved height, flex children collapse to ~0 and content piles into the top-left. Automated gates may miss it, so inspect proof snapshots.

## Layout before animation

1. Identify the **hero frame** (the moment most elements are visible) → build THAT in static CSS first, no GSAP.
2. `.scene-content` fills the scene with padding, not offsets:
   ```css
   display: flex;
   flex-direction: column;
   justify-content: center;
   width: 100%;
   height: 100%;
   padding: 120px 160px;
   gap: 24px;
   box-sizing: border-box;
   ```
   Never `position:absolute; top:Npx` on a content container (it overflows). Reserve absolute for decoratives. Keep ≥80px padding (title-safe margin).
3. **Entrances**: use `gsap.from()` only for a non-clip element active from `t=0`. Inside `.clip`, in sub-compositions, and for later entrances, use explicit `fromTo()`. The CSS position is ground truth; the tween is the journey to it.
4. **Exits**: only the final scene animates elements out; between scenes the transition IS the exit.

## Timeline / clip contract

- ONE `gsap.timeline({paused:true})` on `window.__timelines["<id>"]`; `tl.seek(0)`; never `tl.play()`.
- Timed elements: `class="clip"` + `data-start`/`data-duration`/`data-track-index` + a stable `id`. Timeline-driven groups inside one full-duration clip don't each need timing attrs.
- Deterministic only — no `Date.now()` / `Math.random()` / network. Count-ups tween a proxy object via `onUpdate` (seek-safe), never a wall-clock counter.

## Correctness

- **Seek-safe reveal of delayed elements**: on a non-clip element or wrapper inside a clip, use one registered timeline `fromTo()` with an explicit `{ autoAlpha: 0 }` start and `{ autoAlpha: 1, ... }` end. Do not page-load `gsap.set()` a later `.clip`, and never target `.clip` visibility; the framework owns its lifecycle. _(Eval finding.)_
- **Count-ups** tween a proxy via `onUpdate`; they only render when the host advances the timeline **with events enabled** (`tl.time()` / non-suppressed seek). A bare `seek(t, true)` freezes them at 0 — the HF render host must seek with events on. _(Eval finding.)_
- Clamp at tween bounds; don't let a spring overshoot past a held value.
- Allowed eases: `power1–4`, `back`, `bounce`, `circ`, `elastic`, `expo`, `sine` (`.in/.out/.inOut`).
- One motif per scene. Run `hyperframes check`; mark intentional overflow `data-layout-allow-overflow="true"`.
- **Palette discipline**: define all colors in one `palette` object / CSS custom properties — no inline hex scattered through the markup (for `asset-fusion`, eyedropper the palette from the asset).


<!-- ===== FILE: hyperframes/motion-graphics/references/motion-vocabulary.md ===== -->

# text module · motion vocabulary (primitive → GSAP)

<!-- registry-items: allow= -->

**The live search is the source of truth for what the registry has.** The table(s) below are a hand-maintained sample and under-cover by design: run `npx hyperframes catalog --query "<what you want>" --json` — it needs nothing installed — before concluding the registry lacks something. Item names here are checked against `registry/registry.json` by `bun run lint:skills`.

Named primitives the Director references in `motion` strings and the Builder implements. `code_hint`s are framework-neutral physics; the GSAP recipe is the HF implementation. Prefer an HF **registry component** (bottom) when one fits — don't reinvent.

## Entry

| primitive                     | GSAP recipe (into CSS end-state)                               | suits                     |
| ----------------------------- | -------------------------------------------------------------- | ------------------------- |
| `slide_bottom/top/left/right` | `from({ y:±150 / x:±200, opacity:0, ease:"power4.out" })`      | calm, build, professional |
| `scale_grow`                  | `from({ scale:0, opacity:0, duration:.6, ease:"power2.out" })` | calm, gentle              |
| `scale_punch`                 | `from({ scale:.6, opacity:0, ease:"back.out(2.2)" })`          | impact, energetic         |
| `fade_in`                     | `from({ opacity:0, duration:.4 })`                             | subtle                    |
| `fade_blur`                   | `from({ opacity:0, filter:"blur(14px)" })`                     | cinematic, dreamy         |
| `typewriter`                  | reveal via clip/`SplitText` width step                         | technical, narrative      |
| `word_reveal`                 | per-word `from({opacity:0,y:..}, stagger:.1)`                  | storytelling              |
| `wave`                        | per-letter `from({y:..}, stagger:{each:.04})`                  | flowing, musical          |
| `bounce_in`                   | `from({y:-120}, ease:"bounce.out")`                            | playful                   |
| `slam`                        | `from({ y:-300, ease:"power4.out" })` + shake on land          | impact, heavy             |

## Emphasis (in place, often on a beat)

| primitive     | GSAP recipe                                                          | suits              |
| ------------- | -------------------------------------------------------------------- | ------------------ |
| `scale_pulse` | `to({ scale:1.12, yoyo:true, repeat:1, ease:"sine.inOut" })` at beat | rhythmic, peak     |
| `shake`       | `to({ keyframes:[{x:-9},{x:9},{x:0}], ease:"none" })`                | urgent, intense    |
| `glow`        | `to({ textShadow:"0 0 46px <ink/accent>", yoyo:true, repeat:1 })`    | important, magical |
| `color_shift` | `to({ color:"<accent>" })` (or accent on the word in CSS)            | dynamic            |

## Exit

| primitive   | GSAP recipe                                        | suits      |
| ----------- | -------------------------------------------------- | ---------- |
| `fade_out`  | `to({ opacity:0, duration:.4, ease:"power2.in" })` | ending     |
| `slide_out` | `to({ y/x: off, opacity:0, ease:"power2.in" })`    | transition |
| `scale_out` | `to({ scale:1.06, opacity:0, ease:"power2.in" })`  | transition |

## Accent graphics (not text)

`underline_sweep` `fromTo({scaleX:0},{scaleX:1}, transformOrigin:"left center")` · `bar_wipe` · `hold_breath` `to({scale:1.015, ease:"sine.inOut"})`.

## Prefer HF registry components when they fit

`caption-kinetic-slam` · `caption-editorial-emphasis` · `caption-neon-glow` · `caption-glitch-rgb` · `caption-particle-burst` · `caption-weight-shift` · `caption-matrix-decode` · `caption-pill-karaoke` · `shimmer-sweep`. These are pre-built, in-ecosystem, and already render-tested — the Builder should reach for them before hand-rolling an equivalent.


<!-- ===== FILE: hyperframes/motion-graphics/references/shot-plan-ir.md ===== -->

# shot-plan IR

The single contract between Director and Builder. One file: `PROJECT_DIR/shot-plan.json`.

```jsonc
{
  // ── envelope (every category) ──
  "category": "kinetic-type | stat | charts | logo-reveal | lower-thirds | webpage | news | tweet | asset-fusion",
  "duration_s": 6,
  "fps": 30,
  "canvas": { "w": 1080, "h": 1920, "aspect": "9:16" },
  "style": "free-form visual direction (mood / energy / reference)",
  "palette": ["#…"], // or "derive-from-asset"
  "font": "<HF embed-list font>",
  "beats": [12, 37], // optional accent frames/seconds
  "export": "mp4", // or "alpha-overlay" (transparent webm/mov)

  // ── sourcing seam (Director Part 1) — [] means skip the source phase ──
  "asset_needs": [
    {
      "role": "hero",
      "kind": "image|icon|logo|svg|news|web|tweet",
      "query": "…",
      "source": "…",
      "treatment": "cutout|recolor|vectorize|none",
    },
  ],

  // ── build directive (Director Part 2, reuse-first) ──
  "block": "<catalog block id, e.g. data-chart | caption-kinetic-slam>", // optional
  "customize": {
    /* what to change on the block: data, text, palette, positions */
  },

  // ── category-specific content ──
  "content": {
    /* shape varies by category, below */
  },
}
```

**Per-category `content` shapes:**

- `kinetic-type` → `scenes[]` `{ id, start, end, text, emphasis_words[], emotion, motion, beats[] }`
- `stat` → `{ value, prefix, suffix, label, ring: bool }`
- `charts` → `{ type: bar|line|pie|race|pct, data[], labels[], headline, axes: bool }`
- `logo-reveal` → `{ logo: <asset path>, tagline, url }`
- `lower-thirds` → `{ name, role, position, brand_colors[] }`
- `webpage` → `{ url, capture, highlights: [ { selector|region, label } ] }` (step-highlight a real captured page)
- `news` → `{ outlet, headline, body, keyword, layout: A|B, logo?, date?, subject? }` (article-highlight: lay text out readable — **no zoom** — then sweep a marker band over the keyword in place. Layout **A** = centered-emphasis 9:16 text-only; **B** = full article 16:9 with `logo` + `date` + `subject` (a person photo → `remove-background` cutout))
- `tweet` → `{ author, handle, avatar, text, metrics }`
- `asset-fusion` → `{ data_type, asset: <path>, affordance, element_positions: {center, extent, safe[], avoid[]}, derived_palette[], connectors[] }`

**Invariants:** `scenes` (if present) partition `[0, duration_s]` with no gaps/overlaps · empty `asset_needs` ⇒ Step 2 (source) is skipped · a named `block` ⇒ the Builder reuses + customizes it rather than hand-authoring.
