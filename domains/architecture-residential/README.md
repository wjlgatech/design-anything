# Residential architecture — 3D printing + AI

**Input:** site + program text, sketch/photo → **Output:** IFC blueprint + printable wall geometry, execution-ready.

## The stack (evidence-ranked)
- **Layout AI:** Autodesk Forma Building Layout Explorer (free with Revit, 2026), Finch3D, ARCHITEChTURES; OSS floor-plan generation is stale — **the open lane this repo targets**.
- **3DCP:** COBOD (arm-the-builder survivor), ICON Titan/Vitruvius (~250 structures), WASP (earth materials).
- **Interchange:** IFC (30-year survivor, legally mandated in several countries) — the survival-grade output format.
- **Research anchors:** Gramazio Kohler + Block Research Group (ETH), TopOpt (DTU) for structural validation.

## Governing principles
- **P7 print the walls, buy the windows** — open-system prefab survived (Sears, Crystal Palace); closed systems died (Lustron, Katerra). Printed structure must interface with standard trades.
- **P8 shearing layers** — the critical caution for monolithic printed walls: services in accessible chases, mechanical fastening over bonding.
- **P2 tables are law** — Neufert clearances, ISO 2848 module, stair geometry, ADA/ISO 21542 anthropometrics.
- **P9/P10** — climate-conditioned form (printed earth/concrete = free thermal mass), daylight per habitable room as a gate, courtyard as first-class parti for deep/private lots.

## Ready gate (roadmap — the flagship)
IFC validity (ifcopenshell) · clearance-table audit · span sanity · daylight orientation check · code checklist (explicitly ≠ PE stamp) · print-path continuity for the declared printer.
