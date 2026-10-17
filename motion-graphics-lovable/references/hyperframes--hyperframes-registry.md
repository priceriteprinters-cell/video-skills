

<!-- ===== FILE: hyperframes/hyperframes-registry/GUIDE.md ===== -->

---
name: hyperframes-registry
description: Search, install, and wire registry blocks and components into HyperFrames compositions. Use BEFORE hand-building any named visual — whenever a brief, a user, or a storyboard names a look, effect, treatment, or transition such as CRT scanlines, glitch, chromatic aberration, film grain, a shimmer sweep, a chart, a code or terminal window, a map, or a confetti burst — because roughly 400 hosted items already cover many of them and the search ranks all of them with nothing installed, no project, and no account. Also use when running hyperframes add or hyperframes catalog, installing one item or every block matching a tag, wiring an installed item into index.html, or working with hyperframes.json. Covers discovery, install locations, block sub-composition wiring, component snippet merging, and authoring a new block or component to contribute upstream (idea → scaffold → validate → PR).
---

**Plugin installs:** Before setup or freshness commands, follow [plugin execution rules](../hyperframes/references/plugin-installation.md) when this skill is inside a HyperFrames plugin. Standalone installs keep the update instructions below.

# HyperFrames Registry

The registry provides reusable blocks and components installable via `hyperframes add <name>`.

- **Blocks** — standalone sub-compositions (own dimensions, duration, timeline). Included via `data-composition-src` in a host composition.
- **Components** — effect snippets (no own dimensions). Pasted directly into a host composition's HTML.

## Quick reference

```bash
hyperframes add data-chart              # install a block
hyperframes add grain-overlay           # install a component
hyperframes add captions                # install every block tagged captions
hyperframes add shimmer-sweep --dir .   # target a specific project
hyperframes add data-chart --json       # machine-readable output
hyperframes add data-chart --no-clipboard  # skip clipboard (CI/headless)
```

After install, the CLI prints which files were written and a snippet to paste into your host composition. The snippet is a starting point — you'll need to add `data-composition-id` (must match the block's internal composition ID), `data-start`, and `data-track-index` attributes when wiring blocks.

The positional value is resolved as an exact item name first. If no item matches and the value is a tag, the command installs every block with that tag. Registry dependencies are installed before the requested item. `hyperframes add` works only for blocks and components; for examples, use `hyperframes init <dir> --example <name>` instead.

## Install locations

Blocks install to `compositions/<name>.html` by default. Components install to `compositions/components/<name>.html` by default.

These paths are configurable in `hyperframes.json`:

```json
{
  "registry": "https://raw.githubusercontent.com/heygen-com/hyperframes/main/registry",
  "paths": {
    "blocks": "compositions",
    "components": "compositions/components",
    "assets": "assets"
  }
}
```

See [install-locations.md](./references/install-locations.md) for full details.

## Wiring blocks

Blocks are standalone compositions — include them via `data-composition-src` in your host `index.html`:

```html
<div
  data-composition-id="data-chart"
  data-composition-src="compositions/data-chart.html"
  data-start="2"
  data-duration="15"
  data-track-index="1"
  data-width="1920"
  data-height="1080"
></div>
```

Key attributes:

- `data-composition-src` — path to the block HTML file
- `data-composition-id` — must match the block's internal ID
- `data-start` — when the block appears in the host timeline (seconds)
- `data-duration` — how long the block plays
- `data-width` / `data-height` — block canvas dimensions
- `data-track-index` — Studio timeline row; display only. Use CSS `z-index` for layering

See [wiring-blocks.md](./references/wiring-blocks.md) for full details.

## Wiring components

Components are snippets — paste their HTML into your composition's markup, their CSS into your style block, and their JS into your script (if any):

1. Read the installed file (e.g., `compositions/components/grain-overlay.html`)
2. Copy the HTML elements into your composition's `<div data-composition-id="...">`
3. Copy the `<style>` block into your composition's styles
4. Copy any `<script>` content into your composition's script (before your timeline code)
5. If the component exposes GSAP timeline integration (see the comment block in the snippet), add those calls to your timeline

See [wiring-components.md](./references/wiring-components.md) for full details.

## Discovery

Use the CLI as the primary discovery surface. **Search by intent before browsing:** the registry holds more items than you can scan by eye, so listing them and matching on names or tags is the slow path, and it fails whenever the author's wording differs from yours.

```bash
# Rank the whole catalog against what the beat should do
npx hyperframes catalog --query "reveal a headline one line at a time"
npx hyperframes add caption-clip-wipe
```

Search is local and sends nothing. By default it ranks on vocabulary shared with the item's name, title and description, so it only finds items that reuse your words; `--on-device` ranks by meaning instead, after a one-time model download. With `--json` the envelope names which tier answered, so check that rather than assuming a ranking happened.

**Always query in English, whatever language the video is in.** The catalog is written in English and both tiers index it that way (the on-device model is English-only too). A query in another script produces no searchable terms and returns nothing at all. This is easy to get wrong on a Japanese or Chinese project, where the brief, the captions and the narration are all in that language and the query naturally follows: describe the _move_ in English, then write the on-screen copy in whatever language the video needs. If a query does come back with `No searchable words in query`, that is this rule, not a missing component, and it is not worth a gap report.

Installability is applied after ranking, not before it: a name the vectors carry but this registry cannot serve is dropped from the results and counted in `dropped`, so a non-zero `dropped` means the two are different generations. See `/hyperframes-cli` for the offline tier, the consent gates, and how to refresh a stale index.

To browse or filter instead of search:

```bash
npx hyperframes catalog
npx hyperframes catalog --type block
npx hyperframes catalog --type component
npx hyperframes catalog --type block --tag social
npx hyperframes catalog --json
npx hyperframes catalog --human-friendly
```

The normal table and `--json` modes only list matches; install a selected name with `hyperframes add <name>`. `--human-friendly` opens an interactive picker and installs the selected item immediately. In CI or agent workflows, prefer `--json` followed by an explicit `add`.

### Report what the catalog does not have

When the search comes back and nothing in it does the job, say so before you hand-author the move:

```bash
npx hyperframes feedback --search-miss "<the query you ran>" --wanted "<the move you needed>" --tier <the tier that answered>
```

`catalog --query` prints this line for you, pre-filled, and `--json` carries it as `report_gap` — so it is already in hand at the moment you decide nothing fits.

**Report whenever nothing in the results does the job, on either tier.** Do not wait for the on-device tier to have answered: it needs a consented 33 MB download, so an agent run is on `words` unless it explicitly opted in, and gating on `on-device` would silence almost every report. The `--tier` value rides along so a vocabulary miss stays distinguishable from a meaning miss when these are read. Describe the effect you wanted, not the item name you imagined: what comes back is a list of moves worth building, and a report naming a non-existent item teaches nothing. This is the only path that sends a query anywhere, which is exactly why it is a separate deliberate command rather than something the search does on its own. It carries no rating and never lands in the rating metric.

This is the whole demand signal for the catalog. Skipping it means the gap you hit gets guessed at from install counts instead, which cannot see a move nobody could install.

If the CLI cannot reach the configured registry, inspect the raw manifest as a fallback:

```bash
curl -s https://raw.githubusercontent.com/heygen-com/hyperframes/main/registry/registry.json
```

A registry the CLI cannot reach does **not** empty the catalog for **discovery**: a previously fetched manifest keeps serving past its 24h refresh window whenever revalidation fails, so `catalog` and `catalog --query` still list and rank against the last copy on disk.

**`add` still needs the network, even for an item you installed yesterday.** Only manifests are cached; the item's actual files are fetched on every install. So offline you can search, and you can see what an item is, but installing it fails at the file fetch. Do not promise a user an offline install.

Each item's `registry-item.json` contains: name, type, title, description, tags, dimensions (blocks only), duration (blocks only), and file list.

See [discovery.md](./references/discovery.md) for details on filtering by type and tags.

## Contributing a new block or component

To author a NEW registry item (caption style, VFX block, transition, lower third, or a reusable component) and ship it as an upstream PR — not install an existing one — follow the full idea → scaffold → build → validate → preview → ship workflow in [contributing.md](./references/contributing.md). Copy-paste starter templates (caption / VFX / component / `registry-item.json`) are in [templates.md](./references/templates.md).


<!-- ===== FILE: hyperframes/hyperframes-registry/examples/add-block.md ===== -->

# Worked Example: Adding a Block

## Scenario

User has an existing HyperFrames project and wants to add an animated chart alongside their video content.

## Steps

### 1. Install the block

```bash
hyperframes add data-chart
```

### 2. Wire into index.html

```html
<div id="stage" data-composition-id="main" data-width="1920" data-height="1080" data-duration="30">
  <video
    id="speaker"
    src="speaker.mp4"
    data-start="0"
    data-duration="30"
    data-track-index="0"
    style="position: absolute; width: 60%; height: 100%; left: 0; top: 0; object-fit: cover;"
  ></video>

  <!-- Data chart appears at 5s in the right 40% of the screen -->
  <div
    data-composition-id="data-chart"
    data-composition-src="compositions/data-chart.html"
    data-start="5"
    data-duration="15"
    data-track-index="1"
    data-width="1920"
    data-height="1080"
    style="position: absolute; right: 0; top: 0; width: 40%; height: 100%;"
  ></div>
</div>
```

