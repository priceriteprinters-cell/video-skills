# Audio Production and Mixing

## Protect the narration

Retain the supplied spoken performance, language, speed, and sequence unless changes are authorized. Preserve the source file separately. Decode/resample only for production needs; a stereo conversion is not a creative voice change.

Inspect channels, sample rate, clipping, noise, and intelligibility. Do not assume every input is 48 kHz stereo PCM, signed 16-bit, or even decodable with a WAV-only reader. Normalize the working format through a proven media tool when needed. Keep source and final voice comparisons possible.

Noise reduction, compression, equalization, or gain changes should support intelligibility without making the voice harsh or unnatural. A clipped source cannot be restored merely by reducing final volume; disclose persistent source problems.

## Separate stems and clocks

Maintain working narration, music, and SFX layers independently until mixdown. Use the master narration clock and a consistent audio sample rate. Derive buffer length from measured duration, not the previous video's duration. Safely trim or pad generated beds without cutting the voice.

Keep cue timestamps in a reusable table shared conceptually with visual events. Music rhythm does not override speech timing. Where an important visual hit conflicts with a dense spoken phrase, prefer subtle SFX or silence over masking the word.

## Music options

Choose supplied/appropriately licensed music, a permitted music-generation service, or honest procedural synthesis. Follow the current connector and audio-generation guidance if external services are involved; do not request credentials through an invented workflow.

The captured workflow used synthesized music, not ElevenLabs. Do not claim a particular generator was used unless it actually was. Use user-requested music direction; absent a direction, let the specialist choose an unobtrusive instrumental bed that fits the content.

Avoid vocals beneath narration unless deliberately requested. Shape music to the story: restrained opening, supported explanation, room for an important reveal, and a resolved ending where appropriate. Do not copy the same tense-to-bright arc onto every subject.

Fade the bed in and out naturally. For looping music, repair seams and avoid audible abrupt cuts. If the bed is shorter than the narration, use an intentional extension/loop arrangement rather than unexpected silence.

## Speech-first balance

Keep the voice intelligible at comfortable playback volume. Begin with music materially quieter than narration, then adjust by listening. An initial bed roughly 15–25 dB below the voice may be useful for speech-heavy work, but it is not a universal final target.

Apply smooth ducking during speech when needed. Use an envelope with sensible attack/release or a proven sidechain method, not rapid gain changes that pump with every syllable. Let music recover modestly in pauses. Avoid max-based normalization that divides by zero on silent narration.

Control music's spectral competition with the voice. A low music gain can still obscure consonants if it is dense in the speech band. Assess representative dense speech, pauses, and music transitions.

## SFX as explanatory cues

Use effects selectively:

| Visual event | Candidate sound |
|---|---|
| Panel enters or exits | Short whoosh/swish |
| Small object or label appears | Pop or soft blip |
| Lock closes | Mechanical click |
| Card receives an approval/rejection stamp | Brief contact thud |
| Warning or disrupted process | Controlled buzz/glitch |
| Major reveal | Impact or chime |
| Data connection/transfer | Subtle scan or electronic movement |

These are suggestions, not a fixed sound library for every topic. Prefer silence for a scene that already communicates clearly. Do not place an effect on every caption word or every small movement.

Align perceptual peaks with visual events: whoosh peak near arrival, click at closure, stamp thud at contact. Track effect duration and release so tails do not extend beyond the output unintentionally.

Vary repeated sounds subtly without losing consistency. Use restrained panning that still works on a phone speaker or in mono. Avoid excessive sub-bass, piercing frequencies, or startling level jumps.

## Mix and measure

Combine stems, then check narration-heavy sections, dense overlapping effects, quiet transitions, and the ending. Prevent peak overload at summed events. A hard clip or tanh waveshaper changes sound; it is not a transparent substitute for a controlled limiter and a sensible mix.

Measure integrated loudness, loudness range, and true peak with an appropriate meter when delivering to a specified platform. Use the platform's current requirement if supplied; otherwise aim for a comfortable speech-first mix with peak headroom. Recheck the encoded audio because lossy encoding can create intersample peaks.

Do not equate RMS or FFmpeg volume-detection averages with LUFS. Do not infer “no clipping” from a sample peak report alone. Report exactly which metric was measured and whether listening occurred.

Example diagnostic for a completed export:

```bash
ffmpeg -hide_banner -i "OUTPUT.mp4" -filter_complex ebur128=peak=true -f null -
```

**Success:** analysis completes and yields usable loudness/true-peak evidence. This does not substitute for listening.

## Sound QA and fallback

Check the final audio stream is present and non-silent. Confirm the music and effects are actually audible at the intended balance; stream existence cannot identify separate stems.

Listen at normal volume, low volume, and preferably mono or a phone-like playback condition. Check speech masking, harsh effects, pumping, cutoff, drift, and clipping. If sound could not be auditioned, disclose that limitation instead of claiming it sounds good.

If music generation is unavailable, use a permitted alternative only when consistent with the user's request and platform rules, or report the missing music. If music/SFX were requested and absent, do not call the video complete without noting the omission.