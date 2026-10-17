# Narration, Timing, and Storyboard

## One master clock

Make the narration the authoritative timeline for an audio-led video. Store seconds as the editorial clock and convert to frames only at render boundaries. Use a single frame rate for all scenes. For an audio duration D and frame rate F, plan approximately `ceil(D × F)` frames so the last spoken sample is not truncated; padding below a frame is acceptable and should be reported from the finished export.

Never round 73.560816 seconds down to 73 seconds for editing convenience. Do not treat a 74-second user-facing description as an exact 74-second source measurement.

## Alignment levels

Choose the appropriate level and disclose it:

1. **Transcript only:** identifies subject and order but has no measured timestamps.
2. **Phrase/pause alignment:** measured or manually inspected phrase boundaries; suitable for scene changes and subtitle blocks.
3. **Word alignment:** timed words from an alignment/transcription service, corrected at spot checks; suitable for word reveals or karaoke captions.
4. **Frame alignment:** event timestamps snapped to render frames and checked in output; appropriate for exact lock clicks, stamps, or hits.

Silence detection can locate breathing gaps but is not a word recognizer. Estimated timestamps must not be described as forced alignment. Visual timing may legitimately anticipate a spoken idea or settle after it; synchronization does not mean every animation begins on every word.

## Scene table

Use one structured timeline, internally or within the specialist's production files:

| Field | Meaning |
|---|---|
| id | Stable cue/scene identifier |
| start/end | Absolute time on master narration |
| source phrase | Exact relevant words or transcript segment |
| concept | One primary idea being explained |
| main visual | Diagram, title, comparison, screenshot, symbol, or chart |
| readable text | Short visual wording, not a duplicate paragraph |
| captions | Accurate English rendering of the spoken meaning, unless another language is explicitly requested |
| motion events | Enter, reveal, connect, transform, hold, exit |
| sound cues | Linked event id, intended contact/reveal time, sound category |
| asset/provenance | File references and illustrative/official status |
| review notes | Timing precision and any unresolved content |

Cover the entire meaningful narration with no accidental gaps or double-booked contradictory scenes. Deliberate overlaps for transitions are allowed. Keep each scene's visual hierarchy clear during overlaps.

Map each named subject to the correct asset and exact discussion interval. Bring the relevant product, tool, feature, person, or diagram on screen when it is discussed, not merely somewhere in the video. Verify precise caption/visual synchronization against the source audio. Obtain measured alignment or manual timing correction for important cues; do not silently treat pause estimates as meeting precision requirements.

## Build an explanation, not a slideshow

Use a hook, successive evidence or concepts, comparison/trade-off, conclusion, and ending when the subject supports that arc. Do not force a promotional call to action into an educational narration.

Assign one major idea to a scene. Reveal lists item by item, animate a connection when explaining a relationship, close a lock at the claim about locking, and transfer a data token along an arrow when explaining movement. Avoid random bouncing merely to satisfy “motion.”

Keep spoken paragraphs in subtitles and key ideas in the visual layer. Dense processes can use progressive diagram construction rather than a new title card for every sentence.

## Cue math

Anchor each cue to a scene or phrase rather than burying absolute literals in multiple files:

- `event.time = phrase.start + chosen_offset`
- `event.frame = round(event.time × fps)`
- `effect.start = event.time - effect_attack_or_lead_in`

A whoosh may start before a panel arrives; its peak should match the arrival. A stamp impact belongs at contact, not at the beginning of the stamp's travel. A lock click belongs when the lock visibly closes. Use a small lead-in only when it supports perception, not to hide inaccurate alignment.

## Caption requirements

Create phrase-sized English captions with stable placement and enough time to read. Translate meaning accurately without adding claims or changing the narrator's intent. Use accurate spelling, natural grammar, professional phrasing, and consistent punctuation for every title, label, callout, subtitle, and overlay. Align translations to the corresponding spoken phrases rather than mapping translated words one-for-one onto another language's word order. If another language is explicitly requested, verify its fonts, shaping, script direction, and punctuation. Avoid splitting a grammatical phrase or leaving a single word alone unnecessarily.

Separate captions from large visual labels so they do not compete. Check the longest caption, not only the opening. Reserve a safe caption band and accommodate platform overlays. Do not claim word-synchronized subtitles if only scene-level timing exists.

Optional subtitle files are separate deliverables only when requested. Ensure their cue times match the final export and avoid adding them to Files unasked.

## Changes to narration

If a fixed user duration is shorter than the narration, explain the conflict and obtain permission to trim or rewrite; do not time-stretch silently. If narration changes, realign every downstream cue, not just scene start times. If only visuals change, preserve the master audio and timing wherever possible.