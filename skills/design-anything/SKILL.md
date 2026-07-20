---
name: design-anything
description: >
  Turns any design intent — a text brief or a picture — into an execution-ready,
  gate-verified blueprint: 3D-printable models (STL), construction floor plans,
  garment sewing patterns, game/sim scenes. Discovers what the user wants to
  design, retrieves survival-tested principles and constraint tables, emits
  deterministic parametric source, and verifies with machine gates (watertight,
  clearances, egress, zero-waste, fit). Use when the user wants to design,
  redesign, or validate a physical or spatial thing: "design me a…", "is this
  printable / buildable / cuttable", "turn this sketch or photo into a plan",
  "redesign my room / house / garden / apron / game level", "make it 3D-print
  ready". NOT for graphic/UI/logo design, photoreal rendering, or engineering
  certification (a gate is never a permit or PE stamp).
kind: skill
license: MIT
runtimes: [claude-code]
---

# /design-anything — any design intent → gate-verified blueprint

Engine probe: !`REPO="${DESIGN_ANYTHING_HOME:-$HOME/Documents/Projects/design-anything}"; [ -f "$REPO/Makefile" ] && echo "engine at $REPO ($(cd "$REPO" && git log -1 --format=%h))" || echo "engine ABSENT — clone https://github.com/wjlgatech/design-anything to $REPO first"`

**This skill is a thin router over the design-anything engine repo.** All
tested logic lives there: gates in `pipeline/`, constraint tables in `data/`,
golden generators in `examples/`, knowledge in `principles/` + `domains/`.
Never re-implement in chat what the engine already verifies. Full design
rationale: `docs/SKILL_DESIGN.md`.

## 0. Engine (self-aware, self-heal)

- If the probe above says ABSENT: `git clone https://github.com/wjlgatech/design-anything "$REPO"` and continue.
- Before real work, run `make check` in the repo. **Red ⇒ fix the regression
  first; never build on red.** Capabilities come from artifacts, not claims:
  `llms.txt` (what's curated), the gate table in `pipeline/README.md` (what's
  verifiable). State roadmap gaps plainly, reading the current gate table rather than
  assuming this document is fresh.

## 1. The loop (backbone — every request)

**absorb → route → retrieve → compose → gate → reflect**

1. **Absorb** — reflect the brief back in ≤6 lines (object, domain, target,
   size, process, must-haves). Never silently drop a stated constraint.
2. **Route** — fill three slots, asking **at most 2 questions, only at genuine
   forks** (the user need not know this toolset):
   - WHAT (domain): infer from nouns/image; ask only if truly ambiguous.
   - DONE (target gate): print | construction | garment | game-sim | advice-only
     — the most common real fork.
   - KNOWNS: never interrogate — propose visible defaults and proceed
     ("assuming a 220×220×250 bed and 0.4 nozzle — say otherwise").
3. **Retrieve** (progressive disclosure — read ONLY what the route matched;
   see §2).
4. **Compose** — emit deterministic parametric source with the brief's
   parameters at the top, modeled on the matching golden example. **Emit the
   composition, not the render** — never an opaque mesh.
5. **Gate** — run the target's gate; relay its PASS/FAIL lines **verbatim**.
   Fail ⇒ fix the named gate, re-run; same failure 3× ⇒ stop and escalate
   with what was tried. **No gate pass ⇒ never say "ready."** For an open
   brief, diverge first: sketch 2-3 options, converge with the user, gate one.
6. **Reflect** — bank lessons as repo artifacts, not chat (§3).

## 2. Routing table (what to read/run per target)

