

<!-- ===== FILE: hyperframes/slideshow/GUIDE.md ===== -->

---
name: slideshow
description: >
  Author a HyperFrames slideshow — a presentation, pitch deck, or interactive
  deck with discrete slides, fragment reveals, branching, hotspot navigation,
  and built-in presenter mode with speaker notes; also converts an existing
  page into a deck. Output is a navigable deck, not a rendered MP4. If the
  user didn't explicitly ask for a slideshow, confirm before authoring.
  Unclear → /hyperframes.
---

**Plugin installs:** Before setup or freshness commands, follow [plugin execution rules](../hyperframes/references/plugin-installation.md) when this skill is inside a HyperFrames plugin. Standalone installs keep the update instructions below.

> **First, keep this skill fresh — confirm with the user before running:** `npx hyperframes skills update slideshow`. A fast no-op when everything is current; otherwise it refreshes this skill plus the core domain skills it depends on before you rely on them.

> **figma source**: If the deck's content or storyboard comes from a figma.com URL, run `/figma` first — asset export, brand tokens, and storyboard reconstruction if the source is a strip of scene frames — then build from its output. Don't drive Figma via raw MCP tools directly: that skips SVG sanitization, `.media/manifest.jsonl` provenance, and brand-token `var()` binding, so a later brand change can't propagate without a full re-import.

# Slideshow authoring contract

A HyperFrames slideshow is a normal HyperFrames composition — scenes, clips, GSAP timelines — with one extra ingredient: a **JSON island** that declares which scenes are slides and how they connect. The player's `SlideshowController` reads the island and turns the continuous GSAP timeline into a discrete, navigable deck.

**Read `/hyperframes-core` first** for the base composition contract (clips, tracks, `data-*` attributes, determinism rules). This skill covers only what is new: the island schema, slide writing rules, fragments, branching, validation, and the wrapping component.

## Output — a navigable deck, not a linear MP4

A slideshow's output is the **running deck**: serve it with `hyperframes present <project-dir>` (or Studio present mode) — the player's `SlideshowController` reads the island and drives navigation, fragments, branching, and presenter mode. See **Presenting and handoff** below.

**Do not `hyperframes render` a slideshow into a single MP4.** A deck is authored as several top-level scene compositions (one `data-composition-id` per slide) with **no master-root composition** wrapping them, so `render` resolves only the **first** composition and emits a **silently truncated** MP4 (e.g. 6s of a 40-second deck). A linear main-line export (main slides only, branch sequences excluded) is **deferred** — until it ships, the supported outputs are the live `present` deck and per-slide `snapshot` stills. If a user needs a linear MP4 today, surface this limitation rather than pointing `render` at the deck.

## Intent confirmation

If the user explicitly asks for a slideshow, slide show, or HyperFrames slideshow, proceed with this skill. When the request arrived through `/hyperframes`, the intent layer's triage owns this confirmation — routed here means already confirmed, so don't re-ask; the layer's run-shape questions don't apply (the deliverable is a deck, not a rendered video). A `BRIEF.md`, when present, carries the confirmed intent — read it.

If the skill triggered from an adjacent request such as "presentation", "pitch deck", "deck", "interactive deck", or "convert this page", pause before authoring and frame the choice before asking for confirmation. Briefly explain that a HyperFrames slideshow means a runnable deck with discrete slides, built-in navigation and presenter mode, editable speaker notes, shared media handling, and validation before handoff. For source-page conversions, also mention that the goal is to preserve the original page's visual design, interactions, motion, and media behavior while translating page movement into slide-to-slide transitions.

Then ask a short confirmation question:

> Do you want this as a HyperFrames slideshow?

Use a yes/no choice UI when the environment provides one; otherwise ask the question in plain text.

Do not implement the slideshow until the user says yes. If they say no, stop using this skill — read `/hyperframes` and let the intent layer re-route. This confirmation is a **routing decision**, not a preference gate — per `../hyperframes/references/brief-contract.md` § 1 it survives autonomous mode ("surprise me" does not skip it): building the wrong deliverable type is a quality failure, not a creative call.

---

## The two pieces

### 1. Scenes — declared the normal way

Every slide is backed by a scene. Declare scenes with `data-composition-id`, `data-start`, `data-duration`, and `data-label`:

```html
<div
  data-composition-id="problem"
  data-start="0"
  data-duration="8"
  data-label="The problem"
  data-width="1920"
  data-height="1080"
>
  <!-- clips go here -->
</div>
```

Branch slides (reachable only via a hotspot, excluded from the main line) are declared exactly the same way — they just appear only in a `slideSequences` entry in the island, not in the main `slides` array.

### 2. The JSON island — one script block per composition

Add exactly one `<script type="application/hyperframes-slideshow+json">` block to the composition HTML. It holds all slideshow metadata:

```html
<script type="application/hyperframes-slideshow+json">
  {
    "slides": [...],
    "slideSequences": [...]
  }
</script>
```

The island is the single source of truth for slide order, notes, fragment hold-points, hotspots, and branch sequences. Keep it near the top of the `<body>`, before the scene divs, so it is easy to find.

Do not hide the slideshow manifest behind an alternate `<script type="application/json">` block plus runtime code that creates the island. The `present` command reads the composition HTML statically and expects the real `application/hyperframes-slideshow+json` island to already be present.

---

## Schema

### `SlideshowManifest` (the top-level island object)

```json
{
  "slides": [
    /* SlideRef[] — the main line, in order */
  ],
  "slideSequences": [
    /* SlideSequence[] — off-line branch sequences */
  ]
}
```

### `SlideRef`

```json
{
  "sceneId": "problem",
  "notes": "Lead with the pain, not the company.",
  "fragments": [3.5, 5.2, 7.0],
  "hotspots": [
    /* SlideHotspot[] */
  ],

  "ttsScript": null,
  "ttsAudioUrl": null,
  "ttsDurationMs": null
}
```

| Field                                       | Required | Notes                                                                                                                                                   |
| ------------------------------------------- | -------- | ------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `sceneId`                                   | yes      | Must match a scene's `data-composition-id` exactly (or provide explicit `startTime`/`endTime`). The lint rule resolves scenes by `data-composition-id`. |
| `notes`                                     | no       | Presenter-only text. Never shown to the audience.                                                                                                       |
| `fragments`                                 | no       | Array of times (seconds) within the slide's `[start, end]` range — see Fragments below.                                                                 |
| `hotspots`                                  | no       | Interactive overlays that trigger a branch — see Branching below.                                                                                       |
| `startTime`                                 | no       | Optional. Override the matched scene's time bounds; defaults to the scene's start/end.                                                                  |
| `endTime`                                   | no       | Optional. Override the matched scene's time bounds; defaults to the scene's start/end.                                                                  |
| `ttsScript`, `ttsAudioUrl`, `ttsDurationMs` | no       | **Reserved.** Schema fields exist but TTS playback is not yet wired. Omit unless you are pre-populating for a future build.                             |

### `SlideHotspot`

```json
{
  "id": "h1",
  "label": "How did we calculate this?",
  "target": "market-deep-dive",
  "region": { "x": 60, "y": 10, "w": 35, "h": 20 }
}
```

| Field    | Required | Notes                                                                                                                           |
| -------- | -------- | ------------------------------------------------------------------------------------------------------------------------------- |
| `id`     | yes      | Unique within the slide.                                                                                                        |
| `label`  | yes      | Tooltip / button text shown to the audience.                                                                                    |
| `target` | yes      | Must match a `SlideSequence.id` in `slideSequences`.                                                                            |
| `region` | no       | Percentage-of-slide bounding box: `{x, y, w, h}` in `0–100`. Omit to render the hotspot as a full-slide labeled button instead. |

### `SlideSequence`

```json
{
  "id": "market-deep-dive",
  "label": "Market sizing methodology",
  "slides": [{ "sceneId": "mkt-1" }, { "sceneId": "mkt-2" }]
}
```

`slides` inside a sequence uses the same `SlideRef` shape as the main line. Fragments and nested hotspots are allowed.

---

## Slide writing rules

These are hard constraints, not suggestions. A slide that violates them will be outright replaced when a reviewer sees it.

