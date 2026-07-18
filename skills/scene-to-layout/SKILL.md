---
name: scene-to-layout
description: >
  Turn a room photo, scan, or point cloud into a structured layout — walls,
  openings, furniture as typed objects with dimensions — using SpatialLM-class
  models, ready for blueprint-validate and re-design. Trigger: "here's a photo
  of my room", "measure this space", "redesign from this picture".
kind: skill
license: CC-BY-4.0
runtimes: [claude-code, codex, hermes]
---

# scene-to-layout

## When to use
The input is a picture (the repo's second input modality) rather than text —
an existing room/site that must become structured data before redesign.

## What it does
1. Route by input: photo → monocular layout estimation; scan/point-cloud →
   SpatialLM (https://github.com/manycore-research/SpatialLM); floor-plan
   image → wall/opening extraction.
2. Emit a structured layout JSON: walls (start/end/height/thickness), openings
   (type/position/size), furniture (class/bbox/orientation), declared units.
3. State per-element confidence; dimensions estimated from a single photo are
   marked ESTIMATED and need one user-confirmed reference measurement.
4. Hand off to blueprint-validate (audit) or brief-to-blueprint (redesign).

## Example
"Photo of a 4x5m living room + 'the door is 80cm' reference" → layout JSON with
scaled dimensions → "now add a reading corner with daylight" → redesign loop.

## Verification (eval-with-teeth)
Output JSON must round-trip: rendered back to a 2D plan, wall topology is
closed (rooms are bounded polygons) and openings lie on walls. An unclosed
room polygon is a failed extraction — report it, don't patch it silently.

## Safety
Never claim measured accuracy from an unreferenced photo; renovation decisions
need a tape measure.

## Cross-runtime
Model access varies by runtime; degrade to "ask user for measurements" when no
vision/SpatialLM backend is available (skip-not-fail).
