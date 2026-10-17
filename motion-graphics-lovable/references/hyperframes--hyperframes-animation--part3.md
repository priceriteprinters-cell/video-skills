

<!-- ===== FILE: hyperframes/hyperframes-animation/blueprints/cta-morph-press.md ===== -->

# cta-morph-press — CTA Morph & Press

**intent**: A resting brand mark condenses at the same screen center into a smaller, brighter CTA, then a cursor arrives from off-stage and lands a human-aimed click on it. The viewer's eye is walked from "this is who we are" to "and this is what you do." The morph and the click are the two headline beats.

**roles served**

- CTA (from `cta-morph-press`): when the close moves from brand identity to a single user action, two elements share the same center sequentially (a morph, not a cut), and the payoff is a simulated click with physical feedback. Reach for it for a focused "click here" sign-off — no spatial set, no multi-step UI (that's `cursor-ui-demo`).
- Hook (ROLE-WIDENED, from `widget-morph-on-blank-field`): the same
  machinery run as an OPENER — a lone `[widget]` (pill / chip lockup) on a flat field transforms
  in place, performs its payload, then vanishes to a plain frame that a typed `[title]` resolves.
  The click, when present, ignites the morph rather than closing it; there may be no cursor at
  all. Reach for it when the product hook IS one widget doing one thing — still no spatial set,
  no multi-step UI (that's `cursor-ui-demo`). Mint-reconsideration trigger: if future mining
  brings 2+ more widget-morph openers with the vanish → typed-title resolve, promote this variant
  to its own blueprint (the beat order is fully inverted by then).

**duration**: 4–6s (Hook widget-morph opener 5–7.5s)

**shot structure** (a `[bg]` canvas; hero and CTA are flex-centered siblings sharing one `transform-origin`)

- **Scene 1 (0.0–~1.4s) — presence.** The `[hero mark / brand lockup]` holds dead-center, alive but resting — only a faint rotational breath on the mark; any title text under it stays rock-stable. Camera static.
- **Scene 2 (~1.4–2.4s) — the morph (signature move).** The hero CONDENSES at the same screen center into a smaller, brighter `[CTA]` (button / card): the outgoing mark shrink-fades exactly as the CTA scales up in its place. Because they share one `transform-origin`, the eye reads it as one element transforming, not a swap.
- **Scene 3 (~2.4–3.4s) — approach.** A `[cursor]` arrives from off-stage on a **decelerating** path (it "arrives," it does not pass through) and lands a few px **off** the CTA's geometric center, so the aim reads human, not scripted.
- **Scene 4 (~3.4–end) — press.** The cursor lands a physical CLICK — cursor and CTA compress together in lockstep, then release with feedback (an optional ripple / glow bloom). Holds on the clicked state.
- **Variant — Hook (widget-morph opener)** (from `widget-morph-on-blank-field`;
  reorders the beats — press first, morph second, title last). **(1) presence**: a lone
  `[pill / chip lockup]` sits centered on a flat `[field]`; optionally the `[cursor]` glides in, a
  hover pill-background appears behind the chip, and the click lands with the same lockstep press.
  **(2) the morph**: the widget transforms IN PLACE — expands downward anchored at its top edge
  into a `[menu]`, or spring-morphs outward into a `[prompt card]` with a small overshoot settle —
  new content fades/slides into place. **(3) payload**: the transformed state performs —
  `[placeholder]` types with a blinking caret, `[user text]` types while a control flips from
  muted to its vibrant active color, or the menu snap-collapses back to the pill carrying the
  `[new value]` + a checkmark pop; the background may snap to a new color under the persistent
  foreground card. **(4) resolve**: the widget VANISHES; a plain frame closes the beat — a
  `[closing title]` types on center, or a hold on the flipped solid.

**motion vocabulary**: faint rotation-only resting breath (logo scope only); same-center morph-swap (shrink-fade ↔ scale-up sharing `transform-origin`); cursor decel-arrival from off-stage; off-center human aim; lockstep press compression; release feedback ripple / glow. Hook opener: anchored downward expand of a pill into a menu and springy snap-collapse back;
chip-to-card spring morph with overshoot settle; placeholder / user-text typewriter with blinking
caret (may cut mid-word); control color-state flip muted → vibrant; background color snap under a
persistent foreground card; checkmark pop; widget vanish to blank frame; typed closing title.

**rule mapping**

- hero → CTA condense at one center → `scale-swap-transition` (shared `transform-origin: 50% 50%` is what sells the morph; CTA `position: absolute` so it doesn't shove the hero during the brief overlap)
- resting-hero aliveness (rotation only, scoped to the mark so the Phase-2 scale doesn't fight it) → `sine-wave-loop` (low-amplitude rotation register — subtle jitter, not a scale breath)
- cursor press + release in lockstep (single-target-array so both compress together) → `physics-press-reaction` (PRESS_DOWN + RELEASE portion)
- cursor approach (decel from off-stage, off-center landing, hard-cut opacity in) → `gsap-effects` (translate on `power2.out`)
- click ripple / release glow → `cursor-click-ripple` (attack-decay ring) and/or `ambient-glow-bloom` (release bloom)
- (Hook) chip → prompt-card spring morph at one center → `scale-swap-transition` (the base morph
  contract, run in the expand direction) + `card-morph-anchor` (corner-radius / surface ride-along)
- (Hook) anchored-edge expand / snap-collapse (pill ↔ menu, top edge pinned) →
  `anchored-layout-expand` (edge-anchored directional container growth — origin-pinned expansion
  with counter-scaled children; `card-morph-anchor` stays for uniform-scale morphs only)
- (Hook) placeholder + user typing, blinking caret, mid-word cut → `gsap-effects` (typewriter) +
  `context-sensitive-cursor` (blink) + `discrete-text-sequence` (mid-word cut states)
- (Hook) control color flip muted → vibrant → `press-release-spring` (color-transition variation)
- (Hook) checkmark pop / card-arrival overshoot → `spring-pop-entrance`
- (Hook) hover pill-background + igniting click → the base's `physics-press-reaction` +
  `cursor-click-ripple` mappings apply unchanged

**camera modifier**: camera-static — the morph and click happen in element space; a camera move would compete with the click as the climax. The Hook opener keeps the same contract — even the background color flip is an element-level
snap, not a camera event.


<!-- ===== FILE: hyperframes/hyperframes-animation/blueprints/cursor-ui-demo.md ===== -->

# cursor-ui-demo — Cursor-Driven UI Demo

**intent**: A visible custom cursor drives a real (reconstructed) app UI through clicks / hovers / drags so the screen changes state shot-to-shot, while the camera chases each interaction — the product surface is the subject and the cursor is the actor.

**roles served**

- Product_Intro (from `product-intro-cursor-ui-demo`): first look at the product surface — the cursor sweeps/hovers to \_introduce\* the app and reveal what it is, landing on a hovered hero element or freshly-popped result. Light, exploratory; backdrop steps colors as it goes.
- Key_Feature (from `key-feature-cursor-ui-demo`): one specific multi-step workflow demonstrated \_end-to-end\* (edit / configure / select across 2–4 discrete beats), each beat a real edit the UI responds to live, landing locked on the primary action button or the produced result.
- Key_Feature (from `workflow-approve-press`): an agency / confirmation workflow framed by a cockpit of 3D-tilted flanks — a step list ticks pending → active → complete (a snap state machine, CSS responding to `[data-state]`), and a flank button takes the PRESS as the payoff (its color flips to success, a checkmark stamps). The click is the climax, not a passing gesture.
- Key_Feature (from `cursor-app-state-tour`): the static-stage STATE TOUR — the cursor drives a reconstructed app through 2–4 discrete feature states on a LOCKED frame; every scene change is a click-triggered element swap/scale (modal springs from center, side panel slides in from the right edge, settings hard-swap, table populates, node-graph builds), never a real camera move; optional `[title card]` Scene 0 in front and a `[brand end beat]` behind.
- Key_Feature (from `drag-field-onto-document`): the DRAG-DROP journey — one continuous zoom-breathing shot of a document workspace: the cursor drags a ghosted `[field chip]` from an inputs sidebar onto the page, drop-snaps it into a placed field, a modal/typing beat completes it, and the placed element is adjusted in close-up before the cursor heads to the `[Finish/CTA]`.
- Product_Intro: the low-event BROWSE — the cursor roams ONE clean page state and the filter controls answer with slight hover updates; no typed input, no title beats, and the shot may end mid-roam.
- Product_Intro (from `hover-inspect-run`): the HOVER-INSPECT run — a click SPAWNS a labeled `[toolbar]`, the camera zooms out from a tight crop to the full page, then the cursor sweeps `[page elements]` while a floating `[inspector panel]` TRACKS the cursor, outline-highlighting and content-snapping per hovered element. (The slice's three-beat dark title prelude, scenes 1–3, belongs to `titlecard-reveal`, not here.)
- Hook: the ambient MULTI-CURSOR canvas — several labeled `[teammate cursors]` work a design canvas simultaneously (grab-drag-drop of components between mockups, recolor/identity swaps on drop) while the canvas group translate-PANS within a static frame and a `[headline]` builds word-group by word-group over the demo; the live workshop itself is the hook. One continuous beat, no cuts, no camera.
- Benefits (from `ui-demo-text-interlude-ui-demo`): the demo|text|demo SANDWICH — two static-stage demo beats of this blueprint bridge through a full-screen kinetic/title interlude and back (cursor acts, UI answers, all "zoom" element scale); the interlude beat is `kinetic-type-beats` material, and the sandwich itself is sequencing above the single-shot unit.

**duration**: 4.0–12.9s (Key_Feature 4.0–12.9s — the mined state tours run long, 10.4–12.9s, and the drag-drop journeys 9.8–10.6s, against the original 4.0–7.3s set; Product_Intro 4.5–9.3s — the low-event browse sets the 4.5s floor; Hook ~6.5s; the Benefits demo|text|demo sandwich totals 11.6–12.8s with each demo half ~4–5s)

**shot structure** (a `[product UI surface]` — fixed app window, dashboard/editor, parallax `[content card]` stack, or a `[container object/icon]` — centered over `[bg color/gradient]`, shown `[flat]` or `[3D-isometric]`; a custom `[brand-colored cursor with icon]` is the protagonist and the camera servos to whatever it touches; UI responds _live_ and in sync with each cursor action. Two role-tuned tempos fold in — Product_Intro **sweeps to introduce**, Key_Feature **performs a workflow** — and the camera spans a spectrum: the full CHASE, one continuous zoom-breathe, or a fully LOCKED static stage where the UI itself does all the moving.)

- **Scene 1 (0.0–~Xs) — surface establishes + first touch.** The `[product UI surface]` arrives centered over `[bg color/gradient]` — either it is simply present (fixed window / dashboard / editor), a 3D-parallax stack of `[content cards]`, or a `[container object/icon]` that FLIES IN with a 3D tumble and settles. The custom `[cursor]` enters. The cursor performs the FIRST action on `[cursor target 1]` and the UI responds live in the same beat. Camera holds or begins a slow push-in toward the acted-on region.
  - _Variant — Product_Intro_: low-commitment first touch — cursor HOVERS/sweeps a control or SWEEP-HIGHLIGHTS a field to `[accent color]`, OR the `[container]` fans open. An optional label/title fades/morphs onto the surface. The point is to _show the surface exists_ and is touchable.
  - _Variant — Key_Feature_: a concrete edit — cursor DRAGS a scrollbar / TYPES into a field / DRAGS a handle, and the UI responds materially (`[scroll]` / value climbs / region resizes). If the surface opened in `[3D-isometric]`, it may snap perspective-FLAT here to read the workflow.
  - _Variant — Key_Feature (static-stage tour)_: an optional Scene 0 — `[title card / kinetic brand word]` on a flat field — hard-cuts or window-SCALES-UP into the surface; the `[app UI]` is fully present from the first frame and the cursor enters and glides to the first control. The camera is LOCKED from the start and stays locked.
  - _Variant — Hook (ambient multi-cursor)_: no single protagonist — several labeled `[teammate cursors]` are already at work across `[N mockups]` on a design canvas; the canvas group translate-PANS within the static frame while a `[headline]` builds word-group by word-group over the top. One continuous beat, no cuts.

- **Scene 2 (~Xs–~Ys) — camera chases to the next interaction (the engine).** The camera MOVES to the next target — push-in + pan / whip-pan / pan-down to `[cursor target k]` — and the cursor performs action k as the UI updates live. Each beat is a discrete interaction connected by a fast camera move; the surface's inner content SWAPS per interaction.
  - _Variant — Product_Intro_: navigation is exploratory — a slow camera pan + depth-of-field FOCUS-PULL across a parallax `[content card]` stack, or the `[container]` fanning into `[N option/content cards]` that SPRING to position. As content swaps, the supporting backdrop STEPS its color (`[bg step 1]` → step 2 → …). Typically one or two such moves.
  - _Variant — Key_Feature_: repeat for `[2–4 beats total]`, each a distinct operation the UI answers — counter COUNTS UP, `[pill/swatch]` SELECTS, a modal SLIDES UP and TYPES — connected by whip-pans / progressive zoom. The workflow visibly advances toward a result.
  - _Variant — Key_Feature (static-stage tour)_: the camera never moves — every beat is a click-triggered ELEMENT response: a modal SPRINGS/scales up from center, a `[side detail panel]` SLIDES in from the right edge (a second panel may slide over the first), hamburger→sidebar slide-open, a settings panel HARD-swaps its content, a dropdown fills, a `[table]` populates row-by-row, a formula types into a cell and the range populates on enter, a type-to-filter list live-collapses, a `[block]` pops into the canvas, a node-graph BUILDS (cards + connecting lines radiate from center), a hover drops a `[popover]` below a tag. Any "zoom" is element scale of the UI only.
  - _Variant — Key_Feature (drag-drop)_: the cursor GRABS a `[field chip]` from an `[inputs sidebar]`, drags a semi-transparent GHOST across the page, and drops it — it SNAPS into a placed field with bounding box + corner handles; a completion beat follows (a `[modal]` springs up over the dimmed document, a name types letter-by-letter while a live `[cursive preview]` builds per keystroke, confirm click). The whole clip rides one continuous zoom-BREATHING arc (slow zoom-out / gentle zoom-in / final zoom-out) instead of discrete camera beats.
  - _Variant — Product_Intro (hover-inspect)_: the cursor's first click SPAWNS a labeled `[toolbar]`, the camera zooms OUT from a tight crop to the full page, then the cursor sweeps `[page elements]` — each hovered element gets an outline and a floating `[inspector panel]` TRACKS the cursor, its content snapping per element.

- **Scene 3 (~Ys–end) — payoff state, camera settles, HOLD.** The cursor lands on its final target and the screen reaches the payoff state; the camera comes to rest (static) and holds.
  - _Variant — Product_Intro_: the cursor HOVERS the hero element — a `[content card]` SCALES UP on hover, a node gets an `[Available]`-style pill, or a `[result card]` POPS/springs in — the "here's the product" payoff. Settles static, holds.
  - _Variant — Key_Feature_: locked close-up on the OUTCOME — cursor lands on the `[primary action button: Export / Save / Reimburse]` and a `[hover backdrop / highlight]` SPRING-pops in (the climax is the action button / produced result). Holds.
  - _Variant — Key_Feature (static-stage tour)_: optional detachable end beat — `[brand text beat / icon-ring lockup / end stat card]` — or the cursor simply comes to REST on the next target and holds (006_claudeai ends with the cursor on a panel's close X, the panel never closing).
  - _Variant — Key_Feature (drag-drop)_: close-up on the placed element ADJUSTED — a corner-handle drag proportionally resizes it — then the cursor sweeps toward the `[Finish / CTA]` as the clip ends.
  - _Variant — browse / hover-inspect_: no payoff lock at all — the shot ends MID-demo, cursor still roaming (browse and hover-inspect modes).

**motion vocabulary**: cursor-driven click / hover / sweep-highlight / drag / type; per-interaction live UI response (scroll, value climb, region resize, content swap); camera push-in + pan / whip-pan / pan-down servoing to each target; coordinate zoom onto the acted region; press-and-ripple on a clicked control; button press-compress; screen-state swap shot-to-shot; card fan-out to corners (spring); 3D container fly-in & tumble-settle; perspective-flatten (3D→2D snap); paginated/stepped backdrop color advance; depth-of-field focus-pull across a parallax card stack; counter count-up; pill/swatch select; modal slide-up + typing; label/title morph between states; UI-keyword highlight glow; terminal hover-scale or result-card pop-in; spring hover-backdrop on the final action button; hard panel swap (no easing); side detail panel slide-in from the right edge (second panel over the first); hamburger→sidebar slide-open; hover popover drop below a tag; element-scale fake zoom (UI window scales in/out on click, camera locked); table populates row-by-row; formula typed into a cell + instant cell-range populate on enter; fill-handle drag auto-fill down rows; type-to-filter list live-collapse; dropdown fill on click; block/element pop-in to canvas; node-graph build (cards + connecting lines radiate from center); character-by-character auto-typing with blinking caret; window scale-up with settle; ghost-chip drag (grip dots + icon) across the page; drop-snap into a placed field with bounding box + corner handles + trash icon; modal spring-up over a dimming document; letter-by-letter typing with a live cursive preview building per keystroke; corner-handle drag with proportional resize; continuous zoom-breathing single shot (zoom-out / zoom-in / zoom-out arcs); cursor sweep toward the CTA at clip end; multiple labeled collaborative cursors moving independently; cursor grab-drag-drop of components between mockups; element recolor/identity swap on drop; canvas-group translate-pan within a static frame; headline building word-group by word-group over the demo; hover-triggered micro content/sidebar update; click spawns a labeled toolbar; floating inspector panel tracking the cursor with per-element content snap; per-element hover outline highlight; motion-blur window fly-in; tight-crop open then zoom-out to full page; brand icon-ring end beat; 3D end-card float on the hold.

**rule mapping**

- viewport follows the cursor / camera servos to whatever it touches (primary) → `camera-cursor-tracking`
- cursor moves to a target, presses, emits a ripple (the click itself — primary interaction primitive) → `cursor-click-ripple`
- screen-state swap shot-to-shot (surface inner content changes between beats) → `scale-swap-transition`
- camera push-in + pan / whip-pan / pan-down to the next target → `viewport-change` (pan/zoom across the UI)
- sequencing the chase into discrete interaction beats → `multi-phase-camera`
- zoom onto the specific acted-on UI region → `coordinate-target-zoom`
- cursor icon/state changing with context (e.g. pointer↔grab over a draggable handle) → `context-sensitive-cursor`
- which content appears per beat / step-by-step UI state progression / per-interaction swaps → `dynamic-content-sequencing`
- sweep-highlight a field, highlight a UI keyword to `[accent color]` → `asr-keyword-glow` (keyword glow on the touched element)
- clicked button compresses on press, springs back on release → `press-release-spring`
- cursor + button compress together on a heavier press → `physics-press-reaction`
- panel/card morphs between two states (e.g. card → expanded card, surface state A → B) → `card-morph-anchor`
- terminal hover-scale, `[result card]` pop-in, spring hover-backdrop on the final action button → `spring-pop-entrance`
- card fan-out to corners / option cards springing to position → `split-tilt-cards` (fan/spread into tilted positions) + `spring-pop-entrance` (the spring settle)
- 3D-parallax content-card stack as the surface; UI shown 3D-isometric → `3d-page-scroll` (UI as a tilted scrolling/parallax card)
- node gets an `[Available]`-style pill / tracked badge appears on an element → `ai-tracking-box`
- counter / value count-up as the UI responds → `counting-dynamic-scale`
- a result bar / number FILLS as the workflow's outcome → `stat-bars-and-fills`
- a live `[video]` screen-capture clip used as the surface → technique: video compositing
- perspective-flatten (3D-isometric → flat 2D snap) and the 3D-isometric tilt itself → technique: CSS-3D (no dedicated rule; the tilt/flatten transform is a CSS-3D primitive)
- camera settles static on the payoff and HOLDS → (settle phase of `spring-pop-entrance` on the payoff element; the static hold itself needs no rule)
- 3D container/object fly-in & tumble-settle → `depth-scatter-assemble` (free-tumbling 3D object/container entrance that flies in and tumble-settles; `orbit-3d-entry` only orbits a flat element into place)
- depth-of-field focus-pull across the parallax card stack → `depth-of-field-blur` (rack-focus / DoF blur transition between near and far cards; `3d-page-scroll` supplies the tilted parallax stack and `viewport-change` the pan)
- paginated/stepped backdrop color advance synced to interactions (`[bg step 1]`→step 2→…) → `discrete-text-sequence` (discrete state stepping, here applied to a background-color state rather than text)
- modal slide-up + in-modal typing as one combined beat → `card-morph-anchor` / `scale-swap-transition` (the panel slide-in) + `discrete-text-sequence` (the in-modal typed text)
- element-scale fake zoom — the UI window scales, camera locked (static-stage tour) → `coordinate-target-zoom` (applied to the surface wrapper rather than the world)
- side detail panel slide-in from the right edge / hamburger→sidebar slide-open / hover popover drop → `card-morph-anchor` / `scale-swap-transition` (the panel arrival) + `dynamic-content-sequencing` (which content each panel shows per beat)
- hard panel swap / in-panel content snapping through states / hover-triggered micro update / type-to-filter live-collapse / element identity swap on drop → `dynamic-content-sequencing`
- table populates row-by-row / fill-handle auto-fill cascading down rows / log rows cascade in → `waterfall-entry`
- formula typed into a cell / character-by-character auto-typing with blinking caret / letter-by-letter typed name → `discrete-text-sequence` + `context-sensitive-cursor` (the caret)
- node-graph build (cards + connecting lines radiate from center) → `center-outward-expansion` (the cards) + `svg-path-draw` (the connecting lines draw)
- click spawns a labeled toolbar / dropdown fills on click / drop-snap settle of the placed field / window scale-up with settle → `spring-pop-entrance`
- modal spring-up over a dimming document → `spring-pop-entrance` (the modal) + `depth-of-field-blur` (the document dim/blur beneath)
- ghost-chip drag-and-drop / cursor grab-drag of components between mockups / fill-handle drag / corner-handle resize drag → `cursor-drag` (`cursor-click-ripple` covers move+click only)
- floating inspector panel TRACKS the cursor, content snapping per element → `ai-tracking-box` (the per-frame follow mechanics, restyled as an inspector panel) + `dynamic-content-sequencing` (the per-element content)
- live cursive preview building per typed keystroke → `svg-path-draw` (progressive stroke reveal keyed to typing progress)
- continuous zoom-breathing single shot (drag-drop variant) → `multi-phase-camera` (pull-back / focus / push phases + micro-drift)
- motion-blur window fly-in / tight-crop open then zoom-out to full page → `motion-blur-streak` (the fly-in) + `viewport-change` (the zoom-out)
- multiple labeled collaborative cursors moving independently → `multi-cursor-choreography` (N labeled independent cursor actors; the single-actor cursor rules assume one)
- canvas-group translate-pan within a static frame → `viewport-change` (the `.world` translate realizes the pan; semantically the camera stays locked)
- headline builds word-group by word-group over the demo → `waterfall-entry`
- brand icon-ring end beat → `svg-path-draw` (the ring) + `spring-pop-entrance` (the lockup)
- 3D end-card float on the hold → `sine-wave-loop` — CAUTION: motion-doctrine bans idle wobble; prefer a settle-and-hold

**camera modifier**: The defining motion is the camera CHASE — the viewport follows the cursor from target to target via `camera-cursor-tracking` (primary), realized as concrete push-in + pan / whip-pan / pan-down moves under `viewport-change`, sequenced into discrete interaction beats by `multi-phase-camera`, with each beat's destination targeted via `coordinate-target-zoom` (zoom to the acted-on region). Product_Intro biases toward a slow, exploratory pan + focus-pull that sweeps the surface; Key_Feature biases toward snappier whip-pans / progressive zoom that march through the workflow and lock static on the action button. This camera-servo-to-cursor is what separates the blueprint from hands-off camera scrolls (dataviz-scroll-reveal) and static device/window tours. The golden set widens this into a spectrum. At one pole the **static-stage state tour** (now the largest member set) LOCKS the camera for the entire clip and lets the UI itself do all the moving — panel slide-ins, element-scale fake zooms, content snaps — with the cursor alone carrying the eye. The **drag-drop** variant replaces discrete chase beats with ONE continuous zoom-breathing arc under `multi-phase-camera`. The **hover-inspect** variant inverts the push-in: a tight-crop open zooms OUT to the full page before the cursor sweep. Pick the pole per brief — chase for workflow marches, locked stage for dense reconstructed dashboards, a single breathe for one-document journeys. With the locked pole absorbed, what separates this blueprint from `device-surface-showcase` is the CURSOR-as-actor, not the camera: a fully static tour still belongs here as long as a visible cursor drives every state change.


<!-- ===== FILE: hyperframes/hyperframes-animation/blueprints/dataviz-countup.md ===== -->

# dataviz-countup — Data-Viz / Count-Up

**intent**: Make numbers and charts the hero — a count-up ring/number, a trend chart, a tilted stat/card grid — and traverse the data instruments with a camera that pushes THROUGH them (or scrolls across them) to land on one hero metric, so the data itself carries the argument.

**roles served**

- Problem (from `problem-dataviz-pushthrough`): quantifies the pain with real-looking instruments — a count-up ring → a trend chart → a stat grid — the camera pushing THROUGH each object into the next to dramatize a worsening / large-scale problem ("X% of people struggle with…").
- Product_Intro (from `product-intro-dataviz-scroll-reveal`): a confident "look at the result / the data" open — hard-cut from a hook word into a perspective-tilted grid of data-viz cards, then a hands-off camera scroll lands one glowing hero metric while a kinetic tagline assembles word-by-word.
- Hook (from `hook-counter-burst`): a cold-open hook on ONE dramatic statistic — the frame opens dark and empty, 3–5 thematic icons puncture in clustered at center, then the headline number EXPLODES upward in size as the icons fling outward to their marks (the count-up and the spread are one beat), closed by a slow camera lean-in. Kinetic from frame 1.
- Key_Feature (from dark-stat-scrub-montage): prove the feature with its own analytics — on a black canvas, kinetic headline beats alternate with self-drawing charts and a 3D-tilted dark dashboard that a cursor SCRUBS (tracking line + live tooltips), stitched by hard cuts and one zoom punch. The one variant where a cursor touches the data.
- Social_Proof (from `gauge-beat`): a single count-up instrument — radial gauge arc-draw + rapidly ticking metric + caption — embedded as ONE BEAT inside a kinetic-typography relay; entered and exited by element-level scale/blur push-throughs on a static frame. The instrument guest-stars; the relay itself belongs to kinetic-type-beats.

**duration**: ~4–12s (Hook ~4s · Product_Intro ~6s · dark-scrub-montage ~7.3–7.75s · Problem ~11–12s · gauge-beat ~2.5s inside a ~10.8s relay)

**shot structure** Data-viz field on `[bg color]` (dark or light, soft corner glows); `[gradient A→B]` brand stroke on charts/rings; clean sans-serif white/dark text; a continuous camera move runs underneath that traverses 2–3 data instruments and resolves on a hero metric. One instrument per beat; the camera carries the cut.

- Scene 1 (0.0–Xs): the first data instrument establishes centered — a `[stat]` reads as the hero. A bold center number COUNTS UP `[start]`→`[end]` while its transform scale grows to the static final type size, with `[stat label]` below; its paired graphic (a circular progress RING sweeping to `[pct]` with a `[gradient]` stroke, or a bar/fill) animates in on the SAME ease so number + graphic land as one beat. Supporting `[avatar/object]` elements pop in with spring overshoot into a scattered glowing orbit; a `[headline]` fades up. A very slow continuous camera zoom-in runs throughout.
- Scene 2 (Xs–Ys): the camera traverses to the next instrument and that instrument animates — a `[gradient]` trend line / area chart DRAWS left→right on grid lines (Problem), or off-center cards SCROLL away as the layout glides (Product_Intro). The arriving `[stat-2]` number counts up / the chart resolves.
- Scene 3 / Scene N (…–end): the camera lands the `[hero metric card]` (big number + label + delta + rising chart) in dead-center; a soft `[accent]` glow blooms behind it; the move reaches its peak then eases to a settled, slightly wider composition with the hero centered and supporting cards flanking it. HOLD on the final frame.

- Variant — Problem (push-THROUGH, count-up → trend → grid): Scene 1 is a centered circular progress ring + count-up center number with scattered glowing `[avatar/object]` orbit. Scene 2 is a fast camera PUSH-IN straight through the center of the ring (ring, number, orbiting elements scale up and fly out of frame) into a rounded `[card]` holding `[stat-2 header]` over a `[gradient]` line chart with grid lines + translucent area fill that draws left→right; camera pushes through then settles. Scene 3: camera PANS to a second `[card]` whose number counts up, holding a grid of the `[avatar/object]` elements — a subset dim/blur while the rest receive `[accent]` circular checkmark badges that SPRING-POP; camera settles to the end. The traversal is z-depth push-through between instruments.
- Variant — Product_Intro (scroll-to-hero + word-by-word tagline): a brief opener — Scene 0 (~0.0–0.85s): a full-frame `[hero-color orb]` with a bold white `[hook phrase]` over it; static shimmer, then HARD CUT. Scene 1 cuts to a slightly perspective-TILTED grid of `[data-viz / product cards]` (charts, heatmaps, stat cards with deltas + source footers) with `[tagline word 1]` centered; the grid begins SCROLLING (e.g. toward upper-left) with its tilt held. Scene 2: the grid keeps scrolling so the `[hero metric card]` glides into dead-center as off-center cards slide away; `[tagline word 1]` translates out and `[word 2]` rises in from a frame edge. Scene 3: hero card settles centered, `[accent]` glow blooms behind it, camera PUSHES IN slightly; `[word 2]` holds near it. Scene 4: `[word 2]` slides out, the final `[tagline word]` drops in from the opposite edge above the still-glowing hero, push-in peaks. Scene 5: overlay type clears, camera eases BACK OUT to a settled wider tilted composition — hero centered with glow, supporting cards flanking. The traversal is a hands-off camera SCROLL across a tilted card plane (no cursor, no clicks) + a one-word-at-a-time kinetic headline + push-in-then-out bookend.
- Variant — Key_Feature (dark-scrub-montage: kinetic beats × instruments, cut-stitched): on black, `[kinetic word]` beats ALTERNATE with data instruments; hard cuts stitch the beats and the camera is locked per beat — the traversal is a montage, not a continuous move. Beat A: a bold `[heading]` holds while a thick `[trend line]` DRAWS itself left→right inside a dark chart band, rising to break above the band's edge; at the peak a `[accent]` dot pops and a pill tooltip springs in, its label building to `[value + delta]`. Beat B: ONE fast zoom PUNCH lands a close-up, slightly 3D-tilted dark `[analytics dashboard]` (metric cards with deltas, translucent oversized numerals floating behind); a white cursor SCRUBS a chart — a vertical tracking line follows it and `[date: value]` tooltips read out live, then a second chart ACTIVATES with a color flip and its own scrubbing tooltip — while the tilted plane drifts gently sideways; quick pull-away/fade to black. Beat C: a `[glowing wave / typed line / impact word]` beat lands the closing stat LOCKUP — `[title]` + big `[stat]` counting up + `[green delta arrow + context line]` — and holds static to the end. Kinetic words between instruments scale up violently past the frame as element-level push-through transitions (no camera).
- Variant — Social_Proof (gauge-beat inside a relay): a static-camera kinetic-type relay hosts ONE instrument beat — thin concentric `[accent]` arcs radiate from center, a thick `[accent]` progress arc draws clockwise over them, a large `[metric]` rapidly ticks up to `[big value]` with a `[caption]` below; the group slowly scales up (element-level drift), then hard-cuts out to the next text beat. Entry/exit for every beat is scale-up-from-blur in / scale-up-and-blur-past-frame out — a fake push-through with no camera anywhere. Use when social proof is one number and the surrounding beats are typography.

**motion vocabulary** count-up number with transform-scale growth on the value; circular progress-ring sweep; growth bar / progress fill; gradient trend-line + area-fill left→right draw; spring-overshoot pop-in of scattered glowing avatar/object elements; perspective-tilted card grid; directional grid scroll (cards glide in/out of center); hero-card centering; soft accent glow bloom behind the hero; slow continuous zoom-in; fast camera push-IN / push-THROUGH the center of an instrument; lateral/vertical camera pan between cards; gentle push-in that peaks then eases back out to a wider settle; selective dim/blur of a subset + spring-pop checkmark badges; full-frame hook orb → hard cut; kinetic tagline assembled word-by-word (each word drops/rises from a frame edge, prior word slides out). Dark-scrub-montage additions: self-drawing chart line that breaks above its band; peak dot + pill tooltip spring-pop; cursor chart scrub with vertical tracking line + live date/value tooltip readouts; chart activation color flip; 3D-tilted dark dashboard plane with slow lateral drift; translucent oversized numerals floating behind cards; fast zoom punch-in; pull-away/fade-to-black beat exit; hard-cut beat stitching; kinetic word push-through (element scales up past the frame); typed line with blinking cursor; impact slam word + particle-dissolve punctuation; glowing wave draw; green delta arrow pop; stat lockup hold. Gauge-beat additions: concentric static arcs + thick clockwise progress-arc draw; rapid count-up tick; scale-up-from-blur entrance / scale-up-and-blur-past-frame exit (element-level fake push-through).

**rule mapping** (motion verb → `rules/<id>.md`)

- count-up number whose transform scale grows with the value → `counting-dynamic-scale` (primary text rule)
- circular progress-ring sweep (the ring fill) → `stat-bars-and-fills` (ring form) — its draw mechanics delegate to → `svg-path-draw`
- growth bars / progress fill paired beside a number → `stat-bars-and-fills` (primary data rule)
- gradient trend-line / area-chart left→right draw → `svg-path-draw` (a path/line draws itself)
- spring-overshoot pop-in of the avatar/object elements → `spring-pop-entrance` (elastic overshoot); the scattered-ring layout of glowing avatars/objects → `avatar-cloud-network`; if they keep drifting/orbiting → `orbit-3d-entry`
- spring-pop `[accent]` checkmark badges → `spring-pop-entrance`
- perspective-tilted card grid (tilt held static while content moves) → `3d-page-scroll`
- directional scroll across the tilted card plane (cards glide in/out of center) → `3d-page-scroll` (scroll) + `viewport-change` (lateral/vertical pan form)
- hero metric card centering (scroll/pan lands the target dead-center) → `coordinate-target-zoom` (target lands at viewport center) / `viewport-change`
- hard-cut from the hook orb into the grid → `scale-swap-transition`
- kinetic tagline assembled word-by-word → `kinetic-beat-slam` (one onset grid, distinct per-word entrances)
- slow continuous zoom-in + push-THROUGH the instruments + lateral/vertical pan between cards + push-in-then-out bookend → `multi-phase-camera` (see camera modifier)
- soft accent glow BLOOM behind the hero card → `ambient-glow-bloom` (un-triggered soft glow/bloom behind the static hero element — distinct from `press-release-spring`'s press-triggered glow and `asr-keyword-glow`'s word-timed envelope)
- selective dim/blur of a SUBSET of grid items (focus-falloff on the non-highlighted cards) → `depth-of-field-blur` (selective per-element blur/dim to spotlight the highlighted cards — the same focus-falloff rule used in `constellation-hub`)
- cursor chart scrub (cursor-tied vertical tracking line + live data readout in a tooltip) → `chart-scrub-readout` (the tracking line, tooltip pop, and seek-safe live value readout driven by cursor x)
- chart activation color flip (second chart lights up under the scrub) → `gsap-effects` (color/opacity chord at the scrub handoff — basic tween, no dedicated rule needed)
- 3D-tilted dashboard plane + slow lateral drift → `3d-page-scroll` (the tilt framing) + `sine-wave-loop` (the drift; keep amplitude tiny so the scrub stays legible)
- fast zoom punch-in to the dashboard → `multi-phase-camera` (one short aggressive push phase) aimed via `coordinate-target-zoom`; add `motion-blur-streak` at peak velocity
- kinetic word push-through / scale-up-and-blur-past-frame exit / scale-up-from-blur entrance → `kinetic-beat-slam` (the beat grammar) + `motion-blur-streak` (blur peaks at max speed, resolves at the settle — its entrance form runs the blur-in, its exit form the blow-past)
- typed line with blinking cursor → `discrete-text-sequence` + `context-sensitive-cursor` (square-wave blink)
- impact slam word → `kinetic-beat-slam`; its particle-dissolve punctuation → `particle-burst` (glyph→particles dissolve, deterministic)
- glowing wave draw → `svg-path-draw` (the draw) + `ambient-glow-bloom` (the glow envelope)
- green delta arrow pop / peak dot + pill tooltip → `spring-pop-entrance`
- concentric static arcs + clockwise progress-arc draw (gauge beat) → `stat-bars-and-fills` (ring form) → draw mechanics `svg-path-draw` (both already mapped above — the gauge is the existing ring with static concentric chrome behind it)

**camera modifier**: The camera is the through-line that traverses the data instruments — one camera wrapper sequenced by `multi-phase-camera`, with each stop targeted via `coordinate-target-zoom` onto the focal instrument/card.

- Problem — push-THROUGH: a slow continuous zoom-in (drift overlay) plus a fast PUSH-IN straight through the center of one instrument into the next (`multi-phase-camera`, Steady-push pattern), then a lateral/vertical PAN to the final card. Z-depth push-through is the signature (distinguishes it from a flat pan-tour).
- Product_Intro — scroll-to-hero + bookend push: a hands-off directional SCROLL across the tilted card plane (`3d-page-scroll` scroll / `viewport-change` pan) that lands the hero card center, then a gentle push-in that PEAKS and eases BACK OUT to a wider settle (`multi-phase-camera`, Bookend-pull pattern). No cursor, no clicks — the camera does the navigating.
- Key_Feature — montage-cut: the camera is NOT the through-line — hard cuts stitch the instrument beats, the frame is locked inside each beat, and exactly ONE fast zoom punch (`multi-phase-camera` single push phase + `coordinate-target-zoom`) lands the dashboard close-up; exits are pull-away/fade-to-black. Between instruments, ELEMENTS fake the push: kinetic words scale up past the frame (`kinetic-beat-slam` + `motion-blur-streak`). Gauge-beat form drops even the punch — fully static, all push-through element-level. Reach for this mode when the dialect is a dark rapid montage; the Problem/Product_Intro modes remain the default for a single continuous argument.


<!-- ===== FILE: hyperframes/hyperframes-animation/blueprints/device-surface-showcase.md ===== -->

# device-surface-showcase — Device / Surface Showcase

**intent**: A product surface — a device mockup or a floating browser/app window — is the hero held in frame while its screens cycle through a real flow, showcased by a camera move that ranges from a static hold to a continuous 3D push.

**roles served**

- Key_Feature (from key-feature-device-screen-tour, key-feature-floating-window-scroll, key-feature-3d-device-hand-demo): show a feature being \_experienced inside its real interface\* — the surface houses the action and its screens advance through a flow, rather than enumerating tiles or chasing a cursor across a workflow. (Note: the three founding drafts are Key_Feature and variants differ by MECHANIC, not role; the mined stepwise-flow variant widens the blueprint to Product_Intro.)
- Key_Feature (from demo-page-scroll-spotlight): the floating-window push-scroll variant carried to a spotlight climax — a real webpage rendered as a tilted 3D card coasts in (power2, like a phone held up — no spring), header keywords flare on a karaoke glow as the VO names them, the page rolls to the demoed section, and one element LIFTS off the surface (translateZ + scale) under a radial spotlight that dims the rest.
- Product_Intro (from stepwise-flow-completion): a compact end-to-end product flow — setup/auth → action → success/confirm — plays out cursorless as successive screen states inside the held surface, capped by a confirming button press; bookended by title-card beats. The surface introduces the product by \_completing its core loop\*, not by touring screens.
- Key_Feature (from `showcase-carousel`): the showcase-carousel — two surfaces in sequence (a widget card cycling brand skins, a phone frame with app screens sliding through it) gated by interstitial claim words; the screen cycle is a breadth carousel ("N brands / N apps"), not a flow.

**duration**: 5–11.3s (page-scroll-spotlight 5–9s · floating-window 7.8s · 3d-hand 7.9s · in-device approval 7.9s · stepwise-flow 8.5–9.4s · device-tour 9.6s · showcase-carousel 11.3s)

**shot structure** One product surface — a `[device mockup]` or a `[floating browser/app window]` — is the persistent hero on a `[styled backdrop: gradient / radial / stylized 3D void]`; its `[screens/sections]` cycle through a real `[product flow]` while a showcase camera (static-hold, push-in→zoom-out, or one continuous push) presents it. Each screen state holds ~1.0–1.5s.

- Scene 1 (0.0–~1.5s): The surface ESTABLISHES — it `[slides in from an edge / drifts in from a tilt / dissolves from a full-frame title card]` and settles, with a `[accent shape or backdrop]` resolving behind it; the first `[screen]` is visible. The showcase camera begins (see variants).
- Scene 2 (~1.5–~Xs): The surface is OPERATED on its own face — a `[tap/select/scroll]` triggers the first screen advance: old content `[pushes out / scrolls up]`, new `[screen/section]` `[pulls up / pushes in from the side]`; concurrently a `[label / header word / side headline]` updates. The camera continues its move.
- Scene 3+ (~Xs–end, repeat for `[2–4 screen beats]`): The surface ADVANCES through successive `[screens/sections]`, each a discrete swap or scroll synced to the surface's flow, while the secondary copy `[swaps out-up / in-up]` or stays marked to hold reading position. HOLDS on the final `[screen]` (or, for one variant, blooms out — see variant).

- Variant — static-tour (key-feature-device-screen-tour, 9.6s): a `[device mockup]` slides in from off-screen and settles (ease-out); an `[accent-color shape]` scales up behind it (spring overshoot). Camera STAYS STATIC the entire clip — all motion is element/UI-level: a tap COMPRESSES a button (95%→100%), the UI scrolls/transitions to the next view (old pushes out, new pulls up), and a `[side headline]` SWAPS beside the device (old slides up + fades, new slides up + in) per screen. Holds on the final screen. No camera move, no cursor.
- Variant — floating-window (key-feature-floating-window-scroll, 7.8s): OPENS on a full-frame `[title card]` (a small `[icon]` draws in at center, `[feature name]` below; holds ~2s), which DISSOLVES to a `[macOS-style browser/app window]` floating on a `[vivid gradient]` (traffic-lights + `[URL pill]` + tabs; left nav, central content, right `[sidebar]`). Camera PUSHES IN on a `[target region/sidebar]` (active item highlighted `[accent]`, a cursor drifts down the list), then ZOOMS BACK OUT to re-frame the whole window while the content SCROLLS through `[sections]`; the `[highlighted item]` stays marked. One push-in→zoom-out arc, gated by the title-card opener.
- Variant — 3d-hand (key-feature-3d-device-hand-demo, 7.9s): FULLY 3D — a `[3D device]` drifts in a `[stylized 3D void / bloom + particles]`, opening tilted and self-rotating to face the lens nearly flat as ONE CONTINUOUS forward camera push begins (no cuts). A glossy `[3D hand]` rises from the bottom-foreground and GESTURE-DRIVES the surface: it swipes to scroll a `[picker/sidebar panel]` of `[option cards]` and taps `[option]` (while a `[header word]` letter-flips in place); the selection APPLIES — a `[new layout]` grows from center to fill the device face, nav flips, a `[marquee]` scrolls horizontally; the hand swipes again to scroll the page upward through `[sections]`, then drifts out. The camera never stops pushing; the bright device face keeps growing toward the lens until it BLOOMS into a `[light]` wash — a zoom-through "portal" exit that fills the frame.
- Variant — stepwise-flow (Product_Intro, 8.5–9.4s; in-device Key_Feature sub-mode 7.9s): CURSORLESS end-to-end flow — the surface completes `[setup/auth → action → success]` as a narrative arc. Opens on a `[title card]` that fades in/out on an ambient gradient (or a typed `[command]` running character-by-character on a terminal field). The `[flow surface]` arrives (phone mock slides up oversized and settles / bordered log panel replaces the command) and step 1 completes via rapid sequential pops — `[OTP digits]` fill boxes left-to-right capped by a green check, or `[log steps]` pop top-down with highlighted tokens, ending on a trailing-dots waiting state. State advances laterally (old content slides out left, new in from right, chrome persists) or via a dark-to-light scene swap into a white `[detail/confirm card]` whose elements stagger in. COMMIT: the `[CTA button]` is pressed (press dip / spinner "Processing") and a `[success state]` renders with check bullets — in the in-device sub-mode the commit runs a biometric ritual: dim overlay, `[squircle]` spring-pops, a ring draws around an icon, the icon morphs to a checkmark and holds; a slight camera push-in fires ONLY at the state transition (camera punctuates the commit, then re-locks). EXIT: the surface leaves and closing `[title cards]` pop in and ease smaller — the surface exits before the coda instead of holding. Camera otherwise static. For this variant the persistent hero is the FLOW, not one surface: a terminal panel may hand off wholesale to a confirm card.
- Variant — showcase-carousel (Key_Feature, 11.3s): TWO surfaces in sequence on a slowly drifting `[pastel mesh gradient]`, static camera, gated by centered interstitial `[claim words]` (fade in with gentle scale-up, fade out). Act 1: a white `[widget card]` scales in, flips/morphs into a tilted vertical widget and CYCLES `[N brand skins]` (~0.8s each) — one shared layout, per-skin content and accent swaps — while a large `[brand logo]` crossfades below per flip; the widget scales away. Act 2: a `[phone frame]` enters oversized and tilted, settles upright at center; full `[app screens]` slide left through it (~1s each), holding on the last. The screen cycle is a breadth carousel, not a flow — no taps, no cursor, no camera.

**motion vocabulary** surface establish (edge slide-in + settle / tilt drift-in + self-rotate-to-camera / title-card dissolve); accent shape spring behind surface; element-level screen-cycling (scroll-swap, push-in-from-side, scale-swap); button tap-compress; staggered side-headline reveal + copy swap (out-up / in-up); in-place header-word letter-flip; floating browser-window-on-gradient idle float; full-frame title-card opener (icon draw-in + label); camera push-IN on a region; camera zoom-OUT re-frame; content scroll-through; one continuous 3D camera-follow push (no cuts); 3D device drift + self-rotate; stylized-environment bloom/particles; 3D-hand entrance + swipe-scroll + tap (gesture-driven); picker-panel slide-in; template-apply grow-from-center; horizontal marquee scroll; gesture-driven page scroll; zoom-through bloom/portal exit; static-hold (no camera) as the floor of the camera range. Stepwise-flow additions: title-card bookends (fade-in/out opener; closers pop in then ease smaller); typed terminal command with prompt chevron; sequential top-down log pops with sub-line reveals; animated trailing-dots wait state; sequential digit pops left-to-right + green check confirm; lateral screen slide with persistent chrome; dark-to-light scene swap; staggered card element build-in (fade + slide-up); button press dip + fill flip; spinner processing state; success check-bullet reveal; notification banner spring-in with overshoot; lockscreen fade/blur-away as a card expands to fill the device face; commit-synced micro push-in; dim overlay; squircle spring pop; circular ring draw; icon morph to checkmark; surface exit before a title coda. Showcase-carousel additions: interstitial claim-word gate; brand-skin cycling with per-flip logo crossfade; card flip/morph into a tilted widget; oversized-tilted surface entry settling upright; fast slide-left screen carousel inside a static frame; drifting mesh-gradient backdrop.

**rule mapping** (per motion verb → backing rule, or flagged special)

- screen-cycling — UI scrolls/sections scroll inside the surface (device-tour, floating-window scroll, 3d-hand page scroll) → `3d-page-scroll` (webpage/app as a tilted card whose content `translateY`-scrolls to sections; primary mechanic for the surface's screen flow)
- floating-window establish + the surface presented as a tilted/floating UI card → `3d-page-scroll` (the tilt/perspective framing) + `css-3d-transforms` (perspective/`translateZ` depth)
- screen / side-copy state swaps (discrete screen states; side headline content swapping per beat) → `discrete-text-sequence`
- side-headline reveal (staggered fade + slide-up) → `discrete-text-sequence`
- in-place header-word letter-flip (3d-hand) → `hacker-flip-3d`
- screen swap as a coordinated shrink-out / pop-in between two screen states → `scale-swap-transition`
- template-apply "new layout grows from center to fill the face" (3d-hand) → `center-outward-expansion` (clustered-at-center → expand to fill)
- the surface morphing between states / title-card→window dissolve as the eye-anchor transition → `card-morph-anchor`
- button tap-compress (95%→100% press feedback) → `press-release-spring` (or `physics-press-reaction` for a heavier press)
- floating-window cursor click on the highlighted list item → `cursor-click-ripple`
- accent-highlight pop on the active sidebar/list item → `asr-keyword-glow` (accent glow on the focused item)
- drifting cursor down the sidebar list (floating-window) → `camera-cursor-tracking` (flat-cursor drift; pairs with the push-in)
- floating browser-window idle float / 3D device drift-breathe → `sine-wave-loop`
- 3D device drift + self-rotate-to-camera + perspective depth (3d-hand) → `css-3d-transforms` (CSS-3D) **or** `3d.md` technique (true Three.js/R3F device); see camera modifier
- horizontal `[marquee]` scroll (3d-hand) → `viewport-change` (PAN mode on the marquee strip) — _thin fit; a literal CSS-marquee/translateX loop is closer to a `gsap-effects`/CSS recipe than a named motion rule_
- 3D-hand entrance + swipe + tap as the interaction DRIVER (gesture input that scrolls/selects) → **flagged special — needs a heavier capability beyond the rule library (R3F/Three.js + WebGL), NOT a motion-shape rule.** The 3D hand model + WebGL bloom have a _technique_ backing (`3d.md` — R3F, `useGLTF` HandModel, `--gl=swiftshader` for the shader/bloom), but no motion-shape rule models a 3D hand as the swipe-to-scroll / tap-to-select gesture protocol. `context-sensitive-cursor` / `camera-cursor-tracking` only model a flat typing/pointer cursor, not a 3D gesturing hand.
- zoom-through bloom / portal exit (3d-hand) → **flagged special — needs a heavier capability beyond the rule library (WebGL), NOT a named transition rule.** Capability is `techniques.md` → WebGL shader (via `3d.md` headless WebGL: `--gl=swiftshader --concurrency=1`), but no named transition rule covers a bloom/portal fly-through.
- typed terminal command / non-linear log text (stepwise-flow) → `discrete-text-sequence` (typing + threshold state replacement) with `dynamic-content-sequencing` computing each step's window from content length
- sequential top-down log pops / OTP digit pops left-to-right / staggered confirm-card build-in → `spring-pop-entrance` (staggered group form; low overshoot for log lines)
- trailing-dots wait state → `sine-wave-loop` (finite repeats; step the opacity of 3 dots on a shared phase)
- lateral screen slide with persistent chrome → the existing screen-cycling mapping (`3d-page-scroll` translateX form inside the clipped surface); chrome sits outside the sliding layer
- notification banner spring-in / squircle pop (in-device) → `spring-pop-entrance`
- lockscreen fade/blur-away + card expands to fill the device face → `card-morph-anchor` (uniform-scale container morph — never tween width/height) + `depth-of-field-blur` (the blur-away)
- commit-synced micro push-in (camera punctuates the Approve/tap, then re-locks) → `multi-phase-camera` (single short push phase placed at the state transition)
- button press dip + fill flip / Approve press-down spring-back → `press-release-spring` (already mapped; the fill flip is its color-transition variation)
- spinner processing state → `svg-icon-enrichment` (rotating internal element with explicit SVG center)
- success check bullets / biometric ring draw → `svg-path-draw` (check strokes; ring rotated −90° to start at 12 o'clock) + `spring-pop-entrance` for the bullet pops
- icon morph to checkmark (biometric ritual) → **flagged special — SVG path morph, see hyperframes-keyframes (morph)**; no motion-shape rule models it — mechanics live in `techniques.md` / the keyframes skill, same tier as the blueprint's existing WebGL flags
- interstitial claim-word gate (fade + gentle scale-up, then out) → `gsap-effects` (plain fade/scale chord; deliberately quieter than `kinetic-beat-slam`)
- brand-skin cycling with per-flip logo crossfade → `discrete-text-sequence` (whole-state content replacement at thresholds) + `scale-swap-transition` where a flip reads as shrink-out/pop-in; the card→tilted-widget flip/morph → `card-morph-anchor` + `css-3d-transforms`
- drifting mesh-gradient backdrop → `sine-wave-loop` (very-low-amplitude position/hue drift on gradient blobs)

**camera modifier**: The showcase camera spans a RANGE keyed by variant, all on a single content-wrapping virtual camera (`viewport-change`):

- static-tour → NO camera move (`viewport-change` held at scale 1, or omitted); all motion is element-level. This is the floor of the range and what distinguishes the device-tour from the rest.
- floating-window → a two-phase push-in → zoom-out arc → `multi-phase-camera` (e.g. dramatic-reveal 1.1→1.0→0.95 feel): push IN on the `[sidebar/region]` via `coordinate-target-zoom` (off-center target = scale + counter-translate), then `multi-phase-camera` zooms back OUT to re-frame the whole window while content scrolls.
- 3d-hand → ONE continuous forward push (no cuts) → `multi-phase-camera` in steady-push mode (1.0→1.03→1.06… plus its sine micro-drift) layered over `css-3d-transforms`/`3d.md` so the device self-rotates-to-lens during the push; the push runs unbroken into the bloom/portal exit (exit itself is the WebGL-shader flagged special above). Across all three: `viewport-change` is the base virtual-camera primitive; `multi-phase-camera` sequences the push/zoom phases (and supplies the always-on micro-drift that keeps even the "static" tour from feeling dead); `coordinate-target-zoom` aims the push at off-center screen detail.

**Overflow (pan/scroll surfaces — required for a clean `check`):** a panned or scrolled surface deliberately moves content PAST the edges of its framing card. Clip it at the card (`overflow: hidden` on the card/window) AND mark the moving inner layer (the `.world` / surface wrapper holding the screenshot + any markers/labels) with `data-layout-allow-overflow` — otherwise `check` reports `text_box_overflow` / `container_overflow` errors for the parts that scroll off (e.g. a marker label panned off the left edge). The card clips them visually; the attribute tells the layout audit it's intentional, not a layout bug.


<!-- ===== FILE: hyperframes/hyperframes-animation/blueprints/fixed-anchor-cycle.md ===== -->

# fixed-anchor-cycle — Fixed Anchor, Cycling World

**intent**: One element is PINNED — a wordmark, a composer box, an anchor line that enters once and never moves again — while the adjacent region (or the entire surrounding theme) cycles through many discrete states around it, cadence often manipulated (steady stepping, a fast carousel, or a slow→accelerating flurry), resolving on an emphasis beat into a completed lockup or a muted freeze. The stillness of the anchor IS the claim: everything changes, this stays. Distinct from `kinetic-type-beats` sub-shape A, where a word-slot inside a centered line swaps and the sentence itself is the subject — there the anchor is a sentence frame on a bare type field; here the anchor is the PRODUCT identity and what cycles around it can be non-text (whole theme skins, chrome/logo swaps, textured label chips, a carousel list), the cycle asserts breadth ("everyone says / works everywhere / calling all X"), and the resolve completes the anchor into a lockup. Distinct from `ticker-takeover`, whose cycle ends in a collision — a hero crashes in and shoves the text aside; here nothing ever collides with the anchor: the cycle stops, and a final element quietly joins it.

**roles served**

- Brand_Outro (from `static-anchor-rapid-text-swaps`): when the sign-off is the brand name sitting immovable while praise quotes / tagline words cycle beside or beneath it — steady per-word highlight stepping, or a hard-cut chip flurry that accelerates — landing on the finished lockup ("bolt.new / prompt, run, edit, deploy / enjoy."; "Opus 4.6 by ANTHROP\C").
- Benefits: when "works everywhere" is shown literally — one product surface (a prompt composer with one verbatim string) pinned dead-center while its ENTIRE shell morphs in place through N product themes (background, typography, radii, chrome, logos all crossfading at once), ending in a washed-out freeze.
- Hook: when the opener is a roll-call — a static anchor line holds while an accent-colored line beneath it runs as a fast vertical carousel through an audience/option list, then the block clears into follow-up statement beats that land the brand line.

**duration**: 6.6–11.1s (Benefits shortest ~6.6s at 4 theme beats; Brand_Outro ~9–9.4s; Hook longest ~11s when the anchor-cycle block hands off to follow-up statement beats). The cycle engine itself occupies ~3–5s regardless of role.

**shot structure** (flat static frame — camera locked in every member; a `[bg]` field, solid or subtly drifting; two folded sub-shapes — **(A) adjacent-region cycle**: the anchor holds and a neighboring slot swaps through N states; **(B) whole-context morph**: the anchor holds and everything AROUND it re-skins in place)

- **Scene 1 (0.0–~2.0s) — the anchor lands and PINS.** The `[anchor: wordmark / product name / composer box / lead line]` enters once — fade/scale-in centered, word-by-word build, or already present at frame one — at a fixed position it will hold for the entire clip. Zero movement from here on: no drift, no breathe, no re-layout. If the anchor is a UI surface (sub-shape B), it carries a `[verbatim string]` with a blinking cursor.

- **Scene 2 (~2.0s–~70% of runtime) — the cycle engine (signature move).** The world changes around the unmoved anchor. Choose by sub-shape:
  - **Sub-shape A (adjacent-region cycle)**: a region beside/beneath the anchor steps through N discrete states — pick ONE swap mechanic and ONE cadence:
    - _swap mechanics_: instant hard-cut label replacement (a `[chip / tape label]` slaps over the old one, texture/highlight shifting slightly, chip width re-fitting each `[phrase]` — growing away from the anchor, never over it); sequential per-word highlight stepping (one word of the `[tagline]` snaps bright/bold while the rest sits dim grey, the highlight walking the line); or a fast vertical carousel (each `[list item]` slide/fades through the accent slot ~0.5s/phrase).
    - _cadences_: steady stepping (~0.5–1s/state), or **slow→accelerating flurry** — ~1s beats compressing to ~0.15–0.3s per swap, breadth escalating into a blur of states (12–16 states read as "everyone"; 3–8 read as a roll-call).
    - Geometry law: the cycling region NEVER overlaps, touches, or displaces the anchor; size the layout so the longest state still fits inside the frame with clear margins.
  - **Sub-shape B (whole-context morph)**: at ~1.3s intervals the entire theme — `[bg color]`, typography, corner radii, toolbar icons, footer `[brand logos]`, contextual lines — morphs in place via quick (~0.3s) crossfades through N `[product skins]`, every property blending simultaneously. No hard cuts, no wipes; the anchor's content string is identical in every skin (chrome details like a `> ` prefix may adapt per skin).

- **Scene 3 (~70–85%) — the emphasis beat.** The cycle resolves — it does not just stop:
  - _Variant — Brand_Outro (highlight stepping)_: the whole `[tagline]` snaps solid bright at once — full-line illumination after the per-word walk.
  - _Variant — Brand_Outro (flurry)_: the flurry halts and HOLDS on the `[longest / weightiest phrase]` — a beat of stillness after acceleration.
  - _Variant — Benefits (theme morph)_: the final beat mutes — a faint `[dot-grid]` fades in across the background while the UI drops to low opacity, a washed-out blueprint freeze.
  - _Variant — Hook (carousel)_: the anchor block clears, handing off to 1–3 centered word-by-word statement beats (kinetic-type-beats territory) that carry toward the close.

- **Scene 4 (final beat → end) — lockup completion and HOLD.** A final element joins the still-unmoved anchor and the finished composition holds static to the end: a `[closing word]` drops in below, aligned to the last cycled state ("enjoy."); the chip vanishes on a hard cut and the `[brand sign-off]` appears beside the anchor on a shared baseline ("by ANTHROP\C"); or the final `[brand line]` builds word-by-word dead-center and holds ("with Copilot."). Long static hold — the lockup is the payoff, give it 20–30% of the runtime.

**motion vocabulary**: anchor fade/scale-in entrance; permanently pinned anchor (zero movement, no idle breathe); instant hard-cut label/chip replacement (slap-over with subtle texture/highlight shift); chip width resize-to-fit per phrase (grows away from the anchor); sequential per-word highlight stepping through a line; dim-to-grey line state; whole-line illumination snap; fast vertical carousel slide/fade of one line under a static line; cadence acceleration (slow ~1s beats into a ~0.15–0.3s flurry); hold-on-longest-phrase emphasis beat; in-place theme morph crossfade (~0.3s) blending background/fonts/radii/icons simultaneously; per-beat chrome/logo swap; blinking text cursor; contextual line appearing/disappearing across beats; dot-grid backdrop fade-in; global opacity washout; end freeze; word-by-word phrase build; block clear between scenes; drop-in entrance of a final word; hard cut to final lockup; long static hold.

**rule mapping**

- instant hard-cut chip/label/phrase swaps at time thresholds; per-word highlight stepping (color/weight state swaps); dim-line → full-line illumination snap; per-state chip width set (a per-state layout property, set discretely — never tweened) → `discrete-text-sequence`
- fast vertical carousel of the accent line under the static anchor (slide/fade stepped swaps in a masked slot) → `vertical-spring-ticker` (its footer-reveal step unused — Scene 4's lockup takes its place)
- per-phrase state windows computed from a script of N states (praise quotes, audience list, theme beats) → `dynamic-content-sequencing` (Accelerating cadence — for the flurry, pre-compute the beat array with shrinking `hold` values, geometric decay over the state list)
- word-by-word phrase builds (anchor line, follow-up statements, final brand line) → `dynamic-content-sequencing` + `waterfall-entry` (or `kinetic-beat-slam` when the statements should land percussively)
- anchor entrance fade/scale-in; drop-in of the final closing word → `spring-pop-entrance` (restrained overshoot — the register here is editorial, not bouncy)
- blinking cursor in the pinned composer → `context-sensitive-cursor` (color adapts per theme skin at segment boundaries)
- whole-context theme morph → `theme-crossfade-morph` (N pre-styled full-scene layers stacked at the same geometry, opacity-crossfaded, the shared anchor string rendered once on top); the composer shell's radius/surface component alone → `card-morph-anchor`
- subtly drifting background field beneath the cycle → `sine-wave-loop` (bounded drift; the anchor itself gets none)
- dot-grid fade-in + global opacity washout freeze; long static hold → `gsap-effects` (plain opacity tweens) / static hold (no rule needed)

**camera modifier**: none — every member is fully camera-static; the cycle is the only motion, and the pinned anchor's stillness is load-bearing. Do not add a push-in "for energy"; it would break the anchor contract.


<!-- ===== FILE: hyperframes/hyperframes-animation/blueprints/grid-card-assemble.md ===== -->

# grid-card-assemble — Grid / Card Assemble

**intent**: N items (tiles / cards / logos / list-lines) self-assemble in a staggered cascade into a grid or vertical list and hold — a "look how much / who / what it does" beat that enumerates breadth at once; an optional camera zoom-OUT pulls back to reveal the assembled array sitting inside a vaster whole.

**roles served**

- Key_Feature (from key-feature-card-grid-assemble): a grid of labeled feature tiles/pills (icon + label) cascades one-by-one into a 2-col-brick / 3×3 grid, then holds near-static with a slow push-in — enumerate many capabilities, no live UI, no cursor.
- Key_Feature (from key-feature-glass-card-camera-reveal): open TIGHT on 2–3 glowing icons; a camera zoom-OUT unfolds a row of glassmorphism cards that grow from behind the icons (icons shrink to card headers), center card scales forward, the group floats, then sweeps out — a "pillars revealed at once" reveal variant of the same assemble shape.
- Benefits (from benefits-vertical-list): short value phrases populate a single vertical list ~1 item/sec, co-resident and accumulating; each line enters via a spring marker-pop + check-draw + pill mask-wipe, OR the whole stack snaps up one slot per beat (slot-machine) so the newest lands in the bright focal slot.
- Social_Proof (from social-proof-logo-grid-zoom-out): a wall of partner/app logos builds into a center grid (whole-enter / randomized pop-in / column slide-up), an optional headline + accent-gradient proof-number fills in above, then a continuous camera zoom-OUT shrinks the array to reveal a vast ecosystem; optional fixed HUD/viewfinder brackets; optional grid slide-up fly-out exit.
- Key_Feature (from live-data-populate-board): the array assembles by POPULATING ITSELF — skeleton pills fill and swap to real data, cards spring in tethered to map markers — and its state keeps flipping live after assembly (status pills stepping through states); no cursor, locked frame. The "look how much" beat becomes "look, it's doing it right now."
- Benefits (from item-field-to-payoff-card): a breadth FIELD — a rapidly streaming list past a fixed focal slot, or a chip array with one highlighted hero — plays its breadth motion, then CLEARS to concise centered payoff text (claim / price / URL end card). The array is the argument's setup; the payoff line is its landing.

**duration**: 3.0–10.5s (Social_Proof 3.0–6s · live-populate 4.2–7.8s · Key_Feature grid 5.8–7.3s · Benefits stream/field-to-payoff 5.9–8.4s · Key_Feature glass-card 6.5s · Benefits list 6.5–10.5s, scaling ~1 item/sec with count)

**shot structure** (consolidated template — concrete motion verbs, [slots])

- **Scene 1 (0.0–~1.0s) — open + first arrivals.** On a `[gradient / radial / dark background]` (optional `[dot-grid / drifting-watermark]` texture), an empty `[grid or list region]` is established and items begin to ASSEMBLE in a quick staggered cascade (~0.04–0.08s gap; list pacing ~1 item/sec). Each `[item: feature tile / pill / logo tile / benefit line]` fades + slides/scales a short distance directly into its slot (low drama — no scatter, no big bounce; spring overshoot reserved for accent markers). Camera static. An opening `[headline / hook]` may fill in line-by-line above the array, with any `[proof number]` counting up in an `[accent gradient]`.
- **Scene 2 (~1.0s–~Xs) — array resolves + holds.** Remaining items finish arriving; layout resolves into the final `[2-col-brick / 3×3 grid / dense mosaic / stacked list]`. The completed array HOLDS, alive but resting: a gentle continuous parallax/sine FLOAT on the tiles and/or a slow camera push-in (faint scale-up). Optional `[accent-color]` glow TRAVELS across/behind the tiles.
- **Scene 3 (~Xs–end) — settle / reveal / exit.** Everything settles and holds to the end, OR the optional camera modifier runs (see below), OR a `[closing line / CTA]` book-ends the array. OR the field CLEARS to payoff copy — the array exits and a concise centered `[claim / price / URL]` lands (price via a very fast character snap-build with a split-second partial state; URL via a left-to-right reveal, holding in `[accent]` and flipping to `[ink]` only in the final beat) — OR the camera PUSHES THROUGH one highlighted `[hero item]` (single rapid accelerating push-in) and crossfades into a second, vaster receding `[word-grid depth field]` that continuously scales down to reveal ever more items before fading to the payoff.

Variants (where roles diverge from the template):

- **Variant — Key_Feature grid**: items are labeled `[icon + feature-label]` tiles/pills assembling into a 2-col-brick / 3×3 grid; near-static hold with slow push-in + optional traveling-glow sweep; headline book-ends (`[hook]` → `[CTA]`). No camera reveal.
- **Variant — Key_Feature glass-card-reveal**: the assemble is CAMERA-DRIVEN, not element-stagger. Open tight on `[2–3 glowing icons]`; camera zoom-OUT grows `[N]` glass cards out from behind the icons (icons shrink ~50% to become card headers), `[center card]` scales ~105% and moves forward to overlap the sides (quick spring); cards hold side-by-side with continuous parallax float; exit = fast motion-blur SWEEP slides the cards off-frame.
- **Variant — Benefits vertical-list**: a single vertical `[benefit-line]` stack, ~1 item/sec, three sub-modes — (a) BUILD: each line stays fully lit; entry = `[marker]` spring-pop + `[check/icon]` draw-in + `[pill]` mask-wipe of the text; (b) SNAP: the whole stack steps up one slot per beat (~0.1s eased) so the newest line lands in the bright focal slot and lines leaving it dim by position; (c) STREAM: the list scrolls rapidly and continuously past the focal slot — center item opaque `[ink]` and slightly enlarged, neighbors faded/shrunk — then DECELERATES to stop on the `[chosen item]`; optionally split-framed against a fixed static `[label]` on the opposite side; the field then clears to a centered `[payoff line]`. Static camera; optional perpetual `[decorative orbit/disc]` on the opposite side. No camera reveal.
- **Variant — Key_Feature live-populate**: the assemble is a DATA-POPULATION wave, cursorless, frame locked (± one gentle opening zoom-out that makes room for the `[headline]`). Two board shapes — (a) ANCHORED: `[white data cards]` spring in one-by-one, each tethered by a thin line to its `[marker]` on a `[map/board surface]` whose markers pulse (expanding fading rings); (b) TABULAR: new `[columns]` appear as grey skeleton pills, progress fills run left→right staggered top-to-bottom (colored fill with a leading tip), each bar SWAPPING to its real `[value/avatar chip]` on completion. After assembly the array stays LIVE: `[status pills]` flip states in quick snappy swaps (color-coded, several in succession), or the `[headline]` crossfades and a second population wave runs on a newly revealed region — the table content scrolling horizontally beneath a sticky first column to expose it. Hold lands on the fully populated, fully updated final state.
- **Variant — Social_Proof logo-wall-zoom-out**: intro beat (`[trusted-by headline]` card OR a `[product screenshot]`) crossfades/cuts to a center logo grid that builds (whole-enter / randomized pop-in / column slide-up); a continuous camera zoom-OUT then shrinks the whole grid toward center to reveal a vast ecosystem and holds; optional fixed HUD/viewfinder brackets; optional exit = whole grid SLIDES UP and flies out through the top.

**motion vocabulary**: item stagger-assemble (fade + short slide/scale into slot) · brick/grid/list layout resolve · randomized pop-in · column slide-up · vertical-list step (slot-machine snap-and-hold) · spring-overshoot marker pop · check/icon draw-in · pill/label mask-wipe reveal · dim-by-position de-emphasis · line-by-line headline fill · accent-gradient number count-up · near-static hold · gentle parallax/sine float on hold · slow camera push-in · camera zoom-OUT reveal (continuous OR phased pull-back) · cards-grow-from-behind-icons · icon-shrink-to-header · center-card scale-up + forward overlap (spring) · traveling-glow sweep · fixed HUD/viewfinder brackets · motion-blur slide-out sweep (exit) · grid slide-up fly-out (exit) · book-end headline fade · perpetual decorative orbit/loop · skeleton-pill progress fill (left→right, leading tip, color transition) · fill-completes-swap-to-real-data · staggered top-to-bottom fill cascade · live status-pill state flips (color-coded, post-assembly) · tethered-card spring-in (thin line to an anchor marker) · pulsing marker rings · two-wave populate with headline crossfade · sticky-column internal horizontal scroll · rapid vertical stream past a fixed focal slot + deceleration stop · split fixed-label layout · pill-widens-as-label-fills arrival · highlighted hero chip · push-through-the-hero-item exit · receding word-grid depth field · clear-to-payoff coda · price snap-build (split-second partial state) · left-to-right URL reveal + final-beat color flip.

**rule mapping** (motion verb → `rule-id`)

- item stagger-assemble into slot → `center-outward-expansion` (per-item stagger + short-path slide variant; for a wall too dense for a true center burst, use it in its "starting partially-spread"/direct-into-slot form — see merge tension)
- brick/grid/list layout resolve → `center-outward-expansion` (target positions = final layout slots)
- randomized pop-in stagger → `gsap-effects` (stagger recipe; randomized `from`/order)
- column slide-up into grid → `gsap-effects` (per-column staggered slide-up)
- vertical-list step / slot-machine snap-and-hold → `vertical-spring-ticker` (STEPS = number of line advances)
- spring-overshoot marker pop → `spring-pop-entrance` (back.out spring) — also `gsap-effects` for the staggered pop chain
- check / icon draw-in inside marker → `svg-path-draw`
- live line-art icon in a tile (internal parts) → `svg-icon-enrichment`
- pill / label mask-wipe text reveal → `techniques.md` (clip-path reveal)
- dim-by-position de-emphasis → `gsap-effects` (per-line opacity by slot position; no dedicated rule)
- line-by-line headline fill → `discrete-text-sequence`
- accent-gradient proof number count-up → `counting-dynamic-scale`
- gentle parallax / sine float on hold → `sine-wave-loop` (apply the concurrent-elements amplitude `/√N` rule for a held grid)
- slow camera push-in → `multi-phase-camera` (steady-push phase pattern)
- center-card scale-up + forward overlap → `spring-pop-entrance` (the quick spring) + `techniques.md` CSS-3D (z-depth overlap)
- cards-grow-from-behind-icons / icon-shrink-to-header → driven by the camera reveal (`multi-phase-camera`) — the grow/shrink are scale tweens chorded to the pull-back phase; no separate rule
- fixed HUD / viewfinder brackets → `ai-tracking-box` (static-bracket variant — overlay frame, not tracking)
- book-end headline fade → `discrete-text-sequence` (or `gsap-effects` fade)
- perpetual decorative orbit / disc / loop → `sine-wave-loop` (or `orbit-3d-entry` if it's an orbiting badge ring)
- traveling-glow sweep across/behind tiles → `ambient-glow-bloom` (one-pass traveling glow sweep across the tiles)
- motion-blur slide-out sweep (glass-card exit) → `motion-blur-streak` (directional velocity blur on the fast sweep that carries the cards off-frame)
- grid slide-up fly-out exit → `gsap-effects` (plain staggered translate-off-frame; no dedicated rule needed — a basic exit tween, not a missing capability)
- skeleton-pill progress fill → `stat-bars-and-fills` (progress-fill `scaleX` form; the leading tip is a chorded child element)
- fill-completes-swap-to-real-data / live status-pill flips / headline crossfade between waves → `discrete-text-sequence` (whole-state replacement at time thresholds — the pill's states are text states)
- staggered top-to-bottom fill cascade → `gsap-effects` (per-row stagger on the fill tweens)
- tethered-card spring-in → `spring-pop-entrance` (the card) + `avatar-cloud-network` (the thin connection-line-to-anchor layout; anchor coordinates must match the marker exactly) + `svg-path-draw` if the tether draws in
- pulsing marker rings → `cursor-click-ripple` (its expanding-ring + attack-decay opacity envelope, minus the cursor/click, on a bounded repeat)
- sticky-column internal horizontal scroll → `viewport-change` (PAN form on the inner column layer; the sticky column sits outside the panned layer) — mark the moving layer `data-layout-allow-overflow` and clip at the table card
- rapid vertical stream past a focal slot + deceleration stop → `vertical-spring-ticker` (continuous form: one long decelerating translate instead of its stepped tweens; focal-slot emphasis reuses the dim-by-position mapping above)
- pill-widens-as-label-fills → `card-morph-anchor`'s substitution law (uniform `scaleX`/clip-path — never tween `width`) + `discrete-text-sequence` for the label fill
- push-through-the-hero-item exit → `multi-phase-camera` (single accelerating push phase) aimed via `coordinate-target-zoom` at the highlighted chip, crossfading at peak
- receding word-grid depth field → `viewport-change` (one `.world` wrapper, `cam.scale` ↓ continuously — the zoom-OUT reveal grammar pointed at a word field; size/opacity tiers fake the depth)
- price snap-build (split-second partial state) → `discrete-text-sequence` (non-linear typing with bulk additions — exactly its typo/partial-state mechanic)
- left-to-right URL reveal → `techniques.md` (clip-path reveal — same mapping as the pill mask-wipe); the final-beat color flip → `gsap-effects` (a `tl.set` at the beat — basic, no rule needed)

**camera modifier — zoom-OUT reveal** (optional; the role-defining move for the glass-card and logo-wall variants): a camera wrapper around the whole array scales DOWN over the hold, revealing the assembled grid/cards sitting inside a larger environment (ecosystem scale, or a row of cards unfolding from tight icons).

- Continuous single-pass zoom-out (Social_Proof ecosystem pull-back) → `viewport-change` (one wrapper, `cam.scale` ↓ via onUpdate — single source of truth)
- Phased pull-back → focus → settle, with built-in drift (Key_Feature tight-icons → cards-unfold) → `multi-phase-camera` (use the "Dramatic reveal: push → neutral → pull" / pull-back phase pattern; grow/shrink of cards chords to the pull-back phase)

---

```
BLUEPRINT: grid-card-assemble — serves Key_Feature, Benefits, Social_Proof (folded 4 drafts + 2 mined clusters: live-data-populate-board, item-field-to-payoff-card)
RULE COVERAGE: complete, no gaps — traveling-glow sweep → ambient-glow-bloom; motion-blur slide-out sweep (exit) → motion-blur-streak; grid slide-up fly-out (exit) → gsap-effects (plain translate); skeleton-fill populate → stat-bars-and-fills + discrete-text-sequence; push-through-hero exit → multi-phase-camera + coordinate-target-zoom
```

Merge tension: `center-outward-expansion` (the natural backing for stagger-assemble) caps cleanly at 3–8 items and explicitly warns 8+ causes mid-flight overlap chaos — but a Social_Proof logo wall is deliberately dense (12+ tiles), so for that variant the items must NOT burst from a shared center; they slide a short distance directly into their own slot (the rule's "starting partially-spread"/short-path form, or a `gsap-effects` per-item stagger), which the consolidated Scene-1 verb already specifies as "short distance directly into its slot."
