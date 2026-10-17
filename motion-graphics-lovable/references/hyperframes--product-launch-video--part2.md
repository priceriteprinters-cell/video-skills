

<!-- ===== FILE: hyperframes/product-launch-video/references/story-design.md ===== -->

# Story design — product launch video

Step 3 of the product-launch flow. Output: `STORYBOARD.md` (the narrative plan, one frame per beat) and `SCRIPT.md` (the locked spoken narration).

This step decides **what the video says, in what order, and how each beat is said** — and it says each beat in the SHAPE of a proven script. It does not design layout, composition, or motion (that is Step 4). For exact file syntax follow `../../hyperframes/references/storyboard-format.md` and `../../hyperframes/references/script-format.md`.

## What story design produces

For every beat, four things:

1. **Position in the SEQUENCE** — the shot order. Story truth decides which beats exist and in what order (the arc).
2. **Voiceover written in a blueprint's script shape** — the spoken line, drafted to sound like the proven script for the shape this beat is reaching toward (see the script bank below).
3. **A candidate `blueprint:` id** — the proven shot SHAPE this beat leans toward (a tag, not a commitment; Step 4 confirms or overrides).
4. **`transition_in`** — how this beat enters from the one before it.

The big idea: **the blueprint is applied from the very first step.** The blueprints were reverse-engineered from 50 golden clips; each one implies a proven script. So we write the VO in that script's shape from the start — the voiceover is blueprint-shaped before Step 4 ever runs, which makes the blueprint's hit-rate downstream high.

This is still a SOFT discipline. Story truth comes first: **never invent, bend, drop, or reorder a beat to fit a blueprint.** The script patterns only shape HOW a beat is said and which proven shape it leans toward — they never decide which beats exist.

## Read first

1. `hyperframes.json` — locked brief: angle, length, aspect ratio, language.
2. `frame.md` — tone, mood, design system, brand register.
3. `capture/extracted/visible-text.txt` — product facts, page copy, positioning, proof, CTA.
4. `capture/extracted/asset-descriptions.md` — the ONLY source for the captured asset inventory.
5. `user_script.txt` and `VO_MODE`, when present.

Do not inspect `capture/assets/`, contact sheets, screenshots, or raw files in Step 3. Treat `asset-descriptions.md` as the canonical asset list. Never invent asset filenames.

## Method

### 1. Extract the product truth

From the brief and captured text, name:

- **Audience** — who the video speaks to.
- **Pain / desire** — what they already want fixed or achieved.
- **Promise** — the one-line thesis of the whole video.
- **Product role** — what the product does in the story.
- **Proof** — features, UI moments, metrics, logos, demos.
- **CTA** — what the viewer should do next.

Build the sequence around the **promise**, not a feature list. A website is an information layout; a video is an emotional sequence. Reorder, merge, and omit captured content freely — do not follow page order.

### 2. Choose the arc (the sequence backbone)

Pick ONE arc — it fixes the beat order. Compound only when useful (e.g. `PAS with feature-benefit progression`).

| Arc                       | Use when                                         | Beat order                                                                  |
| ------------------------- | ------------------------------------------------ | --------------------------------------------------------------------------- |
| `PAS`                     | Pain is known and urgent (broken B2B workflows). | hook → pain → agitation → solution tease → product intro → proof/demo → CTA |
| `Future Pacing`           | Sells a new future / category / paradigm.        | imagine → name product → remove pain → mechanism → outcome → CTA            |
| `Demo Loop`               | UI is self-explanatory; best shown working.      | question → product intro → demo cycle 1 → demo cycle 2 → trust → CTA        |
| `BAB`                     | Bridges an old workflow to a better one.         | before → after tease → bridge/product → step 1 → step 2 → wow → CTA         |
| `Feature-Benefit Cascade` | Feature-rich or desire/status-driven.            | category hook → feature → benefit → feature → benefit → climax → CTA        |

Use feature→benefit rhythm inside any arc when there are many capabilities — always translate a feature into viewer value, never stack raw features.

`frame.md` tunes the VOICE, not the arc: restrained/B2B → plain, low-hype; bold/launch → short, punchy; warm/human → friendly direct address; premium/cinematic → aspirational, fewer words.

### 3. Lay out the beats, each with a role

One clear job per beat — never "more benefits" or "another feature." Beat `type` (= blueprint **role**):

`hook | pain_point | product_intro | feature_showcase | benefit_highlight | social_proof | branding | cta`

The opening 3–5s needs ONE hook that creates tension, curiosity, or desire — a shocking stat, pain validation, a rhetorical question, direct address, an imagine/future-pace, a category announcement, or visual spectacle. Never open with generic company description. Per `../../hyperframes-creative/references/story-spine.md`: the hook speaks the viewer's outcome language (what they gain, never a feature list), and the promise (`message`) lands by beat 2 — features after that are its evidence.

A UI demo is usually a SEQUENCE of 3+ consecutive `feature_showcase` / `benefit_highlight` beats on the same surface (input → response → result → benefit), not one isolated frame.

### 4. Write each beat's VO in its blueprint's script shape

For each beat, look up its **role** in the script bank below, find the blueprint whose SHAPE fits the beat you already chose, and **draft the voiceover to sound like that blueprint's pattern.** Tag the candidate `blueprint:` id on the frame.

- The bank is the heart of this step: proven product-launch clips reversed into the one VO line each implies, grouped by role → blueprint, each with a **pattern** to imitate.
- If two blueprints fit the beat, prefer the one whose script shape matches the line you'd naturally write.
- If NO shape fits the beat, omit `blueprint:` and write the VO plainly — Step 4 composes that frame freely. Do not force a wrong shape.
- **Vary the shapes across the video.** Reaching for the same blueprint every beat re-creates the sameness this exists to avoid. `kinetic-type-beats` is the workhorse (6 roles) — lean on it, but not everywhere.
- **Write each VO as discrete cues, not one run-on breath.** Step 5 reveals each on-screen piece _when the voiceover names it_ (the anti-PowerPoint mechanism — `motion-language.md` Part 2). A line with clear phrase boundaries — "Content, sentiment, engagement — in one place" — hands the shot its reveal cadence for free; a single long clause leaves the frame nothing to pace to. The bank patterns are already cue-segmented — keep that rhythm.

