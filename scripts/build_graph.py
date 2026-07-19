#!/usr/bin/env python3
"""build_graph.py — compile data/*.yml into the knowledge graph.

Emits docs/graph.json (nodes + edges) for the interactive map (docs/map.html).
Deterministic: same data, byte-identical graph — so `--check` is a drift gate,
same contract as build_readme.py. Humans edit YAML, never the graph.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"
OUT = ROOT / "docs" / "graph.json"

GATES = ["ready_gate", "construction_gate", "pattern_gate", "scene_gate", "bodyfit_gate"]


def load(name: str) -> list:
    return yaml.safe_load((DATA / name).read_text())


def build() -> dict:
    nodes: list[dict] = [{"id": "design-anything", "kind": "root",
                          "url": "https://github.com/wjlgatech/design-anything"}]
    edges: list[dict] = []
    hubs: set[str] = set()

    def hub(name: str, kind: str) -> str:
        hid = f"{kind}:{name}"
        if hid not in hubs:
            hubs.add(hid)
            nodes.append({"id": hid, "label": name, "kind": kind})
            edges.append({"source": hid, "target": "design-anything", "rel": "part-of"})
        return hid

    for gate in GATES:
        nodes.append({"id": gate, "kind": "gate",
                      "url": f"https://github.com/wjlgatech/design-anything/blob/main/pipeline/{gate}.py"})
        edges.append({"source": gate, "target": "design-anything", "rel": "verifies-for"})

    for e in load("tools.yml"):
        nodes.append({"id": e["name"], "kind": "tool", "tier": e.get("tier"), "url": e["url"]})
        edges.append({"source": e["name"], "target": hub(e["category"], "category"),
                      "rel": "in-category"})
    for e in load("papers.yml"):
        nodes.append({"id": e["name"], "kind": "paper", "tier": e.get("tier"), "url": e["url"]})
        edges.append({"source": e["name"], "target": hub(e["category"], "category"),
                      "rel": "in-category"})
    for e in load("community.yml"):
        nodes.append({"id": e["name"], "kind": e.get("kind", "person"), "url": e["url"]})
        edges.append({"source": e["name"], "target": hub(e.get("domain", "misc"), "domain"),
                      "rel": "shapes"})
    for e in load("registry.yml"):
        nodes.append({"id": e["name"], "kind": "skill", "url": e["url"]})
        edges.append({"source": e["name"], "target": "design-anything", "rel": "skill-of"})
        matching = [g for g in GATES if e["name"].replace("-ready-check", "") in g
                    or g.split("_")[0] in e["name"]]
        for g in matching:
            edges.append({"source": e["name"], "target": g, "rel": "runs"})

    return {"generated_from": "data/*.yml by scripts/build_graph.py",
            "counts": {"nodes": len(nodes), "edges": len(edges)},
            "nodes": nodes, "edges": edges}


def main() -> None:
    generated = json.dumps(build(), indent=1, sort_keys=True) + "\n"
    if "--check" in sys.argv:
        current = OUT.read_text() if OUT.exists() else ""
        if generated != current:
            print("build_graph: DRIFT — docs/graph.json does not match data/*.yml; run `make graph`")
            sys.exit(1)
        print("build_graph: OK (no drift)")
        return
    OUT.write_text(generated)
    g = build()
    print(f"build_graph: docs/graph.json regenerated "
          f"({g['counts']['nodes']} nodes, {g['counts']['edges']} edges)")


if __name__ == "__main__":
    main()
