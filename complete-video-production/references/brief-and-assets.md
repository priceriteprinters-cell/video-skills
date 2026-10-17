# Brief and Asset Intake

## Build a production brief

Record these internally; do not require the user to fill out a long questionnaire:

- Purpose: what the viewer should understand, feel, or do.
- Subject and supplied factual material.
- Audience, language, and intended platform.
- Style already requested: motion graphics, kinetic typography, diagrams, product walkthrough, or another animated format.
- Master content: uploaded narration, supplied script, existing clip, or topic.
- Duration constraint: exact, approximate, maximum, or absent.
- Delivery: aspect ratio, resolution, frame rate if specified, destination, captions, extra deliverables.
- Sound: preserve narration, whether music and SFX are wanted, supplied or generated tracks, intensity and any exclusions.
- Identity: approved assets, real product screenshots, logos, colors, fonts, and factual brand text.
- Revision scope: what stays unchanged and what changes.

Maintain provenance for every asset or assertion: supplied, measured, transcribed, generated, inferred, licensed, or unverified. This prevents illustrative graphics from being presented as real evidence.

## Reasonable defaults

Use the narration length for narrated videos. Always ask the user to choose or confirm the aspect ratio before starting production, including revised exports. If a ratio was supplied, ask whether to keep it; if absent, offer 16:9 landscape, 9:16 portrait, 1:1 square, and a custom option. Wait for the answer. Platform or source dimensions may inform recommendations but never replace this question. Choose resolution consistent with the confirmed ratio; 30 fps is a practical baseline when unspecified.

Use English for every authored caption, subtitle, title, label, callout, and explanatory overlay unless the user explicitly requests another language. Preserve the original spoken narration; translate its meaning accurately for English text. Choose readable typography and visual pacing that suit the subject. Let the animation specialist choose unspecified storyboard and soundtrack details. Add music and SFX when requested; do not automatically add them to every subsequent job.

Ask the three mandatory creative questions defined in SKILL.md together (ratio, font or pairing, palette/theme); preserve supplied choices as explicit “Keep current” options. Besides these, clarify only blocking questions: incompatible exact length and uncut narration; missing audio; expensive alternate versions; unavailable required official assets; ambiguous live-interactive requirements.

## Inspect source media

Locate uploads under their supplied path. In the sandbox, use the read-only upload mount and its mirror if needed. Keep transformations in temporary storage, never overwrite the upload.

Probe audio/video before planning:

```bash
ffprobe -v error -show_entries format=duration,size -show_entries stream=codec_type,codec_name,sample_rate,channels,width,height,r_frame_rate -of json "INPUT"
```

**Success:** the file is readable, has the expected stream types, and a credible finite duration. Record exact values; a rounded display duration is not a timeline clock.

Transcribe an uploaded audio file with the current document parser when available. A transcript without timestamps supplies content, not word alignment. Listen or obtain timed alignment when precise cues are necessary. Flag uncertain proper nouns and poor automatic spelling rather than copying obvious transcription errors into titles.

## Inventory visuals before delegation

If an asset ZIP is attached, first read asset-pack-intake.md. Recognize and validate the motion-assets/v1 manifest, import without executing content, visually inspect PNGs, and preserve scene/provenance mappings. Reuse suitable included art and request the three creative confirmations using pack settings as keepable options. Do not download or regenerate duplicates unnecessarily.

List Files and relevant repository image directories: `public/`, `src/assets/`, `assets/`, `expo/assets/`, and known store-listing folders. Collect every available screenshot, store image, logo, and brand file relevant to the request. Supply only confirmed existing paths; the specialized task cannot discover them on your behalf.

Also pass uploaded visuals explicitly with their purpose. If the current tool only accepts repository or Files visual inputs, make a permitted temporary handoff copy into the allowed location and state its provenance. Do not invent an asset path or replace a provided product image unnecessarily.

Use an actual product screenshot for a walkthrough. Distinguish official logos from drawn approximations. Do not imply that a template app is the user's product: an empty local preview is not useful footage or brand material.

## Authentic-first sourcing and generated fallback

Identify the brands, products, tools, objects, technologies, people, concepts, and features named in narration. Search official websites, product pages, documentation, media kits, and trusted repositories for each identifiable subject. Use parallel research for independent searches. Inspect the actual downloaded images, not just search thumbnails or filenames, and record source URL, identity, usage constraints, and intended scene.

Use genuine official logos whenever available; preserve shape, color, proportion, and brand identity. Use authentic icons from official sources or trusted icon libraries. Prefer high-resolution real photos, accurate product images, genuine screenshots, and verified demonstrations. Never replace an available authentic asset with a generated recreation, unrelated stock image, or generic placeholder.

Acquire assets through the current supported download/asset workflow; keep raw downloads temporary and register app media only when the app needs it. Provide confirmed accessible visual paths to the specialist. Do not invent a URL or claim an asset is official without verifying its provenance.

Only after suitable authentic imagery cannot be found, generate supporting visuals using the current image tools. Maintain consistent lighting, perspective, grading, and composition. For a real product, do not invent unverified features, physical details, or interface layouts. Combine authentic logos/product assets with generated environments or diagrams when useful; never label generated visuals as real photographs, official logos, screenshots, or actual demonstrations. A missing authentic logo is not permission to create an inaccurate branded look-alike.

Preserve authentic screenshots and wordmarks as source evidence rather than altering their identity. If embedded non-English text conflicts with the English-only requirement, select an authentic English-localized asset when available or ask for an explicit exception; do not fabricate a translated interface. All newly authored explanatory text remains English.

Read project branding where relevant. Template-default tokens are not a meaningful brand identity. Avoid copying unrelated colors, layout, or product claims into a standalone video.

## Integrity and safety

Preserve accents, names, technical terms, and the speaker's language in audio. Translate on-screen meaning into English by default and keep translations linked to their source phrases. Use clearly illustrative synthetic examples for contact details only where appropriate; never pass a fabricated interface as a genuine application screenshot or demonstration.

Respect asset rights. Do not promise an independently synthesized track is legally cleared or official. If licensing matters, establish the source and usage rights. If publication depends on current factual accuracy, tell the user that reproducing narration is different from verifying it.
## Resolve the creative brief

After the three answers, assign font roles, weights and verified local paths; palette roles and exact colors; dimensions and safe areas. Use the supplied resource guide as the primary discovery reference. Follow resource-acquisition.md for downloads and rights checks. Validate the structured brief with the helper before delegation. Store downloaded assets with source, identity, license evidence, required attribution, hash, and intended scene; do not silently substitute on failure.
