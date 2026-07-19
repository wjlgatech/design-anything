#!/usr/bin/env python3
"""garmentcode_export.py — emit a marker as a GarmentCode pattern specification.

GarmentCode (ETH) is the research-native interchange the text-to-pattern wave
targets (see skills/use-garmentcode/KNOWLEDGE.md, pinned d44962997902). This
emits our marker JSON as their `*_specification.json` shape: panels with
2D vertex outlines + edges, placement, stitches list, panel_order — units in
centimeters (their convention), panel-local coordinates.

Verification, honest by construction (the ifcopenshell pattern):
  - ALWAYS: round-trip parse (this module's own reader) — panel names, vertex
    counts, and coordinates must survive write→read (gates CI).
  - WHEN AVAILABLE: pygarment's BasicPattern loads the spec. Measured reality:
    the PyPI wheel (probed 2026-07-19) ships only the DSL modules — the
    `pygarment.pattern` subpackage needs the REPO CHECKOUT. Absence is
    reported, never hidden.

Honest edges: v0.1 exports pattern GEOMETRY; stitch topology is emitted empty
(our markers declare symmetry pairs, not sewing order — roadmap), and the spec
shape is derived from the SHA-pinned digest + papers. Load one into the
GarmentCode GUI and file a gate-dispute if it fails.

Usage: python3 pipeline/garmentcode_export.py marker.json out_specification.json
Exit 0 = written + round-trip verified, 1 = mismatch.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any

Marker = dict[str, Any]

MM_TO_CM = 0.1


def write_spec(marker: Marker) -> dict[str, Any]:
    """Render the marker as a GarmentCode-style specification dict."""
    panels: dict[str, Any] = {}
    order = []
    for piece in marker["pieces"]:
        name = piece["name"]
        order.append(name)
        xs = [p[0] for p in piece["polygon"]]
        ys = [p[1] for p in piece["polygon"]]
        x0, y0 = min(xs), min(ys)
        verts = [[round((x - x0) * MM_TO_CM, 4), round((y - y0) * MM_TO_CM, 4)]
                 for x, y in piece["polygon"]]
        n = len(verts)
        panels[name] = {
            "translation": [round(x0 * MM_TO_CM, 4), round(y0 * MM_TO_CM, 4), 0.0],
            "rotation": [0.0, 0.0, 0.0],
            "vertices": verts,
            "edges": [{"endpoints": [i, (i + 1) % n]} for i in range(n)],
        }
    return {
        "pattern": {"panels": panels, "stitches": [], "panel_order": order},
        "properties": {"curvature_coords": "relative", "units_in_meter": 100,
                       "normalize_panel_translation": False},
        "parameters": {},
        "parameter_order": [],
        "provenance": {
            "generator": "design-anything pipeline/garmentcode_export.py",
            "source_marker": marker.get("name", "?"),
            "size": marker.get("size", "-"),
            "spec_shape_pinned_to": "maria-korosteleva/GarmentCode @ d44962997902",
            "note": "geometry only; stitch topology roadmap",
        },
    }


def round_trip_ok(marker: Marker, spec: dict[str, Any], tol: float = 0.001) -> list[str]:
    """Verify every piece survives write→read (names, counts, coordinates)."""
    problems = []
    panels = spec.get("pattern", {}).get("panels", {})
    if spec.get("pattern", {}).get("panel_order") != [p["name"] for p in marker["pieces"]]:
        problems.append("panel_order does not match piece order")
    if spec.get("properties", {}).get("units_in_meter") != 100:
        problems.append("units_in_meter must be 100 (centimeters)")
    for piece in marker["pieces"]:
        panel = panels.get(piece["name"])
        if panel is None:
            problems.append(f"{piece['name']}: missing panel")
            continue
        tx, ty, _ = panel["translation"]
        got = [[v[0] + tx, v[1] + ty] for v in panel["vertices"]]
        want = [[x * MM_TO_CM, y * MM_TO_CM] for x, y in piece["polygon"]]
        if len(got) != len(want) or any(abs(a - b) > tol
                                        for p, q in zip(got, want) for a, b in zip(p, q)):
            problems.append(f"{piece['name']}: vertices do not round-trip to cm")
        if len(panel["edges"]) != len(panel["vertices"]):
            problems.append(f"{piece['name']}: edge loop not closed")
    return problems


def pygarment_check(path: str) -> str:
    """Optional deep validation — skip-not-fail, absence reported honestly."""
    try:
        from pygarment.pattern.core import BasicPattern  # type: ignore
    except ImportError:
        return ("pygarment.pattern unavailable (PyPI wheel ships only the DSL; "
                "BasicPattern needs the repo checkout) — deep validation SKIPPED")
    pattern = BasicPattern(path)
    return (f"pygarment BasicPattern loaded: {len(pattern.pattern['panels'])} panels, "
            f"self-intersecting={pattern.is_self_intersecting()}")


def main() -> None:
    if len(sys.argv) < 3:
        print(__doc__)
        sys.exit(2)
    marker = json.loads(Path(sys.argv[1]).read_text())
    spec = write_spec(marker)
    Path(sys.argv[2]).write_text(json.dumps(spec, indent=2) + "\n")
    problems = round_trip_ok(marker, spec)
    if problems:
        print("garmentcode_export: ROUND-TRIP FAILED")
        for p in problems:
            print(f"  FAIL {p}")
        sys.exit(1)
    print(f"garmentcode_export: wrote {sys.argv[2]} "
          f"({len(marker['pieces'])} panels, round-trip verified)")
    print(f"  {pygarment_check(sys.argv[2])}")


if __name__ == "__main__":
    main()