- **Headline is a complete-sentence claim, not a label.** Write "SMBs spend 14 hours/week on manual scheduling" not "Scheduling problem". The sentence should stand alone if the visual is ignored.
- **One idea + one visual per slide.** If you are tempted to add a second bullet cluster or a second chart, split the slide.
- **Lead with the punchline.** The strongest point goes first — on the slide and in the deck order. Investors read left-to-right, top-to-bottom, and they stop.
- **Bottom-up market sizing only.** Never write "$50B TAM" without showing the math. Build from unit economics up: accounts × ACV, or transactions × take-rate.
- **Font minimum 30pt equivalent.** At 1920×1080, a headline is 72–96px; body copy is 48px. Never go below 40px for any text the audience must read.
- **Search the live catalog before hand-building any named visual.** For every look, effect, chart, treatment or transition a slide needs — "CRT scanlines", "glitch", "bar chart race", "shimmer sweep", "terminal window" — run `npx hyperframes catalog --query "<the visual, in plain English>" --json` and read the top results before you author the slide's clips. The search needs **nothing installed**: no project, no prior `add`, no account. It ranks the whole hosted registry (~400 blocks and components) from any directory. `npx hyperframes add <name>` drops the block's source into the deck, where you customize it in place. This applies with extra force when porting a source page: a real block beats the simplified approximation the porting rules below forbid.

## Porting source pages

When converting an existing page into a slideshow, source fidelity is part of the contract. Do not replace source-specific widgets with simplified approximations unless the user explicitly asks for a redesign.

- Preserve the original page's visual design, motion language, interactive behavior, media behavior, and presentation affordances as closely as practical. When the slideshow system supports presenter mode, include speaker notes using the shared editable-notes behavior rather than a deck-specific implementation.
- Port mechanical visuals from the source DOM/CSS/JS as exactly as practical: custom players, canvas visualizers, timelines, playheads, stems, expanding circles, hover states, and other interactive details should survive the conversion.
- Treat native `<video>` / `<audio>` elements as the source of truth for any custom media chrome, canvas visualizer, waveform, beat grid, or playhead. Wire the source's media events (`play`, `pause`, `timeupdate`, `seeking`, `seeked`, `ended`, `ratechange`, `volumechange`) and derive visual state from `media.currentTime`; do not run a separate timer that can drift away from actual playback.
- Every copied `<video>` or `<audio>` with `src` must have HyperFrames timing attributes before lint: `data-start` and `data-duration`, plus `data-has-audio="true"` when audible native audio should be preserved. Use the scene's time range for slide-specific media; for user-controlled evidence videos that may be played from multiple focused slides, use a deck-wide range. Do not leave `preload="none"` on media; use `metadata` or `auto`.
- Resolve source font tokens before validation. If preserving custom source fonts, add `@font-face` rules for local/captured font files. If using system fallbacks, replace tokenized declarations such as `font-family: var(--f-body)` with concrete render-safe stacks such as `system-ui, sans-serif` or `ui-monospace, monospace`; do not leave `var(...)` as the font family value.
- Audit the source for atypical page movement, especially behavior driven by scroll, wheel, touch, hash state, resize, or a requestAnimationFrame loop. Treat fixed viewports with translated/scaled "world" layers, parallax, pinned panels, horizontal scrollers, scroll-scrubbed timelines, section snapping, and zoom-to-element cameras as source behavior. Scroll is often the source's transition trigger, so preserve the transition by extracting its progress stops, easing, and camera/focus states, then re-host that motion on slideshow navigation through timeline positions, fragments, or a reusable player/harness hook. Standalone wrappers that jump to slide hold-points still need an explicit navigation-camera transition hook; computing per-slide camera transforms is not enough. Do not simulate a literal page-scroll-down transition inside the slide; the viewer should feel camera travel/zoom from one focal point to another, not see a webpage being scrolled. Keep each slide-to-slide camera move continuous: avoid intermediate route stops that reverse x/y direction or zoom unless the source visibly does that at the same boundary. A transition that darts around before landing is worse than a simpler direct focal move.
- Preserve the source's media crop semantics. Treat screenshots, tweets/social posts, product UI captures, charts, docs, code, leaderboards, and any image with readable text as content evidence, not decorative media: use the source aspect ratio (`height: auto`) or `object-fit: contain` inside a stable frame. Use `object-fit: cover` only when the source did, or for intentionally decorative/background/cinematic thumbnails. After fitting these captures into a slide, inspect all four edges for truncated text, logos, controls, or captions; a visible crop on meaningful content is a bug unless the source itself cropped it.
- If a behavior is generic to slideshows, put it in the player/controller or in a reusable skill snippet. Do not solve it with one-off deck scripts.
- Stacked scene frames must never block interaction on the active slide. Hidden frames need both visual hiding and event gating:

```css
.scene-frame {
  opacity: 0;
  visibility: hidden;
  pointer-events: none;
}

.scene-frame.is-active {
  opacity: 1;
  visibility: visible;
  pointer-events: auto;
}
```

If visibility is driven imperatively, set all three properties (`opacity`, `visibility`, and `pointerEvents`) in the visibility controller. `opacity: 0` alone still leaves an invisible layer that can swallow clicks.

---

## Fragments: reveal hold-points within a slide

A fragment is an absolute composition-timeline time (seconds) within a slide's `[start, end]` range where the controller should hold a reveal state.

**How it works:**

1. Player enters a fragmented slide — seeks directly to `fragments[0]` and holds there.
2. User presses Next (or →) — controller seeks to `fragments[1]` and holds.
3. After the last fragment, Next advances to the next slide.
4. A slide without fragments enters at a rest frame inside the slide, usually its midpoint, not exactly at `slide.end`.

Fragment times must fall within `[start, end]` (inclusive of both bounds). The lint rule rejects only fragments outside that range (`time < start` or `time > end`).

Fragment times are **absolute composition-timeline positions** — the same coordinate space as `data-start` — not offsets relative to the scene's start.

Navigation is seek-driven, not play-driven. The controller never starts playback just to move between fragments; each navigation command is a deterministic seek to the target hold time. Design fragment states so they are correct at the target timeline time.

---

## Branching: hotspots and slide sequences

Branch slides are real scenes in the same composition timeline. They are listed only under `slideSequences` and are excluded from main-line navigation — the player never visits them unless a hotspot fires.

**Navigation model:**

- Clicking a hotspot pushes `{sequenceId, slideIndex: 0}` onto the nav stack and enters the branch's first slide.
- **back()** pops the stack and returns to the exact parent slide (the one that held the hotspot).
- **backToMain()** clears the entire stack and returns to the root slide.
- Breadcrumb renders from the stack: `Main deck › Market sizing methodology › Slide 2`.
- The slide counter inside a branch is scoped to that sequence (`1 of 2`, not the main-deck total).

**What to avoid:**

- Do not add branch scene IDs to the main `slides` array. They must appear only inside a `slideSequences` entry. The lint rule flags overlap.
- Branch scenes are included in the continuous timeline, so a naive linear video export would include them. Export reads main-line slides only (deferred; flagged in the spec).

---

## Worked example: 3-slide deck with fragments and a branch

### Scene HTML (skeleton)

