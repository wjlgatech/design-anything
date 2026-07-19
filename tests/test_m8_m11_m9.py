"""M8 (IFC export), M11 (body-fit gate), M9 (knowledge graph) — the gates."""

import importlib.util
import json
import subprocess
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "pipeline"))

import bodyfit_gate  # noqa: E402
import ifc_export  # noqa: E402
import ready_gate  # noqa: E402


def _load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


studio_gen = _load("studio_gen_m8", ROOT / "examples" / "studio-flat" / "generate.py")
eyewear_gen = _load("eyewear_gen", ROOT / "examples" / "eyewear" / "generate.py")
BODYFIT = yaml.safe_load((ROOT / "data" / "bodyfit.yml").read_text())


# ---- M8: IFC export ---------------------------------------------------------

def test_ifc_round_trips_the_golden_studio():
    layout = studio_gen.studio()
    problems = ifc_export.round_trip_ok(layout, ifc_export.write_ifc(layout))
    assert not problems, problems


def test_ifc_is_deterministic():
    layout = studio_gen.studio()
    assert ifc_export.write_ifc(layout) == ifc_export.write_ifc(layout)


def test_ifc_carries_spatial_structure():
    ifc = ifc_export.write_ifc(studio_gen.studio())
    for marker in ("IFCPROJECT", "IFCSITE", "IFCBUILDING", "IFCBUILDINGSTOREY",
                   "IFCSPACE", "IFCDOOR", "IFCQUANTITYAREA", "FILE_SCHEMA(('IFC4'))"):
        assert marker in ifc, marker
    assert ifc.count("IFCSPACE(") == len(studio_gen.studio()["rooms"])


def test_corrupted_ifc_fails_round_trip():
    layout = studio_gen.studio()
    ifc = ifc_export.write_ifc(layout)
    broken = ifc.replace("'kitchen'", "'kitchne'", 1)
    assert any("kitchen" in p for p in ifc_export.round_trip_ok(layout, broken))


def test_ifcopenshell_absence_is_reported_not_hidden(tmp_path):
    p = tmp_path / "x.ifc"
    p.write_text(ifc_export.write_ifc(studio_gen.studio()))
    msg = ifc_export.ifcopenshell_check(str(p))
    assert "SKIPPED" in msg or "ifcopenshell" in msg  # honest either way


# ---- M11: body-fit gate -----------------------------------------------------

def test_golden_fitspec_is_ready():
    report = bodyfit_gate.run_gate(eyewear_gen.fitspec(), BODYFIT)
    assert report["ready"], report


def test_golden_temple_passes_the_print_gate(tmp_path):
    stl = tmp_path / "temple.stl"
    eyewear_gen.write_stl(str(stl), eyewear_gen.temple())
    report = ready_gate.run_gate(str(stl), (220.0, 220.0, 250.0), 0.4,
                                 eyewear_gen.TEMPLE_W)
    assert report["ready"], report


def test_missing_dimension_is_not_measured_therefore_fails():
    spec = eyewear_gen.fitspec()
    del spec["dimensions"]["bridge"]
    report = bodyfit_gate.run_gate(spec, BODYFIT)
    assert not report["gates"]["B1_completeness"]["pass"]


def test_out_of_range_pd_fails():
    spec = eyewear_gen.fitspec()
    spec["dimensions"]["pd"] = 90
    report = bodyfit_gate.run_gate(spec, BODYFIT)
    assert not report["gates"]["B2_ranges"]["pass"]


def test_misaligned_frame_fails_optical_rule():
    spec = eyewear_gen.fitspec()
    spec["dimensions"]["lens_w"] = 58   # frame PD 76 vs wearer 63 -> offset 13
    report = bodyfit_gate.run_gate(spec, BODYFIT)
    assert not report["gates"]["B3_alignment"]["pass"]


def test_thin_temple_fails_print_floor():
    spec = eyewear_gen.fitspec()
    spec["min_feature"] = 1.0
    report = bodyfit_gate.run_gate(spec, BODYFIT)
    assert not report["gates"]["B4_printability"]["pass"]


def test_unknown_product_fails():
    spec = eyewear_gen.fitspec()
    spec["product"] = "helmet"
    report = bodyfit_gate.run_gate(spec, BODYFIT)
    assert not report["ready"]


# ---- M9: knowledge graph ----------------------------------------------------

def test_graph_compiles_and_is_committed_fresh():
    r = subprocess.run([sys.executable, str(ROOT / "scripts" / "build_graph.py"),
                        "--check"], capture_output=True, text=True)
    assert r.returncode == 0, r.stdout


def test_graph_covers_the_data_spine():
    g = json.loads((ROOT / "docs" / "graph.json").read_text())
    kinds = {n["kind"] for n in g["nodes"]}
    assert {"root", "gate", "tool", "paper", "skill"} <= kinds
    assert g["counts"]["nodes"] > 100
    ids = {n["id"] for n in g["nodes"]}
    for e in g["edges"]:
        assert e["source"] in ids and e["target"] in ids, e


def test_map_page_exists_and_loads_the_graph():
    html = (ROOT / "docs" / "map.html").read_text()
    assert 'fetch("graph.json")' in html
