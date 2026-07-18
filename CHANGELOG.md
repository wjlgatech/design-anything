# Changelog

All notable changes to design-anything. Format: [Keep a Changelog](https://keepachangelog.com/), newest first.

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
