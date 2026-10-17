

<!-- ===== FILE: remotion/remotion-multimedia/REFERENCE.md ===== -->

---
name: remotion-multimedia
description: Interacting with Mediabunny
version: 4.0.536
---

Mediabunny is a multimedia library for dealing with audio and video in the browser.
Here is a compact overview of its capabilities: https://mediabunny.dev/llms.txt

## Getting audio duration

See [get-audio-duration.md](get-audio-duration.md) for getting the duration of an audio file in seconds with Mediabunny.

## Getting video dimensions

See [get-video-dimensions.md](get-video-dimensions.md) for getting the width and height of a video file with Mediabunny.

## Getting video duration

See [get-video-duration.md](get-video-duration.md) for getting the duration of a video file in seconds with Mediabunny.


<!-- ===== FILE: remotion/remotion-multimedia/get-audio-duration.md ===== -->

---
name: get-audio-duration
description: Getting the duration of an audio file in seconds with Mediabunny
metadata:
  tags: duration, audio, length, time, seconds, mp3, wav
---

# Getting audio duration with Mediabunny

Mediabunny can extract the duration of an audio file. It works in browser, Node.js, and Bun environments.

## Getting audio duration

```tsx title="get-audio-duration.ts"
import { Input, ALL_FORMATS, UrlSource } from "mediabunny";

export const getAudioDuration = async (src: string) => {
  const input = new Input({
    formats: ALL_FORMATS,
    source: new UrlSource(src),
  });

  const durationInSeconds = await input.computeDuration();
  return durationInSeconds;
};
```

## Usage

```tsx
const duration = await getAudioDuration("https://remotion.media/audio.mp3");
console.log(duration); // e.g. 180.5 (seconds)
```

## Using with staticFile in Remotion

Make sure to wrap the file path in `staticFile()`:

```tsx
import { staticFile } from "remotion";

const duration = await getAudioDuration(staticFile("audio.mp3"));
```

## In Node.js and Bun

Use `FilePathSource` instead of `UrlSource` to read a file from disk:

```tsx
import { Input, ALL_FORMATS, FilePathSource } from "mediabunny";

const input = new Input({
  formats: ALL_FORMATS,
  source: new FilePathSource("audio.mp3"),
});

const durationInSeconds = await input.computeDuration();
input.dispose(); // Closes the file handle
```

For a `File` from a file input or drag and drop, use `new BlobSource(file)` instead.


<!-- ===== FILE: remotion/remotion-multimedia/get-video-dimensions.md ===== -->

---
name: get-video-dimensions
description: Getting the width and height of a video file with Mediabunny
metadata:
  tags: dimensions, width, height, resolution, size, video
---

# Getting video dimensions with Mediabunny

Mediabunny can extract the width and height of a video file. It works in browser, Node.js, and Bun environments.

## Getting video dimensions

```tsx
import { Input, ALL_FORMATS, UrlSource } from "mediabunny";

export const getVideoDimensions = async (src: string) => {
  const input = new Input({
    formats: ALL_FORMATS,
    source: new UrlSource(src),
  });

  const videoTrack = await input.getPrimaryVideoTrack();
  if (!videoTrack) {
    throw new Error("No video track found");
  }

  return {
    width: videoTrack.displayWidth,
    height: videoTrack.displayHeight,
  };
};
```

## Usage

```tsx
const dimensions = await getVideoDimensions("https://remotion.media/video.mp4");
console.log(dimensions.width); // e.g. 1920
console.log(dimensions.height); // e.g. 1080
```

## Using with local files

For a `File` from a file input or drag and drop, use `BlobSource` instead of `UrlSource`:

```tsx
import { Input, ALL_FORMATS, BlobSource } from "mediabunny";

const input = new Input({
  formats: ALL_FORMATS,
  source: new BlobSource(file), // File object from input or drag-drop
});

const videoTrack = await input.getPrimaryVideoTrack();
if (!videoTrack) {
  throw new Error("No video track found");
}

const width = videoTrack.displayWidth;
const height = videoTrack.displayHeight;
```

In Node.js and Bun, use `new FilePathSource(path)` to read a file from disk, and call `input.dispose()` when done.

## Using with staticFile in Remotion

```tsx
import { staticFile } from "remotion";

const dimensions = await getVideoDimensions(staticFile("video.mp4"));
```


<!-- ===== FILE: remotion/remotion-multimedia/get-video-duration.md ===== -->

---
name: get-video-duration
description: Getting the duration of a video file in seconds with Mediabunny
metadata:
  tags: duration, video, length, time, seconds
---

# Getting video duration with Mediabunny

Mediabunny can extract the duration of a video file. It works in browser, Node.js, and Bun environments.

## Getting video duration

```tsx
import { Input, ALL_FORMATS, UrlSource } from "mediabunny";

export const getVideoDuration = async (src: string) => {
  const input = new Input({
    formats: ALL_FORMATS,
    source: new UrlSource(src),
  });

  const durationInSeconds = await input.computeDuration();
  return durationInSeconds;
};
```

## Usage

```tsx
const duration = await getVideoDuration("https://remotion.media/video.mp4");
console.log(duration); // e.g. 10.5 (seconds)
```

## Video files from the public/ directory

Make sure to wrap the file path in `staticFile()`:

```tsx
import { staticFile } from "remotion";

const duration = await getVideoDuration(staticFile("video.mp4"));
```

## In Node.js and Bun

Use `FilePathSource` instead of `UrlSource` to read a file from disk:

```tsx
import { Input, ALL_FORMATS, FilePathSource } from "mediabunny";

const input = new Input({
  formats: ALL_FORMATS,
  source: new FilePathSource("video.mp4"),
});

const durationInSeconds = await input.computeDuration();
input.dispose(); // Closes the file handle
```

For a `File` from a file input or drag and drop, use `new BlobSource(file)` instead.
