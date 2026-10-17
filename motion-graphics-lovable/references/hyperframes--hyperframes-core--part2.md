

<!-- ===== FILE: hyperframes/hyperframes-core/references/tracks-and-clips.md ===== -->

# Tracks and Clips

Clips are timed elements inside a composition. Tracks are a Studio display concept: the render never reads them.

## What is a Clip

A clip is any DOM element with `data-start` and, where required, `data-duration`. `data-track-index` is optional. Common kinds:

- **Visual `<div>` clips** — scenes, cards, overlays. Always require `data-duration`.
- **Sub-composition hosts** — `<div>` with `data-composition-src`. Always require `data-duration`.
- **Video clips** — `<video playsinline>`. With sound: `data-has-audio="true"` (the sound stays on the clip). Silent: `muted`. Duration can default to media length.
- **Audio clips** — `<audio>`. Duration can default to media length.
- **Image clips** — `<img>`. `data-duration` is optional and defaults to 3 seconds; write it only for another length.

Add `class="clip"` to authored visual clips. The runtime does not read it, but the scaffold's shared `.clip { position: absolute; inset: 0 }` rule is what gives a scene its full-frame box, Studio treats it as an edit hint, and `lint` warns without it.

## Tracks Are a Display Lane

`data-track-index` is the row a clip occupies in Studio's timeline. It is **not** read by the render, and it constrains nothing:

- **Two clips on the same track may overlap in time.** Nothing rejects it and the render is well defined: both are visible, painted in CSS order.
- **Visual layering (front/back)** is controlled by CSS `z-index`, not by track index.
- **Omitting it is fine.** The parser defaults it, and Studio then lays out one lane per clip.

A clip on track `5` is not "above" a clip on track `1`. Use CSS for layering, `data-start`/`data-duration` for sequencing.

The one place the value carries meaning: two `<audio>` elements that share a track index **and** overlap in time raise a `lint` warning (`duplicate_audio_track`), which is a useful nudge that you are about to double up a bed.

## Picking a Track Index

Purely a readability choice for whoever opens the file in Studio. Common patterns, owned by `/hyperframes-studio` (one caption track, one element kind per track).

When adding a clip to an existing composition, set its `data-start`/`data-duration` against the clips around it. You do not need to hunt for a free lane, and you never need to renumber tracks after a retime.

## Clip Time Inside the Composition

`data-start` is in seconds, measured from the start of the _composition_. For sub-compositions, the sub-composition's internal timeline (its own `data-duration` and child clips) runs from `data-start` to `data-start + data-duration` of the host.

`data-media-start` (on `<video>`/`<audio>`) is an offset _into the source media_. Use it to skip the first few seconds of a media file without trimming the file itself.

## Cut one source into multiple ranges

For a hard cut, trim, splice, or reorder, duplicate the same video source into
multiple clip elements. Each copy selects its source range with
`data-media-start` plus `data-duration`, and places that range on the authored
timeline with `data-start`. Change the source offsets and placement order; do
not try to keyframe source cutting.

Each video segment keeps its sound: the sound stays on the clip (`data-has-audio="true"`), so cutting the video cuts its sound. A separate `<audio>` is for other sound (music, voiceover, replacement audio, J/L cuts).

## Linked clips

`data-link="<id>"` marks clips that are edited as one: in Studio, moving, trimming, splitting or deleting one member does the same to the others. Detach audio in Studio produces a pair, a muted `<video>` and an `<audio>` over the same file:

```html
<video
  id="talk"
  src="talk.mp4"
  muted
  data-link="lk-1"
  data-sync-origin="lk-1"
  data-start="2"
  data-duration="6"
  data-media-start="1"
  data-track-index="0"
></video>
<audio
  id="talk-audio"
  src="talk.mp4"
  data-link="lk-1"
  data-sync-origin="lk-1"
  data-start="2"
  data-duration="6"
  data-media-start="1"
  data-track-index="2"
></audio>
```

