---
name: pattern-library
description: >
  Retrieve applicable Alexander-style patterns (context/problem/solution) for a
  design brief BEFORE generating form — courtyard, light on two sides, entrance
  transition, prospect/refuge, six-foot balcony, and per-domain equivalents.
  Trigger: "what patterns apply", or invoked by brief-to-blueprint step 3.
kind: skill
license: CC-BY-4.0
runtimes: [claude-code, codex, hermes]
---

# pattern-library

## When to use
Before massing/layout generation for any architecture, interior, landscape, or
game-level brief. Patterns are the generator's representation (principle P5).

## What it does
1. Parse the brief's context: climate zone, lot depth, privacy needs, program,
   play-type mix (for games: agôn/alea/mimicry/ilinx).
2. Match against the pattern set in `principles/DESIGN_PRINCIPLES.md` and the
   300-year digest (courtyard for deep plans, lightwell, entrance transition,
   prospect/refuge for both rooms and game arenas).
3. Return each match as context / problem / solution / source, plus explicit
   conflicts between selected patterns.

## Example
"Brief: narrow 8m-wide row-house lot, hot-dry climate, family of 5" →
courtyard (light/air/privacy in one move), thick-wall thermal mass, sheltered
entrance transition.

## Verification (eval-with-teeth)
Every returned pattern must cite its survival evidence (source + years in use)
from `research/last300years/DIGEST.md`. A pattern without lineage is an
invention, not a retrieval — label it PROPOSED, never mix it into the canon.

## Safety
Patterns are priors, not mandates; site and code override.

## Cross-runtime
Prompt-only.
