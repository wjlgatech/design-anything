# Garment & cloth design

**Input:** design brief, reference photo, body measurements → **Output:** parametric sewing pattern + cut-ready marker (JSON now; DXF-AAMA/GarmentCode roadmap).

## The stack (evidence-ranked, full digest in [RESEARCH.md](RESEARCH.md))

- **Interchange formats (the load-bearing pair):** **GarmentCode** (ETH — patterns as programs, the substrate the AI wave targets) and **DXF-AAMA/ASTM D6673** (factory-native; formally withdrawn 2019 yet every CAD still speaks it — de facto formats outlive their standards bodies).
- **Open pattern CAD:** Seamly2D (913★, pushed today) — the most active open pattern tool; Freesewing (patterns as code, cooling).
- **AI pattern generation (the 2025-26 wave):** GarmentDiffusion (IJCAI 2025, cm-precise vectorized patterns), ChatGarment (CVPR 2025), Design2GarmentCode, DressWild — the field pivoted from mesh generation to **manufacturable pattern generation**, exactly this repo's bet.
- **Incumbent 3D CAD:** Marvelous Designer/CLO (2026.0: interaction bets, no headline AI), Browzwear (hybrid physics-AI), Style3D (most aggressive on AI; open-sourced GarmageNet).
- **Simulation survivors:** Baraff-Witkin implicit integration (1998, still canonical) → PBD/XPBD (what actually ships in engines); **SMPL** (2015) still the body-model standard.
- **Manufacturing wildcard:** unspun Vega — 3D-weaving shaped components directly from yarn, routing around cut-and-sew entirely ($32M Series B, Walmart pilot).

## Governing principles

- **A pattern is a function of measurements, not a fixed outline** — 19th-century proportional drafting systems are literally what GarmentCode reinvented. Emit parametric drafting rules (P5: patterns are the representation).
- **Grade or it's a demo** — a pattern that can't grade coherently across a size run (ASTM D5585 lineage) is not a product.
- **Grain is physics** (Vionnet's bias cut): the generator must reason about grainline and fabric anisotropy, not just silhouette.
- **Zero-waste is the loss function, not an afterthought** — kimono/sari were zero-waste by economics; industry markers waste 10-15%; McQuillan/Rissanen codified the discipline. The gate's F4 efficiency floor is this principle as a number.
- **Every seam must map to a machine operation** — sewing construction froze around the lockstitch 170 years ago; feasibility means assembly order, not just geometry (roadmap check).
- **The anti-portfolio:** RTFKT (garments as speculative assets, −99.8%) died; DressX (garments as try-on utility) survived. Digital garments are useful as *utility*, never as scarcity.

## Ready gate — pattern gate v0.1 (`pipeline/pattern_gate.py`)

F1 valid pieces + declared grain · F2 fabric-width fit + no overlaps (bbox-level) ·
F3 seam allowance ≥ table min · F4 marker efficiency ≥ floor (zero-waste as a number) ·
F5 human-fit vs `data/garment.yml` tables · F6 seam/symmetry pairs within tolerance.
Golden example: [`examples/apron/`](../../examples/apron/generate.py) — **graded S/M/L**,
every size gated independently (a pattern that can't grade is a demo).

**Factory export**: [`pipeline/dxf_aama.py`](../../pipeline/dxf_aama.py) emits the AAMA subset
every pattern CAD imports (boundary layer 1, grain layer 7, annotation layer 15, mm units) and
verifies by round-trip, never by claim. Roadmap: GarmentCode emission (deferred until the
upstream lib provides an honest verification path).
