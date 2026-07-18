# Best practices — building design-AI systems (lessons from the template repos)

Inherited from [animate-anything](https://github.com/wjlgatech/animate-anything)
and [FM-os](https://github.com/wjlgatech/FM-os), adapted to 3D/blueprint work.

## Repo operating system

1. **Spec-as-data + drift gate.** Humans edit `data/*.yml`; README tables, site,
   and `llms.txt` are compiled. `make check` fails if committed output ≠
   generator output. Never hand-edit generated artifacts.
2. **`make check` is the finish line.** validate (schema) + pytest + drift gate +
   the ready gate on the golden example. Exit 0 = green; anything else fails CI.
3. **Golden examples that score 100%.** `examples/planter/` passes the full gate
   with zero dependencies — an executable spec of "what good looks like" and the
   CI regression anchor.
4. **Maker ≠ checker.** The generator (`examples/`) and the gate (`pipeline/`)
   are independent code paths, held against each other and against analytic
   ground truth by tests.
5. **Zero-dependency core.** The gate and golden example are stdlib-only: run in
   any CI, cost zero tokens, behave identically everywhere. Heavy deps
   (trimesh, ifcopenshell, Blender) belong in optional skills, not the core loop.

## Blueprint generation

6. **Emit the composition, not the render.** The blueprint is deterministic
   parametric source (Python/OpenSCAD/CadQuery/IFC), reviewable and diffable.
   Meshes and renders are compiled artifacts.
7. **Ready is per-target.** Print, construction, and game targets have different
   gates; declare the target in the brief and gate against it. A passing gate
   means *buildable*, not *good* — principles cover taste.
8. **Constraint tables are the database.** Anthropometrics, modular grids, DfAM
   rules, span tables load as data the generator must satisfy, not prose it may
   read.
9. **Probe actual model behavior, never reputation.** Before wiring any
   text-to-3D model, verify with one call: output format? watertight? licensed
   for your use? Model IDs and capabilities churn monthly.
10. **Verify at the user's altitude.** A blueprint "works" when it slices/imports
    in the tool a real user runs (PrusaSlicer, Revit, Unity) — not when the
    generator exits 0.

## Research & curation

11. **Three-window ranking.** 30 days = engagement (what's alive now), 30 years =
    survival (what's load-bearing), 300 years = endurance (what governs taste).
    An entry states its window and evidence; freshest signal wins ties.
12. **Grounded or labeled.** Every claim carries a URL and date. Unverifiable ⇒
    UNVERIFIED, single-source promotional ⇒ flagged. No evidence ⇒ No.
13. **Keep an anti-portfolio.** The failure archive (Katerra, Lustron, WinSun,
    Tango) teaches more than the winners list — and inoculates against the same
    pitch in new clothes.
14. **Curate the overlay separately from the compiled.** Generated graphs/tables
    are disposable; hand-curated judgments (lineage edges, tiers) live in
    editable data files that survive regeneration.

## Community & supply chain

15. **External skills are untrusted code.** Read a SKILL.md before installing;
    prefer ephemeral use over persistent install; human-gate anything that
    executes. Popularity is not a safety proof.
16. **Two-line PRs.** Contribution = edit one YAML entry + `make check`. Low
    friction, high signal; the eval harness does the arguing.
17. **Skills ship with eval-with-teeth.** Every SKILL.md ends with a Verification
    section containing an assertion that must pass before success may be
    declared.
