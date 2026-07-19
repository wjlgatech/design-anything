#!/usr/bin/env python3
"""ifc_export.py — emit a construction layout as IFC4 (SPF/STEP), the
30-year survivor format legally mandated for public BIM in several countries.

v0.1 emits the SEMANTIC model — spatial structure (project → site → building
→ storey → spaces), space areas as IfcElementQuantity, and doors with
OverallWidth — not 3D geometry representations (roadmap). BIM tools read the
structure; geometry solids come later.

Verification, honest by construction:
  - ALWAYS: round-trip parse (this module's own SPF subset reader) — space
    names, areas, and door widths must survive write→read (gates CI).
  - WHEN INSTALLED: ifcopenshell opens and schema-checks the file
    (skip-not-fail; absence is reported, never hidden).

Determinism: GlobalIds are content-hashed (IFC base64 of md5), never random —
the same layout always produces byte-identical IFC (drift-gateable).

Usage: python3 pipeline/ifc_export.py layout.json out.ifc
Exit 0 = written + round-trip verified, 1 = mismatch.
"""

from __future__ import annotations

import hashlib
import json
import re
import sys
from pathlib import Path
from typing import Any

Layout = dict[str, Any]

IFC64 = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz_$"


def guid(seed: str) -> str:
    """Deterministic 22-char IFC GlobalId from a content seed."""
    n = int.from_bytes(hashlib.md5(seed.encode()).digest()[:16], "big")
    chars = []
    for _ in range(22):
        chars.append(IFC64[n & 63])
        n >>= 6
    return "".join(chars)


def _area_m2(poly: list[list[float]]) -> float:
    s = 0.0
    for i in range(len(poly)):
        x0, y0 = poly[i]
        x1, y1 = poly[(i + 1) % len(poly)]
        s += x0 * y1 - x1 * y0
    return abs(s) / 2.0 / 1e6


def write_ifc(layout: Layout) -> str:
    """Render the layout as an IFC4 SPF string (semantic subset)."""
    name = layout.get("name", "layout")
    lines = [
        "ISO-10303-21;",
        "HEADER;",
        "FILE_DESCRIPTION(('design-anything semantic export'),'2;1');",
        f"FILE_NAME('{name}.ifc','2026-01-01T00:00:00',('design-anything'),"
        "('design-anything'),'','pipeline/ifc_export.py','');",
        "FILE_SCHEMA(('IFC4'));",
        "ENDSEC;",
        "DATA;",
    ]
    n = [0]

    def e(text: str) -> int:
        n[0] += 1
        lines.append(f"#{n[0]}={text}")
        return n[0]

    length = e("IFCSIUNIT(*,.LENGTHUNIT.,.MILLI.,.METRE.);")
    area_u = e("IFCSIUNIT(*,.AREAUNIT.,$,.SQUARE_METRE.);")
    units = e(f"IFCUNITASSIGNMENT((#{length},#{area_u}));")
    origin = e("IFCCARTESIANPOINT((0.,0.,0.));")
    axis = e(f"IFCAXIS2PLACEMENT3D(#{origin},$,$);")
    ctx = e(f"IFCGEOMETRICREPRESENTATIONCONTEXT($,'Model',3,1.E-5,#{axis},$);")
    project = e(f"IFCPROJECT('{guid(name + ':project')}',$,'{name}',$,$,$,$,(#{ctx}),#{units});")
    site = e(f"IFCSITE('{guid(name + ':site')}',$,'site',$,$,$,$,$,.ELEMENT.,$,$,$,$,$);")
    bldg = e(f"IFCBUILDING('{guid(name + ':building')}',$,'building',$,$,$,$,$,.ELEMENT.,$,$,$);")
    storey = e(f"IFCBUILDINGSTOREY('{guid(name + ':storey')}',$,'storey-0',$,$,$,$,$,.ELEMENT.,0.);")
    e(f"IFCRELAGGREGATES('{guid(name + ':p-s')}',$,$,$,#{project},(#{site}));")
    e(f"IFCRELAGGREGATES('{guid(name + ':s-b')}',$,$,$,#{site},(#{bldg}));")
    e(f"IFCRELAGGREGATES('{guid(name + ':b-st')}',$,$,$,#{bldg},(#{storey}));")

    space_ids = []
    for room in layout.get("rooms", []):
        rn, rtype = room["name"], room.get("type", "")
        sid = e(f"IFCSPACE('{guid(name + ':space:' + rn)}',$,'{rn}','{rtype}',$,$,$,$,"
                ".ELEMENT.,.INTERNAL.,$);")
        space_ids.append(sid)
        q = e(f"IFCQUANTITYAREA('GrossFloorArea',$,$,{_area_m2(room['polygon']):.4f},$);")
        eq = e(f"IFCELEMENTQUANTITY('{guid(name + ':qty:' + rn)}',$,'Qto_SpaceBaseQuantities',"
               f"$,$,(#{q}));")
        e(f"IFCRELDEFINESBYPROPERTIES('{guid(name + ':rdp:' + rn)}',$,$,$,(#{sid}),#{eq});")
    ids = ",".join(f"#{i}" for i in space_ids)
    e(f"IFCRELAGGREGATES('{guid(name + ':st-sp')}',$,$,$,#{storey},({ids}));")

    door_ids = []
    for i, o in enumerate(layout.get("openings", [])):
        label = f"{o.get('type', 'door')}:{'-'.join(o.get('between', []))}"
        did = e(f"IFCDOOR('{guid(name + ':door:' + str(i))}',$,'{label}',$,$,$,$,$,"
                f"2100.,{float(o.get('width', 0)):.1f},.DOOR.,$,$);")
        door_ids.append(did)
    if door_ids:
        ids = ",".join(f"#{i}" for i in door_ids)
        e(f"IFCRELCONTAINEDINSPATIALSTRUCTURE('{guid(name + ':doors')}',$,$,$,({ids}),#{storey});")

    lines += ["ENDSEC;", "END-ISO-10303-21;"]
    return "\n".join(lines) + "\n"


