#!/usr/bin/env python3
"""ready_gate.py — the machine-checkable definition of "3D-print ready".

Stdlib-only geometry, deterministic. A blueprint may not claim "ready" unless
this gate passes. No evidence => Not ready.

Checks (print target):
  G1 watertight     every directed edge is matched by exactly one reverse edge
                    (closed, 2-manifold, consistently wound)
  G2 outward        signed volume > 0 (normals point out; mesh is not inside-out)
  G3 bed-fit        bounding box fits the declared printer bed
  G4 min-feature    declared minimum feature (wall/base) >= nozzle_mm * 2

Usage:
  python3 pipeline/ready_gate.py model.stl --bed 220x220x250 --nozzle 0.4 \
      --min-feature 2.4 [--json]

Exit code 0 = READY, 1 = NOT READY (gates CI).
"""

from __future__ import annotations

import argparse
import struct
from typing import Any, Callable, Iterable

from gate import CheckResult, Gate, emit_report

Triangle = tuple[tuple[float, ...], tuple[float, ...], tuple[float, ...]]
Mesh = dict[str, Any]  # {"path": str, "tris": list[Triangle]}


def read_stl(path: str) -> list[Triangle]:
    """Parse binary or ASCII STL. Returns a list of triangles [(v0, v1, v2)]."""
    with open(path, "rb") as f:
        data = f.read()
    if data[:5] == b"solid" and b"facet" in data[:500]:
        return _read_ascii(data)
    return _read_binary(data)


def _read_binary(data: bytes) -> list[Triangle]:
    """Binary STL: 80-byte header, uint32 count, 50 bytes per facet."""
    (n,) = struct.unpack_from("<I", data, 80)
    tris = []
    off = 84
    for _ in range(n):
        vals = struct.unpack_from("<12f", data, off)
        tris.append((tuple(vals[3:6]), tuple(vals[6:9]), tuple(vals[9:12])))
        off += 50
    return tris


def _read_ascii(data: bytes) -> list[Triangle]:
    """ASCII STL: collect vertex triplets between facet markers."""
    verts: list[tuple[float, ...]] = []
    tris: list[Triangle] = []
    for line in data.decode("ascii", "replace").splitlines():
        parts = line.split()
        if parts[:1] == ["vertex"]:
            verts.append(tuple(float(x) for x in parts[1:4]))
            if len(verts) == 3:
                tris.append((verts[0], verts[1], verts[2]))
                verts = []
    return tris


def check_watertight(tris: list[Triangle]) -> tuple[bool, str]:
    """G1: each directed edge must be matched by exactly one reverse edge."""
    edges: dict[tuple, int] = {}
    for tri in tris:
        for i in range(3):
            e = (tri[i], tri[(i + 1) % 3])
            edges[e] = edges.get(e, 0) + 1
    bad = sum(1 for (a, b), c in edges.items() if c != 1 or edges.get((b, a), 0) != 1)
    return bad == 0, f"{bad} unmatched/duplicate directed edges" if bad else "closed 2-manifold"


def signed_volume(tris: list[Triangle]) -> float:
    """G2: sum of tetra volumes; positive iff consistently outward-wound."""
    v = 0.0
    for (x0, y0, z0), (x1, y1, z1), (x2, y2, z2) in tris:
        v += (x0 * (y1 * z2 - z1 * y2)
              - y0 * (x1 * z2 - z1 * x2)
              + z0 * (x1 * y2 - y1 * x2))
    return v / 6.0


def bounds(tris: list[Triangle]) -> tuple[float, float, float]:
    """Bounding-box extents (dx, dy, dz) of the mesh, in mm."""
    xs = [v[0] for t in tris for v in t]
    ys = [v[1] for t in tris for v in t]
    zs = [v[2] for t in tris for v in t]
    return (max(xs) - min(xs), max(ys) - min(ys), max(zs) - min(zs))


class PrintReadyGate(Gate):
    """Mesh gate: watertight, outward normals, bed fit, minimum feature."""

    disclaimer = ""  # honest edges live in the module docstring

    def __init__(self, bed: tuple[float, float, float], nozzle_mm: float,
                 min_feature_mm: float) -> None:
        self.bed = bed
        self.nozzle_mm = nozzle_mm
        self.min_feature_mm = min_feature_mm

    def checks(self) -> Iterable[tuple[str, Callable[[Mesh], CheckResult]]]:
        return [
            ("G1_watertight", self.check_watertight),
            ("G2_outward_normals", self.check_outward_normals),
            ("G3_bed_fit", self.check_bed_fit),
            ("G4_min_feature", self.check_min_feature),
        ]

    def subject_name(self, subject: Mesh) -> str:
        return subject["path"]

    def extra_report_fields(self, subject: Mesh) -> dict[str, Any]:
        return {"triangles": len(subject["tris"])}

    def run(self, subject: Any) -> dict[str, Any]:
        """Parse the STL once; an empty mesh short-circuits as G0."""
        if isinstance(subject, str):
            subject = {"path": subject, "tris": read_stl(subject)}
        if not subject["tris"]:
            return {"file": subject["path"], "triangles": 0,
                    "gates": {"G0_nonempty": {"pass": False, "detail": "no triangles"}},
                    "ready": False, "disclaimer": self.disclaimer}
        return super().run(subject)

    def check_watertight(self, subject: Mesh) -> CheckResult:
        """G1: closed 2-manifold with consistent winding."""
        ok, detail = check_watertight(subject["tris"])
        return CheckResult(ok, detail)

    def check_outward_normals(self, subject: Mesh) -> CheckResult:
        """G2: positive signed volume means the mesh is not inside-out."""
        vol = signed_volume(subject["tris"])
        return CheckResult(vol > 0, f"signed volume {vol:.1f} mm^3")

    def check_bed_fit(self, subject: Mesh) -> CheckResult:
        """G3: bounding box fits the declared printer bed (any orientation axis-sorted)."""
        dims = bounds(subject["tris"])
        fits = all(d <= b for d, b in zip(sorted(dims), sorted(self.bed)))
        return CheckResult(
            fits, f"model {tuple(round(d, 1) for d in dims)} mm vs bed {self.bed} mm")

    def check_min_feature(self, subject: Mesh) -> CheckResult:
        """G4: smallest declared feature must be at least two nozzle widths."""
        ok = self.min_feature_mm >= self.nozzle_mm * 2
        return CheckResult(
            ok, f"min feature {self.min_feature_mm} mm vs 2x nozzle {self.nozzle_mm * 2} mm")


def run_gate(path: str, bed: tuple[float, float, float], nozzle_mm: float,
             min_feature_mm: float) -> dict[str, Any]:
    """Module-level entry point (kept stable for tests, skills, and evals)."""
    return PrintReadyGate(bed, nozzle_mm, min_feature_mm).run(path)


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("stl")
    ap.add_argument("--bed", default="220x220x250", help="printer bed WxDxH in mm")
    ap.add_argument("--nozzle", type=float, default=0.4, help="nozzle diameter mm")
    ap.add_argument("--min-feature", type=float, required=True,
                    help="smallest declared feature (wall/base) in mm")
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args()

    bed = tuple(float(x) for x in args.bed.lower().split("x"))
    emit_report(run_gate(args.stl, bed, args.nozzle, args.min_feature), as_json=args.json)


if __name__ == "__main__":
    main()
