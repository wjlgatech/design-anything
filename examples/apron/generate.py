#!/usr/bin/env python3
"""generate.py — golden example: text brief -> parametric pattern -> marker JSON.

Brief: "a workshop apron, graded S/M/L: bib front, one big pocket, waist ties
and an over-head neck strap; cut from standard 1500mm-wide canvas with a
defensible zero-waste marker."

Same principle as the planter, studio flat, and arena: emit the COMPOSITION.
This file is the pattern block; marker.json is the compiled artifact;
pipeline/pattern_gate.py is the acceptance test and pipeline/dxf_aama.py the
factory-format exporter.

Grading (ASTM D5585 lineage): a pattern that can't grade coherently across a
size run is a demo, not a product — SIZES below are the grade rules, and every
size must pass the gate (tests/test_dxf_and_grading.py).

Usage: python3 examples/apron/generate.py [out.json] [--size S|M|L]
"""

from __future__ import annotations

import json
import sys

# ---- the parametric brief (all mm) ------------------------------------------
FABRIC_W = 1500
SEAM = 12
BIB_W = 300                   # bib width at the top edge (constant across sizes)
BIB_DROP = 400                # length of the angled bib sides
POCKET_W, POCKET_L = 400, 250
TIE_W, STRAP_W = 80, 60

# grade rules: per-size values for the dimensions that move (ASTM-lineage
# proportional grading; each size must independently pass the fit tables)
SIZES: dict[str, dict[str, float]] = {
    "S": {"body_w": 770, "body_l": 850, "tie_l": 875, "strap_l": 575},
    "M": {"body_w": 800, "body_l": 900, "tie_l": 900, "strap_l": 600},
    "L": {"body_w": 820, "body_l": 950, "tie_l": 925, "strap_l": 625},
}
# ------------------------------------------------------------------------------


def apron(size: str = "M") -> dict:
    """The parametric apron marker for one size of the grade run."""
    g = SIZES[size]
    body_w, body_l, tie_l, strap_l = g["body_w"], g["body_l"], g["tie_l"], g["strap_l"]
    waist_y = body_l - BIB_DROP
    side = (body_w - BIB_W) / 2
    body = [[0, 0], [body_w, 0], [body_w, waist_y],
            [body_w - side, body_l], [side, body_l], [0, waist_y]]
    col = body_w + 50   # lay small pieces in a column right of the body
    return {
        "name": f"workshop-apron-{size}",
        "units": "mm",
        "garment_type": "apron",
        "size": size,
        "fabric": {"width": FABRIC_W},
        "seam_allowance": SEAM,
        "pieces": [
            {"name": "body", "polygon": body, "grain_angle_deg": 0},
            {"name": "waist_tie_left",
             "polygon": [[col, 0], [col + TIE_W, 0], [col + TIE_W, tie_l], [col, tie_l]],
             "grain_angle_deg": 0},
            {"name": "waist_tie_right",
             "polygon": [[col + 110, 0], [col + 110 + TIE_W, 0],
                         [col + 110 + TIE_W, tie_l], [col + 110, tie_l]],
             "grain_angle_deg": 0},
            {"name": "neck_strap",
             "polygon": [[col + 220, 0], [col + 220 + STRAP_W, 0],
                         [col + 220 + STRAP_W, strap_l], [col + 220, strap_l]],
             "grain_angle_deg": 0},
            {"name": "pocket",
             "polygon": [[col + 220, strap_l + 50], [col + 220 + POCKET_W, strap_l + 50],
                         [col + 220 + POCKET_W, strap_l + 50 + POCKET_L],
                         [col + 220, strap_l + 50 + POCKET_L]],
             "grain_angle_deg": 0},
        ],
        # symmetric cut-2-alike pieces must stay identical through grading
        "seam_pairs": [
            {"a": "waist_tie_left", "b": "waist_tie_right", "tolerance_mm": 1.0},
        ],
        "fit": {
            "waist_tie_total": 2 * tie_l,
            "neck_strap": strap_l,
            "body_length": body_l,
        },
    }


if __name__ == "__main__":
    argv = [a for a in sys.argv[1:] if not a.startswith("--") and a not in ("S", "M", "L")]
    size = sys.argv[sys.argv.index("--size") + 1] if "--size" in sys.argv else "M"
    out = argv[0] if argv else "marker.json"
    marker = apron(size)
    with open(out, "w") as f:
        json.dump(marker, f, indent=2)
    print(f"wrote {out}: size {size}, {len(marker['pieces'])} pieces on "
          f"{FABRIC_W}mm fabric, seam {SEAM}mm")