Step 3 only TAGS the candidate id and writes the shaped VO. Step 4 (visual design) picks and instantiates the blueprint into a time-coded shot; it may override or drop a Step 3 candidate. The full menu with picking guidance lives in `../../hyperframes-animation/blueprints-index.md`.

---

## The script bank — what each beat's VO sounds like

> Proven product-launch clips, each reversed into the one spoken line it implies. Grouped by **role → blueprint**. Real product names kept (swap in your own). Draft your beat's VO in the SHAPE of the matching pattern. Kept 1:1 with the role declarations in `../../hyperframes-animation/blueprints-index.md` — when a blueprint gains a role there, add its script shape here.

### HOOK

**kinetic-type-beats** — the words ARE the motion

- Mailoji — "Still using a @gmail address? Or @outlook, or @hotmail, or @yahoo?"
- Outrank — "Getting traffic is hard. Insanely hard."
- AiAgent — "An AI agent that's easy to use — and optimised for you."
- Uizard — "Transform your sketches into prototypes — automatically."
- _Pattern:_ a punchy claim or rhetorical jab whose KEY WORD swaps in place (or escalates beat by beat) — the swap/escalation is the joke.

**typewriter-reveal** — someone is typing this

- "Need answers about your audience — right now?"
- Contra — "You are more than your job title. You are more than your resume."
- _Pattern:_ a relatable line typed live and edited mid-stream (a word backspaces and retypes) — the everyday thought, in your own words.

**spatial-pan-stations** — a panned timeline

- Rows — "From VisiCalc to Excel to Google Sheets — the spreadsheet has barely changed since 1979."
- _Pattern:_ a march of named milestones across time, landing on "...until now / ...up to us."

**constellation-hub** — nodes ring a center, camera pushes in

- "Content, sentiment, engagement, analysis — every platform you're on, in one place."
- _Pattern:_ a spread of tools/channels collapsing onto one center — "it connects everything."

**ticker-takeover** — options cycle, then a hero crashes in

- Notion — "A doc? A database? A wiki? — no, it's all of them, in one place."
- _Pattern:_ a "could be X, or Y, or Z?" cycle on one swapping word, then a hero claim crashes in and replaces it — "actually, this is what it is."

**prompt-type-submit-generate** — watch me ask

- "Build me a landing page for my coffee brand — dark, minimal, launch-ready."
- "What if you could just… ask?"
- _Pattern:_ the VO speaks (or frames) the ask itself while the prompt types live — the question is the whole hook; the answer stays off-screen, or a second ask starts before the cut.

**zoom-out-workspace-reveal** — the mystery re-scopes

- "This isn't a finished animation — it's your canvas."
- _Pattern:_ near-silence or one slow tease over the close-up mystery, with the landing line timed to the zoom-out — the words answer "what am I looking at?" exactly when the workspace does.

**fixed-anchor-cycle** — a roll-call around a pinned line

- "For founders, for designers, for marketers, for teams — for anyone who ships."
- _Pattern:_ one static claim holds while its audience/option list cycles fast beneath it — the list is the sentence's swapping object, and the brand line lands after the cycle clears.

**cursor-ui-demo** — a canvas already alive

- "Your whole team is already in here — designing, commenting, shipping."
- _Pattern:_ a "we're all here working" line over an ambient multi-cursor canvas — presence, not features; the live activity is the proof.

**dataviz-countup** — cold-open on one exploding stat

- "One million users. Ninety days."
- _Pattern:_ ONE statistic counts up as the VO speaks it — scale alone carries the tension; no product, no context yet.

**cta-morph-press** — a lone widget does its trick

- "It starts as a search bar. It becomes your whole workflow."
- _Pattern:_ one small widget on a bare field morphs in place and performs its payload while the VO names the transformation — small thing, big claim, hand off to the title.

### PROBLEM

**kinetic-type-beats** — pain lands alone on a bare canvas

- Butter — "What if your sessions didn't have to be boring and unstructured — or buried under a dozen tabs?"
- SmartCue — "You asked for better leads. We were the cure — MQLs that actually convert, a sales team that becomes your ally."
- _Pattern:_ 3–5 short pain statements (or a "what if?" framing), each landing solo before the next — no product yet.

**spatial-pan-stations** — a panned web of pain

- Vauban — "Coordinating legal documents, signatures, and cross-border transactions — it's a tangled mess."
- _Pattern:_ pain "stations" traversed one by one, ending on a knot — "too many disconnected steps."

**dataviz-countup** — the data IS the argument

- "67% of professionals say leadership is disconnected — and it's costing them a 65% boost in profitability."
- _Pattern:_ a count-up / chart / stat the camera pushes through to dramatize a worsening or large-scale problem.

**overwhelm-surround** — buried by your own tools

- "Slack, email, docs, tickets, three more tabs — and somehow it all lands on you."
- _Pattern:_ recognizable tools pile in until they surround and bury the viewer — the pain is being swamped, not one bad number.

### PRODUCT_INTRO

**kinetic-type-beats** — "Introducing…" name-drop

- "Elevating experiences, removing manual touchpoints, automating processes — so you can focus on the customer."
- Uizard — "Introducing Uizard — the design tool for everyone."
- _Pattern:_ hard-cut through "Introducing…" / tagline / value beats and resolve on the brand name or logo.

**logo-assemble-lockup** — wordless premium sting

- Manifold — "Manifold." _(wordless mark assembles; VO optional — just the name)_
- _Pattern:_ an abstract system assembles around a fixed mark — no copy, or just the product name landing.

**cursor-ui-demo** — first cursor-led look

