#!/usr/bin/env python3
"""ainative.py — self-audit against data/ainative.yml (rubric-as-data).

Audits HOW the repo operates, with in-repo evidence per principle: a `file`
check passes if the path exists; a `grep` check passes if the pattern occurs
in the file. No evidence => that principle fails (never a fake pass).

Usage: python3 scripts/ainative.py [--gate N]   (default gate from the rubric)
Exit 0 = at/above gate, 1 = below (gates CI, same as a code regression).
"""

from __future__ import annotations

import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
RUBRIC = ROOT / "data" / "ainative.yml"


def evidence_found(check: dict[str, str]) -> bool:
    """One evidence probe: file existence or pattern-in-file."""
    path = ROOT / check["path"]
    if check["type"] == "file":
        return path.exists()
    if check["type"] == "grep":
        return path.exists() and check["pattern"] in path.read_text(errors="replace")
    return False  # unknown check type => not measured => fail


def main() -> None:
    rubric = yaml.safe_load(RUBRIC.read_text())
    gate = rubric["gate"]
    if "--gate" in sys.argv:
        gate = int(sys.argv[sys.argv.index("--gate") + 1])

    results = [(p["id"], evidence_found(p["check"])) for p in rubric["principles"]]
    passed = sum(1 for _, ok in results if ok)
    score = round(100 * passed / len(results))

    for pid, ok in results:
        print(f"  {'PASS' if ok else 'FAIL'}  {pid}")
    verdict = "OK" if score >= gate else "BELOW GATE"
    print(f"ainative: {verdict} — {score}/100 ({passed}/{len(results)} principles, gate {gate})")
    sys.exit(0 if score >= gate else 1)


if __name__ == "__main__":
    main()