### 3. Lint and preview

```bash
hyperframes lint
hyperframes preview
```

### 4. Customize (optional)

Edit `compositions/data-chart.html` — data arrays are at the top of the script, colors are in the CSS rules scoped under `[data-composition-id="data-chart"]`.


<!-- ===== FILE: hyperframes/hyperframes-registry/examples/add-component.md ===== -->

# Worked Example: Adding a Component

## Scenario

User wants to add a shimmer light sweep effect to their title text.

## Steps

### 1. Install the component

```bash
hyperframes add shimmer-sweep
```

### 2. Read the snippet

Open `compositions/components/shimmer-sweep.html` and read the comment header.

### 3. Wire into your composition

**HTML** — wrap target elements:

```html
<div class="shimmer-sweep-target" style="--shimmer-color: rgba(255, 255, 255, 0.5)">
  <h1 class="title">AI-Powered Video</h1>
</div>
```

**CSS** — paste the `.shimmer-sweep-target` and `.shimmer-mask` rules from the snippet.

**JS** — paste the auto-injection script (before timeline code):

```js
document.querySelectorAll(".shimmer-sweep-target").forEach((el) => {
  if (!el.querySelector(".shimmer-mask")) {
    const mask = document.createElement("div");
    mask.className = "shimmer-mask";
    el.appendChild(mask);
  }
});
```

**Timeline** — add the sweep:

```js
tl.fromTo(
  ".shimmer-sweep-target",
  {
    "--shimmer-pos": "-20%",
  },
  {
    "--shimmer-pos": "120%",
    duration: 1.2,
    ease: "power2.inOut",
    stagger: 0.15,
  },
  1.5,
);
```

### 4. Lint and preview

```bash
hyperframes lint
hyperframes preview
```

### 5. Customize

- `--shimmer-color`: highlight color per element
- `--shimmer-width`: light band width (default 20%)
- `--shimmer-angle`: sweep direction (default 120deg)
- Timeline `duration`, `ease`, `stagger`: control speed and feel


<!-- ===== FILE: hyperframes/hyperframes-registry/references/component-quality-bar.md ===== -->

# Component quality bar

What a catalog component has to be for us to keep shipping it. Every criterion here comes from a
defect found and verified on this branch, not from taste.

A registry component is a motion primitive an author installs into their own composition and
ships. The catalog page is marketing; the installed file is the product. Every criterion below is
therefore evaluated against **the item's own `<name>.html`, mounted alone**, never against
`demo.html` and never against the catalog page, because both of those carry scaffolding the author
does not receive.

Read this before auditing, scoring or cutting anything. It exists so several people auditing in
parallel reach the same verdict on the same item.

## The one rule

> An item earns its place when the file the author installs, mounted by itself on the ground it
> was designed for, renders the subject its name promises and moves the way its description says.
> Anything that fails that and cannot be fixed into something no other item already does is cut.

## How an audit runs

Two passes, in this order. The mechanical pass is free and runs across every item in seconds; the
visual pass costs a browser and eyes, so it is spent only on what the mechanical pass could not
decide. A mechanical signal is a **candidate**, never a verdict.

| Pass           | Cost           | Decides                                                                                  |
| -------------- | -------------- | ---------------------------------------------------------------------------------------- |
| **Mechanical** | grep and hash  | duplicates, missing timeline, banned hexes, empty markup, name gaps, unbounded variables |
| **Visual**     | render and eye | renders at all, implements its description, legible, deterministic                       |

`hyperframes check` is not a visual gate. It passes compositions that render nothing: a blank plot
produces no error, no warning and no layout finding, because an empty render is a valid render. No
criterion below may rest on `check` alone.

### The mount harness

Three ways to get a false verdict from a working item, all of them the harness's fault. Build the
shell like this or the audit invents defects.

1. **Two shapes of item, two ways to mount.** If the file, with HTML comments stripped, contains a
   `data-composition-id`, it is a sub-composition: mount it with
   `data-composition-src="./<name>.html"` on a clip. If it does not, it is a snippet: paste it
   inline inside a `class="clip"` div. Inlining a sub-composition nests a document in a document
   and renders black, which reads exactly like a dead item.
2. **Use the item's own ground.** Take the background off its `demo.html` body rule. A snippet
   whose ink defaults to `#18181b` is a 16:1 headline on its own `#f7f7f8` and an invisible 1.5:1
   smudge on a dark stage. The stage is not evidence.
3. **Load GSAP and register a paused root timeline**, then snapshot with
   `hyperframes snapshot . --at 0.05,1.2,2.5,4.0 --no-end` and read the contact sheet.

An item whose own `data-duration` is shorter than the shell's will be blank in the last frames.
That is arithmetic, not a defect.

## Fatal, cut the item

Fatal means there is nothing worth keeping underneath the defect: no edit short of writing a
different item fixes it, or the fix produces something the catalog already ships. Cite the named
evidence; a fatal verdict without it does not count.

**F1. Does not implement its own description.** The markup contains no trace of the subject the
item is named and described for. Not "renders badly", but "the thing is absent from the file".
`ecosystem-constellation`, `hero-device-assemble` and `terminal-to-browser-deploy` are the same
file holding empty card divs with different headings.
_Check:_ read the markup, then swap the name for any other item's name. If nothing in the file
would have to change, the name is a label on a generic shell.
_Evidence:_ the named subject has no element (no nodes in a constellation, no terminal in a
terminal deploy).

**F2. Redundant duplicate.** Same **motion fingerprint** and same **markup skeleton** as another
item that survives. Fingerprint is the gsap call list with selectors neutralised, keeping props,
durations and eases; skeleton is the tag sequence with classes and text stripped. One wipe
currently ships eight times with the same properties, durations and easings; one word-stagger
ships seven times.
_Evidence:_ both hashes match a sibling, and the sibling wins the tie-break below.

**F3. Renders nothing.** Frames are blank, or the named subject never appears, with the item
mounted correctly on its own ground and its recipe applied.
_Evidence:_ four blank frames plus the cause, in the item rather than the harness: a missing
sibling asset, a `ReferenceError` in the console, a subject that never enters the viewport. A
frame-capture artifact that renders correctly live is a false alarm, so confirm on a real page
before recording it.

**F4. The description is a different item.** The frames show the promised event never happening: a
wipe that never reveals its second panel, a chart that draws no series. Not a wording gap.

**F5. Cannot be made seekable.** Frame N genuinely depends on frame N-1 with no closed form and no
bounded replay, and making it seekable would make it a different effect. Rare. Most accumulators
have a trivial rewrite, so reach for this only after establishing there is none; a seeded,
index-derived replacement for `Math.random()` is X7, not F5.
_Evidence:_ two snapshots of the same timestamp reached by different seek paths differ.

## Fixable, keep and repair

Real defects, but the item has a reason to exist that nothing else covers and the repair is
bounded. Log the specific fix, never "needs polish".

**X1. No timeline of its own.** No `__timelines` registration, so the installed artifact renders a
still frame while the catalog page looks fine, because the generator transplants the demo's
timeline into the preview. 97 of the 213 new components are in this state.
_Repair:_ fold the trailing `Timeline integration:` recipe into a real `<script>` that builds a
paused timeline and registers it. Roughly 10 to 15 minutes for a single-element item.
_Escalates to fatal_ only when there is no motion anywhere to fold in, which usually means F1 too.

**X2. Name claims a technique the code lacks.** Grep the code region, never the doc header: the
header's prose is full of the exact words you are looking for, and will report a match on an item
that has none.
| Name pattern | Must contain |
| -------------------------------- | -------------------------------------------------- |
| `spring-*` | `elastic`, `back.`, `bounce` or a custom spring ease |
| `mask-*`, `*-mask*` | `mask` or `clip-path` |
| `frosted*`, `*glass*` | `backdrop-filter` |
| `*3d*`, `*depth*`, `*orbit*`, `*camera*` | `perspective`, `rotateX`, `rotateY`, `translateZ` |
| `*-draw`, `*-trace`, `*stroke*` | `stroke-dash` or `pathLength` |
_Repair:_ add the technique, or rename the item. Renaming is often the honest fix.

**X3. Illegible.** At 1920x1080 on its own ground: text under 4.5:1, or a subject whose smallest
meaningful feature is under about 24px.
_Repair:_ one value step, per `placeholder-material.md`. Text never sits below L1.

**X4. Placeholder gradients.** The purple and blue palette standing in for content.
_Repair:_ the monochrome ramp. Already done across the catalog, so a new instance is a regression,
not a legacy defect.

**X5. Hardcoded ink, no theme token.** A literal colour on the item's own text or subject with no
`var(--...)` fallback chain, so it disappears when an author drops it on the opposite theme.
_Repair:_ route it through the theme token with the literal as fallback.

**X6. No markup of its own.** The file is a `<style>` and a `<script>` and nothing else, so
mounting it renders an empty box.
_Repair:_ ship sample markup, or declare it an attachment snippet in `registry-item.json` and give
the demo a host element.