- ClickUp — "This is ClickUp — click through and watch your whole workspace change."
- "Pull up any contact, find the right advisor, and you're matched in seconds."
- PaLM 2 — "Meet PaLM 2 — what is it, what can it do, and how was it built?"
- _Pattern:_ a cursor sweeps in to introduce the surface — a light first look landing on a hovered hero element or fresh result.

**dataviz-countup** — open on the result

- SuperX — "X growth — discover what really works: 19.6 million impressions."
- _Pattern:_ a confident "look at the data / the result" open — scroll a tilted card grid to one glowing hero metric, tagline assembling word by word.

**video-text-pivot** — show it work, then the number

- "Watch it run — then look at what it saved: 14 hours, every week."
- _Pattern:_ the product video plays, then slides aside to hand the frame to one impact stat — "see it work, now see what it's worth."

**prompt-type-submit-generate** — something you talk to

- "Meet Ada — describe what you need, attach what you have, and let it run."
- _Pattern:_ the first look IS the composer — the VO introduces the product as a conversation partner while a long prompt types with attachments and option picks, ending on (or just after) the submit.

**spatial-pan-stations** — decode the idea, then land on it live

- "Capture, structure, publish — that's the idea. Here it is running."
- _Pattern:_ a labeled concept strip read station by station, the final pan bridging into the live demo — "here's the idea → here it is working."

**device-surface-showcase** — introduced by completing its core loop

- "Open a space, drop in your notes, hit share — that's it, that's the product."
- _Pattern:_ the product introduced by DOING its core loop once inside its real interface, stepwise and cursorless — the VO narrates the steps plainly and lands on "that's it."

**titlecard-reveal** — a near-still title prelude

- "Relay. Docs that write themselves. Let's look inside."
- _Pattern:_ 2–3 near-still cards seamed by blur-snap handoffs — name, one-line claim, then into the product; each card carries one short spoken phrase.

### KEY_FEATURE

**grid-card-assemble** — enumerate breadth at once

- Postcards — "Want more? Unlimited exports, 1,400 fonts, an AI assistant, version history — and it's free to try."
- ClearVPN — "ClearVPN is built to help you: streaming access, secure browsing, location changing — only the essentials."
- Copilot — "Command bar, Zapier, white-labeling, API, SOC2 — and a whole lot more."
- _Pattern:_ a tile/pill/card grid self-assembles to show many capabilities at once — "look how much it does."

**cursor-ui-demo** — one workflow, end to end

- "Scroll your feed, then jump straight to your notifications — it's all one click away."
- Flowrite — "Pick your recipient, set your intention, choose a tone — and Flowrite writes it for you."
- Descript — "Tune your edits, add a crossfade, automate the volume, normalize loudness — then export."
- _Pattern:_ one specific multi-step workflow shown end-to-end across 2–4 real edits, landing on the action button or result.

**device-surface-showcase** — experienced inside its real interface

- HRS — "Your flight's cancelled — so book a hotel, a taxi, and get reimbursed, all in one digital journey."
- HelpKit — "A dynamic table of contents that follows your readers as they scroll."
- Graphite — "Use unique themes, recolor one element or several, and configure it all in a handy window."
- Contra — "Pick a template, make it yours, and launch a portfolio that's unmistakably you."
- _Pattern:_ a feature shown being USED inside its real surface — the device/window is the hero and its screens advance through a flow.

**comparison-split** — two paired capabilities, side by side

- "Design on the left, code on the right — always one source of truth."
- _Pattern:_ two complementary capabilities of equal weight shown together — "X and Y, in lockstep."

**video-text-pivot** — the feature, then its result

- "Here's the editor in action — and the result: a publish-ready cut in minutes."
- _Pattern:_ a feature clip runs, then yields the frame to a metric / impact line — the clip proves it, the number lands it.

**prompt-type-submit-generate** — one ask, one answer

- "Ask for revenue by region — and the chart draws itself."
- _Pattern:_ ONE prompt→response round trip — the VO names the ask, lets the status theater breathe a beat, then calls the result as it streams in.

**agent-progress-theater** — the machine visibly works

- "Kick off the scan — it checks every file, flags what's broken, and fixes what it can. Watch."
- _Pattern:_ trigger → working theater → receipt: the VO hands the work over, then reads the findings as rows land and check off — present tense, the machine is the subject.

**panel-edit-live-sync** — one gesture, two surfaces

- "Drag the value — the button follows. Pick a unit — the code converts. Live."
- _Pattern:_ 2–4 short cause→effect couplets, each pairing a gesture with its live mirror ("do X — Y answers"), ending held on the last edit.

**transcript-scroll-artifact-reveal** — the work, then the deliverable

- "It planned, researched, built, and tested — and left you the spreadsheet to prove it."
- _Pattern:_ a "look how much happened" line read down the transcript at traversal pace, then one pivot line cashes it in on the artifact — evidence first, payoff last.

**camera-journey** — a cinematic flight over the result

- "A month of content — planned, scheduled, and ready before you sat down."
- _Pattern:_ a flying camera explores the generated artifact while the VO makes one calm, sweeping claim; the content acts by itself — no hands, no clicks.

**dataviz-countup** — the numbers prove the feature

- "Response time, down 40%. Coverage, 3×. Every claim, a number."
- _Pattern:_ the feature proven by its metrics — a stat montage scrubbed / counted up while the VO reads each number as it lands.

### BENEFITS

**kinetic-type-beats** — rapid-fire value montage

- AiAgent — "No API keys, GPT-4 access, simple UX, clean UI — moving fast."
- Uizard — "Export to Sketch, create style guides, share, collaborate — and code less."
- _Pattern:_ a staccato montage of 8–12 short value phrases, each flashing and clearing at high tempo.

**grid-card-assemble** — an accumulating value list

- Lineicons — "Consistent and clean, tons of free icons, a Figma plugin, a powerful editor, every format you need."
- Plutio — "Manage projects, track time, send invoices, write proposals — all deeply customisable."
- _Pattern:_ short value phrases populate a vertical list ~1/sec, co-resident and accumulating, each popping into its slot.

**titlecard-reveal** — the calm value beat

