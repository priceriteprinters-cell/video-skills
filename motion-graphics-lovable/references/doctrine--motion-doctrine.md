

<!-- ===== FILE: doctrine/motion-doctrine/GUIDE.md ===== -->

---
name: motion-doctrine
description: "GATEWAY — load FIRST before composing any HyperFrames animation or video. The high-level motion law that makes a multi-scene video feel like ONE continuous camera move instead of a stack of independently-animated slides. Covers the vector law (how you exit determines how you enter, incl. the Z scale-sign rule), the film's current, carrier elements, causal motion, the Seam Gate (build-gate enforcement), the ban on idle wobble (motion must PERFORM, not breathe), stillness-before-climax, and the sustained-motion routes. Routes to the low-level technique skills (cut-the-curve — the full catalog incl. waterfall entry + nudge curve, oversized-cursor, seam-craft). These rules SUPERSEDE generic / upstream motion guidance. [continuity, direction, vector, momentum, seam, transition, ease, performance, idle-motion, narrative-motion, film-grammar]"
metadata:
  internal: true
---

# Motion Doctrine (Gateway)

Read this before composing any animation. It decides WHAT happens at every seam and how
every scene performs; the technique skills implement it. These rules supersede generic /
upstream motion guidance. The failure this prevents: scenes authored in isolation — the
eye's momentum dies at every cut, and scenes wobble in place between entry and exit.

## Route map

| Decision (this skill)                              | Implementation skill                                                                              |
| -------------------------------------------------- | ------------------------------------------------------------------------------------------------- |
| Seam transition choice + parameters + code         | `cut-the-curve` §1–5 (the catalog)                                                                |
| Text / element entry cascades                      | `cut-the-curve` §6 (waterfall entry)                                                              |
| In-scene group repositioning (no cut)              | `cut-the-curve` §7 (nudge curve)                                                                  |
| Cursor-led action / scene kickoff / morph ignition | `oversized-cursor`                                                                                |
| Seam render mechanics / white-flash guard          | `seam-craft`                                                                                      |
| Product-launch / explainer / caption work          | overlays `text-beat-economics`, `brand-faithful`, `captions-overlay` on top of the upstream skill |

Authoring order: **vector ledger (`ledger.json`) → STAMP the master seams from it
(`scripts/seam-stamp.mjs --ledger ledger.json --write index.html`) → sustained-motion
route per phase → carriers and causes → build comps → VERIFY (`scripts/seam-gate.mjs`).**
Hand-author only Tier-A morphs/match-cuts; stamped seams pass the gate by construction.

---

# Part 1 — The Seam Law

## The Vector Law

> How Scene A exits determines how Scene B enters: same axis, same direction, matched
> speed, cut mid-motion on both sides.

1. **Axis** — x stays x, y stays y, Z stays Z. Never trade axes across a cut.
2. **Direction** — never mirror. On Z, direction = the SIGN of scale change: growing =
   push (camera forward), shrinking = pull (camera back). A receding exit answered by a
   grow-from-small entry is a mirrored vector — the most common violation, because
   grow-from-small is the default element entrance.
3. **Speed** — entry initial velocity ≈ exit final velocity, via mirrored eases (exit
   `power4.in` + entry `power4.out`, same distance and duration; the incoming side picks
   up ≥50% through the notional path). Mechanics in `cut-the-curve`.
4. **Phase** — the cut lands mid-motion on BOTH sides. Settling to rest before the cut,
   or starting from rest after it, is a dead beat.

## The Current

Every film picks ONE dominant direction (house default: LEFT). Every ordinary seam uses
it. Other vectors are RESERVED — spending one means something:

| Vector                    | Meaning                                                         |
| ------------------------- | --------------------------------------------------------------- |
| The current (LEFT)        | "next beat" — neutral forward progress                          |
| Upward                    | elevation — a conclusion or reveal rises above what came before |
| Z forward (zoom-through)  | pushing deeper into the same thought                            |
| Z backward (inverse zoom) | ARRIVAL — something bigger lands                                |
| Scale-burst (explode out) | leaving a world — a surface blasts past camera                  |

- Never run consecutive seams in opposing directions — ping-pong reads as an error.
- A direction change needs a visible cause (click / bounce / impact) or a chapter boundary.

## The Vector Ledger

Write it before authoring any master timeline — as **`ledger.json` at the project root**
(schema: `references/seam-gate.md`). One row per seam: cut time, exit and entry vectors
(axis + signed direction; Z rows carry the scale sign), selectors, technique. Exit and
entry must match; if a row mismatches, fix the plan, not the easing. The verifier checks
row consistency statically before any runtime sampling.

## Carriers

The eye follows objects, not abstractions. The strongest seams hand a concrete carrier
across the cut at matched position AND velocity: a cursor mid-path, a container that
shrinks/docks into the next layout, a mark that flies into its exact slot, the word group
of a waterfall cut. With no natural carrier, the scene heroes carry it (partial travel +
early fade, entry mid-flight). Never a crossfade — it has no carrier at all.