- **Link offer.** Studio offers Link for exactly one video and one audio, neither already linked; their timing and source file don't matter. A linked pair that is offset moves together (the offset is kept), and a trim carries to the partner only when its edge sits at the same time. Merge back needs the same file and an in-sync pair.
- **Keep members in sync.** Every member needs the same `data-start`, `data-duration`, `data-media-start` (absent = 0) and `data-playback-rate` (absent = 1). Track index, volume, fades and FX may differ. When you retime one member by hand, retime all of them, or `lint` warns `linked_clips_out_of_sync`.
- **Unlink** by removing `data-link` from every member. Removing it from one leaves the other alone with the id, which `lint` flags as `linked_clip_orphan`.
- The render ignores `data-link`: an out-of-sync pair still plays exactly what its timings say.
- Prefer a single `<video data-has-audio="true">` for footage with sound. Link only when the sound needs its own clip (its own track, volume or FX); to undo a detach, move the audio attributes back onto the video and delete the `<audio>`.
- **Sync origin.** `data-sync-origin="<id>"` marks a video and an audio from one source file; Detach writes it, Link writes it only for a pair from one source file, and Unlink keeps it. When the pair drifts (their source-zero points, `data-start − data-media-start / data-playback-rate`, differ), Studio shows a red offset in frames on both halves with Move into Sync / Slip into Sync, `hyperframes timeline` prints `out-of-sync=±Nf`, and the SDK offers `syncOffset`, `moveIntoSync` and `slipIntoSync`. Leave it alone when retiming by hand; remove it only when the clips are no longer one source.
- `@hyperframes/sdk` `setTiming` applies to link partners by default; pass `{ linked: false }` to edit one member, which unlinks it.

## Relative Timing

`data-start` accepts a clip ID instead of a number, meaning "start when that clip ends". Add `+ N` / `- N` to offset; negative produces overlap (useful for crossfades).

```html
<video id="intro" data-start="0" data-duration="10" data-track-index="0" src="..."></video>
<video id="main" data-start="intro" data-duration="20" data-track-index="0" src="..."></video>
<video
  id="scene-a"
  data-start="intro + 2"
  data-duration="20"
  data-track-index="0"
  src="..."
></video>
<video
  id="scene-b"
  data-start="intro - 0.5"
  data-duration="20"
  data-track-index="1"
  src="..."
></video>
```

Rules, and three ways this fails **silently**. Nothing in `lint` checks any of them, so read them before you use a reference:

- **Spaces around the operator are required.** `data-start="intro - 0.5"` means "0.5s before `intro` ends". `data-start="intro-0.5"` (no spaces) is parsed as a reference to an element whose id is literally `intro-0.5`; that element does not exist, so the clip silently starts at 0.
- **An unresolved reference resolves to 0**, it does not error. A typo'd id, or a target that is not in the document, puts the clip at the start of the composition.
- **If the target has no resolvable duration, the reference lands on the target's START, not its end.** So `data-start="hero"` where `hero` has no `data-duration` and no known media length silently means "same time as `hero`" rather than "after `hero`".
- **A cycle resolves to 0** rather than erroring. `A → B → A` puts one of them at 0.
- Lookup is **document-wide** (`getElementById`, then `[data-composition-id]`). A reference can therefore reach a target in another composition on the assembled page. Keep referenced ids unique and keep the reference and its target in the same file, or the result depends on assembly order.
- A value that parses as a number is always absolute seconds. Otherwise the resolver expects `<id>`, `<id> + <number>`, or `<id> - <number>`.
- References can chain (`A → B → C`). Keep chains under 3-4 levels for readability.
- Negative offsets create overlap, which is allowed. Overlapping clips do **not** need different tracks.

Because every failure mode above is a silent 0, snapshot a reference-timed composition and check the clip actually starts where you meant.


<!-- ===== FILE: hyperframes/hyperframes-core/references/variables-and-media.md ===== -->

