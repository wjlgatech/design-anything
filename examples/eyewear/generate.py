#!/usr/bin/env python3
"""generate.py — golden example: measurements -> fit spec + printable temple.

Brief: "reading glasses for a 63mm PD, printable on a stock FDM machine."

The body-fit pattern (docs/DESIGN_DISCIPLINES.md Tier 2): anthropometric
tables + parametric-from-measurements + print gate. This file emits BOTH
artifacts of the pattern:
  - fitspec.json  -> gated by pipeline/bodyfit_gate.py (table fit)
  - temple.stl    -> gated by pipeline/ready_gate.py (printable geometry)

The temple blank is straight; the ear bend is a post-print thermoform step
(standard finishing practice) — stated, not hidden.

Usage: python3 examples/eyewear/generate.py [fitspec.json] [temple.stl]
"""

from __future__ import annotations

import json
import struct
import sys

# ---- the parametric brief (mm) ----------------------------------------------
PD = 63.0            # wearer's interpupillary distance
BRIDGE = 18.0        # DBL
LENS_W = 48.0        # boxed A
LENS_H = 38.0        # boxed B
TEMPLE_L = 140.0     # temple length
TEMPLE_W = 3.0       # cross-section width  -> the min feature
TEMPLE_H = 8.0       # cross-section height
# ------------------------------------------------------------------------------


def fitspec() -> dict:
    """The fit spec the bodyfit gate validates."""
    return {
        "name": f"reading-frame-pd{PD:.0f}",
        "product": "eyewear",
        "dimensions": {"pd": PD, "bridge": BRIDGE, "lens_w": LENS_W,
                       "lens_h": LENS_H, "temple_l": TEMPLE_L},
        "min_feature": TEMPLE_W,
    }


def quad(a: tuple, b: tuple, c: tuple, d: tuple) -> list:
    """One rectangular face as two triangles, preserving winding."""
    return [(a, b, c), (a, c, d)]


def temple() -> list:
    """The temple blank as a closed box solid (12 tris, trivially manifold)."""
    w, h, ln = TEMPLE_W, TEMPLE_H, TEMPLE_L
    v = {(x, y, z): (ln * x, w * y, h * z) for x in (0, 1) for y in (0, 1) for z in (0, 1)}
    tris = []
    tris += quad(v[0, 0, 0], v[0, 1, 0], v[1, 1, 0], v[1, 0, 0])  # bottom
    tris += quad(v[0, 0, 1], v[1, 0, 1], v[1, 1, 1], v[0, 1, 1])  # top
    tris += quad(v[0, 0, 0], v[1, 0, 0], v[1, 0, 1], v[0, 0, 1])  # front
    tris += quad(v[1, 1, 0], v[0, 1, 0], v[0, 1, 1], v[1, 1, 1])  # back
    tris += quad(v[0, 1, 0], v[0, 0, 0], v[0, 0, 1], v[0, 1, 1])  # left
    tris += quad(v[1, 0, 0], v[1, 1, 0], v[1, 1, 1], v[1, 0, 1])  # right
    return tris


def write_stl(path: str, tris: list) -> None:
    """Write triangles as binary STL (normals left to the slicer)."""
    with open(path, "wb") as f:
        f.write(b"design-anything eyewear temple blank".ljust(80, b"\0"))
        f.write(struct.pack("<I", len(tris)))
        for v0, v1, v2 in tris:
            f.write(struct.pack("<3f", 0.0, 0.0, 0.0))
            for v in (v0, v1, v2):
                f.write(struct.pack("<3f", *v))
            f.write(struct.pack("<H", 0))


if __name__ == "__main__":
    spec_out = sys.argv[1] if len(sys.argv) > 1 else "fitspec.json"
    stl_out = sys.argv[2] if len(sys.argv) > 2 else "temple.stl"
    with open(spec_out, "w") as f:
        json.dump(fitspec(), f, indent=2)
    write_stl(stl_out, temple())
    print(f"wrote {spec_out} (frame PD {LENS_W + BRIDGE:.0f} for wearer PD {PD:.0f}) "
          f"and {stl_out} ({TEMPLE_L:.0f}mm temple blank, min feature {TEMPLE_W}mm)")
