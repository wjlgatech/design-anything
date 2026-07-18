# /design-anything — the flagship skill's design contract

The request, evaluated and 10X'd: build a `/design-anything` slash-skill that a
user can invoke **without knowing anything about this repo's internals**, that
discovers their design intent, routes them to the professional process, and is
self-aware, self-healing, and self-improving — with those three properties
**operationally defined and CI-enforced**, not asserted.

## 1. The governing lesson (from /anyagent)

**The skill is a thin router; the engine is the repo.** All logic that can be
tested lives in `pipeline/` (gates), `data/` (tables), `examples/` (golden
generators), `principles/` + `domains/` (knowledge). SKILL.md only: discovers
intent → routes → drives the engine → reports faithfully. A skill that carries
its own logic in markdown can't be tested and silently rots.

## 2. Backbone vs progressive disclosure — the decision table

**Deciding rule (inherited from /anyagent):** if it changes behavior on *every*
design request, it's backbone (lives in SKILL.md, always loaded). If it names a
domain, a target, or a situation, it's disclosure (lives in the repo, loaded on
trigger).

| Backbone (in SKILL.md) | Progressive disclosure (loaded on match) |
|---|---|
| The intent-discovery protocol (§3) | Per-domain guides — `domains/<match>/README.md` only |
| The 6-stage loop: absorb → route → retrieve → compose → gate → reflect | Domain research digests (`RESEARCH.md`, three-window method) |
| "Ready is a gate, not a vibe" + report gate output verbatim | Constraint tables — `data/clearances.yml` / `garment.yml` for the matched target |
| "Emit the composition, not the render" | The DIKW model, design-thinking, disciplines map (read when the user asks *why*) |
| Self-heal protocol (§5) and 3-strike escalation | Golden examples — read the ONE matching the routed target |
| The honesty core: no evidence ⇒ not ready; honest ❌ beats fake ✅ | The landscape tables (only when the brief needs tool selection) |
| Capability self-map via `llms.txt` + `make check` (§4) | Workflow shapes (`workflows/README.md`) for high-stakes review panels |

Budget rule: SKILL.md stays small (one screenful of protocol + a routing
table); everything else is a repo path the skill reads *when triggered*.

## 3. Intent discovery (user doesn't know the toolset)

The user says "I want a bigger balcony" or drops a photo — they never say
"invoke the construction gate". The skill infers three slots and asks **at most
2 questions, only at genuine forks**:

1. **WHAT** (domain) — inferred from nouns/image; fork only if ambiguous
   (e.g. "a chair" → furniture-to-print vs interior layout).
2. **DONE** (target gate) — print / construction / garment / game-sim /
   advice-only. Inferred from context; this is the most common genuine fork.
3. **KNOWNS** (measurements, printer, site, size) — never interrogate;
   propose explicit defaults ("assuming a 220×220 bed — say otherwise") and
   proceed. Defaults are visible, silence is consent, everything re-runs.

Then reflect the absorbed brief back in ≤6 lines and drive. Novices get the
professional process without the vocabulary; experts can name the gate and skip
the discovery.

## 4. Self-aware — operational definition

The skill knows what it can and cannot do **by reading artifacts, not by
claiming**: capabilities come from `llms.txt` (compiled index), gate coverage
from `pipeline/README.md`'s status table, and health from running `make check`
on arrival. It states roadmap gaps honestly (game/sim gate is roadmap — so a
game brief gets composition + principles, and an explicit "no gate yet" flag).
**CI enforcement:** `tests/test_skill.py` asserts every repo path SKILL.md
references exists — the skill cannot drift from the engine.

## 5. Self-heal — operational definition

| Failure | Protocol |
|---|---|
| Repo absent on this machine | Clone from GitHub (public) to a stated path; proceed |
| `make check` red on arrival | Fix the regression FIRST; never build on red |
| Gate fails on generated output | Fix the named failing gate, re-run; same failure 3× → stop and escalate with what was tried |
| Unknown room/garment/opening type | Not-measured ⇒ fail, then propose the missing table entry — never fake a pass |
| Referenced file missing | Fall back to `llms.txt`, report the gap as an issue |

## 6. Self-improve — operational definition

Every run ends with the reflect step; lessons land **in the repo, not the
chat**: a missing constraint becomes a `data/*.yml` PR; a false-READY becomes a
gate-dispute issue; a recurring brief type becomes a golden example. Measured
by artifacts (commits/issues/entries), not by intention. This is the flywheel:
each run either banks nothing (fine) or makes the next run start ahead.

## 7. What 10X'd relative to the request

- Self-* went from adjectives to **protocols with CI teeth** (§4-6).
- The skill ships **inside the engine repo** with a drift test, installed to
  the user's skills dir by symlink — one source of truth, updates flow with
  `git pull`.
- Intent discovery is a bounded protocol (≤2 questions, visible defaults) —
  not "be smart", but a testable conversational contract.
