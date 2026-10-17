---
name: complete-video-production
description: Create or revise motion-graphics videos with selectable font pairings, coordinated palettes, downloadable authentic assets, and a narration-led timeline. Produce motion-graphics videos for any subject, including animated explainers, kinetic typography, educational videos, product walkthroughs, social videos, and animated promos. Use when asked to turn audio or a script into a video, synchronize animation to narration, add background music and timed SFX, or reproduce a complete motion-gfx production workflow. Also generates standalone AI PNG asset packs (verified motion-assets/v1 ZIP with scene mapping) and reuses attached packs. Covers briefing, transcription, scene timing, animation delegation, audio mixing, captions, rendering, verification, revisions, and delivery; not standalone generated footage or an app's video-generation feature.
---

# Complete Motion-Graphics Video Production

Create subject-agnostic motion graphics with a narration-first timeline, readable visuals, background music when requested, and sound effects synchronized to meaningful visual events. Preserve user-supplied content and disclose what was actually checked.

## Scope and inputs

Require a goal plus at least one of: an audio file, script, existing video to revise, or sufficiently specific topic/brief. Accept optional brand assets, reference images, audience, narration language, duration, platform, caption preference, music direction, SFX direction, and output destination. Always ask for and obtain aspect-ratio confirmation before producing any new video or revised export, even when a ratio was already supplied; never infer it from platform or source dimensions.

Interpret “realtime SFX” in a rendered-video request as effects synchronized to animation, not a live interactive application. Clarify only if the user clearly expects live generation or interactive playback.

Stay with motion graphics when that style is named. For a request that actually needs generated footage, live-action scenes, or an app that generates video for its users, use the matching platform skill rather than extending this pipeline. This skill is general across topics, not a guarantee that animation suits every video.

## Required creative briefing (ratio, font, palette, visual mode)

After any required style-routing question, ask these questions together and wait for answers before producing a video. This enhances the existing aspect-ratio confirmation; it does not remove it. These questions are for future video requests, not for installing this skill.

1. **What aspect ratio would you like for the video?** Offer 16:9 landscape, 9:16 portrait, 1:1 square, and Custom. If already supplied or making a revised export, explicitly offer to keep that ratio; never infer confirmation from the platform.
2. **Which font would you like to use?** Pick 3–4 varied, subject-relevant options from the 29 presets in `assets/design-presets.json` (span different moods: e.g. one clean, one editorial, one bold, one playful), plus Custom. **Always show a real font preview first:** run `design_tools.py preview --pairings <keys> --palette <likely palette> --title "<the video's actual headline>"`, render the HTML to PNG with a headless browser after `document.fonts.ready`, inspect it, save it to Files and show it with the question. Where a pairing has `tool_preview_preset`, also use that native fontPair preview in a visual-choice question. Re-preview any Custom font the same way before confirming. State which font serves headings, supporting text, and captions. Include “Choose for me” through the custom response when desired; explicit delegation authorizes a suitable choice, not silent substitution. Read [Typography and palette direction](references/typography-and-palettes.md) for curated pairings, previews, loading, licensing, and glyph checks.
3. **Which color palette or visual theme would you prefer?** Choose from the 24 palette presets (categories such as luxury, gaming, nature, corporate, playful, health, developer) and offer 3–4 subject-appropriate variants; vary across categories rather than near-duplicates, including light and dark options, with swatches and named background, text, primary accent, secondary accent roles. Include Custom and allow explicit creative delegation. The combined palette/theme question replaces separate light/dark and palette questionnaires.

4. **Dark or light visual mode?** Offer Dark, Light, and Match palette. Skip if the chosen palette already fixes it or the user said so.

In the same message, offer sensible defaults the user can simply approve for: overall visual style (e.g. editorial, tech, playful, cinematic), animation intensity (Subtle / Balanced / Energetic — see production-standards.md), and brand guidelines (ask them to attach any). Never re-ask anything already supplied. Do not start final production until these preferences are collected or explicitly delegated.

