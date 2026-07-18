---
name: print-ready-check
description: >
  Run the machine-checkable ready gate on an STL and report READY/NOT-READY with
  per-gate evidence (watertight, normals, bed-fit, min-feature). Trigger: "is
  this printable", "check my STL", "why does my print fail". NOT a slicer and
  NOT a substitute for material/temperature tuning.
kind: skill
license: MIT
runtimes: [claude-code, codex, hermes]
---

# print-ready-check

## When to use
Any mesh claiming to be 3D-print ready — generated here or anywhere else.

## What it does
1. Parse the STL (binary or ASCII, stdlib-only).
2. G1 watertight: every directed edge matched by exactly one reverse edge.
3. G2 outward normals: signed volume > 0.
4. G3 bed-fit against the declared printer envelope.
5. G4 min-feature ≥ 2× nozzle diameter.
6. Emit a JSON report; exit 0 only if all gates pass.

## Example
```bash
python3 pipeline/ready_gate.py model.stl --bed 256x256x256 --nozzle 0.4 --min-feature 1.2 --json
```

## Verification (eval-with-teeth)
The gate must catch known-bad meshes — the test suite deletes a triangle
(hole), inverts winding (inside-out), and oversizes the model, and asserts each
fails its gate:
```bash
python3 -m pytest tests/test_ready_gate.py -q
```

## Safety
A READY verdict means geometrically printable, not fit-for-purpose; load-bearing
parts need engineering review.

## Cross-runtime
Stdlib Python CLI; exit codes gate any CI.
