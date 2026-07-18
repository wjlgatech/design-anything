"""The pattern gate must pass the golden apron and fail known-bad markers."""

import importlib.util
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "pipeline"))

import pattern_gate  # noqa: E402


def _load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


apron_gen = _load("apron_generate", ROOT / "examples" / "apron" / "generate.py")
TABLES = yaml.safe_load((ROOT / "data" / "garment.yml").read_text())


def golden():
    return apron_gen.apron()


def test_golden_apron_is_ready():
    report = pattern_gate.run_gate(golden(), TABLES)
    assert report["ready"], report


def test_thin_seam_allowance_fails():
    marker = golden()
    marker["seam_allowance"] = 8
    report = pattern_gate.run_gate(marker, TABLES)
    assert not report["gates"]["F3_seam_allowance"]["pass"]


def test_piece_beyond_fabric_width_fails():
    marker = golden()
    marker["fabric"]["width"] = 1100
    report = pattern_gate.run_gate(marker, TABLES)
    assert not report["gates"]["F2_fabric_fit"]["pass"]


def test_overlapping_pieces_fail():
    marker = golden()
    pocket = next(p for p in marker["pieces"] if p["name"] == "pocket")
    pocket["polygon"] = [[100, 100], [500, 100], [500, 350], [100, 350]]  # on the body
    report = pattern_gate.run_gate(marker, TABLES)
    assert not report["gates"]["F2_fabric_fit"]["pass"]


def test_wasteful_marker_fails_efficiency():
    marker = golden()
    strap = next(p for p in marker["pieces"] if p["name"] == "neck_strap")
    strap["polygon"] = [[x, y + 2000] for x, y in strap["polygon"]]  # stretch the marker
    report = pattern_gate.run_gate(marker, TABLES)
    assert not report["gates"]["F4_marker_efficiency"]["pass"]


def test_short_waist_ties_fail_fit():
    marker = golden()
    marker["fit"]["waist_tie_total"] = 1200
    report = pattern_gate.run_gate(marker, TABLES)
    assert not report["gates"]["F5_human_fit"]["pass"]


def test_unknown_garment_type_is_not_measured_therefore_fails():
    marker = golden()
    marker["garment_type"] = "cape"
    report = pattern_gate.run_gate(marker, TABLES)
    assert not report["gates"]["F5_human_fit"]["pass"]


def test_undeclared_grain_fails():
    marker = golden()
    del marker["pieces"][0]["grain_angle_deg"]
    report = pattern_gate.run_gate(marker, TABLES)
    assert not report["gates"]["F1_pieces"]["pass"]


def test_report_carries_disclaimer():
    report = pattern_gate.run_gate(golden(), TABLES)
    assert "muslin" in report["disclaimer"]