- CSS Scan Pro — "A smart color picker — with instant tints and shades."
- _Pattern:_ one clean two-line value title, one slide-up crossfade, then held still. Low motion is the point.

**camera-journey** — travel the value chain

- "Leave one comment here — and the forecast updates over there."
- _Pattern:_ a cause→effect round trip: the VO's first half lands on the action, its second half on the payoff the camera travels to — "do this small thing here, get this big thing there."

**zoom-out-workspace-reveal** — this is just one corner

- "That one file it fixed? A corner of everything it already did."
- _Pattern:_ the VO tells the micro-story during the close-up dwell, then the scale line lands with the zoom-out — the benefit is breadth, revealed in one move.

**fixed-anchor-cycle** — everything changes, this stays

- "Same prompt. Every tool you own."
- _Pattern:_ one pinned claim while the entire surface re-skins around it — a short "works everywhere" line, then let the cycling themes speak.

**cursor-ui-demo** — demo, value line, demo

- "Watch it draft the reply — that's an hour back — now watch it file the ticket."
- _Pattern:_ a demo|text|demo sandwich — the VO alternates showing and telling, naming the value in the text beat between two live interactions.

### SOCIAL_PROOF

**constellation-hub** — the hub at the center of your stack

- kyvos — "On any BI tool — Tableau, Looker, Power BI — Kyvos sits at the center of your stack."
- "Connects to thousands of apps — including every one you already use."
- _Pattern:_ the product mark is the hub and partner logos orbit it — "sits at the center of everything you use." In the scatter-drift end-card variant there is no hub and no ring: a serif claim holds center while app icons pop in scattered and drift slowly outward — breadth said with count and spread, not geometry.

**grid-card-assemble** — a logo wall pulling back to a vast ecosystem

- Lineicons — "Used by more than 100,000 designers, developers, and companies — including these."
- ClickUp — "Connect Google Drive, Slack, GitHub, Stripe — your whole ecosystem in one place."
- Copilot — "With thousands of partner apps — Airtable, Calendly, Jira, Asana — you can embed anything."
- _Pattern:_ a wall of partner/app logos builds, then a camera zoom-out reveals a vast ecosystem.

**titlecard-reveal** — busy → clean proof card

- Trumpet — "We supply the trumpet, you bring the band — loved by 1,000+ sales, success, and marketing teams."
- _Pattern:_ wipe a busy open away to a clean lockup plus a "loved by N+ teams" line that settles and holds.

**dataviz-countup** — the numbers vouch

- "Twelve thousand teams. 4.9 stars. 99.98% uptime."
- _Pattern:_ proof by count-up — adoption, rating, and scale metrics tick up as the VO reads them; the biggest number lands last.

### CTA

**kinetic-type-beats** — punchy closing line beat-by-beat

- Stylebit — "Go pro, connect up to five Figma accounts — more features coming. Join now."
- revid.ai — "Boost your engagement and turbocharge your social media."
- _Pattern:_ a closing line (or short value stack) that snaps in beat by beat and lands on the logo or URL.

**logo-assemble-lockup** — logo build → push-through into the URL

- Strapi Cloud — "Deploy on Strapi Cloud — no server hassle, same flexibility. Try it now at strapi.io/cloud."
- Highlander — "Highlander is ready for the future you're building. Let's raise — at highlander.ai."
- STUDIO AI — "Get early access to STUDIO."
- Glorify — "Get started for free now — no credit card required."
- _Pattern:_ the logo builds, a fast camera push-through streaks giant CTA letters past the lens, resolving on the URL or action verb.

**cta-morph-press** — identity condenses into one click

- Linear — "This is Linear. Start building — it's free."
- _Pattern:_ the brand mark condenses straight into the single thing you click — "here's us → click here," no spatial set.

**prompt-type-submit-generate** — the command is the ask

- "One command — npm install relay — and you're live."
- _Pattern:_ the closing invitation IS a typed install command — the headline demotes, the terminal pill types it out, and the VO speaks the command (or one short line over it); the card holds with only the caret blinking.

**constellation-hub** — the orbit collapses into action

- "Everything you use, one hub — click, and it's yours."
- _Pattern:_ the ecosystem ring collapses onto the core on one click that springs the product open — the VO turns "it connects everything" into the action line.

**titlecard-reveal** — a calm end-card stack

- "Try it free. No credit card. relay.app."
- _Pattern:_ 2–3 near-still cards hard-cut in sequence, one short closing phrase each, terminating on the held logo/URL — the calm is the confidence.

### BRAND_OUTRO

**kinetic-type-beats** — a verb barrage resolving on one word

- Phantom — "Buy, store, stake, swap, send, connect, explore — multichain."
- _Pattern:_ a rapid center-channel barrage of single-word verbs asserting breadth, resolving on the brand's one defining word. No logo lockup needed.

**typewriter-reveal** — persistent mark + typed CTA rail

- Collato — "Next time, just Collato it — sign up for free today."
- _Pattern:_ the mark holds dead-center the whole time while a sub-line types or swaps into the final CTA.

**logo-assemble-lockup** — elements clear, the lockup draws itself in

- Copilot — "Copilot." _(pills disperse off-frame, the mark draws on; VO optional — just the name)_
- Dora AI — "Dora AI — join the waitlist."
- _Pattern:_ feature/UI elements clear the stage off all four edges, then the logo mark draws itself on and the wordmark completes the lockup.

**ticker-takeover** — use-cases cycle, the brand takes the frame

- "For notes, for tasks, for plans, for teams — [brand] holds it all."
- _Pattern:_ closing use-cases/verbs cycle through one slot, then the brand mark crashes in and owns the final frame.

**fixed-anchor-cycle** — the anchor holds, the words cycle

- bolt.new — "Prompt, run, edit, deploy — enjoy."
- Anthropic — "Opus 4.6 — by Anthropic."
- _Pattern:_ the brand name sits immovable while tagline words or praise quotes cycle beside it — per-word highlight stepping, or an accelerating flurry — landing on the completed lockup.

---

## VO_MODE handling