**X7. Unseeded randomness.** Scatter derived from `Math.random()` rather than the element index.
_Repair:_ derive from the index.

**X8. Declared bounds it cannot honour.** A number variable with no `min`/`max`, so the control
offers values the item cannot express, or a default it can never return to.
_Repair:_ declare real bounds, or use a numeric field instead of a slider.

## Duplicates, which one survives

A group is the set of items sharing both hashes from F2. Exactly one survives, chosen in order:

1. **The one whose name describes what the shared motion actually does.** A group where one member
   is a directional wipe and the rest borrowed it keeps the directional wipe.
2. **Then the one with subject-specific markup.** More elements that only make sense for that
   name, not more elements.
3. **Then the one already on `origin/main`.** Removing a shipped item breaks installs.
4. **Never a member whose name claims something the shared implementation does not do.**
   `frosted-glass-wipe` has no `backdrop-filter`, `spring-scale-in` has no spring, `mask-reveal-up`
   has no mask, so none of those three is the survivor. Such a member is F2 and X2 at once, and X2
   cannot be fixed without breaking the group. If no member is honest, keep the plainest name.

**If every member of a group fails F1, the group is cut entire.** Do not preserve a survivor to
soften the count. Twelve names on one empty card shell is one bad item, not twelve, and keeping one
of them keeps the bad item.

Same motion with genuinely different subjects is not a duplicate. A bar chart, a line chart and a
dashboard populate can share a stagger; the subject is the item.

## Never cut

Protection is per criterion, not blanket. A protected item still answers every other row.

**N1. Load-bearing colour** is exempt from X4 only. `chromatic-aberration-wipe` (the RGB split is
the effect), `confetti` (multi-hue is the celebration), `matrix-decode` (green is its identity),
`mesh-gradient-bg` (the gradient is the subject), `multi-device-splay`. `us-map`'s gradient is a
sequential choropleth scale, which is colour carrying data.

**N2. Real product depiction** is exempt from X4 and F1. A Figma logo inside a Figma mock is not
slop; the HyperFrames wordmark in `logo-brand-close` is the subject. Judge the placeholder content,
not the depicted product.

**N3. Deliberate static** is exempt from X1. An item whose description promises no motion is not
failing X1. A style snippet or a passive overlay is allowed to sit still.

**N4. Environment sets** are exempt from F3. An item that is a backdrop rather than a shot is not
failing F3 for being calm. Measured PSNR between frames separates the two: sets score 45 or higher,
things that genuinely run score 17 to 24. Judge against the description.

**N5. A rest state that is the recipe's `from` state** is exempt from F3. `confetti` ships
`.particle` spans sitting at opacity 0 until the timeline fans them out. Still is not dead.

**N6. Attachment snippets** are exempt from F3. A text splitter has no markup by design. Grade X6.

**N7. The 36 items already on `origin/main`** are out of audit scope.

## Mechanical first pass

| Signal              | How                                                                                   | Maps to |
| ------------------- | ------------------------------------------------------------------------------------- | ------- |
| No timeline         | `grep -L __timelines` over each composition                                           | X1      |
| Duplicate           | motion fingerprint AND markup skeleton hashes, matched pairwise                       | F2      |
| Empty shell         | markup skeleton matches an unrelated item, or is `<h3>` + `<p>` + generic panels only | F1      |
| No markup at all    | element count of the comment-, style- and script-stripped file is 0                   | X6      |
| Placeholder palette | grep the six banned hexes                                                             | X4      |
| Name gap            | the X2 table, grepped over the code region only                                       | X2      |
| Unbounded number    | read `min`/`max` in `registry-item.json`                                              | X8      |
| Non-determinism     | grep `Math.random`, `Date.now`, `performance.now`, `requestAnimationFrame`            | X7, F5  |

## Visual pass, required for a verdict

Render at least four frames across the duration from the **composition**, not the demo, mounted per
the harness rules above, and look at them. Then, for anything not scoring clean, confirm on the
real catalog page before recording it.

Record per item: the criteria it fails, the evidence you saw, and fatal or fixable. An unviewed
item is not a pass.

## Calibration

Ten items scored with this rubric, frames rendered and looked at. Three of them corrected the
rubric rather than the other way round.

| Item                         | Expected   | Frames actually showed                                                                                                    | Verdict            |
| ---------------------------- | ---------- | ------------------------------------------------------------------------------------------------------------------------- | ------------------ |
| `ecosystem-constellation`    | fatal      | Sidebar with three pill buttons and three empty white panels. No nodes, no edges. Identical at all four timestamps.       | **Cut** F1, F2, F4 |
| `terminal-to-browser-deploy` | fatal      | Pixel-identical to the above, only the `<h3>` and one subtitle differ. No terminal, no browser.                           | **Cut** F1, F2, F4 |
| `frosted-glass-wipe`         | fatal      | One card reading "Before", static, forever; the "After" panel stays clipped. Recipe byte-identical to `directional-wipe`. | **Cut** F2, F4, X2 |
| `char-slam-explode`          | pass       | Letters scattered at 0.05s, assembled into "Impact" by 1.2s, held. Real per-character motion.                             | **Keep**           |
| `echo-trail`                 | pass       | Card travels left to right with a decaying blurred echo trail behind it. Legible on its own light ground.                 | **Keep**           |
| `logo-brand-close`           | pass       | "H" resolves into the full wordmark, tagline and URL land after it. Staged, legible.                                      | **Keep**           |
| `blur-in`                    | borderline | Still, but the still is the correct rest state: legible headline, unique implementation, theme-token ink.                 | **Keep**, X1       |
| `spring-scale-in`            | borderline | Legible on its own `#f7f7f8`. Ease is `power3.out`, no spring anywhere. Shares its recipe with six others.                | **Cut** F2, X2     |
| `confetti`                   | borderline | Card and mesh, no particles visible. Source ships `.particle` spans the recipe fans out from opacity 0.                   | **Keep**, X1       |
| `bottom-up-letters`          | borderline | Four blank frames. The file is a splitter with no markup at all.                                                          | **Keep**, X6       |

Three corrections the calibration forced, all of them false cuts:

- `spring-scale-in` first scored X3 at roughly 1.5:1. That was the harness's dark stage, not the
  item. Hence "use the item's own ground".
- `confetti` first scored F3. Its rest state is its recipe's `from` state. Hence N5.
- `char-slam-explode` first scored F3 with four black frames. It is a sub-composition and was being
  inlined. Hence the two-shapes rule.

A rubric that cuts a working item is wrong even when the verdict is convenient.

## Checklist

Per item, in order. Stop at the first fatal.

- [ ] Mounted the right way for its shape, on its own ground, with GSAP and a paused root.
- [ ] F1: the markup contains the named subject.
- [ ] F2: motion fingerprint and markup skeleton are not both shared with a survivor.
- [ ] F3: it renders something with the recipe applied, or it is protected by N3 to N6.
- [ ] F4: the frames show the event the description promises.
- [ ] F5: frame N is computed from N.
- [ ] X1 through X8 logged with the specific fix.
- [ ] Verdict cites the evidence the criterion names, not an impression.


<!-- ===== FILE: hyperframes/hyperframes-registry/references/contributing.md ===== -->

# Contributing a Block or Component to the Registry

Guide the user from idea to merged PR for a new registry block or component.

## Workflow

```
1. Clarify → 2. Scaffold → 3. Build → 4. Validate → 5. Preview → 6. Ship
```

### Step 1: Clarify

Ask what they're building. The registry has two item types:

- **Block** (`registry/blocks/`, type `hyperframes:block`) — a full standalone composition with fixed dimensions and duration. Caption styles, VFX effects, title cards, lower thirds.
- **Component** (`registry/components/`, type `hyperframes:component`) — a reusable snippet with no fixed dimensions or duration. CSS effects, text treatments, overlays that adapt to any composition size.

Then ask:

- One-sentence description of the effect
- Visual reference (URL, screenshot, or description)
- Who uses this and when?

### Step 2: Scaffold

Create the registry structure:

**For blocks:**

```
registry/blocks/{block-name}/
  {block-name}.html
  registry-item.json
```

**For components:**

```
registry/components/{component-name}/
  {component-name}.html
  registry-item.json
```

**Naming convention:**

| Item name        | ID prefix | Example IDs            |
| ---------------- | --------- | ---------------------- |
| `cap-hormozi`    | `hz`      | `hz-cg-0`, `hz-cw-3`   |
| `cap-typewriter` | `tw`      | `tw-cg-0`, `tw-ch-0-5` |
| `vfx-chrome`     | `vc`      | `vc-canvas`            |

Use a 2-3 letter prefix. ALL element IDs must use this prefix to avoid collisions in sub-compositions.

**registry-item.json** — use the canonical templates in [templates.md](templates.md) (block and component variants, both with all required fields).

### Step 3: Build

Apply the correct template based on type. See [templates.md](templates.md) for copy-paste starters.

#### Caption blocks

**Non-negotiable caption rules:**

