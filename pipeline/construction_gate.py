#!/usr/bin/env python3
"""construction_gate.py — the machine-checkable definition of "construction ready" (v0.1).

Validates a structured layout (JSON: rooms as polygons, openings as a graph)
against the constraint database in data/clearances.yml. The tables ARE the
gate (principle P2); no evidence => Not ready.

Checks:
  C1 topology      every room polygon closed (>=3 vertices, positive area),
                   room names unique, opening endpoints resolve
  C2 clearances    every opening >= its table minimum width
  C3 habitability  per room type: min area, min dimension, daylight
                   (habitable rooms need >=1 window), ceiling height
  C4 egress        every room reachable from 'exterior' through openings,
                   with >=1 entry-grade door on the exterior
  C5 module-grid   >=90% of coordinates on the ISO 2848 100mm module

Layout schema (units mm):
  {"name": "...", "ceiling_height": 2400,
   "rooms":    [{"name": "living", "type": "living",
                 "polygon": [[x,y], ...], "windows": 2}],
   "openings": [{"type": "door_entry", "width": 900,
                 "between": ["exterior", "hall"]}]}

Usage: python3 pipeline/construction_gate.py layout.json [--json]
Exit 0 = READY, 1 = NOT READY (gates CI).

Honest edges: v0.1 checks the layout graph and dimensions, not geometry
consistency between polygons, structural spans, or jurisdiction code text.
IFC validation is roadmap (needs ifcopenshell). A pass here is a design-sanity
gate, never a permit or a PE stamp.
"""

from __future__ import annotations

import json
import sys
from collections import deque
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
CLEARANCES = ROOT / "data" / "clearances.yml"


def shoelace_area_mm2(poly):
    n = len(poly)
    s = 0.0
    for i in range(n):
        x0, y0 = poly[i]
        x1, y1 = poly[(i + 1) % n]
        s += x0 * y1 - x1 * y0
    return abs(s) / 2.0


def bbox_min_dimension(poly):
    xs = [p[0] for p in poly]
    ys = [p[1] for p in poly]
    return min(max(xs) - min(xs), max(ys) - min(ys))


def run_gate(layout, tables):
    gates = {}
    rooms = layout.get("rooms", [])
    openings = layout.get("openings", [])
    room_names = [r["name"] for r in rooms]
    nodes = set(room_names) | {"exterior"}

    # C1 topology
    problems = []
    if len(set(room_names)) != len(room_names):
        problems.append("duplicate room names")
    for r in rooms:
        poly = r.get("polygon", [])
        if len(poly) < 3:
            problems.append(f"{r['name']}: polygon has <3 vertices")
        elif shoelace_area_mm2(poly) <= 0:
            problems.append(f"{r['name']}: zero-area polygon")
    for o in openings:
        for end in o.get("between", []):
            if end not in nodes:
                problems.append(f"opening endpoint '{end}' is not a room or 'exterior'")
    gates["C1_topology"] = {"pass": not problems,
                            "detail": "; ".join(problems) or f"{len(rooms)} rooms, {len(openings)} openings, all resolve"}

    # C2 opening clearances
    problems = []
    for o in openings:
        spec = tables["openings"].get(o.get("type", ""))
        if spec is None:
            problems.append(f"{o.get('type', '?')}: unknown opening type (no table => not measured => fail)")
        elif o.get("width", 0) < spec["min_width"]:
            problems.append(f"{o['type']} {o.get('between')}: {o.get('width')}mm < {spec['min_width']}mm ({spec['source']})")
    gates["C2_clearances"] = {"pass": not problems,
                              "detail": "; ".join(problems) or "all openings meet table minima"}

    # C3 habitability
    problems = []
    ceiling = layout.get("ceiling_height", 0)
    h_min = tables["heights"]["ceiling_habitable_min"]["value"]
    for r in rooms:
        spec = tables["rooms"].get(r.get("type", ""))
        if spec is None:
            problems.append(f"{r['name']}: unknown room type '{r.get('type')}' (not measured => fail)")
            continue
        area_m2 = shoelace_area_mm2(r["polygon"]) / 1e6
        if area_m2 < spec["min_area"]:
            problems.append(f"{r['name']}: {area_m2:.1f}m2 < {spec['min_area']}m2")
        if bbox_min_dimension(r["polygon"]) < spec["min_dimension"]:
            problems.append(f"{r['name']}: min dimension < {spec['min_dimension']}mm")
        if spec["habitable"]:
            if r.get("windows", 0) < 1:
                problems.append(f"{r['name']}: habitable room without daylight (0 windows)")
            if ceiling < h_min:
                problems.append(f"{r['name']}: ceiling {ceiling}mm < {h_min}mm")
    gates["C3_habitability"] = {"pass": not problems,
                                "detail": "; ".join(problems) or "areas, dimensions, daylight, ceiling OK"}

    # C4 egress / connectivity
    problems = []
    adj = {n: set() for n in nodes}
    for o in openings:
        b = o.get("between", [])
        if len(b) == 2 and b[0] in adj and b[1] in adj:
            adj[b[0]].add(b[1])
            adj[b[1]].add(b[0])
    seen, queue = {"exterior"}, deque(["exterior"])
    while queue:
        for nb in adj[queue.popleft()]:
            if nb not in seen:
                seen.add(nb)
                queue.append(nb)
    unreachable = [n for n in room_names if n not in seen]
    if unreachable:
        problems.append(f"unreachable from exterior: {unreachable}")
    entry_min = tables["openings"]["door_entry"]["min_width"]
    has_entry = any("exterior" in o.get("between", []) and o.get("width", 0) >= entry_min
                    for o in openings)
    if not has_entry:
        problems.append(f"no entry-grade door (>= {entry_min}mm) on the exterior")
    gates["C4_egress"] = {"pass": not problems,
                          "detail": "; ".join(problems) or "all rooms reachable; entry door present"}

    # C5 module grid
    module = tables["grid"]["module"]["value"]
    target = tables["grid"]["min_on_module_pct"]["value"]
    coords = [c for r in rooms for p in r["polygon"] for c in p]
    on_module = sum(1 for c in coords if c % module == 0)
    pct = 100.0 * on_module / len(coords) if coords else 0.0
    gates["C5_module_grid"] = {"pass": pct >= target,
                               "detail": f"{pct:.0f}% of coordinates on the {module}mm module (target {target}%)"}

    return {"file": layout.get("name", "?"), "gates": gates,
            "ready": all(g["pass"] for g in gates.values()),
            "disclaimer": "design-sanity gate, not a permit or PE stamp; jurisdiction codes override"}


def main():
    args = [a for a in sys.argv[1:] if a != "--json"]
    if not args:
        print(__doc__)
        sys.exit(2)
    layout = json.loads(Path(args[0]).read_text())
    tables = yaml.safe_load(CLEARANCES.read_text())
    report = run_gate(layout, tables)
    if "--json" in sys.argv:
        print(json.dumps(report, indent=2))
    else:
        for gid, g in report["gates"].items():
            print(f"  {'PASS' if g['pass'] else 'FAIL'}  {gid}: {g['detail']}")
        print(f"{'READY' if report['ready'] else 'NOT READY'}: {report['file']}  ({report['disclaimer']})")
    sys.exit(0 if report["ready"] else 1)


if __name__ == "__main__":
    main()