# Variables and Media

Two separate concerns, grouped because both control "what flows in from outside the HTML": runtime parameters (variables) and external media files (video/audio).

## Variables

Declare variables on the `<html>` element with `data-composition-variables`. Each declaration needs `id`, `type`, `label`, and `default`:

```html
<html
  data-composition-variables='[
    {"id":"title","type":"string","label":"Title","default":"Hello"},
    {"id":"accent","type":"color","label":"Accent","default":"#66d9ef"}
  ]'
></html>
```

**Prefer declarative bindings — no script needed** for direct substitution:

```html
<img class="clip" data-start="0" data-duration="5" data-var-src="heroImage" src="fallback.jpg" />
<h1 class="clip" data-start="0" data-duration="5" data-var-text="title">Fallback</h1>
<style>
  .card {
    color: var(--accent);
  }
</style>
```

- `data-var-src="id"` substitutes the element's `src` (URL string or image `{url}`); the authored `src` is the fallback.
- `data-var-text="id"` substitutes the element's own text; element children (nested clips, animated spans) are preserved.
- Every scalar variable is applied automatically as a `--{id}` CSS custom property on the composition root, so `var(--id)` CSS responds to overrides — no `setProperty` boilerplate.
- Bindings resolve identically in preview and render, and per-instance for sub-compositions.
- Caveat: media with audio should keep a real fallback `src` — render audio extraction reads the authored attribute (lint: `media_variable_src_no_fallback`).

For logic beyond direct substitution (loops, conditionals, derived values), read values once during initialization:

```js
const { title, accent } = window.__hyperframes.getVariables();
document.getElementById("title").textContent = title;
```

### Variable Rules

