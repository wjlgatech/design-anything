#!/usr/bin/env python3
"""scene_gate.py — the machine-checkable definition of "game/sim ready" (v0.1).

Validates a glTF 2.0 scene (.gltf JSON with embedded buffers) against
data/scene.yml. The tables ARE the gate; no evidence => Not ready.

Checks:
  S1 structure   asset.version 2.0; buffers decode to their declared
                 byteLength; accessors fit their bufferViews; index counts
                 divide by 3
  S2 budget      total triangles <= the declared target platform's budget
  S3 true-scale  units declared as meters (asset.extras.units) and the scene
                 bounding box (from POSITION accessor min/max) within sanity
                 extents — a wrongly-scaled world poisons everything downstream
  S4 collision   at least one node carries the collision marker suffix

Usage: python3 pipeline/scene_gate.py scene.gltf [--target pc|mobile] [--json]
Exit 0 = READY, 1 = NOT READY (gates CI).

Honest edges: v0.1 validates structure, budget, scale, and collision presence —
not materials/textures, animation, draw calls, lightmaps, or engine import.
A pass means the scene is dimensionally sane and playable-shaped; art direction
and performance profiling live in the engine.
"""

from __future__ import annotations

import base64
import json
import struct
import sys
from pathlib import Path
from typing import Any, Callable, Iterable

import yaml

from gate import CheckResult, Gate, emit_report

ROOT = Path(__file__).resolve().parents[1]
TABLES_PATH = ROOT / "data" / "scene.yml"

Scene = dict[str, Any]  # {"path": str, "gltf": dict, "buffers": list[bytes]}

COMPONENT_BYTES = {5120: 1, 5121: 1, 5122: 2, 5123: 2, 5125: 4, 5126: 4}
TYPE_COMPONENTS = {"SCALAR": 1, "VEC2": 2, "VEC3": 3, "VEC4": 4, "MAT4": 16}


def load_scene(path: str) -> Scene:
    """Parse a .gltf file and decode its embedded (data-URI) buffers."""
    gltf = json.loads(Path(path).read_text())
    buffers = []
    for buf in gltf.get("buffers", []):
        uri = buf.get("uri", "")
        if uri.startswith("data:"):
            buffers.append(base64.b64decode(uri.split(",", 1)[1]))
        else:
            ext = Path(path).parent / uri
            buffers.append(ext.read_bytes() if ext.exists() else b"")
    return {"path": path, "gltf": gltf, "buffers": buffers}


def triangle_count(gltf: dict[str, Any]) -> int:
    """Total triangles across all mesh primitives (indexed or raw)."""
    accessors = gltf.get("accessors", [])
    total = 0
    for mesh in gltf.get("meshes", []):
        for prim in mesh.get("primitives", []):
            if "indices" in prim:
                total += accessors[prim["indices"]]["count"] // 3
            elif "POSITION" in prim.get("attributes", {}):
                total += accessors[prim["attributes"]["POSITION"]]["count"] // 3
    return total


