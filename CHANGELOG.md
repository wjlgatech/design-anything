# Changelog

All notable changes to design-anything. Format: [Keep a Changelog](https://keepachangelog.com/), newest first.

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