**No pasted script** — write the VO yourself, in the matching blueprint's script shape:

- 1–2 sentences per spoken beat, usually 6–20 words.
- Concrete and human; active verbs; say what the product does for a person.
- Avoid: "seamless experience," "unlock the power of," "streamline your workflow," long noun-phrase lists, a whole beat that is just "Or…".
- Silent beats are allowed when the visual proves the point — leave them out of `SCRIPT.md`.

**`VO_MODE = restructure`** — treat `user_script.txt` as source material. Rewrite, reorder, merge, or omit to fit the arc and target length. You may still shape each segment toward its beat's blueprint pattern.

**`VO_MODE = verbatim`** — do NOT change the user's words. Segment the script into beat-sized chunks at sentence/paragraph boundaries (split a long sentence only at a natural clause boundary). Final duration follows the provided script. Blueprint shaping does not apply to wording — only to which shape each verbatim chunk is paired with.

## Asset candidates

`asset_candidates` is the Step-3 → Step-4 handoff. Rules:

1. Read only `capture/extracted/asset-descriptions.md` to know what exists.
2. Use only filenames listed there; write as `assets/<basename>`.
3. One line, candidates separated by semicolons, a short description after `—`.
4. Prefer `[video]` assets when motion proves the product better than a still.
5. Use content assets (UI, screenshots, product photos, charts, demos). Skip tiny icons, favicons, badges, decorative chrome, repeated logo variants — unless the beat needs them. Partner / third-party logos come from `/media-use` (`resolve --type logo --entity <brand>`) — never redrawn by hand.
6. Pure-typography beats may use an empty asset list. Do not use nested lists.

Example:

```md
- asset_candidates: assets/dashboard-hero.png — dark analytics dashboard, wide screenshot; assets/demo-loop.mp4 — query-to-result interaction clip
```

## transition_in

Between-frame transition — how each frame ENTERS from the one before it. The harness's injector stamps it onto the two whole-frame clips (opacity / transform / filter on the frame wrappers). Name a **registry type** directly; optionally add a direction and/or a duration (`push-slide LEFT`, `crossfade 0.4s`). `cut` / `none` / empty = a hard cut.

The five registry types:

- **`crossfade`** — a plain opacity dissolve; the neutral choice when two frames sit in the same visual world.
- **`blur-crossfade`** — dissolve through a soft blur + slight scale; use when the two frames' backgrounds differ a lot, so the blur masks the color clash a plain crossfade would expose.
- **`push-slide`** `[LEFT|RIGHT|UP|DOWN]` — outgoing slides off, incoming pushes in from the opposite edge; a lateral "next beat" feel for a run of consecutive cards / feature beats.
- **`zoom-through`** — outgoing scales up + blurs out, incoming scales up from small into focus; for a STATE CHANGE / turning to a new section (hook → context).
- **`squeeze`** — outgoing compresses to a line on one edge as incoming expands from the other; a snappy, mechanical beat change.

Pick a small set and repeat them: default to `crossfade` (or `blur-crossfade` when the backgrounds clash), and reach for `zoom-through` at section boundaries. Frame 1's `transition_in` is a placeholder.

## Music & silence

The storyboard's top YAML block carries a `music:` field — the BGM mood the audio step retrieves against (e.g. `music: confident minimal tech underscore`). Omitting it falls back to `message:` → `arc:` → a neutral default, so BGM plays unless turned off explicitly.

- **`music: none`** — BGM off (narration, if any, still runs).
- **`music: none` + no `SCRIPT.md` + no `sfx:` cues or host audio** — the canonical **fully-silent marker**: no narration, no BGM, no SFX. `audio.mjs` generates nothing and Step 3.1 is a clean skip. Use exactly this spelling when the user asks for a silent / music-free video.

## Frame template

Use the exact fields required by the core storyboard format. The narrative shape each frame satisfies:

```md
## Frame N — Short name

- scene: one clear visual idea
- voiceover: "spoken line, written in the candidate blueprint's script shape, or empty"
- duration: rough estimate in seconds
- transition_in: crossfade
- status: outline
- src: compositions/frames/NN-short-name.html
- type: hook
- persuasion: Pain validation
- beat: urgency
- blueprint: kinetic-type-beats — candidate shape from the role→blueprint menu; omit when none fits
- asset_candidates: assets/example.png — short asset description

narrativeRole: what this beat does in the viewer journey.
keyMessage: the one idea the viewer should remember.
```

