

<!-- ===== FILE: remotion/remotion-markup/REFERENCE.md ===== -->

---
name: remotion-markup
description: Content, animation and effects best practices
version: 4.0.536
---

This is guidance for writing Remotion React Markup.
If this is not relevant, load [Remotion Best Practices](../GUIDE.md) instead.

## Preserve user changes

Users may make edits in the code outside of the conversation.

If you detect a surprising change made in the meanwhile, don't overwrite it, assume it was intentional or ask for confirmation.

## General rules

Inside a composition or scene component, get `fps` from `useVideoConfig()` for
all seconds-to-frames calculations, including timing props such as `from`,
`trimBefore` and `durationInFrames`. Keeping the expression on
the JSX node, such as `trimBefore={4 * fps}`, lets Studio edit the timing and
keeps it correct if the composition frame rate changes.

Drive animations using `useCurrentFrame()` and `interpolate()`.  
CSS `transition` or `animation` will not render correctly, they need to refactored.  
Tailwind animation class will not render correctly, they need to be refactored.

Use `Easing.bezier()` and `Easing.spring()` to customize timing.

Use `Track` for successive scenes. Make scenes and reusable elements with
`Interactive.create()`, setting `layout` explicitly to `'absolute-fill'` or
`'none'`, and register them as connected compositions. Put timing directly on
each instance. Follow the complete
[Track + connected compositions example](../remotion-interactivity/timeline-structure.md).
See [Remotion Interactivity](../remotion-interactivity/REFERENCE.md) for editable props
and keyframes.

The Studio edits the JSX source node that created an item. Author every composition registration, clip, scene, layer and sequence that should be editable independently as its own JSX node, with its editable props inline.
Programmatic loops are suitable when the generated instances are intentionally controlled as one source template, not when users need to edit the instances
separately.

```tsx
import { useCurrentFrame, useVideoConfig, Easing, interpolate, Interactive } from "remotion";

export const FadeIn = () => {
  const frame = useCurrentFrame();
  const {fps} = useVideoConfig();

  return (
    <Interactive.Div
      name="Title"
      style={{
        opacity: interpolate(frame, [0, 2 * fps], [0, 1], {
          extrapolateRight: "clamp",
          extrapolateLeft: "clamp",
          easing: Easing.bezier(0.16, 1, 0.3, 1),
        }),
      }}
    >
      Hello World!
    </Interactive.Div>
  );
};
```

Keep the `interpolate()` call inline in the `style` prop.
Use `scale`, `translate`, `rotate` CSS properties over `transform`.

```tsx
// 👍 Inline editable keyframes and transform shorthands
style={{
  scale: interpolate(frame, [0, 100], [0, 1], {
    extrapolateLeft: 'clamp',
    extrapolateRight: 'clamp',
    easing: Easing.spring({damping: 200}),
    output: 'perceptual-scale' // For `scale` animations, use "output: 'perceptual-scale'"
  }),
  translate: interpolate(frame, [0, 100], ["0px 0px", "100px 100px"], {
    extrapolateLeft: 'clamp',
    extrapolateRight: 'clamp',
    easing: Easing.spring({damping: 200}),
  }),
  rotate: interpolate(frame, [0, 100], ["20deg", "90deg"], {
    extrapolateLeft: 'clamp',
    extrapolateRight: 'clamp',
    easing: Easing.spring({damping: 200}),
  }),
}}

// 👎 Non-inline values and transform strings become harder to edit in Studio
const scale = interpolate(frame, [0, 100], [0, 1]);

style={{
  transform: `scale(${scale})`,
}}
```

## Assets

Place assets in the `public/` folder at your project root.
Use `staticFile()` to reference files from the `public/` folder.

## Media components

Add video and audio using `<Video>` and `<Audio>` from `@remotion/media`.  
Add images using the `<CanvasImage>` component.
Add animated GIFs, APNG, WebP or AVIF images using `<AnimatedImage>`, use `@remotion/gif` if not using Chrome.
Use `staticFile()` for files in `public/` or pass a remote URL directly:

```tsx
import { Audio, Video } from "@remotion/media";
import { staticFile, CanvasImage, AnimatedImage } from "remotion";

export const MyComposition = () => {
  return (
    <>
      <Video src={staticFile("video.mp4")} style={{ opacity: 0.5 }} />
      <Audio src={staticFile("audio.mp3")} />
      <CanvasImage
        src={staticFile("logo.png")}
        style={{ width: 100, height: 100 }}
      />
      <Video src="https://remotion.media/video.mp4" />
      <AnimatedImage src={staticFile('nyancat.gif')} />
    </>
  );
};
```

If the composition is primarily a timeline of video or audio clips, read
[video-editing.md](video-editing.md) before choosing its source structure.

## Example scene

A background video with a lower third.
The lower third is an interactive component with its own timeline, registered as a [connected composition](connected-compositions.md).
Its text is passed as `children` and `accentColor` is an editable prop.
The fade-in is keyframed inline at the call site.

```tsx
// MyScene.tsx
import { Video } from "@remotion/media";
import { Easing, Interactive, interpolate, useCurrentFrame, useVideoConfig } from "remotion";
import { LowerThird } from "./LowerThird";

const MySceneInner = () => {
  const { fps } = useVideoConfig();
  const frame = useCurrentFrame();

  return (
    <>
      <Video
        name="Background"
        src="https://remotion.media/video.mp4"
        objectFit="cover"
        style={{
          position: "absolute",
          width: "100%",
          height: "100%",
        }}
      />
      <LowerThird
        name="Lower third"
        from={1 * fps}
        accentColor="#0b84f3"
        style={{
          opacity: interpolate(frame, [1 * fps, 2 * fps], [0, 1], {
            extrapolateRight: "clamp",
            extrapolateLeft: "clamp",
            easing: Easing.bezier(0.16, 1, 0.3, 1),
          }),
        }}
      >
        Jane Doe, Product Designer
      </LowerThird>
    </>
  );
};

export const MyScene = Interactive.create({
  Component: MySceneInner,
  layout: "absolute-fill",
});
```

```tsx
// LowerThird.tsx
import type React from "react";
import { Interactive, type InteractivitySchema } from "remotion";

type LowerThirdProps = {
  readonly children: React.ReactNode;
  readonly accentColor: string;
  readonly style?: React.CSSProperties;
};

const LowerThirdInner: React.FC<LowerThirdProps> = ({
  children,
  accentColor,
  style,
}) => {
  return (
    <div
      style={{
        position: "absolute",
        left: 80,
        bottom: 80,
        display: "flex",
        alignItems: "center",
        gap: 20,
        backgroundColor: "white",
        borderRadius: 16,
        padding: "20px 32px",
        color: "black",
        fontFamily: "Helvetica, Arial, sans-serif",
        fontSize: 48,
        fontWeight: 600,
        ...style,
      }}
    >
      <div
        style={{
          width: 8,
          alignSelf: "stretch",
          borderRadius: 4,
          backgroundColor: accentColor,
        }}
      />
      {children}
    </div>
  );
};

const lowerThirdSchema = {
  ...Interactive.childrenSchema,
  ...Interactive.textSchema,
  accentColor: {
    type: "color",
    default: "#0b84f3",
    description: "Accent color",
  },
} as const satisfies InteractivitySchema;

export const LowerThird = Interactive.create({
  Component: LowerThirdInner,
  layout: "none",
  schema: lowerThirdSchema,
});
```

```tsx title="src/Root.tsx"
import { Composition } from "remotion";
import { LowerThird } from "./LowerThird";
import { MyScene } from "./MyScene";

export const RemotionRoot: React.FC = () => {
  return (
    <>
      <Composition
        id="MyScene"
        component={MyScene}
        durationInFrames={60}
        fps={30}
        width={1280}
        height={720}
      />
      <Composition
        id="LowerThird"
        component={LowerThird}
        durationInFrames={30}
        fps={30}
        width={1280}
        height={720}
        defaultProps={{
          children: "Jane Doe, Product Designer",
          accentColor: "#0b84f3",
        }}
      />
    </>
  );
};
```

## Delaying, trimming

Put timing directly on components that support it. See [Timing props](./timing-props.md) for the supported props, examples, and order of operations.

## Maps

See [Remotion Maps](../remotion-maps/REFERENCE.md) if wanting to include maps in the video.

## Text highlights and annotations

See [text-highlights.md](text-highlights.md) for text highlights (highlight markers), circles, underlines, strike-throughs, crossed-off text, boxes.

## Multi-scene videos

See [multi-scene-video.md](multi-scene-video.md) if planning to make a video with multiple subsequent scenes.

## Connected compositions

When a scene or group of layers deserves its own editable timeline, follow [connected-compositions.md](connected-compositions.md). Prefer this structure for substantial scenes in a multi-scene video.

### Pre-compose action

For a Studio request such as `Pre-compose Ambient glow (src/BarChart.tsx:134)`, find the selected sequence markup at the given location. Make a connected composition, following [connected-compositions.md](connected-compositions.md): extract the markup into a named component, preferably make it interactive with `Interactive.create()`, and register the same exported component reference with a unique `<Composition>` in the root. Render the interactive component directly with its timing props, or as the only child of a sequence when that wrapper has a purpose. If the selected node is already a sequence, keep its props and extract its children. The registration needs dimensions, fps, duration, and `defaultProps` equivalent to its parent use. A component extraction without a registered composition does not complete a pre-compose request.