- Supported types and their extra options (consumed by Studio's editing UI):
  - `string` — optional `placeholder`, `maxLength`
  - `number` — optional `min`, `max`, `step`, `unit`
  - `color` — none
  - `boolean` — none
  - `enum` — **required** `options: [{ "value": "...", "label": "..." }, ...]`
- Always provide useful `default` values so preview works without CLI overrides.
- Use `data-variable-values='{"title":"Pro"}'` on sub-composition hosts for per-instance overrides.
- Use `npx hyperframes render --variables '{"title":"Q4 Report"}'` or `--variables-file` for render-time overrides.
- Add `--strict-variables` in CI: turns undeclared keys, type mismatches, and enum values not in `options` into errors instead of warnings.
- Read values once during init, not on every animation tick — variables don't change mid-render.
- Media color grading can use exact variable references inside `data-color-grading` JSON. Use `$gradingPreset` or `${gradingIntensity}` as the whole field value; the runtime resolves it from the current composition's variables before applying shader adjustments, finishing details, blur/pixelate effects, and custom LUTs.

### Two JSON Shapes (Easy to Confuse)

- `data-composition-variables` is an **array of declarations** (the schema): `[{id, type, label, default}, ...]`
- `--variables` and `data-variable-values` are **objects keyed by id** (the values): `{"title":"Q4","accent":"#fff"}`

## Media

**`<video>`/`<audio>` work at any nesting depth, including inside a sub-composition `<template>` or a wrapper `<div>`.** The runtime discovers media with a flat `document.querySelectorAll("video, audio")`, resolves each element's host composition via `element.closest("[data-composition-id]")`, and rebases its local `data-start` by the accumulated absolute start of every ancestor composition. A host at `2` with child media at `2` therefore starts that media at root time `4`, consistently in preview, snapshot, extraction, and render. Legacy projects that deliberately authored a media start in root time must mark that element with `data-hf-media-start-basis="global"`; never infer the basis from overlapping numbers. New compositions should always use scene-local `data-start`. If a panel renders blank after a render, capture a per-frame `snapshot` and treat it as render-blocking.

The one real constraint is about **timelines, not media placement**: a sub-composition timeline **cannot reach or animate host elements** — neither `document.querySelector("#host-id")` nor a gsap selector string (`tl.to("#host-id", …)`) resolves across the boundary; a sub-comp timeline only drives its own subtree. So if a media element lives at the host root, **its per-scene motion (scale/opacity/morph/tilt/breathing) must be authored on the MAIN timeline in `index.html`, at GLOBAL time** (scene-local time + the scene slot's `data-start`). Keeping the media inside the scene sub-comp instead lets that sub-comp's own timeline animate it with scene-local time. For 3D tilt without a perspective parent, use gsap `transformPerspective` on the element. See `composition-patterns.md` archetype B.

A video with sound keeps it on the `<video>` (`data-has-audio="true"`, no `muted`). Use a separate `<audio>` for music, voiceover, replacement audio, J/L cuts, or audio detached in Studio. Silent footage and b-roll: `muted`.

```html
<video
  id="a-roll"
  class="clip"
  src="assets/demo.mp4"
  playsinline
  data-has-audio="true"
  data-start="0"
  data-duration="12"
  data-track-index="0"
  data-volume="1"
></video>

<!-- Separate <audio> only for other sound: music, voiceover, replacement audio. -->
<audio
  id="music"
  src="assets/bed.mp3"
  data-start="0"
  data-duration="12"
  data-track-index="2"
  data-volume="0.4"
></audio>
```

### Media Rules

- **Do not** call `video.play()`, `audio.play()`, pause, or seek in composition code. HyperFrames owns playback.
- **Do not** drive host-root media from a sub-comp timeline: a sub-comp timeline cannot reach elements outside its subtree, so it has no effect. Drive host-root media from the main timeline at global time (or keep the media inside the sub-comp whose timeline animates it).
- **Do not** animate timed media element dimensions; animate a non-timed wrapper instead.
- **Do not** nest video inside a timed wrapper. `lint` rejects a `<video data-start>` whose ancestor also carries `data-start` (`video_nested_in_timed_element`, error), and the failure is real: the frame extractor resolves the video's start from its own `data-start` without the wrapper's offset, while visibility uses the wrapper's window. The clip then shows the wrong source frames and disappears partway through its slot. Put the timing on the wrapper **or** on the media element, never both.
- **Sub-compositions are exempt and work.** A `<video>`/`<audio>` inside a sub-composition renders identically to one at the host root, because a composition host propagates its offset. Only plain timed wrappers (a `<section data-start>` around a `<video data-start>`) break.
- **Never** add `crossorigin` to `<video>`/`<audio>`. `lint` rejects it unconditionally (`media_crossorigin_breaks_preview`, error) because a media host without `Access-Control-Allow-Origin` then fails silently in preview while renders still work, hiding the bug. There is no suppression, so this holds even for the canvas/WebGL/WebAudio readback case.
- **Every `<audio>` needs an `id`.** The mixer selects `audio[id][src]`, so an id-less `<audio>` is never mixed and the render is **silent**. `lint` catches it as `media_missing_id`.
- A video's own sound stays on the `<video>` (`data-has-audio="true"`, no `muted`). Add a separate `<audio>` only for other sound (music, voiceover, replacement audio, J/L cuts) and mute the video it replaces.
- For volume fades and ducking, use the `data-automation` volume lane; the exact form is in `creator-editing-recipes.md`. `data-volume` is the static baseline. A timeline `volume` tween is ignored when a lane is present.

For media duration: `<video>` and `<audio>` can omit `data-duration` if the media's intrinsic length is known and you want the full clip. Otherwise provide `data-duration` explicitly.

Input codecs: render decodes video via FFmpeg (frames are pre-extracted and injected), so HEVC/H.265 assets (8/10-bit) render correctly everywhere; live preview auto-proxies any browser-hostile asset (transcodes and caches an H.264 copy on first use, opt out with `--no-proxy` or `media.autoProxy: false`), and `lint` emits an info-level `hevc_preview_codec` note naming affected assets.
