# GarmentCode — knowledge digest
> Pinned to maria-korosteleva/GarmentCode @ d44962997902 (read 2026-07-19). Claims below are true of THIS sha.

## What it is
Sewing patterns as programs: a Python DSL/framework (`pygarment`, v2.0.2) for composing parametric sewing patterns from reusable components, from Korosteleva & Sorkine-Hornung at ETH Zurich (SIGGRAPH Asia 2023) plus GarmentCodeData (ECCV 2024), the made-to-measure dataset pipeline built on it.
It is the research substrate the text-to-pattern wave targets: garments are code, parameterized by a design YAML + body-measurement YAML, and serialized to a custom JSON pattern specification.
MIT-licensed; body-measurement extraction lives in a sibling repo (mbotsch/GarmentMeasurements); an online configurator demo runs at garmentcode.ethz.ch.

## Architecture map
- **`pygarment/garmentcode/`** — the DSL core, exported from `pygarment/__init__.py`: `Component` ("garment element (or whole piece) composed of simpler connected garment elements"), `Panel` (single flat fabric piece; a `BaseComponent`), `Edge` / `CircleEdge` / `CurveEdge` / `EdgeSequence`, `Interface` ("description of an interface of a panel or component that can be used in stitches as a single unit", with ruffle coefficient and right/wrong-side control), `Stitches` (connector.py), edge factories (`EdgeSeqFactory`, `CircleEdgeFactory`, `CurveEdgeFactory`), `operators`, and `BodyParametrizationBase` / `DesignSampler` (params.py).
- **`pygarment/pattern/`** — the JSON pattern representation: `BasicPattern` / `ParametrizedPattern` (core.py) and `VisPattern` (wrappers.py) which adds visualization/printable export via `serialize()`.
- **`pygarment/meshgen/`** — box-mesh generation + cloth simulation (`BoxMesh`, `run_sim`) on a custom NVIDIA Warp fork.
- **`assets/garment_programs/`** — garment library written in the DSL (bodice, tee, pants, sleeves, collars, skirts, godet, bands); `MetaGarment` is the top-level component that instantiates upper/bottom/waistband sub-garments from a design dict.
- **`assets/design_params/`** (`default.yaml`, `t-shirt.yaml`) and **`assets/bodies/`** (neutral/mean_female/mean_male/SMPL YAMLs + meshes) — design and body presets.
- **GUI**: `python gui.py` launches a NiceGUI web configurator (loads `assets/design_params/default.yaml`, shows pattern + draped 3D). GarmentCodeData generation is in-repo: `pattern_sampler.py`, `pattern_data_sim.py`, `pattern_fitter.py`.

## How to drive it
Install: `pip install pygarment`, or `conda create -n garmentcode python=3.9` then `pip install -e .`; create `system.json` from `system.template.json` (output/dataset paths). Simulation additionally needs the custom NvidiaWarp-GarmentCode build.
Minimal programmatic flow (from their `test_garmentcode.py`):
```python
from assets.garment_programs.meta_garment import MetaGarment
from assets.bodies.body_params import BodyParameters

body = BodyParameters('./assets/bodies/mean_all.yaml')          # body input
design = yaml.safe_load(open('./assets/design_params/t-shirt.yaml'))['design']
piece = MetaGarment('t-shirt', body, design)
pattern = piece.assembly()                                      # -> VisPattern
if piece.is_self_intersecting(): print('Self-intersecting')
folder = pattern.serialize(out_dir, to_subfolder=True, with_printable=True)
# writes <name>_specification.json (+ printable SVG/PDF outputs)
```
Body parameters are a flat YAML `body:` dict in cm/degrees (height, bust, waist, hips, shoulder_w, arm_length, ... ~26 keys in `mean_all.yaml`); `BodyParameters` (assets/bodies/body_params.py) subclasses `pyg.BodyParametrizationBase` and adds derived measurements. Design params use `{param: {v: value, range: [...], type: ...}}` YAML.

## Design-anything fit
- **M12b target**: our marker JSON ↔ their `*_specification.json` produced by `BasicPattern.serialize()` (pygarment/pattern/core.py:97) — panels with 2D edge outlines, 3D placement (translation/rotation), stitches list, and `panel_order`. That spec format is the ground-truth interchange to emit/parse.
- **Their body-params ≈ our fit tables**: a GarmentCode emitter maps our fit table rows onto the `body:` YAML keys and feeds `BodyParameters`; design intent maps onto `design_params` YAML consumed by `MetaGarment`.
- **Honest verification entry points at this sha**: (1) `Component.is_self_intersecting()` (pygarment/garmentcode/component.py, panel-level check; `Panel.is_self_intersecting()` at panel.py:56) and `BasicPattern.is_self_intersecting()` (pattern/core.py:490) for the serialized spec; (2) `serialize()` raises `RuntimeError` on empty patterns and `EmptyPatternError` exists in core.py; (3) `MetaGarment` raises `TotalLengthError` / `IncorrectElementConfiguration` for infeasible configs; (4) physical verification = drape via `python test_garment_sim.py -p <spec>.json -s <sim_props>` which logs fails/body_collisions/self_collisions stats. There is no single "validate(spec)" CLI beyond these — an emitter should round-trip through `BasicPattern` load + `is_self_intersecting()` and optionally sim.

## Gotchas
- Docs pin **Python 3.9** (setup.cfg loosely says >=3.6; 3.9 is what they test); **numpy<2** required.
- Heavy deps: CairoSVG (Windows quirks — they bundle DLLs in `pygarment/pattern/cairo_dlls`), trimesh, libigl, pyrender, cgal, nicegui, svgpathtools.
- Simulation requires their **custom NVIDIA Warp fork** (maria-korosteleva/NvidiaWarp-GarmentCode), built manually — not on PyPI.
- Scripts expect a machine-local `system.json` at repo root and repo root on `PYTHONPATH`; garment programs live under `assets/` (imported as `assets.garment_programs.*`), not inside the pip package.
- License: **MIT** (c) 2024 Maria Korosteleva — permissive; cite the two papers for research use.
- Some GUI elements solve optimization problems below realtime (sleeve curve inversion) — expect lag; UNVERIFIED whether headless `assembly()` for those elements is similarly slow.

## Verify
```bash
python test_garmentcode.py   # t-shirt on neutral body -> <output>/t-shirt_<ts>/..._specification.json + printable pattern
# optional physical check:
python test_garment_sim.py -p <spec>_specification.json -s ./assets/Sim_props/default_sim_props.yaml
```
