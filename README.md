# design-anything

**Any design intent in (text, picture) → execution-ready 3D blueprint out — construction- and 3D-print-verified.**

Covering: game design · 3D simulation · residential & commercial architecture (3D printing + AI) · interior design (furniture, kitchen, bedroom, living room, balcony) · garden & landscape · garment & cloth design. The full map of design-centric disciplines (and what qualifies one for this repo): [docs/DESIGN_DISCIPLINES.md](docs/DESIGN_DISCIPLINES.md).

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
                                          ├─ construction: topology · clearance tables · habitability · egress · module grid
                                          ├─ garment:      pieces+grain · fabric fit · seam · zero-waste efficiency · fit tables
                                          └─ game/sim:     glTF/USD validity · poly budget · true scale        (roadmap)
```

**Try the vertical slices:**

```bash
# print target (stdlib-only): text brief → parametric solid → STL → gate
python3 examples/planter/generate.py planter.stl
python3 pipeline/ready_gate.py planter.stl --min-feature 3.0

# construction target: text brief → parametric floor plan → layout JSON → gate
python3 examples/studio-flat/generate.py layout.json
python3 pipeline/construction_gate.py layout.json

# garment target: text brief → parametric pattern → marker JSON → gate
python3 examples/apron/generate.py marker.json
python3 pipeline/pattern_gate.py marker.json

