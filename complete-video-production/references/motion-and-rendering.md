# Motion Design and Rendering

These are quality requirements for the specialized animation task, not an instruction for the parent agent to implement a substitute renderer.

## Design for the topic

Choose a coherent visual system: limited semantic colors, readable type scale, consistent line weights, spacing, caption location, diagram language, and animation vocabulary. Match the user's actual brand where supplied. Generalize the production process, not the previous video's dark palette or its messaging-app icons.

Use real screenshots and assets where the viewer must inspect an actual interface or product. Use custom diagrams for abstract concepts. A drawn icon may explain an idea but must not masquerade as an official logo or a genuine screenshot.

Deliver polished, dynamic, premium motion graphics consistently. Use cinematic transitions, smooth camera movement, animated typography, kinetic text, parallax, depth, layered compositions, and sophisticated reveals where they enhance the subject. Add animated diagrams, data visuals, interface callouts, product highlights, and tracking elements to explain relevant concepts. Use tasteful lighting, glow, shadows, reflections, particles, or 3D only when they fit; these are options, not a checklist of decorations. Vary scale, composition, pacing, and motion while maintaining one coherent visual language. Align transitions rhythmically with narration, music, and appropriate SFX, using professional curves and natural acceleration/deceleration.

Prioritize legibility, hierarchy, and explanation over spectacle. Avoid excessive flashes, shake, background clutter, and transitions that erase information before the viewer can read it. Keep movement purposeful and match its intensity to the topic.

## Layout constraints

Establish canvas dimensions, safe margins, caption band, and platform overlay exclusions before scene composition. Anchor titles, diagrams, and comparisons to stable regions. Keep enough clearance for motion overshoot, rotating elements, glow, and shadows.

For text, check the actual chosen font and longest real wording. Wrap or rebalance the layout before shrinking text too far. All authored text is English unless another language is explicitly requested. Inspect punctuation, glyph coverage, and clipped descenders; for an explicit language exception also check shaping and direction. Visual effects must never obscure captions, logos, product details, or demonstrations. Use high-resolution assets, clean framing, consistent grading, and text contrast optimized for the confirmed viewing format.

For portrait and landscape variants, recompose rather than crop a landscape diagram mechanically. Preserve hierarchy, comparison labels, and captions. Do not promise a second format until it is rendered and reviewed.

## Deterministic animation principles

Use a renderer that can evaluate the complete visual state at an explicit time. A seek to time T should yield the same frame whether reached directly, forward, or backward. Avoid dependence on elapsed wall time, DOM history, uncontrolled CSS animation state, random values generated during rendering, or frames captured before fonts/assets are ready.

Reset or derive all visible state from the timeline on each render evaluation. Seed randomness when decorative particles or jitter are necessary. Clamp transitions outside their active interval. Prevent stale elements from previous scenes surviving a direct seek.

Use clear motion phases: enter, explain/reveal, readable hold, exit. Smooth easing is a tool, not a requirement for every event; a stamp may need a fast impact and a diagram may need slow movement. Keep a small consistent animation vocabulary rather than every transition style at once.

## Render discipline

The specialized task owns renderer implementation and export. Before final encoding it should verify a few representative frames, font readiness, image loading, and console errors. A deterministic frame pipeline should produce consecutive correctly sized frames with no missing indices or stale states.

If parallel rendering is used, partition nonoverlapping frame ranges and confirm all expected files exist. Limit concurrency to avoid memory pressure or disk saturation. Parallel work is an optimization, not a reason to skip ordering and readiness checks.

For a typical browser-deliverable MP4, H.264 video, AAC audio, and a widely compatible pixel format are practical choices. Use the user-specified output contract when it differs. For downloadable playback, export a seekable completed container; fast-start metadata is useful but not a substitute for verifying file completeness.

Choose source and output audio duration carefully. Do not use a “shortest stream” option that truncates narration because the visual stream is a few frames short. Retain the end of the last spoken phrase and sound tails within the authorized duration.

## Asynchronous export hazard

A video file can exist and grow before its container metadata is finalized. File size and an `.mp4` suffix do not establish completion. A missing MP4 `moov` atom during an active export may simply mean the encoder has not finished.

Wait for the production task's completion result before final verification. If probing fails after completion, classify it as an invalid export and ask the specialist to repair it. Do not race-read a growing output, continually retry the same final probe, or deliver it as playable.

## Evidence to request

Ask the specialist to return actual duration, dimensions, frame rate, visual review coverage, motion playback coverage, caption review status, audio layers, and unresolved defects. A contact sheet verifies sampled compositions; it cannot prove smoothness, correct transitions, or exact synchronization.
## Typography, color, and asset production gates

Use the approved font roles and palette tokens from the creative brief, not a renderer's default. Read typography-and-palettes.md. Await every required font face and weight, image decode, and animation asset readiness before captures. Verify actual rendered family/weight and inspect longest copy, numerals, punctuation, script shaping, captions, and line breaks. Do not fake bold or silently fall back to a system family. Download and self-host approved resources so final frames do not depend on a live CDN. Retain authentic logo colors unless the brand explicitly permits a monochrome version; frame them on a contrasting surface rather than recoloring arbitrarily.

Use consistent role-based sizes and spacing. Animate by phrase, word, or glyph only when it preserves meaning and reading time. Keep text-bearing holds long enough for the actual copy. For time-based rendering, evaluate delays, staggering, spring progress, masks, camera moves, and seeded particles from the master clock; test direct seeks at scene boundaries and mid-transitions. Inspect the selected palette through light/dark transitions and on actual assets, not only isolated swatches.
