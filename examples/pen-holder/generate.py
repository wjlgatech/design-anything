#!/usr/bin/env python3
"""generate.py — golden example: text brief -> parametric hex solid -> STL.

Brief: "a hexagonal desk pen holder, printable on a 220x220 bed" — banked from
the first live dogfood run of /design-anything (2026-07-19), per the reflect
protocol: a recurring brief type becomes a golden example. It covers what no
other golden does: fan-triangulated non-rectangular geometry (hex rings +
center fans) that must still close as a 2-manifold.

Usage: python3 examples/pen-holder/generate.py [out.stl]
"""

from __future__ import annotations

import math
import struct
import sys

# ---- the parametric brief (mm) ----------------------------------------------
R_OUT = 45.0    # hex outer radius (across corners)
WALL = 3.0      # wall thickness  -> min feature
BASE = 5.0      # base thickness
H = 100.0       # height
# ------------------------------------------------------------------------------

Vec = tuple[float, float, float]


def hexagon(r: float, z: float) -> list[Vec]:
    """Six vertices of a regular hexagon at height z."""
    return [(r * math.cos(math.pi / 3 * i), r * math.sin(math.pi / 3 * i), z)
            for i in range(6)]


def quad(a: Vec, b: Vec, c: Vec, d: Vec) -> list[tuple[Vec, Vec, Vec]]:
    """One rectangular face as two triangles, preserving winding."""
    return [(a, b, c), (a, c, d)]


def pen_holder() -> list[tuple[Vec, Vec, Vec]]:
    """Open-top hex prism with cavity as a closed 2-manifold (48 tris)."""
    tris: list[tuple[Vec, Vec, Vec]] = []
    ob, ot = hexagon(R_OUT, 0.0), hexagon(R_OUT, H)
    ib, it = hexagon(R_OUT - WALL, BASE), hexagon(R_OUT - WALL, H)
    cb: Vec = (0.0, 0.0, 0.0)      # center of outer bottom
    ci: Vec = (0.0, 0.0, BASE)     # center of cavity floor
    for i in range(6):
        j = (i + 1) % 6
        tris.append((cb, ob[j], ob[i]))              # outer bottom fan (down)
        tris += quad(ob[i], ob[j], ot[j], ot[i])     # outer wall (out)
        tris.append((ci, ib[i], ib[j]))              # cavity floor fan (up)
        tris += quad(ib[j], ib[i], it[i], it[j])     # inner wall (into cavity)
        tris += quad(ot[i], ot[j], it[j], it[i])     # top rim (up)
    return tris


def write_stl(path: str, tris: list) -> None:
    """Write triangles as binary STL (normals left to the slicer)."""
    with open(path, "wb") as f:
        f.write(b"design-anything hex pen holder (dogfood-born golden)".ljust(80, b"\0"))
        f.write(struct.pack("<I", len(tris)))
        for v0, v1, v2 in tris:
            f.write(struct.pack("<3f", 0.0, 0.0, 0.0))
            for v in (v0, v1, v2):
                f.write(struct.pack("<3f", *v))
            f.write(struct.pack("<H", 0))


if __name__ == "__main__":
    out = sys.argv[1] if len(sys.argv) > 1 else "pen_holder.stl"
    tris = pen_holder()
    write_stl(out, tris)
    print(f"wrote {out}: {len(tris)} triangles, hex R{R_OUT} H{H} mm, wall {WALL} mm")
