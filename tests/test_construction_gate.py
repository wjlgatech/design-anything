"""The construction gate must pass the golden studio flat and fail known-bad
layouts. Maker != checker: generator and gate are independent code paths."""

import importlib.util
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "pipeline"))

import construction_gate  # noqa: E402


def _load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


# load by path under a unique name (both examples ship a generate.py)
studio_gen = _load("studio_generate", ROOT / "examples" / "studio-flat" / "generate.py")

TABLES = yaml.safe_load((ROOT / "data" / "clearances.yml").read_text())


def golden():
    return studio_gen.studio()


def test_golden_studio_is_ready():
    report = construction_gate.run_gate(golden(), TABLES)
    assert report["ready"], report


def test_narrow_entry_door_fails_clearance_and_egress():
    layout = golden()
    layout["openings"][0]["width"] = 700
    report = construction_gate.run_gate(layout, TABLES)
    assert not report["gates"]["C2_clearances"]["pass"]
    assert not report["gates"]["C4_egress"]["pass"]  # no entry-grade door left


def test_habitable_room_without_daylight_fails():
    layout = golden()
    living = next(r for r in layout["rooms"] if r["name"] == "living")
    living["windows"] = 0
    report = construction_gate.run_gate(layout, TABLES)
    assert not report["gates"]["C3_habitability"]["pass"]


def test_undersized_room_fails():
    layout = golden()
    kitchen = next(r for r in layout["rooms"] if r["name"] == "kitchen")
    kitchen["polygon"] = [[0, 0], [1500, 0], [1500, 1500], [0, 1500]]
    report = construction_gate.run_gate(layout, TABLES)
    assert not report["gates"]["C3_habitability"]["pass"]


def test_unreachable_room_fails_egress():
    layout = golden()
    layout["openings"] = [o for o in layout["openings"]
                          if o["between"] != ["hall", "bathroom"]]
    report = construction_gate.run_gate(layout, TABLES)
    assert not report["gates"]["C4_egress"]["pass"]
    assert "bathroom" in report["gates"]["C4_egress"]["detail"]


def test_off_module_dimensions_fail_grid():
    layout = golden()
    for r in layout["rooms"]:
        r["polygon"] = [[x + 37, y + 37] for x, y in r["polygon"]]
    report = construction_gate.run_gate(layout, TABLES)
    assert not report["gates"]["C5_module_grid"]["pass"]


def test_low_ceiling_fails_habitability():
    layout = golden()
    layout["ceiling_height"] = 2100
    report = construction_gate.run_gate(layout, TABLES)
    assert not report["gates"]["C3_habitability"]["pass"]


def test_unknown_room_type_is_not_measured_therefore_fails():
    layout = golden()
    layout["rooms"][0]["type"] = "man-cave"
    report = construction_gate.run_gate(layout, TABLES)
    assert not report["gates"]["C3_habitability"]["pass"]


def test_report_carries_disclaimer():
    report = construction_gate.run_gate(golden(), TABLES)
    assert "not a permit" in report["disclaimer"]
