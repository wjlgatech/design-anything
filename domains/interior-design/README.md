# Interior design — furniture, decoration, kitchen, bedroom, living room, balcony

**Input:** room photo/scan or text brief → **Output:** structured layout + printable furniture/fixture blueprints.

## The stack (evidence-ranked)
- **Scene understanding:** SpatialLM (NeurIPS 2025, active) — photo/scan → walls, doors, furniture as structured output; the most repo-relevant OSS in the domain.
- **Visualization:** Spacely AI (element-level masking), Planner 5D AI.
- **Furniture generation:** TRELLIS.2 / Meshy-6 for meshes; OpenSCAD/CadQuery for **printable parametric** furniture (the execution-ready path).

## Governing principles
- **P2 Neufert/Panero tables are the database** — work-triangle limits in kitchens, 900mm circulation, seat heights, counter depths, reach zones. A violating layout is a bug.
- **Thonet/Shaker/Eames lineage (P12)** — minimize part count, design for disassembly, integrated storage, iterate against body models; ornament justifies itself or is omitted.
- **Ma — budget negative space deliberately** (400 years of continuous practice); don't fill every void.
- **P10 daylight** — reading corners, work surfaces, and beds placed against orientation, not walls-of-convenience.

## Room-specific gate seeds (roadmap)
Kitchen: work triangle 4-7.9m, landing zones beside appliances. Bedroom: bed clearance ≥ 750mm on access sides. Living: conversation distance ≤ 3.5m, circulation never through it. Balcony: the six-foot-minimum pattern (Alexander) — narrower balconies go unused.
