"""Repo-structure gate: the operating system's own invariants.

- every skill has a SKILL.md with required frontmatter and a Verification section
- registry entries point at real skill dirs
- research digests exist and carry the honesty markers
- GOAL.md (the 10X contract) and core docs exist
"""

from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]

CORE_DOCS = [
    "README.md", "GOAL.md", "CONTRIBUTING.md", "LICENSE", "Makefile",
    "principles/DESIGN_PRINCIPLES.md", "best-practices/BEST_PRACTICES.md",
    "pipeline/README.md", "pipeline/ready_gate.py", "pipeline/pattern_gate.py",
    "principles/DIKW_MODEL.md", "principles/DESIGN_THINKING.md",
    "docs/DESIGN_DISCIPLINES.md", "docs/SKILL_DESIGN.md",
    "skills/design-anything/SKILL.md",
    "bundles/design-from-brief.yaml", "workflows/README.md",
]

DIGESTS = [
    "research/last30days/DIGEST.md",
    "research/last30years/DIGEST.md",
    "research/last300years/DIGEST.md",
]

DOMAINS = ["game-design", "simulation", "architecture-residential",
           "architecture-commercial", "interior-design", "landscape", "garment-design"]


def _frontmatter(text):
    assert text.startswith("---"), "SKILL.md must start with YAML frontmatter"
    return yaml.safe_load(text.split("---", 2)[1])


def test_core_docs_exist():
    missing = [p for p in CORE_DOCS if not (ROOT / p).exists()]
    assert not missing, f"missing core docs: {missing}"


def test_domain_guides_exist():
    missing = [d for d in DOMAINS if not (ROOT / "domains" / d / "README.md").exists()]
    assert not missing, f"missing domain guides: {missing}"


def test_research_digests_exist_and_are_honest():
    for p in DIGESTS:
        text = (ROOT / p).read_text()
        assert len(text) > 2000, f"{p}: digest suspiciously thin"
        assert "http" in text, f"{p}: no URLs — ungrounded research"
    # the honesty marker must appear where claims were unverifiable
    assert "UNVERIFIED" in (ROOT / DIGESTS[0]).read_text()


def test_skills_have_valid_frontmatter_and_teeth():
    skill_dirs = [d for d in (ROOT / "skills").iterdir() if d.is_dir()]
    assert len(skill_dirs) >= 6, "GOAL.md M2 requires >= 6 skills"
    for d in skill_dirs:
        md = d / "SKILL.md"
        assert md.exists(), f"{d.name}: no SKILL.md"
        fm = _frontmatter(md.read_text())
        for key in ("name", "description", "kind", "license", "runtimes"):
            assert key in fm, f"{d.name}: frontmatter missing '{key}'"
        assert fm["name"] == d.name, f"{d.name}: frontmatter name mismatch"
        assert "## Verification" in md.read_text(), \
            f"{d.name}: no eval-with-teeth Verification section"


def test_registry_paths_resolve():
    entries = yaml.safe_load((ROOT / "data" / "registry.yml").read_text())
    for e in entries:
        if "path" in e:
            assert (ROOT / e["path"] / "SKILL.md").exists(), \
                f"registry entry {e['name']}: path does not resolve to a SKILL.md"


def test_goal_contract_defines_ready():
    text = (ROOT / "GOAL.md").read_text()
    for marker in ("READY-GATE", "watertight", "Milestone", "Non-goals"):
        assert marker in text, f"GOAL.md missing '{marker}'"
