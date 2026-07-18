#!/usr/bin/env python3
"""gate.py — the Gate seam every ready-gate implements.

A Gate is a ClosedLoop evaluator: named checks over a subject, an honest
report (no evidence => not ready), an exit code that gates CI. Encapsulating
the shape here means every gate reports, prints, and exits identically —
and a new domain gate is just a subclass with check methods.
"""

from __future__ import annotations

import json
import sys
from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any, Callable, Iterable


@dataclass
class CheckResult:
    """Outcome of one named check: verdict plus human-readable evidence."""

    passed: bool
    detail: str

    @classmethod
    def from_problems(cls, problems: list[str], ok_detail: str) -> "CheckResult":
        """Fail with the joined problem list, or pass with the ok summary."""
        return cls(not problems, "; ".join(problems) or ok_detail)


class Gate(ABC):
    """Base class for all ready-gates (print, construction, pattern, ...)."""

    #: one-line honesty statement appended to every report
    disclaimer: str = ""

    @abstractmethod
    def checks(self) -> Iterable[tuple[str, Callable[[Any], CheckResult]]]:
        """Yield (check_id, check_fn) pairs, run in order."""

    def subject_name(self, subject: Any) -> str:
        """Label for the report; dict subjects default to their 'name'."""
        return subject.get("name", "?") if isinstance(subject, dict) else str(subject)

    def extra_report_fields(self, subject: Any) -> dict[str, Any]:
        """Hook for gate-specific report fields (e.g. triangle count)."""
        return {}

    def run(self, subject: Any) -> dict[str, Any]:
        """Run every check; ready only if all pass. The report is the truth."""
        gates: dict[str, dict[str, Any]] = {}
        for check_id, check_fn in self.checks():
            result = check_fn(subject)
            gates[check_id] = {"pass": result.passed, "detail": result.detail}
        return {
            "file": self.subject_name(subject),
            **self.extra_report_fields(subject),
            "gates": gates,
            "ready": all(g["pass"] for g in gates.values()),
            "disclaimer": self.disclaimer,
        }


def emit_report(report: dict[str, Any], as_json: bool) -> None:
    """Print a gate report (shared CLI surface) and exit with its verdict."""
    if as_json:
        print(json.dumps(report, indent=2))
    else:
        for gate_id, g in report["gates"].items():
            print(f"  {'PASS' if g['pass'] else 'FAIL'}  {gate_id}: {g['detail']}")
        verdict = "READY" if report["ready"] else "NOT READY"
        suffix = f"  ({report['disclaimer']})" if report.get("disclaimer") else ""
        print(f"{verdict}: {report['file']}{suffix}")
    sys.exit(0 if report["ready"] else 1)
