# The DIKW compression ↔ expression model

The mental model that organizes this repo: **design is a round trip between
wisdom and data.** Learning compresses the world; creating expresses it back.

```
        COMPRESSION  (learning: many → few)                EXPRESSION  (creating: few → many)
        ────────────────────────────────────               ─────────────────────────────────
WISDOM      principles P1-P13 · the Lindy rule ·     ⇒     which principles & patterns apply
            GOAL.md's definition of "ready"                to THIS brief
   ▲                                                                  │
KNOWLEDGE   curated data/*.yml · constraint tables   ⇒     the brief + its tables
            (clearances, DfAM, garment fit) ·              (the generator's working set)
            pattern library                                           │
   ▲                                                                  ▼
INFORMATION dated, sourced research digests          ⇒     parametric source — the composition
            (30d / 30y / 300y)                             (reviewable, diffable, re-generatable)
   ▲                                                                  │
DATA        raw signals: papers, stars, releases,    ⇒     geometry: STL · IFC · layout JSON ·
            buildings & tools that survived                DXF pattern markers
        ────────────────────────────────────               ─────────────────────────────────
                     research/  (the input side)                pipeline/ + examples/  (the output side)
```

## What the model buys us

1. **Every artifact has one home.** Raw findings → `research/` digests
   (data→information). Digests → `data/*.yml` (information→knowledge). YAML →
   `principles/` (knowledge→wisdom). The README and `llms.txt` are *compiled
   re-expressions* of knowledge — which is why hand-editing them is a bug the
   drift gate catches.
2. **Gates verify expression at both ends.** Ready-gates check the DATA end
   (is the geometry buildable?); `blueprint-validate` checks the WISDOM end
   (does the design honor the principles?). A design can pass one and fail the
   other — that's the Vitruvian triple gate (P1) restated.
3. **The flywheel is the loop closing.** A gate-dispute ("READY but failed in
   the slicer") is new *data*; it recompresses into a better table or a new
   gate — each turn of the loop sharpens both directions.
4. **Simplify by compressing, never by deleting.** When the repo grows, the
   move is upward compression (20 tools → 1 tier rule; 30 findings → 1
   principle), not truncation. Silent deletion loses the anti-portfolio —
   and the failures teach more than the winners.
5. **Diverge/converge is this same rhythm.** Design thinking's double diamond
   (see [DESIGN_THINKING.md](DESIGN_THINKING.md)) is expression (generate
   options) then compression (select against constraints) — run twice. The
   rhythm is the survivor; the workshop theater is not.

## The domain-inclusion rule (what belongs in this repo)

A discipline earns a `domains/` guide when its **expression endpoint is a
spatial/physical artifact whose "ready" can be machine-gated** — geometry,
clearances, tolerances, fit tables. Design-centric disciplines with non-spatial
endpoints (org design, service design, mechanism design) are *adjacent*: the
operating system (three-window compression, tables-as-data, gates) transfers to
them; the geometry pipeline does not. The full map: [docs/DESIGN_DISCIPLINES.md](../docs/DESIGN_DISCIPLINES.md).
