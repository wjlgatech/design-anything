---
name: bodyfit-ready-check
description: >
  Run the body-fit gate on a fit spec (product dimensions for a specific
  body): completeness, anthropometric/ISO ranges, frame-PD optical alignment,
  print floor — eyewear first; dental/prosthetics/footwear share the pattern.
  Trigger: "do these glasses fit", "check this fit spec", "frame for a 63 PD".
  NOT a fitting: face scan, angles, and Rx compatibility are the optician's.
kind: skill
license: MIT
runtimes: [claude-code, codex, hermes]
---

# bodyfit-ready-check

## When to use
Any body-fit product spec claiming to fit a declared body — before geometry
is generated or printed.

## What it does
1. B1 completeness: every `data/bodyfit.yml` dimension declared — undeclared
   is **not measured ⇒ fail**.
2. B2 ranges: each dimension inside its anthropometric/ISO-lineage range.
3. B3 alignment: frame PD (lens_w + bridge) within the decentration budget of
   the wearer's PD — the dispensing rule as a number.
4. B4 print floor: declared min feature ≥ the product's snap threshold; the
   geometry itself is then gated by `print-ready-check` on the STL.

## Example
```bash
python3 examples/eyewear/generate.py fitspec.json temple.stl
python3 pipeline/bodyfit_gate.py fitspec.json --json
python3 pipeline/ready_gate.py temple.stl --min-feature 3.0
```

## Verification (eval-with-teeth)
Success may be declared ONLY when both gates exit 0. Held by tests that
mutate the golden spec five known-bad ways (missing dim, out-of-range PD,
misaligned frame, thin feature, unknown product) and assert each fails:
```bash
python3 -m pytest tests/test_m8_m11_m9.py -q
```

## Safety
Table-fit, not fitted: population ranges say a spec is plausible, not that it
fits one specific face. The report says so.

## Cross-runtime
Python + PyYAML; exit codes gate any CI.
