"""The ready gate must pass the golden example and fail broken meshes.

Maker != checker: the generator (examples/) and the gate (pipeline/) are
independent; these tests hold them against each other and against analytic
ground truth.
"""

import struct
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "pipeline"))
sys.path.insert(0, str(ROOT / "examples" / "planter"))

import generate  # noqa: E402
import ready_gate  # noqa: E402

BED = (220.0, 220.0, 250.0)


def _stl(tmp_path, tris, name="m.stl"):
    p = tmp_path / name
    generate.write_stl(str(p), tris)
    return str(p)


def test_golden_planter_is_ready(tmp_path):
    tris = generate.planter(generate.W, generate.D, generate.H, generate.WALL, generate.BASE)
    report = ready_gate.run_gate(_stl(tmp_path, tris), BED, 0.4, generate.WALL)
    assert report["ready"], report


def test_volume_matches_analytic_ground_truth(tmp_path):
    w, d, h, t, b = 120.0, 80.0, 60.0, 3.0, 4.0
    tris = generate.planter(w, d, h, t, b)
    expected = w * d * h - (w - 2 * t) * (d - 2 * t) * (h - b)
    vol = ready_gate.signed_volume(ready_gate.read_stl(_stl(tmp_path, tris)))
    assert abs(vol - expected) < 1e-3


def test_hole_fails_watertight(tmp_path):
    tris = generate.planter(generate.W, generate.D, generate.H, generate.WALL, generate.BASE)
    report = ready_gate.run_gate(_stl(tmp_path, tris[1:]), BED, 0.4, generate.WALL)
    assert not report["gates"]["G1_watertight"]["pass"]
    assert not report["ready"]


def test_inside_out_fails_normals(tmp_path):
    tris = [(a, c, b) for a, b, c in
            generate.planter(generate.W, generate.D, generate.H, generate.WALL, generate.BASE)]
    report = ready_gate.run_gate(_stl(tmp_path, tris), BED, 0.4, generate.WALL)
    assert not report["gates"]["G2_outward_normals"]["pass"]


def test_oversize_fails_bed_fit(tmp_path):
    tris = generate.planter(300.0, 80.0, 60.0, 3.0, 4.0)
    report = ready_gate.run_gate(_stl(tmp_path, tris), BED, 0.4, 3.0)
    assert not report["gates"]["G3_bed_fit"]["pass"]


def test_thin_wall_fails_min_feature(tmp_path):
    tris = generate.planter(generate.W, generate.D, generate.H, 0.5, generate.BASE)
    report = ready_gate.run_gate(_stl(tmp_path, tris), BED, 0.4, 0.5)
    assert not report["gates"]["G4_min_feature"]["pass"]


def test_ascii_stl_parses(tmp_path):
    p = tmp_path / "a.stl"
    p.write_text(
        "solid t\n facet normal 0 0 0\n  outer loop\n"
        "   vertex 0 0 0\n   vertex 1 0 0\n   vertex 0 1 0\n"
        "  endloop\n endfacet\nendsolid t\n")
    assert len(ready_gate.read_stl(str(p))) == 1
