# pipeline — input → blueprint → ready gate

```
text | image → brief (schema) → parametric model (source) → 3D blueprint → READY-GATE
```

## The contract

1. **Input**: text brief and/or picture. Pictures become structured layouts via
   skills/scene-to-layout before any generation.
2. **Blueprint = composition, not render**: deterministic parametric source
   with the brief's parameters at the top (see `../examples/planter/generate.py`).
   Meshes (STL/3MF), IFC, and glTF/USD are compiled artifacts.
3. **Ready is a gate, not a vibe**: `ready_gate.py` is the acceptance test.
   Exit 0 = READY. No evidence ⇒ Not ready.

## Gates by target

| Target | Status | Checks |
|---|---|---|
| **3D-print** | ✅ v0.1 (`ready_gate.py`) | G1 watertight 2-manifold · G2 outward normals (signed volume) · G3 bed-fit · G4 min-feature ≥ 2× nozzle |
| **Construction** | 🚧 roadmap (GOAL.md) | IFC validity (ifcopenshell) · span/clearance sanity tables · code-compliance checklist (IBC/IRC refs, explicitly ≠ PE stamp) · shearing-layer audit |
| **Game/sim** | 🚧 roadmap | glTF/USD validation · poly/texture budget · true-to-scale units · collision mesh present |

## Interface bets (the Lindy rule)

Emit the formats that survived 10-30 years of churn: **STL + 3MF** (print),
**IFC** (construction), **glTF + USD** (game/sim). The AI generation layer is
hot-swappable by design — it has already churned once (NeRF→3DGS) while these
formats sat still.
