# /last30days — current landscape (verified 2026-07-18)

Method: web search + live GitHub API star/push checks. Ranked by observed
recency + engagement, not reputation. Unverifiable claims are marked UNVERIFIED.

## 1. Text-to-3D / Image-to-3D generation

| Rank | Tool | What it is | Evidence | Link |
|---|---|---|---|---|
| 🥇 | **Microsoft TRELLIS.2** | Open (MIT) 4B image-to-3D flow-matching model, "O-Voxel" rep, any topology, full PBR, 1536³, GLB/PLY/OBJ — pitched as print/production ready | Released 2025-12-18; 8,786★, pushed 2026-07-10 — fastest star velocity in the space | https://github.com/microsoft/TRELLIS.2 |
| 🥈 | **Rodin Gen-2.5** (Hyper3D/Deemos) | Commercial 3D generator, sculpt-level detail, >10M-poly raw outputs, 3D-native texturing | Launched 2026-05-26 (web/API/enterprise) | https://hyper3d.ai/blog/rodin-gen-2 |
| 🥈 | **Meshy-6** | Market-leader SaaS: text/image→mesh, PBR, auto-rig, Unity/Unreal/Godot plugins, multi-color 3D-print export | GA 2026-01-18 | https://www.meshy.ai/blog/meshy-6-launch |
| 🥉 | **Tripo v3.1 + Smart Mesh P1.0** | Fastest generation (~8s), game-dev focus, topology-aware meshing | Smart Mesh P1.0 shipped 2026-03 | https://www.tripo3d.ai/ |
| 🥉 | **Hunyuan3D-2 / 2.1** (Tencent) | Dominant fully-open asset generator (weights + training code, PBR) | 14,299★ but last push 2025-10-28 — momentum shifting to TRELLIS.2; HY3D-Bench dataset 2026-02-04 | https://github.com/Tencent-Hunyuan/Hunyuan3D-2 |
| 🥇 | **Zoo.dev Zookeeper / Text-to-CAD** | Conversational agent emitting true **parametric CAD** (STEP/DXF, dimensioned) — blueprints, not meshes | Shipped with Design Studio v1.1, 2026-01; open-source, self-hostable | https://zoo.dev/research/zookeeper |
| — | **AdamCAD** | YC W25 text-to-parametric-CAD, $4.1M raised | UNVERIFIED latest-release date | https://adamcad.com/ |

## 2. AI in architecture & construction 3D printing (3DCP)

| Rank | Player | What it is | Evidence | Link |
|---|---|---|---|---|
| 🥇 | **ICON** | ~250 printed structures; **Titan** multi-story robotic printing (to 9m, announced ~2026-03); **Vitruvius** AI architect (roadmap: permit-ready designs, budgets) | Apr-2026 industry reporting | https://www.iconbuild.com/newsroom/icon-unveils-new-construction-technologies-for-lowest-cost-fastest-and-most-sustainable-way-to-build-at-scale |
| 🥈 | **COBOD** | BOD3 modular gantry printer; Europe's largest 3D-printed building project announced; Revit→printer design-to-print sync in the field | UNVERIFIED month on the Fabbaloo piece | https://www.fabbaloo.com/news/cobod-unveils-europes-largest-3d-printed-building-project |
| 🥇 | **Autodesk Forma — Building Layout Explorer** | Generative interior-layout variants + solar/carbon analysis, pushes into Revit | Bundled free with every Revit/AEC Collection subscription (2026) | https://adsknews.autodesk.com/en/news/building-layout-explorer-in-autodesk-forma/ |
| 🥈 | **Finch3D** | AI floor-plan/layout copilot; Forma extension unifying massing → space planning → Revit BIM | Launch coverage, Parametric Architecture | https://parametric-architecture.com/finch-launches-forma-extension/ |
| 🥉 | **ARCHITEChTURES** | Generative residential building design (real-time BIM, cost, EU code rules) | Active in 2026 roundups; UNVERIFIED release date | https://architechtures.com/ |
| — | Market signal | 3DCP forecast as multibillion-dollar construction segment by 2030 | Apr-2026 | https://canada.constructconnect.com/dcn/news/technology/2026/04/3dcp-predicted-to-be-a-multibillion-dollar-player-in-construction-by-2030 |

