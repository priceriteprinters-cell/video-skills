# Resource Acquisition

## Treat the supplied guide as the discovery source

Read `free-design-resources-no-signup.md` for the complete catalog. It is the primary resource reference, not an exhaustive allowlist; it is not a blanket license grant, download API contract, or guarantee that a site still permits no-login access. Inspect the exact item's current terms and download behavior. Do not bypass logins, paywalls, rate limits, access denials, or attribution requirements. The guide's excluded providers are not recommended download paths; broader searches should find other lawful accessible sources, not evade those exclusions.

## Match the asset to its purpose

| Need | Start with the guide's sources | Check before use |
|---|---|---|
| Official brand/logo | Official media kit, Simple Icons, Devicon, then listed logo directories | Identity, current shape/colors, trademark/usage constraints; no endorsement claims |
| Generic explanatory icon | Lucide, Heroicons, Tabler, Phosphor; Iconify by set | Per-set or per-item license, stroke/weight consistency |
| Fonts | Google Fonts, Bunny Fonts, Fontsource; Noto for script coverage | Family and weight metadata, exact license, glyphs, local loading |
| Illustrations | Open Doodles, unDraw, IRA Design, FreeSVG, ctrlv.design | Per-pack license, authenticity versus illustration, aesthetic fit |
| Photos/product imagery | User/official assets first, then listed Unsplash/Pexels/CC0 sources | Actual download works without an account, depicted subject, model/property/trademark restrictions |
| Motion assets | Mixkit, Coverr, listed free animations | Specific item license, free/premium distinction, attribution, actual local rendering support |
| 3D/texture/HDRI | Poly Haven, ambientCG, Kenney, Quaternius | Exact asset license, resolution, dependencies, importer compatibility |
| Music and SFX | Mixkit, Kenney Audio, Sonniss, Musopen; CC0/CC BY filtered sources | Exact track/recording license; composer's public-domain status alone does not clear a recording |
| Palette inspiration | Color Hunt, Coolors, uiGradients, listed contrast tools | Do not assume a public export API; copy approved values rather than inventing endpoints |
| UI reference | shadcn/ui, HyperUI and other listed open-source kits | Use visual inspiration only when appropriate; a template is not an authentic product screenshot |

## Download reproducibly

1. Inventory user assets and authentic official sources first. Search for each named subject and map it to a scene. Do not render an approximate logo because downloading is inconvenient.
2. Prefer documented direct URLs, static CDNs or public APIs. Verify discovery pages using the current web-fetch tools; use direct HTTPS for actual files/API responses. Never construct an undocumented provider endpoint.
3. For Simple Icons use a verified slug; `https://cdn.simpleicons.org/<slug>` returns the source color. For Iconify use a verified prefix/name and check the collection's license; `https://api.iconify.design/<prefix>/<name>.svg` is a direct SVG route. These libraries provide recognizable marks, not proof of endorsement or legal clearance.
4. Use `scripts/design_tools.py fetch`, `icon`, or `fonts` as documented in automation-tools.md. The helper only downloads public HTTPS resources, checks redirects, bounds size, validates supported media signatures and conservative SVG safety, and stores a provenance manifest. It never executes downloaded code or extracts archives. Fetches with missing license evidence or rights-review confirmation fail.
5. Read actual license evidence before entering rights metadata. Retain license text/notices and required credit. Directory summaries or a successful response do not replace this review. Trademark and personality/property rights are separate. User-provided assets still need appropriate permission.
6. Inspect the local visual, decode/probe media with a known tool, check transparency/edges/resolution, verify identity, and record scene purpose. SVG fonts, filters, unsupported external references or nonstandard encodings may need a trusted conversion or another asset; do not disable safety checks to make an unknown SVG work.
7. Keep raw working downloads in `/tmp`. Before specialist delegation, stage only selected, verified files and their license/CSS dependencies into a permitted current Files location or project asset location according to the current platform workflow. Do not assume the specialist can read `/tmp`. Keep any project-served binary behind the supported asset-pointer flow. Do not deliver source assets or working folders unless requested.

## Failures and fallbacks

Acquire the complete set of needed assets yourself, including fonts, logos/icons, imagery and requested audio; do not routinely ask the user to locate/download them. Reuse supplied assets without downloading unnecessary duplicates. Build an asset-needs table with subject, scene interval, desired format/resolution, source attempts, local path, rights evidence, and final status. Resolve every row before final production or record a real blocker.

For each missing visual, follow this ladder:

1. Search the supplied guide's relevant providers and the subject's official source. Inspect and download a suitable asset, not just a search thumbnail.
2. If no suitable match is available, broaden to the public internet: vary the exact subject, visual description, format, and terms such as official media kit, press assets, public domain, CC0 or open license. Use independent parallel research when useful. Inspect actual candidate pages, licensing and files. The helper can accept a newly reviewed public hostname with `--allow-host`; the default host list is not a limit on discovery.
3. Try meaningfully different queries and at least two relevant independent source routes when available, rather than giving up after one failed link. Record attempted sources and concrete rejection reasons such as mismatch, inadequate resolution, unclear rights or access restrictions. Stop futile loops and obey terminal provider failures; persistence is not evasion.
4. If no suitable licensed visual is found after those attempts, generate a cohesive illustrative image using the current designated image-generation tool. This user's policy authorizes that fallback without another routine preference question. Request PNG output, use a transparent background for a cutout/overlay where supported, and keep full-scene artwork nontransparent. Match the approved palette, framing, scene purpose and visual style. Keep important typography in the animation renderer rather than baking long text into images.
5. If the current image tool only produces another format for the requested image type, convert the returned asset to PNG with a trusted image tool; conversion does not create transparency. Inspect the actual PNG, dimensions, alpha/edges, identity and factual accuracy. Record `generated` provenance, prompt purpose, generator result and local file. Never invent a download source or label AI output an official asset.
6. Stage the selected downloaded or generated files for the specialist and pass the complete confirmed inventory. Animate those assets with purposeful motion; a set of generated stills alone is not a motion-graphics video.

Do not generate a counterfeit logo, fabricated product screenshot, misleading real-person image or purported documentary evidence when the authentic asset is unavailable. Use an explicitly illustrative neutral concept or diagram without inventing exact product details, and disclose any material departure. Only ask for a user-supplied permitted file when exact authenticity is indispensable and lawful search cannot resolve it. Audio/font/3D gaps are not solved by a PNG: use an appropriate permitted acquisition/generation workflow or report the missing capability. Do not claim an asset exists or that generation succeeded without a successful tool result. A denied/failed generation is a real blocker, not permission to evade provider restrictions.

If a source requires login, offers unclear rights, returns HTML, or is rate-limited, try another lawful source; do not scrape protected downloads or use private URLs. Preserve identity, rights, and truthful provenance across every fallback.

The generic downloader supports common SVG/PNG/JPEG/WebP/GIF, MP4, MP3/WAV/Ogg, and TTF/OTF/WOFF/WOFF2 files. For Lottie, ZIP packs, 3D, EXR or other formats use current trusted platform acquisition and inspection tools; record the same provenance and rights data, check archive traversal and decompression limits, and never run bundled executable code. Do not promise every catalog source has a programmable no-key endpoint.
