"""The scene gate must pass the golden arena and fail known-bad scenes."""

import importlib.util
import json
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "pipeline"))

import scene_gate  # noqa: E402


def _load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


arena_gen = _load("arena_generate", ROOT / "examples" / "arena" / "generate.py")
TABLES = yaml.safe_load((ROOT / "data" / "scene.yml").read_text())


def _gate(tmp_path, gltf, target="pc"):
    p = tmp_path / "scene.gltf"
    p.write_text(json.dumps(gltf))
    return scene_gate.run_gate(str(p), TABLES, target)


def test_golden_arena_is_ready(tmp_path):
    report = _gate(tmp_path, arena_gen.arena())
    assert report["ready"], report


def test_triangle_count_matches_generator(tmp_path):
    gltf = arena_gen.arena()
    # ground (2) + 4 wall boxes (12 each) = 50 triangles, computed independently
    assert scene_gate.triangle_count(gltf) == 50


def test_over_budget_fails(tmp_path):
    report = _gate(tmp_path, arena_gen.arena(), target="mobile")
    assert report["gates"]["S2_poly_budget"]["pass"]  # 50 tris fits mobile too
    gltf = arena_gen.arena()
    gltf["accessors"][1]["count"] = 100000 * 3 * 4  # fake a huge index count
    gltf["bufferViews"][1]["byteLength"] = 100000 * 3 * 4 * 2
    gltf["buffers"][0]["byteLength"] = 10**9
    report = _gate(tmp_path, gltf, target="mobile")
    assert not report["gates"]["S2_poly_budget"]["pass"]


def test_wrong_units_fail_scale(tmp_path):
    gltf = arena_gen.arena()
    gltf["asset"]["extras"]["units"] = "centimeters"
    report = _gate(tmp_path, gltf)
    assert not report["gates"]["S3_true_scale"]["pass"]


def test_units_bug_extent_fails(tmp_path):
    gltf = arena_gen.arena()
    acc = gltf["accessors"][0]
    acc["min"] = [v * 100 for v in acc["min"]]  # a "40m" arena that is 4km
    acc["max"] = [v * 100 for v in acc["max"]]
    report = _gate(tmp_path, gltf)
    assert not report["gates"]["S3_true_scale"]["pass"]


def test_missing_collision_fails(tmp_path):
    gltf = arena_gen.arena()
    gltf["nodes"] = [n for n in gltf["nodes"] if not n["name"].endswith("_collision")]
    report = _gate(tmp_path, gltf)
    assert not report["gates"]["S4_collision"]["pass"]


def test_corrupt_buffer_fails_structure(tmp_path):
    gltf = arena_gen.arena()
    gltf["buffers"][0]["byteLength"] += 1  # declared length no longer matches
    report = _gate(tmp_path, gltf)
    assert not report["gates"]["S1_structure"]["pass"]


def test_unknown_target_is_not_measured_therefore_fails(tmp_path):
    report = _gate(tmp_path, arena_gen.arena(), target="console9000")
    assert not report["gates"]["S2_poly_budget"]["pass"]


def test_report_carries_disclaimer(tmp_path):
    report = _gate(tmp_path, arena_gen.arena())
    assert "engine" in report["disclaimer"]
