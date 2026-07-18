# Game design

**Input:** concept text, reference art → **Output:** level geometry (glTF/USD), rulesets, world layouts.

## The stack (evidence-ranked)
- **Assets:** TRELLIS.2 (open), Meshy-6/Tripo (SaaS + engine plugins) — see [data/tools.yml](../../data/tools.yml).
- **Worlds:** Marble (World Labs), Project Genie — ideation layer, not engine replacement.
- **Layout:** WaveFunctionCollapse for constraint-based level generation (ships in Townscaper, Bad North).
- **Engines (survivors):** Unreal (28y), Unity (21y), Blender as DCC (30y).

## Governing principles
- **P11 rule economy** — few orthogonal mechanics, large emergent state space (the chess/Go test). Measure depth/complexity ratio via self-play.
- **Magic circle (Huizinga)** — play spaces need explicit boundaries, entry/exit rituals, internally consistent rules.
- **Caillois play-type mix as input parameter** — an ilinx space (vertigo) and an agôn arena (competition) have opposite geometry requirements.
- **Prospect/refuge (P5)** applies to arenas exactly as to living rooms.

## Ready gate (roadmap)
glTF/USD validity · poly/texture budget · true-to-scale units · collision mesh present · decision-density report for rulesets.
