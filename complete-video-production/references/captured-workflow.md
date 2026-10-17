# Captured Workflow and Reusable Lessons

## What happened in the source job

The user supplied a Hindi/Hinglish MP3 and requested realtime motion graphics, background music, and realtime sound effects. The request was interpreted as a rendered narrated animation with synchronized events, not a live app.

The parent agent inventoried Files and image directories, probed the upload at 73.560816 seconds, and transcribed it with the document parser. No meaningful project brand assets existed; the app was an untouched template.

The parent delegated to the specialized animation task with the exact ask, upload path, measured length, transcript, output destination, preservation requirement, and request for QA/limitations. It did not invent a storyboard.

The specialist produced 15 animated scenes, bottom Hindi captions, procedural music, and timed effects. The working production used an explicit-time browser visual renderer, frame capture, separate narration/music/SFX arrays, and a final encoded MP4.

The actual final file was 1920×1080, 30 fps, H.264 video with AAC audio, and 73.566667 seconds long. Its spoken subject was specific to the upload; none of that subject matter belongs in defaults for future videos.

## What was checked and what was limited

The specialist reported reviewing 30 sampled frames and correcting two overlaps. The parent viewed a contact sheet and confirmed final metadata. Still-frame inspection established sampled layout quality, not full motion playback review.

The soundtrack was synthesized, not generated through ElevenLabs. Sound effects included whooshes, pops, clicks, glitches, stamps, impacts, and chimes. Reported volume averages and peaks were not a comprehensive LUFS/true-peak-and-listening review.

Scene timing followed pauses rather than measured word alignment. Logos were simplified look-alikes; displayed chats, phone numbers, and IP addresses were illustrative. Privacy assertions were reproduced from narration and not independently fact-checked.

## Improvements encoded in this skill

- Wait for task completion before probing. In the source run, a growing MP4 briefly failed with a missing `moov` atom; file existence was not readiness.
- Distinguish phrase timing, word alignment, and frame-checked events.
- Distinguish contact-sheet review from actual motion playback.
- Distinguish sample peak/RMS analysis from true peak/LUFS and listening.
- Delegate rendering and repair rather than independently rescuing a failed animation task.
- Keep output paths, source duration, sample formats, layout, language, and subject parameterized.
- Use confirmed existing assets and acknowledge an empty template instead of treating it as a brand.
- Preserve narration and disclose unverified claims rather than silently endorsing them.

## Practices not to copy mechanically

Do not inherit the original video's 73.56-second constant, landscape format, dark backgrounds, 15-scene count, fixed cue timestamps, stereo-WAV assumptions, procedural chord pattern, or hardcoded effect gains. They were choices for one job, not general requirements.

Do not copy environment-specific browser executable overrides. Use the current sandbox's documented bundled browser setup. Do not copy a soft-clipping function as a universal mastering solution. Do not present illustrated logos as official assets.

Use this example to calibrate truthful reporting, not as a template storyboard for every subject.