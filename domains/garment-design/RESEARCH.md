# Garment/cloth design + AI — three-window digest (researched 2026-07-18)

GitHub stats pulled live from api.github.com on the research date. Unverifiable
claims are marked UNVERIFIED.

## Window 1 — last 30 days / current landscape

| Rank | Entry | What it is + evidence | Link |
|---|---|---|---|
| 🥇 | **Seamly2D** | Open-source parametric pattern CAD — most active open pattern tool by far (913★, pushed 2026-07-18, the research date itself) | https://github.com/FashionFreedom/Seamly2D |
| 🥇 | **GarmentCode** (Korosteleva, ETH) | Patterns as programs + GarmentCodeData — the substrate the AI wave targets (386★) | https://github.com/maria-korosteleva/GarmentCode |
| 🥇 | **Text-to-pattern wave** | Field pivoted from meshes to **manufacturable patterns**: GarmentDiffusion (IJCAI 2025, cm-precise, 100× faster than SewingGPT), ChatGarment (CVPR 2025, 166★), Design2GarmentCode, GarmentImage, DressWild (arXiv 2026-02) | https://www.ijcai.org/proceedings/2025/163 |
| 🥈 | **Style3D / GarmageNet** | Most AI-aggressive fashion suite; a commercial CAD vendor open-sourcing generative research (65★, pushed 2026-01-16) is the signal | https://github.com/Style3D/garmagenet-impl |
| 🥈 | **Marvelous Designer 2026.0** (CLO) | Flagship 3D garment tool; Apr-2026 release bets on interaction (3D Pencil, lacing), notably **no headline AI** | https://www.cgchannel.com/2026/04/clo-virtual-fashion-releases-marvelous-designer-2026-0/ |
| 🥈 | **unspun / Vega** | 3D-weaves shaped garment components directly from yarn (~10-min pants), skipping cut-and-sew; $32M Series B, Walmart pilot | https://www.textileworld.com/textile-world/knitting-apparel/2026/05/unspun-focused-on-creating-a-new-category-of-apparel-production/ |
| 🥈 | **DressX Agent** | The digital-fashion survivor: pivoted to AI try-on utility; 200+ brands (Forbes, 2026-04) | https://www.forbes.com/sites/moinroberts-islam/2026/04/14/google-dressx-and-the-new-fashion-ai-virtual-try-on-stack/ |
| 🥉 | **Browzwear** | Technical-fit incumbent; hybrid physics-AI positioning | https://browzwear.com/ |
| 🥉 | **NVIDIA Warp** | Where new differentiable cloth-sim work lands (6,873★, pushed 2026-07-18) | https://github.com/NVIDIA/warp |
| — | Freesewing (patterns-as-code, cooling: pushed 2025-04) · Tukatech (alive, niche) · Seddi (UNVERIFIED momentum) | | |

## Window 2 — last 30 years survival test