## Causal Motion

Chain motion so each move is visibly launched by the last: click → squash → release
spring → flight → impact → recoil → reveal.

- Effects start ON the causing frame — same timeline position, never "shortly after."
- Reactions scale with implied mass: big elements rebound slower, small ones snap.
- A force is a license to change direction; an uncaused flip is a ping-pong.

## The Seam Gate (build gate — run the verifier, exit 0 or the seam is not done)

```bash
node <SKILL_DIR>/scripts/seam-stamp.mjs --ledger ledger.json --write index.html  # generate
node <SKILL_DIR>/scripts/seam-gate.mjs  verify --ledger ledger.json --project .  # verify
```

The script (usage + ledger schema: `references/seam-gate.md`) numerically enforces, per
seam: ledger-row consistency, exit still moving at the cut, entry mid-flight (never from
rest), measured direction = ledger direction, entry/exit speed match (WARN), **zero
overlap** (one side visible per frame — the cut is not a dissolve), the **Z sign** rule
(d(scale)/dt same sign both sides; the incoming scene's own entrances are scanned for
sign-fighting), and carrier rect continuity with ancestor scale included. Use
`seam-gate.mjs probe --t <cut>` to find each seam's true carrier selectors when authoring
the ledger.

Rules the script cannot check — still yours:

1. **Edits re-open the seam.** Any change to a scene's first/last ~1s (including
   re-timing to new VO) invalidates that boundary's audit — re-run the verifier.
2. **Audio is the clock.** Re-time scenes to the VO's real word timestamps; never rush a
   read to fit a slot. A VO regen re-opens its seams.
3. **Clip-gating gotcha** (the usual cause of a zero-overlap FAIL): a clip whose
   `data-start` precedes its entry tween is un-hidden at its initial opacity — set
   initial `autoAlpha: 0` AND `data-start` = the cut time, never earlier.

---

# Part 2 — Performance (the scene keeps performing)

## No idle wobble

Idle sine loops (breathe, float, drift, glow pulse) are BANNED as sustained motion — they
read as "the video is waiting." A scene that finishes entering with seconds left is a
planning bug: add story, not wobble. Every phase between entry and exit is owned by one
of these routes (name the route in the plan):

| Route                  | What it is                                                                                                             |
| ---------------------- | ---------------------------------------------------------------------------------------------------------------------- |
| **Staged reveals**     | Hold content back; pay it off on narration beats — the frame keeps gaining information (default for ≥2 content groups) |
| **Camera with intent** | A mapped scale+pan path: establish wide → travel → arrive on the subject                                               |
| **Sequenced UI life**  | The product behaves over time: progress advances, highlights step, counts tick                                         |
| **Animated sequences** | Elements act out a beat: a card files into a stack, an item gets dragged, a result assembles                           |
| **Cursor-led action**  | An oversized cursor walks the eye to a trigger; its CLICK ignites the next beat (`oversized-cursor`)                   |

Test: pause at any second — something meaningful must be mid-flight (a reveal landing,
the camera traveling, the UI doing what the narration says).

## Stillness before climax

Schedule a **0.3–0.75s pause** between the major action and its result — the dramatic
comma. A scene that jumps straight from action to result loses it.

## Timing intents

- Single entry ≤ ~800ms; longer buildup = multi-element stagger, not one slow element.
- Exit ≈ 75% of entry. Exception: cut-the-curve inverts this (entry ~127% of exit).
- Total stagger ≤ 500ms; with 8+ elements, tighten per-item delay or stagger the first few.
- Forbidden eases: `bounce.out` / `elastic.out`. Entry overshoot `back.out(1.4–1.7)` is fine.
- Similar elements share one ease+duration intent — never a unique pair per element.

## Transition vocabulary

Use only 2–3 inter-scene transitions per film and repeat them; the default boundary is
**cut-the-curve in the current's direction**. Hand-written shared-element morphs
(`intent: morph`) don't count against the budget.

---

## Anti-Patterns

| Don't                                                                      | Instead                                            |
| -------------------------------------------------------------------------- | -------------------------------------------------- |
| Author each scene's entrance in isolation                                  | Write the vector ledger first                      |
| Crossfade between scenes                                                   | Cut-the-curve in the current's direction           |
| Exit completes, THEN the scene changes                                     | Cut mid-motion on both sides                       |
| Entry starts from rest after a cut                                         | Enter ≥50% through the notional path               |
| Inverse-zoom exit → grow-from-small entry (or push → oversized retraction) | Match the scale-velocity sign (Seam Gate 7)        |
| Incoming scene's own pop-in intro under a Z-seam handoff                   | Hold its opening frame composed, or match the sign |
| Idle wobble / breathe / float to fill time                                 | Assign a sustained-motion route; or add story      |
| Direction flip without a cause                                             | Spend a force, or keep the current                 |
| Reserved vectors used as variety                                           | Default to the current; spend them on meaning      |
| Reaction a few frames after its cause                                      | Same-frame ignition                                |
| Action jumps straight to result                                            | Schedule stillness-before-climax (0.3–0.75s)       |


