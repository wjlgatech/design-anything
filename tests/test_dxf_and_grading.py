"""M12: the size run must gate per size; the DXF export must round-trip.

Grading discipline (ASTM D5585 lineage): a pattern that can't grade coherently
is a demo. DXF discipline: an export verified only by claim is not an export.
"""

import importlib.util
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "pipeline"))

import dxf_aama  # noqa: E402
import pattern_gate  # noqa: E402


def _load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


apron_gen = _load("apron_generate_m12", ROOT / "examples" / "apron" / "generate.py")
TABLES = yaml.safe_load((ROOT / "data" / "garment.yml").read_text())


# ---- grading ----------------------------------------------------------------

def test_every_size_in_the_run_passes_the_gate():
    for size in apron_gen.SIZES:
        report = pattern_gate.run_gate(apron_gen.apron(size), TABLES)
        assert report["ready"], (size, report)


def test_grading_is_monotonic():
    dims = {s: apron_gen.SIZES[s] for s in ("S", "M", "L")}
    for key in ("body_w", "body_l", "tie_l", "strap_l"):
        assert dims["S"][key] < dims["M"][key] < dims["L"][key], key


def test_mismatched_symmetric_pieces_fail_seam_pairs():
    marker = apron_gen.apron("M")
    tie = next(p for p in marker["pieces"] if p["name"] == "waist_tie_right")
    tie["polygon"][2][1] -= 40  # one tie graded, its mirror forgotten
    tie["polygon"][3][1] -= 40
    report = pattern_gate.run_gate(marker, TABLES)
    assert not report["gates"]["F6_seam_pairs"]["pass"]


def test_missing_pair_piece_fails_not_fakes():
    marker = apron_gen.apron("M")
    marker["pieces"] = [p for p in marker["pieces"] if p["name"] != "waist_tie_right"]
    report = pattern_gate.run_gate(marker, TABLES)
    assert not report["gates"]["F6_seam_pairs"]["pass"]
    assert "not measured" in report["gates"]["F6_seam_pairs"]["detail"]


def test_no_declared_pairs_is_a_vacuous_pass_with_honest_detail():
    marker = apron_gen.apron("M")
    del marker["seam_pairs"]
    report = pattern_gate.run_gate(marker, TABLES)
    assert report["gates"]["F6_seam_pairs"]["pass"]
    assert "0 seam pairs declared" in report["gates"]["F6_seam_pairs"]["detail"]


# ---- DXF-AAMA export --------------------------------------------------------

def test_dxf_round_trips_every_size():
    for size in apron_gen.SIZES:
        marker = apron_gen.apron(size)
        problems = dxf_aama.round_trip_ok(marker, dxf_aama.write_dxf(marker))
        assert not problems, (size, problems)


def test_dxf_carries_aama_conventions():
    marker = apron_gen.apron("M")
    dxf = dxf_aama.write_dxf(marker)
    assert "$INSUNITS" in dxf              # millimeters declared
    assert dxf.count("BLOCK") >= len(marker["pieces"])  # one block per piece
    parsed = dxf_aama.read_dxf(dxf)
    assert set(parsed) == {p["name"] for p in marker["pieces"]}
    assert all(v["grain"] for v in parsed.values())     # layer-7 grain lines
    assert all("size M" in v["label"] for v in parsed.values())


def test_corrupted_dxf_fails_round_trip():
    marker = apron_gen.apron("M")
    dxf = dxf_aama.write_dxf(marker)
    truncated = dxf[: dxf.index("pocket")]  # drop the last piece
    problems = dxf_aama.round_trip_ok(marker, truncated)
    assert any("pocket" in p for p in problems)
