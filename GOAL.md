# GOAL.md — the 10X contract for design-anything

> The original request, evaluated and recompiled into a machine-verifiable contract.
> Discipline: `/10xgoal` + `anyagent goal` (goal-10x loop).

## 1. The original request (verbatim intent)

Use `animate-anything` and `FM-os` as templates → create a public repo `design-anything` with
design principles, best practices, AI tooling (skills, plugins, bundles, dynamic workflows),
community of influential figures/labs. Cover game design, 3D simulation, residential + commercial
architecture (3D printing + AI focus), interior design (furniture, decoration, kitchen, balcony,
bedroom, living room, garden, landscape). Input: text, picture. Output: 3D blueprint that is
execution/construction/3D-print ready. Research academic publications, repos, people, labs with
high reputation. Use /last30days /last30years /last300years for deep research.

## 2. Eval — what's strong, what breaks

| Verdict | Finding |
|---|---|
| ✅ Strong | The "-anything" framing (any input → verified output) is a proven pattern from the template repos. |
| ✅ Strong | Three-window research (30 days / 30 years / 300 years) forces both freshness and survival-tested truth. |
| ⚠️ Bundled | This is ~6 goals in one: repo + research + tooling + community + pipeline + eval. Un-bundled below into gated milestones. |
| ⚠️ Unmeasurable | "execution-construction-3D_print ready" had no acceptance test. **This is the single most important fix** — without it, every output is vibes. Defined as machine-checkable gates in §3. |
| ⚠️ Unbounded | 6+ domains at equal depth in v0.1 = shallow everywhere. Fixed: one **vertical slice** that works end-to-end, other domains as researched-but-thin guides that deepen per release. |
| ⚠️ Missing finish line | No verification harness. Fixed: `make check` gates the repo (structure, links, schema, geometry tests). |

## 3. The 10X move

**The 10X is not more domains — it is making "ready" verifiable and the repo executable.**

A 1X repo is a curated list of links. The 10X repo is a **design compiler**:

```
text | image  →  brief (schema-validated)  →  parametric model  →  3D blueprint
                                                                      │
                                              READY-GATE (machine-checkable, per target)
                                              ├─ 3D-print:   watertight/manifold mesh, min wall ≥ nozzle×2,
                                              │              overhang ≤ 45° or supported, bed-fit, 3MF/STL valid
                                              ├─ construction: IFC validity, structural sanity (span tables),
                                              │              code-compliance checklist (IBC/IRC refs), dimensioned plans
                                              └─ game/sim:   glTF/USD valid, poly budget, scale-true, collision mesh
```

No output may claim "ready" without passing its gate. **No evidence ⇒ Not ready** (BRACE rule).

## 4. Verifiable milestones (un-bundled)

| Milestone | Done means (machine-checkable) |
|---|---|
| **M0 — Repo live** | Public repo exists; `make check` passes in CI; README states the ready-gate contract. |
| **M1 — Knowledge base** | 3 research digests (30d/30y/300y) with ≥15 cited entries each; principles + best-practices docs; community roster with ≥20 verified people/labs, each with a URL. |
| **M2 — Tooling** | ≥6 SKILL.md skills, ≥1 bundle, ≥1 dynamic workflow — all schema-valid (tested by `make check`). |
| **M3 — Vertical slice** | One end-to-end demo: text brief → parametric model → STL/3MF that **passes the print gate** (watertight, wall-thickness, bed-fit) via `tests/test_ready_gate.py`. |
| **M4 — Community flywheel** | CONTRIBUTING.md with a skill-submission path; issues templated; first external-facing release tagged. |

## 5. Non-goals (v0.x)

- Photoreal rendering, VR walkthroughs, structural PE stamping (a checklist ≠ an engineer's seal — outputs say so explicitly).
- Hosting a generation service; the repo ships knowledge + skills + gates, not GPUs.

## 6. Standing rules inherited from the templates

- **Verify, don't vibe** — every push: review → test → docs → lint → live-verify (no-mistakes ship gate).
- **Grounded research only** — every claim carries a URL/date; unverifiable ⇒ marked UNVERIFIED, never presented as fact.
- **Skills are untrusted until read** — external skills are reviewed before install, ephemeral over persistent.
- **State outside the window** — long tasks tracked in checklists/git, one verified step at a time.
