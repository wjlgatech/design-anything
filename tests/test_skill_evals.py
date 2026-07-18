"""CI gate for the /design-anything eval suite (GOAL.md M14).

Model-graded runs happen in the skill-creator harness; what CI can enforce
deterministically: the scenarios are well-formed, both trigger classes exist,
referenced fixtures exist, and the broken fixture is GENUINELY broken (an eval
against a healthy fixture would be a fake test).
"""

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
EVALS = ROOT / "skills" / "design-anything" / "evals" / "evals.json"

sys.path.insert(0, str(ROOT / "pipeline"))
import ready_gate  # noqa: E402


def _evals():
    return json.loads(EVALS.read_text())["evals"]


def test_minimum_scenario_count_and_shape():
    evals = _evals()
    assert len(evals) >= 3, "Anthropic checklist: 3+ eval scenarios"
    ids = [e["id"] for e in evals]
    assert len(set(ids)) == len(ids), "duplicate eval ids"
    for e in evals:
        assert e["query"].strip(), f"{e['id']}: empty query"
        assert e["expected_behavior"], f"{e['id']}: no expected_behavior"
        assert "design-anything" in e["skills"], f"{e['id']}: wrong skills field"
        assert isinstance(e["should_trigger"], bool), f"{e['id']}: missing should_trigger"


def test_both_trigger_classes_present():
    evals = _evals()
    assert any(e["should_trigger"] for e in evals)
    assert sum(1 for e in evals if not e["should_trigger"]) >= 2, \
        "need should-NOT-trigger cases to measure the NOT-for clause"


def test_every_gated_route_has_a_scenario():
    text = json.dumps(_evals())
    for gate in ("ready_gate.py", "construction_gate.py", "pattern_gate.py"):
        assert gate in text, f"no eval scenario exercises {gate}"


def test_fixture_files_exist():
    for e in _evals():
        for f in e.get("files", []):
            if "/" in f:  # repo paths only; prose placeholders are allowed
                assert (ROOT / f).exists(), f"{e['id']}: missing fixture {f}"


def test_broken_fixture_is_genuinely_broken():
    stl = ROOT / "skills" / "design-anything" / "evals" / "fixtures" / "broken-hole.stl"
    report = ready_gate.run_gate(str(stl), (220.0, 220.0, 250.0), 0.4, 3.0)
    assert not report["gates"]["G1_watertight"]["pass"], \
        "the 'broken' eval fixture passes the gate — the eval would be fake"
    assert not report["ready"]
