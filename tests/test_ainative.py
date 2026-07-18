"""The AI-native self-audit must be real: rubric valid, evidence honest."""

import subprocess
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]


def test_rubric_is_well_formed():
    rubric = yaml.safe_load((ROOT / "data" / "ainative.yml").read_text())
    assert rubric["gate"] >= 80
    assert len(rubric["principles"]) >= 10
    for p in rubric["principles"]:
        assert p["id"] and p["why"], f"{p.get('id')}: principle needs id and why"
        assert p["check"]["type"] in ("file", "grep"), f"{p['id']}: unknown check type"
        assert "path" in p["check"]


def test_audit_passes_at_gate():
    r = subprocess.run([sys.executable, str(ROOT / "scripts" / "ainative.py")],
                       capture_output=True, text=True)
    assert r.returncode == 0, r.stdout


def test_missing_evidence_fails_not_fakes():
    r = subprocess.run([sys.executable, str(ROOT / "scripts" / "ainative.py"),
                        "--gate", "101"], capture_output=True, text=True)
    assert r.returncode == 1, "an unreachable gate must exit non-zero, never fake a pass"
