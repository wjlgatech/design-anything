# Dynamic workflows

Bundles (`../bundles/`) are static compositions. Dynamic workflows are
orchestration *scripts* — deterministic control flow (loops, fan-out,
adversarial verification) over many agents, for work one context can't hold.

## design-review-panel (the canonical shape)

For a high-stakes blueprint, fan out independent reviewers and adversarially
verify every finding before it reaches the user:

```
phase Review:   parallel agents, one per lens —
                  structure (P1/P3), human-factors (P2/P10),
                  buildability (P7/P8), climate (P9), taste (P4/P5)
phase Verify:   each finding → N independent skeptics prompted to REFUTE it;
                a finding survives only on majority non-refutation
phase Gate:     run pipeline/ready_gate.py + blueprint-validate on the artifact
return:         confirmed findings, ranked; gate report attached
```

Rules inherited from the operating system:
- **Maker ≠ checker** — a generating agent never verifies its own output.
- **Loop-until-dry** for discovery (keep spawning finders until 2 consecutive
  rounds surface nothing new); simple counters miss the tail.
- **No silent caps** — if coverage is bounded (top-N rooms, sampled views),
  say what was dropped.

## survey-the-field

Re-run the three-window research (skills/design-research) as a fan-out:
one agent per window × one per domain, synthesis agent merges with the
freshness/survival tie-break rules, output lands in `research/*/DIGEST.md`
and `data/*.yml` — then `make readme` recompiles the front door.

Implementations are harness-specific (Claude Code `Workflow`, a cron, or a CI
matrix); the shapes above are the contract.