class SceneGate(Gate):
    """glTF scene gate: structure, poly budget, true scale, collision present."""

    disclaimer = "structure/budget/scale/collision gate; materials, perf, and art direction live in the engine"

    def __init__(self, tables: dict[str, Any], target: str = "pc") -> None:
        self.tables = tables
        self.target = target

    def checks(self) -> Iterable[tuple[str, Callable[[Scene], CheckResult]]]:
        return [
            ("S1_structure", self.check_structure),
            ("S2_poly_budget", self.check_poly_budget),
            ("S3_true_scale", self.check_true_scale),
            ("S4_collision", self.check_collision),
        ]

    def subject_name(self, subject: Scene) -> str:
        return subject["path"]

    def check_structure(self, subject: Scene) -> CheckResult:
        """S1: version, buffer byte-lengths, accessor/bufferView consistency."""
        gltf, buffers = subject["gltf"], subject["buffers"]
        problems = []
        if gltf.get("asset", {}).get("version") != "2.0":
            problems.append("asset.version is not 2.0")
        for i, buf in enumerate(gltf.get("buffers", [])):
            if len(buffers[i]) != buf.get("byteLength", -1):
                problems.append(f"buffer[{i}]: decoded {len(buffers[i])}B != declared "
                                f"{buf.get('byteLength')}B")
        views = gltf.get("bufferViews", [])
        for i, acc in enumerate(gltf.get("accessors", [])):
            view = views[acc["bufferView"]]
            need = (acc["count"] * TYPE_COMPONENTS[acc["type"]]
                    * COMPONENT_BYTES[acc["componentType"]])
            if acc.get("byteOffset", 0) + need > view["byteLength"]:
                problems.append(f"accessor[{i}]: overruns its bufferView")
            if acc["type"] == "SCALAR" and acc["count"] % 3 != 0:
                problems.append(f"accessor[{i}]: index count {acc['count']} not divisible by 3")
        return CheckResult.from_problems(
            problems, f"glTF 2.0, {len(buffers)} buffer(s), accessors consistent")

    def check_poly_budget(self, subject: Scene) -> CheckResult:
        """S2: triangle total within the declared target's budget."""
        budget = self.tables["budgets"].get(self.target)
        if budget is None:
            return CheckResult(False, f"unknown target '{self.target}' "
                                      "(no budget table => not measured => fail)")
        tris = triangle_count(subject["gltf"])
        return CheckResult(tris <= budget["max_triangles"],
                           f"{tris} triangles vs {self.target} budget "
                           f"{budget['max_triangles']}")

    def check_true_scale(self, subject: Scene) -> CheckResult:
        """S3: meters declared; scene bbox within human-plausible extents."""
        gltf = subject["gltf"]
        problems = []
        units = gltf.get("asset", {}).get("extras", {}).get("units")
        required = self.tables["units_required"]
        if units != required:
            problems.append(f"units '{units}' declared; '{required}' required")
        lo, hi = [], []
        for acc in gltf.get("accessors", []):
            if acc["type"] == "VEC3" and "min" in acc and "max" in acc:
                lo.append(acc["min"])
                hi.append(acc["max"])
        if not lo:
            problems.append("no POSITION accessor with min/max — extent not measured => fail")
        else:
            extent = max(max(h) - min(l) for l, h in
                         [(list(map(min, zip(*lo))), list(map(max, zip(*hi))))])
            e_min = self.tables["scale_sanity"]["min_extent_m"]["value"]
            e_max = self.tables["scale_sanity"]["max_extent_m"]["value"]
            if not e_min <= extent <= e_max:
                problems.append(f"scene extent {extent:.1f}m outside sanity "
                                f"[{e_min}, {e_max}]m — units bug")
            else:
                return CheckResult(not problems,
                                   "; ".join(problems) or
                                   f"meters declared, extent {extent:.1f}m sane")
        return CheckResult.from_problems(problems, "scale sane")

    def check_collision(self, subject: Scene) -> CheckResult:
        """S4: at least one collision-marked node exists."""
        if not self.tables["collision"]["required"]:
            return CheckResult(True, "collision not required by table")
        marker = self.tables["collision"]["marker"]
        hits = [n.get("name", "") for n in subject["gltf"].get("nodes", [])
                if n.get("name", "").endswith(marker)]
        return CheckResult(bool(hits),
                           f"collision nodes: {hits}" if hits
                           else f"no node named *{marker} — scene is not playable")


def run_gate(path: str, tables: dict[str, Any], target: str = "pc") -> dict[str, Any]:
    """Module-level entry point (kept stable for tests, skills, and evals)."""
    return SceneGate(tables, target).run(load_scene(path))


def main() -> None:
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    if not args:
        print(__doc__)
        sys.exit(2)
    target = sys.argv[sys.argv.index("--target") + 1] if "--target" in sys.argv else "pc"
    tables = yaml.safe_load(TABLES_PATH.read_text())
    emit_report(run_gate(args[0], tables, target), as_json="--json" in sys.argv)


if __name__ == "__main__":
    main()
