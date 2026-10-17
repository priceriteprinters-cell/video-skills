

<!-- ===== FILE: remotion/remotion-captions/REFERENCE.md ===== -->

---
name: remotion-captions
description: Transcribing, displaying and animating captions
version: 4.0.536
---

All captions must be processed in JSON. The captions must use the [`Caption`](https://www.remotion.dev/docs/captions/caption.md) type which is the following:

```ts
import type { Caption } from "@remotion/captions";
```

This is the definition:

```ts
type Caption = {
  text: string;
  startMs: number;
  endMs: number;
  timestampMs: number | null;
  confidence: number | null;
  pageBreakAfter?: boolean;
};
```

## Generating captions

To transcribe video and audio files to generate captions, load the [transcribe-captions.md](transcribe-captions.md) file for more instructions.

## Displaying captions

To display captions in your video, load the [display-captions.md](display-captions.md) file for more instructions.

## Importing captions

To import captions from a .srt file, load the [import-srt-captions.md](import-srt-captions.md) file for more instructions.

## Post-creation

After you're done, load this skill: [Remotion Best Practices](../GUIDE.md)

If not alreay done, open the Remotion Studio, unless instructed otherwise.


<!-- ===== FILE: remotion/remotion-captions/display-captions.md ===== -->

---
name: display-captions
description: Displaying captions in Remotion using the Basic Captions element
metadata:
  tags: captions, subtitles, display, element
---

# Displaying captions in Remotion

This guide explains how to display captions in Remotion, assuming you already have captions in the [`Caption`](https://www.remotion.dev/docs/captions/caption.md) format.

## Prerequisites

Read [Transcribing audio](transcribe-captions.md) for how to generate captions.

First, the [`@remotion/captions`](https://www.remotion.dev/docs/captions.md) package needs to be installed.
If it is not installed, use the following command:

```bash
npx remotion add @remotion/captions # If project uses npm
bunx remotion add @remotion/captions # If project uses bun
yarn remotion add @remotion/captions # If project uses yarn
pnpm exec remotion add @remotion/captions # If project uses pnpm
```

## Adding the Basic Captions element

Use the [Basic Captions](https://www.remotion.dev/elements/captions/basic-captions) element to display captions.

Alternatives are available at [Remotion Captions Elements](https://www.remotion.dev/elements/captions), but use Basic Captions unless there are more precise specifications.

Fetch its source code from https://www.remotion.dev/elements/captions/basic-captions.md and copy the `basic-captions.tsx` file into the project unchanged.

## Displaying captions alongside video content

Keep each clip's video and captions inside the same `<Sequence>` or `<TransitionSeries.Sequence>`.
Put the clip's `trimBefore`, `durationInFrames`, and `playbackRate` on that shared parent so trimming or changing the speed affects both.  
For independently positioned clips, put `from` on the shared `<Sequence>` too.

Give every captioned clip its own group and inline caption array; do not combine captions from multiple clips into one overlay outside the scene timeline.  
Moving, reordering, trimming, or deleting the group then affects its video and captions together.

Putting captions inside a scene is insufficient if `trimBefore` or `playbackRate` is still applied only to `<Video>`: its sibling captions do not inherit those props. Apply them to the shared parent instead.

The Caption editor writes back to the array literal on the selected `<BasicCaptions>` source node, so inline the captions directly in its `captions` prop.  
Passing a variable or component prop such as `captions={captions}` leaves no source array for the editor to update.  
If the captions were transcribed to a JSON file, copy its contents into the prop.

Give the caption area a width and position it over the video. In this
1920px-wide composition, the 900px caption area is centered by translating it
`(1920 - 900) / 2 = 510` pixels from the left:

```tsx title="src/MyComposition.tsx"
import { Video } from "@remotion/media";
import { TransitionSeries } from "@remotion/transitions";
import { staticFile, useVideoConfig } from "remotion";
import { BasicCaptions } from "./basic-captions";

export const MyComposition: React.FC = () => {
  const { fps } = useVideoConfig();

  return (
    <TransitionSeries>
      <TransitionSeries.Sequence
        name="Opening"
        trimBefore={4 * fps}
        durationInFrames={20 * fps}
      >
        <Video
          name="Opening footage"
          src={staticFile("opening.mp4")}
          objectFit="cover"
          style={{ width: "100%", height: "100%" }}
        />
        <BasicCaptions
          name="Opening captions"
          width={900}
          style={{
            position: "absolute",
            bottom: 120,
            translate: "510px 0px",
          }}
          captions={[
            {
              text: "Hello",
              startMs: 5000,
              endMs: 5400,
              timestampMs: 5200,
              confidence: null,
            },
            {
              text: " world",
              startMs: 5400,
              endMs: 5900,
              timestampMs: 5650,
              confidence: null,
            },
          ]}
        />
      </TransitionSeries.Sequence>
      <TransitionSeries.Sequence
        name="Next clip"
        trimBefore={1 * fps}
        durationInFrames={5 * fps}
      >
        <Video
          name="Next footage"
          src={staticFile("next.mp4")}
          objectFit="cover"
          style={{ width: "100%", height: "100%" }}
        />
        <BasicCaptions
          name="Next captions"
          width={900}
          style={{
            position: "absolute",
            bottom: 120,
            translate: "510px 0px",
          }}
          captions={[
            {
              text: "Next",
              startMs: 2000,
              endMs: 2400,
              timestampMs: 2200,
              confidence: null,
            },
            {
              text: " clip",
              startMs: 2400,
              endMs: 2900,
              timestampMs: 2650,
              confidence: null,
            },
          ]}
        />
      </TransitionSeries.Sequence>
    </TransitionSeries>
  );
};
```

```tsx title="src/Root.tsx"
import { Composition } from "remotion";
import { MyComposition } from "./MyComposition";

export const RemotionRoot = () => {
  return (
    <Composition
      id="MyComposition"
      component={MyComposition}
      durationInFrames={750}
      fps={30}
      width={1920}
      height={1080}
    />
  );
};
```

To change a captioned clip's speed, set `playbackRate` on its shared sequence.
`durationInFrames` selects a range of source frames; the group occupies `durationInFrames / playbackRate` frames in its parent timeline.
Update the composition duration when changing the total timeline length.

If a caption has `pageBreakAfter: true`, the current page ends after that caption and the next caption starts a new page.

## White-space preservation

The captions are whitespace sensitive. You should include spaces in the `text` field before each word.


<!-- ===== FILE: remotion/remotion-captions/import-srt-captions.md ===== -->

---
name: import-srt-captions
description: Importing .srt subtitle files into Remotion using @remotion/captions
metadata:
  tags: captions, subtitles, srt, import, parse
---

# Importing .srt subtitles into Remotion

If you have an existing `.srt` subtitle file, you can import it into Remotion using `parseSrt()` from `@remotion/captions`.

If you don't have a .srt file, read [Transcribing audio](transcribe-captions.md) for how to generate captions instead.

## Prerequisites

First, the @remotion/captions package needs to be installed.
If it is not installed, use the following command:

```bash
npx remotion add @remotion/captions # If project uses npm
bunx remotion add @remotion/captions # If project uses bun
yarn remotion add @remotion/captions # If project uses yarn
pnpm exec remotion add @remotion/captions # If project uses pnpm
```

## Reading an .srt file

Use `staticFile()` to reference an `.srt` file in your `public` folder, then fetch and parse it:

```tsx
import { useState, useEffect, useCallback } from "react";
import { staticFile, useDelayRender } from "remotion";
import { parseSrt } from "@remotion/captions";
import type { Caption } from "@remotion/captions";

export const MyComponent: React.FC = () => {
  const [captions, setCaptions] = useState<Caption[] | null>(null);
  const { delayRender, continueRender, cancelRender } = useDelayRender();
  const [handle] = useState(() => delayRender());

  const fetchCaptions = useCallback(async () => {
    try {
      const response = await fetch(staticFile("subtitles.srt"));
      const text = await response.text();
      const { captions: parsed } = parseSrt({ input: text });
      setCaptions(parsed);
      continueRender(handle);
    } catch (e) {
      cancelRender(e);
    }
  }, [continueRender, cancelRender, handle]);

  useEffect(() => {
    fetchCaptions();
  }, [fetchCaptions]);

  if (!captions) {
    return null;
  }

  return (
    <>
      {/* Use captions here */}
    </>
  );
};
```

Remote URLs are also supported - you can `fetch()` a remote file via URL instead of using `staticFile()`.

## Using imported captions

Once parsed, the captions are in the `Caption` format and can be used with all `@remotion/captions` utilities.


<!-- ===== FILE: remotion/remotion-captions/transcribe-captions.md ===== -->

# Transcribing audio

To transcribe audio to generate captions in Remotion, use the [`transcribe()`](https://www.remotion.dev/docs/whisper-webgpu/transcribe.md) function from the [`@remotion/whisper-webgpu`](https://www.remotion.dev/docs/whisper-webgpu.md) package.
It runs Whisper locally on the GPU and works in both Node.js and the browser.

## Prerequisites

Install the required packages if they are not installed:

```bash
npx remotion add @remotion/whisper-webgpu @huggingface/transformers mediabunny @mediabunny/server # If project uses npm
bunx remotion add @remotion/whisper-webgpu @huggingface/transformers mediabunny @mediabunny/server # If project uses bun
yarn remotion add @remotion/whisper-webgpu @huggingface/transformers mediabunny @mediabunny/server # If project uses yarn
pnpm exec remotion add @remotion/whisper-webgpu @huggingface/transformers mediabunny @mediabunny/server # If project uses pnpm
```

A compatible GPU is required. ONNX Runtime does not work on Linux arm64.

## Transcribing

Make a Node.js script that decodes the audio to a 16kHz mono waveform, downloads a model, and transcribes it.

```ts
import { registerMediabunnyServer } from "@mediabunny/server";
import {
  WHISPER_WEBGPU_SAMPLE_RATE,
  canUseWhisperWebGpu,
  downloadWhisperModel,
  loadWhisperModel,
  toCaptions,
  transcribe,
} from "@remotion/whisper-webgpu";
import {
  ALL_FORMATS,
  Conversion,
  FilePathSource,
  Input,
  NullTarget,
  Output,
  WavOutputFormat,
} from "mediabunny";
import { writeFile } from "node:fs/promises";

registerMediabunnyServer();

const support = await canUseWhisperWebGpu();
if (!support.supported) {
  throw new Error(support.detailedReason);
}

type WaveformChunk = {
  startFrame: number;
  waveform: Float32Array;
};
const chunks: WaveformChunk[] = [];

using input = new Input({
  formats: ALL_FORMATS,
  source: new FilePathSource("public/video123.mp4"),
});
const audioTrack = await input.getPrimaryAudioTrack();
if (audioTrack === null) {
  throw new Error("The media does not contain an audio track.");
}

const conversion = await Conversion.init({
  input,
  output: new Output({
    format: new WavOutputFormat(),
    target: new NullTarget(),
  }),
  video: { discard: true },
  audio: (track) => {
    if (track.id !== audioTrack.id) {
      return { discard: true };
    }

    return {
      codec: "pcm-f32",
      forceTranscode: true,
      numberOfChannels: 1,
      sampleFormat: "f32",
      sampleRate: WHISPER_WEBGPU_SAMPLE_RATE,
      process: (sample) => {
        const waveform = new Float32Array(
          sample.allocationSize({ format: "f32", planeIndex: 0 }) /
            Float32Array.BYTES_PER_ELEMENT,
        );
        sample.copyTo(waveform, { format: "f32", planeIndex: 0 });
        chunks.push({
          startFrame: Math.round(sample.timestamp * WHISPER_WEBGPU_SAMPLE_RATE),
          waveform,
        });
        return sample;
      },
    };
  },
});

if (!conversion.isValid) {
  throw new Error("The audio track cannot be decoded.");
}

await conversion.execute();

const waveformLength = chunks.reduce(
  (max, chunk) => Math.max(max, chunk.startFrame + chunk.waveform.length),
  0,
);
const channelWaveform = new Float32Array(waveformLength);
for (const chunk of chunks) {
  const destinationStart = Math.max(0, chunk.startFrame);
  const sourceStart = Math.max(0, -chunk.startFrame);
  const availableLength = Math.min(
    chunk.waveform.length - sourceStart,
    channelWaveform.length - destinationStart,
  );

  if (availableLength > 0) {
    channelWaveform.set(
      chunk.waveform.subarray(sourceStart, sourceStart + availableLength),
      destinationStart,
    );
  }
}

const model = "small.en";
await downloadWhisperModel({ model });
await using modelHandle = await loadWhisperModel({ model });
const transcription = await transcribe({ channelWaveform, model });
const { captions } = toCaptions({ whisperWebGpuOutput: transcription });

// Write it to a file so the captions can be inlined into the Remotion code
await writeFile("captions123.json", JSON.stringify(captions, null, 2));
```

## Choosing a model

`small.en` is the recommended default for English.  
For other languages, use a multilingual model such as `small` and pass the `language` option to `transcribe()` - automatic language detection is not supported.  
See [`getAvailableModels()`](https://www.remotion.dev/docs/whisper-webgpu/get-available-models.md) for all models.

## Transcribing in the browser

In the browser, use [`resampleTo16Khz()`](https://www.remotion.dev/docs/whisper-webgpu/resample-to-16khz.md) to get the waveform from a `File` instead of using Mediabunny:

```ts
import {
  downloadWhisperModel,
  resampleTo16Khz,
  toCaptions,
  transcribe,
} from "@remotion/whisper-webgpu";

export const transcribeFile = async (file: File) => {
  await downloadWhisperModel({ model: "small.en" });
  const channelWaveform = await resampleTo16Khz({ file });
  const transcription = await transcribe({
    channelWaveform,
    model: "small.en",
  });

  const { captions } = toCaptions({ whisperWebGpuOutput: transcription });
  return captions;
};
```

Transcribe each original source video or audio file individually.  
Keep the resulting caption timestamps relative to the beginning of that source file, including portions currently trimmed out of the edit.  
Do not add composition offsets or flatten multiple transcripts into composition-wide timestamps.

See [Displaying captions](display-captions.md) for how to display the captions in Remotion.
