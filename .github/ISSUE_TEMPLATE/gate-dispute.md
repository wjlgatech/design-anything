---
name: Gate dispute
about: An output claimed READY but failed in the real tool (slicer/Revit/engine) — or a gate wrongly fails a valid design
labels: gate
---

**Which gate:** print (ready_gate.py) · construction (construction_gate.py)

**What happened** (the honest ❌): expected vs observed, in which real tool
(PrusaSlicer/Bambu/Revit/…):

**Repro:** attach the STL/layout JSON or the generator source + exact command.

**Gate report:** paste the `--json` output.

Gate disputes are the most valuable issues this repo gets — a false READY is a
bug in the definition of ready itself.