make check   # the whole finish line CI runs
```

Agents: a flat, token-cheap index of everything curated here is compiled to [`llms.txt`](llms.txt).

## Design principles

The distilled, survival-tested rules — each traceable to its research window — live in [`principles/DESIGN_PRINCIPLES.md`](principles/DESIGN_PRINCIPLES.md). The organizing mental model — **DIKW compression ↔ expression** (research compresses the world into principles; the pipeline expresses principles into gated artifacts) — is [`principles/DIKW_MODEL.md`](principles/DIKW_MODEL.md). Design thinking, honestly tiered (keep the kernel, drop the theater): [`principles/DESIGN_THINKING.md`](principles/DESIGN_THINKING.md). Best practices: [`best-practices/BEST_PRACTICES.md`](best-practices/BEST_PRACTICES.md). The 10X goal contract that governs the roadmap: [`GOAL.md`](GOAL.md).

## AI tooling — skills, bundles, workflows

Skills are packaged agent capabilities (one folder, one `SKILL.md`, eval-with-teeth). Bundles compose them; workflows orchestrate them dynamically. See [`skills/`](skills/), [`bundles/`](bundles/), [`workflows/`](workflows/).

<!-- BEGIN:skills -->

| Skill | Status | What it does |
|---|---|---|
| [brief-to-blueprint](https://github.com/wjlgatech/design-anything/tree/main/skills/brief-to-blueprint) | dogfooded | Compile a text/image design brief into a parametric blueprint plan with explicit constraints and a target ready-gate. |
| [print-ready-check](https://github.com/wjlgatech/design-anything/tree/main/skills/print-ready-check) | dogfooded | Run the ready gate on an STL and report READY/NOT-READY with per-gate evidence. |
| [construction-ready-check](https://github.com/wjlgatech/design-anything/tree/main/skills/construction-ready-check) | dogfooded | Run the construction ready gate on a rooms+openings layout — clearances, habitability, daylight, egress, module grid. |
| [garment-ready-check](https://github.com/wjlgatech/design-anything/tree/main/skills/garment-ready-check) | dogfooded | Run the pattern gate on a garment marker — pieces, grain, fabric fit, seam allowance, zero-waste efficiency, fit tables. |
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

### garment-design

| Tier | Tool | What it is |
|---|---|---|
| 🥇 | [Seamly2D](https://github.com/FashionFreedom/Seamly2D) | Open-source parametric pattern-making CAD — the most active open pattern tool. |
| 🥇 | [GarmentCode (ETH)](https://github.com/maria-korosteleva/GarmentCode) | Sewing patterns as programs — the substrate the AI pattern-generation wave targets. |
| 🥇 | [Marvelous Designer / CLO](https://www.cgchannel.com/2026/04/clo-virtual-fashion-releases-marvelous-designer-2026-0/) | Flagship 3D garment tool for games/VFX/fashion; 2026.0 bets on interaction, notably not generation. |
| 🥈 | [Style3D + GarmageNet](https://github.com/Style3D/garmagenet-impl) | The most AI-aggressive fashion suite — a commercial CAD vendor open-sourcing its generative garment model. |
| 🥈 | [unspun Vega](https://www.textileworld.com/textile-world/knitting-apparel/2026/05/unspun-focused-on-creating-a-new-category-of-apparel-production/) | 3D-weaves shaped garment components directly from yarn, routing around cut-and-sew entirely. |
| 🥉 | [DressX](https://www.forbes.com/sites/moinroberts-islam/2026/04/14/google-dressx-and-the-new-fashion-ai-virtual-try-on-stack/) | The digital-fashion survivor — pivoted from NFT-era hype to AI try-on utility with 200+ brands. |
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
| 🏛 | [Large Steps in Cloth Simulation (Baraff & Witkin 1998)](https://dl.acm.org/doi/10.1145/280814.280821) | Implicit integration made cloth simulation stable — the canonical citation 28 years on. |
| 🏛 | [PBD → XPBD (Mueller 2007, Macklin 2016)](https://www.emergentmind.com/topics/extended-position-based-dynamics-xpbd) | What actually ships in real-time engines — traded accuracy for stability and won the games market. |
| 🏛 | [SMPL body model (Loper et al. 2015)](https://meshcapade.com/smpl/) | Still THE parametric human body standard in 2026; challengers fix anatomy but have not displaced it. |
| 🏛 | [DXF-AAMA / ASTM D6673 pattern exchange](https://store.astm.org/d6673-10.html) | Standard formally withdrawn in 2019 yet every pattern CAD still speaks it — de facto formats outlive their standards bodies. |
| 🌱 | [Text-to-sewing-pattern wave (GarmentDiffusion, ChatGarment, 2025-26)](https://www.ijcai.org/proceedings/2025/163) | The field pivoted from mesh generation to manufacturable pattern generation — cm-precise, vectorized, gradable. |
| 🏛 | [The Sciences of the Artificial (Simon 1969)](https://mitpress.mit.edu/9780262537537/the-sciences-of-the-artificial/) | The intellectual root defining design as a discipline — "everyone designs who devises courses of action aimed at changing existing situations into preferred ones." |
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
| [Maria Korosteleva (ETH Zurich)](https://github.com/maria-korosteleva/GarmentCode) | person | garment-design | NeuralTailor and GarmentCode — seeded the entire neural sewing-pattern generation wave. |
| [Holly McQuillan](https://www.hollymcquillan.com/publications) | person | garment-design | Codified zero-waste pattern cutting; still publishing on woven textile-form. |
| [Issey Miyake / A-POC ABLE](https://us.isseymiyake.com/pages/apocable) | lab | garment-design | Garment logic programmed into the textile itself — the process survived its founder. |
| [Madeleine Vionnet (1876-1975)](https://en.wikipedia.org/wiki/Madeleine_Vionnet) | person | garment-design | The bias cut — proof that grain direction is a design material; nearly extinct, permanently revived. |
| [Herbert Simon (1916-2001)](https://mitpress.mit.edu/9780262537537/the-sciences-of-the-artificial/) | person | design-theory | Defined design as a discipline in The Sciences of the Artificial — the wisdom-tier anchor of design thinking. |
| [Stanford d.school / IDEO lineage](https://dschool.stanford.edu/) | lab | design-theory | Popularized design thinking (Kelley, Brown); the kernel survives the workshop-theater critique wave. |
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
| Garment & cloth design | [domains/garment-design](domains/garment-design/README.md) |

## Contributing

Two-line PR: edit a `data/*.yml` entry, run `make check`, open a PR. Every entry needs a working URL and a one-sentence non-hypey blurb. Skills need a Verification section that actually asserts. See [CONTRIBUTING.md](CONTRIBUTING.md).

## Honest edges

- Gates shipped: 3D-print (`ready_gate.py`), construction v0.1 (`construction_gate.py` — layout graph + clearance tables, not structural spans or IFC yet), and garment v0.1 (`pattern_gate.py` — marker + fit tables, not drape or sewability; overlap check is bbox-level). The game/sim gate is roadmap (GOAL.md M7).
- A passing gate means *buildable/printable/cuttable*, not *good* — principles cover taste; the gate covers physics and tables.
- The construction gate is a design-sanity check, **not a permit and not a structural engineer's stamp**; the pattern gate is not a muslin — every report says so, and jurisdiction codes / real fittings override.

## License

MIT for code (`scripts/`, `pipeline/`, `examples/`, `tests/`) · CC BY 4.0 for content (docs, data, research). See [LICENSE](LICENSE).