| Tier | Entry | Survival evidence | Link |
|---|---|---|---|
| 🏛 | **Baraff & Witkin 1998** | Implicit integration made cloth sim stable; canonical citation 28 years on; ancestor of film-pipeline solvers | https://dl.acm.org/doi/10.1145/280814.280821 |
| 🏛 | **PBD (2007) → XPBD (2016)** | What actually ships real-time (Unreal Chaos Cloth, PhysX); traded accuracy for stability and won the games market | https://www.emergentmind.com/topics/extended-position-based-dynamics-xpbd |
| 🏛 | **SMPL (2015)** | Still THE body-model standard in 2026 (SMPL-H/X extensions, Meshcapade); challengers fix anatomy but haven't displaced it | https://meshcapade.com/smpl/ |
| 🏛 | **DXF-AAMA / ASTM D6673** | The pattern interchange format — **standard formally withdrawn 2019, yet every CAD still speaks it**. De facto formats outlive their standards bodies. An AI generator that can't emit it is not production-real. | https://store.astm.org/d6673-10.html |
| 🌳 | **Gerber → Lectra** | The 2D industrial pattern-CAD duopoly consolidated into one survivor (AccuMark still sold under Lectra) | https://www.lectra.com/en/fashion/products/gerber-accumark-fashion |
| 🌳 | **Optitex** | One of the few 90s pattern CADs that neither died nor got absorbed | https://optitex.com/ |
| 🌳 | **NeuralTailor lineage (2021-22)** | First credible neural pattern reconstruction; seeded SewFormer, DressCode, and the Window-1 wave | https://github.com/maria-korosteleva/Garment-Pattern-Estimation |
| 🌳 | **ARCSim (2012)** | Survives as absorbed ideas (adaptivity), not shipping software; UNVERIFIED last maintenance | http://graphics.berkeley.edu/resources/ARCSim/ |
| ☠️ | **Anti-portfolio: RTFKT** | NFT wearables, bought by Nike at the 2021 peak; wound down 2024; "Crypto Kicks" $8,000 → $16 (−99.8%), class action. Garments-as-speculation died; garments-as-utility (DressX) survived. | https://www.thestreet.com/crypto/markets/nike-quietly-says-goodbye-to-nft-subsidiary |
| ⚪ | The Fabricant | Pioneer digital-only fashion house; UNVERIFIED current health | https://www.thefabricant.com/ |

## Window 3 — last 300 years endurance (each with its AI constraint)

1. **Proportional drafting systems** (19th-c. tailors) — patterns as arithmetic functions of body measures; literally what GarmentCode reinvented. *Constraint: emit drafting rules, not fixed outlines.*
2. **Butterick graded paper patterns (1863)** — created the pattern-as-product industry, still extant. *Constraint: patterns must be gradable, reproducible artifacts.* (UNVERIFIED current corporate ownership.)
3. **Vionnet's bias cut (1920s)** — exploits fabric anisotropy for drape; nearly extinct mid-century, permanently revived. *Constraint: reason about grainline and directional mechanics.*
4. **Issey Miyake A-POC (1998 → A-POC ABLE, present)** — garment logic programmed into the textile; survived its founder. *Constraint: the true output can be machine instructions (knit/weave programs); cut-and-sew is only one backend.* https://us.isseymiyake.com/pages/apocable
5. **Zero-waste cutting** (kimono/sari → Rissanen & McQuillan) — pre-industrial garments were zero-waste by economics; industry wastes 10-15%. *Constraint: marker efficiency belongs in the loss function.* https://www.hollymcquillan.com/publications
6. **Standardized sizing** (military anthropometry → ASTM D5585-21, with 3D avatars per size) — still governs US grading. *Constraint: grade coherently across the size run or it's a demo.* https://store.astm.org/d5585-21.html
7. **The sewing machine (1850s)** — froze construction around seam types unchanged 170 years; sewing is the automation holdout (unspun's bet routes around it). *Constraint: every seam maps to a feasible machine operation and assembly order.*
8. **Shaker/utility clothing ethos** — economy of cut, durability, repairability; resurfaces every era. *Constraint: bias toward fewer pieces and repairable construction.*

**Whig-history guard:** zero-waste wasn't wisdom rediscovered — it was the default that cheap industrial fabric killed. The bias cut nearly went extinct. DXF-AAMA survives despite formal withdrawal. **Survival here tracks input economics (fabric, labor, installed machine base), not technical superiority** — so optimize against the cost structure of the era, and treat today's constraints (cut-and-sew, DXF, SMPL) as contingent, not eternal.

## Synthesis

(1) Sewing patterns are the AI↔manufacturing interchange representation — GarmentCode research-native, DXF-AAMA factory-native. (2) Incumbents add AI cautiously, Style3D open-sources it, unspun bypasses cut-and-sew — three distinct bets. (3) Everything that survived is **parametric, gradable, grain-aware, manufacturable**; everything that died was none of those.