- Font: **96px minimum** for proportional fonts. **64-72px acceptable for monospace** (wider characters need less size).
- Readability: `-webkit-text-stroke: 2-3px` OR multi-layer `text-shadow`
- Overflow: call `window.__hyperframes.fitTextFontSize()` on every group
- Karaoke: highlight active word via `tl.to(wordEl, { color/scale }, WORDS[wi].start)`
- Hard kill: `tl.set(groupEl, { opacity: 0, visibility: "hidden" }, g.end)` on EVERY group
- **Never use `tl.from(el, { opacity: 0 })` at the same position as `tl.set(el, { opacity: 1 })`** — the from clobbers the set. Use `tl.to` instead.

**Per-character animation** (typewriter, scramble):

- Wrap each character in `<span>` with ID `{prefix}-ch-{group}-{char}`
- Stagger via `tl.set` at computed intervals from word timestamps
- Cursors/decorative elements: use `tl.set` at intervals — NOT CSS animation (not seekable)

**Positioning variants:**

- Centered: `display: flex; align-items: center; justify-content: center;`
- Lower-third: `position: absolute; bottom: 100px; left: 0; width: 100%; text-align: center;`
- Left-aligned: `position: absolute; bottom: 100px; left: 120px; text-align: left;`

#### VFX blocks (Three.js)

- Use `three@0.147.0` from CDN (global script)
- `tl.eventCallback("onUpdate", renderScene); renderScene();` — NO requestAnimationFrame
- State proxy pattern: GSAP animates plain JS object, render function reads it
- Seeded PRNG (`mulberry32`) for randomness

#### All types

- **Load files the block ships through `__hyperframes.assetUrl("assets/...")`** whenever a script
  builds the path (textures, fonts, JSON, models). Attributes like `src` and `href` are rebased
  when the block is mounted; strings in a script are not, so a bare `"assets/..."` 404s once the
  block lives under `compositions/<name>/`. A separate `.js` file gets the URLs from the block's
  inline script. A block whose assets install to the project's own `assets/` (target
  `compositions/<name>.html`) keeps plain project-root paths; `assetUrl` would look beside the file.
- **Placeholder content is monochrome** — read
  [placeholder-material.md](placeholder-material.md) before choosing a single colour. Stand-in
  screens, images, cards, avatars, logos and chart series use four alpha steps of the
  composition's ink; accent marks one element and never a placeholder.
- `data-composition-id` MUST match `window.__timelines["id"]`
- All element IDs prefixed with block abbreviation
- `gsap.timeline({ paused: true })` — always paused
- No `Math.random()`, no `Date.now()`

### Step 4: Validate

```bash
hyperframes lint                    # 0 errors required
hyperframes check --no-contrast  # 0 console errors required
```

### Step 5: Preview

```bash
# Render preview video
hyperframes render -o preview.mp4

# Snapshot for visual QA
hyperframes snapshot --at "1.0,3.0,5.0,7.0"

# Publish to hyperframes.dev for review
npx hyperframes publish
```

**Catalog preview image** — For the default PNG preview, save your snapshot at `docs/images/catalog/{kind}/{name}.png` in the repository checkout (`{kind}` is `blocks` or `components`). After upload, the catalog serves it from `https://static.heygen.ai/hyperframes-oss/docs/images/catalog/{kind}/{name}.png`. If `registry-item.json` declares `preview`, the card uses its `poster` URL; a `preview` without `poster` has no image fallback.

- **HeyGen internal contributors:** run `scripts/upload-docs-images.sh` from the repository root (requires AWS profile `engineering-767398024897`)
- **External contributors:** attach the preview MP4 to your PR description. A maintainer will generate and upload the catalog image before merging.

### Step 6: Ship

**All steps are required. Missing any one produces a broken catalog entry.**

`{kind}` is `blocks` or `components` depending on what you built in Step 1.

```bash
# 1. Create branch
git checkout -b feat/registry-{name}

# 2. Format HTML
npx oxfmt registry/{kind}/{name}/*.html

# 3. Regenerate registry/registry.json from the item directories.
#    Do not hand-edit it: an entry added by hand survives until the next
#    regeneration and then vanishes, and one left behind for a directory that
#    no longer exists is worse, because `hyperframes add <name>` resolves the
#    name and then fails on missing files.
npx tsx scripts/generate-registry-items.ts

# 4. Generate catalog docs page
npx tsx scripts/generate-catalog-pages.ts

# 5. Publish to hyperframes.dev so reviewers can preview
npx hyperframes publish

# 6. Stage everything
git add registry/{kind}/{name}/ registry/registry.json docs/catalog/

# 7. Commit
git commit -m "feat(registry): add {name} — {one sentence}"

# 8. Push and open PR with hyperframes.dev link
git push origin feat/registry-{name}
gh pr create --title "feat(registry): {name}" --body "preview: {hyperframes.dev-url}"
```

**If you don't have a GitHub account:** you need one to open a PR. Sign up at https://github.com/signup, then run `gh auth login`.

## Quality Gate

- [ ] `hyperframes lint` → 0 errors
- [ ] `hyperframes check` → 0 console errors
- [ ] `npx oxfmt --check` passes
- [ ] `registry/registry.json` updated with new entry
- [ ] `scripts/generate-catalog-pages.ts` run (docs page generated)
- [ ] `npx hyperframes publish` run (claim your project URL)
- [ ] Preview MP4 attached to PR (external) or catalog PNG uploaded (internal)
- [ ] All IDs unique and prefixed


<!-- ===== FILE: hyperframes/hyperframes-registry/references/demo-html-pattern.md ===== -->

# The demo.html Convention

## Why components ship demo.html

Every component in the registry ships a companion `demo.html` file alongside its snippet. The demo serves two purposes:

1. **Preview fixture** — the CI preview pipeline renders the demo to generate thumbnail images and preview videos for the catalog docs page.

2. **Usage example** — the demo shows the component effect applied to representative content, serving as a working reference.

## Demo structure

A demo is a complete, standalone HTML composition:

```html
<!doctype html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=1920, height=1080" />
    <title>Component Name — Demo</title>
    <script src="https://cdn.jsdelivr.net/npm/gsap@3.14.2/dist/gsap.min.js"></script>
    <style>
      /* reset + canvas size */
    </style>
  </head>
  <body>
    <div data-composition-id="<name>-demo" data-width="1920" data-height="1080" data-duration="N">
      <!-- Demo content showing the effect -->
      <!-- Component snippet inlined here -->
    </div>
    <script>
      // GSAP timeline demonstrating the effect
      window.__timelines = window.__timelines || {};
      window.__timelines["<name>-demo"] = tl;
    </script>
  </body>
</html>
```

Key conventions:

- `data-composition-id` is `<component-name>-demo` to avoid collisions
- The demo is self-contained — all CSS and JS from the snippet is inlined
- The GSAP timeline is registered on `window.__timelines`
- Duration should be long enough to showcase the effect (typically 5-8 seconds)

## Blocks don't need demo.html

Blocks are already standalone compositions that can be rendered directly. Only components need the demo wrapper.

## Demos are not installed

The `demo.html` is NOT installed by `hyperframes add` — it exists only in the registry for preview generation and as a reference.


<!-- ===== FILE: hyperframes/hyperframes-registry/references/discovery.md ===== -->

# Registry discovery

<!-- registry-items: allow=data-composition-id,data-start,data-track-index -->

## Use the catalog command first

```bash
npx hyperframes catalog
npx hyperframes catalog --type block
npx hyperframes catalog --type component
npx hyperframes catalog --type block --tag social
npx hyperframes catalog --json
npx hyperframes catalog --human-friendly
```

- Default output is a readable table. It does not install anything.
- `--type` accepts `block` or `component`; `--tag` may narrow either result.
- `--json` is the deterministic agent and CI surface. Select a name, then run `npx hyperframes add <name>`.
- `--human-friendly` opens a picker and installs the selected item immediately.

## Read the registry manifest as a fallback

When the CLI is unavailable, the top-level `registry.json` lists all available items:

```bash
curl -s https://raw.githubusercontent.com/heygen-com/hyperframes/main/registry/registry.json
```

Each entry has `name` and `type` (`hyperframes:example`, `hyperframes:block`, or `hyperframes:component`).

## Reading an item's manifest

Each item has a `registry-item.json` with full metadata:

```
<base>/<type-dir>/<name>/registry-item.json
```

Where `<type-dir>` is `examples`, `blocks`, or `components`.

## Item manifest fields

| Field                  | Type     | Required | Description                                    |
| ---------------------- | -------- | -------- | ---------------------------------------------- |
| `name`                 | string   | yes      | Kebab-case identifier                          |
| `type`                 | string   | yes      | `hyperframes:block` or `hyperframes:component` |
| `title`                | string   | yes      | Human-readable title                           |
| `description`          | string   | yes      | One-line description                           |
| `tags`                 | string[] | no       | Filter tags (e.g., `["data", "chart"]`)        |
| `dimensions`           | object   | blocks   | `{ width, height }` — blocks only              |
| `duration`             | number   | blocks   | Duration in seconds — blocks only              |
| `files`                | array    | yes      | Files to install (`path`, `target`, `type`)    |
| `registryDependencies` | string[] | no       | Other registry items this depends on           |

