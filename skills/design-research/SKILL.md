---
name: design-research
description: >
  Run the three-window research method on any design question: /last30days
  (engagement — what's alive now), /last30years (survival — what's load-bearing),
  /last300years (endurance — what governs taste). Trigger: "research X for this
  design", "what's the state of the art in Y", "has Z ever worked".
kind: skill
license: CC-BY-4.0
runtimes: [claude-code, codex, hermes]
---

# design-research

## When to use
Before betting the repo, a project, or a client on a tool, method, or principle.

## What it does
1. **30 days**: rank by observed engagement — releases, stars, pushes, dated
   announcements. Freshest verified signal wins; reputation counts for nothing.
2. **30 years**: rank by survival — still-used + built-upon + hype-survived
   (the 3-probe test). Tier 🏛/🌳/🌱; under-10-years can never outrank a survivor.
3. **300 years**: rank by endurance with a Whig-history guard — keep the
   surviving kernel, flag the superseded dogma (Modulor's ruler, not his city).
4. **Synthesize the Lindy read**: bet interfaces on survivors, hot-swap the
   young layer, and record the anti-portfolio (who was louder and died).

## Example
The repo's own digests are the golden output: `research/last30days/DIGEST.md`,
`research/last30years/DIGEST.md`, `research/last300years/DIGEST.md`.

## Verification (eval-with-teeth)
Every entry carries a URL; dated claims carry dates; anything unverifiable is
marked UNVERIFIED; single-source promotional claims are flagged as such.
A digest with unlabeled uncertainty is a failed run — no evidence ⇒ No.

## Safety
Research grounds decisions; it doesn't make them. Surface trade-offs, let the
human pick at genuine forks.

## Cross-runtime
Needs web search in the harness; degrades to knowledge-cutoff answers with an
explicit staleness warning.
