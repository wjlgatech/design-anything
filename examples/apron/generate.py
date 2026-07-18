#!/usr/bin/env python3
"""generate.py — golden example: text brief -> parametric pattern -> marker JSON.

Brief: "a workshop apron, unisex M: bib front, one big pocket, waist ties and
an over-head neck strap; cut from standard 1500mm-wide canvas with a defensible
zero-waste marker."

Same principle as the planter and the studio flat: emit the COMPOSITION.
This file is the pattern block; marker.json is the compiled artifact;
pipeline/pattern_gate.py is the acceptance test.

Usage: python3 examples/apron/generate.py [out.json]
"""

from __future__ import annotations

import json
import sys

# ---- the parametric brief (all mm) ------------------------------------------
FABRIC_W = 1500
SEAM = 12
BODY_W, BODY_L = 800, 900     # apron body: full width, chest-to-knee length
BIB_W = 300                   # bib width at the top edge
BIB_DROP = 400                # length of the angled bib sides
POCKET_W, POCKET_L = 400, 250
TIE_W, TIE_L = 80, 900        # two waist ties
STRAP_W, STRAP_L = 60, 600    # neck strap
# ------------------------------------------------------------------------------


def apron():
    waist_y = BODY_L - BIB_DROP
    side = (BODY_W - BIB_W) / 2
    body = [[0, 0], [BODY_W, 0], [BODY_W, waist_y],
            [BODY_W - side, BODY_L], [side, BODY_L], [0, waist_y]]
    col = BODY_W + 50   # lay small pieces in a column right of the body
    return {
        "name": "workshop-apron",
        "units": "mm",
        "garment_type": "apron",
        "fabric": {"width": FABRIC_W},
        "seam_allowance": SEAM,
        "pieces": [
            {"name": "body", "polygon": body, "grain_angle_deg": 0},
            {"name": "waist_tie_left",
             "polygon": [[col, 0], [col + TIE_W, 0], [col + TIE_W, TIE_L], [col, TIE_L]],
             "grain_angle_deg": 0},
            {"name": "waist_tie_right",
             "polygon": [[col + 110, 0], [col + 110 + TIE_W, 0],
                         [col + 110 + TIE_W, TIE_L], [col + 110, TIE_L]],
             "grain_angle_deg": 0},
            {"name": "neck_strap",
             "polygon": [[col + 220, 0], [col + 220 + STRAP_W, 0],
                         [col + 220 + STRAP_W, STRAP_L], [col + 220, STRAP_L]],
             "grain_angle_deg": 0},
            {"name": "pocket",
             "polygon": [[col + 220, STRAP_L + 50], [col + 220 + POCKET_W, STRAP_L + 50],
                         [col + 220 + POCKET_W, STRAP_L + 50 + POCKET_L],
                         [col + 220, STRAP_L + 50 + POCKET_L]],
             "grain_angle_deg": 0},
        ],
        "fit": {
            "waist_tie_total": 2 * TIE_L,
            "neck_strap": STRAP_L,
            "body_length": BODY_L,
        },
    }


if __name__ == "__main__":
    out = sys.argv[1] if len(sys.argv) > 1 else "marker.json"
    marker = apron()
    with open(out, "w") as f:
        json.dump(marker, f, indent=2)
    print(f"wrote {out}: {len(marker['pieces'])} pieces on {FABRIC_W}mm fabric, "
          f"seam {SEAM}mm")