<!-- ===== FILE: doctrine/motion-doctrine/references/seam-gate.md ===== -->

# seam-stamp.mjs + seam-gate.mjs — usage + ledger schema

Generate-and-verify pair for the Seam Gate. Zero npm deps (node ≥ 22 + a local Chrome;
the gate finds `~/.cache/puppeteer` chrome-headless-shell or system Chrome automatically).

```bash
# STAMP: write the master seam block (base sets + all wrapper tweens) from the ledger.
# Replaces the // <seams:auto> … // </seams:auto> block (inserts after the
# window.__timelines["main"] registration if markers are absent). Stamped seams pass
# the gate by construction. match-cut/morph rows get visibility sets only — the
# carrier handoff stays hand-authored.
node <SKILL_DIR>/scripts/seam-stamp.mjs --ledger ledger.json --write index.html
```

Per-seam stamp options in the ledger: `exit.dur` / `entry.dur` (durations),
`entry.travel` (xPercent/yPercent offset, default 10 — use 8 for a soft entry),
`blur` (Z seams, default 18px full-frame / set 10 for text-scale).

```bash
# verify every seam in the ledger (exit 0 = gate passed)
node <SKILL_DIR>/scripts/seam-gate.mjs verify --ledger ledger.json --project <project-dir>

# reuse a RUNNING preview server (restart it after comp edits — stale bundle!)
node <SKILL_DIR>/scripts/seam-gate.mjs verify --ledger ledger.json --url http://localhost:5244

# discover movers around a cut time (use to author/fix ledger rows)
node <SKILL_DIR>/scripts/seam-gate.mjs probe --t 44.8 --project <project-dir>
```

`--project` spawns a fresh preview server with `HYPERFRAME_RUNTIME_URL` unset and kills
it after — preferred. `--json` for machine output. `--fps 30` default.

## ledger.json

Lives at the project root. One row per seam; this is the vector ledger as data.

```json
{
  "fps": 30,
  "seams": [
    {
      "id": "hook→claim",
      "cut": 4.2,
      "technique": "cut-the-curve LEFT",
      "exit": { "selector": "#el-hook", "axis": "x", "dir": -1 },
      "entry": { "selector": "#el-claim", "axis": "x", "dir": -1 }
    },

    {
      "id": "claim→payoff",
      "cut": 10.2,
      "technique": "inverse zoom-through",
      "exit": { "selector": "#el-claim", "axis": "z", "dir": -1 },
      "entry": { "selector": "#el-payoff", "axis": "z", "dir": -1, "scanRoot": "#el-payoff" }
    },

    {
      "id": "ui→player (match cut)",
      "cut": 60.6,
      "type": "match-cut",
      "carrier": { "out": "#resting-card", "in": "#product-video" }
    }
  ]
}
```

- `cut` — seconds on the master clock, the frame the incoming side ignites.
- `type` — `"cut"` (default; full vector checks), `"match-cut"` / `"morph"`
  (carrier-continuity + overlap only; motion may start AT the boundary).
- `axis` — `"x"`, `"y"`, or `"z"` (z = scale). `dir` — sign of motion:
  x −1 = leftward, y −1 = upward, z +1 = push (growing), z −1 = pull (shrinking).
- `selector` — the element that CARRIES the seam motion. Use the wrapper when the
  master timeline moves the wrapper; use the in-comp hero (id or `[data-hf-id=…]`)
  when the seam motion is authored inside the sub-comp. `probe` tells you which.
- `entry.scanRoot` (z seams) — subtree scanned for sign-fighting internal entrances;
  defaults to the entry selector.
- `carrier` — optional on `"cut"` rows; required on match-cut/morph. `out`/`in` rects
  must match at cut±1 frame (12px center / 5% size tolerance, ancestors included).

## What each check enforces (Seam Gate rule ↔ report row)

| Report row                           | Rule                                                           |
| ------------------------------------ | -------------------------------------------------------------- |
| `ledger`                             | exit/entry vectors match in the PLAN (axis + dir)              |
| `exit-moving` / `entry-moving`       | rule 1/3 — no settled exits, no from-rest entries              |
| `exit-direction` / `entry-direction` | rule 3 — measured sign matches the ledger                      |
| `speed-match` (WARN)                 | law §3 — entry velocity ≈ exit velocity                        |
| `zero-overlap`                       | rule 6 — one side visible per frame, never both                |
| `z-sign-scan`                        | rule 7 — incoming scene's own entrances don't fight the Z sign |
| `carrier-*`                          | rules 3/4 — carrier rect continuity, ancestor scale included   |

Velocities are measured on `getBoundingClientRect` (center for x/y, width-ratio for z),
so ancestor wrapper transforms are automatically included.
