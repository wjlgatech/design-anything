# Design principles — survival-tested, machine-enforceable where possible

Each principle is traceable to its evidence window (
[30d](../research/last30days/DIGEST.md) ·
[30y](../research/last30years/DIGEST.md) ·
[300y](../research/last300years/DIGEST.md)) and states how it constrains the
generator. Principles that convert to hard gates are marked **[GATE]** (implemented
or roadmap in `pipeline/ready_gate.py`).

## P1 — The Vitruvian triple gate [GATE] (300y)
Every blueprint must simultaneously pass structural, functional, and aesthetic
validation — a zero in any one fails the whole. Firmitas/utilitas/venustas is
the oldest ClosedLoop in the field.

## P2 — Tables beat slogans [GATE] (300y)
The most implementable survivors are *tables and grids*: Neufert/Panero
anthropometric clearances, the ISO 2848 100mm module, DfAM overhang/wall rules,
daylight-factor minimums. A layout violating a clearance table is a **bug**, not
a style choice.

## P3 — Design for the machine that will make it [GATE] (300y Bauhaus → DfAM)
Outputs must be manufacturable by the declared process: printer envelope,
nozzle-derived min feature, 45° overhang rules for FDM, layer-height anisotropy,
extrusion-path continuity for concrete printing. Per-process rules apply *during*
generation, never as post-hoc rejection.

## P4 — Function derives form (300y Sullivan)
Geometry derives from the stated program (adjacencies, loads, circulation,
play-type mix) first; style is applied to a functionally valid skeleton, never
the reverse.

## P5 — Patterns are the representation (300y Alexander)
The generator composes context/problem/solution patterns (courtyard, light on
two sides, entrance transition, prospect/refuge). A Pattern Language already
survived one substrate change (buildings → software); this repo bets it crosses
another (software → AI generation).

## P6 — Bet interfaces on survivors; hot-swap the AI layer (30y)
Emit IFC, glTF/USD, STL/3MF — the 10-30-year-old formats that outlived every
rival. Treat sub-10-year AI models (diffusion, 3DGS, SDS) as replaceable front
ends: that layer already churned once (NeRF→3DGS in 3 years) while COLMAP and
the formats sat still.

## P7 — Open systems survive; closed systems die (300y prefab + 30y anti-portfolio)
Crystal Palace and Sears kit homes survived; Lustron, Katerra, and Veev died on
vertical integration. **Print the walls, buy the windows**: generated construction
must interface with standard trades, fasteners, and stock dimensions. Arm the
builder (COBOD); don't become the builder (Katerra).

## P8 — Separate shearing layers [GATE-roadmap] (300y Brand)
Structure / skin / services / space-plan must be independently replaceable.
The critical caution for monolithic 3D-printed walls: route services in
accessible chases, prefer mechanical fastening to bonded assemblies.

## P9 — Condition on climate and culture (300y vernacular + feng shui kernel)
Generate from climate zone, sun path, and local materials; expose cultural
conventions (orientation preferences, entry sequencing) as a selectable
constraint layer distinct from physics.

## P10 — Human scale, eye level, daylight [GATE-roadmap] (300y Gehl + ancient lights)
Evaluate at 1.6m eye height at walking speed, not god-view axonometric.
Daylight per habitable room is a hard gate (EN 17037 lineage); windows derive
from orientation, never decoration.

## P11 — Rule economy for play systems (300y chess/Go)
For game domains: few orthogonal mechanics, large emergent state space.
Validate transmissibility (rule-text length), fairness (first-move advantage
bounds), and decision density via self-play.

## P12 — Iterate, never single-shot (300y Eames + agent practice)
Generate → simulate against body/physics models → refine. The loop is the
method; one-shot output is the anti-pattern at every scale, from a chair to a
codebase.

## P13 — No evidence ⇒ Not ready [GATE] (repo discipline)
The ready gate never passes on unmeasured items; unverifiable research claims
are marked UNVERIFIED; an honest ❌ beats a fake ✅. This is the principle that
makes all the others enforceable.
