# SpatialLM — knowledge digest
> Pinned to manycore-research/SpatialLM @ 8913c44d84a4 (read 2026-07-19). Claims below are true of THIS sha.

## What it is
SpatialLM is a 3D large language model (NeurIPS 2025) that takes an indoor point cloud and generates a structured scene description: walls, doors, windows, and oriented object bounding boxes with semantic categories.
It works on point clouds from diverse sources — monocular video SLAM (MASt3R-SLAM, SLAM3R), RGBD, LiDAR — no specialized capture rig required.
The LLM emits the layout as Python-dataclass-style text (SceneScript-derived "language string"), which the repo parses back into geometry.

## Architecture map
- **Model variants** (all on Hugging Face under `manycore-research/`):
  - `SpatialLM1.1-Llama-1B` (Llama3.2-1B-Instruct base), `SpatialLM1.1-Qwen-0.5B` (Qwen-2.5 base) — current, 2x point-cloud resolution, category-conditioned detection.
  - `SpatialLM1.0-Llama-1B` (`SpatialLM-Llama-1B`), `SpatialLM1.0-Qwen-0.5B` (`SpatialLM-Qwen-0.5B`) — legacy.
- **Point-cloud encoder**: SpatialLM1.0 uses the SceneScript encoder (`spatiallm/model/scenescript_encoder.py`, needs torchsparse); SpatialLM1.1 uses Sonata (`spatiallm/model/sonata_encoder.py`, Pointcept-based, needs flash-attn). Encoder output is projected into the LLM embedding space (`point_proj` Linear) and spliced in at `<|point_start|><|point_pad|><|point_end|>` in the prompt (`spatiallm/model/spatiallm_qwen.py`, `spatiallm_llama.py`).
- **Output schema** (`code_template.txt`, parsed by `spatiallm/layout/`): text lines
  - `wall_N=Wall(ax,ay,az,bx,by,bz,height,thickness)` — wall as a 3D segment + height/thickness
  - `door_N=Door(wall_id,position_x,position_y,position_z,width,height)` — attached to a wall by id; same for `Window`
  - `bbox_N=Bbox(class,position_x,position_y,position_z,angle_z,scale_x,scale_y,scale_z)` — z-rotated oriented box, one of 59 furniture categories
- Coordinates are generated as discretized bins and converted to meters by `Layout.undiscretize_and_unnormalize()` using `NORMALIZATION_PRESET` (world 0–32 m, height/width 0–25.6 m, scale 0–20 m; `spatiallm/layout/entity.py`), then translated back by the scene's min extent.

## How to drive it
- Install (their tested env: Python 3.11, PyTorch 2.4.1, CUDA 12.4):
  ```bash
  conda create -n spatiallm python=3.11 && conda activate spatiallm
  conda install -y -c nvidia/label/cuda-12.4.0 cuda-toolkit conda-forge::sparsehash
  pip install poetry && poetry config virtualenvs.create false --local
  poetry install
  poe install-torchsparse   # SpatialLM1.0 only
  poe install-sonata        # SpatialLM1.1 only (builds flash-attn)
  ```
- Weights auto-download from Hugging Face via `AutoModelForCausalLM.from_pretrained(model_path)`.
- Minimal inference (`inference.py`; model is moved to `"cuda"` unconditionally — a CUDA GPU is required; default dtype bfloat16, point backbone forced to float32):
  ```bash
  python inference.py --point_cloud pcd/scene0000_00.ply --output scene0000_00.txt \
    --model_path manycore-research/SpatialLM1.1-Qwen-0.5B
  ```
- Task modes via `--detect_type {all,arch,object}` (all=walls+doors+windows+boxes; arch=layout only; object=boxes only) and `--category bed nightstand ...` to restrict to a subset of the 59 categories (SpatialLM1.1). Generation is sampling-based (temp 0.6, top_p 0.95, top_k 10); pass `--seed` for reproducibility. No explicit VRAM figure is stated in the README (UNVERIFIED beyond "CUDA required").

## Design-anything fit
- Natural backend for a scene-to-layout skill: point cloud in → `Layout` object with walls/doors/windows/bboxes in meters, z-up.
- Mapping to our rooms+openings layout JSON needs work: SpatialLM outputs a flat wall list (3D segments), NOT room polygons — we must assemble closed room loops from wall segments ourselves (adjacency/graph closure), and there is no explicit room entity or floor/ceiling.
- Openings map cleanly: Door/Window carry `wall_id` + center position + width/height — convertible to our per-wall opening offsets for construction_gate (egress/clearance checks). Wall `thickness` is predicted but `Layout.to_boxes()` currently hardcodes thickness 0.0 when boxing walls (`spatiallm/layout/layout.py` line ~116) — read thickness from the entity, not from to_boxes.
- Furniture bboxes (class, center, yaw, scale) can seed clearance checks and furnishing layers.
- Output is probabilistic text: entities referencing nonexistent walls are silently dropped by the parser; our adapter should validate counts and re-run with a seed on failure.

## Gotchas
- Input must be a **.ply point cloud, axis-aligned, z-up**, following the ScanNet alignment convention (walls parallel to x-y planes); misaligned clouds need Manhattan-frame estimation first (EXAMPLE.md).
- **Metric scale required**: 1 unit = 1 meter. SLAM outputs often need rescaling (README suggests normalizing to ~2.5 m wall height). World coordinates are normalized into a 0–32 m box — scenes larger than 32 m won't fit the preset.
- Preprocessing is built in: `cleanup_pcd` voxel-downsamples at the model's grid size and removes statistical outliers; colors are expected (encoder consumes coord+color).
- The generated layout is relative to the cloud's min corner (`PositiveShift`); `inference.py` translates it back — replicate this if bypassing the script.
- **License**: Llama-1B weights under the Llama 3.2 Community License (repo LICENSE.txt is the Llama agreement); Qwen-0.5B derived from Apache-2.0 Qwen-2.5. Point encoders: SceneScript (1.0) and Sonata weights (1.1) are **CC-BY-NC-4.0 — non-commercial**; Pointcept-derived code Apache-2.0. Commercial use of the shipped encoder weights is restricted.

## Verify
```bash
huggingface-cli download manycore-research/SpatialLM-Testset pcd/scene0000_00.ply --repo-type dataset --local-dir .
python inference.py --point_cloud pcd/scene0000_00.ply --output scene0000_00.txt --model_path manycore-research/SpatialLM1.1-Qwen-0.5B
python visualize.py --point_cloud pcd/scene0000_00.ply --layout scene0000_00.txt --save scene0000_00.rrd && rerun scene0000_00.rrd
```
Not executed in the digest run (no CUDA GPU on that machine) — command verified against README and `inference.py` argparse at this sha.