Carry inherited styles such as `fontFamily` and font loading into the extracted
component; see [parent independence](connected-compositions.md#make-the-component-independent-of-its-parent).

## Voiceover

See [voiceover.md](voiceover.md) for adding an AI-generated voiceover to Remotion compositions using ElevenLabs TTS.

## Embedding Videos

See [embedding-videos.md](embedding-videos.md) for advanced knowledge about embedding videos - trimming, volume, speed, looping, pitch.

## Embedding Audio

See [audio.md](audio.md) for advanced audio features like trimming, volume, speed, pitch.

## Cropping

See [cropping.md](cropping.md) if needing to crop the visible rectangle of a component.

## Transitions

See [transitions.md](transitions.md) for scene transition patterns.

## Motion blur

When adding motion blur or a movement trail, read [motion-blur.md](motion-blur.md) for the preferred HTML-in-canvas approach, preview requirements, and alternatives.

## Visual and pixel effects

When adding a visual effect, first identify the element or group it should affect.
If the target component supports `effects` and a built-in effect below matches the
request, prefer that effect over a CSS approximation. For example, apply
`vignette()` directly to a `<Video>`'s `effects` prop when the vignette should
affect that video.

These components accept `effects` directly:

| Import from        | Components                                                                                                                    |
| ------------------ | ----------------------------------------------------------------------------------------------------------------------------- |
| `remotion`         | `<Img>`, `<CanvasImage>`, `<AnimatedImage>`, `<Solid>`, `<HtmlInCanvas>`                                                      |
| `@remotion/media`  | `<Video>`                                                                                                                     |
| `@remotion/gif`    | `<Gif>`                                                                                                                       |
| `@remotion/rive`   | `<RemotionRiveCanvas>`                                                                                                        |
| `@remotion/shapes` | `<Arrow>`, `<Callout>`, `<Circle>`, `<Ellipse>`, `<Heart>`, `<Pie>`, `<Polygon>`, `<Rect>`, `<Spark>`, `<Star>`, `<Triangle>` |

Ordinary HTML elements, `<Interactive.*>` DOM wrappers, `<AbsoluteFill>`, and
`<Sequence>` do not accept `effects` directly. To apply effects to their content,
wrap them in `<HtmlInCanvas>` and put the `effects` prop on the wrapper.

For other elements, prefer regular HTML and CSS where suitable. Consider wrapping
a group in [`<HtmlInCanvas>`](html-in-canvas.md) when post-processing the whole
group is appropriate and the environment supports it.

Read [effects.md](effects.md) before applying an effect for imports, parameters,
and setup. It also covers reusable custom effects with `createEffect()` when no
built-in effect matches.

### Available effects

Built-in effects from `@remotion/effects`:

- Color and tone: `brightness()`, `colorCorrection()`, `colorKey()`, `contrast()`, `duotone()`, `exposure()`, `grayscale()`, `hue()`, `invert()`, `levels()`, `linearGradient()`, `linearGradientTint()`, `lut()`, `saturation()`, `shadowsHighlights()`, `thermalVision()`, `tint()`, `vibrance()`, `whiteBalance()`.
- Blur and trails: `blur()`, `lightTrail()`, `linearProgressiveBlur()`, `radialProgressiveBlur()`, `regionBlur()`, `zoomBlur()`.
- Lighting: `dropShadow()`, `glow()`, `lightLeak()`, `shine()`, `starburst()`, `vignette()`.
- Distortion and transforms: `barrelDistortion()`, `chromaticAberration()`, `cornerPin()`, `fisheye()`, `mirror()`, `noiseDisplacement()`, `scale()`, `skew()`, `tile()`, `uvTranslate()`, `wave()`, `xyTranslate()`.
- Textures and patterns: `burlap()`, `checkerboard()`, `contourLines()`, `dotGrid()`, `emboss()`, `flannel()`, `gridlines()`, `halftone()`, `halftoneLinearGradient()`, `lines()`, `liquidContours()`, `noise()`, `paper()`, `pattern()`, `rings()`, `scanlines()`, `speckle()`, `tvSignalOff()`, `waves()`, `whiteNoise()`, `zigzag()`.
- Edges: `outline()`, `roughenEdges()`, `shrinkwrap()`, `tear()`.
- Pixelation and transitions: `evolve()`, `linearProgressivePixelate()`, `pixelate()`, `pixelDissolve()`, `radialProgressivePixelate()`, `venetianBlinds()`.

## Color correction

Read [color-correction.md](color-correction.md) for how to apply color correction, either using the `colorCorrection()` effect or `lut()` to apply a 3D `.cube` color grade.

## 3D content

See [./3d.md](./3d.md) for 3D content in Remotion using Three.js and React Three Fiber.

## Sound effects

When needing to use sound effects, load the [./sfx.md](./sfx.md) file for more information.

## Audio visualization

When needing to visualize audio (spectrum bars, waveforms, bass-reactive effects), load the [./audio-visualization.md](./audio-visualization.md) file for more information.

## Maps

For static maps, animated routes and markers, geographic explainers, Mapbox, MapLibre, MapTiler, GeoJSON, or 3D geographic flyovers, load [Remotion Maps](../remotion-maps/REFERENCE.md).

## Captions

When dealing with captions or subtitles, load the [Remotion Captions](../remotion-captions/REFERENCE.md) skill for more information.

## Google Fonts

Is the recommended way to load fonts in Remotion. See [google-fonts.md](google-fonts.md) for how to load Google Fonts.

## Local fonts

See [local-fonts.md](local-fonts.md) for how to load local fonts.

## GIFs

See [gifs.md](gifs.md) for how to display GIFs synchronized with Remotion's timeline.

## Advanced Images

See [images.md](images.md) for sizing and positioning images, dynamic image paths, and getting image dimensions.

## Lottie animations

See [lottie.md](lottie.md) for embedding Lottie animations in Remotion.

## Timing

See [timing.md](timing.md) for more timing techniques for `interpolate()`.

## Parameterized videos

See [parameters.md](parameters.md) for making a composition parametrizable by adding a Zod schema.

## Measuring DOM nodes

See [measuring-dom-nodes.md](measuring-dom-nodes.md) for measuring DOM element dimensions in Remotion.

## Measuring text

See [measuring-text.md](measuring-text.md) for measuring text dimensions, fitting text to containers, and checking overflow.

## Using FFmpeg

For some video operations, such as trimming videos or detecting silence, FFmpeg should be used. Load the [./ffmpeg.md](./ffmpeg.md) file for more information.

## Silence detection

When needing to detect and trim silent segments from video or audio files, load the [./silence-detection.md](./silence-detection.md) file.

## Dynamic duration, dimensions and data

See [calculate-metadata.md](calculate-metadata.md) for dynamically set composition duration, dimensions, and props.

## Compositions and stills

Before registering `<Composition>` or `<Still>` elements, read [compositions.md](compositions.md) for source-editable registrations, folders, default props and nesting. For Studio navigation into a scene's own timeline, use [connected compositions](connected-compositions.md).

## Advanced sequencing

See [sequencing.md](sequencing.md) for more sequencing patterns - delay, trim, limit duration of items.

## Install modules

Use `npx remotion add` to add new packages with the right version:

```
npx remotion add @remotion/media
```

This goes for `@remotion/*` packages, `mediabunny`, `@mediabunny/*`, `zod`, and `@huggingface/transformers`.

## Visual checks

When a visual check is useful, open the [Remotion Studio](../remotion-studio/REFERENCE.md) for an interactive preview.

You can also use [Rendering](../remotion-render/REFERENCE.md) to inspect one or several frames as images.


<!-- ===== FILE: remotion/remotion-markup/3d.md ===== -->

---
name: 3d
description: 3D content in Remotion using Three.js and React Three Fiber.
metadata:
  tags: 3d, three, threejs
---

# Using Three.js and React Three Fiber in Remotion

Follow React Three Fiber and Three.js best practices.  
Only the following Remotion-specific rules need to be followed:

## Prerequisites

First, the `@remotion/three` package needs to be installed.  
If it is not, use the following command:

```bash
npx remotion add @remotion/three # If project uses npm
bunx remotion add @remotion/three # If project uses bun
yarn remotion add @remotion/three # If project uses yarn
pnpm exec remotion add @remotion/three # If project uses pnpm
```

## Using ThreeCanvas

You MUST wrap 3D content in `<ThreeCanvas>` and include proper lighting.  
`<ThreeCanvas>` MUST have a `width` and `height` prop.

```tsx
import { ThreeCanvas } from "@remotion/three";
import { useVideoConfig } from "remotion";

const { width, height } = useVideoConfig();

<ThreeCanvas width={width} height={height}>
  <ambientLight intensity={0.4} />
  <directionalLight position={[5, 5, 5]} intensity={0.8} />
  <mesh>
    <sphereGeometry args={[1, 32, 32]} />
    <meshStandardMaterial color="red" />
  </mesh>
</ThreeCanvas>;
```

## No animations not driven by `useCurrentFrame()`

Shaders, models etc MUST NOT animate by themselves.  
No animations are allowed unless they are driven by `useCurrentFrame()`.  
Otherwise, it will cause flickering during rendering.

Using `useFrame()` from `@react-three/fiber` is forbidden.

## Animate using `useCurrentFrame()`

Use `useCurrentFrame()` to perform animations.

```tsx
const frame = useCurrentFrame();
const rotationY = frame * 0.02;

<mesh rotation={[0, rotationY, 0]}>
  <boxGeometry args={[2, 2, 2]} />
  <meshStandardMaterial color="#4a9eff" />
</mesh>;
```

## Using `<Sequence>` inside `<ThreeCanvas>`

The `layout` prop of any `<Sequence>` inside a `<ThreeCanvas>` must be set to `none`.

```tsx
import { Sequence } from "remotion";
import { ThreeCanvas } from "@remotion/three";

const { width, height } = useVideoConfig();

<ThreeCanvas width={width} height={height}>
  <Sequence layout="none">
    <mesh>
      <boxGeometry args={[2, 2, 2]} />
      <meshStandardMaterial color="#4a9eff" />
    </mesh>
  </Sequence>
</ThreeCanvas>;
```


<!-- ===== FILE: remotion/remotion-markup/audio-visualization.md ===== -->

---
name: audio-visualization
description: Audio visualization patterns - spectrum bars, waveforms, bass-reactive effects
metadata:
  tags: audio, visualization, spectrum, waveform, bass, music, audiogram, frequency
---

# Audio Visualization in Remotion

## Prerequisites

```bash
npx remotion add @remotion/media-utils
```

## Loading Audio Data

Use `useWindowedAudioData()` (https://www.remotion.dev/docs/use-windowed-audio-data) to load audio data:

```tsx
import { useWindowedAudioData } from "@remotion/media-utils";
import { staticFile, useCurrentFrame, useVideoConfig } from "remotion";

const frame = useCurrentFrame();
const { fps } = useVideoConfig();

const { audioData, dataOffsetInSeconds } = useWindowedAudioData({
  src: staticFile("podcast.wav"),
  frame,
  fps,
  windowInSeconds: 30,
});
```

## Spectrum Bar Visualization

Use `visualizeAudio()` (https://www.remotion.dev/docs/visualize-audio) to get frequency data for bar charts:

```tsx
import { useWindowedAudioData, visualizeAudio } from "@remotion/media-utils";
import { staticFile, useCurrentFrame, useVideoConfig } from "remotion";

const frame = useCurrentFrame();
const { fps } = useVideoConfig();

const { audioData, dataOffsetInSeconds } = useWindowedAudioData({
  src: staticFile("music.mp3"),
  frame,
  fps,
  windowInSeconds: 30,
});

if (!audioData) {
  return null;
}

const frequencies = visualizeAudio({
  fps,
  frame,
  audioData,
  numberOfSamples: 256,
  optimizeFor: "speed",
  dataOffsetInSeconds,
});

return (
  <div style={{ display: "flex", alignItems: "flex-end", height: 200 }}>
    {frequencies.map((v, i) => (
      <div
        key={i}
        style={{
          flex: 1,
          height: `${v * 100}%`,
          backgroundColor: "#0b84f3",
          margin: "0 1px",
        }}
      />
    ))}
  </div>
);
```

- `numberOfSamples` must be power of 2 (32, 64, 128, 256, 512, 1024)
- Values range 0-1; left of array = bass, right = highs
- Use `optimizeFor: "speed"` for Lambda or high sample counts

**Important:** When passing `audioData` to child components, also pass the `frame` from the parent. Do not call `useCurrentFrame()` in each child - this causes discontinuous visualization when children are inside `<Sequence>` with offsets.

## Waveform Visualization

Use `visualizeAudioWaveform()` (https://www.remotion.dev/docs/media-utils/visualize-audio-waveform) with `createSmoothSvgPath()` (https://www.remotion.dev/docs/media-utils/create-smooth-svg-path) for oscilloscope-style displays:

```tsx
import {
  createSmoothSvgPath,
  useWindowedAudioData,
  visualizeAudioWaveform,
} from "@remotion/media-utils";
import { staticFile, useCurrentFrame, useVideoConfig } from "remotion";

const frame = useCurrentFrame();
const { width, fps } = useVideoConfig();
const HEIGHT = 200;

const { audioData, dataOffsetInSeconds } = useWindowedAudioData({
  src: staticFile("voice.wav"),
  frame,
  fps,
  windowInSeconds: 30,
});

if (!audioData) {
  return null;
}

const waveform = visualizeAudioWaveform({
  fps,
  frame,
  audioData,
  numberOfSamples: 256,
  windowInSeconds: 0.5,
  dataOffsetInSeconds,
});

const path = createSmoothSvgPath({
  points: waveform.map((y, i) => ({
    x: (i / (waveform.length - 1)) * width,
    y: HEIGHT / 2 + (y * HEIGHT) / 2,
  })),
});

return (
  <svg width={width} height={HEIGHT}>
    <path d={path} fill="none" stroke="#0b84f3" strokeWidth={2} />
  </svg>
);
```

## Bass-Reactive Effects

Extract low frequencies for beat-reactive animations:

```tsx
const frequencies = visualizeAudio({
  fps,
  frame,
  audioData,
  numberOfSamples: 128,
  optimizeFor: "speed",
  dataOffsetInSeconds,
});

const lowFrequencies = frequencies.slice(0, 32);
const bassIntensity =
  lowFrequencies.reduce((sum, v) => sum + v, 0) / lowFrequencies.length;

const scale = 1 + bassIntensity * 0.5;
const opacity = Math.min(0.6, bassIntensity * 0.8);
```

## Volume-Based Waveform

Use `getWaveformPortion()` (https://www.remotion.dev/docs/get-waveform-portion) when you need simplified volume data instead of frequency spectrum:

```tsx
import { getWaveformPortion } from "@remotion/media-utils";
import { useCurrentFrame, useVideoConfig } from "remotion";

const frame = useCurrentFrame();
const { fps } = useVideoConfig();
const currentTimeInSeconds = frame / fps;

const waveform = getWaveformPortion({
  audioData,
  startTimeInSeconds: currentTimeInSeconds,
  durationInSeconds: 5,
  numberOfSamples: 50,
});

// Returns array of { index, amplitude } objects (amplitude: 0-1)
waveform.map((bar) => (
  <div key={bar.index} style={{ height: bar.amplitude * 100 }} />
));
```

## Postprocessing

Low frequencies naturally dominate. Apply logarithmic scaling for visual balance:

```tsx
const minDb = -100;
const maxDb = -30;

const scaled = frequencies.map((value) => {
  const db = 20 * Math.log10(value);
  return (db - minDb) / (maxDb - minDb);
});
```


<!-- ===== FILE: remotion/remotion-markup/audio.md ===== -->

---
name: audio
description: Using audio and sound in Remotion - importing, trimming, volume, speed, pitch
metadata:
  tags: audio, media, trim, volume, speed, loop, pitch, mute, sound, sfx
---

# Using audio in Remotion

## Prerequisites

First, the @remotion/media package needs to be installed.
If it is not installed, use the following command:

```bash
npx remotion add @remotion/media
```

## Importing Audio

Use `<Audio>` from `@remotion/media` to add audio to your composition.

```tsx
import { Audio } from "@remotion/media";
import { staticFile } from "remotion";

export const MyComposition = () => {
  return <Audio src={staticFile("audio.mp3")} />;
};
```

Remote URLs are also supported:

```tsx
import { Audio } from "@remotion/media";

<Audio src="https://remotion.media/audio.mp3" />
```

By default, audio plays from the start, at full volume and full length.
Multiple audio tracks can be layered by adding multiple `<Audio>` components.

## Trimming

Use `trimBefore` to skip the beginning of the audio and `durationInFrames` to end it early. Values are in frames.

```tsx
import { Audio } from "@remotion/media";

const { fps } = useVideoConfig();

return (
  <Audio
    src={staticFile("audio.mp3")}
    trimBefore={2 * fps} // Skip the first 2 seconds
    durationInFrames={8 * fps} // Play 8 seconds, until the 10 second mark
  />
);
```

The audio still starts playing at the beginning of the composition - only the specified portion is played.

## Delaying

Set `from` directly on `<Audio>` to delay when it starts:

```tsx
import { staticFile, useVideoConfig } from "remotion";
import { Audio } from "@remotion/media";

const { fps } = useVideoConfig();

return (
  <Audio from={fps} src={staticFile("audio.mp3")} />
);
```

The audio will start playing after 1 second.

## Volume

Set a static volume (0 to 1):

```tsx
import { Audio } from "@remotion/media";

<Audio src={staticFile("audio.mp3")} volume={0.5} />
```

Use `useCurrentFrame()` and `interpolate()` for keyframed volume:

```tsx
import { Audio } from "@remotion/media";
import { interpolate, staticFile, useCurrentFrame, useVideoConfig } from "remotion";

const frame = useCurrentFrame();
const { fps } = useVideoConfig();

return (
  <Audio
    src={staticFile("audio.mp3")}
    volume={interpolate(frame, [0, 1 * fps], [0, 1], {
      extrapolateLeft: "clamp",
      extrapolateRight: "clamp",
    })}
  />
);
```

With Studio interactivity enabled, these keyframes can be edited and are shown as a volume curve in the timeline.

## Muting

Use `muted` to silence the audio. It can be set dynamically:

```tsx
import { Audio } from "@remotion/media";

const frame = useCurrentFrame();
const { fps } = useVideoConfig();

return (
  <Audio
    src={staticFile("audio.mp3")}
    muted={frame >= 2 * fps && frame <= 4 * fps} // Mute between 2s and 4s
  />
);
```

## Speed

Use `playbackRate` to change the playback speed:

```tsx
import { Audio } from "@remotion/media";

// 2x speed
<Audio src={staticFile("audio.mp3")} playbackRate={2} />
// Half speed
<Audio src={staticFile("audio.mp3")} playbackRate={0.5} />
```

Reverse playback is not supported.

## Looping

Use `loop` to loop the audio indefinitely:

```tsx
import { Audio } from "@remotion/media";

<Audio src={staticFile("audio.mp3")} loop />
```

Put `name`, `from`, `loop`, and `volume` directly on `<Audio>`.

```tsx
import { Audio } from "@remotion/media";
import { interpolate, staticFile, useCurrentFrame } from "remotion";

const frame = useCurrentFrame();

<Audio
  src={staticFile("audio.mp3")}
  loop
  volume={interpolate(frame, [0, 300], [1, 0], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
  })}
/>
```

## Pitch

Use `toneFrequency` to adjust the pitch without affecting speed. Values range from 0.01 to 2:

```tsx
import { Audio } from "@remotion/media";

<Audio
  src={staticFile("audio.mp3")}
  toneFrequency={1.5} // Higher pitch
/>
<Audio
  src={staticFile("audio.mp3")}
  toneFrequency={0.8} // Lower pitch
/>
```

Pitch shifting only works during server-side rendering, not in the Remotion Studio preview or in the `<Player />`.


<!-- ===== FILE: remotion/remotion-markup/calculate-metadata.md ===== -->

---
name: calculate-metadata
description: Dynamically set composition duration, dimensions, and props
metadata:
  tags: calculateMetadata, duration, dimensions, props, dynamic
---

# Using calculateMetadata

Use `calculateMetadata` on a `<Composition>` to dynamically set duration, dimensions, and transform props before rendering.
Use it when metadata depends on input props, fetched data, or asset metadata.
For static dimensions, duration, FPS, and initial props, inline the values on `<Composition>` instead.

```tsx
<Composition
  id="MyComp"
  component={MyComponent}
  durationInFrames={300}
  fps={30}
  width={1920}
  height={1080}
  defaultProps={{ videoSrc: "https://remotion.media/video.mp4" }}
  calculateMetadata={calculateMetadata}
/>
```

## Setting duration based on a video

Use the [`getVideoDuration`](../remotion-multimedia/get-video-duration.md) and [`getVideoDimensions`](../remotion-multimedia/get-video-dimensions.md) skills to get the video duration and dimensions:

```tsx
import { CalculateMetadataFunction } from "remotion";
import { getVideoDuration } from "./get-video-duration";

const calculateMetadata: CalculateMetadataFunction<Props> = async ({
  props,
}) => {
  const durationInSeconds = await getVideoDuration(props.videoSrc);

  return {
    durationInFrames: Math.ceil(durationInSeconds * 30),
  };
};
```

## Matching dimensions of a video

Use the [`getVideoDimensions`](../remotion-multimedia/get-video-dimensions.md) skill to get the video dimensions:

```tsx
import { CalculateMetadataFunction } from "remotion";
import { getVideoDuration } from "./get-video-duration";
import { getVideoDimensions } from "./get-video-dimensions";

const calculateMetadata: CalculateMetadataFunction<Props> = async ({
  props,
}) => {
  const dimensions = await getVideoDimensions(props.videoSrc);

  return {
    width: dimensions.width,
    height: dimensions.height,
  };
};
```

## Setting duration based on multiple videos

```tsx
const calculateMetadata: CalculateMetadataFunction<Props> = async ({
  props,
}) => {
  const metadataPromises = props.videos.map((video) =>
    getVideoDuration(video.src),
  );
  const allMetadata = await Promise.all(metadataPromises);

  const totalDuration = allMetadata.reduce(
    (sum, durationInSeconds) => sum + durationInSeconds,
    0,
  );

  return {
    durationInFrames: Math.ceil(totalDuration * 30),
  };
};
```

## Setting a default outName

Set the default output filename based on props:

```tsx
const calculateMetadata: CalculateMetadataFunction<Props> = async ({
  props,
}) => {
  return {
    defaultOutName: `video-${props.id}`, // .mp4 is added automatically
  };
};
```

## Transforming props

Fetch data or transform props before rendering:

```tsx
const calculateMetadata: CalculateMetadataFunction<Props> = async ({
  props,
  abortSignal,
}) => {
  const response = await fetch(props.dataUrl, { signal: abortSignal });
  const data = await response.json();

  return {
    props: {
      ...props,
      fetchedData: data,
    },
  };
};
```

The `abortSignal` cancels stale requests when props change in the Studio.

## Return value

All fields are optional. Returned values override the `<Composition>` props:

- `durationInFrames`: Number of frames
- `width`: Composition width in pixels
- `height`: Composition height in pixels
- `fps`: Frames per second
- `props`: Transformed props passed to the component
- `defaultOutName`: Default output filename
- `defaultCodec`: Default codec for rendering


<!-- ===== FILE: remotion/remotion-markup/color-correction.md ===== -->

---
name: color-correction
description: Correct exposure, white balance, and tone, and apply 3D Cube LUTs to footage.
metadata:
  tags: color-correction, color-grading, lut, cube, exposure, white-balance
---

# Color correction

Apply color adjustments through the `effects` prop of `<Video>` from `@remotion/media`, or other supported components.  
See [effects.md](effects.md) for more context on effects.

## Primary adjustments

Prefer [`colorCorrection()`](https://www.remotion.dev/docs/effects/color-correction) when combining adjustments.  
It performs them in one WebGL pass and exposes controls in the Studio.

| Control                 | Meaning and range                                                         | Neutral value |
| ----------------------- | ------------------------------------------------------------------------- | ------------- |
| `exposure`              | Stops, from `-5` to `5`; positive values brighten                         | `0`           |
| `temperature`           | From `-1` (cooler) to `1` (warmer)                                        | `0`           |
| `tint`                  | From `-1` (greener) to `1` (more magenta)                                 | `0`           |
| `shadows`, `highlights` | From `-1` to `1`; negative values darken, positive values lift the region | `0`           |
| `blacks`, `whites`      | From `-1` to `1`; target narrower regions near black and white            | `0`           |
| `contrast`              | Non-negative multiplier around `pivot` (`0` to `1`, default `0.5`)        | `1`           |
| `saturation`            | Non-negative multiplier; `0` is grayscale                                 | `1`           |
| `vibrance`              | From `-1` to `1`; positive values emphasize muted colors                  | `0`           |

```tsx
import {colorCorrection} from '@remotion/effects/color-correction';
import {Video} from '@remotion/media';
import {staticFile} from 'remotion';

export const CorrectedVideo = () => {
  return (
    <Video
      src={staticFile('footage.mp4')}
      effects={[
        colorCorrection({
          exposure: 0.25,
          temperature: 0.1,
          tint: -0.03,
          shadows: 0.15,
          highlights: -0.1,
          contrast: 1.1,
          saturation: 1.05,
          vibrance: 0.15,
        }),
      ]}
    />
  );
};
```

Internally, `colorCorrection()` applies exposure, white balance, tonal regions,
contrast, saturation, then vibrance. Omitted controls use their neutral values.
Keep everything inline on the target's `effects` prop.

Standalone effects are also available when a different order or an additional
adjustment is needed: `exposure()`, `whiteBalance()`, `shadowsHighlights()`,
`contrast()`, `saturation()`, and `vibrance()`. See [effects](effects.md)

## LUTs and combining effects

A LUT (lookup table) maps input RGB colors to output colors. Use
[`lut()`](https://www.remotion.dev/docs/effects/lut) to apply a 3D `.cube` LUT.  
Its `content` parameter takes the complete file contents as a string.

This example uses a small warm LUT inline:

```tsx
import {colorCorrection} from '@remotion/effects/color-correction';
import {lut} from '@remotion/effects/lut';
import {Video} from '@remotion/media';
import {staticFile} from 'remotion';

export const GradedVideo = () => {
  return (
    <Video
      src={staticFile('footage.mp4')}
      effects={[
        colorCorrection({exposure: 0.25, contrast: 1.1}),
        lut({
          content: `TITLE "Warm"
LUT_3D_SIZE 2
0 0 0
1 0.1 0
0 0.9 0.1
1 0.9 0.1
0 0.1 0.8
1 0.2 0.7
0 0.9 0.8
1 0.9 0.8`,
        }),
      ]}
    />
  );
};
```

### Supported format and limitations

- Only 3D `.cube` LUTs are supported. `LUT_3D_SIZE` must be an integer from `2`
  to `256`, followed by exactly `size ** 3` RGB rows. 1D LUTs are unsupported.
- Optional `TITLE`, `DOMAIN_MIN`, `DOMAIN_MAX`, blank lines, and `#` comments are
  supported. Other LUT formats need conversion before use.
- `lut()` has no `src` or strength/amount parameter. Use `disabled: true` to
  bypass it.

## Studio workflow

Put `.cube` files in `public/` to preview them in the Assets panel.  
The user can drag a 3D `.cube` file from the computer or Assets panel onto a
video in the canvas or timeline to apply the LUT effect.

## See also

- [Color correction documentation](https://www.remotion.dev/docs/color-correction)


<!-- ===== FILE: remotion/remotion-markup/compositions.md ===== -->

---
name: compositions
description: Defining compositions, stills, folders, default props and dynamic metadata
metadata:
  tags: composition, still, folder, props, metadata
---

A `<Composition>` defines the component, width, height, fps and duration of a renderable video.

## Source-editable registrations

Give each composition or still that should be edited independently in the
Studio its own authored JSX node. Use a JSX string literal for `id`, and keep
its metadata and editable default values directly on that node.

Programmatic registration is suitable when the generated compositions are
intentionally controlled as one source template and do not need to be
reordered, duplicated, deleted or edited individually in the Studio.

```tsx title="src/MyComposition.tsx"
type Props = {
  readonly title: string;
};

export const MyComposition = ({title}: Props) => <h1>{title}</h1>;
```

```tsx title="src/Root.tsx"
import {Composition} from 'remotion';
import {MyComposition} from './MyComposition';

export const RemotionRoot = () => {
  return (
    <>
      <Composition
        id="Launch"
        component={MyComposition}
        durationInFrames={180}
        fps={30}
        width={1920}
        height={1080}
        defaultProps={{title: 'Launch'}}
      />
      <Composition
        id="Recap"
        component={MyComposition}
        durationInFrames={240}
        fps={30}
        width={1920}
        height={1080}
        defaultProps={{title: 'Recap'}}
      />
    </>
  );
};
```

Both registrations can reuse the same component. Keeping them as separate JSX
nodes gives each one its own source-editing target.

## Default Props and scaffold metadata

Pass `defaultProps` to provide initial values for your component.  
Values must be JSON-serializable (`Date`, `Map`, `Set`, and `staticFile()` are supported).
Use `defaultProps` for composition-wide values that should be visible and editable before the video renders.

Keep data owned by a child editor on that child's JSX node. For example,
captions that should remain editable in the Caption editor belong as an inline
array on `<BasicCaptions>`, not in composition `defaultProps` or a component
prop. See [Displaying captions](../remotion-captions/display-captions.md).

For Studio editing, keep `defaultProps` as an inline object literal on `<Composition>` or `<Still>`.
Keep values that should be written back directly in the object instead of deriving them from a loop variable.
Do not store it in a variable, import it, spread it, create it with a helper, or wrap it in `satisfies`.
Use `type` declarations for props rather than `interface` to ensure `defaultProps` type safety.

```tsx title="src/Root.tsx"
import {Composition} from 'remotion';
import {MyComposition} from './MyComposition';

const defaultProps = { title: "Hello World" };

export const RemotionRoot = () => {
  return (
    <>
      {/* 👍 Inline metadata and defaults */}
      <Composition
        id="MyComposition"
        component={MyComposition}
        durationInFrames={100}
        fps={30}
        width={1080}
        height={1080}
        defaultProps={{ title: "Hello World" }}
      />

      {/* 👎 Hidden defaults cannot be saved back by Studio */}
      <Composition
        id="OtherComposition"
        component={MyComposition}
        durationInFrames={100}
        fps={30}
        width={1080}
        height={1080}
        defaultProps={defaultProps}
      />
    </>
  );
};
```

## Folders

Use `<Folder>` to organize compositions in the sidebar.  
Folder names can only contain letters, numbers, and hyphens.

```tsx title="src/Root.tsx"
import { Composition, Folder } from "remotion";

export const RemotionRoot = () => {
  return (
    <>
      <Folder name="Marketing">
        <Composition id="Promo" /* ... */ />
        <Composition id="Ad" /* ... */ />
      </Folder>
      <Folder name="Social">
        <Folder name="Instagram">
          <Composition id="Story" /* ... */ />
          <Composition id="Reel" /* ... */ />
        </Folder>
      </Folder>
    </>
  );
};
```

## Stills

Use `<Still>` for single-frame images. It does not require `durationInFrames` or `fps`.

```tsx title="src/Root.tsx"
import { Still } from "remotion";
import { Thumbnail } from "./Thumbnail";

export const RemotionRoot = () => {
  return (
    <Still
      id="Thumbnail"
      component={Thumbnail}
      width={1280}
      height={720}
    />
  );
};
```

## Dynamic duration, width, and height

Use [`calculateMetadata`](./calculate-metadata.md) to make dimensions, duration, or props dynamic based on input props, fetched data, or asset metadata.

## Nesting compositions within another

To render a composition's component inside another composition, use `<Sequence>` with `width` and `height` when the nested content needs its own dimensions.

When the nested scene should have its own editable Studio timeline, use the [connected composition structure](connected-compositions.md).

```tsx
<>
  <Video src="https://remotion.media/video.mp4" />
  <Sequence
    width={1920}
    height={1080}
  >
    <OverlayComponent />
  </Sequence>
</>
```


<!-- ===== FILE: remotion/remotion-markup/connected-compositions.md ===== -->

# Connected compositions

Make every scene and reusable element a connected composition:

1. Export it with `Interactive.create()`. Set `layout: 'absolute-fill'` for a scene or `layout: 'none'` for a bounded element.
2. Render the exported component directly inside a named `Track`, with inline timing and props.
3. Register that same reference in `<Composition component={...}>`, alongside the parent video. Keep metadata and representative `defaultProps` inline.

Follow the complete [Track + connected compositions example](../remotion-interactivity/timeline-structure.md), including `Title.tsx`, `Chapter.tsx`, `MyVideo.tsx`, and `Root.tsx`.

Double-clicking an instance opens its connected composition. Editing the shared
component updates both views. Registration defaults do not automatically apply
to the instances in the parent.

## Make the component independent of its parent

The parent is not mounted when the connected composition opens on its own.
Keep required typography in the component and supply background and alignment
in its inline registration defaults. Load fonts in its module or an imported
shared module; see [Google fonts](google-fonts.md) and [local fonts](local-fonts.md).

Verify the component by opening its standalone composition. Keep its fps and
dimensions consistent with the parent unless a difference is intentional.


<!-- ===== FILE: remotion/remotion-markup/cropping.md ===== -->

# Cropping

Preferably, the `cropLeft`, `cropRight`, `cropTop` and `cropBottom` props are used to crop content.
It allows for interactively dragging the components and adapting the outlines in the canvas to the crop.

The following components support `crop*` props:

- `<Sequence>` from `remotion`, when `layout="absolute-fill"`
- `<Interactive.*>` HTML and SVG elements from `remotion`
- Custom components made with `Interactive.create()` from `remotion`, using a managed `layout: 'absolute-fill'` root or forwarding `style` to their own visual root
- `<CanvasImage>` from `remotion`
- `<Img>` from `remotion`
- `<AnimatedImage>` from `remotion`
- `<HtmlInCanvas>` from `remotion`
- `<Solid>` from `remotion`
- `<Video>` from `@remotion/media`
- `<Gif>` from `@remotion/gif`
- `<RemotionRiveCanvas>` from `@remotion/rive`

Crop values are ratios between `0` and `1`.
A value of `0` applies no crop on that edge.
A value of `1` is a full crop.
Keep [Interactivity Best Practices](../remotion-interactivity/REFERENCE.md) also for cropping, to keep it editable and keyframable.

```tsx
<CanvasImage
  src={staticFile("photo.png")}
  cropLeft={interpolate(frame, [0, 30], [0, 0.25], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
  })}
  cropBottom={0.1}
/>
```

Do not use `clipPath` together with crop props.


<!-- ===== FILE: remotion/remotion-markup/effects.md ===== -->

---
name: effects
description: Canvas/WebGL visual effects for Remotion using effects arrays and createEffect().
metadata:
  tags: effects, visual-effects, webgl, canvas, video, create-effect
---

Read this guidance when adding an effect to a component that supports `effects`,
or when considering canvas post-processing or a reusable custom effect.

Docs: https://www.remotion.dev/docs/effects
Custom effect docs: https://www.remotion.dev/docs/create-effect

For exposure, white balance, tonal adjustments, and LUTs, read
[color-correction.md](color-correction.md).

## Usage

Install the package that provides the chosen effect:

```bash
npx remotion add @remotion/effects
```

Effects are functions passed to the `effects` prop of supported components.

These components accept `effects` directly:

| Import from        | Components                                                                                                                    |
| ------------------ | ----------------------------------------------------------------------------------------------------------------------------- |
| `remotion`         | `<Img>`, `<CanvasImage>`, `<AnimatedImage>`, `<Solid>`, `<HtmlInCanvas>`                                                      |
| `@remotion/media`  | `<Video>`                                                                                                                     |
| `@remotion/gif`    | `<Gif>`                                                                                                                       |
| `@remotion/rive`   | `<RemotionRiveCanvas>`                                                                                                        |
| `@remotion/shapes` | `<Arrow>`, `<Callout>`, `<Circle>`, `<Ellipse>`, `<Heart>`, `<Pie>`, `<Polygon>`, `<Rect>`, `<Spark>`, `<Star>`, `<Triangle>` |

Ordinary HTML elements, `<Interactive.*>` DOM wrappers, `<AbsoluteFill>`, and
`<Sequence>` do not accept `effects` directly. To apply effects to their content,
wrap them in `<HtmlInCanvas>` and put the `effects` prop on the wrapper.

For example, apply an effect directly to a video:

```tsx
import {Video} from '@remotion/media';
import {blur} from '@remotion/effects/blur';

<Video
  src="https://remotion.media/video.mp4"
  effects={[blur({radius: 8})]}
/>;
```

Use the effect docs for exact props and imports. Most `@remotion/effects` imports use `@remotion/effects/<effect-slug>`; `uvTranslate()` and `xyTranslate()` use `@remotion/effects/translate`.

These effects use WebGL2. During renders, enable WebGL with:

```ts
import {Config} from '@remotion/cli/config';

Config.setChromiumOpenGlRenderer('angle');
```

## Available effects

Built-in effects from `@remotion/effects`:

- Color and tone: `brightness()`, `colorCorrection()`, `colorKey()`, `contrast()`, `duotone()`, `exposure()`, `grayscale()`, `hue()`, `invert()`, `levels()`, `linearGradient()`, `linearGradientTint()`, `lut()`, `saturation()`, `shadowsHighlights()`, `thermalVision()`, `tint()`, `vibrance()`, `whiteBalance()`.
- Blur and trails: `blur()`, `lightTrail()`, `linearProgressiveBlur()`, `radialProgressiveBlur()`, `regionBlur()`, `zoomBlur()`.
- Lighting: `dropShadow()`, `glow()`, `lightLeak()`, `shine()`, `starburst()`, `vignette()`.
- Distortion and transforms: `barrelDistortion()`, `chromaticAberration()`, `cornerPin()`, `fisheye()`, `mirror()`, `noiseDisplacement()`, `scale()`, `skew()`, `tile()`, `uvTranslate()`, `wave()`, `xyTranslate()`.
- Textures and patterns: `burlap()`, `checkerboard()`, `contourLines()`, `dotGrid()`, `emboss()`, `flannel()`, `gridlines()`, `halftone()`, `halftoneLinearGradient()`, `lines()`, `liquidContours()`, `noise()`, `paper()`, `pattern()`, `rings()`, `scanlines()`, `speckle()`, `tvSignalOff()`, `waves()`, `whiteNoise()`, `zigzag()`.
- Edges: `outline()`, `roughenEdges()`, `shrinkwrap()`, `tear()`.
- Pixelation and transitions: `evolve()`, `linearProgressivePixelate()`, `pixelate()`, `pixelDissolve()`, `radialProgressivePixelate()`, `venetianBlinds()`.

Example:

```tsx
import {Video} from '@remotion/media';
import {brightness} from '@remotion/effects/brightness';

<Video
  src="https://remotion.media/video.mp4"
  effects={[brightness({})]}
/>;
```

## Custom effects

Use `createEffect()` from `remotion` when the user wants a reusable effect factory that works in the same `effects` array as `@remotion/effects`.

Prefer a custom effect over `<HtmlInCanvas onPaint>` when the transformation should be reusable, parameterized, editable in Studio, or stackable with other effects.

For quick project-specific effects, keep the effect next to the composition, for example `src/effects/palette-map.ts`. For library effects intended for `@remotion/effects`, follow the repository's `add-effect` skill instead.

`createEffect()` expects:

- `type`: stable reverse-DNS identifier, for example `com.example.paletteMap`.
- `label`: Studio label, commonly `paletteMap()`.
- `documentationLink`: URL or `null`.
- `backend`: `"2d"`, `"webgl2"` or `"webgpu"`.
- `calculateKey(params)`: stable string containing every resolved parameter that changes output.
- `setup(target)`: create reusable backend state, or return `null`.
- `apply({source, target, width, height, params, state, flipSourceY})`: draw the transformed result into `target`.
- `cleanup(state)`: free resources created by `setup()`.
- `schema`: an `InteractivitySchema` for Studio controls. `disabled` is added automatically.
- `validateParams(params)`: throw on missing or invalid values.

Use `backend: "2d"` for simple pixel, filter, drawImage, or image-data effects. Use WebGL2 only when shader math or GPU performance is needed; during renders, enable WebGL as shown above.

```ts
import {createEffect, type InteractivitySchema} from 'remotion';

type MyEffectParams = {
  readonly amount?: number;
};

const myEffectSchema = {
  amount: {
    type: 'number',
    min: 0,
    max: 1,
    step: 0.01,
    default: 1,
    description: 'Amount',
  },
} as const satisfies InteractivitySchema;

const resolve = (params: MyEffectParams) => ({
  amount: params.amount ?? 1,
});

export const myEffect = createEffect<MyEffectParams, null>({
  type: 'com.example.myEffect',
  label: 'myEffect()',
  documentationLink: null,
  backend: '2d',
  calculateKey: (params) => {
    const {amount} = resolve(params);
    return `my-effect-${amount}`;
  },
  setup: () => null,
  apply: ({source, target, width, height, params}) => {
    const ctx = target.getContext('2d');
    if (!ctx) {
      throw new Error('Could not get a 2D context for myEffect().');
    }

    const {amount} = resolve(params);

    ctx.clearRect(0, 0, width, height);
    ctx.filter = `opacity(${amount * 100}%)`;
    ctx.drawImage(source, 0, 0, width, height);
    ctx.filter = 'none';
  },
  cleanup: () => undefined,
  schema: myEffectSchema,
  validateParams: ({amount = 1}) => {
    if (typeof amount !== 'number' || !Number.isFinite(amount) || amount < 0 || amount > 1) {
      throw new TypeError('amount must be a number between 0 and 1');
    }
  },
});
```

For a WebGL2 effect, compile/link shaders in `setup()`, keep the program, fullscreen quad, texture, and uniform locations in state, upload `source` in `apply()`, and free GPU resources in `cleanup()`. Minimal shape:

```ts
import {createEffect, type InteractivitySchema} from 'remotion';

type RgbShiftParams = {
  readonly amount?: number;
};

type RgbShiftState = {
  readonly gl: WebGL2RenderingContext;
  readonly program: WebGLProgram;
  readonly vao: WebGLVertexArrayObject;
  readonly vbo: WebGLBuffer;
  readonly texture: WebGLTexture;
  readonly uSource: WebGLUniformLocation | null;
  readonly uOffset: WebGLUniformLocation | null;
};

const rgbShiftSchema = {
  amount: {
    type: 'number',
    min: 0,
    max: 80,
    step: 1,
    default: 12,
    description: 'Amount',
  },
} as const satisfies InteractivitySchema;

export const rgbShift = createEffect<RgbShiftParams, RgbShiftState>({
  type: 'com.example.rgbShift',
  label: 'rgbShift()',
  documentationLink: null,
  backend: 'webgl2',
  calculateKey: ({amount = 12}) => `rgb-shift-${amount}`,
  setup: (target) => {
    const gl = target.getContext('webgl2', {
      premultipliedAlpha: true,
      alpha: true,
      preserveDrawingBuffer: true,
    });
    if (!gl) {
      throw new Error('Could not get a WebGL2 context for rgbShift().');
    }

    gl.pixelStorei(gl.UNPACK_PREMULTIPLY_ALPHA_WEBGL, true);

    // Compile/link shaders, create a fullscreen quad VAO/VBO, create a
    // CLAMP_TO_EDGE RGBA texture, and get uSource/uOffset uniform locations.
    return createRgbShiftState(gl);
  },
  apply: ({source, width, height, params, state, flipSourceY}) => {
    const amount = params.amount ?? 12;
    const {gl} = state;

    gl.viewport(0, 0, width, height);
    gl.pixelStorei(gl.UNPACK_FLIP_Y_WEBGL, flipSourceY);
    gl.activeTexture(gl.TEXTURE0);
    gl.bindTexture(gl.TEXTURE_2D, state.texture);
    gl.texImage2D(
      gl.TEXTURE_2D,
      0,
      gl.RGBA,
      gl.RGBA,
      gl.UNSIGNED_BYTE,
      source as TexImageSource,
    );

    gl.bindFramebuffer(gl.FRAMEBUFFER, null);
    gl.useProgram(state.program);
    if (state.uSource) gl.uniform1i(state.uSource, 0);
    if (state.uOffset) gl.uniform2f(state.uOffset, amount / width, 0);
    gl.bindVertexArray(state.vao);
    gl.drawArrays(gl.TRIANGLE_STRIP, 0, 4);
  },
  cleanup: ({gl, program, vao, vbo, texture}) => {
    gl.deleteTexture(texture);
    gl.deleteBuffer(vbo);
    gl.deleteProgram(program);
    gl.deleteVertexArray(vao);
  },
  schema: rgbShiftSchema,
  validateParams: ({amount = 12}) => {
    if (typeof amount !== 'number' || !Number.isFinite(amount) || amount < 0 || amount > 80) {
      throw new TypeError('amount must be a number between 0 and 80');
    }
  },
});
```

For a complete 2D and WebGL2 pair, see `packages/example/src/EffectsTestbed/sample-posterize-2d.ts` and `packages/example/src/EffectsTestbed/sample-rgb-shift-webgl.ts`.

Use the returned factory in an `effects` array:

```tsx
import {CanvasImage, staticFile} from 'remotion';
import {myEffect} from './effects/my-effect';

export const MyComp: React.FC = () => {
  return (
    <CanvasImage
      src={staticFile('image.png')}
      effects={[myEffect({amount: 0.8})]}
    />
  );
};
```

When generating a custom effect, also:

- Include `disabled?: boolean` only through the returned factory; do not add it to the custom params type or schema.
- Validate required parameters at factory-call time with `validateParams`.
- Include all defaults in both `schema` and the `resolve()` helper.
- Reset mutable 2D context state such as `filter`, `globalAlpha`, transforms, and compositing after drawing.
- Preserve alpha unless the requested effect intentionally changes transparency.


<!-- ===== FILE: remotion/remotion-markup/embedding-videos.md ===== -->

---
name: embedding-videos
description: Embedding videos in Remotion - trimming, volume, speed, looping, pitch
metadata:
  tags: video, media, trim, volume, speed, loop, pitch
---

# Using videos in Remotion

## Prerequisites

First, the @remotion/media package needs to be installed.  
If it is not, use the following command:

```bash
npx remotion add @remotion/media # If project uses npm
bunx remotion add @remotion/media # If project uses bun
yarn remotion add @remotion/media # If project uses yarn
pnpm exec remotion add @remotion/media # If project uses pnpm
```

Use `<Video>` from `@remotion/media` to embed videos into your composition.

```tsx
import { Video } from "@remotion/media";
import { staticFile } from "remotion";

export const MyComposition = () => {
  return <Video src={staticFile("video.mp4")} />;
};
```

Remote URLs are also supported:

```tsx
<Video src="https://remotion.media/video.mp4" />
```

## Trimming

Use `trimBefore` to skip the beginning of the video and `durationInFrames` to end it early. Values are in frames.

```tsx
const { fps } = useVideoConfig();

return (
  <Video
    src={staticFile("video.mp4")}
    trimBefore={2 * fps} // Skip the first 2 seconds
    durationInFrames={8 * fps} // Play 8 seconds, until the 10 second mark
  />
);
```

## Delaying

Set `from` directly on `<Video>` to delay when it appears:

```tsx
import { staticFile, useVideoConfig } from "remotion";
import { Video } from "@remotion/media";

const { fps } = useVideoConfig();

return (
  <Video from={fps} src={staticFile("video.mp4")} />
);
```

The video will appear after 1 second.

## Sizing and Position

Use the `style` prop to control size and position:

```tsx
<Video
  src={staticFile("video.mp4")}
  style={{
    width: 500,
    height: 300,
    position: "absolute",
    top: 100,
    left: 50,
  }}
  objectFit="cover"
/>
```

## Volume

Set a static volume (0 to 1):

```tsx
<Video src={staticFile("video.mp4")} volume={0.5} />
```

Use `useCurrentFrame()` and `interpolate()` for keyframed volume:

```tsx
import { Video } from "@remotion/media";
import { interpolate, staticFile, useCurrentFrame, useVideoConfig } from "remotion";

const frame = useCurrentFrame();
const { fps } = useVideoConfig();

return (
  <Video
    src={staticFile("video.mp4")}
    volume={interpolate(frame, [0, 1 * fps], [0, 1], {
      extrapolateLeft: "clamp",
      extrapolateRight: "clamp",
    })}
  />
);
```

With Studio interactivity enabled, these keyframes can be edited and are shown as a volume curve in the timeline.

Use `muted` to silence the video entirely:

```tsx
<Video src={staticFile("video.mp4")} muted />
```

## Speed

Use `playbackRate` to change the playback speed:

```tsx
// 2x speed
<Video src={staticFile("video.mp4")} playbackRate={2} />
// Half speed
<Video src={staticFile("video.mp4")} playbackRate={0.5} />
```

Reverse playback is not supported.

## Looping

Use `loop` to loop the video indefinitely:

```tsx
<Video src={staticFile("video.mp4")} loop />
```

```tsx
import { Video } from "@remotion/media";
import { interpolate, staticFile, useCurrentFrame } from "remotion";

const frame = useCurrentFrame();

<Video
  src={staticFile("video.mp4")}
  loop
  volume={interpolate(frame, [0, 300], [1, 0], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
  })}
/>
```

## Pitch

Use `toneFrequency` to adjust the pitch without affecting speed. Values range from 0.01 to 2:

```tsx
<Video
  src={staticFile("video.mp4")}
  toneFrequency={1.5} // Higher pitch
/>
<Video
  src={staticFile("video.mp4")}
  toneFrequency={0.8} // Lower pitch
/>
```

Pitch shifting only works during server-side rendering, not in the Remotion Studio preview or in the `<Player />`.


<!-- ===== FILE: remotion/remotion-markup/ffmpeg.md ===== -->

---
name: ffmpeg
description: Using FFmpeg and FFprobe in Remotion
metadata:
  tags: ffmpeg, ffprobe, video, trimming
---

## FFmpeg in Remotion

`ffmpeg` and `ffprobe` do not need to be installed. They are available via the `npx remotion ffmpeg` and `npx remotion ffprobe`:

```bash
npx remotion ffmpeg -i input.mp4 output.mp3
npx remotion ffprobe input.mp4
```

### Trimming videos

You have 2 options for trimming videos:

1. **Preferred**: Use the `trimBefore` and `durationInFrames` props of the `<Video>` component. This is non-destructive, requires no re-encoding, and you can change the trim at any time.

```tsx
import {Video} from '@remotion/media';

<Video
  src={staticFile('video.mp4')}
  trimBefore={5 * fps}
  durationInFrames={5 * fps}
/>;
```

2. Use the FFmpeg command line. You MUST re-encode the video to avoid frozen frames at the start of the video. Only use this if you need a standalone trimmed file (e.g. for upload or external use).

```bash
# Re-encodes from the exact frame
npx remotion ffmpeg -ss 00:00:05 -i public/input.mp4 -to 00:00:10 -c:v libx264 -c:a aac public/output.mp4
```


<!-- ===== FILE: remotion/remotion-markup/gifs.md ===== -->

---
name: gif
description: Displaying GIFs, APNG, AVIF and WebP in Remotion
metadata:
  tags: gif, animation, images, animated, apng, avif, webp
---

# Using Animated images in Remotion

## Basic usage

Use `<AnimatedImage>` to display a GIF, APNG, AVIF or WebP image synchronized with Remotion's timeline:

```tsx
import { AnimatedImage, staticFile } from "remotion";

export const MyComposition = () => {
  return (
    <AnimatedImage
      src={staticFile("animation.gif")}
      width={500}
      height={500}
    />
  );
};
```

Remote URLs are also supported (must have CORS enabled):

```tsx
<AnimatedImage
  src="https://example.com/animation.gif"
  width={500}
  height={500}
/>
```

## Sizing and fit

Control how the image fills its container with the `fit` prop:

```tsx
// Stretch to fill (default)
<AnimatedImage
  src={staticFile("animation.gif")}
  width={500}
  height={300}
  fit="fill"
/>

// Maintain aspect ratio, fit inside container
<AnimatedImage
  src={staticFile("animation.gif")}
  width={500}
  height={300}
  fit="contain"
/>

// Fill container, crop if needed
<AnimatedImage
  src={staticFile("animation.gif")}
  width={500}
  height={300}
  fit="cover"
/>
```

## Playback speed

Use `playbackRate` to control the animation speed:

```tsx
// 2x speed
<AnimatedImage
  src={staticFile("animation.gif")}
  width={500}
  height={500}
  playbackRate={2}
/>
// Half speed
<AnimatedImage
  src={staticFile("animation.gif")}
  width={500}
  height={500}
  playbackRate={0.5}
/>
```

## Looping behavior

Control what happens when the animation finishes:

```tsx
// Loop indefinitely (default)
<AnimatedImage
  src={staticFile("animation.gif")}
  width={500}
  height={500}
  loopBehavior="loop"
/>

// Play once, show final frame
<AnimatedImage
  src={staticFile("animation.gif")}
  width={500}
  height={500}
  loopBehavior="pause-after-finish"
/>

// Play once, then clear canvas
<AnimatedImage
  src={staticFile("animation.gif")}
  width={500}
  height={500}
  loopBehavior="clear-after-finish"
/>
```

## Styling

Use the `style` prop for additional CSS (use `width` and `height` props for sizing):

```tsx
<AnimatedImage
  src={staticFile("animation.gif")}
  width={500}
  height={500}
  style={{
    borderRadius: 20,
    position: "absolute",
    top: 100,
    left: 50,
  }}
/>
```

## Getting GIF duration

Use `getGifDurationInSeconds()` from `@remotion/gif` to get the duration of a GIF.

```bash
npx remotion add @remotion/gif
```

```tsx
import { getGifDurationInSeconds } from "@remotion/gif";
import { staticFile } from "remotion";

const duration = await getGifDurationInSeconds(staticFile("animation.gif"));
console.log(duration); // e.g. 2.5
```

This is useful for setting the composition duration to match the GIF:

```tsx
import { getGifDurationInSeconds } from "@remotion/gif";
import { staticFile, CalculateMetadataFunction } from "remotion";

const calculateMetadata: CalculateMetadataFunction = async () => {
  const duration = await getGifDurationInSeconds(staticFile("animation.gif"));
  return {
    durationInFrames: Math.ceil(duration * 30),
  };
};
```

## Alternative

If `<AnimatedImage>` does not work (only supported in Chrome and Firefox), you can use `<Gif>` from `@remotion/gif` instead.

```bash
npx remotion add @remotion/gif # If project uses npm
bunx remotion add @remotion/gif # If project uses bun
yarn remotion add @remotion/gif # If project uses yarn
pnpm exec remotion add @remotion/gif # If project uses pnpm
```

```tsx
import { Gif } from "@remotion/gif";
import { staticFile } from "remotion";

export const MyComposition = () => {
  return <Gif src={staticFile("animation.gif")} width={500} height={500} />;
};
```

The `<Gif>` component has the same props as `<AnimatedImage>` but only supports GIF files.


<!-- ===== FILE: remotion/remotion-markup/google-fonts.md ===== -->

---
name: fonts
description: Loading Google Fonts and local fonts in Remotion
metadata:
  tags: fonts, google-fonts, typography, text
---

# Using fonts in Remotion

## Google Fonts with @remotion/google-fonts

The recommended way to use Google Fonts. It's type-safe and automatically blocks rendering until the font is ready.

### Prerequisites

First, the @remotion/google-fonts package needs to be installed.
If it is not installed, use the following command:

```bash
npx remotion add @remotion/google-fonts # If project uses npm
bunx remotion add @remotion/google-fonts # If project uses bun
yarn remotion add @remotion/google-fonts # If project uses yarn
pnpm exec remotion add @remotion/google-fonts # If project uses pnpm
```

```tsx
import { loadFont } from "@remotion/google-fonts/Lobster";

const { fontFamily } = loadFont();

export const MyComposition = () => {
  return (
    <div style={{ fontFamily }}>
      Hello World
    </div>
  );
};
```

Preferrably, specify only needed weights and subsets to reduce file size:

```tsx
import { loadFont } from "@remotion/google-fonts/Roboto";

const { fontFamily } = loadFont("normal", {
  weights: ["400", "700"],
  subsets: ["latin"],
});
```

## Using in components

Call `loadFont()` at the top level of your component or in a separate file that's imported early:

```tsx
import { loadFont } from "@remotion/google-fonts/Montserrat";

const { fontFamily } = loadFont("normal", {
  weights: ["400", "700"],
  subsets: ["latin"],
});

export const Title: React.FC<{ text: string }> = ({ text }) => {
  return (
    <h1
      style={{
        fontFamily,
        fontSize: 80,
        fontWeight: "bold",
      }}
    >
      {text}
    </h1>
  );
};
```


<!-- ===== FILE: remotion/remotion-markup/html-in-canvas.md ===== -->

# Using `<HtmlInCanvas>` in Remotion

Renders children into a `<canvas>` so you can post-process them with the Canvas 2D API or WebGL.

Only works in Chrome 149+ with the `chrome://flags/#canvas-draw-element` flag enabled.  
Give the user a notice.

## Nesting

Nest `<HtmlInCanvas>` components only when `HtmlInCanvas.isNestingSupported()` returns `true` (Chrome 157.0.8080.0 or newer with HTML-in-canvas enabled). Older browsers reject nesting.

## Enabling WebGL during renders

If you make use of WebGL during renders, you need to enable it:

From the CLI:

```bash
npx remotion render --gl=angle
```

Set it as the default for Studio and CLI (advised):

```ts
import { Config } from "@remotion/cli/config";

Config.setChromiumOpenGlRenderer("angle");
```

## Basic usage

By default, draws to canvas with no effect applied:

```tsx
import { HtmlInCanvas } from "remotion";

export const MyComp = () => {
  return (
    <HtmlInCanvas width={1280} height={720}>
      <div style={{ fontSize: 80 }}>
        Hello
      </div>
    </HtmlInCanvas>
  );
};
```

## 2D effect with `onPaint`

`onPaint` runs whenever the content updates. Call `ctx.drawElementImage(elementImage, 0, 0)` to draw the captured DOM.

```tsx
import {
  AbsoluteFill,
  HtmlInCanvas,
  type HtmlInCanvasOnPaint,
  useCurrentFrame,
  useVideoConfig,
} from "remotion";
import { useCallback } from "react";

export const Blur = () => {
  const frame = useCurrentFrame();
  const { width, height, fps } = useVideoConfig();

  const onPaint: HtmlInCanvasOnPaint = useCallback(
    ({ canvas, elementImage }) => {
      const ctx = canvas.getContext("2d");
      if (!ctx) throw new Error("Failed to acquire 2D context");

      const blurPx = 4 + 18 * (0.5 + 0.5 * Math.sin((frame / fps) * Math.PI));

      ctx.reset();
      ctx.filter = `blur(${blurPx}px)`;
      ctx.drawElementImage(elementImage, 0, 0);
    },
    [frame, fps],
  );

  return (
    <HtmlInCanvas width={width} height={height} onPaint={onPaint}>
      <AbsoluteFill
        style={{
          justifyContent: "center",
          alignItems: "center",
          fontSize: 120,
        }}
      >
        <h1>
          Hello
        </h1>
      </AbsoluteFill>
    </HtmlInCanvas>
  );
};
```

## WebGL effects

For WebGL, set up the context, program, and texture in `onInit` and return a cleanup function. Allocate the texture with `gl.texImage2D(..., null)` when `elementImage` changes size. Inside `onPaint`, upload with `gl.texElementSubImage2D(gl.TEXTURE_2D, 0, 0, 0, elementImage)` and draw. Older Chromium versions only expose `gl.texElementImage2D()`; use it when the new method is absent.

For a fully working minimal example, see https://github.com/remotion-dev/remotion/blob/main/packages/docs/components/demos/HtmlInCanvasDocsDemoWebGL.tsx.

## Async `onPaint`

`onPaint` may be `async`. Remotion holds the frame open via `delayRender()` until the promise resolves. Useful for multi-pass effects with `createImageBitmap`.


<!-- ===== FILE: remotion/remotion-markup/images.md ===== -->

## Sizing and positioning

Use the `style` prop to control size and position:

```tsx
<Img
  src={staticFile("photo.png")}
  style={{
    width: 500,
    height: 300,
    position: "absolute",
    top: 100,
    left: 50,
    objectFit: "cover",
  }}
/>
```

## Dynamic image paths

Use template literals for dynamic file references:

```tsx
import { Img, staticFile, useCurrentFrame } from "remotion";

const frame = useCurrentFrame();

// Image sequence
<Img src={staticFile(`frames/frame${frame}.png`)} />

// Selecting based on props
<Img src={staticFile(`avatars/${props.userId}.png`)} />

// Conditional images
<Img
  src={staticFile(`icons/${isActive ? "active" : "inactive"}.svg`)}
/>
```

This pattern is useful for:

- Image sequences (frame-by-frame animations)
- User-specific avatars or profile images
- Theme-based icons
- State-dependent graphics

## Getting image dimensions

Use `getImageDimensions()` from `@remotion/media-utils` to get the dimensions of an image:

```tsx
import { getImageDimensions } from "@remotion/media-utils";
import { staticFile } from "remotion";

const { width, height } = await getImageDimensions(staticFile("photo.png"));
```

This is useful for calculating aspect ratios or sizing compositions:

```tsx
import { getImageDimensions } from "@remotion/media-utils";
import { staticFile, CalculateMetadataFunction } from "remotion";

const calculateMetadata: CalculateMetadataFunction = async () => {
  const { width, height } = await getImageDimensions(staticFile("photo.png"));
  return {
    width,
    height,
  };
};
```


<!-- ===== FILE: remotion/remotion-markup/light-leaks.md ===== -->

---
name: light-leaks
description: Light leak overlay effects for Remotion using lightLeak() from @remotion/effects.
metadata:
  tags: light-leaks, overlays, effects, transitions
---

## Light Leaks

This only works from Remotion 4.0.500 and up. Use `npx remotion versions` to check your Remotion version and `npx remotion upgrade` to upgrade your Remotion version.

Apply `lightLeak()` from `@remotion/effects/light-leak` to a canvas-based component such as `<Solid>`. Animate `progress` from `0` to `1`; the light leak reveals during the first half and retracts during the second half.

Typically use it inside a `<TransitionSeries.Overlay>` to play over the cut point between two scenes. See the **transitions** rule for `<TransitionSeries>` and overlay usage.

## Prerequisites

```bash
npx remotion add @remotion/effects
```

## Light leak overlay component

Keep the `progress` calculation inline so it is editable in Remotion Studio:

```tsx
import {lightLeak} from '@remotion/effects/light-leak';
import {interpolate, Solid, useCurrentFrame, useVideoConfig} from 'remotion';

const LightLeakOverlay: React.FC<{
  seed?: number;
  hueShift?: number;
}> = ({seed = 0, hueShift = 0}) => {
  const frame = useCurrentFrame();
  const {durationInFrames, height, width} = useVideoConfig();

  return (
    <Solid
      width={width}
      height={height}
      effects={[
        lightLeak({
          seed,
          hueShift,
          progress: interpolate(frame, [0, durationInFrames - 1], [0, 1], {
            extrapolateLeft: 'clamp',
            extrapolateRight: 'clamp',
          }),
        }),
      ]}
    />
  );
};
```

## Basic usage with TransitionSeries

```tsx
import {TransitionSeries} from '@remotion/transitions';

<TransitionSeries>
  <TransitionSeries.Sequence durationInFrames={60}>
    <SceneA />
  </TransitionSeries.Sequence>
  <TransitionSeries.Overlay durationInFrames={30}>
    <LightLeakOverlay />
  </TransitionSeries.Overlay>
  <TransitionSeries.Sequence durationInFrames={60}>
    <SceneB />
  </TransitionSeries.Sequence>
</TransitionSeries>;
```

## Options

- `progress?` — controls the evolve/retract phase from `0` to `1`. Effects do not animate on their own, so drive it with `useCurrentFrame()` and `interpolate()`. Default: `0.5`.
- `seed?` — determines the shape of the light leak pattern. Different seeds produce different patterns. Default: `0`.
- `hueShift?` — rotates the hue in degrees (`0`–`360`). Default: `0` (yellow-to-orange). `120` = green, `240` = blue.
- `disabled?` — skips the effect when `true`. Default: `false`.

## Customizing the look

```tsx
// Blue-tinted light leak with a different pattern
<LightLeakOverlay seed={5} hueShift={240} />;

// Green-tinted light leak
<LightLeakOverlay seed={2} hueShift={120} />;
```

## Standalone usage

The overlay component can also be used outside of `<TransitionSeries>` as a decorative layer in any composition:

```tsx
const MyComp: React.FC = () => (
  <>
    <MyContent />
    <LightLeakOverlay seed={3} />
  </>
);
```

`lightLeak()` uses WebGL2. Enable WebGL during rendering with `Config.setChromiumOpenGlRenderer("angle")`.


<!-- ===== FILE: remotion/remotion-markup/local-fonts.md ===== -->

For local font files, use the `@remotion/fonts` package.

### Prerequisites

First, install @remotion/fonts:

```bash
npx remotion add @remotion/fonts # If project uses npm
bunx remotion add @remotion/fonts # If project uses bun
yarn remotion add @remotion/fonts # If project uses yarn
pnpm exec remotion add @remotion/fonts # If project uses pnpm
```

### Loading a local font

Place your font file in the `public/` folder and use `loadFont()`:

```tsx
import { loadFont } from "@remotion/fonts";
import { staticFile } from "remotion";

await loadFont({
  family: "MyFont",
  url: staticFile("MyFont-Regular.woff2"),
});

export const MyComposition = () => {
  return (
    <div style={{ fontFamily: "MyFont" }}>
      Hello World
    </div>
  );
};
```

### Loading multiple weights

Load each weight separately with the same family name:

```tsx
import { loadFont } from "@remotion/fonts";
import { staticFile } from "remotion";

await Promise.all([
  loadFont({
    family: "Inter",
    url: staticFile("Inter-Regular.woff2"),
    weight: "400",
  }),
  loadFont({
    family: "Inter",
    url: staticFile("Inter-Bold.woff2"),
    weight: "700",
  }),
]);
```

### Available options

```tsx
loadFont({
  family: "MyFont", // Required: name to use in CSS
  url: staticFile("font.woff2"), // Required: font file URL
  format: "woff2", // Optional: auto-detected from extension
  weight: "400", // Optional: font weight
  style: "normal", // Optional: normal or italic
  display: "block", // Optional: font-display behavior
});
```


<!-- ===== FILE: remotion/remotion-markup/lottie.md ===== -->

---
name: lottie
description: Embedding Lottie animations in Remotion.
metadata:
  category: Animation
---

# Using Lottie Animations in Remotion

## Prerequisites

First, the @remotion/lottie package needs to be installed.  
If it is not, use the following command:

```bash
npx remotion add @remotion/lottie # If project uses npm
bunx remotion add @remotion/lottie # If project uses bun
yarn remotion add @remotion/lottie # If project uses yarn
pnpm exec remotion add @remotion/lottie # If project uses pnpm
```

## Displaying a Lottie file

To import a Lottie animation:

- Fetch the Lottie asset
- Wrap the loading process in `delayRender()` and `continueRender()`
- Save the animation data in a state
- Render the Lottie animation using the `Lottie` component from the `@remotion/lottie` package

```tsx
import { Lottie, LottieAnimationData } from "@remotion/lottie";
import { useEffect, useState } from "react";
import { cancelRender, continueRender, delayRender } from "remotion";

export const MyAnimation = () => {
  const [handle] = useState(() => delayRender("Loading Lottie animation"));

  const [animationData, setAnimationData] =
    useState<LottieAnimationData | null>(null);

  useEffect(() => {
    fetch("https://assets4.lottiefiles.com/packages/lf20_zyquagfl.json")
      .then((data) => data.json())
      .then((json) => {
        setAnimationData(json);
        continueRender(handle);
      })
      .catch((err) => {
        cancelRender(err);
      });
  }, [handle]);

  if (!animationData) {
    return null;
  }

  return <Lottie animationData={animationData} />;
};
```

## Styling and animating

Lottie supports the `style` prop to allow styles and animations:

```tsx
return (
  <Lottie
    animationData={animationData}
    style={{ width: 400, height: 400 }}
  />
);
```


<!-- ===== FILE: remotion/remotion-markup/measuring-dom-nodes.md ===== -->

---
name: measuring-dom-nodes
description: Measuring DOM element dimensions in Remotion
metadata:
  tags: measure, layout, dimensions, getBoundingClientRect, scale
---

# Measuring DOM nodes in Remotion

Remotion applies a `scale()` transform to the video container, which affects values from `getBoundingClientRect()`. Use `useCurrentScale()` to get correct measurements.

## Measuring element dimensions

```tsx
import { useCurrentScale } from "remotion";
import { useRef, useEffect, useState } from "react";

export const MyComponent = () => {
  const ref = useRef<HTMLDivElement>(null);
  const scale = useCurrentScale();
  const [dimensions, setDimensions] = useState({ width: 0, height: 0 });

  useEffect(() => {
    if (!ref.current) return;
    const rect = ref.current.getBoundingClientRect();
    setDimensions({
      width: rect.width / scale,
      height: rect.height / scale,
    });
  }, [scale]);

  return (
    <div ref={ref}>
      Content to measure
    </div>
  );
};
```


<!-- ===== FILE: remotion/remotion-markup/measuring-text.md ===== -->

---
name: measuring-text
description: Measuring text dimensions, fitting text to containers, and checking overflow
metadata:
  tags: measure, text, layout, dimensions, fitText, fillTextBox
---

# Measuring text in Remotion

## Prerequisites

Install @remotion/layout-utils if it is not already installed:

```bash
npx remotion add @remotion/layout-utils
```

## Measuring text dimensions

Use `measureText()` to calculate the width and height of text:

```tsx
import { measureText } from "@remotion/layout-utils";

const { width, height } = measureText({
  text: "Hello World",
  fontFamily: "Arial",
  fontSize: 32,
  fontWeight: "bold",
});
```

Results are cached - duplicate calls return the cached result.

## Fitting text to a width

Use `fitText()` to find the optimal font size for a container:

```tsx
import { fitText } from "@remotion/layout-utils";

const { fontSize } = fitText({
  text: "Hello World",
  withinWidth: 600,
  fontFamily: "Inter",
  fontWeight: "bold",
});

return (
  <div
    style={{
      fontSize: Math.min(fontSize, 80), // Cap at 80px
      fontFamily: "Inter",
      fontWeight: "bold",
    }}
  >
    Hello World
  </div>
);
```

## Checking text overflow

Use `fillTextBox()` to check if text exceeds a box:

```tsx
import { fillTextBox } from "@remotion/layout-utils";

const box = fillTextBox({ maxBoxWidth: 400, maxLines: 3 });

const words = ["Hello", "World", "This", "is", "a", "test"];
for (const word of words) {
  const { exceedsBox } = box.add({
    text: word + " ",
    fontFamily: "Arial",
    fontSize: 24,
  });
  if (exceedsBox) {
    // Text would overflow, handle accordingly
    break;
  }
}
```

## Best practices

**Load fonts first:** Only call measurement functions after fonts are loaded.

```tsx
import { loadFont } from "@remotion/google-fonts/Inter";

const { fontFamily, waitUntilDone } = loadFont("normal", {
  weights: ["400"],
  subsets: ["latin"],
});

waitUntilDone().then(() => {
  // Now safe to measure
  const { width } = measureText({
    text: "Hello",
    fontFamily,
    fontSize: 32,
  });
});
```

**Use validateFontIsLoaded:** Catch font loading issues early:

```tsx
measureText({
  text: "Hello",
  fontFamily: "MyCustomFont",
  fontSize: 32,
  validateFontIsLoaded: true, // Throws if font not loaded
});
```

**Match font properties:** Use the same properties for measurement and rendering:

```tsx
const fontStyle = {
  fontFamily: "Inter",
  fontSize: 32,
  fontWeight: "bold" as const,
  letterSpacing: "0.5px",
};

const { width } = measureText({
  text: "Hello",
  ...fontStyle,
});

return (
  <div style={fontStyle}>
    Hello
  </div>
);
```

**Avoid padding and border:** Use `outline` instead of `border` to prevent layout differences:

```tsx
<div style={{ outline: "2px solid red" }}>
  Text
</div>
```


<!-- ===== FILE: remotion/remotion-markup/motion-blur.md ===== -->

# Motion blur

Use `@remotion/motion-blur` for frame-driven motion blur.  
Install it with `npx remotion add @remotion/motion-blur`.

`<HtmlInCanvasMotionBlur>` is the state of the art in Remotion for blurring animated HTML. It captures the content at fractional frames and averages its pixels in a canvas.

## `<HtmlInCanvasMotionBlur>`

Available from Remotion 4.0.529.  
Supply the canvas `width` and `height`, usually from `useVideoConfig()`.  
`shutterAngle` defaults to `180` and accepts `0` to `360`.
`0` disables blur. `samples` defaults to `8` and must be an integer from `1` to `64`. More samples can smooth the blur but increase preview and render cost.

Call `useCurrentFrame()` inside the child component so each sample receives its own frame.

```tsx
import {
  HtmlInCanvasMotionBlur,
} from '@remotion/motion-blur';
import {useCurrentFrame, useVideoConfig} from 'remotion';

const MovingBox = () => {
  const frame = useCurrentFrame();
  return (
    <div
      style={{
        position: 'absolute',
        left: frame * 10,
        top: 200,
        width: 120,
        height: 120,
        backgroundColor: '#ff6b6b',
      }}
    />
  );
};

export const HtmlInCanvasBlur = () => {
  const {width, height} = useVideoConfig();

  return (
    <HtmlInCanvasMotionBlur
      width={width}
      height={height}
      samples={8}
      shutterAngle={180}
    >
      <MovingBox />
    </HtmlInCanvasMotionBlur>
  );
};
```

For live preview, enable HTML-in-canvas in Chrome 149 or later with `chrome://flags/#canvas-draw-element`.  
No configuration for rendering is necessary.

Nest `<HtmlInCanvas>` or `<HtmlInCanvasMotionBlur>` components only when `HtmlInCanvas.isNestingSupported()` returns `true` (Chrome 157.0.8080.0 or newer with HTML-in-canvas enabled).

If HTML-in-canvas is unavailable, see the [motion blur guide](https://www.remotion.dev/docs/motion-blur) for other options. See the [`<HtmlInCanvasMotionBlur>` reference](https://www.remotion.dev/docs/motion-blur/html-in-canvas-motion-blur) for API details.


<!-- ===== FILE: remotion/remotion-markup/multi-scene-video.md ===== -->

# Multi-scene videos

Put successive scenes in a named `Track`. Make each scene with
`Interactive.create({layout: 'absolute-fill'})` and register it as a connected
composition. Write each instance separately with inline timing and props.

```tsx title="MyVideo.tsx"
import {Track, useVideoConfig} from 'remotion';
import {OpeningScene} from './OpeningScene';
import {FeatureScene} from './FeatureScene';

export const MyVideo = () => {
  const {fps} = useVideoConfig();

  return (
    <Track name="Scenes">
      <OpeningScene name="Opening" durationInFrames={3 * fps} />
      <FeatureScene name="Feature" from={3 * fps} durationInFrames={4 * fps} />
    </Track>
  );
};
```

Follow the complete [Track + connected compositions example](../remotion-interactivity/timeline-structure.md)
for scene definitions and `Root.tsx`. Register `OpeningScene`, `FeatureScene`,
and `MyVideo` using those same exported component references, with representative
inline defaults. At 30 fps, this parent lasts 210 frames.

When adding overlapping transitions, use
[`TransitionSeries`](transitions.md) instead of `Track`. Keep each scene as the
only child of its `TransitionSeries.Sequence`, and subtract transition overlaps
from the parent duration.


<!-- ===== FILE: remotion/remotion-markup/parameters.md ===== -->

---
name: parameters
description: Make a video parametrizable by adding a Zod schema
metadata:
  tags: parameters, zod, schema
---

To make a video parametrizable, a Zod schema can be added to a composition.

First, `zod` must be installed .

Search the project for lockfiles and run the correct command depending on the package manager:

If `package-lock.json` is found, use the following command:

```bash
npm i zod
```

If `bun.lockb` is found, use the following command:

```bash
bun i zod
```

If `yarn.lock` is found, use the following command:

```bash
yarn add zod
```

If `pnpm-lock.yaml` is found, use the following command:

```bash
pnpm i zod
```

Then, a Zod schema can be defined alongside the component:

```tsx title="src/MyComposition.tsx"
import { z } from "zod";

export const MyCompositionSchema = z.object({
  title: z.string(),
});

const MyComponent: React.FC<z.infer<typeof MyCompositionSchema>> = () => {
  return (
    <div>
      <h1>
        {props.title}
      </h1>
    </div>
  );
};
```

In the root file, the schema can be passed to the composition:

```tsx title="src/Root.tsx"
import { Composition } from "remotion";
import { MycComponent, MyCompositionSchema } from "./MyComposition";

export const RemotionRoot = () => {
  return (
    <Composition
      id="MyComposition"
      component={MyComponent}
      durationInFrames={100}
      fps={30}
      width={1080}
      height={1080}
      defaultProps={{ title: "Hello World" }}
      schema={MyCompositionSchema}
    />
  );
};
```

Now, the user can edit the parameter visually in the sidebar.

All schemas that are supported by Zod are supported by Remotion.

Remotion requires that the top-level type is a z.object(), because the collection of props of a React component is always an object.

## Color picker

For adding a color picker, use `zColor()` from `@remotion/zod-types`.

If it is not installed, use the following command:

```bash
npx remotion add @remotion/zod-types # If project uses npm
bunx remotion add @remotion/zod-types # If project uses bun
yarn remotion add @remotion/zod-types # If project uses yarn
pnpm exec remotion add @remotion/zod-types # If project uses pnpm
```

Then import `zColor` from `@remotion/zod-types`:

```tsx
import { zColor } from "@remotion/zod-types";
```

Then use it in the schema:

```tsx
export const MyCompositionSchema = z.object({
  color: zColor(),
});
```


<!-- ===== FILE: remotion/remotion-markup/sequencing.md ===== -->

---
name: sequencing
description: Sequencing patterns for Remotion - delay, trim, limit duration of items
metadata:
  tags: sequence, series, timing, delay, trim
---

Prefer timing props directly on built-in interactive components and custom
components made with `Interactive.create()`.  
Avoid wrapping a single timing-capable component in a redundant `<Sequence>`.
Put `name`, `from`, `durationInFrames`, `loop`, and `volume`
directly on `<Audio>` from `@remotion/media` whenever their combination gives the intended timing.

See [Remotion Interactivity](../remotion-interactivity/REFERENCE.md) for creating
schema-wrapped components and [connected compositions](connected-compositions.md)
for registering them with their own Studio timelines.

```tsx
// Title and Subtitle are exported with Interactive.create().
<>
  <Title name="Title" from={30} durationInFrames={60} />
  <Subtitle name="Subtitle" from={60} durationInFrames={60} />
</>
```

Use an explicit `<Sequence>` when multiple siblings need one shared clock,
when overriding dimensions for descendants, or when the child does not accept
timing props. Its default layout adds an absolutely positioned fill element;
use `layout="none"` when no layout wrapper is needed.

## TransitionSeries

Use `<TransitionSeries>` for consecutive scenes, with or without transitions. Without a transition, the scenes play without overlap.

```tsx
import { TransitionSeries } from "@remotion/transitions";

<TransitionSeries>
  <TransitionSeries.Sequence durationInFrames={45}>
    <Intro />
  </TransitionSeries.Sequence>
  <TransitionSeries.Sequence durationInFrames={60}>
    <MainContent />
  </TransitionSeries.Sequence>
  <TransitionSeries.Sequence durationInFrames={30}>
    <Outro />
  </TransitionSeries.Sequence>
</TransitionSeries>;
```

The items will be wrapped in an absolute fill element by default when using `<TransitionSeries.Sequence>`, unless the `layout` prop is set to `none`.
