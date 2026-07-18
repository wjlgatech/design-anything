# Contributing

**The two-line PR:** edit one entry in `data/*.yml`, run `make check`, open a PR.

## Rules

1. **Every entry needs a working URL** and a one-sentence, non-hypey blurb (≤220 chars).
2. **Never hand-edit generated tables** in README.md — edit `data/*.yml` and run `make readme`. CI's drift gate will catch you.
3. **Evidence or UNVERIFIED.** Dated claims carry dates; tiers follow the three-window method in `research/` (engagement / survival / endurance) — not vibes, not fame.
4. **Skills** go in `skills/<name>/SKILL.md` with frontmatter (`name`, `description`, `kind`, `license`, `runtimes`) and a **Verification** section containing an assertion that must pass before success may be declared. Register in `data/registry.yml`. Community skills are `status: submitted` until they ship runnable evidence.
5. **Code** (pipeline/, scripts/, examples/) is stdlib-only in the core loop; heavy dependencies belong in optional skills.
6. **`make check` must be green.** It runs schema validation, the test suite, the README drift gate, and the ready gate on the golden example.

## What to contribute first

- A tool/paper/person entry with fresh evidence (or a correction with better evidence).
- A gate: the construction (IFC) and game (glTF/USD) ready-gates are the roadmap's flagship items — see [GOAL.md](GOAL.md).
- A golden example for a new domain that passes its gate with zero dependencies.
- A room-specific constraint table (Neufert-class) as data.