- `persuasion` — a concrete move (Pain agitation, Negative contrast, Friction reduction, Show-don't-tell proof, Feature-to-benefit translation, Statistical proof, Authority by association, Social proof, Risk reversal, Future pacing, Value stacking, Rule of three, Scarcity/urgency, Status seeking…). Never "show benefit." Invent one if none fits and explain it in the prose.
- `beat` — a specific emotion (anxiety, frustration, overwhelm, tension, urgency, skepticism, FOMO → relief, curiosity, clarity, intrigue, aspiration → trust, confidence, control, ease, power, awe, excitement, belonging → triumph, motivation, urgency-to-act, peace of mind, inevitability). Compound allowed (e.g. `relief + control`).

## Final checklist

- The arc is named; the sequence is narrative-driven, not page-order-driven.
- The opening uses one clear hook strategy that creates tension/curiosity/desire.
- Each beat has one job; every beat has `type`, `persuasion`, `beat`.
- Each beat's `voiceover` is written in its candidate blueprint's script shape (from the bank), with the candidate `blueprint:` tagged wherever a shape fits — and omitted where none does.
- Each `voiceover` is phrase-segmented into cues (each cue a piece Step 5 can reveal on) — not one long run-on clause.
- Shapes vary across the video; no single blueprint on every beat.
- Story truth was never bent to fit a blueprint — no beat invented/dropped/reordered for a shape.
- Every visual beat has suitable `asset_candidates` (filenames only from `asset-descriptions.md`), unless intentionally typography-only.
- UI/product demos use a multi-beat sequence when the value depends on workflow.
- `transition_in` is a registry type (`crossfade` / `blur-crossfade` / `push-slide` / `zoom-through` / `squeeze`) — default `crossfade` (`blur-crossfade` on a background clash), `zoom-through` at section boundaries, repeated across the video.
- `SCRIPT.md` contains only locked spoken narration; silent beats are intentional and omitted.


<!-- ===== FILE: hyperframes/product-launch-video/references/visual-design.md ===== -->

# Visual design — product-launch per-frame shot method

> The method behind **Step 4 (Frame visual design)**. You (the orchestrator) read it to **enrich `STORYBOARD.md` frames in place** — story-design wrote the skeleton (each frame's `scene`, `voiceover`, `transition_in`, the narrative fields, its `asset_candidates`, and optionally a candidate blueprint id); you add how each frame **looks and moves**. The unit you write per frame is a **time-coded shot sequence** — a shot directed across its whole duration, not a static slide. You write **no HTML** (that's the frame workers), you **never read `capture/`** (story already chose the assets), and you do **not** select assets or name transitions (story owns both). `frame.md` is your palette/type truth by role. Layout is a compact vocabulary in this file (the **Layout** section below), stated inline per Scene; motion vocabulary + the motion doctrine + the seek-safe core → `motion-language.md`; the proven shapes → `../../hyperframes-animation/blueprints-index.md` + `blueprints/<id>.md`; concrete rules resolve in Step 5 from this skill's local `../../hyperframes-animation/rules/`. Adding palette theory or a generic font rule here? Wrong home — `frame.md` + `hyperframes-creative`.

## The unit is a time-coded shot sequence

A frame's visual layer is **a sequence of time windows paced to the voiceover**, not a bag of effect tags. The failure that reads as PowerPoint is **front-loading**: the agent rushes the whole canvas on screen in the first ~25%, and then it just sits (the old representation — a flat set of effect names + a prose note — fired everything at entrance and left the rest empty). A time-coded shot sequence written **against the VO** makes that impossible: each window states what is on screen and what is moving, and **nothing appears before the voiceover reaches it.**

Write each frame as a handful of windows cued by the spoken line:

```
Scene 1 (0.0–Xs):  only what the VO is saying at t=0 enters — never the whole canvas
Scene 2 (Xs–Ys):   the next piece reveals as the VO names it (a line / card / stat / icon)
  …                one window per spoken cue — as many or as few as the line calls for
Scene N (…–end):   content has resolved; hold the read (stillness; subtle jitter at most)
```

- Each `Scene` line names **what's on screen**, **what moves in this window**, and **where it sits** (layout, inline). Times are real seconds across the frame's `duration`.
- **Pace reveals to the voiceover; never front-load.** This is the core anti-PowerPoint mechanism (→ `motion-language.md` Part 2 Rule 2). At t=0 show only what the VO is saying then; reveal each further piece — a line, a card, even an h1 — **when the VO names it**, spreading reveals across the shot and especially the **back ~50%**. **The window count = the number of spoken cues the line calls for** — a two-beat line is two windows, a five-feature list is five or six. There is **no fixed count and no mandatory "middle" act**; the only sin is dumping everything up front.
- **End on a held read.** Once the content has resolved it holds and reads — **prefer stillness to bad motion**: no forced camera drift, no lazy breathing, no back-half pan/push; at most a subtle jitter keeps it alive (→ `motion-language.md`). On a short shot the final reveal and the hold are the **same window** — the hold is not a separate mandatory act. Only the final frame has a real exit; every other frame's exit is the harness transition (story's `transition_in`).
- A **deliberately held** frame — content already revealed, now reading still — is legitimate and often right (a climax, a breather). The failure is never "too still"; it is **front-loaded-then-frozen** (everything dumped by ~25%, nothing cued to the VO). Place held beats deliberately for rhythm so the video isn't uniformly busy (allocate them in `## Video direction`). Reveal pacing + holds + the idle budget → `motion-language.md`.

## Pick the shape — instantiate a blueprint

Don't invent each shot from scratch. The frame's **role** (its `type` / `beat`) points to a proven shape:

1. **Match the role to a blueprint.** Open `../../hyperframes-animation/blueprints-index.md`, find the frame's role in the **role→blueprint menu**, and pick the blueprint whose intent fits this beat (story may already have named a candidate id — confirm or override it). Read that `blueprints/<id>.md`: it is a short, product-agnostic, **time-coded shot template with `[slots]`** and a named **signature move** (the thing that makes the shape itself — the SVG ring, the push-THROUGH, the in-place token swap).

2. **Instantiate its `[slots]` with THIS product's content** — three postures:
   - **Reproduce** — the blueprint fits the beat and your content maps onto its slots cleanly. Fill every `[slot]` with this product's word / asset / stat and follow its Scene timing. Write the resulting Scene lines.
   - **Adapt** — the _structure_ fits but the content / asset-count / surface doesn't (or you want a fresher surface to avoid templating). State **what you keep / what you change** in one line, then write the adapted Scene lines. You may extend or vary; you may **never** drop the **signature move** (drop it and you picked the wrong blueprint), and you keep the reveals **paced to the VO** — never collapse the shape to a single front-loaded dump.
   - **Compose** — no blueprint fits the beat. Build the shot from the **motion vocabulary** in `motion-language.md`: still pace the reveals to the VO across the shot, never fire everything at t=0. Mark it `blueprint: compose`.

3. **Keep the signature move.** Whichever posture, the blueprint's signature move (named in its file) is the spine of the shot — it usually lands on the shot's key reveal. Carry it through.

The blueprint's own Scene lines, motion vocabulary, and `rule mapping` are your raw material; you are choosing a shape and casting this product into it, not copying an engineering spec.

## What you add to each frame

Story-design's `## Frame N` block already carries the narrative + `asset_candidates`. You append the shot. Story's `scene` / `voiceover` / `transition_in` / role fields stay untouched.