Use the question tool when available (max 4 questions per call); otherwise ask these same questions in one short message. For visual font previews, use actual supported font-pair presets only when they exactly match the offered pairing; otherwise use an ordinary choice, not a misleading preview. For palette previews, use swatch fields. Do not ask another mandatory question for details already known. If content is missing, request it in the same message or one genuinely blocking follow-up. Revisions can offer “Keep current” for each creative choice. Record exact answers and any explicitly delegated choices in the brief.

Use multiple complementary font families when they improve hierarchy: generally one display family plus one supporting family, with an optional mono or script-coverage family for a specific role. A single family remains a valid user choice; do not impose a universal one-font rule or mandatory San Francisco. Select only fonts whose files, required weights, license, glyph coverage, and renderer loading can be verified. Carry resolved font roles and exact semantic palette tokens into the handoff and QA.

## Resource and automation policy

Use the supplied [Free Design Resources — No Sign-Up Edition](references/free-design-resources-no-signup.md) as the primary discovery reference for fonts, logos, icons, illustrations, photos, audio, and other assets. Read [Resource acquisition](references/resource-acquisition.md) before fetching external assets: directory claims are leads, not proof of current access or usage rights. Prefer authentic assets; download relevant logos and supporting visuals when needed, rather than substituting generic shapes or guessed marks.

Own the acquisition of every required asset: search, download, inspect, and stage it proactively. The catalog is a starting point, not a closed list. If suitable assets are missing, search additional lawful public internet sources; if no suitable visual remains available after a real search, use the current image-generation tool to create an illustrative PNG and inspect it. Do not stop at the first failed source or routinely send users away to collect assets. Generated images never substitute for an authentic logo, genuine screenshot, actual demonstration, or verified evidence; use a clearly labeled illustration or neutral diagram instead when authenticity cannot be established. Follow the detailed fallback ladder in resource-acquisition.md and disclose genuine tool/rights blockers.

Read [Automation tools](references/automation-tools.md) when preparing a production brief or acquiring assets. The bundled Python helper provides preset listings, confirmed-brief validation, contrast checks, provenance-tracked HTTPS downloads, Simple Icons/Iconify retrieval, and self-hosted licensed font acquisition. It is not a renderer and does not guarantee legal clearance or video quality. Use current platform asset and production tools for rendering and permitted specialist handoff.

When an asset ZIP is attached, read [Attached asset-pack intake](references/asset-pack-intake.md) and [Pack contract](references/asset-pack-contract.md) before sourcing or delegating. Recognize the `motion-assets/v1` manifest, validate and safely extract actual PNGs, review context/scene coverage, and start from suitable included assets. Do not run archive scripts or treat an installation ZIP as imagery.

## Asset-pack mode

Use this mode when the user wants only the PNG assets for a video (no render), or wants all illustrative assets generated before production.
1. Read the script/audio/storyboard; ask for a topic if absent. Use the same three-question brief (ratio, font, palette); fonts stay live renderer choices, never baked into art.
2. Read [Asset-pack generation design](references/asset-pack-generation-design.md). Build a needs table: stable ID, scene IDs, purpose, framing, dimensions, transparency, provenance, status. Avoid near-duplicates and static cards per sentence.
3. Generate actual images with the current image tool (respect its batch limit), keeping palette, lighting, perspective and line style consistent; edit/reference earlier images for continuity. Transparent PNG for cutouts, opaque for backgrounds; convert non-PNG output with a trusted tool (renaming is not conversion).
4. Inspect every image at full size (subject, edges, alpha, stray text, distortion); repair via edits. No counterfeit logos, fabricated screenshots, or fake evidence.
5. Stage only reviewed PNGs, write `asset-pack.json`, and run `scripts/asset_pack.py` pack + validate per [Pack contract](references/asset-pack-contract.md). No external URLs, prompts, or credentials inside.
6. Inspect ZIP entries separately, deliver as `application/zip`, summarize assets and provenance. Say "complete pack" only when every planned row is included and reviewed; otherwise label it partial and list gaps. In a full production run, import the pack directly and continue the workflow.

## Integrated video-creator routing

Apply this routing before the production brief; it incorporates the platform video-creator workflow without replacing its current runtime rules:

