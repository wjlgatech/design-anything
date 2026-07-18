# /last30years — survival test (1996–2026)

**Legend:** 🏛 survived (3/3 probes: still-used + built-upon + hype-survived) ·
🌳 aging-well (2/3) · 🌱 too-young-to-tier (<10 yrs; momentum noted, survival
unproven) · ⚪ unproven this run.

## Cluster 1 — Interchange formats & standards (the strongest survivors)

| Tier | Standard | Born | Survival evidence | Link |
|---|---|---|---|---|
| 🏛 | **IFC / buildingSMART** | 1996 | ISO 16739; legally mandated for public BIM (UK 2016, Nordics, Singapore); declared "broken/dying" since the 2000s yet outlived every proprietary rival | https://www.buildingsmart.org/standards/ifc/ |
| 🏛 | **glTF** | 2015 | "the JPEG of 3D"; ISO/IEC 12113:2022; default web/AR delivery; beat its own Khronos predecessor Collada | https://www.khronos.org/gltf/ |
| 🏛 | **OpenUSD** (Pixar) | 2016 | AOUSD Core Spec 1.0 (Dec 2025) heading to ISO; 50 member companies (Apple, Adobe, Autodesk, NVIDIA, Epic) | https://aousd.org/news/core-spec-announcement/ |
| 🌳 | **STL → 3MF** | 1987 / 2015 | STL still what most printers eat after ~39 years; 3MF now default in Bambu Studio, PrusaSlicer, Cura. Emit both. | https://3mf.io/ |

## Cluster 2 — Load-bearing tools