```
## Frame 3 — The problem
- scene: a 20-minute timer over a stack of rejected takes   ← refine only if it could read sharper
- voiceover: "…"            ← story's; leave it
- transition_in: crossfade  ← story's; leave it
- type: pain_point          ← story's
- persuasion: Pain agitation
- beat: frustration
- blueprint: dataviz-countup (Adapt)   ← you add: the id you instantiated (or "compose")
- focal: assets/reject-stat.png         ← you add: the hero asset for this beat
- roles: reject-stat = cutout · timer = supporting · backdrop = background (dim ~40%)  ← you add: role per candidate
- sfx: impact-soft, riser               ← you add: the sound the beat wants (fetched + mounted at root; never yours to embed)

Adapt: keep the count-up-ring signature; one stat not three, and the trend chart becomes the rejected-takes count climbing.
Scene 1 (0.0–1.2s): solid backdrop (dim ~40%); a circular progress ring + bold center number seat dead-center, ring sweeps and number counts 0→20 on one heavy ease — Centered template, ~50% of frame. Slow push-in runs underneath.
Scene 2 (1.2–3.4s): as the VO names the count, the camera pushes THROUGH the ring into the rejected-takes stack lower-left; the stack grows beat-by-beat as a reject counter ticks up beside it (the count-up reveals on its spoken cue, not at t=0). Asymmetric 60/40, 3 depth layers.
Scene 3 (3.4–5.0s): land the hero stat card dead-center, accent glow blooms behind it and holds; the stat reads clean and STILL — no continuing push, no breathing (a held beat beats bad motion). The stillness reads against the prior motion.
```

The lightweight tags:

- **`blueprint:`** — the id you instantiated (with `(Reproduce)` / `(Adapt)`), or `compose`. One id per frame.
- **`focal:`** — which existing candidate is the hero of this beat.
- **`roles:`** — each candidate's role: `cutout` (foreground subject, lay text around it) · `background` (full-bleed, dim 30–50%) · `supporting` (secondary). You **consume** the candidates story chose — never add, swap, or drop one (coverage is story's call; if a frame truly has the wrong candidates, flag it back, don't reach into `capture/`).
- **`sfx:`** — name the sound the beat wants (an impact for a slam, a whoosh for a push, a riser into a reveal). The audio script's `fetch-sfx` pass retrieves it and the assembler mounts it at the root — you only **name** it, never embed an `<audio>` element.

**Layout is stated INLINE in each Scene line** — name the template, density, depth, and hierarchy as part of "where it sits" (`Centered, ~50% of frame`, `asymmetric 60/40, 3 depth layers`), drawing on the **Layout** vocabulary below; never write px / scale / shadow recipes (the worker writes those).

**Motion is named INLINE in each Scene line** — name the move from `motion-language.md`'s vocabulary (`ring sweeps`, `pushes THROUGH`, `count-up`, `glow blooms`) and let it settle on a long-tail curve (`power3` default — smooth beats bouncy; see `motion-language.md`). Never write ease curves / ms / stagger (those resolve in Step 5 from this skill's local `../../hyperframes-animation/rules/`).

## Layout — named inline per Scene

State each Scene's layout as part of "where it sits." **If the blueprint already implies a composition** (a ring around a center, stations on a wide canvas, two cards from opposite wings), that wins — describe it directly; the vocabulary below is for **composing freely** or a generic beat, not a menu you must pick from. Never write px / scale / shadow (the worker does). One frame's layout can EVOLVE across its Scenes (Scene 1 centered hero → Scene 2 rearranges to a grid).

- **Framing vocabulary** — centered (hero / climax) · rule-of-thirds · split-screen (comparison) · layered-depth (immersive) · asymmetric 60/40 or 70/30 (editorial) · triptych (three panels) · full-width strip. Vary the framing across the video so it doesn't read as one repeated template — let the beat decide, not a quota.
- **Density** — primary visual ≥ 40% of canvas; ≥ 3 depth layers (background + midground + foreground); never a lone small cluster floating in empty space. Squint test: after blur you can still pick out the #1 element.
- **Hierarchy** — combine ≥ 2 of size (3:1) / weight (800 vs 400) / contrast / position (upper-third is golden) / motion, so one element clearly dominates.
- **Depth** — layer 2–3 of: size, blur, opacity gradient, overlap, shadow-stack.
- **Don't show**: nav bars, footers, scrollbars, real cursors / browser chrome, generic decorative shapes standing in for a real asset, floating bokeh / purple-blue "AI" gradients — unless it's an intentional UI-demo reconstruction.

## `## Video direction` — write the invariants ONCE

The whole video shares one look and one motion grammar. Write a **`## Video direction`** block ONCE at the top of `STORYBOARD.md` so every frame inherits it and per-frame Scene lines carry only the **delta**. This block is load-bearing — it is what binds many independent shots into one film. **Keep it.**

- **palette system** — from `frame.md`: which roles map to which hues. Never invent.
- **motion grammar + reveal model** — long-tail eases (`power3` default, smooth over bouncy) + the **VO-paced reveal** model every frame follows (reveal each piece on its spoken cue; never front-load) + what may stay alive during a hold (subtle jitter at most; no lazy breathing) (→ `motion-language.md`).
- **rhythm / held-frame allocation** — name the **held / breather frames** (often before a climax) so the video varies its energy: most frames reveal to the VO, a few hold still (a held read beats bad motion; the anti-monotony discipline; → `motion-language.md`).
- **negative list** — what never appears: off-brand textures / effects the pack forbids, **plus both motion failure modes** — slideshow (front-load then freeze) and screensaver (everything floating independently) (→ `motion-language.md`).

Do **not** repeat these per frame — restating video-level rules in every frame is exactly the bloat this layer prevents.

## Palette & type — from `frame.md`, never invented

- **Palette** — `frame.md` (the adopted pack) is the color truth; apply its roles per frame. Generic basics (one accent, tint neutrals, avoid pure `#000`/`#fff`) → `hyperframes-creative/references/house-style.md`.
- **Type** — fonts resolve via `frame.md`'s type tokens; reference them **by role** (display / body / mono / the pack's ramp), never by raw family or px. Generic typography craft (embedded fonts, dark-bg optical compensation, `tabular-nums`) → `hyperframes-creative/references/typography.md`.

