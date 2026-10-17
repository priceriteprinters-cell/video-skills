# Typography and Palette Direction

## Select roles, not a pile of fonts

The supplied resource guide names font libraries, not specific mandated font families. The following combinations are curated suggestions added by this enhancement, not claims about the uploaded guide. Adapt the shortlist to the subject and brand, and let the user select. A single family is a valid option.

| Direction | Heading / supporting text / captions | Why it fits |
|---|---|---|
| Modern | Space Grotesk / DM Sans / DM Sans | Distinct display rhythm with neutral readable support |
| Editorial | DM Serif Display / Manrope / Manrope | Expressive headlines with restrained supporting typography |
| Bold | Bebas Neue / Source Sans 3 / Source Sans 3 | Short emphatic titles and readable explanatory text |
| Unified | Manrope for all roles | Quiet, cohesive hierarchy through size and weight |

Offer three relevant choices plus Custom in the font question. Show the family names and roles, not an unexplained style label. Allow a user to pick a single family, supply a licensed font, choose another pairing, or explicitly delegate the choice. Do not add an unchosen decorative family later. Limit simultaneous families to purposeful roles, generally two; add a mono family for code/data or Noto for actual script coverage only when useful and approved. User brand requirements override these suggestions.

## Acquire and verify

Prefer Google Fonts, Bunny Fonts, or Fontsource from the primary guide for reproducible open-font files; use the other listed font directories only after checking the specific download and license. Never assume all files from a directory have the same terms. San Francisco is not an open-font default: use it only on request with supplied/permitted files and verified rights; do not download proprietary fonts from mirrors.

Use the helper's `fonts --pairing modern --out /tmp/video-assets` for curated pairings. It obtains current Google Fonts CSS, local font files for required weights, and each family's OFL text. Inspect the returned manifest, read the license, and verify the family/file association. Self-host the resulting CSS and font files for deterministic rendering. Keep family license notices. If acquiring manually, preserve actual font metadata, weight/style ranges, Unicode subsets, original license text, source URL, and hash.

Load every face before measuring or capturing text. In a browser renderer await `document.fonts.ready` and explicitly load each used family/weight with representative text; examine actual font availability as well as successful promises. Inspect rendered glyphs: readiness alone can still hide fallback or missing coverage. Check punctuation, numerals, currency, italic/bold availability, ligatures, actual language scripts and RTL shaping when relevant. Noto coverage must be selected for the required script, not assumed from its family name. If a font fails, repair it or seek approval for an alternative; never silently substitute.

## Hierarchy and motion

Define title, subtitle, body, label, caption and data roles once. Use responsive composition appropriate to the chosen canvas, not a fixed landscape layout shrunk for portrait. Start with title/body size ratios around 2–3:1 and adjust to actual copy and viewing distance; these are suggestions, not output acceptance thresholds. Check phone-scale legibility. Prefer shorter copy and better wrapping over tiny labels. Keep caption placement stable and separate from headline motion.

Use tracking intentionally and avoid cramped all-caps paragraphs. Keep body lines comfortable, use consistent line height, and avoid widows or abrupt weight changes. Animate words or phrases with coordinated staggering, masks, emphasis and smooth settles; preserve a readable hold before exit. Do not animate every line with unrelated effects. Respect motion sensitivity: avoid rapid flashing and aggressive shake.

## Palette choices

Offer 3–4 subject-appropriate palettes including light and dark, with custom input available. `assets/design-presets.json` contains usable starting points, not a fixed brand or a reason to override supplied colors. In the question show each swatch in background, text, accent, secondary order and identify those roles in the description. Record the chosen exact values and visual treatment.

Use semantic tokens such as background, surface, text, muted-text, accent, secondary, positive, caution. Derive any additional surfaces deliberately and validate their text combinations. Do not use the same color for unrelated meanings in one diagram. Use labels, patterns or shapes alongside color, especially for comparisons and status.

Validate text on its actual background: aim for WCAG contrast at least 4.5:1 for normal text and 3:1 for genuinely large display text; use 4.5:1 for captions and small labels. Important non-text indicators should reach 3:1 against adjacent colors. These are useful static-design baselines, not certification of accessible video. Check overlays, moving gradients, transparency and image backplates separately. Accent swatches need not all be text colors: validate each actual foreground/background pair. Preserve brand logo colors and provide an appropriate contrasting surface.

The helper reports text/background and accent/background contrast, but only blocks insufficient normal text/background contrast. Other measured combinations are advisory until their intended use is known. Use WebAIM or another checker listed in the guide for manual cross-checks.


## Preset library and live previews (v5)

- `assets/design-presets.json` holds 29 verified OFL font pairings (each with category, mood, roles, weights, Google dirs; 15 map to native `tool_preview_preset` cards) and 24 palettes (light/dark, category, background, surface, text, accent, secondary; all text/background ≥ 4.5:1).
- Preview workflow: `python3 scripts/design_tools.py preview --pairings modern bebas-barlow fredoka-nunito --palette noir-gold --title "Real headline" --out /tmp/preview.html`, open in headless Chromium, `await document.fonts.ready`, screenshot to PNG, inspect that the actual fonts loaded (not fallbacks), then show it to the user. Use the user's real headline and palette so the preview matches the video.
- To compare palettes, render the same pairing in several palettes. Never present a preview whose fonts failed to load.
