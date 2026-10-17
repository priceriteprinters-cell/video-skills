# Interoperable PNG Pack Contract

## Contents

- `asset-pack.json` — root manifest, schema `motion-assets/v1`.
- `assets/<stable-name>.png` — every included visual as actual PNG bytes.
- No executable code, hidden files, nested ZIPs, remote pointers, symlinks, credentials or unnecessary intermediate files.

```json
{
  "schema": "motion-assets/v1",
  "title": "Context-specific video imagery",
  "context": "Short supplied topic or script summary; not invented factual claims",
  "complete": true,
  "missing": [],
  "creative": {"aspect_ratio": "16:9", "theme": "User-selected theme", "palette": {"background": "#15171A", "text": "#F6F7F9", "accent": "#D8F36A", "secondary": "#73CBE5"}},
  "assets": [
    {"id": "scene-01-device", "file": "assets/scene-01-device.png", "scene_ids": ["scene-01"], "purpose": "Device cutout for process explanation", "width": 1024, "height": 1024, "transparent": true, "provenance": "generated", "source": "AI-generated illustrative artwork", "reviewed": true, "sha256": "ACTUAL_SHA256_OF_FILE"}
  ]
}
```

This is a schema illustration, not an existing generated asset. Replace every example with measured values. `complete` is true only after all planned needs are satisfied; otherwise set false and provide meaningful `missing` entries. Creative settings are reuse hints, not proof of the user's three production confirmations. `transparent` means alpha actually contains transparent pixels, not merely an RGBA container. Hash every file. Include generation purpose but no sensitive prompt details. For supplied/downloaded assets record source and rights review; do not falsely label them AI-generated.

## Tools

Copy `scripts/asset_pack.py` to a temporary directory before execution under current skill access rules. Python 3.10+ and Pillow are required; use an isolated temporary dependency installation only if Pillow is unavailable. Do not run scripts from uploaded ZIPs.

```bash
python3 asset_pack.py validate --folder /tmp/png-pack
python3 asset_pack.py pack --folder /tmp/png-pack --zip /tmp/context-assets_v1.zip
python3 asset_pack.py inspect --zip /tmp/context-assets_v1.zip
python3 asset_pack.py import --zip /tmp/context-assets_v1.zip --out /tmp/imported-context-assets
```

Use fresh output paths, retain original uploads, and inspect the ZIP listing in a separate command before copying a deliverable into Files. The helper bounds entry count, individual and expanded sizes, rejects encryption/path traversal/symlinks/duplicate paths/non-PNG extras, verifies hash/dimensions/alpha and review records, and decodes every image. It will not execute any archive content. Imported images still need visual review and confirmation they fit the requested subject. Partial packs can be read but cannot be marked complete.

Pack ZIPs may exceed chat's upload limit (currently 20 MB/file); optimize losslessly or partition into independently validated packs if necessary, never drop assets silently. The pack helper rejects an archive larger than 20 MiB to keep attachments usable. Each split pack must honestly mark coverage and missing needs, and the consumer must validate each independently.