```html
<body style="margin: 0">
  <script type="application/hyperframes-slideshow+json">
    {
      "slides": [
        {
          "sceneId": "hook",
          "notes": "Open with the stat. Pause on the $40B number."
        },
        {
          "sceneId": "problem",
          "notes": "Walk through each pain point one at a time.",
          "fragments": [11.0, 15.0],
          "hotspots": [
            {
              "id": "h1",
              "label": "Where does the $40B figure come from?",
              "target": "market-detail",
              "region": { "x": 55, "y": 60, "w": 40, "h": 20 }
            }
          ]
        },
        {
          "sceneId": "solution",
          "notes": "One sentence: what we do and who it is for."
        }
      ],
      "slideSequences": [
        {
          "id": "market-detail",
          "label": "Market sizing methodology",
          "slides": [{ "sceneId": "mkt-math", "notes": "Bottom-up: 2.3M SMBs × $17k ACV." }]
        }
      ]
    }
  </script>

  <!-- Slide 1 — hook -->
  <div
    data-composition-id="hook"
    data-start="0"
    data-duration="6"
    data-label="The hook"
    data-width="1920"
    data-height="1080"
    style="position: relative; width: 1920px; height: 1080px; overflow: hidden; background: #0a0a0a"
  >
    <section
      class="clip"
      data-start="0"
      data-duration="6"
      data-track-index="1"
      style="position: absolute; inset: 0; display: grid; place-items: center"
    >
      <h1 id="hook-headline" style="font-size: 80px; color: #fff; font-family: sans-serif">
        SMBs lose $40B/year to manual scheduling
      </h1>
    </section>
  </div>

  <!-- Slide 2 — problem (3 fragments) -->
  <div
    data-composition-id="problem"
    data-start="6"
    data-duration="15"
    data-label="The problem"
    data-width="1920"
    data-height="1080"
    style="position: relative; width: 1920px; height: 1080px; overflow: hidden; background: #0a0a0a"
  >
    <section
      class="clip"
      data-start="6"
      data-duration="15"
      data-track-index="1"
      style="position: absolute; inset: 0; padding: 120px 160px; box-sizing: border-box"
    >
      <h2 id="pain-headline" style="font-size: 64px; color: #fff; font-family: sans-serif">
        Three gaps operators can not close
      </h2>
      <p id="pain-1" style="font-size: 48px; color: #ccc; opacity: 0; font-family: sans-serif">
        No-shows cost 23% of booked revenue
      </p>
      <p id="pain-2" style="font-size: 48px; color: #ccc; opacity: 0; font-family: sans-serif">
        Manual reminders take 4h/week per staff
      </p>
      <p id="pain-3" style="font-size: 48px; color: #ccc; opacity: 0; font-family: sans-serif">
        Rescheduling friction drives 40% churn
      </p>
    </section>
  </div>

  <!-- Slide 3 — solution -->
  <div
    data-composition-id="solution"
    data-start="21"
    data-duration="8"
    data-label="The solution"
    data-width="1920"
    data-height="1080"
    style="position: relative; width: 1920px; height: 1080px; overflow: hidden; background: #0a0a0a"
  >
    <section
      class="clip"
      data-start="21"
      data-duration="8"
      data-track-index="1"
      style="position: absolute; inset: 0; display: grid; place-items: center"
    >
      <h2 id="solution-headline" style="font-size: 72px; color: #fff; font-family: sans-serif">
        Acme automates scheduling for service SMBs — no-shows down 80% in 90 days
      </h2>
    </section>
  </div>

  <!-- Branch slide — excluded from main line -->
  <div
    data-composition-id="mkt-math"
    data-start="29"
    data-duration="7"
    data-label="Market math"
    data-width="1920"
    data-height="1080"
    style="position: relative; width: 1920px; height: 1080px; overflow: hidden; background: #111"
  >
    <section
      class="clip"
      data-start="29"
      data-duration="7"
      data-track-index="1"
      style="position: absolute; inset: 0; display: grid; place-items: center"
    >
      <p id="mkt-formula" style="font-size: 56px; color: #fff; font-family: sans-serif">
        2.3M SMBs × $17k ACV = $39B serviceable market
      </p>
    </section>
  </div>

  <script>
    window.__timelines = window.__timelines || {};

    // Slide 2 fragment entrance animations
    gsap.registerPlugin(); // load any plugins before use

    const tl = gsap.timeline({ paused: true });
    window.__timelines["problem"] = tl;

    // Insert positions are absolute composition-timeline times (same as data-start / fragment values).
    tl.from("#pain-1", { opacity: 0, y: 20, duration: 0.4 }, 11.0);
    tl.from("#pain-2", { opacity: 0, y: 20, duration: 0.4 }, 15.0);
    // pain-3 lands at end of slide
    tl.from("#pain-3", { opacity: 0, y: 20, duration: 0.4 }, 13.0);
  </script>
</body>
```

### Key points in the example

- The island `sceneId` values (`"hook"`, `"problem"`, `"solution"`, `"mkt-math"`) exactly match `data-composition-id` values on scene divs.
- `mkt-math` appears only in `slideSequences` — it is never in the top-level `slides` array.
- Fragment times (`11.0`, `15.0`) are within the `problem` scene's `[6, 21]` range (times are absolute composition-timeline positions).
- The hotspot `region` (`x: 55, y: 60, w: 40, h: 20`) positions the clickable area in the lower-right quadrant of the problem slide.
- GSAP timelines are registered on `window.__timelines` and are paused — the HyperFrames engine drives playback; do not call `.play()` at construction time.

---

## Wrapping component

Wrap the composition in `<hyperframes-slideshow>` around `<hyperframes-player>` in any embedding context:

```html
<hyperframes-slideshow>
  <hyperframes-player src="deck.html"></hyperframes-player>
</hyperframes-slideshow>
```

`<hyperframes-slideshow>` provides the navigation chrome (Present, Prev / Next, counter, global mute when `sound` is present, fullscreen), keyboard handling (← / →, Space / Backspace, and P for Present), touch swipe, and hotspot overlays.

