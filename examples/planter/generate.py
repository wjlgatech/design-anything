#!/usr/bin/env python3
"""generate.py — golden example: text brief -> parametric solid -> STL.

Brief: "a rectangular desk planter, 120mm x 80mm x 60mm, 3mm walls, printable
on a stock 220x220 FDM printer with a 0.4mm nozzle."

Principle (from animate-anything): emit the COMPOSITION, not the render. This
file *is* the blueprint — deterministic, parametric, reviewable source. The STL
is a compiled artifact; pipeline/ready_gate.py is the acceptance test.

Usage: python3 examples/planter/generate.py [out.stl]
"""

from __future__ import annotations

import struct
import sys

# ---- the parametric brief (edit these; the gate keeps you honest) ----------
W, D, H = 120.0, 80.0, 60.0   # outer width, depth, height (mm)
WALL = 3.0                    # wall thickness (mm)  -> min feature
BASE = 4.0                    # base thickness (mm)
# ----------------------------------------------------------------------------


def quad(a, b, c, d):
    """One rectangular face -> two triangles, preserving winding."""
    return [(a, b, c), (a, c, d)]


def planter(w, d, h, t, base):
    """Open-top rectangular planter as a closed 2-manifold solid (28 tris)."""
    # outer shell corners
    o = {(x, y, z): (w * x, d * y, h * z) for x in (0, 1) for y in (0, 1) for z in (0, 1)}
    # inner cavity corners (cavity floor at z=base, open to the top rim)
    ix, iy = w - t, d - t
    n = {(x, y, z): (t if x == 0 else ix, t if y == 0 else iy, base if z == 0 else h)
         for x in (0, 1) for y in (0, 1) for z in (0, 1)}

    tris = []
    # outer bottom (viewed from below: -z outward)
    tris += quad(o[0, 0, 0], o[0, 1, 0], o[1, 1, 0], o[1, 0, 0])
    # outer sides (outward normals)
    tris += quad(o[0, 0, 0], o[1, 0, 0], o[1, 0, 1], o[0, 0, 1])  # front  -y
    tris += quad(o[1, 0, 0], o[1, 1, 0], o[1, 1, 1], o[1, 0, 1])  # right  +x
    tris += quad(o[1, 1, 0], o[0, 1, 0], o[0, 1, 1], o[1, 1, 1])  # back   +y
    tris += quad(o[0, 1, 0], o[0, 0, 0], o[0, 0, 1], o[0, 1, 1])  # left   -x
    # cavity floor (faces up into the cavity: +z outward from material)
    tris += quad(n[0, 0, 0], n[1, 0, 0], n[1, 1, 0], n[0, 1, 0])
    # cavity walls (normals point INTO the cavity, i.e. away from material)
    tris += quad(n[0, 0, 0], n[0, 0, 1], n[1, 0, 1], n[1, 0, 0])  # front inner +y
    tris += quad(n[1, 0, 0], n[1, 0, 1], n[1, 1, 1], n[1, 1, 0])  # right inner -x
    tris += quad(n[1, 1, 0], n[1, 1, 1], n[0, 1, 1], n[0, 1, 0])  # back inner  -y
    tris += quad(n[0, 1, 0], n[0, 1, 1], n[0, 0, 1], n[0, 0, 0])  # left inner  +x
    # top rim (annulus between outer and inner top edges, +z outward)
    tris += quad(o[0, 0, 1], o[1, 0, 1], n[1, 0, 1], n[0, 0, 1])  # front strip
    tris += quad(o[1, 0, 1], o[1, 1, 1], n[1, 1, 1], n[1, 0, 1])  # right strip
    tris += quad(o[1, 1, 1], o[0, 1, 1], n[0, 1, 1], n[1, 1, 1])  # back strip
    tris += quad(o[0, 1, 1], o[0, 0, 1], n[0, 0, 1], n[0, 1, 1])  # left strip
    return tris


def write_stl(path, tris):
    with open(path, "wb") as f:
        f.write(b"design-anything planter (parametric golden example)".ljust(80, b"\0"))
        f.write(struct.pack("<I", len(tris)))
        for v0, v1, v2 in tris:
            f.write(struct.pack("<3f", 0.0, 0.0, 0.0))  # normal (recomputed by slicers)
            for v in (v0, v1, v2):
                f.write(struct.pack("<3f", *v))
            f.write(struct.pack("<H", 0))


if __name__ == "__main__":
    out = sys.argv[1] if len(sys.argv) > 1 else "planter.stl"
    tris = planter(W, D, H, WALL, BASE)
    write_stl(out, tris)
    print(f"wrote {out}: {len(tris)} triangles, "
          f"{W}x{D}x{H} mm, wall {WALL} mm, base {BASE} mm")
