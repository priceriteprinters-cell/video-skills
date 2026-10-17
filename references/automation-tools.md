# Automation Tools

## Prepare the helper

Copy `scripts/design_tools.py` and `assets/design-presets.json` together to a temporary working directory using the current skill file-access workflow. The script looks for `../assets/design-presets.json` relative to itself, or accepts global `--presets /path/design-presets.json`. It requires Python 3.10+ standard library only. Run `python3 design_tools.py --help` for current arguments. Outputs are working assets, not final videos.

```bash
python3 design_tools.py --presets /tmp/design-presets.json presets
python3 design_tools.py --presets /tmp/design-presets.json fonts --pairing modern --out /tmp/video-assets
python3 design_tools.py icon --provider simpleicons --name github --out /tmp/video-assets --license CC0 --license-url https://github.com/simple-icons/simple-icons/blob/develop/LICENSE.md --rights-reviewed --purpose "GitHub discussion scene"
python3 design_tools.py icon --provider iconify --name lucide:camera --out /tmp/video-assets --license ISC --license-url https://github.com/lucide-icons/lucide/blob/main/LICENSE --rights-reviewed --purpose "Camera diagram"
python3 design_tools.py fetch --url https://example.org/approved-photo.png --name product-photo.png --out /tmp/video-assets --license "Reviewed item license" --license-url https://example.org/terms --rights-reviewed --purpose "Product scene"
python3 design_tools.py --presets /tmp/design-presets.json validate --brief /tmp/brief.json
```

The example.org URLs above illustrate syntax only; substitute real inspected sources. Do not run placeholders. `--allow-host` adds a single reviewed hostname for downloads outside the built-in public asset hosts. The flag does not authorize access to private networks; all network destinations must resolve to public addresses, HTTPS redirects are revalidated, and IP-literal URLs/credentials/custom ports are rejected. URL queries may contain access tokens; do not use signed/private URLs or secrets. The script rejects common sensitive query names but cannot detect every secret. Use this local helper in a trusted sandbox, not as a public URL-fetching service; DNS validation is a safeguard, not a hardened proxy against DNS rebinding.

Downloads are size-limited (20 MiB by default, up to 100 MiB), do not overwrite existing files, and use a temporary partial file until completion. A per-output `asset-manifest.json` records URL, file, type, bytes, hash, license description and evidence URL, attribution and purpose. Execute downloads serially per output folder so manifest updates do not race. On failure, the command exits nonzero, removes partial files, and leaves successful prior assets intact. Rerun using a fresh output directory or new name. Downloads and manifests are not legal-clearance proof.

The font command supports bundled curated pairings, downloads the required Google Fonts CSS, rewrites its font URLs to local filenames, and saves each family's OFL text. Review the license and verify rendered glyphs before production. A custom family/weight combination can be obtained through current Google/Bunny/Fontsource tooling; use the same manifest and QA requirements. Do not invent a license file for a font absent from the presets.

## Structured brief

```json
{
  "aspect_ratio": "16:9",
  "aspect_ratio_confirmed": true,
  "width": 1920,
  "height": 1080,
  "font_choice_confirmed": true,
  "palette_choice_confirmed": true,
  "fonts": {"heading": "Space Grotesk", "body": "DM Sans", "captions": "DM Sans"},
  "font_files": ["/absolute/existing/local/font.woff2"],
  "font_verification": {"licenses_reviewed": true, "glyphs_checked": true, "renderer_loaded": true},
  "theme": "studio-light",
  "palette": {"background": "#F7F8FA", "text": "#15212B", "accent": "#12634E", "secondary": "#8B3B21"}
}
```

The font path is schematic, not a bundled file. Populate actual existing files from the manifest and include every required family, weight, subset, and license in the specialist handoff. For `Custom` use a numeric positive `W:H` ratio and a named custom theme. Use even dimensions for the baseline H.264 output. Explicit “Choose for me” answers may set the corresponding confirmed flag only after recording the user's delegation and the resolved choice. Never manufacture confirmations or verification flags to pass the helper.

Validation rejects unconfirmed creative choices, dimension/ratio mismatch, missing font roles/files, unrecorded license/glyph/renderer checks, invalid color values, and normal text/background contrast below 4.5:1. It reports accent/background contrast but does not assume every accent is body text. The check verifies records and file presence, not font authenticity, identity mapping, license legality, all moving-frame contrast, or final video playback. Those remain human/agent QA gates.

## Test the helper

Copy and run `scripts/test_design_tools.py` next to the helper using `python3 -m unittest discover -s scripts -p 'test_design_tools.py' -v` from the skill root. Tests use generated temporary fixtures and mocked responses; they do not download user assets. Check live acquisition separately when the network is available.