## 3. AI interior design

| Rank | Tool | What it is | Evidence | Link |
|---|---|---|---|---|
| 🥇 | **SpatialLM** (manycore-research) | LLM for **structured indoor modeling**: point cloud/scene → walls, doors, furniture layout as structured output | NeurIPS 2025; 4,615★, pushed 2026-06-26 — most design-anything-relevant OSS here | https://github.com/manycore-research/SpatialLM |
| 🥈 | **Spacely AI** | Photoreal room renders with element-level masking | Blog actively publishing 2026-07 | https://www.spacely.ai/ |
| 🥈 | **Planner 5D AI** | CAD-lite 3D floor planner + AI layout/style module | Top-ranked in 2026 renovation-tool roundups | https://planner5d.com/use/ai-interior-design |
| — | **MeltFlex** | Won a Jul-2026 14-tool comparison — **its own blog; treat as promotional** | single-source | https://www.meltflexai.com/blog/best-ai-interior-design-tools-compared |
| — | **Interior AI** (levelsio) | Pioneer photo-restyling tool | UNVERIFIED 2026 activity | https://interiorai.com/ |

## 4. Game design / simulation AI pipelines

| Rank | Tool | What it is | Evidence | Link |
|---|---|---|---|---|
| 🥇 | **Marble** (World Labs, Fei-Fei Li) | Multimodal world model: text/image/video/layout → editable 3D worlds; exports Gaussian splats, meshes, video | GA 2026-06-03; World API 2026-01-21; v1.1 2026-04-02 | https://www.worldlabs.ai/blog/marble-world-model |
| 🥈 | **Project Genie / Genie 3** (Google DeepMind) | 11B autoregressive world model, real-time navigable 720p/24fps worlds from text | Public demo to AI Ultra subscribers 2026-01-29; consensus: ideation layer, not engine replacement | https://blog.google/innovation-and-ai/models-and-research/google-deepmind/project-genie/ |
| 🥇 | **NVIDIA Cosmos 3 + Isaac Lab 3.0 + Omniverse DSX** | First fully-open "omnimodel" world foundation model (16B/64B); Isaac Lab 3.0 on Newton 1.0 physics | GTC 2026-03 | https://blogs.nvidia.com/blog/gtc-2026-virtual-worlds-physical-ai/ |
| 🥉 | **HunyuanWorld-1.0** (Tencent) | First open simulation-capable immersive world generator | Released 2025-07-26; 2,877★, pushed 2026-04-15 | https://github.com/Tencent-Hunyuan/HunyuanWorld-1.0 |
| — | **Unity Muse/Sentis** | Folded into general "Unity AI" (~Unity 6.2, mid-2025) | UNVERIFIED current state; fresh signal is with Genie/Marble/Omniverse | https://unity.com/ai |

## 5. Open-source infrastructure with momentum

| Rank | Repo | What it is | Evidence | Link |
|---|---|---|---|---|
| 🥇 | **blender-mcp** (ahujasid) | "Use Blender with any LLM" via MCP — natural execution backbone: LLM → Blender → printable geometry | 24,410★, pushed 2026-07-14 — most-starred, most-active repo in this sweep | https://github.com/ahujasid/blender-mcp |
| 🥈 | **microsoft/TRELLIS** (original) | CVPR'25 spotlight image-to-3D | 13.2k★, updated 2026-06; superseded by TRELLIS.2 | https://github.com/microsoft/TRELLIS |
| ⚠️ | **Gap: OSS floor-plan generation is stale** | Graph2Plan, fml-wright, CSP generators = 2020-2024 academic, no 2026 momentum | text/image → permit-grade blueprint OSS is **unoccupied territory** | https://github.com/HanHan55/Graph2plan |

## The takeaway

**Meshes are solved; blueprints are not.** TRELLIS.2/Meshy/Rodin emit
print-ready *meshes* on demand, but only Zoo.dev outputs constrained parametric
CAD, and no open project spans image → code-compliant architectural blueprint.
That is design-anything's open lane. The live open stack to build on:
TRELLIS.2 + blender-mcp + SpatialLM + Cosmos 3.
