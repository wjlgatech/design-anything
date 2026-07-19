"""v0.13.0: the dogfood-born golden (pen holder) + the GarmentCode emitter."""

import importlib.util
import math
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "pipeline"))

import garmentcode_export  # noqa: E402
import ready_gate  # noqa: E402


def _load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


pen_gen = _load("pen_holder_generate", ROOT / "examples" / "pen-holder" / "generate.py")
apron_gen = _load("apron_gen_gc", ROOT / "examples" / "apron" / "generate.py")


# ---- golden #6: the dogfood-born pen holder ---------------------------------

def test_pen_holder_is_ready(tmp_path):
    stl = tmp_path / "pen.stl"
    pen_gen.write_stl(str(stl), pen_gen.pen_holder())
    report = ready_gate.run_gate(str(stl), (220.0, 220.0, 250.0), 0.4, pen_gen.WALL)
    assert report["ready"], report


def test_pen_holder_volume_matches_analytic(tmp_path):
    """Hex prism shell volume: outer prism - cavity prism (fan triangulation
    must close exactly, or signed volume drifts from the analytic value)."""
    stl = tmp_path / "pen.stl"
    pen_gen.write_stl(str(stl), pen_gen.pen_holder())
    hex_area = lambda r: 3 * math.sqrt(3) / 2 * r * r
    expected = (hex_area(pen_gen.R_OUT) * pen_gen.H
                - hex_area(pen_gen.R_OUT - pen_gen.WALL) * (pen_gen.H - pen_gen.BASE))
    vol = ready_gate.signed_volume(ready_gate.read_stl(str(stl)))
    assert abs(vol - expected) / expected < 1e-4, (vol, expected)


# ---- M12b: GarmentCode emitter ----------------------------------------------

def test_spec_round_trips_every_size():
    for size in apron_gen.SIZES:
        marker = apron_gen.apron(size)
        problems = garmentcode_export.round_trip_ok(
            marker, garmentcode_export.write_spec(marker))
        assert not problems, (size, problems)


def test_spec_carries_garmentcode_shape():
    spec = garmentcode_export.write_spec(apron_gen.apron("M"))
    assert set(spec["pattern"]) == {"panels", "stitches", "panel_order"}
    assert spec["properties"]["units_in_meter"] == 100  # centimeters
    body = spec["pattern"]["panels"]["body"]
    assert len(body["edges"]) == len(body["vertices"])  # closed loop
    assert all(e["endpoints"] for e in body["edges"])
    assert "d44962997902" in spec["provenance"]["spec_shape_pinned_to"]


def test_units_are_centimeters():
    marker = apron_gen.apron("M")
    spec = garmentcode_export.write_spec(marker)
    body_mm = next(p for p in marker["pieces"] if p["name"] == "body")
    width_mm = max(x for x, _ in body_mm["polygon"]) - min(x for x, _ in body_mm["polygon"])
    verts = spec["pattern"]["panels"]["body"]["vertices"]
    width_cm = max(v[0] for v in verts) - min(v[0] for v in verts)
    assert abs(width_cm - width_mm / 10) < 1e-6


def test_corrupt_spec_fails_round_trip():
    marker = apron_gen.apron("M")
    spec = garmentcode_export.write_spec(marker)
    del spec["pattern"]["panels"]["pocket"]
    assert any("pocket" in p for p in garmentcode_export.round_trip_ok(marker, spec))


def test_pygarment_absence_is_reported_not_hidden(tmp_path):
    p = tmp_path / "s.json"
    import json
    p.write_text(json.dumps(garmentcode_export.write_spec(apron_gen.apron("M"))))
    msg = garmentcode_export.pygarment_check(str(p))
    assert "SKIPPED" in msg or "pygarment" in msg
