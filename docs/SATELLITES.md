# Satellites — knowledge + tooling compiled from every top-cited repo

design-anything is the hub of three things: **knowledge** (the data spine +
digests), **tooling** (gates, exporters, skills), and **experts** (the
community roster). Satellites extend all three to the repos we cite: every
`repo:`-marked gold entry in `data/tools.yml` gets a knowledge-graph presence
AND a generated skill — **without hand-writing anything that can rot**.

## The one decision everything follows from

**A satellite is a pointer + a SHA-pinned digest + a compiled skill — never a
vendored copy and never a hand-written page.** The compiler
(`scripts/satellites.py`) is the durable asset; satellites are cattle,
regenerated from data. This is the supply-chain backbone (external code is
untrusted; popularity ≠ safety) plus spec-as-data, applied to other people's
repos.

## The five qualities, by mechanism (not aspiration)

| Quality | Mechanism |
|---|---|
| **High quality** | The deep digest (`KNOWLEDGE.md`) is written by an agent that *reads the actual repo at a pinned SHA* — every claim is true of that commit, marked UNVERIFIED otherwise. The generated SKILL.md carries only API-verifiable facts (stars, license, release, push date) with the fetch date. Maker ≠ checker: satellite outputs still pass **our** gates — a satellite generates, only gates say "ready". |
| **Fast** | Initial batch: N parallel digest agents (5 satellites ≈ one wall-clock digest). Everything else is a deterministic compiler — zero tokens, milliseconds. |
| **Cheap** | LLM spend happens **once per digest per SHA** — refresh is triggered by measured staleness, never by a timer. Metadata refresh costs 3 API calls per satellite per week. The compile step costs nothing. |
| **Most up to date** | Freshness is **measured, not promised**: `satellites.py sync` records upstream HEAD; when it moves past the digest's pinned SHA, the satellite flips to **STALE** — visibly, in the skill itself and the graph — instead of being silently wrong. The weekly workflow opens a human-gated PR with what moved. |
| **Future proof** | Bet on the survivors (the Lindy rule applied to infrastructure): the GitHub REST API and git SHAs, not any repo's internals. Satellites die gracefully — an archived/vanished upstream just stops syncing and shows its last-known state with dates. No vendored code means no license drift, no supply-chain surface, no merge debt. |

## The pipeline

```
data/tools.yml (repo: marked)                        the cited repo (upstream)
        │                                                     │
        ▼            gh api (weekly / on demand)              ▼
scripts/satellites.py sync  ──────────────►  data/satellites.yml
        │                                     (stars · push · release · HEAD sha
        │                                      · digest_sha · status)
        ▼ offline, deterministic
scripts/satellites.py build ──►  skills/use-<slug>/SKILL.md   (generated, drift-gated)
                                 skills/use-<slug>/KNOWLEDGE.md (agent digest, SHA-pinned)
        ▼
scripts/build_graph.py      ──►  satellite nodes + edges in docs/graph.json → the live map
```

`make check` runs `satellites.py build --check` (offline drift gate). The
network step (`sync`) lives ONLY in the weekly freshness workflow and local
runs — CI's finish line never depends on the internet.

## Rules

1. **Digest refresh is an event, not a schedule**: status STALE → re-run the
   digest agent against the new SHA → update `digest_sha`. Until then the old
   digest stays, labeled.
2. **Generated skills conform to the house format** (frontmatter,
   Verification, honest edges) and are tested by the same
   `tests/test_structure.py` as hand-made ones, plus `tests/test_satellites.py`.
3. **Graduation path**: a satellite that earns a hand-tuned workflow (e.g.
   blender-mcp as execution backbone) gets a *curated* skill alongside the
   generated one — curation adds, never replaces, the compiled layer.
4. **Scope control**: satellites are for gold-tier cited repos with a `repo:`
   field — adding one is a one-line data change; the compiler does the rest.
