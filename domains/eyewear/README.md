# Eyewear — the first body-fit domain

**Input:** face measurements (PD, bridge fit) or face scan → **Output:** fit spec + printable frame components, both gated.

This is the [Tier-2 body-fit pattern](../../docs/DESIGN_DISCIPLINES.md) made concrete:
**anthropometric tables + parametric-from-measurements + print gate** — the same
shape dental, prosthetics, and footwear will reuse.

## The stack (conservative claims; UNVERIFIED where not re-checked)

- **Standards lineage:** ISO 12870 (spectacle-frame requirements), ISO 8624 (boxed
  measuring system — the A/B/DBL dimensions the gate uses). https://www.iso.org/standard/69968.html
- **Mass-custom 3D-printed eyewear, survived:** Hoya/Materialise **Yuniku**
  (scan-based parametric frames, in market since 2016-17). https://www.materialise.com/en/industrial/software/yuniku-3d-tailored-eyewear
- **Print-native frame brands** (Monoqool-class SLS nylon) — active niche;
  UNVERIFIED current momentum, not tiered.
- **Scan → parametric:** the scene-to-layout pattern applies (photo + one
  reference measurement); phone LiDAR face scans are the input trend.

## Governing principles

- **P2 tables are the database** — PD/bridge/lens/temple ranges live in
  [`data/bodyfit.yml`](../../data/bodyfit.yml) with sources; a spec outside them is a bug.
- **The optical-fit rule (B3):** frame PD (lens_w + bridge) must sit within the
  decentration budget of the wearer's PD — the dispensing rule as a number.
- **P3 design for the machine:** temple/hinge cross-sections below the print
  floor snap in use; the floor is a table value, not a preference.
- **Two artifacts, two gates** — the fit spec gates against tables
  (`bodyfit_gate.py`); the geometry gates against physics (`ready_gate.py`).
  A frame that fits but won't print fails; so does one that prints but won't fit.

## Ready gate — bodyfit gate v0.1 (`pipeline/bodyfit_gate.py`)

B1 completeness (undeclared ⇒ not measured ⇒ fail) · B2 anthropometric/ISO
ranges · B3 frame-PD alignment budget · B4 print floor. Golden example:
[`examples/eyewear/`](../../examples/eyewear/generate.py) — fit spec + temple
blank STL, each passing its gate. Roadmap: face-scan intake, pantoscopic/wrap
angles, hinge geometry, dental/prosthetic/footwear siblings.
