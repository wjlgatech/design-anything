#!/usr/bin/env python3
"""ready_gate.py — the machine-checkable definition of "3D-print ready".

Stdlib-only, deterministic. A blueprint may not claim "ready" unless this gate
passes. No evidence => Not ready.

Checks (print target):
  G1 watertight     every directed edge is matched by exactly one reverse edge
                    (closed, 2-manifold, consistently wound)
  G2 outward        signed volume > 0 (normals point out; mesh is not inside-out)
  G3 bed-fit        bounding box fits the declared printer bed
  G4 min-feature    declared minimum feature (wall/base) >= nozzle_mm * 2

Usage:
  python3 pipeline/ready_gate.py model.stl --bed 220x220x250 --nozzle 0.4 \
      --min-feature 2.4 [--json]

Exit code 0 = READY, 1 = NOT READY (gates CI).
"""

from __future__ import annotations

import argparse
import json
import struct
import sys


def read_stl(path):
    """Parse binary or ASCII STL. Returns a list of triangles [(v0, v1, v2)]."""
    with open(path, "rb") as f:
        data = f.read()
    if data[:5] == b"solid" and b"facet" in data[:500]:
        return _read_ascii(data)
    return _read_binary(data)


def _read_binary(data):
    (n,) = struct.unpack_from("<I", data, 80)
    tris = []
    off = 84
    for _ in range(n):
        vals = struct.unpack_from("<12f", data, off)
        tris.append((tuple(vals[3:6]), tuple(vals[6:9]), tuple(vals[9:12])))
        off += 50
    return tris


def _read_ascii(data):
    verts, tris = [], []
    for line in data.decode("ascii", "replace").splitlines():
        parts = line.split()
        if parts[:1] == ["vertex"]:
            verts.append(tuple(float(x) for x in parts[1:4]))
            if len(verts) == 3:
                tris.append(tuple(verts))
                verts = []
    return tris


def check_watertight(tris):
    """G1: each directed edge must be matched by exactly one reverse edge."""
    edges = {}
    for tri in tris:
        for i in range(3):
            e = (tri[i], tri[(i + 1) % 3])
            edges[e] = edges.get(e, 0) + 1
    bad = sum(1 for (a, b), c in edges.items() if c != 1 or edges.get((b, a), 0) != 1)
    return bad == 0, f"{bad} unmatched/duplicate directed edges" if bad else "closed 2-manifold"


def signed_volume(tris):
    """G2: sum of tetra volumes; positive iff consistently outward-wound."""
    v = 0.0
    for (x0, y0, z0), (x1, y1, z1), (x2, y2, z2) in tris:
        v += (x0 * (y1 * z2 - z1 * y2)
              - y0 * (x1 * z2 - z1 * x2)
              + z0 * (x1 * y2 - y1 * x2))
    return v / 6.0


def bounds(tris):
    xs = [v[i] for t in tris for v in t for i in (0,)]
    ys = [v[1] for t in tris for v in t]
    zs = [v[2] for t in tris for v in t]
    return (max(xs) - min(xs), max(ys) - min(ys), max(zs) - min(zs))


def run_gate(path, bed, nozzle_mm, min_feature_mm):
    tris = read_stl(path)
    report = {"file": path, "triangles": len(tris), "gates": {}, "ready": False}
    if not tris:
        report["gates"]["G0_nonempty"] = {"pass": False, "detail": "no triangles"}
        return report

    ok1, d1 = check_watertight(tris)
    report["gates"]["G1_watertight"] = {"pass": ok1, "detail": d1}

    vol = signed_volume(tris)
    report["gates"]["G2_outward_normals"] = {
        "pass": vol > 0, "detail": f"signed volume {vol:.1f} mm^3"}

    dims = bounds(tris)
    fits = all(d <= b for d, b in zip(sorted(dims), sorted(bed)))
    report["gates"]["G3_bed_fit"] = {
        "pass": fits,
        "detail": f"model {tuple(round(d, 1) for d in dims)} mm vs bed {bed} mm"}

    ok4 = min_feature_mm >= nozzle_mm * 2
    report["gates"]["G4_min_feature"] = {
        "pass": ok4,
        "detail": f"min feature {min_feature_mm} mm vs 2x nozzle {nozzle_mm * 2} mm"}

    report["ready"] = all(g["pass"] for g in report["gates"].values())
    return report


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("stl")
    ap.add_argument("--bed", default="220x220x250", help="printer bed WxDxH in mm")
    ap.add_argument("--nozzle", type=float, default=0.4, help="nozzle diameter mm")
    ap.add_argument("--min-feature", type=float, required=True,
                    help="smallest declared feature (wall/base) in mm")
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args()

    bed = tuple(float(x) for x in args.bed.lower().split("x"))
    report = run_gate(args.stl, bed, args.nozzle, args.min_feature)

    if args.json:
        print(json.dumps(report, indent=2))
    else:
        for gid, g in report["gates"].items():
            print(f"  {'PASS' if g['pass'] else 'FAIL'}  {gid}: {g['detail']}")
        print(f"{'READY' if report['ready'] else 'NOT READY'}: {args.stl}")
    sys.exit(0 if report["ready"] else 1)


if __name__ == "__main__":
    main()
