---
name: blueprint-validate
description: >
  Validate a blueprint against the survival-tested principles checklist:
  anthropometric clearances, modular grid conformance, daylight orientation,
  shearing-layer separation, open-system interfaces. Trigger: "review this
  floor plan", "is this layout sane", "principles check". NOT code-compliance
  certification.
kind: skill
license: CC-BY-4.0
runtimes: [claude-code, codex, hermes]
---

# blueprint-validate

## When to use
A floor plan, room layout, or building blueprint exists (image, IFC, or
parametric source) and needs a principled review before deeper investment.

## What it does
Walks `principles/DESIGN_PRINCIPLES.md` P1–P13 as a checklist against the
blueprint, scoring each as PASS / FAIL / NOT-MEASURED:
1. Clearances vs Neufert-class tables (doors ≥ 800mm, corridors ≥ 900mm,
   counter work zones, stair geometry).
2. Module grid: % of dimensions on the declared grid (target ≥ 90%).
3. Daylight: every habitable room has an orientation-justified window.
4. Layers: services accessible without demolishing structure.
5. Open system: standard parts (windows/doors/fasteners) vs proprietary.

## Example
Ask: "validate examples/planter against P2/P3" or hand a floor-plan image and
the declared module (e.g. 100mm) and printer/process.

## Verification (eval-with-teeth)
The report must list every principle with a verdict and evidence line;
NOT-MEASURED items are excluded from the score and named in the summary —
a blocking review cannot pass with unmeasured blocking items. An overall score
with no per-item evidence is an invalid output.

## Safety
This is a design review, not a permit document. Jurisdiction codes override
everything here.

## Cross-runtime
Prompt-only; no execution required.