## Available items

### Blocks

For an always-current list run `npx hyperframes catalog --type block`. **The search is the source of truth; the tables below are a hand-maintained sample and under-cover by design** — they group 97 of the registry's 180 blocks by category, so a block missing from them is not evidence the registry lacks it. Only an empty `npx hyperframes catalog --query "<what you want>" --json` is that evidence. Do not grow these tables toward the full set; search instead. **Block name ≠ shader name**: shader-transition blocks (e.g. `domain-warp-dissolve`) wrap a HyperShader runtime whose internal name omits the `-dissolve`/`-warp` suffix — see the showcase HTML installed alongside the block for the canonical name.

#### Shader transitions (14)

Single-shader blocks; each installs one HyperShader runtime + a showcase composition. Use ≤2 per video.

| Name                     | Description                                                              |
| ------------------------ | ------------------------------------------------------------------------ |
| `chromatic-radial-split` | Chromatic aberration radial split                                        |
| `cinematic-zoom`         | Dramatic zoom blur                                                       |
| `cross-warp-morph`       | Cross-warped morphing                                                    |
| `domain-warp-dissolve`   | Fractal noise domain warping                                             |
| `flash-through-white`    | White flash crossfade (rarely a neutral default — see GUIDE.md guidance) |
| `glitch`                 | Digital glitch artifacts                                                 |
| `gravitational-lens`     | Gravitational lensing distortion                                         |
| `light-leak`             | Cinematic light leak overlay                                             |
| `ridged-burn`            | Ridged turbulence burn                                                   |
| `ripple-waves`           | Concentric ripple wave distortion                                        |
| `sdf-iris`               | Signed-distance-field iris reveal                                        |
| `swirl-vortex`           | Swirling vortex distortion                                               |
| `thermal-distortion`     | Heat-haze thermal distortion                                             |
| `whip-pan`               | Fast camera whip-pan                                                     |

#### Transition galleries (13)

Showcase compositions grouping multiple CSS / GSAP transition styles by family. Use as reference for picking a CSS scene transition; not meant to embed as-is.

| Name                      | Description                         |
| ------------------------- | ----------------------------------- |
| `transitions-3d`          | 3D perspective flip and rotate      |
| `transitions-blur`        | Blur-based scene transitions        |
| `transitions-cover`       | Cover / uncover slide               |
| `transitions-destruction` | Destructive break-apart             |
| `transitions-dissolve`    | Dissolve and fade                   |
| `transitions-distortion`  | Warp and distortion                 |
| `transitions-grid`        | Grid-based tile                     |
| `transitions-light`       | Light-based glow and flash          |
| `transitions-mechanical`  | Mechanical shutter and iris         |
| `transitions-other`       | Misc creative (VHS, gravity, morph) |
| `transitions-push`        | Push and slide                      |
| `transitions-radial`      | Radial wipe and reveal              |
| `transitions-scale`       | Scale and zoom                      |

#### Liquid Glass (7)

WebGPU + html-in-canvas frosted-glass surfaces. **Require Brave / Chrome canary** with WebGPU enabled — set `PRODUCER_HEADLESS_SHELL_PATH` to point at the browser; engine auto-passes `--enable-unsafe-webgpu`. See `/hyperframes-animation` → `adapters/typegpu.md`.

| Name                        | Description                                                                             |
| --------------------------- | --------------------------------------------------------------------------------------- |
| `ios26-liquid-glass`        | 3D iPhone (GLTF) + iOS 26 home screen, glass app icons, shader wallpaper, notifications |
| `macos-tahoe-liquid-glass`  | 3D MacBook (GLTF) + macOS Tahoe-style desktop, glass menu bar, Finder, dock             |
| `liquid-glass-widgets`      | Frosted stat cards, showcase panel, pill chips over aurora shader                       |
| `liquid-glass-notification` | Frosted notification cards floating over aurora shader                                  |
| `vfx-liquid-glass`          | Bare VFX composition shell for liquid-glass effects                                     |

#### VFX (6)

HTML-in-canvas + WebGL composition blocks. See `/hyperframes-animation` → `adapters/three.md` and `adapters/html-in-canvas-patterns.md` for the underlying APIs.

| Name                    | Description                                                                                             |
| ----------------------- | ------------------------------------------------------------------------------------------------------- |
| `vfx-iphone-device`     | GLTF iPhone 15 Pro Max + MacBook Pro with live HTML-in-canvas screens, glass-lens morph, 360° turntable |
| `vfx-liquid-background` | Organic liquid sim — vertex displacement on subdivided plane, HTML floats above                         |
| `vfx-magnetic`          | VFX shell (magnetic field-line treatment)                                                               |
| `vfx-portal`            | VFX shell (portal reveal)                                                                               |
| `vfx-shatter`           | VFX shell (shatter into fragments)                                                                      |
| `vfx-text-cursor`       | Cursor glow + chromatic shadow rays + spectral edges on a black stage                                   |

#### Showcases (6)

Story-driven showcase compositions — narrated YouTube-style inserts. Most include bundled SFX.

| Name                       | Description                                                       |
| -------------------------- | ----------------------------------------------------------------- |
| `app-showcase`             | Three floating smartphone screens, fitness app product showcase   |
| `apple-money-count`        | Counter $0 → $10,000, green flash, money-icon burst, SFX          |
| `blue-sweater-intro-video` | Warm AI-creator intro resolving into an X follow card             |
| `north-korea-locked-down`  | Map zoom with red scribble circle, locked-down pop-up label       |
| `nyc-paris-flight`         | Map animation, plane NYC → Paris, marker circle, landing pop, SFX |
| `vpn-youtube-spot`         | App-store scroll, VPN install flow, SFX                           |

#### Maps + data viz (8)

D3 + GSAP animated geographies and charts.

| Name                               | Description                                                                                        |
| ---------------------------------- | -------------------------------------------------------------------------------------------------- |
| `us-map`                           | US choropleth, staggered state reveals, value labels, gradient legend                              |
| `us-map-bubble`                    | US bubble map — proportional city markers, callouts, connection lines                              |
| `us-map-flow`                      | US flow map — animated origin-destination arcs                                                     |
| `us-map-hex`                       | US hex-grid map — each state as equal-weight hex with data fill                                    |
| `spain-map`                        | Spain choropleth by autonomous community — D3 conic conformal                                      |
| `world-map`                        | World choropleth + rotating globe inset, D3 Natural Earth                                          |
| `data-chart`                       | Animated bar + line chart, staggered reveal, NYT-style typography                                  |
| `flowchart` / `flowchart-vertical` | Decision tree, SVG connectors, sticky-note nodes, cursor + typing correction (vertical = portrait) |

#### Social overlays (7)

Platform-recognizable UI overlays. Stamp on top of a beat or use as a beat closer.

| Name                 | Description                                      |
| -------------------- | ------------------------------------------------ |
| `instagram-follow`   | Profile card + follow button                     |
| `tiktok-follow`      | Profile card + follow button                     |
| `yt-lower-third`     | YouTube subscribe lower third with avatar        |
| `x-post`             | X/Twitter post card with engagement metrics      |
| `reddit-post`        | Post card with upvotes and comments              |
| `spotify-card`       | Now-playing card with album art and progress bar |
| `macos-notification` | macOS-style banner with app icon and message     |

#### Branding + 3D UI (2)

| Name           | Description                                                         |
| -------------- | ------------------------------------------------------------------- |
| `logo-outro`   | Piece-by-piece logo assembly, glow bloom, tagline fade-in, URL pill |
| `ui-3d-reveal` | Perspective 3D reveal for UI elements                               |

#### Code snippets (24)

A code/terminal window that **types a code or shell session per-character**. Theme = visual chrome only; structure, wiring, and install are identical across all 24 — pick one by name, wire it like any block (`data-composition-id` + `data-start` + `data-track-index`, see `wiring-blocks.md`). Two chrome families:

**Apple Terminal (12)** — macOS Terminal.app window typing a shell session. Profile = window colors:

| Name                              | Look                             |
| --------------------------------- | -------------------------------- |
| `code-snippet-apple-terminal-pro` | Black bg, grey text, lime cursor |

#### Code Animations (9)

The richer, motion-first counterpart to the static `code-snippet-*` window themes above: each is a self-contained 1920×1080 block (~5–8s) with a paused, deterministic GSAP timeline that _animates_ code — typing, diffing, morphing, spotlighting, or GPU hero reveals — rather than typing a fixed snippet inside editor/terminal chrome. **Reuse-first**: `npx hyperframes add <name>`, then customize the baked code/diff content in place; hand-author only when no block covers the motion you need.

**DOM / text reveal (6):**

| Name             | Description                                                                                                                |
| ---------------- | -------------------------------------------------------------------------------------------------------------------------- |
| `code-typing`    | Token-streamed typing reveal, caret tracks the frontier (no CSS animation) — live-coding on screen                         |
| `code-diff`      | An edit shown as a colored diff: removed lines collapse red, added expand green — before/after at line level               |
| `code-morph`     | One snippet transforms into another, tokens glide between positions (Shiki Magic Move) — a refactor / one state to another |
| `code-highlight` | A highlight band sweeps a target line while surrounding context dims — spotlight one line                                  |
| `code-scroll`    | Camera scrolls a long file to center + spotlight a target line — walk through a real module                                |