1. Playing, embedding, uploading, or repairing an existing video, interface motion, and in-app generation features stay with app code and the matching app skill.
2. A named motion-graphics/animation style goes directly to this detailed workflow. The user's motion-graphics preference is the default here; do not ask about style again unless a fresh request genuinely leaves both production styles open.
3. If both styles fit and neither is named or established, ask the style question before other briefing questions. Use exactly one visual-choice question with exactly two options: **Motion graphics**, preset `video-motion-graphics`, description “Animated text, logos, shapes and images, with precise timing and layout”; **Generated scenes**, preset `video-generated-scenes`, description “AI-generated scenes and movement, from realistic footage to illustrated or surreal worlds.” Localize these labels/descriptions to the user's language. Use no generated previews or additional preview fields. If visual choice is unavailable, use a plain choice; if questions are unavailable, ask in chat. Wait for the answer, then ask the three-question creative brief before production.
4. Motion-graphics ads, explainers, text-heavy videos, and walkthroughs use the animation specialist. Generated-scene ads/promos/commercials use the current ad-video skill; read its body if not loaded. Only if that skill does not exist, use one generated clip.
5. A standalone generated scene, stylized clip, social scene, or cover video uses the current video-generation tool and its supplied rules, not this renderer. Do not substitute still images for footage or claim generation is unavailable without trying the designated tool. Report actual returned duration and audio availability.

The detailed references below govern motion graphics. Generated-scene routing is a handoff, not authorization to bypass the user's English text, authentic-asset, aspect-ratio, or truthful-delivery requirements. Consult current generative-video guidance for prompt, reference-image, model, and refusal rules rather than freezing changing provider details here.

## Required reference map

Read only the references needed for the job, but read all listed mandatory stages before handing off production:

| Stage | Read | When |
|---|---|---|
| Intake and assets | [Brief and asset intake](references/brief-and-assets.md) | Every new video or revision |
| Attached asset ZIP | [Attached asset-pack intake](references/asset-pack-intake.md) and [Pack contract](references/asset-pack-contract.md) | Before importing an attached/generated asset bundle |
| Timing and storyboard | [Narration and scene timing](references/timing-and-storyboard.md) | Every narrated video; also for text-only timing |
| Visual production | [Motion design and rendering](references/motion-and-rendering.md) | Every animation |
| Soundtrack | [Audio production and mixing](references/audio-and-mixing.md) | Whenever narration, music, or SFX is present |
| Tool handoff | [Production delegation](references/delegation.md) | Before starting the animation task |
| Verification and delivery | [Quality assurance and recovery](references/qa-and-delivery.md) | Every export, including revisions |
| Typography and palette | [Typography and palette direction](references/typography-and-palettes.md) | Before offering font/theme choices and composing scenes |
| Asset discovery | [Supplied resource catalog](references/free-design-resources-no-signup.md) and [Resource acquisition](references/resource-acquisition.md) | Before sourcing external fonts, logos, imagery, motion, 3D, or sound |
| Reusable helpers | [Automation tools](references/automation-tools.md) | Before downloading assets or validating a structured brief |
| Research and script audit | [Research, transcription, and script audit](references/research-and-script-audit.md) | Every video with a topic, script, or audio |
| Production standards | [Production-ready standards and premium motion](references/production-standards.md) | Every video: art direction, asset quality gate, zero-placeholder rule, full QA, delivery package |
| Calibration example | [Captured workflow and lessons](references/captured-workflow.md) | When reproducing the original workflow or understanding its limitations |

## End-to-end workflow

1. **Extract the brief, confirm aspect ratio, and obtain visual choices.** Separate supplied facts from creative choices. State the intended result briefly. Ask the three-question creative brief above; wait for the user's selections and resolve the chosen font roles and palette before production. Apply English-only authored text unless another language is explicitly requested, and search for authentic assets before considering generated fallbacks.
2. **Research, transcribe, and audit.** Read [Research, transcription, and script audit](references/research-and-script-audit.md). Transcribe supplied audio first (flag unclear spans), research every checkable claim with cross-checked authoritative sources, collect visual references, then audit the script. Apply mechanical fixes; get approval for meaning-affecting changes; ask about unresolvable ambiguities. Never silently change intended meaning.
3. **Inspect inputs.** Locate files, probe media duration/streams, transcribe speech, inventory visual assets, and identify every subject that needs a matched authentic visual. Do not infer narration from a filename.
   For asset ZIPs, validate and inspect before extraction; use mapped existing PNGs first and resolve only genuine coverage gaps. Create a scene-level asset ledger and do not hand off missing paths or unresolved required inputs as if complete.
