"""Satellite integrity: pointers + SHA-pinned digests + compiled skills.

The honesty core: a digest must be pinned to the sha it was written against,
the pin must match what satellites.yml records, and staleness must be a
computed status, never a hand-typed claim.
"""

import subprocess
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
SAT = yaml.safe_load((ROOT / "data" / "satellites.yml").read_text())


def test_every_repo_marked_tool_has_a_satellite():
    tools = yaml.safe_load((ROOT / "data" / "tools.yml").read_text())
    marked = {e["repo"] for e in tools if "repo" in e}
    assert marked == {s["repo"] for s in SAT}
    assert len(marked) >= 5


def test_satellite_schema():
    for s in SAT:
        for key in ("repo", "slug", "name", "head_sha", "fetched_at", "status",
                    "stars", "license"):
            assert key in s, (s.get("repo"), key)
        assert s["status"] in ("fresh", "STALE", "no-digest")


def test_status_is_computed_not_claimed():
    for s in SAT:
        want = ("no-digest" if not s["digest_sha"] else
                "fresh" if s["digest_sha"] == s["head_sha"] else "STALE")
        assert s["status"] == want, s["repo"]


def test_generated_skills_match_data():
    r = subprocess.run([sys.executable, str(ROOT / "scripts" / "satellites.py"),
                        "build", "--check"], capture_output=True, text=True)
    assert r.returncode == 0, r.stdout


def test_digests_exist_and_quote_their_pin():
    for s in SAT:
        knowledge = ROOT / "skills" / f"use-{s['slug']}" / "KNOWLEDGE.md"
        assert knowledge.exists(), f"{s['slug']}: no KNOWLEDGE.md digest"
        text = knowledge.read_text()
        assert s["digest_sha"], f"{s['slug']}: digest exists but digest_sha not pinned in satellites.yml"
        assert s["digest_sha"] in text, \
            f"{s['slug']}: KNOWLEDGE.md does not quote its pinned sha {s['digest_sha']}"
        assert len(text) > 1500, f"{s['slug']}: digest suspiciously thin"


def test_satellites_never_vendor_code():
    for s in SAT:
        d = ROOT / "skills" / f"use-{s['slug']}"
        files = {p.name for p in d.iterdir() if p.is_file()}
        assert files <= {"SKILL.md", "KNOWLEDGE.md"}, \
            f"{s['slug']}: satellites are pointers+digests, never vendored code: {files}"