**GPU / WebGL hero reveals (3):** heavier, for a title-card / hero code moment.

| Name                     | Description                                                                                                     |
| ------------------------ | --------------------------------------------------------------------------------------------------------------- |
| `code-3d-extrude`        | Syntax-highlighted code on a lit beveled 3D slab that rotates through real space and settles (true WebGL depth) |
| `code-shader-dissolve`   | Code resolves out of seeded noise with a chromatic dissolve front + edge glow, then holds crisp                 |
| `code-particle-assemble` | Thousands of GPU points fly to the exact glyph pixels and resolve into readable syntax-highlighted code         |

### Components

| Name                 | Description                                                                                               | Tags                                             |
| -------------------- | --------------------------------------------------------------------------------------------------------- | ------------------------------------------------ |
| `grain-overlay`      | Animated film grain texture overlay                                                                       | texture, grain, overlay, film                    |
| `shimmer-sweep`      | CSS gradient light sweep for AI accents                                                                   | text, shimmer, highlight, effect                 |
| `morph-text`         | Gooey text morph cycling an editable word list (SVG threshold + GSAP blur)                                | text, text-effect, typography, morph, gooey      |
| `grid-pixelate-wipe` | Grid dissolve transition between scenes                                                                   | transition, wipe, grid, pixelate                 |
| `parallax-zoom`      | Center card scales up to fill the frame while siblings parallax outward (single `--pz-progress` 0→1)      | transition, zoom, parallax, grid, hero           |
| `parallax-unzoom`    | Reverse of `parallax-zoom` — focus card shrinks from full frame as siblings parallax in (`--pu-progress`) | transition, reveal, unzoom, parallax, grid, hero |


<!-- ===== FILE: hyperframes/hyperframes-registry/references/install-locations.md ===== -->

# Install Locations

## Default paths

| Item type | Default install path                  | Configured by                       |
| --------- | ------------------------------------- | ----------------------------------- |
| Block     | `compositions/<name>.html`            | `hyperframes.json#paths.blocks`     |
| Component | `compositions/components/<name>.html` | `hyperframes.json#paths.components` |

## How path remapping works

The `target` field in each item's `registry-item.json` specifies a default install path. The `add` command remaps the prefix based on `hyperframes.json#paths`:

- Block targets starting with `compositions/` get remapped to `<paths.blocks>/`
- Component targets starting with `compositions/components/` get remapped to `<paths.components>/`

## hyperframes.json

Created automatically by `hyperframes init`. If it doesn't exist when you run `add`, the CLI creates it with defaults:

```json
{
  "$schema": "https://hyperframes.heygen.com/schema/hyperframes.json",
  "registry": "https://raw.githubusercontent.com/heygen-com/hyperframes/main/registry",
  "paths": {
    "blocks": "compositions",
    "components": "compositions/components",
    "assets": "assets"
  }
}
```

## Custom layouts

To install blocks into a `scenes/` directory instead of `compositions/`:

```json
{
  "paths": {
    "blocks": "scenes"
  }
}
```

Then `hyperframes add data-chart` writes to `scenes/data-chart.html` instead of `compositions/data-chart.html`. The snippet output reflects the remapped path.


<!-- ===== FILE: hyperframes/hyperframes-registry/references/placeholder-material.md ===== -->

# Placeholder material

Registry items ship with stand-in content: a rectangle where the user's screenshot goes, a
bar where their number goes, a chip where their teammate's face goes. That stand-in is
**placeholder material**, and it is monochrome. No hue, no colour ramps, no purple-to-blue
diagonal fill.

The rule exists because placeholder colour is always arbitrary. A violet card, a blue logo
tile and a rainbow avatar row assert a brand the composition does not have; across 250 items
the same three arbitrary hues become the catalog's identity instead of the author's. Value
says everything colour was saying here, and says it truthfully.

## The one rule

> Placeholder content carries no hue. It is built from four alpha steps of the composition's
> own ink over the composition's own ground, plus a hairline. Accent marks one element per
> composition, and never a placeholder.

## The ramp

Four fill steps and a hairline. All of them are the ink at an alpha, so the ramp inverts for
free on dark themes and needs no second table.

| Step   | Ink alpha | What it is for                                                               |
| ------ | --------- | ---------------------------------------------------------------------------- |
| `ink`  | 100%      | Real content: headline, number, label. Not placeholder.                      |
| `L1`   | 72%       | The subject. Chart bars, a filled logo mark, a play glyph, a front avatar.   |
| `L2`   | 45%       | Support. A comparison series, avatars behind the front one, secondary icons. |
| `L3`   | 18%       | Media fill and skeleton text lines. "Content lives here."                    |
| `L4`   | 8%        | Recessed plate interiors. The tray a card sits in.                           |
| `hair` | 14%       | Every 1px boundary. Replaces the separation a gradient edge was doing.       |

Write them the way the file already writes colour:

```css
/* theme-token primitives (--fg / --surface available) */
background: color-mix(in srgb, var(--fg, #f8fafc) 18%, transparent);

/* fixed-palette ports (local --hf-ink, no theme tokens) */
background: rgba(17, 24, 39, 0.18);
```

**Four steps, not eight.** Grays go muddy when adjacent steps sit close together, so every
step is at least 1.6x the alpha of the one below it. Reaching for a fifth value is the signal
that the layout, not the palette, needs the work. Snap to the nearest step instead.

Contrast, measured against both shipped grounds (`neutral` light `#fcfcfd`, `bold` dark
`#1b1230`): L1 is 7.7:1 / 8.9:1, L2 is 3.1:1 / 4.4:1, L3 and L4 are below 3:1 by design.
Therefore **text never goes below L1**, and L2 is the floor for any graphic a viewer has to
compare (a chart series, a state indicator). L3 and L4 are for surfaces only.

## Depth without colour

In priority order. Reach for the first one that works.

1. **Value step.** Nothing sits on the same step as its ground. One full step of separation
   minimum. This alone resolves most stacking.
2. **Hairline.** `1px` of `hair` on every plate boundary. A border separates two surfaces more
   cleanly than a gradient ever did, and survives video compression that eats a soft edge.
3. **Negative space.** Padding is elevation. A plate with `--space-2` inside it reads as raised
   without any fill difference at all.
4. **Texture, at the finest grain only.** A `repeating-linear-gradient` at `L3`-and-below,
   period 2-4px, achromatic. This is the one thing value cannot say: a flat gray rectangle
   reads as an empty box, the same rectangle finely hatched reads as a surface with content on
   it. Use it to mark media, nothing else.

Shadows are allowed and must be achromatic and diffuse: `0 Npx 3Npx rgba(0,0,0,0.18)`. Never a
coloured glow; a glow is an accent wearing a shadow's clothes.

## Reading each kind in black and white

A gray rectangle has to still say _screen_ and not _image_. Shape, aspect, glyph and texture
carry the meaning that hue was carrying badly.

| Kind            | Signature                                                                                                                                |
| --------------- | ---------------------------------------------------------------------------------------------------------------------------------------- |
| Screen / device | Device aspect + `--radius` + `hair` + scanline texture at L3 + inset vignette. The chrome is the signal; the fill is L3 and stays quiet. |
| Video footage   | Screen signature plus a centred play triangle in a ring at L1. The glyph is what makes it video rather than a static screen.             |
| Image           | 4:3 or 3:2 plate at L3 with a horizon-and-disc glyph at L2, offset toward a corner, never centred. Offset is what reads as "photo".      |
| Card            | Plate at L4, `hair` border, two skeleton rules at L3 (100% and 62% width). Two rules of unequal length is the whole idiom.               |
| Avatar / person | **Circle** at L2 with initials knocked out in the ground colour. Stacks differ by step (L1 front, L2, L3), never by hue.                 |
| Logo / brand    | **Rounded square** at L1 with the mark knocked out in the ground colour. Every mark on the same step: a logo wall means "many, equal".   |
| Chart series    | Flat fills. Primary series L1, comparison series L2, gridlines `hair`. Never a gradient inside a bar.                                    |
| Text block      | Rounded rules at L3, widths 100 / 86 / 62%. The ragged right edge is what reads as prose.                                                |

Circle means person, rounded square means app or brand. Keeping those two shapes distinct is
what lets both live at the same value step without ambiguity.

Why no gradient inside a chart bar: a vertical light-to-dark fill makes every bar lighter at
its top, so the tallest bar reads _palest_ exactly where the eye lands to compare heights. The
decoration contradicts the data. Flat fills are both plainer and more honest.

## Accent

The accent enum stays. `green` rides `--brand`, `blue` rides `--accent`, `violet` rides
`--accent-2`, exactly as before, and every declared `accent` or `tone` variable keeps working
unchanged. What changes is where accent is allowed to land:

> Accent marks at most **one** element per composition, and only where the accent _is_ the
> meaning: the selected tier, the current step, the figure a count-up lands on, the ink of a
> stroke being drawn. Placeholder content is never accent-coloured.

