#!/usr/bin/env bash
# Compare independently decoded frames at matching timestamps, not split streams.
# Usage: frame_strip.sh baseline.mp4 translated.mp4 [output-dir] [samples]
set -euo pipefail
if [[ $# -lt 2 || $# -gt 4 ]]; then
  echo "usage: $0 baseline.mp4 translated.mp4 [output-dir] [samples]" >&2
  exit 2
fi
python3 - "$1" "$2" "${3:-./strip-out}" "${4:-8}" <<'PY'
import json
import math
import subprocess
import sys
import tempfile
from pathlib import Path
from PIL import Image

try:
    baseline, translated, raw_out, raw_samples = sys.argv[1:]
    samples = int(raw_samples)
    if samples <= 0:
        raise ValueError('samples must be a positive integer')
    outdir = Path(raw_out)
    def probe(path):
        if not Path(path).is_file():
            raise ValueError(f'video does not exist: {path}')
        data = json.loads(subprocess.run(
            ['ffprobe', '-v', 'error', '-select_streams', 'v:0',
             '-show_entries', 'stream=avg_frame_rate,duration:format=duration', '-of', 'json', path],
            check=True, capture_output=True, text=True).stdout)
        stream = data['streams'][0]
        num, den = map(float, stream['avg_frame_rate'].split('/'))
        fps = num / den
        duration = float(stream.get('duration') or data['format']['duration'])
        if not all(math.isfinite(v) and v > 0 for v in [fps, duration]):
            raise ValueError('video must have positive finite duration and frame rate')
        return fps, duration
    base_fps, base_duration = probe(baseline)
    translated_fps, translated_duration = probe(translated)
    fps = min(base_fps, translated_fps)
    count = max(1, int(min(base_duration, translated_duration) * fps))
    start = int(count * .05)
    end = max(start, int(count * .95) - 1)
    samples = min(samples, end - start + 1)
    frames = [start] if samples == 1 else [round(start + i * (end-start)/(samples-1)) for i in range(samples)]
    times = [f / fps for f in frames]
    outdir.mkdir(parents=True, exist_ok=True)
    rows = []
    with tempfile.TemporaryDirectory() as temp:
        for i, time in enumerate(times):
            pair = []
            for j, video in enumerate([baseline, translated]):
                dest = Path(temp) / f'{i}-{j}.png'
                subprocess.run(['ffmpeg', '-y', '-v', 'error', '-xerror', '-ss', str(time),
                                '-i', video, '-map', '0:v:0', '-frames:v', '1', str(dest)], check=True)
                with Image.open(dest) as image:
                    pair.append(image.convert('RGB'))
            if pair[0].size != pair[1].size:
                raise ValueError('videos must have matching frame dimensions')
            width, height = pair[0].size
            row = Image.new('RGB', (2*width, height))
            row.paste(pair[0], (0, 0)); row.paste(pair[1], (width, 0))
            rows.append(row)
    strip = Image.new('RGB', (rows[0].width, sum(row.height for row in rows)))
    for i, row in enumerate(rows):
        strip.paste(row, (0, i * row.height))
    strip.save(outdir / 'strip.png')
    (outdir / 'timestamps.txt').write_text('\n'.join(f'{t:.9f}' for t in times) + '\n')
    print(f'wrote {outdir / "strip.png"} ({samples} distinct timestamp samples; Pillow required)')
except (ValueError, OSError, KeyError, IndexError, ZeroDivisionError, subprocess.CalledProcessError) as exc:
    print(f'error: {exc}', file=sys.stderr)
    sys.exit(2)
PY
