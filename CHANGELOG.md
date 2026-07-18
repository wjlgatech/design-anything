# Changelog

All notable changes to design-anything. Format: [Keep a Changelog](https://keepachangelog.com/), newest first.

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