Fixed-palette ports have no theme tokens, so they get the accent through their own
variable with a neutral fallback:

```css
/* was: --hf-accent: #2563eb; */
--hf-accent: var(--accent, #18181b);
```

Unthemed, the item renders in pure black and white. Drop it into a themed composition and
the author's accent lands on that one element and nowhere else. Where the accent is chosen by
an enum, the lookup table maps to tokens, never to hex: `green` to `var(--brand, <neutral>)`,
`blue` to `var(--accent, <neutral>)`, `violet` to `var(--accent-2, <neutral>)`. The enum's
declared options and default are unchanged, so no mount breaks.

"One element" means one role, not one node: an app mark repeated on three devices of the same
mock is still one element.

Killing accent outright was the alternative and it is worse. Accent is already load-bearing in
exactly the cases where it is correct, and it is the only hook an author has for their own
brand; removing it would push those cases into value tricks for a job one hue does better with
one element. The failure was never that accent existed, it was that accent had become the
default fill for every placeholder. Capping it at one element fixes the failure with no
variable migration.

## Gradients that stay

The ban is on **hue-carrying fills**, not on the CSS function. These are material, not
placeholder, and flattening them breaks the thing the item exists to do:

- **Physical surfaces** — device bezels, brushed metal, glass, a screen's inner vignette.
- **Sheens and sweeps** — `linear-gradient(90deg, transparent, rgba(255,255,255,0.75), transparent)`
  driven across an element. That is motion, not decoration.
- **Scrims and vignettes** — `rgba(0,0,0,α)` ramps that buy text contrast over media.
- **Effects whose subject is the gradient** — aurora, liquid glass, chromatic aberration,
  grain fields, shader transitions. The gradient is the product.

All four are achromatic or physically motivated. If a gradient is neither, it is placeholder
slop and it goes.

## Checklist

- [ ] No `#7c3aed`, `#2563eb`, `#6366f1`, `#8b5cf6`, `#a855f7`, `#4f46e5` anywhere in the item.
- [ ] Every placeholder fill is `ink` at 72 / 45 / 18 / 8 / 14 percent, and nothing else.
- [ ] At most one accent-coloured element, and it means something.
- [ ] Text sits at L1 or above; L3 and L4 carry no text.
- [ ] Every remaining gradient is a surface, a sweep, a scrim, or the effect itself.
- [ ] `hyperframes check` passes, and a rendered frame was looked at.


<!-- ===== FILE: hyperframes/hyperframes-registry/references/templates.md ===== -->

# Contribute Templates

Copy-paste starter templates for each component type. These embed the proven patterns that pass `lint` and `check`.

## Caption Template

```html
<!doctype html>
<html lang="en">
  <head>
    <meta charset="utf-8" />
    <link
      href="https://fonts.googleapis.com/css2?family=Montserrat:wght@800;900&display=swap"
      rel="stylesheet"
    />
    <script src="https://cdn.jsdelivr.net/npm/gsap@3.14.2/dist/gsap.min.js"></script>
    <style>
      *,
      *::before,
      *::after {
        margin: 0;
        padding: 0;
        box-sizing: border-box;
      }
      body {
        background: #111;
        overflow: hidden;
      }
      #root-BLOCKNAME {
        position: relative;
        width: 1920px;
        height: 1080px;
        overflow: hidden;
        background: #111;
      }
      .cap-container {
        position: absolute;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        display: flex;
        align-items: center;
        justify-content: center;
      }
      .cg {
        position: absolute;
        display: flex;
        align-items: center;
        justify-content: center;
        gap: 32px;
        max-width: 1700px;
        overflow: visible;
        opacity: 0;
        visibility: hidden;
      }
      .cw {
        font-family: "Montserrat", sans-serif;
        font-weight: 900;
        font-size: 128px;
        color: #ffffff;
        text-transform: uppercase;
        line-height: 1;
        display: inline-block;
        -webkit-text-stroke: 3px rgba(0, 0, 0, 0.8);
        paint-order: stroke fill;
        text-shadow: 0 4px 12px rgba(0, 0, 0, 0.5);
      }
    </style>
  </head>
  <body>
    <div
      id="root-BLOCKNAME"
      data-composition-id="BLOCKNAME"
      data-start="0"
      data-duration="9"
      data-width="1920"
      data-height="1080"
    >
      <div class="cap-container" id="cc-BLOCKNAME"></div>
      <div
        id="drv-BLOCKNAME"
        class="clip"
        data-start="0"
        data-duration="9"
        data-track-index="0"
        style="position:absolute;width:1px;height:1px;opacity:0;pointer-events:none"
      ></div>
    </div>
    <script>
      (function () {
        window.__timelines = window.__timelines || {};

        // REPLACE with actual transcript data
        var WORDS = [
          { text: "Welcome", start: 0.3, end: 0.65 },
          { text: "to", start: 0.65, end: 0.8 },
          { text: "the", start: 0.8, end: 0.95 },
          { text: "future", start: 0.95, end: 1.4 },
          // ... add all words
        ];

        var GROUPS = [
          { start: 0.3, end: 1.3, wordStart: 0, wordEnd: 3, text: "Welcome to the future" },
          // ... add all groups
        ];

        var container = document.getElementById("cc-BLOCKNAME");

        GROUPS.forEach(function (g, gi) {
          var groupEl = document.createElement("div");
          groupEl.id = "PREFIX-cg-" + gi;
          groupEl.className = "cg";

          for (var wi = g.wordStart; wi <= g.wordEnd; wi++) {
            var wordEl = document.createElement("span");
            wordEl.id = "PREFIX-cw-" + wi;
            wordEl.className = "cw";
            wordEl.textContent = WORDS[wi].text;
            groupEl.appendChild(wordEl);
          }

          // Pretext overflow prevention
          if (window.__hyperframes && window.__hyperframes.fitTextFontSize) {
            var _fit = window.__hyperframes.fitTextFontSize(g.text.toUpperCase(), {
              fontFamily: "Montserrat",
              fontWeight: 900,
              maxWidth: 1550,
              baseFontSize: 128,
              minFontSize: 48,
            });
            if (_fit.fontSize < 128) {
              for (var _fi = 0; _fi < groupEl.children.length; _fi++) {
                groupEl.children[_fi].style.fontSize = _fit.fontSize + "px";
              }
            }
          }
          container.appendChild(groupEl);
        });

        var tl = gsap.timeline({ paused: true });

        GROUPS.forEach(function (g, gi) {
          var groupEl = document.getElementById("PREFIX-cg-" + gi);

          // SHOW — set opacity to 1 (never use tl.from with opacity:0 here)
          tl.set(groupEl, { opacity: 1, visibility: "visible" }, g.start);

          // ENTRANCE — customize this per style
          tl.from(groupEl, { scale: 1.3, duration: 0.15, ease: "back.out(2)" }, g.start);

          // KARAOKE — highlight each word
          for (var wi = g.wordStart; wi <= g.wordEnd; wi++) {
            var wordEl = document.getElementById("PREFIX-cw-" + wi);
            tl.to(wordEl, { color: "#FFD700", scale: 1.1, duration: 0.06 }, WORDS[wi].start);
            tl.to(wordEl, { color: "#FFFFFF", scale: 1, duration: 0.08 }, WORDS[wi].end);
          }

          // EXIT
          tl.to(groupEl, { opacity: 0, scale: 0.9, duration: 0.1 }, g.end - 0.1);

          // HARD KILL (mandatory)
          tl.set(groupEl, { opacity: 0, visibility: "hidden" }, g.end);
        });

        window.__timelines["BLOCKNAME"] = tl;
      })();
    </script>
  </body>
</html>
```

**Replace checklist:**

- `BLOCKNAME` → your block name (e.g., `cap-swoosh`)
- `PREFIX` → short unique prefix for IDs (e.g., `sw`)
- Font family, weight, size → your style's typography
- Entrance animation → your style's entrance
- Karaoke highlight → your style's active word treatment
- Colors → your style's palette

---

## VFX Template