| Target | Gate to run | Golden example | Read on match |
|---|---|---|---|
| 3D-print (objects, furniture, planters, hardscape) | `python3 pipeline/ready_gate.py <stl> --min-feature <wall>` | `examples/planter/generate.py` | `domains/interior-design/README.md` or `domains/landscape/README.md` |
| Construction (rooms, floor plans, houses) | `python3 pipeline/construction_gate.py <layout.json>` | `examples/studio-flat/generate.py` | `data/clearances.yml` + matching `domains/architecture-*/README.md` |
| Garment (clothing, patterns, markers) | `python3 pipeline/pattern_gate.py <marker.json>`; export `python3 pipeline/dxf_aama.py <marker.json> <out.dxf>` (factory) or `python3 pipeline/garmentcode_export.py <marker.json> <spec.json>` (research) | `examples/apron/generate.py` (graded S/M/L via `--size`) | `data/garment.yml` + `domains/garment-design/README.md` |
| Game/sim (levels, worlds, scenes) | `python3 pipeline/scene_gate.py <scene.gltf> --target pc\|mobile` | `examples/arena/generate.py` | `data/scene.yml` + `domains/game-design/README.md` or `domains/simulation/README.md` |
| Body-fit products (eyewear; dental/prosthetics/footwear siblings) | `python3 pipeline/bodyfit_gate.py <fitspec.json>` + `ready_gate.py` on the printable part | `examples/eyewear/generate.py` | `data/bodyfit.yml` + `domains/eyewear/README.md` |
| Photo/scan input | route through `skills/scene-to-layout/SKILL.md` first | — | — |
| Tool/landscape question | — | — | `llms.txt`, then the README tables; deep dives per `skills/design-research/SKILL.md` |
| "Why" questions (principles, method) | — | — | `principles/DESIGN_PRINCIPLES.md`, `principles/DIKW_MODEL.md`, `docs/DESIGN_DISCIPLINES.md` |
| High-stakes review | — | — | `workflows/README.md` (design-review-panel shape) |

## 2a. Satellite toolsets (progressive disclosure — table is GENERATED)

When a route needs an **external tool** (generate a mesh, drive a DCC, parse a
scan, interop with a pattern CAD), check the satellites — SHA-pinned digests +
skills compiled from the repos this hub cites. The backbone rules: **load only
the matched satellite** (`SKILL.md` first, then its `KNOWLEDGE.md`); external
code is untrusted regardless of stars; a **STALE** status means upstream moved
past the digest's pin — re-verify before relying on internals; and satellite
output is never "ready" until **our** gate says so. Current list compiled from
`data/satellites.yml`:

<!-- BEGIN:satellite-routes -->

| Satellite | Serves | When to load | Status |
|---|---|---|---|
| `skills/use-trellis-2/SKILL.md` | 3D-print / mesh generation (repair before ready_gate) | Open (MIT) 4B image-to-3D flow-matching model; any topology, full PBR, GLB/PLY/OBJ export. | fresh |
| `skills/use-blender-mcp/SKILL.md` | execution backbone — any route that needs a DCC | Drive Blender from any LLM via MCP — the natural execution backbone from agent to printable geometry. | STALE |
| `skills/use-spatiallm/SKILL.md` | photo/scan input → construction route | LLM for structured indoor modeling — point cloud/scene to walls, doors, and furniture layout as structured output. | fresh |
| `skills/use-seamly2d/SKILL.md` | garment route (patterns, markers, interop) | Open-source parametric pattern-making CAD — the most active open pattern tool. | fresh |
| `skills/use-garmentcode/SKILL.md` | garment route (patterns, markers, interop) | Sewing patterns as programs — the substrate the AI pattern-generation wave targets. | fresh |
<!-- END:satellite-routes -->

## 3. Self-heal & self-improve (protocols, not adjectives)

- Unknown room/garment/opening type ⇒ the gate fails it as not-measured —
  **propose the missing `data/*.yml` table entry; never fake a pass.**
- A referenced file missing ⇒ fall back to `llms.txt`, file a repo issue.
- Every run ends by banking what was learned **in the repo**: missing
  constraint → `data/*.yml` PR · false-READY → gate-dispute issue
  (`.github/ISSUE_TEMPLATE/gate-dispute.md`) · recurring brief type → new
  golden example. Measured by artifacts, not intentions.

## Verification (eval-with-teeth)

This skill's own integrity is CI-tested — `python3 -m pytest tests/test_skill.py -q`
asserts every repo path referenced above exists (the skill cannot drift from
the engine), the description stays within Anthropic's budgets, and the body
stays under 500 lines. Behavioral eval scenarios (routing, honesty, trigger
accuracy incl. should-NOT-trigger) live in `skills/design-anything/evals/evals.json`
— schema and fixture integrity CI-gated by `tests/test_skill_evals.py`; run
model-graded passes via the skill-creator plugin. A design run's success is
verified ONLY by its gate's exit 0 — never by this skill's say-so.

## Honest edges

Gates verify buildable/printable/cuttable — not *good* (principles cover
taste) and not *certified* (construction ⇒ not a permit; garment ⇒ not a
muslin; jurisdiction codes and real fittings override). Say so when it matters.
