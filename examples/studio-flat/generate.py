#!/usr/bin/env python3
"""generate.py — golden example: text brief -> parametric floor plan -> layout JSON.

Brief: "a compact studio flat, ~28 m2: living room with kitchenette zone,
separate kitchen and bathroom off an entry hall; everything code-sane and on
the 100mm module."

Same principle as the planter: emit the COMPOSITION. This file is the
blueprint; layout.json is the compiled artifact;
pipeline/construction_gate.py is the acceptance test.

Usage: python3 examples/studio-flat/generate.py [out.json]
"""

from __future__ import annotations

import json
import sys

# ---- the parametric brief (all mm, all on the 100mm module) -----------------
CEILING = 2400
ROW1_H = 2100        # service row: hall + bathroom + kitchen
LIVING_D = 3600      # living room depth
HALL_W, BATH_W, KITCHEN_W = 1200, 1600, 2200
WIDTH = HALL_W + BATH_W + KITCHEN_W   # 5000 overall
# ------------------------------------------------------------------------------


def rect(x0: int, y0: int, x1: int, y1: int) -> list:
    """Axis-aligned rectangle as a 4-point polygon."""
    return [[x0, y0], [x1, y0], [x1, y1], [x0, y1]]


def studio() -> dict:
    """The parametric studio flat: service row (hall/bath/kitchen) + living room."""
    x_bath = HALL_W
    x_kitchen = HALL_W + BATH_W
    return {
        "name": "studio-flat",
        "units": "mm",
        "ceiling_height": CEILING,
        "rooms": [
            {"name": "hall", "type": "hall",
             "polygon": rect(0, 0, HALL_W, ROW1_H), "windows": 0},
            {"name": "bathroom", "type": "bathroom",
             "polygon": rect(x_bath, 0, x_kitchen, ROW1_H), "windows": 0},
            {"name": "kitchen", "type": "kitchen",
             "polygon": rect(x_kitchen, 0, WIDTH, ROW1_H), "windows": 1},
            {"name": "living", "type": "living",
             "polygon": rect(0, ROW1_H, WIDTH, ROW1_H + LIVING_D), "windows": 2},
        ],
        "openings": [
            {"type": "door_entry", "width": 900, "between": ["exterior", "hall"]},
            {"type": "door_interior", "width": 800, "between": ["hall", "living"]},
            {"type": "door_bathroom", "width": 700, "between": ["hall", "bathroom"]},
            {"type": "door_interior", "width": 800, "between": ["living", "kitchen"]},
        ],
    }


if __name__ == "__main__":
    out = sys.argv[1] if len(sys.argv) > 1 else "layout.json"
    layout = studio()
    with open(out, "w") as f:
        json.dump(layout, f, indent=2)
    area = sum(
        (r["polygon"][2][0] - r["polygon"][0][0]) * (r["polygon"][2][1] - r["polygon"][0][1])
        for r in layout["rooms"]) / 1e6
    print(f"wrote {out}: {len(layout['rooms'])} rooms, {area:.1f} m2, "
          f"{WIDTH}x{ROW1_H + LIVING_D} mm overall")
