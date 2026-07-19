#!/usr/bin/env python3
"""generate.py — golden example: text brief -> parametric game scene -> glTF.

Brief: "a medieval courtyard arena, 40m square with 5m perimeter walls,
true-to-scale in meters, with collision geometry, within a PC poly budget."

Same principle as the planter, the studio flat, and the apron: emit the
COMPOSITION. This file is the level blueprint; arena.gltf is the compiled
artifact; pipeline/scene_gate.py is the acceptance test.

Usage: python3 examples/arena/generate.py [out.gltf]
"""

from __future__ import annotations

import base64
import json
import struct
import sys

# ---- the parametric brief (meters, +Y up) -----------------------------------
SIZE = 40.0      # courtyard side
WALL_H = 5.0     # perimeter wall height
WALL_T = 0.5     # wall thickness
TARGET = "pc"    # declared platform budget (data/scene.yml)
# ------------------------------------------------------------------------------

Vec = tuple[float, float, float]


def box(x0: float, y0: float, z0: float, x1: float, y1: float, z1: float,
        verts: list[Vec], tris: list[tuple[int, int, int]]) -> None:
    """Append an axis-aligned box (8 verts, 12 tris) to the geometry lists."""
    base = len(verts)
    corners = [(x, y, z) for x in (x0, x1) for y in (y0, y1) for z in (z0, z1)]
    verts.extend(corners)
    # 12 triangles over the 6 faces (consistent local winding)
    faces = [(0, 1, 3, 2), (4, 6, 7, 5), (0, 4, 5, 1),
             (2, 3, 7, 6), (0, 2, 6, 4), (1, 5, 7, 3)]
    for a, b, c, d in faces:
        tris.append((base + a, base + b, base + c))
        tris.append((base + a, base + c, base + d))


def arena() -> dict:
    """The courtyard arena as a valid glTF 2.0 dict with an embedded buffer."""
    verts: list[Vec] = [(0, 0, 0), (SIZE, 0, 0), (SIZE, 0, SIZE), (0, 0, SIZE)]
    tris: list[tuple[int, int, int]] = [(0, 1, 2), (0, 2, 3)]  # ground plane
    box(0, 0, 0, SIZE, WALL_H, WALL_T, verts, tris)                    # north wall
    box(0, 0, SIZE - WALL_T, SIZE, WALL_H, SIZE, verts, tris)          # south wall
    box(0, 0, 0, WALL_T, WALL_H, SIZE, verts, tris)                    # west wall
    box(SIZE - WALL_T, 0, 0, SIZE, WALL_H, SIZE, verts, tris)          # east wall

    pos_bytes = b"".join(struct.pack("<3f", *v) for v in verts)
    idx = [i for t in tris for i in t]
    idx_bytes = b"".join(struct.pack("<H", i) for i in idx)
    blob = pos_bytes + idx_bytes

    mins = [min(v[i] for v in verts) for i in range(3)]
    maxs = [max(v[i] for v in verts) for i in range(3)]

    return {
        "asset": {"version": "2.0",
                  "generator": "design-anything examples/arena",
                  "extras": {"units": "meters", "target": TARGET}},
        "buffers": [{
            "uri": "data:application/octet-stream;base64," +
                   base64.b64encode(blob).decode("ascii"),
            "byteLength": len(blob)}],
        "bufferViews": [
            {"buffer": 0, "byteOffset": 0, "byteLength": len(pos_bytes)},
            {"buffer": 0, "byteOffset": len(pos_bytes), "byteLength": len(idx_bytes)},
        ],
        "accessors": [
            {"bufferView": 0, "componentType": 5126, "count": len(verts),
             "type": "VEC3", "min": mins, "max": maxs},
            {"bufferView": 1, "componentType": 5123, "count": len(idx),
             "type": "SCALAR"},
        ],
        "meshes": [{"name": "arena_mesh",
                    "primitives": [{"attributes": {"POSITION": 0}, "indices": 1}]}],
        "nodes": [
            {"name": "arena", "mesh": 0},
            {"name": "arena_collision", "mesh": 0,
             "extras": {"role": "collision proxy (same mesh at this LOD)"}},
        ],
        "scenes": [{"name": "courtyard_arena", "nodes": [0, 1]}],
        "scene": 0,
    }


if __name__ == "__main__":
    out = sys.argv[1] if len(sys.argv) > 1 else "arena.gltf"
    gltf = arena()
    with open(out, "w") as f:
        json.dump(gltf, f, indent=1)
    tris = gltf["accessors"][1]["count"] // 3
    print(f"wrote {out}: {tris} triangles, {SIZE}x{SIZE}m courtyard, "
          f"{WALL_H}m walls, target {TARGET}")
