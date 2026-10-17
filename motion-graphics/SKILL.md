---
name: motion-graphics
description: Unified motion graphics and programmatic video skill combining Remotion (React) and HyperFrames (HTML + GSAP) knowledge. Use for any request to make, edit, animate, caption, or render a video — kinetic typography, explainers, product launch promos, logo reveals, lower-thirds, captions/subtitles, slideshows, music-synced videos, data-viz, maps, 3D, transitions, voiceover, SFX, or porting Remotion to HyperFrames.
---

# Motion Graphics (Remotion + HyperFrames)

One router over two engines plus shared motion doctrine. Read this file, pick the engine, then load only the references the task needs.

## 1. Pick the engine

| Situation | Engine |
| --- | --- |
| Project already has `remotion` in package.json, or user asks for React/Remotion | **Remotion** → `references/remotion/GUIDE.md` |
| Project already has `hyperframes.json` / HyperFrames HTML compositions, or user asks for HyperFrames | **HyperFrames** → `references/hyperframes/hyperframes/GUIDE.md` (mandatory entry) |
| User explicitly asks to convert Remotion → HyperFrames | `references/hyperframes/remotion-to-hyperframes/GUIDE.md` |
| Greenfield, inside a React/Vite/TanStack app (in-app player, editable from code) | Remotion |
| Greenfield, standalone render, heavy GSAP/Lottie/Three.js, or registry blocks wanted | HyperFrames |

Never mix both engines in one composition. Preserve user edits made outside the conversation.

## 2. Always apply motion doctrine (engine-agnostic)

Before choreographing, read:
- `references/doctrine/motion-doctrine/GUIDE.md` — core motion principles
- `references/doctrine/cut-the-curve/GUIDE.md` — easing and curve discipline
- `references/doctrine/seam-craft/GUIDE.md` — scene seams and transitions
- `references/hyperframes/motion-graphics/GUIDE.md` — design-led motion graphic workflow (ideas transfer to Remotion too)
- `references/hyperframes/hyperframes-creative/GUIDE.md` — palette, type, beats, narration

Universal rules: deterministic frame-driven animation only (no `Math.random()` without seed, no wall-clock timers, no CSS animations that ignore the timeline); every element enters, holds, and exits intentionally; 2–4 motion rules per scene; ease everything; plan beats before code.

## 3. Route by task

### Remotion
- New video / project: `references/remotion/remotion-create/REFERENCE.md`
- Markup best practices (sequencing, timing, transitions, fonts, audio, 3D, lottie, effects, text): `references/remotion/remotion-markup/REFERENCE.md`
- Captions: `references/remotion/remotion-captions/REFERENCE.md`
- Maps: `references/remotion/remotion-maps/REFERENCE.md`
- Media metadata / trimming: `references/remotion/remotion-multimedia/REFERENCE.md`
- Studio interactivity: `references/remotion/remotion-interactivity/REFERENCE.md`
- Rendering: `references/remotion/remotion-render/REFERENCE.md`
- Other folders in `references/remotion/` cover docs, studio, and more — list them when needed.
- Standalone Remotion skills (full versions, use when the bundled router copy is thinner): `references/remotion-skills/{remotion-captions,remotion-create,remotion-docs,remotion-interactivity,remotion-maps,remotion-markup,remotion-multimedia,remotion-render,remotion-studio}/GUIDE.md`
- SaaS / Remotion Lambda / embedding videos in a product: `references/remotion-skills/remotion-saas/GUIDE.md`
- Upgrading Remotion versions: `references/remotion-skills/remotion-upgrade/GUIDE.md`

### Ready-made HyperFrames blocks (3D titles, carousels, camera moves)
`references/registry-blocks/{canopy-part-title,code-slice-hero,cuboid-carousel,frost-sequence-camera-orbit,glass-shard-title,orbit-card,wireframe-portal-title}/GUIDE.md` — check these before hand-building a similar effect.

### HyperFrames
- Composition contract (read before writing HTML): `references/hyperframes/hyperframes-core/GUIDE.md`
- Animation rules, blueprints, GSAP/Lottie/Three.js adapters: `references/hyperframes/hyperframes-animation/GUIDE.md`
- Zoom / punch-in / reframe: `references/hyperframes/hyperframes-keyframes/GUIDE.md`
- Audio mixing: `references/hyperframes/hyperframes-audio/GUIDE.md`
- CLI loop (init, lint, snapshot, render): `references/hyperframes/hyperframes-cli/GUIDE.md`
- Registry blocks (check before hand-building named effects): `references/hyperframes/hyperframes-registry/GUIDE.md`
- Studio collaboration: `references/hyperframes/hyperframes-studio/GUIDE.md`
- Media (BGM, SFX, TTS, icons, LUTs): `references/hyperframes/media-use/GUIDE.md`
- Figma import: `references/hyperframes/figma/GUIDE.md`

### Workflows (format-level; adapt to Remotion if that engine is chosen)
- Faceless explainer from text: `references/hyperframes/faceless-explainer/`
- Product launch / promo from URL: `references/hyperframes/product-launch-video/`
- Music-synced / lyric video: `references/hyperframes/music-to-video/`
- PR / changelog video: `references/hyperframes/pr-to-video/`, `references/doctrine/changelog-video/`
- Slideshow / deck: `references/hyperframes/slideshow/`
- Captions on talking head: `references/hyperframes/embedded-captions/`, `references/doctrine/captions-overlay/`
- Graphic overlays on talking head: `references/hyperframes/talking-head-recut/`
- Cursor-driven UI demos: `references/doctrine/oversized-cursor/`
- Anything else: `references/hyperframes/general-video/`

Each workflow folder has a `GUIDE.md` entry plus its own references; bundled `scripts/` are copied to `/tmp` before running.

## 4. Deliver

1. Show a live preview (Remotion Studio / `<Player>`, or HyperFrames Studio/snapshot) before rendering; render only when explicitly asked.
2. Verify: lint/check, scrub key frames, confirm no element pops without easing, text is legible for its on-screen duration, audio aligned to beats.
3. Report what was built and how to preview or render it.
