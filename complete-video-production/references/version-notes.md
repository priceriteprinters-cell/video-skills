# Version 3 — Enhancement and Asset-Pack Notes

## Changes

- Replaced the mandatory San Francisco default with selectable single families and complementary font combinations.
- Preserved explicit ratio confirmation, including revised exports, and combined it with font and palette/theme questions.
- Added curated typography and palette data with named roles and contrast checks.
- Bundled the supplied no-sign-up resource catalog unchanged as the primary discovery reference.
- Added proactive acquisition of all needed assets: listed sources, broader lawful web research, then AI-generated PNG illustration fallback when suitable visuals are unavailable.
- Added HTTPS asset downloads, public-destination/redirect checks, bounded size, signature checks, conservative SVG screening, no-overwrite storage, and provenance records.
- Added Simple Icons/Iconify retrieval and locally cached Google Fonts with OFL files and rewritten local CSS.
- Added structured brief validation and 17 automated tests.
- Extended handoff, motion, and final-review gates for selected type, palette, assets and authentic-versus-generated provenance.
- Added interoperable companion ai-video-asset-pack support with the motion-assets/v1 manifest, scene-mapped real PNGs, safe ZIP import, hash/dimension/alpha checks and complete/partial coverage tracking.
- Added 12 asset-pack tests; all 29 production-tool tests and the companion's 12 tests passed, including ZIP generation/import round trips.

## Verified during preparation

All 17 automated tests passed. A live font-acquisition run downloaded six font files for Space Grotesk/DM Sans plus both OFL license files and local CSS. All six files loaded and measured successfully with Pillow. Live Simple Icons and Iconify downloads returned valid SVGs and manifests. Local Markdown links resolved.

## Boundaries

This update is a reusable production skill and acquisition/validation toolkit, not a standalone video-rendering application. Broad research and AI-image fallback are agent workflow instructions using current platform tools, not hidden third-party API calls in the Python helper. A successful asset download is not blanket legal clearance. PNG fallback is for illustrative imagery; it cannot replace missing audio, a licensed font, a genuine logo or factual product evidence. No video or AI-image generation was requested or run while editing the skill, so a complete rendered-video flow has not been reverified here. Production QA remains mandatory for every future video.

## v4
- Merged the former ai-video-asset-pack skill into this skill as Asset-pack mode; one self-contained skill now generates, packages, validates, and reuses PNG asset packs.

## v5
- Expanded to 29 font pairings and 24 palettes with categories/moods; added `preview` command producing real-font specimen sheets shown to the user before the font question.

## v6
- Briefing adds a dark/light visual-mode question plus default-and-approve style, animation intensity, and brand-guideline preferences.
- New mandatory stage: research (cross-checked authoritative sources, research ledger), audio transcription with unclear-span flagging, and script audit with an approval protocol for meaning-affecting changes (`references/research-and-script-audit.md`).
- New `references/production-standards.md`: art-direction style sheet, motion technique palette, intensity levels, asset quality gate, zero-placeholder rule, full-length review, loudness targets, delivery package.
- New `scripts/production_check.py` (placeholder/debug/missing-asset scan and black-frame detection) with 7 tests.

## v7 (from end-to-end test)
- E2E run passed all stages: font preview, font/icon acquisition, brief validation (incl. low-contrast rejection), PNG generation and asset-pack pack/inspect/import, narration transcription, fact research catching a planted error (Einstein → Edmond Becquerel, 1839), corrected re-record, placeholder scan, render, black-frame scan, decode and loudness check.
- Fix: the export measured −18 LUFS against the −14 LUFS target because loudness targets were not in the handoff; the animation handoff now carries explicit audio targets.
