# Design thinking — survival-tested, honestly

Design thinking gets the same three-probe treatment as everything else here:
still-used + built-upon + hype-survived. It splits cleanly into a 🏛 kernel and
a 🌳/fading wrapper.

## The lineage

| Tier | Layer | Evidence |
|---|---|---|
| 🏛 | **Herbert Simon, *The Sciences of the Artificial* (1969)** — "Everyone designs who devises courses of action aimed at changing existing situations into preferred ones." | 55+ years as the intellectual root; still the standard citation defining design as a discipline. https://mitpress.mit.edu/9780262537537/the-sciences-of-the-artificial/ |
| 🏛 | **Rittel & Webber, wicked problems (1973)** — some problems can't be solved, only re-solved; the problem definition IS design work. | Continuously cited across planning, policy, software; 50+ years unreplaced. |
| 🌳 | **IDEO (1991, David Kelley) / Stanford d.school (2005) / Double Diamond (UK Design Council, 2005) / Tim Brown, *Change by Design* (2009)** — the popularized 5-step recipe (empathize→define→ideate→prototype→test). | Still taught worldwide; d.school still operating; the Double Diamond still the UK Design Council's official model. |
| ⚠️ | **The critique wave** — Natasha Jen's "Design Thinking Is Bullshit" (2017); MIT Technology Review, "Design thinking was supposed to fix the world. Where did it go wrong?" (2023). | The workshop-theater layer (post-its as deliverable, innovation sprints as outcome) is in documented decline — an honest ⚠️, not a dismissal. https://www.technologyreview.com/2023/02/09/1067821/design-thinking-retrospective-what-went-wrong/ |

## The verdict (Whig-guard applied)

**Keep the kernel, drop the theater.** The kernel survives because it's the
[DIKW rhythm](DIKW_MODEL.md) in disguise:

1. **Diverge, then converge** — expression (generate many options) followed by
   compression (select against constraints), run twice (problem space, then
   solution space). The Double Diamond's shape is the survivor; its worksheet
   is not.
2. **Build to think** — a prototype is a question asked in the artifact's own
   language. This repo's golden examples are exactly that.
3. **Test with the user, early, in their tool** — not in your slides. Here:
   verify at the user's altitude (does it slice in PrusaSlicer, import in
   Revit?), and gate-disputes are user testing institutionalized.
4. **Empathy = load the human tables** — the operationalizable core of
   "empathize" is anthropometrics, clearances, fit charts (P2). Feelings about
   users don't gate; tables do.

## What it changes in this repo

- `brief-to-blueprint` step 1 (absorb, reflect back, never drop a constraint)
  is the define phase with teeth.
- Generate **N options before gating one** when the brief is open — diverge
  before converge; the design-review-panel workflow is the converge step.
- A failed gate is a prototype doing its job — the loop, not the exception.
