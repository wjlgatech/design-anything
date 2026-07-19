#!/usr/bin/env python3
"""bodyfit_gate.py — the machine-checkable definition of "body-fit ready" (v0.1).

Validates a fit spec (JSON: product dimensions for a specific body) against
data/bodyfit.yml. First product: eyewear. The tables ARE the gate; an
undeclared dimension is not measured => fail.

Checks:
  B1 completeness   every table dimension declared in the spec
  B2 ranges         every dimension inside its anthropometric/ISO-lineage range
  B3 alignment      frame PD (lens_w + bridge) within the decentration budget
                    of the wearer's PD — the optical-fit rule
  B4 printability   declared min feature >= the product's print floor
                    (the geometry itself is gated by ready_gate on the STL)

Spec schema (mm):
  {"name": "...", "product": "eyewear",
   "dimensions": {"pd": 63, "bridge": 18, "lens_w": 48, "lens_h": 38,
                  "temple_l": 140},
   "min_feature": 3.0}

Usage: python3 pipeline/bodyfit_gate.py fitspec.json [--json]
Exit 0 = READY, 1 = NOT READY (gates CI).

Honest edges: v0.1 checks dimensional fit against population tables — not the
individual face scan, wrap/pantoscopic angles, weight balance, or lens
prescription compatibility. A pass means table-fit, not fitted.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any, Callable, Iterable

import yaml

from gate import CheckResult, Gate, emit_report

ROOT = Path(__file__).resolve().parents[1]
TABLES_PATH = ROOT / "data" / "bodyfit.yml"

Spec = dict[str, Any]


class BodyFitGate(Gate):
    """Fit-spec gate against anthropometric/ISO-lineage dimension tables."""

    disclaimer = "table-fit gate, not a fitting; face scan, angles, and Rx compatibility are the optician's"

    def __init__(self, tables: dict[str, Any]) -> None:
        self.tables = tables

    def checks(self) -> Iterable[tuple[str, Callable[[Spec], CheckResult]]]:
        return [
            ("B1_completeness", self.check_completeness),
            ("B2_ranges", self.check_ranges),
            ("B3_alignment", self.check_alignment),
            ("B4_printability", self.check_printability),
        ]

    def _product_table(self, spec: Spec) -> dict[str, Any] | None:
        return self.tables.get(spec.get("product", ""))

    def check_completeness(self, spec: Spec) -> CheckResult:
        """B1: every table dimension declared; unknown product => fail."""
        table = self._product_table(spec)
        if table is None:
            return CheckResult(False, f"unknown product '{spec.get('product')}' "
                                      "(no table => not measured => fail)")
        dims = spec.get("dimensions", {})
        missing = [d for d in table["dimensions"] if d not in dims]
        return CheckResult(not missing,
                           f"missing: {missing} (not measured => fail)" if missing
                           else f"all {len(table['dimensions'])} dimensions declared")

    def check_ranges(self, spec: Spec) -> CheckResult:
        """B2: each dimension inside its table range."""
        table = self._product_table(spec)
        if table is None:
            return CheckResult(False, "no product table")
        problems = []
        for dim, bounds in table["dimensions"].items():
            val = spec.get("dimensions", {}).get(dim)
            if val is None:
                continue  # B1 already fails the gate for this
            if not bounds["min"] <= val <= bounds["max"]:
                problems.append(f"{dim}={val} outside [{bounds['min']}, {bounds['max']}] "
                                f"({bounds['source']})")
        return CheckResult.from_problems(problems, "all dimensions in range")

    def check_alignment(self, spec: Spec) -> CheckResult:
        """B3: frame PD vs wearer PD within the decentration budget."""
        table = self._product_table(spec)
        dims = spec.get("dimensions", {})
        if table is None or not all(k in dims for k in ("pd", "lens_w", "bridge")):
            return CheckResult(False, "pd/lens_w/bridge not all declared (not measured => fail)")
        frame_pd = dims["lens_w"] + dims["bridge"]
        offset = abs(frame_pd - dims["pd"])
        budget = table["alignment"]["max_frame_pd_offset"]["value"]
        return CheckResult(offset <= budget,
                           f"frame PD {frame_pd} vs wearer PD {dims['pd']}: "
                           f"offset {offset}mm (budget {budget}mm)")

    def check_printability(self, spec: Spec) -> CheckResult:
        """B4: declared min feature above the product's print floor."""
        table = self._product_table(spec)
        if table is None:
            return CheckResult(False, "no product table")
        floor = table["print"]["min_feature"]["value"]
        mf = spec.get("min_feature")
        if mf is None:
            return CheckResult(False, "min_feature not declared (not measured => fail)")
        return CheckResult(mf >= floor, f"min feature {mf}mm vs floor {floor}mm — "
                                        "geometry itself gated by ready_gate on the STL")


def run_gate(spec: Spec, tables: dict[str, Any]) -> dict[str, Any]:
    """Module-level entry point (kept stable for tests, skills, and evals)."""
    return BodyFitGate(tables).run(spec)


def main() -> None:
    args = [a for a in sys.argv[1:] if a != "--json"]
    if not args:
        print(__doc__)
        sys.exit(2)
    spec = json.loads(Path(args[0]).read_text())
    tables = yaml.safe_load(TABLES_PATH.read_text())
    emit_report(run_gate(spec, tables), as_json="--json" in sys.argv)


if __name__ == "__main__":
    main()
