"""Integrity gate for the /design-anything flagship skill.

Enforces the operational definition of self-aware (docs/SKILL_DESIGN.md):
the skill routes to engine artifacts, so every path it references must exist —
the skill cannot drift from the engine. Budgets follow Anthropic's skill
authoring guidance (description <= 1024 chars, body < 500 lines, references
one level deep into the repo).
"""

import re
from glob import glob
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / "skills" / "design-anything" / "SKILL.md"

PATH_RE = re.compile(
    r"`?((?:pipeline|data|examples|domains|principles|docs|skills|workflows|"
    r"bundles|research|\.github)/[\w\-./*]+\.[a-z]+|llms\.txt)`?")


def _parts():
    text = SKILL.read_text()
    fm = yaml.safe_load(text.split("---", 2)[1])
    body = text.split("---", 2)[2]
    return text, fm, body


def test_frontmatter_follows_anthropic_budgets():
    _, fm, _ = _parts()
    assert fm["name"] == "design-anything"  # command name comes from dir name
    desc = fm["description"]
    assert desc and len(desc) <= 1024, f"description {len(desc)} chars > 1024"
    assert "Use when" in desc, "description needs a 'Use when' trigger sentence"
    assert "NOT for" in desc, "description needs a NOT-for clause"
    assert not desc.lstrip().startswith(("I ", "You ")), "description must be third person"


def test_body_stays_lean():
    text, _, _ = _parts()
    assert len(text.splitlines()) < 500, "SKILL.md must stay under 500 lines"


def test_every_referenced_engine_path_exists():
    _, _, body = _parts()
    missing = []
    for ref in set(PATH_RE.findall(body)):
        if "*" in ref:
            if not glob(str(ROOT / ref)):
                missing.append(ref)
        elif not (ROOT / ref).exists():
            missing.append(ref)
    assert not missing, f"skill references missing engine paths: {sorted(missing)}"


def test_skill_declares_the_thin_router_contract():
    _, _, body = _parts()
    for marker in ("thin router", "make check", "verbatim", "not a permit"):
        assert marker in body, f"backbone contract missing '{marker}'"


def test_registered_and_dogfooded():
    entries = yaml.safe_load((ROOT / "data" / "registry.yml").read_text())
    entry = next((e for e in entries if e["name"] == "design-anything"), None)
    assert entry is not None, "flagship skill missing from data/registry.yml"
    assert entry.get("status") == "dogfooded"
