---
name: motion-graphics
description: Unified motion graphics and programmatic video skill combining Remotion (React) and HyperFrames (HTML + GSAP) knowledge. Use for any request to make, edit, animate, caption, or render a video — kinetic typography, explainers, product launch promos, logo reveals, lower-thirds, captions/subtitles, slideshows, music-synced videos, data-viz, maps, 3D, transitions, voiceover, SFX, or porting Remotion to HyperFrames.
---

# Motion Graphics (Remotion + HyperFrames)

One router over two engines plus shared motion doctrine. Read this file, pick the engine, then load only the references the task needs.

## 1. Pick the engine

| Situation | Engine |
| --- | --- |
| Project already has `remotion` in package.json, or user asks for React/Remotion | **Remotion** → `references/remotion-index.md` |
| Project already has `hyperframes.json` / HyperFrames HTML compositions, or user asks for HyperFrames | **HyperFrames** → `references/hyperframes--hyperframes.md` (mandatory entry) |
| User explicitly asks to convert Remotion → HyperFrames | `references/hyperframes--remotion-to-hyperframes.md` |
| Greenfield, inside a React/Vite/TanStack app (in-app player, editable from code) | Remotion |
| Greenfield, standalone render, heavy GSAP/Lottie/Three.js, or registry blocks wanted | HyperFrames |

Never mix both engines in one composition. Preserve user edits made outside the conversation.

### Scripts, templates and full tree
This upload is the knowledge-only edition (Lovable skill limits: 200 files, 1 MB each). Helper scripts (`.mjs/.cjs/.py/.sh`), HTML templates and JSON data live in the full edition: https://github.com/priceriteprinters-cell/video-skills/tree/main/motion-graphics — fetch a file from `https://raw.githubusercontent.com/priceriteprinters-cell/video-skills/main/motion-graphics/<original path>` into `/tmp` when a guide tells you to run or copy it.

### Path translation (upstream references were written as separate skills)
- `/skill-name` or "Unclear → /hyperframes" → `references/hyperframes--skill-name.md`
- `skills/<name>/...` → `references/hyperframes--<name>.md`; `skills/animate-text/...` → `references/hyperframes--hyperframes-animation.md`
- "Remotion Best Practices" → `references/remotion-index.md`; `remotion-<x>` skill → `references/remotion--remotion-<x>.md`
- Any `SKILL.md` mentioned upstream is named `GUIDE.md` here. Example media (png, fonts, mp3) were not bundled; fetch or generate replacements.

### Inside a Lovable / TanStack Start app
- Install `remotion` + `@remotion/player` and render `<Player>` from a lazily imported component behind `<ClientOnly>` (Remotion touches `window`). Keep `remotion`, `@remotion/*` versions identical.
- Verified pattern: `lazy(() => import("@/remotion/Player"))` inside `<ClientOnly><Suspense>` with an aspect-video fallback; pass `acknowledgeRemotionLicense`.
- Browsers may block `autoPlay` until a user gesture, and frame 0 is often empty (elements still entering). Set `initialFrame` to a readable frame or render a `renderPoster`, so the player never looks blank.
- Keep compositions in `src/remotion/`, pure functions of `useCurrentFrame()` / props. Rendering MP4 needs Node + Chromium (`npx remotion render`) or Remotion Lambda — not the Worker runtime.

## 2. Always apply motion doctrine (engine-agnostic)

Before choreographing, read:
- `references/doctrine--motion-doctrine.md` — core motion principles
- `references/doctrine--cut-the-curve.md` — easing and curve discipline
- `references/doctrine--seam-craft.md` — scene seams and transitions
- `references/hyperframes--motion-graphics.md` — design-led motion graphic workflow (ideas transfer to Remotion too)
- `references/hyperframes--hyperframes-creative.md` — palette, type, beats, narration

Universal rules: deterministic frame-driven animation only (no `Math.random()` without seed, no wall-clock timers, no CSS animations that ignore the timeline); every element enters, holds, and exits intentionally; 2–4 motion rules per scene; ease everything; plan beats before code.

## 3. Route by task

### Remotion
- New video / project: `references/remotion--remotion-create.md`
- Markup best practices (sequencing, timing, transitions, fonts, audio, 3D, lottie, effects, text): `references/remotion--remotion-markup.md`
- Captions: `references/remotion--remotion-captions.md`
- Maps: `references/remotion--remotion-maps.md`
- Media metadata / trimming: `references/remotion--remotion-multimedia.md`
- Studio interactivity: `references/remotion--remotion-interactivity.md`
- Rendering: `references/remotion--remotion-render.md`
- Studio (launch, URLs, CLI flags): `references/remotion--remotion-studio.md`
- Looking up Remotion docs/APIs: `references/remotion--remotion-docs.md`
- SaaS / Remotion Lambda / embedding videos in a product: `references/remotion--remotion-saas.md`
- Upgrading Remotion versions: `references/remotion--remotion-upgrade.md`

### Ready-made HyperFrames blocks (3D titles, carousels, camera moves)
`references/registry-blocks.md`, `references/registry-blocks.md`, `references/registry-blocks.md`, `references/registry-blocks.md`, `references/registry-blocks.md`, `references/registry-blocks.md`, `references/registry-blocks.md` — check these before hand-building a similar effect.

### HyperFrames
- Composition contract (read before writing HTML): `references/hyperframes--hyperframes-core.md`
- Animation rules, blueprints, GSAP/Lottie/Three.js adapters: `references/hyperframes--hyperframes-animation.md`
- Zoom / punch-in / reframe: `references/hyperframes--hyperframes-keyframes.md`
- Audio mixing: `references/hyperframes--hyperframes-audio.md`
- CLI loop (init, lint, snapshot, render): `references/hyperframes--hyperframes-cli.md`
- Registry blocks (check before hand-building named effects): `references/hyperframes--hyperframes-registry.md`
- Studio collaboration: `references/hyperframes--hyperframes-studio.md`
- Media (BGM, SFX, TTS, icons, LUTs): `references/hyperframes--media-use.md`
- Figma import: `references/hyperframes--figma.md`

### Workflows (format-level; adapt to Remotion if that engine is chosen)
- Faceless explainer from text: `references/hyperframes--faceless-explainer.md`
- Product launch / promo from URL: `references/hyperframes--product-launch-video.md`
- Music-synced / lyric video: `references/hyperframes--music-to-video.md`
- PR / changelog video: `references/hyperframes--pr-to-video.md`, `references/doctrine--changelog-video.md`
- Slideshow / deck: `references/hyperframes--slideshow.md`
- Captions on talking head: `references/hyperframes--embedded-captions.md`, `references/doctrine--captions-overlay.md`
- Graphic overlays on talking head: `references/hyperframes--talking-head-recut.md`
- Cursor-driven UI demos: `references/doctrine--oversized-cursor.md`
- Anything else: `references/hyperframes--general-video.md`

Each module file bundles a whole upstream folder. Sections start with `<!-- ===== FILE: <original path> ===== -->`; a link to another `.md` means: search for that path's FILE marker (it may be in another module file, or a `--partN.md` continuation).

## 4. Deliver

1. Show a live preview (Remotion Studio / `<Player>`, or HyperFrames Studio/snapshot) before rendering; render only when explicitly asked.
2. Verify: lint/check, scrub key frames, confirm no element pops without easing, text is legible for its on-screen duration, audio aligned to beats.
3. Report what was built and how to preview or render it.
