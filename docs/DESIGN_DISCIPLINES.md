# The map of design-centric disciplines

Which fields are design-centric or design-dominated, and which belong in this
repo? The inclusion rule comes from the [DIKW model](../principles/DIKW_MODEL.md):
**in scope when the expression endpoint is a spatial/physical artifact whose
"ready" is machine-gateable.**

## Tier 1 — Covered (domains/ guide + gates)

| Discipline | Gate status |
|---|---|
| Game design | ✅ scene gate v0.1 |
| 3D simulation | ✅ scene gate v0.1 |
| Residential & commercial architecture (3DCP + AI) | ✅ construction gate v0.1 |
| Interior design | ✅ via construction gate tables |
| Garden & landscape | seeds in guide |
| **Garment & cloth design** | ✅ pattern gate + DXF-AAMA |
| **Eyewear** (first body-fit domain) | ✅ bodyfit gate v0.1 |

## Tier 2 — Gateable next (spatial endpoint, tables exist, strong 3D-print fit)

Ranked by evidence that the domain is *already* gate-driven at scale:

| Discipline | Why it's a strong candidate | The existing gate-culture proof |
|---|---|---|
| **Dental & hearing aids** | The most successful mass-3D-printing categories on Earth — hearing-aid shells went ~100% printed in under a decade; clear aligners print millions/day | FDA device classes; fit derived from scans |
| **Prosthetics & orthotics** | Body-fit tables (the Neufert-of-bodies) + print-native; e-NABLE's open-source hand lineage | ISO 8548/8549 |
| **Footwear** | Zellerfeld/adidas 4D show print-native shoes shipping; lasts are parametric body-fit objects | last grading tables, ASTM |
| **Industrial / product design** | The home discipline of DFM/DFA — Boothroyd-Dewhurst is literally a gate | GD&T (ASME Y14.5) |
| **Jewelry** | Print-to-cast is the dominant workflow already | ring sizing tables, castability rules |
| **Packaging** | Dielines are 2D blueprints exactly like garment patterns | ECMA/FEFCO standard designs |
| **Stage/set & exhibit design** | Architecture's fast-cycle sibling; same clearance/egress tables | venue codes |

## Tier 3 — Design-dominated, non-spatial endpoint (the OS transfers, the pipeline doesn't)

The three-window research method, tables-as-data, and gate discipline apply;
the geometry pipeline does not.

| Discipline | The transferable lesson it *gives us* |
|---|---|
| **Chip design (EDA)** | The strongest validation of this repo's thesis that exists: **DRC (design rule checking) and LVS are ready-gates** — no chip tapes out on vibes. The most mature design field is the most gate-driven. |
| **Aerospace/automotive/naval design** | Certification culture: gates all the way down (also Tier-2-spatial, but pro-tool-locked) |
| **Typography & font design** | 2D but deeply gateable (metrics, kerning tables, hinting) — a plausible Tier-2.5 |
| **Graphic/communication design** | Grid systems = modular coordination's 2D sibling |
| **UX/interaction design** | Nielsen heuristics = a rubric-as-data ClosedLoop; source of the "test with users" kernel |
| **Service design** | Blueprinting (Shostack 1984) — literally borrowed our word |
| **Mechanism design (economics)** | Design with adversarial verification built in — the Nobel-grade version of maker≠checker |
| **Drug & protein design** | AlphaFold-era: generate → *fold gate* → wet-lab verify; same generate-then-gate shape |
| **Synthetic biology** | BioBricks = interchangeable parts (P17) crossing substrates again |
| **Instructional / organization design** | Design thinking's main deployment ground; wisdom-tier only |

## The cross-cutting read

1. **Mature design fields converge on gates.** Chips (DRC), aerospace (cert),
   garments (grading rules), buildings (codes). "Ready is a gate, not a vibe"
   isn't this repo's invention — it's what every design field does when it
   grows up. AI design tools that skip gates are skipping maturity.
2. **Fit-to-the-human-body domains are the nearest expansion** (dental,
   prosthetic, footwear, eyewear, garment): they share one constraint database
   pattern — anthropometric tables + scan-to-parametric — and they're where
   3D printing already won at scale.
3. **Every Tier-3 field contributes a principle back** even when out of scope:
   DRC validates the gate thesis, mechanism design validates adversarial
   verification, service design named the blueprint. Compression flows in from
   everywhere; expression stays spatial.