4. **Establish the master clock.** Use the supplied narration's measured duration unless the user authorizes editing it. Build scene, caption, music, and SFX cues against the same timebase. Distinguish measured word alignment from estimated phrase timing.
5. **Build the asset pack, then delegate animation.** Collect, generate, inspect, and organize every required asset per the asset quality gate in [Production standards](references/production-standards.md); no composition starts while a required asset is missing or unreviewed. Write the style sheet (type scale, palette roles, easing, transition family, intensity). Include explicit audio targets in the handoff (integrated loudness about −14 LUFS for web/social, true peak ≤ −1 dBTP, music ducked under narration) so the export does not land too quiet. Pass the user's ask verbatim, input paths, measured duration, supplied constraints, user-selected theme, exact palette and visual variant, selected font families/roles/weights, local font paths, license and glyph verification, resolved semantic palette tokens, asset provenance manifest, and the requested output directory to the specialized animation task. Let that task own storyboard, audio creation, rendering, and revisions within the brief; do not dictate unnecessary creative details.
6. **Handle asynchronous work truthfully.** Continue independent checks while it runs. Retrieve the result only after completion notification; do not repeatedly poll the agent or mistake a growing MP4 for a completed export.
7. **Verify the deliverable.** Run `scripts/production_check.py scan` on sources/captions and `blackframes` on the export; review the full rendered output start to end per production-standards.md; fix, re-render, re-review. Apply the mandatory acceptance matrix: English text, authentic available assets, accurate subject representation, honest generated fallbacks, polished purposeful motion, synchronization, readability, safe margins, balanced sound, and technical quality. Review scene layouts and motion separately; assess audio separately from its stream's mere existence.
8. **Deliver with qualifications.** Show the returned MP4 and a short summary, plus where applicable the asset pack with sources/licenses, finalized script and transcript, editable project files, and the list of corrections and assumptions. Include every reported qualification: approximate synchronization, silent or missing audio, unofficial assets, fictional examples, factual claims not checked, and incomplete motion review. Label an incompletely reviewed output a rendered draft.
9. **Revise deliberately.** Keep the prior export. Change the requested dimension, rerun the relevant checks, and deliver a new version. Do not restart the whole creative direction without authorization.

## Non-negotiable boundaries

- Zero placeholders: no lorem ipsum, dummy text, TODOs, debug overlays, temporary images, broken assets, unauthorized watermarks, clipped text, or unintended blank frames in any export.
- Quality, accuracy, and completeness outrank speed. When a critical detail is unclear, research it or ask; when a tool is unavailable, say so and offer the best feasible alternative.

- Preserve uploaded narration's words, voice, and speed unless editing is authorized. Mixing underneath it is not permission to rewrite it.
- Do not turn unverified narration into verified factual claims, especially on health, finance, law, security, privacy, or current policy. Offer fact-checking separately when needed.
- Keep private credentials and personal information out of prompts, logs, screenshots, captions, and deliverables unless they are explicitly intended public content.
- Follow the current platform's video-creator animation workflow. Do not substitute generated footage or a still-image slideshow for requested motion graphics.
- If the animation task fails or returns only frames, report failure; do not independently render or encode a rescue video.
- Do not hardcode model IDs, credential procedures, provider limits, or platform retry semantics into this skill. Consult the current matching platform guidance when a provider call is needed.
- Do not claim “frame-perfect,” “lip-synced,” “official logos,” “fact-checked,” “clipping-free,” or “fully reviewed” without evidence specific to that claim.

## Completion contract

The final report must identify the actual duration and dimensions when known, confirm which requested sound layers exist, distinguish layout sampling from motion playback review, and state remaining limitations. Keep the visible reply concise even though the internal workflow is detailed.