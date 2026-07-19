# TRELLIS.2 — knowledge digest
> Pinned to microsoft/TRELLIS.2 @ 75fbf0183001 (read 2026-07-19). Claims below are true of THIS sha; check the satellite status before trusting on a moved HEAD.

## What it is
- 4B-parameter image→3D generative model (MIT license) built on **O-Voxel**: a "field-free" sparse-voxel representation using a Flexible Dual Grid (enhanced-QEF) instead of SDF/occupancy fields, so it natively handles open surfaces, non-manifold geometry, and internal enclosed structures.
- Input: one image (PIL). Output: textured mesh with volumetric PBR attributes (base color, roughness, metallic, opacity), exportable to GLB with baked textures.
- Weights: `microsoft/TRELLIS.2-4B` on Hugging Face; resolutions 512³–1536³ (~3s / ~17s / ~60s on H100 per their README).

## Architecture map
- `trellis2/pipelines/` — orchestration. `trellis2_image_to_3d.py` (`Trellis2ImageTo3DPipeline.run()`, pipeline_type: `'512' | '1024' | '1024_cascade' | '1536_cascade'`) and `trellis2_texturing.py` (shape-conditioned PBR texture generation).
- `trellis2/models/` — the nets: sparse-structure VAE + flow, SC-VAEs (Sparse 3D VAE, 16× downsampling), structured-latent flow DiTs (~1.3B each stage; 3-stage: sparse structure → shape SLat → texture SLat).
- `trellis2/representations/` — mesh + voxel representations (`MeshWithVoxel` is what `run()` returns).
- `o-voxel/` — standalone pip-installable core library (`o_voxel`): mesh↔O-Voxel bidirectional conversion (<10s CPU in, <100ms CUDA out), `.vxz` compression, and `o_voxel.postprocess.to_glb()` (decimation, remeshing, UV unwrap, texture baking).
- `data_toolkit/` — training-data prep (voxelize, encode latents, render conditions); only needed for training/fine-tuning via `train.py` + `configs/`.
- External CUDA/Triton deps by same team: **FlexGEMM** (sparse conv), **CuMesh** (decimation/remesh/UV), plus NVlabs nvdiffrast/nvdiffrec (renderers, separate licenses).

## How to drive it
Requirements as stated: **Linux only**, NVIDIA GPU with **≥24 GB VRAM** (verified on A100/H100), CUDA Toolkit ~12.4 to compile extensions, Python ≥3.8, conda recommended.

```sh
git clone -b main https://github.com/microsoft/TRELLIS.2.git --recursive
cd TRELLIS.2
. ./setup.sh --new-env --basic --flash-attn --nvdiffrast --nvdiffrec --cumesh --o-voxel --flexgemm
```

Minimal image→GLB (their `example.py`, condensed):

```python
import os
os.environ['OPENCV_IO_ENABLE_OPENEXR'] = '1'
os.environ["PYTORCH_CUDA_ALLOC_CONF"] = "expandable_segments:True"
from PIL import Image
from trellis2.pipelines import Trellis2ImageTo3DPipeline
import o_voxel

pipeline = Trellis2ImageTo3DPipeline.from_pretrained("microsoft/TRELLIS.2-4B")
pipeline.cuda()
mesh = pipeline.run(Image.open("input.png"))[0]   # pipeline_type default; '512'|'1024'|'1024_cascade'|'1536_cascade'
mesh.simplify(16777216)                            # nvdiffrast face limit
glb = o_voxel.postprocess.to_glb(
    vertices=mesh.vertices, faces=mesh.faces, attr_volume=mesh.attrs,
    coords=mesh.coords, attr_layout=mesh.layout, voxel_size=mesh.voxel_size,
    aabb=[[-0.5, -0.5, -0.5], [0.5, 0.5, 0.5]],
    decimation_target=1000000, texture_size=4096,
    remesh=True, remesh_band=1, remesh_project=0)
glb.export("sample.glb", extension_webp=True)
```

Web demos: `python app.py` (image→3D), `python app_texturing.py` (texturing).

## Design-anything fit
- Feeds the **3D-printable / mesh route**: image brief → TRELLIS.2 GLB → our mesh ingest → **ready_gate** (watertight, clearances) before STL emission.
- Honest note: O-Voxel's headline feature — open surfaces and non-manifold geometry — is exactly what a watertight gate rejects. Generated meshes should be assumed **non-watertight by default** and routed through repair (remesh/manifold fix; `to_glb(remesh=True)` helps but is a texturing-oriented remesh, not a watertightness guarantee — UNVERIFIED that its output passes any watertight check) before ready_gate.
- Texturing pipeline (`example_texturing.py`) is a possible secondary route: apply PBR materials to an already-gated parametric mesh for visualization; irrelevant to gate verdicts.
- Not a source of dimensioned/parametric geometry — outputs are sculptural, unit-free (AABB-normalized to [-0.5, 0.5]³); scale must be assigned downstream before clearance checks.

## Gotchas
- Linux-only per README; heavy source-compiled CUDA extensions (flash-attn, nvdiffrast, nvdiffrec, cumesh, o-voxel, flexgemm) — install is slow and CUDA_HOME-sensitive; clone must be `--recursive` (submodules).
- flash-attn default; GPUs without it (e.g., V100) need manual `xformers` install + `ATTN_BACKEND=xformers`.
- `OPENCV_IO_ENABLE_OPENEXR=1` must be set before cv2 import (HDRI envmaps are .exr).
- nvdiffrast cap: call `mesh.simplify(16777216)` before rendering.
- GLB exports in OPAQUE mode — alpha is baked into the texture but not wired to material opacity; connect manually in DCC tools.
- 24 GB VRAM floor; higher-res cascade pipelines auto-downshift resolution when token count exceeds `max_num_tokens` (49152 default), printing a warning.
- Issue-tracker gotchas: UNVERIFIED (shallow clone; issues not read).

## Verify
```sh
python example.py   # from repo root; success = sample.mp4 + sample.glb produced
```