| Tier | Tool | Born | Survival evidence | Link |
|---|---|---|---|---|
| 🏛 | **Blender** | 1994/2002 | *Flow* won the 2025 Animation Oscar; survived literal bankruptcy (2002 €100k crowdfunded buyout) and the pre-2.80 UI era; orderly founder succession Jan 2026 | https://www.blender.org/news/blenders-impact-in-film/ |
| 🏛 | **Unreal Engine** | 1998 | UE5 dominant AAA + virtual production + archviz; Datasmith is the CAD/BIM→realtime bridge; survived the 2000s engine-licensing crash that killed RenderWare/Gamebryo | https://www.unrealengine.com/ |
| 🏛 | **Unity** | 2005 | Most-shipped engine by title count; survived the Sept-2023 runtime-fee debacle (CEO out, policy reversed) | https://unity.com/ |
| 🏛 | **Rhino + Grasshopper** | 1998/2007 | *The* computational-design environment of architecture; never acquired; outlived GenerativeComponents and Dynamo's challenge | https://www.rhino3d.com/ |
| 🏛 | **Revit / BIM** | 2000 | Dominant BIM authoring; survived the 2020 UK-practices "stagnating" open letter | https://www.autodesk.com/products/revit/ |
| 🏛 | **CGAL** | 1996 | The computational-geometry library (exact predicates, booleans, meshing); OpenSCAD's kernel — correctness compounds | https://www.cgal.org/ |
| 🌳 | **OpenSCAD** | 2010 | Still the code-CAD standard for printable parametric parts; the natural target for LLM text→CAD (code is an LLM's native 3D output) | https://openscad.org/ |
| 🌳 | **FreeCAD** | 2002 | Hit 1.0 in Nov 2024 after 22 years (fixed topological naming); the open BRep/parametric CAD | https://www.freecad.org/ |
| 🌳 | **COLMAP** | 2016 | Default SfM/MVS pipeline; every NeRF/3DGS paper's preprocessing assumes `colmap` output | https://colmap.github.io/ |

## Cluster 3 — Foundational academic work

| Tier | Work | Survival evidence | Link |
|---|---|---|---|
| 🏛 | **WaveFunctionCollapse** (Gumin 2016, capstone of a 30-yr PCG lineage via Merrell 2007) | Ships in Bad North, Townscaper, Caves of Qud, Matrix Awakens; ~24k★; "the open-source success story of PCG" | https://github.com/mxgmn/WaveFunctionCollapse |
| 🏛 | **Screened Poisson Surface Reconstruction** (Kazhdan 2006/2013) | Still the default mesh-from-points in MeshLab, CloudCompare, Open3D; survived the "learned reconstruction will replace it" wave | https://www.cs.jhu.edu/~misha/MyPapers/ToG13.pdf |
| 🏛 | **Topology optimization (SIMP)** (Bendsøe 1988 → Sigmund's 99-line code 2001) | Inside Fusion generative design, nTop, OptiStruct; survived the 2015-18 "generative design" hype — the marketing died, the math stayed. This is how blueprints get structurally validated. | https://www.topopt.mek.dtu.dk/ |
| 🌱 | **Instant-NGP** (Müller 2022) | SIGGRAPH 2022 Best Paper; baked into Nerfstudio and most 3DGS trainers | https://nvlabs.github.io/instant-ngp/ |
| 🌳 | **libigl / DDG stack** (cotan-Laplacian lineage; libigl 2013) | SGP Software Award; ARAP (Sorkine 2007) in Blender sculpt; any repair/remesh step sits on this | https://libigl.github.io/ |

## Cluster 4 — 🌱 Young, massive momentum (cannot outrank the above yet)

- **Diffusion models** (DDPM 2020; Latent Diffusion 2022) — five-figure citation scale (magnitude estimated, not verified); the text→image half of the pipeline. https://arxiv.org/abs/2006.11239
- **NeRF** (Mildenhall 2020) — revolutionized 3D representation, already partially displaced by 3DGS for real-time — a live lesson: **methods churn; representations, datasets, and COLMAP persist**. https://www.matthewtancik.com/nerf
- **3D Gaussian Splatting** (Kerbl 2023) — production representation at Polycam, Luma, Scaniverse; Unreal/Unity plugins. https://repo-sam.inria.fr/fungraph/3d-gaussian-splatting/
- **DreamFusion / SDS** (Poole 2022) — the mechanism behind most text→3D, now challenged by native 3D generators — may be the first of this batch to die; watch it. https://dreamfusion3d.github.io/

## Cluster 5 — People & labs still shaping the field

| Tier | Who | Why load-bearing | Link |
|---|---|---|---|
| 🏛 | **Gramazio Kohler Research, ETH Zurich** (2005) | Invented "digital fabrication in architecture" as a discipline; alumni seeded labs worldwide | https://gramaziokohler.arch.ethz.ch/ |
| 🏛 | **Block Research Group, ETH** (2009) | Philippe Block; compression-only structures, 3D-printed floors; open-source COMPAS framework is a community standard | https://block.arch.ethz.ch/ |
| 🏛 | **Ole Sigmund, DTU** | Topology optimization's living anchor; TopOpt free codes are the field's curriculum | https://www.topopt.mek.dtu.dk/ |
| 🏛 | **NVIDIA Research** | instant-NGP, Kaolin, Omniverse/OpenUSD, Warp; SIGGRAPH 2025 Test-of-Time (Macklin's unified particle physics) | https://research.nvidia.com/ |
| 🌳 | **IAAC Barcelona + Bartlett UCL B-Pro + TU Delft** | The academic talent pipeline for computational/3DP architecture | https://iaac.net/ |
| 🏛/🌳 | **Miyamoto (still shipping) / Will Wright** | Wright's *systems* (SimCity→Cities: Skylines; The Sims) survived better than his career — an honest split | — |
| 🏛 | **Hanrahan & Catmull** | 2019 Turing Award "for fundamental contributions to 3D computer graphics" — the establishment certifying this whole pipeline | https://amturing.acm.org/ |

## Cluster 6 — 3D-printing construction: who survived

| Tier | Who | Evidence | Link |
|---|---|---|---|
| 🏛-track | **COBOD** (2017) | **Arms the builder** instead of being the builder: 85+ printers, 35+ countries, GE/CEMEX/Holcim partners, PERI-built serial housing in Germany | https://cobod.com/ |
| 🌳 | **ICON** (2017) | Genuine hype-survival in progress: cut ~25% staff Jan 2025, raised $56M a month later; 100-home Lennar community delivered; $57M NASA Project Olympus | https://techcrunch.com/2025/01/09/icon-a-builder-of-3d-printed-homes-last-valued-around-2-billion-cuts-about-25-of-staff/ |
| 🌳 | **Khoshnevis / Contour Crafting** (~1998) | Every gantry-extrusion construction printer descends from his patents; the idea survived better than the company | https://contourcrafting.com/ |
| 🌳 | **WASP** (2012) | TECLA earth-printed habitat; the sustainable/earth-material branch that persisted | https://www.3dwasp.com/ |

## The Anti-Portfolio (louder at birth than most survivors; dead or husk now)

- **Katerra** (2015, ~$2B raised) — Chapter 11 June 2021. Tried to *be* the builder end-to-end. **The single most instructive death for design-anything.** https://www.fastcompany.com/90643381/this-prefab-builder-raised-more-than-2-billion-why-did-it-crash
- **Veev** (~$600M) — shut down 2023-24; same vertical-integration trap.
- **WinSun** — "10 houses in 24 hours" (2014-16), went silent, re-emerged 2024 as Gaudi Tech — a comeback bet, not a survivor. https://3dprint.com/308092/winsun-is-back-as-gaudi-tech-and-its-3d-printing-houses-in-the-u-s/
- **Google Project Tango** (2014) — killed 2018; quiet little glTF became the standard instead.
- **Autodesk 123D Catch** (2011) — discontinued 2017; photogrammetry survived via COLMAP/RealityCapture.

## ⚪ Unproven this run

- Cazza Construction (appears vanished; not directly verified), Mighty Buildings (restructuring verified; 2026 status unconfirmed).
- Space syntax (Hillier 1984), shape grammars (Stiny 1971), marching cubes (1987) — born pre-window; belong to /last300years-class analysis, would likely rank 🏛.
- Exact citation counts for NeRF/DDPM/3DGS — API rate-limited; magnitudes are estimates.

## The Lindy read

Bet the repo's **interfaces** on the 25-30-year survivors — IFC, glTF/USD,
STL/3MF as targets; Blender/Rhino/Unreal as environments; CGAL/libigl/Poisson/
SIMP as the geometry-and-validation core — and treat the sub-10-year AI layer
(diffusion, 3DGS, SDS) as a **hot-swappable front end**, because that layer has
already churned once (NeRF→3DGS in 3 years) while COLMAP, the formats, and the
mesh stack sat still underneath. In construction: copy COBOD (arm the builder),
avoid Katerra (don't become the builder).
