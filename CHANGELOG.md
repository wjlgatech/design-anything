# Changelog

All notable changes to design-anything. Format: [Keep a Changelog](https://keepachangelog.com/), newest first.

## [0.9.0] — 2026-07-19

### Added
- **Pattern-gate deepening v0.2** (GOAL.md M12 — production-real garments):
  - **Size grading**: `examples/apron/generate.py` grades S/M/L (ASTM D5585 lineage, `--size` flag); every size passes the gate independently and grading is monotonic, by test — "a pattern that can't grade is a demo."
  - **F6 seam/symmetry pairs**: declared pairs must match in length within tolerance — the check that catches grading breaking symmetric pieces; missing pieces are not-measured ⇒ fail, zero declared pairs is a vacuous pass with honest detail.
  - **DXF-AAMA export** (`pipeline/dxf_aama.py`): the load-bearing AAMA subset every pattern CAD imports (closed-POLYLINE boundary on layer 1, grain line on layer 7, annotation on layer 15, mm units) — **verified by round-trip parse, never by claim**, and wired into `make check`.
  - 9 new tests (`tests/test_dxf_and_grading.py`); the full size run + export exercised end-to-end.
- **Honest deferral**: GarmentCode emission moved to M12b — without the upstream library, an emitter would be an unverifiable claim. Roadmap re-ranked: M8 (IFC) is now priority 1.

## [0.8.0] — 2026-07-18

### Added
- **Game/sim scene gate v0.1** (GOAL.md M7 — the last roadmap gate; every pipeline route is now verifiable): `pipeline/scene_gate.py` + `data/scene.yml` — S1 glTF 2.0 structure (buffers decode to declared lengths, accessors fit views), S2 poly budget vs declared target platform, S3 true scale (meters declared + extent sanity — the units-bug catcher), S4 collision node present. Built as a `Gate` subclass (the v0.7.0 seam paying off).
- **Golden example #4**: `examples/arena/` — parametric 40m courtyard arena (50 tris, walls, collision node) emitting valid glTF 2.0 with embedded buffers; 9 tests with 7 known-bad mutations (`tests/test_scene_gate.py`).
- **New skill**: `scene-ready-check` (10 skills total); flagship routing table updated — the game route now gates instead of declaring an honest gap; eval scenario updated to match; garment row added to the pipeline gate table (a v0.3.0 doc gap caught during wiring).
- **Roadmap prioritized by ROI** in GOAL.md: M12 (DXF-AAMA + grading) → M8 (IFC) → M11 (body-fit domain) → M9 (knowledge map).

## [0.7.0] — 2026-07-18

### Changed
- **OOP refactor around the `Gate` seam** (GOAL.md M16): new `pipeline/gate.py` — `CheckResult`, abstract `Gate` (named checks → honest report → shared CLI/exit surface). All three gates are now classes (`PrintReadyGate`, `ConstructionGate`, `PatternGate`) with one method per check; the two 80-94-line god-functions are gone; module-level `run_gate()` entry points kept stable for tests/skills/evals. `anyagent analyze`: **50 → 83** (typing/function-size/nesting/testing at 100%; remaining "structure" findings declined as over-engineering for compiler scripts).
- `scripts/validate.py` flattened into per-concern check functions (nesting finding closed); full type annotations across pipeline, scripts, and example generators.

### Added
- **AI-native self-audit in CI** (the FM-os rubric-as-data pattern): `data/ainative.yml` — 12 operating principles (spec-as-data, drift-gate, ready-is-a-gate, no-evidence⇒no, maker≠checker, eval-with-teeth, golden-examples, honest-edges, compounding-memory, human-gated-irreversible, state-outside-the-window, skill-cannot-drift), each with in-repo evidence probes; `scripts/ainative.py` scores them (currently 12/12, gate 90) and **fails `make check` on a regression in how the repo operates**, not just what the code does. Audited by `tests/test_ainative.py` including the no-fake-pass property.

## [0.6.0] — 2026-07-18

### Added
- **📰 News section** (GOAL.md M15) — significant updates curated in `data/news.yml` (date/title/note/link, newest-first enforced by `scripts/validate.py`), compiled into README under the drift gate like every other table. Seeded with the v0.1.0–v0.5.0 release history.
- **Architecture — the system design**: a brand-themed Mermaid diagram of the two coupled loops (research compresses → data spine → pipeline expresses → gates → disputes feed back).
- **A diagram on every major section** (6 total, Anthropic palette per anyagent's brand-as-code): pipeline flowchart (replaces the ASCII art), DIKW compression↔expression loop, three-window research funnel, skill-routing map, contribution flywheel.
- **CI keeps the visuals honest**: `test_readme_visuals_and_news` asserts ≥6 mermaid blocks each carrying the brand init header + news markers present; diagrams verified with `anyagent brand --check`.

## [0.5.0] — 2026-07-18

### Added
- **Skill eval scenarios** (GOAL.md M14) — `skills/design-anything/evals/evals.json`, skill-creator-compatible: 10 scenarios covering every gated route (print/construction/garment), the honest-gap game route, photo input, the one-fork-question discipline, the curated-index answer path, an honest-NOT-READY case against a real broken fixture, and 2 should-NOT-trigger cases (logo, database schema) measuring the description's NOT-for clause.
- **`tests/test_skill_evals.py`** — the deterministic slice CI can enforce: schema validity, both trigger classes present, every gated route exercised, fixtures exist, and `broken-hole.stl` **provably fails G1** (an eval against a healthy fixture would be a fake test).
- `.gitignore` exception so the eval fixture STL ships with the repo.

## [0.4.0] — 2026-07-18

### Added
- **`/design-anything` flagship skill** (GOAL.md M13) — `skills/design-anything/SKILL.md`, built to Anthropic's skill-authoring guidance (≤500-line body, third-person ≤1024-char description with triggers + NOT-for, references one level deep, dynamic engine probe). A **thin router over this engine**: intent discovery (≤2 questions at genuine forks, visible defaults), the absorb→route→retrieve→compose→gate→reflect backbone, per-target routing table as progressive disclosure.
- **Self-aware / self-heal / self-improve as protocols, not adjectives** (`docs/SKILL_DESIGN.md`): capabilities read from artifacts (`llms.txt`, gate table, `make check`); red-check-first, 3-strike escalation, not-measured⇒fail+propose-the-table; lessons bank as repo artifacts (data PRs, gate-dispute issues, golden examples).
- **`tests/test_skill.py`** — the skill's integrity is CI-gated: every referenced engine path must exist (no drift), Anthropic budgets enforced, registry entry required.
- Installed to `~/.claude/skills/design-anything` by symlink — one source of truth; updates flow with `git pull`.

## [0.3.0] — 2026-07-18

### Added
- **Garment & cloth design domain** (GOAL.md M10): `domains/garment-design/` guide + full three-window research digest (RESEARCH.md — sewing patterns as the AI↔manufacturing interchange; GarmentCode + DXF-AAMA as the load-bearing formats; RTFKT joins the anti-portfolio at −99.8%).
- **Pattern gate v0.1** (`pipeline/pattern_gate.py`) + `data/garment.yml` tables: pieces+grain, fabric fit, seam allowance, marker efficiency (zero-waste as a number), human-fit tables. Golden example #3: `examples/apron/` (5 pieces, 67% marker efficiency); 9 tests with 8 known-bad mutations.
- **`principles/DIKW_MODEL.md`** — the organizing mental model: DIKW compression (research → principles) ↔ expression (principles → gated artifacts), with the domain-inclusion rule.
- **`docs/DESIGN_DISCIPLINES.md`** — the map of design-centric disciplines in three tiers: covered, gateable-next (dental/prosthetics/footwear lead — where 3D printing already won), and design-dominated-but-non-spatial (chip design's DRC as the strongest external validation of the gate thesis).
- **`principles/DESIGN_THINKING.md`** — design thinking survival-tiered: Simon/Rittel kernel 🏛, d.school/Double Diamond 🌳, workshop theater ⚠️ (critique wave cited); the kernel mapped to repo practice.
- **New skill**: `garment-ready-check` (8 skills total); 6 garment tools, 6 papers/standards, 6 people/labs added to the data layer.

## [0.2.0] — 2026-07-18

### Added
- **Construction ready-gate v0.1** (`pipeline/construction_gate.py`) — GOAL.md M5, the flagship: validates rooms+openings layouts against `data/clearances.yml` (Neufert/IRC/ADA-lineage tables as data). Five gates: topology, clearances, habitability (area/dimension/daylight/ceiling), egress connectivity, ISO 2848 module grid. Unknown types are not-measured ⇒ fail; every report carries the not-a-permit disclaimer.
- **`data/clearances.yml`** — the constraint database (principle P2: tables beat slogans), each value with its source.
- **Golden example #2**: `examples/studio-flat/` — parametric 28.5 m² floor plan passing all five construction gates; 9 tests including 7 known-bad mutations that must fail (`tests/test_construction_gate.py`).
- **`llms.txt`** (M6) — flat token-cheap agent index compiled from `data/*.yml`, covered by the CI drift gate.
- **New skill**: `construction-ready-check` (7 skills total, registered + dogfooded).
- **M4 flywheel**: issue templates (new-entry, new-skill, gate-dispute), PR template with the make-check checklist, GitHub Release.

### Changed
- `make check` now runs both golden slices through their gates; GOAL.md milestone table gains statuses + M5–M9 roadmap.

## [0.1.0] — 2026-07-18

### Added
- **GOAL.md** — the original request evaluated and 10X'd into a machine-verifiable contract; "ready" defined as per-target gates.
- **pipeline/ready_gate.py** — stdlib-only 3D-print ready gate: watertight 2-manifold, outward normals (signed volume), bed-fit, min-feature. Exit code gates CI.
- **examples/planter/** — golden vertical slice: text brief → parametric solid → STL, passing the full gate; volume verified against analytic ground truth.
- **Three-window research digests** (`research/`): last30days (engagement, verified 2026-07-18), last30years (survival test with anti-portfolio), last300years (civilizational endurance with Whig-history guard).
- **principles/DESIGN_PRINCIPLES.md** — P1–P13, each traceable to its evidence window; gate-convertible principles marked.
- **best-practices/BEST_PRACTICES.md** — 17 practices inherited from animate-anything and FM-os, adapted to blueprint work.
- **Spec-as-data**: `data/*.yml` (tools, papers, community, registry, meta) → generated README tables with a CI drift gate (`scripts/build_readme.py --check`).
- **Six skills** with eval-with-teeth Verification sections: brief-to-blueprint, print-ready-check, blueprint-validate, pattern-library, scene-to-layout, design-research.
- **bundles/design-from-brief.yaml** — the flagship skill composition; **workflows/** — dynamic orchestration shapes (design-review-panel, survey-the-field).
- **Six domain guides**: game design, simulation, residential/commercial architecture (3DCP+AI), interior design, landscape.
- **Verification harness**: `make check` = schema validation + pytest + README drift gate + ready gate on the golden example; GitHub Actions CI.
