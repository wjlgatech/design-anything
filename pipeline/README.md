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
| **Construction** | ✅ v0.1 (`construction_gate.py`) | C1 topology · C2 clearances vs [`data/clearances.yml`](../data/clearances.yml) (Neufert/IRC/ADA lineage) · C3 habitability (area, dimension, daylight, ceiling) · C4 egress connectivity · C5 ISO 2848 module grid. Explicitly ≠ permit/PE stamp. Roadmap: IFC validity (ifcopenshell), span tables, shearing-layer audit |
| **Garment** | ✅ v0.1 (`pattern_gate.py`) | F1 pieces + grain · F2 fabric fit (bbox-level) · F3 seam allowance · F4 zero-waste marker efficiency · F5 fit tables vs [`data/garment.yml`](../data/garment.yml). Not a muslin. Roadmap: DXF-AAMA export, size-run grading, seam-line matching |
| **Game/sim** | ✅ v0.1 (`scene_gate.py`) | S1 glTF 2.0 structure (buffers/accessors consistent) · S2 poly budget vs [`data/scene.yml`](../data/scene.yml) target · S3 true scale (meters declared, extent sanity) · S4 collision node present. Roadmap: USD, materials/textures, draw-call budgets |

## Interface bets (the Lindy rule)

Emit the formats that survived 10-30 years of churn: **STL + 3MF** (print),
**IFC** (construction), **glTF + USD** (game/sim). The AI generation layer is
hot-swappable by design — it has already churned once (NeRF→3DGS) while these
formats sat still.
