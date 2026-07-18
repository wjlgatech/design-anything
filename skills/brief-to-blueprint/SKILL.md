---
name: brief-to-blueprint
description: >
  Compile a messy design brief (text and/or picture) into a structured blueprint
  plan: target (print/construction/game), dimensions, constraints, applicable
  patterns, and the ready-gate it must pass. Trigger: "design me a ...",
  "turn this sketch into a model", "I want a 3D-printable ...". NOT for
  photoreal rendering or structural engineering sign-off.
kind: skill
license: CC-BY-4.0
runtimes: [claude-code, codex, hermes]
---

# brief-to-blueprint

## When to use
The user states a design intent in words or drops an image, and wants a path to
a buildable artifact — not a mood board.

## What it does
1. **Absorb** the brief; reflect it back in ≤6 lines (object, target, size,
   material/process, must-haves). Never silently drop a stated constraint.
2. **Declare the target** — 3D-print | construction | game/sim — and load the
   matching gate spec from `pipeline/`.
3. **Retrieve patterns** (skills/pattern-library) and constraint tables
   (anthropometrics, module grid, DfAM rules for the declared process).
4. **Emit the composition**: deterministic parametric source (Python like
   `examples/planter/generate.py`, OpenSCAD, or CadQuery) with the brief's
   parameters at the top — never an opaque mesh.
5. **Gate it**: generate geometry and run `pipeline/ready_gate.py`. Iterate
   until READY or report the honest failure.

## Example
```bash
# brief: "a desk planter, 120x80x60mm, 3mm walls, my printer is 220x220"
python3 examples/planter/generate.py out.stl
python3 pipeline/ready_gate.py out.stl --bed 220x220x250 --min-feature 3.0
```

## Verification (eval-with-teeth)
Success may be declared ONLY when the gate exits 0:
```bash
python3 pipeline/ready_gate.py out.stl --min-feature <declared-wall> && echo VERIFIED
```
No gate pass ⇒ the skill reports NOT READY with the failing gate's evidence.

## Safety
Outputs are design aids, not engineering certifications. Construction-target
outputs must carry: "checklist ≠ structural engineer's stamp".

## Cross-runtime
Pure prompts + stdlib Python; no runtime-specific APIs.
