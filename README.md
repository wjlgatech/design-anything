# design-anything

**Any design intent in (text, picture) → execution-ready 3D blueprint out — construction- and 3D-print-verified.**

Covering: game design · 3D simulation · residential & commercial architecture (3D printing + AI) · interior design (furniture, kitchen, bedroom, living room, balcony) · garden & landscape.

Sibling of [animate-anything](https://github.com/wjlgatech/animate-anything) and [FM-os](https://github.com/wjlgatech/FM-os) — same operating system, new domain.

## Why this repo is different

1. **"Ready" is a gate, not a vibe.** No output may claim print/construction-ready without passing machine checks ([`pipeline/ready_gate.py`](pipeline/ready_gate.py)). No evidence ⇒ Not ready.
2. **Three-window research.** Everything curated here is ranked by observed evidence in three time windows — [last 30 days](research/last30days/DIGEST.md) (engagement), [last 30 years](research/last30years/DIGEST.md) (survival), [last 300 years](research/last300years/DIGEST.md) (civilizational endurance) — never by hype.
3. **Spec-as-data.** Curated knowledge lives in [`data/*.yml`](data/); the tables below are compiled artifacts with a CI drift gate. Humans edit YAML, never generated tables.
4. **Emit the composition, not the render.** Blueprints are deterministic parametric *source* (reviewable, diffable, re-generatable), never opaque meshes.

## The pipeline

```
text | image  →  brief (schema)  →  parametric model (source)  →  3D blueprint
                                                                      │
                                          READY-GATE (machine-checkable, per target)
                                          ├─ 3D-print:     watertight · outward normals · bed-fit · min-feature
                                          ├─ construction: IFC validity · structural sanity · code checklist   (roadmap)
                                          └─ game/sim:     glTF/USD validity · poly budget · true scale        (roadmap)
```

**Try the vertical slice** (stdlib-only, no dependencies):

```bash
python3 examples/planter/generate.py planter.stl      # text brief → parametric solid → STL
python3 pipeline/ready_gate.py planter.stl --min-feature 3.0   # READY or NOT READY, with evidence
make check                                            # the whole finish line CI runs
```

## Design principles

The distilled, survival-tested rules — each traceable to its research window — live in [`principles/DESIGN_PRINCIPLES.md`](principles/DESIGN_PRINCIPLES.md). Best practices for building with AI in this domain: [`best-practices/BEST_PRACTICES.md`](best-practices/BEST_PRACTICES.md). The 10X goal contract that governs the roadmap: [`GOAL.md`](GOAL.md).

## AI tooling — skills, bundles, workflows

Skills are packaged agent capabilities (one folder, one `SKILL.md`, eval-with-teeth). Bundles compose them; workflows orchestrate them dynamically. See [`skills/`](skills/), [`bundles/`](bundles/), [`workflows/`](workflows/).

<!-- BEGIN:skills -->

| Skill | Status | What it does |
|---|---|---|
| [brief-to-blueprint](https://github.com/wjlgatech/design-anything/tree/main/skills/brief-to-blueprint) | dogfooded | Compile a text/image design brief into a parametric blueprint plan with explicit constraints and a target ready-gate. |
| [print-ready-check](https://github.com/wjlgatech/design-anything/tree/main/skills/print-ready-check) | dogfooded | Run the ready gate on an STL and report READY/NOT-READY with per-gate evidence. |
| [blueprint-validate](https://github.com/wjlgatech/design-anything/tree/main/skills/blueprint-validate) | dogfooded | Validate a blueprint against the enduring-principles checklist (anthropometrics, modular grid, daylight, layers). |
| [pattern-library](https://github.com/wjlgatech/design-anything/tree/main/skills/pattern-library) | dogfooded | Retrieve applicable Alexander-style patterns (context/problem/solution) for a brief before generating form. |
| [scene-to-layout](https://github.com/wjlgatech/design-anything/tree/main/skills/scene-to-layout) | dogfooded | Turn a room photo/scan into a structured layout (walls, openings, furniture) using SpatialLM-class tools. |
| [design-research](https://github.com/wjlgatech/design-anything/tree/main/skills/design-research) | dogfooded | Run the three-window research method (30 days/30 years/300 years) on any design question, with grounding rules. |
<!-- END:skills -->

## The landscape — curated tools

Ranked by observed evidence (recency, engagement, survival). Full method + dates in [`research/`](research/).

<!-- BEGIN:tools -->

### text/image-to-3D

| Tier | Tool | What it is |
|---|---|---|
| 🥇 | [Microsoft TRELLIS.2](https://github.com/microsoft/TRELLIS.2) | Open (MIT) 4B image-to-3D flow-matching model; any topology, full PBR, GLB/PLY/OBJ export. |
| 🥇 | [Zoo.dev Text-to-CAD (Zookeeper)](https://zoo.dev/research/zookeeper) | Conversational agent emitting true parametric CAD (STEP/DXF, dimensioned) — blueprints, not meshes; open-source, self-hostable. |
| 🥈 | [Meshy-6](https://www.meshy.ai/blog/meshy-6-launch) | Market-leader SaaS mesh pipeline with PBR texturing, auto-rig, engine plugins, and multi-color 3D-print export. |
| 🥉 | [Hunyuan3D-2](https://github.com/Tencent-Hunyuan/Hunyuan3D-2) | Fully open asset generator (weights + training code, PBR); momentum shifting to TRELLIS.2. |

### agent-infrastructure

| Tier | Tool | What it is |
|---|---|---|
| 🥇 | [blender-mcp](https://github.com/ahujasid/blender-mcp) | Drive Blender from any LLM via MCP — the natural execution backbone from agent to printable geometry. |

### interior-design

| Tier | Tool | What it is |
|---|---|---|
| 🥇 | [SpatialLM](https://github.com/manycore-research/SpatialLM) | LLM for structured indoor modeling — point cloud/scene to walls, doors, and furniture layout as structured output. |
| 🥈 | [Spacely AI](https://www.spacely.ai/) | Photoreal room renders with element-level masking, used by boutique studios. |
| 🥉 | [Planner 5D AI](https://planner5d.com/use/ai-interior-design) | CAD-lite 3D floor planner with an AI layout/style module. |

### architecture

| Tier | Tool | What it is |
|---|---|---|
| 🥇 | [Autodesk Forma (Building Layout Explorer)](https://adsknews.autodesk.com/en/news/building-layout-explorer-in-autodesk-forma/) | Generative interior-layout variants with solar/carbon analysis, pushing straight into Revit. |
| 🥈 | [Finch3D](https://parametric-architecture.com/finch-launches-forma-extension/) | AI floor-plan copilot; Forma extension unifying massing, space planning, and Revit BIM. |

### construction-3D-printing

| Tier | Tool | What it is |
|---|---|---|
| 🥈 | [ICON (Titan + Vitruvius)](https://www.iconbuild.com/newsroom/icon-unveils-new-construction-technologies-for-lowest-cost-fastest-and-most-sustainable-way-to-build-at-scale) | ~250 printed structures; multi-story robotic printing plus an AI architect aiming at permit-ready designs. |
| 🥇 | [COBOD](https://cobod.com/) | Best-selling construction printers in 35+ countries — the "arm the builder" survival pattern. |
| 🥉 | [WASP](https://www.3dwasp.com/) | Earth-material construction printing (TECLA habitat) — the sustainable branch that persisted. |

### game-and-simulation

| Tier | Tool | What it is |
|---|---|---|
| 🥇 | [Marble (World Labs)](https://www.worldlabs.ai/blog/marble-world-model) | Multimodal world model — text/image/video/layout to editable 3D worlds exporting splats, meshes, or video. |
| 🥇 | [NVIDIA Cosmos 3 + Isaac Lab 3.0](https://blogs.nvidia.com/blog/gtc-2026-virtual-worlds-physical-ai/) | First fully open "omnimodel" world foundation model plus robot-sim stack on the Newton physics engine. |
| 🥈 | [Project Genie (Genie 3)](https://blog.google/innovation-and-ai/models-and-research/google-deepmind/project-genie/) | Real-time navigable worlds from text — an ideation layer, not an engine replacement. |

### survivor-foundations

| Tier | Tool | What it is |
|---|---|---|
| 🥇 | [Blender](https://www.blender.org/) | The free 3D DCC that survived bankruptcy and won an Oscar — 30-year survivor, default research render tool. |
| 🥇 | [Rhino + Grasshopper](https://www.rhino3d.com/) | The computational-design environment of architecture; never acquired, outlived every challenger. |
| 🥈 | [OpenSCAD](https://openscad.org/) | Code-CAD for printable parametric parts — the natural target for LLM text-to-CAD since code is an LLM's native 3D output. |
| 🥈 | [FreeCAD](https://www.freecad.org/) | The open BRep/parametric CAD; reached 1.0 after 22 years. |
| 🥈 | [COLMAP](https://colmap.github.io/) | Default structure-from-motion pipeline every NeRF/3DGS workflow assumes. |
<!-- END:tools -->

## Foundational work — papers & standards

<!-- BEGIN:papers -->

| Tier | Work | Why it matters |
|---|---|---|
| 🏛 | [IFC / ISO 16739](https://www.buildingsmart.org/standards/ifc/) | The open BIM interchange standard (born 1996) — legally mandated for public projects in several countries; the survival-grade architecture output target. |
| 🏛 | [OpenUSD Core Specification](https://aousd.org/news/core-spec-announcement/) | Pixar's scene-graph format, now an industry consortium spec heading to ISO — the presumptive digital-twin standard. |
| 🏛 | [glTF (ISO/IEC 12113)](https://www.khronos.org/gltf/) | The JPEG of 3D — default web/AR delivery format. |
| 🏛 | [3MF](https://3mf.io/) | STL's slow-motion successor for 3D printing, default in Bambu Studio/PrusaSlicer/Cura. |
| 🏛 | [Topology optimization (SIMP; Bendsoe 1988, Sigmund 2001)](https://www.topopt.mek.dtu.dk/) | The math inside every generative-design tool; survived the hype cycle — how blueprints get structurally validated. |
| 🏛 | [Screened Poisson Surface Reconstruction (Kazhdan 2013)](https://www.cs.jhu.edu/~misha/MyPapers/ToG13.pdf) | Still the default mesh-from-points algorithm in MeshLab/CloudCompare/Open3D. |
| 🏛 | [WaveFunctionCollapse (Gumin 2016)](https://github.com/mxgmn/WaveFunctionCollapse) | Constraint-based procedural generation shipping in Townscaper, Bad North, Caves of Qud — the PCG open-source success story. |
| 🏛 | [libigl / discrete differential geometry](https://libigl.github.io/) | The standard mesh-processing toolkit (SGP Software Award); any repair/remesh step sits on it. |
| 🏛 | [A Pattern Language (Alexander 1977)](https://en.wikipedia.org/wiki/A_Pattern_Language) | Composable context/problem/solution patterns — never out of print in 49 years; pre-specifies the architecture of a blueprint generator. |
| 🏛 | [Architects' Data (Neufert, 1936-)](https://en.wikipedia.org/wiki/Ernst_Neufert) | ~43 editions of anthropometric clearance tables — the generator's hard-constraint database. |
| 🌱 | [NeRF (Mildenhall et al. 2020)](https://www.matthewtancik.com/nerf) | Revolutionized 3D representation; already partially displaced by 3DGS — methods churn, representations persist. |
| 🌱 | [3D Gaussian Splatting (Kerbl et al. 2023)](https://repo-sam.inria.fr/fungraph/3d-gaussian-splatting/) | The production real-time capture representation (Polycam, Luma, Scaniverse). |
| 🌱 | [DreamFusion / Score Distillation Sampling (Poole et al. 2022)](https://dreamfusion3d.github.io/) | The mechanism behind most text-to-3D; now challenged by native 3D generators — may be the first of its batch to die. |
| 🌱 | [Instant-NGP (Mueller et al. 2022)](https://nvlabs.github.io/instant-ngp/) | SIGGRAPH 2022 Best Paper; the hash encoding baked into most neural-field trainers. |
| 🌱 | [Denoising Diffusion Probabilistic Models (Ho et al. 2020)](https://arxiv.org/abs/2006.11239) | The text-to-image half of the pipeline; Stable Diffusion and successors descend from it. |
<!-- END:papers -->

## Community — influential figures & labs

Inclusion requires survival evidence, not fame. See the [anti-portfolio](research/last30years/DIGEST.md#the-anti-portfolio-louder-at-birth-than-most-survivors-dead-or-husk-now) for who was louder and died.

<!-- BEGIN:community -->

| Who | Kind | Domain | Why they matter |
|---|---|---|---|
| [Gramazio Kohler Research (ETH Zurich)](https://gramaziokohler.arch.ethz.ch/) | lab | architecture | Invented "digital fabrication in architecture" as a discipline (2005); alumni seeded labs worldwide. |
| [Block Research Group (ETH Zurich)](https://block.arch.ethz.ch/) | lab | architecture | Philippe Block — compression-only structures, 3D-printed floors, and the open-source COMPAS framework. |
| [Ole Sigmund (DTU TopOpt)](https://www.topopt.mek.dtu.dk/) | person | structural-optimization | Topology optimization's living anchor; the group's free codes are the field's curriculum. |
| [NVIDIA Research](https://research.nvidia.com/) | lab | simulation | Instant-NGP, Kaolin, Omniverse/OpenUSD, Warp — the graphics/simulation engine room. |
| [IAAC Barcelona](https://iaac.net/) | lab | architecture | Academic pipeline for computational and 3D-printed architecture (Open Thesis Fabrication, 3D-printed bridge). |
| [Bartlett UCL (B-Pro)](https://www.ucl.ac.uk/bartlett/) | lab | architecture | One of the three main academic talent pipelines for computational design. |
| [TU Delft](https://www.tudelft.nl/en/architecture-and-the-built-environment) | lab | architecture | Built-environment research at scale — the third leg of the computational-architecture academy. |
| [Behrokh Khoshnevis](https://contourcrafting.com/) | person | construction-3D-printing | Contour Crafting — every gantry-extrusion construction printer descends from his patents. |
| [Fei-Fei Li (World Labs)](https://www.worldlabs.ai/) | person | simulation | Spatial-intelligence world models (Marble) — the strongest current text-to-world lineage. |
| [Maxim Gumin](https://github.com/mxgmn) | person | game-design | WaveFunctionCollapse — one person's algorithm shipping in a generation of games. |
| [Shigeru Miyamoto](https://en.wikipedia.org/wiki/Shigeru_Miyamoto) | person | game-design | Still shipping after 45 years — the deep-time control for game design craft. |
| [Will Wright](https://en.wikipedia.org/wiki/Will_Wright_(game_designer)) | person | game-design | SimCity/The Sims — his systems survived better than his career; an honest split. |
| [Pat Hanrahan & Ed Catmull](https://amturing.acm.org/) | person | graphics | 2019 Turing Award for fundamental contributions to 3D computer graphics — the certified foundation of this whole pipeline. |
| [Christopher Alexander (1936-2022)](https://www.patternlanguage.com/) | person | design-theory | A Pattern Language — the design book that already survived one substrate change (buildings to software). |
| [Jan Gehl](https://gehlpeople.com/) | person | urbanism | Human-scale metrics that transformed Copenhagen and were exported worldwide. |
| [Jane Jacobs (1916-2006)](https://en.wikipedia.org/wiki/Jane_Jacobs) | person | urbanism | Overturned the urban-renewal paradigm and stayed overturned; her four conditions live in 2020s zoning reform. |
| [Neri Oxman (MIT Media Lab lineage / OXMAN)](https://oxman.com/) | person | fabrication | Material ecology — biology-informed digital fabrication; the Mediated Matter lineage. |
| [COBOD](https://cobod.com/) | company | construction-3D-printing | The construction-printing company that survived by arming builders instead of being one. |
| [ICON](https://www.iconbuild.com/) | company | construction-3D-printing | ~250 printed structures and an AI-architect roadmap; restructured 2025 and kept building. |
| [buildingSMART International](https://www.buildingsmart.org/) | lab | standards | Stewards of IFC — the 30-year-old open standard everything interoperates through. |
| [Alliance for OpenUSD (AOUSD)](https://aousd.org/) | lab | standards | Pixar, Apple, Adobe, Autodesk, NVIDIA, Epic aligning the 3D scene-graph standard. |
| [Keenan Crane (CMU)](https://www.cs.cmu.edu/~kmcrane/) | person | graphics | Discrete differential geometry — the curriculum every mesh-processing engineer learns from. |
<!-- END:community -->

## Domain guides

| Domain | Guide |
|---|---|
| Game design | [domains/game-design](domains/game-design/README.md) |
| 3D simulation | [domains/simulation](domains/simulation/README.md) |
| Residential architecture (3DCP + AI) | [domains/architecture-residential](domains/architecture-residential/README.md) |
| Commercial architecture (3DCP + AI) | [domains/architecture-commercial](domains/architecture-commercial/README.md) |
| Interior design | [domains/interior-design](domains/interior-design/README.md) |
| Garden & landscape | [domains/landscape](domains/landscape/README.md) |

## Contributing

Two-line PR: edit a `data/*.yml` entry, run `make check`, open a PR. Every entry needs a working URL and a one-sentence non-hypey blurb. Skills need a Verification section that actually asserts. See [CONTRIBUTING.md](CONTRIBUTING.md).

## Honest edges

- The ready gate v0.1 covers the 3D-print target only; construction (IFC/code) and game (glTF/USD) gates are roadmap (see GOAL.md M-next).
- A passing gate means *printable*, not *good* — principles cover taste; the gate covers physics.
- A code-compliance checklist is not a structural engineer's stamp, and outputs must say so.

## License

MIT for code (`scripts/`, `pipeline/`, `examples/`, `tests/`) · CC BY 4.0 for content (docs, data, research). See [LICENSE](LICENSE).
