#!/usr/bin/env python3
"""pattern_gate.py — the machine-checkable definition of "cut-and-sew ready" (v0.1).

Validates a garment pattern marker (JSON: pattern pieces placed on fabric)
against data/garment.yml. The tables ARE the gate; no evidence => Not ready.

Checks:
  F1 pieces        valid polygons (>=3 vertices, positive area), unique names,
                   grain angle declared and allowed
  F2 fabric-fit    every piece inside the fabric width and marker length;
                   no piece bounding boxes overlap (bbox-level, not exact
                   nesting — stated honestly)
  F3 seam          declared seam allowance >= table minimum
  F4 efficiency    marker efficiency (piece area / fabric-used area) >= table
                   floor — the zero-waste lineage as a number
  F5 human-fit     declared fit dimensions inside the garment's fit table
                   (unknown garment type => not measured => fail)

Marker schema (units mm):
  {"name": "...", "garment_type": "apron",
   "fabric": {"width": 1500}, "seam_allowance": 12,
   "pieces": [{"name": "body", "polygon": [[x,y],...], "grain_angle_deg": 0}],
   "fit": {"waist_tie_total": 1800, "neck_strap": 600, "body_length": 900}}

Usage: python3 pipeline/pattern_gate.py marker.json [--json]
Exit 0 = READY, 1 = NOT READY (gates CI).

Honest edges: v0.1 checks the marker and fit tables, not drape, stretch,
sewability order, or pattern-piece seam-line matching. A pass means the marker
cuts; fit beyond the declared dimensions needs a muslin (the garment world's
prototype — build to think).
"""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any, Callable, Iterable

import yaml

from gate import CheckResult, Gate, emit_report

ROOT = Path(__file__).resolve().parents[1]
TABLES_PATH = ROOT / "data" / "garment.yml"

Polygon = list[list[float]]
Marker = dict[str, Any]
Box = tuple[float, float, float, float]


def area_mm2(poly: Polygon) -> float:
    """Absolute polygon area via the shoelace formula, in mm^2."""
    s = 0.0
    for i in range(len(poly)):
        x0, y0 = poly[i]
        x1, y1 = poly[(i + 1) % len(poly)]
        s += x0 * y1 - x1 * y0
    return abs(s) / 2.0


def bbox(poly: Polygon) -> Box:
    """Axis-aligned bounding box (min_x, min_y, max_x, max_y)."""
    xs = [p[0] for p in poly]
    ys = [p[1] for p in poly]
    return min(xs), min(ys), max(xs), max(ys)


def bboxes_overlap(a: Box, b: Box) -> bool:
    """True if two bounding boxes intersect."""
    return a[0] < b[2] and b[0] < a[2] and a[1] < b[3] and b[1] < a[3]


def perimeter_mm(poly: Polygon) -> float:
    """Closed-polygon perimeter length, in mm."""
    total = 0.0
    for i in range(len(poly)):
        x0, y0 = poly[i]
        x1, y1 = poly[(i + 1) % len(poly)]
        total += ((x1 - x0) ** 2 + (y1 - y0) ** 2) ** 0.5
    return total