The slideshow automatically sets the `interactive` attribute on every inner `<hyperframes-player>` at mount time, so clickable controls, links, native media controls, and custom players inside the composition iframe receive pointer events as expected. (Outside a slideshow wrapper, you must add `interactive` manually on `<hyperframes-player>` — the player defaults to `pointer-events: none` on the iframe so clicks on the player host don't get hijacked into toggling timeline playback.)

**Presenter mode:** use the built-in Present icon button in the slideshow nav capsule, or press P. It calls `window.open('?mode=audience')` for a fullscreen audience tab; the originating tab becomes the presenter view (current slide reduced, next-slide preview, notes, elapsed timer). The two tabs sync via `BroadcastChannel('hf-slideshow:' + location.pathname)`. Do not add a custom wrapper-level Present button; the shared component owns its placement, icon, styling, and audience-mode hiding.

**Presenting over Google Meet / Zoom (screen share):** share the _audience_ surface, keep the presenter view on your own screen.

- **Google Meet (or any in-Chrome share):** Present → in Meet choose **Share screen → A tab** → pick the audience tab → switch back to the presenter tab. Chrome keeps a captured tab rendering while backgrounded, so animations and slide nav stay live. Do **not** share "A window" or "Entire screen" — a fully covered window stops rendering (frozen slides for viewers), and entire-screen exposes your notes.
- **Zoom (desktop app):** drag the audience tab out into its own window and share that window. Zoom captures via the OS, so if the audience window becomes _fully_ covered it freezes — use a second monitor, or keep a sliver of the audience window visible behind the presenter view.

Presenter-driven media playback has an autoplay-policy constraint: `BroadcastChannel` can sync intent, time, and state, but it cannot transfer the presenter's user activation to the audience tab. The shared slideshow player mirrors native media events and starts remote audience playback muted first; only fall back to the standalone harness's audience unlock behavior if muted `media.play()` is rejected or if the deck specifically requires audible audience playback. Do not keep applying remote `timeupdate` messages after a rejected play, or the audience will silently seek through the video without playback.

Presenter notes are editable in the presenter view. Edits are stored in `localStorage` per deck and slide, layered over the manifest notes without rewriting the composition file. Do not add one-off note-editing scripts to decks; rely on the shared slideshow player behavior. If a standalone/custom wrapper truly needs to implement this outside the shared player, use the deterministic storage snippet in `references/standalone-harness.md`.

### Media cleanup on slide exit

The slideshow controller owns slide-exit media cleanup. When navigation changes slide or sequence, it calls `hyperframes-player.stopMedia()` before entering the next slide. That command:

- posts `stop-media` to the iframe runtime, which stops WebAudio and pauses native `<video>` / `<audio>` elements;
- pauses same-origin iframe media directly as a fallback; and
- pauses parent-frame proxies adopted from iframe media.

Same-slide fragment navigation does **not** stop media. Global/deck-level parent audio, such as a background track wired through `audio-src`, is not treated as slide media.

Do not add per-slide cleanup scripts for normal media players. Keep slide video/audio as normal media in the composition; use `data-has-audio="true"` only when the player should preserve audible native video audio instead of treating it as silent visual media.

If the source page has custom controls or visualizations attached to media, those controls must listen to the same native element the slideshow player stops and mutes. A pause caused by slide exit, presenter sync, native controls, custom controls, or the global mute button should all update the visible custom UI through media events, not through parallel state.

When implementing direct iframe fallback cleanup, treat iframe media as cross-realm DOM. Do not test iframe nodes with the parent page's `el instanceof HTMLMediaElement`; that returns false in real browsers. Use `el.ownerDocument.defaultView.HTMLMediaElement` (or an equivalent tag/duck-type guard) before setting `muted` or calling `pause()`.

### Global nav mute

When `<hyperframes-slideshow sound>` renders the nav mute button, that button is the global mute control for the page. It must mute:

- child `<hyperframes-player>` instances, including same-origin iframe media;
- top-level page `<audio>` / `<video>` elements; and
- wrapper-owned SFX/global `Audio` objects via the `hf-sound` event.

Do not add a second mute button inside the composition. If a wrapper script creates `new Audio(...)` objects that are not attached to the DOM, it must listen for `hf-sound` and set `clip.muted = detail.muted` on each object, not merely skip future plays.

The same cross-realm rule applies here: global mute must reach iframe `<video>` / `<audio>` elements through the child frame's DOM realm. A passing unit test in a single DOM realm is not enough; verify in a browser that the actual iframe media elements report `muted: true` after clicking the nav mute button.

`hyperframes present` serves built bundles from `packages/player/dist`. After changing player or slideshow chrome behavior, run `bun run build` in `packages/player` and restart the present server before testing in a browser.

---

## Running a slideshow standalone (interim)

The **durable answer** is engine-hosted: `hyperframes preview --slideshow` / studio present mode will host the composition over the real HyperFrames engine, which drives seek-timelines, owns the gesture frame, and reads the island from the composition. That path is coming; prefer it once it ships.

Until then, standalone demos (a composition opened via the bare player bundle in a browser, without the engine) require workarounds for three gaps: the composition must expose a seekable root timeline, the island must be duplicated into the wrapper, and wrapper-owned SFX/global audio should live in the parent frame. These patterns are documented in:

```
references/standalone-harness.md
```

Do not treat the patterns there as the blessed model — they exist only to bridge the gap until the engine-hosted path lands.

## Handoff

For a public or user-facing slideshow project, the root `index.html` should be a runnable slideshow entrypoint. Opening it in a browser should show slideshow navigation and respond to Next/Prev; it should not expose only the raw composition and require the user to know about Studio or an internal wrapper file. If the raw HyperFrames composition must remain separate for CLI compatibility, put it in a subdirectory such as `composition/index.html` and point scripts/commands at that directory.

The direct-open wrapper must rely on the built-in Present icon button rendered by `<hyperframes-slideshow>`. Do not add a bespoke `#present-btn`, fixed-position button, or wrapper-specific Present styling. The shared component owns the control bar, hides Present in `?mode=audience`, and supports P as a keyboard shortcut.

Validate the direct-open path before handoff. If `file://` browser restrictions break iframe media, local scripts, or same-origin player access, use a self-contained wrapper or make the handoff command start a local server and open the working URL; do not leave `index.html` in a broken or ambiguous state.

For a completed slideshow deck, the primary user-facing next step is presenter mode, not Studio. Run or provide:

```bash
npx hyperframes present <project-dir>
```

Studio/`preview` is useful for editing a composition, but it is not a clear final destination for a slideshow user. If you create a `package.json` for a slideshow project where the raw composition lives in `composition/`, make the default runnable script start presenter mode:

```json
{
  "scripts": {
    "dev": "npx hyperframes present ./composition",
    "studio": "npx hyperframes preview ./composition --background"
  }
}
```

At handoff, include the local presenter URL printed by the command and the minimal instruction: "Click Present, or press P, to open the audience tab." If the user will present over Google Meet or Zoom, also pass on the screen-share guidance from the Presenting section above (share the audience tab in Meet; a dragged-out audience window in Zoom). Keep the server running if the user asked you to start it.

---

## Validation

After authoring or editing a slideshow composition, run validation (it reruns lint before opening the browser):

```bash
npx hyperframes check
```

Treat lint errors and validation `StaticGuard` contract messages as blockers even if a command exits successfully. Fix the file and rerun until `check` reports no lint or runtime errors.

The slideshow lint rule checks:

- Every `slide.sceneId` resolves to an existing scene (by `data-composition-id`).
- Every `hotspot.target` references a defined `slideSequence` id.
- Fragment times fall within each slide's `[start, end]` range.
- No two main-line slides overlap in time.

Fix all violations before previewing. A composition that fails lint will not parse correctly in the player.


<!-- ===== FILE: hyperframes/slideshow/references/standalone-harness.md ===== -->

# Standalone HyperFrames Slideshow Harness

## 1. Interim framing — why this exists

These patterns are a **temporary workaround** for standalone demos. The durable solution is engine-hosted: a future `hyperframes preview --slideshow` / studio present mode will host the composition over the real HyperFrames engine, which drives seek-timelines frame-by-frame, owns the gesture frame, and reads the slideshow island directly from the composition. When that path ships, most of what follows collapses.

Until then, a standalone slideshow opened via the bare player bundle must work around three facts:

1. The composition must expose a seekable `window.__timelines.root` timeline. Anything outside that seek path, such as Three.js loops or imperative entrance effects, must be self-driving.
2. `<hyperframes-slideshow>` reads the slideshow island from its **own innerHTML** (the wrapper element), not from the composition the player loads. The island must be duplicated into the wrapper.
3. The composition runs in the player's **iframe**; user keypresses and pointer events land on the **parent page**. Wrapper-owned SFX/global audio should live in the parent, where the activation token is reliable. Normal slide media stays in the composition and is stopped by the slideshow player on slide exit.

Do not treat these as the blessed authoring model. When the engine-hosted path ships, compositions authored the normal way will just work.

**Living reference implementations:**

---

## 2. The parent wrapper (`index.html` for deliverables, `demo.html` in examples)

The parent page hosts the two dist bundles, wraps the components, duplicates the island, and owns all audio.

For public or user-facing generated projects, make this wrapper the root `index.html` so opening the project in a browser runs the slideshow. Put the raw HyperFrames composition in a separate path such as `composition/index.html`. In repo examples you may still see this file called `demo.html`; that name is a reference pattern, not the preferred handoff for a standalone deck.

```html
<!doctype html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>My Deck — Slideshow Demo</title>

    <!--
      Load both bundles from packages/player/dist.
      The global builds register <hyperframes-player> and <hyperframes-slideshow>
      as custom elements — no import map needed.
    -->
    <script src="../../../packages/player/dist/hyperframes-player.global.js"></script>
    <script src="../../../packages/player/dist/slideshow/hyperframes-slideshow.global.js"></script>

    <style>
      *,
      *::before,
      *::after {
        box-sizing: border-box;
        margin: 0;
        padding: 0;
      }
      html,
      body {
        width: 100%;
        height: 100%;
        overflow: hidden;
        background: #111;
      }
    </style>
  </head>
  <body>
    <!--
      tabindex="0" is critical — <hyperframes-slideshow> binds keydown
      (ArrowLeft/Right, Space, Backspace) to itself. Without tabindex the
      element cannot receive focus and arrow keys are dead.
    -->
    <hyperframes-slideshow
      tabindex="0"
      style="display: block; position: relative; width: 100vw; height: 100vh"
    >
      <hyperframes-player
        interactive
        style="position: absolute; inset: 0"
        src="composition/index.html"
      ></hyperframes-player>

      <!--
        DUPLICATED ISLAND — keep in sync with the island inside index.html.
        <hyperframes-slideshow> reads from its own innerHTML, not from the
        composition the player loads. Every time slides/fragments/hotspots/
        sequences change in index.html, update this copy too.
      -->
      <script type="application/hyperframes-slideshow+json">
        {
          "slides": [
            { "sceneId": "scene-one", "notes": "..." },
            {
              "sceneId": "scene-two",
              "notes": "...",
              "fragments": [8.3, 8.6]
            }
          ],
          "slideSequences": [
            {
              "id": "branch-one",
              "label": "Branch label",
              "slides": [{ "sceneId": "branch-scene", "notes": "..." }]
            }
          ]
        }
      </script>
    </hyperframes-slideshow>
    <!-- The built-in slideshow nav capsule renders Present; do not add a wrapper-level button. -->

    <!-- Audio player lives here — see Section 6 -->
  </body>
</html>
```

`interactive` is required for decks with clickable page content or media controls. Without it, iframe pointer events are disabled by the player shell and a click on the composition can be interpreted as a player play/pause toggle instead of a slide interaction.

### Per-slide `autoplay`

Add `"autoplay": true` to a slide in the island to play that slide's first `<video>` from the start when the presenter lands on it. The slideshow still holds — it never auto-advances — so the presenter clicks Next when ready; autoplay only saves a manual play click into the composition.

```json
{
  "sceneId": "cold-open",
  "autoplay": true,
  "notes": "Promo plays on enter; click Next when it ends."
}
```

Use `autoplay` when the video **is** the slide's primary content and its natural end is the cue to advance — a cold-open promo, a demo clip you let run and then move on from. Do **not** use it for background/ambient loops or for footage the presenter talks over; those should start on the presenter's own cue (a click on the clip's controls via `interactive`), not automatically. One autoplay clip per slide (the first `<video>` in the scene).

### Presenter media bridge for interactive media

Presenter/audience mode syncs slide position through a deck-scoped `BroadcastChannel`. If the presenter is expected to play, pause, seek, mute, or change rate on media inside the composition, mirror those native media events over the same channel. Keep the media element as the source of truth; do not mirror a custom button's private state.

Audible playback has one extra browser constraint: a `BroadcastChannel` message does not carry the presenter's user activation into the audience window. The audience window should try presenter-driven playback muted first, because browsers usually allow muted autoplay; it may still reject `media.play()` even while it accepts remote `currentTime` updates. If that happens, do not keep chasing presenter `timeupdate` messages; show an audience-side unlock control, store the latest play intent, and retry playback from that intent after the audience window receives a click/key gesture.

```js
(function () {
  if (typeof BroadcastChannel === "undefined") return;

  var sender =
    new URLSearchParams(location.search).get("mode") === "audience" ? "audience" : "presenter";
  var channel = new BroadcastChannel("hf-slideshow:" + location.pathname);
  var applyingRemote = false;
  var lastTimeBroadcast = 0;
  var pendingPlayByKey = {};
  var blockedPlayByKey = {};
  var mutedPlaybackByKey = {};
  var unlockButton = null;

  function frameDocument() {
    var player = document.querySelector("hyperframes-player");
    var frame = player && player.iframeElement;
    try {
      return frame && frame.contentDocument ? frame.contentDocument : null;
    } catch {
      return null;
    }
  }
  function mediaNodes() {
    var doc = frameDocument();
    return doc ? Array.from(doc.querySelectorAll("video,audio")) : [];
  }
  function mediaKey(el, index) {
    return el.id ? "id:" + el.id : el.tagName.toLowerCase() + ":" + index;
  }
  function findMedia(key) {
    return mediaNodes().find(function (el, index) {
      return mediaKey(el, index) === key;
    });
  }
  function syncMediaState(el, msg, allowTimeSync) {
    if (typeof msg.playbackRate === "number") el.playbackRate = msg.playbackRate;
    if (typeof msg.volume === "number") el.volume = Math.max(0, Math.min(1, msg.volume));
    if (sender === "audience" && mutedPlaybackByKey[msg.key]) {
      el.muted = true;
    } else if (typeof msg.muted === "boolean") {
      el.muted = msg.muted;
    }
    if (
      allowTimeSync &&
      typeof msg.currentTime === "number" &&
      Math.abs((el.currentTime || 0) - msg.currentTime) > 0.35
    ) {
      el.currentTime = Math.max(0, msg.currentTime);
    }
  }
  function hasBlockedPlay() {
    return Object.keys(blockedPlayByKey).length > 0;
  }
  function hideAudienceUnlockIfClear() {
    if (hasBlockedPlay() || !unlockButton) return;
    unlockButton.remove();
    unlockButton = null;
  }
  function showAudienceUnlock() {
    if (sender !== "audience" || unlockButton) return;
    unlockButton = document.createElement("button");
    unlockButton.type = "button";
    unlockButton.textContent = "Enable audience media";
    unlockButton.style.cssText =
      "position:fixed;left:50%;bottom:96px;transform:translateX(-50%);z-index:100000;border:0;border-radius:999px;padding:12px 18px;background:#fff;color:#111827;box-shadow:0 10px 32px rgba(0,0,0,.28);font:700 14px/1 system-ui,sans-serif;cursor:pointer;";
    unlockButton.addEventListener("click", retryBlockedPlays);
    document.body.appendChild(unlockButton);
  }
  function rememberBlockedPlay(msg) {
    pendingPlayByKey[msg.key] = msg;
    blockedPlayByKey[msg.key] = true;
    showAudienceUnlock();
  }
  function clearBlockedPlay(key) {
    delete blockedPlayByKey[key];
    hideAudienceUnlockIfClear();
  }
  function tryPlay(el, msg) {
    if (sender === "audience") mutedPlaybackByKey[msg.key] = true;
    syncMediaState(el, msg, true);
    if (sender === "audience") el.muted = true;
    try {
      var playResult = el.play();
      if (playResult && typeof playResult.then === "function") {
        playResult
          .then(function () {
            clearBlockedPlay(msg.key);
          })
          .catch(function () {
            rememberBlockedPlay(msg);
          });
      } else {
        clearBlockedPlay(msg.key);
      }
    } catch (e) {
      rememberBlockedPlay(msg);
    }
  }
  function retryBlockedPlays() {
    wireMedia();
    applyingRemote = true;
    try {
      Object.keys(pendingPlayByKey).forEach(function (key) {
        var msg = pendingPlayByKey[key];
        var el = findMedia(key);
        if (el && msg) tryPlay(el, msg);
      });
    } finally {
      setTimeout(function () {
        applyingRemote = false;
      }, 300);
    }
  }
  function publish(el, index, action) {
    if (sender !== "presenter") return;
    if (applyingRemote) return;
    if (action === "timeupdate") {
      var now = performance.now();
      if (now - lastTimeBroadcast < 450 && !el.paused) return;
      lastTimeBroadcast = now;
    }
    channel.postMessage({
      type: "media",
      sender,
      key: mediaKey(el, index),
      action,
      currentTime: el.currentTime || 0,
      paused: el.paused,
      ended: el.ended,
      muted: el.muted,
      volume: el.volume,
      playbackRate: el.playbackRate,
    });
  }
  function wireMedia() {
    mediaNodes().forEach(function (el, index) {
      if (el.dataset.hfPresenterMediaSync === "1") return;
      el.dataset.hfPresenterMediaSync = "1";
      [
        "play",
        "pause",
        "seeking",
        "seeked",
        "ratechange",
        "volumechange",
        "ended",
        "timeupdate",
      ].forEach(function (name) {
        el.addEventListener(name, function () {
          publish(el, index, name);
        });
      });
    });
  }
  channel.addEventListener("message", function (event) {
    var msg = event.data;
    if (!msg || msg.type !== "media" || msg.sender === sender) return;
    if (sender === "audience" && blockedPlayByKey[msg.key] && msg.action === "timeupdate") {
      pendingPlayByKey[msg.key] = msg;
      showAudienceUnlock();
      return;
    }
    var el = findMedia(msg.key);
    if (!el) return;
    applyingRemote = true;
    try {
      if (
        msg.action === "play" ||
        (sender === "audience" && msg.action === "timeupdate" && msg.paused === false && el.paused)
      ) {
        pendingPlayByKey[msg.key] = msg;
        tryPlay(el, msg);
      } else {
        syncMediaState(el, msg, true);
      }
      if (msg.action === "pause" || msg.action === "ended") {
        delete pendingPlayByKey[msg.key];
        delete mutedPlaybackByKey[msg.key];
        clearBlockedPlay(msg.key);
        el.pause();
      }
    } catch {
    } finally {
      setTimeout(function () {
        applyingRemote = false;
      }, 300);
    }
  });
  wireMedia();
  window.addEventListener("load", wireMedia);
  window.addEventListener("keydown", retryBlockedPlays, true);
  window.addEventListener("pointerdown", retryBlockedPlays, true);
  setInterval(wireMedia, 1000);
})();
```

### Custom media visualizers

For waveform, beat-grid, canvas, or timeline players, wire visual state to the native media element. This keeps native controls, custom controls, presenter sync, slide-exit cleanup, and global mute in one event path.

```js
function wireMediaDrivenVisualizer(media, renderFrame, fireCrossedEvents) {
  var mediaFrame = 0;
  var lastTime = media.currentTime || 0;

  function update() {
    var time = media.currentTime || 0;
    if (Math.abs(time - lastTime) < 1.5 && time >= lastTime) {
      fireCrossedEvents(lastTime, time);
    }
    lastTime = time;
    renderFrame(time, media);
  }

  function start() {
    if (!media.requestVideoFrameCallback || mediaFrame) return;
    mediaFrame = media.requestVideoFrameCallback(function () {
      mediaFrame = 0;
      update();
      if (!media.paused && !media.ended) start();
    });
  }

  media.addEventListener("play", start);
  media.addEventListener("playing", start);
  media.addEventListener("pause", update);
  media.addEventListener("ended", update);
  media.addEventListener("timeupdate", update);
  media.addEventListener("seeking", function () {
    lastTime = media.currentTime || 0;
    renderFrame(lastTime, media);
  });
  media.addEventListener("seeked", update);
  media.addEventListener("ratechange", update);
  media.addEventListener("volumechange", update);
  renderFrame(media.currentTime || 0, media);
}
```

Do not use `requestAnimationFrame` inside compositions for media sync; composition lint rejects wall-clock loops. Prefer `HTMLVideoElement.requestVideoFrameCallback()` for smooth video-tied updates and rely on native `timeupdate`/seek events as the fallback.

Use a dedicated wiring marker such as `data-media-sync-wired`. Do not reuse a marker like `data-wired` for both "timeline DOM already rendered" and "media event listeners attached"; pre-rendered timeline HTML will otherwise skip listener setup.

### Editable presenter notes

The shared `<hyperframes-slideshow>` presenter already renders speaker notes as an editable textarea and stores edits in `localStorage`. Do not add deck-specific note editors when the shared player is available.

For interim custom wrappers that cannot use the shared presenter chrome, use this deterministic storage contract exactly so notes migrate cleanly:

```js
const NOTES_STORAGE_PREFIX = "hf-slideshow:presenter-notes:v1:";

function notesDeckKey(slideshowEl) {
  const explicit = slideshowEl.getAttribute("notes-storage-key");
  if (explicit && explicit.trim()) return explicit.trim();

  const playerSrc = slideshowEl.querySelector("hyperframes-player")?.getAttribute("src") || "";
  let resolvedPlayerSrc = playerSrc;
  try {
    resolvedPlayerSrc = new URL(playerSrc, location.href).href;
  } catch {}

  return `${location.origin}${location.pathname}|${document.title}|${resolvedPlayerSrc}`;
}

function notesStorageKey(slideshowEl, position, slide) {
  return `${NOTES_STORAGE_PREFIX}${JSON.stringify([
    notesDeckKey(slideshowEl),
    position.sequenceId,
    position.slideIndex,
    slide.sceneId || "",
  ])}`;
}

function readPresenterNotes(slideshowEl, position, slide) {
  const key = notesStorageKey(slideshowEl, position, slide);
  try {
    const stored = localStorage.getItem(key);
    return stored == null ? slide.notes || "" : stored;
  } catch {
    return slide.notes || "";
  }
}

function wirePresenterNotes(textarea, slideshowEl, position, slide) {
  const key = notesStorageKey(slideshowEl, position, slide);
  textarea.value = readPresenterNotes(slideshowEl, position, slide);
  textarea.addEventListener("input", function () {
    try {
      localStorage.setItem(key, textarea.value);
    } catch {}
  });
}
```

Clearing the textarea must save an empty string, not remove the local value, because a presenter may intentionally blank a manifest note for their run. Use `notes-storage-key="stable-deck-id"` on `<hyperframes-slideshow>` when a standalone demo has a stable project id; otherwise the fallback key isolates by page, title, and player `src`.

---

## 3. Playhead-driven scene visibility

Without the engine, scenes are driven by a `root` GSAP timeline that the composition manages on its own clock. The visibility controller reads `window.__timelines.root.time()` via that timeline's `onUpdate` callback and sets `opacity` accordingly. Only the active scene is visible.

The key insight: scene backgrounds must be `transparent` (not opaque) if you want a Three.js canvas behind them; the body/html background and scene inline `background` set the visual fill.

For converted source pages, preserve the original page's visual design, motion language, interactive behavior, media behavior, and presentation affordances as closely as practical. Port source-specific widgets exactly where practical: custom canvas players, waveform/timeline decorations, expanding rings, playheads, hover states, and event wiring are source material, not optional polish. Also audit for atypical page movement: scroll-scrubbed cameras, parallax, pinned sections, horizontal scrollers, section snapping, translated/scaled world layers, or zoom-to-element navigation. Scroll is often the source's transition trigger, so extract the scroll-progress stops, easing, and camera/focus states, then re-host that motion on slideshow navigation through timeline positions, fragments, or reusable harness hooks. Do not recreate the browser's literal page-scroll-down motion inside a slide; translate it into camera travel/zoom from one focus area to the next. If the same mechanical behavior appears across decks, move it into the player or this harness instead of copying a fragile one-off script.

### Navigation camera transitions for converted pages

When a source page uses scroll to move a translated/scaled world, slideshow navigation usually seeks directly to each slide's hold frame. That seek bypasses any in-timeline interpolation near the scene boundary, so a deck can compute the right camera positions and still appear to jump. Add an explicit standalone navigation transition for manual slide changes, while keeping normal HyperFrames timeline seeks static and deterministic.

Use this pattern only for direct-open/presenter slideshow UI. Do not depend on CSS transitions for rendered video output; rendered compositions must still be correct when seeking a single frame.

```css
#world {
  transform-origin: 0 0;
  will-change: transform;
  transition:
    transform 760ms cubic-bezier(0.22, 1, 0.36, 1),
    opacity 0.3s ease;
}

#world.hf-camera-static {
  transition: opacity 0.3s ease;
}
```

```js
var currentCamera = null;
var currentSlideIndex = null;

function cameraTransform(cam) {
  return "translate(" + cam.tx + "px," + cam.ty + "px) scale(" + cam.s + ")";
}

function setWorldCamera(world, cam, animate) {
  if (!cam) return;
  if (!animate) world.classList.add("hf-camera-static");
  world.style.transform = cameraTransform(cam);
  world.style.opacity = "1";
  if (!animate) {
    world.getBoundingClientRect();
    world.classList.remove("hf-camera-static");
  }
  currentCamera = cam;
}

function slideIndexAtTime(t, slideDuration, slideCount) {
  return Math.max(0, Math.min(slideCount - 1, Math.floor(t / slideDuration)));
}

function updateCameraForTime(t, opts) {
  var nextSlideIndex = slideIndexAtTime(t, SLIDE_DURATION, SLIDES.length);
  var jumpedBetweenSlides =
    currentSlideIndex !== null &&
    nextSlideIndex !== currentSlideIndex &&
    Math.abs(t - lastTime) > 1.2;
  var animateCamera = Boolean(
    window.__hfCameraTransitionsEnabled && jumpedBetweenSlides && !(opts && opts.staticCamera),
  );
  var cam = cameraAtTime(t);
  setWorldCamera(world, cam, animateCamera);
  currentSlideIndex = nextSlideIndex;
}
```

During measurement, temporarily remove the transform with `hf-camera-static`, compute all element union rects, then restore `currentCamera` without animation. On initial load, resize, and validation-style seeks, call `updateCameraForTime(t, { staticCamera: true })`. In the standalone wrapper, set `iframe.contentWindow.__hfCameraTransitionsEnabled = true` after the player iframe is available. That keeps the exported composition seekable while letting presenter navigation glide between focal points.

Before validation, resolve source font variables. HyperFrames lint accepts concrete generic stacks such as `system-ui, sans-serif` and `ui-monospace, monospace`, or real `@font-face` declarations pointing at local font files. It does not accept `font-family: var(--f-body)` / `var(--f-mono)` as a render-safe family.

```html
<!-- In index.html (composition) -->

<!-- Shared scene CSS — all scenes start hidden -->
<style>
  .scene-frame {
    position: absolute;
    top: 0;
    left: 0;
    width: 1920px;
    height: 1080px;
    overflow: hidden;
    opacity: 0; /* hidden at rest — visibility controller shows the active one */
    visibility: hidden; /* opacity:0 alone still lets invisible frames block clicks */
    pointer-events: none; /* inactive scenes must not swallow events */
  }
</style>

<!--
  content-visible-at-rest: mark the first scene's elements with their
  final non-hidden state so the deck is not blank before the controller
  fires. The controller calls updateVisibility(0) synchronously on load.

  If using Three.js canvas behind scenes, set background: transparent
  here and let the 3D canvas + body color supply the fill.
-->
<div
  id="scene-cover"
  class="scene-frame clip"
  data-composition-id="cover"
  data-start="0"
  data-duration="9"
  style="background: transparent"
>
  <!-- content here -->
</div>

<div
  id="scene-problem"
  class="scene-frame clip"
  data-composition-id="problem"
  data-start="9"
  data-duration="9"
  style="background: transparent"
>
  <!-- content here -->
</div>

<!-- Root timeline — spans the full composition duration -->
<script>
  (function () {
    window.__timelines = window.__timelines || {};
    var tl = gsap.timeline({ paused: true });
    // A single to() for the full duration establishes the seekable range
    tl.to({}, { duration: 108 }); // replace 108 with your total seconds
    window.__timelines["root"] = tl;
  })();
</script>

<!-- Visibility controller -->
<script>
  (function () {
    var scenes = [
      { id: "scene-cover", start: 0, end: 9 },
      { id: "scene-problem", start: 9, end: 18 },
      // ... all scenes including branch scenes
    ];

    var lastActiveId = null;

    function updateVisibility(t) {
      for (var i = 0; i < scenes.length; i++) {
        var s = scenes[i];
        var el = document.getElementById(s.id);
        if (!el) continue;
        var active = t >= s.start && t < s.end;
        el.style.opacity = active ? "1" : "0";
        el.style.visibility = active ? "visible" : "hidden";
        el.style.pointerEvents = active ? "auto" : "none";

        if (active && lastActiveId !== s.id) {
          lastActiveId = s.id;
          fireEntrance(el); // see Section 4
        }
      }
      // fragment reveals here — see Section 4
    }

    window.__hfSetTime = updateVisibility;

    // Show first slide immediately — avoids blank on load
    updateVisibility(0);

    // Hook the root timeline so every seek drives visibility
    var root = window.__timelines && window.__timelines["root"];
    if (root) {
      root.eventCallback("onUpdate", function () {
        updateVisibility(root.time());
      });
    }
  })();
</script>
```

---

## 4. Imperative entrances on slide-activate

The engine-hosted path drives GSAP seek-timelines frame by frame. Without it, seek-timeline tweens never fire. Instead, fire imperative `gsap.from()` calls each time a scene becomes active — these run on GSAP's own ticker and are independent of any playhead.

Fragment reveals use playhead-crossing: the visibility controller checks whether the playhead has passed each fragment's hold-time and fires an animation on the first crossing. Bunch fragment hold-times near the scene start (within the first 300–500 ms of the scene) so successive ArrowRight presses feel like snappy sequential reveals rather than long waits.

```js
// --- Entrance animations ---

function fireEntrance(sceneEl) {
  // [data-anim] marks elements that should entrance on slide-activate.
  // Add data-anim to eyebrows, headlines, subheads, and card grids.
  var animEls = sceneEl.querySelectorAll("[data-anim]");
  if (!animEls.length) return;
  gsap.from(animEls, {
    opacity: 0,
    y: 28,
    duration: 0.4,
    stagger: 0.07,
    ease: "power2.out",
    overwrite: true, // cancel any in-flight animation on rapid slide changes
  });
}

// --- Fragment reveals ---

// Fragment config: times in absolute composition timeline seconds,
// bunched near the scene start for snappy successive reveals.
var fragments = [
  { time: 9.3, id: "prob-item1", revealed: false },
  { time: 9.6, id: "prob-item2", revealed: false },
];

function revealFragment(id) {
  var el = document.getElementById(id);
  if (!el) return;
  gsap.fromTo(
    el,
    { opacity: 0, x: -24 },
    { opacity: 1, x: 0, duration: 0.35, ease: "power2.out", overwrite: true },
  );
}

// Inside updateVisibility(t):
for (var f = 0; f < fragments.length; f++) {
  if (!fragments[f].revealed && t >= fragments[f].time) {
    fragments[f].revealed = true;
    revealFragment(fragments[f].id);
  }
}

// On problem scene re-entry, reset all fragment states:
if (active && lastActiveId !== s.id && s.id === "scene-problem") {
  for (var f = 0; f < fragments.length; f++) {
    fragments[f].revealed = false;
    var pEl = document.getElementById(fragments[f].id);
    if (pEl) gsap.set(pEl, { opacity: 0, clearProps: "transform" });
  }
}
```

Fragment items start with `opacity: 0` in CSS. The visibility controller reveals them; the entrance driver does not touch them until crossing.

---

## 5. The scenes bootstrap postMessage

`<hyperframes-slideshow>` must know each scene's time range to map a `sceneId` to a playhead position. Without the engine injecting this at runtime, the composition must post it manually after load.

Post the manifest from the composition (index.html), not the parent wrapper:

```js
// In index.html — post after a brief delay so the parent frame has settled
(function () {
  var FPS = 30;
  var totalSeconds = 108; // match your composition's data-duration
  var totalFrames = totalSeconds * FPS;

  var scenes = [
    // EVERY scene — including branch scenes — must appear here.
    // id must match data-composition-id; start/duration in seconds.
    { id: "cover", start: 0, duration: 9 },
    { id: "problem", start: 9, duration: 9 },
    { id: "solution", start: 18, duration: 9 },
    // ... all main-line scenes ...
    // branch scene — listed last, NOT in main slides array in the island
    { id: "market-sizing", start: 99, duration: 9 },
  ];

  function postTimeline() {
    parent.postMessage(
      {
        source: "hf-preview",
        type: "timeline",
        durationInFrames: totalFrames,
        scenes: scenes,
      },
      "*",
    );
  }

  // ~300ms delay after load to let the parent settle
  if (document.readyState === "complete") {
    setTimeout(postTimeline, 300);
  } else {
    window.addEventListener("load", function () {
      setTimeout(postTimeline, 300);
    });
  }
})();
```

Omitting any scene (including branch scenes) from this manifest means the slideshow component cannot seek to it. Include every scene declared in the HTML, even scenes only reachable via a hotspot.

---

## 6. Audio/SFX — built-in mute control via `<hyperframes-slideshow sound>`

Wrapper-owned SFX should live in the parent page. Browsers enforce user-activation for AudioContext and HTMLAudioElement.play() — an iframe without its own activation (i.e., the user never clicked inside it) is often autoplay-blocked. The user's keypress lands on the parent, so the parent is the reliable frame for click/transition sound effects.

Normal slide media should stay in the composition. The slideshow player now stops slide media automatically on slide/sequence changes by calling `hyperframes-player.stopMedia()`, which pauses iframe `<video>` / `<audio>`, runtime WebAudio, and parent proxies adopted from iframe media. Same-slide fragment reveals do not stop media, and global/deck-level parent audio such as `audio-src` is left alone. Do not hand-roll per-slide cleanup scripts for regular video/audio players.

Every copied `<video>` / `<audio>` with a `src` must be timed for HyperFrames ownership:

```html
<video
  src="assets/demo.mp4"
  controls
  playsinline
  preload="metadata"
  data-start="0"
  data-duration="96"
  data-has-audio="true"
></video>
```

Use `data-has-audio="true"` only for audible media. Muted autoplay loops can omit it. Do not leave `preload="none"` in converted compositions.

Implementation detail: iframe media elements belong to the iframe's DOM realm. Fallback code in the parent page/player must not use the parent page's `el instanceof HTMLMediaElement` check for iframe nodes; in real browsers that fails and leaves videos audible. Use `el.ownerDocument.defaultView.HTMLMediaElement` or a tag/duck-type guard before setting `muted` or calling `pause()`.

### Mute toggle — built-in chrome control

Add the `sound` boolean attribute to `<hyperframes-slideshow>` in demo.html. The component renders a speaker/speaker-muted SVG button as the **leftmost item in the nav capsule**, styled identically to the prev/next ghost buttons. No separate mute button in the composition.

```html
<hyperframes-slideshow tabindex="0" sound style="..."> ... </hyperframes-slideshow>
```

The component:

- Tracks `muted` state (default `false`); exposes a `muted` getter
- Reflects to a `data-hf-muted` attribute on the host when muted
- Applies mute globally to child `<hyperframes-player>` media and top-level page `<audio>` / `<video>` elements
- Dispatches `CustomEvent("hf-sound", { detail: { muted }, bubbles: true, composed: true })` on every toggle
- Browser-checks the actual iframe media state after changes; every composition `<video>` / `<audio>` should report `muted: true` after clicking the nav mute button

Wrapper-owned `new Audio(...)` objects are not attached to the DOM, so the parent audio player must mirror the `hf-sound` event onto each clip:

```js
var muted = false;
var slideshow = document.querySelector("hyperframes-slideshow");
if (slideshow) {
  slideshow.addEventListener("hf-sound", function (e) {
    muted = e.detail && e.detail.muted === true;
    Object.keys(clips).forEach(function (name) {
      clips[name].muted = muted;
    });
  });
}
// In message handler:
if (muted) return; // skip play
```

If `sound` is **not** present on `<hyperframes-slideshow>` (decks without audio), the mute control is hidden — the capsule shows only nav.

### Composition: post cues unconditionally

The composition posts sfx cues **unconditionally** — it does not track mute state. The parent gates on `muted`:

**In the composition (index.html):**

```js
// Post an sfx cue at transition points — unconditionally.
// The parent audio player gates on the slideshow component's mute state.
function playSfx(name) {
  try {
    parent.postMessage({ type: "hf-sfx", name: name }, "*");
  } catch (e) {}
}

// Fire at scene transitions:
//   playSfx("advance")      — moving to the next main-line slide
//   playSfx("back")         — returning from a branch
//   playSfx("branch-enter") — entering a branch
//   playSfx("fragment")     — a fragment item is revealed
```

Do NOT add a mute button inside the composition. The `#sfx-mute` coral button pattern is removed; the nav capsule in the parent chrome owns mute.

**In the parent (demo.html):**

```html
<script>
  (function () {
    // Audio elements are preloaded here, in the frame that receives user gestures.
    var clips = {
      advance: new Audio("sfx/advance.mp3"),
      fragment: new Audio("sfx/fragment.mp3"),
      "branch-enter": new Audio("sfx/branch-enter.mp3"),
      back: new Audio("sfx/back.mp3"),
    };
    clips.advance.volume = 0.45;
    clips.fragment.volume = 0.4;
    clips["branch-enter"].volume = 0.4;
    clips.back.volume = 0.4;
    Object.keys(clips).forEach(function (k) {
      clips[k].preload = "auto";
    });

    // Track mute state from the slideshow component's hf-sound event.
    var muted = false;
    var slideshow = document.querySelector("hyperframes-slideshow");
    if (slideshow) {
      slideshow.addEventListener("hf-sound", function (e) {
        muted = e.detail && e.detail.muted === true;
      });
    }

    var unlocked = false;

    function unlock() {
      if (unlocked) return;
      unlocked = true;
      // Prime wrapper-owned SFX clips: play muted then immediately pause/reset.
      // This moves the clip into the "allowed" state so later plays are instant.
      Object.keys(clips).forEach(function (name) {
        var el = clips[name];
        var v = el.volume;
        el.volume = 0;
        el.play()
          .then(function () {
            el.pause();
            el.currentTime = 0;
            el.volume = v;
          })
          .catch(function () {
            el.volume = v;
          });
      });
    }

    // Unlock on the first user gesture in the parent frame.
    window.addEventListener("keydown", unlock, true);
    window.addEventListener("pointerdown", unlock, true);
    window.addEventListener("click", unlock, true);

    window.addEventListener("message", function (e) {
      var d = e.data;
      if (!d || d.type !== "hf-sfx") return;
      // Gate on mute state — the component owns this.
      if (muted) return;
      var el = clips[d.name];
      if (!el || !unlocked) return;
      try {
        el.currentTime = 0;
        el.play().catch(function () {});
      } catch (err) {}
    });
  })();
</script>
```

**Sourcing SFX files:** use the HeyGen MCP `search_audio_sounds` tool with `type=sound_effects` and keywords like "whoosh", "click", "transition". Download the results to a local `sfx/` directory next to `demo.html` and reference them by relative path. Do not fetch SFX at render time — the HyperFrames determinism rule forbids runtime network requests; pre-download and commit them.

---

## 7. Three.js (optional)

Add a Three.js scene behind the slides for ambient motion. The key rules:

- **Own rAF loop** — do not integrate with the HF seek timeline. Three.js runs its own `requestAnimationFrame` loop independent of playhead position.
- **One persistent canvas** — create the canvas once; update geometry/materials in-place per scene.
- **Guard renderer creation** — WebGL may be unavailable (software-GL environments, some CI contexts). Create the renderer inside try/catch once; if it fails, hide the canvas and expose no-op stubs. Do not spam `console.error` — silence it during creation and restore it in `finally`.
- **Full-bleed, behind content** — fix the canvas at `z-index: 0`, `pointer-events: none`, behind scene frames at `z-index: 1`.
- **Transparent scene frames** — set scene backgrounds to `transparent` so the 3D canvas shows through. Use a radial-gradient scrim on the text container (not the scene frame itself) to keep type legible while letting 3D show in the margins.
- **Expose a mood hook** — export `window.__threeApplyMood(sceneKey)` so the visibility controller can switch particle colors, toggle sub-objects, or change the clear color when the active scene changes.

```js
// In index.html — Three.js setup (module script)
import * as THREE from "https://cdn.jsdelivr.net/npm/three@0.160.0/build/three.module.js";

var canvas = document.getElementById("three-canvas");
var renderer = null;
var _err = console.error;
console.error = function () {}; // silence THREE's multi-line GPU error during init
try {
  renderer = new THREE.WebGLRenderer({ canvas: canvas, alpha: true, antialias: true });
} catch (e) {
  // renderer stays null
} finally {
  console.error = _err;
}

if (!renderer) {
  // Graceful degradation — branded layout is the fallback.
  canvas.style.display = "none";
  window.__threeApplyMood = function () {};
  // Do NOT start the rAF loop.
} else {
  renderer.setSize(1920, 1080);
  renderer.setPixelRatio(1);
  canvas.style.cssText =
    "position:fixed;top:0;left:0;width:1920px;height:1080px;z-index:0;pointer-events:none";

  var scene = new THREE.Scene();
  var camera = new THREE.PerspectiveCamera(60, 1920 / 1080, 0.1, 1000);
  camera.position.set(0, 0, 5);

  // --- build your particle system, meshes, etc. here ---

  // Mood config: map sceneId → visual state (colors, sub-object visibility, bg color)
  var MOODS = {
    cover: {
      /* particle color, opacity, bg ... */
    },
    problem: {
      /* ... */
    },
    // one entry per scene key
  };

  window.__threeApplyMood = function (sceneKey) {
    var m = MOODS[sceneKey] || MOODS["cover"];
    // update geometry attributes, material opacity, sub-group visibility, etc.
  };
  window.__threeApplyMood("cover"); // apply initial state

  // --- own rAF loop ---
  var lastTime = null;
  function animate(ts) {
    requestAnimationFrame(animate);
    if (lastTime === null) lastTime = ts;
    var dt = Math.min((ts - lastTime) / 1000, 0.05);
    lastTime = ts;
    // update particles, rotate objects, etc.
    renderer.render(scene, camera);
  }
  requestAnimationFrame(animate);
}
```

**CSS for transparent scene frames + scrim:**

```css
/* Three.js canvas — always behind everything */
#three-canvas {
  position: fixed;
  top: 0;
  left: 0;
  width: 1920px;
  height: 1080px;
  z-index: 0;
  pointer-events: none;
}

/* Scene frames are transparent so the 3D canvas shows through */
.scene-frame {
  position: absolute;
  top: 0;
  left: 0;
  width: 1920px;
  height: 1080px;
  background: transparent; /* NOT opaque — 3D would be occluded */
  z-index: 1;
}

/* Scrim on the TEXT container — not the scene frame.
   Radial gradient: opaque in the center where text is, transparent at edges
   so 3D shows in the whitespace margins. */
.slide-inner.scrim-light {
  background: radial-gradient(
    ellipse 75% 80% at 50% 50%,
    rgba(255, 255, 255, 0.88) 30%,
    rgba(255, 255, 255, 0.6) 65%,
    rgba(255, 255, 255, 0) 100%
  );
}
```

---

## 8. Foot-gun checklist

| Failure                                               | Symptom                                                         | One-line fix                                                                                                                                     |
| ----------------------------------------------------- | --------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------ |
| Island not duplicated in wrapper                      | Slideshow chrome never renders; no slide counter, no prev/next  | Copy the `<script type="application/hyperframes-slideshow+json">` block verbatim into the `<hyperframes-slideshow>` element in demo.html         |
| Wrapper SFX in the iframe                             | Click/transition sounds silent                                  | Move SFX Audio elements and unlock logic to demo.html; post `{type:'hf-sfx',name}` from index.html                                               |
| No self-clock in composition                          | All scene frames stacked / wrong slide visible at load          | Add the root GSAP timeline (`window.__timelines["root"]`) and the `onUpdate` visibility controller as shown in Section 3                         |
| Content opacity:0 with no engine                      | Blank slides — `[data-anim]` elements invisible at rest         | Call `updateVisibility(0)` synchronously after defining the controller so the first slide is shown immediately                                   |
| Keydown bound to the element without focus            | ArrowLeft/Right dead                                            | Add `tabindex="0"` to `<hyperframes-slideshow>` so it can receive keyboard focus                                                                 |
| Opaque scene background occluding Three.js canvas     | 3D never visible                                                | Set `background: transparent` on `.scene-frame`; put the visual fill on the text scrim container instead                                         |
| WebGL renderer creation spams errors in headless envs | Console noise, rAF loop starts anyway                           | Silence `console.error` during `new THREE.WebGLRenderer(...)`, restore in `finally`, guard the rAF start on `renderer !== null`                  |
| Branch scene missing from postMessage manifest        | Hotspot navigates but slide is blank                            | Include every scene — main line and branch — in the `scenes` array of the `postTimeline()` message                                               |
| Prominent 3D/content in nav-capsule zone              | Bright element bleeds behind/beside the nav pill                | Keep the bottom-right ~360×140px region clear; add a background-matching gradient overlay on any slide whose 3D mood is bright in that corner    |
| Custom media visualizer uses its own timer            | Canvas/playhead drifts from the actual video or native controls | Drive visual state from media events and `media.currentTime`; do not use an independent `setTimeout` clock                                       |
| One `data-wired` flag means two different things      | Pre-rendered timeline HTML skips media listener setup           | Use separate markers such as `data-timeline-rendered` and `data-media-sync-wired`                                                                |
| Presenter media events are not bridged                | Audience follows slides but not play/pause/seek/mute            | Mirror native media events over `BroadcastChannel("hf-slideshow:" + location.pathname)` in standalone wrappers with interactive media            |
| Remote play is blocked in the audience window         | Audience media time jumps but video never plays                 | Try muted playback first; if `media.play()` rejects, show an audience unlock button and ignore live `timeupdate` chasing until playback succeeds |
| Audience muted autoplay publishes back to presenter   | Presenter audio starts, then mutes or cuts out                  | Publish media events only from presenter mode; audience mute is a local browser-autoplay workaround, not shared media state                      |
| Copied media lacks HyperFrames timing                 | Lint errors on untimed media; preview/render diverge            | Add `data-start`, `data-duration`, and `data-has-audio="true"` when audible; avoid `preload="none"`                                              |
| Source font CSS variables kept as font-family values  | StaticGuard font-family contract errors                         | Replace with concrete render-safe stacks or add local `@font-face` declarations                                                                  |
| Converted scroll/camera source jumps between slides   | Per-slide focal points are correct but manual navigation snaps  | Add a standalone navigation-camera transition hook; disable it for measurement, initial load, resize, and render/validation seeks                |