## Caption-band keep-out (plan side)

The bottom ~17% of the canvas is reserved for the caption pill. Plan every frame's content into the **top ~83%** so nothing important lands in the band (the worker enforces the pixel cutoff; you plan the layout). Holds even when captions are disabled — bottom-edge consistency.

## Where the detail lives

| For…                                                                      | Read                                                                                         |
| ------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------- |
| the proven shapes + role→blueprint menu + how to pick                     | `../../hyperframes-animation/blueprints-index.md` → `blueprints/<id>.md` (local)             |
| motion — shot model, vocabulary, holds, idle budget, stillness, seek-safe | `motion-language.md` (local)                                                                 |
| layout — templates, density, depth, hierarchy, caption band               | the **Layout** vocabulary in this file                                                       |
| concrete eases / ms / stagger + rule recipe bodies (Step 5)               | local `../../hyperframes-animation/rules/` (the frame worker reads it; you don't)            |
| palette + type tokens                                                     | the project's `frame.md`; basics → `hyperframes-creative` `house-style.md` / `typography.md` |
| "produced, not generated" foreground density                              | `hyperframes-creative/references/video-composition.md`                                       |
| within-frame cuts / seams (zoom-through · cut-the-curve · waterfall)      | `cut-catalog.md` (the worker builds them inside the composition)                             |
| transitions                                                               | story-design owns `transition_in`; you don't touch it                                        |

## Before you finish — checklist

- **`## Video direction`** written once at the top (palette · motion grammar + shot model + idle budget · stillness allocation · negative list incl. both failure modes); per-frame entries are deltas, not restatements.
- Every frame is a **time-coded shot sequence** with real second windows across its `duration` — not a tag bag.
- **No frame front-loads** — at t=0 only what the VO is saying enters; each further piece reveals on its spoken cue, across the back ~50%. Window count follows the VO, not a fixed number.
- Every frame names an **`blueprint:`** id (Reproduce / Adapt) or `compose`; an Adapt states keep/change and **keeps the signature move**; nothing collapses to a single front-loaded dump — reveals stay paced to the VO.
- **Held frames are deliberate** — allocated in Video direction for rhythm; a held read is fine (prefer stillness to bad motion), but no frame may be front-loaded-then-frozen.
- Each frame's `asset_candidates` have a `focal` + per-candidate `roles`; none added, swapped, or dropped.
- Layout named **inline** per Scene (template / density / depth / hierarchy — the **Layout** vocabulary here); motion named **inline** per Scene from the vocabulary (`motion-language.md`). No px / ease curves / ms / JS.
- Content planned into the top ~83% (caption band clear).
- Palette / type pulled from `frame.md` by role — nothing invented.
- You wrote no HTML and never read `capture/`.


<!-- ===== FILE: hyperframes/product-launch-video/sub-agents/frame-worker.md ===== -->

# Frame worker — product-launch delta

> The shared law is the core contract above (the packet builder prepends `../../hyperframes/references/frame-worker-core.md` to this file as `_role.md`) — read the two as one role. This file carries only what's specific to a product-launch frame; you run N-up, **one frame each** — your dispatch carries exactly one packet. Tempted to add a generic GSAP / timeline rule here? Wrong home — it belongs in the core contract or `hyperframes-core`.

## Your `focal:` / `roles:` — real captured media

- `focal:` — which candidate is the hero.
- `roles:` — each candidate's role: `cutout` foreground / `background` full-bleed / supporting — plus the real media available (each `public/<basename> — description`; a **`[video]`** tag marks a `.mp4` motion source that cannot be mounted by this sub-composition worker).
- **Asset paths are project-root relative everywhere.** This includes HTML attributes and CSS `url(...)` values such as `@font-face src`: use `assets/...` (or the supplied `capture/assets/...` path), never `../` or `../../`. Shared fonts are staged before dispatch so every parallel frame resolves the same local files; never fall back to a network `@import`.

## Placing candidates (product-launch constraint)

**Place each candidate by its `roles`** (the `focal` is the hero): a `cutout` is a foreground subject — respect the 83% keep-out, lay text around it, not over its face; a `background` is full-bleed and dimmed ~30–50% so foreground content stays legible. Frame files are sub-compositions. Audio remains orchestrator-owned: never author `<audio>` in a frame. An approved `[video]` candidate may be declared as a frame-local `<video data-frame-video="approved" data-start="..." data-duration="..." data-track-index="...">`; `assemble-index.mjs` hoists it to the host root and translates its timing. Give every approved video explicit host geometry with numeric `data-frame-video-x`, `data-frame-video-y`, `data-frame-video-width`, and `data-frame-video-height`; optionally set `data-frame-video-fit="cover|contain|fill|none|scale-down"` (default `cover`). The assembler converts only those values to host CSS: frame-local classes and inline styles do not cross the hoist boundary. Do not use this declaration for audio, unapproved URLs, or videos without explicit timing and geometry. If no approved video is supplied, use an explicitly supplied static still/key art (`[video-still]` or another image candidate) as `<img>`; do not extract a frame, fabricate a URL, or silently embed an unapproved clip.

When a frame showcases a captured website, use the supplied screenshot as the page. Do not rebuild the full site in HTML: even a close recreation can change the real layout, spacing, or branding. If the shot needs motion inside the page, overlay the supplied real assets at measured positions or rebuild only the moving component.

Brand text comes from your frame's `scene` / narrative — never from `frame.md` (a style spec, not the product's content). Place the named assets, and never invent new ones.

## Cross-frame handoffs

If the packet includes `handoff_in:` or `handoff_out:`, treat those values as a hard boundary contract. Start or end the named element at the exact x/y position, scale, opacity, and motion direction/speed provided; a field the packet states as unchanged is still binding, not optional. Do not restyle or reinterpret that boundary state. The neighboring frame is being built by another worker and will use the matching values.
