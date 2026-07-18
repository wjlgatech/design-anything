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

import yaml

ROOT = Path(__file__).resolve().parents[1]
TABLES_PATH = ROOT / "data" / "garment.yml"


def area_mm2(poly):
    s = 0.0
    for i in range(len(poly)):
        x0, y0 = poly[i]
        x1, y1 = poly[(i + 1) % len(poly)]
        s += x0 * y1 - x1 * y0
    return abs(s) / 2.0


def bbox(poly):
    xs = [p[0] for p in poly]
    ys = [p[1] for p in poly]
    return min(xs), min(ys), max(xs), max(ys)


def bboxes_overlap(a, b):
    return a[0] < b[2] and b[0] < a[2] and a[1] < b[3] and b[1] < a[3]


def run_gate(marker, tables):
    gates = {}
    pieces = marker.get("pieces", [])
    names = [p["name"] for p in pieces]

    # F1 pieces
    problems = []
    if len(set(names)) != len(names):
        problems.append("duplicate piece names")
    allowed = tables["grain"]["allowed_angles_deg"]["values"]
    for p in pieces:
        poly = p.get("polygon", [])
        if len(poly) < 3 or area_mm2(poly) <= 0:
            problems.append(f"{p.get('name', '?')}: invalid polygon")
        if p.get("grain_angle_deg") not in allowed:
            problems.append(f"{p.get('name', '?')}: grain angle {p.get('grain_angle_deg')} "
                            f"not declared/allowed {allowed}")
    gates["F1_pieces"] = {"pass": not problems,
                          "detail": "; ".join(problems) or f"{len(pieces)} pieces, grain declared"}

    # F2 fabric-fit
    problems = []
    width = marker.get("fabric", {}).get("width", 0)
    boxes = {}
    for p in pieces:
        b = bbox(p["polygon"])
        boxes[p["name"]] = b
        if b[0] < 0 or b[1] < 0 or b[2] > width:
            problems.append(f"{p['name']}: outside fabric width {width}mm")
    checked = sorted(boxes)
    for i, a in enumerate(checked):
        for b in checked[i + 1:]:
            if bboxes_overlap(boxes[a], boxes[b]):
                problems.append(f"{a} overlaps {b} (bbox)")
    gates["F2_fabric_fit"] = {"pass": not problems,
                              "detail": "; ".join(problems) or
                              f"all pieces within {width}mm width, no bbox overlaps"}

    # F3 seam allowance
    sa = marker.get("seam_allowance", 0)
    sa_min = tables["seam_allowance"]["min"]["value"]
    gates["F3_seam_allowance"] = {"pass": sa >= sa_min,
                                  "detail": f"{sa}mm vs table min {sa_min}mm"}

    # F4 marker efficiency
    if pieces and width:
        marker_len = max(bbox(p["polygon"])[3] for p in pieces)
        used = width * marker_len
        piece_area = sum(area_mm2(p["polygon"]) for p in pieces)
        pct = 100.0 * piece_area / used if used else 0.0
    else:
        marker_len, pct = 0, 0.0
    floor = tables["marker"]["min_efficiency_pct"]["value"]
    gates["F4_marker_efficiency"] = {"pass": pct >= floor,
                                     "detail": f"{pct:.0f}% of {width}x{marker_len:.0f}mm "
                                               f"fabric used (floor {floor}%)"}

    # F5 human fit
    problems = []
    gtype = marker.get("garment_type", "")
    fit_table = tables.get(f"fit_{gtype}")
    if fit_table is None:
        problems.append(f"unknown garment type '{gtype}' (no fit table => not measured => fail)")
    else:
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
    gates["F5_human_fit"] = {"pass": not problems,
                             "detail": "; ".join(problems) or f"fit table '{gtype}' satisfied"}

    return {"file": marker.get("name", "?"), "gates": gates,
            "ready": all(g["pass"] for g in gates.values()),
            "disclaimer": "marker-and-tables gate; drape/sewability need a muslin"}


def main():
    args = [a for a in sys.argv[1:] if a != "--json"]
    if not args:
        print(__doc__)
        sys.exit(2)
    marker = json.loads(Path(args[0]).read_text())
    tables = yaml.safe_load(TABLES_PATH.read_text())
    report = run_gate(marker, tables)
    if "--json" in sys.argv:
        print(json.dumps(report, indent=2))
    else:
        for gid, g in report["gates"].items():
            print(f"  {'PASS' if g['pass'] else 'FAIL'}  {gid}: {g['detail']}")
        print(f"{'READY' if report['ready'] else 'NOT READY'}: {report['file']}  ({report['disclaimer']})")
    sys.exit(0 if report["ready"] else 1)


if __name__ == "__main__":
    main()