class PatternGate(Gate):
    """Marker gate: pieces, grain, fabric fit, seam, zero-waste, fit tables."""

    disclaimer = "marker-and-tables gate; drape/sewability need a muslin"

    def __init__(self, tables: dict[str, Any]) -> None:
        self.tables = tables

    def checks(self) -> Iterable[tuple[str, Callable[[Marker], CheckResult]]]:
        return [
            ("F1_pieces", self.check_pieces),
            ("F2_fabric_fit", self.check_fabric_fit),
            ("F3_seam_allowance", self.check_seam_allowance),
            ("F4_marker_efficiency", self.check_marker_efficiency),
            ("F5_human_fit", self.check_human_fit),
            ("F6_seam_pairs", self.check_seam_pairs),
        ]

    def check_pieces(self, marker: Marker) -> CheckResult:
        """F1: valid polygons, unique names, grain declared and allowed."""
        pieces = marker.get("pieces", [])
        names = [p["name"] for p in pieces]
        problems = []
        if len(set(names)) != len(names):
            problems.append("duplicate piece names")
        allowed = self.tables["grain"]["allowed_angles_deg"]["values"]
        for p in pieces:
            poly = p.get("polygon", [])
            if len(poly) < 3 or area_mm2(poly) <= 0:
                problems.append(f"{p.get('name', '?')}: invalid polygon")
            if p.get("grain_angle_deg") not in allowed:
                problems.append(f"{p.get('name', '?')}: grain angle "
                                f"{p.get('grain_angle_deg')} not declared/allowed {allowed}")
        return CheckResult.from_problems(problems, f"{len(pieces)} pieces, grain declared")

    def check_fabric_fit(self, marker: Marker) -> CheckResult:
        """F2: pieces inside the fabric width; no bbox overlaps."""
        width = marker.get("fabric", {}).get("width", 0)
        problems = []
        boxes: dict[str, Box] = {}
        for p in marker.get("pieces", []):
            b = bbox(p["polygon"])
            boxes[p["name"]] = b
            if b[0] < 0 or b[1] < 0 or b[2] > width:
                problems.append(f"{p['name']}: outside fabric width {width}mm")
        names = sorted(boxes)
        for i, a in enumerate(names):
            for b in names[i + 1:]:
                if bboxes_overlap(boxes[a], boxes[b]):
                    problems.append(f"{a} overlaps {b} (bbox)")
        return CheckResult.from_problems(
            problems, f"all pieces within {width}mm width, no bbox overlaps")

    def check_seam_allowance(self, marker: Marker) -> CheckResult:
        """F3: declared seam allowance meets the table minimum."""
        sa = marker.get("seam_allowance", 0)
        sa_min = self.tables["seam_allowance"]["min"]["value"]
        return CheckResult(sa >= sa_min, f"{sa}mm vs table min {sa_min}mm")

    def check_marker_efficiency(self, marker: Marker) -> CheckResult:
        """F4: piece area over fabric-used area beats the zero-waste floor."""
        pieces = marker.get("pieces", [])
        width = marker.get("fabric", {}).get("width", 0)
        if pieces and width:
            marker_len = max(bbox(p["polygon"])[3] for p in pieces)
            used = width * marker_len
            piece_area = sum(area_mm2(p["polygon"]) for p in pieces)
            pct = 100.0 * piece_area / used if used else 0.0
        else:
            marker_len, pct = 0.0, 0.0
        floor = self.tables["marker"]["min_efficiency_pct"]["value"]
        return CheckResult(
            pct >= floor,
            f"{pct:.0f}% of {width}x{marker_len:.0f}mm fabric used (floor {floor}%)")

    def check_human_fit(self, marker: Marker) -> CheckResult:
        """F5: declared fit dimensions inside the garment's fit table."""
        gtype = marker.get("garment_type", "")
        fit_table = self.tables.get(f"fit_{gtype}")
        if fit_table is None:
            return CheckResult(
                False, f"unknown garment type '{gtype}' (no fit table => not measured => fail)")
        problems = []
        fit = marker.get("fit", {})
        for dim, spec in fit_table.items():
            val = fit.get(dim)
            if val is None:
                problems.append(f"fit.{dim} not declared (not measured => fail)")
                continue
            if "min" in spec and val < spec["min"]:
                problems.append(f"fit.{dim}: {val} < {spec['min']} ({spec['source']})")
            if "max" in spec and val > spec["max"]:
                problems.append(f"fit.{dim}: {val} > {spec['max']} ({spec['source']})")
        return CheckResult.from_problems(problems, f"fit table '{gtype}' satisfied")

    def check_seam_pairs(self, marker: Marker) -> CheckResult:
        """F6: declared seam/symmetry pairs match in length within tolerance
        (grading breaks symmetric pieces first — this catches it)."""
        pairs = marker.get("seam_pairs", [])
        if not pairs:
            return CheckResult(True, "0 seam pairs declared (nothing to match)")
        by_name = {p["name"]: p["polygon"] for p in marker.get("pieces", [])}
        problems = []
        for pair in pairs:
            a, b = pair.get("a"), pair.get("b")
            tol = pair.get("tolerance_mm", 1.0)
            if a not in by_name or b not in by_name:
                problems.append(f"pair {a}~{b}: piece missing (not measured => fail)")
                continue
            la, lb = perimeter_mm(by_name[a]), perimeter_mm(by_name[b])
            if abs(la - lb) > tol:
                problems.append(f"{a} ({la:.1f}mm) vs {b} ({lb:.1f}mm): "
                                f"differ by {abs(la - lb):.1f}mm > {tol}mm")
        return CheckResult.from_problems(
            problems, f"{len(pairs)} pair(s) matched within tolerance")


def run_gate(marker: Marker, tables: dict[str, Any]) -> dict[str, Any]:
    """Module-level entry point (kept stable for tests, skills, and evals)."""
    return PatternGate(tables).run(marker)


def main() -> None:
    args = [a for a in sys.argv[1:] if a != "--json"]
    if not args:
        print(__doc__)
        sys.exit(2)
    marker = json.loads(Path(args[0]).read_text())
    tables = yaml.safe_load(TABLES_PATH.read_text())
    emit_report(run_gate(marker, tables), as_json="--json" in sys.argv)


if __name__ == "__main__":
    main()