```html
<!doctype html>
<html lang="en">
  <head>
    <meta charset="utf-8" />
    <script src="https://cdn.jsdelivr.net/npm/gsap@3.14.2/dist/gsap.min.js"></script>
    <script src="https://cdn.jsdelivr.net/npm/three@0.147.0/build/three.min.js"></script>
    <style>
      *,
      *::before,
      *::after {
        margin: 0;
        padding: 0;
        box-sizing: border-box;
      }
      body {
        background: #030308;
        overflow: hidden;
      }
      #root-BLOCKNAME {
        position: relative;
        width: 1920px;
        height: 1080px;
        overflow: hidden;
        background: #030308;
      }
      #canvas-BLOCKNAME {
        position: absolute;
        top: 0;
        left: 0;
        width: 1920px;
        height: 1080px;
      }
    </style>
  </head>
  <body>
    <div
      id="root-BLOCKNAME"
      data-composition-id="BLOCKNAME"
      data-start="0"
      data-duration="10"
      data-width="1920"
      data-height="1080"
    >
      <canvas id="canvas-BLOCKNAME" width="1920" height="1080"></canvas>
      <div
        id="drv-BLOCKNAME"
        class="clip"
        data-start="0"
        data-duration="10"
        data-track-index="0"
        style="position:absolute;width:1px;height:1px;opacity:0;pointer-events:none"
      ></div>
    </div>
    <script>
      (function () {
        window.__timelines = window.__timelines || {};

        // Seeded PRNG — NEVER use Math.random()
        function mulberry32(a) {
          return function () {
            a |= 0;
            a = (a + 0x6d2b79f5) | 0;
            var t = Math.imul(a ^ (a >>> 15), 1 | a);
            t = (t + Math.imul(t ^ (t >>> 7), 61 | t)) ^ t;
            return ((t ^ (t >>> 14)) >>> 0) / 4294967296;
          };
        }
        var rng = mulberry32(42);

        var W = 1920,
          H = 1080;
        var canvas = document.getElementById("canvas-BLOCKNAME");
        var renderer = new THREE.WebGLRenderer({ canvas: canvas, antialias: true });
        renderer.setSize(W, H);
        renderer.setPixelRatio(1);
        renderer.toneMapping = THREE.ACESFilmicToneMapping;
        renderer.toneMappingExposure = 1.1;

        var scene = new THREE.Scene();
        scene.background = new THREE.Color(0x030308);
        var camera = new THREE.PerspectiveCamera(50, W / H, 0.1, 100);
        camera.position.set(0, 0, 8);

        // YOUR SCENE SETUP HERE
        // - lights
        // - geometry
        // - materials

        // State proxy — GSAP animates this, render reads it
        var st = {
          rotY: 0,
          camZ: 8,
          // add your animated properties
        };

        var tl = gsap.timeline({ paused: true });

        // YOUR TWEENS HERE
        tl.to(st, { rotY: Math.PI * 2, duration: 10, ease: "none" }, 0);

        window.__timelines["BLOCKNAME"] = tl;

        function renderScene() {
          // Apply state to Three.js objects
          camera.position.z = st.camZ;
          // mesh.rotation.y = st.rotY;

          renderer.render(scene, camera);
        }

        // Render via onUpdate — NO requestAnimationFrame
        tl.eventCallback("onUpdate", renderScene);
        renderScene();
      })();
    </script>
  </body>
</html>
```

**Replace checklist:**

- `BLOCKNAME` → your block name (e.g., `vfx-chrome-blob`)
- Scene setup → your geometry, lights, materials
- State proxy → your animated properties
- Tweens → your animation timeline
- renderScene → apply state to your Three.js objects

---

## registry-item.json Templates

**For blocks:**

```json
{
  "$schema": "https://hyperframes.heygen.com/schema/registry-item.json",
  "name": "BLOCKNAME",
  "type": "hyperframes:block",
  "title": "Human-Readable Title",
  "description": "One sentence: what it does and who uses it",
  "dimensions": { "width": 1920, "height": 1080 },
  "duration": 10,
  "tags": ["category", "subcategory"],
  "files": [
    {
      "path": "BLOCKNAME.html",
      "target": "compositions/BLOCKNAME.html",
      "type": "hyperframes:composition"
    }
  ]
}
```

**For components** (no `dimensions` or `duration`):

```json
{
  "$schema": "https://hyperframes.heygen.com/schema/registry-item.json",
  "name": "COMPONENTNAME",
  "type": "hyperframes:component",
  "title": "Human-Readable Title",
  "description": "One sentence: what it does",
  "tags": ["category"],
  "files": [
    {
      "path": "COMPONENTNAME.html",
      "target": "compositions/components/COMPONENTNAME.html",
      "type": "hyperframes:snippet"
    }
  ]
}
```

Tags by category:

- Captions: `captions`, `viral`, `professional`, `karaoke`, `minimal`
- VFX: `three-js`, `particles`, `shader`, `gpu`
- Transitions: `transition`, `shader`, `wipe`, `dissolve`
- Blocks: `lower-third`, `social`, `title-card`, `data-viz`
- Components: `effect`, `overlay`, `text-treatment`

---

## Component Template

```html
<!doctype html>
<html lang="en">
  <head>
    <meta charset="utf-8" />
    <script src="https://cdn.jsdelivr.net/npm/gsap@3.14.2/dist/gsap.min.js"></script>
    <style>
      *,
      *::before,
      *::after {
        margin: 0;
        padding: 0;
        box-sizing: border-box;
      }
      body {
        background: transparent;
        overflow: hidden;
      }
      .COMPNAME-wrap {
        position: absolute;
        inset: 0;
        overflow: hidden;
        pointer-events: none;
      }
    </style>
  </head>
  <body>
    <div class="COMPNAME-wrap">
      <!-- Your reusable effect/overlay here -->
    </div>
    <script>
      (function () {
        // Component snippet — no data-composition-id, no __timelines.
        // The parent composition controls timing.
        // Keep all class names and IDs prefixed with COMPNAME.
      })();
    </script>
  </body>
</html>
```

**Replace checklist:**

- `COMPNAME` → your component name (e.g., `shimmer-sweep`)
- Background should be `transparent` so it overlays cleanly
- No `data-composition-id` or `window.__timelines` — the parent owns timing


<!-- ===== FILE: hyperframes/hyperframes-registry/references/wiring-blocks.md ===== -->

# Wiring Blocks

Blocks are standalone compositions with their own `data-composition-id`, dimensions, duration, and GSAP timeline. Include them in a host composition using `data-composition-src` on a `<div>`.

## Basic wiring

After `hyperframes add data-chart`, wire it into your `index.html`:

```html
<div id="stage" data-composition-id="main" data-width="1920" data-height="1080" data-duration="20">
  <video id="a-roll" src="video.mp4" data-start="0" data-duration="20" data-track-index="0"></video>

  <!-- Block: appears at 2s, plays for 15s, on layer 1 -->
  <div
    data-composition-id="data-chart"
    data-composition-src="compositions/data-chart.html"
    data-start="2"
    data-duration="15"
    data-track-index="1"
    data-width="1920"
    data-height="1080"
  ></div>
</div>
```

## Required attributes

| Attribute              | Description                                                          |
| ---------------------- | -------------------------------------------------------------------- |
| `data-composition-src` | Path to the block HTML file (relative to index.html)                 |
| `data-composition-id`  | Unique ID matching the block's internal composition ID               |
| `data-start`           | When the block appears in the host timeline (seconds)                |
| `data-duration`        | How long the block plays (seconds, at most the block's own duration) |
| `data-track-index`     | Layer ordering — higher numbers render in front                      |
| `data-width`           | Block canvas width (match the block's dimensions)                    |
| `data-height`          | Block canvas height (match the block's dimensions)                   |

## Timeline coordination

The block's internal GSAP timeline runs independently from the host timeline. The HyperFrames runtime loads the sub-composition, finds its `window.__timelines` registration, and seeks the block in sync with the host, offset by `data-start`. You do NOT need to reference the block's timeline in your host's GSAP code.

## Positioning blocks

To position a block in a specific area of the screen, add CSS:

```html
<div
  data-composition-id="data-chart"
  data-composition-src="compositions/data-chart.html"
  data-start="2"
  data-duration="15"
  data-track-index="1"
  data-width="1920"
  data-height="1080"
  style="position: absolute; right: 0; top: 0; width: 40%; height: 100%;"
></div>
```

## Multiple blocks

Add additional `<div data-composition-src="...">` siblings with non-overlapping or overlapping `data-start` values — each block's timeline is independent and seeked in sync by the runtime.


<!-- ===== FILE: hyperframes/hyperframes-registry/references/wiring-components.md ===== -->

# Wiring Components

Components are effect snippets — HTML, CSS, and optionally JS that you merge directly into an existing composition. Unlike blocks, components have no standalone timeline; they participate in the host composition's timeline.

## General process

1. Run `hyperframes add <component-name>`
2. Open the installed file (e.g., `compositions/components/grain-overlay.html`)
3. Read the comment header for usage instructions
4. Copy the parts into your host composition:
   - **HTML elements** — inside your `<div data-composition-id="...">`
   - **CSS styles** — into your composition's `<style>` block
   - **JS setup** — into your composition's `<script>`, before your timeline code
   - **Timeline calls** — into your GSAP timeline (if the component exposes them)

## Example: grain-overlay (CSS-only, no timeline integration)

```html
<!-- Paste the overlay div into your composition -->
<div
  id="grain-overlay"
  style="position: absolute; top: 0; left: 0; width: 100%; height: 100%; pointer-events: none; z-index: 100;"
>
  <div class="grain-texture"></div>
</div>
```

Then paste the CSS keyframes and `.grain-texture` rule into your styles. No GSAP timeline calls needed — the grain animates via CSS `@keyframes`.

## Example: shimmer-sweep (needs timeline integration)

See `examples/add-component.md` for the full shimmer-sweep walkthrough (HTML wrapping, CSS, JS setup, and timeline call).

## Key principles

- Components inherit the host composition's dimensions and duration
- Place component HTML at the appropriate z-index relative to your content
- Read the comment header in each snippet for customizable values
- Run `hyperframes lint` after wiring to catch structural issues
