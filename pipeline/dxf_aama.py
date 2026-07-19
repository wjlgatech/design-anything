#!/usr/bin/env python3
"""dxf_aama.py — emit a marker as DXF-AAMA/ASTM-style pattern exchange.

Why this exists: the ASTM D6673 standard was formally withdrawn in 2019, yet
every production pattern CAD still imports it — an AI pattern generator that
can't emit it is not production-real (research/last30years + the garment
digest). This writer follows the AAMA conventions that matter for import:

  - one BLOCK per pattern piece, INSERTed into model space
  - piece boundary as a closed POLYLINE on layer 1 (the AAMA cut line)
  - grain line as a LINE on layer 7
  - piece annotation as TEXT on layer 15 (name, size)
  - millimeters declared via $INSUNITS = 4

`read_dxf()` parses the same subset back so the export is verified by
round-trip (tests/test_dxf_and_grading.py), never by claim.

Usage: python3 pipeline/dxf_aama.py marker.json out.dxf
Exit 0 = written + round-trip verified, 1 = round-trip mismatch.

Honest edges: this is the load-bearing AAMA subset (boundary/grain/annotation),
not the full spec (no internal drill holes, notches, or seam-allowance dual
boundaries yet). Import it into your CAD and file a gate-dispute if it fails.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any, Iterator

Marker = dict[str, Any]


def _grain_line(polygon: list[list[float]], angle_deg: float) -> tuple[float, float, float, float]:
    """A grain line through the piece's bbox center, 60% of its extent."""
    xs = [p[0] for p in polygon]
    ys = [p[1] for p in polygon]
    cx, cy = (min(xs) + max(xs)) / 2, (min(ys) + max(ys)) / 2
    if angle_deg == 90:
        half = 0.3 * (max(xs) - min(xs))
        return cx - half, cy, cx + half, cy
    half = 0.3 * (max(ys) - min(ys))
    return cx, cy - half, cx, cy + half


def write_dxf(marker: Marker) -> str:
    """Render the marker as AAMA-style ASCII DXF (R12 subset)."""
    def g(code: int, value: Any) -> str:
        return f"{code}\n{value}\n"

    out = [g(0, "SECTION"), g(2, "HEADER"),
           g(9, "$INSUNITS"), g(70, 4),  # 4 = millimeters
           g(0, "ENDSEC"), g(0, "SECTION"), g(2, "BLOCKS")]

    for piece in marker["pieces"]:
        name = piece["name"]
        out += [g(0, "BLOCK"), g(8, 0), g(2, name), g(70, 0),
                g(10, 0.0), g(20, 0.0), g(30, 0.0)]
        # boundary: closed polyline on layer 1 (AAMA cut line)
        out += [g(0, "POLYLINE"), g(8, 1), g(66, 1), g(70, 1)]
        for x, y in piece["polygon"]:
            out += [g(0, "VERTEX"), g(8, 1), g(10, float(x)), g(20, float(y)), g(30, 0.0)]
        out += [g(0, "SEQEND")]
        # grain line on layer 7
        x0, y0, x1, y1 = _grain_line(piece["polygon"], piece.get("grain_angle_deg", 0))
        out += [g(0, "LINE"), g(8, 7),
                g(10, x0), g(20, y0), g(30, 0.0), g(11, x1), g(21, y1), g(31, 0.0)]
        # annotation on layer 15
        label = f"{name} / {marker.get('name', '')} / size {marker.get('size', '-')}"
        out += [g(0, "TEXT"), g(8, 15), g(10, x0), g(20, y0), g(30, 0.0),
                g(40, 10.0), g(1, label)]
        out += [g(0, "ENDBLK")]

    out += [g(0, "ENDSEC"), g(0, "SECTION"), g(2, "ENTITIES")]
    for piece in marker["pieces"]:
        out += [g(0, "INSERT"), g(8, 0), g(2, piece["name"]),
                g(10, 0.0), g(20, 0.0), g(30, 0.0)]
    out += [g(0, "ENDSEC"), g(0, "EOF")]
    return "".join(out)


def _groups(text: str) -> Iterator[tuple[int, str]]:
    """Iterate DXF (group-code, value) pairs."""
    lines = text.splitlines()
    for i in range(0, len(lines) - 1, 2):
        yield int(lines[i].strip()), lines[i + 1].strip()


def read_dxf(text: str) -> dict[str, dict[str, Any]]:
    """Parse the AAMA subset back: {piece: {polygon, grain, label}}."""
    pieces: dict[str, dict[str, Any]] = {}
    current: dict[str, Any] | None = None
    entity = ""
    vx: float | None = None
    for code, value in _groups(text):
        if code == 0:
            entity = value
            if value == "ENDBLK":
                current = None
            continue
        if entity == "BLOCK" and code == 2:
            current = {"name": value, "polygon": [], "grain": False, "label": ""}
            pieces[value] = current
        elif current is not None and entity == "VERTEX":
            if code == 10:
                vx = float(value)
            elif code == 20 and vx is not None:
                current["polygon"].append([vx, float(value)])
                vx = None
        elif current is not None and entity == "LINE" and code == 8 and value == "7":
            current["grain"] = True
        elif current is not None and entity == "TEXT" and code == 1:
            current["label"] = value
    return pieces


def round_trip_ok(marker: Marker, dxf_text: str, tol: float = 0.01) -> list[str]:
    """Verify the DXF carries every piece faithfully; returns problems."""
    parsed = read_dxf(dxf_text)
    problems = []
    for piece in marker["pieces"]:
        got = parsed.get(piece["name"])
        if got is None:
            problems.append(f"{piece['name']}: missing from DXF")
            continue
        want = [[float(x), float(y)] for x, y in piece["polygon"]]
        if len(got["polygon"]) != len(want) or any(
                abs(a - b) > tol for p, q in zip(got["polygon"], want) for a, b in zip(p, q)):
            problems.append(f"{piece['name']}: boundary vertices differ")
        if not got["grain"]:
            problems.append(f"{piece['name']}: no grain line (layer 7)")
        if not got["label"]:
            problems.append(f"{piece['name']}: no annotation (layer 15)")
    return problems


def main() -> None:
    if len(sys.argv) < 3:
        print(__doc__)
        sys.exit(2)
    marker = json.loads(Path(sys.argv[1]).read_text())
    dxf = write_dxf(marker)
    Path(sys.argv[2]).write_text(dxf)
    problems = round_trip_ok(marker, dxf)
    if problems:
        print("dxf_aama: ROUND-TRIP FAILED")
        for p in problems:
            print(f"  FAIL {p}")
        sys.exit(1)
    print(f"dxf_aama: wrote {sys.argv[2]} ({len(marker['pieces'])} pieces, "
          f"round-trip verified)")


if __name__ == "__main__":
    main()