def read_ifc(text: str) -> dict[str, Any]:
    """Parse the emitted subset back: spaces {name: area}, door widths."""
    spaces: dict[str, float] = {}
    order = []
    for m in re.finditer(r"#\d+=IFCSPACE\('[^']*',\$,'([^']*)'", text):
        order.append(m.group(1))
    for i, m in enumerate(re.finditer(
            r"IFCQUANTITYAREA\('GrossFloorArea',\$,\$,([\d.]+)", text)):
        if i < len(order):
            spaces[order[i]] = float(m.group(1))
    doors = [float(m.group(1)) for m in
             re.finditer(r"IFCDOOR\([^)]*?,2100\.,([\d.]+),", text)]
    return {"spaces": spaces, "door_widths": doors,
            "schema_ok": "FILE_SCHEMA(('IFC4'))" in text and text.rstrip().endswith("END-ISO-10303-21;")}


def round_trip_ok(layout: Layout, ifc_text: str, tol: float = 0.01) -> list[str]:
    """Verify names, areas, and door widths survive write→read."""
    parsed = read_ifc(ifc_text)
    problems = []
    if not parsed["schema_ok"]:
        problems.append("not a well-formed IFC4 SPF envelope")
    for room in layout.get("rooms", []):
        got = parsed["spaces"].get(room["name"])
        if got is None:
            problems.append(f"space '{room['name']}' missing")
        elif abs(got - _area_m2(room["polygon"])) > tol:
            problems.append(f"space '{room['name']}': area {got} != {_area_m2(room['polygon']):.4f}")
    want = sorted(float(o.get("width", 0)) for o in layout.get("openings", []))
    if sorted(parsed["door_widths"]) != want:
        problems.append(f"door widths {sorted(parsed['door_widths'])} != {want}")
    return problems


def ifcopenshell_check(path: str) -> str:
    """Optional deep validation — skip-not-fail, absence reported honestly."""
    try:
        import ifcopenshell  # type: ignore
    except ImportError:
        return "ifcopenshell not installed — deep validation SKIPPED (round-trip only)"
    model = ifcopenshell.open(path)
    return (f"ifcopenshell {ifcopenshell.version}: schema {model.schema}, "
            f"{len(model.by_type('IfcSpace'))} spaces, "
            f"{len(model.by_type('IfcDoor'))} doors")


def main() -> None:
    if len(sys.argv) < 3:
        print(__doc__)
        sys.exit(2)
    layout = json.loads(Path(sys.argv[1]).read_text())
    ifc = write_ifc(layout)
    Path(sys.argv[2]).write_text(ifc)
    problems = round_trip_ok(layout, ifc)
    if problems:
        print("ifc_export: ROUND-TRIP FAILED")
        for p in problems:
            print(f"  FAIL {p}")
        sys.exit(1)
    print(f"ifc_export: wrote {sys.argv[2]} "
          f"({len(layout.get('rooms', []))} spaces, {len(layout.get('openings', []))} doors, "
          f"round-trip verified)")
    print(f"  {ifcopenshell_check(sys.argv[2])}")


if __name__ == "__main__":
    main()
